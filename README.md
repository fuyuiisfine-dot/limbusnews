# Limbus News Bot - 梅菲斯特情報號 🚌

這是一個專為 《Limbus Company》（邊獄公司）玩家設計的新聞推播工具。它能自動監控 Steam 官方公告與 X (Twitter) 的最新動態，並即時發送到指定的 Discord 頻道。

> 「這是我練習寫 Python Scraper 的第一項作品。你能看見我的不足和掙扎嗎？未來的你。」 —— *作者自白*

---

## 🌟 功能特點

- **Steam 官方公告監控**：直接串接 Steam News API，獲取最新的維護、活動及更新資訊。
- **X (Twitter) 動態追蹤**：透過 RSS 服務監控官方推特，確保不漏掉任何圖片或短訊息。
- **Discord 即時推播**：使用 Webhook 技術，將美化後的新聞內容直接送達玩家手中。
- **自動化運行**：整合 GitHub Actions，每 30 分鐘自動檢查一次，無需本地電腦常開。
- **防重複發送**：自動記錄已發送過的 ID，確保訊息不洗版。

## 🛠️ 技術棧

- **Python 3.10+**
- **Requests**: 處理 API 請求與 Discord Webhook。
- **BeautifulSoup4**: 清理 Steam 公告中的 HTML 標籤。
- **Feedparser**: 解析 X 的 RSS Feed。
- **GitHub Actions**: 提供自動化排程執行環境。

## 🚀 快速上手

### 1. 取得 Discord Webhook URL
在你的 Discord 頻道中：
`設定` -> `整合` -> `Webhook` -> `建立新的 Webhook` -> `複製 Webhook 網址`。

### 2. 設定 GitHub Secrets
如果你想在 GitHub 上自動運行，請在 Repo 的 `Settings` -> `Secrets and variables` -> `Actions` 中新增：
- `DISCORD_WEBHOOK_URL`: 填入剛才複製的 URL。

### 3. 本地執行
若要在本地測試，請先安裝依賴：
```bash
pip install -r requirements.txt
```
設定環境變數（Windows 範例）：
```powershell
$env:DISCORD_WEBHOOK_URL="你的網址"
python main.py
```

## 📂 檔案結構

- `main.py`: 程式進入點，整合 Steam 與 X 的爬蟲邏輯。
- `xscraper.py`: 負責監控 X (Twitter) 的 RSS 更新。
- `last_new_id.txt` / `LASTFILE.txt`: 用於紀錄最後一次發送的新聞 ID（請勿手動修改）。
- `.github/workflows/run.yml`: GitHub Actions 的排程設定檔。

## 📝 未來計畫
- [ ] 強化 Webhook 安全性。
- [ ] 使用正規表達式 (Regex) 優化 Steam 公告的內文清理。
- [ ] 加入更多新聞來源（如：官網）。

---

*本專案僅供學習交流使用。*
