#!/bin/bash
# ZYN EMPIRE - Deploy & Start Script
# Run from ~/zyn/ directory

set -e

echo "=============================================="
echo "ZYN EMPIRE - DEPLOY & START"
echo "=============================================="

cd /home/zion/zyn

# Pull latest code
echo "[1/6] Pulling latest code..."
git pull origin main

# Start Master Control (validates config)
echo "[2/6] Running Master Control validation..."
python3 MASTER_CONTROL.py --cycles 1 --interval 1

# Start dashboard on port 80
echo "[3/6] Starting dashboard on port 80..."
sudo pm2 delete zyn-dashboard 2>/dev/null || true
sudo pm2 start "python3 -m http.server 80 --directory /home/zion/zyn" --name zyn-dashboard --user root

# Restart Discord bots
echo "[4/6] Restarting Discord bots..."
pm2 delete noah-manager 2>/dev/null || true
pm2 delete auto-reports 2>/dev/null || true
pm2 delete zyn-agents 2>/dev/null || true

pm2 start noah_discord.js --name noah-manager
pm2 start auto_reports.js --name auto-reports
pm2 start agents.js --name zyn-agents

# Save PM2 process list
echo "[5/6] Saving PM2 process list..."
pm2 save

# Show status
echo "[6/6] Deployment complete!"
echo ""
pm2 list
echo ""
echo "=============================================="
echo "ZYN EMPIRE DEPLOYED ✅"
echo "Dashboard: http://localhost:80"
echo "GitHub Pages: https://ancient1zion.github.io/zynsl-website/dashboard.html"
echo "=============================================="
