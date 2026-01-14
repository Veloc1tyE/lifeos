# LifeOS Complete Setup Plan

**Goal:** Set up once, compound forever.

## Overall Status: 90% COMPLETE

| Phase | Status |
|-------|--------|
| 1. Core Infrastructure | ✅ Complete |
| 2. Dashboard Sync Server | ✅ Complete |
| 3. Google Cloud Project | ✅ Complete |
| 4. Google API Auth | ✅ Complete |
| 5. Garmin Integration | ✅ Complete |
| 6. Social Distribution | ✅ Complete |
| 7. Journal Sync | ✅ Complete |
| 8. Shell Aliases | ✅ Complete |
| 9. First Full Test | ✅ Complete |
| 10. Documentation | ✅ Complete |

---

## Phase 1: Core Infrastructure (Already Done)

- [x] CLAUDE.md with 7 pillars defined
- [x] lifeos/ directory structure created
- [x] State persistence files (commitments, patterns, session log)
- [x] Review templates (daily, weekly, monthly)
- [x] Trigger scripts (morning, evening, weekly, checkin)
- [x] Dashboard auto-sync feature added

---

## Phase 2: Dashboard Sync Server Setup (COMPLETE)

**Status:** Done

### What's Set Up:
- [x] HTTP sync server at `lifeos/sync-server.py`
- [x] Runs on localhost:3456
- [x] Dashboard auto-syncs on every edit
- [x] Works with Brave browser (no File System Access API needed)

### Usage:
```bash
# Start the sync server (keep terminal open)
cd ~/Documents/dashboard && python3 lifeos/sync-server.py
```

---

## Phase 3: Google Cloud Project Setup (COMPLETE)

**Status:** Done

### What's Set Up:
- [x] Project: `lifeos-billy` created
- [x] APIs enabled: Calendar, Sheets, Gmail
- [x] OAuth credentials created (Desktop app)
- [x] Test users added: will@aquila.earth, w.jeremijenko@gmail.com
- [x] Credentials saved to `lifeos/integrations/google-credentials.json`

---

## Phase 4: Google API Authentication (COMPLETE)

**Status:** Done

### What's Set Up:
- [x] Dependencies installed (google-auth-oauthlib, google-api-python-client)
- [x] Auth script at `lifeos/integrations/google-auth-setup.py`
- [x] Work account authenticated: `token-work.json`
- [x] Personal account authenticated: `token-personal.json`

### Available Scopes:
- `https://www.googleapis.com/auth/calendar.readonly`
- `https://www.googleapis.com/auth/spreadsheets.readonly`
- `https://www.googleapis.com/auth/gmail.readonly`

---

## Phase 5: Garmin Integration (COMPLETE)

**Status:** Done

### What's Set Up:
- [x] Garmin Connect API via `garminconnect` Python library
- [x] Credentials stored in `lifeos/integrations/garmin/.env`
- [x] Full sync script at `lifeos/integrations/garmin/sync.py`

### Data Collected:
- Heart Rate (resting, max, min)
- HRV (last night, weekly avg, baseline)
- Sleep (duration, deep/light/REM, score)
- Stress (avg, max)
- Body Battery (latest, high, low)
- Activity (steps, distance, calories, active minutes)
- Training Status (load, status, VO2max)
- Training Readiness (score, level, recovery time)
- Race Predictions (5K, 10K, Half, Marathon)
- Respiration (waking avg, sleeping avg)
- SpO2 (avg, lowest)
- Recent Activities (last 5 with details)

### Usage:
```bash
# Today's data
python3 lifeos/integrations/garmin/sync.py

# Last 7 days
python3 lifeos/integrations/garmin/sync.py --days 7

# Specific date
python3 lifeos/integrations/garmin/sync.py --date 2026-01-10
```

### Output Location:
- Current: `lifeos/integrations/garmin/data/current.json`
- Historical: `lifeos/integrations/garmin/data/garmin-YYYY-MM-DD.json`

---

## Phase 6: Social Distribution Setup (COMPLETE)

