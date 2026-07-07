# Chapter 2 — Data and Methodology Draft

## 1. Introduction

This chapter presents the empirical methodology used to evaluate whether the Variance Risk Premium creates more economic value when it is directly traded or when it is used as an informational signal for regime-based asset allocation.

The empirical framework is designed around five objectives.

First, it constructs volatility-based features from equity-index and volatility-index data. Second, it builds traditional benchmark portfolios in order to evaluate whether more complex models add economic value. Third, it estimates regime-switching models using Hidden Markov Models and Markov-switching regressions. Fourth, it evaluates all strategies out of sample using a rolling-window design. Fifth, it analyzes implementation issues such as transaction costs, turnover, partial rebalancing and crisis-period behavior.

The methodology is applied to two markets:

- the US equity market;
- the European equity market.

This cross-market design is important because the thesis does not only ask whether the Variance Risk Premium is useful in one market. It asks whether its economic value is robust across different market structures.

---

## 2. Data

## 2.1 US market

The US market is represented by three financial series:

| Variable | Proxy | Role |
|---|---|---|
| Equity market | SPY / S&P 500 | Risk asset |
| Implied volatility | VIX | Implied volatility index |
| Bond market | AGG | Defensive asset |

The S&P 500 is used as the main equity-market proxy. The VIX is used as the implied-volatility proxy because it is one of the most widely used measures of US equity-index option-implied volatility. AGG is used as the bond-market proxy in order to construct equity-bond allocation strategies.

The daily US dataset starts in 2005 and extends to 2026 in the current implementation. After monthly aggregation, the main US monthly dataset contains 257 observations. However, models that require rolling estimation windows use a shorter aligned out-of-sample period. In the final aligned US comparisons, the number of out-of-sample observations is 184.

The US dataset is more reliable than the European dataset because VIX and SPY data are easily accessible and consistently available over the full sample.

---

## 2.2 European market

The European market is represented by three financial series:

| Variable | Proxy | Role |
|---|---|---|
| Equity market | EURO STOXX 50 | Risk asset |
| Implied volatility | VSTOXX / V2TX | Implied volatility index |
| Bond market | IEAG.AS | Defensive asset |

The EURO STOXX 50 is used as the European equity-market proxy. The VSTOXX is used as the implied-volatility proxy because it measures implied volatility on EURO STOXX 50 options. IEAG.AS is used as the bond-market proxy.

The European volatility dataset required manual reconstruction. The VSTOXX series is built from two sources:

1. official STOXX historical VSTOXX data up to 2016;
2. MarketWatch V2TX data from 2017 to 2026.

These two sources are merged into a single local file:

data/raw/vstoxx.csv

This reconstruction allows the European sample to be extended beyond the one-year download limit of some public data sources. However, it also introduces a limitation: the European volatility series may contain source differences, timestamp differences or methodology differences between the official historical data and the MarketWatch continuation data.

After the reconstruction, the European monthly dataset contains 200 monthly observations. After the rolling-window alignment required by the HMM and RSM models, the final European out-of-sample comparison contains 127 observations.

---

## 2.3 Data frequency

The raw input data are daily. However, the empirical analysis is conducted at monthly frequency.

This choice is deliberate. Monthly rebalancing is more appropriate for strategic allocation than daily rebalancing because it reduces turnover, transaction costs and noise. It also makes the framework more realistic for portfolio-allocation applications.

The daily data are used to compute realized variance. The resulting realized variance, implied variance, VRP and returns are then aggregated or sampled at monthly frequency.

---

## 3. Feature construction

The empirical analysis uses several volatility and return features.

The main variables are:

- monthly equity returns;
- monthly bond returns;
- realized variance;
- implied variance;
- raw Variance Risk Premium;
- log Variance Risk Premium.

---

## 3.1 Monthly returns

Monthly returns are computed from end-of-month prices.

For an asset with price \(P_t\), the monthly return is:

\[
r_t = \frac{P_t}{P_{t-1}} - 1
\]

where \(P_t\) is the end-of-month price.

The equity return is used both as a portfolio return input and as a feature in some regime models. The bond return is used as the defensive asset return in equity-bond allocation strategies.

---

## 3.2 Realized variance

Realized variance is estimated from daily equity returns within each month.

Let \(r_d\) be the daily equity return. Monthly realized variance is computed as:

\[
RV_t = 252 \sum_{d \in t} r_d^2
\]

where 252 is the standard annualization factor for daily returns.

This produces an annualized monthly realized variance estimate.

Realized variance is backward-looking. It measures the volatility that actually occurred during the month. It is therefore useful for describing realized market risk, but it does not directly measure expected future uncertainty.

---

## 3.3 Implied variance

Implied variance is derived from the volatility index.

