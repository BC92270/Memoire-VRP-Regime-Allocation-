from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.config import OUTPUT_CHARTS_DIR, OUTPUT_TABLES_DIR
from src.performance_metrics import summarize_strategies


IMPLEMENTABLE_MODELS = [
    "Buy-and-Hold Equity",
    "60/40",
    "1/N Equity-Bond",
    "HMM RV",
    "HMM RV + Log VRP",
    "RSM Returns Only",
    "RSM RV",
    "RSM RV + Raw VRP",
    "RSM RV + Log VRP",
]

EXTENDED_MODELS = [
    "Pure VRP Proxy",
    *IMPLEMENTABLE_MODELS,
]

CRISIS_WINDOWS = {
    "Full aligned sample": ("2009-01-01", "2026-12-31"),
    "Eurozone Crisis": ("2010-01-01", "2012-12-31"),
    "Volmageddon and late cycle": ("2018-01-01", "2018-12-31"),
    "Covid Crisis": ("2020-02-01", "2020-06-30"),
    "Inflation Rate Shock": ("2022-01-01", "2022-12-31"),
}


def load_core_outputs(market: str = "eu") -> tuple[pd.DataFrame, pd.DataFrame]:
    returns_path = OUTPUT_TABLES_DIR / f"{market}_core_model_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_core_model_turnovers.csv"

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing core returns file: {returns_path}")

    if not turnovers_path.exists():
        raise FileNotFoundError(f"Missing core turnovers file: {turnovers_path}")

    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    turnovers = pd.read_csv(turnovers_path, index_col=0, parse_dates=True)

    return returns, turnovers


def cumulative_return(returns: pd.Series) -> float:
    returns = returns.dropna()

    if returns.empty:
        return float("nan")

    return float((1.0 + returns).prod() - 1.0)


def subperiod_summary(
    returns: pd.DataFrame,
    turnovers: pd.DataFrame,
    start: str,
    end: str,
    min_obs: int = 3,
) -> pd.DataFrame:
    sub_returns = returns.loc[start:end].copy()
    sub_turnovers = turnovers.reindex(sub_returns.index)

    if sub_returns.shape[0] < min_obs:
        return pd.DataFrame()

    summary = summarize_strategies(
        sub_returns,
        turnovers=sub_turnovers,
        periods_per_year=12,
    )

    summary["Period Return"] = sub_returns.apply(cumulative_return, axis=0)

    return summary


