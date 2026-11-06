/* Builds ../electric.html: the electrical and lighting layout.
   Like wallmap.js it reads the plan's own layout from interactive.html in a headless browser and the steel / furring drawing from sides.html
   (diagrams A and D), so the positions follow the plan's sizes. The electrical choices (where each outlet, switch, light, fuse and run goes)
   are the proposal written below as E_*; change them there.
   Run:  node tools/electric.js        (needs playwright + the bundled Chromium; build.sh runs it and skips it if they are missing)
*/
const {chromium} = require(process.env.NODE_PATH + '/playwright');
const fs = require('fs');
const EW = require('./elwires.js');
const { cheatHTML } = require('./wirecheat.js');
const { hubSVG, trayTopSVG, TRAY_PARTS } = require('./elhub.js');
const TP = k => TRAY_PARTS.find(q => q.k === k);      // the parts of the user\u2019s real board on the tray (section 1c; read from the photo): the electrical page draws the gear where the board has it
const fr = v => { let w = Math.floor(v + 1e-9), r = Math.round((v - w) * 16); if (r === 16){w++;r=0;} let n=r,d=16; while(n&&n%2===0){n/=2;d/=2;} return (n? (w?w+' ':'')+n+'/'+d : ''+w); };
const BOXES = {   // every box you wire by hand has a short name: BX1 to BX9 (JB and JB2 keep theirs); never renumber, a new box takes the next number
  BX1: { n: 'Rear doors plate', where: 'driver wall, 1 3/4 in along, 48 up', what: 'two switches side by side in one deep two gang box: the rear couch light (ED7) and the shower light (ED11)', wires: 'WR21 in; WR22 and WR23 out', s: 'rear doors plate (ED11)', fig: 'EF14' },
  BX2: { n: 'Couch box on S6', where: 'driver wall, on furring rail S6, 64 to 66 in along, 57 1/4 up', what: 'a deep two gang box with a divider: the couch outlet ED10 (120 V, left) and the switch ED19 (12 V, right) for the right couch light ED18', wires: 'WR18 in; WR19 and WR30 on (120 V); WR20 (12 V)', s: 'couch box on S6 (ED10, ED19)', fig: 'EF21' },
  BX3: { n: 'Dinette table outlet box', where: 'driver wall, 121 1/2 in along, 34 up, over the dinette table', what: 'the outlet ED15 (120 V duplex)', wires: 'WR19 in', s: 'dinette table outlet (ED15)', fig: 'not drawn yet' },
  BX4: { n: 'Dinette back wall box (W2)', where: 'driver wall, on W2, 153 in along, 44 3/4 to 48 up', what: 'the dinette light switch ED12 and the slide dimmer ED22 for the soft LED strip', wires: 'WR24 in; WR25 out; WR38 in and WR39 out for the dimmer', s: 'dinette back wall, W2 (ED12, ED22)', fig: 'EF13' },
  BX5: { n: 'Fridge and microwave outlet box', where: 'passenger wall, centered on 55 in along (54 to 56), 60 up, just above S6, above the microwave', what: 'two gang box: the microwave outlet EP4 and the fridge outlet EP3 (120 V)', wires: 'WR37 in (circuit A, the end of that branch); WR28 in (from the selector)', s: 'fridge and microwave outlets (EP3, EP4)', fig: 'not drawn yet' },
  BX6: { n: 'Selector and counter outlet box', where: 'passenger wall, 71 to 73 in along, 50 up', what: 'two gang box: the heater or microwave selector EP9 and the counter outlet EP15 (120 V)', wires: 'WR27 in; WR28 and WR29 out; WR41 in (the end of circuit A)', s: 'selector and counter outlet (EP9, EP15)', fig: 'EF22 and EF23' },
  BX7: { n: 'Heater outlet box', where: 'passenger wall, 85 to 87 in along, 12 to 18 up', what: 'the heater outlet EP7 (120 V, 15 A)', wires: 'WR29 in', s: 'heater outlet (EP7)', fig: 'not drawn yet' },
  BX8: { n: 'TV outlet box', where: 'passenger wall, 92 in along, 60 up, above the cab-side end of the kitchen nook (the nook is 76 to 93 1/4), just above S6, behind the TV', what: 'the TV outlet EP6 (120 V), a single gang box', wires: 'WR30 in; WR37 and WR41 out', s: 'TV outlet (EP6), above the kitchen nook', fig: 'EF20' },
  BX9: { n: 'Switch plate next to the sliding door', where: 'passenger wall, 100 1/4 to 102 1/4 in along, 52 1/4 up, under the TV; the sliding door opening starts at 104', what: 'two 12 V rockers on one plate: EP11 (left, the ceiling light over the counter and sink) and EP14 (right, the two center-row ceiling lights)', wires: 'WR35 in; WR33 and WR34 out', s: 'switch plate by the sliding door (EP11, EP14)', fig: 'EF19' },
  JB: { n: 'Lights junction box', where: 'couch cabinet, 69 1/2 to 73 in along, 70 3/4 to 73 1/4 up', what: 'the splices for the lights circuit (5 A)', wires: 'WR16 in; WR20, WR21, WR24 and WR35 out', s: 'lights junction box', fig: 'EF15 and EF17' },
  JB2: { n: 'Strip junction box', where: 'couch cabinet, 69 1/2 to 73 in along, 67 3/8 to 69 7/8 up, under JB', what: 'the splices for the soft LED strip (10 A)', wires: 'WR14 in; WR38, WR39 and WR40', s: 'strip junction box', fig: 'EF16 and EF18' }
};
function boxTable() {
  const rows = Object.keys(BOXES).map(id => { const b = BOXES[id];
    return `<tr${/^BX/.test(id) ? ` id="item-${id}"` : ''}><td><b class="id" data-go="${id}" role="button" tabindex="0" title="Show ${id} on the diagram">${id}</b></td><td>${esc(b.n)}</td><td>${esc(b.where)}</td><td>${esc(b.what)}</td><td>${esc(b.wires)}</td><td>${esc(b.fig)}</td></tr>`; }).join('');
  return `<div class="tw"><table><thead><tr><th>Box</th><th>What it is</th><th>Where (in from the back mark, up from the floor)</th><th>What is in it</th><th>Wires</th><th>Drawing</th></tr></thead><tbody>${rows}</tbody></table></div>`;
}
const ITEM_INFO = {};   // id -> {n, where, note}, for the click popups on the electric page
const esc = s => String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;');

// ------------------------------------------------------------------ the proposal (x = inches from the back mark, z = inches up from the floor)
// kinds: out120 = 120 V outlet, sw = switch, lt = light, strip = LED strip (x0..x1 at z), box = a mounted unit, inlet, panel, run = a wire run (vertical x from z0 to z1)
const E_DRIVER = pl => { const oz = pl.win && pl.win.cz0 - 5 < 36 ? pl.win.cz0 - 5 : 36, tc = (pl.tbl[0] + pl.tbl[1]) / 2, q1 = pl.bedLen / 4, q3 = 3 * pl.bedLen / 4, lz = pl.cabBot - .5; return [
  {k:'box',   n:'Battery, 280 Ah (assumed lithium)',          x0:52, x1:73, z0:0, z1:9.5, note:'where the plan has it, in front of the wheel well; main fuse (Class T, 250 A) within 7 in of its + post. The gear shelf slides over it, 1 in above its top, so the posts need right-angle lugs'},
  ...(pl.gear ? [
    {k:'box', n:'Inverter, BELTTT 2000 W (inverter only: no charger, no transfer switch)', x0:TP('inv').x0, x1:TP('inv').x1, z0:11, z1:11 + TP('inv').h, note:'on the pull-out tray over the battery (the position on your real board, section 1c), ' + fr(TP('inv').z0) + ' to ' + fr(TP('inv').z1) + ' in out from the wall; its battery cables are 2/0 AWG to the bus with a loop about 2 ft longer than a fixed run so the shelf can slide out (Class T 250 A fuse within 7 in of the battery post, fixed; not the 3 ft cables it comes with); its AC output goes to the transfer switch on the hub board; the remote (23 ft cable) goes to ED20 on the couch wall, by the couch outlet'},
    {k:'box', n:'DC-DC charger, LiTime 60 A', x0:TP('dc').x0, x1:TP('dc').x1, z0:11, z1:11 + TP('dc').h, note:'on the pull-out tray (the position on your real board, section 1c), ' + fr(TP('dc').z0) + ' to ' + fr(TP('dc').z1) + ' in out from the wall; 2 AWG from the starter battery (about 15 ft plus a 2 ft loop for the shelf: 4 AWG would lose 3.6% on the way, 2 AWG 2.5%) with an 80 A fuse at the starter battery, 2 AWG to the battery bus with an 80 A fuse and a loop; the size is as you measured it (16 x 9 x 4.5). Its own diagram (the LiTime manual picture): the starter battery goes to the DC INPUT end, the house battery to the DC OUTPUT end, each with an optional fuse or breaker on the red wire; your 100 A waterproof breaker sits on the INPUT side at the unit (the unit is turned end for end on your board, so input is its right end), a second layer beside the 80 A fuse at the starter battery; the OUTPUT side has none yet, so the 80 A at the bus (WR5) still has to be fitted. Its dial (GEL, AGM, LFP, DC LOAD) goes to LFP for a lithium battery; its small terminal strip (D+, IN+, IN+, LC, with a jumper in the picture) is explained only in its manual'},
    {k:'box', n:'Shore charger, VEVOR 80 A (14.6 V lithium)', x0:TP('ch').x0, x1:TP('ch').x1, z0:11, z1:11 + TP('ch').h, note:'on the pull-out tray (the position on your real board, section 1c), ' + fr(TP('ch').z0) + ' to ' + fr(TP('ch').z1) + ' in out from the wall; its AC input cord also needs a loop for the shelf; AC input from the shore side only, on its own 15 A breaker (about 11 A at 120 V), never from the inverter; 2 AWG to the battery bus with a 100 A fuse; the size is as you measured it (9 1/2 x 7 x 4 thick)'},
  ] : []),
  {k:'box',   n:'Power hub: Class T fuse and shunt',            x0:71.4, x1:74, z0:9.6, z1:15.9, note:'what is left of the old hub board, on the closet\u2019s end panel above the wheel well, facing the battery: the Class T fuse holder (within 7 in of the battery post) and the shunt (EF4). The DC bus bars are on the pull-out tray (red 56 1/4 to 58 3/8 in along, black 56 1/4 to 58 in), the TS-30, the AC panel and the 12 V fuse block are on the divider panel at 34 to 38 3/4 in (ED23 to ED25, EF3). The inverter and the two chargers are on the tray too, over the battery. The couch front under the deck is open (not covered), so all of it is reached from the aisle without a hatch'},
  {k:'inlet', n:'Shore power inlet (30 A)',                    x:9, z:15.75,  note:'on the outside of the driver wall in the cover plate CP (CP is 4 3/4 to 13 1/4 in along, 10 3/4 to 16 3/4 up, a plate and not a hole, so it is cut for the inlet): 9 in along and 15 3/4 up, 2 in above the middle of CP so that its back clears the furring rail S2 (S2 is 10 1/4 to 13 3/4 up and sits straight on the steel). A 3 in inlet flange then spans 14 1/4 to 17 1/4, about 1/2 in over the top edge of CP: check your inlet against the plate before you cut. Moved here from 80 in along, 21 up. The 30 A cable (10 AWG in flexible conduit, about 8 ft) runs inside the wall in the free band above S2, which is 13 3/4 to 19 1/2 up and clear of the couch wall-post screws (they go into S1 and S2), to the closet’s rear panel at about 73 in, then down to the hub board and its 30 A breaker; where it drops past S2 it needs a groove in the back of S2 or a gap. The couch frame’s back rail (13 1/2 to 17 up) is in front of the spot, so reach the inlet’s back with the couch lifted out, or cut a small access panel in the plywood'},
  {k:'lt',    n:'Light under the cabinet over the couch, rear (left) of two', x:pl.bedX0 + pl.bedLen / 4, z:lz, note:'user: ED7 will be 2, centered under the cabinets above the couch. 12 V LED on the underside of the wall cabinet (bottom at ' + fr(pl.cabBot) + ' in), a quarter of the way along the couch (' + fr(pl.bedX0) + ' to ' + fr(pl.bedX1) + '), so the two lights are centered on its two halves; this one, nearer the rear doors, is on the second switch of the plate at the rear doors (ED11; the other light has its own switch next to it); the wire comes down from inside the cabinet'},
  {k:'lt',    n:'Light under the cabinet, dinette rear seat',  x:(pl.bA[0] + pl.bA[1]) / 2 + 6, z:lz, note:'centered over the rear bench seat (' + fr(pl.bA[0]) + ' to ' + fr(pl.bA[1]) + '), then 6 in toward the table; on the dinette switch'},
  {k:'lt',    n:'Light under the cabinet, dinette cab-end seat', x:(pl.bB[0] + pl.bB[1]) / 2 - 6, z:lz, note:'centered over the cab-end bench seat (' + fr(pl.bB[0]) + ' to ' + fr(pl.bB[1]) + '), then 6 in toward the table; on the dinette switch. These two replace the single light I had over the table'},
  {k:'out120',bx:'BX2', n:'Couch outlet (120 V duplex, two plugs)', x:64, z:57.25, note:'the rear-door end gang of a two gang box on furring rail S6 (57 1/4 up, on the 3 1/2 in rail), above the nook behind the couch (it was 44 up, which is inside the nook now; user: the outlet can be in the same box as the couch light switch ED19, devices about 2 in apart: outlet 64, ED19 66 (the box was a three gang box with the dimmer button ED14, now retired); the box is about 4 1/2 wide, 62 3/4 to 67 1/4, clear of the S6 joint at 71 1/4 and 5 in from the inverter remote ED20): a duplex outlet (two plugs) on circuit A (GFCI), 14 AWG: circuit A\u2019s first outlet and its branching point: the cable from the AC panel comes in here (WR18) and two more leave, one to the dinette outlet (WR19) and one to the TV outlet (WR30), all three pigtailed to the outlet in the box: use a deep two gang box with a divider: 120 V and 12 V must not share a compartment, so the divider goes between this outlet and the switch ED19 next to it; the 120 V side holds the three cables and the outlet (about 18 cu in), the 12 V side the switch and its wires. In box BX2: how it is wired is drawing EF21'},
  {k:'sw',    bx:'BX1', n:'Switch plate at the rear doors (shower light, rear couch light)', x:1.75,  z:48, note:'2 gang: the wet bath light over the shower (user: ED11 is for the shower light only) and the rear (left) one of the two lights under the cabinet over the couch (user: its switch will be there too). The roof fan has no switch (user: it operates without one): its 12 V feed is straight from the fuse block, fused, and it is controlled at the fan itself. One deep two gang box with the two switches side by side (user, 2026-11-06: the switches will be side by side; she is using a deep two gang box), so the one box holds both switches, the two lever connectors and the jumpers; it was two single gang boxes one over the other. FIT: a two gang box is about 4 in wide, wider than the 3 1/2 in the plan shows at this corner; the user made room for it (2026-11-06), so nothing more to check on the width'},
  {k:'sw',    bx:'BX4', n:'Light switch on the dinette\u2019s back wall (W2)', x:pl.cab - 1, z:48, note:'on W2, the 3/4 in floor-to-ceiling wall that separates the dinette from the driver\u2019s seat (user: ED12 is on the back wall of the dinette), on its dinette face, 48 in up (10 in above the bench back at 38) and about 3 in out from the driver wall, so it is seen here at the corner of the driver wall with W2; the two lights under the cabinet over the dinette seats only (user: the switch will only be for the dinette lights; the ceiling light over the countertop and the sink has its own switch on the passenger wall). W2 is solid plywood with no cavity, so the switch goes in a shallow surface-mount box on its face; the wire comes down the corner behind the planks and into the side of the box through a 1/2 in hole in the plank (a grommet in it). Move the box along W2 if you would rather reach it from the middle of the bench'},
  {k:'strip', n:'Soft LED strip, ceiling edge, driver side run (154 in)', x0:1, x1:pl.cab - 1, z:73, note:'one of three runs of the strip you found: BTF-LIGHTING FCOB (flip chip COB, no dots) warm white 2700 K, 12 V, 336 LEDs/m, 8 W/m (about 2.4 W a foot), 8 mm wide, CRI 90+, double-layer copper PCB, 3M adhesive backing, cuttable at the marked spots, with a 5.5 x 2.1 mm DC plug on each end of a 16.4 ft (5 m) reel (the listing says UL listed: look for the UL mark and file number on the package). It sits in an aluminum channel with a frosted diffuser (the channel must take an 8 mm strip), at the ceiling edge, aimed up so it glows off the cedar ceiling. Cut off the plugs and solder the feed wires at the cut spots, since the plugs loosen with vibration. The wall cabinets run up to the ceiling here, so the channel sits on the top front edge of the cabinets behind a 1 in lip. Fed from the strip junction box JB2 by WR40, in the middle of each 154 in side (the user chose the middle feed: the far end stays within about 7 ft of power and the brightness is more even)'},
  {k:'retired', n:'Dimmer push button at the couch (retired)', x:68, z:57.25, note:'retired (user, 2026-11-05: no dimming controller; one slide dimmer on the dinette wall instead, ED22): it was a momentary push button in the box on S6 beside the couch outlet, 68 in along. The number is not reused; its wire, WR17, is retired with it'},
  {k:'out120',bx:'BX3', n:'Outlet over the dinette table (120 V duplex)', x:tc, z:oz, note:'on the wall just over the table (its top is at 29 in), in the middle of it, clear of the backrests (38 in); the end of one branch of circuit A: one cable in from the couch outlet (WR19)' + (pl.win ? '; moved down from 36 to ' + fr(oz) + ' in up because the side window (its frame starts at ' + fr(pl.win.cz0 - 1.5) + ') is now over the table' : '') + '; circuit A (GFCI)'},
  {k:'run',   n:'Driver wall run: A/C, 12 V and lights feed',          x:76.5, z0:11, z1:75, note:'up inside the wall behind the planks (4 1/2 in space) to the ceiling, jogged from the hub board (72 to 74) to 76 1/2 in so that it climbs just past the front frame V6 of the nook behind the couch (74 to 75 1/2) and not through the nook (drill S5, do not notch it): A/C 6 AWG pair in its own loom, plus the inverter remote\u2019s 23 ft cable (to ED20), plus the 12 V circuit wires from the fuse block, each its own wire (the strip 14 AWG, the fan 14 AWG, the lights 14 AWG, the dimmer button 18 AWG, and the pump 14 AWG and the control panel 18 AWG, which go on across the ceiling to the passenger wall run: there is no shared 12 V trunk). Grommet where it crosses the top steel'},
  {k:'run',   n:'Cab charge cable (DC-DC input)',              x:70, z0:0, z1:1,  note:'2 AWG from the starter battery fuse (80 A) under the van along the driver side frame to a sealed floor grommet next to the battery'},
  {k:'lt',    n:'Light under the cabinet over the couch, cab-end (right) of two', x:pl.bedX0 + 3 * pl.bedLen / 4, z:lz, note:'the second of the two lights under the cabinet over the couch (user: ED7 will be 2, centered), three quarters of the way along it, the one closer to the cab; 12 V LED on the underside of the wall cabinet; on its own switch right next to it (the next item). Added last, so no ED number moved'},
  {k:'sw',    bx:'BX2', n:'Switch for the cab-end (right) couch light, next to the couch outlet', x:66, z:57.25, note:'user: ED19 and ED14 should be next to each other in the same box, where the dimmer button was (the box on S6, 57 1/4 up), and the outlet ED10 could be in that box too. The dimmer button ED14 is retired now (one slide dimmer on the dinette wall, ED22), so this is the two gang box on S6 with the couch outlet: outlet ED10 at 64, this switch at 66, devices about 2 in apart, with a divider between them (120 V and 12 V must not share a compartment). A small 12 V rocker, on or off, for the cab-end light ED18 only. Its two cables (WR20: the feed from JB comes down behind the covering to the box, the switched wire goes up again to the light inside the wall cabinet) are 12 V and stay on the divider\u2019s 12 V side. If you want this switch somewhere else (it used to be 3 in toward the cab from the light), say so. In box BX2: how it is wired is drawing EF21'},
  {k:'remote', n:'Inverter remote (BELTTT, with its LCD display and on/off)', x:55.5, z:57.25, note:'user: put it by the couch. On furring rail S6 next to the two gang box with the couch outlet (ED10, 64) and the right couch light\u2019s switch (ED19, 66), 8 1/2 in rearward of the outlet, so it is under the cabinet light ED18 (62 1/2 up) with 5 in to spare. About 4 1/2 in wide is allowed (53 1/4 to 57 3/4): its size was not in the listing, so measure it and tell me. Its own 23 ft cable (not a wire of the list) goes from the inverter on the gear shelf, with a loop for the shelf, a few inches along the wall to the driver wall run, up it to the free band above S6 (61 1/2 up), along that band to 55 1/2 and down to the remote: about 8 ft, so 15 ft to spare; with the 12 V wires and at least 2 in from the 120 V (the couch outlet\u2019s cable runs in the same band, WR18); the plug end must pass the grommets. Blocking behind the planks like the outlet box has. Moved here from the passenger wall (it was EP15, beside the control panel)'},
  {k:'box', name:'JB', n:'Lights junction box (the splices for the lights)', x0:69.5, x1:73, z0:70.8, z1:73.3, note:'user: the junction box cannot be against the outside steel, and it goes in the wall cabinet. Inside the wall cabinet over the couch (0 to 74), at its cab end: on the inside face of the cab-end side panel, just under the top panel, toward the back. Wood behind it, not the roof or the van steel; reached through the cab-end door. The lights feed (WR16) comes in through a grommet in that side panel from the driver wall run; the cabinet-light wires leave along the cabinet top, and the feed to the passenger-wall switches (WR35) leaves up through the top. Called JB at the user\u2019s word (it was numbered ED21; that number is not reused), added last so no ED number moved. The soft LED strip splices are in the second box, JB2, just under this one. WIRING (drawing EF15): five pairs of 14 AWG meet here: WR16 comes in from the fuse block, and WR20, WR21, WR24 and WR35 go out. The five + wires join in one 5 port lever connector and the five − wires in another (rated 20 A or more; with only 3 port connectors use three per side and two short jumpers: two connectors and one jumper join only four wires; drawing EF17). A box about 4 in square and 2 in deep holds them, the real box to be checked'},
  {k:'sw', bx:'BX4', n:'Slide dimmer for the soft LED strip, with the dinette light switch', x:pl.cab - 1, z:44.75, note:'user (2026-11-05): one slide or knob dimmer, no dimming controller box, on the wall in the dinette area. It goes where the second push button was: the shallow surface-mount two gang box on W2 with the dinette switch (ED12), ED12 above, this dimmer 3 1/4 in under it (about 3 in out from the driver wall, 44 3/4 in up). CHOSEN (the user ordered it on 2026-11-05): the KEYGMA 12 to 24 V DC slide dimmer, 10 A, 160 W, a rocker paddle for on/off and a slider for brightness, wall plate included, not for 120 V (all from its Amazon listing; nothing measured yet). A one piece 12 V DC PWM dimmer rated 10 A or more (the strip is about 6.4 A at full brightness and ALL of it runs through the dimmer), with an on/off paddle or push and a slider or knob; made for 12 V only (a 120 V wall dimmer cannot work). It switches and dims the whole soft strip from this one place. The supply pair comes from JB (WR38) and the dimmed power goes back to JB (WR39), where it splits to the three strips (WR40). Check on the real dimmer: its depth against the shallow box, whether it dims the + (high-side) or the −, and its temperature rating. It used to be the second dimmer push button. Added last, so no number moved'},
  {k:'box',   n:'TS-30 transfer switch (30 A), on the divider panel', x0:33.9, x1:38.65, z0:2.5, z1:12.15, note:'on the divider panel\u2019s outer face, the face that looks toward the rear doors (the divider is the board at 38 3/4 in that the tray\u2019s rear slide bolts to); 1 1/2 to 8 3/4 in out from the driver wall, 2 1/2 to 12 up, 4 3/4 in deep, on end (EF3). Shore power comes in from the inlet (WR7) along the free band above S2, the inverter\u2019s output through a grommet in the divider (WR8), and the output goes on to the AC panel (WR9)'},
  {k:'box',   n:'AC panel (120 V breakers), on the divider panel', x0:35.65, x1:38.65, z0:6.4, z1:11.4, note:'on the divider panel\u2019s outer face beside the TS-30, 10 1/2 to 17 1/2 in out from the driver wall, 6 1/2 to 11 1/2 up, about 3 in deep (typical size, EF3): the main from the TS-30 (WR9) and the breakers for circuit A (15 A GFCI), B/D (15 A GFCI: the heater is next to water) and C (15 A) and the shore charger (15 A); the circuits leave through the covering above it into the free band above S2 (WR12)'},
  {k:'box',   n:'12 V fuse block (10-way), on the divider panel', x0:36.65, x1:38.65, z0:2.6, z1:6.1, note:'on the divider panel\u2019s outer face, 19 to 25 in out from the driver wall, 2 1/2 to 6 up, about 2 in deep (typical size, EF3): fed from the bus on the tray (WR13); five ways used (lights, strip, fan, pump, control panel), each with its own wire up the driver wall run'},
  {k:'box', name:'JB2', n:'Strip junction box (the splices for the soft LED strip), under JB', x0:69.5, x1:73, z0:67.4, z1:69.9, note:'user (2026-11-05): a second junction box next to JB for the soft LED strip, so the lights splices (5 cables) and the strip splices (6 cables) are not all in one small box. Same size as JB on the plan (about 3 1/2 x 2 1/2 in; the real box needs room for 14 AWG lever connectors), in the wall cabinet over the couch on the same cab-end side panel, just under JB, 1 in below it (if the panel has no room: on the underside of the top panel just rear of JB). The place is my choice, not the user\u2019s. It holds the 10 A strip circuit: the supply from the fuse block comes in (WR14), goes on to the slide dimmer ED22 on W2 (WR38), comes back dimmed (WR39) and splits to the three strips (WR40). The + and the − each join with lever connectors rated 20 A or more, because the + carries the whole 6.4 A. Added last, so no ED number moved; the name JB2 is used in place of its number. WIRING (drawing EF16, drawn for a dimmer that switches the +): 12 wires meet here. A 2 port connector joins WR14 + and WR38 + (the supply to the dimmer); a 5 port connector joins WR39 + (the dimmed power back) with the three WR40 + feeds F1, F2, F3; a second 5 port connector joins WR14 −, WR38 − and the three WR40 − feeds; WR39 − is a spare, capped. All rated 20 A or more. If the KEYGMA turns out to switch the −, the roles of the + and − swap on the dimmed side. With 3 port connectors only: drawing EF18 (6 connectors and 3 jumpers)'},
]; };
const E_PASS = pl => { const sl = pl.lights.filter(l => l.x > 6 && l.x < 6 + pl.panW)[0] || { x: 6 + pl.panW / 2, y: pl.P.vanW - pl.panD / 2 }, wbx = sl.x - 6, wby = sl.y, cl = pl.lights.filter(l => l.x - 6 >= pl.panW).sort((a, b) => a.x - b.x); return [
  {k:'lt',    n:'Wet bath light (ceiling, IP65), over the shower', x:wbx, z:pl.ceilF - .5, note:'over the middle of the stall: ' + fr(wbx) + ' in along the wall, ' + fr(wby) + ' in across from the driver wall, on the slat (the exact center, 18 in, is under a rib, so it sits 2 1/2 in toward the cab); a wet-rated (IP65) LED; one of the four ceiling lights (the two others are in the center row, EP12 and EP13). Switched at the rear doors plate'},
  {k:'lt',    n:'Ceiling light over the countertop and the sink', x:cl[0] ? cl[0].x - 6 : 89.4, z:pl.ceilF - .5, note:'one light over both, about the middle of the counter cabinet and the sink cabinet together (58 to 123), ' + fr(cl[0] ? cl[0].y : 58) + ' in across from the driver wall, on the slat and 2 in clear of the rib at 97 3/8; on its own 12 V switch, the left rocker (EP11) of the two-rocker plate under the TV, not on the dinette switch'},
  {k:'out120',bx:'BX5', n:'Fridge outlet, up by the microwave outlet (120 V)',    x:56, z:60,  note:'user: the fridge outlet is up by the microwave outlet, not behind the fridge platform (it was at 47 in along, 6 up), at the same height as the TV outlet (EP6, 60 up; user, 2026-11-06: BX5 is at 55 along on the blue line at the bottom, and 60 up), and (user: \'it can be in the same box\') in the SAME two gang box as the microwave outlet (EP4): the two receptacles side by side, 2 in apart, the fridge one toward the cab, on blocking just above S6 (a two gang box is about 4 in tall, so it spans about 58 to 62 up); circuit A (GFCI; user, 2026-11-06: WR30 powers the fridge outlet through the TV outlet: WR30 to the TV outlet, then WR37 on to the fridge outlet), a standard 15 A receptacle (the fridge plugs in at its top, so its cord goes up the back of the fridge to here). Two separate receptacles, one for each circuit: the microwave one is on circuit B/D and this one on circuit A, so do not share one duplex receptacle between them'},
  {k:'out120',bx:'BX5', n:'Microwave outlet (120 V, through the selector)',    x:54, z:60, note:'a fifth outlet you did not list: the microwave (1500 W) needs its own, on the wall above it (the microwave is 36 to 58 along and its top is about 55 up), in the same two gang box as the fridge outlet (EP3), at 60 up (user, 2026-11-06: BX5 is at 55 along on the blue line at the bottom, and 60 up), the same height as the TV outlet (EP6), on blocking just above S6; circuit B/D, fed through the selector (one end pin of your 30 A rocker), 14 AWG, with a standard 15 A receptacle (the microwave draws 12.5 A). Drop it if the microwave plugs in elsewhere'},
  {k:'panel', n:'Control panel (battery monitor, pump switch, tank levels)', x:66, z:50, note:'12 V, small 18 AWG, 3 A'},
  {k:'out120',bx:'BX8', n:'TV outlet (120 V), above the kitchen nook, behind the TV', x:92, z:60, note:'user (2026-11-06): BX8 is at 92 along and 60 up, above the cab-side end of the kitchen nook (the nook is 76 to 93 1/4) and behind the TV (the TV is 76 1/2 to 103 1/2 along and its bottom is at 54), in a single gang box on blocking just above furring rail S6 (S6 is 55 1/2 to 59 up): the TV plug is hidden, so use a right-angle plug and check that the TV mount clears the box. It was at 96 in along, 52 1/2 up, under the TV, then centered over the nook (84 5/8). Near the sink, so circuit A (GFCI): WR30 comes in from the couch outlet (down the wall run at 73 and along above S6) and this box is where circuit A branches: WR37 goes on to the fridge outlet EP3 (box BX5), the end of that branch, and WR41 to the counter outlet EP15 (box BX6), the end of the other (user, 2026-11-06). Three cables meet in this box, so a deep two gang box (about 37 cu in) or a 4 in square box has room. Wiring: drawing EF20'},
  {k:'box',   bx:'BX7', n:'Hot water heater outlet (120 V, 15 A, circuit B/D)', x0:85, x1:87, z0:12, z1:18, note:'user: the heater is a KENUOS SY-15, a plug-in unit (1500 W, 12.5 A at 120 V, its manual calls for a 15 A circuit): a single 15 A receptacle in a box beside the hot water tank (87 to 101), level with it now that the heater sits on the fresh tank (10 3/4 to 23 3/4 up); 14 AWG, fed through the selector (the other end pin of your 30 A rocker, on the shared 15 A breaker B/D); the heater\u2019s own cord plugs into it; the heater is next to water, so circuit B/D has a GFCI breaker in the AC panel (ED24)'},
  {k:'strip', n:'Soft LED strip, ceiling edge, passenger side run (154 in)', x0:1, x1:pl.cab - 1, z:73, note:'the other long run, same BTF-LIGHTING FCOB strip and channel, at the top of the wall covering; over the sliding door opening (104 to 155, up to 67 in) the channel carries on along the header at 73 in. Fed through the passenger wall run'},
  {k:'sel',   bx:'BX6', n:'Heater or microwave selector (your 30 A SPDT KCD3 rocker, ON-OFF-ON)', x:71, z:50, note:'your 30 A SPDT rocker (KCD3, 125/250 V AC, 3 pins, ON-OFF-ON), in a two gang box with the counter outlet EP15, does this, with one change from my first plan: it is a single pole, so the two circuits now share ONE breaker (a 2 pole switch was what let each keep its own). Breaker B/D (a 15 A GFCI breaker, 14 AWG) feeds the middle pin, the common; one end pin goes to the microwave outlet\u2019s hot and the other end pin to the heater outlet\u2019s hot (14 AWG both); neutrals and grounds go straight through, not switched. One end position: only the microwave is live; the other end: only the heater; middle: neither. 15 A is enough because only one load can run at a time (the microwave is 12.5 A, the SY-15 heater 12.5 A); 12.5 A is close to the 12 A that a 15 A breaker should carry for hours, so run nothing else on this circuit (the heater cycles with its thermostat). Before wiring, check the pins with a continuity tester: in the middle position no pin connects to another; in each end position the common beeps to one end pin only (if the middle pin is not the common, the one that beeps to both is). The terminals are 1/4 in (6.3 mm) tabs: crimp fully insulated female spade terminals for 16 to 14 AWG (blue) on the wires and slip a heat shrink boot over each, or mount the switch in a single gang plastic box, so no live terminal is bare; measure its panel cutout before you cut the plate. Turn the microwave off before you move the switch. Label it (microwave, off, heater). It sits beside the control panel so you choose before you cook or heat water; the heater only warms the tank while the switch is on its side. In box BX6: how it is wired is drawing EF22'},
  {k:'run',   n:'Passenger wall run: 120 V circuits and 12 V branches',   x:73, z0:8, z1:75, note:'down inside the wall behind the planks from the ceiling: 120 V in flexible conduit (14 AWG), the pump (14 AWG) and control panel (18 AWG) wires in a separate loom (each comes all the way from the hub fuse block, with its own fuse there); they go sideways behind the planks through notches in the furring'},
  {k:'sw',    bx:'BX9', n:'Light switch for the ceiling light over the countertop and the sink', x:102.25, z:52.25, note:'user: EP11 can be on the same plate as EP14, and make sure it is under the TV. One of two 12 V rockers on a small two-rocker plate (about 4 1/2 in wide and 2 1/2 tall, 99 to 103 1/2 in along and 51 to 53 1/2 up) on the wall strip under the TV (the TV is 76 1/2 to 103 1/2 and its bottom is at 54), just rear of the sink and above the dish towel hook (98 1/2, 50 up: the folded towel hangs 94 1/2 to 102 1/2, up to 51, so the plate clears it); this is the left rocker (EP14 is the right one). It switches only the ceiling light over the countertop and the sink (EP2). 14 AWG pair behind the covering to the passenger wall run (73), about 27 in away, then up to the ceiling. My placement on the strip, say if you want the two rockers the other way round. In box BX9 with EP14: how it is wired is drawing EF19'},
  ...(pl.lights.length > 3 ? [
    {k:'lt', n:'Ceiling light, center row, rear one (36 asked for)', x:pl.lights[2].x - 6, z:pl.ceilF - .5, note:'user: two more ceiling lights, 12 V, one at 36 centered and one around 100 centered. This one is centered across the van (' + fr(pl.lights[2].y) + ' in from the driver wall) and ' + fr(pl.lights[2].x) + ' in from the rear-door edge (asked for 36; it is kept 2 in clear of the roof rib at 37 7/8, so it moved 1/8 in), on the slat; on EP14, the right rocker of the plate under the TV'},
    {k:'lt', n:'Ceiling light, center row, cab-side one (around 100 asked for)', x:pl.lights[3].x - 6, z:pl.ceilF - .5, note:'the other center-row light, ' + fr(pl.lights[3].y) + ' in from the driver wall and ' + fr(pl.lights[3].x) + ' in from the rear-door edge (asked for around 100; the roof rib at 97 3/8 is 2 3/4 wide, so it sits 2 in clear of it, on the cab side), on the slat; on the same switch as the other center-row light'},
    {k:'sw', bx:'BX9', n:'Light switch for the two center-row ceiling lights', x:100.25, z:52.25, note:'user: the switch for these will be to the left of the sink on the wall, and EP11 is on the same plate (under the TV). The right rocker of the two-rocker plate (EP11 is the left one), 99 to 103 1/2 in along and 51 to 53 1/2 up, on the wall strip under the TV between the jar nook (ends at 94 3/4) and the sliding door opening (starts at 104), above the dish towel hook. The sink is at 103 to 123 and the opening starts at 104, so the strip is the only wall rear of the sink. 14 AWG pair behind the covering to the passenger wall run (73), about 28 in away, then up to the ceiling junction box. In box BX9 with EP11: how it is wired is drawing EF19'}
  ] : []),
  {k:'out120', bx:'BX6', n:'Outlet for counter items, next to the selector (120 V, circuit A)', x:72.9, z:50, note:'user: an outlet for items on the counter, next to the selector switch, in the same two gang box (the selector EP9 at 71 in along, this outlet 1 7/8 in toward the cab; the countertop is 38 up, so it is 12 in above it); circuit A (GFCI), 14 AWG, a standard 15 A receptacle: circuit A\u2019s cable arrives here from the TV outlet box BX8 (WR41) and stops, so this is the last outlet of its branch (user, 2026-11-06: WR41 goes from the TV outlet to the counter outlet). Four cables in one box (the selector\u2019s three on circuit B/D and this one on circuit A) plus the rocker and the receptacle come to about 28 cu in: a deep two gang box (about 37 cu in, 3 3/4 in deep) has room. Keep the neutrals of the two circuits apart (circuit A\u2019s white wires together, circuit B/D\u2019s together; the grounds may be joined). In box BX6: how it is wired is drawing EF22'},
]; };

