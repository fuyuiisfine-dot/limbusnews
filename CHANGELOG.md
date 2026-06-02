# 更新日誌 (CHANGELOG) 📝

本文件記錄了 「梅菲斯特情報號」 的開發歷程與重大更新。

## [v1.0.2] - 2024-05-31 (今日)
### Added
- 建立詳細的 `README.md` 文件，包含專案介紹、功能特點與快速上手指南。
- 建立 `CHANGELOG.md` 紀錄專案更新歷史。

## [v1.0.1] - 5天前
### Fixed
- 修正 GitHub Actions 腳本中的檔案名稱錯誤 (`--filename issue`)。
- 優化 YAML 工作流，確保 `LASTFILE.txt` 與 `last_new_id.txt` 能正確被提交回儲存庫。

## [v1.0.0] - 2週前
### Added
- **核心功能上線**：完成 Steam API 串接，可抓取邊獄公司官方新聞。
- **X 監控集成**：整合 `xscraper.py`，透過 RSS 監控 X (Twitter) 動態。
- **Discord 推播**：實現 Webhook 自動發送訊息，加入標誌性的 「Ciallo～(∠・ω< )⌒☆」 問候語。
- **自動化部署**：完成 GitHub Actions 配置，達成每 30 分鐘自動檢查。

## [v0.1.0] - 初期開發
### Added
- 專案初始化。
- 測試 Steam API 基本回傳結構。
- 實作簡單的 `last_id` 紀錄機制以防止重複發送。

---

> 「日誌在 obsidian」 —— 這裡是從 Git 歷史中整理出的精簡版。
