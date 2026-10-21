'use strict';
/* ================= sizes ================= */
// k = key, g = group, l = label, d = default, s = step, a/b = min/max, t = type (n number, c checkbox, s select)
const PD = [
  { k: 'cab', g: 'Van', l: 'Cab wall, from the back', d: 154, s: .5, a: 100, b: 200 },
  { k: 'vanW', g: 'Van', l: 'Inside width', d: 68, s: .5, a: 50, b: 90 },
  { k: 'ceil', g: 'Van', l: 'Ceiling height at the wall (bare, to the rib)', d: 75.5, s: .5, a: 60, b: 90 },
  { k: 'bedLen', g: 'Bed / couch', l: 'Length', d: 74, s: .5, a: 40, b: 120 },
  { k: 'bedD', g: 'Bed / couch', l: 'Depth, closed (the couch on its base)', d: 26, s: .5, a: 15, b: 40 },
  { k: 'bedBack', g: 'Bed / couch', l: 'Leaf width (flips out in front; = back cushion length)', d: 20, s: .5, a: 0, b: 40 },
  { k: 'platform', g: 'Bed / couch', l: 'Seat base (deck 3/4 in lower; the leaf folds onto it)', d: 14, s: .5, a: 6, b: 30 },
  { k: 'mattress', g: 'Bed / couch', l: 'Seat and back cushion thickness', d: 6, s: .5, a: 2, b: 12 },
  { k: 'legIn', g: 'Bed / couch', l: 'Legs set in from the leaf free edge', d: 3, s: .5, a: 0, b: 10 },
  { k: 'closetW', g: 'Closet', l: 'Width', d: 15, s: .25, a: 8, b: 40 },
  { k: 'closetD', g: 'Closet', l: 'Depth', d: 25, s: .5, a: 10, b: 40 },
  { k: 'rodHi', g: 'Closet', l: 'Upper rod, up from floor', d: 71, s: .5, a: 40, b: 85 },
  { k: 'rodLo', g: 'Closet', l: 'Lower rod, up from floor', d: 36, s: .5, a: 10, b: 70 },
  { k: 'split', g: 'Closet', l: 'Two doors split at', d: 38, s: .5, a: 20, b: 60 },
  { k: 'hinge', g: 'Closet', l: 'Door hinges on the', d: 'rear', t: 's', o: [['rear', 'bed side'], ['cab', 'dinette side']] },
  { k: 'openAng', g: 'Closet', l: 'Doors open to (degrees)', d: 90, s: 5, a: 30, b: 180 },
  { k: 'benchLen', g: 'Dinette', l: 'Bench length', d: 19.5, s: .5, a: 10, b: 40 },
  { k: 'benchD', g: 'Dinette', l: 'Bench depth', d: 30, s: .5, a: 15, b: 45 },
  { k: 'seatH', g: 'Dinette', l: 'Seat height', d: 17.5, s: .5, a: 10, b: 26 },
  { k: 'backH', g: 'Dinette', l: 'Backrest top', d: 38, s: .5, a: 20, b: 50 },
  { k: 'pillowT', g: 'Dinette', l: 'Backrest cushion thickness (lies on the lowered table)', d: 2.9, s: .1, a: 1, b: 8 },
  { k: 'tableAuto', g: 'Dinette', l: 'Table fills the space between the benches', d: true, t: 'c', f: 'tableLen' },
  { k: 'tableLen', g: 'Dinette', l: 'Table length', d: 26, s: .5, a: 10, b: 70 },
  { k: 'tableD', g: 'Dinette', l: 'Table depth', d: 30, s: .5, a: 10, b: 45 },
  { k: 'tableH', g: 'Dinette', l: 'Table height', d: 29, s: .5, a: 20, b: 40 },
  { k: 'cabBot', g: 'Wall cabinets', l: 'Bottom, up from floor', d: 61, s: .5, a: 40, b: 80 },
  { k: 'cabBackIn', g: 'Wall cabinets', l: 'Set a solid back of the cabinets in from the wall (0 = open backs: the sides are cut to follow the leaning wall)', d: 0, s: .5, a: 0, b: 8 },
  { k: 'cabDepth', g: 'Wall cabinets', l: 'Depth', d: 14, s: .5, a: 6, b: 24 },
  { k: 'doorH', g: 'Wall cabinets', l: 'Door height (3 doors a side, widths follow the cabinet)', d: 12, s: .5, a: 6, b: 24 },
  { k: 'panW', g: 'Passenger side', l: 'Shower pan length', d: 36, s: .5, a: 20, b: 50 },
  { k: 'panD', g: 'Passenger side', l: 'Shower pan depth', d: 24, s: .5, a: 16, b: 36 },
  { k: 'fridgeW', g: 'Passenger side', l: 'Fridge width', d: 22, s: .5, a: 14, b: 30 },
  { k: 'fridgeD', g: 'Passenger side', l: 'Fridge depth', d: 19, s: .5, a: 12, b: 26 },
  { k: 'fridgeH', g: 'Passenger side', l: 'Fridge height', d: 48, s: .5, a: 20, b: 66 },
  { k: 'counterH', g: 'Passenger side', l: 'Counter height', d: 38, s: .5, a: 30, b: 44 },
  { k: 'cabD', g: 'Passenger side', l: 'Cabinet depth', d: 21, s: .5, a: 12, b: 30 },
  { k: 'flatLen', g: 'Passenger side', l: 'Straight part of the cabinet', d: 30, s: .5, a: 10, b: 70 },
  { k: 'sinkD', g: 'Passenger side', l: 'Depth at the sink end (includes the 3/4 in door)', d: 15.75, s: .5, a: 10, b: 24 },
  { k: 'angLen', g: 'Passenger side', l: 'Length of the angled part of the counter front', d: 15, s: .5, a: 3, b: 40 },
  { k: 'sinkW', g: 'Passenger side', l: 'Sink cabinet width', d: 20, s: .5, a: 12, b: 40 },
  { k: 'slideW', g: 'Passenger side', l: 'Sliding door opening width', d: 51, s: .5, a: 30, b: 70 },
  { k: 'slideH', g: 'Passenger side', l: 'Sliding door opening height', d: 67, s: .5, a: 40, b: 76 },
  { k: 'doorX', g: 'Passenger side', l: 'Sliding door starts at', d: 104, s: .5, a: 80, b: 150 },
  { k: 'flapAuto', g: 'Fold-out table and foot ledge', l: 'Length fits the entry', d: true, t: 'c', f: 'flapLen' },
  { k: 'flapGap', g: 'Fold-out table and foot ledge', l: 'Gap left to the cab wall', d: 2, s: .5, a: 0, b: 10 },
  { k: 'flapLen', g: 'Fold-out table and foot ledge', l: 'Length', d: 29, s: .5, a: 8, b: 60 },
  { k: 'flapD', g: 'Fold-out table and foot ledge', l: 'Depth', d: 15, s: .5, a: 8, b: 30 },
  { k: 'microIn', g: 'Fold-out table and foot ledge', l: 'Microwave: set its back in from the passenger wall (the wall leans in, about 2 1/2 in at its top)', d: 2.5, s: .5, a: 0, b: 8 },
  { k: 'cabSeatH', g: 'Fold-out table and foot ledge', l: 'Cab passenger seat: top of the cushion, up from the floor', d: 17, s: .5, a: 10, b: 30 },
  { k: 'cabSeatOut', g: 'Fold-out table and foot ledge', l: 'Cab passenger seat: how far the cushion sticks out past the cab wall into the living area (the back does not)', d: 1, s: .5, a: 0, b: 10 },
  { k: 'cabSeatFwd', g: 'Fold-out table and foot ledge', l: 'Cab passenger seat pulled all the way forward: the cushion rear edge is this far in front of the cab wall', d: 6, s: .5, a: 0, b: 20 },
  { k: 'cabSeatW', g: 'Fold-out table and foot ledge', l: 'Cab passenger seat cushion: width', d: 20, s: .5, a: 10, b: 30 },
  { k: 'cabSeatD', g: 'Fold-out table and foot ledge', l: 'Cab passenger seat cushion: depth (front to back)', d: 19, s: .5, a: 10, b: 30 },
  { k: 'flapH', g: 'Fold-out table and foot ledge', l: 'Height', d: 29, s: .5, a: 20, b: 40 },
  { k: 'ledgeOff', g: 'Fold-out table and foot ledge', l: 'Foot ledge: distance from the cabinet end to where the foot platform starts (0 = it starts at the end, where it is hinged)', d: 0, s: .5, a: 0, b: 25 },
  { k: 'ledgeLen', g: 'Fold-out table and foot ledge', l: 'Foot ledge: length of the foot platform (it ends this far from the cabinet end when the distance above is 0)', d: 13, s: .5, a: 4, b: 20 },
  { k: 'ledgeH', g: 'Fold-out table and foot ledge', l: 'Foot ledge top, up from floor', d: 8.5, s: .5, a: 3, b: 20 },
  { k: 'tankAuto', g: 'Water tanks', l: 'Fresh water tank fills the floor space to the sink end', d: false, t: 'c', f: 'tankLen' },
  { k: 'tankLen', g: 'Water tanks', l: 'Fresh water tank length', d: 41, s: .5, a: 10, b: 70 },
  { k: 'tankD', g: 'Water tanks', l: 'Fresh water tank depth (out from the wall)', d: 10, s: .5, a: 4, b: 20 },
  { k: 'tankH', g: 'Water tanks', l: 'Fresh water tank height', d: 15.5, s: .5, a: 6, b: 24 },
  { k: 'hotGap', g: 'Water tanks', l: 'Clear space each side of the hot water tank', d: 6, s: .5, a: 0, b: 20 },
  { k: 'hotL', g: 'Water tanks', l: 'Hot water tank: how much water it holds (liters; 15 L is about 4 gal; its 14 x 14 x 13 in size is the outside of the heater)', d: 15, s: .5, a: 2, b: 80 },
  { k: 'hotEmptyLb', g: 'Water tanks', l: 'Hot water tank weight empty (lb)', d: 2, s: .5, a: 0, b: 60 },
  { k: 'hotShelf', g: 'Water tanks', l: 'Hot water tank height off the floor (0 = on the floor; 7.5 = on a shelf over the wheel well, right after the fridge platform)', d: 7.5, s: .5, a: 0, b: 30 },
  { k: 'hotW', g: 'Water tanks', l: 'Hot water tank length along the wall', d: 14, s: .5, a: 6, b: 18 },
  { k: 'hotD', g: 'Water tanks', l: 'Hot water tank depth (out from the wall)', d: 14, s: .5, a: 6, b: 20 },
  { k: 'hotH', g: 'Water tanks', l: 'Hot water tank height', d: 13, s: .5, a: 8, b: 34 },
  { k: 'leanOn', g: 'Walls', l: 'The walls lean in toward the roof (checks use the measurements below)', d: true, t: 'c' },
  { k: 'leanZ1', g: 'Walls', l: 'Lean: lower measurement, height up from the floor', d: 47, s: .5, a: 20, b: 76 },
  { k: 'leanW1', g: 'Walls', l: 'Lean: inside width at that height', d: 67, s: .25, a: 50, b: 80 },
  { k: 'leanZ2', g: 'Walls', l: 'Lean: upper measurement, height up from the floor', d: 64, s: .5, a: 30, b: 80 },
  { k: 'leanW2', g: 'Walls', l: 'Lean: inside width at that height', d: 64, s: .25, a: 40, b: 80 },
  { k: 'roofWallH', g: 'Walls', l: 'Roof: height from the floor to the rib along the wall', d: 75.5, s: .25, a: 60, b: 90 },
  { k: 'roofMidH', g: 'Walls', l: 'Roof: height from the floor to the rib in the middle', d: 80, s: .25, a: 60, b: 95 },
  { k: 'wallOn', g: 'Walls', l: 'Cover the walls (birch plywood on the furring)', d: true, t: 'c' },
  { k: 'wallSub', g: 'Walls', l: 'Take the covering thickness off the inside width (leave off if the width was measured to the covered wall)', d: false, t: 'c' },
  { k: 'wallT', g: 'Walls', l: 'Covering thickness', d: .125, s: .125, a: .125, b: .75 },
  { k: 'wallDens', g: 'Walls', l: 'Wood density (lb per cu ft; birch about 41, cedar about 23)', d: 41, s: 1, a: 15, b: 60 },
  { k: 'sheetW', g: 'Walls', l: 'Sheet width (runs floor to ceiling)', d: 48, s: 1, a: 12, b: 60 },
  { k: 'sheetH', g: 'Walls', l: 'Sheet height', d: 96, s: 1, a: 24, b: 120 },
  { k: 'wallSpan', g: 'Walls', l: 'Most the covering may span between furring strips', d: 16, s: 1, a: 6, b: 32 },
  { k: 'ribList', g: 'Roof ribs', l: 'Rib positions along the roof: inches from the back edge (rear doors), separated by commas', d: '21.75, 37.875, 58.375, 97.375, 126.375', t: 'x' },
  { k: 'ribDepth', g: 'Roof ribs', l: 'Rib depth (how far the ribs hang below the steel roof)', d: 2, s: .25, a: .5, b: 6 },
  { k: 'ribW', g: 'Roof ribs', l: 'Rib width (the flange along the van)', d: 2.75, s: .125, a: .5, b: 8 },
  { k: 'ribRef', g: 'Roof ribs', l: 'The positions above are', d: 'back', t: 's', o: [['back', 'the edge of each rib nearest the back'], ['center', 'the middle of each rib'], ['front', 'the edge of each rib nearest the cab']] },
  { k: 'liningOn', g: 'Ceiling', l: 'Cover the ceiling (plywood, then slats)', d: true, t: 'c' },
  { k: 'ceilLen', g: 'Ceiling', l: 'Ceiling length being covered (rear doors to cab wall)', d: 160, s: 1, a: 40, b: 220 },
  { k: 'ceilW', g: 'Ceiling', l: 'Ceiling width being covered (the flat part, measured wall to wall; centered in the van)', d: 62, s: 1, a: 20, b: 90 },
  { k: 'plyT', g: 'Ceiling', l: 'Plywood thickness', d: .25, s: .125, a: .125, b: 1 },
  { k: 'slatW', g: 'Ceiling', l: 'Slat width', d: 3, s: .25, a: 1, b: 8 },
  { k: 'slatT', g: 'Ceiling', l: 'Slat thickness', d: 1, s: .125, a: .25, b: 3 },
  { k: 'slatGap', g: 'Ceiling', l: 'Gap between slats', d: 1, s: .25, a: 0, b: 6 },
  { k: 'slatAuto', g: 'Ceiling', l: 'Slats as long as the whole ceiling (no joints)', d: true, t: 'c', f: 'slatLen' },
  { k: 'slatLen', g: 'Ceiling', l: 'Slat length', d: 160, s: 1, a: 12, b: 220 },
  { k: 'lightN', g: 'Ceiling', l: 'Round lights in the ceiling (count)', d: 6, s: 1, a: 0, b: 24 },
  { k: 'lightRows', g: 'Ceiling', l: 'Rows of lights along the ceiling', d: 2, s: 1, a: 1, b: 4 },
  { k: 'lightD', g: 'Ceiling', l: 'Light diameter (mounted on a slat)', d: 2, s: .25, a: 1, b: 8 },
  { k: 'fanX', g: 'Ceiling', l: 'Shower fan cutout: along the van (from the back)', d: 13.25, s: .5, a: 0, b: 220 },
  { k: 'fanY', g: 'Ceiling', l: 'Shower fan cutout: across (from the driver wall)', d: 46, s: .5, a: 0, b: 90 },
  { k: 'fanUnit', g: 'Ceiling', l: 'Shower fan unit on the roof: square footprint (2012 F36AR exhaust fan: 17.7 x 17.7 x 6.4 tall)', d: 17.75, s: .25, a: 6, b: 40 },
  { k: 'fanW', g: 'Ceiling', l: 'Shower fan cutout: square size', d: 14, s: .25, a: 4, b: 30 },
  { k: 'acX', g: 'Ceiling', l: 'Air conditioning cutout: along the van (from the back)', d: 49.5, s: .5, a: 0, b: 220 },
  { k: 'acY', g: 'Ceiling', l: 'Air conditioning cutout: across (from the driver wall)', d: 34, s: .5, a: 0, b: 90 },
  { k: 'acUnit', g: 'Ceiling', l: 'Air conditioner unit on the roof: square footprint (OutEquip 12 V cooling-only: 28.3 x 28.3 x 6.3 tall, 45 lb on the listing)', d: 28.25, s: .25, a: 10, b: 50 },
  { k: 'acW', g: 'Ceiling', l: 'Air conditioning cutout: square size', d: 14.25, s: .25, a: 4, b: 30 },
  { k: 'battAh', g: 'Power', l: 'Battery capacity (Ah at 12 V)', d: 280, s: 10, a: 50, b: 800 },
  { k: 'acTurboA', g: 'Power', l: 'Air conditioner current in turbo (A at 12 V; the listing says up to 58)', d: 58, s: 1, a: 5, b: 120 },
  { k: 'acEcoA', g: 'Power', l: 'Air conditioner current in eco or sleep (A at 12 V; the listing says 21 and up, reviews 16 to 29)', d: 21, s: 1, a: 2, b: 80 },
  { k: 'acEcoH', g: 'Power', l: 'Hours a day the air conditioner runs in eco', d: 8, s: .5, a: 0, b: 24 },
  { k: 'fanLowW', g: 'Power', l: 'Shower fan power on low (W, 12 V DC)', d: 3, s: 1, a: 0, b: 100 },
  { k: 'fanHighW', g: 'Power', l: 'Shower fan power on high (W, 12 V DC)', d: 32, s: 1, a: 0, b: 200 },
  { k: 'fanHighH', g: 'Power', l: 'Hours a day the fan runs on high (the rest of the day is low)', d: 1, s: .5, a: 0, b: 24 },
  { k: 'heaterW', g: 'Power', l: 'Hot water heater power (W, 120 V)', d: 1440, s: 40, a: 200, b: 3000 }
];
const DEF = {}; PD.forEach(p => DEF[p.k] = p.d);
let P = Object.assign({}, DEF);

/* ================= helpers ================= */
const $ = s => document.querySelector(s);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const f1 = n => String(Math.round(n * 10) / 10);
function fmt(n) {
  const neg = n < 0; n = Math.abs(n);
  let w = Math.floor(n + 1e-9), fr = Math.round((n - w) * 8);
  if (fr === 8) { w++; fr = 0; }
  const F = ['', '1/8', '1/4', '3/8', '1/2', '5/8', '3/4', '7/8'][fr];
  const s = fr ? (w ? w + ' ' + F : F) : String(w);
  return (neg ? '-' : '') + s;
}
const COL = { P: '#534AB7', G: '#444441', K: '#993556', T: '#0F6E56', C: '#993C1D', B: '#8A5A00', W2: '#8A6B4D', BL: '#185FA5' };
const HALO = 'paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-opacity:.85';
function T(x, y, s, o) {
  o = o || {};
  const size = o.size || 12, fill = o.fill || '#2C2C2A', anchor = o.anchor || 'middle', w = o.w || 400, halo = o.halo !== false;
  return `<text x="${f1(x)}" y="${f1(y)}" text-anchor="${anchor}"${o.op != null && o.op < 1 ? ` opacity="${f1(o.op)}"` : ''} style="font-size:${size}px;font-weight:${w};fill:${fill};${halo ? HALO : ''}">${s}</text>`;
}
function R(x, y, w, h, o) {
  o = o || {};
  return `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(Math.max(0, w))}" height="${f1(Math.max(0, h))}" rx="${o.rx || 0}" fill="${o.fill || 'none'}" fill-opacity="${o.fo == null ? 1 : o.fo}" stroke="${o.stroke || 'none'}" stroke-width="${o.sw || 1.5}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}${o.so != null ? ` stroke-opacity="${o.so}"` : ''}${o.op != null && o.op < 1 ? ` opacity="${o.op}"` : ''}/>`;
}
function Ln(x1, y1, x2, y2, o) {
  o = o || {};
  return `<line x1="${f1(x1)}" y1="${f1(y1)}" x2="${f1(x2)}" y2="${f1(y2)}" stroke="${o.stroke || '#444441'}" stroke-width="${o.sw || 1.5}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}${o.so != null ? ` stroke-opacity="${o.so}"` : ''}${o.cap ? ` stroke-linecap="${o.cap}"` : ''}${o.mk ? ' marker-start="url(#arq)" marker-end="url(#arq)"' : ''}/>`;
}
function Poly(pts, o) {
  o = o || {};
  return `<polygon points="${pts.map(p => f1(p[0]) + ',' + f1(p[1])).join(' ')}" fill="${o.fill || 'none'}" fill-opacity="${o.fo == null ? 1 : o.fo}" stroke="${o.stroke || 'none'}" stroke-width="${o.sw || 1.5}"${o.dash ? ` stroke-dasharray="${o.dash}"` : ''}${o.join ? ` stroke-linejoin="${o.join}"` : ''}/>`;
}
// clickable group: ids is a comma list of things to toggle. The invisible rect (hit) keeps the whole closed area clickable.
function MV(ids, inner, hit) {
  return `<g class="mv" data-act="${ids}"><title>Click to open or close</title>${hit || ''}${inner}</g>`;
}
const HITR = (x, y, w, h) => `<rect x="${f1(x)}" y="${f1(y)}" width="${f1(Math.max(0, w))}" height="${f1(Math.max(0, h))}" fill="#000" fill-opacity="0"/>`;

