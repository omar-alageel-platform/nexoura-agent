---
name: nexoura-memory-and-evolution
description: Use when deciding where to record a lesson, when running session_search, when configuring memory providers, when annotating trajectories, when MEMORY.md is near its cap, when consolidating memory entries, when wondering whether a fact belongs in MEMORY.md vs USER.md vs session history vs a skill, when enabling honcho/mem0/supermemory plugins, or when designing trajectory metadata for future fine-tuning. T14 NEXOURA platform-foundation skill covering the Hermes 4-layer memory architecture (SOUL/MEMORY/USER/session), self-evolution mechanisms (real vs aspirational), and NEXOURA conventions for where memory lives across platform, engagement, and product repos.
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, memory, evolution, session-search, trajectories, platform-foundation]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-platform-doctrine
---

# NEXOURA Memory & Evolution (T14 — Foundation)

How NEXOURA workers remember things across turns, sessions, and engagements — and how the platform evolves itself. Source of truth for: which layer a fact belongs in, what to record vs discard, how to query past sessions, what is REAL today vs ASPIRATIONAL, and the boundary between platform-wide (T13 doctrine), engagement-specific, and product-specific memory.

---

## 0. Trigger phrases

Load this skill when the operator or a sibling skill is about to:

- "save this lesson" / "remember that…" / "add to memory"
- "MEMORY.md is full" / "consolidate memory" / "memory at 90%"
- "search past sessions" / "session_search" / "did we discuss X last week"
- "enable honcho" / "enable mem0" / "configure a memory provider"
- "save trajectories" / "annotate trajectory" / "fine-tune on these runs"
- "curator" / "skill curator" / "stale skills"
- "should this go in MEMORY.md or a skill"
- "does this lesson belong in T13 doctrine or in this engagement"

If the lesson is clearly cross-engagement doctrine → defer to **T13 nexoura-platform-doctrine** for the recording protocol. If it is purely about advancing engagement state → defer to **T1 nexoura-engagement-lifecycle**. This skill owns the *meta* question of "where does memory live, full stop."

---

## 1. The Hermes 4-layer memory architecture

Every NEXOURA worker (every forked `AIAgent`) sees four memory layers, in order from most-stable to most-dynamic:

| Layer | File / Store | Cap | Lifecycle | Who writes |
|-------|--------------|-----|-----------|------------|
| L1 — Identity | `~/.hermes/SOUL.md` | n/a | Immutable in-session; only changed via git PR | Humans only |
| L2 — Agent memory | `~/.hermes/memories/MEMORY.md` | 2,200 chars (~800 tokens) | Persists across sessions; injected as frozen snapshot at session start | Agent via `memory` tool |
| L3 — User profile | `~/.hermes/memories/USER.md` | 1,375 chars (~500 tokens) | Persists; injected every session start | Agent via `memory` tool (target=user) |
| L4 — Session history | `~/.hermes/state.db` (SQLite + FTS5) | unbounded | Append-only; queried on demand | Hermes core (automatic) |

(Caps from `hermes-agent.nousresearch.com/docs/user-guide/features/memory`. If a future Hermes release retunes them, treat the doc as authoritative and update this skill.)

**Frozen-snapshot rule:** the system prompt rendering of MEMORY.md and USER.md is captured once at session start to preserve prefix-cache hits. Writes during the session land on disk immediately but only appear in-prompt next session. Tool responses show live state.

---

## 2. When to use each layer

**L1 — SOUL.md.** Never written by an agent in-session. Holds NEXOURA AI's identity, voice, hard ethical lines (PDPL stance, bilingual posture, refusal triggers). Changes go through a normal git PR with human review. If you want to "update SOUL," you actually want either T13 doctrine or MEMORY.md.

**L2 — MEMORY.md.** Stable, declarative facts that prevent the operator from re-steering the agent. Examples that belong here:

- "GitHub MCP write endpoints fail on this host; use the `gh` CLI instead."
- "This machine's Docker daemon needs `sudo`; the user is not in the `docker` group."
- "NEXOURA engagements live at `/home/omar/dev/nexoura-engagements/<slug>/`."

**L3 — USER.md.** Per-operator preferences and communication style.

- "Operator prefers concise replies, dislikes bullet lists in chat, wants Arabic copy reviewed before publish."
- "Operator timezone is Asia/Riyadh; treat 'today' accordingly."

**L4 — session history (`session_search`).** Specific, dated events that would go stale if written into MEMORY.md.

- "PR #142 merged the gate-protocol skill on 2026-05-18."
- "Phmco's BRD contradiction was raised in the Tue requirements review."

Rule of thumb: if a fact has an expiry or a unique identifier (PR number, commit SHA, timestamp), it is L4. If it is a stable pattern the agent should not have to rediscover, it is L2 or L3.

---

