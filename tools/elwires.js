/* The wires of the electrical page, coloured by gauge (AWG). Used by electric.js.
   Every wire has its own number, WR1, WR2 ... (a new prefix: the plan's other numbers are DR, PS, BE, XS, RF, CL, FA, CK, BS, ED, EP, PL).
   The routes are a proposal drawn between the items already on the page; the sizes and fuses come from the one-line diagram and the cable table.
   Wall routes use inches from the back mark (x) and up from the floor (z); ceiling routes use inches from the rear-door edge (x) and from the driver wall (y). */
const AWG = [
  { g: '2/0', c: '#6A1B9A', w: 7.5, cls: 'wg-2o0', name: '2/0', use: 'battery, bus and inverter cables' },
  { g: '2', c: '#D81B60', w: 6, cls: 'wg-2', name: '2', use: 'alternator, DC-DC charger and shore charger cables' },
  { g: '6', c: '#EF6C00', w: 5, cls: 'wg-6', name: '6', use: 'air conditioner feed' },
  { g: '10', c: '#C99A00', w: 4.2, cls: 'wg-10', name: '10', use: 'shore power (30 A) and the fuse block feed' },
  { g: '12', c: '#2E7D32', w: 3.4, cls: 'wg-12', name: '12', use: 'the 120 V circuits' },
  { g: '14', c: '#00ACC1', w: 3, cls: 'wg-14', name: '14', use: 'soft LED strip, roof fan, water pump' },
  { g: '16', c: '#1E4FD8', w: 2.6, cls: 'wg-16', name: '16', use: 'lights and light switches' },
  { g: '18', c: '#202124', w: 2.2, cls: 'wg-18', name: '18', use: 'control panel and the dimmer button' },
];
const byG = Object.fromEntries(AWG.map(a => [a.g, a]));
const gc = g => byG[g].c, gw = g => byG[g].w;

