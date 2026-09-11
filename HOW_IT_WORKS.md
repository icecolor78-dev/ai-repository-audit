# How it works

## 1. Request
Open the **Free Demo Audit** Issue Form and provide a public GitHub repository plus your main concern. Never put secrets or private material in the issue.

## 2. Bind the exact revision
The review is anchored to one exact commit SHA. The automated exact-bound path verifies that the requested GitHub repository matches the local Git origin, the requested SHA equals `HEAD`, the scan root is the repository root, and the working tree has no dirty or untracked content. It also records the Git tree identity and a deterministic manifest digest for tracked content.

If those checks cannot be established, repository-file evidence is not labeled `exact`; the binding remains explicitly unverified. A syntactically valid SHA alone is never enough.

## 3. Evidence review
Repository-visible evidence is reviewed for the selected scope. Typical evidence includes source structure, tests, CI configuration, release controls, authorization boundaries, dependency/configuration signals and documentation. Static configuration is evidence of configuration only: it does not by itself prove execution, exploitability, publication success or runtime behavior.

## 4. Findings
The free demo returns up to three prioritized findings or observations. Findings distinguish confirmed evidence from uncertainty. Missing evidence is not silently treated as PASS.

## 5. Optional paid scope
If the demo is useful, a separate full audit or bounded remediation scope can be agreed. No paid work starts merely because a free issue was opened.

## Evidence semantics
- **VERIFIED** — the bounded claim is directly supported by current, accessible evidence bound to the exact subject.
- **PARTIAL** — some relevant evidence exists, but material parts of the claim remain unproved.
- **UNVERIFIED** — available evidence is insufficient to establish the claim.
- **CONTRADICTED** — current evidence shows the bounded claim is false for the reviewed subject.
- **NOT_APPLICABLE** — the claim is genuinely outside the applicable scope and the report states why.

A release/readiness verdict such as HOLD is a separate composition decision. It must not be manufactured from a missing evidence source or from a single static keyword.

## Exact-revision rule
A report applies only to the exact revision and evidence set reviewed. Later commits, a different repository tree, dirty/untracked content, stale external evidence or a different execution can change the result and require re-verification.
