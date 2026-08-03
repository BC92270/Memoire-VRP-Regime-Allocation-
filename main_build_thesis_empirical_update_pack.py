from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd


TABLES = Path("outputs/tables")
THESIS = Path("thesis")

OUTPUT_PATH = (
    THESIS
    / "empirical_update_pack.md"
)


def require_file(
    path: Path,
) -> None:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required file: {path}"
        )


def read_csv(
    filename: str,
) -> pd.DataFrame:
    path = TABLES / filename

    require_file(path)

    return pd.read_csv(path)


def format_percent(
    value: object,
    digits: int = 2,
) -> str:
    if pd.isna(value):
        return ""

    return (
        f"{100.0 * float(value):.{digits}f}%"
    )


def format_ratio(
    value: object,
    digits: int = 3,
) -> str:
    if pd.isna(value):
        return ""

    return f"{float(value):.{digits}f}"


def format_integer(
    value: object,
) -> str:
    if pd.isna(value):
        return ""

    return str(int(round(float(value))))


def markdown_table(
    frame: pd.DataFrame,
    formats: dict[str, str] | None = None,
) -> str:
    result = frame.copy()

    formats = formats or {}

    for column, formatter in formats.items():
        if column not in result.columns:
            continue

        if formatter == "percent":
            result[column] = result[
                column
            ].map(format_percent)

        elif formatter == "ratio":
            result[column] = result[
                column
            ].map(format_ratio)

        elif formatter == "integer":
            result[column] = result[
                column
            ].map(format_integer)

        elif formatter == "bps":
            result[column] = result[
                column
            ].map(
                lambda value: (
                    ""
                    if pd.isna(value)
                    else f"{float(value):.1f}"
                )
            )

    def render_cell(
        value: object,
    ) -> str:
        if pd.isna(value):
            return ""

        return (
            str(value)
            .replace("\\", "\\\\")
            .replace("|", "\\|")
            .replace("\n", " ")
            .strip()
        )

    headers = [
        render_cell(column)
        for column in result.columns
    ]

    separator = [
        "---"
        for _ in headers
    ]

    rows = [
        [
            render_cell(value)
            for value in row
        ]
        for row in result.itertuples(
            index=False,
            name=None,
        )
    ]

    lines = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join(separator) + " |",
    ]

    lines.extend(
        "| " + " | ".join(row) + " |"
        for row in rows
    )

    return "\n".join(lines)


def validate_numeric(
    frame: pd.DataFrame,
    label: str,
) -> None:
    numeric = frame.select_dtypes(
        include=[np.number]
    )

    if (
        not numeric.empty
        and not np.isfinite(
            numeric.to_numpy()
        ).all()
    ):
        raise ValueError(
            f"Non-finite values in {label}"
        )


def select_rows(
    frame: pd.DataFrame,
    strategies: list[str],
) -> pd.DataFrame:
    rows = []

    for strategy in strategies:
        selected = frame.loc[
            frame[
                "Strategy"
            ].eq(strategy)
        ]

        if selected.empty:
            raise KeyError(
                f"Strategy not found: "
                f"{strategy}"
            )

        rows.append(
            selected.iloc[0]
        )

    return pd.DataFrame(rows)


def build_allocation_section(
) -> str:
    comparison = read_csv(
        (
            "cross_market_"
            "key_strategy_comparison.csv"
        )
    )

    validate_numeric(
        comparison,
        "allocation comparison",
    )

    columns = [
        "Market",
        "Model Group",
        "Strategy",
        "Ann. Return",
        "Ann. Vol",
        "Sharpe",
        "Sortino",
        "Max Drawdown",
        "CVaR 95",
        "Avg Turnover",
        "Obs",
    ]

    comparison = comparison[
        columns
    ]

    return "\n".join(
        [
            "## 1. Equity–bond allocation evidence",
            "",
            (
                "This table compares benchmarks "
                "with the strongest HMM, RSM and "
                "machine-learning specifications. "
                "These strategies belong to the "
                "equity–bond allocation evidence "
                "layer and must not be directly "
                "ranked against direct-variance "
                "strategies without acknowledging "
                "their different samples and payoff "
                "structures."
            ),
            "",
            markdown_table(
                comparison,
                formats={
                    "Ann. Return": "percent",
                    "Ann. Vol": "percent",
                    "Sharpe": "ratio",
                    "Sortino": "ratio",
                    "Max Drawdown": "percent",
                    "CVaR 95": "percent",
                    "Avg Turnover": "percent",
                    "Obs": "integer",
                },
            ),
        ]
    )


