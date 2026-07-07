from __future__ import annotations

import pandas as pd

from src.config import OUTPUT_TABLES_DIR


METRIC_COLUMNS = [
    "Ann. Return",
    "Ann. Vol",
    "Sharpe",
    "Sortino",
    "Max Drawdown",
    "Calmar",
    "VaR 95",
    "CVaR 95",
    "Avg Turnover",
    "Obs",
]


MODEL_GROUPS = {
    "Benchmark": [
        "Buy-and-Hold Equity",
        "60/40",
        "1/N Equity-Bond",
    ],
    "US selected HMM": [
        "HMM RV + Log VRP (full)",
        "HMM RV + Log VRP (partial 0.25)",
    ],
    "EU HMM": [
        "HMM RV",
        "HMM RV + Log VRP",
    ],
    "RSM": [
        "RSM RV + Raw VRP",
        "RSM Returns Only",
        "RSM RV",
        "RSM RV + Log VRP",
    ],
}


def load_summary(market: str) -> pd.DataFrame:
    path = OUTPUT_TABLES_DIR / f"{market}_final_implementable_summary.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing final summary: {path}")

    df = pd.read_csv(path, index_col=0)

    missing = [col for col in METRIC_COLUMNS if col not in df.columns]
    if missing:
        raise ValueError(f"Missing columns in {path}: {missing}")

    df = df[METRIC_COLUMNS].copy()
    df.insert(0, "Market", market.upper())
    df.insert(1, "Strategy", df.index)

    return df.reset_index(drop=True)


def load_extended_summary(market: str) -> pd.DataFrame:
    path = OUTPUT_TABLES_DIR / f"{market}_final_extended_summary_with_synthetic_vrp.csv"

    if not path.exists():
        raise FileNotFoundError(f"Missing extended final summary: {path}")

    df = pd.read_csv(path, index_col=0)
    df = df[METRIC_COLUMNS].copy()
    df.insert(0, "Market", market.upper())
    df.insert(1, "Strategy", df.index)

    return df.reset_index(drop=True)


def assign_model_group(strategy: str) -> str:
    for group, names in MODEL_GROUPS.items():
        if strategy in names:
            return group
    return "Other"


