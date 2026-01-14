#!/usr/bin/env python3
"""
Google API Authentication Setup for LifeOS
Authenticates both work and personal accounts.

Usage:
    python3 google-auth-setup.py
"""

import os
import json
from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

# Scopes needed for LifeOS
SCOPES = [
    'https://www.googleapis.com/auth/calendar.readonly',      # Read calendar
    'https://www.googleapis.com/auth/spreadsheets.readonly',  # Read CRM
    'https://www.googleapis.com/auth/gmail.readonly',         # Read email
]

INTEGRATIONS_DIR = Path(__file__).parent
CREDENTIALS_FILE = INTEGRATIONS_DIR / 'google-credentials.json'

ACCOUNTS = [
    {
        'name': 'work',
        'email': 'will@aquila.earth',
        'token_file': INTEGRATIONS_DIR / 'token-work.json'
    },
    {
        'name': 'personal',
        'email': 'w.jeremijenko@gmail.com',
        'token_file': INTEGRATIONS_DIR / 'token-personal.json'
    }
]


def authenticate_account(account):
    """Authenticate a single account and save token."""
    print(f"\n{'='*50}")
    print(f"Authenticating: {account['email']}")
    print(f"{'='*50}")

    creds = None
    token_file = account['token_file']

    # Check for existing token
    if token_file.exists():
        creds = Credentials.from_authorized_user_file(str(token_file), SCOPES)

    # Refresh or get new credentials
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            print("Refreshing existing token...")
            creds.refresh(Request())
        else:
            print(f"\nOpening browser for {account['email']}...")
            print(f">>> Make sure to sign in with: {account['email']} <<<\n")
            input("Press Enter when ready...")

            flow = InstalledAppFlow.from_client_secrets_file(
                str(CREDENTIALS_FILE), SCOPES
            )
            creds = flow.run_local_server(port=8080)

        # Save token
        with open(token_file, 'w') as f:
            f.write(creds.to_json())
        print(f"Token saved to: {token_file.name}")

    return creds


def test_apis(creds, account_name):
    """Test all APIs with the credentials."""
    print(f"\nTesting APIs for {account_name}...")

    # Test Calendar
    try:
        service = build('calendar', 'v3', credentials=creds)
        events = service.events().list(
            calendarId='primary',
            maxResults=1
        ).execute()
        print(f"  ✓ Calendar API: OK")
    except Exception as e:
        print(f"  ✗ Calendar API: {e}")

    # Test Gmail
    try:
        service = build('gmail', 'v1', credentials=creds)
        profile = service.users().getProfile(userId='me').execute()
        print(f"  ✓ Gmail API: OK ({profile.get('emailAddress')})")
    except Exception as e:
        print(f"  ✗ Gmail API: {e}")

    # Test Sheets (just build service, no specific sheet to test)
    try:
        service = build('sheets', 'v4', credentials=creds)
        print(f"  ✓ Sheets API: OK")
    except Exception as e:
        print(f"  ✗ Sheets API: {e}")


def main():
    print("""
╔═══════════════════════════════════════════════════════╗
║        LifeOS Google API Authentication Setup         ║
╚═══════════════════════════════════════════════════════╝

This will authenticate both your accounts:
  1. will@aquila.earth (work)
  2. w.jeremijenko@gmail.com (personal)

A browser window will open for each account.
Make sure to sign in with the CORRECT account each time.
""")

    if not CREDENTIALS_FILE.exists():
        print(f"ERROR: Credentials file not found: {CREDENTIALS_FILE}")
        return

    for account in ACCOUNTS:
        try:
            creds = authenticate_account(account)
            test_apis(creds, account['name'])
        except Exception as e:
            print(f"Error authenticating {account['email']}: {e}")

    print(f"""
{'='*50}
Setup Complete!
{'='*50}

Token files created:
  - token-work.json (will@aquila.earth)
  - token-personal.json (w.jeremijenko@gmail.com)

LifeOS can now access:
  - Google Calendar (read)
  - Google Sheets/CRM (read)
  - Gmail (read)

Run this script again anytime to refresh tokens.
""")


if __name__ == '__main__':
    main()
