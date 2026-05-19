# Phase 3 — Final Closure Record

**Date:** 2026-05-19 (morning)
**Status:** ✅ FULLY CLOSED — all of 3a, 3c, 3d done.

## Phase 3 complete summary

Phase 3 set out to prove the platform can produce verifiable artifacts
autonomously (real PRs on GitHub, not chat messages), then mirror the
capability to cloud Hermes.

All three subphases closed:

- **3a (MCP setup local):** github MCP (6 tools) + filesystem MCP (5 tools)
  configured on local Ubuntu Hermes.
- **3c (first closed loop):** PR #1 authored, fixed, merged. Worker
  recovered autonomously from MCP auth failure via gh CLI fallback.
  Verification reflex confirmed delta=0 twice (T1 + fix).
- **3d (cloud mirror):** github MCP added to cloud Hermes config.yaml at
  /opt/data/config.yaml. Cloud Hermes restarted. 6 github MCP tools
  successfully enumerated via API call.

## Cost reality (vs estimate)

Estimate during dispatch: $30-50 in API costs for Phase 1-3.
Actual OpenRouter spend through Phase 3 close: $0.32 (Claude Opus 4.6
via OpenRouter with prompt caching).
Discrepancy: 100x cheaper than estimated.

Implication: Phase 4-6 work likely costs $10-30 total at current usage
patterns. Platform runtime + infra dominates spend, not API calls.

## Cloud Hermes state

Endpoint: https://nexoura-studio.zeabur.app
Infrastructure: AWS Lightsail Frankfurt 4C/16GB via Zeabur ($84/mo)
Runtime: K8s pod, Ubuntu 24.04, Hermes nousresearch/hermes-agent:v2026.4.30
Configured:
  - ANTHROPIC_API_KEY, OPENROUTER_API_KEY, GITHUB_TOKEN, GITHUB_PERSONAL_ACCESS_TOKEN
  - API_SERVER_KEY (auto-generated, opaque to user)
  - mcp_servers.github (6 filtered tools)

Open issue (non-blocking): TELEGRAM_BOT_TOKEN env var has placeholder value
${TELEGRAM_BOT_TOKEN}, causing constant reconnect attempts in agent.log.
Fix: remove the env var entirely in Zeabur, or set to empty string. Will
address in Phase 4 cleanup.

## Tool namespace observation

Local Hermes (v0.14): `mcp__github__create_pull_request` (double underscore)
Cloud Hermes (v2026.4.30): `mcp_github_create_pull_request` (single underscore)

Version-specific convention. Future dispatch briefs targeting cloud must
use single-underscore form. Worth tracking for spec v1.4.

## Memory entries from Phase 3 (persist for T2-T11)

1. github MCP write endpoints fail "Authentication Failed"; use gh CLI
   fallback without retrying MCP. (Encoded in T1 + fix dispatches.)
2. Fix-pattern dispatches take 1 commit, 1 verification round, ~$2-4.
3. Worker authoring SKILL.md from existing spec sources lands at 15-16k
   chars typical; recommend ceiling of 16k for stage skills.

## What unlocks next

**Phase 4: Wire Next.js UI to Cloud Hermes**
  - Bridge platform-omae.vercel.app → nexoura-studio.zeabur.app
  - Live chat UI streaming
  - Cost meter visible
  - First user-facing surface

**Phase 5: T2-T11 skill authoring batch**
  - Author 10 more skills using proven dispatch pattern
  - Estimated cost: ~$5-10 total at current rate
  - Estimated time: ~5-8 hours if dispatched sequentially

**Phase 6: First real engagement (APT WATCH supply chain SaaS)**
  - Create /home/omar/dev/nexoura-engagements/apt-watch-supply-chain-saas
  - Run through Stages 1-6 with agents producing artifacts
  - First platform output of real customer-grade work
