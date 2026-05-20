---
name: nexoura-implementation-stage
description: NEXOURA Stage 4.5 — implementation/build playbook. Closes design-to-code gap between Tech Architecture (T9) and GTM (T10). Specifies methodology, sprint cadence, branching, code review, testing, CI/CD, DoD, security/PDPL gates, bilingual i18n build, and 7 specialist roles. Operational gate to launch.
triggers: NEXOURA Stage 4.5, implementation stage, build playbook, sprint plan, CI/CD spec, code review rubric, DoD, gate 4.5
stage: 4.5
gate_type: operational
---

# NEXOURA Stage 4.5 — Implementation / Build Playbook

## 1. Purpose and Stage Position

Stage 4.5 is the build stage. It is inserted between Stage 4 (Tech Architecture, T9) and Stage 5 (GTM/Marketing, T10) in the NEXOURA engagement lifecycle (see T1 Section 3 stage map). Its single purpose: turn the design output of T9 (architecture.md, ADRs, integrations.md, threat model) into a deployable, observable, PDPL-compliant product increment that GTM can launch in Stage 5.

Inputs (from T9): architecture.md, ADRs, integrations.md, NFR register (T7), threat model, data classification map.

Outputs (to T10): deployed staging environment, production-ready build artifact, runbook, observability dashboards, DoD-certified release candidate, operational gate sign-off (gate-4.5-to-5.json).

The gate type is operational (per T2 taxonomy): the question is not "should we build this?" — that was answered at Gate 3->4. The question is "is the build ready to launch?".

## 2. Build Methodology Selection

Decision matrix (pick one at sprint 0):

| Factor | Trunk-based | Gitflow |
|---|---|---|
| Team size | 2-12 | 12+ |
| Release cadence | Continuous / weekly | Quarterly fixed |
| Feature flags adoption | Required | Optional |
| KSA NEXOURA default | YES | Only for regulated banking clients |

Agile cadence:

- Scrum — fixed 2-week sprints, full ceremony set; best when scope is mostly known.
- Kanban — flow-based, WIP-limited; best for ops/support overlap or post-launch evolution.
- Scrumban — sprint planning + WIP limits; pragmatic default when team is forming.

KSA team-size guidance: a NEXOURA platform engagement typically runs 4-7 builders (1 TL, 1-2 FE, 1-2 BE, 1 QA, 1 DevOps, shared Security/A11y). Default methodology = trunk-based + 2-week Scrumban. Working week is Sun-Thu; Friday-Saturday is weekend in KSA — sprint boundaries land on Thursday EoD.

## 3. Sprint and Iteration Cycle

Default sprint = 2 weeks = 10 KSA business days (Sun-Thu x2).

Capacity formula:

    velocity = team_size * focus_factor * sprint_days

where focus_factor = 0.6 for a forming team, 0.75 for an established team, capped at 0.8 for KSA context (accounts for prayer breaks, Ramadan adjustments, public holidays).

Ceremonies:

- Sprint planning — Sun day 1, 2h max, scope locked at end.
- Daily standup — 15min, async-allowed for distributed team.
- Sprint review — Thu day 10, demo to product owner + stakeholders.
- Retro — Thu day 10 after review, 1h, action items tracked in retro log.
- Backlog refinement — Tue day 6, 1h, next sprint candidates groomed.

Ramadan note: reduce sprint capacity by 30% during Ramadan; shift core hours; do not schedule release windows in last 10 days of Ramadan.

## 4. Branching Strategy and PR Conventions

Cross-ref T3 (artifact-conventions) Section on branching. Summary:

- Default branch: main (always deployable).
- Feature branches: feat/<scope>-<slug> — short-lived, max 5 days.
- Fix branches: fix/<scope>-<slug>.
- Chore/docs: chore/<slug>, docs/<slug>.
- Release tags: vMAJOR.MINOR.PATCH (semver).

PR conventions:

- Title: type(scope): description — e.g. feat(billing): add ZATCA e-invoice fields.
- Body: links to issue, screenshots for UI, NFR impact note, rollback plan.
- Reviewers: minimum 1 engineer + 1 domain (security for auth/data, a11y for UI, devops for infra).
- Merge strategy: squash-merge default; merge commit only for release branches.
- Auto-delete branch on merge.

## 5. Code Review Rubric

Five dimensions, each scored pass/conditional/fail:

| Dimension | Checklist |
|---|---|
| Correctness | Logic matches spec; edge cases covered; no obvious bugs; tests assert behavior not implementation |
| Security | No secrets in code; input validated; authz checked; PDPL data class respected; OWASP top-10 considered (cross-ref T9 security) |
| NFR compliance | Perf budget respected; observability hooks present; SLO impact assessed (cross-ref T7 NFR register) |
| Testability | Pure functions where possible; dependencies injected; tests run <30s locally |
| Observability | Structured logs; correlation ID; metrics for new flows; trace spans on external calls |

A PR with any "fail" cannot merge. "Conditional" requires a tracked follow-up ticket linked in the PR.

## 6. Testing Strategy

Five layers, all gated in CI:

1. Unit — Jest/Vitest/PyTest. Coverage gate: 70% line, 60% branch on changed files. Runs in <2min.
2. Integration — service-level with real dependencies via docker-compose or testcontainers. Database, cache, queue exercised.
3. E2E — Playwright (preferred) or Cypress. Critical user journeys: signup, primary action, payment if billing. Run in both AR and EN locales — i18n parity is a hard gate.
4. Load — k6 scripts. p95 latency budget from T7 NFR register validated against staging. Soak test before each release.
5. Accessibility — axe-core automated checks (WCAG 2.1 AA), plus manual screen-reader pass on critical screens in AR RTL.

Test data: synthetic only in CI; PDPL-class data never enters fixtures. Test environments are tagged data-class=synthetic.

## 7. CI/CD Pipeline Spec

GitHub Actions default (GitLab CI for clients on self-hosted). Pipeline stages:

    lint -> unit -> sast (semgrep) -> build -> integration ->
    e2e -> security-scan (trivy) -> deploy-stg -> manual-gate -> deploy-prod

KSA compliance gates inserted at:

- After build: PDPL data-class lint — verifies no class-3 (sensitive personal) data fields leak into logs/metrics.
- Before deploy-stg: data-residency check — confirms target region is me-south-1 (Bahrain) or me-central-1 (UAE); deployment to non-MENA regions blocks.
- Before deploy-prod: ZATCA cert validation (only if billing/e-invoice in scope) — sandbox cert refreshed, production cert chain valid.
- Before deploy-prod: manual operational gate — Tech Lead + DevOps sign-off (gate-4.5-to-5.json).

Pipeline artifacts: SBOM (CycloneDX), signed container image (cosign), test reports, coverage report, accessibility report.

## 8. Feature Flag Strategy

Every new user-visible capability ships behind a flag. Kill-switch is mandatory.

Flag types:

- Release — toggle new capability on/off; removed within 30 days post 100% rollout.
- Ops — circuit breaker for downstream dependency; permanent.
- Permission — entitlement gating (e.g. premium tier); permanent.
- Experiment — A/B test; sunset on experiment conclusion.

Tool: LaunchDarkly for managed; Unleash (self-hosted) for clients requiring KSA data residency. Flag config is code-reviewed like any other change.

Cleanup SLA: 30 days post full rollout. Stale-flag report runs weekly; flags older than SLA appear in retro.

## 9. Definition of Done (DoD)

A story is Done only when ALL apply:

- [ ] Code merged to main via PR with required approvals.
- [ ] Unit + integration + E2E tests pass in CI.
- [ ] Coverage gate met (>=70% line on changed files).
- [ ] NFR-perf p95 measured against budget (T7 NFR register reference).
- [ ] NFR-availability SLO check — no regression in error budget burn rate.
- [ ] Security scan clean (SAST, dependency vuln, container scan).
- [ ] Accessibility audit passed (axe-core + manual RTL pass if UI changed).
- [ ] AR + EN content reviewed by bilingual reviewer; parity verified.
- [ ] Observability dashboard updated (new metrics/logs/traces wired).
- [ ] Runbook updated (new failure modes documented).
- [ ] PDPL DPIA refreshed if data flow changed (new collection point, new third-party share, new retention).
- [ ] Feature flag configured (default off in prod) and documented.
- [ ] Rollback plan validated in staging.

Every checkbox maps back to a named test, scan, or artifact — DoD is mechanically verifiable.

## 10. Security and PDPL Gates per Commit

Pre-commit (developer machine, husky/pre-commit hook):

- gitleaks — secrets scan.
- semgrep — local SAST ruleset (NEXOURA baseline + OWASP).
- prettier/eslint/ruff — format and lint.

PR gates (CI):

- Dependency vulnerability scan (Dependabot + Snyk or osv-scanner) — block on critical/high.
- PDPL data-class lint — custom semgrep rules detect new fields touching class-2/3 data without classification annotation.
- Threat-model delta review — any new external endpoint, auth flow change, or data store triggers a security-engineer review (cross-ref T9 Section security).
- License compliance scan — block on GPL/AGPL drift into proprietary modules.

