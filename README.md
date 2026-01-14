# LifeOS

Personal Life Operating System for tracking commitments, health metrics, and maintaining coherence across 7 pillars.

**Version:** 2.0.0
**Architecture:** 4-document system (SPEC / OPS / TACTICS / STATE)

## Quick Start

```bash
# 1. Activate shell aliases (one-time after setup)
source ~/.zshrc

# 2. Start sync server (keep running in background terminal)
lifeos-sync

# 3. Pull latest Garmin data
lifeos-garmin

# 4. Open dashboard
open dashboard.html

# 5. Start LifeOS session
lifeos
```

## Daily Workflow

### Morning
```bash
lifeos-sync         # Terminal 1 - leave running all day
lifeos-garmin       # Pull overnight biometrics
lifeos-journal      # Pull morning journal if you've made an entry
lifeos              # → "Morning calibration"
```

### Throughout Day
- Keep `dashboard.html` open in browser
- Edit as you go - auto-syncs when server running
- Status pill shows "LIVE" (green) when connected

### Evening
```bash
lifeos              # → "Evening shutdown"
```

### Sunday (Required)
```bash
lifeos              # → "Weekly review"
```

## Shell Aliases

| Alias | Purpose |
|-------|---------|
| `lifeos` | Open Claude with full LifeOS context |
| `lifeos-sync` | Start dashboard sync server |
| `lifeos-garmin` | Sync Garmin health data |
| `lifeos-journal` | Sync DayOne journal entries |
| `lifeos-morning` | Morning calibration |
| `lifeos-evening` | Evening shutdown |
| `lifeos-weekly` | Sunday integrity review |
| `lifeos-checkin` | Quick status check |

## Architecture (v2.0)

LifeOS uses a 4-document architecture optimized for change frequency:

```
dashboard/
├── CLAUDE.md                   # Entry point + quickstart (read first)
├── dashboard.html              # Main tracking dashboard
├── README.md                   # This file
└── lifeos/
    ├── LIFEOS_SPEC.md          # Constitution, invariants, thresholds (rare changes)
    ├── LIFEOS_OPS.md           # Commands, schemas, integrations (occasional changes)
    ├── LIFEOS_TACTICS.md       # Playbooks, checklists, execution (frequent changes)
    ├── CHANGELOG.md            # Version history + evolution log
    ├── SETUP-PLAN.md           # Bootstrap + recovery guide
    ├── state/
    │   ├── STATE.md            # Current snapshot (human-readable)
    │   ├── current-week.json   # Primary state file (JSON)
    │   ├── dashboard-live.json # Auto-synced from browser
    │   ├── commitments.json    # Active commitments
    │   └── session-log.md      # Session history
    ├── integrations/
    │   ├── garmin/             # Garmin Connect sync
    │   ├── dayone/             # DayOne journal sync
    │   ├── calendar/           # Google Calendar sync
    │   └── gmail/              # Gmail sync
    ├── reviews/
    │   └── templates/          # Review templates (daily, weekly, monthly)
    └── triggers/
        ├── morning.sh          # Morning calibration
        ├── evening.sh          # Evening shutdown
        └── weekly.sh           # Weekly review
```

## Document Hierarchy

| Document | Purpose | Change Frequency |
|----------|---------|------------------|
| `LIFEOS_SPEC.md` | Constitution, invariants, pillar definitions | Rare |
| `LIFEOS_OPS.md` | Commands, workflows, data schemas | Occasional |
| `LIFEOS_TACTICS.md` | Daily playbooks, failure responses, execution | Frequent |
| `state/STATE.md` | Current snapshot, facts only | Daily |

## The 7 Pillars

1. **Health & Nervous System** - FIRST-CLASS CONSTRAINT
2. **Training & Physical Capacity** - UTA 100km (May 2026)
3. **Capital, Mission & Leverage** - $50M+ / $20M+ LOIs
4. **Learning & Study** - Arabic, Physics/Optics
5. **Relationships & Social** - 5 core friendships
6. **Output, Writing & Creation** - Weekly shipping
7. **Review & Integrity** - SUPERORDINATE

## Global Invariants

Three non-negotiable rules that override everything:

1. **Shutdown Enforcement** - No new work after shutdown
2. **Friction Budget** - If friction score ≥3, operate in Maintenance Mode
3. **Integrity Requirement** - Weekly Review must produce 3 artifacts

## Garmin Metrics Tracked

- Heart Rate (resting, 7-day avg, min/max)
- HRV (last night, weekly avg, baseline)
- Sleep (duration, deep/light/REM)
- Body Battery (current, range, charged/drained)
- Stress (avg, max, time in zones)
- Activity (steps, calories, active mins)
- Training (VO2max, load, readiness score)
- **Endurance Score** (primary UTA 100 metric)
- Race Predictions (5K, 10K, Half, Marathon)

## Key Principle

> "My strength is not intensity - it's coherence."

LifeOS protects long-term trajectory against drift. Health overrides everything. Structure beats willpower. One adjustment per week, not five.

## Contributing to LifeOS

Changes follow semantic versioning and are logged in `CHANGELOG.md`:

- **SPEC changes:** Rare, require proven benefit (tactics used 3+ times)
- **OPS changes:** When infrastructure evolves
- **TACTICS changes:** Frequent, low friction
- **STATE changes:** Daily, facts only

## License

Private repository. Personal use only.
