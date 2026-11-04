/* One diagram for each wire (wires.html): where its power comes from (a chain of boxes from the power source, with the wire numbers and the fuses on the
   arrows) and its whole run on the walls and the ceiling, zoomed to the wire, with START and END marks. Used by electric.js after the wire list is made. */
const EW = require('./elwires.js');

// ---- the chain of parts that power each wire. Tokens: 'Name|second line' is a box; 'WR12' is a wire (drawn in its gauge colour on the arrow); '-' is a plain
//      link (a cord or a plug); 'f:text' is the fuse or breaker on the arrow that follows.
const BAT = 'Battery|280 Ah', BUS = 'Bus bar|and shunt', FB = 'Fuse block|10-way, 5 ways used';
const DCB = [BAT, 'WR1', 'f:Class T 250 A', BUS, 'WR13', 'f:30 A fuse', FB];       // battery to the 12 V fuse block
const ACP = ['Shore power|inlet ED6', 'WR7', 'f:30 A breaker', 'Transfer switch|TS-30, 30 A', 'WR9', 'f:30 A main', 'AC panel|120 V'];
const ALT_AC = 'On the inverter instead of shore power: Battery → WR1 → Bus bar → WR3 → Inverter → WR8 → Transfer switch → WR9 → AC panel. The transfer switch passes one or the other, never both.';
const CHAINS = {
  WR1: [BAT, 'WR1', 'f:Class T 250 A', 'Bus bar|+ side'],
  WR2: [BAT, 'WR2', 'f:shunt, 500 A', 'Bus bar|− side'],
  WR3: [BAT, 'WR1', 'f:Class T 250 A', BUS, 'WR3', 'f:250 A', 'Inverter|BELTTT 2000 W'],
  WR4: ['Starter battery|and alternator', 'WR4', 'f:80 A at the starter battery', 'DC-DC charger|LiTime 60 A'],
  WR5: ['Starter battery|and alternator', 'WR4', 'f:80 A', 'DC-DC charger|LiTime 60 A', 'WR5', 'f:80 A at the bus', BUS, 'WR1', 'f:Class T 250 A', 'Battery|being charged'],
  WR6: ['Shore power|inlet ED6', 'WR7', 'f:30 A breaker', 'Transfer switch|TS-30, 30 A', 'WR9', 'f:30 A main', 'AC panel|120 V', 'WR10', 'f:15 A breaker', 'Shore charger|VEVOR 80 A', 'WR6', 'f:100 A at the bus', 'Bus bar|and shunt'],
  WR7: ['Shore power|campground pedestal', '-', 'Shore inlet ED6|30 A', 'WR7', 'f:30 A breaker', 'Transfer switch|TS-30, 30 A'],
  WR8: [BAT, 'WR1', 'f:Class T 250 A', BUS, 'WR3', 'f:250 A', 'Inverter|BELTTT 2000 W', 'WR8', 'f:20 A', 'Transfer switch|TS-30, 30 A'],
  WR9: ['Shore power|inlet ED6', 'WR7', 'f:30 A breaker', 'Transfer switch|TS-30, 30 A', 'WR9', 'f:30 A main', 'AC panel|120 V'],
  WR10: ACP.concat(['WR10', 'f:15 A breaker', 'Shore charger|VEVOR 80 A']),
  WR11: [BAT, 'WR11', 'f:100 A fuse at the battery', 'A/C|on the roof'],
  WR12: ACP.concat(['WR12', 'f:B/D 15 A GFCI, C 15 A', 'Circuits B/D and C|through riser A, the ceiling, riser B']),
  WR13: [BAT, 'WR1', 'f:Class T 250 A', BUS, 'WR13', 'f:30 A fuse', FB],
  WR14: DCB.concat(['WR14', 'f:10 A fuse', 'Junction box JB|dimming controller', '-', 'LED strip|three runs']),
  WR15: DCB.concat(['WR15', 'f:5 A fuse', 'Roof fan']),
  WR16: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|in the couch cabinet']),
  WR17: DCB.concat(['WR14', 'f:10 A fuse', 'JB|dimming controller', 'WR17', 'Dimmer button ED14']),
  WR18: ACP.concat(['f:15 A GFCI (A)', 'WR18', 'Couch outlet ED10']),
  WR19: ACP.concat(['f:15 A GFCI (A)', 'WR18', 'Couch outlet ED10', 'WR19', 'Dinette outlet ED15']),
  WR20: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR20', 'Switch ED19|then light ED18']),
  WR21: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR21', 'Rear doors plate|ED11, two switches']),
  WR22: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR21', 'Plate ED11|rear couch switch', 'WR22', 'Rear couch light|ED7']),
  WR23: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR21', 'Plate ED11|shower switch', 'WR23', 'Shower light|EP1, IP65']),
  WR24: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR24', 'Dinette switch|ED12 on W2']),
  WR25: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR24', 'Dinette switch|ED12 on W2', 'WR25', 'Dinette lights|ED8 and ED9']),
  WR26: ACP.concat(['WR12', 'f:15 A (C, fridge only)', 'Riser B', 'WR26', 'Fridge outlet EP3']),
  WR27: ACP.concat(['WR12', 'f:15 A GFCI (B/D)', 'Riser B', 'WR27', 'Selector EP9|30 A rocker']),
  WR28: ACP.concat(['WR12', 'f:15 A GFCI (B/D)', 'Riser B', 'WR27', 'Selector EP9|30 A rocker', 'WR28', 'Microwave outlet|EP4']),
  WR29: ACP.concat(['WR12', 'f:15 A GFCI (B/D)', 'Riser B', 'WR27', 'Selector EP9|30 A rocker', 'WR29', 'Heater outlet EP7|beside the tank']),
  WR30: ACP.concat(['f:15 A GFCI (A)', 'WR18', 'Couch outlet ED10', 'WR30', 'TV outlet EP6']),
  WR31: DCB.concat(['WR31', 'f:10 A fuse', 'Water pump|PL3']),
  WR32: DCB.concat(['WR32', 'f:3 A fuse', 'Control panel|EP5']),
  WR33: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR35', 'Switch EP11', 'WR33', 'Light EP2']),
  WR34: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR35', 'Switch EP14', 'WR34', 'Lights EP12, EP13']),
  WR36: DCB.concat(['WR14', 'f:10 A fuse', 'JB|dimming controller', 'WR36', 'Dimmer button ED22|with the dinette switch']),
  WR35: DCB.concat(['WR16', 'f:5 A fuse', 'Junction box JB|couch cabinet', 'WR35', 'Switches EP11|and EP14']),
};
const ALT_WIRES = new Set(['WR6', 'WR9', 'WR10', 'WR12', 'WR18', 'WR19', 'WR26', 'WR27', 'WR28', 'WR29', 'WR30']);   // the cards that show the inverter as the other source

