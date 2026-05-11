# GitHub Actions — VM Secrets Setup Guide

## Required Repository Secrets

Go to: **github.com/Ancient1ZION/ZYN-Empire → Settings → Secrets and variables → Actions**

Add these 3 secrets:

### 1. `VM_SSH_KEY`
Your SSH private key for the GCP VM:
```bash
# On the VM, generate a deploy key:
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N "" -C "github-actions-deploy"
cat ~/.ssh/deploy_key
cat ~/.ssh/deploy_key.pub >> ~/.ssh/authorized_keys
```
Copy the **private key** contents into the `VM_SSH_KEY` secret.

### 2. `VM_KNOWN_HOSTS`
Get the VM's SSH host fingerprint:
```bash
ssh-keyscan 35.185.40.28
```
Copy the output into the `VM_KNOWN_HOSTS` secret.

### 3. `DISCORD_WEBHOOK_URL` (Optional)
Get a Discord webhook URL from your ZYN Empire server:
1. Server Settings → Integrations → Webhooks → New Webhook
2. Copy the URL
3. Paste into the `DISCORD_WEBHOOK_URL` secret

---

## How It Works

```
git push origin main
        ↓
GitHub Actions triggers
        ↓
1. Checkout code
2. Install npm dependencies (discord.js)
3. SSH into VM (35.185.40.28)
4. Pull latest code
5. npm install --production
6. Restart all 3 bots (noah-manager, auto-reports, zyn-agents)
7. Health check
8. Discord notification (optional)
```

## Testing

After setting secrets, push to trigger:
```bash
git commit --allow-empty -m "test: trigger deploy workflow"
git push origin main
```

Monitor: **Actions** tab in GitHub repo → watch deployment in real-time.