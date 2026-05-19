---
name: nexoura-feasibility-stage
description: "Use when running NEXOURA Stage 1 — phrases like 'feasibility study for <X>', 'is <X> worth building', 'kick off NEXOURA stage 1', 'TAM/SAM/SOM for <X>', 'competitor scan for <engagement>', 'unit economics for <engagement>', 'write the go/no-go memo', 'open the strategic gate from stage 1'. T6 stage skill — drives the feasibility study from problem statement through partner-signed go/no-go, populating `01-feasibility/` per T3, and hands off via a strategic gate per T2."
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, stage-skill, feasibility, stage-1]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-pdpl-compliance
      - nexoura-bilingual-content
---

# NEXOURA Feasibility — Stage 1 Playbook (T6)

Turns a one-paragraph client problem into a partner-signable go/no-go memo. Six artifacts under `01-feasibility/` (T3 §4), one strategic gate at exit (T2 §3, `decision_kind: "strategic"`). Expands the T1 §3 Stage 1 stub; for lifecycle, gates, and filenames, defer to T1 / T2 / T3.

---

## §1. When to load

**Triggers.** "feasibility study for `<X>`"; "is `<X>` worth building"; "kick off NEXOURA stage 1"; "draft the feasibility memo for `<slug>`"; "TAM/SAM/SOM for `<X>`" / "size the market for `<X>`"; "competitor scan for `<engagement>`"; "unit economics for `<engagement>`"; "write go/no-go for `<engagement>`"; "open the strategic gate from stage 1".

**Non-triggers (defer).** PRD/NFR → T7. Naming, brand → T8. Stack, ADRs → T9. Pricing, channels, launch → T10. Runbook, SLA → T11. Gate mechanics → T2. File placement / naming → T3. PDPL substance → T4 (this skill flags PDPL **risk**; T7 + T4 run the DPIA).

**Preconditions.** Repo scaffolded (T1 §9a); `manifest.json:current_stage == "01-feasibility"`; `client` set; README problem paragraph present. If `current_stage != "01-feasibility"`, abort and surface the manifest.

---

## §2. Inputs and outputs

**Required manifest fields to start:** `slug`, `client`, `owner`, `created_at`, `current_stage == "01-feasibility"`. README problem paragraph (T3 §7) is the source-of-truth problem statement; this skill quotes it verbatim into §1 of `feasibility-memo.en.md`.

**Artifacts produced (all six required, all under `01-feasibility/`, all per T3 §4):**

| File | Owner specialist (§7) | Notes |
|------|-----------------------|-------|
| `feasibility-memo.en.md` | Financial Analyst (lead) | 7-section outline §8. |
| `feasibility-memo.ar.md` | Bilingual reviewer | 1:1 section parity; KSA-formal; §8.3. |
| `market-map.csv` | Market Sizer | Clustering view; schema §6.2. |
| `competitors.md` | Competitive Intel | Three-tier template §6.1. |
| `economics.csv` | Financial Analyst | Sizing + 5-year P&L + unit economics; schema §4.3. |
| `go-no-go.json` | Resource Planner → Partner | Schema §9; wrapped by §10 gate payload. |

Stage is artifact-complete (T3 §4) when all six exist and are non-empty, the memo pair has matching section count, and `go-no-go.json` parses against §9.

---

## §3. Market sizing — TAM / SAM / SOM

Three numbers, three methods, three sources. Compute **top-down** AND **bottom-up** for TAM and reconcile within ±25%; wider gap = bad methodology.

### 3.1 Formulas (SAR primary, USD secondary)

- **TAM** — annual revenue if every category buyer bought from one vendor. Top-down: `global_category_revenue × KSA_share`. Bottom-up: `total_buyers × avg_annual_spend`.
- **SAM** — TAM subset reachable by our product, channel, language, and regulatory posture: `TAM × reachable_share × regulatory_eligibility`. PDPL/ZATCA shrink SAM whenever the offering touches personal data or e-invoicing.
- **SOM** — realistic 3-year capture assuming Stage 5 GTM lands: `SAM × win_rate × ramp`. `win_rate` capped at 5% for a new entrant; cite the comparable.

