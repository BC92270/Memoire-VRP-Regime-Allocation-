# Chapter 5 — Limitations and Conclusion Draft

## 1. Introduction

This final chapter discusses the limitations of the thesis and summarizes the main empirical conclusions.

The thesis studied the following research question:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The empirical answer is conditional. The Variance Risk Premium does not appear to be a universally robust standalone return engine. The synthetic pure VRP proxy performs extremely well in the US sample but collapses in the European sample. This cross-market instability makes it difficult to defend direct VRP exposure as a universal allocation strategy.

The evidence is more defensible when VRP is used as an informational signal inside a regime-detection framework. In the US, the HMM RV + Log VRP model improves maximum drawdown relative to traditional benchmarks and remains competitive in Sharpe ratio. Once partial rebalancing is added, the model becomes more implementable because turnover is materially reduced.

The European results are weaker. In Europe, HMM and RSM models do not outperform simple benchmarks such as Buy-and-Hold Equity, 60/40 or 1/N Equity-Bond allocation. This shows that the economic value of VRP-based allocation is market-dependent.

The final conclusion is therefore:

> The Variance Risk Premium appears more useful as a conditional regime-state variable for downside-risk management than as a universally robust standalone return engine. However, its economic value depends on market structure, model specification, feature transformation and implementation frictions.

---

## 2. Data limitations

### 2.1 US and European data comparability

A first limitation concerns data availability and comparability across markets.

The US dataset is more robust because the main variables are liquid, accessible and widely used. SPY, VIX and AGG provide clear proxies for the US equity market, implied volatility and bond exposure.

The European dataset is more complex. The equity proxy is based on the EURO STOXX 50, the implied-volatility proxy is based on VSTOXX / V2TX, and the bond proxy is IEAG.AS. The European volatility series required manual reconstruction.

This creates a comparability issue. The US volatility proxy is cleaner and more directly available, while the European volatility proxy depends on a merged local file. Therefore, part of the weaker European result may be related to differences in data construction.

This does not invalidate the empirical results, but it requires caution when interpreting the cross-market comparison.

### 2.2 VSTOXX reconstruction

The European VSTOXX series was reconstructed from two sources:

1. official STOXX historical data up to 2016;
2. MarketWatch V2TX data from 2017 to 2026.

These two sources were merged into the local file:

`data/raw/vstoxx.csv`

This reconstruction made it possible to extend the European sample. However, it introduces several limitations.

First, the two sources may not use exactly the same timestamp convention. Second, there may be differences between official index values and secondary-source data. Third, the transition between the two sources may create small discontinuities. Fourth, the European sample remains shorter than the US sample after rolling-window alignment.

The final European out-of-sample sample contains 127 observations, compared with 184 observations for the US. This means that European model estimates are based on a shorter and potentially less stable sample.

### 2.3 Monthly frequency

The empirical analysis is conducted at monthly frequency.

This choice is appropriate for strategic allocation because monthly rebalancing reduces noise, turnover and transaction costs. However, it may miss short-lived volatility shocks. Some stress events appear and reverse within days or weeks. A monthly regime model may detect these events late or smooth them excessively.

Daily or weekly frequency could capture faster regime changes, but it would also increase turnover and implementation complexity. Monthly frequency is therefore a reasonable compromise, but it may understate the short-term informational content of volatility variables.

---

## 3. Proxy limitations

### 3.1 Synthetic pure VRP proxy

The synthetic pure VRP proxy is one of the most important limitations of the thesis.

The proxy is used to evaluate whether direct VRP exposure contains economic value. However, it is not a true variance swap strategy.

A true variance swap strategy would require:

- observable variance swap rates;
- maturity-matched contracts;
- option-replication mechanics;
- contract rolling;
- bid-ask spreads;
- margin requirements;
- collateral assumptions;
- variance notional scaling;
- liquidity constraints.

The synthetic proxy does not include all these elements. It is therefore an approximation.

