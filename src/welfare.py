from __future__ import annotations

from collections.abc import Iterable

import numpy as np
import pandas as pd


PERIODS_PER_YEAR = 12


def clean_return_panel(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Convert a return DataFrame into a numeric, date-sorted,
    common-sample panel of simple monthly returns.
    """
    panel = returns.copy()

    panel.columns = [
        str(column).strip()
        for column in panel.columns
    ]

    panel = panel.apply(pd.to_numeric, errors="coerce")
    panel = panel.replace([np.inf, -np.inf], np.nan)

    panel = panel.dropna(axis=1, how="all")
    panel = panel.dropna(axis=0, how="all")

    if not isinstance(panel.index, pd.DatetimeIndex):
        panel.index = pd.to_datetime(
            panel.index,
            errors="coerce",
        )

    panel = panel.loc[~panel.index.isna()]

    panel = panel.loc[
        ~panel.index.duplicated(keep="last")
    ].sort_index()

    # Use exactly the same observations for all strategies.
    panel = panel.dropna(axis=0, how="any")

    if panel.empty:
        raise ValueError(
            "No common return sample remains after alignment."
        )

    return panel


def mv_ceq_annualized(
    returns: pd.Series | np.ndarray,
    gamma: float,
    periods_per_year: int = PERIODS_PER_YEAR,
) -> float:
    """
    Annualized mean-variance certainty equivalent:

        CEQ = mu - gamma / 2 * variance

    The calculation is performed monthly and then annualized.
    """
    values = np.asarray(returns, dtype=float)
    values = values[np.isfinite(values)]

    if values.size < 2:
        return np.nan

    monthly_mean = float(np.mean(values))
    monthly_variance = float(
        np.var(values, ddof=1)
    )

    monthly_ceq = (
        monthly_mean
        - 0.5 * float(gamma) * monthly_variance
    )

    return float(
        periods_per_year * monthly_ceq
    )


def crra_ce_annualized(
    returns: pd.Series | np.ndarray,
    gamma: float,
    periods_per_year: int = PERIODS_PER_YEAR,
) -> float:
    """
    Annualized one-period CRRA certainty-equivalent return.

    For gamma = 1, log utility is used.
    For gamma != 1, power utility is used.
    """
    values = np.asarray(returns, dtype=float)
    values = values[np.isfinite(values)]

    if values.size == 0:
        return np.nan

    gross_returns = 1.0 + values

    # CRRA utility is undefined for non-positive terminal wealth.
    if np.any(gross_returns <= 0.0):
        return np.nan

    gamma = float(gamma)

    if np.isclose(gamma, 1.0):
        monthly_ce_gross = float(
            np.exp(
                np.mean(
                    np.log(gross_returns)
                )
            )
        )

    else:
        expected_power = float(
            np.mean(
                gross_returns ** (1.0 - gamma)
            )
        )

        if (
            expected_power <= 0.0
            or not np.isfinite(expected_power)
        ):
            return np.nan

        monthly_ce_gross = (
            expected_power
            ** (1.0 / (1.0 - gamma))
        )

    return float(
        monthly_ce_gross**periods_per_year
        - 1.0
    )


def build_welfare_summary(
    returns: pd.DataFrame,
    gammas: Iterable[float] = (
        1.0,
        3.0,
        5.0,
        10.0,
    ),
) -> pd.DataFrame:
    """
    Compute mean-variance and CRRA welfare metrics
    for every strategy and every risk-aversion level.
    """
    panel = clean_return_panel(returns)

    rows: list[dict[str, object]] = []

    for gamma in gammas:
        for strategy in panel.columns:
            series = panel[strategy].astype(float)

            gross_domain_valid = bool(
                (1.0 + series > 0.0).all()
            )

            if gross_domain_valid:
                geometric_return = float(
                    (1.0 + series).prod()
                    ** (
                        PERIODS_PER_YEAR
                        / len(series)
                    )
                    - 1.0
                )
            else:
                geometric_return = np.nan

            rows.append(
                {
                    "Strategy": strategy,
                    "Gamma": float(gamma),
                    "Obs": int(len(series)),
                    "Start": (
                        panel.index.min()
                        .date()
                        .isoformat()
                    ),
                    "End": (
                        panel.index.max()
                        .date()
                        .isoformat()
                    ),
                    "Ann. Arithmetic Mean": float(
                        PERIODS_PER_YEAR
                        * series.mean()
                    ),
                    "Ann. Geometric Return": (
                        geometric_return
                    ),
                    "Ann. Vol": float(
                        np.sqrt(PERIODS_PER_YEAR)
                        * series.std(ddof=1)
                    ),
                    "MV CEQ Ann.": (
                        mv_ceq_annualized(
                            series,
                            gamma,
                        )
                    ),
                    "CRRA CE Ann.": (
                        crra_ce_annualized(
                            series,
                            gamma,
                        )
                    ),
                    "Min Monthly Return": float(
                        series.min()
                    ),
                    "CRRA Domain Valid": (
                        gross_domain_valid
                    ),
                }
            )

    return pd.DataFrame(rows)


def _moving_block_indices(
    sample_size: int,
    block_length: int,
    rng: np.random.Generator,
) -> np.ndarray:
    """
    Create moving-block bootstrap indices.

    Blocks preserve part of the serial dependence
    present in monthly financial returns.
    """
    block_length = max(
        1,
        min(
            int(block_length),
            sample_size,
        ),
    )

    number_of_blocks = int(
        np.ceil(
            sample_size / block_length
        )
    )

    maximum_start = (
        sample_size - block_length
    )

    starts = rng.integers(
        0,
        maximum_start + 1,
        size=number_of_blocks,
    )

    indices = np.concatenate(
        [
            np.arange(
                start,
                start + block_length,
            )
            for start in starts
        ]
    )

    return indices[:sample_size]


def bootstrap_welfare_differences(
    returns: pd.DataFrame,
    benchmark: str,
    gammas: Iterable[float] = (
        1.0,
        3.0,
        5.0,
        10.0,
    ),
    n_bootstrap: int = 2000,
    block_length: int = 6,
    seed: int = 42,
) -> pd.DataFrame:
    """
    Paired moving-block bootstrap of welfare differences
    between every strategy and a benchmark.
    """
    panel = clean_return_panel(returns)

    if benchmark not in panel.columns:
        raise KeyError(
            f"Benchmark not found: {benchmark}"
        )

    gammas = tuple(
        float(gamma)
        for gamma in gammas
    )

    strategies = list(panel.columns)

    rng = np.random.default_rng(seed)

    mv_draws = {
        (strategy, gamma): np.full(
            n_bootstrap,
            np.nan,
        )
        for strategy in strategies
        for gamma in gammas
    }

    crra_draws = {
        (strategy, gamma): np.full(
            n_bootstrap,
            np.nan,
        )
        for strategy in strategies
        for gamma in gammas
    }

    for bootstrap_id in range(
        n_bootstrap
    ):
        sample_indices = (
            _moving_block_indices(
                sample_size=len(panel),
                block_length=block_length,
                rng=rng,
            )
        )

        sample = panel.iloc[
            sample_indices
        ]

        for gamma in gammas:
            benchmark_mv = (
                mv_ceq_annualized(
                    sample[benchmark],
                    gamma,
                )
            )

            benchmark_crra = (
                crra_ce_annualized(
                    sample[benchmark],
                    gamma,
                )
            )

            for strategy in strategies:
                strategy_mv = (
                    mv_ceq_annualized(
                        sample[strategy],
                        gamma,
                    )
                )

                strategy_crra = (
                    crra_ce_annualized(
                        sample[strategy],
                        gamma,
                    )
                )

                mv_draws[
                    (strategy, gamma)
                ][bootstrap_id] = (
                    strategy_mv
                    - benchmark_mv
                )

                crra_draws[
                    (strategy, gamma)
                ][bootstrap_id] = (
                    strategy_crra
                    - benchmark_crra
                )

    rows: list[dict[str, object]] = []

    for gamma in gammas:
        benchmark_mv_point = (
            mv_ceq_annualized(
                panel[benchmark],
                gamma,
            )
        )

        benchmark_crra_point = (
            crra_ce_annualized(
                panel[benchmark],
                gamma,
            )
        )

        for strategy in strategies:
            mv_values = mv_draws[
                (strategy, gamma)
            ]

            crra_values = crra_draws[
                (strategy, gamma)
            ]

            valid_crra_values = (
                crra_values[
                    np.isfinite(
                        crra_values
                    )
                ]
            )

            mv_low, mv_high = (
                np.nanquantile(
                    mv_values,
                    [0.025, 0.975],
                )
            )

            if valid_crra_values.size:
                crra_low, crra_high = (
                    np.quantile(
                        valid_crra_values,
                        [0.025, 0.975],
                    )
                )

                crra_probability = float(
                    np.mean(
                        valid_crra_values
                        <= 0.0
                    )
                )

            else:
                crra_low = np.nan
                crra_high = np.nan
                crra_probability = np.nan

            strategy_mv_point = (
                mv_ceq_annualized(
                    panel[strategy],
                    gamma,
                )
            )

            strategy_crra_point = (
                crra_ce_annualized(
                    panel[strategy],
                    gamma,
                )
            )

            rows.append(
                {
                    "Strategy": strategy,
                    "Gamma": gamma,
                    "Benchmark": benchmark,

                    "Delta MV CEQ Ann.": (
                        strategy_mv_point
                        - benchmark_mv_point
                    ),

                    "Delta MV CEQ CI Low": (
                        float(mv_low)
                    ),

                    "Delta MV CEQ CI High": (
                        float(mv_high)
                    ),

                    "Delta MV CEQ Positive": bool(
                        mv_low > 0.0
                    ),

                    "Delta CRRA CE Ann.": (
                        strategy_crra_point
                        - benchmark_crra_point
                    ),

                    "Delta CRRA CE CI Low": (
                        float(crra_low)
                    ),

                    "Delta CRRA CE CI High": (
                        float(crra_high)
                    ),

                    "Delta CRRA CE Positive": (
                        bool(crra_low > 0.0)
                        if np.isfinite(crra_low)
                        else False
                    ),

                    "Bootstrap P(Delta MV <= 0)": float(
                        np.mean(
                            mv_values <= 0.0
                        )
                    ),

                    "Bootstrap P(Delta CRRA <= 0)": (
                        crra_probability
                    ),
                }
            )

    return pd.DataFrame(rows)
