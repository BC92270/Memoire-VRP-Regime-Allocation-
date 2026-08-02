from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import numpy as np
import pandas as pd
from sklearn.ensemble import (
    HistGradientBoostingClassifier,
    RandomForestClassifier,
)
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    balanced_accuracy_score,
    brier_score_loss,
    log_loss,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


BASE_FEATURES = (
    "equity_ret",
    "bond_ret",
    "log_rv_ann",
    "log_iv_ann",
)

VRP_FEATURES = BASE_FEATURES + (
    "vrp_proxy",
    "log_iv_rv",
)


@dataclass(frozen=True)
class MLBacktestConfig:
    estimation_window: int = 72
    return_stress_quantile: float = 0.20
    rv_stress_quantile: float = 0.80
    normal_equity_weight: float = 0.80
    stress_equity_weight: float = 0.20
    transaction_cost_bps: float = 10.0
    classification_threshold: float = 0.50
    random_state: int = 42


def _validate_input(
    data: pd.DataFrame,
    feature_columns: tuple[str, ...],
    config: MLBacktestConfig,
) -> pd.DataFrame:
    required = set(feature_columns) | {
        "equity_ret",
        "bond_ret",
        "rv_ann",
    }

    missing = sorted(
        required.difference(data.columns)
    )

    if missing:
        raise KeyError(
            f"Missing required columns: {missing}"
        )

    frame = data.copy()

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

    if (
        len(frame)
        < config.estimation_window + 2
    ):
        raise ValueError(
            "Insufficient observations for "
            "the requested rolling window: "
            f"{len(frame)} rows for a "
            f"{config.estimation_window}-month "
            "window."
        )

    relevant = list(
        dict.fromkeys(
            [
                *feature_columns,
                "equity_ret",
                "bond_ret",
                "rv_ann",
            ]
        )
    )

    if frame[relevant].isna().any().any():
        counts = (
            frame[relevant]
            .isna()
            .sum()
        )

        counts = counts[
            counts.gt(0)
        ].to_dict()

        raise ValueError(
            "Missing values in required "
            f"ML inputs: {counts}"
        )

    return frame


def _make_estimator(
    model_name: str,
    random_state: int,
) -> Any:
    if model_name == "Logistic":
        return Pipeline(
            steps=[
                (
                    "scaler",
                    StandardScaler(),
                ),
                (
                    "classifier",
                    LogisticRegression(
                        C=0.50,
                        class_weight="balanced",
                        solver="lbfgs",
                        max_iter=2_000,
                    ),
                ),
            ]
        )

    if model_name == "Random Forest":
        return RandomForestClassifier(
            n_estimators=200,
            max_depth=3,
            min_samples_leaf=8,
            max_features="sqrt",
            class_weight=(
                "balanced_subsample"
            ),
            bootstrap=True,
            n_jobs=-1,
            random_state=random_state,
        )

    if model_name == "Gradient Boosting":
        return (
            HistGradientBoostingClassifier(
                learning_rate=0.05,
                max_iter=100,
                max_leaf_nodes=7,
                max_depth=2,
                min_samples_leaf=10,
                l2_regularization=1.0,
                class_weight="balanced",
                early_stopping=False,
                random_state=random_state,
            )
        )

    raise ValueError(
        f"Unsupported model: {model_name}"
    )


def _positive_class_probability(
    estimator: Any,
    x_pred: pd.DataFrame,
    fallback_probability: float,
) -> float:
    probabilities = (
        estimator.predict_proba(x_pred)
    )

    classes = np.asarray(
        estimator.classes_
    )

    positive_positions = np.flatnonzero(
        classes == 1
    )

    if positive_positions.size == 0:
        return float(
            np.clip(
                fallback_probability,
                0.0,
                1.0,
            )
        )

    probability = float(
        probabilities[
            0,
            positive_positions[0],
        ]
    )

    return float(
        np.clip(
            probability,
            0.0,
            1.0,
        )
    )


