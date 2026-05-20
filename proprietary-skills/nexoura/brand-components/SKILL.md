# nexoura-brand-components

Reusable NEXOURA brand component library — logo lockup, O-ring mark, wordmark, color tokens (dark + light), Sora typography, buttons, cards, status pills, footer, and theme switcher. Inline this skill into any single-page HTML output so every artifact looks unmistakably NEXOURA. T15 (`nexoura-output-formatting`) handles document-shaped artifacts; this skill handles the visual primitives those documents — and any standalone HTML — share.

This file documents the primitives. Companion files in this folder are the working source of truth:

- `components.css` — the entire stylesheet (paste inline into `<style>` for portable artifacts, or `<link rel="stylesheet">` for local previews).
- `components.html` — snippet library; every primitive is wrapped in `<!-- name --> ... <!-- /name -->` markers so a downstream agent can extract a specific component cleanly.
- `nexoura-logo.html` — all 4 logo size variants (XL/LG/MD/SM) plus the standalone O-ring mark and the SVG-canonical lockup.
- `sample-page.html` — a full demo (logo + buttons + cards + pills + footer + working theme switcher with `localStorage` persistence).

The output-formatting SKILL.md does not use YAML frontmatter; this file mirrors that convention (`# title` + description paragraph). Flag if downstream tooling expects YAML.

---

## §1 Logo lockup

The lockup is the wordmark `NEX [O-ring] URA` rendered in **Sora 500** at letter-spacing `0.3em`. Four canonical sizes:

| Variant | Class           | font-size | Use                                            |
|---------|-----------------|-----------|------------------------------------------------|
| XL      | `.nx-logo--xl`  | 80px      | Cover pages, hero, splash                      |
| LG      | `.nx-logo--lg`  | 48px      | Report headers, deck title slides              |
| MD      | `.nx-logo--md`  | 32px      | Page top, email signature                      |
| SM      | `.nx-logo--sm`  | 20px      | Inline references, compact reports             |

Markup (carry verbatim — see `components.html` block `<!-- logo-lockup -->`):

```html
<span class="nx-logo nx-logo--lg">
  <span class="nx-wordmark-pre">NEX</span>
  <span class="nx-oring" aria-label="O"></span>
  <span class="nx-wordmark-post">URA</span>
</span>
```

The `.nx-oring` element is a CSS true ring (radial-gradient mask cuts an inner transparent hole — not a flat disc). The O-ring sits on the baseline with `top: 0.04em` micro-nudge for optical centering against the caps.

`nexoura-logo.html` also includes the **SVG-canonical** lockup variant. Prefer that for static exports (email, PDF, deck export) where CSS mask support is unreliable.

---

## §2 O-ring mark alone

For favicons, avatars, watermarks. Standalone (no wordmark):

```html
<!-- CSS variant -->
<span class="nx-mark nx-mark--32"></span>

<!-- SVG canonical (favicon-ready, embeds the gradient) -->
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg" aria-label="NEXOURA mark">
  <defs>
    <linearGradient id="nxg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"  stop-color="#7861FF"/>
      <stop offset="28%" stop-color="#5B30FF"/>
      <stop offset="68%" stop-color="#2563FF"/>
      <stop offset="100%" stop-color="#00E0FF"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="26" fill="none" stroke="url(#nxg)" stroke-width="5"
          filter="drop-shadow(0 0 6px rgba(120,97,255,0.35))"/>
</svg>
```

Geometry rules (locked):

- Outer diameter `1em` (or fixed-pixel via `.nx-mark--16/24/32/48/64`).
- Stroke thickness `~0.08em` (5px on the 64px SVG).
- `fill="none"` / transparent center — the page background must show through.
- Gradient 135° from `#7861FF → #5B30FF → #2563FF → #00E0FF`.
- Optional `drop-shadow(0 0 6px rgba(120,97,255,0.35))` for glow on dark surfaces.

Stakeholder rejected flat-circle attempts (filled disc) and substitute-O attempts (typographic O). The mark **must** be a true ring with a transparent interior.

---

## §3 Wordmark only

When the O-ring won't render reliably (plain-text channels, screen readers reading raw text, monospace contexts), fall back to the plain Sora wordmark with the same `0.3em` tracking. The letters stay flat — **never** apply the gradient to the letterforms themselves.

```html
<span class="nx-wordmark">NEXOURA</span>
```

---

## §4 Color tokens

