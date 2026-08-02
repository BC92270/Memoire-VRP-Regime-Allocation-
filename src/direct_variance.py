from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd


@dataclass(frozen=True)
class DirectVarianceConfig:
    """
    Configuration for the model-based direct variance carry extension.

    This module does not reconstruct a fully tradable variance swap from
    option prices.

    Approximation:
        variance strike at t-1 = implied-volatility index squared
        settlement variance at t = annualized 21-day realized variance

    The strike-normalized payoff is then scaled using strictly lagged
    realized volatility.
    """

    volatility_lookback_months: int = 36
    minimum_volatility_observations: int = 24
    high_vrp_lookback_months: int = 36
    minimum_vrp_observations: int = 24
    max_abs_notional: float = 0.25
    transaction_cost_bps: float = 10.0


DEFAULT_STRATEGY_SPECS: dict[
    str,
    tuple[float, str],
] = {
    "Direct Short Variance 5% Vol": (
        0.05,
        "always",
    ),
    "Direct Short Variance 10% Vol": (
        0.10,
        "always",
    ),
    "Direct Short Variance 10% Vol (VRP > 0)": (
        0.10,
        "positive_vrp",
    ),
    "Direct Short Variance 10% Vol (High VRP)": (
        0.10,
        "high_vrp",
    ),
}


def _validate_monthly_data(
    monthly: pd.DataFrame,
) -> pd.DataFrame:
    required = {
        "iv_ann",
        "rv_ann",
        "vrp_proxy",
        "log_iv_rv",
    }

    missing = sorted(
        required.difference(
            monthly.columns
        )
    )

    if missing:
        raise KeyError(
            "Missing required direct-variance "
            f"columns: {missing}"
        )

    frame = monthly.copy()

    if not isinstance(
        frame.index,
        pd.DatetimeIndex,
    ):
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

    frame = frame.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return frame


def build_direct_variance_panel(
    monthly: pd.DataFrame,
    config: DirectVarianceConfig | None = None,
) -> pd.DataFrame:
    """
    Builds a strictly forward-aligned variance-carry panel.

    For a settlement month t:

        strike_t = IV_(t-1)
        realized_t = RV_t
        short payoff_t = strike_t - realized_t

    The entry signal is also shifted by one month and is therefore
    observable before the settlement return is realized.
    """
    config = (
        config
        or DirectVarianceConfig()
    )

    frame = _validate_monthly_data(
        monthly
    )

    panel = pd.DataFrame(
        index=frame.index
    )

    panel["variance_strike"] = (
        frame["iv_ann"].shift(1)
    )

    panel[
        "settlement_realized_variance"
    ] = frame["rv_ann"]

    panel["short_variance_payoff"] = (
        panel["variance_strike"]
        - panel[
            "settlement_realized_variance"
        ]
    )

    panel["long_variance_payoff"] = (
        -panel["short_variance_payoff"]
    )

    panel[
        "normalized_short_payoff"
    ] = (
        panel["short_variance_payoff"]
        / panel[
            "variance_strike"
        ].replace(
            0.0,
            np.nan,
        )
    )

    panel[
        "log_short_variance_carry"
    ] = np.log(
        panel["variance_strike"]
        / panel[
            "settlement_realized_variance"
        ].replace(
            0.0,
            np.nan,
        )
    )

    # Signals available at the entry month-end.
    panel["entry_vrp_signal"] = (
        frame["vrp_proxy"].shift(1)
    )

    panel["entry_log_vrp_signal"] = (
        frame["log_iv_rv"].shift(1)
    )

    # Strictly lagged risk estimate. At settlement month t,
    # this estimate only contains payoffs realized through t-1.
    panel["lagged_payoff_vol"] = (
        panel[
            "normalized_short_payoff"
        ]
        .rolling(
            window=(
                config
                .volatility_lookback_months
            ),
            min_periods=(
                config
                .minimum_volatility_observations
            ),
        )
        .std(ddof=1)
        .shift(1)
    )

    # Historical VRP threshold excluding the current entry signal.
    panel["lagged_high_vrp_threshold"] = (
        panel["entry_vrp_signal"]
        .rolling(
            window=(
                config
                .high_vrp_lookback_months
            ),
            min_periods=(
                config
                .minimum_vrp_observations
            ),
        )
        .median()
        .shift(1)
    )

    panel = panel.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return panel


