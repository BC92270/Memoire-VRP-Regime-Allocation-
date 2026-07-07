from __future__ import annotations

import matplotlib.pyplot as plt
import pandas as pd


def plot_cumulative_returns(
    strategy_returns: pd.DataFrame,
    output_path,
    title: str = "Cumulative Strategy Returns",
) -> None:
    """
    Plots cumulative wealth for strategy returns.
    """
    returns = strategy_returns.dropna(how="all")
    wealth = (1.0 + returns).cumprod()

    fig, ax = plt.subplots(figsize=(12, 7))
    wealth.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Cumulative wealth")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_vrp_components(
    monthly: pd.DataFrame,
    output_path,
    title: str = "Implied Variance, Realized Variance and VRP Proxy",
) -> None:
    """
    Plots implied variance, realized variance and VRP proxy.
    """
    required = ["iv_ann", "rv_ann", "vrp_proxy"]
    data = monthly[required].dropna()

    fig, ax = plt.subplots(figsize=(12, 7))
    data.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Annualized variance")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_drawdowns(
    strategy_returns: pd.DataFrame,
    output_path,
    title: str = "Strategy Drawdowns",
) -> None:
    """
    Plots drawdowns for all strategies.
    """
    returns = strategy_returns.dropna(how="all")
    wealth = (1.0 + returns).cumprod()
    running_max = wealth.cummax()
    drawdowns = wealth / running_max - 1.0

    fig, ax = plt.subplots(figsize=(12, 7))
    drawdowns.plot(ax=ax)

    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(True, alpha=0.3)

    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)


def plot_feature_correlation_heatmap(
    corr: pd.DataFrame,
    output_path,
    title: str = "Feature Correlation Matrix",
) -> None:
    """
    Plots a simple correlation heatmap without external dependencies.
    """
    fig, ax = plt.subplots(figsize=(9, 7))
    im = ax.imshow(corr.values, aspect="auto", vmin=-1, vmax=1)

    ax.set_xticks(range(len(corr.columns)))
    ax.set_yticks(range(len(corr.index)))
    ax.set_xticklabels(corr.columns, rotation=45, ha="right")
    ax.set_yticklabels(corr.index)
    ax.set_title(title)

    for i in range(len(corr.index)):
        for j in range(len(corr.columns)):
            ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=8)

    fig.colorbar(im, ax=ax, fraction=0.046, pad=0.04)
    fig.tight_layout()
    fig.savefig(output_path, dpi=160)
    plt.close(fig)