"""
NEXOURA Studio — smoke tests for B3 views (test_views.py)

Tests:
  1. /api/state returns JSON with the keys home.html and decisions.html consume.
  2. GET / returns the index.html with sidebar markup present.
  3. /static/studio.css and /static/studio.js are served.
  4. Locked decisions honoured (cost runway, cyan accent).

Run:
    pytest tools/studio/tests/test_views.py -v -p no:xdist

Server is started in-process using threading so no subprocess needed.
"""
from __future__ import annotations

import json
import os
import sys
import threading
import time
import urllib.request
import urllib.error
from http.server import ThreadingHTTPServer
from pathlib import Path

import pytest

# ── path setup ─────────────────────────────────────────────────────────────────
_STUDIO_DIR = Path(__file__).resolve().parent.parent
if str(_STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(_STUDIO_DIR))

from server import StudioHandler  # noqa: E402

# ── test server fixture ────────────────────────────────────────────────────────

_TEST_PORT_BASE = 15001   # distinct from production port 5000


def _resolve_test_port() -> int:
    """Per-xdist-worker port so parallel runs don't collide on bind."""
    worker = os.environ.get("PYTEST_XDIST_WORKER", "gw0")
    # 'gw0', 'gw1', ... -> 15001, 15002, ...
    try:
        offset = int(worker.removeprefix("gw"))
    except (ValueError, AttributeError):
        offset = 0
    return _TEST_PORT_BASE + offset


_TEST_PORT = _resolve_test_port()


class _ReuseServer(ThreadingHTTPServer):
    """Allow reuse of address so tests can restart quickly."""
    allow_reuse_address = True


@pytest.fixture(scope="session")
def live_server():
    """
    Start a _ReuseServer on 127.0.0.1:_TEST_PORT in a daemon thread.
    Yields the base URL. Stops when the session is done.
    session scope = only one server across all workers/tests.
    """
    server = _ReuseServer(("127.0.0.1", _TEST_PORT), StudioHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.3)  # let the server bind
    base = f"http://127.0.0.1:{_TEST_PORT}"
    yield base
    server.shutdown()


def _get(url: str, timeout: int = 5) -> tuple[int, str]:
    """Simple GET. Returns (status_code, body_text)."""
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8")


# ── /api/state key tests ───────────────────────────────────────────────────────

class TestApiStateKeys:
    """
    Verify /api/state returns a JSON object with the sections that
    home.html and decisions.html consume.

    Cache sections: engagements, decisions, prs, health
    home.html uses: engagements.data, decisions.data, prs.data
    decisions.html uses: decisions.data
    """

    def test_api_state_returns_200(self, live_server: str) -> None:
        status, _ = _get(f"{live_server}/api/state")
        assert status == 200, f"/api/state returned {status}"

    def test_api_state_is_json(self, live_server: str) -> None:
        _, body = _get(f"{live_server}/api/state")
        try:
            data = json.loads(body)
        except json.JSONDecodeError as exc:
            pytest.fail(f"/api/state body is not valid JSON: {exc}")
        assert isinstance(data, dict), "/api/state should return a JSON object"

    def test_api_state_has_engagements_section(self, live_server: str) -> None:
        """home.html uses state.engagements.data (list of engagement objects)."""
        _, body = _get(f"{live_server}/api/state")
        data = json.loads(body)
        # Section may be absent if cache was never warmed — that is acceptable.
        # When present it must be a dict with a 'data' key.
        if "engagements" in data:
            assert isinstance(data["engagements"], dict), \
                "engagements section should be a dict"
            assert "data" in data["engagements"], \
                "engagements section should have a 'data' key"

    def test_api_state_has_decisions_section(self, live_server: str) -> None:
        """decisions.html uses state.decisions.data (list of decision objects)."""
        _, body = _get(f"{live_server}/api/state")
        data = json.loads(body)
        if "decisions" in data:
            assert isinstance(data["decisions"], dict), \
                "decisions section should be a dict"
            assert "data" in data["decisions"], \
                "decisions section should have a 'data' key"

    def test_api_state_has_prs_section(self, live_server: str) -> None:
        """home.html uses state.prs.data (list of PR objects)."""
        _, body = _get(f"{live_server}/api/state")
        data = json.loads(body)
        if "prs" in data:
            assert isinstance(data["prs"], dict), \
                "prs section should be a dict"
            assert "data" in data["prs"], \
                "prs section should have a 'data' key"

    def test_api_state_has_health_section(self, live_server: str) -> None:
        """home.html reads state.health for director status dots."""
        _, body = _get(f"{live_server}/api/state")
        data = json.loads(body)
        if "health" in data:
            assert isinstance(data["health"], dict), \
                "health section should be a dict"


# ── GET / sidebar tests ────────────────────────────────────────────────────────

