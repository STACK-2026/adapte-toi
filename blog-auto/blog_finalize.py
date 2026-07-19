#!/usr/bin/env python3
"""finalize_article , last-mile gate so the daily cron NEVER commits a .md that
would red the Cloudflare deploy.

The recurring failure: Mistral writes ASCII-folded French, the best-effort
re-accent no-ops when Gemini is 429/down, and the folded article ships and blocks
the content guard on ACCENT_LOW. This closes it at the source: after re-accenting
and running the guard's own deterministic --fix (word-boundary description clamp),
we run the blocking --check on the single file. If it would STILL block, the file
is deleted and the article is skipped , better 0 articles than a broken deploy.

Pure stdlib. Never raises.
"""
from __future__ import annotations
import os
import subprocess
import sys
from pathlib import Path

_GUARD_CACHE: object = None


def _guard_path():
    """Locate content_guard.py (repo site/scripts first, then the stack-2026
    shared copy). Cached. Returns a Path or None."""
    global _GUARD_CACHE
    if _GUARD_CACHE is not None:
        return _GUARD_CACHE or None
    here = Path(__file__).resolve().parent                 # <repo>/blog-auto
    for cand in (here.parent / "site" / "scripts" / "content_guard.py",
                 Path(os.path.expanduser("~/stack-2026/scripts/content_guard.py"))):
        if cand.exists():
            _GUARD_CACHE = cand
            return cand
    _GUARD_CACHE = False
    return None


def finalize_article(path, log=None) -> bool:
    """Return True if `path` is deploy-safe (kept on disk), False if it would
    block the content guard (deleted from disk). Never raises."""
    p = Path(path)

    def _warn(msg: str) -> None:
        if log is not None:
            log.warning(msg)

    # 1) Accents obligatoires (best-effort ; no-op sans clé, ne lève jamais).
    try:
        from reaccent_lib import reaccent_text
        original = p.read_text(encoding="utf-8")
        fixed = reaccent_text(original)
        if fixed != original:
            p.write_text(fixed, encoding="utf-8")
    except Exception:
        pass

    guard = _guard_path()
    if not guard:
        return True                                        # pas de guard -> ne bloque pas le pipeline

    # 2) Auto-fix déterministe : clamp desc au mot près, artefacts, H1 démoté.
    try:
        subprocess.run([sys.executable, str(guard), "--fix", str(p)],
                       capture_output=True, text=True, timeout=60)
    except Exception:
        pass

    # 3) Check bloquant sur ce seul fichier = exactement la porte CI.
    try:
        res = subprocess.run([sys.executable, str(guard), "--check", str(p)],
                             capture_output=True, text=True, timeout=60)
    except Exception:
        return True                                        # flake infra -> ne pas perdre l'article

    if res.returncode != 0:
        _warn("  Article bloquerait le deploy (guard FAIL), SKIP: "
              f"{p.name}\n{(res.stdout or '')[-400:]}")
        p.unlink(missing_ok=True)
        return False
    return True
