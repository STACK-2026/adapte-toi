# Content Guard (adapte-toi)

Garde-fou de contenu STACK-2026 qui bloque le build local si un article `.md`/`.mdx`
contient un defaut connu de blog-auto.

## Role

`site/scripts/content_guard.py` (copie du guard partage `~/stack-2026/scripts/content_guard.py`)
detecte et, en mode `--fix`, corrige :

1. Artefacts de generation / tool-call (`</content>`, `</invoke>`, `<function_calls>`, fences perdus) — ont deja casse des builds dans le parc.
2. Frontmatter duplique reinjecte dans le corps.
3. Longueur meta : `title` > 65c (flag seul), `description` > 180c (clampe en `--fix`).
4. H1 (`# `) dans le corps => double H1 (le template emet deja le titre en H1).
5. Mojibake (`Ã©`, `â€™`, `Â`, ...).
6. Tiret cadratin / demi-cadratin dans le corps.

Couvre toutes les collections (`actu`, `blog`, `guides`, `metiers`, `outils`, `pages`)
via le plein-scan sur `src/content`.

## Pourquoi

Ces defauts passaient `seo-guardrails.yml` + `publish.py` et n'etaient vus qu'apres
deploiement. Le guard les arrete AVANT le build.

## Prebuild bloquant

`site/package.json` :

```json
"guard:content": "sh scripts/guard-content.sh",
"prebuild": "npm run guard:content",
```

`scripts/guard-content.sh` verifie les `.md`/`.mdx` du dernier commit
(`git diff HEAD~1 HEAD`), avec repli plein-scan sur `src/content`, et sort
proprement (exit 0) si `python3` est absent. `npm run build` declenche `prebuild` ;
un defaut bloquant => build en echec.

## Re-verifier / corriger

```bash
cd site
npm run guard:content
python3 scripts/content_guard.py --check src/content
python3 scripts/content_guard.py --fix   src/content   # idempotent, non destructif
```

## Resultat du backfill

`--fix` initial sur `src/content` : 9 fichiers corriges (descriptions > 180c clampees
sur la collection `actu`).
