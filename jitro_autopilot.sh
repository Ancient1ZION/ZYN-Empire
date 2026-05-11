#!/bin/bash
# ZYN JITRO AUTOPILOT
# Keeps all bots running, auto-restarts on crash, monitors health

HOME_DIR="/home/zion/zyn"
LOG_FILE="$HOME_DIR/logs/autopilot.log"

mkdir -p "$HOME_DIR/logs"

log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_pm2() {
    local process=$1
    if ! pm2 describe "$process" &>/dev/null; then
        log "⚠️  $process not found — starting..."
        cd "$HOME_DIR"
        case $process in
            noah-manager)    pm2 start noah_discord.js --name noah-manager ;;
            auto-reports)    pm2 start auto_reports.js --name auto-reports ;;
            zyn-agents)      pm2 start agents.js --name zyn-agents ;;
            zyn-dashboard)   sudo pm2 start "python3 -m http.server 80 --directory $HOME_DIR" --name zyn-dashboard --user root ;;
        esac
        return 1
    fi
    return 0
}

log "========== AUTOPILOT CHECK STARTED =========="

cd "$HOME_DIR"

# Check and restart each process
for proc in noah-manager auto-reports zyn-agents zyn-dashboard; do
    if check_pm2 "$proc"; then
        # Check if it's errored
        STATUS=$(pm2 describe "$proc" 2>/dev/null | grep "status" | awk '{print $3}')
        if [ "$STATUS" = "errored" ]; then
            log "🔄 $proc is errored — restarting..."
            pm2 restart "$proc"
        else
            log "✅ $proc is $STATUS"
        fi
    fi
done

# Ensure PM2 saves state
pm2 save 2>/dev/null

log "========== AUTOPILOT CHECK COMPLETE =========="