// plumbing shown for reference, drawn as pipes and fixtures in slate with hexagon PL labels so it cannot be mistaken for the electrics (wires are drawn as coloured lines with round labels)
const PLUMB = pl => {
  const rz = 27.5;                                   // rz: the band between furring rails S3 (21 1/4) and S4 (30 1/4), inside the 2 in zone (23 1/4 to 29 1/2 up) and above the five oval slots at 25 1/3
  const rx = pl.valveX - 1.5, vz = pl.valveZ, sx = pl.pdrX;      // the lines rise at rx, between the blocks of S4 (at 17 3/4 and 31 1/4)
  const out = [
    {k:'phead', n:'Shower head', x:pl.headX, z:pl.headZ, lab:'H', note:fr(pl.headZ) + ' in up on a ' + fr(pl.headOut) + ' in arm pointing into the stall, on the cab side of the nook, around 30 in along the wall as you said (' + fr(pl.headX) + '), over the toilet end; the feed rises straight up from the valve at the head\'s own position'},
    {k:'pvalve', n:'Shower valve (mixer handle)', x:pl.valveX, z:pl.valveZ, lab:'V', note:'on the cab side of the shower nook, the left of it in the passenger-wall view (user: the plumbing is to the left of the nook, and the head and the valve are around 30 in along the wall; the nook is ' + fr(pl.snookEnd - (pl.sn ? pl.sn.x1 - pl.sn.x0 : 12)) + ' to ' + fr(pl.snookEnd) + ' in), under the head, ' + fr(vz) + ' in up, between furring rails S4 and S5, over the toilet end; the hot and cold lines come up beside it at ' + fr(rx) + ' in. The steel angle at the rear end stands 1 1/2 in off the body up to 36 3/4 (sloping down to 31 at 11 in), so about 3 in of room is left behind the covering. The valve is mounted on the small hinged valve door in the paneling (25 to 34 in along, 31 1/2 to 42 1/4 up; the opening is 25 1/2 to 33 1/2 and 32 to 41 3/4, between S4 and S5), so its back and its two elbows are reached by backing out four stainless screws and swinging the door open on its cab-side hinge'},
    {k:'ppump', n:'Water pump, under the sink beside the water heater', x0:104, x1:107, z0:12, z1:20, note:'user: the pump will fit somewhere closer to the water heater (it was at 119 to 122). On the inside of the sink cabinet\u2019s rear end panel (the heater, 87 1/4 to 101 1/4, is just beyond it), above the fresh tank (top at 10 in), about 3 in from the heater\u2019s fittings; reached through the sink cabinet\u2019s doors or hatch (my placement). Its 12 V feed (14 AWG, 10 A, from the fuse block) is the pump circuit on the one-line diagram'},
    {k:'ppath', two:true, n:'Hot and cold supply to the shower valve (two 1/2 in PEX lines)', pts:[[105.5, 20.5], [105.5, rz], [rx, rz], [rx, vz - 1.5]], at:[70, rz], note:'cold leaves the pump (now beside the heater, at 104 to 107) and rises inside the sink cabinet (from 104 on, the wall is the sliding door, so there is no cavity there: clip it inside the cabinet) to ' + fr(rz) + ' in up, then through the cabinet\u2019s rear end panel at 103 into the wall cavity behind the covering at ' + fr(rz) + ' in up: between furring rails S3 and S4 (the free band between the 3 1/2 in furring rails is 23 to 28 1/2 up), in the 2 in zone (23 1/4 to 29 1/2 up) where the steel is only 2 in off the body so there is about 2 1/2 in of room behind the covering, and above the five oval slots at 25 1/3 up. It crosses the pillar at about 98 and runs on behind the covering past the back of the fridge (there is no wall between the fridge and the shower now: its end is a curtain) to the rear end of the stall, then up at ' + fr(rx) + ' in, between the blocks of S4 (at 17 3/4 and 31 1/4), through S4 (drill it, do not notch) to the valve. The hot line branches off the hot water tank (87 1/4 to 101 1/4, fittings at its back) at about 94 and runs beside the cold one, 1 in apart; foam sleeve on the hot one, and insulation between both lines and the steel. At the valve (user: the back of it is 1/2 in-14 NPSM, male, the threads outside): a 90 degree PEX elbow with a female swivel nut and its flat washer on each inlet, right behind the valve, so the lines turn from the wall to the vertical in about 1 1/2 in (user chose two SharkBite UC532LFA: brass, 1/2 in PEX barb by 1/2 in FIP swivel, 90 degrees; the PEX goes on the barb with a stainless cinch clamp, 5/8 in size, one per barb, with a cinch tool); each line is about 7 to 7 3/4 ft, so cut 10 ft of red (hot) and 10 ft of blue (cold), and leave 8 to 12 in of it loose in the gap behind the valve door, so the valve can be pulled forward; put a shutoff on each line in the sink cabinet, and pressure-test the lines with the door open before it is closed up'},
    {k:'ppath', n:'Feed from the valve to the shower head', pts:[[pl.valveX, vz + 1.5], [pl.headX, vz + 1.5], [pl.headX, pl.headZ - 1.2]], at:[pl.headX, 52], note:'from the top of the valve straight up (the head is at the valve\'s own place), past S5, S6 and S7 (drill each, do not notch) in the gap between their blocks at 17 3/4 and 31 1/4, to the head; one mixed-water line'},
    {k:'pdrain', n:'Shower drain, through the floor to the grey water tank under the van', x:sx, z:.8, note:'a 1 1/2 in drain at the rear-door end of the pan (' + fr(sx) + ' in along, about ' + fr(pl.pdrY) + ' in out from the wall), the pan floor sloping to it; straight down through the floor, a shallow trap under it, then to the grey tank (the WT-5544, 24 x 15 x 9 in, 12 gal, behind the spare tire, position not placed) with its vent. The tank has to be lower than the pan; its inlet has to take the 1 1/2 in drain'},
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
      win: L.win, batt: L.batt, bA: L.bA, bB: L.bB, headX: P.headX, headZ: P.headZ, headOut: P.headOut, valveX: P.valveX, valveZ: P.valveZ, cab: P.cab, ceilF: L.ceilF, panW: P.panW, panD: P.panD, gear: L.gear, toilet: L.toilet, sn: L.sn, wallsOn: P.wallsOn, fwT: P.fwT, hotX: L.hotX, snookEnd: L.snx[1], pdrX: P.pdrX, pdrY: P.pdrY, slatY: L.slatY, slatW: P.slatW, tbl: L.tbl, bedLen: P.bedLen, bedX0: P.bedX0, bedX1: P.bedX1, tableH: P.tableH, cabBot: P.cabBot,
    };
  });
}
async function grabItems(page) {            // the furniture outlines (same positions as wall-map)
  return page.evaluate(() => {
    const P = L.P, ch = P.counterH, f = v => Math.round(v * 100) / 100, a = (x0, x1, z0, z1) => ({ x0: f(x0), x1: f(x1), z0: f(z0), z1: f(z1) });
    const D = [a(P.bedX0, P.bedX1, 0, P.platform + P.mattress + P.bedBack), a(42, 76, 0, 7.5), a(L.c0, L.c1, 0, L.ceilF), a(L.bA[0], L.bA[1], 0, P.seatH), a(L.bB[0], L.bB[1], 0, P.seatH)];
    if (L.tableLen > 0) D.push(a(L.tbl[0], L.tbl[1], P.tableH - 1.5, P.tableH));
    L.cabs.forEach(c => D.push(a(c[0], c[1], P.cabBot, L.ceilF)));
    if (L.win) D.push(Object.assign(a(L.win.cx0, L.win.cx1, L.win.cz0, L.win.cz1), { win: true }));
    const nk0 = L.snx[0], nkx = L.snx[1];
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
const CPL = '#475569', CPLF = '#D9E2EC', INK = '#1b1a17', C120 = '#B3261E', C12 = '#185FA5', CAC = '#B45309', CLT = '#B8860B';
function symbol(e, X, Y) {
  const o = [], r = 7;
  if (e.k === 'out120') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${C120}" stroke-width="1.8"/><line x1="${x-3}" y1="${y-3}" x2="${x-3}" y2="${y+1}" stroke="${C120}" stroke-width="1.6"/><line x1="${x+3}" y1="${y-3}" x2="${x+3}" y2="${y+1}" stroke="${C120}" stroke-width="1.6"/>`); return [o.join(''), x, y]; }
  if (e.k === 'usb') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#fff" stroke="${C12}" stroke-width="1.8"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">12</text>`); return [o.join(''), x, y]; }
  if (e.k === 'sw') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-6.5}" y="${y-6.5}" width="13" height="13" rx="2" fill="#fff" stroke="${INK}" stroke-width="1.8"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${INK}">S</text>`); return [o.join(''), x, y]; }
  if (e.k === 'lt') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="${r}" fill="#FFD84A" stroke="${CLT}" stroke-width="1.8"/>`); return [o.join(''), x, y]; }
  if (e.k === 'plate') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-17}" y="${y-9}" width="34" height="18" rx="3" fill="#fff" stroke="${INK}" stroke-width="1.8"/><rect x="${x-14}" y="${y-5.5}" width="11" height="11" rx="1.5" fill="#fff" stroke="${INK}" stroke-width="1.5"/><text x="${x-8.5}" y="${y+3}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:${INK}">S</text><circle cx="${x+9}" cy="${y}" r="6" fill="#fff" stroke="${C120}" stroke-width="1.6"/><line x1="${x+6.6}" y1="${y-2.6}" x2="${x+6.6}" y2="${y+.8}" stroke="${C120}" stroke-width="1.4"/><line x1="${x+11.4}" y1="${y-2.6}" x2="${x+11.4}" y2="${y+.8}" stroke="${C120}" stroke-width="1.4"/>`); return [o.join(''), x, y]; }
  if (e.k === 'phead') { const x = X(e.x), y = Y(e.z); o.push(`<line x1="${x}" y1="${y-12}" x2="${x}" y2="${y-3}" stroke="${CPL}" stroke-width="3.4" stroke-linecap="round"/><path d="M${x-11} ${y+3} Q${x} ${y-12} ${x+11} ${y+3} Z" fill="${CPLF}" stroke="${CPL}" stroke-width="2.2" stroke-linejoin="round"/><g stroke="${CPL}" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="1 3.2"><line x1="${x-7}" y1="${y+7}" x2="${x-9}" y2="${y+17}"/><line x1="${x}" y1="${y+7}" x2="${x}" y2="${y+18}"/><line x1="${x+7}" y1="${y+7}" x2="${x+9}" y2="${y+17}"/></g>`); return [o.join(''), x, y]; }
  if (e.k === 'pvalve') { const x = X(e.x), y = Y(e.z); o.push(`<line x1="${x-11}" y1="${y}" x2="${x+11}" y2="${y}" stroke="${CPL}" stroke-width="3.6" stroke-linecap="round"/><circle cx="${x}" cy="${y}" r="7" fill="#fff" stroke="${CPL}" stroke-width="2.4"/><line x1="${x}" y1="${y}" x2="${x+5}" y2="${y-9}" stroke="${CPL}" stroke-width="3" stroke-linecap="round"/>`); return [o.join(''), x, y]; }
  if (e.k === 'ppump') { const xa = X(e.x0), xb = X(e.x1), x = Math.min(xa, xb), w = Math.max(14, Math.abs(xb - xa)), y0 = Y(e.z1), h = 6 * (e.z1 - e.z0), cx = x + w / 2, cy = y0 + h / 2; o.push(`<rect x="${x}" y="${y0}" width="${w}" height="${h}" rx="7" fill="${CPLF}" fill-opacity=".9" stroke="${CPL}" stroke-width="2.4"/><circle cx="${cx}" cy="${cy - 6}" r="9" fill="#fff" stroke="${CPL}" stroke-width="2"/><path d="M${cx} ${cy-6} m-5 0 a5 5 0 0 1 5 -5 M${cx} ${cy-6} m5 0 a5 5 0 0 1 -5 5" fill="none" stroke="${CPL}" stroke-width="2" stroke-linecap="round"/><text x="${cx}" y="${y0 + h - 7}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${CPL}">pump</text>`); return [o.join(''), cx, cy]; }
  if (e.k === 'ppath') { const tube = (pts, inner) => { const q = pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' '); return `<polyline points="${q}" fill="none" stroke="${CPL}" stroke-width="9" stroke-linejoin="round" stroke-linecap="round"/><polyline points="${q}" fill="none" stroke="${inner}" stroke-width="5" stroke-linejoin="round" stroke-linecap="round"/>`; };
    const fit = (pts, dx, dy) => pts.map(p => `<circle cx="${X(p[0]) + dx}" cy="${Y(p[1]) + dy}" r="5.6" fill="#fff" stroke="${CPL}" stroke-width="2"/>`).join('');
    if (e.two) { const sh = pts => pts.map(p => [p[0] + 8 / 6 * (X(1) < X(0) ? -1 : 1), p[1] - 8 / 6]); o.push(tube(e.pts, '#CFE6FA')); o.push(tube(sh(e.pts), '#FAD7CC')); o.push(fit(e.pts.slice(1, -1), 0, 0), fit(sh(e.pts).slice(1, -1), 0, 0)); }
    else { o.push(tube(e.pts, '#EEF1F5')); o.push(fit(e.pts.slice(1, -1), 0, 0)); }
    return [o.join(''), X(e.at[0]), Y(e.at[1])]; }
  if (e.k === 'pdrain') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-4.5}" y="${y}" width="9" height="22" fill="#fff" stroke="${CPL}" stroke-width="2"/><ellipse cx="${x}" cy="${y}" rx="11" ry="5" fill="${CPLF}" stroke="${CPL}" stroke-width="2.2"/><g stroke="${CPL}" stroke-width="1.6" stroke-linecap="round"><line x1="${x-5}" y1="${y}" x2="${x+5}" y2="${y}"/></g><path d="M${x-6} ${y+27} L${x} ${y+34} L${x+6} ${y+27}" fill="none" stroke="${CPL}" stroke-width="2.4" stroke-linejoin="round"/>`); return [o.join(''), x, y]; }
  if (e.k === 'pvent') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-8}" y="${y-8}" width="16" height="16" rx="8" fill="${CPLF}" stroke="${CPL}" stroke-width="2.2"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:${CPL}">VT</text>`); return [o.join(''), x, y]; }
  if (e.k === 'wet') { const x = X(e.x), y = Y(e.z); o.push(`<circle cx="${x}" cy="${y}" r="7" fill="#DCEAF6" stroke="${C12}" stroke-width="1.8" stroke-dasharray="3 2"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">${e.lab}</text>`); return [o.join(''), x, y]; }
  if (e.k === 'sel') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-10}" y="${y-8}" width="20" height="16" rx="3" fill="#fff" stroke="${C120}" stroke-width="2"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:8.5px;font-weight:700;fill:${C120}">M/H</text>`); return [o.join(''), x, y]; }
  if (e.k === 'inlet') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-8}" y="${y-8}" width="16" height="16" rx="3" fill="#FFF1D6" stroke="${CAC}" stroke-width="2"/><text x="${x}" y="${y+3.6}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${CAC}">IN</text>`); return [o.join(''), x, y]; }
  if (e.k === 'remote') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-14}" y="${y-9}" width="28" height="18" rx="3" fill="#fff" stroke="${C12}" stroke-width="1.8"/><rect x="${x-10}" y="${y-5.5}" width="14" height="8" rx="1" fill="#CFE6FA" stroke="${C12}" stroke-width="1"/><circle cx="${x+8}" cy="${y-1}" r="2.6" fill="${C12}"/><text x="${x}" y="${y+7.6}" text-anchor="middle" style="font-size:6.5px;font-weight:700;fill:${C12}">REMOTE</text>`); return [o.join(''), x, y]; }
  if (e.k === 'panel') { const x = X(e.x), y = Y(e.z); o.push(`<rect x="${x-9}" y="${y-7}" width="18" height="14" rx="2" fill="#fff" stroke="${C12}" stroke-width="1.8"/><text x="${x}" y="${y+3.4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:${C12}">M</text>`); return [o.join(''), x, y]; }
  if (e.k === 'strip') { const xa = X(e.x0), xb = X(e.x1), y = Y(e.z), x = Math.min(xa, xb), w = Math.abs(xb - xa); o.push(`<rect x="${x}" y="${y-2.5}" width="${w}" height="5" rx="2.5" fill="#FFD84A" stroke="${CLT}" stroke-width="1.2"/>`); return [o.join(''), x + w / 2, y]; }
  if (e.k === 'box') { const xa = X(e.x0), xb = X(e.x1), x = Math.min(xa, xb), w = Math.max(10, Math.abs(xb - xa)), y0 = Y(e.z1), h = 6 * (e.z1 - e.z0); o.push(`<rect x="${x}" y="${y0}" width="${w}" height="${h}" rx="2" fill="#FFF1D6" fill-opacity=".75" stroke="${CAC}" stroke-width="2"/>`); return [o.join(''), x + w / 2, y0 + h / 2]; }
  if (e.k === 'run') { const x = X(e.x); o.push(`<line x1="${x}" y1="${Y(e.z0)}" x2="${x}" y2="${Y(e.z1)}" stroke="${C12}" stroke-width="3" stroke-dasharray="7 4" opacity=".85"/><line x1="${x+4}" y1="${Y(e.z0)}" x2="${x+4}" y2="${Y(e.z1)}" stroke="${C120}" stroke-width="3" stroke-dasharray="7 4" opacity=".85"/>`); return [o.join(''), x + 2, Y((e.z0 + e.z1) / 2)]; }
  return ['', 0, 0];
}
function wallSVG(list, side, base, furn, plumb) {
  const flip = side === 'P', X = x => +(flip ? 1020 - 6 * x : 50 + 6 * x).toFixed(1), Y = z => +(544 - 6 * z).toFixed(1);
  const o = [], bo = [], placed = [];
  furn.forEach(it => { const xa = X(it.x0), xb = X(it.x1); o.push(it.win
    ? `<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="#B5D4F4" fill-opacity=".3" stroke="#185FA5" stroke-width="1.6"/><text x="${(xa + xb) / 2}" y="${Y(it.z0) - 6}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#0C447C;paint-order:stroke;stroke:#fff;stroke-width:3px">side window</text>`
    : `<rect x="${Math.min(xa, xb)}" y="${Y(it.z1)}" width="${Math.abs(xb - xa)}" height="${6 * (it.z1 - it.z0)}" rx="2" fill="none" stroke="${INK}" stroke-opacity=".28" stroke-width="1.2" stroke-dasharray="4 3"/>`); });
  const rows = list.map((e, i) => {
    e.id = e.name || ('E' + side + (i + 1));
    if (e.k === 'retired') return `<tr id="item-${e.id}"><td><b class="id">${e.id}</b></td><td>${esc(e.n)}</td><td>retired</td><td class="kd">${esc(e.note)}</td></tr>`;
    const [g, cx, cy] = symbol(e, X, Y); o.push(`<g class="itm" data-item="${e.id}"><title>${e.id}: ${esc(e.n)}</title>${g}</g>`);
    let bx = cx + (e.k === 'strip' || e.k === 'box' || e.k === 'run' ? 0 : 13), by = cy - (e.k === 'strip' ? 13 : e.k === 'run' ? 0 : 13);
    if (e.k === 'strip') { bx = cx; }
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0] - bx, q[1] - by) < 24); t++) by -= 14;
    placed.push([bx, by]);
    o.push(`<g class="itm" data-item="${e.id}"><rect x="${bx-14}" y="${by-8}" width="28" height="16" rx="8" fill="#fff" fill-opacity=".95" stroke="${C120}" stroke-width="1.3"/><text x="${bx}" y="${by+3.8}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${C120}">${e.id}</text></g>`);
    const where = e.k === 'strip' ? `${fr(e.x0)} to ${fr(e.x1)}, at ${fr(e.z)} up` : e.k === 'box' ? `${fr(e.x0)} to ${fr(e.x1)}, ${fr(e.z0)} to ${fr(e.z1)} up` : e.k === 'run' ? `at ${fr(e.x)}, ${fr(e.z0)} to ${fr(e.z1)} up` : `${fr(e.x)} in, ${fr(e.z)} up`;
    ITEM_INFO[e.id] = { n: e.n + (e.bx ? ' (in box ' + e.bx + ')' : ''), where, note: e.note };
    return `<tr id="item-${e.id}"><td><b class="id" data-go="${e.id}" role="button" tabindex="0" title="Show ${e.id} on the diagram">${e.id}</b></td><td>${esc(e.n)}${e.bx ? ` <span class="bxt">[box ${e.bx}]</span>` : ''}</td><td>${where}</td><td class="kd">${esc(e.note)}</td></tr>`;
  });
  { const grp = {}; list.forEach(e => { if (e.bx && e.k !== 'retired') (grp[e.bx] = grp[e.bx] || []).push(e); });
    Object.keys(grp).forEach(id => { const m = grp[id], bi = BOXES[id], xs = m.map(e => e.x), zs = m.map(e => e.z), xa = X(Math.min(...xs) - 2.4), xb = X(Math.max(...xs) + 2.4), ya = Y(Math.min(...zs) - 2.9), yb = Y(Math.max(...zs) + 2.9), l = Math.min(xa, xb), w = Math.abs(xb - xa), t = Math.min(ya, yb), h = Math.abs(yb - ya);
      bo.push(`<g class="itm" data-item="${id}"><title>${id}: ${esc(bi.n)}</title><rect x="${l}" y="${t}" width="${w}" height="${h}" rx="5" fill="#7A4B12" fill-opacity=".07" stroke="#7A4B12" stroke-width="1.8" stroke-dasharray="5 3"/><rect x="${l - 2}" y="${t + h + 1}" width="32" height="16" rx="8" fill="#7A4B12" stroke="#fff" stroke-width="1.2"/><text x="${l + 14}" y="${t + h + 12.6}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#fff">${id}</text></g>`);
      ITEM_INFO[id] = { n: 'Box ' + id + ': ' + bi.n, where: bi.where, note: 'In it: ' + bi.what + '. Wires: ' + bi.wires + '. Drawing: ' + bi.fig + '.' }; }); }
  const pg = [];
  const prow = (plumb || []).map((e, i) => {
    e.id = 'PL' + (i + 1);
    const [g, cx, cy] = symbol(e, X, Y); pg.push(g);
    let bx = cx + 14, by = cy + 16;
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0] - bx, q[1] - by) < 26); t++) by += 14;
    placed.push([bx, by]);
    pg.push(`<polygon points="${bx-18},${by} ${bx-12},${by-9} ${bx+12},${by-9} ${bx+18},${by} ${bx+12},${by+9} ${bx-12},${by+9}" fill="${CPLF}" stroke="${CPL}" stroke-width="1.6"/><text x="${bx}" y="${by+3.8}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${CPL}">${e.id}</text>`);
    const where = e.pts ? `from ${fr(e.pts[0][0])} in, ${fr(e.pts[0][1])} up, to ${fr(e.pts[e.pts.length - 1][0])} in, ${fr(e.pts[e.pts.length - 1][1])} up` : e.x0 != null ? `${fr(e.x0)} to ${fr(e.x1)}, ${fr(e.z0)} to ${fr(e.z1)} up` : `${fr(e.x)} in, ${fr(e.z)} up`;
    return `<tr><td><b class="pid">${e.id}</b></td><td>${esc(e.n)}</td><td>${where}</td><td class="kd">${esc(e.note)}</td></tr>`;
  });
  const svg = `<svg viewBox="0 0 1070 636" role="img" aria-label="${flip ? 'Passenger' : 'Driver'} wall: steel, furring rails, furniture outlines, the electrical items${plumb && plumb.length ? ' and the plumbing as pipes' : ''}">${base.inner}<g id="elec${side}">${bo.join('')}${o.join('')}</g>${pg.length ? `<g id="plumb${side}">${pg.join('')}</g>` : ''}</svg>`;
  const ptable = prow.length ? `<div id="plumbTable${side}"><h3 style="color:${CPL}">Plumbing on this wall (pipes with hexagon labels, for reference: not electrical)</h3><div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${prow.join('')}</tbody></table></div></div>` : '';
  return { svg, table: `<div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>`, ptable, legend: base.legend };
}

