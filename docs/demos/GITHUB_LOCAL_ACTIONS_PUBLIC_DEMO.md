# Independent Public Demo Audit — GitHub Local Actions

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by the repository owner or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `SanjulaGanepola/github-local-actions`
- Exact revision: `bc25f97d709188cc9d1669763d8d447e418c3634`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

This repository is a useful demonstration of why a working CI/release setup and exact-revision release evidence are not the same thing. The visible build workflow runs on pull requests and pushes to `main`, packages a VSIX artifact, and provides positive automation evidence. The separate publish workflow can run manually or on release creation, but it explicitly checks out `main` rather than tying checkout to the release/tag revision. Both workflows also reference GitHub Actions by mutable major-version tags and install some tooling without immutable version locks.

These observations do **not** establish that the project is insecure, broken, or incorrectly released. They establish narrower evidence boundaries: static workflow text alone does not prove that a published marketplace artifact corresponds to the exact release revision, nor does it fully reconstruct all third-party implementation versions that executed.

## Observation 1 — Build/package automation is visible for PRs and pushes

The `webpack` workflow runs for pull requests and pushes targeting `main`, installs dependencies, builds with webpack, packages the VS Code extension, and uploads the resulting VSIX artifact.

**Evidence state:** `PARTIAL`

**Why this matters:** this is useful positive evidence that changes are automatically built and packaged. This bounded demo does not establish test completeness, runtime behavior, or release identity.

## Observation 2 — Release publication checks out `main`, not the release revision

The `Publish to the Marketplace and Open VSX` workflow is triggered manually or when a release is created. Its checkout step sets `ref: main`.

**Evidence state:** `OBSERVED`

**Why this matters:** a release event identifies a release/tag context, but the workflow text instructs checkout of the branch tip. Static repository evidence therefore does not prove that the code published to Open VSX or the VS Marketplace is the exact commit associated with the triggering release. Proving that identity would require additional run/artifact evidence or an immutable release checkout rule.

This is an evidence/provenance observation, not a statement that any historical release was wrong.

## Observation 3 — Workflow dependencies and publish tooling are not fully immutable

The sampled workflows reference `actions/checkout@v4`, `actions/setup-node@v4`, and `actions/upload-artifact@v4`. They also install `vsce` / `ovsx` globally without an explicit version in the workflow.

**Evidence state:** `OBSERVED`

**Why this matters:** major-version action tags and unversioned tool installs are operationally convenient, but future executions of the same YAML may resolve to different implementations. Exact historical reconstruction therefore requires resolved-run evidence beyond the static file.

## Observation 4 — The project explicitly offers Discussions for non-sensitive feedback

The public README states that project-specific issues or feature requests may be opened as Issues or posted on the Discussion board.

**Evidence state:** `PASS` for the visible communication path.

**Why this matters:** this gives a clear public feedback channel for a non-sensitive independent demo. Any security-sensitive material remains outside the scope of this public report.

## 15-domain v2 applicability snapshot

This is a bounded demonstration, not a full security or release audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No complete threat-model review performed. |
| Data Privacy | UNVERIFIED | Settings include secrets/variables handling, but privacy lifecycle was not audited. |
| Migration | NOT_APPLICABLE | No migration claim tested. |
| Resilience | UNVERIFIED | No recovery/failure-injection evidence sampled. |
| Concurrency | UNVERIFIED | No concurrency conclusion established. |
| Config | PARTIAL | Workflow triggers, runner, registry and publish configuration are visible. |
| Interface | PARTIAL | Extension packaging and public action-facing behavior are visible; compatibility was not fully audited. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | UNVERIFIED | No operational incident-response conclusion established. |
| License/IP | PARTIAL | Public licensing/dependency metadata is repository-visible; broader dependency-license review not performed. |
| Identity & Access | PARTIAL | Marketplace/Open VSX token use is visible, but account-side controls are not. |
| External Dependency Failure | UNVERIFIED | No dependency-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact subject revision is frozen, but release checkout and mutable dependency resolution limit reconstruction from static YAML alone. |

## Calibration lesson

**A release workflow can be automated without static repository evidence proving exact release-to-artifact identity.** When a release-triggered workflow checks out a moving branch and uses mutable dependencies, the correct audit output is to preserve the positive automation evidence while keeping release identity/provenance explicitly `PARTIAL` or `UNVERIFIED` until stronger run/artifact evidence exists.

## Outreach boundary

The repository README explicitly allows project-specific feedback through GitHub Discussions. A single concise, non-security, non-sales-pressure message linking to this independent demo is therefore an appropriate candidate after our own post-merge verification. Do not use that channel for security-sensitive findings.

## Limitations

This demo is not a penetration test, vulnerability assessment, certification, endorsement, or statement that `github-local-actions` is secure or insecure. It does not execute the project, inspect private infrastructure, inspect marketplace account controls, prove historical artifact identity, or validate secrets handling beyond the public repository evidence sampled here.
