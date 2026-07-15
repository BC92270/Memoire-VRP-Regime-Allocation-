# Master Thesis Draft

## Variance Risk Premium and Regime-Based Allocation

### Direct VRP Exposure versus Informational Regime Signal

This document contains the full thesis draft package, including abstract, keywords, literature review, methodology, empirical results, robustness analysis, limitations and conclusion.

---

# Abstract and Keywords

## Abstract

This thesis investigates whether the Variance Risk Premium creates more economic value as a direct synthetic exposure or as an informational signal for regime-based portfolio allocation. The analysis compares the US and European equity markets using equity index proxies, implied-volatility proxies, realized variance, synthetic VRP measures, traditional allocation benchmarks, Hidden Markov Models and Markov-switching regression models.

The empirical framework evaluates buy-and-hold equity, 60/40 equity-bond allocation, 1/N equity-bond allocation, synthetic VRP exposure, HMM-based regime allocation and RSM-based regime allocation. The models are estimated using rolling out-of-sample procedures and assessed through annualized return, volatility, Sharpe ratio, Sortino ratio, maximum drawdown, Calmar ratio, VaR, CVaR, turnover, transaction-cost sensitivity, partial rebalancing and crisis-period performance.

The results show a clear asymmetry between the US and Europe. In the US, VRP-enhanced HMM models are competitive with traditional benchmarks and improve maximum drawdown. The most defensible implementable specification is HMM RV + Log VRP with partial rebalancing, which preserves competitive performance while materially reducing turnover. In Europe, however, regime-switching models do not outperform simple benchmarks. The VRP signal does not transfer robustly to the European market in the tested specifications.

The synthetic pure VRP proxy performs extremely well in the US but collapses in Europe. This instability suggests that direct synthetic VRP exposure should be treated as an exploratory proxy rather than as a universally tradable allocation strategy.

The main conclusion is that the Variance Risk Premium is more useful as a conditional market-state signal for downside-risk management than as a universally robust standalone return engine. Its economic value depends on market structure, model specification, feature transformation, turnover control and implementation frictions.

## Keywords

Variance Risk Premium; realized variance; implied variance; volatility risk; Hidden Markov Model; Markov-switching regression; regime-based allocation; portfolio allocation; downside-risk management; transaction costs; turnover; VIX; VSTOXX; S&P 500; EURO STOXX 50.

---

# Introduction

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

---

# Chapter 1 — Literature Review

## 1. Introduction

This chapter reviews the academic foundations of the thesis. The objective is to position the research question at the intersection of the Variance Risk Premium literature, the volatility risk premium literature, regime-switching models, and dynamic asset allocation.

The central question of the thesis is:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

This question requires connecting several strands of research. First, the Variance Risk Premium must be defined and linked to option markets and variance swaps. Second, the economic intuition behind the premium must be explained. Third, the literature on the predictive content of the VRP must be reviewed. Fourth, regime-switching models must be introduced as a natural framework for using volatility-based information in allocation decisions. Finally, simple benchmarks such as 60/40 and 1/N portfolios must be discussed because complex allocation models should be evaluated against robust and transparent alternatives.

The thesis does not aim to prove that the Variance Risk Premium is a universally profitable standalone trading strategy. Instead, it studies whether VRP is more useful as a market-state variable for dynamic allocation. This distinction is central because direct variance trading is difficult to implement, while using VRP as an informational signal may be more relevant for portfolio management.

---

## 2. Variance Risk Premium: definition and economic meaning

### 2.1 Definition

The Variance Risk Premium is generally defined as the difference between the risk-neutral expectation of future variance and the physical expectation of realized variance. In empirical applications, it is often approximated as the difference between implied variance and realized variance:

\[
VRP_t = IV_t - RV_t
\]

where \(IV_t\) represents implied variance and \(RV_t\) represents realized variance.

Implied variance is extracted from option prices or volatility indices. It reflects the price investors are willing to pay for future volatility protection under the risk-neutral probability measure. Realized variance is computed from historical returns under the physical probability measure. The difference between the two captures the compensation required by investors who sell volatility or variance protection.

Carr and Wu (2009) provide one of the central references on variance risk premia. Their framework studies variance risk premia across different asset classes and links the concept directly to variance swaps. This is important because variance swaps offer a clean theoretical instrument for isolating exposure to future realized variance. In a variance swap, the payoff depends on the difference between realized variance and the fixed variance swap rate. This makes the variance premium directly observable when variance swap data are available.

In practice, however, variance swap data are not always easily accessible. Many empirical studies therefore rely on proxies based on implied volatility indices and realized variance. This thesis follows that practical approach by using VIX for the US market and VSTOXX for the European market.

### 2.2 Economic intuition

The existence of the Variance Risk Premium is usually explained by investors’ demand for protection against volatility spikes and market crashes. During periods of uncertainty, investors are willing to pay for options that protect their portfolios against large downside moves. Sellers of this protection demand compensation for bearing volatility and crash risk.

As a result, implied variance tends to exceed subsequently realized variance on average. This difference can be interpreted as an insurance premium paid by option buyers to option sellers.

The VRP is therefore connected to several economic mechanisms:

- crash insurance demand;
- risk aversion;
- volatility risk compensation;
- hedging pressure;
- intermediary risk-bearing capacity;
- option-market supply and demand.

Bakshi and Kapadia (2003) provide important evidence on the negative market volatility risk premium using delta-hedged option strategies. Their results show that option returns contain compensation for volatility risk. This supports the interpretation of the VRP as a priced risk premium rather than a purely statistical artifact.

The economic intuition also explains why VRP may contain information about market regimes. A high implied variance relative to realized variance may indicate elevated demand for protection, increased risk aversion, or market stress. Therefore, VRP may be useful not only as a return premium, but also as a state variable.

---

## 3. Direct VRP exposure versus informational VRP signal

The literature suggests two possible uses of the Variance Risk Premium.

The first use is direct trading. In this interpretation, investors attempt to harvest the variance premium by selling variance or volatility protection. The logic is that if implied variance tends to exceed realized variance, a short variance exposure should earn positive compensation over time.

The second use is informational. In this interpretation, VRP is not necessarily traded directly. Instead, it is used to infer the state of the market. A high or changing VRP may contain information about investor fear, hedging pressure or crash-risk pricing. This information can then be used to adjust asset allocation.

This distinction is important for the thesis.

Direct VRP exposure may appear attractive in theory, but it is difficult to implement realistically. A true variance swap strategy requires:

- variance swap prices;
- maturity matching;
- contract rolling;
- option-market replication;
- margin and collateral assumptions;
- bid-ask spreads;
- liquidity modelling;
- transaction costs;
- variance notional scaling.

A simplified VRP proxy does not capture all these elements. Therefore, the thesis treats the synthetic pure VRP proxy as an exploratory benchmark rather than as a fully tradable strategy.

Using VRP as a signal is more realistic for an asset-allocation framework. A portfolio manager may not need to trade variance swaps directly. Instead, the manager can use the VRP to detect whether the market is entering a stress regime and reduce equity exposure accordingly.

This thesis therefore asks whether the VRP creates more economic value as a direct synthetic exposure or as a regime-detection signal.

---

## 4. Predictive content of the Variance Risk Premium

A major contribution of the VRP literature is the finding that variance risk premia may contain predictive information about future equity returns.

Bollerslev, Tauchen and Zhou (2009) show that the variance risk premium has predictive power for stock market returns. Their paper is central for this thesis because it supports the idea that the gap between implied and realized variance contains information about future market conditions.

