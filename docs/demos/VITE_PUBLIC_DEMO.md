# Independent Public Demo Audit — Vite

> Independent public demonstration audit. This was not requested, commissioned, sponsored, approved, or endorsed by the Vite maintainers. It is based only on public repository evidence and is intended to demonstrate evidence-scope analysis.

## Frozen subject

- Repository: `vitejs/vite`
- Exact revision: `99bd9d1d46153fa939f4a304cc0177db42e28776`
- Scope sampled: repository-visible GitHub Actions CI evidence at that revision

## Demo observations

### 1. A green aggregate CI label can intentionally include a skipped test matrix

The main CI workflow first classifies changed files. For changes limited to documentation, most `.github/**` files, create-vite templates, or Markdown, the main `test` job is skipped. The aggregate job is deliberately named **Build & Test Passed or Skipped** and succeeds when the workflow has neither cancellation nor failure.

**Evidence state:** `PARTIAL`

**Why this matters:** the aggregate green state is truthful about the workflow contract, but it is not equivalent to saying the full build-and-test matrix executed for every change. Consumers of CI evidence need the path/change context, not only the badge color.

### 2. Lint/type/docs checks have a different evidence scope from the main test matrix

The `lint` job builds, lints, checks formatting, typechecks, and runs documentation tests without the same `should_skip` condition used by the main test matrix.

**Evidence state:** `PARTIAL`

**Why this matters:** one workflow can contain multiple evidence scopes. Treating all jobs as one undifferentiated PASS loses useful information about what was actually exercised.

### 3. Workflow hardening is visible, but runtime safety is still not proven by static workflow inspection

The workflow removes default `GITHUB_TOKEN` permissions, disables persisted checkout credentials, pins third-party actions to commit SHAs, and runs a multi-version / multi-OS test matrix.

**Evidence state:** `PARTIAL`

These are positive repository-visible controls. They do not by themselves prove production runtime security, dependency safety, rollback behavior, deployment configuration, or absence of vulnerabilities.

## 15-domain v2 applicability snapshot

This is a bounded demo, not a full audit. Domains not directly supported by the sampled evidence remain `UNVERIFIED` rather than inferred as PASS.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No complete threat-model evidence sampled. |
| Data Privacy | UNVERIFIED | No data-flow/privacy lifecycle evidence sampled. |
| Migration | NOT_APPLICABLE | No database/schema migration claim tested in this bounded CI sample. |
| Resilience | UNVERIFIED | CI matrix is not runtime fault-injection evidence. |
| Concurrency | UNVERIFIED | No race/concurrency proof established here. |
| Config | PARTIAL | CI environment, versions and workflow conditions are explicit. |
| Interface | UNVERIFIED | No cross-service/API compatibility conclusion tested. |
| FinOps | UNVERIFIED | Runner limits are visible but no measured cost model was established. |
| Agent Safety | UNVERIFIED | No agent/tool-action safety evidence sampled. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested in this sample. |
| Incident Readiness | UNVERIFIED | No restore/rollback/runbook operational proof sampled. |
| License/IP | UNVERIFIED | License/provenance review was outside this bounded sample. |
| Identity & Access | PARTIAL | Workflow token permissions and persisted credentials are visible. |
| External Dependency Failure | UNVERIFIED | No provider-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact revision and explicit job conditions make CI evidence traceable, but complete forensic reconstruction is unproven. |

## Calibration lesson

**Do not convert an aggregate green job into a claim that every test path executed.** A useful audit must preserve conditional/skipped semantics and report them as evidence scope, not as a defect by default.

## Limitations

This demo does not claim Vite is unsafe, vulnerable, misconfigured, or release-unready. It does not replace the project's own testing or security process. Findings are limited to the exact public evidence sampled above.
