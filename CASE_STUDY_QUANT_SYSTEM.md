# Case Study — AI-Assisted Quantitative System

> **Sanitized and anonymized internal case study.** This page demonstrates audit depth and methodology. It does not identify the private repository, reproduce its source code, disclose proprietary trading logic, or publish actionable private weaknesses. Details have been generalized and some examples are representative rather than verbatim findings.

## The question

A quantitative trading codebase can have many strategies, tests and green CI checks while still lacking evidence that it has a reproducible positive edge after realistic costs.

The audit question was therefore not “does the code run?” It was:

> **Does the reviewed evidence support a reproducible decision process after realistic costs, while allowing the system to choose NO_TRADE when evidence is weak?**

That framing changed the review from ordinary code review into an evidence audit.

## What the review examined

The review treated the repository as a chain of claims that had to remain valid from historical data to a simulated decision and eventually to an executable action. Representative review areas included:

- closed-candle and decision-time semantics;
- entry timing and same-bar ambiguity;
- lookahead and information leakage;
- historical-universe / point-in-time selection risk;
- warm-up and timeframe aggregation;
- fees, slippage and other carrying/execution costs;
- whether nominally different strategies were mechanically independent;
- regime classification and trade/no-trade gating;
- parameter-search and multiple-testing risk;
- holdout and walk-forward discipline;
- multi-symbol / multi-timeframe aggregation;
- portfolio risk, drawdown and execution boundaries;
- reproducibility and provenance of research evidence.

## Representative finding 1 — A backtest can be internally consistent and still answer the wrong historical question

**Severity:** High  
**Confidence:** High  
**Audit state:** BLOCK until point-in-time semantics are established

A common failure mode in market research is constructing historical experiments using information selected from the present. For example, a universe chosen using current availability or current liquidity can make past results look cleaner than a decision process that actually existed at that historical time.

The important audit step is not merely checking a loop for an obvious future-data reference. The reviewer must trace **how the historical opportunity set itself was constructed**.

**Evidence expected before PASS:** a point-in-time universe policy, reproducible historical membership/liquidity inputs, explicit delisting/missing-data treatment, and tests demonstrating that a historical decision cannot depend on later membership information.

## Representative finding 2 — Costs belong inside the edge claim, not in a disclaimer after it

**Severity:** High  
**Confidence:** High  
**Audit state:** UNVERIFIED until net economics are evidenced

A positive gross backtest is not evidence of a positive executable edge. The relevant quantity is the result after the costs and constraints that the strategy would have encountered.

The audit therefore asks whether fees, slippage, carrying costs, spread/liquidity assumptions and execution timing are applied at the same semantic boundary as the simulated trade. It also checks whether those assumptions remain stable under adverse but plausible scenarios.

**Evidence expected before PASS:** cost-aware net metrics, sensitivity analysis, explicit execution assumptions, stable results outside the parameter-selection sample, and enough observations to distinguish signal from noise.

## Representative finding 3 — Strategy count is not strategy diversity

**Severity:** Medium / High  
**Confidence:** Medium / High  
**Audit state:** UNVERIFIED until independence is measured

A repository may expose many strategy names while several strategies ultimately express the same underlying market bet. Counting classes or configuration variants can therefore overstate diversification and inflate confidence when correlated signals are evaluated as independent evidence.

The audit groups strategies by **mechanical source of return**, not by file/class name. It then asks whether purported confluence factors add independent information or repeatedly vote for the same latent feature.

**Evidence expected before PASS:** signal-return correlation analysis, overlap/ablation tests, regime-conditioned contribution, and portfolio aggregation that does not treat correlated variants as independent confirmation.

## Representative finding 4 — NO_TRADE must be a first-class valid output

**Severity:** High  
**Confidence:** High  
**Audit state:** design requirement

When the goal is durable edge rather than trade frequency, forcing every market state into a strategy is dangerous. The system needs an explicit abstention path when evidence, expected net value, liquidity, regime confidence or risk budget is insufficient.

The audit therefore tests the decision boundary in both directions: not only “why did this trade happen?” but also “what evidence is required before the system is allowed to stop abstaining?”

A useful design treats opportunity selection as a competition for scarce risk budget. A candidate that does not clear the evidence and net-value threshold loses to **NO_TRADE**.

## Representative finding 5 — Research evidence needs provenance

**Severity:** Medium / High  
**Confidence:** High  
**Audit state:** UNVERIFIED when provenance is incomplete

Charts, metrics and generated reports are weak evidence if they cannot be reproduced from a frozen source revision, data identity, configuration and runtime/tool identity.

The review therefore distinguishes “a result exists” from “the result is bound to the exact experiment that produced it.” This is the same exact-revision principle used by AI Repository Audit for software evidence generally.

**Evidence expected before PASS:** immutable experiment identity, source revision, data/config identity, runtime/tool version, command or workflow provenance, and an artifact that can be traced back to those inputs.

## Representative finding 6 — Missing cost evidence must stay missing, not become zero

