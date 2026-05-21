---
name: nexoura-iteration-framework
description: Use when a NEXOURA worker is about to produce a creative or strategic artifact (brand concepts, visual designs, marketing copy, landing pages, product positioning, UX flows). Codifies the T19 iteration model — Round 0 research (T18), Round 1 divergent (3 concepts), Round 2 convergent (refine PM's pick), Round 3 polish. Defines concept-card presentation, feedback capture loop, and when to iterate vs ship one-shot.
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, iteration, methodology, creative-process]
    related_skills:
      - nexoura-research-first
      - nexoura-pm-decisions
      - nexoura-platform-doctrine
---

# NEXOURA Iteration Framework (T19)

How NEXOURA workers produce creative and strategic artifacts. A three-round cadence where the PM sees options early, picks a direction, and refinement happens with their feedback inside the loop instead of after a finished artifact lands.

On *methodology* (how many rounds, what to show, when to stop) this skill wins. On *brand tokens / palette / typography* `nexoura-output-formatting` (T15) wins. On *what counts as a verified claim* `nexoura-platform-doctrine` (T13) wins.

---

## §1 Why iteration beats one-shot

Every worker arrives wanting to ship a thirty-page polished document on first contact. It feels diligent. It is a PM-time tax.

A one-shot has three failure modes. The PM cannot read it under load — a long artifact asking yes/no actually asks for a forty-minute reading session they don't have. The artifact represents one direction with no way to compare against alternatives the worker silently discarded. And when the PM pushes back, the worker is N hours and 30 pages deep in a direction that has to be thrown out.

Three short rounds with explicit PM input lands closer to the target with less total work. Round 1 is cheap; if the PM picks B over A, being wrong costs half an hour, not half a week. Round 2 inherits the PM's actual taste. Round 3 is polish on a direction already ratified. This is the practical form of `nexoura-platform-doctrine` §11 (Expert Mode): the PM is a domain expert; the worker's job is to expose options at the resolution where the PM's expertise applies.

---

## §2 Round structure

Four rounds, including a Round 0 that often gets skipped and shouldn't. Time targets are rough; if a round consistently blows past 2× target, the brief is wrong, not the worker.

### Round 0 — Research (≈30 min)

Owned by `nexoura-research-first` (T18). Output: a one-page HTML research brief covering competitor landscape, audience signal, prior art the engagement has already touched, and any client-supplied references. Cited per `nexoura-platform-doctrine` §1: every claim links to a file, URL, or grep result. Without Round 0 the worker is inventing concepts from training-data priors — how brand directions converge on whatever was fashionable in 2023. Ends with a `[VERIFIED]` brief under the engagement's research directory, linked from the PR.

### Round 1 — Divergent (≈30 min)

Three directional concepts. **Visual cards, not prose.** §3 has the full spec. Each concept must be genuinely different — three flavors of one idea is one concept and two distractors, and the PM will see through it. If the worker cannot honestly produce three different directions, they ship two with the missing-third reason stated. Output: a single HTML file (`round1-concepts.html`) ready for T20 decision review.

### Round 2 — Convergent (≈20 min)

Refine the PM's chosen concept against the PM's notes. §4 governs the loop. Round 2 is **not** a fresh draft — it inherits the chosen concept wholesale and adjusts only what the PM flagged. Output references which feedback points it addressed.

### Round 3 — Polish (≈10 min)

Final pass: copy tightening, accessibility, alignment with `nexoura-output-formatting` (T15) tokens, byte-budget verification, gate-readiness check per `nexoura-gate-protocol` (T2). No new creative decisions. If a major direction question opens here, the worker has fallen back into Round 2 and must say so explicitly rather than smuggling it into polish.

Total wall-clock: ~90 min worker time, ~5 min PM time per decision point.

---

## §3 Concept presentation (Round 1)

The Round 1 deliverable is a single self-contained HTML file the PM opens in a browser and decides from. Not a slide deck. Not a Markdown document. Not a folder of PNGs. One file, three concepts side-by-side, ready to drive a T20 decision UI.