### 3.2 KSA sources (primary before consultancy; carried in `economics.csv:source`)

- **GASTAT** (stats.gov.sa) — population, employment, enterprise census → buyer counts and segments.
- **Monsha'at** (monshaat.gov.sa) — SME census and spend → SMB-segment SAM.
- **MCIT** (mcit.gov.sa) — ICT spend, digital adoption → digital-product SAM.
- **SAMA** (sama.gov.sa) — payments, lending → fintech-adjacent plays.
- **World Bank** (data.worldbank.org) — GCC peer benchmarks.
- **Vision 2030 / PIF** program reports — public-sector tailwinds (NEOM, ROSHN, NIS).
- Consultancy (Gartner, Statista, McKinsey, BCG, IDC) — secondary only; never sole source for a TAM number.

### 3.3 Recording in `economics.csv` (sizing block — schema shared with §4.3, `block` discriminates)

```csv
block,line_item,year,unit,value_sar,value_usd,method,source,assumption
sizing,TAM,2026,SAR/year,1200000000,320000000,bottom-up,GASTAT 2025 + buyer interviews,N buyers × avg spend
sizing,TAM,2026,SAR/year,1180000000,314000000,top-down,Gartner KSA ICT 2025 + MCIT share,global × KSA share
sizing,SAM,2026,SAR/year,420000000,112000000,calc,Monsha'at + PDPL eligibility,TAM × 0.35 × 1.0
sizing,SOM,2028,SAR/year,21000000,5600000,calc,internal,SAM × 5% × 1.0 ramp
```

Top-down and bottom-up live side-by-side so the reconciliation paragraph in memo §2 cites both by line.

---

## §4. Financial model — 5-year P&L + unit economics

Stage 1 is **not** the budgeting stage (Stage 4 `cost.md` owns precision). Stage 1 produces a directional 5-year model sufficient to test if the unit economics could close.

### 4.1 P&L line items (`economics.csv` `block=pnl`, columns Y1–Y5)

| Line item | Formula | Sanity check |
|-----------|---------|---------------|
| `revenue` | `customers × ARPU` | Matches SOM ramp. |
| `cogs` | `customers × variable_cost_per_customer` | Cloud + payment fees + tier-1 support. |
| `gross_margin` | `revenue − cogs` | SaaS target ≥ 70%. |
| `opex_rnd` | headcount × loaded cost | Engineering. |
| `opex_sm` | salaries + paid media + events | Sales + Marketing. |
| `opex_ga` | salaries + rent + legal | G&A. |
| `ebitda` | `gross_margin − Σ opex_*` | Negative Y1–Y2 expected; cross-over ≤ Y3 or revisit pricing. |

### 4.2 Unit economics (`block=unit`)

| Metric | Formula | Threshold |
|--------|---------|-----------|
| `CAC` | `total_sm_spend / new_customers` | KSA SaaS target. |
| `ARPU` | `revenue / avg_customers` | SAR/year. |
| `LTV` | `ARPU × gross_margin_% / churn_rate` | 12-month rolling churn. |
| `payback_months` | `CAC / (ARPU × gross_margin_% / 12)` | ≤ 18 months. |
| `LTV_to_CAC` | `LTV / CAC` | ≥ 3 → GO; 2–3 → REVISE w/ conditions; < 2 → NO-GO. |

### 4.3 `economics.csv` schema and currency

Columns: `block,line_item,year,unit,value_sar,value_usd,method,source,assumption`. One CSV, three blocks (`sizing`, `pnl`, `unit`). SAR primary; USD secondary at the SAMA mid-rate on `manifest.json:created_at` (record the rate in memo §4). `assumption` mandatory — every number traces to a `source` row or stated assumption. VAT (15%) is **excluded** from Stage 1 revenue lines; VAT enters Stage 5 `pricing.md` per T10. State the exclusion in memo §4 so the partner does not double-count.

---

## §5. Risk register

Lives in `feasibility-memo.en.md` §5 (mirrored in `.ar.md` §5). Optional machine carry: `risks[]` array inside `go-no-go.json`.

### 5.1 Schema

