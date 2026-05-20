#!/usr/bin/env python3
"""Fetch a SERP brief for a single topic via Gemini 2.5 Pro + Google Search grounding.

Usage:
  python3 scripts/serp_brief_one.py "<topic>" "<niche>" > /tmp/serp_brief.json

Env required:
  GOOGLE_API_KEY (Gemini API key from .env.master or routine env)

Output: prints JSON brief to stdout. Exits 0 even if no brief (prints empty {}), so callers can grep gracefully.
"""
from __future__ import annotations
import json
import os
import sys
import urllib.request
import urllib.error

def main() -> int:
    if len(sys.argv) < 3:
        print("{}", file=sys.stdout)
        print("usage: serp_brief_one.py <topic> <niche>", file=sys.stderr)
        return 0

    topic = sys.argv[1]
    niche = sys.argv[2]
    key = os.environ.get("GOOGLE_API_KEY") or os.environ.get("GEMINI_API_KEY")

    if not key:
        print("{}", file=sys.stdout)
        print("SERP skip: no GOOGLE_API_KEY/GEMINI_API_KEY env var", file=sys.stderr)
        return 0

    prompt_text = (
        f"Tu es strategiste SEO+GEO niche {niche}. "
        f"Execute recherche Google.fr pour la requete suivante, analyse top 10 resultats, identifie ce qui ranke + ce qui manque. "
        f"Retourne UNIQUEMENT ce JSON strict (no markdown, no commentary):\n\n"
        f"REQUETE: '{topic}'\n\n"
        f"Format:\n"
        f'{{"common_angles":["3 angles couverts par majorite concurrents"],'
        f'"weak_angles":["2-3 angles mal traites ou absents"],'
        f'"winning_moves":["5 moves precis pour battre le top 3"],'
        f'"must_include_h2":["6 titres H2 a inclure pour couvrir intention"],'
        f'"paa_questions":["5 questions People Also Ask exactes"],'
        f'"citable_facts":["3 stats/chiffres concurrents citent + source a verifier"],'
        f'"entities_to_mention":["4 marques/organismes/etudes cles"],'
        f'"target_word_count":2000,'
        f'"intent_type":"informational|commercial|transactional",'
        f'"featured_snippet_opportunity":"format (definition|list|table|steps) + formulation cible",'
        f'"serp_features":["AI Overview","PAA","Featured Snippet","Video","Image Pack"]}}\n\n'
        f"Regles: JSON strict, langue match requete, prise en compte SERP features, orientation GEO (LLM citability)."
    )

    payload = json.dumps({
        "contents": [{"parts": [{"text": prompt_text}]}],
        "tools": [{"googleSearch": {}}],
        "generationConfig": {"temperature": 0.2, "maxOutputTokens": 4000},
    }).encode("utf-8")

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-pro:generateContent?key={key}"
    req = urllib.request.Request(url, data=payload, headers={"Content-Type": "application/json"})

    try:
        with urllib.request.urlopen(req, timeout=180) as resp:
            data = json.loads(resp.read().decode("utf-8"))
    except (urllib.error.HTTPError, urllib.error.URLError, json.JSONDecodeError, TimeoutError) as e:
        print("{}", file=sys.stdout)
        print(f"SERP fail: {e}", file=sys.stderr)
        return 0

    try:
        cand = data["candidates"][0]
        text = "".join(p.get("text", "") for p in cand["content"]["parts"] if "text" in p)
        text = text.strip()
        if text.startswith("```"):
            lines = text.split("\n")
            text = "\n".join(lines[1:])
            if text.rstrip().endswith("```"):
                text = text.rsplit("```", 1)[0]
        start = text.find("{")
        end = text.rfind("}")
        if start < 0 or end <= start:
            print("{}", file=sys.stdout)
            print("SERP no JSON in response", file=sys.stderr)
            return 0
        brief = json.loads(text[start : end + 1])

        # Attach grounding sources (top 15)
        gm = cand.get("groundingMetadata", {})
        chunks = gm.get("groundingChunks", [])
        brief["grounding_sources"] = [
            {
                "title": c.get("web", {}).get("title", ""),
                "uri": c.get("web", {}).get("uri", ""),
            }
            for c in chunks[:15]
        ]
        brief["topic"] = topic
        brief["niche"] = niche

        print(json.dumps(brief, ensure_ascii=False, indent=2))
        print(
            f"SERP OK: H2={len(brief.get('must_include_h2',[]))} "
            f"PAA={len(brief.get('paa_questions',[]))} "
            f"entities={len(brief.get('entities_to_mention',[]))} "
            f"sources={len(brief.get('grounding_sources',[]))}",
            file=sys.stderr,
        )
        return 0
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        print("{}", file=sys.stdout)
        print(f"SERP parse fail: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
