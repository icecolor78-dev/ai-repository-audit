# Public Dogfood and Outreach Policy

This policy governs unsolicited public demonstration audits of third-party open-source repositories.

## Purpose

Public dogfood exists to validate the AI Repository Audit method on real public repositories and to provide reproducible, public-safe examples. It is not a customer engagement unless the repository owner separately requests or accepts one.

## Required labeling

Every unsolicited third-party audit must be labeled clearly as an **independent public demonstration audit**.

Never imply:
- that the repository owner requested, commissioned, approved, endorsed, or partnered on the audit;
- that the audited project is a customer;
- that a finding is an exploitable vulnerability unless verified under an appropriate security process;
- that a green CI result or static review proves production safety, compliance, or defect absence.

## Evidence rules

- Bind every technical observation to an exact public repository revision.
- Prefer links to exact files/lines or exact commit evidence over copied source.
- Keep quotations minimal; summarize in our own words.
- Distinguish observed evidence from inference, hypothesis, and untested scope.
- Missing evidence remains `UNVERIFIED`.
- Do not publish a global score that hides unknowns.

## Security boundary

Potentially exploitable or sensitive security findings must not be published in a public issue, discussion, case study, or outreach message.

Before contacting maintainers about security-relevant material:
1. read the repository's `SECURITY.md` or equivalent reporting instructions;
2. use the project's designated private security channel when available;
3. disclose only what is necessary for responsible triage;
4. do not use a public report as leverage or marketing material for an undisclosed vulnerability.

## Outreach rules

Outreach is optional and must be low-volume, relevant, and respectful.

Before contacting a project:
- inspect `CONTRIBUTING.md`, `SECURITY.md`, issue templates, Discussions, and repository guidance;
- use the project's preferred channel when one is stated;
- do not create an issue solely for promotion if project rules discourage it;
- send at most one initial message unless maintainers respond;
- make clear that no action is required;
- include a link to the public demonstration report rather than pasting a long audit into their tracker.

Suggested neutral wording:

> We ran an independent public demonstration of our evidence-first repository audit method on this public revision. This was not requested or sponsored by the project. No action is required; sharing the report in case the evidence review is useful. If this is not an appropriate channel, please ignore/close it and we will not follow up here.

## Intellectual-property boundary

- Analyze only publicly accessible material.
- Respect the upstream project's license and attribution requirements.
- Do not republish substantial portions of source code or documentation.
- Use repository names and marks only to identify the public subject of the analysis; do not imply affiliation or endorsement.

## Commercial boundary

A public demonstration audit may link back to AI Repository Audit, but it must not fabricate demand, customers, testimonials, conversion, revenue, or endorsement.

The public demonstration and any later paid engagement are separate. Paid work begins only after a separately agreed scope.

## Current benchmark set

Issue #41 freezes the initial public dogfood set. Each report must preserve the exact subject SHA recorded there or explicitly document a later replacement revision.
