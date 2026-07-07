from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.config import OUTPUT_CHARTS_DIR, OUTPUT_TABLES_DIR
from src.performance_metrics import summarize_strategies
from src.plots import plot_cumulative_returns, plot_drawdowns


SELECTED_MODELS = [
    "Buy-and-Hold Equity",
    "60/40",
    "1/N Equity-Bond",
    "HMM RV",
    "HMM RV + Raw VRP",
    "HMM RV + Log VRP",
]


def _safe_name(name: str) -> str:
    return (
        name.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("+", "plus")
        .replace("-", "_")
    )


def load_grid_outputs(market: str = "us") -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    returns_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_strategy_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_turnovers.csv"
    diagnostics_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_diagnostic_summary.csv"

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing returns file: {returns_path}")

    if not turnovers_path.exists():
        raise FileNotFoundError(f"Missing turnovers file: {turnovers_path}")

    if not diagnostics_path.exists():
        raise FileNotFoundError(f"Missing diagnostics file: {diagnostics_path}")

    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    turnovers = pd.read_csv(turnovers_path, index_col=0, parse_dates=True)
    diagnostics = pd.read_csv(diagnostics_path, index_col=0)

    return returns, turnovers, diagnostics


def plot_selected_equity_curves(
    selected_returns: pd.DataFrame,
    output_path,
) -> None:
    wealth = (1.0 + selected_returns.dropna(how="all")).cumprod()

    fig, ax = plt.subplots(figsize=(12, 7))
    wealth.plot(ax=ax)

    ax.set_title("US - Selected HMM Models vs Benchmarks")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative wealth")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_selected_drawdowns(
    selected_returns: pd.DataFrame,
    output_path,
) -> None:
    wealth = (1.0 + selected_returns.dropna(how="all")).cumprod()
    drawdowns = wealth / wealth.cummax() - 1.0

    fig, ax = plt.subplots(figsize=(12, 7))
    drawdowns.plot(ax=ax)

    ax.set_title("US - Selected HMM Drawdowns vs Benchmarks")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_selected_hmm_report(market: str = "us") -> None:
    returns, turnovers, diagnostics = load_grid_outputs(market)

    missing = [model for model in SELECTED_MODELS if model not in returns.columns]
    if missing:
        raise ValueError(f"Missing selected model columns: {missing}")

    selected_returns = returns[SELECTED_MODELS].dropna(how="all")
    selected_turnovers = turnovers[SELECTED_MODELS].reindex(selected_returns.index)

    selected_summary = summarize_strategies(
        selected_returns,
        turnovers=selected_turnovers,
        periods_per_year=12,
    )

    selected_diagnostics = diagnostics.reindex(
        ["HMM RV", "HMM RV + Raw VRP", "HMM RV + Log VRP"]
    )

    selected_returns_path = OUTPUT_TABLES_DIR / f"{market}_selected_hmm_returns.csv"
    selected_turnovers_path = OUTPUT_TABLES_DIR / f"{market}_selected_hmm_turnovers.csv"
    selected_summary_path = OUTPUT_TABLES_DIR / f"{market}_selected_hmm_performance_summary.csv"
    selected_diagnostics_path = OUTPUT_TABLES_DIR / f"{market}_selected_hmm_diagnostic_summary.csv"

    selected_returns.to_csv(selected_returns_path)
    selected_turnovers.to_csv(selected_turnovers_path)
    selected_summary.to_csv(selected_summary_path)
    selected_diagnostics.to_csv(selected_diagnostics_path)

    plot_selected_equity_curves(
        selected_returns,
        OUTPUT_CHARTS_DIR / f"{market}_selected_hmm_cumulative_returns.png",
    )

    plot_selected_drawdowns(
        selected_returns,
        OUTPUT_CHARTS_DIR / f"{market}_selected_hmm_drawdowns.png",
    )

    print("\n" + "=" * 80)
    print("Selected HMM performance summary")
    print("=" * 80)
    print(selected_summary.round(4))

    print("\n" + "=" * 80)
    print("Selected HMM diagnostic summary")
    print("=" * 80)
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)
    print(selected_diagnostics.to_string())

    print("\nSaved files:")
    print(selected_returns_path)
    print(selected_turnovers_path)
    print(selected_summary_path)
    print(selected_diagnostics_path)
    print(OUTPUT_CHARTS_DIR / f"{market}_selected_hmm_cumulative_returns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_selected_hmm_drawdowns.png")


if __name__ == "__main__":
    run_selected_hmm_report("us")