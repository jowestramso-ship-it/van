/* ================= elevation views (driver side and passenger side) ================= */
function mkElev(flip, L) {
  const P = L.P, S = 6, X0 = 50;
  const zMax = Math.max(P.ceil + 4, 80), FL = 60 + S * zMax, xs = P.cab + 8;
  const xx = x => flip ? X0 + S * (xs - x) : X0 + S * x;
  const yy = z => FL - S * z;
  const box = (x0, x1, z0, z1, o) => R(Math.min(xx(x0), xx(x1)), yy(z1), Math.abs(xx(x1) - xx(x0)), S * (z1 - z0), o);
  return { S, X0, FL, xs, zMax, W: X0 + S * xs + 50, H: FL + 96, xx, yy, box, flip };
}
function elevFrame(E, L, title) {
  const P = L.P, { S, X0, FL, xs, zMax, xx, yy, box } = E, o = [];
  o.push(T(X0, 22, title, { anchor: 'start', size: 14, fill: '#5F5E5A', halo: false }));
  for (let x = 0; x <= xs; x += 10) o.push(Ln(xx(x), yy(zMax), xx(x), FL, { stroke: '#3F3E3A', so: .35, sw: .9, dash: '3 3' }));
  for (let z = 0; z <= zMax; z += 10) {
    o.push(Ln(xx(0), yy(z), xx(xs), yy(z), { stroke: '#3F3E3A', so: .35, sw: .9, dash: '3 3' }));
    o.push(T(E.flip ? xx(0) + 6 : xx(0) - 6, yy(z) + 4, z + '↑', { anchor: E.flip ? 'start' : 'end', size: 11, fill: '#8A4B0F', w: 700, halo: false }));
  }
  o.push(R(Math.min(xx(0), xx(P.cab)), yy(P.ceil), S * P.cab, S * P.ceil, { fill: '#F1EFE8', fo: .6, stroke: '#5F5E5A', sw: 1.2 }));
  o.push(T(E.flip ? xx(0) - 4 : xx(0) + 4, yy(P.ceil) - (L.lining > 0 ? 17 : 5), 'ceiling (bare) ' + fmt(P.ceil) + (L.lining > 0 ? `; with the covering (${fmt(P.plyT)} plywood + ${fmt(P.slatT)} slats) it is ${fmt(L.ceilF)}` : ''), { anchor: E.flip ? 'end' : 'start', size: 11, fill: '#5F5E5A', halo: false }));
  if (L.lining > 0) {
    o.push(R(Math.min(xx(0), xx(P.cab)), yy(P.ceil), S * P.cab, S * P.plyT, { fill: '#D9C7A5', fo: .9, stroke: '#8A6B4D', sw: .8 }));
    for (let x0 = -6; x0 < P.cab; x0 += L.slatLen + .25) { const a0 = Math.max(0, x0), a1 = Math.min(P.cab, x0 + L.slatLen); if (a1 > a0) o.push(R(Math.min(xx(a0), xx(a1)), yy(P.ceil - P.plyT), S * (a1 - a0), S * P.slatT, { fill: '#9A6B3A', fo: .85, stroke: '#5A3A00', sw: .8 })); }
    [L.fan, L.ac].forEach(c => { const a0 = Math.max(0, c.x - 6 - c.w / 2), a1 = Math.min(P.cab, c.x - 6 + c.w / 2); if (a1 > a0) { o.push(R(Math.min(xx(a0), xx(a1)), yy(P.ceil), S * (a1 - a0), S * L.lining, { fill: '#2C2C2A', fo: .85 })); o.push(T((xx(a0) + xx(a1)) / 2, yy(P.ceil) - 4, c.nm, { size: 10, fill: '#2C2C2A', halo: false })); } });
    L.lights.forEach(l => { const px = l.x - 6; if (px > 0 && px < P.cab) o.push(`<circle cx="${f1(xx(px))}" cy="${f1(yy(L.ceilF) + 1.5)}" r="2.6" fill="#FFD84A" stroke="#B8860B" stroke-width=".8"/>`); });
  }
  return o.join('');
}
// wall covering: the sheet joints (sheets run floor to ceiling from the rear edge, 6 in behind the 0 mark), left out below the top of the sliding door opening
const FURR = [3, 12, 21.5, 30.25, 43.5, 57.25, 66, 76.75];
function wallSeams(E, L, pass) {
  const P = L.P, { xx, yy } = E, o = [];
  if (!P.wallOn) return '';
  let first = true;
  for (let x = -6 + P.sheetW; x < P.cab; x += P.sheetW) {
    const inDoor = pass && x > P.doorX && x < P.doorX + P.slideW, z0 = inDoor ? P.slideH : 0;
    o.push(Ln(xx(x), yy(z0), xx(x), yy(L.ceilF), { stroke: '#8A6B4D', so: .7, sw: 1, dash: '2 3' }));
    if (first) { o.push(T(xx(x) + (E.flip ? -3 : 3), yy(L.ceilF) + 11, 'sheet joint', { anchor: E.flip ? 'end' : 'start', size: 8, fill: '#8A6B4D', halo: false })); first = false; }
  }
  return o.join('');
}
function elevTail(E, L, xlabel) {
  const P = L.P, { S, FL, xs, xx, yy, box } = E, o = [];
  o.push(box(P.cab, P.cab + 4, 0, P.ceil, { fill: 'url(#hatch)', fo: .4 }));
  o.push(Ln(xx(P.cab), yy(P.ceil + 3), xx(P.cab), FL, { stroke: '#5F5E5A', sw: 2, dash: '6 3' }));
  o.push(T(xx(P.cab) + (E.flip ? 4 : -4), yy(P.ceil + 3) - 4, `cab wall at ${fmt(P.cab)} (could be off by 2 to 4 in)`, { anchor: E.flip ? 'start' : 'end', size: 11, fill: '#5F5E5A', halo: false }));
  const yb = FL + 16;
  o.push(Ln(xx(0), yb, xx(xs), yb, { stroke: '#888780', sw: .6 }));
  for (let t = 0; t <= xs; t += 10) {
    o.push(Ln(xx(t), yb - 4, xx(t), yb + 4, { stroke: '#888780', sw: .6 }));
    o.push(T(xx(t), yb + 18, t + (E.flip ? '←' : '→'), { size: 11, fill: '#185FA5', w: 700, halo: false }));
  }
  o.push(T((xx(0) + xx(xs)) / 2, yb + 36, xlabel, { size: 12, fill: '#5F5E5A', halo: false }));
  return o.join('');
}

