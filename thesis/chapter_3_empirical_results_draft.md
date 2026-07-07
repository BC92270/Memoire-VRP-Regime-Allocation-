# Chapter 3 — Empirical Results Draft

## 1. Introduction

This chapter presents the empirical results of the thesis. The objective is to evaluate whether the Variance Risk Premium creates more economic value when it is directly traded through a synthetic proxy or when it is used as an informational signal inside regime-based allocation models.

The chapter follows the empirical structure introduced in the methodology. It compares:

- traditional benchmarks;
- synthetic pure VRP exposure;
- Hidden Markov Model strategies;
- Markov-switching regression strategies;
- US and European results;
- cross-market evidence.

The central question remains:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The results show a clear asymmetry between the US and European markets. In the US, VRP-enhanced Hidden Markov Models are competitive with traditional equity-bond benchmarks and improve maximum drawdown. In Europe, regime-switching models do not outperform simple benchmarks. The synthetic pure VRP proxy also behaves very differently across markets: it is extremely strong in the US but collapses in Europe.

The main empirical conclusion is therefore nuanced. VRP appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine.

---

## 2. US empirical results

## 2.1 US benchmark results

The first step is to evaluate the traditional benchmark portfolios.

The US benchmark strategies are:

- Buy-and-Hold Equity;
- 60/40 Equity-Bond;
- 1/N Equity-Bond.

The aligned US results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 0.1396 | 0.1420 | 0.9955 | 1.4827 | -0.2393 | 0.5833 | -0.0608 | -0.0818 | 0.0000 | 184 |
| 60/40 | 0.0939 | 0.0921 | 1.0238 | 1.4811 | -0.2006 | 0.4681 | -0.0385 | -0.0520 | 0.0147 | 184 |
| 1/N Equity-Bond | 0.0823 | 0.0805 | 1.0253 | 1.4596 | -0.1910 | 0.4308 | -0.0336 | -0.0458 | 0.0153 | 184 |

The benchmark results show that simple equity-bond portfolios are difficult to outperform. Buy-and-Hold Equity has the highest annualized return, with 13.96%, but it also has the largest drawdown among the three benchmarks, at -23.93%.

The 60/40 and 1/N portfolios produce lower annualized returns but better risk-adjusted performance. Their Sharpe ratios are slightly above 1, with 1.0238 for 60/40 and 1.0253 for 1/N. They also reduce maximum drawdown relative to buy-and-hold equity.

This is an important benchmark result. It means that any regime-switching model must be evaluated against already strong traditional allocation rules. A model that performs well in isolation may still fail to add economic value if it does not improve on these simple portfolios.

---

## 2.2 US synthetic pure VRP proxy

The synthetic pure VRP proxy produces very strong performance in the US sample.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Synthetic Pure VRP Proxy | 0.3875 | 0.1162 | 2.9144 | 4.0317 | -0.0975 | 3.9724 | -0.0229 | -0.0505 | 0.0037 | 184 |

The US synthetic pure VRP proxy strongly outperforms the traditional benchmarks. It has an annualized return of 38.75%, annualized volatility of 11.62%, and a Sharpe ratio of 2.9144. Its maximum drawdown is only -9.75%, materially below the drawdowns of the traditional benchmarks.

However, this result must be interpreted cautiously. The synthetic pure VRP proxy is not a fully tradable variance swap strategy. It does not include variance swap contract pricing, maturity matching, margin requirements, option-market transaction costs, bid-ask spreads, liquidity constraints or variance notional scaling.

Therefore, this result should not be interpreted as direct evidence that an investor could have earned this exact performance by trading variance swaps. Instead, it shows that the US VRP proxy contains strong economic information over the sample.

This distinction is central to the thesis. The pure proxy result supports the informational relevance of the VRP, but not necessarily the direct tradability of the proxy.

---

## 2.3 US HMM results

The HMM specifications test whether VRP-related variables improve regime-based allocation.

