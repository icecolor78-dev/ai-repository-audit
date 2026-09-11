# Independent Public Demo Audit — cargo-make

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by the repository owner or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `sagiegurari/cargo-make`
- Exact revision: `95dcc545db8cf08af6fbec524e200e7c80b06027`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

The repository shows substantial cross-platform CI coverage: stable, beta and nightly Rust are exercised across Ubuntu, Windows and macOS. That is meaningful positive evidence. The same workflow, however, references several reusable actions and a Rust toolchain branch by mutable tags/branch names rather than immutable commit SHAs. The publish workflow is tag-triggered, but it also relies on mutable third-party action tags.

These observations do **not** mean cargo-make is insecure or incorrectly released. They define the evidence boundary: static YAML proves the intended matrix and release flow, but it does not by itself fully reconstruct the exact third-party implementations that executed historically.

## Observation 1 — CI matrix provides broad positive compatibility evidence

The `CI` workflow runs on both `push` and `pull_request` and covers `stable`, `beta`, and `nightly` Rust across Ubuntu, Windows, and macOS.

**Evidence state:** `PASS` for visible matrix intent; `PARTIAL` for full runtime confidence.

**Why this matters:** the matrix is much stronger evidence than a single-run green badge. It still does not establish that every supported behavior or dependency combination is covered.

## Observation 2 — CI dependencies are not fully immutable

The CI workflow uses `actions/checkout@v4`, `dtolnay/rust-toolchain@master`, and `Swatinem/rust-cache@v2`.

**Evidence state:** `OBSERVED`

**Why this matters:** mutable major tags and branch names can resolve to different implementations over time. Exact historical reconstruction therefore requires resolved-run provenance in addition to the static workflow file.

## Observation 3 — Release automation is tag-triggered but still depends on mutable actions

The `Publish` workflow runs on pushed tags and builds five binary targets. It uses `actions/checkout@v2`, `actions-rs/cargo@v1`, and `svenstaro/upload-release-action@v1-release`.

**Evidence state:** `PARTIAL`

**Why this matters:** the tag trigger is useful release-binding evidence, but the workflow does not make every external action implementation immutable. The release process is automated, while full historical reproducibility remains bounded by dependency provenance.

## 15-domain v2 applicability snapshot

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No full threat-model review performed. |
| Data Privacy | NOT_APPLICABLE | No privacy claim tested in this bounded demo. |
| Migration | UNVERIFIED | No migration path evaluated. |
| Resilience | PARTIAL | Cross-platform CI is visible; recovery behavior was not tested. |
| Concurrency | PARTIAL | CI declares concurrency cancellation, but broader concurrency safety was not audited. |
| Config | PARTIAL | CI/release configuration is visible. |
| Interface | PARTIAL | Multi-platform build behavior is exercised; complete interface compatibility was not established. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | UNVERIFIED | No incident-response evidence sampled. |
| License/IP | PARTIAL | Public license/dependency metadata exists; full license analysis was not performed. |
| Identity & Access | PARTIAL | `GITHUB_TOKEN` use is visible in publish automation; account-side controls are not. |
| External Dependency Failure | UNVERIFIED | No dependency-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact subject revision is frozen, but mutable workflow dependencies limit reconstruction from YAML alone. |

## Calibration lesson

**A broad green matrix can provide strong compatibility evidence without proving immutable execution provenance.** The correct result is to preserve the positive matrix evidence while keeping historical third-party action identity explicitly bounded.

## Outreach boundary

The repository has GitHub Discussions enabled. Before any outreach, the current contribution/discussion guidance should be checked and a single non-security, non-sales-pressure message used only if the channel is appropriate. Do not create an unsolicited bug Issue solely to advertise this demo.

## Limitations

This demo is not a penetration test, vulnerability assessment, certification, endorsement, or statement that `cargo-make` is secure or insecure. It does not execute the project, inspect private infrastructure, or prove historical artifact provenance beyond the public repository evidence sampled here.
