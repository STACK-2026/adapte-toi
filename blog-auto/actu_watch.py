#!/usr/bin/env python3
"""
Adapte-toi Décrypte - Pipeline quotidienne de décryptage d'actualités IA x emploi.

Flux:
  1. Ingestion multi-sources RSS (médias FR + orgs publiques + international)
  2. Dédup (URL + hash titre + cache state)
  3. Filtrage de pertinence via Claude Haiku (score 0-10, garde >= 7)
  4. Génération du décryptage MDX via Claude Sonnet avec le prompt Décrypte
  5. Écriture du fichier dans site/src/content/actu/ + commit git

Usage:
  python actu_watch.py                  # fetch + filtre + écrit 1 article (le mieux scoré)
  python actu_watch.py --dry-run        # ne commit pas, affiche le résultat
  python actu_watch.py --max 3          # jusqu'à 3 articles en un run
  python actu_watch.py --seed-only      # fetch + score, pas de génération (debug)
"""
from __future__ import annotations

import argparse
import hashlib
import json
import logging
import os
import re
import subprocess
import sys
import time
import unicodedata
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
REPO_DIR = SCRIPT_DIR.parent
ACTU_DIR = REPO_DIR / "site" / "src" / "content" / "actu"
PROMPT_FILE = SCRIPT_DIR / "prompts" / "actu-decrypte.md"
STATE_FILE = SCRIPT_DIR / "actu_state.json"
LOG_FILE = SCRIPT_DIR / "logs" / "actu.log"

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
CLAUDE_HAIKU = "claude-haiku-4-5-20251001"
CLAUDE_SONNET = "claude-sonnet-4-5-20251015"
CLAUDE_TIMEOUT = 240
RELEVANCE_THRESHOLD = 7

# Sources RSS. Liste robuste, tolère les 404 ponctuels.
RSS_FEEDS = [
    # FR généralistes / éco / tech
    ("Les Échos Tech", "https://services.lesechos.fr/rss/les-echos-tech-medias.xml"),
    ("Le Monde Éco", "https://www.lemonde.fr/economie/rss_full.xml"),
    ("Le Figaro Éco", "https://www.lefigaro.fr/rss/figaro_economie.xml"),
    ("France Info Éco", "https://www.francetvinfo.fr/economie.rss"),
    ("Maddyness", "https://www.maddyness.com/feed/"),
    ("Usbek & Rica", "https://usbeketrica.com/fr/rss"),
    ("Frandroid", "https://www.frandroid.com/feed"),
    ("Next INpact", "https://www.nextinpact.com/rss/news.xml"),
    ("Welcome to the Jungle", "https://www.welcometothejungle.com/fr/articles.rss"),
    ("Courrier Cadres", "https://courriercadres.com/feed/"),
    # FR institutions (publications études / chiffres)
    ("France Travail Statistiques", "https://www.francetravail.org/statistiques-analyses.rss"),
    # International cadre
    ("Financial Times Tech", "https://www.ft.com/technology?format=rss"),
    ("Reuters Tech", "https://www.reutersagency.com/feed/?best-topics=tech&post_type=best"),
    ("MIT Tech Review AI", "https://www.technologyreview.com/topic/artificial-intelligence/feed"),
    ("Anthropic News", "https://www.anthropic.com/news/rss.xml"),
    # Google News RSS searches (real-time, targets hot topics)
    ("Google News, OpenAI FR", "https://news.google.com/rss/search?q=OpenAI+OR+Altman&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google News, Anthropic FR", "https://news.google.com/rss/search?q=Anthropic+OR+Claude+AI&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google News, IA emploi FR", "https://news.google.com/rss/search?q=%22intelligence+artificielle%22+emploi+OR+licenciement&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google News, reconversion IA", "https://news.google.com/rss/search?q=reconversion+IA+OR+%22intelligence+artificielle%22+formation&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google News, automation travail", "https://news.google.com/rss/search?q=%22automation+travail%22+OR+%22IA+remplace%22+OR+%22metiers+menaces%22&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google News, Mistral FR", "https://news.google.com/rss/search?q=Mistral+AI+France&hl=fr&gl=FR&ceid=FR:fr"),
    ("Google News, chatgpt entreprise", "https://news.google.com/rss/search?q=ChatGPT+entreprise+OR+productivite&hl=fr&gl=FR&ceid=FR:fr"),
]

