from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from src.direct_variance import (
    DEFAULT_STRATEGY_SPECS,
    DirectVarianceConfig,
    build_direct_variance_strategy_set,
)
from src.performance_metrics import (
    summarize_strategies,
)
from src.welfare import (
    build_welfare_summary,
    clean_return_panel,
)


PROCESSED_DIR = Path("data/processed")
TABLES_DIR = Path("outputs/tables")

GAMMAS = (
    1.0,
    3.0,
    5.0,
    10.0,
)

KEY_STRATEGIES = {
    "us": (
        "Direct Short Variance "
        "10% Vol (High VRP)"
    ),
    "eu": (
        "Direct Short Variance "
        "10% Vol (VRP > 0)"
    ),
}

COST_GRID_BPS = (
    0.0,
    10.0,
    25.0,
    50.0,
)

LOOKBACK_GRID = {
    12: 12,
    24: 18,
    36: 24,
    60: 36,
}

NOTIONAL_CAP_GRID = (
    0.05,
    0.10,
    0.15,
    0.25,
    0.50,
)

CRISIS_WINDOWS = {
    "Global Financial Crisis": (
        "2008-09-01",
        "2009-06-30",
    ),
    "Euro Sovereign Crisis": (
        "2011-07-01",
        "2012-07-31",
    ),
    "Volmageddon": (
        "2018-02-01",
        "2018-03-31",
    ),
    "Covid Shock": (
        "2020-02-01",
        "2020-05-31",
    ),
    "Inflation Rate Shock": (
        "2022-01-01",
        "2022-10-31",
    ),
}


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


def load_benchmarks(
    market: str,
) -> pd.DataFrame:
    returns = read_indexed_csv(
        TABLES_DIR
        / f"{market}_mvp1_strategy_returns.csv"
    )

    required = [
        "Buy-and-Hold Equity",
        "60/40",
        "1/N Equity-Bond",
    ]

    missing = [
        column
        for column in required
        if column not in returns.columns
    ]

    if missing:
        raise KeyError(
            f"{market.upper()} missing "
            f"benchmarks: {missing}"
        )

    return returns[required]


def make_config(
    *,
    lookback: int = 36,
    minimum_observations: int = 24,
    notional_cap: float = 0.25,
    transaction_cost_bps: float = 10.0,
) -> DirectVarianceConfig:
    return DirectVarianceConfig(
        volatility_lookback_months=lookback,
        minimum_volatility_observations=(
            minimum_observations
        ),
        high_vrp_lookback_months=36,
        minimum_vrp_observations=24,
        max_abs_notional=notional_cap,
        transaction_cost_bps=(
            transaction_cost_bps
        ),
    )


def run_configuration(
    monthly: pd.DataFrame,
    config: DirectVarianceConfig,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
]:
    (
        returns,
        turnovers,
        _,
        _,
    ) = build_direct_variance_strategy_set(
        monthly=monthly,
        config=config,
    )

    return (
        returns,
        turnovers,
    )


def common_index(
    frames: list[pd.DataFrame],
) -> pd.DatetimeIndex:
    if not frames:
        return pd.DatetimeIndex([])

    index = frames[0].index

    for frame in frames[1:]:
        index = index.intersection(
            frame.index
        )

    return index.sort_values()


def performance_table(
    returns: pd.DataFrame,
    turnovers: pd.DataFrame,
) -> pd.DataFrame:
    summary = summarize_strategies(
        returns,
        turnovers,
    ).reset_index()

    first_column = summary.columns[0]

    return summary.rename(
        columns={
            first_column: "Strategy"
        }
    )