/* ================= layout (everything derived from the sizes) ================= */
function layout(P0) {
  // the wall covering takes its thickness off each side of the inside width, only if the 'take it off' box is on
  const P = Object.assign({}, P0, { vanW: P0.vanW - (P0.wallOn && P0.wallSub ? 2 * P0.wallT : 0) });
  const L = { P };
  L.c0 = P.bedLen; L.c1 = P.bedLen + P.closetW;
  L.bA = [L.c1, L.c1 + P.benchLen]; L.bB = [P.cab - P.benchLen, P.cab];
  L.gap = L.bB[0] - L.bA[1];
  L.tableLen = P.tableAuto ? Math.max(0, L.gap) : P.tableLen;
  L.spare = L.gap - L.tableLen;
  const tx = L.bA[1] + Math.max(0, L.spare / 2);
  L.tbl = [tx, tx + L.tableLen];
  L.tableLow = Math.max(3, P.seatH - P.pillowT);
  L.cabs = [[0, P.bedLen], [L.c1, P.cab]];
  L.doors = [];
  L.cabs.forEach((c, ci) => {
    const len = c[1] - c[0], w = Math.max(1, (len - 0.5) / 3);
    for (let i = 0; i < 3; i++) { const x0 = c[0] + 0.125 + i * (w + 0.125); L.doors.push({ id: 'dc' + (ci * 3 + i), x0, x1: x0 + w, w }); }
  });
  L.doorZ = [P.cabBot + 0.5, P.cabBot + 0.5 + P.doorH];
  L.batt = [L.c0 - 1 - 21, L.c0 - 1];
  L.pan = P.panW; L.fr = [P.panW, P.panW + P.fridgeW]; L.cabS = L.fr[1];
  L.angS = L.cabS + P.flatLen; L.angLen = P.cabD > P.sinkD ? P.angLen : 0;
  L.slope = L.angLen > 0 ? (P.cabD - P.sinkD) / L.angLen : 0.4;
  L.sinkS = L.angS + L.angLen; L.sinkE = L.sinkS + P.sinkW;
  L.entry = P.cab - L.sinkE;
  L.flapLen = P.flapAuto ? Math.max(1, L.entry - P.flapGap) : P.flapLen;
  // the sink cabinet is open to the area beside it, so the fresh water tank sits on the floor at the sink end (against the cab-side end panel);
  // the hot water tank is on the floor next to the wheel well (which ends at 76 in), between the well and the fresh tank, with up to hotGap in clear each side
  const endX = L.sinkE - .75, wellEnd = 76;
  if (P.tankAuto) { L.hotX = [wellEnd + P.hotGap, wellEnd + P.hotGap + P.hotW]; L.tankX = [L.hotX[1] + P.hotGap, endX]; }
  else { L.tankX = [endX - P.tankLen, endX]; const gap = Math.max(0, Math.min(P.hotGap, (L.tankX[0] - wellEnd - P.hotW) / 2)); L.hotX = [wellEnd + gap, wellEnd + gap + P.hotW]; }
  if (P.hotShelf > .5) L.hotX = [L.fr[1] + 1.5, L.fr[1] + 1.5 + P.hotW]; // on a shelf over the wheel well, 1 1/2 in past the fridge platform
  L.tankLen = L.tankX[1] - L.tankX[0];
  L.hotGal = P.hotL / 3.78541; // the hot water tank is given in liters
  {
    // the shelves under the drawers: each column's shelf sits half an inch over whatever is under it (a tank or the wheel well, 7.5)
    const dm = L.cabS + 14.75, hotTopZ = P.hotShelf + P.hotH, ov = (x0, x1, a, b) => x1 > a && x0 < b;
    const overCab = ov(L.hotX[0], L.hotX[1], dm + .9, dm + 14), overBack = ov(L.hotX[0], L.hotX[1], L.cabS + 1.25, dm - .5);
    const freshCab = ov(L.tankX[0], L.tankX[1], dm + .9, dm + 14), freshBack = ov(L.tankX[0], L.tankX[1], L.cabS + 1.25, dm - .5);
    L.cabShelf = Math.max(7.5, overCab ? hotTopZ : 0, freshCab ? P.tankH : 0) + .5;
    L.backShelf = Math.max(7.5, overBack ? hotTopZ : 0, freshBack ? P.tankH : 0) + .5;
  }
  L.hotY = [0, P.hotD];
  // ceiling covering: plywood against the roof, slats on it; everything that reaches the ceiling stops at the finished ceiling
  // wall lean from two width measurements: each wall comes in k per inch of height above where it stops being vertical (found from the full width)
  L.leanK = Math.max(0, (P.leanW1 - P.leanW2) / 2 / Math.max(.1, P.leanZ2 - P.leanZ1));
  L.leanStart = L.leanK > 0 ? P.leanZ1 - Math.max(0, P.vanW - P.leanW1) / 2 / L.leanK : 1e9;
  L.leanAt = z => P.leanOn && z > L.leanStart ? L.leanK * (z - L.leanStart) : 0;
  // the roof is an arc from the wall tops (rib height at the wall) up to the middle rib; roofZ(y) is its height y in from the driver wall
  {
    const zw = P.roofWallH, c = P.vanW - 2 * L.leanAt(zw), sg = P.roofMidH - zw, R = sg > .01 ? (c * c / 4 + sg * sg) / (2 * sg) : 1e9;
    L.roofW = c; L.roofR = R; L.roofSag = Math.max(0, sg);
    L.roofZ = y => { const d = Math.min(Math.abs(y - P.vanW / 2), c / 2); return zw + (R > 1e8 ? 0 : Math.sqrt(R * R - d * d) - Math.sqrt(R * R - c * c / 4)); };
    L.roofTilt = y => R > 1e8 ? 0 : Math.atan(Math.min(Math.abs(y - P.vanW / 2), c / 2) / Math.sqrt(R * R - Math.pow(Math.min(Math.abs(y - P.vanW / 2), c / 2), 2))) * 180 / Math.PI;
  }
  L.ribs = String(P.ribList || '').split(/[\s,;]+/).map(parseFloat).filter(v => isFinite(v) && v >= 0 && v <= P.ceilLen + 20).sort((a, b) => a - b);
  L.ribBands = L.ribs.map(r => P.ribRef === 'center' ? [r - P.ribW / 2, r + P.ribW / 2] : P.ribRef === 'front' ? [r - P.ribW, r] : [r, r + P.ribW]);
  L.ledgeTot = P.ledgeOff + P.ledgeLen;
  L.lining = P.liningOn ? P.plyT + P.slatT : 0;
  L.ceilF = P.ceil - L.lining;
  L.slatLen = P.slatAuto ? P.ceilLen : P.slatLen;
  L.nSlats = Math.max(0, Math.floor((P.ceilW + P.slatGap) / (P.slatW + P.slatGap)));
  // slat rows across the width (centered), the lights (each row of lights is mounted on the slat nearest its row, centered on it, so every slat still runs the whole length except where a cutout crosses it), and the cutouts
  {
    const n = L.nSlats, used = n * P.slatW + Math.max(0, n - 1) * P.slatGap, m = (P.ceilW - used) / 2;
    L.ceilOff = (P.vanW - P.ceilW) / 2; // the flat part is centered in the van; every ceiling y below is across from the driver wall
    L.slatY = []; for (let k = 0; k < n; k++) L.slatY.push(L.ceilOff + m + k * (P.slatW + P.slatGap));
    L.slatOut = new Set(); L.lights = []; L.chanY = [];
    const rows = Math.max(1, Math.round(P.lightRows)), N = Math.max(0, Math.round(P.lightN));
    for (let r = 0; r < rows; r++) {
      const cnt = Math.floor(N / rows) + (r < N % rows ? 1 : 0); if (cnt < 1) continue;
      const target = L.ceilOff + P.ceilW * (r + 1) / (rows + 1); let y = target;
      if (P.liningOn && n > 0) { let best = 0, bd = 1e9; L.slatY.forEach((sy, k) => { const d = Math.abs(sy + P.slatW / 2 - target); if (d < bd) { bd = d; best = k; } }); y = L.slatY[best] + P.slatW / 2; L.chanY.push(y); }
      for (let c = 0; c < cnt; c++) L.lights.push({ x: P.ceilLen * (c + .5) / cnt, y });
    }
    L.fan = { x: P.fanX, y: P.fanY, w: P.fanW, nm: 'shower fan', u: P.fanUnit }; L.ac = { x: P.acX, y: P.acY, w: P.acW, nm: 'A/C', u: P.acUnit };
    L.slatsCut = c => L.slatY.filter((sy, k) => !L.slatOut.has(k) && sy < c.y + c.w / 2 && sy + P.slatW > c.y - c.w / 2).length;
  }
  return L;
}

