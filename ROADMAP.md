# AI Repository Audit Roadmap

This roadmap turns the service from a strong evidence-first review method into a repeatable repository-wide audit system. It is intentionally capability-oriented: new repositories/programs are created only when a genuinely separate ownership boundary, lifecycle, API, or data model is proven necessary.

## Product objective

Build an audit that answers, at one exact source revision:

1. What does this repository claim?
2. What evidence actually exists?
3. What is verified, weakly supported, stale, contradictory, or UNVERIFIED?
4. What can fail despite green CI?
5. What should be fixed first, and what evidence would prove the fix?

The target output is an **Overall Repository Portrait**, not a longer generic code review.

## Phase A — benchmark real audit depth

Run governed read-only dogfood on materially different public repositories and compare results using the same evidence model.

Current benchmark archetypes:
- backend / API;
- frontend / tooling;
- infrastructure / release-heavy;
- security-sensitive / cryptographic library;
- existing internal sanitized quantitative-system and adaptive-learning case studies.

For every subject capture:
- exact repository + commit SHA;
- evidence categories inspected;
- material findings by severity and confidence;
- UNVERIFIED / NOT_TESTED areas;
- actionable remediation steps;
- evidence-depth and coverage limitations;
- false-positive / low-value observations rejected during review.

Do not treat external public dogfood as customer work, endorsement, certification, or penetration testing.

## Phase B — Repository Evidence Mapper

Create a repository-intelligence layer that maps the exact subject before verdicting.

Target map:

`repository -> languages -> packages/modules -> workflows -> tests -> security checks -> release paths -> dependencies -> public claims -> evidence -> UNVERIFIED gaps`

Initial implementation should reuse existing Audit/PatchSeal capabilities. Do not create a separate program unless later evidence proves a distinct long-lived product boundary.

### Evidence Mapper outputs
- repository inventory and architecture surface;
- CI/workflow inventory;
- test inventory and test-to-subsystem map;
- release/publish path inventory;
- dependency and lockfile inventory;
- security-check inventory;
- documentation/claim inventory;
- exact-revision evidence references;
- confidence and evidence freshness;
- explicit unknowns.

## Phase C — CI Evidence Profiler

Go beyond "CI exists".

Analyze:
- required vs optional checks;
- branch/path filters and skipped changes;
- conditional jobs and success aggregators;
- runtime/language/version matrix;
- OS/architecture matrix;
- cancellation/retry semantics;
- permissions and token scope;
- action pinning and mutable references;
- release-only checks;
- stale/wrong-SHA evidence risks;
- whether green status can be achieved while meaningful work is skipped.

Output: CI confidence profile + false-green risk assessment.

## Phase D — Test Depth Map

Classify and map evidence from:
- unit tests;
- integration tests;
- end-to-end tests;
- smoke tests;
- contract/schema tests;
- property-based tests;
- fuzzing;
- security tests;
- compatibility tests;
- migration/upgrade tests;
- performance/regression tests;
- release artifact tests.

Map each meaningful subsystem to VERIFIED / PARTIAL / UNVERIFIED and explain why.

## Phase E — Release and Provenance Audit

Analyze:
- build reproducibility;
- source-to-artifact binding;
- release workflow authorization;
- artifact handoff between jobs;
- trusted publishing / OIDC usage;
- signing/provenance when present;
- action/dependency pinning;
- package/image publication paths;
- release smoke tests;
- rollback/recovery path;
- whether release evidence is exact-subject bound.

Output: release-confidence and provenance portrait.

## Phase F — Workflow Security Analysis

Audit GitHub automation and adjacent repository workflows for:
- excessive permissions;
- credential persistence;
- unsafe untrusted-input interpolation;
- pull_request_target / privileged-context hazards;
- third-party actions and mutable tags;
- secret exposure surfaces;
- artifact poisoning / cross-job trust;
- unsafe cache use;
- shell injection risk;
- dangerous release triggers;
- missing fail-closed behavior.

Reuse PatchSeal security/verdict authority rather than creating a competing security verdict engine.

## Phase G — Supply-chain and Dependency Health

Analyze:
- direct/transitive dependency inventory;
- lockfile presence and reproducibility;
- dependency pinning/update policy;
- dependency provenance where available;
- stale/abandoned dependencies;
- known vulnerability evidence where accessible;
- SBOM presence/quality;
- license inventory and incompatible-license risk;
- generated/vendor code boundaries;
- package-manager integrity settings.

