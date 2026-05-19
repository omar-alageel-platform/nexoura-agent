---
name: nexoura-tech-architecture-stage
description: "Use when running NEXOURA Stage 4 — phrases like 'architect <engagement>', 'tech stack selection', 'NEXOURA stage 4', 'ADR for <X>', 'data model for <slug>', 'deployment topology for <X>', 'KSA integrations (ZATCA / Fasah / Nafath / Wathq)', 'cost model for <slug>', 'open the strategic gate from stage 4'. T9 stage skill — turns a Stage 3 partner-signed brand into a partner-signable architecture bundle (architecture overview, ADRs, data model, integrations, deployment topology, cost) and hands off via a strategic gate per T2."
version: 1.0.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, stage-skill, tech-architecture, stage-4]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-requirements-stage
      - nexoura-branding-stage
      - nexoura-pdpl-compliance
---

# NEXOURA Tech Architecture — Stage 4 Playbook (T9)

Turns a signed Stage 3 GO into a partner-signable architecture bundle. Six artifacts under `04-tech/` plus the gate decision under `gates/`, one strategic gate at exit per T2 §3. Implementation itself is out of scope in NEXOURA v1 — this stage produces the design and the budget; build kickoff is deferred to v2. Expands the T1 §3 Stage 4 stub; for lifecycle, gates, filenames, defer to T1 / T2 / T3.

طلب — مرحلة العمارة التقنية (Stage 4): من هويّة العلامة إلى تصميم يُبنى منه ومُوازَنَة تُعتمَد.

---

## §1. Triggers and preconditions

**Triggers.** "architect `<engagement>`"; "tech stack selection"; "NEXOURA stage 4"; "ADR for `<X>`"; "data model for `<slug>`"; "deployment topology for `<X>`"; "KSA integrations" / "ZATCA / Fasah / Nafath / Wathq"; "cost model for `<slug>`"; "open the strategic gate from stage 4".

**Non-triggers (defer).** Feasibility → T6. PRD/NFR/stories → T7. Naming/brand/visual → T8. Pricing/channels/launch → T10. Runbook/SLA/incident → T11. Gate mechanics → T2. File placement → T3. PDPL DPIA substance → T4 (deferred — see §5.4, §13).

**Preconditions.** `manifest.json:current_stage == "04-tech"`; `gates/gate-3-to-4.json` is `approved` with `decision: "GO"`; `02-requirements/{prd.en.md,prd.ar.md,nfr.md}` and `03-branding/brand-book.{en,ar}.md` exist. If `current_stage != "04-tech"`, abort and surface the manifest. If the inbound gate is not approved-GO, refuse and route the operator to T2.

---

## §2. Stage 4 scope and outputs

Six artifacts under `04-tech/` plus the gate file under `gates/` (T3 §3). Filenames are canonical per T3 §4 — this skill does not invent paths.

| Path | Owner (§10) | Required H2 sections |
|------|-------------|----------------------|
| `04-tech/architecture.md` | Solution Architect | 1 System context · 2 Component inventory · 3 Data flow · 4 Trust boundaries · 5 NFR coverage matrix · 6 Brief AR executive summary |
| `04-tech/adrs/NNNN-<slug>.md` (≥ 3) | Solution Architect (+ specialist) | Status · Context · Decision · Consequences · Alternatives (§4) |
| `04-tech/data-model.md` | Data Architect | 1 Entity inventory · 2 Schema conventions · 3 Versioning + migration · 4 Personal-data inventory (PDPL hook) |
| `04-tech/integrations.md` | Solution Architect | 1 Third-party catalogue · 2 KSA government surfaces (§8) · 3 Auth + secret handling · 4 Failure modes |
| `04-tech/deployment-topology.md` | DevOps Engineer | 1 Environments · 2 Regions + residency · 3 Network + edges · 4 Scaling · 5 DR (RTO/RPO) |
| `04-tech/cost.md` | Cost Engineer | per §9.1 |
| `gates/gate-4-to-5.json` | Engagement owner | per T2 §3 — `decision_kind: "strategic"` |

