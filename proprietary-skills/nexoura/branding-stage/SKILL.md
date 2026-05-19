---
name: nexoura-branding-stage
description: "Use when running NEXOURA Stage 3 — phrases like 'branding for <engagement>', 'name candidates', 'NEXOURA stage 3', 'positioning statement for <X>', 'voice and tone guide for <slug>', 'brand book for <X>', 'open the strategic gate from stage 3'. T8 stage skill — turns a Stage 2 partner-signed PRD into a bilingual brand foundation (naming shortlist, positioning, voice & tone, brand-book with embedded visual direction) and hands off via a strategic gate per T2."
version: 0.1.0
author: NEXOURA AI (APT WATCH)
license: Proprietary
metadata:
  hermes:
    tags: [nexoura, stage-skill, branding, stage-3]
    related_skills:
      - nexoura-engagement-lifecycle
      - nexoura-gate-protocol
      - nexoura-artifact-conventions
      - nexoura-requirements-stage
      - nexoura-bilingual-content
---

# NEXOURA Branding — Stage 3 Playbook (T8)

Turns a signed Stage 2 GO into a partner-signable brand foundation: a name, a positioning statement, a voice the engagement will speak in, and a brand-book the Stage 4 build skins against. Four artifacts under `03-branding/` (plus the gate decision under `gates/`), one strategic gate at exit per T2 §3. Expands the T1 §3 Stage 3 stub; for lifecycle, gates, filenames, defer to T1 / T2 / T3.

طلب — مرحلة العلامة التجارية (Stage 3): من متطلبات الحاسوب إلى هويّة يتحدّث بها المنتج بلغتين.

---

## §1. Scope and triggers

**Triggers.** "branding for `<engagement>`"; "name candidates"; "NEXOURA stage 3"; "positioning statement for `<X>`"; "voice and tone guide for `<slug>`"; "brand book for `<X>`"; "open the strategic gate from stage 3".

**Non-triggers (defer).** Feasibility → T6. PRD, NFRs, stories → T7. Stack, ADRs → T9. GTM channel messaging → T10. Gate mechanics → T2. File placement → T3. Bilingual register rules → T5 (deferred this phase; applied inline below).

**Preconditions.** `manifest.json:current_stage == "03-branding"`. Stage 2 left behind partner-signed `02-requirements/prd.en.md` **and** `02-requirements/prd.ar.md` (parity per T3 §5), and the persona section (PRD §4) is populated — branding without a persona is a refusal. The exit gate of Stage 2 (`gates/gate-2-to-3.json`) must be `approved` with `decision == "GO"`. If `current_stage != "03-branding"`, abort and surface the manifest. If either PRD file is missing or §4 is empty, refuse and route back to T7.

---

## §2. Stage 3 workflow

1. **Kickoff.** Read PRD §1, §2, §4 in both EN and AR. The persona's language preference distribution sets the AR/EN weighting in §3.
2. **Brief assembly.** Brand Strategist drafts a one-page internal brief (working file, not gate-tracked).
3. **Naming.** Naming Specialist runs the §3 methodology; ≥ 5 candidates with bilingual rationale and trademark sanity-check notes. Trademark Researcher signs before positioning starts.
4. **Positioning.** Brand Strategist authors `positioning.md` — one statement, one EN and one AR worked example (§4).
5. **Voice & tone.** Copywriter (AR + EN) drafts `voice-tone.md` with formality↔warmth calibration and concrete do/don't pairs **in both languages** (§5).
6. **Visual direction.** Visual Designer authors the visual section embedded in the brand-book (§6.5). No image generation in v1.
7. **Brand-book assembly.** Brand Strategist composes `brand-book.en.md` and the parity Arabic mirror `brand-book.ar.md` per T3 §5, weaving name + positioning + voice + visual + application examples (§7).
8. **Review.** Trademark Researcher re-signs the chosen name; Copywriter signs voice/tone parity; Visual Designer signs the visual section; partner reviews the bundle.
9. **Strategic gate.** Engagement owner writes `gates/gate-3-to-4.json` per T2 §3 and §9 below.