def welfare_deltas(
    direct_returns: pd.DataFrame,
    benchmarks: pd.DataFrame,
    gamma: float = 5.0,
) -> pd.DataFrame:
    panel = pd.concat(
        [
            benchmarks,
            direct_returns,
        ],
        axis=1,
    )

    panel = clean_return_panel(
        panel
    )

    summary = build_welfare_summary(
        returns=panel,
        gammas=(gamma,),
    )

    benchmark_values = (
        summary.set_index(
            "Strategy"
        )["MV CEQ Ann."]
    )

    rows = []

    for strategy in direct_returns.columns:
        strategy_row = summary.loc[
            summary["Strategy"].eq(
                strategy
            )
        ]

        if strategy_row.empty:
            continue

        ceq = float(
            strategy_row[
                "MV CEQ Ann."
            ].iloc[0]
        )

        crra = float(
            strategy_row[
                "CRRA CE Ann."
            ].iloc[0]
        )

        rows.append(
            {
                "Strategy": strategy,
                "Gamma": gamma,
                "MV CEQ Ann.": ceq,
                "CRRA CE Ann.": crra,
                (
                    "Delta MV CEQ "
                    "vs 60/40"
                ): (
                    ceq
                    - float(
                        benchmark_values[
                            "60/40"
                        ]
                    )
                ),
                (
                    "Delta MV CEQ "
                    "vs 1/N"
                ): (
                    ceq
                    - float(
                        benchmark_values[
                            "1/N Equity-Bond"
                        ]
                    )
                ),
                "Welfare Obs": int(
                    len(panel)
                ),
                "Welfare Start": (
                    panel.index.min()
                ),
                "Welfare End": (
                    panel.index.max()
                ),
            }
        )

    return pd.DataFrame(rows)


def add_target_diagnostics(
    frame: pd.DataFrame,
) -> pd.DataFrame:
    result = frame.copy()

    target_map = {
        strategy: specification[0]
        for (
            strategy,
            specification,
        ) in DEFAULT_STRATEGY_SPECS.items()
    }

    result[
        "Target Ann. Vol"
    ] = result["Strategy"].map(
        target_map
    )

    result[
        "Realized / Target Vol"
    ] = (
        result["Ann. Vol"]
        / result[
            "Target Ann. Vol"
        ]
    )

    return result


def run_parameter_sensitivity(
    market: str,
    monthly: pd.DataFrame,
    benchmarks: pd.DataFrame,
    dimension: str,
    configurations: list[
        tuple[
            str,
            float,
            DirectVarianceConfig,
        ]
    ],
) -> pd.DataFrame:
    results: dict[
        str,
        tuple[
            float,
            pd.DataFrame,
            pd.DataFrame,
        ],
    ] = {}

    return_frames = []

    for (
        label,
        numeric_value,
        config,
    ) in configurations:
        returns, turnovers = (
            run_configuration(
                monthly=monthly,
                config=config,
            )
        )

        results[label] = (
            numeric_value,
            returns,
            turnovers,
        )

        return_frames.append(
            returns
        )

    shared_index = common_index(
        return_frames
    )

    if len(shared_index) < 36:
        raise ValueError(
            f"{market.upper()} {dimension}: "
            "insufficient common sample."
        )

    rows = []

    for (
        label,
        (
            numeric_value,
            returns,
            turnovers,
        ),
    ) in results.items():
        aligned_returns = returns.reindex(
            shared_index
        )

        aligned_turnovers = (
            turnovers.reindex(
                shared_index
            )
        )

        performance = performance_table(
            returns=aligned_returns,
            turnovers=aligned_turnovers,
        )

        welfare = welfare_deltas(
            direct_returns=aligned_returns,
            benchmarks=benchmarks.reindex(
                shared_index
            ),
            gamma=5.0,
        )

        merged = performance.merge(
            welfare,
            on="Strategy",
            how="left",
        )

        merged.insert(
            0,
            "Market",
            market.upper(),
        )

        merged.insert(
            1,
            "Dimension",
            dimension,
        )

        merged.insert(
            2,
            "Parameter Label",
            label,
        )

        merged.insert(
            3,
            "Parameter Value",
            numeric_value,
        )

        merged[
            "Common Obs"
        ] = len(shared_index)

        merged[
            "Common Start"
        ] = shared_index.min()

        merged[
            "Common End"
        ] = shared_index.max()

        rows.append(
            merged
        )

    combined = pd.concat(
        rows,
        ignore_index=True,
    )

    return add_target_diagnostics(
        combined
    )


