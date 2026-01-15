#!/bin/bash
# LifeOS Quick Check-in
# Run anytime for a quick status check and course correction

DASHBOARD_DIR="$HOME/Documents/dashboard"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "======================================"
echo "LifeOS Check-in"
echo "$TIMESTAMP | Abu Dhabi"
echo "======================================"

cd "$DASHBOARD_DIR"

# Pull fresh data BEFORE launching Claude
echo "Syncing data..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null || echo "Garmin sync skipped"

# Launch Claude Code with explicit state update requirements
claude -p "
LifeOS CHECK-IN

Time: $(date +"%A, %B %d %H:%M") Abu Dhabi

MANDATORY DATA READS:
1. Read lifeos/state/current-week.json (handoff, today, pillar status)
2. Read lifeos/integrations/garmin/data/current.json (fresh biometrics)
3. Read lifeos/state/dashboard-live.json if exists

THEN:
1. Provide brief status on all 7 pillars (one line each)
2. Identify primary bottleneck right now
3. Suggest one-step correction if needed

MANDATORY STATE UPDATE:
Before closing, update lifeos/state/current-week.json:
- today.dayState
- today.frictionScore
- handoff.lastSession with timestamp
- Any task status changes

Keep response under 200 words after state update. Facts only.
"
