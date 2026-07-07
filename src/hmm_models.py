from __future__ import annotations

from dataclasses import dataclass

import numpy as np
import pandas as pd
import logging
import warnings
from hmmlearn.hmm import GaussianHMM
from sklearn.preprocessing import StandardScaler


@dataclass(frozen=True)
class HMMBacktestConfig:
    n_components: int = 2
    train_window: int = 72
    covariance_type: str = "diag"
    n_iter: int = 300
    tol: float = 1e-3
    random_state: int = 42
    normal_equity_weight: float = 0.80
    stress_equity_weight: float = 0.20
    transaction_cost_bps: float = 10.0


def _fit_hmm_model(
    train_features: pd.DataFrame,
    config: HMMBacktestConfig,
) -> tuple[GaussianHMM, StandardScaler, np.ndarray]:
    """
    Fits a Gaussian HMM on standardized training features.
    Uses a parsimonious configuration to improve rolling stability.
    """
    scaler = StandardScaler()
    x_train = scaler.fit_transform(train_features.values)

    model = GaussianHMM(
        n_components=config.n_components,
        covariance_type=config.covariance_type,
        n_iter=config.n_iter,
        tol=config.tol,
        random_state=config.random_state,
        min_covar=1e-5,
        verbose=False,
    )

    hmm_logger = logging.getLogger("hmmlearn")
    previous_level = hmm_logger.level
    hmm_logger.setLevel(logging.ERROR)

    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            model.fit(x_train)
    finally:
        hmm_logger.setLevel(previous_level)

    hidden_states = model.predict(x_train)

    return model, scaler, hidden_states

def _identify_stress_state(
    train_df: pd.DataFrame,
    hidden_states: np.ndarray,
) -> int:
    """
    Identifies the stress state as the state with the highest average realized variance.
    This avoids relying on arbitrary HMM state labels.
    """
    temp = train_df.copy()
    temp["hmm_state"] = hidden_states

    state_stats = temp.groupby("hmm_state").agg(
        avg_rv=("rv_ann", "mean"),
        avg_equity_ret=("equity_ret", "mean"),
        obs=("rv_ann", "count"),
    )

    stress_state = int(state_stats["avg_rv"].idxmax())
    return stress_state


def _compute_probability_weighted_allocation(
    stress_probability: float,
    config: HMMBacktestConfig,
) -> tuple[float, float]:
    """
    Converts stress probability into equity/bond weights.

    If stress probability is high, equity weight falls toward stress_equity_weight.
    If stress probability is low, equity weight moves toward normal_equity_weight.
    """
    p_stress = float(np.clip(stress_probability, 0.0, 1.0))

    equity_weight = (
        config.normal_equity_weight * (1.0 - p_stress)
        + config.stress_equity_weight * p_stress
    )
    equity_weight = float(np.clip(equity_weight, 0.0, 1.0))

    bond_weight = 1.0 - equity_weight

    return equity_weight, bond_weight


def run_rolling_hmm_backtest(
    monthly: pd.DataFrame,
    feature_columns: list[str],
    strategy_name: str,
    config: HMMBacktestConfig | None = None,
) -> tuple[pd.Series, pd.Series, pd.DataFrame]:
    """
    Runs a rolling out-of-sample HMM allocation backtest.

    At date t:
    - train HMM on data available up to t;
    - infer filtered regime probabilities for date t;
    - allocate for t+1;
    - realize portfolio return at t+1.

    This avoids using future features to decide current portfolio weights.
    """
    if config is None:
        config = HMMBacktestConfig()

    required_columns = list(set(feature_columns + ["equity_ret", "bond_ret", "rv_ann"]))
    data = monthly[required_columns].dropna().copy()

    if data.shape[0] <= config.train_window + 5:
        raise ValueError(
            f"Not enough observations for HMM backtest. "
            f"Need more than {config.train_window + 5}, got {data.shape[0]}."
        )

    returns = []
    turnovers = []
    records = []

    previous_target_weights = None
    cost_rate = config.transaction_cost_bps / 10_000.0

    for i in range(config.train_window, data.shape[0] - 1):
        train = data.iloc[: i + 1].copy()
        current_features = data.iloc[[i]][feature_columns]
        next_row = data.iloc[i + 1]
        next_date = data.index[i + 1]

        train_features = train[feature_columns]

        try:
            model, scaler, hidden_states = _fit_hmm_model(train_features, config)
            stress_state = _identify_stress_state(train, hidden_states)

            x_train = scaler.transform(train_features.values)
            state_probabilities = model.predict_proba(x_train)
            current_proba = state_probabilities[-1]
            stress_probability = float(current_proba[stress_state])

            equity_weight, bond_weight = _compute_probability_weighted_allocation(
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
                    "equity_weight": equity_weight,
                    "bond_weight": bond_weight,
                    "turnover": turnover,
                    "gross_return": float(gross_return),
                    "net_return": net_return,
                    "train_obs": int(train.shape[0]),
                }
            )

        except Exception as exc:
            records.append(
                {
                    "date": next_date,
                    "strategy": strategy_name,
                    "stress_state": np.nan,
                    "stress_probability": np.nan,
                    "equity_weight": np.nan,
                    "bond_weight": np.nan,
                    "turnover": np.nan,
                    "gross_return": np.nan,
                    "net_return": np.nan,
                    "train_obs": int(train.shape[0]),
                    "error": f"{type(exc).__name__}: {exc}",
                    "state_0_probability": float(current_proba[0]),
                    "state_1_probability": float(current_proba[1]) if len(current_proba) > 1 else np.nan,
                    "converged": bool(getattr(model.monitor_, "converged", False)),
                    "log_likelihood": float(model.score(x_train)),
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


def build_hmm_strategy_set(
    monthly: pd.DataFrame,
    config: HMMBacktestConfig | None = None,
) -> tuple[pd.DataFrame, pd.DataFrame, dict[str, pd.DataFrame]]:
    """
    Builds two HMM strategies:
    - HMM without VRP
    - HMM with VRP as signal
    """
    if config is None:
        config = HMMBacktestConfig()

    strategy_specs = {
        "HMM without VRP": ["equity_ret", "rv_ann"],
        "HMM with VRP Signal": ["equity_ret", "rv_ann", "vrp_proxy"],
    }

    strategy_returns = {}
    strategy_turnovers = {}
    diagnostics = {}

    for strategy_name, features in strategy_specs.items():
        ret, turn, diag = run_rolling_hmm_backtest(
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