def _allocation_from_probability(
    stress_probability: float,
    config: MLBacktestConfig,
) -> tuple[float, float]:
    p_stress = float(
        np.clip(
            stress_probability,
            0.0,
            1.0,
        )
    )

    equity_weight = (
        config.normal_equity_weight
        * (1.0 - p_stress)
        + config.stress_equity_weight
        * p_stress
    )

    equity_weight = float(
        np.clip(
            equity_weight,
            0.0,
            1.0,
        )
    )

    bond_weight = (
        1.0 - equity_weight
    )

    return (
        equity_weight,
        bond_weight,
    )


def run_rolling_ml_backtest(
    data: pd.DataFrame,
    strategy_name: str,
    model_name: str,
    feature_columns: tuple[str, ...],
    config: MLBacktestConfig | None = None,
) -> tuple[
    pd.Series,
    pd.Series,
    pd.DataFrame,
]:
    """
    Strict rolling one-step-ahead classification.

    At signal date t:
    - features dated t are observable;
    - training pairs end at t-1;
    - each training label uses the outcome at s+1;
    - thresholds use only the rolling training window;
    - the probability at t sets weights for t+1.
    """
    config = (
        config
        or MLBacktestConfig()
    )

    frame = _validate_input(
        data=data,
        feature_columns=feature_columns,
        config=config,
    )

    next_equity_return = (
        frame["equity_ret"].shift(-1)
    )

    next_realized_variance = (
        frame["rv_ann"].shift(-1)
    )

    returns: list[
        tuple[pd.Timestamp, float]
    ] = []

    turnovers: list[
        tuple[pd.Timestamp, float]
    ] = []

    diagnostics: list[
        dict[str, object]
    ] = []

    previous_target_weights: (
        pd.Series | None
    ) = None

    cost_rate = (
        config.transaction_cost_bps
        / 10_000.0
    )

    for signal_position in range(
        config.estimation_window,
        len(frame) - 1,
    ):
        training_start = (
            signal_position
            - config.estimation_window
        )

        training_positions = np.arange(
            training_start,
            signal_position,
        )

        signal_date = (
            frame.index[signal_position]
        )

        next_date = (
            frame.index[
                signal_position + 1
            ]
        )

        x_train = frame.iloc[
            training_positions
        ][list(feature_columns)]

        x_pred = frame.iloc[
            [signal_position]
        ][list(feature_columns)]

        train_next_equity = (
            next_equity_return.iloc[
                training_positions
            ]
        )

        train_next_rv = (
            next_realized_variance.iloc[
                training_positions
            ]
        )

        return_threshold = float(
            train_next_equity.quantile(
                config.return_stress_quantile
            )
        )

        rv_threshold = float(
            train_next_rv.quantile(
                config.rv_stress_quantile
            )
        )

        y_train = (
            train_next_equity.le(
                return_threshold
            )
            | train_next_rv.ge(
                rv_threshold
            )
        ).astype(int)

        train_stress_rate = float(
            y_train.mean()
        )

        fit_status = "fitted"
        error_message = ""

        try:
            if y_train.nunique() < 2:
                stress_probability = (
                    train_stress_rate
                )

                fit_status = (
                    "single_class_fallback"
                )

            else:
                estimator = _make_estimator(
                    model_name=model_name,
                    random_state=(
                        config.random_state
                        + signal_position
                    ),
                )

                estimator.fit(
                    x_train,
                    y_train,
                )

                stress_probability = (
                    _positive_class_probability(
                        estimator=estimator,
                        x_pred=x_pred,
                        fallback_probability=(
                            train_stress_rate
                        ),
                    )
                )

        except Exception as exc:
            stress_probability = (
                train_stress_rate
            )

            fit_status = (
                "fit_error_fallback"
            )

            error_message = (
                f"{type(exc).__name__}: "
                f"{exc}"
            )

        (
            equity_weight,
            bond_weight,
        ) = _allocation_from_probability(
            stress_probability=(
                stress_probability
            ),
            config=config,
        )

        target_weights = pd.Series(
            {
                "equity_ret": (
                    equity_weight
                ),
                "bond_ret": (
                    bond_weight
                ),
            },
            dtype=float,
        )

        if (
            previous_target_weights
            is None
        ):
            turnover = float(
                target_weights
                .abs()
                .sum()
            )

        else:
            turnover = float(
                (
                    target_weights
                    - previous_target_weights
                )
                .abs()
                .sum()
            )

        next_asset_returns = (
            frame.loc[
                next_date,
                [
                    "equity_ret",
                    "bond_ret",
                ],
            ].astype(float)
        )

        gross_return = float(
            (
                target_weights
                * next_asset_returns
            ).sum()
        )

        net_return = float(
            gross_return
            - cost_rate * turnover
        )

        actual_stress = int(
            (
                frame.at[
                    next_date,
                    "equity_ret",
                ]
                <= return_threshold
            )
            or (
                frame.at[
                    next_date,
                    "rv_ann",
                ]
                >= rv_threshold
            )
        )

        predicted_stress = int(
            stress_probability
            >= config.classification_threshold
        )

        returns.append(
            (
                next_date,
                net_return,
            )
        )

        turnovers.append(
            (
                next_date,
                turnover,
            )
        )

        diagnostics.append(
            {
                "date": next_date,
                "signal_date": signal_date,
                "strategy": strategy_name,
                "model": model_name,
                "features": (
                    " + ".join(
                        feature_columns
                    )
                ),
                "feature_count": (
                    len(feature_columns)
                ),
                "stress_probability": (
                    stress_probability
                ),
                "predicted_stress": (
                    predicted_stress
                ),
                "actual_stress": (
                    actual_stress
                ),
                "train_stress_rate": (
                    train_stress_rate
                ),
                "return_threshold": (
                    return_threshold
                ),
                "rv_threshold": (
                    rv_threshold
                ),
                "equity_weight": (
                    equity_weight
                ),
                "bond_weight": (
                    bond_weight
                ),
                "turnover": turnover,
                "gross_return": (
                    gross_return
                ),
                "net_return": (
                    net_return
                ),
                "next_equity_return": float(
                    frame.at[
                        next_date,
                        "equity_ret",
                    ]
                ),
                "next_realized_variance": float(
                    frame.at[
                        next_date,
                        "rv_ann",
                    ]
                ),
                "train_obs": int(
                    len(x_train)
                ),
                "fit_status": (
                    fit_status
                ),
                "error_message": (
                    error_message
                ),
            }
        )

        previous_target_weights = (
            target_weights
        )

    return_series = pd.Series(
        data=[
            value
            for _, value in returns
        ],
        index=[
            date
            for date, _ in returns
        ],
        name=strategy_name,
        dtype=float,
    )

    turnover_series = pd.Series(
        data=[
            value
            for _, value in turnovers
        ],
        index=[
            date
            for date, _ in turnovers
        ],
        name=strategy_name,
        dtype=float,
    )

    diagnostic_frame = pd.DataFrame(
        diagnostics
    )

    return (
        return_series,
        turnover_series,
        diagnostic_frame,
    )


