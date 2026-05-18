# NEXOURA AI Platform Specification

**Document version:** 1.3
**Date:** 2026-05-18
**Status:** Approved, ready for execution (Phase 1 closed, Phase 2 in progress)
**Operator:** APT WATCH (legal entity, Riyadh, Saudi Arabia)
**Platform:** NEXOURA AI
**License:** Proprietary (closed source)
**Owner:** Omar Alageel (GitHub: omar9988, uamgll@gmail.com)

---

## How to use this document

This is the canonical specification for the NEXOURA AI platform. It is self-contained — any AI assistant or human reading it without prior context should be able to understand the architecture, decisions, and execution plan.

If you are a new chat picking this up: read top-to-bottom once, then return to specific sections as needed. The execution plan is in §31. Changes since previous versions are in §37.

---

## 1. Executive Summary

NEXOURA AI is a proprietary AI-native platform operated by APT WATCH. It is built on top of a forked Hermes Agent runtime (NousResearch, MIT licensed) with NEXOURA's SaaS UI, plugins, profile configurations, custom skills, and brand assets remaining proprietary intellectual property of APT WATCH.

NEXOURA AI ships four products — STUDIO, WORK, ONE, and ENTERPRISE. STUDIO is the foundational product: a platform that builds AI-powered platforms. It is built first; the other three products (and any internal product like APT WATCH supply chain SaaS) are subsequently built BY Studio using Studio's lifecycle workflow.

**Core thesis:** Exponential speed via self-improving agents. Humans gate strategic decisions; agents do the work; agents continuously improve themselves through Hermes's autonomous skill creation and Curator-driven skill maintenance.

**Tagline:** *WHERE AI BUILDS*

**Build estimate:** Studio v1.0 in 8–10 weeks. First product output in 4–8 weeks after Studio. Revenue customer projection: Q4 2026.

---

## 2. License & Intellectual Property

### What's proprietary (NEXOURA AI — closed source)

- **NEXOURA SaaS layer** — Next.js application (chat UI, admin dashboards, Mission Control, project pages, customer portals, billing)
- **NEXOURA plugins** — Python plugins in `~/.hermes/plugins/` that extend the forked Hermes with NEXOURA-specific business logic
- **NEXOURA profile configurations** — All SOUL.md files, config.yaml settings, agent-specific personalities
- **Custom NEXOURA skills** — Any skills authored specifically for NEXOURA workflows
- **Brand assets** — NEXOURA name, logos, color palette, typography, design system, marketing materials, product names (STUDIO, WORK, ONE, ENTERPRISE)
- **Customer data** — All tenant data, conversations, deliverables, billing records
- **Domain expertise** — APT WATCH supply chain, Saudi compliance, NEXOURA enhancement workflow
- **Trajectory data** — All conversation/execution trajectories captured for fine-tuning APT WATCH local LLM

### What's used but not modified (Hermes — MIT licensed, our fork)

