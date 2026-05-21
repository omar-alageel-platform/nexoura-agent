# ADR 002 — Product Registry

**Status:** Proposed
**Date:** 2025 (Studio B6, PR #61)
**Author:** Architecture Director

---

## Context

The PROJECTS view in NEXOURA Studio currently shows one product:
**Supply Chain SaaS**. The product name, repo, stage count, and accent color
are all written directly into the view code. This is called "hardcoding."

Hardcoding one product is fine when there is only one product. But NEXOURA
plans to build more products — for example, Work, One, and Enterprise. When
product #2 arrives, we will need to:

- Add it to the PROJECTS view.
- Give it its own repo link, stage count, and brand color.
- Not break the existing Supply Chain SaaS view.

Right now there is no single place to add a new product. A developer would
have to dig into the view code and the cache code at the same time. That is
error-prone and slow.

This ADR proposes a registry — one file that lists all products. The PROJECTS
view and the cache read from this file. Adding product #2 means editing one
file, not two or three.

**Important:** This is a proposal. Nothing is built yet. The current code
still hardcodes Supply Chain SaaS. Implementation waits until product #2 is
ready to onboard. Premature abstractions create maintenance debt.

---

## Decision

When product #2 onboards, we will create `tools/studio/products.json`. It
will be a JSON array. Each item in the array represents one product.

Each product has these fields:

| Field | Type | Meaning |
|---|---|---|
| `slug` | string | Short ID, no spaces. Example: `supply-chain-saas` |
| `name` | string | Display name shown in the UI |
| `repo` | string | GitHub repo URL |
| `stage_count` | number | How many lifecycle stages this product has |
| `accent_color` | string | One of the four locked NEXOURA hex codes |

Example `products.json`:

```json
[
  {
    "slug": "supply-chain-saas",
    "name": "Supply Chain SaaS",
    "repo": "https://github.com/nexoura/supply-chain-saas",
    "stage_count": 7,
    "accent_color": "#00E0FF"
  }
]
```

`tools/studio/cache.py` will read `products.json` in its existing
`get_engagements()` function (or a new `get_products()` function — TBD in
the implementation PR). The PROJECTS view will loop over the registry to
build tabs and timelines.

**accent_color must be one of:** `#7861FF`, `#5B30FF`, `#2563FF`, `#00E0FF`.
No other hex codes are allowed. This is enforced by the brand spec.

---

## Consequences

**Good:**
- Adding a new product becomes a 5-line JSON edit, not a code change.
- The cache and view stay in sync automatically.
- Easy to review in a PR — product metadata is visible at a glance.
- No new dependencies. JSON parsing is stdlib.

**Watch out for:**
- `products.json` becomes a critical file. If it is missing or malformed,
  the PROJECTS view will show an error. The cache must handle this gracefully
  (show "Unknown" state, per Locked Decision #1).
- `accent_color` is a free-form string in JSON. Nothing enforces the brand
  palette at parse time. A future validation step (or a JSON Schema check in
  CI) would close this gap.
- `stage_count` is a number, but the actual stage labels are not in the
  registry. Stage names are still in the view template. If a future product
  has different stage names, the view template will need updating too. This
  is acceptable for now.

**This does not change anything today.** Supply Chain SaaS stays hardcoded
until the implementation PR runs. At that point, the hardcoded values move
into `products.json` and the code reads from the file. No visible behavior
change for Omar.

---

## Alternatives Considered

**Database table (SQLite)**
- Pros: queryable, supports more fields, easy to extend.
- Cons: adds complexity. For 1-4 products, a JSON file is simpler.
  Re-evaluate if product count exceeds 10.
- Rejected for now.

**Environment variables per product**
- Pros: easy to override per deployment.
- Cons: no structure. Listing all products requires naming conventions.
  Hard to read and hard to review.
- Rejected.

**Hardcode each product in a separate Python module**
- Pros: type-safe, IDE autocomplete.
- Cons: requires a code change (and a deploy) to add a new product. A JSON
  file can be edited by a non-engineer. That matters as the team grows.
- Rejected.