**Layout.** Three-column grid on desktop; stacks on mobile. NEXOURA-branded shell per `nexoura-output-formatting` §1: navy background, Sora display, Inter body, signature gradient on accents only. One coordinated gradient surface total — usually the kicker pill. No gradients on the concept cards themselves; gradient noise across three options makes them indistinguishable.

**Per concept, exactly these elements, in this order:**

1. **Name** — 1–3 words, Sora 700. Examples: `Quiet Authority`, `Living Network`, `BUILT FOR BUILDERS`. Avoid generic adjectives (`Modern`, `Bold`, `Clean`) — they are noise.
2. **Description** — exactly two sentences. First states the directional thesis; second states the implication for the artifact at hand. If you can't describe it in two sentences, it's not crisp enough.
3. **Visual swatch** — the actual look. Brand concept: logo treatment, palette, one typographic specimen. Homepage: a wireframe-quality hero, not lorem-ipsum. The swatch is the concept; the words are explanation.
4. **Pros** — 2–3 short bullets. What this concept does well *that the other two don't*. If a pro is true of all three, it's a baseline; cut it.
5. **Cons** — 2–3 short bullets. Where this direction is risky, expensive, or off-target. Honest cons are the credibility signal — no cons reads as a sales pitch.
6. **Recommendation footer** — one sentence at page bottom (not per-card): which concept the worker recommends and why, format `Recommend Concept B — best resolves <tension from Round 0>`.

**What not to do.** No nine-concept grids (decision fatigue). No identical concepts with one color flipped (fake variety). No `Option 1 / 2 / 3` names. No "all three are great" — then you have no recommendation.

**Self-contained.** Inline CSS, inline SVG, Google Fonts link for Sora/Inter with `system-ui` fallback, no JS, no external images. The PM may review on a plane.

---

## §4 Feedback capture loop

The framework lives or dies on what happens between Round 1 and Round 2. A vague reaction (`I like B better, let's go with that`) is not feedback — it is a vote. Workers must extract structured feedback or Round 2 becomes blind polish.

**The two-bucket prompt.** When the PM picks a concept, the T20 decision UI asks them to fill two fields:

- **AMPLIFY** — what to keep doing, more of. (`The condensed typography. The restraint on color. The way the hero copy commits to one idea.`)
- **CHANGE** — what to stop doing, or do differently. (`Drop the gradient on the CTA. Headlines too quiet — try one notch more weight. 'Built for builders' is too narrow; we serve operators too.`)

If the PM leaves either field blank, the worker requests one more pass before starting Round 2. Single-field feedback produces lopsided Round 2 outputs.

**Round 2 references its inputs.** The Round 2 HTML opens with a box: `Round 2 addresses: AMPLIFY [item 1, item 2…] · CHANGED [item 1, item 2…]`. Each item maps to a specific edit. If a piece of feedback was not addressable, the worker says so and proposes an alternative — they do not silently ignore it.

**No silent direction changes.** Round 2 inherits the chosen concept. If the worker discovers the chosen direction is fundamentally broken, they STOP Round 2 and flag back to the PM — they do not pivot to Concept A or invent Concept D under cover of "refinement". This is `nexoura-platform-doctrine` §1.3 applied to creative work.

**One pass, not many.** Round 2 is a single refinement. If the PM wants three more cycles, the framework has failed (wrong concept won Round 1, or Round 0 was thin) and the worker should escalate, not grind. Cosmetic feedback ("make it pop more") in Round 2 is a Round 3 input, deferred.

---

## §5 When to iterate vs ship one-shot

Not every artifact deserves three rounds. Iteration is expensive in PM attention; spending it on artifacts without subjective taste tradeoffs is the opposite mistake from the one-shot trap.

**Decision rule.** If the artifact has subjective taste tradeoffs that the PM's domain expertise resolves better than the worker's, iterate. If it is a constraint-driven correctness problem where the right answer is defined by external facts, ship in one pass.

