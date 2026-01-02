#!/usr/bin/env python3
"""
License Activation Server
=========================

Optional online license activation and validation server.
"""

import os
import json
import hashlib
import sqlite3
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from dataclasses import dataclass, asdict
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse


@dataclass
class ActivationRecord:
    """Record of a license activation."""
    license_key: str
    machine_id: str
    activated_at: str
    expires_at: str
    is_active: bool = True
    activation_count: int = 1


class ActivationDatabase:
    """SQLite database for activation records."""

    def __init__(self, db_path: str = "activations.db"):
        self.db_path = db_path
        self._init_db()

    def _init_db(self) -> None:
        """Initialize database schema."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS activations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                license_key TEXT NOT NULL,
                machine_id TEXT NOT NULL,
                activated_at TEXT NOT NULL,
                expires_at TEXT NOT NULL,
                is_active INTEGER DEFAULT 1,
                activation_count INTEGER DEFAULT 1,
                UNIQUE(license_key, machine_id)
            )
        """)

        cursor.execute("""
            CREATE INDEX IF NOT EXISTS idx_license_key ON activations(license_key)
        """)

        conn.commit()
        conn.close()

    def activate(
        self,
        license_key: str,
        machine_id: str,
        duration_days: int = 365
    ) -> ActivationRecord:
        """Activate a license for a machine."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        now = datetime.utcnow()
        expires = now + timedelta(days=duration_days)

        # Check if already activated
        cursor.execute(
            "SELECT * FROM activations WHERE license_key = ? AND machine_id = ?",
            (license_key, machine_id)
        )
        existing = cursor.fetchone()

        if existing:
            # Update existing activation
            cursor.execute("""
                UPDATE activations
                SET is_active = 1, activation_count = activation_count + 1
                WHERE license_key = ? AND machine_id = ?
            """, (license_key, machine_id))
        else:
            # New activation
            cursor.execute("""
                INSERT INTO activations (license_key, machine_id, activated_at, expires_at)
                VALUES (?, ?, ?, ?)
            """, (license_key, machine_id, now.isoformat(), expires.isoformat()))

        conn.commit()
        conn.close()

        return ActivationRecord(
            license_key=license_key,
            machine_id=machine_id,
            activated_at=now.isoformat(),
            expires_at=expires.isoformat(),
        )

    def validate(self, license_key: str, machine_id: str) -> Optional[ActivationRecord]:
        """Validate an activation."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT license_key, machine_id, activated_at, expires_at, is_active, activation_count
            FROM activations
            WHERE license_key = ? AND machine_id = ? AND is_active = 1
        """, (license_key, machine_id))

        row = cursor.fetchone()
        conn.close()

        if not row:
            return None

        # Check expiration
        expires = datetime.fromisoformat(row[3])
        if datetime.utcnow() > expires:
            return None

        return ActivationRecord(
            license_key=row[0],
            machine_id=row[1],
            activated_at=row[2],
            expires_at=row[3],
            is_active=bool(row[4]),
            activation_count=row[5],
        )

    def deactivate(self, license_key: str, machine_id: str) -> bool:
        """Deactivate a license."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE activations SET is_active = 0
            WHERE license_key = ? AND machine_id = ?
        """, (license_key, machine_id))

        affected = cursor.rowcount
        conn.commit()
        conn.close()

        return affected > 0

    def get_activation_count(self, license_key: str) -> int:
        """Get number of active activations for a license."""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT COUNT(*) FROM activations
            WHERE license_key = ? AND is_active = 1
        """, (license_key,))

        count = cursor.fetchone()[0]
        conn.close()

        return count


class ActivationHandler(BaseHTTPRequestHandler):
    """HTTP handler for activation requests."""

    db: ActivationDatabase = None

    def do_POST(self):
        """Handle POST requests."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        data = json.loads(body) if body else {}

        if self.path == "/activate":
            self._handle_activate(data)
        elif self.path == "/validate":
            self._handle_validate(data)
        elif self.path == "/deactivate":
            self._handle_deactivate(data)
        else:
            self._send_error(404, "Not found")

    def _handle_activate(self, data: dict):
        """Handle activation request."""
        license_key = data.get("license_key")
        machine_id = data.get("machine_id")

        if not license_key or not machine_id:
            self._send_error(400, "Missing license_key or machine_id")
            return

        # Check activation limit (e.g., 3 machines per license)
        current_count = self.db.get_activation_count(license_key)
        if current_count >= 3:
            self._send_error(403, "Activation limit reached")
            return

        record = self.db.activate(license_key, machine_id)
        self._send_json(200, asdict(record))

    def _handle_validate(self, data: dict):
        """Handle validation request."""
        license_key = data.get("license_key")
        machine_id = data.get("machine_id")

        if not license_key or not machine_id:
            self._send_error(400, "Missing license_key or machine_id")
            return

        record = self.db.validate(license_key, machine_id)
        if record:
            self._send_json(200, {"valid": True, **asdict(record)})
        else:
            self._send_json(200, {"valid": False})

    def _handle_deactivate(self, data: dict):
        """Handle deactivation request."""
        license_key = data.get("license_key")
        machine_id = data.get("machine_id")

        if not license_key or not machine_id:
            self._send_error(400, "Missing license_key or machine_id")
            return

        success = self.db.deactivate(license_key, machine_id)
        self._send_json(200, {"success": success})

    def _send_json(self, status: int, data: dict):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, status: int, message: str):
        """Send error response."""
        self._send_json(status, {"error": message})

    def log_message(self, format, *args):
        """Suppress default logging."""
        pass


def run_server(host: str = "0.0.0.0", port: int = 8080, db_path: str = "activations.db"):
    """Run the activation server."""
    db = ActivationDatabase(db_path)
    ActivationHandler.db = db

    server = HTTPServer((host, port), ActivationHandler)
    print(f"Activation server running on {host}:{port}")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("Server stopped")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="License Activation Server")
    parser.add_argument("--host", default="0.0.0.0", help="Host to bind to")
    parser.add_argument("--port", type=int, default=8080, help="Port to listen on")
    parser.add_argument("--db", default="activations.db", help="Database path")

    args = parser.parse_args()
    run_server(args.host, args.port, args.db)
