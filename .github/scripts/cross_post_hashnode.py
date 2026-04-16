"""
Cross-post new blog articles to Hashnode via GraphQL. Runs in GH Actions.

Env vars:
  HASHNODE_TOKEN         - required, Hashnode API token
  HASHNODE_PUBLICATION_ID - required, publication ID
  PROJECT_SITE_URL       - required, source site URL
  PROJECT_CONTENT_DIR    - required, relative path to blog markdown dir
  HASHNODE_TAGS          - comma-separated tag slugs, e.g. ai,career,learning,productivity
  HASHNODE_HOOK          - optional markdown hook prepended to body. Use {site_url} placeholder.

Tracks posted articles in .github/scripts/.hashnode-log.json (committed back).
"""
import json
import os
import re
import sys
import urllib.request
import urllib.error
from datetime import date
from pathlib import Path

TOKEN = os.environ["HASHNODE_TOKEN"]
PUB_ID = os.environ["HASHNODE_PUBLICATION_ID"]
SITE_URL = os.environ["PROJECT_SITE_URL"]
CONTENT_DIR = Path(os.environ["PROJECT_CONTENT_DIR"])
TAG_SLUGS = [t.strip().lower() for t in os.environ.get("HASHNODE_TAGS", "").split(",") if t.strip()]
HOOK = os.environ.get("HASHNODE_HOOK", "").format(site_url=SITE_URL) if os.environ.get("HASHNODE_HOOK") else ""

LOG_PATH = Path(__file__).parent / ".hashnode-log.json"
GQL_URL = "https://gql.hashnode.com/"


def load_log():
    return json.loads(LOG_PATH.read_text()) if LOG_PATH.exists() else {}


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


def gql(query, variables=None):
    payload = {"query": query, "variables": variables or {}}
    req = urllib.request.Request(
        GQL_URL,
        data=json.dumps(payload).encode(),
        headers={"Authorization": TOKEN, "Content-Type": "application/json",
                 "User-Agent": "stack2026-crosspost/1"},
        method="POST",
    )
    with urllib.request.urlopen(req, timeout=30) as r:
        d = json.loads(r.read().decode())
    if d.get("errors"):
        raise RuntimeError(json.dumps(d["errors"])[:500])
    return d["data"]


PUBLISH_MUTATION = """
mutation PublishPost($input: PublishPostInput!) {
  publishPost(input: $input) {
    post { id title slug url }
  }
}
"""


def publish(path, log):
    slug = path.stem
    if slug in log:
        print(f"  skip: {slug}")
        return False
    fm, body = parse_frontmatter(path.read_text())
    if str(fm.get("draft", "")).lower() == "true":
        print(f"  skip (draft): {slug}")
        return False
    body = clean_body(body)
    canonical = f"{SITE_URL}/blog/{slug}/"
    footer = f"\n\n---\n\n*Originally published on [{SITE_URL.replace('https://', '')}]({canonical}).*\n"
    content = HOOK + body + footer

    tags = [{"slug": s, "name": s.capitalize()} for s in TAG_SLUGS[:5]]

    input_var = {
        "title": fm["title"],
        "contentMarkdown": content,
        "publicationId": PUB_ID,
        "tags": tags,
        "originalArticleURL": canonical,
    }
    if fm.get("image"):
        input_var["coverImageOptions"] = {"coverImageURL": fm["image"]}

    try:
        data = gql(PUBLISH_MUTATION, {"input": input_var})
    except Exception as e:
        print(f"  FAIL {slug}: {e}")
        return False

    post = data["publishPost"]["post"]
    log[slug] = {"id": post["id"], "url": post["url"], "slug": post["slug"]}
    save_log(log)
    print(f"  posted {slug}: {post['url']}")
    return True


def main():
    if not CONTENT_DIR.is_dir():
        sys.exit(f"Content dir not found: {CONTENT_DIR}")
    log = load_log()
    today = date.today().isoformat()
    posted = 0
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
        if publish(md, log):
            posted += 1
    print(f"done. posted {posted} article(s) to Hashnode")


if __name__ == "__main__":
    main()
