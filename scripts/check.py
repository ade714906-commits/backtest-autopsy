"""回測驗屍室 驗證腳本 — 把 CLAUDE.md 的規則變成可執行的檢查。

用法：python scripts/check.py
全部通過會印出 ALL CHECKS PASSED，否則列出每個錯誤並以 exit code 1 結束。
"""
import io
import json
import os
import re
import sys

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")  # Windows 終端機中文不亂碼

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECTIONS = ["hypothesis", "why", "rules", "result", "cause", "lesson"]  # CLAUDE.md 第 3 節
VERDICTS = {"dead": "死亡", "alive": "存活", "watch": "觀察中"}
KNOWN_TAGS = {"事件", "籌碼", "基本面", "動能", "選擇權", "預測"}  # CLAUDE.md 第 5 節
BANNED = ["推薦買進", "必賺", "保證獲利", "穩賺", "明牌"]  # CLAUDE.md 第 7 節
SLUG_RE = re.compile(r"^\d{4}-\d{2}-\d{2}-[a-z0-9]+(-[a-z0-9]+)*$")

errors = []
warnings = []


def read(path):
    with io.open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def load_index():
    js = read("data/autopsies.js")
    body = js[js.index("[") : js.rindex("]") + 1]
    body = re.sub(r"^\s*//.*$", "", body, flags=re.M)
    body = re.sub(r"(\w+):", r'"\1":', body)  # key: -> "key":
    body = re.sub(r",\s*([}\]])", r"\1", body)  # 尾逗號
    return json.loads(body)


index = load_index()
slugs = [a["slug"] for a in index]
files = sorted(f[:-5] for f in os.listdir(os.path.join(ROOT, "autopsies")) if f.endswith(".html"))

# 1. 索引與檔案一一對應
for s in set(slugs) - set(files):
    errors.append("索引有 %s，但 autopsies/ 找不到檔案" % s)
for s in set(files) - set(slugs):
    errors.append("autopsies/%s.html 沒有登記到 data/autopsies.js" % s)
if len(slugs) != len(set(slugs)):
    errors.append("data/autopsies.js 有重複的 slug")
if [a["date"] for a in index] != sorted([a["date"] for a in index], reverse=True):
    errors.append("data/autopsies.js 沒有依日期由新到舊排列")

# 2. 每筆索引欄位
for a in index:
    s = a.get("slug", "?")
    for k in ["slug", "title", "date", "market", "verdict", "tags", "headline"]:
        if k not in a:
            errors.append("%s 缺欄位 %s" % (s, k))
    if not SLUG_RE.match(s):
        errors.append("%s 檔名格式錯誤，應為 YYYY-MM-DD-小寫英文-連字號" % s)
    if not s.startswith(a.get("date", "")):
        errors.append("%s 的 date 與檔名日期不一致" % s)
    if a.get("verdict") not in VERDICTS:
        errors.append("%s 的 verdict 必須是 dead/alive/watch" % s)
    if not 1 <= len(a.get("tags", [])) <= 3:
        errors.append("%s 標籤數量應為 1–3 個" % s)
    for t in a.get("tags", []):
        if t not in KNOWN_TAGS:
            warnings.append("%s 用了新標籤「%s」，若是刻意新增請更新 CLAUDE.md 與 check.py" % (s, t))
    if len(a.get("headline", "")) > 40:
        errors.append("%s 的 headline 超過 40 字" % s)

# 3. 每篇報告頁的結構
for a in index:
    s = a["slug"]
    if s not in files:
        continue
    html = read("autopsies/%s.html" % s)
    ids = re.findall(r'<section id="([a-z]+)"', html)
    if ids != SECTIONS:
        errors.append("%s 區塊順序應為 %s，實際為 %s" % (s, SECTIONS, ids))
    if "{{" in html:
        errors.append("%s 還有沒替換的範本佔位符 {{...}}" % s)
    h1 = re.search(r"<h1>(.*?)</h1>", html)
    if not h1 or h1.group(1) != a["title"]:
        errors.append("%s 的 <h1> 與索引 title 不一致" % s)
    badge = re.search(r'<span class="badge (\w+)">(.*?)</span>', html)
    if not badge or badge.group(1) != a["verdict"] or badge.group(2) != VERDICTS[a["verdict"]]:
        errors.append("%s 的判決徽章與索引 verdict 不一致" % s)
    if "<table>" not in html.split('id="result"')[1].split("</section>")[0]:
        errors.append("%s 的結果區塊必須有表格" % s)
    lesson = re.search(r'<blockquote class="lesson">(.*?)</blockquote>', html, re.S)
    if not lesson:
        errors.append("%s 缺少一句話教訓 blockquote.lesson" % s)
    elif len(lesson.group(1).strip()) > 30:
        errors.append("%s 的教訓超過 30 字" % s)
    if "不構成任何投資建議" not in html:
        errors.append("%s 缺少頁尾免責聲明" % s)
    if 'style="' in html:
        errors.append("%s 使用了 inline style（請改用 style.css 的 class）" % s)
    if re.search(r'(href|src)="/', html):
        errors.append("%s 有用 / 開頭的絕對路徑，GitHub Pages 子路徑下會壞" % s)

# 4. 全站禁用字與外部腳本
for path in ["index.html", "method.html"] + ["autopsies/%s.html" % f for f in files]:
    html = read(path)
    for w in BANNED:
        if w in html:
            errors.append("%s 出現禁用字「%s」" % (path, w))
    for src in re.findall(r'<script[^>]+src="([^"]+)"', html):
        if src.startswith("http"):
            errors.append("%s 引入了外部腳本 %s" % (path, src))

for w in warnings:
    print("WARN  " + w)
for e in errors:
    print("ERROR " + e)
if errors:
    print("\n%d 個錯誤，請修正後再跑一次。" % len(errors))
    sys.exit(1)
print("檢查了 %d 篇報告。ALL CHECKS PASSED" % len(index))
