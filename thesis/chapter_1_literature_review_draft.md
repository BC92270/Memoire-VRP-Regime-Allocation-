# Chapter 1 — Literature Review Draft

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