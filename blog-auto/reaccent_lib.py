#!/usr/bin/env python3
"""
reaccent_lib.py , safe string->string French re-accentuation for blog-auto.

Vendored next to each blog-auto pipeline. Call reaccent_text(md, key) on the
final markdown right BEFORE committing so the published .md is already accented
(accents are mandatory parc-wide). stdlib only (urllib), no deps.

SAFE BY DEFAULT: returns the input UNCHANGED on any problem (no key, API error,
or a safety-guard failure). It can only ever ADD diacritics, proven mechanically
(reconcile keeps only accents-only token changes; guarded re-validates), and it
NEVER raises , so wiring it into a cron pipeline can never break publishing.

Mirror of scripts/reaccent_gemini.py's core (keep in sync if that changes).
"""
from __future__ import annotations
import os, re, json, unicodedata, urllib.request, difflib

# Model fallback chain: flash first (highest free quota), then pro, then
# flash-lite. gemini-2.5-pro alone was 429-starved on the shared parc key and
# every re-accent layer silently no-op'd on 429 -> folded FR shipped -> deploy
# blocked on ACCENT_LOW (recurring). A GEMINI_MODEL override is tried first.
_MODELS = [m for m in (os.getenv("GEMINI_MODEL"), "gemini-2.5-flash",
                       "gemini-2.5-pro", "gemini-2.5-flash-lite") if m]


def _ep(model: str) -> str:
    return f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent"
_URL_RE = re.compile(r"https?://[^\s\)\"'>]+")
_TOKEN = re.compile(r"\w+|\W+", re.UNICODE)
_PROT_KEYS = ("slug", "url", "author", "vertical", "category", "clusterAnchor",
              "articleType", "articleTier", "lang", "qid", "pubDate", "date",
              "updatedDate", "image", "ogImageAuto", "draft", "intent")
_ACCENTS = "éèàêôîûçùâëïüœÉÈÀÊÔÎÛÇÙÂËÏÜ"
_SYS = ("Tu es correcteur orthographique français. On te donne un fichier Markdown "
        "dont le texte français a perdu ses accents. Ta SEULE tâche : rétablir les "
        "accents et cédilles corrects du français (é è à ê ô î û ç ù â ë ï œ...). "
        "RÈGLES STRICTES : ne change AUCUN mot, AUCUNE ponctuation, AUCUNE structure, "
        "AUCUNE URL, AUCUN slug, AUCUNE clé YAML, AUCUN code, AUCUNE balise. "
        "N'ajoute/ne retire rien d'autre que des diacritiques. N'ajoute jamais de tiret "
        "cadratin. Renvoie le fichier complet, identique au caractère près sauf les accents.")


def _fold(s: str) -> str:
    return unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")


def _is_folded_french(md: str) -> bool:
    """Cheap pre-check: only call the API when the body really looks like
    ASCII-folded French (low accent density). Avoids a pointless API round-trip
    on already-accented or non-French content."""
    body = re.sub(r"^---\n.*?\n---\n", "", md, flags=re.S)
    body = re.sub(r"```.*?```", " ", body, flags=re.S)
    prose = re.sub(r"https?://\S+", " ", body)
    if len(prose) < 400:
        return False
    density = sum(1 for c in prose if c in _ACCENTS) * 1000 / max(len(prose), 1)
    if density >= 8:
        return False
    low = prose.lower()
    folded_markers = ("securite", "methode", "donnees", "strategie", "numerique",
                      "societe", "etape", "deja", "tres", "apres", "egalement",
                      "reference", "francais", "generale", "qualite", "activite")
    hits = sum(1 for w in folded_markers if re.search(rf"\b{w}\b", low))
    return hits >= 4


def _call_gemini(text: str, key: str) -> str:
    payload = {
        "systemInstruction": {"parts": [{"text": _SYS}]},
        "contents": [{"role": "user", "parts": [{"text": text}]}],
        "generationConfig": {"temperature": 0, "maxOutputTokens": 65536},
    }
    last_err: Exception | None = None
    for model in dict.fromkeys(_MODELS):          # de-dup, preserve order
        try:
            req = urllib.request.Request(
                _ep(model) + "?key=" + key, data=json.dumps(payload).encode(),
                headers={"Content-Type": "application/json"})
            with urllib.request.urlopen(req, timeout=180) as r:
                body = json.loads(r.read())
            cand = (body.get("candidates") or [{}])[0]
            out = "".join(p.get("text", "") for p in cand.get("content", {}).get("parts", []))
            if out.startswith("```"):
                out = re.sub(r"^```[a-z]*\n", "", out)
                out = re.sub(r"\n```\s*$", "", out)
            if out.strip():
                return out
        except Exception as e:                    # 429/5xx/timeout -> next model
            last_err = e
            continue
    if last_err:
        raise last_err
    return ""


def _reconcile(orig: str, model: str) -> str:
    a, b = _TOKEN.findall(orig), _TOKEN.findall(model)
    out: list[str] = []
    sm = difflib.SequenceMatcher(None, [_fold(t) for t in a], [_fold(t) for t in b], autojunk=False)
    for op, i1, i2, j1, j2 in sm.get_opcodes():
        if op == "equal":
            out.extend(b[j1:j2])
        elif op == "replace":
            out.extend(b[j1:j2] if _fold("".join(a[i1:i2])) == _fold("".join(b[j1:j2])) else a[i1:i2])
        elif op == "delete":
            out.extend(a[i1:i2])
    result = "".join(out)
    ol, rl = orig.split("\n"), result.split("\n")
    if len(ol) == len(rl):
        for i, a_line in enumerate(ol):
            k = a_line.split(":", 1)[0].strip().lstrip("- ")
            if k in _PROT_KEYS:
                rl[i] = a_line
        result = "\n".join(rl)
    return result


def _guarded(orig: str, new: str) -> bool:
    if not new.strip() or _fold(orig) != _fold(new):
        return False
    if sorted(_URL_RE.findall(orig)) != sorted(_URL_RE.findall(new)):
        return False
    for a, b in zip(orig.split("\n"), new.split("\n")):
        k = a.split(":", 1)[0].strip().lstrip("- ")
        if k in _PROT_KEYS and a != b:
            return False
    if ("—" in new or "–" in new) and ("—" not in orig and "–" not in orig):
        return False
    return True


def reaccent_text(md: str, key: str | None = None) -> str:
    """Return `md` with French accents restored. SAFE: returns `md` unchanged on
    a missing key, an API error, content that isn't folded French, or any guard
    failure. Never raises."""
    # GOOGLE_API_KEY is the same Google AI Studio key and is already present in
    # the blog-auto cron envs that only declared GOOGLE_API_KEY (decryptebot,
    # bebedecrypte, pulsari), so reaccent activates with no secret/workflow change.
    key = key or os.getenv("GEMINI_API_KEY") or os.getenv("GOOGLE_API_KEY")
    if not key:
        return md
    try:
        if not _is_folded_french(md):
            return md
        new = _reconcile(md, _call_gemini(md, key))
        return new if (new != md and _guarded(md, new)) else md
    except Exception:
        return md
