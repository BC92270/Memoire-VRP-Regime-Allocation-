# Chapter 5 — Limitations, Discussion and Conclusion Draft

## 1. Introduction

This final chapter discusses the interpretation, limitations and contribution of the thesis and provides a direct answer to the research question.

The thesis investigated whether the Variance Risk Premium creates more economic value through:

1. its informational content for dynamic equity–bond allocation; or
2. a model-based direct variance-payoff approximation.

The empirical results demonstrate that these two channels are not equivalent.

Adding VRP variables to Hidden Markov Models, Markov-switching regressions and machine-learning classifiers produces model-dependent information but limited portfolio gains relative to simple benchmarks.

The direct variance-payoff evidence is stronger, but highly asymmetric across markets. In the United States, the selected High-VRP strategy improves selected risk-adjusted metrics without establishing statistically significant welfare dominance. In Europe, the positive-VRP strategy produces large and bootstrap-significant welfare gains within the tested model and sample.

The principal conclusion is therefore not that VRP is universally superior as either a signal or a standalone strategy.

The principal conclusion is:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested, the market in which it is measured and the implementation assumptions used to transform the underlying variance spread into portfolio returns.

This conclusion must be interpreted within the methodological boundaries of the thesis.

---

## 2. Final interpretation of the empirical evidence

### 2.1 Information and payoff are different economic objects

The same underlying variance variables are used in two distinct ways.

In the allocation layer, realized variance, implied variance and VRP-related transformations are explanatory features. Their purpose is to improve estimates of future stress probabilities.

The resulting investment payoff remains an equity–bond portfolio payoff.

In the direct-variance layer, lagged implied variance and subsequently observed realized variance define a variance-linked payoff:

\[
\widetilde{\Pi}^{short}_t
=
\frac{
IV_{t-1}-RV_t
}{
IV_{t-1}
}
\]

The resulting strategy return is produced by scaling this payoff with a lagged volatility estimate and a constrained notional.

A variable can therefore possess predictive information without generating an attractive equity–bond allocation.

Conversely, a variance-linked payoff can generate positive economic value even when the same variable adds little to an allocation model.

The thesis results demonstrate precisely this distinction.

---

### 2.2 Allocation evidence

The allocation evidence is modest in both markets.

In the United States:

- the strongest benchmark Sharpe ratio is 1.025 for 1/N Equity–Bond;
- the strongest HMM Sharpe ratio is 1.019 for HMM RV + Log VRP;
- the strongest RSM Sharpe ratio is 0.949 for RSM RV + Raw VRP;
- the strongest ML Sharpe ratio is 1.002 for ML Logistic Base.

HMM RV + Log VRP improves maximum drawdown to −16.67%, compared with −20.06% for 60/40 and −19.10% for 1/N.

However, its average turnover is 25.35%. Partial rebalancing reduces this value to 9.10%, but does not create benchmark dominance.

In Europe:

- Buy-and-Hold Equity has a Sharpe ratio of 0.313;
- 60/40 has a Sharpe ratio of 0.292;
- 1/N has a Sharpe ratio of 0.280;
- the strongest RSM reaches 0.281;
- the strongest HMM reaches 0.218;
- the strongest ML allocation reaches 0.274.

The European Random Forest with VRP contains incremental predictive information, but its economic and welfare performance remains statistically indistinguishable from simple benchmarks.

The appropriate allocation conclusion is:

> VRP-related variables contain conditional predictive information, but their inclusion in the tested HMM, RSM and machine-learning allocation models does not establish robust economic superiority over simple equity–bond portfolios.

---

### 2.3 Direct variance-payoff evidence

The direct-variance diagnostics reveal positive average carry and negative skewness in both markets.

| Market | Positive-payoff rate | Mean normalized payoff | Skewness | Worst normalized payoff |
|---|---:|---:|---:|---:|
| United States | 82.42% | 0.253 | −3.849 | −4.432 |
| Europe | 78.35% | 0.239 | −2.231 | −2.439 |

These distributions reflect the central economic structure of short variance.