def build_market_leaders(summary: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for market, sub in summary.groupby("Market"):
        sub = sub.copy()

        best_sharpe = sub.sort_values("Sharpe", ascending=False).iloc[0]
        best_drawdown = sub.sort_values("Max Drawdown", ascending=False).iloc[0]
        lowest_turnover = sub.sort_values("Avg Turnover", ascending=True).iloc[0]

        rows.append(
            {
                "Market": market,
                "Criterion": "Best Sharpe",
                "Strategy": best_sharpe["Strategy"],
                "Sharpe": best_sharpe["Sharpe"],
                "Max Drawdown": best_sharpe["Max Drawdown"],
                "Avg Turnover": best_sharpe["Avg Turnover"],
            }
        )

        rows.append(
            {
                "Market": market,
                "Criterion": "Best Max Drawdown",
                "Strategy": best_drawdown["Strategy"],
                "Sharpe": best_drawdown["Sharpe"],
                "Max Drawdown": best_drawdown["Max Drawdown"],
                "Avg Turnover": best_drawdown["Avg Turnover"],
            }
        )

        rows.append(
            {
                "Market": market,
                "Criterion": "Lowest Turnover",
                "Strategy": lowest_turnover["Strategy"],
                "Sharpe": lowest_turnover["Sharpe"],
                "Max Drawdown": lowest_turnover["Max Drawdown"],
                "Avg Turnover": lowest_turnover["Avg Turnover"],
            }
        )

    return pd.DataFrame(rows)


def build_key_strategy_comparison(summary: pd.DataFrame) -> pd.DataFrame:
    """
    Thesis-facing table with the most relevant models only.
    """
    selected_rows = []

    selections = {
        "US": [
            "Buy-and-Hold Equity",
            "60/40",
            "1/N Equity-Bond",
            "HMM RV + Log VRP (full)",
            "HMM RV + Log VRP (partial 0.25)",
            "RSM RV + Raw VRP",
        ],
        "EU": [
            "Buy-and-Hold Equity",
            "60/40",
            "1/N Equity-Bond",
            "HMM RV + Log VRP",
            "RSM Returns Only",
            "RSM RV + Raw VRP",
        ],
    }

    for market, strategies in selections.items():
        sub = summary[summary["Market"] == market].copy()

        for strategy in strategies:
            row = sub[sub["Strategy"] == strategy]

            if row.empty:
                continue

            selected_rows.append(row.iloc[0].to_dict())

    out = pd.DataFrame(selected_rows)
    out["Model Group"] = out["Strategy"].map(assign_model_group)

    ordered_cols = [
        "Market",
        "Model Group",
        "Strategy",
        "Ann. Return",
        "Ann. Vol",
        "Sharpe",
        "Sortino",
        "Max Drawdown",
        "Calmar",
        "VaR 95",
        "CVaR 95",
        "Avg Turnover",
        "Obs",
    ]

    return out[ordered_cols]


def build_synthetic_vrp_comparison(extended_summary: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for market, sub in extended_summary.groupby("Market"):
        candidates = sub[
            sub["Strategy"].isin(["Synthetic Pure VRP Proxy", "Pure VRP Proxy"])
        ]

        if candidates.empty:
            continue

        row = candidates.iloc[0].copy()
        rows.append(row)

    out = pd.DataFrame(rows)

    if out.empty:
        return out

    ordered_cols = [
        "Market",
        "Strategy",
        "Ann. Return",
        "Ann. Vol",
        "Sharpe",
        "Sortino",
        "Max Drawdown",
        "Calmar",
        "VaR 95",
        "CVaR 95",
        "Avg Turnover",
        "Obs",
    ]

    return out[ordered_cols]


def build_empirical_conclusions() -> pd.DataFrame:
    rows = [
        {
            "Theme": "US evidence",
            "Conclusion": (
                "In the US sample, VRP-enhanced HMM models are competitive with "
                "60/40 and 1/N benchmarks and improve maximum drawdown. The most "
                "defensible implementable specification is HMM RV + Log VRP with "
                "partial rebalancing."
            ),
        },
        {
            "Theme": "EU evidence",
            "Conclusion": (
                "In the European sample, regime-switching models do not outperform "
                "simple benchmarks. The VRP signal does not transfer robustly to "
                "EU allocation in the tested specifications."
            ),
        },
        {
            "Theme": "Pure VRP proxy",
            "Conclusion": (
                "The synthetic pure VRP proxy is extremely strong in the US but "
                "collapses in Europe. It should be treated as an exploratory proxy, "
                "not as a fully tradable variance swap strategy."
            ),
        },
        {
            "Theme": "Main thesis result",
            "Conclusion": (
                "VRP appears more useful as a regime-state variable for downside-risk "
                "management than as a universally robust standalone return engine."
            ),
        },
        {
            "Theme": "Methodological implication",
            "Conclusion": (
                "Simple equity-bond benchmarks remain difficult to beat. The economic "
                "value of regime-switching allocation depends strongly on market, "
                "feature transformation, turnover and implementation frictions."
            ),
        },
    ]

    return pd.DataFrame(rows)


def run_cross_market_report() -> None:
    us_summary = load_summary("us")
    eu_summary = load_summary("eu")

    us_extended = load_extended_summary("us")
    eu_extended = load_extended_summary("eu")

    combined_summary = pd.concat([us_summary, eu_summary], axis=0, ignore_index=True)
    combined_extended = pd.concat([us_extended, eu_extended], axis=0, ignore_index=True)

    combined_summary["Model Group"] = combined_summary["Strategy"].map(assign_model_group)

    key_comparison = build_key_strategy_comparison(combined_summary)
    market_leaders = build_market_leaders(combined_summary)
    synthetic_vrp_comparison = build_synthetic_vrp_comparison(combined_extended)
    empirical_conclusions = build_empirical_conclusions()

    combined_summary_path = OUTPUT_TABLES_DIR / "cross_market_implementable_summary.csv"
    key_comparison_path = OUTPUT_TABLES_DIR / "cross_market_key_strategy_comparison.csv"
    market_leaders_path = OUTPUT_TABLES_DIR / "cross_market_leaders.csv"
    synthetic_vrp_path = OUTPUT_TABLES_DIR / "cross_market_synthetic_vrp_comparison.csv"
    conclusions_path = OUTPUT_TABLES_DIR / "cross_market_empirical_conclusions.csv"

    combined_summary.to_csv(combined_summary_path, index=False)
    key_comparison.to_csv(key_comparison_path, index=False)
    market_leaders.to_csv(market_leaders_path, index=False)
    synthetic_vrp_comparison.to_csv(synthetic_vrp_path, index=False)
    empirical_conclusions.to_csv(conclusions_path, index=False)

    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_colwidth", 160)

    print("\n" + "=" * 120)
    print("CROSS-MARKET — Key strategy comparison")
    print("=" * 120)
    print(key_comparison.round(4).to_string(index=False))

    print("\n" + "=" * 120)
    print("CROSS-MARKET — Market leaders")
    print("=" * 120)
    print(market_leaders.round(4).to_string(index=False))

    print("\n" + "=" * 120)
    print("CROSS-MARKET — Synthetic VRP proxy comparison")
    print("=" * 120)

    if synthetic_vrp_comparison.empty:
        print("No synthetic VRP proxy rows found.")
    else:
        print(synthetic_vrp_comparison.round(4).to_string(index=False))

    print("\n" + "=" * 120)
    print("CROSS-MARKET — Empirical conclusions")
    print("=" * 120)
    print(empirical_conclusions.to_string(index=False))

    print("\nSaved cross-market files:")
    print(combined_summary_path)
    print(key_comparison_path)
    print(market_leaders_path)
    print(synthetic_vrp_path)
    print(conclusions_path)


if __name__ == "__main__":
    run_cross_market_report()
