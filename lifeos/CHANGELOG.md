# LifeOS Changelog

All notable changes to LifeOS are documented in this file.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/).
Versioning follows [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [2.0.1] - 2026-01-14

### Changed
- Renamed `pending-notes.md` → `inbox.md` (function over status)
- Added `state/README.md` to protect against philosophy creep

### Fixed
- `weekly.sh` reference to journal path (`Journal.json` → `lifeos/integrations/dayone/data/journal.json`)
- Removed stale backlog reference in `current-week.json`

### Removed
- Temporary files: `combined_chart.js`, `SETUP-PLAN.md`, untracked data artifacts

---

## [2.0.0] - 2026-01-14

### Architecture

**BREAKING:** Complete restructure from single CLAUDE.md into 4-document architecture.

| Document | Purpose | Change Frequency |
|----------|---------|-----------------|
| `LIFEOS_SPEC.md` | Constitution, invariants, thresholds | Rare |
| `LIFEOS_OPS.md` | Commands, schemas, data flow | Occasional |
| `LIFEOS_TACTICS.md` | Playbooks, checklists, execution | Frequent |
| `state/STATE.md` | Current snapshot, facts | Daily |

### Added

#### Global Invariants
- **Shutdown Enforcement:** "No new work after shutdown" — undone items → backlog for tomorrow, never night rescue
- **Friction Budget:** 0-5 scale computed from sleep/admin/conflict/travel/injury; Maintenance Mode if ≥3
- **Integrity Requirement:** Weekly Review must produce exactly 3 artifacts or it didn't happen

#### Meta-Governance
- **System Health Meta-Signal:** COMPOUNDING / STABLE / FRAGILE — one-line long-horizon read
- **Pre-Mortem Trigger:** 2 consecutive bad weeks → mandatory 15-min pre-mortem
- **Structural Change Versioning:** Rule evolution log with format `v2026-01-XX`

#### Pillar Enhancements
- **P2 Training:** Endurance Score as PRIMARY metric with monthly targets (5800-6200 Jan → 8500-9000 May)
- **P3 Capital:** Measurable weekly cadence — 2 decision-maker meetings + 5 next-step conversions minimum
- **Day State vs Friction Score:** Clarified physiological (Day State) vs environmental (Friction) load

#### TACTICS Document (New)
- Daily/Weekly operating systems for all 7 pillars
- Identity guardrails (anti-ego, anti-overreach, anti-avoidance)
- Pre-written action packets (Capital outreach, social distribution)
- Drift detection with early/material/critical gradations and paired playbooks
- Agent authority per pillar (what LifeOS may/may not do)
- Full social distribution orchestration (content bank, API flows, reply targets)

#### Tactics Governance
- **Promotion rule:** Tactic used ≥3x successfully → consider promoting to SPEC
- **Deletion rule:** Unused 60-90 days → archive or delete
- **Constraint:** Tactics may contradict preferences, never SPEC invariants

#### Navigation Aids
- **Frequency Tags:** `[DAILY]` `[WEEKLY]` `[WHEN FRAGILE]` `[EMERGENCY]`
- **Failure Mode Index:** Quick lookup table for common failures → relevant tactic

### Changed
- CLAUDE.md reduced from ~2000 lines to ~220 lines (entry point + document map)
- Pillar content distributed to appropriate documents based on change frequency
- State files now include `frictionScore`, `systemHealth`, P3 metrics fields

### Technical
- `current-week.json` schema extended with `frictionScore`, `frictionSignals`, `systemHealth`
- P3 metrics changed from `meetingsThisWeek`/`followUpsSent` to `decisionMakerMeetings`/`nextStepConversions`
- Cross-references corrected across all documents

---

## [1.0.0] - 2026-01-13

### Added
- Initial LifeOS implementation
- 7-pillar system (Health, Training, Capital, Learning, Relationships, Output, Integrity)
- Pillar hierarchy (P7 superordinate, P1 first-class constraint)
- Dashboard auto-sync infrastructure
- Garmin, DayOne, Calendar, Gmail integrations
- Typefully and Buttondown API integration for social distribution
- Session handoff protocol
- Review templates (daily, weekly, monthly)
- Trigger scripts (morning, evening, weekly, checkin)

### Infrastructure
- `lifeos/state/` — State persistence
- `lifeos/integrations/` — External data sources
- `lifeos/reviews/templates/` — Review templates
- `lifeos/triggers/` — Automation scripts
- `lifeos/sync-server.py` — Dashboard HTTP sync

---

## Promotion Pipeline

**Tactics → SPEC lifecycle:**
> Tactics used ≥3x successfully → distilled rule promoted to SPEC (recorded as `STRUCTURAL CHANGE vYYYY-MM-DD`)

This keeps the system lean while preserving proven operational wisdom.

---

## Version History Summary

| Version | Date | Summary |
|---------|------|---------|
| 2.0.0 | 2026-01-14 | 4-document architecture, TACTICS layer, meta-governance |
| 1.0.0 | 2026-01-13 | Initial release, 7-pillar system |

---

## Upgrade Notes

### 1.x → 2.x

1. CLAUDE.md is now an entry point only — detailed content moved to SPEC/OPS/TACTICS
2. State files have new required fields (`frictionScore`, `systemHealth`)
3. Weekly Review now requires 3 explicit artifacts
4. P3 metrics renamed and minimums enforced

### Migration Checklist
- [ ] Update any scripts that parse CLAUDE.md directly
- [ ] Add `frictionScore` and `systemHealth` to state templates
- [ ] Update weekly review process to produce 3 artifacts
- [ ] Familiarize with TACTICS document for execution under stress
