/* The wires of the electrical page, coloured by gauge (AWG). Used by electric.js.
   Every wire has its own number, WR1, WR2 ... (a new prefix: the plan's other numbers are DR, PS, BE, XS, RF, CL, FA, CK, BS, ED, EP, PL).
   The routes are a proposal drawn between the items already on the page; the sizes and fuses come from the one-line diagram and the cable table.
   Wall routes use inches from the back mark (x) and up from the floor (z); ceiling routes use inches from the rear-door edge (x) and from the driver wall (y). */
const AWG = [
  { g: '2/0', c: '#6A1B9A', w: 7.5, cls: 'wg-2o0', name: '2/0', use: 'battery, bus and inverter cables' },
  { g: '2', c: '#D81B60', w: 6, cls: 'wg-2', name: '2', use: 'alternator, DC-DC charger and shore charger cables' },
  { g: '6', c: '#EF6C00', w: 5, cls: 'wg-6', name: '6', use: 'air conditioner feed' },
  { g: '10', c: '#C99A00', w: 4.2, cls: 'wg-10', name: '10', use: 'shore power (30 A) and the fuse block feed' },
  { g: '12', c: '#2E7D32', w: 3.4, cls: 'wg-12', name: '12', use: 'the inverter output (WR8) only: it can deliver about 17 A, more than a 15 A breaker and 14 AWG' },
  { g: '14', c: '#00ACC1', w: 3, cls: 'wg-14', name: '14', use: 'soft LED strip, roof fan, water pump, lights and light switches (single wires, 12 V); and the 120 V circuits (15 A breakers; those are 3-conductor cable with a ground, a separate buy)' },
  { g: '18', c: '#202124', w: 2.2, cls: 'wg-18', name: '18', use: 'control panel and the dimmer button' },
];
const byG = Object.fromEntries(AWG.map(a => [a.g, a]));
const gc = g => byG[g].c, gw = g => byG[g].w;

