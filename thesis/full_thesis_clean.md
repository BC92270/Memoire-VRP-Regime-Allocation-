# Introduction

## 1. General context

Financial markets alternate between periods of relative stability, gradual repricing, volatility shocks and severe stress. These changes matter for portfolio construction because the return distribution of risky assets is not constant through time. An allocation rule that performs well during a low-volatility expansion may become inappropriate during a liquidity shock, an abrupt increase in risk aversion or a persistent inflationary regime.

Traditional portfolios such as buy-and-hold equity, 60/40 equity–bond allocation and equal-weighted equity–bond allocation remain important reference points. They are transparent, inexpensive and difficult to outperform out of sample. However, they do not explicitly adapt their risk exposure to changes in market conditions.

This motivates the study of forward-looking indicators that may contain information about future stress. Volatility-related variables are natural candidates. Realized variance measures the variation that has already occurred, whereas option-implied variance reflects the market price of future volatility and crash protection. The difference between these quantities is commonly associated with the Variance Risk Premium.

---

## 2. Variance Risk Premium and economic intuition

The Variance Risk Premium can be represented empirically as the difference between implied variance and realized variance:

\[
VRP_t = IV_t - RV_t
\]

where \(IV_t\) denotes an implied-variance proxy and \(RV_t\) denotes a realized-variance measure.

A positive variance premium is economically intuitive. Investors frequently demand insurance against market crashes, volatility spikes and nonlinear losses. This demand raises the price of option-based protection and can cause implied variance to exceed subsequently realized variance. Investors who sell volatility protection may therefore earn a premium in normal periods, while remaining exposed to infrequent but severe losses when realized variance rises sharply.

The Variance Risk Premium can consequently be used through two distinct channels.

The first channel is informational. VRP-related variables may help identify latent market states or forecast future stress. In this interpretation, the VRP is an input to a Hidden Markov Model, a Markov-switching regression or a machine-learning classifier. The estimated state probability is then translated into a dynamic equity–bond allocation.

The second channel is a payoff channel. Instead of using the VRP only to change asset weights, an investor attempts to harvest the spread between implied and subsequently realized variance. In this thesis, that channel is studied through a model-based direct variance-payoff approximation.

These two channels must not be conflated. A variable can contain predictive information without generating an attractive standalone payoff. Conversely, a payoff can exhibit positive carry even when the same variable adds little value to an equity–bond allocation model.

---

## 3. Research problem

The central research problem is:

> Does the Variance Risk Premium create more economic value when it is harvested through a model-based direct variance-payoff approximation or when it is used as an informational signal inside regime-based equity–bond allocation models?

This question is more precise than asking whether the Variance Risk Premium exists. The empirical existence of a positive average spread between implied and realized variance does not automatically establish that it can be transformed into robust portfolio welfare.

Three separate questions must be addressed.

First, does the inclusion of VRP variables improve the performance of dynamic allocation models relative to strong and inexpensive benchmarks?

Second, does an approximation of direct variance carry generate attractive risk-adjusted returns after strictly lagged risk targeting, notional caps and monthly roll costs?

Third, are the conclusions stable across the United States and Europe?

The distinction between the signal channel and the payoff channel is the core organizing principle of the thesis.

---

## 4. Research gap

The literature on variance risk premia has established that option-implied variance often exceeds subsequently realized variance and that volatility-related variables can contain information about risk aversion, future returns and crash risk.

A separate literature studies regime-dependent portfolio allocation using Hidden Markov Models, Markov-switching regressions and, more recently, machine-learning classifiers.

However, these two research areas are often examined separately. Studies of the Variance Risk Premium commonly focus on derivative pricing, variance-swap returns or return prediction. Studies of regime allocation frequently use volatility or macroeconomic variables without directly comparing the economic value of the informational channel with the value of a variance-linked payoff.

This thesis links the two literatures by evaluating:

1. VRP as an explanatory and predictive state variable;
2. VRP as the basis of a model-based direct variance-payoff approximation;
3. the welfare implications of both approaches;
4. the cross-market stability of the results.

The analysis also imposes benchmark discipline. Complex strategies are compared with buy-and-hold equity, 60/40 and equal-weighted equity–bond portfolios rather than being evaluated only in isolation.

---

## 5. Research question and sub-questions

The principal research question is:

> Does the Variance Risk Premium create more economic value through direct variance carry or through its informational content for dynamic asset allocation?

The analysis is structured around the following sub-questions:

1. Do VRP-enhanced HMM and RSM specifications outperform simple equity–bond benchmarks?
2. Do machine-learning models extract incremental stress-prediction information from VRP-related variables?
3. Does a model-based direct short-variance payoff produce attractive risk-adjusted performance?
4. Do welfare gains remain statistically significant under block-bootstrap inference?
5. Are the conclusions stable across transaction costs, volatility-estimation windows, notional caps, subperiods and risk-aversion levels?
6. Are the results consistent between the United States and Europe?
7. Does the economic value of VRP depend more on the information contained in the variable or on the payoff structure used to harvest it?

---

## 6. Hypotheses

### Hypothesis 1 — Positive variance carry with negative skewness

Implied variance is expected to exceed subsequently realized variance in a majority of observations. A short-variance payoff should therefore generate frequent positive carry, combined with negatively skewed and occasionally severe losses.

### Hypothesis 2 — Limited allocation-model dominance

VRP-related variables may improve stress identification or downside-risk control, but HMM, RSM and machine-learning allocation strategies are not expected to dominate simple equity–bond benchmarks consistently after turnover and implementation costs.

### Hypothesis 3 — Payoff-structure dependence

The economic value of the Variance Risk Premium is expected to depend on the mechanism through which it is monetized. Direct variance exposure may produce results that differ materially from those obtained when VRP is used only as an allocation feature.

### Hypothesis 4 — Cross-market heterogeneity

The strength and economic value of the variance premium are expected to differ between the United States and Europe because of differences in option-market structure, volatility-index construction, sample composition and crisis dynamics.

### Hypothesis 5 — Importance of implementation constraints

Headline performance is expected to weaken when realistic implementation controls are imposed. Transaction costs, rolling of monthly exposure, risk-estimation windows, notional constraints and tail losses are therefore central to the evaluation.

---

## 7. Empirical architecture

The empirical framework contains two distinct layers.

### 7.1 Equity–bond allocation layer

The allocation layer compares:

- Buy-and-Hold Equity;
- 60/40 Equity–Bond;
- 1/N Equity–Bond;
- Hidden Markov Model strategies;
- Markov-switching regression strategies;
- machine-learning stress-classification strategies.

The HMM and RSM models estimate latent stress probabilities. These probabilities are translated into bounded equity and bond weights. Machine-learning classifiers provide an additional nonlinear prediction layer.

The allocation models are evaluated on aligned rolling out-of-sample periods:

| Market | Allocation observations |
|---|---:|
| United States | 184 |
| Europe | 122 |

### 7.2 Direct variance-payoff layer

The direct-variance layer approximates the payoff from selling one-month variance exposure.

The strike proxy is lagged implied variance:

\[
K^{var}_{t} = IV_{t-1}
\]

The settlement proxy is the realized-variance measure observed at \(t\):

\[
RV^{settlement}_{t} = RV_t
\]

The short-variance payoff is:

\[
\Pi^{short}_{t}
=
K^{var}_{t}
-
RV^{settlement}_{t}
\]

The normalized payoff is:

\[
\widetilde{\Pi}^{short}_{t}
=
\frac{
K^{var}_{t}
-
RV^{settlement}_{t}
}{
K^{var}_{t}
}
\]

Exposure is sized using lagged estimates of payoff volatility and is capped by a maximum absolute notional. Transaction costs are charged on the full absolute notional entered each month because the one-month exposure settles and must be renewed.

The final direct-variance strategy samples are:

| Market | Direct-variance observations |
|---|---:|
| United States | 232 |
| Europe | 170 |

The allocation and direct-variance layers must not be ranked mechanically because they use different samples and payoff constructions.

---

## 8. Main empirical results

### 8.1 Equity–bond allocation

The allocation results do not establish robust dominance by complex models.

In the United States, the strongest HMM specification is HMM RV + Log VRP. It achieves an annualized return of 8.36%, volatility of 8.24% and a Sharpe ratio of 1.019. The equal-weighted equity–bond benchmark produces a Sharpe ratio of 1.025. The HMM improves maximum drawdown to −16.67%, compared with −19.10% for equal weighting, but its turnover is substantially higher.

The strongest US machine-learning allocation strategy is the Logistic Base model, with a Sharpe ratio of 1.002. Its performance does not establish benchmark dominance.

In Europe, the strongest HMM or RSM specification is RSM RV + Raw VRP, with a Sharpe ratio of 0.281. Buy-and-hold equity reaches 0.313, while the 60/40 and equal-weighted portfolios reach 0.292 and 0.280 respectively. The European Random Forest with VRP produces incremental predictive content but no statistically significant welfare advantage.

The informational channel is therefore economically relevant but limited. VRP variables modify regime probabilities and may improve particular risk dimensions, yet they do not generate consistent superiority over simple portfolios.

### 8.2 Direct variance carry

The direct-variance evidence differs substantially across markets.

In the United States, the highest-Sharpe specification is Direct Short Variance 10% Vol with a High-VRP filter. It generates:

- annualized return: 6.23%;
- annualized volatility: 7.17%;
- Sharpe ratio: 0.882;
- Sortino ratio: 1.218;
- maximum drawdown: −23.46%.

At a risk-aversion coefficient of five, its mean–variance certainty equivalent is below both 60/40 and equal-weighted allocation. The bootstrap confidence intervals contain zero, so no statistically significant welfare dominance is established.

In Europe, the strongest specification is Direct Short Variance 10% Vol with exposure restricted to periods in which the lagged VRP is positive. It generates:

- annualized return: 13.08%;
- annualized volatility: 9.70%;
- Sharpe ratio: 1.324;
- Sortino ratio: 1.891;
- maximum drawdown: −21.36%.

At a risk-aversion coefficient of five, the strategy produces a mean–variance certainty equivalent of approximately 10.49%. Its advantage is approximately 927 basis points relative to 60/40 and 899 basis points relative to equal weighting. The lower bootstrap confidence bounds remain positive against both benchmarks.

### 8.3 Robustness

The European direct-variance result remains economically strong under:

- transaction costs from 0 to 50 basis points;
- volatility-estimation windows from 12 to 60 months;
- a maximum notional cap reduced to 5%;
- first-half and second-half subsamples;
- pre-Covid and post-Covid subsamples;
- risk-aversion coefficients from 1 to 10;
- exclusion of major crisis windows.

The US result is less stable. It is particularly sensitive to short volatility-estimation windows and does not produce consistent welfare gains relative to traditional benchmarks.

---

## 9. Main contribution

The principal contribution of the thesis is not the identification of a universally superior VRP strategy.

The contribution is the empirical separation of three mechanisms:

1. VRP as a latent-state variable in HMM and RSM allocation;
2. VRP as an input to machine-learning stress classification;
3. VRP as the basis of a model-based direct variance-payoff approximation.

The results show that predictive content and economic value are not equivalent. A variable may improve classification without producing portfolio welfare. Conversely, a variance-linked payoff may generate strong economic performance even when VRP adds little value to a conventional equity–bond regime model.

The main result is therefore:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested.

This conclusion is stronger and more precise than claiming that the VRP is universally superior either as a state variable or as a direct return factor.

---

## 10. Methodological boundary

The direct-variance extension is not a reconstructed variance-swap backtest.

It does not include:

- a strike calculated from the complete option surface;
- exact contract maturity matching;
- daily mark-to-market;
- collateral remuneration;
- margin calls;
- dealer bid–ask spreads;
- counterparty credit risk;
- crisis-time market impact;
- exact variance-notional conventions.

The normalized payoff is not an observed return on invested capital. The risk-targeted strategy return is a synthetic mapping from a variance payoff to portfolio capital.

Accordingly, the expressions “actual variance-swap return”, “tradable variance-swap performance” or equivalent language are not used.

---

## 11. Structure of the thesis

Chapter 1 reviews the literature on the Variance Risk Premium, volatility risk premia, variance-linked payoffs, regime-switching models, machine-learning classification and benchmark portfolio allocation.

Chapter 2 presents the data and methodology. It distinguishes the allocation layer from the direct variance-payoff layer and explains the rolling estimation, risk targeting, transaction costs, welfare measures and bootstrap procedures.

Chapter 3 presents the empirical results for the United States and Europe. It compares benchmarks, HMM, RSM, machine-learning and direct-variance strategies while preserving the distinction between evidence layers.

Chapter 4 examines robustness and implementation. It studies transaction costs, volatility-estimation windows, notional caps, subperiod stability, crisis exclusions and risk-aversion sensitivity.

Chapter 5 discusses data, modelling, statistical and implementation limitations and provides the final answer to the research question.

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

This chapter presents the data, variable construction, model specifications, portfolio rules and statistical procedures used in the empirical analysis.

The methodology is organized around two distinct evidence layers:

1. an equity–bond allocation layer;
2. a model-based direct variance-payoff layer.

The allocation layer evaluates whether Variance Risk Premium variables improve dynamic portfolio decisions when used inside Hidden Markov Models, Markov-switching regressions and machine-learning classifiers.

The direct-variance layer evaluates whether a payoff linked more directly to the difference between implied and subsequently realized variance generates economic value.