// ------------------------------------------------------------------ the wires
// t: 'dc' (12 V and the battery cables, drawn solid) or 'ac' (120 V, drawn dashed). D, P, C: polylines on the driver wall, the passenger wall, the ceiling.
// lab: where the number sits on each drawing. len: the length in feet when the drawn route is not the real one (the hub board, the A/C).
function wiresFor(pl, Dl, Pl, ceil) {
  const find = (list, re, what) => { const e = list.find(x => re.test(x.n)); if (!e) throw new Error('wire map: no item for ' + what + ' (' + re + ')'); return e; };
  const D = {
    batt: find(Dl, /^Battery/, 'battery'), inv: find(Dl, /^Inverter/, 'inverter'), dc: find(Dl, /^DC-DC/, 'DC-DC'), ch: find(Dl, /^Shore charger/, 'shore charger'),
    hub: find(Dl, /^Power hub/, 'hub'), inlet: find(Dl, /^Shore power inlet/, 'inlet'), lrear: find(Dl, /rear \(left\) of two/, 'rear couch light'),
    ld1: find(Dl, /dinette rear seat/, 'dinette light 1'), ld2: find(Dl, /dinette cab-end seat/, 'dinette light 2'), cout: find(Dl, /^Couch outlet/, 'couch outlet'),
    plate: find(Dl, /^Switch plate at the rear doors/, 'rear doors plate'), dsw: find(Dl, /^Light switch on the dinette/, 'dinette switch'),
    dim: find(Dl, /^Switch and dimmer/, 'dimmer'), dout: find(Dl, /^Outlet over the dinette table/, 'dinette outlet'), rA: find(Dl, /^Riser A/, 'riser A'),
    lright: find(Dl, /cab-end \(right\) of two/, 'right couch light'), swr: find(Dl, /^Switch for the cab-end \(right\)/, 'right couch switch'),
  };
  const P = {
    wet: find(Pl, /^Wet bath light/, 'wet bath light'), cl: find(Pl, /^Ceiling light over the countertop/, 'counter light'), fr: find(Pl, /^Fridge outlet/, 'fridge'),
    mic: find(Pl, /^Microwave outlet/, 'microwave'), pan: find(Pl, /^Control panel/, 'panel'), tv: find(Pl, /^Outlet under the TV/, 'TV outlet'),
    ht: find(Pl, /^Hot water heater feed/, 'heater'), sel: find(Pl, /^Heater or microwave selector/, 'selector'), rB: find(Pl, /^Riser B/, 'riser B'),
    s11: find(Pl, /^Light switch for the ceiling light over the countertop/, 'EP11'), s14: find(Pl, /^Light switch for the two center-row/, 'EP14'),
  };
  const lz = pl.cabBot - .5, RX = 79, ac = ceil.ac, fan = ceil.fan, acY = ac.y - ac.w / 2, fanY = fan.y - fan.w / 2;
  const ra = k => +(76.5 + (k - 3) * 1.1).toFixed(2);          // the cable bundle in riser A: 0 A/C, 1 120 V, 2 pump, 3 strip, 4 fan, 5 lights, 6 dimmer button, 7 control panel
  const rb = k => +(72.2 + k * .9).toFixed(2);                // riser B: 0 120 V, 1 pump, 2 control panel, 4 EP11, 5 EP14
  const lt = ceil.lights;                                      // ceiling coordinates: [shower, counter/sink, center rear, center front]
  const aR = ac.x + ac.w / 2 + 1.5, aT = ac.y - ac.w / 2 - 1.5;
  const R0 = 17.5;                                             // the risers start in the free band above S2 (13 3/4 to 19 1/2 up), where they jog away from the hub board
  const W = [];
  const add = w => { W.push(w); return w; };
  // ---- the hub board and the gear shelf (drawn on the one-line diagram: the runs are short, inside the hub's 2 x 10 in)
  add({ g: '2/0', t: 'dc', n: 'Battery + to the Class T fuse and the bus +', from: 'battery', to: 'bus', prot: 'Class T 250 A, within 7 in of the post', len: 1.5, hub: true, T: { D: [[[70.5, 9.5], [70.5, 6.5], [72, 6.5]]] }, tnote: 'The battery\u2019s post positions are assumed (+ at the cab end of the top); the order of the parts on the hub board is yours to choose.', note: 'red 2 ft; the whole inverter load goes through it' });
  add({ g: '2/0', t: 'dc', n: 'Battery − to the shunt and the bus −', from: 'battery', to: 'bus', prot: 'none (the shunt, 500 A)', len: 1.5, hub: true, T: { D: [[[67, 9.5], [67, 3.5], [72, 3.5]]] }, note: 'black 2 ft; the shunt sits on the negative' });
  add({ g: '2/0', t: 'dc', n: 'Bus to the inverter, + and −', from: 'bus', to: 'inverter', prot: '250 A on the + (the Class T can serve it)', len: 4, hub: true, T: { D: [[[72, 9], [71, 9], [71, 11]]] }, note: 'with a 2 ft loop so the gear shelf can slide out' });
  add({ g: '2', t: 'dc', n: 'Cab charge cable: starter battery to the DC-DC charger, + and −', from: 'starter battery, under the van', to: 'DC-DC charger', prot: '80 A at the starter battery', len: 17, note: 'about 15 ft under the van plus a 2 ft loop; it comes up through the sealed floor grommet at 70 in beside the battery, under the gear shelf',
    D: [[[70, .5], [75.4, .5], [75.4, 10], [dcMid(D.dc), 10], [dcMid(D.dc), D.dc.z0]]], lab: { D: [75.4, 5] } });
  add({ g: '2', t: 'dc', n: 'DC-DC charger to the bus, + and −', from: 'DC-DC charger', to: 'bus', prot: '80 A at the bus', len: 6, hub: true, T: { D: [[[57.05, 12.4], [57.05, 10.2], [72, 10.2], [72, 7.6]]] }, note: '4 ft plus a 2 ft loop for the shelf' });
  add({ g: '2', t: 'dc', n: 'Shore charger (VEVOR 80 A) to the bus, + and −', from: 'shore charger', to: 'bus', prot: '100 A at the bus', len: 6, hub: true, T: { D: [[[50.55, 12.6], [50.55, 9.8], [72, 9.8], [72, 8.4]]] }, note: 'its 120 V input is WR10' });
  add({ g: '10', t: 'ac', n: 'Shore power inlet to the transfer switch and the hub (30 A cable in flexible conduit)', from: D.inlet.id + ' shore inlet', to: 'hub board, 30 A breaker', prot: '30 A shore breaker', len: 8, note: 'runs inside the wall in the free band above S2 (13 3/4 to 19 1/2 up), clear of the couch wall-post screws',
    D: [[[D.inlet.x, D.inlet.z], [D.inlet.x, 16.7], [72.2, 16.7], [72.2, 11]]], lab: { D: [30, 16.7] } });
  add({ g: '12', t: 'ac', n: 'Inverter output to the transfer switch', from: 'inverter', to: 'transfer switch', prot: '20 A at the inverter output (about 17 A at 2000 W)', len: 3, hub: true, T: { D: [[[72.35, 13.4], [73.2, 13.4], [73.2, 10.2]]] }, note: 'my size (the BELTTT manual was not found): 12 AWG carries the 2000 W; follow its manual' });
  add({ g: '10', t: 'ac', n: 'Transfer switch to the AC panel (30 A main)', from: 'transfer switch', to: 'AC panel', prot: '30 A main', len: 2, hub: true, T: { D: [[[73.6, 10], [73.6, 8.5]]] }, tnote: 'Both ends are on the hub board; the order of its parts is yours to choose, so only the board is marked.', note: 'shore or inverter, never both' });
  add({ g: '12', t: 'ac', n: 'AC panel to the shore charger (its own breaker)', from: 'AC panel', to: 'shore charger', prot: '15 A breaker', len: 3, hub: true, T: { D: [[[73.9, 8.5], [73.9, 16.3], [46, 16.3], [46, 15]]] }, note: 'from the shore side only, never from the inverter; the cord needs a loop for the shelf' });
  // ---- the risers (no 12 V trunk: every 12 V circuit has its own wire from the fuse block)
  add({ g: '6', t: 'dc', n: 'A/C feed pair (+ and −), up riser A and across the ceiling', from: 'battery side of the hub (100 A fuse)', to: 'A/C unit', prot: '100 A fuse at the battery', len: 12, T: { D: [[[73, 11], [73, R0], [ra(0), R0]]] }, note: 'in its own loom in riser A; 6 AWG is the maker’s size for 12 ft (4 AWG would lose less)',
    D: [[[ra(0), R0], [ra(0), 75]]], C: [[[RX, 0], [RX, acY], [ac.x, acY]]], lab: { D: [ra(0), 26], C: [RX, 13] } });
  add({ g: '12', t: 'ac', n: '120 V circuits A, B/D and C (three 12 AWG cables in flexible conduit): up riser A, across the ceiling, down riser B', from: 'AC panel', to: 'every 120 V outlet', prot: 'A 15 A GFCI, B/D 20 A, C 15 A', T: { D: [[[73, 11], [73, R0], [ra(1), R0]]] }, note: 'the ceiling run and riser B follow the red dashed trunk of the ceiling diagram; separate from the 12 V loom by 2 in',
    D: [[[ra(1), R0], [ra(1), 75]]], C: [[[RX + 1.2, 0], [RX + 1.2, 68]]], P: [[[rb(0), 75], [rb(0), 8]]], lab: { D: [ra(1), 44], C: [RX + 1.2, 52], P: [rb(0), 40] } });
  add({ g: '10', t: 'dc', n: '12 V fuse block feed, + and −: bus to the fuse block', from: 'bus', to: 'hub fuse block', prot: '30 A fuse at the bus', len: 3, hub: true, T: { D: [[[73.2, 6], [73.2, 7.7]]] }, tnote: 'Both ends are on the hub board; the order of its parts is yours to choose, so only the board is marked.', note: 'my size: the 12 V circuits can draw about 20 A all at once (strip 6.4, pump 7, fan 2.7, lights 2.7, panel 1), which would leave 12 AWG at its limit, so 10 AWG with a 30 A fuse; each circuit below it has its own fuse and its own wire (there is no shared 12 V trunk); it feeds your 10-way blade fuse block (check that its input terminal takes a 10 AWG ring lug)' });
  add({ g: '14', t: 'dc', n: 'Soft LED strip circuit: up riser A to the junction box, then to the strip’s three feeds', from: 'hub fuse block', to: 'strip along the ceiling edge, three runs', prot: '10 A, its own circuit', T: { D: [[[73, 11], [73, R0], [ra(3), R0]]] }, endsOverride: [['C', [82.5, 1.5]], ['C', [82.5, 66.5]], ['C', [1.9, 3.4]]], note: 'the strip is about 76 W (6.4 A) at full: 14 AWG has plenty of margin; the back run is fed from the driver run’s feed',
    D: [[[ra(3), R0], [ra(3), 75]]], C: [[[82.5, 0], [82.5, 66.5]], [[RX, 34], [82.5, 34]], [[82.5, 3.4], [1.9, 3.4]]], lab: { D: [ra(3), 22], C: [82.5, 12] } });
  add({ g: '14', t: 'dc', n: 'Roof fan feed: up riser A to the junction box, then to the fan', from: 'hub fuse block', to: 'roof fan', prot: '5 A', T: { D: [[[73, 11], [73, R0], [ra(4), R0]]] }, note: 'the fan has no switch: it is controlled at the fan itself',
    D: [[[ra(4), R0], [ra(4), 75]]], C: [[[83.6, 0], [83.6, 20.5], [fan.x, 20.5], [fan.x, fanY]]], lab: { D: [ra(4), 38], C: [50, 20.5] } });
  add({ g: '16', t: 'dc', n: 'Lights feed: up riser A to the junction box and the cabinet tops', from: 'hub fuse block', to: 'ceiling lights, cabinet lights, their switches', prot: '5 A (4 ceiling + 4 cabinet lights, about 32 W)', T: { D: [[[73, 11], [73, R0], [ra(5), R0]]] }, note: 'the cabinet-light wires leave it along the cabinet tops (WR20, WR21, WR23)',
    D: [[[ra(5), R0], [ra(5), 75]]], C: [[[84.7, 0], [84.7, 36], [RX, 36]]], lab: { D: [ra(5), 55], C: [84.7, 24] } });
  add({ g: '18', t: 'dc', n: 'Dimmer push button ED14 to the dimming controller at the junction box', from: D.dim.id + ' button', to: 'dimming controller at JB', prot: 'with the strip circuit', note: 'a 12 V PWM controller rated 10 A or more sits at JB (my placement) and switches the strip circuit; the button wire is low current',
    D: [[[D.dim.x, D.dim.z], [D.dim.x, 62.6], [ra(6), 62.6], [ra(6), 75]]], C: [[[85.8, 0], [85.8, 37.5], [RX, 37.5]]], lab: { D: [D.dim.x, 60.6], C: [85.8, 45] } });
  // ---- driver wall loads
  add({ g: '12', t: 'ac', n: 'Couch outlet ' + D.cout.id + ', circuit A', from: 'riser A (120 V)', to: D.cout.id + ' couch outlet', prot: '15 A GFCI (circuit A)', note: 'along the free band above S6, into the box on S6',
    D: [[[ra(1), 61.5], [D.cout.x, 61.5], [D.cout.x, D.cout.z + .9]]], lab: { D: [(ra(1) + D.cout.x) / 2 + 3, 61.5] } });
  add({ g: '12', t: 'ac', n: 'Dinette outlet ' + D.dout.id + ', circuit A', from: 'riser A (120 V)', to: D.dout.id + ' dinette outlet', prot: '15 A GFCI (circuit A)', note: 'in the free band between S4 and the window sill frame, below the window',
    D: [[[ra(1), D.dout.z + 1.7], [D.dout.x, D.dout.z + 1.7], [D.dout.x, D.dout.z + .9]]], lab: { D: [(ra(1) + D.dout.x) / 2, D.dout.z + 1.7] } });
  add({ g: '16', t: 'dc', n: 'Right couch light ' + D.lright.id + ' through its switch ' + D.swr.id, from: 'lights feed, top of riser A', to: D.lright.id + ' light', prot: '5 A (lights circuit)', note: 'inside the wall cabinet, along its top, then down to the light; the switch is 3 in toward the cab from the light',
    D: [[[ra(5), 71.9], [D.swr.x, 71.9], [D.swr.x, lz], [D.lright.x, lz]]], lab: { D: [(ra(5) + D.swr.x) / 2, 71.9] } });
  add({ g: '16', t: 'dc', n: 'Feed to the rear doors plate ' + D.plate.id, from: 'lights feed, top of riser A', to: D.plate.id + ' two switches', prot: '5 A (lights circuit)', note: 'along the cabinet top, down the rear corner behind the planks',
    D: [[[ra(5), 70.9], [1.75, 70.9], [1.75, 49]]], lab: { D: [30, 70.9] } });
  add({ g: '16', t: 'dc', n: 'Rear couch light ' + D.lrear.id + ' from the plate ' + D.plate.id, from: D.plate.id + ' (switched)', to: D.lrear.id + ' light', prot: '5 A (lights circuit)', note: 'up the rear corner, along the cabinet interior, down to the light',
    D: [[[2.6, 49], [2.6, 69.6], [D.lrear.x, 69.6], [D.lrear.x, lz + .5]]], lab: { D: [(2.6 + D.lrear.x) / 2 + 4, 69.6] } });
  add({ g: '16', t: 'dc', n: 'Shower light from the plate ' + D.plate.id + ', up the corner and across the ceiling', from: D.plate.id + ' (switched)', to: P.wet.id + ' shower light', prot: '5 A (lights circuit)', note: 'up the driver wall’s rear corner, over the first bay of the ceiling (before the rib at 21 3/4), then along the slat to the light (grommet through the rib)',
    D: [[[3.45, 49], [3.45, 75]]], C: [[[9.45, 0], [9.45, lt[0].y], [lt[0].x, lt[0].y]]], lab: { D: [3.45, 60], C: [9.45, 29] } });
  add({ g: '16', t: 'dc', n: 'Feed to the dinette switch ' + D.dsw.id + ' on W2', from: 'lights feed, top of riser A', to: D.dsw.id + ' switch', prot: '5 A (lights circuit)', note: 'along the cabinet top toward the cab, down the corner behind the planks, into the box through a grommet',
    D: [[[ra(5), 71.4], [D.dsw.x, 71.4], [D.dsw.x, D.dsw.z + .8]]], lab: { D: [118, 71.4] } });
  add({ g: '16', t: 'dc', n: 'Dinette lights ' + D.ld1.id + ' and ' + D.ld2.id + ' from the switch ' + D.dsw.id, from: D.dsw.id + ' (switched)', to: D.ld1.id + ' and ' + D.ld2.id, prot: '5 A (lights circuit)', endsOverride: [['D', [D.ld1.x, lz + .5]], ['D', [D.ld2.x, lz + .5]]], note: 'back up the corner, along the cabinet interior, one drop to each light',
    D: [[[D.dsw.x - 1.1, D.dsw.z + .8], [D.dsw.x - 1.1, 69.4], [D.ld1.x, 69.4], [D.ld1.x, lz + .5]], [[D.ld2.x, 69.4], [D.ld2.x, lz + .5]]], lab: { D: [(D.ld1.x + D.ld2.x) / 2, 69.4] } });
  // ---- passenger wall loads
  add({ g: '12', t: 'ac', n: 'Fridge outlet ' + P.fr.id + ', circuit C', from: 'riser B (120 V)', to: P.fr.id + ' outlet behind the fridge', prot: '15 A (circuit C, the fridge alone)', note: 'in the free band between S1 and S2, behind the fridge platform',
    P: [[[rb(0), 8], [rb(0), 7.4], [P.fr.x, 7.4], [P.fr.x, P.fr.z + .9]]], lab: { P: [60, 7.4] } });
  add({ g: '12', t: 'ac', n: 'Riser B to the selector ' + P.sel.id + ' (circuit B/D, shared)', from: 'riser B (120 V)', to: P.sel.id + ' common pin', prot: '20 A breaker B/D', note: 'the middle pin of your 30 A rocker is the common',
    P: [[[rb(0), P.sel.z], [P.sel.x, P.sel.z]]], lab: { P: [rb(0) - 3.2, P.sel.z - 3.2] } });
  add({ g: '12', t: 'ac', n: 'Selector ' + P.sel.id + ' to the microwave outlet ' + P.mic.id, from: P.sel.id + ' (one end pin)', to: P.mic.id + ' outlet', prot: '20 A breaker B/D (one load at a time)', note: 'a 20 A receptacle',
    P: [[[P.sel.x, P.sel.z], [P.sel.x, 62.2], [P.mic.x, 62.2], [P.mic.x, P.mic.z - .9]]], lab: { P: [(P.sel.x + P.mic.x) / 2, 62.2] } });
  add({ g: '12', t: 'ac', n: 'Selector ' + P.sel.id + ' to the heater feed box ' + P.ht.id, from: P.sel.id + ' (other end pin)', to: P.ht.id + ' box beside the tank', prot: '20 A breaker B/D (one load at a time)', note: 'down behind the planks, drilled through S5 to S3, then along the free band above S2',
    P: [[[P.sel.x, P.sel.z], [P.sel.x, 15.5], [P.ht.x0, 15.5]]], lab: { P: [P.sel.x, 33] } });
  add({ g: '12', t: 'ac', n: 'TV outlet ' + P.tv.id + ', circuit A', from: 'riser B (120 V)', to: P.tv.id + ' outlet under the TV', prot: '15 A GFCI (circuit A)', note: 'behind the TV, above the two-rocker plate',
    P: [[[rb(0), 54.5], [P.tv.x, 54.5], [P.tv.x, P.tv.z + .9]]], lab: { P: [(rb(0) + P.tv.x) / 2 + 6, 54.5] } });
  add({ g: '14', t: 'dc', n: 'Water pump PL3: its own wire from the fuse block, up riser A, across the ceiling, down riser B', from: 'hub fuse block (10 A fuse)', to: 'PL3 pump beside the heater', prot: '10 A', T: { D: [[[73, 11], [73, R0], [ra(2), R0]]] }, note: 'the pump draws about 7 A; in riser B it leaves the loom at 24 in up and goes along the free band above S3 (through the notches in S2 to S4); about 16 ft longer than a tap would have been, so each wire is protected by its own fuse',
    D: [[[ra(2), R0], [ra(2), 75]]], C: [[[77.8, 0], [77.8, 68]]], P: [[[rb(1), 75], [rb(1), 24], [105.5, 24], [105.5, 20.6]]], lab: { D: [ra(2), 33], C: [77.8, 6], P: [88, 24] } });
  add({ g: '18', t: 'dc', n: 'Control panel ' + P.pan.id + ' (battery monitor, pump switch, tank levels): its own wire from the fuse block', from: 'hub fuse block (3 A fuse)', to: P.pan.id + ' panel', prot: '3 A', T: { D: [[[73, 11], [73, R0], [ra(7), R0]]] }, note: 'small 18 AWG, up riser A, across the ceiling and down riser B with the pump wire',
    D: [[[ra(7), R0], [ra(7), 75]]], C: [[[76.7, 0], [76.7, 68]]], P: [[[rb(2), 75], [rb(2), 47.5], [P.pan.x, 47.5], [P.pan.x, P.pan.z - .8]]], lab: { D: [ra(7), 48], C: [76.7, 17], P: [P.pan.x - 1, 47.5 - 3.6] } });
  add({ g: '16', t: 'dc', n: 'Switch ' + P.s11.id + ' to the counter and sink light ' + P.cl.id, from: P.s11.id + ' left rocker', to: P.cl.id + ' light', prot: '5 A (lights circuit)', flow: ['P', 'C'], note: '16 AWG pair behind the covering to riser B (about 27 in), up to the ceiling, then along the slat to the light',
    P: [[[P.s11.x, P.s11.z], [P.s11.x, 61.3], [rb(4), 61.3], [rb(4), 75]]], C: [[[81.8, 68], [81.8, lt[1].y], [lt[1].x, lt[1].y]]], lab: { P: [88, 61.3], C: [88, lt[1].y] } });
  add({ g: '16', t: 'dc', n: 'Switch ' + P.s14.id + ' to the two center-row ceiling lights', from: P.s14.id + ' right rocker', to: 'center row lights, rear and front', prot: '5 A (lights circuit)', flow: ['P', 'C'], endsOverride: [['C', [lt[2].x, lt[2].y]], ['C', [lt[3].x, lt[3].y]]], note: 'up riser B, across to the center slat, then along it, round the A/C opening, to both lights',
    P: [[[P.s14.x, P.s14.z], [P.s14.x, 62.2], [rb(5), 62.2], [rb(5), 75]]], C: [[[82.7, 68], [82.7, 34]], [[lt[2].x, lt[2].y], [lt[2].x, aT], [aR, aT], [aR, 34], [lt[3].x, lt[3].y]]], lab: { P: [88, 62.2], C: [92, 34] } });
  W.forEach((w, i) => { w.id = 'WR' + (i + 1); });
  W.forEach(w => { if (w.len == null) { let d = 0; ['D', 'P', 'C'].forEach(v => (w[v] || []).forEach(pl_ => { for (let i = 1; i < pl_.length; i++) d += Math.hypot(pl_[i][0] - pl_[i - 1][0], pl_[i][1] - pl_[i - 1][1]); })); w.len = d / 12; } });
  return W;
  function dcMid(b) { return +((b.x0 + b.x1) / 2).toFixed(2); }
}

