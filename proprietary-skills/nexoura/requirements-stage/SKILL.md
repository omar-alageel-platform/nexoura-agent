---
name: nexoura-requirements-stage
description: "Use when running NEXOURA Stage 2 — phrases like 'draft PRD for <engagement>', 'requirements capture for <X>', 'NEXOURA stage 2', 'write the NFR catalog', 'user stories with acceptance criteria for <slug>', 'wireframe spec for <X>', 'open the strategic gate from stage 2'. T7 stage skill — turns a Stage 1 GO into a partner-signable Stage 2 requirements bundle (bilingual PRD, NFR catalog, user stories, wireframe spec) and hands off via a strategic gate per T2."
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, stage-skill, requirements, stage-2]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-feasibility-stage
      - nexoura-pdpl-compliance
---

# NEXOURA Requirements — Stage 2 Playbook (T7)

Turns a signed Stage 1 GO into a partner-signable requirements bundle. Five artifacts under `02-requirements/` (plus one deferred PDPL placeholder), one strategic gate at exit (T2 §3, `decision_kind: "strategic"`). Expands the T1 §3 Stage 2 stub; for lifecycle, gates, filenames, defer to T1 / T2 / T3.

طلب — مرحلة المتطلبات (Stage 2): from idea to specification a developer can build and a tester can verify.

---

## §1. Scope and triggers

**Triggers.** "draft PRD for `<engagement>`"; "requirements capture for `<X>`"; "NEXOURA stage 2"; "write the NFR catalog for `<slug>`"; "user stories with acceptance criteria"; "wireframe spec for `<X>`"; "open the strategic gate from stage 2".

**Non-triggers (defer).** Feasibility / market sizing → T6. Naming, brand, persona visual identity → T8. Stack choice, ADRs → T9. Build cost, pricing → T10. Runbook, SLA → T11. Gate mechanics → T2. File placement / naming → T3. PDPL DPIA substance → T4 (deferred — see §7).

**Preconditions.** `manifest.json:current_stage == "02-requirements"`; Stage 1 left behind a partner-signed `01-feasibility/feasibility-memo.en.md` and a `01-feasibility/go-no-go.json` with `decision == "GO"` (or `REVISE`-then-`GO`). If `current_stage != "02-requirements"`, abort and surface the manifest. If `go-no-go.json.decision != "GO"`, refuse — the engagement is not eligible for Stage 2.

---

## §2. Stage 2 workflow

1. **Kickoff.** Read Stage 1 memo §1 (problem) and §7 (recommendation) verbatim. Confirm scope hasn't drifted; if it has, surface to partner before drafting.
2. **Discovery.** Stakeholder interviews (≥ 3 — engagement owner, client sponsor, one prospective end-user). Notes land in `02-requirements/discovery-notes.md` as a working file (not a gate artifact; do not include in §10).
3. **PRD drafting (bilingual).** Business Analyst frames problem and scope; Product Manager authors `prd.en.md` and the matching `prd.ar.md` per T3 §5. Section parity (§3) is enforced before review.
4. **NFR catalog.** Tech Lead Reviewer drafts `nfr.md` against the §4 categories with KSA-context targets.
5. **User stories.** Product Manager + UX Researcher write `user-stories.md` with Given/When/Then acceptance criteria (§5). QA Lead reviews the testability bar.
6. **Wireframe spec.** UX Researcher writes `wireframe-spec.md` — text-level only (§6). No Figma in v1.
7. **Review.** Tech Lead Reviewer signs NFR feasibility; QA Lead signs acceptance-criteria testability; Business Analyst signs scope boundary.
8. **Strategic gate.** Resource Planner / engagement owner writes `gates/gate-2-to-3.json` per T2 §3 and §9 below. Partner + client sponsor approve.

---

## §3. PRD template — `prd.en.md` + `prd.ar.md`

Bilingual product requirements document. T3 §5 contract: same H2 structure, same H2 order, 1:1 semantic parity. Currency in SAR primary, USD parenthetical. Inline English technical terms (`MVP`, `KPI`, `SLO`) stay in Latin script in the Arabic mirror.

### 3.1 Required section skeleton (paste into both files)

