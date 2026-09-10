# How it works

## 1. Request
Open the **Free Demo Audit** Issue Form and provide a public GitHub repository plus your main concern. Never put secrets or private material in the issue.

## 2. Freeze the revision
The review is anchored to one exact commit SHA. If you do not provide one, the current revision is frozen before findings are finalized.

## 3. Evidence review
Repository-visible evidence is reviewed for the selected scope. Typical evidence includes source structure, tests, CI configuration, release controls, authorization boundaries, dependency/configuration signals and documentation.

## 4. Findings
The free demo returns up to three prioritized findings or observations. Findings distinguish confirmed evidence from uncertainty. Missing evidence is not silently treated as PASS.

## 5. Optional paid scope
If the demo is useful, a separate full audit or bounded remediation scope can be agreed. No paid work starts merely because a free issue was opened.

## Evidence semantics
- **PASS** — requested control is supported by reviewed evidence.
- **BLOCK** — evidence shows a material release/readiness problem within scope.
- **UNVERIFIED** — evidence is insufficient to support a claim.
- **NOT_TESTED** — outside the tests actually performed.
- **NOT_APPLICABLE** — genuinely outside the agreed scope.

## Exact-revision rule
A report applies to the exact revision reviewed. Later commits can change the result and require re-verification.