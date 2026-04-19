#!/usr/bin/env python3
"""
Adapte-toi Décrypte, pipeline Mistral + Claude-audit.

Optimise le coût Claude en déléguant 95% du travail à Mistral et en gardant
Claude uniquement comme auditeur factuel sur le draft final. Flow:

  1. Fetch RSS (réutilise RSS_FEEDS de actu_watch.py)
  2. Dédup via actu_state.json (partagé avec actu_watch.py)
  3. Scoring Mistral-small (remplace Haiku)
  4. Fetch body des top candidats (quality gate 1500 chars min)
  5. Rédaction Mistral-large avec les bodies réels (ground truth)
  6. Audit grounding Claude Sonnet (détecte hallucinations)
  7. Fix Mistral-large sur les claims flaggés
  8. Re-audit Claude Sonnet, si toujours MAJOR -> abort
  9. Post-process déterministe (tirets cadratins, apos typo, longueur)
 10. Validation règles déterministe (slugs, sections, liens, signature)
 11. Write + git commit/push

Usage:
  python actu_watch_mistral.py                # 1 article, commit
  python actu_watch_mistral.py --dry-run      # pas de commit
  python actu_watch_mistral.py --max 2        # jusqu'a 2 articles
  python actu_watch_mistral.py --strict       # abort si audit MAJOR final

Variables d'env:
  MISTRAL_API_KEY       requis
  ANTHROPIC_API_KEY     requis (audit uniquement)
"""
from __future__ import annotations

import argparse
import json
import logging
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

# Reuse shared helpers and constants from actu_watch.py
sys.path.insert(0, str(Path(__file__).parent))
from actu_watch import (  # noqa: E402
    ACTU_DIR,
    AI_KEYWORDS,
    CATEGORY_ENUM,
    PROMPT_FILE,
    REPO_DIR,
    RSS_FEEDS,
    STATE_FILE,
    extract_slug_from_mdx,
    fetch_rss,
    git_commit_and_push,
    has_ai_signal,
    load_decrypte_prompt,
    load_state,
    save_state,
    slugify,
    submit_indexnow,
    title_hash,
    write_article,
)

# -----------------------------------------------------------------------------
# CONFIG
# -----------------------------------------------------------------------------

SCRIPT_DIR = Path(__file__).parent
LOG_FILE = SCRIPT_DIR / "logs" / "actu_mistral.log"

MISTRAL_API_KEY = os.getenv("MISTRAL_API_KEY", "")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")

MISTRAL_URL = "https://api.mistral.ai/v1/chat/completions"
ANTHROPIC_URL = "https://api.anthropic.com/v1/messages"

MISTRAL_SMALL = "mistral-small-latest"
MISTRAL_LARGE = "mistral-large-latest"
CLAUDE_SONNET = "claude-sonnet-4-6"

API_TIMEOUT = 180
MIN_BODY_CHARS = 1500
MIN_TOTAL_SOURCES_CHARS = 5000
RELEVANCE_THRESHOLD = 6
# Score maximum autorise si aucun signal IA explicite dans titre+summary.
# Volontairement sous le threshold pour exclure les news "emploi / formation /
# reconversion" qui ne font pas le lien IA (ex: farfadets France Travail 18/04).
NO_AI_SIGNAL_CAP = 5

UA_BROWSER = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# Allow-lists (kept in sync with actu-decrypte.md prompt)
VALID_METIERS = {
    "agent-immobilier-ia", "agriculteur-ia", "analyste-financier-ia", "architecte-ia",
    "assistant-administratif-ia", "avocat-ia", "charge-clientele-ia", "chef-de-projet-ia",
    "commercial-ia", "community-manager-ia", "comptable-ia", "consultant-ia",
    "copywriter-ia", "cuisinier-ia", "data-analyst-ia", "developpeur-ia",
    "enseignant-ia", "graphiste-ia", "infirmier-ia", "journaliste-ia",
}
VALID_GUIDES = {
    "automatiser-travail-ia", "etudes-inutiles-que-faire", "financer-formation-ia-cpf",
    "freelance-ia-guide", "ia-emploi-chiffres-cles", "ia-europe-reglementation",
    "negocier-salaire-competences-ia", "prompt-engineering-debutant",
    "reconversion-ia-guide-complet", "se-former-ia-gratuitement",
}
VALID_OUTILS = {
    "claude", "chatgpt", "perplexity", "copilot", "cursor", "midjourney", "notion-ai",
    "gamma", "zapier", "make", "canva-ai", "elevenlabs", "otter-ai", "descript",
    "hubspot", "writesonic", "jasper", "copy-ai", "surfer-seo", "adobe-firefly",
}

