---
name: nexoura-gate-protocol
description: Use when requesting a NEXOURA gate approval, advancing between stages, blocking on a human go/no-go decision, recording a gate rejection, routing back from a rejected gate, auditing past decisions, showing gate history, sealing a gate after async approval, recovering from a crashed mid-advance, or when any sibling NEXOURA stage skill reaches end-of-stage and needs to hand control to a partner-signed strategic gate (Stages 1–5) or an operational launch-readiness gate (Stage 6). T2 foundation skill — supersedes the §5 inline stub in T1 (nexoura-engagement-lifecycle). Defines the gate.json schema, the gate.log.jsonl audit format, the atomic three-file write protocol, the v1 approval channels (CLI clarify, Kanban card, gateway message, manual), and bilingual AR+EN gate-request prompt templates.
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, gate-protocol, engagement, platform-foundation]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-artifact-conventions
      - nexoura-pdpl-compliance
---

# NEXOURA Gate Protocol (T2 — Foundation)

The contract for every gate between NEXOURA stages. Defines the request payload, the audit format, the atomic write order, the approval channels, and the bilingual prompt templates that stage skills use to hand control to a human approver. Supersedes T1 §5. Every stage skill (T6–T11) calls into §9 of this file at end-of-stage.

---

## 1. Trigger phrases

Load this skill when the operator says any of: "request gate approval", "open a gate", "advance NEXOURA stage", "advance `<slug>` to next stage", "approve gate" / "reject gate" / "revise gate", "block on human decision", "gate rejection", "route back from gate", "gate audit", "show gate history", "show gate log", "seal gate", "commit gate decision", "recover crashed gate advance", "what channel for gate approval", "gate request template" (AR or EN). If a stage skill is mid-run and reaches end-of-stage, that skill loads T2 implicitly via the §9 call pattern — no operator phrase required.

---

## 2. What is a gate

A gate is the single point of human control between two NEXOURA stages. No stage may begin until the prior gate is `approved`. Two kinds, matching T1 §3:

**Strategic (Stages 1→2, 2→3, 3→4, 4→5, 5→6).** Binary go/no-go on strategic fit, signed by a NEXOURA partner. Inputs: the closing stage's artifacts (memo, PRD, brand book, architecture, GTM plan). Decisions: `GO`, `NO-GO`, `REVISE`.

**Operational (Stage 6 only, pre-launch).** Launch-readiness review. Inputs: runbook, SLA, incident-response playbook (with the inlined 72-hour PDPL breach SLA from T4), billing-ops doc, KPI dashboard spec. Decisions: `READY`, `NOT-READY`, `CONDITIONAL`.

The protocol is uniform — only the decision vocabulary and `decision_kind` differ. Both kinds share the schema (§3), atomic write order (§5), audit log, and channels (§6).

---

## 3. The `gate.json` schema

