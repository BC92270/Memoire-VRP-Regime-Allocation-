from __future__ import annotations

from itertools import product
from pathlib import Path

import pandas as pd

from src.config import (
    END_DATE,
    MARKET_CONFIGS,
    START_DATE,
)
from src.data_loader import (
    download_close_series,
    read_manual_close_csv,
    select_first_valid_series,
)


def series_stats(
    name: str,
    series: pd.Series,
) -> dict[str, object]:
    values = series.dropna().copy()
    values.index = pd.to_datetime(
        values.index,
        errors="coerce",
    )
    values = values.loc[
        ~values.index.isna()
    ]
    values = values.loc[
        ~values.index.duplicated(
            keep="last"
        )
    ].sort_index()

    gaps = (
        values.index.to_series()
        .diff()
        .dt.days
    )

    return {
        "Series": name,
        "Observations": len(values),
        "Start": (
            values.index.min().date()
            if not values.empty
            else None
        ),
        "End": (
            values.index.max().date()
            if not values.empty
            else None
        ),
        "Median Gap Days": (
            float(gaps.median())
            if gaps.notna().any()
            else float("nan")
        ),
        "Mean Gap Days": (
            float(gaps.mean())
            if gaps.notna().any()
            else float("nan")
        ),
        "Gaps Above 7 Days": int(
            gaps.gt(7).sum()
        ),
    }


def common_dates(
    *series: pd.Series,
) -> pd.DatetimeIndex:
    index = None

    for current in series:
        current_index = pd.DatetimeIndex(
            pd.to_datetime(
                current.dropna().index,
                errors="coerce",
            )
        ).dropna()

        current_index = (
            current_index
            .drop_duplicates()
            .sort_values()
        )

        index = (
            current_index
            if index is None
            else index.intersection(
                current_index
            )
        )

    return (
        pd.DatetimeIndex([])
        if index is None
        else index
    )


def main() -> None:
    config = MARKET_CONFIGS["EU"]

    manual_path = Path(
        config["manual_vol_csv"]
    )

    vstoxx = read_manual_close_csv(
        path=manual_path,
        series_name="VSTOXX",
        start=START_DATE,
        end=END_DATE,
    )

    downloaded: dict[str, pd.Series] = {
        "VSTOXX": vstoxx
    }

    rows = [
        series_stats(
            "VSTOXX",
            vstoxx,
        )
    ]

    candidates = (
        list(config["equity_candidates"])
        + list(config["bond_candidates"])
    )

    for ticker in candidates:
        try:
            series = download_close_series(
                ticker=ticker,
                start=START_DATE,
                end=END_DATE,
            )

            downloaded[ticker] = series

            rows.append(
                series_stats(
                    ticker,
                    series,
                )
            )

        except Exception as exc:
            rows.append(
                {
                    "Series": ticker,
                    "Observations": 0,
                    "Start": None,
                    "End": None,
                    "Median Gap Days": None,
                    "Mean Gap Days": None,
                    "Gaps Above 7 Days": None,
                    "Error": (
                        f"{type(exc).__name__}: "
                        f"{exc}"
                    ),
                }
            )

    summary = pd.DataFrame(rows)

    print("=" * 110)
    print("EU COMPONENT SERIES")
    print("=" * 110)
    print(summary.to_string(index=False))

    selected_equity_ticker, selected_equity = (
        select_first_valid_series(
            candidates=config[
                "equity_candidates"
            ],
            start=START_DATE,
            end=END_DATE,
        )
    )

    selected_bond_ticker, selected_bond = (
        select_first_valid_series(
            candidates=config[
                "bond_candidates"
            ],
            start=START_DATE,
            end=END_DATE,
        )
    )

    print()
    print("=" * 110)
    print("CURRENT AUTOMATIC SELECTION")
    print("=" * 110)

    print(
        f"Equity selected: "
        f"{selected_equity_ticker}"
    )

    print(
        f"Bond selected: "
        f"{selected_bond_ticker}"
    )

    equity_vol_dates = common_dates(
        selected_equity,
        vstoxx,
    )

    full_dates = common_dates(
        selected_equity,
        vstoxx,
        selected_bond,
    )

    print(
        "Equity + VSTOXX common dates: "
        f"{len(equity_vol_dates)}"
    )

    print(
        "Equity + VSTOXX + bond common dates: "
        f"{len(full_dates)}"
    )

    print(
        "Dates lost because of bond alignment: "
        f"{len(equity_vol_dates) - len(full_dates)}"
    )

    print()
    print("=" * 110)
    print("ALL EQUITY/BOND INTERSECTIONS")
    print("=" * 110)

    intersection_rows = []

    for equity_ticker, bond_ticker in product(
        config["equity_candidates"],
        config["bond_candidates"],
    ):
        if (
            equity_ticker not in downloaded
            or bond_ticker not in downloaded
        ):
            continue

        equity = downloaded[
            equity_ticker
        ]

        bond = downloaded[
            bond_ticker
        ]

        equity_vol = common_dates(
            equity,
            vstoxx,
        )

        full = common_dates(
            equity,
            vstoxx,
            bond,
        )

        intersection_rows.append(
            {
                "Equity": equity_ticker,
                "Bond": bond_ticker,
                "Equity + VSTOXX": (
                    len(equity_vol)
                ),
                "Full Intersection": (
                    len(full)
                ),
                "Lost to Bond": (
                    len(equity_vol)
                    - len(full)
                ),
            }
        )

    intersections = pd.DataFrame(
        intersection_rows
    ).sort_values(
        [
            "Full Intersection",
            "Equity + VSTOXX",
        ],
        ascending=False,
    )

    print(
        intersections.to_string(
            index=False
        )
    )

    output_path = Path(
        "outputs/tables/"
        "eu_component_data_audit.csv"
    )

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    summary.to_csv(
        output_path,
        index=False,
    )

    print()
    print(
        f"Audit saved to: {output_path}"
    )


if __name__ == "__main__":
    main()
