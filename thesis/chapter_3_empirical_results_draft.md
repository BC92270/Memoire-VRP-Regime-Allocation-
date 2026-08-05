# Chapter 3 — Empirical Results Draft

## 1. Introduction

This chapter presents the empirical results of the thesis.

The analysis distinguishes two evidence layers.

The first layer evaluates whether Variance Risk Premium variables improve equity–bond allocation when incorporated into Hidden Markov Models, Markov-switching regressions and machine-learning stress classifiers.

The second layer evaluates a model-based direct variance-payoff approximation designed to represent the economic consequences of selling variance exposure.

This distinction is essential. Allocation strategies and direct-variance strategies use different payoff constructions and different aligned samples. They are therefore interpreted jointly but are not ranked mechanically as if they represented identical investment opportunities.

Because the thesis is dated March 2026, all newly generated empirical datasets should be cut off before March 2026. The project configuration therefore fixes the data end date at 2026-02-28. Previously generated output tables may still show later dates if they were produced before the cutoff was imposed; those tables should be regenerated before final submission.

Because the HMM, RSM, machine-learning and direct-variance layers impose different rolling-window, one-step-ahead and payoff-alignment requirements, some summary files may contain different observation counts. Comparisons are therefore made within each evidence layer on its own aligned sample, rather than by mechanically pooling all reported rows across files.

The allocation comparisons contain:

| Market | Out-of-sample observations |
|---|---:|
| United States | 184 |
| Europe | 122 |

The direct-variance comparisons contain:

| Market | Strategy observations |
|---|---:|
| United States | 232 |
| Europe | 170 |

---

## 2. Equity–bond allocation evidence

### 2.1 United States benchmarks

The United States allocation benchmarks are:

- Buy-and-Hold Equity;
- 60/40 Equity–Bond;
- 1/N Equity–Bond.

Their aligned out-of-sample results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 13.96% | 14.20% | 0.995 | 1.483 | −23.93% | −8.18% | 0.00% | 184 |
| 60/40 | 9.39% | 9.21% | 1.024 | 1.481 | −20.06% | −5.20% | 1.47% | 184 |
| 1/N Equity–Bond | 8.23% | 8.05% | 1.025 | 1.460 | −19.10% | −4.58% | 1.53% | 184 |

Buy-and-Hold Equity generates the highest annualized return, but it also produces the greatest volatility and the largest drawdown among the three benchmarks.

The 60/40 and 1/N portfolios sacrifice return in exchange for lower volatility, lower tail losses and smaller drawdowns. Their Sharpe ratios are slightly above one.

The equal-weighted portfolio produces the highest benchmark Sharpe ratio, at 1.025. This creates a demanding comparison for the regime and machine-learning models.

---

### 2.2 United States HMM results

The principal HMM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 8.17% | 8.33% | 0.987 | 1.446 | −17.79% | −4.88% | 17.57% | 184 |
| HMM RV + Raw VRP | 10.67% | 10.59% | 1.014 | 1.509 | −21.98% | −6.03% | 9.57% | 184 |
| HMM RV + Log VRP | 8.36% | 8.24% | 1.019 | 1.493 | −16.67% | −4.86% | 25.35% | 184 |

The highest HMM Sharpe ratio is obtained by HMM RV + Log VRP, at 1.019.

This value is close to the 60/40 and 1/N benchmarks, but remains slightly below them. The model therefore does not establish superior average risk-adjusted performance.

Its principal advantage is drawdown control. Its maximum drawdown is −16.67%, compared with −20.06% for 60/40, −19.10% for 1/N and −23.93% for Buy-and-Hold Equity.

The improvement in drawdown is economically relevant, but the strategy requires substantially greater turnover. Average turnover reaches 25.35%, compared with approximately 1.5% for the balanced benchmarks.

The HMM RV + Raw VRP model produces a higher annualized return of 10.67%, but its drawdown and volatility are also higher. Its risk-adjusted performance does not exceed the simple benchmarks.