function drawDriver(L, V) {
  const P = L.P, E = mkElev(false, L), { S, FL, xx, yy, box } = E, o = [];
  const X = x => xx(x), Y = z => yy(z);
  o.push(elevFrame(E, L, 'Driver side wall seen from the aisle: rear on the left, cab on the right. Click a door to open it.'));
  o.push(wallSeams(E, L, false));
  // wheel well
  const WW = [[42, 0], [76, 0], [76, 2], [66.75, 7.5], [51.25, 7.5], [42, 2]];
  o.push(Poly(WW.map(p => [X(p[0]), Y(p[1])]), { fill: '#E24B4A', fo: .35, stroke: '#A32D2D', sw: 1.6, dash: '5 3', join: 'round' }));
  o.push(T(X(59), Y(3.2), 'wheel well', { size: 12, fill: '#791F1F', halo: false }));
  // wall cabinets
  L.cabs.forEach(c => {
    o.push(box(c[0], c[1], P.cabBot, L.ceilF, { fill: COL.P, fo: .12, stroke: COL.P, sw: 1.4, rx: 3 }));
    o.push(T(X((c[0] + c[1]) / 2), Y(P.cabBot - 2.4), `Wall cabinet, ${fmt(c[1] - c[0])} long x ${fmt(P.cabDepth)} deep x ${fmt(L.ceilF - P.cabBot)} tall (${fmt(P.cabBot)} to ${fmt(L.ceilF)} in up)`, { size: 12, fill: COL.P }));
  });
  // bed / couch with a hinged leaf. The deck top is 3/4 in below the seat base: by day the leaf (face down) lies on the deck under the seat cushion; at night it is flipped out level with the deck, on three legs, with the back cushion on it
  {
    const s = V.bed || 0, bs = bedState(s), plat = P.platform, lt = .75, deck = plat - lt, bt = plat + P.mattress, LW = P.bedBack, th = bs.th;
    const sn = Math.sin(th), cs = Math.cos(th);
    const zr = (r0, r1, t0, t1) => { const zs = [[r0, t0], [r0, t1], [r1, t0], [r1, t1]].map(c => deck + c[0] * sn + c[1] * cs); return [Math.min.apply(null, zs), Math.max.apply(null, zs)]; };
    let g = box(0, P.bedLen, 0, deck - lt, { stroke: COL.P, sw: 1, dash: '5 3', so: .45 });
    g += box(0, P.bedLen, deck - lt, deck, { fill: COL.G, fo: .25, stroke: COL.G, sw: 1 });
    if (bs.legs > .01) {
      const psi = bs.legs * Math.PI / 2, tp = lt / 2, LG = deck - tp - .25, pr = LW - P.legIn;
      legXs(P).forEach(lx => {
        const a = deck + pr * sn + tp * cs, b = deck + (pr - LG * Math.cos(psi)) * sn + (tp + LG * Math.sin(psi)) * cs;
        g += box(lx, lx + 1.25, Math.min(a, b), Math.max(a, b), { fill: COL.G, fo: .8, stroke: COL.G, sw: 1 });
      });
    }
    const lf = zr(0, LW, 0, lt);
    g += box(0, P.bedLen, lf[0], Math.max(lf[1], lf[0] + .3), { fill: '#B07A2A', fo: .55 + .3 * bs.lift, stroke: '#5A3A00', sw: 1.2 });
    const fade = 1 - .75 * Math.sin(clamp((s - .2) / .6, 0, 1) * Math.PI), sb0 = deck + lt * Math.max(0, cs);
    g += box(0, P.bedLen, sb0, sb0 + P.mattress, { fill: COL.P, fo: .12 * fade, stroke: COL.P, sw: 1.4, rx: 3, so: fade });
    if (bs.back > .02) g += box(0, P.bedLen, bt, bt + LW * bs.back, { fill: COL.P, fo: .1, stroke: COL.P, sw: 1.4, rx: 3 });
    if (bs.flat > .02) g += box(0, P.bedLen, deck, deck + P.mattress, { fill: COL.P, fo: .2 * bs.flat, stroke: COL.P, sw: 2.2, rx: 3, so: bs.flat });
    if (s < .3) {
      g += T(X(P.bedLen / 2), Y(plat + P.mattress / 2 - 0.4), `Seat cushion, top at ${fmt(bt)} in (click to make up the bed)`, { size: 12.5, fill: COL.P, op: 1 - s / .3 });
      if (LW * bs.back > 9) g += T(X(P.bedLen / 2), Y(bt + LW * bs.back / 2), `Back cushion, upright, ${fmt(LW)} tall`, { size: 12.5, fill: COL.P, op: 1 - s / .3 });
    }
    if (s > .85) g += T(X(P.bedLen / 2), Y(deck + P.mattress / 2 - 0.4), `Bed made up: ${fmt(P.bedD + LW)} wide, top at ${fmt(deck + P.mattress)} in, leaf on 4 legs`, { size: 12.5, fill: COL.P, op: (s - .85) / .15 });
    else if (s >= .3) g += T(X(P.bedLen / 2), Y(bt + 6), 'leaf flips over (the seat cushion comes off)', { size: 11, fill: '#5A3A00', op: Math.min(1, (s - .3) * 4) * (s > .75 ? (.85 - s) * 10 : 1) });
    o.push(MV('bed', g, HITR(Math.min(X(0), X(P.bedLen)), Y(bt + LW), S * P.bedLen, S * (bt + LW))));
  }
  // closet
  o.push(box(L.c0, L.c1, 0, L.ceilF, { fill: COL.G, fo: .12, stroke: COL.G, sw: 1.4, rx: 3 }));
  o.push(T(X((L.c0 + L.c1) / 2), Y(L.ceilF * 0.62), 'Closet', { size: 12.5, fill: COL.G }));
  o.push(T(X((L.c0 + L.c1) / 2), Y(L.ceilF * 0.62) + 15, fmt(P.closetW) + ' in', { size: 11, fill: COL.G }));
  // pockets on the inside of the closet doors
  const pw = (P.closetW - 1.75) / 2;
  const prow = [[5, 12], [12.5, 19.5], [20, 27], [27.5, 34.5]].filter(r => r[1] < P.split - 3);
  const prow2 = [[4, 11], [11.5, 18.5], [19, 26]].map(r => [P.split + r[0], P.split + r[1]]);
  prow.concat(prow2).forEach(r => { [L.c0 + 0.625, L.c0 + 0.625 + pw + 0.5].forEach(px => { if (r[0] > 0 && r[1] < P.ceil) o.push(box(px, px + pw, r[0], r[1], { fill: '#B07A2A', fo: .1, stroke: '#8A5A00', sw: 1, rx: 2, dash: '3 2' })); }); });
  o.push(T(X((L.c0 + L.c1) / 2), Y(P.split + 28.5), 'dashed: door pockets inside', { size: 9.5, fill: '#8A5A00' }));
  // closet interior when the doors are open: darker back, garments
  const hx = P.hinge === 'rear' ? L.c0 + 0.125 : L.c1 - 0.125, wC = P.closetW - 0.25;
  const cdoors = [{ id: 'clo_hi', z0: P.split + 0.1, z1: L.ceilF - 0.25, nm: 'upper door' }, { id: 'clo_lo', z0: 0.25, z1: P.split - 0.1, nm: 'lower door' }];
  cdoors.forEach(dc => {
    const s = V[dc.id] || 0;
    if (s > 0.02) o.push(box(L.c0 + 0.125, L.c1 - 0.125, dc.z0, dc.z1, { fill: '#2C2C2A', fo: .3 * Math.min(1, s * 1.5) }));
  });
  [[P.rodHi, 'clo_hi'], [P.rodLo, 'clo_lo']].forEach(r => {
    const s = V[r[1]] || 0, cols = ['#B5502F', '#185FA5', '#0F6E56', '#993556'];
    if (s > 0.05) for (let x = L.c0 + 2.2, i = 0; x + 0.9 < L.c1 - 2; x += 1.5, i++) o.push(box(x, x + 0.9, r[0] - 30, r[0] - 0.8, { fill: cols[i % 4], fo: .55 * Math.min(1, s * 1.6), stroke: cols[i % 4], sw: .6, rx: 1 }));
    o.push(Ln(X(L.c0 + 2), Y(r[0]), X(L.c1 - 2), Y(r[0]), { stroke: COL.G, sw: 3.5, cap: 'round' }));
    o.push(T(X((L.c0 + L.c1) / 2), Y(r[0]) - 5, `rod, ${fmt(r[0])} in up`, { size: 10, fill: COL.G, w: 700 }));
  });
  // closet doors (hinge side and angle follow the sizes)
  cdoors.forEach(dc => {
    const s = V[dc.id] || 0, th = s * P.openAng * Math.PI / 180, sw = wC * Math.cos(th);
    const tip = P.hinge === 'rear' ? hx + sw : hx - sw, dx0 = Math.min(hx, tip), dx1 = Math.max(hx, tip);
    let g = box(dx0, dx1, dc.z0, dc.z1, { fill: COL.G, fo: .12 + .14 * s, stroke: COL.G, sw: 1.6, rx: 3 });
    if (s < .35) {
      const zc = (dc.z0 + dc.z1) / 2 + (dc.nm === 'upper door' ? 9 : -9);
      g += T(X((L.c0 + L.c1) / 2), Y(zc), dc.nm, { size: 11.5, fill: COL.G, op: 1 - s / .35 });
      g += T(X((L.c0 + L.c1) / 2), Y(zc) + 13, `${fmt(wC)} x ${fmt(dc.z1 - dc.z0)}`, { size: 10, fill: COL.G, op: 1 - s / .35 });
    }
    o.push(MV(dc.id, g, HITR(Math.min(X(L.c0 + 0.125), X(L.c1 - 0.125)), Y(dc.z1), S * wC, S * (dc.z1 - dc.z0))));
  });
  // benches and table. The dinette makes up into a bed: the table lowers, the backrest cushions come off and lie on it, so the three sections are level
  {
    const s = V.dinette || 0, ds = dinState(s), pt = P.pillowT, tt = P.tableH + (L.tableLow - P.tableH) * ds.tbl, bh = P.seatH + (P.backH - P.seatH) * ds.back;
    let g = '';
    [[L.bA, L.bA[0], L.bA[0] + pt], [L.bB, L.bB[1] - pt, L.bB[1]]].forEach(b => {
      g += box(b[0][0], b[0][1], 0, P.seatH, { fill: COL.K, fo: .12, stroke: COL.K, sw: 1.4, rx: 3 });
      if (ds.back > .02) g += box(b[1], b[2], P.seatH, bh, { fill: COL.K, fo: .12, stroke: COL.K, sw: 1.4, rx: 3 });
      g += T(X((b[0][0] + b[0][1]) / 2), Y(2.5), 'Bench', { size: 12.5, fill: COL.K });
    });
    if (L.tableLen > 0) {
      g += box(L.tbl[0], L.tbl[1], tt - 1, tt, { fill: COL.G, fo: .35, stroke: COL.G, sw: 1.4 });
      if (ds.pil > .02) g += box(L.tbl[0], L.tbl[1], tt, tt + pt, { fill: COL.K, fo: .28 * ds.pil, stroke: COL.K, sw: 1.8, rx: 2, so: ds.pil });
      g += T(X((L.tbl[0] + L.tbl[1]) / 2), Y(tt - 3.7), `Table, ${fmt(tt)} in high`, { size: 12.5, fill: COL.G });
      if (s < .1) g += T(X((L.tbl[0] + L.tbl[1]) / 2), Y(tt - 8), 'click: dinette to bed', { size: 10, fill: COL.G, op: 1 - s * 10 });
    }
    if (ds.pil > .5) g += T(X((L.bA[0] + L.bB[1]) / 2), Y(P.seatH + 7), `Dinette bed: ${fmt(L.bB[1] - L.bA[0])} x ${fmt(Math.min(P.benchD, P.tableD))} in, top at ${fmt(P.seatH)} in`, { size: 12.5, fill: COL.K, op: (ds.pil - .5) * 2 });
    o.push(MV('dinette', g, HITR(Math.min(X(L.bA[0]), X(L.bB[1])), Y(P.backH), S * (L.bB[1] - L.bA[0]), S * P.backH)));
  }
  // wall cabinet doors: flip up (hinged on the top edge), shown from the front so the door gets shorter as it swings up
  L.doors.forEach(d => {
    const s = V[d.id] || 0, th = s * Math.PI / 2, h = P.doorH * Math.cos(th), zb = L.doorZ[0], zt = L.doorZ[1];
    let g = '';
    if (s > 0.02) g += box(d.x0, d.x1, zb, zt, { fill: '#2C2C2A', fo: .12 + .3 * Math.min(1, s * 1.5) });
    g += box(d.x0, d.x1, zt - h, zt, { fill: COL.P, fo: .18 + .2 * s, stroke: COL.P, sw: 1.6, rx: 3 });
    if (s < .3) g += T(X((d.x0 + d.x1) / 2), Y((zb + zt) / 2 + .3), `door ${fmt(d.w)} x ${fmt(P.doorH)}`, { size: 12, fill: COL.P, op: 1 - s / .3 });
    o.push(MV(d.id, g, HITR(Math.min(X(d.x0), X(d.x1)), Y(zt), S * d.w, S * P.doorH)));
  });
  // battery in front of the wheel well
  o.push(box(L.batt[0], L.batt[1], 0, 9.5, { fill: '#F2B84B', fo: .65, stroke: '#8A5A00', sw: 2, rx: 3 }));
  o.push(T(X((L.batt[0] + L.batt[1]) / 2), Y(5.8), 'Battery', { size: 11, fill: '#5A3A00' }));
  o.push(T(X((L.batt[0] + L.batt[1]) / 2), Y(5.8) + 13, `21 x 9.5 in, ${fmt(L.batt[0])} to ${fmt(L.batt[1])} in`, { size: 10, fill: '#5A3A00' }));
  o.push(elevTail(E, L, 'inches from where you start measuring at the back (about 6 in in from the rear edge; the rear lip is not counted)'));
  return { w: E.W, h: E.H, body: o.join('') };
}

