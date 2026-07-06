from __future__ import annotations

import numpy as np
import pandas as pd


def add_return_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Adds daily log returns for equity and bond series.
    """
    out = df.copy()

    out["equity_log_ret"] = np.log(out["equity_price"] / out["equity_price"].shift(1))
    out["bond_log_ret"] = np.log(out["bond_price"] / out["bond_price"].shift(1))

    return out


def add_realized_variance(
    df: pd.DataFrame,
    window: int = 21,
    trading_days_per_year: int = 252,
) -> pd.DataFrame:
    """
    Computes annualized realized variance from daily equity log returns.
    """
    out = df.copy()

    out["rv_ann"] = (
        out["equity_log_ret"]
        .pow(2)
        .rolling(window=window, min_periods=window)
        .sum()
        * (trading_days_per_year / window)
    )

    return out


def add_implied_variance(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts implied volatility index level into annualized implied variance.
    Example: VIX = 20 means implied volatility = 20%, so IV = (20/100)^2.
    """
    out = df.copy()

    out["iv_ann"] = (out["implied_vol_index"] / 100.0) ** 2

    return out


def add_vrp_proxy(df: pd.DataFrame) -> pd.DataFrame:
    """
    Baseline VRP proxy:
        VRP = implied variance - past realized variance

    This is a signal proxy, not a perfect tradable variance swap return.
    """
    out = df.copy()

    out["vrp_proxy"] = out["iv_ann"] - out["rv_ann"]

    return out


def build_daily_feature_set(
    df: pd.DataFrame,
    rv_window: int = 21,
    trading_days_per_year: int = 252,
) -> pd.DataFrame:
    """
    Full daily feature pipeline.
    """
    out = add_return_columns(df)
    out = add_realized_variance(
        out,
        window=rv_window,
        trading_days_per_year=trading_days_per_year,
    )
    out = add_implied_variance(out)
    out = add_vrp_proxy(out)
    out = out.dropna()

    return out


def build_monthly_rebalance_dataset(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converts daily features to a monthly rebalancing dataset.

    Features are observed at month-end.
    Returns are monthly holding-period returns.
    """
    monthly_prices = df[["equity_price", "bond_price"]].resample("ME").last()
    monthly_returns = monthly_prices.pct_change()
    monthly_returns = monthly_returns.rename(
        columns={
            "equity_price": "equity_ret",
            "bond_price": "bond_ret",
        }
    )

    monthly_features = df[
        [
            "rv_ann",
            "iv_ann",
            "vrp_proxy",
            "implied_vol_index",
        ]
    ].resample("ME").last()

    monthly = pd.concat([monthly_features, monthly_returns], axis=1)
    monthly = monthly.dropna()

    return monthly