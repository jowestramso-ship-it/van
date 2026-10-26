/* Builds ../interior.html: a 3D view of the inside of the van, drawn from the plan's own sizes (read from interactive.html in a headless browser).
   The page loads three.js from cdnjs; tools/interior_scene.js builds the scene.
   Run:  node tools/interior.js      (needs playwright + the bundled Chromium; build.sh runs it and skips it if they are missing)
   With SC set it also writes a copy that loads a local three.js (SC/three3d/node_modules/three/build/three.min.js), for stills. */
const {chromium} = require(process.env.NODE_PATH + '/playwright');
const fs = require('fs');

(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport: {width: 1400, height: 1000}});
  await page.goto('file://' + __dirname + '/../interactive.html'); await page.waitForTimeout(700);
  const D = await page.evaluate(() => {
    const P = L.P, f = v => Math.round(v * 1000) / 1000, o = {};
    Object.keys(P).forEach(k => { if (typeof P[k] === 'number' || typeof P[k] === 'boolean') o[k] = typeof P[k] === 'number' ? f(P[k]) : P[k]; });
    const roofY = []; for (let y = 0; y <= P.vanW + .001; y += 2) roofY.push(f(L.roofZ(Math.min(y, P.vanW))));
    const nk = NK(P);
    return {
      P: o, roofY, roofS: 2, nook: nk, nookX: L.nookX.map(f), nookZ: f(L.nookZ), jars: JN(P),
      cabLights: [P.bedLen / 2, (L.bA[0] + L.bA[1]) / 2 + 6, (L.bB[0] + L.bB[1]) / 2 - 6].map(f),
      L: {
        cabs: L.cabs, doors: L.doors.map(d => ({x0: f(d.x0), x1: f(d.x1)})), doorZ: L.doorZ.map(f), c0: L.c0, c1: L.c1, bA: L.bA, bB: L.bB, tbl: L.tbl.map(f), tableLen: f(L.tableLen),
        fr: L.fr, microX: L.microX.map(f), microZ: L.microZ.map(f), cabS: L.cabS, angS: L.angS, sinkS: L.sinkS, sinkE: L.sinkE,
        parts: L.parts.map(p => ({id: p.id, kind: p.kind, x0: f(p.x0), x1: f(p.x1), z0: f(p.z0), z1: f(p.z1)})),
        lights: L.lights.map(l => ({x: f(l.x), y: f(l.y)})), ceilF: f(L.ceilF), lining: f(L.lining), slatY: L.slatY.map(f),
        fan: {x: L.fan.x, y: L.fan.y, w: L.fan.w}, ac: {x: L.ac.x, y: L.ac.y, w: L.ac.w},
        hook: L.hook ? {x: f(L.hook.x), z: f(L.hook.z), z0: f(L.hook.z0)} : null,
        split: f(L.split), cloDr: L.cloDr.map(d => ({z0: f(d.z0), z1: f(d.z1)})), hangBot: f(L.hangBot),
        toilet: L.toilet, sn: L.sn, batt: L.batt.map(f), win: L.win ? JSON.parse(JSON.stringify(L.win, (k, v) => typeof v === 'number' ? f(v) : v)) : null, chairs: L.chairs ? { x0: f(L.chairs.x0), x1: f(L.chairs.x1), d0: f(L.chairs.d0), d1: f(L.chairs.d1), z0: f(L.chairs.z0), z1: f(L.chairs.z1) } : null, gear: L.gear ? JSON.parse(JSON.stringify(L.gear, (k, v) => typeof v === 'number' ? f(v) : v)) : null,
        walls: L.walls.map(w => ({id: w.id, side: w.side, x0: f(w.x0), x1: f(w.x1), d: f(w.d)})),
      },
    };
  });
  await b.close();
  const scene = fs.readFileSync(__dirname + '/interior_scene.js', 'utf8');
  const css = `:root{color-scheme:light dark;--bg:#fbfaf7;--card:#fff;--ink:#26241f;--mute:#6a665c;--line:#d9d5ca;--acc:#185FA5}
  @media (prefers-color-scheme:dark){:root{--bg:#1b1a17;--card:#242320;--ink:#ece9e0;--mute:#aaa598;--line:#3d3b34;--acc:#6fb1ee}}
  *{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",system-ui,sans-serif}
  .wrap{max-width:1180px;margin:0 auto;padding-block:16px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
  h1{font-size:24px;margin:6px 0 2px}.lead{color:var(--mute);margin:0 0 10px;font-size:15px}
  .stage{border:1px solid var(--line);border-radius:12px;overflow:hidden;background:#222;line-height:0}
  canvas{display:block;touch-action:none;cursor:grab;max-width:100%}
  .bar{display:flex;flex-wrap:wrap;gap:8px;margin:10px 0}
  button{font:inherit;font-size:14px;padding:6px 12px;border:1px solid var(--line);border-radius:18px;background:var(--card);color:var(--ink);cursor:pointer}
  button[aria-pressed=true]{background:var(--ink);color:var(--bg)}
  .note{color:var(--mute);font-size:14px;margin:8px 0}.sl{display:flex;gap:10px;align-items:center;font-size:14px;flex:1 1 320px}.sl input{flex:1;min-width:120px}`;
  const body = `<div class="wrap"><h1>Inside the van, in 3D</h1>
  <p class="lead">A 3D model built from the plan's own sizes: the walls and the cabinets in a light wood stain, the countertop medium grey, a light grey plywood ceiling under light wood planks. Drag to look around, scroll or pinch to zoom, and use the buttons to jump to a viewpoint or to step along the van. Under the couch, the inverter and the two chargers sit on one pull-out shelf over the battery: the shelf is the sliding top of a gear cabinet (two floor-mounted panels, the battery on the floor under it): press Play (or drag the slider) to see it slide out into the aisle. The couch above is a removable frame on three wall blocks with a separate deck lid.</p>
  <div class="stage"><canvas id="c" width="1280" height="720"></canvas></div>
  <div class="bar" id="views"></div>
  <div class="bar"><button id="back" type="button">Step back</button><button id="fwd" type="button">Step forward</button></div>
  <div class="bar" id="railbar"><button id="rplay" type="button">Play</button><label class="sl">The gear shelf sliding out of its cabinet <input type="range" id="rs" min="0" max="100" value="0"></label></div>
  <p class="note" id="cap"></p>
  <p class="note">This is a rendering of a model, not a photograph. The positions and sizes come from the plan. The finishes are placeholders where you have not chosen: the fabric (oatmeal), the floor (a mid grey-brown plank), the fridge (white), the pulls (black), and the cab seen through the open end. The sliding door is drawn open with daylight coming in.</p></div>`;
  const mk = three => `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Van interior in 3D</title><style>${css}</style></head><body>${body}<script src="${three}"></script><script>const D=${JSON.stringify(D)};</script><script>${scene}</script></body></html>`;
  fs.writeFileSync(__dirname + '/../interior.html', mk('https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js'));
  if (process.env.SC) {
    fs.writeFileSync(process.env.SC + '/three3d/interior_local.html', mk('node_modules/three/build/three.min.js'));
    fs.mkdirSync(process.env.SC + '/in3d', {recursive: true});
    fs.writeFileSync(process.env.SC + '/in3d/index.html', `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Van Interior 3D</title>\n<style>${css}</style>\n${body}\n<script src="https://cdnjs.cloudflare.com/ajax/libs/three.js/r128/three.min.js"></script>\n<script>const D=${JSON.stringify(D)};</script>\n<script>${scene}</script>\n`);
  }
  console.log('interior.html written, data', JSON.stringify(D).length, 'bytes');
})();
