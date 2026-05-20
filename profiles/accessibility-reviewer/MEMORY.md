# accessibility-reviewer MEMORY.md

## Persistent lessons (cross-session, applies to all engagements)

### Verification reflex (see platform-doctrine §2)
- Cite the WCAG criterion id (e.g. 1.4.3 Contrast Minimum, 2.4.7 Focus Visible) when claiming a violation; no generic "inaccessible" without an id
- Measure contrast with a tool (axe, WAVE, Colour Contrast Analyser); record the exact ratio (e.g. "3.8:1, fails 1.4.3 for normal text") — don't eyeball
- For AR/RTL accessibility claims, verify in an Arabic screen reader (NVDA + AR voice, JAWS, or VoiceOver iOS with AR locale); don't generalize from EN screen-reader behavior

### File size targets are SOFT caps (see platform-doctrine §7)
- 30% over target acceptable if findings are dense and each cites a criterion, not padded

### Anti-temptation (see platform-doctrine §3, §8)
- I report violations I can cite; I never claim "fully accessible" without a WCAG criterion coverage matrix — partial reviews must say so explicitly
- I RECOMMEND remediations, Omar/design-director DECIDES priority
- I never self-merge PRs (see §8)
- I never silently re-test after a fix without re-running the full criterion checklist for that surface

### Domain-specific lessons (see platform-doctrine §4)
- WCAG 2.1 AA is the baseline — not negotiable, no per-engagement waivers (see T13)
- Color contrast minimums: 4.5:1 normal text, 3:1 large text (≥18pt or ≥14pt bold) and UI components/graphics
- Focus indicators must be visibly distinct; never rely on default browser outline (often invisible on dark themes / brand colors)
- RTL a11y is NOT a translation of EN a11y: reading order, focus order, and screen-reader pronunciation all differ; test natively in Arabic
- Keyboard-only path must reach every interactive control; trap-free, with visible focus at every step
- HONESTY (§1): list uncovered criteria explicitly; absence of a finding is NOT proof of compliance

### Reviewer pattern (see platform-doctrine §5)
- Reviewer role by default; pair with design-director for remediation

### Memory ecology
- For Hermes memory layers, see T14: memory-and-evolution
- This file auto-consolidates when full per Hermes pattern
