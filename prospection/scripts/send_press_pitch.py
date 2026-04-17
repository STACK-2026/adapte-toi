#!/usr/bin/env python3
"""
Envoi des pitches presse Baromètre Adapte-toi via Resend.

Usage:
    export RESEND_API_KEY="re_xxx"
    python3 scripts/send_press_pitch.py --dry-run --touch T1
    python3 scripts/send_press_pitch.py --touch T1 --batch 5

Le script lit `journalists.csv` (que l'utilisateur edite), match le template
correspondant au `touch` demandé, personnalise via les champs {first_name},
{recent_article}, {recent_url}, et envoie via l'API Resend.

Un fichier `sent_log.csv` garde trace des envois (anti-doublon).
"""
from __future__ import annotations

import argparse
import csv
import os
import re
import sys
import time
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    sys.exit("pip install requests")


ROOT = Path(__file__).resolve().parent.parent
CSV_FILE = ROOT / "journalists.csv"
SENT_LOG = ROOT / "sent_log.csv"
TEMPLATES_DIR = ROOT / "templates"

FROM_NAME = "Lea · Rédaction Adapte-toi"
FROM_EMAIL = "presse@adapte-toi.com"
REPLY_TO = "presse@adapte-toi.com"

TEMPLATES = {
    "T1": TEMPLATES_DIR / "t1-decouverte.md",
    "T2": TEMPLATES_DIR / "t2-relance-angle.md",
    "T3": TEMPLATES_DIR / "t3-breakup.md",
}


def load_template(touch: str) -> tuple[str, str]:
    """Returns (subject, body) extracted from markdown template."""
    fp = TEMPLATES[touch]
    raw = fp.read_text(encoding="utf-8")
    # Split: subject lines before '---', body after
    parts = raw.split("\n---\n", 1)
    if len(parts) != 2:
        sys.exit(f"Template {fp.name} invalide: pas de '---' separateur")
    header, body = parts
    # Pick first bullet line starting with '- `'
    subject_match = re.search(r"- `([^`]+)`", header)
    subject = subject_match.group(1) if subject_match else f"Adapte-toi {touch}"
    return subject.strip(), body.strip()


def load_journalists() -> list[dict]:
    if not CSV_FILE.exists():
        sys.exit(f"Fichier manquant: {CSV_FILE}. Copie journalists.example.csv.")
    with CSV_FILE.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def load_sent() -> set[tuple[str, str]]:
    if not SENT_LOG.exists():
        return set()
    with SENT_LOG.open(encoding="utf-8") as f:
        return {(row["email"], row["touch"]) for row in csv.DictReader(f)}


def log_sent(email: str, touch: str, subject: str) -> None:
    exists = SENT_LOG.exists()
    with SENT_LOG.open("a", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        if not exists:
            w.writerow(["email", "touch", "subject", "sent_at"])
        w.writerow([email, touch, subject, datetime.now().isoformat()])


def personalize(text: str, row: dict) -> str:
    out = text
    for key in ("first_name", "last_name", "outlet", "recent_article", "recent_url", "beat"):
        out = out.replace("{" + key + "}", row.get(key, "") or "")
        out = out.replace("{Prénom}", row.get("first_name", "") or "bonjour")
    # Fallback si pas d'article recent
    if "{titre_article_récent}" in out:
        fallback = row.get("recent_article") or f"votre dernier papier dans {row.get('outlet', '')}"
        out = out.replace("{titre_article_récent}", fallback)
    if "{sujet_original}" in out:
        out = out.replace("{sujet_original}", "chiffre propriétaire IA et emploi")
    return out


def md_to_html(md: str) -> str:
    """Simple markdown -> HTML (paragraphes + blockquotes + liens + bold)."""
    html = md
    # Blockquotes
    html = re.sub(r"^> (.+)$", r'<blockquote style="border-left:3px solid #E63946;padding:4px 12px;margin:16px 0;color:#374151;">\1</blockquote>', html, flags=re.MULTILINE)
    # Bold
    html = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", html)
    # Links (markdown autolinks)
    html = re.sub(r"(https?://[^\s<]+)", r'<a href="\1">\1</a>', html)
    # Paragraphes (double newline)
    paragraphs = [p.strip() for p in html.split("\n\n") if p.strip()]
    html = "\n".join(f"<p>{p.replace(chr(10), '<br>')}</p>" if not p.startswith("<blockquote") else p for p in paragraphs)
    return f'<div style="font-family:Inter,Arial,sans-serif;font-size:15px;line-height:1.6;color:#1a1a2e;max-width:600px;">{html}</div>'


def send_email(to: str, subject: str, body_md: str, dry_run: bool) -> bool:
    body_html = md_to_html(body_md)
    if dry_run:
        print(f"[DRY] To: {to}")
        print(f"[DRY] Subject: {subject}")
        print(f"[DRY] Body:\n{body_md[:400]}...\n")
        return True
    key = os.getenv("RESEND_API_KEY", "")
    if not key:
        sys.exit("RESEND_API_KEY manquant. export RESEND_API_KEY=re_xxx")
    try:
        r = requests.post(
            "https://api.resend.com/emails",
            headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
            json={
                "from": f"{FROM_NAME} <{FROM_EMAIL}>",
                "to": [to],
                "reply_to": REPLY_TO,
                "subject": subject,
                "html": body_html,
                "text": body_md,
            },
            timeout=30,
        )
        if r.status_code not in (200, 201):
            print(f"Resend KO {r.status_code}: {r.text}")
            return False
        print(f"OK → {to}")
        return True
    except Exception as e:
        print(f"Send failed {to}: {e}")
        return False


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--touch", choices=["T1", "T2", "T3"], required=True)
    ap.add_argument("--batch", type=int, default=0, help="Limit nb envois")
    ap.add_argument("--dry-run", action="store_true", default=True, help="Mode test (default)")
    ap.add_argument("--send", dest="dry_run", action="store_false", help="Envoi reel")
    args = ap.parse_args()

    subject_tpl, body_tpl = load_template(args.touch)
    journalists = load_journalists()
    sent = load_sent()

    todo = [j for j in journalists if j.get("email") and (j["email"], args.touch) not in sent]
    if args.batch > 0:
        todo = todo[: args.batch]

    if not todo:
        print("Rien a envoyer (tous deja traites pour ce touch).")
        return 0

    print(f"Mode: {'DRY-RUN' if args.dry_run else 'ENVOI REEL'}")
    print(f"Touch: {args.touch}")
    print(f"Destinataires: {len(todo)}")
    print("-" * 50)

    for i, row in enumerate(todo):
        subject = personalize(subject_tpl, row)
        body = personalize(body_tpl, row)
        ok = send_email(row["email"], subject, body, args.dry_run)
        if ok and not args.dry_run:
            log_sent(row["email"], args.touch, subject)
            time.sleep(2)  # rate limiting anti-spam

    print("-" * 50)
    print(f"Termine. {len(todo)} email(s) {'simules' if args.dry_run else 'envoyes'}.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
