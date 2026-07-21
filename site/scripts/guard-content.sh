#!/usr/bin/env sh
# STACK-2026 content guard — local blocking prebuild gate.
# Checks the .md/.mdx touched by the last commit; full-scans CONTENT_DIR as a
# fallback (e.g. shallow/initial checkout). Skips cleanly if python3 is absent
# so a missing interpreter never blocks a deploy.
set -e

GUARD="$(CDPATH= cd "$(dirname "$0")" && pwd)/content_guard.py"
REPO_ROOT="$(CDPATH= cd "$(dirname "$0")/../.." && pwd)"
CONTENT_DIR="${CONTENT_DIR:-src/content}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[guard:content] python3 not found — skipping content guard."
  exit 0
fi

if [ ! -f "$GUARD" ]; then
  echo "[guard:content] content_guard.py not found at $GUARD — skipping."
  exit 0
fi

# Re-accent ASCII-folded FR files before the blocking --check when a correction
# API key is available. content_guard.py flags ACCENT_LOW but cannot fix it; the
# repository-local wrapper restores diacritics so a freshly-published
# unaccented FR article self-heals at build instead of blocking the deploy.
reaccent_low() {
  if [ -n "${GEMINI_API_KEY:-}" ] || [ -n "${MISTRAL_API_KEY:-}" ]; then
    RX="$REPO_ROOT/blog-auto/reaccent_file.py"
    if [ -f "$RX" ]; then
      BAD=$(python3 "$GUARD" --check "$@" 2>&1 | awk '/^\[FAIL\] /{f=$2} /ACCENT_LOW/{if(f)print f}' | sort -u || true)
      if [ -n "$BAD" ]; then
        echo "[guard:content] re-accenting ASCII-folded FR: $BAD"
        for f in $BAD; do
          if [ -f "$f" ]; then python3 "$RX" "$f" || true; fi
        done
      fi
    fi
  fi
  return 0
}

# Files changed in the last commit (diff HEAD~1 HEAD), restricted to md/mdx.
FILES=""
if command -v git >/dev/null 2>&1 && git rev-parse --verify HEAD~1 >/dev/null 2>&1; then
  FILES="$(git diff --name-only --diff-filter=ACMR HEAD~1 HEAD -- '*.md' '*.mdx' 2>/dev/null || true)"
fi

if [ -n "$FILES" ]; then
  # Keep only files that still exist (renames/moves) and are readable.
  EXISTING=""
  for f in $FILES; do
    [ -f "$f" ] && EXISTING="$EXISTING $f"
  done
  if [ -n "$EXISTING" ]; then
    echo "[guard:content] auto-fix then check last-commit content files."
    # --fix first: auto-clamp long descriptions / strip artifacts / demote H1 so a
    # cosmetic defect (e.g. desc >180c) self-heals at build instead of blocking the
    # deploy (recurring adapte-toi breakage 11-12/06). --check then still blocks on
    # non-auto-fixable defects (ACCENT_LOW, mojibake).
    # shellcheck disable=SC2086
    python3 "$GUARD" --fix $EXISTING || true
    # shellcheck disable=SC2086
    reaccent_low $EXISTING
    # shellcheck disable=SC2086
    exec python3 "$GUARD" --check --strict-images $EXISTING
  fi
fi

echo "[guard:content] auto-fix then full-scan fallback on $CONTENT_DIR."
python3 "$GUARD" --fix "$CONTENT_DIR" || true
reaccent_low "$CONTENT_DIR"
exec python3 "$GUARD" --check "$CONTENT_DIR"
