from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.config import OUTPUT_TABLES_DIR


METRIC_COLUMNS = [
    "Ann. Return",
    "Ann. Vol",
    "Sharpe",
    "Sortino",
    "Max Drawdown",
    "Calmar",
    "VaR 95",
    "CVaR 95",
    "Avg Turnover",
    "Obs",
]

BENCHMARKS = [
    "Buy-and-Hold Equity",
    "60/40",
    "1/N Equity-Bond",
]

DIRECT_VARIANCE_PREFIX = (
    "Direct Short Variance"
)

DIRECT_VARIANCE_WELFARE_COLUMNS = [
    "Market",
    "Strategy",
    "Model Group",
    "Gamma",
    "Obs",
    "Start",
    "End",
    "MV CEQ Ann.",
    "CRRA CE Ann.",
    "Delta MV CEQ Ann. vs 60/40",
    "Delta MV CEQ CI Low vs 60/40",
    "Delta MV CEQ CI High vs 60/40",
    "Bootstrap P(Delta MV <= 0) vs 60/40",
    "Fee Eq. bps vs 60/40",
    (
        "Delta MV CEQ Ann. "
        "vs 1/N Equity-Bond"
    ),
    (
        "Delta MV CEQ CI Low "
        "vs 1/N Equity-Bond"
    ),
    (
        "Delta MV CEQ CI High "
        "vs 1/N Equity-Bond"
    ),
    (
        "Bootstrap P(Delta MV <= 0) "
        "vs 1/N Equity-Bond"
    ),
    (
        "Fee Eq. bps "
        "vs 1/N Equity-Bond"
    ),
]


def require_file(
    path: Path,
) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )


def normalize_strategy_column(
    frame: pd.DataFrame,
) -> pd.DataFrame:
    result = frame.copy()

    if "Strategy" in result.columns:
        return result

    unnamed_columns = [
        column
        for column in result.columns
        if str(column).startswith(
            "Unnamed:"
        )
    ]

    if unnamed_columns:
        return result.rename(
            columns={
                unnamed_columns[0]: (
                    "Strategy"
                )
            }
        )

    first_column = result.columns[0]

    return result.rename(
        columns={
            first_column: "Strategy"
        }
    )


def assign_model_group(
    strategy: str,
) -> str:
    strategy = str(strategy)

    if strategy in BENCHMARKS:
        return "Benchmark"

    if strategy.startswith("HMM "):
        return "HMM"

    if strategy.startswith("RSM "):
        return "RSM"

    if strategy.startswith("ML "):
        return "Machine Learning"

    if strategy.startswith(
        DIRECT_VARIANCE_PREFIX
    ):
        return (
            "Direct Variance Approximation"
        )

    if "VRP Proxy" in strategy:
        return (
            "Exploratory Synthetic VRP"
        )

    return "Other"


def validate_metrics(
    frame: pd.DataFrame,
    path: Path,
) -> None:
    missing = [
        column
        for column in METRIC_COLUMNS
        if column not in frame.columns
    ]

    if missing:
        raise ValueError(
            f"Missing metric columns in "
            f"{path}: {missing}"
        )

    numeric = frame[
        METRIC_COLUMNS
    ].select_dtypes(
        include=[np.number]
    )

    if not np.isfinite(
        numeric.to_numpy()
    ).all():
        raise ValueError(
            f"Non-finite metric values "
            f"in {path}"
        )


def load_indexed_performance(
    path: Path,
    market: str,
) -> pd.DataFrame:
    require_file(path)

    frame = pd.read_csv(
        path,
        index_col=0,
    )

    validate_metrics(
        frame,
        path,
    )

    frame = frame[
        METRIC_COLUMNS
    ].copy()

    frame.insert(
        0,
        "Strategy",
        frame.index.astype(str),
    )

    frame.insert(
        0,
        "Market",
        market.upper(),
    )

    frame["Model Group"] = (
        frame["Strategy"].map(
            assign_model_group
        )
    )

    return frame.reset_index(
        drop=True
    )


def load_allocation_summary(
    market: str,
) -> pd.DataFrame:
    path = (
        OUTPUT_TABLES_DIR
        / (
            f"{market}_final_"
            "implementable_summary.csv"
        )
    )

    return load_indexed_performance(
        path=path,
        market=market,
    )


