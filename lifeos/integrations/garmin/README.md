# Garmin Connect Integration

## Overview

Pull biometric data from Garmin Connect to inform Pillar 1 (Health) and Pillar 2 (Training) assessments.

## Data Available

| Metric | Use | Pillar |
|--------|-----|--------|
| Resting Heart Rate | Recovery signal, trend tracking | P1 |
| Heart Rate Variability | Nervous system state, stress signal | P1 |
| Sleep Duration | Primary health metric | P1 |
| Sleep Score | Sleep quality assessment | P1 |
| Training Load | Load vs capacity | P2 |
| Intensity Minutes | Weekly training volume | P2 |
| Steps | Activity baseline | P1/P2 |
| Body Battery | Energy state proxy | P1 |
| Stress Level | Nervous system signal | P1 |

## Integration Options

### Option 1: Manual Daily Export (Current)

1. Open Garmin Connect app or web
2. Note key metrics in dashboard
3. Simple but requires daily discipline

### Option 2: Garmin Connect API (Automated)

**Setup Required:**
1. Create Garmin Developer account
2. Register application
3. Obtain OAuth credentials
4. Store in `lifeos/integrations/garmin/.env`

**API Endpoints:**
- `/wellness-api/rest/dailies` - Daily summary
- `/wellness-api/rest/epochs` - Time-series data
- `/wellness-api/rest/sleeps` - Sleep data
- `/wellness-api/rest/activities` - Activity data

**Note:** Garmin's API requires OAuth 1.0a which is complex. Consider Option 3.

### Option 3: Third-Party Sync (Recommended)

Use a service that already has Garmin integration:

**Recommended: Export via Apple Health**
1. Garmin Connect syncs to Apple Health
2. Export Apple Health data periodically
3. Parse the XML export

**Alternative: Intervals.icu**
1. Connect Garmin to Intervals.icu (free)
2. Use Intervals.icu API (simpler auth)
3. Pull training metrics

**Alternative: Strava**
1. Connect Garmin to Strava
2. Use Strava API
3. Pull activity data

## Daily Sync Script (Template)

```bash
#!/bin/bash
# lifeos/integrations/garmin/sync.sh
# Placeholder for automated sync

# Manual mode: Prompt user for values
echo "Enter today's Garmin metrics:"
read -p "RHR: " rhr
read -p "HRV: " hrv
read -p "Sleep hours: " sleep_hours
read -p "Sleep score: " sleep_score
read -p "Training load: " training_load

# Write to state
# (implementation depends on chosen approach)
```

## Recommended Approach

**Phase 1 (Now):** Manual entry into dashboard
- Already working
- Builds habit of checking metrics
- Zero setup required

**Phase 2 (Later):** Apple Health export
- Weekly export from iPhone
- Parse for trend data
- Semi-automated

**Phase 3 (Optional):** Full API integration
- Requires developer setup
- Best for complete automation
- Consider if manual becomes friction

## File Structure

```
lifeos/integrations/garmin/
├── README.md          # This file
├── .env               # API credentials (if using)
├── sync.sh            # Sync script
└── data/              # Cached Garmin data
    └── .gitignore     # Exclude data from git
```

## Key Metrics for LifeOS

**Daily (Pillar 1):**
- RHR before bed
- HRV morning
- Sleep duration
- Sleep score

**Weekly (Pillar 2):**
- Total intensity minutes
- Training load trend
- Recovery time

**Intervention Triggers:**
- RHR >70 → Recovery day
- HRV <40 → Reduce load
- Sleep <6 hrs for 2+ days → P1 override
