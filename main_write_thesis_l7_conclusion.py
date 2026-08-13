from __future__ import annotations

from pathlib import Path
import re


TARGET = Path(
    "thesis/latex/sections/"
    "06_conclusion.tex"
)


TEXT = r"""
\section{Discussion and Conclusion}
\label{sec:conclusion}

This thesis returns to the research question stated in the introduction: \emph{Does the Variance Risk Premium create more economic value as an informational state variable for dynamic equity--bond allocation or through a model-based direct variance-payoff approximation, and how robust is this distinction across the United States and Europe?}

The empirical answer is conditional rather than universal. VRP-related variables contain useful information in selected allocation models, but their inclusion does not establish robust superiority over simple equity--bond benchmarks. The direct-payoff evidence is stronger, particularly in Europe, yet the economic interpretation remains constrained by the fact that the variance exposure is modeled rather than reconstructed from executable derivative contracts.

The central result is therefore not that one universally optimal VRP strategy has been identified. It is that the economic value associated with variance information depends critically on the mechanism through which that information is transformed into portfolio payoffs.

\subsection{Answer to the research question}

The allocation channel provides evidence of informational content but limited incremental portfolio value.

In the United States, HMM RV + Log VRP reaches a Sharpe ratio of 1.019, compared with 1.025 for the strongest balanced benchmark. The model improves maximum drawdown relative to 60/40 and equal weighting, but requires substantially more turnover. Partial rebalancing improves implementability without creating benchmark dominance. The strongest United States machine-learning allocation, ML Logistic Base, does not use the VRP-enhanced feature set.

In Europe, the allocation evidence is weaker. The strongest HMM reaches a Sharpe ratio of 0.218, the strongest RSM 0.281, and the strongest machine-learning allocation 0.274, compared with 0.313 for buy-and-hold equity. VRP variables can still contribute information within individual models. In particular, the European Random Forest with VRP improves stress-classification metrics. That predictive improvement, however, does not translate into statistically robust welfare gains relative to the traditional allocation benchmarks.

The direct-payoff channel produces a different result.

In the United States, the selected High-VRP strategy generates a Sharpe ratio of 0.882 and has defensive characteristics relative to alternative direct-variance specifications. At a risk-aversion coefficient of five, however, its mean--variance certainty-equivalent differences remain approximately -71 basis points relative to 60/40 and -45 basis points relative to equal weighting. The corresponding bootstrap confidence intervals include zero. The strategy therefore does not establish robust investor-welfare dominance.

In Europe, the selected strategy takes exposure only when lagged VRP is positive. It generates an annualized return of 13.08\%, annualized volatility of 9.70\%, and a Sharpe ratio of 1.324. At a risk-aversion coefficient of five, its mean--variance certainty-equivalent advantage is approximately 927 basis points relative to 60/40 and 899 basis points relative to equal weighting. The lower bootstrap confidence bounds remain positive against both benchmarks.

Robustness analysis reinforces rather than eliminates this difference. The European result remains economically strong under costs up to 50 basis points, risk-estimation windows from 12 to 60 months, a maximum notional reduced to 5\%, separate subperiods, major-crisis exclusions, and risk-aversion coefficients from one to ten. The United States direct strategy is materially less stable, particularly under a short 12-month risk-estimation window and across subperiods.

The most defensible answer to the research question is therefore the following:

\begin{quote}
The Variance Risk Premium does not possess a single market-independent form of economic value. In this thesis, its economic contribution depends more on the payoff structure through which it is harvested than on its mere inclusion as a state variable. The direct variance-payoff approximation generates substantially stronger evidence in Europe, while neither the allocation channel nor the direct-payoff channel establishes robust welfare dominance in the United States.
\end{quote}

This answer applies to the tested data, samples, models, and implementation assumptions. It should not be interpreted as a universal ranking of markets or as evidence that a directly executable variance strategy has been identified.

\subsection{Predictive information and economic value}

One of the main implications of the results is that predictive information and economic value should be treated as separate empirical objects.

In the allocation layer, VRP-related variables influence estimated stress states or classification probabilities. Their economic value depends on several subsequent transformations: how accurately stress is identified, how probabilities are converted into portfolio weights, how frequently those weights change, and whether the resulting reduction in losses compensates for lower participation in favorable equity markets and higher turnover.

The European machine-learning result illustrates this distinction clearly. The Random Forest with VRP contains incremental predictive information, but this does not generate significant welfare dominance over 60/40 or equal weighting. A predictor can therefore be statistically informative without being economically sufficient.

The direct-payoff layer changes the problem. Lagged implied variance and subsequent realized variance enter the payoff itself rather than merely conditioning an equity--bond decision. The same broad class of variance information can consequently possess a different economic value when embedded in a different payoff structure.

This distinction is the principal conceptual contribution of the thesis. It prevents two common interpretations from being conflated: that a predictor with forecasting power must generate an attractive portfolio, and that a positive variance spread must imply a superior dynamic allocation signal. The empirical evidence supports neither inference in general.

\subsection{Interpretation of the cross-market asymmetry}

The European direct-payoff evidence is substantially stronger than the corresponding United States evidence. This is a robust empirical observation within the tested samples, but its causal origin is not identified.

Several mechanisms could contribute to the difference. The two markets have different sample histories, volatility-index methodologies, equity compositions, derivatives-market structures, crisis sequences, and monetary environments. The European volatility history also requires greater source harmonization than the United States series. These differences make a purely structural interpretation inappropriate.

The evaluation samples also differ across evidence layers. The allocation exercises contain 184 United States and 122 European out-of-sample observations, while the direct-variance strategies contain 232 and 170 observations respectively. A higher Sharpe ratio in the direct-payoff layer therefore cannot be attributed mechanically to payoff design alone because the evaluation dates are not identical.

For this reason, the thesis does not conduct a pooled horse race between allocation and direct variance. The stronger European direct-payoff result is interpreted as evidence that the modeled payoff mechanism creates substantial economic value in that historical sample, not as proof that direct variance must dominate allocation in every common period or every market.

The same caution applies to the comparison between the United States and Europe. The evidence demonstrates cross-market heterogeneity. It does not establish that European variance carry is structurally or permanently larger.

\subsection{Data and measurement limitations}

The first group of limitations concerns data comparability.

The United States and European empirical systems use different equity, bond, and volatility proxies. Even when the economic concepts are matched, the underlying instruments differ in composition, duration, liquidity, index construction, and derivatives-market depth. Cross-market differences can therefore reflect both genuine economic heterogeneity and differences in measurement.

The European volatility history is particularly important. It is assembled from source segments that required explicit date-format and calendar-gap controls. The final pipeline treats ISO-formatted dates explicitly and invalidates returns that span interruptions longer than seven calendar days. These controls materially strengthen the European sample, but they do not make the reconstructed history equivalent to a single uninterrupted institutional data feed.

The second limitation concerns the measurement of implied variance. The thesis uses the square of VIX or VSTOXX, expressed in decimal volatility units, as a transparent implied-variance proxy. This is economically related to risk-neutral expected variance but is not identical to an exact forward variance-swap strike. Exact replication would require the relevant option surface, maturity matching, forward estimation, strike integration, tail treatment, and contract-specific conventions.

Realized variance is also an approximation. It is constructed from a trailing 21-observation window of daily equity returns and annualized before month-end sampling. This design is transparent and reproducible, but it does not reproduce the exact contractual settlement interval of a variance swap. Daily close-to-close data also omit part of the information available from intraday volatility estimators.

Finally, the empirical VRP proxy should not be interpreted as a pure structural risk premium. The difference between implied and realized variance can reflect expected future variance, compensation for volatility and jump risk, measurement choices, and characteristics of the volatility-index construction. The thesis studies the economic information contained in this empirical spread rather than claiming to isolate a unique structural parameter.

\subsection{Direct-payoff and implementation limitations}

The strongest result in the thesis also requires the strongest qualification.

The normalized short-variance payoff compares lagged implied variance with subsequent realized variance and scales that difference by the strike proxy. This normalized payoff is dimensionless. It is not an observed return on invested capital and does not correspond directly to the cash return of a fully specified variance-swap account.

Portfolio-level direct-variance returns are created by applying a lagged volatility target, an entry gate, and a constrained notional to that payoff. This allows the economic characteristics of the variance mechanism to be studied on a common return scale, but the capital mapping remains model dependent.

The implementation also operates at monthly frequency. A short-variance position can experience severe intramonth mark-to-market losses even when its final monthly settlement is manageable. The model does not include initial margin, variation margin, collateral remuneration, liquidity buffers, forced deleveraging, counterparty exposure, or close-out costs. These omissions are economically important because short-volatility strategies can become constrained precisely during periods of rapidly increasing volatility.

Transaction costs are treated more conservatively than a simple turnover model because the full absolute notional is charged each month when the one-month exposure is renewed. Nevertheless, the cost grid remains stylized. It does not reproduce dealer quotations, crisis-time bid--ask widening, option-replication costs, funding spreads, documentation costs, market impact, or capacity constraints.

Consequently, robustness up to 50 basis points should be interpreted as sensitivity to a stylized cost assumption. It is not evidence that all real implementation costs would remain below that value.

The European result is therefore best described as strong evidence for a model-based direct variance-payoff mechanism. It is not a verified historical return from an executable variance swap.

\subsection{Model and statistical limitations}

The regime models impose deliberately parsimonious structures. HMM and RSM specifications use two latent states, which makes state interpretation tractable but compresses potentially distinct market environments into a normal-versus-stress representation. Inflationary equity--bond drawdowns, liquidity crises, deflationary crashes, volatility shocks, and high-volatility recoveries need not belong to the same economic state.

The estimation design also imposes choices. HMM and RSM estimation begins after a 72-month burn-in and then uses an expanding estimation history. The machine-learning layer instead uses a fixed 72-month rolling training window. These choices balance parameter stability against adaptability, but alternative histories could change the results.

Machine-learning performance additionally depends on the stress-label definition, classification algorithm, feature set, and mapping from predicted stress probability to portfolio weights. A different definition of stress or a nonlinear allocation mapping could produce different economic outcomes even with identical predictor information.

Specification-search risk remains relevant. The thesis evaluates multiple HMM and RSM features, machine-learning algorithms, VRP transformations, entry gates, cost assumptions, risk windows, notional caps, and sample partitions. Rolling out-of-sample estimation, common-sample comparisons, benchmark discipline, robustness grids, and welfare bootstrap inference reduce the risk of overfitting, but they do not eliminate multiple-testing concerns.

The welfare bootstrap itself is an inferential approximation. It uses 2,000 paired moving-block replications with six-month blocks. This preserves part of the serial dependence in strategy and benchmark returns, but alternative block lengths or bootstrap methods could produce different confidence intervals.

Tail inference is especially difficult. The normalized direct-variance payoff is strongly negatively skewed, yet the final strategy samples contain only 232 United States and 170 European observations. The number of independent extreme volatility episodes is consequently small. Maximum drawdown, CVaR, CRRA utility, and the apparent stability of risk targeting remain sensitive to a limited set of tail observations.

The European bootstrap evidence is therefore meaningful but finite-sample. Positive lower confidence bounds support the conclusion inside the tested design; they do not identify an immutable population premium.

\subsection{Contribution of the thesis}

The thesis makes four main contributions.

First, it separates the informational and payoff uses of the Variance Risk Premium. This distinction allows predictive content to be evaluated independently from the economic properties of a variance-linked payoff.

Second, it applies the comparison across two markets rather than relying on a single United States result. The cross-market evidence demonstrates that conclusions about VRP are not automatically portable across regions or empirical constructions.

Third, the empirical design imposes strict temporal and implementation discipline. Allocation signals are evaluated out of sample, direct-payoff inputs are lagged appropriately, risk estimates and High-VRP thresholds exclude current settlement information, costs are incorporated, and strategies are compared against transparent benchmarks.

Fourth, the thesis evaluates economic value through more than headline Sharpe ratios. Drawdown, tail risk, turnover, certainty equivalents, bootstrap confidence intervals, cost sensitivity, notional constraints, subperiods, crisis exclusions, and risk-aversion sensitivity all contribute to the final interpretation.

The resulting contribution is therefore methodological as much as empirical. The thesis demonstrates that a financial variable should not be assigned economic value independently of the payoff mapping, benchmark, risk control, and implementation mechanism through which that value is measured.

\subsection{Directions for future research}

The most valuable extension would be to replace the volatility-index-based strike proxy with contract-matched forward variance constructed from option chains. This would require the full option surface, maturity interpolation, forward prices, appropriate strike integration, and tail treatment. It would materially reduce the distance between the current model-based approximation and an investable variance exposure.

A second extension would use observed derivative-market information. Variance-swap quotations, or a carefully constructed option-replication portfolio, would permit explicit modeling of bid--ask spreads, hedge costs, contract rolls, collateral, margin, and liquidity.

Higher-frequency data would also improve realized-variance measurement. Intraday observations could support realized kernels, jump-robust variation measures, and settlement windows matched more closely to derivative maturities.

External validation is equally important. The framework could be tested in the United Kingdom, Japan, additional European markets, other developed equity indices, and later holdout periods not used in the current model-selection process. Such evidence would help determine whether the European result reflects a broader variance-pricing phenomenon or a sample-specific historical outcome.

The allocation layer could be extended through richer regime structures, alternative definitions of stress, probability calibration, nonlinear mappings from state probability to weights, and explicit optimization under downside-risk constraints. Any additional complexity should continue to be evaluated against simple benchmark portfolios and after implementation costs.

Finally, stronger multiple-model inference could complement the current bootstrap design. Reality-check procedures, Superior Predictive Ability tests, model-confidence sets, false-discovery controls, and direct tests of Sharpe or welfare differences would provide additional protection against specification-search bias.

\subsection{Final conclusion}

The empirical evidence rejects both a purely informational interpretation of VRP and an unqualified direct-trading interpretation.

VRP-related variables can improve selected estimates of market stress and selected downside-risk characteristics, but the dynamic equity--bond models do not establish robust benchmark dominance. In the United States, the direct High-VRP strategy improves selected risk-adjusted measures but does not establish statistically robust investor-welfare superiority.

The European result is stronger. The positive-VRP direct variance-payoff approximation produces substantial risk-adjusted performance and positive certainty-equivalent differences, and the conclusion survives the principal robustness tests conducted in this thesis. This provides evidence that the payoff channel can contain materially greater economic value than the signal-only allocation channel in the tested European sample.

That result remains conditional on the model. The strategy does not reconstruct an exact variance-swap strike, contractual variance notional, collateral process, margin path, dealer bid--ask spread, or daily mark-to-market. The magnitude of the historical welfare gain should therefore not be interpreted as the return available from a directly executable derivative strategy.

The final conclusion is deliberately narrow:

\begin{quote}
The economic value of the Variance Risk Premium depends critically on the payoff structure through which it is harvested. In the tested European sample, a model-based direct variance-payoff approximation produces substantial and robust economic value, whereas the inclusion of VRP as a state variable in dynamic equity--bond allocation produces only limited gains. In the United States, neither channel establishes robust investor-welfare dominance over traditional portfolios.
\end{quote}

This conclusion does not identify a universal trading strategy. It identifies a broader empirical principle: the economic value of a financial signal cannot be separated from the payoff, risk controls, benchmarks, and implementation mechanism used to monetize it.
""".strip() + "\n"