The strategy earns frequent positive payoffs when implied variance exceeds subsequent realized variance, but remains exposed to infrequent and severe losses.

### United States

The selected United States strategy is Direct Short Variance 10% Vol with a High-VRP gate.

It produces:

- annualized return of 6.23%;
- annualized volatility of 7.17%;
- Sharpe ratio of 0.882;
- Sortino ratio of 1.218;
- maximum drawdown of −23.46%.

Its headline Sharpe ratio is slightly above those of the aligned 60/40 and 1/N portfolios.

However, at a risk-aversion coefficient of five:

- its mean–variance certainty equivalent is approximately 5.04%;
- its fee-equivalent difference is approximately −71 basis points relative to 60/40;
- its fee-equivalent difference is approximately −45 basis points relative to 1/N;
- both bootstrap confidence intervals contain zero.

The strategy therefore does not establish robust welfare dominance.

### Europe

The selected European strategy is Direct Short Variance 10% Vol with exposure restricted to months in which the lagged VRP is positive.

It produces:

- annualized return of 13.08%;
- annualized volatility of 9.70%;
- Sharpe ratio of 1.324;
- Sortino ratio of 1.891;
- maximum drawdown of −21.36%.

At a risk-aversion coefficient of five:

- its mean–variance certainty equivalent is approximately 10.49%;
- its CRRA certainty equivalent is approximately 10.67%;
- its fee-equivalent advantage is approximately 927 basis points relative to 60/40;
- its fee-equivalent advantage is approximately 899 basis points relative to 1/N.

The lower bootstrap confidence bounds remain positive against both benchmarks.

Within the tested framework, the European welfare advantage is therefore statistically significant.

---

## 3. Evaluation of the hypotheses

### 3.1 Hypothesis 1 — Positive variance carry with negative skewness

The first hypothesis predicted that implied variance would exceed subsequent realized variance in a majority of observations, producing frequent positive carry combined with severe downside risk.

This hypothesis is supported in both markets.

The short-variance payoff is positive in:

- 82.42% of United States observations;
- 78.35% of European observations.

Both normalized payoff distributions are negatively skewed and contain losses below −100% of the strike-normalized exposure.

The positive average carry must therefore not be interpreted independently of tail risk.

---

### 3.2 Hypothesis 2 — Limited allocation-model dominance

The second hypothesis predicted that VRP-related variables could improve stress identification or downside control without consistently dominating simple benchmarks.

This hypothesis is supported.

The strongest HMM, RSM and ML portfolios remain close to or below the strongest benchmarks in Sharpe ratio.

The United States HMM improves maximum drawdown, while the European Random Forest with VRP provides incremental prediction information.

Neither result establishes general allocation superiority.

---

### 3.3 Hypothesis 3 — Payoff-structure dependence

The third hypothesis predicted that the value of VRP would depend on the mechanism through which it is monetized.

This hypothesis receives the strongest support.

The inclusion of VRP as an allocation feature generates modest results, while the European direct variance-payoff approximation generates economically large and statistically significant welfare gains.

The underlying variable is similar, but the payoff mapping differs.

The result confirms that predictive relevance and investment value must be evaluated separately.

---

### 3.4 Hypothesis 4 — Cross-market heterogeneity

The fourth hypothesis predicted material differences between the United States and Europe.

This hypothesis is supported.

The selected United States direct strategy does not produce statistically significant welfare gains.

The selected European strategy produces positive lower confidence bounds against both benchmarks.

However, this cross-market heterogeneity must not be interpreted as proof that European variance carry is structurally superior in all periods.

The result may depend on:

- sample dates;
- volatility-index construction;
- option-market structure;
- crisis composition;
- source quality;
- equity and bond proxies;
- the approximation used to construct the payoff.

---

### 3.5 Hypothesis 5 — Importance of implementation constraints

The fifth hypothesis predicted that implementation controls would materially affect the results.

This hypothesis is supported.

For equity–bond allocation, partial rebalancing reduces HMM turnover from 25.35% to 9.10%.

