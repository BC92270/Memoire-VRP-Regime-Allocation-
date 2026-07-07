# Empirical Results

## 1. Research question

The central research question of this thesis is:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The empirical framework compares the informational value of the Variance Risk Premium across the US and European equity markets. The US market is represented by the S&P 500 and VIX, while the European market is represented by the EURO STOXX 50 and VSTOXX. The study evaluates whether VRP-enhanced regime-switching models improve allocation relative to traditional benchmarks such as buy-and-hold equity, 60/40 equity-bond allocation, and an equal-weighted equity-bond portfolio.

The main empirical result is asymmetric across markets. In the US, VRP-enhanced HMM models are competitive with traditional benchmarks and improve maximum drawdown. In Europe, the same logic does not transfer robustly: regime-switching models remain technically feasible, but fail to outperform simple benchmarks.

---

## 2. US empirical results

### 2.1 Implementable strategies

The US implementable strategy results are summarized below.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 0.0823 | 0.0805 | 1.0253 | 1.4596 | -0.1910 | 0.4308 | -0.0336 | -0.0458 | 0.0153 | 184 |
| 60/40 | 0.0939 | 0.0921 | 1.0238 | 1.4811 | -0.2006 | 0.4681 | -0.0385 | -0.0520 | 0.0147 | 184 |
| HMM RV + Log VRP, full rebalance | 0.0836 | 0.0824 | 1.0187 | 1.4926 | -0.1667 | 0.5013 | -0.0419 | -0.0486 | 0.2535 | 184 |
| HMM RV + Log VRP, partial rebalance 0.25 | 0.0869 | 0.0862 | 1.0135 | 1.4948 | -0.1804 | 0.4819 | -0.0394 | -0.0500 | 0.0910 | 184 |
| Buy-and-Hold Equity | 0.1396 | 0.1420 | 0.9955 | 1.4827 | -0.2393 | 0.5833 | -0.0608 | -0.0818 | 0.0000 | 184 |
| RSM RV + Raw VRP | 0.0961 | 0.1025 | 0.9486 | 1.4117 | -0.1543 | 0.6225 | -0.0398 | -0.0553 | 0.3669 | 184 |

The US evidence indicates that simple equity-bond benchmarks remain difficult to outperform in Sharpe ratio. The 1/N Equity-Bond portfolio reaches a Sharpe ratio of 1.0253, while the 60/40 portfolio reaches 1.0238. The HMM RV + Log VRP model with full rebalancing is very close, with a Sharpe ratio of 1.0187. Therefore, the regime-switching model does not clearly dominate traditional benchmarks on average risk-adjusted performance.

However, the HMM RV + Log VRP model improves downside-risk control. Its full-rebalancing version has a maximum drawdown of -16.67%, compared with -20.06% for 60/40, -19.10% for 1/N, and -23.93% for buy-and-hold equity. This suggests that the VRP-enhanced HMM model is more useful as a defensive allocation mechanism than as an unconditional return-maximization strategy.

The partial rebalancing version of HMM RV + Log VRP is the most defensible implementable specification. It preserves a competitive Sharpe ratio of 1.0135 while reducing average turnover from 25.35% to 9.10%. This makes the strategy more realistic from an implementation perspective.

### 2.2 Synthetic Pure VRP Proxy

The synthetic pure VRP proxy delivers very strong US performance.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover |
|---|---:|---:|---:|---:|---:|
| Synthetic Pure VRP Proxy | 0.3875 | 0.1162 | 2.9144 | -0.0975 | 0.0037 |

This result should be interpreted with caution. The synthetic pure VRP proxy is not a fully tradable variance swap strategy. It is an exploratory benchmark designed to capture the direction and magnitude of the variance premium. Its performance indicates that the US VRP signal contains strong information, but it should not be treated as direct evidence of a frictionless implementable trading strategy.

### 2.3 US interpretation

