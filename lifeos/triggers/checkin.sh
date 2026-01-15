#!/bin/bash
# LifeOS Check-in - Quick status check with Claude

DASHBOARD_DIR="$HOME/Documents/dashboard"
cd "$DASHBOARD_DIR"

# Ensure sync server is running
if ! curl -s http://localhost:3456/health > /dev/null 2>&1; then
    echo "Starting dashboard sync server..."
    python3 lifeos/sync-server.py &
    sleep 1
fi

# Quick Garmin sync
echo "Syncing Garmin..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null

# Launch Claude with quick checkin prompt
exec claude -p "Quick check-in. Show current status and any signals that need attention."
