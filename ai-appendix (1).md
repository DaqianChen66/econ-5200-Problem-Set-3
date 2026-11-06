# AI Appendix — ECON 5200 Problem Set 3
## The Rollout That Looked Like It Worked

**Model:** GPT-5.6 Sol  
**Date:** November 5, 2026

> Important: The course requires the AI exchange to be reproduced as raw output, not summarized.
> The prompts below are the prompts used in the project. Before submission, compare the reply sections
> against the original chat and replace any wording that differs from the model's exact raw response.

---

# Task 4.1 — Wild Cluster Bootstrap

## Version 1 Prompt

[Prep] Act as an applied microeconometrician who has implemented
cluster-robust inference for panels with very few clusters.

[Request] Implement the wild cluster bootstrap exactly to the
specification below, for a county-year panel with treatment assigned
at the level of eight regional boards. Impose the null, apply
Rademacher weights at the cluster level, enumerate all 256 weight
vectors rather than resampling, and return the bootstrap p-value for
the treatment coefficient.

1. Fit the restricted model: my DiD regression with the treatment coefficient forced to zero. Keep the restricted residuals and fitted values.
2. Draw one Rademacher weight per board — +1 or −1, each with probability one half. One weight per board, not per observation.
3. Build a synthetic outcome using the restricted fitted values plus the board weight times the restricted residual.
4. Re-estimate the unrestricted model on the synthetic outcome and store the cluster-robust t-statistic on the treatment coefficient.
5. The bootstrap p-value is the share of absolute bootstrap t-statistics at least as large as the actual absolute t-statistic.
6. With 8 boards there are only 2^8 = 256 distinct weight vectors, so enumerate all 256 rather than resampling.

[Iterate] numpy, pandas and statsmodels only. Reuse my panel's column
names. The function must accept the cluster variable as an argument.

[Mechanism Check] Explain why the weights are applied to residuals at
the CLUSTER level rather than the observation level, why imposing the
null matters, and what changes when the number of clusters drops
below roughly ten.

[Evaluate] Run it on my panel and compare the p-value against the
naive cluster-robust one. Tell me which conclusion changes.

## Version 1 Raw Reply

**Replace this section with the exact Version 1 model reply copied directly from the original chat.**

The verified numerical results from that exchange were:

```text
Estimate: 1.523
Cluster p-value: 0.0011
Wild bootstrap p-value: 0.0078
Number of weight vectors: 256
```

---

## Version 2 Prompt

[Prep] Act as an applied microeconometrician who has implemented cluster-robust inference for panels with very few clusters.

[Request] Revise the wild cluster bootstrap for my actual PS3 panel. My DataFrame is called `panel`, with outcome `earnings`, treatment indicator `D`, county identifier `county`, year variable `year`, and regional workforce board identifier `board`.

Estimate the unrestricted model:

`earnings ~ D + C(county) + C(year)`

Treatment is assigned at the `board` level and there are exactly 8 boards.

Implement the wild cluster bootstrap as follows:

1. Fit the restricted model under H0: coefficient on `D` = 0, using `earnings ~ C(county) + C(year)`.
2. Keep the restricted fitted values and residuals.
3. Apply one Rademacher weight (+1 or -1) to each board, so every observation in the same board receives the same weight.
4. Generate the bootstrap outcome from the restricted fitted values plus the board weight times the restricted residual.
5. Re-estimate the unrestricted model with standard errors clustered by `board`.
6. Store the t-statistic on `D`.
7. Enumerate all 2^8 = 256 possible board-level weight vectors instead of randomly resampling.
8. Compute the two-sided bootstrap p-value as the fraction of absolute bootstrap t-statistics at least as large as the absolute actual t-statistic.

Use only numpy, pandas and statsmodels.

Write a reusable function that still accepts the outcome, treatment, unit, time and cluster column names as arguments, so I can place it in `src/did_toolkit.py`.

Return the treatment estimate, actual board-clustered standard error, actual t-statistic, ordinary board-clustered p-value, wild-bootstrap p-value, and number of enumerated weight vectors.

[Mechanism Check] Briefly explain:

- why weights must be applied at the board level;
- why the restricted model must impose the null;
- why 8 clusters make conventional cluster-robust inference questionable;
- why enumeration removes Monte Carlo error;
- what the smallest nonzero two-sided p-value is with 256 sign vectors.

[Evaluate] Run the function on `panel` and compare the ordinary board-clustered p-value with the wild-bootstrap p-value. State whether the statistical-significance conclusion changes.

## Version 2 Raw Reply

**Replace this section with the exact Version 2 model reply copied directly from the original chat.**

The verified numerical results from that exchange were:

```text
Estimate: 1.523
Board-clustered SE: 0.468
Board-clustered p-value: 0.0011
Wild bootstrap p-value: 0.0078
Weight vectors: 256
```

## Changes from Version 1 to Version 2

I revised the prompt to specify my actual DataFrame and column names, the exact unrestricted and restricted formulas, the required return values, the fact that there are exactly eight boards, and that the function must be reusable in `src/did_toolkit.py`.

Because all 256 possible Rademacher sign vectors are enumerated exactly once, there is no bootstrap replication count to choose. Enumeration removes Monte Carlo error, so additional random replications would only repeat sign vectors that have already been used.

---

# Task 4.3 — Hostile Read

## Prompt

[Prep] Act as the state agency's lead econometrician. You believe the
programme works and you are reading an external review that says your
TWFE estimate is uninformative.

[Request] Here is the reviewer's paragraph on parallel trends and
identification:

I omit event time (e=-1), the last year before treatment, so all event-study coefficients are measured relative to the final untreated period.

The pre-treatment coefficients are close to zero, which is consistent with parallel trends before adoption. However, flat pre-trends do not prove the parallel-trends assumption. The identifying assumption concerns what treated counties would have experienced after adoption without the programme, which cannot be observed directly. Therefore, the design still requires an argument that no other board-level changes occurred at the same time as programme adoption and that untreated counties provide a credible counterfactual.

Give the three strongest objections you would raise in a written response.

[Evaluate] Rank them by how much damage each does to the reviewer's conclusion.

## Raw Reply

**Replace this section with the exact hostile-read model reply copied directly from the original chat.**

The three objections raised in the exchange were:

1. The conventional TWFE event study may itself be contaminated by staggered adoption and heterogeneous treatment effects.
2. Flat pre-trends do not show that parallel trends fails; absence of evidence is not evidence of failure.
3. The concern about simultaneous board-level shocks is hypothetical unless an actual coincident policy or shock is identified.

The objections were ranked from strongest to weakest in that order.

---

# Student Response to the Hostile Read

**Objection 1:** The conventional TWFE event study may itself be contaminated by staggered adoption and heterogeneous treatment effects.  
**Decision:** Accept.  
This is a valid limitation, so near-zero pre-treatment coefficients should only be treated as suggestive evidence. I changed the paragraph to make that limitation explicit.

**Objection 2:** Flat pre-trends mean the reviewer has not shown that parallel trends fails.  
**Decision:** Reject.  
My claim is not that parallel trends is proven false. My claim is that flat pre-trends cannot prove the identifying assumption. I clarified that the issue is uncertainty about the counterfactual rather than evidence of a demonstrated pre-trend violation.

**Objection 3:** The concern about simultaneous board-level shocks is only hypothetical.  
**Decision:** Reject.  
The paragraph does not claim that such shocks occurred. It says their absence must be supported as part of the identification argument. I clarified that this requires substantive justification rather than a statistical test.

## Revised Paragraph

I omit event time \(e=-1\), the last year before treatment, so the event-study coefficients are measured relative to the final untreated period. The pre-treatment coefficients are close to zero, which is consistent with parallel trends, but they are only suggestive evidence because a conventional TWFE event study can itself be affected by staggered adoption and heterogeneous treatment effects.

More importantly, parallel trends after adoption is an identifying assumption rather than something the event study can prove. The design requires a credible argument that, without the programme, treated counties would have followed the same outcome path as the never-treated or not-yet-treated counties. That argument must be supported by the rollout process and by evidence that no other board-level changes systematically coincided with adoption.
