# AI Repository Audit — Repository Rules

## Governance

This intentionally public commercial repository follows the owner's current engineering governance plus the stronger public-surface rules below. Internal continuity, coordination and implementation sources are not part of the public product contract and must not be named or reconstructed here.

Before meaningful work or any writable action, inspect this repository's live GitHub state, exact target SHA, active Issues/PRs/branches, and overlapping writable scopes. If required current evidence is unavailable, stale, or uncertain, remain read-only until the uncertainty is resolved.

## Public-origin-only boundary

Everything committed here must be safe for unrestricted public disclosure **and must originate only from public sources or from synthetic material created specifically for this public product**.

Allowed publication inputs:
- evidence from public repositories, public documentation, public APIs, public standards, and other openly accessible sources;
- synthetic fixtures, examples, tests, schemas, code, and documentation created specifically for this repository and containing no private-derived facts;
- public product statements approved by the owner.

Forbidden publication inputs include material derived from private or internal sources even after anonymization, sanitization, aggregation, paraphrase, or generalization. A public-safe transformation of private evidence is still private-derived and must not be committed here.

Never publish or reconstruct:
- credentials, tokens, secrets, account/session data, or private customer data;
- private repository source, private SHAs, internal paths, private URLs, internal repository names, or non-public infrastructure details;
- proprietary strategy logic, parameters, datasets, private performance details, or customer-confidential findings;
- exploitable private weaknesses or architecture detail sufficient to reconstruct a private system;
- case studies, benchmarks, examples, statistics, findings, or claims whose factual basis comes from a non-public repository, customer engagement, internal system, or private evidence set.

If origin is uncertain, treat the material as non-public-derived and do not publish it. Public case studies and demos must be reproducible from named public sources or be explicitly synthetic and labeled as such.

## Evidence semantics

This repository's product promise is evidence-first auditing. Preserve that standard in the repository itself:
- bind meaningful technical claims to the exact revision/evidence available;
- a syntactically valid SHA is not proof that the scanned tree belongs to that SHA or repository;
- missing, stale, inaccessible or wrong-subject evidence is `UNVERIFIED`, not PASS;
- a green CI result proves only the checks that actually ran on that subject;
- static workflow configuration does not by itself prove execution, exploitability, publication success or runtime behavior;
- do not weaken tests, validators, confidentiality checks, or wording merely to obtain green status;
- do not present a manual/semi-automated service as fully automated SaaS;
- case studies must distinguish verified observations from architecture intent, claims, hypotheses, and untested scope.

## Work and publication flow

For non-trivial changes use an explicit Issue, one active writable owner, one implementation branch, relevant checks, review of the exact diff, and a PR to `main`. Do not collide with an active writable scope.

Public-content changes require an explicit source-origin and confidentiality pass before merge. Workflow/security changes require exact-head verification appropriate to their risk. A change is not DONE merely because it was committed or CI is green.

## Commercial boundary

Current prices, offer text, guarantees, customer claims, testimonials, metrics, and publication channels must come from current owner-approved state. Never invent customers, revenue, testimonials, download counts, security guarantees, certification, or compliance claims.

AI Repository Audit is an audit/assurance service and portfolio cash bridge. It is not automatically a penetration test, formal certification, legal/compliance opinion, or guarantee of defect-free software unless a separately governed scope explicitly says otherwise.
