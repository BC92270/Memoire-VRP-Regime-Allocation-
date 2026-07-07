# Chapter 4 — Robustness and Implementation Draft

## 1. Introduction

This chapter examines whether the empirical results remain economically meaningful after considering implementation constraints. This is essential because a regime-switching allocation model can look attractive in a frictionless backtest but become less relevant once transaction costs, turnover, rebalancing constraints and crisis-period behavior are taken into account.

The objective is not only to identify the strategy with the highest Sharpe ratio. The objective is to determine whether the strategy is realistic, robust and defensible from a portfolio-management perspective.

The robustness analysis focuses on four dimensions:

1. transaction-cost sensitivity;
2. no-trade band sensitivity;
3. partial rebalancing;
4. crisis-period performance.

The main result of this chapter is that the US HMM RV + Log VRP model remains economically interesting, but only when implementation frictions are controlled. Full rebalancing generates high turnover, while partial rebalancing improves implementability. In Europe, robustness tests confirm that regime-switching models remain economically weak relative to simple benchmarks.

---

## 2. Why implementation matters

The previous chapter showed that VRP-enhanced HMM models can improve downside-risk management in the US. However, a model that reduces drawdown but requires excessive turnover may not be attractive in practice.

Implementation matters for three reasons.

First, transaction costs reduce net returns. Strategies that rebalance frequently are more exposed to costs.

Second, high turnover creates operational complexity. Even if transaction costs are low, frequent rebalancing can make a strategy less realistic.

Third, regime-switching models may react to noise. A model that changes allocation too frequently may overfit short-term fluctuations rather than identify stable regimes.

Therefore, the robustness analysis evaluates whether the results survive more realistic portfolio-construction assumptions.

---

## 3. Transaction-cost sensitivity

### 3.1 Method

Transaction costs are applied through turnover-adjusted returns:

\[
r^{net}_t = r^{gross}_t - c \times Turnover_t
\]

where \(c\) is the transaction-cost rate.

The tested transaction-cost levels are:

\[
0,\ 5,\ 10,\ 25,\ 50 \text{ bps}
\]

The baseline transaction-cost assumption is 10 bps. The sensitivity analysis evaluates how Sharpe ratios and drawdowns evolve when costs increase.

---

### 3.2 US transaction-cost sensitivity: Sharpe ratio

| Strategy | 0 bps | 5 bps | 10 bps | 25 bps | 50 bps |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 1.0275 | 1.0264 | 1.0253 | 1.0219 | 1.0163 |
| 60/40 | 1.0256 | 1.0247 | 1.0238 | 1.0209 | 1.0162 |
| Buy-and-Hold Equity | 0.9955 | 0.9955 | 0.9955 | 0.9955 | 0.9955 |
| HMM RV | 1.0123 | 0.9997 | 0.9870 | 0.9488 | 0.8843 |
| HMM RV + Log VRP | 1.0553 | 1.0370 | 1.0187 | 0.9631 | 0.8694 |
| HMM RV + Raw VRP | 1.0241 | 1.0188 | 1.0135 | 0.9974 | 0.9702 |
| Synthetic Pure VRP Proxy | 2.9144 | 2.9143 | 2.9141 | 2.9136 | 2.9127 |
| RSM RV | 0.8939 | 0.8734 | 0.8530 | 0.7917 | 0.6902 |
| RSM RV + Log VRP | 0.8215 | 0.8066 | 0.7917 | 0.7470 | 0.6720 |
| RSM RV + Raw VRP | 0.9924 | 0.9705 | 0.9486 | 0.8828 | 0.7730 |
| RSM Returns Only | 0.9534 | 0.9411 | 0.9287 | 0.8914 | 0.8290 |

The transaction-cost sensitivity shows that simple benchmarks are highly robust. The Sharpe ratios of the 60/40 and 1/N portfolios barely decline as transaction costs increase, because their turnover is low.

