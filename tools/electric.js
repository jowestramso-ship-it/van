/* Builds ../electric.html: the electrical and lighting layout.
   Like wallmap.js it reads the plan's own layout from interactive.html in a headless browser and the steel / furring drawing from sides.html
   (diagrams A and D), so the positions follow the plan's sizes. The electrical choices (where each outlet, switch, light, fuse and run goes)
   are the proposal written below as E_*; change them there.
   Run:  node tools/electric.js        (needs playwright + the bundled Chromium; build.sh runs it and skips it if they are missing)
*/
const {chromium} = require(process.env.NODE_PATH + '/playwright');
const fs = require('fs');
const fr = v => { let w = Math.floor(v + 1e-9), r = Math.round((v - w) * 16); if (r === 16){w++;r=0;} let n=r,d=16; while(n&&n%2===0){n/=2;d/=2;} return (n? (w?w+' ':'')+n+'/'+d : ''+w); };
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

// ------------------------------------------------------------------ the proposal (x = inches from the back mark, z = inches up from the floor)
// kinds: out120 = 120 V outlet, usb = 12 V / USB-C socket, sw = switch, lt = light, strip = LED strip (x0..x1 at z), box = a mounted unit, inlet, panel, run = a wire run (vertical x from z0 to z1)
const E_DRIVER = pl => { const tc = (pl.tbl[0] + pl.tbl[1]) / 2, q1 = pl.bedLen / 4, q3 = 3 * pl.bedLen / 4, lz = pl.cabBot - .5; return [
  {k:'box',   n:'Battery, 280 Ah (assumed lithium)',          x0:52, x1:73, z0:0, z1:9.5, note:'where the plan has it, in front of the wheel well; main fuse (Class T, 250 A) within 7 in of its + post'},
  {k:'box',   n:'Power hub board',                             x0:72, x1:74, z0:1, z1:11, note:'a plywood board on the closet’s rear panel, facing the battery: inverter-charger, DC bus bars, shunt, 12 V fuse block, DC-DC charger, AC panel. Needs an access hatch in the couch front, 52 to 74 in'},
  {k:'inlet', n:'Shore power inlet (30 A)',                    x:80, z:21,  note:'through the solid steel band at 19 1/2 to 23 in up (S3), inside the closet’s lower part; 30 A breaker on the hub board'},
  {k:'lt',    n:'Light under the cabinet over the couch, rear', x:q1, z:lz, note:'12 V LED, on the underside of the wall cabinet (bottom at 61 in), a quarter of the way along the couch (74 in); on the lights circuit and the couch switch. Replaces the wall reading lights I had suggested'},
  {k:'lt',    n:'Light under the cabinet over the couch, cab end', x:q3, z:lz, note:'same, three quarters of the way along; wire comes down from inside the cabinet'},
  {k:'lt',    n:'Light over the dinette table',                x:tc, z:lz, note:'12 V LED under the dinette wall cabinet, centered over the table (108 1/2 to 134 1/2); on the lights circuit and the dinette switch'},
  {k:'usb',   n:'USB-C and 12 V socket, couch rear',           x:6,  z:44, note:'above the back cushion (40 in up); 12 V sockets circuit, 14 AWG, 15 A'},
  {k:'out120',n:'Couch outlet (120 V duplex)',                  x:62, z:44, note:'above the back cushion (40 in up); circuit A (GFCI), 12 AWG'},
  {k:'usb',   n:'USB-C and 12 V socket, couch cab end',        x:70, z:44, note:'12 V sockets circuit'},
  {k:'sw',    n:'Switch plate at the rear doors (fan, wet bath light)', x:3,  z:48, note:'2 gang: roof fan and the wet bath light. You did not list this one, but those two need a switch; the ceiling lights are not on it'},
  {k:'sw',    n:'Light switch by the couch',                   x:70, z:50, note:'ceiling lights (one of three points, with the dinette and the sink) and the two reading lights'},
  {k:'sw',    n:'Light switch by the dinette',                  x:106, z:48, note:'ceiling lights (second point) and the entry light over the sliding door'},
  {k:'out120',n:'Outlet over the dinette table (120 V duplex)', x:tc, z:36, note:'on the wall just over the table (its top is at 29 in), in the middle of it, clear of the backrests (38 in); circuit A (GFCI)'},
  {k:'usb',   n:'USB-C and 12 V socket, dinette (cab end)',    x:144,z:42, note:'12 V sockets circuit'},
  {k:'strip', n:'Closet light',                                x0:76,x1:87, z:73, note:'inside the closet, on a door switch'},
  {k:'run',   n:'Riser A: A/C, 12 V and lights feed',          x:73, z0:11, z1:75, note:'up inside the wall behind the planks (4 1/2 in space) to the ceiling: A/C 6 AWG pair in its own loom, plus the 12 V ceiling feed (12 AWG). Grommet where it crosses the top steel'},
  {k:'run',   n:'Cab charge cable (DC-DC input)',              x:70, z0:0, z1:1,  note:'4 AWG from the starter battery fuse (60 A) under the van along the driver side frame to a sealed floor grommet next to the battery'},
]; };
const E_PASS = [
  {k:'out120',n:'Fridge outlet, behind the fridge (120 V)',    x:47, z:6,  note:'on the wall behind the fridge platform (the fridge stands on a platform 8 1/4 up); circuit C, the fridge alone'},
  {k:'out120',n:'Microwave outlet (120 V, its own breaker)',    x:60, z:64, note:'a fifth outlet you did not list: the microwave (1500 W) needs its own, on the wall just cab-side of it (36 to 58); circuit B. Drop it if the microwave plugs in elsewhere'},
  {k:'panel', n:'Control panel (battery monitor, pump switch, tank levels)', x:66, z:50, note:'12 V, small 18 AWG, 3 A'},
  {k:'out120',n:'Outlet under the TV (120 V)',                  x:96, z:52.5, note:'on the wall strip under the TV (its bottom is at 54), above the dish towel hook (98 1/2, 50 up): check the plug clears the towel. Near the sink, so circuit A (GFCI)'},
  {k:'box',   n:'Hot water heater feed (120 V, 20 A, circuit D)', x0:85, x1:87, z0:18, z1:24, note:'junction box beside the hot water tank (87 to 101); 12 AWG, its own breaker; heater is 1440 W'},
  {k:'box',   n:'Water pump (12 V, under the sink)',           x0:119, x1:122, z0:12, z1:20, note:'on the sink cabinet’s cab-side end panel, above the fresh tank (top at 10 in), 14 AWG, 10 A; service hatch'},
  {k:'strip', n:'Toe-kick LED strip',                          x0:58, x1:103, z:2, note:'night light along the base of the counter; lights circuit'},
  {k:'strip', n:'Jar nook LED strip',                          x0:77, x1:92, z:52.5, note:'inside the top of the jar nook'},
  {k:'strip', n:'Shower nook LED strip (wet rated)',           x0:14, x1:28, z:52.5, note:'IP65, fed by the wet bath light circuit'},
  {k:'sw',    n:'Light switch by the sink',                    x:123, z:34, note:'ceiling lights (third point), toe-kick strip and the nook strips; on the cab-side end panel of the sink cabinet, facing the entry, under the countertop (38) and over the fold-out table hinge (29). The wall strip beside the sink is too full (hook, TV)'},
  {k:'strip', n:'Entry light over the sliding door',           x0:106, x1:152, z:69, note:'on the dinette switch'},
  {k:'run',   n:'Riser B: 120 V circuits and 12 V branches',   x:73, z0:8, z1:75, note:'down inside the wall behind the planks from the ceiling: 120 V in flexible conduit (12 AWG), 12 V branches (pump, control panel) in a separate loom; branches go sideways behind the planks through notches in the furring'},
];

