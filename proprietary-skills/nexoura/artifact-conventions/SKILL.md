---
name: nexoura-artifact-conventions
description: "Use when answering 'where do NEXOURA artifacts go', 'save engagement deliverable', 'name a NEXOURA file', 'how do I structure an engagement repo', 'what goes in 01-feasibility / 02-requirements / 03-branding / 04-tech / 05-gtm / 06-operations', '.gitignore for engagement repo', 'NEXOURA commit message format', 'who owns this artifact', or 'bilingual filename convention' — T3 foundation skill that fixes the engagement repo directory layout, filenames, .gitignore, README template, commit grammars, and file-ownership rules; supersedes the §6 inline stub in T1 nexoura-engagement-lifecycle."
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, artifact-conventions, platform-foundation]
    related_skills: [nexoura-engagement-lifecycle, nexoura-gate-protocol]
---

# NEXOURA Artifact Conventions (T3)

Single source of truth for **where files live**, **what they are called**,
and **who owns them** inside a NEXOURA engagement repo. Stage skills (T6–T11)
and the gate skill (T2) MUST conform. Where this skill and the T1 §6 inline
stub disagree, **this skill wins**.

## §1. Trigger phrases

- "where do NEXOURA artifacts go"
- "save engagement deliverable"
- "name a NEXOURA file"
- "how do I structure an engagement repo"
- "what goes in 01-feasibility / 02-requirements / 03-branding / 04-tech / 05-gtm / 06-operations"
- ".gitignore for engagement repo"
- "NEXOURA commit message format"
- "who owns this artifact" / "bilingual filename convention" / "engagement README template"

## §2. Scope and authority

**This skill governs:** engagement repo directory layout (top-level and
per-stage); filenames, extensions, case, and language suffixes
(`.en.md` / `.ar.md`); the canonical `.gitignore`; the canonical `README.md`
skeleton; commit message grammars for stage work, gate transitions, manifest
bumps, and hygiene; file-ownership rules (which skill may write where).

**This skill does NOT govern:**

- The `gate.json` schema or gate state machine — see **T2 nexoura-gate-protocol** §3.
- The engagement lifecycle, stage definitions, or `manifest.json` schema — see **T1 nexoura-engagement-lifecycle**.
- PDPL legal substance or `pdpl-assessment.md` body format — see **T4 nexoura-pdpl-compliance** (when it lands).
- Bilingual AR/EN content quality, translation parity, RTL rendering — see **T5 nexoura-bilingual-content** (when it lands). T3 only governs the *filenames*.

**Conflict rule:** T1 §6 contains an inline directory-layout stub authored
before this skill existed. If anything in T1 §6 contradicts this document,
this document is authoritative and T1 §6 is superseded.

## §3. Engagement repo root layout

Every engagement repo MUST match this tree:

```
<engagement-slug>/
├── manifest.json           # Lifecycle state. Schema → T1. Owner: T1.
├── README.md               # Human-readable index. Template in §7. Owner: T1.
├── .gitignore              # Canonical ignore set. Template in §6. Owner: T3.
├── gates/                  # gate.json files, one per transition. Owner: T2.
├── 01-feasibility/         # Stage 1 deliverables. Owner: T6.
├── 02-requirements/        # Stage 2 deliverables. Owner: T7.
├── 03-branding/            # Stage 3 deliverables. Owner: T8.
├── 04-tech/                # Stage 4 deliverables. Owner: T9.
├── 05-gtm/                 # Stage 5 deliverables. Owner: T10.
├── 06-operations/          # Stage 6 deliverables. Owner: T11.
├── _assets/                # Shared images, diagrams, published snapshots. Shared write.
│   └── published/          # `vN`-suffixed external snapshots only. See §5.
└── scratch/                # Operator-local drafts. Gitignored. Never pushed.
```

No other top-level directories are permitted without first updating this skill
and the T1 lifecycle skill in lockstep.

## §4. Per-stage directory reference