// ------------------------------------------------------------------ the wires
// t: 'dc' (12 V and the battery cables, drawn solid) or 'ac' (120 V, drawn dashed). D, P, C: polylines on the driver wall, the passenger wall, the ceiling.
// lab: where the number sits on each drawing. len: the length in feet when the drawn route is not the real one (the A/C and the runs on the tray).
function wiresFor(pl, Dl, Pl, ceil) {
  const find = (list, re, what) => { const e = list.find(x => re.test(x.n)); if (!e) throw new Error('wire map: no item for ' + what + ' (' + re + ')'); return e; };
  const D = {
    batt: find(Dl, /^Battery/, 'battery'), inv: find(Dl, /^Inverter/, 'inverter'), dc: find(Dl, /^DC-DC/, 'DC-DC'), ch: find(Dl, /^Shore charger/, 'shore charger'),
    hub: find(Dl, /^Power hub/, 'hub'), ts: find(Dl, /^TS-30/, 'TS-30'), acp: find(Dl, /^AC panel/, 'AC panel'), fb: find(Dl, /^12 V fuse block/, 'fuse block'), inlet: find(Dl, /^Shore power inlet/, 'inlet'), lrear: find(Dl, /rear \(left\) of two/, 'rear couch light'),
    ld1: find(Dl, /dinette rear seat/, 'dinette light 1'), ld2: find(Dl, /dinette cab-end seat/, 'dinette light 2'), cout: find(Dl, /^Couch outlet/, 'couch outlet'),
    plate: find(Dl, /^Switch plate at the rear doors/, 'rear doors plate'), dsw: find(Dl, /^Light switch on the dinette/, 'dinette switch'),
    dim: find(Dl, /^Dimmer push button at the couch/, 'retired couch dimmer'), dout: find(Dl, /^Outlet over the dinette table/, 'dinette outlet'), rA: find(Dl, /^Riser A/, 'riser A'),
    lright: find(Dl, /cab-end \(right\) of two/, 'right couch light'), jb: find(Dl, /^Lights junction box/, 'junction box'), jb2: find(Dl, /^Strip junction box/, 'strip junction box'), dim2: find(Dl, /^Slide dimmer for the soft LED strip/, 'slide dimmer'), swr: find(Dl, /^Switch for the cab-end \(right\)/, 'right couch switch'),
  };
  const P = {
    wet: find(Pl, /^Wet bath light/, 'wet bath light'), cl: find(Pl, /^Ceiling light over the countertop/, 'counter light'), fr: find(Pl, /^Fridge outlet/, 'fridge'),
    mic: find(Pl, /^Microwave outlet/, 'microwave'), pan: find(Pl, /^Control panel/, 'panel'), tv: find(Pl, /^Outlet under the TV/, 'TV outlet'), ce: find(Pl, /^Outlet for counter items/, 'counter outlet'),
    ht: find(Pl, /^Hot water heater outlet/, 'heater'), sel: find(Pl, /^Heater or microwave selector/, 'selector'), rB: find(Pl, /^Riser B/, 'riser B'),
    s11: find(Pl, /^Light switch for the ceiling light over the countertop/, 'EP11'), s14: find(Pl, /^Light switch for the two center-row/, 'EP14'),
  };
  const lz = pl.cabBot - .5, RX = 79, ac = ceil.ac, fan = ceil.fan, acY = ac.y - ac.w / 2, fanY = fan.y - fan.w / 2;
  const ra = k => +(76.5 + (k - 3) * 1.1).toFixed(2);          // the cable bundle in riser A: 0 A/C, 1 120 V, 2 pump, 3 strip, 4 fan, 5 lights, 6 dimmer button, 7 control panel
  const rb = k => +(72.2 + k * .9).toFixed(2);                // riser B: 0 120 V, 1 pump, 2 control panel, 4 EP11, 5 EP14
  const lt = ceil.lights;                                      // ceiling coordinates: [shower, counter/sink, center rear, center front]
  const aR = ac.x + ac.w / 2 + 1.5, aT = ac.y - ac.w / 2 - 1.5;
  const R0 = 17.5, jbc = (D.jb.x0 + D.jb.x1) / 2;                                             // the risers start in the free band above S2 (13 3/4 to 19 1/2 up), where they jog away from the hub board
  // the gear area as it is now (EF3 and EF4): the TS-30, the AC panel and the 12 V fuse block are on the divider panel's outer face (x = 38.65, the face toward the rear doors), the DC bus bars, the inverter and the two chargers on the pull-out tray,
  // the Class T fuse and the shunt on the closet's end panel (74); the divider has a grommet hole to the tray at 13.8 in up. The 12 V cables leave the fuse block, go up past the parts to 15.4 in and out through the covering at x = 37 into the free band above S2
  // (R0), then east along it to riser A; the 120 V cables leave the AC panel and go through the covering at x = 34.5, 2 1/2 in away from the 12 V ones
  const TS = D.ts, AP = D.acp, FB = D.fb, GZ = 13.8, HX12 = 37, HX120 = 34.5, bus = 57.3;
  const tail12 = k => [[FB.x1 - 1, FB.z1], [FB.x1 - 1, 15.4], [HX12, 15.4], [HX12, R0], [ra(k), R0]];
  const W = [];
  const add = w => { W.push(w); return w; };
  // ---- the gear area: the divider panel, the pull-out tray and the closet's end panel (EF3, EF4); the short runs inside it are drawn on the driver wall in the dotted box and on the one-line diagram
  add({ g: '2/0', t: 'dc', n: 'Battery + to the Class T fuse and the bus +', from: 'battery', to: 'bus', prot: 'Class T 250 A, within 7 in of the post', len: 4, hub: true, T: { D: [[[71.4, 10.4], [72.7, 10.4], [72.7, 13.6], [57.8, 13.6], [57.8, 12.9]]] }, tnote: 'The battery\u2019s post positions are assumed (+ at the cab end of the top).', note: 'red: from the battery post to the Class T fuse on the closet\u2019s end panel (within 7 in of the post), then to the red bus bar on the tray, with a loop of about 24 in so the tray can slide out; the whole inverter load goes through it' });
  add({ g: '2/0', t: 'dc', n: 'Battery − to the shunt and the bus −', from: 'battery', to: 'bus', prot: 'none (the shunt, 500 A)', len: 4, hub: true, T: { D: [[[71.4, 10.9], [73.2, 10.9], [73.2, 14.9], [57.2, 14.9], [57.2, 12.9]]] }, note: 'black: from the battery post to the shunt on the closet\u2019s end panel, then to the black bus bar on the tray, with the same 24 in loop; the shunt sits on the negative' });
  add({ g: '2/0', t: 'dc', n: 'Bus to the inverter, + and −', from: 'bus', to: 'inverter', prot: '250 A on the + (the Class T can serve it)', len: 2, hub: true, T: { D: [[[57.1, 12.2], [55.5, 12.2], [55.5, 13.2]]] }, note: 'both ends are on the tray (the bus bars and the inverter slide together), so there is no loop: a short run of about 1 ft' });
  add({ g: '2', t: 'dc', n: 'Cab charge cable: starter battery to the DC-DC charger, + and −', from: 'starter battery, under the van', to: 'DC-DC charger', prot: '80 A at the starter battery', len: 17, note: 'about 15 ft under the van plus a 2 ft loop; it comes up through the sealed floor grommet at 70 in beside the battery, under the gear shelf',
    D: [[[70, .5], [75.4, .5], [75.4, 10], [dcMid(D.dc), 10], [dcMid(D.dc), D.dc.z0]]], lab: { D: [75.4, 5] } });
  add({ g: '2', t: 'dc', n: 'DC-DC charger to the bus, + and −', from: 'DC-DC charger', to: 'bus', prot: '80 A at the bus', len: 1.5, hub: true, T: { D: [[[59.1, 12.4], [58.4, 12.4]]] }, note: 'both ends are on the tray: the DC-DC charger is next to the bus bars, so a short run of about 1 ft' });
  add({ g: '2', t: 'dc', n: 'Shore charger (VEVOR 80 A) to the bus, + and −', from: 'shore charger', to: 'bus', prot: '100 A at the bus', len: 2, hub: true, T: { D: [[[61.4, 12.6], [58.4, 12.6]]] }, note: 'both ends are on the tray, a short run of about 1 1/2 ft; its 120 V input is WR10' });
  add({ g: '10', t: 'ac', n: 'Shore power inlet to the transfer switch (30 A cable in flexible conduit)', from: D.inlet.id + ' shore inlet', to: 'TS-30 transfer switch (30 A input)', prot: '30 A shore breaker', len: 4, note: 'runs inside the wall in the free band above S2 (13 3/4 to 19 1/2 up), clear of the couch wall-post screws',
    D: [[[D.inlet.x, D.inlet.z], [D.inlet.x, 16.7], [HX120, 16.7], [HX120, TS.z1]]], lab: { D: [20, 16.7] } });
  add({ g: '12', t: 'ac', n: 'Inverter output to the transfer switch', from: 'inverter', to: 'transfer switch', prot: '20 A at the inverter output (about 17 A at 2000 W)', len: 3, hub: true, T: { D: [[[47.5, 13.4], [38.65, GZ], [36.3, GZ], [36.3, TS.z1]]] }, note: 'from the inverter\u2019s AC output on the tray, about 9 in west through the grommet in the divider panel to the TS-30 (EF3), with a loop of about 24 in so the tray can slide out; my size (the BELTTT manual was not found): 12 AWG carries the 2000 W; follow its manual' });
  add({ g: '10', t: 'ac', n: 'Transfer switch to the AC panel (30 A main)', from: 'transfer switch', to: 'AC panel', prot: '30 A main', len: 2, hub: true, T: { D: [[[36.2, TS.z1], [36.2, 13], [37.6, 13], [37.6, AP.z1]]] }, tnote: 'Both ends are on the divider panel, side by side (EF3).', note: 'shore or inverter, never both' });
  add({ g: '14', t: 'ac', n: 'AC panel to the shore charger (its own breaker)', from: 'AC panel', to: 'shore charger', prot: '15 A breaker', len: 5, hub: true, T: { D: [[[37, AP.z1], [37, 14.2], [62, 14.2], [62, 13]]] }, note: 'from the AC panel on the divider, through the grommet, to the shore charger on the tray: about 25 in plus a 24 in loop so the tray can slide out; from the shore side only, never from the inverter' });
  // ---- the risers (no 12 V trunk: every 12 V circuit has its own wire from the fuse block)
  add({ g: '6', t: 'dc', n: 'A/C feed pair (+ and −), up riser A and across the ceiling', from: 'red bus bar on the tray (100 A fuse beside it)', to: 'A/C unit', prot: '100 A fuse at the battery', len: 12, T: { D: [[[bus, 12.6], [bus, R0], [ra(0), R0]]] }, note: 'in its own loom in riser A, with a loop of about 24 in near the bus bar so the tray can slide out; 6 AWG is the maker’s size for 12 ft (4 AWG would lose less)',
    D: [[[ra(0), R0], [ra(0), 75]]], C: [[[RX, 0], [RX, acY], [ac.x, acY]]], lab: { D: [ra(0), 26], C: [RX, 13] } });
  add({ g: '14', t: 'ac', n: '120 V circuits B/D and C (two 14 AWG cables in flexible conduit): up riser A, across the ceiling, down riser B', from: 'AC panel', to: 'riser B at 54 in up, where the C cable (WR26) leaves for the fridge outlet and the B/D cable (WR27) goes on to the selector', prot: 'B/D 15 A GFCI, C 15 A', T: { D: [[[37, AP.z1], [37, 15], [HX120, 15], [HX120, R0], [ra(1), R0]]] }, note: 'the ceiling run and riser B follow the red dashed trunk of the ceiling diagram; separate from the 12 V loom by 2 in',
    D: [[[ra(1), R0], [ra(1), 75]]], C: [[[RX + 1.2, 0], [RX + 1.2, 68]]], P: [[[rb(0), 75], [rb(0), 54]]], lab: { D: [ra(1), 44], C: [RX + 1.2, 52], P: [rb(0), 40] } });
  add({ g: '10', t: 'dc', n: '12 V fuse block feed, + and −: bus to the fuse block', from: 'bus', to: '12 V fuse block', prot: '30 A fuse at the bus', len: 5, hub: true, T: { D: [[[bus, 13.6], [38.65, GZ], [37.65, GZ], [37.65, FB.z1]]] }, tnote: 'From the bus bar on the tray, through the grommet in the divider, to the fuse block on the divider\u2019s outer face (EF3).', note: 'about 20 in plus a 24 in loop so the tray can slide out; my size: the 12 V circuits can draw about 20 A all at once (strip 6.4, pump 7, fan 2.7, lights 2.7, panel 1), which would leave 12 AWG at its limit, so 10 AWG with a 30 A fuse; each circuit below it has its own fuse and its own wire (there is no shared 12 V trunk); it feeds your 10-way blade fuse block (check that its input terminal takes a 10 AWG ring lug)' });
  add({ g: '14', t: 'dc', n: 'Soft LED strip circuit: up riser A to the strip junction box ' + D.jb2.id + ' (the supply for the slide dimmer)', from: '12 V fuse block', to: 'strip junction box ' + D.jb2.id, prot: '10 A, its own circuit', T: { D: [tail12(3)] }, note: 'the strip is about 76 W (6.4 A) at full: 14 AWG has plenty of margin. This pair brings the 10 A strip circuit to ' + D.jb2.id + ', the second junction box just under ' + D.jb.id + ' (the lights splices stay in ' + D.jb.id + '), where it is spliced on to the slide dimmer ' + D.dim2.id + ' on W2 (WR38); the dimmed power comes back to ' + D.jb2.id + ' (WR39) and splits to the three strips (WR40). There is no dimming controller (user, 2026-11-05)',
    D: [[[ra(3), R0], [ra(3), 68.7], [D.jb2.x1, 68.7]]], lab: { D: [ra(3), 22] } });
  add({ g: '14', t: 'dc', n: 'Roof fan feed: up riser A and across the ceiling to the fan', from: '12 V fuse block', to: 'roof fan', prot: '5 A', T: { D: [tail12(4)] }, note: 'the fan has no switch: it is controlled at the fan itself',
    D: [[[ra(4), R0], [ra(4), 75]]], C: [[[83.6, 0], [83.6, 20.5], [fan.x, 20.5], [fan.x, fanY]]], lab: { D: [ra(4), 38], C: [50, 20.5] } });
  add({ g: '14', t: 'dc', n: 'Lights feed: up riser A to the junction box ' + D.jb.id + ' in the couch cabinet', from: '12 V fuse block', to: 'junction box ' + D.jb.id, prot: '5 A (4 ceiling + 4 cabinet lights, about 32 W)', T: { D: [tail12(5)] }, note: 'it goes through a grommet in the cabinet’s cab-end side panel; the lights circuit splits at ' + D.jb.id + ': the cabinet-light wires leave along the cabinet top (WR20, WR21, WR24) and WR35 goes on to the passenger-wall switches',
    D: [[[ra(5), R0], [ra(5), 71.4], [D.jb.x1, 71.4]]], lab: { D: [ra(5), 55] } });
  add({ retired: true, g: '18', t: 'dc', n: 'Dimmer push button ED14 to the dimming controller in JB (retired)', from: 'ED14 button (retired)', to: 'dimming controller (retired)', prot: 'none', len: 0, note: 'retired (user, 2026-11-05: no dimming controller; one slide dimmer on the dinette wall, ED22, fed by WR38 and WR39). The number is not reused. If this cable was already pulled, leave it as a spare or take it out' });
  // ---- driver wall loads
  add({ g: '14', t: 'ac', n: 'Couch outlet ' + D.cout.id + ', circuit A: the cable from the AC panel', from: 'AC panel (circuit A, 15 A GFCI)', to: D.cout.id + ' couch outlet', prot: '15 A GFCI (circuit A)', T: { D: [[[37, AP.z1], [37, 15], [HX120, 15], [HX120, R0], [ra(1), R0]]] }, note: 'circuit A\u2019s own cable (14 AWG, hot, neutral and ground): from the AC panel through the covering at 34 1/2 in, east along the free band above S2, up riser A, then along the free band above S6 into the box on S6; it does not stop here: two more cables leave the box, one for the dinette outlet (WR19) and one for the counter outlet (WR30), and all of them are joined to the outlet with pigtails in the box (three cables: the outlet gang of the deep three gang box on S6, with a divider between it and the 12 V switches ED19 and ED14 beside it)',
    D: [[[ra(1), R0], [ra(1), 61.5], [D.cout.x, 61.5], [D.cout.x, D.cout.z + .9]]], lab: { D: [(ra(1) + D.cout.x) / 2 + 3, 61.5] } });
  add({ g: '14', t: 'ac', n: 'Dinette outlet ' + D.dout.id + ', circuit A: on from the couch outlet ' + D.cout.id, from: D.cout.id + ' couch outlet (through its box)', to: D.dout.id + ' dinette outlet', prot: '15 A GFCI (circuit A)', note: 'a second cable out of the couch outlet\u2019s box: along the free band above S6 to riser A, down riser A to the free band between S4 and the window sill frame, then east below the window to the box; the dinette outlet is the end of this branch, so one cable only reaches it',
    D: [[[D.cout.x + .6, D.cout.z + .9], [D.cout.x + .6, 62.3], [ra(1) + .5, 62.3], [ra(1) + .5, D.dout.z + 1.7], [D.dout.x, D.dout.z + 1.7], [D.dout.x, D.dout.z + .9]]], lab: { D: [ra(1) + .5, 44] } });
  add({ g: '14', t: 'dc', n: 'Right couch light ' + D.lright.id + ' through its switch ' + D.swr.id, from: 'junction box ' + D.jb.id, to: D.lright.id + ' light', prot: '5 A (lights circuit)', note: 'two 14 AWG cables, because the switch is in the two gang box on S6 beside the couch outlet: the feed goes from JB down behind the covering to the box, and the switched wire goes from the box back up into the wall cabinet, along inside it and down to the light',
    D: [[[D.jb.x0, 71.9], [D.swr.x, 71.9], [D.swr.x, D.swr.z + .9]], [[D.swr.x - .6, D.swr.z + .9], [D.swr.x - .6, lz + 2], [D.lright.x, lz + 2], [D.lright.x, lz]]], lab: { D: [(D.jb.x0 + D.swr.x) / 2 + 3, 71.9] } });
  add({ g: '14', t: 'dc', n: 'Feed to the rear doors plate ' + D.plate.id, from: 'junction box ' + D.jb.id, to: D.plate.id + ' two switches', prot: '5 A (lights circuit)', note: 'along the cabinet top, down the rear corner behind the planks. AT THE PLATE (user chose two jumpers and a lever connector, 2026-11-06; drawing EF14): the + goes into a 3 port lever connector (rated 20 A or more) with two short jumpers, red 14 AWG, about 6 in, a spade terminal on the switch end, one to the IN of the rear couch light switch and one to the IN of the shower light switch; the OUT of each switch is the + of WR22 and WR23; the \u2212 joins WR22 \u2212 and WR23 \u2212 in a second 3 port lever connector. The plate is one deep two gang box with the two switches side by side, so the lever connectors, the jumpers and all the wires are in that one box',
    D: [[[D.jb.x0, 70.9], [1.75, 70.9], [1.75, 49]]], lab: { D: [30, 70.9] } });
  add({ g: '14', t: 'dc', n: 'Rear couch light ' + D.lrear.id + ' from the plate ' + D.plate.id, from: D.plate.id + ' (switched)', to: D.lrear.id + ' light', prot: '5 A (lights circuit)', note: 'up the rear corner, along the cabinet interior, down to the light. Its + is the OUT of the rear couch light switch on the plate; its \u2212 goes back to the \u2212 lever connector in the plate (see WR21 and EF14)',
    D: [[[2.6, 49], [2.6, 69.6], [D.lrear.x, 69.6], [D.lrear.x, lz + .5]]], lab: { D: [(2.6 + D.lrear.x) / 2 + 4, 69.6] } });
  add({ g: '14', t: 'dc', n: 'Shower light from the plate ' + D.plate.id + ', up the corner and across the ceiling', from: D.plate.id + ' (switched)', to: P.wet.id + ' shower light', prot: '5 A (lights circuit)', note: 'its + is the OUT of the shower light switch on the plate and its \u2212 goes back to the \u2212 lever connector in the plate (see WR21 and EF14). Up the driver wall’s rear corner to the ceiling edge, east along the edge (the straight way is through the roof fan opening, 6 1/4 to 20 1/4 in from the rear doors), through the web of the rib at 21 3/4 (grommet), then across the ceiling at about 26 1/2 in to the light, on the slat at 58 in across',
    D: [[[3.45, 49], [3.45, 75]]], C: [[[9.45, 0], [9.45, 2.5], [lt[0].x, 2.5], [lt[0].x, lt[0].y]]], lab: { D: [3.45, 60], C: [lt[0].x, 30] } });
  add({ g: '14', t: 'dc', n: 'Feed to the dinette switch ' + D.dsw.id + ' on W2', from: 'junction box ' + D.jb.id, to: D.dsw.id + ' switch', prot: '5 A (lights circuit)', note: 'along the cabinet top toward the cab, down the corner behind the planks, into the box through a grommet',
    D: [[[D.jb.x1, 71.4], [D.dsw.x, 71.4], [D.dsw.x, D.dsw.z + .8]]], lab: { D: [118, 71.4] } });
  add({ g: '14', t: 'dc', n: 'Dinette lights ' + D.ld1.id + ' and ' + D.ld2.id + ' from the switch ' + D.dsw.id, from: D.dsw.id + ' (switched)', to: D.ld1.id + ' and ' + D.ld2.id, prot: '5 A (lights circuit)', endsOverride: [['D', [D.ld1.x, lz + .5]], ['D', [D.ld2.x, lz + .5]]], note: 'back up the corner, along the cabinet interior, one drop to each light',
    D: [[[D.dsw.x - 1.1, D.dsw.z + .8], [D.dsw.x - 1.1, 69.4], [D.ld1.x, 69.4], [D.ld1.x, lz + .5]], [[D.ld2.x, 69.4], [D.ld2.x, lz + .5]]], lab: { D: [(D.ld1.x + D.ld2.x) / 2, 69.4] } });
  // ---- passenger wall loads
  add({ g: '14', t: 'ac', n: 'Fridge outlet ' + P.fr.id + ', circuit C', from: 'riser B (120 V)', to: P.fr.id + ' outlet up by the microwave outlet', prot: '15 A (circuit C, the fridge alone)', note: 'circuit C\u2019s own cable, the same cable as the one that comes down riser B from the ceiling (WR12): it leaves the other cable (circuit B/D goes on down to the selector, WR27) at 54 in up, runs west in the free band between S5 and S6 (45 1/4 to 55 1/2 up) just below the microwave cable (WR28) and goes down into the two gang box that it shares with the microwave outlet, at 52 1/2 up like the TV outlet (its own receptacle, 1 7/8 in toward the cab from the microwave one); the fridge outlet is the only outlet on circuit C',
    P: [[[rb(0), 54], [P.fr.x, 54], [P.fr.x, P.fr.z + .9]]], lab: { P: [(rb(0) + P.fr.x) / 2, 54] } });
  add({ g: '14', t: 'ac', n: 'Riser B to the selector ' + P.sel.id + ' (circuit B/D, shared)', from: 'riser B (120 V)', to: P.sel.id + ' common pin', prot: '15 A GFCI breaker B/D', note: 'the middle pin of your 30 A rocker is the common',
    P: [[[rb(0), 54], [rb(0), P.sel.z], [P.sel.x, P.sel.z]]], lab: { P: [rb(0) - 3.2, P.sel.z + 2] } });
  add({ g: '14', t: 'ac', n: 'Selector ' + P.sel.id + ' to the microwave outlet ' + P.mic.id, from: P.sel.id + ' (one end pin)', to: P.mic.id + ' outlet', prot: '15 A GFCI breaker B/D (one load at a time)', note: 'a standard 15 A receptacle (the microwave draws 12.5 A), in the same two gang box as the fridge outlet (WR26), each with its own cable; protected by the GFCI breaker for B/D in the AC panel',
    P: [[[P.sel.x, P.sel.z], [P.sel.x, 54.9], [P.mic.x, 54.9], [P.mic.x, P.mic.z + .9]]], lab: { P: [(P.sel.x + P.mic.x) / 2 + 2, 54.9] } });
  add({ g: '14', t: 'ac', n: 'Selector ' + P.sel.id + ' to the heater outlet ' + P.ht.id, from: P.sel.id + ' (other end pin)', to: P.ht.id + ' outlet beside the tank', prot: '15 A GFCI breaker B/D (one load at a time)', note: 'down behind the planks, drilled through S5 to S3, then along the free band above S2',
    P: [[[P.sel.x, P.sel.z], [P.sel.x, 15.5], [P.ht.x0, 15.5]]], lab: { P: [P.sel.x, 33] } });
  add({ g: '14', t: 'ac', n: 'Counter outlet ' + P.ce.id + ', circuit A: on from the couch outlet ' + D.cout.id, from: D.cout.id + ' couch outlet (through its box)', to: P.ce.id + ' counter outlet, next to the selector', prot: '15 A GFCI (circuit A)', note: 'a third cable out of the couch outlet\u2019s box (the end of WR18): along the free band above S6 to riser A, up riser A and across the ceiling beside the 120 V conduit of WR12, then down riser B into the two gang box that the counter outlet shares with the selector; the cable goes on from that box to the TV outlet (WR37)',
    D: [[[D.cout.x - .6, D.cout.z + .9], [D.cout.x - .6, 62.9], [ra(1) - .4, 62.9], [ra(1) - .4, 75]]], C: [[[RX + 1.7, 0], [RX + 1.7, 68]]], P: [[[rb(0) + .4, 75], [rb(0) + .4, 53], [P.ce.x, 53], [P.ce.x, P.ce.z + .9]]], lab: { D: [ra(1) - .4, 66], C: [RX + 1.7, 40], P: [rb(0) + .4, 64] } });
  add({ g: '14', t: 'dc', n: 'Water pump PL3: its own wire from the fuse block, up riser A, across the ceiling, down riser B', from: '12 V fuse block (10 A fuse)', to: 'PL3 pump beside the heater', prot: '10 A', T: { D: [tail12(2)] }, note: 'the pump draws about 7 A; in riser B it leaves the loom at 24 in up and goes along the free band above S3 (through the notches in S2 to S4); about 16 ft longer than a tap would have been, so each wire is protected by its own fuse',
    D: [[[ra(2), R0], [ra(2), 75]]], C: [[[77.8, 0], [77.8, 68]]], P: [[[rb(1), 75], [rb(1), 24], [105.5, 24], [105.5, 20.6]]], lab: { D: [ra(2), 33], C: [77.8, 6], P: [88, 24] } });
  add({ g: '18', t: 'dc', n: 'Control panel ' + P.pan.id + ' (battery monitor, pump switch, tank levels): its own wire from the fuse block', from: '12 V fuse block (3 A fuse)', to: P.pan.id + ' panel', prot: '3 A', T: { D: [tail12(7)] }, note: 'small 18 AWG, up riser A, across the ceiling and down riser B with the pump wire',
    D: [[[ra(7), R0], [ra(7), 75]]], C: [[[76.7, 0], [76.7, 68]]], P: [[[rb(2), 75], [rb(2), 47.5], [P.pan.x, 47.5], [P.pan.x, P.pan.z - .8]]], lab: { D: [ra(7), 48], C: [76.7, 17], P: [P.pan.x - 1, 47.5 - 3.6] } });
  add({ g: '14', t: 'dc', n: 'Switch ' + P.s11.id + ' to the counter and sink light ' + P.cl.id, from: P.s11.id + ' left rocker', to: P.cl.id + ' light', prot: '5 A (lights circuit)', flow: ['P', 'C'], note: '14 AWG pair behind the covering to riser B (about 27 in), up to the ceiling, then along the slat to the light',
    P: [[[P.s11.x, P.s11.z], [P.s11.x, 61.3], [rb(4), 61.3], [rb(4), 75]]], C: [[[81.8, 68], [81.8, lt[1].y], [lt[1].x, lt[1].y]]], lab: { P: [88, 61.3], C: [88, lt[1].y] } });
  add({ g: '14', t: 'dc', n: 'Switch ' + P.s14.id + ' to the two center-row ceiling lights', from: P.s14.id + ' right rocker', to: 'center row lights, rear and front', prot: '5 A (lights circuit)', flow: ['P', 'C'], endsOverride: [['C', [lt[2].x, lt[2].y]], ['C', [lt[3].x, lt[3].y]]], note: 'two cables, so there is no splice hidden above the plywood: the first goes up riser B and across to the front center light (through the web of the rib at 97 3/8); the second goes from that light back along the center slat, round the A/C opening (above it, through the ribs at 58 3/8 and 37 7/8), to the rear center light; the two meet the front light’s leads in its cutout, where you can reach them',
    P: [[[P.s14.x, P.s14.z], [P.s14.x, 62.2], [rb(5), 62.2], [rb(5), 75]]], C: [[[82.7, 68], [82.7, 34], [lt[3].x, lt[3].y]], [[lt[3].x, lt[3].y], [lt[3].x, 36], [aR, 36], [aR, aT], [lt[2].x, aT], [lt[2].x, lt[2].y]]], lab: { P: [88, 62.2], C: [92, 34] } });
  add({ g: '14', t: 'dc', n: 'Lights feed from ' + D.jb.id + ' to the passenger-wall switches ' + P.s11.id + ' and ' + P.s14.id + ': up through the cabinet top, across the ceiling, down riser B', from: 'junction box ' + D.jb.id, to: P.s11.id + ' and ' + P.s14.id + ' switches', prot: '5 A (lights circuit)', note: 'one 14 AWG pair to the box behind the two-rocker plate; it does not split in the wall. In the box the + goes by two short jumpers to the two rockers, and the − joins the − of WR33 and WR34 in a lever connector. It was missing from the wire list: the switches used to be fed from the 12 V trunk, which was dropped',
    D: [[[D.jb.x0 + 1, D.jb.z1], [D.jb.x0 + 1, 75]]], C: [[[D.jb.x0 + 7, 2.5], [84.5, 2.5], [84.5, 67.5]]], P: [[[rb(7), 75], [rb(7), 63.2], [(P.s11.x + P.s14.x) / 2, 63.2], [(P.s11.x + P.s14.x) / 2, P.s14.z + .9]]], lab: { C: [84.5, 30], P: [83.5, 63.2] } });
  add({ retired: true, g: '18', t: 'dc', n: 'Second dimmer button ED22 to the dimming controller in JB (retired)', from: 'ED22 button (retired)', to: 'dimming controller (retired)', prot: 'none', len: 0, note: 'retired (user, 2026-11-05: no dimming controller; ED22 is now the slide dimmer). The number is not reused. The 18 AWG cable already pulled from the W2 box to JB is not needed: leave it in place as the pull line for the new WR38 and WR39 cables, then keep it as a spare or take it out' });
  add({ g: '14', t: 'ac', n: 'TV outlet ' + P.tv.id + ', circuit A: the end of the chain, on from the counter outlet ' + P.ce.id, from: P.ce.id + ' counter outlet (through its box)', to: P.tv.id + ' outlet under the TV', prot: '15 A GFCI (circuit A)', note: 'the last cable of circuit A: from the two gang box next to the selector up to 54 1/2 in, east behind the TV to the box above the two-rocker plate; the TV outlet is the end of the line, so one cable only reaches it (it used to be the end of WR30, which now stops at the counter outlet)',
    P: [[[P.ce.x - .6, P.ce.z + .9], [P.ce.x - .6, 54.4], [P.tv.x, 54.4], [P.tv.x, P.tv.z + .9]]], lab: { P: [(P.ce.x + P.tv.x) / 2 + 6, 54.4] } });
  add({ g: '14', t: 'dc', n: 'Soft LED strip: the supply pair from ' + D.jb2.id + ' to the slide dimmer ' + D.dim2.id + ' on W2', from: 'strip junction box ' + D.jb2.id, to: D.dim2.id + ' slide dimmer (input)', prot: '10 A, its own circuit (fuse block way 2)', note: 'user (2026-11-05): no dimming controller, one slide or knob dimmer on the wall in the dinette area. This 14 AWG pair (+ and −) takes the strip circuit from the splice in ' + D.jb2.id + ' to the dimmer on W2: through the cab-end side panel (a grommet, like WR24), along the cabinet top toward the cab, down the corner behind the planks and into the box through a grommet, beside the dinette switch feed (WR24). All 6.4 A of the strip runs through the dimmer, so it is 14 AWG all the way',
    D: [[[D.jb2.x1, 69.5], [D.dim2.x - .8, 69.5], [D.dim2.x - .8, D.dim2.z + .8]]], lab: { D: [124, 69.5] } });
  add({ g: '14', t: 'dc', n: 'Soft LED strip: the dimmed power from the slide dimmer ' + D.dim2.id + ' back to ' + D.jb2.id, from: D.dim2.id + ' slide dimmer (output)', to: 'strip junction box ' + D.jb2.id + ' (the splice for the three feeds)', prot: '10 A, its own circuit (fuse block way 2)', note: 'a second 14 AWG pair, the same way as the supply pair (WR38) and tied to it: the dimmed power goes back to ' + D.jb2.id + ', where it splits to the three strips (WR40). A pair, so it works with a dimmer that switches the + (high-side) or the − (low-side); a high-side dimmer leaves the − spare. The old 18 AWG cable (WR36, retired) left in place from W2 to the couch cabinet is the pull line for both',
    D: [[[D.dim2.x - 1.6, D.dim2.z + .8], [D.dim2.x - 1.6, 68.9], [D.jb2.x1, 68.9]]], lab: { D: [100, 68.9] } });
  add({ g: '14', t: 'dc', n: 'Soft LED strip: the three feeds from ' + D.jb2.id + ' to the strips', from: 'strip junction box ' + D.jb2.id + ' (dimmed power)', to: 'strip along the ceiling edge, three runs', prot: '10 A, its own circuit (fuse block way 2)', endsOverride: [['C', [82.5, 1.5], 'F1: driver run'], ['C', [82.5, 66.5], 'F2: passenger run'], ['C', [1.9, 3.4], 'F3: back run']], note: 'LABELS (user, 2026-11-06): tag both ends of every wire 3 in from the end: WR40 F1 +, WR40 F1 − (driver run), WR40 F2 +, WR40 F2 − (passenger run), WR40 F3 +, WR40 F3 − (back run), red for + and black for −, and write the strip name on the strip-end tags. Three 14 AWG cables from the splice in ' + D.jb2.id + ', one to each strip feed: the driver run (about 2 ft cut), the passenger run across the ceiling at 82 1/2 in (about 7 1/2 ft) and the back run along the ceiling edge, through the ribs at 58 3/8, 37 7/8 and 21 3/4 (a grommet in each web; about 8 1/2 ft); the back run is fed from the driver run side. They carry 2.6, 2.6 and 1.1 A (6.4 A in all, through the dimmer). They were part of WR14 before the dimmer moved to W2',
    C: [[[jbc + 6, 2.5], [82.5, 2.5]], [[82.5, 0], [82.5, 66.5]], [[82.5, 3.4], [1.9, 3.4]]], lab: { C: [82.5, 12] } });
  W.forEach((w, i) => { w.id = 'WR' + (i + 1); });
  W.forEach(w => { if (w.len == null) { let d = 0; const seg = pl_ => { for (let i = 1; i < pl_.length; i++) d += Math.hypot(pl_[i][0] - pl_[i - 1][0], pl_[i][1] - pl_[i - 1][1]); }; ['D', 'P', 'C'].forEach(v => (w[v] || []).forEach(seg)); Object.keys(w.T || {}).forEach(v => (w.T[v] || []).forEach(seg)); w.len = d / 12; } });   // the drawn route, its lead-in from the gear area (T) included
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
  return { start: { v: vs[0], pt: first[0][0] }, ends: w.endsOverride ? w.endsOverride.map(e => ({ v: e[0], pt: e[1], tag: e[2] })) : [{ v: vs[vs.length - 1], pt: last[last.length - 1][last[last.length - 1].length - 1] }] };
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
function marker(label, pt, X, Y, col, up, tag) {
  const core = markerCore(label, pt, X, Y, col, up);
  if (!tag) return core;
  const x = X(pt[0]), y = Y(pt[1]), w = label === 'START' ? 48 : 36;
  let by = up ? y - 40 : y + 36; if (by < 34) by = y + 36; if (by > 600) by = y - 40;
  const bx = Math.min(1040 - w / 2, Math.max(30 + w / 2, x));
  const st = 'font-size:11px;font-weight:700;fill:#111;paint-order:stroke;stroke:#fff;stroke-width:3.2px';
  if (x < 200) return core + `<text x="${bx}" y="${by > y ? by + 25 : by - 15}" text-anchor="middle" style="${st}">${tag}</text>`;
  return core + `<text x="${x + 12}" y="${y > 400 ? y - 22 : y + 34}" text-anchor="start" style="${st}">${tag}</text>`;
}
function markerCore(label, pt, X, Y, col, up) {
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
  e.ends.filter(x => x.v === view).forEach(x => parts.push(marker('END', x.pt, X, Y, '#111', false, x.tag)));
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
    if (e.k === 'run' || e.k === 'retired') return;
    if (e.k === 'box' || e.k === 'strip') { const [g] = symbol(e, X, Y); bigs.push(`<g class="itm" data-item="${e.id}"><title>${e.id}: ${esc(e.n)}</title>${g}</g>`);
      if (e.k === 'box') {                       // name the boxes, so a wire can be followed from one to the next
        const xa = X(e.x0), xb = X(e.x1), bx = Math.min(xa, xb), bw = Math.abs(xb - xa), by = Y(e.z1), bh = 6 * (e.z1 - e.z0), nm = e.n.split(/[,(]/)[0].replace(/^Power hub: Class T fuse and shunt$/, 'Class T, shunt').replace(/^TS-30 transfer switch \(30 A\), on the divider panel$/, 'TS-30').replace(/^AC panel \(120 V breakers\), on the divider panel$/, 'AC panel').replace(/^12 V fuse block \(10-way\), on the divider panel$/, 'fuse block').replace(/^Shore charger$/, 'charger').replace(/^Inverter$/, 'inverter').replace(/^Battery$/, 'battery').replace(/^DC-DC charger$/, 'DC-DC').trim();
        const st = 'font-size:9.5px;font-weight:700;fill:#6b3a00;paint-order:stroke;stroke:#fff;stroke-width:2.6px';
        if (bw >= 80 && bh >= 40) bigs.push(`<text x="${bx + bw / 2}" y="${by + bh / 2 + 3.5}" text-anchor="middle" style="${st}">${e.id} ${esc(nm)}</text>`);
        else if (bw >= 50) bigs.push(`<text x="${bx + 4}" y="${/charger/.test(nm) ? by + bh - 5 : by + 12}" style="${st}">${e.id} ${esc(nm)}</text>`);
        else if (bh >= 50) bigs.push(`<text transform="rotate(-90 ${bx + bw / 2 + 3.4} ${by + bh / 2})" x="${bx + bw / 2 + 3.4}" y="${by + bh / 2}" text-anchor="middle" style="${st}">${e.id} ${esc(nm)}</text>`);
        else if (e.id === 'JB2') bigs.push(`<text x="${bx - 4}" y="${by + bh / 2 + 3.5}" text-anchor="end" style="${st}">${e.id}</text>`);   // JB2 has the wires and the START or END marker on its cab side: its label goes on the rear side
        else bigs.push(`<text x="${bx + bw + 4}" y="${by + bh / 2 + 3.5}" style="${st}">${e.id}</text>`);
      }
      return; }
    const [g, cx, cy] = symbol(e, X, Y);
    smalls.push(`<g class="itm" data-item="${e.id}"><title>${e.id}: ${esc(e.n)}</title>` + g + `<text x="${cx + 9}" y="${cy + 15}" style="font-size:8.5px;font-weight:700;fill:#5F5E5A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">${e.id}</text></g>`);
  });
  // the 12 V cables leave the fuse block on the divider panel, go up through the covering into the free band above S2 and run east along it to riser A
  const stub = flip ? '' : `<polyline points="${X(37)},${Y(15.4)} ${X(37)},${Y(17.5)} ${X(76.5)},${Y(17.5)}" fill="none" stroke="#fff" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/><polyline points="${X(37)},${Y(15.4)} ${X(37)},${Y(17.5)} ${X(76.5)},${Y(17.5)}" fill="none" stroke="#9a9a94" stroke-width="8" stroke-linecap="round" stroke-linejoin="round"/>`;
  const pump = flip ? `<rect x="${X(107)}" y="${Y(20)}" width="${X(104) - X(107)}" height="${6 * 8}" rx="6" fill="#D9E2EC" fill-opacity=".9" stroke="#475569" stroke-width="2.2"/><text x="${(X(104) + X(107)) / 2}" y="${Y(16) + 3}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#475569">pump</text>` : '';
  // the gear area (the divider panel, the tray, the end panel): its short runs are on the one-line diagram
  let call = '';
  if (!flip) { const hubItem = items.find(e => /^Power hub/.test(e.n)); if (hubItem) { const tx = (y, t) => `<text x="${X(32.5) - 8}" y="${Y(y)}" text-anchor="end" style="font-size:10.5px;font-weight:700;fill:#6A1B9A;paint-order:stroke;stroke:#fff;stroke-width:3px">${t}</text>`;
    call = `<rect x="${X(32.5)}" y="${Y(16.4)}" width="${X(75) - X(32.5) + 4}" height="${Y(0) - Y(16.4)}" fill="none" stroke="#6A1B9A" stroke-width="1.6" stroke-dasharray="3 4"/>` + tx(8, 'gear area (dotted box): the divider panel,') + tx(5.4, 'the tray, the end panel. WR1 to WR3, WR5, WR6,') + tx(2.8, 'WR8 to WR10, WR13 run inside it: see 5a'); } }
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