function parse(tokens) {
  const nodes = [], links = []; let pend = null;
  tokens.forEach(t => {
    if (/^WR\d+$/.test(t)) { pend = pend || {}; pend.wire = t; }
    else if (t === '-') { pend = pend || {}; pend.wire = null; }
    else if (t.startsWith('f:')) { pend = pend || {}; pend.fuse = t.slice(2); }
    else { if (nodes.length) { links.push(pend || {}); } pend = null; nodes.push(t); }
  });
  return { nodes, links };
}
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function wrap(txt, n) { const out = []; let cur = ''; txt.split(' ').forEach(w => { if ((cur + ' ' + w).trim().length > n && cur) { out.push(cur); cur = w; } else cur = (cur + ' ' + w).trim(); }); if (cur) out.push(cur); return out; }

// ---- the power chain of one wire
function chainSVG(w, WRbyId) {
  const { nodes, links } = parse(CHAINS[w.id]);
  const perRow = 5, bw = 150, bh = 58, gap = 72, x0 = 16, rowH = 120, top = 38;
  const rows = Math.ceil(nodes.length / perRow), H = top + rows * rowH - 10;
  const pos = i => { const r = Math.floor(i / perRow), c = i % perRow; return { x: x0 + c * (bw + gap), y: top + r * rowH, r, c }; };
  const o = [];
  const arrowHead = (x, y, dir, col) => `<path d="M${x} ${y} l${-9 * dir} -6 l0 12 Z" fill="${col}" stroke="#fff" stroke-width=".8"/>`;
  links.forEach((lk, i) => {
    const a = pos(i), b = pos(i + 1), g = lk.wire ? WRbyId[lk.wire].g : null, col = g ? EW.gc(g) : '#8a8a84', lw = g ? Math.min(EW.gw(g), 7) : 2;
    const focus = lk.wire === w.id, dash = lk.wire && WRbyId[lk.wire].t === 'ac' ? ' stroke-dasharray="9 6"' : '';
    const ay = a.y + bh / 2;
    let px, py, path;
    if (a.r === b.r) { const xa = a.x + bw, xb = b.x; path = `M${xa} ${ay} L${xb - 8} ${ay}`; px = (xa + xb) / 2; py = ay - 15; if (focus) o.push(`<rect x="${xa + 1}" y="${a.y - 6}" width="${gap - 2}" height="${bh + 12}" rx="9" fill="#FFF3B0"/>`);
      o.push(`<g opacity="${focus || !g ? 1 : .6}"><path d="${path}" fill="none" stroke="#fff" stroke-width="${lw + 3}" stroke-linecap="round"/><path d="${path}" fill="none" stroke="${col}" stroke-width="${focus ? lw + 1.5 : lw}"${dash}/>${arrowHead(xb, ay, -1, col)}</g>`);
      if (g) o.push(EW.wirePill(lk.wire, g, px, py + (focus ? 0 : 0)));
      if (lk.fuse) wrap(lk.fuse, 13).slice(0, 3).forEach((ln, k) => o.push(`<text x="${px}" y="${ay + 16 + k * 11}" text-anchor="middle" style="font-size:9.5px;fill:#3d3b34">${esc(ln)}</text>`));
    } else {                                        // wrap to the next row: down, back along the gap between the rows, down into the first box
      const xa = a.x + bw / 2, ya = a.y + bh, xb = b.x + bw / 2, yb = b.y, ym = (ya + yb) / 2;
      path = `M${xa} ${ya} L${xa} ${ym} L${xb} ${ym} L${xb} ${yb - 8}`;
      o.push(`<g opacity="${focus || !g ? 1 : .6}"><path d="${path}" fill="none" stroke="#fff" stroke-width="${lw + 3}" stroke-linejoin="round"/><path d="${path}" fill="none" stroke="${col}" stroke-width="${focus ? lw + 1.5 : lw}" stroke-linejoin="round"${dash}/><path d="M${xb} ${yb} l-6 -9 l12 0 Z" fill="${col}" stroke="#fff" stroke-width=".8"/></g>`);
      if (g) o.push(EW.wirePill(lk.wire, g, (xa + xb) / 2, ym - 0));
      if (lk.fuse) o.push(`<text x="${(xa + xb) / 2 + 40}" y="${ym + 4}" style="font-size:9.5px;fill:#3d3b34">${esc(lk.fuse)}</text>`);
    }
  });
  nodes.forEach((t, i) => {
    const p = pos(i), parts = t.split('|'), lines = [];
    parts.forEach((s, k) => wrap(s, k === 0 ? 19 : 22).forEach(l => lines.push([l, k === 0])));
    const first = i === 0, last = i === nodes.length - 1, ln = lines.slice(0, 3), sy = p.y + bh / 2 - (ln.length - 1) * 7 + 4;
    o.push(`<rect x="${p.x}" y="${p.y}" width="${bw}" height="${bh}" rx="7" fill="${first ? '#E8F5EC' : last ? '#EFEFEF' : '#fff'}" stroke="${first ? '#1B7F3B' : last ? '#111' : '#1b1a17'}" stroke-width="${first || last ? 2.4 : 1.6}"/>`);
    ln.forEach((l, k) => o.push(`<text x="${p.x + bw / 2}" y="${sy + k * 14}" text-anchor="middle" style="font-size:${l[1] ? 12 : 10.5}px;font-weight:${l[1] ? 700 : 400};fill:${l[1] ? '#1b1a17' : '#5F5E5A'}">${esc(l[0])}</text>`));
    if (first) o.push(`<rect x="${p.x + 8}" y="${p.y - 9}" width="52" height="16" rx="8" fill="#1B7F3B"/><text x="${p.x + 34}" y="${p.y + 3}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#fff;letter-spacing:.4px">POWER</text>`);
    if (last) o.push(`<rect x="${p.x + 8}" y="${p.y - 9}" width="38" height="16" rx="8" fill="#111"/><text x="${p.x + 27}" y="${p.y + 3}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#fff;letter-spacing:.4px">END</text>`);
  });
  return `<svg viewBox="0 0 1070 ${H}" role="img" aria-label="${w.id}: from the power to the end of the wire" style="min-width:820px">${o.join('')}</svg>`;
}

