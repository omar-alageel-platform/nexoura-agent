---
name: nexoura-gtm-marketing-stage
description: "Use when running NEXOURA Stage 5 — phrases like 'GTM plan for <engagement>', 'go-to-market for <slug>', 'NEXOURA stage 5', 'pricing model for <X>', 'launch plan for <X>', 'ICP for <engagement>', 'channels plan', 'content calendar', 'open the strategic gate from stage 5'. T10 stage skill — turns a Stage 3 brand and a Stage 4 architecture + cost envelope into a partner-signable bilingual GTM bundle (ICP, pricing in SAR with 15% VAT and USD parenthetical, channels, launch sequence, content calendar) and hands off to Stage 6 operations via a strategic gate per T2."
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, stage-skill, gtm, marketing, stage-5]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-branding-stage
      - nexoura-operations-stage
      - nexoura-bilingual-content
---

# NEXOURA GTM & Marketing — Stage 5 Playbook (T10)

Turns a signed Stage 3 brand + Stage 4 architecture/cost into a partner-signable go-to-market bundle: an ICP, a pricing model (SAR, 15% VAT, USD parenthetical), a KSA-first channel plan, a T-minus launch sequence, and a content-calendar stub. Five artifacts under `05-gtm/` (plus the gate decision under `gates/`), one strategic gate at exit per T2 §3. Expands the T1 §3 Stage 5 stub; defer to T1 / T2 / T3 for lifecycle, gate mechanics, filenames.

طلب — مرحلة الذهاب إلى السوق: من العلامة والمعمار إلى خطّة إطلاق ثنائيّة اللغة قابلة للاعتماد.

---

## §1. Scope and triggers

**Triggers.** "GTM plan for `<engagement>`"; "go-to-market for `<slug>`"; "NEXOURA stage 5"; "pricing model for `<X>`"; "launch plan for `<X>`"; "ICP for `<engagement>`"; "channels plan"; "content calendar"; "open the strategic gate from stage 5".

**Non-triggers (defer).** Feasibility → T6. PRD → T7. Brand voice / naming → T8. Stack, ADRs, cost itself → T9. Runbook, SLA, support tiers, billing-ops invoicing mechanics → T11. Gate mechanics → T2. File placement → T3. Bilingual register rules → T5 (deferred; applied inline below).

**Preconditions.** `manifest.json:current_stage == "05-gtm"`. Stage 3 produced partner-signed `03-branding/brand-book.{en,ar}.md`, `positioning.md`, `voice-tone.md`. Stage 4 produced partner-signed `04-tech/cost.md` (CAPEX + OPEX in SAR + USD) and `04-tech/architecture.md`. PRD §4 persona is the seed for §3 ICP refinement. The exit gate of Stage 4 (`gates/gate-4-to-5.json`) must be `approved` with `decision == "GO"`. If `current_stage != "05-gtm"`, abort and surface the manifest. If `cost.md` is missing or OPEX line items are not priced in SAR, refuse and route back to T9 — pricing without a cost floor is a refusal.

---

## §2. Stage 5 workflow

1. **Kickoff.** GTM Strategist reads PRD §4 persona, Stage 1 memo §3 (TAM/SAM/SOM), brand-book §3 positioning, `cost.md` OPEX. Locks SAR/USD FX at **3.75 SAR = 1 USD** (SAMA peg; recorded in `pricing.md` §0).
2. **ICP refinement.** GTM Strategist authors `gtm-plan.{en,ar}.md` §1 — persona sharpened into 1–3 named segments (§3).
3. **Pricing.** Pricing Analyst authors `pricing.md` — tier matrix, usage meter (if any), hybrid logic, VAT, annual vs. monthly, gross-margin reconciliation to `cost.md` (§4).
4. **Channels.** Digital Marketer + Sales Enablement co-author `channels.md` — direct, partnerships, LinkedIn, content; per-channel CAC envelope reconciled to LTV (§5).
5. **Launch sequence.** GTM Strategist authors `launch-plan.md` — T-minus calendar with soft-launch → beta → GA milestones, owners per row (§6).
6. **Content calendar stub.** Content Strategist drafts §7 appendix inside `gtm-plan.{en,ar}.md` (12-week stub; live calendar is operator-maintained post-launch).
7. **Competitive positioning.** GTM Strategist completes §8 grid inside `gtm-plan.{en,ar}.md`.
8. **Review.** Pricing Analyst signs margin; Sales Enablement signs CAC; Content Strategist signs calendar parity; partner reviews the bundle.
9. **Strategic gate.** Engagement owner writes `gates/gate-5-to-6.json` per T2 §3 and §10.

