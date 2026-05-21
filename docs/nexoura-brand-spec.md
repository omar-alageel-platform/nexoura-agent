# Nexoura Brand Color & Wordmark Spec

## Overview
This document defines the **approved Nexoura color palette**, the **master logo / wordmark direction**, and the **visual writing style** for how **NEXOURA** should appear across presentations, product UI, web, app, social assets, and marketing materials.

**Brand line:** `Where AI Builds`

---

## 1) Core Brand Colors

### Primary Palette

| Token | Name | Hex | RGB | Usage |
|---|---|---:|---:|---|
| `nx-purple-500` | Nexoura Purple | `#7861FF` | `120, 97, 255` | Primary accent, headline accent, ring gradient start |
| `nx-violet-600` | Nexoura Violet | `#5B30FF` | `91, 48, 255` | Secondary accent, darker purple contrast |
| `nx-blue-500` | Nexoura Blue | `#2563FF` | `37, 99, 255` | Main blue accent, CTA emphasis |
| `nx-cyan-400` | Nexoura Cyan | `#00E0FF` | `0, 224, 255` | Glow finish, highlight, ring gradient end |
| `nx-navy-950` | Deep Navy | `#0A0F16` | `10, 15, 22` | Dark-mode background |
| `nx-white-50` | Soft White | `#F5F7FA` | `245, 247, 250` | Light text on dark surfaces, light-mode base |

### Supporting Neutrals

| Token | Name | Hex | RGB | Usage |
|---|---|---:|---:|---|
| `nx-slate-900` | Graphite Navy | `#101826` | `16, 24, 38` | Elevated dark cards / panels |
| `nx-slate-700` | Muted Slate | `#475569` | `71, 85, 105` | Secondary labels in light mode |
| `nx-slate-500` | Mid Slate | `#64748B` | `100, 116, 139` | Supporting copy / borders |
| `nx-slate-300` | Light Border | `#CBD5E1` | `203, 213, 225` | Light-mode separators |
| `nx-slate-100` | Surface Mist | `#F1F5F9` | `241, 245, 249` | Soft light cards / neutral fills |

---

## 2) Signature Gradient

The Nexoura identity is strongly associated with the **glowing O ring**. The ring should use a premium tech gradient, not a flat color.

### Primary Gradient (Recommended)
- Start: `#7861FF`
- Mid 1: `#5B30FF`
- Mid 2: `#2563FF`
- End: `#00E0FF`

### CSS Example
```css
background: linear-gradient(135deg, #7861FF 0%, #5B30FF 28%, #2563FF 68%, #00E0FF 100%);
```

### Glow Recommendation
For dark mode, use a soft outer glow based on:
- Purple glow: `rgba(120, 97, 255, 0.35)`
- Cyan glow: `rgba(0, 224, 255, 0.28)`

Do **not** overdo the glow. Nexoura should feel **premium and controlled**, not gaming/cyberpunk.

---

## 3) Light / Dark Mode Color Intent

### Dark Mode
- Background: `#0A0F16`
- Primary text: `#F5F7FA`
- Secondary text: `#94A3B8`
- Accent gradient: purple → blue → cyan
- Use glow subtly around the O, CTA focus states, and data highlights.

### Light Mode
- Background: `#FFFFFF` or `#F8FAFC`
- Primary text: `#0A0F16`
- Secondary text: `#475569`
- Accent gradient remains identical.
- Glow should be softer and cleaner than dark mode.

---

## 4) Logo System

## Master Logo
The master brand signature is:

**NEXOURA**

with:
- uppercase wordmark
- wide, premium letter spacing
- a custom **O** rendered as the gradient ring
- tagline below in uppercase: **WHERE AI BUILDS**

### Master Logo Components
1. **Wordmark**: `N E X [O-ring] U R A`
2. **O Ring**: circular glowing ring with Nexoura gradient
3. **Tagline**: `WHERE AI BUILDS`

### Recommended Lockup
- Wordmark centered
- Tagline centered beneath it
- Ample breathing room around the full lockup

---

## 5) Wordmark / Writing Style (“How Nexoura is Written”)

This is the approved writing design direction for the brand name:

### Preferred Display Form
`NEXOURA`