By contrast, regime-switching models are more sensitive to costs. The HMM RV + Log VRP model has the highest Sharpe ratio before costs, at 1.0553. At 10 bps, it remains competitive with a Sharpe ratio of 1.0187. However, at 25 bps and 50 bps, its Sharpe ratio falls materially.

This confirms that the model’s economic value depends on implementation frictions. Without turnover control, the HMM RV + Log VRP specification is less robust than the simple benchmarks.

The RSM models are even more sensitive to transaction costs, especially because they generate higher turnover. This makes them less attractive from an implementation perspective.

---

### 3.3 US transaction-cost sensitivity: maximum drawdown

| Strategy | 0 bps | 5 bps | 10 bps | 25 bps | 50 bps |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.1909 | -0.1909 | -0.1910 | -0.1913 | -0.1916 |
| 60/40 | -0.2005 | -0.2005 | -0.2006 | -0.2008 | -0.2012 |
| Buy-and-Hold Equity | -0.2393 | -0.2393 | -0.2393 | -0.2393 | -0.2393 |
| HMM RV | -0.1770 | -0.1774 | -0.1779 | -0.1793 | -0.1817 |
| HMM RV + Log VRP | -0.1657 | -0.1662 | -0.1667 | -0.1682 | -0.1708 |
| HMM RV + Raw VRP | -0.2198 | -0.2198 | -0.2198 | -0.2198 | -0.2198 |
| Synthetic Pure VRP Proxy | -0.0975 | -0.0975 | -0.0975 | -0.0975 | -0.0975 |
| RSM RV | -0.1539 | -0.1542 | -0.1567 | -0.1642 | -0.1767 |
| RSM RV + Log VRP | -0.2048 | -0.2068 | -0.2088 | -0.2147 | -0.2245 |
| RSM RV + Raw VRP | -0.1542 | -0.1543 | -0.1543 | -0.1645 | -0.1834 |
| RSM Returns Only | -0.1823 | -0.1830 | -0.1837 | -0.1858 | -0.1893 |

The drawdown results are more favorable to regime-switching models. HMM RV + Log VRP maintains a lower maximum drawdown than 60/40 and 1/N across all tested cost levels. At the baseline 10 bps cost, its maximum drawdown is -16.67%, compared with -20.06% for 60/40 and -19.10% for 1/N.

This reinforces the main interpretation: the value of the HMM RV + Log VRP model is not primarily higher return, but downside-risk reduction.

However, the model’s Sharpe sensitivity to costs means that drawdown improvement alone is not sufficient. Turnover control is required to make the strategy more defensible.

---

## 4. No-trade band sensitivity

### 4.1 Method

A no-trade band prevents rebalancing when the difference between current weights and target weights is small. This reduces unnecessary trading.

The tested no-trade bands are:

\[
0\%,\ 2\%,\ 5\%,\ 10\%
\]

The goal is to determine whether avoiding small trades improves the robustness of the regime-switching strategies.

---

### 4.2 No-trade band sensitivity: Sharpe ratio

| Strategy | 0% | 2% | 5% | 10% |
|---|---:|---:|---:|---:|
| HMM RV | 0.9874 | 0.9843 | 0.9928 | 0.9819 |
| HMM RV + Log VRP | 1.0188 | 1.0186 | 1.0221 | 1.0256 |
| HMM RV + Raw VRP | 1.0129 | 1.0130 | 1.0189 | 1.0101 |
| RSM RV | 0.8524 | 0.8523 | 0.8630 | 0.8484 |
| RSM RV + Log VRP | 0.7915 | 0.7924 | 0.7979 | 0.7966 |
| RSM RV + Raw VRP | 0.9479 | 0.9485 | 0.9517 | 0.9480 |
| RSM Returns Only | 0.9290 | 0.9358 | 0.9251 | 0.9524 |

The no-trade band results show modest improvements for some models. For HMM RV + Log VRP, the Sharpe ratio increases from 1.0188 with no band to 1.0256 with a 10% band.

