"""SERP briefs Gemini 2.5 Pro pour les 25 fiches metiers (V2 enrichissement)."""
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
OUTPUT_FILE = REPO_DIR / "docs" / "seo-plans" / "serp-briefs-metiers-2026-04-26.json"

KEYWORDS = [
    {"slug": "comptable-ia", "keyword": "comptable et intelligence artificielle 2026"},
    {"slug": "avocat-ia", "keyword": "avocat intelligence artificielle 2026"},
    {"slug": "marketing-ia", "keyword": "marketeur ia metier 2026"},
    {"slug": "commercial-ia", "keyword": "commercial b2b ia metier 2026"},
    {"slug": "rh-recruteur-ia", "keyword": "rh recruteur ia metier 2026"},
    {"slug": "developpeur-ia", "keyword": "developpeur ia metier salaire 2026"},
    {"slug": "enseignant-ia", "keyword": "enseignant intelligence artificielle 2026"},
    {"slug": "consultant-ia", "keyword": "consultant ia metier 2026"},
    {"slug": "journaliste-ia", "keyword": "journaliste intelligence artificielle 2026"},
    {"slug": "graphiste-ia", "keyword": "graphiste ia metier 2026"},
    {"slug": "community-manager-ia", "keyword": "community manager ia 2026"},
    {"slug": "data-analyst-ia", "keyword": "data analyst ia metier 2026"},
    {"slug": "analyste-financier-ia", "keyword": "analyste financier ia 2026"},
    {"slug": "chef-de-projet-ia", "keyword": "chef de projet ia 2026"},
    {"slug": "copywriter-ia", "keyword": "copywriter ia metier 2026"},
    {"slug": "assistant-administratif-ia", "keyword": "assistant administratif ia 2026"},
    {"slug": "charge-clientele-ia", "keyword": "charge clientele ia 2026"},
    {"slug": "agent-immobilier-ia", "keyword": "agent immobilier ia 2026"},
    {"slug": "architecte-ia", "keyword": "architecte ia metier 2026"},
    {"slug": "infirmier-ia", "keyword": "infirmier intelligence artificielle 2026"},
    {"slug": "cuisinier-ia", "keyword": "cuisinier intelligence artificielle 2026"},
    {"slug": "plombier-ia", "keyword": "plombier intelligence artificielle 2026"},
    {"slug": "agriculteur-ia", "keyword": "agriculteur intelligence artificielle 2026"},
    {"slug": "photographe-ia", "keyword": "photographe ia metier 2026"},
    {"slug": "traducteur-ia", "keyword": "traducteur ia metier 2026"},
]

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
log = logging.getLogger("serp_brief_metiers")


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
        log.info(f"[{slug}] requesting brief for: {entry['keyword']}")
        try:
            brief = gemini_serp_brief(entry["keyword"])
            briefs[slug] = {
                "keyword": entry["keyword"],
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
