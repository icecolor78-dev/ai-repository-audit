# AI Repository Audit Roadmap

This roadmap describes the public AI Repository Audit capability system as it exists now and the evidence-depth work that remains. A capability is not called complete merely because code exists or CI is green.

## Product objective

At one exact source revision, answer:

1. What does this repository claim?
2. What evidence actually exists?
3. What is VERIFIED, PARTIAL, UNVERIFIED, CONTRADICTED, or NOT_APPLICABLE?
4. What can fail despite green CI?
5. What should be fixed first, and what evidence would prove the fix?

The target output is an **Overall Repository Portrait**, not a generic code review or opaque score.

## Accepted bounded implementation

The current public product includes:

- exact repository/revision binding to an immutable Git tree;
- Repository Evidence Mapper v1.1 with mandatory evidence-contract validation;
- exact README claim preservation and claim-source/proof-source separation;
- structured GitHub Actions, workflow-security and release-signal inspection;
- bounded false-green CI signals, including statically skipped jobs;
- reusable-workflow, permissions, action-ref and secret-forwarding analysis;
- test/config discovery with execution kept separate from file presence;
- bounded supply-chain/dependency metadata extraction;
- repository-local architecture/dependency-edge and contract-drift evidence;
- 15 Audit v2 assurance domains and integrated Overall Repository Portrait;
- exact-subject caller-supplied workflow/test/release evidence with `SUPPLIED_EXACT` trust;
- bounded runtime/performance/observability evidence with explicit units, environment and sample count;
- bounded source-to-artifact provenance records with exact source SHA and artifact digest;
- time-bound branch/ruleset observations with separate `SUPPLIED_PLATFORM_STATE` trust;
- golden adversarial end-to-end regression coverage;
- deterministic customer-facing Markdown report rendering.

These capabilities are **not** equivalent to penetration testing, certification, vulnerability absence, production readiness, legal clearance, successful deployment, independently authenticated runtime evidence, or product-market fit.

## Public evidence boundary

This public repository uses only public-source evidence plus synthetic material created specifically for this public product. Private/internal-derived evidence is not republished here even after anonymization, sanitization, aggregation, paraphrase, or generalization.

Public dogfood and case material must be reproducible from named public sources or be explicitly synthetic.

## Capability map A-S

### A — Public dogfood / benchmark depth — ACTIVE / ADVANCED
Public exact-revision demonstration audits exist across materially different public repository archetypes.

Residual: rerun selected subjects when comparability matters; add only benchmark dimensions that materially differ; measure repeatability and false-positive/low-value rejection without treating stars or maintainer response as quality proof.

### B — Repository Evidence Mapper — IMPLEMENTED v1.1
Exact immutable-subject extraction and mandatory evidence validation are integrated.

Residual: richer typed evidence relations where semantics can remain deterministic and fail closed.

### C — CI Evidence Profiler — IMPLEMENTED BOUNDED STATIC + SUPPLIED-EXECUTION LAYER
Static workflow structure and exact-subject caller-supplied workflow observations are represented separately.

Residual: independently provider-retrieved run/job evidence; matrix-leg, retry/cancellation and current check-suite semantics; provider-authenticated branch enforcement comparison.

### D — Test Depth Map — IMPLEMENTED DISCOVERY + SUPPLIED-EXECUTION LAYER
Recognized tests/configuration are discovered without arbitrary truncation; supplied exact execution counts can be represented without converting them to independently VERIFIED proof.

Residual: subsystem/test membership, assertion/coverage/depth evidence when corresponding artifacts exist, and independent provider retrieval.

### E — Release and Provenance Audit — IMPLEMENTED BOUNDED STATIC + SUPPLIED PROVENANCE LAYER
Release/publisher signals, artifact handoffs and bounded source-to-artifact provenance records are represented. Provenance records require exact source SHA, sha256 artifact digest, predicate/builder identity and same-repository public GitHub source.

Residual: independent attestation/signature verification, trusted-builder authorization, reproducible-build evidence, exact release execution and deployed-artifact confirmation.

