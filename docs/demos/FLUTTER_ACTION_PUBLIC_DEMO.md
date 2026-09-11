# Independent Public Demo Audit — flutter-action

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by the repository owner or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `subosito/flutter-action`
- Exact revision: `4cab68ce0f1c7c924f688bff4792e044f1aeb30c`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

The repository exposes a large multi-platform test matrix covering multiple Flutter channels, dry-run behavior, cache behavior, version-file handling, and several alternative Flutter sources. This is strong positive behavioral evidence for a GitHub Action. At the same time, pull-request execution is path-filtered to a small set of files, and at least one lint dependency is referenced through a mutable branch (`ludeeus/action-shellcheck@master`).

These observations do **not** mean flutter-action is unsafe or incorrectly tested. They show why a green workflow must be interpreted together with its trigger scope and dependency provenance.

## Observation 1 — The test workflow exercises a broad behavioral matrix

The workflow runs across Ubuntu, Windows, and macOS and tests stable/beta/master channels, dry-run behavior, cache behavior, version-file handling, specific Flutter revisions, and alternative source repositories.

**Evidence state:** `PASS` for visible test breadth; `PARTIAL` for complete product behavior.

**Why this matters:** this is materially stronger evidence than a single smoke test and demonstrates multiple real configuration paths.

## Observation 2 — Pull-request CI is explicitly path-filtered

For `pull_request`, the workflow is triggered only when `setup.sh`, `action.yaml`, or `.github/workflows/workflow.yaml` changes.

**Evidence state:** `OBSERVED`

**Why this matters:** changes elsewhere in the repository can fall outside this PR workflow trigger. A green badge therefore proves the checks that actually ran, not that every PR path necessarily exercised this workflow.

## Observation 3 — Not every workflow dependency is immutable

The workflow uses `actions/checkout@v6` and `ludeeus/action-shellcheck@master`.

**Evidence state:** `OBSERVED`

**Why this matters:** branch- or major-tag references are convenient but can move. Exact historical execution identity therefore requires resolved-run evidence beyond static YAML alone.

## Observation 4 — Version pinning is an explicit project concern

The frozen subject commit itself is titled `Enforce SHA pinning templates (#399)`, showing that immutable-reference discipline is already an explicit maintenance concern in the project.

**Evidence state:** `OBSERVED`

**Why this matters:** the audit should distinguish between a repository that ignores provenance entirely and one that is actively tightening it. The correct output preserves both the positive governance signal and the remaining evidence boundary.

## 15-domain v2 applicability snapshot

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No full threat-model review performed. |
| Data Privacy | UNVERIFIED | External source/mirror behavior exists, but privacy lifecycle was not audited. |
| Migration | PARTIAL | Multiple Flutter channels/versions are exercised; migration safety was not fully tested. |
| Resilience | PARTIAL | Multi-source/multi-platform paths are tested; failure recovery remains unverified. |
| Concurrency | UNVERIFIED | No concurrency conclusion established. |
| Config | PASS | Many action inputs/configuration paths are explicitly exercised in CI. |
| Interface | PARTIAL | Action inputs and outputs are tested, but complete compatibility is not proven. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | UNVERIFIED | No incident-response evidence sampled. |
| License/IP | PARTIAL | Public license/dependency metadata exists; full analysis was not performed. |
| Identity & Access | UNVERIFIED | No account-side authorization controls were reviewed. |
| External Dependency Failure | PARTIAL | Multiple external Flutter sources are exercised, but explicit failure injection was not sampled. |
| Auditability/Forensics | PARTIAL | Exact subject revision is frozen; mutable workflow references limit complete reconstruction from static YAML alone. |

## Calibration lesson

**Test breadth and trigger breadth are different dimensions.** A repository can have an excellent matrix once the workflow starts, while path filters still define where that evidence is absent. Audit output should preserve both facts instead of collapsing them into one green score.

## Outreach boundary

GitHub Discussions are enabled for this repository. Before outreach, current contribution/discussion guidance should be checked. If appropriate, use one concise, non-security, non-sales-pressure message; do not open an unsolicited bug Issue solely to advertise this demo.

## Limitations

This demo is not a penetration test, vulnerability assessment, certification, endorsement, or statement that `flutter-action` is secure or insecure. It does not execute the action, inspect private infrastructure, or establish complete runtime/release guarantees beyond the public repository evidence sampled here.
