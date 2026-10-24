/* Builds ../wall-map.html: a to-scale, transparent map of each wall for marking.
   It drives interactive.html in a headless browser so the positions come from the
   plan's own layout (single source of truth), then renders a clean marking map.
   Run:  node tools/wallmap.js        (needs playwright + the bundled Chromium)
*/
const {chromium} = require(process.env.NODE_PATH + '/playwright');
const fs = require('fs');

const fr = v => { let w = Math.floor(v + 1e-9), r = Math.round((v - w) * 16); if (r === 16){w++;r=0;} let n=r,d=16; while(n&&n%2===0){n/=2;d/=2;} return (n? (w?w+' ':'')+n+'/'+d : ''+w); };
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

// category -> colour (token names resolved in CSS)
const CAT = [
  [/wall cabinet|closet|counter cabinet|sink cabinet|drawer|shelf board|board/i, 'c1'],
  [/couch|cushion|bench|dinette|fold-out|foot ledge/i, 'c2'],
  [/tank|jug|drain|paper towel|trash/i, 'c3'],
  [/fridge|microwave|\btv\b|nook|jar/i, 'c4'],
  [/wheel well|battery|sliding door|wet bath|hook|lawn chair/i, 'c5'],
];
const colorOf = n => (CAT.find(c => c[0].test(n)) || [,'c6'])[1];