def run_subperiod_analysis(
    market: str,
    returns: pd.DataFrame,
    turnovers: pd.DataFrame,
    benchmarks: pd.DataFrame,
) -> pd.DataFrame:
    split_position = (
        len(returns) // 2
    )

    split_date = returns.index[
        split_position
    ]

    periods = {
        "Full Sample": (
            returns.index
        ),
        "First Half": (
            returns.index[
                returns.index < split_date
            ]
        ),
        "Second Half": (
            returns.index[
                returns.index >= split_date
            ]
        ),
        "Pre-Covid": (
            returns.index[
                returns.index
                < pd.Timestamp(
                    "2020-01-31"
                )
            ]
        ),
        "Covid and After": (
            returns.index[
                returns.index
                >= pd.Timestamp(
                    "2020-01-31"
                )
            ]
        ),
    }

    rows = []

    for (
        period_name,
        index,
    ) in periods.items():
        if len(index) < 24:
            continue

        period_returns = returns.reindex(
            index
        )

        period_turnovers = (
            turnovers.reindex(index)
        )

        performance = performance_table(
            period_returns,
            period_turnovers,
        )

        welfare = welfare_deltas(
            direct_returns=period_returns,
            benchmarks=benchmarks.reindex(
                index
            ),
            gamma=5.0,
        )

        merged = performance.merge(
            welfare,
            on="Strategy",
            how="left",
        )

        merged.insert(
            0,
            "Market",
            market.upper(),
        )

        merged.insert(
            1,
            "Period",
            period_name,
        )

        merged[
            "Period Obs"
        ] = len(index)

        merged[
            "Period Start"
        ] = index.min()

        merged[
            "Period End"
        ] = index.max()

        rows.append(
            merged
        )

    return add_target_diagnostics(
        pd.concat(
            rows,
            ignore_index=True,
        )
    )


def date_window_mask(
    index: pd.DatetimeIndex,
    start: str,
    end: str,
) -> pd.Series:
    return pd.Series(
        (
            index >= pd.Timestamp(start)
        )
        & (
            index <= pd.Timestamp(end)
        ),
        index=index,
    )


def run_crisis_exclusion_analysis(
    market: str,
    returns: pd.DataFrame,
    turnovers: pd.DataFrame,
    benchmarks: pd.DataFrame,
) -> pd.DataFrame:
    exclusion_masks = {
        "Full Sample": pd.Series(
            False,
            index=returns.index,
        )
    }

    combined_crisis_mask = pd.Series(
        False,
        index=returns.index,
    )

    for (
        crisis_name,
        (
            start,
            end,
        ),
    ) in CRISIS_WINDOWS.items():
        crisis_mask = date_window_mask(
            returns.index,
            start,
            end,
        )

        exclusion_masks[
            f"Exclude {crisis_name}"
        ] = crisis_mask

        combined_crisis_mask = (
            combined_crisis_mask
            | crisis_mask
        )

    exclusion_masks[
        "Exclude All Major Crises"
    ] = combined_crisis_mask

    rows = []

    for (
        scenario,
        exclusion_mask,
    ) in exclusion_masks.items():
        retained_index = returns.index[
            ~exclusion_mask.to_numpy()
        ]

        if len(retained_index) < 24:
            continue

        retained_returns = returns.reindex(
            retained_index
        )

        retained_turnovers = (
            turnovers.reindex(
                retained_index
            )
        )

        performance = performance_table(
            retained_returns,
            retained_turnovers,
        )

        welfare = welfare_deltas(
            direct_returns=retained_returns,
            benchmarks=benchmarks.reindex(
                retained_index
            ),
            gamma=5.0,
        )

        merged = performance.merge(
            welfare,
            on="Strategy",
            how="left",
        )

        merged.insert(
            0,
            "Market",
            market.upper(),
        )

        merged.insert(
            1,
            "Scenario",
            scenario,
        )

        merged[
            "Excluded Obs"
        ] = int(
            exclusion_mask.sum()
        )

        merged[
            "Retained Obs"
        ] = len(retained_index)

        rows.append(
            merged
        )

    return add_target_diagnostics(
        pd.concat(
            rows,
            ignore_index=True,
        )
    )


