# Release / Handoff Evidence Review

A narrow use case for the existing **$49 Full AI Repository Audit** founding offer.

## The buyer question

Before a release or project handoff, answer one practical question:

> **What is actually supported by evidence for the exact version we are about to release or hand over, what material uncertainty remains, and what should happen next?**

This is for a founder, CTO, delivery lead or technical owner who needs a bounded review before making a delivery decision. It is not a promise to prove that the whole system is safe or correct.

## Founding price

**$49** for a separately agreed Release / Handoff Evidence Review within the existing Full AI Repository Audit offer.

The price does not start work automatically. Scope and acceptable public inputs are agreed first.

## Default public scope

Unless a different bounded scope is explicitly agreed, the review covers:

- **one public GitHub repository**;
- **one exact source revision**;
- up to **three priority release/handoff questions** agreed before the review;
- repository-visible public evidence plus separately supplied public evidence that can be safely used;
- a bounded evidence-first conclusion for those questions.

A question should be decision-relevant, for example:

- Did the important CI path actually provide evidence for the version being handed over?
- Is the available release/provenance evidence tied to the source revision under review?
- Does a documented readiness claim have supporting evidence, or is a material part still UNVERIFIED?
- Is there a workflow or repository-control gap that should be addressed before handoff?

The review may determine that available evidence is insufficient. **UNVERIFIED is a valid result.**

## Inputs

For the public workflow, provide only material that is safe to make public:

1. public GitHub repository URL;
2. the intended revision or release/handoff context;
3. up to three concrete questions or concerns;
4. public GitHub evidence links that matter to the decision, when available — for example public workflow runs, releases or attestations.

Do **not** put credentials, secrets, private repository data, customer-confidential information, private vulnerability details or other non-public evidence in a public GitHub Issue.

A public repository does not make every external business detail public.

## Deliverable

The bounded review returns a written evidence-first report that identifies, for the agreed questions:

- the exact source subject reviewed;
- what evidence was actually available;
- VERIFIED, PARTIAL, UNVERIFIED, CONTRADICTED or NOT_APPLICABLE states where applicable;
- material findings or observations without turning every unknown into a defect;
- explicit remaining unknowns;
- prioritized next actions;
- what evidence would be needed to verify an unresolved point.

Where the current deterministic Audit v2 path is applicable, it can support the expert review and produce a reproducible Markdown report. Automation does not replace the evidence boundary.

## Completion criterion

The review is complete when:

1. the agreed repository/revision and up to three questions have been addressed within the agreed public scope;
2. the available evidence and its trust boundary are stated;
3. each material question has a bounded conclusion or is explicitly left UNVERIFIED;
4. material next actions and verification requirements are stated;
5. no unsupported global PASS, certification or release authorization is implied.

Completion does **not** require finding a defect.

## Not included in the $49 review

Unless separately agreed, this review does not include:

- penetration testing or exploit development;
- a guarantee of vulnerability absence;
- legal, compliance or certification attestation;
- full architecture due diligence of an entire business;
- production monitoring or SLA certification;
- private-repository access through the public Issue flow;
- unlimited remediation;
- implementation of all recommended changes;
- deployment or release authorization;
- proof that caller-supplied evidence is independently authenticated when it is not.

## If a fix is needed

The existing **$149 Audit + bounded remediation** offer can cover an explicitly agreed limited set of changes followed by re-verification. It is not an unlimited “fix everything” package.

For a team that needs a repeatable evidence/acceptance process rather than one review, the existing **Setup / Pilot from $299** can be discussed separately.

## Start with the free qualification step

If you have a public repository and a real upcoming release or handoff, open a **Free Demo Audit** request and state the concrete decision you are trying to make. The free step is a bounded qualification/review, not a requirement to buy anything.

[Request a Free Demo Audit](https://github.com/icecolor78-dev/ai-repository-audit/issues/new?template=free-demo-audit.yml)

---

AI Repository Audit is an evidence-first review service and tooling project. It is not a certification authority, penetration-test provider, legal adviser or guarantee that software is defect-free.