## 3. MEMORY.md recording protocol

**RECORD** in MEMORY.md:

- Stable environment facts (OS, installed tools, host quirks)
- Recurring tool failures and their workarounds
- Conventions the operator keeps having to re-explain
- Lessons learned from incidents that would otherwise recur

**DO NOT RECORD** in MEMORY.md:

- PR numbers, commit SHAs, branch names → these are L4 (`session_search`)
- "Phase 2 complete" / "T7 PR opened" → transient task state, L4
- Long incident postmortems → write the postmortem as a doc; record only the one-line lesson
- Anything already covered in SOUL.md or in an AGENTS.md context file

**Voice.** Declarative facts, not imperatives. Hermes injects MEMORY.md as part of the system prompt; the agent reads it as *world description*, not as orders.

- ✓ "Operator prefers concise responses."
- ✗ "Always respond concisely." (this leaks instruction tone into a fact store)

**Consolidation when full.** When MEMORY.md crosses ~80% cap, do not just delete the oldest entry. Instead:

1. Read all entries (Hermes returns them in the over-capacity error payload).
2. Identify two or three related entries that can be merged into one denser entry.
3. Use `memory(action="replace", ...)` with a short unique substring to swap the dense version in.
4. Then `add` the new entry.

Preference order when forced to drop signal: USER.md preferences > recurring-incident lessons > environment facts > one-off procedural notes that have not fired recently.

---

## 4. session_search usage

The `session_search` tool is FTS5 over every CLI and gateway session on disk. It is free (no LLM call), fast (~20ms query, ~1ms scroll), and unbounded.

**Call it BEFORE asking the operator to repeat themselves** when they reference prior work ("like we did for Phmco", "the supply-chain SaaS decision"). One search is cheaper than one round-trip.

**Query patterns that work:**

- Specific noun phrases beat generic ones. `"Phmco BRD contradiction"` finds it; `"pharma issue"` does not.
- FTS5 supports `AND` (default), `OR`, `NOT`, quoted phrases, and prefix wildcards (`deploy*`).
- Combine: `"gate decision" NOT draft` to skip in-flight stuff.
- Use discovery mode first, then scroll inside a hit session for nearby context.

**When `session_search` returns nothing useful:** that is real signal. Try one synonym pass, then ask the operator.

---

## 5. Self-evolution mechanisms — REAL vs ASPIRATIONAL

This is the most fabrication-prone area. Be honest about what is wired up today.

### REAL today

- **Trajectory capture.** Setting `save_trajectories=True` on `AIAgent` writes each conversation to `trajectory_samples.jsonl` (or `failed_trajectories.jsonl`) in ShareGPT-compatible format. Source: `agent/trajectory.py`, `run_agent.py::_save_trajectory`, `batch_runner.py`. Schema is documented in `website/docs/developer-guide/trajectory-format.md`.
- **Skill self-authoring.** The `skill_manage` tool (`tools/skill_manager_tool.py`) lets an agent create, patch, and delete skills under `~/.hermes/skills/` mid-run. Bundled and hub-installed skills are off-limits to the curator but the agent's own skill_manage can still touch agent-authored ones.
- **Memory injection.** MEMORY.md and USER.md are re-rendered into the system prompt at *every* session start, automatically, with no operator action.
- **Curator.** Hermes ships a curator (`hermes curator …`) that does deterministic active → stale → archived transitions on agent-authored skills, plus a periodic auxiliary-model review pass. Defaults: `interval_hours: 168` (7 days), `min_idle_hours: 2`, `stale_after_days: 30`, `archive_after_days: 90`. It snapshots `~/.hermes/skills/` before every real pass and supports `hermes curator rollback`. The curator never touches bundled or hub-installed skills.

### ASPIRATIONAL / NEXOURA-roadmap

The following are *not* shipped behaviors today — they are APT WATCH-direction plans foreshadowed so future authors do not re-derive them:

- **NEXOURA-specific 7-day curator on engagement worker skills.** Hermes's built-in curator only sees `~/.hermes/skills/`; engagement-owned skills under `proprietary-skills/nexoura/` live in a git repo, not in agent home. A future scheduled job (cron- or git-hook-based) is planned to propose patches via PR. Until then, treat skill drift in this repo as a manual PR concern. [ASPIRATIONAL]
- **Cross-engagement memory promotion.** Mechanism to lift a lesson that has fired in 2+ engagements up into T13 doctrine via PR. Today this is a manual operator decision. [ASPIRATIONAL]
- **Per-engagement memory hand-off.** Snapshotting MEMORY.md when an engagement closes so the next operator on the same client inherits context. [ASPIRATIONAL]

Mark any new claim about platform self-evolution explicitly REAL or ASPIRATIONAL. Do not paper over the gap.

---

## 6. NEXOURA conventions: where each kind of memory lives