This should evolve toward the existing SupplySeal direction rather than become a duplicate program.

## Phase H — Claims vs Evidence Matrix

Extract material claims from README/docs/release notes/configuration and compare them with actual evidence.

Examples:
- "supports X" -> compatibility evidence?
- "secure" -> what security evidence exists?
- "tested on Y" -> exact current CI matrix?
- "production ready" -> release/recovery/observability evidence?
- "reproducible" -> source/data/config/artifact binding?

Every claim is classified as:
- VERIFIED;
- PARTIAL;
- UNVERIFIED;
- CONTRADICTED;
- NOT_APPLICABLE.

This is a core differentiator of the product.

## Phase I — AI-assisted Change Provenance

When AI-assisted development evidence is visible, analyze:
- AI co-author/session provenance;
- exact source revision affected;
- whether human review boundaries are visible;
- whether tests cover changed semantics;
- generated-code boundaries;
- prompt/session evidence only when intentionally public and relevant;
- whether AI-generated changes receive weaker or stronger verification than equivalent human changes.

Do not claim AI authorship where repository evidence does not support it.

## Phase J — Architecture and Change-impact Analysis

Build an evidence-backed change/architecture portrait:
- module/package boundaries;
- dependency direction;
- public/internal API boundaries;
- high-coupling components;
- cycles where detectable;
- high-change hotspots;
- blast radius of changes;
- ownership/boundary violations;
- duplicated implementation authority;
- migration/compatibility layers;
- testability and failure-isolation gaps.

Avoid generic architecture scoring unsupported by repository evidence.

## Phase K — API / Contract Drift

Where applicable, compare:
- code vs public API docs;
- schemas vs consumers;
- CLI flags/configuration vs docs/examples;
- generated API specs vs implementation;
- migration/version compatibility contracts;
- deprecation policy vs actual behavior/tests.

Output explicit drift and compatibility-risk findings.

## Phase L — Documentation vs Runtime/Build Reality

Check whether:
- documented install commands are reproducible;
- examples compile/run where feasible;
- documented versions match supported versions;
- configuration examples match actual schema/defaults;
- README badges/current claims correspond to exact/current evidence;
- docs-only paths bypass important validation unexpectedly.

## Phase M — Performance and Resource Evidence

When relevant and evidence exists, inspect:
- benchmark infrastructure;
- regression thresholds;
- latency/throughput claims;
- memory/CPU/resource constraints;
- benchmark reproducibility;
- noisy or non-comparable benchmark design;
- performance checks in CI/release gates.

Missing performance evidence is UNVERIFIED, not an assumed defect.

## Phase N — Observability and Operability

For deployable/services repositories, inspect evidence for:
- structured logging;
- metrics;
- tracing;
- health/readiness signals;
- error reporting;
- graceful degradation;
- alerting/runbook hooks;
- rollback/recovery evidence;
- migration safety;
- operational failure modes.

This capability should converge with the existing RuntimeSeal direction where appropriate.

## Phase O — Maintainability and Hotspot Analysis

Analyze repository-visible maintainability evidence:
- change concentration/hotspots;
- complexity and duplication;
- oversized modules;
- brittle test coupling;
- ownership concentration / bus-factor signals where public history supports them;
- stale/dead code indicators;
- dependency on generated or vendored internals;
- repeated defect-prone boundaries.

Do not infer team quality from contributor counts alone.

## Phase P — Policy and Governance Evidence

Inspect:
- branch/ruleset protections where accessible;
- required checks;
- CODEOWNERS/review policies;
- security policy;
- contribution/release rules;
- dependency update automation;
- privilege boundaries;
- evidence retention/provenance practices;
- whether repository policy matches actual enforcement.

Reuse existing engineering-governance/PolicySeal direction rather than create a twin.

## Phase Q — Overall Repository Portrait

Full Audit final output should converge on one structured portrait:

### 1. Exact subject
Repository, exact SHA, audit scope, timestamp/evidence freshness.

### 2. Executive verdict
PASS / HOLD / REJECT / ESCALATE only where the applicable evidence model supports such a verdict; otherwise explicitly state bounded confidence and UNVERIFIED areas.

### 3. Evidence scorecard
At minimum:
- CI confidence;
- test depth;
- security/workflow posture;
- release/provenance confidence;
- supply-chain health;
- architecture/maintainability;
- claims-vs-evidence consistency;
- runtime/operability when applicable.

