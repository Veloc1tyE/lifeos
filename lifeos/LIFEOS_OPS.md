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
lifeos-beeper       # Pull Beeper chats (WhatsApp, etc.)
```

### File Locations

| Data | Location |
|------|----------|
| LifeOS spec | `lifeos/LIFEOS_SPEC.md` |
| LifeOS ops | `lifeos/LIFEOS_OPS.md` |
| Current state | `lifeos/state/STATE.md` |
| Dashboard live | `lifeos/state/dashboard-live.json` |
| Week state | `lifeos/state/current-week.json` |
| Artifacts (temp) | `lifeos/artifacts/` |
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

# Terminal 2: Morning calibration (auto-syncs data first)
lifeos-morning
```

**Note:** The trigger scripts (morning, evening, checkin, weekly) now automatically pull fresh data before launching Claude. Manual sync commands are only needed for ad-hoc data checks.

**Morning Data Requirement:** LifeOS must ALWAYS read fresh Garmin biometrics (`garmin-YYYY-MM-DD.json`) and DayOne journal entries (`current.json`) during morning calibration. Dashboard data alone is insufficient — Garmin provides overnight recovery metrics (RHR, HRV, sleep score, Training Readiness, Body Battery) and journals contain actionable items to extract.

### 2. Throughout Day

- Dashboard auto-syncs to `lifeos/state/dashboard-live.json` on every edit
- Status pill shows "LIVE" when sync server running
- Make edits in dashboard → data flows to LifeOS automatically

### 3. End of Day

```bash
# Refresh data before evening protocol
lifeos-garmin       # Fresh biometrics (recovery, body battery)
lifeos-journal      # Today's journal entries

# Then run shutdown
lifeos-evening
```

**Evening Data Refresh:** Always pull fresh Garmin and journal data before evening shutdown. Body battery and recovery metrics change throughout the day; journal entries contain actionable items that need extraction.

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

### 1b. EXTRACT FROM JOURNALS

Scan journal entries for actionable items. Extract and categorize:

| Type | Examples | Action |
|------|----------|--------|
| **Tasks mentioned** | "need to...", "should...", "have to..." | Add to backlog if not already tracked |
| **People to contact** | "reach out to X", "follow up with Y" | Add to capital pipeline or relationship list |
| **Open loops** | "left my key at...", "waiting for..." | Add to handoff.openLoops |
| **Insights for pillars** | Training observations, health signals | Note in pillar status |
| **Values/identity notes** | Reflections, commitments | Flag for weekly review |

**Rule:** Journal items should not stay buried in entries. Surface them into the operational system where they can be tracked and closed.

**Format for surfacing:**
```
JOURNAL EXTRACTION (date range):
- TASKS: [list new items to add to backlog]
- CONTACTS: [people mentioned to reach out to]
- OPEN LOOPS: [things waiting/pending]
- FLAGS: [anything requiring attention]
```

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

**Note on Training Load "Above Targets":** The Garmin Forerunner 996 automatically increases optimal training load range over time as fitness improves. During intentional ramp-up phases, `load_feedback: ABOVE_TARGETS` is expected and not a concern — it reflects the device adapting to higher capacity. Treat as informational, not a warning requiring intervention.

**Progressive Loading Pattern:** Billy increases intensity minutes and floors progressively throughout each week. Early-week totals are not representative of weekly output — expect back-loaded volume toward Thu-Sat.

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

**Account features:**
- X Premium enabled (no character limits)
- Use longer-form posts with depth

**Optimal posting times (AU/US audience):**
- **Primary window:** 21:00-23:00 UTC
  - Australia: 8-10am AEDT (morning engagement)
  - US East: 4-6pm EST (evening wind-down)
  - US West: 1-3pm PST (afternoon)
- Always use `publish_at: "next-free-slot"` or specific datetime
- **Never** publish multiple posts simultaneously

**Scheduling rules:**
- Schedule posts, don't publish immediately
- Space posts apart for natural cadence
- One post at a time looks organic

### Buttondown (Newsletter)

**Purpose:** Newsletter distribution

**Username:** ageofwonders
**API key location:** `~/age-of-wonders/private/.env`
**Archive:** buttondown.com/ageofwonders

### Beeper (WhatsApp, Telegram, etc.)

**Purpose:** Business conversations across messaging platforms

**Sync command:**
```bash
lifeos-beeper
# or: python3 ~/Documents/dashboard/lifeos/integrations/beeper/sync.py
```

**Setup required:**
1. Open Beeper Desktop
2. Go to Settings → Developers
3. Enable the Desktop API (runs on localhost:23373)

**Data available:**
- All chats across platforms
- Business-related conversations (auto-filtered by keywords)
- UAE-specific message search
- Contact extraction

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

## Deep Work Sessions

### Overview

Deep work sessions are focused blocks for substantial work on a single pillar. They use a temporary artifacts workflow to process external data (CRM exports, spreadsheets, etc.) without polluting the permanent state.

### Artifacts Workflow

**Location:** `lifeos/artifacts/`

**Pattern: Import → Work → Export → Delete**

1. **IMPORT** — Copy/paste data from external systems into artifacts folder
   - Name files descriptively: `crm-pipeline-2026-01-14.md`
   - Include source and date in filename

2. **WORK** — Process with LifeOS
   - Triage, analyze, update
   - Generate action items
   - Build plans

3. **EXPORT** — Push changes back to external systems
   - Update CRM, spreadsheets, etc.
   - Confirm changes applied

4. **DELETE** — Remove artifact file
   - Artifacts are temporary working files
   - Don't accumulate stale data

**Rules:**
- Files in artifacts/ are git-ignored (not version controlled)
- Delete artifacts at end of each session
- Never store credentials or sensitive auth tokens here
- One artifact per deep work topic

### Session Types

| Type | Focus | Typical Artifacts |
|------|-------|-------------------|
| Capital motion | CRM, pipeline, outreach | CRM export, lead lists |
| Technical thinking | Architecture, design | Diagrams, specs |
| Writing/output | Essays, content | Drafts, outlines |
| Strategic | Planning, reviews | Analysis docs |

### Session Protocol

1. **Declare focus** — State the single topic
2. **Set duration** — Typical: 1-2 hours
3. **Import artifacts** — Bring in external data if needed
4. **Execute** — Stay on topic; capture other-pillar insights for handoff
5. **Export** — Push changes to external systems
6. **Clean up** — Delete artifacts, update handoff

**Distraction rule:** If something surfaces for another pillar, note it in handoff and return to focus. Don't context-switch.

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
    "p2_training": {
      "status": "",
      "minutesLogged": 0,
      "sessionsCompleted": 0,
      "dailyLog": [
        {"day": "Sun", "date": "YYYY-MM-DD", "session": null, "minutes": null, "confirmed": false},
        {"day": "Mon", "date": "YYYY-MM-DD", "session": "description", "minutes": 90, "confirmed": true},
        // ... one entry per day of week
      ],
      "enduranceScore": {},
      ...
    },
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
