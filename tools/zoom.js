/* zoom and pan for the diagrams: + / - / reset buttons in the corner, Ctrl (or Cmd) + scroll, pinch on a touch screen, drag to move once zoomed */
(function () {
  var CSS = '.zvp{position:relative;overflow:hidden}.zvp>svg{transform-origin:0 0}.zvp.zoomed{cursor:grab;touch-action:none}.zvp.zdrag{cursor:grabbing}' +
    '.zbar{position:absolute;top:6px;right:6px;z-index:5;display:flex;gap:4px}' +
    '.zbar button{font:inherit;font-size:15px;line-height:1;min-width:30px;height:30px;padding:0 9px;border:1px solid #B4B2A9;border-radius:6px;background:rgba(255,255,255,.93);color:#2C2C2A;cursor:pointer}' +
    '.zbar button:hover{border-color:#2C2C2A}.zbar button[disabled]{opacity:.4;cursor:default}';
  var st = document.createElement('style'); st.textContent = CSS; document.head.appendChild(st);
  var MAX = 8;
  function make(svg) {
    if (svg.__zoom || !svg.parentNode) return;
    var vp = document.createElement('div'); vp.className = 'zvp';
    svg.parentNode.insertBefore(vp, svg); vp.appendChild(svg);
    var k = 1, x = 0, y = 0, ptrs = {}, last = null, dragged = false, down = null;
    var bar = document.createElement('div'); bar.className = 'zbar';
    function btn(t, label, f) { var b = document.createElement('button'); b.type = 'button'; b.textContent = t; b.title = label; b.setAttribute('aria-label', label); b.onclick = function (e) { e.stopPropagation(); f(); }; bar.appendChild(b); return b; }
    var bIn = btn('+', 'Zoom in', function () { zoomAt(vp.clientWidth / 2, vp.clientHeight / 2, 1.5); });
    var bOut = btn('−', 'Zoom out', function () { zoomAt(vp.clientWidth / 2, vp.clientHeight / 2, 1 / 1.5); });
    var bReset = btn('Reset', 'Reset the zoom', reset);
    vp.appendChild(bar);
    function apply() {
      var cs = getComputedStyle(svg), sw = parseFloat(cs.width) || vp.clientWidth, sh = parseFloat(cs.height) || vp.clientHeight;
      x = Math.max(Math.min(0, vp.clientWidth - sw * k), Math.min(0, x));
      y = Math.max(Math.min(0, vp.clientHeight - sh * k), Math.min(0, y));
      if (k <= 1.001) { k = 1; x = 0; y = 0; }
      svg.style.transform = k === 1 ? '' : 'translate(' + x + 'px,' + y + 'px) scale(' + k + ')';
      vp.classList.toggle('zoomed', k > 1);
      if (k > 1) vp.scrollLeft = 0;
      bIn.disabled = k >= MAX - .01; bOut.disabled = bReset.disabled = k === 1;
    }
    function zoomAt(cx, cy, f) {
      var nk = Math.min(MAX, Math.max(1, k * f)); f = nk / k;
      x = cx - (cx - x) * f; y = cy - (cy - y) * f; k = nk; apply();
    }
    function reset() { k = 1; x = 0; y = 0; apply(); }
    svg.__zoom = true; svg.__zoomReset = reset;
    vp.addEventListener('wheel', function (e) {
      if (!(e.ctrlKey || e.metaKey)) return;
      e.preventDefault();
      var r = vp.getBoundingClientRect();
      zoomAt(e.clientX - r.left, e.clientY - r.top, Math.exp(-e.deltaY * (e.deltaMode === 1 ? .05 : .0025)));
    }, { passive: false });
    function dist() { var a = Object.keys(ptrs).map(function (i) { return ptrs[i]; }); return Math.hypot(a[0].x - a[1].x, a[0].y - a[1].y); }
    function mid() { var a = Object.keys(ptrs).map(function (i) { return ptrs[i]; }); return { x: (a[0].x + a[1].x) / 2, y: (a[0].y + a[1].y) / 2 }; }
    var listening = false;
    function mv(ev) {
      var p = ptrs[ev.pointerId]; if (!p) return;
      var n = Object.keys(ptrs).length, r = vp.getBoundingClientRect();
      if (n === 2 && last) {
        p.x = ev.clientX; p.y = ev.clientY;
        var d = dist(), m = mid();
        x += m.x - last.m.x; y += m.y - last.m.y;
        zoomAt(m.x - r.left, m.y - r.top, d / last.d); last = { d: d, m: m }; dragged = true;
      } else if (n === 1 && k > 1) {
        if (Math.hypot(ev.clientX - down.x, ev.clientY - down.y) > 4) { dragged = true; vp.classList.add('zdrag'); }
        if (dragged) { x += ev.clientX - p.x; y += ev.clientY - p.y; apply(); }
        p.x = ev.clientX; p.y = ev.clientY;
      } else { p.x = ev.clientX; p.y = ev.clientY; }
    }
    function up(ev) {
      delete ptrs[ev.pointerId]; last = null; vp.classList.remove('zdrag');
      if (!Object.keys(ptrs).length) { listening = false; window.removeEventListener('pointermove', mv); window.removeEventListener('pointerup', up); window.removeEventListener('pointercancel', up); }
    }
    vp.addEventListener('pointerdown', function (e) {
      if (e.target.closest('.zbar')) return;
      if (!Object.keys(ptrs).length) dragged = false;
      ptrs[e.pointerId] = { x: e.clientX, y: e.clientY }; down = { x: e.clientX, y: e.clientY };
      last = Object.keys(ptrs).length === 2 ? { d: dist(), m: mid() } : null;
      if (!listening) { listening = true; window.addEventListener('pointermove', mv); window.addEventListener('pointerup', up); window.addEventListener('pointercancel', up); }
    });
    // a drag is not a click: keep it from toggling or opening whatever is under the pointer
    vp.addEventListener('click', function (e) { if (dragged) { e.stopPropagation(); e.preventDefault(); dragged = false; } }, true);
    window.addEventListener('resize', apply);
  }
  window.makeZoomable = make;
  window.zoomAll = function () { document.querySelectorAll('svg[role="img"]').forEach(make); };
})();