In-scope: design, decisions, costed plan, integration contracts. Out-of-scope (v1): application code, live infrastructure, load/pen tests, Figma comps (text-level per T8 §6.5). The §11 gate approves architecture + budget; build kickoff is v2 — the gate `summary` makes this explicit.

---

## §3. Stack selection methodology

A stack is `(runtime, web framework, datastore, queue, cache, IaC, CI/CD, observability, identity)`. Selection precedes ADRs — each significant choice becomes one ADR (§4).

### 3.1 Criteria matrix (score 1–5; any score-1 in a Hard column disqualifies)

| Criterion | Weight | Hard? | Source of truth |
|-----------|:-----:|:-----:|-----------------|
| NFR fit (perf, availability, RTL/i18n) | 0.25 | yes | `02-requirements/nfr.md` — every numeric target reachable |
| KSA data residency + sovereign-cloud availability | 0.15 | yes | §7.2 + T4 (deferred) |
| Operator skill + KSA labour market | 0.10 | no | Operator profile, Riyadh talent availability |
| 3-year TCO (SAR) | 0.15 | no | `cost.md` §6 |
| Ecosystem maturity (LTS, CVE response, vendor stability) | 0.10 | no | Public CVE feeds, vendor LTS calendar |
| Vendor lock-in risk | 0.10 | yes | §3.3 |
| Bilingual / RTL first-class support | 0.05 | yes | Framework ships RTL primitives, not bolt-on |
| Integration fit with §8 KSA surfaces | 0.05 | no | §8 catalogue |
| Compliance posture (ISO 27001, SOC 2, NCA ECC alignment) | 0.05 | no | Vendor attestation pack |

Weighted score = Σ(weight × raw). Score-1 in any Hard column disqualifies regardless of total. Disqualified candidates are documented in ADR §4 Alternatives — never silently dropped.

### 3.2 Process

(1) ≥ 2 candidates per stack slot — single-candidate proposals fail review. (2) Score against §3.1 in a working table inside the ADR draft. (3) Winner = highest weighted score that passes every Hard column. (4) ADR records matrix + choice + alternatives with source citations (vendor docs, CVE feeds, KSA presence pages); "trust me" is not acceptable.

### 3.3 Vendor lock-in assessment

For every paid managed service in the winning stack, the ADR answers: **(a) Exit cost** — engineer-weeks to migrate. **(b) Data export** — documented bulk-export path in an open format? **(c) Proprietary surface** — fraction of code calling vendor-only APIs (target ≤ 10%). **(d) Reversal trigger** — observable event (price >2× budget, KSA market exit, CVE without 30-day patch) forcing migration. Lock-in is acceptable when answered, rejected when unanswered.

---

## §4. ADR process and template

Every significant decision lands as one ADR file under `04-tech/adrs/` per T3 §5 (`NNNN-short-title.md`, four-digit zero-padded monotonic counter starting at `0001`, never reused, never renumbered on rebase). Minimum three ADRs at gate; 5–12 typical. "Significant" = a choice that is hard to reverse, cross-cutting, or materially changes `cost.md`. Examples: runtime; primary datastore; auth provider (Nafath vs. in-house IAM); region (in-Kingdom vs. me-south-1); event-bus vs. direct calls; multi-tenant isolation model.

### 4.1 Template (paste verbatim)

```markdown
# ADR NNNN — <one-line decision title>

- **Status:** Proposed | Accepted | Superseded by ADR NNNN | Deprecated
- **Date:** YYYY-MM-DD
- **Authors:** <role>, <role>
- **Stage gate:** stage4 → stage5

## 1. Context
What forces this decision now? Cite `nfr.md` row(s) and prior ADRs. 2–4 paragraphs, no solution language.

## 2. Decision
One paragraph, active voice: "We will use <X> for <Y> because <Z>." Followed by the §3.1 scoring matrix as a markdown table.

## 3. Consequences
### Positive / Negative / Neutral
Bulleted. Negative includes lock-in posture per §3.3 for paid managed services.

## 4. Alternatives considered
Per alternative: name, why considered, why rejected (≥ 1 sentence each). ≥ 2 alternatives. "No alternative" is itself an alternative and must be argued.

## 5. References
NFR rows; vendor docs (URLs + retrieved YYYY-MM-DD); related ADRs.
```

