#!/bin/bash
# Processes Claude output and extracts queue data
# Usage: queue-processor.sh <output_file>
#
# Looks for data between <<<QUEUE_START>>> and <<<QUEUE_END>>> markers
# Appends valid JSON entries to state-queue.json

DASHBOARD_DIR="$HOME/Documents/dashboard"
QUEUE_FILE="$DASHBOARD_DIR/lifeos/state/state-queue.json"
OUTPUT_FILE="$1"

if [ ! -f "$OUTPUT_FILE" ]; then
    exit 0
fi

# Extract queue data between markers
QUEUE_DATA=$(sed -n '/<<<QUEUE_START>>>/,/<<<QUEUE_END>>>/p' "$OUTPUT_FILE" | sed '1d;$d')

if [ -z "$QUEUE_DATA" ]; then
    # No queue data found
    rm -f "$OUTPUT_FILE"
    exit 0
fi

# Append to queue file
python3 << EOF
import json
import sys
from datetime import datetime

queue_file = "$QUEUE_FILE"
raw_data = '''$QUEUE_DATA'''

try:
    new_entries = json.loads(raw_data)
    if not isinstance(new_entries, list):
        new_entries = [new_entries]
except json.JSONDecodeError as e:
    print(f"Warning: Could not parse queue data: {e}", file=sys.stderr)
    sys.exit(0)

# Read existing queue
try:
    with open(queue_file, 'r') as f:
        queue = json.load(f)
except (FileNotFoundError, json.JSONDecodeError):
    queue = {"description": "Queue for state updates from automated sessions", "queue": [], "lastProcessed": None}

# Append new entries
queue['queue'].extend(new_entries)

# Write back
with open(queue_file, 'w') as f:
    json.dump(queue, f, indent=2)

print(f"Queued {len(new_entries)} state update(s) for next manual session.")
EOF

# Clean up temp file
rm -f "$OUTPUT_FILE"