The intuition is that implied variance reflects forward-looking market prices, while realized variance reflects past market movements. The difference between them may capture changes in risk aversion, uncertainty and the compensation investors require for holding risky assets.

In this thesis, the predictive interpretation is not used to forecast returns directly. Instead, it motivates the use of VRP as an input in regime-detection models. The question becomes:

> Can the Variance Risk Premium help identify whether the market is in a normal or stressed regime?

This is why the empirical framework uses features such as:

\[
RV_t
\]

\[
IV_t
\]

\[
VRP_t = IV_t - RV_t
\]

and

\[
LogVRP_t = \log\left(\frac{IV_t}{RV_t}\right)
\]

The log transformation is useful because it captures the relative difference between implied and realized variance. It may also reduce scale instability compared with the raw difference.

---

## 5. Regime-switching models

### 5.1 Why regimes matter in finance

Financial markets are not stable through time. Expected returns, volatility, correlations and tail risks change across market environments. A portfolio that performs well during calm periods may perform poorly during crises.

This motivates the use of regime-switching models. Instead of assuming one stable data-generating process, these models assume that markets switch between different latent states. These states may correspond to normal conditions, stress periods, high-volatility regimes or crisis states.

Regime-switching models are particularly relevant for asset allocation because portfolio weights should depend on the state of the market. If the probability of a stress regime increases, a dynamic allocation strategy may reduce equity exposure and increase defensive exposure.

### 5.2 Hamilton’s Markov-switching framework

Hamilton (1989) provides the foundational econometric framework for Markov-switching models. In his approach, the economy can switch between latent states, and the observed time series depends on the current state. The state itself follows a Markov process.

This framework is useful because it allows model parameters to change across regimes. For example, returns may have different means and variances in normal and crisis states.

The core idea is that the state is not directly observed. It must be inferred from the data. This is precisely the type of problem faced by investors: the market regime is not known with certainty, but it can be estimated probabilistically.

### 5.3 Hidden Markov Models

Hidden Markov Models are a natural extension of this idea. An HMM assumes that observed data are generated by an unobserved state process. The model estimates the probability of each hidden state using observable features.

In this thesis, the HMM is used to estimate a market stress probability. The observable variables include equity returns, realized variance and VRP-related features. The hidden states are interpreted as normal and stress regimes.

The allocation rule then uses the estimated stress probability to adjust equity exposure:

\[
w^{eq}_t = 0.80(1 - p^{stress}_t) + 0.20p^{stress}_t
\]

When the stress probability is low, the portfolio holds more equity. When the stress probability is high, the portfolio reduces equity exposure and moves toward bonds.

This creates a direct link between the VRP literature and dynamic asset allocation.

### 5.4 Markov-switching regressions

The thesis also uses Markov-switching regression models. Unlike the HMM, which models latent states through the joint distribution of observed features, the Markov-switching regression framework allows return dynamics to vary across regimes.

The tested RSM specifications include:

- returns-only models;
- realized-variance models;
- realized-variance plus raw VRP models;
- realized-variance plus log VRP models.

The objective is to test whether adding VRP-related information improves the economic value of regime-based allocation.

---

## 6. Regime-switching and asset allocation literature

Regime-switching models have been widely used in asset allocation because investment opportunities vary over time.

Ang and Bekaert (2002) study international asset allocation with regime shifts. Their work shows that regimes matter because volatility and correlations can change significantly across states. This is especially important during market stress, when diversification benefits may decline.

Guidolin and Timmermann (2007) also show that regime-switching models can generate materially different asset-allocation decisions across states. Their work supports the idea that dynamic portfolio weights can be justified when return distributions are regime-dependent.

This thesis builds on that literature but introduces a specific volatility-based state variable: the Variance Risk Premium. The key question is not simply whether regimes exist, but whether VRP improves the identification of economically useful regimes.

This is the main link between the literature and the empirical design of the thesis.

---

## 7. Benchmark allocation and model discipline

A central methodological issue in asset allocation is benchmark discipline. Complex models should not be evaluated in isolation. They must be compared with simple strategies that are transparent, robust and difficult to beat.

The thesis uses three main benchmarks:

- buy-and-hold equity;
- 60/40 equity-bond allocation;
- 1/N equity-bond allocation.

The 60/40 portfolio is a standard balanced benchmark. It combines equity risk exposure with defensive bond exposure. The 1/N portfolio is a naive equal-weighted allocation rule.

DeMiguel, Garlappi and Uppal (2009) show that many optimized portfolio strategies fail to consistently outperform the naive 1/N diversification rule out of sample. This result is important because it warns against overestimating the value of complex models.

This thesis takes that warning seriously. The empirical question is not whether HMM or RSM models look sophisticated, but whether they improve performance relative to simple and robust benchmarks after considering turnover and transaction costs.

This benchmark discipline is essential for the credibility of the thesis.

---

## 8. Positioning of the thesis

The literature provides the following foundations:

1. The Variance Risk Premium is economically meaningful and related to compensation for bearing variance risk.
2. VRP may contain predictive information about future equity-market conditions.
3. Regime-switching models are appropriate when market conditions change through time.
4. Simple benchmarks such as 60/40 and 1/N are difficult to beat out of sample.

This thesis connects these ideas in one empirical framework.

The research question is positioned as follows:

> Is the Variance Risk Premium more valuable as a direct synthetic exposure or as an informational signal for regime-based allocation?

The thesis contributes by testing this question across both the US and European markets. This cross-market dimension is important because much of the volatility literature is heavily US-centered. If a signal works only in the US, its generality is limited.

The empirical results later show precisely this type of asymmetry. VRP-enhanced HMM models are useful in the US mainly through drawdown reduction, but the same logic does not transfer robustly to Europe.

This means that the thesis does not simply confirm or reject the VRP literature. It refines it.

The main positioning is:

> VRP may be informative, but its economic value depends on the market, the model, the transformation, the benchmark and the implementation assumptions.

---

## 9. Research gap addressed by the thesis

The existing literature often studies VRP either as a derivatives-market risk premium or as a predictor of future returns.

This thesis studies a different question:

> Can VRP improve dynamic asset allocation by helping detect market regimes?

This research gap is important because a variable can be statistically predictive without being economically useful in a portfolio after costs and constraints. The thesis therefore focuses on economic value, not only statistical interpretation.

The thesis addresses the gap in four ways.

First, it compares direct synthetic VRP exposure with VRP-based regime allocation.

Second, it evaluates the models against simple benchmarks.

Third, it includes both HMM and RSM frameworks.

Fourth, it compares the US and European markets.

This gives the thesis a clear empirical contribution: it evaluates VRP as a conditional regime signal rather than as a universal return factor.

---

## 10. Expected contribution before empirical testing

Before observing the empirical results, the expected contribution of the thesis is to clarify whether VRP is more useful for trading or for allocation.

If the pure VRP proxy performs consistently across markets, this would support the idea that the VRP can be treated as a standalone return premium.

If the regime models outperform benchmarks, this would support the idea that VRP is useful as a state variable.

If the results differ across markets, this would show that VRP is conditional and market-dependent.

The empirical results later support the third interpretation. The VRP has useful informational content in the US, especially for drawdown control, but it does not transfer robustly to Europe.

This makes the thesis contribution more nuanced and more credible.

---

## 11. Chapter conclusion

This chapter reviewed the literature needed to understand the thesis.

