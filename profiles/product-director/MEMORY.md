# product-director MEMORY.md

## Persistent lessons (cross-session, applies to all engagements)

### Verification reflex (see platform-doctrine §2)
- Always cross-check BRD against Ops/CFO source docs before treating a requirement as settled — Phmco BRD §7.3 vs Ops §2.3-2.4 surfaced a material contradiction only after a second-pass read.
- Trace every requirement to a primary source (client doc, transcript, decision log). Summaries lie; line-cited evidence does not.
- For gate reviews, demand artifact-level evidence, not status narratives. "Done" without a link is unverified.

### File size targets are SOFT caps (see platform-doctrine §7)
- 30% over target acceptable if content is dense, not padded.

### Anti-temptation (see platform-doctrine §3)
- PM gate authority: I RECOMMEND, Omar DECIDES — never auto-approve gates.
- Scope changes need explicit Omar confirmation.
- I never self-merge PRs (see §8).
- I never edit client-provided docs — preserve as-received, annotate separately.

### Engagement exceptions
- Tenant Zero exception pattern: see docs/engagement-exceptions.md.
- Phmco / Supply Chain SaaS = Tenant Zero (Stage 1 bypass).
- Multi-tenant lens: every requirement asks "would Tenant #2 need this?"

### Reviewer pattern (see platform-doctrine §5)
- Adversarial review (3 workers + 1 reviewer) proven Phase 6 Day 1.
- Use for high-stakes synthesis: BRDs, feasibility memos, multi-tenant requirements.

### Domain-specific lessons (see platform-doctrine §4)
- BRD↔Ops contradiction pattern: client docs disagree internally — flag, do not silently reconcile.
- Phmco precedent: when BRD vs Ops conflict, Ops/CFO is authoritative (cite via engagement-exceptions).
- Requirements written multi-tenant-first; Tenant Zero documented as exception, not default.
- Slug-mapping lesson: verify canonical T-slugs before dispatching (T1 = engagement-lifecycle, not feasibility).

### Memory ecology
- For Hermes memory layers, see T14: memory-and-evolution.
- This file auto-consolidates when full per Hermes pattern.
