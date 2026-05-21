#!/usr/bin/env python3
"""
PM Console live dashboard generator.

Reads git/gh/Desktop state and renders a self-contained branded HTML dashboard
into $NEXOURA_PREVIEW_DIR/console.html.

Usage:
    python3 tools/pm-console/generate.py            # write to preview dir + snapshot
    python3 tools/pm-console/generate.py --dry-run  # print rendered HTML to stdout

Env:
    NEXOURA_PREVIEW_DIR  default: /mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview/

Stdlib only. No external deps.
"""
from __future__ import annotations

import html
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

# ---------- Configuration ----------

DEFAULT_PREVIEW_DIR = "/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview"
ENGAGEMENTS_ROOT = Path("/home/omar/dev/nexoura-engagements")
AGENT_REPO = "omar-alageel-platform/nexoura-agent"
WATCHDOG_LOG = Path.home() / ".hermes" / "watchdog.log"

# NEXOURA engagement lifecycle stages
NEXOURA_STAGES = [
    "requirements", "feasibility", "branding", "tech-architecture",
    "implementation", "gtm-marketing", "operations", "gate-review", "live",
]

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATE_PATH = SCRIPT_DIR / "console.html"
SNAPSHOT_PATH = SCRIPT_DIR / "console.last.html"


# ---------- Helpers ----------

def _run(cmd: list[str], cwd: Path | None = None, timeout: int = 15) -> tuple[int, str, str]:
    """Run a subprocess; return (rc, stdout, stderr). Never raises."""
    try:
        p = subprocess.run(
            cmd, cwd=cwd, capture_output=True, text=True, timeout=timeout, check=False,
        )
        return p.returncode, p.stdout, p.stderr
    except (FileNotFoundError, subprocess.TimeoutExpired) as e:
        return 127, "", str(e)


def _iso_to_dt(s: str) -> datetime | None:
    if not s:
        return None
    try:
        # GitHub uses Z suffix
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


# ---------- Data collectors ----------

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

        # Detect current stage from presence of stage marker files / dirs
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
    entries.sort(key=lambda e: e["mtime"])  # oldest first
    for e in entries:
        e.pop("mtime", None)
        out.append(e)
    return out


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


def get_recent_prs() -> list[dict]:
    """Recent PRs (last 24h created OR merged) across nexoura-agent + any engagement repos."""
    cutoff = datetime.now(timezone.utc) - timedelta(hours=24)
    repos = [AGENT_REPO]
    # Optional engagement repos: scan dirs for `gh repo view` remote if available
    if ENGAGEMENTS_ROOT.exists():
        for child in ENGAGEMENTS_ROOT.iterdir():
            if not (child / ".git").exists():
                continue
            rc, stdout, _ = _run(["git", "-C", str(child), "remote", "get-url", "origin"])
            if rc == 0 and "github.com" in stdout:
                m = re.search(r"github\.com[:/]([^/]+/[^/.\s]+)", stdout)
                if m:
                    repos.append(m.group(1))
    seen = set()
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