The Variance Risk Premium literature explains why implied variance can exceed realized variance and why investors may be compensated for bearing volatility risk. The predictive-VRP literature suggests that the difference between implied and realized variance can contain information about future market conditions. The regime-switching literature provides the econometric framework for using this information to detect latent market states. The benchmark-allocation literature explains why simple portfolios such as 60/40 and 1/N must be used as strict comparison points.

The thesis is therefore positioned between variance-risk-premium research and regime-based asset allocation.

The central argument developed from the literature is:

> The Variance Risk Premium should not only be studied as a tradable derivatives premium. It can also be studied as a conditional market-state variable for dynamic asset allocation.

The empirical chapters test whether this interpretation creates economic value in the US and European markets.

---

## References

Bakshi, G., & Kapadia, N. (2003). Delta-Hedged Gains and the Negative Market Volatility Risk Premium. *The Review of Financial Studies*, 16(2), 527–566.

Carr, P., & Wu, L. (2009). Variance Risk Premiums. *The Review of Financial Studies*, 22(3), 1311–1341.

Bollerslev, T., Tauchen, G., & Zhou, H. (2009). Expected Stock Returns and Variance Risk Premia. *The Review of Financial Studies*, 22(11), 4463–4492.

Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. *Econometrica*, 57(2), 357–384.

Ang, A., & Bekaert, G. (2002). International Asset Allocation with Regime Shifts. *The Review of Financial Studies*, 15(4), 1137–1187.

Guidolin, M., & Timmermann, A. (2007). Asset Allocation under Multivariate Regime Switching. *Journal of Economic Dynamics and Control*, 31(11), 3503–3544.

DeMiguel, V., Garlappi, L., & Uppal, R. (2009). Optimal versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy? *The Review of Financial Studies*, 22(5), 1915–1953.

---

# Chapter 2 — Data and Methodology

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

---

# Chapter 3 — Empirical Results

## 1. Introduction

This chapter presents the empirical results of the thesis. The objective is to evaluate whether the Variance Risk Premium creates more economic value when it is directly traded through a synthetic proxy or when it is used as an informational signal inside regime-based allocation models.

The chapter follows the empirical structure introduced in the methodology. It compares:

- traditional benchmarks;
- synthetic pure VRP exposure;
- Hidden Markov Model strategies;
- Markov-switching regression strategies;
- US and European results;
- cross-market evidence.

The central question remains:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The results show a clear asymmetry between the US and European markets. In the US, VRP-enhanced Hidden Markov Models are competitive with traditional equity-bond benchmarks and improve maximum drawdown. In Europe, regime-switching models do not outperform simple benchmarks. The synthetic pure VRP proxy also behaves very differently across markets: it is extremely strong in the US but collapses in Europe.

The main empirical conclusion is therefore nuanced. VRP appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine.

---

## 2. US empirical results

## 2.1 US benchmark results

The first step is to evaluate the traditional benchmark portfolios.

The US benchmark strategies are:

- Buy-and-Hold Equity;
- 60/40 Equity-Bond;
- 1/N Equity-Bond.

The aligned US results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 0.1396 | 0.1420 | 0.9955 | 1.4827 | -0.2393 | 0.5833 | -0.0608 | -0.0818 | 0.0000 | 184 |
| 60/40 | 0.0939 | 0.0921 | 1.0238 | 1.4811 | -0.2006 | 0.4681 | -0.0385 | -0.0520 | 0.0147 | 184 |
| 1/N Equity-Bond | 0.0823 | 0.0805 | 1.0253 | 1.4596 | -0.1910 | 0.4308 | -0.0336 | -0.0458 | 0.0153 | 184 |

The benchmark results show that simple equity-bond portfolios are difficult to outperform. Buy-and-Hold Equity has the highest annualized return, with 13.96%, but it also has the largest drawdown among the three benchmarks, at -23.93%.

The 60/40 and 1/N portfolios produce lower annualized returns but better risk-adjusted performance. Their Sharpe ratios are slightly above 1, with 1.0238 for 60/40 and 1.0253 for 1/N. They also reduce maximum drawdown relative to buy-and-hold equity.

This is an important benchmark result. It means that any regime-switching model must be evaluated against already strong traditional allocation rules. A model that performs well in isolation may still fail to add economic value if it does not improve on these simple portfolios.

---

## 2.2 US synthetic pure VRP proxy

The synthetic pure VRP proxy produces very strong performance in the US sample.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Synthetic Pure VRP Proxy | 0.3875 | 0.1162 | 2.9144 | 4.0317 | -0.0975 | 3.9724 | -0.0229 | -0.0505 | 0.0037 | 184 |

The US synthetic pure VRP proxy strongly outperforms the traditional benchmarks. It has an annualized return of 38.75%, annualized volatility of 11.62%, and a Sharpe ratio of 2.9144. Its maximum drawdown is only -9.75%, materially below the drawdowns of the traditional benchmarks.

However, this result must be interpreted cautiously. The synthetic pure VRP proxy is not a fully tradable variance swap strategy. It does not include variance swap contract pricing, maturity matching, margin requirements, option-market transaction costs, bid-ask spreads, liquidity constraints or variance notional scaling.

Therefore, this result should not be interpreted as direct evidence that an investor could have earned this exact performance by trading variance swaps. Instead, it shows that the US VRP proxy contains strong economic information over the sample.

This distinction is central to the thesis. The pure proxy result supports the informational relevance of the VRP, but not necessarily the direct tradability of the proxy.

---

## 2.3 US HMM results

The HMM specifications test whether VRP-related variables improve regime-based allocation.

The selected US HMM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 0.0817 | 0.0833 | 0.9870 | 1.4462 | -0.1779 | 0.4590 | -0.0428 | -0.0488 | 0.1757 | 184 |
| HMM RV + Raw VRP | 0.1067 | 0.1059 | 1.0135 | 1.5094 | -0.2198 | 0.4853 | -0.0461 | -0.0603 | 0.0957 | 184 |
| HMM RV + Log VRP | 0.0836 | 0.0824 | 1.0187 | 1.4926 | -0.1667 | 0.5013 | -0.0419 | -0.0486 | 0.2535 | 184 |

The HMM results are economically meaningful but nuanced.

The HMM RV + Log VRP model produces a Sharpe ratio of 1.0187, which is close to the 60/40 and 1/N benchmarks. It does not clearly dominate them in terms of Sharpe ratio. However, it improves maximum drawdown. The maximum drawdown of HMM RV + Log VRP is -16.67%, compared with -20.06% for 60/40, -19.10% for 1/N, and -23.93% for buy-and-hold equity.

This is the main positive US HMM result. The model does not primarily create value through higher average returns. Instead, it creates value by reducing downside risk.

The HMM RV + Raw VRP specification has a higher annualized return than HMM RV + Log VRP, at 10.67%, but it has a worse maximum drawdown of -21.98%. This makes it less attractive from a downside-risk perspective.

The HMM RV model without VRP also improves drawdown relative to traditional benchmarks, but its Sharpe ratio is lower than the HMM specifications that include VRP. This suggests that volatility information is useful, but the VRP-enhanced specifications provide additional economic content.

---

## 2.4 US partial rebalancing result

The full-rebalancing HMM RV + Log VRP model has strong downside-risk properties, but it also has high turnover. Its average turnover is 25.35%, which may be too high for a realistic allocation strategy.

To address this issue, partial rebalancing is applied. The most defensible implementable specification is HMM RV + Log VRP with partial rebalancing speed 0.25.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV + Log VRP, full rebalance | 0.0836 | 0.0824 | 1.0187 | 1.4926 | -0.1667 | 0.5013 | -0.0419 | -0.0486 | 0.2535 | 184 |
| HMM RV + Log VRP, partial rebalance 0.25 | 0.0869 | 0.0862 | 1.0135 | 1.4948 | -0.1804 | 0.4819 | -0.0394 | -0.0500 | 0.0910 | 184 |