### Rules
- Always written in **uppercase** for the logo / hero presentation lockup.
- Use **wide tracking** / generous letter spacing.
- The **O** is not a normal letterform in the logo lockup — it is the signature gradient ring.
- The rest of the letters should be **clean, geometric, modern, and minimal**.
- The overall look should feel:
  - premium
  - futuristic
  - calm
  - intelligent
  - scalable

### Brand Personality of the Wordmark
The wordmark should signal:
- an AI-native company
- precision and infrastructure
- elegance, not aggression
- high-end enterprise software

### What to Avoid
Do **not** render Nexoura as:
- playful rounded bubble text
- sharp sci-fi / gaming style typography
- glitch or distorted lettering
- heavily italicized forms
- condensed techno fonts
- metallic chrome effects

---

## 6) Typography Direction

### For UI / Documents / Presentations
Recommended primary font:
- **Sora**

Fallbacks:
- Inter
- Geist
- SF Pro / system sans

### Style Guidance
- Headings: clean, modern, slightly spaced
- Body: simple and readable
- Avoid decorative futuristic fonts in body copy

### Suggested Usage
| Use | Font | Weight |
|---|---|---|
| Wordmark supporting text | Sora | Medium / SemiBold |
| Headings | Sora | SemiBold / Bold |
| Body copy | Sora / Inter | Regular / Medium |
| UI labels | Sora / Inter | Medium |

---

## 7) Clear Space & Sizing

### Clear Space
Use the height of the `O` ring as a guide.
Recommended minimum clear space around the logo = **0.5× O height** on all sides.

### Minimum Sizes
#### Digital
- Full logo with tagline: minimum width `220 px`
- Wordmark only: minimum width `150 px`
- O ring icon only: minimum width `24 px`

#### Print
- Full logo with tagline: minimum width `45 mm`
- Wordmark only: minimum width `30 mm`

---

## 8) Logo Variants

### Primary Variant
- White letters on deep navy background
- O ring in signature purple/blue/cyan gradient
- Tagline in purple-blue accent

### Secondary Variant
- Dark letters on white/light background
- O ring remains gradient
- Tagline may be dark navy or purple-blue accent

### Icon Variant
Use the **O ring alone** as:
- app icon core mark
- favicon base
- small avatar element
- loading animation basis

### Product Family Variant
For product lines like:
- Nexoura Studio
- Nexoura Work
- Nexoura One
- Nexoura Enterprise

Use the **same core O-ring logo** and differentiate by:
- text label
- sub-label color accent
- supporting iconography

Do **not** create unrelated product logos.

---

## 9) Recommended CSS Tokens

```css
:root {
  --nx-purple-500: #7861FF;
  --nx-violet-600: #5B30FF;
  --nx-blue-500: #2563FF;
  --nx-cyan-400: #00E0FF;
  --nx-navy-950: #0A0F16;
  --nx-white-50: #F5F7FA;
  --nx-slate-900: #101826;
  --nx-slate-700: #475569;
  --nx-slate-500: #64748B;
  --nx-slate-300: #CBD5E1;
  --nx-slate-100: #F1F5F9;

  --nx-gradient-primary: linear-gradient(135deg, #7861FF 0%, #5B30FF 28%, #2563FF 68%, #00E0FF 100%);
}
```

---

## 10) Quick Developer Guidance

### Use the O Ring for
- hero sections
- loading states
- app icon
- launch / teaser graphics
- section dividers
- AI / orchestration motif

### Use Text Lockup for
- presentations
- website header / footer
- launch posters
- product overview pages
- social brand covers

### Avoid
- rebuilding the wordmark with random fonts
- replacing the ring with a plain O unless necessary for plain text environments
- changing the approved color codes

---

## 11) Plain-Text Fallbacks

When the full design lockup cannot be used:

### Preferred plain-text forms
- `Nexoura`
- `NEXOURA`

### Product names
- `Nexoura Studio`
- `Nexoura Work`
- `Nexoura One`
- `Nexoura Enterprise`

### Tagline
- `Where AI Builds`

---

## 12) Summary

Nexoura’s visual identity depends on three things:
1. **The signature O ring** using the approved purple → blue → cyan gradient
2. **A clean uppercase wordmark** with spacious premium letter spacing
3. **A controlled dark/light system** anchored by deep navy and soft white

This combination should always feel:
- futuristic
- elegant
- minimal
- intelligent
- premium
- enterprise-ready

