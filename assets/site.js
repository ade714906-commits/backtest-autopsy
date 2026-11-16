// 首頁：讀 data/autopsies.js 的 window.AUTOPSIES，畫卡片 + 篩選。規則見 CLAUDE.md
(function () {
  var list = (window.AUTOPSIES || []).slice().sort(function (a, b) {
    return a.date < b.date ? 1 : -1;
  });
  var LABEL = { dead: "死亡", alive: "存活", watch: "觀察中" };
  var cards = document.getElementById("cards");
  var filters = document.getElementById("filters");
  if (!cards) return;

  function esc(s) {
    return String(s).replace(/[&<>"]/g, function (c) {
      return { "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c];
    });
  }

  // 統計
  var count = { dead: 0, alive: 0, watch: 0 };
  list.forEach(function (a) { count[a.verdict]++; });
  document.getElementById("n-total").textContent = list.length;
  document.getElementById("n-dead").textContent = count.dead;
  document.getElementById("n-alive").textContent = count.alive;

  // 篩選按鈕：全部 + 三種判決 + 所有標籤
  var keys = ["all", "v:dead", "v:alive", "v:watch"];
  var tags = [];
  list.forEach(function (a) { a.tags.forEach(function (t) { if (tags.indexOf(t) < 0) tags.push(t); }); });
  tags.forEach(function (t) { keys.push("t:" + t); });
  var current = "all";

  function label(k) {
    if (k === "all") return "全部";
    if (k.indexOf("v:") === 0) return LABEL[k.slice(2)];
    return "#" + k.slice(2);
  }
  function match(a) {
    if (current === "all") return true;
    if (current.indexOf("v:") === 0) return a.verdict === current.slice(2);
    return a.tags.indexOf(current.slice(2)) >= 0;
  }
  function render() {
    filters.innerHTML = keys.map(function (k) {
      return '<button data-k="' + esc(k) + '" class="' + (k === current ? "on" : "") + '">' + esc(label(k)) + "</button>";
    }).join("");
    cards.innerHTML = list.filter(match).map(function (a) {
      return '<a class="card ' + a.verdict + '" href="autopsies/' + esc(a.slug) + '.html">' +
        '<span class="badge ' + a.verdict + '">' + LABEL[a.verdict] + "</span>" +
        '<span class="tag market">' + esc(a.market) + "</span>" +
        a.tags.map(function (t) { return '<span class="tag">' + esc(t) + "</span>"; }).join("") +
        "<h2>" + esc(a.title) + "</h2><p>" + esc(a.headline) + "</p>" +
        '<p class="date">判決日 ' + esc(a.date) + "</p></a>";
    }).join("") || "<p>這個分類還沒有報告。</p>";
  }
  filters.addEventListener("click", function (e) {
    var k = e.target.getAttribute && e.target.getAttribute("data-k");
    if (k) { current = k; render(); }
  });
  render();
})();