async function grab(page, side) {
  // every item comes straight from the plan's layout L (same numbers the interactive page draws)
  return page.evaluate((side) => {
    const P = L.P, ch = P.counterH, f = v => Math.round(v * 100) / 100, items = [];
    const add = (name, x0, x1, z0, z1, dims, zv) => items.push({ name, dims: dims || '', x0: f(x0), x1: f(x1), z0: f(z0), z1: f(z1), zv: zv == null ? null : f(zv) });
    const F = fmt;
    if (side === 'driver') {
      add('Couch base', 0, P.bedLen, 0, P.platform, `${F(P.bedLen)} long x ${F(P.bedD)} deep`);
      add('Seat cushion', 0, P.bedLen, P.platform, P.platform + P.mattress, `top at ${F(P.platform + P.mattress)}`);
      add('Back cushion, upright', 0, P.bedLen, P.platform + P.mattress, P.platform + P.mattress + P.bedBack, `${F(P.bedBack)} tall`);
      add('Wheel well', 42, 76, 0, 7.5, 'sticks out 7 in');
      if (P.battOn) add('Battery', L.batt[0], L.batt[1], 0, 9.5, `${F(L.batt[1] - L.batt[0])} wide, 9 1/2 tall`);
      if (L.chairs) add('Lawn chairs, folded flat', L.chairs.x0, L.chairs.x1, L.chairs.z0, L.chairs.z1, `${P.chairN} stacked`);
      if (P.closetOn) {
        add('Closet', L.c0, L.c1, 0, L.ceilF, `${F(P.closetW)} wide x ${F(P.closetD)} deep, doors split at ${F(P.split)} up`);
        add('Closet rod, upper', L.c0, L.c1, P.rodHi - .75, P.rodHi + .75, `${F(P.rodHi)} up`, P.rodHi);
        add('Closet rod, lower', L.c0, L.c1, P.rodLo - .75, P.rodLo + .75, `${F(P.rodLo)} up`, P.rodLo);
      }
      add('Dinette bench', L.bA[0], L.bA[1], 0, P.seatH, `seat at ${F(P.seatH)}, ${F(P.benchD)} deep`);
      add('Dinette bench', L.bB[0], L.bB[1], 0, P.seatH, `seat at ${F(P.seatH)}, ${F(P.benchD)} deep`);
      if (L.tableLen > 0) add('Dinette table', L.tbl[0], L.tbl[1], P.tableH - 1.5, P.tableH, `top at ${F(P.tableH)}`, P.tableH);
      L.cabs.forEach((c, i) => add('Wall cabinet', c[0], c[1], P.cabBot, L.ceilF, `${F(c[1] - c[0])} long x ${F(P.cabDepth)} deep, 3 doors ${F(L.doors[i * 3].w)} wide`));
    } else {
      add('Wet bath (shower)', 0, P.panW, 0, L.ceilF, `${F(P.panW)} x ${F(P.panD)}`);
      { const nkx = Math.min(29.75, P.panW - 6.25), nk0 = nkx - P.snookLen; add('Shower nook', nk0, nkx, P.snookTop - P.snookH, P.snookTop, `${F(P.snookLen)} wide x ${F(P.snookH)} tall, 4 1/2 deep`); }
      if (P.fridgeOn) add('Fridge', L.fr[0], L.fr[1], 8.25, 8.25 + P.fridgeH, `${F(P.fridgeW)} x ${F(P.fridgeD)} x ${F(P.fridgeH)}, on a platform`);
      if (P.microOn) add('Microwave', L.microX[0], L.microX[1], L.microZ[0], L.microZ[1], 'on its shelf');
      add('Counter cabinet', L.cabS, L.sinkS, 0, ch, `top at ${F(ch)}, ${F(P.cabD)} deep`);
      add('Sink cabinet', L.sinkS, L.sinkE, 0, ch, `${F(P.sinkW)} wide, ${F(P.sinkD)} deep`);
      if (P.drawersOn) L.parts.forEach(p => add(cap(p.n.replace(/^the /i, '')), p.x0, p.x1, p.z0, p.z1, `${F(p.x1 - p.x0)} wide x ${F(p.z1 - p.z0)} tall`));
      if (L.can) add('Trash can on a pull-out', L.can.x0, L.can.x1, L.can.z0, L.can.z1, `${F(L.can.x1 - L.can.x0)} x ${F(P.canD)} x ${F(P.canH)}`);
      add('Fresh water tank', L.tankX[0], L.tankX[1], P.tankLift, P.tankLift + P.tankH, `${F(L.tankX[1] - L.tankX[0])} long x ${F(P.tankD)} deep x ${F(P.tankH)} tall`);
      add('Hot water tank', L.hotX[0], L.hotX[1], P.hotShelf, P.hotShelf + P.hotH, `${F(P.hotW)} long x ${F(P.hotD)} deep x ${F(P.hotH)} tall`);
      if (L.jug) add('Drain jug', L.jug.x0, L.jug.x1, L.jug.z0, L.jug.z1, `${F(P.jugD)} across x ${F(P.jugH)} tall`);
      if (P.towelOn) add('Paper towel recess', L.sinkS - 11.5, L.sinkS - .5, 29.75, 35.25, 'in the angled front');
      if (L.hook) add('Dish towel hook and towel', L.hook.x0, L.hook.x1, L.hook.z0, L.hook.z1, `hook at ${F(L.hook.z)} up`);
      if (P.tvOn) add('TV', 76.5, 103.5, ch + 16, ch + 31.4, `bottom at ${F(ch + 16)} up`);
      if (P.nookOn) {
        add('Jar nook', NK(P)[0], NK(P)[1], ch, ch + P.nookH, `${F(NK(P)[1] - NK(P)[0])} wide x ${F(P.nookH)} tall, 4 1/2 deep`);
        add('Jar shelf and jars', L.nookX[0], L.nookX[1], L.nookZ, L.nookZ + 7.75, `shelf at ${F(L.nookZ)} up`);
      }
      add('Wheel well', 42, 76, 0, 7.5, 'sticks out 7 in');
      add('Sliding door opening', P.doorX, P.doorX + P.slideW, 0, P.slideH, `${F(P.slideW)} wide x ${F(P.slideH)} tall`);
      add('Fold-out table (when open)', L.sinkE, L.sinkE + L.flapLen, P.flapH - .75, P.flapH, `${F(L.flapLen)} long x ${F(P.flapD)} deep, top at ${F(P.flapH)}`, P.flapH);
      add('Foot ledge (when down)', L.sinkE, L.sinkE + L.ledgeTot, P.ledgeH - .75, P.ledgeH, `top at ${F(P.ledgeH)}`, P.ledgeH);
    }
    return { items, cab: P.cab, ceil: P.ceil, ceilF: L.ceilF, doorX: P.doorX };
  }, side);
}

