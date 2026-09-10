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

## Why this is deeper than a scanner

A conventional scanner can detect known code patterns. It generally cannot decide whether:

- the historical universe was knowable at decision time;
- two differently named strategies are economically the same bet;
- a green research artifact actually supports the exact revision being claimed;
- a profitable gross result survives realistic cost assumptions;
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