---

## §3. Naming methodology — `naming-shortlist.md`

Each candidate is evaluated on five axes:

1. **Semantic mapping (EN + AR).** What does the name evoke in EN and in its closest AR rendering? Drift between the two is a rejection signal unless intentional.
2. **Phonetic — EN.** Pronounceable by a non-Arabic-speaking English reader without coaching; no embedded slur or awkward homophone.
3. **Phonetic — AR.** Pronounceable in KSA-formal register without forced sound substitution (e.g. names whose only AR rendering forces `p → ب` ambiguity are flagged if the brand will be spoken aloud in support). Verify against KSA pronunciation specifically.
4. **Trademark sanity check.** Search Saudi Authority for Intellectual Property (SAIP) public register for exact and near matches in the Nice class(es) relevant to the engagement. WHOIS on `.sa`, `.com.sa`, `.com` — taken `.com` is acceptable if `.sa` is free and brand is KSA-first; both taken is a hard reject. **Not legal clearance** — the brand-book §1 carries a disclaimer routing the client to formal counsel pre-filing.
5. **KSA cultural register.** No religiously-charged term used commercially; no tribe / family name without explicit client authorisation; no political or geographic claim the engagement cannot back.

### 3.1 Shortlist row template

```markdown
### Candidate N — <Name>
- **AR rendering:** <native form, e.g. نِكسا> — transliteration: <Nexa>
- **Semantic — EN / AR:** one sentence each. AR مثال: يُوحي بالامتداد والترابط.
- **Phonetic — EN / AR:** clean / acceptable / awkward (with note).
- **Trademark sanity:** SAIP result (clear / collision class N / unclear); WHOIS `.sa / .com.sa / .com`.
- **Cultural register:** clean / requires-authorisation / flagged.
- **Recommendation:** advance / hold / drop.
```

**Minimum at gate:** five candidates. **Acceptance criterion (kanban T8):** at least one candidate must work cleanly in BOTH AR and EN markets — flagged `advance` with no awkward phonetic on either axis. Five EN-only candidates fails the gate.

---

## §4. Positioning — `positioning.md`

Template: **For** `<persona, citing PRD §4>` / **who** `<job-to-be-done>`, `<name>` is the `<category>` that `<primary benefit>`. **Unlike** `<incumbent alternative>`, our product `<defensible differentiator from PRD §2>`.

One paragraph of supporting evidence cites PRD §1 and Stage 1 memo §3. Currency in SAR primary, USD parenthetical.

### 4.1 Worked example — English

> **For** Riyadh-based SMB owners running multi-branch retail **who** lose hours weekly reconciling daily branch close-outs across WhatsApp and spreadsheets, **Nexa** is the operations cockpit that consolidates every branch into one Arabic-first dashboard by 09:00 the next morning. **Unlike** generic ERP modules that demand six-week implementations, Nexa onboards in under a day and ships ZATCA-compliant export out of the box.

### 4.2 Worked example — Arabic (KSA-formal register)

> **لأصحاب المنشآت الصغيرة والمتوسطة في الرياض** الذين يديرون فروعاً متعدّدة في قطاع التجزئة، و**الذين** يُهدرون ساعات أسبوعياً في تسوية إقفال الفروع اليومي عبر مجموعات واتساب والجداول، فإنّ **نِكسا** هي منصّة التشغيل التي تُوحِّد جميع الفروع في لوحة واحدة باللغة العربيّة قبل الساعة التاسعة من صباح اليوم التالي. **بخلاف** وحدات تخطيط الموارد التقليديّة التي تتطلّب تطبيقاً يمتدّ ستّة أسابيع، تنطلق نِكسا في أقلّ من يوم، وتدعم التصدير المتوافق مع متطلّبات هيئة الزكاة والضريبة والجمارك (ZATCA) منذ اللحظة الأولى.

