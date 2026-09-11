# Case Study — Adaptive Language-Learning System

> **Sanitized and anonymized internal case study.** This page demonstrates audit depth and methodology. It does not identify the private repository, reproduce its source code, disclose private commit hashes or paths, or provide reconstruction-enabling implementation details. Some descriptions are generalized to preserve confidentiality.

## The question

An adaptive learning application can have a coherent architecture, deterministic tests, persistent learner state and a release-ready core while still lacking evidence for its strongest pedagogical claims.

The audit question was therefore not merely “does the application run?” It was:

> **Does the reviewed implementation actually enforce the learning, mastery, progression and pronunciation claims described by the architecture?**

That distinction matters because a documented policy is not evidence that the runtime enforces it.

## Overall Portrait v1 dogfood refresh

The current Audit v1 pipeline was re-applied read-only to a fresh exact revision of this private system. The public result below is intentionally sanitized; source identity, revision, paths and implementation details remain private.

**Repository Evidence Map:** the reviewed subject had a compact Python application surface, explicit architecture/product documentation, a deterministic test surface and one primary pull-request verification workflow. Exact-revision binding was available internally, but is intentionally omitted here.

**CI / Test Depth:** static workflow evidence showed a PR verification path combining lint/static checks, compilation and automated tests. Repository evidence also showed tests spanning core learning state, adaptive behavior, conversation behavior, curriculum/review/session behavior, script bridging, speech boundaries and the local web surface. This supports a meaningful verified-core claim; it does **not** prove real-world learning outcomes or every documented product capability.

**Workflow Security:** the reviewed workflow used scoped read permission. Third-party action references were version-tag based rather than full immutable commit pins, so the static evidence supports a hardening opportunity rather than a vulnerability claim. Live branch-enforcement and exact-run freshness require separate platform evidence and remain distinct from workflow-definition evidence.

**Release / Provenance:** repository-level evidence supported engineering verification and a governed release/readiness process, but the static repository snapshot did not independently prove a packaged end-user release, external distribution result or pedagogical outcome. Those claims remain `UNVERIFIED` unless separately evidenced.

**Claims vs Evidence:** the strongest useful separation remained unchanged: deterministic learning mechanics can be supported by tests while broader claims about mastery quality, pronunciation quality, CEFR outcomes or language-general behavior require evidence at their own semantic level.

**Overall Portrait:** the strongest positive signal was a small, testable, fail-closed core with explicit learning/privacy boundaries. The highest-value remediation direction is to keep expanding evidence from “core mechanics are deterministic” toward “documented product and pedagogical claims are demonstrated independently,” without converting architecture intent into PASS.

This refresh demonstrates the new Overall Portrait layers; it is not a pedagogical certification, security certification, accessibility audit or proof of learning efficacy.

## What the review examined

Representative review areas included:

- whether declared language-agnostic architecture was actually generic in the implementation;
- whether mastery state was derived from sufficient learning evidence rather than directly assignable state;
- prerequisite and unlock enforcement;
- spaced-repetition behavior versus the stronger scheduling claims in the design;
- script-bridge behavior and whether it operated on pronunciation/phoneme semantics or simple character substitution;
- separation of speech recognition from pronunciation evidence;
- conversation constraints and whether conversational activity could improperly mutate mastery;
- learner-state isolation and persistence;
- test coverage versus the breadth of product and pedagogical claims;
- the boundary between a verified core and a complete learner-facing product.

## Representative finding 1 — Architecture can promise generality that the runtime does not yet enforce

**Severity:** High  
**Confidence:** High  
**Audit state:** BLOCK for the generic-language claim until implementation matches the abstraction

A system may describe a language-pack architecture intended to support additional languages without changing the core, while the current implementation still contains assumptions tied to the first supported language.

This is more than a naming problem. If core session behavior, validation or defaults depend directly on one language pack, the extensibility claim is not yet supported by the implementation.

**Evidence expected before PASS:** language-independent core contracts, pack registration/injection rather than direct first-language dependencies, tests using at least one alternate or synthetic language pack, and proof that adding a pack does not require modifying core learning logic.

## Representative finding 2 — A `MASTERED` state is not evidence of mastery

**Severity:** High  
**Confidence:** High  
**Audit state:** BLOCK when mastery can be reached without the required evidence

A learning architecture may define mastery using multiple signals such as independent recall, delayed retrieval, latency, confusion rate, sufficient sample size and forgetting risk. The implementation must derive the state from those signals.

If a state transition can mark a skill as mastered after only prerequisite checks, the stored label proves that a transition happened — not that the learner demonstrated mastery.

This is a classic evidence-boundary failure: **state is being treated as proof of the evidence that should have produced the state.**