def validate(text: str) -> None:
    errors: list[str] = []

    required = [
        (
            "Does the Variance Risk Premium "
            "create more economic value as an "
            "informational state variable"
        ),
        "184 United States",
        "122 European",
        "232 United States",
        "170 European",
        "1.019",
        "1.324",
        "927 basis points",
        "899 basis points",
        "2,000 paired moving-block",
        "six-month blocks",
        "expanding estimation history",
        "fixed 72-month rolling training window",
        (
            "not an observed return on "
            "invested capital"
        ),
        (
            "does not identify a universal "
            "trading strategy"
        ),
        (
            "The economic value of the "
            "Variance Risk Premium depends "
            "critically on the payoff structure"
        ),
    ]

    forbidden = [
        "collapses in Europe",
        "collapses in the European",
        "-2.8511",
        "-0.3625",
        "-0.9901",
        "0.1281",
        "127 observations",
        "200 monthly observations",
        (
            "allocation models use a "
            "72-month rolling estimation window"
        ),
        "true variance swap",
        "directly traded variance",
        "verified executable variance strategy",
        "available traded return",
        "filecite",
        "turn136file",
        "Final discussion and conclusion pending",
    ]

    for marker in required:
        if marker.lower() not in text.lower():
            errors.append(
                f"missing required marker: {marker}"
            )

    for marker in forbidden:
        if marker.lower() in text.lower():
            errors.append(
                f"forbidden/stale marker: {marker}"
            )

    for environment in (
        "quote",
    ):
        begin = text.count(
            rf"\begin{{{environment}}}"
        )
        end = text.count(
            rf"\end{{{environment}}}"
        )

        if begin != end:
            errors.append(
                f"{environment}: "
                f"{begin} begin / {end} end"
            )

    if text.count("{") != text.count("}"):
        errors.append(
            "unbalanced curly braces: "
            f"{text.count('{')} / "
            f"{text.count('}')}"
        )

    if text.count("$") % 2:
        errors.append(
            "odd number of inline $ delimiters"
        )

    labels = re.findall(
        r"\\label\{([^}]+)\}",
        text,
    )

    if len(labels) != len(set(labels)):
        errors.append(
            "duplicate LaTeX labels"
        )

    for number, line in enumerate(
        text.splitlines(),
        start=1,
    ):
        stripped = line.strip()

        if re.match(
            r"^#{1,6}\s+",
            stripped,
        ):
            errors.append(
                f"Markdown heading at line {number}"
            )

        if stripped.startswith("```"):
            errors.append(
                f"Markdown fence at line {number}"
            )

        if (
            len(stripped) >= 2
            and set(stripped) == {"="}
        ):
            errors.append(
                f"copy corruption '=' at line {number}"
            )

        if (
            len(stripped) >= 2
            and set(stripped) == {"-"}
        ):
            errors.append(
                f"copy corruption '-' at line {number}"
            )

        if "S&P" in line:
            errors.append(
                f"unescaped S&P at line {number}"
            )

    word_count = len(text.split())

    if word_count < 2_400:
        errors.append(
            "conclusion unexpectedly short: "
            f"{word_count} words"
        )

    if word_count > 3_600:
        errors.append(
            "conclusion unexpectedly long: "
            f"{word_count} words"
        )

    # Important conceptual consistency check.
    if (
        "HMM and RSM estimation begins after "
        "a 72-month burn-in and then uses an "
        "expanding estimation history"
        not in text
    ):
        errors.append(
            "HMM/RSM timing statement missing"
        )

    if (
        "machine-learning layer instead uses "
        "a fixed 72-month rolling training window"
        not in text
    ):
        errors.append(
            "ML rolling-window distinction missing"
        )

    if errors:
        print("=" * 92)
        print(
            "L7 DISCUSSION AND CONCLUSION "
            "VALIDATION FAILED"
        )
        print("=" * 92)

        for error in errors:
            print(
                "ERROR —",
                error,
            )

        raise SystemExit(1)


validate(TEXT)

TARGET.parent.mkdir(
    parents=True,
    exist_ok=True,
)

TARGET.write_text(
    TEXT,
    encoding="utf-8",
)

print("=" * 92)
print("L7 DISCUSSION AND CONCLUSION WRITER")
print("=" * 92)
print(
    f"PASS — wrote {TARGET}"
)
print(
    f"Words: {len(TEXT.split())}"
)
print(
    f"Lines: {len(TEXT.splitlines())}"
)
print(
    "Subsections:",
    TEXT.count(
        r"\subsection{"
    ),
)
print(
    "PASS — conceptual, numerical "
    "and LaTeX validation completed"
)
