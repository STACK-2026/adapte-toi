# Adapte-toi : plan visibilité accélérée 5% → 1%

**Date** : 2026-04-25
**Goal** : passer adapte-toi.com du top 5% au top 1% francophone IA × emploi via 8 phases d'expansion contenu + autorité topique.
**Architecture** : 7 phases additives, chacune livrable indépendante, build cumulé. Pas de refonte technique, on capitalise sur l'existant Astro+CF Pages+collections.
**Tech Stack** : Astro 5 SSG, Cloudflare Pages, Tailwind v4, content collections (`actu` `blog` `guides` `metiers` `outils`), satori OG, pipeline Mistral+Claude actu_watch.

---

## Etat de départ (audit 25/04 21h)

- 116 URLs sitemap, lastmod fresh
- 21 fiches outils (700-900 mots chacune, sous-densifiées vu volumes Bing 28K-3.9M)
- 26 fiches métier
- 11 guides + 10 blog (cannibalisation `formation-ia-gratuite` détectée)
- 0 page comparateur (`X vs Y`) malgré le potentiel évident
- Schemas Article + Breadcrumb OK, manque Product/SoftwareApplication + Review + FAQ
- robots.txt 11 bots IA + llms.txt + ChatGPT-User OK depuis ce soir

## Cibles keywords (volumes Bing fournis)

| Keyword | Vol Bing/mois | Priorité |
|---|---|---|
| perplexity ai en français | 28K | P0 |
| formation ia gratuite | 518 | P0 |
| bmo france travail 2026 | 92 | P1 (niche autorité) |
| cursor (terme) | 1.5M (large) | P0 |
| perplexity (terme) | 3.9M (large) | P0 |

Dérivées hautes valeurs : `perplexity vs chatgpt`, `cursor vs copilot`, `claude vs chatgpt`, `outils ia gratuits`, `chatgpt en français`, `outils ia pour [métier]`.

---

## Phase 0 : Foundation (30 min)

### Task 0.1 — Résoudre cannibalisation `formation-ia-gratuite`
**Files:**
- Delete: `site/src/content/blog/formation-ia-gratuite-10-cours-ligne-debuter.md`
- Modify: `site/src/content/guides/se-former-ia-gratuitement.md` (devient pillar)
- Create: `site/public/_redirects` (ajouter ligne 301)

**Steps:**
- [ ] Lire le contenu du blog/ et merger les passages uniques dans guides/
- [ ] Supprimer le doublon blog/
- [ ] Ajouter redirect 301 : `/blog/formation-ia-gratuite-10-cours-ligne-debuter/ /guides/se-former-ia-gratuitement/ 301`
- [ ] Build local, vérifier les 2 URLs
- [ ] Commit `seo: kill cannibalisation formation-ia-gratuite (blog→guides 301)`

### Task 0.2 — Util schemas réutilisables (FAQ + SoftwareApplication + Comparison)
**Files:**
- Modify: `site/src/utils/seo.ts`

**Steps:**
- [ ] Ajouter `jsonLdFAQ(items)` (Question/acceptedAnswer)
- [ ] Ajouter `jsonLdSoftwareApplication({ name, url, pricing, rating, reviewCount, ... })`
- [ ] Ajouter `jsonLdComparison({ items: [{name, url}] })` (ItemList type)
- [ ] Build, commit `seo: add FAQ/SoftwareApp/ItemList schema helpers`

---

## Phase 1 : Tier 1 — 6 pages comparateur (jour 1, money pages)

Format unique : 2500-3500 mots, tableau comparatif détaillé, FAQ 8-10 Q, verdict tranché par persona, CTA double, schemas full.

Slugs cible (collection `guides` pour réutiliser le layout BlogLayout existant) :

1. `guides/perplexity-vs-chatgpt.md` — capture "perplexity ai en français" + "perplexity vs chatgpt"
2. `guides/cursor-vs-github-copilot.md` — capture "cursor" 1.5M
3. `guides/claude-vs-chatgpt.md` — autorité topique LLM
4. `guides/perplexity-vs-google.md` — décrochage moteur recherche
5. `guides/midjourney-vs-dalle-vs-firefly.md` — génération image (pivot rond)
6. `guides/notion-ai-vs-chatgpt.md` — productivité

Pour chaque page :
- [ ] Frontmatter `category: "Comparateur"`, `lastReviewed`, `keywords` ciblés, `tldr` 4 bullets
- [ ] Intro 250 mots avec angle reconversion/emploi (différenciation Frandroid/Numerama)
- [ ] Tableau comparatif 12-15 lignes (prix, FR support, intégrations, sources, vitesse, verdict)
- [ ] Section "Lequel choisir si tu es..." × 5 personas (salarié inquiet, freelance, étudiant, cadre, demandeur emploi)
- [ ] Cas d'usage concrets (3-5 par outil avec mini-tutos)
- [ ] FAQ 8 Q (incl. "X est-il en français ?", "X est-il gratuit ?", "X vs Y pour [métier]")
- [ ] Verdict final + CTA affilié si dispo
- [ ] JSON-LD : Article + Comparison ItemList + FAQPage + Breadcrumbs
- [ ] OG image satori personnalisée
- [ ] Commit individuel par page

---

## Phase 2 : Etoffer 21 fiches outils existantes (jours 2-3)

Pour chaque `outils/*.md`, passer de 700-900 → 2000-2500 mots :

- [ ] Section **"[Outil] en français"** (capte le 28K vol perplexity FR + variantes chatgpt/cursor)
- [ ] Section **"[Outil] gratuit ou payant ?"** avec tableau plans
- [ ] Section **"Tutoriel express : 3 cas d'usage pour [métier1] [métier2] [métier3]"**
- [ ] Section **"Alternatives à [Outil]"** (3 alternatives + lien interne /outils/X)
- [ ] Section **"FAQ"** 6-8 Q
- [ ] Schema upgrade : ajouter `SoftwareApplication` + `Review` + `aggregateRating` + `FAQPage`
- [ ] Commit groupé par batch de 5 outils

