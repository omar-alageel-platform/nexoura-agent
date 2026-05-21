"""
NEXOURA Studio — B4 tests (test_b4.py)

Tests:
  1. /api/artifact rejects path traversal (403)
  2. /api/artifact returns 400 for missing path param
  3. /api/artifact serves a real file (200 + correct Content-Type)
  4. /api/gate/decide writes a JSON file
  5. /api/gate/decide rejects missing engagement_id (400)
  6. /api/gate/decide rejects path-traversal engagement_id (400)
  7. GET /views/projects.html exists and is served (200)
  8. GET /views/artifact.html exists and is served (200)
  9. GET /views/gate-ceremony.html exists and is served (200)
 10. studio.js contains renderProjects
 11. studio.js contains /api/artifact fetch
 12. studio.js contains /api/gate/decide fetch
 13. studio.css contains .projects-* namespace
 14. studio.css contains .artifact-* namespace
 15. studio.css contains .gate-* namespace

Run:
    pytest tools/studio/tests/test_b4.py -v -p no:xdist
"""
from __future__ import annotations

import json
import os
import socket
import sys
import tempfile
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

import server as srv_mod  # noqa: E402  type: ignore[import]


# ── helpers ────────────────────────────────────────────────────────────────────

def _free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


class _ReuseServer(ThreadingHTTPServer):
    allow_reuse_address = True


def _get(url: str, timeout: int = 5) -> tuple[int, str, dict]:
    try:
        with urllib.request.urlopen(url, timeout=timeout) as r:
            hdrs = dict(r.headers)
            return r.status, r.read().decode("utf-8", errors="replace"), hdrs
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace"), {}


def _post(url: str, body: dict, timeout: int = 5) -> tuple[int, str]:
    data = json.dumps(body).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, r.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, e.read().decode("utf-8", errors="replace")


# ── session-scoped server + temp engagements root ──────────────────────────────

@pytest.fixture(scope="session")
def b4_server(tmp_path_factory):
    """
    Start a live server wired to a temp engagements root so we can
    exercise /api/artifact and /api/gate/decide without touching real data.
    """
    td = tmp_path_factory.mktemp("b4_engs")

    # Patch the module-level roots
    orig_eng_root = srv_mod._ENGAGEMENTS_ROOT
    orig_gate_root = srv_mod._GATE_DECISIONS_ROOT
    srv_mod._ENGAGEMENTS_ROOT = td
    srv_mod._GATE_DECISIONS_ROOT = td

    # Create a sample artifact file
    (td / "my-artifact.md").write_text("# Hello\nThis is a test artifact.", encoding="utf-8")
    (td / "image.png").write_bytes(b"\x89PNG\r\n\x1a\n" + b"\x00" * 8)

    port = _free_port()
    server = _ReuseServer(("127.0.0.1", port), srv_mod.StudioHandler)
    t = threading.Thread(target=server.serve_forever, daemon=True)
    t.start()
    time.sleep(0.2)

    base = f"http://127.0.0.1:{port}"
    yield base, td

    server.shutdown()
    srv_mod._ENGAGEMENTS_ROOT = orig_eng_root
    srv_mod._GATE_DECISIONS_ROOT = orig_gate_root


# ── /api/artifact tests ────────────────────────────────────────────────────────

