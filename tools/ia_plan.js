/* ================= walkway model: what sticks out into the aisle right now ================= */
// D = things on the driver side (depth from the driver wall), Q = things on the passenger side (depth from the passenger wall)
function obstacles(L, V) {
  const P = L.P, D = [], Q = [], rad = Math.PI / 180;
  const sb = V.bed || 0;
  D.push({ x0: 0, x1: L.c0, d: P.bedD + P.bedBack * bedState(sb).ext, n: sb > .02 ? 'the bed (made up)' : 'the bed' });
  D.push({ x0: L.c0, x1: L.c1, d: P.closetD, n: 'the closet' });
  D.push({ x0: L.bA[0], x1: L.bA[1], d: P.benchD, n: 'the bench' });
  if (L.tableLen > 0) D.push({ x0: L.tbl[0], x1: L.tbl[1], d: P.tableD, n: 'the dinette table' });
  D.push({ x0: L.bB[0], x1: L.bB[1], d: P.benchD, n: 'the bench' });
  const hx = P.hinge === 'rear' ? L.c0 + 0.125 : L.c1 - 0.125, wC = P.closetW - 0.25, sg = P.hinge === 'rear' ? 1 : -1;
  ['clo_lo', 'clo_hi'].forEach(id => {
    const s = V[id] || 0; if (s < .02) return;
    const th = s * P.openAng * rad;
    for (let k = 0; k <= 24; k++) { const r = wC * k / 24; D.push({ x0: hx + sg * r * Math.cos(th) - .4, x1: hx + sg * r * Math.cos(th) + .4, d: P.closetD + r * Math.sin(th), n: 'the closet door', door: true, px: hx + sg * r * Math.cos(th) }); }
  });
  const sp = V.pan || 0;
  Q.push({ x0: 0, x1: P.panW, d: 3.5 + (P.panD - 3.5) * (1 - sp), n: sp > .5 ? 'the shower pan (tipped up)' : 'the shower pan' });
  Q.push({ x0: L.fr[0], x1: L.fr[1], d: P.cabD, n: 'the fridge' });
  const sf = V.fridge || 0;
  if (sf > .02) {
    const th = sf * Math.PI / 2;
    for (let k = 0; k <= 24; k++) { const r = P.fridgeW * k / 24; Q.push({ x0: L.fr[0] + r * Math.cos(th) - .4, x1: L.fr[0] + r * Math.cos(th) + .4, d: P.cabD + r * Math.sin(th), n: 'the fridge door' }); }
  }
  Q.push({ x0: L.cabS, x1: L.angS, d: P.cabD, n: 'the cabinet' });
  for (let x = L.angS; x < L.sinkS - 1e-9; x += .5) Q.push({ x0: x, x1: x + .5, d: Math.max(P.sinkD, P.cabD - L.slope * (x + .25 - L.angS)), n: 'the angled cabinet front' });
  Q.push({ x0: L.sinkS, x1: L.sinkE, d: P.sinkD, n: 'the sink counter' });
  const fo = V.flap || 0;
  if (fo > .02) Q.push({ x0: L.sinkE, x1: L.sinkE + .75 + (L.flapLen - .75) * Math.sin(fo * Math.PI / 2), d: P.flapD, n: 'the fold-out table' });
  if ((V.ledge || 0) > .02) Q.push({ x0: L.sinkE, x1: L.sinkE + L.ledgeTot * Math.sin((V.ledge || 0) * Math.PI / 2), d: P.sinkD, n: 'the foot ledge' });
  return { D, Q };
}
function depthAt(list, x) { let m = 0, n = ''; for (const o of list) if (x >= o.x0 && x <= o.x1 && o.d > m) { m = o.d; n = o.n; } return { m, n }; }
function aisleAt(L, O, x) { const a = depthAt(O.D, x), b = depthAt(O.Q, x); return { v: L.P.vanW - a.m - b.m, dn: a.n, qn: b.n, dm: a.m, qm: b.m }; }
function aisleMin(L, O) {
  let best = { v: 1e9 };
  for (let x = 0; x <= L.P.cab + 1e-9; x += .25) { const r = aisleAt(L, O, x); if (r.dm > 0 && r.qm > 0 && r.v < best.v) best = Object.assign({ x }, r); }
  return best;
}
// does an open closet door run into the bed, a bench or the table?
function doorHits(L, O) {
  const hits = new Set();
  O.D.filter(o => o.door).forEach(p => {
    O.D.filter(o => !o.door && o.n !== 'the closet').forEach(r => { if (p.px >= r.x0 && p.px <= r.x1 && p.d < r.d) hits.add(r.n); });
  });
  return [...hits];
}