```markdown
# PRD — <engagement> (Stage 2)

## 1. Problem statement
Quote the README problem paragraph verbatim, then one paragraph framing buyer, job-to-be-done, current alternative, friction. Cite Stage 1 memo §1.

## 2. Solution overview
What we build, in two paragraphs. End with the one defensible wedge from Stage 1 memo §3.

## 3. In-scope / Out-of-scope
### In-scope (v1)
- Bullet list. Each bullet is one capability.
### Out-of-scope (explicit)
- Bullet list. Each bullet is one capability we are NOT building, with a one-line reason (deferred, regulatory, no ROI).

## 4. Target users and personas
Two to four personas. Each persona: name, role, primary goal, top frustration, KSA context (language preference AR/EN, device class, network class). Visual identity and tone deferred to T8 — link `../03-branding/personas.md` when T8 produces it.

## 5. Success metrics (KPIs)
| KPI | Target value | Measurement method | Cadence |
|-----|--------------|---------------------|---------|
| Activation rate | ≥ 40% of signups complete onboarding within 7 days | Mixpanel funnel `signup → first_action` | Weekly |
| ... | ... | ... | ... |
Minimum three KPIs; at least one is a leading indicator (behaviour), at least one is a lagging indicator (revenue or retention).

## 6. MVP cut
### Ships in v1
- Bullet list mapped 1:1 to §3 in-scope.
### Deferred to v1.x or v2
- Bullet list with a one-line trigger ("revisit when MAU > 5,000").

## 7. Open questions
Numbered list. Each question has an owner (email) and a needed-by date. A non-empty Open Questions section is acceptable at the gate only if every entry is non-blocking; blocking questions must be closed pre-gate.
```

The Arabic mirror (`prd.ar.md`) keeps section numbers and H2 titles in the same order; H2 text is translated (e.g. `## 1. المشكلة`, `## 3. النطاق / خارج النطاق`, `## 6. الحدّ الأدنى للمنتج (MVP)`). KSA-formal register per T5 stub.

---

## §4. Non-functional requirements — `nfr.md`

Catalog with seven categories, each with concrete KSA-context targets. Tech Lead Reviewer owns; reviewed against Stage 1 economics (a 99.99% uptime SLO that demands triple-region redundancy may bust the cap from T6 memo §4).

### 4.1 Table template

```markdown
| Category | Requirement | Target | Notes |
|----------|-------------|--------|-------|
| Performance | p95 API response | ≤ 400 ms over STC/Mobily 4G | KSA mobile p50 ~ 35 Mbps down; design assuming p10 = 5 Mbps. |
| Performance | Cold page load (first contentful paint) | ≤ 2.5 s on mid-tier Android over 4G | Lighthouse mobile profile. |
| Security | Transport | TLS 1.3 minimum; HSTS preload | No TLS 1.0/1.1. |
| Security | Secrets | Managed via vault (Stage 4 picks); never in repo | See T3 §6 `.gitignore`. |
| Security | Dependencies | SCA scan on every PR; block high CVEs | Stage 4 wires CI. |
| Security | PDPL alignment | Personal-data flows logged; consent captured pre-collection | DPIA deferred to `pdpl-assessment.md` — see §7 and T4. |
| Scalability | Horizontal | Stateless web tier; queue-backed workers | Vertical scale capped at one node class. |
| Scalability | Load growth | Sustain 10× Stage 1 SOM Y1 traffic without re-architecture | Cite Stage 1 SOM curve. |
| Availability | Uptime SLO | 99.5% v1 (≈ 3.6 h/month allowed) | 99.9% deferred until revenue justifies. |
| Availability | RTO / RPO | RTO ≤ 4 h, RPO ≤ 1 h | Backup snapshot ≤ hourly. |
| Accessibility | WCAG 2.1 AA baseline | All v1 screens audited | Axe + manual screen-reader pass. |
| Accessibility | Arabic RTL | Full RTL layout parity, bidi-correct numerics | Mandatory; not optional. |
| Observability | Logs | Structured JSON, correlation-id per request | 30-day hot retention. |
| Observability | Metrics | RED (rate/errors/duration) per service | Alert thresholds with on-call rota. |
| Observability | Traces | Distributed traces sampled ≥ 10% | OpenTelemetry. |
| Localization | AR/EN parity | Every user-visible string in both languages | No machine translation in v1 UI. |
| Localization | Calendar | Hijri (التقويم الهجري) + Gregorian shown together for KSA-context dates | Religious/civic dates Hijri-primary; commercial Gregorian-primary. |
| Localization | RTL | Mirrored layout, bidi-safe inputs | Tested with mixed AR/EN strings and Latin numerals. |
```

