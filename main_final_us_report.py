from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd

from src.config import (
    BASE_TRANSACTION_COST_BPS,
    DATA_PROCESSED_DIR,
    OUTPUT_CHARTS_DIR,
    OUTPUT_TABLES_DIR,
)
from src.performance_metrics import summarize_strategies
from src.robustness import simulate_smoothed_dynamic_target_weight_strategy


HMM_PARTIAL_SPEED = 0.25

IMPLEMENTABLE_MODELS = [
    "Buy-and-Hold Equity",
    "60/40",
    "1/N Equity-Bond",
    "HMM RV + Log VRP (full)",
    "HMM RV + Log VRP (partial 0.25)",
    "RSM RV + Raw VRP",
]

EXTENDED_MODELS = [
    "Synthetic Pure VRP Proxy",
    *IMPLEMENTABLE_MODELS,
]

CRISIS_WINDOWS = {
    "Full aligned sample": ("2005-01-01", "2026-12-31"),
    "Eurozone Crisis": ("2010-01-01", "2012-12-31"),
    "Volmageddon and late cycle": ("2018-01-01", "2018-12-31"),
    "Covid Crisis": ("2020-02-01", "2020-06-30"),
    "Inflation Rate Shock": ("2022-01-01", "2022-12-31"),
}


def load_core_outputs(market: str = "us") -> tuple[pd.DataFrame, pd.DataFrame]:
    returns_path = OUTPUT_TABLES_DIR / f"{market}_core_model_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_core_model_turnovers.csv"

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing core returns file: {returns_path}")

    if not turnovers_path.exists():
        raise FileNotFoundError(f"Missing core turnovers file: {turnovers_path}")

    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    turnovers = pd.read_csv(turnovers_path, index_col=0, parse_dates=True)

    return returns, turnovers


def load_monthly_data(market: str = "us") -> pd.DataFrame:
    monthly_path = DATA_PROCESSED_DIR / f"{market}_monthly_rebalance.csv"

    if not monthly_path.exists():
        raise FileNotFoundError(f"Missing monthly file: {monthly_path}")

    return pd.read_csv(monthly_path, index_col=0, parse_dates=True)


def load_hmm_log_vrp_diagnostics(market: str = "us") -> pd.DataFrame:
    path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_hmm_rv_plus_log_vrp_diagnostics.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing HMM diagnostics file: {path}")

    return pd.read_csv(path, index_col=0, parse_dates=True)


def build_final_return_set(market: str = "us") -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Builds final US model set:
    - classic benchmarks
    - HMM RV + Log VRP full rebalance
    - HMM RV + Log VRP with partial rebalancing speed = 0.25
    - RSM RV + Raw VRP
    - Synthetic Pure VRP Proxy, kept separately in the extended table
    """
    core_returns, core_turnovers = load_core_outputs(market)
    monthly = load_monthly_data(market)
    hmm_diag = load_hmm_log_vrp_diagnostics(market)

    hmm_partial_returns, hmm_partial_turnover, _weights = simulate_smoothed_dynamic_target_weight_strategy(
        monthly=monthly,
        diagnostics=hmm_diag,
        strategy_name="HMM RV + Log VRP (partial 0.25)",
        cost_bps=BASE_TRANSACTION_COST_BPS,
        adjustment_speed=HMM_PARTIAL_SPEED,
    )

    final_returns = pd.DataFrame(index=core_returns.index)
    final_turnovers = pd.DataFrame(index=core_returns.index)

    final_returns["Synthetic Pure VRP Proxy"] = core_returns["Pure VRP Proxy"]
    final_turnovers["Synthetic Pure VRP Proxy"] = core_turnovers["Pure VRP Proxy"]

    final_returns["Buy-and-Hold Equity"] = core_returns["Buy-and-Hold Equity"]
    final_turnovers["Buy-and-Hold Equity"] = core_turnovers["Buy-and-Hold Equity"]

    final_returns["60/40"] = core_returns["60/40"]
    final_turnovers["60/40"] = core_turnovers["60/40"]

    final_returns["1/N Equity-Bond"] = core_returns["1/N Equity-Bond"]
    final_turnovers["1/N Equity-Bond"] = core_turnovers["1/N Equity-Bond"]

    final_returns["HMM RV + Log VRP (full)"] = core_returns["HMM RV + Log VRP"]
    final_turnovers["HMM RV + Log VRP (full)"] = core_turnovers["HMM RV + Log VRP"]

    final_returns["HMM RV + Log VRP (partial 0.25)"] = hmm_partial_returns
    final_turnovers["HMM RV + Log VRP (partial 0.25)"] = hmm_partial_turnover

    final_returns["RSM RV + Raw VRP"] = core_returns["RSM RV + Raw VRP"]
    final_turnovers["RSM RV + Raw VRP"] = core_turnovers["RSM RV + Raw VRP"]

    final_returns = final_returns.dropna(how="any")
    final_turnovers = final_turnovers.reindex(final_returns.index)

    return final_returns, final_turnovers


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


def run_final_us_report() -> None:
    market = "us"

    final_returns, final_turnovers = build_final_return_set(market)

    implementable_returns = final_returns[IMPLEMENTABLE_MODELS]
    implementable_turnovers = final_turnovers[IMPLEMENTABLE_MODELS]

    extended_returns = final_returns[EXTENDED_MODELS]
    extended_turnovers = final_turnovers[EXTENDED_MODELS]

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
        returns=final_returns,
        turnovers=final_turnovers,
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

    final_returns.to_csv(final_returns_path)
    final_turnovers.to_csv(final_turnovers_path)
    implementable_summary.to_csv(implementable_summary_path)
    extended_summary.to_csv(extended_summary_path)

    crisis_long.to_csv(crisis_long_path, index=False)
    crisis_period_return.to_csv(crisis_period_return_path)
    crisis_maxdd.to_csv(crisis_maxdd_path)
    crisis_sharpe.to_csv(crisis_sharpe_path)

    plot_cumulative_returns(
        implementable_returns,
        OUTPUT_CHARTS_DIR / f"{market}_final_implementable_cumulative_returns.png",
        title="US - Final Implementable Strategies: Cumulative Wealth",
    )

    plot_drawdowns(
        implementable_returns,
        OUTPUT_CHARTS_DIR / f"{market}_final_implementable_drawdowns.png",
        title="US - Final Implementable Strategies: Drawdowns",
    )

    plot_cumulative_returns(
        extended_returns,
        OUTPUT_CHARTS_DIR / f"{market}_final_extended_cumulative_returns_with_synthetic_vrp.png",
        title="US - Final Strategies Including Synthetic Pure VRP Proxy",
    )

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 100)
    print("FINAL US — Implementable strategy summary")
    print("=" * 100)
    print(implementable_summary.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL US — Extended summary including Synthetic Pure VRP Proxy")
    print("=" * 100)
    print(extended_summary.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL US — Crisis analysis: Period Return")
    print("=" * 100)
    print(crisis_period_return.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL US — Crisis analysis: Max Drawdown")
    print("=" * 100)
    print(crisis_maxdd.round(4).to_string())

    print("\n" + "=" * 100)
    print("FINAL US — Crisis analysis: Sharpe")
    print("=" * 100)
    print(crisis_sharpe.round(4).to_string())

    print("\nSaved final files:")
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
    run_final_us_report()