### 4.2 Lifecycle

Append-only. Never edit a past ADR's Decision. To reverse: write a new ADR (`NNNN+1`) with `Accepted`, whose §1 cites the prior; update the prior ADR's Status line only to `Superseded by ADR NNNN+1`. `git log -- 04-tech/adrs/` is the audit trail.

---

## §5. Data model conventions — `data-model.md`

Logical model first; physical schema notes follow. Diagrams text-level (Mermaid ER blocks) — no binary images in v1.

**§5.1 Entity inventory.** Table of entities: name, owner-service, primary identifier, cardinality, personal-data flag (Y/N — feeds T4), residency (in-Kingdom / unrestricted), retention period (days; cite `nfr.md` or KSA regulatory floor — ZATCA invoice retention is 6 years per Article 9 of the e-invoicing regulation).

**§5.2 Schema conventions.** IDs: UUID v7 (time-ordered); never auto-increment integers across service boundaries. Naming: snake_case columns, singular tables (`customer`), foreign keys `<referenced>_id`. Timestamps: `created_at`, `updated_at` on every table; UTC ISO-8601 (`TIMESTAMPTZ` in Postgres) — Hijri is presentation, not storage. Soft delete: `deleted_at TIMESTAMPTZ NULL` on personal-data tables (PDPL right-to-erasure complicates this — flagged for T4). Money: minor units (halalas for SAR) as `BIGINT`; never `FLOAT`; currency code on the row. Bilingual fields: `name_en` + `name_ar` as separate columns when user-visible; never one JSON blob.

**§5.3 Versioning + migration.** Forward-only migrations, monotonically numbered (`0001_init.sql`, `0002_<verb>.sql`); rollback is a new forward migration. Each migration transactional unless DDL forbids (`CREATE INDEX CONCURRENTLY`). API-visible breaking changes require an ADR; additive same-shape changes do not. Each PII column carries `-- PII: <category>` (national_id, phone, address, biometric, location, payment, health) — T4 lifts these into a formal inventory.

**§5.4 Personal-data inventory (PDPL hook).** Subsection lists every PII column, category, lawful-basis placeholder, retention period. **Lawful-basis decision is deferred to T4 nexoura-pdpl-compliance** — this section captures the surface so T4 can populate without a data-model change. Do not invent lawful-basis text here.

---

## §6. API design patterns

**§6.1 REST vs. GraphQL rubric.** REST when external integrators (KSA banks, government endpoints) consume the API, the surface is verb-centric, HTTP caching matters, response shape stable per resource. GraphQL when a single client drives most calls, query shape varies per screen, over-fetching is a measured pain point. Mixed acceptable: REST for integrators, GraphQL for first-party app. The choice lands in an ADR.

**§6.2 Versioning.** REST: URI-versioned (`/v1/...`); `v1` only at launch. Deprecation ≥ 6 months notice; `Sunset` header (RFC 9745) on the deprecated version. GraphQL: schema evolution with `@deprecated(reason: "…")`; no URL version.

**§6.3 Auth.** Internal: mTLS or signed JWT, ≤ 1 h TTL, KMS-rotated keys. External integrator: OAuth 2.0 client_credentials or signed JWT bearer. End-user: OIDC; Nafath as IdP for KSA-resident users where lawful and operationally fit (§8.3). Secrets vault-issued at deploy time per T7 §4 NFR Security.

**§6.4 Rate limiting.** Token-bucket per `(api_key, route_group)`; soft `429` with `Retry-After`; hard `403` with rationale. Default tiers: anonymous 10 req/min/IP; authenticated 600 req/min/principal; integrator 6 000 req/min/principal (negotiable). KSA government surfaces (§8) impose vendor limits — the integration layer respects and surfaces them.

**§6.5 Conventions.** Idempotency keys on every non-`GET` (`Idempotency-Key: <uuid>`). Cursor pagination on tables > 100 k rows (never offset). Errors: RFC 9457 `application/problem+json` with bilingual messages on user-facing endpoints (keyed by `Accept-Language`). Time: ISO-8601 UTC on the wire; presentation handles Hijri/Gregorian.