These layers must remain conceptually separate. They use different payoff structures, different aligned samples and different implementation assumptions. Their results can be interpreted jointly, but they must not be ranked mechanically as if they represented identical investment opportunities.

---

## 2. Markets and data

### 2.1 United States

The United States is represented by three financial series:

| Economic component | Proxy | Empirical role |
|---|---|---|
| Equity market | SPY / S&P 500 | Risky asset and return feature |
| Implied volatility | VIX | Implied-variance proxy |
| Bond market | AGG | Defensive asset |

SPY provides the equity price series used to compute daily and monthly equity returns.

The VIX is converted into an annualized implied-variance proxy.

AGG provides the defensive bond return used in the benchmark and dynamic equity–bond portfolios.

The final United States monthly feature dataset contains 257 observations. After the 72-month rolling-estimation requirement and one-step-ahead alignment, the allocation comparison contains 184 out-of-sample observations.

The direct-variance payoff panel contains 256 valid settlement observations. After the minimum lagged-risk-estimation requirements and common-strategy alignment, the direct-variance strategy comparison contains 232 observations.

### 2.2 Europe

Europe is represented by:

| Economic component | Proxy | Empirical role |
|---|---|---|
| Equity market | EURO STOXX 50 | Risky asset and return feature |
| Implied volatility | VSTOXX / V2TX | Implied-variance proxy |
| Bond market | IEAG.AS | Defensive asset |

The European implied-volatility series is reconstructed in the local file:

`data/raw/vstoxx.csv`

The reconstruction combines historical VSTOXX observations with a continuation series. Date strings written in ISO format are parsed explicitly as year-month-day. This prevents European dates such as `2017-01-03` from being incorrectly interpreted under a day-first convention.

After alignment of the equity, volatility and bond components, the European daily feature panel contains 4,041 processed observations. The monthly dataset contains 195 observations.

After rolling estimation and one-step-ahead alignment, the European allocation comparison contains 122 out-of-sample observations.

The direct-variance payoff panel contains 194 valid settlement observations. After lagged-risk estimation and common-strategy alignment, the direct-variance strategy comparison contains 170 observations.

### 2.3 Calendar-gap protection

Daily equity and bond returns are computed only when consecutive prices are separated by no more than seven calendar days.

Let \(P_d\) denote a daily price. The daily log return is:

\[
r_d
=
\log
\left(
\frac{P_d}{P_{d-1}}
\right)
\]

When the calendar gap between \(d-1\) and \(d\) exceeds seven days, the corresponding return is set to missing.

This rule prevents a price movement spanning several weeks or months from being treated as a one-day return. It also forces rolling realized-variance calculations to restart after major interruptions in the source data.

---

## 3. Frequency and monthly aggregation

The raw inputs are daily.

Daily observations are required to construct realized variance and to preserve the timing of implied-volatility information.

Portfolio allocation and strategy evaluation are performed at monthly frequency.

At each month-end:

- the final valid equity price is retained;
- the final valid bond price is retained;
- the final daily volatility features are retained;
- monthly equity and bond holding-period returns are calculated from month-end prices.

For asset \(i\), the monthly simple return is:

\[
R_{i,t}
=
\frac{P_{i,t}}
     {P_{i,t-1}}
-
1
\]

Monthly frequency is appropriate for strategic allocation and reduces noise and excessive rebalancing. It nevertheless means that the analysis does not reproduce daily derivative mark-to-market or intramonth trading decisions.

---

## 4. Realized variance

### 4.1 Daily log returns

Daily realized variance is constructed from equity log returns:

\[
r_d
=
\log
\left(
\frac{P_d}{P_{d-1}}
\right)
\]

### 4.2 Twenty-one-observation rolling measure

The annualized realized-variance proxy is:

\[
RV_d
=
\frac{252}{21}
\sum_{j=0}^{20}
r_{d-j}^{2}
\]

The measure therefore uses the most recent 21 valid daily observations and annualizes their sum of squared log returns.

This is not an exact calendar-month realized-variance measure. It is a trailing 21-observation estimate sampled at month-end.

The distinction matters for interpretation. In particular, the settlement variable used in the direct-variance extension represents the annualized trailing realized variance observed at the settlement month-end, rather than the exact realized variance accumulated between two contractual variance-swap dates.

### 4.3 Log realized variance

A log transformation is also constructed:

\[
\log RV_t
=
\log
\left(
\max(RV_t,\varepsilon)
\right)
\]

where \(\varepsilon\) is a small positive numerical floor.

The transformation reduces scale asymmetry and improves numerical stability in the regime and machine-learning models.

---

## 5. Implied variance

Let \(V_t\) denote the VIX or VSTOXX index level expressed in volatility percentage points.

Annualized implied variance is approximated by:

\[
IV_t
=
\left(
\frac{V_t}{100}
\right)^2
\]

For example, a volatility-index level of 20 corresponds to an implied-volatility estimate of 20% and an implied-variance estimate of:

\[
0.20^2
=
0.04
\]

The volatility index is treated as an implied-variance proxy. It is not identical to an exact variance-swap strike because the thesis does not reconstruct the full option surface or the precise static replication portfolio.

A log implied-variance feature is also calculated:

\[
\log IV_t
=
\log
\left(
\max(IV_t,\varepsilon)
\right)
\]

---

## 6. Variance Risk Premium variables

### 6.1 Raw VRP proxy

The raw Variance Risk Premium proxy is:

\[
VRP_t
=
IV_t
-
RV_t
\]

A positive value means that current implied variance exceeds the trailing realized-variance measure.

A negative value means that realized variance is above implied variance.

For the allocation models, this is an informational feature observed at month-end. It is not itself treated as an observed derivative return.

### 6.2 Log implied-to-realized variance ratio

The relative transformation is:

\[
LogVRP_t
=
\log
\left(
\frac{IV_t}{RV_t}
\right)
\]

This measure is positive when implied variance exceeds realized variance and negative in the opposite case.

Compared with the raw difference, the log ratio:

- expresses the spread proportionally;
- reduces sensitivity to the absolute variance level;
- provides a more symmetric feature;
- can improve numerical behavior in nonlinear models.

### 6.3 Timing distinction

The allocation models use contemporaneously observable month-end VRP features to form the following month’s allocation.

The direct-variance layer uses lagged implied variance as a strike proxy and the subsequent realized-variance observation as settlement.

The same underlying variables therefore enter the two evidence layers through different temporal and economic mappings.

---

## 7. Benchmark portfolios

The principal allocation benchmarks are:

1. Buy-and-Hold Equity;
2. 60/40 Equity–Bond;
3. 1/N Equity–Bond.

### 7.1 Buy-and-Hold Equity

The portfolio remains fully invested in equity:

\[
w^{eq}_t = 1
\]

\[
w^{bond}_t = 0
\]

### 7.2 60/40 portfolio

The portfolio maintains:

\[
w^{eq}_t = 0.60
\]

\[
w^{bond}_t = 0.40
\]

### 7.3 Equal-weighted portfolio

The 1/N benchmark maintains:

\[
w^{eq}_t = 0.50
\]

\[
w^{bond}_t = 0.50
\]

These simple portfolios impose benchmark discipline. A complex dynamic strategy is economically useful only if it improves return, downside risk, welfare or implementation characteristics relative to transparent alternatives.

---

## 8. Hidden Markov Model allocation

### 8.1 Latent-state framework

The Hidden Markov Model assumes that observed variables are generated by an unobservable state process.

Two states are estimated:

1. a normal state;
2. a stress state.

The stress state is identified from the estimated state characteristics, particularly realized variance and adverse market conditions.

### 8.2 HMM feature specifications

The principal HMM specifications include combinations of:

- equity returns;
- log realized variance;
- raw VRP;
- log implied-to-realized variance;
- log implied variance.

The central specifications are:

| Specification | Main features |
|---|---|
| HMM RV | Equity return and log realized variance |
| HMM RV + Raw VRP | Equity return, log realized variance and raw VRP |
| HMM RV + Log VRP | Equity return, log realized variance and log VRP |

Additional specification-grid models are used for diagnostic and model-selection purposes.

### 8.3 Rolling estimation

The HMM is estimated using a rolling window of 72 months.

At signal date \(t\):

1. only observations available through \(t\) enter the model;
2. the latent states are estimated on the rolling historical window;
3. the probability of the stress state is calculated;
4. that probability determines the portfolio weights used for the next holding period.

This procedure prevents full-sample state estimation from leaking future information into the backtest.

### 8.4 Allocation mapping

Let \(p^{stress}_t\) denote the estimated stress probability.

The equity weight is:

\[
w^{eq}_t
=
0.80
\left(
1-p^{stress}_t
\right)
+
0.20
p^{stress}_t
\]

Equivalently:

\[
w^{eq}_t
=
0.80
-
0.60p^{stress}_t
\]

The bond weight is:

\[
w^{bond}_t
=
1-w^{eq}_t
\]

Equity exposure therefore varies continuously between 80% in the lowest-stress case and 20% in the highest-stress case.

---

## 9. Markov-switching regression allocation

The Markov-switching regression provides a second latent-regime framework.

The tested specifications are:

| Specification | Exogenous information |
|---|---|
| RSM Returns Only | No volatility feature |
| RSM RV | Log realized variance |
| RSM RV + Raw VRP | Log realized variance and raw VRP |
| RSM RV + Log VRP | Log realized variance and log VRP |

The RSM produces a stress probability which is mapped into equity and bond weights using the same 80%–20% defensive allocation rule as the HMM.

Using an identical allocation mapping isolates the effect of the regime-estimation method.

The RSM is also estimated on rolling 72-month windows and evaluated one step ahead.

---

## 10. Machine-learning stress classification

### 10.1 Objective

The machine-learning layer tests whether nonlinear classifiers extract stress-prediction information that is not captured by the parametric regime models.

Three classifier families are examined:

- penalized logistic regression;
- Random Forest;
- histogram-based Gradient Boosting.

### 10.2 Feature sets

The base feature set contains:

\[
X^{base}_t
=
\{
R^{eq}_t,
R^{bond}_t,
\log RV_t,
\log IV_t
\}
\]

The VRP-enhanced feature set adds:

\[
X^{VRP}_t
=
X^{base}_t
\cup
\{
VRP_t,
LogVRP_t
\}
\]

Comparing base and VRP-enhanced versions allows the incremental information content of the variance premium to be evaluated.

### 10.3 Stress label

For every rolling training window, the next period is labelled as stress when either:

\[
R^{eq}_{t+1}
\leq
Q_{0.20}
\left(
R^{eq}_{training}
\right)
\]

or:

\[
RV_{t+1}
\geq
Q_{0.80}
\left(
RV_{training}
\right)
\]

The thresholds are recalculated within each rolling training window.

The label therefore identifies periods characterized by either unusually weak equity returns or unusually high realized variance.

### 10.4 Strict one-step-ahead design

At signal date \(t\):

- features dated \(t\) are observable;
- training feature-label pairs end at \(t-1\);
- each training label describes the outcome at \(s+1\);
- quantile thresholds are estimated only from the rolling training window;
- the probability estimated at \(t\) determines weights for \(t+1\).

The estimation window is 72 months.

### 10.5 Allocation rule

The predicted stress probability is mapped into the same continuous equity–bond allocation used by the HMM and RSM:

\[
w^{eq}_t
=
0.80
-
0.60p^{stress}_t
\]

\[
w^{bond}_t
=
1-w^{eq}_t
\]

This makes the economic comparison depend primarily on the quality of the estimated stress probability rather than on different portfolio rules.

### 10.6 Prediction evaluation

Classification is evaluated through:

- ROC-AUC;
- precision–recall AUC;
- Brier score;
- log loss;
- accuracy;
- balanced accuracy;
- precision;
- recall.

Prediction metrics are reported separately from portfolio metrics because stronger classification does not necessarily imply higher investment welfare.

---

## 11. Allocation turnover and transaction costs

For the equity–bond strategies, turnover is the absolute change in target asset weights:

\[
Turnover_t
=
\left|
w^{eq}_t
-
w^{eq}_{t-1}
\right|
+
\left|
w^{bond}_t
-
w^{bond}_{t-1}
\right|
\]

Net portfolio return is:

\[
R^{net}_t
=
R^{gross}_t
-
c
\times
Turnover_t
\]

where \(c\) is the proportional transaction-cost assumption.

The baseline allocation cost is 10 basis points per unit of turnover.

---

## 12. Model-based direct variance-payoff approximation

### 12.1 Methodological status

The direct-variance extension is not a reconstructed variance-swap backtest.

It is a model-based mapping from a variance payoff into a synthetic portfolio-capital return.

It does not use:

- an exact option-replicated variance strike;
- an observed variance-swap price;
- contractual variance notional;
- daily derivative mark-to-market;
- collateral remuneration;
- margin calls;
- dealer bid–ask spreads;
- counterparty adjustments.

### 12.2 Strike proxy

For settlement month \(t\), the strike proxy is the implied variance observed at the preceding month-end:

\[
K^{var}_t
=
IV_{t-1}
\]

The one-period shift ensures that the strike proxy is observable before the settlement variance is realized.

### 12.3 Settlement proxy

The settlement proxy is:

\[
RV^{settlement}_t
=
RV_t
\]

where \(RV_t\) is the annualized trailing 21-observation realized-variance measure sampled at settlement month-end.

### 12.4 Short-variance payoff

The unnormalized short-variance payoff is:

\[
\Pi^{short}_t
=
K^{var}_t
-
RV^{settlement}_t
\]

