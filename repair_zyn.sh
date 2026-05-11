#!/bin/bash
# ZYN EMPIRE - Repair Script
# Fixes common issues: PM2 crashes, missing dependencies, stale processes

set -e

HOME_DIR="/home/zion/zyn"
cd "$HOME_DIR"

echo "=============================================="
echo "ZYN EMPIRE - REPAIR"
echo "=============================================="

# 1. Stop all PM2
echo "[1/5] Stopping all PM2 processes..."
pm2 stop all 2>/dev/null || true
pm2 delete all 2>/dev/null || true

# 2. Reinstall npm dependencies
echo "[2/5] Reinstalling npm dependencies..."
rm -rf node_modules package-lock.json
npm install

# 3. Pull latest code
echo "[3/5] Pulling latest code..."
git stash 2>/dev/null || true
git pull origin main

# 4. Verify token exists
echo "[4/5] Checking Discord token..."
if [ -f "token.txt" ]; then
    echo "✓ token.txt exists"
    TOKEN_LEN=$(cat token.txt | wc -c)
    if [ "$TOKEN_LEN" -lt 20 ]; then
        echo "⚠️  token.txt seems too short! Check your token."
    fi
else
    echo "✗ token.txt MISSING! Create it with your Discord bot token."
fi

# 5. Restart all processes
echo "[5/5] Restarting PM2 processes..."
pm2 start noah_discord.js --name noah-manager
pm2 start auto_reports.js --name auto-reports
pm2 start agents.js --name zyn-agents
sudo pm2 start "python3 -m http.server 80 --directory $HOME_DIR" --name zyn-dashboard --user root
sleep 3

echo ""
echo "=============================================="
echo "REPAIR COMPLETE - Current Status:"
echo "=============================================="
pm2 list