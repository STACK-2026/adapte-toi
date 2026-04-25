"""SERP briefs Gemini 2.5 Pro pour les 7 fiches outils high-volume (Phase 2, plan visibilite acceleree).

Reutilise gemini_serp_brief() de serp_brief.py.

Usage : python3 scripts/serp_brief_outils.py
"""
from __future__ import annotations

import json
import logging
import sys
import time
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
sys.path.insert(0, str(SCRIPT_DIR))
from serp_brief import gemini_serp_brief  # noqa: E402

REPO_DIR = SCRIPT_DIR.parent
OUTPUT_FILE = REPO_DIR / "docs" / "seo-plans" / "serp-briefs-outils-2026-04-26.json"

KEYWORDS = [
    {"slug": "perplexity", "keyword": "perplexity ai en français"},
    {"slug": "chatgpt", "keyword": "chatgpt en français"},
    {"slug": "claude", "keyword": "claude ia en français"},
    {"slug": "cursor", "keyword": "cursor ide en français"},
    {"slug": "midjourney", "keyword": "midjourney prix avis"},
    {"slug": "notion-ai", "keyword": "notion ai avis"},
    {"slug": "copilot", "keyword": "github copilot en français"},
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("serp_brief_outils")


def main() -> None:
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    if OUTPUT_FILE.exists():
        existing = json.loads(OUTPUT_FILE.read_text(encoding="utf-8"))
    else:
        existing = {"generated_at": "", "briefs": {}}

    briefs = existing.get("briefs", {})

    for entry in KEYWORDS:
        slug = entry["slug"]
        if slug in briefs and briefs[slug].get("brief"):
            log.info(f"skip {slug} (already enriched)")
            continue
        keyword = entry["keyword"]
        log.info(f"[{slug}] requesting brief for: {keyword}")
        try:
            brief = gemini_serp_brief(keyword)
            briefs[slug] = {
                "keyword": keyword,
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "brief": brief,
            }
            existing["briefs"] = briefs
            existing["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            OUTPUT_FILE.write_text(
                json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            log.info(f"  saved brief for {slug}")
            time.sleep(3)
        except Exception as e:
            log.error(f"[{slug}] {e}")
            continue

    log.info(f"output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
