# Model Limitations

## 1. Data limitations

The empirical results depend on the quality and consistency of volatility-index data.

For the US market, the VIX series is relatively stable, liquid, widely used in the literature, and easily accessible through standard financial data providers. This makes the US part of the empirical analysis more reliable from a data-quality perspective.

For the European market, the VSTOXX series required manual reconstruction. The final VSTOXX dataset combines:

1. official STOXX historical data up to 2016;
2. MarketWatch V2TX data from 2017 to 2026.

Although the merged series allows the European replication to be implemented over a longer sample, this reconstruction introduces potential limitations. Different sources may differ in terms of timestamp conventions, closing-price definitions, missing observations, index dissemination rules, or data-cleaning methodology.

Therefore, the European results should be interpreted with more caution than the US results.

---

## 2. Synthetic VRP proxy limitation

The synthetic pure VRP proxy should not be interpreted as a directly tradable variance swap strategy.

A true variance swap strategy would require:

- variance swap prices or option-implied variance replication;
- correct treatment of contract maturity;
- rolling contract mechanics;
- option transaction costs;
- liquidity and bid-ask spreads;
- margin and collateral assumptions;
- variance notional scaling;
- treatment of jumps and convexity effects.

The proxy used in this thesis captures the difference between implied and realized variance, but it does not replicate the exact payoff of a listed or OTC variance product.

This limitation is especially important because the synthetic VRP proxy performs extremely well in the US but collapses in Europe. This contrast suggests that the proxy is useful for exploratory analysis, but should not be treated as a fully implementable trading strategy.

The proxy is therefore used to assess the informational content of the variance premium rather than to claim direct tradability.

---

## 3. Market-transferability limitation

The US and European results differ sharply.

In the US, VRP-enhanced HMM models improve drawdown control and remain competitive with traditional benchmarks such as 60/40 and 1/N equity-bond allocation.

In Europe, HMM and RSM models fail to outperform simple benchmarks. The VRP signal does not transfer robustly to the European allocation problem under the tested specifications.

This means that the informational content of VRP is not directly transferable across markets. The effectiveness of VRP-based allocation may depend on:

- option-market depth;
- volatility-index construction;
- liquidity conditions;
- equity-index composition;
- sector concentration;
- macroeconomic regime;
- monetary-policy environment;
- investor demand for crash protection;
- institutional hedging flows;
- volatility risk supply and demand.

Therefore, the thesis cannot conclude that VRP is a universal allocation signal. The more defensible conclusion is that VRP can be useful in specific markets and under specific implementation assumptions.

---

## 4. Model-specification limitation

The analysis uses two-regime HMM and RSM models.

This choice is parsimonious and interpretable, but real financial markets may contain more than two regimes. For example, markets can experience:

- low-volatility expansion regimes;
- high-volatility correction regimes;
- inflation-shock regimes;
- liquidity-crisis regimes;
- policy-driven recovery regimes;
- volatility-compression regimes;
- recessionary bear-market regimes.

A two-regime structure may be too restrictive to capture all relevant market states.

Moreover, HMM and RSM models are sensitive to:

- feature selection;
- scaling and normalization;
- rolling-window length;
- covariance assumptions;
- convergence behavior;
- regime-label identification;
- sample period.

Therefore, the results should be interpreted as evidence from a specific regime-modelling framework, not as a definitive statement about all possible regime-switching models.

---

## 5. Rolling-window limitation

The rolling estimation window is set to 72 months.

This creates a trade-off:

- a longer window gives more stable parameter estimation;
- a shorter window adapts faster to regime changes.

A 72-month window is methodologically consistent across the US and European samples, but it may not be optimal for all regimes or all markets.

For example, a model trained on a long window may react slowly to a structural break, while a model trained on a short window may become unstable and overfit recent observations.

This limitation is particularly relevant for regime-switching models, because the estimated transition probabilities and state distributions can change materially when the training window is modified.

---

## 6. Turnover and implementation frictions

The results are sensitive to turnover and transaction costs.

In the US, the HMM RV + Log VRP full-rebalancing model improves drawdown but has relatively high turnover. Partial rebalancing reduces turnover and makes the strategy more realistic, but it also changes the drawdown and return profile.

In Europe, regime-switching models generate turnover without sufficient economic benefit. This suggests that implementation frictions can destroy the value of a weak signal.