// ------------------------------------------------------------------ reading the plan
async function readPlan(page) {
  return page.evaluate(() => {
    const P = L.P, f = v => Math.round(v * 100) / 100;
    return {
      P: { battAh: P.battAh, acEcoA: P.acEcoA, acEcoH: P.acEcoH, acTurboA: P.acTurboA, fanLowW: P.fanLowW, fanHighW: P.fanHighW, fanHighH: P.fanHighH, heaterW: P.heaterW, hotGal: P.hotGal || 4,
        vanW: P.vanW, ceilLen: P.ceilLen, lightD: P.lightD, cab: P.cab, ribW: P.ribW, ribDepth: P.ribDepth },
      lights: L.lights.map(l => ({ x: f(l.x), y: f(l.y) })),
      chanY: L.chanY.map(f),
      fan: { x: L.fan.x, y: L.fan.y, w: L.fan.w, u: L.fan.u },
      ac: { x: L.ac.x, y: L.ac.y, w: L.ac.w, u: L.ac.u },
      ribBands: L.ribBands,
      batt: L.batt, tbl: L.tbl, bedLen: P.bedLen, tableH: P.tableH, cabBot: P.cabBot,
    };
  });
}
async function grabItems(page) {            // the furniture outlines (same positions as wall-map)
  return page.evaluate(() => {
    const P = L.P, ch = P.counterH, f = v => Math.round(v * 100) / 100, a = (x0, x1, z0, z1) => ({ x0: f(x0), x1: f(x1), z0: f(z0), z1: f(z1) });
    const D = [a(0, P.bedLen, 0, P.platform + P.mattress + P.bedBack), a(42, 76, 0, 7.5), a(L.c0, L.c1, 0, L.ceilF), a(L.bA[0], L.bA[1], 0, P.seatH), a(L.bB[0], L.bB[1], 0, P.seatH)];
    if (L.tableLen > 0) D.push(a(L.tbl[0], L.tbl[1], P.tableH - 1.5, P.tableH));
    L.cabs.forEach(c => D.push(a(c[0], c[1], P.cabBot, L.ceilF)));
    const nkx = Math.min(29.75, P.panW - 6.25), nk0 = nkx - P.snookLen;
    const PS = [a(0, P.panW, 0, L.ceilF), a(nk0, nkx, P.snookTop - P.snookH, P.snookTop), a(L.fr[0], L.fr[1], 8.25, 8.25 + P.fridgeH), a(L.microX[0], L.microX[1], L.microZ[0], L.microZ[1]),
      a(L.cabS, L.sinkE, 0, ch), a(76.5, 103.5, ch + 16, ch + 31.4), a(NK(P)[0], NK(P)[1], ch, ch + P.nookH), a(L.tankX[0], L.tankX[1], P.tankLift, P.tankLift + P.tankH),
      a(L.hotX[0], L.hotX[1], P.hotShelf, P.hotShelf + P.hotH), a(42, 76, 0, 7.5), a(P.doorX, P.doorX + P.slideW, 0, P.slideH)];
    return { D, P: PS };
  });
}
async function grabBase(page2, idx) {
  return page2.evaluate((idx) => {
    const svg = [...document.querySelectorAll('svg[viewBox="0 0 1070 636"]')][idx].cloneNode(true);
    svg.querySelectorAll('text').forEach(t => { if (/^(Driver side wall:|Passenger side, seen)/.test(t.textContent.trim())) t.remove(); });
    const lg = [...document.querySelectorAll('p.legend')][idx === 0 ? 0 : 1] || document.querySelector('p.legend');
    return { inner: svg.innerHTML, legend: lg ? lg.outerHTML : '' };
  }, idx);
}