Partial rebalancing reduces average turnover from 25.35% to 9.10%. The Sharpe ratio remains competitive, falling only slightly from 1.0187 to 1.0135. Maximum drawdown increases from -16.67% to -18.04%, but remains below the drawdown of 60/40 and buy-and-hold equity.

This result is important because it shows that the model can be made more implementable without destroying its economic properties.

The partial rebalancing result supports the idea that VRP-enhanced HMM models are useful not as aggressive return engines, but as controlled risk-management tools.

---

## 2.5 US RSM results

The Markov-switching regression models provide a second regime-based framework.

The selected US RSM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 0.0713 | 0.0776 | 0.9287 | 1.3252 | -0.1837 | 0.3878 | -0.0368 | -0.0463 | 0.1592 | 184 |
| RSM RV | 0.0830 | 0.0995 | 0.8530 | 1.1934 | -0.1567 | 0.5297 | -0.0417 | -0.0585 | 0.3214 | 184 |
| RSM RV + Raw VRP | 0.0961 | 0.1025 | 0.9486 | 1.4117 | -0.1543 | 0.6225 | -0.0398 | -0.0553 | 0.3669 | 184 |
| RSM RV + Log VRP | 0.0757 | 0.0985 | 0.7917 | 1.0882 | -0.2088 | 0.3624 | -0.0432 | -0.0602 | 0.2428 | 184 |

The RSM RV + Raw VRP model has the best maximum drawdown among the implementable US regime-switching strategies, at -15.43%. However, it also has very high turnover, at 36.69%. This makes it less attractive from an implementation perspective.

The RSM results confirm that regime-switching models can improve drawdown, but they also show the cost of model instability. High turnover can reduce the practical value of a strategy even when the headline risk metrics look attractive.

Compared with the HMM results, the RSM results are less compelling. The HMM RV + Log VRP model provides a better balance between Sharpe ratio, drawdown and implementability, especially after partial rebalancing.

---

## 2.6 US conclusion

The US results support the idea that the Variance Risk Premium contains useful information for regime-based allocation.

However, the evidence must be interpreted precisely.

The US evidence does not show that VRP-enhanced regime models clearly dominate traditional benchmarks in all dimensions. The 60/40 and 1/N portfolios remain highly competitive in Sharpe ratio. The value of the HMM RV + Log VRP model is mainly visible in downside-risk control.

The most defensible US result is:

> In the US market, VRP-enhanced HMM models are competitive with traditional equity-bond benchmarks and improve maximum drawdown. The most defensible implementable specification is HMM RV + Log VRP with partial rebalancing.

This supports the interpretation of VRP as a regime-state variable rather than as a simple standalone return factor.

---

## 3. European empirical results

## 3.1 European benchmark results

The European benchmark results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 0.0688 | 0.1835 | 0.4629 | 0.5000 | -0.3397 | 0.2025 | -0.0601 | -0.1215 | 0.0000 | 127 |
| 60/40 | 0.0466 | 0.1140 | 0.4590 | 0.4923 | -0.2090 | 0.2229 | -0.0380 | -0.0760 | 0.0167 | 127 |
| 1/N Equity-Bond | 0.0401 | 0.0975 | 0.4539 | 0.4931 | -0.2034 | 0.1970 | -0.0352 | -0.0656 | 0.0174 | 127 |

The European benchmark results differ from the US results. Sharpe ratios are materially lower in Europe. Buy-and-Hold Equity has the highest annualized return and the highest Sharpe ratio, but it also has the largest drawdown, at -33.97%.

The 60/40 and 1/N portfolios reduce drawdown substantially. Their Sharpe ratios are close to buy-and-hold equity, while their maximum drawdowns are much lower.

This means that the European benchmark environment is difficult for regime-switching models. A model must improve risk-adjusted performance or downside protection relative to already defensive equity-bond benchmarks.

---

## 3.2 European synthetic pure VRP proxy

The European pure VRP proxy performs very poorly.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| Pure VRP Proxy | -0.3625 | 0.1508 | -2.8511 | -3.4570 | -0.9901 | -0.3661 | -0.1094 | -0.1453 | 0.0054 | 127 |

This result is one of the most important findings of the thesis. The same synthetic VRP logic that performs extremely well in the US collapses in Europe.

The European pure VRP proxy has an annualized return of -36.25%, a Sharpe ratio of -2.8511, and a maximum drawdown of -99.01%. This makes it economically unusable as a standalone proxy strategy in the European sample.

The contrast between the US and European pure VRP proxies shows that direct synthetic VRP exposure is not robust across markets.

This supports a cautious interpretation:

> The synthetic pure VRP proxy is useful as an exploratory indicator of variance-premium information, but it should not be interpreted as a universally tradable return engine.

---

## 3.3 European HMM results

The European HMM results are weak.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 0.0096 | 0.1233 | 0.1455 | 0.1335 | -0.3197 | 0.0301 | -0.0410 | -0.0902 | 0.1160 | 127 |
| HMM RV + Raw VRP | 0.0076 | 0.1235 | 0.1295 | 0.1193 | -0.3316 | 0.0231 | -0.0410 | -0.0908 | 0.1261 | 127 |
| HMM RV + Log VRP | 0.0075 | 0.1231 | 0.1281 | 0.1177 | -0.3110 | 0.0240 | -0.0410 | -0.0906 | 0.1338 | 127 |

The European HMM models fail to outperform the benchmarks. Their Sharpe ratios are far below the benchmark Sharpe ratios. Their maximum drawdowns are also worse than those of the 60/40 and 1/N portfolios.

The HMM RV + Log VRP model, which is the strongest implementable HMM candidate in the US, performs poorly in Europe. Its Sharpe ratio is only 0.1281 and its maximum drawdown is -31.10%.

This result is important because it shows that the US HMM conclusion does not transfer mechanically to Europe. The model remains technically feasible, but it is economically weak.

---

## 3.4 European RSM results

The European RSM results are stronger than the HMM results but still below the benchmarks.

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | Calmar | VaR 95 | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 0.0346 | 0.1371 | 0.3219 | 0.3235 | -0.2686 | 0.1288 | -0.0456 | -0.0966 | 0.1457 | 127 |
| RSM RV | 0.0342 | 0.1373 | 0.3187 | 0.3241 | -0.2692 | 0.1269 | -0.0453 | -0.0964 | 0.1161 | 127 |
| RSM RV + Raw VRP | 0.0193 | 0.1202 | 0.2233 | 0.2223 | -0.2815 | 0.0685 | -0.0436 | -0.0857 | 0.2476 | 127 |
| RSM RV + Log VRP | 0.0289 | 0.1366 | 0.2822 | 0.2849 | -0.2695 | 0.1072 | -0.0452 | -0.0965 | 0.1437 | 127 |

The best European RSM model is RSM Returns Only, with a Sharpe ratio of 0.3219. However, this is still below the benchmark Sharpe ratios of Buy-and-Hold Equity, 60/40 and 1/N.

Adding VRP does not improve the RSM results. The RSM RV + Raw VRP specification has a lower Sharpe ratio and higher turnover. The RSM RV + Log VRP specification also remains below the returns-only and RV-only models.

This suggests that in Europe, the VRP features do not add robust economic value to regime-switching allocation.

---

## 3.5 European conclusion

