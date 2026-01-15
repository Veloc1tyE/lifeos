#!/bin/bash
# LifeOS Evening Shutdown Trigger
# Run this before bed to close loops and protect tomorrow

DASHBOARD_DIR="$HOME/Documents/dashboard"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
TODAY=$(date +"%Y-%m-%d")
DAY_OF_WEEK=$(date +"%u")  # 1=Mon, 7=Sun

echo "======================================"
echo "LifeOS Evening Shutdown"
echo "$TIMESTAMP | Abu Dhabi"
echo "======================================"

cd "$DASHBOARD_DIR"

# Pull fresh data BEFORE launching Claude
echo "Syncing Garmin data (end of day metrics)..."
python3 lifeos/integrations/garmin/sync.py 2>/dev/null || echo "Garmin sync failed"

echo "Syncing journal entries..."
python3 lifeos/integrations/dayone/sync.py 2>/dev/null || echo "DayOne sync skipped"

# Launch Claude Code with evening context
claude -p "
LifeOS EVENING SHUTDOWN

Today was $(date +"%A, %B %d, %Y").
Time: $(date +"%H:%M") Abu Dhabi (GMT+4)
Day of week index: $DAY_OF_WEEK (1=Mon, 7=Sun)

STEP 1 - MANDATORY DATA READS (do these first):
- lifeos/state/current-week.json
- lifeos/integrations/garmin/data/current.json (today's activity data)
- lifeos/integrations/dayone/data/current.json (today's journal)
- lifeos/state/dashboard-live.json (if exists)

STEP 2 - TRAINING COMPLETION CHECK (CRITICAL):
From Garmin data, check today's activities:
- What training was completed today?
- Duration in minutes?
- Type (run, elliptical, strength, etc.)?

Ask me to confirm if unclear. Do NOT assume rest day unless I confirm.

STEP 3 - EXTRACT FROM JOURNALS:
Scan today's journal entries for:
- Tasks mentioned
- People to contact
- Open loops
- Insights for pillars

STEP 4 - DAY REVIEW:
- Were Top 3 priorities completed?
- What slipped and why?
- Any drift signals?

STEP 5 - TOMORROW PREP:
- What's the training plan for tomorrow?
- Any calendar items to note?
- One adjustment for tomorrow?

STEP 6 - MANDATORY STATE UPDATE (before closing):
Update lifeos/state/current-week.json with:

1. p2_training.dailyLog - update today's entry with:
   - session: description of what was done
   - minutes: actual duration
   - confirmed: true

2. p2_training.minutesLogged - add today's minutes to total
3. p2_training.sessionsCompleted - increment if session completed

4. today.training.actual - what actually happened
5. today.critical3 - mark completed/incomplete
6. today.backlog - update status

7. biometrics array - update today's index (RHR, HRV, sleep, body battery)

8. handoff.lastSession - timestamp
9. handoff.sessionSummary - key points
10. handoff.openLoops - any unfinished items
11. handoff.nextSessionContext - tomorrow context

HARD STOP RULE: Complete state update by 20:00. No new work after shutdown.

Output: Show state changes made, then confirm shutdown complete.
"