The selected US HMM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 0.0817 | 0.0833 | 0.9870 | 1.4462 | -0.1779 | 0.4590 | -0.0428 | -0.0488 | 0.1757 | 184 |
| HMM RV + Raw VRP | 0.1067 | 0.1059 | 1.0135 | 1.5094 | -0.2198 | 0.4853 | -0.0461 | -0.0603 | 0.0957 | 184 |
| HMM RV + Log VRP | 0.0836 | 0.0824 | 1.0187 | 1.4926 | -0.1667 | 0.5013 | -0.0419 | -0.0486 | 0.2535 | 184 |

The HMM results are economically meaningful but nuanced.

The HMM RV + Log VRP model produces a Sharpe ratio of 1.0187, which is close to the 60/40 and 1/N benchmarks. It does not clearly dominate them in terms of Sharpe ratio. However, it improves maximum drawdown. The maximum drawdown of HMM RV + Log VRP is -16.67%, compared with -20.06% for 60/40, -19.10% for 1/N, and -23.93% for buy-and-hold equity.

This is the main positive US HMM result. The model does not primarily create value through higher average returns. Instead, it creates value by reducing downside risk.

The HMM RV + Raw VRP specification has a higher annualized return than HMM RV + Log VRP, at 10.67%, but it has a worse maximum drawdown of -21.98%. This makes it less attractive from a downside-risk perspective.

The HMM RV model without VRP also improves drawdown relative to traditional benchmarks, but its Sharpe ratio is lower than the HMM specifications that include VRP. This suggests that volatility information is useful, but the VRP-enhanced specifications provide additional economic content.

---

## 2.4 US partial rebalancing result

The full-rebalancing HMM RV + Log VRP model has strong downside-risk properties, but it also has high turnover. Its average turnover is 25.35%, which may be too high for a realistic allocation strategy.

To address this issue, partial rebalancing is applied. The most defensible implementable specification is HMM RV + Log VRP with partial rebalancing speed 0.25.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV + Log VRP, full rebalance | 0.0836 | 0.0824 | 1.0187 | 1.4926 | -0.1667 | 0.5013 | -0.0419 | -0.0486 | 0.2535 | 184 |
| HMM RV + Log VRP, partial rebalance 0.25 | 0.0869 | 0.0862 | 1.0135 | 1.4948 | -0.1804 | 0.4819 | -0.0394 | -0.0500 | 0.0910 | 184 |

Partial rebalancing reduces average turnover from 25.35% to 9.10%. The Sharpe ratio remains competitive, falling only slightly from 1.0187 to 1.0135. Maximum drawdown increases from -16.67% to -18.04%, but remains below the drawdown of 60/40 and buy-and-hold equity.

This result is important because it shows that the model can be made more implementable without destroying its economic properties.

The partial rebalancing result supports the idea that VRP-enhanced HMM models are useful not as aggressive return engines, but as controlled risk-management tools.

---

## 2.5 US RSM results

The Markov-switching regression models provide a second regime-based framework.

The selected US RSM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 0.0713 | 0.0776 | 0.9287 | 1.3252 | -0.1837 | 0.3878 | -0.0368 | -0.0463 | 0.1592 | 184 |
| RSM RV | 0.0830 | 0.0995 | 0.8530 | 1.1934 | -0.1567 | 0.5297 | -0.0417 | -0.0585 | 0.3214 | 184 |
| RSM RV + Raw VRP | 0.0961 | 0.1025 | 0.9486 | 1.4117 | -0.1543 | 0.6225 | -0.0398 | -0.0553 | 0.3669 | 184 |
| RSM RV + Log VRP | 0.0757 | 0.0985 | 0.7917 | 1.0882 | -0.2088 | 0.3624 | -0.0432 | -0.0602 | 0.2428 | 184 |

The RSM RV + Raw VRP model has the best maximum drawdown among the implementable US regime-switching strategies, at -15.43%. However, it also has very high turnover, at 36.69%. This makes it less attractive from an implementation perspective.