The normalized payoff is:

\[
\widetilde{\Pi}^{short}_t
=
\frac{
K^{var}_t
-
RV^{settlement}_t
}{
K^{var}_t
}
\]

The corresponding log carry diagnostic is:

\[
LogCarry_t
=
\log
\left(
\frac{
K^{var}_t
}{
RV^{settlement}_t
}
\right)
\]

The normalized payoff is not an observed return on invested capital. It is a dimensionless payoff representation used for risk scaling.

### 12.5 Entry signals

The positive-VRP gate is active when:

\[
VRP_{t-1}
>
0
\]

The High-VRP gate is active when the lagged entry VRP exceeds the median of its preceding rolling history.

The historical median uses a 36-month window with at least 24 observations and is shifted by one additional month. At settlement date \(t\), the threshold therefore uses entry signals corresponding at the latest to \(VRP_{t-2}\). The current entry signal \(VRP_{t-1}\) and the current settlement outcome are excluded from threshold estimation.

### 12.6 Lagged risk estimate

The payoff-volatility estimate is calculated from the normalized payoff:

\[
\widehat{\sigma}_{t-1}
=
Std
\left(
\widetilde{\Pi}^{short}_{t-36},
\ldots,
\widetilde{\Pi}^{short}_{t-1}
\right)
\]

The primary window is 36 months, with a minimum of 24 observations.

The estimate is shifted by one month. At settlement \(t\), it therefore contains only payoffs realized through \(t-1\).

### 12.7 Risk-targeted notional

For annual target volatility \(\sigma^{target}\), the monthly target is:

\[
\sigma^{target}_{monthly}
=
\frac{
\sigma^{target}
}{
\sqrt{12}
}
\]

The unconstrained notional is:

\[
N^{raw}_t
=
\frac{
\sigma^{target}_{monthly}
}{
\widehat{\sigma}_{t-1}
}
\]

The final notional is:

\[
N_t
=
\min
\left(
N^{raw}_t,
N^{max}
\right)
\times
Gate_t
\]

with baseline maximum absolute notional:

\[
N^{max}
=
0.25
\]

The value 0.25 corresponds to a 25% maximum absolute notional.

The principal strategies target either 5% or 10% annual volatility.

The target is an ex ante forecast-volatility objective. It is not a guarantee that ex post realized volatility will equal the target.

### 12.8 Direct-variance strategy set

The four principal specifications are:

| Strategy | Target | Gate |
|---|---:|---|
| Direct Short Variance 5% Vol | 5% | Always active |
| Direct Short Variance 10% Vol | 10% | Always active |
| Direct Short Variance 10% Vol (VRP > 0) | 10% | Positive lagged VRP |
| Direct Short Variance 10% Vol (High VRP) | 10% | VRP above lagged historical median |

All four return series are aligned to their common available sample before comparison.

---

## 13. Monthly roll costs

Each variance exposure represents a one-month payoff.

At settlement, the old exposure expires and a new exposure must be initiated for the following month.

Transaction costs are therefore charged on the full absolute notional entered:

\[
Cost_t
=
c
\left|
N_t
\right|
\]

and not merely on:

\[
\left|
N_t-N_{t-1}
\right|
\]

The latter quantity is retained only as a diagnostic of changes in desired exposure.

The baseline direct-variance roll-cost assumption is 10 basis points per unit of monthly absolute notional.

Net synthetic strategy return is:

\[
R^{DV,net}_t
=
N_t
\widetilde{\Pi}^{short}_t
-
c
\left|
N_t
\right|
\]

This cost remains stylized. It is not an observed bid–ask spread for a variance-swap transaction.

---

## 14. Exploratory Pure VRP Proxy

The Pure VRP Proxy is retained as an exploratory diagnostic.

It represents a synthetic transformation of the implied-to-realized variance relationship.

It is not classified as an implementable direct-variance strategy because it does not reproduce:

- a forward contractual payoff;
- a risk-targeted notional;
- an exact derivative settlement;
- realistic derivative execution.

Its performance is therefore reported separately from the implementable evidence layer.

---

## 15. Performance measures

The strategies are evaluated using:

- annualized geometric return;
- annualized volatility;
- Sharpe ratio;
- Sortino ratio;
- maximum drawdown;
- Calmar ratio;
- monthly VaR at 95%;
- monthly CVaR at 95%;
- average turnover;
- number of observations.

### 15.1 Sharpe ratio

The annualized Sharpe ratio is:

\[
Sharpe
=
\sqrt{12}
\frac{
\overline{R}
}{
\sigma(R)
}
\]

The risk-free rate is treated as zero in the reported strategy comparisons.

### 15.2 Sortino ratio

With a zero monthly minimum acceptable return, downside deviation is:

\[
DD
=
\sqrt{
\frac{1}{T}
\sum_{t=1}^{T}
\min(R_t,0)^2
}
\]

The annualized Sortino ratio is:

\[
Sortino
=
\sqrt{12}
\frac{
\overline{R}
}{
DD
}
\]

Positive observations contribute zero downside rather than being removed from the denominator.

### 15.3 Drawdown

Cumulative wealth is:

\[
W_t
=
\prod_{s=1}^{t}
(1+R_s)
\]

Drawdown is:

\[
DD_t
=
\frac{
W_t
}{
\max_{s\leq t} W_s
}
-
1
\]

Maximum drawdown is the minimum value of \(DD_t\).

### 15.4 Tail risk

The 95% monthly VaR is the empirical fifth percentile of monthly returns.

The 95% CVaR is the average return conditional on being below or equal to that VaR threshold.

---

## 16. Welfare analysis

### 16.1 Mean–variance certainty equivalent

For annualized mean return \(\mu\), annualized variance \(\sigma^2\), and risk-aversion coefficient \(\gamma\), the mean–variance certainty equivalent is:

\[
CEQ^{MV}
=
\mu
-
\frac{\gamma}{2}
\sigma^2
\]

The tested risk-aversion coefficients are:

\[
\gamma
\in
\{
1,3,5,10
\}
\]

### 16.2 CRRA certainty equivalent

A Constant Relative Risk Aversion certainty equivalent is also calculated from the distribution of monthly gross returns.

The CRRA measure captures higher-order distributional effects that are not fully summarized by the first two moments.

The CRRA domain is validated by checking that:

\[
1+R_t
>
0
\]

for every observation.

### 16.3 Fee-equivalent gain

The welfare difference against benchmark \(b\) is:

\[
\Delta CEQ_{s,b}
=
CEQ_s
-
CEQ_b
\]

The annual fee-equivalent value in basis points is:

\[
FeeEquivalent_{s,b}
=
10,000
\times
\Delta CEQ_{s,b}
\]

### 16.4 Block bootstrap

Confidence intervals for welfare differences are calculated using a block bootstrap.

The baseline procedure uses:

- 2,000 bootstrap replications;
- six-month blocks;
- comparisons against 60/40;
- comparisons against 1/N Equity–Bond.

A strategy is classified as statistically superior when the lower confidence bound of its welfare difference is above zero.

---

## 17. Robustness analysis

The direct-variance robustness analysis evaluates six dimensions.

### 17.1 Transaction costs

The tested cost assumptions are:

\[
0,\ 10,\ 25,\ 50
\text{ basis points}
\]

### 17.2 Volatility-estimation window

The tested payoff-volatility windows are:

\[
12,\ 24,\ 36,\ 60
\text{ months}
\]

Comparisons are performed on a common sample within each sensitivity dimension.

### 17.3 Notional caps

The tested maximum notionals are:

\[
5\%,\ 10\%,\ 15\%,\ 25\%,\ 50\%
\]

### 17.4 Subperiods

The strategy is evaluated over:

- the full sample;
- the first half;
- the second half;
- the pre-Covid period;
- the Covid-and-after period.

### 17.5 Crisis exclusions

Robustness tests exclude individual crisis windows and all identified major crises jointly.

This tests whether average performance is driven by a small number of exceptional observations.

### 17.6 Risk aversion

Welfare stability is examined for:

\[
\gamma
=
1,\ 3,\ 5,\ 10
\]

---

## 18. Comparability and interpretation rules

The following rules are applied throughout the thesis.

First, allocation strategies are compared with allocation benchmarks on their aligned 184-observation US and 122-observation European samples.

Second, direct-variance strategies are compared with benchmarks realigned to their 232-observation US and 170-observation European samples.

Third, performance values from different evidence layers are not treated as if they came from the same sample.

Fourth, the Pure VRP Proxy remains exploratory.

Fifth, the direct-variance strategy is described as a model-based approximation rather than as a traded variance-swap return.

Sixth, strong in-sample or historical results are not interpreted as proof of future profitability.

---

## 19. Methodological limitations

The framework improves on a purely contemporaneous VRP proxy by introducing forward alignment, lagged risk targeting, payoff normalization, notional constraints, roll costs and welfare inference.

Nevertheless, it remains subject to major limitations.

It does not reconstruct:

- exact option-implied forward variance;
- an option-replicated variance-swap strike;
- contractual maturity conventions;
- exact variance notional;
- daily derivative valuation;
- collateral and financing;
- variation margin;
- bid–ask spreads;
- dealer intermediation costs;
- counterparty risk;
- market impact under stress.

The direct-variance results must therefore be interpreted as evidence about a stylized payoff mechanism, not as a verified historical return available to an investor.

---

## 20. Summary

The methodology separates the information contained in the Variance Risk Premium from the payoff through which that information may be monetized.

The allocation layer asks whether VRP improves regime identification and equity–bond portfolio decisions.

The direct-variance layer asks whether a forward-aligned short-variance payoff produces economic value after lagged risk control and stylized implementation costs.

The welfare and robustness analyses then evaluate whether apparent performance survives benchmark comparison, sampling uncertainty and alternative implementation assumptions.

This architecture makes it possible to answer the central research question without conflating predictive information, portfolio allocation and derivative payoff exposure.

---

# Chapter 3 — Empirical Results

## 1. Introduction

This chapter presents the empirical results of the thesis.

The analysis distinguishes two evidence layers.

The first layer evaluates whether Variance Risk Premium variables improve equity–bond allocation when incorporated into Hidden Markov Models, Markov-switching regressions and machine-learning stress classifiers.

The second layer evaluates a model-based direct variance-payoff approximation designed to represent the economic consequences of selling variance exposure.

This distinction is essential. Allocation strategies and direct-variance strategies use different payoff constructions and different aligned samples. They are therefore interpreted jointly but are not ranked mechanically as if they represented identical investment opportunities.

The allocation comparisons contain:

| Market | Out-of-sample observations |
|---|---:|
| United States | 184 |
| Europe | 122 |

The direct-variance comparisons contain:

| Market | Strategy observations |
|---|---:|
| United States | 232 |
| Europe | 170 |

---

## 2. Equity–bond allocation evidence

### 2.1 United States benchmarks

The United States allocation benchmarks are:

- Buy-and-Hold Equity;
- 60/40 Equity–Bond;
- 1/N Equity–Bond.

Their aligned out-of-sample results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 13.96% | 14.20% | 0.995 | 1.483 | −23.93% | −8.18% | 0.00% | 184 |
| 60/40 | 9.39% | 9.21% | 1.024 | 1.481 | −20.06% | −5.20% | 1.47% | 184 |
| 1/N Equity–Bond | 8.23% | 8.05% | 1.025 | 1.460 | −19.10% | −4.58% | 1.53% | 184 |

Buy-and-Hold Equity generates the highest annualized return, but it also produces the greatest volatility and the largest drawdown among the three benchmarks.

The 60/40 and 1/N portfolios sacrifice return in exchange for lower volatility, lower tail losses and smaller drawdowns. Their Sharpe ratios are slightly above one.

The equal-weighted portfolio produces the highest benchmark Sharpe ratio, at 1.025. This creates a demanding comparison for the regime and machine-learning models.

---

### 2.2 United States HMM results

The principal HMM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 8.17% | 8.33% | 0.987 | 1.446 | −17.79% | −4.88% | 17.57% | 184 |
| HMM RV + Raw VRP | 10.67% | 10.59% | 1.014 | 1.509 | −21.98% | −6.03% | 9.57% | 184 |
| HMM RV + Log VRP | 8.36% | 8.24% | 1.019 | 1.493 | −16.67% | −4.86% | 25.35% | 184 |

The highest HMM Sharpe ratio is obtained by HMM RV + Log VRP, at 1.019.

This value is close to the 60/40 and 1/N benchmarks, but remains slightly below them. The model therefore does not establish superior average risk-adjusted performance.

Its principal advantage is drawdown control. Its maximum drawdown is −16.67%, compared with −20.06% for 60/40, −19.10% for 1/N and −23.93% for Buy-and-Hold Equity.

The improvement in drawdown is economically relevant, but the strategy requires substantially greater turnover. Average turnover reaches 25.35%, compared with approximately 1.5% for the balanced benchmarks.

The HMM RV + Raw VRP model produces a higher annualized return of 10.67%, but its drawdown and volatility are also higher. Its risk-adjusted performance does not exceed the simple benchmarks.

The United States HMM evidence therefore supports a limited conclusion: VRP-related variables can alter the risk profile of dynamic allocation, particularly the maximum drawdown, but they do not generate robust benchmark dominance.

---

### 2.3 United States RSM results

