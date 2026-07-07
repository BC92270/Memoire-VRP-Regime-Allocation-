from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.config import OUTPUT_CHARTS_DIR, OUTPUT_TABLES_DIR
from src.plots import plot_cumulative_returns, plot_drawdowns

pd.set_option("display.max_columns", None)
pd.set_option("display.width", 200)


def _safe_strategy_name(name: str) -> str:
    return name.lower().replace(" ", "_").replace("/", "_")


def load_hmm_diagnostics(market: str) -> dict[str, pd.DataFrame]:
    strategy_names = [
        "HMM without VRP",
        "HMM with VRP Signal",
    ]

    diagnostics = {}

    for strategy in strategy_names:
        safe_name = _safe_strategy_name(strategy)
        path = OUTPUT_TABLES_DIR / f"{market}_mvp2_{safe_name}_diagnostics.csv"

        if not path.exists():
            raise FileNotFoundError(f"Missing diagnostics file: {path}")

        diagnostics[strategy] = pd.read_csv(path, index_col=0, parse_dates=True)

    return diagnostics


def summarize_hmm_diagnostics(diagnostics: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = {}

    for strategy, diag in diagnostics.items():
        rows[strategy] = {
            "obs": diag.shape[0],
            "convergence_rate": diag["converged"].mean() if "converged" in diag else None,
            "avg_stress_probability": diag["stress_probability"].mean(),
            "median_stress_probability": diag["stress_probability"].median(),
            "p95_stress_probability": diag["stress_probability"].quantile(0.95),
            "avg_equity_weight": diag["equity_weight"].mean(),
            "min_equity_weight": diag["equity_weight"].min(),
            "max_equity_weight": diag["equity_weight"].max(),
            "avg_turnover": diag["turnover"].mean(),
        }

    return pd.DataFrame(rows).T


def plot_hmm_stress_probabilities(
    diagnostics: dict[str, pd.DataFrame],
    output_path,
) -> None:
    fig, ax = plt.subplots(figsize=(12, 7))

    for strategy, diag in diagnostics.items():
        diag["stress_probability"].plot(ax=ax, label=strategy)

    ax.set_title("US - HMM Stress Probability")
    ax.set_xlabel("Date")
    ax.set_ylabel("Stress probability")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_hmm_equity_weights(
    diagnostics: dict[str, pd.DataFrame],
    output_path,
) -> None:
    fig, ax = plt.subplots(figsize=(12, 7))

    for strategy, diag in diagnostics.items():
        diag["equity_weight"].plot(ax=ax, label=strategy)

    ax.set_title("US - HMM Equity Weights")
    ax.set_xlabel("Date")
    ax.set_ylabel("Equity weight")
    ax.grid(True, alpha=0.3)
    ax.legend()

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_hmm_diagnostics(market: str = "us") -> None:
    market = market.lower()

    returns_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_hmm_strategy_returns.csv"

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing HMM strategy returns: {returns_path}")

    strategy_returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    diagnostics = load_hmm_diagnostics(market)

    hmm_index = diagnostics["HMM with VRP Signal"].index
    aligned_returns = strategy_returns.reindex(hmm_index).dropna(how="all")

    diagnostic_summary = summarize_hmm_diagnostics(diagnostics)

    summary_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_hmm_diagnostic_summary.csv"
    diagnostic_summary.to_csv(summary_path)

    plot_cumulative_returns(
        aligned_returns,
        OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_aligned_cumulative_returns.png",
        title=f"{market.upper()} - HMM Aligned Cumulative Returns",
    )

    plot_drawdowns(
        aligned_returns,
        OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_aligned_drawdowns.png",
        title=f"{market.upper()} - HMM Aligned Drawdowns",
    )

    plot_hmm_stress_probabilities(
        diagnostics,
        OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_stress_probabilities.png",
    )

    plot_hmm_equity_weights(
        diagnostics,
        OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_equity_weights.png",
    )

    print("\n" + "=" * 80)
    print(f"MVP 2 HMM diagnostics complete for {market.upper()}")
    print("=" * 80)

    print("\nHMM diagnostic summary:")
    print(diagnostic_summary.round(4))

    print("\nSaved diagnostic summary:")
    print(summary_path)

    print("\nSaved charts:")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_aligned_cumulative_returns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_aligned_drawdowns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_stress_probabilities.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp2_hmm_equity_weights.png")


if __name__ == "__main__":
    run_hmm_diagnostics("us")