function drawPass(L, V) {
  const P = L.P, E = mkElev(true, L), { S, FL, xx, yy, box } = E, o = [];
  const X = x => xx(x), Y = z => yy(z);
  const ch = P.counterH, cabS = L.cabS, angS = L.angS, sinkS = L.sinkS, sinkE = L.sinkE;
  o.push(elevFrame(E, L, 'Passenger side wall seen from inside the van: cab on the left, rear on the right. Click the fold-out table, the fridge or the shower pan.'));
  o.push(wallSeams(E, L, true));
  // wheel well (same as the driver side)
  const WW = [[42, 0], [76, 0], [76, 2], [66.75, 7.5], [51.25, 7.5], [42, 2]];
  o.push(Poly(WW.map(p => [X(p[0]), Y(p[1])]), { fill: '#D8B79A', fo: .8, stroke: '#8A6B4D', sw: 1.2 }));
  o.push(T(X(59), Y(3.2), 'wheel well (same as the driver side)', { size: 10, fill: '#5F5E5A', halo: false }));
  // wet bath: outline, curtain, pan (tips up toward the wall)
  const sp = V.pan || 0, tp = sp * Math.PI / 2, panTop = 0.8 + P.panD * Math.sin(tp) + 3 * Math.cos(tp);
  o.push(box(0, P.panW, 0, L.ceilF, { fill: COL.T, fo: .08, stroke: COL.T, sw: 1.5, rx: 3 }));
  o.push(T(X(P.panW / 2), Y(L.ceilF * 0.9), 'Wet bath', { size: 12, fill: COL.T }));
  o.push(T(X(P.panW / 2), Y(L.ceilF * 0.9) + 14, `${fmt(P.panW)} x ${fmt(P.panD)} in, shower curtain`, { size: 10.5, fill: COL.T }));
  // shower nook and counter nook are recesses in the wall (fixed positions)
  const nkx = Math.min(29.75, P.panW - 6.25);
  o.push(box(6, nkx, 31, 56.5, { fill: '#7A4A1E', fo: .2, stroke: '#7A4A1E', sw: 1.5, rx: 3, dash: '5 3' }));
  o.push(T(X((6 + nkx) / 2), Y(44), 'Shower nook', { size: 12, fill: '#7A4A1E' }));
  o.push(T(X((6 + nkx) / 2), Y(44) + 14, `${fmt(nkx - 6)} x 25 1/2, 4 1/2 deep`, { size: 10.5, fill: '#7A4A1E' }));
  {
    let g = box(0, P.panW, 1, 75, { fill: '#7B3FA0', fo: .12 * (1 - sp) });
    g += box(0, P.panW, 0, panTop, { fill: '#D9ECF7', fo: .95, stroke: COL.BL, sw: 1.8 });
    if (sp > .55) g += T(X(P.panW / 2), Y(panTop / 2) + 4, 'pan tipped up', { size: 11, fill: COL.BL });
    else if (sp < .1) g += T(X(P.panW / 2), Y(2), 'pan down', { size: 10, fill: COL.BL });
    o.push(MV('pan', g, HITR(Math.min(X(0), X(P.panW)), Y(P.panD + 2), S * P.panW, S * (P.panD + 2))));
  }
  // cabinets, counter
  o.push(box(cabS, sinkS, 0, ch, { fill: COL.C, fo: .08, stroke: COL.C, sw: 1.5, rx: 3 }));
  o.push(box(sinkS, sinkE, 0, ch, { fill: COL.C, fo: .08, stroke: COL.C, sw: 1.5, rx: 3 }));
  o.push(T(X((sinkS + sinkE) / 2), Y(ch * .68), 'Sink cabinet', { size: 12, fill: COL.C }));
  o.push(T(X((sinkS + sinkE) / 2), Y(ch * .68) + 14, `${fmt(P.sinkW)} wide, counter ${fmt(P.sinkD)} deep`, { size: 10.5, fill: COL.C }));
  o.push(box(cabS, sinkE, ch - 1.2, ch, { fill: '#5F5E5A', fo: .75 }));
  o.push(T(X(sinkS - 3), Y(ch) - 4, `countertop at ${fmt(ch)} in`, { size: 10.5, fill: '#5F5E5A', halo: false }));
  // fridge on a platform over the wheel well, microwave on its shelf
  const q0 = L.fr[0], q1 = L.fr[1], fb = 8.25, ft = fb + P.fridgeH;
  o.push(box(q0, q1, 7.5, 8.25, { fill: '#8A6B4D', stroke: '#3E230B', sw: 1 }));
  o.push(box(q0, q0 + 1.5, 0, 7.5, { fill: '#8A6B4D', stroke: '#3E230B', sw: 1 }));
  {
    const s = V.fridge || 0, th = s * Math.PI / 2, wv = P.fridgeW * Math.cos(th);
    let g = box(q0, q1, fb, ft, { fill: '#0A6A8A', fo: .22, stroke: '#0A6A8A', sw: 1.5, rx: 3 });
    if (s > .02) {
      g += box(q0, q1, fb, ft, { fill: '#E1F5EE', fo: .85 * Math.min(1, s * 1.5) });
      for (let k = 1; k <= 4; k++) g += Ln(X(q0 + .8), Y(fb + P.fridgeH * k / 5), X(q1 - .8), Y(fb + P.fridgeH * k / 5), { stroke: '#0A6A8A', sw: 2, so: Math.min(1, s * 1.5) });
    }
    g += box(q0, q0 + wv, fb, ft, { fill: '#0A6A8A', fo: .3 + .1 * s, stroke: '#0A6A8A', sw: 1.8, rx: 3 });
    if (s < .4) {
      g += T(X((q0 + q1) / 2), Y(34), 'Fridge', { size: 12, fill: '#0A6A8A', op: 1 - s / .4 });
      g += T(X((q0 + q1) / 2), Y(34) + 14, `${fmt(P.fridgeW)} x ${fmt(P.fridgeD)} x ${fmt(P.fridgeH)}, front opening`, { size: 10.5, fill: '#0A6A8A', op: 1 - s / .4 });
      g += T(X((q0 + q1) / 2), Y(34) + 28, 'on a platform over the well', { size: 9.5, fill: '#0A6A8A', op: 1 - s / .4 });
    }
    o.push(MV('fridge', g, HITR(Math.min(X(q0), X(q1)), Y(ft), S * P.fridgeW, S * P.fridgeH)));
  }
  const md = P.dzMicro, mx = P.dxMicro;
  o.push(box(q0 + mx, q1 + mx, ft + 2 + md, ft + 2.75 + md, { fill: '#8A6B4D', stroke: '#3E230B', sw: 1 }));
  o.push(box(q0 + mx + (P.fridgeW - 18.5) / 2, q1 + mx - (P.fridgeW - 18.5) / 2, ft + 2.75 + md, ft + 12.75 + md, { fill: COL.G, fo: .25, stroke: COL.G, sw: 1.5, rx: 3 }));
  o.push(T(X((q0 + q1) / 2 + mx), Y(ft + 6.9 + md), 'Microwave', { size: 12, fill: COL.G }));
  o.push(T(X((q0 + q1) / 2 + mx), Y(ft + 6.9 + md) + 14, '18.5 x 10 x 12 in', { size: 10.5, fill: COL.G }));
  // counter nook (a recess in the wall) with the jar shelf
  const nx0 = 58, nx1 = 93.25;
  o.push(box(nx0, nx1, ch, ch + 18.5, { fill: '#7A4A1E', fo: .2, stroke: '#7A4A1E', sw: 1.5, rx: 3, dash: '5 3' }));
  const nd = P.dzNook, ndx = P.dxNook;
  o.push(box(nx0 + ndx, nx1 + ndx, ch + 7.5 + nd, ch + 8.25 + nd, { fill: '#8A6B4D', stroke: '#3E230B', sw: 1 }));
  [ch, ch + 8.25 + nd].forEach(base => {
    for (let i = 0; i < 9; i++) {
      const jx = 58.75 + ndx + 3.75 * i;
      o.push(box(jx + .1, jx + 3.65, base, base + 6.25, { fill: '#A9D4F5', fo: .6, stroke: COL.BL, sw: .9, rx: 2.5 }));
      o.push(box(jx + .45, jx + 3.3, base + 6.25, base + 7, { fill: '#8A8A8A', stroke: COL.G, sw: .6 }));
    }
    o.push(Ln(X(58.4 + ndx), Y(base + 3.5), X(92.85 + ndx), Y(base + 3.5), { stroke: '#7A4A1E', sw: 1.6, dash: '3 2' }));
  });
  o.push(T(X(67), Y(ch + 16.7), 'Nook: quart jars', { size: 11, fill: '#7A4A1E' }));
  o.push(T(X(98.8), Y(ch + 8 + nd), `shelf ${fmt(ch + 7.5 + nd)} up`, { size: 10, fill: '#5A3510' }));
  o.push(T(X(98.8), Y(ch + 8 + nd) + 12, '9 jars a tier', { size: 10, fill: '#5A3510' }));
  // TV
  o.push(box(76.5, 103.5, ch + 16, ch + 31.4, { fill: COL.G, fo: .25, stroke: COL.G, sw: 1.5, rx: 3 }));
  o.push(T(X(90), Y(ch + 25), 'TV 30 in', { size: 12, fill: COL.G }));
  o.push(T(X(90), Y(ch + 25) + 14, '27 x 15.4, over the cabinet', { size: 10.5, fill: COL.G }));
  // fresh water tank on the floor at the sink end (runs out of the open sink cabinet)
  o.push(box(L.tankX[0], L.tankX[1], P.tankLift, P.tankLift + P.tankH, { fill: COL.BL, fo: .14, stroke: COL.BL, sw: 1.5, rx: 3, dash: '5 3' }));
  o.push(T(X((L.tankX[0] + L.tankX[1]) / 2), Y(P.tankLift + P.tankH * .62), 'Fresh water tank', { size: 12, fill: COL.BL }));
  o.push(T(X((L.tankX[0] + L.tankX[1]) / 2), Y(P.tankLift + P.tankH * .62) + 14, `${fmt(L.tankLen)} x ${fmt(P.tankD)} x ${fmt(P.tankH)}, ${P.tankLift > .01 ? fmt(P.tankLift) + ' in off the floor' : 'on the floor'}`, { size: 10.5, fill: COL.BL }));
  // angle marker
  o.push(Ln(X(angS), Y(23), X(angS), Y(ch), { stroke: '#A32D2D', sw: 2, dash: '5 3' }));
  // paper towels and towel bars in the angled front
  const pt0 = sinkS - 11.5, pt1 = sinkS - .5;
  o.push(box(pt0, pt1, 29.75, 35.25, { fill: '#B07A2A', fo: .35, stroke: '#B07A2A', sw: 1.5, rx: 3 }));
  o.push(T(X((pt0 + pt1) / 2), Y(32.5), 'Paper towels', { size: 12, fill: '#B07A2A' }));
  o.push(T(X((pt0 + pt1) / 2), Y(32.5) + 14, '11 in roll, recessed', { size: 10.5, fill: '#B07A2A' }));
  [25.5, 19.5].forEach(zb => { o.push(Ln(X(pt0), Y(zb), X(pt1), Y(zb), { stroke: COL.G, sw: 3.5, cap: 'round' })); o.push(`<circle cx="${f1(X(pt0))}" cy="${f1(Y(zb))}" r="3" fill="#444441"/><circle cx="${f1(X(pt1))}" cy="${f1(Y(zb))}" r="3" fill="#444441"/>`); });
  o.push(T(X((pt0 + pt1) / 2), Y(22.2), '2 towel bars, 11 in', { size: 9.5, fill: COL.G }));
  // hot water tank on the floor next to the wheel well (or on a shelf if raised), and sink plumbing
  if (P.hotShelf > .5) o.push(box(L.hotX[0] - 1, L.hotX[1] + 1, P.hotShelf - .75, P.hotShelf, { fill: '#8A6B4D', fo: .6, stroke: '#3E230B', sw: 1 }));
  o.push(box(L.hotX[0], L.hotX[1], P.hotShelf, P.hotShelf + P.hotH, { fill: '#C0392B', fo: .18, stroke: '#C0392B', sw: 1.5, rx: 3, dash: '5 3' }));
  o.push(T(X((L.hotX[0] + L.hotX[1]) / 2), Y(P.hotShelf + P.hotH * .6), 'Hot water tank', { size: 12, fill: '#C0392B' }));
  o.push(T(X((L.hotX[0] + L.hotX[1]) / 2), Y(P.hotShelf + P.hotH * .6) + 14, `${fmt(P.hotW)} x ${fmt(P.hotD)}, ${fmt(P.hotH)} tall; fittings at the back`, { size: 10.5, fill: '#C0392B' }));
  // relief valve drain line: from the valve on the back of the tank, up and over the top, forward, down in front of the fresh tank, out through the floor
  if (P.drainOn && P.hotShelf > 10) {
    const rx = L.hotX[0] + .8 * P.hotW, topz = P.hotShelf + P.hotH + 1.5 + P.drainDz, dx = P.drainX, st = { stroke: '#0F6E56', sw: 3, dash: '5 2' };
    o.push(Ln(X(rx), Y(P.hotShelf + P.hotH - 2), X(rx), Y(topz), st)); o.push(Ln(X(rx), Y(topz), X(dx), Y(topz), st)); o.push(Ln(X(dx), Y(topz), X(dx), Y(-2), st));
    o.push(`<circle cx="${f1(X(rx))}" cy="${f1(Y(P.hotShelf + P.hotH - 2))}" r="3.6" fill="#444441"/>`);
    o.push(T(X(dx), Y(topz) - 6, 'relief valve drain', { size: 9.5, fill: '#0F6E56' }));
    o.push(T(X(dx) + (E.flip ? 5 : -5), Y(3), 'through the floor to outside', { size: 8.5, fill: '#0F6E56', anchor: E.flip ? 'start' : 'end' }));
  }
  // the drawers and shelves under the counter: each one is an entry in L.parts (where it was planned plus how far it was dragged); the rail and the divider stay put
  {
    const dm = L.cabS + 14.75, z0 = ch - 6.75, z1 = ch - 2.75, part = id => L.partById[id];
    const board = p => box(p.x0, p.x1, p.z0, p.z1, { fill: '#8A6B4D', fo: 1, stroke: '#3E230B', sw: .8 });
    const drawer = p => box(p.x0, p.x1, p.z0, p.z1, { fill: '#8A5A00', fo: .2, stroke: '#8A5A00', sw: 1.5, rx: 3 });
    o.push(box(L.cabS, L.angS - .75, ch - 2.25, ch - 1.5, { fill: '#8A6B4D', fo: 1, stroke: '#3E230B', sw: .8 }));
    o.push(box(dm, dm + .5, z0 - .5, z1 + .25, { fill: '#8A6B4D', fo: 1, stroke: '#3E230B', sw: .8 }));
    const tb = part('TB'), tc = part('TC');
    o.push(drawer(tb)); o.push(drawer(tc));
    o.push(T(X(tb.x0 + 6.5), Y((tb.z0 + tb.z1) / 2) - 5, 'Drawer + tray', { size: 11, fill: '#8A5A00' }));
    o.push(T(X(tb.x0 + 6.5), Y((tb.z0 + tb.z1) / 2) + 7, '13 x 20 x 4', { size: 9, fill: '#8A5A00' }));
    o.push(T(X(tc.x0 + 6.5), Y((tc.z0 + tc.z1) / 2) - 5, 'Drawer', { size: 11, fill: '#8A5A00' }));
    o.push(T(X(tc.x0 + 6.5), Y((tc.z0 + tc.z1) / 2) + 7, '13 x 20 x 4', { size: 9, fill: '#8A5A00' }));
    // lower drawers under the pair: a 3/4 in shelf half an inch over the top of the hot water tank (or the wheel well, 7.5), 20 deep so they reach the wall over both
    if (part('SC')) {
      o.push(board(part('SC'))); o.push(board(part('SB')));
      o.push(box(dm, dm + .5, L.wellShelf + .75, z0 - .5, { fill: '#8A6B4D', fo: 1, stroke: '#3E230B', sw: .8 }));
      const drw = p => {
        const b0 = p.z0, b1 = p.z1;
        o.push(drawer(p));
        if (b1 - b0 < 5) { o.push(T(X((p.x0 + p.x1) / 2), Y((b0 + b1) / 2) + 3, `13 x 20 x ${fmt(b1 - b0)}`, { size: 9, fill: '#8A5A00' })); return; }
        o.push(T(X((p.x0 + p.x1) / 2), Y((b0 + b1) / 2) - 3, 'Drawer', { size: 11, fill: '#8A5A00' }));
        o.push(T(X((p.x0 + p.x1) / 2), Y((b0 + b1) / 2) + 10, `13 x 20 x ${fmt(b1 - b0)}`, { size: 9, fill: '#8A5A00' }));
      };
      // two 5 in drawers on the cab side (under the top pair, with the strip below them open), a 5 in one to the right of it (toward the back) with two equal drawers under it, on their own shelf 1/2 in over the wheel well; one row of two if there is too little height
      if (part('SC2')) {
        // cab side: two 5 in drawers; back side: a 5 in over two equal drawers when there is room (over the wheel well alone), else one drawer filling the space over the hot water tank
        o.push(board(part('SC2'))); drw(part('C1')); drw(part('C2'));
        if (part('SB1')) { o.push(board(part('SB1'))); o.push(board(part('SB2'))); drw(part('B1')); drw(part('B2')); drw(part('B3')); } else drw(part('B1'));
      } else { drw(part('B1')); drw(part('C1')); }
    }
  }
  o.push(Ln(X(sinkS + 8), Y(0), X(sinkS + 8), Y(ch - 7), { stroke: COL.BL, sw: 3, dash: '2 2' }));
  o.push(Ln(X(sinkS), Y(ch - P.sinkBowlD), X(sinkE), Y(ch - P.sinkBowlD), { stroke: COL.BL, sw: 1.6, dash: '5 3' }));
  o.push(T(X(sinkE - 1), Y(ch - P.sinkBowlD) + 11, `sink underside ${fmt(ch - P.sinkBowlD)} up (${fmt(P.sinkBowlD)} deep)`, { size: 9, fill: COL.BL, anchor: E.flip ? 'start' : 'end' }));
  o.push(T(X(sinkS + 10), Y(ch - 4), `sink plumbing, ${fmt(sinkE - sinkS - 8)} in from the cab-side edge`, { size: 9.5, fill: COL.BL }));
  // foot ledge on the cabinet end: hinged on its bottom edge, folds up into a recess in the end panel
  {
    const s = V.ledge || 0, phi = Math.PI / 2 * (1 - s), th = .75, Lg = L.ledgeTot, lz = P.ledgeH;
    const d = [Math.cos(phi), Math.sin(phi)], n = [-Math.sin(phi), Math.cos(phi)];
    const p0 = [sinkE, lz - th], p1 = [p0[0] + Lg * d[0], p0[1] + Lg * d[1]];
    const q0 = [p0[0] + th * n[0], p0[1] + th * n[1]], q1 = [p1[0] + th * n[0], p1[1] + th * n[1]];
    const px = pt => [X(pt[0]), Y(pt[1])];
    let g = box(sinkE - th, sinkE, lz - th, lz - th + Lg, { stroke: '#5A3A00', sw: .8, dash: '2 2', so: .55 });
    if (s > .6) { const a1 = px([sinkE, lz - th - 6]), a2 = px([sinkE + Lg - 1.5, lz - th]); g += Ln(a1[0], a1[1], a2[0], a2[1], { stroke: '#5A3A00', sw: 2.2, so: clamp((s - .6) / .4, 0, 1) }); }
    g += Poly([px(p0), px(p1), px(q1), px(q0)], { fill: '#B07A2A', fo: .9, stroke: '#5A3A00', sw: 1.2 });
    g += `<circle cx="${f1(px(p0)[0])}" cy="${f1(px(p0)[1])}" r="2.6" fill="#5A3A00"/>`;
    if (s > .5) g += T(X(sinkE + Lg / 2 + 3), Y(lz - 5), `Foot ledge, ${fmt(Lg)} x ${fmt(P.sinkD)}, top ${fmt(lz)} up`, { size: 10.5, fill: '#5A3A00', op: (s - .5) * 2 });
    o.push(MV('ledge', g, HITR(Math.min(X(sinkE), X(sinkE + Lg)), Y(lz + 3), S * Lg, S * 5) + HITR(Math.min(X(sinkE - 2), X(sinkE + .5)), Y(lz - th + Lg), S * 2.5, S * Lg)));
  }
  // fold-out table at the cab-side end of the sink cabinet: hinged on the cabinet end, folds down against it, carried by a folding brace
  {
    const s = V.flap || 0, phi = -Math.PI / 2 * (1 - s), th = 0.75, Lf = L.flapLen - th, hz = P.flapH;
    const d = [Math.cos(phi), Math.sin(phi)], n = [-Math.sin(phi), Math.cos(phi)];
    const p0 = [sinkE + th, hz], p1 = [p0[0] + Lf * d[0], p0[1] + Lf * d[1]];
    const q0 = [p0[0] - th * n[0], p0[1] - th * n[1]], q1 = [p1[0] - th * n[0], p1[1] - th * n[1]];
    const px = pt => [X(pt[0]), Y(pt[1])];
    // brace: an arm hinged on the cabinet end 13 in below the board; folded it lies up along the end, open it swings to the board's underside 15 3/4 in out
    const A = [sinkE, hz - th - 13], tx = sinkE + th + 15, tz = hz - th, ang1 = Math.atan2(tz - A[1], tx - A[0]), blen = Math.hypot(tx - A[0], tz - A[1]);
    const u = clamp((s - .55) / .45, 0, 1), ang = Math.PI / 2 + u * (ang1 - Math.PI / 2), tip = [A[0] + blen * Math.cos(ang), A[1] + blen * Math.sin(ang)];
    let g = Ln(px(A)[0], px(A)[1], px(tip)[0], px(tip)[1], { stroke: '#5A3A00', sw: 3, cap: 'round' });
    g += `<circle cx="${f1(px(A)[0])}" cy="${f1(px(A)[1])}" r="3" fill="#5A3A00"/>`;
    g += Poly([px(p0), px(p1), px(q1), px(q0)], { fill: '#B07A2A', fo: .9, stroke: '#5A3A00', sw: 1.2 });
    g += `<circle cx="${f1(px(p0)[0])}" cy="${f1(px(p0)[1])}" r="3.2" fill="#5A3A00"/>`;
    const lx = sinkE + L.flapLen / 2;
    if (s > .5) {
      g += T(X(lx), Y(hz + 17), 'Fold-out table', { size: 11.5, fill: '#5A3A00', op: (s - .5) * 2 });
      g += T(X(lx), Y(hz + 13.5), `${fmt(L.flapLen)} long x ${fmt(P.flapD)} deep, ${fmt(hz)} up, folding brace under it`, { size: 10, fill: '#5A3A00', op: (s - .5) * 2 });
    } else {
      g += T(X(sinkE + 6), Y(hz + 4), 'click: fold-out table', { size: 10, fill: '#5A3A00', op: 1 - s * 2 });
    }
    o.push(MV('flap,ledge', g, HITR(Math.min(X(sinkE), X(sinkE + L.flapLen)), Y(hz + 3), S * L.flapLen, S * 6) + HITR(Math.min(X(sinkE), X(sinkE + 3)), Y(hz + 2), S * 3, S * (hz + 2))));
  }
  // sliding door opening and the entry
  const dx1 = Math.min(P.doorX + P.slideW, P.cab + 1);
  o.push(R(Math.min(X(P.doorX), X(dx1)), Y(P.slideH), S * (dx1 - P.doorX), S * P.slideH, { stroke: '#BA7517', sw: 2, dash: '8 4' }));
  o.push(T(X((P.doorX + dx1) / 2), Y(52), `Sliding door opening (${fmt(P.doorX)} to ${fmt(dx1 + 0)})`, { size: 12, fill: '#854F0B' }));
  o.push(T(X(P.cab - 8), Y(13), `Entry, ${fmt(L.entry)} in clear`, { size: 11, fill: COL.G }));
  // the cab passenger seat cushion level, in the strip past the cab wall
  o.push(Ln(X(P.cab - P.cabSeatOut), Y(P.cabSeatH), X(P.cab + 7), Y(P.cabSeatH), { stroke: '#534AB7', sw: 3 }));
  o.push(T(X(P.cab + 3.5), Y(P.cabSeatH) - 5, `cab seat ${fmt(P.cabSeatH)} up, sticks out ${fmt(P.cabSeatOut)}`, { size: 9, fill: '#534AB7' }));
  o.push(elevTail(E, L, 'inches from where you start measuring at the back'));
  // things you can drag (this view runs right to left, so a drag to the right moves toward the rear; up is up): the drawers and boards, then the shelves in the nook and over the fridge, then the tanks
  {
    const hx = (x0, x1) => Math.min(X(x0), X(x1));
    L.parts.filter(p => p.kind === 'drawer' && p.z1 - p.z0 > .5).forEach(p => o.push(HIT(p.id, hx(p.x0, p.x1), Y(p.z1), S * (p.x1 - p.x0), S * (p.z1 - p.z0), [p.dxk, -1 / S, p.dzk, -1 / S], L.coll.ids.has(p.id), cap(p.n) + ' (along the wall and up)')));
    L.parts.filter(p => p.kind === 'shelf').forEach(p => o.push(HIT(p.id, hx(p.x0, p.x1), Y(p.z1) - 4, S * (p.x1 - p.x0), S * (p.z1 - p.z0) + 8, [p.dxk, -1 / S, p.dzk, -1 / S], L.coll.ids.has(p.id), cap(p.n) + ' (along the wall and up)')));
    o.push(HIT('Nook', hx(nx0 + ndx, nx1 + ndx), Y(ch + 8.25 + nd) - 4, S * (nx1 - nx0), S * .75 + 8, ['dxNook', -1 / S, 'dzNook', -1 / S], L.coll.ids.has('Nook'), 'The jar shelf in the nook with its upper row of jars (along the wall and up)'));
    o.push(HIT('Micro', hx(q0 + mx, q1 + mx), Y(ft + 12.75 + md), S * (q1 - q0), S * 10.75, ['dxMicro', -1 / S, 'dzMicro', -1 / S], L.coll.ids.has('Micro'), 'The microwave and its shelf (along the wall and up)'));
  }
  o.push(HIT('fresh', Math.min(X(L.tankX[0]), X(L.tankX[1])), Y(P.tankLift + P.tankH), S * L.tankLen, S * P.tankH, ['tankShift', 1 / S, 'tankLift', -1 / S], L.coll.ids.has('fresh'), 'Fresh water tank (along the wall and up)'));
  if (P.drainOn && P.hotShelf > 10) o.push(HIT('drain', X(P.drainX) - 8, Y(P.hotShelf + P.hotH + 1.5) - 4, 16, S * (P.hotShelf + P.hotH + 1.5 + 2) + 8, ['drainX', -1 / S, 'drainDz', -1 / S], false, 'Relief valve drain line (where it comes down, and the height of its run)'));
  o.push(HIT('hot', Math.min(X(L.hotX[0]), X(L.hotX[1])), Y(P.hotShelf + P.hotH), S * P.hotW, S * P.hotH, ['hotX0', -1 / S, 'hotShelf', -1 / S], L.coll.ids.has('hot'), 'Hot water tank (along the wall and up)', 'hotFree'));
  return { w: E.W, h: E.H, body: o.join('') };
}

