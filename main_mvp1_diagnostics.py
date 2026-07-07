from __future__ import annotations

import pandas as pd
import sys

from src.config import OUTPUT_CHARTS_DIR, OUTPUT_TABLES_DIR
from src.plots import (
    plot_cumulative_returns,
    plot_drawdowns,
    plot_feature_correlation_heatmap,
    plot_vrp_components,
)


def describe_features(monthly: pd.DataFrame) -> pd.DataFrame:
    """
    Builds descriptive statistics for the core monthly variables.
    """
    cols = [
        "equity_ret",
        "bond_ret",
        "rv_ann",
        "iv_ann",
        "vrp_proxy",
        "implied_vol_index",
    ]

    available_cols = [c for c in cols if c in monthly.columns]
    data = monthly[available_cols].dropna()

    desc = pd.DataFrame(index=available_cols)
    desc["mean"] = data.mean()
    desc["std"] = data.std()
    desc["min"] = data.min()
    desc["p05"] = data.quantile(0.05)
    desc["median"] = data.median()
    desc["p95"] = data.quantile(0.95)
    desc["max"] = data.max()
    desc["skew"] = data.skew()
    desc["kurtosis"] = data.kurtosis()
    desc["obs"] = data.count()

    return desc


def compute_autocorrelations(monthly: pd.DataFrame, lags: list[int] | None = None) -> pd.DataFrame:
    """
    Computes simple autocorrelations for core features.
    """
    if lags is None:
        lags = [1, 3, 6, 12]

    cols = [
        "equity_ret",
        "rv_ann",
        "iv_ann",
        "vrp_proxy",
        "implied_vol_index",
    ]

    available_cols = [c for c in cols if c in monthly.columns]
    rows = {}

    for col in available_cols:
        rows[col] = {}
        series = monthly[col].dropna()
        for lag in lags:
            rows[col][f"acf_lag_{lag}"] = series.autocorr(lag=lag)

    return pd.DataFrame(rows).T


def run_mvp1_diagnostics(market: str = "us") -> None:
    market = market.lower()

    monthly_path = OUTPUT_TABLES_DIR.parents[1] / "data" / "processed" / f"{market}_monthly_rebalance.csv"
    returns_path = OUTPUT_TABLES_DIR / f"{market}_mvp1_strategy_returns.csv"
    summary_path = OUTPUT_TABLES_DIR / f"{market}_mvp1_performance_summary.csv"

    if not monthly_path.exists():
        raise FileNotFoundError(f"Missing monthly dataset: {monthly_path}")

    if not returns_path.exists():
        raise FileNotFoundError(f"Missing strategy returns file: {returns_path}")

    monthly = pd.read_csv(monthly_path, index_col=0, parse_dates=True)
    strategy_returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)

    feature_desc = describe_features(monthly)
    feature_corr = monthly[
        [
            "equity_ret",
            "bond_ret",
            "rv_ann",
            "iv_ann",
            "vrp_proxy",
            "implied_vol_index",
        ]
    ].corr()
    autocorr = compute_autocorrelations(monthly)

    feature_desc_path = OUTPUT_TABLES_DIR / f"{market}_mvp1_feature_descriptive_stats.csv"
    feature_corr_path = OUTPUT_TABLES_DIR / f"{market}_mvp1_feature_correlations.csv"
    autocorr_path = OUTPUT_TABLES_DIR / f"{market}_mvp1_feature_autocorrelations.csv"

    feature_desc.to_csv(feature_desc_path)
    feature_corr.to_csv(feature_corr_path)
    autocorr.to_csv(autocorr_path)

    plot_vrp_components(
        monthly,
        OUTPUT_CHARTS_DIR / f"{market}_mvp1_vrp_components.png",
        title=f"{market.upper()} - IV, RV and VRP Proxy",
    )

    plot_cumulative_returns(
        strategy_returns,
        OUTPUT_CHARTS_DIR / f"{market}_mvp1_cumulative_returns.png",
        title=f"{market.upper()} - Cumulative Benchmark Returns",
    )

    plot_drawdowns(
        strategy_returns,
        OUTPUT_CHARTS_DIR / f"{market}_mvp1_drawdowns.png",
        title=f"{market.upper()} - Benchmark Drawdowns",
    )

    plot_feature_correlation_heatmap(
        feature_corr,
        OUTPUT_CHARTS_DIR / f"{market}_mvp1_feature_correlation_heatmap.png",
        title=f"{market.upper()} - Feature Correlation Matrix",
    )

    print("\n" + "=" * 80)
    print(f"MVP 1 diagnostics complete for {market.upper()}")
    print("=" * 80)

    print("\nFeature descriptive statistics:")
    print(feature_desc.round(4))

    print("\nFeature correlations:")
    print(feature_corr.round(4))

    print("\nFeature autocorrelations:")
    print(autocorr.round(4))

    if summary_path.exists():
        summary = pd.read_csv(summary_path, index_col=0)
        print("\nExisting performance summary:")
        print(summary.round(4))

    print("\nSaved diagnostic tables:")
    print(feature_desc_path)
    print(feature_corr_path)
    print(autocorr_path)

    print("\nSaved diagnostic charts:")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp1_vrp_components.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp1_cumulative_returns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp1_drawdowns.png")
    print(OUTPUT_CHARTS_DIR / f"{market}_mvp1_feature_correlation_heatmap.png")


if __name__ == "__main__":
    market = sys.argv[1] if len(sys.argv) > 1 else "us"
    run_mvp1_diagnostics(market)