For direct variance carry, the analysis demonstrates the importance of:

- monthly roll costs;
- long lagged-risk windows;
- notional constraints;
- entry filters;
- subperiod analysis;
- crisis exclusions;
- investor risk aversion.

The United States strategy becomes unstable under a short 12-month risk window, reaching a maximum drawdown above 50%.

The European result remains strong under the tested implementation variations, but its magnitude still depends on a stylized payoff framework.

---

## 4. Data limitations

### 4.1 Cross-market data comparability

The United States and European datasets are not perfectly comparable.

The United States uses:

- SPY or the S&P 500 as the equity proxy;
- VIX as the implied-volatility proxy;
- AGG as the bond proxy.

Europe uses:

- EURO STOXX 50 as the equity proxy;
- VSTOXX or V2TX as the implied-volatility proxy;
- IEAG.AS as the bond proxy.

These instruments differ in:

- market composition;
- currency exposure;
- duration;
- liquidity;
- index methodology;
- investor base;
- derivatives-market depth.

Differences in strategy results may therefore reflect both economic variation and proxy construction.

---

### 4.2 VSTOXX reconstruction

The European VSTOXX history is reconstructed from multiple source segments and stored locally.

The date parsing and long-gap problems identified during the empirical process were corrected.

ISO dates are now interpreted explicitly as year-month-day, and returns crossing calendar interruptions longer than seven days are invalidated.

These corrections materially improve the reliability of the European results.

Nevertheless, residual limitations remain.

Different source segments may contain:

- distinct timestamp conventions;
- rounding differences;
- source-specific revisions;
- methodology differences;
- discontinuities at the merge point.

The corrected European results are more reliable than the earlier estimates, but they are not equivalent to a single uninterrupted official institutional dataset.

---

### 4.3 Sample length

The principal allocation samples contain:

| Market | Monthly features | Allocation OOS | Direct-variance strategies |
|---|---:|---:|---:|
| United States | 257 | 184 | 232 |
| Europe | 195 | 122 | 170 |

The European allocation sample is particularly limited for estimating nonlinear and regime-dependent models.

A 122-month out-of-sample period contains only a small number of major market regimes.

This reduces statistical power and makes the results more sensitive to individual episodes.

The direct-variance samples are longer, but remain insufficient to observe a large number of independent volatility crises.

---

### 4.4 Monthly frequency

Monthly analysis is appropriate for strategic portfolio allocation, but it suppresses intramonth information.

A volatility shock can begin, peak and partially reverse within a single month.

A monthly model may:

- detect the event late;
- obscure the path of losses;
- understate turnover required within the month;
- ignore temporary liquidity needs;
- miss daily margin pressure.

The monthly design should therefore be interpreted as a strategic research framework rather than a high-frequency execution model.

---

## 5. Measurement limitations

### 5.1 Implied-variance proxy

The thesis approximates implied variance as:

\[
IV_t
=
\left(
\frac{V_t}{100}
\right)^2
\]

where \(V_t\) is VIX or VSTOXX.

This approximation is transparent and reproducible, but it is not identical to an investable variance-swap strike.

An exact strike would require:

- the full option surface;
- maturity interpolation;
- forward-price estimation;
- strike integration or summation;
- tail extrapolation;
- contract-specific conventions.

The volatility-index square is therefore best understood as a model-based strike proxy.

---

### 5.2 Realized-variance proxy

Realized variance is constructed as a trailing 21-observation annualized measure:

\[
RV_d
=
\frac{252}{21}
\sum_{j=0}^{20}
r_{d-j}^{2}
\]

It is sampled at month-end.

This measure does not reproduce exact contractual settlement over a fixed calendar interval.

It may also be affected by:

- close-to-close measurement;
- market holidays;
- asynchronous source dates;
- price corrections;
- overnight jumps;
- microstructure effects not visible in daily data.

Future work using intraday observations could construct realized kernels, jump-robust estimates or exact contract-matched realized variance.

---

### 5.3 Difference between physical and risk-neutral objects

