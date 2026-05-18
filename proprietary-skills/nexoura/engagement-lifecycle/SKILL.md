---
name: nexoura-engagement-lifecycle
description: Use when starting a new NEXOURA client engagement, kicking off a new client project, listing the NEXOURA stages, checking what stage an engagement is in, scaffolding the engagement directory, advancing between stages, or when any sibling NEXOURA stage skill needs to look up the canonical stage order, gate model, manifest schema, or on-disk artifact layout. This is the T1 foundation skill that every NEXOURA stage skill (feasibility, requirements, branding, tech-architecture, gtm-marketing, operations) cross-links to as the source of truth for engagement state and handoff format.
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, lifecycle, engagement, platform-foundation]
    related_skills:
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-pdpl-compliance
      - nexoura-bilingual-content
---

# NEXOURA Engagement Lifecycle (T1 — Foundation)

The map for every NEXOURA engagement. Source of truth for: the 6 stages in order, the gate between each, the engagement-as-own-repo architecture, the `manifest.json` schema, and the on-disk directory layout. Every stage skill (T6–T11) cross-links back here. When in doubt about stage order, handoff format, or where an artifact belongs on disk, this skill wins.

---

## 1. Trigger phrases

Load this skill when the operator says any of:

- "start a NEXOURA engagement"
- "new client project" / "kick off a new client"
- "list NEXOURA stages" / "what are the NEXOURA stages"
- "what stage is `<engagement>` in"
- "advance `<engagement>` to the next stage"
- "show engagement manifest" / "where does the engagement live"
- "scaffold engagement directory"
- "how do NEXOURA gates work" (until T2 lands — then defer to T2)
- "where do NEXOURA artifacts go" (until T3 lands — then defer to T3)

If a sibling foundation skill (T2 gate-protocol, T3 artifact-conventions, T4 PDPL, T5 bilingual) is loaded and the question is squarely in its domain, defer to it. This skill carries inline stubs for those four so the foundation is usable today; the sibling skills supersede the stubs as soon as they exist.

---

## 2. What is a NEXOURA engagement

A NEXOURA engagement is a single client project that moves through 6 sequential stages, each ending in a human-approved gate. Engagements are run by NEXOURA AI (the APT WATCH-incubated studio) under a strategic-fit model derived from the v1.3 platform specification: multi-LLM-routed (§11), plugin-extensible (§13), PDPL-compliant (§29), and Arabic-first bilingual (§15).

### Engagement-as-own-repo architecture

Each engagement is its own git repository at:

```
~/.hermes/nexoura/engagements/<slug>/
```

Rationale: full audit trail (`git log` is the engagement timeline), isolation (one engagement failing does not corrupt another), portability (zip and hand off; mirror to a client repo), reproducibility (a fresh operator clones, reads `manifest.json` + `README.md`, picks up where the prior operator stopped).

The `<slug>` is kebab-case, derived from client + product (e.g. `apt-watch-supply-chain-saas`). One slug, one repo, one engagement, forever.

### `manifest.json` schema

The manifest is the engagement's machine-readable state header, at the repo root.

```json
{
  "slug": "apt-watch-supply-chain-saas",
  "client": "APT WATCH",
  "owner": "omar@nexoura.ai",
  "created_at": "2026-05-19T10:00:00Z",
  "current_stage": "01-feasibility",
  "gate_history": [
    {
      "from_stage": "01-feasibility",
      "to_stage": "02-requirements",
      "status": "approved",
      "approver": "omar@nexoura.ai",
      "decision": "GO",
      "rationale": "TAM defensible, unit economics clear.",
      "timestamp": "2026-05-22T14:30:00Z"
    }
  ]
}
```

Field contract:

- `slug` — kebab-case, immutable, matches directory name.
- `client` — human-readable client name (free-form, may be bilingual).
- `owner` — single accountable operator email. One throat to choke per engagement.
- `created_at` — ISO-8601 UTC, set once at scaffold time.
- `current_stage` — exactly one of the six stage directory names (`01-feasibility` ... `06-operations`).
- `gate_history` — append-only array. Each entry records one gate decision. Rejections too (`status: rejected`, `next_action` populated). Never delete entries — that is what `git revert` is for.

Stage skills read `current_stage` to know whether they are allowed to run. The gate-protocol skill (T2) updates `current_stage` and appends to `gate_history` atomically on gate approval.

---

## 3. The 6 stages (overview)

Each stage ends in a gate. No stage may begin until the prior gate is `approved`. Rejections route back to the prior stage with `next_action` rationale.

**Stage 1 — Feasibility (`01-feasibility/`).** Problem statement to go/no-go memo. Market sizing, competitor scan, buyer interview outline, simple economics (TAM/SAM/SOM), strategic-fit reasoning. Artifacts: `feasibility-memo.{en,ar}.md`, `market-map.csv`, `competitors.md`, `economics.csv`, `go-no-go.json`. Ends in a STRATEGIC gate (binary go/no-go, signed by partner).

**Stage 2 — Requirements (`02-requirements/`).** Functional + non-functional requirements. Pulls in PDPL assessment (T4) and bilingual UI copy considerations (T5). Artifacts: `prd.{en,ar}.md`, `nfr.md`, `pdpl-assessment.md`, `acceptance-criteria.md`, `wireframe-spec.md`. Ends in a STRATEGIC gate (scope + budget envelope locked).

**Stage 3 — Branding (`03-branding/`).** Naming (AR + EN, ≥5 candidates with trademark sanity check), positioning, voice/tone with bilingual do/don't examples, brand book. Bilingual rules (T5) load-bearing. Artifacts: `brand-book.{en,ar}.md`, `naming-shortlist.md`, `positioning.md`, `voice-tone.md`. Ends in a STRATEGIC gate (name and identity locked before tech commits).

**Stage 4 — Tech Architecture (`04-tech/`).** Stack selection, Architecture Decision Records, data model, integration surface (KSA-specific surfaces — ZATCA, Fasah, Nafath, Absher — where applicable), deployment topology under PDPL data-residency constraints (T4), cost estimate in SAR + USD. Implementation itself is out of scope in v1. Artifacts: `architecture.md`, `adrs/000N-*.md`, `data-model.md`, `integrations.md`, `deployment-topology.md`, `cost.md`. Ends in a STRATEGIC gate (architecture + budget approved; build kickoff deferred to v2).

**Stage 5 — GTM / Marketing (`05-gtm/`).** ICP refinement, channel plan (KSA enterprise + SMB), pricing in SAR with 15% VAT treatment, launch sequence (T-minus calendar), content calendar stub. Bilingual content rules (T5) apply. Artifacts: `gtm-plan.{en,ar}.md`, `pricing.md`, `channels.md`, `launch-plan.md`. Ends in a STRATEGIC gate (pricing + launch date approved; reconciles to `cost.md` from Stage 4).

**Stage 6 — Operations (`06-operations/`).** SLA, on-call / support tiers, customer onboarding, billing ops (SAR + VAT invoicing), incident response (includes the 72-hour PDPL breach SLA inlined from T4 so on-call need not re-derive it at incident time), KPI dashboard spec. Artifacts: `runbook.md`, `sla.md`, `onboarding.md`, `billing-ops.md`, `incident-response.md`, `kpis.md`. Ends in an OPERATIONAL gate (readiness review before public launch).

---

## 4. Engagement directory layout

A scaffolded engagement looks like this:

```
~/.hermes/nexoura/engagements/<slug>/
├── manifest.json              # machine-readable engagement state
├── gate.log.jsonl             # append-only audit trail of all gate decisions
├── README.md                  # human-readable engagement summary, populated by operator
├── .gitignore                 # excludes secrets, scratch, *.tmp, .DS_Store, node_modules, etc.
├── 01-feasibility/            # Stage 1 artifacts
├── 02-requirements/           # Stage 2 artifacts
├── 03-branding/               # Stage 3 artifacts
├── 04-tech/                   # Stage 4 artifacts
│   └── adrs/                  # one ADR per significant decision
├── 05-gtm/                    # Stage 5 artifacts
└── 06-operations/             # Stage 6 artifacts
```