Every gate is one JSON file in the closing stage's directory (e.g. `01-feasibility/gate.json`). Schema extends the T1 §5 stub:

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "pending | approved | rejected",
  "decision_kind": "strategic | operational",
  "from_stage": "01-feasibility",
  "to_stage": "02-requirements",
  "approver": "partner-email@nexoura.ai",
  "decision": "GO | NO-GO | REVISE | READY | NOT-READY | CONDITIONAL",
  "channel": "cli-clarify | kanban | gateway-telegram | gateway-email | manual",
  "timestamp": "2026-05-22T14:30:00Z",
  "rationale": "Free-text reasoning, ≥1 sentence, bilingual permitted.",
  "artifacts_reviewed": ["01-feasibility/feasibility-memo.en.md", "..."],
  "conditions": [],
  "next_action": null
}
```

Field contract: `request_id` UUID v4 set at pending-creation (idempotency §8.4, async correlation). `status` `pending` → `approved` | `rejected`; single transition; re-opening means a new file with a fresh `request_id`. `decision_kind` derived: `strategic` for `from_stage` ∈ {01..05}, `operational` for `06-operations`. `decision` — only the vocabulary matching `decision_kind` is legal. `channel` recorded for auditability (§6). `artifacts_reviewed` — explicit list of paths the approver saw; the request prompt MUST present it; the approver MUST be able to amend it before approving. `conditions` — populated only when `decision ∈ {REVISE, CONDITIONAL}`; one actionable string per entry. `next_action` — populated only when `status == rejected`; single-paragraph instruction back to the stage skill.

### Examples

Strategic, approved (canonical full form):

```json
{
  "request_id": "550e8400-e29b-41d4-a716-446655440000",
  "status": "approved",
  "decision_kind": "strategic",
  "from_stage": "01-feasibility",
  "to_stage": "02-requirements",
  "approver": "omar@nexoura.ai",
  "decision": "GO",
  "channel": "cli-clarify",
  "timestamp": "2026-05-22T14:30:00Z",
  "rationale": "TAM defensible at 1.2B SAR, unit economics clear, no blocking PDPL risk.",
  "artifacts_reviewed": ["01-feasibility/feasibility-memo.en.md", "01-feasibility/economics.csv"],
  "conditions": [],
  "next_action": null
}
```

Operational conditional (`decision_kind: "operational"`, `from_stage: "06-operations"`, `to_stage: "launch"`, `decision: "CONDITIONAL"`, `channel: "kanban"`): same shape, `conditions` carries one actionable string per open obligation (e.g. `"Verify ZATCA e-invoice sandbox → prod cutover before first paid invoice."`), `next_action: null`.

Strategic rejected (`status: "rejected"`, `decision: "REVISE"`, `channel: "gateway-telegram"`): same shape, `conditions` lists the required fixes, `next_action` carries the single-paragraph instruction back to the stage skill (e.g. `"Re-run T7 requirements addressing rationale; open a fresh gate with a new request_id."`).

---

## 4. Advance / Reject / Revise flow

Three branches. Each ends in exactly one commit.

**(a) Approve and advance** (`decision ∈ {GO, READY}`): Set `status: approved`, `decision`, `approver`, `timestamp`, `channel`. Update `manifest.json:current_stage` to `to_stage`. Append entry to `manifest.json:gate_history` and a line to `gate.log.jsonl`. Apply §5 atomic order. Single commit: `gate: <from_stage> → <to_stage> approved`.

**(b) Reject** (`decision ∈ {NO-GO, NOT-READY}`): `gate.json` status → `rejected`; populate `next_action`. `manifest.json:current_stage` **unchanged**. Append rejection entry to `gate_history` and `gate.log.jsonl`. Single commit: `gate: <from_stage> → <to_stage> rejected`. Stage skill re-runs with `next_action` as input; next attempt opens a fresh `gate.json` with a new `request_id`.

**(c) Revise / Conditional.** **REVISE** (strategic): rejection (§4b) with `conditions` populated and `next_action` summarising them; stage re-runs to address conditions, then opens a fresh gate. **CONDITIONAL** (operational, Stage 6 only): approval (§4a) with `conditions` populated; engagement advances to launch with open obligations tracked in the array; operator owns closing them; T11 tracks them in the runbook. Commit: `gate: 06-operations → launch approved (conditional)`.

---

## 5. Atomic write protocol

Three files mutate together on approve-and-advance: `gate.json` (status flip), `manifest.json` (current_stage + gate_history append), `gate.log.jsonl` (single line append). Order matters because `gate.log.jsonl` is the truth and `manifest.json:gate_history` is its cached mirror (T1 §5). The cache must never be durable before the source.

Safe order on POSIX:

1. Read current `manifest.json`. Validate `current_stage == gate.json.from_stage`. If not, abort (concurrent advance or stale state).
2. Write `gate.json.new`, `fsync(2)`, `rename(2)` over `gate.json`. POSIX rename is atomic within a filesystem — readers see either the old pending file or the new approved file, never torn.
3. Open `gate.log.jsonl` in append mode, write the one-line JSON object terminated by `\n`, `fsync(2)`, close. After this step the audit truth is durable.
4. Write `manifest.json.new` with `current_stage` updated and the new `gate_history` entry appended, `fsync(2)`, `rename(2)` over `manifest.json`.
5. `git add` all three files, single commit: `gate: <from> → <to> <status>`.

For rejection (§4b) the order is identical; step 4 writes only the `gate_history` append (no `current_stage` change).

Justification: if a crash happens between steps 3 and 4, recovery reads the trailing line of `gate.log.jsonl`, observes that `manifest.json` has not yet reflected it, and replays the manifest update. Truth → cache is always recoverable. Cache → truth is not.

Anti-patterns: writing `manifest.json` before `gate.log.jsonl` (cache without truth on crash); editing `gate.json` in place without rename (partial writes corrupt the file); splitting into multiple commits (audit reader cannot match manifest state to gate decision).

---

## 6. Approval channels (v1)

Four channels. Each captures the same decision; only transport differs. The `channel` field on `gate.json` records which one was used.

**6.1 CLI clarify (default, synchronous).** Operator runs the stage skill interactively. At end-of-stage the skill emits the §7 prompt inline. Operator types one of the decision keywords; worker parses and proceeds. Rationale captured by follow-up prompt. The only channel guaranteed in v1. `channel: cli-clarify`.

**6.2 Kanban card (async).** Orchestrator opens a card titled `GATE: <slug> <from_stage> → <to_stage>` (with `request_id` for back-linking). Body contains artifact list, rationale prompt, decision options as checklist. Approver edits card status and writes keyword + rationale in description. Worker poller reads description, writes back to `gate.json`. `channel: kanban`.

**6.3 Gateway message (remote).** A Hermes gateway hook DMs the approver via Telegram or Email. Body carries the bilingual §7 prompt and artifact list. Approver replies with `/approve`, `/reject`, or `/revise` plus a rationale line. Hook parses first whitespace-delimited token as keyword, remainder as rationale, matches `request_id`, writes back. Unknown keywords echo a usage hint; gate stays pending. `channel: gateway-telegram` or `gateway-email`.

**6.4 Manual (fallback).** Operator edits `gate.json` by hand, then runs `nexoura gate seal <stage>` (future tool — see §9) which validates, applies §5, commits. In v1 the operator performs §5 manually and commits. Audit-of-last-resort; expected to be rare. `channel: manual`.

---

## 7. Bilingual gate-request prompt templates

Placeholders: `{{slug}}`, `{{from_stage}}`, `{{to_stage}}`, `{{artifact_list}}`, `{{summary}}`.

### 7.1 Strategic gate request (Stages 1–5)

English:

```text
GATE REQUEST — {{slug}}
Stage transition: {{from_stage}} → {{to_stage}}