def build_direct_performance_section(
) -> str:
    performance = read_csv(
        (
            "cross_market_direct_variance_"
            "performance.csv"
        )
    )

    validate_numeric(
        performance,
        "direct variance performance",
    )

    selected = select_rows(
        performance,
        strategies=[
            "Direct Short Variance 10% Vol (High VRP)",
            "60/40",
            "1/N Equity-Bond",
            "Direct Short Variance 10% Vol (VRP > 0)",
        ],
    )

    selected = selected[
        [
            "Market",
            "Model Group",
            "Strategy",
            "Ann. Return",
            "Ann. Vol",
            "Sharpe",
            "Sortino",
            "Max Drawdown",
            "Calmar",
            "CVaR 95",
            "Avg Turnover",
            "Obs",
        ]
    ]

    return "\n".join(
        [
            "## 2. Selected direct-variance evidence",
            "",
            (
                "The direct-variance extension is a "
                "model-based carry approximation. "
                "It is not an observed variance-swap "
                "return series."
            ),
            "",
            markdown_table(
                selected,
                formats={
                    "Ann. Return": "percent",
                    "Ann. Vol": "percent",
                    "Sharpe": "ratio",
                    "Sortino": "ratio",
                    "Max Drawdown": "percent",
                    "Calmar": "ratio",
                    "CVaR 95": "percent",
                    "Avg Turnover": "percent",
                    "Obs": "integer",
                },
            ),
        ]
    )


def build_payoff_section(
) -> str:
    payoff = read_csv(
        (
            "cross_market_direct_variance_"
            "payoff_summary.csv"
        )
    )

    validate_numeric(
        payoff,
        "direct variance payoff",
    )

    preferred_columns = [
        "Market",
        "Observations",
        "Start",
        "End",
        "Mean Variance Strike",
        "Mean Realized Variance",
        "Mean Short Variance Payoff",
        "Positive Payoff Rate",
        "Mean Normalized Payoff",
        "Normalized Payoff Skew",
        "Normalized Payoff 1%",
        "Worst Normalized Payoff",
        "Months Below -100% Rate",
    ]

    columns = [
        column
        for column in preferred_columns
        if column in payoff.columns
    ]

    payoff = payoff[
        columns
    ]

    formats = {
        "Observations": "integer",
        "Mean Variance Strike": "percent",
        "Mean Realized Variance": "percent",
        "Mean Short Variance Payoff": "percent",
        "Positive Payoff Rate": "percent",
        "Mean Normalized Payoff": "ratio",
        "Normalized Payoff Skew": "ratio",
        "Normalized Payoff 1%": "ratio",
        "Worst Normalized Payoff": "ratio",
        "Months Below -100% Rate": "percent",
    }

    return "\n".join(
        [
            "## 3. Underlying variance-payoff diagnostics",
            "",
            (
                "The payoff is constructed from the "
                "lagged implied-variance proxy and "
                "the subsequent realized-variance "
                "proxy. Frequent positive carry is "
                "combined with negatively skewed "
                "tail outcomes."
            ),
            "",
            markdown_table(
                payoff,
                formats=formats,
            ),
        ]
    )


def build_welfare_section(
) -> str:
    welfare = read_csv(
        (
            "cross_market_direct_variance_"
            "welfare_gamma5.csv"
        )
    )

    validate_numeric(
        welfare,
        "direct variance welfare",
    )

    selected_names = {
        "US": (
            "Direct Short Variance "
            "10% Vol (High VRP)"
        ),
        "EU": (
            "Direct Short Variance "
            "10% Vol (VRP > 0)"
        ),
    }

    rows = []

    for market, strategy in (
        selected_names.items()
    ):
        selected = welfare.loc[
            welfare["Market"].eq(market)
            & welfare["Strategy"].eq(
                strategy
            )
        ]

        if selected.empty:
            raise KeyError(
                f"Missing welfare row: "
                f"{market} / {strategy}"
            )

        rows.append(
            selected.iloc[0]
        )

    selected = pd.DataFrame(rows)

    columns = [
        "Market",
        "Strategy",
        "Gamma",
        "MV CEQ Ann.",
        "CRRA CE Ann.",
        "Fee Eq. bps vs 60/40",
        (
            "Delta MV CEQ CI Low "
            "vs 60/40"
        ),
        (
            "Delta MV CEQ CI High "
            "vs 60/40"
        ),
        (
            "Fee Eq. bps "
            "vs 1/N Equity-Bond"
        ),
        (
            "Delta MV CEQ CI Low "
            "vs 1/N Equity-Bond"
        ),
        (
            "Delta MV CEQ CI High "
            "vs 1/N Equity-Bond"
        ),
        (
            "Statistically Superior "
            "vs 60/40"
        ),
        (
            "Statistically Superior "
            "vs 1/N Equity-Bond"
        ),
    ]

    selected = selected[
        columns
    ]

    return "\n".join(
        [
            "## 4. Welfare evidence at gamma = 5",
            "",
            markdown_table(
                selected,
                formats={
                    "Gamma": "ratio",
                    "MV CEQ Ann.": "percent",
                    "CRRA CE Ann.": "percent",
                    (
                        "Fee Eq. bps "
                        "vs 60/40"
                    ): "bps",
                    (
                        "Delta MV CEQ CI Low "
                        "vs 60/40"
                    ): "percent",
                    (
                        "Delta MV CEQ CI High "
                        "vs 60/40"
                    ): "percent",
                    (
                        "Fee Eq. bps "
                        "vs 1/N Equity-Bond"
                    ): "bps",
                    (
                        "Delta MV CEQ CI Low "
                        "vs 1/N Equity-Bond"
                    ): "percent",
                    (
                        "Delta MV CEQ CI High "
                        "vs 1/N Equity-Bond"
                    ): "percent",
                },
            ),
            "",
            (
                "Interpretation: the selected US "
                "strategy does not establish "
                "statistical welfare dominance over "
                "both benchmarks. The selected "
                "European strategy has positive "
                "lower confidence bounds against "
                "both 60/40 and 1/N."
            ),
        ]
    )


