# Chapter 2 — Data and Methodology Draft

## 1. Introduction

This chapter presents the data, variable construction, model specifications, portfolio rules and statistical procedures used in the empirical analysis.

The methodology is organized around two distinct evidence layers:

1. an equity–bond allocation layer;
2. a model-based direct variance-payoff layer.

The allocation layer evaluates whether Variance Risk Premium variables improve dynamic portfolio decisions when used inside Hidden Markov Models, Markov-switching regressions and machine-learning classifiers.

The direct-variance layer evaluates whether a payoff linked more directly to the difference between implied and subsequently realized variance generates economic value.

These layers must remain conceptually separate. They use different payoff structures, different aligned samples and different implementation assumptions. Their results can be interpreted jointly, but they must not be ranked mechanically as if they represented identical investment opportunities.

---

## 2. Markets and data

### 2.1 United States

The United States is represented by three financial series:

| Economic component | Proxy | Empirical role |
|---|---|---|
| Equity market | SPY / S&P 500 | Risky asset and return feature |
| Implied volatility | VIX | Implied-variance proxy |
| Bond market | AGG | Defensive asset |

SPY provides the equity price series used to compute daily and monthly equity returns.

The VIX is converted into an annualized implied-variance proxy.

AGG provides the defensive bond return used in the benchmark and dynamic equity–bond portfolios.

The final United States monthly feature dataset contains 257 observations. After the 72-month rolling-estimation requirement and one-step-ahead alignment, the allocation comparison contains 184 out-of-sample observations.

The direct-variance payoff panel contains 256 valid settlement observations. After the minimum lagged-risk-estimation requirements and common-strategy alignment, the direct-variance strategy comparison contains 232 observations.

### 2.2 Europe

Europe is represented by:

| Economic component | Proxy | Empirical role |
|---|---|---|
| Equity market | EURO STOXX 50 | Risky asset and return feature |
| Implied volatility | VSTOXX / V2TX | Implied-variance proxy |
| Bond market | IEAG.AS | Defensive asset |

The European implied-volatility series is reconstructed in the local file:

`data/raw/vstoxx.csv`

The reconstruction combines historical VSTOXX observations with a continuation series. Date strings written in ISO format are parsed explicitly as year-month-day. This prevents European dates such as `2017-01-03` from being incorrectly interpreted under a day-first convention.

After alignment of the equity, volatility and bond components, the European daily feature panel contains 4,041 processed observations. The monthly dataset contains 195 observations.

After rolling estimation and one-step-ahead alignment, the European allocation comparison contains 122 out-of-sample observations.

The direct-variance payoff panel contains 194 valid settlement observations. After lagged-risk estimation and common-strategy alignment, the direct-variance strategy comparison contains 170 observations.

### 2.3 Calendar-gap protection

Daily equity and bond returns are computed only when consecutive prices are separated by no more than seven calendar days.

Let \(P_d\) denote a daily price. The daily log return is:

\[
r_d
=
\log
\left(
\frac{P_d}{P_{d-1}}
\right)
\]

When the calendar gap between \(d-1\) and \(d\) exceeds seven days, the corresponding return is set to missing.

This rule prevents a price movement spanning several weeks or months from being treated as a one-day return. It also forces rolling realized-variance calculations to restart after major interruptions in the source data.

---

## 3. Frequency and monthly aggregation

The raw inputs are daily.

Daily observations are required to construct realized variance and to preserve the timing of implied-volatility information.

Portfolio allocation and strategy evaluation are performed at monthly frequency.

At each month-end:

- the final valid equity price is retained;
- the final valid bond price is retained;
- the final daily volatility features are retained;
- monthly equity and bond holding-period returns are calculated from month-end prices.

For asset \(i\), the monthly simple return is:

\[
R_{i,t}
=
\frac{P_{i,t}}
     {P_{i,t-1}}
-
1
\]

Monthly frequency is appropriate for strategic allocation and reduces noise and excessive rebalancing. It nevertheless means that the analysis does not reproduce daily derivative mark-to-market or intramonth trading decisions.

---

## 4. Realized variance

