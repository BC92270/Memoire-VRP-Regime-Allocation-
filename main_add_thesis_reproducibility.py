from pathlib import Path


METHODOLOGY = Path(
    "thesis/latex/sections/"
    "03_data_methodology.tex"
)

APPENDIX = Path(
    "thesis/latex/appendix/"
    "D_reproducibility.tex"
)


methodology = METHODOLOGY.read_text(
    encoding="utf-8"
)


marker = (
    "Its results therefore provide evidence "
    "about a stylized variance-carry mechanism "
    "rather than a verified historical "
    "variance-swap return available to an "
    "investor."
)


addition = r"""

\subsection{Code, Data, and Reproducibility}
\label{subsec:reproducibility}

All empirical analyses in this thesis are implemented in Python. The project repository separates data ingestion and feature construction, econometric and machine-learning models, portfolio construction, welfare analysis, robustness testing, reporting, and LaTeX production. The empirical tables and figures reported in the thesis are generated from the same codebase used to estimate the models and construct the portfolios rather than being reconstructed manually for presentation.

The data pipeline combines programmatically downloaded market series with locally supplied files when an external history cannot be reproduced reliably through the same interface. Date parsing, duplicate removal, numerical cleaning, sample filtering, temporal alignment, and calendar-gap treatment are implemented explicitly in the source code. Where redistribution of a raw dataset is restricted or impractical, replication requires access to the original source or an equivalent local input file.

Raw and processed datasets are not assumed to be bundled automatically with the version-controlled repository. Final thesis-facing tables and figures are retained separately so that the numerical results reported in the manuscript can be checked against the outputs produced by the empirical pipeline.

The computational sequence proceeds from baseline market and benchmark construction to HMM and RSM estimation, robustness analysis, welfare analysis, machine-learning stress classification, and the model-based direct variance-payoff extension. Appendix~\ref{app:reproducibility} documents the principal scripts, input locations, output directories, and replication sequence. Appendix~\ref{app:data} documents the principal data-construction diagnostics.
""".strip()


if (
    r"\subsection{Code, Data, and Reproducibility}"
    in methodology
):
    raise SystemExit(
        "Code/data subsection already exists."
    )

count = methodology.count(
    marker
)

if count != 1:
    raise SystemExit(
        "Expected insertion marker exactly once, "
        f"found {count}."
    )

methodology = methodology.replace(
    marker,
    marker + "\n\n" + addition,
    1,
)

METHODOLOGY.write_text(
    methodology,
    encoding="utf-8",
)


appendix = r"""
\section{Reproducibility}
\label{app:reproducibility}

\subsection{Repository organization}

The empirical project is organized around reusable source modules, execution scripts, generated outputs, and the thesis manuscript. The \texttt{src/} directory contains the principal data, feature, model, portfolio, performance, welfare, and robustness functions. Top-level \texttt{main\_*.py} scripts execute the major empirical stages. Generated tables and charts are stored under \texttt{outputs/tables/} and \texttt{outputs/charts/}, while the final manuscript is maintained under \texttt{thesis/latex/}.

Raw and processed market datasets are treated as local analytical inputs rather than as universally redistributable repository assets. Replication therefore requires access to the relevant original data sources or equivalent local input files when redistribution is not possible.

\subsection{Core empirical sequence}

A representative replication sequence is:

\begin{verbatim}
python main_mvp1.py

python main_mvp1_diagnostics.py us
python main_mvp1_diagnostics.py eu

python main_mvp2_hmm_spec_grid.py us
python main_mvp2_hmm_spec_grid.py eu
python main_mvp2_hmm_selected_models.py

python main_mvp3_rsm.py us
python main_mvp3_rsm.py eu

python main_mvp4_robustness.py
python main_mvp4_crisis_analysis.py

python main_mvp5_welfare.py

python main_mvp6_ml_regime.py
python main_mvp6_ml_welfare.py

python main_mvp7_direct_variance.py
python main_mvp7_direct_variance_welfare.py
python main_mvp7_direct_variance_robustness.py

python main_final_cross_market_report.py
\end{verbatim}

Each stage writes intermediate or final outputs that are subsequently used by the reporting and thesis layers.

\subsection{Direct-variance outputs}

The direct-variance stage generates market-specific strategy returns, turnover series, payoff diagnostics, performance summaries, benchmark comparisons, and cross-market consolidation tables. The final thesis-facing direct-variance results are drawn from the validated cross-market output tables used elsewhere in the manuscript.

\subsection{Figures}

Figures used in the main manuscript are stored under \texttt{thesis/latex/figures/}. Some are copied from the validated empirical chart outputs and others are regenerated directly from final cross-market thesis tables. This separation ensures that graphical presentation remains tied to the same numerical evidence reported in the tables.

\subsection{Version identification}

The exact code version associated with the submitted thesis can be identified using:

\begin{verbatim}
git rev-parse HEAD
\end{verbatim}

The installed Python environment can be archived at submission time using:

\begin{verbatim}
python -m pip freeze > requirements_thesis_lock.txt
\end{verbatim}

This provides a record of the package versions used for the final empirical run.

\subsection{Manuscript validation}

The final LaTeX manuscript can be rebuilt using:

\begin{verbatim}
latexmk -cd -pdf \
  -interaction=nonstopmode \
  -halt-on-error \
  thesis/latex/main.tex
\end{verbatim}

The global consistency audit is executed using:

\begin{verbatim}
python main_audit_final_latex_thesis.py
\end{verbatim}

The audit checks critical numerical markers, model-timing terminology, citation keys, internal references, deprecated empirical conclusions, and the university page limit before the appendices.
""".strip() + "\n"


APPENDIX.write_text(
    appendix,
    encoding="utf-8",
)


print(
    "PASS — methodology reproducibility "
    "subsection added"
)

print(
    "PASS — Appendix D reproducibility "
    "material written"
)
