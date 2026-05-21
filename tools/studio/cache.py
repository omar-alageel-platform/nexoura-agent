#!/usr/bin/env python3
"""
NEXOURA Studio — cache layer (B1).

Wraps the four PM-Console data collectors in a persistent JSON cache.
Cache file lives at ~/.hermes/nexoura-studio/cache.json.

Each section has its own 'updated_at' ISO timestamp so the SSE endpoint
can tell the browser exactly which part changed.

On any collector error the section keeps its old data. The error is
printed to stderr. The server keeps running.

Usage (CLI smoke-test):
    python3 tools/studio/cache.py --refresh-all
    python3 tools/studio/cache.py --refresh engagements
    python3 tools/studio/cache.py --refresh decisions
    python3 tools/studio/cache.py --refresh prs
    python3 tools/studio/cache.py --refresh health

Stdlib only — no external deps.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ── Constants (ported verbatim from tools/pm-console/generate.py) ─────────

DEFAULT_PREVIEW_DIR = "/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview"
ENGAGEMENTS_ROOT = Path("/home/omar/dev/nexoura-engagements")
AGENT_REPO = "omar-alageel-platform/nexoura-agent"
WATCHDOG_LOG = Path.home() / ".hermes" / "watchdog.log"

NEXOURA_STAGES = [
    "requirements", "feasibility", "branding", "tech-architecture",
    "implementation", "gtm-marketing", "operations", "gate-review", "live",
]

CACHE_PATH = Path.home() / ".hermes" / "nexoura-studio" / "cache.json"

# ── Low-level helpers (ported verbatim) ───────────────────────────────────

def _run(cmd: list[str], cwd: Path | None = None, timeout: int = 15) -> tuple[int, str, str]:
    """Run a subprocess. Return (rc, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True,
            timeout=timeout, check=False,
        )
        return p.returncode, p.stdout, p.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 127, "", str(e)


def _iso_to_dt(s: str) -> datetime | None:
    if not s:
        return None
    try:
        return datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        return None


def _humanize_age(dt: datetime) -> str:
    now = datetime.now(timezone.utc)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    delta = now - dt
    secs = int(delta.total_seconds())
    if secs < 60:
        return f"{secs}s ago"
    if secs < 3600:
        return f"{secs // 60}m ago"
    if secs < 86400:
        return f"{secs // 3600}h ago"
    return f"{secs // 86400}d ago"


def _gh_prs(repo: str) -> list[dict]:
    rc, stdout, _ = _run([
        "gh", "pr", "list", "--repo", repo,
        "--state", "all", "--limit", "20",
        "--json", "number,title,state,createdAt,mergedAt,url",
    ], timeout=20)
    if rc != 0 or not stdout.strip():
        return []
    try:
        return json.loads(stdout)
    except json.JSONDecodeError:
        return []


# ── Data collectors (ported verbatim, signatures preserved) ───────────────

def get_active_engagements() -> list[dict]:
    """Scan ENGAGEMENTS_ROOT for git repos; return list of engagement dicts."""
    out: list[dict] = []
    if not ENGAGEMENTS_ROOT.exists() or not ENGAGEMENTS_ROOT.is_dir():
        return out
    for child in sorted(ENGAGEMENTS_ROOT.iterdir()):
        if not (child / ".git").exists():
            continue
        commits = []
        rc, stdout, _ = _run(
            ["git", "log", "-5", "--pretty=format:%h|%an|%at|%s"],
            cwd=child,
        )
        if rc == 0 and stdout.strip():
            for line in stdout.strip().splitlines():
                parts = line.split("|", 3)
                if len(parts) != 4:
                    continue
                sha, author, ts, msg = parts
                try:
                    dt = datetime.fromtimestamp(int(ts), tz=timezone.utc)
                    age = _humanize_age(dt)
                except (ValueError, OSError):
                    age = ""
                commits.append({"sha": sha, "author": author, "age": age, "message": msg})

        stage_idx = 0
        current_stage = NEXOURA_STAGES[0]
        for i, st in enumerate(NEXOURA_STAGES):
            if (child / f"docs/{st}").exists() or (child / f".nexoura/{st}.done").exists():
                stage_idx = i
                current_stage = st
        out.append({
            "name": child.name,
            "stage_index": stage_idx,
            "stage_total": len(NEXOURA_STAGES),
            "current_stage": current_stage,
            "commits": commits,
        })
    return out


