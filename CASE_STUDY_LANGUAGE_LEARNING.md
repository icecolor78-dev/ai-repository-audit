# Case Study — Adaptive Language-Learning System

> **Sanitized and anonymized internal case study.** This page demonstrates audit depth and methodology. It does not identify the private repository, reproduce its source code, disclose private commit hashes or paths, or provide reconstruction-enabling implementation details.

## Post-RC evidence refresh

This case was re-evaluated read-only after the Audit exact-subject and evidence-contract hardening. The source repository and exact private revision were verified internally, while their identity remains intentionally omitted from this public page.

The refreshed review preserves three separate truth states that earlier software reviews often collapse:

- deterministic learning mechanics can be supported by repository tests;
- a learner-facing capability can exist without proving its strongest pedagogical claim;
- educational outcomes, pronunciation quality and proficiency remain `UNVERIFIED` unless evidence at that semantic level exists.

The current private subject has a reproducible deterministic verification baseline and an independently reproduced exact-bound test run for the accepted core. That is useful engineering evidence. It is **not** evidence of CEFR attainment, pronunciation correctness, real-world retention or general learning efficacy.

## The question

The audit question is not merely “does the application run?” It is:

> **Does the reviewed implementation actually enforce the learning, mastery, progression and pronunciation claims described by the architecture?**

That distinction matters because a documented policy is not evidence that the runtime enforces it.

## Current Overall Repository Portrait

**Exact-subject discipline:** the review is bound internally to a verified repository/revision subject rather than treating an arbitrary local tree as “exact.” Public sanitization removes that identity from this page; it does not remove the internal binding requirement.

**CI / test depth:** current repository evidence supports a deterministic core verification surface across learning state, progression, scheduling, language-pack behavior and local application boundaries. Test existence is kept separate from exact-subject execution evidence, and neither is promoted into proof of educational outcome.

**Claims vs evidence:** broad claims are evaluated at their own semantic level. A tested scheduler can support “deterministic review scheduling” without supporting “optimal spaced repetition.” A safe ASR boundary can support “speech recognition does not fabricate pronunciation evidence” without supporting “pronunciation is accurately scored.”

**Workflow / release:** repository-visible workflow and release-readiness evidence supports engineering process claims within its observed scope. Static configuration does not prove publication success, distribution quality, user outcomes or security absence.

**Overall result:** the strongest supported claim is a testable, fail-closed learning core with explicit privacy and evidence boundaries. The strongest unsupported claims remain pedagogical: general mastery quality, pronunciation quality, proficiency outcomes and language-general efficacy.

This is not a pedagogical certification, security certification, accessibility audit or proof of learning efficacy.

## Representative finding 1 — Architecture generality needs runtime evidence

**Severity:** High  
**Confidence:** High  
**State:** `UNVERIFIED` or `CONTRADICTED` depending on the exact implementation evidence

A language-pack architecture may be designed to support additional languages without changing the core while the implementation still contains first-language assumptions.

The audit therefore does not infer generality from interface names or architecture diagrams. Evidence must show that language-specific grapheme, phoneme, lexicon and curriculum behavior is supplied through the language contract rather than embedded in core progression logic.

**Evidence expected before VERIFIED:** language-independent core contracts, pack injection/registration, an alternate or synthetic pack, and negative tests proving the core does not silently depend on first-language defaults.

## Representative finding 2 — A stored `MASTERED` state is not mastery evidence

**Severity:** High  
**Confidence:** High

If a skill can enter a strong state without the evidence that state is supposed to summarize, the state transition proves only that the transition happened.

A stronger model derives mastery from bounded evidence such as sufficient independent attempts, delayed recall, confusion/error history, prerequisite stability and other explicitly defined signals. Missing evidence must remain missing rather than becoming “mastered.”

**Evidence expected before VERIFIED:** one authoritative mastery policy, minimum-sample gates, delayed-recall evidence, anti-gaming rules, deterministic transition tests and negative tests for insufficient evidence.

## Representative finding 3 — Script substitution is not pronunciation-aware bridging

**Severity:** Medium / High  
**Confidence:** High

A script bridge can look convincing while reducing to direct character substitution. That is not equivalent to a phoneme-aware transformation.

**Evidence expected before VERIFIED:** explicit phoneme/grapheme relationships, contextual approximation states, normalization rules and cases where orthography and pronunciation disagree.

## Representative finding 4 — Speech recognition is not pronunciation proof

**Severity:** High when conflated  
**Confidence:** High

One important positive control is a fail-closed boundary between speech recognition and pronunciation evidence. A recognizer answering “the utterance was understood” does not establish phoneme accuracy, stress, timing or articulation quality.

The safe result when pronunciation-specific evidence is missing is `UNVERIFIED`, not a plausible-looking score.

## Representative finding 5 — Deterministic scheduling can be VERIFIED while stronger SRS claims remain UNVERIFIED

**Severity:** Medium

The evidence model separates:

- “the scheduler deterministically produces the documented scheduling decision for the tested inputs”; and
- “the scheduler implements an empirically effective adaptive-learning policy.”

The first can be verified by exact-subject tests. The second requires evidence at a different level.

## Representative finding 6 — Green tests validate only what actually ran

**Severity:** Medium / High  
**Confidence:** High

A passing suite can establish important invariants such as prerequisite gates, learner-state isolation, deterministic attempts, pack validation and fail-closed speech behavior. It does not automatically establish the full learner-facing product or its real-world educational effect.

The refreshed audit therefore keeps **discovered tests**, **exact-subject execution**, **implemented product surface** and **validated outcome** as separate evidence layers.

## Positive evidence matters

Evidence-first auditing is not defect hunting. Useful positive controls in this case include deterministic state transitions, local-first learner-data boundaries, prerequisite modeling, explicit unknown states and refusal to manufacture pronunciation evidence.

The audit goal is to preserve those strengths while preventing documentation or release language from outrunning evidence.

## What this public case deliberately omits

The public version contains no private repository name, source code, internal file paths, commit hashes, issue/PR identifiers, proprietary curriculum data, learner data, credentials, private infrastructure details, exploitable weakness or reconstruction-enabling implementation detail.

## Result semantics

The refreshed case uses evidence states rather than a generic score:

- **VERIFIED** — current exact-subject evidence directly supports the bounded claim;
- **PARTIAL** — current evidence supports only part of the claim;
- **UNVERIFIED** — evidence is insufficient;
- **CONTRADICTED** — current evidence conflicts with the claim;
- **NOT_APPLICABLE** — the claim is genuinely outside the applicable scope and the reason is explicit.

Missing evidence is never silently converted into VERIFIED.

## Boundary

This case study does not claim that a learning system produces a particular educational outcome, language proficiency level or certification. It demonstrates an engineering audit methodology for checking whether repository evidence supports the technical and product claims being made.