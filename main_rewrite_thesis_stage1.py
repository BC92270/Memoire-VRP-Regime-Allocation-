from __future__ import annotations

from pathlib import Path


THESIS = Path("thesis")

ABSTRACT_PATH = (
    THESIS
    / "abstract_keywords.md"
)

INTRODUCTION_PATH = (
    THESIS
    / "introduction_draft.md"
)

EMPIRICAL_PACK = (
    THESIS
    / "empirical_update_pack.md"
)


ABSTRACT_TEXT = r"""# Abstract and Keywords

## Abstract

This thesis investigates whether the Variance Risk Premium creates more economic value when it is harvested through a model-based direct variance-payoff approximation or when it is used as an informational variable inside regime-based equity–bond allocation models. The analysis compares the United States and Europe and deliberately separates two empirical evidence layers: dynamic asset allocation and direct variance carry. This separation is necessary because the two approaches use different payoff structures, aligned samples and implementation assumptions.

The allocation framework evaluates buy-and-hold equity, 60/40 and equal-weighted equity–bond benchmarks against Hidden Markov Models, Markov-switching regressions and machine-learning stress classifiers. The regime models use realized variance, implied variance and alternative transformations of the Variance Risk Premium. They are estimated through rolling out-of-sample procedures and evaluated using annualized return, volatility, Sharpe and Sortino ratios, maximum drawdown, tail-risk measures, turnover and welfare metrics.

The direct-variance extension approximates the payoff from selling one-month variance exposure. The strike proxy is lagged implied variance derived from the relevant volatility index, while settlement is represented by the subsequent annualized trailing realized-variance measure. Exposure is sized using strictly lagged volatility estimates, subject to notional caps and monthly roll costs. The resulting series is a model-based capital mapping from a normalized variance payoff and must not be interpreted as an observed variance-swap return.

The asset-allocation evidence is modest. In the United States, the strongest HMM specification, HMM RV + Log VRP, achieves a Sharpe ratio of 1.019 compared with 1.025 for the equal-weighted equity–bond benchmark. It improves maximum drawdown but does not establish robust benchmark dominance. In Europe, the strongest HMM or RSM specification reaches a Sharpe ratio of 0.281, compared with 0.313 for buy-and-hold equity. Machine-learning models provide incremental predictive information in some specifications, particularly the European Random Forest with VRP, but do not produce statistically significant welfare gains relative to simple benchmarks.

The direct-variance evidence differs sharply across markets. In the United States, the High-VRP strategy generates an annualized return of 6.23%, volatility of 7.17% and a Sharpe ratio of 0.882. Its welfare advantage relative to 60/40 and equal-weighted allocation is not statistically significant. In Europe, the strategy that takes exposure only when the lagged VRP is positive generates an annualized return of 13.08%, volatility of 9.70% and a Sharpe ratio of 1.324. At a risk-aversion coefficient of five, its mean–variance certainty-equivalent advantage is approximately 927 basis points relative to 60/40 and 899 basis points relative to equal-weighted allocation. Bootstrap confidence intervals remain positive against both benchmarks.

The main conclusion is that the economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested. Adding VRP variables to regime-detection or machine-learning allocation models produces limited and model-dependent gains. The model-based direct variance-payoff approximation produces much stronger European evidence, although its results remain subject to substantial implementation limitations. The framework does not reconstruct exact variance-swap strikes, option surfaces, collateral accounts, bid–ask spreads, margin paths or daily mark-to-market dynamics.

## Keywords

Variance Risk Premium; implied variance; realized variance; variance carry; direct variance-payoff approximation; Hidden Markov Model; Markov-switching regression; machine learning; regime-based allocation; equity–bond allocation; certainty equivalent; bootstrap inference; downside risk; transaction costs; VIX; VSTOXX.
"""


INTRODUCTION_TEXT = r"""# Introduction Draft

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
"""


def require_empirical_pack() -> None:
    if not EMPIRICAL_PACK.exists():
        raise FileNotFoundError(
            f"Missing empirical source: "
            f"{EMPIRICAL_PACK}"
        )

    text = EMPIRICAL_PACK.read_text(
        encoding="utf-8"
    )

    required_markers = [
        "EU direct-variance evidence",
        (
            "Direct Short Variance "
            "10% Vol (VRP > 0)"
        ),
        (
            "Statistically Superior "
            "vs 60/40"
        ),
        (
            "Mandatory methodological "
            "terminology"
        ),
    ]

    for marker in required_markers:
        if marker not in text:
            raise AssertionError(
                f"Empirical pack missing: "
                f"{marker}"
            )


def validate_text(
    text: str,
    label: str,
) -> None:
    stale_phrases = [
        "collapses in Europe",
        "collapses in the European",
        (
            "more useful as a "
            "regime-state variable"
        ),
        (
            "more useful as a conditional "
            "market-state signal"
        ),
        (
            "Direct synthetic VRP exposure "
            "is not robust"
        ),
        "-2.8511",
        "-0.3625",
        "-0.9901",
        "0.1281",
    ]

    for phrase in stale_phrases:
        if phrase.lower() in text.lower():
            raise AssertionError(
                f"{label}: stale phrase: "
                f"{phrase}"
            )

    if len(text.split()) < 250:
        raise AssertionError(
            f"{label}: text unexpectedly short."
        )


def main() -> None:
    require_empirical_pack()

    validate_text(
        ABSTRACT_TEXT,
        "Abstract",
    )

    validate_text(
        INTRODUCTION_TEXT,
        "Introduction",
    )

    ABSTRACT_PATH.write_text(
        ABSTRACT_TEXT.strip() + "\n",
        encoding="utf-8",
    )

    INTRODUCTION_PATH.write_text(
        INTRODUCTION_TEXT.strip() + "\n",
        encoding="utf-8",
    )

    print("=" * 100)
    print(
        "THESIS REWRITE STAGE 1 COMPLETE"
    )
    print("=" * 100)

    print(
        f"Updated: {ABSTRACT_PATH}"
    )

    print(
        f"Updated: {INTRODUCTION_PATH}"
    )

    print(
        "Abstract words: "
        f"{len(ABSTRACT_TEXT.split())}"
    )

    print(
        "Introduction words: "
        f"{len(INTRODUCTION_TEXT.split())}"
    )


if __name__ == "__main__":
    main()
