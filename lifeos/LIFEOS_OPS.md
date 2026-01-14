# LifeOS Operations Manual

**Version:** 2.0
**Last Updated:** 2026-01-14
**Document Type:** Operations (changes as infrastructure evolves)

This document contains operational commands, workflows, integrations, and data flow. It should be updated whenever infrastructure changes.

For core principles and pillar doctrine, see: `LIFEOS_SPEC.md`
For current state snapshot, see: `lifeos/state/STATE.md`

---

## Quick Reference

### Shell Aliases

```bash
lifeos              # Open Claude with full LifeOS context
lifeos-sync         # Start dashboard sync server (keep running)
lifeos-garmin       # Pull latest Garmin health data
lifeos-journal      # Pull recent DayOne journal entries
lifeos-calendar     # Pull Google Calendar (today + 3 days)
lifeos-email        # Pull Gmail inbox status + priority threads
lifeos-morning      # Morning calibration ritual
lifeos-evening      # Evening shutdown ritual
lifeos-weekly       # Sunday integrity review
lifeos-checkin      # Quick status check anytime
```

### File Locations

| Data | Location |
|------|----------|
| LifeOS spec | `lifeos/LIFEOS_SPEC.md` |
| LifeOS ops | `lifeos/LIFEOS_OPS.md` |
| Current state | `lifeos/state/STATE.md` |
| Dashboard live | `lifeos/state/dashboard-live.json` |
| Week state | `lifeos/state/current-week.json` |
| Garmin data | `lifeos/integrations/garmin/data/current.json` |
| DayOne journal | `lifeos/integrations/dayone/data/current.json` |
| Google Calendar | `lifeos/integrations/calendar/data/current.json` |
| Gmail inbox | `lifeos/integrations/gmail/data/current.json` |
| Commitments | `lifeos/state/commitments.json` |
| Session log | `lifeos/state/session-log.md` |
| Patterns | `lifeos/state/patterns.json` |
| Social content | `~/age-of-wonders/private/content/` |

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                      BILLY'S WORKFLOW                        │
├─────────────────────────────────────────────────────────────┤
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │   Garmin     │───▶│  Dashboard   │───▶│   Claude     │  │
│   │   Watch      │    │  (Browser)   │    │   (LifeOS)   │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         ▼                    ▼                    ▼          │
│   ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│   │ Garmin API   │    │  HTTP Sync   │    │ State Files  │  │
│   │  (sync.py)   │    │  Server      │    │ & Reviews    │  │
│   └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                    │                    │          │
│         └────────────────────┼────────────────────┘          │
│                              ▼                               │
│                    ┌──────────────────┐                      │
│                    │  lifeos/state/   │                      │
│                    │  (JSON files)    │                      │
│                    └──────────────────┘                      │
└─────────────────────────────────────────────────────────────┘
```

---

## Daily Workflow

### 1. Start of Day

```bash
# Terminal 1: Start sync server (keep open all day)
lifeos-sync

# Terminal 2: Pull fresh data
lifeos-garmin       # Biometrics from Garmin
lifeos-journal      # Recent journal entries
lifeos-calendar     # Calendar for today + 3 days
lifeos-email        # Inbox status + priority threads

# Terminal 2: Morning calibration
lifeos-morning
```

### 2. Throughout Day

- Dashboard auto-syncs to `lifeos/state/dashboard-live.json` on every edit
- Status pill shows "LIVE" when sync server running
- Make edits in dashboard → data flows to LifeOS automatically

### 3. End of Day

```bash
lifeos-evening      # Shutdown ritual
```

**Shutdown Enforcement:** No new work after shutdown. If something is undone, it becomes a backlog loop for tomorrow — never a night rescue.

### 4. Weekly (Sunday)

```bash
lifeos-weekly       # Full integrity review
```

---

## Dashboard Auto-Sync Setup

**Start the sync server (any terminal):**
```bash
cd ~/Documents/dashboard && python3 lifeos/sync-server.py
```

Or use the shortcut:
```bash
cd ~/Documents/dashboard/lifeos && ./start-sync.sh
```

**How it works:**
- Sync server runs on `http://localhost:3456`
- Dashboard POSTs data automatically after 3 seconds of inactivity
- Status pill shows "LIVE" (green) when server is running
- Status pill shows "OFFLINE" (yellow) when server is stopped
- Click the pill to force sync or check server status
- Works in ANY browser

---

## Operational Loop (Session Start)

When Billy opens a session, execute this loop:

### 1. INGEST

Read these files in order:

