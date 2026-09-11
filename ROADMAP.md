# AI Repository Audit Roadmap

This roadmap describes the public AI Repository Audit capability system as it exists now and the remaining evidence-depth work. It is capability-oriented: a new repository or product is created only when a genuinely separate ownership boundary, lifecycle, API, or data model is proven necessary.

## Product objective

At one exact source revision, answer:

1. What does this repository claim?
2. What evidence actually exists?
3. What is VERIFIED, PARTIAL, UNVERIFIED, CONTRADICTED, or NOT_APPLICABLE?
4. What can fail despite green CI?
5. What should be fixed first, and what evidence would prove the fix?

The target output is an **Overall Repository Portrait**, not a generic code review or an opaque score.

## Current implementation boundary

The current public product already includes a deterministic bounded implementation of the core repository portrait path:

- exact repository/revision binding to an immutable Git tree;
- Repository Evidence Mapper v1.1 and evidence-contract validation;
- exact README claim preservation from common README formats;
- structured GitHub Actions inspection;
- bounded CI, workflow-security and release signals;
- test/config discovery without silent list truncation;
- explicit evidence states and fail-closed VERIFIED semantics;
- 15 Audit v2 assurance domains;
- integrated Overall Repository Portrait;
- adversarial/self-quality regression coverage.

These capabilities are **not** equivalent to runtime proof, penetration testing, certification, vulnerability absence, production readiness, legal clearance, or successful release execution. Static evidence remains static evidence.

## Public evidence boundary

This public repository uses only public-source evidence plus synthetic material created specifically for this public product. Private/internal-derived evidence is not republished here even after anonymization, sanitization, aggregation, paraphrase, or generalization.

Public dogfood and case material must therefore be reproducible from named public sources or be explicitly synthetic.

## Capability map A-S

### Phase A — Public dogfood / benchmark depth — ACTIVE / ADVANCED

Public exact-revision demonstration audits exist across multiple repository archetypes. Continue expanding only when new public subjects add a meaningful benchmark dimension.

Residual work:
- rerun selected public demos against newer engine revisions when benchmark comparability matters;
- maintain explicit false-positive/low-value rejection notes;
- build cross-demo reproducibility metrics without treating GitHub stars or maintainer reaction as product-quality proof.

### Phase B — Repository Evidence Mapper — IMPLEMENTED v1.1

Current bounded implementation maps repository inventory, workflows, tests, release/security signals, public claims, evidence references and explicit unknowns.

Residual work:
- deepen typed evidence relationships;
- expand ecosystem-aware dependency and contract evidence without weakening exact-subject binding.

### Phase C — CI Evidence Profiler — IMPLEMENTED STATIC BASELINE

Current implementation inspects triggers, path filters, matrices, conditions, dependency/aggregate structure, permissions, action refs, reusable-workflow refs and obvious statically skipped jobs.

Residual work:
- ingest exact-subject workflow-run/job conclusions when supplied through an explicit trusted evidence path;
- compare configured checks with actual branch/ruleset enforcement;
- model cancellation/retry and matrix-leg execution evidence.

A green workflow definition or observed static graph never proves the jobs actually executed.

### Phase D — Test Depth Map — IMPLEMENTED DISCOVERY BASELINE

Current implementation discovers recognized repository-visible test/config evidence, preserves large test trees without arbitrary truncation, classifies bounded test types and separates discovery from execution.

Residual work:
- bind suites to actual CI/runtime execution evidence;
- improve subsystem/test membership mapping;
- measure coverage/depth only when corresponding evidence exists.

File presence is not test execution proof.

### Phase E — Release and Provenance Audit — PARTIAL / IMPLEMENTED STATIC BASELINE

Current implementation identifies bounded release/publisher signals, artifact handoffs, OIDC permission signals, signing/attestation vocabulary, smoke/verification and rollback/recovery signals while avoiding simple negated-word false positives.

Residual work:
- source-to-artifact digest binding;
- artifact identity/attestation verification;
- exact release execution evidence;
- trusted-publisher identity and authorization proof;
- reproducible build evidence.

