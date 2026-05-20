# architecture-director MEMORY.md

## Persistent lessons (cross-session, applies to all engagements)

### Verification reflex (see platform-doctrine §2)
- Every tech-stack claim verified against pinned versions, not assumed (lesson: stack drift between BRD and reality).
- Spot-check at least 2 cited integration points before claiming a system is wired (§2(d)).
- Never claim a KSA integration is "in place" without explicit grep on config + endpoint (§2(a) — no absence claim without a grep).

### File size targets are SOFT caps (see platform-doctrine §7)
- 30% over target acceptable if content is dense, not padded. Compress prose, never drop citations or lessons.

### Anti-temptation (see platform-doctrine §3, §8)
- I RECOMMEND tech choices, Omar DECIDES (all ADRs). Never auto-approve a gate (§3.2).
- I never self-merge PRs (§8). Terminal output ends "Not merged. Awaiting your call."
- I never silently override BRD tech specs — flag conflicts, let Ops/CFO arbitrate (§4 lesson 4).

### Engagement exceptions
- Tenant Zero exception pattern: see docs/engagement-exceptions.md.
- Phmco / Supply Chain SaaS = Tenant Zero (Stage 1 bypass).
- BRD↔Ops contradiction lesson (§4.4): client tech specs may disagree with BRD — Ops/CFO authoritative per Phmco precedent. Run cross-doc contradiction sweep before any downstream architecture work opens.

### Reviewer pattern
- Adversarial review (3 workers + 1 reviewer) proven Phase 6 Day 1.
- Use for ADRs touching multi-tenant boundaries, security, KSA-regulated integrations.

### Domain-specific lessons
- ADR discipline: every significant tech choice gets an ADR with Why-not alternatives.
- KSA integrations mandatory for KSA-deployed products: ZATCA, Fasah, Nafath, Wathq.
- Stack pinned: Next.js 16, React 19, Supabase, BullMQ — see T9 (do not redecide per engagement).
- BRD↔Ops contradiction: when client tech spec conflicts with BRD, Ops/CFO wins (Phmco precedent, §4.4).

### Memory ecology
- For Hermes memory layers, see T14: nexoura-memory-and-evolution.
- This file auto-consolidates when full per Hermes pattern. New lessons append here; superseded rules deprecated, not deleted.
