# 回測驗屍室 Backtest Autopsy

> 大部分策略都死了。這裡記錄它們是怎麼死的。

一個交易策略「驗屍報告」知識庫網站。每一篇記錄一個被認真測過的交易想法：為什麼看起來會賺、扣掉成本後實際怎樣、死因是什麼。

🔗 **網站**：https://ade714906-commits.github.io/backtest-autopsy/ （以 GitHub Pages 發佈）

## 這個專案的重點不是網頁，是規則

這個 repo 的設計目標是：**讓 AI 讀完 [`CLAUDE.md`](CLAUDE.md) 之後，就能自己照同一套格式繼續加新報告**，不需要每次重新解釋。

| 檔案 | 作用 |
|---|---|
| [`CLAUDE.md`](CLAUDE.md) | 專案憲法：目的、結構、命名、六段式報告格式、數字誠實規則、風格、禁止事項 |
| [`AGENTS.md`](AGENTS.md) | 給其他 AI 工具的入口，摘要五條最重要規則並指向 CLAUDE.md |
| [`templates/autopsy.html`](templates/autopsy.html) | 唯一範本，新報告一律從這裡複製 |
| [`data/autopsies.js`](data/autopsies.js) | 報告索引，首頁卡片與篩選都從這裡產生 |
| [`scripts/check.py`](scripts/check.py) | 把規則變成可執行檢查：檔名、區塊順序、判決一致、禁用字、路徑… |
| [`.claude/commands/new-autopsy.md`](.claude/commands/new-autopsy.md) | Claude Code 指令 `/new-autopsy <素材>`，一行觸發整個新增流程 |

## 新增一篇報告

```bash
# 在 Claude Code 裡
/new-autopsy 測了「月底買高股息 ETF」，探索期淨 +0.1%/筆 t 0.4 ...

# 或手動：複製範本 → 填六區塊 → 登記索引 → 驗證
python scripts/check.py
```

## 本機預覽

純靜態網站，直接用瀏覽器打開 `index.html` 即可，或：

```bash
python -m http.server 8000
```

---

本站內容為個人回測研究紀錄，僅供學習「如何檢驗策略」，不構成任何投資建議。
