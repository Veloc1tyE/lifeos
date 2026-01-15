#!/bin/bash
# LifeOS Morning - Syncs data and launches morning calibration session

DASHBOARD_DIR="$HOME/Documents/dashboard"
cd "$DASHBOARD_DIR"

# Ensure sync server is running
if ! curl -s http://localhost:3456/health > /dev/null 2>&1; then
    echo "Starting dashboard sync server..."
    python3 lifeos/sync-server.py &
    sleep 1
fi

# Sync all data sources
echo "Syncing data..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null
python3 lifeos/integrations/dayone/sync.py 2>/dev/null
python3 lifeos/integrations/calendar/sync.py 2>/dev/null

# Launch Claude with morning calibration prompt
exec claude -p "Morning calibration. Read current state, extract journal items, assess trajectory, and lock in today's priorities."
