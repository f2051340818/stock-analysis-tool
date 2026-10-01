# Stock Analysis Tool

台灣科技股為主、搭配美股市場資訊的研究型分析工具。只產生研究報告，不包含下單、交易或投資執行功能。

## Preview MVP

- 自動從預設台灣科技股 universe 篩選短線／長線研究候選
- 加入 NASDAQ、費城半導體指數、S&P 500 與指定美股科技股背景
- 以技術面、穩定度、護城河代理指標產生可解釋評分
- 產生 HTML 報告並由 GitHub Actions 上傳 artifact
- 預設不寄信、不下單；先確認報告內容

> 本報告僅供研究參考，不是投資建議，也不保證預測正確。資料缺漏或行情 API 異常時，報告會標示限制。

## 使用方式

到 **Actions → Generate preview report → Run workflow**，選擇 `after-market` 或 `intraday`，完成後下載 artifact。排程目前只產生 artifact，不寄信。

- 台灣 10:30 盤中分析：UTC 02:30
- 台灣 20:30 盤後分析：UTC 12:30

GitHub Actions 的 cron 可能延遲數分鐘；台股與美股交易日不同，請確認報告資料日期。

## 本機執行

```bash
pip install -r requirements.txt
python -m stock_tool.cli --mode after-market
```

報告輸出於 `reports/`。資料預覽來源為 Yahoo Finance，可能延遲、缺漏或調整。

## 後續 Email

確認報告格式後，再設定 GitHub Actions Secrets：`SMTP_USERNAME`、`SMTP_APP_PASSWORD`、`REPORT_RECIPIENT`。程式不保存券商憑證，也沒有下單功能。

目前尚未接入即時新聞、完整財報 API 與 walk-forward 回測；新聞不會被模型自行臆測。護城河分數是公開資料的保守代理分數，不等同完整專利、市占率或客戶續約研究。
