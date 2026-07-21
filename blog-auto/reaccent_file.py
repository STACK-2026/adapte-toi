#!/usr/bin/env python3
"""Re-accent Markdown files with the repository-local, guarded implementation."""

from __future__ import annotations

import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from reaccent_lib import reaccent_text

# Long Markdown inputs make both correction APIs copy the text without applying
# diacritics. At ~1k characters they reliably perform the constrained task.
MAX_CHUNK_CHARS = 1_000


def _chunks(text: str):
    """Yield newline-preserving chunks small enough for reliable model output."""
    chunk = ""
    for line in text.splitlines(keepends=True):
        if chunk and len(chunk) + len(line) > MAX_CHUNK_CHARS:
            yield chunk
            chunk = ""
        chunk += line
    if chunk:
        yield chunk


def reaccent_file(path: Path) -> bool:
    """Restore French diacritics and return whether the file changed."""
    original = path.read_text(encoding="utf-8")
    # This CLI is only called for files already flagged ACCENT_LOW by the
    # authoritative content guard. Do not apply a second, divergent heuristic.
    corrected = "".join(reaccent_text(chunk, force=True) for chunk in _chunks(original))
    if corrected == original:
        print(f"• {path}: no change")
        return False
    path.write_text(corrected, encoding="utf-8")
    print(f"✅ {path}: accents restored")
    return True


def main(argv: list[str]) -> int:
    if not argv:
        print("usage: reaccent_file.py <file.md> [<file.md> ...]", file=sys.stderr)
        return 2
    failed = False
    for raw_path in argv:
        try:
            reaccent_file(Path(raw_path))
        except Exception as error:
            print(f"❌ {raw_path}: {error}", file=sys.stderr)
            failed = True
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
