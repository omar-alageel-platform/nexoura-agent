#!/usr/bin/env python3
"""
NEXOURA Studio — HTTP server + SSE endpoint (B1).

Routes:
    GET /             → serve tools/studio/index.html
    GET /api/state    → return Cache.read() as JSON (snapshot for page load)
    GET /api/events   → SSE stream; emits 'state-changed' on each cache refresh

Bound to 127.0.0.1:5000 (localhost only — Open Decision #5).

Run:
    python3 tools/studio/server.py

Graceful shutdown on SIGTERM / SIGINT (Ctrl-C).
Stdlib only — no external deps.
"""
from __future__ import annotations

import json
import os
import queue
import signal
import sys
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

# ── Module path setup ─────────────────────────────────────────────────────
# Allow sibling imports (cache, watcher) when run directly.
_STUDIO_DIR = Path(__file__).resolve().parent
if str(_STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(_STUDIO_DIR))

from cache import Cache       # type: ignore[import]
from watcher import FileWatcher  # type: ignore[import]

# ── Global state ──────────────────────────────────────────────────────────

HOST = "127.0.0.1"
PORT = 5000

_cache = Cache()
_event_queue: queue.Queue = queue.Queue()

# Each SSE connection gets its own per-client queue.
# We fan out from _event_queue to all client queues.
_client_queues: list[queue.Queue] = []
_clients_lock = threading.Lock()

_INDEX_PATH = _STUDIO_DIR / "index.html"
_STATIC_DIR = _STUDIO_DIR / "static"

# MIME types for static assets
_MIME = {
    ".css": "text/css; charset=utf-8",
    ".js":  "application/javascript; charset=utf-8",
    ".html": "text/html; charset=utf-8",
}

# Heartbeat interval (seconds) — keeps proxies from closing idle SSE connections.
_HEARTBEAT_INTERVAL = 15


def _fan_out_events() -> None:
    """
    Background thread: reads from the global event queue and copies
    each event to every connected client's queue.
    """
    while True:
        try:
            event = _event_queue.get(timeout=1)
        except queue.Empty:
            continue
        with _clients_lock:
            dead = []
            for cq in _client_queues:
                try:
                    cq.put_nowait(event)
                except queue.Full:
                    dead.append(cq)
            for cq in dead:
                _client_queues.remove(cq)


# ── HTTP request handler ──────────────────────────────────────────────────

class StudioHandler(BaseHTTPRequestHandler):

    def log_message(self, fmt: str, *args) -> None:  # type: ignore[override]
        """Short server log. Easy to read."""
        sys.stderr.write(f"[studio/server] {self.address_string()} {fmt % args}\n")

    # ── routing ──

    def do_GET(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/":
            self._serve_index()
        elif path == "/api/state":
            self._serve_state()
        elif path == "/api/events":
            self._serve_events()
        elif path.startswith("/static/"):
            self._serve_static(path)
        else:
            self._send_404()

    # ── handlers ──

    def _serve_index(self) -> None:
        try:
            body = _INDEX_PATH.read_bytes()
        except OSError:
            body = b"<h1>NEXOURA Studio B1</h1>"
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _serve_static(self, url_path: str) -> None:
        """Serve files from tools/studio/static/. Only serves known extensions."""
        # Strip /static/ prefix and resolve to the static dir
        rel = url_path[len("/static/"):]
        file_path = (_STATIC_DIR / rel).resolve()
        # Security: must be under _STATIC_DIR
        try:
            file_path.relative_to(_STATIC_DIR.resolve())
        except ValueError:
            self._send_404()
            return
        suffix = file_path.suffix
        if suffix not in _MIME:
            self._send_404()
            return
        try:
            body = file_path.read_bytes()
        except OSError:
            self._send_404()
            return
        self.send_response(200)
        self.send_header("Content-Type", _MIME[suffix])
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _serve_state(self) -> None:
        data = _cache.read()
        body = json.dumps(data, indent=2, default=str).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _serve_events(self) -> None:
        """SSE stream. Stays open until the client disconnects."""
        self.send_response(200)
        self.send_header("Content-Type", "text/event-stream")
        self.send_header("Cache-Control", "no-cache")
        self.send_header("Connection", "keep-alive")
        self.send_header("X-Accel-Buffering", "no")
        self.end_headers()

        # Register this client.
        client_q: queue.Queue = queue.Queue(maxsize=50)
        with _clients_lock:
            _client_queues.append(client_q)

        def _write(data: bytes) -> bool:
            """Write bytes; return False if client disconnected."""
            try:
                self.wfile.write(data)
                self.wfile.flush()
                return True
            except (BrokenPipeError, ConnectionResetError, OSError):
                return False

        try:
            # Send an initial heartbeat so the client knows the stream is alive.
            if not _write(b": heartbeat\n\n"):
                return

            last_heartbeat = time.monotonic()

            while True:
                # Wait up to 1s for an event so we can send periodic heartbeats.
                try:
                    event = client_q.get(timeout=1.0)
                    line = (
                        f"event: state-changed\n"
                        f"data: {json.dumps(event)}\n\n"
                    ).encode("utf-8")
                    if not _write(line):
                        return
                    last_heartbeat = time.monotonic()
                except queue.Empty:
                    pass

                now = time.monotonic()
                if now - last_heartbeat >= _HEARTBEAT_INTERVAL:
                    if not _write(b": heartbeat\n\n"):
                        return
                    last_heartbeat = now

        finally:
            with _clients_lock:
                if client_q in _client_queues:
                    _client_queues.remove(client_q)

    def _send_404(self) -> None:
        body = b"Not found"
        self.send_response(404)
        self.send_header("Content-Type", "text/plain")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


# ── Server startup ────────────────────────────────────────────────────────

def run(host: str = HOST, port: int = PORT) -> None:
    """Start the watcher, fan-out thread, then serve forever."""

    # Initial cache warm-up so /api/state is useful right away.
    print(f"[studio/server] Warming up cache...")
    _cache.refresh_all()

    # File-watcher in background threads.
    watcher = FileWatcher(_cache, _event_queue)
    watcher.start_background()
    print("[studio/server] File watcher started.")

    # Fan-out thread: distributes events to per-client queues.
    fan_out_thread = threading.Thread(target=_fan_out_events, daemon=True, name="fan-out")
    fan_out_thread.start()

    server = ThreadingHTTPServer((host, port), StudioHandler)

    def _shutdown(sig, frame):
        print(f"\n[studio/server] Shutting down (signal {sig})...")
        watcher.stop()
        threading.Thread(target=server.shutdown, daemon=True).start()

    signal.signal(signal.SIGTERM, _shutdown)
    signal.signal(signal.SIGINT, _shutdown)

    print(f"[studio/server] Listening on http://{host}:{port}/")
    print(f"[studio/server] State: http://{host}:{port}/api/state")
    print(f"[studio/server] Events: http://{host}:{port}/api/events")
    server.serve_forever()


if __name__ == "__main__":
    run()
