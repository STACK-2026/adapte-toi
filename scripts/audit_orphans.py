#!/usr/bin/env python3
"""Audit orphan pages : pages with zero internal incoming links.

Usage : python3 scripts/audit_orphans.py
Lit le contenu de site/dist/ apres `cd site && npm run build`.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "site" / "dist"

# Pages de "maillage de service" qu'on ne veut PAS flagger orphelines
# (sitemap, RSS, robots, /og/, hubs eux-memes)
EXCLUDE_PATHS = {
    "/",
    "/404/",
    "/admin/",
    "/sitemap-index.xml",
    "/sitemap-0.xml",
    "/sitemap-news.xml",
    "/rss.xml",
    "/robots.txt",
}
EXCLUDE_PREFIXES = ("/og/", "/admin/")


def extract_internal_links(html: str) -> set[str]:
    """Return set of internal hrefs (starting with /) found in <a href>."""
    raw = re.findall(r'href="([^"#]*?)"', html)
    out: set[str] = set()
    for href in raw:
        if not href.startswith("/"):
            continue
        # normalize: strip trailing slash sauf root
        h = href.split("?")[0]
        if h != "/" and h.endswith("/"):
            h = h
        out.add(h)
    return out


def page_url_for(file: Path) -> str:
    """Map dist/foo/bar/index.html -> /foo/bar/."""
    rel = file.relative_to(DIST).as_posix()
    if rel == "index.html":
        return "/"
    if rel.endswith("/index.html"):
        return "/" + rel[: -len("index.html")]
    # cas /404.html, /rss.xml, /sitemap-*.xml
    return "/" + rel


def main() -> int:
    if not DIST.exists():
        print(f"[ERR] {DIST} introuvable. Run `cd site && npm run build` d'abord.", file=sys.stderr)
        return 1

    all_pages: set[str] = set()
    incoming: defaultdict[str, set[str]] = defaultdict(set)

    for file in DIST.rglob("*.html"):
        url = page_url_for(file)
        all_pages.add(url)

    for file in DIST.rglob("*.html"):
        src_url = page_url_for(file)
        try:
            html = file.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for href in extract_internal_links(html):
            # match exact OR avec trailing slash
            if href in all_pages and href != src_url:
                incoming[href].add(src_url)
            elif href + "/" in all_pages and href + "/" != src_url:
                incoming[href + "/"].add(src_url)

    orphans: list[str] = []
    for url in sorted(all_pages):
        if url in EXCLUDE_PATHS:
            continue
        if any(url.startswith(p) for p in EXCLUDE_PREFIXES):
            continue
        if not incoming.get(url):
            orphans.append(url)

    print(f"=== ORPHAN AUDIT adapte-toi ===")
    print(f"Total pages : {len(all_pages)}")
    print(f"Orphelines (0 lien entrant) : {len(orphans)}")
    print()
    for url in orphans:
        print(f"  {url}")

    # bonus : pages tres faiblement maillees (1-2 incoming)
    weakly = sorted(
        [(u, len(incoming[u])) for u in all_pages if u not in EXCLUDE_PATHS
         and not any(u.startswith(p) for p in EXCLUDE_PREFIXES)
         and 1 <= len(incoming[u]) <= 2],
        key=lambda x: (x[1], x[0]),
    )
    print()
    print(f"=== Pages faiblement maillees (1-2 liens entrants) : {len(weakly)} ===")
    for url, count in weakly[:30]:
        print(f"  [{count}] {url}")
    if len(weakly) > 30:
        print(f"  ... +{len(weakly) - 30} autres")

    return 0


if __name__ == "__main__":
    sys.exit(main())
