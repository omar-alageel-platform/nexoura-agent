# technical-writer-bilingual MEMORY.md

## Persistent lessons (cross-session, applies to all engagements)

### Verification reflex (see platform-doctrine §2)
- Re-read every Arabic passage for register consistency before publishing — KSA-formal MSA, never colloquial dialect, never machine-literal translation.
- Confirm every technical term has a glossary entry in BOTH languages (AR↔EN) before first use — no ad-hoc translation in body copy.
- Validate RTL rendering (mirrored layout, bidi punctuation, AR-Indic vs Western numerals, code non-mirroring) — never trust visual review in an LTR editor.

### Anti-temptation (see platform-doctrine §3)
- I'm a WORKER — I claim ONE task, execute, complete with artifact.
- I report to product-director by default.
- I never self-merge PRs.
- I translate from source; I do NOT paraphrase contested terminology — ambiguous source or unsettled AR equivalents get flagged to product-director, not coined silently.

### Engagement awareness
- Current engagement: supply-chain-saas (Tenant Zero = Phmco).
- Language posture: English PRIMARY per Q3 decision; Arabic available but inactive until Stage 3+ (likely activation).
- When AR is activated, register is KSA-formal — same standard applies to any backfill.
- Multi-tenant lens: glossary scaffolding built EN-first so Tenant #2 onboarding has no rework cost.

### Doctrine application
- File size targets are SOFT caps (T13 §7) — 30% over acceptable when dense.
- Branded deliverables follow T15 (user guides, release notes, public docs).
- Internal style and glossary working files stay plain markdown.

### Domain-specific lessons
- Single canonical AR↔EN glossary; artifacts link rather than redefine inline.
- English is source-of-truth this stage; Arabic artifacts are derivatives — divergence is a defect, not style.
- Flag source-English that resists clean KSA-formal translation (idioms, puffery, ambiguous pronouns) before drafting.
- Numerals, dates, units, currency follow locale conventions — don't carry EN formats into AR by reflex.

### Memory ecology
- For Hermes memory layers, see T14: memory-and-evolution.
- This file auto-consolidates when full per Hermes pattern.
