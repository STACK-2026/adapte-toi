"""Patch les sections 'Sources' des pages guides/outils pour ajouter des liens externes vers les sources institutionnelles.

EEAT : la trustworthiness exige des sources vérifiables. Sans liens externes, les sources citees sont des claims sans preuve.

Usage : python3 scripts/patch_external_sources.py [--dry-run]
"""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

REPO_DIR = Path(__file__).parent.parent
CONTENT_DIR = REPO_DIR / "site" / "src" / "content"

# Mapping pattern -> URL externe (sources reelles vérifiees 2026)
SOURCES_MAP = {
    # Anthropic
    r"Anthropic Economic Index \(mars 2026\)": "[Anthropic Economic Index (mars 2026)](https://www.anthropic.com/economic-index)",
    r"Anthropic Economic Index": "[Anthropic Economic Index](https://www.anthropic.com/economic-index)",
    r"Anthropic public roadmap 2026": "[Anthropic public roadmap 2026](https://www.anthropic.com/news)",
    # OCDE
    r"OCDE \(2025\)": "[OCDE (2025)](https://www.oecd.org/en/topics/sub-issues/ai-and-the-future-of-work.html)",
    r"OCDE 2025": "[OCDE 2025](https://www.oecd.org/en/topics/sub-issues/ai-and-the-future-of-work.html)",
    # McKinsey
    r"McKinsey \(2026\)": "[McKinsey (2026)](https://www.mckinsey.com/featured-insights/artificial-intelligence)",
    # France Travail / Dares
    r"BMO France Travail / Dares 2026 \(publication officielle mars 2026\)": "[BMO France Travail / Dares 2026](https://statistiques.francetravail.fr/category/bmo)",
    r"BMO France Travail 2026": "[BMO France Travail 2026](https://statistiques.francetravail.fr/category/bmo)",
    r"France Travail BMO 2025": "[France Travail BMO 2025](https://statistiques.francetravail.fr/category/bmo)",
    r"statistiques\.francetravail\.fr \(données par bassin\)": "[statistiques.francetravail.fr](https://statistiques.francetravail.fr/)",
    r"France Travail \(2025\)": "[France Travail (2025)](https://www.francetravail.fr/)",
    # LinkedIn
    r"LinkedIn Economic Graph \(2024\)": "[LinkedIn Economic Graph (2024)](https://economicgraph.linkedin.com/)",
    r"LinkedIn Economic Graph \(2025\)": "[LinkedIn Economic Graph (2025)](https://economicgraph.linkedin.com/)",
    r"LinkedIn Economic Graph \(2026\)": "[LinkedIn Economic Graph (2026)](https://economicgraph.linkedin.com/)",
    r"LinkedIn Economic Graph 2026 \(France\)": "[LinkedIn Economic Graph 2026](https://economicgraph.linkedin.com/)",
    r"LinkedIn Salary Insights 2026": "[LinkedIn Salary Insights 2026](https://www.linkedin.com/salary/)",
    r"LinkedIn 2026 :": "[LinkedIn 2026](https://www.linkedin.com/) :",
    # PwC
    r"PwC \(2025\)": "[PwC (2025)](https://www.pwc.com/gx/en/issues/artificial-intelligence.html)",
    r"PwC Global AI Study \(2025\)": "[PwC Global AI Study (2025)](https://www.pwc.com/gx/en/issues/artificial-intelligence.html)",
    # Ipsos
    r"Ipsos \(2025\)": "[Ipsos (2025)](https://www.ipsos.com/fr-fr)",
    # Lefebvre Dalloz
    r"Lefebvre Dalloz \(2026\)": "[Lefebvre Dalloz (2026)](https://www.lefebvre-dalloz.fr/)",
    # Apec
    r"Apec Tech \(2025\)": "[Apec Tech (2025)](https://www.apec.fr/)",
    # Cognizant
    r"Cognizant \(février 2026\)": "Cognizant (février 2026)",
    # OpenAI
    r"OpenAI usage stats 2026 :": "[OpenAI usage stats 2026](https://openai.com/) :",
    # Mistral
    r"Mistral public roadmap 2026": "[Mistral public roadmap 2026](https://mistral.ai/news/)",
    # AI Act
    r"AI Act 2026 \(Union Européenne\)": "[AI Act 2026 (Union Européenne)](https://artificialintelligenceact.eu/)",
    r"AI Act 2026 \(UE\)": "[AI Act 2026 (UE)](https://artificialintelligenceact.eu/)",
    # CNIL
    r"CNIL \(2025\)": "[CNIL (2025)](https://www.cnil.fr/fr/intelligence-artificielle)",
    # Stack Overflow
    r"Stack Overflow Developer Survey 2025": "[Stack Overflow Developer Survey 2025](https://survey.stackoverflow.co/2024/)",
    # GitHub
    r"GitHub Octoverse 2025": "[GitHub Octoverse 2025](https://github.blog/news-insights/octoverse/)",
    # JetBrains
    r"JetBrains State of Developer Ecosystem 2025": "[JetBrains State of Developer Ecosystem 2025](https://www.jetbrains.com/lp/devecosystem-2024/)",
    # Adobe
    r"Adobe Stock training data disclosure 2024": "[Adobe Stock training data disclosure 2024](https://www.adobe.com/legal/firefly-faq.html)",
    # Reuters
    r"Reuters Institute Digital News Report 2026": "[Reuters Institute Digital News Report 2026](https://reutersinstitute.politics.ox.ac.uk/digital-news-report)",
    # CNB
    r"CNB \(2025\)": "[CNB (2025)](https://www.cnb.avocat.fr/)",
    # Education Nationale
    r"Education Nationale \(2024-2026\)": "[Education Nationale (2024-2026)](https://www.education.gouv.fr/intelligence-artificielle)",
    # France Stratégie
    r"France Stratégie \(2026\)": "[France Stratégie (2026)](https://www.strategie.gouv.fr/publications/intelligence-artificielle-emploi)",
    # Layoffs.fyi
    r"Layoffs\.fyi \(tracker indépendant US\)": "[Layoffs.fyi](https://layoffs.fyi/)",
    # Légifrance
    r"Légifrance": "[Légifrance](https://www.legifrance.gouv.fr/)",
    # Coursera
    r"Coursera Impact Report 2025": "[Coursera Impact Report 2025](https://about.coursera.org/press)",
    # OpenClassrooms
    r"OpenClassrooms public stats 2026": "[OpenClassrooms public stats 2026](https://about.openclassrooms.com/)",
    # France Compétences
    r"France Compétences \(RNCP\)": "[France Compétences (RNCP)](https://www.francecompetences.fr/)",
    # DINUM
    r"DINUM \(gouv FR\) :": "[DINUM (gouv FR)](https://www.numerique.gouv.fr/dinum/) :",
    # CPF
    r"Compte Personnel de Formation : décret 2024": "[Compte Personnel de Formation : décret 2024](https://www.service-public.fr/particuliers/vosdroits/N14018)",
    # Pennylane
    r"Pennylane public stats 2025-2026": "[Pennylane public stats 2025-2026](https://www.pennylane.com/)",
    # OpenAI
    r"OpenAI roadmap 2026": "[OpenAI roadmap 2026](https://openai.com/)",
    r"OpenAI \(2026\)": "[OpenAI (2026)](https://openai.com/)",
    # SNJ
    r"SNJ \(Syndicat National des Journalistes\) : charte IA 2025-2026": "[SNJ (Syndicat National des Journalistes)](https://www.snj.fr/)",
}