Minimum one row per category. Numeric targets are mandatory — "fast" and "secure" are not requirements.

### 4.2 KSA-context notes

Mobile network: assume STC / Mobily / Zain 4G mid-tier baseline; 5G coverage is dense in Riyadh/Jeddah/Dammam but not load-bearing for v1. PDPL: any personal-data flow (national ID, phone, address, biometric) is flagged in the security category and re-assessed by T4 when it lands. Arabic RTL is non-negotiable — a v1 that ships LTR-only fails the gate.

---

## §5. User stories — `user-stories.md`

Format mandatory: `As a <role>, I want <capability>, so that <outcome>.` Acceptance criteria use Given / When / Then (Gherkin-style, readable, **not** executable). Every acceptance criterion must be testable — a criterion no QA engineer can write a test against is rejected by the QA Lead at review. معايير القبول (acceptance criteria) are the stage's testability contract.

### 5.1 Story template

```markdown
### US-<NN> — <one-line title>
**As a** <role>, **I want** <capability>, **so that** <outcome>.

**Acceptance criteria**
- **AC-1.** Given <state>, when <action>, then <observable outcome>.
- **AC-2.** Given <state>, when <action>, then <observable outcome>.

**Priority:** must | should | could (MoSCoW)
**Linked KPI:** PRD §5 row reference (optional, recommended).
```

### 5.2 Worked example — authenticated user flow

```markdown
### US-07 — First-run wizard saves draft on exit
**As a** newly signed-up SMB owner, **I want** the first-run wizard to save my progress if I leave mid-flow, **so that** I can finish later without re-entering company data.

**Acceptance criteria**
- **AC-1.** Given a user has completed wizard step 2 of 4, when they close the tab, then on next sign-in they are routed back to step 3 with steps 1–2 pre-filled.
- **AC-2.** Given a user is on wizard step 3, when the network drops for ≥ 10 s, then the step's entered data persists locally and uploads automatically on reconnect.
- **AC-3.** Given a user has been idle for ≥ 30 days mid-wizard, when they sign in, then the draft is discarded and the wizard restarts at step 1.

**Priority:** must
**Linked KPI:** PRD §5 — Activation rate.
```

### 5.3 Worked example — admin / back-office flow

```markdown
### US-21 — Operator can suspend a tenant account
**As a** NEXOURA back-office operator, **I want** to suspend a tenant account with a reason code, **so that** payment-failure or abuse cases are contained without a code deploy.

**Acceptance criteria**
- **AC-1.** Given an operator has the `tenant:suspend` permission, when they submit a suspension with reason code `payment_failed`, then all tenant users are signed out within 60 s and shown the suspension page on next request.
- **AC-2.** Given a tenant has been suspended, when the suspension reason is `payment_failed` and payment is later cleared, then an operator with `tenant:reinstate` can reverse the suspension and the audit log records both events with operator email and timestamp.
- **AC-3.** Given an operator lacks `tenant:suspend`, when they call the suspension endpoint, then the call returns 403 and an audit row records the denied attempt.

**Priority:** must
**Linked KPI:** PRD §5 — Operational containment time.
```

Minimum twelve stories at gate; at least one admin / back-office story; at least one error / negative-path story per critical flow.

---

## §6. Wireframe spec — `wireframe-spec.md`

**Text-level only** — visual wireframes (Figma, sketches) are explicitly out of scope for NEXOURA v1. The UX Researcher writes a structured text spec that an engineer can build from and a designer can later reify into Figma in Stage 4 if needed.

### 6.1 Per-screen structure

