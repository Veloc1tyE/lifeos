#!/usr/bin/env python3
"""
LifeOS Sync Server
Receives dashboard data via HTTP POST and writes to lifeos/state/

Usage:
    python3 sync-server.py

Runs on http://localhost:3456
Dashboard POSTs to /sync endpoint
"""

import http.server
import json
import os
from datetime import datetime
from pathlib import Path

PORT = 3456
STATE_DIR = Path(__file__).parent / "state"
DASHBOARD_FILE = STATE_DIR / "dashboard-live.json"

class SyncHandler(http.server.BaseHTTPRequestHandler):
    def _send_cors_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")

    def do_OPTIONS(self):
        """Handle CORS preflight"""
        self.send_response(200)
        self._send_cors_headers()
        self.end_headers()

    def do_GET(self):
        """Health check endpoint"""
        if self.path == "/health":
            self.send_response(200)
            self._send_cors_headers()
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            response = {
                "status": "ok",
                "server": "lifeos-sync",
                "port": PORT,
                "state_dir": str(STATE_DIR),
                "last_sync": get_last_sync_time()
            }
            self.wfile.write(json.dumps(response).encode())
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        """Receive and save dashboard data"""
        if self.path == "/sync":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body = self.rfile.read(content_length)
                data = json.loads(body.decode("utf-8"))

                # Ensure state directory exists
                STATE_DIR.mkdir(parents=True, exist_ok=True)

                # Write dashboard data
                with open(DASHBOARD_FILE, "w") as f:
                    json.dump(data, f, indent=2)

                # Send success response
                self.send_response(200)
                self._send_cors_headers()
                self.send_header("Content-Type", "application/json")
                self.end_headers()

                timestamp = datetime.now().isoformat()
                response = {
                    "status": "synced",
                    "timestamp": timestamp,
                    "file": str(DASHBOARD_FILE)
                }
                self.wfile.write(json.dumps(response).encode())

                print(f"[{timestamp}] Synced dashboard data")

            except json.JSONDecodeError as e:
                self.send_response(400)
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(f"Invalid JSON: {e}".encode())

            except Exception as e:
                self.send_response(500)
                self._send_cors_headers()
                self.end_headers()
                self.wfile.write(f"Server error: {e}".encode())
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        """Suppress default logging, we do our own"""
        pass


def get_last_sync_time():
    """Get last modification time of dashboard file"""
    if DASHBOARD_FILE.exists():
        mtime = DASHBOARD_FILE.stat().st_mtime
        return datetime.fromtimestamp(mtime).isoformat()
    return None


def main():
    print(f"""
╔═══════════════════════════════════════════╗
║         LifeOS Sync Server                ║
╠═══════════════════════════════════════════╣
║  Port:     http://localhost:{PORT}          ║
║  Endpoint: POST /sync                     ║
║  Health:   GET /health                    ║
║  Output:   {STATE_DIR}/dashboard-live.json
╚═══════════════════════════════════════════╝
    """)

    server = http.server.HTTPServer(("localhost", PORT), SyncHandler)

    try:
        print("Server running. Press Ctrl+C to stop.\n")
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down...")
        server.shutdown()


if __name__ == "__main__":
    main()
