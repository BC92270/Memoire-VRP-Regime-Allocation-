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

N_BOOTSTRAP = 2000
BLOCK_LENGTH = 6
SEED = 20260802


def read_returns(
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

    frame.columns = [
        str(column).strip()
        for column in frame.columns
    ]

    return frame


def load_market_panel(
    market: str,
) -> pd.DataFrame:
    """
    Load the final implementable model set.

    The synthetic direct-VRP proxy is added from
    the core comparison when it is absent from
    the final implementable return file.
    """
    final_path = (
        TABLES_DIR
        / f"{market}_final_model_returns.csv"
    )

    core_path = (
        TABLES_DIR
        / f"{market}_core_model_returns.csv"
    )

    final_returns = read_returns(
        final_path
    )

    core_returns = read_returns(
        core_path
    )

    rename_map = {
        "Pure VRP Proxy": (
            "Synthetic Pure VRP Proxy"
        )
    }

    final_returns = (
        final_returns.rename(
            columns=rename_map
        )
    )

    core_returns = (
        core_returns.rename(
            columns=rename_map
        )
    )

    if (
        "Synthetic Pure VRP Proxy"
        not in final_returns.columns
        and
        "Synthetic Pure VRP Proxy"
        in core_returns.columns
    ):
        final_returns[
            "Synthetic Pure VRP Proxy"
        ] = core_returns[
            "Synthetic Pure VRP Proxy"
        ]

    required_columns = {
        "60/40",
        "1/N Equity-Bond",
        "Synthetic Pure VRP Proxy",
    }

    missing_columns = (
        required_columns.difference(
            final_returns.columns
        )
    )

    if missing_columns:
        raise KeyError(
            f"{market.upper()} "
            f"missing columns: "
            f"{sorted(missing_columns)}"
        )

    panel = clean_return_panel(
        final_returns
    )

    if len(panel) < 36:
        raise ValueError(
            f"{market.upper()} has only "
            f"{len(panel)} common observations."
        )

    return panel


def merge_benchmark_results(
    summary: pd.DataFrame,
    bootstrap: pd.DataFrame,
    benchmark: str,
) -> pd.DataFrame:
    metrics = [
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
        metrics
    ].copy()

    selected = selected.rename(
        columns={
            column: (
                f"{column} vs {benchmark}"
            )
            for column
            in selected.columns
            if column
            not in {
                "Strategy",
                "Gamma",
            }
        }
    )

    merged = summary.merge(
        selected,
        on=[
            "Strategy",
            "Gamma",
        ],
        how="left",
    )

    merged[
        f"Fee Eq. bps vs {benchmark}"
    ] = (
        10000.0
        * merged[
            f"Delta MV CEQ Ann. "
            f"vs {benchmark}"
        ]
    )

    merged[
        f"CRRA Fee Eq. bps vs {benchmark}"
    ] = (
        10000.0
        * merged[
            f"Delta CRRA CE Ann. "
            f"vs {benchmark}"
        ]
    )

    return merged


def run_market(
    market: str,
) -> pd.DataFrame:
    returns = load_market_panel(
        market
    )

    aligned_path = (
        TABLES_DIR
        / f"{market}_welfare_aligned_returns.csv"
    )

    returns.to_csv(
        aligned_path,
        index_label="Date",
    )

    summary = build_welfare_summary(
        returns=returns,
        gammas=GAMMAS,
    )

    for benchmark in (
        "60/40",
        "1/N Equity-Bond",
    ):
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

        summary = (
            merge_benchmark_results(
                summary=summary,
                bootstrap=bootstrap,
                benchmark=benchmark,
            )
        )

    summary.insert(
        0,
        "Market",
        market.upper(),
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
        / f"{market}_welfare_summary.csv"
    )

    summary.to_csv(
        output_path,
        index=False,
    )

    print("=" * 100)
    print(
        f"{market.upper()} "
        "WELFARE ANALYSIS"
    )
    print("=" * 100)

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
        f"Strategies: "
        f"{len(returns.columns)}"
    )

    print(
        f"Aligned returns: "
        f"{aligned_path}"
    )

    print(
        f"Summary: "
        f"{output_path}"
    )

    print()

    gamma_five = summary.loc[
        summary["Gamma"].eq(5.0),
        [
            "Strategy",
            "MV CEQ Ann.",
            "CRRA CE Ann.",
            "Fee Eq. bps vs 60/40",
            (
                "Fee Eq. bps vs "
                "1/N Equity-Bond"
            ),
        ],
    ]

    print(
        gamma_five.to_string(
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

    us_summary = run_market("us")
    eu_summary = run_market("eu")

    combined = pd.concat(
        [
            us_summary,
            eu_summary,
        ],
        ignore_index=True,
    )

    combined_path = (
        TABLES_DIR
        / "cross_market_welfare_comparison.csv"
    )

    combined.to_csv(
        combined_path,
        index=False,
    )

    print("=" * 100)
    print(
        "MVP 5 WELFARE ANALYSIS COMPLETE"
    )
    print("=" * 100)

    print(
        f"Combined output: "
        f"{combined_path}"
    )

    print(
        f"Risk-aversion levels: "
        f"{GAMMAS}"
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
