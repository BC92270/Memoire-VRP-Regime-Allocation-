# Literature Positioning

## 1. Objective of the literature positioning

This thesis is positioned at the intersection of four strands of literature:

1. the Variance Risk Premium and variance swap literature;
2. the predictive content of volatility and variance risk premia;
3. regime-switching models and dynamic asset allocation;
4. benchmark allocation and the difficulty of beating simple diversified portfolios.

The contribution of the thesis is not to claim that the Variance Risk Premium is a universal standalone return factor. Instead, the thesis studies whether VRP is more useful as an informational state variable for regime detection and portfolio allocation.

The empirical results show a clear cross-market asymmetry:

- in the US, VRP-enhanced HMM models improve downside-risk management and remain competitive with 60/40 and 1/N benchmarks;
- in Europe, VRP-enhanced HMM and RSM models fail to outperform simple benchmarks;
- the synthetic pure VRP proxy performs very strongly in the US but collapses in Europe.

This positions the thesis as a conditional and comparative study of VRP-based allocation.

---

## 2. Variance Risk Premium literature

### 2.1 Definition of the Variance Risk Premium

The Variance Risk Premium is generally defined as the difference between the risk-neutral expectation of future variance and the physical expectation of realized variance.

In simplified empirical form, the proxy is:

\[
VRP_t = IV_t - RV_t
\]

where:

- \(IV_t\) is implied variance, inferred from option prices or volatility indices;
- \(RV_t\) is realized variance, estimated from historical returns.

Carr and Wu (2009) provide a central reference for the measurement of variance risk premia across assets. Their framework links the variance risk premium to variance swap rates and realized variance. This is important because it gives the VRP a direct derivatives-market interpretation: it represents compensation for bearing variance risk.

In this thesis, the VRP is not observed from OTC variance swap data. Instead, it is proxied using volatility-index data:

- VIX for the US;
- VSTOXX for Europe.

The proxy approach is empirically practical but imperfect. This is why the thesis distinguishes between:

1. direct synthetic VRP exposure;
2. using VRP as an informational signal inside regime models.

### 2.2 Why the VRP should exist

The VRP exists because investors are generally willing to pay for protection against volatility spikes and market crashes. Option sellers demand compensation for providing this insurance. As a result, implied variance tends to exceed subsequently realized variance on average.

This mechanism is closely related to:

- crash insurance demand;
- volatility risk aversion;
- option-market risk premia;
- hedging pressure;
- intermediary risk-bearing capacity.

Bakshi and Kapadia (2003) provide evidence using delta-hedged option portfolios. Their results connect option returns and the sign of the volatility risk premium, supporting the idea that investors pay a premium for volatility protection.

This literature justifies the first part of the thesis question:

> Does direct exposure to the variance premium create economic value?

However, direct exposure is not straightforward. A true variance swap strategy requires option replication, contract rolling, liquidity assumptions, margin assumptions and transaction-cost modelling. This motivates the thesis decision to treat the pure VRP proxy as exploratory rather than fully tradable.

---

## 3. Predictive content of the VRP

Bollerslev, Tauchen and Zhou (2009) show that the difference between implied and realized variation contains information about future stock returns. This is central for the thesis because it shifts the interpretation of VRP from a pure derivatives return factor to a predictive state variable.

The logic is:

\[
IV_t - RV_t
\]

may contain information about:

- investors’ fear of future volatility;
- market stress pricing;
- risk aversion;
- crash-protection demand;
- expected equity compensation.

This thesis builds on that idea but applies it to dynamic allocation rather than pure return prediction.

The practical question becomes:

> Can VRP help detect whether the market is in a normal or stress regime?

This is why the empirical framework includes features such as:

- realized variance;
- implied variance;
- raw VRP;
- log implied-to-realized variance ratio.

The log ratio is especially useful:

\[
\log\left(\frac{IV_t}{RV_t}\right)
\]

because it captures the relative spread between implied and realized variance and reduces some scale instability.