The European evidence is negative but highly informative.

The main European conclusion is:

> In the European sample, regime-switching models are technically feasible but economically weak relative to simple equity-bond benchmarks. The VRP signal does not transfer robustly to Europe in the tested specifications.

This does not invalidate the thesis. On the contrary, it strengthens the empirical contribution by showing that VRP-based allocation is not universal.

The European results show that:

- market structure matters;
- volatility-index construction matters;
- proxy quality matters;
- simple benchmarks remain difficult to beat;
- VRP-based allocation is conditional rather than universal.

---

## 4. Cross-market comparison

## 4.1 Key strategy comparison

The cross-market results summarize the main empirical evidence.

| Market | Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover | Obs |
|---|---|---:|---:|---:|---:|---:|---:|
| US | Buy-and-Hold Equity | 0.1396 | 0.1420 | 0.9955 | -0.2393 | 0.0000 | 184 |
| US | 60/40 | 0.0939 | 0.0921 | 1.0238 | -0.2006 | 0.0147 | 184 |
| US | 1/N Equity-Bond | 0.0823 | 0.0805 | 1.0253 | -0.1910 | 0.0153 | 184 |
| US | HMM RV + Log VRP, full rebalance | 0.0836 | 0.0824 | 1.0187 | -0.1667 | 0.2535 | 184 |
| US | HMM RV + Log VRP, partial rebalance 0.25 | 0.0869 | 0.0862 | 1.0135 | -0.1804 | 0.0910 | 184 |
| US | RSM RV + Raw VRP | 0.0961 | 0.1025 | 0.9486 | -0.1543 | 0.3669 | 184 |
| EU | Buy-and-Hold Equity | 0.0688 | 0.1835 | 0.4629 | -0.3397 | 0.0000 | 127 |
| EU | 60/40 | 0.0466 | 0.1140 | 0.4590 | -0.2090 | 0.0167 | 127 |
| EU | 1/N Equity-Bond | 0.0401 | 0.0975 | 0.4539 | -0.2034 | 0.0174 | 127 |
| EU | HMM RV + Log VRP | 0.0075 | 0.1231 | 0.1281 | -0.3110 | 0.1338 | 127 |
| EU | RSM Returns Only | 0.0346 | 0.1371 | 0.3219 | -0.2686 | 0.1457 | 127 |
| EU | RSM RV + Raw VRP | 0.0193 | 0.1202 | 0.2233 | -0.2815 | 0.2476 | 127 |

The cross-market comparison shows that the US and European results are fundamentally different.

In the US, the best HMM model is competitive with traditional benchmarks and improves drawdown. In Europe, the same type of model fails to outperform simple benchmarks.

This result implies that the economic value of VRP-based regime allocation is market-dependent.

---

## 4.2 Pure VRP proxy comparison

The pure VRP proxy comparison is even more striking.

| Market | Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover | Obs |
|---|---|---:|---:|---:|---:|---:|---:|
| US | Synthetic Pure VRP Proxy | 0.3875 | 0.1162 | 2.9144 | -0.0975 | 0.0037 | 184 |
| EU | Pure VRP Proxy | -0.3625 | 0.1508 | -2.8511 | -0.9901 | 0.0054 | 127 |

The synthetic pure VRP proxy is extremely strong in the US and extremely weak in Europe.

This finding is central to the thesis. It shows that the direct VRP proxy is not robust across markets. A result that looks very attractive in one region can collapse in another.

This supports the argument that VRP should not be treated mechanically as a universal return factor.

---

## 4.3 Cross-market interpretation

The cross-market evidence leads to three conclusions.

First, the US evidence supports the informational value of VRP. The HMM RV + Log VRP model improves drawdown while remaining competitive with simple benchmarks.

Second, the European evidence rejects a universal interpretation. VRP-enhanced models fail to outperform traditional portfolios in Europe.

Third, the pure VRP proxy is too unstable to support a strong conclusion in favor of direct VRP exposure.

Therefore, the most defensible interpretation is:

> VRP is more credible as a conditional regime-state variable than as a universally robust standalone return engine.

---

## 5. Answer to the research question

The research question asked:

> Does the Variance Risk Premium create more economic value when it is directly traded, or when it is used as an informational signal to detect market regimes and improve portfolio allocation?

The empirical answer is conditional.

The direct synthetic VRP proxy performs extremely well in the US but collapses in Europe. This means that direct proxy exposure cannot be considered a robust cross-market return engine.

Using VRP as a regime signal produces more defensible results. In the US, the HMM RV + Log VRP model improves maximum drawdown and remains competitive with strong benchmarks. Its partial rebalancing version also reduces turnover, making it more realistic.

However, the European results show that even the signal-based approach is not universally robust.

The final answer is therefore:

> The Variance Risk Premium appears more useful as a regime-state variable for downside-risk management than as a universally robust standalone return engine. However, its economic value is market-dependent and conditional on implementation assumptions.

---

## 6. Main empirical contribution

The main contribution of this chapter is not to show that a complex model always beats simple benchmarks. The results show the opposite: simple portfolios remain extremely difficult to outperform.

The contribution is more precise.

First, the thesis shows that VRP-enhanced HMM models can improve downside-risk management in the US.

Second, it shows that this result does not replicate in Europe.

Third, it documents a strong instability in synthetic pure VRP proxy performance across markets.

Fourth, it shows that turnover and implementation constraints materially affect the attractiveness of regime-switching strategies.

Fifth, it provides a disciplined comparison against simple benchmarks.

The thesis therefore contributes to the literature by showing that VRP should be interpreted as a conditional market-state signal, not as a universal return factor.

---

## 7. Chapter conclusion

This chapter presented the empirical results of the thesis.

The US results show that VRP-enhanced HMM models are competitive with traditional benchmarks and improve maximum drawdown. The HMM RV + Log VRP model with partial rebalancing is the most defensible implementable specification because it preserves competitive performance while reducing turnover.

The European results are materially weaker. HMM and RSM models do not outperform simple benchmarks, and VRP features do not add robust economic value.

The synthetic pure VRP proxy performs extremely well in the US but collapses in Europe. This confirms that direct VRP proxy exposure is not robust across markets.

The main conclusion is that the Variance Risk Premium is more useful as a conditional regime-state variable than as a universally robust standalone return engine.

The next chapter examines robustness and implementation issues, including transaction costs, no-trade bands, partial rebalancing and crisis-period performance.

---

# Chapter 4 — Robustness and Implementation

## 1. Introduction

This chapter examines whether the empirical results remain economically meaningful after considering implementation constraints. This is essential because a regime-switching allocation model can look attractive in a frictionless backtest but become less relevant once transaction costs, turnover, rebalancing constraints and crisis-period behavior are taken into account.

The objective is not only to identify the strategy with the highest Sharpe ratio. The objective is to determine whether the strategy is realistic, robust and defensible from a portfolio-management perspective.

The robustness analysis focuses on four dimensions:

1. transaction-cost sensitivity;
2. no-trade band sensitivity;
3. partial rebalancing;
4. crisis-period performance.

The main result of this chapter is that the US HMM RV + Log VRP model remains economically interesting, but only when implementation frictions are controlled. Full rebalancing generates high turnover, while partial rebalancing improves implementability. In Europe, robustness tests confirm that regime-switching models remain economically weak relative to simple benchmarks.

---

## 2. Why implementation matters

The previous chapter showed that VRP-enhanced HMM models can improve downside-risk management in the US. However, a model that reduces drawdown but requires excessive turnover may not be attractive in practice.

Implementation matters for three reasons.

