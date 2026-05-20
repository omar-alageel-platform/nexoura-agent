# nexoura-output-formatting

Branded output formatting for NEXOURA · STUDIO deliverables. Converts internal Markdown into the house HTML (dark, premium, gradient-accented) and DOCX (palette-aware headings) for client-facing reports, gate artifacts, and stage-transition summaries.

Opt-in per artifact. Code, `SOUL.md`, config, and inter-worker chatter stay in plain Markdown. Branded rendering is reserved for documents that leave the studio or represent a formal decision point. §6 has the decision rule, anchored in `nexoura-platform-doctrine` §7 (Artifact quality).

---

## §1 Brand tokens

Locked. Deviation breaks visual identity across deliverables and must be raised with the brand director before merge. Source of truth: the NEXOURA brand spec; values below are the working copy used by this skill's template.

### Palette

| Token             | Hex       | Role                                              |
|-------------------|-----------|---------------------------------------------------|
| `nx-purple-500`   | `#7861FF` | Primary brand accent, kicker, gradient start      |
| `nx-violet-600`   | `#5B30FF` | Gradient mid-stop, H1/Title colour in DOCX        |
| `nx-blue-500`     | `#2563FF` | Gradient mid-stop, H3 colour in DOCX              |
| `nx-cyan-400`     | `#00E0FF` | Gradient end, links, RESOLVED pill                |
| `nx-navy-950`     | `#0A0F16` | Dark-mode background (primary surface)            |
| `nx-white-50`     | `#F5F7FA` | Body text on dark                                 |
| `nx-slate-900`    | `#101826` | Pre/code blocks, deep surface                     |
| `nx-slate-700`    | `#475569` | Secondary borders, H4 colour in DOCX              |

### Signature gradient

```css
background: linear-gradient(135deg, #7861FF 0%, #5B30FF 28%, #2563FF 68%, #00E0FF 100%);
```

Used for the O-ring, H2 left-border accent, and footer tagline. At most one coordinated gradient surface per document. Never a full-bleed background.

### Typography

- Primary: **Sora** (300 / 400 / 600 / 700) — headings, kicker, metric values, tagline.
- Body: **Inter** 400 / 500 / 600 — paragraphs, lists, tables.
- Fallback chain: `Sora, Inter, Geist, system-ui, -apple-system, sans-serif`.
- Monospace: `ui-monospace, 'JetBrains Mono', Menlo, Consolas`.

Google Fonts CDN link is in the template `<head>`; offline fallback in §2.

### Logo — the O-ring

CSS-only, no SVG. A 48×48 gradient ring with a navy core, rendered via `::before` (inner navy fill) and `::after` (small gradient dot). Always paired with the `NEXOURA · STUDIO` wordmark in the kicker; never standalone.

### Tagline

**WHERE AI BUILDS** — uppercase, gradient text, footer only.

---

## §2 HTML report template

`nexoura-template.html` is a self-contained standalone HTML document with all CSS inlined. The only external dependency is the Google Fonts `<link>` for Sora + Inter; if it fails to load, the `system-ui` fallback chain takes over (typography degrades, layout and palette do not).

**Offline fallback.** For air-gapped delivery, download Sora and Inter `.woff2` into a sibling `fonts/` directory and replace the Google Fonts `<link>` with a local `@font-face` block. Otherwise zero-dependency: no JS, no external images, no remote stylesheets.

### Layout (top to bottom)

Header (kicker pill + Sora 700 title + Inter subtitle; right side: O-ring, date, author). Optional metric-card grid (auto-fit, minmax(220px, 1fr)). Body sections — H2 with 3px gradient left-border, body Inter 16px line-height 1.7. Status pills inline. Footer — NEXOURA wordmark left, gradient `WHERE AI BUILDS` centre, build timestamp right.

### Placeholders

The template uses brace-delimited placeholders (not pandoc-native `$var$`) so it can be populated by any string-substitution renderer:

| Placeholder           | Source                                    | Required |
|-----------------------|-------------------------------------------|----------|
| `{{TITLE}}`           | YAML `title:`                             | yes      |
| `{{KICKER}}`          | YAML `kicker:` (default `NEXOURA · STUDIO`) | no     |
| `{{SUBTITLE}}`        | YAML `subtitle:`                          | no       |
| `{{DATE}}`            | YAML `date:` (ISO 8601)                   | yes      |
| `{{AUTHOR_PROFILE}}`  | YAML `author_profile:`                    | yes      |
| `{{BODY_HTML}}`       | Pandoc-rendered Markdown body fragment    | yes      |
| `{{METRICS_HTML}}`    | Hand-authored metric-card HTML block      | no       |
| `{{TIMESTAMP}}`       | Build-time UTC stamp (injected)           | yes      |

### Populating the template

Two supported paths:

1. **`render.py`** (bundled). Parses front-matter, runs `pandoc -f markdown -t html` on the body, expands `[STATUS]` markers into pill spans, substitutes placeholders. Used to produce `examples/sample-report.html`.
2. **Hand substitution** — placeholders are plain `{{NAME}}` tokens; a `sed`/Python/Node one-liner suffices.

Pandoc's native `--template` mode is **not** wired to this file (would require renaming placeholders to `$title$`/`$body$`/etc.). Keeping brace syntax preserves renderer flexibility and avoids pandoc-version coupling.

### Status pills

```html
<span class="pill pill-verified">VERIFIED</span>
<span class="pill pill-resolved">RESOLVED</span>
<span class="pill pill-pending">PENDING</span>
<span class="pill pill-blocked">BLOCKED</span>
```

In source Markdown write the bracketed marker (`[VERIFIED]`); `render.py` expands it.

### Metric cards

Injected into `{{METRICS_HTML}}`:

```html
<div class="nx-metric">
  <div class="label">Cache hit</div>
  <div class="value">87%</div>
  <div class="delta">target ≥ 85%</div>
</div>
```

The `nth-child(3n+2 / 3n+3)` rule rotates value colour through purple / blue / cyan automatically.

---

## §3 Pandoc reference doc for `.docx`

**Location:** `reference.docx` next to this SKILL.md. Pandoc consumes it via `--reference-doc=` to inherit paragraph styles, heading colours, and default fonts.

### Generation

```bash
# 1. Emit pandoc's stock reference (one-time)
pandoc -o reference.docx --print-default-data-file reference.docx
# 2. Patch heading colours to the NEXOURA palette
python3 patch_reference_docx.py
```

`patch_reference_docx.py` (bundled) opens the `.docx` as a zip, edits `word/styles.xml`, and writes `<w:color w:val="…">` entries onto the `Heading1`/`Heading2`/`Heading3`/`Heading4`/`Title`/`Subtitle` blocks. No `python-docx` dependency — stdlib only.

### Customization status — HONESTY

The committed `reference.docx` **has been patched**: heading colours map to the palette (H1 violet-600, H2 purple-500, H3 blue-500, H4 slate-700, Title violet-600, Subtitle purple-500). Verified by regenerating sample DOCX against it.

What is **not** yet customized (TODO, low priority):