Defined as CSS custom properties on `:root`. Brand accents are theme-invariant; surface colors flip between dark (default) and light (via `[data-theme="light"]`).

### Brand accents (locked, both themes)

| Token         | Hex       | Role                                           |
|---------------|-----------|------------------------------------------------|
| `--nx-purple` | `#7861FF` | Primary accent, gradient start                 |
| `--nx-violet` | `#5B30FF` | Gradient mid-stop                              |
| `--nx-blue`   | `#2563FF` | Gradient mid-stop                              |
| `--nx-cyan`   | `#00E0FF` | Gradient end, links, RESOLVED pill             |
| `--nx-grad`   | (see CSS) | 135° gradient through all 4 accents            |
| `--nx-glow`   | `0 0 18px rgba(120,97,255,0.35)` | Primary glow shadow      |

### Dark surface (default)

| Token              | Hex/Value | Role             |
|--------------------|-----------|------------------|
| `--bg-primary`     | `#0A0F16` | Page background  |
| `--bg-elevated`    | `#101826` | Cards            |
| `--text-primary`   | `#F5F7FA` | Body text        |
| `--text-secondary` | `#94A3B8` | Muted text       |

### Light surface (`[data-theme="light"]`)

| Token              | Hex/Value | Role             |
|--------------------|-----------|------------------|
| `--bg-primary`     | `#FFFFFF` | Page background  |
| `--bg-elevated`    | `#F5F7FA` | Cards            |
| `--text-primary`   | `#0A0F16` | Body text        |
| `--text-secondary` | `#475569` | Muted text       |

`prefers-color-scheme: light` auto-applies the light surface when the user has not pinned a theme.

---

## §5 Typography — Sora via Google Fonts

Sora is loaded from the Google Fonts CDN (weights 400 / 500 / 700). **Do not bundle WOFF files** — keep the skill cdn-only so artifacts stay small and the cache is shared with every other Sora-using page.

