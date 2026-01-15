#!/bin/bash
# LifeOS Weekly - Full integrity review

DASHBOARD_DIR="$HOME/Documents/dashboard"
cd "$DASHBOARD_DIR"

# Ensure sync server is running
if ! curl -s http://localhost:3456/health > /dev/null 2>&1; then
    echo "Starting dashboard sync server..."
    python3 lifeos/sync-server.py &
    sleep 1
fi

# Sync all data sources
echo "Syncing all data..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null
python3 lifeos/integrations/dayone/sync.py --days 7 2>/dev/null
python3 lifeos/integrations/calendar/sync.py 2>/dev/null
python3 lifeos/integrations/gmail/sync.py 2>/dev/null

# Launch Claude with weekly review prompt
exec claude -p "Weekly integrity review. Run the full review: kept promises, broken promises with disposition, ONE structural adjustment as a rule."
