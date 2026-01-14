#!/usr/bin/env python3
"""
Google Calendar Sync for LifeOS
Pulls calendar events for today + next 3 days
"""

import json
import os
from datetime import datetime, timedelta
from pathlib import Path
from zoneinfo import ZoneInfo

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Paths
SCRIPT_DIR = Path(__file__).parent
INTEGRATIONS_DIR = SCRIPT_DIR.parent
DATA_DIR = SCRIPT_DIR / "data"
TOKEN_FILE = INTEGRATIONS_DIR / "token-work.json"
CREDENTIALS_FILE = INTEGRATIONS_DIR / "google-credentials.json"

# Timezone
TZ = ZoneInfo("Asia/Dubai")

def get_credentials():
    """Load and refresh credentials."""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(f"Token file not found: {TOKEN_FILE}")

    creds = Credentials.from_authorized_user_file(str(TOKEN_FILE))

    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        with open(TOKEN_FILE, 'w') as f:
            f.write(creds.to_json())

    return creds

def get_events(days_ahead=3):
    """Fetch calendar events for today + next N days."""
    creds = get_credentials()
    service = build('calendar', 'v3', credentials=creds)

    now = datetime.now(TZ)
    start = now.replace(hour=0, minute=0, second=0, microsecond=0)
    end = start + timedelta(days=days_ahead + 1)

    events_result = service.events().list(
        calendarId='primary',
        timeMin=start.isoformat(),
        timeMax=end.isoformat(),
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    events = events_result.get('items', [])

    # Process events
    processed = []
    for event in events:
        start_raw = event['start'].get('dateTime', event['start'].get('date'))
        end_raw = event['end'].get('dateTime', event['end'].get('date'))

        # Parse datetime
        if 'T' in start_raw:
            start_dt = datetime.fromisoformat(start_raw.replace('Z', '+00:00'))
            end_dt = datetime.fromisoformat(end_raw.replace('Z', '+00:00'))
            all_day = False
        else:
            start_dt = datetime.strptime(start_raw, '%Y-%m-%d').replace(tzinfo=TZ)
            end_dt = datetime.strptime(end_raw, '%Y-%m-%d').replace(tzinfo=TZ)
            all_day = True

        processed.append({
            'id': event['id'],
            'summary': event.get('summary', '(No title)'),
            'start': start_dt.isoformat(),
            'end': end_dt.isoformat(),
            'all_day': all_day,
            'location': event.get('location'),
            'description': event.get('description', '')[:200],  # Truncate
            'status': event.get('status'),
            'date': start_dt.strftime('%Y-%m-%d'),
            'time': start_dt.strftime('%H:%M') if not all_day else None,
            'duration_mins': int((end_dt - start_dt).total_seconds() / 60) if not all_day else None
        })

    return processed

def find_free_blocks(events, date, min_duration_mins=120):
    """Find free blocks of at least min_duration_mins on a given date."""
    day_events = [e for e in events if e['date'] == date and not e['all_day']]
    day_events.sort(key=lambda x: x['start'])

    # Working hours: 8am - 8pm
    day_start = datetime.strptime(f"{date} 08:00", '%Y-%m-%d %H:%M').replace(tzinfo=TZ)
    day_end = datetime.strptime(f"{date} 20:00", '%Y-%m-%d %H:%M').replace(tzinfo=TZ)

    free_blocks = []
    current = day_start

    for event in day_events:
        event_start = datetime.fromisoformat(event['start'])
        event_end = datetime.fromisoformat(event['end'])

        if event_start > current:
            gap_mins = int((event_start - current).total_seconds() / 60)
            if gap_mins >= min_duration_mins:
                free_blocks.append({
                    'start': current.strftime('%H:%M'),
                    'end': event_start.strftime('%H:%M'),
                    'duration_mins': gap_mins
                })

        current = max(current, event_end)

    # Check end of day
    if day_end > current:
        gap_mins = int((day_end - current).total_seconds() / 60)
        if gap_mins >= min_duration_mins:
            free_blocks.append({
                'start': current.strftime('%H:%M'),
                'end': day_end.strftime('%H:%M'),
                'duration_mins': gap_mins
            })

    return free_blocks

def sync():
    """Main sync function."""
    print("Pulling Google Calendar...")

    DATA_DIR.mkdir(exist_ok=True)

    now = datetime.now(TZ)
    today = now.strftime('%Y-%m-%d')

    events = get_events(days_ahead=3)

    # Organize by date
    by_date = {}
    for event in events:
        date = event['date']
        if date not in by_date:
            by_date[date] = []
        by_date[date].append(event)

    # Find free blocks for today
    free_blocks_today = find_free_blocks(events, today)

    # Count meetings by date
    meeting_counts = {date: len(evts) for date, evts in by_date.items()}

    output = {
        'fetched_at': now.isoformat(),
        'timezone': 'Asia/Dubai',
        'today': today,
        'events': events,
        'by_date': by_date,
        'free_blocks_today': free_blocks_today,
        'meeting_counts': meeting_counts,
        'total_events': len(events)
    }

    # Save
    output_file = DATA_DIR / "current.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    # Also save dated backup
    dated_file = DATA_DIR / f"calendar-{today}.json"
    with open(dated_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"Saved to {output_file}")
    print(f"Today: {len(by_date.get(today, []))} events")
    print(f"Free 2hr+ blocks today: {len(free_blocks_today)}")

    return output

if __name__ == '__main__':
    sync()