def build_robustness_section(
) -> str:
    costs = read_csv(
        (
            "cross_market_direct_variance_"
            "robustness_costs.csv"
        )
    )

    lookbacks = read_csv(
        (
            "cross_market_direct_variance_"
            "robustness_lookbacks.csv"
        )
    )

    caps = read_csv(
        (
            "cross_market_direct_variance_"
            "robustness_caps.csv"
        )
    )

    subperiods = read_csv(
        (
            "cross_market_direct_variance_"
            "robustness_subperiods.csv"
        )
    )

    gamma = read_csv(
        (
            "cross_market_direct_variance_"
            "robustness_gamma.csv"
        )
    )

    for label, frame in {
        "costs": costs,
        "lookbacks": lookbacks,
        "caps": caps,
        "subperiods": subperiods,
        "gamma": gamma,
    }.items():
        validate_numeric(
            frame,
            f"robustness {label}",
        )

    key_strategies = {
        "US": (
            "Direct Short Variance "
            "10% Vol (High VRP)"
        ),
        "EU": (
            "Direct Short Variance "
            "10% Vol (VRP > 0)"
        ),
    }

    blocks = [
        "## 5. Direct-variance robustness",
        "",
    ]

    dimensions = [
        (
            "Transaction-cost sensitivity",
            costs,
            "Parameter Label",
        ),
        (
            "Volatility-lookback sensitivity",
            lookbacks,
            "Parameter Label",
        ),
        (
            "Notional-cap sensitivity",
            caps,
            "Parameter Label",
        ),
        (
            "Subperiod stability",
            subperiods,
            "Period",
        ),
    ]

    for (
        title,
        frame,
        parameter_column,
    ) in dimensions:
        selected_rows = []

        for market, strategy in (
            key_strategies.items()
        ):
            selected = frame.loc[
                frame["Market"].eq(market)
                & frame["Strategy"].eq(
                    strategy
                )
            ].copy()

            selected_rows.append(
                selected
            )

        selected = pd.concat(
            selected_rows,
            ignore_index=True,
        )

        columns = [
            "Market",
            parameter_column,
            "Ann. Return",
            "Ann. Vol",
            "Sharpe",
            "Max Drawdown",
            "CVaR 95",
            "Avg Turnover",
            "MV CEQ Ann.",
            "Delta MV CEQ vs 60/40",
            "Delta MV CEQ vs 1/N",
        ]

        selected = selected[
            [
                column
                for column in columns
                if column
                in selected.columns
            ]
        ]

        blocks.extend(
            [
                f"### {title}",
                "",
                markdown_table(
                    selected,
                    formats={
                        "Ann. Return": "percent",
                        "Ann. Vol": "percent",
                        "Sharpe": "ratio",
                        "Max Drawdown": "percent",
                        "CVaR 95": "percent",
                        "Avg Turnover": "percent",
                        "MV CEQ Ann.": "percent",
                        (
                            "Delta MV CEQ "
                            "vs 60/40"
                        ): "percent",
                        (
                            "Delta MV CEQ "
                            "vs 1/N"
                        ): "percent",
                    },
                ),
                "",
            ]
        )

    gamma_rows = []

    for market, strategy in (
        key_strategies.items()
    ):
        selected = gamma.loc[
            gamma["Market"].eq(market)
            & gamma["Strategy"].eq(
                strategy
            )
        ].copy()

        gamma_rows.append(
            selected
        )

    gamma_selected = pd.concat(
        gamma_rows,
        ignore_index=True,
    )

    gamma_selected = gamma_selected[
        [
            "Market",
            "Gamma",
            "MV CEQ Ann.",
            "CRRA CE Ann.",
            "Delta MV CEQ vs 60/40",
            "Delta MV CEQ vs 1/N",
        ]
    ]

    blocks.extend(
        [
            "### Risk-aversion stability",
            "",
            markdown_table(
                gamma_selected,
                formats={
                    "Gamma": "ratio",
                    "MV CEQ Ann.": "percent",
                    "CRRA CE Ann.": "percent",
                    (
                        "Delta MV CEQ "
                        "vs 60/40"
                    ): "percent",
                    (
                        "Delta MV CEQ "
                        "vs 1/N"
                    ): "percent",
                },
            ),
        ]
    )

    return "\n".join(blocks)