The US results support the idea that the VRP contains useful information for regime-based allocation. The value is not primarily expressed through unconditional Sharpe domination over simple benchmarks. Instead, the value appears through downside-risk management, especially maximum drawdown reduction.

The strongest US conclusion is:

> In the US market, VRP-enhanced HMM models are competitive with traditional equity-bond benchmarks and improve downside-risk management. The most defensible implementable model is HMM RV + Log VRP with partial rebalancing.

---

## 3. European empirical results

### 3.1 Implementable strategies

The European implementable results are summarized below.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 0.0688 | 0.1835 | 0.4629 | 0.5000 | -0.3397 | 0.2025 | -0.0601 | -0.1215 | 0.0000 | 127 |
| 60/40 | 0.0466 | 0.1140 | 0.4590 | 0.4923 | -0.2090 | 0.2229 | -0.0380 | -0.0760 | 0.0167 | 127 |
| 1/N Equity-Bond | 0.0401 | 0.0975 | 0.4539 | 0.4931 | -0.2034 | 0.1970 | -0.0352 | -0.0656 | 0.0174 | 127 |
| RSM Returns Only | 0.0346 | 0.1371 | 0.3219 | 0.3235 | -0.2686 | 0.1288 | -0.0456 | -0.0966 | 0.1457 | 127 |
| RSM RV | 0.0342 | 0.1373 | 0.3187 | 0.3241 | -0.2692 | 0.1269 | -0.0453 | -0.0964 | 0.1161 | 127 |
| RSM RV + Log VRP | 0.0289 | 0.1366 | 0.2822 | 0.2849 | -0.2695 | 0.1072 | -0.0452 | -0.0965 | 0.1437 | 127 |
| RSM RV + Raw VRP | 0.0193 | 0.1202 | 0.2233 | 0.2223 | -0.2815 | 0.0685 | -0.0436 | -0.0857 | 0.2476 | 127 |
| HMM RV | 0.0096 | 0.1233 | 0.1455 | 0.1335 | -0.3197 | 0.0301 | -0.0410 | -0.0902 | 0.1160 | 127 |
| HMM RV + Log VRP | 0.0075 | 0.1231 | 0.1281 | 0.1177 | -0.3110 | 0.0240 | -0.0410 | -0.0906 | 0.1338 | 127 |

The European results do not confirm the US findings. The benchmarks dominate the regime-switching strategies. Buy-and-hold equity has the highest Sharpe ratio, while 60/40 and 1/N offer materially lower drawdowns. The HMM and RSM specifications fail to improve either Sharpe ratio or drawdown relative to the traditional benchmarks.

The best regime-switching model in Europe is RSM Returns Only, with a Sharpe ratio of 0.3219, but it remains below all three simple benchmarks. HMM RV + Log VRP performs poorly, with a Sharpe ratio of 0.1281 and a maximum drawdown of -31.10%.

### 3.2 European Pure VRP Proxy

The European pure VRP proxy collapses.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover |
|---|---:|---:|---:|---:|---:|
| Pure VRP Proxy | -0.3625 | 0.1508 | -2.8511 | -0.9901 | 0.0054 |

This result sharply contrasts with the US pure VRP proxy. It suggests that the proxy construction is not robust across markets and that direct VRP exposure cannot be assumed to generate stable returns across regions.

### 3.3 European interpretation

The European evidence suggests that the VRP signal does not transfer robustly to the European market under the tested specifications. The models are technically feasible: both HMM and RSM generate regime probabilities and the RSM specifications converge correctly. However, technical feasibility does not imply economic value.

The strongest European conclusion is:

> In the European sample, VRP-enhanced regime-switching models do not outperform simple equity-bond benchmarks. The informational value of VRP appears weaker, less stable, or less exploitable in the tested European allocation framework.

---

## 4. Cross-market comparison

The cross-market comparison gives the central empirical contribution of the thesis.

