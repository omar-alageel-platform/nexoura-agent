# NEXOURA Brand Components

**Skill ID:** `nexoura/brand-components`
**Reports to:** `brand-director`, `design-director`
**Refs:** T13 (doctrine), T15 (output-formatting)
**Status:** v1.0

This skill ships a self-contained, copy-pasteable brand component library for any HTML output produced under the NEXOURA Studio identity. It defines the logo lockup (including the signature O-ring), color tokens for both dark and light modes, typography scale, buttons, cards, status pills, footer pattern, and a working theme switcher.

Use this skill whenever you generate a standalone HTML deliverable, dashboard, report cover, briefing, or landing snippet. For full-document report rendering (long-form, multi-section, print-capable), defer to `nexoura/output-formatting` (T15) — this skill is the *primitive* layer; T15 is the *composition* layer.

---

## §1. Logo lockup — `N E X (O-ring) U R A`

The signature mark. The letter `O` is **replaced** by a gradient ring; it is never spelled out as a regular `O`. Wide tracking (`letter-spacing: 0.3em`) on the wordmark, Sora medium 500.

### HTML
```html
<span class="nx-logo nx-logo--lg">
  <span class="nx-wordmark-pre">NEX</span>
  <span class="nx-oring" aria-label="O"></span>
  <span class="nx-wordmark-post">URA</span>
</span>
```

### CSS (canonical — included in `components.css`)
```css
.nx-logo {
  display: inline-flex; align-items: center;
  font-family: 'Sora', sans-serif; font-weight: 500;
  letter-spacing: 0.3em; line-height: 1; white-space: nowrap;
  color: var(--text-primary); user-select: none;
}
.nx-logo--xl { font-size: 80px; }
.nx-logo--lg { font-size: 48px; }
.nx-logo--md { font-size: 32px; }
.nx-logo--sm { font-size: 20px; }

.nx-oring {
  display: inline-block; width: 1em; height: 1em; border-radius: 50%;
  background: linear-gradient(135deg,#7861FF 0%,#5B30FF 28%,#2563FF 68%,#00E0FF 100%);
  -webkit-mask: radial-gradient(circle, transparent 0 calc(50% - 0.08em),
                                #000 calc(50% - 0.08em) 100%);
          mask: radial-gradient(circle, transparent 0 calc(50% - 0.08em),
                                #000 calc(50% - 0.08em) 100%);
  box-shadow: 0 0 18px rgba(120,97,255,0.35);
  margin: 0 0.06em; position: relative; top: 0.04em;
}
```

**Size variants:**
- `--xl` (80px) — hero / cover pages
- `--lg` (48px) — page headers
- `--md` (32px) — section headers, email signatures
- `--sm` (20px) — inline / dense reports

**Honesty note (T13 §2):** The O-ring is implemented as a radial-gradient mask cutting an inner hole through a conic-style linear gradient disc. This is a CSS approximation of an SVG `<circle stroke="url(#grad)">`. It renders as a true gradient ring in all modern browsers (Chrome, Firefox, Safari, Edge 2019+). For print/PDF/email contexts where `mask` is unreliable, use the SVG variant in §2.

---

## §2. O-ring mark alone (no wordmark)

For favicons, avatars, watermarks, loading spinners.

### CSS variant
```html
<span class="nx-mark nx-mark--32"></span>
```
Sizes shipped: `--16`, `--24`, `--32`, `--48`, `--64`.

### SVG variant (preferred for favicon / email / PDF)
```html
<svg width="64" height="64" viewBox="0 0 64 64" xmlns="http://www.w3.org/2000/svg">
  <defs>
    <linearGradient id="nxg" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0%"   stop-color="#7861FF"/>
      <stop offset="28%"  stop-color="#5B30FF"/>
      <stop offset="68%"  stop-color="#2563FF"/>
      <stop offset="100%" stop-color="#00E0FF"/>
    </linearGradient>
  </defs>
  <circle cx="32" cy="32" r="26" fill="none" stroke="url(#nxg)" stroke-width="5"/>
</svg>
```

The SVG is the most portable variant — embed it as `favicon.svg`, in `<img>`, or inline.

---

## §3. Wordmark only (no O-ring)

When the O-ring would compete with surrounding UI (very tight headers, single-line footer chrome). The wordmark is *bolder* (700) to compensate for the missing visual anchor.

```html
<span class="nx-wordmark">NEXOURA</span>
```
```css
.nx-wordmark {
  font-family: 'Sora', sans-serif; font-weight: 700;
  letter-spacing: 0.3em; color: var(--text-primary);
}
```

Never gradient-fill the wordmark letters (see §12).

---

## §4. Color tokens — CSS variables

All tokens are CSS custom properties scoped to `:root`. Theme is selected by `data-theme="dark"` (default) or `data-theme="light"` on `<html>`. Brand accents are identical across themes — only surface and text shift.

