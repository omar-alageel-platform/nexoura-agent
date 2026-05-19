---
name: nexoura-operations-stage
description: "Use when running NEXOURA Stage 6 — phrases like 'ops runbook for <engagement>', 'NEXOURA stage 6', 'operations playbook', 'SLA for <slug>', 'on-call rotation', 'incident response runbook', 'billing ops for <slug>', 'ZATCA invoicing', 'KPI dashboard spec', 'customer onboarding flow', 'enhancement triage', 'promote enhancement to Stage 7', 'open the operational gate-6-to-7'. T11 stage skill — turns a launched Stage 5 product into a CONTINUOUS day-2 operation: SLA, on-call tiers, incident response (with the inlined 72-hour PDPL breach path from T4), tenant onboarding, SAR + 15% VAT (ZATCA-compliant) billing, KPI dashboards, and an enhancement-capture loop that promotes batches into Stage 7 via an operational gate per T2. Stage 6 has NO exit — it runs for the life of the engagement; the gate governs enhancement promotion, not stage closure."
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, stage-skill, operations, stage-6, sla, on-call, incident-response, billing, kpi, enhancement-loop]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-requirements-stage
      - nexoura-pdpl-compliance
---

# NEXOURA Operations — Stage 6 Playbook (T11)

Day-2 operation of a launched NEXOURA product. Unlike Stages 1–5, Stage 6 is **continuous**: no end-state, no "stage exit." It runs for the life of the product. The gate this skill governs (`gate-6-to-7`) is an **operational** gate per T2 §2 that promotes a batch of captured enhancements into a follow-on Stage 7 build cycle — it does not close Stage 6. Expands the T1 §3 Stage 6 stub; for lifecycle, gates, and file placement, defer to T1 / T2 / T3.

طلب — مرحلة التشغيل (Stage 6): تشغيل مستمرّ بلا نهاية، تحكمها اتّفاقيّة مستوى الخدمة، ومناوبة تشغيل متعدّدة الطبقات، واستجابة حوادث متوافقة مع نظام حماية البيانات الشخصيّة، ودورة التقاط التحسينات وترقيتها.

---

## §1. Scope and triggers

**Triggers.** "ops runbook for `<engagement>`"; "NEXOURA stage 6"; "operations playbook"; "SLA for `<slug>`"; "on-call rotation"; "incident response runbook"; "billing ops"; "ZATCA invoicing"; "KPI dashboard spec"; "customer onboarding flow"; "enhancement triage"; "promote enhancement to Stage 7"; "open the operational gate-6-to-7".

**Non-triggers (defer).** Feasibility → T6. PRD / NFRs → T7 (this skill *validates* NFRs in prod; it does not author them). Brand → T8. Stack / ADRs → T9. Pricing model + launch sequence → T10. Gate state-machine → T2. Filenames / placement → T3. PDPL legal substance → T4 (this skill inlines only the 72-hour breach path).

**Preconditions.** `manifest.json:current_stage == "06-operations"`. Stage 5 left behind `05-gtm/pricing.md` (SAR amounts, VAT treatment, billing cadence), `05-gtm/launch-plan.md`, and a partner-signed `gates/gate-5-to-6.json` with `decision == "GO"`. Stage 4 left behind `04-tech/architecture.md`, `04-tech/deployment-topology.md` (data-residency posture, per T4), and `04-tech/integrations.md` (ZATCA e-invoice integration surface lives here). If any of these are missing, abort and route back to the owning stage.

---

## §2. Stage 6 workflow (continuous)

Stage 6 is a steady-state loop, not a one-shot pipeline. The first pass through stands the operation up; every subsequent pass refines it. There is no terminal step.

1. **Stand-up (one-shot, week 0).** Author `sla.md`, `ops-runbook.{en,ar}.md`, `incident-response.md`, `onboarding-flow.md`, `kpi-dashboard-spec.md`. SRE Lead signs the runbook. Security Lead signs the incident-response plan. Finance / Billing Lead signs the billing ops section. Partner signs the bundle.
2. **Onboard tenants (continuous).** Run the §6 flow per new tenant. Track time-to-first-value as a KPI (§8).
3. **Operate (continuous).** On-call rotation per §4; incident response per §5; billing cycles per §7; KPI review weekly per §8.
4. **Capture enhancements (continuous).** Every support ticket, incident postmortem action item, NPS comment, and account-manager note feeds `enhancement-log.jsonl` per §9.
5. **Triage (weekly).** Enhancement Triage Council scores the log (RICE + strategic-fit) and tags items `defer | quick-win | promote-to-stage-7`.
6. **Operational gate (when a Stage 7 batch is ready).** Engagement owner writes `gates/gate-6-to-7.json` per T2 §3 + §10 below. Operational decisions: `READY` (promote the batch), `NOT-READY` (keep capturing), `CONDITIONAL` (promote with explicit constraints). Stage 6 keeps running through and after the gate.