- Hermes Agent core (`run_agent.py`, agent runtime, tool calling loop)
- Hermes-bundled skills (kanban-orchestrator, kanban-worker, software-development, github, mcp, etc.)
- Hermes built-in tools (kanban, terminal, file, web, search, vision, video, etc.)
- Hermes Kanban coordination layer
- Hermes Curator (background skill maintenance)
- Hermes memory system (MEMORY.md, USER.md, session search, external providers)
- Hermes plugin system (we use it, but don't modify the system itself)
- Hermes messaging gateways (configure, don't fork)

### Contribution policy

- **Bug fixes to Hermes core:** May be contributed back upstream
- **Hermes-general improvements:** May be contributed back if non-strategic
- **NEXOURA-specific extensions:** Stay in our proprietary fork or `~/.hermes/plugins/`
- **Brand, product names, customer assets:** Never contributed, always proprietary

### Why fork instead of vendor

- Full control over deployment, versioning, and rollback
- Ability to apply security patches without waiting for upstream
- Selective merging of upstream improvements
- No dependency on a third party's release cadence
- Customer-facing brand (NEXOURA AI) is decoupled from the underlying open-source project

---

## 3. Brand & Identity

| Term | Meaning |
|---|---|
| **NEXOURA AI** | The platform brand (proprietary, closed source) |
| **APT WATCH** | The company name (legal entity that operates NEXOURA AI) |
| **STUDIO / WORK / ONE / ENTERPRISE** | The four products on the NEXOURA AI platform |
| **NEXOURA-1** | Future custom LLM, fine-tuned on NEXOURA trajectories, hosted by APT WATCH |

**Vision:** *To build the infrastructure layer where AI agents become active builders, operators, and collaborators in both business and everyday life.*

**Visual identity:** Each product shares NEXOURA umbrella tokens (color palette, typography, voice principles) and maintains distinct positioning for its audience segment. All visual identity is proprietary IP.

---

## 4. Product Architecture

### The four products

| Product | Tagline | Audience | What it does |
|---|---|---|---|
| **NEXOURA STUDIO** | Build AI-powered platforms | Startups, enterprises, product teams, builders | The factory — agents design, build, deploy complete platforms |
| **NEXOURA WORK** | Your AI workforce | Enterprises, operations, support, GRC, digital orgs | Hire, manage, orchestrate AI agents across the organization |
| **NEXOURA ONE** | AI for everyday life | Professionals, creators, entrepreneurs, individuals | Personal AI OS — assistants, scheduling, finance automation |
| **NEXOURA ENTERPRISE** | For large-scale impact | Banks, government, healthcare, industrial, regulated | Custom AI + dedicated infra + SOC2/ISO + private deployments + HUMAIN sovereign hosting for Saudi |

### The recursive build thesis

STUDIO is the platform that builds AI-powered platforms. Therefore:

- STUDIO is built first (manually scaffolded, then increasingly self-building as agents come online)
- WORK, ONE, ENTERPRISE are subsequent **outputs** of STUDIO, not separate codebases
- APT WATCH supply chain SaaS — if pursued — is also a Studio output

We build STUDIO once. Everything else flows through Studio's lifecycle workflow.

---

## 5. Vision & Mission

**Mission:** Eliminate the human bottleneck in building AI-powered software. AI agents handle requirements, branding, engineering, marketing, operations, and continuous improvement. Humans gate strategic decisions.

**Why this matters:** Current AI tooling treats agents as autocomplete or single-turn copilots. NEXOURA AI treats agents as autonomous teams that own products end-to-end, coordinated through verifiable handoffs. This unlocks exponential speed because agents improve themselves and other agents over time (Phase D self-improvement).

---

## 6. Product Lifecycle

Every product progresses through 8 stages across 4 phases.

### Phase A — BUILD (gated, linear)

| Stage | Name | Deliverable | Gate |
|---|---|---|---|
| **0** | Feasibility Study | Go/no-go PDF: TAM/SAM/SOM, 5-year P&L, technical complexity, risk register, competitive matrix, resource plan | PM approves go / kills idea |
| **1** | Requirements & Discovery | Product Requirements Brief | PM approves brief |
| **2** | Branding & Identity | Brand Book | PM approves brand |
| **3** | Technical Implementation | Working product (URL, repo, docs, runbook). Sub-stages: 3a Architecture, 3b Backend, 3c Frontend, 3d Integration, 3e Security audit, 3f QA | PM approves "ready to launch" |
| **4** | Marketing & Launch | Live marketing site, content library, campaigns | PM approves "live" |

### Phase B — OPERATE (continuous, parallel post-launch)

| Stage | Sub-track | Purpose |
|---|---|---|
| **5A** | Application Support | Bugs and user issues. Tiered L1/L2/L3 + Bug Triager |
| **5B** | Infrastructure | SRE monitoring, capacity, deployments, performance, on-call |
| **5C** | Security | Threat detection, incident response, forensics, compliance |
| **5D** | Customer-Facing | Customer Success, Support, Account Management — multi-channel |
| **5E** | Cross-Cutting | Maintenance, Documentation, Audit |
| **6** | Value Measurement | Revenue, costs, usage, customer insights, ROI per feature, forecasting |

### Phase C — EVOLVE (triggered, loops back)

Stage 7: Iteration & Growth — triggered by Stage 6 quarterly review OR customer enhancement workflow. Mini-lifecycle: Requirements lite → Tech → Marketing update.

### Phase D — SELF-IMPROVE (background, continuous)

- Hermes Curator: 7-day cycle grading skills
- Trajectory export → fine-tuning pipeline (feeds APT WATCH local LLM)
- Skill self-improvement during use
- Cross-product skill transfer
- Built on Hermes `hermes-agent-self-evolution` (GEPA/DSPy)

### Customer enhancement workflow

```
Customer raises enhancement request
   ↓
Stage 5D: customer-service profile captures, logs to Enhancement DB
   ↓
Enhancement Coordinator skill (loaded by researcher profile):
   - Classify, aggregate, financial+technical analysis
   ↓
Weekly review: product-lead-{slug}
   ↓
Human PM decision (Omar):
   REJECT | DEFER | QUICK FIX (Stage 5 hotfix) | FORK TO STAGE 7 (mini-lifecycle)
```

---

## 7. Agent Framework

### Foundation: Hermes Agent (forked)

- **Source:** `NousResearch/hermes-agent`
- **Our fork:** `omar-alageel-platform/nexoura-agent` (private)
- **License:** Hermes is MIT; our fork additions are proprietary NEXOURA IP
- **Runtime backends:** Modal (default, serverless), Daytona, Hetzner VPS, local Docker

### Profile + skill architecture

```
PROFILE = unit of isolation
  - Own SOUL.md (voice, anti-temptation rules, identity)
  - Own config.yaml (model, toolset, always-load skills)
  - Own memory (MEMORY.md, USER.md, session DB)
  - Own cron jobs, sessions, state.db
  - Own messaging gateway endpoint
  - Own terminal backend

SKILL = unit of capability
  - SKILL.md file with frontmatter (name, description, triggers, version)
  - Loaded on demand by any profile based on triggers
  - Hermes Curator maintains them
```

**Critical rule:** Most "roles" are skills, not profiles. A Financial Analyst is a SKILL any profile can load. A profile is only created when isolation is genuinely required (different toolset, model, SOUL voice, cron, or terminal backend).

### Director-Worker pattern

| Archetype | Auto-loaded skill | Behavior |
|---|---|---|
| **Director (Orchestrator)** | `kanban-orchestrator` | Decomposes work into Kanban tasks, assigns to Workers, verifies handoffs, NEVER executes implementation |
| **Worker (Executor)** | `kanban-worker` | Claims one task, executes with verifiable artifact, completes with structured metadata |

### Coordination via Kanban

Durable SQLite at `~/.hermes/kanban.db`. 15 verbs. Heartbeat-based zombie reclaim. Hallucination recovery. Workspace_path enforcement. Tenant scoping.

### Subagent delegation (delegate_task tool)

Beyond Kanban (durable + multi-agent), Hermes supports synchronous subagent delegation within a single agent turn. Up to 3 concurrent children by default. Roles: leaf (default) vs orchestrator. Not durable — for durable work use cronjob or `terminal(background=True)`.

---

## 8. Profile Roster

### Naming convention (Hermes-aligned, kebab-case)

All profile names use lowercase kebab-case. Hierarchy is encoded by function, not seniority. Per-product profiles use the product slug as suffix.

### Cross-product directors (always-on, instantiate as needed)

| Profile | Model | Terminal backend | Default skills |
|---|---|---|---|
| `product-director` | Opus 4.7 | Modal | kanban-orchestrator, decision-frameworks, strategic-planning, brainstorming |
| `architecture-director` | Opus 4.7 | Modal | kanban-orchestrator, software-architecture, system-design |
| `design-director` | Opus 4.7 | Modal | kanban-orchestrator, claude-design, taste-skill, design-md |
| `brand-director` | Opus 4.7 | Modal | kanban-orchestrator, brand-strategy, naming, voice-development |
| `marketing-director` | Opus 4.7 | Modal | kanban-orchestrator, marketing-strategy, SEO-research, growth |

**Spawning policy:** Don't auto-create all 5 at Phase 1. Spawn `product-director` first (most needed). Others come online when relevant work begins.

### Per-product directors (one triad per active product)

| Profile | Model | Terminal backend | When spawned |
|---|---|---|---|
| `product-lead-{slug}` | Sonnet 4.6 | Modal | Stage 0 of product lifecycle |
| `tech-lead-{slug}` | Sonnet 4.6 | Daytona (dev env) | Stage 1 of product lifecycle |
| `design-lead-{slug}` | Sonnet 4.6 | Modal | Stage 1 of product lifecycle |

For APT WATCH supply chain SaaS: `product-lead-apt-watch`, `tech-lead-apt-watch`, `design-lead-apt-watch`. For NEXOURA WORK: `product-lead-work`, `tech-lead-work`, `design-lead-work`.

### Workers (function-based, shared across products)

| Profile | Model | Terminal backend | Loads skills like |
|---|---|---|---|
| `builder` | Sonnet 4.6 | Daytona (full dev env) | github-pr-workflow, TDD, debug-python, engineering-backend-architect, engineering-frontend-architect, code-review, database-design, devops, security-test |
| `researcher` | Sonnet 4.6 | Modal | web-research, finance-financial-analyst, market-sizing, competitive-intel, risk-analysis, user-research, BA-requirements, enhancement-coordinator |
| `designer` | Sonnet 4.6 + Nano Banana | Modal | claude-design, taste-skill, design-md, brand-strategy, visual-design |
| `writer` | Sonnet 4.6 | Modal | copywriter, content-writer, SEO, marketing skills, humanizer, documentation |
| `reviewer` | Opus 4.7 + GPT-5 (dual) | Modal | code review, design QA, video_analyze, vision_analyze, accessibility-auditor, reality-checker |
| `customer-service` | Haiku 4.5 + Sonnet 4.6 (escalate) | Modal | customer-success, support-skills, customer-insights |
| `operator` | Haiku 4.5 | Modal (cron-driven) | SRE-monitoring, security-monitoring, audit, compliance-monitor, performance-optimization |
| `auditor` | Opus 4.7 | Modal | governance, compliance-auditor, security-audit |
| `domain-specialist-{slug}` | Provider varies by domain | Backend varies | Domain-specific skills (e.g., `domain-specialist-apt-watch` loads Arabic-content, PDPL-compliance, supply-chain-domain; uses HUMAIN ALLaM) |

### Notes

- **`operator` may split** into `sre` + `operator` when Stage 5 operations volume justifies the isolation (different cron schedules, different terminal backends, different model needs)
- **`reviewer` is a Hermes built-in archetype** — used for critical-task dual-LLM validation, code review, design QA
- **`auditor` is a Worker, not a Director** — it executes audits with verifiable artifacts, doesn't orchestrate
- **Multiple `domain-specialist-{slug}` profiles** can coexist (one per active domain)

### Agent-proposed profile expansion

When existing profiles can't cleanly handle a workload, the responsible Director profile proposes a new profile via PR review (committed to nexoura-agent fork). Approved profiles join the roster. No artificial cap — profiles cost nothing when idle (Hermes hibernation on Modal/Daytona).

---

## 9. Skill Strategy

### Adopt before authoring (priority order)

1. **Use bundled Hermes skills first** (70+ ship with Hermes; `hermes skills list`)
2. **Install proven community skill collections second**
3. **Author custom NEXOURA skills only when no equivalent exists**

### Community skill collections to install (Studio Stage 3a, Week 1)

| Repo | Coverage | Approx skills |
|---|---|---|
| `itgoyo/hermes-skills` | Finance, sales, marketing, testing, engineering, gaming, domain experts | 310+ |
| `Undermybelt/hermes-skills` | Security/DevOps heavy, automation, browser control | 900+ |
| `wondelai/skills` | Cross-platform skills library | 380+ |
| `obra/superpowers` | Software dev discipline (TDD, systematic-debugging, subagent-driven-development) | Curated set |
| `Leonxlnx/taste-skill` | Senior UI/UX engineer; design quality knobs | Variants |
| `blader/humanizer` | Strip AI-isms from generated copy | Single skill |
| `blader/Claudeception` | Sharpen Hermes's learning loop | Single skill |
| `kepano/obsidian-skills` | Read/write Obsidian vault | Pack |
| `aaron-he-zhu/seo-geo-claude-skills` | Full SEO/GEO lifecycle | 20 skills |

### Custom NEXOURA skills to author (proprietary)

- `humain-allam-wrapper` (if HUMAIN lacks native MCP)
- `nexoura-brand-voice` (umbrella voice across products)
- `apt-watch-supply-chain-domain` (when product is built)
- `nexoura-billing-rules` (multi-tenant SaaS billing)
- `nexoura-pdpl-compliance` (Saudi data protection)
- `nexoura-enhancement-coordinator` (customer enhancement triage)
- `nexoura-arabic-localization` (Arabic content workflows)

---

## 10. Memory Architecture

Hermes provides four layers of memory plus eight external providers. NEXOURA uses all of them strategically.

### Layer 1 — SOUL.md (personality, immutable per session)

- Defines profile's voice, identity, anti-temptation rules
- Loaded once at session start; frozen for the session (preserves prefix cache)
- Edited via git PRs to nexoura-agent fork

### Layer 2 — MEMORY.md (~2,200 chars, agent self-notes)

- Bounded, agent-curated
- Persists across sessions
- Stored in `~/.hermes/memories/`
- Injected into system prompt as frozen snapshot at session start
- When full, agent consolidates or replaces entries

### Layer 3 — USER.md (~1,375 chars, user profile)

- User-specific knowledge per profile
- Critical for multi-tenant SaaS — each customer gets their own USER.md per profile

### Layer 4 — Session history (SQLite + FTS5 full-text search)

- All past conversations stored locally, full-text indexed
- `session_search` tool queries weeks-old conversations

### External providers (NEXOURA recommendation: Honcho)

Hermes ships 8 external memory provider plugins:

| Provider | Strength | NEXOURA use |
|---|---|---|
| **Honcho** (default for customer-service) | AI-native dialectic reasoning, peer profiles per customer | Cross-session customer intelligence |
| **Mem0** | Simpler setup, knowledge graph | Lighter alternative |
| **Hindsight** | Replay-driven memory | RL training workflows |
| **Holographic** | Vector memory | Heavy semantic search |
| **RetainDB** | Structured retention | Compliance-driven memory |
| **ByteRover** | Code-context optimized | Engineering-heavy profiles |
| **Supermemory** | Cloud-hosted | Quick start |
| **OpenViking** | Self-hosted | On-prem requirement |

### NEXOURA memory strategy

| Profile | External provider |
|---|---|
| All profiles | Built-in (SOUL + MEMORY + USER + session search) |
| `customer-service` | + Honcho (cross-session customer intelligence, dialectic reasoning) |
| `builder` | + ByteRover (code-context optimization) |
| `domain-specialist-apt-watch` | + OpenViking self-hosted (sovereignty requirement) |

### Multi-agent peer profiles

When multiple profiles talk to the same customer (e.g., `customer-service` + `operator` during an incident), Honcho maintains separate peer profiles. Each peer sees only its own observations, preventing context cross-contamination.

---

## 11. Multi-LLM Strategy

### Provider matrix

| Tier | Provider | Use case |
|---|---|---|
| **Sovereign Arabic** | HUMAIN ALLaM 34B (via Groq/Watsonx/Azure) | NEXOURA ENTERPRISE Saudi customers, Arabic content, MENA, sovereignty workloads |
| **Sovereign / Custom** | APT WATCH local LLM (in development) | Internal NEXOURA workflows, NEXOURA-1 fine-tuned from trajectories |
| **Premium reasoning** | Anthropic Claude Opus 4.7 | Cross-product directors |
| **Premium execution** | Anthropic Sonnet 4.6 | Per-product directors + most workers |
| **Routine ops** | Anthropic Haiku 4.5 | customer-service tier 1, operator monitoring, triage |
| **Subscription proxy** | Claude Pro / ChatGPT Pro / SuperGrok | Personal subscription routing (v0.14+) for near-zero marginal cost on premium tier |
| **Alternative cloud** | OpenAI GPT-4o/5 | A/B testing, critical-task validation |
| **Multi-model router** | OpenRouter (200+ models) | Cost-optimized routing |
| **Specialized cloud** | Novita AI, NVIDIA NIM (Nemotron) | Specific workloads |
| **Local privacy** | LM Studio, Unsloth, Ollama | Customer data that cannot leave premises |
| **Image gen** | Nano Banana, FAL, Flux | Visual assets |
| **Vision** | Gemini (via OpenRouter) | Visual review, design QA |
| **Voice** | ElevenLabs, OpenAI TTS, Whisper local | Marketing audio, customer voice notes |

### Subscription proxy — cost optimization

Hermes v0.14+ ships a local subscription proxy. If APT WATCH already pays for Claude Pro ($200/month), cross-product directors can route through that subscription instead of API costs. Estimated savings: $30-200/month depending on usage.

### Per-task user override with agent recommendation

UI exposes a model picker per message with Auto mode:

- Auto (default): Agent recommends based on task complexity + budget state
- User can override: Opus, Sonnet, Haiku, HUMAIN ALLaM, APT WATCH local, Subscription proxy, Free tier
- Agent surfaces reasoning
- Budget-aware fallback when project approaches cap
- Free tier path: Groq free, OpenRouter free, local LM Studio

### Auxiliary models — per-task overrides (major cost lever)

Hermes ships **per-task model overrides** for side tasks. A profile can run Opus 4.7 for its main reasoning while routing every auxiliary task (image analysis, web summarization, compression, etc.) to a Haiku-class model. This is **the single largest cost lever in NEXOURA's economics**.

Hermes auxiliary task slots (each independently configurable via `auxiliary.<task>` in config.yaml):

| Auxiliary task | What it does | NEXOURA target model |
|---|---|---|
| `vision` | Image analysis (vision_analyze tool, browser screenshots) | Gemini 2.5 Flash via OpenRouter |
| `web_extract` | Page summarization for `web_extract` and `web_crawl` | Gemini 2.5 Flash via OpenRouter |
| `approval` | Smart approval classifier (`approvals.mode: smart`) | Haiku 4.5 |
| `compression` | Context compression when conversation exceeds threshold | Haiku 4.5 |
| `session_search` | Past session matching summarization | Haiku 4.5 |
| `skills_hub` | Skill matching and search | Haiku 4.5 |
| `mcp` | MCP tool dispatch routing | Haiku 4.5 |
| `triage_specifier` | Kanban triage spec expansion | Haiku 4.5 |

**Cost impact:** without auxiliary overrides, `product-director` running Opus 4.7 ($15/M input, $75/M output) would route vision tasks to Opus at $15/$75. With auxiliary override to Gemini Flash ($0.50/M input, $3/M output), the same vision task costs ~30x less. Across the 8 task slots, expected total cost reduction for cross-product directors: **70-85%** vs naive routing.

### Credential pool strategies (rate limit + failover)

Hermes supports multiple API keys per provider with rotation strategies:

| Strategy | Behavior | NEXOURA use |
|---|---|---|
| `fill_first` | Use first key until exhausted (default) | Default safe |
| `round_robin` | Cycle through keys evenly | Multiply effective rate limits |
| `least_used` | Pick least-used key | Balance load |
| `random` | Random pick | Anti-pattern detection in upstream |

Configured in config.yaml per provider:

```yaml
credential_pool_strategies:
  openrouter: round_robin    # 5 keys → 5x effective rate limit
  anthropic: least_used      # 2 keys → automatic failover + balancing
```

This lets NEXOURA buy 5x rate limit on OpenRouter without paying for an enterprise plan.

### Iteration budget pressure (automatic, no config needed)

Hermes auto-injects budget warnings into tool results at 70% (caution) and 90% (warning) of iteration budget. When the agent sees `[BUDGET WARNING: 81/90. Only 9 left. Respond NOW.]` in a tool result, it consolidates and delivers vs spinning forever. This is a built-in safeguard against runaway agent loops. We do NOT need to build a budget guardrail plugin.

### Critical-task validation (Hermes Reviewer archetype)

Critical tasks auto-spawn three Kanban tasks:
- Task A on Model 1 (e.g., Opus)
- Task B on Model 2 (e.g., GPT-5)
- Task C: `reviewer` profile reads both artifacts, picks/synthesizes

~10-15% of tasks qualify as critical. ~2.3x cost on those tasks.

---

## 12. Hermes API Server (Our Backend)

Critical architectural point: **NEXOURA does not need a custom backend.** Hermes ships an OpenAI-compatible API server that becomes NEXOURA's backend.

### Endpoints exposed

- `POST /v1/chat/completions` — Standard OpenAI-compatible chat
- `POST /v1/responses` — Structured response format
- `GET /api/jobs` + `POST /api/jobs` — REST cron job management
- `GET /api/sessions/{id}` — Session continuity

### Features

- Real-time tool progress streaming (v0.7+)
- SQLite-backed response persistence
- Idempotency-Key support (v0.5+)
- Session continuity via `X-Hermes-Session-Id` header
- CORS origin protection
- Field whitelists + input limits

### Implication for NEXOURA architecture

We do NOT need to write:
- Agent runtime code, tool dispatch, streaming infrastructure, session management, cron scheduling

We DO need to write:
- Multi-tenant routing (which profile for which customer)
- Billing instrumentation (track tokens per tenant)
- Auth bridge (NEXOURA user → Hermes session)
- UI layer (chat, dashboards, Mission Control)

**Code savings: ~10,000-15,000 lines of custom backend code we don't write.**

---

## 12.1. Hermes Capabilities We LEVERAGE vs NEXOURA Capabilities We BUILD

This section is the orienting principle. Before designing any NEXOURA feature, the question is always: **does Hermes already do this?** If yes, leverage it. If no, build it. Spec v1.3 is the result of doing this audit against Hermes v0.14 documentation.

### What Hermes ALREADY ships (we configure, not build)

| Capability | Hermes mechanism | Where in docs |
|---|---|---|
| **Profile isolation** (concurrent agents) | `hermes -p <name>` — each profile has own HERMES_HOME with config/SOUL/memory/sessions/cron/gateway | user-guide/profiles |
| **Identity injection** | `SOUL.md` = slot #1 in system prompt, replaces built-in identity | user-guide/features/personality |
| **Director-Worker delegation** | `delegate_task(tasks=[...], role="orchestrator"|"leaf")` with depth/concurrency caps | user-guide/features/delegation |
| **Kanban coordination** | `kanban_create`, `kanban_complete`, kanban-orchestrator + kanban-worker skills | user-guide/features/kanban |
| **8-task auxiliary model overrides** | `auxiliary.*` config for vision/web_extract/approval/compression/session_search/skills_hub/mcp/triage_specifier | user-guide/configuration |
| **Smart command approval** | `approvals.mode: smart` uses auxiliary LLM to classify risk | user-guide/configuration |
| **Iteration budget pressure** | Auto-injected warnings at 70%/90% of `agent.max_turns` | user-guide/configuration |
| **Credential pool rotation** | `credential_pool_strategies` for round-robin/least-used multi-key | user-guide/configuration |
| **PII redaction** | `privacy.redact_pii: true` hashes phone/user/chat IDs before LLM | user-guide/configuration |
| **Secret redaction** | `security.redact_secrets: true` strips API key patterns from tool output | user-guide/configuration |
| **Pre-execution security scan** | `security.tirith_enabled` scans terminal commands for danger | user-guide/configuration |
| **Website blocklist** | `security.website_blocklist` blocks domain patterns from web/browser tools | user-guide/configuration |
| **20 messaging gateways** | Built-in adapters: telegram/discord/slack/whatsapp/signal/matrix/mattermost/email/sms/dingtalk/feishu/wecom/weixin/bluebubbles/qqbot/yuanbao/homeassistant/webhook/api_server | user-guide/messaging |
| **Group session isolation** | `group_sessions_per_user: true` per-user sessions in shared chats | user-guide/sessions |
| **Cron first-class** | `~/.hermes/cron/` agent task scheduling with multiple formats, attached skills, multi-platform delivery | developer-guide/cron-internals |
| **Voice mode** | STT (Whisper/Groq/OpenAI/Mistral) + TTS (8 providers including free Edge) | user-guide/features/voice-mode |
| **MCP client** | Native MCP server integration with tool filtering | user-guide/features/mcp |
| **Trajectory export** | `batch_runner.py` exports ShareGPT format for fine-tuning training data | developer-guide/trajectory-format |
| **Plugin discovery** | Three paths: `~/.hermes/plugins/`, `.hermes/plugins/`, pip entry points | developer-guide/contributing |
| **Custom providers in YAML** | Define LLM providers in `config.yaml` `custom_providers` without writing plugin | user-guide/configuring-models |
| **Context engine swap** | `context.engine: lcm` swaps lossy compression for lossless | user-guide/configuration |
| **Quick commands** | Zero-token slash command shortcuts (exec or alias) | user-guide/configuration |
| **ACP IDE integration** | Stdio/JSON-RPC for VS Code, Zed, JetBrains | developer-guide/acp-internals |
| **Skill self-improvement** | Agent-curated memory + autonomous skill creation + skill self-improvement during use | user-guide/features/skills |
| **Session search via FTS5** | SQLite FTS5 full-text search across all past sessions | developer-guide/session-storage |
| **Honcho dialectic user modeling** | Built-in user-modeling memory provider | user-guide/features/memory-providers |
| **Subagent delegation depth** | `delegation.max_spawn_depth: 1-3`, `max_concurrent_children: 3` configurable | user-guide/features/delegation |
| **Per-platform display overrides** | `display.platforms.<name>.tool_progress` per-platform verbosity | user-guide/configuration |
| **Human delay** | `human_delay.mode: natural` for human-like response pacing | user-guide/configuration |

That's 27 capabilities NEXOURA does not need to build.

### What NEXOURA must BUILD (proprietary work)

| Capability | Why Hermes can't ship this | Where it lives |
|---|---|---|
| **Multi-tenancy** | Hermes is single-user. NEXOURA serves many customers concurrently | Plugin `nexoura-multi-tenant` |
| **Per-tenant billing** | Hermes has no concept of customer billing | Plugin `nexoura-billing` |
| **NEXOURA SaaS UI** | Hermes ships TUI + API server; we need a polished web UI | Next.js at platform-omae.vercel.app |
| **Mission Control dashboard** | Hermes ships per-session views; we need fleet/cost/per-product views | Next.js + plugin |
| **Stage gate workflow (product lifecycle)** | Hermes Smart Approvals covers command-level. Stage gates are different — they're 8-stage product lifecycle decisions (feasibility approval, PRD approval, etc.) | Plugin + Next.js UI |
| **12-category severity-routed notifications** | Hermes routes per-platform but doesn't do severity-based fanout across 4 tiers with quiet hours | Plugin `nexoura-notification-router` |
| **Customer enhancement workflow** | Hermes doesn't have a concept of "customer requests → triage → roadmap" | Plugin `nexoura-enhancement-router` |
| **HUMAIN ALLaM provider** | Possibly NOT needed as a plugin — HUMAIN is OpenAI-compatible and can be a `custom_providers` entry in config.yaml. To validate in Phase 2. | config.yaml (preferred) OR plugin if config.yaml insufficient |
| **APT WATCH local LLM provider** | Same as HUMAIN — likely `custom_providers` entry. Plugin only if config.yaml insufficient | config.yaml (preferred) |
| **NEXOURA-specific skills** | Domain skills for engagement lifecycle, gate protocol, artifact conventions, PDPL, bilingual content, plus 6 stage skills | `~/.hermes/skills/nexoura-*/` |
| **decision-frameworks skill** | Spec §8 lists as auto-loaded for product-director — does not exist in any community collection | `~/.hermes/skills/decision-frameworks/` |
| **strategic-planning skill** | Spec §8 lists as auto-loaded for product-director — does not exist in any community collection | `~/.hermes/skills/strategic-planning/` |

That's the complete proprietary build list. Everything else is Hermes configuration.

### Implication for spec v1.3

Compared to v1.2, the plugin count drops from **9 to 5** (see §13 revised). Skills to author drops by 2 (we recognized these are net-new authoring, not "use existing"). Phase 5 timeline likely shortens by 1-2 weeks because more "build" becomes "configure."

---

## 13. Plugin System (Our Primary Extension Point)

Hermes plugins live in `~/.hermes/plugins/`. Drop Python files there and Hermes loads them at startup. **No forking required.** This is where NEXOURA proprietary business logic lives.

### Plugin extension points

| Extension | What you can build |
|---|---|
| Custom tools | New tool functions agents can call |
| Custom commands | New `/command` handlers in chat |
| Hooks | Lifecycle event handlers |
| Dashboard tabs | New views in Hermes TUI |
| Gateway platforms | New messaging adapters |
| Provider backends | New LLM provider integrations |
| Image-generation backends | New image gen providers |
| Memory providers | New memory backends |
| Context engines | New context assembly strategies |

### NEXOURA plugins to build (proprietary — v1.3 revised, was 9 plugins in v1.2)

| Plugin | Purpose | Effort |
|---|---|---|
| `nexoura-multi-tenant` | Tenant isolation middleware, per-tenant RLS enforcement on Hermes API server. Routes incoming API calls to the right Hermes profile per customer. | 2-3 days |
| `nexoura-billing` | Per-tenant token tracking via `tool:after` hook, aggregates into Supabase, Stripe + Tap/HyperPay integration for KSA. | 3-4 days |
| `nexoura-notification-router` | Routes notifications across 12 categories × 4 severity tiers (CRITICAL/HIGH/MEDIUM/LOW) to WhatsApp/Slack/Teams/Email/SMS per user preferences. Implements quiet hours, weekend handling, acknowledgment escalation. Hermes' built-in messaging is per-platform; this adds severity-based fanout. | 2-3 days |
| `nexoura-enhancement-router` | Customer enhancement workflow: capture → triage → aggregate similar requests → financial/technical analysis → weekly review queue → Omar approval → fork into Stage 7 mini-lifecycle. | 2 days |
| `nexoura-stage-gate` | Stage gate approval flow for the 8-stage product lifecycle. Distinct from Hermes' Smart Approvals (which gates command-level dangerous ops). Stage gates are product-decision gates (Stage 0 feasibility go/no-go, PRD approval, branding approval, etc.). | 2 days |

**Total: ~11-14 days of plugin development. Was ~17-22 days in v1.2 — reduction of ~30-40% by recognizing Hermes built-ins.**

### Plugins dropped from v1.2 (reasons)

| Dropped plugin | v1.2 effort | Why dropped (v1.3) |
|---|---|---|
| `nexoura-humain-provider` | 1-2 days | HUMAIN ALLaM is OpenAI-compatible. Define as `custom_providers` entry in `config.yaml` (no plugin code). Validate in Phase 2. Re-add as plugin only if config.yaml proves insufficient. |
| `nexoura-apt-watch-llm` | 1-2 days | Same reasoning as HUMAIN. APT WATCH local LLM will be OpenAI-compatible (DeepSeek/Qwen base served by vLLM/Ollama). Config.yaml entry. |
| `nexoura-budget-guardrail` | 1 day | Hermes ships `agent.max_turns` iteration budget pressure + `credential_pool_strategies` for rate limit handling. Cost tracking is covered by `nexoura-billing` plugin via `tool:after` hook. Pre-execution budget check still useful but no longer a separate plugin — it becomes a feature of `nexoura-billing`. |
| `nexoura-pii-redaction` | 1-2 days | Hermes ships `privacy.redact_pii: true` (hashes phone/user/chat IDs) + `security.redact_secrets: true` (strips API key patterns). Together these cover most PDPL requirements. NEXOURA-specific additions (Saudi National ID redaction, IBAN format) can be a small addition to `nexoura-multi-tenant` or a tiny standalone (~0.5 day if needed). |

---

## 14. Hooks System

Hermes has an event-driven hooks system for cross-cutting concerns.

### Gateway hooks (currently outbound)

| Event | When it fires | NEXOURA use |
|---|---|---|
| `agent:start` | Agent run begins | Log to audit, check budget |
| `agent:end` | Agent run completes | Track token usage |
| `session:reset` | Session cleared | Audit log |
| `command:*` | Any /command | Track command usage |
| `tool:before` | Before tool execution | Budget pre-check, redaction |
| `tool:after` | After tool execution | Result audit |
| `error:*` | Errors | Sentry alert + outbound notification |

### Plugin hooks

- Tool wrapping (pre-execution validation, post-execution logging)
- Metric collection (Datadog/PostHog integration)
- Guardrails (block dangerous operations)

### NEXOURA hook strategy

1. **Audit hook on every agent:start/end** → writes to Supabase audit_log
2. **Budget guardrail on tool:before** → blocks if tenant over cap
3. **PII redaction on tool:before** → scans for credit cards, Saudi national IDs
4. **Cost tracking on tool:after** → records token usage per tenant
5. **Notification trigger on error:*** → routes to appropriate channel (see §20)
6. **Stage gate approval trigger** → notifies Omar via preferred channel

---

## 15. Toolsets (Per-Profile Assignment)

Hermes ships these toolsets. Each can be enabled/disabled per profile per platform.

### Available toolsets

`browser, clarify, code_execution, cronjob, debugging, delegation, file, image_gen, kanban, memory, messaging, moa, rl, safe, search, session_search, skills, terminal, todo, tts, video, vision, web` + platform-specific (`discord, feishu_doc, homeassistant, spotify, yuanbao`)

### Toolset assignment per NEXOURA profile

| Profile | Enabled toolsets |
|---|---|
| `product-director` | kanban (orchestrator), memory, delegation, clarify, web, search, session_search, skills, messaging |
| `architecture-director` | kanban (orchestrator), memory, delegation, file, web, search, session_search, skills, messaging |
| `design-director` | kanban (orchestrator), memory, delegation, vision, image_gen, web, search, skills, messaging |
| `brand-director` | kanban (orchestrator), memory, delegation, image_gen, web, search, skills, messaging |
| `marketing-director` | kanban (orchestrator), memory, delegation, web, search, skills, messaging |
| `product-lead-{slug}` | kanban (orchestrator), memory, delegation, clarify, messaging, todo, skills |
| `tech-lead-{slug}` | kanban (orchestrator), memory, delegation, file, terminal, code_execution, skills |
| `design-lead-{slug}` | kanban (orchestrator), memory, image_gen, vision, skills |
| `builder` | kanban (worker), file, terminal, code_execution, debugging, web, search, skills |
| `researcher` | kanban (worker), web, search, browser, file, memory, vision, skills |
| `designer` | kanban (worker), image_gen, vision, file, browser, skills |
| `writer` | kanban (worker), file, web, search, skills, memory |
| `reviewer` | kanban (worker), video, vision, file, terminal, code_execution, delegation, skills |
| `customer-service` | kanban (worker), messaging, memory, tts, session_search, skills |
| `operator` | kanban (worker), cronjob, terminal, web, messaging, skills |
| `auditor` | kanban (worker), memory, file, web, search, session_search, skills |
| `domain-specialist-{slug}` | kanban (worker), file, web, search, memory, skills (+ domain-specific MCPs) |

**Security note:** `customer-service` and `researcher` do NOT get `code_execution` or `terminal`. Only `builder`, `tech-lead-{slug}`, `operator`, and `reviewer` (for testing) get full code execution. This is principle-of-least-privilege at the toolset layer.

---

## 16. Batch Processing & Self-Evolution

### Batch processing (for fine-tuning data)

```bash
hermes batch --input prompts.jsonl --profile builder --output trajectories.jsonl
```

Every agent run generates a trajectory. Batched + filtered + scored = training data for NEXOURA-1.

### Self-evolution pipeline (hermes-agent-self-evolution)

Built on DSPy + GEPA (Genetic-Pareto Prompt Evolution):

1. **Trajectory capture** — every agent run writes ShareGPT-format trajectory
2. **Quality scoring** — `auditor` + `reviewer` profiles grade trajectories
3. **Filtering** — successful trajectories selected for training
4. **GEPA optimization** — prompt evolution finds better prompts based on outcomes
5. **Fine-tuning** — periodic training run on DeepSeek/Qwen base produces NEXOURA-1
6. **Deployment** — NEXOURA-1 added to provider pool

### Skill self-improvement during use

- Agent identifies skill gap during execution
- Skill self-improvement plugin proposes patch
- Patch committed to nexoura-agent fork via PR
- Human reviews, approves merge
- Improved skill available to all profiles next session

### Curator (background skill maintenance)

7-day cycle: Reviews all agent-created skills. Grades by usage frequency + outcome quality. States: active → stale → archived. Archives recoverable (never deleted).

---

## 17. MCP Ecosystem

### Principle (D13)

For every external integration, use existing public MCP servers via `hermes mcp install` (OAuth 2.1 PKCE for remote MCPs). Build custom MCPs only when no public equivalent exists.

### Categories of MCPs to enable

| Category | Examples |
|---|---|
| Source control | GitHub, GitLab, Bitbucket |
| Project management | Linear, Jira, Asana, Notion, Confluence, Trello, ClickUp |
| Communication | Slack, Discord, Microsoft Teams, Telegram, WhatsApp, Email |
| Cloud platforms | AWS, GCP, Azure, Cloudflare, Vercel, Netlify |
| Databases | Postgres, MySQL, MongoDB, Supabase, Redis, Pinecone, Weaviate |
| Design | Figma, Sketch, Canva |
| Payments | Stripe, Square, PayPal, Tap (Saudi), HyperPay (Saudi) |
| Analytics | PostHog, Mixpanel, Segment, Amplitude |
| Marketing | Mailchimp, SendGrid, HubSpot, Customer.io, Resend |
| Sales/CRM | Salesforce, HubSpot, Pipedrive, Close |
| Customer support | Zendesk, Intercom, Front, Help Scout |
| Code execution | Replit, E2B, Modal, Daytona, Vercel Sandbox |
| Browser automation | Playwright, Browserbase, Puppeteer, Stagehand |
| Filesystem | S3, Google Drive, Dropbox, OneDrive, R2 |
| Monitoring | Sentry, DataDog, New Relic, PagerDuty, Grafana |
| Search | Brave, Tavily, Perplexity, Serper, Exa |
| Knowledge | Notion, Confluence, Google Docs, Obsidian, GitBook |
| Calendar | Google Calendar, Outlook, Calendly, Cal.com |
| Voice | ElevenLabs, OpenAI TTS, Whisper, Deepgram, Cartesia |
| Image/video | ComfyUI, Replicate, FAL, Runway, Luma |

Plus the Anthropic MCP marketplace and `awesome-mcp-servers` — hundreds available.

---

## 18. UI & Transparency Principles

### Core principle

Silent agents are forbidden by SOUL.md. Every tool call, decision point, thinking step gets surfaced. Bad outputs are okay; opaque outputs are not.

### Three connected views

**View 1: Chat (per project, agent thinking visible)**
- Streaming reasoning + tool calls inline
- Per-message model picker with Auto recommendation
- "Show full reasoning" toggle, Replay button

**View 2: Mission Control Dashboard (live operations map)**
- Fleet view: profile status dots (green=idle, blue=working, yellow=blocked, red=error)
- Data flow visualization (React Flow + D3)
- Activity feed (live event stream)
- Code/PR sidebar with CI status

**View 3: Per-product dashboard (stage gate view)**
- Stage progress bars (0-7)
- Active agents
- Next gate + approval button
- Budget burn chart, customer pipeline, value reports

### Tech stack

| Need | Tool |
|---|---|
| Real-time streaming | SSE from Hermes API → Next.js → browser |
| Animations | Framer Motion |
| Data flow diagrams | React Flow + D3.js |
| Charts | Recharts |
| Live editor view | Monaco Editor |
| RTL Arabic support | next-intl + Tailwind RTL plugin |

### Chat UI base

Fork open-webui (40k+ stars) or LobeChat (50k+ stars) and apply NEXOURA brand.

### ACP for IDE integration (optional)

Hermes ACP connects profiles to IDEs (VS Code, Zed, JetBrains). Enable when team grows and engineers want `builder` + `reviewer` available inside their IDE.

---

## 19. Multi-Channel Messaging (Inbound + Gateway Config)

### Hermes built-in gateways (24 platforms as of v0.14)

Customer-facing inbound messaging. The `customer-service` profile (and others when needed) receives messages via these gateways.

| Channel | NEXOURA priority | Customer segment |
|---|---|---|
| **Slack** | HIGH | Internal team, B2B customer ops |
| **Microsoft Teams** | HIGH | Enterprise customers |
| **WhatsApp** | HIGH | MENA region customer-facing |
| **BlueBubbles (iMessage)** | HIGH | Saudi/MENA premium customers (iPhone-heavy) |
| **Email (Resend/SMTP, IMAP)** | HIGH | All customers |
| **Telegram** | MEDIUM | Alt customer channel |
| **SMS (Twilio)** | MEDIUM | Urgent notifications |
| **Google Chat** | MEDIUM | Workspace customers |
| **Discord** | LOW | Only if community |
| **Signal** | LOW | Privacy-conscious customers |
| **DingTalk, Feishu/Lark, WeCom, Weixin, QQBot, Yuanbao** | LOW | Only if expanding into Chinese markets |
| **LINE** | LOW | Japan/Thailand expansion |
| **SimpleX Chat, Matrix, Mattermost, IRC** | NICHE | Specific customers |
| **Home Assistant** | If NEXOURA ONE smart home integration | — |
| **Webhook (generic)** | HIGH | Any custom integration |

### How agents use inbound messaging

- `customer-service` profile receives customer messages, routes through Kanban for escalation
- Voice memo transcription via Whisper STT (Hermes built-in)
- Cross-platform conversation continuity built into Hermes — same conversation context across channels
- Customer can write in Arabic on WhatsApp → `customer-service` loads HUMAIN ALLaM → responds in Arabic
- Complex tickets escalate to `support-engineer` (a skill loaded by customer-service) or to human via notification

### Pairing system for security

```bash
hermes pairing approve <platform> <code>
hermes pairing revoke <platform> <user-id>
```

Prevents random strangers from talking to our gateway. Customer onboarding flow: customer requests access → gets pairing code → admin approves.

---

## 20. Notifications & Alerts (Outbound)

This section covers notifications FROM the platform TO Omar (and future team) — distinct from inbound customer messaging in §19. NEXOURA AI uses the same Hermes messaging gateways but for outbound notifications and alerts.

### Notification categories

| Category | Trigger | Severity | Default channel |
|---|---|---|---|
| **Stage gate approval needed** | Director completes a stage deliverable | HIGH | WhatsApp + email |
| **Budget alert** | Project at 80% / 100% of monthly cap | HIGH at 100%, MEDIUM at 80% | Slack + email |
| **Critical incident** | P0 production issue, security breach | CRITICAL | WhatsApp + SMS + Slack |
| **Customer escalation** | `customer-service` can't resolve | HIGH | WhatsApp + Slack |
| **Failed agent task** | Worker fails after retries | MEDIUM | Slack |
| **Daily digest** | End of day summary | LOW | Email (08:00 next day) |
| **Weekly Product Value Report** | Monday morning | LOW | Email + Slack |
| **PR awaiting review** | Builder opens a PR | MEDIUM | Slack (with link) |
| **Skill drift detected** | Curator finds suspect skill behavior | MEDIUM | Slack |
| **Customer signed up** | New tenant onboarded | LOW | Slack (celebrate!) |
| **Payment received / failed** | Billing event | MEDIUM | Slack + email |
| **Trajectory training run complete** | NEXOURA-1 fine-tuning batch finished | LOW | Email |

### Channel routing matrix

| Severity | Channels (in order) | Why |
|---|---|---|
| **CRITICAL** | WhatsApp + SMS + Slack + Email | Multi-channel redundancy, hard to miss |
| **HIGH** | WhatsApp + Slack + Email | Likely to be seen quickly |
| **MEDIUM** | Slack + Email | Standard work-hours channels |
| **LOW** | Email only | Doesn't interrupt; reviewed when convenient |

### Routing rules

1. **Quiet hours:** 22:00 - 07:00 Riyadh time. Only CRITICAL pierces quiet hours; HIGH and below are queued and delivered at 08:00.
2. **Weekend handling:** Weekends (Friday-Saturday in Saudi context) treated as extended quiet hours for MEDIUM/LOW. CRITICAL and HIGH always go through.
3. **Acknowledgment escalation:** If CRITICAL not acknowledged within 15 min, escalate to second contact (future: when team exists). If HIGH not acknowledged within 4 hours, downgrade to MEDIUM (assume seen).
4. **Channel preferences:** Each user (Omar + future team) can override defaults via settings UI.
5. **Batching:** Notifications below MEDIUM severity batched into morning digest (rather than 50 individual pings).
6. **Per-product subscription:** Future team members can subscribe to notifications for specific products only.

### Hermes mechanism: webhook direct-delivery vs gateway send

Hermes supports two notification mechanisms:

**Webhook direct-delivery (zero-LLM cost):**
- Triggered by hooks (e.g., budget threshold crossed)
- No agent involved; raw payload sent to webhook endpoint
- Endpoint (NEXOURA Next.js) forwards to messaging gateway
- Cheapest option — used for routine alerts

**Gateway send (LLM-composed message):**
- An agent (typically `operator` or `customer-service`) composes a contextual message
- Sent via Hermes gateway (Slack, WhatsApp, etc.)
- More expensive (uses LLM tokens) but human-friendly phrasing
- Used for incident summaries, weekly reports, customer-facing communications

### NEXOURA notification router plugin

We build `nexoura-notification-router` (proprietary plugin, ~2-3 days):

- Receives notification events from hooks across the platform
- Looks up user preferences for routing (from Supabase `notification_preferences` table)
- Applies quiet hours and severity routing
- Dispatches to appropriate Hermes gateway
- Tracks delivery status (sent/delivered/acknowledged)
- Implements escalation timers

### Examples

**Stage gate approval needed:**
```
WhatsApp message to Omar:
  🚦 NEXOURA Studio — Stage 1 ready for review
  Project: APT Watch Supply Chain SaaS
  Deliverable: Product Requirements Brief (12 pages)
  Open: https://app.nexoura.ai/projects/apt-watch/stage/1
  Reply APPROVE / REJECT / FEEDBACK
```

**Budget alert (80% threshold):**
```
Slack message:
  ⚠️ Budget alert — Project nexoura-work
  Spent: $159 / $200 monthly cap (79.5%)
  Burn rate: $5.2/day
  At current rate, will exceed cap on day 26
  Active profiles: product-lead-work, tech-lead-work, builder
  Action: Review or adjust cap
```

**Critical incident:**
```
WhatsApp + SMS + Slack:
  🚨 CRITICAL — NEXOURA Work Production Down
  Error: Hermes API server unresponsive (Modal)
  Started: 14:23 UTC (3 min ago)
  Affected: 12 customers, all WORK product
  operator agent triaging now
  Reply ACK to acknowledge
```

### Per-user notification preferences

Stored in Supabase `notification_preferences` table:

```
user_id | category | channels (json) | quiet_hours_override | enabled
omar    | stage-gate | ["whatsapp", "email"] | null | true
omar    | budget-alert | ["slack", "whatsapp"] | null | true
omar    | critical | ["whatsapp", "sms", "slack"] | { override: true } | true
omar    | daily-digest | ["email"] | null | true
```

UI in NEXOURA admin: `/settings/notifications` — toggle channels per category, set quiet hours, test delivery.

### Customer-side notifications (Stage 5+ products)

When NEXOURA products are operating (Stage 5), their CUSTOMERS also get notifications. Same architecture, just scoped per tenant:

- Each tenant has their own notification preferences
- Channel choices depend on which NEXOURA product (WORK might default to Slack, ONE might default to push notifications)
- Per-tenant rate limiting prevents notification storms
- Per-tenant audit log of all sent notifications

---

## 21. Infrastructure

### Architecture diagram

```
                  Customers (browsers, mobile, APIs, messaging)
                              ↓ HTTPS
                  ┌───────────────────────────┐
                  │  Cloudflare (DDoS, CDN)   │
                  └───────────┬───────────────┘
                              ↓
                  ┌───────────────────────────┐
                  │  Vercel (Next.js app)     │
                  │  - NEXOURA chat UI        │
                  │  - Admin / Mission Ctrl   │
                  │  - SaaS API routes        │
                  │  - Auth bridge            │
                  │  - Multi-tenant routing   │
                  │  - Notification router    │
                  └───────┬───────────────────┘
                          ↓ /v1/chat/completions
                  ┌───────────────────────────┐
                  │  Hermes API Server        │
                  │  (Modal serverless)       │
                  │  - 13+ profiles           │
                  │  - Kanban (SQLite)        │
                  │  - Curator (cron)         │
                  │  - 24 messaging gateways  │
                  │  - Plugin layer (NEXOURA) │
                  └───────┬───────────────────┘
                          ↓
        ┌─────────────────┼─────────────────┐
        ↓                 ↓                 ↓
   ┌────────┐      ┌───────────┐      ┌──────────────┐
   │Supabase│      │Cloudflare │      │External APIs:│
   │Postgres│      │R2 (back- │      │HUMAIN ALLaM  │
   │+ Auth  │      │ups +      │      │Anthropic     │
   │+Storage│      │trajec.)   │      │OpenAI        │
   └────────┘      └───────────┘      │OpenRouter    │
                                       │MCP servers   │
                                       │APT WATCH LLM │
                                       └──────────────┘
```

### Terminal backends (7 options, per profile)

| Backend | When to use | Cost |
|---|---|---|
| **Modal** (default) | Most profiles, serverless | $0 idle, ~$0.10-0.30/active hour |
| **Daytona** | `builder`, `tech-lead-{slug}` (full dev env) | $5-20/month per workspace |
| **Hetzner VPS** | Always-on heavy workloads | $5-15/month flat |
| **Vercel Sandbox** | Lightweight code execution | Pay per invocation |
| **Docker (local)** | Development, testing | Free |
| **SSH** | Custom hardware | Variable |
| **Singularity** | HPC/GPU workloads (future fine-tuning) | Variable |

### Components

| Component | Purpose | Status |
|---|---|---|
| Vercel | Next.js UI + auth bridge + multi-tenant routing + notification router | Existing |
| Modal | Hermes API server runtime | NEW |
| Supabase | Auth + user data + projects + audit logs + billing | Existing |
| Cloudflare R2 | Backups + trajectory storage | Existing |
| Cloudflare | DDoS, CDN | NEW |
| Sentry | Error tracking | Configured |
| Resend | Transactional email | Existing |
| Stripe | International billing | NEW |
| Tap / HyperPay | Saudi/MENA billing | NEW |
| Future: GPU instance | Fine-tuning NEXOURA-1 | When trajectory volume justifies |

### Estimated infrastructure cost (v1.3 — actual numbers from Phase 2)

| State | Monthly cost | Notes |
|---|---|---|
| Phase 2 (current) — Hermes API on Hetzner Falkenstein via Zeabur | $16 infra + ~$20 API = **$36** | Zeabur-managed Hetzner $16/mo VPS |
| 1 product in Stage 3 active build | $16 infra + ~$100 API = $116 | API cost dominated by builder profile |
| Studio + 1 product Stage 3 + 1 product Stage 5 ops | $16-30 infra + ~$200 API = $216-230 | May add second Hetzner instance for product isolation |
| 3 products in operations + 1 building (success state) | $30-50 infra + ~$300-500 API = $330-550 | Per-product Zeabur deployments may be needed |
| Enterprise customer demanding sovereign hosting | +$50-200 KSA infra | STC Cloud / Oracle Jeddah / Google Dammam for that customer |

Auxiliary cost reductions vs naive routing: **70-85%** on directors (Opus 4.7 for main, Haiku 4.5 for 8 auxiliary tasks). Subscription proxy (Claude Pro) can further reduce: subtract $30-200/month.

**Modal:** kept on free Hobby tier ($30/mo compute credit free) for Phase 3+ agent terminal-backend sandboxes. Not used for API server hosting.

---

## 21.5. Phase 2 Deployment Record

This subsection captures the actual Phase 2 deployment decision so future spec versions can trace the reasoning.

### Decision: Zeabur-managed Hetzner Falkenstein VPS, $16/mo

**Date:** 2026-05-18

**Alternatives considered:**

| Option | Cost | Verdict |
|---|---|---|
| Modal serverless (custom wrapper) | ~$5-30/mo | Rejected: Modal lacks built-in Hermes API server deploy. Custom wrapper = ~100 LOC + ongoing maintenance. Modal's sweet spot is sandboxes, not API hosting. |
| AWS EC2 (t3.xlarge equivalent) | $200-450/mo | Rejected: 10-20x cost premium for capabilities we don't need yet. Egress is the killer ($260/mo for 3TB). Re-evaluate Phase 7 when enterprise customers demand it. |
| Google Cloud Compute | $150-400/mo | Rejected: same reasoning as AWS. |
| DigitalOcean / Linode standard | $24-48/mo | Rejected: 1.5-3x Hetzner cost for similar specs, less bandwidth headroom. |
| Hetzner direct (DIY) | $16/mo + setup time | Rejected: same hardware cost but ~4-8 hrs DIY deployment work vs Zeabur one-click. Zeabur saves time at zero premium. |
| **Zeabur-managed Hetzner Falkenstein, DE** | **$16/mo** | **Selected** ✓ |

**Why Hetzner Falkenstein specifically:**
- $16/mo for 4 vCPU / 8 GB RAM / 160 GB SSD / 20 TB egress — best $/spec ratio in Zeabur marketplace
- ~80-100ms latency to Riyadh (Germany has excellent MENA connectivity)
- Hetzner reputation for reliability at this price tier (Plausible Analytics, many indie SaaS use Hetzner extensively)
- GDPR jurisdiction = good privacy posture, complements PDPL stance
- 20 TB egress (vs AWS-priced $0.09/GB) means no bandwidth anxiety

**Why Zeabur orchestrator on top:**
- One-click Hermes deployment template (RTWI4O)
- Manages Docker image pull, env vars, SSL, restart, monitoring
- Files tab edits `config.yaml` / `SOUL.md` / `.env` without SSH
- We're not locked in — can move Docker image to bare Hetzner or another host later

**Image used:** `nousresearch/hermes-agent:v2026.4.30` (upstream — see constraint below)

### Constraint: upstream image, not our fork (deferred to Phase 4)

The Zeabur template deploys the upstream `nousresearch/hermes-agent` Docker image. This violates our runtime independence principle (D14) — strictly we want our fork running in production.

**Why OK for Phase 2:** we have not yet modified Hermes source code. Our fork is identical to upstream at the code level. The only NEW thing we've added is `PHASE1-KANBAN-SPEC.md` which is data, not code. The deployed runtime behaves identically.

**When we revisit (Phase 4-5):** when we start adding NEXOURA plugins (`nexoura-multi-tenant`, `nexoura-billing`, etc.), the upstream image won't include them. Options:

| Option | Effort | Pros / Cons |
|---|---|---|
| α. Build custom Docker image from our fork, push to GHCR | 1 day | Full control; ~4-5 GB image; per-deploy rebuild needed |
| β. Use Zeabur "Deploy from Git" instead of template | 0.5 day | Zeabur builds from our fork; slower deploys; same final result |
| γ. Move from Zeabur to bare Hetzner with Docker Compose | 1-2 days | Full control; manage SSL/monitoring ourselves |

Decision deferred to Phase 4. Option β is the leading candidate.

### Modal subscription downgrade plan

You signed up for Modal Team ($250/mo) before pivoting to Zeabur. After Phase 2 verification:
- **Downgrade Modal to Free Hobby tier** ($0/mo, $30 free compute credit each month)
- Modal stays in toolkit for Phase 3+ as agent terminal-backend sandboxes (`tools/environments/modal.py` — its actual sweet spot)
- Re-upgrade only if Phase 5 heavy workloads or Phase 7 GPU compute require it

### Phase 2 deployment env vars (Zeabur)

Required at deploy time:
- `OPENROUTER_API_KEY` — from local `~/.hermes/.env`

Configured post-deploy via Zeabur env vars UI, restart required:
- `ANTHROPIC_API_KEY`
- `GITHUB_TOKEN`

Optional, added when needed:
- `TELEGRAM_BOT_TOKEN` (Phase 4 messaging)
- `SLACK_BOT_TOKEN` (Phase 4 messaging)
- `WHATSAPP_*` (Phase 4 messaging)
- `HUMAIN_API_KEY` (Phase 5 customer)
- `TAVILY_API_KEY` / `EXA_API_KEY` (Phase 5 researcher)
- `FAL_KEY` (Phase 5 designer)
- `ELEVENLABS_API_KEY` (Phase 6 marketing voice)

### Phase 2 acceptance criteria

Phase 2 is closed when ALL of:
1. ✅ Modal account created (done before pivot)
2. ✅ Zeabur account created
3. ⏳ Hetzner Falkenstein server provisioned via Zeabur
4. ⏳ Hermes deployed via Zeabur template, status: Running
5. ⏳ Public HTTPS endpoint returns Hermes response to curl test
6. ⏳ All 3 API keys configured in Zeabur (Anthropic, OpenRouter, GitHub)
7. ⏳ Modal downgraded to Free Hobby tier
8. ⏳ Spec v1.3 committed to fork as decision record

---

## 22. Security Baseline

### Hermes built-in security (v1.3 updated with v0.14 specifics)

| Capability | Hermes config | Notes |
|---|---|---|
| PII redaction (gateway) | `privacy.redact_pii: true` | Hashes phone numbers, user IDs, chat IDs before LLM. WhatsApp/Signal/Telegram supported. |
| Secret redaction (logs + context) | `security.redact_secrets: true` | Strips API key patterns from tool output and logs. Off by default — turn on for production. |
| Pre-execution command scanning | `security.tirith_enabled: true` | Tirith scans terminal commands for danger patterns. `tirith_fail_open: false` to block on scan failure. |
| Smart command approval | `approvals.mode: smart` | Auxiliary LLM classifies risk on dangerous commands. Low-risk = auto-approve with session persistence. High-risk = escalate to user. |
| Website blocklist | `security.website_blocklist.enabled: true` | Block domain patterns from web/browser tools. Wildcard support: `*.internal.example.com`. Cached 30s. |
| Background skill content scan | (always on) | Prompt injection patterns scanned in assembled skill content |
| TOCTOU closure | (always on) | Auth.json access serialized |
| OAuth isolation | (always on) | Per-provider token validation |
| Secret storage | `~/.hermes/.env` + OS keyring | macOS Keychain → ~/.hermes/.env → env vars precedence |
| Tool guardrails | (always on) | `ToolCallGuardrailController` pre-execution validation |
| Workspace isolation | `hermes -p <name>` | Each profile confined to own HERMES_HOME |
| Audit logging | (always on) | Centralized via `hermes_logging` |
| RBAC via profiles | (always on) | Each profile has own toolset/skill/credential isolation |
| Bedrock Guardrails | provider-specific | For ENTERPRISE customers on AWS Bedrock |
| Anti-temptation rules | `SOUL.md` | Behavioral guardrails authored in profile identity |
| Heartbeat / zombie reclaim | (always on in Kanban) | Stuck workers reclaimed automatically |
| Hallucination recovery | (always on in Kanban) | Workers flagged ⚠ when output suspect |
| Credential pool rotation | `credential_pool_strategies` | Multiple keys per provider with `round_robin` / `least_used` |
| File mutation verifier | `display.file_mutation_verifier: true` (default) | Advisory footer when write_file/patch failed silently |
| Iteration budget pressure | `agent.max_turns: 90` | Auto-warnings at 70% and 90% to prevent runaway loops |
| Container backends | `terminal.backend: docker` (or modal/daytona/vercel_sandbox/singularity) | 7 options for sandboxed code execution |

**Phase 2 stance:** Hermes built-ins cover most of the security baseline. We turn on `redact_pii`, `redact_secrets`, `tirith_enabled`, and `approvals.mode: smart` from day one.

### NEXOURA SaaS-layer security additions

| Layer | What we add |
|---|---|
| Authentication | Supabase Auth + MFA + SSO for Enterprise |
| RBAC | Owner / Admin / Contributor / Viewer per project |
| Multi-tenancy | Project isolation via tenant scoping + RLS |
| Encryption at rest | Supabase + R2 |
| Encryption in transit | HTTPS everywhere; mTLS if private network |
| Audit per user | Every action logged with user_id + tenant_id |
| Per-user budget caps | Pre-execution hook reads tenant budget |
| PII redaction hook | Saudi national ID, credit cards scanning |
| SOC2/ISO ready | For ENTERPRISE — Hermes + AWS path |
| Saudi PDPL compliance | HUMAIN sovereign hosting for Saudi data |
| EU GDPR | EU customer data only on Anthropic EU endpoints |
| Customer data isolation | Per-tenant Hermes profiles + per-tenant Supabase schemas |
| DDoS protection | Cloudflare in front of Vercel |
| Vulnerability scanning | Dependabot, Snyk |
| Secret rotation | Quarterly via Maintenance skills |
| Incident response runbook | Stage 5C Security Response owns |

---

## 23. Data Model

### Existing tables (carry forward from current platform)

| Table | Purpose |
|---|---|
| `users` | NEXOURA SaaS users (Supabase auth) |
| `usage_events` | Per-call token tracking |
| `audit_log` | Every tool call + agent action |
| `library_files` | Stored documents |
| `pending_file_writes` | Staged file writes awaiting approval |

### New tables (NEXOURA AI SaaS layer)

| Table | Purpose |
|---|---|
| `tenants` | Customer organizations (id, name, plan, region, locale) |
| `projects` | Products being built (id, tenant_id, name, slug, stage, status, budget_monthly) |
| `lifecycle_stages` | Stage progression per project |
| `deliverables` | Stage gate outputs (PDF, Word, URL) |
| `enhancements` | Customer enhancement backlog |
| `budgets` | Per-tenant per-project budget caps |
| `profiles_active` | Which profiles are spawned per project |
| `kanban_tasks_index` | NEXOURA-side index of Hermes Kanban tasks for UI |
| `messages` | Cross-platform messaging history (inbound) |
| `notifications` | Outbound notification log (sent, delivered, acknowledged) |
| `notification_preferences` | Per-user channel preferences per category |
| `customers` | End customers (B2B and B2C) |
| `subscriptions` | Billing subscriptions |
| `billing_invoices` | Generated invoices |
| `trajectories` | Captured agent runs for fine-tuning |

### Multi-tenant isolation

- Every table has `tenant_id` column
- Supabase Row Level Security policy: `tenant_id = auth.jwt() -> 'tenant_id'`
- Hermes profiles scoped by `--tenant <slug>` flag
- Workspace paths: `~/.hermes/workspaces/<tenant-slug>/<project-slug>/`

---

## 24. Localization (Arabic & MENA)

### UI requirements

- RTL support (Tailwind RTL plugin + `dir="rtl"` switching)
- Bidi text handling
- Locale switching (`next-intl` for i18n with Arabic + English)
- Date/time/number formatting (Hijri + Gregorian)
- Currency (SAR primary for Saudi, USD secondary)
- Font stack (Tajawal, Cairo, Almarai)

### Content workflows

- Arabic-first authoring via `domain-specialist-apt-watch` using HUMAIN ALLaM
- Translation pipeline: when Studio builds a product, `writer` profile produces both EN + AR
- Customer support in Arabic via `customer-service` loading HUMAIN ALLaM when locale=ar
- Voice memo transcription in Arabic via Whisper Large-v3
- Arabic SEO

### Regulatory

- PDPL (Saudi customer data hosted in Saudi via HUMAIN sovereign)
- Data localization (APT WATCH operating from Riyadh)
- Sharia-compliant billing terms

### Marketing

- NEXOURA name pronunciation in Arabic (نيكسورا — TBD)
- Marketing localization
- Customer onboarding in customer's language

---

## 25. Versioning Discipline

### Version hierarchy

```
NEXOURA AI Platform v1.0.0
  ├── nexoura-agent (Hermes fork) v0.14.0-nexoura.0
  │     └── 13+ profiles, each versioned
  │           └── Skills (versioned individually)
  ├── nexoura-saas (Next.js) v1.0.0
  │     ├── Database schema v45
  │     └── Vercel deploy ID
  ├── nexoura-plugins (proprietary) v1.0.0
  │     └── 5 plugins, each versioned (was 9 in v1.2 — see §13)
  └── Hermes service deploy: Zeabur app (Hetzner Falkenstein) — image tag from upstream until Phase 4 custom build
```

### Hermes built-in versioning

- Each SKILL.md has `version` field
- `hermes skills reset <name> --restore` restores bundled version
- Session checkpoints via `CheckpointManager`
- `hermes update` syncs bundled skills
- `hermes profile list/clone/export` for profile snapshots

### NEXOURA SaaS-layer versioning

- Semantic versioning + git tags
- Release branches: `main` / `staging` / `dev`
- Migration versioning (timestamped, reversible)
- Vercel auto-tagged deploys
- Modal `app rollback` for Hermes service
- Plugin versioning in file headers
- All SOUL.md, config.yaml, skills/ in git
- Nightly profile backups to R2
- Audit log immutable, archived after 90 days (5 years for financial per PDPL)
- Agent-created skill changes: PR review before merging
- Blue/green deploys for major changes
- Release notes per version

### Rollback procedure

1. Skill issue → `hermes skills reset <name> --restore`
2. Profile issue → restore from nightly R2 snapshot
3. Plugin issue → git revert + redeploy
4. SaaS UI issue → Vercel previous deploy
5. Hermes service issue → `modal app rollback`
6. Database issue → R2 backup + replay migrations
7. Major platform issue → git revert to previous semver tag + redeploy all

---

## 26. Decision Rules

| # | Rule |
|---|---|
| **D1** | Product-scoped projects within single Studio codebase |
| **D2** | Omar = PM of Studio + sole human gate. Product PMs hired after Studio produces |
| **D3** | Lifecycle discipline. No stage skipping |
| **D4** | Per-stage agent activation. Idle profiles cost nothing |
| **D5** | Multi-LLM by profile (no default Opus). Every profile declares its model |
| **D6** | Hermes-first. Check Hermes role-archetypes and skill registry before introducing patterns |
| **D7** | Brand consistency across NEXOURA products |
| **D8** | NEXOURA AI = platform name (proprietary) / APT WATCH = company name (legal entity) |
| **D9** | Director-Worker pattern with anti-temptation rules in SOUL.md |
| **D10** | Verification reflex. Workers complete with verifiable artifacts; orchestrators verify |
| **D11** | Self-improvement continuous. Phase D never stops |
| **D12** | Exponential speed thesis. Agents train agents. Humans gate, don't code |
| **D13** | MCP-first for integrations |
| **D14** | Closed-source by default. NEXOURA SaaS, plugins, profiles, brand are proprietary |
| **D15** | Plugins over forking. Extend Hermes via `~/.hermes/plugins/` not core mods |
| **D16** | Toolset minimization. Each profile gets only the toolsets it needs |
| **D17** | Notification severity-routed. CRITICAL pierces quiet hours; LOW batches into morning digest |

---

## 27. Risk Register

### Strategic risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Hermes upstream pivots or stops maintenance | HIGH | LOW | We own a fork |
| HUMAIN access changes | MEDIUM | MEDIUM | Multi-provider fallback |
| Anthropic API cost escalation | MEDIUM | MEDIUM | Multi-LLM + subscription proxy + APT WATCH local LLM |
| Single-founder risk | HIGH | LOW | Document everything; build agents capable of running |
| Saudi regulatory changes | MEDIUM | MEDIUM | HUMAIN partnership; auditor profile from Stage 0 |
| Competitor moves | MEDIUM | HIGH | NEXOURA brand, HUMAIN sovereignty, recursive Studio |
| Trademark dispute on NEXOURA | MEDIUM | LOW | File trademark in KSA + EU + US early |

### Technical risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| Modal outage | HIGH | LOW | Hetzner VPS failover |
| Anthropic API outage | HIGH | LOW | OpenRouter fallback configured |
| Vercel outage | MEDIUM | LOW | Cloudflare front; static fallback |
| Supabase outage | HIGH | LOW | R2 daily backups |
| HUMAIN outage | MEDIUM | LOW | Sonnet 4.6 Arabic fallback |
| Prompt injection in uploaded content | HIGH | MEDIUM | Hermes scanner + PII hook + tool guardrails |
| Skill quality drift | MEDIUM | LOW | Curator review cadence + audit hook |
| Data exfiltration via agent tools | HIGH | LOW | Toolset minimization + workspace isolation + audit |
| Notification delivery failure (WhatsApp/SMS) | MEDIUM | LOW | Multi-channel fan-out for CRITICAL |

### Business risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| First product fails to find customers | HIGH | MEDIUM | Stage 0 Feasibility before Stage 3 expense |
| Customer churn exceeds acquisition | HIGH | MEDIUM | Stage 6 Value Measurement quarterly review |
| Pricing wrong | HIGH | MEDIUM | Tiered with usage-based component |
| Saudi market doesn't materialize | MEDIUM | LOW | STUDIO and WORK sold globally |
| Founder burnout | HIGH | MEDIUM | Phase D self-improvement reduces human bottleneck |

### Compliance & legal risks

| Risk | Impact | Probability | Mitigation |
|---|---|---|---|
| PDPL violation (Saudi data leaves Saudi) | HIGH | LOW | HUMAIN sovereign hosting |
| GDPR violation | HIGH | LOW | EU customer data only on Anthropic EU endpoints |
| SOC2/ISO needed before Enterprise can buy | MEDIUM | HIGH | Plan SOC2 audit at Stage 5+ |
| OAuth credential leak | HIGH | LOW | Hermes OAuth isolation |

---

## 28. Success Metrics & Acceptance Criteria

### Platform North Star

**Time from "PM approves Stage 0" to "Product launched in Stage 5":**

- Target Q4 2026: < 12 weeks
- Target Q2 2027: < 8 weeks
- Target 2028: < 4 weeks (with NEXOURA-1 trained)

### Per-stage acceptance criteria

**Stage 0 — Feasibility Study "done" when:** PDF produced with market sizing (sources), 5-year P&L, complexity score, risk register (≥10 risks), competitive matrix (≥3 competitors), resource plan, go/no-go recommendation. PM signs off.

**Stage 1 — Requirements "done" when:** Requirements Brief PDF with 3+ personas, 10+ use cases, scope in/out, success metrics with targets, technical constraints. PM signs off.

**Stage 2 — Branding "done" when:** Brand Book PDF with name, 3-5 taglines, voice, visual identity, design tokens as Tailwind config. PM signs off.

**Stage 3 — Tech "done" when:** Deployed URL, clean repo, >80% test coverage critical paths, security scan clean, P95 < 500ms read / < 2s write, runbook documented. PM signs off.

**Stage 4 — Marketing "done" when:** Site live with SEO meta, 5+ content pieces, launch campaign sent, acquisition channels active, analytics tracking. PM signs off.

**Stage 5 — Operations "healthy" when:** 24/7 monitoring, P0 incident response <15 min, customer support <4 hour first response, monthly Maintenance reports clean.

**Stage 6 — Value "healthy" when:** Monthly Product Value Report on time, unit economics positive (CAC < LTV/3 by month 6), feature ROI scored >80% of features, customer NPS tracked.

### Studio MVP acceptance

NEXOURA Studio v1.0 is "done" when:
- 13 starting profiles deployed and functional
- All 5 NEXOURA plugins working (multi-tenant, billing, notification-router, enhancement-router, stage-gate)
- Chat UI streams agent thinking + tool calls
- Mission Control shows live fleet
- Stage gate UI works for at least one product walk-through
- Multi-LLM picker functional with HUMAIN + Claude + free tier
- 5+ MCP servers integrated
- Notifications working across WhatsApp + Slack + Email + SMS
- Studio successfully builds its own marketing site (recursive demo)
- Cost dashboard tracks per-tenant per-project per-profile spend
- One non-trivial product walks Stage 0 → Stage 4 end-to-end

---

## 29. Pricing Model (proposed)

### NEXOURA STUDIO

| Tier | Price | Includes |
|---|---|---|
| Builder | $99/mo + usage | 1 active product, basic profiles, $50 LLM credits |
| Studio | $499/mo + usage | 3 active products, full roster, $300 LLM credits |
| Enterprise | Custom (from $5K/mo) | Unlimited products, dedicated infra, SLA, sovereign |

### NEXOURA WORK

| Tier | Price | Includes |
|---|---|---|
| Team | $29/agent/mo | Per-agent pricing, basic workforce management |
| Business | $79/agent/mo | Advanced workflows, integrations |
| Enterprise | Custom (from $10K/mo) | Custom agents, SOC2, on-prem option |

### NEXOURA ONE

| Tier | Price | Includes |
|---|---|---|
| Free | $0 | Limited usage, basic profile |
| Premium | $19/mo | Full access, no ads, priority |
| Pro | $49/mo | Multiple personas, advanced integrations |

### NEXOURA ENTERPRISE

| Tier | Price | Includes |
|---|---|---|
| Standard | $25K-$100K/yr | Custom solution, dedicated profiles, SLA |
| Premium | $100K-$500K/yr | Sovereign hosting (HUMAIN for KSA), SOC2/ISO |
| Strategic | $500K+/yr | Multi-year, co-development, custom NEXOURA-1 |

### Saudi/MENA pricing

- All tiers billed in SAR for Saudi customers
- Tap and HyperPay alongside Stripe
- Sharia-compliant billing terms

---

## 30. Cost Model

### Cost per product built (Stage 0 → Stage 4)

| Stage | Duration | Cost estimate |
|---|---|---|
| Stage 0 Feasibility | 3-7 days | $20-60 |
| Stage 1 Requirements | 7-14 days | $30-100 |
| Stage 2 Branding | 3-5 days | $40-80 |
| Stage 3 Tech (heaviest) | 4-6 weeks | $200-800 |
| Stage 4 Marketing | 2 weeks | $50-150 |
| **Total per product** | **8-12 weeks** | **$340-1190** |

Plus infrastructure: ~$200-500 over the 8-12 weeks. Total: $540-1690 per product.

### Unit economics target

- CAC: TBD — Stage 4 marketing budget will determine
- LTV: $99-499/mo × ~24 month avg retention = $2,400-12,000
- Gross margin per Studio customer: ~60-70%
- Payback period target: < 6 months

---

## 31. Build Plan: NEXOURA Studio

### Studio Stage 0 — Feasibility Study

**Status: COMPLETE.** This document IS Studio's feasibility study.

### Studio Stage 1 — Requirements (~1 week)

Studio MVP requirements captured in §28 acceptance criteria. Produced by `researcher` profile loading BA + User Researcher skills.

### Studio Stage 2 — Branding (~3-5 days)

Studio brand within NEXOURA umbrella. Produced by `designer` profile.

### Studio Stage 3 — Technical Implementation (~4-6 weeks)

#### 3a. Foundation (Week 1)

```bash
# WSL2 terminal
git clone https://github.com/NousResearch/hermes-agent.git
cd hermes-agent
git remote add nexoura git@github.com:omar-alageel-platform/nexoura-agent.git
git push nexoura main

# Install locally
./setup-hermes.sh
hermes setup  # Anthropic + HUMAIN + OpenRouter

# Deploy to Modal
hermes deploy --backend modal

# Verify
hermes doctor
```

Tasks:
- Fork to `omar-alageel-platform/nexoura-agent` (private)
- Install Hermes on WSL2
- Deploy Hermes API server on Modal
- Configure providers
- Set up Claude Pro subscription proxy
- Install foundational MCP servers: GitHub, Filesystem, Postgres, Sentry, Notion

#### 3b. Initial profile setup (Week 2)

```bash
# Create the first profile
hermes profile create product-director

# Edit SOUL.md, config.yaml, skills/
# ...

# Repeat for other profiles as needed
```

Phase 1 starting set (just enough to bootstrap):
- `product-director` (Day 1 — your conversation partner)
- `architecture-director` (Day 2 — technical peer)
- `builder` (Day 3 — proves end-to-end PR creation)

Other profiles spawned in Phase 5 as agents take over the build.

Tasks:
- Create initial 3 profiles (others later)
- Configure SOUL.md, config.yaml per profile
- Install community skill collections (itgoyo, Undermybelt, wondelai, obra/superpowers, Leonxlnx/taste-skill, blader/humanizer)
- Configure remaining MCP servers (Linear, Stripe, Slack, WhatsApp Business)
- Configure toolsets per profile (§15)
- Configure Honcho external memory for customer-service (when spawned)

#### 3c. SaaS UI (Weeks 3-4)

Tasks:
- Fork chat UI (open-webui or LobeChat)
- Apply NEXOURA brand
- Build project picker, chat per project, admin pages, Mission Control
- Connect to Hermes API Server
- Add NEXOURA-specific features: stage gates, deliverable preview, model picker, cost dashboard
- Build RTL Arabic support
- Build notification preferences UI

#### 3d. Lifecycle workflow (Weeks 4-5)

Tasks:
- Stage-gate UI (PM approval flow)
- New Supabase tables (§23 data model)
- Deliverable preview (PDF/Word inline)
- Kanban board view per project
- Cost dashboard with per-task LLM attribution
- Customer enhancement workflow UI

#### 3e. NEXOURA plugins (Weeks 5-6 — v1.3 reduced scope)

Tasks:
- Build 5 NEXOURA plugins (§13): nexoura-multi-tenant, nexoura-billing, nexoura-notification-router, nexoura-enhancement-router, nexoura-stage-gate
- Configure HUMAIN + APT WATCH local LLM via `custom_providers` in config.yaml (no plugin code)
- Configure `privacy.redact_pii`, `security.redact_secrets`, `security.tirith_enabled`, `approvals.mode: smart` (no plugin code)
- Integration tests
- Configure hooks (§14)
- Test notification flow end-to-end (WhatsApp + Slack + Email + SMS)
- Estimated effort: ~11-14 plugin-days (was 17-22 in v1.2)

#### 3f. Integration + QA (Week 6)

Tasks:
- End-to-end test: spawn test product, walk Stage 0-4
- Security audit
- Performance check (100 concurrent agents)
- Multi-LLM verification
- Critical-task validation flow
- PDPL compliance check
- Notification delivery test across all channels

### Studio Stage 4 — Marketing & Launch (~2 weeks)

- Studio's own marketing site (recursive demo)
- Content library (5+ pieces)
- SEO (English + Arabic)
- Invite-only beta launch
- Pricing page live

### Studio Stages 5-7

Operations + Value Measurement begin from launch. Stage 7 iteration after first real product build.

**Total Studio build: 8-10 weeks.**

---

## 32. Roadmap & Sequencing

### Q2 2026 (May-June): Studio v1.0

- Weeks 1-6: Studio Stage 3
- Weeks 7-8: Studio Stage 4
- End of June: Studio operational, invite-only beta

### Q3 2026 (July-September): First product

Choose: **NEXOURA WORK** OR **APT WATCH supply chain SaaS**.

- Studio builds chosen product Stage 0-4
- 8-12 weeks
- Phase D self-improvement compounds for subsequent products

### Q4 2026 (October-December): Revenue customer

- Selected product launched, Stage 5 operations
- First paying customer onboarded
- Begin scoping second product
- NEXOURA AI publicly launched

### 2027 H1: Multi-product, multi-user

- Second product
- Staff hires for product-lead roles
- Third product begins
- Trajectory data collection for NEXOURA-1

### 2027 H2: NEXOURA-1 LLM trained

- Custom NEXOURA-1 online
- Cost per operation drops dramatically

### 2028: Scale

- All 4 NEXOURA products in market
- ENTERPRISE customers in Saudi gov, financial institutions
- Regional expansion to UAE, Egypt, MENA
- Consider PIF / Saudi investor funding

---

## 33. Open Questions

| # | Question | Need by |
|---|---|---|
| Q1 | First product after Studio: WORK or APT WATCH supply chain? | End of Stage 3d (Week 5) |
| Q2 | Modal vs Hetzner VPS for Hermes deployment? | Stage 3a (Week 1) |
| Q3 | Fork open-webui vs LobeChat vs custom Next.js? | Stage 3c (Week 3) |
| Q4 | When to hire first product PM? | When first product reaches Stage 3 |
| Q5 | NEXOURA-1 base model (DeepSeek-V3, Qwen 2.5)? | Year 2 |
| Q6 | Validate pricing tiers with target customers? | Stage 4 (Week 7-8) |
| Q7 | Honcho default for `customer-service` or simpler Mem0 start? | Stage 3b (Week 2) |
| Q8 | NEXOURA AI domain name? | Stage 4 |
| Q9 | Funding strategy — bootstrap, pre-seed, or PIF? | Q4 2026 review |
| Q10 | Trademark filing jurisdictions and timing? | Stage 2-3 |
| Q11 | Default `customer-service` notification channel for tenant onboarding? | Stage 3d (Week 4) |

---

## 34. Glossary

| Term | Meaning |
|---|---|
| **NEXOURA AI** | The platform brand (proprietary, closed source) |
| **APT WATCH** | The company name (legal entity) |
| **STUDIO** | The first NEXOURA product — builds AI-powered platforms |
| **WORK / ONE / ENTERPRISE** | The other three NEXOURA products, built BY Studio |
| **Hermes Agent** | Open-source AI agent framework by NousResearch (MIT) — our runtime |
| **NEXOURA-1** | Future custom LLM, fine-tuned on NEXOURA trajectories |
| **Profile** | Isolated agent instance with own SOUL, memory, toolset, model, skills, cron |
| **Skill** | A capability (SKILL.md file) any profile can load on demand |
| **SOUL.md** | Per-profile personality file |
| **MEMORY.md** | Per-profile agent-curated memory (~2200 chars) |
| **USER.md** | Per-user profile knowledge (~1375 chars) |
| **Kanban** | Hermes durable multi-agent task board |
| **Director archetype** | Profile that decomposes and routes (auto-loads kanban-orchestrator) |
| **Worker archetype** | Profile that claims one task and executes (auto-loads kanban-worker) |
| **Curator** | Hermes background process for skill maintenance (7-day cycle) |
| **Honcho** | External memory provider with dialectic reasoning |
| **HUMAIN** | Saudi Arabia's $100B PIF AI company; provides ALLaM 34B Arabic LLM |
| **APT WATCH local LLM** | In-development sovereign LLM at APT WATCH |
| **MCP** | Model Context Protocol — open standard for tool/integration servers |
| **ACP** | Agent Communication Protocol — Hermes IDE integration |
| **Phase D** | Background self-improvement phase |
| **Stage gate** | Human PM approval point between Phase A stages |
| **Subscription proxy** | Hermes feature to route through Claude Pro/ChatGPT Pro subscriptions |
| **GEPA** | Genetic-Pareto Prompt Evolution — Hermes self-evolution mechanism |
| **Pairing** | Hermes gateway access control for messaging platforms |

---

## 35. Profile naming reference (quick lookup)

### Cross-product directors (instantiate as needed)
- `product-director`
- `architecture-director`
- `design-director`
- `brand-director`
- `marketing-director`

### Per-product directors (spawned per active product, slug = product name)
- `product-lead-{slug}` (e.g., `product-lead-apt-watch`, `product-lead-work`)
- `tech-lead-{slug}`
- `design-lead-{slug}`

### Workers (function-based, shared across products)
- `builder`
- `researcher`
- `designer`
- `writer`
- `reviewer`
- `customer-service`
- `operator` (may split into `sre` + `operator` when justified)
- `auditor`
- `domain-specialist-{slug}` (e.g., `domain-specialist-apt-watch`)

---

## 36. References

### Hermes Agent
- GitHub: https://github.com/NousResearch/hermes-agent
- Docs: https://hermes-agent.nousresearch.com/docs/
- Skills catalog: https://hermes-agent.nousresearch.com/docs/reference/skills-catalog
- Kanban: https://hermes-agent.nousresearch.com/docs/user-guide/features/kanban
- Skills: https://hermes-agent.nousresearch.com/docs/user-guide/features/skills
- Memory: https://hermes-agent.nousresearch.com/docs/user-guide/features/memory

### Standards
- agentskills.io: https://agentskills.io
- MCP awesome list: https://github.com/punkpeye/awesome-mcp-servers
- Model Context Protocol: https://modelcontextprotocol.io

### HUMAIN
- Website: https://www.humain.com/

### Community skill collections
- itgoyo/hermes-skills (310+ skills)
- Undermybelt/hermes-skills (900+ skills)
- wondelai/skills (380+ skills)
- obra/superpowers
- Leonxlnx/taste-skill
- blader/humanizer

### Saudi regulatory
- PDPL: https://sdaia.gov.sa/en/SDAIA/about/Pages/PersonalDataProtection.aspx
- SDAIA: https://sdaia.gov.sa/

---

## 37. Document Change Log

| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-17 | Initial specification approved for execution |
| 1.1 | 2026-05-17 | Brand changed to NEXOURA AI (proprietary). Added: License & IP (§2), Memory Architecture (§10), Hermes API Server (§12), Plugin System (§13), Hooks System (§14), Toolsets per profile (§15), Batch Processing & Self-Evolution (§16), Data Model (§22), Localization (§23), Risk Register (§26), Success Metrics & Acceptance Criteria (§27), Pricing Model (§28). Fixed messaging count to 24. Added 7 terminal backends. Subscription proxy added to cost model. Added D14-D16. |
| 1.2 | 2026-05-17 | Renamed all profiles to Hermes-aligned kebab-case (product-director, architecture-director, builder, researcher, customer-service, operator, auditor, etc.). Removed corporate "Senior/Project/CEO/CTO" hierarchy. Added §20 Notifications & Alerts (outbound notifications via WhatsApp/Slack/Teams/Email/SMS with severity routing, quiet hours, escalation). Added `nexoura-notification-router` plugin. Added D17 (notification severity routing). Added §35 Profile naming quick reference. Updated §15 toolsets table with new names. Added Q11 open question. |
| 1.3 | 2026-05-18 | **Hermes documentation review pass.** Surfaced 27 Hermes capabilities that NEXOURA was planning to build from scratch but are already shipped — see new §12.1 ("Hermes capabilities we LEVERAGE vs NEXOURA capabilities we BUILD"). Key changes: §11 expanded auxiliary model overrides from 5 tasks to 8 tasks (vision, web_extract, approval, compression, session_search, skills_hub, mcp, triage_specifier) with explicit cost-impact analysis. §11 added credential pool rotation strategies for rate limit / failover. §11 added iteration budget pressure as built-in safeguard (drops need for `nexoura-budget-guardrail` plugin). §13 plugin count reduced 9 → 5 (dropped nexoura-humain-provider, nexoura-apt-watch-llm, nexoura-budget-guardrail, nexoura-pii-redaction — Hermes built-ins or config.yaml entries cover them). §21 actual infrastructure costs updated with Phase 2 reality ($16/mo Hetzner Falkenstein via Zeabur vs original $50+ estimate). New §21.5 Phase 2 Deployment Record (alternatives considered, Hetzner choice rationale, upstream-image constraint deferred to Phase 4, Modal downgrade plan, acceptance criteria). §22 Security Baseline updated with v0.14-specific Hermes config keys (`privacy.redact_pii`, `security.redact_secrets`, `security.tirith_enabled`, `security.website_blocklist`, `approvals.mode: smart`, `display.file_mutation_verifier`). §25 version hierarchy updated (5 plugins, Zeabur deploy). §28 Studio MVP acceptance updated (5 plugins). §31 Stage 3e plugin work reduced 17-22 days → 11-14 days. Phase 1 closed May 18 with PHASE1-KANBAN-SPEC.md as Director artifact, committed and pushed to fork as 38cbbfd18. |

---

**End of NEXOURA AI Platform Specification v1.3**