Option-implied variance reflects risk-neutral pricing and compensation for volatility risk.

Realized variance is observed under the physical historical process.

The spread between the two quantities therefore combines several components:

- expected future variance;
- volatility-risk compensation;
- jump-risk compensation;
- model and measurement differences;
- volatility-index construction effects.

The empirical VRP proxy should not be interpreted as a pure structural risk premium without qualification.

---

### 5.4 Exploratory Pure VRP Proxy

The Pure VRP Proxy remains an exploratory transformation.

It does not impose:

- a forward contractual strike;
- a subsequent settlement date;
- notional scaling;
- a volatility target;
- monthly roll costs;
- derivative execution constraints.

Its high historical performance cannot be used as evidence of an available traded return.

It is retained only to illustrate the information contained in the implied-to-realized variance relationship.

---

## 6. Direct-payoff and capital-mapping limitations

### 6.1 Normalized payoff is not return on invested capital

The normalized payoff is:

\[
\frac{
IV_{t-1}-RV_t
}{
IV_{t-1}
}
\]

This quantity has no direct equivalence to the return on a fully specified capital account.

Variance swaps are typically expressed using variance notional and payoff conventions that differ from an initial cash investment.

The thesis converts the normalized payoff into a synthetic portfolio return through risk-targeted notional scaling.

This mapping is useful for comparing risk-adjusted performance, but it remains model dependent.

---

### 6.2 Ex ante target versus realized volatility

The strategy uses a lagged payoff-volatility estimate to target either 5% or 10% annual volatility.

The target is ex ante.

It does not guarantee ex post volatility.

The United States always-active 10% strategy realizes volatility above 16%, demonstrating that lagged standard deviation can severely underestimate future tail exposure.

This is a fundamental limitation of volatility targeting for negatively skewed strategies.

---

### 6.3 Monthly roll costs

The model applies transaction costs to the full absolute notional initiated each month.

This is more appropriate than charging only for the change in desired exposure.

However, the cost assumption remains stylized.

It does not reproduce:

- actual dealer quotations;
- option-replication spreads;
- crisis-time widening;
- transaction-size effects;
- financing charges;
- legal and documentation costs;
- counterparty valuation adjustments.

Robustness up to 50 basis points does not prove that all actual implementation costs would lie below that level.

---

### 6.4 Margin, collateral and liquidity

The framework does not model:

- initial margin;
- variation margin;
- collateral remuneration;
- liquidity buffers;
- forced deleveraging;
- intramonth margin calls;
- counterparty default;
- close-out costs.

These omissions are particularly important for short variance.

A strategy can finish a month with a manageable final payoff while experiencing a severe intramonth mark-to-market loss.

An investor may be forced to reduce or close the position before settlement.

The monthly return series cannot capture this path dependency.

---

## 7. Model limitations

### 7.1 Two-regime assumption

The HMM and RSM frameworks use two regimes:

1. normal;
2. stress.

This structure is parsimonious and interpretable, but it compresses several economically distinct environments into a single stress state.

Potentially distinct regimes include:

- deflationary equity crashes;
- inflationary equity–bond drawdowns;
- liquidity crises;
- volatility shocks without persistent recession;
- post-crisis recoveries;
- high-volatility expansions.

A two-state model may not differentiate these environments adequately.

---

### 7.2 Regime-label instability

Latent states are not directly observed.

The identity of the stress state can change across rolling estimation windows.

A state associated with high volatility in one window may represent a different combination of returns and variance in another.

The implementation identifies stress through the state’s estimated characteristics, but some label uncertainty remains unavoidable.

---

### 7.3 Rolling-window choice

The allocation models use a 72-month rolling estimation window.

This choice balances adaptability and statistical stability, but remains a modelling assumption.

A shorter window:

- responds faster;
- uses fewer observations;
- increases parameter uncertainty.

A longer window:

- improves estimation stability;
- may retain obsolete historical relationships;
- reacts more slowly to structural change.

A broader window analysis would strengthen the allocation-model robustness assessment.

---

### 7.4 Machine-learning label and threshold

