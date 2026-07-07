from __future__ import annotations

import logging
import warnings
from dataclasses import dataclass

import numpy as np
import pandas as pd
import statsmodels.api as sm
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class RSMBacktestConfig:
    n_regimes: int = 2
    train_window: int = 72
    maxiter: int = 300
    em_iter: int = 10
    normal_equity_weight: float = 0.80
    stress_equity_weight: float = 0.20
    transaction_cost_bps: float = 10.0


def _extract_filtered_probabilities(result, train_index: pd.Index, n_regimes: int) -> pd.DataFrame:
    """
    Robust extraction of filtered marginal probabilities from statsmodels.
    """
    probs = result.filtered_marginal_probabilities

    if isinstance(probs, pd.DataFrame):
        arr = probs.values
    else:
        arr = np.asarray(probs)

    if arr.ndim != 2:
        raise ValueError(f"Unexpected probability array shape: {arr.shape}")

    if arr.shape[0] == n_regimes and arr.shape[1] != n_regimes:
        arr = arr.T

    if arr.shape[1] != n_regimes:
        raise ValueError(f"Could not orient probability array. Shape: {arr.shape}")

    return pd.DataFrame(
        arr,
        index=train_index[-arr.shape[0]:],
        columns=[f"state_{i}" for i in range(n_regimes)],
    )


def _fit_rsm_model(
    train: pd.DataFrame,
    feature_columns: list[str],
    config: RSMBacktestConfig,
):
    """
    Fits a Markov-switching regression.

    Endogenous variable:
        monthly equity return

    Exogenous variables:
        selected features such as log realized variance and log VRP.

    The model is used as a regime detector. Allocation is based on filtered
    regime probabilities at the end of the training sample.
    """
    y = train["equity_ret"].astype(float).values.reshape(-1, 1)

    y_scaler = StandardScaler()
    y_scaled = y_scaler.fit_transform(y).ravel()

    x_scaled = None

    if feature_columns:
        x = train[feature_columns].astype(float).values
        x_scaler = StandardScaler()
        x_scaled = x_scaler.fit_transform(x)
        switching_exog = [True] * len(feature_columns)
    else:
        switching_exog = False

    model = sm.tsa.MarkovRegression(
        endog=y_scaled,
        k_regimes=config.n_regimes,
        trend="c",
        exog=x_scaled,
        switching_trend=True,
        switching_exog=switching_exog,
        switching_variance=True,
    )

    sm_logger = logging.getLogger("statsmodels")
    previous_level = sm_logger.level
    sm_logger.setLevel(logging.ERROR)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = model.fit(
                disp=False,
                maxiter=config.maxiter,
                em_iter=config.em_iter,
            )
    finally:
        sm_logger.setLevel(previous_level)

    return result


def _identify_stress_state_from_probabilities(
    train: pd.DataFrame,
    filtered_probs: pd.DataFrame,
) -> int:
    """
    Identifies the stress regime as the state with highest average realized variance.
    """
    states = filtered_probs.idxmax(axis=1).str.replace("state_", "").astype(int)

    temp = train.reindex(filtered_probs.index).copy()
    temp["rsm_state"] = states.values

    state_stats = temp.groupby("rsm_state").agg(
        avg_rv=("rv_ann", "mean"),
        avg_return=("equity_ret", "mean"),
        obs=("rv_ann", "count"),
    )

    stress_state = int(state_stats["avg_rv"].idxmax())
    return stress_state


def _allocation_from_stress_probability(
    stress_probability: float,
    config: RSMBacktestConfig,
) -> tuple[float, float]:
    p_stress = float(np.clip(stress_probability, 0.0, 1.0))

    equity_weight = (
        config.normal_equity_weight * (1.0 - p_stress)
        + config.stress_equity_weight * p_stress
    )

    equity_weight = float(np.clip(equity_weight, 0.0, 1.0))
    bond_weight = 1.0 - equity_weight

    return equity_weight, bond_weight


