# Independent Public Demo Audit — pyca/cryptography

> Independent public demonstration audit. This was not requested, commissioned, sponsored, approved, or endorsed by the pyca/cryptography maintainers. It is based only on public repository evidence and demonstrates evidence-scope analysis.

## Frozen subject

- Repository: `pyca/cryptography`
- Exact revision: `c507932a7d555e2a163f680722105727d91d472b`
- Scope sampled: repository-visible CI evidence at that revision

## Demo observations

### 1. CI breadth is unusually large, but breadth still does not equal universal proof

The main CI workflow spans multiple Python versions, PyPy, Rust toolchains, several OpenSSL versions/configurations, LibreSSL, BoringSSL, AWS-LC, FIPS-oriented configurations, multiple Linux distributions and multiple architectures.

**Evidence state:** `PARTIAL`

**Why this matters:** this is strong positive evidence of compatibility-oriented engineering discipline. It still proves only the combinations and behaviors actually exercised by those jobs; it is not a blanket proof of security or correctness for every runtime/environment.

### 2. Repository token scope and checkout credential handling are constrained

The workflow uses `permissions: contents: read`, pins external actions to immutable commit SHAs, and disables persisted checkout credentials.

**Evidence state:** `PARTIAL`

**Why this matters:** these controls reduce workflow credential exposure and improve reproducibility, but static workflow review cannot prove all supply-chain or runtime-security properties.

### 3. Test-vector provenance is visible as part of the verification path

CI explicitly fetches external cryptographic test vectors and uses them in nox sessions together with backend/version matrices.

**Evidence state:** `PARTIAL`

**Why this matters:** the evidence path includes more than unit-test success; exact external inputs and their retrieval path are relevant to reproducibility and provenance. A full audit would need to inspect the referenced fetch actions and exact vector revisions rather than assume them from job names alone.

### 4. The frozen revision itself contains visible AI-assisted authorship metadata

The exact commit message includes a Claude session reference and a `Co-authored-by: Claude` trailer.

**Evidence state:** `OBSERVED`

**Why this matters:** AI-assisted provenance can be visible directly in repository history. This does not make the change unsafe or low quality; it demonstrates why provenance and executed evidence should be evaluated separately from assumptions about who or what authored a change.

## 15-domain v2 applicability snapshot

This is a bounded demo, not a full cryptographic or security audit. Unsupported claims remain `UNVERIFIED`.

| Domain | Demo state | Reason |
|---|---|---|
| Threat Model | UNVERIFIED | No complete threat-model review performed. |
| Data Privacy | UNVERIFIED | No privacy/data-flow lifecycle review performed. |
| Migration | NOT_APPLICABLE | No database/schema migration claim tested in this sample. |
| Resilience | UNVERIFIED | CI diversity is not failure-injection/recovery proof. |
| Concurrency | UNVERIFIED | No race/concurrency conclusion established here. |
| Config | PARTIAL | Backend/version/FIPS/toolchain configurations are explicit in CI. |
| Interface | PARTIAL | Multi-backend compatibility is exercised, but public API compatibility was not fully audited. |
| FinOps | UNVERIFIED | No measured CI/runtime cost conclusion established. |
| Agent Safety | UNVERIFIED | AI authorship metadata does not establish agent tool/action safety. |
| Model Eval | NOT_APPLICABLE | No model-quality claim tested. |
| Incident Readiness | UNVERIFIED | No operational restore/rollback/runbook proof sampled. |
| License/IP | PARTIAL | AI authorship provenance is visible for the frozen commit; broader license/IP review was not performed. |
| Identity & Access | PARTIAL | Workflow token permission scope and credential persistence controls are visible. |
| External Dependency Failure | UNVERIFIED | No provider-failure execution evidence sampled. |
| Auditability/Forensics | PARTIAL | Exact revision, immutable action references and authorship metadata improve traceability; complete forensic reconstruction is unproven. |

## Calibration lesson

**Large test matrices deserve positive credit without being promoted into a universal PASS.** The right audit output preserves both facts at once: broad verification evidence exists, and untested/security/operational claims remain explicitly bounded.

## Limitations

This demo is not a cryptographic security review, penetration test, vulnerability assessment, certification, or endorsement. It does not claim pyca/cryptography is unsafe or defect-free. Conclusions are limited to the exact public evidence sampled above.