| Stage | Dir | Owner skill | Required artifacts | Optional artifacts |
|-------|-----|-------------|--------------------|--------------------|
| 1 | `01-feasibility/` | T6 nexoura-feasibility | `feasibility-memo.en.md`, `feasibility-memo.ar.md`, `market-map.csv`, `competitors.md`, `economics.csv`, `go-no-go.json` | — |
| 2 | `02-requirements/` | T7 nexoura-requirements | `prd.en.md`, `prd.ar.md`, `nfr.md`, `pdpl-assessment.md`, `acceptance-criteria.md`, `wireframe-spec.md` | — |
| 3 | `03-branding/` | T8 nexoura-branding | `brand-book.en.md`, `brand-book.ar.md`, `naming-shortlist.md`, `positioning.md`, `voice-tone.md` | — |
| 4 | `04-tech/` | T9 nexoura-tech-architecture | `architecture.md`, `data-model.md`, `integrations.md`, `deployment-topology.md`, `cost.md` | `adrs/0001-*.md`, `adrs/0002-*.md`, … |
| 5 | `05-gtm/` | T10 nexoura-gtm-marketing | `gtm-plan.en.md`, `gtm-plan.ar.md`, `pricing.md`, `channels.md`, `launch-plan.md` | — |
| 6 | `06-operations/` | T11 nexoura-operations | `runbook.md`, `sla.md`, `onboarding.md`, `billing-ops.md`, `incident-response.md`, `kpis.md` | — |

A stage is **artifact-complete** when all "Required" files exist, are
non-empty, and (for bilingual pairs) have 1:1 section parity. T2 reads this
table when scoring a stage exit.

## §5. Naming cheatsheet

- **Bilingual files:** `<basename>.en.md` and `<basename>.ar.md`. Each
  language in its own file. **Never** mix AR and EN inside one file.
  Section count and order must match 1:1 between siblings.
- **Single-language files** (CSV, JSON, generic `.md` like `nfr.md`): no
  language suffix. Canonically bilingual files would be split.
- **Case and charset:** lowercase, kebab-case basenames. ASCII only in
  filenames (Arabic content **inside** files is welcome; Arabic in
  filenames breaks cross-platform tooling, shell history, and grep).
- **ADR files:** `04-tech/adrs/NNNN-short-title.md` where `NNNN` is a
  four-digit zero-padded monotonic counter starting at `0001`. Never reuse a
  number, never renumber on rebase.
- **Versioning — DO NOT** use `v1` / `v2` / `-final` suffixes for in-repo
  drafts; git history is the version log. The `vN` suffix is reserved
  **exclusively** for externally-published deliverables snapshotted into
  `_assets/published/` (e.g. `_assets/published/prd-v2.pdf` = the PRD as
  sent to the client, with the commit SHA recorded in the authorising gate).
- **CSV:** UTF-8 without BOM, header row required, comma-separated, RFC 4180
  quoting (`"`-quoted cells, doubled `""` to escape). Arabic cells are fine;
  the file is still ASCII-named.
- **JSON:** 2-space indent, trailing newline, UTF-8 without BOM. Keys sorted
  alphabetically where order carries no semantics (configuration objects);
  arrays and ordered records preserve insertion order.
