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

# Launch Claude Code with weekly review context
claude --print "
LifeOS WEEKLY INTEGRITY REVIEW

Week $WEEK_NUM of $YEAR ending $(date +"%Y-%m-%d")
This is the most important ritual in LifeOS.

Execute full weekly protocol:

1. INGEST ALL DATA
   - Read lifeos/state/current-week.json
   - Read lifeos/state/commitments.json
   - Read lifeos/state/session-log.md (this week's entries)
   - Read lifeos/reviews/daily/* (this week)
   - Read latest dashboard export
   - Read lifeos/integrations/dayone/data/journal.json (this week's entries)

2. PROMISES AUDIT
   - List all commitments made this week
   - For each: kept, broken, or renegotiated?
   - Calculate integrity score

3. DASHBOARD REALITY
   - Status and trend for each pillar
   - Hard numbers: training mins, meetings, follow-ups, learning days, output shipped
   - Biometric trends (RHR, HRV, sleep)

4. PATTERN DETECTION
   - What repeated this week?
   - Where did structure hold?
   - Where did structure slip?
   - Update lifeos/state/patterns.json

5. NARRATIVE CHECK
   - What story am I telling myself?
   - What does the data actually say?
   - Where is the gap?

6. COURSE CORRECTION
   - Identify ONE structural adjustment
   - Must be structural, not motivational
   - Document why this one

7. RECOMMITMENT OR RELEASE
   - For each active commitment: RECOMMIT / REDUCE / DROP
   - Set commitments for next week

8. NEXT WEEK SETUP
   - Top 3 priorities
   - 2-hour block focus
   - Recovery anchors
   - Drift risks

9. LOGGING
   - Create weekly review in lifeos/reviews/weekly/week-$WEEK_NUM.md
   - Update lifeos/state/current-week.json for new week
   - Archive completed commitments

10. VERDICT
    - Overall trajectory: ON MISSION / SLIGHT DRIFT / MATERIAL DRIFT

This review should take 20-30 minutes. Facts first. No softening.
"