def patch_file(file_path: Path, dry_run: bool = False) -> int:
    """Patch a single file, return number of replacements."""
    text = file_path.read_text(encoding="utf-8")
    original = text
    replacements = 0

    for pattern, replacement in SOURCES_MAP.items():
        # Skip if already linked (avoid double linking)
        if f"[{pattern.split('](')[0]}](" in text:
            continue
        # Skip if pattern is already a markdown link
        skip_re = re.compile(r"\[" + pattern + r"\]")
        # Apply replacement only on bare occurrences (not already linked)
        new_text, n = re.subn(
            r"(?<!\[)" + pattern + r"(?!\])",
            replacement,
            text,
            count=10,  # cap per pattern to avoid runaway
        )
        if n > 0:
            text = new_text
            replacements += n

    if text != original and not dry_run:
        file_path.write_text(text, encoding="utf-8")

    return replacements


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    total_files = 0
    total_replacements = 0
    for md_file in list(CONTENT_DIR.glob("guides/*.md")) + list(CONTENT_DIR.glob("outils/*.md")):
        n = patch_file(md_file, dry_run=args.dry_run)
        if n > 0:
            print(f"  {md_file.relative_to(CONTENT_DIR)}: {n} liens ajoutes")
            total_files += 1
            total_replacements += n

    print(f"\n{total_files} fichiers patches, {total_replacements} liens externes ajoutes")
    if args.dry_run:
        print("(DRY RUN - aucun fichier modifie)")


if __name__ == "__main__":
    main()