This is why the thesis treats the pure VRP proxy as an exploratory benchmark, not as a directly tradable strategy. The US pure VRP proxy produces very strong results, but those results cannot be interpreted as evidence that an investor could obtain the same performance in live variance-swap trading.

### 3.2 Implied variance proxy

The thesis uses volatility indices to proxy implied variance:

\[
IV_t = \left(\frac{VolIndex_t}{100}\right)^2
\]

This is practical and standard in empirical work, but it remains an approximation. A volatility index is not identical to a variance swap rate. It reflects a specific index methodology, maturity convention, interpolation process and option-market construction.

This limitation matters especially for the comparison between VIX and VSTOXX. The two indices are conceptually similar, but they are not identical in construction, market depth, liquidity or institutional usage.

### 3.3 Realized variance proxy

Realized variance is computed from daily returns:

\[
RV_t = 252 \sum_{d \in t} r_d^2
\]

This is a practical approximation. It may be affected by missing trading days, holidays, extreme daily observations, close-to-close price measurement, annualization assumptions and price-source differences.

More advanced realized-variance measures could use intraday data, realized kernels or jump-robust volatility estimators. These methods may improve precision, but they require more granular data. The thesis uses daily data because it is accessible and sufficient for the empirical objective.

---

## 4. Model limitations

### 4.1 Two-regime assumption

The HMM and RSM frameworks use a two-regime structure:

1. normal regime;
2. stress regime.

This creates a clear interpretation, but real markets may have more than two regimes. Markets may move through low-volatility bull markets, high-volatility bear markets, inflationary drawdowns, liquidity crises, recovery regimes and sideways high-uncertainty regimes.

A two-regime model simplifies this complexity. It may force different types of stress into one state. This is important because Covid, inflation shocks and volatility events have different dynamics. A single stress regime may not capture all crisis types equally well.

### 4.2 Regime-label instability

Regimes are not directly observable. They are inferred from the estimated model.

This creates regime-label uncertainty. A state that looks like a stress regime in one rolling window may not have exactly the same meaning in another window. The thesis identifies the stress state based on risk characteristics, such as higher volatility or weaker market conditions, but this remains an approximation.

Regime uncertainty is unavoidable in HMM and RSM frameworks.

### 4.3 Rolling-window sensitivity

The main rolling estimation window is 72 months.

This choice is defensible because it balances estimation stability and adaptability. However, it remains a modelling assumption. A shorter window would make the model more reactive but less stable. A longer window would make the model more stable but slower to adapt.

Future research could test several rolling windows, such as 48, 60, 72, 96 and 120 months. This would allow a more complete evaluation of window sensitivity.

### 4.4 Feature sensitivity

The results depend on the selected features.

The HMM specifications include combinations of equity returns, realized variance, implied variance, raw VRP and log VRP. The RSM specifications include returns-only, realized variance, realized variance plus raw VRP and realized variance plus log VRP.

The US results suggest that HMM RV + Log VRP is the most defensible specification. However, this does not prove that it is the globally optimal feature set.

Future work could test additional variables, such as volatility term structure, credit spreads, interest-rate variables, liquidity indicators, macroeconomic variables, realized skewness, realized correlation and drawdown-based features.

---

## 5. Implementation limitations

### 5.1 Transaction costs

The thesis includes transaction-cost sensitivity from 0 to 50 basis points.

This is useful, but transaction costs remain simplified. In reality, transaction costs vary through time and across assets. They may increase during crisis periods, when liquidity becomes thinner and bid-ask spreads widen.

The current framework applies transaction costs mechanically through turnover. It does not model dynamic liquidity, market impact or crisis-time execution risk.

Therefore, the implementation analysis is more realistic than a frictionless backtest, but simpler than a full institutional execution model.

### 5.2 Turnover and rebalancing

The thesis analyzes turnover, no-trade bands and partial rebalancing.

Partial rebalancing improves implementability, especially for HMM RV + Log VRP in the US. The chosen adjustment speed of 0.25 reduces turnover materially while preserving competitive performance.