Metadata presence alone never proves a safe or successful release.

### F — Workflow Security Analysis — IMPLEMENTED STATIC BASELINE
Scoped/broad permissions, credential persistence, untrusted expressions, privileged PR context, mutable action/reusable-workflow refs and secret forwarding are covered.

Residual: transitive called-workflow analysis, cache/artifact trust flow and runtime/effective token evidence.

### G — Supply-chain and Dependency Health — PARTIAL / USEFUL BASELINE
Manifest/lockfile, update automation, SBOM/license, integrity and generated/vendor signals are represented at a bounded static level.

Residual: ecosystem-complete direct/transitive resolution, independently current vulnerability data, deeper license compatibility/provenance/freshness and reproducibility checks.

### H — Claims vs Evidence Matrix — IMPLEMENTED BASELINE
Exact claims remain distinct from proof sources; VERIFIED fails closed on self-support, contradictions and wrong-subject evidence.

Residual: richer typed semantics and bounded contradiction matching beyond README where false-positive risk is acceptable.

### I — AI-assisted Change Provenance — PARTIAL
Explicit repository evidence can be represented; unsupported authorship inference is prohibited.

Residual: deterministic extraction from supported public provenance metadata and changed-semantics/review-boundary evidence.

### J — Architecture and Change-impact Analysis — IMPLEMENTED BOUNDED STATIC BASELINE
Repository-local dependency edges/cycles and bounded API/schema surfaces are extracted for supported languages/formats.

Residual: broader language support, public-history hotspots, deeper blast-radius semantics, duplicate-authority/compatibility-layer analysis and dynamic/runtime dependency evidence.

No generic architecture score is produced.

### K — API / Contract Drift — IMPLEMENTED EARLY BOUNDED BASELINE
Supported schema/spec surfaces and broken local references are detected deterministically.

Residual: producer/consumer comparison, CLI/config/docs drift, deprecation/compatibility evidence and broader contract formats.

### L — Documentation vs Runtime/Build Reality — PARTIAL
Claims, repository structure, workflows and supplied execution evidence form a bounded baseline.

Residual: independently reproducible install/build/example execution and version/config drift checks.

### M — Performance and Resource Evidence — IMPLEMENTED SUPPLIED-EVIDENCE BASELINE
Structured latency/duration/CPU/memory/throughput/health/recovery measurements preserve unit, environment, sample count, exact SHA and public source.

Residual: independently authenticated benchmark artifacts, baseline/threshold comparison and noise/statistical treatment. Supplied measurements do not prove production representativeness or SLA compliance.

### N — Observability and Operability — IMPLEMENTED SUPPLIED-EVIDENCE BASELINE
Logs/metrics/traces/health/recovery artifact references and bounded operational signals can be represented.

Residual: provider-authenticated runtime evidence, recovery exercises, graceful-degradation and failure-mode verification.

### O — Maintainability and Hotspots — PARTIAL STATIC BASELINE
Large/generated/vendor signals are bounded and observable.

Residual: public-history change concentration, calibrated complexity/duplication, brittle coupling and stale/dead-code evidence.

### P — Policy and Governance Evidence — IMPLEMENTED BOUNDED STATIC + SUPPLIED PLATFORM-STATE BASELINE
Repository-visible governance is separated from time-bound branch/ruleset state. Supplied enforcement observations use `SUPPLIED_PLATFORM_STATE`, not exact-source trust, and can show whether a required-status gate is absent from the supplied state.

Residual: independently provider-retrieved current rulesets/branch protection and robust comparison to actual check-run identities.

For this repository, successful CI is not described as a guaranteed merge gate unless current platform evidence establishes that enforcement.

### Q — Overall Repository Portrait — IMPLEMENTED / INTEGRATED
Audit v2 composes exact REM v1.1 evidence, assurance domains, findings, explicit unknowns, remediation and a bounded verdict.

Residual is evidence depth and calibration, not creation of another portrait engine.

