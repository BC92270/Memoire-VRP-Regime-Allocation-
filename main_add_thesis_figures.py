from pathlib import Path


RESULTS = Path(
    "thesis/latex/sections/"
    "04_empirical_results.tex"
)

text = RESULTS.read_text(
    encoding="utf-8"
)


def insert_before(
    source,
    marker,
    addition,
):
    count = source.count(
        marker
    )

    if count != 1:
        raise RuntimeError(
            f"Marker expected once: "
            f"{marker!r}; found {count}."
        )

    return source.replace(
        marker,
        addition
        + "\n\n"
        + marker,
        1,
    )


# ============================================================
# FIGURE 1 — VRP COMPONENTS
# ============================================================

figure_vrp = r"""
Figure~\ref{fig:vrp-components} provides descriptive context for the variance measures used throughout the empirical analysis. The panels display the implied- and realized-variance components underlying the empirical VRP construction in the two markets. The purpose of the figure is descriptive rather than causal: it illustrates the time variation of the variance measures that subsequently enter the allocation and direct-payoff exercises.

\begin{figure}[htbp]
\centering

\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{us_mvp1_vrp_components.png}
\caption{United States}
\end{subfigure}
\hfill
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{eu_mvp1_vrp_components.png}
\caption{Europe}
\end{subfigure}

\caption{Implied variance, realized variance, and empirical VRP components}
\label{fig:vrp-components}
\end{figure}
""".strip()


text = insert_before(
    text,
    r"\subsection{Equity--bond allocation: United States}",
    figure_vrp,
)


# ============================================================
# FIGURE 2 — HMM MECHANISM
# ============================================================

figure_hmm = r"""
The implementation mechanism of the selected United States HMM is illustrated in Figure~\ref{fig:hmm-mechanism}. The first panel reports the filtered stress probabilities and the second reports the corresponding equity weights. The figure shows how changes in the inferred latent state are mapped into portfolio exposure rather than treating the HMM as a purely statistical classification device.

\begin{figure}[htbp]
\centering

\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{us_mvp2_hmm_stress_probabilities.png}
\caption{Filtered stress probabilities}
\end{subfigure}
\hfill
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{us_mvp2_hmm_equity_weights.png}
\caption{Resulting equity weights}
\end{subfigure}

\caption{Selected United States HMM: state probability and portfolio mapping}
\label{fig:hmm-mechanism}
\end{figure}
""".strip()


text = insert_before(
    text,
    r"\subsection{Equity--bond allocation: Europe}",
    figure_hmm,
)


# ============================================================
# FIGURE 3 — IMPLEMENTABLE ALLOCATION
# ============================================================

figure_allocation = r"""
Figure~\ref{fig:allocation-cumulative} complements the summary statistics by displaying cumulative performance for the final implementable allocation comparisons. The visual evidence reinforces the table-based conclusion: the dynamic models can alter the path and drawdown profile of wealth, but they do not generate uniform cross-market dominance over the simple benchmarks.

\begin{figure}[htbp]
\centering

\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{us_final_implementable_cumulative_returns.png}
\caption{United States}
\end{subfigure}
\hfill
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{eu_final_implementable_cumulative_returns.png}
\caption{Europe}
\end{subfigure}

\caption{Cumulative performance of the final implementable allocation comparisons}
\label{fig:allocation-cumulative}
\end{figure}
""".strip()


text = insert_before(
    text,
    r"\subsection{Underlying direct variance-payoff diagnostics}",
    figure_allocation,
)


# ============================================================
# FIGURE 4 — DIRECT VARIANCE CROSS-MARKET COMPARISON
# ============================================================

figure_direct = r"""
Figure~\ref{fig:direct-variance-cross-market} summarizes the central cross-market direct-payoff result. Panel (a) compares the Sharpe ratio of the selected direct-variance strategy with the two balanced benchmarks. Panel (b) reports the corresponding fee-equivalent welfare difference at $\gamma=5$. The two panels highlight why Sharpe-ratio improvement alone is insufficient for the United States conclusion, while the European result remains economically much stronger under the welfare criterion.

\begin{figure}[htbp]
\centering

\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{direct_variance_sharpe_cross_market.png}
\caption{Sharpe-ratio comparison}
\end{subfigure}
\hfill
\begin{subfigure}[t]{0.49\textwidth}
\centering
\includegraphics[
    width=\linewidth
]{direct_variance_welfare_cross_market.png}
\caption{Fee-equivalent welfare comparison}
\end{subfigure}

\caption{Cross-market economic comparison of the selected model-based direct variance-payoff strategies}
\label{fig:direct-variance-cross-market}
\end{figure}
""".strip()


text = insert_before(
    text,
    r"\subsection{Investor-welfare evidence}",
    figure_direct,
)


# ============================================================
# VALIDATION
# ============================================================

expected = [
    "fig:vrp-components",
    "fig:hmm-mechanism",
    "fig:allocation-cumulative",
    "fig:direct-variance-cross-market",
]

for label in expected:
    count = text.count(
        label
    )

    if count != 2:
        raise RuntimeError(
            f"{label}: expected reference "
            f"+ label, found {count}."
        )


if text.count(
    r"\begin{figure}"
) < 4:
    raise RuntimeError(
        "Fewer than four figure environments."
    )


for forbidden in [
    "us_direct_variance_cumulative_vs_benchmarks.png",
    "eu_direct_variance_cumulative_vs_benchmarks.png",
]:
    if forbidden in text:
        raise RuntimeError(
            f"Obsolete figure reference: {forbidden}"
        )


RESULTS.write_text(
    text,
    encoding="utf-8",
)


print(
    "PASS — four analytical figures "
    "integrated into Empirical Results"
)