### 4.1 Daily log returns

Daily realized variance is constructed from equity log returns:

\[
r_d
=
\log
\left(
\frac{P_d}{P_{d-1}}
\right)
\]

### 4.2 Twenty-one-observation rolling measure

The annualized realized-variance proxy is:

\[
RV_d
=
\frac{252}{21}
\sum_{j=0}^{20}
r_{d-j}^{2}
\]

The measure therefore uses the most recent 21 valid daily observations and annualizes their sum of squared log returns.

This is not an exact calendar-month realized-variance measure. It is a trailing 21-observation estimate sampled at month-end.

The distinction matters for interpretation. In particular, the settlement variable used in the direct-variance extension represents the annualized trailing realized variance observed at the settlement month-end, rather than the exact realized variance accumulated between two contractual variance-swap dates.

### 4.3 Log realized variance

A log transformation is also constructed:

\[
\log RV_t
=
\log
\left(
\max(RV_t,\varepsilon)
\right)
\]

where \(\varepsilon\) is a small positive numerical floor.

The transformation reduces scale asymmetry and improves numerical stability in the regime and machine-learning models.

---

## 5. Implied variance

Let \(V_t\) denote the VIX or VSTOXX index level expressed in volatility percentage points.

Annualized implied variance is approximated by:

\[
IV_t
=
\left(
\frac{V_t}{100}
\right)^2
\]

For example, a volatility-index level of 20 corresponds to an implied-volatility estimate of 20% and an implied-variance estimate of:

\[
0.20^2
=
0.04
\]

The volatility index is treated as an implied-variance proxy. It is not identical to an exact variance-swap strike because the thesis does not reconstruct the full option surface or the precise static replication portfolio.

A log implied-variance feature is also calculated:

\[
\log IV_t
=
\log
\left(
\max(IV_t,\varepsilon)
\right)
\]

---

## 6. Variance Risk Premium variables

### 6.1 Raw VRP proxy

The raw Variance Risk Premium proxy is:

\[
VRP_t
=
IV_t
-
RV_t
\]

A positive value means that current implied variance exceeds the trailing realized-variance measure.

A negative value means that realized variance is above implied variance.

For the allocation models, this is an informational feature observed at month-end. It is not itself treated as an observed derivative return.

### 6.2 Log implied-to-realized variance ratio

The relative transformation is:

\[
LogVRP_t
=
\log
\left(
\frac{IV_t}{RV_t}
\right)
\]

This measure is positive when implied variance exceeds realized variance and negative in the opposite case.

Compared with the raw difference, the log ratio:

- expresses the spread proportionally;
- reduces sensitivity to the absolute variance level;
- provides a more symmetric feature;
- can improve numerical behavior in nonlinear models.

### 6.3 Timing distinction

The allocation models use contemporaneously observable month-end VRP features to form the following month’s allocation.

The direct-variance layer uses lagged implied variance as a strike proxy and the subsequent realized-variance observation as settlement.

The same underlying variables therefore enter the two evidence layers through different temporal and economic mappings.

---

## 7. Benchmark portfolios

The principal allocation benchmarks are:

1. Buy-and-Hold Equity;
2. 60/40 Equity–Bond;
3. 1/N Equity–Bond.

### 7.1 Buy-and-Hold Equity

The portfolio remains fully invested in equity:

\[
w^{eq}_t = 1
\]

\[
w^{bond}_t = 0
\]

### 7.2 60/40 portfolio

The portfolio maintains:

\[
w^{eq}_t = 0.60
\]

\[
w^{bond}_t = 0.40
\]

### 7.3 Equal-weighted portfolio

The 1/N benchmark maintains:

\[
w^{eq}_t = 0.50
\]

\[
w^{bond}_t = 0.50
\]

These simple portfolios impose benchmark discipline. A complex dynamic strategy is economically useful only if it improves return, downside risk, welfare or implementation characteristics relative to transparent alternatives.

---

## 8. Hidden Markov Model allocation

### 8.1 Latent-state framework

The Hidden Markov Model assumes that observed variables are generated by an unobservable state process.