```markdown
### S-<NN> — <Screen name>
- **ID:** S-<NN>
- **Purpose:** one sentence.
- **Key elements:** bullet list (header, primary CTA, list view, filter chip, ...).
- **User actions available:** bullet list, each an active verb (Submit, Filter, Edit, Cancel).
- **Entry points:** which flow brings the user here (S-IDs or external link / push).
- **Exit points:** for each action above, name the destination (another S-ID or "external: <where>").
```

### 6.2 User flows

Subsection at the end of `wireframe-spec.md`. Two to three critical flows, each a numbered step sequence of S-IDs:

```markdown
## User flows

### Flow 1 — Onboarding
1. S-01 Landing → 2. S-02 Sign-up → 3. S-03 Verify (email + phone) → 4. S-04 First-run wizard step 1 → ... → 5. S-08 Dashboard (first view).

### Flow 2 — Core task (place an order)
1. S-08 Dashboard → 2. S-12 Catalogue → 3. S-13 Item detail → 4. S-14 Cart → 5. S-15 Checkout → 6. S-16 Confirmation.

### Flow 3 — Recovery (forgot password)
1. S-02 Sign-up/Sign-in → 2. S-30 Forgot password → 3. S-31 Email sent confirmation → 4. (external: email) → 5. S-32 Reset password → 6. S-08 Dashboard.
```

Minimum eight screens at gate; minimum three flows including one error / recovery flow. RTL mirroring is a layout property, not a separate screen — call it out in §4 (NFR Localization) and reference it from `wireframe-spec.md` §1 once.

---

## §7. PDPL hook (deferred)

`pdpl-assessment.md` is listed as a Stage 2 artifact in the kanban spec (T7 card), but the PDPL assessment template lives in T4 (nexoura-pdpl-compliance / nexoura-ksa-compliance), which is **deferred** in the current phase. When T4 lands, this section will cross-link to its DPIA template and the file becomes a hard gate artifact. Until then, engagement workers MAY draft a placeholder `pdpl-assessment.md` noting which personal-data flows exist (national ID, phone, address, biometrics, location, payment, health), where they are collected, where they are stored, and whether residency is in-Kingdom — to be hardened against T4 once available. The placeholder is **not** a gate-blocking artifact in this phase; the NFR security row in §4 carries the PDPL flag in the interim.

---

## §8. Specialist profiles

Five roles, usually sub-agents or hat-swaps. Specialists write only into files they own (T3 §9); read is universal.

| Role | Owns | Responsibility | Review checkpoints |
|------|------|----------------|---------------------|
| **Business Analyst** | PRD §1, §3, §5 | Problem framing, scope boundary (in/out), success-metrics definition. Signs scope before PM drafts solution. | After PRD §1 + §3 draft; before user-stories drafting. |
| **Product Manager** | `prd.en.md`, `prd.ar.md`, `user-stories.md` priorities, MVP cut | PRD authorship end-to-end, MVP cut decisions, story prioritisation (MoSCoW). | After PRD complete; after story list complete. |
| **UX Researcher** | PRD §4 (personas), `wireframe-spec.md` | Persona development from discovery notes, user-flow definition, screen-by-screen spec. | After personas; after wireframe spec complete. |
| **Tech Lead Reviewer** | `nfr.md` | NFR catalog authorship; reviews targets for feasibility against Stage 1 economics; flags integration risks (Nafath, ZATCA, payment gateways) early for Stage 4. Gate-blocking veto on infeasible NFRs. | After NFR draft; before strategic gate. |
| **QA Lead** | acceptance-criteria testability bar | Reviews every AC for the testability contract (§5); rejects vague criteria. Owns the testability bar at the gate. | After user-stories draft; before strategic gate. |

---

## §9. Strategic gate — `gate-2-to-3.json`

Stage 2 ends at a **strategic** gate per T2 §2. Engagement owner writes `gates/gate-2-to-3.json` (path per T3 §3) with `decision_kind: "strategic"`. Approvers: engagement owner (NEXOURA partner) **and** client sponsor — both required.

### 9.1 Gate fields specific to Stage 2