/* ================= plan view (looking down) ================= */
function drawPlan(L, V) {
  const P = L.P, S = 6, X0 = 60, Y0 = 64, Wd = P.vanW;
  const xx = x => X0 + S * x, yy = d => Y0 + S * d;     // d: distance from the driver wall
  const yp = d => yy(Wd - d);                            // d: distance from the passenger wall
  const o = [], W = xx(P.cab) + 100, H = yy(Wd) + 60;
  const it = (x0, x1, y0, y1, col, label, sub, op) => {
    op = op || {};
    let g = R(xx(x0), yy(y0), S * (x1 - x0), S * (y1 - y0), { rx: 2, fill: col, fo: op.fo == null ? .14 : op.fo, stroke: col, sw: 1.6, dash: op.dash });
    const cx = xx((x0 + x1) / 2), cy = yy((y0 + y1) / 2);
    if (label) g += T(cx, cy, label, { size: op.fs || 11, fill: col, w: 500 });
    if (sub) g += T(cx, cy + 13, sub, { size: 9.5, fill: col });
    return g;
  };
  const ip = (x0, x1, d0, d1, col, label, sub, op) => it(x0, x1, Wd - d1, Wd - d0, col, label, sub, op);
  o.push(T(X0, 18, 'Looking down into the van. Rear doors on the left, cab on the right, driver side wall at the top, passenger side wall at the bottom. Click things to open them.', { anchor: 'start', size: 13, fill: '#5F5E5A', halo: false }));
  o.push(T(xx(P.cab / 2), yy(0) - 30, 'DRIVER SIDE WALL', { size: 13, fill: COL.G, w: 500, halo: false }));
  o.push(T(xx(P.cab / 2), yy(Wd) + 34, 'PASSENGER SIDE WALL', { size: 13, fill: COL.G, w: 500, halo: false }));
  for (let t = 0; t <= P.cab; t += 10) { o.push(Ln(xx(t), yy(0), xx(t), yy(Wd), { stroke: '#3F3E3A', so: .22, dash: '3 3', sw: 1 })); o.push(T(xx(t), yy(0) - 8, t + '→', { size: 10, fill: '#185FA5', w: 700, halo: false })); }
  for (let d = 0; d <= Wd; d += 10) { o.push(Ln(xx(0), yy(d), xx(P.cab), yy(d), { stroke: '#3F3E3A', so: .22, dash: '3 3', sw: 1 })); o.push(T(xx(0) - 6, yy(d) + 4, d + '↓', { anchor: 'end', size: 10, fill: '#8A4B0F', w: 700, halo: false })); }
  o.push(R(xx(0), yy(0), S * P.cab, S * Wd, { fill: '#F1EFE8', fo: .7, stroke: '#5F5E5A', sw: 2 }));
  o.push(T(xx(0) + 3, yy(Wd) + 14, 'rear doors', { anchor: 'start', size: 10, fill: '#5F5E5A', halo: false }));
  o.push(R(xx(P.cab - 4), yy(0), S * 4, S * Wd, { fill: 'url(#hq)', fo: .35 }));
  o.push(Ln(xx(P.cab), yy(0), xx(P.cab), yy(Wd), { stroke: '#5F5E5A', sw: 2, dash: '6 3' }));
  o.push(T(xx(P.cab) - 3, yy(Wd) + 14, `cab wall at ${fmt(P.cab)} (could be off by 2 to 4 in)`, { anchor: 'end', size: 10, fill: '#5F5E5A', halo: false }));
  // ---------- driver side ----------
  const sb = V.bed || 0;
  {
    const bs = bedState(sb);
    let g = R(xx(0), yy(P.bedD), S * P.bedLen, S * P.bedBack * bs.ext, { fill: COL.P, fo: .14, stroke: COL.P, sw: 1.6 });
    if (bs.legs > .02) legXs(P).forEach(lx => { g += R(xx(lx), yy(P.bedD + P.bedBack - P.legIn - .6), S * 1.25, S * 1.25, { fill: '#B07A2A', fo: .9 * bs.legs, stroke: '#5A3A00', sw: 1 }); });
    g += R(xx(0), yy(P.bedD), S * P.bedLen, S * P.bedBack, { fill: COL.P, fo: .05, stroke: COL.P, sw: 1.6, dash: '6 4' });
    g += it(0, P.bedLen, 0, P.bedD, COL.P, 'Bed / couch', `${fmt(P.bedLen)} x ${fmt(P.bedD)}, platform ${fmt(P.platform)}, mattress top ${fmt(P.platform + P.mattress)}`, { fo: .12 });
    g += T(xx(P.bedLen * .7), yy(P.bedD + P.bedBack * .67), `bed made up with the leaf: ${fmt(P.bedLen)} x ${fmt(P.bedD + P.bedBack)}`, { size: 10.5, fill: COL.P, w: 500 });
    o.push(MV('bed', g, HITR(xx(0), yy(0), S * P.bedLen, S * (P.bedD + P.bedBack))));
  }
  o.push(Ln(xx(L.c0 + 2), yy(P.closetD / 2), xx(L.c1 - 2), yy(P.closetD / 2), { stroke: COL.G, sw: 3.5, cap: 'round' }));
  o.push(it(L.c0, L.c1, 0, P.closetD, COL.G, 'Closet', `${fmt(P.closetW)} x ${fmt(P.closetD)}, 2 rods`, { fo: .14 }));
  {
    const ds = dinState(V.dinette || 0), tt = P.tableH + (L.tableLow - P.tableH) * ds.tbl, bw = Math.min(P.benchD, P.tableD);
    let g = it(L.bA[0], L.bA[1], 0, P.benchD, COL.K, 'Bench', `${fmt(P.benchLen)} x ${fmt(P.benchD)}, seat ${fmt(P.seatH)} up`);
    if (L.tableLen > 0) g += it(L.tbl[0], L.tbl[1], 0, P.tableD, COL.G, 'Table', `${fmt(L.tableLen)} x ${fmt(P.tableD)}, ${fmt(tt)} up`);
    g += it(L.bB[0], L.bB[1], 0, P.benchD, COL.K, 'Bench', `${fmt(P.benchLen)} x ${fmt(P.benchD)}, seat ${fmt(P.seatH)} up`);
    if (ds.pil > .02 && L.tableLen > 0) {
      g += R(xx(L.tbl[0]), yy(0), S * L.tableLen, S * P.tableD, { fill: COL.K, fo: .3 * ds.pil, stroke: COL.K, sw: 1.4, rx: 2, so: ds.pil });
      g += T(xx((L.tbl[0] + L.tbl[1]) / 2), yy(P.tableD) - 5, 'backrest cushions laid flat', { size: 9, fill: COL.K, op: ds.pil });
    }
    if (ds.pil > .3) {
      g += R(xx(L.bA[0]), yy(0), S * (L.bB[1] - L.bA[0]), S * bw, { stroke: COL.K, sw: 2.2, dash: '7 4', so: ds.pil });
      g += T(xx((L.bA[0] + L.bB[1]) / 2), yy(bw) + 14, `dinette bed ${fmt(L.bB[1] - L.bA[0])} x ${fmt(bw)}`, { size: 11, fill: COL.K, w: 500, op: ds.pil });
    }
    o.push(MV('dinette', g, ''));
  }
  o.push(it(42, 76, 0, 7, COL.W2, 'Wheel well', '34 x 7, 7.5 tall', { fo: .5, fs: 10 }));
  o.push(it(L.batt[0], L.batt[1], 7, 17, COL.B, 'Battery', '21 x 10 x 9.5', { fo: .5, fs: 10 }));
  o.push(Ln(xx(50), yy(0), xx(50), yy(17), { stroke: '#A32D2D', sw: 1.5, mk: 1 }) + T(xx(48.6), yy(10), '17', { anchor: 'end', size: 10, fill: '#A32D2D', w: 700, halo: false }));
  // closet doors in plan: a line swinging out from the hinge, with the dashed sweep
  const hx = P.hinge === 'rear' ? L.c0 + 0.125 : L.c1 - 0.125, wC = P.closetW - 0.25, sg = P.hinge === 'rear' ? 1 : -1;
  [['clo_lo', COL.G, 1], ['clo_hi', '#7A7A72', .8]].forEach(dd => {
    const s = V[dd[0]] || 0, th = s * P.openAng * Math.PI / 180;
    const tip = [hx + sg * wC * Math.cos(th), P.closetD + wC * Math.sin(th)];
    let g = '';
    if (s > .01) {
      const a0 = [hx + sg * wC, P.closetD];
      g += `<path d="M${f1(xx(a0[0]))} ${f1(yy(a0[1]))} A${f1(S * wC)} ${f1(S * wC)} 0 ${th > Math.PI ? 1 : 0} ${sg > 0 ? 1 : 0} ${f1(xx(tip[0]))} ${f1(yy(tip[1]))}" fill="none" stroke="${dd[1]}" stroke-width="1.2" stroke-dasharray="3 3"/>`;
    }
    g += Ln(xx(hx), yy(P.closetD), xx(tip[0]), yy(tip[1]), { stroke: dd[1], sw: 4, cap: 'round' });
    o.push(MV(dd[0], g, ''));
  });
  if ((V.clo_lo || 0) + (V.clo_hi || 0) > .05) o.push(T(xx((L.c0 + L.c1) / 2), yy(P.closetD + wC + 6), 'closet door open', { size: 9.5, fill: COL.G }));
  else o.push(T(xx((L.c0 + L.c1) / 2), yy(P.closetD + 4), 'click to open', { size: 9, fill: '#5F5E5A' }));
  // ---------- passenger side ----------
  const sp = V.pan || 0, panDepth = 3.5 + (P.panD - 3.5) * (1 - sp);
  {
    let g = ip(0, P.panW, 0, panDepth, COL.T, 'Fold-up shower', sp > .5 ? 'tipped up against the wall' : `${fmt(P.panW)} x ${fmt(P.panD)} open, folds into the side wall`, { fo: .08, dash: '6 4' });
    o.push(MV('pan', g, HITR(xx(0), yp(P.panD), S * P.panW, S * P.panD)));
  }
  const nkx = Math.min(29.75, P.panW - 6.25);
  o.push(ip(6, nkx, 0, 4.5, '#7A4A1E', '', null, { fo: .3, dash: '3 2' }));
  o.push(T(xx((6 + nkx) / 2), yp(1.3), 'shower nook 4.5 deep', { size: 8.5, fill: '#5A3510' }));
  o.push(T(xx(L.cabS + 8), yp(P.cabD - 3.5), `Cabinet ${fmt(P.cabD)} deep`, { size: 10, fill: COL.C, w: 500 }));
  o.push(Poly([[xx(L.cabS), yp(P.cabD)], [xx(L.angS), yp(P.cabD)], [xx(L.sinkS), yp(P.sinkD)], [xx(L.sinkE), yp(P.sinkD)], [xx(L.sinkE), yp(0)], [xx(L.cabS), yp(0)]], { fill: COL.C, fo: .12, stroke: COL.C, sw: 1.6 }));
  const fgap = Math.max(0, P.cabD - P.fridgeD);
  o.push(ip(L.fr[0], L.fr[1], fgap, fgap + P.fridgeD, '#0A6A8A', '', null, { fo: .3 }));
  o.push(T(xx((L.fr[0] + L.fr[1]) / 2), yp(P.cabD - 3.5), `Fridge ${fmt(P.fridgeW)} x ${fmt(P.fridgeD)} x ${fmt(P.fridgeH)}`, { size: 10, fill: '#0A6A8A', w: 500 }));
  o.push(ip(L.sinkS, L.sinkE, 0, P.sinkD, COL.C, 'Sink', `${fmt(P.sinkW)} x ${fmt(P.sinkD)} counter`, { fo: .12, fs: 10 }));
  {
    const sfl = V.flap || 0, w = .75 + (L.flapLen - .75) * Math.sin(sfl * Math.PI / 2);
    let g = ip(L.sinkE, L.sinkE + w, 0, P.flapD, '#8A5A00', sfl > .5 ? 'Fold-out table' : '', sfl > .5 ? `${fmt(L.flapLen)} x ${fmt(P.flapD)}, ${fmt(P.flapH)} up (open)` : '', { fo: .2, dash: sfl > .98 ? '5 3' : '', fs: 10 });
    if (sfl < .5) g += T(xx(L.sinkE + 3), yp(P.flapD + 3), 'fold-out table (folded)', { anchor: 'start', size: 9.5, fill: '#8A5A00', op: 1 - sfl * 2 });
    o.push(MV('flap,ledge', g, HITR(xx(L.sinkE), yp(P.flapD), S * Math.max(w, 6), S * P.flapD)));
  }
  {
    const sl = V.ledge || 0, lw = L.ledgeTot * Math.sin(sl * Math.PI / 2);
    if (sl > .02) {
      o.push(ip(L.sinkE, L.sinkE + lw, 0, P.sinkD, '#5A3A00', '', null, { fo: .14, dash: '2 2' }));
      if (sl > .8) o.push(T(xx(L.sinkE + P.ledgeOff + P.ledgeLen / 2), yp(1.3), `foot platform ${fmt(P.ledgeLen)} (starts ${fmt(P.ledgeOff)} from the end)`, { size: 8, fill: '#5A3A00' }));
    }
  }
  o.push(ip(L.fr[0], L.fr[1], 0, P.cabD, '#8A6B4D', '', null, { fo: .08, dash: '6 3' }));
  o.push(ip(L.microX[0] + 1.75, L.microX[1] - 1.75, P.microIn, P.microIn + 12, COL.G, '', null, { fo: .2, dash: '4 3' }));
  o.push(T(xx((L.microX[0] + L.microX[1]) / 2), yp(5.5 + P.microIn), 'Microwave 18.5 x 12', { size: 9, fill: COL.G, w: 500 }));
  o.push(ip(42, 76, 0, 7, COL.W2, '', null, { fo: .3 }));
  o.push(ip(L.tankX[0], L.tankX[1], P.tankBack, P.tankBack + P.tankD, COL.BL, '', null, { fo: .1, dash: '5 3' }));
  o.push(ip(L.hotX[0], L.hotX[1], P.hotBack, P.hotBack + P.hotD, '#C0392B', '', null, { fo: .2, dash: '4 3' }));
  // the hot and cold fittings and the relief valve are on the back of the tank, in the gap to the wall
  [['C', .2, '#185FA5'], ['H', .5, '#C0392B'], ['R', .8, '#444441']].forEach(([n, f, col]) => { const fx = L.hotX[0] + f * P.hotW; o.push(`<circle cx="${f1(xx(fx))}" cy="${f1(yp(P.hotBack / 2))}" r="3.4" fill="${col}"/>`); o.push(T(xx(fx), yp(P.hotBack / 2) + 12, n, { size: 8, fill: col, halo: false })); });
  if (P.drainOn && P.hotShelf > 10) {
    const rx = L.hotX[0] + .8 * P.hotW, dy = P.tankBack + P.tankD + 2.5, st = { stroke: '#0F6E56', sw: 2, dash: '4 2' };
    o.push(Ln(xx(rx), yp(P.hotBack / 2), xx(rx), yp(dy), st)); o.push(Ln(xx(rx), yp(dy), xx(P.drainX), yp(dy), st));
    o.push(`<circle cx="${f1(xx(P.drainX))}" cy="${f1(yp(dy))}" r="4" fill="none" stroke="#0F6E56" stroke-width="2"/>`);
    o.push(T(xx(P.drainX), yp(dy) + 11, 'drain down', { size: 8, fill: '#0F6E56' }));
  }
  o.push(T(xx((L.hotX[0] + L.hotX[1]) / 2), yp(P.hotBack + P.hotD / 2) + 3, `hot water tank ${fmt(P.hotW)} x ${fmt(P.hotD)}`, { size: 8.5, fill: '#C0392B' }));
  // drawer footprints: drawers that stand over each other share one (a column)
  const cols = {};
  L.parts.filter(p => p.kind === 'drawer').forEach(p => { const k = f1(p.x0) + '|' + f1(p.x1); (cols[k] = cols[k] || { x0: p.x0, x1: p.x1, ids: [] }).ids.push(p.id); });
  Object.values(cols).forEach(c => o.push(ip(c.x0, c.x1, 0, 20, '#8A5A00', '', null, { fo: .15, dash: '3 2' })));
  o.push(T(xx(L.cabS + 14.75), yp(10), `${L.parts.filter(p => p.kind === 'drawer').length} drawers, 20 deep`, { size: 8.5, fill: '#8A5A00' }));
  o.push(`<circle cx="${f1(xx(L.sinkS + 8))}" cy="${f1(yp(.9))}" r="3.5" fill="#185FA5"/>`);
  o.push(ip(58, 93.25, 0, 4.5, '#7A4A1E', '', null, { fo: .3, dash: '3 2' }));
  o.push(T(xx(66), yp(1.3), 'nook 4.5 deep', { size: 8.5, fill: '#5A3510' }));
  o.push(T(xx((L.tankX[0] + L.tankX[1]) / 2), yp(P.tankBack + 6.5), `Fresh water tank ${fmt(L.tankLen)} x ${fmt(P.tankD)}`, { size: 9.5, fill: COL.BL, w: 500 }));
  o.push(T(xx((L.tankX[0] + L.tankX[1]) / 2), yp(P.tankBack + 3.5), 'on the floor, out of the open sink cabinet', { size: 9, fill: COL.BL }));
  o.push(T(xx(53), yp(1.8), 'wheel well 7 out', { size: 9, fill: '#3E230B' }));
  // paper towel roll on the angled front
  const nrm = [L.slope, -1], nl = Math.hypot(nrm[0], nrm[1]), nu = [nrm[0] / nl, nrm[1] / nl];
  const FP = (x, off) => [x + off * nu[0], (Wd - P.cabD) + L.slope * (x - L.angS) + off * nu[1]];
  const t0 = L.sinkS - 11.5, t1 = L.sinkS - .5;
  o.push(Poly([FP(t0, -.5), FP(t1, -.5), FP(t1, -6), FP(t0, -6)].map(p => [xx(p[0]), yy(p[1])]), { fill: '#B07A2A', fo: .35, stroke: '#8A5A00', sw: 1.2 }));
  const b0 = FP(t0, 2.5), b1 = FP(t1, 2.5);
  o.push(Ln(xx(b0[0]), yy(b0[1]), xx(b1[0]), yy(b1[1]), { stroke: COL.G, sw: 2.5, dash: '2 2' }));
  o.push(T(xx(L.sinkS + 3), yy(Wd - P.cabD) - 1, 'paper towels (recessed, high)', { size: 8.5, fill: '#8A5A00' }) + T(xx(L.sinkS + 3), yy(Wd - P.cabD) + 9, 'towel bars stick out 2 1/2 in', { size: 8.5, fill: COL.G }));
  // sliding door opening in the passenger wall
  const dxe = Math.min(P.doorX + P.slideW, P.cab);
  o.push(Ln(xx(P.doorX), yy(Wd), xx(dxe), yy(Wd), { stroke: '#BA7517', sw: 5, dash: '10 5' }));
  o.push(T(xx((P.doorX + dxe) / 2 + 8), yp(18.5), 'Sliding door opening', { size: 11, fill: '#854F0B', w: 500 }));
  o.push(T(xx((P.doorX + dxe) / 2 + 8), yp(21.5), `${fmt(P.slideW)} wide, ${fmt(P.doorX)} to ${fmt(P.doorX + P.slideW)}`, { size: 10, fill: '#854F0B' }));
  o.push(T(xx((P.doorX + dxe) / 2 + 8), yp(24.5), `entry ${fmt(L.entry)} clear` + ((V.flap || 0) > .5 ? ' (blocked by the table)' : ''), { size: 10, fill: COL.G }));
  // overhead cabinets (outline on top so the doors above them can be clicked); their doors flip up and stick out over the aisle
  L.cabs.forEach((c, ci) => {
    const ids = [0, 1, 2].map(i => 'dc' + (ci * 3 + i)).join(',');
    const cy0 = Math.max(P.cabBackIn, L.leanAt(L.ceilF)); let g = R(xx(c[0]), yy(cy0), S * (c[1] - c[0]), S * (P.cabBackIn + P.cabDepth - cy0), { rx: 2, stroke: COL.P, sw: 1.6, dash: '5 3' });
    L.doors.slice(ci * 3, ci * 3 + 3).forEach(d => { const s = V[d.id] || 0; if (s > .01) g += R(xx(d.x0), yy(P.cabBackIn + P.cabDepth), S * d.w, S * P.doorH * Math.sin(s * Math.PI / 2), { fill: COL.P, fo: .2, stroke: COL.P, sw: 1.2, dash: '3 2' }); });
    g += T(xx((c[0] + c[1]) / 2), yy(P.cabBackIn + P.cabDepth - 3.5), `overhead cabinet ${fmt(c[1] - c[0])} x ${fmt(P.cabDepth)} (bottom ${fmt(P.cabBot)} up)`, { size: 9, fill: COL.P, halo: false });
    o.push(MV(ids, g, ''));
  });
  // ---------- walkway dimensions, worked out from what is open right now ----------
  const O = obstacles(L, V);
  const dim = (x, label) => {
    const r = aisleAt(L, O, x); if (!(r.dm > 0 && r.qm > 0)) return '';
    const bad = r.v < 0, col = bad ? '#A32D2D' : (r.v < 14 ? '#BA7517' : '#A32D2D');
    return Ln(xx(x), yy(r.dm), xx(x), yy(Wd - r.qm), { stroke: col, sw: 1.6, mk: !bad }) + `<text x="${f1(xx(x) + 5)}" y="${f1(yy((r.dm + Wd - r.qm) / 2) + 4)}" style="font-size:11px;font-weight:700;fill:${col};${HALO}">${bad ? 'overlap ' + fmt(-r.v) : fmt(r.v)} ${label}</text>`;
  };
  o.push(dim(Math.min(14, P.panW - 2), 'gap in front of the shower'));
  o.push(dim((L.c0 + L.c1) / 2, 'aisle'));
  o.push(dim(L.cabS + 2, 'aisle'));
  o.push(dim(L.sinkS + 9, 'aisle'));
  const am = aisleMin(L, O);
  if (am.v < 1e8) o.push(dim(clamp(am.x, 1, P.cab - 1), 'aisle (tightest)'));
  o.push(Ln(xx(P.cab) + 18, yy(0), xx(P.cab) + 18, yy(Wd), { stroke: COL.G, sw: 1.5, mk: 1 }) + T(xx(P.cab) + 24, yy(Wd / 2), fmt(Wd) + ' wide', { anchor: 'start', size: 11, fill: COL.G, w: 700, halo: false }));
  // things you can drag (last, so they sit on top of everything)
  Object.values(cols).forEach(c => o.push(HIT(c.ids[0], xx(c.x0), yp(20), S * (c.x1 - c.x0), S * 20, [c.ids.map(id => 'dx' + id).join(','), 1 / S, '', 0], c.ids.some(id => L.coll.ids.has(id)), c.ids.length > 1 ? `The ${c.ids.length} drawers in this column (along the wall)` : cap(L.partById[c.ids[0]].n) + ' (along the wall)')));
  o.push(HIT('Micro', xx(L.microX[0] + 1.75), yp(P.microIn + 12), S * (L.microX[1] - L.microX[0] - 3.5), S * 12, ['dxMicro', 1 / S, 'microIn', -1 / S], L.coll.ids.has('Micro'), 'The microwave (along the wall and out from it)'));
  o.push(HIT('fresh', xx(L.tankX[0]), yp(P.tankBack + P.tankD), S * L.tankLen, S * P.tankD, ['tankShift', -1 / S, 'tankBack', -1 / S], L.coll.ids.has('fresh'), 'Fresh water tank (along the wall and out from it)'));
  if (P.drainOn && P.hotShelf > 10) o.push(HIT('drain', xx(P.drainX) - 8, yp(P.tankBack + P.tankD + 2.5) - 8, 16, 16, ['drainX', 1 / S, '', 0], false, 'Relief valve drain line (where it comes down)'));
  o.push(HIT('hot', xx(L.hotX[0]), yp(P.hotBack + P.hotD), S * P.hotW, S * P.hotD, ['hotX0', 1 / S, 'hotBack', -1 / S], L.coll.ids.has('hot'), 'Hot water tank (along the wall and out from it)', 'hotFree'));
  return { w: W, h: H, body: o.join('') };
}

/* ================= the ceiling covering: plywood sheets and slats ================= */
function drawCeiling(L, V) {
  const P = L.P, S = 5, X0 = 70, Y0 = 90, CL = P.ceilLen, CW = P.ceilW, o = [];
  const xx = x => X0 + S * x, yy = y => Y0 + S * y, hits = [];
  o.push(T(X0, 22, 'The ceiling covering seen from above through the roof: rear doors on the left, cab wall on the right, driver side at the top.', { anchor: 'start', size: 14, fill: '#5F5E5A', halo: false }));
  o.push(T(X0, 40, P.liningOn ? `${fmt(P.plyT)} in plywood against the roof, then ${L.nSlats - L.slatOut.size} cedar slats (${fmt(P.slatW)} wide x ${fmt(P.slatT)} thick x ${fmt(L.slatLen)} long) with ${fmt(P.slatGap)} in gaps and the lights mounted on the slats. Finished ceiling at ${fmt(L.ceilF)} in.` : 'The covering is turned off (Ceiling sizes on the right).', { anchor: 'start', size: 12, fill: '#5F5E5A', halo: false }));
  // plywood sheets (4 x 8 ft, long way along the van): pieces
  const cx = [0], cy = [0]; for (let x = 96; x < CL; x += 96) cx.push(x); cx.push(CL); for (let y = 48; y < CW; y += 48) cy.push(y); cy.push(CW);
  if (P.liningOn) {
    for (let i = 0; i < cx.length - 1; i++) for (let j = 0; j < cy.length - 1; j++) {
      o.push(R(xx(cx[i]), yy(L.ceilOff + cy[j]), S * (cx[i + 1] - cx[i]), S * (cy[j + 1] - cy[j]), { fill: '#D9C7A5', fo: .7, stroke: '#8A6B4D', sw: 1.2 }));
      o.push(T(xx((cx[i] + cx[i + 1]) / 2), yy(L.ceilOff + cy[j]) + 12, `plywood ${fmt(cx[i + 1] - cx[i])} x ${fmt(cy[j + 1] - cy[j])}`, { size: 10, fill: '#5A3A00', w: 600 }));
    }
    // slats: one row each, as long as the ceiling, cut where the fan and A/C openings cross them; a row is left out where each row of lights goes
    const seg = (x0, x1, ex) => { let parts = [[x0, x1]]; ex.forEach(([e0, e1]) => { const nx = []; parts.forEach(([p0, p1]) => { if (e1 <= p0 || e0 >= p1) nx.push([p0, p1]); else { if (e0 > p0) nx.push([p0, e0]); if (e1 < p1) nx.push([e1, p1]); } }); parts = nx; }); return parts; };
    L.slatY.forEach((y0, k) => {
      if (L.slatOut.has(k)) return;
      const ex = [L.fan, L.ac].filter(c => y0 < c.y + c.w / 2 && y0 + P.slatW > c.y - c.w / 2).map(c => [c.x - c.w / 2, c.x + c.w / 2]);
      for (let x0 = 0; x0 < CL; x0 += L.slatLen + .25) seg(x0, Math.min(CL, x0 + L.slatLen), ex).forEach(([a0, a1]) => o.push(R(xx(a0), yy(y0), S * (a1 - a0), S * P.slatW, { fill: '#9A6B3A', fo: .85, stroke: '#5A3A00', sw: .8 })));
    });
    o.push(T(xx(CL * .62), yy(L.slatY[Math.min(L.slatY.length - 1, 6)] || 4) + 9, `slats ${fmt(P.slatW)} x ${fmt(P.slatT)} x ${fmt(L.slatLen)}`, { size: 11, fill: '#fff', w: 600, halo: false }));
    L.lights.forEach(l => { o.push(`<circle cx="${f1(xx(l.x))}" cy="${f1(yy(l.y))}" r="${f1(S * P.lightD / 2)}" fill="#FFE9A0" stroke="#B8860B" stroke-width="1.4"/>`); });
    o.push(R(xx(L.ac.x - L.ac.u / 2), yy(L.ac.y - L.ac.u / 2), S * L.ac.u, S * L.ac.u, { stroke: '#444441', sw: 1.2, dash: '6 4' }));
    o.push(T(xx(L.ac.x), yy(L.ac.y + L.ac.u / 2) + 13, `A/C unit on the roof ${fmt(L.ac.u)} x ${fmt(L.ac.u)}`, { size: 10, fill: '#444441', halo: true }));
    o.push(R(xx(L.fan.x - L.fan.u / 2), yy(L.fan.y - L.fan.u / 2), S * L.fan.u, S * L.fan.u, { stroke: '#444441', sw: 1.2, dash: '6 4' }));
    o.push(T(xx(L.fan.x), yy(L.fan.y - L.fan.u / 2) - 5, `fan unit ${fmt(L.fan.u)} sq`, { size: 10, fill: '#444441', halo: true }));
    [L.fan, L.ac].forEach(c => { o.push(R(xx(c.x - c.w / 2), yy(c.y - c.w / 2), S * c.w, S * c.w, { fill: '#2C2C2A', fo: .88, stroke: '#000', sw: 1.4 })); o.push(T(xx(c.x), yy(c.y) - 2, c.nm, { size: 11, fill: '#fff', w: 600, halo: false })); o.push(T(xx(c.x), yy(c.y) + 11, `${fmt(c.w)} x ${fmt(c.w)} cutout`, { size: 9.5, fill: '#fff', halo: false })); });
    hits.push(HIT('ac', xx(L.ac.x - L.ac.u / 2), yy(L.ac.y - L.ac.u / 2), S * L.ac.u, S * L.ac.u, ['acX', 1 / S, 'acY', 1 / S], L.coll.ids.has('ac'), 'Air conditioner (along the van and across)'));
    hits.push(HIT('fan', xx(L.fan.x - L.fan.u / 2), yy(L.fan.y - L.fan.u / 2), S * L.fan.u, S * L.fan.u, ['fanX', 1 / S, 'fanY', 1 / S], L.coll.ids.has('fan'), 'Shower fan (along the van and across)'));
  } else o.push(R(xx(0), yy(L.ceilOff), S * CL, S * CW, { fill: '#F1EFE8', fo: .7, stroke: '#5F5E5A', sw: 1.2 }));
  // the roof ribs marked on the Bare roof tab (from the back edge): dashed red lines across the roof
  L.ribBands.forEach((b, i) => { o.push(R(xx(b[0]), yy(0), S * (b[1] - b[0]), S * P.vanW, { fill: '#A32D2D', fo: .16, stroke: '#A32D2D', sw: 1.4, dash: '9 4' })); o.push(T(xx((b[0] + b[1]) / 2), yy(0) - 6 - (i % 2) * 12, `rib ${fmt(L.ribs[i])}`, { size: 10.5, fill: '#A32D2D', w: 700 })); });
  if (!L.ribs.length) o.push(T(xx(CL / 2), yy(0) - 22, 'No roof ribs marked yet: type them in the Roof ribs box (Sizes) and they show here', { size: 11, fill: '#8A8A8A', halo: false }));
  // outline (the inside of the van) and dimensions; the flat part being covered is centered in it
  const VW = P.vanW;
  o.push(R(xx(0), yy(0), S * CL, S * VW, { stroke: '#2C2C2A', sw: 1.8 }));
  o.push(Ln(xx(0), yy(VW) + 18, xx(CL), yy(VW) + 18, { stroke: '#A32D2D', sw: 1.4, mk: true }));
  o.push(T(xx(CL / 2), yy(VW) + 34, `${fmt(CL)} in long (rear doors to cab wall)`, { size: 12, fill: '#A32D2D', w: 500, halo: false }));
  o.push(Ln(xx(CL) + 18, yy(L.ceilOff), xx(CL) + 18, yy(L.ceilOff + CW), { stroke: '#A32D2D', sw: 1.4, mk: true }));
  o.push(T(xx(CL) + 28, yy(L.ceilOff + CW / 2) - 6, `${fmt(CW)} flat part`, { size: 12, fill: '#A32D2D', w: 500, halo: false, anchor: 'start' }));
  o.push(T(xx(CL) + 28, yy(L.ceilOff + CW / 2) + 10, `${fmt(L.ceilOff)} each side`, { size: 11, fill: '#A32D2D', halo: false, anchor: 'start' }));
  o.push(T(xx(0) - 6, yy(VW / 2), 'rear', { size: 11, fill: '#5F5E5A', halo: false, anchor: 'end' })); o.push(T(xx(CL) - 4, yy(0) - 6, 'cab wall', { size: 11, fill: '#5F5E5A', halo: false, anchor: 'end' }));
  o.push(T(xx(CL / 2), yy(0) - 6, 'driver side wall', { size: 11, fill: '#5F5E5A', halo: false })); o.push(T(xx(CL / 2), yy(VW) + 52, 'passenger side wall', { size: 11, fill: '#5F5E5A', halo: false }));
  return { w: xx(CL) + 130, h: yy(VW) + 70, body: o.join('') + hits.join('') };
}