def run_gamma_stability(
    market: str,
    returns: pd.DataFrame,
    benchmarks: pd.DataFrame,
) -> pd.DataFrame:
    panel = pd.concat(
        [
            benchmarks,
            returns,
        ],
        axis=1,
    )

    panel = clean_return_panel(
        panel
    )

    summary = build_welfare_summary(
        returns=panel,
        gammas=GAMMAS,
    )

    rows = []

    for gamma in GAMMAS:
        gamma_frame = summary.loc[
            summary["Gamma"].eq(
                gamma
            )
        ].copy()

        values = gamma_frame.set_index(
            "Strategy"
        )["MV CEQ Ann."]

        direct = gamma_frame.loc[
            gamma_frame[
                "Strategy"
            ].str.startswith(
                "Direct Short Variance"
            )
        ].copy()

        direct[
            "Delta MV CEQ vs 60/40"
        ] = (
            direct["MV CEQ Ann."]
            - float(values["60/40"])
        )

        direct[
            "Delta MV CEQ vs 1/N"
        ] = (
            direct["MV CEQ Ann."]
            - float(
                values[
                    "1/N Equity-Bond"
                ]
            )
        )

        direct.insert(
            0,
            "Market",
            market.upper(),
        )

        rows.append(
            direct
        )

    return pd.concat(
        rows,
        ignore_index=True,
    )


def print_key_results(
    market: str,
    name: str,
    frame: pd.DataFrame,
    parameter_column: str,
) -> None:
    key_strategy = (
        KEY_STRATEGIES[market]
    )

    selected = frame.loc[
        frame["Strategy"].eq(
            key_strategy
        )
    ].copy()

    display_columns = [
        parameter_column,
        "Ann. Return",
        "Ann. Vol",
        "Sharpe",
        "Max Drawdown",
        "CVaR 95",
        "Avg Turnover",
        "MV CEQ Ann.",
        "Delta MV CEQ vs 60/40",
        "Delta MV CEQ vs 1/N",
        "Realized / Target Vol",
    ]

    display_columns = [
        column
        for column in display_columns
        if column in selected.columns
    ]

    print()
    print("=" * 120)
    print(
        f"{market.upper()} — "
        f"{name} — "
        f"{key_strategy}"
    )
    print("=" * 120)

    print(
        selected[
            display_columns
        ].to_string(
            index=False
        )
    )