This suggests that some small rebalancing decisions are not economically useful. Filtering them out can slightly improve performance.

However, the improvement is not large enough to change the main conclusion. The no-trade band helps, but it does not fully solve the turnover problem.

---

### 4.3 No-trade band sensitivity: average turnover

| Strategy | 0% | 2% | 5% | 10% |
|---|---:|---:|---:|---:|
| HMM RV | 0.1729 | 0.1662 | 0.1595 | 0.1535 |
| HMM RV + Log VRP | 0.2530 | 0.2461 | 0.2395 | 0.2353 |
| HMM RV + Raw VRP | 0.1007 | 0.0961 | 0.0947 | 0.0933 |
| RSM RV | 0.3265 | 0.3234 | 0.3125 | 0.2952 |
| RSM RV + Log VRP | 0.2448 | 0.2405 | 0.2350 | 0.2096 |
| RSM RV + Raw VRP | 0.3736 | 0.3715 | 0.3617 | 0.3459 |
| RSM Returns Only | 0.1568 | 0.1508 | 0.1442 | 0.1255 |

No-trade bands reduce turnover, but only moderately. For HMM RV + Log VRP, turnover falls from 25.30% to 23.53% when the band increases from 0% to 10%. This is an improvement, but turnover remains elevated.

This explains why the thesis places more emphasis on partial rebalancing than on no-trade bands. No-trade bands help filter small trades, but they do not sufficiently smooth large regime-driven allocation changes.

---

## 5. Partial rebalancing

### 5.1 Method

Partial rebalancing moves the portfolio only partially toward the target allocation.

The rule is:

\[
w_t^{final} = \lambda w_t^{target} + (1-\lambda) w_{t-1}^{portfolio}
\]

where \(\lambda\) is the adjustment speed.

The tested adjustment speeds are:

\[
0.10,\ 0.25,\ 0.50,\ 0.75,\ 1.00
\]

A value of \(\lambda = 1.00\) corresponds to full rebalancing. A lower value means that the strategy moves more gradually toward the model target.

---

### 5.2 Partial rebalancing: Sharpe ratio

| Strategy | 0.10 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| HMM RV | 0.9728 | 0.9634 | 0.9532 | 0.9642 | 0.9874 |
| HMM RV + Log VRP | 1.0196 | 1.0135 | 0.9935 | 1.0011 | 1.0188 |
| HMM RV + Raw VRP | 1.0108 | 0.9985 | 0.9894 | 0.9990 | 1.0129 |
| RSM RV | 0.9991 | 0.9837 | 0.9443 | 0.9011 | 0.8524 |
| RSM RV + Log VRP | 0.9256 | 0.8852 | 0.8402 | 0.8141 | 0.7915 |
| RSM RV + Raw VRP | 1.0062 | 0.9929 | 0.9800 | 0.9672 | 0.9479 |
| RSM Returns Only | 0.9618 | 0.9476 | 0.9288 | 0.9274 | 0.9290 |

The HMM RV + Log VRP model remains competitive across adjustment speeds. Its Sharpe ratio is 1.0135 at a partial rebalancing speed of 0.25, compared with 1.0188 under full rebalancing. The loss in Sharpe ratio is therefore small.

This is important because the main purpose of partial rebalancing is not to maximize Sharpe mechanically. Its purpose is to reduce turnover and improve implementability.

---

### 5.3 Partial rebalancing: average turnover

| Strategy | 0.10 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| HMM RV | 0.0389 | 0.0756 | 0.1183 | 0.1458 | 0.1729 |
| HMM RV + Log VRP | 0.0444 | 0.0910 | 0.1537 | 0.2035 | 0.2530 |
| HMM RV + Raw VRP | 0.0190 | 0.0382 | 0.0632 | 0.0826 | 0.1007 |
| RSM RV | 0.0358 | 0.0787 | 0.1527 | 0.2329 | 0.3265 |
| RSM RV + Log VRP | 0.0360 | 0.0756 | 0.1321 | 0.1848 | 0.2448 |
| RSM RV + Raw VRP | 0.0353 | 0.0810 | 0.1645 | 0.2589 | 0.3736 |
| RSM Returns Only | 0.0361 | 0.0672 | 0.1008 | 0.1276 | 0.1568 |

