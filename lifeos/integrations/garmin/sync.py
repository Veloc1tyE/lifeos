#!/usr/bin/env python3
"""
Garmin Connect Data Sync for LifeOS
Pulls health, sleep, and activity data.

Usage:
    python3 sync.py              # Today's data
    python3 sync.py --days 7     # Last 7 days
    python3 sync.py --date 2026-01-10  # Specific date
"""

import os
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path
from garminconnect import Garmin

# Load credentials
ENV_FILE = Path(__file__).parent / '.env'
DATA_DIR = Path(__file__).parent / 'data'
DATA_DIR.mkdir(exist_ok=True)

def load_credentials():
    """Load Garmin credentials from .env file."""
    creds = {}
    if ENV_FILE.exists():
        with open(ENV_FILE) as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    key, value = line.split('=', 1)
                    creds[key.strip()] = value.strip()
    return creds

def get_client():
    """Initialize and authenticate Garmin client."""
    creds = load_credentials()
    email = creds.get('GARMIN_EMAIL')
    password = creds.get('GARMIN_PASSWORD')

    if not email or not password or password == 'YOUR_PASSWORD_HERE':
        print("ERROR: Please set your Garmin password in:")
        print(f"  {ENV_FILE}")
        return None

    client = Garmin(email, password)

    print("Logging in to Garmin Connect...")
    client.login()
    print("Logged in successfully.")

    return client