The principal Markov-switching regression results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 7.13% | 7.76% | 0.929 | 1.325 | −18.37% | −4.63% | 15.92% | 184 |
| RSM RV | 8.30% | 9.95% | 0.853 | 1.193 | −15.67% | −5.85% | 32.14% | 184 |
| RSM RV + Raw VRP | 9.61% | 10.25% | 0.949 | 1.412 | −15.43% | −5.53% | 36.69% | 184 |
| RSM RV + Log VRP | 7.57% | 9.85% | 0.792 | 1.088 | −20.88% | −6.02% | 24.28% | 184 |

RSM RV + Raw VRP produces the highest RSM Sharpe ratio, at 0.949, and the smallest drawdown, at −15.43%.

However, its average turnover reaches 36.69%. The reduction in drawdown is therefore accompanied by considerable implementation intensity.

None of the RSM specifications dominates the balanced benchmarks in Sharpe ratio. The RSM results reinforce the distinction between improvements in a specific risk dimension and broad economic superiority.

---

### 2.4 United States machine-learning results

The strongest United States machine-learning allocation strategy is ML Logistic Base:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ML Logistic Base | 7.58% | 7.60% | 1.002 | 1.449 | −18.54% | −4.35% | 17.39% | 184 |

The strategy produces volatility below the traditional balanced portfolios and a maximum drawdown below that of Buy-and-Hold Equity and 60/40.

Its Sharpe ratio remains below those of 60/40 and 1/N.

The strongest machine-learning portfolio is also a base specification without VRP variables. This means that the inclusion of VRP does not universally improve machine-learning allocation in the United States.

Prediction quality and portfolio value must therefore remain distinct. A classifier may improve a statistical prediction metric without producing a sufficiently different allocation to improve investor welfare.

---

### 2.5 United States allocation conclusion

The United States allocation evidence does not support a claim of robust model dominance.

The best dynamic models are competitive with simple benchmarks and may improve particular downside-risk measures, especially maximum drawdown.

However:

- the strongest benchmark Sharpe ratio is 1.025;
- the strongest HMM Sharpe ratio is 1.019;
- the strongest RSM Sharpe ratio is 0.949;
- the strongest ML Sharpe ratio is 1.002.

The economic advantage of the dynamic models is therefore limited and dependent on the selected performance criterion.

---

### 2.6 European benchmarks

The corrected European allocation results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Buy-and-Hold Equity | 3.98% | 17.17% | 0.313 | 0.468 | −35.74% | −9.86% | 0.00% | 122 |
| 60/40 | 2.68% | 11.24% | 0.292 | 0.428 | −20.32% | −6.55% | 1.74% | 122 |
| 1/N Equity–Bond | 2.30% | 9.84% | 0.280 | 0.408 | −19.66% | −5.85% | 1.81% | 122 |

Risk-adjusted performance is materially weaker in Europe than in the United States.

Buy-and-Hold Equity produces the highest benchmark Sharpe ratio, at 0.313, but also the largest drawdown, at −35.74%.

The balanced portfolios substantially reduce drawdown and tail risk. Their Sharpe ratios remain close to the equity benchmark.

---

### 2.7 European HMM results

The corrected European HMM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| HMM RV | 1.80% | 10.94% | 0.218 | 0.315 | −19.39% | −6.20% | 17.76% | 122 |
| HMM RV + Raw VRP | 1.55% | 11.10% | 0.166 | 0.239 | −21.07% | −6.34% | 25.83% | 122 |
| HMM RV + Log VRP | 1.66% | 11.11% | 0.179 | 0.257 | −20.81% | −6.34% | 29.59% | 122 |

The HMM RV model without VRP produces the highest HMM Sharpe ratio, at 0.218.

Adding raw or log VRP reduces the Sharpe ratio and increases turnover.

The HMM models generate drawdowns close to those of the balanced benchmarks, but do not improve return or risk-adjusted performance sufficiently to compensate for their greater complexity.

The corrected data therefore do not imply that the VRP is absent in Europe. Instead, they show that adding VRP to these HMM allocation specifications does not improve portfolio performance.

---

### 2.8 European RSM results

The European RSM results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| RSM Returns Only | 2.12% | 10.61% | 0.239 | 0.344 | −19.74% | −6.28% | 15.14% | 122 |
| RSM RV | 1.85% | 10.75% | 0.216 | 0.310 | −20.01% | −6.44% | 30.63% | 122 |
| RSM RV + Raw VRP | 2.55% | 11.24% | 0.281 | 0.407 | −20.47% | −6.74% | 34.00% | 122 |
| RSM RV + Log VRP | 2.33% | 10.86% | 0.263 | 0.380 | −19.78% | −6.38% | 28.01% | 122 |

RSM RV + Raw VRP is the strongest European regime specification.

Its Sharpe ratio of 0.281 is close to the 1/N benchmark but remains below Buy-and-Hold Equity and 60/40.

Its average turnover is 34.00%, compared with less than 2% for the balanced benchmarks.

The RSM result indicates that raw VRP contains some useful information within this model family, but the economic gain is insufficient to establish benchmark dominance.

---

### 2.9 European machine-learning results

The strongest European machine-learning portfolio is:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| ML Random Forest + VRP | 2.26% | 9.99% | 0.274 | 0.396 | −19.17% | −5.82% | 15.38% | 122 |

The model achieves a maximum drawdown slightly below the balanced benchmarks and a Sharpe ratio close to 1/N.

Its portfolio performance is economically competitive, but not superior.

The predictive results show that VRP variables add information in some nonlinear specifications, particularly the Random Forest. However, the portfolio and welfare results show that this incremental information does not translate into statistically significant gains over simple portfolios.

---

### 2.10 European allocation conclusion

The corrected European evidence is not that the Variance Risk Premium disappears.

The appropriate conclusion is narrower:

> VRP-related variables contain model-dependent information, but their inclusion in the tested HMM, RSM and machine-learning equity–bond allocation models does not produce robust dominance over simple benchmarks.

This distinction becomes important when the direct-variance results are introduced.

---

## 3. Direct variance-payoff diagnostics

The direct-variance layer begins with the underlying payoff rather than with a portfolio-allocation rule.

The strike proxy is lagged implied variance:

\[
K^{var}_t = IV_{t-1}
\]

The settlement proxy is the realized-variance measure observed at \(t\):

\[
RV^{settlement}_t = RV_t
\]

The normalized short-variance payoff is:

\[
\widetilde{\Pi}^{short}_t
=
\frac{
IV_{t-1}-RV_t
}{
IV_{t-1}
}
\]

The underlying diagnostics are:

| Market | Obs | Mean Strike | Mean RV | Mean Short Payoff | Positive Months | Mean Normalized Payoff | Skewness | 1% Quantile | Worst Payoff | Below −100% |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| United States | 256 | 4.35% | 3.57% | 0.78% | 82.42% | 0.253 | −3.849 | −4.080 | −4.432 | 4.69% |
| Europe | 194 | 5.22% | 4.02% | 1.21% | 78.35% | 0.239 | −2.231 | −2.060 | −2.439 | 4.12% |

Both markets display the central short-variance characteristic:

- positive payoff in a large majority of observations;
- positive average carry;
- severe negative skewness;
- occasional losses exceeding the strike-normalized initial exposure.

The European average variance spread is larger than the United States spread in the sample.

However, average carry alone is insufficient. The highly negative tail observations mean that notional scaling and welfare analysis are necessary.

---

## 4. United States direct-variance results

The main United States direct-variance results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct Short Variance 5% Vol | 4.16% | 8.03% | 0.548 | 0.631 | −23.46% | −6.79% | 2.31% | 232 |
| Direct Short Variance 10% Vol | 8.43% | 16.07% | 0.604 | 0.696 | −39.77% | −13.57% | 4.61% | 232 |
| Direct Short Variance 10% Vol (VRP > 0) | 8.18% | 16.07% | 0.590 | 0.659 | −39.77% | −13.29% | 3.99% | 232 |
| Direct Short Variance 10% Vol (High VRP) | 6.23% | 7.17% | 0.882 | 1.218 | −23.46% | −5.26% | 2.01% | 232 |

The always-active 10% strategy experiences volatility far above its target and a drawdown of approximately 40%.

This illustrates the weakness of purely backward-looking risk targeting in a negatively skewed payoff. A lagged volatility estimate cannot guarantee ex post volatility when a large variance shock occurs.

The positive-VRP gate does not materially improve the United States result. It retains most active months and remains exposed to the principal tail losses.

The High-VRP filter is more effective. It reduces activity, volatility and drawdown and produces the strongest Sharpe ratio, at 0.882.

Relative to the aligned benchmarks:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Max Drawdown |
|---|---:|---:|---:|---:|
| High-VRP direct variance | 6.23% | 7.17% | 0.882 | −23.46% |
| 60/40 | 8.00% | 9.92% | 0.827 | −32.35% |
| 1/N Equity–Bond | 7.20% | 8.62% | 0.852 | −26.89% |

The High-VRP strategy has a higher Sharpe ratio and lower drawdown than the two aligned benchmarks. However, these headline metrics do not establish welfare dominance because sampling uncertainty and nonlinear tail risk remain substantial.

---

## 5. European direct-variance results

The European direct-variance results are:

| Strategy | Ann. Return | Ann. Vol | Sharpe | Sortino | Max Drawdown | CVaR 95 | Avg Turnover | Obs |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Direct Short Variance 5% Vol | 6.78% | 5.69% | 1.186 | 1.708 | −11.00% | −4.09% | 2.70% | 170 |
| Direct Short Variance 10% Vol | 13.61% | 11.37% | 1.186 | 1.708 | −21.37% | −8.18% | 5.40% | 170 |
| Direct Short Variance 10% Vol (VRP > 0) | 13.08% | 9.70% | 1.324 | 1.891 | −21.36% | −7.34% | 4.39% | 170 |
| Direct Short Variance 10% Vol (High VRP) | 6.39% | 7.65% | 0.852 | 1.214 | −16.97% | −5.97% | 2.33% | 170 |

The strongest European specification is the 10% target strategy with a positive-VRP gate.

It produces:

- annualized return of 13.08%;
- annualized volatility of 9.70%;
- Sharpe ratio of 1.324;
- Sortino ratio of 1.891;
- maximum drawdown of −21.36%;
- average monthly roll notional of 4.39%.

The always-active strategy also performs strongly, but the positive-VRP gate lowers realized volatility while preserving most of the annual return.

The High-VRP gate is less effective in Europe. Requiring the VRP to exceed its historical median removes many months in which the variance spread remains positive and economically valuable.

The European evidence therefore favors a simple sign filter rather than an extreme-value filter.

---

## 6. Welfare analysis

Headline performance metrics do not directly measure investor utility.

The welfare analysis compares the direct-variance strategies with 60/40 and 1/N using mean–variance and CRRA certainty equivalents.

At a risk-aversion coefficient of five, the selected strategies produce:

| Market | Strategy | MV CEQ | CRRA CE | Fee equivalent vs 60/40 | 95% CI vs 60/40 | Fee equivalent vs 1/N | 95% CI vs 1/N |
|---|---|---:|---:|---:|---:|---:|---:|
| United States | 10% High VRP | 5.04% | 5.00% | −70.9 bp | [−5.49%, 4.92%] | −45.0 bp | [−4.94%, 4.59%] |
| Europe | 10% VRP > 0 | 10.49% | 10.67% | 926.6 bp | [3.27%, 15.72%] | 898.8 bp | [2.91%, 15.51%] |

### 6.1 United States welfare

The selected United States strategy does not dominate the benchmarks.

Its estimated mean–variance certainty equivalent is lower than both comparison portfolios. More importantly, the bootstrap confidence intervals contain zero.

The data therefore do not establish that the strategy produces a statistically positive welfare gain.

The United States conclusion is:

> The High-VRP direct-variance approximation improves selected risk-adjusted performance measures but does not establish robust investor-welfare dominance.

### 6.2 European welfare

The European result is materially different.

The selected strategy has a mean–variance certainty equivalent of 10.49% and a CRRA certainty equivalent of 10.67%.

The estimated fee-equivalent advantage is approximately:

- 927 basis points relative to 60/40;
- 899 basis points relative to 1/N.

The lower bootstrap confidence bounds are positive against both benchmarks.

Within the tested model and sample, the European welfare advantage is therefore statistically significant.

This statistical result is stronger than a comparison based only on Sharpe ratios.

---

## 7. Cross-market interpretation

The cross-market evidence cannot be summarized by stating that VRP works in one region and fails in another.

The evidence is conditional on the economic mechanism.

### 7.1 Informational allocation channel

In both markets:

- HMM, RSM and ML models are feasible;
- VRP variables affect state probabilities or classification;
- some models improve particular downside-risk measures;
- simple benchmarks remain difficult to beat;
- robust welfare dominance is not established.

### 7.2 Direct payoff channel

In the United States:

- average variance carry is positive;
- the payoff is strongly negatively skewed;
- the High-VRP filter improves the profile;
- welfare dominance is not statistically established.

In Europe:

- average variance carry is also positive;
- the positive-VRP gate produces strong risk-adjusted performance;
- welfare gains remain positive under bootstrap inference;
- the result survives the principal robustness tests.

### 7.3 Central empirical result

The main empirical result is:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested.

Using VRP as a state variable and harvesting a variance-linked payoff are not economically equivalent.

---

## 8. Interpretation of the Pure VRP Proxy

The Pure VRP Proxy is retained as an exploratory diagnostic only.

It is not a forward contractual payoff and does not include:

- lagged strike formation;
- settlement mechanics;
- risk-targeted variance notional;
- monthly roll costs;
- derivative execution constraints.

