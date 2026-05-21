# PM Console — Live Dashboard

A self-contained, NEXOURA-branded HTML dashboard that gives Omar an at-a-glance
view of factory state: active engagements, pending decisions, recent PR
activity, and system health.

This tool is **read-only**. It scrapes git, the GitHub CLI, the Desktop preview
directory, and the local watchdog log — then renders a single HTML file you
open in a browser.

## What it shows

1. **Active Engagements** — one card per engagement repo under
   `/home/omar/dev/nexoura-engagements/*`. Shows a 9-stage NEXOURA lifecycle
   progress bar, current-stage badge, and the last 5 commits.
2. **Pending Decisions** — every `*.html` file in
   `$NEXOURA_PREVIEW_DIR/decisions/`, oldest first. Title is parsed from the
   `<title>` tag; each card links to the file.
3. **Recent Activity (24h)** — PRs created or merged in the last 24 hours across
   `nexoura-agent` and any engagement repos with a GitHub remote. Direct links
   to GitHub.
4. **System Health** — gateway / dashboard / workspace-UI status pills parsed
   from `~/.hermes/watchdog.log`. Renders a friendly placeholder if the log
   isn't there yet (B3 produces it).

## Install / requirements

- Python 3.9+ (stdlib only — no `pip install`).
- `git` on `$PATH`.
- `gh` CLI authenticated (`gh auth login`). Optional — without it, the
  Recent Activity panel just shows "No PR activity".

## Run

One-shot:

    python3 tools/pm-console/generate.py

Dry-run (prints rendered HTML to stdout, writes nothing):

    python3 tools/pm-console/generate.py --dry-run

The script writes two files:

- `$NEXOURA_PREVIEW_DIR/console.html` — the live dashboard (open in browser)
- `tools/pm-console/console.last.html` — local snapshot for git inspection

## Cron (refresh every 5 minutes)

    */5 * * * * cd /home/omar/dev/nexoura-agent && python3 tools/pm-console/generate.py >> ~/.hermes/pm-console.log 2>&1

## Environment variables

| Variable              | Default                                                   | Meaning                                  |
|-----------------------|-----------------------------------------------------------|------------------------------------------|
| `NEXOURA_PREVIEW_DIR` | `/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview`      | Where `console.html` is written.         |

If the directory doesn't exist, `generate.py` creates it (`mkdir -p`).

## Files

- `console.html` — HTML template with four `<!-- … -->` substitution markers
  (`ENGAGEMENTS`, `DECISIONS`, `ACTIVITY`, `HEALTH`, plus `TIMESTAMP`).
- `generate.py` — collector + renderer. Stdlib only.
- `schema.json` — JSON Schema describing the internal data dict that
  `generate.py` builds before rendering.
- `console.last.html` — generated snapshot (overwritten on every run; safe to
  inspect under git).

## Design

- Branded with the NEXOURA palette inline: `#7861FF` (purple), `#5B30FF`
  (violet), `#2563FF` (blue), `#00E0FF` (cyan), `#0A0F16` (navy), `#F5F7FA`
  (soft white).
- Sora display / Inter body via Google Fonts CDN.
- Dark and light modes via `prefers-color-scheme`.
- Mobile responsive: single column under 720px.
- Zero external JS — pure HTML+CSS, ~250 lines.

## Failure modes (all graceful)

| Missing                            | Behavior                                          |
|------------------------------------|---------------------------------------------------|
| `nexoura-engagements/` dir         | Engagements section shows empty-state message     |
| `decisions/` dir under preview     | Decisions section shows "No pending decisions"    |
| `gh` not installed / not auth'd    | Activity section shows graceful empty-state       |
| `~/.hermes/watchdog.log` missing   | Health section shows "No watchdog log yet"        |
| `NEXOURA_PREVIEW_DIR` missing      | Created with `mkdir -p`                           |

## Verification

    python3 tools/pm-console/generate.py --dry-run | head -20   # exit 0, prints HTML
    python3 tools/pm-console/generate.py                         # exit 0, writes file
    ls "$NEXOURA_PREVIEW_DIR/console.html"                       # exists
    python3 -c 'import json; json.load(open("tools/pm-console/schema.json"))'
