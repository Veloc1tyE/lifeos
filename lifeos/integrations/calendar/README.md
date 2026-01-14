# Google Calendar Integration

## Overview

Read calendar data to assess load, identify conflicts, and prepare daily structure. Write access for scheduling with approval.

**Account:** will@aquila.earth
**Client:** Vimcal

## Data Available

| Data | Use | Pillar |
|------|-----|--------|
| Today's events | Day planning, load assessment | All |
| Meeting count | Capital velocity tracking | P3 |
| Free blocks | 2-hour deep work identification | P3 |
| Travel events | Transition/load prediction | P1 |
| Recurring events | Routine structure | P7 |
| Buffer time | Recovery anchor identification | P1 |

## Integration Options

### Option 1: Google Calendar API (Recommended)

**Setup Required:**
1. Go to Google Cloud Console
2. Create project or use existing
3. Enable Google Calendar API
4. Create OAuth 2.0 credentials
5. Download credentials JSON
6. Store in `lifeos/integrations/calendar/.env`

**Scopes Needed:**
- `https://www.googleapis.com/auth/calendar.readonly` (read)
- `https://www.googleapis.com/auth/calendar.events` (write, if approved)

**API Endpoints:**
- `GET /calendars/{calendarId}/events` - List events
- `POST /calendars/{calendarId}/events` - Create event (requires approval)

### Option 2: ICS Export (Simpler)

1. Export calendar to ICS file
2. Parse ICS for events
3. Manual but no auth required

### Option 3: Vimcal Integration

If Vimcal has an API, may be simpler than direct Google integration.

## Integration Script (Template)

```python
# lifeos/integrations/calendar/sync.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json

def get_today_events():
    """Fetch today's calendar events."""
    # Load credentials
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('calendar', 'v3', credentials=creds)

    # Get today's events
    now = datetime.utcnow()
    start = now.replace(hour=0, minute=0, second=0).isoformat() + 'Z'
    end = now.replace(hour=23, minute=59, second=59).isoformat() + 'Z'

    events = service.events().list(
        calendarId='primary',
        timeMin=start,
        timeMax=end,
        singleEvents=True,
        orderBy='startTime'
    ).execute()

    return events.get('items', [])

def get_week_meeting_count():
    """Count meetings this week for P3 tracking."""
    # Implementation here
    pass

def find_deep_work_blocks():
    """Identify 2+ hour free blocks."""
    # Implementation here
    pass
```

## Daily Calendar Queries

**Morning Calibration:**
1. What's on the calendar today?
2. Are there 2-hour free blocks?
3. Any high-stakes meetings?
4. Any travel or transitions?

**Evening Shutdown:**
1. What's on tomorrow?
2. Any early meetings that affect sleep?
3. Conflicts to resolve?

**Weekly Review:**
1. Total meetings this week
2. Meeting:recovery ratio
3. Calendar load trend

## Action Packets (Write Operations)

**Requires "approve" before execution:**

1. **Reschedule meeting** (sleep protection)
   - Identify early meeting
   - Propose new time
   - Draft reschedule message

2. **Block focus time**
   - Create 2-hour event
   - Label: "2-Hour Block: [Focus Area]"

3. **Add recovery anchor**
   - Block low-stimulus time
   - No meetings allowed

## File Structure

```
lifeos/integrations/calendar/
├── README.md          # This file
├── .env               # API credentials
├── credentials.json   # OAuth credentials
├── token.json         # Access token (generated)
├── sync.py            # Python sync script
└── cache/             # Cached calendar data
```

## Timezone Handling

**Primary:** Asia/Dubai (GMT+4)
**Note:** When traveling, calendar times should auto-adjust but load assessment may need manual timezone override.

## Integration with LifeOS

**Morning trigger reads:**
- Today's events
- Meeting count
- Free blocks
- Transition events

**Weekly trigger reads:**
- Total meetings
- Meeting velocity trend
- Calendar density

**P3 Capital tracking:**
- Meetings held this week
- Meeting-to-follow-up ratio
