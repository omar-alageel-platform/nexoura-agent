# nexoura-output-formatting

Branded output formatting for NEXOURA · STUDIO deliverables. Converts internal Markdown into the house HTML (dark, premium, gradient-accented) and DOCX (palette-aware) used for client-facing reports, verification summaries, and stage gates.

This skill is **opt-in per artifact**. Internal scratchpads, code, SOUL.md, and configuration stay in plain Markdown. Branded rendering is reserved for documents that leave the studio or that represent a formal decision point.

---

## §1 Brand tokens

These tokens are locked. Any deviation breaks visual identity across deliverables and must be raised with the brand director before merge.

### Palette

| Token              | Hex       | Role                                              |
|--------------------|-----------|---------------------------------------------------|
| `nx-purple-500`    | `#7861FF` | Primary brand accent, headings, gradient start    |
| `nx-violet-600`    | `#5B30FF` | Gradient mid-stop, resolved-status pill           |
| `nx-blue-500`      | `#2563FF` | Gradient mid-stop                                 |
| `nx-cyan-400`      | `#00E0FF` | Verified-status pill, links, accent stripes       |
| `nx-navy-950`      | `#0A0F16` | Background (dark mode primary)                    |
| `nx-white-50`      | `#F5F7FA` | Body text on dark                                 |
| `nx-slate-900`     | `#101826` | Card backgrounds                                  |
| `nx-slate-700`     | `#475569` | Borders, secondary text                           |

### Gradient

```css
background: linear-gradient(135deg,
  #7861FF 0%,
  #5B30FF 28%,
  #2563FF 68%,
  #00E0FF 100%);
```

Use the gradient for: the O-ring logo mark, the kicker accent, the footer tagline, and at most one hero element per page. Never as a full-bleed background — calm, not loud.

### Typography

- Primary: **Sora** (300/400/500/600/700) for headings and the kicker.
- Fallback chain: `Sora, Inter, Geist, system-ui, -apple-system, sans-serif`.
- Body weight 400, headings 600, kicker 600 with `letter-spacing: 0.18em` and uppercase.
- Monospace: `JetBrains Mono, ui-monospace, 'SF Mono', Menlo` for inline code and pre blocks.

### Logo mark — the O-ring

CSS-only, no SVG asset. A 36px gradient ring rendered as a gradient-filled circle with a navy core punched out:

```html
<div class="nx-oring" aria-hidden="true"></div>
```

```css
.nx-oring {
  width: 36px; height: 36px;
  border-radius: 50%;
  background: var(--nx-gradient);
  position: relative;
}
.nx-oring::after {
  content: "";
  position: absolute; inset: 4px;
  border-radius: 50%;
  background: var(--nx-navy-950);
}
```

This is the only logotype permitted in generated documents. Always pair with the wordmark NEXOURA · STUDIO in the kicker — never alone, never with surrounding text effects.

### Tagline

**WHERE AI BUILDS** — uppercase, gradient text, footer-only. Do not repeat it in the body.

---

## §2 HTML report template structure

The pandoc template `nexoura-template.html` is a self-contained standalone HTML file. It inlines all CSS and links Sora from Google Fonts with a system-ui fallback so the document renders correctly even offline.

### Layout

```
+--------------------------------------------------------+
| KICKER (NEXOURA · STUDIO · ...)             [ O-ring ] |
| Title                                                  |
| Date · Author · Status                                 |
+--------------------------------------------------------+
|                                                        |
| (optional) Metric cards row                            |
|                                                        |
| ## Executive Summary                                   |
| ...                                                    |
|                                                        |
| ## Findings                                            |
| ### F-01  [VERIFIED pill] ...                          |
| ### F-02  [RESOLVED pill] ...                          |
|                                                        |
| ## Decisions                                           |
|                                                        |
+--------------------------------------------------------+
| WHERE AI BUILDS                            2026-05-20  |
+--------------------------------------------------------+
```

### Template variables (pandoc)

| Variable    | Source                                   | Required |
|-------------|------------------------------------------|----------|
| `$title$`   | YAML front-matter `title:`               | yes      |
| `$kicker$`  | YAML front-matter `kicker:`              | no (defaults to `NEXOURA · STUDIO`) |
| `$date$`    | YAML front-matter `date:`                | yes      |
| `$author$`  | YAML front-matter `author:`              | yes      |
| `$status$`  | YAML front-matter `status:`              | no       |
| `$body$`    | Rendered Markdown body                   | auto     |

### Metric cards

