from __future__ import annotations

import pandas as pd

from src.benchmarks import build_benchmark_strategies
from src.config import (
    BASE_TRANSACTION_COST_BPS,
    DATA_PROCESSED_DIR,
    OUTPUT_TABLES_DIR,
    PERIODS_PER_YEAR_MONTHLY,
)
from src.performance_metrics import summarize_strategies
from src.rsm_models import RSMBacktestConfig, build_rsm_strategy_set


def summarize_rsm_diagnostics(diagnostics: dict[str, pd.DataFrame]) -> pd.DataFrame:
    rows = {}

    for strategy, diag in diagnostics.items():
        rows[strategy] = {
            "obs": diag.shape[0],
            "valid_obs": diag["net_return"].notna().sum() if "net_return" in diag else 0,
            "convergence_rate": diag["converged"].mean() if "converged" in diag else None,
            "avg_stress_probability": diag["stress_probability"].mean(),
            "median_stress_probability": diag["stress_probability"].median(),
            "p95_stress_probability": diag["stress_probability"].quantile(0.95),
            "max_stress_probability": diag["stress_probability"].max(),
            "avg_equity_weight": diag["equity_weight"].mean(),
            "min_equity_weight": diag["equity_weight"].min(),
            "max_equity_weight": diag["equity_weight"].max(),
            "avg_turnover": diag["turnover"].mean(),
        }

    return pd.DataFrame(rows).T


def run_mvp3_rsm(market: str = "us") -> None:
    market = market.lower()

    monthly_path = DATA_PROCESSED_DIR / f"{market}_monthly_rebalance.csv"

    if not monthly_path.exists():
        raise FileNotFoundError(
            f"Missing monthly dataset: {monthly_path}. Run main_mvp1.py first."
        )

    monthly = pd.read_csv(monthly_path, index_col=0, parse_dates=True)

    print("\n" + "=" * 80)
    print(f"Running MVP 3 RSM pipeline for {market.upper()}")
    print("=" * 80)
    print(f"Monthly dataset shape: {monthly.shape}")
    print(f"Date range: {monthly.index.min().date()} → {monthly.index.max().date()}")

    benchmark_returns, benchmark_turnovers = build_benchmark_strategies(
        monthly,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    rsm_config = RSMBacktestConfig(
        n_regimes=2,
        train_window=72,
        maxiter=300,
        em_iter=10,
        normal_equity_weight=0.80,
        stress_equity_weight=0.20,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    rsm_returns, rsm_turnovers, rsm_diagnostics = build_rsm_strategy_set(
        monthly,
        config=rsm_config,
    )

    all_returns = pd.concat([benchmark_returns, rsm_returns], axis=1).dropna(how="all")
    all_turnovers = pd.concat([benchmark_turnovers, rsm_turnovers], axis=1).reindex(
        all_returns.index
    )

    rsm_index = rsm_returns.dropna(how="all").index

    aligned_returns = all_returns.reindex(rsm_index).dropna(how="all")
    aligned_turnovers = all_turnovers.reindex(aligned_returns.index)

    aligned_summary = summarize_strategies(
        aligned_returns,
        turnovers=aligned_turnovers,
        periods_per_year=PERIODS_PER_YEAR_MONTHLY,
    )

    diagnostic_summary = summarize_rsm_diagnostics(rsm_diagnostics)

    returns_path = OUTPUT_TABLES_DIR / f"{market}_mvp3_rsm_strategy_returns.csv"
    turnovers_path = OUTPUT_TABLES_DIR / f"{market}_mvp3_rsm_turnovers.csv"
    performance_path = OUTPUT_TABLES_DIR / f"{market}_mvp3_rsm_aligned_performance_summary.csv"
    diagnostics_path = OUTPUT_TABLES_DIR / f"{market}_mvp3_rsm_diagnostic_summary.csv"

    aligned_returns.to_csv(returns_path)
    aligned_turnovers.to_csv(turnovers_path)
    aligned_summary.to_csv(performance_path)
    diagnostic_summary.to_csv(diagnostics_path)

    for strategy_name, diag in rsm_diagnostics.items():
        safe_name = (
            strategy_name.lower()
            .replace(" ", "_")
            .replace("/", "_")
            .replace("+", "plus")
        )
        diag.to_csv(OUTPUT_TABLES_DIR / f"{market}_mvp3_{safe_name}_diagnostics.csv")

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)

    print("\n" + "=" * 80)
    print("Aligned RSM performance summary")
    print("=" * 80)
    print(aligned_summary.round(4))

    print("\n" + "=" * 80)
    print("RSM diagnostic summary")
    print("=" * 80)
    print(diagnostic_summary.round(4).to_string())

    print("\nSaved files:")
    print(returns_path)
    print(turnovers_path)
    print(performance_path)
    print(diagnostics_path)


if __name__ == "__main__":
    run_mvp3_rsm("us")