The backtest includes simplified transaction costs, but a more realistic implementation would require:

- bid-ask spreads;
- market impact;
- financing costs;
- tax effects;
- ETF expense ratios;
- futures roll costs;
- option-market execution costs;
- borrow and collateral assumptions;
- rebalancing constraints.

Therefore, the strategy performance should be interpreted as a controlled backtest result rather than a fully executable institutional trading strategy.

---

## 7. Monthly-frequency limitation

The analysis is performed at monthly frequency.

This frequency is appropriate for strategic asset allocation, but it may miss faster volatility dynamics. VRP and implied volatility can change sharply within days, especially during market stress.

A monthly model may therefore be too slow to exploit some volatility signals, particularly during:

- sudden market crashes;
- volatility spikes;
- central-bank shocks;
- geopolitical shocks;
- liquidity events.

A higher-frequency extension could test weekly or daily rebalancing. However, this would also increase transaction costs, turnover, noise, and model instability.

The monthly frequency is therefore a conservative choice, but it may understate the short-term informational value of VRP.

---

## 8. Benchmark limitation

The benchmarks used in the thesis are intentionally simple:

- buy-and-hold equity;
- 60/40 equity-bond allocation;
- 1/N equity-bond allocation.

These benchmarks are transparent, robust, and difficult to beat. They allow the marginal value of VRP-based regime allocation to be evaluated clearly.

However, institutional allocators may also compare against more advanced benchmarks, such as:

- risk parity;
- volatility targeting;
- minimum-variance allocation;
- trend-following;
- tactical asset allocation;
- dynamic drawdown-control strategies;
- option-overlay strategies;
- managed-volatility portfolios.

The thesis focuses on simple benchmarks to maintain interpretability, but future work could compare VRP-based regime allocation against more sophisticated allocation frameworks.

---

## 9. Statistical-inference limitation

The empirical results are primarily evaluated through backtest performance metrics.

The current framework includes:

- annualized return;
- annualized volatility;
- Sharpe ratio;
- Sortino ratio;
- maximum drawdown;
- Calmar ratio;
- VaR;
- CVaR;
- turnover;
- crisis-period performance.

However, the thesis does not yet include a full statistical inference layer such as:

- bootstrap confidence intervals;
- Sharpe ratio difference tests;
- Jobson-Korkie tests;
- Ledoit-Wolf Sharpe comparisons;
- White Reality Check;
- Superior Predictive Ability tests;
- parameter-stability tests;
- regime-classification accuracy tests.

Therefore, the results should be interpreted as empirical evidence rather than definitive statistical proof of model superiority.

---

## 10. Overfitting and data-snooping limitation

The empirical design tests several model specifications:

- HMM RV;
- HMM RV + Raw VRP;
- HMM RV + Log VRP;
- HMM IV;
- HMM IV + Log VRP;
- HMM RV + IV;
- HMM RV + IV + Log VRP;
- RSM Returns Only;
- RSM RV;
- RSM RV + Raw VRP;
- RSM RV + Log VRP.

Testing multiple specifications creates a risk of model selection bias. A model that performs well in-sample or in a specific market may do so partly because of data mining.

The use of rolling out-of-sample backtests reduces this risk, but it does not eliminate it fully. Future research could apply formal multiple-testing corrections or out-of-sample validation on additional markets.

---

## 11. Interpretation of negative European results

The European results are not a failure of the project. They are an important empirical finding.

The fact that VRP-enhanced regime models work better in the US than in Europe suggests that the value of VRP is conditional. This strengthens the thesis because it avoids an overly simplistic conclusion.

The European results show that:

- VRP is not universally robust;
- simple benchmarks remain difficult to beat;
- market structure matters;
- volatility-index construction matters;
- implementation frictions matter;
- regime models can be statistically feasible but economically weak.

This negative replication is part of the contribution of the thesis.

---

## 12. Main limitation and final caution

The main limitation of the thesis is that the economic value of VRP depends heavily on:

- market;
- proxy construction;
- model specification;
- rebalancing assumptions;
- transaction costs;
- turnover control;
- data quality.

The thesis therefore avoids the overly strong conclusion that VRP is a universal return factor.

The more defensible conclusion is:

> VRP can be useful as a regime-state variable for downside-risk management, especially in the US, but its allocation value is conditional and not robustly transferable across markets.

This conclusion is more cautious, but also more credible.