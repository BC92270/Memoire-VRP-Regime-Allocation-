# Empirical Update Pack

This document is generated from the final validated output tables. It is the numerical and interpretive source of truth for the thesis rewrite.

Allocation-model and direct-variance results are presented as distinct evidence layers because they use different payoff structures and may use different aligned samples.

---

## 1. Equity–bond allocation evidence

This table compares benchmarks with the strongest HMM, RSM and machine-learning specifications. These strategies belong to the equity–bond allocation evidence layer and must not be directly ranked against direct-variance strategies without acknowledging their different samples and payoff structures.

| Market | Model Group | Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | Benchmark | Buy-and-Hold Equity | 13.96% | 14.20% | 0.995 | 1.483 | -23.93% | -8.18% | 0.00% | 184 |
| US | Benchmark | 60/40 | 9.39% | 9.21% | 1.024 | 1.481 | -20.06% | -5.20% | 1.47% | 184 |
| US | Benchmark | 1/N Equity-Bond | 8.23% | 8.05% | 1.025 | 1.460 | -19.10% | -4.58% | 1.53% | 184 |
| US | HMM | HMM RV + Log VRP (full) | 8.36% | 8.24% | 1.019 | 1.493 | -16.67% | -4.86% | 25.35% | 184 |
| US | RSM | RSM RV + Raw VRP | 9.61% | 10.25% | 0.949 | 1.412 | -15.43% | -5.53% | 36.69% | 184 |
| US | Machine Learning | ML Logistic Base | 7.58% | 7.60% | 1.002 | 1.449 | -18.54% | -4.35% | 17.39% | 184 |
| EU | Benchmark | Buy-and-Hold Equity | 3.98% | 17.17% | 0.313 | 0.468 | -35.74% | -9.86% | 0.00% | 122 |
| EU | Benchmark | 60/40 | 2.68% | 11.24% | 0.292 | 0.428 | -20.32% | -6.55% | 1.74% | 122 |
| EU | Benchmark | 1/N Equity-Bond | 2.30% | 9.84% | 0.280 | 0.408 | -19.66% | -5.85% | 1.81% | 122 |
| EU | HMM | HMM RV | 1.80% | 10.94% | 0.218 | 0.315 | -19.39% | -6.20% | 17.76% | 122 |
| EU | RSM | RSM RV + Raw VRP | 2.55% | 11.24% | 0.281 | 0.407 | -20.47% | -6.74% | 34.00% | 122 |
| EU | Machine Learning | ML Random Forest + VRP | 2.26% | 9.99% | 0.274 | 0.396 | -19.17% | -5.82% | 15.38% | 122 |

---

## 2. Selected direct-variance evidence

The direct-variance extension is a model-based carry approximation. It is not an observed variance-swap return series.

| Market | Model Group | Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | CVaR 95 | Avg Turnover | Obs |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | Direct Variance Approximation | Direct Short Variance 10% Vol (High VRP) | 6.23% | 7.17% | 0.882 | 1.218 | -23.46% | 0.266 | -5.26% | 2.01% | 232 |
| US | Benchmark | 60/40 | 8.00% | 9.92% | 0.827 | 1.276 | -32.35% | 0.247 | -6.28% | 1.63% | 232 |
| US | Benchmark | 1/N Equity-Bond | 7.20% | 8.62% | 0.852 | 1.320 | -26.89% | 0.268 | -5.48% | 1.69% | 232 |
| US | Direct Variance Approximation | Direct Short Variance 10% Vol (VRP > 0) | 8.18% | 16.07% | 0.590 | 0.659 | -39.77% | 0.206 | -13.29% | 3.99% | 232 |

---

## 3. Underlying variance-payoff diagnostics

The payoff is constructed from the lagged implied-variance proxy and the subsequent realized-variance proxy. Frequent positive carry is combined with negatively skewed tail outcomes.

| Market | Observations | Start | End | Mean Variance Strike | Mean Realized Variance | Mean Short Variance Payoff | Positive Payoff Rate | Mean Normalized Payoff | Normalized Payoff Skew | Normalized Payoff 1% | Worst Normalized Payoff | Months Below -100% Rate |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | 256 | 2005-04-30 | 2026-07-31 | 4.35% | 3.57% | 0.78% | 82.42% | 0.253 | -3.849 | -4.080 | -4.432 | 4.69% |
| EU | 194 | 2009-06-30 | 2026-07-31 | 5.22% | 4.02% | 1.21% | 78.35% | 0.239 | -2.231 | -2.060 | -2.439 | 4.12% |

