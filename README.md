# Memoire-VRP-Regime-Allocation

Master thesis project on Variance Risk Premium, regime-based allocation, HMM/RSM models, and portfolio performance against traditional benchmarks.

## Research question

Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

## Empirical objective

The project compares regime-based allocation models using HMM and Regime Switching Models on US and European equity markets.

The empirical framework studies:

- SPX / S&P 500 and VIX for the US market;
- SX5E / Euro Stoxx 50 and VSTOXX for the European market;
- realized variance;
- implied variance;
- Variance Risk Premium proxy;
- benchmark strategies;
- HMM and RSM regime-based allocation strategies.

## Strategy comparison

The project compares:

- buy-and-hold equity;
- 60/40 portfolio;
- 1/N allocation;
- pure VRP proxy strategy;
- HMM without VRP;
- HMM with VRP as signal;
- RSM without VRP;
- RSM with VRP as signal;
- synthetic VRP exposure as an extension.

## Core contribution

The thesis decomposes the economic value of the Variance Risk Premium into two channels:

1. VRP as a tradable variance exposure;
2. VRP as an informational signal for regime-based allocation.

## Project structure

```text
data/
notebooks/
src/
outputs/
thesis/
