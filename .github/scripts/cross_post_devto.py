"""
Cross-post new blog articles to dev.to. Runs in GH Actions after blog-auto success.

Config via env vars:
  DEVTO_API_KEY     - required, dev.to API key
  PROJECT_SITE_URL  - required, e.g. https://getpulsari.com
  PROJECT_CONTENT_DIR - required, e.g. site/src/content/blog (relative to repo root)
  DEVTO_TAGS        - comma-separated, e.g. ai,seo,startup,webdev
  DEVTO_DEFAULT_IMAGE - optional image URL for articles without an image: frontmatter field
  DEVTO_HOOK        - optional markdown hook prepended to body. Use {site_url} placeholder.

Tracks posted articles in .github/scripts/.devto-log.json (committed back).
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

API_KEY = os.environ["DEVTO_API_KEY"]
SITE_URL = os.environ["PROJECT_SITE_URL"]
CONTENT_DIR = Path(os.environ["PROJECT_CONTENT_DIR"])
TAGS = [t.strip() for t in os.environ.get("DEVTO_TAGS", "").split(",") if t.strip()]
DEFAULT_IMAGE = os.environ.get("DEVTO_DEFAULT_IMAGE", "").strip() or None
HOOK = os.environ.get("DEVTO_HOOK", "").format(site_url=SITE_URL) if os.environ.get("DEVTO_HOOK") else ""

LOG_PATH = Path(__file__).parent / ".devto-log.json"


def load_log():
    if LOG_PATH.exists():
        return json.loads(LOG_PATH.read_text())
    return {}


def save_log(log):
    LOG_PATH.write_text(json.dumps(log, indent=2))


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.DOTALL)
    if not m:
        raise ValueError("No frontmatter")
    raw, body = m.group(1), m.group(2)
    fm = {}
    for line in raw.split("\n"):
        if ":" not in line or line.startswith(" "):
            continue
        k, _, v = line.partition(":")
        v = v.strip()
        if v.startswith('"') and v.endswith('"'):
            v = v[1:-1]
        elif v.startswith("[") and v.endswith("]"):
            v = [t.strip().strip('"').strip("'") for t in v[1:-1].split(",") if t.strip()]
        fm[k.strip()] = v
    return fm, body


def normalize_tags(tags, max_n=4):
    out = []
    for t in tags or []:
        if not t:
            continue
        t = re.sub(r"[^a-z0-9]", "", t.lower())
        if t and t not in out:
            out.append(t)
    return out[:max_n]


def clean_body(body):
    """Strip IMAGE_N placeholders, rewrite relative links, strip em/en dashes (STACK-2026 hard ban)."""
    body = re.sub(r"!\[[^\]]*\]\(IMAGE_\d+\)\s*\n?", "", body)
    def rewrite(m):
        text, url = m.group(1), m.group(2)
        if url.startswith("/") and not url.startswith("//"):
            return f"[{text}]({SITE_URL}{url})"
        return m.group(0)
    body = re.sub(r"\[([^\]]+)\]\((/[^\)]+)\)", rewrite, body)
    body = body.replace("\u2014", ",").replace("\u2013", ",")
    body = re.sub(r"\n{3,}", "\n\n", body)
    return body.strip()


def post(path, log):
    slug = path.stem
    if slug in log:
        print(f"  skip: {slug}")
        return False
    fm, body = parse_frontmatter(path.read_text())
    if fm.get("draft") == "true":
        print(f"  skip (draft): {slug}")
        return False
    body = clean_body(body)
    canonical = f"{SITE_URL}/blog/{slug}/"
    tags = normalize_tags(TAGS or fm.get("tags"))
    main_image = fm.get("image") or DEFAULT_IMAGE
    description = fm.get("description", "")[:250]
    footer = f"\n\n---\n\n*Originally published on [{SITE_URL.replace('https://', '')}]({canonical}).*\n"

    article = {
        "title": fm["title"],
        "body_markdown": HOOK + body + footer,
        "published": True,
        "canonical_url": canonical,
        "tags": tags,
        "description": description,
    }
    if main_image:
        article["main_image"] = main_image

    req = urllib.request.Request(
        "https://dev.to/api/articles",
        data=json.dumps({"article": article}).encode(),
        headers={
            "api-key": API_KEY,
            "Content-Type": "application/json",
            "User-Agent": "stack2026-crosspost/1",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            result = json.loads(r.read().decode())
    except urllib.error.HTTPError as e:
        print(f"  FAIL {slug}: HTTP {e.code} {e.read().decode()[:300]}")
        return False
    log[slug] = {"id": result.get("id"), "url": result.get("url"), "at": result.get("published_at")}
    save_log(log)
    print(f"  posted {slug}: {result.get('url')}")
    return True


def main():
    if not CONTENT_DIR.is_dir():
        sys.exit(f"Content dir not found: {CONTENT_DIR}")
    log = load_log()
    posted = 0
    # Sort newest first; only process articles with date <= today
    today = date.today().isoformat()
    for md in sorted(CONTENT_DIR.glob("*.md"), reverse=True):
        try:
            fm, _ = parse_frontmatter(md.read_text())
        except Exception:
            continue
        d = str(fm.get("date", ""))[:10]
        if d and d > today:
            continue
        if md.stem in log:
            continue
        if post(md, log):
            posted += 1
    print(f"done. posted {posted} article(s)")


if __name__ == "__main__":
    main()
