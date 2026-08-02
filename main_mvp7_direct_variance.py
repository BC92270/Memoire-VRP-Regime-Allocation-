from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.direct_variance import (
    DirectVarianceConfig,
    build_direct_variance_strategy_set,
    summarize_direct_variance_diagnostics,
)
from src.performance_metrics import (
    summarize_strategies,
)


PROCESSED_DIR = Path(
    "data/processed"
)

TABLES_DIR = Path(
    "outputs/tables"
)


def read_indexed_csv(
    path: Path,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )

    frame = pd.read_csv(
        path,
        index_col=0,
    )

    frame.index = pd.to_datetime(
        frame.index,
        errors="coerce",
    )

    frame = frame.loc[
        ~frame.index.isna()
    ]

    frame = frame.loc[
        ~frame.index.duplicated(
            keep="last"
        )
    ].sort_index()

    frame.index.name = "Date"

    frame.columns = [
        str(column).strip()
        for column in frame.columns
    ]

    return frame


def load_monthly(
    market: str,
) -> pd.DataFrame:
    return read_indexed_csv(
        PROCESSED_DIR
        / f"{market}_monthly_rebalance.csv"
    )


def load_mvp1_benchmarks(
    market: str,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
]:
    returns = read_indexed_csv(
        TABLES_DIR
        / f"{market}_mvp1_strategy_returns.csv"
    )

    turnovers = read_indexed_csv(
        TABLES_DIR
        / f"{market}_mvp1_turnovers.csv"
    )

    common_columns = [
        column
        for column in returns.columns
        if column in turnovers.columns
    ]

    return (
        returns[common_columns],
        turnovers[common_columns],
    )


def add_model_groups(
    performance: pd.DataFrame,
) -> pd.DataFrame:
    result = performance.copy()

    groups = []

    for strategy in result.index.astype(
        str
    ):
        if strategy.startswith(
            "Direct Short Variance"
        ):
            groups.append(
                "Direct Variance Approximation"
            )

        elif strategy == "Pure VRP Proxy":
            groups.append(
                "Synthetic Log-VRP Proxy"
            )

        else:
            groups.append(
                "Benchmark"
            )

    result.insert(
        0,
        "Model Group",
        groups,
    )

    return result


def build_payoff_summary(
    market: str,
    panel: pd.DataFrame,
) -> pd.DataFrame:
    valid = panel.dropna(
        subset=[
            "variance_strike",
            "settlement_realized_variance",
            "short_variance_payoff",
            "normalized_short_payoff",
        ]
    )

    normalized = valid[
        "normalized_short_payoff"
    ]

    row = {
        "Market": market.upper(),
        "Observations": int(
            len(valid)
        ),
        "Start": (
            valid.index.min()
        ),
        "End": (
            valid.index.max()
        ),
        "Mean Variance Strike": float(
            valid[
                "variance_strike"
            ].mean()
        ),
        "Mean Realized Variance": float(
            valid[
                "settlement_realized_variance"
            ].mean()
        ),
        "Mean Short Variance Payoff": float(
            valid[
                "short_variance_payoff"
            ].mean()
        ),
        "Positive Payoff Rate": float(
            valid[
                "short_variance_payoff"
            ].gt(0.0).mean()
        ),
        "Mean Normalized Payoff": float(
            normalized.mean()
        ),
        "Median Normalized Payoff": float(
            normalized.median()
        ),
        "Normalized Payoff Vol": float(
            normalized.std(ddof=1)
        ),
        "Normalized Payoff Skew": float(
            normalized.skew()
        ),
        "Normalized Payoff 5%": float(
            normalized.quantile(0.05)
        ),
        "Normalized Payoff 1%": float(
            normalized.quantile(0.01)
        ),
        "Worst Normalized Payoff": float(
            normalized.min()
        ),
        "Months Below -100%": int(
            normalized.le(-1.0).sum()
        ),
        "Months Below -100% Rate": float(
            normalized.le(-1.0).mean()
        ),
    }

    return pd.DataFrame(
        [row]
    )