The United States HMM evidence therefore supports a limited conclusion: VRP-related variables can alter the risk profile of dynamic allocation, particularly the maximum drawdown, but they do not generate robust benchmark dominance.

---

### 2.3 United States RSM results

The principal Markov-switching regression results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 7.13% | 7.76% | 0.929 | 1.325 | −18.37% | −4.63% | 15.92% | 184 |
| RSM RV | 8.30% | 9.95% | 0.853 | 1.193 | −15.67% | −5.85% | 32.14% | 184 |
| RSM RV + Raw VRP | 9.61% | 10.25% | 0.949 | 1.412 | −15.43% | −5.53% | 36.69% | 184 |
| RSM RV + Log VRP | 7.57% | 9.85% | 0.792 | 1.088 | −20.88% | −6.02% | 24.28% | 184 |

RSM RV + Raw VRP produces the highest RSM Sharpe ratio, at 0.949, and the smallest drawdown, at −15.43%.

However, its average turnover reaches 36.69%. The reduction in drawdown is therefore accompanied by considerable implementation intensity.

None of the RSM specifications dominates the balanced benchmarks in Sharpe ratio. The RSM results reinforce the distinction between improvements in a specific risk dimension and broad economic superiority.

---

### 2.4 United States machine-learning results

The strongest United States machine-learning allocation strategy is ML Logistic Base:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ML Logistic Base | 7.58% | 7.60% | 1.002 | 1.449 | −18.54% | −4.35% | 17.39% | 184 |

The strategy produces volatility below the traditional balanced portfolios and a maximum drawdown below that of Buy-and-Hold Equity and 60/40.

Its Sharpe ratio remains below those of 60/40 and 1/N.

The strongest machine-learning portfolio is also a base specification without VRP variables. This means that the inclusion of VRP does not universally improve machine-learning allocation in the United States.

Prediction quality and portfolio value must therefore remain distinct. A classifier may improve a statistical prediction metric without producing a sufficiently different allocation to improve investor welfare.

---

### 2.5 United States allocation conclusion

The United States allocation evidence does not support a claim of robust model dominance.

The best dynamic models are competitive with simple benchmarks and may improve particular downside-risk measures, especially maximum drawdown.

However:

- the strongest benchmark Sharpe ratio is 1.025;
- the strongest HMM Sharpe ratio is 1.019;
- the strongest RSM Sharpe ratio is 0.949;
- the strongest ML Sharpe ratio is 1.002.

The economic advantage of the dynamic models is therefore limited and dependent on the selected performance criterion.

---

### 2.6 European benchmarks

The corrected European allocation results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 3.98% | 17.17% | 0.313 | 0.468 | −35.74% | −9.86% | 0.00% | 122 |
| 60/40 | 2.68% | 11.24% | 0.292 | 0.428 | −20.32% | −6.55% | 1.74% | 122 |
| 1/N Equity–Bond | 2.30% | 9.84% | 0.280 | 0.408 | −19.66% | −5.85% | 1.81% | 122 |

Risk-adjusted performance is materially weaker in Europe than in the United States.

Buy-and-Hold Equity produces the highest benchmark Sharpe ratio, at 0.313, but also the largest drawdown, at −35.74%.

The balanced portfolios substantially reduce drawdown and tail risk. Their Sharpe ratios remain close to the equity benchmark.

---

### 2.7 European HMM results

The corrected European HMM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 1.80% | 10.94% | 0.218 | 0.315 | −19.39% | −6.20% | 17.76% | 122 |
| HMM RV + Raw VRP | 1.55% | 11.10% | 0.166 | 0.239 | −21.07% | −6.34% | 25.83% | 122 |
| HMM RV + Log VRP | 1.66% | 11.11% | 0.179 | 0.257 | −20.81% | −6.34% | 29.59% | 122 |

The HMM RV model without VRP produces the highest HMM Sharpe ratio, at 0.218.

