#!/usr/bin/env python3
"""
Récap hebdo Adapte-toi Décrypte (dimanche matin).
Ramasse les articles publiés dans les 7 derniers jours, produit un article "Récap"
déterministe (sans appel LLM, coût zéro) avec titre, tldr, liens vers chaque article,
et lien vers la page /actu/semaine/[week].
"""
from __future__ import annotations

import json
import re
import subprocess
import sys
import unicodedata
from datetime import datetime, timedelta, timezone
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
ACTU_DIR = REPO_DIR / "site" / "src" / "content" / "actu"
LOG_FILE = SCRIPT_DIR / "logs" / "actu-recap.log"
LOG_FILE.parent.mkdir(parents=True, exist_ok=True)


def log(msg):
    stamp = datetime.now(timezone.utc).isoformat()
    line = f"{stamp} {msg}\n"
    print(line, end="")
    LOG_FILE.write_text((LOG_FILE.read_text() if LOG_FILE.exists() else "") + line, encoding="utf-8")


def parse_frontmatter(path: Path) -> dict | None:
    try:
        text = path.read_text(encoding="utf-8")
    except Exception:
        return None
    if not text.startswith("---"):
        return None
    m = re.match(r"^---\n(.*?)\n---", text, re.DOTALL)
    if not m:
        return None
    block = m.group(1)
    data: dict = {}
    for line in block.splitlines():
        ml = re.match(r'^(\w+):\s*"([^"]*)"', line)
        if ml:
            data[ml.group(1)] = ml.group(2)
            continue
        ml2 = re.match(r'^(\w+):\s*(\S.*)$', line)
        if ml2 and ml2.group(2) != "":
            data[ml2.group(1)] = ml2.group(2).strip()
    return data


def iso_week(d: datetime) -> str:
    y, w, _ = d.isocalendar()
    return f"{y}-W{w:02d}"


def slugify(s: str, maxlen: int = 80) -> str:
    s = unicodedata.normalize("NFD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^\w\s-]", "", s.lower())
    s = re.sub(r"[\s_-]+", "-", s).strip("-")
    return s[:maxlen].rstrip("-")


def main():
    today = datetime.now(timezone.utc)
    cutoff = today - timedelta(days=7)
    week_key = iso_week(today)

    entries = []
    for path in ACTU_DIR.glob("*.md"):
        fm = parse_frontmatter(path)
        if not fm or not fm.get("date"):
            continue
        if "recap-semaine" in path.stem:
            continue  # skip past recaps
        try:
            d = datetime.fromisoformat(fm["date"].replace("Z", "+00:00"))
            if d.tzinfo is None:
                d = d.replace(tzinfo=timezone.utc)
        except Exception:
            continue
        if d < cutoff:
            continue
        entries.append({
            "slug": path.stem,
            "title": fm.get("title", path.stem),
            "description": fm.get("description", ""),
            "category": fm.get("category", "etude"),
            "date": d,
        })

    if not entries:
        log("Pas d'articles dans les 7 derniers jours, récap skipped")
        return 0

    entries.sort(key=lambda e: e["date"], reverse=True)
    top = entries[0]

    start = cutoff.strftime("%d %B").lstrip("0")
    end = today.strftime("%d %B %Y").lstrip("0")
    recap_slug = f"recap-semaine-{week_key.lower().replace('-w', '-s')}"
    recap_path = ACTU_DIR / f"{recap_slug}.md"

    if recap_path.exists():
        log(f"Récap {recap_slug} existe déjà, skipped")
        return 0

    CATEGORY_LABELS = {
        "menace": "Menace", "etude": "Étude", "annonce": "Annonce",
        "politique": "Politique", "outil": "Outil", "voix": "Voix", "chiffre": "Chiffre",
    }

    bullets = []
    for e in entries[:7]:
        label = CATEGORY_LABELS.get(e["category"], e["category"])
        bullets.append(f'  - "{label} : {e["title"].replace(chr(34), chr(39))}"')
    bullets_yaml = "\n".join(bullets)

    links_md = "\n".join([
        f'- **{CATEGORY_LABELS.get(e["category"], e["category"])}** · [{e["title"]}](/actu/{e["slug"]})'
        for e in entries
    ])

    content = f"""---
title: "Récap semaine : {len(entries)} décryptages IA × emploi à retenir ({start} au {end})"
description: "Le résumé de la semaine sur Adapte-toi Décrypte : {len(entries)} décryptages sur l'IA, l'emploi et la reconversion. Les titres, les catégories, les liens directs."
date: {today.strftime('%Y-%m-%d')}
category: "chiffre"
impactLevel: 3
author: "Rédaction Adapte-toi"
tldr:
{bullets_yaml}
sources:
  - title: "Archive semaine {week_key} sur Adapte-toi"
    url: "https://adapte-toi.com/actu/semaine/{week_key}"
    outlet: "Adapte-toi"
    date: {today.strftime('%Y-%m-%d')}
relatedMetiers: []
relatedGuides:
  - "ia-emploi-chiffres-cles"
relatedOutils: []
keywords: "récap ia emploi, actu reconversion, semaine {week_key}"
lastReviewed: {today.strftime('%Y-%m-%d')}
reviewedBy: "Rédaction Adapte-toi"
draft: false
---

## Cette semaine, {len(entries)} décryptages

Du {start} au {end}, on a publié {len(entries)} décryptages sur l'IA, l'emploi et la reconversion. Voilà les raccourcis pour retrouver ce qui compte.

{links_md}

## Le sujet qui a le plus compté

Le décryptage à ne pas rater cette semaine : [{top['title']}](/actu/{top['slug']}). {top['description']}

## Lire la semaine en une page

Tous les décryptages de cette semaine sont compilés dans la page archive [Semaine {week_key}](/actu/semaine/{week_key}). Tu y trouveras les TL;DR, les citations clés et les liens directs vers chaque article complet.

## La semaine prochaine

On continue à publier tous les jours du lundi au samedi. Pour ne rien rater, abonne-toi au [Signal](/newsletter), notre newsletter hebdo zéro bullshit. Et pour approfondir les concepts techniques qui reviennent dans nos articles, [notre glossaire](/glossaire) détaille chaque terme avec exemple concret et source officielle.
"""

    recap_path.write_text(content, encoding="utf-8")
    log(f"Écrit : {recap_path.name}")

    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "add", str(recap_path)], check=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", f"Récap semaine {week_key}"], check=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "push", "origin", "main"], check=True)
        log("Push OK")
    except subprocess.CalledProcessError as e:
        log(f"Git KO: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
