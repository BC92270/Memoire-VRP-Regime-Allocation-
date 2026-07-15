# Memoire-VRP-Regime-Allocation

Master thesis research project on the Variance Risk Premium, regime-based allocation, Hidden Markov Models, Markov-switching regression models, and portfolio performance across US and European equity markets.

## 1. Research question

The central research question is:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The project compares direct synthetic VRP exposure with regime-based allocation models using the VRP as an informational state variable.

## 2. Empirical contribution

The thesis connects two strands of literature:

1. Variance Risk Premium and volatility-risk premia.
2. Regime-switching asset allocation.

The main empirical result is conditional:

> The Variance Risk Premium appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine.

The result is asymmetric across markets:

- In the US, VRP-enhanced HMM models are competitive with traditional benchmarks and improve maximum drawdown.
- In Europe, regime-switching models do not outperform simple benchmarks.
- The synthetic pure VRP proxy performs very strongly in the US but collapses in Europe.
- Simple equity-bond benchmarks remain difficult to beat.

## 3. Markets and data

### US market

The US market is represented by:

- Equity proxy: SPY / S&P 500
- Implied-volatility proxy: VIX
- Bond proxy: AGG

### European market

The European market is represented by:

- Equity proxy: EURO STOXX 50
- Implied-volatility proxy: VSTOXX / V2TX
- Bond proxy: IEAG.AS

The VSTOXX series is reconstructed from official STOXX historical data and MarketWatch V2TX data, then merged into:

    data/raw/vstoxx.csv

## 4. Methodology

The empirical framework includes:

- realized variance construction;
- implied variance construction;
- synthetic VRP proxy construction;
- traditional benchmark portfolios;
- Hidden Markov Models;
- Markov-switching regression models;
- rolling out-of-sample estimation;
- transaction-cost sensitivity;
- no-trade band sensitivity;
- partial rebalancing;
- crisis-period performance analysis;
- cross-market comparison.

## 5. Benchmark strategies

The benchmark strategies are:

- Buy-and-Hold Equity
- 60/40 Equity-Bond portfolio
- 1/N Equity-Bond portfolio
- Synthetic Pure VRP Proxy

## 6. Regime-based models

The main regime-based strategies are:

- HMM RV
- HMM RV + Raw VRP
- HMM RV + Log VRP
- HMM IV
- HMM IV + Log VRP
- HMM RV + IV
- HMM RV + IV + Log VRP
- RSM Returns Only
- RSM RV
- RSM RV + Raw VRP
- RSM RV + Log VRP

## 7. Main empirical findings

### US evidence

In the US sample, VRP-enhanced HMM models are competitive with 60/40 and 1/N benchmarks.

The most defensible implementable specification is:

    HMM RV + Log VRP with partial rebalancing

This specification improves downside-risk management while reducing turnover relative to full rebalancing.

### European evidence

In the European sample, regime-switching models do not outperform simple benchmarks.

The VRP signal does not transfer robustly to European allocation in the tested specifications.

### Pure VRP proxy

The synthetic pure VRP proxy is very strong in the US but fails in Europe.

It should therefore be treated as an exploratory proxy rather than as a fully tradable variance-swap strategy.

## 8. Repository structure

    data/
      raw/
        vstoxx.csv
      processed/

    outputs/
      charts/
      logs/
      models/
      tables/

    src/
      backtest_engine.py
      benchmarks.py
      config.py
      data_loader.py
      features_vrp.py
      hmm_models.py
      performance_metrics.py
      plots.py
      robustness.py
      rsm_models.py

    thesis/
      abstract_keywords.md
      introduction_draft.md
      chapter_1_literature_review_draft.md
      chapter_2_data_methodology_draft.md
      chapter_3_empirical_results_draft.md
      chapter_4_robustness_implementation_draft.md
      chapter_5_limitations_conclusion_draft.md
      full_thesis_clean.md
      final_thesis_package.md
      empirical_results.md
      methodology_pipeline.md
      literature_positioning.md
      model_limitations.md
      thesis_structure.md

## 9. Main scripts

### Data and benchmark pipeline

    python main_mvp1.py

Runs the baseline data pipeline for the US and European markets, builds realized variance, implied variance, VRP proxies, benchmark returns and performance summaries.

### Feature diagnostics

    python main_mvp1_diagnostics.py us
    python main_mvp1_diagnostics.py eu

Produces descriptive statistics, correlation matrices, autocorrelations and diagnostic charts.

### HMM model grid

    python main_mvp2_hmm_spec_grid.py us
    python main_mvp2_hmm_spec_grid.py eu

Runs the HMM specification grid and compares regime-based allocation models.

### HMM selected models

    python main_mvp2_hmm_selected_models.py

Builds selected HMM models for deeper comparison.

### RSM models

    python main_mvp3_rsm.py us
    python main_mvp3_rsm.py eu

Runs Markov-switching regression strategies.

### Core comparison

    python main_core_model_comparison.py us
    python main_core_model_comparison.py eu

Compares benchmarks, HMM models and RSM models.

### Robustness analysis

    python main_mvp4_robustness.py

Runs transaction-cost sensitivity, no-trade band sensitivity and partial-rebalancing sensitivity.

### Crisis-period analysis

    python main_mvp4_crisis_analysis.py

Evaluates performance during crisis and stress windows.

### Final reports

    python main_final_us_report.py
    python main_final_eu_report.py
    python main_final_cross_market_report.py

Generates the final US, European and cross-market summaries.

### Thesis build

    python main_build_clean_thesis.py
    python main_build_final_thesis_package.py
    python main_thesis_quality_check.py

Builds the clean thesis draft, the final thesis package and a quality-check report.

## 10. Outputs

The main output folders are:

    outputs/tables/
    outputs/charts/

Key final output tables include:

    outputs/tables/us_final_implementable_summary.csv
    outputs/tables/eu_final_implementable_summary.csv
    outputs/tables/cross_market_key_strategy_comparison.csv
    outputs/tables/cross_market_empirical_conclusions.csv

Key final thesis files include:

    thesis/full_thesis_clean.md
    thesis/final_thesis_package.md
    thesis/abstract_keywords.md

## 11. Main limitations

The project has several important limitations:

- The pure VRP proxy is synthetic and should not be interpreted as a fully tradable variance-swap strategy.
- The European volatility series required manual reconstruction.
- Monthly frequency may miss short-lived volatility shocks.
- HMM and RSM models rely on a two-regime structure.
- Results may be sensitive to rolling-window length and feature selection.
- Transaction costs are simplified and do not fully model market impact, liquidity stress or execution delay.
- The project compares historical backtests and does not prove future profitability.

## 12. Final thesis conclusion

The Variance Risk Premium is not a universal standalone allocation factor.

The empirical evidence suggests that VRP is more defensible as a conditional regime-state signal for downside-risk management, especially in the US market.

However, its economic value depends on market structure, model specification, feature transformation, turnover control and implementation frictions.

## 13. Project status

Current status:

- US pipeline complete.
- European pipeline complete.
- VSTOXX reconstruction complete.
- HMM models complete.
- RSM models complete.
- Robustness analysis complete.
- Crisis-period analysis complete.
- Cross-market comparison complete.
- Thesis draft package complete.
- Academic README complete.