---

## §3. ICP definition + segmentation

ICP (Ideal Customer Profile) is a tighter restatement of the PRD §4 persona using buyer-side firmographics + behavioural signals. Author 1–3 named segments inside `gtm-plan.{en,ar}.md` §1.

**Per-segment axes (all required):** **firmographics** (vertical with NACE/ISIC; size band employees + SAR revenue; KSA region Riyadh / Jeddah / Eastern / Other; ownership family / corporate / government / GRE); **behavioural signals** (trigger event — ZATCA phase, Vision 2030 mandate, multi-branch expansion; current workaround; budget-owner role); **buying motion** (self-serve / sales-assisted / enterprise; cycle length in weeks; procurement — PO, Etimad vendor reg for government, Nafath signatory for regulated); **disqualifiers** (hard rejects — e.g. revenue below SAR 2M for enterprise tier, non-KSA operations, sanctioned entity).

**Segment naming.** Title-case noun phrase that survives in the deck — "Riyadh Multi-Branch Retail SMB", "Eastern Province Industrial Mid-Market". Avoid persona-as-individual names at this stage; that lives in `voice-tone.md`. **SOM bridge:** each segment cites the Stage 1 memo's SOM cell it draws from, so the partner can trace addressable revenue at the gate without re-deriving sizing.

---

## §4. Pricing model — `pricing.md`

**Section 0 — FX and tax constants (mandatory header).** `FX: 3.75 SAR = 1 USD (SAMA peg, locked at <YYYY-MM-DD>)`. `VAT: 15% per ZATCA general regime`. All headline numbers are quoted **SAR incl. 15% VAT** with `USD ≈` parenthetical at the locked rate. A VAT-exclusive column is shown for procurement.

**Section 1 — Tier matrix (subscription).** Three tiers minimum — **Starter**, **Growth**, **Enterprise**. Per tier: target ICP segment (§3); monthly price (SAR incl. VAT) and annual price (10–17% discount vs. 12× monthly is the convention); feature gating (≤ 6 bullets); included usage caps; overage policy reference (§2).

```markdown
| Tier      | Monthly (SAR incl. VAT) | Monthly (USD ≈) | Annual (SAR incl. VAT) | VAT-excl. monthly | Included usage           |
|-----------|------------------------:|----------------:|-----------------------:|------------------:|--------------------------|
| Starter   |               1,150 SAR |       USD 307   |             11,500 SAR |         1,000 SAR | 1 branch, 5 users, 5k tx |
| Growth    |               3,450 SAR |       USD 920   |             34,500 SAR |         3,000 SAR | 5 branches, 25 users     |
| Enterprise|                  Custom |          Custom |                 Custom |            Custom | Unlimited, SSO, SLA      |
```

**Section 2 — Usage-based meter (if any).** Name the meter (transactions, API calls, branches, seats, GB stored), unit price (SAR incl. VAT + USD ≈), included band per tier, overage rate. Overage invoiced monthly in arrears via T11 billing-ops. If pure subscription, state explicitly: "No usage-based component in v1."

**Section 3 — Hybrid logic.** If hybrid (subscription floor + usage overage): which tier inclusions are hard vs. soft caps; whether annual prepay credits roll over (default: no); the upsell trigger (e.g. ≥ 3 months of overage → sales-assisted upgrade).