/* ================= cross-section from the rear doors: both walls leaning in toward the flat roof ================= */
function drawCross(L, V) {
  const P = L.P, S = 7, X0 = 260, zMax = Math.max(P.roofMidH + P.ribDepth + 6, 88), FL = 60 + S * zMax, W = P.vanW, o = [];
  const xx = y => X0 + S * y, yy = z => FL - S * z, bx = (y0, y1, z0, z1, q) => R(xx(y0), yy(z1), S * (y1 - y0), S * (z1 - z0), q);
  const lean = z => L.leanAt(z), s0 = Math.min(Math.max(L.leanStart, 0), P.ceil), lc = lean(P.ceil);
  o.push(T(20, 22, 'Cross-section seen from the rear doors: driver side wall on the left, passenger side on the right.', { anchor: 'start', size: 14, fill: '#5F5E5A', halo: false }));
  o.push(T(20, 40, P.leanOn && L.leanK > 0 ? `Walls straight up to ${fmt(L.leanStart)} in, then leaning in ${(L.leanK * 12).toFixed(2)} in per foot (${(Math.atan(L.leanK) * 180 / Math.PI).toFixed(1)} degrees), ${fmt(lean(P.roofWallH))} in each at ${fmt(P.roofWallH)} up (${fmt(W - 2 * lean(P.roofWallH))} wide); roof arcs to ${fmt(P.roofMidH)} in the middle.` : 'The walls are drawn straight up (lean switched off).', { anchor: 'start', size: 12, fill: '#5F5E5A', halo: false }));
  for (let y = 0; y <= W; y += 10) { o.push(Ln(xx(y), yy(zMax), xx(y), FL, { stroke: '#3F3E3A', so: .3, sw: .9, dash: '3 3' })); o.push(T(xx(y), FL + 18, y + '', { size: 11, fill: '#185FA5', w: 700, halo: false })); }
  for (let z = 0; z <= zMax; z += 10) { o.push(Ln(xx(0), yy(z), xx(W), yy(z), { stroke: '#3F3E3A', so: .3, sw: .9, dash: '3 3' })); o.push(T(xx(0) - 6, yy(z) + 4, z + '↑', { anchor: 'end', size: 11, fill: '#8A4B0F', w: 700, halo: false })); }
  o.push(T(xx(W / 2), FL + 38, 'inches across from the driver side wall', { size: 12, fill: '#5F5E5A', halo: false }));
  // the inside of the van, and the space lost to the lean (hatched) outside the straight walls
  const zw = P.roofWallH, lw = lean(zw), arc = []; for (let i = 0; i <= 40; i++) { const y = lw + (W - 2 * lw) * i / 40; arc.push([xx(y), yy(L.roofZ(y))]); }
  o.push(Poly([[xx(0), yy(0)], [xx(0), yy(Math.min(s0, zw))], [xx(lw), yy(zw)], ...arc, [xx(W - lw), yy(zw)], [xx(W), yy(Math.min(s0, zw))], [xx(W), yy(0)]], { fill: '#F1EFE8', fo: .7, stroke: '#2C2C2A', sw: 2.4 }));
  if (lw > 0) { o.push(Poly([[xx(0), yy(s0)], [xx(0), yy(zw)], [xx(lw), yy(zw)]], { fill: 'url(#hatch)', fo: .5, stroke: '#A32D2D', sw: 1, dash: '4 3' })); o.push(Poly([[xx(W), yy(s0)], [xx(W), yy(zw)], [xx(W - lw), yy(zw)]], { fill: 'url(#hatch)', fo: .5, stroke: '#A32D2D', sw: 1, dash: '4 3' })); }
  // outside of the steel roof: the ribs hang ribDepth below it, so it is that much above the rib height
  o.push(`<polyline points="${arc.map(p => f1(p[0]) + ',' + f1(p[1] - S * P.ribDepth)).join(' ')}" fill="none" stroke="#5F5E5A" stroke-width="1.4" stroke-dasharray="2 3"/>`);
  o.push(T(xx(W / 2), yy(L.roofZ(W / 2) + P.ribDepth) - 6, `outside of the steel roof ${fmt(L.roofZ(W / 2) + P.ribDepth)} in up in the middle (ribs ${fmt(P.ribDepth)} deep)`, { size: 10.5, fill: '#5F5E5A', halo: false }));
  // finished ceiling
  if (L.lining > 0) o.push(`<polyline points="${arc.map(p => f1(p[0]) + ',' + f1(p[1] + S * L.lining)).join(' ')}" fill="none" stroke="#8A6B4D" stroke-width="1.6" stroke-dasharray="6 3"/>`);
  o.push(T(xx(W / 2), yy(L.roofZ(W / 2) - L.lining) + 24, `roof ribs ${fmt(zw)} at the wall, ${fmt(L.roofZ(W / 2))} in the middle`, { size: 11, fill: '#5A3A00' })); if (L.lining > 0) o.push(T(xx(W / 2), yy(L.roofZ(W / 2) - L.lining) + 38, `finished ceiling ${fmt(zw - L.lining)} at the wall, ${fmt(L.roofZ(W / 2) - L.lining)} in the middle`, { size: 11, fill: '#5A3A00' }));
  // width at the two measured heights, at the cabinet bottom and at the finished ceiling
  [[P.leanZ1, 'measured'], [P.leanZ2, 'measured'], [P.cabBot, 'cabinet bottom']].forEach(([z, nm], i) => { const l = lean(z), x0 = xx(l), x1 = xx(W - l); o.push(Ln(x0, yy(z), x1, yy(z), { stroke: '#A32D2D', sw: 1.2, mk: true })); o.push(T(xx(W / 2) + (i === 2 ? 0 : 0), yy(z) - 4, `${fmt(W - 2 * l)} wide at ${fmt(z)} up (${nm})`, { size: 10.5, fill: '#A32D2D' })); });
  // driver side: couch and the wall cabinets; passenger side: counter, fridge, microwave shelf
  o.push(bx(0, P.bedD, 0, P.seatH, { fill: COL.P, fo: .18, stroke: COL.P, sw: 1.5, rx: 3 })); o.push(T(xx(P.bedD / 2), yy(P.seatH / 2), 'couch', { size: 11, fill: COL.P }));
  o.push(bx(0, 6, P.seatH, P.backH, { fill: COL.P, fo: .18, stroke: COL.P, sw: 1.5, rx: 3 }));
  // wall cabinets and the closet have open backs: the side panels run against the leaning wall, front edge vertical
  {
    const bk = P.cabBackIn, yf = bk + P.cabDepth, b0 = Math.max(bk, lean(P.cabBot)), b1 = Math.max(bk, lean(L.ceilF));
    o.push(Poly([[xx(b0), yy(P.cabBot)], [xx(yf), yy(P.cabBot)], [xx(yf), yy(L.ceilF)], [xx(b1), yy(L.ceilF)]], { fill: '#534AB7', fo: .16, stroke: '#534AB7', sw: 1.6, dash: '5 3' }));
    const cd = P.closetD, c1 = Math.max(0, lean(L.ceilF));
    o.push(Poly([[xx(0), yy(0)], [xx(cd), yy(0)], [xx(cd), yy(L.ceilF)], [xx(c1), yy(L.ceilF)], [xx(lean(Math.max(L.leanStart, 0.0001)) ), yy(Math.min(L.leanStart, L.ceilF))]], { fill: 'none', stroke: '#444441', sw: 1.2, dash: '2 3' }));
    o.push(T(xx(cd - 4), yy(L.ceilF - 26), `closet ${fmt(cd)} deep`, { size: 10, fill: '#444441' }));
  }
  o.push(T(xx(P.cabBackIn + P.cabDepth / 2 + 1.5), yy((P.cabBot + L.ceilF) / 2), 'wall cabinet', { size: 11, fill: '#3C3489' })); o.push(T(xx(P.cabBackIn + P.cabDepth / 2 + 1.5), yy((P.cabBot + L.ceilF) / 2) + 13, `${fmt(P.cabDepth)} deep`, { size: 10, fill: '#3C3489' }));
  o.push(bx(W - P.cabD, W, 0, P.counterH, { fill: COL.C, fo: .12, stroke: COL.C, sw: 1.5, rx: 3 })); o.push(T(xx(W - P.cabD / 2), yy(P.counterH / 2), 'counter and cabinet', { size: 11, fill: COL.C }));
  o.push(bx(W - 2 - 19, W - 2, 8.25, 56.25, { fill: '#0A6A8A', fo: .14, stroke: '#0A6A8A', sw: 1.4, dash: '5 3' })); o.push(T(xx(W - 11.5), yy(40), 'fridge', { size: 11, fill: '#0A6A8A' }));
  o.push(bx(W - 12 - P.microIn, W - P.microIn, 59, 69, { fill: COL.G, fo: .2, stroke: COL.G, sw: 1.4, rx: 2 })); o.push(T(xx(W - 6 - P.microIn), yy(64.5), 'micro', { size: 10, fill: COL.G }));
  o.push(T(xx(0) + 6, yy(P.roofMidH + P.ribDepth + 5), 'driver side wall', { anchor: 'start', size: 11, fill: '#5F5E5A', halo: false })); o.push(T(xx(W) - 6, yy(P.roofMidH + P.ribDepth + 5), 'passenger side wall', { anchor: 'end', size: 11, fill: '#5F5E5A', halo: false }));
  o.push(Ln(xx(0), yy(0), xx(W), yy(0), { stroke: '#5F5E5A', sw: 2 }));
  o.push(T(20, FL + 58, 'Things at different places along the van are drawn together (the fridge and the counter are side by side along the wall, not on top of each other).', { anchor: 'start', size: 10.5, fill: '#5F5E5A', halo: false }));
  return { w: xx(W) + 260, h: FL + 72, body: o.join('') };
}

