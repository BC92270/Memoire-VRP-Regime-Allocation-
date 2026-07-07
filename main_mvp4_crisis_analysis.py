from __future__ import annotations

import pandas as pd

from src.config import OUTPUT_TABLES_DIR
from src.performance_metrics import summarize_strategies


CRISIS_WINDOWS = {
    "Full aligned sample": ("2005-01-01", "2026-12-31"),
    "Global Financial Crisis": ("2007-07-01", "2009-06-30"),
    "Eurozone Crisis": ("2010-01-01", "2012-12-31"),
    "Volmageddon and late cycle": ("2018-01-01", "2018-12-31"),
    "Covid Crisis": ("2020-02-01", "2020-06-30"),
    "Inflation Rate Shock": ("2022-01-01", "2022-12-31"),
}


CORE_CRISIS_MODELS = [
    "Buy-and-Hold Equity",
    "60/40",
    "1/N Equity-Bond",
    "HMM RV + Log VRP",
    "HMM RV + Raw VRP",
    "RSM RV + Raw VRP",
]


def load_core_returns_and_turnovers(market: str = "us") -> tuple[pd.DataFrame, pd.DataFrame]:
    returns_path = OUTPUT_TABLES_DIR / f"{market}_core_model_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_core_model_turnovers.csv"

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing returns file: {returns_path}")

    if not turnovers_path.exists():
        raise FileNotFoundError(f"Missing turnovers file: {turnovers_path}")

    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    turnovers = pd.read_csv(turnovers_path, index_col=0, parse_dates=True)

    missing = [m for m in CORE_CRISIS_MODELS if m not in returns.columns]
    if missing:
        raise ValueError(f"Missing models in core returns: {missing}")

    returns = returns[CORE_CRISIS_MODELS].dropna(how="any")
    turnovers = turnovers[CORE_CRISIS_MODELS].reindex(returns.index)

    return returns, turnovers


def cumulative_return(returns: pd.Series) -> float:
    returns = returns.dropna()
    if returns.empty:
        return float("nan")
    return float((1.0 + returns).prod() - 1.0)


def crisis_window_summary(
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
    summary["Start"] = pd.to_datetime(start)
    summary["End"] = pd.to_datetime(end)

    return summary


def run_crisis_analysis(market: str = "us") -> None:
    market = market.lower()

    returns, turnovers = load_core_returns_and_turnovers(market)

    all_rows = []

    for window_name, (start, end) in CRISIS_WINDOWS.items():
        summary = crisis_window_summary(
            returns=returns,
            turnovers=turnovers,
            start=start,
            end=end,
        )

        if summary.empty:
            print(f"Skipping {window_name}: insufficient observations.")
            continue

        summary.insert(0, "Window", window_name)
        summary.insert(1, "Strategy", summary.index)

        all_rows.append(summary.reset_index(drop=True))

    crisis_summary = pd.concat(all_rows, axis=0, ignore_index=True)

    output_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_crisis_subperiod_summary.csv"
    crisis_summary.to_csv(output_path, index=False)

    # Compact pivots for thesis tables
    sharpe_pivot = crisis_summary.pivot(
        index="Strategy",
        columns="Window",
        values="Sharpe",
    )

    maxdd_pivot = crisis_summary.pivot(
        index="Strategy",
        columns="Window",
        values="Max Drawdown",
    )

    period_return_pivot = crisis_summary.pivot(
        index="Strategy",
        columns="Window",
        values="Period Return",
    )

    sharpe_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_crisis_sharpe.csv"
    maxdd_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_crisis_max_drawdown.csv"
    period_return_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_crisis_period_return.csv"

    sharpe_pivot.to_csv(sharpe_path)
    maxdd_pivot.to_csv(maxdd_path)
    period_return_pivot.to_csv(period_return_path)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 100)
    print("MVP 4D — Crisis analysis: Period Return")
    print("=" * 100)
    print(period_return_pivot.round(4).to_string())

    print("\n" + "=" * 100)
    print("MVP 4D — Crisis analysis: Max Drawdown")
    print("=" * 100)
    print(maxdd_pivot.round(4).to_string())

    print("\n" + "=" * 100)
    print("MVP 4D — Crisis analysis: Sharpe")
    print("=" * 100)
    print(sharpe_pivot.round(4).to_string())

    print("\nSaved crisis analysis files:")
    print(output_path)
    print(sharpe_path)
    print(maxdd_path)
    print(period_return_path)


if __name__ == "__main__":
    run_crisis_analysis("us")