Drop a raw HTML block in the Markdown body — pandoc passes raw HTML through by default:

```html
<div class="nx-metrics">
  <div class="nx-metric">
    <div class="nx-metric-label">Findings</div>
    <div class="nx-metric-value">2</div>
  </div>
</div>
```

### Status pills

Inline spans rendered with semantic classes. The Markdown convention (§4) is to write `[VERIFIED]` style markers; for branded HTML, expand them to spans:

```html
<span class="pill-verified">VERIFIED</span>
<span class="pill-resolved">RESOLVED</span>
<span class="pill-pending">PENDING</span>
```

Color mapping:
- `pill-verified` → cyan (`nx-cyan-400`)
- `pill-resolved` → violet/purple (`nx-purple-500`)
- `pill-pending`  → slate

### Footer

Fixed layout: gradient tagline on the left, date on the right. Footer cannot be removed or replaced — it is the document's signature.

---

## §3 Pandoc reference doc for `.docx`

**Location:** `proprietary-skills/nexoura/output-formatting/reference.docx`

This file is consumed by pandoc via `--reference-doc=` when producing Word output. It defines paragraph styles, heading colors, and default font choices.

### Regenerating the default

```bash
pandoc -o reference.docx --print-default-data-file reference.docx
```

### HONESTY — current state of `reference.docx`

The committed `reference.docx` is currently **the pandoc default**, unmodified. Palette customization (heading colors to NEXOURA tokens, Sora as the default Latin font) is **deferred** because `python-docx` is not available in the studio's default dev environment and we did not want to ship a manually-edited binary without a reproducible script.

When customization lands:

1. Install python-docx in the skill's tooling venv: `pip install python-docx`.
2. Run the (forthcoming) `scripts/customize_reference_docx.py` to:
   - Set `Heading 1` color to `#7861FF`, `Heading 2` to `#5B30FF`.
   - Set the default font to Sora (fall back to Calibri on systems lacking it).
   - Adjust `Title` style to weight 600.
3. Re-commit `reference.docx`.

Until then, DOCX exports will render correctly structurally (headings, lists, tables, code blocks) but will use pandoc's default visual identity, not NEXOURA's. Flag this in any client-facing DOCX deliverable and prefer the HTML route when visual branding matters.

---

## §4 Markdown conventions

### YAML front-matter (required)

Every brandable document opens with a front-matter block:

```yaml
---
title: "Verification Report — Multi-Tenant Workspace Isolation"
kicker: "NEXOURA · STUDIO · VERIFICATION REPORT"
date: "2026-05-20"
author: "product-director"
status: "Issued"
---
```

Fields:
- `title` — sentence case, em-dash for subtitles, no trailing period.
- `kicker` — uppercase, ` · ` separators, never longer than ~50 chars. Typical pattern: `NEXOURA · STUDIO · {DOCUMENT TYPE}`.
- `date` — ISO 8601 (`YYYY-MM-DD`).
- `author` — an agent role-slug (`product-director`, `brand-director`, `tech-architect`, …) or a human name. Never anonymous.
- `status` — optional. Free-text but prefer `Draft`, `Issued`, `Superseded`.

### Required body sections

For any report-class deliverable (verification, gate review, feasibility summary, post-mortem):

1. `## Executive Summary` — one paragraph, no bullets, decision-grade.
2. `## Findings` (or `## Observations`) — one `### F-NN` heading per finding, each opened with a status pill.
3. `## Decisions` — a flat bulleted list of resolutions.
4. `## Next Steps` — optional but recommended.

For other deliverables (briefs, plans, changelogs) the schema is looser, but the front-matter is still required.

### Status markers

Inline at the start of the relevant paragraph. The canonical written form is the bracketed marker:

- `[VERIFIED]` — claim has been independently checked against evidence.
- `[RESOLVED]` — issue has been closed and the fix re-verified.
- `[PENDING]` — known gap, still open.

For branded HTML render, expand these to `<span class="pill-...">...</span>` (see §2). For DOCX render, leave the bracketed form — until §3 customization lands, pills are HTML-only.

### What not to do in the Markdown

- No emoji.
- No literal hex codes in prose (`#7861FF`) — refer to tokens by name (`nx-purple-500`).
- No raw `<style>` blocks — the template owns visual styling.
- Tables: use Markdown pipe-tables; do not hand-author HTML tables unless you need rowspan/colspan.

---

## §5 Conversion commands

All commands assume you are running from the engagement root with this skill's directory available.

### Markdown → branded HTML