Container/image gates (pre-deploy):

- Trivy scan — block on critical CVEs without justified exception.
- Cosign signature verification on pull.

## 11. Bilingual Content Build Pipeline

Stack: i18next (web) or ICU MessageFormat (mobile/native). All user-visible strings externalized.

Rules:

- Two locale files: en.json (source of truth for keys), ar.json (KSA-formal register).
- Build-time check: missing AR key OR missing EN key = build fails.
- AR RTL: CSS logical properties (margin-inline-start, padding-inline-end) — no left/right. Tested via Playwright with locale=ar-SA, dir=rtl.
- Pluralization: AR has 6 plural forms (zero, one, two, few, many, other) — all must be supplied for numeric strings.
- Number formatting: Intl.NumberFormat with locale ar-SA; Hijri date option available where relevant.
- Translation memory: stored in /i18n/tm/ to keep tone consistent across releases.
- Reviewer: Accessibility Reviewer signs off on AR RTL UX before merge of UI changes.

## 12. Specialist Profiles

Seven roles. Each has mission, primary outputs, KSA context, escalation triggers.

Tech Lead. Mission: own the implementation outcome end-to-end. Outputs: sprint plan, DoD enforcement, architecture-implementation fidelity, gate 4.5 sign-off. KSA context: stakeholder-facing in Arabic when needed. Escalate: scope-vs-NFR conflict, slipped gate criteria.

Frontend Engineer. Mission: ship UI matching design system, AR/RTL parity. Outputs: components, E2E tests, a11y compliance. KSA context: AR RTL is first-class, not bolt-on. Escalate: design ambiguity, a11y blockers.

Backend Engineer. Mission: implement services per architecture.md and ADRs. Outputs: APIs, data models, integration adapters, unit/integration tests. KSA context: data-residency-aware (me-south-1/me-central-1). Escalate: schema-vs-PDPL conflict, integration partner SLA gaps.

QA Engineer. Mission: prove the build meets DoD. Outputs: test plan, E2E suites, regression matrix, bug reports with reproductions. KSA context: tests run in AR+EN. Escalate: untestable requirements, flaky-test rate >5%.

DevOps Engineer. Mission: CI/CD, infra-as-code, observability, deploy. Outputs: pipeline config, Terraform/Pulumi modules, dashboards, runbook. KSA context: deployments restricted to me-south-1 (Bahrain) or me-central-1 (UAE) by default; PDPL-aware logging (no class-3 data to non-KSA log sinks). Escalate: region capacity issues, cost overruns vs budget.

Security Engineer. Mission: threat-model new endpoints, enforce PDPL gates. Outputs: threat model delta, security checklist sign-off, DPIA refresh. KSA context: PDPL + SAMA (if banking) + NCA ECC controls. Escalate: critical CVE in dependency, data-class violation, unresolved threat.

Accessibility Reviewer. Mission: WCAG 2.1 AA + AR RTL UX quality. Outputs: a11y audit report, RTL review notes. KSA context: AR screen-reader testing (VoiceOver ar-SA, NVDA Arabic). Escalate: contrast/keyboard/RTL regressions blocking release.

## 13. Output Artifacts

All under 05-implementation/ (per T3 canonical path):

    05-implementation/
      build-plan.en.md
      build-plan.ar.md
      sprint-plan.md
      ci-cd-spec.md
      code-review-rubric.md
      dod.md
      security-checklist.md
      runbook.md
      observability/
        dashboards.md
        slo.md
      gates/
        gate-4.5-to-5.json

Bilingual split (build-plan.en.md + build-plan.ar.md) follows T3 Section 3.2 file-split convention. All other operational docs are EN-primary; AR translation only for client-facing deliverables.

## 14. Operational Gate to Stage 5

File: gates/gate-4.5-to-5.json. Gate type is operational (per T2): evaluates build readiness, not strategic fit.

Schema:

    {
      "gate_id": "string",
      "gate_type": "operational",
      "from_stage": "4.5",
      "to_stage": "5",
      "evaluator": ["Tech Lead", "DevOps Engineer"],
      "criteria": [
        "dod_complete",
        "security_scan_clean",
        "perf_slo_met",
        "accessibility_pass",
        "ar_en_parity",
        "runbook_published",
        "rollback_tested"
      ],
      "decision": "go | conditional-go | no-go",
      "conditions": ["string"],
      "signed_by": ["name (role)"],
      "signed_at": "ISO-8601"
    }