Partial rebalancing has a much stronger effect on turnover than no-trade bands. For HMM RV + Log VRP, turnover falls from 25.30% under full rebalancing to 9.10% with an adjustment speed of 0.25.

This makes the strategy materially more realistic.

The 0.10 adjustment speed reduces turnover further, but it may react too slowly to regime changes. The 0.25 specification therefore provides a better compromise between responsiveness and implementation control.

---

### 5.4 Partial rebalancing: maximum drawdown

| Strategy | 0.10 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| HMM RV | -0.1929 | -0.1837 | -0.1786 | -0.1787 | -0.1779 |
| HMM RV + Log VRP | -0.1917 | -0.1804 | -0.1734 | -0.1704 | -0.1668 |
| HMM RV + Raw VRP | -0.2210 | -0.2208 | -0.2204 | -0.2202 | -0.2199 |
| RSM RV | -0.1964 | -0.1857 | -0.1711 | -0.1601 | -0.1568 |
| RSM RV + Log VRP | -0.1892 | -0.1863 | -0.1914 | -0.1997 | -0.2088 |
| RSM RV + Raw VRP | -0.1993 | -0.1903 | -0.1782 | -0.1657 | -0.1544 |
| RSM Returns Only | -0.1865 | -0.1802 | -0.1779 | -0.1802 | -0.1837 |

For HMM RV + Log VRP, full rebalancing gives the best maximum drawdown, at approximately -16.68%. Partial rebalancing at 0.25 gives a maximum drawdown of -18.04%.

This is a reasonable trade-off. The strategy sacrifices some drawdown protection but reduces turnover substantially. Since the full-rebalancing model has high turnover, the partial-rebalancing version is more defensible as an implementable allocation strategy.

This supports the final US model selection:

> HMM RV + Log VRP with partial rebalancing speed 0.25 is the most defensible implementable US specification.

---

## 6. Crisis-period analysis

### 6.1 Purpose

The crisis analysis tests whether regime-switching strategies behave defensively during market stress.

This matters because the expected contribution of a regime-based model is not necessarily to increase average returns. Its main value may be to reduce drawdowns and losses during crises.

The tested crisis windows include:

- Eurozone Crisis;
- Covid Crisis;
- Inflation / Rate Shock;
- Volmageddon and late-cycle period;
- full aligned sample.

---

## 7. US crisis analysis

### 7.1 US crisis-period returns

| Strategy | Covid Crisis | Eurozone Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 0.0089 | 0.1217 | 2.3624 | -0.1533 | -0.0185 |
| 60/40 | 0.0014 | 0.1214 | 2.9599 | -0.1585 | -0.0235 |
| Buy-and-Hold Equity | -0.0317 | 0.1161 | 6.4140 | -0.1818 | -0.0457 |
| HMM RV + Log VRP, full | -0.0286 | 0.1094 | 2.4234 | -0.1429 | 0.0220 |
| HMM RV + Log VRP, partial 0.25 | -0.0310 | 0.0973 | 2.5904 | -0.1559 | -0.0168 |
| RSM RV + Raw VRP | -0.0442 | 0.1604 | 3.0815 | -0.0813 | -0.0087 |

During the US inflation and rate shock period, RSM RV + Raw VRP has the best period return, with a loss of only -8.13%. HMM RV + Log VRP full rebalancing also performs better than the traditional benchmarks during the same window.

During the Volmageddon and late-cycle period, HMM RV + Log VRP full rebalancing produces a positive return, while the traditional benchmarks are negative.

However, during the Covid Crisis, the HMM and RSM strategies do not clearly protect better than the benchmarks. This suggests that the regime signal is not uniformly effective across all crisis types.

---

### 7.2 US crisis maximum drawdown