```bash
pandoc input.md \
  --template proprietary-skills/nexoura/output-formatting/nexoura-template.html \
  --standalone \
  -o output.html
```

For a report inside this skill's `examples/`:

```bash
cd proprietary-skills/nexoura/output-formatting
pandoc examples/sample-report.md \
  --template nexoura-template.html \
  --standalone \
  -o examples/sample-report.html
```

### Markdown → DOCX (palette-aware)

```bash
pandoc input.md \
  --reference-doc=proprietary-skills/nexoura/output-formatting/reference.docx \
  -o output.docx
```

Until §3 customization lands, prefer HTML for client delivery and treat DOCX as a structural fallback.

### Markdown → PDF (via HTML)

```bash
pandoc input.md \
  --template proprietary-skills/nexoura/output-formatting/nexoura-template.html \
  --standalone \
  --pdf-engine=weasyprint \
  -o output.pdf
```

`weasyprint` honors the inlined CSS, so the PDF matches the HTML 1:1. If `weasyprint` is unavailable, fall back to rendering the HTML in a headless browser and printing-to-PDF.

---

## §6 When to apply

Decision tree — answer top-down, take the first match.

1. **Is this a client-facing deliverable, gate artifact, or formal verification report?**
   → Apply this skill. Output HTML (primary) and, if the recipient asked for it, DOCX.

2. **Is this an internal verification log, scratchpad, or working note?**
   → Plain Markdown. No template, no kicker. Keep it cheap.

3. **Is this `SOUL.md`, `MEMORY.md`, configuration, or any agent-internal file?**
   → Plain Markdown. Never branded. Branding here would imply these files are external artifacts, which they are not.

4. **Is this source code, schema, or machine-consumed text?**
   → Plain. Branding is content-layer; code is structure-layer.

5. **Is this a board update, sprint summary, or quick internal report?**
   → Optional. If it will be archived or shared outside the immediate squad, brand it. Otherwise plain.

When in doubt, default to **plain**. Re-rendering is one pandoc command away; over-applied branding cheapens it.

---

## §7 Examples

See the `examples/` directory in this skill:

- `examples/sample-report.md` — a minimal verification report demonstrating the full pattern: YAML front-matter, executive summary, two findings with `[VERIFIED]` and `[RESOLVED]` pills (rendered as HTML spans), decisions, next steps, and a metric-cards block.
- `examples/sample-report.html` — the output of running pandoc with `nexoura-template.html` against the sample. This file is checked in as a self-test: if the pipeline breaks, this file goes stale and the diff in PR review surfaces it.

To regenerate after editing the template or the sample:

```bash
cd proprietary-skills/nexoura/output-formatting
pandoc examples/sample-report.md \
  --template nexoura-template.html \
  --standalone \
  -o examples/sample-report.html
```

---

## §8 Anti-patterns

Things that look on-brand at first glance but are not. Reject these in review.

- **No cyberpunk neon.** The palette is purple-to-cyan but the aesthetic is calm. Avoid scanline overlays, glitch effects, oversized monospace headers, or `text-shadow: 0 0 20px ...` "glow" effects. The single permitted glow-adjacent element is the gradient itself, used sparingly.
- **No emoji.** Not in front-matter, not in headings, not in pills, not in body. Status pills replace any urge to reach for ✅ / ❌ / ⏳.
- **No overdone glow.** Drop shadows on cards: forbidden. Subtle 1px borders at `rgba(255,255,255,0.08)` only.
- **No gaming-UI metaphors.** No HUD frames, hex-grid backgrounds, faux-3D bevels, or progress bars styled like loot meters. We are a studio, not a launcher.
- **No mixing light and dark.** The template is dark-primary. Do not introduce light-mode cards on a dark page, or vice versa. A second light template may ship later — until then, dark only.
- **No alternate fonts.** Sora, Inter, Geist, system-ui — that is the entire allowed stack. No Roboto, no Montserrat, no display fonts.
- **No alternate logo treatments.** The O-ring is the mark. Do not stretch, recolor, animate, or replace it with text-only NEXOURA in a stylized face.
- **No tagline elsewhere.** WHERE AI BUILDS lives in the footer. Do not put it in the kicker, hero, or body.
- **No multi-gradient pages.** One gradient surface per document (O-ring + kicker accent + footer tagline all count as one coordinated use). Do not add a second gradient on cards, buttons, or section dividers.

If you find yourself reaching for any of the above, the answer is almost always: a smaller, calmer, more typographic version of the same idea.
