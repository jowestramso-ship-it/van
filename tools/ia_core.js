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
  { k: 'hotGal', g: 'Water tanks', l: 'Hot water tank: how much water it holds (gallons; 3.96 gal is 15 liters; its 14 x 14 x 13 in size is the outside of the heater)', d: 3.96, s: .1, a: 1, b: 20 },
  { k: 'hotEmptyLb', g: 'Water tanks', l: 'Heater weight: the hot water tank empty (lb)', d: 2, s: .5, a: 0, b: 60 },
  { k: 'hotX0', g: 'Water tanks', l: 'Hot water tank: where it starts along the wall when it sits on the fresh tank or is placed by hand (from the back; you can drag it)', d: 87.25, s: .5, a: 0, b: 140 },
  { k: 'hotFree', g: 'Water tanks', l: 'Hot water tank: place it by hand at any height and spot (dragging it turns this on; turn it off to go back to the floor or shelf spots)', d: false, t: 'c' },
  { k: 'hotShelf', g: 'Water tanks', l: 'Hot water tank bottom, up from the floor (0 = on the floor; 7.5 = on a shelf over the wheel well; 16.75 = on a shelf on top of the fresh tank)', d: 16.75, s: .5, a: 0, b: 30 },
  { k: 'hotW', g: 'Water tanks', l: 'Hot water tank length along the wall', d: 14, s: .5, a: 6, b: 18 },
  { k: 'hotBack', g: 'Water tanks', l: 'Hot water tank: space behind it for the hot and cold fittings and the relief valve (they are at the back)', d: 1.625, s: .125, a: 0, b: 24 },
  { k: 'tankShift', g: 'Water tanks', l: 'Fresh water tank: moved toward the rear from the sink end (you can drag it)', d: 0, s: .5, a: 0, b: 50 },
  { k: 'drainOn', g: 'Water tanks', l: 'Draw the relief valve drain line (over the top of the tank, down in front of the fresh tank, out through the floor)', d: true, t: 'c' },
  { k: 'drainX', g: 'Water tanks', l: 'Relief valve drain line: where it comes down (from the back)', d: 89, s: .5, a: 60, b: 125 },
  { k: 'drainDia', g: 'Water tanks', l: 'Relief valve drain line: pipe size (at least the valve outlet, usually 3/4)', d: .75, s: .125, a: .375, b: 1.5 },
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
// the drawers and shelves under the counter, the jar shelf and the microwave shelf: how far each is moved from its planned spot (you can drag them; double-click one to put it back)
[['TB', 'Top drawer, back side', 1], ['TC', 'Top drawer, cab side', 1], ['C1', 'Cab-side column: upper (or only) drawer', 1], ['C2', 'Cab-side column: lower drawer', 1], ['B1', 'Back-side column: upper (or only) drawer', 1], ['B2', 'Back-side column: middle drawer', 1], ['B3', 'Back-side column: bottom drawer', 1],
  ['SC', 'Shelf under the cab-side drawers', 0], ['SB', 'Shelf under the back-side drawers', 0], ['SC2', 'Board between the two cab-side lower drawers', 0], ['SB1', 'Board between the upper and middle back-side drawers', 0], ['SB2', 'Board between the middle and bottom back-side drawers', 0],
  ['Nook', 'Jar shelf in the nook (with its upper row of jars)', 0], ['Micro', 'Microwave and its shelf', 0]].forEach(([k, nm, along]) => {
  if (along) PD.push({ k: 'dx' + k, g: 'Drawers and shelves', l: nm + ': moved along the wall (+ toward the cab, - toward the rear)', d: 0, s: .25, a: -60, b: 60 });
  PD.push({ k: 'dz' + k, g: 'Drawers and shelves', l: nm + ': moved up (+) or down (-)', d: 0, s: .25, a: -40, b: 40 });
});
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