**Section 4 — Annual vs. monthly.** Annual prepay default for Growth and Enterprise; monthly default for Starter. Annual discount band 10–17%. Cancellation: monthly → end of cycle, no refund; annual → pro-rated refund minus consumed months at the monthly rate (the "ratchet" — protects against annual-shop-then-cancel).

**Section 5 — Gross-margin reconciliation to `cost.md`.** Mandatory table mapping each tier's effective ARPU (SAR, VAT-excl.) against allocated OPEX per active account from `04-tech/cost.md`. Show absolute margin (SAR) and margin % per tier. **Acceptance:** lowest tier shows non-negative contribution margin at projected steady-state utilisation; a negative-margin tier is a gate-blocking finding (partner-only override).

**Section 6 — Invoicing & procurement.** All invoices in SAR per ZATCA e-invoicing (Phase 2 integration owned by T11). Government / GRE buyers: **Etimad** vendor registration is a prerequisite — flag in §5 channel mix so the timeline is honest. Enterprise tier carries a one-page MSA template (lives under `06-operations/` per T11 ownership, referenced not duplicated).

---

## §5. Channel strategy — `channels.md`

Four channels in v1, weighted to the KSA enterprise/SMB market.

**5.1 Direct sales (sales-assisted + enterprise).** Outbound list from §3 ICP segments. Cadence: 5-touch sequence over 14 days (LinkedIn connect → Arabic intro → AR + EN one-pager → demo offer → break-up). First touch is Arabic for KSA-domiciled accounts; switch to bilingual on buyer signal. Track in HubSpot or a CRM stub.

