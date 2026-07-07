from __future__ import annotations

import sys
import pandas as pd

from src.config import (
    BASE_TRANSACTION_COST_BPS,
    DATA_PROCESSED_DIR,
    OUTPUT_TABLES_DIR,
    PERIODS_PER_YEAR_MONTHLY,
)
from src.benchmarks import build_benchmark_strategies
from src.hmm_models import HMMBacktestConfig, run_rolling_hmm_backtest
from src.performance_metrics import summarize_strategies


HMM_FEATURE_SPECS = {
    "HMM RV": ["equity_ret", "log_rv_ann"],
    "HMM RV + Raw VRP": ["equity_ret", "log_rv_ann", "vrp_proxy"],
    "HMM RV + Log VRP": ["equity_ret", "log_rv_ann", "log_iv_rv"],
    "HMM IV": ["equity_ret", "log_iv_ann"],
    "HMM IV + Log VRP": ["equity_ret", "log_iv_ann", "log_iv_rv"],
    "HMM RV + IV": ["equity_ret", "log_rv_ann", "log_iv_ann"],
    "HMM RV + IV + Log VRP": [
        "equity_ret",
        "log_rv_ann",
        "log_iv_ann",
        "log_iv_rv",
    ],
}


def _safe_name(name: str) -> str:
    """
    Converts strategy names into stable file-safe names.

    Example:
        HMM RV + Log VRP -> hmm_rv_plus_log_vrp
    """
    return (
        name.lower()
        .replace(" ", "_")
        .replace("/", "_")
        .replace("+", "plus")
        .replace("-", "_")
        .replace("__", "_")
    )


def _validate_required_columns(monthly: pd.DataFrame, specs: dict[str, list[str]]) -> None:
    """
    Ensures all features required by the HMM grid exist in the monthly dataset.
    """
    required = set()

    for features in specs.values():
        required.update(features)

    missing = sorted([col for col in required if col not in monthly.columns])

    if missing:
        raise ValueError(
            "Missing required columns in monthly dataset: "
            f"{missing}. Run main_mvp1.py again after updating features_vrp.py."
        )


def run_hmm_spec_grid(market: str = "us") -> None:
    market = market.lower()

    monthly_path = DATA_PROCESSED_DIR / f"{market}_monthly_rebalance.csv"

    if not monthly_path.exists():
        raise FileNotFoundError(
            f"Missing monthly dataset: {monthly_path}. Run main_mvp1.py first."
        )

    monthly = pd.read_csv(monthly_path, index_col=0, parse_dates=True)

    print("\n" + "=" * 80)
    print(f"Running HMM specification grid for {market.upper()}")
    print("=" * 80)
    print(f"Monthly dataset shape: {monthly.shape}")

    if not monthly.empty:
        print(f"Date range: {monthly.index.min().date()} → {monthly.index.max().date()}")

    _validate_required_columns(monthly, HMM_FEATURE_SPECS)

    benchmark_returns, benchmark_turnovers = build_benchmark_strategies(
        monthly,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    # US and EU now both have enough observations for a 72-month rolling window.
    # If the EU sample becomes short again, reduce only here, not inside src/hmm_models.py.
    train_window = 72

    hmm_config = HMMBacktestConfig(
        n_components=2,
        train_window=train_window,
        covariance_type="diag",
        n_iter=300,
        tol=1e-3,
        random_state=42,
        normal_equity_weight=0.80,
        stress_equity_weight=0.20,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    hmm_returns = {}
    hmm_turnovers = {}
    diagnostic_rows = {}

    for strategy_name, features in HMM_FEATURE_SPECS.items():
        print(f"\nRunning {strategy_name} with features: {features}")

        ret, turn, diag = run_rolling_hmm_backtest(
            monthly=monthly,
            feature_columns=features,
            strategy_name=strategy_name,
            config=hmm_config,
        )

        hmm_returns[strategy_name] = ret
        hmm_turnovers[strategy_name] = turn

        diagnostic_rows[strategy_name] = {
            "features": ", ".join(features),
            "obs": diag.shape[0],
            "convergence_rate": diag["converged"].mean()
            if "converged" in diag.columns
            else None,
            "avg_stress_probability": diag["stress_probability"].mean(),
            "median_stress_probability": diag["stress_probability"].median(),
            "p95_stress_probability": diag["stress_probability"].quantile(0.95),
            "max_stress_probability": diag["stress_probability"].max(),
            "avg_equity_weight": diag["equity_weight"].mean(),
            "min_equity_weight": diag["equity_weight"].min(),
            "max_equity_weight": diag["equity_weight"].max(),
            "avg_turnover": diag["turnover"].mean(),
        }

        safe_name = _safe_name(strategy_name)
        diag_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_{safe_name}_diagnostics.csv"
        diag.to_csv(diag_path)

    hmm_returns_df = pd.DataFrame(hmm_returns)
    hmm_turnovers_df = pd.DataFrame(hmm_turnovers)

    all_returns = pd.concat([benchmark_returns, hmm_returns_df], axis=1).dropna(how="all")
    all_turnovers = pd.concat([benchmark_turnovers, hmm_turnovers_df], axis=1).reindex(
        all_returns.index
    )

    # Align all strategies on the HMM out-of-sample dates.
    hmm_index = hmm_returns_df.dropna(how="all").index

    aligned_returns = all_returns.reindex(hmm_index).dropna(how="all")
    aligned_turnovers = all_turnovers.reindex(aligned_returns.index)

    aligned_summary = summarize_strategies(
        aligned_returns,
        turnovers=aligned_turnovers,
        periods_per_year=PERIODS_PER_YEAR_MONTHLY,
    )

    diagnostic_summary = pd.DataFrame(diagnostic_rows).T

    performance_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_aligned_performance_summary.csv"
    diagnostics_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_diagnostic_summary.csv"
    returns_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_strategy_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_hmm_grid_turnovers.csv"

    aligned_summary.to_csv(performance_path)
    diagnostic_summary.to_csv(diagnostics_path)
    aligned_returns.to_csv(returns_path)
    aligned_turnovers.to_csv(turnovers_path)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 100)

    print("\n" + "=" * 80)
    print("Aligned HMM grid performance summary")
    print("=" * 80)
    print(aligned_summary.round(4).to_string())

    print("\n" + "=" * 80)
    print("HMM grid diagnostic summary")
    print("=" * 80)
    print(diagnostic_summary.round(4).to_string())

    print("\nSaved files:")
    print(performance_path)
    print(diagnostics_path)
    print(returns_path)
    print(turnovers_path)


if __name__ == "__main__":
    selected_market = sys.argv[1] if len(sys.argv) > 1 else "us"
    run_hmm_spec_grid(selected_market)