Adding raw or log VRP reduces the Sharpe ratio and increases turnover.

The HMM models generate drawdowns close to those of the balanced benchmarks, but do not improve return or risk-adjusted performance sufficiently to compensate for their greater complexity.

The corrected data therefore do not imply that the VRP is absent in Europe. Instead, they show that adding VRP to these HMM allocation specifications does not improve portfolio performance.

---

### 2.8 European RSM results

The European RSM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 2.12% | 10.61% | 0.239 | 0.344 | −19.74% | −6.28% | 15.14% | 122 |
| RSM RV | 1.85% | 10.75% | 0.216 | 0.310 | −20.01% | −6.44% | 30.63% | 122 |
| RSM RV + Raw VRP | 2.55% | 11.24% | 0.281 | 0.407 | −20.47% | −6.74% | 34.00% | 122 |
| RSM RV + Log VRP | 2.33% | 10.86% | 0.263 | 0.380 | −19.78% | −6.38% | 28.01% | 122 |

RSM RV + Raw VRP is the strongest European regime specification.

Its Sharpe ratio of 0.281 is close to the 1/N benchmark but remains below Buy-and-Hold Equity and 60/40.

Its average turnover is 34.00%, compared with less than 2% for the balanced benchmarks.

The RSM result indicates that raw VRP contains some useful information within this model family, but the economic gain is insufficient to establish benchmark dominance.

---

### 2.9 European machine-learning results

The strongest European machine-learning portfolio is:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ML Random Forest + VRP | 2.26% | 9.99% | 0.274 | 0.396 | −19.17% | −5.82% | 15.38% | 122 |

The model achieves a maximum drawdown slightly below the balanced benchmarks and a Sharpe ratio close to 1/N.

Its portfolio performance is economically competitive, but not superior.

The predictive results show that VRP variables add information in some nonlinear specifications, particularly the Random Forest. However, the portfolio and welfare results show that this incremental information does not translate into statistically significant gains over simple portfolios.

---

### 2.10 European allocation conclusion

The corrected European evidence is not that the Variance Risk Premium disappears.

The appropriate conclusion is narrower:

> VRP-related variables contain model-dependent information, but their inclusion in the tested HMM, RSM and machine-learning equity–bond allocation models does not produce robust dominance over simple benchmarks.

This distinction becomes important when the direct-variance results are introduced.

---

## 3. Direct variance-payoff diagnostics

The direct-variance layer begins with the underlying payoff rather than with a portfolio-allocation rule.

The strike proxy is lagged implied variance:

\[
K^{var}_t = IV_{t-1}
\]

The settlement proxy is the realized-variance measure observed at \(t\):

\[
RV^{settlement}_t = RV_t
\]

The normalized short-variance payoff is:

\[
\widetilde{\Pi}^{short}_t
=
\frac{
IV_{t-1}-RV_t
}{
IV_{t-1}
}
\]

The underlying diagnostics are:

| Market | Obs | Mean Strike | Mean RV | Mean Short Payoff | Positive Months | Mean Normalized Payoff | Skewness | 1% Quantile | Worst Payoff | Below −100% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| United States | 256 | 4.35% | 3.57% | 0.78% | 82.42% | 0.253 | −3.849 | −4.080 | −4.432 | 4.69% |
| Europe | 194 | 5.22% | 4.02% | 1.21% | 78.35% | 0.239 | −2.231 | −2.060 | −2.439 | 4.12% |

Both markets display the central short-variance characteristic:

- positive payoff in a large majority of observations;
- positive average carry;
- severe negative skewness;
- occasional losses exceeding the strike-normalized initial exposure.

The European average variance spread is larger than the United States spread in the sample.

However, average carry alone is insufficient. The highly negative tail observations mean that notional scaling and welfare analysis are necessary.

---

## 4. United States direct-variance results

