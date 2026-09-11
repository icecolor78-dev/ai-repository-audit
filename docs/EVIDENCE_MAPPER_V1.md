# Repository Evidence Mapper v1

Status: proposed v1 contract for AI Repository Audit.

## Purpose

Repository Evidence Mapper (REM) creates an exact-subject, machine-readable evidence portrait before any audit verdict is composed. It answers what evidence exists, what it proves, how fresh it is, and what remains unknown.

REM is an Audit/PatchSeal capability layer, not a new standalone product or verdict authority.

## Core invariants

1. Every portrait is bound to one repository and one exact source revision.
2. Evidence about a different revision cannot silently prove the current subject.
3. Missing, inaccessible, stale, skipped, conditional, or externally-hosted evidence is represented explicitly.
4. Absence of evidence is not automatically evidence of a defect.
5. A green CI state is evidence only for the checks that actually ran for the exact subject.
6. PR confidence and release confidence are distinct.
7. Security evidence freshness is distinct from general CI freshness.
8. Numeric summaries must not convert UNVERIFIED into PASS.
9. Findings and verdicts remain downstream consumers; REM maps evidence rather than inventing severity.
10. Public output must not leak private identifiers, credentials, customer data, proprietary internals, or reconstruction-enabling details.

## Evidence states

Every material coverage assertion uses one of:

- `VERIFIED`: direct evidence supports the assertion for the exact subject.
- `PARTIAL`: evidence supports only part of the assertion or coverage surface.
- `UNVERIFIED`: evidence required to support or reject the assertion is unavailable, inaccessible, not run, stale, or out of scope.
- `CONTRADICTED`: available evidence materially conflicts with the assertion.
- `NOT_APPLICABLE`: the dimension does not reasonably apply to this subject.

Optional execution state may further distinguish:

- `PASSED`
- `FAILED`
- `SKIPPED`
- `NOT_RUN`
- `INACCESSIBLE`
- `UNKNOWN`

Execution state never replaces evidence state.

## Canonical portrait

```yaml
schema_version: rem/v1
subject:
  provider: github
  repository: owner/repo
  revision: full-commit-sha
  default_branch: main
  observed_at: RFC3339 timestamp
  visibility: public|private

inventory:
  languages: []
  manifests: []
  lockfiles: []
  modules: []
  generated_or_vendor_boundaries: []

ci:
  workflows: []
  required_checks: []
  trigger_model: []
  path_filters: []
  runtime_matrix: []
  os_arch_matrix: []
  conditional_jobs: []
  aggregate_checks: []
  exact_subject_runs: []
  confidence: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
  unknowns: []

tests:
  suites: []
  types: []
  subsystem_map: []
  exact_subject_execution: []
  confidence: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
  unknowns: []

security:
  workflow_permissions: []
  credential_persistence: []
  action_pinning: []
  static_analysis: []
  dependency_security: []
  secret_scanning_evidence: []
  freshness: []
  confidence: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
  unknowns: []

release:
  workflows: []
  artifact_handoffs: []
  source_artifact_binding: []
  trusted_publishing: []
  signing_or_attestation: []
  smoke_or_release_tests: []
  rollback_or_recovery: []
  confidence: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
  unknowns: []

supply_chain:
  dependencies: []
  update_automation: []
  sbom: []
  license_evidence: []
  provenance: []
  confidence: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
  unknowns: []

claims:
  items:
    - claim: string
      source_ref: evidence-ref
      state: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
      supporting_refs: []
      contradicting_refs: []
      notes: string

provenance:
  ai_assisted_changes: []
  generated_code: []
  external_build_or_test_services: []
  confidence: VERIFIED|PARTIAL|UNVERIFIED|CONTRADICTED|NOT_APPLICABLE
  unknowns: []

coverage:
  dimensions: []
  explicit_unknowns: []
  excluded_scope: []

sources: []
```

The example is descriptive, not a promise that every field is populated for every repository.

## Evidence reference

Every reusable evidence item should contain:

```yaml
id: stable-local-id
kind: repository_file|workflow_definition|workflow_run|workflow_job|commit|status|release|issue|pull_request|external
subject_revision: full-commit-sha
locator: provider-specific locator
observed_at: RFC3339 timestamp
freshness:
  state: exact|current-but-not-exact|historical|unknown
  reason: string
access:
  state: accessible|partial|inaccessible
content_digest: optional digest
supports: []
limits: []
```

Rules:
- `subject_revision` is mandatory for repository-bound evidence.
- evidence from another SHA is `historical` unless explicitly used for history/change analysis.
- external evidence must state its binding limitation.
- inaccessible evidence remains a source record with an explicit limit; it does not disappear from the portrait.

## CI Evidence Profiler contract