Stage 6 never transitions `manifest.json:current_stage` to a different stage. The gate appends to `gate_history` and creates a Stage 7 engagement-child, but `current_stage` stays `"06-operations"`.

---

## §3. SLA framework — `sla.md`

Three uptime tiers, four severity tiers, response and resolution targets per (tier × severity). KSA business hours = Sun–Thu 08:00–17:00 AST; off-hours and Fri/Sat covered by on-call.

### 3.1 Uptime tiers

| Tier | Uptime SLO | Monthly error budget | Typical buyer |
|------|------------|----------------------|---------------|
| **Bronze** | 99.5% | 3h 39m | SMB pilot, sandbox tenants |
| **Silver** | 99.9% | 43m 12s | KSA SMB production, default tier |
| **Gold** | 99.95% | 21m 36s | Enterprise; named in contract |

Measurement: synthetic probes every 60s from two in-Kingdom regions + one international. A minute counts as down if both in-Kingdom probes fail. Status page surfaces real-time uptime per T10 launch-plan §X (when relevant).

### 3.2 Severity tiers

- **P1 — Critical.** Production down for ≥ 10% of tenants, or any data-integrity / PDPL exposure event. Response **15 min**, mitigation **1h**, resolution **4h**. War room opens, partner paged.
- **P2 — High.** Major feature degraded; workaround exists. Response **1h** business / **2h** off-hours, resolution **next business day**.
- **P3 — Medium.** Single-tenant impact or non-blocking bug. Response **1 business day**, resolution **5 business days**.
- **P4 — Low.** Cosmetic / enhancement request. Response **3 business days**, resolved in the enhancement loop (§9), not the incident channel.

`sla.md` carries the full grid plus the credit schedule (SLO breach → service credit per §7.4).

---

## §4. On-call and support tiers

Three escalation tiers, weekly rotation, written handoff per §4.3.

### 4.1 Escalation ladder

- **L1 — App Support (Tier 5A).** First responder. Triages tickets, classifies severity, runs the §5.2 first-15-minutes checklist, applies known-good runbook entries. May restart workers, rotate API keys, re-run a stuck job. **May not** ship code, perform production DB writes outside runbook macros, or contact clients on a P1 (defers to L2).
- **L2 — SRE / Service Owner (Tier 5B).** Second responder. Owns mitigation: feature-flag rollback, traffic shedding, dependency cutover, hotfix coordination. Opens the war room on P1. Carries pager off-hours.
- **L3 — Engineering / Security on-call (Tiers 5B + 5C).** Engineering writes the hotfix; Security leads any PDPL-touching incident (§5.5). Partner paged in parallel for P1.

### 4.2 Rotation

Weekly. Handoff Sundays 10:00 AST. Minimum two engineers per tier (primary + backup). Compensating rest after any pager event exceeding 60 minutes off-hours. No single human carries L2 + L3 simultaneously.

### 4.3 Handoff protocol

Outgoing on-call writes to the shared on-call log: (a) open incidents and state, (b) tenants in elevated-watch, (c) deferred follow-ups due this week, (d) any anomaly that did not page but should be watched. Incoming acknowledges in writing before outgoing leaves the channel. No verbal-only handoffs.

---

## §5. Incident response — `incident-response.md`

### 5.1 Severity classification

L1 classifies on first contact using the §3.2 grid. Reclassification is allowed at any time; every reclassification is logged with rationale. Default-up: when in doubt between P1/P2, treat as P1 until evidence supports downgrading.

### 5.2 First 15 minutes (P1 checklist)

1. Acknowledge the page; declare incident in the incident channel.
2. Page L2; if PDPL-touching, page Security on-call (L3) in parallel.
3. Open war room (audio bridge + shared doc). Assign Incident Commander (IC), Comms, Scribe.
4. Snapshot: status-page metrics, error rates, recent deploys (last 24h), recent config changes.
5. Decide: mitigate-first (rollback, flag-off, traffic shed) vs. diagnose-first. Default: mitigate-first if customer-visible.
6. First customer comms within 30 min for P1, even if cause unknown ("we are investigating; next update in 30 min").

### 5.3 Runbook structure (`ops-runbook.{en,ar}.md`)

Bilingual pair, T3 §5 parity. EN is authoritative for operator procedures; AR mirror keeps section numbering and translates user-facing message templates. Required H2 skeleton:

```markdown
# Operations Runbook — <product> (Stage 6)

## 1. Architecture orientation (pointer to 04-tech/architecture.md)
## 2. Daily checks (08:00 AST checklist)
## 3. Common procedures (deploy, rollback, key rotation, backup restore drill)
## 4. Known-good macros (one section per L1-authorised action)
## 5. Escalation paths (cross-ref §4)
## 6. Postmortem template (cross-ref §5.4)
## 7. PDPL breach path (cross-ref §5.5 — inlined, not by reference)
## 8. Contacts and pager schedule (link, not literal phone numbers)
```

The AR mirror keeps the same H2 numbering; macros named in Latin (`ROLLBACK_LAST_DEPLOY`) stay Latin per T3 §5.

### 5.4 Postmortem template

Within 5 business days of a P1 / P2 resolution: timeline (UTC), impact (tenants × minutes × revenue), root cause (technical), contributing factors (process), what went well, what went poorly, action items (each with owner + due date + tracking link). Blameless register; humans are never the root cause, systems that let humans fail are. Action items feed `enhancement-log.jsonl` per §9.

### 5.5 PDPL breach path (inlined from T4 — 72-hour SDAIA SLA)

Inlined verbatim so on-call does not load T4 mid-incident:

1. **T+0** — Security on-call declares "PDPL breach suspected". Containment begins (revoke tokens, isolate affected tenants, freeze relevant logs read-only).
2. **T+4h** — Forensics snapshot captured (logs, DB state, access traces) to evidence vault. Legal and partner paged.
3. **T+24h** — Scope confirmed: tenants affected, data categories, volume, lawful basis impacted (cross-ref `02-requirements/pdpl-assessment.md`).
4. **T+48h** — Draft SDAIA notification + draft data-subject notifications (AR + EN). Legal sign-off.
5. **T+72h** — SDAIA notification submitted; data-subject notifications dispatched per preferred language. Public statement only if scope warrants (partner decision).
6. **Post-incident** — Full postmortem per §5.4 with the PDPL action-item track separately tagged for regulator follow-up.

AR + EN templates for SDAIA notification and data-subject notification live in `incident-response.md` §6.3. Operator fills blanks; does not draft mid-incident.

---

## §6. Tenant onboarding — `onboarding-flow.md`

New-tenant journey from contract-signed to first-value, target ≤ 1 business day for Silver. Steps:

1. **Provisioning (automated, ≤ 15 min).** Tenant record created; data-residency region set per `04-tech/deployment-topology.md`; admin invited via bilingual email.
2. **Welcome call (≤ 1 business day; optional Bronze, mandatory Silver/Gold).** Customer Success walks the in-product tour, confirms payment method, captures escalation contact.
3. **Data import (variable).** Self-service for documented formats; CS-assisted otherwise. Validation report in AR + EN.
4. **First-value milestone.** Tenant performs the keystone action (defined per-engagement in `prd.en.md` §2). Logged as `time_to_first_value` (KPI §8).
5. **30-day check-in.** CS reviews usage, surfaces NPS, captures enhancement requests into `enhancement-log.jsonl`.

Tenant health: `green` (healthy), `amber` (declining usage, payment retry, or NPS < 7), `red` (payment failed twice, or no logins for 14 days, or open P2 > 5 days). Amber → CS outreach; red → save play (§7.6).

---

## §7. Billing operations

### 7.1 Currency and tax

Primary currency: **SAR**. Invoices priced in SAR with **15% VAT** per ZATCA rules. USD parenthetical acceptable on contract-summary surfaces only; invoices are SAR-only. VAT number printed on every invoice. ZATCA e-invoice integration (from `04-tech/integrations.md`) must be in place before the first paid invoice issues.

### 7.2 Invoice generation (ZATCA-compliant)

Each invoice carries the ZATCA-mandated fields: seller VAT, buyer VAT (when applicable), sequential invoice number, issue date, supply date, item description (AR + EN for KSA buyers), unit price, line total, tax rate (15%), tax amount, gross total, QR code encoding the ZATCA payload, UUID, hash, and previous-invoice hash (FATOORA phase-2 chaining). Invoices issue from the e-invoice service; never hand-rolled.

### 7.3 Payment, dunning, retries

Default cycle: monthly, in advance. Retry on payment failure: T+1, T+3, T+7 days (each retry → bilingual dunning email). T+10 with no recovery → `amber`; T+14 → `red`, access soft-degrades (read-only). T+30 → suspension (formal 7-day notice prior, AR + EN). No silent suspension.

### 7.4 SLO credits

