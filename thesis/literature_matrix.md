# Literature Matrix

This matrix links the main references to the role they play in the thesis design, interpretation and possible extensions. It is intended as an examiner-facing map rather than a substitute for the literature review.

| Reference | Core idea used in the thesis | How it supports the empirical design | Implication for interpretation or future work |
|---|---|---|---|
| Bakshi and Kapadia (2003) | Option returns contain compensation for volatility risk. | Motivates the economic intuition that selling volatility/variance protection may earn a premium while retaining crash exposure. | Direct VRP evidence must always be interpreted together with tail-loss and implementation-risk measures. |
| Carr and Wu (2009) | Variance risk premia are best measured using synthetic variance-swap rates from option portfolios. | Provides the theoretical benchmark for treating VRP as a variance-linked payoff rather than only a forecasting variable. | The thesis approximation should be presented as a first-pass payoff mapping; a higher-grade extension would reconstruct option-implied variance-swap strikes. |
| Bollerslev, Tauchen and Zhou (2009) | VRP contains predictive information about expected stock returns. | Supports testing VRP as an informational state variable in HMM, RSM and ML allocation models. | Statistical predictability is not sufficient; the thesis must test whether it translates into portfolio and welfare gains. |
| Hamilton (1989) | Regime switching can model unobserved changes in time-series dynamics. | Provides the econometric foundation for latent market regimes and Markov-switching specifications. | Regime labels must be interpreted economically and evaluated out of sample. |
| Ang and Bekaert (2002) | Asset returns, volatilities and correlations can shift across regimes, affecting allocation. | Supports the thesis choice to evaluate dynamic allocation rather than static forecasting only. | Cross-market validation is important because regime dynamics can differ between regions. |
| Guidolin and Timmermann (2007) | Multiple regimes can materially affect optimal stock-bond allocations. | Motivates comparing HMM/RSM state probabilities with portfolio weights and investor welfare. | Future work could test richer multi-state models, but only if they survive turnover and sample-size discipline. |
| DeMiguel, Garlappi and Uppal (2009) | Naive 1/N diversification is difficult to beat out of sample once estimation error and turnover are considered. | Justifies the strict use of 1/N, 60/40 and buy-and-hold as benchmarks. | The thesis should not claim model superiority unless it beats simple portfolios on aligned samples and welfare metrics. |

## Literature-informed optimisation priorities

1. Replace the volatility-index-square approximation with option-replicated variance-swap strikes when option-chain data are available.
2. Re-run all empirical outputs under the final dated cutoff before submission to avoid stale generated artifacts.
3. Add external validation on other markets or later holdout samples before generalising the European direct-variance result.
4. Test richer regime structures only after confirming that the existing two-state and selected RSM specifications are not already constrained by sample size.
5. Use stronger multiple-model inference, such as model-confidence sets or superior predictive ability tests, before claiming that any strategy dominates the benchmark universe.