---

## §7. Deployment topology and DR — `deployment-topology.md`

**§7.1 Environments.** Minimum `dev` / `staging` / `prod`. A fourth `sandbox` is required when §8 KSA integrations are in scope. Promotion dev → staging → sandbox (if needed) → prod; no skipping. Config environment-scoped, never branched by code path.

**§7.2 Regions and KSA data residency.** Default for engagements processing KSA-resident personal data: **in-Kingdom primary region**. Supported KSA / GCC presences (2026): STC Cloud (Riyadh, Jeddah — sovereign); Mobily Cloud (Riyadh); AWS me-south-1 (Bahrain — GCC, not in-Kingdom; acceptable only with documented PDPL exception, T4-deferred); AWS me-central-1 / Azure KSA Central (in-Kingdom AZs); Oracle Jeddah (in-Kingdom); GCP Dammam (in-Kingdom). The region ADR cites a specific presence and its sovereign-cloud status. Cross-border transfer of personal data requires the T4 cross-border decision; until T4 lands, default in-Kingdom and flag any exception as a blocker.

**§7.3 Network + edges.** Public surface fronted by WAF + CDN, edge in-Kingdom where the provider supports it. TLS 1.3 terminated at the edge; mTLS service-to-service inside the VPC. Egress through a NAT with static IPs (KSA government surfaces often require IP allowlisting). Datastores on private subnets; no public IP on databases ever.

**§7.4 Scaling.** Stateless web tier behind an autoscaler keyed on p95 latency + CPU. Workers behind a queue (SQS/SNS-equivalent, RabbitMQ, NATS), keyed on queue depth. Datastore vertical-scaled to one node class; read replicas for read-heavy workloads. Cache (Redis-equivalent) sized to ≥ 20% of hot working set.

**§7.5 DR — RTO / RPO.** Default v1 targets (cite `nfr.md` Availability rows): **RTO ≤ 4 h** — restore to degraded read-only within 4 h of region outage. **RPO ≤ 1 h** — at most 1 h of writes lost. Backups: continuous WAL archive to in-Kingdom object storage; hourly logical snapshot; daily verified restore drill in `staging`. Multi-region failover out of scope for v1 unless an NFR row demands it; second in-Kingdom region (STC Riyadh primary + Jeddah secondary) is the preferred upgrade path. Cross-border DR replication is a T4 decision; do not encode it without T4 sign-off.

---

## §8. KSA integrations — `integrations.md` §2

Mandatory whenever the engagement touches the named domain. Four canonical KSA government / regulatory surfaces. For each: purpose, sandbox URL placeholder, auth model, integration pattern. **All URLs below are placeholders** — confirm against the authority's developer portal at integration time; URLs drift.

### 8.1 ZATCA — Zakat, Tax and Customs Authority (e-invoicing / Fatoorah)

- **Purpose.** Mandatory e-invoicing for VAT-registered KSA entities (Phase 2 "Integration" — XML invoices, cryptographic stamp, real-time clearance B2B / reporting B2C).
- **Sandbox URL (placeholder).** `https://gw-apic-gov.gazt.gov.sa/e-invoicing/developer-portal` — confirm at integration time.
- **Auth model.** Onboarding via OTP-issued CSID (Cryptographic Stamp Identifier); per-invoice signing with the device certificate; PIH (Previous Invoice Hash) chained per device.
- **Integration pattern.** Outbound: generate UBL 2.1 XML invoice → embed QR (TLV-encoded fields) → sign → submit to clearance endpoint synchronously (B2B) or reporting endpoint within 24 h (B2C). Inbound: store clearance response (UUID, status, hash) on the invoice row; retry on transient errors with idempotent re-submission keyed on invoice UUID.
- **Retention.** ZATCA-mandated 6-year retention for invoices, credit notes, debit notes — encoded in `data-model.md` §5.1 retention column.
- **Operational.** Two environments (sandbox + prod); certificate issuance is manual first-time per CR/VAT registration. Plan a one-week onboarding window with the client's accounting team.