def default_ml_strategy_specs(
) -> dict[
    str,
    tuple[
        str,
        tuple[str, ...],
    ],
]:
    return {
        "ML Logistic Base": (
            "Logistic",
            BASE_FEATURES,
        ),
        "ML Logistic + VRP": (
            "Logistic",
            VRP_FEATURES,
        ),
        "ML Random Forest Base": (
            "Random Forest",
            BASE_FEATURES,
        ),
        "ML Random Forest + VRP": (
            "Random Forest",
            VRP_FEATURES,
        ),
        "ML Gradient Boosting Base": (
            "Gradient Boosting",
            BASE_FEATURES,
        ),
        "ML Gradient Boosting + VRP": (
            "Gradient Boosting",
            VRP_FEATURES,
        ),
    }


def build_ml_strategy_set(
    data: pd.DataFrame,
    config: MLBacktestConfig | None = None,
    strategy_specs: (
        dict[
            str,
            tuple[
                str,
                tuple[str, ...],
            ],
        ]
        | None
    ) = None,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
    pd.DataFrame,
]:
    config = (
        config
        or MLBacktestConfig()
    )

    strategy_specs = (
        strategy_specs
        or default_ml_strategy_specs()
    )

    strategy_returns: dict[
        str,
        pd.Series,
    ] = {}

    strategy_turnovers: dict[
        str,
        pd.Series,
    ] = {}

    diagnostic_frames: list[
        pd.DataFrame
    ] = []

    for (
        strategy_name,
        (
            model_name,
            feature_columns,
        ),
    ) in strategy_specs.items():
        (
            returns,
            turnovers,
            diagnostics,
        ) = run_rolling_ml_backtest(
            data=data,
            strategy_name=strategy_name,
            model_name=model_name,
            feature_columns=(
                feature_columns
            ),
            config=config,
        )

        strategy_returns[
            strategy_name
        ] = returns

        strategy_turnovers[
            strategy_name
        ] = turnovers

        diagnostic_frames.append(
            diagnostics
        )

    returns_frame = pd.DataFrame(
        strategy_returns
    ).dropna(
        how="all"
    )

    turnovers_frame = pd.DataFrame(
        strategy_turnovers
    ).reindex(
        returns_frame.index
    )

    diagnostics_frame = pd.concat(
        diagnostic_frames,
        ignore_index=True,
    )

    return (
        returns_frame,
        turnovers_frame,
        diagnostics_frame,
    )


