# NEXOURA Studio — Phase 1 Kanban Spec

**Status:** Draft, awaiting builder profile creation.
**Author:** product-director (running on default Hermes profile, session of project kickoff).
**Purpose:** Specification for the 11 Kanban cards that will be created once the `builder` profile is formalized. Each card produces one SKILL.md under `~/.hermes/skills/` for the NEXOURA engagement lifecycle.

---

## Architecture decisions locked in this spec

- **Engagement state location (v1):** `~/.hermes/nexoura/engagements/<slug>/`. Each engagement is git-versioned — the engagement directory IS a git repo (mono-repo vs. per-engagement-repo TBD later, does not affect v1 skill authoring).
- **Stages in v1:** 6 (feasibility, requirements, branding, tech-architecture, gtm-marketing, operations). **No implementation stage in v1** — added to v2 candidate list below.
- **Foundation skills are referenced by stage skills** via `metadata.hermes.related_skills`, keeping each stage skill in the 8–15k char peer range.
- **All skills follow `hermes-agent-skill-authoring` conventions:** frontmatter with `name`, `description` (≤1024 chars, starts with "Use when ..."), `version`, `author`, `license`, `metadata.hermes.{tags, related_skills}`. Total file ≤100k chars.

---

## Dependency graph

```
Foundation (no parents, parallel):
  T1 nexoura-engagement-lifecycle
  T2 nexoura-gate-protocol
  T3 nexoura-artifact-conventions
  T4 nexoura-pdpl-compliance
  T5 nexoura-bilingual-content

Stage (gated on foundation):
  T6  nexoura-feasibility         parents: [T1, T2, T3]
  T7  nexoura-requirements        parents: [T1, T2, T3, T4, T5]
  T8  nexoura-branding            parents: [T1, T2, T3, T5]
  T9  nexoura-tech-architecture   parents: [T1, T2, T3, T4]
  T10 nexoura-gtm-marketing       parents: [T1, T2, T3, T5]
  T11 nexoura-operations          parents: [T1, T2, T3, T4]
```

All 11 cards assigned to `builder` (placeholder — profile does not yet exist). Same-profile queue → dispatcher serializes; the parent links enforce read-order, not parallelism.

---

## LANE A — FOUNDATION SKILLS

### T1 — nexoura-engagement-lifecycle

- **Card ID:** T1
- **Title:** `nexoura-engagement-lifecycle`
- **Description:** The map for every NEXOURA engagement. Names the 6 stages in order, the gate between each, the artifact contract, and the on-disk engagement directory layout. Every stage skill cross-links back to this one as the source of truth for stage order and handoff format.
- **Trigger phrases:**
  - "start a NEXOURA engagement"
  - "new client project"
  - "list NEXOURA stages"
  - "what stage is `<engagement>` in"
- **Inputs / parents:** none (foundation).
- **Artifacts produced (by following the skill):**
  - Engagement scaffold directory at `~/.hermes/nexoura/engagements/<slug>/`
  - `manifest.json` with fields: `slug`, `client`, `owner`, `created_at`, `current_stage`, `gate_history[]`
  - Per-stage subdirectories (empty placeholders): `01-feasibility/`, `02-requirements/`, `03-branding/`, `04-tech/`, `05-gtm/`, `06-operations/`
  - Initial `.gitignore` and `README.md` for the engagement repo
