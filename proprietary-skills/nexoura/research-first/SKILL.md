---
name: nexoura-research-first
description: Use when a NEXOURA worker is about to author any creative, strategic, or factual artifact (brand book, positioning, marketing copy, landing page, UX flow, NFR, architecture choice, market analysis, competitive teardown) and has not yet grounded the work in real sources. This skill is the T18 research methodology — 5-10 source minimum, tool preference order (Exa → Firecrawl → Parallel → web_search), the one-page visual research brief format for PM consumption, when NOT to research, and how research Round 0 feeds T19 iteration. Auto-load before any "authoring" card.
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, research, methodology, grounding, sources]
    related_skills: [nexoura-iteration-framework, nexoura-pm-decisions, nexoura-platform-doctrine]
---

# NEXOURA Research-First Methodology (T18)

The pre-authoring gate. Before a NEXOURA worker writes the first line of any
creative, strategic, or factual artifact, this skill is what they consult.
Round 0 of every authoring engagement is research; Round 1 (concept
divergence, T19 `nexoura-iteration-framework`) cannot start until the
research brief from §4 is in PM's hands.

On *grounding* (where sources come from, how many, what shape) this skill
wins. On *behavior* (how to claim, how to verify) `nexoura-platform-doctrine`
wins. On *file shape and citation format* T3 `nexoura-artifact-conventions`
wins. This skill is the research layer between them.

---

## §1 Research-before-authoring principle

The most common quality failure on NEXOURA authoring work is ungrounded
confident prose: a worker drafts a brand book, positioning statement, NFR
table, landing section, or competitive teardown *from internal
pattern-matching alone* and ships without opening a source. The output reads
plausible; PM catches the absence only when a client asks "where does this
come from".

Fix is structural. Authoring without grounding is banned. Every authoring
card opens with Round 0 — research — and Round 1 only starts when 5–10
sources are captured (3–5 tactical, §3) and the brief (§4) is in PM's hands.
Precedent: `nexoura-platform-doctrine` §4 lesson #3 (zero-hit overreach,
May 2026) — generalizing "absent in one file" to "absent in the corpus".
Same shape recurs in authoring: "I know how SaaS pricing pages work"
generalizes from 2–3 remembered pages to "the pattern" and produces
confident copy on a foundation PM cannot audit. Cite or do not claim.

---

## §2 Tool stack — preference order

Four tools. Pick the highest-preference one that fits the question, not the
most familiar.

### Exa API — semantic search (PREFERRED for concepts)

Best for concepts, patterns, prior art, "how do people in X space think
about Y", research papers, high-signal blogs. Exa indexes semantically — a
natural-language query retrieves on *meaning*, not keyword overlap. Default
for brand, positioning, UX-pattern, architecture-pattern research.

Env: `EXA_API_KEY` · Endpoint: `https://api.exa.ai/search`

```bash
curl -s https://api.exa.ai/search \
  -H "x-api-key: $EXA_API_KEY" -H "content-type: application/json" \
  -d '{"query":"how B2B SaaS pricing pages communicate value tiers",
       "numResults":10,"useAutoprompt":true,
       "category":"research paper","contents":{"text":true}}'
```

Useful `category` values: `research paper`, `company`, `news`, `tweet`,
`personal site`. Leave `useAutoprompt: true` on unless you need exact-phrase
matching.

### Firecrawl — full-page extraction (PREFERRED for one URL deep)

Best for one URL you already know is relevant, when you want clean markdown
stripped of nav/ads/footer. Use after Exa surfaces a URL, or when a
stakeholder hands you a link.

Env: `FIRECRAWL_API_KEY` · Endpoint: `https://api.firecrawl.dev/v1/scrape`

```bash
curl -s https://api.firecrawl.dev/v1/scrape \
  -H "Authorization: Bearer $FIRECRAWL_API_KEY" \
  -H "content-type: application/json" \
  -d '{"url":"https://stripe.com/pricing",
       "formats":["markdown"],"onlyMainContent":true}'
```

`onlyMainContent: true` drops nav/footer/cookie-banners.

### Parallel API — search + extract batch (PREFERRED for N comparative)

Best for comparative research across 5–10 sources where you want structured
output in one round-trip. Use when the question is "how do {Stripe, Linear,
Vercel, Notion, Figma} price" — same schema across N sources, returned as
JSON.

Env: `PARALLEL_API_KEY` · Endpoint: `https://api.parallel.ai/v1/tasks`
(verify in loaded env docs; surface has moved more than once). Submit a
task with a URL list (or fan-out query) plus a JSON schema for fields to
extract; poll for the structured result. Falls back to Exa+Firecrawl
per-source if unavailable.

### web_search — last resort

Generic, no semantic recall, no full-page extraction, SEO-biased. Use only
for very fresh news Exa hasn't indexed, deeply long-tail queries, or a
sanity check that a fact is findable. Never default.

### Decision rule (one line)

**Concepts → Exa; one URL deep → Firecrawl; comparative N sources →
Parallel; nothing else fits → web_search.**

---

## §3 Research workflow