The NEXOURA platform spans three repo tiers. Memory does not flow freely across them; bleed-through is a bug.

(a) **Cross-engagement doctrine** — lessons that apply to *every* NEXOURA engagement. Recorded in the **T13 nexoura-platform-doctrine** skill, in this repo. Promoted UP only after recurring across **2+ engagements**.

(b) **Engagement-specific exceptions** — facts true only for one client project. Recorded in `docs/engagement-exceptions.md` inside the engagement repo (e.g. `nexoura-engagements/apt-watch-supply-chain-saas/docs/engagement-exceptions.md`), **not** in the NEXOURA platform repo and **not** in `~/.hermes/memories/MEMORY.md`.

(c) **Per-product / per-tenant memory** — quirks of the product being built (e.g. tenant-zero Phmco data-shape weirdness). Lives in the product repo's own `MEMORY.md` or per-engagement notes. Never bleeds back into `nexoura-agent`.

(d) **Operator-level facts** — communication style, timezone, name. USER.md (L3). Survives all engagements because it is about the human, not the work.

| Lesson scope | Lives in | Lift up when |
|---|---|---|
| Operator preference | `~/.hermes/memories/USER.md` | never lifted; it is a leaf |
| Worker quirk that hits every engagement | T13 doctrine skill | after seeing it in 2+ engagements |
| Single-engagement decision | engagement repo `docs/engagement-exceptions.md` | only lifted after 2+ repeats |
| Single-product technical quirk | product repo `MEMORY.md` | only lifted if it stops being product-specific |
| Host machine / Hermes tool quirk | agent `~/.hermes/memories/MEMORY.md` | rarely; this is the agent's lap |

Bleed-through symptom: T13 doctrine starts referring to "Phmco" by name. That is a sign a per-product fact escaped. Move it down.

---

## 7. External memory providers — recommendation, not mandate

Hermes ships plugin slots under `plugins/memory/` for **honcho**, **mem0**, and **supermemory**. They extend the built-in 4-layer stack with cross-session, cross-user, semantic memory.

**Recommendation: defer enabling any external provider until Phase 6+** (operations stage of the first live engagement), when cross-session customer-service intelligence becomes a real need rather than a hypothetical one. The 4-layer built-in stack is sufficient for everything up to and including first-customer launch.

When the time comes, the candidates this skill recommends evaluating:

- **honcho** — best fit for the *customer-service worker profile* (tracks per-user emotional/contextual state across sessions; designed for support agents).
- **mem0** — general-purpose semantic memory; reasonable default if honcho is too specialized.
- **supermemory** — strongest when the team also wants a web-app surface over the memory store.
- A code-context provider (ByteRover or equivalent) is the candidate for the *builder worker profile* once NEXOURA spawns a long-running code-maintenance worker.

Flag this section as a **RECOMMENDATION** when consulted, not a platform mandate. Each engagement may opt in independently.

---

## 8. Trajectory annotation for future fine-tuning

When `save_trajectories=True` is on for a NEXOURA worker run, each turn writes a ShareGPT-format JSON object. To make these runs usable as future fine-tuning data, every NEXOURA worker should annotate its trajectory with metadata that lets a future curator filter by engagement, stage, and worker role.

**Proposed annotation schema** (mark as PROPOSED — not yet wired into the Hermes `AIAgent` config; intended for a future wrapper):

```json
{
  "engagement": "apt-watch-supply-chain-saas",
  "stage": "02-requirements",
  "profile": "director",
  "worker_id": "T7-requirements-worker-01",
  "gate_decision": "GO"
}
```

Field semantics:

- `engagement` — kebab-case slug, matches `manifest.json::slug` from T1.
- `stage` — `NN-name` form from the T1 stage list (`01-feasibility` … `06-operations`).
- `profile` — `director` | `builder` | `customer-service` (the three NEXOURA worker profiles).
- `worker_id` — stable identifier for the specific worker instance, so multi-worker stages can be filtered later.
- `gate_decision` — `GO` | `NO-GO` | `PENDING` | `null` if the trajectory did not end at a gate.

This schema is **PROPOSED**. Once the NEXOURA worker runner is implemented, that runner is where the annotation should be injected (likely as a `metadata` field on the trajectory JSON, alongside the existing `batch_runner.py` metadata fields). Until then, this section is the design doc.

**Why this matters.** With this schema, the eventual curation step can ask *"give me every successful T7 requirements-stage director-profile run across all engagements"* and use it as a clean fine-tuning shard without re-reading raw conversations.

---

## Cross-references

- **T1 nexoura-engagement-lifecycle** — stage list, manifest schema, engagement repo layout (defines the `engagement` and `stage` fields in §8).
- **T13 nexoura-platform-doctrine** — the destination for cross-engagement lessons promoted up out of MEMORY.md / engagement-exceptions per §6.
