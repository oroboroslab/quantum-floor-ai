"""
Connection-Core REST API
========================

Simple REST API for the memory engine.
"""

import json
from typing import Optional
from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse

from .connection_core import MemoryEngine, MemoryConfig


class MemoryAPI(BaseHTTPRequestHandler):
    """HTTP handler for Memory API."""

    engine: MemoryEngine = None

    def do_GET(self):
        """Handle GET requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path
        query = urllib.parse.parse_qs(parsed.query)

        if path == "/health":
            self._send_json(200, {"status": "healthy"})

        elif path == "/stats":
            stats = self.engine.get_stats()
            self._send_json(200, stats)

        elif path == "/memories":
            # List/search memories
            q = query.get("q", [""])[0]
            limit = int(query.get("limit", [10])[0])

            memories = self.engine.recall(q, limit=limit)
            self._send_json(200, {
                "memories": [m.to_dict() for m in memories],
                "count": len(memories),
            })

        elif path.startswith("/memories/"):
            # Get specific memory
            memory_id = path.split("/")[-1]
            memory = self.engine.get(memory_id)

            if memory:
                self._send_json(200, memory.to_dict())
            else:
                self._send_error(404, "Memory not found")

        else:
            self._send_error(404, "Not found")

    def do_POST(self):
        """Handle POST requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        body = self._read_body()

        if path == "/memories":
            # Create memory
            content = body.get("content")
            if not content:
                self._send_error(400, "Content required")
                return

            memory = self.engine.add(
                content=content,
                importance=body.get("importance"),
                tags=body.get("tags"),
                metadata=body.get("metadata"),
            )

            self._send_json(201, memory.to_dict())

        elif path == "/recall":
            # Recall memories
            query = body.get("query", "")
            limit = body.get("limit", 5)

            memories = self.engine.recall(query, limit=limit)
            self._send_json(200, {
                "memories": [m.to_dict() for m in memories],
                "count": len(memories),
            })

        else:
            self._send_error(404, "Not found")

    def do_PUT(self):
        """Handle PUT requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path.startswith("/memories/"):
            memory_id = path.split("/")[-1]
            body = self._read_body()

            memory = self.engine.update(
                memory_id,
                content=body.get("content"),
                importance=body.get("importance"),
                tags=body.get("tags"),
                metadata=body.get("metadata"),
            )

            if memory:
                self._send_json(200, memory.to_dict())
            else:
                self._send_error(404, "Memory not found")
        else:
            self._send_error(404, "Not found")

    def do_DELETE(self):
        """Handle DELETE requests."""
        parsed = urllib.parse.urlparse(self.path)
        path = parsed.path

        if path == "/memories":
            # Clear all
            count = self.engine.clear()
            self._send_json(200, {"deleted": count})

        elif path.startswith("/memories/"):
            memory_id = path.split("/")[-1]
            success = self.engine.delete(memory_id)

            if success:
                self._send_json(200, {"deleted": True})
            else:
                self._send_error(404, "Memory not found")
        else:
            self._send_error(404, "Not found")

    def _read_body(self) -> dict:
        """Read and parse JSON body."""
        content_length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(content_length).decode()
        return json.loads(body) if body else {}

    def _send_json(self, status: int, data: dict):
        """Send JSON response."""
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(json.dumps(data).encode())

    def _send_error(self, status: int, message: str):
        """Send error response."""
        self._send_json(status, {"error": message})

    def log_message(self, format, *args):
        """Custom logging."""
        pass  # Suppress default logs


def create_app(
    storage_path: str = "memory.db",
    host: str = "127.0.0.1",
    port: int = 8000
) -> HTTPServer:
    """
    Create the API server.

    Args:
        storage_path: Path for memory database
        host: Host to bind to
        port: Port to listen on

    Returns:
        HTTPServer instance
    """
    config = MemoryConfig(storage_path=storage_path)
    engine = MemoryEngine(config)

    MemoryAPI.engine = engine

    server = HTTPServer((host, port), MemoryAPI)
    return server


def run_server(
    storage_path: str = "memory.db",
    host: str = "127.0.0.1",
    port: int = 8000
):
    """Run the API server."""
    server = create_app(storage_path, host, port)
    print(f"Connection-Core API running on http://{host}:{port}")
    print(f"Storage: {storage_path}")
    print("\nEndpoints:")
    print("  GET  /health          - Health check")
    print("  GET  /stats           - Memory statistics")
    print("  GET  /memories        - List/search memories")
    print("  GET  /memories/<id>   - Get specific memory")
    print("  POST /memories        - Create memory")
    print("  POST /recall          - Recall relevant memories")
    print("  PUT  /memories/<id>   - Update memory")
    print("  DELETE /memories/<id> - Delete memory")
    print("  DELETE /memories      - Clear all memories")
    print("\nPress Ctrl+C to stop")

    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
    print("\nServer stopped")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Connection-Core API Server")
    parser.add_argument("--storage", default="memory.db", help="Storage path")
    parser.add_argument("--host", default="127.0.0.1", help="Host")
    parser.add_argument("--port", type=int, default=8000, help="Port")

    args = parser.parse_args()
    run_server(args.storage, args.host, args.port)
