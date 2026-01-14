#!/usr/bin/env python3
"""
Gmail Sync for LifeOS
Pulls inbox status, unread count, and priority threads
"""

import json
import base64
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

# Timezone
TZ = ZoneInfo("Asia/Dubai")

# Priority senders (add known investor/partner domains)
PRIORITY_DOMAINS = [
    'taqa.com',
    'mubadala.ae',
    'adnoc.ae',
    'masdar.ae',
    'adia.ae',
]

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

def get_header(headers, name):
    """Extract header value from message headers."""
    for h in headers:
        if h['name'].lower() == name.lower():
            return h['value']
    return None

def sync():
    """Main sync function."""
    print("Pulling Gmail inbox status...")

    DATA_DIR.mkdir(exist_ok=True)

    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)

    now = datetime.now(TZ)
    today = now.strftime('%Y-%m-%d')

    # Get unread count
    unread_result = service.users().messages().list(
        userId='me',
        q='is:unread is:inbox',
        maxResults=1
    ).execute()
    unread_count = unread_result.get('resultSizeEstimate', 0)

    # Get recent unread messages (last 24h, max 20)
    yesterday = (now - timedelta(days=1)).strftime('%Y/%m/%d')
    recent_result = service.users().messages().list(
        userId='me',
        q=f'is:unread is:inbox after:{yesterday}',
        maxResults=20
    ).execute()

    recent_messages = []
    priority_threads = []

    for msg in recent_result.get('messages', []):
        msg_detail = service.users().messages().get(
            userId='me',
            id=msg['id'],
            format='metadata',
            metadataHeaders=['From', 'Subject', 'Date']
        ).execute()

        headers = msg_detail.get('payload', {}).get('headers', [])
        from_header = get_header(headers, 'From') or ''
        subject = get_header(headers, 'Subject') or '(No subject)'
        date = get_header(headers, 'Date') or ''

        # Extract email address from From header
        email = from_header
        if '<' in from_header:
            email = from_header.split('<')[1].split('>')[0]

        # Check if priority sender
        is_priority = any(domain in email.lower() for domain in PRIORITY_DOMAINS)

        msg_data = {
            'id': msg['id'],
            'thread_id': msg_detail.get('threadId'),
            'from': from_header,
            'email': email,
            'subject': subject,
            'date': date,
            'is_priority': is_priority,
            'snippet': msg_detail.get('snippet', '')[:100]
        }

        recent_messages.append(msg_data)

        if is_priority:
            priority_threads.append(msg_data)

    # Get threads needing response (in inbox, not sent by me recently)
    needs_response_result = service.users().threads().list(
        userId='me',
        q='is:inbox -from:me',
        maxResults=10
    ).execute()
    threads_needing_response = needs_response_result.get('resultSizeEstimate', 0)

    # Determine load status
    if unread_count < 20:
        load_status = 'GREEN'
    elif unread_count < 50:
        load_status = 'YELLOW'
    else:
        load_status = 'RED'

    output = {
        'fetched_at': now.isoformat(),
        'timezone': 'Asia/Dubai',
        'date': today,
        'unread_count': unread_count,
        'load_status': load_status,
        'threads_needing_response': threads_needing_response,
        'priority_threads': priority_threads,
        'recent_unread': recent_messages,
        'priority_domains': PRIORITY_DOMAINS
    }

    # Save
    output_file = DATA_DIR / "current.json"
    with open(output_file, 'w') as f:
        json.dump(output, f, indent=2, default=str)

    print(f"Saved to {output_file}")
    print(f"Unread: {unread_count} ({load_status})")
    print(f"Priority threads: {len(priority_threads)}")
    print(f"Threads needing response: {threads_needing_response}")

    return output

if __name__ == '__main__':
    sync()