```
lifeos/state/current-week.json     # Handoff, today's tasks, pillar status
lifeos/state/dashboard-live.json   # Current week tracking
lifeos/integrations/garmin/data/current.json    # Biometrics
lifeos/integrations/dayone/data/current.json    # Recent journals
```

Then check:
- Google Calendar for today + next 3 days
- Gmail inbox status (unread count, priority threads)

### 2. ASSESS

- Compare current week against goals
- Check trajectory (improving/stable/declining)
- Calculate Friction Score (see LIFEOS_SPEC.md)
- Identify the ONE primary bottleneck

### 3. REPORT

Provide coherence status:
```
STATUS: [ON MISSION | SLIGHT DRIFT | MATERIAL DRIFT]
DAY STATE: [GREEN | YELLOW | RED]
FRICTION: [0-5] — [maintenance mode if ≥3]

KEY SIGNALS:
[table of domain/signal/assessment]

PRIMARY BOTTLENECK: [single sentence]
ONE-STEP CORRECTION: [actionable, specific]
```

### 4. ACTION PACKET (if needed)

```
DOMAIN: [which goal]
TRIGGER: [when]
ACTION: [specific steps]
COMPLETION CRITERIA: [how to verify done]
ABORT IF: [safety conditions]
```

### 5. CLOSE LOOPS

- What was committed last session?
- What was completed?
- What slipped and why?

### 6. SESSION END

Update `lifeos/state/current-week.json`:
- `handoff.lastSession`: timestamp
- `handoff.openLoops`: any unfinished items
- `handoff.nextSessionContext`: what next session needs
- `handoff.blockers`: anything preventing progress
- `today.critical3`: updated status
- `today.backlog`: remaining items

---

## Integrations

### Garmin Connect

**Purpose:** RHR, HRV, Sleep, Training Load, Readiness

**Sync command:**
```bash
lifeos-garmin
# or: python3 ~/Documents/dashboard/lifeos/integrations/garmin/sync.py
```

**Data available (40+ metrics):**

| Category | Metrics |
|----------|---------|
| Heart Rate | Resting, 7-day avg, min/max |
| HRV | Last night, weekly avg, baseline |
| Sleep | Duration, deep/light/REM breakdown |
| Body Battery | Current, range, charged/drained |
| Stress | Avg, max, low/med/high minutes |
| Activity | Steps, calories, active mins, floors |
| Training | VO2max, load, status |
| Readiness | Score, HRV feedback, recovery time |

**Note on RHR/HRV:** Dashboard values are manually logged before bed using Garmin's "Health Check" feature. These are typically higher than Garmin's overnight values.

**Endurance Score:** Not available via API. Manual entry required weekly.

### DayOne Journal

**Purpose:** Subjective state, pattern detection, narrative vs reality checks

**Sync command:**
```bash
lifeos-journal              # Last 7 days (default)
lifeos-journal --days 30    # Last 30 days
lifeos-journal --all        # All entries
lifeos-journal --markdown   # Also export as .md files
```

### Google Calendar

**Purpose:** Schedule, meetings, load, available blocks

**Sync command:**
```bash
lifeos-calendar
# or: python3 ~/Documents/dashboard/lifeos/integrations/calendar/sync.py
```

**Accounts:**
- Work: will@aquila.earth
- Personal: w.jeremijenko@gmail.com

**Timezone:** Asia/Dubai (GMT+4)

### Gmail

**Purpose:** Communication load, follow-ups, priority threads

**Sync command:**
```bash
lifeos-email
# or: python3 ~/Documents/dashboard/lifeos/integrations/gmail/sync.py
```

**Load signal:**
- <20 unread: GREEN
- 20-50 unread: YELLOW
- >50 unread: RED

### Typefully (Social)

**Purpose:** X, LinkedIn posting

**Access:** MCP configured globally (typefully_* tools available)
**Social set ID:** 277101 (@BJeremijenko)

### Buttondown (Newsletter)

**Purpose:** Newsletter distribution

**Username:** ageofwonders
**API key location:** `~/age-of-wonders/private/.env`
**Archive:** buttondown.com/ageofwonders

### CRM (Google Sheets)

**Purpose:** Capital pipeline, contracts

**URL:** https://docs.google.com/spreadsheets/d/1qIKepulGJSrJ0i4GTCkku1wbO8bVGqOj4MqLIN4GHuM/

---

## Social Distribution

### Daily Social Loop

**Command:** "Run the daily social loop"

**Flow:**
1. Read content bank: `~/age-of-wonders/private/content/one-liners.md`
2. Select 1-2 unused items (`[ ]`)
3. Present draft for approval
4. Post via Typefully MCP (social set 277101)
5. Mark items as `[x]` in content bank
6. Log to: `~/age-of-wonders/private/content/posting-log.md`