def get_pending_decisions(preview_dir: Path) -> list[dict]:
    """Glob $preview/decisions/*.html and parse <title>."""
    out: list[dict] = []
    decisions_dir = preview_dir / "decisions"
    if not decisions_dir.exists():
        return out
    title_re = re.compile(r"<title[^>]*>(.*?)</title>", re.IGNORECASE | re.DOTALL)
    entries = []
    for f in decisions_dir.glob("*.html"):
        try:
            text = f.read_text(encoding="utf-8", errors="replace")
        except OSError:
            continue
        m = title_re.search(text)
        title = m.group(1).strip() if m else f.name
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=timezone.utc)
        entries.append({
            "title": title,
            "age": _humanize_age(mtime),
            "mtime": mtime,
            "path": str(f),
            "url": f"file://{f}",
        })
    entries.sort(key=lambda e: e["mtime"])
    for e in entries:
        e.pop("mtime", None)
        out.append(e)
    return out


def get_recent_prs() -> list[dict]:
    """Recent PRs (last 24h created OR merged) across nexoura-agent + engagement repos."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    repos = [AGENT_REPO]
    if ENGAGEMENTS_ROOT.exists():
        for child in ENGAGEMENTS_ROOT.iterdir():
            if not (child / ".git").exists():
                continue
            rc, stdout, _ = _run(["git", "-C", str(child), "remote", "get-url", "origin"])
            if rc == 0 and "github.com" in stdout:
                m = re.search(r"github\.com[:/]([^/]+/[^/.\s]+)", stdout)
                if m:
                    repos.append(m.group(1))
    seen: set[str] = set()
    results: list[dict] = []
    for repo in repos:
        if repo in seen:
            continue
        seen.add(repo)
        for pr in _gh_prs(repo):
            created = _iso_to_dt(pr.get("createdAt", ""))
            merged = _iso_to_dt(pr.get("mergedAt") or "")
            rel_dt = merged or created
            if rel_dt is None or rel_dt < cutoff:
                continue
            state = (pr.get("state") or "").lower()
            if merged is not None:
                state = "merged"
            results.append({
                "repo": repo,
                "number": pr.get("number"),
                "title": pr.get("title", ""),
                "state": state,
                "url": pr.get("url", ""),
                "age": _humanize_age(rel_dt),
            })
    results.sort(key=lambda r: r.get("age", ""))
    return results


def get_agent_activity() -> dict:
    """
    Return { active: [...], available: [...], idle: [...], all_sessions: [...] }
    by scanning ~/.hermes/state.db.

    active    — sessions started in last 60s with parent_session_id NOT NULL.
    idle      — profiles whose most-recent session started > 7 days ago.
    available — all profiles in PROFILES_DIR minus active and idle sets.

    Graceful degradation: if state.db is missing, all profiles → available.
    """
    import sqlite3 as _sqlite3

    PROFILES_DIR = Path(__file__).resolve().parents[2] / "profiles"
    STATE_DB     = Path.home() / ".hermes" / "state.db"

    # Discover all on-disk profiles (enumerate from filesystem — not hardcoded)
    all_slugs: list[str] = []
    if PROFILES_DIR.exists():
        for p in sorted(PROFILES_DIR.iterdir()):
            if p.is_dir() and (p / "SOUL.md").exists():
                all_slugs.append(p.name)

    def _slug_entry(slug: str) -> dict:
        return {"slug": slug, "name": slug}

    if not STATE_DB.exists():
        return {
            "active": [],
            "available": [_slug_entry(s) for s in all_slugs],
            "idle": [],
            "all_sessions": [],
        }

    now_ts   = datetime.now(timezone.utc).timestamp()
    cutoff_active = now_ts - 60
    cutoff_idle   = now_ts - 7 * 86400

    try:
        conn = _sqlite3.connect(str(STATE_DB), timeout=5)
        conn.row_factory = _sqlite3.Row
        cur = conn.cursor()

        # Active: child sessions started in last 60s still running (no ended_at)
        cur.execute(
            "SELECT id, parent_session_id, started_at, estimated_cost_usd "
            "FROM sessions WHERE parent_session_id IS NOT NULL "
            "AND started_at >= ? AND ended_at IS NULL",
            (cutoff_active,),
        )
        active_rows = [dict(r) for r in cur.fetchall()]

        # Most-recent session per profile isn't stored by slug — use title heuristic
        # or match on profile slug in the id/title. For idle: find sessions whose
        # most-recent started_at < 7 days ago, grouped by rough slug match.
        # Since we can't reliably map sessions↔slugs from DB alone, we query
        # recent top-level sessions and cross-reference by title containing slug.
        cur.execute(
            "SELECT id, started_at, title, estimated_cost_usd "
            "FROM sessions WHERE parent_session_id IS NULL "
            "ORDER BY started_at DESC LIMIT 200"
        )
        all_top = [dict(r) for r in cur.fetchall()]

        # Build all_sessions (dispatch feed) — child sessions, last 100
        cur.execute(
            "SELECT id, parent_session_id, started_at, estimated_cost_usd "
            "FROM sessions WHERE parent_session_id IS NOT NULL "
            "ORDER BY started_at DESC LIMIT 100"
        )
        all_sessions = [dict(r) for r in cur.fetchall()]

        conn.close()
    except Exception as exc:
        print(f"[studio/cache] get_agent_activity DB error: {exc}", file=sys.stderr)
        return {
            "active": [],
            "available": [_slug_entry(s) for s in all_slugs],
            "idle": [],
            "all_sessions": [],
        }

    # Map active session IDs to slugs (best effort: match slug in session id prefix)
    active_slugs: set[str] = set()
    active_out: list[dict] = []
    for row in active_rows:
        # session id like 20260518_131318_e3f100 — no slug embedded, so mark unknown
        entry = {"slug": "unknown", "dispatch_id": row["id"], "started_at": row["started_at"]}
        active_out.append(entry)

    # Idle: profile slugs where their slug appears in a title of a recent session
    # and that session's started_at < 7 days ago.
    # Strategy: a profile is idle if NO session in the last 7 days has its slug in title.
    recent_titles: set[str] = set()
    for row in all_top:
        if row["started_at"] and row["started_at"] >= cutoff_idle:
            t = (row.get("title") or "").lower()
            recent_titles.add(t)

    idle_out: list[dict] = []
    available_out: list[dict] = []

    for slug in all_slugs:
        slug_lower = slug.lower()
        # Check if any recent session references this slug
        found_recent = any(slug_lower in title for title in recent_titles)
        if not found_recent:
            idle_out.append(_slug_entry(slug))
        else:
            available_out.append(_slug_entry(slug))

    # If nothing maps to idle (common early on), put all in available
    if not idle_out and not available_out:
        available_out = [_slug_entry(s) for s in all_slugs]

    return {
        "active": active_out,
        "available": available_out,
        "idle": idle_out,
        "all_sessions": all_sessions,
    }


def get_system_data() -> dict:
    """
    Return watchdog log tail (last 20 lines) + token spend per provider (last 7 days).
    """
    import sqlite3 as _sqlite3

    STATE_DB = Path.home() / ".hermes" / "state.db"

    # Watchdog log tail
    watchdog_lines = None
    if WATCHDOG_LOG.exists():
        try:
            with WATCHDOG_LOG.open("r", encoding="utf-8", errors="replace") as fh:
                lines = fh.readlines()[-20:]
            watchdog_lines = [l.rstrip("\n") for l in lines]
        except OSError:
            watchdog_lines = None

    # Token spend per provider — last 7 days
    spend: dict = {}
    if STATE_DB.exists():
        try:
            conn = _sqlite3.connect(str(STATE_DB), timeout=5)
            cur = conn.cursor()
            cutoff = datetime.now(timezone.utc).timestamp() - 7 * 86400
            cur.execute(
                "SELECT billing_provider, SUM(estimated_cost_usd) "
                "FROM sessions WHERE started_at >= ? AND estimated_cost_usd IS NOT NULL "
                "GROUP BY billing_provider",
                (cutoff,),
            )
            for provider, total in cur.fetchall():
                key = provider or "unknown"
                spend[key] = round(float(total or 0), 4)
            conn.close()
        except Exception as exc:
            print(f"[studio/cache] get_system_data DB error: {exc}", file=sys.stderr)

    return {"watchdog_lines": watchdog_lines, "spend": spend}


def get_system_health() -> dict:
    """Parse ~/.hermes/watchdog.log tail. Works fine even if the file is missing."""
    health: dict = {
        "gateway": {"status": "unknown", "color": "amber"},
        "dashboard": {"status": "unknown", "color": "amber"},
        "workspace": {"status": "unknown", "color": "amber"},
        "last_check": None,
        "log_exists": WATCHDOG_LOG.exists(),
    }
    if not WATCHDOG_LOG.exists():
        return health
    try:
        with WATCHDOG_LOG.open("r", encoding="utf-8", errors="replace") as fh:
            lines = fh.readlines()[-200:]
    except OSError:
        return health

    status_map = {
        "ok": ("OK", "green"), "up": ("UP", "green"), "healthy": ("HEALTHY", "green"),
        "degraded": ("DEGRADED", "amber"), "warn": ("WARN", "amber"),
        "down": ("DOWN", "red"), "fail": ("FAIL", "red"), "error": ("ERROR", "red"),
    }
    components = {"gateway", "dashboard", "workspace"}
    last_ts = None
    for line in lines:
        low = line.lower()
        for comp in components:
            if comp in low:
                for key, (label, color) in status_map.items():
                    if re.search(rf"\b{key}\b", low):
                        health[comp] = {"status": label, "color": color}
                        break
        m = re.match(r"^\s*(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})", line)
        if m:
            last_ts = m.group(1)
    health["last_check"] = last_ts
    return health


# ── Cache class ───────────────────────────────────────────────────────────

class Cache:
    """
    Persistent JSON cache for Studio data.

    Sections: 'engagements', 'decisions', 'prs', 'health'.
    Each section stores its data plus an 'updated_at' ISO timestamp.
    """

    _SECTION_COLLECTORS = {
        "engagements": lambda preview_dir: get_active_engagements(),
        "decisions":   lambda preview_dir: get_pending_decisions(preview_dir),
        "prs":         lambda preview_dir: get_recent_prs(),
        "health":      lambda preview_dir: get_system_health(),
        "agents":      lambda preview_dir: get_agent_activity(),
        "system":      lambda preview_dir: get_system_data(),
    }

    def __init__(self, path: Path = CACHE_PATH) -> None:
        self._path = path

    def _preview_dir(self) -> Path:
        return Path(
            os.environ.get("NEXOURA_PREVIEW_DIR", DEFAULT_PREVIEW_DIR)
        ).expanduser()

    def _now_iso(self) -> str:
        return datetime.now(timezone.utc).isoformat()

    def read(self) -> dict:
        """Read the cache file. Returns {} if the file is missing or broken."""
        if not self._path.exists():
            return {}
        try:
            text = self._path.read_text(encoding="utf-8")
            return json.loads(text)
        except (OSError, json.JSONDecodeError):
            return {}

    def _write(self, data: dict) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._path.write_text(json.dumps(data, indent=2, default=str), encoding="utf-8")

    def last_updated(self, section: str) -> str | None:
        """Return the ISO timestamp of the last successful refresh for section."""
        data = self.read()
        entry = data.get(section)
        if not isinstance(entry, dict):
            return None
        return entry.get("updated_at")

    def refresh(self, section: str) -> None:
        """
        Refresh ONE section by name.

        If the collector raises, the old data is kept and the error
        is printed to stderr. The server keeps running.
        """
        if section not in self._SECTION_COLLECTORS:
            print(
                f"[studio/cache] Unknown section '{section}'. "
                f"Valid: {', '.join(self._SECTION_COLLECTORS)}",
                file=sys.stderr,
            )
            return

        collector = self._SECTION_COLLECTORS[section]
        preview_dir = self._preview_dir()
        data = self.read()

        try:
            result = collector(preview_dir)
        except Exception as exc:
            print(
                f"[studio/cache] ERROR refreshing '{section}': {exc}. "
                "Keeping old data.",
                file=sys.stderr,
            )
            return

        data[section] = {"data": result, "updated_at": self._now_iso()}
        self._write(data)

    def refresh_all(self) -> None:
        """Refresh all four sections in order."""
        for section in self._SECTION_COLLECTORS:
            self.refresh(section)


# ── CLI entry point ───────────────────────────────────────────────────────

def _main(argv: list[str]) -> int:
    cache = Cache()
    if "--refresh-all" in argv:
        print("[studio/cache] Refreshing all sections...")
        cache.refresh_all()
        print(f"[studio/cache] Done. Cache at: {cache._path}")
        return 0
    if "--refresh" in argv:
        idx = argv.index("--refresh")
        if idx + 1 >= len(argv):
            print("Usage: cache.py --refresh <section>", file=sys.stderr)
            return 1
        section = argv[idx + 1]
        print(f"[studio/cache] Refreshing '{section}'...")
        cache.refresh(section)
        print(f"[studio/cache] Done. updated_at={cache.last_updated(section)}")
        return 0
    print("Usage: cache.py --refresh-all | --refresh <section>", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(_main(sys.argv[1:]))
