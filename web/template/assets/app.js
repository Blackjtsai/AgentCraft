/* AgentCraft 前台 Template — 極簡互動（僅示意流程，無後端） */
(function () {
  // 分頁切換：<div class="tabs" data-tabs> 按鈕 aria-controls 指向面板 id
  document.querySelectorAll('[data-tabs]').forEach(function (tabs) {
    var buttons = tabs.querySelectorAll('button[aria-controls]');
    buttons.forEach(function (btn) {
      btn.addEventListener('click', function () {
        buttons.forEach(function (b) {
          b.setAttribute('aria-selected', b === btn ? 'true' : 'false');
          var panel = document.getElementById(b.getAttribute('aria-controls'));
          if (panel) panel.hidden = b !== btn;
        });
      });
    });
  });

  // 通用顯示切換：<button data-toggle="#id">
  document.querySelectorAll('[data-toggle]').forEach(function (btn) {
    btn.addEventListener('click', function () {
      var el = document.querySelector(btn.getAttribute('data-toggle'));
      if (el) el.hidden = !el.hidden;
    });
  });

  // 示意：寄送登入連結後顯示成功訊息
  var sendForm = document.getElementById('send-link-form');
  if (sendForm) {
    sendForm.addEventListener('submit', function (e) {
      e.preventDefault();
      document.getElementById('send-link-form').hidden = true;
      document.getElementById('link-sent').hidden = false;
    });
  }

  // 首次互動導覽（示意）：依序高亮 data-coach 的元素
  var steps = [].slice.call(document.querySelectorAll('[data-coach]'))
    .sort(function (a, b) { return +a.getAttribute('data-coach-order') - +b.getAttribute('data-coach-order'); });
  var startBtn = document.getElementById('start-tour');
  if (startBtn && steps.length) {
    var backdrop, pop, idx = 0;
    function clear() { steps.forEach(function (s) { s.classList.remove('coach-target'); }); }
    function end() { clear(); if (backdrop) backdrop.remove(); if (pop) pop.remove(); backdrop = pop = null; }
    function show() {
      clear();
      var s = steps[idx];
      s.classList.add('coach-target');
      s.scrollIntoView({ block: 'center', behavior: 'smooth' });
      pop.querySelector('[data-pop-title]').textContent = '（' + (idx + 1) + '／' + steps.length + '）' + s.getAttribute('data-coach');
      pop.querySelector('[data-pop-text]').textContent = s.getAttribute('data-coach-text');
      pop.querySelector('[data-next]').textContent = idx === steps.length - 1 ? '完成' : '下一步';
    }
    startBtn.addEventListener('click', function () {
      idx = 0;
      backdrop = document.createElement('div'); backdrop.className = 'coach-backdrop';
      pop = document.createElement('div'); pop.className = 'coach-pop card';
      pop.innerHTML = '<h3 data-pop-title></h3><p data-pop-text></p><div class="row spread">' +
        '<button class="btn ghost sm" data-skip>跳過導覽</button><button class="btn primary sm" data-next>下一步</button></div>';
      document.body.appendChild(backdrop); document.body.appendChild(pop);
      pop.querySelector('[data-skip]').onclick = end;
      backdrop.onclick = end;
      pop.querySelector('[data-next]').onclick = function () { if (idx >= steps.length - 1) end(); else { idx++; show(); } };
      show();
    });
  }
})();