For a volatility index \(VolIndex_t\), implied variance is computed as:

\[
IV_t = \left(\frac{VolIndex_t}{100}\right)^2
\]

The VIX is used for the US market and the VSTOXX is used for the European market.

Implied variance is forward-looking because it is extracted from option prices. It reflects the market price of future volatility risk under the risk-neutral measure.

---

## 3.4 Raw Variance Risk Premium proxy

The raw Variance Risk Premium proxy is defined as:

\[
VRP_t = IV_t - RV_t
\]

A positive value means that implied variance is higher than realized variance. This is consistent with the idea that investors pay a premium for volatility protection.

A negative value means that realized variance exceeds implied variance. This can happen during volatility shocks, market crashes or periods where realized volatility rises faster than implied volatility had anticipated.

The raw VRP proxy is simple and economically intuitive. However, it can be unstable because it is measured as an absolute difference between two variance quantities.

---

## 3.5 Log Variance Risk Premium proxy

The log VRP proxy is defined as:

\[
LogVRP_t = \log\left(\frac{IV_t}{RV_t}\right)
\]

This transformation measures the relative difference between implied and realized variance.

The log transformation has three advantages:

1. it reduces scale instability;
2. it makes the implied-realized variance spread relative rather than absolute;
3. it improves numerical behavior in some regime models.

The HMM RV + Log VRP specification is one of the most important models in the thesis because it provides the most defensible US implementable result.

---

## 4. Benchmark strategies

The empirical framework compares regime-based strategies against simple benchmark portfolios.

This is important because complex models should not be evaluated in isolation. A regime-switching model has economic value only if it improves performance relative to transparent and robust alternatives.

The benchmarks are:

1. Buy-and-Hold Equity;
2. 60/40 Equity-Bond;
3. 1/N Equity-Bond;
4. Synthetic Pure VRP Proxy.

---

## 4.1 Buy-and-Hold Equity

The buy-and-hold equity benchmark is fully invested in the equity index:

\[
w^{eq}_t = 1
\]

\[
w^{bond}_t = 0
\]

This benchmark captures the performance of passive equity exposure.

It is useful because it provides the highest direct exposure to the equity risk premium. However, it also usually has higher volatility and larger drawdowns than diversified equity-bond portfolios.

---

## 4.2 60/40 Equity-Bond portfolio

The 60/40 benchmark allocates 60% to equity and 40% to bonds:

\[
w^{eq}_t = 0.60
\]

\[
w^{bond}_t = 0.40
\]

This is a standard balanced portfolio benchmark. It is simple, widely used and difficult to beat in practice.

The 60/40 benchmark is important because a dynamic allocation model should improve either return, risk-adjusted performance or drawdown relative to this simple allocation.

---

## 4.3 1/N Equity-Bond portfolio

The 1/N benchmark allocates equally between equity and bonds:

\[
w^{eq}_t = 0.50
\]

\[
w^{bond}_t = 0.50
\]

This benchmark is intentionally simple. It is used because naive diversification is often difficult to outperform out of sample.

In this thesis, the 1/N portfolio is particularly important because it performs strongly in the US sample and remains competitive relative to more complex regime-switching strategies.

---

## 4.4 Synthetic Pure VRP Proxy

The Synthetic Pure VRP Proxy is designed to test whether direct exposure to the VRP signal produces economic value.

However, this strategy must be interpreted cautiously. It is not a true variance swap strategy. A true variance swap strategy would require:

- variance swap prices;
- maturity matching;
- contract rolling;
- option replication;
- transaction costs;
- bid-ask spreads;
- liquidity assumptions;
- margin and collateral modelling;
- variance notional scaling.

The synthetic proxy is therefore used as an exploratory benchmark. It helps evaluate whether the VRP signal contains economic information, but it should not be interpreted as a fully tradable institutional strategy.

This distinction is central to the thesis.

---

## 5. Hidden Markov Model methodology

## 5.1 Purpose of the HMM

The Hidden Markov Model is used to estimate latent market regimes.

The model assumes that observed market variables are generated by an unobserved state process. The states are not directly observable, but they can be inferred from the data.

In this thesis, the HMM is used to estimate the probability that the market is in a stress regime.

The objective is not only to classify regimes ex post. The objective is to use estimated regime probabilities to adjust portfolio weights out of sample.

---

## 5.2 Two-regime structure

The HMM uses two regimes:

1. normal regime;
2. stress regime.

The normal regime corresponds to periods of lower volatility and more stable market conditions. The stress regime corresponds to periods of higher volatility, weaker returns or elevated market uncertainty.

The stress state is identified from the estimated model by comparing state characteristics. The state associated with higher realized variance or worse risk conditions is labelled as the stress state.

---

## 5.3 HMM feature specifications

