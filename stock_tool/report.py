from __future__ import annotations

from datetime import datetime, timezone
from pathlib import Path

from jinja2 import Template

PAGE = Template('''<!doctype html>
<html lang="zh-Hant">
<head><meta charset="utf-8"><title>{{ title }}</title>
<style>
body { font-family: system-ui, -apple-system, sans-serif; max-width: 1200px; margin: 2rem auto; line-height: 1.6; padding: 0 1rem; }
.note { background: #fff8dc; padding: 1rem; border-radius: 8px; }
table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
th, td { border: 1px solid #d9dde5; padding: 0.5rem; text-align: left; }
th { background: #f1f5f9; }
</style>
</head>
<body>
<h1>{{ title }}</h1>
<p>產生時間：{{ created }}｜模式：{{ mode }}</p>
<div class="note"><b>研究聲明：</b>本報告僅供研究參考，不是投資建議、不保證預測都會發生，也不包含下單功能。明日預測僅為偏多／中性／偏空情境。</div>
<h2>明日情境</h2>
<p>{{ conclusion }}</p>
<h2>台灣科技股候選</h2>
<table>
<tr><th>代號</th><th>價格</th><th>5日%</th><th>20日%</th><th>評分</th><th>方向</th><th>信心</th><th>理由</th></tr>
{% for x in results %}
<tr><td>{{ x.symbol }}</td><td>{{ x.price|default('-') }}</td><td>{{ x.r5|default('-') }}</td><td>{{ x.r20|default('-') }}</td><td>{{ x.score|default('-') }}</td><td>{{ x.direction|default('-') }}</td><td>{{ x.confidence|default('-') }}%</td><td>{{ x.reason|default('資料不足') }}</td></tr>
{% endfor %}
</table>
<h2>美股與市場背景</h2>
<table><tr><th>標的</th><th>最新</th><th>變化%</th></tr>
{% for x in market %}<tr><td>{{ x.symbol }}</td><td>{{ x.price }}</td><td>{{ x.change }}</td></tr>{% endfor %}</table>
<h2>限制</h2>
<ul>
<li>行情使用 Yahoo Finance 公開資料，可能延遲、缺漏或調整。</li>
<li>目前未接入即時新聞、完整財報與 walk-forward 回測；不臆測新聞。</li>
<li>護城河是公開資料代理分數，不等同完整專利、市占率或客戶研究。</li>
</ul>
</body></html>
''')


def render(results: list[dict], market: list[dict], mode: str, output_dir: str) -> Path:
    valid = sorted([x for x in results if x.get("status") == "OK"], key=lambda x: x["score"], reverse=True)
    short = ", ".join(x["symbol"] for x in valid[:5]) or "資料不足"
    long = ", ".join(x["symbol"] for x in sorted(valid, key=lambda x: (x["moat"], x["stability"]), reverse=True)[:5]) or "資料不足"
    conclusion = f"短線觀察：{short}；長線研究：{long}。僅在資料與風險可接受時進一步研究，不直接指示買入。"
    created = datetime.now(timezone.utc).astimezone().strftime("%Y-%m-%d %H:%M %Z")
    html = PAGE.render(title="台灣科技股與美股市場研究報告", created=created, mode=mode, results=valid, market=market, conclusion=conclusion)
    path = Path(output_dir)
    path.mkdir(parents=True, exist_ok=True)
    file = path / f"{datetime.now():%Y%m%d_%H%M}_{mode}.html"
    file.write_text(html, encoding="utf-8")
    (path / "latest.html").write_text(html, encoding="utf-8")
    return file
