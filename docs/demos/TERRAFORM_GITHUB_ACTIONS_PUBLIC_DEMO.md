# Independent Public Demo Audit — terraform-github-actions

> **Independent public demonstration.** This review was not requested, commissioned, sponsored, approved, or endorsed by the repository owner or contributors. It is based only on public repository evidence at the exact revision below.

## Frozen subject

- Repository: `dflook/terraform-github-actions`
- Exact revision: `bb0ed9a8ea82a38e966e372da328aa881e00fef4`
- Review mode: bounded public static/evidence review
- Customer status: **not a customer engagement**

## Executive summary

This repository provides unusually strong positive examples of repository-visible CI and release evidence. The sampled release workflow pins third-party GitHub Actions to immutable commit SHAs, scopes token permissions by job, verifies a base-image attestation before use, builds by digest, emits provenance attestations, and records the GitHub revision in image annotations.

The repository also uses `pull_request_target`, but the sampled workflow applies an explicit same-repository guard before granting pull-request write permission and references the tested Terraform actions by immutable commit SHA.

These observations do **not** prove the entire project secure, defect-free, or release-ready in every dimension. They show that several high-value supply-chain and identity claims have concrete repository-visible evidence, while broader runtime, privacy, incident, and dependency-failure behavior remains outside this bounded review.

## Observation 1 — Release dependencies are pinned to immutable revisions

The sampled release workflow references `actions/checkout`, `docker/setup-buildx-action`, and `actions/attest-build-provenance` by full commit SHA rather than mutable major-version tags.

**Evidence state:** `PASS` for the sampled workflow dependency pinning.

**Why this matters:** the static workflow text identifies the exact third-party action revisions intended to execute, materially improving reproducibility and reducing ambiguity compared with floating tags.

## Observation 2 — Release provenance and image identity are explicit

The release workflow resolves the base-image digest, verifies its GitHub attestation, rewrites the Dockerfile to use that digest, builds multi-platform images, adds revision/source/version annotations, and emits GitHub build-provenance attestations for Docker Hub and GHCR subjects.

**Evidence state:** `PASS` for repository-visible provenance controls in the sampled release path.

**Why this matters:** this is stronger than a generic green CI badge. The workflow records concrete artifact identity and provenance controls that can be independently inspected. This demo does not verify every historical run or registry-side state.

## Observation 3 — Token permissions are explicitly scoped

The release workflow starts with `contents: read`; the image job adds `packages: write`, `id-token: write`, and `attestations: write`, while another job explicitly sets an empty permission map. The sampled `pull_request_target` workflow also starts from `permissions: {}` and grants only `pull-requests: write` to the guarded job.

**Evidence state:** `PASS` for explicit permission declarations in the sampled workflows.

**Why this matters:** repository-visible least-privilege intent is concrete evidence. Account-level controls, secret policies, environment protection rules, and organization settings remain outside this static review.

## Observation 4 — `pull_request_target` use includes a visible same-repository guard

The sampled `pull_request_target` workflow runs the privileged job only when the pull request head repository is the same repository and the current repository name matches the expected project. Its tested Terraform actions are also pinned to full commit SHAs.

**Evidence state:** `PARTIAL`

**Why this matters:** the dangerous trigger is not ignored blindly; the repository contains a concrete guard that narrows the execution condition. This bounded review does not claim the complete event/permission threat model is proven.

## Observation 5 — Maintainers explicitly direct general questions to Discussions

The repository issue configuration provides a `Question` contact link to GitHub Discussions and says questions should be asked there when others would benefit from seeing the answer.

**Evidence state:** `PASS` for the visible public feedback path.

**Why this matters:** a concise, non-security, non-sales-pressure note about an independent public demo can be routed through a channel the project explicitly exposes for general questions. Security-sensitive material would require a different path.

## 15-domain v2 applicability snapshot

This is a bounded demonstration, not a full security or release audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | PARTIAL | Privileged-trigger guard and token scoping are visible; no complete threat model reviewed. |
| Data Privacy | UNVERIFIED | No privacy lifecycle conclusion established. |
| Migration | NOT_APPLICABLE | No migration claim tested. |
| Resilience | UNVERIFIED | No failure-injection or recovery evidence sampled. |
| Concurrency | UNVERIFIED | No concurrency conclusion established. |
| Config | PARTIAL | Workflow triggers, permissions, environments and release configuration are visible. |
| Interface | PARTIAL | GitHub Action/release interfaces are visible; compatibility was not fully audited. |
| FinOps | UNVERIFIED | No measured cost conclusion established. |
| Agent Safety | NOT_APPLICABLE | No autonomous-agent behavior evaluated. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | UNVERIFIED | No operational incident-response conclusion established. |
| License/IP | UNVERIFIED | No bounded license analysis performed here. |
| Identity & Access | PARTIAL | Job permissions and token use are explicit; account-side controls are not. |
| External Dependency Failure | PARTIAL | Digest and attestation controls are visible; dependency-outage behavior was not executed. |
| Auditability/Forensics | PASS | Exact revision, immutable action pins, artifact digests, annotations and provenance controls materially support reconstruction. |

## Calibration lesson

**Positive evidence should be preserved, not flattened into generic suspicion.** An evidence-first audit must be able to say that concrete controls are present and well-scoped while still keeping unrelated domains `UNVERIFIED`.

## Outreach boundary

The repository explicitly exposes Discussions for general questions. After our own post-merge verification, a single concise note linking to this independent demo is an appropriate candidate there. Do not use bug or security channels for promotion, and do not imply endorsement or partnership.

## Limitations

This demo is not a penetration test, certification, legal/compliance opinion, endorsement, or guarantee. It does not inspect private organization settings, secrets, environments, registry controls, historical workflow executions, or runtime infrastructure beyond the public repository evidence sampled here.