### 8.2 Fasah — Customs single-window

- **Purpose.** Pre-clearance of imports/exports; required only when the engagement is a logistics / trade / customs-touching SaaS. If irrelevant, document as "not applicable, reason: <X>" — do not silently omit.
- **Sandbox URL (placeholder).** `https://fasah.sa/en/developer` — confirm at integration time.
- **Auth model.** Customs Broker license code + API key issued by ZATCA-Customs to the broker entity; tokens scoped per declaration type.
- **Integration pattern.** Outbound: submit declaration (manifest, BL, invoice, certificate-of-origin references) as JSON; poll status (or subscribe to event bus where available) until `cleared` / `rejected`. Inbound: parse rejection codes (catalogue of ~80 standardised codes) into actionable operator-facing messages.
- **Operational.** Customs cutover windows can shift quarterly; the integration surfaces a banner when sandbox and prod schemas diverge.

### 8.3 Nafath — National IAM (under Absher / NIC umbrella)

- **Purpose.** Identity assurance for KSA residents via the national app; satisfies KYC for regulated flows (financial, healthcare, government-adjacent). Absher is the broader citizen-services platform; Nafath is its authentication front-door for third parties.
- **Sandbox URL (placeholder).** `https://nafath.api.elm.sa/api/v1/mfa` (via Elm) — confirm at integration time; access is gated by a commercial agreement with Elm and a regulator-sanctioned use case.
- **Auth model.** OIDC-compatible; SP holds a `client_id` / `client_secret` issued post-onboarding; user authenticates in the Nafath mobile app (push-to-approve with a 6-digit verification number displayed in the SP UI for anti-phishing).
- **Integration pattern.** Initiate session with the user's national ID → display verification number → user approves in Nafath app → SP polls or receives webhook with signed assertion → SP verifies signature and consumes claims (full name, national ID, DOB, nationality). No password is exchanged.
- **Operational.** Nafath onboarding is the longest-lead-time KSA integration; budget **6–10 weeks** for commercial + regulator approval. Plan an in-house IAM fallback (email-OTP + phone-OTP) for non-KSA users and for the period before Nafath production access lands.

### 8.4 Wathq — Business registry

- **Purpose.** Authoritative B2B verification — pull a Saudi commercial registration (CR) record, legal status, authorised signatories, declared activities. Mandatory for KYB on enterprise-customer onboarding flows.
- **Sandbox URL (placeholder).** `https://api.wathq.sa/v1/commercialregistration/info/<cr>` — confirm at integration time; production access requires a Wathq subscription.
- **Auth model.** API key in `apikey` header; per-call billing on production tier; rate limits per subscription level.
- **Integration pattern.** Read-only lookup keyed on CR number. Cache the CR snapshot in `data-model.md` (entity `business_party`) with a `wathq_fetched_at` timestamp; refresh on a configurable cadence (default 90 days) or on demand. Treat Wathq as source of truth — never let operator-entered company data override a Wathq field silently.
- **Operational.** Wathq has multiple endpoints (CR info, contracts, ownership, activities); pick the minimum subset needed and document each in `integrations.md`.

### 8.5 Cross-cutting integration rules

**Secrets** — all KSA integration secrets in the vault per T7 §4 NFR Security; never in `.env` committed to the repo (T3 §6 `.gitignore` enforces). **Failure modes** — every integration in `integrations.md` §4 lists: timeout default, retry policy (jittered exponential backoff, max attempts), circuit-breaker threshold, operator-facing message when upstream is degraded. KSA government surfaces have public maintenance windows — subscribe to status feeds. **PDPL touchpoint** — personal-data fields returned by Nafath / Wathq feed `data-model.md` §5.4 with `PII: Y`. The lawful-basis decision is **deferred to T4 nexoura-pdpl-compliance**; until T4 lands, integration code captures the consent / regulatory-basis timestamp on the request row so T4 can backfill the lawful-basis label without a data-model change.

---

## §9. Cost model — `cost.md` (SAR + USD)

USD → SAR conversion: **1 USD ≈ 3.75 SAR** (SAMA peg; document the assumption in `cost.md` §1 and re-verify against SAMA at gate time).