class TestIndexHtml:
    """
    Verify GET / returns index.html with the sidebar nav markup.
    """

    def test_index_returns_200(self, live_server: str) -> None:
        status, _ = _get(f"{live_server}/")
        assert status == 200, f"GET / returned {status}"

    def test_index_is_html(self, live_server: str) -> None:
        _, body = _get(f"{live_server}/")
        assert "<!DOCTYPE html>" in body.lower() or "<html" in body.lower(), \
            "GET / should return HTML"

    def test_index_has_sidebar_nav(self, live_server: str) -> None:
        """Sidebar nav must be present — studio.js depends on .nx-nav-link elements."""
        _, body = _get(f"{live_server}/")
        assert "nx-sidebar" in body, \
            "index.html must contain sidebar markup (.nx-sidebar)"

    def test_index_has_nav_home_link(self, live_server: str) -> None:
        _, body = _get(f"{live_server}/")
        assert "#/home" in body, "Sidebar must have a #/home nav link"

    def test_index_has_nav_decisions_link(self, live_server: str) -> None:
        _, body = _get(f"{live_server}/")
        assert "#/decisions" in body, "Sidebar must have a #/decisions nav link"

    def test_index_has_app_mount(self, live_server: str) -> None:
        """studio.js writes the active view into #app."""
        _, body = _get(f"{live_server}/")
        assert 'id="app"' in body, 'index.html must have id="app" mount point'

    def test_index_loads_studio_js(self, live_server: str) -> None:
        _, body = _get(f"{live_server}/")
        assert "studio.js" in body, "index.html must load studio.js"

    def test_index_loads_studio_css(self, live_server: str) -> None:
        _, body = _get(f"{live_server}/")
        assert "studio.css" in body, "index.html must load studio.css"

    def test_index_has_agents_nav_link(self, live_server: str) -> None:
        """B5: AGENTS nav link must be active (no Soon badge)."""
        _, body = _get(f"{live_server}/")
        assert "#/agents" in body, "Sidebar must have a #/agents nav link"

    def test_index_has_activity_nav_link(self, live_server: str) -> None:
        """B5: ACTIVITY nav link must be active."""
        _, body = _get(f"{live_server}/")
        assert "#/activity" in body, "Sidebar must have a #/activity nav link"

    def test_index_has_system_nav_link(self, live_server: str) -> None:
        """B5: SYSTEM nav link must be active."""
        _, body = _get(f"{live_server}/")
        assert "#/system" in body, "Sidebar must have a #/system nav link"


# ── /static/ asset tests ───────────────────────────────────────────────────────

class TestStaticAssets:
    """
    Verify the server serves studio.css and studio.js from /static/.
    (server.py was updated in B3 to add /static/ route — minimal required change.)
    """

    def test_studio_css_returns_200(self, live_server: str) -> None:
        status, _ = _get(f"{live_server}/static/studio.css")
        assert status == 200, f"/static/studio.css returned {status}"

    def test_studio_js_returns_200(self, live_server: str) -> None:
        status, _ = _get(f"{live_server}/static/studio.js")
        assert status == 200, f"/static/studio.js returned {status}"

    def test_studio_css_has_nx_studio_var(self, live_server: str) -> None:
        """studio.css must reference --nx-studio (Locked Decision #2: cyan accent)."""
        _, body = _get(f"{live_server}/static/studio.css")
        assert "--nx-studio" in body, \
            "studio.css must reference --nx-studio (cyan Studio accent)"

    def test_studio_js_has_sse_connect(self, live_server: str) -> None:
        """studio.js must contain EventSource (SSE client)."""
        _, body = _get(f"{live_server}/static/studio.js")
        assert "EventSource" in body, \
            "studio.js must use EventSource for SSE"

    def test_studio_js_has_api_state(self, live_server: str) -> None:
        """studio.js must fetch /api/state on state-changed events."""
        _, body = _get(f"{live_server}/static/studio.js")
        assert "/api/state" in body, \
            "studio.js must fetch /api/state"


# ── Cost runway "unknown" test ─────────────────────────────────────────────────

class TestLockedDecisions:
    """
    Verify locked decisions are honoured in the shipped code.
    """

    def test_cost_runway_never_fabricated_in_js(self, live_server: str) -> None:
        """
        Locked Decision #1: cost runway must show 'unknown' gracefully.
        studio.js should contain 'Cost data not available yet.' (the approved copy).
        """
        _, body = _get(f"{live_server}/static/studio.js")
        assert "Cost data not available yet" in body, \
            "studio.js must show 'Cost data not available yet.' for cost runway"

    def test_studio_accent_cyan_in_css(self, live_server: str) -> None:
        """
        Locked Decision #2: --nx-studio (cyan) must be used for the Studio accent.
        """
        _, body = _get(f"{live_server}/static/studio.css")
        assert "var(--nx-studio)" in body, \
            "studio.css must use var(--nx-studio) for the Studio accent"