/* ================= the bed seen from the end: the leaf flipping over, the legs folding down out of their slots ================= */
function drawBedEnd(L, V) {
  const P = L.P, s = V.bed || 0, bs = bedState(s), S = 10, X0 = 80, zMax = 44, FL = 60 + S * zMax, LW = P.bedBack, lt = .75, deck = P.platform - lt, bt = P.platform + P.mattress;
  const yMax = Math.max(P.bedD + LW, 46) + 6, xx = y => X0 + S * y, yy = z => FL - S * z;
  const bx = (y0, y1, z0, z1, o) => R(xx(y0), yy(z1), S * (y1 - y0), S * (z1 - z0), o);
  const o = [];
  o.push(T(X0, 22, 'The bed seen from the rear doors, cut across the couch: wall on the left, aisle on the right.', { anchor: 'start', size: 14, fill: '#5F5E5A', halo: false }));
  o.push(T(X0, 40, 'Click the couch to make up the bed. The leaf flips out on the hinge at the front of the deck; the legs lie in slots in it.', { anchor: 'start', size: 12, fill: '#5F5E5A', halo: false }));
  for (let y = 0; y <= yMax; y += 10) { o.push(Ln(xx(y), yy(zMax), xx(y), FL, { stroke: '#3F3E3A', so: .35, sw: .9, dash: '3 3' })); o.push(T(xx(y), FL + 18, y + '→', { size: 11, fill: '#185FA5', w: 700, halo: false })); }
  for (let z = 0; z <= zMax; z += 10) { o.push(Ln(xx(0), yy(z), xx(yMax), yy(z), { stroke: '#3F3E3A', so: .35, sw: .9, dash: '3 3' })); o.push(T(xx(0) - 6, yy(z) + 4, z + '↑', { anchor: 'end', size: 11, fill: '#8A4B0F', w: 700, halo: false })); }
  o.push(T(xx(yMax / 2), FL + 38, 'inches out from the wall', { size: 12, fill: '#5F5E5A', halo: false }));
  o.push(Ln(xx(0), yy(0), xx(yMax), yy(0), { stroke: '#5F5E5A', sw: 2 }));
  o.push(Ln(xx(0), yy(zMax), xx(0), yy(0), { stroke: '#2C2C2A', sw: 3 }));
  // wheel well, battery, and the shower pan's front edge (all are at other places along the wall; dashed)
  o.push(bx(0, 6.25, 0, 7.5, { fill: '#E24B4A', fo: .2, stroke: '#A32D2D', sw: 1.4, dash: '5 3' }));
  o.push(T(xx(3.1), yy(3), 'well', { size: 10, fill: '#791F1F', halo: false }));
  o.push(bx(6.25, 16.25, 0, 9.5, { fill: '#F2B84B', fo: .35, stroke: '#8A5A00', sw: 1.4, dash: '5 3' }));
  o.push(T(xx(11.25), yy(4.5), 'battery', { size: 10, fill: '#5A3A00', halo: false }));
  const pe = P.vanW - P.panD;
  if (pe < yMax) { o.push(bx(pe, Math.min(yMax, P.vanW), 0, 3, { fill: '#185FA5', fo: .15, stroke: '#185FA5', sw: 1.2, dash: '4 3' })); o.push(T(xx(pe + 1), yy(1.2), 'shower pan, down', { anchor: 'start', size: 9.5, fill: '#185FA5', halo: false })); }
  // the base: a front rail under the deck edge and the deck itself (the ends and the wall ledger are behind the cut)
  o.push(bx(0, P.bedD, deck - lt, deck, { fill: COL.G, fo: .3, stroke: COL.G, sw: 1.2 }));
  o.push(bx(P.bedD - .75, P.bedD, deck - lt - 1.5, deck - lt, { fill: COL.G, fo: .3, stroke: COL.G, sw: 1 }));
  o.push(T(xx(P.bedD + 1.2), yy(deck - lt - .6), 'base front rail holds up the deck front', { anchor: 'start', size: 10, fill: COL.G, halo: false, op: bs.th < .2 ? 1 : 0 }));
  // the leaf: hinged on the top faces at the deck front edge (y = bedD, z = deck); th: 0 folded back on the deck, pi flipped out level
  const th = bs.th, hy = P.bedD, d = [-Math.cos(th), Math.sin(th)], n = [Math.sin(th), Math.cos(th)];
  const pt = (r, t) => [xx(hy + r * d[0] + t * n[0]), yy(deck + r * d[1] + t * n[1])];
  const leaf = [pt(0, 0), pt(LW, 0), pt(LW, lt), pt(0, lt)];
  o.push(Poly(leaf, { fill: '#B07A2A', fo: .75, stroke: '#5A3A00', sw: 1.2 }));
  // the leg slot is shown as the leg: lying in the leaf (dark line) or swung down
  const tp = lt / 2, LG = deck - tp - .25, rp = LW - P.legIn, psi = bs.legs * Math.PI / 2;
  const p0 = pt(rp, tp);
  if (bs.legs < .01) { const p1 = pt(rp - LG, tp); o.push(Ln(p0[0], p0[1], p1[0], p1[1], { stroke: '#2C2C2A', sw: 3.75, cap: 'round' })); }
  else { const tipY = hy + rp - LG * Math.cos(psi), tipZ = deck - tp - LG * Math.sin(psi); o.push(Ln(p0[0], p0[1], xx(tipY), yy(tipZ), { stroke: COL.G, sw: 3.75, cap: 'round' })); if (bs.legs > .9) { o.push(bx(tipY - .7, tipY + .7, 0, .25, { fill: COL.G })); o.push(T(xx(tipY - 1.4), yy(5.5), `legs land ${fmt(hy + rp)} in out`, { anchor: 'end', size: 10, fill: COL.G, halo: false, op: (bs.legs - .9) * 10 })); } }
  const hp = pt(0, 0); o.push(`<circle cx="${f1(hp[0])}" cy="${f1(hp[1])}" r="3.6" fill="#2C2C2A"/>`);
  o.push(T(xx(P.bedD + 1.5), yy(deck + 3.2), 'hinge on the top faces', { anchor: 'start', size: 10, fill: '#5A3A00', halo: false, op: bs.th < .2 ? 1 : 0 }));
  // cushions: the seat cushion rides on the folded leaf by day (top at plat + mattress) and sits on the deck at night; the back cushion stands, then lies on the leaf
  const sb0 = deck + lt * Math.max(0, Math.cos(th)), fade = 1 - .75 * Math.sin(clamp((s - .2) / .6, 0, 1) * Math.PI);
  o.push(bx(0, P.bedD, sb0, sb0 + P.mattress, { fill: COL.P, fo: .12 * fade, stroke: COL.P, sw: 1.4, rx: 3, so: fade }));
  if (bs.back > .02) o.push(bx(0, P.mattress, bt, bt + LW * bs.back, { fill: COL.P, fo: .1, stroke: COL.P, sw: 1.4, rx: 3 }));
  if (bs.flat > .02) {
    o.push(bx(0, P.bedD, deck, deck + P.mattress, { fill: COL.P, fo: .2 * bs.flat, stroke: COL.P, sw: 2, rx: 3, so: bs.flat }));
    o.push(bx(P.bedD, P.bedD + LW, deck, deck + P.mattress, { fill: COL.P, fo: .2 * bs.flat, stroke: COL.P, sw: 2, rx: 3, so: bs.flat }));
    o.push(T(xx(P.bedD / 2), yy(deck + P.mattress / 2) + 4, 'seat cushion', { size: 11, fill: COL.P, op: bs.flat }));
    o.push(T(xx(P.bedD + LW / 2), yy(deck + P.mattress / 2) + 4, 'back cushion, lying', { size: 11, fill: COL.P, op: bs.flat }));
    o.push(Ln(xx(0), yy(deck + P.mattress + 4), xx(P.bedD + LW), yy(deck + P.mattress + 4), { stroke: '#A32D2D', sw: 1.6, mk: true, so: bs.flat }));
    o.push(T(xx((P.bedD + LW) / 2), yy(deck + P.mattress + 4) - 6, `bed ${fmt(P.bedD)} + ${fmt(LW)} = ${fmt(P.bedD + LW)} wide, top at ${fmt(deck + P.mattress)}`, { size: 11.5, fill: '#A32D2D', w: 500, op: bs.flat }));
  } else if (bs.th < .05) o.push(T(xx(P.bedD / 2), yy(sb0 + P.mattress / 2) + 4, `seat cushion, top at ${fmt(bt)}`, { size: 11, fill: COL.P }));
  o.push(MV('bed', '', HITR(xx(0), yy(bt + LW), S * (P.bedD + LW), S * (bt + LW))));
  return { w: xx(yMax) + 60, h: FL + 70, body: o.join('') };
}