def load_extended_summary(
    market: str,
) -> pd.DataFrame:
    path = (
        OUTPUT_TABLES_DIR
        / (
            f"{market}_final_extended_"
            "summary_with_synthetic_vrp.csv"
        )
    )

    return load_indexed_performance(
        path=path,
        market=market,
    )


def load_ml_summary(
    market: str,
) -> pd.DataFrame:
    path = (
        OUTPUT_TABLES_DIR
        / (
            f"{market}_ml_vs_core_"
            "performance_summary.csv"
        )
    )

    if not path.exists():
        print(
            "Warning: optional ML summary "
            f"not found: {path}"
        )

        return pd.DataFrame()

    frame = pd.read_csv(path)

    frame = normalize_strategy_column(
        frame
    )

    missing = [
        column
        for column in METRIC_COLUMNS
        if column not in frame.columns
    ]

    if missing:
        raise ValueError(
            f"Missing ML metrics in "
            f"{path}: {missing}"
        )

    frame = frame.loc[
        frame["Strategy"]
        .astype(str)
        .str.startswith("ML ")
    ].copy()

    frame.insert(
        0,
        "Market",
        market.upper(),
    )

    frame["Model Group"] = (
        "Machine Learning"
    )

    return frame[
        [
            "Market",
            "Strategy",
            "Model Group",
            *METRIC_COLUMNS,
        ]
    ].reset_index(
        drop=True
    )


def load_direct_variance_performance(
) -> pd.DataFrame:
    path = (
        OUTPUT_TABLES_DIR
        / (
            "cross_market_direct_variance_"
            "performance.csv"
        )
    )

    require_file(path)

    frame = pd.read_csv(path)

    required = [
        "Market",
        "Strategy",
        "Model Group",
        *METRIC_COLUMNS,
    ]

    missing = [
        column
        for column in required
        if column not in frame.columns
    ]

    if missing:
        raise ValueError(
            "Missing direct-variance "
            f"columns in {path}: {missing}"
        )

    numeric = frame[
        METRIC_COLUMNS
    ].select_dtypes(
        include=[np.number]
    )

    if not np.isfinite(
        numeric.to_numpy()
    ).all():
        raise ValueError(
            "Non-finite direct-variance "
            f"metrics in {path}"
        )

    return frame[
        required
    ].copy()


def load_direct_variance_welfare(
) -> pd.DataFrame:
    path = (
        OUTPUT_TABLES_DIR
        / (
            "cross_market_direct_variance_"
            "welfare_implementable.csv"
        )
    )

    require_file(path)

    frame = pd.read_csv(path)

    missing = [
        column
        for column
        in DIRECT_VARIANCE_WELFARE_COLUMNS
        if column not in frame.columns
    ]

    if missing:
        raise ValueError(
            "Missing direct-variance "
            f"welfare columns: {missing}"
        )

    frame = frame.loc[
        frame["Gamma"].eq(5.0)
    ].copy()

    frame[
        "Statistically Superior vs 60/40"
    ] = (
        frame[
            "Delta MV CEQ CI Low vs 60/40"
        ]
        > 0.0
    )

    frame[
        (
            "Statistically Superior "
            "vs 1/N Equity-Bond"
        )
    ] = (
        frame[
            (
                "Delta MV CEQ CI Low "
                "vs 1/N Equity-Bond"
            )
        ]
        > 0.0
    )

    return frame


def best_row(
    frame: pd.DataFrame,
    metric: str,
) -> pd.Series | None:
    if frame.empty:
        return None

    valid = frame.dropna(
        subset=[metric]
    )

    if valid.empty:
        return None

    return valid.sort_values(
        metric,
        ascending=False,
    ).iloc[0]


def append_unique_row(
    rows: list[dict],
    row: pd.Series | None,
    role: str,
    seen: set[tuple[str, str]],
) -> None:
    if row is None:
        return

    key = (
        str(row["Market"]),
        str(row["Strategy"]),
    )

    if key in seen:
        return

    payload = row.to_dict()
    payload["Selection Role"] = role

    rows.append(payload)
    seen.add(key)


