_path=(ROOT+'/sides.html')
_h=open(_path).read()
_css='''<style>
  .tgbar { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; margin: 4px 0 10px; }
  .tgbar .hint { flex: 1 1 100%; margin: 0 0 2px; font-size: 13px; line-height: 1.4; color: #5F5E5A; }
  .tgbar button { font: inherit; font-size: 13px; line-height: 1.3; padding: 4px 10px; border: 1px solid #B4B2A9; border-radius: 14px; background: #fff; color: #2C2C2A; cursor: pointer; }
  .tgbar button:hover { border-color: #2C2C2A; }
  .tgbar button.chip::before { content: ""; display: inline-block; width: 9px; height: 9px; border-radius: 50%; margin-right: 6px; background: var(--c, #888780); }
  .tgbar button.chip[aria-pressed="false"] { background: #F1EFE8; color: #888780; text-decoration: line-through; }
  .tgbar button.chip[aria-pressed="false"]::before { opacity: .35; }
  .tgbar button.all { background: #2C2C2A; border-color: #2C2C2A; color: #fff; }
  svg g.tg { cursor: pointer; }
  svg g.tg.off { display: none; }
  svg g.tg.hl, svg g.tg:hover { filter: drop-shadow(0 0 3px rgba(186, 117, 23, .95)); }
</style>
'''
_js='''<script>
(function () {
  document.querySelectorAll('svg').forEach(function (svg) {
    var groups = Array.prototype.slice.call(svg.querySelectorAll('g.tg'));
    if (!groups.length) return;
    var wrap = svg.closest('.wide') || svg.parentNode;
    var bar = document.createElement('div');
    bar.className = 'tgbar';
    var hint = document.createElement('p');
    hint.className = 'hint';
    hint.textContent = 'Click a part of the drawing to hide it, or use the buttons. A crossed-out button is hidden; click it to bring the part back.';
    bar.appendChild(hint);
    var chips = {};
    function set(g, show) {
      g.classList.toggle('off', !show);
      chips[g.dataset.g].setAttribute('aria-pressed', show ? 'true' : 'false');
    }
    function mkBtn(text, cls) {
      var b = document.createElement('button');
      b.type = 'button'; b.className = cls; b.textContent = text;
      return b;
    }
    var showAll = mkBtn('Show all', 'all'), hideAll = mkBtn('Hide all', 'all');
    showAll.onclick = function () { groups.forEach(function (g) { set(g, true); }); };
    hideAll.onclick = function () { groups.forEach(function (g) { set(g, false); }); };
    bar.appendChild(showAll); bar.appendChild(hideAll);
    groups.forEach(function (g) {
      var b = mkBtn(g.dataset.label, 'chip');
      var colored = g.querySelector('[stroke]:not([stroke="none"])');
      if (colored) b.style.setProperty('--c', colored.getAttribute('stroke'));
      b.setAttribute('aria-pressed', 'true');
      b.onclick = function () { set(g, g.classList.contains('off')); };
      b.onmouseenter = function () { g.classList.add('hl'); };
      b.onmouseleave = function () { g.classList.remove('hl'); };
      chips[g.dataset.g] = b;
      bar.appendChild(b);
      g.addEventListener('click', function (e) { e.stopPropagation(); set(g, false); g.classList.remove('hl'); });
    });
    wrap.parentNode.insertBefore(bar, wrap);
  });
})();
</script>
'''
assert '</head>' in _h and '</body>' in _h
_h=_h.replace('</head>',_css+'</head>',1)
_h=_h.replace('</body>',_js+'</body>',1)
_h=_h.replace('<h2>1. Driver side</h2>','<p><b>Interactive version:</b> <a href="interactive.html">open and close the doors, tables, the bed and the shower pan with a click, and change any size</a>.</p>\n<h2>1. Driver side</h2>',1)
open(_path,'w').write(_h)