CATEGORY_ENUM = ["menace", "etude", "annonce", "politique", "outil", "voix", "chiffre"]

# -----------------------------------------------------------------------------
# LOGGING
# -----------------------------------------------------------------------------

LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[logging.FileHandler(LOG_FILE, encoding="utf-8"), logging.StreamHandler(sys.stdout)],
)
log = logging.getLogger(__name__)

# -----------------------------------------------------------------------------
# STATE (dedup persistant)
# -----------------------------------------------------------------------------

def load_state() -> dict:
    if STATE_FILE.exists():
        try:
            return json.loads(STATE_FILE.read_text(encoding="utf-8"))
        except Exception:
            return {"seen_urls": [], "seen_hashes": [], "published_slugs": []}
    return {"seen_urls": [], "seen_hashes": [], "published_slugs": []}


def save_state(state: dict) -> None:
    STATE_FILE.write_text(json.dumps(state, ensure_ascii=False, indent=2), encoding="utf-8")


# -----------------------------------------------------------------------------
# RSS FETCH
# -----------------------------------------------------------------------------

def fetch_rss(outlet: str, url: str) -> list[dict]:
    try:
        r = requests.get(url, timeout=20, headers={"User-Agent": "AdapteToiDecrypte/1.0 (+https://adapte-toi.com)"})
        r.raise_for_status()
        content = r.content
    except Exception as e:
        log.warning(f"RSS {outlet} KO: {e}")
        return []
    try:
        root = ET.fromstring(content)
    except ET.ParseError as e:
        log.warning(f"RSS {outlet} parse KO: {e}")
        return []
    items = []
    for item in root.iter("item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        desc = (item.findtext("description") or "").strip()
        pub = (item.findtext("pubDate") or "").strip()
        if title and link:
            items.append({"outlet": outlet, "title": title, "url": link, "summary": desc[:800], "pubDate": pub})
    # Atom fallback
    if not items:
        ns = {"a": "http://www.w3.org/2005/Atom"}
        for entry in root.iter("{http://www.w3.org/2005/Atom}entry"):
            title_el = entry.find("a:title", ns)
            link_el = entry.find("a:link", ns)
            sum_el = entry.find("a:summary", ns)
            title = (title_el.text or "").strip() if title_el is not None else ""
            link = (link_el.get("href") if link_el is not None else "") or ""
            desc = (sum_el.text or "").strip() if sum_el is not None else ""
            if title and link:
                items.append({"outlet": outlet, "title": title, "url": link, "summary": desc[:800], "pubDate": ""})
    return items


# -----------------------------------------------------------------------------
# CLAUDE
# -----------------------------------------------------------------------------

def claude_call(model: str, system: str, user: str, max_tokens: int = 1024) -> str:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY manquant")
    headers = {
        "x-api-key": ANTHROPIC_API_KEY,
        "anthropic-version": "2023-06-01",
        "content-type": "application/json",
    }
    payload = {
        "model": model,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    for attempt in range(3):
        try:
            r = requests.post("https://api.anthropic.com/v1/messages", headers=headers, json=payload, timeout=CLAUDE_TIMEOUT)
            if r.status_code in (429, 529):
                wait = 10 * (2 ** attempt)
                log.warning(f"Claude {r.status_code}, retry in {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            data = r.json()
            return data["content"][0]["text"]
        except Exception as e:
            log.warning(f"Claude call error (attempt {attempt + 1}): {e}")
            if attempt == 2:
                raise
            time.sleep(5)
    return ""


# -----------------------------------------------------------------------------
# FILTRAGE DE PERTINENCE (Haiku)
# -----------------------------------------------------------------------------

RELEVANCE_SYSTEM = """Tu es un rédacteur en chef du média Adapte-toi (FR), spécialisé IA x emploi x reconversion professionnelle.
Ton rôle : juger si une news mérite d'être décryptée pour nos lecteurs. Pas de tiède, pas de contenu générique.

PERTINENT (7-10) : études chiffrées sur IA/emploi, annonces d'entreprises qui licencient/embauchent à cause de l'IA, politiques publiques (France Travail, CPF, EU AI Act), prises de position publiques fortes, sorties de modèles majeurs qui vont changer le marché, livres/tribunes impactants, statistiques nouvelles (OCDE, INSEE, France Travail, Ipsos), vagues de reconversion documentées.

MOYEN (4-6) : news IA tech sans angle emploi direct, annonce produit sans impact marché, étude partielle.

NON PERTINENT (0-3) : crypto, gaming, politique générale, sport, people, news d'entreprise sans lien emploi/IA.

Réponds UNIQUEMENT avec un JSON strict : {"score": X, "category": "menace|etude|annonce|politique|outil|voix|chiffre", "why": "une phrase"}
"""


def score_item(item: dict) -> dict | None:
    prompt = f"Titre : {item['title']}\nSource : {item['outlet']}\nExtrait : {item['summary'][:500]}\n\nScore cette news pour Adapte-toi."
    try:
        resp = claude_call(CLAUDE_HAIKU, RELEVANCE_SYSTEM, prompt, max_tokens=200)
        m = re.search(r"\{.*\}", resp, re.DOTALL)
        if not m:
            return None
        data = json.loads(m.group(0))
        score = int(data.get("score", 0))
        cat = data.get("category", "annonce")
        if cat not in CATEGORY_ENUM:
            cat = "annonce"
        return {"score": score, "category": cat, "why": data.get("why", "")}
    except Exception as e:
        log.warning(f"Score KO pour {item['url']}: {e}")
        return None


# -----------------------------------------------------------------------------
# GÉNÉRATION DU DÉCRYPTAGE (Sonnet)
# -----------------------------------------------------------------------------

def load_decrypte_prompt() -> str:
    if PROMPT_FILE.exists():
        return PROMPT_FILE.read_text(encoding="utf-8")
    return DEFAULT_PROMPT


DEFAULT_PROMPT = """Tu es la plume de "Adapte-toi Décrypte", le média FR qui traduit les news IA x emploi x reconversion pour ses lecteurs francophones (France, Belgique, Suisse).

TON : franc, direct, zéro bullshit. Tutoiement obligatoire partout. Pas de franglais gratuit. Style inspiré de Hugo Décrypte version adulte et engagée : on ne résume pas, on prend position, on chiffre, on recommande du concret.

INTERDIT ABSOLU : tirets cadratins (— ou –). Utilise virgule, deux-points, point, ou tiret normal (-) à la place. C'est une règle non négociable.

STRUCTURE OBLIGATOIRE (en markdown, pas de H1, le titre est dans le frontmatter) :

## Le fait
(annonce brute en 2-4 paragraphes factuels)

## Ce qu'on en dit vraiment
(3 à 4 angles numérotés **Un.** **Deux.** **Trois.** **Quatre.** Chaque angle = 1 paragraphe qui décale la lecture dominante)

## Les chiffres qui comptent
(liste à puces, chaque puce commence par un chiffre en **gras**, source entre parenthèses)

## La citation qui résume tout
(blockquote markdown > avec la citation et la source *en italique*)
(2-3 lignes qui expliquent pourquoi cette citation capte tout)

## Pour toi concrètement
(Découpé en 3-4 cas "Tu es X", avec des actions précises à 90 jours max. Inclus OBLIGATOIREMENT au moins 3 liens internes vers /metiers/..., /guides/..., /outils/...)

## Le verdict Adapte-toi
(Paragraphe de conclusion qui tranche, puis 1 paragraphe de maillage interne final : "Va lire notre [guide X](/guides/...), consulte notre fiche [métier Y](/metiers/...)")

OBLIGATIONS :
- Longueur corps : 900-1400 mots
- Maillage interne : minimum 5 liens vers /metiers/<slug>, /guides/<slug>, /outils/<slug>, /actu/<slug>
- Pas de générique, on nomme les boîtes, les gens, les chiffres, les dates

SORTIE : frontmatter YAML valide + corps markdown. Aucun commentaire hors du fichier. Le frontmatter doit contenir EXACTEMENT ces champs :
---
title: "..."
description: "..." (max 260 caractères, commence par une phrase qui accroche)
date: YYYY-MM-DD (aujourd'hui)
category: "menace|etude|annonce|politique|outil|voix|chiffre"
impactLevel: 1-5 (honnête, 5 = ça change le marché)
author: "Léa Moreau"
keyQuote:
  text: "..."
  author: "..."
  context: "..."
tldr:
  - "bullet 1 (30-40 mots)"
  - "bullet 2"
  - "bullet 3"
  - "bullet 4"
sources:
  - title: "..."
    url: "..."
    outlet: "..."
    date: YYYY-MM-DD
relatedMetiers:
  - "slug-metier-1"
  - "slug-metier-2"
relatedGuides:
  - "slug-guide-1"
relatedOutils:
  - "claude"
image: "https://images.unsplash.com/..."
imageAlt: "..."
keywords: "mot-cle-1, mot-cle-2, mot-cle-3"
lastReviewed: YYYY-MM-DD (aujourd'hui)
reviewedBy: "Rédaction Adapte-toi"
draft: false
---

SLUGS DISPONIBLES (utilise EXACTEMENT ceux-ci, pas d'invention) :
Métiers : agent-immobilier-ia, agriculteur-ia, analyste-financier-ia, architecte-ia, assistant-administratif-ia, avocat-ia, charge-clientele-ia, chef-de-projet-ia, commercial-ia, community-manager-ia, comptable-ia, consultant-ia, copywriter-ia, cuisinier-ia, data-analyst-ia, developpeur-ia, enseignant-ia, graphiste-ia, infirmier-ia, journaliste-ia
Guides : automatiser-travail-ia, etudes-inutiles-que-faire, financer-formation-ia-cpf, freelance-ia-guide, ia-emploi-chiffres-cles, ia-europe-reglementation, negocier-salaire-competences-ia, prompt-engineering-debutant, reconversion-ia-guide-complet, se-former-ia-gratuitement
Outils : claude, chatgpt, perplexity, copilot, cursor, midjourney, notion-ai, gamma, zapier, make, canva-ai, elevenlabs, otter-ai, descript, hubspot, writesonic, jasper, copy-ai, surfer-seo, adobe-firefly
"""


def generate_decrypte(item: dict, relevance: dict) -> str:
    prompt = load_decrypte_prompt()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")
    user = f"""Aujourd'hui : {today}

News à décrypter :
- Titre : {item['title']}
- Outlet : {item['outlet']}
- URL : {item['url']}
- Extrait : {item['summary']}
- Catégorie suggérée : {relevance['category']}
- Pertinence : {relevance['why']}

Écris le décryptage complet selon la structure imposée. Le frontmatter doit référencer la source ci-dessus en premier dans `sources` (et tu peux ajouter 1 ou 2 sources externes crédibles). Choisis un image URL Unsplash pertinent (format https://images.unsplash.com/photo-XXX?w=1200&h=630&fit=crop&q=80).
"""
    return claude_call(CLAUDE_SONNET, prompt, user, max_tokens=8000)


# -----------------------------------------------------------------------------
# SLUGIFY + ECRITURE
# -----------------------------------------------------------------------------

def slugify(text: str, max_len: int = 80) -> str:
    text = unicodedata.normalize("NFD", text).encode("ascii", "ignore").decode("ascii")
    text = re.sub(r"[^\w\s-]", "", text.lower())
    text = re.sub(r"[\s_-]+", "-", text).strip("-")
    return text[:max_len].rstrip("-")


def extract_slug_from_mdx(mdx: str) -> str:
    m = re.search(r'^title:\s*"([^"]+)"', mdx, re.MULTILINE)
    title = m.group(1) if m else f"decrypte-{int(time.time())}"
    return slugify(title, 80)


def write_article(mdx: str, slug: str) -> Path:
    ACTU_DIR.mkdir(parents=True, exist_ok=True)
    path = ACTU_DIR / f"{slug}.md"
    # Ne JAMAIS écraser un fichier existant
    i = 2
    while path.exists():
        path = ACTU_DIR / f"{slug}-{i}.md"
        i += 1
    path.write_text(mdx, encoding="utf-8")
    return path


# -----------------------------------------------------------------------------
# GIT
# -----------------------------------------------------------------------------

def git_commit_and_push(paths: list[Path], titles: list[str]) -> bool:
    try:
        subprocess.run(["git", "-C", str(REPO_DIR), "add", *[str(p) for p in paths]], check=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "add", str(STATE_FILE)], check=False)
        msg_head = "Decrypte: " + ", ".join(titles[:2])
        if len(titles) > 2:
            msg_head += f" +{len(titles) - 2}"
        subprocess.run(["git", "-C", str(REPO_DIR), "commit", "-m", msg_head], check=True)
        subprocess.run(["git", "-C", str(REPO_DIR), "push", "origin", "main"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"Git KO: {e}")
        return False


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

def title_hash(title: str) -> str:
    return hashlib.sha1(slugify(title, 120).encode()).hexdigest()[:16]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed-only", action="store_true", help="Fetch + score, pas de génération")
    ap.add_argument("--max", type=int, default=1, help="Nombre max d'articles à générer")
    args = ap.parse_args()

    state = load_state()
    seen_urls = set(state.get("seen_urls", []))
    seen_hashes = set(state.get("seen_hashes", []))

    # 1. Fetch RSS
    all_items = []
    for outlet, url in RSS_FEEDS:
        items = fetch_rss(outlet, url)
        log.info(f"RSS {outlet}: {len(items)} items")
        all_items.extend(items)

    # 2. Dédup
    fresh = []
    for it in all_items:
        u = it["url"].split("?")[0].rstrip("/")
        h = title_hash(it["title"])
        if u in seen_urls or h in seen_hashes:
            continue
        fresh.append(it)
        seen_urls.add(u)
        seen_hashes.add(h)
    log.info(f"Fresh items: {len(fresh)} / {len(all_items)}")

    if not fresh:
        log.info("Rien de frais, on sort.")
        return 0

    # 3. Scoring Haiku (cap à 40 items pour limiter les appels)
    scored = []
    for it in fresh[:40]:
        r = score_item(it)
        if r and r["score"] >= RELEVANCE_THRESHOLD:
            scored.append({**it, **r})
    scored.sort(key=lambda x: x["score"], reverse=True)
    log.info(f"Scored >= {RELEVANCE_THRESHOLD}: {len(scored)}")

    if args.seed_only:
        for s in scored[:10]:
            log.info(f"[{s['score']}/{s['category']}] {s['title']} ({s['outlet']})")
        save_state({"seen_urls": list(seen_urls), "seen_hashes": list(seen_hashes), "published_slugs": state.get("published_slugs", [])})
        return 0

    # 4. Génération Sonnet + écriture
    published_slugs = set(state.get("published_slugs", []))
    written_paths = []
    written_titles = []
    for s in scored[: args.max]:
        try:
            mdx = generate_decrypte(s, s)
            slug = extract_slug_from_mdx(mdx)
            if slug in published_slugs:
                log.info(f"Slug déjà publié: {slug}, skip")
                continue
            if args.dry_run:
                log.info(f"[DRY] Décryptage généré pour: {s['title']}\n---\n{mdx[:500]}\n---")
                continue
            path = write_article(mdx, slug)
            log.info(f"Écrit : {path.name}")
            written_paths.append(path)
            written_titles.append(s["title"])
            published_slugs.add(slug)
        except Exception as e:
            log.error(f"Génération KO pour {s['title']}: {e}")

    # 5. Save state + git
    save_state({"seen_urls": list(seen_urls)[-5000:], "seen_hashes": list(seen_hashes)[-5000:], "published_slugs": list(published_slugs)[-2000:]})

    if written_paths and not args.dry_run:
        if git_commit_and_push(written_paths, written_titles):
            log.info(f"Push OK: {len(written_paths)} décryptage(s)")
        else:
            log.warning("Push KO, articles écrits mais pas committés")

    return 0


if __name__ == "__main__":
    sys.exit(main())