// ---- one view of the run, zoomed to the wire; the shared base of the wall or the ceiling comes from the hidden defs (<use>)
function routeSVG(w, view, ctx) {
  const c = ctx[view], e = EW.endsOf(w), pts = [];
  EW.allIn(w, view).forEach(pl => pl.forEach(p => pts.push([c.X(p[0]), c.Y(p[1])])));
  if (e.start.v === view) pts.push([c.X(e.start.pt[0]), c.Y(e.start.pt[1])]);
  e.ends.filter(x => x.v === view).forEach(x => pts.push([c.X(x.pt[0]), c.Y(x.pt[1])]));
  let x0 = 1e9, y0 = 1e9, x1 = -1e9, y1 = -1e9; pts.forEach(p => { x0 = Math.min(x0, p[0]); y0 = Math.min(y0, p[1]); x1 = Math.max(x1, p[0]); y1 = Math.max(y1, p[1]); });
  const W = 1070, H = c.H, asp = H / W, pad = 80, bw = x1 - x0, bh = y1 - y0;
  let vw = Math.max(bw + 2 * pad, 560), vh = vw * asp; if (bh + 2 * pad > vh) { vh = bh + 2 * pad; vw = vh / asp; }
  if (vw >= W) { vw = W; vh = H; }
  const vx = Math.min(Math.max((x0 + x1) / 2 - vw / 2, 0), W - vw), vy = Math.min(Math.max((y0 + y1) / 2 - vh / 2, 0), H - vh);
  const lines = (w[view] || []).map(pl => EW.wireLine(pl, c.X, c.Y, w.g, w.t)).join('');
  const trace = EW.traceLayer(w, view, c.X, c.Y).replace(/^<g class="wtr"[^>]*>/, '<g>');
  const lab = w.lab && w.lab[view];
  const pill = lab ? EW.wirePill(w.id, w.g, c.X(lab[0]), c.Y(lab[1])) : '';
  return `<svg viewBox="${vx.toFixed(1)} ${vy.toFixed(1)} ${vw.toFixed(1)} ${vh.toFixed(1)}" role="img" aria-label="${w.id} on the ${c.name}" style="min-width:820px">${c.use}${lines}${pill}${trace}</svg>`;
}