However, this value is selected from a finite grid. It is not necessarily optimal in a strict statistical sense. The result should therefore be interpreted as evidence that turnover control improves the model, not as proof that 0.25 is universally optimal.

### 5.3 Direct VRP implementation

Direct VRP exposure is harder to implement than equity-bond allocation.

The regime strategies allocate between equity and bonds with bounded weights. This is relatively realistic. By contrast, true variance exposure may involve derivatives, margin, collateral and nonlinear losses.

This is why the thesis avoids making strong claims about the direct tradability of the pure VRP proxy.

---

## 6. Statistical limitations

### 6.1 Backtest-based evidence

The thesis is based on historical backtests.

Backtests are useful for evaluating historical performance, but they do not prove future profitability. The rolling out-of-sample design reduces look-ahead bias, but it does not eliminate all forms of data-mining risk.

Model selection, feature selection and rebalancing-rule selection may still be influenced by the observed sample.

### 6.2 Lack of formal Sharpe-ratio tests

The thesis compares Sharpe ratios, drawdowns and other performance metrics. However, it does not include formal statistical tests of Sharpe-ratio differences.

Future work could add:

- Jobson-Korkie tests;
- Memmel correction;
- bootstrap confidence intervals;
- White Reality Check;
- Superior Predictive Ability tests.

These tests would help evaluate whether observed performance differences are statistically significant or could be explained by sampling variability.

### 6.3 Multiple-testing risk

Several model specifications are tested. This creates multiple-testing risk. When many strategies are evaluated, some may appear attractive by chance.

The thesis mitigates this risk through economic interpretation, cross-market comparison and implementation robustness. However, future research could apply formal multiple-testing corrections.

This limitation reinforces the need for caution in interpreting the US HMM RV + Log VRP result. The result is promising and defensible, but not definitive proof of a universal allocation edge.

---

## 7. Cross-market limitations

### 7.1 US versus Europe

One of the main findings is the asymmetry between the US and Europe.

In the US, VRP-enhanced HMM models are competitive and improve drawdown. In Europe, the same logic does not transfer robustly.

This asymmetry may reflect real economic differences, including:

- different option-market depth;
- different volatility-index construction;
- different equity-market composition;
- different monetary-policy regimes;
- different crisis dynamics;
- different bond-market behavior;
- different sample length.

The thesis documents the asymmetry, but it does not fully identify the causal reason behind it.

### 7.2 Market structure

The economic value of VRP may depend heavily on market structure.

The US option market is deep, liquid and highly institutionalized. The VIX is globally followed and widely traded through derivatives and volatility products.

The European volatility market is also important, but it is less central globally than the VIX ecosystem. This difference may partly explain why the VRP signal appears more useful in the US than in Europe.

The thesis therefore suggests that VRP should not be interpreted as a universal factor independent of market structure.

---

## 8. Summary of empirical findings

### Finding 1 — US VRP-enhanced HMM models are useful for downside-risk control

In the US, the HMM RV + Log VRP specification improves maximum drawdown relative to traditional benchmarks.

The full-rebalancing version has a maximum drawdown of -16.67%, compared with -20.06% for 60/40, -19.10% for 1/N and -23.93% for Buy-and-Hold Equity.

This supports the idea that VRP can help identify defensive allocation regimes.

### Finding 2 — Partial rebalancing improves implementability

The full-rebalancing HMM RV + Log VRP model has high turnover.

Partial rebalancing with adjustment speed 0.25 reduces average turnover from 25.35% to 9.10%, while keeping the Sharpe ratio close to the full-rebalancing version.

This makes the partial-rebalancing model the most defensible US implementation.

### Finding 3 — European regime-switching results are weak

In Europe, HMM and RSM models fail to outperform simple benchmarks.

The HMM RV + Log VRP model has a Sharpe ratio of 0.1281, far below the benchmark Sharpe ratios. The RSM models perform better than the HMMs, but remain below traditional portfolios.

This means that the VRP regime signal does not transfer robustly to Europe in the tested specifications.