def build_crisis_tables(
    returns: pd.DataFrame,
    turnovers: pd.DataFrame,
    model_list: list[str],
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    rows = []

    selected_returns = returns[model_list]
    selected_turnovers = turnovers[model_list]

    for window_name, (start, end) in CRISIS_WINDOWS.items():
        summary = subperiod_summary(
            returns=selected_returns,
            turnovers=selected_turnovers,
            start=start,
            end=end,
        )

        if summary.empty:
            continue

        summary.insert(0, "Window", window_name)
        summary.insert(1, "Strategy", summary.index)

        rows.append(summary.reset_index(drop=True))

    long_summary = pd.concat(rows, axis=0, ignore_index=True)

    period_return_pivot = long_summary.pivot(
        index="Strategy",
        columns="Window",
        values="Period Return",
    )

    maxdd_pivot = long_summary.pivot(
        index="Strategy",
        columns="Window",
        values="Max Drawdown",
    )

    sharpe_pivot = long_summary.pivot(
        index="Strategy",
        columns="Window",
        values="Sharpe",
    )

    return long_summary, period_return_pivot, maxdd_pivot, sharpe_pivot


def plot_cumulative_returns(
    returns: pd.DataFrame,
    output_path,
    title: str,
) -> None:
    wealth = (1.0 + returns).cumprod()

    fig, ax = plt.subplots(figsize=(13, 8))
    wealth.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative wealth")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_drawdowns(
    returns: pd.DataFrame,
    output_path,
    title: str,
) -> None:
    wealth = (1.0 + returns).cumprod()
    drawdowns = wealth / wealth.cummax() - 1.0

    fig, ax = plt.subplots(figsize=(13, 8))
    drawdowns.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def run_final_eu_report() -> None:
    market = "eu"

    core_returns, core_turnovers = load_core_outputs(market)

    missing = [m for m in EXTENDED_MODELS if m not in core_returns.columns]
    if missing:
        raise ValueError(f"Missing expected models: {missing}")

    implementable_returns = core_returns[IMPLEMENTABLE_MODELS].dropna(how="any")
    implementable_turnovers = core_turnovers[IMPLEMENTABLE_MODELS].reindex(
        implementable_returns.index
    )

    extended_returns = core_returns[EXTENDED_MODELS].dropna(how="any")
    extended_turnovers = core_turnovers[EXTENDED_MODELS].reindex(
        extended_returns.index
    )

    implementable_summary = summarize_strategies(
        implementable_returns,
        turnovers=implementable_turnovers,
        periods_per_year=12,
    )

    extended_summary = summarize_strategies(
        extended_returns,
        turnovers=extended_turnovers,
        periods_per_year=12,
    )

    implementable_summary = implementable_summary.sort_values(
        ["Sharpe", "Max Drawdown"],
        ascending=[False, False],
    )

    extended_summary = extended_summary.sort_values(
        ["Sharpe", "Max Drawdown"],
        ascending=[False, False],
    )

    crisis_long, crisis_period_return, crisis_maxdd, crisis_sharpe = build_crisis_tables(
        returns=implementable_returns,
        turnovers=implementable_turnovers,
        model_list=IMPLEMENTABLE_MODELS,
    )

    final_returns_path = OUTPUT_TABLES_DIR / f"{market}_final_model_returns.csv"
    final_turnovers_path = OUTPUT_TABLES_DIR / f"{market}_final_model_turnovers.csv"
    implementable_summary_path = OUTPUT_TABLES_DIR / f"{market}_final_implementable_summary.csv"
    extended_summary_path = OUTPUT_TABLES_DIR / f"{market}_final_extended_summary_with_synthetic_vrp.csv"

    crisis_long_path = OUTPUT_TABLES_DIR / f"{market}_final_crisis_long.csv"
    crisis_period_return_path = OUTPUT_TABLES_DIR / f"{market}_final_crisis_period_return.csv"
    crisis_maxdd_path = OUTPUT_TABLES_DIR / f"{market}_final_crisis_max_drawdown.csv"
    crisis_sharpe_path = OUTPUT_TABLES_DIR / f"{market}_final_crisis_sharpe.csv"

    implementable_returns.to_csv(final_returns_path)
    implementable_turnovers.to_csv(final_turnovers_path)
    implementable_summary.to_csv(implementable_summary_path)
    extended_summary.to_csv(extended_summary_path)

    crisis_long.to_csv(crisis_long_path, index=False)
    crisis_period_return.to_csv(crisis_period_return_path)
    crisis_maxdd.to_csv(crisis_maxdd_path)
    crisis_sharpe.to_csv(crisis_sharpe_path)

    plot_cumulative_returns(
        implementable_returns,
        OUTPUT_CHARTS_DIR / f"{market}_final_implementable_cumulative_returns.png",
        title="EU - Final Implementable Strategies: Cumulative Wealth",
    )

    plot_drawdowns(
        implementable_returns,
        OUTPUT_CHARTS_DIR / f"{market}_final_implementable_drawdowns.png",
        title="EU - Final Implementable Strategies: Drawdowns",
    )

    plot_cumulative_returns(
        extended_returns,
        OUTPUT_CHARTS_DIR / f"{market}_final_extended_cumulative_returns_with_synthetic_vrp.png",
        title="EU - Final Strategies Including Synthetic Pure VRP Proxy",
    )

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 100)
    print("FINAL EU — Implementable strategy summary")
    print("=" * 100)
    print(implementable_summary.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL EU — Extended summary including Synthetic Pure VRP Proxy")
    print("=" * 100)
    print(extended_summary.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL EU — Crisis analysis: Period Return")
    print("=" * 100)
    print(crisis_period_return.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL EU — Crisis analysis: Max Drawdown")
    print("=" * 100)
    print(crisis_maxdd.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL EU — Crisis analysis: Sharpe")
    print("=" * 100)
    print(crisis_sharpe.round(4).to_string())

    print("\nSaved final EU files:")
    print(final_returns_path)
    print(final_turnovers_path)
    print(implementable_summary_path)
    print(extended_summary_path)
    print(crisis_long_path)
    print(crisis_period_return_path)
    print(crisis_maxdd_path)
    print(crisis_sharpe_path)
    print(OUTPUT_CHARTS_DIR / f"{market}_final_implementable_cumulative_returns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_final_implementable_drawdowns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_final_extended_cumulative_returns_with_synthetic_vrp.png")


if __name__ == "__main__":
    run_final_eu_report()