---

## 4. Welfare evidence at gamma = 5

| Market | Strategy | Gamma | MV CEQ Ann. | CRRA CE Ann. | Fee Eq. bps vs 60/40 | Delta MV CEQ CI Low vs 60/40 | Delta MV CEQ CI High vs 60/40 | Fee Eq. bps vs 1/N Equity-Bond | Delta MV CEQ CI Low vs 1/N Equity-Bond | Delta MV CEQ CI High vs 1/N Equity-Bond | Statistically Superior vs 60/40 | Statistically Superior vs 1/N Equity-Bond |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | Direct Short Variance 10% Vol (High VRP) | 5.000 | 5.04% | 5.00% | -70.9 | -5.49% | 4.92% | -45.0 | -4.94% | 4.59% | False | False |
| EU | Direct Short Variance 10% Vol (VRP > 0) | 5.000 | 10.49% | 10.67% | 926.6 | 3.27% | 15.72% | 898.8 | 2.91% | 15.51% | True | True |

Interpretation: the selected US strategy does not establish statistical welfare dominance over both benchmarks. The selected European strategy has positive lower confidence bounds against both 60/40 and 1/N.

---

## 5. Direct-variance robustness

### Transaction-cost sensitivity

| Market | Parameter Label | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | Avg Turnover | MV CEQ Ann. | Delta MV CEQ vs 60/40 | Delta MV CEQ vs 1/N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | 0 bps | 6.26% | 7.18% | 0.885 | -23.42% | -5.26% | 2.01% | 5.06% | -0.69% | -0.43% |
| US | 10 bps | 6.23% | 7.17% | 0.882 | -23.46% | -5.26% | 2.01% | 5.04% | -0.71% | -0.45% |
| US | 25 bps | 6.19% | 7.17% | 0.877 | -23.53% | -5.27% | 2.01% | 5.00% | -0.74% | -0.48% |
| US | 50 bps | 6.13% | 7.16% | 0.869 | -23.63% | -5.28% | 2.01% | 4.95% | -0.80% | -0.54% |
| EU | 0 bps | 13.14% | 9.70% | 1.329 | -21.35% | -7.34% | 4.39% | 10.54% | 9.32% | 9.04% |
| EU | 10 bps | 13.08% | 9.70% | 1.324 | -21.36% | -7.34% | 4.39% | 10.49% | 9.27% | 8.99% |
| EU | 25 bps | 12.99% | 9.69% | 1.316 | -21.38% | -7.35% | 4.39% | 10.41% | 9.19% | 8.91% |
| EU | 50 bps | 12.84% | 9.69% | 1.303 | -21.42% | -7.37% | 4.39% | 10.28% | 9.06% | 8.78% |

### Volatility-lookback sensitivity

| Market | Parameter Label | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | Avg Turnover | MV CEQ Ann. | Delta MV CEQ vs 60/40 | Delta MV CEQ vs 1/N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | 12 months | 8.10% | 16.15% | 0.578 | -50.69% | -11.71% | 3.12% | 2.81% | -3.30% | -2.94% |
| US | 24 months | 6.38% | 9.94% | 0.678 | -32.59% | -7.18% | 2.14% | 4.27% | -1.85% | -1.49% |
| US | 36 months | 6.50% | 7.10% | 0.926 | -23.46% | -5.18% | 1.91% | 5.32% | -0.80% | -0.44% |
| US | 60 months | 6.26% | 6.87% | 0.922 | -23.00% | -5.17% | 1.78% | 5.15% | -0.97% | -0.60% |
| EU | 12 months | 18.35% | 11.21% | 1.570 | -15.92% | -7.92% | 5.65% | 14.45% | 11.74% | 11.78% |
| EU | 24 months | 15.66% | 10.46% | 1.453 | -19.97% | -8.06% | 4.97% | 12.46% | 9.75% | 9.79% |
| EU | 36 months | 14.15% | 9.79% | 1.409 | -21.36% | -7.58% | 4.54% | 11.40% | 8.69% | 8.73% |
| EU | 60 months | 13.92% | 8.93% | 1.513 | -17.21% | -6.70% | 4.27% | 11.52% | 8.80% | 8.84% |