Host-page integration (preferred — `<head>`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet"
  href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;700&display=swap">
```

`components.css` also contains an `@import url(...)` fallback at the top for cases where you cannot edit `<head>`. The font stack falls back to Inter → Geist → system sans-serif if the CDN is blocked.

Weight usage: 400 body small/muted, 500 body & headings, 700 wordmark and pills.

---

## §6 Buttons

Three primitives. All use Sora 600 / 14px / 0.02em tracking / 8px radius / `transition` on transform + box-shadow.

| Class                | Visual                                    |
|----------------------|-------------------------------------------|
| `.nx-btn--primary`   | Gradient fill (`--nx-grad`), glow shadow  |
| `.nx-btn--secondary` | Outline, purple text on `--border-strong` |
| `.nx-btn--ghost`     | Transparent, muted text → purple on hover |

States (all variants):

- `:hover:not(:disabled)` — primary lifts `translateY(-1px)` and intensifies glow; secondary and ghost gain `--bg-tint` background.
- `:focus-visible` — `2px` cyan outline at `2px` offset (accessibility — ring must remain visible).
- `:disabled` / `[aria-disabled="true"]` — `opacity: 0.45` and `cursor: not-allowed`.

```html
<button class="nx-btn nx-btn--primary">Launch project</button>
<button class="nx-btn nx-btn--secondary">View brief</button>
<button class="nx-btn nx-btn--ghost">Skip</button>
```

---

## §7 Cards

Three variants. All share `8px` radius and `20px 22px` padding.

| Class             | Treatment                                                       |
|-------------------|-----------------------------------------------------------------|
| `.nx-card`        | Elevated: `--bg-elevated` + 1px brand border + soft shadow      |
| `.nx-card--accent`| Brand-tint background + 2px gradient top edge (`::before` bar)  |
| `.nx-card--flat`  | Brand-tint background only, no border, no shadow                |

Use `--accent` to draw the eye to a key decision; `--flat` for dense grids where elevation noise gets in the way.

---

## §8 Pills (status & priority)

Carried from T15 `nexoura-output-formatting` §3 so the same status vocabulary works inside and outside generated documents. All pills are uppercase, Sora 700 / 11px / 0.10em tracking.

| Class            | Use                                       |
|------------------|-------------------------------------------|
| `.pill-verified` | Stakeholder-confirmed item (green)        |
| `.pill-resolved` | Closed/decided item (cyan)                |
| `.pill-warning`  | Attention needed, non-blocking (amber)    |
| `.pill-blocked`  | Hard block (red)                          |
| `.pill-p0`       | Severity 0 — drop everything              |
| `.pill-p1`       | Severity 1 — fix this sprint              |
| `.pill-p2`       | Severity 2 — fix soon                     |
| `.pill-p3`       | Severity 3 — scheduled                    |
| `.pill-p4`       | Severity 4 — backlog                      |

```html
<h3>Requirements <span class="pill pill-verified">Verified</span></h3>
```

---

## §9 Footer

Two-column grid: tagline left, meta right. A 2px gradient bar (`--nx-grad`) anchors the top edge. The tagline text is **WHERE AI BUILDS** (literal uppercase, `0.5em` tracking, gradient text-fill).

```html
<footer class="nx-footer">
  <div class="nx-tagline">WHERE AI BUILDS</div>
  <div class="nx-meta">NEXOURA Studio · 2026 · v1.0</div>
</footer>
```

---

## §10 Theme switcher JS

The bootstrap script runs in `<head>` *before paint* to avoid a flash of incorrect theme. The controller script (placed at end of `<body>`) wires a button to toggle `document.documentElement.dataset.theme` and persists to `localStorage` under the key `nx-theme`.

```html
<!-- in <head>, before any rendered content -->
<script>
  (function() {
    try {
      var stored = localStorage.getItem('nx-theme');
      var prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
      document.documentElement.setAttribute(
        'data-theme', stored || (prefersLight ? 'light' : 'dark'));
    } catch (e) {
      document.documentElement.setAttribute('data-theme', 'dark');
    }
  })();
</script>

<!-- toggle button anywhere in the page -->
<div class="nx-theme-toggle">
  <button id="themeToggle" class="nx-btn nx-btn--secondary">Theme</button>
</div>

<!-- at end of <body> -->
<script>
  document.getElementById('themeToggle').addEventListener('click', function () {
    var current = document.documentElement.getAttribute('data-theme') || 'dark';
    var next = current === 'dark' ? 'light' : 'dark';
    document.documentElement.setAttribute('data-theme', next);
    try { localStorage.setItem('nx-theme', next); } catch (e) {}
  });
</script>
```

A full working version with iconography, label updates, and `prefers-color-scheme` change listener lives in `sample-page.html`.

---

## §11 Usage guide

Two integration patterns:

**Pattern A — single-file portable artifact (preferred for client deliverables).** Paste the entire contents of `components.css` into a `<style>` block in `<head>`. The artifact is then self-contained: one HTML file with no external CSS dependency, only the Google Fonts CDN call. Use this for any HTML that will be emailed, attached, or rendered offline.

**Pattern B — local preview / multi-page site.** `<link rel="stylesheet" href="components.css">` and serve the folder. Use this for `sample-page.html`-style demos and the component library while iterating.

Bare minimum boilerplate for a new branded HTML output:

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;700&display=swap">
  <style>/* paste components.css here for Pattern A */</style>
  <script>/* theme bootstrap from §10 */</script>
</head>
<body>
  <!-- logo, content, footer -->
</body>
</html>
```

When in doubt, copy `sample-page.html` and edit the body.

---

## §12 What NOT to do

- **No plain `NEXOURA` text** in places that need the logo. The lockup is the brand. If the O-ring won't render, fall back to §3 wordmark — never substitute a bare word.
- **No substitute O** (typographic capital O, ⭕ emoji, ◯ unicode). The O slot is the gradient ring or nothing.
- **No gradient fill on wordmark letters.** The letters stay flat in `--text-primary`. The only gradient text in the system is the footer tagline.
- **No gaming / cyberpunk treatments.** No neon glows beyond the spec'd `--nx-glow`, no chrome bevels, no scanlines, no animated rainbow gradients, no Orbitron / Audiowide / Eurostile font substitutions. NEXOURA reads as premium operator, not arcade.
- **No bundled WOFF files.** Sora ships via Google Fonts CDN only (§5). Bundling fonts bloats artifacts and fragments cache.
- **No theme-color hardcoding.** Always reference `var(--text-primary)` / `var(--bg-primary)` etc. so the light/dark flip works automatically.
- **No re-rolling the palette.** The four brand hex codes (`#7861FF`, `#5B30FF`, `#2563FF`, `#00E0FF`) are locked. Add semantic tokens that *reference* them; never introduce a fifth accent.