Priorité d'exécution : perplexity, cursor, chatgpt, claude, midjourney, notion-ai, copilot (les 7 high-volume), puis le reste.

---

## Phase 3 : Cluster `/formation-ia-gratuite/` (jour 4)

### Task 3.1 — Pillar refondu
- [ ] `guides/se-former-ia-gratuitement.md` passé à 3500 mots
- [ ] TL;DR + tableau 10 formations + filtres (durée, niveau, certif)
- [ ] CTA quiz `/diagnostic/`
- [ ] FAQ 10 Q

### Task 3.2 — 5 spokes
- [ ] `guides/formation-ia-cpf-comment-financer.md` (existe partiel, étoffer)
- [ ] `guides/formation-ia-coursera-en-francais.md` (NEW)
- [ ] `guides/formation-ia-openclassrooms.md` (NEW)
- [ ] `guides/formation-ia-sans-bac.md` (NEW)
- [ ] `guides/formation-ia-quiz-quel-niveau.md` (NEW)

Maillage interne pillar↔spokes obligatoire.

---

## Phase 4 : Programmatic `/outils-ia-pour-[metier]/` (jours 5-6, 12 pages)

Nouvelle collection `outils-pro` (ou réutiliser `guides`). Format 1500 mots :

- [ ] `comptable` — top 5 outils (chatgpt, perplexity, copilot, notion-ai, claude)
- [ ] `avocat`
- [ ] `marketing`
- [ ] `commercial`
- [ ] `rh-recruteur`
- [ ] `developpeur`
- [ ] `freelance`
- [ ] `enseignant`
- [ ] `consultant`
- [ ] `journaliste`
- [ ] `graphiste`
- [ ] `community-manager`

Chaque page : intro contexte métier × IA, top 5 curé, tableau, prompts prêts à l'emploi, FAQ 5 Q, schema ItemList + FAQ, lien fiche métier `/metiers/[metier]-ia/`.

---

## Phase 5 : Pages "alternatives françaises" (jour 7, 4 pages)

- [ ] `guides/alternatives-francaises-a-perplexity.md` (Mistral, Le Chat, etc.)
- [ ] `guides/alternatives-francaises-a-chatgpt.md` (Mistral Le Chat, Hugging Chat fr)
- [ ] `guides/alternatives-francaises-a-cursor.md` (Continue, Codestral)
- [ ] `guides/alternatives-francaises-a-midjourney.md` (Stable Diffusion FR communautés)

Angle souverainté + RGPD = backlink magnet + différenciation.

---

## Phase 6 : Hub `/outils-ia-gratuits/` (jour 8)

- [ ] Nouvelle page `pages/outils-ia-gratuits/index.astro` (custom annuaire)
- [ ] Filtres : usage, métier, niveau
- [ ] 50 outils référencés (les 21 actuels + 29 nouveaux référencés)
- [ ] FAQ 8 Q
- [ ] Schema ItemList
- [ ] Cible "outils ia gratuits" (>10K vol Google+Bing)

---

## Phase 7 : Baromètre BMO 2026 (jour 9-10)

### Task 7.1 — Hub `/barometre/`
- [ ] Refondre `content/pages/barometre/` ou nouvelle page Astro custom
- [ ] Sommaire 4 baromètres trimestriels propriétaires

### Task 7.2 — Baromètre BMO France Travail 2026 décrypté
- [ ] `barometre/bmo-france-travail-2026.md`
- [ ] Charts (CSV inline) : top 30 métiers en tension × score IA
- [ ] Sources Pôle Emploi (URLs intégrales)
- [ ] FAQ 6 Q
- [ ] CTA newsletter

### Task 7.3 — Tracker mensuel licenciements IA 2026
- [ ] `barometre/licenciements-ia-2026.md`
- [ ] Tableau cumul (Klarna, IBM, Snap, Block, Duolingo, etc.) → données déjà publiées en actu/
- [ ] Update mensuel automatisable

---

## Sécurité contenu (rappels)

- **Pas d'em-dash `—` ni `–`** — virgule, deux points, point, middle dot `·`, ou tiret normal `-`. Audit `audit_standards.py` doit passer.
- **Tutoiement** systématique
- **Angle IA × emploi** explicite dès l'intro (règle adapte-toi)
- **Sources institutionnelles** obligatoires (Dares, Apec, France Stratégie, OCDE, McKinsey, Anthropic Index)
- **Auteurs** : "Léa Moreau" pour actu, "Théo Marchand" pour outils, signature humaine
- **Accents FR** propres en UTF-8 direct

## Vérification post-déploiement

À chaque phase :
- [ ] `npm run build` local OK
- [ ] `git push origin main` → CF Pages deploy
- [ ] Sitemap se met à jour automatiquement
- [ ] IndexNow ping (déjà automatisé au push si workflow existe)
- [ ] Submit BWT sitemap (script `~/stack-2026/scripts/bwt_check.py --submit-sitemap`)
- [ ] Spot-check 2 URLs random en HTTP 200
- [ ] Spot-check rich-results sur 1 nouvelle URL

---

## Métriques succès (90 jours)

| KPI | Baseline 25/04 | Cible 25/07 |
|---|---|---|
| URLs indexées Google | ~80 (estim) | 250+ |
| Impressions GSC/jour | <100 | 2000+ |
| Citations IA (ChatGPT, Perplexity) | qq | 50+/mois |
| Backlinks RD | <20 | 80+ |
| Pages 1k+ mots | ~50 | 200+ |
