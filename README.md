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

**Evidence-first AI code and GitHub repository review at one exact revision.**

[**Request a Free Demo Audit — $0 →**](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)

No signup, domain, paid infrastructure, or private repository access is required for the free demo.

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

These are independent public demonstrations based only on public repository evidence. They are not customer engagements, partnerships, sponsorships, or upstream endorsements.

## What you get for $0

Submit one public GitHub repository. The demo returns:
- up to **3 high-leverage findings or observations**;
- an exact-revision evidence check;
- prioritized next actions;
- a bounded view of CI/test confidence, architecture, authorization boundaries, AI-assisted changes, or release readiness.

**Best fit:** small teams and solo builders shipping quickly with GitHub, Cursor, Claude Code, Codex, Copilot, or other AI-assisted workflows.

[**Open the Free Demo Audit form →**](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)

## What we catch that ordinary AI code review can miss

A code review can tell you that code looks reasonable. An evidence audit asks whether the repository can actually support the claim being made about it.

Typical examples include:
- green CI that is stale, incomplete, skipped, or bound to the wrong revision;
- tests that execute successfully but do not establish release confidence;
- authorization boundaries that exist in code but fail closed only on the happy path;
- AI-assisted changes whose generated evidence cannot be traced to the exact source revision;
- research or benchmark results that are not reproducible from frozen code, data and configuration;
- multiple implementations that appear independent but ultimately prove the same underlying assumption;
- missing evidence silently being interpreted as “probably fine.”

Our rule is simple: **missing evidence stays UNVERIFIED.**

## Why exact revision matters

Branches move. A green result on yesterday's `main` is not evidence about today's code. Every audit is tied to one exact commit so findings and evidence cannot silently drift.

Unknown evidence stays **UNVERIFIED** instead of being turned into “looks good.”

## Founding offers

| Offer | Founding price | Scope |
|---|---:|---|
| Free Demo Audit | **$0** | One public repository at one exact revision, up to 3 high-leverage findings/observations and prioritized next actions. |
| Full AI Repository Audit | **$49** | Deeper evidence review across the agreed repository scope, including relevant CI/tests, architecture, authorization/security boundaries, reproducibility and release-readiness evidence, with prioritized findings. |
| Audit + bounded remediation | **$149** | Full audit plus an explicitly agreed, bounded set of fixes or hardening changes for selected findings, followed by re-verification of those changes. |
| Setup / pilot | **from $299** | Implementation/process enablement for a team or project: define the scope, evidence workflow and repository controls needed to make the audit discipline repeatable. |

The tiers are intentionally different: the **Free Demo samples the method**, the **Full Audit expands the evidence depth**, **remediation changes selected code/configuration**, and a **Setup/Pilot installs a repeatable workflow**. The free request creates no payment obligation. Paid work starts only after a separate scope is agreed.

## Typical review areas

- CI, tests, build and release confidence;
- false-green or stale-evidence patterns;
- architecture and maintainability risks;
- authentication/authorization boundaries visible in reviewed source;
- AI-generated or AI-assisted change risks;
- reproducibility and exact-revision discipline.

## See the audit depth

Start with the short [synthetic sample audit](SAMPLE_AUDIT.md).

See the [independent public demo audits](docs/demos/README.md) for exact-revision examples on real public repositories. These are unsolicited public demonstrations, not customer engagements or upstream endorsements.

For deeper examples:
- [sanitized AI-assisted quantitative-system case study](CASE_STUDY_QUANT_SYSTEM.md) — backtest validity, historical-data semantics, cost modeling, strategy independence, trade/no-trade gating and research provenance;
- [sanitized adaptive language-learning case study](CASE_STUDY_LANGUAGE_LEARNING.md) — mastery evidence, architecture-vs-runtime drift, script/phoneme boundaries, speech-recognition claims, adaptive scheduling and the difference between a verified core and a complete product.

Both case studies deliberately omit private source and reconstruction-enabling implementation details.

## How it works

1. [Submit a Free Demo Audit request](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml).
2. Freeze the exact revision.
3. Review repository-visible evidence within the requested scope.
4. Receive up to three prioritized findings/observations.
5. Continue only if a deeper paid audit or remediation is useful.

See [HOW_IT_WORKS.md](HOW_IT_WORKS.md), [SAMPLE_AUDIT.md](SAMPLE_AUDIT.md), [CASE_STUDY_QUANT_SYSTEM.md](CASE_STUDY_QUANT_SYSTEM.md), [CASE_STUDY_LANGUAGE_LEARNING.md](CASE_STUDY_LANGUAGE_LEARNING.md), [FAQ.md](FAQ.md), and [SECURITY.md](SECURITY.md).

## Public-safety boundary

The Free Demo Audit is for **public repositories only**. Do not submit secrets, credentials, private source, confidential customer data, private repository URLs, or sensitive vulnerability details in a public issue.

This service is not a penetration test, certification, compliance attestation, legal opinion, or guarantee that software is secure or defect-free.

---

### Ready?

[**Request your Free Demo Audit — $0 →**](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)