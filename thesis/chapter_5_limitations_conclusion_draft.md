# Chapter 5 — Limitations and Conclusion Draft

## 1. Introduction

This final chapter discusses the limitations of the thesis and summarizes the main empirical conclusions.

The objective of the thesis was to answer the following research question:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The empirical results provide a conditional answer. The Variance Risk Premium does not appear to be a universally robust standalone return engine. The synthetic pure VRP proxy performs extremely well in the US sample but collapses in the European sample. This cross-market instability makes it difficult to defend direct VRP exposure as a universal allocation strategy.

However, the VRP appears more useful when it is used as an informational signal in a regime-detection framework. In the US, the HMM RV + Log VRP model improves maximum drawdown relative to traditional benchmarks and remains competitive in Sharpe ratio. Once partial rebalancing is added, the model becomes more implementable because turnover is materially reduced.

The European results are weaker. In Europe, HMM and RSM models do not outperform simple benchmarks such as Buy-and-Hold Equity, 60/40 or 1/N Equity-Bond allocation. This shows that the economic value of VRP-based allocation is market-dependent.

The final conclusion is therefore:

> The Variance Risk Premium appears more useful as a conditional regime-state variable for downside-risk management than as a universally robust standalone return engine. However, its economic value depends on market structure, model specification, feature transformation and implementation frictions.

---

## 2. Data limitations

### 2.1 Difference between US and European data quality

A first limitation concerns data availability and data quality.

The US dataset is more robust because the main variables are easily accessible and widely used. SPY, VIX and AGG provide clean and liquid proxies for the US equity market, implied volatility and bond exposure.

The European dataset is more complex. The equity proxy is based on the EURO STOXX 50, the implied-volatility proxy is based on the VSTOXX, and the bond proxy is IEAG.AS. The VSTOXX series had to be manually reconstructed from multiple sources.

This creates a potential comparability issue between the US and European samples.

The US volatility proxy is cleaner and more directly available, while the European volatility proxy depends on a merged local file. Therefore, part of the weaker European result may be related to differences in data construction.

This does not invalidate the empirical results, but it requires caution when interpreting the cross-market comparison.

---

### 2.2 VSTOXX reconstruction

The European VSTOXX series was reconstructed from:

1. official STOXX historical data up to 2016;
2. MarketWatch V2TX data from 2017 to 2026.

These two sources were merged into:

```text
data/raw/vstoxx.csv