const fig = (id, text) => `<div class="figtag"><span class="fid">${id}</span>${text}</div>`;
function ceilingSVG(d, WR, baseOnly) {
  const G = !!WR && !baseOnly;                                   // gauge mode: the wires are drawn from the wire list, coloured by gauge
  const S = 6, X = x => 50 + S * x, Y = y => 56 + S * y, W = 1070, H = 56 + S * 68 + 140 + (G ? 60 : 0);
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
  const RX = 79;                                   // the ceiling cables are drawn at 73 on the wall maps = 79 from the rear-door edge, in the bay between the ribs at 61 and 97; passenger wall run climbs the passenger wall there, driver wall run the driver wall at 76 1/2 (82 1/2 from the rear-door edge, past the nook's front frame) and jogs 3 1/2 in at the ceiling
  const line = (pts, col, w, dash) => `<polyline points="${pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' ')}" fill="none" stroke="${col}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} stroke-linejoin="round"/>`;
  const acY = ac.y - ac.w / 2, fanY = fan.y - fan.w / 2;
  if (!G && !baseOnly) {
  o.push(line([[RX - 1.2, 0], [RX - 1.2, 68]], C12, 3));                              // the pump and control panel wires across (each its own wire from the fuse block)
  o.push(line([[RX + 1.2, 0], [RX + 1.2, 68]], C120, 3, '8 4'));                       // 120 V across
  o.push(line([[RX, 0], [RX, acY], [ac.x, acY]], CAC, 4.5));                           // A/C feed to the notch in the frame's driver-side wall
  o.push(line([[83.6, 0], [83.6, 20.5], [fan.x, 20.5], [fan.x, fanY]], C12, 2.4));    // fan feed, up the driver wall run
  { const ys = [...new Set(d.lights.map(l => l.y))], aR = ac.x + ac.w / 2 + 1.5, aT = ac.y - ac.w / 2 - 1.5;
    ys.forEach(y => { const xs = d.lights.filter(l => l.y === y).map(l => l.x), x0 = Math.min(...xs), x1 = Math.max(...xs); if (xs.length < 2) return;
      // each row of ceiling lights runs along one slat; a row that crosses the A/C opening (it cuts that slat) goes round the opening, above it, in the gap between slats
      const cross = y > ac.y - ac.w / 2 && y < ac.y + ac.w / 2 && x0 < ac.x - ac.w / 2 && x1 > ac.x + ac.w / 2;
      o.push(line(cross ? [[x0, y], [x0, aT], [aR, aT], [aR, y], [x1, y]] : [[x0, y], [x1, y]], CLT, 2.2, '2 3')); }); }
  }
  // the wet bath stall (36 along the wall, 24 out from the passenger wall; wall numbers + 6 from the rear-door edge)
  o.push(`<rect x="${X(6)}" y="${Y(44)}" width="${S * 36}" height="${S * 24}" fill="${G ? '#5F5E5A' : C12}" fill-opacity=".07" stroke="${G ? '#5F5E5A' : C12}" stroke-width="1.4" stroke-dasharray="5 3"/><text x="${X(6) + 6}" y="${Y(44) + 14}" style="font-size:11px;font-weight:700;fill:${G ? '#5F5E5A' : C12}">wet bath stall</text>`);
  // the soft LED strip around the ceiling edge: driver side, across the back, passenger side (about 31 ft in all, fed in three sections)
  { const e = 1.5, cabX = d.P.cab + 6;
    o.push(`<polyline points="${X(cabX)},${Y(e)} ${X(e)},${Y(e)} ${X(e)},${Y(68 - e)} ${X(cabX)},${Y(68 - e)}" fill="none" stroke="#F4C95D" stroke-width="9" stroke-opacity=".55" stroke-linejoin="round"/><polyline points="${X(cabX)},${Y(e)} ${X(e)},${Y(e)} ${X(e)},${Y(68 - e)} ${X(cabX)},${Y(68 - e)}" fill="none" stroke="#B8860B" stroke-width="1.6" stroke-linejoin="round"/>`);
    o.push(`<text x="${G ? X(16) : X(e) + 8}" y="${Y(e) + (G ? 38 : 32)}" style="font-size:10.5px;font-weight:700;fill:#8a6a00">soft LED strip around the edge</text>`)
    o.push(`<text x="${X(cabX) - 4}" y="${Y(e) + 22}" text-anchor="end" style="font-size:10.5px;font-weight:700;fill:#8a6a00">strip starts here (cab end, driver side)</text><text x="${X(cabX) - 4}" y="${Y(68 - e) - 12}" text-anchor="end" style="font-size:10.5px;font-weight:700;fill:#8a6a00">strip ends here (cab end, passenger side)</text>`); }
  // lights
  d.lights.forEach((l, i) => { const wet = l.y > d.P.vanW - d.panD && l.x < 6 + d.panW && l.x > 6; o.push(`<circle cx="${X(l.x)}" cy="${Y(l.y)}" r="${Math.max(6, S * d.P.lightD / 2)}" fill="#FFD84A" stroke="${wet && !G ? C12 : CLT}" stroke-width="${wet ? 3 : 1.8}"/>`); if (wet) o.push(`<text x="${X(l.x) + 12}" y="${Y(l.y) + 16}" style="font-size:10.5px;font-weight:700;fill:${G ? '#5F5E5A' : C12}">wet-rated (IP65)</text>`); });
  if (G) { const placed = [], wg = WR.filter(w => w.C).map(w => EW.wireGroup(w, 'C', X, Y, placed)); wg.forEach(g => o.push(g.l));
    wg.forEach(g => o.push(g.p)); WR.forEach(w => o.push(EW.traceLayer(w, 'C', X, Y))); }
  // where the wall runs meet the walls
  o.push(`<text x="${X(RX + 3.5) + 14}" y="${Y(0) + 14}" style="font-size:11px;font-weight:700;fill:${INK}">driver wall run (A/C, 12 V) at ${RX + 3.5}</text><text x="${X(RX + 3.5) + 14}" y="${Y(68) - 8}" style="font-size:11px;font-weight:700;fill:${INK}">passenger wall run (120 V, branches) at ${RX}</text>`);
  // legend
  if (baseOnly) return o.join('');
  const ly = Y(68) + 66;
  if (G) {
    EW.AWG.forEach((a, i) => { const x = X(0) + Math.floor(i / 4) * 520, y = ly + (i % 4) * 18; o.push(`<line x1="${x}" y1="${y}" x2="${x + 36}" y2="${y}" stroke="${a.c}" stroke-width="${a.w}" stroke-linecap="round"/><text x="${x + 44}" y="${y + 4}" style="font-size:12px;fill:${INK}"><tspan style="font-weight:700">${a.name} AWG</tspan>, ${a.use}</text>`); });
    ['solid = 12 V; dashed = 120 V. The WR labels are the wires\u2019 numbers (the table below). The junction box is JB, in the couch cabinet (EF10).', 'Grey bands = ribs; dashed squares = the roof units; yellow circles = the four ceiling', 'lights; the pale band = the soft LED strip. Driver wall run comes up at the top (driver wall), passenger wall run at the bottom (passenger wall).'].forEach((t, i) => o.push(`<text x="${X(0)}" y="${ly + 88 + i * 16}" style="font-size:12px;fill:${INK}">${t}</text>`));
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ceiling seen from above: every wire coloured by gauge"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
  }
  const leg = [[C12, 'solid blue: 12 V wires (fan 14 AWG; pump and control panel)', null, 3], [C120, 'dashed red: 120 V circuits in flexible conduit (14 AWG, 15 A breakers)', '8 4', 3], [CAC, 'solid orange: A/C feed, 6 AWG, 100 A fuse at the battery', null, 4.5], [CLT, 'dotted yellow: the ceiling lights, one slat per row (14 AWG)', '2 3', 2.2], ['#F4C95D', 'pale yellow band: soft LED strip around the edge (14 AWG, its own 10 A circuit)', null, 7]];
  leg.forEach((l, i) => o.push(`<line x1="${X(0)}" y1="${ly + i * 16}" x2="${X(0) + 34}" y2="${ly + i * 16}" stroke="${l[0]}" stroke-width="${l[3]}"${l[2] ? ` stroke-dasharray="${l[2]}"` : ''}/><text x="${X(0) + 42}" y="${ly + i * 16 + 4}" style="font-size:12px;fill:${INK}">${l[1]}</text>`));
  o.push(`<text x="${X(86)}" y="${ly + 4}" style="font-size:12px;fill:${INK}">the junction box (JB) is in the couch cabinet, not on the ceiling</text><text x="${X(86)}" y="${ly + 20}" style="font-size:12px;fill:${INK}">grey bands = ribs; dashed squares = the unit footprints on the roof</text><text x="${X(86)}" y="${ly + 36}" style="font-size:12px;fill:${INK}">yellow circles = the four ceiling lights (shower; countertop and sink;</text><text x="${X(86)}" y="${ly + 52}" style="font-size:12px;fill:${INK}">two in the center row; positions from the plan)</text><text x="${X(86)}" y="${ly + 68}" style="font-size:12px;fill:${INK}">the center row goes round the A/C opening, above it, in the gap between slats</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ceiling seen from above: lights, fan, A/C and wire runs"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

// the high-current cables and fuses to buy: gauges from the plan's own currents and lengths; the drop is computed here (copper, 20 C) so the numbers cannot drift from the table
const AWGR = {'10': .9989, '6': .3951, '4': .2485, '2': .1563, '1/0': .0983, '2/0': .0780, '4/0': .0490};   // ohms per 1000 ft
const AWGA = {'10': 40, '6': 75, '4': 95, '2': 130, '1/0': 170, '2/0': 195, '4/0': 260};                    // A, 90 C chassis wiring; 105 C marine cable carries more
function cableTable() {
  const rows = [
    ['Battery + to the Class T fuse and the bus +', '2/0', 168, 1.5, 12.8, 'Class T 250 A, within 7 in of the battery post', 'red 2 ft', 'the whole inverter load goes through it'],
    ['Battery − to the shunt and the bus −', '2/0', 168, 1.5, 12.8, 'none (the shunt, 500 A)', 'black 2 ft', 'the shunt sits on the negative, before the bus'],
    ['Bus to the inverter, + and −', '2/0', 168, 4, 12.8, '250 A on the + (the Class T can serve it if they are within 7 in)', 'red 4.5 ft, black 4.5 ft', '2 ft plus a 2 ft loop so the gear shelf can slide out (use extra-flexible welding cable, which bends tighter); the BELTTT 2000 W draws about 170 A at full load and about 340 A for its 4000 W surge; do not use the 3 ft cables it ships with'],
    ['Alternator side: starter battery to the DC-DC charger, + and −', '2', 65, 17, 13.5, '80 A at the starter battery, within 7 in of its post', 'red 19 ft, black 19 ft', 'about 15 ft in the van plus a 2 ft loop so the gear shelf can slide out; the plan said 4 AWG: that loses 4% over 17 ft, 2 AWG 2.5%; the chassis can be the − only if the LiTime manual says so'],
    ['DC-DC charger to the bus, + and −', '2', 60, 6, 14.0, '80 A at the bus', 'red 7 ft, black 7 ft', '4 ft plus a 2 ft loop for the shelf; the plan said 4 AWG; 2 AWG keeps one size for all the charger runs'],
    ['Shore charger (VEVOR 80 A) to the bus, + and −', '2', 80, 6, 14.6, '100 A at the bus', 'red 7 ft, black 7 ft', '4 AWG carries only about 95 A, which is under the 100 A fuse, so the plan’s 4 AWG is changed to 2 AWG'],
    ['A/C feed, + and −', '6', 58, 12, 12.8, '100 A at the battery', 'red 14 ft, black 14 ft', '6 AWG is what the A/C maker lists for 12 ft; my arithmetic says it loses 4.3%, 4 AWG would lose 2.7%: follow the A/C manual, or use 4 AWG'],
    ['12 V fuse block feed (bus to the fuse block), + and −', '10', 30, 3, 12.8, '30 A at the bus', 'red 4 ft, black 4 ft', 'my size: the 12 V circuits can draw about 20 A all at once (strip 6.4, pump 7, fan 2.7, lights 2.7, panel 1), so 12 AWG on a 20 A fuse would have no margin; every circuit below it has its own fuse and its own wire to its load (WR14 to WR17, WR31, WR32)'],
    ['Chassis ground for the bus bars and the inverter', '4', 20, 3, 12.8, 'none', 'black 4 ft', 'one short strap from the − bus to the van body']];
  const tr = rows.map(r => { const drop = r[2] * AWGR[r[1]] / 1000 * 2 * r[3], pc = drop / r[4] * 100, over = r[6] && AWGA[r[1]] < r[2];
    return `<tr><td>${esc(r[0])}</td><td class="num"><b>${r[1]}</b></td><td class="num">${r[2]} A</td><td class="num">${r[3]} ft</td><td class="num">${drop.toFixed(2)} V (${pc.toFixed(1)}%)</td><td>${esc(r[5])}</td><td>${esc(r[6])}</td><td class="kd">${esc(r[7])}</td></tr>`; }).join('');
  return `<div class="tw"><table><thead><tr><th>Run</th><th>AWG</th><th>Current</th><th>One way</th><th>Drop</th><th>Fuse</th><th>Buy</th><th>Notes</th></tr></thead><tbody>${tr}</tbody></table></div>
  <p class="lead"><b>Buy in total:</b> about 10 ft red and 10 ft black of 2/0, about 32 ft red and 32 ft black of 2 AWG, about 15 ft red and 15 ft black of 6 AWG (or 4), about 4 ft red and 4 ft black of 10 AWG for the fuse block feed, and 4 ft of 4 AWG black. The drop is the voltage lost in the copper at the full current, one way out and back, from 20 C copper resistance; keep it near 3% for the charger runs and well under that for the short ones.</p>
  <ul><li><b>Cable:</b> tinned copper, fine strand (class K or better, UL 1426 or marine battery cable, 105 C insulation), true AWG with no copper-clad aluminium; red and black. Welding cable is fine if it is tinned or the ends are sealed.</li>
  <li><b>Lugs:</b> tinned copper ring lugs, one per cable end (about 10 in 2/0, 16 in 2 AWG, 6 in 6 AWG, 2 in 4 AWG, 2 in 10 AWG), each with the hole size of the stud it goes on (the inverter’s, the battery post, the fuse block and the bus bar: check each before buying), crimped with a hydraulic or hammer crimper, then adhesive-lined heat shrink. Do not solder high-current lugs.</li>
  <li><b>Fuses and gear:</b> a Class T holder and 250 A fuse, a 500 A shunt, two bus bars rated 250 A or more, an 80 A fuse and holder at the starter battery, an 80 A and a 100 A for the chargers at the bus, a 30 A for the 12 V fuse block feed, and a 100 A for the A/C at the battery; a cable cutter and a hydraulic crimper (or have a shop crimp the lugs).</li></ul>`;
}
// the selector wiring: the user's single pole, center off rocker (one common, two throws) on one shared breaker
function selectorSVG() {
  const o = [], W = 800, H = 330, tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const box = (x, y, w, h, a, b, col) => { o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff" stroke="${col}" stroke-width="1.8"/>`); tx(x + 10, y + 21, a, 'font-weight:700'); if (b) tx(x + 10, y + 39, b, 'fill:#5F5E5A;font-size:11px'); };
  const ln = (x1, y1, x2, y2, col, w = 2.4, d = '') => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"${d ? ` stroke-dasharray="${d}"` : ''}/>`);
  const pin = (x, y) => o.push(`<rect x="${x}" y="${y - 5}" width="22" height="10" rx="2" fill="#B9BCC2" stroke="${INK}" stroke-width="1"/>`);
  tx(20, 24, 'Rocker up: only the microwave is live. Middle: neither. Rocker down: only the heater.', 'font-size:12px;fill:#5F5E5A');
  tx(20, 42, 'Drawn as a diagram: on the real switch the three pins are in a row, and the middle one is the common.', 'font-size:12px;fill:#5F5E5A');
  box(20, 120, 170, 58, 'Breaker B/D, 15 A GFCI', 'AC panel, 14 AWG hot', C120);
  o.push(`<rect x="300" y="70" width="200" height="160" rx="8" fill="#FFF1D6" stroke="${C120}" stroke-width="1.8"/>`);
  tx(312, 92, '30 A SPDT rocker (KCD3)', 'font-weight:700'); tx(312, 109, 'ON - OFF - ON, 3 pins', 'font-size:11px;fill:#5F5E5A');
  tx(312, 153, 'common', 'font-weight:700'); tx(312, 169, '(middle pin)', 'font-size:11px;fill:#5F5E5A');
  tx(402, 98 + 33, 'pin 1', 'font-size:11px'); tx(402, 192 + 3, 'pin 3', 'font-size:11px');
  pin(278, 149); pin(478, 128); pin(478, 192);
  ln(190, 149, 280, 149, C120); tx(196, 140, 'hot', 'font-size:11px;fill:' + C120);
  box(600, 90, 180, 58, 'Microwave outlet', '15 A receptacle, 14 AWG hot', C120);
  box(600, 172, 180, 58, 'Heater outlet', 'beside the tank, 14 AWG hot', C120);
  ln(500, 128, 600, 118, C120); ln(500, 192, 600, 200, C120);
  tx(520, 112, 'up', 'font-size:11px;fill:#5F5E5A'); tx(520, 222, 'down', 'font-size:11px;fill:#5F5E5A');
  ln(20, 268, 780, 268, '#5F5E5A', 2, '7 4'); tx(20, 260, 'neutral and ground: straight from the bus to both loads, not through the switch', 'font-size:11px;fill:#5F5E5A');
  tx(20, 292, 'Check the pins with a continuity tester first. Use fully insulated 12 to 10 AWG 1/4 in spade terminals', 'font-size:11px;fill:#5F5E5A');
  tx(20, 308, 'with heat shrink boots, or put the switch in a plastic box. Turn the microwave off before moving the switch.', 'font-size:11px;fill:#5F5E5A');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Wiring of the heater or microwave selector: the breaker feeds the common pin, the two other pins go to the microwave outlet and the heater"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function ledSVG() {
  const o = [], W = 800, H = 430, RED = '#D32F2F', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.4) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const box = (x, y, w, h, a, b, col, fill = '#fff') => { o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="${fill}" stroke="${col}" stroke-width="1.8"/>`); tx(x + 10, y + 19, a, 'font-weight:700'); if (b) tx(x + 10, y + 35, b, 'fill:#5F5E5A;font-size:11px'); };
  const gray = 'font-size:11px;fill:#5F5E5A';
  tx(20, 22, 'One slide dimmer on the dinette wall switches and dims all three strips. There is no controller box.', 'fill:#5F5E5A');
  box(20, 70, 170, 58, '12 V fuse block, way 2', '10 A fuse', C12);
  o.push(`<rect x="300" y="50" width="200" height="190" rx="8" fill="#E8F1FB" stroke="${C12}" stroke-width="1.8"/>`);
  tx(312, 72, 'JB2 (couch cabinet)', 'font-weight:700'); tx(312, 88, 'strip splices only, no controller', gray);
  ln(190, 92, 300, 92, RED); ln(190, 106, 300, 106, INK); tx(196, 84, '+', `font-weight:700;fill:${RED}`); tx(196, 122, '−', 'font-weight:700'); tx(20, 148, 'WR14: 14 AWG pair, about 9 ft drawn', gray); tx(20, 164, '(cut about 11 ft, for slack)', gray);
  box(640, 70, 150, 120, 'Slide dimmer ED22', 'dinette wall W2', C12, '#FFF1D6'); tx(650, 126, '12 V, 10 A or more', gray); tx(650, 142, 'switches and dims', gray); tx(650, 158, 'all three strips', gray);
  ln(500, 92, 640, 92, RED); ln(500, 106, 640, 106, INK); tx(506, 82, 'WR38 supply pair', gray); tx(506, 122, 'about 8 3/4 ft', gray);
  ln(640, 150, 500, 150, RED); ln(640, 164, 500, 164, INK); tx(506, 144, 'WR39 dimmed power', gray); tx(506, 184, 'about 8 3/4 ft', gray);
  ln(330, 240, 330, 258, RED); ln(340, 240, 340, 266, INK); ln(200, 258, 600, 258, RED); ln(200, 266, 600, 266, INK);
  [200, 400, 600].forEach(cx => { ln(cx - 5, 258, cx - 5, 300, RED); ln(cx + 5, 266, cx + 5, 300, INK); });
  tx(612, 262, 'WR40: three 14 AWG feeds, F1 to F3', gray);
  box(105, 300, 190, 44, 'Driver side strip, 154 in', 'F1: about 2 ft, 2.6 A', '#B8860B', '#FFF8E1'); box(305, 300, 190, 44, 'Passenger side strip, 154 in', 'F2: about 7 1/2 ft, 2.6 A', '#B8860B', '#FFF8E1'); box(505, 300, 190, 44, 'Back strip, 68 in', 'F3: about 8 1/2 ft, 1.1 A', '#B8860B', '#FFF8E1');
  tx(20, 372, 'Slide it or push it: the dimmer switches the strips on or off and sets their brightness, from this one place.', gray);
  tx(20, 388, 'All 6.4 A of the strip runs through the dimmer, so it must be made for 12 V DC and rated 10 A or more.', gray);
  tx(20, 404, 'At each strip: + to + and − to −. Join the 14 AWG cable to a short 18 to 20 AWG pigtail with a lever connector, then solder the pigtail to the pads.', gray);
  tx(20, 420, 'The old 18 AWG cable (WR36, retired) from the W2 box to the couch cabinet stays in place as the pull line for WR38 and WR39.', gray);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Wiring of the soft LED strip: the fuse block feeds the strip junction box JB2, a pair goes to the slide dimmer on the dinette wall and the dimmed power comes back to JB2, which feeds the three strips"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function plateSVG() {
  const o = [], W = 800, H = 884, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.6) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700';
  tx(20, 22, 'A. What a lever connector is: a small block that joins wires together', bold);
  o.push(`<rect x="60" y="60" width="200" height="52" rx="8" fill="#EEF1F4" stroke="#5F5E5A" stroke-width="1.8"/>`);
  ln(70, 100, 250, 100, '#8a867a', 2);
  [85, 150, 215].forEach(x => { o.push(`<rect x="${x - 15}" y="66" width="30" height="30" rx="4" fill="${ORG}" stroke="#A64F00" stroke-width="1.5"/>`); ln(x, 112, x, 168, RED, 3); });
  tx(268, 104, 'metal inside joins every wire', gray);
  tx(60, 52, 'levers: lift to open, press down to lock', gray);
  tx(60, 186, 'wires push in from this side, one per port (3 ports = 3 wires)', gray);
  ['1  Strip about 1/2 in of insulation off the wire.', '2  Lift the lever up.', '3  Push the wire in all the way.', '4  Press the lever down, then tug the wire gently.'].forEach((t, i) => tx(470, 76 + i * 20, t));
  tx(470, 166, 'Every wire in one connector is joined together.', gray); tx(470, 180, 'To take a wire out, lift its lever.', gray); tx(470, 194, 'Brands look a little different.', gray);
  ln(20, 210, 780, 210, '#cfcbbd', 1.5);
  tx(20, 232, 'B. Inside BX1, the plate ED11: one deep two gang box, seen from the front, the two switches side by side', bold);
  o.push('<g transform="translate(0,50)">');
  o.push(`<rect x="230" y="246" width="500" height="286" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(240, 262, 'the deep box', gray);
  const cbox = (x, y, lab, col) => { o.push(`<rect x="${x}" y="${y}" width="120" height="54" rx="7" fill="#EEF1F4" stroke="${col}" stroke-width="2.2"/>`); [x + 22, x + 60, x + 98].forEach(cx => o.push(`<rect x="${cx - 9}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`)); tx(x + 12, y + 42, lab, 'font-size:11px;font-weight:700'); };
  const swb = (x, lab1, lab2) => { o.push(`<rect x="${x}" y="290" width="130" height="64" rx="7" fill="#fff" stroke="${INK}" stroke-width="2"/>`); tx(x + 10, 312, lab1, 'font-size:11.5px;font-weight:700'); tx(x + 10, 328, lab2, 'font-size:11.5px;font-weight:700'); tx(x + 52, 348, 'OUT ↑', gray); tx(x + 52, 370, 'IN ↓', gray); };
  swb(380, 'Rear couch', 'light switch'); swb(560, 'Shower', 'light switch');
  // OUT wires leave through the top
  ln(445, 290, 445, 222, RED, 3); tx(396, 218, 'WR22 + to light ED7', `font-weight:700;fill:${RED};font-size:11px`);
  ln(625, 290, 625, 222, RED, 3); tx(560, 218, 'WR23 + to shower light', `font-weight:700;fill:${RED};font-size:11px`);
  // + side
  ln(20, 410, 250, 410, RED, 3.4); tx(24, 402, 'WR21 +', `font-weight:700;fill:${RED}`);
  cbox(250, 384, '3-port (+)', RED);
  ln(370, 396, 445, 396, RED); ln(445, 396, 445, 358, RED); tx(452, 392, 'jumper 1', gray);
  ln(370, 412, 625, 412, RED); ln(625, 412, 625, 358, RED); tx(560, 428, 'jumper 2', gray);
  // - side
  ln(20, 494, 250, 494, INK, 3.4); tx(24, 486, 'WR21 −', bold);
  cbox(250, 466, '3-port (−)', INK);
  ln(370, 478, 780, 478, INK); ln(370, 496, 780, 496, INK); tx(450, 470, 'WR22 − and WR23 − come back from the lights', gray);
  o.push('</g>');
  ln(20, 600, 780, 600, '#cfcbbd', 1.5);
  tx(20, 622, 'C. What connects to what', bold);
  const rows = [['WR21 + (from JB)', '+ connector, port 1'], ['Jumper 1 (red, about 6 in)', '+ connector, port 2  and  the IN of the rear couch light switch'], ['Jumper 2 (red, about 6 in)', '+ connector, port 3  and  the IN of the shower light switch'],
    ['WR22 +', 'the OUT of the rear couch light switch'], ['WR23 +', 'the OUT of the shower light switch'], ['WR21 − (from JB)', '− connector, port 1'], ['WR22 −', '− connector, port 2'], ['WR23 −', '− connector, port 3']];
  rows.forEach((r, k) => { const y = 644 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  tx(20, 836, 'The + goes through the switches, so a light is only powered when its switch is on.', gray);
  tx(20, 852, 'The − passes straight through the box. Which switch is on the left makes no difference.', gray);
  tx(20, 868, 'The two connectors sit behind the switches, in the same box.', gray);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="How a lever connector works and how the rear doors plate ED11 is wired: WR21 plus goes through a three port connector and two short jumpers to the two switches, and the minus joins WR22 and WR23 in a second connector"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function plate2SVG() {
  const o = [], W = 800, H = 690, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.6) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700';
  tx(20, 22, 'A. Inside BX9, the plate EP11 and EP14: one two gang box under the TV, next to the sliding door opening', bold);
  tx(20, 40, 'How a lever connector works: see EF14. The two switches sit side by side; EP11 is the left rocker, EP14 the right one.', gray);
  o.push(`<rect x="230" y="96" width="500" height="286" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(240, 112, 'the box, seen from the front', gray);
  const cbox = (x, y, lab, col) => { o.push(`<rect x="${x}" y="${y}" width="120" height="54" rx="7" fill="#EEF1F4" stroke="${col}" stroke-width="2.2"/>`); [x + 22, x + 60, x + 98].forEach(cx => o.push(`<rect x="${cx - 9}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`)); tx(x + 12, y + 46, lab, 'font-size:10.5px;font-weight:700'); };
  const swb = (x, l1, l2) => { o.push(`<rect x="${x}" y="140" width="130" height="64" rx="7" fill="#fff" stroke="${INK}" stroke-width="2"/>`); tx(x + 10, 162, l1, 'font-size:11.5px;font-weight:700'); tx(x + 10, 178, l2, 'font-size:11.5px;font-weight:700'); tx(x + 52, 198, 'OUT ↑', gray); tx(x + 70, 224, 'IN ↓', gray); };
  swb(380, 'Counter and sink', 'light switch EP11'); swb(560, 'Center row lights', 'switch EP14');
  ln(445, 140, 445, 72, RED, 3); tx(396, 68, 'WR33 + to EP2 light', `font-weight:700;fill:${RED};font-size:11px`);
  ln(625, 140, 625, 72, RED, 3); tx(560, 68, 'WR34 + to center lights', `font-weight:700;fill:${RED};font-size:11px`);
  ln(20, 260, 250, 260, RED, 3.4); tx(24, 252, 'WR35 +', `font-weight:700;fill:${RED}`);
  cbox(250, 234, '3-port (+)', RED);
  ln(370, 246, 445, 246, RED); ln(445, 246, 445, 208, RED); tx(452, 242, 'jumper 1', gray);
  ln(370, 262, 625, 262, RED); ln(625, 262, 625, 208, RED); tx(560, 278, 'jumper 2', gray);
  ln(20, 344, 250, 344, INK, 3.4); tx(24, 336, 'WR35 −', bold);
  cbox(250, 316, '3-port (−)', INK);
  ln(370, 328, 780, 328, INK); ln(370, 346, 780, 346, INK); tx(450, 320, 'WR33 − and WR34 − go out to the lights', gray);
  ln(20, 410, 780, 410, '#cfcbbd', 1.5);
  tx(20, 432, 'B. What connects to what', bold);
  const rows = [['WR35 + (from JB)', '+ connector, port 1'], ['Jumper 1 (red, about 6 in)', '+ connector, port 2  and  the IN of the counter light switch EP11'], ['Jumper 2 (red, about 6 in)', '+ connector, port 3  and  the IN of the center row switch EP14'],
    ['WR33 +', 'the OUT of the counter light switch EP11'], ['WR34 +', 'the OUT of the center row switch EP14'], ['WR35 − (from JB)', '− connector, port 1'], ['WR33 −', '− connector, port 2'], ['WR34 −', '− connector, port 3']];
  rows.forEach((r, k) => { const y = 454 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  tx(20, 626, 'The + goes through the switches, so a light is only powered when its switch is on. The − passes straight through the box.', gray);
  tx(20, 642, 'Parts: two 3 port lever connectors rated 20 A or more and two red 14 AWG jumpers about 6 in long.', gray);
  tx(20, 658, 'WR33, WR34 and WR35 all run behind the covering to the passenger wall run, so they all come in on the rear side of the box.', gray);
  tx(20, 674, 'The two connectors sit behind the switches, in the same box.', gray);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Inside the passenger switch plate BX9: WR35 plus goes through a three port connector and two short jumpers to the two switches EP11 and EP14, and the minus joins WR33 and WR34 in a second connector"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function box8SVG() {
  const o = [], W = 800, H = 640, ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700', sm = 'font-size:10.5px;font-weight:700';
  const wire = (pts, col, w = 3.2, outline) => { const d = pts.map(p => p.join(',')).join(' '); if (outline) o.push(`<polyline points="${d}" fill="none" stroke="${outline}" stroke-width="${w + 2.6}" stroke-linecap="round" stroke-linejoin="round"/>`); o.push(`<polyline points="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`); };
  const conn = (x, y, lab) => { o.push(`<rect x="${x}" y="${y}" width="120" height="56" rx="7" fill="#EEF1F4" stroke="${INK}" stroke-width="2.2"/>`); for (let i = 0; i < 4; i++) o.push(`<rect x="${x + 14 + i * 28}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`); tx(x + 10, y + 48, lab, sm); };
  const COL = [{ c: '#1b1a17', ol: null, nm: 'black (hot)' }, { c: '#fff', ol: '#8a867a', nm: 'white (neutral)' }, { c: '#2E7D32', ol: null, nm: 'green (ground)' }];
  tx(20, 22, 'A. Inside BX8: the TV outlet EP6 and three cables (WR30 in, WR37 and WR41 on)', bold);
  o.push(`<rect x="190" y="40" width="420" height="292" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(200, 56, 'BX8, 120 V, circuit A (GFCI): where circuit A branches', gray);
  o.push(`<rect x="470" y="64" width="130" height="262" rx="8" fill="#EEF1F4" stroke="#5F5E5A" stroke-width="2"/>`);
  tx(535, 86, 'Outlet EP6', 'font-weight:700;text-anchor:middle'); tx(535, 102, 'duplex, 15 A', 'font-size:11px;fill:#5F5E5A;text-anchor:middle');
  [{ y: 112, sc: '#D4A82A', sl: 'brass (hot)' }, { y: 204, sc: '#C9CDD2', sl: 'silver (neutral)' }, { y: 296, sc: '#2E7D32', sl: 'green (ground)' }].forEach((r, k) => {
    const cl = COL[k]; [-8, 0, 8].forEach(d => wire([[20, r.y + d], [250, r.y + d]], cl.c, 2.6, cl.ol));
    tx(22, r.y - 18, 'WR30, WR37, WR41', sm); tx(22, r.y + 26, cl.nm, gray);
    conn(250, r.y - 28, '4-port');
    wire([[370, r.y], [470, r.y]], cl.c, 3.2, cl.ol); tx(388, r.y - 8, 'pigtail', 'font-size:10.5px;fill:#5F5E5A');
    o.push(`<circle cx="470" cy="${r.y}" r="7" fill="${r.sc}" stroke="#444" stroke-width="1.4"/>`); tx(482, r.y + 20, r.sl, 'font-size:10.5px;fill:#5F5E5A');
  });
  o.push(`<line x1="20" y1="348" x2="780" y2="348" stroke="#cfcbbd" stroke-width="1.5"/>`);
  tx(20, 370, 'B. What connects to what', bold);
  const rows = [['Hot (black): WR30, WR37, WR41', 'one 4 port connector, with a pigtail to the brass screw of the outlet EP6'], ['Neutral (white): WR30, WR37, WR41', 'one 4 port connector, with a pigtail to the silver screw'], ['Ground (green): WR30, WR37, WR41', 'one 4 port connector, with a pigtail to the green screw (and to the box if it is metal)']];
  rows.forEach((r, k) => { const y = 392 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  ['WR30 comes in from the couch outlet BX2 (down the wall at 73 and along above S6). WR37 goes on to the fridge outlet BX5.', 'WR41 goes on to the counter outlet BX6. Each cable has a hot, a neutral and a ground.',
   'Four wires meet in each connector (three cable wires and the pigtail): three 4 port lever connectors rated 20 A or more.', 'With only 3 port connectors: 6 connectors and 3 jumpers (black, white, green, about 3 in).',
   'Three cables, three connectors and the outlet need room: use a deep two gang box (about 37 cu in) or a 4 in square box.', 'The box sits behind the TV: use a right-angle plug and check that the TV mount clears the box.',
   'Circuit A has its 15 A GFCI breaker at the AC panel, so this is a plain outlet. Tag both ends of each cable.'].forEach((t, k) => tx(20, 474 + k * 16, t, gray));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Inside the TV outlet box BX8: the cables WR30, WR37 and WR41 meet the outlet EP6 through three four port connectors and pigtails: black to the brass screw, white to the silver screw and green to the green screw"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function box2SVG() {
  const o = [], W = 800, H = 902, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700', sm = 'font-size:10.5px;font-weight:700';
  const wire = (pts, col, w = 3.2, outline) => { const d = pts.map(p => p.join(',')).join(' '); if (outline) o.push(`<polyline points="${d}" fill="none" stroke="${outline}" stroke-width="${w + 2.6}" stroke-linecap="round" stroke-linejoin="round"/>`); o.push(`<polyline points="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`); };
  const conn = (x, y, n, lab) => { o.push(`<rect x="${x}" y="${y}" width="120" height="56" rx="7" fill="#EEF1F4" stroke="${INK}" stroke-width="2.2"/>`); for (let i = 0; i < n; i++) o.push(`<rect x="${x + 14 + i * 28}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`); tx(x + 10, y + 48, lab, sm); };
  tx(20, 22, 'A. The 120 V side of BX2: the outlet ED10 and three cables (WR18 in, WR19 and WR30 on)', bold);
  o.push(`<rect x="190" y="40" width="420" height="292" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(200, 56, '120 V side, left of the divider', gray);
  o.push(`<rect x="470" y="64" width="130" height="262" rx="8" fill="#EEF1F4" stroke="#5F5E5A" stroke-width="2"/>`);
  tx(535, 86, 'Outlet ED10', 'font-weight:700;text-anchor:middle'); tx(535, 102, 'duplex, 15 A', 'font-size:11px;fill:#5F5E5A;text-anchor:middle');
  [{ y: 112, c: '#1b1a17', ol: null, sc: '#D4A82A', sl: 'brass (hot)', nm: 'black (hot)' }, { y: 204, c: '#fff', ol: '#8a867a', sc: '#C9CDD2', sl: 'silver (neutral)', nm: 'white (neutral)' }, { y: 296, c: '#2E7D32', ol: null, sc: '#2E7D32', sl: 'green (ground)', nm: 'green (ground)' }].forEach(r => {
    [-8, 0, 8].forEach(d => wire([[20, r.y + d], [250, r.y + d]], r.c, 2.6, r.ol));
    tx(22, r.y - 18, 'WR18, WR19, WR30', sm); tx(22, r.y + 26, r.nm, gray);
    conn(250, r.y - 28, 4, '4-port');
    wire([[370, r.y], [470, r.y]], r.c, 3.2, r.ol); tx(388, r.y - 8, 'pigtail', 'font-size:10.5px;fill:#5F5E5A');
    o.push(`<circle cx="470" cy="${r.y}" r="7" fill="${r.sc}" stroke="#444" stroke-width="1.4"/>`); tx(482, r.y + 20, r.sl, 'font-size:10.5px;fill:#5F5E5A');
  });
  o.push(`<line x1="20" y1="348" x2="780" y2="348" stroke="#cfcbbd" stroke-width="1.5"/>`);
  tx(20, 370, 'B. The 12 V side of BX2: the switch ED19 and the two WR20 cables', bold);
  o.push(`<rect x="190" y="386" width="420" height="208" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(200, 402, '12 V side, right of the divider', gray);
  wire([[20, 456], [300, 456]], RED, 3.4); tx(22, 446, 'WR20 feed + from JB', `font-size:11px;font-weight:700;fill:${RED}`);
  o.push(`<rect x="300" y="426" width="120" height="60" rx="7" fill="#fff" stroke="${INK}" stroke-width="2"/>`);
  tx(310, 446, 'Switch ED19', 'font-size:11.5px;font-weight:700'); tx(310, 462, 'right couch light', 'font-size:11px;font-weight:700'); tx(306, 480, 'IN', gray); tx(386, 480, 'OUT', gray);
  wire([[420, 456], [780, 456]], RED, 3.4); tx(616, 446, 'WR20 switched + to ED18', `font-size:11px;font-weight:700;fill:${RED}`);
  wire([[20, 548], [300, 548]], INK, 3.4); tx(22, 538, 'WR20 feed ' + '−' + ' from JB', 'font-size:11px;font-weight:700');
  conn(300, 520, 3, '3-port (−)'); tx(306, 588, 'third port empty', gray);
  wire([[420, 548], [780, 548]], INK, 3.4); tx(616, 538, 'WR20 switched ' + '−' + ' to ED18', 'font-size:11px;font-weight:700');
  o.push(`<line x1="20" y1="608" x2="780" y2="608" stroke="#cfcbbd" stroke-width="1.5"/>`);
  tx(20, 630, 'C. What connects to what', bold);
  const rows = [['Hot (black): WR18, WR19, WR30', 'one 4 port connector, with a pigtail to the brass screw of the outlet ED10'], ['Neutral (white): WR18, WR19, WR30', 'one 4 port connector, with a pigtail to the silver screw'], ['Ground (green): WR18, WR19, WR30', 'one 4 port connector, with a pigtail to the green screw (and to the box if it is metal)'],
    ['WR20 feed + (from JB)', 'the IN of the switch ED19'], ['WR20 switched + (to ED18)', 'the OUT of the switch ED19'], ['WR20 feed − and switched −', 'one connector: the − passes straight through the box']];
  rows.forEach((r, k) => { const y = 652 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  ['WR18 comes in from the AC panel; WR19 goes on to the dinette outlet (BX3) and WR30 to the TV outlet (BX8).', 'Each cable has a hot, a neutral and a ground.', 'Four wires meet in each connector (three cable wires and the pigtail), so use three 4 port lever connectors rated 20 A or more.',
   'With only 3 port connectors, four wires need two connectors and one short jumper: 6 connectors and 3 jumpers (black, white, green, about 3 in).', 'The 12 V side needs one more connector: a 2 port, or a 3 port with one port empty.',
   'The divider keeps the 120 V and 12 V in separate compartments of one deep two gang box: nothing 12 V on the left, nothing 120 V on the right.', 'The 120 V side holds the three cables and the outlet (about 18 cu in): check the real depth of your box.'].forEach((t, k) => tx(20, 784 + k * 16, t, gray));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Inside the couch box BX2: on the 120 V side three cables WR18, WR19 and WR30 meet the outlet ED10 through three four port connectors and pigtails; on the 12 V side the WR20 cables go through the switch ED19 and a connector for the minus"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function box6SVG() {
  const o = [], W = 800, H = 1092, ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700', sm = 'font-size:10.5px;font-weight:700';
  const wire = (pts, col, w = 3.2, outline) => { const d = pts.map(p => p.join(',')).join(' '); if (outline) o.push(`<polyline points="${d}" fill="none" stroke="${outline}" stroke-width="${w + 2.6}" stroke-linecap="round" stroke-linejoin="round"/>`); o.push(`<polyline points="${d}" fill="none" stroke="${col}" stroke-width="${w}" stroke-linecap="round" stroke-linejoin="round"/>`); };
  const conn = (x, y, lab) => { o.push(`<rect x="${x}" y="${y}" width="120" height="56" rx="7" fill="#EEF1F4" stroke="${INK}" stroke-width="2.2"/>`); for (let i = 0; i < 3; i++) o.push(`<rect x="${x + 22 + i * 36}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`); tx(x + 10, y + 48, lab, sm); };
  const COL = [{ c: '#1b1a17', ol: null, nm: 'black (hot)' }, { c: '#fff', ol: '#8a867a', nm: 'white (neutral)' }, { c: '#2E7D32', ol: null, nm: 'green (ground)' }];
  tx(20, 22, 'A. Circuit A in BX6: the counter outlet EP15, the end of circuit A (WR41 comes in, nothing goes on)', bold);
  o.push(`<rect x="190" y="40" width="420" height="292" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(200, 56, '120 V, circuit A (GFCI)', gray);
  o.push(`<rect x="470" y="64" width="130" height="262" rx="8" fill="#EEF1F4" stroke="#5F5E5A" stroke-width="2"/>`);
  tx(535, 86, 'Outlet EP15', 'font-weight:700;text-anchor:middle'); tx(535, 102, 'duplex, 15 A', 'font-size:11px;fill:#5F5E5A;text-anchor:middle');
  [{ y: 112, sc: '#D4A82A', sl: 'brass (hot)' }, { y: 204, sc: '#C9CDD2', sl: 'silver (neutral)' }, { y: 296, sc: '#2E7D32', sl: 'green (ground)' }].forEach((r, k) => {
    const cl = COL[k]; wire([[20, r.y], [470, r.y]], cl.c, 3.2, cl.ol);
    tx(22, r.y - 10, 'WR41 ' + cl.nm, sm);
    o.push(`<circle cx="470" cy="${r.y}" r="7" fill="${r.sc}" stroke="#444" stroke-width="1.4"/>`); tx(482, r.y + 20, r.sl, 'font-size:10.5px;fill:#5F5E5A');
  });
  o.push(`<line x1="20" y1="348" x2="780" y2="348" stroke="#cfcbbd" stroke-width="1.5"/>`);
  tx(20, 370, 'B. Circuit B/D in BX6: the selector EP9 (WR27 comes in, WR28 goes to BX5, WR29 to BX7)', bold);
  o.push(`<rect x="190" y="386" width="420" height="338" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(200, 402, '120 V, circuit B/D (one 15 A GFCI breaker)', gray);
  o.push(`<rect x="330" y="440" width="110" height="96" rx="7" fill="#fff" stroke="${INK}" stroke-width="2"/>`);
  tx(330, 432, 'Selector EP9 (KCD3, 30 A)', 'font-size:11.5px;font-weight:700');
  [[458, 'WR28 hot (to BX5)', 'end pin'], [488, 'WR27 hot (in)', 'common'], [518, 'WR29 hot (to BX7)', 'end pin']].forEach(r => {
    wire([[20, r[0]], [330, r[0]]], '#1b1a17', 3.2); tx(22, r[0] - 8, r[1], 'font-size:11px;font-weight:700');
    o.push(`<circle cx="330" cy="${r[0]}" r="5.5" fill="#C9CDD2" stroke="#444" stroke-width="1.4"/>`); tx(342, r[0] + 4, r[2], 'font-size:10.5px;fill:#5F5E5A');
  });
  tx(330, 554, 'rocker: microwave, off, heater', gray);
  [{ y: 618, k: 1 }, { y: 686, k: 2 }].forEach(r => { const cl = COL[r.k];
    [-8, 0, 8].forEach(d => wire([[20, r.y + d], [300, r.y + d]], cl.c, 2.6, cl.ol));
    tx(22, r.y - 18, 'WR27, WR28, WR29', sm); tx(22, r.y + 26, cl.nm, gray);
    conn(300, r.y - 28, '3-port'); });
  o.push(`<line x1="20" y1="736" x2="780" y2="736" stroke="#cfcbbd" stroke-width="1.5"/>`);
  tx(20, 758, 'C. What connects to what', bold);
  const rows = [['WR41 black wire (hot)', 'the brass screw of the counter outlet EP15'], ['WR41 white wire (neutral)', 'the silver screw'], ['WR41 green wire (ground)', 'the green screw (and the box if it is metal)'],
    ['WR27 hot (in)', 'the middle pin (the common) of the selector EP9'], ['WR28 hot', 'one end pin of the selector (the microwave side)'], ['WR29 hot', 'the other end pin (the heater side)'],
    ['WR27, WR28, WR29 neutral', 'one 3 port connector (not switched; keep them apart from circuit A’s whites)'], ['WR27, WR28, WR29 ground', 'one 3 port connector']];
  rows.forEach((r, k) => { const y = 780 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  ['Four cables meet here: three on circuit B/D (the selector) and one on circuit A (the counter outlet, the end of the line).', 'Use a deep two gang box (about 37 cu in, 3 3/4 in deep): four cables, the rocker and the outlet come to about 28 cu in.',
   'Parts: two 3 port lever connectors rated 20 A or more (circuit B/D neutrals and grounds), and three blue female spade terminals', '(16 to 14 AWG) with heat shrink boots, for the 1/4 in tabs of the selector. The outlet needs no connectors: each WR41 wire goes to its screw.',
   'Only the hot is switched. Neutrals and grounds go straight through. Keep circuit A\u2019s white wire apart from the circuit B/D whites.', 'Check the pins with a continuity tester first: in the middle position no pin touches another;',
   'in each end position the common beeps to one end pin only. Label the switch: microwave, off, heater.', '15 A is enough because only one of the two runs at a time.'].forEach((t, k) => tx(20, 968 + k * 16, t, gray));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Inside the selector and counter outlet box BX6: the one circuit A cable WR41 goes straight to the counter outlet EP15; on circuit B/D the three hot wires WR27, WR28 and WR29 go to the three pins of the selector EP9 and the neutrals and grounds are joined in connectors"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function pinsSVG() {
  const o = [], W = 800, H = 840, COP = '#C77D2E', BLK = '#1b1a17', BLU = '#2F6FBF', MET = '#B9BDC2', TUBE = '#2b2b2b';
  const tx = (x, y, t, st = '') => `<text x="${x}" y="${y}" style="font-size:11px;fill:${INK};${st}">${esc(t)}</text>`;
  const r = (x, y, w, h, fill, stroke, rx = 3, extra = '') => `<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="${rx}" fill="${fill}"${stroke ? ` stroke="${stroke}" stroke-width="1.2"` : ''} ${extra}/>`;
  const ln = (x1, y1, x2, y2, col, w = 2) => `<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`;
  const strands = (x, y) => [-6, -3, 0, 3, 6].map(d => ln(x, y + d * .6, x + 42, y + d * 1.5, COP, 2.2)).join('');
  const sw = (pins) => r(30, 36, 300, 34, '#E8E6DE', '#5F5E5A', 6) + tx(40, 57, 'KCD3 30 A rocker, ON-OFF-ON') + [84, 180, 276].map(x => r(x - 7, 70, 14, 34, MET, '#777', 2)).join('');
  const term = (cx, shrink) => r(cx - 12, 76, 24, 28, '#D6D9DC', '#777', 3) + r(cx - 9, 104, 18, 8, MET, '#777', 2) + r(cx - 12, 112, 24, 18, BLU, '#1B4F93', 5) + r(cx - 4, 130, 8, 18, BLK, null, 3) + (shrink ? r(cx - 17, 70, 34, 66, TUBE, '#000', 11, 'fill-opacity=".62"') : '');
  const P = [
    ['Strip the wire', r(20, 78, 200, 18, BLK, null, 4) + strands(220, 87) + ln(220, 64, 262, 64, '#5F5E5A', 1.6) + ln(220, 59, 220, 69, '#5F5E5A', 1.6) + ln(262, 59, 262, 69, '#5F5E5A', 1.6) + tx(120, 56, 'bare copper 1/4 in (6 mm)'),
      ['Strip 1/4 in (6 mm) of insulation off each of the three', 'black wires: WR27, WR28 and WR29 (14 AWG).', 'Twist the strands so none stick out.']],
    ['Slide the heat shrink on first', r(20, 78, 200, 18, BLK, null, 4) + strands(220, 87) + r(60, 68, 90, 38, TUBE, '#000', 9, 'fill-opacity=".6"') + ln(142, 122, 66, 122, '#C0392B', 3) + `<polygon points="60,122 70,116 70,128" fill="#C0392B"/>` + tx(76, 138, 'slide it well back from the end'),
      ['Cut three pieces of 1/2 in heat shrink tube, about 1 1/4 in', 'long. Put one on each wire now, before the terminal:', 'it cannot go on afterwards.']],
    ['Crimp the terminal', r(10, 78, 95, 18, BLK, null, 4) + r(100, 72, 50, 30, BLU, '#1B4F93', 6) + r(150, 76, 40, 22, MET, '#777', 3) + r(190, 80, 60, 14, '#D6D9DC', '#777', 2) + ln(200, 87, 240, 87, '#8a8f95', 1.4) + `<polygon points="146,50 194,50 188,74 152,74" fill="#7a7f85"/><polygon points="146,124 194,124 188,100 152,100" fill="#7a7f85"/>` + ln(146, 50, 112, 26, '#7a7f85', 7) + ln(146, 124, 112, 148, '#7a7f85', 7) + tx(206, 56, 'crimp here (the metal barrel)'),
      ['Blue female 1/4 in spade terminal (16 to 14 AWG): the', 'bare copper goes in the metal barrel. Squeeze the blue-jaw', 'crimper until it clicks open. Give the wire a firm tug.']],
    ['Test, then push it onto the pin', sw() + term(180, false) + tx(68, 122, 'WR28') + tx(262, 122, 'WR29') + tx(198, 142, 'WR27 on the common', 'font-size:10px'),
      ['Before you shrink anything, check the pins and wires with', 'the tester (a boot cannot be taken off again). Push each', 'terminal fully on: WR27 middle, WR28 and WR29 the ends.']],
    ['Slide the tube over and heat it', sw() + term(180, true) + `<path d="M204,112 q6,-8 12,0 t12,0" fill="none" stroke="#E5532D" stroke-width="2.4"/><path d="M204,124 q6,-8 12,0 t12,0" fill="none" stroke="#E5532D" stroke-width="2.4"/><path d="M204,136 q6,-8 12,0 t12,0" fill="none" stroke="#E5532D" stroke-width="2.4"/>` + `<polygon points="268,116 242,120 242,138 268,142" fill="#7a7f85"/>` + r(268, 112, 62, 34, '#D9822B', '#8a4b10', 7) + r(290, 146, 18, 24, '#D9822B', '#8a4b10', 4) + tx(318, 166, 'heat gun'),
      ['Slide the tube up over the terminal and the pin. Heat it', 'with a heat gun until it hugs tight. Keep the gun moving', 'and the heat off the switch body.']],
    ['Check it', sw() + [84, 180, 276].map(x => term(x, true)).join('') + `<path d="M326,24 l9,11 l18,-22" fill="none" stroke="#2E7D32" stroke-width="4.5" stroke-linecap="round" stroke-linejoin="round"/>`,
      ['No bare metal showing, and each wire gives a gentle tug.', 'Label the switch: microwave, off, heater. The neutrals and', 'grounds do not touch the switch.']]
  ];
  o.push(tx(20, 22, 'You need: three blue female 1/4 in spade terminals (16 to 14 AWG), a ratcheting crimper, three pieces of 1/2 in heat shrink,', 'font-size:12px;font-weight:700'));
  o.push(tx(20, 40, 'wire strippers and a heat gun. The pins of the selector EP9 carry 120 V, so every pin gets a terminal and a boot.', 'font-size:12px'));
  P.forEach((p, k) => { const x = 20 + (k % 2) * 390, y = 56 + Math.floor(k / 2) * 260;
    o.push(`<g transform="translate(${x},${y})"><rect x="0" y="0" width="370" height="246" rx="8" fill="#FAFAF7" stroke="#cfcbbd" stroke-width="1.4"/><circle cx="22" cy="22" r="12" fill="${INK}"/><text x="22" y="26.5" text-anchor="middle" style="font-size:12px;font-weight:700;fill:#fff">${k + 1}</text>${tx(42, 27, p[0], 'font-size:13px;font-weight:700')}<g transform="translate(10,34)">${p[1]}</g>${p[2].map((t, i) => tx(14, 210 + i * 15, t)).join('')}</g>`); });
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Six steps for the selector pins: strip the wire, slide on the heat shrink, crimp the terminal, push it onto the pin, shrink the tube and check it"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function jbSVG() {
  const o = [], W = 800, H = 640, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.6) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700';
  tx(20, 22, 'A. Inside JB: five pairs of wires meet in two 5-port lever connectors, one for the + and one for the −', bold);
  o.push(`<rect x="200" y="44" width="420" height="326" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(212, 62, 'JB, the lights junction box (couch cabinet)', gray);
  const c5 = (y, lab, col) => { o.push(`<rect x="330" y="${y}" width="170" height="72" rx="7" fill="#EEF1F4" stroke="${col}" stroke-width="2.2"/>`); [0, 1, 2, 3, 4].forEach(i => o.push(`<rect x="${344 + i * 29}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`)); tx(342, y + 62, lab, 'font-size:11px;font-weight:700'); };
  c5(92, '5-port (+)', RED); c5(262, '5-port (−)', INK);
  const outs = [['WR21', 'to the rear plate ED11'], ['WR20', 'to the switch ED19'], ['WR24', 'to the dinette switch ED12'], ['WR35', 'to the switches EP11, EP14']];
  outs.forEach((r, i) => { const yr = 112 + i * 14, yb = 282 + i * 14; ln(18, yr, 330, yr, RED, 2.4); ln(18, yb, 330, yb, INK, 2.4); tx(22, yr - 3, r[0] + ' + ' + r[1], `fill:${RED};font-size:10.5px;font-weight:700`); tx(22, yb - 3, r[0] + ' − ' + r[1], 'font-size:10.5px;font-weight:700'); });
  ln(500, 128, 780, 128, RED, 3.4); tx(640, 120, 'WR16 +', `font-weight:700;fill:${RED}`); tx(632, 146, 'from the fuse block, 5 A', gray);
  ln(500, 298, 780, 298, INK, 3.4); tx(640, 290, 'WR16 −', bold); tx(632, 316, 'from the fuse block', gray);
  tx(212, 360, 'Every wire is 14 AWG: red for +, black for −. Tag both ends of every wire.', gray);
  ln(20, 392, 780, 392, '#cfcbbd', 1.5);
  tx(20, 414, 'B. What connects to what', bold);
  const rows = [['WR16 + (from the fuse block)', '+ connector, port 1'], ['WR20 +', '+ connector, port 2 (to the switch ED19 on S6)'], ['WR21 +', '+ connector, port 3 (to the rear plate ED11)'], ['WR24 +', '+ connector, port 4 (to the dinette switch ED12)'], ['WR35 +', '+ connector, port 5 (to the switches EP11 and EP14)'],
    ['WR16 − (from the fuse block)', '− connector, port 1'], ['WR20 −', '− connector, port 2'], ['WR21 −', '− connector, port 3'], ['WR24 −', '− connector, port 4'], ['WR35 −', '− connector, port 5']];
  rows.forEach((r, k) => { const y = 436 + k * 19; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="19" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  tx(20, 646, 'The five wires on each side are joined together by the connector, so the lights get power from WR16 and each out cable takes its share.', gray);
  tx(20, 662, 'A 5 A fuse and about 3 A of lights: 5-port connectors rated 20 A or more are plenty.', gray);
  tx(20, 678, 'With only 3-port connectors: five wires need three connectors and two short jumpers per side', gray);
  tx(20, 694, '(two connectors and one jumper join only four wires, the jumper uses a port at each end).', gray);
  tx(20, 710, 'A box about 4 in square and 2 in deep holds the two connectors and ten wires comfortably. Check your real box.', gray);
  return `<svg viewBox="0 0 ${W} ${H + 82}" role="img" aria-label="Inside the lights junction box JB: the plus wires of WR16, WR20, WR21, WR24 and WR35 join in one five port lever connector and their minus wires in another"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function jb2SVG() {
  const o = [], W = 800, H = 700, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.6) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700', sm = 10.5;
  tx(20, 22, 'A. Inside JB2: the strip circuit meets in three lever connectors (drawn for a dimmer that switches the +)', bold);
  o.push(`<rect x="196" y="44" width="450" height="360" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(208, 62, 'JB2, the strip junction box (couch cabinet, under JB)', gray);
  const cb = (x, y, w, n, lab, col) => { o.push(`<rect x="${x}" y="${y}" width="${w}" height="64" rx="7" fill="#EEF1F4" stroke="${col}" stroke-width="2.2"/>`); for (let i = 0; i < n; i++) o.push(`<rect x="${x + 14 + i * 29}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`); tx(x + 10, y + 54, lab, 'font-size:10.5px;font-weight:700'); };
  cb(210, 100, 112, 2, '2-port (+ supply)', RED); cb(440, 100, 190, 5, '5-port (+ dimmed)', RED); cb(300, 280, 190, 5, '5-port (−)', INK);
  // + supply: WR14 + in, WR38 + out (left side)
  ln(18, 118, 210, 118, RED, 3.2); tx(22, 112, 'WR14 + from the fuse block (10 A)', `fill:${RED};font-size:${sm}px;font-weight:700`);
  ln(18, 144, 210, 144, RED, 3.2); tx(22, 138, 'WR38 + to the dimmer (supply)', `fill:${RED};font-size:${sm}px;font-weight:700`);
  // + dimmed: WR39 + in, F1 F2 F3 out (right side)
  ln(630, 112, 782, 112, RED, 3.2); tx(652, 106, 'WR39 + from the dimmer', `fill:${RED};font-size:${sm}px;font-weight:700`);
  [['F1', 'driver strip'], ['F2', 'passenger strip'], ['F3', 'back strip']].forEach((r, i) => { const y = 130 + i * 18; ln(630, y, 782, y, RED, 2.4); tx(652, y - 4, 'WR40 ' + r[0] + ' + ' + r[1], `fill:${RED};font-size:${sm - .5}px;font-weight:700`); });
  // - connector: WR14 -, WR38 - on the left; F1 F2 F3 - on the right; WR39 - spare
  ln(18, 296, 300, 296, INK, 3.2); tx(22, 290, 'WR14 − from the fuse block', `font-size:${sm}px;font-weight:700`);
  ln(18, 322, 300, 322, INK, 3.2); tx(22, 316, 'WR38 − to the dimmer', `font-size:${sm}px;font-weight:700`);
  [['F1', 'driver strip'], ['F2', 'passenger strip'], ['F3', 'back strip']].forEach((r, i) => { const y = 292 + i * 18; ln(490, y, 782, y, INK, 2.4); tx(652, y - 4, 'WR40 ' + r[0] + ' − ' + r[1], `font-size:${sm - .5}px;font-weight:700`); });
  ln(500, 352, 570, 352, '#8a867a', 2.4); o.push(`<rect x="570" y="346" width="18" height="12" rx="3" fill="#CFCBBD" stroke="#5F5E5A" stroke-width="1"/>`); tx(500, 372, 'WR39 − spare, capped', gray);
  tx(208, 397, 'Every wire is 14 AWG: red +, black −. Tag both ends of every wire.', gray);
  ln(20, 424, 780, 424, '#cfcbbd', 1.5);
  tx(20, 446, 'B. What connects to what', bold);
  const rows = [['WR14 +  (from the fuse block)', '+ supply connector, port 1'], ['WR38 +  (to the dimmer)', '+ supply connector, port 2'], ['WR39 +  (from the dimmer)', '+ dimmed connector, port 1'], ['WR40 F1 +  (driver strip)', '+ dimmed connector, port 2'], ['WR40 F2 +  (passenger strip)', '+ dimmed connector, port 3'], ['WR40 F3 +  (back strip)', '+ dimmed connector, port 4'],
    ['WR14 −  (from the fuse block)', '− connector, port 1'], ['WR38 −  (to the dimmer)', '− connector, port 2'], ['WR40 F1 −', '− connector, port 3'], ['WR40 F2 −', '− connector, port 4'], ['WR40 F3 −', '− connector, port 5'], ['WR39 −  (spare)', 'not connected: put a wire cap on it, and leave the dimmer end free too']];
  rows.forEach((r, k) => { const y = 468 + k * 19; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="19" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(290, y, r[1]); });
  ['Drawn for a dimmer that switches the +. If the KEYGMA switches the − instead, the + and − roles', 'on the dimmed side swap, and I redraw this once I see its terminals.', 'All 6.4 A of the strip passes through the + dimmed connector: use connectors rated 20 A or more.', 'Parts: one 2-port (or 3-port) and two 5-port lever connectors. The lights wires stay in JB, the box above.', 'With only 3-port connectors: the dimmed + (4 wires) takes two connectors and one jumper; the − (5 wires) takes three and two jumpers.', 'A box about 4 in square and 2 in deep holds everything: check your real box.'].forEach((t, k) => tx(20, 716 + k * 16, t, gray));
  return `<svg viewBox="0 0 ${W} ${H + 116}" role="img" aria-label="Inside the strip junction box JB2: the supply plus of WR14 and WR38 meet in one connector, the dimmed plus of WR39 and the three WR40 feeds in a second, and the minus wires in a third"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function jb3SVG() {
  const o = [], W = 800, H = 690, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.6) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700', sm = 10.5;
  tx(20, 22, 'A. Inside JB with 3-port lever connectors: three per side, joined by two short jumpers', bold);
  o.push(`<rect x="150" y="44" width="500" height="372" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(162, 62, 'JB, the lights junction box (couch cabinet)', gray);
  const c3 = (x, y, lab, col) => { o.push(`<rect x="${x}" y="${y}" width="104" height="60" rx="7" fill="#EEF1F4" stroke="${col}" stroke-width="2.2"/>`); [0, 1, 2].forEach(i => o.push(`<rect x="${x + 14 + i * 30}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`)); tx(x + 8, y + 50, lab, 'font-size:10.5px;font-weight:700'); };
  const row = (y, col, sgn, M) => {
    c3(180, y, '3-port ' + M + ' A', col); c3(340, y, '3-port ' + M + ' B', col); c3(500, y, '3-port ' + M + ' C', col);
    ln(284, y + 38, 340, y + 38, col, 3.2); tx(290, y + 78, 'jumper 1', gray);
    ln(444, y + 38, 500, y + 38, col, 3.2); tx(450, y + 78, 'jumper 2', gray);
    const st = `font-size:${sm}px;font-weight:700;${sgn ? 'fill:' + RED : ''}`;
    ln(18, y + 22, 180, y + 22, col, 3); tx(22, y + 16, 'WR16 ' + M + ' fuse block', st);
    ln(18, y + 44, 180, y + 44, col, 3); tx(22, y + 38, 'WR21 ' + M + ' plate ED11', st);
    ln(392, y, 392, y - 26, col, 3); tx(300, y - 32, 'WR20 ' + M + ' to the switch ED19', st);
    ln(604, y + 22, 782, y + 22, col, 3); tx(660, y + 16, 'WR24 ' + M + ' to ED12', st);
    ln(604, y + 44, 782, y + 44, col, 3); tx(660, y + 38, 'WR35 ' + M + ' to EP11, EP14', st);
  };
  row(112, RED, true, '+'); row(290, INK, false, '−');
  tx(162, 408, 'Every wire is 14 AWG: red +, black −. Jumpers about 3 to 4 in long. Tag both ends of every wire.', gray);
  ln(20, 436, 780, 436, '#cfcbbd', 1.5);
  tx(20, 458, 'B. What connects to what (the same on the + side and on the − side)', bold);
  const rows = [['Connector A', 'WR16 (from the fuse block), WR21 (to the rear plate ED11) and jumper 1'], ['Connector B', 'jumper 1, WR20 (to the switch ED19) and jumper 2'], ['Connector C', 'jumper 2, WR24 (to the dinette switch ED12) and WR35 (to EP11 and EP14)']];
  rows.forEach((r, k) => { const y = 482 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(180, y, r[1]); });
  ['Each connector uses all 3 ports: A has 2 wires and a jumper, B has 2 jumpers and a wire, C has a jumper and 2 wires.', 'Parts for JB: 6 three-port connectors (3 for the + side, 3 for the − side) and 4 jumpers (2 red, 2 black).', 'The + side and the − side are two separate rows: never connect a red wire to a black one.', 'The jumpers carry only the current of the wires after them, a few amps at most, so 14 AWG is plenty.'].forEach((t, k) => tx(20, 560 + k * 16, t, gray));
  return `<svg viewBox="0 0 ${W} ${H - 40}" role="img" aria-label="Inside the lights junction box JB with three port lever connectors: three connectors for the plus wires and three for the minus wires, each row joined by two short jumpers"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function jb2c3SVG() {
  const o = [], W = 800, H = 790, RED = '#D32F2F', ORG = '#F57C00', tx = (x, y, t, st = '') => o.push(`<text x="${x}" y="${y}" style="font-size:12px;fill:${INK};${st}">${esc(t)}</text>`);
  const ln = (x1, y1, x2, y2, col, w = 2.6) => o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${col}" stroke-width="${w}" stroke-linecap="round"/>`);
  const gray = 'font-size:11px;fill:#5F5E5A', bold = 'font-weight:700', sm = 10.5;
  tx(20, 22, 'A. Inside JB2 with 3-port lever connectors and jumpers (drawn for a dimmer that switches the +)', bold);
  o.push(`<rect x="150" y="44" width="500" height="478" rx="10" fill="#FAFAF7" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="7 4"/>`);
  tx(162, 62, 'JB2, the strip junction box (couch cabinet, under JB)', gray);
  const c3 = (x, y, lab, col) => { o.push(`<rect x="${x}" y="${y}" width="104" height="60" rx="7" fill="#EEF1F4" stroke="${col}" stroke-width="2.2"/>`); [0, 1, 2].forEach(i => o.push(`<rect x="${x + 14 + i * 30}" y="${y + 5}" width="18" height="14" rx="3" fill="${ORG}" stroke="#A64F00" stroke-width="1"/>`)); tx(x + 8, y + 50, lab, 'font-size:10.5px;font-weight:700'); };
  const st = (c) => `font-size:${sm}px;font-weight:700;${c === RED ? 'fill:' + RED : ''}`;
  // row 1: + supply, one connector, one port spare
  const y1 = 92; c3(330, y1, '+ supply', RED);
  ln(18, y1 + 22, 330, y1 + 22, RED, 3); tx(22, y1 + 16, 'WR14 + fuse block', st(RED));
  ln(434, y1 + 22, 782, y1 + 22, RED, 3); tx(660, y1 + 16, 'WR38 + to dimmer', st(RED));
  tx(340, y1 + 78, 'the third port stays empty', gray);
  // row 2: + dimmed, two connectors and one jumper
  const y2 = 232; c3(250, y2, '+ dimmed A', RED); c3(430, y2, '+ dimmed B', RED);
  ln(354, y2 + 38, 430, y2 + 38, RED, 3.2); tx(366, y2 + 78, 'jumper', gray);
  ln(18, y2 + 22, 250, y2 + 22, RED, 3); tx(22, y2 + 16, 'WR39 + from dimmer', st(RED));
  ln(18, y2 + 44, 250, y2 + 44, RED, 3); tx(22, y2 + 38, 'WR40 F1 + driver', st(RED));
  ln(534, y2 + 22, 782, y2 + 22, RED, 3); tx(660, y2 + 16, 'WR40 F2 + passenger', st(RED));
  ln(534, y2 + 44, 782, y2 + 44, RED, 3); tx(660, y2 + 38, 'WR40 F3 + back', st(RED));
  // row 3: minus, three connectors and two jumpers
  const y3 = 384; c3(180, y3, '3-port ' + '−' + ' A', INK); c3(340, y3, '3-port ' + '−' + ' B', INK); c3(500, y3, '3-port ' + '−' + ' C', INK);
  ln(284, y3 + 38, 340, y3 + 38, INK, 3.2); tx(290, y3 + 78, 'jumper 1', gray); ln(444, y3 + 38, 500, y3 + 38, INK, 3.2); tx(450, y3 + 78, 'jumper 2', gray);
  ln(18, y3 + 22, 180, y3 + 22, INK, 3); tx(22, y3 + 16, 'WR14 − fuse block', st()); ln(18, y3 + 44, 180, y3 + 44, INK, 3); tx(22, y3 + 38, 'WR38 − to dimmer', st());
  ln(392, y3, 392, y3 - 26, INK, 3); tx(300, y3 - 32, 'WR40 F1 − driver strip', st());
  ln(604, y3 + 22, 782, y3 + 22, INK, 3); tx(660, y3 + 16, 'WR40 F2 − passenger', st()); ln(604, y3 + 44, 782, y3 + 44, INK, 3); tx(660, y3 + 38, 'WR40 F3 − back', st());
  tx(162, 490, 'Every wire is 14 AWG: red +, black −. Tag both ends of every wire.', gray);
  tx(162, 506, 'WR39 − is a spare: put a wire cap on it.', gray);
  ln(20, 540, 780, 540, '#cfcbbd', 1.5);
  tx(20, 562, 'B. What connects to what', bold);
  const rows = [['+ supply connector', 'WR14 +, WR38 + and one spare port'], ['+ dimmed connector A', 'WR39 + (from the dimmer), WR40 F1 + and the jumper'], ['+ dimmed connector B', 'the jumper, WR40 F2 + and WR40 F3 +'],
    ['− connector A', 'WR14 −, WR38 − and jumper 1'], ['− connector B', 'jumper 1, WR40 F1 − and jumper 2'], ['− connector C', 'jumper 2, WR40 F2 − and WR40 F3 −']];
  rows.forEach((r, k) => { const y = 586 + k * 20; if (k % 2 === 0) o.push(`<rect x="20" y="${y - 14}" width="760" height="20" fill="#F6F4EE"/>`); tx(30, y, r[0], 'font-weight:700'); tx(250, y, r[1]); });
  ['Parts for JB2: 6 three-port connectors and 3 jumpers (1 red for the dimmed +, 2 black for the −), all rated 20 A or more.', 'With 3 connectors you can do the whole + side now (the supply and the dimmed + take 3); the − side needs 3 more.', 'All 6.4 A of the strip passes through the dimmed + connectors and their jumper: 14 AWG, about 3 to 4 in long.', 'If the KEYGMA switches the − instead of the +, the roles on the dimmed side swap and I redraw this.'].forEach((t, k) => tx(20, 726 + k * 16, t, gray));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Inside the strip junction box JB2 with three port lever connectors: one for the supply plus, two joined by a jumper for the dimmed plus, and three joined by two jumpers for the minus"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
function oneLineSVG(WR) {
  const G = !!WR, id = re => ((WR || []).find(w => re.test(w.n)) || {}).id || '';
  const W = 1070, H = 640, o = [];
  const box = (x, y, w, h, t1, t2, col) => { if (G) col = INK; o.push(`<rect x="${x}" y="${y}" width="${w}" height="${h}" rx="6" fill="#fff" stroke="${col || INK}" stroke-width="1.8"/><text x="${x + w / 2}" y="${y + (t2 ? h / 2 - 3 : h / 2 + 4)}" text-anchor="middle" style="font-size:12.5px;font-weight:700;fill:${INK}">${esc(t1)}</text>`); if (t2) o.push(`<text x="${x + w / 2}" y="${y + h / 2 + 12}" text-anchor="middle" style="font-size:11px;fill:#5F5E5A">${esc(t2)}</text>`); };
  const ln = (x1, y1, x2, y2, col, lab, lx, ly, w, g, wid, px, py, tg) => {
    if (G && g) { const dash = col === C120 ? ' stroke-dasharray="9 6"' : '', tag = tg || wid || '';
      o.push(`<g class="wgrp ${EW.byG[g].cls}"${tag ? ` data-wr="${tag}"` : ''}><line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="#fff" stroke-width="${EW.gw(g) + 3}" stroke-linecap="round"/><line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${EW.gc(g)}" stroke-width="${EW.gw(g)}"${dash}/>${wid ? EW.wirePill(wid, g, px, py) : ''}</g>`); }
    else o.push(`<line x1="${x1}" y1="${y1}" x2="${x2}" y2="${y2}" stroke="${G ? '#9a9a94' : col}" stroke-width="${G ? 1.4 : (w || 2.4)}"/>`);
    if (lab) o.push(`<text x="${lx}" y="${ly}" text-anchor="middle" style="font-size:11px;fill:${INK}">${esc(lab)}</text>`); };
  // sources (left)
  box(20, 30, 190, 50, 'Shore power inlet', '30 A, 120 V', CAC);
  box(20, 105, 190, 52, 'Shore charger VEVOR 80 A', 'shore side only, 14.6 V lithium', INK);
  box(20, 185, 190, 56, 'Alternator', 'starter battery fuse 80 A', INK);
  box(20, 270, 190, 52, 'DC-DC charger LiTime 60 A', 'on the gear shelf', INK);
  ln(115, 80, 115, 105, C120, '15 A breaker', 170, 98, 0, '12', id(/^AC panel to the shore charger/), 115, 92);
  ln(210, 55, 270, 55, C120, '30 A', 240, 48, 0, '10', id(/^Shore power inlet to/), 240, 66);
  ln(115, 241, 115, 270, C12, '', 0, 0, 0, '2', id(/^Cab charge cable/), 72, 256); o.push(`<text x="122" y="259" style="font-size:11px;fill:${INK}">2 AWG, about 15 ft</text>`);
  // the charger output to the battery (2 AWG, 100 A fuse), running down between the left column and the battery
  { const vv = id(/^Shore charger \(VEVOR/); ln(210, 131, 235, 131, C12, '', 0, 0, 0, '2', '', 0, 0, vv); ln(235, 131, 235, 346, C12, '', 0, 0, 0, '2', vv, 235, 160); ln(235, 346, 270, 346, C12, '', 0, 0, 0, '2', '', 0, 0, vv); }
  o.push(`<text x="231" y="338" style="font-size:10.5px;fill:${INK}" transform="rotate(-90 231 338)">VEVOR 2 AWG, 100 A fuse</text>`);
  // transfer switch and the inverter (inverter only: no charger, no transfer switch of its own)
  box(270, 30, 200, 60, 'Transfer switch TS-30, 30 A', 'shore or inverter, never both', C120);
  box(270, 115, 200, 60, 'Inverter BELTTT 2000 W', 'pure sine, inverter only', CAC);
  ln(370, 115, 370, 90, C120, '', 0, 0, 0, '12', id(/^Inverter output/), 392, 103);
  // battery + bus
  box(270, 330, 190, 66, 'Battery 280 Ah, 12.8 V', 'lithium assumed (3.6 kWh)', INK);
  ln(115, 322, 115, 362, C12, '', 0, 0, 0, '2', '', 0, 0, id(/^DC-DC charger to the bus/)); ln(115, 362, 270, 362, C12, '2 AWG, 80 A', 172, 356, 0, '2', id(/^DC-DC charger to the bus/), 150, 378);
  ln(365, 330, 365, 300, C12, 'Class T 250 A, 2/0 AWG', 440, 322, 4, '2/0', id(/^Battery \+ to the Class T/) + ' ' + id(/^Battery . to the shunt/), 312, 315);
  box(270, 240, 190, 54, '+ bus bar and shunt (500 A)', 'near the battery', INK);
  ln(365, 240, 365, 175, C12, '2/0 AWG, 250 A fuse', 440, 214, 4, '2/0', id(/^Bus to the inverter/), 365, 208);
  // 12 V branches (right of the bus)
  const br = [['A/C 12 V, up to 58 A', '6 AWG pair, 100 A fuse', CAC, '6', /^A\/C feed/], ['Fuse block: 4 ceiling, 4 cabinet lights', '14 AWG, 5 A', CLT, '14', /^Lights feed/], ['Soft LED strip, about 31 ft in 3 runs', '14 AWG, its own 10 A circuit', CLT, '14', /^Soft LED strip circuit/], ['Roof fan, up to 2.7 A', '14 AWG, 5 A', C12, '14', /^Roof fan/], ['Water pump, 7 A (under the sink)', '14 AWG, 10 A, own wire', C12, '14', /^Water pump/], ['Control panel and shunt display', '18 AWG, 3 A, own wire', C12, '18', /^Control panel/]];
  br.forEach((b, i) => { const y = 214 + i * 56; ln(460, 267, 540, 267, C12, i === 0 ? '10 AWG, 30 A fuse' : '', 500, 288, 0, '10', i === 0 ? id(/^12 V fuse block feed/) : '', 500, 259, id(/^12 V fuse block feed/)); ln(540, 267, 540, y + 20, C12, '', 0, 0, 0, '10', '', 0, 0, id(/^12 V fuse block feed/)); ln(540, y + 20, 600, y + 20, b[2], '', 0, 0, 2.8, b[3], id(b[4]), 570, y + 12); box(600, y, 330, 40, b[0], b[1], b[2]); });
  o.push(`<text x="600" y="198" style="font-size:12px;font-weight:700;fill:${C12}">12 V DC circuits (your 10-way blade fuse block, 5 of 10 ways used; not the A/C)</text>`);
  // AC side
  ln(470, 60, 600, 60, C120, '', 0, 0, 0, '10', id(/^Transfer switch to the AC panel/), 535, 76);
  box(600, 56, 150, 48, 'AC panel', '30 A main, GFCI', C120);
  o.push(`<text x="540" y="46" style="font-size:12px;font-weight:700;fill:${C120}">120 V AC circuits</text>`);
  [['A  counter outlets, GFCI', '15 A, 14 AWG'], ['B  microwave, its own', '15 A, 14 AWG'], ['C  fridge, TV, dinette outlets', '15 A, 14 AWG'], ['D  water heater 1500 W', '15 A, 14 AWG']].forEach((c, i) => { const y = 16 + i * 0; });
  const ac = [['A  couch, dinette, counter, TV (GFCI)', '15 A, 14 AWG'], ['B/D  microwave or water heater, via the selector', '15 A GFCI, 14 AWG, one at a time'], ['C  fridge, its own breaker', '15 A, 14 AWG']];
  ac.forEach((c, i) => { const x = 770, y = 12 + i * 34; ln(750, 80, 760, 80, C120, '', 0, 0, 0, '12', '', 0, 0, id(/^120 V circuits/)); ln(760, 80, 760, y + 14, C120, '', 0, 0, 0, '12', '', 0, 0, id(/^120 V circuits/)); ln(760, y + 14, x, y + 14, C120, '', 0, 0, 0, '12', i === 0 ? id(/^120 V circuits/) : '', 740, 62, id(/^120 V circuits/)); o.push(`<rect x="${x}" y="${y}" width="280" height="28" rx="5" fill="#fff" stroke="${C120}" stroke-width="1.5"/><text x="${x + 8}" y="${y + 13}" style="font-size:11.5px;font-weight:700;fill:${INK}">${esc(c[0])}</text><text x="${x + 8}" y="${y + 24}" style="font-size:10.5px;fill:#5F5E5A">${esc(c[1])}</text>`); });
  o.push(`<rect x="600" y="112" width="150" height="58" rx="5" fill="#FFF1D6" stroke="${C120}" stroke-width="1.5"/><text x="610" y="128" style="font-size:11.5px;font-weight:700;fill:${INK}">B/D: one 30 A SPDT</text><text x="610" y="143" style="font-size:11px;fill:${INK}">center off rocker (KCD3):</text><text x="610" y="158" style="font-size:11px;fill:${INK}">microwave | off | heater</text>`);
  if (G) o.push(`<text x="600" y="560" style="font-size:11.5px;fill:#5F5E5A">Colour and thickness = gauge; dashed = 120 V; WR = wire number.</text>`);
  o.push(`<text x="20" y="${H - 54}" style="font-size:11.5px;fill:#5F5E5A">Fuses sit within 7 in of the battery or bus (Class T for the inverter, 100 A for the A/C). Wire sizes are for the short runs shown (battery to inverter under 3 ft, A/C about 12 ft);</text><text x="20" y="${H - 38}" style="font-size:11.5px;fill:#5F5E5A">the A/C size comes from a related OutEquipPro model. Follow your inverter’s and the A/C maker’s manuals where they differ.</text><text x="20" y="${H - 22}" style="font-size:11.5px;fill:#5F5E5A">One neutral-to-ground bond only: follow the inverter\u2019s manual (the BELTTT\u2019s was not found) and make sure the transfer switch does not create a second one. Have the 120 V side inspected before use.</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="One-line diagram: shore power and alternator charging, battery, inverter, chargers, transfer switch, fuses and circuits${G ? ', coloured by wire gauge' : ''}"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

function loadTable(d) {
  const P = d.P, Vn = 12.8, ahToKwh = a => a * Vn / 1000, kwhGal = 8.34 * 80 / 3412;
  const batt = P.battAh * Vn / 1000;
  const L = [
    ['Air conditioner, eco', `${fr(P.acEcoA)} A for ${fr(P.acEcoH)} h`, P.acEcoA * P.acEcoH, 'figures from the listing and reviews'],
    ['Fridge, 120 V', 'about 100 W while it runs, assumed 45% of the day', 0.1 * 24 * 0.45 / Vn * 1000, 'your figure of 100 W; the 45% is my assumption for a warm van'],
    ['Inverter idling, on all day for the fridge', 'about 20 W for 24 h', 0.02 * 24 / Vn * 1000, 'assumed; some inverters have a search mode that cuts this to a few watts, but check it still wakes for the fridge'],
    ['4 ceiling lights, 4 under-cabinet lights', 'about 32 W for 4 h', 32 * 4 / Vn, 'assumed LEDs: about 4 W each'],
    ['Roof fan', `${fr(P.fanLowW)} W low, ${fr(P.fanHighW)} W high for ${fr(P.fanHighH)} h`, ((P.fanLowW * (24 - P.fanHighH) + P.fanHighW * P.fanHighH) / 12), 'from the plan'],
    ['Soft LED strip, dimmed', 'about 31 ft at 8 W/m (BTF FCOB 336 LEDs/m), about 30% for 4 h', 76 * .3 * 4 / Vn, 'from the listing: 8 W/m, so about 76 W at full for the 9.55 m; the 30% for 4 h is assumed'],
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
  const WRall = EW.wiresFor(plan, Dlist, Plist, { ac: plan.ac, fan: plan.fan, lights: plan.lights }), WR = WRall.filter(w => !w.retired);   // retired wires keep their number (so no number moves) but have no drawing
  const wDw = EW.wallWires('D', Dlist, baseA, furn.D, WR, symbol, fr, esc, INK), wPw = EW.wallWires('P', Plist, baseD, furn.P, WR, symbol, fr, esc, INK);

  const style = css + `
  body { max-width: none; margin: 0; padding: 0; background: #fff; color: #2C2C2A; color-scheme: light; }
  .wrap { max-width: 1180px; margin: 0 auto; padding-block: 16px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }
  h1 { font-size: 24px; margin: 6px 0 2px; } h2 { font-size: 19px; margin: 28px 0 6px; } h3 { font-size: 16px; margin: 14px 0 4px; }
  .lead { color: #5F5E5A; margin: 4px 0 10px; font-size: 15px; }
  .fid { display: inline-block; font-weight: 700; font-size: 12px; letter-spacing: .04em; background: #2b2a26; color: #fff; border-radius: 5px; padding: 1px 7px; margin-right: 6px; vertical-align: 1px; }
  .figtag { font-size: 14px; margin: 10px 0 0; color: #3d3b34; }
  .figwrap { overflow-x: auto; border: 1px solid #D3D1C7; border-radius: 10px; padding: 6px; margin: 6px 0; background: #fff; }
  .figwrap svg { min-width: 820px; }
  .tog { display: flex; flex-wrap: wrap; gap: 8px 22px; font-size: 14px; margin: 6px 0; }
  .tw { overflow-x: auto; }
  table { border-collapse: collapse; width: 100%; font-size: 14px; margin: 6px 0 8px; }
  th, td { border-bottom: 1px solid #D3D1C7; padding: 5px 8px; text-align: left; vertical-align: top; }
  th { color: #5F5E5A; font-weight: 600; } td.num { white-space: nowrap; text-align: right; } tr.tot td { border-top: 2px solid #5F5E5A; }
  b.id { color: ${C120}; white-space: nowrap; } b.wid { color: #1b1a17; white-space: nowrap; background: #fff; border: 1.5px solid #8a8a84; border-radius: 9px; padding: 0 6px; } b.pid { color: ${CPL}; white-space: nowrap; } .kd { color: #5F5E5A; }
  .note { background: #FAF9F5; border: 1px solid #D3D1C7; border-radius: 10px; padding: 10px 14px; color: #3d3b34; font-size: 14px; margin: 0 0 14px; }
  .note ul { margin: 4px 0 0 18px; padding: 0; } .note li { font-size: 14px; line-height: 1.5; }
  .wtrace { background: #FAF9F5; border: 1px solid #D3D1C7; border-radius: 10px; padding: 10px 14px; margin: 10px 0 8px; }
  @media (min-width: 900px) { .wtrace { position: sticky; top: 0; z-index: 20; box-shadow: 0 3px 10px rgba(0,0,0,.10); } }
  .wt-row { display: flex; flex-wrap: wrap; gap: 8px; align-items: center; }
  .wt-row select { flex: 1 1 260px; min-width: 0; font-size: 14px; padding: 6px; }
  .wt-row button { font-size: 14px; padding: 6px 12px; border: 1px solid #8a8a84; border-radius: 8px; background: #fff; color: #2C2C2A; cursor: pointer; }
  .wt-card { margin-top: 8px; font-size: 14px; line-height: 1.45; color: #3d3b34; }
  .wt-h { font-size: 15px; margin-bottom: 2px; } .wt-id { font-weight: 700; border: 1.5px solid #8a8a84; border-radius: 9px; padding: 0 7px; background: #fff; } .wt-n { font-weight: 600; margin: 2px 0 4px; } .wt-m { color: #5F5E5A; margin-top: 2px; }
  .wt-s, .wt-e { display: inline-block; font-size: 11px; font-weight: 700; color: #fff; border-radius: 9px; padding: 1px 8px; margin-right: 6px; letter-spacing: .4px; } .wt-s { background: #1B7F3B; } .wt-e { background: #111; }
  #wsec svg .wtr { display: none; } #wsec.trace svg .wtr.sel { display: inline; }
  #wsec.trace svg .wgrp { display: none !important; } #wsec.trace svg .wgrp.sel { display: inline !important; }
  tr.wgrp.sel td { background: #FFF6CC; }
  a { color: #185FA5; }`;
  const tog = (id, furr, label, plumbId) => `<div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('${furr}').style.display=this.checked?'':'none'"> Show the furring rails and dots</label><label><input type="checkbox" checked onchange="document.getElementById('${id}').style.display=this.checked?'':'none'"> ${label}</label>${plumbId ? `<label style="color:${CPL};font-weight:600"><input type="checkbox" checked onchange="var d=this.checked?'':'none';document.getElementById('plumb${plumbId}').style.display=d;var t=document.getElementById('plumbTable${plumbId}');if(t)t.style.display=d"> Show the plumbing (pipes)</label>` : ''}</div>`;
  const key = `<p class="legend"><span><svg width="16" height="16" viewBox="0 0 16 16" style="display:inline;vertical-align:-3px;width:16px;min-width:0"><circle cx="8" cy="8" r="6.5" fill="#fff" stroke="${C120}" stroke-width="1.8"/></svg> 120 V outlet</span><span>S = switch</span><span style="color:${CPL};font-weight:600">grey pipes and fixtures with hexagon labels (PL) = plumbing, shown for reference: shower head, valve, pump, drain (hide it with the box above the drawing)</span><span>M = control panel</span><span>REMOTE = inverter remote</span><span>M/H = heater or microwave selector</span><span>IN = shore inlet</span><span style="color:#B8860B">yellow = lights and LED strips</span><span>orange boxes = mounted units</span><span>dashed boxes = furniture (for reference)</span><span style="color:${C12}">blue dashed</span> / <span style="color:${C120}">red dashed</span> = 12 V / 120 V runs</p>`;
  const body = `<div class="wrap">
  <h1>Electrical and lighting layout</h1>
  <p class="lead">A proposal for where the electrics go, drawn on the same steel and furring rails as the wall marking map, with the furniture outlined for reference. Positions are inches from the back mark (0 is 6 in in from the rear-door edge) and up from the floor; the ceiling plan uses inches from the rear-door edge. The steel and furring rails are the measured drawing; the electrical items are my proposal, so check each one against the real wall and tell me what to move.</p>
  <div class="note"><b>What you chose:</b> a 2000 W inverter, charging from the alternator and from shore power (no solar), a 120 V fridge, and the water pump under the sink. <b>What I assumed (tell me if wrong):</b>
  <ul><li>The battery is lithium, 280 Ah at 12.8 V (about 3.6 kWh), where the plan has it under the couch, 52 to 73 in.</li>
  <li><b>Your equipment:</b> a BELTTT 2000 W inverter (an inverter only: the listings show no charger and no transfer switch), a LiTime 60 A DC-DC charger from the alternator (2 AWG from the starter battery), and a VEVOR 80 A lithium shore charger. All three sit on one pull-out gear shelf over the battery under the couch (the shelf slides out into the aisle on two 18 in slides; every cable to it has a loop for that, see the cable table). Because the inverter has no transfer switch, the AC panel has a 30 A transfer switch that connects either shore power or the inverter, never both, and the shore charger is fed from the shore side only, on its own 15 A breaker (about 11 A at 120 V). With the charger running, a heater or microwave and the fridge could pass the 30 A shore inlet, so the charger is its own circuit and the total is worth watching.</li>
  <li><b>Ceiling lights:</b> four: one over the shower (wet rated) and one over the countertop and sink together, both on the slat at 58 in across, and two in the center row (36 and about 100 from the rear-door edge, centered across the van; each is kept 2 in clear of a rib, so they sit at 35 7/8 and 102 1/8), all 12 V and on a slat. The two in the center row share one switch on the passenger wall just rear of the sink. Everything else is lit from the cabinets, the jar nook and the soft LED strip.</li>
  <li><b>Your 12 V lights:</b> a 6 pack of recessed 12 V LED lights for RVs, boats and campers (3000 K warm white, CRI 90+, stepless dimming). The plan has eight 12 V lights (four in the ceiling and four under the cabinets), and you have bought enough of them to cover all eight. I have not seen the listing\u2019s numbers, so check these before you cut any hole: the cutout (hole) size and the depth behind the panel (the ceiling is 3/16 plywood plus a 3/4 slat; the cabinet bottoms are 3/4, and the cabinet is open above them); the watts each (I assumed 4 W); whether the dimming is built into the light (a touch ring or a press-and-hold) or needs a dimmer switch, because the rocker switches in this plan are plain on-off; and the IP rating, since the light over the shower has to be wet rated (IP65). Send me those numbers and I will change the plan to match.</li>
  <li><b>Your 12 V fuse block:</b> a 10-way blade fuse box with a blown-fuse LED on each way and a waterproof cover. The plan uses five of its ten ways, each with its own wire: 1 the lights (WR16, 5 A), 2 the soft LED strip (WR14, 10 A, through the slide dimmer on W2), 3 the roof fan (WR15, 5 A), 4 the water pump (WR31, 10 A), 5 the control panel (WR32, 3 A); ways 6 to 10 are spare (for example to give the ceiling lights and the cabinet lights a fuse each). It is fed by WR13, 10 AWG with a 30 A fuse at the bus. The A/C is not on it (its own 100 A fuse at the battery). I have not seen the listing, so check these before you buy fuses and mount it: that it takes standard ATC or ATO blade fuses (not mini); its rating for each way (most are 30 A, fine for these) and for the feed (most are 100 A in); that its input terminal takes a 10 AWG ring lug; and whether it has a negative bus bar (most have only the + side: then the five \u2212 wires go to the \u2212 bus bar next to it, not onto the block). Its wire terminals are screws or clamps for thicker wire than 18 AWG: use ferrules or ring lugs on the fine-strand copper wire.</li>
  <li><b>Your transfer switch:</b> a TS-30, 30 A. That name is the Go Power! model (an automatic switch with a shore input, a second input for a generator or here the inverter, and one output, locked so that only one input is connected; the listing says it prefers the generator input and waits 20 to 45 seconds before switching to it); other makers use the same name, so check the label. Shore goes to the shore input (WR7, 10 AWG), the inverter output goes to the other input (WR8), and the output goes to the AC panel (WR9, 10 AWG). Things to check in its manual: (1) the priority: if it prefers the second input, then whenever the inverter is on the loads come from the inverter, not shore, so switch the inverter off when you want shore power (the shore charger is fed from the shore side anyway); (2) whether it switches the neutral as well as the hot: this decides the one neutral-to-ground bond (see the note under the one-line diagram); (3) the wire size its terminals take (10 AWG is planned). Its size is listed as about 9 5/8 x 7 1/4 x 4 3/4 in: the hub board is drawn only 10 in tall (1 to 11 in up) and also has to hold the bus bars, the shunt, the Class T fuse, the fuse block and the AC panel, so it will not all fit as drawn: the hub board needs a layout with the real sizes.</li>
  <li><b>Light switches:</b> at the rear doors (the shower light, and the rear one of the two lights under the cabinet over the couch; the roof fan has no switch), in the two gang box on S6 with the couch outlet (the cab-end one of the two lights over the couch, its own), on the dinette\u2019s back wall W2, between the dinette and the driver\u2019s seat (only the two lights under the cabinet over the seats), a two-rocker 12 V plate on the passenger wall under the TV, just rear of the sink (EP11, the left rocker, for the ceiling light over the countertop and the sink, and EP14, the right one, for the two center-row ceiling lights), and a slide dimmer for the soft strip on the dinette\u2019s back wall W2 (ED22). Each switch runs its own group, so ordinary 12 V rated switches work: no push buttons or controller are needed.</li>
  <li><b>Under-cabinet lights:</b> one in the middle of the couch, and two over the dinette, each centered over its bench seat and then moved 6 in toward the table, all on the underside of the wall cabinets. They replace the under-cabinet LED strips, the wall reading lights and the single light over the table I had first suggested.</li>
  <li><b>Soft LED lighting:</b> one warm white dimmable strip around the ceiling edge, along the driver side, across the back and along the passenger side (154 + 68 + 154 = 376 in, about 31 ft), in three runs fed separately: each 154 in side is fed in the middle (user, 2026-11-06: keep the middle feed; at 82 1/2 in on the ceiling diagram), so no strip is more than about 7 ft from its feed, and the 68 in back run is fed at the rear driver corner. The strip you found (BTF-LIGHTING FCOB, 336 LEDs/m, 8 mm wide) is 8 W/m, so the 9.55 m is about 76 W (6.4 A) at full: it has its own 10 A circuit on 14 AWG, with plenty of margin. Buy three 5 m (16.4 ft) reels: two (32.8 ft) would cover the 31.3 ft only with soldered joins and about 1 1/2 ft to spare, and the spare third reel lights something else. One slide dimmer (no controller box) on the dinette\u2019s back wall W2, ED22, that switches and dims all three runs.</li>
  <li><b>Outlets:</b> the four 120 V outlets you asked for (couch, over the middle of the dinette table, above the kitchen nook behind the TV, and the fridge, up by the microwave outlet in the same two gang box), plus one for items on the counter, next to the selector, plus one for the microwave, which cannot share a circuit with them. Everything else is 12 V: the lights, the fan, the pump and the control panel. There are no USB-C or 12 V sockets (you said they are not needed); phones charge from the 120 V outlets.</li>
  <li><b>Wet bath:</b> a wet-rated (IP65) ceiling light over the stall (the exact center is under a rib, so it sits 2 1/2 in toward the cab), and no outlet in the stall (you said no outlet there). The light is at the center of the stall (18 in along the wall, 56 in across from the driver wall). That point falls in the 1 in gap between two slats, so mount the light on a short cross block laid across the gap, or on the nearest slat 2 in to one side. It is one of the four ceiling lights.</li>
  <li>The hot water heater (the SY-15, 1500 W) and the microwave (about 1500 W) must not run together: that is more than a 2000 W inverter can supply. Your 30 A SPDT rocker (KCD3, ON-OFF-ON: microwave, off, heater) on one shared 15 A GFCI breaker makes it impossible: see item ${selId} on the passenger wall.</li>
  <li>All 120 V work is for an electrician to check; I give layout and sizes, not a code review.</li></ul></div>
  <h2>1. One-line diagram</h2>
  ${fig('EF1', 'The one-line diagram: every part and the cable between them')}<div class="figwrap">${oneLineSVG()}</div>
  <h3>The heater or microwave selector, wired (your 30 A SPDT rocker)</h3>
  ${fig('EF2', 'The heater or microwave selector, wired')}<div class="figwrap">${selectorSVG()}</div>
  <h3>The soft LED strip, wired (one slide dimmer on the dinette wall, power through JB2, the three feeds)</h3>
  ${fig('EF13', 'The soft LED strip, wired: fuse block, JB2, slide dimmer on W2 (in box BX4), three strips')}<div class="figwrap">${ledSVG()}</div>
  <h3>The rear doors plate ED11, wired (lever connectors and short jumpers)</h3>
  ${fig('EF14', 'The rear doors plate BX1 (ED11): what a lever connector is, and where WR21, WR22 and WR23 connect')}<div class="figwrap">${plateSVG()}</div>
  <h3>The lights junction box JB, wired (two 5-port lever connectors)</h3>
  ${fig('EF15', 'The lights junction box JB: what connects to what')}<div class="figwrap">${jbSVG()}</div>
  <h3>The strip junction box JB2, wired (three lever connectors)</h3>
  ${fig('EF16', 'The strip junction box JB2: what connects to what')}<div class="figwrap">${jb2SVG()}</div>
  <h3>The lights junction box JB with 3-port lever connectors and jumpers</h3>
  ${fig('EF17', 'The lights junction box JB with 3 port connectors and jumpers: what connects to what')}<div class="figwrap">${jb3SVG()}</div>
  <h3>The strip junction box JB2 with 3-port lever connectors and jumpers</h3>
  ${fig('EF18', 'The strip junction box JB2 with 3 port connectors and jumpers: what connects to what')}<div class="figwrap">${jb2c3SVG()}</div>
  <h3>The switch plate next to the sliding door, BX9</h3>
  ${fig('EF19', 'The passenger switch plate BX9 (EP11 and EP14) wired: what connects to what')}<div class="figwrap">${plate2SVG()}</div>
  <h3>The TV outlet box BX8, centered above the kitchen nook</h3>
  ${fig('EF20', 'The TV outlet box BX8 (EP6) wired: the end of circuit A')}<div class="figwrap">${box8SVG()}</div>
  <h3>The couch box BX2 on S6</h3>
  ${fig('EF21', 'The couch box BX2 (outlet ED10 and switch ED19) wired: what connects to what')}<div class="figwrap">${box2SVG()}</div>
  <h3>The selector and counter outlet box BX6</h3>
  ${fig('EF22', 'The selector and counter outlet box BX6 (EP9 and EP15) wired: what connects to what')}<div class="figwrap">${box6SVG()}</div>
  <h3>The selector\u2019s pins: terminals and heat shrink</h3>
  ${fig('EF23', 'The selector EP9: crimping the terminals and shrinking the boots on its three pins')}<div class="figwrap">${pinsSVG()}</div>
  <h2>1a. High-current cables and fuses to buy</h2>
  ${cableTable()}
  <h2>1b. The hub board: where the parts go</h2>
  <p class="lead">The hub board of the plan (a thin board on the closet\u2019s end panel, 10 in tall) is too small for your parts, and that panel cannot be made bigger because the battery, the inverter and the gear shelf stand in front of it. So the parts are split by where there is room. The TS-30, the AC panel and the fuse block go on the outer face of the divider panel (the tray\u2019s rear side wall, EF3), right beside the tray. The DC parts that have to be near the battery post, the Class T holder, the shunt and the two bus bars, stay on the closet\u2019s end panel (EF4). The wire drawings below still show the hub at 72 to 74 in; they change once you choose.</p>
  <p class="figtag"><span class="fid">EF3</span><span class="fid">EF4</span>Two drawings below: EF3 the divider panel, EF4 the closet\u2019s end panel</p><div class="figwrap">${hubSVG(plan, esc)}</div>
  <h2>1c. Your real board on the pull-out tray</h2>
  <p class="lead">From your photo of the board as built (IMG_0143): the inverter, the DC-DC charger, the shore charger, the two bus bars and the 100 A breaker on one plywood board. This is how it sits on the plan\u2019s pull-out tray, and where the other parts go. The sizes are scaled from the photo, so check them.</p>
  ${fig('EF5', 'Your real board on the pull-out tray, from above')}<div class="figwrap">${trayTopSVG(plan, esc)}</div>
  <h2>2. Driver side wall</h2>
  ${tog('elecD', 'furr', 'Show the electrical items')}
  ${fig('EF6', 'Driver side wall, the electrical items')}<div class="figwrap">${Dw.svg}</div>
  ${key}${Dw.table}
  <h2>3. Passenger side wall</h2>
  ${tog('elecP', 'furrP', 'Show the electrical items', 'P')}
  ${fig('EF7', 'Passenger side wall, the electrical items')}<div class="figwrap">${Pw.svg}</div>
  ${key}${Pw.table}${Pw.ptable}
  <h2>3a. The boxes you wire by hand: BX1 to BX9, JB and JB2</h2>
  <p class="lead">Every box has a short name so you can say which one: BX1 to BX9 along the two walls, and JB and JB2 for the two junction boxes in the couch cabinet. The dashed brown outlines on the two wall drawings mark them; click one to see what is in it. A new box takes the next number.</p>
  ${boxTable()}
  <h2>4. Ceiling: lights, fan, A/C and the wire runs</h2>
  <p class="lead">Four ceiling lights in two rows (positions from the plan): the shower light and the countertop and sink light on one slat, the two center-row lights on another, so each row is on its own slat. The soft LED strip runs round the edge. The driver and passenger wall runs stand at 79 in from the rear-door edge (73 on the wall maps), in the bay between the ribs at 61 and 97. Every rib the cables cross needs a grommeted hole: use any factory holes first, and keep to the web of the rib, not the flange.</p>
  <p class="lead">The drawing for this section is <b>EF12</b> (5d, in section 5 below): the same ceiling with every wire on it, colored by gauge, with the fan, the A/C, the four lights, the ribs and the wall runs. Untick a gauge in the key there to hide its wires. The lights are on one slat per row; the center row goes round the A/C opening, above it, in the gap between slats.</p>
  <div id="wsec">
  <h2>5. All the wires, colored by gauge</h2>
  <p class="lead wlead">Every wire in the van, drawn on the same steel and furring rails (faint) and the same items as the sections above. The colour and the thickness show the gauge (AWG, the bigger the number the thinner the wire); the key sets which ones to show. The routes are my proposal, drawn between the items already on this page, straight along the free bands between the furring rails and up the two wall runs: the real path follows the notches and grommets. The sizes and fuses are the ones in the one-line diagram and the cable table; the few places where I chose a size are marked in the wire list. <b>To follow one wire from where it starts to where it goes, use the wire box just below the key, or open <a href="wires.html">Wire by wire</a>: one diagram for each wire, from the power to its end.</b></p>
  <div class="wkey">${EW.keyHTML(WR)}</div>
  <div class="wtrace" id="wtrace">
    <div class="wt-row"><button type="button" onclick="wtStep(-1)">\u25C0 Previous</button><select id="wtSel" onchange="wtr(this.value)" aria-label="Pick one wire"><option value="">All wires</option>${WR.map(w => `<option value="${w.id}">${w.id} \u00B7 ${EW.byG[w.g].name} AWG \u00B7 ${esc(w.n.length > 72 ? w.n.slice(0, 70) + '\u2026' : w.n)}</option>`).join('')}</select><button type="button" onclick="wtStep(1)">Next \u25B6</button><button type="button" onclick="wtr('')">Show all wires</button></div>
    <div class="wt-card" id="wtCard">All the wires are showing. Pick one (or press Next) and only that wire stays: a green START mark where it begins, a black END mark where it ends, and arrows along the way. The drawings that do not have it are hidden.</div>
  </div>
  <div class="wview" data-title="the one-line diagram" data-nozoom="1"><h3><span class="fid">EF9</span>5a. One-line diagram, by gauge</h3>
  <div class="figwrap">${oneLineSVG(WR)}</div></div>
  <div class="wview" data-title="the driver side wall"><h3><span class="fid">EF10</span>5b. Driver side wall, by gauge</h3>
  <div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('wbaseD').style.display=this.checked?'':'none'"> Show the steel, furring rails and furniture (faint)</label></div>
  <div class="figwrap">${wDw}</div></div>
  <div class="wview" data-title="the passenger side wall"><h3><span class="fid">EF11</span>5c. Passenger side wall, by gauge</h3>
  <div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('wbaseP').style.display=this.checked?'':'none'"> Show the steel, furring rails and furniture (faint)</label></div>
  <div class="figwrap">${wPw}</div></div>
  <div class="wview" data-title="the ceiling"><h3><span class="fid">EF12</span>5d. Ceiling, by gauge</h3>
  <div class="figwrap">${ceilingSVG(plan, WR)}</div></div>
  </div>
  <h3>5e. The wire list</h3>
  <div class="wlist">${EW.tableHTML(WR, fr)}</div>
  <script>
  var WRD = ${JSON.stringify(WR.map(w => ({ id: w.id, g: EW.byG[w.g].name, c: EW.gc(w.g), lw: EW.gw(w.g), t: w.t, n: w.n, from: w.from, to: w.to, prot: w.prot, len: w.len >= 10 ? Math.round(w.len) : Math.round(w.len * 10) / 10, note: (w.note || '') + (w.tnote ? (w.note ? '. ' : '') + w.tnote : '') }))).replace(/</g, '\\u003c')};
  function wgShow(c,on){var l=document.querySelectorAll('.'+c);for(var i=0;i<l.length;i++)l[i].style.display=on?'':'none'}
  function wzoom(svg,id){
    var orig=svg.getAttribute('data-vb')||svg.getAttribute('viewBox');svg.setAttribute('data-vb',orig);
    var o=orig.split(' ').map(Number),els=svg.querySelectorAll('.wtr.sel,.wgrp.sel'),x0=1e9,y0=1e9,x1=-1e9,y1=-1e9,k,b;
    if(!els.length){svg.setAttribute('viewBox',orig);return}
    for(k=0;k<els.length;k++){b=els[k].getBBox();if(!b.width&&!b.height)continue;x0=Math.min(x0,b.x);y0=Math.min(y0,b.y);x1=Math.max(x1,b.x+b.width);y1=Math.max(y1,b.y+b.height)}
    var bw=x1-x0,bh=y1-y0,pad=70,asp=o[3]/o[2];
    if(!(bw>0)||bw>0.6*o[2]&&bh>0.6*o[3]){svg.setAttribute('viewBox',orig);return}
    var w=Math.max(bw+2*pad,640),h=w*asp;if(bh+2*pad>h){h=bh+2*pad;w=h/asp}
    if(w>=o[2]){svg.setAttribute('viewBox',orig);return}
    var cx=(x0+x1)/2,cy=(y0+y1)/2,vx=Math.min(Math.max(cx-w/2,o[0]),o[0]+o[2]-w),vy=Math.min(Math.max(cy-h/2,o[1]),o[1]+o[3]-h);
    svg.setAttribute('viewBox',vx.toFixed(1)+' '+vy.toFixed(1)+' '+w.toFixed(1)+' '+h.toFixed(1))
  }
  function wesc(s){return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;')}
  function wtr(id){
    var sec=document.getElementById('wsec'),all=!id,els=document.querySelectorAll('[data-wr]'),i;
    sec.classList.toggle('trace',!all);
    for(i=0;i<els.length;i++){var on=!all&&(' '+els[i].getAttribute('data-wr')+' ').indexOf(' '+id+' ')>=0;els[i].classList.toggle('sel',on)}
    var vw=document.querySelectorAll('#wsec .wview'),shown=[];
    for(i=0;i<vw.length;i++){var has=all||!!vw[i].querySelector('[data-wr~="'+id+'"]');vw[i].style.display=has?'':'none';if(has&&!all)shown.push(vw[i].getAttribute('data-title'))}
    for(i=0;i<vw.length;i++){if(vw[i].style.display==='none'||vw[i].getAttribute('data-nozoom'))continue;wzoom(vw[i].querySelector('svg'),id)}
    if(all){for(i=0;i<vw.length;i++){var sv=vw[i].querySelector('svg');if(sv&&sv.getAttribute('data-vb'))sv.setAttribute('viewBox',sv.getAttribute('data-vb'))}}
    document.getElementById('wtSel').value=id;
    var card=document.getElementById('wtCard');
    if(all){card.textContent='All the wires are showing. Pick one (or press Next) and only that wire stays: a green START mark where it begins, a black END mark where it ends, and arrows along the way. The drawings that do not have it are hidden.';return}
    var w=WRD.filter(function(x){return x.id===id})[0];
    card.innerHTML='<div class="wt-h"><span class="wt-id">'+w.id+'</span> <svg width="46" height="14" viewBox="0 0 46 14" style="display:inline-block;width:46px;max-width:46px;min-width:0;height:14px;vertical-align:-3px"><line x1="3" y1="7" x2="43" y2="7" stroke="'+w.c+'" stroke-width="'+w.lw+'" stroke-linecap="round"'+(w.t==='ac'?' stroke-dasharray="8 5"':'')+'/></svg> <b>'+w.g+' AWG</b> \u00B7 '+(w.t==='ac'?'120 V':'12 V or battery')+' \u00B7 about '+w.len+' ft</div><div class="wt-n">'+wesc(w.n)+'</div><div class="wt-l"><span class="wt-s">START</span>'+wesc(w.from)+'</div><div class="wt-l"><span class="wt-e">END</span>'+wesc(w.to)+'</div><div class="wt-m"><b>Fuse or breaker:</b> '+wesc(w.prot)+'</div>'+(w.note?'<div class="wt-m">'+wesc(w.note)+'</div>':'')+'<div class="wt-m"><b>Drawn on:</b> '+shown.join(', ')+'</div>'
  }
  function wtStep(d){var s=document.getElementById('wtSel'),i=s.selectedIndex+d;if(i<0)i=s.options.length-1;if(i>=s.options.length)i=0;wtr(s.options[i].value)}
  var ITEMS = ${JSON.stringify(ITEM_INFO).replace(/</g, '\\u003c')};
  (function(){
  var pop=document.createElement('div');pop.id='ipop';pop.hidden=true;document.body.appendChild(pop);
  function has(t,id){var i=t.indexOf(id);while(i>=0){var c=t.charAt(i+id.length);if(!(c>='0'&&c<='9'))return true;i=t.indexOf(id,i+1)}return false}
  function wiresOf(id){var r=[];if(typeof WRD==='undefined')return r;for(var i=0;i<WRD.length;i++){var w=WRD[i];if(has(' '+w.from+' '+w.to+' '+w.n+' ',id))r.push(w.id)}return r}
  function vis(e){return e.getClientRects().length>0}
  var shownAt=0;function hide(){pop.hidden=true}
  window.addEventListener('scroll',function(){if(!pop.hidden&&Date.now()-shownAt>400)hide()},{passive:true});
  function flash(l){for(var i=0;i<l.length;i++)l[i].classList.add('hl');setTimeout(function(){for(var i=0;i<l.length;i++)l[i].classList.remove('hl')},3000)}
  function show(id,el){var it=ITEMS[id];if(!it)return;var ws=wiresOf(id),note=it.note||'';if(note.length>420)note=note.slice(0,417)+'...';
    pop.innerHTML='<div class="ph"><b>'+id+'</b> '+wesc(it.n)+'</div><div class="pw">'+wesc(it.where)+'</div>'+(ws.length?'<div class="pw">Wires: '+ws.join(', ')+'</div>':'')+'<div class="pn">'+wesc(note)+'</div><div class="pa"><a href="#" data-row="'+id+'">Show its table row</a> &middot; <a href="#" data-close="1">Close</a></div>';
    pop.hidden=false;shownAt=Date.now();var r=el.getBoundingClientRect(),w=pop.offsetWidth,h=pop.offsetHeight;
    var x=Math.max(8,Math.min(r.left,window.innerWidth-w-8)),y=r.bottom+8;if(y+h>window.innerHeight-8)y=Math.max(8,r.top-h-8);
    pop.style.left=x+'px';pop.style.top=y+'px'}
  function pick(id){var l=document.querySelectorAll('[data-item="'+id+'"]');for(var i=0;i<l.length;i++)if(vis(l[i]))return l[i];return null}
  function row(id){var r=document.getElementById('item-'+id);if(r){r.scrollIntoView({behavior:'smooth',block:'center'});flash([r])}}
  function go(id){var els=document.querySelectorAll('[data-item="'+id+'"]'),el=pick(id);if(!el){row(id);return}
    var same=[];for(var i=0;i<els.length;i++)if(els[i].ownerSVGElement===el.ownerSVGElement)same.push(els[i]);
    el.scrollIntoView({block:'center'});flash(same);setTimeout(function(){show(id,el)},120)}
  document.addEventListener('click',function(ev){var t=ev.target;if(!t.closest)return;
    var a=t.closest('[data-row]');if(a){ev.preventDefault();hide();row(a.getAttribute('data-row'));return}
    if(t.closest('[data-close]')){ev.preventDefault();hide();return}
    var g=t.closest('[data-go]');if(g){go(g.getAttribute('data-go'));return}
    var it=t.closest('[data-item]');if(it){show(it.getAttribute('data-item'),it);return}
    if(!t.closest('#ipop'))hide()});
  document.addEventListener('keydown',function(ev){if(ev.key==='Escape')hide();var g=ev.target&&ev.target.getAttribute&&ev.target.getAttribute('data-go');if(g&&(ev.key==='Enter'||ev.key===' ')){ev.preventDefault();go(g)}});
  })();
  </script>
  <style>
  .itm{cursor:pointer}
  .bxt{color:#7A4B12;font-weight:700;white-space:nowrap}
  .itm.hl{filter:drop-shadow(0 0 3px #ff9800) drop-shadow(0 0 7px #ff9800)}
  b.id[data-go]{cursor:pointer;text-decoration:underline dotted;text-underline-offset:3px}
  b.id[data-go]:hover,b.id[data-go]:focus{background:#fff3cd;outline:none}
  tr.hl td{background:#fff3cd}
  #ipop{position:fixed;z-index:60;max-width:min(380px,92vw);background:#fff;color:#1b1a17;border:1.5px solid #185FA5;border-radius:10px;padding:10px 12px;box-shadow:0 8px 24px rgba(0,0,0,.28);font-size:13px;line-height:1.4}
  #ipop[hidden]{display:none}
  #ipop .ph{font-size:14px;margin-bottom:3px}#ipop .pw{color:#5F5E5A;margin-bottom:3px}#ipop .pn{margin:6px 0;color:#2C2C2A}#ipop .pa{font-size:12px}
  </style>
  <h2>6. What it adds up to</h2>
  ${loadTable(plan)}
  <h2>7. Order of work</h2>
  <div class="note"><ul>
  <li>Before the walls and ceiling are covered: run the cables up both walls, across the ceiling and every branch, with grommets in all steel and the 12 V and 120 V in separate looms (at least 2 in apart, crossing at right angles). This is the rough-in step of the build order.</li>
  <li>With the furring rails: fix the electrical boxes to blocking between the furring rails, and add the blocking behind the switch plates and the outlets before the planks go on (the TS-30, the AC panel and the fuse block are on the divider panel, which is a board of its own).</li>
  <li>Last: the Class T fuse and shunt on the end panel, the bus bars, the inverter and the two chargers on the tray, the TS-30, the AC panel and the fuse block on the divider, the lights and the plates, after the covering is up.</li>
  <li>Test every circuit with a meter before you connect the battery, and test the GFCI outlets with the button.</li></ul></div>
  <p class="lead" style="margin-top:14px"><a href="interactive.html">Back to the interactive plan</a> &middot; <a href="wall-map.html">Wall marking map</a></p>
  </div>`;
  // ---- wires.html: one diagram for each wire (power chain and the whole run), sharing one copy of the wall and ceiling base through <use>
  { const EC = require('./elcards.js');
    const LD = EW.wallLayers('D', Dlist, baseA, furn.D, symbol, esc, INK), LP = EW.wallLayers('P', Plist, baseD, furn.P, symbol, esc, INK);
    const noDefs = t => t.replace(/<defs>[\s\S]*?<\/defs>/g, ''), defs = (baseA.inner.match(/<defs>[\s\S]*?<\/defs>/g) || []).join('') + (baseD.inner.match(/<defs>[\s\S]*?<\/defs>/g) || []).join('');
    const hidden = `<svg width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">${defs}<g id="bD">${noDefs(LD.inner)}</g><g id="fD">${LD.fu}${LD.bigs.join('')}${LD.pump}${LD.stub}${LD.smalls.join('')}${LD.call}</g><g id="bP">${noDefs(LP.inner)}</g><g id="fP">${LP.fu}${LP.bigs.join('')}${LP.pump}${LP.stub}${LP.smalls.join('')}${LP.call}</g><g id="bC">${ceilingSVG(plan, null, true)}</g></svg>`;
    const ctx = { D: { X: LD.X, Y: LD.Y, H: 636, name: 'driver wall', use: '<use href="#bD" opacity=".33"/><use href="#fD"/>' }, P: { X: LP.X, Y: LP.Y, H: 636, name: 'passenger wall', use: '<use href="#bP" opacity=".33"/><use href="#fP"/>' }, C: { X: x => 50 + 6 * x, Y: y => 56 + 6 * y, H: 500, name: 'ceiling', use: '<use href="#bC"/>' } };
    const { index, cards } = EC.cardsPage(WRall, ctx);
    const wstyle = style + `
  .wcard { border-top: 3px solid #1b1a17; margin-top: 30px; padding-top: 6px; }
  .wcard h3 { font-size: 18px; margin: 6px 0 6px; } .wcard h4 { font-size: 14px; margin: 12px 0 2px; color: #3d3b34; } .wcard h4 .kd { font-weight: 400; }
  .wc-h { font-size: 15px; } .wc-l { margin: 3px 0; font-size: 14.5px; }
  .wt-s, .wt-e { display: inline-block; font-size: 11px; font-weight: 700; color: #fff; border-radius: 9px; padding: 1px 8px; margin-right: 8px; letter-spacing: .4px; } .wt-s { background: #1B7F3B; } .wt-e { background: #111; }
  b.wid { color: #1b1a17; white-space: nowrap; background: #fff; border: 1.5px solid #8a8a84; border-radius: 9px; padding: 0 6px; }`;
    const wbody = `<div class="wrap">
  <h1>Wire by wire</h1>
  <p class="lead">One diagram for each of the ${WR.length} wires in use (${WRall.length} numbers; the retired ones keep their number and have a short card) on the <a href="electric.html">electrical layout page</a>. Each starts with the chain from the power (the battery, the shore power inlet or the starter battery) through the fuses to the end of the wire, with the wire numbers on the arrows and this wire highlighted; then its whole run on the wall and the ceiling drawings, zoomed in, from the green START mark to the black END mark, with arrows showing the direction. Colour and thickness are the gauge, as on the electrical page (a solid line is 12 V or battery cable, a dashed line is 120 V). The routes are my proposal, drawn straight along the free bands between the furring rails and up the two wall runs, not measured paths.</p>
  ${index}
  ${cards}
  <p class="lead" style="margin-top:14px"><a href="electric.html">Back to the electrical layout</a> &middot; <a href="interactive.html">The interactive plan</a></p>
  </div>`;
    fs.writeFileSync(__dirname + '/../cheatsheet.html', cheatHTML(WRall, BOXES));   // the printable one-page list of every wire
    fs.writeFileSync(__dirname + '/../wires.html', `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Wire by wire</title><style>${wstyle}</style></head><body>${hidden}${wbody}</body></html>`);
    if (process.env.SC) { fs.mkdirSync(process.env.SC + '/wires', { recursive: true }); fs.writeFileSync(process.env.SC + '/wires/index.html', `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Wire by Wire</title>\n<style>${wstyle}</style>\n${hidden}${wbody.replace('<a href="electric.html">electrical layout page</a>', '<a href="https://claude.ai/artifact/8PUd9dBRmRp6NNH54L33bZ" target="_blank" rel="noopener">electrical layout page</a>').replace('<a href="electric.html">Back to the electrical layout</a>', '<a href="https://claude.ai/artifact/8PUd9dBRmRp6NNH54L33bZ" target="_blank" rel="noopener">Back to the electrical layout</a>').replace('<a href="interactive.html">The interactive plan</a>', '<a href="https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs" target="_blank" rel="noopener">The interactive plan</a>')}\n`); }
  }
  const doc = `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Electrical layout</title><style>${style}</style></head><body>${body}</body></html>`;
  fs.writeFileSync(__dirname + '/../electric.html', doc);
  if (!process.env.SC) return console.log('electric.html', doc.length);
  fs.mkdirSync(process.env.SC + '/elec', {recursive: true});
  const frag = `<meta name="claude:viewport-fit-sides" content="cover">\n<title>Electrical Layout</title>\n<style>${style}</style>\n${body.replace('<a href="interactive.html">', '<a href="https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs" target="_blank" rel="noopener">').replace('<a href="wall-map.html">', '<a href="https://claude.ai/artifact/1quE178yLUJmgmSuhm626H" target="_blank" rel="noopener">')}\n`;
  fs.writeFileSync(process.env.SC + '/elec/index.html', frag);
  console.log('electric.html', doc.length, 'driver', E_DRIVER(plan).length, 'pass', E_PASS(plan).length);
})();