/* ================= the bare roof from above, before any covering, to mark where the ribs are ================= */
function drawBare(L, V) {
  const P = L.P, S = 5, X0 = 70, Y0 = 100, CL = P.ceilLen, W = P.vanW, o = [];
  const xx = x => X0 + S * x, yy = y => Y0 + S * y, hits = [];
  o.push(T(20, 22, 'The bare roof seen from above, before any covering: rear doors on the left, cab wall on the right, driver side at the top.', { anchor: 'start', size: 14, fill: '#5F5E5A', halo: false }));
  o.push(T(20, 40, 'Measure from the back edge (the rear doors). Type the rib positions in the Roof ribs box below the drawing, separated by commas.', { anchor: 'start', size: 12, fill: '#5F5E5A', halo: false }));
  o.push(T(20, 56, `Heights from the floor: ${fmt(P.roofWallH)} in to the rib at the wall, ${fmt(P.roofMidH)} in to the rib in the middle (the roof arcs ${fmt(L.roofSag)} in across the ${fmt(L.roofW)} in between the wall tops).`, { anchor: 'start', size: 12, fill: '#5F5E5A', halo: false }));
  o.push(R(xx(0), yy(0), S * CL, S * W, { fill: '#F1EFE8', fo: .8, stroke: '#2C2C2A', sw: 2 }));
  // the flat/arched part between the wall tops, and the middle line
  const e = (W - L.roofW) / 2;
  o.push(R(xx(0), yy(e), S * CL, S * L.roofW, { stroke: '#8A6B4D', sw: 1, dash: '6 4' }));
  o.push(Ln(xx(0), yy(W / 2), xx(CL), yy(W / 2), { stroke: '#8A6B4D', sw: 1, dash: '2 4' }));
  o.push(T(xx(CL) + 8, yy(W / 2) + 4, `middle, ${fmt(P.roofMidH)} up`, { anchor: 'start', size: 10.5, fill: '#5A3A00', halo: false }));
  o.push(T(xx(CL) + 8, yy(e) + 4, `wall top, ${fmt(P.roofWallH)} up`, { anchor: 'start', size: 10.5, fill: '#5A3A00', halo: false }));
  o.push(T(xx(CL) + 8, yy(W - e) + 4, `wall top, ${fmt(P.roofWallH)} up`, { anchor: 'start', size: 10.5, fill: '#5A3A00', halo: false }));
  // grid every 10 in and a ruler along the top and bottom edges (a tick every 5 in, a number every 10)
  for (let x = 0; x <= CL; x += 10) o.push(Ln(xx(x), yy(0), xx(x), yy(W), { stroke: '#3F3E3A', so: .28, sw: .8, dash: '3 3' }));
  for (let y = 0; y <= W; y += 10) o.push(Ln(xx(0), yy(y), xx(CL), yy(y), { stroke: '#3F3E3A', so: .28, sw: .8, dash: '3 3' }));
  for (let x = 0; x <= CL; x += 5) {
    const big = x % 10 === 0;
    o.push(Ln(xx(x), yy(0), xx(x), yy(0) - (big ? 9 : 5), { stroke: '#185FA5', sw: 1 })); o.push(Ln(xx(x), yy(W), xx(x), yy(W) + (big ? 9 : 5), { stroke: '#185FA5', sw: 1 }));
    if (big) { o.push(T(xx(x), yy(0) - 13, x + '', { size: 10.5, fill: '#185FA5', w: 700, halo: false })); o.push(T(xx(x), yy(W) + 22, x + '', { size: 10.5, fill: '#185FA5', w: 700, halo: false })); }
  }
  for (let y = 0; y <= W; y += 5) { const big = y % 10 === 0; o.push(Ln(xx(0), yy(y), xx(0) - (big ? 9 : 5), yy(y), { stroke: '#185FA5', sw: 1 })); if (big) o.push(T(xx(0) - 14, yy(y) + 4, y + '', { anchor: 'end', size: 10.5, fill: '#185FA5', w: 700, halo: false })); }
  o.push(T(xx(CL / 2), yy(W) + 40, 'inches from the back edge (the rear doors)', { size: 12, fill: '#5F5E5A', halo: false }));
  o.push(T(xx(0) - 50, yy(0) - 28, 'down the side: inches across from the driver wall', { anchor: 'start', size: 10.5, fill: '#5F5E5A', halo: false }));
  // the cab wall
  o.push(Ln(xx(CL), yy(0), xx(CL), yy(W), { stroke: '#2C2C2A', sw: 3 })); o.push(T(xx(CL) - 4, yy(0) - 30, 'cab wall', { anchor: 'end', size: 11, fill: '#5F5E5A', halo: false }));
  // the roof openings (planned) and the units over them
  [L.fan, L.ac].forEach(c => {
    o.push(R(xx(c.x - c.u / 2), yy(c.y - c.u / 2), S * c.u, S * c.u, { stroke: '#444441', sw: 1.2, dash: '6 4' }));
    o.push(R(xx(c.x - c.w / 2), yy(c.y - c.w / 2), S * c.w, S * c.w, { fill: '#2C2C2A', fo: .75, stroke: '#000', sw: 1.2 }));
    o.push(T(xx(c.x), yy(c.y) + 4, c.nm === 'A/C' ? 'A/C' : 'fan', { size: 11, fill: '#fff', w: 600, halo: false }));
    o.push(T(xx(c.x), yy(c.y - c.u / 2) - 4, `${c.nm === 'A/C' ? 'A/C' : 'fan'} unit ${fmt(c.u)} sq, opening ${fmt(c.w)} sq at ${fmt(c.x)} / ${fmt(c.y)}`, { size: 9.5, fill: '#444441' }));
  });
  hits.push(HIT('ac', xx(L.ac.x - L.ac.u / 2), yy(L.ac.y - L.ac.u / 2), S * L.ac.u, S * L.ac.u, ['acX', 1 / S, 'acY', 1 / S], L.coll.ids.has('ac'), 'Air conditioner (along the van and across)'));
  hits.push(HIT('fan', xx(L.fan.x - L.fan.u / 2), yy(L.fan.y - L.fan.u / 2), S * L.fan.u, S * L.fan.u, ['fanX', 1 / S, 'fanY', 1 / S], L.coll.ids.has('fan'), 'Shower fan (along the van and across)'));
  // the ribs the user has marked: full width lines with their position
  L.ribBands.forEach((b, i) => { o.push(R(xx(b[0]), yy(0), S * (b[1] - b[0]), S * W, { fill: '#A32D2D', fo: .3, stroke: '#A32D2D', sw: 1.6 })); o.push(T(xx((b[0] + b[1]) / 2), yy(W) - 6 - (i % 2) * 12, `${fmt(L.ribs[i])}${P.ribRef === 'center' ? '' : P.ribRef === 'front' ? ' (front edge)' : ' (back edge)'}`, { size: 10.5, fill: '#A32D2D', w: 700 })); });
  if (!L.ribs.length) o.push(T(xx(CL / 2), yy(W / 2) + 40, 'No ribs marked yet', { size: 13, fill: '#8A8A8A', halo: false }));
  return { w: xx(CL) + 130, h: yy(W) + 70, body: o.join('') + hits.join('') };
}