For each workflow record:
- path + exact blob/ref;
- triggers and event types;
- branch/tag/path filters;
- job graph and conditional expressions;
- permissions;
- checkout credential behavior;
- third-party action references and pinning;
- runtime/OS/architecture matrix;
- cache/artifact handoffs;
- aggregate/all-green semantics;
- exact-subject run evidence when accessible;
- checks known to run only after merge, on schedule, manually, or on release.

Derived states must include separate:
- `pr_confidence`;
- `main_confidence`;
- `release_confidence`;
- `security_evidence_freshness`.

## Test Depth Map contract

Test evidence is classified by type and subsystem. At minimum support:
- unit;
- integration;
- end-to-end;
- smoke;
- contract/schema;
- property;
- fuzz;
- security;
- compatibility;
- migration/upgrade;
- performance/regression;
- release-artifact.

Each subsystem mapping states whether the relevant tests are discovered, executed for the exact subject, skipped/conditional, externally executed, or unknown.

Test-file count alone is never a test-depth score.

## Release/provenance contract

Capture separately from PR CI:
- release trigger;
- authorization/permissions;
- source checkout/ref semantics;
- artifact producer and consumer chain;
- trusted publishing/OIDC;
- signing/attestation;
- release tag/source binding;
- release smoke validation;
- external registry/package evidence when in scope;
- rollback/recovery evidence when applicable.

A successful PR test run cannot substitute for missing release evidence.

## Claims vs Evidence contract

Material claims may originate from README, docs, release documentation, configuration, package metadata, badges, or explicit project policy.

Each claim requires:
- exact claim source;
- normalized assertion;
- applicable evidence dimension;
- supporting/contradicting evidence refs;
- evidence state;
- explanation of limitations.

Do not create negative findings merely because a marketing-style claim is broad; report the evidence boundary precisely.

## AI-assisted change provenance

If public repository evidence explicitly identifies AI assistance, REM may record:
- provenance source;
- affected commit/revision;
- visible co-author/session/tool metadata;
- whether changed semantics have exact-subject verification evidence.

AI assistance is not itself a vulnerability, defect, or severity signal.

## External evidence

Examples include documentation builders, external CI, package registries, coverage services, hosted security scanners, or deployment systems.

REM records:
- existence/source;
- accessibility;
- revision binding if provable;
- freshness;
- what it could prove;
- what remains UNVERIFIED.

Never translate an inaccessible badge/service into VERIFIED.

## Multidimensional confidence

v1 does not define one global numeric repository score.

Required dimensions are at least:
- CI;
- tests;
- workflow security;
- release/provenance;
- supply chain;
- claims consistency.

Architecture, runtime/operability, performance, maintainability, API/contract drift, and governance can be added when applicable and sufficiently evidenced.

The Overall Repository Portrait may summarize these dimensions, but underlying evidence states and unknowns remain visible.

## v1 boundaries

REM v1 does not by itself:
- execute arbitrary untrusted repository code;
- perform penetration testing;
- certify security or compliance;
- guarantee absence of vulnerabilities;
- infer production runtime behavior without runtime evidence;
- declare commercial/release readiness from repository evidence alone when material external dependencies are unknown;
- replace PatchSeal verdict composition;
- replace Local Test Hub execution;
- replace Evidence Vault durable evidence storage;
- create a new canonical owner for SupplySeal/RuntimeSeal/PolicySeal domains.

## Dogfood-derived requirements

The v1 contract is specifically designed to represent patterns observed in the public dogfood batch:
- workflows whose path filters mean green CI does not cover all repository changes;
- scheduled/manual security scanning that is not exact-PR evidence;
- fast PR checks separated from broader post-merge/release matrices;
- trusted publishing and artifact attestation chains;
- explicit AI-assisted commit provenance;
- externally-hosted documentation/build evidence.

## Acceptance examples

A conforming mapper must be able to express without ambiguity:

1. "PR tests passed, but architecture-specific release checks were not run for this PR" -> PR evidence may be VERIFIED/PARTIAL while release confidence remains PARTIAL or UNVERIFIED.
2. "Semgrep exists but last exact-subject scan is not evidenced" -> scanner presence VERIFIED, exact-subject security freshness UNVERIFIED.
3. "Release uses OIDC trusted publishing and attestation" -> those mechanisms VERIFIED when exact workflow evidence supports them; successful publication remains separate evidence.
4. "Docs are built by an external service whose exact revision result is inaccessible" -> build configuration VERIFIED, exact build result UNVERIFIED.
5. "Commit metadata explicitly records AI assistance" -> provenance VERIFIED; code quality/security remains determined by independent evidence.

## Next implementation slices

After this contract is accepted:
1. define a concrete JSON Schema or typed model;
2. implement repository/workflow inventory extraction;
3. implement CI trigger/path/permission/action-pinning normalization;
4. implement test discovery/type classification;
5. implement release/provenance extraction;
6. implement claims extraction and evidence linking;
7. generate an Overall Repository Portrait fixture for each dogfood archetype;
8. add golden tests for stale-SHA, skipped-check, external-evidence and UNVERIFIED handling.