def get_health_data(client, date):
    """Get all health metrics for a specific date."""
    date_str = date.strftime('%Y-%m-%d')

    data = {
        'date': date_str,
        'fetched_at': datetime.now().isoformat(),
    }

    # Heart Rate
    try:
        hr_data = client.get_heart_rates(date_str)
        data['heart_rate'] = {
            'resting': hr_data.get('restingHeartRate'),
            'resting_7day_avg': hr_data.get('lastSevenDaysAvgRestingHeartRate'),
            'max': hr_data.get('maxHeartRate'),
            'min': hr_data.get('minHeartRate'),
        }
    except Exception as e:
        data['heart_rate'] = {'error': str(e)}

    # HRV
    try:
        hrv_data = client.get_hrv_data(date_str)
        if hrv_data and 'hrvSummary' in hrv_data:
            summary = hrv_data['hrvSummary']
            data['hrv'] = {
                'weekly_avg': summary.get('weeklyAvg'),
                'last_night': summary.get('lastNightAvg'),
                'baseline': summary.get('baseline', {}).get('balancedLow'),
            }
        else:
            data['hrv'] = hrv_data
    except Exception as e:
        data['hrv'] = {'error': str(e)}

    # Sleep
    try:
        sleep_data = client.get_sleep_data(date_str)
        if sleep_data and 'dailySleepDTO' in sleep_data:
            sleep = sleep_data['dailySleepDTO']
            data['sleep'] = {
                'duration_seconds': sleep.get('sleepTimeSeconds'),
                'duration_hours': round(sleep.get('sleepTimeSeconds', 0) / 3600, 2),
                'deep_seconds': sleep.get('deepSleepSeconds'),
                'light_seconds': sleep.get('lightSleepSeconds'),
                'rem_seconds': sleep.get('remSleepSeconds'),
                'awake_seconds': sleep.get('awakeSleepSeconds'),
                'score': sleep_data.get('sleepScores', {}).get('overall', {}).get('value'),
            }
        else:
            data['sleep'] = sleep_data
    except Exception as e:
        data['sleep'] = {'error': str(e)}

    # Stress (from stats endpoint which has more detail)
    try:
        stats = client.get_stats(date_str)
        data['stress'] = {
            'avg': stats.get('averageStressLevel'),
            'max': stats.get('maxStressLevel'),
            'rest_percent': stats.get('restStressPercentage'),
            'activity_percent': stats.get('activityStressPercentage'),
            'low_minutes': (stats.get('lowStressDuration', 0) or 0) // 60,
            'medium_minutes': (stats.get('mediumStressDuration', 0) or 0) // 60,
            'high_minutes': (stats.get('highStressDuration', 0) or 0) // 60,
        }
    except Exception as e:
        data['stress'] = {'error': str(e)}

    # Body Battery
    try:
        bb_data = client.get_body_battery(date_str)
        if bb_data and len(bb_data) > 0:
            day_data = bb_data[0]
            values = day_data.get('bodyBatteryValuesArray', [])
            # Values are [timestamp, level] pairs
            levels = [v[1] for v in values if len(v) > 1 and v[1] is not None]
            data['body_battery'] = {
                'latest': levels[-1] if levels else None,
                'high': max(levels) if levels else None,
                'low': min(levels) if levels else None,
                'charged': day_data.get('charged'),
                'drained': day_data.get('drained'),
            }
    except Exception as e:
        data['body_battery'] = {'error': str(e)}

    # Steps & Activity
    try:
        stats = client.get_stats(date_str)
        highly_active = stats.get('highlyActiveSeconds', 0) or 0
        active = stats.get('activeSeconds', 0) or 0
        data['activity'] = {
            'steps': stats.get('totalSteps'),
            'step_goal': stats.get('dailyStepGoal'),
            'distance_meters': stats.get('totalDistanceMeters'),
            'active_minutes': (highly_active + active) // 60,
            'moderate_intensity_minutes': stats.get('moderateIntensityMinutes'),
            'vigorous_intensity_minutes': stats.get('vigorousIntensityMinutes'),
            'calories_total': stats.get('totalKilocalories'),
            'calories_active': stats.get('activeKilocalories'),
            'calories_bmr': stats.get('bmrKilocalories'),
            'intensity_minutes_goal': stats.get('intensityMinutesGoal'),
            'floors_climbed': stats.get('floorsAscended'),
            'floors_goal': stats.get('userFloorsAscendedGoal'),
            'sedentary_minutes': (stats.get('sedentarySeconds', 0) or 0) // 60,
        }
    except Exception as e:
        data['activity'] = {'error': str(e)}

    # Training Status
    try:
        training = client.get_training_status(date_str)
        if training:
            vo2max_data = training.get('mostRecentVO2Max', {}).get('generic', {})
            load_balance = training.get('mostRecentTrainingLoadBalance', {})
            metrics = load_balance.get('metricsTrainingLoadBalanceDTOMap', {})
            # Get first device's metrics
            device_metrics = list(metrics.values())[0] if metrics else {}

            data['training'] = {
                'vo2max': vo2max_data.get('vo2MaxValue'),
                'vo2max_precise': vo2max_data.get('vo2MaxPreciseValue'),
                'fitness_age': vo2max_data.get('fitnessAge'),
                'load_aerobic_low': device_metrics.get('monthlyLoadAerobicLow'),
                'load_aerobic_high': device_metrics.get('monthlyLoadAerobicHigh'),
                'load_anaerobic': device_metrics.get('monthlyLoadAnaerobic'),
                'load_feedback': device_metrics.get('trainingBalanceFeedbackPhrase'),
            }

            # Heat/Altitude acclimation
            acclim = training.get('mostRecentVO2Max', {}).get('heatAltitudeAcclimation', {})
            if acclim:
                data['acclimation'] = {
                    'heat_percent': acclim.get('heatAcclimationPercentage'),
                    'heat_trend': acclim.get('heatTrend'),
                    'altitude_percent': acclim.get('altitudeAcclimation'),
                }
    except Exception as e:
        data['training'] = {'error': str(e)}

    # Training Readiness
    try:
        readiness = client.get_training_readiness(date_str)
        if readiness:
            r = readiness[0] if isinstance(readiness, list) else readiness
            if isinstance(r, dict):
                data['training_readiness'] = {
                    'score': r.get('score'),
                    'level': r.get('level'),
                    'recovery_time_minutes': r.get('recoveryTime'),
                    'sleep_score': r.get('sleepScore'),
                    'sleep_score_feedback': r.get('sleepScoreFactorFeedback'),
                    'hrv_weekly_avg': r.get('hrvWeeklyAverage'),
                    'hrv_feedback': r.get('hrvFactorFeedback'),
                    'stress_feedback': r.get('stressHistoryFactorFeedback'),
                    'sleep_history_feedback': r.get('sleepHistoryFactorFeedback'),
                    'acute_load': r.get('acuteLoad'),
                }
    except Exception as e:
        data['training_readiness'] = {'error': str(e)}

    # Race Predictions
    try:
        predictions = client.get_race_predictions()
        if predictions:
            data['race_predictions'] = {
                '5k_seconds': predictions.get('time5K'),
                '10k_seconds': predictions.get('time10K'),
                'half_marathon_seconds': predictions.get('timeHalfMarathon'),
                'marathon_seconds': predictions.get('timeMarathon'),
            }
    except Exception as e:
        data['race_predictions'] = {'error': str(e)}

    # Endurance Score (Primary Training Metric)
    try:
        # Try multiple potential endpoints for endurance score
        endurance = None

        # Method 1: Direct endpoint (if available)
        if hasattr(client, 'get_endurance_score'):
            endurance = client.get_endurance_score(date_str)

        # Method 2: May be in training status
        if not endurance and 'training' in data and isinstance(data.get('training'), dict):
            training = client.get_training_status(date_str)
            if training:
                endurance = training.get('enduranceScore') or training.get('mostRecentEnduranceScore')

        # Method 3: Check activities for endurance data
        if not endurance:
            try:
                # Some Garmin endpoints expose this in user stats
                stats = client.get_stats(date_str)
                endurance = stats.get('enduranceScore')
            except:
                pass

        if endurance:
            if isinstance(endurance, dict):
                data['endurance_score'] = {
                    'current': endurance.get('score') or endurance.get('enduranceScore'),
                    'weekly_avg': endurance.get('weeklyAverage'),
                }
            else:
                data['endurance_score'] = {'current': endurance}
        else:
            data['endurance_score'] = {'note': 'Manual entry required - check Garmin app'}
    except Exception as e:
        data['endurance_score'] = {'error': str(e), 'note': 'Manual entry required'}

    # Respiration
    try:
        resp_data = client.get_respiration_data(date_str)
        if resp_data:
            data['respiration'] = {
                'avg_waking': resp_data.get('avgWakingRespirationValue'),
                'highest': resp_data.get('highestRespirationValue'),
                'lowest': resp_data.get('lowestRespirationValue'),
                'avg_sleeping': resp_data.get('avgSleepingRespirationValue'),
            }
    except Exception as e:
        data['respiration'] = {'error': str(e)}

    # SpO2 (Blood Oxygen)
    try:
        spo2_data = client.get_spo2_data(date_str)
        if spo2_data:
            data['spo2'] = {
                'avg': spo2_data.get('averageSpO2'),
                'lowest': spo2_data.get('lowestSpO2'),
                'avg_sleeping': spo2_data.get('avgSleepingSpO2'),
            }
    except Exception as e:
        data['spo2'] = {'error': str(e)}

    # Recent Activities (last 10)
    try:
        activities = client.get_activities(0, 10)  # start, limit
        if activities:
            data['recent_activities'] = [{
                'name': a.get('activityName'),
                'type': a.get('activityType', {}).get('typeKey'),
                'date': a.get('startTimeLocal'),
                'duration_seconds': a.get('duration'),
                'distance_meters': a.get('distance'),
                'calories': a.get('calories'),
                'avg_hr': a.get('averageHR'),
                'max_hr': a.get('maxHR'),
            } for a in activities[:5]]  # Store last 5
    except Exception as e:
        data['recent_activities'] = {'error': str(e)}

    return data