def run_market(
    market: str,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    monthly = load_monthly(
        market
    )

    config = DirectVarianceConfig(
        volatility_lookback_months=36,
        minimum_volatility_observations=24,
        high_vrp_lookback_months=36,
        minimum_vrp_observations=24,
        max_abs_notional=0.25,
        transaction_cost_bps=10.0,
    )

    (
        direct_returns,
        direct_turnovers,
        diagnostics,
        panel,
    ) = build_direct_variance_strategy_set(
        monthly=monthly,
        config=config,
    )

    direct_performance = (
        summarize_strategies(
            direct_returns,
            turnovers=direct_turnovers,
            periods_per_year=12,
        )
    )

    direct_performance = (
        add_model_groups(
            direct_performance
        )
    )

    diagnostic_summary = (
        summarize_direct_variance_diagnostics(
            diagnostics
        )
    )

    payoff_summary = build_payoff_summary(
        market=market,
        panel=panel,
    )

    (
        benchmark_returns,
        benchmark_turnovers,
    ) = load_mvp1_benchmarks(
        market
    )

    combined_returns = pd.concat(
        [
            benchmark_returns,
            direct_returns,
        ],
        axis=1,
    ).dropna(
        how="any"
    )

    combined_turnovers = pd.concat(
        [
            benchmark_turnovers,
            direct_turnovers,
        ],
        axis=1,
    ).reindex(
        index=combined_returns.index,
        columns=combined_returns.columns,
    ).fillna(0.0)

    combined_performance = (
        summarize_strategies(
            combined_returns,
            turnovers=combined_turnovers,
            periods_per_year=12,
        )
    )

    combined_performance = (
        add_model_groups(
            combined_performance
        )
    )

    output_paths = {
        "panel": (
            TABLES_DIR
            / f"{market}_direct_variance_panel.csv"
        ),
        "returns": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "strategy_returns.csv"
            )
        ),
        "turnovers": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "turnovers.csv"
            )
        ),
        "diagnostics": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "diagnostics.csv"
            )
        ),
        "diagnostic_summary": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "diagnostic_summary.csv"
            )
        ),
        "payoff_summary": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "payoff_summary.csv"
            )
        ),
        "performance": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "performance.csv"
            )
        ),
        "combined_returns": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "vs_benchmarks_returns.csv"
            )
        ),
        "combined_performance": (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                "vs_benchmarks_performance.csv"
            )
        ),
    }

    panel.to_csv(
        output_paths["panel"]
    )

    direct_returns.to_csv(
        output_paths["returns"]
    )

    direct_turnovers.to_csv(
        output_paths["turnovers"]
    )

    diagnostics.to_csv(
        output_paths["diagnostics"],
        index=False,
    )

    diagnostic_summary.to_csv(
        output_paths[
            "diagnostic_summary"
        ],
        index=False,
    )

    payoff_summary.to_csv(
        output_paths["payoff_summary"],
        index=False,
    )

    direct_performance.to_csv(
        output_paths["performance"]
    )

    combined_returns.to_csv(
        output_paths["combined_returns"]
    )

    combined_performance.to_csv(
        output_paths[
            "combined_performance"
        ]
    )

    print("=" * 120)
    print(
        f"{market.upper()} — "
        "MVP 7 DIRECT VARIANCE CARRY"
    )
    print("=" * 120)

    print(
        f"Monthly source observations: "
        f"{len(monthly)}"
    )

    print(
        "Direct-strategy observations: "
        f"{len(direct_returns)}"
    )

    print(
        "Direct-strategy sample: "
        f"{direct_returns.index.min().date()} "
        "-> "
        f"{direct_returns.index.max().date()}"
    )

    print()
    print("UNDERLYING PAYOFF DIAGNOSTICS")

    display_payoff_columns = [
        "Mean Variance Strike",
        "Mean Realized Variance",
        "Mean Short Variance Payoff",
        "Positive Payoff Rate",
        "Mean Normalized Payoff",
        "Normalized Payoff Skew",
        "Normalized Payoff 1%",
        "Worst Normalized Payoff",
        "Months Below -100% Rate",
    ]

    print(
        payoff_summary[
            display_payoff_columns
        ].to_string(
            index=False
        )
    )

    print()
    print("NOTIONAL AND IMPLEMENTATION")

    print(
        diagnostic_summary.to_string(
            index=False
        )
    )

    print()
    print(
        "ECONOMIC PERFORMANCE — "
        "COMMON SAMPLE"
    )

    display_columns = [
        column
        for column in [
            "Model Group",
            "Ann. Return",
            "Ann. Vol",
            "Sharpe",
            "Sortino",
            "Max Drawdown",
            "Calmar",
            "CVaR 95",
            "Avg Turnover",
            "Obs",
        ]
        if column
        in combined_performance.columns
    ]

    sort_column = (
        "Sharpe"
        if "Sharpe"
        in combined_performance.columns
        else combined_performance.columns[0]
    )

    print(
        combined_performance[
            display_columns
        ]
        .sort_values(
            sort_column,
            ascending=False,
        )
        .to_string()
    )

    print()
    print("OUTPUTS")

    for label, path in (
        output_paths.items()
    ):
        print(
            f"- {label}: {path}"
        )

    market_performance = (
        combined_performance
        .reset_index()
    )

    strategy_column = (
        market_performance
        .columns[0]
    )

    market_performance = (
        market_performance.rename(
            columns={
                strategy_column: "Strategy"
            }
        )
    )

    market_performance.insert(
        0,
        "Market",
        market.upper(),
    )

    return (
        payoff_summary,
        diagnostic_summary.assign(
            Market=market.upper()
        ),
        market_performance,
    )


def main() -> None:
    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    payoff_frames = []
    diagnostic_frames = []
    performance_frames = []

    for market in (
        "us",
        "eu",
    ):
        (
            payoff,
            diagnostics,
            performance,
        ) = run_market(
            market
        )

        payoff_frames.append(
            payoff
        )

        diagnostic_frames.append(
            diagnostics
        )

        performance_frames.append(
            performance
        )

    cross_payoff = pd.concat(
        payoff_frames,
        ignore_index=True,
    )

    cross_diagnostics = pd.concat(
        diagnostic_frames,
        ignore_index=True,
    )

    cross_performance = pd.concat(
        performance_frames,
        ignore_index=True,
    )

    payoff_path = (
        TABLES_DIR
        / (
            "cross_market_direct_variance_"
            "payoff_summary.csv"
        )
    )

    diagnostic_path = (
        TABLES_DIR
        / (
            "cross_market_direct_variance_"
            "diagnostics.csv"
        )
    )

    performance_path = (
        TABLES_DIR
        / (
            "cross_market_direct_variance_"
            "performance.csv"
        )
    )

    cross_payoff.to_csv(
        payoff_path,
        index=False,
    )

    cross_diagnostics.to_csv(
        diagnostic_path,
        index=False,
    )

    cross_performance.to_csv(
        performance_path,
        index=False,
    )

    print("=" * 120)
    print(
        "MVP 7 DIRECT VARIANCE "
        "CARRY COMPLETE"
    )
    print("=" * 120)

    print(
        f"Cross-market payoff: "
        f"{payoff_path}"
    )

    print(
        f"Cross-market diagnostics: "
        f"{diagnostic_path}"
    )

    print(
        f"Cross-market performance: "
        f"{performance_path}"
    )


if __name__ == "__main__":
    main()
