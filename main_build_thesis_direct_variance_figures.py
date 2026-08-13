from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


TABLES = Path("outputs/tables")
FIGURES = Path("thesis/latex/figures")

FIGURES.mkdir(
    parents=True,
    exist_ok=True,
)


PERFORMANCE_FILE = (
    TABLES
    / "cross_market_direct_variance_key_comparison.csv"
)

WELFARE_FILE = (
    TABLES
    / "cross_market_direct_variance_welfare_gamma5.csv"
)


for path in [
    PERFORMANCE_FILE,
    WELFARE_FILE,
]:
    if not path.exists():
        raise FileNotFoundError(
            f"Missing required final table: {path}"
        )


performance = pd.read_csv(
    PERFORMANCE_FILE
)

welfare = pd.read_csv(
    WELFARE_FILE
)


# ============================================================
# EXACT FINAL STRATEGY DEFINITIONS
# ============================================================

selected_direct = {
    "US": (
        "Direct Short Variance 10% Vol "
        "(High VRP)"
    ),
    "EU": (
        "Direct Short Variance 10% Vol "
        "(VRP > 0)"
    ),
}

benchmarks = [
    "60/40",
    "1/N Equity-Bond",
]


# ============================================================
# VALIDATE FINAL TABLE CONTENT
# ============================================================

required_perf_columns = {
    "Market",
    "Strategy",
    "Sharpe",
}

missing_perf = (
    required_perf_columns
    - set(performance.columns)
)

if missing_perf:
    raise KeyError(
        "Performance table missing columns: "
        f"{sorted(missing_perf)}"
    )


required_welfare_columns = {
    "Market",
    "Strategy",
    "Fee Eq. bps vs 60/40",
    "Fee Eq. bps vs 1/N Equity-Bond",
}

missing_welfare = (
    required_welfare_columns
    - set(welfare.columns)
)

if missing_welfare:
    raise KeyError(
        "Welfare table missing columns: "
        f"{sorted(missing_welfare)}"
    )


def exact_row(
    frame,
    market,
    strategy,
):
    rows = frame.loc[
        (frame["Market"] == market)
        & (frame["Strategy"] == strategy)
    ]

    if len(rows) != 1:
        raise RuntimeError(
            f"Expected exactly one row for "
            f"{market} / {strategy}; "
            f"found {len(rows)}."
        )

    return rows.iloc[0]


# ============================================================
# FIGURE A
# SHARPE — SELECTED DIRECT STRATEGY VS BENCHMARKS
# ============================================================

markets = [
    "US",
    "EU",
]

display_strategies = [
    "60/40",
    "1/N",
    "Selected Direct",
]

values = {
    label: []
    for label in display_strategies
}


for market in markets:

    row_6040 = exact_row(
        performance,
        market,
        "60/40",
    )

    row_1n = exact_row(
        performance,
        market,
        "1/N Equity-Bond",
    )

    row_direct = exact_row(
        performance,
        market,
        selected_direct[market],
    )

    values["60/40"].append(
        float(row_6040["Sharpe"])
    )

    values["1/N"].append(
        float(row_1n["Sharpe"])
    )

    values["Selected Direct"].append(
        float(row_direct["Sharpe"])
    )


x = np.arange(
    len(markets)
)

width = 0.23

fig, ax = plt.subplots(
    figsize=(7.6, 4.6)
)

for index, label in enumerate(
    display_strategies
):
    positions = (
        x
        + (index - 1) * width
    )

    bars = ax.bar(
        positions,
        values[label],
        width,
        label=label,
    )

    ax.bar_label(
        bars,
        fmt="%.2f",
        padding=3,
        fontsize=8,
    )


ax.set_xticks(
    x,
    markets,
)

ax.set_ylabel(
    "Sharpe ratio"
)

ax.set_xlabel(
    "Market"
)

ax.legend(
    frameon=False,
    ncol=3,
)

ax.grid(
    axis="y",
    alpha=0.20,
)

fig.tight_layout()

sharpe_output = (
    FIGURES
    / (
        "direct_variance_"
        "sharpe_cross_market.png"
    )
)

fig.savefig(
    sharpe_output,
    dpi=220,
    bbox_inches="tight",
)

plt.close(fig)

print(
    f"PASS — {sharpe_output}"
)


# ============================================================
# FIGURE B
# GAMMA=5 WELFARE ADVANTAGE OF SELECTED DIRECT STRATEGY
# ============================================================

vs_6040 = []
vs_1n = []


for market in markets:

    row = exact_row(
        welfare,
        market,
        selected_direct[market],
    )

    vs_6040.append(
        float(
            row[
                "Fee Eq. bps vs 60/40"
            ]
        )
    )

    vs_1n.append(
        float(
            row[
                "Fee Eq. bps vs 1/N Equity-Bond"
            ]
        )
    )


fig, ax = plt.subplots(
    figsize=(7.6, 4.6)
)

width = 0.30

bars_6040 = ax.bar(
    x - width / 2,
    vs_6040,
    width,
    label="vs 60/40",
)

bars_1n = ax.bar(
    x + width / 2,
    vs_1n,
    width,
    label="vs 1/N",
)

ax.bar_label(
    bars_6040,
    fmt="%.0f",
    padding=3,
    fontsize=8,
)

ax.bar_label(
    bars_1n,
    fmt="%.0f",
    padding=3,
    fontsize=8,
)

ax.axhline(
    0.0,
    linewidth=0.8,
)

ax.set_xticks(
    x,
    markets,
)

ax.set_ylabel(
    "Fee-equivalent advantage (basis points)"
)

ax.set_xlabel(
    "Market"
)

ax.legend(
    frameon=False,
)

ax.grid(
    axis="y",
    alpha=0.20,
)

fig.tight_layout()

welfare_output = (
    FIGURES
    / (
        "direct_variance_"
        "welfare_cross_market.png"
    )
)

fig.savefig(
    welfare_output,
    dpi=220,
    bbox_inches="tight",
)

plt.close(fig)

print(
    f"PASS — {welfare_output}"
)


# ============================================================
# FINAL NUMERICAL VALIDATION
# ============================================================

expected = {
    "US_direct_sharpe": (
        0.8816668516675211
    ),
    "EU_direct_sharpe": (
        1.3239358698465211
    ),
    "US_vs_6040_bps": (
        -70.92273872067393
    ),
    "EU_vs_6040_bps": (
        926.6220906188886
    ),
}


actual = {
    "US_direct_sharpe":
        values["Selected Direct"][0],
    "EU_direct_sharpe":
        values["Selected Direct"][1],
    "US_vs_6040_bps":
        vs_6040[0],
    "EU_vs_6040_bps":
        vs_6040[1],
}


for key, expected_value in (
    expected.items()
):
    if not np.isclose(
        actual[key],
        expected_value,
        rtol=0.0,
        atol=1e-10,
    ):
        raise AssertionError(
            f"{key}: expected "
            f"{expected_value}, "
            f"found {actual[key]}"
        )


print(
    "PASS — direct-variance chart "
    "numerical validation"
)

print(
    "PASS — thesis direct-variance "
    "figures generated"
)