### R — Auditor Self-Quality Controls — IMPLEMENTED / ACTIVE
Adversarial component tests and golden end-to-end cases exercise exact binding, scan isolation, evidence misbinding, claim self-support, workflow false-green cases, mutable refs, test false positives, contract drift, supplied runtime/provenance/platform evidence and final report preservation.

Residual: more materially different golden subjects, duplicate-finding/severity calibration, isolation tests and measured repeatability. Do not call the synthetic suite an accuracy benchmark.

### S — Customer-facing Report Experience — IMPLEMENTED BOUNDED MARKDOWN BASELINE
The product deterministically renders exact subject, verdict, evidence states, findings, unknowns, remediation and supplied-evidence trust boundaries into Markdown without creating a second verdict engine.

Residual: improve presentation only when real customer use demonstrates a need. Do not build dashboard, billing, multi-tenant SaaS, Marketplace/App or heavy UI merely to make the product look complete.

## Audit v2 assurance domains

The integrated portrait contains 15 explicit assurance domains:

**Wave A** — Threat Model; Data Privacy; Agent Safety; Identity & Access.  
**Wave B** — Resilience; Incident Readiness; External Dependency Failure; Auditability & Forensics.  
**Wave C** — Model Evaluation; FinOps; Configuration; Concurrency.  
**Wave D** — Migration; Interface / Contract Compatibility; License / IP.

Presence of all 15 domains means the evidence contract is structurally present. It does **not** mean all domains passed.

## Evidence trust boundaries

- Exact Git-tree evidence is bound to the audited repository and source revision.
- `SUPPLIED_EXACT` means caller-supplied evidence passed strict subject/source validation; it is **not** independently fetched or authenticated by the Audit path.
- `SUPPLIED_PLATFORM_STATE` is time-bound branch/ruleset evidence; it is **not** commit-bound proof.
- Source-to-artifact provenance metadata does not by itself prove signature validity, builder trust, reproducibility, deployment success, vulnerability absence or release authorization.
- Static findings do not prove exploitability.
- Green CI does not prove economic, security, runtime or release correctness beyond the checks actually evidenced.

## Ownership / anti-twin rule

No new standalone repository is approved by this roadmap. AI Repository Audit remains the public audit/product surface. Deeper execution, supply-chain, runtime, policy, evidence-storage, provider or control-plane capability should integrate with existing accepted portfolio directions rather than create duplicate independently writable authorities.

## Residual engineering order

Feature expansion is no longer the default. Remaining engineering should be driven by a demonstrated evidence gap or real customer requirement.

Priority residuals:

1. Independently provider-authenticated GitHub execution/ruleset/attestation evidence where the available access model permits it.
2. Deepen typed claim/evidence, dependency and contract relations only where false-positive risk remains bounded.
3. Improve calibration, deduplication, information isolation and repeatability on golden/public subjects.
4. Keep public docs/examples current with accepted exact-head behavior.
5. Fix defects that block honest delivery of the existing scoped service.

Do **not** start speculative dashboard, GitHub App, billing platform, multi-tenant SaaS or broad integration expansion before customer evidence justifies it.

## Commercial validation boundary

Engineering maturity and market validation are separate. Current pricing, demand and product-market fit remain hypotheses until external customers pay and repeat.

The accepted commercial direction is to use the existing product to test a narrow release/handoff evidence service rather than continue broad feature expansion indefinitely. Real buyer questions should determine which residual technical gaps deserve priority.

## Definition of trustworthy progress

Progress requires, as applicable:

- exact-subject implementation;
- deterministic negative/adversarial tests;
- current candidate-SHA evidence;
- no false PASS or evidence-state loss;
- public-origin-only compliance;
- explicit static/runtime/external/platform evidence boundaries;
- integration impact review;
- truthful documentation;
- post-merge verification.

## Success criteria

The roadmap succeeds when materially different audits consistently produce repository-specific findings, exact-revision traceability, explicit unknowns/contradictions, useful remediation, reproducible evidence depth and low false-positive/duplicate rates — and when external customers demonstrate that the resulting decision support is worth paying for.

Until then, technical acceptance must not be confused with market acceptance.