| Field | Type | Notes |
|-------|------|-------|
| `id` | `R-<NN>` | Zero-padded, monotonic. |
| `category` | enum | `market` \| `regulatory` \| `tech` \| `operational` \| `financial` |
| `description` | string | One sentence, ≤ 30 words. |
| `likelihood` | int 1–5 | 1=rare, 5=near-certain. |
| `impact` | int 1–5 | 1=cosmetic, 5=engagement-killer. |
| `score` | int 1–25 | `likelihood × impact`. Sort table desc by `score`. |
| `mitigation` | string | What we do **before** the gate, or what we accept. |
| `owner` | email | Single accountable person. |

### 5.2 Example rows (3, including a KSA-regulatory)

| id | cat | description | L | I | score | mitigation | owner |
|----|-----|-------------|---|---|-------|------------|-------|
| R-01 | regulatory | PDPL classifies supplier contact data as personal data; EU processor breaches data-residency without explicit consent. | 4 | 5 | 20 | In-Kingdom hosting default; T4 DPIA in Stage 2; consent flow in PRD. | omar@nexoura.ai |
| R-02 | regulatory | ZATCA Phase 2 e-invoicing mandatory once volume crosses threshold; sandbox→prod cutover non-trivial. | 3 | 4 | 12 | ZATCA SDK spike in Stage 4; cutover as Stage 6 launch precondition. | omar@nexoura.ai |
| R-03 | market | Three incumbents serve top-20 KSA importers; new entrant must crack reference accounts. | 4 | 3 | 12 | Anchor-buyer LOIs before Stage 4 commit; design-partner pricing. | omar@nexoura.ai |

Any `score ≥ 15` must be addressed in memo §7 — mitigated to < 15 pre-gate or explicitly accepted in the rationale.

---

## §6. Competitive analysis

### 6.1 `competitors.md` structure (three tiers, in this order)

```markdown
# Competitive landscape — <engagement>

## 1. Incumbents (direct, established KSA presence)
### <Company name>
- **Offering:** one sentence.
- **Pricing posture:** entry SAR/month, enterprise SAR/year band.
- **KSA presence:** office, local team, Vision 2030 / PIF references, ZATCA certified.
- **Defensibility (theirs):** data, integrations, contracts, brand.
- **Our angle:** the one wedge where we beat them.

## 2. Near-adjacents (same buyer, different problem)
### <Company name>   (same five bullets)

## 3. Indirect (status quo — spreadsheets, manual, in-house build)
- One paragraph. Usually the real competitor for a Stage 1 pilot.
```

Minimum five entries across tiers combined; minimum one entry in tier 3 (the "do nothing" comparison is mandatory).

### 6.2 `market-map.csv` schema (clustering view)

Companion CSV powering a 2D scatter in memo §3. Columns: `name,tier,segment,price_band,ksa_presence,founded_year,last_funding_sar,defensibility_score,our_overlap_score,notes`. `tier` ∈ {`incumbent`, `near-adjacent`, `indirect`}. Scores 1–5 ints. Memo plots `defensibility_score` (x) vs `our_overlap_score` (y); top-right-quadrant competitors are direct threats and must appear in §5.

---

## §7. Specialist profiles

Six roles, usually run as sub-agents or hat-swaps. Specialists write only into files they own (T3 §9); read is universal.

| Role | Owns | Responsibility | Pre-load |
|------|------|---------------|----------|
| **Financial Analyst** | memo §4, `economics.csv` (`pnl` + `unit`) | Builds 5-year P&L and unit economics; ties revenue to SOM curve; flags LTV/CAC < 3. Lead memo author. | T1, T2, T3, §4. |
| **Market Sizer** | `economics.csv` `sizing`, memo §2 | TAM/SAM/SOM top-down + bottom-up; reconciles within ±25%; cites primary KSA sources (§3.2). | T1, §3. |
| **Risk Analyst** | memo §5; optional `risks[]` in `go-no-go.json` | Enumerates risks across five categories; scores; mitigations; ensures every score ≥ 15 is addressed in §7. | T1, T4, §5. |
| **Competitive Intel** | `competitors.md`, `market-map.csv` | Maps incumbents + near-adjacents + indirect; sources public filings, ZATCA registry, press; populates the 2D plot. | T1, §6. |
| **Resource Planner** | drafts `go-no-go.json`; memo §6 | Translates the financial model into headcount/cap needed; judges fit with NEXOURA capacity. | T1, T2, §4 + §9. |
| **Tech Feasibility Reviewer** | memo §3 + §5 tech rows | One-page judgment: buildable inside the cap envelope? Names integration risks (ZATCA, Nafath, Fasah) for Stage 4. | T1, T4, §5. |

