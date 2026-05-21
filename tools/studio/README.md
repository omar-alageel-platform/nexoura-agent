# NEXOURA Studio — Tools

This folder contains brand and copy assets for NEXOURA Studio.
Every Studio view must include `brand-preamble.html` and follow `microcopy-brief.md`.

---

## What is NEXOURA Studio?

NEXOURA Studio is the PM-facing UI layer of the NEXOURA platform.
It gives Omar a single surface to dispatch agents, review decisions,
monitor jobs, and approve or reject outputs.

The UI spec (source of truth for scope) is at:
`/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview/nexoura-studio-ui-spec.html`

---

## Files in this folder

| File | Purpose |
|---|---|
| `brand-preamble.html` | Chrome fragment — include at the top of every Studio view. Loads Sora, defines CSS tokens, renders the NEXOURA wordmark header and Studio footer. |
| `microcopy-brief.md` | Voice guide for every PM-facing string Studio will ever ship. Owned by brand-director. |
| `README.md` | This file. |

---

## brand-preamble.html

Self-contained HTML fragment. No JavaScript. No external CSS beyond Google Fonts (Sora).

It provides:
- CSS custom properties for the 4 locked brand hex codes and dark-mode surface tokens.
- The NEXOURA wordmark header with the O-ring gradient mark.
- The Studio footer: `WHERE AI BUILDS · NEXOURA Studio`.
- Studio-specific cyan accent (`#00E0FF`) for active nav and primary CTA borders only.

See: [brand-preamble.html](./brand-preamble.html)

### Planned run command (deferred to B6)

```bash
# Serve Studio locally for development
cd tools/studio
python3 -m http.server 8765
# Then open http://localhost:8765/brand-preamble.html
```

---

## microcopy-brief.md

Voice guide covering:
1. Voice principles (5 rules)
2. Banned words list with reasons
3. Preferred constructions (do/don't pairs)
4. Empty state patterns
5. Error message patterns
6. Button label patterns
7. Time and date patterns
8. Acronym policy

See: [microcopy-brief.md](./microcopy-brief.md)

---

## Brand references

- Master brand spec: [`docs/nexoura-brand-spec.md`](../../docs/nexoura-brand-spec.md)
- Brand component library (T16): [`proprietary-skills/nexoura/brand-components/SKILL.md`](../../proprietary-skills/nexoura/brand-components/SKILL.md)
- Output formatting (T15): [`proprietary-skills/nexoura/output-formatting/SKILL.md`](../../proprietary-skills/nexoura/output-formatting/SKILL.md)
- UI spec (source of truth for Studio scope): `/mnt/c/Users/Omar/OneDrive/Desktop/nexoura-preview/nexoura-studio-ui-spec.html`

---

*Studio tooling commands (serve, build, test) are deferred to B6 once all views ship.*