def build_conclusions_section(
) -> str:
    conclusions = read_csv(
        (
            "cross_market_empirical_"
            "conclusions.csv"
        )
    )

    required_columns = {
        "Theme",
        "Evidence Layer",
        "Conclusion",
    }

    missing = (
        required_columns.difference(
            conclusions.columns
        )
    )

    if missing:
        raise ValueError(
            "Missing conclusion columns: "
            f"{sorted(missing)}"
        )

    blocks = [
        "## 6. Final empirical conclusions",
        "",
    ]

    for _, row in conclusions.iterrows():
        blocks.extend(
            [
                f"### {row['Theme']}",
                "",
                (
                    "**Evidence layer:** "
                    f"{row['Evidence Layer']}"
                ),
                "",
                str(row["Conclusion"]),
                "",
            ]
        )

    return "\n".join(blocks)

def build_methodological_boundary(
) -> str:
    return "\n".join(
        [
            "## 7. Mandatory methodological terminology",
            "",
            (
                "The following terminology must be "
                "used consistently throughout the "
                "thesis:"
            ),
            "",
            (
                "- **Model-based direct variance "
                "carry approximation** or "
                "**model-based direct variance-payoff "
                "approximation**."
            ),
            (
                "- The strike proxy is lagged implied "
                "variance derived from the volatility "
                "index."
            ),
            (
                "- The settlement proxy is the "
                "subsequent annualized trailing "
                "realized variance."
            ),
            (
                "- The normalized payoff is not an "
                "observed return on invested capital."
            ),
            (
                "- Risk-targeted returns are a "
                "synthetic capital mapping from the "
                "variance payoff."
            ),
            (
                "- Transaction costs are stylized "
                "monthly roll costs applied to the "
                "absolute notional entered."
            ),
            (
                "- The framework does not reconstruct "
                "an exact variance-swap strike, option "
                "surface, collateral account, margin "
                "path, bid-ask spread or daily "
                "mark-to-market."
            ),
            "",
            (
                "The expressions **tradable variance "
                "swap return**, **actual variance-swap "
                "performance** and similar formulations "
                "must not be used for the MVP 7 series."
            ),
        ]
    )


def main() -> None:
    THESIS.mkdir(
        parents=True,
        exist_ok=True,
    )

    title = "\n".join(
        [
            "# Empirical Update Pack",
            "",
            (
                "This document is generated from the "
                "final validated output tables. It is "
                "the numerical and interpretive source "
                "of truth for the thesis rewrite."
            ),
            "",
            (
                "Allocation-model and direct-variance "
                "results are presented as distinct "
                "evidence layers because they use "
                "different payoff structures and may "
                "use different aligned samples."
            ),
        ]
    )

    sections = [
        title,
        build_allocation_section(),
        build_direct_performance_section(),
        build_payoff_section(),
        build_welfare_section(),
        build_robustness_section(),
        build_conclusions_section(),
        build_methodological_boundary(),
    ]

    text = "\n\n---\n\n".join(
        sections
    ).strip() + "\n"

    stale_phrases = [
        "collapses in Europe",
        (
            "more useful as a "
            "regime-state variable"
        ),
        (
            "universally robust "
            "standalone return engine"
        ),
    ]

    for phrase in stale_phrases:
        if phrase.lower() in text.lower():
            raise AssertionError(
                "Stale phrase generated: "
                f"{phrase}"
            )

    OUTPUT_PATH.write_text(
        text,
        encoding="utf-8",
    )

    print("=" * 100)
    print(
        "THESIS EMPIRICAL UPDATE PACK "
        "COMPLETE"
    )
    print("=" * 100)
    print(f"Saved: {OUTPUT_PATH}")
    print(
        f"Lines: {len(text.splitlines())}"
    )
    print(
        f"Characters: {len(text)}"
    )


if __name__ == "__main__":
    main()