### 9.1 Required structure

```markdown
## 1. Assumptions
- Year 1 traffic: <citation to Stage 1 SOM / NFR scalability row>.
- Region: <chosen per §7.2>.
- FX: 1 USD = 3.75 SAR (SAMA peg, retrieved YYYY-MM-DD).
- Tax: KSA VAT 15% on KSA-billed services; non-KSA vendors typically USD VAT-exempt
  with reverse-charge applying — flagged for T10/T11.
- Reserved-instance discounts: <applied / not applied; reason>.

## 2. Compute
| Component | SKU | Units | Unit price (USD) | Monthly (USD) | Monthly (SAR) |
| ... rows per service ... |

## 3. Storage   (block, object, backup, snapshots — same table shape)
## 4. Network / CDN   (egress, CDN requests, NAT, inter-AZ)
## 5. Third-party  (observability, error tracking, email, SMS — KSA SMS aggregator
                    pricing differs from international; Nafath/Wathq per-call fees)

## 6. Totals
| | Monthly USD | Monthly SAR | Annual USD | Annual SAR |
|--|--:|--:|--:|--:|
| Subtotal | ... | ... | ... | ... |
| + 15% VAT (KSA-billed only) | ... | ... | ... | ... |
| Total | ... | ... | ... | ... |

## 7. Sensitivity
- 2× traffic: total → <SAR>
- 0.5× traffic: total → <SAR>
- Reserved 1-yr commitment applied: total → <SAR>
- KSA-only region (no me-south-1 cost arbitrage): delta → <SAR>
```

### 9.2 Reproducibility and sanity check

Every row carries a source citation (vendor-calculator URL with retrieval timestamp, or contract reference). A reader must be able to re-derive the total without contacting the author. For a typical KSA B2B SaaS at 500–5 000 MAU, the v1 monthly cloud bill lands in the **2 000–8 000 USD (≈ 7 500–30 000 SAR)** band before third-party services. Third-party (observability, error tracking, email, SMS, Nafath/Wathq per-call) typically adds 30–60%. If the bottom-up total lands outside this band, surface the rationale in §1 Assumptions.

---

## §10. Specialist roster

Five roles. Specialists write only into files they own (T3 §9); read is universal.

| Role | Owns | Deliverable | Prompt seed |
|------|------|-------------|-------------|
| **Solution Architect** | `architecture.md`, ADRs | `architecture.md`, ≥ 3 ADRs | "Given `02-requirements/{prd.en.md,nfr.md}` + `03-branding/brand-book.en.md`, propose a component architecture that satisfies every numeric NFR target. Produce `architecture.md` per T9 §2 and one ADR per significant choice per T9 §4." |
| **Data Architect** | `data-model.md` | `data-model.md` | "Given the PRD entities and `nfr.md` Localization rows, draft `data-model.md` per T9 §5. Tag every personal-data column `-- PII: <category>`; populate §5.4 — do not invent PDPL lawful-basis text (T4-deferred)." |
| **Security Architect** | ADRs on auth, secrets, network trust boundaries; reviews `integrations.md` §3 | ≥ 1 ADR (auth) + ADR (secret handling) | "Given `nfr.md` Security rows and §8 KSA integrations, propose the auth + secret-management architecture as one or more ADRs per T9 §4. Cite NCA ECC controls by number where applicable." |
| **DevOps Engineer** | `deployment-topology.md`, ADRs on IaC / CI/CD | `deployment-topology.md` + ADRs | "Given the chosen region per §7.2 and DR targets from `nfr.md`, author `deployment-topology.md` per T9 §7. Justify the in-Kingdom presence; surface any cross-border exception as a T4 blocker." |
| **Cost Engineer** | `cost.md` | `cost.md` | "Given the stack ADRs and the deployment topology, produce `cost.md` per T9 §9. Cite every vendor-calculator URL with retrieval date. Use 1 USD = 3.75 SAR; apply KSA VAT 15% only to KSA-billed services. Reproduce §9.1 structure exactly." |

---

## §11. Strategic gate — `gate-4-to-5.json`

