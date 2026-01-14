#!/bin/bash
# LifeOS Morning Calibration Trigger
# Run this at wake time to start the day with clarity

DASHBOARD_DIR="$HOME/Documents/dashboard"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")

echo "======================================"
echo "LifeOS Morning Calibration"
echo "$TIMESTAMP | Abu Dhabi"
echo "======================================"

cd "$DASHBOARD_DIR"

# Launch Claude Code with morning context
claude --print "
LifeOS MORNING CALIBRATION

Today is $(date +"%A, %B %d, %Y").
Time: $(date +"%H:%M") Abu Dhabi (GMT+4)

Execute morning protocol:

1. INGEST
   - Read lifeos/state/current-week.json
   - Read latest dashboard export if available
   - Check commitments due today from lifeos/state/commitments.json

2. BIOMETRICS CHECK
   - Query last night's sleep data
   - Note RHR and HRV
   - Classify day state: GREEN / YELLOW / RED

3. DAY SETUP
   - Confirm Top 3 priorities for today
   - Confirm 2-hour block focus (People/Product/BizDev)
   - Flag any calendar conflicts

4. PILLAR QUICK STATUS
   - Any pillar in RED requiring load reduction?
   - Any commitments at risk today?

5. OUTPUT
   - Provide day calibration report
   - Set day state classification
   - List specific actions for today

Keep response concise. Facts first. No motivation.
"
