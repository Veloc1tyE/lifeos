#!/bin/bash
# LifeOS Evening - Syncs data and launches evening shutdown session

DASHBOARD_DIR="$HOME/Documents/dashboard"
cd "$DASHBOARD_DIR"

# Ensure sync server is running
if ! curl -s http://localhost:3456/health > /dev/null 2>&1; then
    echo "Starting dashboard sync server..."
    python3 lifeos/sync-server.py &
    sleep 1
fi

# Sync all data sources (Garmin for training data)
echo "Syncing data..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null
python3 lifeos/integrations/dayone/sync.py 2>/dev/null

# Launch Claude with evening shutdown prompt
exec claude -p "Evening shutdown. Log today's training, close loops, update handoff. Hard stop by 20:00."