def save_data(data, date):
    """Save data to JSON file."""
    filename = DATA_DIR / f"garmin-{date.strftime('%Y-%m-%d')}.json"
    with open(filename, 'w') as f:
        json.dump(data, f, indent=2)
    return filename

def print_summary(data):
    """Print a quick summary of the data."""
    def fmt_time(secs):
        if not secs:
            return "N/A"
        m, s = divmod(int(secs), 60)
        h, m = divmod(m, 60)
        return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

    print(f"\n{'='*60}")
    print(f"  GARMIN DATA: {data['date']}")
    print(f"{'='*60}")

    # Heart Rate
    if 'heart_rate' in data and 'resting' in data['heart_rate']:
        hr = data['heart_rate']
        print(f"\n  HEART RATE")
        print(f"    Resting: {hr.get('resting')} bpm (7-day avg: {hr.get('resting_7day_avg')})")
        print(f"    Range: {hr.get('min')}-{hr.get('max')} bpm")

    # HRV
    if 'hrv' in data and isinstance(data['hrv'], dict) and 'last_night' in data['hrv']:
        hrv = data['hrv']
        print(f"\n  HRV")
        print(f"    Last night: {hrv.get('last_night')} ms")
        print(f"    Weekly avg: {hrv.get('weekly_avg')} ms (baseline: {hrv.get('baseline')})")

    # Sleep
    if 'sleep' in data and 'duration_hours' in data.get('sleep', {}):
        sleep = data['sleep']
        print(f"\n  SLEEP")
        print(f"    Duration: {sleep.get('duration_hours')} hrs")
        deep_hrs = round((sleep.get('deep_seconds') or 0) / 3600, 1)
        rem_hrs = round((sleep.get('rem_seconds') or 0) / 3600, 1)
        print(f"    Deep: {deep_hrs}h | REM: {rem_hrs}h")

    # Body Battery
    if 'body_battery' in data and data['body_battery'].get('latest'):
        bb = data['body_battery']
        print(f"\n  BODY BATTERY")
        print(f"    Current: {bb.get('latest')} (range: {bb.get('low')}-{bb.get('high')})")
        print(f"    Charged: +{bb.get('charged')} | Drained: -{bb.get('drained')}")

    # Stress
    if 'stress' in data and 'avg' in data.get('stress', {}):
        stress = data['stress']
        print(f"\n  STRESS")
        print(f"    Average: {stress.get('avg')} (max: {stress.get('max')})")
        print(f"    Low: {stress.get('low_minutes')}m | Med: {stress.get('medium_minutes')}m | High: {stress.get('high_minutes')}m")

    # Activity
    if 'activity' in data and data['activity'].get('steps'):
        act = data['activity']
        print(f"\n  ACTIVITY")
        print(f"    Steps: {act.get('steps'):,} / {act.get('step_goal'):,}")
        print(f"    Active: {act.get('active_minutes')}m (vigorous: {act.get('vigorous_intensity_minutes')}m)")
        print(f"    Calories: {int(act.get('calories_total') or 0):,} total ({int(act.get('calories_active') or 0):,} active)")

    # Training
    if 'training' in data and data['training'].get('vo2max'):
        tr = data['training']
        print(f"\n  TRAINING")
        print(f"    VO2 Max: {tr.get('vo2max')}")
        print(f"    Load: Low {int(tr.get('load_aerobic_low') or 0)} | High {int(tr.get('load_aerobic_high') or 0)}")
        print(f"    Status: {tr.get('load_feedback')}")

    # Heat Acclimation
    if 'acclimation' in data and data['acclimation'].get('heat_percent'):
        acc = data['acclimation']
        print(f"    Heat Acclimation: {acc.get('heat_percent')}% ({acc.get('heat_trend')})")

    # Training Readiness
    if 'training_readiness' in data and data['training_readiness'].get('score'):
        tr = data['training_readiness']
        print(f"\n  TRAINING READINESS")
        print(f"    Score: {tr.get('score')} ({tr.get('level')})")
        print(f"    Sleep: {tr.get('sleep_score')} ({tr.get('sleep_score_feedback')}) | HRV: {tr.get('hrv_feedback')}")
        recovery_mins = tr.get('recovery_time_minutes')
        recovery_str = f"{recovery_mins // 60}h {recovery_mins % 60}m" if recovery_mins else "N/A"
        print(f"    Recovery: {recovery_str} | Acute Load: {tr.get('acute_load')}")

    # Race Predictions
    if 'race_predictions' in data and data['race_predictions'].get('5k_seconds'):
        rp = data['race_predictions']
        print(f"\n  RACE PREDICTIONS")
        print(f"    5K: {fmt_time(rp.get('5k_seconds'))} | 10K: {fmt_time(rp.get('10k_seconds'))}")
        print(f"    Half: {fmt_time(rp.get('half_marathon_seconds'))} | Marathon: {fmt_time(rp.get('marathon_seconds'))}")

    # Respiration
    if 'respiration' in data and data['respiration'].get('avg_waking'):
        resp = data['respiration']
        print(f"\n  RESPIRATION")
        print(f"    Waking avg: {resp.get('avg_waking')} breaths/min")

    # Recent Activities
    if 'recent_activities' in data and isinstance(data['recent_activities'], list) and len(data['recent_activities']) > 0:
        print(f"\n  RECENT ACTIVITIES")
        for act in data['recent_activities'][:3]:
            dist_km = round((act.get('distance_meters') or 0) / 1000, 1)
            dur_min = round((act.get('duration_seconds') or 0) / 60)
            print(f"    {act.get('date', '')[:10]}: {act.get('name')} - {dist_km}km, {dur_min}m, HR {act.get('avg_hr')}/{act.get('max_hr')}")


def main():
    parser = argparse.ArgumentParser(description='Sync Garmin Connect data')
    parser.add_argument('--days', type=int, default=1, help='Number of days to fetch')
    parser.add_argument('--date', type=str, help='Specific date (YYYY-MM-DD)')
    args = parser.parse_args()

    client = get_client()
    if not client:
        return

    print(f"Connected to Garmin as: {client.get_full_name()}")

    if args.date:
        dates = [datetime.strptime(args.date, '%Y-%m-%d')]
    else:
        dates = [datetime.now() - timedelta(days=i) for i in range(args.days)]

    for date in dates:
        print(f"\nFetching data for {date.strftime('%Y-%m-%d')}...")
        data = get_health_data(client, date)
        filename = save_data(data, date)
        print(f"Saved to: {filename}")
        print_summary(data)

    # Also save latest as current.json for easy access
    if len(dates) == 1:
        latest_file = DATA_DIR / 'current.json'
        with open(latest_file, 'w') as f:
            json.dump(data, f, indent=2)
        print(f"\nAlso saved to: {latest_file}")


if __name__ == '__main__':
    main()
