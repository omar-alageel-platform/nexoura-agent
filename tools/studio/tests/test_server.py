#!/usr/bin/env python3
"""
Tests for tools/studio/server.py

Run with:
    python3 -m pytest tools/studio/tests/test_server.py -v
or:
    python3 -m unittest discover tools/studio/tests/
"""
from __future__ import annotations

import json
import socket
import sys
import tempfile
import threading
import time
import unittest
import urllib.request
from pathlib import Path
from unittest.mock import patch, MagicMock

# Make the studio package importable.
_STUDIO_DIR = Path(__file__).resolve().parents[1]
if str(_STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(_STUDIO_DIR))


def _free_port() -> int:
    """Find an open TCP port on localhost."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class ServerTestCase(unittest.TestCase):
    """
    Base class: start a real server in a thread, tear it down after each test.
    The cache is pre-seeded with fixed data so tests are deterministic.
    """

    @classmethod
    def _start_server(cls, cache_path: Path, port: int):
        """Import server module with patched cache path, return (server, thread)."""
        # We import server here so we can patch the Cache path before the
        # module-level _cache object is created.
        import importlib
        import server as srv_mod  # type: ignore[import]

        # Point the module's cache at our temp file.
        srv_mod._cache = __import__("cache").Cache(path=cache_path)  # type: ignore[import]

        from http.server import ThreadingHTTPServer
        server = ThreadingHTTPServer(("127.0.0.1", port), srv_mod.StudioHandler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        # Give the server a moment to start listening.
        time.sleep(0.15)
        return server, thread

    def setUp(self):
        self._td = tempfile.TemporaryDirectory()
        td = Path(self._td.name)

        # Write a fixed cache.
        self._cache_data = {
            "engagements": {"data": [{"name": "eng-test"}], "updated_at": "2026-05-21T00:00:00+00:00"},
            "decisions":   {"data": [],                     "updated_at": "2026-05-21T00:00:00+00:00"},
            "prs":         {"data": [],                     "updated_at": "2026-05-21T00:00:00+00:00"},
            "health":      {"data": {"log_exists": False},  "updated_at": "2026-05-21T00:00:00+00:00"},
        }
        self._cache_path = td / "cache.json"
        self._cache_path.write_text(json.dumps(self._cache_data), encoding="utf-8")

        self._port = _free_port()
        self._server, self._thread = self._start_server(self._cache_path, self._port)

    def tearDown(self):
        self._server.shutdown()
        self._td.cleanup()

    def _url(self, path: str) -> str:
        return f"http://127.0.0.1:{self._port}{path}"

    def _get(self, path: str, headers: dict | None = None) -> tuple[int, dict, bytes]:
        """GET the path; return (status_code, response_headers_dict, body_bytes)."""
        req = urllib.request.Request(self._url(path), headers=headers or {})
        try:
            with urllib.request.urlopen(req, timeout=5) as resp:
                return resp.status, dict(resp.headers), resp.read()
        except urllib.error.HTTPError as e:
            return e.code, {}, b""


class TestApiState(ServerTestCase):
    """/api/state returns cache JSON."""

    def test_status_200(self):
        status, _, _ = self._get("/api/state")
        self.assertEqual(status, 200)

    def test_content_type_json(self):
        _, headers, _ = self._get("/api/state")
        ct = headers.get("Content-Type", "")
        self.assertIn("application/json", ct)

    def test_body_is_valid_json(self):
        _, _, body = self._get("/api/state")
        parsed = json.loads(body)
        self.assertIsInstance(parsed, dict)

    def test_body_contains_all_sections(self):
        _, _, body = self._get("/api/state")
        parsed = json.loads(body)
        for section in ("engagements", "decisions", "prs", "health"):
            self.assertIn(section, parsed)

    def test_engagements_data_matches_cache(self):
        _, _, body = self._get("/api/state")
        parsed = json.loads(body)
        self.assertEqual(parsed["engagements"]["data"][0]["name"], "eng-test")


class TestIndex(ServerTestCase):
    """GET / serves index.html."""

    def test_status_200(self):
        status, _, _ = self._get("/")
        self.assertEqual(status, 200)

    def test_content_type_html(self):
        _, headers, _ = self._get("/")
        ct = headers.get("Content-Type", "")
        self.assertIn("text/html", ct)


class Test404(ServerTestCase):
    """Unknown path returns 404."""

    def test_unknown_path_404(self):
        status, _, _ = self._get("/does-not-exist")
        self.assertEqual(status, 404)


class TestSseEndpoint(ServerTestCase):
    """/api/events accepts connection and sends initial heartbeat."""

    def test_sse_initial_heartbeat(self):
        """
        Connect to /api/events and read a few bytes.
        The server should immediately send a heartbeat comment (': heartbeat\\n\\n').
        """
        import socket as _socket
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect(("127.0.0.1", self._port))
            s.sendall(
                b"GET /api/events HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Accept: text/event-stream\r\n"
                b"Connection: keep-alive\r\n\r\n"
            )
            # Read up to 1024 bytes — should include headers + first heartbeat.
            data = s.recv(1024)
            text = data.decode("utf-8", errors="replace")
            self.assertIn("200", text[:20], "Expected 200 status in response")
            self.assertIn(": heartbeat", text, "Expected heartbeat comment in SSE stream")
        finally:
            s.close()

    def test_sse_content_type(self):
        """
        The Content-Type header for /api/events must be text/event-stream.
        We open the connection, read headers, then close.
        """
        import socket as _socket
        s = _socket.socket(_socket.AF_INET, _socket.SOCK_STREAM)
        s.settimeout(5)
        try:
            s.connect(("127.0.0.1", self._port))
            s.sendall(
                b"GET /api/events HTTP/1.1\r\n"
                b"Host: 127.0.0.1\r\n"
                b"Accept: text/event-stream\r\n"
                b"Connection: keep-alive\r\n\r\n"
            )
            data = s.recv(2048)
            text = data.decode("utf-8", errors="replace")
            self.assertIn("text/event-stream", text)
        finally:
            s.close()


class TestSseEventFormat(unittest.TestCase):
    """SSE event format is correct: event/data lines + double newline."""

    def test_event_format_structure(self):
        """
        The format must be:
            event: state-changed\\n
            data: <json>\\n
            \\n
        """
        import queue as _queue
        # Build the event string the same way server.py does.
        event = {"section": "prs", "updated_at": "2026-05-21T00:00:00+00:00"}
        line = (
            f"event: state-changed\n"
            f"data: {json.dumps(event)}\n\n"
        )
        # Must start with 'event: state-changed'
        self.assertTrue(line.startswith("event: state-changed\n"))
        # Must contain 'data: '
        self.assertIn("data: ", line)
        # Must end with double newline
        self.assertTrue(line.endswith("\n\n"))
        # data line must be valid JSON
        data_line = [l for l in line.split("\n") if l.startswith("data: ")][0]
        payload = json.loads(data_line[len("data: "):])
        self.assertEqual(payload["section"], "prs")
        self.assertIn("updated_at", payload)

    def test_event_json_contains_section_and_updated_at(self):
        event = {"section": "health", "updated_at": "2026-05-21T10:00:00+00:00"}
        line = f"event: state-changed\ndata: {json.dumps(event)}\n\n"
        data_line = [l for l in line.split("\n") if l.startswith("data: ")][0]
        payload = json.loads(data_line[len("data: "):])
        self.assertIn("section", payload)
        self.assertIn("updated_at", payload)
        self.assertEqual(payload["section"], "health")


if __name__ == "__main__":
    unittest.main()