The ML stress label is defined using the next equity return and next realized variance relative to rolling quantiles.

This definition is economically intuitive, but not unique.

Alternative labels could use:

- drawdown;
- volatility jumps;
- joint equity–bond losses;
- liquidity stress;
- credit spreads;
- recession indicators.

The classification threshold of 0.50 and the 80%–20% allocation mapping also influence the resulting portfolio.

ML performance therefore reflects both predictive quality and design choices governing how probabilities are converted into trades.

---

### 7.5 Model-selection risk

Several feature transformations, model families, filters and calibration values are evaluated.

This creates a risk that some results appear attractive through sample-specific selection.

The thesis mitigates this risk through:

- rolling out-of-sample estimation;
- benchmark comparison;
- cross-market analysis;
- common-sample sensitivity tests;
- subperiod analysis;
- bootstrap welfare inference.

These controls reduce but do not eliminate specification-search risk.

---

## 8. Statistical limitations

### 8.1 Historical backtest evidence

The thesis relies on historical backtests.

Rolling out-of-sample estimation reduces look-ahead bias, but historical performance does not prove future profitability.

Structural relationships may change because of:

- regulation;
- market participation;
- volatility-product development;
- monetary policy;
- dealer balance-sheet constraints;
- systematic volatility-selling strategies;
- crisis composition.

The observed European result may weaken or reverse in a future sample.

---

### 8.2 Limited number of tail events

The direct-variance payoff is strongly negatively skewed.

Its economic risk depends disproportionately on a small number of extreme observations.

Even a sample of 170 or 232 monthly strategy observations contains relatively few major volatility shocks.

Estimates of:

- maximum drawdown;
- CVaR;
- CRRA utility;
- optimal notional;
- tail-loss probability

are therefore subject to considerable uncertainty.

---

### 8.3 Bootstrap limitations

The welfare analysis uses:

- 2,000 block-bootstrap replications;
- six-month blocks;
- comparisons against 60/40 and 1/N.

The block structure preserves part of the serial dependence in returns.

However, the results can depend on:

- block length;
- bootstrap method;
- number of replications;
- treatment of structural breaks;
- finite-sample tail behavior.

Positive confidence bounds increase confidence in the European result, but do not establish a universal population parameter.

---

### 8.4 Multiple testing

The empirical framework evaluates several:

- HMM features;
- RSM features;
- ML algorithms;
- VRP transformations;
- variance-entry gates;
- risk windows;
- notional caps;
- cost levels;
- subperiods.

This creates multiple-testing risk.

The analysis does not apply a complete familywise correction such as a White Reality Check or a Superior Predictive Ability test across every specification.

The strongest result should therefore be interpreted as validated within the stated robustness design, not as immune to data-snooping concerns.

---

### 8.5 Certainty-equivalent assumptions

Mean–variance certainty equivalent assumes that investor preferences can be summarized by expected return and variance.

This approximation may be inadequate for strongly skewed short-variance payoffs.

The CRRA certainty equivalent addresses part of this limitation, but still depends on:

- a specific utility function;
- the chosen risk-aversion coefficient;
- monthly return aggregation;
- absence of intermediate liquidity constraints.

Welfare estimates should therefore complement, rather than replace, distributional and implementation analysis.

---

## 9. Cross-market interpretation limitations

### 9.1 Sample-specific asymmetry

The European direct-variance result is stronger than the United States result in the observed samples.

This should not be interpreted as proof that Europe offers a permanently larger or more exploitable variance premium.

The difference may reflect:

- sample start dates;
- the frequency and timing of crises;
- volatility-index methodologies;
- equity-market composition;
- monetary-policy regimes;
- source reconstruction;
- differences in realized-variance dynamics.

The thesis identifies cross-market heterogeneity but does not establish its causal origin.

---

### 9.2 Different evidence-layer samples

The allocation and direct-variance layers use different aligned samples.

Allocation results contain 184 United States observations and 122 European observations.

Direct-variance results contain 232 United States observations and 170 European observations.