Two states are estimated:

1. a normal state;
2. a stress state.

The stress state is identified from the estimated state characteristics, particularly realized variance and adverse market conditions.

### 8.2 HMM feature specifications

The principal HMM specifications include combinations of:

- equity returns;
- log realized variance;
- raw VRP;
- log implied-to-realized variance;
- log implied variance.

The central specifications are:

| Specification | Main features |
|---|---|
| HMM RV | Equity return and log realized variance |
| HMM RV + Raw VRP | Equity return, log realized variance and raw VRP |
| HMM RV + Log VRP | Equity return, log realized variance and log VRP |

Additional specification-grid models are used for diagnostic and model-selection purposes.

### 8.3 Rolling estimation

The HMM is estimated using a rolling window of 72 months.

At signal date \(t\):

1. only observations available through \(t\) enter the model;
2. the latent states are estimated on the rolling historical window;
3. the probability of the stress state is calculated;
4. that probability determines the portfolio weights used for the next holding period.

This procedure prevents full-sample state estimation from leaking future information into the backtest.

### 8.4 Allocation mapping

Let \(p^{stress}_t\) denote the estimated stress probability.

The equity weight is:

\[
w^{eq}_t
=
0.80
\left(
1-p^{stress}_t
\right)
+
0.20
p^{stress}_t
\]

Equivalently:

\[
w^{eq}_t
=
0.80
-
0.60p^{stress}_t
\]

The bond weight is:

\[
w^{bond}_t
=
1-w^{eq}_t
\]

Equity exposure therefore varies continuously between 80% in the lowest-stress case and 20% in the highest-stress case.

---

## 9. Markov-switching regression allocation

The Markov-switching regression provides a second latent-regime framework.

The tested specifications are:

| Specification | Exogenous information |
|---|---|
| RSM Returns Only | No volatility feature |
| RSM RV | Log realized variance |
| RSM RV + Raw VRP | Log realized variance and raw VRP |
| RSM RV + Log VRP | Log realized variance and log VRP |

The RSM produces a stress probability which is mapped into equity and bond weights using the same 80%–20% defensive allocation rule as the HMM.

Using an identical allocation mapping isolates the effect of the regime-estimation method.

The RSM is also estimated on rolling 72-month windows and evaluated one step ahead.

---

## 10. Machine-learning stress classification

### 10.1 Objective

The machine-learning layer tests whether nonlinear classifiers extract stress-prediction information that is not captured by the parametric regime models.

Three classifier families are examined:

- penalized logistic regression;
- Random Forest;
- histogram-based Gradient Boosting.

### 10.2 Feature sets

The base feature set contains:

\[
X^{base}_t
=
\{
R^{eq}_t,
R^{bond}_t,
\log RV_t,
\log IV_t
\}
\]

The VRP-enhanced feature set adds:

\[
X^{VRP}_t
=
X^{base}_t
\cup
\{
VRP_t,
LogVRP_t
\}
\]

Comparing base and VRP-enhanced versions allows the incremental information content of the variance premium to be evaluated.

### 10.3 Stress label

For every rolling training window, the next period is labelled as stress when either:

\[
R^{eq}_{t+1}
\leq
Q_{0.20}
\left(
R^{eq}_{training}
\right)
\]

or:

\[
RV_{t+1}
\geq
Q_{0.80}
\left(
RV_{training}
\right)
\]

The thresholds are recalculated within each rolling training window.

The label therefore identifies periods characterized by either unusually weak equity returns or unusually high realized variance.

### 10.4 Strict one-step-ahead design

At signal date \(t\):

- features dated \(t\) are observable;
- training feature-label pairs end at \(t-1\);
- each training label describes the outcome at \(s+1\);
- quantile thresholds are estimated only from the rolling training window;
- the probability estimated at \(t\) determines weights for \(t+1\).

The estimation window is 72 months.

### 10.5 Allocation rule

The predicted stress probability is mapped into the same continuous equity–bond allocation used by the HMM and RSM:

\[
w^{eq}_t
=
0.80
-
0.60p^{stress}_t
\]