Stage 4 ends at a **strategic** gate per T2 §2. Engagement owner writes `gates/gate-4-to-5.json` (path per T3 §3) with `decision_kind: "strategic"`. Approvers: engagement owner (NEXOURA partner) **and** client sponsor — both required. This gate approves architecture **and** budget; a downstream Stage 5 launch cannot recover from an unapproved cost envelope.

### 11.1 Gate fields specific to Stage 4

- `decision_kind`: `"strategic"`. `from_stage`: `"04-tech"` → `to_stage`: `"05-gtm"`.
- `artifacts_reviewed`: all six §2 paths, with `adrs/` enumerated file-by-file.
- `approvers_required`: `["engagement_owner", "client_sponsor"]`.
- **Rejection paths.** `REVISE → next_action: "rescope_cost"` (cost over envelope; cut features or change region/SKUs). `REVISE → next_action: "re-adr"` (a specific ADR is rejected; rerun §3 for that slot). `REVISE → next_action: "integration_descope"` (a KSA surface lift is too costly for v1; defer with a documented trigger). `NO-GO` — rare; usually signals the NFR catalogue was wrong (route back to T7).

### 11.2 Example payload (full schema in T2 §3)

```json
{
  "request_id": "b4e7c2a1-9d8f-4e3b-a5c6-1f2d8e9a0b3c",
  "status": "pending",
  "decision_kind": "strategic",
  "from_stage": "04-tech",
  "to_stage": "05-gtm",
  "approvers_required": ["engagement_owner", "client_sponsor"],
  "approver": "omar@nexoura.ai",
  "decision": "GO",
  "channel": "cli-clarify",
  "timestamp": "2026-08-19T13:00:00Z",
  "rationale": "Architecture meets every NFR target; 7 ADRs accepted; data model tags PII for T4 backfill; ZATCA + Nafath + Wathq integrations scoped with sandbox URLs and auth models; deployment in STC Cloud Riyadh + Jeddah satisfies KSA residency; monthly cost 14,200 SAR (3,787 USD) within Stage 1 envelope; DR RTO 4h / RPO 1h confirmed.",
  "artifacts_reviewed": [
    "04-tech/architecture.md", "04-tech/data-model.md",
    "04-tech/integrations.md", "04-tech/deployment-topology.md",
    "04-tech/cost.md",
    "04-tech/adrs/0001-choose-typescript-node-runtime.md",
    "04-tech/adrs/0002-choose-postgres-primary-datastore.md",
    "04-tech/adrs/0003-nafath-for-ksa-resident-iam.md"
  ],
  "conditions": [], "next_action": null
}
```

### 11.3 Bilingual approval prompt (Stage 4 instantiation of T2 §7.1)

English:

```text
GATE REQUEST — <slug>
Stage transition: 04-tech → 05-gtm

Artifacts: 04-tech/{architecture.md, data-model.md, integrations.md,
deployment-topology.md, cost.md, adrs/*.md}

Summary: Architecture satisfies every NFR target; <N> ADRs accepted with
alternatives documented; data model tags PII columns for T4 backfill;
KSA integrations scoped (ZATCA / Fasah / Nafath / Wathq as applicable)
with sandbox URLs and auth models; deployment in <chosen KSA presence>
satisfies in-Kingdom residency; monthly cost <SAR> (<USD>); DR targets
RTO <H>h / RPO <H>h. Build kickoff deferred to v2 — this gate approves
design + budget only.

Reply: GO | NO-GO | REVISE — plus a one-sentence rationale.
```

Arabic (KSA-formal register):

