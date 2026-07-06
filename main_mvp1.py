from __future__ import annotations

import pandas as pd

from src.config import (
    BASE_TRANSACTION_COST_BPS,
    END_DATE,
    MARKET_CONFIGS,
    OUTPUT_TABLES_DIR,
    PERIODS_PER_YEAR_MONTHLY,
    RV_WINDOW_DAYS,
    START_DATE,
    TRADING_DAYS_PER_YEAR,
    DATA_PROCESSED_DIR,
)
from src.data_loader import build_market_dataset
from src.features_vrp import build_daily_feature_set, build_monthly_rebalance_dataset
from src.benchmarks import build_benchmark_strategies
from src.performance_metrics import summarize_strategies


def run_market_pipeline(market_name: str, market_config: dict) -> None:
    print("\n" + "=" * 80)
    print(f"Running MVP 1 pipeline for {market_name}")
    print("=" * 80)

    daily_raw, selected_tickers = build_market_dataset(
        market_name=market_name,
        market_config=market_config,
        start=START_DATE,
        end=END_DATE,
    )

    daily_features = build_daily_feature_set(
        daily_raw,
        rv_window=RV_WINDOW_DAYS,
        trading_days_per_year=TRADING_DAYS_PER_YEAR,
    )

    monthly = build_monthly_rebalance_dataset(daily_features)

    daily_path = DATA_PROCESSED_DIR / f"{market_name.lower()}_daily_features.csv"
    monthly_path = DATA_PROCESSED_DIR / f"{market_name.lower()}_monthly_rebalance.csv"

    daily_features.to_csv(daily_path)
    monthly.to_csv(monthly_path)

    print(f"[{market_name}] Saved daily features: {daily_path}")
    print(f"[{market_name}] Saved monthly dataset: {monthly_path}")
    print(f"[{market_name}] Monthly dataset shape: {monthly.shape}")

    strategy_returns, turnovers = build_benchmark_strategies(
        monthly,
        transaction_cost_bps=BASE_TRANSACTION_COST_BPS,
    )

    summary = summarize_strategies(
        strategy_returns,
        turnovers=turnovers,
        periods_per_year=PERIODS_PER_YEAR_MONTHLY,
    )

    returns_path = OUTPUT_TABLES_DIR / f"{market_name.lower()}_mvp1_strategy_returns.csv"
    turnover_path = OUTPUT_TABLES_DIR / f"{market_name.lower()}_mvp1_turnovers.csv"
    summary_path = OUTPUT_TABLES_DIR / f"{market_name.lower()}_mvp1_performance_summary.csv"

    strategy_returns.to_csv(returns_path)
    turnovers.to_csv(turnover_path)
    summary.to_csv(summary_path)

    print(f"[{market_name}] Saved strategy returns: {returns_path}")
    print(f"[{market_name}] Saved turnovers: {turnover_path}")
    print(f"[{market_name}] Saved performance summary: {summary_path}")

    print("\nSelected tickers:")
    print(selected_tickers)

    print("\nPerformance summary:")
    print(summary.round(4))


def main() -> None:
    successful_markets = []
    failed_markets = {}

    for market_name, market_config in MARKET_CONFIGS.items():
        try:
            run_market_pipeline(market_name, market_config)
            successful_markets.append(market_name)
        except Exception as exc:
            failed_markets[market_name] = str(exc)
            print("\n" + "!" * 80)
            print(f"Pipeline failed for {market_name}")
            print(type(exc).__name__, exc)
            print("!" * 80)

    print("\n" + "=" * 80)
    print("MVP 1 complete")
    print("=" * 80)
    print(f"Successful markets: {successful_markets}")

    if failed_markets:
        print("\nFailed markets:")
        for market, error in failed_markets.items():
            print(f"- {market}: {error}")


if __name__ == "__main__":
    main()