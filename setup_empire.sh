#!/bin/bash
# ZYN EMPIRE - Full Setup Script
# Run once on a fresh GCP VM to set up all dependencies

set -e

HOME_DIR="/home/zion/zyn"
echo "=============================================="
echo "ZYN EMPIRE - FULL SETUP"
echo "=============================================="

# 1. Install Node.js dependencies
echo "[1/6] Installing Node.js dependencies..."
cd "$HOME_DIR"
if [ ! -f "package.json" ]; then
    echo "ERROR: package.json not found!"
    exit 1
fi
npm install

# 2. Create .env from example
echo "[2/6] Setting up environment..."
if [ ! -f ".env" ] && [ -f ".env.example" ]; then
    cp .env.example .env
    echo "Created .env from .env.example"
    echo "⚠️  EDIT .env and add your API keys before running bots!"
fi

# 3. Ensure token.txt exists
echo "[3/6] Checking Discord token..."
if [ ! -f "token.txt" ]; then
    echo "ERROR: token.txt not found!"
    echo "Create token.txt with your Discord bot token:"
    echo "  echo 'YOUR_TOKEN_HERE' > token.txt"
    exit 1
fi
echo "✓ token.txt found"

# 4. Ensure Python dependencies
echo "[4/6] Checking Python..."
python3 --version
if ! command -v python3 &> /dev/null; then
    echo "ERROR: Python3 not installed"
    exit 1
fi

# 5. Create PM2 processes
echo "[5/6] Starting PM2 processes..."
cd "$HOME_DIR"

# Kill existing if any
pm2 delete noah-manager 2>/dev/null || true
pm2 delete auto-reports 2>/dev/null || true
pm2 delete zyn-agents 2>/dev/null || true
pm2 delete zyn-dashboard 2>/dev/null || true

# Start bots
pm2 start noah_discord.js --name noah-manager
pm2 start auto_reports.js --name auto-reports
pm2 start agents.js --name zyn-agents

# Start dashboard on port 80
sudo pm2 start "python3 -m http.server 80 --directory $HOME_DIR" --name zyn-dashboard --user root

# Save and startup
pm2 save
pm2 startup

echo "=============================================="
echo "ZYN EMPIRE SETUP COMPLETE ✅"
echo "=============================================="
echo ""
echo "Dashboard: https://ancient1zion.github.io/zynwebsite"
echo "Or local:  http://$(curl -s ifconfig.me)"
echo ""
pm2 list