```text
طلب اعتماد بوابة — <slug>
الانتقال بين المراحل: 04-tech ← 05-gtm

المخرجات: 04-tech/{architecture.md, data-model.md, integrations.md,
deployment-topology.md, cost.md, adrs/*.md}

ملخّص تنفيذي: تستوفي العمارة المقترَحة جميعَ أهداف المتطلّبات غير
الوظيفيّة؛ اعتُمد <N> من سجلات قرارات العمارة (ADRs) مع توثيق البدائل؛
يُعلِّم نموذج البيانات حقولَ البيانات الشخصيّة تمهيداً لإكمال T4؛
حُدِّدت تكامُلات الجهات السعوديّة (هيئة الزكاة والضريبة والجمارك ZATCA،
فسح، نفاذ، واثق) بروابط بيئات الاختبار ونماذج المصادقة؛ يستوفي
الاستضافة في <المنطقة السعوديّة المختارة> اشتراطَ إقامة البيانات داخل
المملكة؛ التكلفة الشهريّة <ريال> (<USD>)؛ أهداف التعافي من الكوارث:
زمن الاستعادة <س> ساعة، زمن فقد البيانات <س> ساعة. يُؤجَّل البدء
بالتنفيذ إلى الإصدار الثاني — تَعتمِد هذه البوابة التصميمَ والموازنةَ
دون التنفيذ.

يُرجى الإفادة: GO | NO-GO | REVISE — مع مسوّغ مختصر في سطر مستقل.
```

Commit per T3 §8: `gate: stage4 → stage5 APPROVED` (or `REVISE` / `BLOCKED`).

---

## §12. Output artifacts summary

All paths root-relative to the engagement repo (T3 §4). Stage is artifact-complete when:

| Path | Owner | Completeness check |
|------|-------|--------------------|
| `04-tech/architecture.md` | Solution Architect | Every `nfr.md` numeric row appears in the NFR coverage matrix |
| `04-tech/adrs/NNNN-*.md` | Solution Architect + co-author | ≥ 3 ADRs; each has §1–§5 per §4.1; counter monotonic from 0001 |
| `04-tech/data-model.md` | Data Architect | Every PII column tagged `PII: <category>`; §5.4 populated |
| `04-tech/integrations.md` | Solution Architect | Every relevant KSA surface present with sandbox URL placeholder + auth + pattern; non-applicable surfaces explicitly justified |
| `04-tech/deployment-topology.md` | DevOps Engineer | Region cites a named KSA presence; RTO/RPO numeric; any cross-border flow flagged for T4 |
| `04-tech/cost.md` | Cost Engineer | Every row source-cited; totals in SAR + USD; §7 Sensitivity populated |
| `gates/gate-4-to-5.json` | Engagement owner | Parses; `decision_kind: "strategic"`; `artifacts_reviewed` enumerates the six above plus the ADRs |

---

## §13. Cross-references

- **T1 nexoura-engagement-lifecycle** §3 (Stage 4 stub this skill expands), §6 (artifact layout — superseded by T3).
- **T2 nexoura-gate-protocol** §3 (gate schema, `decision_kind: "strategic"`), §4 (advance / reject / revise), §7.1 (bilingual strategic prompt; §11.3 is the Stage-4 instantiation).
- **T3 nexoura-artifact-conventions** §3 (`gates/gate-4-to-5.json` canonical path), §4 (per-stage artifact table), §5 (ADR `NNNN-<slug>.md` filename rule), §8 (`stage4: …` / `gate: stage4 → stage5 …` commits), §9 (T9 owns `04-tech/` exclusively).
- **T7 nexoura-requirements-stage** — NFR catalogue this architecture must satisfy. Every numeric target in T7 §4 (Performance / Security / Scalability / Availability / Accessibility / Observability / Localization) lands in `architecture.md` §5 NFR coverage matrix.
- **T8 nexoura-branding-stage** — palette tokens, type pairing, and the chosen product name flow into UI-scaffolding ADRs (frontend framework, design-token strategy).
- **T10 nexoura-gtm-marketing** (forthcoming) — consumes `cost.md` for pricing floor and `architecture.md` for the capability narrative.
- **T11 nexoura-operations** (forthcoming) — consumes `deployment-topology.md` (DR, region) and `integrations.md` (vendor on-call surfaces) for the runbook.
- **T4 nexoura-pdpl-compliance** (deferred) — DPIA template, lawful-basis matrix, cross-border-transfer decision tree. T9 surfaces every PDPL touchpoint (PII tags in `data-model.md` §5.4; residency rationale in `deployment-topology.md` §7.2; consent timestamps in `integrations.md` §8.5) so T4 can backfill substance without re-architecting. **Do not fabricate PDPL templates in this stage.**