- **Gate type:** none (this skill itself doesn't gate; it defines what gates exist).
- **Assignee:** builder
- **Acceptance criteria:** A new operator can invoke any trigger phrase, follow the skill's numbered steps, and end up with a valid engagement directory + manifest. Manifest schema is documented in the skill body.

---

### T2 — nexoura-gate-protocol

- **Card ID:** T2
- **Title:** `nexoura-gate-protocol`
- **Description:** Defines how strategic and operational gates work end-to-end — the request payload format, the approval channel (CLI `clarify` for v1; Kanban card for async; gateway message for remote approval), what an approval/rejection writes back to `gate.json`, and how rejection routes work back to the prior stage.
- **Trigger phrases:**
  - "request gate approval"
  - "advance NEXOURA stage"
  - "block on human decision"
- **Inputs / parents:** none (foundation).
- **Artifacts produced:**
  - `gate.json` schema spec (status: `pending|approved|rejected`, approver, decision, timestamp, rationale, next_action)
  - Decision audit trail format (append-only `gate.log.jsonl` per engagement)
  - Template strings for gate-request prompts (bilingual: AR + EN)
- **Gate type:** none.
- **Assignee:** builder
- **Acceptance criteria:** Any stage skill can call into this protocol with a single procedure call. Rejected gates produce a clear route-back path with rationale captured. Audit trail is reconstructible from `gate.log.jsonl` alone.

---

### T3 — nexoura-artifact-conventions

- **Card ID:** T3
- **Title:** `nexoura-artifact-conventions`
- **Description:** The filesystem and naming contract for everything a NEXOURA engagement produces. Directory layout, filename conventions, versioning policy (vN suffix vs. git history), bilingual file naming (`*.ar.md` / `*.en.md`), what gets committed vs. gitignored. Every stage skill defers to this for output paths.
- **Trigger phrases:**
  - "where do NEXOURA artifacts go"
  - "save engagement deliverable"
  - "name a NEXOURA file"
- **Inputs / parents:** none (foundation).
- **Artifacts produced:**
  - Directory-layout reference table (stage → subpath → expected files)
  - Naming-convention cheatsheet
  - `templates/.gitignore` for engagement repos
  - `templates/README.md` skeleton for engagement repos
- **Gate type:** none.
- **Assignee:** builder
- **Acceptance criteria:** Two different operators producing the same artifact land on identical file paths. No stage skill duplicates path logic — they all reference back to T3.

---

### T4 — nexoura-pdpl-compliance

- **Card ID:** T4
- **Title:** `nexoura-pdpl-compliance`
- **Description:** KSA Personal Data Protection Law (PDPL) guardrails referenced by requirements, tech-architecture, and operations stages. Lawful-basis matrix, data-subject-rights checklist, cross-border transfer rules, SDAIA/NDMO touch points, the 72-hour breach notification SLA.
- **Trigger phrases:**
  - "PDPL check"
  - "data residency"
  - "personal data flow"
  - "SDAIA / NDMO compliance"
- **Inputs / parents:** none (foundation).
- **Artifacts produced:**
  - `pdpl-assessment.md` template (lawful basis per data category, processor/controller mapping, retention)
  - DPIA worksheet (Data Protection Impact Assessment) template
  - Cross-border transfer decision tree
  - Breach-response checklist with 72-hour SLA timeline
- **Gate type:** none (advisory cross-cutting; gates that USE it live in stages).
- **Assignee:** builder
- **Acceptance criteria:** Requirements (T7), tech (T9), and operations (T11) stages can complete their PDPL-touching artifacts without re-deriving the law — they fill in the templates and follow the decision tree from T4.

---

### T5 — nexoura-bilingual-content

- **Card ID:** T5
- **Title:** `nexoura-bilingual-content`
- **Description:** Arabic-first authoring rules referenced by branding, requirements (UI copy), and gtm-marketing. Terminology glossary policy, RTL/LTR mixing rules, when to translate vs. localize, formality register for KSA enterprise audience.
- **Trigger phrases:**
  - "Arabic-first output"
  - "bilingual deliverable"
  - "RTL layout review"
- **Inputs / parents:** none (foundation).
- **Artifacts produced:**
  - `terminology-glossary.csv` template (term_en, term_ar, register, notes)
  - RTL/LTR mixing rules cheatsheet
  - Translate-vs-localize decision matrix
- **Gate type:** none.
- **Assignee:** builder
- **Acceptance criteria:** Any AR/EN deliverable produced by a stage skill is consistent in terminology and register because every author reads T5 first and updates the glossary.

---

## LANE B — STAGE SKILLS

### T6 — nexoura-feasibility (Stage 1)

- **Card ID:** T6
- **Title:** `nexoura-feasibility`
- **Description:** Stage 1 of a NEXOURA engagement. Drives the feasibility study from problem statement through go/no-go memo. Covers market sizing, competitor scan, buyer interview outline, simple economics model, and strategic-fit reasoning. Ends at a strategic gate.
- **Trigger phrases:**
  - "feasibility study for `<X>`"
  - "is `<X>` worth building"
  - "kick off NEXOURA stage 1"
- **Inputs / parents:** engagement `manifest.json` with client + problem statement. Card parents: [T1, T2, T3].
- **Artifacts produced (under `01-feasibility/`):**
  - `feasibility-memo.en.md`
  - `feasibility-memo.ar.md`
  - `market-map.csv`
  - `competitors.md`
  - `economics.csv` (TAM/SAM/SOM, unit economics)
  - `go-no-go.json` (decision, rationale, approver)
- **Gate type:** **STRATEGIC** — human approves go/no-go before any stage 2 work.
- **Assignee:** builder
- **Acceptance criteria:** Following the skill on the APT WATCH supply-chain SaaS pilot would produce a memo a partner could read and sign in one sitting; the gate payload is unambiguous (binary go/no-go + rationale).

---

### T7 — nexoura-requirements (Stage 2)

- **Card ID:** T7
- **Title:** `nexoura-requirements`
- **Description:** Stage 2. Captures functional and non-functional requirements, including a PDPL assessment (via T4) and bilingual UI copy considerations (via T5). Produces a PRD, NFR doc, acceptance criteria, and a wireframe spec stub.
- **Trigger phrases:**
  - "draft PRD for `<engagement>`"
  - "requirements capture"
  - "NEXOURA stage 2"
- **Inputs / parents:** signed `feasibility-memo` + `go-no-go.json` with `decision=GO`. Card parents: [T1, T2, T3, T4, T5].
- **Artifacts produced (under `02-requirements/`):**
  - `prd.en.md`, `prd.ar.md`
  - `nfr.md` (performance, security, availability, compliance summary)
  - `pdpl-assessment.md` (filled from T4 template)
  - `acceptance-criteria.md`
  - `wireframe-spec.md` (text spec of key screens; visual wireframes out of scope for v1)
- **Gate type:** **STRATEGIC** — scope and budget envelope approved before stage 3.
- **Assignee:** builder
- **Acceptance criteria:** Acceptance criteria are testable (every line maps to a verifiable outcome). PDPL assessment identifies every personal-data flow before tech stage begins.

---

### T8 — nexoura-branding (Stage 3)

- **Card ID:** T8
- **Title:** `nexoura-branding`
- **Description:** Stage 3. Naming exploration (AR + EN), positioning statement, visual direction brief, logo concept spec (text-level — no image generation in v1), and voice/tone guide. PDPL not relevant; bilingual rules (T5) load-bearing.
- **Trigger phrases:**
  - "branding for `<engagement>`"
  - "name candidates"
  - "NEXOURA stage 3"
- **Inputs / parents:** `prd.{en,ar}.md` + target persona section. Card parents: [T1, T2, T3, T5].
- **Artifacts produced (under `03-branding/`):**
  - `brand-book.en.md`, `brand-book.ar.md`
  - `naming-shortlist.md` (≥5 candidates, AR + EN, trademark sanity-check notes)
  - `positioning.md`
  - `voice-tone.md`
- **Gate type:** **STRATEGIC** — name and identity locked before tech build commits to it.
- **Assignee:** builder
- **Acceptance criteria:** Naming shortlist includes at least one candidate that works in both AR and EN markets. Voice/tone guide has concrete do/don't examples in both languages.

---

### T9 — nexoura-tech-architecture (Stage 4)

- **Card ID:** T9
- **Title:** `nexoura-tech-architecture`
- **Description:** Stage 4. Stack selection, Architecture Decision Records, data model, integration surface (KSA-specific: ZATCA, Fasah, Nafath, Absher as applicable), deployment topology with data-residency constraints from T4, and a cost estimate. Implementation itself is out of scope in v1.
- **Trigger phrases:**
  - "architect `<engagement>`"
  - "tech stack selection"
  - "NEXOURA stage 4"
- **Inputs / parents:** `prd.{en,ar}.md` + `nfr.md` + `pdpl-assessment.md`. Card parents: [T1, T2, T3, T4].
- **Artifacts produced (under `04-tech/`):**
  - `architecture.md` (system context, components, data flow)
  - `adrs/0001-*.md`, `adrs/0002-*.md`, ... (one ADR per significant choice)
  - `data-model.md`
  - `integrations.md` (third-party + KSA gov surfaces)
  - `deployment-topology.md` (regions, residency, network)
  - `cost.md` (monthly + annual, SAR + USD)
- **Gate type:** **STRATEGIC** — architecture and budget approved. (Implementation is a v2 stage; this gate effectively defers build kickoff.)
- **Assignee:** builder
- **Acceptance criteria:** Every ADR has context, decision, consequences. Cost estimate is reproducible (sources cited). Integrations doc names the KSA-specific surfaces explicitly when applicable.

---

### T10 — nexoura-gtm-marketing (Stage 5)

- **Card ID:** T10
- **Title:** `nexoura-gtm-marketing`
- **Description:** Stage 5. ICP refinement, channel plan (enterprise vs. SMB, KSA-specific channels), pricing in SAR with 15% VAT, launch sequence, and content calendar stub. Bilingual content rules (T5) apply throughout.
- **Trigger phrases:**
  - "GTM plan for `<engagement>`"
  - "marketing strategy"
  - "NEXOURA stage 5"
- **Inputs / parents:** `brand-book.{en,ar}.md` + `prd` + `cost.md`. Card parents: [T1, T2, T3, T5].
- **Artifacts produced (under `05-gtm/`):**
  - `gtm-plan.en.md`, `gtm-plan.ar.md`
  - `pricing.md` (tiers, SAR, VAT-inclusive vs. exclusive, annual vs. monthly)
  - `channels.md`
  - `launch-plan.md` (T-minus calendar)
- **Gate type:** **STRATEGIC** — pricing and launch date approved.
- **Assignee:** builder
- **Acceptance criteria:** Pricing reconciles with cost.md (gross margin shown). Launch plan has explicit owners per milestone.

---

### T11 — nexoura-operations (Stage 6)

- **Card ID:** T11
- **Title:** `nexoura-operations`
- **Description:** Stage 6. SLA definition, on-call / support tiers, customer onboarding flow, billing operations (SAR + VAT invoicing), incident response with PDPL breach-notification SLA (via T4), and a KPI dashboard spec.
- **Trigger phrases:**
  - "ops runbook for `<engagement>`"
  - "onboarding plan"
  - "NEXOURA stage 6"
- **Inputs / parents:** `architecture.md` + `gtm-plan.{en,ar}.md`. Card parents: [T1, T2, T3, T4].
- **Artifacts produced (under `06-operations/`):**
  - `runbook.md`
  - `sla.md`
  - `onboarding.md`
  - `billing-ops.md`
  - `incident-response.md` (includes 72-hour PDPL breach path from T4)
  - `kpis.md`
- **Gate type:** **OPERATIONAL** — readiness review before public launch.
- **Assignee:** builder
- **Acceptance criteria:** Runbook is executable by an operator who was not in the engagement. Incident-response plan covers the PDPL 72-hour SLA without referring back to T4 at incident time.

---

## v2 candidate skills (not in this round)

- **`nexoura-implementation`** — sits between T9 (tech-architecture) and T10 (gtm-marketing) in v2. Drives the actual build: scaffolding, sprint cadence, code review gates, QA. Deliberately deferred from v1 so the upstream stages prove out first against the APT WATCH pilot before we commit to a build workflow.
- **`nexoura-discovery-intake`** — pre-stage-1 client intake (problem framing, stakeholder map) that today is implicit in T6's inputs. Promote if intake quality varies engagement-to-engagement.
- **`nexoura-engagement-retrospective`** — post-stage-6 retrospective skill that feeds learnings back into the lifecycle skills themselves. Closes the loop.

---

## Skills to pre-load for the product-director profile (when formalized)

When the product-director profile is created, configure auto-load of these in addition to whatever the schema-loader brings in by trigger:

**Already loaded by context in this session (keep):**
- `kanban-orchestrator` — the routing playbook; required for the role.
- `hermes-agent-skill-authoring` — needed whenever product-director patches a stage skill or commissions a new one.

**Recommended additions (community / built-in):**
- `writing-plans` — bite-sized implementation plans with paths and code references. Maps cleanly to how product-director hands work to the builder.
- `plan` — Plan-mode skill that writes a markdown plan to `.hermes/plans/` without executing. Useful when an engagement needs a multi-stage plan artifact before any gate fires.
- `spike` — throwaway experiments to de-risk a stage before committing. Particularly relevant for tech-architecture (T9) decisions.
- `subagent-driven-development` — two-stage delegate/review pattern. Product-director uses `delegate_task` to spawn focused subagents for in-stage research without flooding orchestrator context.
- `ideation` — generate options via creative constraints. Direct fit for branding (T8) naming exploration and gtm (T10) channel brainstorming.
- `codebase-inspection` — useful when stage 4 (tech-architecture) needs to scope a refactor or audit a candidate codebase.
- `github-issues` — for any external commitment tracking once an engagement leaves NEXOURA and lives in a client/internal repo.

**Gaps (no community skill exists; candidates to author later):**
- A `decision-frameworks` skill (RICE, MoSCoW, weighted-shortest-job-first, RACI selection) — currently no equivalent in the available skill set. Worth authoring as a foundation skill in a future round.
- A `strategic-planning` skill (OKR cascade, Wardley mapping, SWOT) — also absent. Same recommendation: author later.

---

## Next steps (out of scope for this card-creation pass)

1. Formalize the `product-director` and `builder` profiles via `hermes profile create`. Configure auto-loaded skills per the list above.
2. Once `builder` exists, create the 11 Kanban cards from this spec with the dependency graph as defined. Each card body can quote directly from the matching section of this file.
3. Builder works the foundation lane first (T1–T5) in priority order, then the stage lane (T6–T11).
4. Run the APT WATCH supply-chain SaaS engagement as the first real use of the lifecycle. Patch any stage skill that fails to handle the pilot cleanly before declaring v1 stable.
