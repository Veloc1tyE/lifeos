#!/usr/bin/env python3
"""
DayOne Journal Sync for LifeOS
Extracts journal entries from DayOne SQLite database.

Usage:
    python3 sync.py              # Last 7 days
    python3 sync.py --days 30    # Last 30 days
    python3 sync.py --all        # All entries
"""

import sqlite3
import json
import argparse
from datetime import datetime, timedelta
from pathlib import Path

# DayOne database location
DAYONE_DB = Path.home() / "Library/Group Containers/5U8NS4GX82.dayoneapp2/Data/Documents/DayOne.sqlite"
DATA_DIR = Path(__file__).parent / "data"
DATA_DIR.mkdir(exist_ok=True)


def get_entries(days=7, all_entries=False):
    """Extract journal entries from DayOne database."""
    if not DAYONE_DB.exists():
        print(f"ERROR: DayOne database not found at {DAYONE_DB}")
        return []

    conn = sqlite3.connect(f"file:{DAYONE_DB}?mode=ro", uri=True)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    # Build date filter
    if all_entries:
        date_filter = ""
        params = ()
    else:
        cutoff = datetime.now() - timedelta(days=days)
        # DayOne uses Core Data timestamp (seconds since 2001-01-01)
        core_data_epoch = datetime(2001, 1, 1)
        cutoff_timestamp = (cutoff - core_data_epoch).total_seconds()
        date_filter = "WHERE ZCREATIONDATE >= ?"
        params = (cutoff_timestamp,)

    # Query entries
    query = f"""
        SELECT
            ZUUID as uuid,
            ZCREATIONDATE as creation_date,
            ZMODIFIEDDATE as modified_date,
            ZMARKDOWNTEXT as content,
            ZSTARRED as starred,
            ZISPINNED as pinned,
            ZDURATION as duration,
            ZGREGORIANDAY as day,
            ZGREGORIANMONTH as month,
            ZGREGORIANYEAR as year,
            ZWEATHER as weather_id,
            ZLOCATION as location_id,
            ZJOURNAL as journal_id
        FROM ZENTRY
        {date_filter}
        ORDER BY ZCREATIONDATE DESC
    """

    cursor.execute(query, params)
    rows = cursor.fetchall()

    # Convert Core Data timestamps to ISO format
    core_data_epoch = datetime(2001, 1, 1)

    entries = []
    for row in rows:
        entry = dict(row)

        # Convert timestamps
        if entry['creation_date']:
            dt = core_data_epoch + timedelta(seconds=entry['creation_date'])
            entry['creation_date'] = dt.isoformat()
            entry['date'] = dt.strftime('%Y-%m-%d')
            entry['time'] = dt.strftime('%H:%M')

        if entry['modified_date']:
            dt = core_data_epoch + timedelta(seconds=entry['modified_date'])
            entry['modified_date'] = dt.isoformat()

        # Ensure content is string
        entry['content'] = entry.get('content') or ''

        entries.append(entry)

    # Try to get journal names
    try:
        cursor.execute("SELECT Z_PK, ZNAME FROM ZJOURNAL")
        journals = {row['Z_PK']: row['ZNAME'] for row in cursor.fetchall()}
    except:
        journals = {}

    conn.close()
    return entries


def get_tags(conn):
    """Get all tags from database."""
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT ZUUID, ZNAME FROM ZTAG")
        return {row[0]: row[1] for row in cursor.fetchall()}
    except:
        return {}


def save_entries(entries, filename="journal.json"):
    """Save entries to JSON file."""
    filepath = DATA_DIR / filename
    with open(filepath, 'w') as f:
        json.dump(entries, f, indent=2, ensure_ascii=False)
    return filepath


def print_summary(entries):
    """Print summary of extracted entries."""
    print(f"\n{'='*60}")
    print(f"  DAYONE JOURNAL SYNC")
    print(f"{'='*60}")
    print(f"\n  Entries extracted: {len(entries)}")

    if entries:
        # Date range
        dates = [e['date'] for e in entries if 'date' in e]
        if dates:
            print(f"  Date range: {min(dates)} to {max(dates)}")

        # Recent entries preview
        print(f"\n  RECENT ENTRIES:")
        for entry in entries[:5]:
            date = entry.get('date', 'Unknown')
            time = entry.get('time', '')
            content = entry.get('content', '')[:60].replace('\n', ' ')
            starred = '⭐' if entry.get('starred') else '  '
            print(f"    {starred} {date} {time}: {content}...")


def export_markdown(entries, output_dir=None):
    """Export entries as individual markdown files."""
    if output_dir is None:
        output_dir = DATA_DIR / "markdown"
    output_dir = Path(output_dir)
    output_dir.mkdir(exist_ok=True)

    for entry in entries:
        date = entry.get('date', 'unknown')
        time = entry.get('time', '0000').replace(':', '')
        uuid = entry.get('uuid', 'unknown')[:8]
        filename = f"{date}_{time}_{uuid}.md"

        content = entry.get('content', '')
        filepath = output_dir / filename

        with open(filepath, 'w') as f:
            f.write(f"# {date} {entry.get('time', '')}\n\n")
            f.write(content)

    return output_dir


def main():
    parser = argparse.ArgumentParser(description='Sync DayOne journal entries')
    parser.add_argument('--days', type=int, default=7, help='Number of days to fetch (default: 7)')
    parser.add_argument('--all', action='store_true', help='Fetch all entries')
    parser.add_argument('--markdown', action='store_true', help='Also export as markdown files')
    args = parser.parse_args()

    print("Reading DayOne database...")
    entries = get_entries(days=args.days, all_entries=args.all)

    if not entries:
        print("No entries found.")
        return

    # Save as JSON
    filepath = save_entries(entries)
    print(f"Saved to: {filepath}")

    # Also save as current.json for easy access
    current_path = save_entries(entries, "current.json")
    print(f"Also saved to: {current_path}")

    # Optionally export markdown
    if args.markdown:
        md_dir = export_markdown(entries)
        print(f"Markdown files: {md_dir}")

    print_summary(entries)


if __name__ == '__main__':
    main()