MANDATORY_SECTIONS = [
    "## Le fait",
    "## Ce qu'on en dit vraiment",
    "## Les chiffres qui comptent",
    "## La citation qui résume tout",
    "## Pour toi concrètement",
    "## Le verdict Adapte-toi",
]

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
# API CALLS
# -----------------------------------------------------------------------------

def mistral_call(messages, model=MISTRAL_SMALL, temperature=0.3, max_tokens=4000,
                 json_mode=False, retries=3) -> tuple[str, dict]:
    if not MISTRAL_API_KEY:
        raise RuntimeError("MISTRAL_API_KEY manquant")
    payload = {"model": model, "messages": messages, "temperature": temperature,
               "max_tokens": max_tokens}
    if json_mode:
        payload["response_format"] = {"type": "json_object"}
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.post(MISTRAL_URL, json=payload, headers={
                "Authorization": f"Bearer {MISTRAL_API_KEY}",
                "Content-Type": "application/json",
            }, timeout=API_TIMEOUT)
            if r.status_code in (429, 503):
                wait = 5 * (2 ** attempt)
                log.warning(f"Mistral {r.status_code}, retry in {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            j = r.json()
            return j["choices"][0]["message"]["content"], j.get("usage", {})
        except Exception as e:
            last_err = e
            log.warning(f"Mistral call error (attempt {attempt + 1}): {e}")
            time.sleep(3)
    raise last_err


def claude_call_audit(system: str, user: str, max_tokens: int = 2500, retries=3) -> tuple[str, dict]:
    if not ANTHROPIC_API_KEY:
        raise RuntimeError("ANTHROPIC_API_KEY manquant")
    payload = {
        "model": CLAUDE_SONNET,
        "max_tokens": max_tokens,
        "system": system,
        "messages": [{"role": "user", "content": user}],
    }
    last_err = None
    for attempt in range(retries):
        try:
            r = requests.post(ANTHROPIC_URL, json=payload, headers={
                "x-api-key": ANTHROPIC_API_KEY,
                "anthropic-version": "2023-06-01",
                "content-type": "application/json",
            }, timeout=API_TIMEOUT)
            if r.status_code in (429, 529):
                wait = 10 * (2 ** attempt)
                log.warning(f"Claude {r.status_code}, retry in {wait}s")
                time.sleep(wait)
                continue
            r.raise_for_status()
            j = r.json()
            text = "".join(b.get("text", "") for b in j.get("content", []) if b.get("type") == "text")
            return text, j.get("usage", {})
        except Exception as e:
            last_err = e
            log.warning(f"Claude audit error (attempt {attempt + 1}): {e}")
            time.sleep(3)
    raise last_err


# -----------------------------------------------------------------------------
# ARTICLE BODY FETCH
# -----------------------------------------------------------------------------

def fetch_article_body(url: str, max_chars: int = 12000) -> tuple[str | None, str | None]:
    """Return (body, error). None body if fetch failed or content too thin."""
    try:
        r = requests.get(url, headers={
            "User-Agent": UA_BROWSER,
            "Accept": "text/html,application/xhtml+xml",
            "Accept-Language": "fr-FR,fr;q=0.9,en;q=0.8",
        }, timeout=25, allow_redirects=True)
        if r.status_code != 200:
            return None, f"HTTP {r.status_code}"
        final_url = str(r.url)
        if "consent.google.com" in final_url or "accounts.google.com" in final_url:
            return None, "consent-redirect"
        try:
            from bs4 import BeautifulSoup
        except ImportError:
            return None, "bs4 missing, pip install beautifulsoup4"
        soup = BeautifulSoup(r.text, "html.parser")
        for t in soup(["script", "style", "nav", "footer", "header", "aside", "form", "iframe", "noscript"]):
            t.decompose()
        main = soup.find("article") or soup.find("main") or soup.body
        if not main:
            return None, "no main content"
        text = main.get_text("\n", strip=True)
        text = re.sub(r"\n{2,}", "\n\n", text)
        text = re.sub(r" +", " ", text)
        if len(text) < MIN_BODY_CHARS:
            return None, f"too-short ({len(text)} chars)"
        return text[:max_chars], None
    except Exception as e:
        return None, str(e)


# -----------------------------------------------------------------------------
# STEP A: SCORING via Mistral-small
# -----------------------------------------------------------------------------

SCORE_SYSTEM = """Tu es redacteur en chef du media Adapte-toi (FR), specialise IA x emploi x reconversion.
Tu juges si une news merite un decryptage pour nos lecteurs.

REGLE NON NEGOCIABLE : l'angle IA doit etre EXPLICITE dans la news (mention directe de
IA/AI/ChatGPT/algorithme/automatisation ou acteur IA comme OpenAI/Anthropic/Mistral).
Une news sur l'emploi, la formation, la reconversion ou France Travail SANS lien IA
explicite n'est PAS pertinente pour ce media. Score <= 5 dans ce cas, meme si le sujet
est interessant en soi. On couvre IA x travail, pas travail en general.

PERTINENT (7-10, angle IA explicite obligatoire) :
- Etudes chiffrees IA/emploi (OCDE, Dares, INSEE, Apec, France Strategie, Stanford HAI, Anthropic Economic Index)
- Licenciements/embauches explicitement lies a l'IA (Klarna, IBM, Duolingo type)
- Politiques publiques nommant l'IA (AI Act, plans France IA, CPF IA, France Travail IA)
- Sorties de modeles majeurs (GPT, Claude, Gemini, Mistral, DeepSeek) avec impact marche
- Prises de position fortes sur IA x travail (Babinet, Villani, Altman, Hassabis...)
- Statistiques chiffrees sur automatisation / metiers menaces
- Comparaisons internationales IA x emploi (US/UK/DE vs FR)

MOYEN (4-6) : news IA tech pure sans angle emploi, annonce produit sans impact marche,
scandale formation sans lien IA, politique sociale sans lien IA.

NON PERTINENT (0-3) : crypto, gaming, politique generale, sport, people, tech non-IA.

Reponds UNIQUEMENT en JSON : {"score": X, "category": "menace|etude|annonce|politique|outil|voix|chiffre", "why": "une phrase", "ai_angle": "phrase qui cite le signal IA dans la source, ou \\"absent\\" si pas explicite"}"""


def score_item(item: dict) -> dict | None:
    # Pre-filtre deterministe : pas de signal IA dans title+summary -> cap a 5.
    # Evite de depenser un call Mistral inutile et bloque les faux positifs
    # type "farfadets France Travail" sans lien IA.
    ai_signal = has_ai_signal(item.get("title", ""), item.get("summary", ""))
    user = (f"Titre : {item['title']}\nSource : {item['outlet']}\n"
            f"Extrait : {item['summary'][:500]}\n\nScore cette news pour Adapte-toi.")
    try:
        content, _ = mistral_call(
            [{"role": "system", "content": SCORE_SYSTEM},
             {"role": "user", "content": user}],
            model=MISTRAL_SMALL, max_tokens=250, json_mode=True,
        )
        data = json.loads(content)
        score = int(data.get("score", 0))
        cat = data.get("category", "annonce")
        if cat not in CATEGORY_ENUM:
            cat = "annonce"
        ai_angle = data.get("ai_angle", "")
        # Enforce: pas de signal IA titre+summary ET Mistral ne cite pas d'angle IA -> cap.
        if not ai_signal and (not ai_angle or ai_angle.lower().strip() in ("absent", "aucun", "none", "")):
            if score > NO_AI_SIGNAL_CAP:
                log.info(f"  AI-filter: cap {score}->{NO_AI_SIGNAL_CAP} pour '{item['title'][:60]}...' (pas de signal IA)")
            score = min(score, NO_AI_SIGNAL_CAP)
        return {"score": score, "category": cat, "why": data.get("why", ""),
                "ai_angle": ai_angle, "ai_signal_detected": ai_signal}
    except Exception as e:
        log.warning(f"Score KO pour {item.get('url')}: {e}")
        return None


# -----------------------------------------------------------------------------
# STEP B: GENERATE DRAFT via Mistral-large (with real source bodies)
# -----------------------------------------------------------------------------

def generate_decrypte_draft(item: dict, relevance: dict, body: str) -> str:
    sys_prompt = load_decrypte_prompt()
    today = datetime.now(timezone.utc).strftime("%Y-%m-%d")

    source_block = (f"[SOURCE PRIMAIRE] {item['title']}\nURL: {item['url']}\n"
                    f"OUTLET: {item['outlet']}\nPUB: {item.get('pubDate','')}\n\n{body[:9000]}")

    user = f"""Écris un décryptage Adapte-toi Décrypte sur cette news.

DATE DE PUBLICATION : {today}

NEWS À DÉCRYPTER :
- Titre : {item['title']}
- Outlet : {item['outlet']}
- URL : {item['url']}
- Catégorie suggérée : {relevance['category']}
- Angle : {relevance['why']}

CONTENU VÉRIFIÉ DE LA SOURCE (seule base autorisée pour chiffres, citations, dates, noms propres précis) :

{source_block}

RÈGLES DURES :
- Aucun tiret cadratin (— U+2014 ni – U+2013). Utilise virgule, deux-points, point, ou tiret simple (-).
- Chaque chiffre, citation littérale, date, nom d'entreprise doit être ancré dans la source ci-dessus ou relever de la culture générale vérifiable. Si tu n'as pas de source, reformule en opinion ou retire.
- Signature auteur : Léa Moreau.
- Minimum 5 liens internes vers /metiers/<slug>, /guides/<slug>, /outils/<slug> parmi les slugs autorisés UNIQUEMENT.
- Longueur corps : 900-1400 mots.
- Frontmatter YAML strict, champ `sources:` avec au moins l'URL de la source primaire ci-dessus.
- Accents FR systématiques.

SORTIE : UNIQUEMENT le fichier MDX (frontmatter + corps). Pas de ```markdown wrapper. Pas de commentaire hors fichier.
"""
    content, usage = mistral_call(
        [{"role": "system", "content": sys_prompt},
         {"role": "user", "content": user}],
        model=MISTRAL_LARGE, temperature=0.4, max_tokens=6000,
    )
    log.info(f"  Mistral-large draft usage: {usage}")
    return strip_markdown_fence(content)


def strip_markdown_fence(text: str) -> str:
    text = re.sub(r"^```(?:markdown|md|yaml)?\s*\n", "", text.strip())
    text = re.sub(r"\n```\s*$", "", text)
    return text


# -----------------------------------------------------------------------------
# STEP C: GROUNDING AUDIT via Claude Sonnet
# -----------------------------------------------------------------------------

AUDIT_SYSTEM = """Tu es auditeur factuel strict. Ta seule tâche : vérifier que chaque chiffre, citation littérale, date précise, et nom propre saillant du DRAFT est présent ou clairement dérivable de la SOURCE fournie.

Retourne un JSON strict :
{
  "hallucinations": [
    {"claim": "citation exacte du draft (max 200 chars)", "type": "chiffre|citation|date|nom", "reason": "absent des sources / contredit source"}
  ],
  "ok_claims_count": N,
  "verdict": "CLEAN|MINOR|MAJOR"
}

CLEAN = 0 hallucination. MINOR = 1-3 éléments non ancrés. MAJOR = >3 ou citation entière inventée.

Ignore opinions, jugements éditoriaux, ton. Concentre-toi UNIQUEMENT sur les faits vérifiables. Les liens internes /metiers/... /guides/... /outils/... ne sont PAS des hallucinations (ils pointent vers nos pages internes)."""


def audit_grounding(draft: str, source_block: str) -> dict:
    user = f"DRAFT À AUDITER :\n{draft}\n\nSOURCE AUTORISÉE :\n{source_block}\n\nRetourne le JSON uniquement."
    content, usage = claude_call_audit(AUDIT_SYSTEM, user, max_tokens=2500)
    log.info(f"  Claude audit usage: {usage}")
    m = re.search(r"\{[\s\S]*\}", content)
    if not m:
        log.warning("Audit JSON introuvable, considéré comme UNKNOWN")
        return {"verdict": "UNKNOWN", "hallucinations": [], "ok_claims_count": 0}
    try:
        return json.loads(m.group())
    except json.JSONDecodeError as e:
        log.warning(f"Audit JSON parse KO: {e}")
        return {"verdict": "UNKNOWN", "hallucinations": [], "ok_claims_count": 0}


# -----------------------------------------------------------------------------
# STEP D: FIX HALLUCINATIONS via Mistral-large
# -----------------------------------------------------------------------------

def fix_hallucinations(draft: str, hallucinations: list, source_block: str) -> str:
    sys_prompt = load_decrypte_prompt()
    user = f"""Voici un draft. Claude a flaggé {len(hallucinations)} hallucinations factuelles.

Pour chacune : soit SUPPRIME l'affirmation, soit REFORMULE pour retirer le fait non sourcé. Ne réécris pas tout l'article, modifie UNIQUEMENT les phrases/paragraphes concernés. Conserve la structure, le style, tous les autres chiffres et citations valides.

HALLUCINATIONS À CORRIGER :
{json.dumps(hallucinations, ensure_ascii=False, indent=2)}

SOURCE AUTORISÉE (rappel) :
{source_block[:8000]}

DRAFT ACTUEL :
{draft}

Retourne le MDX corrigé complet. Pas de ```markdown. Pas de commentaire."""
    content, usage = mistral_call(
        [{"role": "system", "content": sys_prompt},
         {"role": "user", "content": user}],
        model=MISTRAL_LARGE, temperature=0.2, max_tokens=6000,
    )
    log.info(f"  Mistral-large fix usage: {usage}")
    return strip_markdown_fence(content)


# -----------------------------------------------------------------------------
# STEP E: TRIM if too long
# -----------------------------------------------------------------------------

def trim_if_too_long(draft: str, target_max: int = 1400) -> str:
    body = draft.split("---", 2)[-1] if draft.count("---") >= 2 else draft
    words = len(re.findall(r"\w+", body))
    if words <= target_max:
        return draft
    link_count = len(re.findall(r"\]\(/(?:metiers|guides|outils|actu)/", draft))
    log.info(f"  Trim needed: {words} -> {target_max} max (liens à préserver: {link_count})")
    user = f"""Le draft fait {words} mots dans le corps. Réduis à 1200-1350 mots MAX sans supprimer aucune section obligatoire ni aucun des {link_count} liens internes. Garde le frontmatter intact (zéro modif).

Resserre les phrases, coupe les répétitions, supprime les adjectifs gratuits. Interdiction d'ajouter de nouvelles affirmations factuelles.

DRAFT :
{draft}

Retourne le MDX trimé complet. Pas de ```markdown. Pas de commentaire."""
    content, usage = mistral_call(
        [{"role": "user", "content": user}],
        model=MISTRAL_LARGE, temperature=0.2, max_tokens=5500,
    )
    log.info(f"  Mistral-large trim usage: {usage}")
    return strip_markdown_fence(content)


# -----------------------------------------------------------------------------
# STEP F: DETERMINISTIC POST-PROCESS
# -----------------------------------------------------------------------------

def post_process(draft: str) -> tuple[str, dict]:
    stats = {"em_dashes": 0, "en_dashes": 0, "typo_apos": 0}
    stats["em_dashes"] = draft.count("\u2014")
    stats["en_dashes"] = draft.count("\u2013")
    stats["typo_apos"] = draft.count("\u2019")

    # Kill em/en dashes -> ", "
    draft = re.sub(r"\s*[\u2014\u2013]\s*", ", ", draft)
    draft = re.sub(r",\s*,", ",", draft)
    # Normalize typographic apostrophe to straight (repo convention)
    draft = draft.replace("\u2019", "'")
    return draft, stats


# -----------------------------------------------------------------------------
# STEP G: RULE VALIDATION (deterministic)
# -----------------------------------------------------------------------------

def _extract_frontmatter_block(draft: str) -> str:
    """Retourne le bloc entre les deux premiers '---'. Vide si absent."""
    m = re.search(r"^---\s*\n(.*?)\n---", draft, re.DOTALL)
    return m.group(1) if m else ""


def _extract_tldr_bullets(frontmatter: str) -> list[str]:
    """Parse les bullets sous 'tldr:' du YAML (sans dep yaml stricte)."""
    m = re.search(r"^tldr:\s*\n((?:\s*-\s+.*\n?)+)", frontmatter, re.MULTILINE)
    if not m:
        return []
    bullets = []
    for line in m.group(1).splitlines():
        line = line.strip()
        if line.startswith("- "):
            bullets.append(line[2:].strip().strip('"\''))
    return bullets


def _extract_description(frontmatter: str) -> str:
    m = re.search(r'^description:\s*["\'](.+?)["\']\s*$', frontmatter, re.MULTILINE)
    return m.group(1) if m else ""


def _extract_first_fact_paragraph(draft: str) -> str:
    """Premier paragraphe non vide sous '## Le fait'."""
    m = re.search(r"^## Le fait\s*\n+(.+?)(?:\n\s*\n|$)", draft, re.MULTILINE | re.DOTALL)
    return m.group(1).strip() if m else ""


def _extract_sources_urls(frontmatter: str) -> list[str]:
    """Extrait les URLs du champ sources: du frontmatter YAML (sans lib yaml)."""
    m = re.search(r"^sources:\s*\n((?:\s{2,}.*\n?)+?)(?=^\w|\Z)", frontmatter, re.MULTILINE)
    if not m:
        return []
    urls = re.findall(r'^\s*url:\s*["\']?(https?://[^\s"\']+)["\']?', m.group(1), re.MULTILINE)
    return urls


def _extract_external_links_body(body: str, own_host: str = "adapte-toi.com") -> list[str]:
    """Liens markdown [txt](https://...) dans le corps, hors liens vers notre propre domaine."""
    all_ext = re.findall(r"\]\((https?://[^)\s]+)\)", body)
    return [u for u in all_ext if own_host not in u]


def validate_rules(draft: str) -> list[str]:
    issues = []
    if "\u2014" in draft or "\u2013" in draft:
        issues.append(f"TIRETS CADRATINS: em={draft.count(chr(0x2014))} en={draft.count(chr(0x2013))}")
    if not draft.lstrip().startswith("---"):
        issues.append("Frontmatter absent au début")
    for sec in MANDATORY_SECTIONS:
        if sec not in draft:
            issues.append(f"Section manquante: {sec}")
    links = re.findall(r"\]\((/(?:metiers|guides|outils|actu)/[^)]+)\)", draft)
    if len(links) < 5:
        issues.append(f"Liens internes < 5 ({len(links)})")
    bad_slugs = []
    for link in links:
        parts = link.split("/")
        if len(parts) >= 3:
            kind, slug = parts[1], parts[2].split("#")[0]
            if kind == "metiers" and slug not in VALID_METIERS:
                bad_slugs.append(f"metiers/{slug}")
            elif kind == "guides" and slug not in VALID_GUIDES:
                bad_slugs.append(f"guides/{slug}")
            elif kind == "outils" and slug not in VALID_OUTILS:
                bad_slugs.append(f"outils/{slug}")
    if bad_slugs:
        issues.append(f"Slugs invalides: {bad_slugs}")
    body = draft.split("---", 2)[-1] if draft.count("---") >= 2 else draft
    words = len(re.findall(r"\w+", body))
    if words < 900 or words > 1500:
        issues.append(f"Longueur hors fourchette ({words} mots, attendu 900-1500)")
    if "Léa Moreau" not in draft:
        issues.append("Signature 'Léa Moreau' absente")
    if "sources:" not in draft:
        issues.append("Frontmatter sans champ `sources:`")

    # Angle IA obligatoire : description + au moins 1 bullet tldr + 1er paragraphe du fait.
    fm = _extract_frontmatter_block(draft)
    desc = _extract_description(fm)
    bullets = _extract_tldr_bullets(fm)
    first_fact = _extract_first_fact_paragraph(body)
    if not has_ai_signal(desc):
        issues.append("AI-angle: description sans mention IA explicite")
    if bullets and not any(has_ai_signal(b) for b in bullets):
        issues.append(f"AI-angle: aucun bullet tldr ne mentionne IA ({len(bullets)} bullets)")
    elif not bullets:
        issues.append("AI-angle: tldr introuvable ou vide")
    if first_fact and not has_ai_signal(first_fact[:400]):
        issues.append("AI-angle: premier paragraphe '## Le fait' sans mention IA dans les 400 premiers chars")

    # Maillage : sources frontmatter + liens externes inline = autorite + transparence.
    source_urls = _extract_sources_urls(fm)
    if len(source_urls) < 2:
        issues.append(f"Sources frontmatter < 2 ({len(source_urls)}) : min 2 URLs distinctes requises")
    source_domains = {re.sub(r"^https?://(www\.)?", "", u).split("/")[0] for u in source_urls}
    if len(source_urls) >= 2 and len(source_domains) < 2:
        issues.append(f"Sources frontmatter sur un seul domaine ({source_domains}), diversifier les outlets")
    ext_links = _extract_external_links_body(body)
    if len(ext_links) < 2:
        issues.append(f"Liens externes inline dans le corps < 2 ({len(ext_links)}) : lier les chiffres/citations a leur source")
    return issues


# -----------------------------------------------------------------------------
# MAIN
# -----------------------------------------------------------------------------

def build_pipeline(item: dict, relevance: dict, strict: bool = False) -> tuple[str | None, dict]:
    """Run full pipeline on one item. Return (final_mdx or None, stats)."""
    stats = {"item": item["title"], "url": item["url"]}

    log.info(f"Fetching body: {item['url']}")
    body, err = fetch_article_body(item["url"])
    if not body:
        stats["abort"] = f"fetch_body: {err}"
        log.warning(f"  SKIP: {err}")
        return None, stats
    stats["body_chars"] = len(body)
    if len(body) < MIN_TOTAL_SOURCES_CHARS:
        log.info(f"  Body short ({len(body)} chars), on tente quand meme car source primaire")

    source_block = (f"[SOURCE PRIMAIRE] {item['title']}\nURL: {item['url']}\n"
                    f"OUTLET: {item['outlet']}\nPUB: {item.get('pubDate','')}\n\n{body[:9000]}")

    log.info("Draft via Mistral-large")
    draft = generate_decrypte_draft(item, relevance, body)

    log.info("Audit grounding via Claude Sonnet")
    audit1 = audit_grounding(draft, source_block)
    stats["audit1_verdict"] = audit1.get("verdict")
    stats["audit1_hallucinations"] = len(audit1.get("hallucinations", []))
    log.info(f"  Audit 1: {audit1.get('verdict')} ({stats['audit1_hallucinations']} hallucinations)")

    if audit1.get("hallucinations"):
        log.info("Fix via Mistral-large")
        draft = fix_hallucinations(draft, audit1["hallucinations"], source_block)

        log.info("Re-audit via Claude Sonnet")
        audit2 = audit_grounding(draft, source_block)
        stats["audit2_verdict"] = audit2.get("verdict")
        stats["audit2_hallucinations"] = len(audit2.get("hallucinations", []))
        log.info(f"  Audit 2: {audit2.get('verdict')} ({stats['audit2_hallucinations']} hallucinations)")

        if strict and audit2.get("verdict") == "MAJOR":
            stats["abort"] = "strict: MAJOR after fix"
            log.warning(f"  ABORT (strict): {stats['abort']}")
            return None, stats

    log.info("Trim si trop long")
    draft = trim_if_too_long(draft)

    log.info("Post-process déterministe (tirets, apos)")
    draft, pp_stats = post_process(draft)
    stats.update({"killed_dashes_em": pp_stats["em_dashes"],
                  "killed_dashes_en": pp_stats["en_dashes"],
                  "normalized_apos": pp_stats["typo_apos"]})

    log.info("Validation règles")
    issues = validate_rules(draft)
    stats["rule_issues"] = issues
    # AI-angle issues = hard fail meme hors strict mode (positionnement du media).
    ai_issues = [i for i in issues if i.startswith("AI-angle:")]
    if ai_issues:
        log.warning(f"  AI-angle hard fail: {ai_issues} -> abort")
        stats["abort"] = f"ai-angle: {ai_issues}"
        return None, stats
    if issues:
        log.warning(f"  {len(issues)} issues: {issues}")
        if strict:
            stats["abort"] = f"strict: rules {issues}"
            return None, stats

    return draft, stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--seed-only", action="store_true", help="Fetch + score, pas de génération")
    ap.add_argument("--max", type=int, default=1, help="Nombre max d'articles à générer")
    ap.add_argument("--strict", action="store_true", help="Abort si MAJOR après fix ou si issues règles")
    args = ap.parse_args()

    state = load_state()
    seen_urls = set(state.get("seen_urls", []))
    seen_hashes = set(state.get("seen_hashes", []))
    published_slugs = set(state.get("published_slugs", []))

    # 1. Fetch RSS
    all_items = []
    for outlet, url in RSS_FEEDS:
        items = fetch_rss(outlet, url)
        log.info(f"RSS {outlet}: {len(items)} items")
        all_items.extend(items)

    # 2. Dedup
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

    # 3a. Pre-filtre deterministe AI : on ne score QUE les items avec signal IA.
    # Avec 60+ feeds, on a 3000+ items frais dont 90% hors-sujet. Scorer tout
    # via Mistral est cher et dilue le signal (les 40 premiers sont souvent
    # generalistes). Le pre-filtre garantit qu'on donne a Mistral uniquement
    # des candidats IA-relevant.
    ai_relevant = [it for it in fresh if has_ai_signal(it.get("title",""), it.get("summary",""))]
    log.info(f"AI-relevant (pre-filter): {len(ai_relevant)} / {len(fresh)}")

    # 3b. Cap a 80 candidats (score Mistral-small coute ~0.0001$, on peut monter).
    # Les feeds institutionnels / acteurs IA passent tous, on garde de la marge.
    candidates = ai_relevant[:80]

    # 3c. Mistral scoring
    scored = []
    for it in candidates:
        r = score_item(it)
        if r and r["score"] >= RELEVANCE_THRESHOLD:
            scored.append({**it, **r})
    scored.sort(key=lambda x: x["score"], reverse=True)
    log.info(f"Scored >= {RELEVANCE_THRESHOLD}: {len(scored)} / {len(candidates)} candidates")

    if args.seed_only:
        for s in scored[:10]:
            log.info(f"[{s['score']}/{s['category']}] {s['title']} ({s['outlet']})")
        save_state({
            "seen_urls": list(seen_urls)[-5000:],
            "seen_hashes": list(seen_hashes)[-5000:],
            "published_slugs": list(published_slugs)[-2000:],
        })
        return 0

    # 4. Pipeline per-item (try until args.max articles pass or we exhaust candidates)
    written_paths = []
    written_titles = []
    attempts = 0
    for s in scored:
        if len(written_paths) >= args.max:
            break
        attempts += 1
        if attempts > args.max * 3:  # don't loop forever on bad fetches
            log.info(f"Stopping after {attempts} attempts")
            break
        log.info(f"\n=== Item [{s['score']}] {s['title']} ({s['outlet']}) ===")
        try:
            mdx, stats = build_pipeline(s, s, strict=args.strict)
            log.info(f"  Stats: {json.dumps({k:v for k,v in stats.items() if k not in ('item','url')}, ensure_ascii=False)}")
            if not mdx:
                log.warning(f"  SKIP: {stats.get('abort','no draft')}")
                continue

            slug = extract_slug_from_mdx(mdx)
            if slug in published_slugs:
                log.info(f"  Slug déjà publié: {slug}, skip")
                continue
            if args.dry_run:
                log.info(f"  [DRY] OK, {len(mdx)} chars\n---\n{mdx[:600]}\n---")
                continue
            path = write_article(mdx, slug)
            log.info(f"  Écrit: {path.name}")
            written_paths.append(path)
            written_titles.append(s["title"])
            published_slugs.add(slug)
        except Exception as e:
            log.error(f"Pipeline KO pour {s['title']}: {e}", exc_info=True)

    # 5. Save state + git commit
    save_state({
        "seen_urls": list(seen_urls)[-5000:],
        "seen_hashes": list(seen_hashes)[-5000:],
        "published_slugs": list(published_slugs)[-2000:],
    })

    if written_paths and not args.dry_run:
        if git_commit_and_push(written_paths, written_titles):
            log.info(f"Push OK: {len(written_paths)} décryptage(s)")
            site_url = os.getenv("SITE_URL", "https://adapte-toi.com").rstrip("/")
            urls = [f"{site_url}/actu/{p.stem}/" for p in written_paths]
            submit_indexnow(urls)
        else:
            log.warning("Push KO, articles écrits mais pas committés")

    return 0


if __name__ == "__main__":
    sys.exit(main())
