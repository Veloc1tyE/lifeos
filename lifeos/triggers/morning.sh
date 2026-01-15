#!/bin/bash
# LifeOS Morning Calibration Trigger
# Run this at wake time to start the day with clarity

DASHBOARD_DIR="$HOME/Documents/dashboard"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
TODAY=$(date +"%Y-%m-%d")

echo "======================================"
echo "LifeOS Morning Calibration"
echo "$TIMESTAMP | Abu Dhabi"
echo "======================================"

cd "$DASHBOARD_DIR"

# Pull fresh data BEFORE launching Claude
echo "Syncing Garmin data..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null || echo "Garmin sync failed - check credentials"

echo "Syncing journal entries..."
python3 lifeos/integrations/dayone/sync.py 2>/dev/null || echo "DayOne sync skipped"

echo "Syncing calendar..."
python3 lifeos/integrations/calendar/sync.py 2>/dev/null || echo "Calendar sync skipped"

# Launch Claude Code with morning context
claude -p "
LifeOS MORNING CALIBRATION

Today is $(date +"%A, %B %d, %Y").
Time: $(date +"%H:%M") Abu Dhabi (GMT+4)

STEP 1 - MANDATORY DATA READS (do these first):
- lifeos/state/current-week.json
- lifeos/integrations/garmin/data/current.json (overnight biometrics)
- lifeos/integrations/dayone/data/current.json (recent journals)
- lifeos/integrations/calendar/data/current.json (today's schedule)
- lifeos/state/dashboard-live.json (if exists)

STEP 2 - EXTRACT FROM JOURNALS:
Scan journal entries for actionable items. Surface:
- Tasks mentioned ('need to...', 'should...', 'have to...')
- People to contact
- Open loops
Report findings before proceeding.

STEP 3 - BIOMETRICS CHECK:
From Garmin data, extract and report:
- Last night's sleep (duration, quality)
- RHR and HRV (note if below baseline)
- Training Readiness score
- Body Battery
Classify day state: GREEN / YELLOW / RED

STEP 4 - DAY SETUP:
- Confirm Top 3 priorities for today
- Confirm training plan for today
- Flag any calendar conflicts

STEP 5 - MANDATORY STATE UPDATE:
Update lifeos/state/current-week.json with:
- today.date = '$TODAY'
- today.dayState
- today.frictionScore
- today.critical3 (from priorities)
- today.training.planned
- biometrics array (update today's index)
- handoff.lastSession = timestamp

Output format: STATUS REPORT then confirm state was updated.
"