- Default Latin font (still pandoc's Calibri-equivalent, not Sora). Embedding Sora requires shipping the font into the docx package and editing `word/fontTable.xml` — fragile across Word versions.
- Footer/header gradient tagline. Word does not render CSS gradients; would need a pre-rendered image in `word/media/`.
- Status pills. DOCX has no inline-span equivalent; the bracketed `[VERIFIED]` marker is left as plain text — readers see the marker, not a styled pill.

Reproduce the patch from scratch:

```bash
rm reference.docx
pandoc -o reference.docx --print-default-data-file reference.docx
python3 patch_reference_docx.py
```

### Usage

```bash
pandoc input.md --reference-doc=reference.docx -o output.docx
```

For client deliverables where visual fidelity matters, **prefer HTML**. DOCX is the structural fallback for stakeholders who must edit in Word.

---

## §4 Markdown conventions for branded reports

### YAML front-matter (required)

```yaml
---
title: "Architecture Review — Phoenix Migration"
kicker: "NEXOURA · STUDIO"
subtitle: "Tech-stack evaluation and gap analysis"
date: "2026-05-20"
author_profile: "T20 · solution-architect"
status: "draft"
---
```

- `title` — sentence case, em-dash for subtitles, no trailing period.
- `kicker` — uppercase, ` · ` separators, ~50 char max. Pattern: `NEXOURA · STUDIO` or `NEXOURA · STUDIO · {DOC TYPE}`.
- `subtitle` — single line, ≤ 64ch.
- `date` — ISO 8601 (`YYYY-MM-DD`).
- `author_profile` — agent role-slug or human name. Never anonymous.
- `status` — `draft` / `issued` / `superseded`.

### Required body sections (report-class deliverables)

For verification reports, gate reviews, feasibility summaries, architecture reviews, security audits, post-mortems:

1. `## Executive Summary` — one paragraph, decision-grade, no bullets.
2. `## Findings` — bulleted or `### F-NN`-headed, each ending in a `[STATUS]` marker.
3. `## Decisions` — flat numbered list.
4. `## Verification` — how each finding was checked (commands, file:lines, commit SHAs).
5. `## Citations` — file paths + line numbers, URLs, or commit SHAs. Non-negotiable per platform-doctrine §7.

### Status markers

Bracketed in source; renderer converts to a pill span.

- `[VERIFIED]` — independently checked against evidence (green).
- `[RESOLVED]` — issue closed and fix re-verified (cyan).
- `[PENDING]` — known gap, still open (amber).
- `[BLOCKED]` — cannot progress without external input (red).

DOCX: bracketed form is left as plain text (§3).

### What not to put in the Markdown

- No emoji.
- No literal hex codes in prose — use token names (`nx-purple-500`, not `#7861FF`).
- No raw `<style>` blocks — the template owns styling.
- Tables: Markdown pipe-tables. Raw HTML tables only for rowspan/colspan.

---

## §5 Conversion commands

Assume cwd is `proprietary-skills/nexoura/output-formatting/`.

### Markdown → branded HTML (bundled renderer)

```bash
python3 render.py examples/sample-report.md examples/sample-report.html
```

Handles front-matter parsing, pandoc body conversion, status-pill expansion, placeholder substitution.

### Markdown → branded HTML (pandoc-only, manual swap)

```bash
BODY=$(pandoc -f markdown -t html < input.md)
sed -e "s|{{TITLE}}|My Title|" \
    -e "s|{{BODY_HTML}}|${BODY}|" \
    -e "s|{{DATE}}|2026-05-20|" \
    nexoura-template.html > output.html
```

Works for simple cases. For real content `render.py` is more robust (handles `|` and `&` in body).

### Markdown → DOCX

```bash
pandoc input.md --reference-doc=reference.docx -o output.docx
```

### Markdown → PDF (via branded HTML)

```bash
python3 render.py input.md /tmp/input.html
weasyprint /tmp/input.html output.pdf
```

`weasyprint` honours inlined CSS; PDF matches HTML 1:1. Otherwise headless-browser print-to-PDF.

### Limitations (HONESTY)

- Native pandoc `--template nexoura-template.html` will **not** work — file uses `{{NAME}}` placeholders, not pandoc `$name$`. Intentional. See §2.
- `render.py` injects `{{METRICS_HTML}}` as empty unless front-matter declares a `metrics_html` field. The sample patches metrics in via `build_sample.py` — a thin demo of how production pipelines compose metrics from upstream data.

---

## §6 When to apply — decision tree

Anchored in `nexoura-platform-doctrine` §7 (Artifact quality): density beats compression compliance, citations are non-negotiable, audience drives presentation.

Top-down, take the first match:

1. **Will a stakeholder, PM, client, or future engineer without context read this STANDALONE as a finished artifact?**
   → Branded. Apply this skill. HTML primary, DOCX if recipient asked.
2. **Tooling output, CI/CD log, internal verification report consumed by an orchestrator, or inter-worker chatter?**
   → Plain Markdown. No template.
3. **Source code, schema, config, `SOUL.md`, `MEMORY.md`, `swarm.yaml`, or any agent-internal file?**
   → Plain. Branding implies external artifact status; these are not external.
4. **One-off scratchpad or sprint micro-update?**
   → Plain. If archived or escalated later, brand it then.

### Branded (apply this skill)

PRDs · gap analyses · executive summaries · brand books · GTM plans · ADRs · architecture review reports · tech-stack evaluations · security audits · test/QA reports · performance and load reports · multi-file code review syntheses · stage-transition reports · cost and capacity reports · post-mortems · client-facing feasibility summaries.

### Not branded

Individual code files (`.ts`/`.py`/`.yaml`/`.json`/`.md` source) · internal verification reports with raw tables · CI/CD logs · inter-worker quick reports · `SOUL.md` / `MEMORY.md` / `swarm.yaml` / config · scratchpads · commit messages · PR bodies.

When in doubt, default to **plain**. Re-rendering is one command away; over-applied branding cheapens the mark.

---

## §7 Examples

See `examples/`:

- `examples/sample-report.md` — minimal architecture-review sample: full front-matter, exec summary, five findings spanning all four status states, decisions, verification, citations.
- `examples/sample-report.html` — rendered output of `python3 build_sample.py` (wraps `render.py` and injects three metric cards). Self-test: pipeline regression goes stale here and the PR diff surfaces it.

**Screenshot description** (rendered HTML in a browser): dark navy page; top-left a small purple kicker pill `NEXOURA · STUDIO`; below it the Sora title; top-right a 48px gradient O-ring above date and author. Three metric cards (Findings · Cache hit · Failover p50) — values purple, blue, cyan. Body sections open with a 3px gradient left-border H2. Five findings end in coloured pills (green/cyan/amber/red). Footer: NEXOURA wordmark, gradient `WHERE AI BUILDS`, UTC timestamp.

Regenerate:

```bash
cd proprietary-skills/nexoura/output-formatting
python3 build_sample.py
```

---

## §8 Anti-patterns

Reject these in review.

- **No cyberpunk / gaming neon.** Palette is purple→cyan but aesthetic is calm. No scanline overlays, glitch effects, oversized monospace headers, or `text-shadow: 0 0 20px …` glow stacks.
- **No emoji.** Not in front-matter, headings, or body. Status pills replace ✅ / ❌ / ⏳.
- **No overdone gradient.** Maximum one coordinated gradient surface per document (O-ring + H2 borders + footer tagline = one coordinated use). No gradient cards, buttons, or dividers.
- **No drop shadows on cards.** Subtle 1px borders at `rgba(120,97,255,0.20)` only.
- **No HUD / loot-meter metaphors.** No hex-grid backgrounds, faux-3D bevels, or game-UI progress bars.
- **No light-on-dark mixing.** Template is dark-primary. A light template may ship later; until then dark only.
- **No alternate fonts.** Sora / Inter / Geist / system-ui is the entire allowed stack.
- **No alternate logo treatments.** The O-ring is the mark. Do not stretch, recolour, animate, or replace with stylized text-only NEXOURA.
- **No tagline elsewhere.** `WHERE AI BUILDS` is footer-only.
- **No all-caps body text.** All-caps is reserved for kicker, pills, wordmark, tagline.
- **No neon green or magenta-pink accents.** Those are gaming palettes. Pill colours (green-VERIFIED, red-BLOCKED) are muted; do not promote them to body accents.
- **No animated GIFs, no auto-playing video, no embedded fonts beyond Sora/Inter.** Static, premium, intelligent — not flashy.

If you find yourself reaching for any of the above, the answer is almost always a smaller, calmer, more typographic version of the same idea.

---

## Cross-references

- **`nexoura-platform-doctrine` §7** — Artifact quality; size budgets and citation non-negotiables that constrain §4 and §6.
- **`nexoura-platform-doctrine` §8** — No-self-merge; binds delivery of branded artifacts to Omar's merge authority.
- **`nexoura-artifact-conventions`** (T3) — file naming, directory structure, bilingual layout; citation format §4 requires.
- **`nexoura-memory-and-evolution`** (T14) — how rendering-breakage lessons feed back into §3 customization roadmap and §8 anti-patterns.
