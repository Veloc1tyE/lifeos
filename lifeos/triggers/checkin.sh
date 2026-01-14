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

# Launch Claude Code
claude --print "
LifeOS CHECK-IN

Time: $(date +"%A, %B %d %H:%M") Abu Dhabi

Quick status check:

1. Read lifeos/state/current-week.json
2. Read lifeos/state/commitments.json (check what's due)
3. Provide brief status on all 7 pillars
4. Identify primary bottleneck right now
5. Suggest one-step correction if needed

Keep response under 200 words. Facts only.
"