Volume scales with artifact authority. A brand book on a client's desk for
18 months is not the same as copy for one landing section.

### Source-count minimums

| Artifact class                                       | Min sources |
|------------------------------------------------------|-------------|
| Brand book, positioning, voice & tone, naming       | 5–10        |
| NFR table, architecture choice, tech-stack eval     | 5–10        |
| GTM plan, pricing strategy, channel mix             | 5–10        |
| Competitive teardown (single competitor, 360°)      | 5–10        |
| Market analysis, TAM/SAM, industry pattern brief    | 5–10        |
| Landing-page section copy, single decision card     | 3–5         |
| Single-screen UX flow, copy revision, one ADR       | 3–5         |
| Internal config, script, README, swarm.yaml entry   | 0 (§5)      |

Below minimum is a quality blocker. Above 10 is rarely useful: the
eleventh tends to be redundant.

### Per-source capture (worker's scratch log, NOT in final brief)

| Field           | Format         | Example                                          |
|-----------------|----------------|--------------------------------------------------|
| URL             | full https     | `https://stripe.com/pricing`                     |
| Key claim       | one sentence   | "Stripe leads usage-based; flat tiers hidden"    |
| Relevance score | 1–5            | `4` (relevant, B2B-only)                         |

Five-point scale: **5** primary, will cite · **4** supporting, likely cited
· **3** adjacent context · **2** tangential, dropped · **1** off-topic,
recorded only so you don't re-find it. Anything ≤ 2 stays out of the brief;
anything ≥ 4 should be footnoted (§4).

### From sources to insight (synthesis)

The deliverable is not a list of summaries. A worker who reports "Stripe
does X, Linear does Y, Vercel does Z" has summarized, not synthesized.
Synthesis asks: **what do these sources, taken together, imply about the
choice in front of us?**

Format: "**X and Y together imply Z, which means our wedge is W.**"

Example: usage-based reads premium for dev infra (X); flat-tier reads safe
for operator-buyer SaaS (Y); persona is operator-buyer with monthly budget
volatility — *together* they imply our audience will distrust usage-based as
"bills I can't predict", so **our wedge is a flat-tier headline with a
usage-based overage line below it (W)**. One insight grounded in three
sources. A brief carries 3–5. Pure summaries get sent back for resynthesis.

### Citation format

Follows `nexoura-artifact-conventions` (T3). In the brief:

- Inline: bracketed index, e.g. `Operator-buyers prefer flat tiers [3].`
- Footnote: `[3] Linear pricing — https://linear.app/pricing — accessed
  2026-05-21.`
- Every URL gets an ISO 8601 access date — web pages drift, the date is
  the audit trail.
- If Firecrawl-snapshotted, cite the snapshot:
  `... — snapshot: _assets/research/linear-pricing.md`. Snapshots are
  encouraged when the artifact materially depends on the source.

---

## §4 Research brief format (the deliverable)

The brief is the unit of output for Round 0. Consumed by PM (T20
`nexoura-pm-decisions`); feeds Round 1 of T19. Shape it for a PM's
90-second read, not for your notes.

### Shape: one page, visual, decision-grade

A **single-page HTML artifact**, dark-themed, NEXOURA-branded, rendered
via the T15 `nexoura-output-formatting` template. Four blocks, only four:

1. **3–5 key findings** — one line each, each ending with a footnote ref.
2. **2–3 recommended directions** — visual cards. Each: name, one-sentence
   thesis, "best for" line, "risk" line.
3. **1 PM decision needed** — single decision, framed binary (yes/no) or
   small-choice (A/B/C). The brief exists to *unblock* PM, not to hand
   them homework.
4. **Source footnotes** — numbered list at bottom: URLs, access dates,
   snapshot paths where relevant.

Methodology notes, source-by-source summaries, and the worker's internal
debate live in a separate `research-log.md` in `_assets/research/`, not in
PM's brief.

### Why one page

