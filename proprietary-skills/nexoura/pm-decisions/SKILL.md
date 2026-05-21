---
name: nexoura-pm-decisions
description: Use when a NEXOURA worker, director, or orchestrator needs to surface a decision to the PM (Omar). PM is a DECIDER, not a reader — goal is decision in <60 seconds. Defines the decision-card pattern (title + context + 2-4 options + recommendation + action), HTML template, NEXOURA brand application, file-naming convention, summary-brief variant for non-decision comms, and forbidden anti-patterns (walls of text, in-conclusion paragraphs, lists >5 items). Working HTML templates committed alongside.
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, pm-communication, decisions, visual, ui]
    related_skills:
      - nexoura-output-formatting
      - nexoura-iteration-framework
      - nexoura-research-first
      - nexoura-platform-doctrine
---

# NEXOURA PM Decisions (T20)

How NEXOURA workers and orchestrators surface decisions to the PM (Omar). The PM is the bottleneck of the entire factory; every wasted second of his attention is a tax on throughput. This skill defines the *one* format we use to ask him things.

On *visual / PM-comms* questions this skill wins over T15 (output formatting). On *behavioral / verification* questions T13 (platform doctrine) still wins.

---

## §1 PM communication principle

The PM is a **DECIDER, not a READER**. Every NEXOURA-to-PM artifact must let him decide in **under 60 seconds**.

That number is not aspirational, it's a budget. A typical NEXOURA day surfaces 5–15 decisions across stages, tenants, and infra. At 60 s each, that is 5–15 minutes of PM time per day on decisions alone. At 5 minutes each (the natural human tendency when given prose), it is 25–75 minutes — half a workday gone to reading worker reports.

**Visual > text.** Cards, options, color-coded recommendations, one-click actions. Long prose is for end-customers and BRDs — *never* for PM-facing summaries.

**One decision per card.** If you have three decisions, send three cards. Do not bundle. Bundled decisions force re-reading, which kills the 60 s budget.

---

## §2 Decision-card structure

Every PM-facing decision card has exactly five sections, in this order:

```
┌──────────────────────────────────────────────────┐
│  TITLE          One sentence stating the decision │
│                 e.g. "Pick brand direction for    │
│                 NEXOURA Studio homepage"          │
├──────────────────────────────────────────────────┤
│  CONTEXT        Two sentences max. Why now,       │
│                 what blocks if undecided.         │
├──────────────────────────────────────────────────┤
│  OPTIONS        2–4 cards. Each card:             │
│                   • Name (1–3 words)              │
│                   • 2-sentence description        │
│                   • 2–3 pros                      │
│                   • 2–3 cons                      │
├──────────────────────────────────────────────────┤
│  RECOMMENDATION One sentence: WHICH + WHY.        │
│                 Colored with brand gradient.      │
├──────────────────────────────────────────────────┤
│  ACTIONS        [Approve] [Pick alternative]      │
│                 [Need more info]                  │
└──────────────────────────────────────────────────┘
```

Hard rules:

- **Title** is a question or a "Pick X for Y" imperative. Not a statement.
- **Context** is ≤2 sentences. If you need more, the decision is not ready — go research more (see T18 nexoura-research-first).
- **Options** are 2, 3, or 4. Never 1 (not a decision), never 5+ (cognitive overload).
- **Recommendation** is mandatory. A card without a recommendation is a worker hiding behind "you decide" — refused.
- **Actions** are visual buttons (no JS required, just styled `<a>` or `<button>` for the PM's mental model — actual wiring is the PM Console's job).

---

## §3 Visual implementation

The committed template at `templates/decision-card.html` is the canonical form. Workers fill placeholders; nothing else changes.

NEXOURA palette, used inline (no external CSS):

```
Primary gradient: linear-gradient(135deg, #7861FF 0%, #5B30FF 28%, #2563FF 68%, #00E0FF 100%)
Dark bg:          #0A0F16
Light bg:         #F5F7FA
Recommendation:   gradient fill on the card border + text
```

Implementation requirements:

- **Self-contained.** No `<link>`, no `<script src>`. All CSS inline in a single `<style>` tag.
- **Dark + light mode** via `@media (prefers-color-scheme: dark)`. PM uses both.
- **Mobile responsive.** Cards stack vertically below 720 px (PM checks on phone).
- **Print-clean.** PM occasionally screenshots for clients; cards must render correctly when saved as PDF.
- **No JS dependencies.** Buttons are visual only; the PM Console intercepts clicks at the aggregator layer.

---

## §4 PM Console integration

Decision cards are written to disk at:

```
$NEXOURA_PREVIEW_DIR/decisions/decision-<NNN>-<slug>.html
```

Default `$NEXOURA_PREVIEW_DIR` = `/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview/`.

Filename rules:

- `<NNN>` is a three-digit zero-padded sequence (`001`, `002`, ...). Workers pick the next free number atomically (read `ls`, pick max+1).
- `<slug>` is kebab-case, ≤6 words. Use words from the title.
- Examples: `decision-001-brand-direction.html`, `decision-042-tenant-zero-rollout.html`.

The PM Console (separate tool, not in this skill) watches `decisions/` and aggregates open cards into a single board. This skill produces the *atoms*; the Console handles flow.

Summary briefs (non-decisions) go to `$NEXOURA_PREVIEW_DIR/briefs/summary-<NNN>-<slug>.html`. Same naming rules.

---

## §5 Summary brief variant

For non-decision communications (status updates, weekly metrics, research digests), use the **summary brief** variant. Template at `templates/summary-brief.html`.

Structure:

- **Title** — one sentence subject.
- **Body** — 5–10 lines max. Bullet points or a short paragraph.
- **Metrics** — 3–5 numeric tiles (e.g. "PRs merged: 12", "Open decisions: 3").
- **Next actions** — 1–2 lines, prefixed "Next: ...".

Same brand palette, same dark/light handling, same self-contained constraint. The visual difference: summary briefs have a neutral border (no gradient ring), to make decision cards stand out in the Console.

If a summary brief reaches >10 lines of body text, it has become an essay and must be split: extract the decision atoms into decision cards, keep only the status as a brief.

---

## §6 Anti-patterns (refused on review)

- **Walls of text.** Any decision card with >300 words of prose is refused. Compress to cards or research more (T18).
- **"In conclusion" paragraphs.** Decision cards have no conclusions, they have recommendations. If the word "conclusion" appears, the card is refused.
- **Bullet lists with >5 items.** Cap pros at 3, cons at 3, options at 4. If you need more, the decision is not framed correctly.
- **Options without pros/cons.** Every option must have both, or it's not really an option.
- **Card without recommendation.** Workers do not get to punt the decision back uncolored. Pick one and defend it in one sentence.
- **External CSS or JS.** No CDNs, no Tailwind, no Bootstrap, no inline `<script src>`. Brand palette inline only.
- **Mixed decisions.** One decision per card. If two are coupled, say so in context and still produce two cards with cross-references.
- **No-context decisions.** A card that skips §2 context to "save space" wastes more PM time than it saves — refused.

---

## §7 Working files committed alongside

```
proprietary-skills/nexoura/pm-decisions/
├── SKILL.md                                  (this file)
├── templates/
│   ├── decision-card.html                    Generic {{PLACEHOLDER}} template
│   └── summary-brief.html                    Generic summary template
└── examples/
    ├── decision-001-brand-direction.html     Filled: Studio homepage direction
    ├── decision-002-research-tool.html       Filled: Stage 3 research tool pick
    ├── decision-003-tenant-rollout.html      Filled: Tenant Zero rollout strategy
    ├── summary-001-stage3-status.html        Filled: Stage 3 weekly status
    └── summary-002-weekly-metrics.html       Filled: weekly metrics digest
```

Workers copy a template, replace placeholders, drop into `$NEXOURA_PREVIEW_DIR/decisions/` (or `briefs/`), and stop. The PM Console takes over from there.

---

## Cross-references

- **T13 nexoura-platform-doctrine** — verification reflex applies; do not claim "the data shows X" in a decision card without having checked.
- **T15 nexoura-output-formatting** — defines the broader visual language; this skill is the PM-comms specialization.
- **T18 nexoura-research-first** — if you cannot fill context in 2 sentences, research more before sending the card.
- **T19 nexoura-iteration-framework** — decision cards are the *output* of an iteration loop; do not send a card mid-iteration.