// ------------------------------------------------------------------ drawing helpers (shared by the wall views, the ceiling and the one-line diagram)
function wireLine(pts, X, Y, g, t) {
  const q = pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' '), w = gw(g), dash = t === 'ac' ? ' stroke-dasharray="9 6"' : '';
  return `<polyline points="${q}" fill="none" stroke="#fff" stroke-opacity=".9" stroke-width="${w + 3.2}" stroke-linejoin="round" stroke-linecap="round"/><polyline points="${q}" fill="none" stroke="${gc(g)}" stroke-width="${w}" stroke-linejoin="round" stroke-linecap="${t === 'ac' ? 'butt' : 'round'}"${dash}/>`;
}
function wirePill(id, g, x, y) {
  const w = 10 + id.length * 6.2;
  return `<rect x="${x - w / 2}" y="${y - 8}" width="${w}" height="16" rx="8" fill="#fff" fill-opacity=".96" stroke="${gc(g)}" stroke-width="2"/><text x="${x}" y="${y + 3.7}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#1b1a17">${id}</text>`;
}
// where a wire starts and where it ends: the first point of its first view and the last point of its last view (lead-ins and hub routes included), unless set by hand
const FLOW = ['D', 'C', 'P'];
function viewsOf(w) { return (w.flow || FLOW).filter(v => (w[v] && w[v].length) || (w.T && w.T[v] && w.T[v].length)); }
function allIn(w, v) { return ((w.T && w.T[v]) || []).concat(w[v] || []); }
function endsOf(w) {
  const vs = viewsOf(w); if (!vs.length) return null;
  const first = allIn(w, vs[0]), last = allIn(w, vs[vs.length - 1]);
  return { start: { v: vs[0], pt: first[0][0] }, ends: w.endsOverride ? w.endsOverride.map(e => ({ v: e[0], pt: e[1] })) : [{ v: vs[vs.length - 1], pt: last[last.length - 1][last[last.length - 1].length - 1] }] };
}
function arrows(pts, X, Y, g) {
  let o = '';
  for (let i = 1; i < pts.length; i++) {
    const x0 = X(pts[i - 1][0]), y0 = Y(pts[i - 1][1]), x1 = X(pts[i][0]), y1 = Y(pts[i][1]), len = Math.hypot(x1 - x0, y1 - y0);
    if (len < 46) continue;
    const n = Math.max(1, Math.floor(len / 150)), ang = Math.atan2(y1 - y0, x1 - x0), ca = Math.cos(ang), sa = Math.sin(ang);
    for (let k = 1; k <= n; k++) { const t = k / (n + 1), cx = x0 + (x1 - x0) * t, cy = y0 + (y1 - y0) * t;
      o += `<path d="M${(cx + 7 * ca).toFixed(1)} ${(cy + 7 * sa).toFixed(1)} L${(cx - 5 * ca - 6 * sa).toFixed(1)} ${(cy - 5 * sa + 6 * ca).toFixed(1)} L${(cx - 5 * ca + 6 * sa).toFixed(1)} ${(cy - 5 * sa - 6 * ca).toFixed(1)} Z" fill="#fff" stroke="#111" stroke-width="1.6" stroke-linejoin="round"/>`; }
  }
  return o;
}
function marker(label, pt, X, Y, col, up) {
  const x = X(pt[0]), y = Y(pt[1]), w = label === 'START' ? 48 : 36;
  let by = up ? y - 40 : y + 36; if (by < 34) by = y + 36; if (by > 600) by = y - 40;
  const bx = Math.min(1040 - w / 2, Math.max(30 + w / 2, x));
  return `<line x1="${x}" y1="${y}" x2="${bx}" y2="${by + (by > y ? -9 : 9)}" stroke="${col}" stroke-width="2.4"/><circle cx="${x}" cy="${y}" r="6.5" fill="#fff" fill-opacity=".85" stroke="${col}" stroke-width="3"/><circle cx="${x}" cy="${y}" r="2.2" fill="${col}"/><rect x="${bx - w / 2}" y="${by - 9}" width="${w}" height="18" rx="9" fill="${col}" stroke="#fff" stroke-width="1.5"/><text x="${bx}" y="${by + 4}" text-anchor="middle" style="font-size:10.5px;font-weight:700;fill:#fff;letter-spacing:.4px">${label}</text>`;
}
// what is added to one drawing when this wire is picked: its hidden-otherwise routes, direction arrows, START and END
function traceLayer(w, view, X, Y) {
  const e = endsOf(w); if (!e) return '';
  const parts = [];
  ((w.T && w.T[view]) || []).forEach(p => parts.push(wireLine(p, X, Y, w.g, w.t)));
  allIn(w, view).forEach(p => parts.push(arrows(p, X, Y, w.g)));
  if (e.start.v === view) parts.push(marker('START', e.start.pt, X, Y, '#1B7F3B', true));
  e.ends.filter(x => x.v === view).forEach(x => parts.push(marker('END', x.pt, X, Y, '#111', false)));
  return parts.length ? `<g class="wtr" data-wr="${w.id}">${parts.join('')}</g>` : '';
}