The RSM results confirm that regime-switching models can improve drawdown, but they also show the cost of model instability. High turnover can reduce the practical value of a strategy even when the headline risk metrics look attractive.

Compared with the HMM results, the RSM results are less compelling. The HMM RV + Log VRP model provides a better balance between Sharpe ratio, drawdown and implementability, especially after partial rebalancing.

---

## 2.6 US conclusion

The US results support the idea that the Variance Risk Premium contains useful information for regime-based allocation.

However, the evidence must be interpreted precisely.

The US evidence does not show that VRP-enhanced regime models clearly dominate traditional benchmarks in all dimensions. The 60/40 and 1/N portfolios remain highly competitive in Sharpe ratio. The value of the HMM RV + Log VRP model is mainly visible in downside-risk control.

The most defensible US result is:

> In the US market, VRP-enhanced HMM models are competitive with traditional equity-bond benchmarks and improve maximum drawdown. The most defensible implementable specification is HMM RV + Log VRP with partial rebalancing.

This supports the interpretation of VRP as a regime-state variable rather than as a simple standalone return factor.

---

## 3. European empirical results

## 3.1 European benchmark results

The European benchmark results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 0.0688 | 0.1835 | 0.4629 | 0.5000 | -0.3397 | 0.2025 | -0.0601 | -0.1215 | 0.0000 | 127 |
| 60/40 | 0.0466 | 0.1140 | 0.4590 | 0.4923 | -0.2090 | 0.2229 | -0.0380 | -0.0760 | 0.0167 | 127 |
| 1/N Equity-Bond | 0.0401 | 0.0975 | 0.4539 | 0.4931 | -0.2034 | 0.1970 | -0.0352 | -0.0656 | 0.0174 | 127 |

The European benchmark results differ from the US results. Sharpe ratios are materially lower in Europe. Buy-and-Hold Equity has the highest annualized return and the highest Sharpe ratio, but it also has the largest drawdown, at -33.97%.

The 60/40 and 1/N portfolios reduce drawdown substantially. Their Sharpe ratios are close to buy-and-hold equity, while their maximum drawdowns are much lower.

This means that the European benchmark environment is difficult for regime-switching models. A model must improve risk-adjusted performance or downside protection relative to already defensive equity-bond benchmarks.

---

## 3.2 European synthetic pure VRP proxy

The European pure VRP proxy performs very poorly.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Pure VRP Proxy | -0.3625 | 0.1508 | -2.8511 | -3.4570 | -0.9901 | -0.3661 | -0.1094 | -0.1453 | 0.0054 | 127 |

This result is one of the most important findings of the thesis. The same synthetic VRP logic that performs extremely well in the US collapses in Europe.

The European pure VRP proxy has an annualized return of -36.25%, a Sharpe ratio of -2.8511, and a maximum drawdown of -99.01%. This makes it economically unusable as a standalone proxy strategy in the European sample.

The contrast between the US and European pure VRP proxies shows that direct synthetic VRP exposure is not robust across markets.

This supports a cautious interpretation:

> The synthetic pure VRP proxy is useful as an exploratory indicator of variance-premium information, but it should not be interpreted as a universally tradable return engine.

---

## 3.3 European HMM results

The European HMM results are weak.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 0.0096 | 0.1233 | 0.1455 | 0.1335 | -0.3197 | 0.0301 | -0.0410 | -0.0902 | 0.1160 | 127 |
| HMM RV + Raw VRP | 0.0076 | 0.1235 | 0.1295 | 0.1193 | -0.3316 | 0.0231 | -0.0410 | -0.0908 | 0.1261 | 127 |
| HMM RV + Log VRP | 0.0075 | 0.1231 | 0.1281 | 0.1177 | -0.3110 | 0.0240 | -0.0410 | -0.0906 | 0.1338 | 127 |

The European HMM models fail to outperform the benchmarks. Their Sharpe ratios are far below the benchmark Sharpe ratios. Their maximum drawdowns are also worse than those of the 60/40 and 1/N portfolios.

