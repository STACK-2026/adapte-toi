#!/usr/bin/env python3
"""Deterministic checks for built search metadata and canonical consistency."""
from __future__ import annotations

from html import unescape
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"
MAX_TITLE = 70


def main() -> int:
    failures: list[str] = []
    titles: dict[str, list[str]] = {}
    pages = 0

    for html_file in DIST.rglob("index.html"):
        rel = "/" + html_file.parent.relative_to(DIST).as_posix().strip("./")
        html = html_file.read_text(encoding="utf-8", errors="ignore")
        if 'name="robots" content="noindex' in html:
            continue
        match = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
        if not match:
            failures.append(f"{rel}: missing title")
            continue
        title = unescape(re.sub(r"\s+", " ", match.group(1))).strip()
        pages += 1
        if len(title) > MAX_TITLE:
            failures.append(f"{rel}: title {len(title)}c > {MAX_TITLE}: {title}")
        titles.setdefault(title, []).append(rel)

    for title, urls in titles.items():
        if len(urls) > 1:
            failures.append(f"duplicate title: {title} -> {', '.join(urls[:4])}")

    news = DIST / "sitemap-news.xml"
    if news.exists():
        for loc in re.findall(r"<loc>(.*?)</loc>", news.read_text(encoding="utf-8")):
            if not loc.endswith("/"):
                failures.append(f"News sitemap non-canonical URL: {loc}")

    if failures:
        print("BUILT SEO CHECK FAILED")
        for failure in failures[:100]:
            print(f"- {failure}")
        if len(failures) > 100:
            print(f"- ... {len(failures) - 100} more")
        return 1

    print(f"BUILT SEO CHECK OK: {pages} indexable HTML pages, unique titles <= {MAX_TITLE}c")
    return 0


if __name__ == "__main__":
    sys.exit(main())
