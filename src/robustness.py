from __future__ import annotations

import numpy as np
import pandas as pd

from src.performance_metrics import summarize_strategies


def infer_gross_returns_from_net(
    net_returns: pd.DataFrame,
    turnovers: pd.DataFrame,
    base_cost_bps: float = 10.0,
    no_addback_columns: list[str] | None = None,
) -> pd.DataFrame:
    """
    Infers approximate gross returns from net returns and turnover.

    Most strategies in the pipeline are already net of 10 bps transaction costs.
    Pure VRP Proxy is treated separately because the MVP proxy was not initially
    constructed as a fully cost-adjusted tradable strategy.
    """
    if no_addback_columns is None:
        no_addback_columns = []

    no_addback_columns = set(no_addback_columns)

    returns = net_returns.copy()
    turns = turnovers.reindex(returns.index).fillna(0.0)

    gross = returns.copy()
    base_cost_rate = base_cost_bps / 10_000.0

    for col in gross.columns:
        if col in turns.columns and col not in no_addback_columns:
            gross[col] = returns[col] + base_cost_rate * turns[col]

    return gross


def transaction_cost_sensitivity(
    net_returns: pd.DataFrame,
    turnovers: pd.DataFrame,
    cost_bps_grid: list[float],
    base_cost_bps: float = 10.0,
    periods_per_year: int = 12,
    no_addback_columns: list[str] | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[float, pd.DataFrame]]:
    """
    Recomputes net returns and performance summaries under alternative
    transaction-cost assumptions.
    """
    gross_returns = infer_gross_returns_from_net(
        net_returns=net_returns,
        turnovers=turnovers,
        base_cost_bps=base_cost_bps,
        no_addback_columns=no_addback_columns,
    )

    turns = turnovers.reindex(gross_returns.index).fillna(0.0)

    summaries = []
    net_returns_by_cost = {}

    for cost_bps in cost_bps_grid:
        cost_rate = cost_bps / 10_000.0

        adjusted_returns = gross_returns.copy()

        for col in adjusted_returns.columns:
            if col in turns.columns:
                adjusted_returns[col] = gross_returns[col] - cost_rate * turns[col]

        net_returns_by_cost[cost_bps] = adjusted_returns

        summary = summarize_strategies(
            adjusted_returns,
            turnovers=turns,
            periods_per_year=periods_per_year,
        )

        summary.insert(0, "Cost bps", cost_bps)
        summary.insert(1, "Strategy", summary.index)

        summaries.append(summary.reset_index(drop=True))

    long_summary = pd.concat(summaries, axis=0, ignore_index=True)

    sharpe_pivot = long_summary.pivot(
        index="Strategy",
        columns="Cost bps",
        values="Sharpe",
    )

    maxdd_pivot = long_summary.pivot(
        index="Strategy",
        columns="Cost bps",
        values="Max Drawdown",
    )

    return long_summary, sharpe_pivot, maxdd_pivot, net_returns_by_cost