**Evidence expected before PASS:** a single authoritative mastery policy, minimum-sample gates, delayed-recall evidence, anti-gaming rules, deterministic transition tests, and negative tests proving that insufficient evidence cannot unlock mastery.

## Representative finding 3 — Script substitution is not automatically pronunciation-aware bridging

**Severity:** Medium / High  
**Confidence:** High  
**Audit state:** UNVERIFIED until phonetic semantics are demonstrated

A script-bridge feature may be designed around a chain such as source pronunciation -> phoneme representation -> target grapheme. A visually convincing implementation can still reduce to direct character replacement.

Those mechanisms are not equivalent. Character similarity or convenient substitution can teach the wrong sound correspondence when spelling and pronunciation diverge.

**Evidence expected before PASS:** explicit phoneme-level mapping, contextual/approximate correspondence states, disclosed approximation behavior, normalization rules, and tests covering cases where orthography and pronunciation disagree.

## Representative finding 4 — Speech recognition is not pronunciation proof

**Severity:** High when conflated  
**Confidence:** High  
**Audit state:** PASS for a fail-closed boundary when recognition cannot manufacture a pronunciation score

One positive pattern in the reviewed design was an explicit refusal to treat successful automatic speech recognition as evidence of correct pronunciation.

A recognizer answering “I understood the utterance” does not establish phoneme accuracy, stress, timing or articulation quality. A safe system should keep those claims separate until pronunciation-specific evidence exists.

This is an example where **not implementing a score is safer and more truthful than generating an unsupported one**.

## Representative finding 5 — A simple scheduler may work while stronger SRS claims remain unverified

**Severity:** Medium  
**Confidence:** High  
**Audit state:** UNVERIFIED for advanced adaptive scheduling

A deterministic review scheduler can be useful and testable while still being materially simpler than an architecture that claims to incorporate forgetting risk, mastery confidence, delayed retrieval and prerequisite instability.

The audit therefore separates two claims:

- “the scheduler deterministically schedules reviews” may be supported;
- “the scheduler implements the documented adaptive learning policy” requires additional evidence.

**Evidence expected before PASS:** scheduling inputs bound to the claimed learner signals, boundary tests, forgetting/retention scenarios, reproducible scheduling decisions and evidence that unstable prerequisite skills affect downstream review behavior as designed.

## Representative finding 6 — Green tests can validate a core without validating the whole product

**Severity:** Medium / High  
**Confidence:** High  
**Audit state:** scope-dependent

A compact deterministic test suite may correctly establish important invariants: prerequisite gates, learner isolation, attempt recording, fail-closed speech boundaries and adaptive prioritization.

That is valuable evidence. It does not automatically establish that the full learner-facing product exists, that the complete pedagogical policy is implemented, or that real-world learning outcomes are validated.

The audit therefore keeps **verified core**, **implemented product surface**, and **validated pedagogical outcome** as separate claims.

## Positive evidence matters too

Evidence-first auditing is not only about finding defects. Useful PASS-level patterns in this review included boundaries designed to fail closed rather than invent evidence, deterministic state behavior, local-first learner-data principles, prerequisite modeling and tests for important invariants.

The goal is to preserve those strengths while preventing broader documentation or release language from outrunning the evidence.

## Why this is deeper than ordinary code review

A conventional review may see clean classes, passing tests and sensible interfaces. An evidence audit asks additional questions:

- Can the runtime reach a strong state without the evidence that state is supposed to represent?
- Does a generic abstraction remain generic below the interface layer?
- Is a phonetic claim actually implemented at the phonetic level?
- Does a green test suite support the exact breadth of the release claim?
- Is a safe `not implemented` boundary being preserved instead of replaced by a plausible-looking but unsupported score?

These questions trace claims from documentation through implementation, tests, state transitions and product boundaries.

## What was deliberately removed from this public case study

The public version contains **no** private repository name, private source code, file paths, commit hashes, issue/PR identifiers, proprietary curriculum data, learner data, internal architecture identifiers, credentials, private infrastructure details, exploitable weakness, or reconstruction-enabling implementation detail.

The omission is intentional. The case study demonstrates the audit method without turning a private product into public technical documentation.

## Result format

A full audit can separate findings into:

- **PASS** — the requested claim is supported by reviewed evidence;
- **BLOCK** — evidence demonstrates a material problem within scope;
- **UNVERIFIED** — evidence is insufficient to support the claim;
- **NOT_TESTED** — the claim was outside tests actually performed;
- **NOT_APPLICABLE** — genuinely outside the agreed scope.

Missing evidence is never silently converted into PASS.

## Boundary

This case study does not claim that a learning system produces a particular educational outcome, language proficiency level or certification. It is not a pedagogical certification, accessibility certification, security penetration test, legal opinion or guarantee. It demonstrates an engineering audit methodology for checking whether repository evidence supports the technical and product claims being made.