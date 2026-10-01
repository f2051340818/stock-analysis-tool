from dataclasses import dataclass

@dataclass(frozen=True)
class Settings:
    tw_symbols: tuple[str, ...] = ("2330.TW","2454.TW","2303.TW","3711.TW","2379.TW","3034.TW","3661.TW","5274.TW","2382.TW","3231.TW","2357.TW","6669.TW","3443.TW","2368.TW","6488.TW","3037.TW","2408.TW","2308.TW","3008.TW","6415.TW")
    market_symbols: tuple[str, ...] = ("^TWII","^IXIC","^SOX","^GSPC","NVDA","AMD","AVGO","MSFT","AAPL")
    period: str = "400d"
    output_dir: str = "reports"

settings = Settings()
