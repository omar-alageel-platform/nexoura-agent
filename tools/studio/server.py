#!/usr/bin/env python3
"""
NEXOURA Studio — HTTP server + SSE endpoint (B1).

Routes:
    GET /                   → serve tools/studio/index.html
    GET /api/state          → return Cache.read() as JSON (snapshot for page load)
    GET /api/events         → SSE stream; emits 'state-changed' on each cache refresh
    GET /views/<name>.html  → serve tools/studio/views/<name>.html (B4)
    GET /api/artifact       → serve artifact files under nexoura-engagements/ (B4)
    POST /api/gate/decide   → write a gate decision JSON record (B4)

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
from datetime import datetime, timezone
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse, parse_qs

# ── Module path setup ─────────────────────────────────────────────────────
# Allow sibling imports (cache, watcher) when run directly.
_STUDIO_DIR = Path(__file__).resolve().parent
if str(_STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(_STUDIO_DIR))

from cache import Cache       # type: ignore[import]
from watcher import FileWatcher  # type: ignore[import]

# ── Global state ──────────────────────────────────────────────────────

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
_VIEWS_DIR  = _STUDIO_DIR / "views"

# Root for artifact file serving (B4) — path traversal is validated server-side.
_ENGAGEMENTS_ROOT = Path("/home/omar/dev/nexoura-engagements")

# Root for gate decision records (B4)
_GATE_DECISIONS_ROOT = _ENGAGEMENTS_ROOT

# Root for director/agent profile SOULs (B5)
_PROFILES_DIR = _STUDIO_DIR.parents[1] / "profiles"

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
        elif path.startswith("/views/"):
            self._serve_view(path)
        elif path == "/api/artifact":
            self._serve_artifact()
        elif path.startswith("/api/profile/"):
            self._serve_profile(path)
        else:
            self._send_404()

    def do_POST(self) -> None:
        path = self.path.split("?", 1)[0]
        if path == "/api/gate/decide":
            self._handle_gate_decide()
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

    def _serve_view(self, url_path: str) -> None:
        """Serve view HTML fragments from tools/studio/views/."""
        rel = url_path[len("/views/"):]
        file_path = (_VIEWS_DIR / rel).resolve()
        try:
            file_path.relative_to(_VIEWS_DIR.resolve())
        except ValueError:
            self._send_404()
            return
        if file_path.suffix != ".html":
            self._send_404()
            return
        try:
            body = file_path.read_bytes()
        except OSError:
            self._send_404()
            return
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    def _serve_profile(self, url_path: str) -> None:
        """
        GET /api/profile/<slug>
        Return JSON: { soul: <first 800 chars>, dispatches: [...], memory: <str|null> }
        """
        import sqlite3 as _sqlite3
        slug = url_path[len("/api/profile/"):]
        # Security: slug must be simple identifier
        import re as _re
        if not _re.match(r"^[a-z0-9][a-z0-9\-]{0,63}$", slug):
            self._send_404()
            return
        profile_dir = (_PROFILES_DIR / slug).resolve()
        try:
            profile_dir.relative_to(_PROFILES_DIR.resolve())
        except ValueError:
            self._send_404()
            return
        # Profile must exist as a directory containing SOUL.md
        if not (profile_dir.is_dir() and (profile_dir / "SOUL.md").exists()):
            self._send_404()
            return

        soul_text: str | None = None
        soul_path = profile_dir / "SOUL.md"
        if soul_path.exists():
            try:
                soul_text = soul_path.read_text(encoding="utf-8", errors="replace")[:800]
            except OSError:
                soul_text = None

        memory_text: str | None = None
        memory_path = profile_dir / "MEMORY.md"
        if memory_path.exists():
            try:
                memory_text = memory_path.read_text(encoding="utf-8", errors="replace")[:400]
            except OSError:
                pass

        # Last 5 dispatches from state.db where title contains slug
        dispatches: list[dict] = []
        state_db = Path.home() / ".hermes" / "state.db"
        if state_db.exists():
            try:
                conn = _sqlite3.connect(str(state_db), timeout=3)
                cur = conn.cursor()
                cur.execute(
                    "SELECT id, started_at, estimated_cost_usd, end_reason "
                    "FROM sessions WHERE (title LIKE ? OR id LIKE ?) "
                    "ORDER BY started_at DESC LIMIT 5",
                    (f"%{slug}%", f"%{slug}%"),
                )
                for row in cur.fetchall():
                    dispatches.append({
                        "id": row[0],
                        "started_at": row[1],
                        "estimated_cost_usd": row[2],
                        "outcome": row[3],
                    })
                conn.close()
            except Exception:
                pass

        payload = {"soul": soul_text, "dispatches": dispatches, "memory": memory_text}
        body = json.dumps(payload, default=str).encode("utf-8")
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

    # ── B4: artifact handler ───────────────────────────────────────────────

    _ARTIFACT_MIME = {
        ".html": "text/html; charset=utf-8",
        ".htm":  "text/html; charset=utf-8",
        ".md":   "text/plain; charset=utf-8",
        ".txt":  "text/plain; charset=utf-8",
        ".png":  "image/png",
        ".jpg":  "image/jpeg",
        ".jpeg": "image/jpeg",
    }

    def _serve_artifact(self) -> None:
        """
        GET /api/artifact?path=<relative-path>
        Serves files under _ENGAGEMENTS_ROOT. Rejects path traversal.
        """
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        rel_parts = qs.get("path", [])
        if not rel_parts:
            self._send_error(400, b"Missing path parameter.")
            return
        rel = rel_parts[0].lstrip("/")
        candidate = (_ENGAGEMENTS_ROOT / rel).resolve()
        try:
            candidate.relative_to(_ENGAGEMENTS_ROOT.resolve())
        except ValueError:
            self._send_error(403, b"Path not allowed.")
            return
        if not candidate.exists() or not candidate.is_file():
            self._send_404()
            return
        mime = self._ARTIFACT_MIME.get(candidate.suffix.lower(), "application/octet-stream")
        try:
            body = candidate.read_bytes()
        except OSError:
            self._send_error(500, b"Could not read file.")
            return
        self.send_response(200)
        self.send_header("Content-Type", mime)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(body)

    # ── B4: gate/decide handler ────────────────────────────────────────────

    def _handle_gate_decide(self) -> None:
        """
        POST /api/gate/decide
        Writes a JSON decision record to:
            _ENGAGEMENTS_ROOT/<engagement_id>/decisions/<timestamp>.json
        No git commit — the file watcher picks it up.
        """
        try:
            length = int(self.headers.get("Content-Length", 0))
        except (TypeError, ValueError):
            length = 0
        raw = self.rfile.read(length) if length > 0 else b"{}"
        try:
            payload = json.loads(raw.decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError):
            self._send_error(400, b"Invalid JSON body.")
            return

        eng_id = str(payload.get("engagement_id", "")).strip()
        if not eng_id:
            self._send_error(400, b"Missing engagement_id.")
            return

        # Validate engagement_id is a safe directory name (no slashes, no ..)
        if "/" in eng_id or "\\" in eng_id or ".." in eng_id:
            self._send_error(400, b"Invalid engagement_id.")
            return

        decisions_dir = _ENGAGEMENTS_ROOT / eng_id / "decisions"
        try:
            decisions_dir.mkdir(parents=True, exist_ok=True)
        except OSError:
            self._send_error(500, b"Could not create decisions directory.")
            return

        ts = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")
        record_path = decisions_dir / f"{ts}.json"
        record = {
            "engagement_id": eng_id,
            "stage":         payload.get("stage", ""),
            "decision":      payload.get("decision", ""),
            "rationale":     payload.get("rationale", ""),
            "note":          payload.get("note", ""),
            "recorded_at":   datetime.now(timezone.utc).isoformat(),
        }
        try:
            record_path.write_text(
                json.dumps(record, indent=2, default=str),
                encoding="utf-8",
            )
        except OSError:
            self._send_error(500, b"Could not write decision record.")
            return

        resp = json.dumps({"ok": True, "path": str(record_path)}).encode("utf-8")
        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(resp)))
        self.end_headers()
        self.wfile.write(resp)

    def _send_error(self, code: int, body: bytes) -> None:
        self.send_response(code)
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