Scores must never hide missing evidence. Numeric scoring, if introduced, must preserve the underlying evidence state and cannot convert UNVERIFIED into PASS.

### 4. Findings
All material findings in agreed scope, not an arbitrary fixed count.

Each finding should include:
- severity;
- confidence;
- exact evidence reference;
- why it matters;
- affected boundary;
- remediation;
- verification required after remediation.

### 5. UNVERIFIED map
Explicitly list important things the audit could not prove.

### 6. Remediation roadmap
Prioritized by risk, evidence value and implementation cost/complexity where reasonably inferable.

## Phase R — Quality controls for the auditor itself

The audit system must test itself for:
- false positives;
- duplicate findings;
- unsupported severity inflation;
- stale-SHA references;
- claim/evidence misbinding;
- missing negative evidence;
- hallucinated files/tests/workflows;
- generic advice that is not repository-specific;
- inconsistent results across repeated review of the same exact subject;
- information leakage between audited repositories.

Maintain benchmark/golden cases as the method matures.

## Phase S — Customer-facing report experience

After technical depth is proven, improve presentation:
- concise executive summary;
- evidence matrix;
- severity/confidence filtering;
- finding-to-file/workflow references;
- remediation checklist;
- printable/exportable Full Audit report;
- clear Free Demo vs Full Audit boundary;
- sanitized shareable summary when requested.

Do not add heavy dashboard/SaaS infrastructure before real demand justifies it.

## Public next-release capability set

The next release cycle is targeting these capability areas:

- Claims vs Evidence Matrix;
- CI Evidence Profiler;
- Test Depth Map;
- Release and Provenance Audit;
- Workflow Security Analysis;
- Supply-chain and Dependency Health;
- Architecture and Change-impact Analysis;
- API, Contract and Documentation Drift;
- Runtime, Performance and Observability Evidence;
- Auditor Self-Quality and Golden Cases;
- Customer-facing Report Experience.

Active implementation is developed on a private engineering surface. This public roadmap communicates product direction only; it does **not** claim that any unreleased capability is already available, complete, verified, or release-ready. Reviewed public-safe artifacts are published here when they reach the appropriate release boundary.

## Program ownership / anti-twin decision

No new standalone repository is approved by this roadmap today.

Default ownership remains:
- PatchSeal: verification/security/quality/verdict composition;
- local-test-hub: reproducible bounded execution;
- Evidence-Vault: durable exact-subject evidence;
- GitHub-integration: GitHub transport/provider boundary;
- Platform-Control-Plane: customer/tenant/commercial surface;
- AI-Orchestrator: workflow coordination;
- future SupplySeal / RuntimeSeal / PolicySeal directions: extend their already-defined domains when real demand requires them.

A future `Repository Intelligence`, `RepoSeal`, or `Evidence Mapper` program may be proposed only if dogfood demonstrates all of the following:
1. a distinct stable domain boundary;
2. a separate lifecycle/API/data model;
3. enough functionality that embedding it in PatchSeal/Audit creates harmful coupling;
4. no duplication of an existing canonical owner;
5. a concrete customer/product reason to pay the complexity cost.

Until then, implement Repository Evidence Mapper as an Audit/PatchSeal capability layer.

## Near-term execution order

1. Complete public dogfood benchmark batch (#14).
2. Produce a cross-dogfood gap matrix.
3. Define Repository Evidence Mapper v1 schema/output.
4. Add CI Evidence Profiler and Test Depth Map.
5. Add Claims-vs-Evidence Matrix.
6. Add Release/Provenance + Workflow Security analysis.
7. Add Dependency/Supply-chain health.
8. Add Architecture/Change-impact + API/docs drift.
9. Add Runtime/Performance/Observability where applicable.
10. Build Overall Repository Portrait v1.
11. Add auditor self-quality/golden-case checks.
12. Validate on additional real repositories before increasing automation/price based on assumed value.

## Success criteria

The roadmap is successful when repeated audits on different repository archetypes consistently produce:
- repository-specific findings rather than generic advice;
- exact-revision evidence traceability;
- explicit UNVERIFIED areas;
- useful remediation steps;
- comparable evidence-depth metrics;
- low false-positive/duplicate rates;
- materially deeper Full Audit output than Free Demo;
- enough demonstrated value to support the owner-approved pricing escalation policy using real customer evidence.