def simulate_dynamic_target_weight_strategy(
    monthly: pd.DataFrame,
    diagnostics: pd.DataFrame,
    strategy_name: str,
    cost_bps: float = 10.0,
    no_trade_band: float = 0.0,
) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """
    Re-simulates a dynamic allocation strategy using stored target weights.

    no_trade_band:
        If the absolute difference between the desired equity weight and the
        current drifted equity weight is below the band, the strategy does not rebalance.

    This controls turnover without changing the underlying model signals.
    """
    required_diag_cols = ["equity_weight", "bond_weight"]
    required_monthly_cols = ["equity_ret", "bond_ret"]

    for col in required_diag_cols:
        if col not in diagnostics.columns:
            raise ValueError(f"Missing diagnostics column: {col}")

    for col in required_monthly_cols:
        if col not in monthly.columns:
            raise ValueError(f"Missing monthly column: {col}")

    target_weights = diagnostics[required_diag_cols].dropna().copy()
    asset_returns = monthly[required_monthly_cols].reindex(target_weights.index).dropna()

    target_weights = target_weights.reindex(asset_returns.index).dropna()

    if target_weights.empty:
        raise ValueError(f"No overlapping target weights and monthly returns for {strategy_name}")

    cost_rate = cost_bps / 10_000.0

    portfolio_returns = []
    turnovers = []
    records = []

    current_pre_trade_weights = None

    for date, target_row in target_weights.iterrows():
        asset_ret = asset_returns.loc[date].astype(float)

        target = pd.Series(
            {
                "equity_ret": float(target_row["equity_weight"]),
                "bond_ret": float(target_row["bond_weight"]),
            },
            dtype=float,
        )

        target = target / target.sum()

        if current_pre_trade_weights is None:
            trade_weights = target.copy()
            turnover = float(trade_weights.abs().sum())
            traded = True
        else:
            equity_gap = abs(target["equity_ret"] - current_pre_trade_weights["equity_ret"])

            if equity_gap <= no_trade_band:
                trade_weights = current_pre_trade_weights.copy()
                turnover = 0.0
                traded = False
            else:
                trade_weights = target.copy()
                turnover = float((trade_weights - current_pre_trade_weights).abs().sum())
                traded = True

        gross_return = float((trade_weights * asset_ret).sum())
        net_return = float(gross_return - cost_rate * turnover)

        denominator = 1.0 + gross_return

        if denominator <= 0:
            current_pre_trade_weights = target.copy()
        else:
            current_pre_trade_weights = trade_weights * (1.0 + asset_ret)
            current_pre_trade_weights = current_pre_trade_weights / denominator

        portfolio_returns.append((date, net_return))
        turnovers.append((date, turnover))

        records.append(
            {
                "date": date,
                "strategy": strategy_name,
                "no_trade_band": no_trade_band,
                "cost_bps": cost_bps,
                "target_equity_weight": target["equity_ret"],
                "traded_equity_weight": trade_weights["equity_ret"],
                "target_bond_weight": target["bond_ret"],
                "traded_bond_weight": trade_weights["bond_ret"],
                "turnover": turnover,
                "traded": traded,
                "gross_return": gross_return,
                "net_return": net_return,
            }
        )

    ret_series = pd.Series(
        data=[x[1] for x in portfolio_returns],
        index=[x[0] for x in portfolio_returns],
        name=strategy_name,
    )

    turnover_series = pd.Series(
        data=[x[1] for x in turnovers],
        index=[x[0] for x in turnovers],
        name=strategy_name,
    )

    weights = pd.DataFrame(records).set_index("date")

    return ret_series, turnover_series, weights


def no_trade_band_sensitivity(
    monthly: pd.DataFrame,
    diagnostics_by_strategy: dict[str, pd.DataFrame],
    no_trade_bands: list[float],
    cost_bps: float = 10.0,
    periods_per_year: int = 12,
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Tests no-trade bands on stored HMM/RSM target weights.
    """
    summaries = []
    all_returns = {}
    all_turnovers = {}

    for band in no_trade_bands:
        strategy_returns = {}
        strategy_turnovers = {}

        for strategy_name, diag in diagnostics_by_strategy.items():
            ret, turn, _weights = simulate_dynamic_target_weight_strategy(
                monthly=monthly,
                diagnostics=diag,
                strategy_name=strategy_name,
                cost_bps=cost_bps,
                no_trade_band=band,
            )

            strategy_returns[strategy_name] = ret
            strategy_turnovers[strategy_name] = turn

        returns_df = pd.DataFrame(strategy_returns).dropna(how="all")
        turnovers_df = pd.DataFrame(strategy_turnovers).reindex(returns_df.index)

        summary = summarize_strategies(
            returns_df,
            turnovers=turnovers_df,
            periods_per_year=periods_per_year,
        )

        summary.insert(0, "No-trade band", band)
        summary.insert(1, "Strategy", summary.index)

        summaries.append(summary.reset_index(drop=True))

        all_returns[band] = returns_df
        all_turnovers[band] = turnovers_df

    long_summary = pd.concat(summaries, axis=0, ignore_index=True)

    sharpe_pivot = long_summary.pivot(
        index="Strategy",
        columns="No-trade band",
        values="Sharpe",
    )

    turnover_pivot = long_summary.pivot(
        index="Strategy",
        columns="No-trade band",
        values="Avg Turnover",
    )

    return long_summary, sharpe_pivot, turnover_pivot