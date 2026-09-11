# AI Repository Audit

[![Public repository checks](https://github.com/icecolor78-dev/ai-repository-audit/actions/workflows/public-repo-checks.yml/badge.svg?branch=main)](https://github.com/icecolor78-dev/ai-repository-audit/actions/workflows/public-repo-checks.yml)
[![Free Demo](https://img.shields.io/badge/Free_Demo-$0-brightgreen)](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)
![Public repositories](https://img.shields.io/badge/Public_repositories-supported-blue)
![Evidence first](https://img.shields.io/badge/Evidence-first-informational)
![Exact revision](https://img.shields.io/badge/Audit-exact_revision-blueviolet)
![Setup pilot](https://img.shields.io/badge/Setup%2FPilot-from_$299-orange)

[![GitHub stars](https://img.shields.io/github/stars/icecolor78-dev/ai-repository-audit?style=flat&logo=github)](https://github.com/icecolor78-dev/ai-repository-audit/stargazers)
[![GitHub forks](https://img.shields.io/github/forks/icecolor78-dev/ai-repository-audit?style=flat&logo=github)](https://github.com/icecolor78-dev/ai-repository-audit/forks)
[![Last commit](https://img.shields.io/github/last-commit/icecolor78-dev/ai-repository-audit?style=flat&logo=github)](https://github.com/icecolor78-dev/ai-repository-audit/commits/main)

**Evidence-first GitHub repository audit and AI code audit for CI/CD, software assurance, security evidence and release readiness — bound to one exact revision when that binding can be verified.**

The central question is not “does this repository look good?” It is: **what can the available evidence actually prove about this exact subject, and what remains unverified?**

**Shipping a release or handing a project to a client?** The existing $49 Full Audit can be scoped as a [**Release / Handoff Evidence Review →**](RELEASE_HANDOFF_REVIEW.md): one public repository, one exact revision, up to three agreed decision-relevant questions, explicit unknowns and next actions.

[**Request a Free Demo Audit — $0 →**](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)

No signup, domain, paid infrastructure, or private repository access is required for the free demo.

## Current automation boundary

The current public automated path is intentionally narrower than the full expert audit service.

**Automated / deterministic in the accepted Audit v2 path:**
- exact GitHub repository + selected `HEAD` SHA + immutable Git-tree binding;
- Git-tree content manifest identity;
- exact README claim text preservation without inferring truth from documentation;
- structured GitHub Actions trigger/job/step inspection;
- bounded workflow-security and false-green review signals;
- test-file/type discovery without silently truncating large test trees;
- bounded supply-chain, repository-local architecture and contract-drift evidence;
- standard JSON Schema validation plus fail-closed evidence rules for `VERIFIED`;
- optional caller-supplied exact workflow/test/release/runtime/provenance evidence with explicit trust boundaries;
- optional time-bound supplied branch/ruleset state kept distinct from commit-bound evidence;
- deterministic customer-facing Markdown rendering and golden adversarial end-to-end tests.

**Still requires independently retrieved/provider-authenticated evidence or expert review for stronger conclusions:**
- whether externally supplied CI/runtime/provenance/platform evidence is independently authentic and current;
- exploitability and absence of vulnerabilities;
- trusted-builder/signature/reproducible-build conclusions;
- successful deployment and production behavior;
- deep dependency/license/vulnerability conclusions beyond bounded repository evidence;
- final release/readiness judgment in the agreed business context.

Static configuration never becomes runtime proof merely because it was discovered. Caller-supplied evidence never becomes independently authenticated merely because it is well formed. Missing, stale, inaccessible or wrong-subject evidence stays bounded or **UNVERIFIED**.

## Evidence states

- **VERIFIED** — the bounded claim is directly supported by current, accessible evidence bound to the exact subject.
- **PARTIAL** — relevant evidence exists, but material parts remain unproved.
- **UNVERIFIED** — evidence is insufficient to establish the claim.
- **CONTRADICTED** — current evidence shows the bounded claim is false for the reviewed subject.
- **NOT_APPLICABLE** — the claim is genuinely outside the applicable scope and the report states why.

There is no opaque global security score. A green CI badge is not a blanket PASS.

## Public Demo Audits

See the method on real public repositories before requesting your own audit.

- [Flask — public demo audit](docs/demos/FLASK_PUBLIC_DEMO.md)
- [Vite — public demo audit](docs/demos/VITE_PUBLIC_DEMO.md)
- [Terraform — public demo audit](docs/demos/TERRAFORM_PUBLIC_DEMO.md)
- [pyca/cryptography — public demo audit](docs/demos/CRYPTOGRAPHY_PUBLIC_DEMO.md)
- [git-auto-commit-action — public demo audit](docs/demos/GIT_AUTO_COMMIT_ACTION_PUBLIC_DEMO.md)
- [GitHub Local Actions — public demo audit](docs/demos/GITHUB_LOCAL_ACTIONS_PUBLIC_DEMO.md)
- [cargo-make — public demo audit](docs/demos/CARGO_MAKE_PUBLIC_DEMO.md)
- [flutter-action — public demo audit](docs/demos/FLUTTER_ACTION_PUBLIC_DEMO.md)

[**Browse all public demo audits →**](docs/demos/README.md)

These are independent public demonstrations based only on public repository evidence. They are not customer engagements, partnerships, sponsorships, upstream approvals or endorsements. Existing demos are expert/manual or semi-automated evidence reviews and must not be treated as benchmark proof for a newer automated engine version unless explicitly rerun and labeled as such.

## What you get for $0

Submit one public GitHub repository. The demo returns:
- up to **3 high-leverage findings or observations**;
- an exact-revision evidence check;
- prioritized next actions;
- a bounded view of relevant CI/test, architecture, authorization, reproducibility or release-readiness evidence.

**Best fit:** small teams and solo builders shipping quickly with GitHub and AI-assisted development tools.

[**Open the Free Demo Audit form →**](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)

## What an evidence audit looks for

Typical examples include:
- green CI whose important job was skipped, filtered or not required;
- evidence generated for a different repository or revision;
- tests that exist but have no exact-subject execution evidence;
- a privileged workflow context that needs trust-boundary review;
- OIDC permission being mistaken for proof that trusted publishing occurred;
- a release artifact whose source identity or verification is not established;
- documentation claims that are stronger than the available evidence;
- missing evidence silently being interpreted as “probably fine.”

The auditor must distinguish a **potential review signal** from a **proven defect**. Missing evidence is not automatically a vulnerability.

## Why exact revision matters

Branches move. A green result on yesterday's `main` is not evidence about today's code. The exact-bound automated path verifies repository identity, requested `HEAD`, and the selected Git tree before repository-file evidence receives exact freshness. Repository content for the exact automated path is materialized from Git objects belonging to that tree rather than from unrelated ignored/untracked working-tree files.

If that binding cannot be established, the audit fails closed rather than borrowing confidence from a caller-supplied SHA.

## Founding offers

| Offer | Founding price | Scope |
|---|---:|---|
| Free Demo Audit | **$0** | One public repository at one reviewed revision, up to 3 high-leverage findings/observations and prioritized next actions. |
| Full AI Repository Audit | **$49** | Deeper expert evidence review across the agreed repository scope. A concrete starting scope is the [Release / Handoff Evidence Review](RELEASE_HANDOFF_REVIEW.md). |
| Audit + bounded remediation | **$149** | Full audit plus an explicitly agreed, bounded set of fixes or hardening changes for selected findings, followed by re-verification. |
| Setup / pilot | **from $299** | Implementation/process enablement for a team or project: define scope, evidence workflow and repository controls needed to make the discipline repeatable. |

The free request creates no payment obligation. Paid work starts only after a separate scope is agreed.

## How it works

1. [Submit a Free Demo Audit request](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml) with the decision or concern you need help with.
2. Freeze and, where automation is used, verify the subject binding.
3. Review repository-visible and available execution evidence within scope.
4. Separate verified facts, partial evidence, unknowns and contradictions.
5. Receive prioritized findings/observations and continue only if a deeper paid audit or remediation is useful.

See [RELEASE_HANDOFF_REVIEW.md](RELEASE_HANDOFF_REVIEW.md), [HOW_IT_WORKS.md](HOW_IT_WORKS.md), [SAMPLE_AUDIT.md](SAMPLE_AUDIT.md), [FAQ.md](FAQ.md), and [SECURITY.md](SECURITY.md).

## Public-origin-only boundary

The public repository and Free Demo Audit use only **public-source evidence** plus clearly synthetic fixtures/material created specifically for this public product. Private or internal evidence is not republished here even after anonymization, sanitization, aggregation, paraphrase, or generalization.

Do not submit secrets, credentials, private source, confidential customer data, private repository URLs, or sensitive vulnerability details in a public issue.

This service is not a penetration test, certification, compliance attestation, legal opinion, security guarantee, or guarantee that software is defect-free.

---

### Ready?

If you have a real release or handoff question, [**request a Free Demo Audit — $0 →**](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)
