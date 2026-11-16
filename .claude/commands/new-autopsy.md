---
description: 依 CLAUDE.md 規則新增一篇策略驗屍報告
argument-hint: <策略描述與測試結果>
---

請新增一篇驗屍報告，素材如下：

$ARGUMENTS

步驟（全部依照 CLAUDE.md，有衝突以 CLAUDE.md 為準）：

1. 讀 `CLAUDE.md` 第 3–7 節。
2. 決定判決日期與英文 slug，檔名 `autopsies/YYYY-MM-DD-slug.html`；先確認不和既有檔案重複。
3. 複製 `templates/autopsy.html`，填完六個區塊，換掉所有 `{{...}}`。
4. 素材裡沒有的數字一律寫「未測」或「—」，**不要自己補數字**。缺 t 值時在回覆中提醒我。
5. 在 `data/autopsies.js` 陣列最前面登記。
6. 若用到 `method.html` 沒有的名詞，補進名詞表。
7. 跑 `python scripts/check.py`，修到 `ALL CHECKS PASSED`。
8. 回報：新檔路徑、判決、一句話教訓。先不要 commit，等我確認。
