from __future__ import annotations

import logging
from typing import Iterable

import pandas as pd
import yfinance as yf

log = logging.getLogger(__name__)


def download_prices(symbols: Iterable[str], period: str = "400d") -> dict[str, pd.DataFrame]:
    result: dict[str, pd.DataFrame] = {}
    for symbol in symbols:
        try:
            df = yf.download(symbol, period=period, interval="1d", auto_adjust=False, progress=False, threads=False)
            if isinstance(df.columns, pd.MultiIndex):
                df.columns = df.columns.get_level_values(0)
            df = df.rename(columns=str.title).dropna(subset=["Close"])
            if not df.empty:
                result[symbol] = df
        except Exception as exc:
            log.warning("Skip %s due to %s", symbol, exc)
    return result
