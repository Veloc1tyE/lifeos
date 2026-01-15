# LifeOS

A personal operating system for maintaining coherence across health, work, training, relationships, and long-term commitments.

**Version:** 2.0.1
**Architecture:** 4-document system (SPEC / OPS / TACTICS / STATE)

## One-Command Workflow

Each ritual is a single command. Data syncs automatically.

| Time | Command | What it does |
|------|---------|--------------|
| **Morning** | `lifeos-morning` | Syncs Garmin + journal + calendar → runs morning calibration |
| **Anytime** | `lifeos-checkin` | Syncs Garmin → quick status check |
| **Evening** | `lifeos-evening` | Syncs Garmin + journal → runs shutdown protocol, logs training |
| **Sunday** | `lifeos-weekly` | Syncs all data → full integrity review |

That's it. One command per session.

## Quick Reference

```bash
lifeos-morning      # Morning calibration (auto-syncs data)
lifeos-checkin      # Quick status check (auto-syncs Garmin)
lifeos-evening      # Evening shutdown (auto-syncs, logs training completion)
lifeos-weekly       # Sunday integrity review (auto-syncs all sources)
lifeos              # Ad-hoc session (no auto-sync, for deep work)
```

## Optional: Browser Dashboard

If you want live-sync while editing the browser dashboard:

```bash
# Terminal 1: Keep running for browser auto-sync
lifeos-sync

# Then open dashboard.html in browser
# Status pill shows "LIVE" when connected
```

The browser dashboard is optional. The trigger commands work without it.

## What Each Command Does

### `lifeos-morning`
1. Syncs: Garmin, journal, calendar
2. Reads: current-week.json, biometrics, journals
3. Extracts: actionable items from journals
4. Classifies: day state (GREEN/YELLOW/RED)
5. Updates: current-week.json with today's plan

### `lifeos-evening`
1. Syncs: Garmin, journal
2. Checks: training completion from Garmin activities
3. Confirms: what was actually done today
4. Updates: training dailyLog, minutes, session count
5. Closes: loops, prepares tomorrow

### `lifeos-weekly`
1. Syncs: all data sources
2. Audits: training log, promises, pillars
3. Detects: patterns, drift
4. Resets: current-week.json for new week
5. Archives: week to reviews folder

## Training Tracking

Training is now tracked per-day in `current-week.json`:

```json
"p2_training": {
  "dailyLog": [
    {"day": "Mon", "date": "2026-01-12", "session": "90-min run", "minutes": 90, "confirmed": true},
    {"day": "Tue", "date": "2026-01-13", "session": "Strength", "minutes": 45, "confirmed": true},
    ...
  ],
  "minutesLogged": 135,
  "sessionsCompleted": 2
}
```

Evening shutdown pulls from Garmin and confirms with you before updating.

## Architecture

```
dashboard/
├── CLAUDE.md                   # Entry point (read first)
├── dashboard.html              # Browser dashboard (optional)
└── lifeos/
    ├── LIFEOS_SPEC.md          # Constitution, invariants (rare changes)
    ├── LIFEOS_OPS.md           # Commands, schemas (occasional changes)
    ├── LIFEOS_TACTICS.md       # Playbooks, execution (frequent changes)
    ├── state/
    │   ├── current-week.json   # Primary state file
    │   └── session-log.md      # Session history
    ├── integrations/
    │   ├── garmin/             # Garmin Connect sync
    │   ├── dayone/             # DayOne journal sync
    │   ├── calendar/           # Google Calendar sync
    │   └── gmail/              # Gmail sync
    └── triggers/
        ├── morning.sh          # Morning (auto-syncs)
        ├── evening.sh          # Evening (auto-syncs)
        ├── checkin.sh          # Check-in (auto-syncs)
        └── weekly.sh           # Weekly (auto-syncs)
```

## The 7 Pillars

1. **Health & Nervous System** — FIRST-CLASS CONSTRAINT
2. **Training & Physical Capacity** — UTA 100km (May 2026)
3. **Capital, Mission & Leverage** — $50M+ / $20M+ LOIs
4. **Learning & Study** — Arabic, Physics/Optics
5. **Relationships & Social** — 5 core friendships
6. **Output, Writing & Creation** — Weekly shipping
7. **Review & Integrity** — SUPERORDINATE

## Key Principle

> "My strength is not intensity — it's coherence."

LifeOS protects long-term trajectory against drift. Health overrides everything. Structure beats willpower.

## Where To Go Next

- Start a session: `lifeos-morning` or `lifeos`
- See rules: `lifeos/LIFEOS_SPEC.md`
- When things go wrong: `lifeos/LIFEOS_TACTICS.md`
- System evolution: `lifeos/CHANGELOG.md`
