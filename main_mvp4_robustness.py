from __future__ import annotations

import pandas as pd

from src.config import (
    BASE_TRANSACTION_COST_BPS,
    DATA_PROCESSED_DIR,
    OUTPUT_TABLES_DIR,
)
from src.robustness import (
    no_trade_band_sensitivity,
    transaction_cost_sensitivity,
)


COST_BPS_GRID = [0, 5, 10, 25, 50]
NO_TRADE_BANDS = [0.00, 0.02, 0.05, 0.10]

# Pure VRP is not initially netted the same way as the other strategies.
NO_ADDBACK_COLUMNS = ["Pure VRP Proxy"]


DYNAMIC_DIAGNOSTIC_FILES = {
    "HMM RV": "us_hmm_grid_hmm_rv_diagnostics.csv",
    "HMM RV + Raw VRP": "us_hmm_grid_hmm_rv_plus_raw_vrp_diagnostics.csv",
    "HMM RV + Log VRP": "us_hmm_grid_hmm_rv_plus_log_vrp_diagnostics.csv",
    "RSM Returns Only": "us_mvp3_rsm_returns_only_diagnostics.csv",
    "RSM RV": "us_mvp3_rsm_rv_diagnostics.csv",
    "RSM RV + Raw VRP": "us_mvp3_rsm_rv_plus_raw_vrp_diagnostics.csv",
    "RSM RV + Log VRP": "us_mvp3_rsm_rv_plus_log_vrp_diagnostics.csv",
}


def load_core_outputs(market: str = "us") -> tuple[pd.DataFrame, pd.DataFrame]:
    market = market.lower()

    returns_path = OUTPUT_TABLES_DIR / f"{market}_core_model_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_core_model_turnovers.csv"

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing core returns file: {returns_path}")

    if not turnovers_path.exists():
        raise FileNotFoundError(f"Missing core turnovers file: {turnovers_path}")

    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)
    turnovers = pd.read_csv(turnovers_path, index_col=0, parse_dates=True)

    return returns, turnovers


def load_dynamic_diagnostics() -> dict[str, pd.DataFrame]:
    diagnostics = {}

    for strategy, filename in DYNAMIC_DIAGNOSTIC_FILES.items():
        path = OUTPUT_TABLES_DIR / filename

        if not path.exists():
            print(f"Warning: missing diagnostics for {strategy}: {path}")
            continue

        diagnostics[strategy] = pd.read_csv(path, index_col=0, parse_dates=True)

    if not diagnostics:
        raise RuntimeError("No dynamic diagnostics were loaded.")

    return diagnostics


def run_transaction_cost_robustness(market: str = "us") -> None:
    returns, turnovers = load_core_outputs(market)

    long_summary, sharpe_pivot, maxdd_pivot, _net_returns_by_cost = transaction_cost_sensitivity(
        net_returns=returns,
        turnovers=turnovers,
        cost_bps_grid=COST_BPS_GRID,
        base_cost_bps=BASE_TRANSACTION_COST_BPS,
        periods_per_year=12,
        no_addback_columns=NO_ADDBACK_COLUMNS,
    )

    long_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_cost_sensitivity_long.csv"
    sharpe_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_cost_sensitivity_sharpe.csv"
    maxdd_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_cost_sensitivity_max_drawdown.csv"

    long_summary.to_csv(long_path, index=False)
    sharpe_pivot.to_csv(sharpe_path)
    maxdd_pivot.to_csv(maxdd_path)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 100)
    print("MVP 4A — Transaction cost sensitivity: Sharpe")
    print("=" * 100)
    print(sharpe_pivot.round(4).to_string())

    print("\n" + "=" * 100)
    print("MVP 4A — Transaction cost sensitivity: Max Drawdown")
    print("=" * 100)
    print(maxdd_pivot.round(4).to_string())

    print("\nSaved cost sensitivity files:")
    print(long_path)
    print(sharpe_path)
    print(maxdd_path)


def run_no_trade_band_robustness(market: str = "us") -> None:
    market = market.lower()

    monthly_path = DATA_PROCESSED_DIR / f"{market}_monthly_rebalance.csv"

    if not monthly_path.exists():
        raise FileNotFoundError(f"Missing monthly data: {monthly_path}")

    monthly = pd.read_csv(monthly_path, index_col=0, parse_dates=True)
    diagnostics = load_dynamic_diagnostics()

    long_summary, sharpe_pivot, turnover_pivot = no_trade_band_sensitivity(
        monthly=monthly,
        diagnostics_by_strategy=diagnostics,
        no_trade_bands=NO_TRADE_BANDS,
        cost_bps=BASE_TRANSACTION_COST_BPS,
        periods_per_year=12,
    )

    long_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_no_trade_band_long.csv"
    sharpe_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_no_trade_band_sharpe.csv"
    turnover_path = OUTPUT_TABLES_DIR / f"{market}_mvp4_no_trade_band_turnover.csv"

    long_summary.to_csv(long_path, index=False)
    sharpe_pivot.to_csv(sharpe_path)
    turnover_pivot.to_csv(turnover_path)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 100)
    print("MVP 4B — No-trade band sensitivity: Sharpe")
    print("=" * 100)
    print(sharpe_pivot.round(4).to_string())

    print("\n" + "=" * 100)
    print("MVP 4B — No-trade band sensitivity: Avg Turnover")
    print("=" * 100)
    print(turnover_pivot.round(4).to_string())

    print("\nSaved no-trade band files:")
    print(long_path)
    print(sharpe_path)
    print(turnover_path)


def main() -> None:
    run_transaction_cost_robustness("us")
    run_no_trade_band_robustness("us")


if __name__ == "__main__":
    main()