### Dark mode (default)
| Token | Value | Use |
|---|---|---|
| `--bg-primary` | `#0A0F16` (nx-navy) | page background |
| `--bg-elevated` | `#101826` (slate-900) | cards, surfaces |
| `--bg-tint` | `rgba(120,97,255,0.06)` | accent fills |
| `--text-primary` | `#F5F7FA` (nx-white) | body text |
| `--text-secondary` | `#94A3B8` (slate-500) | meta, labels |
| `--border` | `rgba(120,97,255,0.18)` | hairline rules |

### Light mode (`data-theme="light"`)
| Token | Value | Use |
|---|---|---|
| `--bg-primary` | `#FFFFFF` | page background |
| `--bg-elevated` | `#F5F7FA` | cards |
| `--text-primary` | `#0A0F16` | body |
| `--text-secondary` | `#475569` (slate-700) | meta |
| `--border` | `rgba(10,15,22,0.10)` | hairline |

### Brand accents (both modes)
| Token | Value |
|---|---|
| `--nx-purple` | `#7861FF` |
| `--nx-violet` | `#5B30FF` |
| `--nx-blue` | `#2563FF` |
| `--nx-cyan` | `#00E0FF` |
| `--nx-navy` | `#0A0F16` |
| `--nx-white` | `#F5F7FA` |
| `--nx-grad` | `linear-gradient(135deg, #7861FF 0%, #5B30FF 28%, #2563FF 68%, #00E0FF 100%)` |

---

## §5. Typography

**Primary:** Sora, medium 500 default. **Fallback stack:** Inter → Geist → system.

Sora is shipped as a local asset by T15 (`proprietary-skills/nexoura/output-formatting/assets/sora-regular.{woff,ttf}`). `components.css` references it with a relative URL. If you embed this skill into a different directory tree, update the `@font-face` `src` paths or duplicate the asset.

```css
@font-face {
  font-family: 'Sora';
  src: local('Sora'),
       url('../output-formatting/assets/sora-regular.woff') format('woff'),
       url('../output-formatting/assets/sora-regular.ttf') format('truetype');
  font-weight: 400 700; font-display: swap;
}
```

### Scale
| Token | Size | Weight | Line height | Letter-spacing |
|---|---|---|---|---|
| h1 | 32px | 500 | 1.2 | -0.01em |
| h2 | 24px | 500 | 1.25 | -0.01em |
| h3 | 18px | 500 | 1.3 | -0.005em |
| body | 15px | 500 | 1.6 | 0 |
| small | 12px | 500 | 1.5 | 0.02em |

Default body weight is **500** (not 400) — this is deliberate, gives the NEXOURA voice its quiet confidence. Use 600 for `<strong>` and button labels, 700 only for the wordmark.

### Tagline
`WHERE AI BUILDS` — always uppercase, `letter-spacing: 0.5em`, often gradient-clipped (see footer §9).

---

## §6. Buttons

Three variants. All use 8px radius, 10/18 padding, Sora 600 / 14px.

```html
<button class="nx-btn nx-btn--primary">Launch</button>
<button class="nx-btn nx-btn--secondary">View brief</button>
<button class="nx-btn nx-btn--ghost">Skip</button>
```

- **Primary** — filled with `--nx-grad`, white text, soft purple glow. Lifts 1px on hover.
- **Secondary** — transparent background, purple text, brand-tinted border. Tint fill on hover.
- **Ghost** — transparent, secondary-text color, lifts to purple on hover.

All variants support `:focus-visible` (cyan outline), `:disabled` (45% opacity, no-drop cursor).

---

## §7. Cards

Three card types — pick by *purpose*, not aesthetic preference.

- `.nx-card` — **elevated.** Default. 1px border + 8px radius + soft shadow. Use for primary content blocks.
- `.nx-card--accent` — **accent.** Thin gradient top border + brand-tinted background. Use for the *one* card you want to draw the eye to per section.
- `.nx-card--flat` — **flat.** Background tint only, no border. Use for grids of peer items where elevation would create visual noise.

```html
<div class="nx-card"><h3>Title</h3><p>Body.</p></div>
<div class="nx-card--accent"><h3>Title</h3><p>Body.</p></div>
<div class="nx-card--flat"><h3>Title</h3><p>Body.</p></div>
```

---

## §8. Pills / badges

Status and priority indicators. Colors carry forward from T15 for cross-skill consistency. 11px Sora bold, 4px radius, 10% letter-spacing, uppercase.

| Class | Use | Color |
|---|---|---|
| `pill-verified` | Confirmed, passed review | Green `#34D399` |
| `pill-resolved` | Closed issue | Cyan `#00E0FF` |
| `pill-warning` | Attention needed | Amber `#FBBF24` |
| `pill-blocked` | Blocker present | Red `#F87171` |
| `pill-p0` | Critical | Solid red `#DC2626` |
| `pill-p1` | High | Solid blue `#2563FF` |
| `pill-p2` | Medium | Solid amber `#F59E0B` (dark text) |
| `pill-p3` | Low | Gray `#6B7280` |
| `pill-p4` | Backlog | Slate `#475569` |