// one wire as two svg groups (its lines, and its number label), both with its gauge as the class so the gauge boxes can hide them; draw every wire's lines first, then every label
function wireGroup(w, view, X, Y, placed) {
  const segs = w[view]; if (!segs) return { l: '', p: '' };
  const o = segs.map(p => wireLine(p, X, Y, w.g, w.t)).join('');
  let pill = '';
  const lb = w.lab && w.lab[view];
  if (lb) { let x = X(lb[0]), y = Y(lb[1]); for (let t = 0; t < 8 && placed.some(q => Math.abs(q[0] - x) < 46 && Math.abs(q[1] - y) < 17); t++) y -= 17; placed.push([x, y]); pill = wirePill(w.id, w.g, x, y); }
  return { l: `<g class="wgrp ${byG[w.g].cls}" data-wr="${w.id}"><title>${w.id}: ${byG[w.g].name} AWG</title>${o}</g>`, p: pill ? `<g class="wgrp ${byG[w.g].cls}" data-wr="${w.id}">${pill}</g>` : '' };
}

// ------------------------------------------------------------------ the wall views: the steel and furring faint, every wire on top
function wallLayers(side, items, base, furn, symbol, esc, INK) {
  const flip = side === 'P', view = flip ? 'P' : 'D';
  const X = x => +(flip ? 1020 - 6 * x : 50 + 6 * x).toFixed(1), Y = z => +(544 - 6 * z).toFixed(1);
  const fu = furn.map(it => { const xa = X(it.x0), xb = X(it.x1); return it.win
    ? `<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="#B5D4F4" fill-opacity=".25" stroke="#185FA5" stroke-width="1.4"/>`
    : `<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="none" stroke="${INK}" stroke-opacity=".3" stroke-width="1.2" stroke-dasharray="4 3"/>`; }).join('');
  const bigs = [], smalls = [];
  items.forEach(e => {
    if (e.k === 'run') return;
    if (e.k === 'box' || e.k === 'strip') { const [g] = symbol(e, X, Y); bigs.push(g);
      if (e.k === 'box') {                       // name the boxes, so a wire can be followed from one to the next
        const xa = X(e.x0), xb = X(e.x1), bx = Math.min(xa, xb), bw = Math.abs(xb - xa), by = Y(e.z1), bh = 6 * (e.z1 - e.z0), nm = e.n.split(/[,(]/)[0].replace(/^Power hub board$/, 'hub').replace(/^Shore charger$/, 'charger').replace(/^Inverter$/, 'inverter').replace(/^Battery$/, 'battery').replace(/^DC-DC charger$/, 'DC-DC').trim();
        const st = 'font-size:9.5px;font-weight:700;fill:#6b3a00;paint-order:stroke;stroke:#fff;stroke-width:2.6px';
        if (bw >= 80 && bh >= 40) bigs.push(`<text x="${bx + bw / 2}" y="${by + bh / 2 + 3.5}" text-anchor="middle" style="${st}">${e.id} ${esc(nm)}</text>`);
        else if (bw >= 50) bigs.push(`<text x="${bx + 4}" y="${/charger/.test(nm) ? by + bh - 5 : by + 12}" style="${st}">${e.id} ${esc(nm)}</text>`);
        else if (bh >= 50) bigs.push(`<text transform="rotate(-90 ${bx + bw / 2 + 3.4} ${by + bh / 2})" x="${bx + bw / 2 + 3.4}" y="${by + bh / 2}" text-anchor="middle" style="${st}">${e.id} ${esc(nm)}</text>`);
        else bigs.push(`<text x="${bx + bw + 4}" y="${by + bh / 2 + 3.5}" style="${st}">${e.id}</text>`);
      }
      return; }
    const [g, cx, cy] = symbol(e, X, Y);
    smalls.push(g + `<text x="${cx + 9}" y="${cy + 15}" style="font-size:8.5px;font-weight:700;fill:#5F5E5A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">${e.id}</text>`);
  });
  // riser A leaves the hub board through a short conduit and jogs over to its bundle
  const stub = flip ? '' : `<polyline points="${X(73)},${Y(11)} ${X(73)},${Y(17.5)} ${X(76.5)},${Y(17.5)}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><polyline points="${X(73)},${Y(11)} ${X(73)},${Y(17.5)} ${X(76.5)},${Y(17.5)}" fill="none" stroke="#9a9a94" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
  const pump = flip ? `<rect x="${X(107)}" y="${Y(20)}" width="${X(104) - X(107)}" height="${6 * 8}" rx="6" fill="#D9E2EC" fill-opacity=".9" stroke="#475569" stroke-width="2.2"/><text x="${(X(104) + X(107)) / 2}" y="${Y(16) + 3}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#475569">pump</text>` : '';
  // the hub board and the gear shelf: their short runs are on the one-line diagram
  let call = '';
  if (!flip) { const hubItem = items.find(e => /^Power hub/.test(e.n)); if (hubItem) { const tx = (y, t) => `<text x="${X(40) - 10}" y="${Y(y)}" text-anchor="end" style="font-size:10.5px;font-weight:700;fill:#6A1B9A;paint-order:stroke;stroke:#fff;stroke-width:3px">${t}</text>`;
    call = `<rect x="${X(40) - 4}" y="${Y(16.4)}" width="${X(75) - X(40) + 8}" height="${Y(0) - Y(16.4)}" fill="none" stroke="#6A1B9A" stroke-width="1.6" stroke-dasharray="3 4"/>` + tx(8, 'hub board and gear shelf (dotted box):') + tx(5.4, 'WR1 to WR3, WR5, WR6, WR8 to WR10, WR13') + tx(2.8, 'are short runs inside it: see 5a'); } }
  const inner = base.inner.replace(/ id="[^"]*"/g, '');
  return { flip, view, X, Y, fu, bigs, smalls, stub, pump, call, inner };
}
function wallWires(side, items, base, furn, W, symbol, fr, esc, INK) {
  const L = wallLayers(side, items, base, furn, symbol, esc, INK), { flip, view, X, Y } = L;
  const placed = [], wg = W.filter(w => w[view]).map(w => wireGroup(w, view, X, Y, placed)), wires = wg.map(g => g.l).join('') + wg.map(g => g.p).join('');
  // arrows where the risers go on to the ceiling
  const arrows = W.filter(w => w[view] && w.C).map(w => { const top = w[view].map(p => p[p.length - 1]).filter(p => p[1] >= 74.9)[0]; return top ? `<path d="M${X(top[0]) - 4} ${Y(75) - 2} L${X(top[0])} ${Y(75) - 9} L${X(top[0]) + 4} ${Y(75) - 2}" fill="${gc(w.g)}" stroke="#fff" stroke-width=".8"/>` : ''; }).join('');
  return `<svg viewBox="0 0 1070 636" role="img" aria-label="${flip ? 'Passenger' : 'Driver'} wall: every wire, coloured by gauge"><g class="wbase" id="wbase${side}" opacity=".33">${L.inner}</g>${L.fu}${L.bigs.join('')}${L.pump}${L.stub}${wires}${L.smalls.join('')}${arrows}${L.call}${W.map(w => traceLayer(w, view, X, Y)).join('')}</svg>`;
}

// ------------------------------------------------------------------ the key, the gauge boxes and the table
function keyHTML(W) {
  const rows = AWG.map(a => {
    const ws = W.filter(w => w.g === a.g), ft = ws.reduce((s, w) => s + w.len, 0);
    return `<tr><td><label><input type="checkbox" checked onchange="wgShow('${a.cls}',this.checked)"> <svg width="58" height="14" viewBox="0 0 58 14" style="display:inline-block;width:58px;max-width:58px;min-width:0;height:14px;vertical-align:-3px"><line x1="3" y1="7" x2="55" y2="7" stroke="#fff" stroke-width="${a.w + 3}" stroke-linecap="round"/><line x1="3" y1="7" x2="55" y2="7" stroke="${a.c}" stroke-width="${a.w}" stroke-linecap="round"/></svg> <b>${a.name} AWG</b></label></td><td>${a.use}</td><td class="num">${Math.round(ft)} ft</td><td class="kd">${ws.map(w => w.id).join(', ')}</td></tr>`;
  }).join('');
  return `<div class="tw"><table><thead><tr><th>Gauge (tick to show, untick to hide)</th><th>Used for</th><th>Drawn length</th><th>Wires</th></tr></thead><tbody>${rows}</tbody></table></div>
  <p class="lead"><b>How to read it:</b> the colour and thickness show the gauge. A solid line is 12 V or battery cable (a + and a − of that size); a dashed line is 120 V (one cable with hot, neutral and ground). The white round label is the wire’s own number, WR1, WR2 and so on. The drawn length is one way along the route drawn, with no slack or loops, so add 15 to 20% when you buy and double the 12 V and battery runs for the − wire. The hub board runs and the A/C length use the figures in the cable table.</p>`;
}
function tableHTML(W, fr) {
  const rows = W.map(w => `<tr class="wgrp ${byG[w.g].cls}" data-wr="${w.id}"><td><b class="wid">${w.id}</b></td><td style="white-space:nowrap"><svg width="40" height="12" viewBox="0 0 40 12" style="display:inline-block;width:40px;max-width:40px;min-width:0;height:12px;vertical-align:-2px"><line x1="3" y1="6" x2="37" y2="6" stroke="${gc(w.g)}" stroke-width="${gw(w.g)}" stroke-linecap="round"${w.t === 'ac' ? ' stroke-dasharray="7 5"' : ''}/></svg> <b>${byG[w.g].name}</b></td><td>${w.t === 'ac' ? '120 V' : '12 V / battery'}</td><td>${esc2(w.n)}<div class="kd">${esc2(w.from)} → ${esc2(w.to)}</div></td><td>${esc2(w.prot)}</td><td class="num">${w.len >= 10 ? Math.round(w.len) : (Math.round(w.len * 10) / 10)} ft</td><td class="kd">${esc2(w.note || '')}</td></tr>`).join('');
  return `<div class="tw"><table><thead><tr><th>#</th><th>AWG</th><th>Carries</th><th>Wire (from → to)</th><th>Fuse or breaker</th><th>Length</th><th>Notes</th></tr></thead><tbody>${rows}</tbody></table></div>`;
  function esc2(s) { return String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;'); }
}

module.exports = { AWG, byG, gc, gw, wiresFor, wireLine, wirePill, wireGroup, wallLayers, wallWires, keyHTML, tableHTML, traceLayer, viewsOf, endsOf, allIn, marker, arrows };
