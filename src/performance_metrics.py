from __future__ import annotations

import numpy as np
import pandas as pd


def cumulative_wealth(returns: pd.Series, initial_value: float = 1.0) -> pd.Series:
    returns = returns.dropna()
    return initial_value * (1.0 + returns).cumprod()


def max_drawdown(returns: pd.Series) -> float:
    wealth = cumulative_wealth(returns)
    running_max = wealth.cummax()
    drawdown = wealth / running_max - 1.0
    return float(drawdown.min())


def annualized_return(returns: pd.Series, periods_per_year: int = 12) -> float:
    returns = returns.dropna()
    if returns.empty:
        return np.nan

    total_return = (1.0 + returns).prod()
    years = len(returns) / periods_per_year

    if years <= 0:
        return np.nan

    return float(total_return ** (1.0 / years) - 1.0)


def annualized_volatility(returns: pd.Series, periods_per_year: int = 12) -> float:
    returns = returns.dropna()
    if returns.shape[0] < 2:
        return np.nan
    return float(returns.std(ddof=1) * np.sqrt(periods_per_year))


def sharpe_ratio(returns: pd.Series, periods_per_year: int = 12) -> float:
    returns = returns.dropna()
    vol = returns.std(ddof=1)

    if returns.empty or vol == 0 or np.isnan(vol):
        return np.nan

    return float((returns.mean() / vol) * np.sqrt(periods_per_year))


def sortino_ratio(returns: pd.Series, periods_per_year: int = 12) -> float:
    returns = returns.dropna()
    downside = returns[returns < 0]

    if downside.empty:
        return np.nan

    downside_vol = downside.std(ddof=1)

    if downside_vol == 0 or np.isnan(downside_vol):
        return np.nan

    return float((returns.mean() / downside_vol) * np.sqrt(periods_per_year))


def calmar_ratio(returns: pd.Series, periods_per_year: int = 12) -> float:
    ann_ret = annualized_return(returns, periods_per_year=periods_per_year)
    mdd = max_drawdown(returns)

    if mdd == 0 or np.isnan(mdd):
        return np.nan

    return float(ann_ret / abs(mdd))


def var_cvar(
    returns: pd.Series,
    alpha: float = 0.05,
) -> tuple[float, float]:
    """
    Returns left-tail VaR and CVaR in return space.
    Values are usually negative.
    """
    returns = returns.dropna()

    if returns.empty:
        return np.nan, np.nan

    var = float(returns.quantile(alpha))
    cvar = float(returns[returns <= var].mean())

    return var, cvar


def summarize_strategy(
    returns: pd.Series,
    turnover: pd.Series | None = None,
    periods_per_year: int = 12,
) -> dict:
    returns = returns.dropna()
    var_95, cvar_95 = var_cvar(returns, alpha=0.05)

    if turnover is not None:
        avg_turnover = float(turnover.reindex(returns.index).dropna().mean())
    else:
        avg_turnover = np.nan

    return {
        "Ann. Return": annualized_return(returns, periods_per_year),
        "Ann. Vol": annualized_volatility(returns, periods_per_year),
        "Sharpe": sharpe_ratio(returns, periods_per_year),
        "Sortino": sortino_ratio(returns, periods_per_year),
        "Max Drawdown": max_drawdown(returns),
        "Calmar": calmar_ratio(returns, periods_per_year),
        "VaR 95": var_95,
        "CVaR 95": cvar_95,
        "Avg Turnover": avg_turnover,
        "Obs": int(returns.shape[0]),
    }


def summarize_strategies(
    strategy_returns: pd.DataFrame,
    turnovers: pd.DataFrame | None = None,
    periods_per_year: int = 12,
) -> pd.DataFrame:
    rows = {}

    for column in strategy_returns.columns:
        turnover = None
        if turnovers is not None and column in turnovers.columns:
            turnover = turnovers[column]

        rows[column] = summarize_strategy(
            strategy_returns[column],
            turnover=turnover,
            periods_per_year=periods_per_year,
        )

    summary = pd.DataFrame(rows).T
    return summary