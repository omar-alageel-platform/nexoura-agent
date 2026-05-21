#!/usr/bin/env python3
"""
Tests for tools/studio/cache.py

Run with:
    python3 -m pytest tools/studio/tests/test_cache.py -v
or:
    python3 -m unittest discover tools/studio/tests/
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock

# Make the studio package importable.
_STUDIO_DIR = Path(__file__).resolve().parents[1]
if str(_STUDIO_DIR) not in sys.path:
    sys.path.insert(0, str(_STUDIO_DIR))

from cache import Cache  # type: ignore[import]
import cache as cache_mod  # type: ignore[import]


class TestCacheRead(unittest.TestCase):
    """Cache.read() behaviour."""

    def test_read_returns_empty_when_file_missing(self):
        with tempfile.TemporaryDirectory() as td:
            cache = Cache(path=Path(td) / "nonexistent" / "cache.json")
            result = cache.read()
            self.assertEqual(result, {})

    def test_read_returns_empty_on_invalid_json(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "cache.json"
            p.write_text("NOT JSON", encoding="utf-8")
            cache = Cache(path=p)
            result = cache.read()
            self.assertEqual(result, {})

    def test_read_returns_dict_on_valid_file(self):
        with tempfile.TemporaryDirectory() as td:
            p = Path(td) / "cache.json"
            p.write_text(json.dumps({"engagements": {"data": [], "updated_at": "x"}}), encoding="utf-8")
            cache = Cache(path=p)
            result = cache.read()
            self.assertIn("engagements", result)


class TestCacheRefreshAll(unittest.TestCase):
    """Cache.refresh_all() writes JSON with all four sections."""

    def _mock_collectors(self):
        return {
            "get_active_engagements": MagicMock(return_value=[{"name": "eng-a"}]),
            "get_pending_decisions": MagicMock(return_value=[]),
            "get_recent_prs":        MagicMock(return_value=[]),
            "get_system_health":     MagicMock(return_value={"gateway": {"status": "OK"}}),
        }

    def test_refresh_all_writes_four_sections(self):
        with tempfile.TemporaryDirectory() as td:
            cache_path = Path(td) / "cache.json"
            cache = Cache(path=cache_path)

            mocks = self._mock_collectors()
            import cache as cache_mod
            with (
                patch.object(cache_mod, "get_active_engagements", mocks["get_active_engagements"]),
                patch.object(cache_mod, "get_pending_decisions",   mocks["get_pending_decisions"]),
                patch.object(cache_mod, "get_recent_prs",          mocks["get_recent_prs"]),
                patch.object(cache_mod, "get_system_health",        mocks["get_system_health"]),
            ):
                cache.refresh_all()

            self.assertTrue(cache_path.exists(), "cache.json not created")
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            for section in ("engagements", "decisions", "prs", "health"):
                self.assertIn(section, data, f"Section '{section}' missing")
                self.assertIn("updated_at", data[section], f"'{section}' missing updated_at")
                self.assertIn("data", data[section], f"'{section}' missing data key")

    def test_refresh_all_calls_each_collector_once(self):
        with tempfile.TemporaryDirectory() as td:
            cache = Cache(path=Path(td) / "cache.json")
            mocks = self._mock_collectors()
            import cache as cache_mod
            with (
                patch.object(cache_mod, "get_active_engagements", mocks["get_active_engagements"]),
                patch.object(cache_mod, "get_pending_decisions",   mocks["get_pending_decisions"]),
                patch.object(cache_mod, "get_recent_prs",          mocks["get_recent_prs"]),
                patch.object(cache_mod, "get_system_health",        mocks["get_system_health"]),
            ):
                cache.refresh_all()
                mocks["get_active_engagements"].assert_called_once()
                mocks["get_recent_prs"].assert_called_once()
                mocks["get_system_health"].assert_called_once()


class TestCacheRefreshSection(unittest.TestCase):
    """Cache.refresh(section) updates only that section."""

    def test_refresh_single_section_only_touches_that_section(self):
        with tempfile.TemporaryDirectory() as td:
            cache_path = Path(td) / "cache.json"
            # Pre-populate with all four sections.
            initial = {
                "engagements": {"data": ["old"], "updated_at": "2000-01-01T00:00:00+00:00"},
                "decisions":   {"data": [],       "updated_at": "2000-01-01T00:00:00+00:00"},
                "prs":         {"data": [],       "updated_at": "2000-01-01T00:00:00+00:00"},
                "health":      {"data": {},       "updated_at": "2000-01-01T00:00:00+00:00"},
            }
            cache_path.write_text(json.dumps(initial), encoding="utf-8")
            cache = Cache(path=cache_path)

            import cache as cache_mod
            with patch.object(cache_mod, "get_system_health", return_value={"gateway": {"status": "UP"}}):
                cache.refresh("health")

            data = json.loads(cache_path.read_text(encoding="utf-8"))
            # health updated
            self.assertNotEqual(data["health"]["updated_at"], "2000-01-01T00:00:00+00:00")
            self.assertEqual(data["health"]["data"]["gateway"]["status"], "UP")
            # others unchanged
            self.assertEqual(data["engagements"]["data"], ["old"])
            self.assertEqual(data["engagements"]["updated_at"], "2000-01-01T00:00:00+00:00")

    def test_refresh_unknown_section_does_not_crash(self):
        with tempfile.TemporaryDirectory() as td:
            cache = Cache(path=Path(td) / "cache.json")
            # Should not raise.
            cache.refresh("nonexistent_section")


class TestCacheExceptionHandling(unittest.TestCase):
    """Collector exception keeps old data; does not crash."""

    def test_collector_exception_preserves_old_data(self):
        with tempfile.TemporaryDirectory() as td:
            cache_path = Path(td) / "cache.json"
            old_data = {
                "prs": {"data": [{"title": "old PR"}], "updated_at": "2000-01-01T00:00:00+00:00"},
            }
            cache_path.write_text(json.dumps(old_data), encoding="utf-8")
            cache = Cache(path=cache_path)

            import cache as cache_mod
            with patch.object(cache_mod, "get_recent_prs", side_effect=RuntimeError("gh down")):
                cache.refresh("prs")  # Must not raise.

            data = json.loads(cache_path.read_text(encoding="utf-8"))
            # Old data is preserved.
            self.assertEqual(data["prs"]["data"][0]["title"], "old PR")


class TestLastUpdated(unittest.TestCase):
    """Cache.last_updated() returns the ISO timestamp or None."""

    def test_last_updated_returns_timestamp(self):
        with tempfile.TemporaryDirectory() as td:
            cache_path = Path(td) / "cache.json"
            cache_path.write_text(
                json.dumps({"prs": {"data": [], "updated_at": "2026-01-01T00:00:00+00:00"}}),
                encoding="utf-8",
            )
            cache = Cache(path=cache_path)
            self.assertEqual(cache.last_updated("prs"), "2026-01-01T00:00:00+00:00")

    def test_last_updated_returns_none_when_missing(self):
        with tempfile.TemporaryDirectory() as td:
            cache = Cache(path=Path(td) / "cache.json")
            self.assertIsNone(cache.last_updated("prs"))


# ── B5: Agent activity tests ───────────────────────────────────────────────


class TestGetAgentActivityReturnThreeKeys(unittest.TestCase):
    """get_agent_activity() always returns active, available, idle keys."""

    def test_returns_three_keys(self):
        result = cache_mod.get_agent_activity()
        self.assertIn("active",    result, "Missing 'active' key")
        self.assertIn("available", result, "Missing 'available' key")
        self.assertIn("idle",      result, "Missing 'idle' key")

    def test_all_values_are_lists(self):
        result = cache_mod.get_agent_activity()
        self.assertIsInstance(result["active"],    list)
        self.assertIsInstance(result["available"], list)
        self.assertIsInstance(result["idle"],      list)

    def test_all_profiles_have_slug_key(self):
        result = cache_mod.get_agent_activity()
        for zone in ("active", "available", "idle"):
            for entry in result[zone]:
                self.assertIn("slug", entry, f"Entry in '{zone}' missing 'slug': {entry}")


class TestGetAgentActivityGracefulWhenStateDbMissing(unittest.TestCase):
    """When state.db is missing, all profiles go to 'available'."""

    def test_graceful_degradation(self):
        import tempfile as _tmp
        with _tmp.TemporaryDirectory() as fake_home:
            # Point home to a dir without state.db
            with patch.dict("os.environ", {"HOME": fake_home}):
                from pathlib import Path as _P
                fake_db = _P(fake_home) / ".hermes" / "state.db"
                self.assertFalse(fake_db.exists(), "state.db should not exist in fake home")
                # Call with a patched STATE_DB path that doesn't exist
                with patch.object(cache_mod, "get_agent_activity",
                                  wraps=cache_mod.get_agent_activity):
                    # We test directly: monkeypatch the DB path
                    original = cache_mod.Path.home
                    try:
                        cache_mod.Path.home = staticmethod(lambda: _P(fake_home))
                        result = cache_mod.get_agent_activity()
                    finally:
                        cache_mod.Path.home = original
                # Either graceful (no crash) or all in available
                self.assertIsInstance(result, dict)
                self.assertIn("active",    result)
                self.assertIn("available", result)
                self.assertIn("idle",      result)
                # When DB is missing, nothing should be in active
                self.assertEqual(result["active"], [])

    def test_no_crash_on_missing_db(self):
        """get_agent_activity() must never raise — only return safe defaults."""
        import tempfile as _tmp
        with _tmp.TemporaryDirectory() as fake_home:
            from pathlib import Path as _P
            orig = cache_mod.Path.home
            try:
                cache_mod.Path.home = staticmethod(lambda: _P(fake_home))
                result = cache_mod.get_agent_activity()
            except Exception as exc:
                self.fail(f"get_agent_activity raised unexpectedly: {exc}")
            finally:
                cache_mod.Path.home = orig
            self.assertIsInstance(result, dict)


class TestCacheAgentsSection(unittest.TestCase):
    """Cache.refresh('agents') adds 'agents' section with data + updated_at."""

    def test_refresh_agents_section(self):
        with tempfile.TemporaryDirectory() as td:
            cache_path = Path(td) / "cache.json"
            cache = Cache(path=cache_path)
            mock_result = {"active": [], "available": [{"slug": "test"}], "idle": []}
            with patch.object(cache_mod, "get_agent_activity", return_value=mock_result):
                cache.refresh("agents")
            data = json.loads(cache_path.read_text(encoding="utf-8"))
            self.assertIn("agents", data)
            self.assertIn("updated_at", data["agents"])
            self.assertEqual(data["agents"]["data"]["available"][0]["slug"], "test")


if __name__ == "__main__":
    unittest.main()
