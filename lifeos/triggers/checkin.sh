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

# Create temp file for output capture
TEMP_OUTPUT=$(mktemp)

# Launch Claude and capture output (tee shows output while capturing)
claude -p "Quick check-in. Show current status and any signals that need attention. Output any state updates between <<<QUEUE_START>>> and <<<QUEUE_END>>> markers as JSON array." 2>&1 | tee "$TEMP_OUTPUT"

# Process any queued data
./lifeos/triggers/queue-processor.sh "$TEMP_OUTPUT"