Artifacts for review:
{{artifact_list}}

Summary: {{summary}}

Please reply with one of:
  GO       — approve and advance
  NO-GO    — reject; engagement halts at {{from_stage}}
  REVISE   — reject with conditions; stage will re-run

Include a one-sentence rationale on the following line.
```

Arabic (formal KSA enterprise register):

```text
طلب اعتماد بوابة — {{slug}}
الانتقال بين المراحل: {{from_stage}} ← {{to_stage}}

المخرجات المرفوعة للمراجعة:
{{artifact_list}}

ملخّص تنفيذي: {{summary}}

نأمل التكرّم بإفادتنا بأحد الخيارات:
  GO       — الموافقة والانتقال إلى المرحلة التالية
  NO-GO    — الرفض وإيقاف العمل عند المرحلة الحالية
  REVISE   — الرفض المشروط مع إعادة تنفيذ المرحلة

يُرجى إرفاق مسوّغ مختصر في سطر مستقل عقب القرار.
```

### 7.2 Operational gate request (Stage 6)

English:

```text
LAUNCH READINESS GATE — {{slug}}
Transition: 06-operations → launch

Readiness artifacts:
{{artifact_list}}

Readiness summary: {{summary}}

Please reply with one of:
  READY        — approve launch
  NOT-READY    — block launch; operations re-runs
  CONDITIONAL  — approve launch with open conditions (list them next)

Include a one-sentence rationale and, for CONDITIONAL, one condition per line.
```

Arabic:

```text
بوابة جاهزية الإطلاق — {{slug}}
الانتقال: 06-operations ← مرحلة الإطلاق

مخرجات الجاهزية التشغيلية:
{{artifact_list}}

ملخّص الجاهزية: {{summary}}

نأمل التفضّل بأحد الخيارات:
  READY        — اعتماد الإطلاق
  NOT-READY    — تأجيل الإطلاق وإعادة المرحلة التشغيلية
  CONDITIONAL  — اعتماد الإطلاق بشروط (تُذكر كلٌّ في سطر مستقل)

يُرجى إرفاق مسوّغ مختصر مع تعداد الشروط إن وُجدت.
```

### 7.3 Rejection notification (back to the stage operator)

English:

```text
GATE REJECTED — {{slug}} ({{from_stage}} → {{to_stage}})
Decision: {{decision}}     Approver: {{approver}}

Rationale: {{rationale}}
Required next action: {{next_action}}

Re-run the {{from_stage}} stage skill addressing the rationale, then open a fresh gate with a new request_id.
```

Arabic:

```text
رُفض اعتماد البوابة — {{slug}} ({{from_stage}} ← {{to_stage}})
القرار: {{decision}}     المعتمد: {{approver}}

المسوّغ: {{rationale}}
الإجراء المطلوب: {{next_action}}

يُرجى إعادة تنفيذ مرحلة {{from_stage}} وفق المسوّغ أعلاه، ثم فتح بوابة جديدة بمُعرّف طلب مستقل.
```

---

## 8. Error recovery

**8.1 Partial write of `gate.log.jsonl`.** Detect: `tail -n 1 gate.log.jsonl | jq . >/dev/null 2>&1 || echo "CORRUPT TAIL"`. Recover: truncate the corrupt trailing line (`sed -i '$d' gate.log.jsonl`) and rebuild from git. Every gate decision is its own commit, so `git log --diff-filter=AM -- gate.log.jsonl` lists every append. Pick the missing entry from the diff of the most recent gate commit and re-append.

**8.2 `manifest.json` out of sync with `gate.log.jsonl`.** `gate.log.jsonl` wins (T1 §5). Rebuild `manifest.json:gate_history` by replaying every line of the log in order. `current_stage` is the `to_stage` of the last `status: approved` line whose `decision ∈ {GO, READY, CONDITIONAL}`.

**8.3 Crashed mid-advance.** Detect on startup: read `gate.json` and `manifest.json`. If `gate.json.status == approved` and `manifest.json.current_stage == gate.json.from_stage`, the §5 sequence crashed between steps 3 and 4 — replay step 4 (write the manifest update), then commit `gate: <from> → <to> approved (recovered)`. If `gate.json.status == approved` and the trailing log line does not carry `gate.json.request_id`, the crash was between steps 2 and 3 — re-emit the log line, then proceed to step 4.

**8.4 Duplicate approval (idempotency).** Before appending to `gate.log.jsonl`, scan for the incoming `request_id`. If it already exists with `status: approved` or `rejected`, the request is a replay (common on gateway retries) — drop silently, do not re-commit. This is why `request_id` is set at pending-creation, not at decision time.

---

## 9. How stage skills call this

V1 has no `nexoura_gate` binary yet, so stage skills perform §4 + §5 manually. The pseudocode documents the v2 API surface and is the contract stage skills should code against today (substituting manual file ops for the call).

```python
import nexoura_gate  # v2 — not yet shipped

result = nexoura_gate.request(engagement_slug, {
    "from_stage": "01-feasibility",
    "to_stage": "02-requirements",
    "artifacts_reviewed": [...],
    "summary": "TAM ≈ 1.2B SAR; 3 anchor buyers interviewed; no PDPL blocker.",
    "channel": "cli-clarify",
})

if result.decision in ("GO", "READY"):
    handoff_to_next_stage(result.to_stage)
elif result.decision in ("REVISE", "CONDITIONAL"):
    re_run_with(result.conditions)
else:  # NO-GO, NOT-READY
    halt_engagement(result.rationale)
```

V1 manual equivalent: stage skill (a) generates a `request_id`, (b) writes `gate.json` with `status: pending`, (c) emits the §7 prompt on the chosen channel, (d) reads the decision back, (e) applies §4 + §5, (f) returns the decision to its caller.

---

## 10. Cross-references

- **T1 `nexoura-engagement-lifecycle`** — §2 manifest schema, §3 stage definitions (strategic vs operational vocabulary), §4 directory layout (`gate.log.jsonl` at engagement root, `gate.json` in each closing stage subdirectory). T1 §5 is the stub this skill supersedes.
- **T3 `nexoura-artifact-conventions`** (when it lands) — defers to T3 for filename casing of `gate.json` and placement rules for `gate.log.jsonl`. Protocol (schema, atomic order, channels, templates) stays here.
- **T6–T11 stage skills** (when they land) — each calls into §9 at end-of-stage. T11 (operations) is the only caller using the operational vocabulary.

---

When T3 lands, §5's path conventions defer to T3; the protocol itself stays here.
