# Sample Audit

> Synthetic example only. This is not a real customer audit.

**Repository:** `example/project`  
**Revision:** `0123456789abcdef0123456789abcdef01234567`  
**Scope:** release readiness / CI confidence

## Executive summary
The repository has useful automated tests, but the reviewed revision does not provide enough evidence to call the release process reproducible. The highest-leverage improvement is to bind release acceptance to the exact commit that passed required checks.

## Finding ARA-001 — Release evidence is not exact-revision bound
**Severity:** High  
**Confidence:** High  
**Status:** BLOCK

The release documentation refers to a passing branch state but does not preserve the exact accepted commit identity. A later commit can therefore make the evidence stale.

**Recommended action:** record the exact candidate SHA and require release checks against that immutable revision.

## Finding ARA-002 — CI does not exercise the documented install path
**Severity:** Medium  
**Confidence:** Medium  
**Status:** UNVERIFIED

The README documents a clean installation path, while reviewed CI starts from a preconfigured environment. The documented clean-install claim is therefore not established by the reviewed evidence.

**Recommended action:** add a clean-environment CI job that follows the public installation instructions.

## Finding ARA-003 — Test result is present but artifact provenance is unclear
**Severity:** Medium  
**Confidence:** Medium  
**Status:** UNVERIFIED

A generated test report exists, but the reviewed repository evidence does not bind it clearly to the frozen source revision.

**Recommended action:** publish immutable test evidence containing the exact source SHA and tool/runtime identity.

## Boundary
This sample demonstrates report structure only. It is not a penetration test, certification, compliance attestation, or claim about any real repository.