The HMM RV + Log VRP model, which is the strongest implementable HMM candidate in the US, performs poorly in Europe. Its Sharpe ratio is only 0.1281 and its maximum drawdown is -31.10%.

This result is important because it shows that the US HMM conclusion does not transfer mechanically to Europe. The model remains technically feasible, but it is economically weak.

---

## 3.4 European RSM results

The European RSM results are stronger than the HMM results but still below the benchmarks.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 0.0346 | 0.1371 | 0.3219 | 0.3235 | -0.2686 | 0.1288 | -0.0456 | -0.0966 | 0.1457 | 127 |
| RSM RV | 0.0342 | 0.1373 | 0.3187 | 0.3241 | -0.2692 | 0.1269 | -0.0453 | -0.0964 | 0.1161 | 127 |
| RSM RV + Raw VRP | 0.0193 | 0.1202 | 0.2233 | 0.2223 | -0.2815 | 0.0685 | -0.0436 | -0.0857 | 0.2476 | 127 |
| RSM RV + Log VRP | 0.0289 | 0.1366 | 0.2822 | 0.2849 | -0.2695 | 0.1072 | -0.0452 | -0.0965 | 0.1437 | 127 |

The best European RSM model is RSM Returns Only, with a Sharpe ratio of 0.3219. However, this is still below the benchmark Sharpe ratios of Buy-and-Hold Equity, 60/40 and 1/N.

Adding VRP does not improve the RSM results. The RSM RV + Raw VRP specification has a lower Sharpe ratio and higher turnover. The RSM RV + Log VRP specification also remains below the returns-only and RV-only models.

This suggests that in Europe, the VRP features do not add robust economic value to regime-switching allocation.

---

## 3.5 European conclusion

The European evidence is negative but highly informative.

The main European conclusion is:

> In the European sample, regime-switching models are technically feasible but economically weak relative to simple equity-bond benchmarks. The VRP signal does not transfer robustly to Europe in the tested specifications.

This does not invalidate the thesis. On the contrary, it strengthens the empirical contribution by showing that VRP-based allocation is not universal.

The European results show that:

- market structure matters;
- volatility-index construction matters;
- proxy quality matters;
- simple benchmarks remain difficult to beat;
- VRP-based allocation is conditional rather than universal.

---

## 4. Cross-market comparison

## 4.1 Key strategy comparison

The cross-market results summarize the main empirical evidence.

| Market | Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover | Obs |
|---|---|---:|---:|---:|---:|---:|---:|
| US | Buy-and-Hold Equity | 0.1396 | 0.1420 | 0.9955 | -0.2393 | 0.0000 | 184 |
| US | 60/40 | 0.0939 | 0.0921 | 1.0238 | -0.2006 | 0.0147 | 184 |
| US | 1/N Equity-Bond | 0.0823 | 0.0805 | 1.0253 | -0.1910 | 0.0153 | 184 |
| US | HMM RV + Log VRP, full rebalance | 0.0836 | 0.0824 | 1.0187 | -0.1667 | 0.2535 | 184 |
| US | HMM RV + Log VRP, partial rebalance 0.25 | 0.0869 | 0.0862 | 1.0135 | -0.1804 | 0.0910 | 184 |
| US | RSM RV + Raw VRP | 0.0961 | 0.1025 | 0.9486 | -0.1543 | 0.3669 | 184 |
| EU | Buy-and-Hold Equity | 0.0688 | 0.1835 | 0.4629 | -0.3397 | 0.0000 | 127 |
| EU | 60/40 | 0.0466 | 0.1140 | 0.4590 | -0.2090 | 0.0167 | 127 |
| EU | 1/N Equity-Bond | 0.0401 | 0.0975 | 0.4539 | -0.2034 | 0.0174 | 127 |
| EU | HMM RV + Log VRP | 0.0075 | 0.1231 | 0.1281 | -0.3110 | 0.1338 | 127 |
| EU | RSM Returns Only | 0.0346 | 0.1371 | 0.3219 | -0.2686 | 0.1457 | 127 |
| EU | RSM RV + Raw VRP | 0.0193 | 0.1202 | 0.2233 | -0.2815 | 0.2476 | 127 |