// ------------------------------------------------------------------ drawing
const INK = '#1b1a17', C120 = '#B3261E', C12 = '#185FA5', CAC = '#B45309', CLT = '#B8860B';
function symbol(e, X, Y) {
  const o = [], r = 7;
  if (e.k === 'out120') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${C120}" stroke-width="1.8"/><line x1="${x-3}" y1="${y-3}" x2="${x-3}" y2="${y+1}" stroke="${C120}" stroke-width="1.6"/><line x1="${x+3}" y1="${y-3}" x2="${x+3}" y2="${y+1}" stroke="${C120}" stroke-width="1.6"/>`); return [o.join(''), x, y]; }
  if (e.k === 'usb') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${C12}" stroke-width="1.8"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">12</text>`); return [o.join(''), x, y]; }
  if (e.k === 'sw') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-6.5}" y="${y-6.5}" width="13" height="13" rx="2" fill="#fff" stroke="${INK}" stroke-width="1.8"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${INK}">S</text>`); return [o.join(''), x, y]; }
  if (e.k === 'lt') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#FFD84A" stroke="${CLT}" stroke-width="1.8"/>`); return [o.join(''), x, y]; }
  if (e.k === 'inlet') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-8}" y="${y-8}" width="16" height="16" rx="3" fill="#FFF1D6" stroke="${CAC}" stroke-width="2"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${CAC}">IN</text>`); return [o.join(''), x, y]; }
  if (e.k === 'panel') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-9}" y="${y-7}" width="18" height="14" rx="2" fill="#fff" stroke="${C12}" stroke-width="1.8"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">M</text>`); return [o.join(''), x, y]; }
  if (e.k === 'strip') { const xa = X(e.x0), xb = X(e.x1), y = Y(e.z), x = Math.min(xa, xb), w = Math.abs(xb - xa); o.push(`<rect x="${x}" y="${y-2.5}" width="${w}" height="5" rx="2.5" fill="#FFD84A" stroke="${CLT}" stroke-width="1.2"/>`); return [o.join(''), x + w / 2, y]; }
  if (e.k === 'box') { const xa = X(e.x0), xb = X(e.x1), x = Math.min(xa, xb), w = Math.max(10, Math.abs(xb - xa)), y0 = Y(e.z1), h = 6 * (e.z1 - e.z0); o.push(`<rect x="${x}" y="${y0}" width="${w}" height="${h}" rx="2" fill="#FFF1D6" fill-opacity=".75" stroke="${CAC}" stroke-width="2"/>`); return [o.join(''), x + w / 2, y0 + h / 2]; }
  if (e.k === 'run') { const x = X(e.x); o.push(`<line x1="${x}" y1="${Y(e.z0)}" x2="${x}" y2="${Y(e.z1)}" stroke="${C12}" stroke-width="3" stroke-dasharray="7 4" opacity=".85"/><line x1="${x+4}" y1="${Y(e.z0)}" x2="${x+4}" y2="${Y(e.z1)}" stroke="${C120}" stroke-width="3" stroke-dasharray="7 4" opacity=".85"/>`); return [o.join(''), x + 2, Y((e.z0 + e.z1) / 2)]; }
  return ['', 0, 0];
}
function wallSVG(list, side, base, furn) {
  const flip = side === 'P', X = x => +(flip ? 1020 - 6 * x : 50 + 6 * x).toFixed(1), Y = z => +(544 - 6 * z).toFixed(1);
  const o = [], placed = [];
  furn.forEach(it => { const xa = X(it.x0), xb = X(it.x1); o.push(`<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="none" stroke="${INK}" stroke-opacity=".28" stroke-width="1.2" stroke-dasharray="4 3"/>`); });
  const rows = list.map((e, i) => {
    e.id = 'E' + side + (i + 1);
    const [g, cx, cy] = symbol(e, X, Y); o.push(g);
    let bx = cx + (e.k === 'strip' || e.k === 'box' || e.k === 'run' ? 0 : 13), by = cy - (e.k === 'strip' ? 13 : e.k === 'run' ? 0 : 13);
    if (e.k === 'strip') { bx = cx; }
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0] - bx, q[1] - by) < 24); t++) by -= 14;
    placed.push([bx, by]);
    o.push(`<rect x="${bx-14}" y="${by-8}" width="28" height="16" rx="8" fill="#fff" fill-opacity=".95" stroke="${C120}" stroke-width="1.3"/><text x="${bx}" y="${by+3.8}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${C120}">${e.id}</text>`);
    const where = e.k === 'strip' ? `${fr(e.x0)} to ${fr(e.x1)}, at ${fr(e.z)} up` : e.k === 'box' ? `${fr(e.x0)} to ${fr(e.x1)}, ${fr(e.z0)} to ${fr(e.z1)} up` : e.k === 'run' ? `at ${fr(e.x)}, ${fr(e.z0)} to ${fr(e.z1)} up` : `${fr(e.x)} in, ${fr(e.z)} up`;
    return `<tr><td><b class="id">${e.id}</b></td><td>${esc(e.n)}</td><td>${where}</td><td class="kd">${esc(e.note)}</td></tr>`;
  });
  const svg = `<svg viewBox="0 0 1070 636" role="img" aria-label="${flip ? 'Passenger' : 'Driver'} wall: steel, furring strips, furniture outlines and the electrical items">${base.inner}<g id="elec${side}">${o.join('')}</g></svg>`;
  return { svg, table: `<div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>`, legend: base.legend };
}

