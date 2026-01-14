#!/bin/bash
# Start LifeOS Sync Server
# Run this before using the dashboard for auto-sync

cd "$(dirname "$0")"
python3 sync-server.py
