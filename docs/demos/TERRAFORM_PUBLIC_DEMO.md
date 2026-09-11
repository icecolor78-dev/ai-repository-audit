# Independent Public Demo Audit — Terraform

> Independent public demonstration audit. This was not requested, commissioned, sponsored, approved, or endorsed by HashiCorp or the Terraform maintainers. It is based only on public repository evidence and demonstrates evidence-scope analysis.

## Frozen subject

- Repository: `hashicorp/terraform`
- Exact revision: `01081abb7f4e644d32fecc4839484eb0ce30385f`
- Scope sampled: repository-visible GitHub Actions quick-check evidence at that revision

## Demo observations

### 1. The PR quick-check workflow explicitly documents that it is not the full release-confidence surface

The workflow comments state that `checks.yml` is intended to keep pull-request feedback fast, while `build.yml` contains additional checks for already-merged release branches and tags and may catch architecture-specific or OS-specific issues that quick checks do not.

**Evidence state:** `PARTIAL`

**Why this matters:** a green PR workflow is intentionally narrower than the repository's broader release verification. An audit should preserve that distinction rather than collapse both into one generic PASS.

### 2. Race detection is deliberately selective

The quick-check workflow runs Go's race detector only against selected package groups rather than the entire repository.

**Evidence state:** `PARTIAL`

**Why this matters:** this is useful positive concurrency evidence for the covered packages, but it is not proof that the whole codebase is race-free.

### 3. Pull-request E2E coverage is intentionally platform-bounded

The E2E job states that it is an intentionally limited Linux-only PR run; broader platform coverage is delegated to `build.yml` after merge.

**Evidence state:** `PARTIAL`

**Why this matters:** platform coverage is a first-class part of evidence provenance. A successful Linux E2E run must not silently become a cross-platform release claim.

### 4. Least-privilege workflow permissions and dependency consistency checks are visible

The workflow uses `permissions: contents: read`, pins external actions to commit SHAs, checks module consistency, and verifies generated files remain synchronized.

**Evidence state:** `PARTIAL`

These are positive controls. They do not prove the absence of defects, security vulnerabilities, or release regressions outside the executed scope.

## 15-domain v2 applicability snapshot

This is a bounded demo, not a full audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No complete threat-model evidence sampled. |
| Data Privacy | UNVERIFIED | No privacy/data-flow evidence sampled. |
| Migration | UNVERIFIED | Terraform state/schema compatibility was not evaluated here. |
| Resilience | UNVERIFIED | No bounded fault-injection evidence sampled. |
| Concurrency | PARTIAL | Selected package groups run the Go race detector. |
| Config | PARTIAL | Workflow environments, triggers and toolchain selection are explicit. |
| Interface | PARTIAL | Generated/protobuf consistency checks are visible, but compatibility conclusions are bounded. |
| FinOps | UNVERIFIED | No measured runtime/cloud cost evidence sampled. |
| Agent Safety | UNVERIFIED | No agent/tool-action safety evidence sampled. |
| Model Eval | NOT_APPLICABLE | No model-evaluation claim tested in this sample. |
| Incident Readiness | UNVERIFIED | No backup/rollback/runbook evidence established. |
| License/IP | UNVERIFIED | License/provenance review was outside this bounded sample. |
| Identity & Access | PARTIAL | Workflow token scope is explicitly read-only for repository contents. |
| External Dependency Failure | UNVERIFIED | No provider-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact revision and named checks provide traceable evidence scope. |

## Calibration lesson

**Repository-authored scope disclaimers are evidence, not noise.** When maintainers explicitly say one workflow is intentionally narrower than another, an auditor should preserve that statement and avoid overclaiming from the greener/faster check surface.

## Limitations

This demo does not claim Terraform is unsafe, vulnerable, misconfigured, or release-unready. It does not replace HashiCorp's own engineering or security review. Conclusions are limited to the exact public evidence sampled above.