---

## §8. Feasibility memo structure

### 8.1 Section outline (mandatory, same order EN and AR)

1. **Problem statement.** Quote README paragraph verbatim, then one paragraph of NEXOURA-framed restatement (buyer, job-to-be-done, current alternative, friction).
2. **Market.** TAM/SAM/SOM with both methods; reconciliation paragraph; cite `economics.csv` `sizing` rows.
3. **Competitive landscape.** Summary of `competitors.md` + 2D plot from `market-map.csv`; name the one defensible wedge.
4. **Economics.** P&L summary table (Y1, Y3, Y5), unit economics, payback months, LTV/CAC. SAR primary, USD parenthetical. Cite `economics.csv` rows.
5. **Risks.** §5 register, sorted by score desc. Every score ≥ 15 carries a mitigation paragraph below the table.
6. **Strategic fit.** Why NEXOURA / APT WATCH wins this versus alternative engagements. Capacity, expertise, reference value, Vision 2030 alignment.
7. **Recommendation.** One paragraph proposing `GO` / `NO-GO` / `CONDITIONAL` with the rationale the partner signs in §9.

Target 1,500–2,500 words EN. Partner-readable-in-one-sitting (kanban acceptance) is hard.

### 8.3 Arabic mirror (`feasibility-memo.ar.md`)

Mirrors §8.1 1:1. KSA-formal register per T5 (until T5 lands, T1 §8 stub). Filename + section-parity rules per T3 §5. **This skill does not duplicate the Arabic template** — see T3 for the bilingual filename contract and T5 for register / terminology / RTL. Currency: SAR primary; USD parenthetical. Inline English technical terms (`CAC`, `LTV`, `ZATCA`) stay in Latin script — do not transliterate.

---

## §9. Decision artifact — `go-no-go.json`

The Stage 1 exit document. Drafted by the Resource Planner (§7), signed by the Partner. Wrapped by the §10 gate payload.

### 9.1 Schema

```json
{
  "decision": "GO | NO-GO | CONDITIONAL",
  "rationale_en": "One paragraph, ≥2 sentences, cites the LTV/CAC and the top-ranked risk.",
  "rationale_ar": "Mirror of rationale_en, KSA-formal register.",
  "conditions": [],
  "approver": "partner-email@nexoura.ai",
  "decided_at": "2026-05-22T14:30:00Z",
  "confidence": "low | medium | high"
}
```

Field contract: `decision` — `GO` advance, `NO-GO` halt, `CONDITIONAL` advance only after `conditions[]` close (gate payload §10 carries them as gate `conditions`, T2 §3). `rationale_*` — both languages mandatory even when one is more polished; the bilingual obligation is structural. `conditions` — populated only when `decision == "CONDITIONAL"`; each entry one actionable string. `confidence` — Resource Planner's self-rating; `low` should trigger an extra interview round before signing.

### 9.2 Example (APT WATCH supply-chain SaaS pilot — GO)

```json
{
  "decision": "GO",
  "rationale_en": "TAM 1.2B SAR (bottom-up) reconciles within 2% of the top-down number; LTV/CAC of 4.1 clears the 3.0 threshold; the highest-ranked risk (PDPL residency, R-01, score 20) has a tractable mitigation through in-Kingdom hosting that Stage 4 will confirm. NEXOURA capacity matches the 18-month build window and APT WATCH supplies three anchor-buyer LOIs.",
  "rationale_ar": "حجم السوق الكلّي ١٫٢ مليار ريال يتّسق مع الحساب التنازلي بفارق ٢٪، ونسبة LTV/CAC تبلغ ٤٫١ متجاوزةً الحدّ الأدنى (٣٫٠). أعلى المخاطر (R-01، PDPL، الأثر ٢٠) قابلٌ للمعالجة عبر الاستضافة داخل المملكة في المرحلة الرابعة.",
  "conditions": [],
  "approver": "omar@nexoura.ai",
  "decided_at": "2026-05-22T14:30:00Z",
  "confidence": "high"
}
```

