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
  [/floor-to-ceiling wall|wall cabinet|closet|counter cabinet|sink cabinet|drawer|shelf board|board/i, 'c1'],
  [/couch|cushion|bench|dinette|fold-out|foot ledge/i, 'c2'],
  [/tank|jug|drain|paper towel|trash/i, 'c3'],
  [/fridge|microwave|\btv\b|nook|jar/i, 'c4'],
  [/wheel well|battery|inverter|charger|sliding door|wet bath|hook|lawn chair|side window|gear cabinet|gear shelf/i, 'c5'],
];
const colorOf = n => (CAT.find(c => c[0].test(n)) || [,'c6'])[1];

async function grab(page, side) {
  // every item comes straight from the plan's layout L (same numbers the interactive page draws)
  return page.evaluate((side) => {
    const P = L.P, ch = P.counterH, f = v => Math.round(v * 100) / 100, items = [];
    const add = (name, x0, x1, z0, z1, dims, zv) => items.push({ name, dims: dims || '', x0: f(x0), x1: f(x1), z0: f(z0), z1: f(z1), zv: zv == null ? null : f(zv) });
    const F = fmt;
    if (side === 'driver') {
      add('Couch frame and deck (removable)', 0, P.bedLen, 0, P.platform, `${F(P.bedLen)} long x ${F(P.bedD)} deep; rails ${F(P.platform - 1.5 - 3.5)} to ${F(P.platform - 1.5)} up, deck ${F(P.platform - 1.5)} to ${F(P.platform - .75)}; it lifts out (see the wall blocks and the gear cabinet)`);
      if (L.cmod) add('Front rail across the gear cabinet', L.cmod.fr.x0, L.cmod.fr.x1, L.cmod.fr.z0, L.cmod.fr.z1, `3/4 x ${F(L.cmod.fr.h)} hardwood, glued and screwed under the deck front, bottom ${F(L.cmod.fr.z0)} up`);
      add('Seat cushion', 0, P.bedLen, P.platform, P.platform + P.mattress, `top at ${F(P.platform + P.mattress)}`);
      add('Back cushion, upright', 0, P.bedLen, P.platform + P.mattress, P.platform + P.mattress + P.bedBack, `${F(P.bedBack)} tall`);
      add('Wheel well', 42, 76, 0, 7.5, 'sticks out 7 in');
      if (P.battOn) add('Battery', L.batt[0], L.batt[1], 0, 9.5, `${F(L.batt[1] - L.batt[0])} wide, 9 1/2 tall`);
      if (L.gear) {
        const sh = L.gear.sh;
        add('Gear shelf (pull-out, over the battery)', sh.x0, sh.x1, sh.z0, sh.z1, `${F(sh.x1 - sh.x0)} x ${F(sh.y1 - sh.y0)} in with its rails, ${F(sh.z0)} up (1 in over the battery top), ${F(sh.y0)} to ${F(sh.y1)} out from the wall, on two ${F(P.shPull)} in slides: one on the closet end panel, one on a divider at ${F(sh.div)} to ${F(sh.div + .75)}`);
        [['Inverter, BELTTT 2000 W', L.gear.inv], ['DC-DC charger, LiTime 60 A', L.gear.dc], ['Shore charger, VEVOR 80 A', L.gear.ch]].forEach(r => add(r[0], r[1].x0, r[1].x1, r[1].z0, r[1].z1, `${F(r[1].x1 - r[1].x0)} x ${F(r[1].y1 - r[1].y0)} x ${F(r[1].z1 - r[1].z0)}, on the gear shelf (${F(r[1].z0)} up), ${F(r[1].y0)} to ${F(r[1].y1)} out from the wall`));
      }
      if (L.gcab) {
        const c = L.gcab;
        add('Gear cabinet (floor-mounted, two side panels)', c.x0, c.x1 + .75, 0, c.z1, `3/4 in plywood panels at ${F(c.x0)} and ${F(c.x1)} in from the back, ${F(c.y1)} deep, floor to the deck (${F(c.z1)} up); the gear shelf is its sliding top, the battery stays on the floor under it; each panel stands on a floor cleat`);
        L.cblk.forEach(b => add('Couch wall block at ' + F(b.x), b.x0, b.x1, b.z0, b.z1, `a 2x2 post ${F(b.x1 - b.x0)} wide x ${F(b.y1)} out x ${F(b.z1 - b.z0)} tall, standing on the floor, centered ${F(b.x)} in from the back; screw it through the planks into the furring rails S1 and S2; the couch frame's back rail rests on it${b.x === P.blkB ? ' (if needed)' : ''}`));
      }
      if (L.chairs) add('Lawn chairs, folded flat', L.chairs.x0, L.chairs.x1, L.chairs.z0, L.chairs.z1, `${P.chairN} stacked`);
      if (P.closetOn) {
        add('Closet', L.c0, L.c1, 0, L.ceilF, `${F(P.closetW)} wide x ${F(P.closetD)} deep, one door above ${F(L.split)} up, drawers below`);
        add('Closet rod', L.c0, L.c1, P.rodHi - .75, P.rodHi + .75, `${F(P.rodHi)} up, ${F(P.cloLen)} in clothes hang to ${F(L.hangBot)}`, P.rodHi);
        add('Closet drawers', L.c0, L.c1, 1, L.drawTop, `${L.cloDr.length} drawers, each ${F(L.cloDrH)} tall x ${F(L.cloDrW)} wide x ${F(P.cloDrawD)} deep inside`);
      }
      add('Dinette bench', L.bA[0], L.bA[1], 0, P.seatH, `seat at ${F(P.seatH)}, ${F(P.benchD)} deep`);
      add('Dinette bench', L.bB[0], L.bB[1], 0, P.seatH, `seat at ${F(P.seatH)}, ${F(P.benchD)} deep`);
      if (L.tableLen > 0) add('Dinette table', L.tbl[0], L.tbl[1], P.tableH - 1.5, P.tableH, `top at ${F(P.tableH)}`, P.tableH);
      if (L.win) {
        const w = L.win;
        add('Side window cutout (cut through the steel)', w.cx0, w.cx1, w.cz0, w.cz1, `${F(w.cx1 - w.cx0)} wide x ${F(w.cz1 - w.cz0)} tall, sill ${F(w.cz0)} up (the slider frame outline; mark it from the template, then cut)`);
        add('Side window glass outline (outside the van)', w.gx0, w.gx1, w.gz0, w.gz1, `${F(w.gx1 - w.gx0)} x ${F(w.gz1 - w.gz0)}, the glass is bigger than the hole: it ends ${F(w.cx0 - w.gx0)} in left of the cutout`);
        add('Side window frame (furring: two jambs, sill and head)', w.cx0 - 1.5, w.cx1 + 1.5, w.cz0 - 1.5, w.cz1 + 1.5, `3/4 x 1 1/2 in furring rail all round the cutout; S5 and S6 stop at it`);
      }
      L.walls.filter(w => w.side === 'd').forEach(w => add('Floor-to-ceiling wall', w.x0, w.x1, 0, L.ceilF, `${w.id}: ${F(P.fwT)} thick, ${F(w.d)} out from the wall, ${w.id === 'W1' ? 'the back of the rear bench leans on it' : 'behind the driver seat, the back of the cab-end bench leans on it'}`));
      L.cabs.forEach((c, i) => add('Wall cabinet', c[0], c[1], P.cabBot, L.ceilF, `${F(c[1] - c[0])} long x ${F(P.cabDepth)} deep, 3 doors ${F(L.doors[i * 3].w)} wide`));
    } else {
      add('Wet bath (shower)', 0, P.panW, 0, L.ceilF, `${F(P.panW)} x ${F(P.panD)}`);
      { const nkx = Math.min(29.75, P.panW - 6.25), nk0 = nkx - P.snookLen; add('Shower nook', nk0, nkx, P.snookTop - P.snookH, P.snookTop, `${F(P.snookLen)} wide x ${F(P.snookH)} tall, 4 1/2 deep`); }
      if (P.fridgeOn) add('Fridge', L.fr[0], L.fr[1], 8.25, 8.25 + P.fridgeH, `${F(P.fridgeW)} x ${F(P.fridgeD)} x ${F(P.fridgeH)}, on a platform`);
      if (P.microOn) add('Microwave', L.microX[0], L.microX[1], L.microZ[0], L.microZ[1], 'on its shelf');
      L.walls.filter(w => w.side === 'p').forEach(w => add('Floor-to-ceiling wall', w.x0, w.x1, 0, L.ceilF, `${w.id}: ${F(P.fwT)} thick, ${F(w.d)} out from the wall, ${w.id === 'W3' ? 'between the shower and the fridge' : 'between the fridge and the counter cabinet'}`));
      if (L.liner) add('Waterproof liner (FRP, over the plywood)', L.liner.x0, L.liner.x1, L.liner.z0, L.liner.z1, `${(+P.linerT).toFixed(2)} in thick; stops ${F(P.linerGap)} in above the pan edge (sealant in the gap); the nook cut out and lined; also on W3's stall face`);
      if (L.toilet) add('Toilet', L.toilet.x0, L.toilet.x1, 3.8, 3.8 + L.toilet.z1, `${F(P.toiletD)} along the wall x ${F(P.toiletW)} out, ${F(L.toilet.z1)} high, back against the wall to the fridge, the Reliance Fold-To-Go, left set up in the stall`);
      if (L.sn) {
        add('Towel bar (in the shower nook)', L.sn.bar.x0, L.sn.bar.x1, L.sn.bar.z - .5, L.sn.bar.z + .5, `${F(L.sn.bar.z)} up, inside the nook`, L.sn.bar.z);
        if (L.sn.cord) add('Bungee cord (across the shower nook front)', L.sn.cord.x0, L.sn.cord.x1, L.sn.cord.z - .25, L.sn.cord.z + .25, `${F(L.sn.cord.z)} up, between two screw eyes, keeps the bottles in`, L.sn.cord.z);
        add('Shelf board (in the shower nook)', L.sn.bay, L.sn.x1, L.sn.shelfTop - .75, L.sn.shelfTop, `top at ${F(L.sn.shelfTop)} up, toilet paper under it, bottles on it`, L.sn.shelfTop);
      }
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


// the wall's own drawing (depth colours, pans, holes, furring rails and dots) comes from sides.html (diagrams A and D);
// the items are drawn on top of it, almost transparent, in the same coordinates
async function grabBase(page, idx) {
  return page.evaluate((idx) => {
    const svg = [...document.querySelectorAll('svg[viewBox="0 0 1070 636"]')][idx].cloneNode(true);
    svg.querySelectorAll('text').forEach(t => { if (/^(Driver side wall:|Passenger side, seen)/.test(t.textContent.trim())) t.remove(); });
    const legend = svg.closest ? null : null;
    const lg = [...document.querySelectorAll('p.legend')][idx === 0 ? 0 : 1] || document.querySelector('p.legend');
    return { inner: svg.innerHTML, legend: lg ? lg.outerHTML : '' };
  }, idx);
}

function wallSVG(d, side, base) {
  const flip = side === 'pass';
  const X = x => flip ? 1020 - 6 * x : 50 + 6 * x, Y = z => 544 - 6 * z;
  const o = [];
  const items = d.items.slice().sort((a, b) => a.x0 - b.x0 || a.z0 - b.z0), placed = [];
  items.forEach((it, i) => {
    it.n = i + 1;
    const xa = X(it.x0), xb = X(it.x1), x = Math.min(xa, xb), w = Math.abs(xb - xa), y = Y(it.z1), h = 6 * (it.z1 - it.z0);
    o.push(`<rect x="${x.toFixed(1)}" y="${y.toFixed(1)}" width="${w.toFixed(1)}" height="${Math.max(h, 1.5).toFixed(1)}" rx="2" fill="#1b1a17" fill-opacity=".05" stroke="#1b1a17" stroke-width="1.4" stroke-dasharray="${it.zv != null ? '3 2' : 'none'}"/>`);
    let cx = (xa + xb) / 2, cy = Y((it.z0 + it.z1) / 2);
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0] - cx, q[1] - cy) < 19); t++) cy += 12;
    placed.push([cx, cy]);
    o.push(`<circle cx="${cx.toFixed(1)}" cy="${cy.toFixed(1)}" r="9" fill="#fff" fill-opacity=".92" stroke="#1b1a17" stroke-width="1.5"/><text x="${cx.toFixed(1)}" y="${(cy + 3.6).toFixed(1)}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#1b1a17">${it.n}</text>`);
  });
  const id = flip ? 'P' : 'D';
  const svg = `<svg viewBox="0 0 1070 636" role="img" aria-label="${flip ? 'Passenger' : 'Driver'} wall: steel depth map, furring rails and the items, almost transparent, on top">${base.inner}<g id="wmItems${id}">${o.join('')}</g></svg>`;
  const rows = items.map(it => `<tr><td><span class="kn">${it.n}</span></td><td>${esc(it.name)}${it.dims ? ` <span class="kd">${esc(it.dims)}</span>` : ''}</td><td>${fr(it.x0)} to ${fr(it.x1)}</td><td>${it.zv != null ? fr(it.zv) : fr(it.z0) + ' to ' + fr(it.z1)}</td></tr>`).join('');
  const table = `<div class="tw"><table><thead><tr><th></th><th>Item</th><th>From the back mark (in)</th><th>Up from the floor (in)</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  return { svg, table, id, legend: base.legend };
}

(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport:{width:1400,height:1000}});
  await page.goto('file://' + __dirname + '/../interactive.html');
  await page.waitForTimeout(700);
  const drv = await grab(page, 'driver');
  const pas = await grab(page, 'pass');
  const page2 = await b.newPage({viewport:{width:1400,height:1000}});
  await page2.goto('file://' + __dirname + '/../sides.html');
  await page2.waitForTimeout(500);
  const baseA = await grabBase(page2, 0), baseD = await grabBase(page2, 2);
  const css = await page2.evaluate(() => [...document.querySelectorAll('style')].map(s => s.textContent).join('\n'));
  await b.close();
  const D = wallSVG(drv, 'driver', baseA), P = wallSVG(pas, 'pass', baseD);

  const style = css + `
  body { max-width: none; margin: 0; padding: 0; background: #fff; color: #2C2C2A; color-scheme: light; }
  .wrap { max-width: 1180px; margin: 0 auto; padding-block: 16px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
  h1 { font-size: 24px; margin: 6px 0 2px; } h2 { font-size: 19px; margin: 26px 0 6px; }
  .lead { color: #5F5E5A; margin: 0 0 10px; font-size: 15px; }
  .figwrap { overflow-x: auto; border: 1px solid #D3D1C7; border-radius: 10px; padding: 6px; margin: 6px 0; background: #fff; }
  .figwrap svg { min-width: 820px; }
  .tog { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 14px; margin: 6px 0; }
  .tw { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; font-size: 14px; margin: 6px 0 8px; }
  th, td { border-bottom: 1px solid #D3D1C7; padding: 5px 8px; text-align: left; vertical-align: top; }
  th { color: #5F5E5A; font-weight: 600; } td:nth-child(3), td:nth-child(4), th:nth-child(3), th:nth-child(4) { white-space: nowrap; }
  .kn { display: inline-flex; align-items: center; justify-content: center; width: 22px; height: 22px; border: 1.6px solid #1b1a17; border-radius: 50%; font-weight: 700; font-size: 12px; }
  .kd { color: #5F5E5A; }
  .note { background: #FAF9F5; border: 1px solid #D3D1C7; border-radius: 10px; padding: 10px 14px; color: #5F5E5A; font-size: 14px; margin: 0 0 14px; }
  a { color: #185FA5; }`;

  const sec = (title, W, itemsId, furrId, furrLabel) => `<h2>${title}</h2>
  <div class="tog"><label><input type="checkbox" id="t_${furrId}" checked onchange="document.getElementById('${furrId}').style.display=this.checked?'':'none'"> ${furrLabel}</label>
  <label><input type="checkbox" id="t_${itemsId}" checked onchange="document.getElementById('${itemsId}').style.display=this.checked?'':'none'"> Show the items (numbered, almost transparent)</label></div>
  <div class="figwrap">${W.svg}</div>
  ${W.legend}
  ${W.table}`;
  const body = `<div class="wrap">
  <h1>Wall marking map: steel, furring rails and items</h1>
  <p class="lead">Diagrams A and D from the static page (the colors are how far the steel stands off the body, the white dots are the furring rails' attachment points) with every built item drawn almost transparent on top, numbered. Each table says where an item sits: measure along the wall from the <b>back mark</b> (0 is <b>6 in in from the rear-door edge</b>, the same zero as the plan and the wall diagrams, so add 6 in to measure from the doors) and <b>up from the floor</b>. Positions come from the plan and change with its sizes; the steel and the furring rails are the measured drawing.</p>
  <div class="note"><b>The three kinds of attachment mark.</b> Every white dot is a place where a furring rail, one of the long 1x4 boards, is fixed to the van. What goes between the steel and the furring rail is a spacer, and there are three kinds. <b>Adhesive pad</b> (S1, S2, S3, the S5 pieces and V4 that sit on flat steel): the furring rail lies straight on the steel with a patch of structural adhesive or VHB tape, no spacer. <b>Spacer block, 3 1/2 in</b> (S4, S5, S6, the window frame and the nook frames V1 to V3): a 3 1/2 in cut of 2x4, 1 1/2 along the wall by 3 1/2 up on the steel and 3 5/8 in out with the glue, glued to the steel and never screwed, and the furring rail is then glued and screwed to it. <b>Thin shim</b> (S7, S8, ordinary 1x4 furring rails like the rest; only what sits under them differs): a plywood square, 1 1/2 x 1 1/2 in, 1/4 in thick under S7 and 5/8 in under S8, glued to the steel, because the steel up there is already about 3 1/2 in deep. The Furring page of the build guide has the block chart (every block with its distance from the back mark) and how to attach a block to the steel.</div>
  <div class="note">The driver wall is drawn with the back of the van on the left. The passenger wall is drawn as diagram D is, with the cab on the left and the back on the right. Dashed item boxes are things that only exist at one height (rods, table tops, the foot ledge): the table gives that one height. Out-from-the-wall depths are not in the tables.</div>
  ${sec('Driver side wall', D, 'wmItemsD', 'furr', 'Show the furring rails (S1 to S8) and their attachment dots')}
  ${sec('Passenger side wall', P, 'wmItemsP', 'furrP', 'Show the furring rails (S1 to S8) and the nook frames (V1 to V4)')}
  <p class="lead" style="margin-top:14px"><a href="interactive.html">Back to the interactive plan</a></p>
  </div>`;

  const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Wall marking map</title><style>${style}</style></head><body>${body}</body></html>`;
  fs.writeFileSync(__dirname + '/../wall-map.html', doc);
  if (!process.env.SC) return console.log('wall-map.html', doc.length);
  const frag = `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Wall Marking Map</title>\n<style>${style}</style>\n${body.replace('<a href="interactive.html">','<a href="https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs" target="_blank" rel="noopener">')}\n`;
  fs.writeFileSync(process.env.SC + '/wmap/index.html', frag);
  fs.writeFileSync(process.env.SC + '/wmap/preview.html', '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body>'+frag+'</body></html>');
  console.log('wall-map.html', doc.length, 'driver items', drv.items.length, 'pass items', pas.items.length);
})();