Several HMM specifications are tested.

| Model | Features |
|---|---|
| HMM RV | equity return, log realized variance |
| HMM RV + Raw VRP | equity return, log realized variance, raw VRP |
| HMM RV + Log VRP | equity return, log realized variance, log VRP |
| HMM IV | equity return, log implied variance |
| HMM IV + Log VRP | equity return, log implied variance, log VRP |
| HMM RV + IV | equity return, log realized variance, log implied variance |
| HMM RV + IV + Log VRP | equity return, log realized variance, log implied variance, log VRP |

The purpose of this specification grid is to test whether adding VRP-related information improves the economic value of regime-based allocation.

---

## 5.4 HMM allocation rule

Once the HMM estimates the stress probability, the portfolio weight is adjusted dynamically.

The equity weight is defined as:

\[
w^{eq}_t = 0.80(1 - p^{stress}_t) + 0.20p^{stress}_t
\]

where \(p^{stress}_t\) is the estimated probability of the stress regime.

This allocation rule implies:

- if \(p^{stress}_t = 0\), the equity weight is 80%;
- if \(p^{stress}_t = 1\), the equity weight is 20%;
- if \(p^{stress}_t\) is between 0 and 1, the equity weight is adjusted continuously.

The bond weight is:

\[
w^{bond}_t = 1 - w^{eq}_t
\]

This rule gives the strategy a defensive structure. Equity exposure decreases when the model identifies higher market stress.

---

## 6. Markov-switching regression methodology

## 6.1 Purpose of the RSM

The Markov-switching regression model is used as a second regime-based framework.

While the HMM detects latent states from a multivariate feature distribution, the RSM models return dynamics directly with regime-dependent parameters.

This allows the thesis to test whether the conclusions are specific to HMMs or whether similar results appear in a different regime-switching framework.

---

## 6.2 RSM specifications

The tested RSM specifications are:

| Model | Features |
|---|---|
| RSM Returns Only | no exogenous feature |
| RSM RV | log realized variance |
| RSM RV + Raw VRP | log realized variance, raw VRP |
| RSM RV + Log VRP | log realized variance, log VRP |

The RSM Returns Only model provides a baseline regime-switching model without volatility or VRP features.

The RSM RV model tests whether realized variance alone improves regime allocation.

The RSM RV + Raw VRP and RSM RV + Log VRP models test whether VRP adds economic value beyond realized variance.

---

## 6.3 RSM allocation rule

The RSM also produces a stress probability. The portfolio allocation rule is the same defensive equity-bond rule used for the HMM:

\[
w^{eq}_t = 0.80(1 - p^{stress}_t) + 0.20p^{stress}_t
\]

\[
w^{bond}_t = 1 - w^{eq}_t
\]

Using the same allocation rule for HMM and RSM makes the model comparison cleaner. Differences in performance then come from regime estimation rather than from different allocation mechanics.

---

## 7. Rolling out-of-sample design

## 7.1 Motivation

The empirical strategy uses a rolling out-of-sample backtest.

This is necessary to avoid look-ahead bias. A model should only use information that would have been available at the time of the investment decision.

A full-sample regime classification may be useful for description, but it is not sufficient for testing whether a strategy could have been implemented in real time.

---

## 7.2 Rolling estimation window

The main rolling estimation window is 72 months.

At each monthly date:

1. the model is estimated using the previous 72 months of data;
2. the regime probability is computed;
3. the portfolio weight for the next month is determined;
4. the next-month portfolio return is recorded;
5. the window rolls forward by one month.

This produces an out-of-sample sequence of strategy returns.

The 72-month window is a compromise. It is long enough to estimate regime models with some stability, but short enough to allow the model to adapt to changing market conditions.

---

## 7.3 Sample alignment

Because HMM and RSM models require a 72-month estimation window, the final model-comparison sample is shorter than the full monthly dataset.

In the current implementation:

| Market | Monthly observations before rolling alignment | Final aligned out-of-sample observations |
|---|---:|---:|
| US | 257 | 184 |
| Europe | 200 | 127 |

This alignment is essential for fair comparison. All models in the final comparison are evaluated over the same out-of-sample period within each market.

---

## 8. Transaction costs and turnover

## 8.1 Turnover

Turnover measures the amount of portfolio reallocation required by a strategy.

For a two-asset equity-bond portfolio, turnover is computed as the absolute change in portfolio weights:

\[
Turnover_t = \sum_i |w_{i,t} - w_{i,t-1}|
\]

High turnover is undesirable because it increases transaction costs and implementation complexity.

Turnover is particularly important for regime-switching models because regime probabilities can change frequently, causing the model to rebalance often.

---

## 8.2 Transaction cost adjustment

Strategy returns are adjusted for transaction costs using:

\[
r^{net}_t = r^{gross}_t - c \times Turnover_t
\]

where \(c\) is the transaction cost rate.

The baseline transaction cost is 10 basis points.

Robustness tests also examine the following transaction-cost levels:

\[
0,\ 5,\ 10,\ 25,\ 50 \text{ bps}
\]

This makes it possible to evaluate whether the performance of a strategy survives realistic implementation frictions.

---

## 9. Turnover-control mechanisms

The thesis tests two methods for reducing turnover:

1. no-trade bands;
2. partial rebalancing.

These mechanisms are important because a model may look attractive before costs but become unattractive after implementation frictions.

---

## 9.1 No-trade bands

A no-trade band prevents rebalancing when the difference between the current weight and the target weight is small.

The tested no-trade bands are:

\[
0\%,\ 2\%,\ 5\%,\ 10\%
\]

The intuition is that small allocation changes may not be worth implementing if they generate transaction costs without materially improving performance.

---

## 9.2 Partial rebalancing

Partial rebalancing moves the portfolio only partially toward the target weight.

The final portfolio weight is defined as:

\[
w_t^{final} = \lambda w_t^{target} + (1-\lambda) w_{t-1}^{portfolio}
\]

where \(\lambda\) is the adjustment speed.

The tested adjustment speeds are:

\[
0.10,\ 0.25,\ 0.50,\ 0.75,\ 1.00
\]

A value of \(\lambda = 1.00\) corresponds to full rebalancing. A value of \(\lambda = 0.25\) means that only 25% of the distance between the current weight and the target weight is closed at each rebalance.

This mechanism is especially important in the US results. The HMM RV + Log VRP model with partial rebalancing speed 0.25 is selected as the most defensible implementable specification because it reduces turnover while preserving competitive risk-adjusted performance.

---

## 10. Performance metrics

The strategies are evaluated using several metrics.

| Metric | Interpretation |
|---|---|
| Annualized return | Average yearly return |
| Annualized volatility | Yearly volatility of returns |
| Sharpe ratio | Return per unit of total volatility |
| Sortino ratio | Return per unit of downside volatility |
| Maximum drawdown | Largest peak-to-trough loss |
| Calmar ratio | Annualized return divided by maximum drawdown |
| VaR 95 | Historical 5% loss threshold |
| CVaR 95 | Average loss conditional on being below VaR |
| Average turnover | Average monthly reallocation |
| Observations | Number of out-of-sample monthly observations |

The thesis gives particular attention to downside metrics because the expected value of regime-switching allocation is not necessarily higher average return. A regime model may be valuable if it reduces drawdowns, tail losses or crisis-period exposure.

---

## 11. Crisis-period analysis

The thesis also evaluates strategies during crisis periods.

The crisis windows include:

- Eurozone Crisis;
- Covid Crisis;
- Inflation / Rate Shock;
- Volmageddon and late-cycle period;
- full aligned sample.

The objective is to assess whether VRP-based regime models add value specifically when market conditions deteriorate.

This is important because a defensive regime model should be judged not only by average performance but also by its behavior during stress events.

---

## 12. Cross-market comparison

The same broad methodology is applied to the US and European markets. This allows the thesis to test whether VRP-based allocation is robust across regions.

The cross-market comparison is essential because it separates two possible conclusions.

If the VRP signal works in both the US and Europe, then it may be interpreted as a robust allocation signal.

If it works only in one market, then its economic value is conditional and market-dependent.

The empirical results support the second interpretation. VRP-enhanced HMM models are useful in the US mainly for downside-risk management, but the same logic does not transfer robustly to Europe.

---

## 13. Methodological contribution

The methodology contributes to the thesis in four ways.

First, it compares direct synthetic VRP exposure with VRP as a regime signal.

Second, it evaluates complex regime-switching models against simple benchmarks such as 60/40 and 1/N.

Third, it uses rolling out-of-sample testing to reduce look-ahead bias.

Fourth, it includes implementation frictions through transaction costs, turnover, no-trade bands and partial rebalancing.

This makes the empirical framework more realistic than a simple in-sample signal test.

---

## 14. Chapter conclusion

This chapter presented the data and methodology used in the thesis.

The empirical framework is built around the construction of realized variance, implied variance and Variance Risk Premium proxies. These features are used in HMM and RSM regime-switching models to estimate market stress probabilities. The resulting regime probabilities are transformed into dynamic equity-bond allocations.

The models are evaluated out of sample and compared with simple benchmarks. Transaction costs, turnover, partial rebalancing and crisis-period performance are included to assess whether the strategies are economically realistic.

The next chapter presents the empirical results and evaluates whether the Variance Risk Premium creates more value as a direct synthetic exposure or as a regime-detection signal.