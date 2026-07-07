from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

import pandas as pd
import yfinance as yf


@dataclass(frozen=True)
class SelectedTickers:
    equity: str
    implied_vol: str
    bond: str


def _extract_close(downloaded: pd.DataFrame, ticker: str) -> pd.Series:
    """
    Robustly extracts the adjusted close-like series from yfinance output.
    With auto_adjust=True, yfinance's 'Close' is adjusted.
    """
    if downloaded is None or downloaded.empty:
        return pd.Series(dtype=float, name=ticker)

    if isinstance(downloaded.columns, pd.MultiIndex):
        if ("Close", ticker) in downloaded.columns:
            close = downloaded[("Close", ticker)]
        elif "Close" in downloaded.columns.get_level_values(0):
            close = downloaded["Close"].iloc[:, 0]
        else:
            return pd.Series(dtype=float, name=ticker)
    else:
        if "Close" not in downloaded.columns:
            return pd.Series(dtype=float, name=ticker)
        close = downloaded["Close"]

    close = close.dropna()
    close.name = ticker
    return close


def download_close_series(
    ticker: str,
    start: str,
    end: str | None = None,
) -> pd.Series:
    """
    Downloads one close series from Yahoo Finance.
    """
    data = yf.download(
        ticker,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False,
        threads=False,
    )
    return _extract_close(data, ticker)


def select_first_valid_series(
    candidates: Iterable[str],
    start: str,
    end: str | None = None,
    min_obs: int = 500,
) -> tuple[str, pd.Series]:
    """
    Tries candidate tickers and returns the first one with enough data.
    """
    errors = []

    for ticker in candidates:
        try:
            series = download_close_series(ticker, start=start, end=end)
            obs = series.dropna().shape[0]

            if obs >= min_obs:
                return ticker, series

            errors.append(f"{ticker}: insufficient observations ({obs})")

        except Exception as exc:
            errors.append(f"{ticker}: {type(exc).__name__}: {exc}")

    message = "No valid ticker found. Attempts:\n" + "\n".join(errors)
    raise RuntimeError(message)


def _clean_numeric_series(series: pd.Series) -> pd.Series:
    """
    Cleans numeric strings from CSV files.

    Handles:
    - 19.32
    - 19,32
    - 1,234.56
    - 1.234,56
    - percentage signs
    - spaces
    """
    cleaned = series.astype(str).str.strip()
    cleaned = cleaned.str.replace("%", "", regex=False)
    cleaned = cleaned.str.replace("\u202f", "", regex=False)
    cleaned = cleaned.str.replace(" ", "", regex=False)

    def parse_one(value: str) -> float:
        if value.lower() in {"nan", "none", "", "-"}:
            return float("nan")

        # European style: 1.234,56
        if "," in value and "." in value and value.rfind(",") > value.rfind("."):
            value = value.replace(".", "").replace(",", ".")

        # US style: 1,234.56
        elif "," in value and "." in value and value.rfind(".") > value.rfind(","):
            value = value.replace(",", "")

        # Decimal comma: 19,32
        elif "," in value and "." not in value:
            value = value.replace(",", ".")

        return float(value)

    return cleaned.map(parse_one)


