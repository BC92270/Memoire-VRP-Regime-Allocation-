from __future__ import annotations

from dataclasses import dataclass
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
            if series.dropna().shape[0] >= min_obs:
                return ticker, series
            errors.append(f"{ticker}: insufficient observations ({series.dropna().shape[0]})")
        except Exception as exc:
            errors.append(f"{ticker}: {type(exc).__name__}: {exc}")

    message = "No valid ticker found. Attempts:\n" + "\n".join(errors)
    raise RuntimeError(message)


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
        market_config["equity_candidates"], start=start, end=end
    )

    vol_ticker, implied_vol = select_first_valid_series(
        market_config["vol_candidates"], start=start, end=end
    )

    bond_ticker, bond = select_first_valid_series(
        market_config["bond_candidates"], start=start, end=end
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
    print(f"[{market_name}] Date range: {df.index.min().date()} → {df.index.max().date()}")

    return df, selected