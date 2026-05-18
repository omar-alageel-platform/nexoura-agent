# Phase 2 Deployment Record

**Status:** ✅ Closed 2026-05-18
**Hermes API:** Live at https://nexoura-studio.zeabur.app
**Infrastructure:** AWS Lightsail Frankfurt 4C/16GB via Zeabur
**Cost:** $84/mo (Lightsail) — note: original plan was Hetzner Falkenstein $16/mo, selected Lightsail at deploy time

## Verification

First curl test response:
Second curl test (Opus reasoning depth verified): 965-token coherent response,
correctly identified itself as Hermes Agent on Opus 4.6 via OpenRouter,
confirmed runtime location as AWS Linux container.

## Findings

1. Default routing: OpenRouter (not Anthropic direct). Both keys configured.
   Cost trade: ~5-10% OpenRouter margin. Acceptable for Phase 2.
2. Model resolution: "claude-opus-4-7" → Opus 4.6 (closest available).
   Catalog may need refresh; fine-tune in Phase 4.
3. Default SOUL.md (generic Hermes identity). NEXOURA-specific SOUL.md
   will be authored in Phase 3 when profiles are formalized.
4. Runtime: Kubernetes pod on AWS Lightsail (Zeabur orchestration).

## Next: Phase 3

Configure named profiles (product-director, builder) with custom SOUL.md.
Test first closed loop: Director dispatches Builder → real PR on GitHub.
