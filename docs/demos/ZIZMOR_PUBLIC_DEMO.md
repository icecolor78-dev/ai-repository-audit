# Independent Public Demo Audit — zizmor

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by the repository owner or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `zizmorcore/zizmor`
- Exact revision: `bb180c27ef1f03dd231d8ca536fce7bcf458dfa9`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

`zizmor` is itself a GitHub Actions security-analysis project, so it is a useful positive-control subject for evidence-first auditing. The sampled CI workflow runs linting, cross-platform tests, site-build checks, schema-consistency checks, and an aggregate all-tests gate. Third-party actions in the sampled CI are pinned to immutable commit SHAs and checkout disables persisted credentials.

The repository also runs `zizmor` against its own `.github/` directory. Importantly, the self-audit workflow explicitly says it intentionally does **not** scan the entire repository because the repository contains integration tests. That is valuable evidence semantics: the control exists, but its scope is bounded and should not be overstated.

These observations do **not** establish that the project is vulnerability-free or that every release/runtime path is fully verified. They show strong repository-visible controls plus one explicit scope boundary that an audit should preserve rather than hide.

## Observation 1 — CI covers several distinct verification classes

The sampled CI workflow runs formatting, Clippy linting, tests across Ubuntu/macOS/Windows, site-build verification, generated-schema consistency checks, and a final aggregate job that depends on the earlier verification jobs.

**Evidence state:** `PASS` for the presence of the sampled CI coverage.

**Why this matters:** a green result from this workflow can be interpreted more precisely because the repository exposes what the workflow actually checks. It still does not prove untested runtime or operational behavior.

## Observation 2 — Sampled third-party Actions are pinned to immutable revisions

The sampled CI references `actions/checkout`, `Swatinem/rust-cache`, `astral-sh/setup-uv`, and `re-actors/alls-green` by full commit SHA. The checkout steps also set `persist-credentials: false`.

**Evidence state:** `PASS` for sampled dependency pinning and checkout credential persistence control.

**Why this matters:** the workflow is materially more reconstructable than one using floating major tags. Account-side or runner-side controls remain outside this static review.

## Observation 3 — The project self-audits its GitHub Actions configuration

A dedicated workflow runs `zizmorcore/zizmor-action` against `./.github/`, with both checkout and the audit action pinned to immutable commit SHAs. The workflow grants only `security-events: write` to the audit job after starting from an empty top-level permission map.

**Evidence state:** `PASS` for the visible self-audit control.

**Why this matters:** security analysis is part of the repository's own CI process rather than only a product claim.

## Observation 4 — The self-audit scope is explicitly incomplete by design

The self-audit workflow comments that it intentionally does not scan the entire repository because integration tests are present, and passes only `./.github/` as input.

**Evidence state:** `PARTIAL`

**Why this matters:** this is exactly the kind of boundary that a green security job must not erase. The correct conclusion is that the sampled `.github/` scope is analyzed by that workflow; a whole-repository security conclusion would be unsupported.

## Observation 5 — The repository separates general feedback from security reporting

Its issue configuration links GitHub Discussions for questions and ideas, while potential security vulnerabilities are directed to GitHub Security Advisories.

**Evidence state:** `PASS` for the visible communication boundary.

**Why this matters:** non-sensitive feedback has an explicit public channel, while security-sensitive material has a separate private disclosure path.

## 15-domain v2 applicability snapshot

This is a bounded demonstration, not a full security or release audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | PARTIAL | Security-focused workflows are visible, but no complete project threat model was reviewed. |
| Data Privacy | UNVERIFIED | No privacy lifecycle conclusion established. |
| Migration | NOT_APPLICABLE | No migration claim tested. |
| Resilience | UNVERIFIED | No runtime recovery/failure-injection evidence sampled. |
| Concurrency | PARTIAL | CI concurrency cancellation is visible; application concurrency was not audited. |
| Config | PARTIAL | CI triggers, permissions, matrices and self-audit scope are visible. |
| Interface | PARTIAL | CLI/schema/build interfaces are tested in visible workflows; full compatibility not audited. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | PARTIAL | A dedicated security-reporting path is visible; operational response readiness was not audited. |
| License/IP | UNVERIFIED | No bounded license analysis performed here. |
| Identity & Access | PARTIAL | Explicit workflow permissions and disabled persisted checkout credentials are visible. |
| External Dependency Failure | UNVERIFIED | Dependency-failure behavior was not executed. |
| Auditability/Forensics | PASS | Exact revision, immutable action pins, explicit job scopes and aggregate test dependencies provide strong repository-visible traceability. |

## Calibration lesson

**A security control can PASS while the broader security claim remains PARTIAL.** The self-audit is concrete positive evidence, but its own configuration documents a deliberate scope boundary. Evidence-first reporting should preserve both facts at once.

## Outreach boundary

The project explicitly allows questions and ideas through GitHub Discussions and reserves Security Advisories for vulnerability reports. After our own post-merge verification, one concise, non-sensitive Discussion linking to this independent demo is an appropriate candidate. Do not place security-sensitive findings in Discussions.

## Limitations

This demo is not a penetration test, vulnerability assessment, certification, endorsement, or guarantee. It does not execute the project, inspect private infrastructure or organization settings, prove all release artifacts, or extend the repository's own self-audit beyond the scope configured in the sampled workflow.
