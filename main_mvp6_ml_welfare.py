from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.welfare import (
    bootstrap_welfare_differences,
    build_welfare_summary,
    clean_return_panel,
)


TABLES_DIR = Path("outputs/tables")

GAMMAS = (
    1.0,
    3.0,
    5.0,
    10.0,
)

BENCHMARKS = (
    "60/40",
    "1/N Equity-Bond",
)

N_BOOTSTRAP = 2_000
BLOCK_LENGTH = 6
SEED = 20260802


def read_return_panel(
    path: Path,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )

    frame = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
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

    frame.columns = [
        str(column).strip()
        for column in frame.columns
    ]

    return clean_return_panel(frame)


def identify_model_group(
    strategy: str,
) -> str:
    if strategy.startswith("ML "):
        return "Machine Learning"

    if strategy.startswith("HMM "):
        return "HMM"

    if strategy.startswith("RSM "):
        return "RSM"

    if "VRP Proxy" in strategy:
        return "Exploratory Synthetic VRP"

    return "Benchmark"


def merge_bootstrap_results(
    summary: pd.DataFrame,
    bootstrap: pd.DataFrame,
    benchmark: str,
) -> pd.DataFrame:
    columns = [
        "Strategy",
        "Gamma",
        "Delta MV CEQ Ann.",
        "Delta MV CEQ CI Low",
        "Delta MV CEQ CI High",
        "Delta MV CEQ Positive",
        "Delta CRRA CE Ann.",
        "Delta CRRA CE CI Low",
        "Delta CRRA CE CI High",
        "Delta CRRA CE Positive",
        "Bootstrap P(Delta MV <= 0)",
        "Bootstrap P(Delta CRRA <= 0)",
    ]

    selected = bootstrap[
        columns
    ].copy()

    selected = selected.rename(
        columns={
            column: f"{column} vs {benchmark}"
            for column in selected.columns
            if column not in {
                "Strategy",
                "Gamma",
            }
        }
    )

    result = summary.merge(
        selected,
        on=[
            "Strategy",
            "Gamma",
        ],
        how="left",
    )

    result[
        f"Fee Eq. bps vs {benchmark}"
    ] = (
        10_000.0
        * result[
            f"Delta MV CEQ Ann. vs {benchmark}"
        ]
    )

    result[
        f"CRRA Fee Eq. bps vs {benchmark}"
    ] = (
        10_000.0
        * result[
            f"Delta CRRA CE Ann. vs {benchmark}"
        ]
    )

    return result


def run_market(
    market: str,
) -> pd.DataFrame:
    returns_path = (
        TABLES_DIR
        / f"{market}_ml_vs_core_returns.csv"
    )

    returns = read_return_panel(
        returns_path
    )

    required = {
        "60/40",
        "1/N Equity-Bond",
    }

    missing = sorted(
        required.difference(
            returns.columns
        )
    )

    if missing:
        raise KeyError(
            f"{market.upper()} missing "
            f"benchmarks: {missing}"
        )

    summary = build_welfare_summary(
        returns=returns,
        gammas=GAMMAS,
    )

    for benchmark in BENCHMARKS:
        bootstrap = (
            bootstrap_welfare_differences(
                returns=returns,
                benchmark=benchmark,
                gammas=GAMMAS,
                n_bootstrap=N_BOOTSTRAP,
                block_length=BLOCK_LENGTH,
                seed=SEED,
            )
        )

        summary = merge_bootstrap_results(
            summary=summary,
            bootstrap=bootstrap,
            benchmark=benchmark,
        )

    summary.insert(
        0,
        "Market",
        market.upper(),
    )

    summary.insert(
        2,
        "Model Group",
        summary["Strategy"].map(
            identify_model_group
        ),
    )

    summary = summary.sort_values(
        [
            "Gamma",
            "MV CEQ Ann.",
        ],
        ascending=[
            True,
            False,
        ],
    ).reset_index(
        drop=True
    )

    output_path = (
        TABLES_DIR
        / f"{market}_ml_welfare_summary.csv"
    )

    summary.to_csv(
        output_path,
        index=False,
    )

    gamma_five = summary.loc[
        summary["Gamma"].eq(5.0)
    ].copy()

    implementable = gamma_five.loc[
        gamma_five[
            "Model Group"
        ].ne(
            "Exploratory Synthetic VRP"
        )
    ]

    display_columns = [
        "Strategy",
        "Model Group",
        "MV CEQ Ann.",
        "CRRA CE Ann.",
        "Fee Eq. bps vs 60/40",
        "Fee Eq. bps vs 1/N Equity-Bond",
        "Delta MV CEQ CI Low vs 60/40",
        "Delta MV CEQ CI High vs 60/40",
        (
            "Delta MV CEQ CI Low "
            "vs 1/N Equity-Bond"
        ),
        (
            "Delta MV CEQ CI High "
            "vs 1/N Equity-Bond"
        ),
    ]

    print("=" * 120)
    print(
        f"{market.upper()} — "
        "ML WELFARE EXTENSION"
    )
    print("=" * 120)

    print(
        f"Observations: {len(returns)}"
    )

    print(
        "Sample: "
        f"{returns.index.min().date()} "
        "-> "
        f"{returns.index.max().date()}"
    )

    print(
        f"Strategies: {len(returns.columns)}"
    )

    print(
        f"Output: {output_path}"
    )

    print()
    print(
        "IMPLEMENTABLE STRATEGIES — "
        "GAMMA = 5"
    )

    print(
        implementable[
            display_columns
        ]
        .sort_values(
            "MV CEQ Ann.",
            ascending=False,
        )
        .to_string(
            index=False
        )
    )

    print()

    return summary


def main() -> None:
    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    summaries = [
        run_market("us"),
        run_market("eu"),
    ]

    combined = pd.concat(
        summaries,
        ignore_index=True,
    )

    combined_path = (
        TABLES_DIR
        / (
            "cross_market_ml_"
            "welfare_comparison.csv"
        )
    )

    combined.to_csv(
        combined_path,
        index=False,
    )

    selected = combined.loc[
        combined["Model Group"].ne(
            "Exploratory Synthetic VRP"
        )
    ].copy()

    selected_path = (
        TABLES_DIR
        / (
            "cross_market_ml_"
            "welfare_implementable.csv"
        )
    )

    selected.to_csv(
        selected_path,
        index=False,
    )

    print("=" * 120)
    print(
        "MVP 6 ML WELFARE "
        "EXTENSION COMPLETE"
    )
    print("=" * 120)

    print(
        f"Full comparison: {combined_path}"
    )

    print(
        f"Implementable comparison: "
        f"{selected_path}"
    )

    print(
        f"Risk-aversion levels: {GAMMAS}"
    )

    print(
        f"Bootstrap replications: "
        f"{N_BOOTSTRAP}"
    )

    print(
        f"Moving-block length: "
        f"{BLOCK_LENGTH} months"
    )


if __name__ == "__main__":
    main()
