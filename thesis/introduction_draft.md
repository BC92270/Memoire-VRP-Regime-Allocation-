# Introduction Draft

## 1. General context

Financial markets are characterized by periods of calm, stress, volatility spikes and regime changes. For portfolio managers, this creates a central problem: asset returns are not stable through time. The same allocation rule may perform well in a normal market environment and fail during periods of crisis, liquidity stress or sudden repricing of risk.

Traditional portfolio allocation often relies on simple diversified portfolios, such as buy-and-hold equity, 60/40 equity-bond allocation, or equal-weighted equity-bond portfolios. These benchmarks are transparent and robust, but they are not explicitly designed to detect changes in market regimes. In particular, they may remain too exposed to equity risk during periods of market stress.

This motivates the search for indicators that can identify market fragility before or during stress episodes. Volatility-based indicators are natural candidates because volatility tends to increase when markets become unstable. However, realized volatility alone is backward-looking. Implied volatility, by contrast, reflects market expectations and the price investors are willing to pay for protection against future uncertainty.

The Variance Risk Premium is located precisely at the intersection between realized volatility and implied volatility.

---

## 2. Variance Risk Premium and economic intuition

The Variance Risk Premium can be defined as the difference between implied variance and realized variance:

\[
VRP_t = IV_t - RV_t
\]

where \(IV_t\) is implied variance and \(RV_t\) is realized variance.

In theory, implied variance reflects the risk-neutral expectation of future variance embedded in option prices, while realized variance reflects the variance that actually materializes under the physical probability measure. The difference between the two can be interpreted as compensation for bearing variance risk.

The economic intuition is straightforward. Investors often demand protection against market crashes and volatility spikes. This protection is usually purchased through options or volatility-related instruments. Because demand for protection is high, implied volatility often exceeds subsequently realized volatility. The difference between implied and realized variance can therefore contain information about risk aversion, crash insurance demand, hedging pressure and market stress.

This makes the Variance Risk Premium interesting for two distinct reasons.

First, it may be treated as a tradable premium. In this interpretation, investors attempt to earn compensation by selling variance or volatility protection.

Second, it may be treated as an informational signal. In this interpretation, the VRP is not necessarily traded directly. Instead, it is used to detect whether the market is in a normal or stressed regime, and to adjust portfolio allocation accordingly.

This thesis focuses on the comparison between these two interpretations.

---

## 3. Research problem

The central research problem is the following:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

This question is important because the VRP literature often emphasizes the existence and predictive content of the variance premium. However, from an asset-allocation perspective, the practical question is not only whether the VRP exists, but whether it can improve portfolio decisions after transaction costs, turnover and implementation constraints.

A pure VRP strategy may look attractive in theory, but it is difficult to implement directly without variance swap data, option replication, contract rolling, margin assumptions and liquidity modelling. By contrast, using VRP as a signal inside a regime-based allocation model may be more realistic for a portfolio-allocation framework.

The thesis therefore compares two channels of economic value:

1. direct synthetic VRP exposure;
2. VRP as a regime-state variable used inside dynamic allocation models.

---

## 4. Research gap

The existing literature provides strong foundations for studying the Variance Risk Premium. Prior research shows that the difference between implied and realized variance is economically meaningful, related to option-market risk premia, and potentially informative about future equity-market conditions.

However, the literature often studies VRP either as a risk premium in derivatives markets or as a predictor of returns. Less attention is given to the question of whether VRP can improve dynamic portfolio allocation when used as an input to regime-detection models.

This thesis addresses this gap by combining three elements:

1. VRP-based features;
2. regime-switching models;
3. portfolio allocation against simple benchmarks.

The thesis also adds a cross-market comparison between the United States and Europe. This is important because a signal that works in the US market may not be robust in another market. Testing both regions makes it possible to assess whether VRP-based allocation is a general mechanism or a market-specific result.

---

## 5. Research question

The research question is:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

This question is decomposed into four sub-questions:

1. Does a synthetic pure VRP proxy generate stable performance across the US and European markets?
2. Does VRP improve regime detection in Hidden Markov Models and Markov-switching regression models?
3. Do VRP-enhanced regime models outperform traditional equity-bond benchmarks?
4. Are the results robust to market choice, transaction costs, turnover and crisis periods?

---

## 6. Hypotheses

The thesis tests the following hypotheses.

### Hypothesis 1 — Direct VRP exposure

A synthetic pure VRP proxy may generate attractive performance in some markets, but it is unlikely to be universally robust across regions because it depends heavily on volatility-index construction, option-market structure and proxy assumptions.

