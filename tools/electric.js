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
// kinds: out120 = 120 V outlet, sw = switch, lt = light, strip = LED strip (x0..x1 at z), box = a mounted unit, inlet, panel, run = a wire run (vertical x from z0 to z1)
const E_DRIVER = pl => { const oz = pl.win && pl.win.cz0 - 5 < 36 ? pl.win.cz0 - 5 : 36, tc = (pl.tbl[0] + pl.tbl[1]) / 2, q1 = pl.bedLen / 4, q3 = 3 * pl.bedLen / 4, lz = pl.cabBot - .5; return [
  {k:'box',   n:'Battery, 280 Ah (assumed lithium)',          x0:52, x1:73, z0:0, z1:9.5, note:'where the plan has it, in front of the wheel well; main fuse (Class T, 250 A) within 7 in of its + post. The gear shelf slides over it, 1 in above its top, so the posts need right-angle lugs'},
  ...(pl.gear ? [
    {k:'box', n:'Inverter, BELTTT 2000 W (inverter only: no charger, no transfer switch)', x0:pl.gear.inv.x0, x1:pl.gear.inv.x1, z0:pl.gear.inv.z0, z1:pl.gear.inv.z1, note:'on the pull-out gear shelf over the battery, rear row, ' + fr(pl.gear.inv.y0) + ' to ' + fr(pl.gear.inv.y1) + ' in out from the wall; its battery cables are 2/0 AWG to the bus with a loop about 2 ft longer than a fixed run so the shelf can slide out (Class T 250 A fuse within 7 in of the battery post, fixed; not the 3 ft cables it comes with); its AC output goes to the transfer switch on the hub board; the remote (23 ft cable) goes by the control panel'},
    {k:'box', n:'DC-DC charger, LiTime 60 A', x0:pl.gear.dc.x0, x1:pl.gear.dc.x1, z0:pl.gear.dc.z0, z1:pl.gear.dc.z1, note:'on the pull-out gear shelf, rear row, ' + fr(pl.gear.dc.y0) + ' to ' + fr(pl.gear.dc.y1) + ' in out from the wall; 2 AWG from the starter battery (about 15 ft plus a 2 ft loop for the shelf: 4 AWG would lose 3.6% on the way, 2 AWG 2.5%) with an 80 A fuse at the starter battery, 2 AWG to the battery bus with an 80 A fuse and a loop; the size is as you measured it (16 x 9 x 4.5)'},
    {k:'box', n:'Shore charger, VEVOR 80 A (14.6 V lithium)', x0:pl.gear.ch.x0, x1:pl.gear.ch.x1, z0:pl.gear.ch.z0, z1:pl.gear.ch.z1, note:'on the pull-out gear shelf, front row, ' + fr(pl.gear.ch.y0) + ' to ' + fr(pl.gear.ch.y1) + ' in out from the wall; its AC input cord also needs a loop for the shelf; AC input from the shore side only, on its own 15 A breaker (about 11 A at 120 V), never from the inverter; 2 AWG to the battery bus with a 100 A fuse; the size is as you measured it (9 1/2 x 7 x 4 thick)'},
  ] : []),
  {k:'box',   n:'Power hub board',                             x0:72, x1:74, z0:1, z1:11, note:'a plywood board on the closet’s rear panel, facing the battery: DC bus bars, shunt, Class T fuse, 12 V fuse block, and the AC panel with its 30 A transfer switch (shore or inverter, never both) and the breakers for the shore charger. The inverter and the two chargers are separate, on the pull-out gear shelf over the battery. The couch front under the deck is open (not covered), so the board and the battery are reached from the aisle without a hatch'},
  {k:'inlet', n:'Shore power inlet (30 A)',                    x:9, z:13.75,  note:'in the middle of the cover plate CP on the outside of the driver wall (CP is 4 3/4 to 13 1/4 in along, 10 3/4 to 16 3/4 up, a plate and not a hole, so it is cut for the inlet; its middle is 9 in along, 13 3/4 up). Moved here from 80 in along, 21 up. The 30 A cable (10 AWG in flexible conduit, about 8 ft) runs inside the wall in the free band above the furring strip S2 (S2 is 10 1/4 to 13 3/4 up; the band is 13 3/4 to 19 1/2 up, clear of the couch wall-post screws, which go into S1 and S2) to the closet’s rear panel at about 73 in, then down to the hub board and its 30 A breaker. Two things to settle: S2 sits straight on the steel and crosses the lower half of CP, so it needs a box-out around the inlet’s back (or the inlet sits 2 in higher), and the cable needs a groove in the back of S2 (or a gap) where it drops to the hub board. The couch frame’s back rail (13 1/2 to 17 up) is in front of the spot, so reach the inlet’s back with the couch lifted out, or cut a small access panel in the plywood'},
  {k:'lt',    n:'Light under the cabinet, middle of the couch', x:pl.bedLen / 2, z:lz, note:'12 V LED on the underside of the wall cabinet (bottom at ' + fr(pl.cabBot) + ' in), in the middle of the couch (0 to 74); on the couch switch; the wire comes down from inside the cabinet'},
  {k:'lt',    n:'Light under the cabinet, dinette rear seat',  x:(pl.bA[0] + pl.bA[1]) / 2 + 6, z:lz, note:'centered over the rear bench seat (' + fr(pl.bA[0]) + ' to ' + fr(pl.bA[1]) + '), then 6 in toward the table; on the dinette switch'},
  {k:'lt',    n:'Light under the cabinet, dinette cab-end seat', x:(pl.bB[0] + pl.bB[1]) / 2 - 6, z:lz, note:'centered over the cab-end bench seat (' + fr(pl.bB[0]) + ' to ' + fr(pl.bB[1]) + '), then 6 in toward the table; on the dinette switch. These two replace the single light I had over the table'},
  {k:'plate', n:'Couch plate: light switch and 120 V outlet (two plugs)', x:62, z:44, note:'one 2 gang plate above the back cushion (40 in up): a switch for the light under the cabinet over the middle of the couch, and a duplex outlet (two plugs) on circuit A (GFCI), 12 AWG. The switch wire is 12 V, the outlet is 120 V: use a divided box or two separate boxes, never one cable for both'},
  {k:'sw',    n:'Switch plate at the rear doors (fan, wet bath light)', x:3,  z:48, note:'2 gang: roof fan and the wet bath light over the shower. You did not list this one, but those two need a switch'},
  {k:'sw',    n:'Light switch by the dinette',                  x:pl.cab - 1, z:48, note:'on the wall behind the driver seat (the cab wall, at the cab end of the dinette; drawn here at its corner with the driver wall), above the bench back (38 in): the two lights under the cabinet over the dinette seats, the ceiling light over the countertop and the sink. The wire comes down the corner behind the planks'},
  {k:'strip', n:'Soft LED strip, ceiling edge, driver side run (154 in)', x0:1, x1:pl.cab - 1, z:73, note:'one of three runs of one warm white (2700 K or warmer) dimmable 12 V strip in an aluminum channel with a frosted diffuser, at the ceiling edge, aimed up so it glows off the cedar ceiling. The wall cabinets run up to the ceiling here, so the channel sits on the top front edge of the cabinets behind a 1 in lip. Fed from the ceiling junction box through riser A'},
  {k:'sw',    n:'Switch and dimmer for the soft LED lighting',  x:70, z:44, note:'next to the couch plate (a separate single gang box, 8 in along from it): a momentary push button into a dimming controller for the soft strip, which has its own 12 V circuit (10 A, 14 AWG) because the strip draws more than the other lights. Say if you want it on the rear doors plate or the dinette plate instead'},
  {k:'out120',n:'Outlet over the dinette table (120 V duplex)', x:tc, z:oz, note:'on the wall just over the table (its top is at 29 in), in the middle of it, clear of the backrests (38 in)' + (pl.win ? '; moved down from 36 to ' + fr(oz) + ' in up because the side window (its frame starts at ' + fr(pl.win.cz0 - 1.5) + ') is now over the table' : '') + '; circuit A (GFCI)'},
  {k:'run',   n:'Riser A: A/C, 12 V and lights feed',          x:73, z0:11, z1:75, note:'up inside the wall behind the planks (4 1/2 in space) to the ceiling: A/C 6 AWG pair in its own loom, plus the 12 V ceiling feed (12 AWG). Grommet where it crosses the top steel'},
  {k:'run',   n:'Cab charge cable (DC-DC input)',              x:70, z0:0, z1:1,  note:'2 AWG from the starter battery fuse (80 A) under the van along the driver side frame to a sealed floor grommet next to the battery'},
]; };
const E_PASS = pl => { const sl = pl.lights.filter(l => l.x > 6 && l.x < 6 + pl.panW)[0] || { x: 6 + pl.panW / 2, y: pl.P.vanW - pl.panD / 2 }, wbx = sl.x - 6, wby = sl.y, cl = pl.lights.filter(l => l.x - 6 >= pl.panW).sort((a, b) => a.x - b.x); return [
  {k:'lt',    n:'Wet bath light (ceiling, IP65), over the shower', x:wbx, z:pl.ceilF - .5, note:'over the middle of the stall: ' + fr(wbx) + ' in along the wall, ' + fr(wby) + ' in across from the driver wall, on the slat (the exact center, 18 in, is under a rib, so it sits 2 1/2 in toward the cab); a wet-rated (IP65) LED; one of the two ceiling lights, the only ceiling lights in the van. Switched at the rear doors plate'},
  {k:'lt',    n:'Ceiling light over the countertop and the sink', x:cl[0] ? cl[0].x - 6 : 89.4, z:pl.ceilF - .5, note:'one light over both, about the middle of the counter cabinet and the sink cabinet together (58 to 123), ' + fr(cl[0] ? cl[0].y : 58) + ' in across from the driver wall, on the slat and 2 in clear of the rib at 97 3/8; on the dinette switch'},
  {k:'out120',n:'Fridge outlet, behind the fridge (120 V)',    x:47, z:6,  note:'on the wall behind the fridge platform (the fridge stands on a platform 8 1/4 up); circuit C, the fridge alone'},
  {k:'out120',n:'Microwave outlet (120 V, its own breaker)',    x:60, z:64, note:'a fifth outlet you did not list: the microwave (1500 W) needs its own, on the wall just cab-side of it (36 to 58); circuit B. Drop it if the microwave plugs in elsewhere'},
  {k:'panel', n:'Control panel (battery monitor, pump switch, tank levels)', x:66, z:50, note:'12 V, small 18 AWG, 3 A'},
  {k:'out120',n:'Outlet under the TV (120 V)',                  x:96, z:52.5, note:'on the wall strip under the TV (its bottom is at 54), above the dish towel hook (98 1/2, 50 up): check the plug clears the towel. Near the sink, so circuit A (GFCI)'},
  {k:'box',   n:'Hot water heater feed (120 V, 20 A, circuit D)', x0:85, x1:87, z0:18, z1:24, note:'junction box beside the hot water tank (87 to 101); 12 AWG, its own breaker; heater is 1440 W'},
  {k:'strip', n:'Soft LED strip, ceiling edge, passenger side run (154 in)', x0:1, x1:pl.cab - 1, z:73, note:'the other long run, same strip and channel, at the top of the wall covering; over the sliding door opening (104 to 155, up to 67 in) the channel carries on along the header at 73 in. Fed through riser B'},
  {k:'sel',   n:'Heater or microwave selector (2 pole, 3 position)', x:71, z:50, note:'yes, a 2 pole switch does this: a double pole, on-off-on (center off) switch or rotary selector rated at least 25 A at 120 V AC (AC rated, not a 12 V switch). Each circuit keeps its own breaker (B 15 A on 14 AWG for the microwave, D 20 A on 12 AWG for the heater); breaker B\u2019s hot feeds the common of one pole, breaker D\u2019s the common of the other; the microwave\u2019s hot leaves pole 1 on the microwave side, the heater\u2019s leaves pole 2 on the heater side, the other terminals stay empty. Microwave position: only the microwave is live; heater position: only the heater; middle: neither. Label it. It sits beside the control panel so you choose before you cook or heat water; the heater only warms the tank while the switch is on its side'},
  {k:'run',   n:'Riser B: 120 V circuits and 12 V branches',   x:73, z0:8, z1:75, note:'down inside the wall behind the planks from the ceiling: 120 V in flexible conduit (12 AWG), 12 V branches (pump, control panel) in a separate loom; branches go sideways behind the planks through notches in the furring'},
]; };

// plumbing shown for reference, drawn in teal with PL numbers so it cannot be mistaken for the electrics
const PLUMB = pl => {
  const rz = 27.5, bz = 62;                          // rz: the band between furring strips S3 (21 1/4) and S4 (30 1/4), inside the 2 in zone (23 1/4 to 29 1/2 up) and above the five oval slots at 25 1/3; bz: the band between S6 (57 1/4) and S7 (66)
  const rx = pl.snookEnd + 2.25, vz = pl.valveZ, sx = pl.toilet ? pl.toilet.x0 / 2 : pl.panW / 2;
  const out = [
    {k:'phead', n:'Shower head', x:pl.headX, z:pl.headZ, lab:'H', note:fr(pl.headZ) + ' in up on a ' + fr(pl.headOut) + ' in arm pointing into the stall, above the shower nook (its top is at ' + fr(pl.sn ? pl.sn.z1 : 54) + ' in); the feed comes down to it from the run at ' + fr(bz) + ' in up'},
    {k:'pvalve', n:'Shower valve (mixer handle)', x:pl.valveX, z:pl.valveZ, lab:'V', note:'at the cab end, above the back of the toilet, just past the end of the shower nook; the hot and cold lines come up beside it at ' + fr(rx) + ' in. The pan is fixed (3 in curb), so nothing moves under it'},
    {k:'ppump', n:'Water pump, under the sink', x0:119, x1:122, z0:12, z1:20, note:'on the sink cabinet’s cab-side end panel, above the fresh tank (top at 10 in), with a service hatch. Its 12 V feed (14 AWG, 10 A, from the fuse block) is the pump circuit on the one-line diagram'},
    {k:'ppath', n:'Hot and cold supply to the shower valve (two 1/2 in PEX lines)', pts:[[120.5, 20.5], [120.5, rz], [rx, rz], [rx, vz - 1.5]], at:[70, rz], note:'cold leaves the pump and runs along the back panel of the sink cabinet (from 123 to 104 that wall is the sliding door, so there is no cavity there: clip it inside the cabinet, behind the hatch), then at 104 goes into the wall cavity behind the covering at ' + fr(rz) + ' in up: between furring strips S3 and S4 (the free band between the 3 1/2 in strips is 23 to 28 1/2 up), in the 2 in zone (23 1/4 to 29 1/2 up) where the steel is only 2 in off the body so there is about 2 1/2 in of room behind the covering, and above the five oval slots at 25 1/3 up. It crosses the pillar at about 98 and goes through a drilled hole in the 3/4 in wall between the shower and the fridge, then up past strips S4 and S5 (drill each, do not notch) beside the end of the shower nook to the valve. The hot line branches off the hot water tank (87 1/4 to 101 1/4, fittings at its back) at about 94 and runs beside the cold one, 1 in apart; foam sleeve on the hot one, and insulation between both lines and the steel'},
    {k:'ppath', n:'Feed from the valve to the shower head', pts:[[rx, vz + 1.5], [rx, bz], [pl.headX, bz], [pl.headX, pl.headZ - 1.2]], at:[(rx + pl.headX) / 2, bz], note:'up beside the nook past furring strip S5 (drill a 3/4 in hole through it, do not notch it), along the band at ' + fr(bz) + ' in up over the nook (between S6 and S7: the free band is 59 to 64 1/4 up) and down to the head; one mixed-water line'},
    {k:'pdrain', n:'Shower drain, through the floor to the grey water tank under the van', x:sx, z:.8, note:'a 1 1/2 in drain in the middle of the standing part of the pan (' + fr(sx) + ' in along, about ' + fr(pl.panD / 2) + ' in out from the wall), the pan floor sloping to it; straight down through the floor, a shallow trap under it, then to the grey tank (30 x 17 x 8 space, position not set) with its vent. The tank has to be lower than the pan'},
  ];
  return out;
};

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
      win: L.win, batt: L.batt, bA: L.bA, bB: L.bB, headX: P.headX, headZ: P.headZ, headOut: P.headOut, valveX: P.valveX, valveZ: P.valveZ, cab: P.cab, ceilF: L.ceilF, panW: P.panW, panD: P.panD, gear: L.gear, toilet: L.toilet, sn: L.sn, wallsOn: P.wallsOn, fwT: P.fwT, hotX: L.hotX, snookEnd: Math.min(29.75, P.panW - 6.25), slatY: L.slatY, slatW: P.slatW, tbl: L.tbl, bedLen: P.bedLen, tableH: P.tableH, cabBot: P.cabBot,
    };
  });
}
async function grabItems(page) {            // the furniture outlines (same positions as wall-map)
  return page.evaluate(() => {
    const P = L.P, ch = P.counterH, f = v => Math.round(v * 100) / 100, a = (x0, x1, z0, z1) => ({ x0: f(x0), x1: f(x1), z0: f(z0), z1: f(z1) });
    const D = [a(0, P.bedLen, 0, P.platform + P.mattress + P.bedBack), a(42, 76, 0, 7.5), a(L.c0, L.c1, 0, L.ceilF), a(L.bA[0], L.bA[1], 0, P.seatH), a(L.bB[0], L.bB[1], 0, P.seatH)];
    if (L.tableLen > 0) D.push(a(L.tbl[0], L.tbl[1], P.tableH - 1.5, P.tableH));
    L.cabs.forEach(c => D.push(a(c[0], c[1], P.cabBot, L.ceilF)));
    if (L.win) D.push(Object.assign(a(L.win.cx0, L.win.cx1, L.win.cz0, L.win.cz1), { win: true }));
    const nkx = Math.min(29.75, P.panW - 6.25), nk0 = nkx - P.snookLen;
    const PS = [a(0, P.panW, 0, L.ceilF), a(nk0, nkx, P.snookTop - P.snookH, P.snookTop), a(L.fr[0], L.fr[1], 8.25, 8.25 + P.fridgeH), a(L.microX[0], L.microX[1], L.microZ[0], L.microZ[1]),
      a(L.cabS, L.sinkE, 0, ch), a(76.5, 103.5, ch + 16, ch + 31.4), a(NK(P)[0], NK(P)[1], ch, ch + P.nookH), a(L.tankX[0], L.tankX[1], P.tankLift, P.tankLift + P.tankH),
      a(L.hotX[0], L.hotX[1], P.hotShelf, P.hotShelf + P.hotH), a(42, 76, 0, 7.5), a(P.doorX, P.doorX + P.slideW, 0, P.slideH)];
    if (L.toilet) PS.push(a(L.toilet.x0, L.toilet.x1, 3.8, 3.8 + L.toilet.z1));
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
const CPL = '#0E7C86', INK = '#1b1a17', C120 = '#B3261E', C12 = '#185FA5', CAC = '#B45309', CLT = '#B8860B';
function symbol(e, X, Y) {
  const o = [], r = 7;
  if (e.k === 'out120') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${C120}" stroke-width="1.8"/><line x1="${x-3}" y1="${y-3}" x2="${x-3}" y2="${y+1}" stroke="${C120}" stroke-width="1.6"/><line x1="${x+3}" y1="${y-3}" x2="${x+3}" y2="${y+1}" stroke="${C120}" stroke-width="1.6"/>`); return [o.join(''), x, y]; }
  if (e.k === 'usb') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${C12}" stroke-width="1.8"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">12</text>`); return [o.join(''), x, y]; }
  if (e.k === 'sw') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-6.5}" y="${y-6.5}" width="13" height="13" rx="2" fill="#fff" stroke="${INK}" stroke-width="1.8"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${INK}">S</text>`); return [o.join(''), x, y]; }
  if (e.k === 'lt') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#FFD84A" stroke="${CLT}" stroke-width="1.8"/>`); return [o.join(''), x, y]; }
  if (e.k === 'plate') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-17}" y="${y-9}" width="34" height="18" rx="3" fill="#fff" stroke="${INK}" stroke-width="1.8"/><rect x="${x-14}" y="${y-5.5}" width="11" height="11" rx="1.5" fill="#fff" stroke="${INK}" stroke-width="1.5"/><text x="${x-8.5}" y="${y+3}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:${INK}">S</text><circle cx="${x+9}" cy="${y}" r="6" fill="#fff" stroke="${C120}" stroke-width="1.6"/><line x1="${x+6.6}" y1="${y-2.6}" x2="${x+6.6}" y2="${y+.8}" stroke="${C120}" stroke-width="1.4"/><line x1="${x+11.4}" y1="${y-2.6}" x2="${x+11.4}" y2="${y+.8}" stroke="${C120}" stroke-width="1.4"/>`); return [o.join(''), x, y]; }
  if (e.k === 'phead' || e.k === 'pvalve') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="8" fill="#D7F0F2" stroke="${CPL}" stroke-width="2.2"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${CPL}">${e.lab}</text>`); return [o.join(''), x, y]; }
  if (e.k === 'ppump') { const xa = X(e.x0), xb = X(e.x1), x = Math.min(xa, xb), w = Math.max(12, Math.abs(xb - xa)), y0 = Y(e.z1), h = 6 * (e.z1 - e.z0); o.push(`<rect x="${x}" y="${y0}" width="${w}" height="${h}" rx="4" fill="#D7F0F2" fill-opacity=".8" stroke="${CPL}" stroke-width="2.2"/><text x="${x + w / 2}" y="${y0 + h / 2 + 3.4}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${CPL}">pump</text>`); return [o.join(''), x + w / 2, y0 + h / 2]; }
  if (e.k === 'ppath') { const pts = e.pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' '); o.push(`<polyline points="${pts}" fill="none" stroke="${CPL}" stroke-width="3.2" stroke-dasharray="9 5" stroke-linejoin="round" opacity=".9"/><polyline points="${e.pts.map(p => (X(p[0]) + 4) + ',' + (Y(p[1]) + 4)).join(' ')}" fill="none" stroke="#B3261E" stroke-width="2" stroke-dasharray="9 5" stroke-linejoin="round" opacity=".55"/>`); return [o.join(''), X(e.at[0]), Y(e.at[1])]; }
  if (e.k === 'pdrain') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="8" fill="#D7F0F2" stroke="${CPL}" stroke-width="2.2"/><line x1="${x}" y1="${y-4}" x2="${x}" y2="${y+14}" stroke="${CPL}" stroke-width="2.4"/><path d="M${x-5} ${y+9} L${x} ${y+16} L${x+5} ${y+9}" fill="none" stroke="${CPL}" stroke-width="2.4"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${CPL}">D</text>`); return [o.join(''), x, y]; }
  if (e.k === 'pvent') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-8}" y="${y-8}" width="16" height="16" rx="8" fill="#D7F0F2" stroke="${CPL}" stroke-width="2.2"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:${CPL}">VT</text>`); return [o.join(''), x, y]; }
  if (e.k === 'wet') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="7" fill="#DCEAF6" stroke="${C12}" stroke-width="1.8" stroke-dasharray="3 2"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">${e.lab}</text>`); return [o.join(''), x, y]; }
  if (e.k === 'sel') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-10}" y="${y-8}" width="20" height="16" rx="3" fill="#fff" stroke="${C120}" stroke-width="2"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:${C120}">M/H</text>`); return [o.join(''), x, y]; }
  if (e.k === 'inlet') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-8}" y="${y-8}" width="16" height="16" rx="3" fill="#FFF1D6" stroke="${CAC}" stroke-width="2"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${CAC}">IN</text>`); return [o.join(''), x, y]; }
  if (e.k === 'panel') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-9}" y="${y-7}" width="18" height="14" rx="2" fill="#fff" stroke="${C12}" stroke-width="1.8"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">M</text>`); return [o.join(''), x, y]; }
  if (e.k === 'strip') { const xa = X(e.x0), xb = X(e.x1), y = Y(e.z), x = Math.min(xa, xb), w = Math.abs(xb - xa); o.push(`<rect x="${x}" y="${y-2.5}" width="${w}" height="5" rx="2.5" fill="#FFD84A" stroke="${CLT}" stroke-width="1.2"/>`); return [o.join(''), x + w / 2, y]; }
  if (e.k === 'box') { const xa = X(e.x0), xb = X(e.x1), x = Math.min(xa, xb), w = Math.max(10, Math.abs(xb - xa)), y0 = Y(e.z1), h = 6 * (e.z1 - e.z0); o.push(`<rect x="${x}" y="${y0}" width="${w}" height="${h}" rx="2" fill="#FFF1D6" fill-opacity=".75" stroke="${CAC}" stroke-width="2"/>`); return [o.join(''), x + w / 2, y0 + h / 2]; }
  if (e.k === 'run') { const x = X(e.x); o.push(`<line x1="${x}" y1="${Y(e.z0)}" x2="${x}" y2="${Y(e.z1)}" stroke="${C12}" stroke-width="3" stroke-dasharray="7 4" opacity=".85"/><line x1="${x+4}" y1="${Y(e.z0)}" x2="${x+4}" y2="${Y(e.z1)}" stroke="${C120}" stroke-width="3" stroke-dasharray="7 4" opacity=".85"/>`); return [o.join(''), x + 2, Y((e.z0 + e.z1) / 2)]; }
  return ['', 0, 0];
}
function wallSVG(list, side, base, furn, plumb) {
  const flip = side === 'P', X = x => +(flip ? 1020 - 6 * x : 50 + 6 * x).toFixed(1), Y = z => +(544 - 6 * z).toFixed(1);
  const o = [], placed = [];
  furn.forEach(it => { const xa = X(it.x0), xb = X(it.x1); o.push(it.win
    ? `<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="#B5D4F4" fill-opacity=".3" stroke="#185FA5" stroke-width="1.6"/><text x="${(xa + xb) / 2}" y="${Y(it.z0) - 6}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#0C447C;paint-order:stroke;stroke:#fff;stroke-width:3px">side window</text>`
    : `<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="none" stroke="${INK}" stroke-opacity=".28" stroke-width="1.2" stroke-dasharray="4 3"/>`); });
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
  const pg = [];
  const prow = (plumb || []).map((e, i) => {
    e.id = 'PL' + (i + 1);
    const [g, cx, cy] = symbol(e, X, Y); pg.push(g);
    let bx = cx + 14, by = cy + 16;
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0] - bx, q[1] - by) < 24); t++) by += 14;
    placed.push([bx, by]);
    pg.push(`<rect x="${bx-15}" y="${by-8}" width="30" height="16" rx="3" fill="#fff" fill-opacity=".95" stroke="${CPL}" stroke-width="1.5"/><text x="${bx}" y="${by+3.8}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${CPL}">${e.id}</text>`);
    const where = e.pts ? `from ${fr(e.pts[0][0])} in, ${fr(e.pts[0][1])} up, to ${fr(e.pts[e.pts.length - 1][0])} in, ${fr(e.pts[e.pts.length - 1][1])} up` : e.x0 != null ? `${fr(e.x0)} to ${fr(e.x1)}, ${fr(e.z0)} to ${fr(e.z1)} up` : `${fr(e.x)} in, ${fr(e.z)} up`;
    return `<tr><td><b class="pid">${e.id}</b></td><td>${esc(e.n)}</td><td>${where}</td><td class="kd">${esc(e.note)}</td></tr>`;
  });
  const svg = `<svg viewBox="0 0 1070 636" role="img" aria-label="${flip ? 'Passenger' : 'Driver'} wall: steel, furring strips, furniture outlines, the electrical items${plumb && plumb.length ? ' and the plumbing in teal' : ''}">${base.inner}<g id="elec${side}">${o.join('')}</g>${pg.length ? `<g id="plumb${side}">${pg.join('')}</g>` : ''}</svg>`;
  const ptable = prow.length ? `<h3 style="color:${CPL}">Plumbing on this wall (teal, for reference: not electrical)</h3><div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${prow.join('')}</tbody></table></div>` : '';
  return { svg, table: `<div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>`, ptable, legend: base.legend };
}