A higher Sharpe ratio in the direct-variance layer cannot be attributed solely to payoff structure without acknowledging the difference in evaluation dates.

The thesis therefore avoids a mechanical pooled ranking across evidence layers.

---

### 9.3 External validity

Only two developed equity markets are examined.

The results cannot automatically be generalized to:

- the United Kingdom;
- Japan;
- emerging markets;
- individual equities;
- commodities;
- foreign exchange;
- interest-rate volatility.

Additional markets would be required to determine whether the European result represents a broader phenomenon or a region-specific historical outcome.

---

## 10. Principal empirical findings

Six principal findings emerge.

### Finding 1 — Positive carry is accompanied by severe tail risk

The short-variance payoff is positive in the majority of observations in both markets.

However, both distributions are negatively skewed and contain severe losses.

Average carry is therefore not sufficient to evaluate economic value.

### Finding 2 — Simple allocation benchmarks remain difficult to beat

The 60/40 and 1/N portfolios remain highly competitive.

Dynamic models can improve selected risk measures, but generally require substantially more turnover.

### Finding 3 — VRP information is model dependent

Raw and log VRP transformations do not produce uniform improvements.

The strongest US ML portfolio excludes VRP, whereas the strongest European ML portfolio includes it.

The value of the variable depends on the model family and transformation.

### Finding 4 — United States direct variance is not welfare dominant

The High-VRP strategy improves headline Sharpe and drawdown relative to aligned balanced benchmarks.

Its certainty-equivalent differences are not statistically positive.

The result is economically plausible but not dominant.

### Finding 5 — European direct variance is strong within the tested model

The positive-VRP strategy produces a Sharpe ratio of 1.324 and large welfare gains.

The result survives the tested costs, risk windows, notional caps, subperiods, crisis exclusions and risk-aversion levels.

### Finding 6 — Payoff structure is central

The most important finding is not a universal ranking of the United States and Europe.

It is that the economic value of VRP changes materially when it is transformed from an allocation feature into a variance-linked payoff.

---

## 11. Answer to the research question

The research question is:

> Does the Variance Risk Premium create more economic value through direct variance carry or through its informational content for dynamic asset allocation?

The empirical answer is conditional.

For equity–bond allocation, VRP-related variables contain useful but model-dependent information. They can improve stress classification and selected downside-risk measures, but they do not establish robust benchmark dominance.

For the United States direct-variance approximation, positive carry and improved headline risk-adjusted performance do not translate into statistically significant welfare superiority.

For the European direct-variance approximation, the positive-VRP strategy produces economically large and bootstrap-significant welfare gains within the tested sample.

The most defensible answer is therefore:

> The Variance Risk Premium does not possess a single market-independent form of economic value. In this thesis, its economic contribution depends more on the payoff structure through which it is harvested than on its mere inclusion as a state variable. The direct variance-payoff approximation generates substantially stronger evidence in Europe, while neither the allocation channel nor the direct-payoff channel establishes robust welfare dominance in the United States.

This answer is empirical rather than universal.

It applies to the tested data, markets, models and implementation assumptions.

---

## 12. Contribution of the thesis

The thesis makes five principal contributions.

### 12.1 Separation of information and payoff

The first contribution is conceptual.

The thesis separates VRP as an informational variable from VRP as the basis of a variance-linked payoff.

This prevents predictive content from being confused with investment profitability.

### 12.2 Cross-market evaluation

The second contribution is the comparison between the United States and Europe.

The results demonstrate that conclusions obtained in one market should not be transferred mechanically to another.

### 12.3 Strict temporal alignment

The third contribution is methodological.

The empirical pipeline uses:

- rolling out-of-sample estimation;
- one-step-ahead allocation;
- lagged implied variance;
- subsequent realized-variance settlement;
- strictly lagged risk estimation;
- lagged filter thresholds.

These choices reduce look-ahead bias.

### 12.4 Welfare and implementation analysis

The fourth contribution is economic.

Strategies are evaluated not only through Sharpe ratios but also through:

- downside risk;
- turnover;
- roll costs;
- certainty equivalents;
- bootstrap confidence intervals;
- notional constraints;
- subperiods;
- crisis exclusions.

### 12.5 Reproducible correction of European data

The fifth contribution is empirical reliability.

The European date-parsing and gap-contamination problems were identified, corrected and incorporated into a reproducible pipeline.

The corrected data materially change the interpretation of the European variance premium.

This demonstrates the importance of data auditing in quantitative research.

---

## 13. Research-question answer matrix

The thesis is ultimately judged by whether the empirical design answers the questions stated in the proposal. The following matrix links each question to the corresponding evidence and conclusion.

| Research question | Main evidence | Answer | Interpretation for the thesis |
|---|---|---|---|
| Do regime-based methods improve equity-index allocation when VRP is available? | HMM, RSM and ML strategies are feasible and sometimes improve drawdown or classification metrics, but they do not establish robust Sharpe or welfare dominance over simple benchmarks. | Partially, but not robustly. | VRP is informative in some specifications, yet informational content is not sufficient to guarantee economic value after turnover and benchmark discipline. |
| Do traditional benchmarks remain difficult to beat? | 60/40 and 1/N remain competitive, especially in risk-adjusted and welfare comparisons. | Yes. | This is consistent with benchmark-discipline arguments in the portfolio-choice literature and prevents overclaiming model value. |
| Is VRP more valuable when traded directly or used as a state variable? | The direct-variance approximation is much stronger in Europe, while allocation gains are limited; in the United States, neither channel establishes robust welfare dominance. | The answer is market- and payoff-dependent. | The thesis should not claim a universal best use of VRP; it should claim that the payoff mechanism dominates the signal-only interpretation in the tested European sample. |
| Does the project identify an implementable variance-swap strategy? | The direct-variance layer uses lagged implied variance, realized-variance settlement proxies, notional caps and roll costs, but not actual option-surface replication or dealer quotes. | No. | The result is an economically informative approximation, not a verified executable derivative strategy. |
| What is the safest final conclusion? | Allocation evidence is modest; European direct-variance evidence is strong but approximate; US direct-variance welfare dominance is not established. | VRP has conditional economic value. | The strongest contribution is the separation between informational and payoff channels, not a claim that one model always beats benchmarks. |

This matrix also clarifies why the thesis deliberately avoids a simple positive conclusion. A high-grade interpretation is not that every sophisticated method improves performance, but that the empirical evidence identifies where the economic value of VRP survives benchmark, welfare and implementation discipline.

---

## 14. Implications for investors and researchers

### 14.1 Implications for allocation investors

Investors should not assume that adding a sophisticated regime model will automatically improve a balanced portfolio.

Simple benchmarks remain difficult to outperform after turnover.

Regime models may nevertheless have value when the objective prioritizes:

- maximum-drawdown reduction;
- smoother exposure changes;
- explicit stress probabilities;
- defensive overlays.

Partial rebalancing is more effective than simple no-trade bands in reducing turnover for the selected US HMM.

---

### 14.2 Implications for volatility investors

Positive average variance carry should never be evaluated without:

- tail-loss measurement;
- notional scaling;
- margin analysis;
- collateral requirements;
- crisis liquidity;
- settlement conventions.

The strong European result warrants further investigation, but not immediate interpretation as a directly tradable return.

An institutional implementation would require a complete derivative-pricing and execution layer.

---

### 14.3 Implications for empirical research

The results show that data quality can reverse an empirical conclusion.

The original European interpretation was driven by a date-parsing error that severely reduced the usable VSTOXX sample.

Quantitative research should therefore include explicit tests for:

- date formats;
- duplicate observations;
- missing periods;
- calendar gaps;
- alignment across assets;
- feature identities;
- look-ahead bias;
- common-sample comparability.

---

## 15. Future research