### Hypothesis 2 — VRP as a regime signal

VRP is expected to be more useful as an informational regime-state variable than as a standalone return engine, because it may help identify periods of market stress and reduce equity exposure during fragile regimes.

### Hypothesis 3 — Benchmark discipline

Simple benchmarks such as 60/40 and 1/N equity-bond allocation are difficult to beat out of sample. Therefore, a regime-switching model should not only improve returns, but also improve drawdowns, tail risk or turnover-adjusted performance.

### Hypothesis 4 — Cross-market instability

The economic value of VRP-based allocation is expected to be market-dependent. A signal that is useful in the US may not necessarily transfer to Europe.

---

## 7. Methodological overview

The empirical analysis is conducted on two markets:

- the US market, represented by the S&P 500, VIX and AGG;
- the European market, represented by the EURO STOXX 50, VSTOXX and IEAG.AS.

The core volatility features are:

\[
RV_t = 252 \sum_{d \in t} r_d^2
\]

\[
IV_t = \left(\frac{VolIndex_t}{100}\right)^2
\]

\[
VRP_t = IV_t - RV_t
\]

\[
LogVRP_t = \log\left(\frac{IV_t}{RV_t}\right)
\]

The empirical framework compares:

- buy-and-hold equity;
- 60/40 equity-bond allocation;
- 1/N equity-bond allocation;
- synthetic pure VRP exposure;
- Hidden Markov Model allocation;
- Markov-switching regression allocation.

The regime models are estimated using a rolling 72-month window and tested out of sample at monthly frequency. The allocation rule reduces equity exposure when the estimated stress probability increases.

Transaction costs, turnover, partial rebalancing and crisis-period performance are also analyzed to assess whether the strategies remain economically realistic.

---

## 8. Main empirical results

The empirical results are asymmetric across markets.

In the US, VRP-enhanced Hidden Markov Models are competitive with traditional equity-bond benchmarks and improve maximum drawdown. The HMM RV + Log VRP specification does not clearly dominate 60/40 or 1/N in Sharpe ratio, but it improves downside-risk control. The partial rebalancing version reduces turnover while preserving competitive performance, making it the most defensible implementable specification.

In Europe, the results do not confirm the US evidence. HMM and RSM models are technically feasible and generate regime probabilities, but they fail to outperform simple benchmarks. The European VRP signal does not transfer robustly in the tested framework.

The synthetic pure VRP proxy also behaves very differently across markets. It performs extremely well in the US but collapses in Europe. This suggests that direct VRP exposure, at least in proxy form, is not a universally robust return engine.

The main empirical conclusion is therefore:

> The Variance Risk Premium appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine. However, its economic value is market-dependent and conditional on implementation assumptions.

---

## 9. Contribution of the thesis

The thesis contributes to the literature in five ways.

First, it evaluates VRP not only as a direct premium, but also as an informational signal for regime-based allocation.

Second, it compares VRP-enhanced regime models with simple and robust benchmarks such as 60/40 and 1/N equity-bond allocation.

Third, it introduces a cross-market comparison between the US and Europe, showing that VRP-based allocation is not universally robust.

Fourth, it explicitly considers implementation issues such as transaction costs, turnover and partial rebalancing.

Fifth, it shows that the main value of VRP may be defensive rather than purely return-enhancing. In the US, the signal is most useful for reducing drawdowns, not for mechanically dominating simple benchmarks in Sharpe ratio.

This leads to a more nuanced interpretation of the Variance Risk Premium. The VRP should not be treated as a universal return factor. It is better understood as a conditional market-state signal whose value depends on market structure, model specification and implementation frictions.

---

## 10. Structure of the thesis

The thesis is organized as follows.

Chapter 1 reviews the literature on the Variance Risk Premium, volatility risk premia, regime-switching models and benchmark allocation. It positions the thesis between the variance-swap literature and the dynamic asset-allocation literature.

Chapter 2 presents the data and methodology. It describes the US and European datasets, the construction of realized variance, implied variance and VRP proxies, the benchmark strategies, the HMM and RSM frameworks, and the rolling out-of-sample backtest design.

Chapter 3 presents the empirical results. It analyzes the US results, the European results, and the cross-market comparison. It also discusses the interpretation of the synthetic pure VRP proxy.

Chapter 4 studies robustness and implementation. It examines transaction-cost sensitivity, no-trade bands, partial rebalancing and crisis-period performance.

Chapter 5 discusses the limitations of the study, including data limitations, proxy construction, model specification, market transferability, turnover and statistical-inference limitations.

The conclusion answers the research question and summarizes the main contribution: VRP appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine.