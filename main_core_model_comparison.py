from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.config import OUTPUT_CHARTS_DIR, OUTPUT_TABLES_DIR
from src.performance_metrics import summarize_strategies


CORE_MODELS = [
    "Buy-and-Hold Equity",
    "60/40",
    "1/N Equity-Bond",
    "Pure VRP Proxy",
    "HMM RV",
    "HMM RV + Raw VRP",
    "HMM RV + Log VRP",
    "RSM Returns Only",
    "RSM RV",
    "RSM RV + Raw VRP",
    "RSM RV + Log VRP",
]


def load_outputs(market: str = "us") -> tuple[pd.DataFrame, pd.DataFrame]:
    market = market.lower()

    hmm_returns_path = OUTPUT_TABLES_DIR / f"{market}_selected_hmm_returns.csv"
    hmm_turnovers_path = OUTPUT_TABLES_DIR / f"{market}_selected_hmm_turnovers.csv"

    rsm_returns_path = OUTPUT_TABLES_DIR / f"{market}_mvp3_rsm_strategy_returns.csv"
    rsm_turnovers_path = OUTPUT_TABLES_DIR / f"{market}_mvp3_rsm_turnovers.csv"

    for path in [
        hmm_returns_path,
        hmm_turnovers_path,
        rsm_returns_path,
        rsm_turnovers_path,
    ]:
        if not path.exists():
            raise FileNotFoundError(f"Missing required file: {path}")

    hmm_returns = pd.read_csv(hmm_returns_path, index_col=0, parse_dates=True)
    hmm_turnovers = pd.read_csv(hmm_turnovers_path, index_col=0, parse_dates=True)

    rsm_returns = pd.read_csv(rsm_returns_path, index_col=0, parse_dates=True)
    rsm_turnovers = pd.read_csv(rsm_turnovers_path, index_col=0, parse_dates=True)

    returns = pd.concat([hmm_returns, rsm_returns], axis=1)
    turnovers = pd.concat([hmm_turnovers, rsm_turnovers], axis=1)

    returns = returns.loc[:, ~returns.columns.duplicated()]
    turnovers = turnovers.loc[:, ~turnovers.columns.duplicated()]

    missing = [model for model in CORE_MODELS if model not in returns.columns]
    if missing:
        raise ValueError(f"Missing expected models in returns: {missing}")

    returns = returns[CORE_MODELS]
    turnovers = turnovers[CORE_MODELS]

    # Align all strategies on common dates.
    aligned_returns = returns.dropna(how="any")
    aligned_turnovers = turnovers.reindex(aligned_returns.index)

    return aligned_returns, aligned_turnovers


def plot_core_cumulative_returns(
    returns: pd.DataFrame,
    output_path,
) -> None:
    wealth = (1.0 + returns).cumprod()

    fig, ax = plt.subplots(figsize=(13, 8))
    wealth.plot(ax=ax)

    ax.set_title("US - Core Model Comparison: Cumulative Wealth")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative wealth")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_core_drawdowns(
    returns: pd.DataFrame,
    output_path,
) -> None:
    wealth = (1.0 + returns).cumprod()
    drawdowns = wealth / wealth.cummax() - 1.0

    fig, ax = plt.subplots(figsize=(13, 8))
    drawdowns.plot(ax=ax)

    ax.set_title("US - Core Model Comparison: Drawdowns")
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_reduced_cumulative_returns(
    returns: pd.DataFrame,
    output_path,
) -> None:
    """
    Cleaner chart for the thesis: removes Pure VRP Proxy because it dominates visually
    and is only a synthetic proxy at this stage.
    """
    reduced_cols = [
        "Buy-and-Hold Equity",
        "60/40",
        "1/N Equity-Bond",
        "HMM RV + Log VRP",
        "RSM RV + Raw VRP",
    ]

    wealth = (1.0 + returns[reduced_cols]).cumprod()

    fig, ax = plt.subplots(figsize=(13, 8))
    wealth.plot(ax=ax)

    ax.set_title("US - Selected Implementable Strategies: Cumulative Wealth")
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative wealth")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_core_comparison(market: str = "us") -> None:
    returns, turnovers = load_outputs(market)

    summary = summarize_strategies(
        returns,
        turnovers=turnovers,
        periods_per_year=12,
    )

    summary = summary.sort_values(["Sharpe", "Max Drawdown"], ascending=[False, False])

    returns_path = OUTPUT_TABLES_DIR / f"{market}_core_model_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_core_model_turnovers.csv"
    summary_path = OUTPUT_TABLES_DIR / f"{market}_core_model_performance_summary.csv"

    returns.to_csv(returns_path)
    turnovers.to_csv(turnovers_path)
    summary.to_csv(summary_path)

    plot_core_cumulative_returns(
        returns,
        OUTPUT_CHARTS_DIR / f"{market}_core_model_cumulative_returns.png",
    )

    plot_core_drawdowns(
        returns,
        OUTPUT_CHARTS_DIR / f"{market}_core_model_drawdowns.png",
    )

    plot_reduced_cumulative_returns(
        returns,
        OUTPUT_CHARTS_DIR / f"{market}_core_model_reduced_cumulative_returns.png",
    )

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 100)
    print("Core model performance summary")
    print("=" * 100)
    print(summary.round(4).to_string())

    print("\nSaved files:")
    print(returns_path)
    print(turnovers_path)
    print(summary_path)
    print(OUTPUT_CHARTS_DIR / f"{market}_core_model_cumulative_returns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_core_model_drawdowns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_core_model_reduced_cumulative_returns.png")


if __name__ == "__main__":
    run_core_comparison("us")