function wallSVG(d, side) {
  const S = 7, ML = 44, MT = 26, MB = 54, END = Math.max(d.cab, 156), TOP = 82;
  const W = ML + S*END + 20, H = MT + S*TOP + MB;
  const X = x => ML + S*x, Y = z => MT + S*(TOP - z);
  const o = [];
  // grid
  for (let x = 0; x <= END; x += 6) { const mj = x % 12 === 0; o.push(`<line x1="${X(x).toFixed(1)}" y1="${Y(0).toFixed(1)}" x2="${X(x).toFixed(1)}" y2="${Y(TOP).toFixed(1)}" class="${mj?'gmaj':'gmin'}"/>`); if (mj) o.push(`<text x="${X(x).toFixed(1)}" y="${(Y(0)+16).toFixed(1)}" text-anchor="middle" class="ax">${x}</text>`); }
  for (let z = 0; z <= TOP; z += 6) { const mj = z % 12 === 0; o.push(`<line x1="${X(0).toFixed(1)}" y1="${Y(z).toFixed(1)}" x2="${X(END).toFixed(1)}" y2="${Y(z).toFixed(1)}" class="${mj?'gmaj':'gmin'}"/>`); if (mj) o.push(`<text x="${(X(0)-6).toFixed(1)}" y="${(Y(z)+4).toFixed(1)}" text-anchor="end" class="ax">${z}</text>`); }
  // furring strips (reference), with the passenger door caveat
  const FURR = [[3,'S1'],[12,'S2'],[21.5,'S3'],[30.25,'S4'],[43.5,'S5'],[57.25,'S6'],[66,'S7'],[76.75,'S8']];
  const stopsAtDoor = new Set(['S1','S2','S3','S4','S6']);
  FURR.forEach(([z,nm]) => { const end = (side==='pass' && stopsAtDoor.has(nm)) ? d.doorX : END; o.push(`<line x1="${X(0).toFixed(1)}" y1="${Y(z).toFixed(1)}" x2="${X(end).toFixed(1)}" y2="${Y(z).toFixed(1)}" class="furr"/>`); o.push(`<text x="${(X(0)+3).toFixed(1)}" y="${(Y(z)-2).toFixed(1)}" class="furrlab">${nm} ${fr(z)}"</text>`); });
  // ceiling line
  o.push(`<line x1="${X(0).toFixed(1)}" y1="${Y(d.ceilF).toFixed(1)}" x2="${X(END).toFixed(1)}" y2="${Y(d.ceilF).toFixed(1)}" class="ceil"/>`);
  o.push(`<text x="${(X(END)-4).toFixed(1)}" y="${(Y(d.ceilF)-4).toFixed(1)}" text-anchor="end" class="furrlab">finished ceiling ${fr(d.ceilF)}"</text>`);
  // items, numbered left-to-right then bottom-to-top
  const items = d.items.slice().sort((a,b) => a.x0 - b.x0 || a.z0 - b.z0), placed = [];
  items.forEach((it, i) => { it.n = i+1; const col = colorOf(it.name);
    o.push(`<rect x="${X(it.x0).toFixed(1)}" y="${Y(it.z1).toFixed(1)}" width="${(S*(it.x1-it.x0)).toFixed(1)}" height="${(S*(it.z1-it.z0)).toFixed(1)}" rx="2" fill="var(--${col})" fill-opacity=".12" stroke="var(--${col})" stroke-width="1.4"/>`);
    let cx = X((it.x0+it.x1)/2), cy = Y((it.z0+it.z1)/2);
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0]-cx, q[1]-cy) < 19); t++) cy += 12;
    placed.push([cx, cy]);
    o.push(`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="9" fill="var(--bg)" fill-opacity=".92" stroke="var(--${col})" stroke-width="1.6"/><text x="${cx.toFixed(1)}" y="${(cy+3.6).toFixed(1)}" text-anchor="middle" class="badge" style="fill:var(--${col})">${it.n}</text>`); });
  // frame + end labels
  o.push(`<rect x="${X(0).toFixed(1)}" y="${Y(TOP).toFixed(1)}" width="${(S*END).toFixed(1)}" height="${(S*TOP).toFixed(1)}" fill="none" stroke="var(--line)" stroke-width="1.2"/>`);
  o.push(`<text x="${X(0).toFixed(1)}" y="${(Y(TOP)-8).toFixed(1)}" text-anchor="start" class="end">← rear doors</text>`);
  o.push(`<text x="${X(END).toFixed(1)}" y="${(Y(TOP)-8).toFixed(1)}" text-anchor="end" class="end">cab →</text>`);
  o.push(`<text x="${(X(END/2)).toFixed(1)}" y="${(Y(0)+40).toFixed(1)}" text-anchor="middle" class="axt">inches from the back mark (0 = 6 in in from the rear-door edge)</text>`);
  o.push(`<text transform="translate(${(ML-32).toFixed(1)},${(Y(TOP/2)).toFixed(1)}) rotate(-90)" text-anchor="middle" class="axt">inches up from the floor</text>`);
  const svg = `<svg viewBox="0 0 ${W.toFixed(0)} ${H.toFixed(0)}" role="img" aria-label="${side} wall marking map">${o.join('')}</svg>`;
  // table
  const rows = items.map(it => `<tr><td><span class="kn" style="color:var(--${colorOf(it.name)});border-color:var(--${colorOf(it.name)})">${it.n}</span></td><td>${esc(it.name)}${it.dims?` <span class="kd">${esc(it.dims)}</span>`:''}</td><td>${fr(it.x0)} to ${fr(it.x1)}</td><td>${it.zv != null ? fr(it.zv) : fr(it.z0)+' to '+fr(it.z1)}</td></tr>`).join('');
  const table = `<div class="tw"><table><thead><tr><th></th><th>Item</th><th>From the back mark (in)</th><th>Up from the floor (in)</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  return {svg, table};
}

(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport:{width:1400,height:1000}});
  await page.goto('file://' + __dirname + '/../interactive.html');
  await page.waitForTimeout(700);
  const drv = await grab(page, 'driver');
  const pas = await grab(page, 'pass');
  await b.close();
  const D = wallSVG(drv, 'driver'), P = wallSVG(pas, 'pass');

  const style = `:root{color-scheme:light;--bg:#faf9f5;--card:#fff;--ink:#26241f;--mute:#6a665c;--line:#cdcabf;
  --c1:#185FA5;--c2:#8A5A00;--c3:#0F6E56;--c4:#8B4A8F;--c5:#A3522D;--c6:#5F5E5A;--door:#d9d5ca;}
  @media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#1b1a17;--card:#242320;--ink:#ece9e0;--mute:#aaa598;--line:#3d3b34;--c1:#6fb1ee;--c2:#e0b25d;--c3:#5cc9a7;--c4:#d79bd3;--c5:#e0956b;--c6:#b7b2a6;--door:#33312b;color-scheme:dark;}}
  :root[data-theme="dark"]{--bg:#1b1a17;--card:#242320;--ink:#ece9e0;--mute:#aaa598;--line:#3d3b34;--c1:#6fb1ee;--c2:#e0b25d;--c3:#5cc9a7;--c4:#d79bd3;--c5:#e0956b;--c6:#b7b2a6;--door:#33312b;color-scheme:dark;}
  *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 system-ui,-apple-system,'Segoe UI',Roboto,sans-serif}
  .wrap{max-width:1180px;margin:0 auto;padding-block:16px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  h1{font-size:25px;margin:6px 0 2px}h2{font-size:20px;margin:22px 0 6px}.lead{color:var(--mute);margin:0 0 10px}
  .figwrap{overflow-x:auto;border:1px solid var(--line);border-radius:12px;background:var(--card);padding:8px;margin:0 0 10px}
  svg{min-width:760px;width:100%;height:auto;display:block}
  .gmin{stroke:var(--line);stroke-width:.5;opacity:.5}.gmaj{stroke:var(--line);stroke-width:1}
  .ax{font-size:10px;fill:var(--mute)}.axt{font-size:12px;fill:var(--mute)}
  .furr{stroke:var(--c2);stroke-width:1.3;stroke-dasharray:6 4;opacity:.8}.furrlab{font-size:9.5px;fill:var(--c2)}
  .ceil{stroke:var(--mute);stroke-width:1.4;stroke-dasharray:2 3}
  .badge{font-size:10px;font-weight:700}.end{font-size:12px;font-weight:700;fill:var(--mute)}
  .doorlab{font-size:12px;fill:var(--mute)}
  .tw{overflow-x:auto}
  table{border-collapse:collapse;width:100%;font-size:14px;margin:0 0 8px}
  th,td{border-bottom:1px solid var(--line);padding:5px 8px;text-align:left;vertical-align:top}
  th{color:var(--mute);font-weight:600}td:nth-child(3),td:nth-child(4),th:nth-child(3),th:nth-child(4){white-space:nowrap}
  .kn{display:inline-flex;align-items:center;justify-content:center;width:22px;height:22px;border:1.6px solid;border-radius:50%;font-weight:700;font-size:12px}
  .kd{color:var(--mute)}
  .note{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:10px 14px;color:var(--mute);font-size:14px;margin:0 0 14px}
  a{color:var(--c1)}`;

  const body = `<div class="wrap">
  <h1>Wall marking map</h1>
  <p class="lead">Every built item laid out see-through on each wall, to scale, with a 12 in grid. Measure along the bottom from the <b>back mark</b> (0 is <b>6 in in from the rear-door edge</b>, the same zero as the plan and the wall diagrams, so add 6 in to measure from the doors) and <b>up from the floor</b> on the side, then mark the numbered boxes on the real wall. Dashed brown lines are the furring strips (S1 to S8); the dashed grey line is the finished ceiling. Positions come from the plan and change if you change the sizes there.</p>
  <div class="note">Both walls are drawn with the <b>back of the van on the left</b>, so you measure the same way on either side. (In the interactive plan the passenger wall is drawn the other way round, with the cab on the left.) Out-from-the-wall depths are not shown here; they are in the plan's item list.</div>
  <h2>Driver side wall</h2>
  <div class="figwrap">${D.svg}</div>
  ${D.table}
  <h2>Passenger side wall</h2>
  <div class="figwrap">${P.svg}</div>
  ${P.table}
  <p class="lead" style="margin-top:14px"><a href="interactive.html">Back to the interactive plan</a></p>
  </div>`;

  const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Wall marking map</title><style>${style}</style></head><body>${body}</body></html>`;
  fs.writeFileSync(__dirname + '/../wall-map.html', doc);
  // fragment for the artifact
  const frag = `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Wall Marking Map</title>\n<style>${style}</style>\n${body.replace('<a href="interactive.html">','<a href="https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs" target="_blank" rel="noopener">')}\n`;
  if (!process.env.SC) return console.log('wall-map.html', doc.length);
  fs.writeFileSync(process.env.SC + '/wmap/index.html', frag);
  fs.writeFileSync(process.env.SC + '/wmap/preview.html', '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+frag+'</body></html>');
  console.log('wall-map.html', doc.length, 'driver items', drv.items.length, 'pass items', pas.items.length);
})();
