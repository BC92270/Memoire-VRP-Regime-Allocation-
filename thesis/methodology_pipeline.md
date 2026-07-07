# Methodology Pipeline

## 1. Empirical objective

The empirical objective is to evaluate whether the Variance Risk Premium improves portfolio allocation when it is used as a regime-detection signal. The analysis compares traditional benchmarks, synthetic VRP exposure, Hidden Markov Models, and Markov-switching regression models across the US and European equity markets.

The pipeline is designed to answer three questions:

1. Does direct synthetic VRP exposure generate stable performance?
2. Does VRP improve regime detection and dynamic allocation?
3. Are the results robust across markets and implementation assumptions?

---

## 2. Markets and data

### 2.1 US market

The US market is represented by:

- Equity index proxy: SPY / S&P 500
- Implied volatility proxy: VIX
- Bond proxy: AGG

The US sample covers the period from 2005 to 2026, depending on the final aligned sample used by each model.

### 2.2 European market

The European market is represented by:

- Equity index proxy: EURO STOXX 50
- Implied volatility proxy: VSTOXX
- Bond proxy: IEAG.AS

The VSTOXX data is constructed from two sources:

1. official STOXX historical VSTOXX data up to 2016;
2. MarketWatch V2TX data from 2017 to 2026.

These files are merged into a single local file:

```text
data/raw/vstoxx.csv