Its high historical performance must therefore not be interpreted as evidence of a directly tradable strategy.

The direct-variance extension is methodologically stronger because it imposes forward timing and explicit risk scaling. It nevertheless remains an approximation rather than a reconstructed variance-swap return.

---

## 9. Answer to the empirical question

The empirical question asks whether the Variance Risk Premium creates more economic value through direct variance carry or through its informational content for dynamic allocation.

The allocation evidence is limited. VRP-enhanced models can improve particular risk dimensions, but they do not consistently dominate simple portfolios.

The direct-payoff evidence is stronger in Europe. The positive-VRP strategy produces large and statistically significant welfare gains within the tested sample and model.

The United States evidence remains more cautious. The selected direct-variance strategy improves selected risk metrics but does not establish welfare superiority.

The most defensible empirical answer is therefore:

> The Variance Risk Premium does not possess a single, market-independent form of economic value. Its contribution depends on how it is transformed into a portfolio payoff. In the tested European sample, the model-based direct variance-payoff approximation creates substantially greater economic value than the use of VRP as an allocation feature. In the United States, neither channel establishes robust welfare dominance over traditional portfolios.

---

## 10. Summary

Five findings emerge.

First, the corrected European data invalidate the earlier claim that the European variance premium disappears.

Second, HMM, RSM and machine-learning allocation models do not establish robust superiority over simple equity–bond portfolios.

Third, short-variance payoffs display positive average carry and severe negative skewness in both markets.

Fourth, the selected United States direct-variance specification improves headline risk-adjusted metrics but does not generate statistically significant welfare gains.

Fifth, the selected European direct-variance specification produces strong and bootstrap-significant welfare gains, although it remains a model-based approximation subject to important implementation limitations.

These findings motivate the robustness and implementation analysis developed in the next chapter.

---

# Chapter 4 — Robustness and Implementation

## 1. Introduction

This chapter evaluates whether the empirical results remain economically meaningful under alternative implementation and calibration assumptions.

The purpose of robustness analysis is not to identify the parameter combination with the highest historical Sharpe ratio. It is to determine whether the principal conclusions survive when assumptions governing transaction costs, risk estimation, exposure limits, sample selection and investor risk aversion are changed.

The chapter preserves the distinction between the two empirical evidence layers.

The equity–bond allocation layer is primarily exposed to:

- dynamic-weight turnover;
- model instability;
- excessive reactions to estimated regime probabilities;
- implementation costs generated by frequent rebalancing.

The direct-variance layer is exposed to:

- monthly contract renewal;
- negatively skewed payoff shocks;
- errors in lagged volatility forecasts;
- choice of notional cap;
- choice of entry filter;
- transaction-cost assumptions;
- sensitivity to crisis periods and sample composition.

The two layers therefore require different robustness tests.

The main conclusion is that the allocation models remain economically competitive in selected dimensions but do not establish robust benchmark dominance. The United States HMM can be made more implementable through partial rebalancing, but its principal advantage remains drawdown control rather than superior welfare.

The direct-variance results are more asymmetric. The selected United States strategy remains sensitive to risk-estimation choices and does not consistently dominate conventional benchmarks in certainty-equivalent terms. The selected European strategy remains strong across the principal robustness dimensions tested.

---

## 2. Principles of the robustness design

Five principles govern the analysis.

First, all sensitivity calculations use only information that would have been available before the corresponding strategy return.

Second, comparisons within a calibration dimension are aligned to a common sample. A strategy using a 12-month volatility window and a strategy using a 60-month window are therefore compared over the dates available to both specifications.

Third, transaction costs are applied to the economically relevant implementation quantity.

For equity–bond allocation, the cost base is the change in portfolio weights.

For direct variance carry, the cost base is the absolute notional of the newly initiated monthly exposure because the previous one-month exposure has settled.

Fourth, robustness is evaluated through multiple dimensions rather than a single Sharpe ratio. The analysis considers:

- annualized return;
- realized volatility;
- Sharpe ratio;
- maximum drawdown;
- CVaR;
- turnover;
- mean–variance certainty equivalent;
- CRRA certainty equivalent;
- welfare differences relative to 60/40 and 1/N.

Fifth, the robustness results do not eliminate the methodological limitations of the direct-variance approximation. Stability within a stylized model does not transform that model into an observed variance-swap backtest.

---

## 3. Allocation-model implementation robustness

### 3.1 Baseline implementation burden

The strongest allocation models generally require substantially more trading than the simple benchmarks.

The principal aligned results are:

| Market | Strategy | Sharpe | Max Drawdown | Avg Turnover |
|---|---|---:|---:|---:|
| US | 60/40 | 1.024 | −20.06% | 1.47% |
| US | 1/N Equity–Bond | 1.025 | −19.10% | 1.53% |
| US | HMM RV + Log VRP | 1.019 | −16.67% | 25.35% |
| US | RSM RV + Raw VRP | 0.949 | −15.43% | 36.69% |
| EU | 60/40 | 0.292 | −20.32% | 1.74% |
| EU | 1/N Equity–Bond | 0.280 | −19.66% | 1.81% |
| EU | HMM RV | 0.218 | −19.39% | 17.76% |
| EU | RSM RV + Raw VRP | 0.281 | −20.47% | 34.00% |
| EU | ML Random Forest + VRP | 0.274 | −19.17% | 15.38% |

The contrast is substantial.

Simple balanced portfolios change weights only as asset prices drift away from their fixed targets. Their turnover remains below 2% in the aligned samples.

Dynamic models modify exposure as estimated stress probabilities change. Their average turnover ranges from approximately 15% to more than 36%.

This does not make dynamic allocation invalid, but it raises the standard required for economic justification. A modest drawdown improvement must be evaluated against greater trading, model risk and operational complexity.

---

### 3.2 United States allocation cost sensitivity

The United States HMM RV + Log VRP specification provides the clearest allocation example because it combines a competitive Sharpe ratio with improved drawdown.

Its cost sensitivity is:

| Strategy | 0 bps | 10 bps | 25 bps | 50 bps |
|---|---:|---:|---:|---:|
| 60/40 Sharpe | 1.026 | 1.024 | 1.021 | 1.016 |
| 1/N Sharpe | 1.028 | 1.025 | 1.022 | 1.016 |
| HMM RV + Log VRP Sharpe | 1.055 | 1.019 | 0.963 | 0.869 |

Before transaction costs, the HMM has a higher Sharpe ratio than the balanced benchmarks.

At the baseline cost of 10 basis points per unit of weight turnover, its Sharpe ratio falls to 1.019 and becomes slightly lower than both balanced benchmarks.

At 25 and 50 basis points, the performance difference becomes more material.

The benchmark portfolios are much less sensitive because their turnover is low.

The allocation result therefore depends partly on execution assumptions. The HMM does not generate a sufficiently large gross advantage to absorb high transaction costs without losing its competitive position.

Its drawdown advantage is more persistent. At the baseline cost, its maximum drawdown is −16.67%, compared with −20.06% for 60/40 and −19.10% for 1/N.

This supports a defensive interpretation of the HMM rather than a claim of broad performance dominance.

---

### 3.3 No-trade bands

A no-trade band avoids rebalancing when the difference between the current and desired weights is small.

For the United States HMM RV + Log VRP model, increasing the band from zero to 10% changes:

- the Sharpe ratio from approximately 1.019 to 1.026;
- average turnover from approximately 25.30% to 23.53%.

The effect is favorable but limited.

The no-trade band eliminates small adjustments but does not prevent large changes when the estimated state probability moves substantially. It therefore cannot fully resolve the turnover generated by regime switching.

---

### 3.4 Partial rebalancing

Partial rebalancing moves the portfolio gradually toward the target allocation:

\[
w_t^{implemented}
=
\lambda w_t^{target}
+
(1-\lambda)
w_{t-1}^{implemented}
\]

where \(\lambda\) is the adjustment speed.

A value of one corresponds to full rebalancing. Lower values smooth the transition between portfolio states.

For HMM RV + Log VRP:

| Implementation | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | Avg Turnover |
|---|---:|---:|---:|---:|---:|
| Full rebalancing | 8.36% | 8.24% | 1.019 | −16.67% | 25.35% |
| Partial rebalancing, \(\lambda=0.25\) | 8.69% | 8.62% | 1.014 | −18.04% | 9.10% |

Partial rebalancing reduces turnover by approximately two thirds.

The Sharpe ratio declines only marginally, while the maximum drawdown remains below that of 60/40 and Buy-and-Hold Equity.

This makes the 0.25 implementation more defensible than full monthly movement to the estimated target.

However, the result does not imply benchmark dominance. The strategy still has more turnover than 60/40 and 1/N, and its Sharpe ratio remains slightly lower.

The correct interpretation is:

> Partial rebalancing improves the implementability of the selected United States HMM without converting it into a statistically superior allocation strategy.

---

### 3.5 European allocation robustness

The corrected European results do not identify an allocation model whose baseline performance would justify a detailed search for implementation parameters.

The strongest HMM has a Sharpe ratio of 0.218. The strongest RSM reaches 0.281 and the strongest ML strategy reaches 0.274.

These values remain close to or below the simple benchmarks, while the dynamic strategies require materially greater turnover.

The inclusion of raw or log VRP can improve selected model specifications, but the improvement is not stable across model families.

The European allocation conclusion is therefore robust in a negative but precise sense:

- VRP-related variables contain information;
- model performance varies with feature transformation;
- some dynamic portfolios improve particular downside measures;
- no tested allocation framework establishes robust economic dominance over simple benchmarks.

---

## 4. Direct-variance implementation framework

### 4.1 Baseline implementation assumptions

The baseline direct-variance strategy uses:

- one-month variance-payoff observations;
- lagged implied variance as the strike proxy;
- subsequent trailing realized variance as the settlement proxy;
- a 36-month payoff-volatility window;
- a minimum of 24 risk observations;
- a 25% maximum absolute notional;
- 10 basis points of cost per unit of monthly notional entered.

The risk target is an ex ante sizing objective. It is not an ex post volatility guarantee.

This distinction is particularly important in the United States, where the always-active 10% strategy realizes volatility above 16%.

A negatively skewed payoff can experience a shock far outside the distribution implied by its lagged volatility estimate.

---

### 4.2 Monthly roll-cost treatment

The direct-variance exposure settles every month.

Even when the desired notional remains unchanged, a new exposure must be initiated.

The transaction-cost base is therefore:

\[
Turnover^{cost}_t
=
|N_t|
\]

rather than:

\[
|N_t-N_{t-1}|
\]

Net return is:

\[
R^{net}_t
=
N_t
\widetilde{\Pi}^{short}_t
-
c|N_t|
\]

The change in desired notional is retained as an additional diagnostic but is not used as the cost base.

The baseline average cost notionals are:

- approximately 2.01% for the selected United States High-VRP strategy;
- approximately 4.39% for the selected European positive-VRP strategy.

---

## 5. Transaction-cost sensitivity

The tested direct-variance costs are:

\[
0,\ 10,\ 25,\ 50
\text{ basis points}
\]

### 5.1 United States

| Cost | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | 6.26% | 7.18% | 0.885 | −23.42% | −5.26% | 5.06% | −0.69% | −0.43% |
| 10 bps | 6.23% | 7.17% | 0.882 | −23.46% | −5.26% | 5.04% | −0.71% | −0.45% |
| 25 bps | 6.19% | 7.17% | 0.877 | −23.53% | −5.27% | 5.00% | −0.74% | −0.48% |
| 50 bps | 6.13% | 7.16% | 0.869 | −23.63% | −5.28% | 4.95% | −0.80% | −0.54% |

The United States High-VRP strategy is not highly sensitive to the tested cost range because its average active notional is low.

However, the strategy begins with a negative certainty-equivalent difference against both benchmarks. Higher costs therefore reinforce, rather than create, its welfare disadvantage.

### 5.2 Europe

| Cost | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 0 bps | 13.14% | 9.70% | 1.329 | −21.35% | −7.34% | 10.54% | 9.32% | 9.04% |
| 10 bps | 13.08% | 9.70% | 1.324 | −21.36% | −7.34% | 10.49% | 9.27% | 8.99% |
| 25 bps | 12.99% | 9.69% | 1.316 | −21.38% | −7.35% | 10.41% | 9.19% | 8.91% |
| 50 bps | 12.84% | 9.69% | 1.303 | −21.42% | −7.37% | 10.28% | 9.06% | 8.78% |

The European result remains strong throughout the tested range.

At 50 basis points per unit of monthly notional, the Sharpe ratio remains above 1.30 and the mean–variance certainty-equivalent advantage remains close to nine percentage points.

This test does not prove that actual derivative costs would be lower than the break-even level. It shows that the result is not generated by the difference between zero and moderate stylized roll costs.

---

## 6. Volatility-estimation window

The payoff-volatility windows tested are:

\[
12,\ 24,\ 36,\ 60
\text{ months}
\]

All specifications in this sensitivity test are aligned to the common sample required by the 60-month window. Consequently, the 36-month figures in this section differ slightly from the unrestricted baseline.

### 6.1 United States

| Window | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 12 months | 8.10% | 16.15% | 0.578 | −50.69% | −11.71% | 2.81% | −3.30% | −2.94% |
| 24 months | 6.38% | 9.94% | 0.678 | −32.59% | −7.18% | 4.27% | −1.85% | −1.49% |
| 36 months | 6.50% | 7.10% | 0.926 | −23.46% | −5.18% | 5.32% | −0.80% | −0.44% |
| 60 months | 6.26% | 6.87% | 0.922 | −23.00% | −5.17% | 5.15% | −0.97% | −0.60% |