### Essay Launch Protocol

**Command:** "Launch [essay name]"

**Flow:**
1. Read essay from: `~/age-of-wonders/src/content/essays/[slug].mdx`
2. Draft: Newsletter (Buttondown), X post, LinkedIn post
3. Execute on approval
4. Log to posting-log.md

### Social Metrics Check

**Command:** "Check social metrics"

**Reports:**
- Days with posts this week
- Content bank remaining
- Newsletter subscriber count

---

## State Files Schema

### current-week.json

```json
{
  "week": 3,
  "weekStart": "2026-01-12",
  "timezone": "Asia/Dubai",
  "lastUpdated": "ISO timestamp",

  "pillarStatus": {
    "p1_health": { "status": "GREEN|YELLOW|RED", "signals": [], "lastAssessed": "" },
    "p2_training": { "status": "", "minutesLogged": 0, "enduranceScore": {}, ... },
    "p3_capital": { "status": "", "decisionMakerMeetings": 0, "nextStepConversions": 0, "weeklyMinimum": {"meetings": 2, "conversions": 5}, ... },
    "p4_learning": { "status": "", "arabicDays": 0, "physicsDays": 0, ... },
    "p5_relationships": { "status": "", "coreTouched": 0, ... },
    "p6_output": { "status": "", "shippedThisWeek": false, ... },
    "p7_integrity": { "status": "", "reviewsCompleted": 0, ... }
  },

  "today": {
    "date": "YYYY-MM-DD",
    "dayState": "GREEN|YELLOW|RED",
    "frictionScore": 0,
    "deepWork": { "focus": "", "area": "", "completed": false },
    "critical3": [{ "task": "", "status": "pending|done|blocked" }],
    "backlog": [{ "task": "", "status": "open|done|deferred" }]
  },

  "biometrics": {
    "rhr": [null, ...],
    "hrv": [null, ...],
    "sleepHours": [null, ...],
    "bodyBattery": [null, ...]
  },

  "handoff": {
    "lastSession": "",
    "sessionSummary": [],
    "openLoops": [],
    "pendingActions": { "critical": [], "backlog": [] },
    "nextSessionContext": "",
    "blockers": []
  }
}
```

---

## Review Templates

### Daily Micro-Review

Location: `lifeos/reviews/templates/daily-micro.md`

Capture:
- What actually happened (facts only)
- One signal worth noticing
- One adjustment for tomorrow

### Weekly Integrity Review

Location: `lifeos/reviews/templates/weekly-integrity.md`

**Must produce three artifacts:**
1. Kept promises list
2. Broken promises list (with disposition)
3. ONE structural adjustment (as rule)

### Monthly Pattern Review

Location: `lifeos/reviews/templates/monthly-pattern.md`

Questions:
- What is compounding?
- What is stalling?
- What keeps breaking despite effort?

---

## Trigger Scripts

Location: `lifeos/triggers/`

| Script | Purpose |
|--------|---------|
| `morning.sh` | Morning calibration |
| `evening.sh` | Evening shutdown |
| `weekly.sh` | Sunday integrity review |
| `checkin.sh` | Quick status check |
| `crontab.txt` | Automation config |

**Quick commands:**
```bash
cd ~/Documents/dashboard && ./lifeos/triggers/morning.sh
cd ~/Documents/dashboard && ./lifeos/triggers/evening.sh
cd ~/Documents/dashboard && ./lifeos/triggers/checkin.sh
cd ~/Documents/dashboard && ./lifeos/triggers/weekly.sh
```

---

## Action Authority

### LifeOS May PREPARE (not execute without approval):

- Calendar adjustments for sleep protection
- Emails to reduce load
- Scheduling medical/psych/recovery appointments
- Admin tasks that reduce friction
- Draft social posts
- Draft newsletter content
- CRM updates

### LifeOS May Execute Immediately:

- State file updates
- Session log entries
- Dashboard data reads
- Biometric data pulls

### Requires Explicit "Approve":

- Sending any external communication
- Publishing any content
- Calendar modifications
- Any action affecting others

### Requires "Approve High-Risk":

- Anything touching Aquila formally
- Financial commitments
- Legal implications

---

## Adding New Aliases

```bash
echo 'alias lifeos-calendar="python3 ~/Documents/dashboard/lifeos/integrations/calendar/sync.py"' >> ~/.zshrc
echo 'alias lifeos-email="python3 ~/Documents/dashboard/lifeos/integrations/gmail/sync.py"' >> ~/.zshrc
source ~/.zshrc
```

---

*Operations evolve. Principles persist.*
