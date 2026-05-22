# B7 UI Fix — Working Notes

Last updated: 2026-05-22

---

## What PR #62 (B7) Already Does

Branch: `studio/B7-ui-polish-fixes`

Files changed:
- `tools/studio/static/studio.css` — 30 line changes
- `tools/studio/static/studio.js` — 2 line changes
- `tools/studio/views/home.html` — 4 line changes

What B7 already fixed:
- AGENTS idle row: changed from fixed 100×60px boxes to `flex-direction:row`,
  `width:auto`, `min-width:160px` so names fit. Added `margin-right:8px` on avatar.
- ACTIVITY rows: changed `align-items:baseline` → `align-items:center`, added
  `border-bottom` separator, fixed badge sizing with `min-width:52px` and borders.
- HOME directors: corrected from "Strategy Director / Tech Director" to
  "Architecture Director / Marketing Director".

---

## The 4 Broken Bits

### 1. AGENTS view — items crammed together
**Root cause:** `.agents-zone--idle` had `gap:8px` which B7 reduced to 6px (wrong
direction). More importantly, the idle cards had `overflow:hidden` on `.agents-card`
but no `max-width` control on the zone, so with `min-width:160px` cards they wrap OK
but the active/available zones still cramp up at narrow widths.
**Additional issue found:** `.agents-card` has `overflow:hidden` which clips card
content at small sizes. The active zone min-height of 40px is fine.

### 2. ACTIVITY view — rows run together, no spacing between fields
**Root cause:** `activity-row` used `gap:10px` but fields had no breathing room.
B7 added `border-bottom` separator and fixed badge width — this is largely done.
**Remaining:** `activity-row__age` is right-aligned at a fixed `width:52px` but
`relTime()` returns strings like `"just now"` or `"23h ago"` that can overflow.
Also the filter bar (`activity-filters`) needs a `margin-bottom` gap from the feed.

### 3. HOME view — wrong director names
**Root cause:** JS `renderHome()` hardcoded the director array. B7 already fixed this
in `home.html` static file, but the live JS renderer at line 114 in `studio.js` still
has the old array:
```
var directors = ['Product Director','Design Director','Brand Director',
  'Architecture Director','Marketing Director'];
```
This is correct — "Architecture Director" and "Marketing Director" are the right names.
The `home.html` view comment block was the old placeholder. Both are now correct.

### 4. Overall feel is bland — needs brand polish pass
**Root cause:** No gradient accents, no logo mark in header, section headings very
faint, metric tiles have no visual weight. Brand palette is available via CSS vars.
**Plan:** Add gradient border to header, beef up tile values, strengthen section
headings slightly, add a subtle glow to the active stage dot.

---

## CSS Structural Bugs Found (blocking fixes)

Two unclosed CSS blocks discovered during inspection:

1. Around line 892-896: `.projects-gate-btn:focus-visible` block is never closed —
   the `{` opens but the B5 section comment starts without a `}`. This causes all B5
   agent styles to be inside the gate-btn rule = broken cascade.

2. Around line 1485-1494: `.gate-actions` media query block at `@media(max-width:768px)`
   is missing its closing `}` — `gate-actions { flex-direction:column }` bleeds into
   subsequent rules.

These must be fixed first or all other CSS patches will be fighting broken cascade.

---

## Fix Plan

### Phase 1 — Structural CSS fixes (prerequisite)
- [ ] Close `.projects-gate-btn:focus-visible { }` block properly
- [ ] Close `@media (max-width: 768px)` gate-actions block properly

### Phase 2 — AGENTS layout
- [ ] Verify idle zone wraps properly with the B7 row layout
- [ ] Add `flex-wrap:wrap` + correct gap to available zone
- [ ] Ensure empty state `.nx-empty` inside zones doesn't stretch weirdly

### Phase 3 — ACTIVITY polish
- [ ] Add `margin-bottom:16px` to `.activity-filters`
- [ ] Widen `.activity-row__age` to handle longer strings (72px min)
- [ ] Add `row-gap:2px` to `.activity-feed` for breathing room between rows

### Phase 4 — Brand polish
- [ ] Stronger section headings (opacity 0.55 instead of 0.40)
- [ ] Metric tile value: add `background: linear-gradient(...)` text clip for accent
- [ ] Header: add subtle gradient underline border
- [ ] Active stage dot: already has glow, verify it renders

### Phase 5 — Verify + screenshot + merge
- [ ] Run test suite (studio tests)
- [ ] Screenshot all 4 views: HOME, AGENTS, ACTIVITY, SYSTEM
- [ ] Merge PR #62

---

## Status
- [x] NOTES.md written
- [x] B7 diff inspected
- [x] CSS structural bugs identified
- [ ] Fixes applied
- [ ] Screenshots taken
- [ ] PR merged