def _strategy_gate(
    panel: pd.DataFrame,
    gate_name: str,
) -> tuple[
    pd.Series,
    pd.Series,
]:
    if gate_name == "always":
        gate = pd.Series(
            True,
            index=panel.index,
        )

        valid_gate = pd.Series(
            True,
            index=panel.index,
        )

        return gate, valid_gate

    if gate_name == "positive_vrp":
        valid_gate = panel[
            "entry_vrp_signal"
        ].notna()

        gate = (
            panel["entry_vrp_signal"]
            > 0.0
        )

        return gate, valid_gate

    if gate_name == "high_vrp":
        valid_gate = (
            panel["entry_vrp_signal"]
            .notna()
            & panel[
                "lagged_high_vrp_threshold"
            ].notna()
        )

        gate = (
            panel["entry_vrp_signal"]
            > panel[
                "lagged_high_vrp_threshold"
            ]
        )

        return gate, valid_gate

    raise ValueError(
        f"Unsupported gate: {gate_name}"
    )


def run_direct_variance_strategy(
    panel: pd.DataFrame,
    strategy_name: str,
    target_ann_vol: float,
    gate_name: str,
    config: DirectVarianceConfig | None = None,
) -> tuple[
    pd.Series,
    pd.Series,
    pd.DataFrame,
]:
    config = (
        config
        or DirectVarianceConfig()
    )

    if target_ann_vol <= 0.0:
        raise ValueError(
            "target_ann_vol must be positive."
        )

    monthly_target_vol = (
        target_ann_vol
        / np.sqrt(12.0)
    )

    lagged_vol = panel[
        "lagged_payoff_vol"
    ]

    base_notional = (
        monthly_target_vol
        / lagged_vol.replace(
            0.0,
            np.nan,
        )
    )

    base_notional = base_notional.clip(
        lower=0.0,
        upper=config.max_abs_notional,
    )

    gate, valid_gate = _strategy_gate(
        panel=panel,
        gate_name=gate_name,
    )

    valid = (
        panel[
            "normalized_short_payoff"
        ].notna()
        & lagged_vol.notna()
        & lagged_vol.gt(0.0)
        & valid_gate
    )

    # Preserve NaN outside the estimable sample.
    # Inside the valid sample, take exposure only when the gate is active.
    target_notional = pd.Series(
        np.nan,
        index=panel.index,
        dtype=float,
    )

    target_notional.loc[valid] = (
        base_notional.loc[valid]
        * gate.loc[valid].astype(float)
    )

    target_notional.name = (
        "target_notional"
    )

    previous_notional = (
        target_notional.shift(1)
    )

    # Change in desired exposure, retained as a diagnostic.
    rebalance_turnover = (
        target_notional
        - previous_notional
    ).abs()

    first_valid_index = (
        target_notional
        .first_valid_index()
    )

    if first_valid_index is not None:
        rebalance_turnover.loc[
            first_valid_index
        ] = abs(
            target_notional.loc[
                first_valid_index
            ]
        )

    # Each one-month variance exposure settles and must be
    # replaced by a new contract. Transaction costs therefore
    # apply to the full monthly notional entered, not merely
    # to the change relative to the previous month.
    roll_notional = (
        target_notional.abs()
    )

    transaction_cost_notional = (
        roll_notional
    )

    gross_return = (
        target_notional
        * panel[
            "normalized_short_payoff"
        ]
    )

    cost_rate = (
        config.transaction_cost_bps
        / 10_000.0
    )

    transaction_cost = (
        cost_rate
        * transaction_cost_notional
    )

    net_return = (
        gross_return
        - transaction_cost
    )

    net_return = net_return.dropna()
    net_return.name = strategy_name

    # Report the notional on which implementation costs
    # are charged as the economically relevant turnover.
    turnover = (
        transaction_cost_notional
        .reindex(net_return.index)
    )

    turnover.name = strategy_name

    diagnostics = panel.reindex(
        net_return.index
    ).copy()

    diagnostics.insert(
        0,
        "strategy",
        strategy_name,
    )

    diagnostics.insert(
        1,
        "target_ann_vol",
        target_ann_vol,
    )

    diagnostics.insert(
        2,
        "gate_name",
        gate_name,
    )

    diagnostics[
        "gate_active"
    ] = gate.reindex(
        net_return.index
    ).astype(int)

    diagnostics[
        "target_notional"
    ] = target_notional.reindex(
        net_return.index
    )

    diagnostics["turnover"] = (
        turnover
    )

    diagnostics["gross_return"] = (
        gross_return.reindex(
            net_return.index
        )
    )

    diagnostics[
        "transaction_cost"
    ] = transaction_cost.reindex(
        net_return.index
    )

    diagnostics["net_return"] = (
        net_return
    )

    diagnostics.index.name = "Date"
    diagnostics = (
        diagnostics.reset_index()
    )

    return (
        net_return,
        turnover,
        diagnostics,
    )