### Finding 4 — Direct synthetic VRP exposure is unstable across markets

The pure VRP proxy performs extremely well in the US but collapses in Europe.

In the US, the synthetic pure VRP proxy has a Sharpe ratio of 2.9144. In Europe, the pure VRP proxy has a Sharpe ratio of -2.8511.

This instability prevents a strong conclusion in favor of direct VRP exposure.

### Finding 5 — Simple benchmarks remain difficult to beat

The 60/40 and 1/N portfolios remain strong competitors.

This confirms the importance of benchmark discipline. A complex model must be compared against simple and robust allocation rules, not only against buy-and-hold equity.

The thesis shows that regime-switching models can improve specific risk dimensions, but they do not universally dominate simple benchmarks.

---

## 9. Answer to the research question

The research question was:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The empirical answer is:

> The Variance Risk Premium creates more defensible economic value as an informational regime-state variable than as a direct standalone proxy exposure. However, this result is conditional, market-dependent and sensitive to implementation assumptions.

Direct synthetic VRP exposure is not robust. It performs very well in the US but fails dramatically in Europe.

The signal-based approach is more defensible. In the US, VRP-enhanced HMM allocation improves downside-risk control. However, the European results show that this approach is not universal.

Therefore, the thesis does not claim that VRP is a universal allocation factor. It argues that VRP is best understood as a conditional market-state signal.

---

## 10. Final contribution

The thesis contributes to the literature by connecting the Variance Risk Premium literature with regime-based asset allocation.

Its contribution is not that VRP always improves portfolio performance.

Its contribution is more precise:

1. VRP can contain useful regime information.
2. This information can improve downside-risk management in the US.
3. Direct VRP proxy exposure is not robust across markets.
4. European evidence does not support universal transferability.
5. Implementation frictions materially affect the attractiveness of regime-switching models.
6. Simple benchmarks remain difficult to beat.

This leads to the final positioning:

> The Variance Risk Premium is best understood as a conditional market-state signal whose economic value depends on market structure, model specification and implementation frictions.

---

## 11. Future research

Future research could extend the thesis in several directions.

First, future work could use true variance swap data instead of volatility-index proxies. This would allow a more accurate evaluation of direct VRP trading.

Second, it could use option-implied variance constructed from option chains, rather than relying only on volatility indices.

Third, it could test additional markets, such as the UK, Japan or global equity indices.

Fourth, it could add formal statistical tests of performance differences.

Fifth, it could include more advanced regime models, such as time-varying transition probability models, Bayesian regime-switching models, multivariate HMMs with macro variables or machine-learning regime classifiers.

Sixth, it could improve implementation realism by modelling dynamic transaction costs, bid-ask spreads, market impact, liquidity stress, execution delay and margin constraints.

These extensions would allow a more complete assessment of VRP-based allocation.

---

## 12. Final conclusion

This thesis studied whether the Variance Risk Premium creates more economic value as a direct tradable premium or as an informational signal for regime-based allocation.

The empirical evidence does not support a universal direct VRP strategy. The synthetic pure VRP proxy performs extremely well in the US but collapses in Europe. This cross-market instability makes it unsuitable as a general standalone return engine.

The evidence is stronger for the signal-based interpretation. In the US, the HMM RV + Log VRP model improves maximum drawdown and remains competitive with traditional benchmarks. When partial rebalancing is applied, the strategy becomes more implementable because turnover falls substantially.

However, the European results show that the signal is not universal. HMM and RSM models do not outperform simple equity-bond benchmarks in Europe.

The final answer is therefore conditional:

> The Variance Risk Premium is more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine. Its economic value depends on market structure, model specification, feature transformation, turnover control and implementation frictions.

This conclusion is more realistic than claiming that VRP is always profitable or always useful. The evidence suggests that VRP has economic content, but that this content must be used carefully, tested across markets and evaluated against simple benchmarks.

The main lesson is that the value of the Variance Risk Premium is conditional, not universal.