const VIEW_NAME = { D: 'Driver side wall', P: 'Passenger side wall', C: 'Ceiling' };
const VIEW_NOTE = { D: 'seen from inside the van, rear doors on the left; inches along the wall from the back mark are the blue numbers', P: 'seen from inside the van, cab on the left, rear doors on the right', C: 'seen from above: driver wall at the top, rear doors on the left' };

function cardsPage(WR, ctx, helpers) {
  const byId = Object.fromEntries(WR.map(w => [w.id, w]));
  const sw = (w, wd) => `<svg width="${wd}" height="14" viewBox="0 0 ${wd} 14" style="display:inline-block;width:${wd}px;max-width:${wd}px;min-width:0;height:14px;vertical-align:-3px"><line x1="3" y1="7" x2="${wd - 3}" y2="7" stroke="${EW.gc(w.g)}" stroke-width="${EW.gw(w.g)}" stroke-linecap="round"${w.t === 'ac' ? ' stroke-dasharray="8 5"' : ''}/></svg>`;
  const index = `<div class="tw"><table><thead><tr><th>#</th><th>AWG</th><th>Wire</th><th>Length</th></tr></thead><tbody>${WR.map(w => `<tr><td><a href="#${w.id.toLowerCase()}"><b class="wid">${w.id}</b></a></td><td style="white-space:nowrap">${sw(w, 40)} <b>${EW.byG[w.g].name}</b></td><td>${esc(w.n.length > 110 ? w.n.slice(0, 108) + '…' : w.n)}</td><td class="num">${w.len >= 10 ? Math.round(w.len) : Math.round(w.len * 10) / 10} ft</td></tr>`).join('')}</tbody></table></div>`;
  const cards = WR.map(w => {
    const e = EW.endsOf(w), views = EW.viewsOf(w);
    const len = w.len >= 10 ? Math.round(w.len) : Math.round(w.len * 10) / 10;
    const ac = ALT_WIRES.has(w.id);
    return `<section class="wcard" id="${w.id.toLowerCase()}">
    <div class="wc-h"><b class="wid">${w.id}</b> ${sw(w, 46)} <b>${EW.byG[w.g].name} AWG</b> · ${w.t === 'ac' ? '120 V' : '12 V or battery'} · about ${len} ft · fuse or breaker: ${esc(w.prot)}</div>
    <h3>${esc(w.n)}</h3>
    <div class="wc-l"><span class="wt-s">START</span>${esc(w.from)}</div>
    <div class="wc-l"><span class="wt-e">END</span>${esc(w.to)}</div>
    <h4><span class="fid">${w.id} A</span>Power to the end of the wire</h4>
    <div class="figwrap">${chainSVG(w, byId)}</div>
    ${ac ? `<p class="kd">${esc(ALT_AC)}</p>` : ''}
    ${views.map((v, vi) => `<h4><span class="fid">${w.id} ${String.fromCharCode(66 + vi)}</span>${VIEW_NAME[v]} <span class="kd">(${VIEW_NOTE[v]})</span></h4><div class="figwrap">${routeSVG(w, v, ctx)}</div>`).join('')}
    <p class="kd">${esc(w.note || '')}${w.tnote ? ' ' + esc(w.tnote) : ''}</p>
    </section>`;
  }).join('');
  return { index, cards };
}
module.exports = { cardsPage, CHAINS };
