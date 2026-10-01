from __future__ import annotations

import math

import numpy as np
import pandas as pd


def _close(frame: pd.DataFrame) -> pd.Series:
    return pd.to_numeric(frame["Close"], errors="coerce").dropna()


def analyze(symbol: str, frame: pd.DataFrame) -> dict:
    close = _close(frame)
    if len(close) < 60:
        return {"symbol": symbol, "status": "資料不足", "score": 0, "confidence": 0}

    volume = pd.to_numeric(frame.get("Volume", pd.Series(index=frame.index, dtype=float)), errors="coerce")
    last = float(close.iloc[-1])
    ma20 = float(close.rolling(20).mean().iloc[-1])
    ma60 = float(close.rolling(60).mean().iloc[-1])
    ret5 = float(close.pct_change(5).iloc[-1] * 100)
    ret20 = float(close.pct_change(20).iloc[-1] * 100)
    avg_vol = float(volume.rolling(20).mean().iloc[-1]) if volume.rolling(20).mean().iloc[-1] else 0
    vol_ratio = float(volume.iloc[-1] / avg_vol) if avg_vol > 0 else 1.0
    volatility = float(close.pct_change().rolling(20).std().iloc[-1] * math.sqrt(252) * 100)

    trend = float(np.clip(50 + ret20 * 2 + (10 if last > ma20 > ma60 else 0), 0, 100))
    momentum = float(np.clip(50 + ret5 * 3 + (10 if vol_ratio > 1.2 else 0), 0, 100))
    stability = float(np.clip(100 - volatility * 1.5, 0, 100))
    moat = 58 if symbol in {"2330.TW", "2454.TW", "3711.TW", "2379.TW", "5274.TW"} else 45
    score = round(float(0.35 * trend + 0.25 * momentum + 0.20 * stability + 0.20 * moat), 1)
    direction = "偏多" if score >= 65 else "中性" if score >= 45 else "偏空"
    confidence = round(float(np.clip(45 + abs(score - 50) * 0.7 + min(len(close), 250) / 25, 0, 85)), 1)
    return {
        "symbol": symbol,
        "status": "OK",
        "price": round(last, 2),
        "r5": round(ret5, 2),
        "r20": round(ret20, 2),
        "ma20": round(ma20, 2),
        "ma60": round(ma60, 2),
        "volume_ratio": round(vol_ratio, 2),
        "volatility": round(volatility, 2),
        "trend": round(trend, 1),
        "momentum": round(momentum, 1),
        "stability": round(stability, 1),
        "moat": moat,
        "score": score,
        "direction": direction,
        "confidence": confidence,
        "reason": f"5日 {ret5:+.1f}%、20日 {ret20:+.1f}%；價格{'高於' if last > ma20 else '低於'}20日均線，量比 {vol_ratio:.2f}。",
    }


def market_snapshot(data: dict[str, pd.DataFrame]) -> list[dict]:
    rows: list[dict] = []
    for symbol, frame in data.items():
        close = _close(frame)
        if len(close) >= 2:
            rows.append({
                "symbol": symbol,
                "price": round(float(close.iloc[-1]), 2),
                "change": round(float(close.pct_change().iloc[-1] * 100), 2),
            })
    return rows