First, transaction costs reduce net returns. Strategies that rebalance frequently are more exposed to costs.

Second, high turnover creates operational complexity. Even if transaction costs are low, frequent rebalancing can make a strategy less realistic.

Third, regime-switching models may react to noise. A model that changes allocation too frequently may overfit short-term fluctuations rather than identify stable regimes.

Therefore, the robustness analysis evaluates whether the results survive more realistic portfolio-construction assumptions.

---

## 3. Transaction-cost sensitivity

### 3.1 Method

Transaction costs are applied through turnover-adjusted returns:

\[
r^{net}_t = r^{gross}_t - c \times Turnover_t
\]

where \(c\) is the transaction-cost rate.

The tested transaction-cost levels are:

\[
0,\ 5,\ 10,\ 25,\ 50 \text{ bps}
\]

The baseline transaction-cost assumption is 10 bps. The sensitivity analysis evaluates how Sharpe ratios and drawdowns evolve when costs increase.

---

### 3.2 US transaction-cost sensitivity: Sharpe ratio

| Strategy | 0 bps | 5 bps | 10 bps | 25 bps | 50 bps |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 1.0275 | 1.0264 | 1.0253 | 1.0219 | 1.0163 |
| 60/40 | 1.0256 | 1.0247 | 1.0238 | 1.0209 | 1.0162 |
| Buy-and-Hold Equity | 0.9955 | 0.9955 | 0.9955 | 0.9955 | 0.9955 |
| HMM RV | 1.0123 | 0.9997 | 0.9870 | 0.9488 | 0.8843 |
| HMM RV + Log VRP | 1.0553 | 1.0370 | 1.0187 | 0.9631 | 0.8694 |
| HMM RV + Raw VRP | 1.0241 | 1.0188 | 1.0135 | 0.9974 | 0.9702 |
| Synthetic Pure VRP Proxy | 2.9144 | 2.9143 | 2.9141 | 2.9136 | 2.9127 |
| RSM RV | 0.8939 | 0.8734 | 0.8530 | 0.7917 | 0.6902 |
| RSM RV + Log VRP | 0.8215 | 0.8066 | 0.7917 | 0.7470 | 0.6720 |
| RSM RV + Raw VRP | 0.9924 | 0.9705 | 0.9486 | 0.8828 | 0.7730 |
| RSM Returns Only | 0.9534 | 0.9411 | 0.9287 | 0.8914 | 0.8290 |

The transaction-cost sensitivity shows that simple benchmarks are highly robust. The Sharpe ratios of the 60/40 and 1/N portfolios barely decline as transaction costs increase, because their turnover is low.

By contrast, regime-switching models are more sensitive to costs. The HMM RV + Log VRP model has the highest Sharpe ratio before costs, at 1.0553. At 10 bps, it remains competitive with a Sharpe ratio of 1.0187. However, at 25 bps and 50 bps, its Sharpe ratio falls materially.

This confirms that the model’s economic value depends on implementation frictions. Without turnover control, the HMM RV + Log VRP specification is less robust than the simple benchmarks.

The RSM models are even more sensitive to transaction costs, especially because they generate higher turnover. This makes them less attractive from an implementation perspective.

---

### 3.3 US transaction-cost sensitivity: maximum drawdown

| Strategy | 0 bps | 5 bps | 10 bps | 25 bps | 50 bps |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.1909 | -0.1909 | -0.1910 | -0.1913 | -0.1916 |
| 60/40 | -0.2005 | -0.2005 | -0.2006 | -0.2008 | -0.2012 |
| Buy-and-Hold Equity | -0.2393 | -0.2393 | -0.2393 | -0.2393 | -0.2393 |
| HMM RV | -0.1770 | -0.1774 | -0.1779 | -0.1793 | -0.1817 |
| HMM RV + Log VRP | -0.1657 | -0.1662 | -0.1667 | -0.1682 | -0.1708 |
| HMM RV + Raw VRP | -0.2198 | -0.2198 | -0.2198 | -0.2198 | -0.2198 |
| Synthetic Pure VRP Proxy | -0.0975 | -0.0975 | -0.0975 | -0.0975 | -0.0975 |
| RSM RV | -0.1539 | -0.1542 | -0.1567 | -0.1642 | -0.1767 |
| RSM RV + Log VRP | -0.2048 | -0.2068 | -0.2088 | -0.2147 | -0.2245 |
| RSM RV + Raw VRP | -0.1542 | -0.1543 | -0.1543 | -0.1645 | -0.1834 |
| RSM Returns Only | -0.1823 | -0.1830 | -0.1837 | -0.1858 | -0.1893 |

The drawdown results are more favorable to regime-switching models. HMM RV + Log VRP maintains a lower maximum drawdown than 60/40 and 1/N across all tested cost levels. At the baseline 10 bps cost, its maximum drawdown is -16.67%, compared with -20.06% for 60/40 and -19.10% for 1/N.

This reinforces the main interpretation: the value of the HMM RV + Log VRP model is not primarily higher return, but downside-risk reduction.

However, the model’s Sharpe sensitivity to costs means that drawdown improvement alone is not sufficient. Turnover control is required to make the strategy more defensible.

---

## 4. No-trade band sensitivity

### 4.1 Method

A no-trade band prevents rebalancing when the difference between current weights and target weights is small. This reduces unnecessary trading.

The tested no-trade bands are:

\[
0\%,\ 2\%,\ 5\%,\ 10\%
\]

The goal is to determine whether avoiding small trades improves the robustness of the regime-switching strategies.

---

### 4.2 No-trade band sensitivity: Sharpe ratio

| Strategy | 0% | 2% | 5% | 10% |
|---|---:|---:|---:|---:|
| HMM RV | 0.9874 | 0.9843 | 0.9928 | 0.9819 |
| HMM RV + Log VRP | 1.0188 | 1.0186 | 1.0221 | 1.0256 |
| HMM RV + Raw VRP | 1.0129 | 1.0130 | 1.0189 | 1.0101 |
| RSM RV | 0.8524 | 0.8523 | 0.8630 | 0.8484 |
| RSM RV + Log VRP | 0.7915 | 0.7924 | 0.7979 | 0.7966 |
| RSM RV + Raw VRP | 0.9479 | 0.9485 | 0.9517 | 0.9480 |
| RSM Returns Only | 0.9290 | 0.9358 | 0.9251 | 0.9524 |

The no-trade band results show modest improvements for some models. For HMM RV + Log VRP, the Sharpe ratio increases from 1.0188 with no band to 1.0256 with a 10% band.

This suggests that some small rebalancing decisions are not economically useful. Filtering them out can slightly improve performance.

However, the improvement is not large enough to change the main conclusion. The no-trade band helps, but it does not fully solve the turnover problem.

---

### 4.3 No-trade band sensitivity: average turnover

| Strategy | 0% | 2% | 5% | 10% |
|---|---:|---:|---:|---:|
| HMM RV | 0.1729 | 0.1662 | 0.1595 | 0.1535 |
| HMM RV + Log VRP | 0.2530 | 0.2461 | 0.2395 | 0.2353 |
| HMM RV + Raw VRP | 0.1007 | 0.0961 | 0.0947 | 0.0933 |
| RSM RV | 0.3265 | 0.3234 | 0.3125 | 0.2952 |
| RSM RV + Log VRP | 0.2448 | 0.2405 | 0.2350 | 0.2096 |
| RSM RV + Raw VRP | 0.3736 | 0.3715 | 0.3617 | 0.3459 |
| RSM Returns Only | 0.1568 | 0.1508 | 0.1442 | 0.1255 |

