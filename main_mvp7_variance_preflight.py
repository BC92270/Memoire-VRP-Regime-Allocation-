from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


PROCESSED_DIR = Path("data/processed")


def load_monthly(market: str) -> pd.DataFrame:
    path = (
        PROCESSED_DIR
        / f"{market}_monthly_rebalance.csv"
    )

    if not path.exists():
        raise FileNotFoundError(
            f"Missing file: {path}"
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

    required = {
        "iv_ann",
        "rv_ann",
        "vrp_proxy",
    }

    missing = sorted(
        required.difference(
            frame.columns
        )
    )

    if missing:
        raise KeyError(
            f"{market.upper()} missing: "
            f"{missing}"
        )

    return frame


def build_direct_variance_panel(
    monthly: pd.DataFrame,
) -> pd.DataFrame:
    panel = pd.DataFrame(
        index=monthly.index
    )

    # Variance strike observed at the previous
    # month-end, before the settlement month.
    panel["variance_strike"] = (
        monthly["iv_ann"].shift(1)
    )

    # Realized variance known only at the end
    # of the settlement month.
    panel["settlement_realized_variance"] = (
        monthly["rv_ann"]
    )

    # Short variance payoff in variance units.
    panel["short_variance_payoff"] = (
        panel["variance_strike"]
        - panel[
            "settlement_realized_variance"
        ]
    )

    # Long variance payoff for completeness.
    panel["long_variance_payoff"] = (
        -panel["short_variance_payoff"]
    )

    # Return-like normalization using the
    # variance strike as the economic base.
    panel["normalized_short_payoff"] = (
        panel["short_variance_payoff"]
        / panel["variance_strike"].replace(
            0.0,
            np.nan,
        )
    )

    # Log representation used by the existing
    # exploratory Pure VRP Proxy.
    panel["log_short_variance_carry"] = (
        np.log(
            panel["variance_strike"]
            / panel[
                "settlement_realized_variance"
            ].replace(
                0.0,
                np.nan,
            )
        )
    )

    panel["current_signal_vrp_proxy"] = (
        monthly["vrp_proxy"]
    )

    panel = panel.replace(
        [np.inf, -np.inf],
        np.nan,
    )

    return panel.dropna()


def print_summary(
    market: str,
    panel: pd.DataFrame,
) -> None:
    raw = panel["short_variance_payoff"]
    normalized = panel[
        "normalized_short_payoff"
    ]
    log_carry = panel[
        "log_short_variance_carry"
    ]

    print()
    print("=" * 100)
    print(
        f"{market.upper()} — "
        "CORRECTED DIRECT VARIANCE PREFLIGHT"
    )
    print("=" * 100)

    print(
        f"Valid observations: {len(panel)}"
    )

    print(
        "Sample: "
        f"{panel.index.min().date()} "
        "-> "
        f"{panel.index.max().date()}"
    )

    print()
    print("VARIANCE LEVELS")

    print(
        "Mean variance strike: "
        f"{panel['variance_strike'].mean():.6f}"
    )

    print(
        "Mean settlement realized variance: "
        f"{panel['settlement_realized_variance'].mean():.6f}"
    )

    print(
        "Mean short variance payoff: "
        f"{raw.mean():.6f}"
    )

    print(
        "Median short variance payoff: "
        f"{raw.median():.6f}"
    )

    print(
        "Positive short-variance months: "
        f"{raw.gt(0.0).mean():.2%}"
    )

    print()
    print("TAIL RISK")

    print(
        "Minimum short variance payoff: "
        f"{raw.min():.6f}"
    )

    print(
        "Maximum short variance payoff: "
        f"{raw.max():.6f}"
    )

    print(
        "5% quantile: "
        f"{raw.quantile(0.05):.6f}"
    )

    print(
        "1% quantile: "
        f"{raw.quantile(0.01):.6f}"
    )

    print()
    print("NORMALIZED PAYOFF")

    print(
        "Mean normalized short payoff: "
        f"{normalized.mean():.6f}"
    )

    print(
        "Median normalized short payoff: "
        f"{normalized.median():.6f}"
    )

    print(
        "Minimum normalized short payoff: "
        f"{normalized.min():.6f}"
    )

    print(
        "Months below -100% normalized payoff: "
        f"{normalized.le(-1.0).sum()} "
        f"({normalized.le(-1.0).mean():.2%})"
    )

    print()
    print("LOG CARRY")

    print(
        "Mean log short-variance carry: "
        f"{log_carry.mean():.6f}"
    )

    print(
        "Log-carry monthly volatility: "
        f"{log_carry.std(ddof=1):.6f}"
    )

    print(
        "Correlation between normalized payoff "
        "and log carry: "
        f"{normalized.corr(log_carry):.6f}"
    )

    print(
        "Correlation between current VRP signal "
        "and future short payoff: "
        f"{panel['current_signal_vrp_proxy'].corr(raw):.6f}"
    )

    print()
    print("RISK-TARGETING FEASIBILITY")

    for lookback in (
        12,
        24,
        36,
    ):
        lagged_vol = (
            normalized
            .rolling(
                window=lookback,
                min_periods=lookback,
            )
            .std(ddof=1)
            .shift(1)
        )

        print(
            f"{lookback}-month lagged volatility "
            f"observations: "
            f"{lagged_vol.notna().sum()}"
        )

    print()
    print("FIRST OBSERVATIONS")

    print(
        panel[
            [
                "variance_strike",
                "settlement_realized_variance",
                "short_variance_payoff",
                "normalized_short_payoff",
                "log_short_variance_carry",
            ]
        ]
        .head(8)
        .to_string()
    )


def main() -> None:
    for market in (
        "us",
        "eu",
    ):
        monthly = load_monthly(
            market
        )

        panel = (
            build_direct_variance_panel(
                monthly
            )
        )

        print_summary(
            market=market,
            panel=panel,
        )

    print()
    print("=" * 100)
    print(
        "CORRECTED MVP 7A PREFLIGHT COMPLETE"
    )
    print("=" * 100)


if __name__ == "__main__":
    main()