Several extensions would materially strengthen the analysis. The most useful extensions are not additional black-box models, but improvements that follow directly from the literature reviewed in the thesis. Carr and Wu (2009) motivate exact variance-swap replication from option portfolios; Bollerslev, Tauchen and Zhou (2009) motivate treating VRP as a predictive variable whose statistical content must be converted into economic value; Ang and Bekaert (2002) and Guidolin and Timmermann (2007) motivate richer regime structures and out-of-sample asset-allocation discipline; DeMiguel, Garlappi and Uppal (2009) motivate strict comparison with transparent benchmark portfolios.

This literature implies that the most valuable next steps are: first, improve the measurement of the variance payoff; second, validate the result outside the selected sample; third, test whether richer regimes improve allocation after turnover; and fourth, apply stronger multiple-model inference before claiming superiority.

### 15.1 Exact variance-swap replication

Future work should construct fair variance strikes from option chains using the appropriate replication formula.

This would replace the volatility-index-square approximation with contract-matched forward variance.

### 15.2 Observed derivative data

Institutional variance-swap quotes or proprietary dealer data would allow:

- observed bid–ask spreads;
- exact maturities;
- contract rolls;
- collateral assumptions;
- executable notional conventions.

### 15.3 Option-based replication

A complementary approach could backtest delta-hedged option portfolios designed to approximate variance exposure.

This would permit direct measurement of:

- option transaction costs;
- hedge rebalancing;
- discrete-strike effects;
- tail truncation;
- volatility-surface dynamics.

### 15.4 Higher-frequency realized variance

Intraday data could support:

- realized kernels;
- bipower variation;
- jump decomposition;
- overnight-return treatment;
- more accurate settlement matching.

### 15.5 External validation

The models should be tested on:

- the United Kingdom;
- Japan;
- global developed markets;
- alternative European indices;
- later holdout periods not used for any model selection.

### 15.6 Stronger statistical corrections

Future work could add:

- White Reality Check;
- Hansen Superior Predictive Ability test;
- false-discovery-rate control;
- model-confidence sets;
- bootstrap Sharpe-difference tests;
- nested forecast-comparison procedures.

### 15.7 Dynamic transaction and margin costs

A more realistic implementation model could link costs and margin requirements to:

- volatility level;
- market stress;
- trade size;
- dealer balance-sheet conditions;
- liquidity indicators.

### 15.8 Alternative allocation mappings

Future work could test nonlinear mappings from stress probability to portfolio weights, including:

- threshold allocation;
- volatility scaling;
- expected-utility optimization;
- constrained mean–CVaR allocation;
- probability calibration before weight conversion.

---

## 16. Final conclusion

This thesis studied whether the Variance Risk Premium creates greater economic value as an informational input for dynamic equity–bond allocation or through a model-based direct variance-payoff approximation.

The allocation evidence is disciplined but modest.

Hidden Markov Models, Markov-switching regressions and machine-learning classifiers produce feasible dynamic portfolios and occasionally improve selected downside-risk measures. They do not consistently outperform simple benchmarks after turnover and implementation costs.

The direct-variance evidence reveals a different economic mechanism.

Both markets exhibit frequent positive carry and severe negative skewness.

In the United States, a High-VRP filter improves the strategy profile, but welfare superiority is not statistically established.

In Europe, the positive-VRP strategy generates strong risk-adjusted returns and bootstrap-significant certainty-equivalent gains. Its performance remains robust across the tested transaction costs, risk windows, notional caps, subperiods, crisis exclusions and levels of risk aversion.

Nevertheless, the European strategy remains an approximation.

It does not reconstruct an exact variance-swap strike, contractual variance notional, collateral account, margin path, bid–ask spread or daily mark-to-market process.

The final conclusion is therefore deliberately precise:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested. In the tested European sample, a model-based direct variance-payoff approximation produces substantial and robust economic value, whereas the inclusion of VRP as a state variable in dynamic equity–bond allocation produces only limited gains. In the United States, neither channel establishes robust investor-welfare dominance over traditional portfolios.

This conclusion does not identify a universal trading strategy.

It identifies a methodological principle: the economic value of a financial signal cannot be separated from the payoff, risk controls and implementation mechanism used to monetize it.
