# CRM Integration (Google Sheets)

## Overview

Track capital pipeline and contract leads for Pillar 3. Read for status, write for updates with approval.

**Location:** Google Sheets
**URL:** https://docs.google.com/spreadsheets/d/1qIKepulGJSrJ0i4GTCkku1wbO8bVGqOj4MqLIN4GHuM/edit
**Account:** will@aquila.earth

## Data Model (Current/Proposed)

### Capital Pipeline

| Column | Description |
|--------|-------------|
| Name | Contact/Fund name |
| Organization | Fund/Entity |
| Type | Sovereign / Strategic / VC / Family Office |
| Stage | Cold / Warm / Active / Due Diligence / Committed |
| Size Potential | $ amount target |
| Last Contact | Date of last interaction |
| Next Action | Specific next step |
| Notes | Context and history |
| UAE Relevant | Yes/No (for filtering) |

### Contract Pipeline

| Column | Description |
|--------|-------------|
| Name | Contract/Client name |
| Type | Defence / Logistics / Energy / Infrastructure |
| Stage | Lead / Proposal / Negotiation / LOI / Signed |
| Value | $ amount |
| Last Contact | Date |
| Next Action | Specific next step |
| Notes | Context |

## Integration Options

### Option 1: Google Sheets API (Recommended)

**Setup Required:**
1. Enable Google Sheets API in Cloud Console
2. Use same OAuth credentials as Calendar
3. Add Sheets scope

**Scopes:**
- `https://www.googleapis.com/auth/spreadsheets.readonly` (read)
- `https://www.googleapis.com/auth/spreadsheets` (write, if approved)

**API Operations:**
- `GET /spreadsheets/{id}/values/{range}` - Read data
- `PUT /spreadsheets/{id}/values/{range}` - Update data

### Option 2: CSV Export (Simpler)

1. Export sheet as CSV
2. Parse locally
3. Manual but no auth

## Integration Script (Template)

```python
# lifeos/integrations/crm/sync.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import json

SPREADSHEET_ID = '1qIKepulGJSrJ0i4GTCkku1wbO8bVGqOj4MqLIN4GHuM'

def get_pipeline_status():
    """Read CRM and compute pipeline metrics."""
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('sheets', 'v4', credentials=creds)

    # Read capital pipeline
    result = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range='Capital!A:J'
    ).execute()

    rows = result.get('values', [])
    return process_pipeline(rows)

def get_stale_leads(days=7):
    """Find leads with no contact in X days."""
    # Implementation
    pass

def get_follow_ups_due():
    """List leads needing follow-up today."""
    # Implementation
    pass
```

## Daily CRM Queries

**Morning:**
- Follow-ups due today
- Stale leads (>7 days no contact)
- Meetings scheduled with pipeline contacts

**P3 Daily Action Requirement:**
At least one of:
- Follow-up sent
- Meeting scheduled
- Intro requested
- CRM updated

## Weekly CRM Queries

**Capital Pipeline:**
- Total leads by stage
- Movement this week (stage changes)
- Pipeline value
- Stale lead count
- Conversion velocity

**Contract Pipeline:**
- Active conversations
- LOIs in progress
- Total contract value in pipeline

## Action Packets (Write Operations)

**Requires "approve":**

1. **Update Last Contact**
   - After meeting/call
   - Log date and brief note

2. **Update Stage**
   - When lead progresses
   - Document reason

3. **Add Next Action**
   - Specific, dated
   - Accountable

4. **Add New Lead**
   - Basic info capture
   - Initial stage assignment

## File Structure

```
lifeos/integrations/crm/
├── README.md          # This file
├── sync.py            # Sync script
└── cache/
    └── pipeline.json  # Cached pipeline data
```

## P3 Metrics from CRM

**Weekly Dashboard:**
- Meetings held
- Follow-ups sent
- Pipeline movement (leads advancing)
- Total pipeline value
- Days since last major contact

**Intervention Triggers:**
- 0 follow-ups this week → immediate flag
- All leads stale (>7 days) → material drift
- No stage movement in 2 weeks → intervention

## UAE Relevance Filter

For Abu Dhabi focus:
- Filter by "UAE Relevant = Yes"
- Prioritize sovereign/strategic leads
- Track TAQA, Mubadala, ADIA specifically
