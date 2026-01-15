# LifeOS

A personal operating system for maintaining coherence across health, work, training, relationships, and long-term commitments.

**Version:** 2.0.2

## How It Works

```
┌─────────────────────────────────────────────────────────────────┐
│                                                                 │
│   BROWSER DASHBOARD          CLAUDE                             │
│   (dashboard.html)     ←→    (lifeos-*)                         │
│         │                         │                             │
│         ▼                         ▼                             │
│   ┌─────────────┐          ┌─────────────┐                      │
│   │ Sync Server │──────────│ State Files │                      │
│   │  (auto)     │          │   (JSON)    │                      │
│   └─────────────┘          └─────────────┘                      │
│         │                         │                             │
│         └─────────┬───────────────┘                             │
│                   ▼                                             │
│            ┌─────────────┐                                      │
│            │   Garmin    │                                      │
│            │   DayOne    │                                      │
│            │   Calendar  │                                      │
│            │   Gmail     │                                      │
│            └─────────────┘                                      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

**The browser dashboard is the main interface.** You edit priorities, track tasks, manage the week there. Changes sync automatically to `dashboard-live.json`.

**Claude sessions read this data + external sources** (Garmin, journal, calendar) and help you assess, plan, close loops.

## Commands

| Command | When | What happens |
|---------|------|--------------|
| `lifeos-morning` | Start of day | Syncs all data → launches Claude for morning calibration |
| `lifeos-checkin` | Anytime | Syncs Garmin → launches Claude for quick status |
| `lifeos-evening` | End of day | Syncs Garmin/journal → launches Claude for shutdown |
| `lifeos-weekly` | Sunday | Syncs everything → launches Claude for integrity review |
| `lifeos` | Deep work | Launches Claude without prompt (state your topic) |

**One command per ritual.** Each command:
1. Ensures the sync server is running
2. Pulls fresh data from integrations
3. Launches Claude with the appropriate session prompt

## Dashboard Sync

The sync server runs automatically via launchd (`com.lifeos.sync`). It starts on login and stays running.

- **Check status:** `curl http://localhost:3456/health`
- **Stop:** `launchctl stop com.lifeos.sync`
- **Start:** `launchctl start com.lifeos.sync`
- **Logs:** `lifeos/state/sync-server.log`

The browser dashboard shows a status pill: **LIVE** (green) when connected, **OFFLINE** (yellow) when not.

## File Structure

```
dashboard/
├── CLAUDE.md                   # Claude reads this first
├── dashboard.html              # Browser dashboard (main interface)
└── lifeos/
    ├── LIFEOS_SPEC.md          # Rules, pillars, invariants
    ├── LIFEOS_OPS.md           # Commands, integrations, schemas
    ├── LIFEOS_TACTICS.md       # Playbooks, daily/weekly protocols
    ├── state/
    │   ├── current-week.json   # Week state (canonical)
    │   ├── dashboard-live.json # Browser dashboard sync
    │   └── session-log.md      # Session history
    ├── integrations/
    │   ├── garmin/             # RHR, HRV, sleep, training
    │   ├── dayone/             # Journal entries
    │   ├── calendar/           # Google Calendar
    │   └── gmail/              # Email load
    └── triggers/
        ├── morning.sh          # lifeos-morning
        ├── evening.sh          # lifeos-evening
        ├── checkin.sh          # lifeos-checkin
        └── weekly.sh           # lifeos-weekly
```

## The 7 Pillars

1. **Health & Nervous System** — First-class constraint
2. **Training & Physical Capacity** — UTA 100km (May 2026)
3. **Capital, Mission & Leverage** — $50M+ target
4. **Learning & Study** — Arabic, Physics/Optics
5. **Relationships & Social** — 5 core friendships
6. **Output, Writing & Creation** — Weekly shipping
7. **Review & Integrity** — Superordinate (oversees all)

Health overrides everything. Integrity ensures coherence.

## Key Principle

> "My strength is not intensity — it's coherence."

LifeOS protects long-term trajectory against drift. Structure beats willpower.

## Getting Started

1. Open `dashboard.html` in your browser (the sync server auto-starts)
2. Run `lifeos-morning` to start your first session
3. Claude will read your state and guide you through calibration

## Where To Go Next

- Daily protocols: `lifeos/LIFEOS_TACTICS.md`
- System rules: `lifeos/LIFEOS_SPEC.md`
- Integration details: `lifeos/LIFEOS_OPS.md`