### Notional-cap sensitivity

| Market | Parameter Label | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | Avg Turnover | MV CEQ Ann. | Delta MV CEQ vs 60/40 | Delta MV CEQ vs 1/N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | 5% | 5.37% | 6.53% | 0.836 | -23.46% | -4.91% | 1.73% | 4.39% | -1.35% | -1.09% |
| US | 10% | 6.25% | 7.17% | 0.884 | -23.46% | -5.24% | 2.01% | 5.05% | -0.70% | -0.44% |
| US | 15% | 6.23% | 7.17% | 0.882 | -23.46% | -5.26% | 2.01% | 5.04% | -0.71% | -0.45% |
| US | 25% | 6.23% | 7.17% | 0.882 | -23.46% | -5.26% | 2.01% | 5.04% | -0.71% | -0.45% |
| US | 50% | 6.23% | 7.17% | 0.882 | -23.46% | -5.26% | 2.01% | 5.04% | -0.71% | -0.45% |
| EU | 5% | 12.07% | 7.94% | 1.482 | -17.95% | -5.85% | 3.82% | 10.19% | 8.97% | 8.69% |
| EU | 10% | 13.08% | 9.70% | 1.324 | -21.36% | -7.34% | 4.39% | 10.49% | 9.27% | 8.99% |
| EU | 15% | 13.08% | 9.70% | 1.324 | -21.36% | -7.34% | 4.39% | 10.49% | 9.27% | 8.99% |
| EU | 25% | 13.08% | 9.70% | 1.324 | -21.36% | -7.34% | 4.39% | 10.49% | 9.27% | 8.99% |
| EU | 50% | 13.08% | 9.70% | 1.324 | -21.36% | -7.34% | 4.39% | 10.49% | 9.27% | 8.99% |

### Subperiod stability

| Market | Period | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | Avg Turnover | MV CEQ Ann. | Delta MV CEQ vs 60/40 | Delta MV CEQ vs 1/N |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| US | Full Sample | 6.23% | 7.17% | 0.882 | -23.46% | -5.26% | 2.01% | 5.04% | -0.71% | -0.45% |
| US | First Half | 6.64% | 5.84% | 1.131 | -6.11% | -3.57% | 2.03% | 5.76% | 1.68% | 1.43% |
| US | Second Half | 5.83% | 8.32% | 0.726 | -23.46% | -6.94% | 1.99% | 4.31% | -3.11% | -2.33% |
| US | Pre-Covid | 5.40% | 7.19% | 0.770 | -13.60% | -5.65% | 1.97% | 4.24% | -1.13% | -1.15% |
| US | Covid and After | 7.87% | 7.17% | 1.096 | -15.37% | -4.40% | 2.09% | 6.58% | 0.13% | 0.92% |
| EU | Full Sample | 13.08% | 9.70% | 1.324 | -21.36% | -7.34% | 4.39% | 10.49% | 9.27% | 8.99% |
| EU | First Half | 12.77% | 7.07% | 1.743 | -6.33% | -4.27% | 3.85% | 11.08% | 11.09% | 10.16% |
| EU | Second Half | 13.38% | 11.79% | 1.132 | -21.36% | -9.34% | 4.92% | 9.87% | 7.44% | 7.81% |
| EU | Pre-Covid | 12.81% | 7.30% | 1.695 | -6.33% | -4.65% | 3.90% | 11.04% | 10.43% | 9.66% |
| EU | Covid and After | 13.39% | 11.92% | 1.121 | -21.16% | -10.60% | 4.95% | 9.81% | 7.92% | 8.22% |

### Risk-aversion stability

| Market | Gamma | MV CEQ Ann. | CRRA CE Ann. | Delta MV CEQ vs 60/40 | Delta MV CEQ vs 1/N |
| --- | --- | --- | --- | --- | --- |
| US | 1.000 | 6.07% | 6.23% | -1.65% | -0.91% |
| US | 3.000 | 5.55% | 5.64% | -1.18% | -0.68% |
| US | 5.000 | 5.04% | 5.00% | -0.71% | -0.45% |
| US | 10.000 | 3.75% | 3.11% | 0.47% | 0.12% |
| EU | 1.000 | 12.37% | 13.08% | 8.81% | 9.10% |
| EU | 3.000 | 11.43% | 11.93% | 9.04% | 9.05% |
| EU | 5.000 | 10.49% | 10.67% | 9.27% | 8.99% |
| EU | 10.000 | 8.14% | 6.96% | 9.83% | 8.84% |

