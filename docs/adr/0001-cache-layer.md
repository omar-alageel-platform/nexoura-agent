# ADR 001 — Cache Layer Contract

**Status:** Accepted
**Date:** 2025 (implemented in Studio B1, PR #57)
**Author:** Architecture Director

---

## Context

NEXOURA Studio needs fresh data to show on screen. That data comes from files
on disk — things like open GitHub pull requests, pending decisions, and system
health checks.

We had two choices for how to watch those files:

1. Ask the operating system to tell us when a file changes (called "inotify"
   on Linux). Fast, but requires an extra library.

2. Check the files ourselves on a timer, every few seconds. Slower, but works
   with Python's built-in tools and nothing extra to install.

We also needed to decide how to send updates to the browser. The browser has
to show new data without the user refreshing the page.

Studio runs only on localhost (127.0.0.1). No outside users. No mobile
network. This keeps the design simple.

The goal was a working cache by the end of B1 with zero new dependencies.

---

## Decision

We built a polling cache in `tools/studio/cache.py`. Here is what it does:

**Polling, not watching.** The cache checks for new data every 2 seconds using
Python's `threading.Timer`. This is called the "tick." We chose 2 seconds
because it is fast enough to feel live, and slow enough to not waste CPU.

**No extra libraries.** We used only Python's standard library (stdlib). No
inotify. No Redis. No message queues. This means anyone can run Studio with
just `python3` — no `pip install` needed.

**Four data sections.** The cache splits data into four independent sections:
- `engagements` — active client projects
- `decisions` — pending decisions awaiting approval
- `prs` — recent GitHub pull requests
- `health` — server and watchdog status

Each section refreshes on its own. If one section fails (for example, a file
is missing), only that section shows an error. The other three keep working.
This is called "per-section exception safety."

**State file.** After each tick, the cache writes all four sections to
`state.json`. The HTTP server reads this file to answer `/api/state` requests.

**SSE fan-out.** SSE stands for Server-Sent Events. It is a way for the server
to push updates to the browser over a long-lived connection. When the cache
detects a change (any section's data is different from last tick), it sends
a `state-changed` event to all connected browsers. The browser then re-fetches
`/api/state` and updates the view.

**Heartbeat.** Every 15 seconds, the server sends a keep-alive message over
the SSE connection. This stops firewalls and proxies from closing idle
connections.

**Each section has a timestamp.** `updated_at` records when that section last
changed. The UI can show "last updated 2 minutes ago" per section.

---

## Consequences

**Good:**
- Zero extra dependencies. Studio ships as a single folder.
- Simple to debug. The cache is just a Python class with one timer loop.
- Safe. If one section crashes, the rest keep running.
- state.json is easy to inspect by hand. Open it in a text editor.

**Watch out for:**
- The 2-second tick means data is always slightly behind real time. A PR
  merged right now may take up to 2 seconds to appear in Studio. This is fine
  for a dashboard. It is not fine for a real-time trading system.
- All sections run in the same Python process. A very slow section could delay
  others. In B1, each section is fast (just reading small JSON files), so this
  is not a problem yet.
- Polling creates some CPU activity every 2 seconds even when nothing changes.
  On a laptop, this is negligible.
- No Redis means no shared cache across multiple processes. Studio runs as a
  single process on localhost, so this is not a problem in Round 1.

**Future signals to watch:**
- If the number of sections grows past ~10, consider increasing the tick to 5s.
- If Studio ever runs on a server with many users, re-evaluate Redis or a
  proper message broker. That would need a new ADR.

---

## Alternatives Considered

**inotify (Linux kernel file-watching)**
- Pros: zero polling overhead, instant notification.
- Cons: requires `watchdog` or `pyinotify` (extra dependency). Also
  platform-specific — would not work on macOS or Windows dev machines.
- Rejected: dependency discipline takes priority at this stage.

**Redis pub/sub**
- Pros: industry standard, supports many connected clients, persistent.
- Cons: requires running a Redis server. Adds ops burden for a localhost tool.
- Rejected: violates the "no new dependencies" rule. Revisit when product #2
  onboards and multi-user becomes a real requirement.

**Filesystem mtime polling (per-file)**
- Pros: only reads files when mtime changes.
- Cons: more complex code with little benefit at 2s tick and small file count.
- Rejected: over-engineered for current scale.