---

## §10. Gate handoff (strategic)

Stage 1 ends at a **strategic** gate per T2 §2. Resource Planner writes `gates/gate-1-to-2.json` (path per T3 §3) with `decision_kind: "strategic"`. The gate payload wraps `go-no-go.json`: gate `decision` is copied from `go-no-go.json.decision`, `rationale` is `rationale_en` (Arabic stays in the wrapped artifact, not duplicated), `artifacts_reviewed` enumerates all six §2 files, `channel` records how the partner approved.

### 10.1 Payload pattern (full schema in T2 §3)

```json
{
  "request_id": "<uuid-v4>",
  "status": "pending",
  "decision_kind": "strategic",
  "from_stage": "01-feasibility",
  "to_stage": "02-requirements",
  "approver": "omar@nexoura.ai",
  "decision": "GO",
  "channel": "cli-clarify",
  "timestamp": "2026-05-22T14:30:00Z",
  "rationale": "<copy of go-no-go.json.rationale_en>",
  "artifacts_reviewed": [
    "01-feasibility/feasibility-memo.en.md", "01-feasibility/feasibility-memo.ar.md",
    "01-feasibility/market-map.csv", "01-feasibility/competitors.md",
    "01-feasibility/economics.csv", "01-feasibility/go-no-go.json"
  ],
  "conditions": [], "next_action": null
}
```

### 10.2 Operator flow

1. Confirm all six artifacts present and non-empty (T3 §10 recipe).
2. Resource Planner finalises `01-feasibility/go-no-go.json`.
3. Generate `request_id` (UUID v4); write `gates/gate-1-to-2.json` with `status: pending`.
4. Emit the strategic gate prompt from T2 §7.1 (EN + AR) on the chosen channel; `{{artifact_list}}` is the six paths above; `{{summary}}` is the memo §7 recommendation paragraph.
5. On partner response, apply T2 §4 + §5. Commit per T3 §8: `gate: stage1 → stage2 APPROVED` (or `REVISE` / `BLOCKED`).
6. **GO** → hand off to T7. **NO-GO** → halt, leave `current_stage` at `01-feasibility`, archive. **REVISE** → re-run affected specialists addressing `next_action`; open a fresh gate with a new `request_id` per T2 §4c.

`CONDITIONAL` is not strategic-gate vocabulary under T2 §3 — if Stage 1 wants to advance with open obligations, encode them as a `REVISE` with explicit `conditions[]` in `go-no-go.json` and re-open a clean gate after each closes. `CONDITIONAL` is reserved for the operational gate at Stage 6.

---

## §11. Cross-references

- **T1 nexoura-engagement-lifecycle** — §3 (Stage 1 stub this skill expands), §4 (directory layout), §6 (superseded by T3).
- **T2 nexoura-gate-protocol** — §3 (`gate.json` schema, `decision_kind: "strategic"`), §4 (advance / reject / revise), §5 (atomic write), §7.1 (bilingual strategic gate prompt), §7.3 (rejection notification).
- **T3 nexoura-artifact-conventions** — §3 (`gates/` and `01-feasibility/` placement), §4 (per-stage required artifacts this skill enforces), §5 (filename / CSV / JSON / markdown rules), §6 (`.gitignore`), §8 (`stage1: …` and `gate: stage1 → stage2 …` commit grammar), §9 (this skill owns `01-feasibility/`, T2 owns `gates/`).
- **T4 nexoura-pdpl-compliance** (forthcoming) — substance of any PDPL risk row in §5; this skill flags PDPL **risk** only and defers the DPIA to T7 + T4.
- **T5 nexoura-bilingual-content** (forthcoming) — Arabic register, terminology, RTL/LTR rules used by the Arabic memo mirror (§8.3) and the Arabic rationale in `go-no-go.json` (§9).