**Creative — three rounds default.** Brand identity, visual design, marketing copy, product positioning, landing-page hero, naming, taglines, illustration direction, voice and tone. Three rounds is the floor — a brand identity that resolves cleanly in two rounds is rare and should be examined for skipped tradeoffs.

**Technical — one to two rounds.** ADRs, NFR specs, code-review summaries, schema designs, infra topology, capacity plans. Round 0 (prior art, constraint scan) + one implementation pass is usually sufficient. A technical artifact with three "concepts" usually means constraints weren't pinned down — tighten them rather than presenting three architectures that all might work.

**Operational — one round.** Swarm-config entries, CI scripts, runbook updates, gateway configs, manifest edits, dependency bumps. Ship it; PM changes are a normal PR-review cycle. No concept divergence — there isn't taste to query.

**Edge case — strategic narrative.** GTM plans, executive briefings, board memos, investor narratives. Creative even though they look like documents. Three rounds. Voice and audience read are exactly the expertise the worker can't replicate from training data, and one-shot strategic narratives are the highest-cost rework in the platform.

When in doubt, ask the PM at brief time. Embedding the iteration mode in the brief is cheaper than discovering it after Round 1.

---

## §6 Anti-patterns to avoid

Reject these in review. Each has bitten the platform.

- **"Perfect first draft" mentality.** A polished artifact without prior concept review. Reads confident; expensive to revise. Pause the PR and back-fill Round 1.
- **Thirty-page concept documents.** PMs don't read them. A Round 1 needing more than ten minutes' reading before the PM can decide has substituted thoroughness for clarity.
- **Concepts without explicit recommendations.** "Three options, let me know" forces blind choice. The worker's recommendation + one sentence of reasoning is part of the deliverable.
- **No clear decision point at end of Round 1.** Without a `[DECISION REQUESTED]` driving into a T20 review, the round silently extends into Round 2 with the worker guessing PM intent.
- **Skipping Round 0.** Concepts invented from training-data priors. Round 1 outputs that don't cite Round 0 get rejected as "this doesn't feel like us".
- **Round 2 that ignores feedback.** Cosmetic refinement that doesn't engage AMPLIFY / CHANGE notes. Caught by §4's feedback-mapping box. Empty box is a doctrine violation.
- **Placeholder concept names** (`Option 1`, `Concept A`). Diagnostic of a worker who didn't commit enough to label them.
- **Iterating operational artifacts.** Three concepts for a `swarm.yaml` entry. No taste here; ship it.

---

## §7 Working example

`examples/round1-sample.html` is a hypothetical Round 1 deliverable for "NEXOURA Studio public homepage hero". It demonstrates §3: three concepts (`Quiet Authority`, `Living Network`, `Built For Builders`), each with name / two-sentence description / visual swatch / pros / cons, plus a single recommendation footer. NEXOURA-branded shell, no gradient noise on the cards. Self-contained: no remote JS, no external images, Google Fonts with `system-ui` fallback.

Open it in a browser to see the target shape. When dispatching a creative worker on a Round 1 task, link to this file as the reference; do not paraphrase the layout in the brief.

---

## Cross-references

- **`nexoura-research-first` (T18)** — Round 0 owner; research-brief format and citation rules.
- **`nexoura-pm-decisions` (T20)** — Round 1 / 2 decision UI; defines the AMPLIFY / CHANGE fields §4 depends on.
- **`nexoura-output-formatting` (T15)** — brand tokens, palette, typography; the visual shell every Round 1 / 2 / 3 HTML conforms to.
- **`nexoura-platform-doctrine` (T13)** — §11 Expert Mode (philosophical anchor), §1 HONESTY (no silent direction changes), §8 no-self-merge.
- **`nexoura-gate-protocol` (T2)** — Round 3 polish ends at a gate review; this skill defers gate criteria to T2.