No-trade bands reduce turnover, but only moderately. For HMM RV + Log VRP, turnover falls from 25.30% to 23.53% when the band increases from 0% to 10%. This is an improvement, but turnover remains elevated.

This explains why the thesis places more emphasis on partial rebalancing than on no-trade bands. No-trade bands help filter small trades, but they do not sufficiently smooth large regime-driven allocation changes.

---

## 5. Partial rebalancing

### 5.1 Method

Partial rebalancing moves the portfolio only partially toward the target allocation.

The rule is:

\[
w_t^{final} = \lambda w_t^{target} + (1-\lambda) w_{t-1}^{portfolio}
\]

where \(\lambda\) is the adjustment speed.

The tested adjustment speeds are:

\[
0.10,\ 0.25,\ 0.50,\ 0.75,\ 1.00
\]

A value of \(\lambda = 1.00\) corresponds to full rebalancing. A lower value means that the strategy moves more gradually toward the model target.

---

### 5.2 Partial rebalancing: Sharpe ratio

| Strategy | 0.10 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| HMM RV | 0.9728 | 0.9634 | 0.9532 | 0.9642 | 0.9874 |
| HMM RV + Log VRP | 1.0196 | 1.0135 | 0.9935 | 1.0011 | 1.0188 |
| HMM RV + Raw VRP | 1.0108 | 0.9985 | 0.9894 | 0.9990 | 1.0129 |
| RSM RV | 0.9991 | 0.9837 | 0.9443 | 0.9011 | 0.8524 |
| RSM RV + Log VRP | 0.9256 | 0.8852 | 0.8402 | 0.8141 | 0.7915 |
| RSM RV + Raw VRP | 1.0062 | 0.9929 | 0.9800 | 0.9672 | 0.9479 |
| RSM Returns Only | 0.9618 | 0.9476 | 0.9288 | 0.9274 | 0.9290 |

The HMM RV + Log VRP model remains competitive across adjustment speeds. Its Sharpe ratio is 1.0135 at a partial rebalancing speed of 0.25, compared with 1.0188 under full rebalancing. The loss in Sharpe ratio is therefore small.

This is important because the main purpose of partial rebalancing is not to maximize Sharpe mechanically. Its purpose is to reduce turnover and improve implementability.

---

### 5.3 Partial rebalancing: average turnover

| Strategy | 0.10 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| HMM RV | 0.0389 | 0.0756 | 0.1183 | 0.1458 | 0.1729 |
| HMM RV + Log VRP | 0.0444 | 0.0910 | 0.1537 | 0.2035 | 0.2530 |
| HMM RV + Raw VRP | 0.0190 | 0.0382 | 0.0632 | 0.0826 | 0.1007 |
| RSM RV | 0.0358 | 0.0787 | 0.1527 | 0.2329 | 0.3265 |
| RSM RV + Log VRP | 0.0360 | 0.0756 | 0.1321 | 0.1848 | 0.2448 |
| RSM RV + Raw VRP | 0.0353 | 0.0810 | 0.1645 | 0.2589 | 0.3736 |
| RSM Returns Only | 0.0361 | 0.0672 | 0.1008 | 0.1276 | 0.1568 |

Partial rebalancing has a much stronger effect on turnover than no-trade bands. For HMM RV + Log VRP, turnover falls from 25.30% under full rebalancing to 9.10% with an adjustment speed of 0.25.

This makes the strategy materially more realistic.

The 0.10 adjustment speed reduces turnover further, but it may react too slowly to regime changes. The 0.25 specification therefore provides a better compromise between responsiveness and implementation control.

---

### 5.4 Partial rebalancing: maximum drawdown

| Strategy | 0.10 | 0.25 | 0.50 | 0.75 | 1.00 |
|---|---:|---:|---:|---:|---:|
| HMM RV | -0.1929 | -0.1837 | -0.1786 | -0.1787 | -0.1779 |
| HMM RV + Log VRP | -0.1917 | -0.1804 | -0.1734 | -0.1704 | -0.1668 |
| HMM RV + Raw VRP | -0.2210 | -0.2208 | -0.2204 | -0.2202 | -0.2199 |
| RSM RV | -0.1964 | -0.1857 | -0.1711 | -0.1601 | -0.1568 |
| RSM RV + Log VRP | -0.1892 | -0.1863 | -0.1914 | -0.1997 | -0.2088 |
| RSM RV + Raw VRP | -0.1993 | -0.1903 | -0.1782 | -0.1657 | -0.1544 |
| RSM Returns Only | -0.1865 | -0.1802 | -0.1779 | -0.1802 | -0.1837 |

For HMM RV + Log VRP, full rebalancing gives the best maximum drawdown, at approximately -16.68%. Partial rebalancing at 0.25 gives a maximum drawdown of -18.04%.

This is a reasonable trade-off. The strategy sacrifices some drawdown protection but reduces turnover substantially. Since the full-rebalancing model has high turnover, the partial-rebalancing version is more defensible as an implementable allocation strategy.

This supports the final US model selection:

> HMM RV + Log VRP with partial rebalancing speed 0.25 is the most defensible implementable US specification.

---

## 6. Crisis-period analysis

### 6.1 Purpose

The crisis analysis tests whether regime-switching strategies behave defensively during market stress.

This matters because the expected contribution of a regime-based model is not necessarily to increase average returns. Its main value may be to reduce drawdowns and losses during crises.

The tested crisis windows include:

- Eurozone Crisis;
- Covid Crisis;
- Inflation / Rate Shock;
- Volmageddon and late-cycle period;
- full aligned sample.

---

## 7. US crisis analysis

### 7.1 US crisis-period returns

| Strategy | Covid Crisis | Eurozone Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 0.0089 | 0.1217 | 2.3624 | -0.1533 | -0.0185 |
| 60/40 | 0.0014 | 0.1214 | 2.9599 | -0.1585 | -0.0235 |
| Buy-and-Hold Equity | -0.0317 | 0.1161 | 6.4140 | -0.1818 | -0.0457 |
| HMM RV + Log VRP, full | -0.0286 | 0.1094 | 2.4234 | -0.1429 | 0.0220 |
| HMM RV + Log VRP, partial 0.25 | -0.0310 | 0.0973 | 2.5904 | -0.1559 | -0.0168 |
| RSM RV + Raw VRP | -0.0442 | 0.1604 | 3.0815 | -0.0813 | -0.0087 |

During the US inflation and rate shock period, RSM RV + Raw VRP has the best period return, with a loss of only -8.13%. HMM RV + Log VRP full rebalancing also performs better than the traditional benchmarks during the same window.

During the Volmageddon and late-cycle period, HMM RV + Log VRP full rebalancing produces a positive return, while the traditional benchmarks are negative.

However, during the Covid Crisis, the HMM and RSM strategies do not clearly protect better than the benchmarks. This suggests that the regime signal is not uniformly effective across all crisis types.

---

### 7.2 US crisis maximum drawdown

| Strategy | Covid Crisis | Eurozone Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.0651 | -0.0618 | -0.1910 | -0.1605 | -0.0586 |
| 60/40 | -0.0771 | -0.0822 | -0.2006 | -0.1676 | -0.0741 |
| Buy-and-Hold Equity | -0.1249 | -0.1622 | -0.2393 | -0.2025 | -0.1353 |
| HMM RV + Log VRP, full | -0.0304 | -0.0486 | -0.1667 | -0.1399 | -0.0566 |
| HMM RV + Log VRP, partial 0.25 | -0.0735 | -0.0405 | -0.1804 | -0.1457 | -0.0714 |
| RSM RV + Raw VRP | -0.1010 | -0.0710 | -0.1543 | -0.1271 | -0.0708 |