```html
<span class="pill pill-verified">Verified</span>
<span class="pill pill-p0">P0</span>
```

---

## §9. Footer pattern

Gradient hairline + tagline left + metadata right.

```html
<footer class="nx-footer">
  <div class="nx-tagline">Where AI Builds</div>
  <div class="nx-meta">NEXOURA Studio · 2026 · v1.0</div>
</footer>
```

The tagline uses `background-clip: text` to receive the brand gradient as fill. The 2px gradient bar sits above the footer as a `::before` overlay on a `border-top` rule.

---

## §10. Theme switcher

JavaScript controller in three parts: (a) pre-paint bootstrap, (b) toggle button, (c) OS-preference listener.

### Pre-paint bootstrap (in `<head>`, before stylesheet)
```html
<script>
(function() {
  try {
    var stored = localStorage.getItem('nx-theme');
    var prefersLight = window.matchMedia('(prefers-color-scheme: light)').matches;
    var theme = stored || (prefersLight ? 'light' : 'dark');
    document.documentElement.setAttribute('data-theme', theme);
  } catch (e) {
    document.documentElement.setAttribute('data-theme', 'dark');
  }
})();
</script>
```

### Toggle controller (end of `<body>`)
```html
<script>
document.getElementById('themeToggle').addEventListener('click', function() {
  var cur = document.documentElement.getAttribute('data-theme') || 'dark';
  var next = cur === 'dark' ? 'light' : 'dark';
  document.documentElement.setAttribute('data-theme', next);
  localStorage.setItem('nx-theme', next);
});
</script>
```

Honors `prefers-color-scheme` only when the user has not explicitly chosen. Once they click the toggle, their choice persists.

See `sample-page.html` for the full working pattern with icon + label updates and OS-change listener.

---

## §11. Usage guide

To brand a new HTML output:

1. **Inline `components.css`** into a `<style>` tag (or link it with a relative path). Inlining is the default — most outputs ship as single self-contained `.html` files.
2. **Add the theme bootstrap script** to `<head>` (§10).
3. **Open with the logo lockup** (`--lg` or `--xl` in headers; `--md`/`--sm` inline).
4. **Compose with cards + pills** — one accent card per section maximum.
5. **Close with the footer** carrying the gradient bar + `WHERE AI BUILDS`.

### Minimal example
```html
<!DOCTYPE html>
<html data-theme="dark">
<head>
  <meta charset="UTF-8"><title>Briefing</title>
  <style>/* paste components.css here */</style>
</head>
<body style="padding:48px;max-width:900px;margin:0 auto;">
  <span class="nx-logo nx-logo--md">
    <span>NEX</span><span class="nx-oring"></span><span>URA</span>
  </span>
  <h1>Briefing title</h1>
  <div class="nx-card--accent">
    <h3>Headline finding <span class="pill pill-verified">Verified</span></h3>
    <p>Body…</p>
  </div>
  <button class="nx-btn nx-btn--primary">Next step</button>
  <footer class="nx-footer">
    <div class="nx-tagline">Where AI Builds</div>
    <div class="nx-meta">2026</div>
  </footer>
</body></html>
```

For longer documents (multi-section reports, deliverables with TOC, print layouts) defer to `nexoura/output-formatting` which composes these primitives into a full page chrome.

---

## §12. What NOT to do

- ❌ **Don't** use plain `NEXOURA` text where the logo lockup should appear (cover pages, headers, footers). Use the lockup *or* the wordmark variant from §3 — never raw text.
- ❌ **Don't** substitute the O-ring with a regular letter `O`. The ring is the brand mark; the letter is not.
- ❌ **Don't** gradient-fill the wordmark letters (`NEX...URA`). Only the O-ring and the footer tagline carry the gradient. Letter wordmarks stay in `--text-primary`.
- ❌ **Don't** introduce gaming, cyberpunk, neon-grid, glitch, or scan-line effects. NEXOURA reads premium, futuristic, **calm**. Heavy glow, animated gradients on letters, holographic chrome — all off-brand.
- ❌ **Don't** swap brand accents between themes. Surface and text re-tone for light/dark; purple/violet/blue/cyan stay constant.
- ❌ **Don't** mix the gradient direction. Always `135deg` with the four stops at `0/28/68/100%`. Reversing or rotating breaks recognition.
- ❌ **Don't** ship a NEXOURA HTML output without a footer. The gradient bar + tagline is the closing brand beat.

---

## Files in this skill

| File | Purpose |
|---|---|
| `SKILL.md` | this document |
| `components.css` | all CSS tokens + classes — inline into outputs |
| `components.html` | copy-paste primitive library |
| `nexoura-logo.html` | 4 logo sizes + mark + SVG variants |
| `sample-page.html` | full integration demo with working theme switcher |
