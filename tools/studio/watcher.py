#!/usr/bin/env python3
"""
NEXOURA Studio — file-watcher bridge (B1).

Watches key paths for changes and tells the cache to refresh.
When the cache refreshes, it puts an event on a queue so the
SSE handler can push it to every connected browser.

Choice: stdlib polling (no inotify_simple dep).
Why: inotify_simple is not in stdlib. Adding it would break the
"stdlib only" rule. The ctypes wrapper route works but adds ~100 LOC
of fragile low-level code. Polling every 2 seconds is simple,
correct, and good enough for a local dev tool.

inotify reliability note:
- inotify works only on local Linux filesystems (ext4, btrfs, etc.).
- It fails silently on NFS, CIFS/Samba, and FUSE mounts.
- /home/omar/dev/ is on local ext4, so inotify would work there.
- But if the engagements root ever moves to a network mount, inotify
  would stop firing. Polling is immune to that problem.
- If lower latency (< 1s) is needed in a future sprint, a thin
  ctypes wrapper around IN_CLOSE_WRITE / IN_CREATE / IN_MODIFY
  can replace the polling loop here. The queue contract stays the same.

Stdlib only — no external deps.
"""
from __future__ import annotations

import queue
import sys
import threading
import time
import os
from datetime import datetime, timezone
from pathlib import Path

# Keep a reference to the cache module sibling without a package import.
# The server imports this module after appending the studio dir to sys.path.
from cache import Cache  # type: ignore[import]

# ── Paths to watch ────────────────────────────────────────────────────────

_ENGAGEMENTS_ROOT = Path("/home/omar/dev/nexoura-engagements")
_WATCHDOG_LOG = Path.home() / ".hermes" / "watchdog.log"

# How often to poll filesystem paths (seconds).
_POLL_INTERVAL = 2.0

# How often to refresh PRs via gh CLI (seconds).
_PR_INTERVAL = 60.0


def _preview_decisions_dir() -> Path:
    """Return the decisions dir. Reads NEXOURA_PREVIEW_DIR env each call."""
    base = Path(
        os.environ.get(
            "NEXOURA_PREVIEW_DIR",
            "/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview",
        )
    ).expanduser()
    return base / "decisions"


# ── Snapshot helpers ──────────────────────────────────────────────────────

def _dir_snapshot(path: Path) -> dict[str, float]:
    """
    Walk a directory tree and record (path -> mtime) for every file.
    Returns {} if the directory does not exist.
    Fast enough for small trees (dozens of files).
    """
    snap: dict[str, float] = {}
    if not path.exists():
        return snap
    try:
        for root, _dirs, files in os.walk(str(path)):
            for name in files:
                fp = Path(root) / name
                try:
                    snap[str(fp)] = fp.stat().st_mtime
                except OSError:
                    pass
    except OSError:
        pass
    return snap


def _file_mtime(path: Path) -> float:
    """Return file mtime, or 0.0 if missing."""
    try:
        return path.stat().st_mtime
    except OSError:
        return 0.0


def _changed(old: dict[str, float], new: dict[str, float]) -> bool:
    return old != new


# ── Watcher threads ───────────────────────────────────────────────────────

class FileWatcher:
    """
    Polls filesystem paths and triggers Cache.refresh(section).
    Puts a dict onto event_queue for each refresh so the SSE
    handler can push it to the browser.

    event_queue items look like:
        {"section": "engagements", "updated_at": "2026-05-21T10:00:00+00:00"}
    """

    def __init__(self, cache: Cache, event_queue: queue.Queue) -> None:
        self._cache = cache
        self._q = event_queue
        self._stop = threading.Event()

    def stop(self) -> None:
        self._stop.set()

    def _refresh(self, section: str) -> None:
        """Refresh one section and push an event."""
        self._cache.refresh(section)
        self._q.put({
            "section": section,
            "updated_at": datetime.now(timezone.utc).isoformat(),
        })

    def _watch_engagements(self) -> None:
        """Poll engagements root for new commits or stage markers."""
        # Track .git/HEAD mtime for every engagement dir + stage marker files.
        prev_snap: dict[str, float] = {}

        def _eng_snapshot() -> dict[str, float]:
            snap: dict[str, float] = {}
            if not _ENGAGEMENTS_ROOT.exists():
                return snap
            try:
                for child in _ENGAGEMENTS_ROOT.iterdir():
                    git_head = child / ".git" / "HEAD"
                    if git_head.exists():
                        snap[str(git_head)] = _file_mtime(git_head)
                    nexoura_dir = child / ".nexoura"
                    snap.update(_dir_snapshot(nexoura_dir))
            except OSError:
                pass
            return snap

        prev_snap = _eng_snapshot()
        while not self._stop.wait(_POLL_INTERVAL):
            new_snap = _eng_snapshot()
            if _changed(prev_snap, new_snap):
                prev_snap = new_snap
                try:
                    self._refresh("engagements")
                except Exception as exc:
                    print(f"[studio/watcher] engagements refresh error: {exc}", file=sys.stderr)

    def _watch_decisions(self) -> None:
        """Poll decisions dir for new or changed HTML files."""
        prev_snap: dict[str, float] = {}

        while not self._stop.wait(_POLL_INTERVAL):
            decisions_dir = _preview_decisions_dir()
            new_snap = _dir_snapshot(decisions_dir)
            if _changed(prev_snap, new_snap):
                prev_snap = new_snap
                try:
                    self._refresh("decisions")
                except Exception as exc:
                    print(f"[studio/watcher] decisions refresh error: {exc}", file=sys.stderr)

    def _watch_health(self) -> None:
        """Poll watchdog.log mtime."""
        prev_mtime = _file_mtime(_WATCHDOG_LOG)

        while not self._stop.wait(_POLL_INTERVAL):
            new_mtime = _file_mtime(_WATCHDOG_LOG)
            if new_mtime != prev_mtime:
                prev_mtime = new_mtime
                try:
                    self._refresh("health")
                except Exception as exc:
                    print(f"[studio/watcher] health refresh error: {exc}", file=sys.stderr)

    def _watch_prs(self) -> None:
        """Refresh PRs every 60 seconds (gh CLI — cannot be inotified)."""
        while not self._stop.wait(_PR_INTERVAL):
            try:
                self._refresh("prs")
            except Exception as exc:
                print(f"[studio/watcher] prs refresh error: {exc}", file=sys.stderr)

    def start_background(self) -> list[threading.Thread]:
        """Spawn all watcher threads as daemons. Return thread list."""
        threads = []
        for target in (
            self._watch_engagements,
            self._watch_decisions,
            self._watch_health,
            self._watch_prs,
        ):
            t = threading.Thread(target=target, daemon=True, name=f"watcher-{target.__name__}")
            t.start()
            threads.append(t)
        return threads