**Status:** Done

### What's Set Up:
- [x] Typefully API key configured
- [x] Buttondown API key configured
- [x] Content bank at `~/age-of-wonders/private/content/`
  - `one-liners.md` (5KB of content)
  - `posting-log.md` (tracking)

### API Locations:
- Keys: `~/age-of-wonders/private/.env`

---

## Phase 7: Journal Sync Setup (OPTIONAL)

**Status:** Pending - Manual step required

### When Ready:
1. [ ] In DayOne app, go to File → Export → JSON
2. [ ] Save to: `~/Documents/dashboard/Journal.json`
3. [ ] Set calendar reminder: "Export DayOne" every Sunday

**Note:** This is optional and can be done anytime. DayOne CLI tools can automate this later if needed.

---

## Phase 8: Shell Aliases & Shortcuts (COMPLETE)

**Status:** Done

### Aliases Added to ~/.zshrc:
- `lifeos` - Open Claude in dashboard directory
- `lifeos-morning` - Run morning trigger
- `lifeos-evening` - Run evening trigger
- `lifeos-weekly` - Run weekly review
- `lifeos-checkin` - Quick check-in
- `lifeos-sync` - Start sync server
- `lifeos-garmin` - Sync Garmin data

### Activate Now:
```bash
source ~/.zshrc
```

---

## Phase 9: First Full Test

**Status:** Ready to test

### After sourcing ~/.zshrc, test:

```bash
# 1. Start sync server (in one terminal)
lifeos-sync

# 2. Sync Garmin data
lifeos-garmin

# 3. Test morning flow
lifeos-morning

# 4. Test evening flow
lifeos-evening

# 5. Open dashboard and verify LifeOS: LIVE status
open ~/Documents/dashboard/dashboard.html
```

---

## Phase 10: Documentation & Backup (COMPLETE)

**Status:** Done

### What's Set Up:
- [x] Git repo initialized
- [x] `.gitignore` created with proper exclusions:
  - Credentials and tokens
  - Personal health data (Garmin)
  - Live state files
  - Python cache, OS files

### Recommended:
- [ ] Set monthly calendar reminder: "Backup LifeOS data"
- [ ] Optional: Push to private GitHub repo for backup

---

## Phase 11: Ongoing Maintenance

### Daily
- [ ] Morning trigger (or manual check-in)
- [ ] Evening shutdown
- [ ] Dashboard auto-syncs

### Weekly (Sunday)
- [ ] Weekly integrity review
- [ ] Export DayOne journal
- [ ] Review and update commitments

### Monthly
- [ ] Monthly pattern review
- [ ] Backup data
- [ ] Review system friction, adjust

---

## Quick Reference: What's Where

| Component | Location |
|-----------|----------|
| LifeOS spec | `~/Documents/dashboard/CLAUDE.md` |
| Dashboard | `~/Documents/dashboard/dashboard.html` |
| Live sync | `~/Documents/dashboard/lifeos/state/dashboard-live.json` |
| Commitments | `~/Documents/dashboard/lifeos/state/commitments.json` |
| Session log | `~/Documents/dashboard/lifeos/state/session-log.md` |
| Triggers | `~/Documents/dashboard/lifeos/triggers/` |
| Reviews | `~/Documents/dashboard/lifeos/reviews/` |
| Google creds | `~/Documents/dashboard/lifeos/integrations/google-credentials.json` |
| Garmin data | `~/Documents/dashboard/lifeos/integrations/garmin/data/` |
| Social content | `~/age-of-wonders/private/content/` |

---

## What's Left

1. **Run `source ~/.zshrc`** to activate the new aliases
2. **Test the system** with the commands in Phase 9

---

## Daily Operations

```bash
# Start of day
lifeos-sync         # Terminal 1 - keep running
lifeos-garmin       # Sync latest health data
lifeos-morning      # Morning calibration

# End of day
lifeos-evening      # Evening shutdown

# Any time
lifeos              # Open Claude with full LifeOS context
lifeos-checkin      # Quick status check
```