The 12-month estimate is unstable. It assigns excessive notional before large payoff shocks and generates a drawdown above 50%.

Windows of 36 and 60 months produce much more stable results.

This supports the use of a relatively long risk-estimation window for the United States payoff.

It also confirms that the risk target should not be interpreted as a realized-volatility guarantee.

### 6.2 Europe

| Window | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | CVaR 95 | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| 12 months | 18.35% | 11.21% | 1.570 | −15.92% | −7.92% | 14.45% | 11.74% | 11.78% |
| 24 months | 15.66% | 10.46% | 1.453 | −19.97% | −8.06% | 12.46% | 9.75% | 9.79% |
| 36 months | 14.15% | 9.79% | 1.409 | −21.36% | −7.58% | 11.40% | 8.69% | 8.73% |
| 60 months | 13.92% | 8.93% | 1.513 | −17.21% | −6.70% | 11.52% | 8.80% | 8.84% |

Every tested European window produces a Sharpe ratio above 1.40 on the common sample.

The result is therefore not dependent on a unique 36-month calibration.

The strongest return is obtained with the shortest window, but the 60-month window produces lower realized volatility and a smaller drawdown.

The objective is not to select the ex post best window. The central finding is that the economic conclusion remains stable across the full range.

---

## 7. Notional-cap sensitivity

The tested maximum absolute notionals are:

\[
5\%,\ 10\%,\ 15\%,\ 25\%,\ 50\%
\]

### 7.1 United States

| Cap | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5% | 5.37% | 6.53% | 0.836 | −23.46% | 4.39% | −1.35% | −1.09% |
| 10% | 6.25% | 7.17% | 0.884 | −23.46% | 5.05% | −0.70% | −0.44% |
| 15% | 6.23% | 7.17% | 0.882 | −23.46% | 5.04% | −0.71% | −0.45% |
| 25% | 6.23% | 7.17% | 0.882 | −23.46% | 5.04% | −0.71% | −0.45% |
| 50% | 6.23% | 7.17% | 0.882 | −23.46% | 5.04% | −0.71% | −0.45% |

The High-VRP strategy rarely requires notionals above 10%.

Caps above 15% are therefore non-binding.

Reducing the cap to 5% lowers return and volatility but does not remove the historical maximum drawdown, because the principal drawdown occurs during periods in which the strategy already uses a relatively low notional.

### 7.2 Europe

| Cap | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|
| 5% | 12.07% | 7.94% | 1.482 | −17.95% | 10.19% | 8.97% | 8.69% |
| 10% | 13.08% | 9.70% | 1.324 | −21.36% | 10.49% | 9.27% | 8.99% |
| 15% | 13.08% | 9.70% | 1.324 | −21.36% | 10.49% | 9.27% | 8.99% |
| 25% | 13.08% | 9.70% | 1.324 | −21.36% | 10.49% | 9.27% | 8.99% |
| 50% | 13.08% | 9.70% | 1.324 | −21.36% | 10.49% | 9.27% | 8.99% |

The European result survives a substantial tightening of the exposure constraint.

With a 5% cap, the strategy produces:

- annualized return of 12.07%;
- volatility of 7.94%;
- Sharpe ratio of 1.482;
- maximum drawdown of −17.95%;
- CEQ advantages above eight percentage points relative to both benchmarks.

The result is therefore not driven by occasional use of the baseline 25% maximum notional.

Caps above 10% are non-binding in the baseline sample.

---

## 8. Subperiod stability

### 8.1 United States

| Period | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full sample | 6.23% | 7.17% | 0.882 | −23.46% | 5.04% | −0.71% | −0.45% |
| First half | 6.64% | 5.84% | 1.131 | −6.11% | 5.76% | 1.68% | 1.43% |
| Second half | 5.83% | 8.32% | 0.726 | −23.46% | 4.31% | −3.11% | −2.33% |
| Pre-Covid | 5.40% | 7.19% | 0.770 | −13.60% | 4.24% | −1.13% | −1.15% |
| Covid and after | 7.87% | 7.17% | 1.096 | −15.37% | 6.58% | 0.13% | 0.92% |

The United States result is not uniform through time.

The first half produces a Sharpe ratio above one and positive CEQ differences.

The second half produces greater volatility, a lower Sharpe ratio and negative welfare differences.

The strategy also performs better after Covid than in the preceding period.

This instability prevents a strong claim of persistent benchmark dominance.

### 8.2 Europe

| Period | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|
| Full sample | 13.08% | 9.70% | 1.324 | −21.36% | 10.49% | 9.27% | 8.99% |
| First half | 12.77% | 7.07% | 1.743 | −6.33% | 11.08% | 11.09% | 10.16% |
| Second half | 13.38% | 11.79% | 1.132 | −21.36% | 9.87% | 7.44% | 7.81% |
| Pre-Covid | 12.81% | 7.30% | 1.695 | −6.33% | 11.04% | 10.43% | 9.66% |
| Covid and after | 13.39% | 11.92% | 1.121 | −21.16% | 9.81% | 7.92% | 8.22% |

The European strategy remains profitable in every tested subperiod.

Risk increases in the second half and after Covid, but annualized return remains close to 13%.

The CEQ advantage remains above seven percentage points against both benchmarks in the weaker subperiods.

The full-sample European result is therefore not generated solely by an unusually favorable first half.

---

## 9. Crisis-exclusion analysis

The crisis tests remove the following windows individually and jointly:

- Global Financial Crisis;
- European sovereign-debt crisis;
- Volmageddon;
- Covid shock;
- inflation and interest-rate shock.

Removing crisis months serves two purposes.

First, it tests whether positive performance is generated by mechanically profiting from a small number of volatility events.

Second, it identifies whether tail losses during crises dominate the full-sample result.

### 9.1 United States

The United States High-VRP strategy remains sensitive to the identity of the excluded crisis.

Removing particular stress episodes can improve its Sharpe ratio and drawdown, but the welfare conclusion is not uniformly reversed.

This confirms that the strategy’s economic value is partly dependent on the timing of a small number of volatility shocks.

The crisis analysis therefore supports the cautious United States conclusion rather than a claim of structural dominance.

### 9.2 Europe

The European positive-VRP strategy remains strong when major crises are excluded jointly.

| Scenario | Retained Obs | Ann. Return | Ann. Vol | Sharpe | Max Drawdown | MV CEQ | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| Full sample | 170 | 13.08% | 9.70% | 1.324 | −21.36% | 10.49% | 9.27% | 8.99% |
| Exclude all major crises | 141 | 17.38% | 8.80% | 1.877 | −14.05% | 14.59% | 8.57% | 8.90% |

Excluding 29 crisis observations increases the Sharpe ratio and reduces maximum drawdown.

The CEQ advantage remains large relative to both benchmarks.

The European result is therefore not created by gains concentrated exclusively in the designated crisis windows.

This does not imply that crisis-period trading would be frictionless. It only shows that the historical statistical result survives their removal.

---

## 10. Risk-aversion stability

The tested risk-aversion coefficients are:

\[
\gamma
\in
\{1,3,5,10\}
\]

### 10.1 United States

| Gamma | MV CEQ | CRRA CE | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---:|---:|---:|---:|---:|
| 1 | 6.07% | 6.23% | −1.65% | −0.91% |
| 3 | 5.55% | 5.64% | −1.18% | −0.68% |
| 5 | 5.04% | 5.00% | −0.71% | −0.45% |
| 10 | 3.75% | 3.11% | 0.47% | 0.12% |

The United States High-VRP strategy is inferior to both benchmarks for risk-aversion coefficients from one to five.

It becomes slightly favorable under the mean–variance criterion at \(\gamma=10\), because its lower volatility receives greater weight.

This result is not sufficient to establish general superiority. It shows that the strategy may be attractive to a highly risk-averse investor who assigns substantial value to volatility reduction.

### 10.2 Europe

| Gamma | MV CEQ | CRRA CE | Delta CEQ vs 60/40 | Delta CEQ vs 1/N |
|---:|---:|---:|---:|---:|
| 1 | 12.37% | 13.08% | 8.81% | 9.10% |
| 3 | 11.43% | 11.93% | 9.04% | 9.05% |
| 5 | 10.49% | 10.67% | 9.27% | 8.99% |
| 10 | 8.14% | 6.96% | 9.83% | 8.84% |

The European CEQ advantage remains positive and economically large at every tested risk-aversion level.

The CRRA certainty equivalent declines more rapidly at high risk aversion because it is more sensitive to the negatively skewed payoff distribution.

Nevertheless, the central welfare conclusion remains unchanged.

---

## 11. Interpretation of the robustness evidence

The robustness results produce four principal conclusions.

First, the United States allocation model can be made more implementable through partial rebalancing. The reduction in turnover is substantial, but the model remains economically close to the simple benchmarks rather than clearly superior.

Second, the selected United States direct-variance strategy is robust to moderate transaction costs and long volatility-estimation windows, but its results vary materially across subperiods. It does not establish consistent welfare dominance.

Third, the European positive-VRP direct-variance strategy survives every principal calibration test:

- costs up to 50 basis points;
- volatility windows from 12 to 60 months;
- a 5% notional cap;
- first-half and second-half samples;
- pre-Covid and post-Covid periods;
- major-crisis exclusions;
- risk-aversion coefficients from one to ten.

Fourth, robustness inside the model does not eliminate execution uncertainty. The European result is statistically and economically strong under the tested assumptions, but the magnitude may be overstated by the absence of exact derivative-market frictions.

---

## 12. Implementation limitations

Several implementation elements remain outside the model.

### 12.1 Exact variance strike

The volatility-index square is not an exact forward variance-swap strike.

A full implementation would require the complete option surface and the relevant static replication formula.

### 12.2 Settlement convention

The realized-variance settlement proxy is a trailing 21-observation annualized estimate.

It is not the exact sum of squared returns over a contractual calendar interval.

### 12.3 Financing and collateral

The model does not include:

- collateral remuneration;
- funding spreads;
- initial margin;
- variation margin;
- liquidity reserves required during losses.

### 12.4 Daily mark-to-market

Only monthly payoff observations are represented.

Intramonth losses may create margin or liquidity constraints even when the final monthly payoff is positive.

### 12.5 Bid–ask spread and dealer costs

The cost grid is stylized.

Actual variance-swap or option-replication costs may vary with:

- maturity;
- market volatility;
- dealer balance-sheet conditions;
- trade size;
- crisis liquidity;
- counterparty quality.

### 12.6 Market impact and capacity

The strategy is evaluated without market impact.

A payoff accessible to a small investor may not scale to institutional size without changing execution costs.

### 12.7 Model and data risk

The European result depends on reconstructed VSTOXX history and a model-based payoff mapping.

Although date parsing and gap handling have been audited, residual source and methodology differences remain possible.

---

## 13. Robustness conclusion

The robustness evidence strengthens the main thesis result while also narrowing its interpretation.

The allocation models do not provide a universal improvement over simple portfolios. Their value is concentrated in selected risk dimensions and depends on turnover control.

The United States direct-variance result remains economically plausible but not dominant. Its performance is weaker in the second half of the sample and its welfare advantage is generally negative or statistically uncertain.

The European direct-variance result is considerably more stable. It survives changes in costs, risk estimation, exposure constraints, subperiods, crisis treatment and investor risk aversion.

The appropriate conclusion is therefore:

> The European direct-variance result is robust within the model-based framework, but it remains evidence about a stylized variance-payoff mechanism rather than proof of an exactly replicable traded return.

The final chapter evaluates how this evidence should be interpreted in light of the remaining data, modelling, statistical and implementation limitations.

---

# Chapter 5 — Limitations, Discussion and Conclusion

## 1. Introduction

This final chapter discusses the interpretation, limitations and contribution of the thesis and provides a direct answer to the research question.

The thesis investigated whether the Variance Risk Premium creates more economic value through:

1. its informational content for dynamic equity–bond allocation; or
2. a model-based direct variance-payoff approximation.

The empirical results demonstrate that these two channels are not equivalent.

Adding VRP variables to Hidden Markov Models, Markov-switching regressions and machine-learning classifiers produces model-dependent information but limited portfolio gains relative to simple benchmarks.

The direct variance-payoff evidence is stronger, but highly asymmetric across markets. In the United States, the selected High-VRP strategy improves selected risk-adjusted metrics without establishing statistically significant welfare dominance. In Europe, the positive-VRP strategy produces large and bootstrap-significant welfare gains within the tested model and sample.

The principal conclusion is therefore not that VRP is universally superior as either a signal or a standalone strategy.

The principal conclusion is:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested, the market in which it is measured and the implementation assumptions used to transform the underlying variance spread into portfolio returns.

This conclusion must be interpreted within the methodological boundaries of the thesis.

---

## 2. Final interpretation of the empirical evidence

### 2.1 Information and payoff are different economic objects

The same underlying variance variables are used in two distinct ways.

In the allocation layer, realized variance, implied variance and VRP-related transformations are explanatory features. Their purpose is to improve estimates of future stress probabilities.

The resulting investment payoff remains an equity–bond portfolio payoff.

In the direct-variance layer, lagged implied variance and subsequently observed realized variance define a variance-linked payoff:

\[
\widetilde{\Pi}^{short}_t
=
\frac{
IV_{t-1}-RV_t
}{
IV_{t-1}
}
\]