class TestApiArtifact:

    def test_missing_path_param_returns_400(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/api/artifact")
        assert status == 400, f"Expected 400, got {status}"

    def test_path_traversal_rejected_403(self, b4_server):
        base, _ = b4_server
        # Try to escape the engagements root with ../
        status, _, _ = _get(f"{base}/api/artifact?path=../etc/passwd")
        assert status == 403, f"Expected 403 for path traversal, got {status}"

    def test_path_traversal_double_encoded_rejected(self, b4_server):
        base, _ = b4_server
        import urllib.parse
        evil = urllib.parse.quote("../../etc/passwd", safe="")
        status, _, _ = _get(f"{base}/api/artifact?path={evil}")
        # Should be 403 or 404 — either way, not 200
        assert status != 200, f"Path traversal should not return 200, got {status}"

    def test_nonexistent_file_returns_404(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/api/artifact?path=no-such-file.md")
        assert status == 404, f"Expected 404, got {status}"

    def test_existing_md_returns_200_with_text_content_type(self, b4_server):
        base, _ = b4_server
        status, body, hdrs = _get(f"{base}/api/artifact?path=my-artifact.md")
        assert status == 200, f"Expected 200, got {status}"
        ct = hdrs.get("Content-Type", "")
        assert "text/plain" in ct, f"Expected text/plain, got {ct}"
        assert "Hello" in body, "Expected artifact content in body"

    def test_png_returns_image_content_type(self, b4_server):
        base, _ = b4_server
        status, _, hdrs = _get(f"{base}/api/artifact?path=image.png")
        assert status == 200, f"Expected 200, got {status}"
        ct = hdrs.get("Content-Type", "")
        assert "image/png" in ct, f"Expected image/png, got {ct}"


# ── /api/gate/decide tests ─────────────────────────────────────────────────────

class TestApiGateDecide:

    def test_missing_engagement_id_returns_400(self, b4_server):
        base, _ = b4_server
        status, _ = _post(f"{base}/api/gate/decide", {"stage": "S1", "decision": "approve"})
        assert status == 400, f"Expected 400, got {status}"

    def test_path_traversal_engagement_id_rejected(self, b4_server):
        base, _ = b4_server
        status, _ = _post(f"{base}/api/gate/decide", {
            "engagement_id": "../evil",
            "stage": "S1",
            "decision": "approve",
        })
        assert status == 400, f"Expected 400 for traversal engagement_id, got {status}"

    def test_slash_in_engagement_id_rejected(self, b4_server):
        base, _ = b4_server
        status, _ = _post(f"{base}/api/gate/decide", {
            "engagement_id": "a/b",
            "stage": "S1",
            "decision": "approve",
        })
        assert status == 400, f"Expected 400 for slash in engagement_id, got {status}"

    def test_valid_request_writes_file(self, b4_server):
        base, td = b4_server
        status, body = _post(f"{base}/api/gate/decide", {
            "engagement_id": "test-eng",
            "stage": "S2",
            "decision": "approve",
            "rationale": "All deliverables look good.",
        })
        assert status == 200, f"Expected 200, got {status}: {body}"
        resp = json.loads(body)
        assert resp.get("ok") is True, f"Expected ok:true, got {resp}"

        # Verify the file was written
        dec_dir = td / "test-eng" / "decisions"
        assert dec_dir.exists(), "decisions/ directory not created"
        files = list(dec_dir.glob("*.json"))
        assert len(files) >= 1, "No decision file was written"

        record = json.loads(files[0].read_text(encoding="utf-8"))
        assert record["decision"] == "approve"
        assert record["stage"] == "S2"
        assert record["engagement_id"] == "test-eng"

    def test_record_contains_recorded_at(self, b4_server):
        base, td = b4_server
        status, body = _post(f"{base}/api/gate/decide", {
            "engagement_id": "test-eng-ts",
            "stage": "S1",
            "decision": "defer",
            "rationale": "",
        })
        assert status == 200
        dec_dir = td / "test-eng-ts" / "decisions"
        files = list(dec_dir.glob("*.json"))
        assert files, "No file written"
        record = json.loads(files[0].read_text(encoding="utf-8"))
        assert "recorded_at" in record, "record must have recorded_at"


# ── /views/ route tests ────────────────────────────────────────────────────────

class TestViewsRoute:

    def test_projects_html_returns_200(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/views/projects.html")
        assert status == 200, f"/views/projects.html returned {status}"

    def test_projects_html_is_html(self, b4_server):
        base, _ = b4_server
        _, body, hdrs = _get(f"{base}/views/projects.html")
        ct = hdrs.get("Content-Type", "")
        assert "text/html" in ct, f"Expected text/html, got {ct}"
        assert "projects" in body.lower(), "projects.html should mention 'projects'"

    def test_artifact_html_returns_200(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/views/artifact.html")
        assert status == 200, f"/views/artifact.html returned {status}"

    def test_gate_ceremony_html_returns_200(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/views/gate-ceremony.html")
        assert status == 200, f"/views/gate-ceremony.html returned {status}"

    def test_views_traversal_blocked(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/views/../server.py")
        assert status == 404, f"Path traversal in /views/ should be 404, got {status}"

    def test_views_non_html_blocked(self, b4_server):
        base, _ = b4_server
        status, _, _ = _get(f"{base}/views/studio.py")
        assert status == 404, f"Non-html in /views/ should be 404, got {status}"


# ── studio.js B4 additions ─────────────────────────────────────────────────────

class TestStudioJsB4:

    def test_studio_js_has_renderProjects(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "renderProjects" in body, "studio.js must contain renderProjects"

    def test_studio_js_has_api_artifact(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "/api/artifact" in body, "studio.js must fetch /api/artifact"

    def test_studio_js_has_api_gate_decide(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "/api/gate/decide" in body, "studio.js must POST to /api/gate/decide"

    def test_studio_js_has_openGateCeremony(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "openGateCeremony" in body, "studio.js must contain openGateCeremony"

    def test_studio_js_has_openArtifact(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "openArtifact" in body, "studio.js must contain openArtifact"

    def test_studio_js_empty_state_copy(self, b4_server):
        """6th-grade copy: 'No projects yet. Start one to see it here.'"""
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "No projects yet" in body, "studio.js must have empty state copy"

    def test_studio_js_gate_toast_copy(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.js")
        assert "Gate decision recorded" in body, "studio.js must have gate toast copy"


# ── studio.css B4 namespace checks ────────────────────────────────────────────

class TestStudioCssB4:

    def test_css_has_projects_namespace(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.css")
        assert ".projects-" in body, "studio.css must contain .projects-* classes"

    def test_css_has_artifact_namespace(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.css")
        assert ".artifact-" in body, "studio.css must contain .artifact-* classes"

    def test_css_has_gate_namespace(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.css")
        assert ".gate-" in body, "studio.css must contain .gate-* classes"

    def test_css_uses_nx_studio_var_in_b4(self, b4_server):
        base, _ = b4_server
        _, body, _ = _get(f"{base}/static/studio.css")
        # Should appear in B4 sections too
        count = body.count("var(--nx-studio)")
        assert count > 3, f"Expected multiple uses of var(--nx-studio), found {count}"
