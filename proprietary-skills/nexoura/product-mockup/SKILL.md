---
name: nexoura-product-mockup
description: Author high-fidelity NEXOURA-branded product mockups (static HTML/CSS) for landing pages, dashboards, and auth flows. LOOK-AND-FEEL prototypes — not production code. Real product copy (never Lorem Ipsum), Sora typography, 4-stop gradient used sparingly, dark-mode-first.
when_to_use: When a client or sibling skill needs a static, self-contained HTML mockup of a NEXOURA Studio product surface (landing page, dashboard, auth, settings) for review or as a visual contract before any production build.
---

# T17 — nexoura-product-mockup

Anchors: T13 §7 (information density) · T15 (brand integrity, palette, O-ring) · T16 `nexoura-brand-components` (component primitives — referenced by class name; see §1).

---

## §1 — Philosophy

A NEXOURA product mockup is a **LOOK-AND-FEEL prototype**: one self-contained HTML+CSS file that a stakeholder can open in a browser and immediately understand the surface, hierarchy, and tone. It is NOT production code — no state management, no real i18n, no accessibility audit beyond contrast, no data plumbing.

Non-negotiables:

1. **Real product copy.** Every headline, label, button, table row, testimonial, and price tier must be plausible for the engagement context. Lorem Ipsum is banned. If the domain is unknown, ask — do not fake.
2. **Static HTML, no framework.** No React/Vue/Svelte, no build step, no npm. One file, opens in a browser. The only permitted external request is the Sora font CDN; system-font fallback if offline.
3. **T16 component contract.** Mockups reference T16 classes by name — `.btn-primary`, `.btn-ghost`, `.card-elevated`, `.nx-logo`, `.pill` (with `.p0/.p1/.verified/.resolved`), `.sb-item`, `.stat-card`. T16 owns the canonical CSS. Because T16 may not be merged when these mockups are viewed, **every example file ships a minimal inline CSS stub for each T16 class** so the file renders standalone. When T16 lands, the stubs stay (cheap, self-contained) — they are the visual contract, not the source of truth.
4. **Premium, calm, intelligent.** Never gaming/cyberpunk. Gradient is a precision instrument, not wallpaper. Think Linear / Stripe / Vercel, not Razer / Discord.
5. **Dark mode is the default** (`#0A0F16`). Light mode only for auth, billing, or content-heavy reading surfaces.
6. **Density.** A real product surface has nav, breadcrumbs, search, filters, stats, tables, pills, footer. Do not ship a half-empty wireframe.

### Brand tokens (inline these into every mockup)

```css
:root {
  --nx-purple: #7861FF;  --nx-violet: #5B30FF;
  --nx-blue:   #2563FF;  --nx-cyan:   #00E0FF;
  --nx-navy:   #0A0F16;  --nx-white:  #F5F7FA;
  --slate-900: #101826;  --slate-700: #475569;  --slate-500: #94A3B8;
  --nx-gradient: linear-gradient(135deg,#7861FF 0%,#5B30FF 28%,#2563FF 68%,#00E0FF 100%);
  --font-sora: 'Sora', ui-sans-serif, system-ui, -apple-system, sans-serif;
}
body { font-family: var(--font-sora); background: var(--nx-navy); color: var(--nx-white); }
```

Font (top of `<head>`):

```html
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Sora:wght@400;500;600;700&display=swap" rel="stylesheet">
```

### O-ring logo (T16 `.nx-logo` — inline SVG)

Wordmark replaces the **O** with a 4-stop gradient ring. Always paired with the tagline **WHERE AI BUILDS** somewhere on the page (caps, letter-spaced).

```html
<span class="nx-logo">NEXO<svg viewBox="0 0 32 32" class="nx-oring" aria-label="O">
  <defs><linearGradient id="og" x1="0" y1="0" x2="1" y2="1">
    <stop offset="0%" stop-color="#7861FF"/><stop offset="28%" stop-color="#5B30FF"/>
    <stop offset="68%" stop-color="#2563FF"/><stop offset="100%" stop-color="#00E0FF"/>
  </linearGradient></defs>
  <circle cx="16" cy="16" r="12" fill="none" stroke="url(#og)" stroke-width="4"/>
</svg>URA</span>
```