The resulting strategy return is produced by scaling this payoff with a lagged volatility estimate and a constrained notional.

A variable can therefore possess predictive information without generating an attractive equity–bond allocation.

Conversely, a variance-linked payoff can generate positive economic value even when the same variable adds little to an allocation model.

The thesis results demonstrate precisely this distinction.

---

### 2.2 Allocation evidence

The allocation evidence is modest in both markets.

In the United States:

- the strongest benchmark Sharpe ratio is 1.025 for 1/N Equity–Bond;
- the strongest HMM Sharpe ratio is 1.019 for HMM RV + Log VRP;
- the strongest RSM Sharpe ratio is 0.949 for RSM RV + Raw VRP;
- the strongest ML Sharpe ratio is 1.002 for ML Logistic Base.

HMM RV + Log VRP improves maximum drawdown to −16.67%, compared with −20.06% for 60/40 and −19.10% for 1/N.

However, its average turnover is 25.35%. Partial rebalancing reduces this value to 9.10%, but does not create benchmark dominance.

In Europe:

- Buy-and-Hold Equity has a Sharpe ratio of 0.313;
- 60/40 has a Sharpe ratio of 0.292;
- 1/N has a Sharpe ratio of 0.280;
- the strongest RSM reaches 0.281;
- the strongest HMM reaches 0.218;
- the strongest ML allocation reaches 0.274.

The European Random Forest with VRP contains incremental predictive information, but its economic and welfare performance remains statistically indistinguishable from simple benchmarks.

The appropriate allocation conclusion is:

> VRP-related variables contain conditional predictive information, but their inclusion in the tested HMM, RSM and machine-learning allocation models does not establish robust economic superiority over simple equity–bond portfolios.

---

### 2.3 Direct variance-payoff evidence

The direct-variance diagnostics reveal positive average carry and negative skewness in both markets.

| Market | Positive-payoff rate | Mean normalized payoff | Skewness | Worst normalized payoff |
|---|---:|---:|---:|---:|
| United States | 82.42% | 0.253 | −3.849 | −4.432 |
| Europe | 78.35% | 0.239 | −2.231 | −2.439 |

These distributions reflect the central economic structure of short variance.

The strategy earns frequent positive payoffs when implied variance exceeds subsequent realized variance, but remains exposed to infrequent and severe losses.

### United States

The selected United States strategy is Direct Short Variance 10% Vol with a High-VRP gate.

It produces:

- annualized return of 6.23%;
- annualized volatility of 7.17%;
- Sharpe ratio of 0.882;
- Sortino ratio of 1.218;
- maximum drawdown of −23.46%.

Its headline Sharpe ratio is slightly above those of the aligned 60/40 and 1/N portfolios.

However, at a risk-aversion coefficient of five:

- its mean–variance certainty equivalent is approximately 5.04%;
- its fee-equivalent difference is approximately −71 basis points relative to 60/40;
- its fee-equivalent difference is approximately −45 basis points relative to 1/N;
- both bootstrap confidence intervals contain zero.

The strategy therefore does not establish robust welfare dominance.

### Europe

The selected European strategy is Direct Short Variance 10% Vol with exposure restricted to months in which the lagged VRP is positive.

It produces:

- annualized return of 13.08%;
- annualized volatility of 9.70%;
- Sharpe ratio of 1.324;
- Sortino ratio of 1.891;
- maximum drawdown of −21.36%.

At a risk-aversion coefficient of five:

- its mean–variance certainty equivalent is approximately 10.49%;
- its CRRA certainty equivalent is approximately 10.67%;
- its fee-equivalent advantage is approximately 927 basis points relative to 60/40;
- its fee-equivalent advantage is approximately 899 basis points relative to 1/N.

The lower bootstrap confidence bounds remain positive against both benchmarks.

Within the tested framework, the European welfare advantage is therefore statistically significant.

---

## 3. Evaluation of the hypotheses

### 3.1 Hypothesis 1 — Positive variance carry with negative skewness

The first hypothesis predicted that implied variance would exceed subsequent realized variance in a majority of observations, producing frequent positive carry combined with severe downside risk.

This hypothesis is supported in both markets.

The short-variance payoff is positive in:

- 82.42% of United States observations;
- 78.35% of European observations.

Both normalized payoff distributions are negatively skewed and contain losses below −100% of the strike-normalized exposure.

The positive average carry must therefore not be interpreted independently of tail risk.

---

### 3.2 Hypothesis 2 — Limited allocation-model dominance

The second hypothesis predicted that VRP-related variables could improve stress identification or downside control without consistently dominating simple benchmarks.

This hypothesis is supported.

The strongest HMM, RSM and ML portfolios remain close to or below the strongest benchmarks in Sharpe ratio.

The United States HMM improves maximum drawdown, while the European Random Forest with VRP provides incremental prediction information.

Neither result establishes general allocation superiority.

---

### 3.3 Hypothesis 3 — Payoff-structure dependence

The third hypothesis predicted that the value of VRP would depend on the mechanism through which it is monetized.

This hypothesis receives the strongest support.

The inclusion of VRP as an allocation feature generates modest results, while the European direct variance-payoff approximation generates economically large and statistically significant welfare gains.

The underlying variable is similar, but the payoff mapping differs.

The result confirms that predictive relevance and investment value must be evaluated separately.

---

### 3.4 Hypothesis 4 — Cross-market heterogeneity

The fourth hypothesis predicted material differences between the United States and Europe.

This hypothesis is supported.

The selected United States direct strategy does not produce statistically significant welfare gains.

The selected European strategy produces positive lower confidence bounds against both benchmarks.

However, this cross-market heterogeneity must not be interpreted as proof that European variance carry is structurally superior in all periods.

The result may depend on:

- sample dates;
- volatility-index construction;
- option-market structure;
- crisis composition;
- source quality;
- equity and bond proxies;
- the approximation used to construct the payoff.

---

### 3.5 Hypothesis 5 — Importance of implementation constraints

The fifth hypothesis predicted that implementation controls would materially affect the results.

This hypothesis is supported.

For equity–bond allocation, partial rebalancing reduces HMM turnover from 25.35% to 9.10%.

For direct variance carry, the analysis demonstrates the importance of:

- monthly roll costs;
- long lagged-risk windows;
- notional constraints;
- entry filters;
- subperiod analysis;
- crisis exclusions;
- investor risk aversion.

The United States strategy becomes unstable under a short 12-month risk window, reaching a maximum drawdown above 50%.

The European result remains strong under the tested implementation variations, but its magnitude still depends on a stylized payoff framework.

---

## 4. Data limitations

### 4.1 Cross-market data comparability

The United States and European datasets are not perfectly comparable.

The United States uses:

- SPY or the S&P 500 as the equity proxy;
- VIX as the implied-volatility proxy;
- AGG as the bond proxy.

Europe uses:

- EURO STOXX 50 as the equity proxy;
- VSTOXX or V2TX as the implied-volatility proxy;
- IEAG.AS as the bond proxy.

These instruments differ in:

- market composition;
- currency exposure;
- duration;
- liquidity;
- index methodology;
- investor base;
- derivatives-market depth.

Differences in strategy results may therefore reflect both economic variation and proxy construction.

---

### 4.2 VSTOXX reconstruction

The European VSTOXX history is reconstructed from multiple source segments and stored locally.

The date parsing and long-gap problems identified during the empirical process were corrected.

ISO dates are now interpreted explicitly as year-month-day, and returns crossing calendar interruptions longer than seven days are invalidated.

These corrections materially improve the reliability of the European results.

Nevertheless, residual limitations remain.

Different source segments may contain:

- distinct timestamp conventions;
- rounding differences;
- source-specific revisions;
- methodology differences;
- discontinuities at the merge point.

The corrected European results are more reliable than the earlier estimates, but they are not equivalent to a single uninterrupted official institutional dataset.

---

### 4.3 Sample length

The principal allocation samples contain:

| Market | Monthly features | Allocation OOS | Direct-variance strategies |
|---|---:|---:|---:|
| United States | 257 | 184 | 232 |
| Europe | 195 | 122 | 170 |

The European allocation sample is particularly limited for estimating nonlinear and regime-dependent models.

A 122-month out-of-sample period contains only a small number of major market regimes.

This reduces statistical power and makes the results more sensitive to individual episodes.

The direct-variance samples are longer, but remain insufficient to observe a large number of independent volatility crises.

---

### 4.4 Monthly frequency

Monthly analysis is appropriate for strategic portfolio allocation, but it suppresses intramonth information.

A volatility shock can begin, peak and partially reverse within a single month.

A monthly model may:

- detect the event late;
- obscure the path of losses;
- understate turnover required within the month;
- ignore temporary liquidity needs;
- miss daily margin pressure.

The monthly design should therefore be interpreted as a strategic research framework rather than a high-frequency execution model.

---

## 5. Measurement limitations

### 5.1 Implied-variance proxy

The thesis approximates implied variance as:

\[
IV_t
=
\left(
\frac{V_t}{100}
\right)^2
\]

where \(V_t\) is VIX or VSTOXX.

This approximation is transparent and reproducible, but it is not identical to an investable variance-swap strike.

An exact strike would require:

- the full option surface;
- maturity interpolation;
- forward-price estimation;
- strike integration or summation;
- tail extrapolation;
- contract-specific conventions.

The volatility-index square is therefore best understood as a model-based strike proxy.

---

### 5.2 Realized-variance proxy

Realized variance is constructed as a trailing 21-observation annualized measure:

\[
RV_d
=
\frac{252}{21}
\sum_{j=0}^{20}
r_{d-j}^{2}
\]

It is sampled at month-end.

This measure does not reproduce exact contractual settlement over a fixed calendar interval.

It may also be affected by:

- close-to-close measurement;
- market holidays;
- asynchronous source dates;
- price corrections;
- overnight jumps;
- microstructure effects not visible in daily data.

Future work using intraday observations could construct realized kernels, jump-robust estimates or exact contract-matched realized variance.

---

### 5.3 Difference between physical and risk-neutral objects

Option-implied variance reflects risk-neutral pricing and compensation for volatility risk.

Realized variance is observed under the physical historical process.

The spread between the two quantities therefore combines several components:

- expected future variance;
- volatility-risk compensation;
- jump-risk compensation;
- model and measurement differences;
- volatility-index construction effects.

The empirical VRP proxy should not be interpreted as a pure structural risk premium without qualification.

---

### 5.4 Exploratory Pure VRP Proxy

The Pure VRP Proxy remains an exploratory transformation.

It does not impose:

- a forward contractual strike;
- a subsequent settlement date;
- notional scaling;
- a volatility target;
- monthly roll costs;
- derivative execution constraints.

Its high historical performance cannot be used as evidence of an available traded return.

It is retained only to illustrate the information contained in the implied-to-realized variance relationship.

---

## 6. Direct-payoff and capital-mapping limitations

### 6.1 Normalized payoff is not return on invested capital

The normalized payoff is:

\[
\frac{
IV_{t-1}-RV_t
}{
IV_{t-1}
}
\]

This quantity has no direct equivalence to the return on a fully specified capital account.

Variance swaps are typically expressed using variance notional and payoff conventions that differ from an initial cash investment.

The thesis converts the normalized payoff into a synthetic portfolio return through risk-targeted notional scaling.

This mapping is useful for comparing risk-adjusted performance, but it remains model dependent.

---

### 6.2 Ex ante target versus realized volatility

The strategy uses a lagged payoff-volatility estimate to target either 5% or 10% annual volatility.

The target is ex ante.

It does not guarantee ex post volatility.

The United States always-active 10% strategy realizes volatility above 16%, demonstrating that lagged standard deviation can severely underestimate future tail exposure.

This is a fundamental limitation of volatility targeting for negatively skewed strategies.

---

### 6.3 Monthly roll costs

The model applies transaction costs to the full absolute notional initiated each month.

This is more appropriate than charging only for the change in desired exposure.

However, the cost assumption remains stylized.

It does not reproduce:

- actual dealer quotations;
- option-replication spreads;
- crisis-time widening;
- transaction-size effects;
- financing charges;
- legal and documentation costs;
- counterparty valuation adjustments.

Robustness up to 50 basis points does not prove that all actual implementation costs would lie below that level.

---

### 6.4 Margin, collateral and liquidity

The framework does not model:

- initial margin;
- variation margin;
- collateral remuneration;
- liquidity buffers;
- forced deleveraging;
- intramonth margin calls;
- counterparty default;
- close-out costs.

These omissions are particularly important for short variance.

A strategy can finish a month with a manageable final payoff while experiencing a severe intramonth mark-to-market loss.

An investor may be forced to reduce or close the position before settlement.

The monthly return series cannot capture this path dependency.

---

## 7. Model limitations

### 7.1 Two-regime assumption

The HMM and RSM frameworks use two regimes:

1. normal;
2. stress.

This structure is parsimonious and interpretable, but it compresses several economically distinct environments into a single stress state.

Potentially distinct regimes include:

- deflationary equity crashes;
- inflationary equity–bond drawdowns;
- liquidity crises;
- volatility shocks without persistent recession;
- post-crisis recoveries;
- high-volatility expansions.

A two-state model may not differentiate these environments adequately.

---

### 7.2 Regime-label instability

Latent states are not directly observed.

The identity of the stress state can change across rolling estimation windows.

A state associated with high volatility in one window may represent a different combination of returns and variance in another.

The implementation identifies stress through the state’s estimated characteristics, but some label uncertainty remains unavoidable.