SLO breach (§3.1) auto-credits next invoice: Silver → 10% credit per affected hour beyond budget, capped at 30% of monthly fee; Gold doubles those. Manual override requires Finance Lead approval logged in `billing-ops` notes.

### 7.5 Churn detection

Signals: payment failure, usage drop > 50% week-on-week, NPS < 6, sentiment-flagged support tickets. Any two within 14 days → `red` + save play.

### 7.6 Save play

CS contacts within 1 business day; offers discount or pause; captures cancel reason into `enhancement-log.jsonl` (cancellations are the highest-signal enhancement source). No discount > 30% without partner approval; no permanent discount without contract amendment.

---

## §8. KPI dashboard — `kpi-dashboard-spec.md`

Six headline metrics, refreshed at least hourly, reviewed weekly.

| KPI | Definition | Target (default) | Owner |
|-----|------------|------------------|-------|
| **Uptime** | Per §3.1 measurement | Meet tier SLO | SRE Lead |
| **MTTR** | Mean time-to-resolve, P1+P2, trailing 30 days | < 2h | SRE Lead |
| **NPS** | Net Promoter, 0–10, trailing 90 days | ≥ +30 | Customer Success Lead |
| **MRR** | Monthly recurring revenue, SAR | Plan per `05-gtm/pricing.md` | Finance Lead |
| **Logo churn** | Cancelled tenants / opening tenants, monthly | < 2% | Customer Success Lead |
| **Time-to-first-value** | Median across new tenants this month | ≤ 1 business day (Silver) | Customer Success Lead |

The spec file documents data sources, transformation rules, the dashboard layout (one screen, AR + EN labels), and the weekly review agenda. Dashboards live in the existing analytics surface — this skill specifies *what*, not *which BI tool*.

---

## §9. Enhancement coordination loop

`enhancement-log.jsonl` (under `06-operations/`) is append-only, one JSON object per captured enhancement:

```json
{
  "id": "ENH-2026-0142",
  "captured_at": "2026-05-19T11:00:00Z",
  "source": "support-ticket | postmortem | nps | account-manager | churn-exit",
  "summary_en": "...",
  "summary_ar": "...",
  "tenant_count_affected": 7,
  "rice": {"reach": 7, "impact": 2, "confidence": 0.8, "effort_weeks": 3},
  "strategic_fit": "core | adjacent | out-of-scope",
  "tag": "defer | quick-win | promote-to-stage-7",
  "linked_incidents": ["INC-2026-0031"]
}
```

Weekly triage: Enhancement Triage Council (SRE Lead + Customer Success Lead + Product, with partner as tie-breaker) scores. `quick-win` items ship within the current Stage 6 budget (no gate). `promote-to-stage-7` items batch toward the next operational gate. `defer` items remain in the log; review quarterly.

When ≥ 5 `promote-to-stage-7` items accumulate, OR strategic-fit "core" items have aged > 30 days, the engagement owner opens `gate-6-to-7` per §10.

---

## §10. Operational gate — `gates/gate-6-to-7.json`

Operational gate per T2 §2. Decisions: `READY | NOT-READY | CONDITIONAL`. The gate **promotes a batch of enhancements** into a Stage 7 build cycle; it does not exit Stage 6.

### 10.1 Bilingual gate-request prompt (≤ 30 lines total)

```text
GATE — <slug> enhancement promotion (06-operations → 07-build-cycle)
Batch size: <N> enhancements; effort: <M> engineer-weeks
Artifacts: 06-operations/{sla.md, ops-runbook.en.md, incident-response.md,
  kpi-dashboard-spec.md, onboarding-flow.md, enhancement-log.jsonl}

Summary: Stage 6 healthy — uptime <U%>, MTTR <T>, NPS <N>, churn <C%>.
Batch: <one-line per item with RICE score and strategic_fit>.
Conditions to surface (if any): <list>.

Reply: READY | NOT-READY | CONDITIONAL — plus a one-sentence rationale,
and (for CONDITIONAL) one condition per line.
```

```text
بوابة تشغيليّة — ترقية التحسينات (06-operations ← 07-build-cycle) — <slug>
حجم الدفعة: <N> تحسينات؛ الجهد المقدّر: <M> أسبوع-مهندس
المخرجات: 06-operations/{sla.md, ops-runbook.en.md, incident-response.md,
  kpi-dashboard-spec.md, onboarding-flow.md, enhancement-log.jsonl}

ملخّص الجاهزية: الجاهزة سليمة — توافر <U%>، زمن الإصلاح <T>،
صافي مؤشّر الترشيح <N>، نسبة الفقد <C%>. الدفعة: <عناصر مختصرة>.

يُرجى الإفادة: READY | NOT-READY | CONDITIONAL مع مسوّغ مختصر،
وفي حالة CONDITIONAL تُذكر الشروط كلٌّ في سطر مستقل.
```