function ceilingSVG(d) {
  const S = 6, X = x => 50 + S * x, Y = y => 56 + S * y, W = 1070, H = 56 + S * 68 + 140;
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
  { const xs = d.lights.map(l => l.x); if (xs.length > 1) o.push(line([[Math.min(...xs), d.lights[0].y], [Math.max(...xs), d.lights[0].y]], CLT, 2.2, '2 3')); }   // the row of ceiling lights
  o.push(`<rect x="${X(RX) - 11}" y="${Y(34) - 8}" width="22" height="16" rx="3" fill="#FFF1D6" stroke="${CAC}" stroke-width="2"/><text x="${X(RX)}" y="${Y(34) + 4}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${CAC}">JB</text>`);
  // the wet bath stall (36 along the wall, 24 out from the passenger wall; wall numbers + 6 from the rear-door edge)
  o.push(`<rect x="${X(6)}" y="${Y(44)}" width="${S * 36}" height="${S * 24}" fill="${C12}" fill-opacity=".07" stroke="${C12}" stroke-width="1.4" stroke-dasharray="5 3"/><text x="${X(6) + 6}" y="${Y(44) + 14}" style="font-size:11px;font-weight:700;fill:${C12}">wet bath stall</text>`);
  // the soft LED strip around the ceiling edge: driver side, across the back, passenger side (about 31 ft in all, fed in three sections)
  { const e = 1.5, cabX = d.P.cab + 6;
    o.push(`<polyline points="${X(cabX)},${Y(e)} ${X(e)},${Y(e)} ${X(e)},${Y(68 - e)} ${X(cabX)},${Y(68 - e)}" fill="none" stroke="#F4C95D" stroke-width="9" stroke-opacity=".55" stroke-linejoin="round"/><polyline points="${X(cabX)},${Y(e)} ${X(e)},${Y(e)} ${X(e)},${Y(68 - e)} ${X(cabX)},${Y(68 - e)}" fill="none" stroke="#B8860B" stroke-width="1.6" stroke-linejoin="round"/>`);
    o.push(`<text x="${X(e) + 8}" y="${Y(e) + 20}" style="font-size:10.5px;font-weight:700;fill:#8a6a00">soft LED strip around the edge</text>`); }
  // lights
  d.lights.forEach((l, i) => { const wet = l.y > d.P.vanW - d.panD && l.x < 6 + d.panW && l.x > 6; o.push(`<circle cx="${X(l.x)}" cy="${Y(l.y)}" r="${Math.max(6, S * d.P.lightD / 2)}" fill="#FFD84A" stroke="${wet ? C12 : CLT}" stroke-width="${wet ? 3 : 1.8}"/>`); if (wet) o.push(`<text x="${X(l.x) + 12}" y="${Y(l.y) + 16}" style="font-size:10.5px;font-weight:700;fill:${C12}">wet-rated (IP65)</text>`); });
  // where the risers meet the walls
  o.push(`<text x="${X(RX) + 16}" y="${Y(0) + 14}" style="font-size:11px;font-weight:700;fill:${INK}">riser A (A/C, 12 V) at ${RX}</text><text x="${X(RX) + 16}" y="${Y(68) - 8}" style="font-size:11px;font-weight:700;fill:${INK}">riser B (120 V, branches) at ${RX}</text>`);
  // legend
  const ly = Y(68) + 66;
  const leg = [[C12, 'dashed blue: 12 V trunk (fuse block feed, 12 AWG)', '8 4', 3], [C120, 'dashed red: 120 V circuits in flexible conduit (12 AWG)', '8 4', 3], [CAC, 'solid orange: A/C feed, 6 AWG, 100 A fuse at the battery', null, 4.5], [CLT, 'dotted yellow: the two ceiling lights (16 AWG, one slat)', '2 3', 2.2], ['#F4C95D', 'pale yellow band: soft LED strip around the edge (14 AWG, its own 10 A circuit)', null, 7]];
  leg.forEach((l, i) => o.push(`<line x1="${X(0)}" y1="${ly + i * 16}" x2="${X(0) + 34}" y2="${ly + i * 16}" stroke="${l[0]}" stroke-width="${l[3]}"${l[2] ? ` stroke-dasharray="${l[2]}"` : ''}/><text x="${X(0) + 42}" y="${ly + i * 16 + 4}" style="font-size:12px;fill:${INK}">${l[1]}</text>`));
  o.push(`<text x="${X(86)}" y="${ly + 4}" style="font-size:12px;fill:${INK}">JB = ceiling junction box (12 V fuse block feed splits here)</text><text x="${X(86)}" y="${ly + 20}" style="font-size:12px;fill:${INK}">grey bands = ribs; dashed squares = the unit footprints on the roof</text><text x="${X(86)}" y="${ly + 36}" style="font-size:12px;fill:${INK}">yellow circles = the two ceiling lights (shower; countertop and sink together; positions from the plan)</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ceiling seen from above: lights, fan, A/C, junction box and wire runs"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

// the high-current cables and fuses to buy: gauges from the plan's own currents and lengths; the drop is computed here (copper, 20 C) so the numbers cannot drift from the table
const AWGR = {'6': .3951, '4': .2485, '2': .1563, '1/0': .0983, '2/0': .0780, '4/0': .0490};   // ohms per 1000 ft
const AWGA = {'6': 75, '4': 95, '2': 130, '1/0': 170, '2/0': 195, '4/0': 260};                    // A, 90 C chassis wiring; 105 C marine cable carries more
function cableTable() {
  const rows = [
    ['Battery + to the Class T fuse and the bus +', '2/0', 168, 1.5, 12.8, 'Class T 250 A, within 7 in of the battery post', 'red 2 ft', 'the whole inverter load goes through it'],
    ['Battery − to the shunt and the bus −', '2/0', 168, 1.5, 12.8, 'none (the shunt, 500 A)', 'black 2 ft', 'the shunt sits on the negative, before the bus'],
    ['Bus to the inverter, + and −', '2/0', 168, 4, 12.8, '250 A on the + (the Class T can serve it if they are within 7 in)', 'red 4.5 ft, black 4.5 ft', '2 ft plus a 2 ft loop so the gear shelf can slide out (use extra-flexible welding cable, which bends tighter); the BELTTT 2000 W draws about 170 A at full load and about 340 A for its 4000 W surge; do not use the 3 ft cables it ships with'],
    ['Alternator side: starter battery to the DC-DC charger, + and −', '2', 65, 17, 13.5, '80 A at the starter battery, within 7 in of its post', 'red 19 ft, black 19 ft', 'about 15 ft in the van plus a 2 ft loop so the gear shelf can slide out; the plan said 4 AWG: that loses 4% over 17 ft, 2 AWG 2.5%; the chassis can be the − only if the LiTime manual says so'],
    ['DC-DC charger to the bus, + and −', '2', 60, 6, 14.0, '80 A at the bus', 'red 7 ft, black 7 ft', '4 ft plus a 2 ft loop for the shelf; the plan said 4 AWG; 2 AWG keeps one size for all the charger runs'],
    ['Shore charger (VEVOR 80 A) to the bus, + and −', '2', 80, 6, 14.6, '100 A at the bus', 'red 7 ft, black 7 ft', '4 AWG carries only about 95 A, which is under the 100 A fuse, so the plan’s 4 AWG is changed to 2 AWG'],
    ['A/C feed, + and −', '6', 58, 12, 12.8, '100 A at the battery', 'red 14 ft, black 14 ft', '6 AWG is what the A/C maker lists for 12 ft; my arithmetic says it loses 4.3%, 4 AWG would lose 2.7%: follow the A/C manual, or use 4 AWG'],
    ['Chassis ground for the hub board and the inverter', '4', 20, 3, 12.8, 'none', 'black 4 ft', 'one short strap from the − bus to the van body']];
  const tr = rows.map(r => { const drop = r[2] * AWGR[r[1]] / 1000 * 2 * r[3], pc = drop / r[4] * 100, over = r[6] && AWGA[r[1]] < r[2];
    return `<tr><td>${esc(r[0])}</td><td class="num"><b>${r[1]}</b></td><td class="num">${r[2]} A</td><td class="num">${r[3]} ft</td><td class="num">${drop.toFixed(2)} V (${pc.toFixed(1)}%)</td><td>${esc(r[5])}</td><td>${esc(r[6])}</td><td class="kd">${esc(r[7])}</td></tr>`; }).join('');
  return `<div class="tw"><table><thead><tr><th>Run</th><th>AWG</th><th>Current</th><th>One way</th><th>Drop</th><th>Fuse</th><th>Buy</th><th>Notes</th></tr></thead><tbody>${tr}</tbody></table></div>
  <p class="lead"><b>Buy in total:</b> about 10 ft red and 10 ft black of 2/0, about 32 ft red and 32 ft black of 2 AWG, about 15 ft red and 15 ft black of 6 AWG (or 4), and 4 ft of 4 AWG black. The drop is the voltage lost in the copper at the full current, one way out and back, from 20 C copper resistance; keep it near 3% for the charger runs and well under that for the short ones.</p>
  <ul><li><b>Cable:</b> tinned copper, fine strand (class K or better, UL 1426 or marine battery cable, 105 C insulation), true AWG with no copper-clad aluminium; red and black. Welding cable is fine if it is tinned or the ends are sealed.</li>
  <li><b>Lugs:</b> tinned copper ring lugs, one per cable end (about 10 in 2/0, 16 in 2 AWG, 6 in 6 AWG, 2 in 4 AWG), each with the hole size of the stud it goes on (the inverter’s, the battery post, the fuse block and the bus bar: check each before buying), crimped with a hydraulic or hammer crimper, then adhesive-lined heat shrink. Do not solder high-current lugs.</li>
  <li><b>Fuses and gear:</b> a Class T holder and 250 A fuse, a 500 A shunt, two bus bars rated 250 A or more, an 80 A fuse and holder at the starter battery, an 80 A and a 100 A for the chargers at the bus, and a 100 A for the A/C at the battery; a cable cutter and a hydraulic crimper (or have a shop crimp the lugs).</li></ul>`;
}
function oneLineSVG() {
  const W = 1070, H = 640, o = [];
  const box = (x, y, w, h, t1, t2, col) => { o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff" stroke="${col || INK}" stroke-width="1.8"/><text x="${x + w / 2}" y="${y + (t2 ? h / 2 - 3 : h / 2 + 4)}" text-anchor="middle" style="font-size:12.5px;font-weight:700;fill:${INK}">${esc(t1)}</text>`); if (t2) o.push(`<text x="${x + w / 2}" y="${y + h / 2 + 12}" text-anchor="middle" style="font-size:11px;fill:#5F5E5A">${esc(t2)}</text>`); };
  const ln = (x1, y1, x2, y2, col, lab, lx, ly, w) => { o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w || 2.4}"/>`); if (lab) o.push(`<text x="${lx}" y="${ly}" text-anchor="middle" style="font-size:11px;fill:${INK}">${esc(lab)}</text>`); };
  // sources (left)
  box(20, 30, 190, 50, 'Shore power inlet', '30 A, 120 V', CAC);
  box(20, 105, 190, 52, 'Shore charger VEVOR 80 A', 'shore side only, 14.6 V lithium', INK);
  box(20, 185, 190, 56, 'Alternator', 'starter battery fuse 80 A', INK);
  box(20, 270, 190, 52, 'DC-DC charger LiTime 60 A', 'on the gear shelf', INK);
  ln(115, 80, 115, 105, C120, '15 A breaker', 170, 98);
  ln(210, 55, 270, 55, C120, '30 A', 240, 48);
  ln(115, 241, 115, 270, C12, '', 0, 0); o.push(`<text x="122" y="259" style="font-size:11px;fill:${INK}">2 AWG, about 15 ft</text>`);
  // the charger output to the battery (2 AWG, 100 A fuse), running down between the left column and the battery
  ln(210, 131, 235, 131, C12, '', 0, 0); ln(235, 131, 235, 346, C12, '', 0, 0); ln(235, 346, 270, 346, C12, '', 0, 0);
  o.push(`<text x="231" y="338" style="font-size:10.5px;fill:${INK}" transform="rotate(-90 231 338)">VEVOR 2 AWG, 100 A fuse</text>`);
  // transfer switch and the inverter (inverter only: no charger, no transfer switch of its own)
  box(270, 30, 200, 60, 'Transfer switch, 30 A', 'shore or inverter, never both', C120);
  box(270, 115, 200, 60, 'Inverter BELTTT 2000 W', 'pure sine, inverter only', CAC);
  ln(370, 115, 370, 90, C120, '', 0, 0);
  // battery + bus
  box(270, 330, 190, 66, 'Battery 280 Ah, 12.8 V', 'lithium assumed (3.6 kWh)', INK);
  ln(115, 322, 115, 362, C12, '', 0, 0); ln(115, 362, 270, 362, C12, '2 AWG, 80 A', 172, 356);
  ln(365, 330, 365, 300, C12, 'Class T 250 A, 2/0 AWG', 440, 322, 4); 
  box(270, 240, 190, 54, '+ bus bar and shunt (500 A)', 'near the battery', INK);
  ln(365, 240, 365, 175, C12, '2/0 AWG, 250 A fuse', 440, 214, 4);
  // 12 V branches (right of the bus)
  const br = [['A/C 12 V, up to 58 A', '6 AWG pair, 100 A fuse', CAC], ['Fuse block: 2 ceiling, 3 cabinet lights', '16 AWG, 5 A', CLT], ['Soft LED strip, about 31 ft in 3 runs', '14 AWG, its own 10 A circuit', CLT], ['Roof fan, up to 2.7 A', '14 AWG, 5 A', C12], ['Water pump, 7 A (under the sink)', '14 AWG, 10 A', C12], ['Control panel and shunt display', '18 AWG, 3 A', C12]];
  br.forEach((b, i) => { const y = 214 + i * 56; ln(460, 267, 540, 267, C12, '', 0, 0); ln(540, 267, 540, y + 20, C12, '', 0, 0); ln(540, y + 20, 600, y + 20, b[2], '', 0, 0, 2.8); box(600, y, 330, 40, b[0], b[1], b[2]); });
  o.push(`<text x="600" y="198" style="font-size:12px;font-weight:700;fill:${C12}">12 V DC circuits (blade fuse block, except the A/C)</text>`);
  // AC side
  ln(470, 60, 600, 60, C120, '', 0, 0);
  box(600, 56, 150, 48, 'AC panel', '30 A main, GFCI', C120);
  o.push(`<text x="540" y="46" style="font-size:12px;font-weight:700;fill:${C120}">120 V AC circuits</text>`);
  [['A  counter outlets, GFCI', '15 A, 12 AWG'], ['B  microwave, its own', '15 A, 12 AWG'], ['C  fridge, TV, dinette outlets', '15 A, 12 AWG'], ['D  water heater 1440 W', '20 A, 12 AWG']].forEach((c, i) => { const y = 16 + i * 0; });
  const ac = [['A  couch, dinette, under-TV outlets (GFCI)', '15 A, 12 AWG'], ['B  microwave, via the selector', '15 A, 12 AWG'], ['C  fridge, its own breaker', '15 A, 12 AWG'], ['D  water heater 1440 W, via the selector', '20 A, 12 AWG']];
  ac.forEach((c, i) => { const x = 770, y = 12 + i * 34; ln(750, 80, 760, 80, C120, '', 0, 0); ln(760, 80, 760, y + 14, C120, '', 0, 0); ln(760, y + 14, x, y + 14, C120, '', 0, 0); o.push(`<rect x="${x}" y="${y}" width="280" height="28" rx="5" fill="#fff" stroke="${C120}" stroke-width="1.5"/><text x="${x + 8}" y="${y + 13}" style="font-size:11.5px;font-weight:700;fill:${INK}">${esc(c[0])}</text><text x="${x + 8}" y="${y + 24}" style="font-size:10.5px;fill:#5F5E5A">${esc(c[1])}</text>`); });
  o.push(`<rect x="600" y="112" width="150" height="58" rx="5" fill="#FFF1D6" stroke="${C120}" stroke-width="1.5"/><text x="610" y="128" style="font-size:11.5px;font-weight:700;fill:${INK}">B and D go through</text><text x="610" y="143" style="font-size:11px;fill:${INK}">one 2 pole, 3 position</text><text x="610" y="158" style="font-size:11px;fill:${INK}">selector (25 A or more)</text>`);
  o.push(`<text x="20" y="${H - 54}" style="font-size:11.5px;fill:#5F5E5A">Fuses sit within 7 in of the battery or bus (Class T for the inverter, 100 A for the A/C). Wire sizes are for the short runs shown (battery to inverter under 3 ft, A/C about 12 ft);</text><text x="20" y="${H - 38}" style="font-size:11.5px;fill:#5F5E5A">the A/C size comes from a related OutEquipPro model. Follow your inverter’s and the A/C maker’s manuals where they differ.</text><text x="20" y="${H - 22}" style="font-size:11.5px;fill:#5F5E5A">One neutral-to-ground bond only: follow the inverter\u2019s manual (the BELTTT\u2019s was not found) and make sure the transfer switch does not create a second one. Have the 120 V side inspected before use.</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="One-line diagram: shore power and alternator charging, battery, inverter, chargers, transfer switch, fuses and circuits"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

function loadTable(d) {
  const P = d.P, Vn = 12.8, ahToKwh = a => a * Vn / 1000, kwhGal = 8.34 * 80 / 3412;
  const batt = P.battAh * Vn / 1000;
  const L = [
    ['Air conditioner, eco', `${fr(P.acEcoA)} A for ${fr(P.acEcoH)} h`, P.acEcoA * P.acEcoH, 'figures from the listing and reviews'],
    ['Fridge, 120 V', 'about 100 W while it runs, assumed 45% of the day', 0.1 * 24 * 0.45 / Vn * 1000, 'your figure of 100 W; the 45% is my assumption for a warm van'],
    ['Inverter idling, on all day for the fridge', 'about 20 W for 24 h', 0.02 * 24 / Vn * 1000, 'assumed; some inverters have a search mode that cuts this to a few watts, but check it still wakes for the fridge'],
    ['2 ceiling lights, 3 under-cabinet lights', 'about 20 W for 4 h', 20 * 4 / Vn, 'assumed LEDs: about 4 W each'],
    ['Roof fan', `${fr(P.fanLowW)} W low, ${fr(P.fanHighW)} W high for ${fr(P.fanHighH)} h`, ((P.fanLowW * (24 - P.fanHighH) + P.fanHighW * P.fanHighH) / 12), 'from the plan'],
    ['Soft LED strip, dimmed', 'about 31 ft at about 3 W a foot, about 30% for 4 h', 94 * .3 * 4 / Vn, 'assumed: a 2700 K strip at about 3 W a foot is about 94 W at full'],
    ['Water pump', 'about 7 A for 20 min', 7 / 3, 'assumed'],
    ['Hot water heater, one full heating', `about ${Math.round(P.hotGal * 10) / 10} gal heated by 80 F`, kwhGal * P.hotGal / .9 * 1000 / Vn, 'from the plan’s formula, 90% efficient'],
    ['Microwave', '1500 W for 12 min', 1500 * .2 / Vn / .9, 'assumed'],
    ['TV', '60 W for 3 h', 60 * 3 / Vn / .9, 'assumed']];
  const tot = L.reduce((s, r) => s + r[2], 0);
  const rows = L.map(r => `<tr><td>${esc(r[0])}</td><td>${esc(r[1])}</td><td class="num">${Math.round(r[2])} Ah</td><td class="num">${ahToKwh(r[2]).toFixed(2)} kWh</td><td class="kd">${esc(r[3])}</td></tr>`).join('');
  return `<div class="tw"><table><thead><tr><th>Load</th><th>Use</th><th>Per day</th><th></th><th>Basis</th></tr></thead><tbody>${rows}<tr class="tot"><td><b>A hot day, everything</b></td><td></td><td class="num"><b>${Math.round(tot)} Ah</b></td><td class="num"><b>${ahToKwh(tot).toFixed(2)} kWh</b></td><td class="kd">the battery holds ${P.battAh} Ah, about ${batt.toFixed(1)} kWh</td></tr></tbody></table></div>
  <p class="lead">That is ${(tot / P.battAh).toFixed(1)} times the battery on a hot day with the A/C on for ${fr(P.acEcoH)} hours, so it needs refilling every day: driving through the alternator charger (the 60 A DC-DC is about 800 W, so 2 hours adds about 1.6 kWh) or shore power (the VEVOR 80 A is about 1.1 kW, so an hour adds about 1.1 kWh). The fridge and the inverter idling are about a quarter of that total: a 12 V fridge would cut it, because the inverter could be switched off. These are estimates to size the system, not a measurement.</p>`;
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
  const Dlist = E_DRIVER(plan), Plist = E_PASS(plan), Dw = wallSVG(Dlist, 'D', baseA, furn.D), Pw = wallSVG(Plist, 'P', baseD, furn.P, PLUMB(plan));
  const selId = (Plist.find(e => e.k === 'sel') || {}).id;

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
  b.id { color: ${C120}; white-space: nowrap; } b.pid { color: #0E7C86; white-space: nowrap; } .kd { color: #5F5E5A; }
  .note { background: #FAF9F5; border: 1px solid #D3D1C7; border-radius: 10px; padding: 10px 14px; color: #3d3b34; font-size: 14px; margin: 0 0 14px; }
  .note ul { margin: 4px 0 0 18px; padding: 0; } .note li { font-size: 14px; line-height: 1.5; }
  a { color: #185FA5; }`;
  const tog = (id, furr, label) => `<div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('${furr}').style.display=this.checked?'':'none'"> Show the furring strips and dots</label><label><input type="checkbox" checked onchange="document.getElementById('${id}').style.display=this.checked?'':'none'"> ${label}</label></div>`;
  const key = `<p class="legend"><span><svg width="16" height="16" viewBox="0 0 16 16" style="display:inline;vertical-align:-3px;width:16px;min-width:0"><circle cx="8" cy="8" r="6.5" fill="#fff" stroke="${C120}" stroke-width="1.8"/></svg> 120 V outlet</span><span>S = switch plate (the couch plate has the switch and two plugs)</span><span style="color:#0E7C86;font-weight:600">teal = plumbing, shown for reference (H = shower head, V = valve, pump)</span><span>M = control panel</span><span>M/H = heater or microwave selector</span><span>IN = shore inlet</span><span style="color:#B8860B">yellow = lights and LED strips</span><span>orange boxes = mounted units</span><span>dashed boxes = furniture (for reference)</span><span style="color:${C12}">blue dashed</span> / <span style="color:${C120}">red dashed</span> = 12 V / 120 V runs</p>`;
  const body = `<div class="wrap">
  <h1>Electrical and lighting layout</h1>
  <p class="lead">A proposal for where the electrics go, drawn on the same steel and furring strips as the wall marking map, with the furniture outlined for reference. Positions are inches from the back mark (0 is 6 in in from the rear-door edge) and up from the floor; the ceiling plan uses inches from the rear-door edge. The steel and strips are the measured drawing; the electrical items are my proposal, so check each one against the real wall and tell me what to move.</p>
  <div class="note"><b>What you chose:</b> a 2000 W inverter, charging from the alternator and from shore power (no solar), a 120 V fridge, and the water pump under the sink. <b>What I assumed (tell me if wrong):</b>
  <ul><li>The battery is lithium, 280 Ah at 12.8 V (about 3.6 kWh), where the plan has it under the couch, 52 to 73 in.</li>
  <li><b>Your equipment:</b> a BELTTT 2000 W inverter (an inverter only: the listings show no charger and no transfer switch), a LiTime 60 A DC-DC charger from the alternator (2 AWG from the starter battery), and a VEVOR 80 A lithium shore charger. All three sit on one pull-out gear shelf over the battery under the couch (the shelf slides out into the aisle on two 18 in slides; every cable to it has a loop for that, see the cable table). Because the inverter has no transfer switch, the AC panel has a 30 A transfer switch that connects either shore power or the inverter, never both, and the shore charger is fed from the shore side only, on its own 15 A breaker (about 11 A at 120 V). With the charger running, a heater or microwave and the fridge could pass the 30 A shore inlet, so the charger is its own circuit and the total is worth watching.</li>
  <li><b>Ceiling lights:</b> only two, one over the shower (wet rated) and one over the countertop and sink together, both on one slat and 2 in clear of the ribs. Everything else is lit from the cabinets, the jar nook and the soft LED strip.</li>
  <li><b>Light switches:</b> by the couch (the light under the cabinet over the middle of the couch), by the dinette on the cab wall (the two lights under the cabinet over the seats, the ceiling light over the countertop and the sink), a small plate at the rear doors (roof fan and the shower light), and the dimmer for the soft strip. Each switch runs its own group, so ordinary 12 V rated switches work: no push buttons or controller are needed.</li>
  <li><b>Under-cabinet lights:</b> one in the middle of the couch, and two over the dinette, each centered over its bench seat and then moved 6 in toward the table, all on the underside of the wall cabinets. They replace the under-cabinet LED strips, the wall reading lights and the single light over the table I had first suggested.</li>
  <li><b>Soft LED lighting:</b> one warm white dimmable strip around the ceiling edge, along the driver side, across the back and along the passenger side (154 + 68 + 154 = 376 in, about 31 ft), in three runs fed separately so none is longer than about 13 ft from its feed. At about 3 W a foot that is about 94 W (8 A) at full, so it has its own 10 A circuit. One switch with a dimmer next to the couch plate.</li>
  <li><b>Outlets:</b> the four 120 V outlets you asked for (couch, over the middle of the dinette table, under the TV, behind the fridge), plus one for the microwave, which cannot share a circuit with them. Everything else is 12 V: the lights, the fan, the pump and the control panel. There are no USB-C or 12 V sockets (you said they are not needed); phones charge from the 120 V outlets.</li>
  <li><b>Wet bath:</b> a wet-rated (IP65) ceiling light over the stall (the exact center is under a rib, so it sits 2 1/2 in toward the cab), and no outlet in the stall (you said no outlet there). The light is at the center of the stall (18 in along the wall, 56 in across from the driver wall). That point falls in the 1 in gap between two slats, so mount the light on a short cross block laid across the gap, or on the nearest slat 2 in to one side. It takes the place of the plan\u2019s first passenger-side light, so there are still six lights.</li>
  <li>The hot water heater (1440 W) and the microwave (about 1500 W) must not run together: that is more than a 2000 W inverter can supply. A 2 pole, 3 position selector switch (off, microwave, heater) makes it impossible: see item ${selId} on the passenger wall.</li>
  <li>All 120 V work is for an electrician to check; I give layout and sizes, not a code review.</li></ul></div>
  <h2>1. One-line diagram</h2>
  <div class="figwrap">${oneLineSVG()}</div>
  <h2>1a. High-current cables and fuses to buy</h2>
  ${cableTable()}
  <h2>2. Driver side wall</h2>
  ${tog('elecD', 'furr', 'Show the electrical items')}
  <div class="figwrap">${Dw.svg}</div>
  ${key}${Dw.table}
  <h2>3. Passenger side wall</h2>
  ${tog('elecP', 'furrP', 'Show the electrical items')}
  <div class="figwrap">${Pw.svg}</div>
  <div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('plumbP').style.display=this.checked?'':'none'"> Show the plumbing (teal)</label></div>
  ${key}${Pw.table}${Pw.ptable}
  <h2>4. Ceiling: lights, fan, A/C and the wire runs</h2>
  <p class="lead">Six lights in two rows (positions from the plan), each row on its own slat. Risers A and B stand at 79 in from the rear-door edge (73 on the wall maps), in the bay between the ribs at 61 and 97. Every rib the cables cross needs a grommeted hole: use any factory holes first, and keep to the web of the rib, not the flange.</p>
  <div class="figwrap">${ceilingSVG(plan)}</div>
  <h2>5. What it adds up to</h2>
  ${loadTable(plan)}
  <h2>6. Order of work</h2>
  <div class="note"><ul>
  <li>Before the walls and ceiling are covered: run the risers, the ceiling trunk and every branch, with grommets in all steel and the 12 V and 120 V in separate looms (at least 2 in apart, crossing at right angles). This is the rough-in step of the build order.</li>
  <li>With the furring strips: fix the electrical boxes to blocking between the strips, and add the blocking behind the hub board, the switch plates and the outlets before the planks go on.</li>
  <li>Last: the hub board and fuses, the inverter and the two chargers, the transfer switch, the lights and the plates, after the covering is up.</li>
  <li>Test every circuit with a meter before you connect the battery, and test the GFCI outlets with the button.</li></ul></div>
  <p class="lead" style="margin-top:14px"><a href="interactive.html">Back to the interactive plan</a> &middot; <a href="wall-map.html">Wall marking map</a></p>
  </div>`;
  const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Electrical layout</title><style>${style}</style></head><body>${body}</body></html>`;
  fs.writeFileSync(__dirname + '/../electric.html', doc);
  if (!process.env.SC) return console.log('electric.html', doc.length);
  fs.mkdirSync(process.env.SC + '/elec', {recursive: true});
  const frag = `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Electrical Layout</title>\n<style>${style}</style>\n${body.replace('<a href="interactive.html">', '<a href="https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs" target="_blank" rel="noopener">').replace('<a href="wall-map.html">', '<a href="https://claude.ai/artifact/1quE178yLUJmgmSuhm626H" target="_blank" rel="noopener">')}\n`;
  fs.writeFileSync(process.env.SC + '/elec/index.html', frag);
  console.log('electric.html', doc.length, 'driver', E_DRIVER(plan).length, 'pass', E_PASS(plan).length);
})();