\[
w^{bond}_t
=
1-w^{eq}_t
\]

This makes the economic comparison depend primarily on the quality of the estimated stress probability rather than on different portfolio rules.

### 10.6 Prediction evaluation

Classification is evaluated through:

- ROC-AUC;
- precision–recall AUC;
- Brier score;
- log loss;
- accuracy;
- balanced accuracy;
- precision;
- recall.

Prediction metrics are reported separately from portfolio metrics because stronger classification does not necessarily imply higher investment welfare.

---

## 11. Allocation turnover and transaction costs

For the equity–bond strategies, turnover is the absolute change in target asset weights:

\[
Turnover_t
=
\left|
w^{eq}_t
-
w^{eq}_{t-1}
\right|
+
\left|
w^{bond}_t
-
w^{bond}_{t-1}
\right|
\]

Net portfolio return is:

\[
R^{net}_t
=
R^{gross}_t
-
c
\times
Turnover_t
\]

where \(c\) is the proportional transaction-cost assumption.

The baseline allocation cost is 10 basis points per unit of turnover.

---

## 12. Model-based direct variance-payoff approximation

### 12.1 Methodological status

The direct-variance extension is not a reconstructed variance-swap backtest.

It is a model-based mapping from a variance payoff into a synthetic portfolio-capital return.

It does not use:

- an exact option-replicated variance strike;
- an observed variance-swap price;
- contractual variance notional;
- daily derivative mark-to-market;
- collateral remuneration;
- margin calls;
- dealer bid–ask spreads;
- counterparty adjustments.

### 12.2 Strike proxy

For settlement month \(t\), the strike proxy is the implied variance observed at the preceding month-end:

\[
K^{var}_t
=
IV_{t-1}
\]

The one-period shift ensures that the strike proxy is observable before the settlement variance is realized.

### 12.3 Settlement proxy

The settlement proxy is:

\[
RV^{settlement}_t
=
RV_t
\]

where \(RV_t\) is the annualized trailing 21-observation realized-variance measure sampled at settlement month-end.

### 12.4 Short-variance payoff

The unnormalized short-variance payoff is:

\[
\Pi^{short}_t
=
K^{var}_t
-
RV^{settlement}_t
\]

The normalized payoff is:

\[
\widetilde{\Pi}^{short}_t
=
\frac{
K^{var}_t
-
RV^{settlement}_t
}{
K^{var}_t
}
\]

The corresponding log carry diagnostic is:

\[
LogCarry_t
=
\log
\left(
\frac{
K^{var}_t
}{
RV^{settlement}_t
}
\right)
\]

The normalized payoff is not an observed return on invested capital. It is a dimensionless payoff representation used for risk scaling.

### 12.5 Entry signals

The positive-VRP gate is active when:

\[
VRP_{t-1}
>
0
\]

The High-VRP gate is active when the lagged entry VRP exceeds the median of its preceding rolling history.

The historical median uses a 36-month window with at least 24 observations and is shifted by one additional month. At settlement date \(t\), the threshold therefore uses entry signals corresponding at the latest to \(VRP_{t-2}\). The current entry signal \(VRP_{t-1}\) and the current settlement outcome are excluded from threshold estimation.

### 12.6 Lagged risk estimate

The payoff-volatility estimate is calculated from the normalized payoff:

\[
\widehat{\sigma}_{t-1}
=
Std
\left(
\widetilde{\Pi}^{short}_{t-36},
\ldots,
\widetilde{\Pi}^{short}_{t-1}
\right)
\]

The primary window is 36 months, with a minimum of 24 observations.

The estimate is shifted by one month. At settlement \(t\), it therefore contains only payoffs realized through \(t-1\).

### 12.7 Risk-targeted notional

For annual target volatility \(\sigma^{target}\), the monthly target is:

\[
\sigma^{target}_{monthly}
=
\frac{
\sigma^{target}
}{
\sqrt{12}
}
\]

The unconstrained notional is:

\[
N^{raw}_t
=
\frac{
\sigma^{target}_{monthly}
}{
\widehat{\sigma}_{t-1}
}
\]

The final notional is:

\[
N_t
=
\min
\left(
N^{raw}_t,
N^{max}
\right)
\times
Gate_t
\]

with baseline maximum absolute notional:

\[
N^{max}
=
0.25
\]

The value 0.25 corresponds to a 25% maximum absolute notional.

The principal strategies target either 5% or 10% annual volatility.

The target is an ex ante forecast-volatility objective. It is not a guarantee that ex post realized volatility will equal the target.

### 12.8 Direct-variance strategy set

The four principal specifications are:

| Strategy | Target | Gate |
|---|---:|---|
| Direct Short Variance 5% Vol | 5% | Always active |
| Direct Short Variance 10% Vol | 10% | Always active |
| Direct Short Variance 10% Vol (VRP > 0) | 10% | Positive lagged VRP |
| Direct Short Variance 10% Vol (High VRP) | 10% | VRP above lagged historical median |

All four return series are aligned to their common available sample before comparison.

---

## 13. Monthly roll costs

Each variance exposure represents a one-month payoff.

At settlement, the old exposure expires and a new exposure must be initiated for the following month.

Transaction costs are therefore charged on the full absolute notional entered:

\[
Cost_t
=
c
\left|
N_t
\right|
\]

and not merely on:

\[
\left|
N_t-N_{t-1}
\right|
\]

The latter quantity is retained only as a diagnostic of changes in desired exposure.

The baseline direct-variance roll-cost assumption is 10 basis points per unit of monthly absolute notional.

Net synthetic strategy return is:

\[
R^{DV,net}_t
=
N_t
\widetilde{\Pi}^{short}_t
-
c
\left|
N_t
\right|
\]

This cost remains stylized. It is not an observed bid–ask spread for a variance-swap transaction.

---

## 14. Exploratory Pure VRP Proxy

The Pure VRP Proxy is retained as an exploratory diagnostic.

It represents a synthetic transformation of the implied-to-realized variance relationship.

It is not classified as an implementable direct-variance strategy because it does not reproduce:

- a forward contractual payoff;
- a risk-targeted notional;
- an exact derivative settlement;
- realistic derivative execution.

Its performance is therefore reported separately from the implementable evidence layer.

---

## 15. Performance measures

The strategies are evaluated using:

- annualized geometric return;
- annualized volatility;
- Sharpe ratio;
- Sortino ratio;
- maximum drawdown;
- Calmar ratio;
- monthly VaR at 95%;
- monthly CVaR at 95%;
- average turnover;
- number of observations.

### 15.1 Sharpe ratio

The annualized Sharpe ratio is:

\[
Sharpe
=
\sqrt{12}
\frac{
\overline{R}
}{
\sigma(R)
}
\]

The risk-free rate is treated as zero in the reported strategy comparisons.

### 15.2 Sortino ratio

With a zero monthly minimum acceptable return, downside deviation is:

\[
DD
=
\sqrt{
\frac{1}{T}
\sum_{t=1}^{T}
\min(R_t,0)^2
}
\]

The annualized Sortino ratio is:

\[
Sortino
=
\sqrt{12}
\frac{
\overline{R}
}{
DD
}
\]

Positive observations contribute zero downside rather than being removed from the denominator.

### 15.3 Drawdown

Cumulative wealth is:

\[
W_t
=
\prod_{s=1}^{t}
(1+R_s)
\]

Drawdown is:

\[
DD_t
=
\frac{
W_t
}{
\max_{s\leq t} W_s
}
-
1
\]

Maximum drawdown is the minimum value of \(DD_t\).

### 15.4 Tail risk

The 95% monthly VaR is the empirical fifth percentile of monthly returns.

The 95% CVaR is the average return conditional on being below or equal to that VaR threshold.

---

## 16. Welfare analysis

### 16.1 Mean–variance certainty equivalent

For annualized mean return \(\mu\), annualized variance \(\sigma^2\), and risk-aversion coefficient \(\gamma\), the mean–variance certainty equivalent is:

\[
CEQ^{MV}
=
\mu
-
\frac{\gamma}{2}
\sigma^2
\]

The tested risk-aversion coefficients are:

\[
\gamma
\in
\{
1,3,5,10
\}
\]

### 16.2 CRRA certainty equivalent

A Constant Relative Risk Aversion certainty equivalent is also calculated from the distribution of monthly gross returns.

The CRRA measure captures higher-order distributional effects that are not fully summarized by the first two moments.

The CRRA domain is validated by checking that:

\[
1+R_t
>
0
\]

for every observation.

### 16.3 Fee-equivalent gain

The welfare difference against benchmark \(b\) is:

\[
\Delta CEQ_{s,b}
=
CEQ_s
-
CEQ_b
\]

The annual fee-equivalent value in basis points is:

\[
FeeEquivalent_{s,b}
=
10,000
\times
\Delta CEQ_{s,b}
\]

### 16.4 Block bootstrap

Confidence intervals for welfare differences are calculated using a block bootstrap.

The baseline procedure uses:

- 2,000 bootstrap replications;
- six-month blocks;
- comparisons against 60/40;
- comparisons against 1/N Equity–Bond.

A strategy is classified as statistically superior when the lower confidence bound of its welfare difference is above zero.

---

## 17. Robustness analysis

The direct-variance robustness analysis evaluates six dimensions.

### 17.1 Transaction costs

The tested cost assumptions are:

\[
0,\ 10,\ 25,\ 50
\text{ basis points}
\]

### 17.2 Volatility-estimation window

The tested payoff-volatility windows are:

\[
12,\ 24,\ 36,\ 60
\text{ months}
\]

Comparisons are performed on a common sample within each sensitivity dimension.

### 17.3 Notional caps

The tested maximum notionals are:

\[
5\%,\ 10\%,\ 15\%,\ 25\%,\ 50\%
\]

### 17.4 Subperiods

The strategy is evaluated over:

- the full sample;
- the first half;
- the second half;
- the pre-Covid period;
- the Covid-and-after period.

### 17.5 Crisis exclusions

Robustness tests exclude individual crisis windows and all identified major crises jointly.

This tests whether average performance is driven by a small number of exceptional observations.

### 17.6 Risk aversion

Welfare stability is examined for:

\[
\gamma
=
1,\ 3,\ 5,\ 10
\]

---

## 18. Comparability and interpretation rules

The following rules are applied throughout the thesis.

First, allocation strategies are compared with allocation benchmarks on their aligned 184-observation US and 122-observation European samples.

Second, direct-variance strategies are compared with benchmarks realigned to their 232-observation US and 170-observation European samples.

Third, performance values from different evidence layers are not treated as if they came from the same sample.

Fourth, the Pure VRP Proxy remains exploratory.

Fifth, the direct-variance strategy is described as a model-based approximation rather than as a traded variance-swap return.

Sixth, strong in-sample or historical results are not interpreted as proof of future profitability.

---

## 19. Methodological limitations

The framework improves on a purely contemporaneous VRP proxy by introducing forward alignment, lagged risk targeting, payoff normalization, notional constraints, roll costs and welfare inference.

Nevertheless, it remains subject to major limitations.

It does not reconstruct:

- exact option-implied forward variance;
- an option-replicated variance-swap strike;
- contractual maturity conventions;
- exact variance notional;
- daily derivative valuation;
- collateral and financing;
- variation margin;
- bid–ask spreads;
- dealer intermediation costs;
- counterparty risk;
- market impact under stress.

The direct-variance results must therefore be interpreted as evidence about a stylized payoff mechanism, not as a verified historical return available to an investor.

---

## 20. Summary

The methodology separates the information contained in the Variance Risk Premium from the payoff through which that information may be monetized.

The allocation layer asks whether VRP improves regime identification and equity–bond portfolio decisions.

The direct-variance layer asks whether a forward-aligned short-variance payoff produces economic value after lagged risk control and stylized implementation costs.

The welfare and robustness analyses then evaluate whether apparent performance survives benchmark comparison, sampling uncertainty and alternative implementation assumptions.

This architecture makes it possible to answer the central research question without conflating predictive information, portfolio allocation and derivative payoff exposure.
