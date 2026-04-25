"""SERP briefs Gemini 2.5 Pro pour les pages comparator Tier 1 (Phase 1, plan visibilite acceleree 25/04).

Reutilise la fonction gemini_serp_brief() de serp_brief.py et l'applique a une liste
de keywords cibles definie en dur, sortie JSON dans docs/seo-plans/.

Usage : python3 scripts/serp_brief_comparators.py
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
OUTPUT_FILE = REPO_DIR / "docs" / "seo-plans" / "serp-briefs-2026-04-25.json"

# Keywords cibles : 1 keyword principal par comparator
KEYWORDS = [
    {
        "slug": "perplexity-vs-chatgpt",
        "keyword": "perplexity vs chatgpt",
        "secondary_keywords": ["perplexity ai en français", "perplexity ou chatgpt"],
    },
    {
        "slug": "cursor-vs-github-copilot",
        "keyword": "cursor vs github copilot",
        "secondary_keywords": ["cursor en français", "cursor ide"],
    },
    {
        "slug": "claude-vs-chatgpt",
        "keyword": "claude vs chatgpt",
        "secondary_keywords": ["claude en français", "claude ou chatgpt"],
    },
    {
        "slug": "perplexity-vs-google",
        "keyword": "perplexity vs google",
        "secondary_keywords": ["remplacer google par perplexity"],
    },
    {
        "slug": "midjourney-vs-dalle-vs-firefly",
        "keyword": "midjourney vs dalle",
        "secondary_keywords": ["meilleur generateur image ia"],
    },
    {
        "slug": "notion-ai-vs-chatgpt",
        "keyword": "notion ai vs chatgpt",
        "secondary_keywords": ["notion ai en français"],
    },
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("serp_brief_comparators")


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
                "secondary_keywords": entry["secondary_keywords"],
                "generated_at": time.strftime("%Y-%m-%dT%H:%M:%S"),
                "brief": brief,
            }
            existing["briefs"] = briefs
            existing["generated_at"] = time.strftime("%Y-%m-%dT%H:%M:%S")
            OUTPUT_FILE.write_text(
                json.dumps(existing, ensure_ascii=False, indent=2) + "\n",
                encoding="utf-8",
            )
            log.info(f"  saved brief for {slug} ({len(brief.get('top10', []))} top results)")
            time.sleep(3)
        except Exception as e:
            log.error(f"[{slug}] {e}")
            continue

    log.info(f"output: {OUTPUT_FILE}")


if __name__ == "__main__":
    main()