def run_market(
    market: str,
) -> dict[str, pd.DataFrame]:
    monthly = load_monthly(
        market
    )

    benchmarks = load_benchmarks(
        market
    )

    cost_configurations = [
        (
            f"{cost:.0f} bps",
            cost,
            make_config(
                transaction_cost_bps=cost
            ),
        )
        for cost in COST_GRID_BPS
    ]

    lookback_configurations = [
        (
            f"{lookback} months",
            float(lookback),
            make_config(
                lookback=lookback,
                minimum_observations=(
                    minimum_observations
                ),
            ),
        )
        for (
            lookback,
            minimum_observations,
        ) in LOOKBACK_GRID.items()
    ]

    cap_configurations = [
        (
            f"{cap:.0%}",
            cap,
            make_config(
                notional_cap=cap
            ),
        )
        for cap in NOTIONAL_CAP_GRID
    ]

    cost_table = (
        run_parameter_sensitivity(
            market=market,
            monthly=monthly,
            benchmarks=benchmarks,
            dimension=(
                "Transaction Costs"
            ),
            configurations=(
                cost_configurations
            ),
        )
    )

    lookback_table = (
        run_parameter_sensitivity(
            market=market,
            monthly=monthly,
            benchmarks=benchmarks,
            dimension=(
                "Volatility Lookback"
            ),
            configurations=(
                lookback_configurations
            ),
        )
    )

    cap_table = (
        run_parameter_sensitivity(
            market=market,
            monthly=monthly,
            benchmarks=benchmarks,
            dimension=(
                "Notional Cap"
            ),
            configurations=(
                cap_configurations
            ),
        )
    )

    baseline_config = make_config()

    (
        baseline_returns,
        baseline_turnovers,
    ) = run_configuration(
        monthly=monthly,
        config=baseline_config,
    )

    subperiod_table = (
        run_subperiod_analysis(
            market=market,
            returns=baseline_returns,
            turnovers=baseline_turnovers,
            benchmarks=benchmarks,
        )
    )

    crisis_table = (
        run_crisis_exclusion_analysis(
            market=market,
            returns=baseline_returns,
            turnovers=baseline_turnovers,
            benchmarks=benchmarks,
        )
    )

    gamma_table = run_gamma_stability(
        market=market,
        returns=baseline_returns,
        benchmarks=benchmarks,
    )

    tables = {
        "costs": cost_table,
        "lookbacks": lookback_table,
        "caps": cap_table,
        "subperiods": subperiod_table,
        "crises": crisis_table,
        "gamma": gamma_table,
    }

    for name, frame in tables.items():
        path = (
            TABLES_DIR
            / (
                f"{market}_direct_variance_"
                f"robustness_{name}.csv"
            )
        )

        frame.to_csv(
            path,
            index=False,
        )

    print_key_results(
        market=market,
        name="TRANSACTION COSTS",
        frame=cost_table,
        parameter_column=(
            "Parameter Label"
        ),
    )

    print_key_results(
        market=market,
        name="VOLATILITY LOOKBACK",
        frame=lookback_table,
        parameter_column=(
            "Parameter Label"
        ),
    )

    print_key_results(
        market=market,
        name="NOTIONAL CAP",
        frame=cap_table,
        parameter_column=(
            "Parameter Label"
        ),
    )

    print_key_results(
        market=market,
        name="SUBPERIODS",
        frame=subperiod_table,
        parameter_column="Period",
    )

    print_key_results(
        market=market,
        name="CRISIS EXCLUSIONS",
        frame=crisis_table,
        parameter_column="Scenario",
    )

    print()
    print("=" * 120)
    print(
        f"{market.upper()} — "
        "GAMMA STABILITY"
    )
    print("=" * 120)

    key_strategy = (
        KEY_STRATEGIES[market]
    )

    gamma_display = gamma_table.loc[
        gamma_table[
            "Strategy"
        ].eq(
            key_strategy
        ),
        [
            "Gamma",
            "MV CEQ Ann.",
            "CRRA CE Ann.",
            "Delta MV CEQ vs 60/40",
            "Delta MV CEQ vs 1/N",
        ],
    ]

    print(
        gamma_display.to_string(
            index=False
        )
    )

    return tables


def main() -> None:
    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    cross_market: dict[
        str,
        list[pd.DataFrame],
    ] = {
        "costs": [],
        "lookbacks": [],
        "caps": [],
        "subperiods": [],
        "crises": [],
        "gamma": [],
    }

    for market in (
        "us",
        "eu",
    ):
        market_tables = run_market(
            market
        )

        for (
            name,
            frame,
        ) in market_tables.items():
            cross_market[name].append(
                frame
            )

    for (
        name,
        frames,
    ) in cross_market.items():
        combined = pd.concat(
            frames,
            ignore_index=True,
        )

        path = (
            TABLES_DIR
            / (
                "cross_market_direct_variance_"
                f"robustness_{name}.csv"
            )
        )

        combined.to_csv(
            path,
            index=False,
        )

        print(
            f"Saved: {path}"
        )

    print()
    print("=" * 120)
    print(
        "MVP 7 DIRECT VARIANCE "
        "ROBUSTNESS COMPLETE"
    )
    print("=" * 120)


if __name__ == "__main__":
    main()