---

## 6. Final empirical conclusions

### US regime-allocation evidence

**Evidence layer:** Equity-Bond Allocation

The best HMM/RSM specification is HMM RV + Log VRP (full) with a Sharpe ratio of 1.019, compared with 1.025 for the strongest benchmark (1/N Equity-Bond). The regime-switching layer does not establish robust benchmark dominance.

### US machine-learning evidence

**Evidence layer:** Stress Classification and Equity-Bond Allocation

The strongest ML strategy is ML Logistic Base with a Sharpe ratio of 1.002. Predictive improvements do not by themselves imply statistically significant economic gains relative to simple allocation benchmarks.

### US direct-variance evidence

**Evidence layer:** Model-Based Direct Variance Carry Approximation

The highest-Sharpe direct specification is Direct Short Variance 10% Vol (High VRP) with annualized return 6.23%, volatility 7.17%, Sharpe 0.882 and maximum drawdown -23.46%. Its gamma-five welfare comparison does not establish statistically significant dominance over both 60/40 and 1/N.

### EU regime-allocation evidence

**Evidence layer:** Equity-Bond Allocation

The best HMM/RSM specification is RSM RV + Raw VRP with a Sharpe ratio of 0.281, compared with 0.313 for the strongest benchmark (Buy-and-Hold Equity). The regime-switching layer does not establish robust benchmark dominance.

### EU machine-learning evidence

**Evidence layer:** Stress Classification and Equity-Bond Allocation

The strongest ML strategy is ML Random Forest + VRP with a Sharpe ratio of 0.274. Predictive improvements do not by themselves imply statistically significant economic gains relative to simple allocation benchmarks.

### EU direct-variance evidence

**Evidence layer:** Model-Based Direct Variance Carry Approximation

The highest-Sharpe direct specification is Direct Short Variance 10% Vol (VRP > 0) with annualized return 13.08%, volatility 9.70%, Sharpe 1.324 and maximum drawdown -21.36%. Its gamma-five MV CEQ advantage is statistically positive relative to both 60/40 and 1/N.

### Cross-market main result

**Evidence layer:** Integrated Interpretation

The economic value of the variance risk premium depends critically on the payoff structure through which it is harvested. Adding VRP variables to HMM, RSM or ML allocation models produces limited and model-dependent gains, whereas the direct variance-payoff approximation generates much stronger European evidence.

### US versus Europe

**Evidence layer:** Cross-Market Comparison

The selected US direct-variance strategy improves risk-adjusted performance but does not robustly dominate traditional portfolios in welfare terms. In Europe, the VRP-positive direct strategy produces economically large and bootstrap-significant welfare gains in the tested sample.

### Synthetic proxy

**Evidence layer:** Exploratory Diagnostic

The Pure VRP Proxy remains an exploratory synthetic log-VRP series. Its performance must not be interpreted as a tradable variance-swap return or compared without qualification with implementable strategies.

### Implementation limitation

**Evidence layer:** Methodological Boundary

The direct-variance extension is a model-based carry approximation using lagged implied variance, realized-variance settlement proxies, lagged risk targeting and stylized monthly roll costs. It does not reconstruct an exact variance-swap strike, collateral process, bid-ask spread, margin path or daily mark-to-market.


---

## 7. Mandatory methodological terminology

The following terminology must be used consistently throughout the thesis:

- **Model-based direct variance carry approximation** or **model-based direct variance-payoff approximation**.
- The strike proxy is lagged implied variance derived from the volatility index.
- The settlement proxy is the subsequent annualized trailing realized variance.
- The normalized payoff is not an observed return on invested capital.
- Risk-targeted returns are a synthetic capital mapping from the variance payoff.
- Transaction costs are stylized monthly roll costs applied to the absolute notional entered.
- The framework does not reconstruct an exact variance-swap strike, option surface, collateral account, margin path, bid-ask spread or daily mark-to-market.

The expressions **tradable variance swap return**, **actual variance-swap performance** and similar formulations must not be used for the MVP 7 series.
