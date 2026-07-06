from __future__ import annotations

import numpy as np
import pandas as pd


def static_rebalanced_portfolio(
    asset_returns: pd.DataFrame,
    target_weights: dict[str, float],
    transaction_cost_bps: float = 0.0,
) -> tuple[pd.Series, pd.Series]:
    """
    Simulates a static target-weight portfolio rebalanced every period.

    asset_returns columns must match target_weights keys.
    """
    returns = asset_returns[list(target_weights.keys())].dropna()
    weights = pd.Series(target_weights, dtype=float)
    weights = weights / weights.sum()

    cost_rate = transaction_cost_bps / 10_000.0

    portfolio_returns = []
    turnovers = []

    current_weights = weights.copy()

    for date, row in returns.iterrows():
        asset_ret = row.astype(float)

        gross_return = float((current_weights * asset_ret).sum())

        # Weights after asset returns, before rebalancing
        pre_rebalance_weights = current_weights * (1.0 + asset_ret)
        pre_rebalance_weights = pre_rebalance_weights / (1.0 + gross_return)

        turnover = float((weights - pre_rebalance_weights).abs().sum())
        net_return = gross_return - cost_rate * turnover

        portfolio_returns.append((date, net_return))
        turnovers.append((date, turnover))

        # Rebalance back to target weights
        current_weights = weights.copy()

    ret_series = pd.Series(
        data=[x[1] for x in portfolio_returns],
        index=[x[0] for x in portfolio_returns],
        name="portfolio_return",
    )

    turnover_series = pd.Series(
        data=[x[1] for x in turnovers],
        index=[x[0] for x in turnovers],
        name="turnover",
    )

    return ret_series, turnover_series


def pure_vrp_proxy_strategy(
    monthly: pd.DataFrame,
    target_ann_vol: float = 0.10,
    lookback_months: int = 12,
    max_leverage: float = 3.0,
) -> tuple[pd.Series, pd.Series]:
    """
    Synthetic short-VRP proxy.

    Approximation:
        short variance payoff ≈ log(IV_{t-1} / RV_t)

    This is not a true variance swap backtest.
    It is a dimensionless proxy used as a first-pass benchmark.
    """
    iv_lag = monthly["iv_ann"].shift(1)
    realized_rv = monthly["rv_ann"]

    raw = np.log(iv_lag / realized_rv.replace(0.0, np.nan))
    raw = raw.replace([np.inf, -np.inf], np.nan)

    # Volatility targeting based only on past raw proxy returns
    monthly_target_vol = target_ann_vol / np.sqrt(12)
    rolling_vol = raw.rolling(lookback_months).std().shift(1)

    leverage = monthly_target_vol / rolling_vol
    leverage = leverage.clip(lower=0.0, upper=max_leverage)
    leverage = leverage.replace([np.inf, -np.inf], np.nan).fillna(0.0)

    strategy_ret = leverage * raw
    strategy_ret.name = "Pure VRP Proxy"

    turnover = leverage.diff().abs().fillna(0.0)
    turnover.name = "Pure VRP Proxy"

    return strategy_ret.dropna(), turnover.reindex(strategy_ret.dropna().index)


def build_benchmark_strategies(
    monthly: pd.DataFrame,
    transaction_cost_bps: float = 10.0,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """
    Builds MVP benchmark strategies:
    - Buy-and-hold equity
    - 60/40 equity/bond
    - 1/N equity/bond
    - Pure VRP proxy
    """
    asset_returns = monthly[["equity_ret", "bond_ret"]].dropna()

    strategy_returns = pd.DataFrame(index=asset_returns.index)
    turnovers = pd.DataFrame(index=asset_returns.index)

    # S0 Buy-and-hold equity
    strategy_returns["Buy-and-Hold Equity"] = asset_returns["equity_ret"]
    turnovers["Buy-and-Hold Equity"] = 0.0

    # S1 60/40
    ret_6040, turn_6040 = static_rebalanced_portfolio(
        asset_returns,
        target_weights={"equity_ret": 0.60, "bond_ret": 0.40},
        transaction_cost_bps=transaction_cost_bps,
    )
    strategy_returns["60/40"] = ret_6040
    turnovers["60/40"] = turn_6040

    # S2 1/N across equity and bond
    ret_1n, turn_1n = static_rebalanced_portfolio(
        asset_returns,
        target_weights={"equity_ret": 0.50, "bond_ret": 0.50},
        transaction_cost_bps=transaction_cost_bps,
    )
    strategy_returns["1/N Equity-Bond"] = ret_1n
    turnovers["1/N Equity-Bond"] = turn_1n

    # S3 Pure VRP proxy
    ret_vrp, turn_vrp = pure_vrp_proxy_strategy(monthly)
    strategy_returns["Pure VRP Proxy"] = ret_vrp
    turnovers["Pure VRP Proxy"] = turn_vrp

    strategy_returns = strategy_returns.dropna(how="all")
    turnovers = turnovers.reindex(strategy_returns.index).fillna(0.0)

    return strategy_returns, turnovers