- `decision_kind`: `"strategic"`
- `from_stage`: `"02-requirements"` → `to_stage`: `"03-branding"`
- `artifacts_reviewed`: the five §10 artifact paths (PDPL placeholder excluded while T4 is deferred)
- `approvers_required`: `["engagement_owner", "client_sponsor"]`
- **Rejection paths.** `REVISE` with `next_action: "scope_cut"` (cut §3 in-scope items; cheapest path); `REVISE` with `next_action: "scope_expand"` (rare — usually triggers re-feasibility back to Stage 1, flag the partner); or `REVISE` with `next_action: "hold"` (pause Stage 2; client-side dependency unresolved). `NO-GO` halts the engagement entirely and is rare at this gate — a Stage 1 GO that flips to NO-GO at Stage 2 is a signal that the feasibility memo was wrong.

### 9.2 Example payload (full schema in T2 §3)

```json
{
  "request_id": "8f2d1e6c-3a4b-4f5d-9c2e-0a7b1c8d9e4f",
  "status": "pending",
  "decision_kind": "strategic",
  "from_stage": "02-requirements",
  "to_stage": "03-branding",
  "approvers_required": ["engagement_owner", "client_sponsor"],
  "approver": "omar@nexoura.ai",
  "decision": "GO",
  "channel": "cli-clarify",
  "timestamp": "2026-06-04T11:15:00Z",
  "rationale": "PRD in/out boundary is partner-signed; twelve user stories with testable ACs cover the three critical flows; NFRs (uptime 99.5%, p95 400ms, WCAG 2.1 AA + RTL) clear Stage 1 economics envelope; PDPL placeholder filed pending T4.",
  "artifacts_reviewed": [
    "02-requirements/prd.en.md", "02-requirements/prd.ar.md",
    "02-requirements/nfr.md", "02-requirements/user-stories.md",
    "02-requirements/wireframe-spec.md"
  ],
  "conditions": [], "next_action": null
}
```

Commit per T3 §8: `gate: stage2 → stage3 APPROVED` (or `REVISE` / `BLOCKED`).

---

## §10. Output artifacts summary

All under `engagements/<slug>/02-requirements/` unless noted (T3 §4):

- `prd.en.md` — PRD English (§3).
- `prd.ar.md` — PRD Arabic, section-parity with EN (§3, T3 §5).
- `nfr.md` — non-functional requirements catalog (§4).
- `user-stories.md` — user stories with Given/When/Then ACs (§5).
- `wireframe-spec.md` — text-level wireframe + user flows (§6).
- `pdpl-assessment.md` — **deferred**, see §7 and T4. Not gate-blocking this phase.
- `../gates/gate-2-to-3.json` — strategic gate decision artifact (§9, placed under `gates/` per T3 §3, not under `02-requirements/`).

Stage is artifact-complete when the five required files exist and are non-empty, `prd.en.md` and `prd.ar.md` have matching H2 section count, `nfr.md` has ≥ one row per §4 category, `user-stories.md` has ≥ 12 stories each with ≥ 2 ACs, `wireframe-spec.md` has ≥ 8 screens and ≥ 3 flows, and `gate-2-to-3.json` parses against T2 §3.

---

## §11. Cross-references

- **T1 nexoura-engagement-lifecycle** — §3 (Stage 2 stub this skill expands), §6 (artifact layout — superseded by T3).
- **T2 nexoura-gate-protocol** — §3 (`gate.json` schema, `decision_kind: "strategic"`), §4 (advance / reject / revise), §7.1 (bilingual strategic gate prompt).
- **T3 nexoura-artifact-conventions** — §3 (`gates/` and `02-requirements/` placement), §4 (per-stage required artifacts), §5 (`.en.md` / `.ar.md` filename + parity contract), §8 (`stage2: …` and `gate: stage2 → stage3 …` commit grammar).
- **T6 nexoura-feasibility-stage** — preceding stage; this skill's input is its output (`feasibility-memo.en.md` + `go-no-go.json` with `decision == "GO"`).
- **T8 nexoura-branding-stage** (forthcoming) — next stage; will consume the PRD §4 persona section to produce `personas.md` with visual identity and tone.
- **T4 nexoura-pdpl-compliance** (deferred) — DPIA template for `pdpl-assessment.md`; until T4 lands, the placeholder pattern in §7 holds and the NFR security row in §4 carries the PDPL flag.