Worked example:

    {
      "gate_id": "nx-acme-2026Q2-gate-4.5",
      "gate_type": "operational",
      "from_stage": "4.5",
      "to_stage": "5",
      "evaluator": ["Tech Lead", "DevOps Engineer"],
      "criteria": [
        "dod_complete",
        "security_scan_clean",
        "perf_slo_met",
        "accessibility_pass",
        "ar_en_parity",
        "runbook_published",
        "rollback_tested"
      ],
      "evidence": {
        "dod_complete": "All 47 stories DoD-certified, see retro-2026-05.md",
        "security_scan_clean": "Trivy 0 critical, Semgrep 0 high, Snyk 2 medium accepted",
        "perf_slo_met": "p95 218ms vs 250ms budget (T7 NFR-PERF-01)",
        "accessibility_pass": "axe-core 0 violations, RTL manual pass 2026-05-18",
        "ar_en_parity": "i18n diff = 0",
        "runbook_published": "runbook.md v1.3.0",
        "rollback_tested": "Staging rollback drill 2026-05-19, RTO 4m"
      },
      "decision": "go",
      "conditions": [],
      "signed_by": ["Omar A. (Tech Lead)", "F. Al-Harbi (DevOps)"],
      "signed_at": "2026-05-20T14:00:00+03:00"
    }

A conditional-go must list specific conditions with owners and dates; a no-go reopens the sprint.

## 15. Strategic Gate Prompt (Bilingual)

This gate is operational, so the prompt addresses Tech Lead + DevOps, not the strategic exec board.

EN (max 30 lines):

    Operational Gate 4.5 -> 5: Build Readiness Review.
    Evaluators: Tech Lead, DevOps Engineer.
    Question: Is the build ready to launch?
    For each criterion, attach evidence:
      1. DoD complete for every story in scope.
      2. Security scans clean (SAST, dependency, container).
      3. Performance SLO met against T7 NFR register.
      4. Accessibility audit passed (WCAG 2.1 AA + AR RTL).
      5. AR/EN content parity verified.
      6. Runbook published and reviewed by on-call.
      7. Rollback drill executed in staging with measured RTO.
    Decision: go, conditional-go, or no-go.
    If conditional-go, list each condition with owner and date.
    Sign and timestamp in gate-4.5-to-5.json.
    Escalation: if no-go, return to sprint with named blockers.

AR (KSA-formal, max 30 lines):

    بوابة تشغيلية 4.5 -> 5: مراجعة جاهزية الإطلاق.
    المقيّمون: القائد التقني، مهندس العمليات.
    السؤال: هل البناء جاهز للإطلاق؟
    لكل معيار، يُرفق الدليل:
      1. اكتمال تعريف الإنجاز لكل قصة في النطاق.
      2. نظافة الفحوصات الأمنية (SAST، التبعيات، الحاويات).
      3. تحقيق هدف مستوى الأداء وفق سجل المتطلبات غير الوظيفية (T7).
      4. اجتياز تدقيق إمكانية الوصول (WCAG 2.1 AA ودعم العربية RTL).
      5. التحقق من تكافؤ المحتوى العربي والإنجليزي.
      6. نشر دليل التشغيل ومراجعته من فريق المناوبة.
      7. تنفيذ تجربة الاسترجاع في بيئة الاختبار مع قياس زمن الاسترداد.
    القرار: موافقة، موافقة مشروطة، أو رفض.
    في حال الموافقة المشروطة، تُذكر كل شرط مع المسؤول والتاريخ.
    يُوقَّع ويُؤرَّخ في الملف gate-4.5-to-5.json.
    التصعيد: في حال الرفض، تُعاد الدورة مع تحديد المعوقات.

## 16. Cross-References

- T1 (engagement-lifecycle) — Stage 4.5 inserted between Stage 4 and Stage 5 in Section 3 stage map. T1 is the master sequence; this skill is the contents of Stage 4.5.
- T2 (gate-protocol) — defines operational vs strategic gate types. Gate 4.5->5 is operational; evaluator panel is build-side (TL + DevOps), not exec board.
- T3 (artifact-conventions) — branch naming (feat/fix/chore), PR title type(scope): description, bilingual file split (.en.md / .ar.md), canonical path 05-implementation/.
- T7 (nfr-quality) — every NFR in the register must be validated by a named test or scan listed in Section 9 DoD. Implementation does not declare an NFR met without mechanical evidence.
- T9 (tech-architecture-stage) — Stage 4 outputs (architecture.md, ADRs, integrations.md, threat model) are the design input. Stage 4.5 implements them; any deviation requires an ADR update before merge.
