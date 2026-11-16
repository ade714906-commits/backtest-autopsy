# AGENTS.md

本專案的完整規則在 **[CLAUDE.md](CLAUDE.md)**，那份是唯一權威。任何 AI 代理（Codex、Cursor、Gemini…）動手前請先讀完它。

最重要的五條摘要：

1. 新報告 = 複製 `templates/autopsy.html` → 存成 `autopsies/YYYY-MM-DD-slug.html`，六個區塊（hypothesis / why / rules / result / cause / lesson）順序與 id 不能改。
2. 在 `data/autopsies.js` 陣列最前面登記一筆，`slug` 必須和檔名一致。
3. 只寫真的算過的數字；報酬一律扣成本並附 t 值；沒資料寫「未測」。
4. 判決只有 `dead` / `alive` / `watch` 三種，已發佈的判決不准事後改。
5. 改完必跑 `python scripts/check.py`，顯示 `ALL CHECKS PASSED` 才算完成。
