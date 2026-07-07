# Thesis Structure

## Working title

**Variance Risk Premium, Regime Detection and Dynamic Asset Allocation: Evidence from US and European Equity Markets**

Alternative title:

**Does the Variance Risk Premium Add More Value as a Tradable Premium or as a Regime-Detection Signal?**

---

## Central research question

The central research question is:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The thesis answers this question through an empirical comparison between:

1. direct synthetic VRP exposure;
2. traditional equity-bond benchmarks;
3. Hidden Markov Model regime-based allocation;
4. Markov-switching regression allocation;
5. US and European market evidence.

---

# Proposed thesis plan

## Introduction

### Objective

Introduce the Variance Risk Premium and explain why it matters for asset allocation, volatility risk and portfolio risk management.

### Key ideas to cover

- Volatility is not only a risk measure but also a priced risk factor.
- Investors often pay a premium for crash protection.
- This creates a difference between implied variance and realized variance.
- The key question is whether this premium should be traded directly or used as a signal.
- The thesis compares the US and European markets to test whether the result is robust across regions.

### Research question

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

### Expected contribution

The thesis contributes by showing that:

- VRP can be useful as a regime-state variable in the US;
- VRP does not transfer robustly to Europe in the tested framework;
- pure synthetic VRP exposure is highly unstable across markets;
- simple benchmarks remain difficult to outperform;
- turnover and implementation assumptions materially affect the value of regime-based allocation.

---

## Chapter 1 — Literature Review

### 1.1 Variance Risk Premium

Explain the VRP as the difference between implied and realized variance.

Core formula:

\[
VRP_t = IV_t - RV_t
\]

Main concepts:

- variance swaps;
- option-implied variance;
- realized variance;
- crash insurance demand;
- volatility risk compensation;
- risk-neutral versus physical expectations.

Key references:

- Bakshi and Kapadia (2003);
- Carr and Wu (2009);
- Bollerslev, Tauchen and Zhou (2009).

### 1.2 Predictive content of VRP

Explain why VRP can contain information about future market states.

Main ideas:

- high implied variance relative to realized variance may reflect stress pricing;
- VRP may proxy risk aversion and crash-protection demand;
- VRP may help forecast equity risk premia or identify fragile regimes.

### 1.3 Regime-switching models

Introduce the logic of regime-dependent markets.

Main ideas:

- market returns and volatility are not stable through time;
- hidden regimes can explain changes in risk and return;
- regime probabilities can be used to dynamically adjust allocation.

Key references:

- Hamilton (1989);
- Ang and Bekaert (2002);
- Guidolin and Timmermann (2007).

### 1.4 Benchmark allocation

Explain why simple benchmarks are essential.

Benchmarks:

- Buy-and-Hold Equity;
- 60/40 Equity-Bond;
- 1/N Equity-Bond.

Key argument:

Complex models must be compared against simple robust portfolios because naive diversification is often difficult to beat out of sample.

Key reference:

- DeMiguel, Garlappi and Uppal (2009).

### File to use

```text
thesis/literature_positioning.md