def read_manual_close_csv(
    path: str | Path,
    series_name: str,
    start: str | None = None,
    end: str | None = None,
) -> pd.Series:
    """
    Reads a manual CSV price/index series with flexible column names.

    Expected columns can be:
    - Date / date / time / Date Dernier
    - Close / Price / Dernier / Last
    """
    path = Path(path)

    if not path.exists():
        raise FileNotFoundError(f"Manual CSV does not exist: {path}")

    read_errors = []
    df = None

    for sep in [",", ";", "\t"]:
        try:
            candidate = pd.read_csv(path, sep=sep)
            if candidate.shape[1] >= 2:
                df = candidate
                break
        except Exception as exc:
            read_errors.append(f"sep={sep}: {type(exc).__name__}: {exc}")

    if df is None:
        message = "Could not read manual CSV. Attempts:\n" + "\n".join(read_errors)
        raise RuntimeError(message)

    df.columns = [str(c).strip() for c in df.columns]

    date_candidates = [
        "Date",
        "date",
        "DATE",
        "Time",
        "time",
        "Datetime",
        "datetime",
    ]

    price_candidates = [
        "Close",
        "close",
        "CLOSE",
        "Adj Close",
        "Price",
        "price",
        "Last",
        "last",
        "Dernier",
        "dernier",
        "Dernière",
        "PX_LAST",
        "Value",
        "value",
    ]

    date_col = next((c for c in date_candidates if c in df.columns), None)
    price_col = next((c for c in price_candidates if c in df.columns), None)

    if date_col is None:
        raise ValueError(
            f"Could not find a date column in {path}. Columns found: {list(df.columns)}"
        )

    if price_col is None:
        raise ValueError(
            f"Could not find a price/close column in {path}. Columns found: {list(df.columns)}"
        )

    dates = pd.to_datetime(df[date_col], errors="coerce", dayfirst=True)
    values = _clean_numeric_series(df[price_col])

    out = pd.Series(values.values, index=dates, name=series_name)
    out = out[~out.index.isna()]
    out = out.dropna()
    out = out.sort_index()

    # Remove duplicate dates if the CSV contains repeated rows.
    out = out[~out.index.duplicated(keep="last")]

    if start is not None:
        out = out.loc[pd.to_datetime(start):]

    if end is not None:
        out = out.loc[:pd.to_datetime(end)]

    return out


def select_series_with_manual_fallback(
    candidates: Iterable[str],
    start: str,
    end: str | None = None,
    manual_csv: str | Path | None = None,
    manual_name: str = "manual_series",
    min_obs: int = 500,
) -> tuple[str, pd.Series]:
    """
    Uses manual CSV first if present, then falls back to Yahoo tickers.
    """
    if manual_csv is not None:
        manual_path = Path(manual_csv)

        if manual_path.exists():
            manual_series = read_manual_close_csv(
                manual_path,
                series_name=manual_name,
                start=start,
                end=end,
            )

            obs = manual_series.dropna().shape[0]

            if obs >= min_obs:
                return f"manual:{manual_path.name}", manual_series

            print(
                f"Manual CSV found but insufficient observations for {manual_name}: "
                f"{obs} observations."
            )

    return select_first_valid_series(
        candidates=candidates,
        start=start,
        end=end,
        min_obs=min_obs,
    )


def build_market_dataset(
    market_name: str,
    market_config: dict,
    start: str,
    end: str | None = None,
) -> tuple[pd.DataFrame, SelectedTickers]:
    """
    Builds a daily dataset with equity price, implied volatility index and bond proxy.
    """
    equity_ticker, equity = select_first_valid_series(
        market_config["equity_candidates"],
        start=start,
        end=end,
    )

    vol_ticker, implied_vol = select_series_with_manual_fallback(
        candidates=market_config["vol_candidates"],
        start=start,
        end=end,
        manual_csv=market_config.get("manual_vol_csv"),
        manual_name=f"{market_name}_implied_vol_index",
    )

    bond_ticker, bond = select_first_valid_series(
        market_config["bond_candidates"],
        start=start,
        end=end,
    )

    df = pd.concat(
        [
            equity.rename("equity_price"),
            implied_vol.rename("implied_vol_index"),
            bond.rename("bond_price"),
        ],
        axis=1,
    ).sort_index()

    df = df.dropna(how="any")

    selected = SelectedTickers(
        equity=equity_ticker,
        implied_vol=vol_ticker,
        bond=bond_ticker,
    )

    print(f"[{market_name}] Selected tickers: {selected}")
    print(f"[{market_name}] Daily dataset shape: {df.shape}")

    if not df.empty:
        print(f"[{market_name}] Date range: {df.index.min().date()} → {df.index.max().date()}")

    return df, selected