**Severity:** High  
**Confidence:** High  
**Audit state:** PASS when accounting fails closed; BLOCK if missing cost data is silently coerced to zero

A subtle but important accounting error is treating unavailable funding, commission or fill evidence as a numeric zero. Zero is an observed economic value. Missing is an evidence state.

A stronger design keeps incomplete accounting explicitly incomplete and prevents downstream profitability or admission logic from treating an unknown cost as if the cost was proven to be zero.

**Evidence expected before PASS:** explicit accounting-completeness state, immutable or reproducible cost receipts, long/short symmetry, one-time commission charging, no duplicate slippage subtraction, and negative tests proving that missing funding or fees cannot manufacture a complete net-PnL result.

## Representative finding 7 — Historical replication is not untouched out-of-sample evidence

**Severity:** High  
**Confidence:** High  
**Audit state:** BLOCK if retrospective survivor selection is relabeled as pristine OOS

A later broad experiment may identify a subset of symbols, strategies, regimes or configurations that look interesting. Replaying that selected subset on an earlier historical period can be a useful replication or stress test — but the selection process has already seen information from another historical experiment.

The correct label matters. Calling such a run “untouched OOS” would overstate independence and make the evidence stronger on paper than it is in reality.

**Evidence expected before PASS:** immutable selection provenance, explicit retrospective/replication labeling, frozen train/validation boundaries before outcomes are inspected, no validation-time retuning, disclosed multiple-testing burden, and genuinely future prospective evidence before production admission.

## Representative finding 8 — Engineering readiness is not profitability evidence

**Severity:** High  
**Confidence:** High  
**Audit state:** PASS only when the boundary is explicit

A repository can be fully prepared to execute a research protocol: code accepted, tests green, exact revision frozen, data loader verified, workflow guarded, artifacts reproducible and safety gates closed. None of that proves the economic hypothesis itself.

This is an important distinction for AI-assisted systems because automated engineering progress can make a project look “done” while the empirical question remains unanswered.

The evidence audit therefore separates:

- **engineering readiness** — can the intended experiment run reproducibly and safely?;
- **research result** — what did the experiment actually show?;
- **admission** — is the evidence strong enough to promote a strategy or policy?;
- **execution authorization** — is the system allowed to take real financial action?

A PASS in one layer must not silently grant PASS in the next.

## Representative finding 9 — Retrospective and prospective programs need separate truth states

**Severity:** Medium / High  
**Confidence:** High  
**Audit state:** BLOCK when evidence from one program is used to satisfy the other

It is common for a mature research repository to contain several evidence programs at once: historical replication, broad screening, prospective collection, holdout confirmation, regime diagnostics and deployment-readiness checks.

The danger is not only statistical. Operational documents, dashboards or agents can accidentally collapse those programs into one status and apply the wrong gate to the wrong experiment.

**Evidence expected before PASS:** distinct experiment identities, separate acceptance criteria, exact-subject provenance, explicit supersession rules and fail-closed handling when the active research track is ambiguous.

## Positive evidence matters too

Evidence-first auditing is not limited to defect discovery. Strong patterns can be worth preserving explicitly. Examples include point-in-time universe selection that rejects future metadata, causal delisting treatment, cost accounting that keeps missing evidence unknown, first-class abstention, exact-revision provenance and safety gates that prevent research success from authorizing execution.

The value of the audit is not to replace those mechanisms, but to determine which claims they actually support and where additional evidence is still required.

## Why this is deeper than a scanner

A conventional scanner can detect known code patterns. It generally cannot decide whether:

- the historical universe was knowable at decision time;
- two differently named strategies are economically the same bet;
- a green research artifact actually supports the exact revision being claimed;
- a profitable gross result survives realistic cost assumptions;
- missing funding was incorrectly converted into zero;
- a historical replication is being mislabeled as untouched OOS;
- engineering readiness is being confused with positive economic evidence;
- the system has enough evidence to trade rather than abstain.

Those questions require tracing claims across architecture, data semantics, tests, generated evidence and decision boundaries.

## What was deliberately removed from this public case study

The public version contains **no** private repository name, source code, file paths, commit hashes, issue/PR identifiers, proprietary strategy implementation, parameters, symbols, timeframes, datasets, credentials, account details, infrastructure details, exploitable private finding, or performance number.

That omission is intentional. A useful portfolio example should demonstrate the review method without turning a private system into public documentation.

## Result format

A full audit can separate findings into:

- **PASS** — the requested claim is supported by reviewed evidence;
- **BLOCK** — evidence demonstrates a material problem within scope;
- **UNVERIFIED** — evidence is insufficient to support the claim;
- **NOT_TESTED** — the claim was outside tests actually performed;
- **NOT_APPLICABLE** — genuinely outside the agreed scope.

Missing evidence is never silently converted into PASS.

## Boundary

This case study is not a claim that any trading system is profitable, safe, production-ready, or suitable for investment. It is not financial advice, a penetration test, certification, or compliance attestation. It demonstrates an engineering audit methodology for evaluating whether repository evidence supports the claims being made about a quantitative system.