/* ================= animation state ================= */
// every moving thing has an id; 0 = closed, 1 = open
const ANIM = {}; const DUR = 2080;
const ease = p => p < .5 ? 2 * p * p : 1 - Math.pow(-2 * p + 2, 2) / 2;
function ensure(id) { return ANIM[id] || (ANIM[id] = { from: 0, to: 0, t0: -1e9 }); }
function valOf(a, now) { const p = clamp((now - a.t0) / DUR, 0, 1); return a.from + (a.to - a.from) * ease(p); }
function curVals(now) { const V = {}; for (const id in ANIM) V[id] = valOf(ANIM[id], now); return V; }
function setTarget(id, to, delay) {
  const a = ensure(id), now = performance.now();
  if (a.to === to) return;
  a.from = valOf(a, now); a.to = to; a.t0 = now + (delay || 0);
}
function isOpenIds(ids) { return ids.some(id => ensure(id).to > 0.5); }
function toggleIds(ids) {
  const open = isOpenIds(ids), gap = ids.includes('flap') && ids.includes('ledge') ? 320 : 70;
  // closing runs the list backwards, so the foot ledge folds up before the table comes down over it
  (open ? ids.slice().reverse() : ids).forEach((id, i) => setTarget(id, open ? 0 : 1, i * gap));
  kick();
}
function animating(now) { for (const id in ANIM) if (now - ANIM[id].t0 < DUR) return true; return false; }
// the four legs along the free edge: the end legs 1 in from the ends of the leaf, the others evenly between (about 24 in apart on the 74 in leaf)
const legXs = P => { const k = (P.bedLen - 3.25) / 3; return [1, 1 + k, 1 + 2 * k, P.bedLen - 2.25]; };
// the bed makes up in three moves: the back cushion comes off the wall, the leaf flips over the front edge, the legs fold down
function bedState(s) {
  const th = clamp((s - .25) / .5, 0, 1) * Math.PI;
  return { th, ext: Math.max(0, -Math.cos(th)), lift: Math.sin(th), legs: clamp((s - .72) / .28, 0, 1), back: Math.cos(clamp(s / .45, 0, 1) * Math.PI / 2), flat: clamp((s - .7) / .3, 0, 1) };
}
// the dinette makes up into a bed: the table lowers, the backrest cushions come off and lie on it
function dinState(s) { return { tbl: ease(clamp(s / .5, 0, 1)), back: 1 - ease(clamp((s - .15) / .4, 0, 1)), pil: clamp((s - .55) / .45, 0, 1) }; }
const MOVER_IDS = ['dc0', 'dc1', 'dc2', 'dc3', 'dc4', 'dc5', 'clo_lo', 'clo_hi', 'bed', 'dinette', 'pan', 'flap', 'ledge', 'fridge'];
MOVER_IDS.forEach(ensure);