def run_rolling_rsm_backtest(
    monthly: pd.DataFrame,
    feature_columns: list[str],
    strategy_name: str,
    config: RSMBacktestConfig | None = None,
) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """
    Rolling out-of-sample RSM allocation backtest.

    At each date t:
    - estimate the Markov regression using data up to t;
    - extract filtered regime probabilities at t;
    - allocate for t+1;
    - record next-period portfolio return.
    """
    if config is None:
        config = RSMBacktestConfig()

    required_columns = list(set(["equity_ret", "bond_ret", "rv_ann"] + feature_columns))
    data = monthly[required_columns].dropna().copy()

    if data.shape[0] <= config.train_window + 5:
        raise ValueError(
            f"Not enough observations for RSM backtest. "
            f"Need more than {config.train_window + 5}, got {data.shape[0]}."
        )

    returns = []
    turnovers = []
    records = []

    previous_target_weights = None
    cost_rate = config.transaction_cost_bps / 10_000.0

    for i in range(config.train_window, data.shape[0] - 1):
        train = data.iloc[: i + 1].copy()
        next_row = data.iloc[i + 1]
        next_date = data.index[i + 1]

        try:
            result = _fit_rsm_model(
                train=train,
                feature_columns=feature_columns,
                config=config,
            )

            filtered_probs = _extract_filtered_probabilities(
                result=result,
                train_index=train.index,
                n_regimes=config.n_regimes,
            )

            stress_state = _identify_stress_state_from_probabilities(
                train=train,
                filtered_probs=filtered_probs,
            )

            current_probs = filtered_probs.iloc[-1]
            stress_probability = float(current_probs[f"state_{stress_state}"])

            equity_weight, bond_weight = _allocation_from_stress_probability(
                stress_probability,
                config,
            )

            target_weights = pd.Series(
                {
                    "equity_ret": equity_weight,
                    "bond_ret": bond_weight,
                },
                dtype=float,
            )

            if previous_target_weights is None:
                turnover = float(target_weights.abs().sum())
            else:
                turnover = float((target_weights - previous_target_weights).abs().sum())

            gross_return = (
                target_weights["equity_ret"] * next_row["equity_ret"]
                + target_weights["bond_ret"] * next_row["bond_ret"]
            )

            net_return = float(gross_return - cost_rate * turnover)

            previous_target_weights = target_weights.copy()

            returns.append((next_date, net_return))
            turnovers.append((next_date, turnover))

            records.append(
                {
                    "date": next_date,
                    "strategy": strategy_name,
                    "stress_state": stress_state,
                    "stress_probability": stress_probability,
                    "state_0_probability": float(current_probs["state_0"]),
                    "state_1_probability": float(current_probs["state_1"]),
                    "equity_weight": equity_weight,
                    "bond_weight": bond_weight,
                    "turnover": turnover,
                    "gross_return": float(gross_return),
                    "net_return": net_return,
                    "train_obs": int(train.shape[0]),
                    "llf": float(result.llf),
                    "aic": float(result.aic),
                    "bic": float(result.bic),
                    "converged": bool(result.mle_retvals.get("converged", False)),
                }
            )

        except Exception as exc:
            records.append(
                {
                    "date": next_date,
                    "strategy": strategy_name,
                    "stress_state": np.nan,
                    "stress_probability": np.nan,
                    "state_0_probability": np.nan,
                    "state_1_probability": np.nan,
                    "equity_weight": np.nan,
                    "bond_weight": np.nan,
                    "turnover": np.nan,
                    "gross_return": np.nan,
                    "net_return": np.nan,
                    "train_obs": int(train.shape[0]),
                    "error": f"{type(exc).__name__}: {exc}",
                }
            )

    ret_series = pd.Series(
        data=[x[1] for x in returns],
        index=[x[0] for x in returns],
        name=strategy_name,
    )

    turnover_series = pd.Series(
        data=[x[1] for x in turnovers],
        index=[x[0] for x in turnovers],
        name=strategy_name,
    )

    diagnostics = pd.DataFrame(records)

    if not diagnostics.empty and "date" in diagnostics.columns:
        diagnostics = diagnostics.set_index("date")

    return ret_series, turnover_series, diagnostics


def build_rsm_strategy_set(
    monthly: pd.DataFrame,
    config: RSMBacktestConfig | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, pd.DataFrame]]:
    """
    Selected RSM specifications.
    """
    if config is None:
        config = RSMBacktestConfig()

    strategy_specs = {
        "RSM Returns Only": [],
        "RSM RV": ["log_rv_ann"],
        "RSM RV + Raw VRP": ["log_rv_ann", "vrp_proxy"],
        "RSM RV + Log VRP": ["log_rv_ann", "log_iv_rv"],
    }

    strategy_returns = {}
    strategy_turnovers = {}
    diagnostics = {}

    for strategy_name, features in strategy_specs.items():
        print(f"\nRunning {strategy_name} with features: {features}")

        ret, turn, diag = run_rolling_rsm_backtest(
            monthly=monthly,
            feature_columns=features,
            strategy_name=strategy_name,
            config=config,
        )

        strategy_returns[strategy_name] = ret
        strategy_turnovers[strategy_name] = turn
        diagnostics[strategy_name] = diag

    returns_df = pd.DataFrame(strategy_returns)
    turnovers_df = pd.DataFrame(strategy_turnovers)

    return returns_df, turnovers_df, diagnostics