### Phase F — Workflow Security Analysis — IMPLEMENTED STATIC BASELINE

Current implementation covers scoped/broad permissions, credential persistence signals, untrusted event interpolation, privileged PR context, mutable action references, reusable workflows and secret forwarding.

Residual work:
- called reusable-workflow transitive analysis;
- cache/artifact trust-flow analysis;
- runtime/effective token and enforcement evidence where accessible.

A static signal is not a proven exploit.

### Phase G — Supply-chain and Dependency Health — PARTIAL

Current implementation inventories manifests/lockfiles, update automation, SBOM/license signals and generated/vendor boundaries at a bounded static level.

Residual work:
- resolved direct/transitive dependency inventory;
- integrity/hash evidence;
- known-vulnerability evidence where a current source is accessible;
- license compatibility evidence;
- dependency provenance and freshness;
- ecosystem-specific reproducibility checks.

This capability should integrate with the portfolio's existing accepted supply-chain assurance direction rather than create a duplicate authority.

### Phase H — Claims vs Evidence Matrix — IMPLEMENTED BASELINE

Current implementation preserves exact claim wording and separates claim-source from proof-source. VERIFIED claims require exact accessible supporting evidence and fail closed on contradictions/self-support patterns covered by the evidence contract.

Residual work:
- richer typed claim-to-evidence semantics;
- docs/release/config claim discovery beyond README where source semantics can remain deterministic;
- automated contradiction matching only where false-positive risk is acceptably bounded.

### Phase I — AI-assisted Change Provenance — PARTIAL

The evidence model represents AI-assisted changes, generated code and external build/test services when explicit evidence exists.

Residual work:
- deterministic public provenance extraction from supported public metadata;
- review-boundary and changed-semantics evidence;
- avoid any authorship inference unsupported by repository evidence.

### Phase J — Architecture and Change-impact Analysis — PARTIAL

Current implementation provides repository/path/API boundary signals and explicit unknowns.

Residual work:
- language-aware dependency graph;
- dependency direction and cycles;
- change hotspots from public history;
- blast-radius/change-impact evidence;
- duplicated authority and compatibility-layer signals.

No generic architecture score should be produced without evidence.

### Phase K — API / Contract Drift — EARLY / PARTIAL

Current portrait can identify API/schema-like surfaces, but a full producer/consumer drift engine is not yet implemented.

Residual work:
- compare supported public schemas/specifications with consumers/implementation where deterministic parsing is available;
- configuration/CLI/docs drift;
- compatibility and deprecation evidence.

### Phase L — Documentation vs Runtime/Build Reality — PARTIAL

Claims, workflow and repository evidence provide a bounded baseline.

Residual work:
- reproducible documented install/build/example checks when safe execution evidence is supplied;
- version/configuration example drift;
- docs-only validation-bypass evidence.

### Phase M — Performance and Resource Evidence — EARLY / EVIDENCE-ORIENTED

Current assurance model can represent static benchmark/performance signals, but it does not manufacture runtime measurements.

Residual work:
- ingest exact benchmark artifacts;
- compare thresholds and baselines;
- preserve environment/tool identity and noise limits.

### Phase N — Observability and Operability — PARTIAL STATIC BASELINE

Current portrait detects bounded repository-visible operational signals such as health/runbook/deployment-related files.

Residual work:
- structured logging/metrics/tracing evidence;
- exact recovery/rollback exercise evidence;
- runtime health and graceful-degradation evidence;
- operational failure-mode verification.

This should integrate with the existing accepted runtime-assurance direction rather than duplicate it.

### Phase O — Maintainability and Hotspots — PARTIAL STATIC BASELINE

Current implementation identifies bounded large-file and generated/vendor signals.

Residual work:
- change concentration from public history;
- complexity/duplication evidence;
- brittle test coupling;
- stale/dead-code signals with calibrated confidence.

Contributor count alone is not a team-quality metric.

### Phase P — Policy and Governance Evidence — PARTIAL STATIC BASELINE

Current portrait inspects repository-visible governance files and keeps platform enforcement separate.