- **Markdown:** ATX headings (`#`, `##`, …) — never Setext. Reference-style
  links allowed and encouraged for repeated URLs. Fenced code blocks MUST
  carry a language tag (` ```bash`, ` ```json`, ` ```gitignore`).
- **Cross-reference paths:** always relative to the engagement repo root
  (e.g. `02-requirements/prd.en.md`). Never absolute. Never `../`. Never
  symlinks. A document that needs to cite another stage's output cites it by
  repo-root-relative path so it survives clone, archive, and rename.

## §6. `.gitignore` template

Drop this verbatim into every new engagement repo. Owner: T3 (this skill).

```gitignore
# --- OS junk ---
.DS_Store
Thumbs.db
ehthumbs.db
desktop.ini

# --- Editor / IDE ---
*.swp
*.swo
*~
.vscode/
.idea/
*.sublime-workspace
*.sublime-project

# --- Python (analysis notebooks/scripts) ---
__pycache__/
*.pyc
.venv/
venv/
.ipynb_checkpoints/

# --- Node (JS prototypes) ---
node_modules/
npm-debug.log*
yarn-debug.log*

# --- Secrets / env ---
.env
.env.local
.env.*.local
*.local.*
*.pem
*.key

# --- Build / temp ---
*.tmp
*.bak
*.log
dist/
build/
out/

# --- Engagement-specific ---
scratch/
*.draft.md

# --- Large binaries ---
# Files >50MB MUST go through git-lfs (see _assets/published/).
# Track them with: git lfs track "*.pdf" "*.psd" "*.fig"
```

## §7. `README.md` template

Drop this verbatim into every new engagement repo and fill the placeholders.
Owner: T1 (lifecycle) — this skill just defines the skeleton.

```markdown
# <Engagement Title>

<One paragraph: the client problem in plain language. Who they are, what
they want, the constraint that makes this non-trivial. No marketing fluff,
no NEXOURA boilerplate. Two to five sentences.>

## Stage progress

- [ ] Stage 1 — Feasibility (`01-feasibility/`)
- [ ] Stage 2 — Requirements (`02-requirements/`)
- [ ] Stage 3 — Branding (`03-branding/`)
- [ ] Stage 4 — Tech architecture (`04-tech/`)
- [ ] Stage 5 — GTM & marketing (`05-gtm/`)
- [ ] Stage 6 — Operations (`06-operations/`)

Authoritative stage state lives in `manifest.json`. The checklist above is
a human cue and may lag by one commit.

## Artifacts

- `01-feasibility/` — feasibility memo, market map, competitors, unit economics, go/no-go.
- `02-requirements/` — PRD, NFRs, PDPL assessment, acceptance criteria, wireframe spec.
- `03-branding/` — brand book, naming shortlist, positioning, voice & tone.
- `04-tech/` — architecture, data model, integrations, deployment topology, cost, ADRs.
- `05-gtm/` — GTM plan, pricing, channels, launch plan.
- `06-operations/` — runbook, SLA, onboarding, billing ops, incident response, KPIs.

## Gates

Stage-exit gate decisions live in `gates/` as `gate-<N>-to-<N+1>.json`
files. The schema is defined in **T2 nexoura-gate-protocol §3**.

## How to run

<Operator instructions: which NEXOURA skills to invoke, in which order,
and any client-specific overrides. Default flow → T1.>

## Bilingual content

EN/AR parallel deliverables. Filename rules → **T3** §5; content quality
(translation parity, terminology, RTL) → **T5 nexoura-bilingual-content**.

## License

Proprietary — NEXOURA AI (APT WATCH). Not for redistribution.
```

## §8. Commit message conventions

Imperative mood, no trailing period, subject line ≤72 characters, optional
body separated by one blank line. Wrap the body at 72 characters.

- **Stage work** — `stage<N>: <verb> <artifact-or-scope>`
  - `stage1: add feasibility-memo.en.md`
  - `stage4: revise architecture.md per gate feedback`
  - `stage4: add adrs/0003-choose-postgres-over-mysql.md`
- **Gate transitions** — `gate: stage<N> → stage<N+1> <STATUS>` where
  `<STATUS>` is one of `APPROVED`, `REVISE`, `BLOCKED` (see T2 for the full
  state machine). Use the literal Unicode arrow `→`.
  - `gate: stage1 → stage2 APPROVED`
  - `gate: stage3 → stage3 REVISE`
  - `gate: stage2 → stage2 BLOCKED`
- **Manifest updates** — `manifest: <change>`
  - `manifest: bump stage=2 after gate 1 approved`
  - `manifest: record client sign-off timestamp for stage 3`
- **Repo hygiene** — `chore: <scope>`, `docs: <scope>`, `fix: <scope>`
  - `chore: tighten .gitignore for *.draft.md`
  - `docs: clarify README problem statement`
  - `fix: correct broken cross-ref in prd.en.md`

Commits that span multiple stages are forbidden — split them. Commits that
both bump the manifest and add stage content are forbidden — split them, and
land the stage content first.

## §9. File ownership rules

| Path | Owner skill | Write access |
|------|-------------|--------------|
| `manifest.json` | T1 nexoura-engagement-lifecycle | T1 only |
| `README.md` | T1 | T1 only |
| `.gitignore` | T3 (this skill) | T3 only |
| `gates/` | T2 nexoura-gate-protocol | T2 only |
| `01-feasibility/` | T6 | T6 only |
| `02-requirements/` | T7 | T7 only |
| `03-branding/` | T8 | T8 only |
| `04-tech/` | T9 | T9 only |
| `05-gtm/` | T10 | T10 only |
| `06-operations/` | T11 | T11 only |
| `_assets/` | shared | any stage |
| `scratch/` | operator-local | operator (gitignored) |

Read access is universal — every skill may read any file.

**Cross-stage rule:** if Stage N needs Stage M's output, it **reads** that
file at its canonical path (e.g. T9 reads `02-requirements/nfr.md` to build
`04-tech/architecture.md`). It does **NOT** copy that content into its own
stage directory, and it does **NOT** write into Stage M's directory. Cite by
relative path; don't duplicate.

Ownership violations are caught by T2 at stage exit: any commit touching a
foreign stage directory without a matching gate authorisation fails the gate.

## §10. Verification recipes

Inspect the top-level layout:

```bash
tree -L 2 -a engagement-repo/
```

Confirm every required artifact for the **current** stage exists. The loop
reads `manifest.json`, looks up the stage's required files, and prints
`OK` / `MISSING` per file:

```bash
#!/usr/bin/env bash
set -euo pipefail
stage=$(jq -r .stage manifest.json)
case "$stage" in
  1) dir=01-feasibility;  req="feasibility-memo.en.md feasibility-memo.ar.md market-map.csv competitors.md economics.csv go-no-go.json" ;;
  2) dir=02-requirements; req="prd.en.md prd.ar.md nfr.md pdpl-assessment.md acceptance-criteria.md wireframe-spec.md" ;;
  3) dir=03-branding;     req="brand-book.en.md brand-book.ar.md naming-shortlist.md positioning.md voice-tone.md" ;;
  4) dir=04-tech;         req="architecture.md data-model.md integrations.md deployment-topology.md cost.md" ;;
  5) dir=05-gtm;          req="gtm-plan.en.md gtm-plan.ar.md pricing.md channels.md launch-plan.md" ;;
  6) dir=06-operations;   req="runbook.md sla.md onboarding.md billing-ops.md incident-response.md kpis.md" ;;
  *) echo "unknown stage: $stage"; exit 2 ;;
esac
for f in $req; do
  if [[ -s "$dir/$f" ]]; then echo "OK       $dir/$f"
  else                        echo "MISSING  $dir/$f"; fi
done
```

Audit history for a single stage:

```bash
git log --oneline -- 04-tech/
```

Confirm no stage has written into a foreign directory in the last commit
(use before a gate review):

```bash
git diff --name-only HEAD~1 HEAD | awk -F/ '{print $1}' | sort -u
```

## §11. Cross-references

- **T1 nexoura-engagement-lifecycle** §4 (layout authority, lifecycle view)
  and §6 (inline stub — **superseded by this skill**).
- **T2 nexoura-gate-protocol** §3 — `gate.json` schema and `gates/` contents.
- **T4 nexoura-pdpl-compliance** (forthcoming) — body format of
  `02-requirements/pdpl-assessment.md`; T3 fixes only the filename.
- **T5 nexoura-bilingual-content** (forthcoming) — AR/EN content parity,
  terminology, RTL; T3 fixes only the `.en.md` / `.ar.md` convention.
