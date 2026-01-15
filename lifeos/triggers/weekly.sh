#!/bin/bash
# LifeOS Weekly Integrity Review Trigger
# Run this Sunday evening - the most important ritual in LifeOS

DASHBOARD_DIR="$HOME/Documents/dashboard"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
WEEK_NUM=$(date +"%V")
YEAR=$(date +"%Y")

echo "======================================"
echo "LifeOS Weekly Integrity Review"
echo "Week $WEEK_NUM | $TIMESTAMP"
echo "======================================"

cd "$DASHBOARD_DIR"

# Pull fresh data BEFORE launching Claude
echo "Syncing all data sources..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null || echo "Garmin sync failed"
python3 lifeos/integrations/dayone/sync.py --days 7 2>/dev/null || echo "DayOne sync skipped"
python3 lifeos/integrations/calendar/sync.py 2>/dev/null || echo "Calendar sync skipped"
python3 lifeos/integrations/gmail/sync.py 2>/dev/null || echo "Gmail sync skipped"

# Launch Claude Code with weekly review context
claude -p "
LifeOS WEEKLY INTEGRITY REVIEW

Week $WEEK_NUM of $YEAR ending $(date +"%Y-%m-%d")
This is the most important ritual in LifeOS.

STEP 1 - MANDATORY DATA READS:
- lifeos/state/current-week.json (full week state + training dailyLog)
- lifeos/integrations/garmin/data/current.json (week's biometrics)
- lifeos/integrations/dayone/data/current.json (week's journals)
- lifeos/state/dashboard-live.json
- lifeos/state/session-log.md

STEP 2 - TRAINING AUDIT (CRITICAL):
Review p2_training.dailyLog for the week:
- Which days had confirmed sessions?
- Total minutes vs target?
- Any sessions missing from log that should be there?
- Calculate weekly training consistency %

STEP 3 - PROMISES AUDIT:
- List all commitments made this week
- For each: kept, broken, or renegotiated?
- Calculate integrity score

STEP 4 - DASHBOARD REALITY:
- Status and trend for each pillar
- Hard numbers: training mins, meetings, follow-ups, learning days, output shipped
- Biometric trends (RHR, HRV, sleep)

STEP 5 - PATTERN DETECTION:
- What repeated this week?
- Where did structure hold?
- Where did structure slip?

STEP 6 - NARRATIVE CHECK:
- What story am I telling myself?
- What does the data actually say?
- Where is the gap?

STEP 7 - COURSE CORRECTION:
- Identify ONE structural adjustment
- Must be structural, not motivational
- Document why this one

STEP 8 - NEXT WEEK SETUP:
- Top 3 priorities
- Training plan (day by day)
- Recovery anchors
- Drift risks

STEP 9 - MANDATORY STATE UPDATES:
1. Archive current week to lifeos/reviews/weekly/week-$WEEK_NUM.md
2. Reset current-week.json for new week:
   - Increment week number
   - Reset dailyLog with null sessions
   - Reset minutesLogged to 0
   - Reset sessionsCompleted to 0
   - Clear today section
   - Update weekStart date
3. Create handoff for new week

STEP 10 - VERDICT:
- Overall trajectory: ON MISSION / SLIGHT DRIFT / MATERIAL DRIFT

This review should take 20-30 minutes. Facts first. No softening.
"
