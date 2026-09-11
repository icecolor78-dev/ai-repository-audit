# Independent Public Demo Audit — git-auto-commit-action

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by the repository owner or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `stefanzweifel/git-auto-commit-action`
- Exact revision: `92648143fd6aebb695590bfe3fc28f92bcf383e4`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

This repository is a useful demonstration of why a green workflow result and reproducible supply-chain evidence are related but not identical. The visible CI runs tests and linting, while several workflow dependencies are referenced through moving major or `latest` tags rather than immutable commit SHAs. The release-versioning path also grants `contents: write` to a job that invokes a third-party action through a moving `latest` tag.

These observations do **not** establish that the repository is insecure or compromised. They establish a narrower evidence point: when workflow dependencies are mutable, reproducing exactly which third-party implementation executed requires evidence beyond the workflow file alone.

## Observation 1 — Tests run on pull requests and pushes to the default branch

The `tests` workflow runs on pull requests and pushes to `master`, installs dependencies, and runs the project test command.

**Evidence state:** `PARTIAL`

**Why this matters:** repository-visible automated tests are positive evidence. This bounded demo does not establish the completeness of the test suite, runtime coverage, or behavior outside the exercised environment.

## Observation 2 — CI actions use mutable major-version references

The test workflow references `actions/checkout@v7`. The linter workflow references both `actions/checkout@v7` and `github/super-linter@v7`.

**Evidence state:** `OBSERVED`

**Why this matters:** major-version tags are convenient and commonly used, but they are not immutable references. A future resolution of the same workflow text may select a different upstream implementation than the one used for the frozen run. Exact executed-action provenance therefore requires run-time or resolved-SHA evidence rather than inference from the YAML alone.

## Observation 3 — Release-versioning job combines write permission with a moving third-party action tag

The `Keep the versions up-to-date` workflow grants `contents: write` and invokes `Actions-R-Us/actions-tagger@latest` when a release is published or edited.

**Evidence state:** `OBSERVED`

**Why this matters:** this is not a vulnerability claim. It is an evidence-boundary observation: a write-capable workflow whose third-party dependency is selected by a moving `latest` tag has weaker static reproducibility than the same workflow pinned to an immutable action revision.

## Observation 4 — Public security reporting guidance is explicit

The repository's security policy instructs reporters to use a private email address for security-related issues rather than the public issue tracker.

**Evidence state:** `PASS` for the visible reporting-path control.

**Why this matters:** the repository provides a clear private path for sensitive reports. This demo intentionally contains no vulnerability disclosure and no exploit-oriented claim.

## 15-domain v2 applicability snapshot

This is a bounded demonstration, not a full security or release audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No complete threat-model review performed. |
| Data Privacy | NOT_APPLICABLE | No privacy/data-lifecycle claim tested in this sample. |
| Migration | NOT_APPLICABLE | No migration claim tested. |
| Resilience | UNVERIFIED | CI execution is not recovery/failure-injection evidence. |
| Concurrency | UNVERIFIED | No concurrency conclusion established. |
| Config | PARTIAL | Workflow triggers, environment and permissions are visible. |
| Interface | PARTIAL | Public action inputs/behavior are repository-visible, but compatibility was not fully audited. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | PARTIAL | A private security reporting path is documented; operational incident handling remains unverified. |
| License/IP | PARTIAL | Public license metadata is visible; broader dependency-license review not performed. |
| Identity & Access | PARTIAL | Workflow token permission scope is visible in sampled jobs. |
| External Dependency Failure | UNVERIFIED | No dependency-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact subject revision is frozen, but moving action tags limit what can be reconstructed from static YAML alone. |

## Calibration lesson

**A workflow can be useful and green while its exact third-party execution provenance remains only partially reconstructable from static repository evidence.** The correct audit output is not a blanket failure; it is to separate positive CI evidence from unresolved provenance and reproducibility evidence.

## Outreach boundary

The repository has GitHub Discussions enabled. Before any outreach, the current Discussion categories and repository communication guidance must be checked. Do not use the public issue tracker for security material; the repository explicitly directs security reports to its private security channel.

## Limitations

This demo is not a penetration test, vulnerability assessment, certification, endorsement, or statement that `git-auto-commit-action` is secure or insecure. It does not execute the project, inspect private infrastructure, validate account protections, or prove historical workflow resolution beyond the public evidence sampled here.