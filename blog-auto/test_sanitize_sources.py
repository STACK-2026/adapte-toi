"""Schema-safety tests for the actu frontmatter sanitizer.

The actu `sources[].url` schema is `z.string().url()` and `sources` is `.min(1)`.
The generator must never commit a source whose url is empty/non-http, because that
throws InvalidContentEntryDataError and silently red-fails the deploy (incident 25/06).
"""
import importlib.util
import pathlib

_here = pathlib.Path(__file__).parent
spec = importlib.util.spec_from_file_location("actu_watch", _here / "actu_watch.py")
aw = importlib.util.module_from_spec(spec)
spec.loader.exec_module(aw)

MDX_BAD_URL = '''---
title: "T"
description: "d"
category: "menace"
sources:
  - title: "Good"
    url: "https://example.com/x"
    outlet: "BFM"
    date: 2026-06-25
  - title: "Bad empty"
    url: ""
    outlet: "FT"
    date: 2026-06-24
---
body text here
'''


def test_drops_empty_url_source():
    out = aw._sanitize_actu_frontmatter(MDX_BAD_URL)
    assert 'url: ""' not in out, "empty-url source must be dropped"
    assert "https://example.com/x" in out, "valid source must be kept"
    assert out.count("- title:") == 1, "exactly one (valid) source must remain"


def test_keeps_all_valid_sources():
    mdx = '''---
title: "T"
description: "d"
category: "etude"
sources:
  - title: "A"
    url: "https://a.com/1"
    outlet: "A"
  - title: "B"
    url: "http://b.org/2"
    outlet: "B"
---
body
'''
    out = aw._sanitize_actu_frontmatter(mdx)
    assert out.count("- title:") == 2, "both valid sources kept"


def test_all_invalid_keeps_original_block():
    # never emit a sourceless actu (schema requires min(1)); leave it for the build
    # gate to catch loudly rather than produce a structurally different defect.
    mdx = '''---
title: "T"
description: "d"
category: "annonce"
sources:
  - title: "Bad"
    url: ""
    outlet: "X"
---
body
'''
    out = aw._sanitize_actu_frontmatter(mdx)
    assert "sources:" in out


if __name__ == "__main__":
    test_drops_empty_url_source()
    test_keeps_all_valid_sources()
    test_all_invalid_keeps_original_block()
    print("ALL PASS")
