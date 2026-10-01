from __future__ import annotations

import argparse
import logging
from pathlib import Path

from .analysis import analyze, market_snapshot
from .config import settings
from .data import download_prices
from .report import render

logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")


def main() -> None:
    parser = argparse.ArgumentParser(description="Research-only stock report generator")
    parser.add_argument("--mode", choices=["intraday", "after-market"], default="after-market")
    parser.add_argument("--output", default=settings.output_dir)
    args = parser.parse_args()

    tw = download_prices(settings.tw_symbols, settings.period)
    market = download_prices(settings.market_symbols, settings.period)
    results = [analyze(symbol, frame) for symbol, frame in tw.items()]
    output = render(results, market_snapshot(market), args.mode, args.output)
    logging.info("Generated: %s", Path(output).resolve())


if __name__ == "__main__":
    main()
