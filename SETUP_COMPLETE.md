# 🏛️ ZYN EMPIRE — COMPLETE SETUP GUIDE
**Last Updated:** May 11, 2026
**Target:** Fresh Ubuntu 22.04 GCP VM (`35.185.40.28`)

---

## 📋 CONTENTS

- [Part 1: VM Initial Setup](#part-1)
- [Part 2: Install Dependencies](#part-2)
- [Part 3: Deploy Code](#part-3)
- [Part 4: Configure Discord Bot](#part-4)
- [Part 5: Start All Services](#part-5)
- [Part 6: Verify Everything](#part-6)
- [Part 7: Enable Auto-Deploy (GitHub Actions)](#part-7)
- [Part 8: Dashboard Access](#part-8)
- [Part 9: Firewall Rules](#part-9)
- [Troubleshooting](#troubleshooting)

---

<a name="part-1"></a>
## Part 1: VM Initial Setup

### Connect to your VM
```bash
gcloud compute ssh zion@35.185.40.28 --project=zyn-empire-prod
# OR if SSH keys are set up:
ssh zion@35.185.40.28
```

### Update system
```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl wget git python3-pip python3-venv nginx ufw htop
```

### Create project directory
```bash
mkdir -p /home/zion/zyn/logs
cd /home/zion/zyn
```

### Install Node.js 20 LTS
```bash
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs
node --version   # should show v20.x
npm --version    # should show 10.x+
```

### Install PM2 (Process Manager)
```bash
sudo npm install -g pm2
pm2 --version

# Set up PM2 startup script (auto-restart on reboot)
pm2 startup systemd -u zion --hp /home/zion
# Copy the command it outputs and run it, e.g.:
# sudo env PATH=$PATH:/usr/bin /usr/lib/node_modules/pm2/bin/pm2 startup systemd -u zion --hp /home/zion
```

### Install Python dependencies
```bash
pip3 install requests flask  # lightweight deps for dashboard + price fetch
```

---

<a name="part-2"></a>
## Part 2: Install Project Dependencies

### Clone the repo (if not already done)
```bash
cd /home/zion/zyn
if [ ! -d ".git" ]; then
    git clone https://github.com/Ancient1ZION/ZYN-Empire.git .
else
    git pull origin main
fi
```

### Install npm packages
```bash
cd /home/zion/zyn
npm install --production
```

**Verify:**
```bash
ls node_modules/discord.js/package.json
npm ls discord.js  # should show discord.js ^14.16.3
```

---

<a name="part-3"></a>
## Part 3: Configure Discord Bot Token

### Get your Discord bot token
1. Go to: https://discord.com/developers/applications
2. Select your app (or create new: "Noah the Architect")
3. Go to **Bot** → **Reset Token** → Copy the token
4. Enable these **Privileged Gateway Intents**:
   - ✅ PRESENCE INTENT
   - ✅ SERVER MEMBERS INTENT
   - ✅ MESSAGE CONTENT INTENT

### Save the token
```bash
echo "PASTE_YOUR_DISCORD_BOT_TOKEN_HERE" > /home/zion/zyn/token.txt
chmod 600 /home/zion/zyn/token.txt
cat /home/zion/zyn/token.txt  # verify it has content
```

### Add the bot to your Discord server
1. Go to **OAuth2** → **URL Generator**
2. Scopes: `bot` + `applications.commands`
3. Bot Permissions: `Administrator` (or at minimum: `Send Messages`, `Read Messages`, `Embed Links`, `Manage Webhooks`)
4. Copy the generated URL and open it in browser
5. Select your **Z.Y.N Empire** server → Authorize

---

<a name="part-4"></a>
## Part 4: Verify Discord Channel IDs

Run the channel discovery tool to map your channels:
```bash
cd /home/zion/zyn
node channel_discovery.js
```

This prints all channel names and IDs. Cross-reference with the expected channels in `agents_config.json` and update channel IDs if they differ.

---

<a name="part-5"></a>
## Part 5: Start All Services

### Option A: Using setup script (Recommended)
```bash
cd /home/zion/zyn
bash setup_empire.sh
```

### Option B: Manual start
```bash
cd /home/zion/zyn

# Kill any existing processes
pm2 delete all 2>/dev/null || true

# Start Noah (conversational bot)
pm2 start noah_discord.js --name noah-manager

# Start Auto Reports (system health reporter)
pm2 start auto_reports.js --name auto-reports

# Start Agents (Sara, Malik, Adam, Elijah, Lea, Caleb)
pm2 start agents.js --name zyn-agents

# Start Dashboard on port 80
sudo pm2 start "python3 -m http.server 80 --directory /home/zion/zyn" --name zyn-dashboard --user root

# Save state (survives reboot)
pm2 save
```

---

<a name="part-6"></a>
## Part 6: Verify Everything

### Check PM2 processes
```bash
pm2 list
```

**Expected output (all ONLINE):**

| id  | name          | status    | cpu | memory    |
|-----|---------------|-----------|-----|-----------|
| 0   | noah-manager  | online    | ~0% | ~50 MB    |
| 1   | auto-reports  | online    | ~0% | ~50 MB    |
| 2   | zyn-agents    | online    | ~0% | ~50 MB    |
| 3   | zyn-dashboard | online    | ~0% | ~30 MB    |

### Check logs
```bash
pm2 logs noah-manager --lines 20     # Should show "Online as Noah#2924"
pm2 logs zyn-agents --lines 20       # Should show "All 6 agents active"
pm2 logs auto-reports --lines 20     # Should show "Online as ..."
```

### Test bot commands (in Discord)
Type in any channel:
- `yo` → Status overview
- `status` → Full system status
- `help` → All commands
- `agents` → All 19 agents listed
- `trade` → NQ trading status
- `money` → Revenue pipeline

### Test dashboard
```bash
curl -s http://localhost:80 | head -5
# Should return HTML with "ZYN EMPIRE"
```

### Run diagnostics (optional)
```bash
node diagnose_discord.js
```

### Run all Python agents
```bash
python3 AGENTS.py
# Should initialize all 19 agents with demo tasks
```

### Run Master Control
```bash
python3 MASTER_CONTROL.py --cycles 1 --interval 60
```

---

<a name="part-7"></a>
## Part 7: Enable Auto-Deploy (GitHub Actions)

### Step 1: Generate SSH key on VM
```bash
ssh-keygen -t ed25519 -f ~/.ssh/deploy_key -N "" -C "github-actions-deploy"
cat ~/.ssh/deploy_key          # COPY THIS (private key)
cat ~/.ssh/deploy_key.pub >> ~/.ssh/authorized_keys
```

### Step 2: Add repository secrets on GitHub
Go to: **https://github.com/Ancient1ZION/ZYN-Empire/settings/secrets/actions**

Click **New repository secret** and add:

| Name | Value |
|------|-------|
| `VM_SSH_KEY` | Contents of `~/.ssh/deploy_key` (private key) |
| `VM_KNOWN_HOSTS` | Output of `ssh-keyscan 35.185.40.28` |
| `DISCORD_WEBHOOK_URL` | Your Discord webhook URL (optional, for deploy alerts) |

### Step 3: Add the workflow file
Since the OAuth token lacks `workflow` scope, add the file manually:

**Method 1 — GitHub UI:**
1. Go to repo → **Actions** tab → **Set up a workflow yourself**
2. Delete the default content
3. Paste contents of `.github/workflows/deploy.yml`
4. Name: `.github/workflows/deploy.yml`
5. Click **Start commit**

**Method 2 — Direct push:**
```bash
# On your local machine, push the .github folder separately:
git add .github/
git commit -m "feat: add GitHub Actions deploy workflow"
git push origin HEAD:main
```
*(Requires a token with `workflow` scope)*

---

<a name="part-8"></a>
## Part 8: Dashboard & Website Access

### GitHub Pages (Public)
```
https://ancient1zion.github.io/zynwebsite
```
*(Ensure the `dashboard.html` is in the `docs/` folder or `gh-pages` branch, or configure GitHub Pages to serve from root)*

### Local Dashboard (Private)
```
http://localhost:80
http://35.185.40.28
```

### External Access
```
http://EXTERNAL_IP_OF_VM
```

---

<a name="part-9"></a>
## Part 9: Firewall Rules

### GCP Firewall
In **Google Cloud Console → VPC Network → Firewall Rules**, create:

| Name | Direction | Targets | Protocols | Ports | Source |
|------|-----------|---------|-----------|-------|--------|
| allow-http | Ingress | All instances | TCP | 80 | 0.0.0.0/0 |
| allow-https | Ingress | All instances | TCP | 443 | 0.0.0.0/0 |
| allow-ssh | Ingress | All instances | TCP | 22 | Your IP / 32 |

### UFW (on VM)
```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw enable
sudo ufw status
```

---

## 🛠️ Post-Setup Checklist

- [ ] All 4 PM2 processes showing `online`
- [ ] Noah responds to `yo` in Discord
- [ ] Agents posting hourly to their channels
- [ ] Dashboard accessible at `http://localhost:80`
- [ ] GitHub Pages serving `dashboard.html`
- [ ] PM2 startup saves (survives reboot)
- [ ] SSH key added to GitHub secrets
- [ ] GitHub Actions workflow active
- [ ] Firewall configured (ports 80, 443, SSH only)

---

## 📁 Complete File Inventory (All 25 Files)

### Core System
| File | Purpose |
|------|---------|
| `AGENTS.py` | 19-agent autonomous engine (Python) |
| `MASTER_CONTROL.py` | Central orchestration hub (Python) |
| `START_ENGINE.py` | Bootstrap script (Python) |
| `agents_config.json` | Configuration (19 agents, channels, integrations) |
| `index.js` | Main entry point with crash handlers |

### Discord Bots
| File | Purpose |
|------|---------|
| `noah_discord.js` | Conversational bot (14 keyword commands) |
| `agents.js` | 6 active agents posting hourly to 12 channels |
| `auto_reports.js` | System health reporter (hourly) |
| `channel_discovery.js` | One-time channel ID discovery |
| `diagnose_discord.js` | Diagnostic tool (prints all channels, roles) |

### Web Dashboard
| File | Purpose |
|------|---------|
| `dashboard.html` | Web UI v12.2 (dark theme, live stats, 19 agents) |
| `index.html` | Landing page for domain root |

### Infrastructure
| File | Purpose |
|------|---------|
| `package.json` | npm dependencies (`discord.js`) |
| `price_fetch.py` | Live NQ futures price from Yahoo Finance |
| `DEPLOY.sh` | One-command redeploy |
| `setup_empire.sh` | Full initial setup + PM2 start |
| `repair_zyn.sh` | Auto-repair (reinstall deps, restart bots) |
| `jitro_autopilot.sh` | Health monitor + crash recovery |
| `nginx.conf` | Production nginx configuration |
| `.env.example` | Configuration template |
| `.github/workflows/deploy.yml` | GitHub Actions auto-deploy |
| `SETUP_SECRETS.md` | GitHub secrets setup guide |

### Documentation
| File | Purpose |
|------|---------|
| `README.md` | Master documentation (all 19 agents, commands, architecture) |
| `QUICKSTART.md` | Quick start guide |
| `DRY_RUN_REPORT.md` | Dry run execution report |
| `DEPLOYMENT_CHECKLIST.md` | Deployment checklist |

### Automation (from original repo)
| File | Purpose |
|------|---------|
| `APPLY_LEADS_NOW.py` | Trigger immediate lead assignment |
| `AUTO_APPLY_ASSIGNMENTS.py` | Automatic lead assignment engine |
| `LEAD_ASSIGNMENT_ENGINE.py` | Production lead routing |
| `ERROR_HANDLER.py` | Error handling module |
| `SCHEDULER.py` | Task scheduler |
| `RUN_ALL.ps1` | Windows: Run all processes |
| `RUN_NOW.ps1` | Windows: Trigger lead assignment |
| `RUN_AUTO_APPLY.ps1` | Windows: Auto-apply assigner |
| `LEAD_APPLY.ps1` | Windows: Lead assignment |
| `SETUP.bat` | Windows setup script |

---

## 🔄 Daily Operations

### Check system health
```bash
pm2 list
```

### View bot logs
```bash
pm2 logs noah-manager --lines 10
pm2 logs zyn-agents --lines 10
pm2 logs auto-reports --lines 10
```

### Restart a crashed bot
```bash
pm2 restart noah-manager
```

### Redeploy after code changes
```bash
cd /home/zion/zyn
git pull origin main
npm install --production
pm2 restart all
```

### Run Python agents
```bash
python3 AGENTS.py
```

### Run Master Control cycle
```bash
python3 MASTER_CONTROL.py --cycles 1 --interval 60
```

---

**ZYN EMPIRE — FULLY OPERATIONAL** 🏛️
*3 Discord bots | 19 agents | Web dashboard | GitHub Actions auto-deploy*