---

## 4. Regime-switching literature

### 4.1 Hamilton and Markov-switching models

Hamilton (1989) provides the foundational econometric framework for regime-switching time series. In this framework, model parameters depend on an unobserved latent state that follows a Markov process.

This is relevant for financial markets because returns, volatility and correlations are not stable through time. Markets alternate between different states, such as:

- calm expansion;
- high-volatility correction;
- crisis;
- recovery;
- late-cycle fragility.

A linear model with constant parameters may fail to capture these changes. Regime-switching models allow the investment process to respond to latent market states.

### 4.2 HMM as a regime-detection tool

Hidden Markov Models are useful when the state of the market is not directly observable. The model estimates the probability that the market is in each latent state.

In this thesis, the HMM uses observable features such as equity returns, realized variance and VRP proxies to estimate a stress probability.

The allocation rule is then:

\[
w^{eq}_t = 0.80(1 - p^{stress}_t) + 0.20p^{stress}_t
\]

This means:

- when the stress probability is low, the strategy holds more equity;
- when the stress probability is high, the strategy reduces equity exposure and moves toward bonds.

This connects the VRP literature to a practical allocation mechanism.

### 4.3 Regime-switching and asset allocation

Ang and Bekaert (2002) show that regime shifts matter for international asset allocation, especially because correlations and volatilities tend to rise in bad states. This is important because diversification can become less effective precisely when investors need it most.

Guidolin and Timmermann (2007) extend the regime-switching asset-allocation literature by showing that stock and bond returns can be described by several regimes and that optimal allocations vary substantially across states.

This thesis follows the same broad logic:

> If asset-return distributions change across regimes, portfolio weights should also change across regimes.

However, the thesis differs in one important way. Instead of relying only on returns and volatility, it explicitly tests whether the Variance Risk Premium improves regime identification and allocation.

---

## 5. Benchmark literature and the difficulty of outperforming simple rules

A key methodological choice in this thesis is to compare regime-switching strategies against simple benchmarks:

- buy-and-hold equity;
- 60/40 equity-bond portfolio;
- 1/N equity-bond allocation.

This is important because complex models can appear attractive in isolation but fail to outperform simple robust allocation rules.

DeMiguel, Garlappi and Uppal (2009) show that many optimized portfolio models fail to consistently beat the naive 1/N rule out of sample. Their result is highly relevant for this thesis because regime-switching models also face estimation error, turnover and model instability.

The empirical results of this thesis are consistent with that warning.

In the US:

- HMM RV + Log VRP improves drawdown;
- but 60/40 and 1/N remain extremely competitive in Sharpe ratio.

In Europe:

- simple benchmarks dominate the regime-switching strategies.

This strengthens the credibility of the thesis because it avoids overstating the value of complex models.

---

## 6. Positioning of the thesis relative to the literature

The literature shows that:

1. VRP is a meaningful risk premium related to variance swap pricing and option-market compensation.
2. VRP contains predictive information about future equity-market conditions.
3. Regime-switching models are useful for modelling time-varying investment opportunities.
4. Simple allocation rules such as 60/40 and 1/N are difficult to beat out of sample.

This thesis connects these ideas into one empirical framework.

The thesis asks:

> Is VRP more useful as a directly traded premium or as an informational regime signal?

The answer from the empirical analysis is conditional.

In the US, VRP has useful informational content. HMM models using realized variance and log VRP deliver competitive risk-adjusted performance and improve maximum drawdown. However, they do not clearly dominate 60/40 and 1/N in Sharpe ratio.

In Europe, the same framework does not produce robust value. The HMM and RSM models are technically feasible but economically weak relative to simple benchmarks.

Therefore, the thesis contributes to the literature by showing that:

- VRP is not a universal standalone return engine;
- VRP can be useful as a regime-state variable;
- the economic value of VRP is market-dependent;
- implementation frictions and turnover matter materially;
- cross-market replication is essential before claiming robustness.

---

## 7. Literature gap addressed by the thesis