AR is **not** a translation of EN — it is a parallel composition in the formal KSA register per T5 (deferred). The transliteration نِكسا is fixed in `naming-shortlist.md` and quoted, not re-romanised, across artifacts.

---

## §5. Voice & tone — `voice-tone.md`

### 5.1 Formality and warmth scales

Default register: **formal-warm** (سمت رسميّ ودود). Two scales 0–4:

- **Formality.** 0 = casual peer → 4 = ceremonial. Defaults: marketing **2.5**, partner/operator **3**, in-product UI **2**, support **1.5**. The Arabic baseline runs **+0.5** above EN on the same surface — KSA-formal has a higher floor than US business English.
- **Warmth.** 0 = transactional → 4 = effusive. Default **2.5** in both languages. Warm but not familiar.

### 5.2 Do / don't pairs — English

| Do | Don't |
|----|-------|
| "Your branches are reconciled. Review the variance report by 09:00." | "🎉 You're all set! Pop into the variance report whenever." |
| "Payment failed. We've retried 3 times. Tap to update card details." | "Oops, something went wrong. Try again later?" |
| "This deletes 14 records. Type the branch name to confirm." | "Are you sure? This cannot be undone." |

### 5.3 Do / don't pairs — Arabic (KSA-formal register)

| المقبول (Do) | المرفوض (Don't) |
|-------------|----------------|
| «تمّت تسوية الفروع. يُرجى مراجعة تقرير الفروقات قبل الساعة التاسعة.» | «تمام! شوف الفروقات لمّا تفضى.» |
| «تعذّر إتمام عملية الدفع بعد ثلاث محاولات. اضغط لتحديث بيانات البطاقة.» | «صار خطأ، حاول بعدين.» |
| «سيُحذف 14 سجلّاً. يُرجى كتابة اسم الفرع للتأكيد.» | «متأكّد؟ ما يصير ترجع.» |

### 5.4 Cross-cutting rules

- Emoji: forbidden in product UI and operator comms; ≤ 1 per piece in social marketing only; **never** in Arabic copy in the KSA-enterprise register (drops formality ~1.5 points).
- Latin technical terms (`ZATCA`, `MVP`, `API`) stay in Latin script inside Arabic copy per T3 §5.
- Numerals: Latin digits in both EN and AR. Currency: `SAR` (or `ريال سعودي` in formal AR contexts).
- Voice never drops below 1.5 in any surface; never rises above 3.5 outside ceremonial press releases.

---

## §6. Brand-book — `brand-book.en.md` + `brand-book.ar.md`

Bilingual pair, T3 §5 parity. Single document weaves name → positioning → voice → visual direction → application examples. Required H2 skeleton:

```markdown
# Brand Book — <name> (Stage 3)

## 1. Brand essence
One paragraph: who, what claim, what tone. Legal disclaimer (trademark sanity-check ≠ clearance).

## 2. Name and rationale
Chosen candidate from naming-shortlist.md; AR rendering; pronunciation note.

## 3. Positioning
Inline copy of the `positioning.md` statement (EN file = EN; AR file = AR).

## 4. Voice and tone
Two-paragraph synthesis of `voice-tone.md` §5.1 + §5.4; pointer to that file for the full grid.

## 5. Visual direction
(§6.5 below)

## 6. Tagline
Chosen tagline (EN + AR) with §7 rationale.

## 7. Application examples
Text-level only; see §7 of this skill.
```

The AR mirror keeps the same H2 numbering and order, translates the prose into KSA-formal Arabic, and keeps colour token names, font names, CSS variable names, and Latin technical terms in Latin script per T3 §5.

### 6.5 Visual direction (text-level spec)

**Palette tokens.** Minimum five CSS-variable tokens, WCAG AA verified. Example: `--brand-primary: #0F4C5C` (deep teal, primary surface + hero CTAs), `--brand-accent: #E5A823` (warm gold, secondary CTA), `--brand-ink: #14181F` (body), `--brand-surface: #FAFAF7` (page bg; reads warmer than pure white in Arabic body copy), `--brand-surface-dark: #0B1419` (dark mode). State tokens (`--state-success/warn/error`) added inline.

**Typography pairing.** Heading + body in a humanist sans with full Arabic glyph coverage (e.g. **IBM Plex Sans Arabic** or **Tajawal**) — KSA Arabic legibility at small sizes with clean Latin parity. Body 16px / 1.55 (Latin) and 17px / 1.7 (Arabic needs more leading). Numerals: Latin tabular figures in tables and dashboards.

**Logo concept brief (for a designer).** Symbol: a single continuous mark referencing the PRD §2 wedge, rendered so it reads identically LTR and RTL (the wordmark sits beside both Latin and Arabic copy). Wordmark: lowercase Latin in the heading family at optical weight 500–600; Arabic wordmark hand-tuned, **not** auto-rendered, with kashida-aware spacing. Clearspace 1× cap-height; min size 24px digital / 16mm print. Mono-colour and reversed-out variants required. No drop shadow / gradient in v1.

**Spacing scale.** 4-pt base grid: `--space-1..12` at 4/8/12/16/24/32/48 px. RTL mirrors horizontal tokens; no separate AR scale.

---

## §7. Tagline + application examples

### 7.1 Tagline process

Brand Strategist proposes three candidates per language; Copywriter writes natural-Arabic alternatives (not translations of the EN); team picks one per language. Constraint: ≤ 7 words EN, ≤ 6 words AR; must not contradict the §4 differentiator.

**Worked example.** EN: "Every branch, one morning view." AR: «كلّ الفروع، في لوحة صباح واحدة.» Both ship in `brand-book.{en,ar}.md` §6. AR is composed parallel, not literal.

### 7.2 Brand applications (text-level, no images in v1)

Three descriptions land in `brand-book.{en,ar}.md` §7. **Web hero:** `--brand-surface`; wordmark top-left (LTR) / top-right (RTL); H1 carries the §7.1 tagline at heading family weight 600, 56px desktop / 36px mobile; subhead is the §4 positioning sentence one at 20px; primary CTA on `--brand-primary`. No hero illustration in v1. **Product UI label (dashboard tile):** card on `--brand-surface`, `--space-4` padding, heading 14px/600, metric 32px/500 tabular figures, delta in `--state-success`/`--state-error` at 12px; AR variant mirrored RTL with heading 15px. **Deck cover:** `--brand-surface-dark`; wordmark centred at 1/6 page height; title 48pt heading family; engagement slug + date 12pt in `--brand-accent`; AR deck mirrored RTL with title composed parallel.

---

## §8. Specialist profiles

Five roles. Specialists write only into files they own (T3 §9); read is universal.

| Role | Owns | Responsibility | Gate handoff |
|------|------|----------------|--------------|
| **Brand Strategist** | `positioning.md`, `brand-book.{en,ar}.md` §1, §6, §7 | Reads PRD §1, §2, §4; authors positioning; integrates sub-deliverables into the brand-book. | Signs positioning and the bundled brand-book. |
| **Naming Specialist (AR + EN)** | `naming-shortlist.md` | Runs the §3 five-axis methodology over ≥ 5 candidates; AR rendering and rationale per candidate. Owns the bilingual-acceptance criterion. | Signs the shortlist; flags the chosen candidate to Trademark Researcher. |
| **Visual Designer** | `brand-book.{en,ar}.md` §5 (per §6.5 above) | Colour tokens with WCAG AA contrast verification; type pairing rationale; logo concept brief; spacing scale. Text-level only in v1. | Signs the visual section. |
| **Copywriter (AR + EN)** | `voice-tone.md`, taglines (§7.1) | Do/don't pairs in BOTH languages; calibrates the formality↔warmth scale per surface; AR composed parallel, not translated. | Signs voice/tone parity and the tagline pair. |
| **Trademark Researcher** | Trademark notes embedded in `naming-shortlist.md` | SAIP register search; WHOIS check on `.sa`, `.com.sa`, `.com`; sanity-check line per candidate. **Disclaims clearance.** | Re-signs the **chosen** candidate at gate. Gate-blocking veto on an active SAIP collision in a relevant Nice class. |

---

## §9. Strategic gate — `gate-3-to-4.json`

Stage 3 ends at a **strategic** gate per T2 §2. Engagement owner writes `gates/gate-3-to-4.json` (path per T3 §3) with `decision_kind: "strategic"`. Approvers: engagement owner (NEXOURA partner) **and** client sponsor — both required. Name change at Stage 4 is expensive (architecture and integrations skin against the brand), so this gate hard-locks the chosen candidate.

### 9.1 Decision inputs

`artifacts_reviewed` carries the four §10 artifact paths. The approval prompt's `{{summary}}` is one paragraph synthesising: chosen name (EN + AR rendering), positioning one-line extract, tone register defaults, palette primary token, tagline pair, and an explicit line that the trademark check is a sanity check, not legal clearance.

### 9.2 Example payload (full schema in T2 §3)

```json
{
  "request_id": "9a3e7b2c-5d6f-4e8a-b1c7-2f4d9e0a5b6c",
  "status": "pending",
  "decision_kind": "strategic",
  "from_stage": "03-branding",
  "to_stage": "04-tech",
  "approvers_required": ["engagement_owner", "client_sponsor"],
  "approver": "omar@nexoura.ai",
  "decision": "GO",
  "channel": "cli-clarify",
  "timestamp": "2026-07-12T09:30:00Z",
  "rationale": "Name 'Nexa' (نِكسا) clears SAIP class 9/42 sanity check; positioning locks operations-cockpit wedge; voice/tone calibrated formal-warm at 2.5/4 EN, 3/4 AR with bilingual do/don't grid; palette + type pairing meet WCAG AA; tagline pair partner-approved.",
  "artifacts_reviewed": [
    "03-branding/brand-book.en.md", "03-branding/brand-book.ar.md",
    "03-branding/naming-shortlist.md", "03-branding/positioning.md",
    "03-branding/voice-tone.md"
  ],
  "conditions": [], "next_action": null
}
```

### 9.3 Bilingual prompt (Stage 3 instantiation of T2 §7.1)

Use the T2 §7.1 strategic template with `{{from_stage}}=03-branding`, `{{to_stage}}=04-tech`, `{{artifact_list}}` = the five §10 paths, and a `{{summary}}` paragraph carrying: chosen name (EN + AR), positioning one-liner, tone register defaults, palette primary token, tagline pair, and the sanity-check-not-clearance line.

English instantiation:

```text
GATE REQUEST — <slug>
Stage transition: 03-branding → 04-tech

Artifacts: 03-branding/{brand-book.en.md, brand-book.ar.md,
naming-shortlist.md, positioning.md, voice-tone.md}

Summary: Name "Nexa" (نِكسا); positioning locks the operations-cockpit wedge
for KSA SMB multi-branch retail; voice formal-warm 2.5/4 EN, 3/4 AR; palette
anchors on deep teal #0F4C5C; tagline "Every branch, one morning view." /
«كلّ الفروع، في لوحة صباح واحدة.» SAIP sanity-check clear class 9/42 — NOT
legal clearance; partner advises filing pre-Stage-4 spend.

Reply: GO | NO-GO | REVISE — plus a one-sentence rationale.
```

Arabic (KSA-formal register):

```text
طلب اعتماد بوابة — <slug>
الانتقال بين المراحل: 03-branding ← 04-tech

المخرجات: 03-branding/{brand-book.en.md, brand-book.ar.md,
naming-shortlist.md, positioning.md, voice-tone.md}

ملخّص تنفيذي: الاسم المعتمَد «نِكسا» (Nexa)؛ يُثبِّت بيانُ الموقعة وَتِدَ
منصّةِ التشغيل لقطاع التجزئة متعدّدة الفروع للمنشآت السعوديّة الصغيرة
والمتوسطة؛ السِّمت الرسميّ الودود عند 2.5/4 إنجليزيّاً و3/4 عربيّاً؛
لوحة الألوان تستند إلى الأخضر المُزرَقّ العميق #0F4C5C؛ الشعار التسويقيّ
«كلّ الفروع، في لوحة صباح واحدة.» الفحص المبدئيّ لدى الهيئة السعوديّة
للملكيّة الفكريّة خالٍ من التعارض في الفئتَين 9 و42؛ ولا يُغني عن
الاعتماد القانونيّ الرسميّ.

يُرجى الإفادة: GO | NO-GO | REVISE — مع مسوّغ مختصر في سطر مستقل.
```

### 9.4 Rejection paths

- **REVISE → `next_action: "rename"`** — chosen candidate hit a late SAIP collision or client veto; re-run §3 from the runner-up.
- **REVISE → `next_action: "retone"`** — voice misses the persona; re-run §5 with a new register target.
- **REVISE → `next_action: "revisual"`** — palette / type pairing rejected; re-run §6.5.
- **NO-GO** — rare; usually signals the PRD persona was wrong (route back to T7, not a Stage-3 internal re-run).

Commit per T3 §8: `gate: stage3 → stage4 APPROVED` (or `REVISE` / `BLOCKED`).

---

## §10. Output artifacts summary

All under `engagements/<slug>/03-branding/` unless noted (T3 §4):

| Path | Owner (§8) | Notes |
|------|------------|-------|
| `brand-book.en.md` | Brand Strategist | English brand-book; visual direction embedded as §5; T3 §5 parity with AR. |
| `brand-book.ar.md` | Brand Strategist | Arabic mirror, KSA-formal register, identical H2 order. |
| `naming-shortlist.md` | Naming Specialist | ≥ 5 candidates per §3; trademark notes inline; ≥ 1 candidate viable in BOTH AR and EN markets (kanban acceptance criterion). |
| `positioning.md` | Brand Strategist | One statement; EN + AR worked examples per §4. |
| `voice-tone.md` | Copywriter (AR + EN) | Formality/warmth scales + do/don't grids in BOTH languages (kanban acceptance criterion). |
| `../gates/gate-3-to-4.json` | Engagement owner | Strategic gate decision per T2 §3; placed under `gates/` per T3 §3, not under `03-branding/`. |

Stage is artifact-complete when all five `03-branding/` files exist and are non-empty, the two brand-book files have matching H2 section count, `naming-shortlist.md` has ≥ 5 candidates with ≥ 1 flagged `advance` viable in both languages, `voice-tone.md` carries do/don't pairs in both EN and AR, and `gate-3-to-4.json` parses against T2 §3.

---

## §11. Cross-references

- **T1 nexoura-engagement-lifecycle** — §3 (Stage 3 stub this skill expands), §6 (artifact layout — superseded by T3).
- **T2 nexoura-gate-protocol** — §3 (`gate.json` schema, `decision_kind: "strategic"`), §4 (advance / reject / revise vocabulary), §7.1 (bilingual strategic gate prompt; §9.3 above is the Stage-3 instantiation).
- **T3 nexoura-artifact-conventions** — §3 (`gates/` and `03-branding/` placement), §4 (per-stage required artifacts), §5 (`.en.md` / `.ar.md` parity contract for the brand-book pair), §8 (`stage3: …` and `gate: stage3 → stage4 …` commit grammar).
- **T7 nexoura-requirements-stage** — preceding stage; this skill's input is its output (`prd.en.md` + `prd.ar.md` with §4 personas, and `gates/gate-2-to-3.json` approved as GO).
- **T9 nexoura-tech-architecture** (forthcoming) — next stage; consumes brand-book palette and type tokens for UI scaffolding decisions, and the chosen name as the canonical product noun across `architecture.md` and ADRs.
- **T5 nexoura-bilingual-content** (deferred) — AR-first authoring rules, terminology glossary, KSA-formal register definition. Until T5 lands, §4–§7 above carry the bilingual contract inline.