Notes: stage directories are created empty at scaffold time (stage skills populate them); `gate.log.jsonl` is the canonical audit trail and `manifest.json:gate_history` mirrors it for fast reads (T2 keeps both in sync atomically); `README.md` is operator-owned, not auto-generated; the `.gitignore` template ships from T3 once that skill lands — until then use the defaults in §6.

---

## 5. Gate protocol (inline stub — T2 supersedes)

> **Note:** Stub. The full T2 `nexoura-gate-protocol` skill will replace this with the complete request payload format, bilingual prompt templates, and async-approval channel rules.

Every gate is a JSON file written into the closing stage's directory (e.g. `01-feasibility/gate.json`).

### `gate.json` schema

```json
{
  "status": "pending | approved | rejected",
  "from_stage": "01-feasibility",
  "to_stage": "02-requirements",
  "approver": "partner-email@nexoura.ai",
  "decision": "GO | NO-GO | REVISE",
  "timestamp": "2026-05-22T14:30:00Z",
  "rationale": "Free-text reasoning, ≥1 sentence.",
  "next_action": "Only populated when status=rejected. Describes the specific revision required before re-submission."
}
```

### Advance / reject flow

1. Stage skill finishes its artifacts and writes `gate.json` with `status: pending`.
2. Operator (or async approver via CLI `clarify` in v1) reviews the artifacts.
3. **On approval:** set `status: approved`, set `current_stage` in `manifest.json` to the new stage, append the entry to `manifest.json:gate_history` AND `gate.log.jsonl`, commit with `gate: <from> → <to> approved`.
4. **On rejection:** set `status: rejected`, populate `next_action`, append to log, leave `current_stage` unchanged. The stage skill re-runs with the rejection rationale as input.

`gate.log.jsonl` is append-only, one JSON object per line. The full gate history must be reconstructible from this file alone — `manifest.json:gate_history` is a convenience cache, not the truth.

---

## 6. Artifact conventions (inline stub — T3 supersedes)

> **Note:** Stub. T3 `nexoura-artifact-conventions` will replace this with the complete directory-layout reference table, naming cheatsheet, and `.gitignore` / `README.md` templates.

Until T3 lands, these inline rules are normative:

- **Bilingual file naming:** `<basename>.en.md` and `<basename>.ar.md`. Never embed both languages in one file. Pair files track 1:1 in section structure.
- **Versioning (v1):** use git history. Do NOT use `v1`/`v2` filename suffixes; that pattern is reserved for externally-published deliverables, not in-repo drafts.
- **CSV files:** UTF-8, header row required, comma-separated. Arabic text in cells is fine.
- **JSON files:** 2-space indent, trailing newline, sorted keys where order is not semantic.
- **`.gitignore` defaults:** `*.tmp`, `*.swp`, `.DS_Store`, `node_modules/`, `__pycache__/`, `.env`, `*.local.*`, `scratch/`.
- **Commit messages:** `stage<N>: <verb> <artifact>` (e.g. `stage1: add feasibility-memo.en.md`) or `gate: <from> → <to> <status>` for gate transitions.

Stage skills MUST write artifacts only inside their own stage directory. Cross-stage references go through `manifest.json` and the file paths agreed in T3, never via ad-hoc inclusion.

---

## 7. PDPL stub (T4 supersedes)

> **Note:** Stub. T4 `nexoura-pdpl-compliance` will provide the lawful-basis matrix, DPIA worksheet, cross-border transfer decision tree, and breach-response checklist.

Every NEXOURA engagement that touches personal data of KSA residents is in scope for the Personal Data Protection Law (PDPL), enforced by SDAIA. Three lifecycle touch points matter:

