# Independent Public Demo Audit — Flask

> **Independent public demonstration.** This audit was not requested, commissioned, sponsored, or endorsed by the Flask project or its maintainers. It reviews only publicly accessible repository evidence at the exact revision below.

## Subject

- Repository: `pallets/flask`
- Exact revision: `d73fa1cdcbd8b1465c151db8924ba58b1dd14e35`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

The repository exposes a mature and intentionally scoped CI setup. The key demonstration lesson is not that the project is "unsafe"; it is that even strong green CI has a defined evidence boundary. At this revision, the primary test workflow deliberately ignores documentation-only changes, while workflow-security analysis is scoped to YAML changes. Therefore a green result must be interpreted as evidence about the checks and paths that actually ran, not as a universal repository-wide safety claim.

## Observation 1 — Primary tests intentionally skip docs-only changes

The `Tests` workflow is configured with `paths-ignore: ['docs/**', 'README.md']` for both pull requests and pushes to `main`/`stable`.

**Evidence:** `.github/workflows/tests.yaml` at the exact subject revision.

**Interpretation:** this is a reasonable optimization, but it means a docs-only change can be green without executing the primary test matrix. The correct evidence statement is therefore scoped: tests passed for revisions where this workflow actually ran; documentation-only changes require different evidence if documentation/runtime consistency matters.

**State:** `PARTIAL` evidence for repository-wide change verification.

## Observation 2 — Workflow security analysis is path-scoped

The `zizmor` workflow runs on pull requests and pushes only when matching YAML files change.

**Evidence:** `.github/workflows/zizmor.yaml` at the exact subject revision.

**Interpretation:** the repository has explicit workflow-security analysis, which is strong positive evidence. At the same time, a green `zizmor` result should not be generalized to unrelated source/runtime behavior.

**State:** `PARTIAL` evidence for workflow-security assurance; broader security remains outside this bounded demo.

## Observation 3 — Release workflow uses narrowly scoped permissions and immutable action references

The release path starts with empty default permissions, grants `contents: write` only to the release-creation job, grants `id-token: write` only to the PyPI publication job, disables persisted checkout credentials, and pins referenced actions by commit SHA.

**Evidence:** `.github/workflows/publish.yaml` at the exact subject revision.

**Interpretation:** this is strong repository-visible evidence of least-privilege and supply-chain hardening in the release workflow. It does **not** independently prove PyPI account policy, environment protection, runtime integrity, or release success outside the evidence visible here.

**State:** `PASS` for the specific visible controls described above; wider release assurance remains `UNVERIFIED` in this bounded demo.

## What this demo does not claim

This is not a penetration test, vulnerability assessment, compliance attestation, legal opinion, or statement that Flask is secure/insecure. It does not execute the project, inspect private infrastructure, validate maintainer accounts, or prove production behavior.

## Why this is useful

The main demonstration point is evidence scope:

- green CI proves the checks that ran;
- path filters and conditional workflows narrow what a result establishes;
- positive controls such as pinned actions and least-privilege permissions deserve explicit credit;
- anything outside observed evidence remains `UNVERIFIED`, not silently treated as PASS.

## Suggested maintainer outreach

Before any outreach, check the upstream repository's current contribution/security guidance and preferred communication channel. Do not send this report through a public issue if repository policy discourages general promotional or unsolicited audit issues. Security-sensitive findings, if any arise in later work, must follow the upstream private security process instead.