function ceilingSVG(d) {
  const S = 6, X = x => 50 + S * x, Y = y => 56 + S * y, W = 1070, H = 56 + S * 68 + 120;
  const o = [`<rect x="${X(0)}" y="${Y(0)}" width="${S * 160}" height="${S * 68}" fill="#fff" stroke="#5F5E5A" stroke-width="1.6"/>`];
  d.ribBands.forEach(b => o.push(`<rect x="${X(b[0])}" y="${Y(0)}" width="${S * (b[1] - b[0])}" height="${S * 68}" fill="#9aa3ad" fill-opacity=".45" stroke="#5F5E5A" stroke-width=".8"/>`));
  for (let x = 0; x <= 160; x += 20) o.push(`<text x="${X(x)}" y="${Y(68) + 16}" text-anchor="middle" style="font-size:10px;fill:#185FA5;font-weight:700">${x}</text>`);
  o.push(`<text x="${X(80)}" y="${Y(68) + 32}" text-anchor="middle" style="font-size:12px;fill:#5F5E5A">inches from the rear-door edge (add 6 to the wall maps’ numbers)</text>`);
  o.push(`<text x="${X(0)}" y="${Y(0) - 8}" style="font-size:12px;fill:#5F5E5A">driver wall (top)  ← rear doors</text><text x="${X(160)}" y="${Y(0) - 8}" text-anchor="end" style="font-size:12px;fill:#5F5E5A">cab →</text><text x="${X(0)}" y="${Y(68) + 48}" style="font-size:12px;fill:#5F5E5A">passenger wall (bottom)</text>`);
  // roof units: unit footprints dashed, cutouts solid; the A/C unit sits 3 1/8 forward of its opening
  const acOff = 3.125, fan = d.fan, ac = d.ac;
  o.push(`<rect x="${X(fan.x - fan.u / 2)}" y="${Y(fan.y - fan.u / 2)}" width="${S * fan.u}" height="${S * fan.u}" fill="#185FA5" fill-opacity=".06" stroke="#185FA5" stroke-width="1.2" stroke-dasharray="6 3"/><rect x="${X(fan.x - fan.w / 2)}" y="${Y(fan.y - fan.w / 2)}" width="${S * fan.w}" height="${S * fan.w}" fill="#fff" stroke="${INK}" stroke-width="1.8"/><text x="${X(fan.x)}" y="${Y(fan.y) + 4}" text-anchor="middle" style="font-size:12px;font-weight:700">FAN</text>`);
  o.push(`<rect x="${X(ac.x + acOff - ac.u / 2)}" y="${Y(ac.y - ac.u / 2)}" width="${S * ac.u}" height="${S * ac.u}" fill="#185FA5" fill-opacity=".06" stroke="#185FA5" stroke-width="1.2" stroke-dasharray="6 3"/><rect x="${X(ac.x - ac.w / 2)}" y="${Y(ac.y - ac.w / 2)}" width="${S * ac.w}" height="${S * ac.w}" fill="#fff" stroke="${INK}" stroke-width="1.8"/><text x="${X(ac.x)}" y="${Y(ac.y) + 4}" text-anchor="middle" style="font-size:12px;font-weight:700">A/C</text>`);
  // wire runs
  const RX = 79;                                   // both risers stand at 73 on the wall maps = 79 from the rear-door edge, in the bay between the ribs at 61 and 97
  const line = (pts, col, w, dash) => `<polyline points="${pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' ')}" fill="none" stroke="${col}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} stroke-linejoin="round"/>`;
  const acY = ac.y - ac.w / 2, fanY = fan.y - fan.w / 2;
  o.push(line([[RX - 1.2, 0], [RX - 1.2, 68]], C12, 3, '8 4'));                        // 12 V trunk across
  o.push(line([[RX + 1.2, 0], [RX + 1.2, 68]], C120, 3, '8 4'));                       // 120 V across
  o.push(line([[RX, 0], [RX, acY], [ac.x, acY]], CAC, 4.5));                           // A/C feed to the notch in the frame's driver-side wall
  o.push(line([[RX - 2.4, 20.5], [fan.x, 20.5], [fan.x, fanY]], C12, 2.4));            // fan feed
  d.chanY.forEach(y => o.push(line([[2, y], [158, y]], CLT, 2.2, '2 3')));             // light rows
  o.push(`<rect x="${X(RX) - 11}" y="${Y(34) - 8}" width="22" height="16" rx="3" fill="#FFF1D6" stroke="${CAC}" stroke-width="2"/><text x="${X(RX)}" y="${Y(34) + 4}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${CAC}">JB</text>`);
  // lights
  d.lights.forEach((l, i) => { o.push(`<circle cx="${X(l.x)}" cy="${Y(l.y)}" r="${Math.max(6, S * d.P.lightD / 2)}" fill="#FFD84A" stroke="${CLT}" stroke-width="1.8"/>`); });
  // where the risers meet the walls
  o.push(`<text x="${X(RX) + 16}" y="${Y(0) + 14}" style="font-size:11px;font-weight:700;fill:${INK}">riser A (A/C, 12 V) at ${RX}</text><text x="${X(RX) + 16}" y="${Y(68) - 8}" style="font-size:11px;font-weight:700;fill:${INK}">riser B (120 V, branches) at ${RX}</text>`);
  // legend
  const ly = Y(68) + 66;
  const leg = [[C12, 'dashed blue: 12 V trunk (fuse block feed, 12 AWG)', '8 4', 3], [C120, 'dashed red: 120 V circuits in flexible conduit (12 AWG)', '8 4', 3], [CAC, 'solid orange: A/C feed, 6 AWG, 100 A fuse at the battery', null, 4.5], [CLT, 'dotted yellow: light rows (16 AWG, one slat each)', '2 3', 2.2]];
  leg.forEach((l, i) => o.push(`<line x1="${X(0)}" y1="${ly + i * 16}" x2="${X(0) + 34}" y2="${ly + i * 16}" stroke="${l[0]}" stroke-width="${l[3]}"${l[2] ? ` stroke-dasharray="${l[2]}"` : ''}/><text x="${X(0) + 42}" y="${ly + i * 16 + 4}" style="font-size:12px;fill:${INK}">${l[1]}</text>`));
  o.push(`<text x="${X(86)}" y="${ly + 4}" style="font-size:12px;fill:${INK}">JB = ceiling junction box (12 V fuse block feed splits here)</text><text x="${X(86)}" y="${ly + 20}" style="font-size:12px;fill:${INK}">grey bands = ribs; dashed squares = the unit footprints on the roof</text><text x="${X(86)}" y="${ly + 36}" style="font-size:12px;fill:${INK}">yellow circles = ceiling lights (positions from the plan)</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ceiling seen from above: lights, fan, A/C, junction box and wire runs"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

function oneLineSVG() {
  const W = 1070, H = 640, o = [];
  const box = (x, y, w, h, t1, t2, col) => { o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff" stroke="${col || INK}" stroke-width="1.8"/><text x="${x + w / 2}" y="${y + (t2 ? h / 2 - 3 : h / 2 + 4)}" text-anchor="middle" style="font-size:12.5px;font-weight:700;fill:${INK}">${esc(t1)}</text>`); if (t2) o.push(`<text x="${x + w / 2}" y="${y + h / 2 + 12}" text-anchor="middle" style="font-size:11px;fill:#5F5E5A">${esc(t2)}</text>`); };
  const ln = (x1, y1, x2, y2, col, lab, lx, ly, w) => { o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w || 2.4}"/>`); if (lab) o.push(`<text x="${lx}" y="${ly}" text-anchor="middle" style="font-size:11px;fill:${INK}">${esc(lab)}</text>`); };
  // sources (left)
  box(20, 40, 190, 52, 'Shore power inlet', '30 A, 120 V', CAC);
  box(20, 160, 190, 56, 'Alternator', 'starter battery fuse 60 A', INK);
  box(20, 250, 190, 52, 'DC-DC charger', '40 to 60 A, on the hub board', INK);
  ln(115, 92, 115, 124, C120, '', 0, 0); ln(115, 124, 270, 124, C120, '30 A breaker', 190, 118);
  ln(115, 216, 115, 250, C12, '', 0, 0); o.push(`<text x="122" y="238" style="font-size:11px;fill:${INK}">4 AWG, about 15 ft</text>`);
  // inverter-charger
  box(270, 100, 200, 74, 'Inverter-charger 2000 W', 'pure sine, 30 A pass-through', CAC);
  // battery + bus
  box(270, 330, 190, 66, 'Battery 280 Ah, 12.8 V', 'lithium assumed (3.6 kWh)', INK);
  ln(115, 302, 115, 362, C12, '', 0, 0); ln(115, 362, 270, 362, C12, '4 AWG', 190, 356);
  ln(365, 330, 365, 300, C12, 'Class T 250 A, 2/0 AWG', 440, 322, 4); 
  box(270, 240, 190, 54, '+ bus bar and shunt (500 A)', 'near the battery', INK);
  ln(365, 240, 365, 174, C12, '2/0 AWG, 250 A fuse', 440, 214, 4);
  // 12 V branches (right of the bus)
  const br = [['A/C 12 V, up to 58 A', '6 AWG pair, 100 A fuse', CAC], ['Fuse block: ceiling lights, strips, reading lights', '16 AWG, 10 A', CLT], ['Roof fan, up to 2.7 A', '14 AWG, 5 A', C12], ['Water pump, 7 A (under the sink)', '14 AWG, 10 A', C12], ['12 V and USB-C sockets', '14 AWG, 15 A', C12], ['Control panel and shunt display', '18 AWG, 3 A', C12]];
  br.forEach((b, i) => { const y = 214 + i * 56; ln(460, 267, 540, 267, C12, '', 0, 0); ln(540, 267, 540, y + 20, C12, '', 0, 0); ln(540, y + 20, 600, y + 20, b[2], '', 0, 0, 2.8); box(600, y, 330, 40, b[0], b[1], b[2]); });
  o.push(`<text x="600" y="198" style="font-size:12px;font-weight:700;fill:${C12}">12 V DC circuits (blade fuse block, except the A/C)</text>`);
  // AC side
  ln(460, 137, 540, 137, C120, '', 0, 0); ln(540, 137, 540, 80, C120, '', 0, 0); ln(540, 80, 600, 80, C120, '', 0, 0);
  box(600, 56, 150, 48, 'AC panel', '30 A main, GFCI', C120);
  o.push(`<text x="540" y="46" style="font-size:12px;font-weight:700;fill:${C120}">120 V AC circuits</text>`);
  [['A  counter outlets, GFCI', '15 A, 12 AWG'], ['B  microwave, its own', '15 A, 12 AWG'], ['C  fridge, TV, dinette outlets', '15 A, 12 AWG'], ['D  water heater 1440 W', '20 A, 12 AWG']].forEach((c, i) => { const y = 16 + i * 0; });
  const ac = [['A  couch, dinette, under-TV outlets (GFCI)', '15 A, 12 AWG'], ['B  microwave, its own breaker', '15 A, 12 AWG'], ['C  fridge, its own breaker', '15 A, 12 AWG'], ['D  water heater, 1440 W', '20 A, 12 AWG']];
  ac.forEach((c, i) => { const x = 770, y = 12 + i * 34; ln(750, 80, 760, 80, C120, '', 0, 0); ln(760, 80, 760, y + 14, C120, '', 0, 0); ln(760, y + 14, x, y + 14, C120, '', 0, 0); o.push(`<rect x="${x}" y="${y}" width="280" height="28" rx="5" fill="#fff" stroke="${C120}" stroke-width="1.5"/><text x="${x + 8}" y="${y + 13}" style="font-size:11.5px;font-weight:700;fill:${INK}">${esc(c[0])}</text><text x="${x + 8}" y="${y + 24}" style="font-size:10.5px;fill:#5F5E5A">${esc(c[1])}</text>`); });
  o.push(`<text x="20" y="${H - 54}" style="font-size:11.5px;fill:#5F5E5A">Fuses sit within 7 in of the battery or bus (Class T for the inverter, 100 A for the A/C). Wire sizes are for the short runs shown (battery to inverter under 3 ft, A/C about 12 ft);</text><text x="20" y="${H - 38}" style="font-size:11.5px;fill:#5F5E5A">the A/C size comes from a related OutEquipPro model. Follow your inverter’s and the A/C maker’s manuals where they differ.</text><text x="20" y="${H - 22}" style="font-size:11.5px;fill:#5F5E5A">One neutral-to-ground bond only, inside the inverter-charger (its manual says how). Have the 120 V side inspected before use.</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="One-line diagram: shore power and alternator charging, battery, inverter-charger, fuses and circuits"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

function loadTable(d) {
  const P = d.P, Vn = 12.8, ahToKwh = a => a * Vn / 1000, kwhGal = 8.34 * 80 / 3412;
  const batt = P.battAh * Vn / 1000;
  const L = [
    ['Air conditioner, eco', `${fr(P.acEcoA)} A for ${fr(P.acEcoH)} h`, P.acEcoA * P.acEcoH, 'figures from the listing and reviews'],
    ['Fridge, 120 V', 'about 100 W while it runs, assumed 45% of the day', 0.1 * 24 * 0.45 / Vn * 1000, 'your figure of 100 W; the 45% is my assumption for a warm van'],
    ['Inverter idling, on all day for the fridge', 'about 20 W for 24 h', 0.02 * 24 / Vn * 1000, 'assumed; some inverters have a search mode that cuts this to a few watts, but check it still wakes for the fridge'],
    ['Ceiling lights, strips, reading lights', 'about 4 A for 4 h', 16, 'assumed LEDs, about 50 W together'],
    ['Roof fan', `${fr(P.fanLowW)} W low, ${fr(P.fanHighW)} W high for ${fr(P.fanHighH)} h`, ((P.fanLowW * (24 - P.fanHighH) + P.fanHighW * P.fanHighH) / 12), 'from the plan'],
    ['Water pump and USB charging', 'about 17 Ah', 17, 'assumed'],
    ['Hot water heater, one full heating', `about ${Math.round(P.hotGal * 10) / 10} gal heated by 80 F`, kwhGal * P.hotGal / .9 * 1000 / Vn, 'from the plan’s formula, 90% efficient'],
    ['Microwave', '1500 W for 12 min', 1500 * .2 / Vn / .9, 'assumed'],
    ['TV', '60 W for 3 h', 60 * 3 / Vn / .9, 'assumed']];
  const tot = L.reduce((s, r) => s + r[2], 0);
  const rows = L.map(r => `<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td class="num">${Math.round(r[2])} Ah</td><td class="num">${ahToKwh(r[2]).toFixed(2)} kWh</td><td class="kd">${esc(r[3])}</td></tr>`).join('');
  return `<div class="tw"><table><thead><tr><th>Load</th><th>Use</th><th>Per day</th><th></th><th>Basis</th></tr></thead><tbody>${rows}<tr class="tot"><td><b>A hot day, everything</b></td><td></td><td class="num"><b>${Math.round(tot)} Ah</b></td><td class="num"><b>${ahToKwh(tot).toFixed(2)} kWh</b></td><td class="kd">the battery holds ${P.battAh} Ah, about ${batt.toFixed(1)} kWh</td></tr></tbody></table></div>
  <p class="lead">That is ${(tot / P.battAh).toFixed(1)} times the battery on a hot day with the A/C on for ${fr(P.acEcoH)} hours, so it needs refilling every day: driving through the alternator charger (50 A is about 640 W, so 2 hours adds about 1.3 kWh) or shore power (60 A charger, about 770 W). The fridge and the inverter idling are about a quarter of that total: a 12 V fridge would cut it, because the inverter could be switched off. These are estimates to size the system, not a measurement.</p>`;
}

(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport: {width: 1400, height: 1000}});
  await page.goto('file://' + __dirname + '/../interactive.html'); await page.waitForTimeout(700);
  const plan = await readPlan(page), furn = await grabItems(page);
  const page2 = await b.newPage({viewport: {width: 1400, height: 1000}});
  await page2.goto('file://' + __dirname + '/../sides.html'); await page2.waitForTimeout(500);
  const baseA = await grabBase(page2, 0), baseD = await grabBase(page2, 2);
  const css = await page2.evaluate(() => [...document.querySelectorAll('style')].map(s => s.textContent).join('\n'));
  await b.close();
  const Dw = wallSVG(E_DRIVER(plan), 'D', baseA, furn.D), Pw = wallSVG(E_PASS, 'P', baseD, furn.P);

  const style = css + `
  body { max-width: none; margin: 0; padding: 0; background: #fff; color: #2C2C2A; color-scheme: light; }
  .wrap { max-width: 1180px; margin: 0 auto; padding-block: 16px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
  h1 { font-size: 24px; margin: 6px 0 2px; } h2 { font-size: 19px; margin: 28px 0 6px; } h3 { font-size: 16px; margin: 14px 0 4px; }
  .lead { color: #5F5E5A; margin: 4px 0 10px; font-size: 15px; }
  .figwrap { overflow-x: auto; border: 1px solid #D3D1C7; border-radius: 10px; padding: 6px; margin: 6px 0; background: #fff; }
  .figwrap svg { min-width: 820px; }
  .tog { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 14px; margin: 6px 0; }
  .tw { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; font-size: 14px; margin: 6px 0 8px; }
  th, td { border-bottom: 1px solid #D3D1C7; padding: 5px 8px; text-align: left; vertical-align: top; }
  th { color: #5F5E5A; font-weight: 600; } td.num { white-space: nowrap; text-align: right; } tr.tot td { border-top: 2px solid #5F5E5A; }
  b.id { color: ${C120}; white-space: nowrap; } .kd { color: #5F5E5A; }
  .note { background: #FAF9F5; border: 1px solid #D3D1C7; border-radius: 10px; padding: 10px 14px; color: #3d3b34; font-size: 14px; margin: 0 0 14px; }
  .note ul { margin: 4px 0 0 18px; padding: 0; } .note li { font-size: 14px; line-height: 1.5; }
  a { color: #185FA5; }`;
  const tog = (id, furr, label) => `<div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('${furr}').style.display=this.checked?'':'none'"> Show the furring strips and dots</label><label><input type="checkbox" checked onchange="document.getElementById('${id}').style.display=this.checked?'':'none'"> ${label}</label></div>`;
  const key = `<p class="legend"><span><svg width="16" height="16" viewBox="0 0 16 16" style="display:inline;vertical-align:-3px;width:16px;min-width:0"><circle cx="8" cy="8" r="6.5" fill="#fff" stroke="${C120}" stroke-width="1.8"/></svg> 120 V outlet</span><span><svg width="16" height="16" viewBox="0 0 16 16" style="display:inline;vertical-align:-3px;width:16px;min-width:0"><circle cx="8" cy="8" r="6.5" fill="#fff" stroke="${C12}" stroke-width="1.8"/></svg> 12 V / USB-C socket</span><span>S = switch plate</span><span>M = control panel</span><span>IN = shore inlet</span><span style="color:#B8860B">yellow = lights and LED strips</span><span>orange boxes = mounted units</span><span>dashed boxes = furniture (for reference)</span><span style="color:${C12}">blue dashed</span> / <span style="color:${C120}">red dashed</span> = 12 V / 120 V runs</p>`;
  const body = `<div class="wrap">
  <h1>Electrical and lighting layout</h1>
  <p class="lead">A proposal for where the electrics go, drawn on the same steel and furring strips as the wall marking map, with the furniture outlined for reference. Positions are inches from the back mark (0 is 6 in in from the rear-door edge) and up from the floor; the ceiling plan uses inches from the rear-door edge. The steel and strips are the measured drawing; the electrical items are my proposal, so check each one against the real wall and tell me what to move.</p>
  <div class="note"><b>What you chose:</b> a 2000 W inverter, charging from the alternator and from shore power (no solar), a 120 V fridge, and the water pump under the sink. <b>What I assumed (tell me if wrong):</b>
  <ul><li>The battery is lithium, 280 Ah at 12.8 V (about 3.6 kWh), where the plan has it under the couch, 52 to 73 in.</li>
  <li>A combined inverter-charger with at least a 30 A pass-through, so shore power both runs the 120 V loads and charges the battery.</li>
  <li>A 40 to 60 A DC-DC charger from the alternator, 4 AWG from the starter battery.</li>
  <li><b>Light switches:</b> by the couch, the dinette and the sink, as you asked. They all control the ceiling lights from three places, which needs momentary push-buttons into a 12 V dimming controller (a lighting module with several button inputs), not ordinary 3 way switches. I kept a small 2 gang plate at the rear doors only for the roof fan and the wet bath light.</li>
  <li><b>Under-cabinet lights:</b> two over the couch (a quarter and three quarters along it) and one centered over the dinette table, all on the underside of the wall cabinets. They replace the under-cabinet LED strips and the wall reading lights I had first suggested.</li>
  <li><b>Outlets:</b> the four 120 V outlets you asked for (couch, over the middle of the dinette table, under the TV, behind the fridge), plus one for the microwave, which cannot share a circuit with them. Everything else is 12 V or USB-C.</li>
  <li>The hot water heater (1440 W) and the microwave (about 1500 W) must not run together: that is more than a 2000 W inverter can supply.</li>
  <li>All 120 V work is for an electrician to check; I give layout and sizes, not a code review.</li></ul></div>
  <h2>1. One-line diagram</h2>
  <div class="figwrap">${oneLineSVG()}</div>
  <h2>2. Driver side wall</h2>
  ${tog('elecD', 'furr', 'Show the electrical items')}
  <div class="figwrap">${Dw.svg}</div>
  ${key}${Dw.table}
  <h2>3. Passenger side wall</h2>
  ${tog('elecP', 'furrP', 'Show the electrical items')}
  <div class="figwrap">${Pw.svg}</div>
  ${key}${Pw.table}
  <h2>4. Ceiling: lights, fan, A/C and the wire runs</h2>
  <p class="lead">Six lights in two rows (positions from the plan), each row on its own slat. Risers A and B stand at 79 in from the rear-door edge (73 on the wall maps), in the bay between the ribs at 61 and 97. Every rib the cables cross needs a grommeted hole: use any factory holes first, and keep to the web of the rib, not the flange.</p>
  <div class="figwrap">${ceilingSVG(plan)}</div>
  <h2>5. What it adds up to</h2>
  ${loadTable(plan)}
  <h2>6. Order of work</h2>
  <div class="note"><ul>
  <li>Before the walls and ceiling are covered: run the risers, the ceiling trunk and every branch, with grommets in all steel and the 12 V and 120 V in separate looms (at least 2 in apart, crossing at right angles). This is the rough-in step of the build order.</li>
  <li>With the furring strips: fix the electrical boxes to blocking between the strips, and add the blocking behind the hub board, the switch plates and the outlets before the planks go on.</li>
  <li>Last: the hub board, fuses and inverter-charger, the lights and the plates, after the covering is up.</li>
  <li>Test every circuit with a meter before you connect the battery, and test the GFCI outlets with the button.</li></ul></div>
  <p class="lead" style="margin-top:14px"><a href="interactive.html">Back to the interactive plan</a> &middot; <a href="wall-map.html">Wall marking map</a></p>
  </div>`;
  const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Electrical layout</title><style>${style}</style></head><body>${body}</body></html>`;
  fs.writeFileSync(__dirname + '/../electric.html', doc);
  if (!process.env.SC) return console.log('electric.html', doc.length);
  fs.mkdirSync(process.env.SC + '/elec', {recursive: true});
  const frag = `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Electrical Layout</title>\n<style>${style}</style>\n${body.replace('<a href="interactive.html">', '<a href="https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs" target="_blank" rel="noopener">').replace('<a href="wall-map.html">', '<a href="https://claude.ai/artifact/1quE178yLUJmgmSuhm626H" target="_blank" rel="noopener">')}\n`;
  fs.writeFileSync(process.env.SC + '/elec/index.html', frag);
  console.log('electric.html', doc.length, 'driver', E_DRIVER(plan).length, 'pass', E_PASS.length);
})();
