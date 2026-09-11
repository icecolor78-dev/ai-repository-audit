# How it works

## 1. Request
Open the **Free Demo Audit** Issue Form and provide a public GitHub repository plus your main concern. Never put secrets or private material in the issue.

## 2. Bind the exact revision
The review is anchored to one exact commit SHA. The automated exact-bound path verifies that the requested GitHub repository matches the local Git origin, the requested SHA equals the selected local `HEAD`, and the scan root is the repository root. It resolves the requested Git tree and records a deterministic manifest digest from the tree's regular tracked blobs.

The repository-file scan is then materialized from immutable Git objects belonging to that exact tree. Unrelated ignored or untracked working-tree files are **not** part of the audited scan-set and do not silently enter the evidence. Unsupported tree entries such as symlinks or gitlinks fail closed rather than being treated as ordinary audited files.

If repository/revision/root identity or the supported exact-tree contract cannot be established, the exact audit fails closed. A syntactically valid caller-supplied SHA alone is never enough.

## 3. Evidence review
Repository-visible evidence is reviewed for the selected scope. Typical evidence includes source structure, tests, CI configuration, release controls, authorization boundaries, dependency/configuration signals and documentation. Static configuration is evidence of configuration only: it does not by itself prove execution, exploitability, publication success or runtime behavior.

When separately supplied execution, runtime, provenance or platform-state evidence is used, its trust class and boundary remain explicit. Caller-supplied exact evidence is not silently upgraded to independently authenticated evidence, and time-bound branch/ruleset state is not represented as commit-bound proof.

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
A report applies only to the exact revision and evidence set reviewed. Later commits, a different repository tree, newly supplied execution evidence, or a different platform/runtime state can change the result and require re-verification. Ignored or untracked working-tree files are outside the immutable exact-tree scan-set unless they become tracked content of the audited revision.