The main United States direct-variance results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct Short Variance 5% Vol | 4.16% | 8.03% | 0.548 | 0.631 | −23.46% | −6.79% | 2.31% | 232 |
| Direct Short Variance 10% Vol | 8.43% | 16.07% | 0.604 | 0.696 | −39.77% | −13.57% | 4.61% | 232 |
| Direct Short Variance 10% Vol (VRP > 0) | 8.18% | 16.07% | 0.590 | 0.659 | −39.77% | −13.29% | 3.99% | 232 |
| Direct Short Variance 10% Vol (High VRP) | 6.23% | 7.17% | 0.882 | 1.218 | −23.46% | −5.26% | 2.01% | 232 |

The always-active 10% strategy experiences volatility far above its target and a drawdown of approximately 40%.

This illustrates the weakness of purely backward-looking risk targeting in a negatively skewed payoff. A lagged volatility estimate cannot guarantee ex post volatility when a large variance shock occurs.

The positive-VRP gate does not materially improve the United States result. It retains most active months and remains exposed to the principal tail losses.

The High-VRP filter is more effective. It reduces activity, volatility and drawdown and produces the strongest Sharpe ratio, at 0.882.

Relative to the aligned benchmarks:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown |
|---|---:|---:|---:|---:|
| High-VRP direct variance | 6.23% | 7.17% | 0.882 | −23.46% |
| 60/40 | 8.00% | 9.92% | 0.827 | −32.35% |
| 1/N Equity–Bond | 7.20% | 8.62% | 0.852 | −26.89% |

The High-VRP strategy has a higher Sharpe ratio and lower drawdown than the two aligned benchmarks. However, these headline metrics do not establish welfare dominance because sampling uncertainty and nonlinear tail risk remain substantial.

---

## 5. European direct-variance results

The European direct-variance results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct Short Variance 5% Vol | 6.78% | 5.69% | 1.186 | 1.708 | −11.00% | −4.09% | 2.70% | 170 |
| Direct Short Variance 10% Vol | 13.61% | 11.37% | 1.186 | 1.708 | −21.37% | −8.18% | 5.40% | 170 |
| Direct Short Variance 10% Vol (VRP > 0) | 13.08% | 9.70% | 1.324 | 1.891 | −21.36% | −7.34% | 4.39% | 170 |
| Direct Short Variance 10% Vol (High VRP) | 6.39% | 7.65% | 0.852 | 1.214 | −16.97% | −5.97% | 2.33% | 170 |

The strongest European specification is the 10% target strategy with a positive-VRP gate.

It produces:

- annualized return of 13.08%;
- annualized volatility of 9.70%;
- Sharpe ratio of 1.324;
- Sortino ratio of 1.891;
- maximum drawdown of −21.36%;
- average monthly roll notional of 4.39%.

The always-active strategy also performs strongly, but the positive-VRP gate lowers realized volatility while preserving most of the annual return.

The High-VRP gate is less effective in Europe. Requiring the VRP to exceed its historical median removes many months in which the variance spread remains positive and economically valuable.

The European evidence therefore favors a simple sign filter rather than an extreme-value filter.

---

## 6. Welfare analysis

Headline performance metrics do not directly measure investor utility.

The welfare analysis compares the direct-variance strategies with 60/40 and 1/N using mean–variance and CRRA certainty equivalents.

At a risk-aversion coefficient of five, the selected strategies produce:

| Market | Strategy | MV CEQ | CRRA CE | Fee equivalent vs 60/40 | 95% CI vs 60/40 | Fee equivalent vs 1/N | 95% CI vs 1/N |
|---|---|---:|---:|---:|---:|---:|---:|
| United States | 10% High VRP | 5.04% | 5.00% | −70.9 bp | [−5.49%, 4.92%] | −45.0 bp | [−4.94%, 4.59%] |
| Europe | 10% VRP > 0 | 10.49% | 10.67% | 926.6 bp | [3.27%, 15.72%] | 898.8 bp | [2.91%, 15.51%] |

### 6.1 United States welfare

The selected United States strategy does not dominate the benchmarks.

