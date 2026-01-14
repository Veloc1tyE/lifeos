#!/bin/bash
# LifeOS Evening Shutdown Trigger
# Run this before bed to close loops and protect tomorrow

DASHBOARD_DIR="$HOME/Documents/dashboard"
TIMESTAMP=$(date +"%Y-%m-%d %H:%M:%S")
TODAY=$(date +"%Y-%m-%d")

echo "======================================"
echo "LifeOS Evening Shutdown"
echo "$TIMESTAMP | Abu Dhabi"
echo "======================================"

cd "$DASHBOARD_DIR"

# Launch Claude Code with evening context
claude --print "
LifeOS EVENING SHUTDOWN

Today was $(date +"%A, %B %d, %Y").
Time: $(date +"%H:%M") Abu Dhabi (GMT+4)

Execute evening protocol:

1. DAY REVIEW (Facts Only)
   - What actually happened today?
   - Were Top 3 priorities completed?
   - Was 2-hour block completed?

2. COMMITMENT CHECK
   - Read lifeos/state/commitments.json
   - Which commitments due today were kept?
   - Which were not? Why?
   - Update commitment status

3. PILLAR SIGNALS
   - Quick signal from each pillar (one line each)
   - Any drift detected?

4. BIOMETRICS CAPTURE
   - Prompt for RHR before bed
   - Note if available: HRV, sleep target

5. TOMORROW PREP
   - What's the one adjustment for tomorrow?
   - Any commitments due tomorrow?
   - Any calendar items to note?

6. MICRO-REVIEW LOGGING
   - Create daily micro-review entry in lifeos/reviews/daily/$TODAY.md
   - One signal worth noticing
   - One adjustment for tomorrow

7. SHUTDOWN
   - Confirm clean shutdown
   - No 'just one more thing'
   - Protect tomorrow

Keep response concise. Close loops. No late-night catch-up recommendations.
"
