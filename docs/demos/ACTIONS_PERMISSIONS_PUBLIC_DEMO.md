# Independent Public Demo Audit — actions-permissions

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by GitHub, GitHub Security Lab, the repository owner, or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `GitHubSecurityLab/actions-permissions`
- Exact revision: `bf82d13b9b10051d224345ab9184f5ede0a94289`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

This repository is a useful evidence-first subject because its purpose is to observe actual `GITHUB_TOKEN` usage and recommend minimum workflow permissions. The README explicitly describes least privilege as the goal, explains that one workflow run may be incomplete because steps/jobs can be skipped, and says the Advisor action aggregates recommendations from multiple runs.

The sampled repository test workflow declares read-only repository permissions at workflow level and exercises the Monitor action across a broad runner matrix. At the same time, several action references in that workflow use mutable branch/major-version refs such as `monitor@main`, `actions/checkout@v4`, and `actions/github-script@v7`. That does not make the project insecure; it means the static workflow text alone cannot identify the exact implementation revision that every future run will execute.

## Observation 1 — The product model explicitly accounts for conditional/skipped execution

The README states that some steps or jobs may be skipped based on conditions and that the Advisor action can aggregate recommendations from multiple workflow runs.

**Evidence state:** `PASS` for the documented evidence model.

**Why this matters:** a single green run is not treated as universal evidence. The repository itself recognizes that observed permission use is path-dependent, which aligns with evidence-first audit semantics.

## Observation 2 — The sampled workflow declares bounded read permissions

The test workflow sets workflow-level permissions to `contents: read`, `issues: read`, and `pull-requests: read`.

**Evidence state:** `PASS` for the visible permission declaration.

**Why this matters:** the requested token scope is explicit and inspectable rather than relying on an unspecified default. This does not prove organization-level defaults or every other consumer workflow.

## Observation 3 — The test matrix intentionally samples many GitHub-hosted runner variants

The sampled workflow defines a non-fail-fast matrix across multiple Ubuntu and macOS runner labels, including current, older, large/xlarge, ARM and preview variants; Windows entries are present but commented out.

**Evidence state:** `PARTIAL`

**Why this matters:** there is positive evidence of environment breadth, but the active matrix is not equivalent to all supported platforms. In particular, the commented Windows entries are not execution evidence.

## Observation 4 — Several action dependencies are referenced by mutable names

The sampled workflow uses `GitHubSecurityLab/actions-permissions/monitor@main`, `actions/checkout@v4`, and `actions/github-script@v7`.

**Evidence state:** `OBSERVED`

**Why this matters:** future executions of the same YAML can resolve to implementations different from those used historically. Exact run reconstruction therefore requires resolved action/run evidence in addition to the static workflow file.

This is an auditability/provenance observation, not a claim that the referenced actions are unsafe.

## Observation 5 — Public Discussions exist, but an explicit outreach instruction was not established in this bounded check

Repository metadata shows GitHub Discussions are enabled. The checked `.github/ISSUE_TEMPLATE/config.yml` path was not present, and this bounded review did not establish an explicit maintainer instruction that Discussions should be used for unsolicited project feedback.

**Evidence state:** `PARTIAL` for outreach suitability.

**Why this matters:** availability of a channel is not the same as permission or preference to use it. The safe current action is to publish the independent demo in our own repository but hold maintainer outreach until a clearly appropriate public feedback path is confirmed.

## 15-domain v2 applicability snapshot

This is a bounded demonstration, not a full security or release audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | PARTIAL | Least-privilege concerns are central to the project, but no complete threat model was reviewed. |
| Data Privacy | UNVERIFIED | No privacy lifecycle conclusion established. |
| Migration | NOT_APPLICABLE | No migration claim tested. |
| Resilience | UNVERIFIED | No recovery or failure-injection behavior sampled. |
| Concurrency | UNVERIFIED | No application concurrency conclusion established. |
| Config | PARTIAL | Permission declarations, matrix and workflow inputs are visible. |
| Interface | PARTIAL | Monitor/Advisor usage is documented; compatibility was not fully audited. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | UNVERIFIED | No incident-response conclusion established. |
| License/IP | PARTIAL | Public repository metadata exposes licensing context; no dependency-license review performed. |
| Identity & Access | PASS | The reviewed material is explicitly about GitHub token permission minimization and declares bounded read scopes in the sampled workflow. |
| External Dependency Failure | UNVERIFIED | No dependency-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact subject revision is frozen, but mutable action refs limit reconstruction from static YAML alone. |

## Calibration lesson

**Observed runtime behavior can be better evidence than static intention, but observation coverage is conditional.** A least-privilege advisor that aggregates multiple runs addresses this directly; the audit still must distinguish observed paths from unexecuted paths and static workflow dependency identity from resolved-run identity.

## Outreach boundary

No outreach should be sent yet from this demo alone. Discussions are technically enabled, but this bounded check did not establish a maintainer instruction that unsolicited audit feedback belongs there. Keep any outreach on HOLD until an appropriate project-defined channel is confirmed. Do not use bug or security-reporting Issues for promotion.

## Limitations

This demo is not a penetration test, certification, endorsement, legal/compliance opinion, or guarantee. It does not execute Monitor/Advisor, inspect private organization settings, reconstruct historical resolved action versions, or prove the minimum permissions of arbitrary third-party workflows.