1. **Lawful basis.** Every personal-data flow identified in Stage 2 (`pdpl-assessment.md`) must name its lawful basis (consent, contract, legal obligation, vital interest, public interest, or legitimate interest). No flow ships without one.
2. **Data residency.** Stage 4 (`deployment-topology.md`) must explicitly state where personal data is stored and processed. Cross-border transfers require an adequacy decision, explicit consent, or a documented exception. Default to in-Kingdom hosting unless a documented exception applies.
3. **Breach response.** Stage 6 (`incident-response.md`) must encode the 72-hour SDAIA breach-notification SLA inline — on-call cannot be required to load T4 mid-incident. Notification path, contact, and template strings live in the runbook.

Platform spec §29 is the canonical reference; this stub captures only the lifecycle hooks.

---

## 8. Bilingual content stub (T5 supersedes)

> **Note:** Stub. T5 `nexoura-bilingual-content` will ship the terminology glossary template, RTL/LTR mixing cheatsheet, and translate-vs-localize decision matrix.

NEXOURA is Arabic-first for the KSA market, English-parallel for international stakeholders (platform spec §15). Until T5 lands: client-facing deliverables are Arabic-first (Arabic is authoritative, English is the parallel translation); internal artifacts (ADRs, runbooks) may be English-first. When embedding English technical terms inside Arabic prose, do not force LTR isolation marks by hand — let the renderer handle bidi; inline code (backticks) is always rendered LTR. Every engagement maintains a `terminology-glossary.csv` (template lands in T5); the glossary is updated, not bypassed, when a new term appears. Register: formal KSA enterprise register for client deliverables; informal acceptable for internal scratch. Files use `.en.md` / `.ar.md` suffixes per §6.

---

## 9. How to use this skill

### (a) Start a new engagement

Operator: "start a NEXOURA engagement for APT WATCH supply-chain SaaS":

1. Choose a slug: `apt-watch-supply-chain-saas`.
2. `mkdir -p ~/.hermes/nexoura/engagements/apt-watch-supply-chain-saas`.
3. `cd` in and `git init`.
4. Create the six stage subdirectories (`01-feasibility/` ... `06-operations/`), each with a `.gitkeep`.
5. Write `manifest.json` with `current_stage: "01-feasibility"`, `created_at` set to now (UTC ISO-8601), empty `gate_history: []`.
6. Write a starter `README.md` (one paragraph: client, problem, owner) and `.gitignore` (defaults from §6).
7. Create empty `gate.log.jsonl`.
8. Commit: `chore: scaffold engagement <slug>`.
9. Hand off to the T6 feasibility skill.

### (b) Advance a stage

Operator: "advance apt-watch-supply-chain-saas to requirements":

1. Verify `01-feasibility/gate.json` exists with `status: pending`.
2. Apply the §5 advance flow: set status to `approved`, update `manifest.json:current_stage` to `02-requirements`, append the entry to `gate_history` and `gate.log.jsonl`.
3. Commit: `gate: 01-feasibility → 02-requirements approved`.
4. Hand off to the T7 requirements skill.

### (c) List stages

Operator: "list NEXOURA stages" or "what stage is apt-watch in":

1. Print the canonical stage order from §3.
2. Read `manifest.json:current_stage` and `manifest.json:gate_history` to show progress.
3. For the current stage, list which artifacts (from §3) are present vs. missing in the stage directory.

### (d) Query engagement state

Operator: "show me the apt-watch engagement state":

1. Print `manifest.json` (pretty-formatted).
2. Print the last 5 entries of `gate.log.jsonl`.
3. Print the working-tree status (`git status --short`) of the engagement repo.
4. Surface uncommitted work with a reminder to commit before any gate transition.

---

When T2/T3/T4/T5 land, sections 5–8 of this file collapse to one-line pointers. The lifecycle definition (§§1–4, §9) is stable.
