from __future__ import annotations

import pandas as pd


from src.config import (
    BASE_TRANSACTION_COST_BPS,
    DATA_PROCESSED_DIR,
    OUTPUT_TABLES_DIR,
    PERIODS_PER_YEAR_MONTHLY,
)
from src.benchmarks import build_benchmark_strategies
from src.hmm_models import HMMBacktestConfig, build_hmm_strategy_set
from src.performance_metrics import summarize_strategies


def run_mvp2_hmm(market: str = "us") -> None:
    market = market.lower()

    monthly_path = DATA_PROCESSED_DIR / f"{market}_monthly_rebalance.csv"

    if not monthly_path.exists():
        raise FileNotFoundError(
            f"Missing monthly dataset: {monthly_path}. Run main_mvp1.py first."
        )

    monthly = pd.read_csv(monthly_path, index_col=0, parse_dates=True)

    print("\n" + "=" * 80)
    print(f"Running MVP 2 HMM pipeline for {market.upper()}")
    print("=" * 80)
    print(f"Monthly dataset shape: {monthly.shape}")
    print(f"Date range: {monthly.index.min().date()} → {monthly.index.max().date()}")

    benchmark_returns, benchmark_turnovers = build_benchmark_strategies(
        monthly,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    hmm_config = HMMBacktestConfig(
        n_components=2,
        train_window=72,
        covariance_type="diag",
        n_iter=300,
        tol=1e-3,
        random_state=42,
        normal_equity_weight=0.80,
        stress_equity_weight=0.20,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    hmm_returns, hmm_turnovers, hmm_diagnostics = build_hmm_strategy_set(
        monthly,
        config=hmm_config,
    )

    all_returns = pd.concat([benchmark_returns, hmm_returns], axis=1).dropna(how="all")
    all_turnovers = pd.concat([benchmark_turnovers, hmm_turnovers], axis=1).reindex(
        all_returns.index
    )

    summary = summarize_strategies(
        all_returns,
        turnovers=all_turnovers,
        periods_per_year=PERIODS_PER_YEAR_MONTHLY,
    )

    all_returns_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_hmm_strategy_returns.csv"
    all_turnovers_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_hmm_turnovers.csv"
    summary_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_hmm_performance_summary.csv"

    all_returns.to_csv(all_returns_path)
    all_turnovers.to_csv(all_turnovers_path)
    summary.to_csv(summary_path)

    for strategy_name, diag in hmm_diagnostics.items():
        safe_name = strategy_name.lower().replace(" ", "_").replace("/", "_")
        diag_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_{safe_name}_diagnostics.csv"
        diag.to_csv(diag_path)

    hmm_index = hmm_returns.dropna(how="all").index

    aligned_returns = all_returns.reindex(hmm_index).dropna(how="all")
    aligned_turnovers = all_turnovers.reindex(aligned_returns.index)

    aligned_summary = summarize_strategies(
        aligned_returns,
        turnovers=aligned_turnovers,
        periods_per_year=PERIODS_PER_YEAR_MONTHLY,
    )

    aligned_summary_path = OUTPUT_TABLES_DIR / f"{market}_mvp2_hmm_aligned_performance_summary.csv"
    aligned_summary.to_csv(aligned_summary_path)

    print("\nPerformance summary:")
    print(summary.round(4))

    print("\nSaved MVP 2 outputs:")
    print(all_returns_path)
    print(all_turnovers_path)
    print(summary_path)

    print("\nHMM diagnostic files saved in outputs/tables/.")

    print("\nAligned performance summary:")
    print(aligned_summary.round(4))

    print("\nSaved aligned performance summary:")
    print(aligned_summary_path)


if __name__ == "__main__":
    run_mvp2_hmm("us")