| Market | Strategy | Sharpe | Max Drawdown | Avg Turnover |
|---|---|---:|---:|---:|
| US | 1/N Equity-Bond | 1.0253 | -0.1910 | 0.0153 |
| US | 60/40 | 1.0238 | -0.2006 | 0.0147 |
| US | HMM RV + Log VRP, full rebalance | 1.0187 | -0.1667 | 0.2535 |
| US | HMM RV + Log VRP, partial rebalance 0.25 | 1.0135 | -0.1804 | 0.0910 |
| US | RSM RV + Raw VRP | 0.9486 | -0.1543 | 0.3669 |
| EU | Buy-and-Hold Equity | 0.4629 | -0.3397 | 0.0000 |
| EU | 60/40 | 0.4590 | -0.2090 | 0.0167 |
| EU | 1/N Equity-Bond | 0.4539 | -0.2034 | 0.0174 |
| EU | HMM RV + Log VRP | 0.1281 | -0.3110 | 0.1338 |
| EU | RSM Returns Only | 0.3219 | -0.2686 | 0.1457 |
| EU | RSM RV + Raw VRP | 0.2233 | -0.2815 | 0.2476 |

The cross-market results show that VRP-based regime allocation is not universally robust. In the US, VRP improves drawdown control and produces competitive risk-adjusted performance. In Europe, the same type of model underperforms simple benchmarks.

The synthetic pure VRP proxy also behaves very differently across markets.

| Market | Strategy | Ann. Return | Sharpe | Max Drawdown |
|---|---|---:|---:|---:|
| US | Synthetic Pure VRP Proxy | 0.3875 | 2.9144 | -0.0975 |
| EU | Pure VRP Proxy | -0.3625 | -2.8511 | -0.9901 |

This contrast is one of the most important findings of the thesis. It shows that direct VRP exposure, at least in proxy form, is highly unstable across regions. This supports the idea that VRP should be used carefully as an informational variable rather than mechanically as a standalone return engine.

---

## 5. Answer to the research question

The research question asked whether the Variance Risk Premium creates more economic value when directly traded or when used as a signal for regime detection and portfolio allocation.

The empirical answer is nuanced.

First, the synthetic pure VRP proxy performs extremely well in the US but collapses in Europe. This means that direct VRP exposure cannot be considered a universally robust return engine in this framework. Its instability across markets makes it unsuitable as the main conclusion of the thesis.

Second, using VRP as a regime-state variable provides more defensible results, especially in the US. The HMM RV + Log VRP model improves maximum drawdown and remains competitive with strong equity-bond benchmarks. Its partial rebalancing version reduces turnover while preserving most of the risk-adjusted performance. This makes the signal-based approach more realistic and more academically defensible than the pure proxy exposure.

Third, the European results impose an important limitation. The VRP signal does not transfer robustly to the European market in the tested specifications. Therefore, the thesis cannot conclude that VRP is a universal regime-allocation signal. Instead, its value depends on market structure, option-market dynamics, feature transformation, model choice, transaction costs and turnover constraints.

The final answer is therefore:

> The Variance Risk Premium appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine. However, its economic value is market-dependent and conditional on implementation assumptions.

---

## 6. Main empirical contribution

The main empirical contribution of this thesis is not to show that a complex regime model mechanically beats simple benchmarks. On the contrary, the results show that traditional benchmarks such as 60/40 and 1/N remain difficult to beat.

The contribution is more precise:

1. The thesis shows that VRP-enhanced regime models can improve downside-risk management in the US.
2. It shows that this result is not robustly replicated in Europe.
3. It documents a strong instability in pure VRP proxy performance across markets.
4. It demonstrates that implementation frictions, turnover and partial rebalancing materially affect the economic value of regime-switching strategies.
5. It provides a comparative framework for evaluating VRP as a signal rather than as a simple return factor.

The thesis therefore contributes to the literature by positioning the Variance Risk Premium as a conditional regime indicator rather than a universally stable allocation factor.