| Strategy | Covid Crisis | Eurozone Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.0651 | -0.0618 | -0.1910 | -0.1605 | -0.0586 |
| 60/40 | -0.0771 | -0.0822 | -0.2006 | -0.1676 | -0.0741 |
| Buy-and-Hold Equity | -0.1249 | -0.1622 | -0.2393 | -0.2025 | -0.1353 |
| HMM RV + Log VRP, full | -0.0304 | -0.0486 | -0.1667 | -0.1399 | -0.0566 |
| HMM RV + Log VRP, partial 0.25 | -0.0735 | -0.0405 | -0.1804 | -0.1457 | -0.0714 |
| RSM RV + Raw VRP | -0.1010 | -0.0710 | -0.1543 | -0.1271 | -0.0708 |

The drawdown results are favorable for the US HMM strategy. HMM RV + Log VRP full rebalancing has lower drawdowns than the benchmarks during the Covid Crisis, Eurozone Crisis, full aligned sample and inflation shock period.

The partial rebalancing version gives up some crisis drawdown protection, but remains competitive on the full sample. It also remains more implementable because of lower turnover.

The RSM RV + Raw VRP model has the best full-sample drawdown, but its turnover remains high. This weakens its practical attractiveness.

---

### 7.3 US crisis Sharpe ratios

| Strategy | Covid Crisis | Eurozone Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 0.1894 | 1.0129 | 1.0253 | -1.0562 | -0.2229 |
| 60/40 | 0.1024 | 0.8438 | 1.0238 | -0.9767 | -0.2291 |
| Buy-and-Hold Equity | -0.0803 | 0.5135 | 0.9955 | -0.7570 | -0.2365 |
| HMM RV + Log VRP, full | -0.4610 | 0.9913 | 1.0187 | -1.4105 | 0.2784 |
| HMM RV + Log VRP, partial 0.25 | -0.3006 | 0.9989 | 1.0135 | -1.3870 | -0.1326 |
| RSM RV + Raw VRP | -0.2866 | 0.9343 | 0.9486 | -0.4292 | -0.0433 |

The US crisis Sharpe ratios are mixed. HMM RV + Log VRP is not universally superior across crisis windows. It performs well in drawdown terms, but not always in Sharpe terms.

This is consistent with the main thesis result: the model’s contribution is defensive and conditional, not universally dominant.

---

## 8. European crisis analysis

### 8.1 European crisis-period returns

| Strategy | Covid Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.0664 | 0.5158 | -0.1029 | -0.0745 |
| 60/40 | -0.0841 | 0.6190 | -0.0948 | -0.0872 |
| Buy-and-Hold Equity | -0.1702 | 1.0219 | -0.0660 | -0.1368 |
| HMM RV | -0.2346 | 0.1068 | -0.1659 | -0.1121 |
| HMM RV + Log VRP | -0.2346 | 0.0818 | -0.1687 | -0.1121 |
| RSM RV | -0.2063 | 0.4270 | -0.1293 | -0.1109 |
| RSM RV + Log VRP | -0.2068 | 0.3519 | -0.1344 | -0.1109 |
| RSM RV + Raw VRP | -0.2063 | 0.2240 | -0.2152 | -0.1099 |
| RSM Returns Only | -0.2053 | 0.4332 | -0.1096 | -0.1131 |

The European crisis-period returns confirm the weakness of the regime-switching models. During the Covid Crisis, the HMM and RSM models lose more than the 1/N and 60/40 benchmarks.

During the full aligned sample, Buy-and-Hold Equity, 60/40 and 1/N all outperform the regime models in period-return terms.

This confirms that the European VRP-based framework does not produce robust defensive value.

---

### 8.2 European crisis maximum drawdown

