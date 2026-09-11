# AI Repository Audit v2 — 15-domain assurance portrait

Audit v2 extends the evidence-first repository portrait with 15 explicit assurance domains while preserving exact-subject and fail-closed semantics.

## Domains

1. Threat model — assets, entry points, trust/execution boundaries and evidence-backed STRIDE hypotheses.
2. Data privacy — personal/customer-data, logging, lifecycle and encryption-boundary signals.
3. Agent safety — tool authority, untrusted-content boundaries, confirmation gates, loop/budget and memory-provenance signals.
4. Identity and access — authentication, authorization, tenant and service-identity signals.
5. Resilience — timeout, retry/backoff, idempotency, degraded-mode and bounded failure-injection signals.
6. Incident readiness — backup/restore, rollback, kill-switch, runbook and RTO/RPO signals.
7. External dependency failure — provider/API/database/storage failure-handling boundaries.
8. Auditability and forensics — actor/correlation/event IDs, audit trails and tamper-resistance signals.
9. Model evaluation — frozen eval/holdout, leakage, grader, error-taxonomy and model-version regression signals.
10. FinOps — API/LLM/token/storage/log cost drivers, budgets and amplification risks.
11. Configuration — defaults, required settings, feature flags, fallbacks and environment-drift signals.
12. Concurrency — locks, transactions, duplicate workers/webhooks, idempotency and exactly-once assumptions.
13. Migration — schema changes, backfills, rollback/irreversibility and compatibility assumptions.
14. Interface — OpenAPI/schema/event/protobuf and producer-consumer compatibility signals.
15. License/IP — license, attribution and source-origin/provenance signals.

## Evidence semantics

The v2 completion contract requires all 15 domains to be represented. Contract completeness is not a global PASS. A domain with only static repository evidence remains PARTIAL or UNVERIFIED as appropriate.

Signal counts are descriptive only and are never converted into an opaque readiness or security score. Missing evidence stays explicit.

## What static v2 does not prove

Repository evidence alone does not prove exploitability or vulnerability absence; privacy/legal/compliance status; production authentication/authorization or tenant isolation; prompt-injection resistance; runtime resilience or achieved SLAs; backup/restore success or RTO/RPO; actual provider-failure behavior; model quality or absence of evaluation leakage; actual cost/savings; race freedom/exactly-once behavior; migration safety/zero-downtime behavior; deployed cross-service compatibility; or legal IP/license clearance.

Those claims require the corresponding runtime, operational, adversarial, legal, economic, compatibility or evaluation evidence.

## Composition and ownership

Audit v2 remains a capability layer of the existing Audit/Seal Platform. It does not create fifteen new verdict authorities or fifteen repositories.

PatchSeal retains system/component verification and verdict authority where applicable; local-test-hub owns reproducible bounded execution; Evidence-Vault owns durable exact-subject evidence; GitHub-integration owns provider transport; Platform-Control-Plane owns tenant/commercial state.

A v2 capability should graduate to a standalone canonical repository only after dogfood proves a genuinely separate domain model, lifecycle, API/evidence contract and ownership boundary.

## Completion gate

The public CI gate validates:
- the base Repository Evidence Map extractor;
- Wave A, B, C and D deterministic regression fixtures;
- Overall Repository Portrait composition;
- the 15-domain assurance completion contract;
- the integrated v2 portrait;
- public-repository confidentiality/safety validation.

Passing these checks proves that the repository's current v2 implementation contract and regression fixtures pass on the tested exact subject. It does not certify third-party repositories or turn static evidence into runtime proof.