The cross-market comparison shows that the US and European results are fundamentally different.

In the US, the best HMM model is competitive with traditional benchmarks and improves drawdown. In Europe, the same type of model fails to outperform simple benchmarks.

This result implies that the economic value of VRP-based regime allocation is market-dependent.

---

## 4.2 Pure VRP proxy comparison

The pure VRP proxy comparison is even more striking.

| Market | Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover | Obs |
|---|---|---:|---:|---:|---:|---:|---:|
| US | Synthetic Pure VRP Proxy | 0.3875 | 0.1162 | 2.9144 | -0.0975 | 0.0037 | 184 |
| EU | Pure VRP Proxy | -0.3625 | 0.1508 | -2.8511 | -0.9901 | 0.0054 | 127 |

The synthetic pure VRP proxy is extremely strong in the US and extremely weak in Europe.

This finding is central to the thesis. It shows that the direct VRP proxy is not robust across markets. A result that looks very attractive in one region can collapse in another.

This supports the argument that VRP should not be treated mechanically as a universal return factor.

---

## 4.3 Cross-market interpretation

The cross-market evidence leads to three conclusions.

First, the US evidence supports the informational value of VRP. The HMM RV + Log VRP model improves drawdown while remaining competitive with simple benchmarks.

Second, the European evidence rejects a universal interpretation. VRP-enhanced models fail to outperform traditional portfolios in Europe.

Third, the pure VRP proxy is too unstable to support a strong conclusion in favor of direct VRP exposure.

Therefore, the most defensible interpretation is:

> VRP is more credible as a conditional regime-state variable than as a universally robust standalone return engine.

---

## 5. Answer to the research question

The research question asked:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The empirical answer is conditional.

The direct synthetic VRP proxy performs extremely well in the US but collapses in Europe. This means that direct proxy exposure cannot be considered a robust cross-market return engine.

Using VRP as a regime signal produces more defensible results. In the US, the HMM RV + Log VRP model improves maximum drawdown and remains competitive with strong benchmarks. Its partial rebalancing version also reduces turnover, making it more realistic.

However, the European results show that even the signal-based approach is not universally robust.

The final answer is therefore:

> The Variance Risk Premium appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine. However, its economic value is market-dependent and conditional on implementation assumptions.

---

## 6. Main empirical contribution

The main contribution of this chapter is not to show that a complex model always beats simple benchmarks. The results show the opposite: simple portfolios remain extremely difficult to outperform.

The contribution is more precise.

First, the thesis shows that VRP-enhanced HMM models can improve downside-risk management in the US.

Second, it shows that this result does not replicate in Europe.

Third, it documents a strong instability in synthetic pure VRP proxy performance across markets.

Fourth, it shows that turnover and implementation constraints materially affect the attractiveness of regime-switching strategies.

Fifth, it provides a disciplined comparison against simple benchmarks.

The thesis therefore contributes to the literature by showing that VRP should be interpreted as a conditional market-state signal, not as a universal return factor.

---

## 7. Chapter conclusion

This chapter presented the empirical results of the thesis.

The US results show that VRP-enhanced HMM models are competitive with traditional benchmarks and improve maximum drawdown. The HMM RV + Log VRP model with partial rebalancing is the most defensible implementable specification because it preserves competitive performance while reducing turnover.

The European results are materially weaker. HMM and RSM models do not outperform simple benchmarks, and VRP features do not add robust economic value.

The synthetic pure VRP proxy performs extremely well in the US but collapses in Europe. This confirms that direct VRP proxy exposure is not robust across markets.

The main conclusion is that the Variance Risk Premium is more useful as a conditional regime-state variable than as a universally robust standalone return engine.

The next chapter examines robustness and implementation issues, including transaction costs, no-trade bands, partial rebalancing and crisis-period performance.