The drawdown results are favorable for the US HMM strategy. HMM RV + Log VRP full rebalancing has lower drawdowns than the benchmarks during the Covid Crisis, Eurozone Crisis, full aligned sample and inflation shock period.

The partial rebalancing version gives up some crisis drawdown protection, but remains competitive on the full sample. It also remains more implementable because of lower turnover.

The RSM RV + Raw VRP model has the best full-sample drawdown, but its turnover remains high. This weakens its practical attractiveness.

---

### 7.3 US crisis Sharpe ratios

| Strategy | Covid Crisis | Eurozone Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|---:|
| 1/N Equity-Bond | 0.1894 | 1.0129 | 1.0253 | -1.0562 | -0.2229 |
| 60/40 | 0.1024 | 0.8438 | 1.0238 | -0.9767 | -0.2291 |
| Buy-and-Hold Equity | -0.0803 | 0.5135 | 0.9955 | -0.7570 | -0.2365 |
| HMM RV + Log VRP, full | -0.4610 | 0.9913 | 1.0187 | -1.4105 | 0.2784 |
| HMM RV + Log VRP, partial 0.25 | -0.3006 | 0.9989 | 1.0135 | -1.3870 | -0.1326 |
| RSM RV + Raw VRP | -0.2866 | 0.9343 | 0.9486 | -0.4292 | -0.0433 |

The US crisis Sharpe ratios are mixed. HMM RV + Log VRP is not universally superior across crisis windows. It performs well in drawdown terms, but not always in Sharpe terms.

This is consistent with the main thesis result: the model’s contribution is defensive and conditional, not universally dominant.

---

## 8. European crisis analysis

### 8.1 European crisis-period returns

| Strategy | Covid Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.0664 | 0.5158 | -0.1029 | -0.0745 |
| 60/40 | -0.0841 | 0.6190 | -0.0948 | -0.0872 |
| Buy-and-Hold Equity | -0.1702 | 1.0219 | -0.0660 | -0.1368 |
| HMM RV | -0.2346 | 0.1068 | -0.1659 | -0.1121 |
| HMM RV + Log VRP | -0.2346 | 0.0818 | -0.1687 | -0.1121 |
| RSM RV | -0.2063 | 0.4270 | -0.1293 | -0.1109 |
| RSM RV + Log VRP | -0.2068 | 0.3519 | -0.1344 | -0.1109 |
| RSM RV + Raw VRP | -0.2063 | 0.2240 | -0.2152 | -0.1099 |
| RSM Returns Only | -0.2053 | 0.4332 | -0.1096 | -0.1131 |

The European crisis-period returns confirm the weakness of the regime-switching models. During the Covid Crisis, the HMM and RSM models lose more than the 1/N and 60/40 benchmarks.

During the full aligned sample, Buy-and-Hold Equity, 60/40 and 1/N all outperform the regime models in period-return terms.

This confirms that the European VRP-based framework does not produce robust defensive value.

---

### 8.2 European crisis maximum drawdown

| Strategy | Covid Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.1713 | -0.2034 | -0.1944 | -0.0684 |
| 60/40 | -0.2050 | -0.2090 | -0.2003 | -0.0821 |
| Buy-and-Hold Equity | -0.3397 | -0.3397 | -0.2261 | -0.1355 |
| HMM RV | -0.2722 | -0.3197 | -0.2325 | -0.1090 |
| HMM RV + Log VRP | -0.2722 | -0.3110 | -0.2350 | -0.1090 |
| RSM RV | -0.2692 | -0.2692 | -0.2448 | -0.1077 |
| RSM RV + Log VRP | -0.2695 | -0.2695 | -0.2471 | -0.1077 |
| RSM RV + Raw VRP | -0.2417 | -0.2815 | -0.2680 | -0.1067 |
| RSM Returns Only | -0.2686 | -0.2686 | -0.2331 | -0.1099 |

The European drawdown analysis confirms that the simple equity-bond benchmarks remain superior. The 1/N portfolio has a full-sample maximum drawdown of -20.34%, while HMM RV + Log VRP has a drawdown of -31.10%.

The regime-switching models reduce drawdown relative to buy-and-hold equity in some cases, but they do not improve on 60/40 or 1/N.

This is an important distinction. A model does not add enough value if it only beats the riskiest benchmark but fails to beat simple diversified portfolios.

---

### 8.3 European crisis Sharpe ratios

| Strategy | Covid Crisis | Full aligned sample | Inflation Rate Shock | Volmageddon and late cycle |
|---|---:|---:|---:|---:|
| 1/N Equity-Bond | -0.3654 | 0.4539 | -0.6308 | -1.5144 |
| 60/40 | -0.3657 | 0.4590 | -0.4928 | -1.5498 |
| Buy-and-Hold Equity | -0.3646 | 0.4629 | -0.1477 | -1.5930 |
| HMM RV | -1.1994 | 0.1455 | -1.2559 | -1.5815 |
| HMM RV + Log VRP | -1.1994 | 0.1281 | -1.2633 | -1.5814 |
| RSM RV | -0.9706 | 0.3187 | -0.6117 | -1.5875 |
| RSM RV + Log VRP | -0.9729 | 0.2822 | -0.6499 | -1.5895 |
| RSM RV + Raw VRP | -1.1906 | 0.2233 | -1.5689 | -1.5869 |
| RSM Returns Only | -0.9662 | 0.3219 | -0.4812 | -1.7151 |

The European Sharpe results are clearly unfavorable to the regime-switching models. The HMM strategies have materially weaker Sharpe ratios than the benchmarks during the full aligned sample and most crisis windows.

This confirms that the European results are not merely weaker because of one metric. They are weak across returns, Sharpe ratios and drawdowns.

---

## 9. Robustness conclusion

The robustness analysis leads to four conclusions.

First, transaction costs matter. Regime-switching models are more sensitive to costs than simple benchmarks because they generate higher turnover.

Second, no-trade bands provide only moderate improvement. They reduce turnover slightly, but they do not fully solve the implementation problem.

Third, partial rebalancing is the most useful implementation adjustment. It materially reduces turnover while preserving competitive performance. For the US HMM RV + Log VRP model, partial rebalancing speed 0.25 is the best compromise between performance, drawdown control and turnover.

Fourth, crisis analysis confirms that the US model has defensive value mainly through drawdown control. However, the crisis results are not uniformly dominant across all windows. In Europe, crisis analysis confirms that regime-switching models do not add enough value relative to simple benchmarks.

The final robustness conclusion is:

> The US HMM RV + Log VRP model is economically defensible only when implemented with turnover control. The European regime-switching results remain weak even after robustness analysis.

---

## 10. Chapter conclusion

This chapter tested whether the empirical results survive implementation constraints.

The results show that the US HMM RV + Log VRP model has useful defensive properties, especially in maximum drawdown terms. However, full rebalancing produces high turnover. Partial rebalancing materially improves the strategy’s implementability and leads to the selection of HMM RV + Log VRP with adjustment speed 0.25 as the most defensible US specification.

The European results are materially weaker. Regime-switching models do not outperform simple benchmarks in the main sample or during crisis periods. This confirms that the VRP signal is not robustly transferable across markets.

The next chapter discusses the limitations of the thesis and explains why the final conclusion must remain conditional rather than universal.

---

# Chapter 5 — Limitations and Conclusion

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
