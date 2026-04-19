#!/usr/bin/env python3
"""
Envoie un email via Resend quand un cron GitHub Actions fail.

Utilise comme dernier step dans les workflows :
    - name: Alert on failure
      if: failure()
      env:
        RESEND_API_KEY: ${{ secrets.RESEND_API_KEY }}
      run: python blog-auto/alert_cron_failure.py "${{ github.workflow }}" "${{ github.run_id }}"

Requiert RESEND_API_KEY en env. Email destinataire hardcode (owner).
"""
from __future__ import annotations
import os
import sys
import json
import urllib.request
import urllib.error

RESEND_URL = "https://api.resend.com/emails"
FROM_EMAIL = "alerts@adapte-toi.com"  # doit etre un domaine verifie Resend
TO_EMAIL = "augustin.foucheres@gmail.com"
REPO = "STACK-2026/adapte-toi"


def main() -> int:
    api_key = os.getenv("RESEND_API_KEY", "")
    if not api_key:
        print("RESEND_API_KEY missing, skipping alert", file=sys.stderr)
        return 0  # ne casse pas le workflow pour une alerte

    workflow = sys.argv[1] if len(sys.argv) > 1 else "unknown"
    run_id = sys.argv[2] if len(sys.argv) > 2 else "unknown"
    run_url = f"https://github.com/{REPO}/actions/runs/{run_id}"

    subject = f"[adapte-toi] Cron FAIL : {workflow}"
    body_html = f"""<html><body style="font-family:system-ui,sans-serif;max-width:600px">
<h2>Cron GitHub Actions KO</h2>
<p><strong>Workflow :</strong> {workflow}</p>
<p><strong>Run ID :</strong> {run_id}</p>
<p><a href="{run_url}" style="background:#000;color:#fff;padding:10px 20px;border-radius:6px;text-decoration:none">Voir le run</a></p>
<hr>
<p><strong>Plan B manuel</strong> depuis la machine de dev (pipeline local) :</p>
<pre style="background:#f0f0f0;padding:10px;border-radius:4px;overflow-x:auto">
cd ~/stack-2026/adapte-toi/blog-auto
export ANTHROPIC_API_KEY=$(grep "^ANTHROPIC_API_KEY=" ~/stack-2026/.env.master | cut -d= -f2-)
export MISTRAL_API_KEY=$(grep "^MISTRAL_API_KEY=" ~/stack-2026/.env.master | cut -d= -f2-)
export BING_URL_SUBMISSION_KEY=$(grep "^BING_URL_SUBMISSION_KEY=" ~/stack-2026/.env.master | cut -d= -f2-)
export INDEXNOW_KEY=$(curl -sS https://adapte-toi.com/1b9f16f45a975434ae4f45a8e21bdbd0.txt)
export SITE_URL=https://adapte-toi.com
cd ~/stack-2026/adapte-toi && git pull origin main
cd blog-auto && python3 actu_watch_mistral.py --max 1
</pre>
</body></html>"""

    payload = json.dumps({
        "from": FROM_EMAIL,
        "to": [TO_EMAIL],
        "subject": subject,
        "html": body_html,
    }).encode("utf-8")

    req = urllib.request.Request(
        RESEND_URL,
        data=payload,
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "AdapteToiAlerts/1.0",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            resp = r.read().decode("utf-8")
            print(f"Alert sent: {r.status} {resp[:200]}")
            return 0
    except urllib.error.HTTPError as e:
        print(f"Alert HTTP error {e.code}: {e.read().decode('utf-8')[:200]}", file=sys.stderr)
        return 0  # ne casse pas le workflow
    except Exception as e:
        print(f"Alert error: {e}", file=sys.stderr)
        return 0


if __name__ == "__main__":
    sys.exit(main())
