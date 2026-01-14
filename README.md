# LifeOS

Personal Life Operating System for tracking commitments, health metrics, and maintaining coherence across 7 pillars.

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
lifeos-journal      # pull morning journal if you've made an entry
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

## File Structure

```
dashboard/
├── dashboard.html              # Main tracking dashboard
├── CLAUDE.md                   # LifeOS specification (7 pillars)
├── README.md                   # This file
└── lifeos/
    ├── state/
    │   ├── dashboard-live.json # Auto-synced from browser
    │   ├── commitments.json    # Active commitments
    │   └── session-log.md      # Session history
    ├── integrations/
    │   ├── garmin/
    │   │   ├── sync.py         # Garmin data sync
    │   │   ├── data/           # Health data JSON files
    │   │   └── .env            # Garmin credentials
    │   ├── google-credentials.json
    │   ├── token-work.json     # Google OAuth (will@aquila.earth)
    │   └── token-personal.json # Google OAuth (personal)
    ├── reviews/
    │   ├── daily/              # Daily micro-reviews
    │   └── templates/          # Review templates
    └── triggers/
        ├── morning.sh
        ├── evening.sh
        └── weekly.sh
```

## The 7 Pillars

1. **Health & Nervous System** - FIRST-CLASS CONSTRAINT
2. **Training & Physical Capacity** - UTA 100km (May 2026)
3. **Capital, Mission & Leverage** - $50M+ / $20M+ LOIs
4. **Learning & Study** - Arabic, Physics/Optics
5. **Relationships & Social** - 5 core friendships
6. **Output, Writing & Creation** - Weekly shipping
7. **Review & Integrity** - SUPERORDINATE

## Garmin Metrics Tracked

- Heart Rate (resting, 7-day avg, min/max)
- HRV (last night, weekly avg, baseline)
- Sleep (duration, deep/light/REM)
- Body Battery (current, range, charged/drained)
- Stress (avg, max, time in zones)
- Activity (steps, calories, active mins)
- Training (VO2max, load, readiness score)
- Race Predictions (5K, 10K, Half, Marathon)

## Key Principle

> "My strength is not intensity - it's coherence."

LifeOS protects long-term trajectory against drift. Health overrides everything. Structure beats willpower. One adjustment per week, not five.

## Documentation

Full specification in `CLAUDE.md` including:
- All 7 pillar definitions and protocols
- Intervention thresholds and playbooks
- Daily/weekly operating systems
- Social distribution workflows