def summarize_ml_predictions(
    diagnostics: pd.DataFrame,
) -> pd.DataFrame:
    rows: list[
        dict[str, object]
    ] = []

    for (
        strategy,
        group,
    ) in diagnostics.groupby(
        "strategy",
        sort=True,
    ):
        valid = group.dropna(
            subset=[
                "actual_stress",
                "stress_probability",
            ]
        ).copy()

        y_true = (
            valid["actual_stress"]
            .astype(int)
            .to_numpy()
        )

        y_probability = np.clip(
            valid[
                "stress_probability"
            ]
            .astype(float)
            .to_numpy(),
            1e-8,
            1.0 - 1e-8,
        )

        y_pred = (
            y_probability >= 0.50
        ).astype(int)

        has_both_classes = (
            np.unique(y_true).size == 2
        )

        rows.append(
            {
                "Strategy": strategy,
                "Model": (
                    valid["model"].iloc[0]
                ),
                "Features": (
                    valid[
                        "features"
                    ].iloc[0]
                ),
                "Obs": int(len(valid)),
                "Actual Stress Rate": float(
                    np.mean(y_true)
                ),
                (
                    "Avg Predicted "
                    "Stress Probability"
                ): float(
                    np.mean(y_probability)
                ),
                "ROC AUC": (
                    float(
                        roc_auc_score(
                            y_true,
                            y_probability,
                        )
                    )
                    if has_both_classes
                    else np.nan
                ),
                "PR AUC": (
                    float(
                        average_precision_score(
                            y_true,
                            y_probability,
                        )
                    )
                    if has_both_classes
                    else np.nan
                ),
                "Brier Score": float(
                    brier_score_loss(
                        y_true,
                        y_probability,
                    )
                ),
                "Log Loss": float(
                    log_loss(
                        y_true,
                        y_probability,
                        labels=[0, 1],
                    )
                ),
                "Accuracy": float(
                    accuracy_score(
                        y_true,
                        y_pred,
                    )
                ),
                "Balanced Accuracy": float(
                    balanced_accuracy_score(
                        y_true,
                        y_pred,
                    )
                ),
                "Precision": float(
                    precision_score(
                        y_true,
                        y_pred,
                        zero_division=0,
                    )
                ),
                "Recall": float(
                    recall_score(
                        y_true,
                        y_pred,
                        zero_division=0,
                    )
                ),
                "Avg Equity Weight": float(
                    valid[
                        "equity_weight"
                    ].mean()
                ),
                "Avg Turnover": float(
                    valid[
                        "turnover"
                    ].mean()
                ),
                "Fit Success Rate": float(
                    valid[
                        "fit_status"
                    ]
                    .eq("fitted")
                    .mean()
                ),
                "Fit Error Count": int(
                    valid[
                        "fit_status"
                    ]
                    .eq(
                        "fit_error_fallback"
                    )
                    .sum()
                ),
            }
        )

    return (
        pd.DataFrame(rows)
        .sort_values(
            [
                "Brier Score",
                "ROC AUC",
            ],
            ascending=[
                True,
                False,
            ],
        )
        .reset_index(drop=True)
    )