def build_direct_variance_strategy_set(
    monthly: pd.DataFrame,
    config: DirectVarianceConfig | None = None,
    strategy_specs: (
        dict[
            str,
            tuple[float, str],
        ]
        | None
    ) = None,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    config = (
        config
        or DirectVarianceConfig()
    )

    specs = (
        strategy_specs
        or DEFAULT_STRATEGY_SPECS
    )

    panel = build_direct_variance_panel(
        monthly=monthly,
        config=config,
    )

    return_series: dict[
        str,
        pd.Series,
    ] = {}

    turnover_series: dict[
        str,
        pd.Series,
    ] = {}

    diagnostics: list[
        pd.DataFrame
    ] = []

    for (
        strategy_name,
        (
            target_ann_vol,
            gate_name,
        ),
    ) in specs.items():
        (
            strategy_return,
            strategy_turnover,
            strategy_diagnostics,
        ) = run_direct_variance_strategy(
            panel=panel,
            strategy_name=strategy_name,
            target_ann_vol=(
                target_ann_vol
            ),
            gate_name=gate_name,
            config=config,
        )

        return_series[
            strategy_name
        ] = strategy_return

        turnover_series[
            strategy_name
        ] = strategy_turnover

        diagnostics.append(
            strategy_diagnostics
        )

    returns = pd.DataFrame(
        return_series
    ).dropna(
        how="any"
    )

    turnovers = pd.DataFrame(
        turnover_series
    ).reindex(
        returns.index
    )

    diagnostic_frame = pd.concat(
        diagnostics,
        ignore_index=True,
    )

    diagnostic_frame = (
        diagnostic_frame.loc[
            diagnostic_frame[
                "Date"
            ].isin(
                returns.index
            )
        ]
        .reset_index(drop=True)
    )

    panel.index.name = "Date"

    return (
        returns,
        turnovers,
        diagnostic_frame,
        panel,
    )


def summarize_direct_variance_diagnostics(
    diagnostics: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[
        dict[str, object]
    ] = []

    for strategy, group in (
        diagnostics.groupby(
            "strategy",
            sort=True,
        )
    ):
        rows.append(
            {
                "Strategy": strategy,
                "Target Ann. Vol": float(
                    group[
                        "target_ann_vol"
                    ].iloc[0]
                ),
                "Gate": (
                    group[
                        "gate_name"
                    ].iloc[0]
                ),
                "Observations": int(
                    len(group)
                ),
                "Active Rate": float(
                    group[
                        "gate_active"
                    ].mean()
                ),
                "Avg Abs Notional": float(
                    group[
                        "target_notional"
                    ]
                    .abs()
                    .mean()
                ),
                "Max Abs Notional": float(
                    group[
                        "target_notional"
                    ]
                    .abs()
                    .max()
                ),
                "Avg Turnover": float(
                    group[
                        "turnover"
                    ].mean()
                ),
                "Avg Gross Return": float(
                    group[
                        "gross_return"
                    ].mean()
                ),
                "Avg Transaction Cost": float(
                    group[
                        "transaction_cost"
                    ].mean()
                ),
                "Worst Monthly Return": float(
                    group[
                        "net_return"
                    ].min()
                ),
                "Best Monthly Return": float(
                    group[
                        "net_return"
                    ].max()
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values(
            "Strategy"
        )
        .reset_index(drop=True)
    )
