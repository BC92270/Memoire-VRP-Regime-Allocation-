from __future__ import annotations

from pathlib import Path

import pandas as pd

from src.ml_regime import (
    MLBacktestConfig,
    build_ml_strategy_set,
    summarize_ml_predictions,
)
from src.performance_metrics import (
    summarize_strategies,
)


TABLES_DIR = Path(
    "outputs/tables"
)

PROCESSED_DIR = Path(
    "data/processed"
)


def read_indexed_csv(
    path: Path,
) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )

    frame = pd.read_csv(
        path,
        index_col=0,
        parse_dates=True,
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

    frame.columns = [
        str(column).strip()
        for column in frame.columns
    ]

    return frame


def load_monthly_data(
    market: str,
) -> pd.DataFrame:
    path = (
        PROCESSED_DIR
        / f"{market}_monthly_rebalance.csv"
    )

    data = read_indexed_csv(
        path
    )

    required = {
        "rv_ann",
        "vrp_proxy",
        "log_rv_ann",
        "log_iv_ann",
        "log_iv_rv",
        "equity_ret",
        "bond_ret",
    }

    missing = sorted(
        required.difference(
            data.columns
        )
    )

    if missing:
        raise KeyError(
            f"{market.upper()} monthly "
            f"data missing: {missing}"
        )

    return data


def load_final_core_panels(
    market: str,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
]:
    returns_path = (
        TABLES_DIR
        / f"{market}_final_model_returns.csv"
    )

    turnovers_path = (
        TABLES_DIR
        / f"{market}_final_model_turnovers.csv"
    )

    returns = read_indexed_csv(
        returns_path
    )

    turnovers = read_indexed_csv(
        turnovers_path
    )

    common_columns = [
        column
        for column in returns.columns
        if column in turnovers.columns
    ]

    returns = returns[
        common_columns
    ]

    turnovers = turnovers[
        common_columns
    ]

    return (
        returns,
        turnovers,
    )


def add_model_group(
    summary: pd.DataFrame,
) -> pd.DataFrame:
    result = summary.copy()

    strategy_names = (
        result.index.astype(str)
    )

    groups = []

    for strategy in strategy_names:
        if strategy.startswith("ML "):
            groups.append(
                "Machine Learning"
            )

        elif strategy.startswith("HMM "):
            groups.append("HMM")

        elif strategy.startswith("RSM "):
            groups.append("RSM")

        elif "VRP Proxy" in strategy:
            groups.append(
                "Synthetic Direct VRP"
            )

        else:
            groups.append(
                "Benchmark"
            )

    result.insert(
        0,
        "Model Group",
        groups,
    )

    return result


def run_market(
    market: str,
) -> tuple[
    pd.DataFrame,
    pd.DataFrame,
]:
    data = load_monthly_data(
        market
    )

    config = MLBacktestConfig(
        estimation_window=72,
        return_stress_quantile=0.20,
        rv_stress_quantile=0.80,
        normal_equity_weight=0.80,
        stress_equity_weight=0.20,
        transaction_cost_bps=10.0,
        classification_threshold=0.50,
        random_state=(
            42
            if market == "us"
            else 84
        ),
    )

    (
        ml_returns,
        ml_turnovers,
        diagnostics,
    ) = build_ml_strategy_set(
        data=data,
        config=config,
    )

    prediction_summary = (
        summarize_ml_predictions(
            diagnostics
        )
    )

    prediction_summary.insert(
        0,
        "Market",
        market.upper(),
    )

    ml_performance = (
        summarize_strategies(
            ml_returns,
            ml_turnovers,
        )
    )

    ml_performance = add_model_group(
        ml_performance
    )

    (
        core_returns,
        core_turnovers,
    ) = load_final_core_panels(
        market
    )

    combined_returns = pd.concat(
        [
            core_returns,
            ml_returns,
        ],
        axis=1,
    )

    combined_returns = (
        combined_returns.loc[
            ~combined_returns
            .index
            .duplicated(
                keep="last"
            )
        ]
    )

    combined_returns = (
        combined_returns.reindex(
            ml_returns.index
        )
    )

    combined_returns = (
        combined_returns.dropna(
            how="any"
        )
    )

    combined_turnovers = pd.concat(
        [
            core_turnovers,
            ml_turnovers,
        ],
        axis=1,
    )

    combined_turnovers = (
        combined_turnovers.reindex(
            index=(
                combined_returns.index
            ),
            columns=(
                combined_returns.columns
            ),
        )
        .fillna(0.0)
    )

    combined_performance = (
        summarize_strategies(
            combined_returns,
            combined_turnovers,
        )
    )

    combined_performance = (
        add_model_group(
            combined_performance
        )
    )

    paths = {
        "ml_returns": (
            TABLES_DIR
            / f"{market}_ml_strategy_returns.csv"
        ),
        "ml_turnovers": (
            TABLES_DIR
            / f"{market}_ml_strategy_turnovers.csv"
        ),
        "diagnostics": (
            TABLES_DIR
            / f"{market}_ml_diagnostics.csv"
        ),
        "prediction": (
            TABLES_DIR
            / f"{market}_ml_prediction_summary.csv"
        ),
        "ml_performance": (
            TABLES_DIR
            / f"{market}_ml_performance_summary.csv"
        ),
        "combined_returns": (
            TABLES_DIR
            / f"{market}_ml_vs_core_returns.csv"
        ),
        "combined_turnovers": (
            TABLES_DIR
            / f"{market}_ml_vs_core_turnovers.csv"
        ),
        "combined_performance": (
            TABLES_DIR
            / (
                f"{market}_ml_vs_core_"
                "performance_summary.csv"
            )
        ),
    }

    ml_returns.to_csv(
        paths["ml_returns"],
        index_label="Date",
    )

    ml_turnovers.to_csv(
        paths["ml_turnovers"],
        index_label="Date",
    )

    diagnostics.to_csv(
        paths["diagnostics"],
        index=False,
    )

    prediction_summary.to_csv(
        paths["prediction"],
        index=False,
    )

    ml_performance.to_csv(
        paths["ml_performance"]
    )

    combined_returns.to_csv(
        paths["combined_returns"],
        index_label="Date",
    )

    combined_turnovers.to_csv(
        paths["combined_turnovers"],
        index_label="Date",
    )

    combined_performance.to_csv(
        paths["combined_performance"]
    )

    print("=" * 110)
    print(
        f"{market.upper()} — "
        "MVP 6 MACHINE LEARNING "
        "REGIME ALLOCATION"
    )
    print("=" * 110)

    print(
        "Raw monthly observations: "
        f"{len(data)}"
    )

    print(
        "ML out-of-sample observations: "
        f"{len(ml_returns)} "
        f"("
        f"{ml_returns.index.min().date()} "
        "-> "
        f"{ml_returns.index.max().date()}"
        ")"
    )

    print(
        f"ML strategies: "
        f"{len(ml_returns.columns)}"
    )

    print()

    prediction_columns = [
        "Strategy",
        "ROC AUC",
        "PR AUC",
        "Brier Score",
        "Balanced Accuracy",
        "Recall",
        "Avg Equity Weight",
        "Avg Turnover",
        "Fit Success Rate",
    ]

    print(
        "PREDICTIVE PERFORMANCE"
    )

    print(
        prediction_summary[
            prediction_columns
        ]
        .sort_values(
            "Brier Score"
        )
        .to_string(
            index=False
        )
    )

    print()

    display_columns = [
        column
        for column in [
            "Model Group",
            "Ann. Return",
            "Ann. Vol",
            "Sharpe",
            "Sortino",
            "Max Drawdown",
            "CVaR 95",
            "Avg Turnover",
            "Obs",
        ]
        if column
        in combined_performance.columns
    ]

    print(
        "ECONOMIC PERFORMANCE — "
        "ML AND FINAL CORE MODELS"
    )

    if (
        "Sharpe"
        in combined_performance.columns
    ):
        display = (
            combined_performance
            .sort_values(
                "Sharpe",
                ascending=False,
            )
        )

    else:
        display = (
            combined_performance
        )

    print(
        display[
            display_columns
        ].to_string()
    )

    print()
    print("OUTPUTS")

    for (
        label,
        path,
    ) in paths.items():
        print(
            f"- {label}: {path}"
        )

    print()

    market_performance = (
        combined_performance
        .reset_index()
    )

    first_column = (
        market_performance
        .columns[0]
    )

    market_performance = (
        market_performance.rename(
            columns={
                first_column: "Strategy"
            }
        )
    )

    market_performance.insert(
        0,
        "Market",
        market.upper(),
    )

    return (
        prediction_summary,
        market_performance,
    )


def main() -> None:
    TABLES_DIR.mkdir(
        parents=True,
        exist_ok=True,
    )

    prediction_frames = []
    performance_frames = []

    for market in (
        "us",
        "eu",
    ):
        (
            prediction,
            performance,
        ) = run_market(
            market
        )

        prediction_frames.append(
            prediction
        )

        performance_frames.append(
            performance
        )

    cross_prediction = pd.concat(
        prediction_frames,
        ignore_index=True,
    )

    cross_performance = pd.concat(
        performance_frames,
        ignore_index=True,
    )

    cross_prediction_path = (
        TABLES_DIR
        / (
            "cross_market_ml_"
            "prediction_summary.csv"
        )
    )

    cross_performance_path = (
        TABLES_DIR
        / (
            "cross_market_ml_vs_core_"
            "performance.csv"
        )
    )

    cross_prediction.to_csv(
        cross_prediction_path,
        index=False,
    )

    cross_performance.to_csv(
        cross_performance_path,
        index=False,
    )

    print("=" * 110)
    print(
        "MVP 6 MACHINE LEARNING "
        "REGIME ALLOCATION COMPLETE"
    )
    print("=" * 110)

    print(
        "Cross-market prediction: "
        f"{cross_prediction_path}"
    )

    print(
        "Cross-market performance: "
        f"{cross_performance_path}"
    )


if __name__ == "__main__":
    main()