Residual work:
- branch/ruleset/required-check evidence ingestion where accessible;
- compare documented policy with actual enforcement;
- retention/provenance enforcement evidence.

For this repository specifically, current GitHub state does **not** establish required-status-check enforcement; successful CI must not be described as a guaranteed merge gate until platform configuration proves it.

This capability should integrate with the existing accepted policy-assurance direction rather than create a duplicate authority.

### Phase Q — Overall Repository Portrait — IMPLEMENTED / INTEGRATED

Current Audit v2 composes the exact validated REM v1.1 subject with all 15 assurance domains and produces findings, explicit unknowns, remediation and a bounded verdict.

Residual work is depth, not creation of another portrait engine.

### Phase R — Auditor Self-Quality Controls — IMPLEMENTED BASELINE / ACTIVE

Current regression suite includes adversarial cases for exact-subject binding, ignored/untracked scan isolation, symlink boundaries, wrong-subject evidence, self-support/contradiction handling, reusable workflows, explicit empty permissions, statically skipped jobs, release-word false positives, large test trees and test-path false positives.

Residual work:
- more golden public subjects;
- repeatability/determinism measurement;
- duplicate-finding and severity-calibration tests;
- information-isolation tests across independent public/synthetic audit subjects.

### Phase S — Customer-facing Report Experience — WORKING BASELINE

Current public repository provides executive explanations, evidence-state semantics, demo reports, Free Demo intake and differentiated paid-service scopes.

Residual work:
- cleaner structured Full Audit export;
- evidence matrix/finding filters;
- printable/shareable report generation when customer evidence justifies the investment.

Do not build heavy dashboard/SaaS infrastructure before real demand requires it.

## Audit v2 assurance domains

The integrated v2 portrait contains 15 explicit assurance domains:

**Wave A** — Threat Model; Data Privacy; Agent Safety; Identity & Access.  
**Wave B** — Resilience; Incident Readiness; External Dependency Failure; Auditability & Forensics.  
**Wave C** — Model Evaluation; FinOps; Configuration; Concurrency.  
**Wave D** — Migration; Interface / Contract Compatibility; License / IP.

Presence of all 15 domains means the evidence contract is structurally complete. It does **not** mean all 15 domains passed.

## Ownership / anti-twin rule

No new standalone repository is approved by this roadmap.

AI Repository Audit remains the public audit/product surface. When deeper execution, supply-chain, runtime, policy, evidence-storage, GitHub-provider or control-plane capability is required, integrate with the portfolio's existing accepted canonical capability direction instead of creating a second independently writable implementation.

New extraction into a separate product is justified only by a stable independent domain boundary, lifecycle/API/data model, clear anti-duplication case and concrete customer value.

## Residual execution order

1. Deepen supply-chain/dependency evidence.
2. Deepen architecture/change-impact and contract drift.
3. Add explicit external exact-run evidence ingestion for CI/test/release where trustworthy inputs are available.
4. Deepen source-to-artifact provenance and release verification.
5. Expand runtime/performance/observability evidence adapters without manufacturing runtime proof.
6. Expand auditor golden cases and repeatability metrics.
7. Improve Full Audit report/export experience only to the level justified by real use.
8. Reassess product depth and commercial scope using real public audits and customer evidence.

## Definition of trustworthy progress

A capability is not complete because code exists or CI is green. Progress requires, as applicable:
- exact-subject implementation;
- deterministic tests including negative/adversarial cases;
- current evidence bound to the candidate SHA;
- no false PASS or evidence-state loss;
- public-origin-only publication compliance;
- explicit static/runtime/external-evidence boundary;
- integration impact review;
- truthful documentation.

## Success criteria

The roadmap succeeds when repeated audits on materially different public repository archetypes consistently produce:
- repository-specific findings rather than generic advice;
- exact-revision traceability;
- explicit UNVERIFIED and CONTRADICTED states;
- useful remediation and verification requirements;
- reproducible evidence-depth outputs;
- low false-positive/duplicate rates;
- materially deeper Full Audit output than Free Demo;
- customer evidence that the resulting audit is worth paying for.

Until customer evidence exists, pricing and market demand remain hypotheses rather than technical facts.