def get_system_health() -> dict:
    """Parse ~/.hermes/watchdog.log tail. Gracefully handle missing."""
    health = {
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

    # Look for the most recent status per component. Expected log line conventions:
    #   "<iso-ts> <component> <status>"   where status is OK / DEGRADED / DOWN / FAIL / UP
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
        # Capture leading ISO timestamp if present
        m = re.match(r"^\s*(\d{4}-\d{2}-\d{2}[T ]\d{2}:\d{2}:\d{2})", line)
        if m:
            last_ts = m.group(1)
    health["last_check"] = last_ts
    return health


# ---------- HTML fragment renderers ----------

def _esc(s) -> str:
    return html.escape(str(s) if s is not None else "")


def render_engagements(items: list[dict]) -> str:
    if not items:
        return '<div class="empty">No active engagements found in /home/omar/dev/nexoura-engagements/.</div>'
    out = []
    for e in items:
        stages_html = ""
        for i in range(e["stage_total"]):
            cls = "stage"
            if i < e["stage_index"]:
                cls += " done"
            elif i == e["stage_index"]:
                cls += " active"
            stages_html += f'<div class="{cls}" title="{_esc(NEXOURA_STAGES[i] if i < len(NEXOURA_STAGES) else "")}"></div>'

        commits_html = ""
        if e["commits"]:
            commits_html = '<ul class="commits">' + "".join(
                f'<li><span class="commit-msg">{_esc(c["message"])}</span> — {_esc(c["author"])} · {_esc(c["age"])} · <code>{_esc(c["sha"])}</code></li>'
                for c in e["commits"]
            ) + "</ul>"
        else:
            commits_html = '<div class="empty" style="margin-top:8px;">No commits yet.</div>'

        out.append(
            f'<div class="card">'
            f'<div class="card-title">{_esc(e["name"])} <span class="stage-badge">{_esc(e["current_stage"])}</span></div>'
            f'<div class="card-meta">Stage {e["stage_index"] + 1} of {e["stage_total"]}</div>'
            f'<div class="stages">{stages_html}</div>'
            f'{commits_html}'
            f'</div>'
        )
    return "".join(out)


def render_decisions(items: list[dict]) -> str:
    if not items:
        return '<div class="empty">No pending decisions.</div>'
    out = []
    for d in items:
        out.append(
            f'<div class="card">'
            f'<div class="card-title">{_esc(d["title"])}</div>'
            f'<div class="card-meta">Age: {_esc(d["age"])}</div>'
            f'<a class="decision-link" href="{_esc(d["url"])}">Open decision →</a>'
            f'</div>'
        )
    return "".join(out)


def render_activity(items: list[dict]) -> str:
    if not items:
        return '<div class="empty">No PR activity in the last 24h (or gh not authenticated).</div>'
    out = []
    for p in items:
        state = p.get("state", "open")
        state_cls = state if state in ("open", "merged", "closed") else "open"
        out.append(
            f'<div class="pr">'
            f'<span class="pr-state {state_cls}">{_esc(state)}</span>'
            f'<a href="{_esc(p["url"])}">#{_esc(p["number"])} {_esc(p["title"])}</a>'
            f'<span style="color:var(--muted); margin-left:auto; font-size:0.78rem;">{_esc(p["repo"])} · {_esc(p.get("age", ""))}</span>'
            f'</div>'
        )
    return "".join(out)


def render_health(h: dict) -> str:
    if not h.get("log_exists"):
        return (
            '<div class="empty">No watchdog log yet (~/.hermes/watchdog.log not found). '
            'B3 watchdog will populate this once running.</div>'
        )
    last = h.get("last_check") or "—"
    pills = []
    for label, key in [("Gateway", "gateway"), ("Dashboard", "dashboard"), ("Workspace UI", "workspace")]:
        comp = h.get(key, {})
        color = comp.get("color", "amber")
        status = comp.get("status", "unknown")
        pills.append(
            f'<div class="pill">'
            f'<div class="pill-label">{_esc(label)}</div>'
            f'<div class="pill-value"><span class="dot {_esc(color)}"></span>{_esc(status)}</div>'
            f'<div class="pill-stamp">Last check: {_esc(last)}</div>'
            f'</div>'
        )
    return f'<div class="health">{"".join(pills)}</div>'


# ---------- Renderer ----------

def render(template_html: str, data: dict) -> str:
    out = template_html
    out = out.replace("<!-- TIMESTAMP -->", _esc(data.get("generated_at", "")))
    out = out.replace("<!-- ENGAGEMENTS -->", render_engagements(data.get("engagements", [])))
    out = out.replace("<!-- DECISIONS -->", render_decisions(data.get("decisions", [])))
    out = out.replace("<!-- ACTIVITY -->", render_activity(data.get("prs", [])))
    out = out.replace("<!-- HEALTH -->", render_health(data.get("health", {})))
    return out


# ---------- Main ----------

def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv

    preview_dir = Path(os.environ.get("NEXOURA_PREVIEW_DIR", DEFAULT_PREVIEW_DIR)).expanduser()

    try:
        template_html = TEMPLATE_PATH.read_text(encoding="utf-8")
    except OSError as e:
        print(f"ERROR: cannot read template {TEMPLATE_PATH}: {e}", file=sys.stderr)
        return 1

    data = {
        "generated_at": datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S UTC"),
        "engagements": get_active_engagements(),
        "decisions": get_pending_decisions(preview_dir),
        "prs": get_recent_prs(),
        "health": get_system_health(),
    }

    rendered = render(template_html, data)

    if dry_run:
        sys.stdout.write(rendered)
        return 0

    # Ensure preview dir exists
    try:
        preview_dir.mkdir(parents=True, exist_ok=True)
        target = preview_dir / "console.html"
        target.write_text(rendered, encoding="utf-8")
        # snapshot for git inspection (gitignored optionally)
        SNAPSHOT_PATH.write_text(rendered, encoding="utf-8")
    except OSError as e:
        print(f"ERROR: failed to write console.html: {e}", file=sys.stderr)
        return 1

    print(f"Wrote {target}")
    print(f"Snapshot: {SNAPSHOT_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
