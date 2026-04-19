# Ops adapte-toi : runbook

## Cron automatiques
- `actu-watch.yml` : 3 crons/jour lun-sam (06h37 / 12h37 / 18h37 Paris, +random 0-90min). Runner : self-hosted VPS Hetzner.
- `actu-recap.yml` : dimanche 08h37 Paris (+random). Runner : ubuntu-latest.
- `rebuild-guard.yml` : tous les jours 07h00 Paris. Touch marker + push, force rebuild CF Pages des articles programmes. Runner : ubuntu-latest.
- `deploy-site.yml` : on push main OR on workflow_run success. Runner : ubuntu-latest.

## Alerting
Chaque fail envoie un email via Resend `alerts@adapte-toi.com` -> `augustin.foucheres@gmail.com` avec lien vers le run GH Actions + bloc plan B copy-paste.

Secret GitHub : `RESEND_API_KEY` (shared STACK-2026, plan $20/mo).

## Plan B : publication manuelle si le cron fail

Depuis la machine de dev :

```bash
cd ~/stack-2026/adapte-toi/blog-auto
export ANTHROPIC_API_KEY=$(grep "^ANTHROPIC_API_KEY=" ~/stack-2026/.env.master | cut -d= -f2-)
export MISTRAL_API_KEY=$(grep "^MISTRAL_API_KEY=" ~/stack-2026/.env.master | cut -d= -f2-)
export BING_URL_SUBMISSION_KEY=$(grep "^BING_URL_SUBMISSION_KEY=" ~/stack-2026/.env.master | cut -d= -f2-)
export INDEXNOW_KEY=$(curl -sS https://adapte-toi.com/1b9f16f45a975434ae4f45a8e21bdbd0.txt)
export SITE_URL=https://adapte-toi.com

cd ~/stack-2026/adapte-toi
git pull origin main

cd blog-auto
python3 actu_watch_mistral.py --max 1
# -> fetch RSS + score + draft + audit + validate + write + commit + push + IndexNow + Bing
```

Le push declenche `deploy-site.yml` qui rebuild CF Pages en ~40s.

## Plan B urgence : deploy sans nouvel article

Si CF Pages / workflow GH est KO mais on a deja du contenu pusher :

```bash
cd ~/stack-2026/adapte-toi/site
export CLOUDFLARE_API_TOKEN=$(grep "^CLOUDFLARE_API_TOKEN=" ~/stack-2026/.env.master | cut -d= -f2-)
export CLOUDFLARE_ACCOUNT_ID=$(grep "^CLOUDFLARE_ACCOUNT_ID=" ~/stack-2026/.env.master | cut -d= -f2-)
npm run build
npx wrangler pages deploy dist --project-name=adapte-toi-site --commit-dirty=true
```

## Monitoring indexation

- IndexNow : log "IndexNow: 200 (N URLs)" dans actu-watch-logs artifact
- Bing URL Submission API : log "Bing URL Submission API: 200 (N URLs)"
- Bing sitemap ping : peut retourner 410 (deprecated cote Bing, non bloquant)

URLs a verifier apres publication :
- `https://adapte-toi.com/actu/<slug>` -> 200
- `https://adapte-toi.com/rss.xml` -> contient le nouvel article
- `https://adapte-toi.com/sitemap-news.xml` -> contient le nouvel article si < 48h

## Debug runner VPS stuck

Si actu-watch reste queued :

```bash
# Check org runners state
GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/stack-2026/.env.master | cut -d= -f2)
curl -sS -H "Authorization: Bearer $GITHUB_TOKEN" \
  https://api.github.com/orgs/STACK-2026/actions/runners \
  | python3 -m json.tool

# Si runners offline : SSH VPS Hetzner 168.119.229.20 et
#   sudo systemctl restart actions.runner.*.service
```

## Debug deploy CF Pages

Si deploy-site fail : fallback wrangler CLI local (plan B urgence ci-dessus).

## Credits used daily (approx)

- Mistral : 3 decryptages x ~60k tokens = ~180k tokens/jour, 5.4M/mois. Dans quota 1B largement.
- Claude (audit grounding) : 3 x ~14k tokens = 42k/jour, 1.3M/mois. ~$20/mois.
- GitHub Actions ubuntu-latest : ~360 min/mois (2000 free tier).
- GitHub Actions self-hosted : illimite (VPS Hetzner).
- IndexNow : gratuit.
- Bing URL Submission API : 10k URLs/jour gratuit (on utilise ~12/jour).
- CF Pages : gratuit.
- Resend : compte partage plan Pro $20/mo pour tous les projets STACK-2026.