| Strategy | Covid Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.1713 | -0.2034 | -0.1944 | -0.0684 |
| 60/40 | -0.2050 | -0.2090 | -0.2003 | -0.0821 |
| Buy-and-Hold Equity | -0.3397 | -0.3397 | -0.2261 | -0.1355 |
| HMM RV | -0.2722 | -0.3197 | -0.2325 | -0.1090 |
| HMM RV + Log VRP | -0.2722 | -0.3110 | -0.2350 | -0.1090 |
| RSM RV | -0.2692 | -0.2692 | -0.2448 | -0.1077 |
| RSM RV + Log VRP | -0.2695 | -0.2695 | -0.2471 | -0.1077 |
| RSM RV + Raw VRP | -0.2417 | -0.2815 | -0.2680 | -0.1067 |
| RSM Returns Only | -0.2686 | -0.2686 | -0.2331 | -0.1099 |

The European drawdown analysis confirms that the simple equity-bond benchmarks remain superior. The 1/N portfolio has a full-sample maximum drawdown of -20.34%, while HMM RV + Log VRP has a drawdown of -31.10%.

The regime-switching models reduce drawdown relative to buy-and-hold equity in some cases, but they do not improve on 60/40 or 1/N.

This is an important distinction. A model does not add enough value if it only beats the riskiest benchmark but fails to beat simple diversified portfolios.

---

### 8.3 European crisis Sharpe ratios

| Strategy | Covid Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.3654 | 0.4539 | -0.6308 | -1.5144 |
| 60/40 | -0.3657 | 0.4590 | -0.4928 | -1.5498 |
| Buy-and-Hold Equity | -0.3646 | 0.4629 | -0.1477 | -1.5930 |
| HMM RV | -1.1994 | 0.1455 | -1.2559 | -1.5815 |
| HMM RV + Log VRP | -1.1994 | 0.1281 | -1.2633 | -1.5814 |
| RSM RV | -0.9706 | 0.3187 | -0.6117 | -1.5875 |
| RSM RV + Log VRP | -0.9729 | 0.2822 | -0.6499 | -1.5895 |
| RSM RV + Raw VRP | -1.1906 | 0.2233 | -1.5689 | -1.5869 |
| RSM Returns Only | -0.9662 | 0.3219 | -0.4812 | -1.7151 |

The European Sharpe results are clearly unfavorable to the regime-switching models. The HMM strategies have materially weaker Sharpe ratios than the benchmarks during the full aligned sample and most crisis windows.

This confirms that the European results are not merely weaker because of one metric. They are weak across returns, Sharpe ratios and drawdowns.

---

## 9. Robustness conclusion

The robustness analysis leads to four conclusions.

First, transaction costs matter. Regime-switching models are more sensitive to costs than simple benchmarks because they generate higher turnover.

Second, no-trade bands provide only moderate improvement. They reduce turnover slightly, but they do not fully solve the implementation problem.

Third, partial rebalancing is the most useful implementation adjustment. It materially reduces turnover while preserving competitive performance. For the US HMM RV + Log VRP model, partial rebalancing speed 0.25 is the best compromise between performance, drawdown control and turnover.

Fourth, crisis analysis confirms that the US model has defensive value mainly through drawdown control. However, the crisis results are not uniformly dominant across all windows. In Europe, crisis analysis confirms that regime-switching models do not add enough value relative to simple benchmarks.

The final robustness conclusion is:

> The US HMM RV + Log VRP model is economically defensible only when implemented with turnover control. The European regime-switching results remain weak even after robustness analysis.

---

## 10. Chapter conclusion

This chapter tested whether the empirical results survive implementation constraints.

The results show that the US HMM RV + Log VRP model has useful defensive properties, especially in maximum drawdown terms. However, full rebalancing produces high turnover. Partial rebalancing materially improves the strategy’s implementability and leads to the selection of HMM RV + Log VRP with adjustment speed 0.25 as the most defensible US specification.

The European results are materially weaker. Regime-switching models do not outperform simple benchmarks in the main sample or during crisis periods. This confirms that the VRP signal is not robustly transferable across markets.

The next chapter discusses the limitations of the thesis and explains why the final conclusion must remain conditional rather than universal.