The existing literature often studies the VRP in one of two ways:

1. as a priced risk premium in option and variance swap markets;
2. as a predictor of future returns.

This thesis studies a slightly different question:

> Can VRP improve dynamic allocation by helping identify market regimes?

The thesis also adds a cross-market comparison between the US and Europe.

This is important because a signal that works in the US may not be robust in another market. The European results show that the VRP signal is not mechanically transferable.

The gap addressed is therefore:

> The thesis evaluates the economic value of VRP as a regime-allocation signal across markets, while explicitly comparing it against simple robust benchmarks and implementation constraints.

---

## 8. Contribution to the literature

The contribution can be summarized in five points.

### 8.1 VRP as a conditional signal

The thesis supports the idea that VRP should be treated as a conditional state variable, not as a universal return factor.

### 8.2 Downside-risk management

In the US, the main value of VRP-enhanced HMM models is drawdown reduction rather than unconditional Sharpe improvement.

### 8.3 Cross-market instability

The contrast between US and Europe shows that VRP-based allocation is market-dependent.

### 8.4 Benchmark discipline

The results confirm that simple benchmarks such as 60/40 and 1/N remain difficult to beat.

### 8.5 Implementation realism

The thesis incorporates turnover, transaction costs, partial rebalancing and crisis-period analysis, which makes the empirical framework more realistic than a purely theoretical signal test.

---

## 9. How the empirical results relate to the literature

The US results are consistent with the literature suggesting that VRP contains useful information about market risk and future returns. However, the fact that the model mainly improves drawdown rather than clearly improving Sharpe ratio suggests that VRP is especially useful for defensive allocation.

The European results qualify the literature. They show that the informational value of VRP is not automatic. Differences in volatility-index construction, option-market depth, investor hedging demand and market structure may affect whether the VRP signal is exploitable.

The strong difference between the US and European synthetic pure VRP proxy also reinforces the need for caution. A proxy that works in one market can fail in another.

Therefore, the thesis does not reject the VRP literature. It refines it:

> VRP may be informative, but its economic value depends on the market, the model, the transformation, the benchmark and the implementation assumptions.

---

## 10. Key references

### Variance Risk Premium and volatility risk

- Bakshi, G., & Kapadia, N. (2003). Delta-Hedged Gains and the Negative Market Volatility Risk Premium. The Review of Financial Studies, 16(2), 527-566.
- Carr, P., & Wu, L. (2009). Variance Risk Premiums. The Review of Financial Studies, 22(3), 1311-1341.
- Bollerslev, T., Tauchen, G., & Zhou, H. (2009). Expected Stock Returns and Variance Risk Premia. The Review of Financial Studies, 22(11), 4463-4492.

### Regime-switching and dynamic allocation

- Hamilton, J. D. (1989). A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle. Econometrica, 57(2), 357-384.
- Ang, A., & Bekaert, G. (2002). International Asset Allocation with Regime Shifts. The Review of Financial Studies, 15(4), 1137-1187.
- Guidolin, M., & Timmermann, A. (2007). Asset Allocation under Multivariate Regime Switching. Journal of Economic Dynamics and Control, 31(11), 3503-3544.

### Benchmark allocation

- DeMiguel, V., Garlappi, L., & Uppal, R. (2009). Optimal versus Naive Diversification: How Inefficient is the 1/N Portfolio Strategy? The Review of Financial Studies, 22(5), 1915-1953.

---

## 11. Final positioning statement

This thesis is positioned between the variance risk premium literature and the regime-switching asset-allocation literature.

It does not claim that VRP is universally profitable as a direct trading strategy. Instead, it argues that VRP may be more useful as a regime-state variable for downside-risk management.

The empirical evidence supports this conclusion in the US but not in Europe. This cross-market asymmetry is the main contribution of the thesis.

The final positioning is:

> The Variance Risk Premium is best understood as a conditional market-state signal whose economic value depends on market structure, model specification and implementation frictions.