---

## §2 — Marketing page patterns

**Landing hero.** Large headline (`clamp(2.5rem, 6vw, 4.5rem)`, weight 700, line-height 1.05) with one phrase clipped to the gradient via `background-clip: text`. Subtext one line, `slate-500`. Two CTAs: `.btn-primary` (gradient fill) + `.btn-ghost` (outlined). Background optional dot pattern: `radial-gradient(circle at 1px 1px, rgba(120,97,255,0.15) 1px, transparent 0) 0 0/24px 24px`.

**Feature grid (3–6 cards).** Each card: small gradient icon block (48×48, gradient background, white inline SVG), headline (weight 600), one-line description. Layout: 3 cols desktop / 2 cols at 1024px / 1 col at 768px via CSS grid `repeat(auto-fit, minmax(280px, 1fr))`.

**Pricing teaser (3 tiers).** Three columns: Starter / Studio / Forge. Middle tier "most popular" — wrap with a gradient border via `background: var(--nx-gradient); padding: 1.5px; border-radius: 16px;` containing an inner card on `--nx-navy`. Each tier: name, price, billing cadence, 5–7 feature bullets with check icons, CTA.

**Testimonials.** Either one hero quote (large) or a 3-up grid. Each: avatar (CSS gradient circle if no photo), real-sounding name + title + company (e.g. "VP Supply Chain, Meridian Logistics" — never "John Doe, Customer").

**Footer with newsletter.** Multi-column (Product / Company / Resources / Legal) above a bottom row: O-ring logo + **WHERE AI BUILDS** + copyright + single-input newsletter form (email + gradient Subscribe button). Top border: `1px solid rgba(255,255,255,0.06)`.

---

## §3 — Dashboard patterns

**Collapsible sidebar nav.** Two states: expanded 240px (icon + label), collapsed 72px (icon only). Default expanded on desktop, collapsed at ≤1024px. Active item: 2px gradient left border + `rgba(120,97,255,0.08)` row background. Use T16 `.sb-item` and `.sb-item.active`.

**Top header.** 64px tall, `border-bottom: 1px solid rgba(255,255,255,0.06)`. Three zones: left (breadcrumbs or product name), center (search input full-width to ~520px), right (notifications bell with red count badge, user avatar circle + caret). On mobile (≤768px): hamburger replaces sidebar; search collapses to icon.

**Main content grid.**

1. **Top row — 4 metric cards** (T16 `.stat-card`): uppercase label `slate-500` 0.7rem, big value (2rem, weight 700, gradient text on the headline metric), delta row (`+12.4% vs last week` in cyan for positive, amber for negative), optional 30-day sparkline (inline SVG polyline).
2. **Middle row — 2 columns**: left = recent activity feed (timestamped events, status pills); right = chart (inline SVG bar/line, no Chart.js).
3. **Tables row** — 1 or 2 tables. Header `slate-700` background, body rows with `border-bottom: 1px solid rgba(255,255,255,0.05)`, row hover `rgba(120,97,255,0.06)`. Status column always uses T16 `.pill`. Filter bar above: search + 2–3 dropdowns + "Export CSV" `.btn-ghost`.
4. **Quick actions row** — 3–4 icon+label tiles for common next steps.

**Status pills (T16).** `.pill.p0` (red), `.pill.p1` (amber), `.pill.verified` (cyan), `.pill.resolved` (green). Pill-shaped (`border-radius: 999px`), 0.7rem, weight 600, letter-spaced 0.06em.

---

## §4 — Auth flow patterns

**Sign-up.** 2-column layout (single column ≤768px). Left: form (email, password, company, role select, Terms checkbox, gradient Sign Up button, "Continue with Google" + "Continue with Microsoft" ghost buttons with provider logos). Right: three value-prop blocks (icon + headline + one-line copy) showing what they get post-signup. Light mode is acceptable for auth — users spend <30s here and form contrast matters.

**Login.** Centered card, max-width 420px, vertically centered (`min-height: 100vh; display: grid; place-items: center`). O-ring logo at top of card. Email + password + "Forgot password?" + Sign In gradient button + SSO row + link to sign-up.