PMs (and the founder, when cc'd) read briefs in the cracks. Two pages get
skimmed; five pages get deferred to "later" and Round 1 stalls. One page
forces the worker to *do the synthesis* (§3) rather than punting synthesis
cost to the reader.

### Concrete examples (committed in this skill)

Two worked examples ship next to this SKILL.md:

- `examples/sample-brief.html` — "B2B SaaS pricing page patterns" — 5
  findings, 3 directions, 1 decision (flat-tier vs usage-based vs hybrid).
- `examples/sample-brief-pharma.html` — "Pharma supply-chain UX standards"
  — same shape, different domain (regulated, RTL-bilingual,
  compliance-led).

Both render standalone (no build step) and are reference implementations a
worker copies and adapts rather than re-authoring.

### Visual language alignment with T20

The brief MUST use the decision-card patterns from T20
`nexoura-pm-decisions`: 3px gradient left-border on H2s, status pills for
`[RECOMMENDED]` / `[CONTRARIAN]` / `[BLOCKED-IF-CHOSEN]`, recommendation
cards as a 3-column grid collapsing to 1-column under 720px. **Do not
re-invent the visual language.** A brief that looks different from a PM
decision card creates two mental models for PM; one is enough.

---

## §5 When NOT to research

Research is a cost. Justified for authoring work whose output is consumed by
a human, defends a money decision, or sits in a client's hand. Wasted on
four categories — reaching for Exa on any of them is the wrong reflex.

1. **Pure execution.** Running a known script, applying a known patch,
   bumping a version, regenerating a fixture. Correctness criterion is "did
   the script exit 0", not "did we ground the approach". Just run it.

2. **Internal infra files.** SKILL.md edits, `swarm.yaml` worker
   registrations, profile SOUL.md / MEMORY.md seeds, `.gitignore` lines,
   config keys. Audience is other NEXOURA agents. Shape is dictated by the
   meta-skill (T13, T1, T3), not external research. Read meta-skill, ship.

3. **Verification and testing.** A verifier runs the checks the brief
   prescribes. A test writer writes tests for behavior in the spec. Neither
   researches "industry best practice for verification/testing".

4. **Operational artifacts.** Internal READMEs, commit messages, PR bodies,
   verification reports, inter-worker chatter. Not external artifacts
   (`nexoura-output-formatting` §6 decision tree). Brand them plain.

Uncertain whether a task is authoring (research-required) or execution
(research-skipped)? Test: **will a human read this as a standalone artifact
and form an opinion or make a decision based on it?** Yes → research. No →
ship plain.

---

## §6 Working examples

Two complete briefs ship as reference implementations. Self-contained HTML —
Sora/Inter via Google Fonts, falls back to system-ui offline. No build step.

**`examples/sample-brief.html` — B2B SaaS pricing patterns.** 5 findings
(flat vs usage vs hybrid prevalence, CTA pattern, feature-grid depth, social
proof placement, enterprise framing). 3 directions: Flat-tier-first,
Usage-based-first, Hybrid-headline. 1 PM decision. 6 footnoted sources
(Stripe, Linear, Vercel, Notion, Figma, Mutiny). Template for any pricing,
packaging, or landing-page brief.

**`examples/sample-brief-pharma.html` — Pharma supply-chain UX.** 5 findings
(dense-table density, batch/lot primacy, multi-step confirms on destructive
actions, bilingual-RTL handling, audit-log permanence). 3 directions:
Compliance-first, Operator-first, Bilingual-first. 1 PM decision. 6 sources
(SAP, Oracle SCM, Veeva, Tracelink, regulator guidance, regional case study).

Workers picking up a new-domain card start from whichever example is closer
and adapt. Both use the NEXOURA palette from `docs/nexoura-brand-spec.md`
and follow T15 `nexoura-output-formatting` status-pill conventions.

---

## §7 Integration with iteration (T19)

Research-first is Round 0 of T19 `nexoura-iteration-framework`. The handoff
is concrete and one-directional: the brief from §4 is the *input* to Round
1, not a sibling.

### Round 0 → Round 1 handoff

| Round | Output                                                   | Input to next round              |
|-------|----------------------------------------------------------|----------------------------------|
| 0     | Research brief (§4): 3–5 findings, 2–3 directions, 1 dec | Brief + PM's decision on it      |
| 1     | Concept divergence — 3 concepts, one per direction       | All 3 side-by-side, to PM        |
| 2     | Convergence — 1 chosen concept to draft fidelity         | Draft to PM for refinement notes |
| 3     | Refinement — draft → polished artifact                   | Artifact to gate review          |

Round 1 cannot start until PM answers the §4 decision. The brief is the
unblocking artifact; PM's answer is the unblocking event. If PM declines
("explore all three"), that is a Round 0 outcome — log it, develop all
three in Round 1 — but PM must explicitly say so. A worker who proceeds
without the decision is jumping the gate.

### Why Round 0 exists as a distinct round

Folding research into Round 1 — "I'll research as I go in parallel with the
first concept" — collapses Round 0 and loses §3 synthesis. The worker drafts
a concept, retrofits sources to defend it, and the concept is grounded in
confirmation bias. Separating the rounds forces synthesis *before*
committing to a direction.

### When Round 0 is skipped

Only when (a) the task falls under §5, or (b) PM has explicitly waived it —
usually because the engagement is on a refinement loop and the source base
is established. "PM didn't ask for research" is not a waiver; PM's defaults
assume research happened. The worker who silently skipped Round 0 owns the
quality failure when PM later asks "where does this come from".

---

## Cross-references

- **`nexoura-platform-doctrine`** — HONESTY and VERIFICATION REFLEX
  underwrite every claim in a brief. §4 lesson #3 (zero-hit overreach) is
  this skill's anchor precedent.
- **`nexoura-artifact-conventions`** (T3) — citation format,
  `_assets/research/` structure for snapshots, bilingual filename rules.
- **`nexoura-output-formatting`** (T15) — branded HTML template the brief
  renders into; status-pill markers; the §6 decision tree on when to
  brand at all.
- **`nexoura-iteration-framework`** (T19) — consumes the brief as Round 0
  → Round 1 input.
- **`nexoura-pm-decisions`** (T20) — decision-card visual language the brief
  reuses for its "1 PM decision needed" block.

This skill is the grounding layer.