def build_allocation_key_comparison(
    allocation: pd.DataFrame,
    ml: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[dict] = []
    seen: set[tuple[str, str]] = set()

    for market in ("US", "EU"):
        market_allocation = allocation.loc[
            allocation["Market"].eq(
                market
            )
        ]

        for benchmark in BENCHMARKS:
            candidate = market_allocation.loc[
                market_allocation[
                    "Strategy"
                ].eq(
                    benchmark
                )
            ]

            row = (
                candidate.iloc[0]
                if not candidate.empty
                else None
            )

            append_unique_row(
                rows=rows,
                row=row,
                role="Benchmark",
                seen=seen,
            )

        for model_group in (
            "HMM",
            "RSM",
        ):
            candidates = (
                market_allocation.loc[
                    market_allocation[
                        "Model Group"
                    ].eq(
                        model_group
                    )
                ]
            )

            append_unique_row(
                rows=rows,
                row=best_row(
                    candidates,
                    "Sharpe",
                ),
                role=(
                    f"Best {model_group} "
                    "by Sharpe"
                ),
                seen=seen,
            )

        if not ml.empty:
            candidates = ml.loc[
                ml["Market"].eq(
                    market
                )
            ]

            append_unique_row(
                rows=rows,
                row=best_row(
                    candidates,
                    "Sharpe",
                ),
                role=(
                    "Best Machine Learning "
                    "by Sharpe"
                ),
                seen=seen,
            )

    result = pd.DataFrame(rows)

    ordered_columns = [
        "Market",
        "Model Group",
        "Selection Role",
        "Strategy",
        *METRIC_COLUMNS,
    ]

    return result[
        ordered_columns
    ]


def build_allocation_leaders(
    allocation: pd.DataFrame,
    ml: pd.DataFrame,
) -> pd.DataFrame:
    combined = pd.concat(
        [
            allocation,
            ml,
        ],
        ignore_index=True,
    )

    rows = []

    for market in ("US", "EU"):
        market_frame = combined.loc[
            combined["Market"].eq(
                market
            )
        ].copy()

        benchmark_frame = (
            market_frame.loc[
                market_frame[
                    "Model Group"
                ].eq(
                    "Benchmark"
                )
            ]
        )

        dynamic_frame = (
            market_frame.loc[
                market_frame[
                    "Model Group"
                ].isin(
                    [
                        "HMM",
                        "RSM",
                        "Machine Learning",
                    ]
                )
            ]
        )

        criteria = [
            (
                "Best benchmark Sharpe",
                best_row(
                    benchmark_frame,
                    "Sharpe",
                ),
            ),
            (
                "Best dynamic-model Sharpe",
                best_row(
                    dynamic_frame,
                    "Sharpe",
                ),
            ),
            (
                "Best dynamic-model drawdown",
                best_row(
                    dynamic_frame,
                    "Max Drawdown",
                ),
            ),
        ]

        for criterion, row in criteria:
            if row is None:
                continue

            rows.append(
                {
                    "Market": market,
                    "Criterion": criterion,
                    "Model Group": (
                        row["Model Group"]
                    ),
                    "Strategy": (
                        row["Strategy"]
                    ),
                    "Ann. Return": (
                        row["Ann. Return"]
                    ),
                    "Ann. Vol": (
                        row["Ann. Vol"]
                    ),
                    "Sharpe": row["Sharpe"],
                    "Sortino": row["Sortino"],
                    "Max Drawdown": (
                        row["Max Drawdown"]
                    ),
                    "CVaR 95": (
                        row["CVaR 95"]
                    ),
                    "Avg Turnover": (
                        row["Avg Turnover"]
                    ),
                    "Obs": row["Obs"],
                }
            )

    return pd.DataFrame(rows)


def build_direct_variance_key_comparison(
    performance: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for market in ("US", "EU"):
        market_frame = performance.loc[
            performance["Market"].eq(
                market
            )
        ].copy()

        selected_direct = best_row(
            market_frame.loc[
                market_frame[
                    "Strategy"
                ]
                .astype(str)
                .str.startswith(
                    DIRECT_VARIANCE_PREFIX
                )
            ],
            "Sharpe",
        )

        selected_name = (
            None
            if selected_direct is None
            else str(
                selected_direct[
                    "Strategy"
                ]
            )
        )

        include = market_frame.loc[
            (
                market_frame[
                    "Strategy"
                ].isin(BENCHMARKS)
            )
            |
            (
                market_frame[
                    "Strategy"
                ]
                .astype(str)
                .str.startswith(
                    DIRECT_VARIANCE_PREFIX
                )
            )
        ].copy()

        include[
            "Selection Role"
        ] = np.where(
            include["Strategy"].eq(
                selected_name
            ),
            (
                "Selected direct-variance "
                "specification"
            ),
            np.where(
                include[
                    "Model Group"
                ].eq(
                    "Benchmark"
                ),
                "Benchmark",
                (
                    "Alternative direct-variance "
                    "specification"
                ),
            ),
        )

        include = include.sort_values(
            [
                "Model Group",
                "Sharpe",
            ],
            ascending=[
                True,
                False,
            ],
        )

        rows.append(include)

    result = pd.concat(
        rows,
        ignore_index=True,
    )

    return result[
        [
            "Market",
            "Model Group",
            "Selection Role",
            "Strategy",
            *METRIC_COLUMNS,
        ]
    ]


def build_direct_variance_welfare_table(
    welfare: pd.DataFrame,
) -> pd.DataFrame:
    include = welfare.loc[
        (
            welfare[
                "Model Group"
            ].eq(
                "Direct Variance Approximation"
            )
        )
        |
        (
            welfare[
                "Strategy"
            ].isin(
                [
                    "60/40",
                    "1/N Equity-Bond",
                ]
            )
        )
    ].copy()

    columns = [
        "Market",
        "Strategy",
        "Model Group",
        "Gamma",
        "Obs",
        "Start",
        "End",
        "MV CEQ Ann.",
        "CRRA CE Ann.",
        "Delta MV CEQ Ann. vs 60/40",
        "Delta MV CEQ CI Low vs 60/40",
        "Delta MV CEQ CI High vs 60/40",
        "Bootstrap P(Delta MV <= 0) vs 60/40",
        "Fee Eq. bps vs 60/40",
        (
            "Delta MV CEQ Ann. "
            "vs 1/N Equity-Bond"
        ),
        (
            "Delta MV CEQ CI Low "
            "vs 1/N Equity-Bond"
        ),
        (
            "Delta MV CEQ CI High "
            "vs 1/N Equity-Bond"
        ),
        (
            "Bootstrap P(Delta MV <= 0) "
            "vs 1/N Equity-Bond"
        ),
        (
            "Fee Eq. bps "
            "vs 1/N Equity-Bond"
        ),
        (
            "Statistically Superior "
            "vs 60/40"
        ),
        (
            "Statistically Superior "
            "vs 1/N Equity-Bond"
        ),
    ]

    return include[
        columns
    ].sort_values(
        [
            "Market",
            "MV CEQ Ann.",
        ],
        ascending=[
            True,
            False,
        ],
    )


def build_synthetic_vrp_comparison(
    performance: pd.DataFrame,
) -> pd.DataFrame:
    result = performance.loc[
        performance[
            "Strategy"
        ].isin(
            [
                "Pure VRP Proxy",
                "Synthetic Pure VRP Proxy",
            ]
        )
    ].copy()

    result[
        "Interpretation"
    ] = (
        "Exploratory synthetic log-VRP "
        "proxy; not a traded variance-swap "
        "return and not an implementable "
        "standalone strategy."
    )

    return result[
        [
            "Market",
            "Strategy",
            "Model Group",
            *METRIC_COLUMNS,
            "Interpretation",
        ]
    ]


def build_model_family_leaders(
    allocation: pd.DataFrame,
    ml: pd.DataFrame,
    direct: pd.DataFrame,
) -> pd.DataFrame:
    direct_implementable = direct.loc[
        direct[
            "Model Group"
        ].ne(
            "Synthetic Log-VRP Proxy"
        )
    ].copy()

    combined = pd.concat(
        [
            allocation,
            ml,
            direct_implementable,
        ],
        ignore_index=True,
    )

    combined = combined.loc[
        combined[
            "Model Group"
        ].isin(
            [
                "Benchmark",
                "HMM",
                "RSM",
                "Machine Learning",
                (
                    "Direct Variance "
                    "Approximation"
                ),
            ]
        )
    ].copy()

    rows = []

    for (
        market,
        model_group,
    ), subframe in combined.groupby(
        [
            "Market",
            "Model Group",
        ]
    ):
        row = best_row(
            subframe,
            "Sharpe",
        )

        if row is None:
            continue

        payload = row.to_dict()

        payload[
            "Comparability Warning"
        ] = (
            "Performance is ranked only "
            "within its evidence layer. "
            "Allocation and direct-variance "
            "samples may have different "
            "start dates."
        )

        rows.append(payload)

    result = pd.DataFrame(rows)

    return result[
        [
            "Market",
            "Model Group",
            "Strategy",
            *METRIC_COLUMNS,
            "Comparability Warning",
        ]
    ].sort_values(
        [
            "Market",
            "Model Group",
        ]
    )


def format_percent(
    value: float,
) -> str:
    return f"{100.0 * value:.2f}%"


def format_ratio(
    value: float,
) -> str:
    return f"{value:.3f}"


def build_empirical_conclusions(
    allocation: pd.DataFrame,
    ml: pd.DataFrame,
    direct: pd.DataFrame,
    welfare: pd.DataFrame,
) -> pd.DataFrame:
    rows = []

    for market in ("US", "EU"):
        allocation_market = (
            allocation.loc[
                allocation[
                    "Market"
                ].eq(
                    market
                )
            ]
        )

        benchmark = best_row(
            allocation_market.loc[
                allocation_market[
                    "Model Group"
                ].eq(
                    "Benchmark"
                )
            ],
            "Sharpe",
        )

        dynamic = best_row(
            allocation_market.loc[
                allocation_market[
                    "Model Group"
                ].isin(
                    [
                        "HMM",
                        "RSM",
                    ]
                )
            ],
            "Sharpe",
        )

        if (
            benchmark is not None
            and dynamic is not None
        ):
            rows.append(
                {
                    "Theme": (
                        f"{market} "
                        "regime-allocation evidence"
                    ),
                    "Evidence Layer": (
                        "Equity-Bond Allocation"
                    ),
                    "Conclusion": (
                        f"The best HMM/RSM "
                        f"specification is "
                        f"{dynamic['Strategy']} "
                        f"with a Sharpe ratio of "
                        f"{format_ratio(dynamic['Sharpe'])}, "
                        f"compared with "
                        f"{format_ratio(benchmark['Sharpe'])} "
                        f"for the strongest benchmark "
                        f"({benchmark['Strategy']}). "
                        "The regime-switching layer "
                        "does not establish robust "
                        "benchmark dominance."
                    ),
                }
            )

        if not ml.empty:
            ml_market = ml.loc[
                ml["Market"].eq(
                    market
                )
            ]

            best_ml = best_row(
                ml_market,
                "Sharpe",
            )

            if best_ml is not None:
                rows.append(
                    {
                        "Theme": (
                            f"{market} "
                            "machine-learning evidence"
                        ),
                        "Evidence Layer": (
                            "Stress Classification "
                            "and Equity-Bond Allocation"
                        ),
                        "Conclusion": (
                            f"The strongest ML strategy "
                            f"is {best_ml['Strategy']} "
                            f"with a Sharpe ratio of "
                            f"{format_ratio(best_ml['Sharpe'])}. "
                            "Predictive improvements do "
                            "not by themselves imply "
                            "statistically significant "
                            "economic gains relative to "
                            "simple allocation benchmarks."
                        ),
                    }
                )

        direct_market = direct.loc[
            direct["Market"].eq(
                market
            )
        ]

        best_direct = best_row(
            direct_market.loc[
                direct_market[
                    "Strategy"
                ]
                .astype(str)
                .str.startswith(
                    DIRECT_VARIANCE_PREFIX
                )
            ],
            "Sharpe",
        )

        welfare_market = welfare.loc[
            (
                welfare[
                    "Market"
                ].eq(
                    market
                )
            )
            &
            (
                welfare[
                    "Model Group"
                ].eq(
                    (
                        "Direct Variance "
                        "Approximation"
                    )
                )
            )
        ]

        best_welfare = best_row(
            welfare_market,
            "MV CEQ Ann.",
        )

        if (
            best_direct is not None
            and best_welfare is not None
        ):
            superior_6040 = bool(
                best_welfare[
                    (
                        "Statistically Superior "
                        "vs 60/40"
                    )
                ]
            )

            superior_1n = bool(
                best_welfare[
                    (
                        "Statistically Superior "
                        "vs 1/N Equity-Bond"
                    )
                ]
            )

            if (
                superior_6040
                and superior_1n
            ):
                welfare_statement = (
                    "Its gamma-five MV CEQ "
                    "advantage is statistically "
                    "positive relative to both "
                    "60/40 and 1/N."
                )
            else:
                welfare_statement = (
                    "Its gamma-five welfare "
                    "comparison does not establish "
                    "statistically significant "
                    "dominance over both 60/40 "
                    "and 1/N."
                )

            rows.append(
                {
                    "Theme": (
                        f"{market} direct-variance "
                        "evidence"
                    ),
                    "Evidence Layer": (
                        "Model-Based Direct "
                        "Variance Carry Approximation"
                    ),
                    "Conclusion": (
                        f"The highest-Sharpe direct "
                        f"specification is "
                        f"{best_direct['Strategy']} "
                        f"with annualized return "
                        f"{format_percent(best_direct['Ann. Return'])}, "
                        f"volatility "
                        f"{format_percent(best_direct['Ann. Vol'])}, "
                        f"Sharpe "
                        f"{format_ratio(best_direct['Sharpe'])} "
                        f"and maximum drawdown "
                        f"{format_percent(best_direct['Max Drawdown'])}. "
                        f"{welfare_statement}"
                    ),
                }
            )

    rows.extend(
        [
            {
                "Theme": (
                    "Cross-market main result"
                ),
                "Evidence Layer": (
                    "Integrated Interpretation"
                ),
                "Conclusion": (
                    "The economic value of the "
                    "variance risk premium depends "
                    "critically on the payoff "
                    "structure through which it is "
                    "harvested. Adding VRP variables "
                    "to HMM, RSM or ML allocation "
                    "models produces limited and "
                    "model-dependent gains, whereas "
                    "the direct variance-payoff "
                    "approximation generates much "
                    "stronger European evidence."
                ),
            },
            {
                "Theme": (
                    "US versus Europe"
                ),
                "Evidence Layer": (
                    "Cross-Market Comparison"
                ),
                "Conclusion": (
                    "The selected US direct-variance "
                    "strategy improves risk-adjusted "
                    "performance but does not robustly "
                    "dominate traditional portfolios "
                    "in welfare terms. In Europe, the "
                    "VRP-positive direct strategy "
                    "produces economically large and "
                    "bootstrap-significant welfare "
                    "gains in the tested sample."
                ),
            },
            {
                "Theme": (
                    "Synthetic proxy"
                ),
                "Evidence Layer": (
                    "Exploratory Diagnostic"
                ),
                "Conclusion": (
                    "The Pure VRP Proxy remains an "
                    "exploratory synthetic log-VRP "
                    "series. Its performance must not "
                    "be interpreted as a tradable "
                    "variance-swap return or compared "
                    "without qualification with "
                    "implementable strategies."
                ),
            },
            {
                "Theme": (
                    "Implementation limitation"
                ),
                "Evidence Layer": (
                    "Methodological Boundary"
                ),
                "Conclusion": (
                    "The direct-variance extension is "
                    "a model-based carry approximation "
                    "using lagged implied variance, "
                    "realized-variance settlement "
                    "proxies, lagged risk targeting "
                    "and stylized monthly roll costs. "
                    "It does not reconstruct an exact "
                    "variance-swap strike, collateral "
                    "process, bid-ask spread, margin "
                    "path or daily mark-to-market."
                ),
            },
        ]
    )

    return pd.DataFrame(rows)


def print_table(
    title: str,
    frame: pd.DataFrame,
) -> None:
    print()
    print("=" * 125)
    print(title)
    print("=" * 125)

    if frame.empty:
        print("No rows available.")
        return

    print(
        frame.round(4).to_string(
            index=False
        )
    )


def run_cross_market_report() -> None:
    us_allocation = load_allocation_summary(
        "us"
    )

    eu_allocation = load_allocation_summary(
        "eu"
    )

    allocation = pd.concat(
        [
            us_allocation,
            eu_allocation,
        ],
        ignore_index=True,
    )

    us_extended = load_extended_summary(
        "us"
    )

    eu_extended = load_extended_summary(
        "eu"
    )

    extended = pd.concat(
        [
            us_extended,
            eu_extended,
        ],
        ignore_index=True,
    )

    us_ml = load_ml_summary("us")
    eu_ml = load_ml_summary("eu")

    ml = pd.concat(
        [
            us_ml,
            eu_ml,
        ],
        ignore_index=True,
    )

    direct = (
        load_direct_variance_performance()
    )

    welfare = (
        load_direct_variance_welfare()
    )

    allocation_key = (
        build_allocation_key_comparison(
            allocation=allocation,
            ml=ml,
        )
    )

    allocation_leaders = (
        build_allocation_leaders(
            allocation=allocation,
            ml=ml,
        )
    )

    direct_key = (
        build_direct_variance_key_comparison(
            performance=direct,
        )
    )

    direct_welfare = (
        build_direct_variance_welfare_table(
            welfare=welfare,
        )
    )

    synthetic_comparison = (
        build_synthetic_vrp_comparison(
            performance=direct,
        )
    )

    family_leaders = (
        build_model_family_leaders(
            allocation=allocation,
            ml=ml,
            direct=direct,
        )
    )

    conclusions = (
        build_empirical_conclusions(
            allocation=allocation,
            ml=ml,
            direct=direct,
            welfare=welfare,
        )
    )

    output_frames = {
        (
            "cross_market_"
            "implementable_summary.csv"
        ): allocation,
        (
            "cross_market_"
            "key_strategy_comparison.csv"
        ): allocation_key,
        (
            "cross_market_leaders.csv"
        ): allocation_leaders,
        (
            "cross_market_direct_variance_"
            "key_comparison.csv"
        ): direct_key,
        (
            "cross_market_direct_variance_"
            "welfare_gamma5.csv"
        ): direct_welfare,
        (
            "cross_market_synthetic_"
            "vrp_comparison.csv"
        ): synthetic_comparison,
        (
            "cross_market_model_"
            "family_leaders.csv"
        ): family_leaders,
        (
            "cross_market_empirical_"
            "conclusions.csv"
        ): conclusions,
    }

    for filename, frame in (
        output_frames.items()
    ):
        path = (
            OUTPUT_TABLES_DIR
            / filename
        )

        frame.to_csv(
            path,
            index=False,
        )

        print(
            f"Saved: {path}"
        )

    pd.set_option(
        "display.max_columns",
        None,
    )

    pd.set_option(
        "display.width",
        300,
    )

    pd.set_option(
        "display.max_colwidth",
        220,
    )

    print_table(
        title=(
            "CROSS-MARKET — "
            "ALLOCATION KEY STRATEGIES"
        ),
        frame=allocation_key,
    )

    print_table(
        title=(
            "CROSS-MARKET — "
            "DIRECT VARIANCE KEY COMPARISON"
        ),
        frame=direct_key,
    )

    print_table(
        title=(
            "CROSS-MARKET — "
            "DIRECT VARIANCE WELFARE "
            "AT GAMMA = 5"
        ),
        frame=direct_welfare,
    )

    print_table(
        title=(
            "CROSS-MARKET — "
            "MODEL-FAMILY LEADERS"
        ),
        frame=family_leaders,
    )

    print()
    print("=" * 125)
    print(
        "CROSS-MARKET — "
        "EMPIRICAL CONCLUSIONS"
    )
    print("=" * 125)

    print(
        conclusions.to_string(
            index=False
        )
    )

    stale_phrases = [
        "collapses in Europe",
        (
            "more useful as a "
            "regime-state variable"
        ),
    ]

    conclusion_text = " ".join(
        conclusions[
            "Conclusion"
        ].astype(str)
    )

    for phrase in stale_phrases:
        if phrase.lower() in (
            conclusion_text.lower()
        ):
            raise AssertionError(
                "Stale conclusion remains: "
                f"{phrase}"
            )

    print()
    print("=" * 125)
    print(
        "FINAL CROSS-MARKET REPORT "
        "COMPLETE"
    )
    print("=" * 125)


if __name__ == "__main__":
    run_cross_market_report()
