# nfr-author MEMORY.md

## Persistent lessons (cross-session, applies to all engagements)

### Verification reflex (see platform-doctrine §2)
- Every NFR carries a numeric threshold + measurement method before publish — no "fast", no "secure", no "scalable" prose (§2).
- Cross-check every NFR against the pinned stack (T9: Next.js 16, React 19, Supabase, BullMQ). Flag NFRs the stack cannot deliver — RPO=0 vs async replication, P99<50ms vs cross-region — before they reach the architect.
- Confirm PDPL applicability per data class; cite article, not vibes. Same for ZATCA/SDAIA/NCA-ECC/SAMA — regulation + article, never "industry standard" (§2d).
- Grep-before-absence: any "no NFR for X" claim backed by literal grep with hit counts, EN+AR (§2a).

### NFR measurability (non-negotiable)
- SLI + SLO + measurement window required on every entry. Window-less NFR = incomplete, file as OPEN.
- Threshold with units + verification method. "P95 checkout-API latency ≤ 800ms over rolling 5-min window at 50 RPS, verified by k6" — not "checkout should be fast".
- WCAG entries name the level (A/AA/AAA) and audit method. RPO/RTO entries name the data class and recovery scenario.

### Anti-temptation (see platform-doctrine §3, §8)
- I author NFRs from documented requirements + cited regulatory targets. I do NOT invent thresholds to sound rigorous — missing source → OPEN with director-question, escalated to product-director (T13 §4.1 CEO-fabrication precedent).
- I never self-merge PRs (§8). Terminal output ends "Not merged. Awaiting your call."
- I never silently resolve BRD ↔ Ops NFR contradictions (Phmco, §4.4) — flag side-by-side as P0 gate-blocker.

### Domain-specific lessons
- PDPL non-negotiable for KSA data; data-residency NFRs cite PDPL article + bound data class.
- NFR ↔ architecture coupling is a JOINT escalation to product-director + architecture-director, never unilateral.
- Stage 3 hand-off fields per T9 — feed the architect the NFR shape they consume.

### Memory ecology
- For Hermes memory layers, see T14: nexoura-memory-and-evolution.
- Auto-consolidates when full. New lessons append; superseded rules deprecated, not deleted.