/* ================= things you can drag, and the overlap finder ================= */
// a see-through rectangle over an item that can be dragged.
// ax = [size changed by sideways drags, inches per drawing unit, size changed by up and down drags, inches per drawing unit]; a size name may be '' for none, and the inches
// are negative where the drawing runs the other way. on = a tick box size that the first drag switches on.
function HIT(id, x, y, w, h, ax, bad, label, on) {
  const k = v => +(+v || 0).toFixed(5);
  return `<rect class="drg" data-drag="${id}" data-px="${ax[0]}" data-kx="${k(ax[1])}" data-py="${ax[2]}" data-ky="${k(ax[3])}" data-on="${on || ''}" x="${f1(x)}" y="${f1(y)}" width="${f1(Math.max(2, w))}" height="${f1(Math.max(2, h))}" rx="3" fill="#534AB7" fill-opacity="${bad ? .12 : .02}" stroke="${bad ? '#C0392B' : '#534AB7'}" stroke-width="${bad ? 2.6 : 1}" stroke-dasharray="${bad ? '5 2' : '2 3'}" stroke-opacity="${bad ? 1 : .6}"><title>${label}${bad ? ' (overlaps something: see the red message above the drawing)' : ' (drag to move it, double-click to put it back)'}</title></rect>`;
}
// every drawer and shelf board under the counter as a box: kind, id (the sizes that move it are dx<id> along the wall, drawers only, and dz<id> up), n = its name,
// x0/x1 along the wall and z0/z1 up (the planned spot plus how far it was dragged), y0/y1 out from the wall. The planned spots fill the space between the shelves, the
// top drawers and the tanks, as before; dragging only adds to them.
function cabinetParts(L) {
  const P = L.P, ch = P.counterH, d0 = L.cabS + 1.25, dm = L.cabS + 14.75, z0 = ch - 6.75, z1 = ch - 2.75, tl = z0 - .25, bs = L.cabShelf + 1, tot = tl - bs, parts = [];
  const add = (kind, id, n, x0, x1, b0, b1) => {
    const dx = kind === 'drawer' ? P['dx' + id] || 0 : 0, dz = P['dz' + id] || 0;
    parts.push({ kind, id, n, x0: x0 + dx, x1: x1 + dx, z0: b0 + dz, z1: b1 + dz, y0: 0, y1: 20, dxk: kind === 'drawer' ? 'dx' + id : '', dzk: 'dz' + id });
  };
  L.cabTot = tot; L.wellShelf = tot >= 10 ? L.backShelf : L.cabShelf;
  add('drawer', 'TB', 'the top drawer on the back side', d0, dm - .5, z0, z1);
  add('drawer', 'TC', 'the top drawer on the cab side', dm + 1, dm + 14, z0, z1);
  if (tot >= 3) {
    const ws = L.wellShelf;
    add('shelf', 'SC', 'the shelf under the cab-side drawers', dm, L.angS - .75, L.cabShelf, L.cabShelf + .75);
    add('shelf', 'SB', 'the shelf under the back-side drawers', L.cabS, dm, ws, ws + .75);
    if (tot >= 10) {
      const bt = tl - 6, bb = ws + 1, many = bt - bb >= 14.5, rh2 = (bt - bb - 1) / 2;
      add('shelf', 'SC2', 'the board between the two cab-side lower drawers', dm, L.angS - .75, tl - 6, tl - 5.25);
      add('drawer', 'C1', 'the upper cab-side drawer', dm + 1, dm + 14, tl - 5, tl);
      add('drawer', 'C2', 'the lower cab-side drawer', dm + 1, dm + 14, tl - 11, tl - 6);
      if (many) {
        add('shelf', 'SB1', 'the board between the upper and middle back-side drawers', L.cabS, dm, bt, bt + .75);
        add('shelf', 'SB2', 'the board between the middle and bottom back-side drawers', L.cabS, dm, bb + rh2, bb + rh2 + .75);
        add('drawer', 'B1', 'the upper back-side drawer', d0, dm - .5, tl - 5, tl);
        add('drawer', 'B2', 'the middle back-side drawer', d0, dm - .5, bb + rh2 + 1, bt);
        add('drawer', 'B3', 'the bottom back-side drawer', d0, dm - .5, bb, bb + rh2);
      } else add('drawer', 'B1', 'the back-side drawer', d0, dm - .5, bb, tl);
    } else {
      add('drawer', 'B1', 'the back-side drawer', d0, dm - .5, bs, tl);
      add('drawer', 'C1', 'the cab-side drawer', dm + 1, dm + 14, bs, tl);
    }
  }
  return parts;
}
// solid things on the passenger side (x along the van from the back, y out from the passenger wall, z up) and the roof units; reports what overlaps.
// Movable things (the tanks, drawers, shelves, jar shelf, microwave) are checked against each other and against the fixed ones; a fixed thing with vs only counts for those kinds.
function collisions(L) {
  const P = L.P, list = [], ids = new Set(), ch = P.counterH, dm = L.cabS + 14.75, ft = 8.25 + P.fridgeH;
  const bx = (id, n, x0, x1, y0, y1, z0, z1, o) => Object.assign({ id, n, x0, x1, y0, y1, z0, z1, kind: '' }, o);
  const hot = bx('hot', 'the hot water tank', L.hotX[0], L.hotX[1], P.hotBack, P.hotBack + P.hotD, P.hotShelf, P.hotShelf + P.hotH, { kind: 'tank' });
  const fresh = bx('fresh', 'the fresh water tank', L.tankX[0], L.tankX[1], 0, P.tankD, 0, P.tankH, { kind: 'tank' });
  const mov = [hot, fresh];
  L.parts.forEach(p => mov.push(bx(p.id, p.n, p.x0, p.x1, p.y0, p.y1, p.z0, p.z1, { kind: p.kind })));
  const nx0 = 58, nx1 = 93.25;
  mov.push(bx('Nook', 'the jar shelf in the nook with its upper row of jars', nx0, nx1, 0, 4.5, L.nookZ, L.nookZ + .75 + 7, { kind: 'jars' }));
  mov.push(bx('Micro', 'the microwave and its shelf', L.fr[0], L.fr[1], 0, P.microIn + 12, L.microZ[0] - .75, L.microZ[1], { kind: 'micro' }));
  const fix = [
    bx('', 'the wheel well', 42, 76, 0, 7, 0, 7.5), bx('', 'the fridge', L.fr[0], L.fr[1], 2, 2 + P.fridgeD, 8.25, ft), bx('', 'the cab wall', P.cab, P.cab + 60, 0, 40, 0, 120),
    bx('', 'the floor', -10, P.cab + 10, -5, 45, -40, 0), bx('', 'the ceiling', -10, P.cab + 10, -5, 45, L.ceilF, L.ceilF + 40),
    bx('', 'the counter and its rail', L.cabS, L.angS - .75, 0, P.cabD, ch - 2.25, ch), bx('', 'the countertop', L.angS - .75, L.sinkE, 0, P.cabD, ch - 1.2, ch),
    bx('', 'the lower row of jars', 58.75, 92.5, 0, 4.5, ch, ch + 7), bx('', 'the top of the nook', nx0, nx1, 0, 4.5, ch + 18.5, ch + 40),
    // the cabinet walls around the drawers (only drawers count: the shelves and the tanks reach into them by design)
    bx('', 'the end panel on the fridge side', L.cabS, L.cabS + .75, 0, P.cabD, 0, ch, { vs: ['drawer'] }), bx('', 'the end panel at the angled front', L.angS - .75, L.angS, 0, P.cabD, 0, ch, { vs: ['drawer'] }),
    bx('', 'the divider between the two columns', dm, dm + .5, 0, 20, L.cabTot >= 3 ? L.wellShelf + .75 : ch - 7.25, ch - 2.5, { vs: ['drawer'] })
  ];
  const ov = (a0, a1, b0, b1) => Math.min(a1, b1) - Math.max(a0, b0), seen = new Set(), cp = n => n[0].toUpperCase() + n.slice(1);
  const test = (a, b) => {
    if (b.vs && !b.vs.includes(a.kind)) return;
    const ox = ov(a.x0, a.x1, b.x0, b.x1), oy = ov(a.y0, a.y1, b.y0, b.y1), oz = ov(a.z0, a.z1, b.z0, b.z1);
    if (ox > .06 && oy > .06 && oz > .06) {
      const key = a.id + '|' + b.n + '|' + b.id; if (seen.has(key)) return; seen.add(key); ids.add(a.id); if (b.id) ids.add(b.id);
      list.push({ ids: [a.id, b.id], msg: `${cp(a.n)} overlaps ${b.n} (${fmt(ox)} in along the wall, ${fmt(oy)} in out from it, ${fmt(oz)} in up).` });
    }
  };
  mov.forEach((a, i) => { for (let j = i + 1; j < mov.length; j++) test(a, mov[j]); fix.forEach(b => test(a, b)); });
  // the open floor beside the sink cabinet end is the entry: nothing may stand past the cabinet end panel
  [hot, fresh].forEach(a => { const past = a.x1 - (L.sinkE - .75); if (past > .06 && a.z0 < ch) { ids.add(a.id); list.push({ ids: [a.id], msg: `${cp(a.n)} sticks out ${fmt(past)} in past the end of the sink cabinet (${fmt(L.sinkE - .75)} in) into the entry by the sliding door.` }); } });
  // roof units: the fan and air conditioner bases must not overlap on the roof
  const f = L.fan, a = L.ac, ox = ov(f.x - f.u / 2, f.x + f.u / 2, a.x - a.u / 2, a.x + a.u / 2), oy = ov(f.y - f.u / 2, f.y + f.u / 2, a.y - a.u / 2, a.y + a.u / 2);
  if (ox > .06 && oy > .06) { ids.add('fan'); ids.add('ac'); list.push({ ids: ['fan', 'ac'], msg: `The fan unit and the air conditioner unit overlap on the roof (${fmt(ox)} x ${fmt(oy)} in).` }); }
  return { list, ids };
}

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
  const endX = L.sinkE - .75 - P.tankShift, wellEnd = 76;
  if (P.tankAuto) { L.hotX = [wellEnd + P.hotGap, wellEnd + P.hotGap + P.hotW]; L.tankX = [L.hotX[1] + P.hotGap, endX]; }
  else { L.tankX = [endX - P.tankLen, endX]; const gap = Math.max(0, Math.min(P.hotGap, (L.tankX[0] - wellEnd - P.hotW) / 2)); L.hotX = [wellEnd + gap, wellEnd + gap + P.hotW]; }
  if (P.hotShelf > 10 || P.hotFree) L.hotX = [P.hotX0, P.hotX0 + P.hotW]; // on a shelf on top of the fresh tank, or put where you dragged it
  else if (P.hotShelf > .5) L.hotX = [L.fr[1] + 1.5, L.fr[1] + 1.5 + P.hotW]; // on a shelf over the wheel well, 1 1/2 in past the fridge platform
  L.tankLen = L.tankX[1] - L.tankX[0];
  L.hotGal = P.hotGal;
  {
    // the shelves under the drawers: each column's shelf sits half an inch over whatever is under it (a tank or the wheel well, 7.5)
    const dm = L.cabS + 14.75, hotTopZ = P.hotShelf + P.hotH, ov = (x0, x1, a, b) => x1 > a && x0 < b;
    const overCab = ov(L.hotX[0], L.hotX[1], dm + .9, dm + 14), overBack = ov(L.hotX[0], L.hotX[1], L.cabS + 1.25, dm - .5);
    const freshCab = ov(L.tankX[0], L.tankX[1], dm + .9, dm + 14), freshBack = ov(L.tankX[0], L.tankX[1], L.cabS + 1.25, dm - .5);
    L.cabShelf = Math.max(7.5, overCab ? hotTopZ : 0, freshCab ? P.tankH : 0) + .5;
    L.backShelf = Math.max(7.5, overBack ? hotTopZ : 0, freshBack ? P.tankH : 0) + .5;
  }
  L.hotY = [P.hotBack, P.hotBack + P.hotD];
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
  // the drawers and shelves under the counter (as planned plus dragged), the jar shelf in the nook and the microwave shelf above the fridge
  L.parts = cabinetParts(L); L.partById = {}; L.parts.forEach(p => { L.partById[p.id] = p; });
  L.nookZ = P.counterH + 7.5 + P.dzNook;
  L.microZ = [8.25 + P.fridgeH + 2.75 + P.dzMicro, 8.25 + P.fridgeH + 12.75 + P.dzMicro];   // the microwave bottom and top; its shelf is the 3/4 in under it, 2 in over the fridge top
  L.coll = collisions(L);
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