### 10.2 Decision paths

- **READY** — batch promoted; Stage 7 engagement-child opens; Stage 6 continues unchanged.
- **NOT-READY** — batch deferred; keep capturing; reopen when triage criteria re-met. `next_action` names the gap.
- **CONDITIONAL** — batch promoted with explicit `conditions[]` (e.g. "ship behind a feature flag until 100 tenants validate"). Conditions tracked in `ops-runbook.md` §4 macros for the lifespan of the Stage 7 work.

Commit per T3 §8: `gate: stage6 → stage7-cycle-N <decision>`.

---

## §11. Specialist tier organization

Five sub-teams (5A–5E are organizational labels, not stage IDs):

- **5A App Support.** L1 / L2 / L3 responders per §4 + **Bug Triager** (ticket queue, severity classification, first-pass `enhancement-log.jsonl` capture).
- **5B SRE.** **Infrastructure** (IaC, capacity) + **On-Call** (§4 rotation primary) + **Performance** (NFR validation in prod per §12). Owns `ops-runbook.{en,ar}.md` and the §3 SLA grid.
- **5C Security.** **Monitoring** (SIEM) + **Incident Response** (lead §5.5 PDPL path) + **Forensics** (evidence vault) + **Compliance** (PDPL per T4, ZATCA per §7.2). Owns `incident-response.md` §5.5.
- **5D Customer Success.** **Support** (soft-issue escalation) + **Account Management** (save plays, expansion). Owns `onboarding-flow.md` and the NPS / churn KPIs.
- **5E Maintenance.** **Patches** (security + dependency cadence) + **Docs** (keeps runbooks current) + **Audit** (quarterly review, feeds gaps into §9).

Small engagements compress 5A+5D into one human and 5B+5E into another. Roles, not headcounts, are load-bearing.

---

## §12. Cross-references

- **T1 §3** — Stage 6 stub (continuous; operational gate). This skill expands it; T1 §3 is normative for the lifecycle frame.
- **T2 §2 + §3** — operational gate vocabulary and schema. `decision_kind` is `operational`; decisions are `READY | NOT-READY | CONDITIONAL`. Atomic write order per T2 §5.
- **T3 §3 + §4** — `gates/gate-6-to-7.json` lives under `gates/` (not `06-operations/`); per-stage required artifacts under `06-operations/`.
- **T7 §4 NFRs** — every Stage 2 NFR target (availability, latency, throughput, recoverability, security, localization, accessibility) MUST be wired into a §8 KPI or an alert in `ops-runbook.md` §2. NFRs not measurable in production are not NFRs — route back to T7. Stage 6 is where T7's NFRs prove out.
- **T4 (PDPL)** — §5.5 inlines the 72-hour SDAIA breach path verbatim. T4 carries the legal substance; do not re-derive at incident time.

---

## §13. Output artifacts summary

All under `engagements/<slug>/06-operations/` unless noted (T3 §4):

| Path | Owner (§11) | Notes |
|------|-------------|-------|
| `ops-runbook.en.md` | SRE Lead (5B) | English runbook; H2 skeleton per §5.3. |
| `ops-runbook.ar.md` | SRE Lead (5B) + Docs (5E) | AR mirror; KSA-formal; T3 §5 parity. |
| `sla.md` | SRE Lead (5B) | Tier × severity grid per §3; credits per §7.4. |
| `incident-response.md` | Security Lead (5C) | §5; §5.5 PDPL inlined; AR/EN templates §6.3. |
| `onboarding-flow.md` | CS Lead (5D) | §6; health states; bilingual email templates. |
| `kpi-dashboard-spec.md` | SRE + CS Leads | §8 grid; sources; weekly-review agenda. |
| `enhancement-log.jsonl` | Bug Triager (5A) | Append-only; schema §9; feeds §10 batches. |
| `../gates/gate-6-to-7.json` | Engagement owner | Operational gate per T2 §3; one per batch. |

**Stand-up-complete** (not stage-complete — Stage 6 has no completion) when the seven `06-operations/` files exist, are non-empty, the runbook pair has matching H2 count, `incident-response.md` §5.5 is present verbatim, and the first weekly KPI dashboard has rendered against live data. From there Stage 6 runs forever; gates fire as enhancement batches mature.

---

When T4 lands as a full skill, §5.5 collapses to a pointer plus the inlined operator-facing template strings; the operational discipline (§§1–4, §6–§13) is stable.
