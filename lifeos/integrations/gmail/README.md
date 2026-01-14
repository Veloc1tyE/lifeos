# Gmail Integration

## Overview

Read email for load assessment, follow-up detection, and communication tracking. Draft capability for action packets with approval.

**Account:** will@aquila.earth (primary)

## Data Available

| Data | Use | Pillar |
|------|-----|--------|
| Unread count | Load signal | P1 |
| Threads needing response | Follow-up tracking | P3 |
| Sent emails | Output tracking | P3/P6 |
| Meeting confirmations | Calendar cross-reference | P3 |
| Investor/partner threads | Pipeline signal | P3 |

## Integration Options

### Option 1: Gmail API (Recommended)

**Setup Required:**
1. Enable Gmail API in Cloud Console
2. Use same OAuth credentials
3. Add Gmail scopes

**Scopes:**
- `https://www.googleapis.com/auth/gmail.readonly` (read)
- `https://www.googleapis.com/auth/gmail.compose` (draft, if approved)

**API Operations:**
- `GET /users/me/messages` - List messages
- `GET /users/me/threads` - List threads
- `GET /users/me/labels` - Get labels
- `POST /users/me/drafts` - Create draft (requires approval)

### Option 2: Manual Review

1. Check inbox daily
2. Note key threads
3. Track follow-ups manually

## Integration Script (Template)

```python
# lifeos/integrations/gmail/sync.py
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build

def get_inbox_status():
    """Get inbox load metrics."""
    creds = Credentials.from_authorized_user_file('token.json')
    service = build('gmail', 'v1', credentials=creds)

    # Get unread count
    results = service.users().messages().list(
        userId='me',
        q='is:unread',
        maxResults=1
    ).execute()

    unread_estimate = results.get('resultSizeEstimate', 0)

    return {
        'unread_count': unread_estimate,
        'assessed_at': datetime.now().isoformat()
    }

def get_threads_needing_response():
    """Find threads where I'm expected to respond."""
    # Query: in inbox, not from me, no recent reply from me
    pass

def get_capital_threads():
    """Find threads with known investor contacts."""
    # Cross-reference with CRM contacts
    pass
```

## Daily Email Queries

**Morning:**
- Unread count (load signal)
- Urgent threads requiring response
- Capital/partner threads to prioritize

**Evening:**
- Threads responded to today
- Threads still pending

## Weekly Email Queries

**P3 Assessment:**
- Follow-up emails sent
- Investor thread activity
- Response time to important contacts

## Action Packets (Write Operations)

**Requires "approve":**

1. **Draft follow-up email**
   - To specific contact
   - With suggested content
   - User reviews before send

2. **Draft meeting request**
   - To pipeline contact
   - With suggested times

3. **Draft intro request**
   - To connector
   - For specific introduction

## Load Assessment Thresholds

| Unread Count | Assessment | Action |
|--------------|------------|--------|
| <20 | GREEN | Normal |
| 20-50 | YELLOW | Triage priority |
| >50 | RED | Email backlog intervention |

## File Structure

```
lifeos/integrations/gmail/
├── README.md          # This file
├── sync.py            # Sync script
└── cache/
    └── status.json    # Cached inbox status
```

## Privacy Notes

- LifeOS reads metadata primarily (counts, senders, subjects)
- Full message content only when relevant to capital tracking
- No storage of sensitive personal emails
- Focus on work-related threads

## Integration Priority

**Phase 1:** Unread count as load signal
**Phase 2:** Capital thread tracking
**Phase 3:** Draft capability for follow-ups