**5.2 Partnerships.** Three archetypes: (a) **systems integrators / consultancies** already inside the buyer (Big-4 KSA practices, local SIs); (b) **complementary SaaS** (accounting, POS, logistics — same buyer monthly); (c) **government / GRE accelerators** (Monsha'at for SMB, MCIT for tech, NTDP for tech-export). Each gets a one-pager and a referral economic — default 15–20% of Year-1 net ARR, capped at 12 months.

**5.3 LinkedIn (dominant KSA B2B channel).** Twitter/X is consumption-only, Instagram is brand-not-sales, TikTok is consumer — LinkedIn is the platform. Mix: 60% organic thought-leadership from the engagement owner's personal profile (highest reach), 30% company-page educational content, 10% paid (Sponsored Content + InMail to §3 firmographics). Arabic-first posts outperform EN-only on KSA feeds — default AR primary with EN as a pinned-comment translation or a second post.

**5.4 Content marketing.** Long-form (≥ 1,500 words) Arabic-primary articles on the engagement's site, syndicated to LinkedIn as articles and to one local industry publication where relevant (e.g. Argaam for fintech). SEO: target Arabic long-tail intent first — the EN-only competitor set is sparse on AR keywords, so AR content compounds faster. Cadence at GA: 2 long-form/month + 8 LinkedIn posts/month.

**CAC envelope (illustrative — replace per engagement):** direct sales SAR 8,000–18,000 / closed Growth account; partnership SAR 4,000–9,000 (referral dominates); LinkedIn paid SAR 3,500–7,000 / SQL; content marketing SAR 1,200–3,000 / SQL at steady state (back-loaded — months 1–3 yield zero). **Reconcile to LTV** from §4: blended CAC ≤ 1/3 of Year-1 ARR per closed Growth account, payback ≤ 12 months.

---

## §6. Launch sequence — `launch-plan.md`

T-minus calendar from a chosen GA date `T0`. Three internal milestones — **not** Stage gates (those are T2-governed).

**Soft launch (T-8 to T-4w).** Invite-only. 3–5 design-partner accounts from §3 primary ICP, ideally pre-committed during Stage 2 buyer interviews. Goal: production exercised end-to-end, T11 runbook drafted against real incidents, pricing not yet published. Exit: zero P1 over 14 consecutive days + design partners willing to be named references.

**Beta (T-4w to T0).** Public sign-up gated by waitlist + manual approval. Pricing published per §4. Goal: ~20 accounts onboarded, self-serve funnel validated for Starter, sales-assisted motion validated for Growth. Exit: onboarding median ≤ 1 business day, NPS ≥ 30, zero open P1, billing-ops cycle closed once (per T11).

**General Availability (T0+).** Public, unrestricted sign-up. Marketing live (LinkedIn paid + content + partner co-announce). Pipeline goal for first 90 days set by §5 CAC envelope back-solved from the partner-approved revenue target. Informal exit: first three closed-won Growth accounts via repeatable motion, not founder-led heroics.

**T-minus calendar template (required in `launch-plan.md`):** table columns `T-minus | Date | Milestone | Owner | Status`. Seed rows (replace per engagement): T-8w design partners signed (GTM Strategist); T-6w T11 runbook v0.1 (Operations lead); T-4w beta waitlist opens, pricing public (Digital Marketer); T-2w LinkedIn paid brief signed (Digital Marketer); T-1w GA press / partner co-announce QA (GTM Strategist); T0 GA public sign-up live (Engagement owner); T+30d first 3 Growth closed-won (Sales Enablement). Every row carries a named owner — anonymous milestones are gate-blocking.

---

## §7. Content calendar (12-week stub)

Embedded as the closing appendix of `gtm-plan.{en,ar}.md`. Operator maintains the live calendar post-launch; this stub seeds the first 12 weeks so launch is not author-blocked.

**Mix per week (default):** 2 LinkedIn posts (1 AR-primary, 1 EN-primary or bilingual); 1 long-form article every other week (alternating AR/EN primary); 1 partner co-marketing slot every fourth week. AR content composed parallel in KSA-formal register per T8 §5 — not auto-translated.

**Theme rotation (4-week loop).** W1 problem framing (the workaround being replaced). W2 product capability (one feature tied to PRD §2 differentiator). W3 customer story (design-partner case once consented). W4 category education (Vision 2030 / ZATCA / sector context that positions the brand as the informed local choice).

**Required columns in the stub table:** week, date, format (post/article/case/partner), language (AR / EN / bilingual), theme, CTA, owner. Empty CTA/owner cells at draft time are acceptable — the gate checks structure, not full population.

---

## §8. Competitive positioning template

Inside `gtm-plan.{en,ar}.md` §4. Single grid, ≤ 5 competitors from Stage 1 `competitors.md`. Columns: Competitor | Their wedge | Where they win | Where we win | Pricing posture | Our counter-narrative (one sentence, AR + EN).

The counter-narrative cell is load-bearing — it's the line Sales Enablement drops into a deck and LinkedIn content riffs on. The wedge column quotes brand-book §3 positioning verbatim — Stage 5 must not silently re-position. A blank "where they win" cell after honest analysis = incomplete competitive intel — route back to T6 for a Stage 1 addendum; do not paper over.

---

## §9. Specialist profiles

Five roles. Specialists write only into files they own (T3 §9); read is universal.

| Role | Owns | Responsibility | Gate handoff |
|------|------|----------------|--------------|
| **GTM Strategist** | `gtm-plan.{en,ar}.md` §1, §4, §6 stub; `launch-plan.md` | Reads PRD §4, brand-book §3, Stage 1 memo §3. Authors ICP segmentation, competitive grid, T-minus launch calendar with owners. | Signs ICP-to-SOM traceability and the launch calendar. |
| **Pricing Analyst** | `pricing.md` | Tier matrix in SAR incl. VAT with USD parenthetical; usage meter; hybrid logic; annual/monthly mechanics; gross-margin reconciliation to `04-tech/cost.md`. | Signs margin reconciliation — no tier ships at negative steady-state contribution margin without explicit partner override. |
| **Sales Enablement** | §5 direct-sales + partnerships of `channels.md`; §8 counter-narratives | 5-touch outbound (Arabic-first first touch for KSA); partner archetypes + referral economics; one-pager copy; CAC envelope per channel reconciled to LTV. | Signs CAC envelope and AR + EN counter-narrative cells. |
| **Content Strategist** | §7 calendar stub in `gtm-plan.{en,ar}.md`; long-form briefs | 12-week calendar with theme rotation; AR-primary editorial line; KSA SEO long-tail brief; partner co-marketing slot scheduling. | Signs AR/EN parity of the calendar appendix. |
| **Digital Marketer** | §5 LinkedIn + content-marketing of `channels.md` | LinkedIn organic + paid plan (Arabic-first); content distribution + syndication map; channel measurement spec (SQL definition, attribution); paid CAC envelope. | Signs LinkedIn paid plan and syndication map; flags any channel whose projected CAC breaks the §4 LTV ceiling. |

---

## §10. Strategic gate — `gate-5-to-6.json`

Stage 5 ends at a **strategic** gate per T2 §2. Engagement owner writes `gates/gate-5-to-6.json` (path per T3 §3) with `decision_kind: "strategic"`. Approvers: engagement owner (NEXOURA partner) **and** client sponsor — both required. Pricing and launch date are the two hard-locked outputs; downstream T11 operations skins SLA, billing-ops, and incident KPIs against them.

### 10.1 Decision inputs

`artifacts_reviewed` carries the five §11 artifact paths. The approval prompt's `{{summary}}` is one paragraph: primary ICP segment (named), Starter and Growth headline prices (SAR incl. VAT + USD ≈), gross-margin posture per tier, channel mix headline, GA date `T0`, and one risk callout (e.g. ZATCA Phase 2 dependency, Etimad timeline for government segment).

### 10.2 Example payload (full schema in T2 §3)

```json
{
  "request_id": "7c4b9d1e-3a82-4f6e-9c0d-5b1e8a3f2d4c",
  "status": "pending",
  "decision_kind": "strategic",
  "from_stage": "05-gtm",
  "to_stage": "06-operations",
  "approvers_required": ["engagement_owner", "client_sponsor"],
  "approver": "omar@nexoura.ai",
  "decision": "GO",
  "channel": "cli-clarify",
  "timestamp": "2026-09-04T11:00:00Z",
  "rationale": "ICP Riyadh Multi-Branch Retail SMB from SOM cell B; Starter 1,150 SAR/mo (USD 307) at 58% margin, Growth 3,450 SAR/mo (USD 920) at 71%; LinkedIn-led mix; GA T0 2026-11-15; ZATCA Phase 2 tracked as launch dependency.",
  "artifacts_reviewed": [
    "05-gtm/gtm-plan.en.md", "05-gtm/gtm-plan.ar.md",
    "05-gtm/pricing.md", "05-gtm/channels.md", "05-gtm/launch-plan.md"
  ],
  "conditions": [], "next_action": null
}
```

### 10.3 Bilingual prompt (Stage 5 instantiation of T2 §7.1)

```text
GATE REQUEST — <slug>
Stage transition: 05-gtm → 06-operations
Artifacts: 05-gtm/{gtm-plan.en.md, gtm-plan.ar.md, pricing.md,
channels.md, launch-plan.md}
Summary: ICP primary <segment>; Starter <SAR>/mo (USD ~<X>),
Growth <SAR>/mo (USD ~<Y>); margin <tier:%>; channel mix
<LinkedIn/partnerships/direct%>; GA T0 <YYYY-MM-DD>; risk <one line>.
Reply: GO | NO-GO | REVISE — plus a one-sentence rationale.
```

```text
طلب اعتماد بوابة — <slug>
الانتقال بين المراحل: 05-gtm ← 06-operations
المخرجات: 05-gtm/{gtm-plan.en.md, gtm-plan.ar.md, pricing.md,
channels.md, launch-plan.md}
ملخّص تنفيذي: الشريحة المستهدفة <اسم الشريحة>؛ باقة Starter بسعر
<SAR> ريالاً شهريّاً شاملةً ضريبة القيمة المضافة (≈ <X> دولاراً)،
وباقة Growth بسعر <SAR> ريالاً شهريّاً (≈ <Y> دولاراً)؛ هامش
الربح <%>؛ مزيج القنوات <LinkedIn/شراكات/مبيعات مباشرة %>؛
تاريخ الإطلاق العام T0 <YYYY-MM-DD>؛ المخاطرة <سطر واحد>.
يُرجى الإفادة: GO | NO-GO | REVISE — مع مسوّغ مختصر في سطر مستقل.
```

### 10.4 Rejection paths

- **REVISE → `next_action: "reprice"`** — margin reconciliation fails or a tier prices below CAC payback; re-run §4.
- **REVISE → `next_action: "rechannel"`** — channel mix projects CAC over the LTV ceiling; re-run §5.
- **REVISE → `next_action: "relaunch-calendar"`** — milestone owners missing or a dependency (e.g. ZATCA Phase 2) lands after T0; re-run §6.
- **NO-GO** — rare; usually signals the upstream brand or persona is wrong (route back to T7 or T8, not a Stage-5 internal re-run).

Commit per T3 §8: `gate: stage5 → stage6 APPROVED` (or `REVISE` / `BLOCKED`).

---

## §11. Output artifacts summary

All under `engagements/<slug>/05-gtm/` unless noted (T3 §4):

| Path | Owner (§9) | Notes |
|------|------------|-------|
| `gtm-plan.en.md` | GTM Strategist | English plan; ICP §3, competitive grid §8, calendar appendix §7; T3 §5 parity with AR. |
| `gtm-plan.ar.md` | GTM Strategist | Arabic mirror, KSA-formal register, identical H2 order. |
| `pricing.md` | Pricing Analyst | Tiers in SAR incl. VAT + USD ≈; usage meter (or explicit "none"); margin reconciliation to `04-tech/cost.md`. |
| `channels.md` | Sales Enablement + Digital Marketer | Direct, partnerships, LinkedIn, content; per-channel CAC envelope reconciled to LTV. |
| `launch-plan.md` | GTM Strategist | T-minus calendar with named owners; soft-launch → beta → GA milestones. |
| `../gates/gate-5-to-6.json` | Engagement owner | Strategic gate per T2 §3; under `gates/` per T3 §3. |

Stage is artifact-complete when all five `05-gtm/` files exist and are non-empty, the two gtm-plan files have matching H2 section count, `pricing.md` carries the §0 FX/VAT header and a non-negative-margin row per tier (or a flagged partner override), `channels.md` carries a per-channel CAC envelope, `launch-plan.md` has a named owner on every milestone row, and `gate-5-to-6.json` parses against T2 §3.

---

## §12. Cross-references

- **T1 nexoura-engagement-lifecycle** — §3 (Stage 5 stub this skill expands), §6 (artifact layout — superseded by T3).
- **T2 nexoura-gate-protocol** — §3 (`gate.json` schema, `decision_kind: "strategic"`), §4 (advance / reject / revise), §7.1 (bilingual strategic prompt; §10.3 above is the Stage-5 instantiation).
- **T3 nexoura-artifact-conventions** — §3 (`gates/` and `05-gtm/` placement), §4 (required artifacts), §5 (`.en.md` / `.ar.md` parity for the gtm-plan pair), §8 (`stage5: …` and `gate: stage5 → stage6 …` commit grammar).
- **T8 nexoura-branding-stage** — brand feeds GTM: brand-book §3 positioning feeds §3 ICP framing and §8 competitive grid; voice/tone defaults govern §7 content register. Stage 5 does not silently re-brand.
- **T9 nexoura-tech-architecture** (forthcoming) — preceding stage; `04-tech/cost.md` is the floor for the §4 margin reconciliation; `architecture.md` integration surfaces (ZATCA, Etimad, Nafath) drive §6 launch dependencies.
- **T11 nexoura-operations-stage** (forthcoming) — next-stage ops handoff: consumes `pricing.md` for billing-ops invoicing flow, `launch-plan.md` for runbook drafting during soft-launch, `channels.md` for support-tier SLA shape.
- **T5 nexoura-bilingual-content** (deferred) — AR-first authoring rules, terminology glossary, KSA-formal register. Until T5 lands, §3–§8 carry the bilingual contract inline.