---

### 7.3 Rolling-window choice

The allocation models use a 72-month rolling estimation window.

This choice balances adaptability and statistical stability, but remains a modelling assumption.

A shorter window:

- responds faster;
- uses fewer observations;
- increases parameter uncertainty.

A longer window:

- improves estimation stability;
- may retain obsolete historical relationships;
- reacts more slowly to structural change.

A broader window analysis would strengthen the allocation-model robustness assessment.

---

### 7.4 Machine-learning label and threshold

The ML stress label is defined using the next equity return and next realized variance relative to rolling quantiles.

This definition is economically intuitive, but not unique.

Alternative labels could use:

- drawdown;
- volatility jumps;
- joint equity–bond losses;
- liquidity stress;
- credit spreads;
- recession indicators.

The classification threshold of 0.50 and the 80%–20% allocation mapping also influence the resulting portfolio.

ML performance therefore reflects both predictive quality and design choices governing how probabilities are converted into trades.

---

### 7.5 Model-selection risk

Several feature transformations, model families, filters and calibration values are evaluated.

This creates a risk that some results appear attractive through sample-specific selection.

The thesis mitigates this risk through:

- rolling out-of-sample estimation;
- benchmark comparison;
- cross-market analysis;
- common-sample sensitivity tests;
- subperiod analysis;
- bootstrap welfare inference.

These controls reduce but do not eliminate specification-search risk.

---

## 8. Statistical limitations

### 8.1 Historical backtest evidence

The thesis relies on historical backtests.

Rolling out-of-sample estimation reduces look-ahead bias, but historical performance does not prove future profitability.

Structural relationships may change because of:

- regulation;
- market participation;
- volatility-product development;
- monetary policy;
- dealer balance-sheet constraints;
- systematic volatility-selling strategies;
- crisis composition.

The observed European result may weaken or reverse in a future sample.

---

### 8.2 Limited number of tail events

The direct-variance payoff is strongly negatively skewed.

Its economic risk depends disproportionately on a small number of extreme observations.

Even a sample of 170 or 232 monthly strategy observations contains relatively few major volatility shocks.

Estimates of:

- maximum drawdown;
- CVaR;
- CRRA utility;
- optimal notional;
- tail-loss probability

are therefore subject to considerable uncertainty.

---

### 8.3 Bootstrap limitations

The welfare analysis uses:

- 2,000 block-bootstrap replications;
- six-month blocks;
- comparisons against 60/40 and 1/N.

The block structure preserves part of the serial dependence in returns.

However, the results can depend on:

- block length;
- bootstrap method;
- number of replications;
- treatment of structural breaks;
- finite-sample tail behavior.

Positive confidence bounds increase confidence in the European result, but do not establish a universal population parameter.

---

### 8.4 Multiple testing

The empirical framework evaluates several:

- HMM features;
- RSM features;
- ML algorithms;
- VRP transformations;
- variance-entry gates;
- risk windows;
- notional caps;
- cost levels;
- subperiods.

This creates multiple-testing risk.

The analysis does not apply a complete familywise correction such as a White Reality Check or a Superior Predictive Ability test across every specification.

The strongest result should therefore be interpreted as validated within the stated robustness design, not as immune to data-snooping concerns.

---

### 8.5 Certainty-equivalent assumptions

Mean–variance certainty equivalent assumes that investor preferences can be summarized by expected return and variance.

This approximation may be inadequate for strongly skewed short-variance payoffs.

The CRRA certainty equivalent addresses part of this limitation, but still depends on:

- a specific utility function;
- the chosen risk-aversion coefficient;
- monthly return aggregation;
- absence of intermediate liquidity constraints.

Welfare estimates should therefore complement, rather than replace, distributional and implementation analysis.

---

## 9. Cross-market interpretation limitations

### 9.1 Sample-specific asymmetry

The European direct-variance result is stronger than the United States result in the observed samples.

This should not be interpreted as proof that Europe offers a permanently larger or more exploitable variance premium.

The difference may reflect:

- sample start dates;
- the frequency and timing of crises;
- volatility-index methodologies;
- equity-market composition;
- monetary-policy regimes;
- source reconstruction;
- differences in realized-variance dynamics.

The thesis identifies cross-market heterogeneity but does not establish its causal origin.

---

### 9.2 Different evidence-layer samples

The allocation and direct-variance layers use different aligned samples.

Allocation results contain 184 United States observations and 122 European observations.

Direct-variance results contain 232 United States observations and 170 European observations.

A higher Sharpe ratio in the direct-variance layer cannot be attributed solely to payoff structure without acknowledging the difference in evaluation dates.

The thesis therefore avoids a mechanical pooled ranking across evidence layers.

---

### 9.3 External validity

Only two developed equity markets are examined.

The results cannot automatically be generalized to:

- the United Kingdom;
- Japan;
- emerging markets;
- individual equities;
- commodities;
- foreign exchange;
- interest-rate volatility.

Additional markets would be required to determine whether the European result represents a broader phenomenon or a region-specific historical outcome.

---

## 10. Principal empirical findings

Six principal findings emerge.

### Finding 1 — Positive carry is accompanied by severe tail risk

The short-variance payoff is positive in the majority of observations in both markets.

However, both distributions are negatively skewed and contain severe losses.

Average carry is therefore not sufficient to evaluate economic value.

### Finding 2 — Simple allocation benchmarks remain difficult to beat

The 60/40 and 1/N portfolios remain highly competitive.

Dynamic models can improve selected risk measures, but generally require substantially more turnover.

### Finding 3 — VRP information is model dependent

Raw and log VRP transformations do not produce uniform improvements.

The strongest US ML portfolio excludes VRP, whereas the strongest European ML portfolio includes it.

The value of the variable depends on the model family and transformation.

### Finding 4 — United States direct variance is not welfare dominant

The High-VRP strategy improves headline Sharpe and drawdown relative to aligned balanced benchmarks.

Its certainty-equivalent differences are not statistically positive.

The result is economically plausible but not dominant.

### Finding 5 — European direct variance is strong within the tested model

The positive-VRP strategy produces a Sharpe ratio of 1.324 and large welfare gains.

The result survives the tested costs, risk windows, notional caps, subperiods, crisis exclusions and risk-aversion levels.

### Finding 6 — Payoff structure is central

The most important finding is not a universal ranking of the United States and Europe.

It is that the economic value of VRP changes materially when it is transformed from an allocation feature into a variance-linked payoff.

---

## 11. Answer to the research question

The research question is:

> Does the Variance Risk Premium create more economic value through direct variance carry or through its informational content for dynamic asset allocation?

The empirical answer is conditional.

For equity–bond allocation, VRP-related variables contain useful but model-dependent information. They can improve stress classification and selected downside-risk measures, but they do not establish robust benchmark dominance.

For the United States direct-variance approximation, positive carry and improved headline risk-adjusted performance do not translate into statistically significant welfare superiority.

For the European direct-variance approximation, the positive-VRP strategy produces economically large and bootstrap-significant welfare gains within the tested sample.

The most defensible answer is therefore:

> The Variance Risk Premium does not possess a single market-independent form of economic value. In this thesis, its economic contribution depends more on the payoff structure through which it is harvested than on its mere inclusion as a state variable. The direct variance-payoff approximation generates substantially stronger evidence in Europe, while neither the allocation channel nor the direct-payoff channel establishes robust welfare dominance in the United States.

This answer is empirical rather than universal.

It applies to the tested data, markets, models and implementation assumptions.

---

## 12. Contribution of the thesis

The thesis makes five principal contributions.

### 12.1 Separation of information and payoff

The first contribution is conceptual.

The thesis separates VRP as an informational variable from VRP as the basis of a variance-linked payoff.

This prevents predictive content from being confused with investment profitability.

### 12.2 Cross-market evaluation

The second contribution is the comparison between the United States and Europe.

The results demonstrate that conclusions obtained in one market should not be transferred mechanically to another.

### 12.3 Strict temporal alignment

The third contribution is methodological.

The empirical pipeline uses:

- rolling out-of-sample estimation;
- one-step-ahead allocation;
- lagged implied variance;
- subsequent realized-variance settlement;
- strictly lagged risk estimation;
- lagged filter thresholds.

These choices reduce look-ahead bias.

### 12.4 Welfare and implementation analysis

The fourth contribution is economic.

Strategies are evaluated not only through Sharpe ratios but also through:

- downside risk;
- turnover;
- roll costs;
- certainty equivalents;
- bootstrap confidence intervals;
- notional constraints;
- subperiods;
- crisis exclusions.

### 12.5 Reproducible correction of European data

The fifth contribution is empirical reliability.

The European date-parsing and gap-contamination problems were identified, corrected and incorporated into a reproducible pipeline.

The corrected data materially change the interpretation of the European variance premium.

This demonstrates the importance of data auditing in quantitative research.

---

## 13. Implications for investors and researchers

### 13.1 Implications for allocation investors

Investors should not assume that adding a sophisticated regime model will automatically improve a balanced portfolio.

Simple benchmarks remain difficult to outperform after turnover.

Regime models may nevertheless have value when the objective prioritizes:

- maximum-drawdown reduction;
- smoother exposure changes;
- explicit stress probabilities;
- defensive overlays.

Partial rebalancing is more effective than simple no-trade bands in reducing turnover for the selected US HMM.

---

### 13.2 Implications for volatility investors

Positive average variance carry should never be evaluated without:

- tail-loss measurement;
- notional scaling;
- margin analysis;
- collateral requirements;
- crisis liquidity;
- settlement conventions.

The strong European result warrants further investigation, but not immediate interpretation as a directly tradable return.

An institutional implementation would require a complete derivative-pricing and execution layer.

---

### 13.3 Implications for empirical research

The results show that data quality can reverse an empirical conclusion.

The original European interpretation was driven by a date-parsing error that severely reduced the usable VSTOXX sample.

Quantitative research should therefore include explicit tests for:

- date formats;
- duplicate observations;
- missing periods;
- calendar gaps;
- alignment across assets;
- feature identities;
- look-ahead bias;
- common-sample comparability.

---

## 14. Future research

Several extensions would materially strengthen the analysis.

### 14.1 Exact variance-swap replication

Future work should construct fair variance strikes from option chains using the appropriate replication formula.

This would replace the volatility-index-square approximation with contract-matched forward variance.

### 14.2 Observed derivative data

Institutional variance-swap quotes or proprietary dealer data would allow:

- observed bid–ask spreads;
- exact maturities;
- contract rolls;
- collateral assumptions;
- executable notional conventions.

### 14.3 Option-based replication

A complementary approach could backtest delta-hedged option portfolios designed to approximate variance exposure.

This would permit direct measurement of:

- option transaction costs;
- hedge rebalancing;
- discrete-strike effects;
- tail truncation;
- volatility-surface dynamics.

### 14.4 Higher-frequency realized variance

Intraday data could support:

- realized kernels;
- bipower variation;
- jump decomposition;
- overnight-return treatment;
- more accurate settlement matching.

### 14.5 External validation

The models should be tested on:

- the United Kingdom;
- Japan;
- global developed markets;
- alternative European indices;
- later holdout periods not used for any model selection.

### 14.6 Stronger statistical corrections

Future work could add:

- White Reality Check;
- Hansen Superior Predictive Ability test;
- false-discovery-rate control;
- model-confidence sets;
- bootstrap Sharpe-difference tests;
- nested forecast-comparison procedures.

### 14.7 Dynamic transaction and margin costs

A more realistic implementation model could link costs and margin requirements to:

- volatility level;
- market stress;
- trade size;
- dealer balance-sheet conditions;
- liquidity indicators.

### 14.8 Alternative allocation mappings

Future work could test nonlinear mappings from stress probability to portfolio weights, including:

- threshold allocation;
- volatility scaling;
- expected-utility optimization;
- constrained mean–CVaR allocation;
- probability calibration before weight conversion.

---

## 15. Final conclusion

This thesis studied whether the Variance Risk Premium creates greater economic value as an informational input for dynamic equity–bond allocation or through a model-based direct variance-payoff approximation.

The allocation evidence is disciplined but modest.

Hidden Markov Models, Markov-switching regressions and machine-learning classifiers produce feasible dynamic portfolios and occasionally improve selected downside-risk measures. They do not consistently outperform simple benchmarks after turnover and implementation costs.

The direct-variance evidence reveals a different economic mechanism.

Both markets exhibit frequent positive carry and severe negative skewness.

In the United States, a High-VRP filter improves the strategy profile, but welfare superiority is not statistically established.

In Europe, the positive-VRP strategy generates strong risk-adjusted returns and bootstrap-significant certainty-equivalent gains. Its performance remains robust across the tested transaction costs, risk windows, notional caps, subperiods, crisis exclusions and levels of risk aversion.

Nevertheless, the European strategy remains an approximation.

It does not reconstruct an exact variance-swap strike, contractual variance notional, collateral account, margin path, bid–ask spread or daily mark-to-market process.

The final conclusion is therefore deliberately precise:

> The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested. In the tested European sample, a model-based direct variance-payoff approximation produces substantial and robust economic value, whereas the inclusion of VRP as a state variable in dynamic equity–bond allocation produces only limited gains. In the United States, neither channel establishes robust investor-welfare dominance over traditional portfolios.

This conclusion does not identify a universal trading strategy.

It identifies a methodological principle: the economic value of a financial signal cannot be separated from the payoff, risk controls and implementation mechanism used to monetize it.