**Forgot password.** Single email field + "Send reset link" button + back-to-login link.

**Email verification.** Large gradient checkmark icon, "Check your inbox at user@company.com", resend link with cooldown text.

Inputs: 44px tall, `border: 1px solid var(--slate-700)`, `border-radius: 8px`, focus-ring 2px nx-purple. Labels above inputs (not floating — clarity over cleverness). Error text below input in amber.

---

## §5 — Mobile-responsive

Breakpoints (pick one direction per file and stay consistent):

- `1280px` — large tablet / small laptop, slight padding compression
- `1024px` — tablet, sidebar collapses to icons-only, 3-col grids → 2-col
- `768px` — mobile, sidebar becomes off-canvas drawer behind hamburger, all multi-col grids → 1 col, hero scales down
- `640px` — small mobile, tighter padding, tables shift to stacked-card pattern OR horizontal scroll for ops-heavy data

Use CSS grid + flexbox. No JS frameworks. A few lines of vanilla JS for menu toggle is acceptable (toggle a `body.menu-open` class).

---

## §6 — Reference design searches

When the vibe isn't coming, do not invent in a vacuum:

- `image_search('SaaS landing page design 2026')`
- `image_search('B2B dashboard UI inspiration')`
- `image_search('Linear app pricing page')` — Linear, Vercel, Stripe, Resend, Cursor are the current gold standard for premium B2B aesthetic
- `image_search('dark mode dashboard purple gradient')`

Reference for typography rhythm, whitespace density, gradient restraint. Then make it ours: navy not black, 4-stop NEXOURA gradient, Sora not Inter, O-ring always.

---

## §7 — Sample mockups (worked examples)

The files in `examples/` are the canonical worked examples. They are committed and **they ARE the skill output for these three surfaces.** Read them, fork them, adapt them.

| File | Surface | Mode |
|---|---|---|
| `examples/landing-page-full.html` | NEXOURA Forge marketing landing | Dark |
| `examples/dashboard-overview.html` | Ops dashboard (SKUs / suppliers / shipments) | Dark |
| `examples/auth-signup.html` | New account signup (2-col + value props) | Light |

Each is self-contained, includes inline stubs for T16 classes, includes at least one `@media (max-width: 768px)` block, and uses real domain copy (supply-chain ops for Forge).

---

## §8 — DO NOT

- **No Lorem Ipsum.** Ever. Use real product copy for the engagement context.
- **No placeholder images** (`placehold.co`, `picsum.photos`). Use CSS gradient placeholders, inline SVG, or solid blocks with labels.
- **No abstract gestures** (`<!-- button here -->`, `[CTA goes here]`). Show the actual button with the actual label.
- **No broken mobile.** Every mockup must include at least one `@media (max-width: 768px)` block that proves it survives 375px width.
- **No gradient everywhere.** Hero CTA, headline text-clip, active nav indicator, "most popular" pricing border. If every card has a gradient, none do.
- **No cyberpunk neon.** No glowing borders, Tron grids, 80s synth.
- **No external JS framework.** Static HTML/CSS only. Vanilla JS for menu toggle is fine; React/Vue/Tailwind CDN is not.
- **No skipping the O-ring.** Plain "NEXOURA" text without the gradient ring is a brand violation.
- **No `<img src="logo.png">`.** Inline SVG only — mockup must render with zero local assets.
- **No claiming "production-ready" in handoff.** These are visual contracts. Flag the simplification honestly in PR/client notes.

---

## Verification checklist before commit

- [ ] `grep -i 'lorem' examples/` returns nothing.
- [ ] HTML parses cleanly (`python3 -c 'from html.parser import HTMLParser; HTMLParser().feed(open(f).read())'`).
- [ ] Every file references Sora font family.
- [ ] O-ring logo present in every file.
- [ ] Tagline **WHERE AI BUILDS** appears at least once.
- [ ] At least one `@media (max-width: 768px)` block per file.
- [ ] No external image URLs, no JS framework CDN.
- [ ] T16 stubs present at top of `<style>` so file renders standalone.
