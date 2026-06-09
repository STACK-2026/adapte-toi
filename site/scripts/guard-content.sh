#!/usr/bin/env sh
# STACK-2026 content guard — local blocking prebuild gate.
# Checks the .md/.mdx touched by the last commit; full-scans CONTENT_DIR as a
# fallback (e.g. shallow/initial checkout). Skips cleanly if python3 is absent
# so a missing interpreter never blocks a deploy.
set -e

GUARD="$(CDPATH= cd "$(dirname "$0")" && pwd)/content_guard.py"
CONTENT_DIR="${CONTENT_DIR:-src/content}"

if ! command -v python3 >/dev/null 2>&1; then
  echo "[guard:content] python3 not found — skipping content guard."
  exit 0
fi

if [ ! -f "$GUARD" ]; then
  echo "[guard:content] content_guard.py not found at $GUARD — skipping."
  exit 0
fi

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
    echo "[guard:content] checking last-commit content files."
    # shellcheck disable=SC2086
    exec python3 "$GUARD" --check $EXISTING
  fi
fi

echo "[guard:content] full-scan fallback on $CONTENT_DIR."
exec python3 "$GUARD" --check "$CONTENT_DIR"