Its estimated mean–variance certainty equivalent is lower than both comparison portfolios. More importantly, the bootstrap confidence intervals contain zero.

The data therefore do not establish that the strategy produces a statistically positive welfare gain.

The United States conclusion is:

> The High-VRP direct-variance approximation improves selected risk-adjusted performance measures but does not establish robust investor-welfare dominance.

### 6.2 European welfare

The European result is materially different.

The selected strategy has a mean–variance certainty equivalent of 10.49% and a CRRA certainty equivalent of 10.67%.

The estimated fee-equivalent advantage is approximately:

- 927 basis points relative to 60/40;
- 899 basis points relative to 1/N.

The lower bootstrap confidence bounds are positive against both benchmarks.

Within the tested model and sample, the European welfare advantage is therefore statistically significant.

This statistical result is stronger than a comparison based only on Sharpe ratios.

---

## 7. Cross-market interpretation

The cross-market evidence cannot be summarized by stating that VRP works in one region and fails in another.

The evidence is conditional on the economic mechanism.

### 7.1 Informational allocation channel

In both markets:

- HMM, RSM and ML models are feasible;
- VRP variables affect state probabilities or classification;
- some models improve particular downside-risk measures;
- simple benchmarks remain difficult to beat;
- robust welfare dominance is not established.

### 7.2 Direct payoff channel

In the United States:

- average variance carry is positive;
- the payoff is strongly negatively skewed;
- the High-VRP filter improves the profile;
- welfare dominance is not statistically established.

In Europe:

- average variance carry is also positive;
- the positive-VRP gate produces strong risk-adjusted performance;
- welfare gains remain positive under bootstrap inference;
- the result survives the principal robustness tests.

### 7.3 Central empirical result

The main empirical result is:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested.

Using VRP as a state variable and harvesting a variance-linked payoff are not economically equivalent.

---

## 8. Interpretation of the Pure VRP Proxy

The Pure VRP Proxy is retained as an exploratory diagnostic only.

It is not a forward contractual payoff and does not include:

- lagged strike formation;
- settlement mechanics;
- risk-targeted variance notional;
- monthly roll costs;
- derivative execution constraints.

Its high historical performance must therefore not be interpreted as evidence of a directly tradable strategy.

The direct-variance extension is methodologically stronger because it imposes forward timing and explicit risk scaling. It nevertheless remains an approximation rather than a reconstructed variance-swap return.

---

## 9. Answer to the empirical question

The empirical question asks whether the Variance Risk Premium creates more economic value through direct variance carry or through its informational content for dynamic allocation.

The allocation evidence is limited. VRP-enhanced models can improve particular risk dimensions, but they do not consistently dominate simple portfolios.

The direct-payoff evidence is stronger in Europe. The positive-VRP strategy produces large and statistically significant welfare gains within the tested sample and model.

The United States evidence remains more cautious. The selected direct-variance strategy improves selected risk metrics but does not establish welfare superiority.

The most defensible empirical answer is therefore:

> The Variance Risk Premium does not possess a single, market-independent form of economic value. Its contribution depends on how it is transformed into a portfolio payoff. In the tested European sample, the model-based direct variance-payoff approximation creates substantially greater economic value than the use of VRP as an allocation feature. In the United States, neither channel establishes robust welfare dominance over traditional portfolios.

---

## 10. Summary

Five findings emerge.

First, the corrected European data invalidate the earlier claim that the European variance premium disappears.

Second, HMM, RSM and machine-learning allocation models do not establish robust superiority over simple equity–bond portfolios.

Third, short-variance payoffs display positive average carry and severe negative skewness in both markets.

Fourth, the selected United States direct-variance specification improves headline risk-adjusted metrics but does not generate statistically significant welfare gains.

Fifth, the selected European direct-variance specification produces strong and bootstrap-significant welfare gains, although it remains a model-based approximation subject to important implementation limitations.

These findings motivate the robustness and implementation analysis developed in the next chapter.
