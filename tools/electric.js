/* Builds ../electric.html: the electrical and lighting layout.
   Like wallmap.js it reads the plan's own layout from interactive.html in a headless browser and the steel / furring drawing from sides.html
   (diagrams A and D), so the positions follow the plan's sizes. The electrical choices (where each outlet, switch, light, fuse and run goes)
   are the proposal written below as E_*; change them there.
   Run:  node tools/electric.js        (needs playwright + the bundled Chromium; build.sh runs it and skips it if they are missing)
*/
const {chromium} = require(process.env.NODE_PATH + '/playwright');
const fs = require('fs');
const EW = require('./elwires.js');
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
  {k:'box',   n:'Power hub board',                             x0:72, x1:74, z0:1, z1:11, note:'a plywood board on the closet’s rear panel, facing the battery: DC bus bars, shunt, Class T fuse, the 12 V fuse block (your 10-way blade block, five ways used), and the AC panel with its 30 A transfer switch (shore or inverter, never both) and the breakers for the shore charger. The inverter and the two chargers are separate, on the pull-out gear shelf over the battery. The couch front under the deck is open (not covered), so the board and the battery are reached from the aisle without a hatch'},
  {k:'inlet', n:'Shore power inlet (30 A)',                    x:9, z:15.75,  note:'on the outside of the driver wall in the cover plate CP (CP is 4 3/4 to 13 1/4 in along, 10 3/4 to 16 3/4 up, a plate and not a hole, so it is cut for the inlet): 9 in along and 15 3/4 up, 2 in above the middle of CP so that its back clears the furring rail S2 (S2 is 10 1/4 to 13 3/4 up and sits straight on the steel). A 3 in inlet flange then spans 14 1/4 to 17 1/4, about 1/2 in over the top edge of CP: check your inlet against the plate before you cut. Moved here from 80 in along, 21 up. The 30 A cable (10 AWG in flexible conduit, about 8 ft) runs inside the wall in the free band above S2, which is 13 3/4 to 19 1/2 up and clear of the couch wall-post screws (they go into S1 and S2), to the closet’s rear panel at about 73 in, then down to the hub board and its 30 A breaker; where it drops past S2 it needs a groove in the back of S2 or a gap. The couch frame’s back rail (13 1/2 to 17 up) is in front of the spot, so reach the inlet’s back with the couch lifted out, or cut a small access panel in the plywood'},
  {k:'lt',    n:'Light under the cabinet over the couch, rear (left) of two', x:pl.bedX0 + pl.bedLen / 4, z:lz, note:'user: ED7 will be 2, centered under the cabinets above the couch. 12 V LED on the underside of the wall cabinet (bottom at ' + fr(pl.cabBot) + ' in), a quarter of the way along the couch (' + fr(pl.bedX0) + ' to ' + fr(pl.bedX1) + '), so the two lights are centered on its two halves; this one, nearer the rear doors, is on the second switch of the plate at the rear doors (ED11; the other light has its own switch next to it); the wire comes down from inside the cabinet'},
  {k:'lt',    n:'Light under the cabinet, dinette rear seat',  x:(pl.bA[0] + pl.bA[1]) / 2 + 6, z:lz, note:'centered over the rear bench seat (' + fr(pl.bA[0]) + ' to ' + fr(pl.bA[1]) + '), then 6 in toward the table; on the dinette switch'},
  {k:'lt',    n:'Light under the cabinet, dinette cab-end seat', x:(pl.bB[0] + pl.bB[1]) / 2 - 6, z:lz, note:'centered over the cab-end bench seat (' + fr(pl.bB[0]) + ' to ' + fr(pl.bB[1]) + '), then 6 in toward the table; on the dinette switch. These two replace the single light I had over the table'},
  {k:'out120',n:'Couch outlet (120 V duplex, two plugs)', x:62, z:57.25, note:'one single gang box on furring rail S6 (57 1/4 up, on the 3 1/2 in rail), above the nook behind the couch (it was 44 up, which is inside the nook now): a duplex outlet (two plugs) on circuit A (GFCI), 12 AWG. It used to be a 2 gang plate with the light switch; the couch lights are now switched at the rear doors (the rear one) and next to the light (the cab-end one), so this box is the outlet only'},
  {k:'sw',    n:'Switch plate at the rear doors (shower light, rear couch light)', x:1.75,  z:48, note:'2 gang: the wet bath light over the shower (user: ED11 is for the shower light only) and the rear (left) one of the two lights under the cabinet over the couch (user: its switch will be there too). The roof fan has no switch (user: it operates without one): its 12 V feed is straight from the fuse block, fused, and it is controlled at the fan itself. Two single gang boxes one over the other, because the wall between the rear and the nook behind the couch (its rear frame V5 is at 3 1/2 to 5 in) is only 3 1/2 in wide'},
  {k:'sw',    n:'Light switch on the dinette\u2019s back wall (W2)', x:pl.cab - 1, z:48, note:'on W2, the 3/4 in floor-to-ceiling wall that separates the dinette from the driver\u2019s seat (user: ED12 is on the back wall of the dinette), on its dinette face, 48 in up (10 in above the bench back at 38) and about 3 in out from the driver wall, so it is seen here at the corner of the driver wall with W2; the two lights under the cabinet over the dinette seats only (user: the switch will only be for the dinette lights; the ceiling light over the countertop and the sink has its own switch on the passenger wall). W2 is solid plywood with no cavity, so the switch goes in a shallow surface-mount box on its face; the wire comes down the corner behind the planks and into the side of the box through a 1/2 in hole in the plank (a grommet in it). Move the box along W2 if you would rather reach it from the middle of the bench'},
  {k:'strip', n:'Soft LED strip, ceiling edge, driver side run (154 in)', x0:1, x1:pl.cab - 1, z:73, note:'one of three runs of the strip you found: BTF-LIGHTING FCOB (flip chip COB, no dots) warm white 2700 K, 12 V, 336 LEDs/m, 8 W/m (about 2.4 W a foot), 8 mm wide, CRI 90+, double-layer copper PCB, 3M adhesive backing, cuttable at the marked spots, with a 5.5 x 2.1 mm DC plug on each end of a 16.4 ft (5 m) reel (the listing says UL listed: look for the UL mark and file number on the package). It sits in an aluminum channel with a frosted diffuser (the channel must take an 8 mm strip), at the ceiling edge, aimed up so it glows off the cedar ceiling. Cut off the plugs and solder the feed wires at the cut spots, since the plugs loosen with vibration. The wall cabinets run up to the ceiling here, so the channel sits on the top front edge of the cabinets behind a 1 in lip. Fed from the ceiling junction box through riser A'},
  {k:'sw',    n:'Switch and dimmer for the soft LED lighting',  x:68, z:57.25, note:'next to the couch outlet, on S6 too (a separate single gang box, 6 in along from it, clear of the S6 joint at 71 1/4): a momentary push button into a 12 V PWM dimming controller for the soft strip (rated 10 A or more: the strip is about 6.4 A at full brightness; the listing\u2019s ELV, TRIAC and DMX dimmers are for mains-powered drivers, not for this 12 V strip), which has its own 12 V circuit (10 A, 14 AWG) because the strip draws more than the other lights. Say if you want it on the rear doors plate or the dinette plate instead'},
  {k:'out120',n:'Outlet over the dinette table (120 V duplex)', x:tc, z:oz, note:'on the wall just over the table (its top is at 29 in), in the middle of it, clear of the backrests (38 in)' + (pl.win ? '; moved down from 36 to ' + fr(oz) + ' in up because the side window (its frame starts at ' + fr(pl.win.cz0 - 1.5) + ') is now over the table' : '') + '; circuit A (GFCI)'},
  {k:'run',   n:'Riser A: A/C, 12 V and lights feed',          x:76.5, z0:11, z1:75, note:'up inside the wall behind the planks (4 1/2 in space) to the ceiling, jogged from the hub board (72 to 74) to 76 1/2 in so that it climbs just past the front frame V6 of the nook behind the couch (74 to 75 1/2) and not through the nook (drill S5, do not notch it): A/C 6 AWG pair in its own loom, plus the 12 V circuit wires from the fuse block, each its own wire (the strip 14 AWG, the fan 14 AWG, the lights 16 AWG, the dimmer button 18 AWG, and the pump 14 AWG and the control panel 18 AWG, which go on across the ceiling to riser B: there is no shared 12 V trunk). Grommet where it crosses the top steel'},
  {k:'run',   n:'Cab charge cable (DC-DC input)',              x:70, z0:0, z1:1,  note:'2 AWG from the starter battery fuse (80 A) under the van along the driver side frame to a sealed floor grommet next to the battery'},
  {k:'lt',    n:'Light under the cabinet over the couch, cab-end (right) of two', x:pl.bedX0 + 3 * pl.bedLen / 4, z:lz, note:'the second of the two lights under the cabinet over the couch (user: ED7 will be 2, centered), three quarters of the way along it, the one closer to the cab; 12 V LED on the underside of the wall cabinet; on its own switch right next to it (the next item). Added last, so no ED number moved'},
  {k:'sw',    n:'Switch for the cab-end (right) couch light, next to the light', x:pl.bedX0 + 3 * pl.bedLen / 4 + 3, z:lz, note:'user: the light switch for the right light (closer to the cab) will be right next to the light. A small 12 V rocker on the underside of the wall cabinet, 3 in toward the cab from the light (my reading of \u201cright next to\u201d; slide it if you want it nearer), wired inside the cabinet, so no wire shows; it switches only that light'},
]; };
const E_PASS = pl => { const sl = pl.lights.filter(l => l.x > 6 && l.x < 6 + pl.panW)[0] || { x: 6 + pl.panW / 2, y: pl.P.vanW - pl.panD / 2 }, wbx = sl.x - 6, wby = sl.y, cl = pl.lights.filter(l => l.x - 6 >= pl.panW).sort((a, b) => a.x - b.x); return [
  {k:'lt',    n:'Wet bath light (ceiling, IP65), over the shower', x:wbx, z:pl.ceilF - .5, note:'over the middle of the stall: ' + fr(wbx) + ' in along the wall, ' + fr(wby) + ' in across from the driver wall, on the slat (the exact center, 18 in, is under a rib, so it sits 2 1/2 in toward the cab); a wet-rated (IP65) LED; one of the four ceiling lights (the two others are in the center row, EP12 and EP13). Switched at the rear doors plate'},
  {k:'lt',    n:'Ceiling light over the countertop and the sink', x:cl[0] ? cl[0].x - 6 : 89.4, z:pl.ceilF - .5, note:'one light over both, about the middle of the counter cabinet and the sink cabinet together (58 to 123), ' + fr(cl[0] ? cl[0].y : 58) + ' in across from the driver wall, on the slat and 2 in clear of the rib at 97 3/8; on its own 12 V switch, the left rocker (EP11) of the two-rocker plate under the TV, not on the dinette switch'},
  {k:'out120',n:'Fridge outlet, behind the fridge (120 V)',    x:47, z:6,  note:'on the wall behind the fridge platform (the fridge stands on a platform 8 1/4 up); circuit C, the fridge alone'},
  {k:'out120',n:'Microwave outlet (120 V, through the selector)',    x:60, z:64, note:'a fifth outlet you did not list: the microwave (1500 W) needs its own, on the wall just cab-side of it (36 to 58); circuit B/D, fed through the selector (one end pin of your 30 A rocker), 12 AWG, with a 20 A rated receptacle (a single receptacle on a 20 A circuit; it takes 15 A plugs too). Drop it if the microwave plugs in elsewhere'},
  {k:'panel', n:'Control panel (battery monitor, pump switch, tank levels)', x:66, z:50, note:'12 V, small 18 AWG, 3 A'},
  {k:'out120',n:'Outlet under the TV (120 V)',                  x:96, z:52.5, note:'on the wall strip under the TV (its bottom is at 54), above the dish towel hook (98 1/2, 50 up): check the plug clears the towel. Near the sink, so circuit A (GFCI)'},
  {k:'box',   n:'Hot water heater feed (120 V, 20 A, circuit B/D)', x0:85, x1:87, z0:12, z1:18, note:'junction box beside the hot water tank (87 to 101), level with it now that the heater sits on the fresh tank (10 3/4 to 23 3/4 up); 12 AWG, fed through the selector (the other end pin of your 30 A rocker, on the shared 20 A breaker B/D); heater is 1440 W'},
  {k:'strip', n:'Soft LED strip, ceiling edge, passenger side run (154 in)', x0:1, x1:pl.cab - 1, z:73, note:'the other long run, same BTF-LIGHTING FCOB strip and channel, at the top of the wall covering; over the sliding door opening (104 to 155, up to 67 in) the channel carries on along the header at 73 in. Fed through riser B'},
  {k:'sel',   n:'Heater or microwave selector (your 30 A SPDT KCD3 rocker, ON-OFF-ON)', x:71, z:50, note:'your 30 A SPDT rocker (KCD3, 125/250 V AC, 3 pins, ON-OFF-ON) does this, with one change from my first plan: it is a single pole, so the two circuits now share ONE breaker (a 2 pole switch was what let each keep its own). Breaker B/D (20 A, 12 AWG) feeds the middle pin, the common; one end pin goes to the microwave outlet\u2019s hot and the other end pin to the heater\u2019s hot (12 AWG both); neutrals and grounds go straight through, not switched. One end position: only the microwave is live; the other end: only the heater; middle: neither. 20 A is enough because only one load can run at a time (the microwave is 12.5 A, the heater 12 A). Before wiring, check the pins with a continuity tester: in the middle position no pin connects to another; in each end position the common beeps to one end pin only (if the middle pin is not the common, the one that beeps to both is). The terminals are 1/4 in (6.3 mm) tabs: crimp fully insulated female spade terminals for 12 to 10 AWG on the wires and slip a heat shrink boot over each, or mount the switch in a single gang plastic box, so no live terminal is bare; measure its panel cutout before you cut the plate. Turn the microwave off before you move the switch. Label it (microwave, off, heater). It sits beside the control panel so you choose before you cook or heat water; the heater only warms the tank while the switch is on its side'},
  {k:'run',   n:'Riser B: 120 V circuits and 12 V branches',   x:73, z0:8, z1:75, note:'down inside the wall behind the planks from the ceiling: 120 V in flexible conduit (12 AWG), the pump (14 AWG) and control panel (18 AWG) wires in a separate loom (each comes all the way from the hub fuse block, with its own fuse there); they go sideways behind the planks through notches in the furring'},
  {k:'sw',    n:'Light switch for the ceiling light over the countertop and the sink', x:100.25, z:52.25, note:'user: EP11 can be on the same plate as EP14, and make sure it is under the TV. One of two 12 V rockers on a small two-rocker plate (about 4 1/2 in wide and 2 1/2 tall, 99 to 103 1/2 in along and 51 to 53 1/2 up) on the wall strip under the TV (the TV is 76 1/2 to 103 1/2 and its bottom is at 54), just rear of the sink and above the dish towel hook (98 1/2, 50 up: the folded towel hangs 94 1/2 to 102 1/2, up to 51, so the plate clears it); this is the left rocker (EP14 is the right one). It switches only the ceiling light over the countertop and the sink (EP2). 16 AWG pair behind the covering to riser B (73), about 27 in away, then up to the ceiling. My placement on the strip, say if you want the two rockers the other way round'},
  ...(pl.lights.length > 3 ? [
    {k:'lt', n:'Ceiling light, center row, rear one (36 asked for)', x:pl.lights[2].x - 6, z:pl.ceilF - .5, note:'user: two more ceiling lights, 12 V, one at 36 centered and one around 100 centered. This one is centered across the van (' + fr(pl.lights[2].y) + ' in from the driver wall) and ' + fr(pl.lights[2].x) + ' in from the rear-door edge (asked for 36; it is kept 2 in clear of the roof rib at 37 7/8, so it moved 1/8 in), on the slat; on EP14, the right rocker of the plate under the TV'},
    {k:'lt', n:'Ceiling light, center row, cab-side one (around 100 asked for)', x:pl.lights[3].x - 6, z:pl.ceilF - .5, note:'the other center-row light, ' + fr(pl.lights[3].y) + ' in from the driver wall and ' + fr(pl.lights[3].x) + ' in from the rear-door edge (asked for around 100; the roof rib at 97 3/8 is 2 3/4 wide, so it sits 2 in clear of it, on the cab side), on the slat; on the same switch as the other center-row light'},
    {k:'sw', n:'Light switch for the two center-row ceiling lights', x:102.25, z:52.25, note:'user: the switch for these will be to the left of the sink on the wall, and EP11 is on the same plate (under the TV). The right rocker of the two-rocker plate (EP11 is the left one), 99 to 103 1/2 in along and 51 to 53 1/2 up, on the wall strip under the TV between the jar nook (ends at 94 3/4) and the sliding door opening (starts at 104), level with the outlet under the TV (96) and above the dish towel hook. The sink is at 103 to 123 and the opening starts at 104, so the strip is the only wall rear of the sink. 16 AWG pair behind the covering to riser B (73), about 28 in away, then up to the ceiling junction box'}
  ] : []),
]; };

// plumbing shown for reference, drawn as pipes and fixtures in slate with hexagon PL labels so it cannot be mistaken for the electrics (wires are drawn as coloured lines with round labels)
const PLUMB = pl => {
  const rz = 27.5;                                   // rz: the band between furring rails S3 (21 1/4) and S4 (30 1/4), inside the 2 in zone (23 1/4 to 29 1/2 up) and above the five oval slots at 25 1/3
  const rx = pl.valveX - 1.5, vz = pl.valveZ, sx = pl.pdrX;      // the lines rise at rx, between the blocks of S4 (at 17 3/4 and 31 1/4)
  const out = [
    {k:'phead', n:'Shower head', x:pl.headX, z:pl.headZ, lab:'H', note:fr(pl.headZ) + ' in up on a ' + fr(pl.headOut) + ' in arm pointing into the stall, on the cab side of the nook, around 30 in along the wall as you said (' + fr(pl.headX) + '), over the toilet end; the feed rises straight up from the valve at the head\'s own position'},
    {k:'pvalve', n:'Shower valve (mixer handle)', x:pl.valveX, z:pl.valveZ, lab:'V', note:'on the cab side of the shower nook, the left of it in the passenger-wall view (user: the plumbing is to the left of the nook, and the head and the valve are around 30 in along the wall; the nook is ' + fr(pl.snookEnd - (pl.sn ? pl.sn.x1 - pl.sn.x0 : 12)) + ' to ' + fr(pl.snookEnd) + ' in), under the head, ' + fr(vz) + ' in up, between furring rails S4 and S5, over the toilet end; the hot and cold lines come up beside it at ' + fr(rx) + ' in. The steel angle at the rear end stands 1 1/2 in off the body up to 36 3/4 (sloping down to 31 at 11 in), so about 3 in of room is left behind the covering'},
    {k:'ppump', n:'Water pump, under the sink beside the water heater', x0:104, x1:107, z0:12, z1:20, note:'user: the pump will fit somewhere closer to the water heater (it was at 119 to 122). On the inside of the sink cabinet\u2019s rear end panel (the heater, 87 1/4 to 101 1/4, is just beyond it), above the fresh tank (top at 10 in), about 3 in from the heater\u2019s fittings; reached through the sink cabinet\u2019s doors or hatch (my placement). Its 12 V feed (14 AWG, 10 A, from the fuse block) is the pump circuit on the one-line diagram'},
    {k:'ppath', two:true, n:'Hot and cold supply to the shower valve (two 1/2 in PEX lines)', pts:[[105.5, 20.5], [105.5, rz], [rx, rz], [rx, vz - 1.5]], at:[70, rz], note:'cold leaves the pump (now beside the heater, at 104 to 107) and rises inside the sink cabinet (from 104 on, the wall is the sliding door, so there is no cavity there: clip it inside the cabinet) to ' + fr(rz) + ' in up, then through the cabinet\u2019s rear end panel at 103 into the wall cavity behind the covering at ' + fr(rz) + ' in up: between furring rails S3 and S4 (the free band between the 3 1/2 in furring rails is 23 to 28 1/2 up), in the 2 in zone (23 1/4 to 29 1/2 up) where the steel is only 2 in off the body so there is about 2 1/2 in of room behind the covering, and above the five oval slots at 25 1/3 up. It crosses the pillar at about 98 and runs on behind the covering past the back of the fridge (there is no wall between the fridge and the shower now: its end is a curtain) to the rear end of the stall, then up at ' + fr(rx) + ' in, between the blocks of S4 (at 17 3/4 and 31 1/4), through S4 (drill it, do not notch) to the valve. The hot line branches off the hot water tank (87 1/4 to 101 1/4, fittings at its back) at about 94 and runs beside the cold one, 1 in apart; foam sleeve on the hot one, and insulation between both lines and the steel'},
    {k:'ppath', n:'Feed from the valve to the shower head', pts:[[pl.valveX, vz + 1.5], [pl.headX, vz + 1.5], [pl.headX, pl.headZ - 1.2]], at:[pl.headX, 52], note:'from the top of the valve straight up (the head is at the valve\'s own place), past S5, S6 and S7 (drill each, do not notch) in the gap between their blocks at 17 3/4 and 31 1/4, to the head; one mixed-water line'},
    {k:'pdrain', n:'Shower drain, through the floor to the grey water tank under the van', x:sx, z:.8, note:'a 1 1/2 in drain at the rear-door end of the pan (' + fr(sx) + ' in along, about ' + fr(pl.pdrY) + ' in out from the wall), the pan floor sloping to it; straight down through the floor, a shallow trap under it, then to the grey tank (30 x 17 x 8 space, position not set) with its vent. The tank has to be lower than the pan'},
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
    for (let t = 0; t < 6 && placed.some(q => Math.hypot(q[0] - bx, q[1] - by) < 26); t++) by += 14;
    placed.push([bx, by]);
    pg.push(`<polygon points="${bx-18},${by} ${bx-12},${by-9} ${bx+12},${by-9} ${bx+18},${by} ${bx+12},${by+9} ${bx-12},${by+9}" fill="${CPLF}" stroke="${CPL}" stroke-width="1.6"/><text x="${bx}" y="${by+3.8}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:${CPL}">${e.id}</text>`);
    const where = e.pts ? `from ${fr(e.pts[0][0])} in, ${fr(e.pts[0][1])} up, to ${fr(e.pts[e.pts.length - 1][0])} in, ${fr(e.pts[e.pts.length - 1][1])} up` : e.x0 != null ? `${fr(e.x0)} to ${fr(e.x1)}, ${fr(e.z0)} to ${fr(e.z1)} up` : `${fr(e.x)} in, ${fr(e.z)} up`;
    return `<tr><td><b class="pid">${e.id}</b></td><td>${esc(e.n)}</td><td>${where}</td><td class="kd">${esc(e.note)}</td></tr>`;
  });
  const svg = `<svg viewBox="0 0 1070 636" role="img" aria-label="${flip ? 'Passenger' : 'Driver'} wall: steel, furring rails, furniture outlines, the electrical items${plumb && plumb.length ? ' and the plumbing as pipes' : ''}">${base.inner}<g id="elec${side}">${o.join('')}</g>${pg.length ? `<g id="plumb${side}">${pg.join('')}</g>` : ''}</svg>`;
  const ptable = prow.length ? `<div id="plumbTable${side}"><h3 style="color:${CPL}">Plumbing on this wall (pipes with hexagon labels, for reference: not electrical)</h3><div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${prow.join('')}</tbody></table></div></div>` : '';
  return { svg, table: `<div class="tw"><table><thead><tr><th>#</th><th>Item</th><th>Where (in from the back mark, up from the floor)</th><th>Notes</th></tr></thead><tbody>${rows.join('')}</tbody></table></div>`, ptable, legend: base.legend };
}

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
  const RX = 79;                                   // the ceiling cables are drawn at 73 on the wall maps = 79 from the rear-door edge, in the bay between the ribs at 61 and 97; riser B climbs the passenger wall there, riser A the driver wall at 76 1/2 (82 1/2 from the rear-door edge, past the nook's front frame) and jogs 3 1/2 in at the ceiling
  const line = (pts, col, w, dash) => `<polyline points="${pts.map(p => X(p[0]) + ',' + Y(p[1])).join(' ')}" fill="none" stroke="${col}" stroke-width="${w}"${dash ? ` stroke-dasharray="${dash}"` : ''} stroke-linejoin="round"/>`;
  const acY = ac.y - ac.w / 2, fanY = fan.y - fan.w / 2;
  if (!G && !baseOnly) {
  o.push(line([[RX - 1.2, 0], [RX - 1.2, 68]], C12, 3));                              // the pump and control panel wires across (each its own wire from the fuse block)
  o.push(line([[RX + 1.2, 0], [RX + 1.2, 68]], C120, 3, '8 4'));                       // 120 V across
  o.push(line([[RX, 0], [RX, acY], [ac.x, acY]], CAC, 4.5));                           // A/C feed to the notch in the frame's driver-side wall
  o.push(line([[83.6, 0], [83.6, 20.5], [fan.x, 20.5], [fan.x, fanY]], C12, 2.4));    // fan feed, up riser A
  { const ys = [...new Set(d.lights.map(l => l.y))], aR = ac.x + ac.w / 2 + 1.5, aT = ac.y - ac.w / 2 - 1.5;
    ys.forEach(y => { const xs = d.lights.filter(l => l.y === y).map(l => l.x), x0 = Math.min(...xs), x1 = Math.max(...xs); if (xs.length < 2) return;
      // each row of ceiling lights runs along one slat; a row that crosses the A/C opening (it cuts that slat) goes round the opening, above it, in the gap between slats
      const cross = y > ac.y - ac.w / 2 && y < ac.y + ac.w / 2 && x0 < ac.x - ac.w / 2 && x1 > ac.x + ac.w / 2;
      o.push(line(cross ? [[x0, y], [x0, aT], [aR, aT], [aR, y], [x1, y]] : [[x0, y], [x1, y]], CLT, 2.2, '2 3')); }); }
  }
  o.push(`<rect x="${X(RX) - 11}" y="${Y(34) - 8}" width="22" height="16" rx="3" fill="#FFF1D6" stroke="${G ? INK : CAC}" stroke-width="2"/><text x="${X(RX)}" y="${Y(34) + 4}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${G ? INK : CAC}">JB</text>`);
  // the wet bath stall (36 along the wall, 24 out from the passenger wall; wall numbers + 6 from the rear-door edge)
  o.push(`<rect x="${X(6)}" y="${Y(44)}" width="${S * 36}" height="${S * 24}" fill="${G ? '#5F5E5A' : C12}" fill-opacity=".07" stroke="${G ? '#5F5E5A' : C12}" stroke-width="1.4" stroke-dasharray="5 3"/><text x="${X(6) + 6}" y="${Y(44) + 14}" style="font-size:11px;font-weight:700;fill:${G ? '#5F5E5A' : C12}">wet bath stall</text>`);
  // the soft LED strip around the ceiling edge: driver side, across the back, passenger side (about 31 ft in all, fed in three sections)
  { const e = 1.5, cabX = d.P.cab + 6;
    o.push(`<polyline points="${X(cabX)},${Y(e)} ${X(e)},${Y(e)} ${X(e)},${Y(68 - e)} ${X(cabX)},${Y(68 - e)}" fill="none" stroke="#F4C95D" stroke-width="9" stroke-opacity=".55" stroke-linejoin="round"/><polyline points="${X(cabX)},${Y(e)} ${X(e)},${Y(e)} ${X(e)},${Y(68 - e)} ${X(cabX)},${Y(68 - e)}" fill="none" stroke="#B8860B" stroke-width="1.6" stroke-linejoin="round"/>`);
    o.push(`<text x="${G ? X(16) : X(e) + 8}" y="${Y(e) + (G ? 38 : 20)}" style="font-size:10.5px;font-weight:700;fill:#8a6a00">soft LED strip around the edge</text>`); }
  // lights
  d.lights.forEach((l, i) => { const wet = l.y > d.P.vanW - d.panD && l.x < 6 + d.panW && l.x > 6; o.push(`<circle cx="${X(l.x)}" cy="${Y(l.y)}" r="${Math.max(6, S * d.P.lightD / 2)}" fill="#FFD84A" stroke="${wet && !G ? C12 : CLT}" stroke-width="${wet ? 3 : 1.8}"/>`); if (wet) o.push(`<text x="${X(l.x) + 12}" y="${Y(l.y) + 16}" style="font-size:10.5px;font-weight:700;fill:${G ? '#5F5E5A' : C12}">wet-rated (IP65)</text>`); });
  if (G) { const placed = [], wg = WR.filter(w => w.C).map(w => EW.wireGroup(w, 'C', X, Y, placed)); wg.forEach(g => o.push(g.l));
    o.push(`<rect x="${X(RX) - 11}" y="${Y(34) - 8}" width="22" height="16" rx="3" fill="#FFF1D6" stroke="${INK}" stroke-width="2"/><text x="${X(RX)}" y="${Y(34) + 4}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:${INK}">JB</text>`); wg.forEach(g => o.push(g.p)); WR.forEach(w => o.push(EW.traceLayer(w, 'C', X, Y))); }
  // where the risers meet the walls
  o.push(`<text x="${X(RX) + 16}" y="${Y(0) + 14}" style="font-size:11px;font-weight:700;fill:${INK}">riser A (A/C, 12 V) at ${RX + 3.5}</text><text x="${X(RX) + 16}" y="${Y(68) - 8}" style="font-size:11px;font-weight:700;fill:${INK}">riser B (120 V, branches) at ${RX}</text>`);
  // legend
  if (baseOnly) return o.join('');
  const ly = Y(68) + 66;
  if (G) {
    EW.AWG.forEach((a, i) => { const x = X(0) + Math.floor(i / 4) * 520, y = ly + (i % 4) * 18; o.push(`<line x1="${x}" y1="${y}" x2="${x + 36}" y2="${y}" stroke="${a.c}" stroke-width="${a.w}" stroke-linecap="round"/><text x="${x + 44}" y="${y + 4}" style="font-size:12px;fill:${INK}"><tspan style="font-weight:700">${a.name} AWG</tspan>, ${a.use}</text>`); });
    ['solid = 12 V; dashed = 120 V. The WR labels are the wires\u2019 numbers (the table below). JB = the ceiling junction box,', 'with the dimming controller (my placement). Grey bands = ribs; dashed squares = the roof units; yellow circles = the four ceiling', 'lights; the pale band = the soft LED strip. Riser A comes up at the top (driver wall), riser B at the bottom (passenger wall).'].forEach((t, i) => o.push(`<text x="${X(0)}" y="${ly + 88 + i * 16}" style="font-size:12px;fill:${INK}">${t}</text>`));
    return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ceiling seen from above: every wire coloured by gauge"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
  }
  const leg = [[C12, 'solid blue: 12 V wires (fan 14 AWG; pump and control panel)', null, 3], [C120, 'dashed red: 120 V circuits in flexible conduit (12 AWG)', '8 4', 3], [CAC, 'solid orange: A/C feed, 6 AWG, 100 A fuse at the battery', null, 4.5], [CLT, 'dotted yellow: the ceiling lights, one slat per row (16 AWG)', '2 3', 2.2], ['#F4C95D', 'pale yellow band: soft LED strip around the edge (14 AWG, its own 10 A circuit)', null, 7]];
  leg.forEach((l, i) => o.push(`<line x1="${X(0)}" y1="${ly + i * 16}" x2="${X(0) + 34}" y2="${ly + i * 16}" stroke="${l[0]}" stroke-width="${l[3]}"${l[2] ? ` stroke-dasharray="${l[2]}"` : ''}/><text x="${X(0) + 42}" y="${ly + i * 16 + 4}" style="font-size:12px;fill:${INK}">${l[1]}</text>`));
  o.push(`<text x="${X(86)}" y="${ly + 4}" style="font-size:12px;fill:${INK}">JB = ceiling junction box (dimming controller and the light splices)</text><text x="${X(86)}" y="${ly + 20}" style="font-size:12px;fill:${INK}">grey bands = ribs; dashed squares = the unit footprints on the roof</text><text x="${X(86)}" y="${ly + 36}" style="font-size:12px;fill:${INK}">yellow circles = the four ceiling lights (shower; countertop and sink;</text><text x="${X(86)}" y="${ly + 52}" style="font-size:12px;fill:${INK}">two in the center row; positions from the plan)</text><text x="${X(86)}" y="${ly + 68}" style="font-size:12px;fill:${INK}">the center row goes round the A/C opening, above it, in the gap between slats</text>`);
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Ceiling seen from above: lights, fan, A/C, junction box and wire runs"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
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
    ['Chassis ground for the hub board and the inverter', '4', 20, 3, 12.8, 'none', 'black 4 ft', 'one short strap from the − bus to the van body']];
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
  box(20, 120, 170, 58, 'Breaker B/D, 20 A', 'AC panel, 12 AWG hot', C120);
  o.push(`<rect x="300" y="70" width="200" height="160" rx="8" fill="#FFF1D6" stroke="${C120}" stroke-width="1.8"/>`);
  tx(312, 92, '30 A SPDT rocker (KCD3)', 'font-weight:700'); tx(312, 109, 'ON - OFF - ON, 3 pins', 'font-size:11px;fill:#5F5E5A');
  tx(312, 153, 'common', 'font-weight:700'); tx(312, 169, '(middle pin)', 'font-size:11px;fill:#5F5E5A');
  tx(402, 98 + 33, 'pin 1', 'font-size:11px'); tx(402, 192 + 3, 'pin 3', 'font-size:11px');
  pin(278, 149); pin(478, 128); pin(478, 192);
  ln(190, 149, 280, 149, C120); tx(196, 140, 'hot', 'font-size:11px;fill:' + C120);
  box(600, 90, 180, 58, 'Microwave outlet', '20 A receptacle, 12 AWG hot', C120);
  box(600, 172, 180, 58, 'Heater feed box', 'beside the tank, 12 AWG hot', C120);
  ln(500, 128, 600, 118, C120); ln(500, 192, 600, 200, C120);
  tx(520, 112, 'up', 'font-size:11px;fill:#5F5E5A'); tx(520, 222, 'down', 'font-size:11px;fill:#5F5E5A');
  ln(20, 268, 780, 268, '#5F5E5A', 2, '7 4'); tx(20, 260, 'neutral and ground: straight from the bus to both loads, not through the switch', 'font-size:11px;fill:#5F5E5A');
  tx(20, 292, 'Check the pins with a continuity tester first. Use fully insulated 12 to 10 AWG 1/4 in spade terminals', 'font-size:11px;fill:#5F5E5A');
  tx(20, 308, 'with heat shrink boots, or put the switch in a plastic box. Turn the microwave off before moving the switch.', 'font-size:11px;fill:#5F5E5A');
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Wiring of the heater or microwave selector: the breaker feeds the common pin, the two other pins go to the microwave outlet and the heater"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
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
  const br = [['A/C 12 V, up to 58 A', '6 AWG pair, 100 A fuse', CAC, '6', /^A\/C feed/], ['Fuse block: 4 ceiling, 4 cabinet lights', '16 AWG, 5 A', CLT, '16', /^Lights feed/], ['Soft LED strip, about 31 ft in 3 runs', '14 AWG, its own 10 A circuit', CLT, '14', /^Soft LED strip circuit/], ['Roof fan, up to 2.7 A', '14 AWG, 5 A', C12, '14', /^Roof fan/], ['Water pump, 7 A (under the sink)', '14 AWG, 10 A, own wire', C12, '14', /^Water pump/], ['Control panel and shunt display', '18 AWG, 3 A, own wire', C12, '18', /^Control panel/]];
  br.forEach((b, i) => { const y = 214 + i * 56; ln(460, 267, 540, 267, C12, i === 0 ? '10 AWG, 30 A fuse' : '', 500, 288, 0, '10', i === 0 ? id(/^12 V fuse block feed/) : '', 500, 259, id(/^12 V fuse block feed/)); ln(540, 267, 540, y + 20, C12, '', 0, 0, 0, '10', '', 0, 0, id(/^12 V fuse block feed/)); ln(540, y + 20, 600, y + 20, b[2], '', 0, 0, 2.8, b[3], id(b[4]), 570, y + 12); box(600, y, 330, 40, b[0], b[1], b[2]); });
  o.push(`<text x="600" y="198" style="font-size:12px;font-weight:700;fill:${C12}">12 V DC circuits (your 10-way blade fuse block, 5 of 10 ways used; not the A/C)</text>`);
  // AC side
  ln(470, 60, 600, 60, C120, '', 0, 0, 0, '10', id(/^Transfer switch to the AC panel/), 535, 76);
  box(600, 56, 150, 48, 'AC panel', '30 A main, GFCI', C120);
  o.push(`<text x="540" y="46" style="font-size:12px;font-weight:700;fill:${C120}">120 V AC circuits</text>`);
  [['A  counter outlets, GFCI', '15 A, 12 AWG'], ['B  microwave, its own', '15 A, 12 AWG'], ['C  fridge, TV, dinette outlets', '15 A, 12 AWG'], ['D  water heater 1440 W', '20 A, 12 AWG']].forEach((c, i) => { const y = 16 + i * 0; });
  const ac = [['A  couch, dinette, under-TV outlets (GFCI)', '15 A, 12 AWG'], ['B/D  microwave or water heater, via the selector', '20 A, 12 AWG, one at a time'], ['C  fridge, its own breaker', '15 A, 12 AWG']];
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
  const WR = EW.wiresFor(plan, Dlist, Plist, { ac: plan.ac, fan: plan.fan, lights: plan.lights });
  const wDw = EW.wallWires('D', Dlist, baseA, furn.D, WR, symbol, fr, esc, INK), wPw = EW.wallWires('P', Plist, baseD, furn.P, WR, symbol, fr, esc, INK);

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
  const key = `<p class="legend"><span><svg width="16" height="16" viewBox="0 0 16 16" style="display:inline;vertical-align:-3px;width:16px;min-width:0"><circle cx="8" cy="8" r="6.5" fill="#fff" stroke="${C120}" stroke-width="1.8"/></svg> 120 V outlet</span><span>S = switch</span><span style="color:${CPL};font-weight:600">grey pipes and fixtures with hexagon labels (PL) = plumbing, shown for reference: shower head, valve, pump, drain (hide it with the box above the drawing)</span><span>M = control panel</span><span>M/H = heater or microwave selector</span><span>IN = shore inlet</span><span style="color:#B8860B">yellow = lights and LED strips</span><span>orange boxes = mounted units</span><span>dashed boxes = furniture (for reference)</span><span style="color:${C12}">blue dashed</span> / <span style="color:${C120}">red dashed</span> = 12 V / 120 V runs</p>`;
  const body = `<div class="wrap">
  <h1>Electrical and lighting layout</h1>
  <p class="lead">A proposal for where the electrics go, drawn on the same steel and furring rails as the wall marking map, with the furniture outlined for reference. Positions are inches from the back mark (0 is 6 in in from the rear-door edge) and up from the floor; the ceiling plan uses inches from the rear-door edge. The steel and furring rails are the measured drawing; the electrical items are my proposal, so check each one against the real wall and tell me what to move.</p>
  <div class="note"><b>What you chose:</b> a 2000 W inverter, charging from the alternator and from shore power (no solar), a 120 V fridge, and the water pump under the sink. <b>What I assumed (tell me if wrong):</b>
  <ul><li>The battery is lithium, 280 Ah at 12.8 V (about 3.6 kWh), where the plan has it under the couch, 52 to 73 in.</li>
  <li><b>Your equipment:</b> a BELTTT 2000 W inverter (an inverter only: the listings show no charger and no transfer switch), a LiTime 60 A DC-DC charger from the alternator (2 AWG from the starter battery), and a VEVOR 80 A lithium shore charger. All three sit on one pull-out gear shelf over the battery under the couch (the shelf slides out into the aisle on two 18 in slides; every cable to it has a loop for that, see the cable table). Because the inverter has no transfer switch, the AC panel has a 30 A transfer switch that connects either shore power or the inverter, never both, and the shore charger is fed from the shore side only, on its own 15 A breaker (about 11 A at 120 V). With the charger running, a heater or microwave and the fridge could pass the 30 A shore inlet, so the charger is its own circuit and the total is worth watching.</li>
  <li><b>Ceiling lights:</b> four: one over the shower (wet rated) and one over the countertop and sink together, both on the slat at 58 in across, and two in the center row (36 and about 100 from the rear-door edge, centered across the van; each is kept 2 in clear of a rib, so they sit at 35 7/8 and 102 1/8), all 12 V and on a slat. The two in the center row share one switch on the passenger wall just rear of the sink. Everything else is lit from the cabinets, the jar nook and the soft LED strip.</li>
  <li><b>Your 12 V lights:</b> a 6 pack of recessed 12 V LED lights for RVs, boats and campers (3000 K warm white, CRI 90+, stepless dimming). The plan has eight 12 V lights (four in the ceiling and four under the cabinets), and you have bought enough of them to cover all eight. I have not seen the listing\u2019s numbers, so check these before you cut any hole: the cutout (hole) size and the depth behind the panel (the ceiling is 3/16 plywood plus a 3/4 slat; the cabinet bottoms are 3/4, and the cabinet is open above them); the watts each (I assumed 4 W); whether the dimming is built into the light (a touch ring or a press-and-hold) or needs a dimmer switch, because the rocker switches in this plan are plain on-off; and the IP rating, since the light over the shower has to be wet rated (IP65). Send me those numbers and I will change the plan to match.</li>
  <li><b>Your 12 V fuse block:</b> a 10-way blade fuse box with a blown-fuse LED on each way and a waterproof cover. The plan uses five of its ten ways, each with its own wire: 1 the lights (WR16, 5 A), 2 the soft LED strip (WR14, 10 A, with the dimming controller), 3 the roof fan (WR15, 5 A), 4 the water pump (WR31, 10 A), 5 the control panel (WR32, 3 A); ways 6 to 10 are spare (for example to give the ceiling lights and the cabinet lights a fuse each). It is fed by WR13, 10 AWG with a 30 A fuse at the bus. The A/C is not on it (its own 100 A fuse at the battery). I have not seen the listing, so check these before you buy fuses and mount it: that it takes standard ATC or ATO blade fuses (not mini); its rating for each way (most are 30 A, fine for these) and for the feed (most are 100 A in); that its input terminal takes a 10 AWG ring lug; and whether it has a negative bus bar (most have only the + side: then the five \u2212 wires go to the \u2212 bus bar next to it, not onto the block). Its wire terminals are screws or clamps for thicker wire than 18 AWG: use ferrules or ring lugs on the fine-strand copper wire.</li>
  <li><b>Your transfer switch:</b> a TS-30, 30 A. That name is the Go Power! model (an automatic switch with a shore input, a second input for a generator or here the inverter, and one output, locked so that only one input is connected; the listing says it prefers the generator input and waits 20 to 45 seconds before switching to it); other makers use the same name, so check the label. Shore goes to the shore input (WR7, 10 AWG), the inverter output goes to the other input (WR8), and the output goes to the AC panel (WR9, 10 AWG). Things to check in its manual: (1) the priority: if it prefers the second input, then whenever the inverter is on the loads come from the inverter, not shore, so switch the inverter off when you want shore power (the shore charger is fed from the shore side anyway); (2) whether it switches the neutral as well as the hot: this decides the one neutral-to-ground bond (see the note under the one-line diagram); (3) the wire size its terminals take (10 AWG is planned). Its size is listed as about 9 5/8 x 7 1/4 x 4 3/4 in: the hub board is drawn only 10 in tall (1 to 11 in up) and also has to hold the bus bars, the shunt, the Class T fuse, the fuse block and the AC panel, so it will not all fit as drawn: the hub board needs a layout with the real sizes.</li>
  <li><b>Light switches:</b> at the rear doors (the shower light, and the rear one of the two lights under the cabinet over the couch; the roof fan has no switch), right next to the cab-end one of the two lights over the couch (its own), on the dinette\u2019s back wall W2, between the dinette and the driver\u2019s seat (only the two lights under the cabinet over the seats), a two-rocker 12 V plate on the passenger wall under the TV, just rear of the sink (EP11, the left rocker, for the ceiling light over the countertop and the sink, and EP14, the right one, for the two center-row ceiling lights), and the dimmer for the soft strip. Each switch runs its own group, so ordinary 12 V rated switches work: no push buttons or controller are needed.</li>
  <li><b>Under-cabinet lights:</b> one in the middle of the couch, and two over the dinette, each centered over its bench seat and then moved 6 in toward the table, all on the underside of the wall cabinets. They replace the under-cabinet LED strips, the wall reading lights and the single light over the table I had first suggested.</li>
  <li><b>Soft LED lighting:</b> one warm white dimmable strip around the ceiling edge, along the driver side, across the back and along the passenger side (154 + 68 + 154 = 376 in, about 31 ft), in three runs fed separately so none is longer than about 13 ft from its feed. The strip you found (BTF-LIGHTING FCOB, 336 LEDs/m, 8 mm wide) is 8 W/m, so the 9.55 m is about 76 W (6.4 A) at full: it has its own 10 A circuit on 14 AWG, with plenty of margin. Buy three 5 m (16.4 ft) reels: two (32.8 ft) would cover the 31.3 ft only with soldered joins and about 1 1/2 ft to spare, and the spare third reel lights something else. One switch with a dimmer next to the couch outlet.</li>
  <li><b>Outlets:</b> the four 120 V outlets you asked for (couch, over the middle of the dinette table, under the TV, behind the fridge), plus one for the microwave, which cannot share a circuit with them. Everything else is 12 V: the lights, the fan, the pump and the control panel. There are no USB-C or 12 V sockets (you said they are not needed); phones charge from the 120 V outlets.</li>
  <li><b>Wet bath:</b> a wet-rated (IP65) ceiling light over the stall (the exact center is under a rib, so it sits 2 1/2 in toward the cab), and no outlet in the stall (you said no outlet there). The light is at the center of the stall (18 in along the wall, 56 in across from the driver wall). That point falls in the 1 in gap between two slats, so mount the light on a short cross block laid across the gap, or on the nearest slat 2 in to one side. It is one of the four ceiling lights.</li>
  <li>The hot water heater (1440 W) and the microwave (about 1500 W) must not run together: that is more than a 2000 W inverter can supply. Your 30 A SPDT rocker (KCD3, ON-OFF-ON: microwave, off, heater) on one shared 20 A breaker makes it impossible: see item ${selId} on the passenger wall.</li>
  <li>All 120 V work is for an electrician to check; I give layout and sizes, not a code review.</li></ul></div>
  <h2>1. One-line diagram</h2>
  <div class="figwrap">${oneLineSVG()}</div>
  <h3>The heater or microwave selector, wired (your 30 A SPDT rocker)</h3>
  <div class="figwrap">${selectorSVG()}</div>
  <h2>1a. High-current cables and fuses to buy</h2>
  ${cableTable()}
  <h2>2. Driver side wall</h2>
  ${tog('elecD', 'furr', 'Show the electrical items')}
  <div class="figwrap">${Dw.svg}</div>
  ${key}${Dw.table}
  <h2>3. Passenger side wall</h2>
  ${tog('elecP', 'furrP', 'Show the electrical items', 'P')}
  <div class="figwrap">${Pw.svg}</div>
  ${key}${Pw.table}${Pw.ptable}
  <h2>4. Ceiling: lights, fan, A/C and the wire runs</h2>
  <p class="lead">Four ceiling lights in two rows (positions from the plan): the shower light and the countertop and sink light on one slat, the two center-row lights on another, so each row is on its own slat. The soft LED strip runs round the edge. Risers A and B stand at 79 in from the rear-door edge (73 on the wall maps), in the bay between the ribs at 61 and 97. Every rib the cables cross needs a grommeted hole: use any factory holes first, and keep to the web of the rib, not the flange.</p>
  <div class="figwrap">${ceilingSVG(plan)}</div>
  <div id="wsec">
  <h2>5. All the wires, colored by gauge</h2>
  <p class="lead wlead">Every wire in the van, drawn on the same steel and furring rails (faint) and the same items as the sections above. The colour and the thickness show the gauge (AWG, the bigger the number the thinner the wire); the key sets which ones to show. The routes are my proposal, drawn between the items already on this page, straight along the free bands between the furring rails and up the two risers: the real path follows the notches and grommets. The sizes and fuses are the ones in the one-line diagram and the cable table; the few places where I chose a size are marked in the wire list. <b>To follow one wire from where it starts to where it goes, use the wire box just below the key, or open <a href="wires.html">Wire by wire</a>: one diagram for each wire, from the power to its end.</b></p>
  <div class="wkey">${EW.keyHTML(WR)}</div>
  <div class="wtrace" id="wtrace">
    <div class="wt-row"><button type="button" onclick="wtStep(-1)">\u25C0 Previous</button><select id="wtSel" onchange="wtr(this.value)" aria-label="Pick one wire"><option value="">All wires</option>${WR.map(w => `<option value="${w.id}">${w.id} \u00B7 ${EW.byG[w.g].name} AWG \u00B7 ${esc(w.n.length > 72 ? w.n.slice(0, 70) + '\u2026' : w.n)}</option>`).join('')}</select><button type="button" onclick="wtStep(1)">Next \u25B6</button><button type="button" onclick="wtr('')">Show all wires</button></div>
    <div class="wt-card" id="wtCard">All the wires are showing. Pick one (or press Next) and only that wire stays: a green START mark where it begins, a black END mark where it ends, and arrows along the way. The drawings that do not have it are hidden.</div>
  </div>
  <div class="wview" data-title="the one-line diagram" data-nozoom="1"><h3>5a. One-line diagram, by gauge</h3>
  <div class="figwrap">${oneLineSVG(WR)}</div></div>
  <div class="wview" data-title="the driver side wall"><h3>5b. Driver side wall</h3>
  <div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('wbaseD').style.display=this.checked?'':'none'"> Show the steel, furring rails and furniture (faint)</label></div>
  <div class="figwrap">${wDw}</div></div>
  <div class="wview" data-title="the passenger side wall"><h3>5c. Passenger side wall</h3>
  <div class="tog"><label><input type="checkbox" checked onchange="document.getElementById('wbaseP').style.display=this.checked?'':'none'"> Show the steel, furring rails and furniture (faint)</label></div>
  <div class="figwrap">${wPw}</div></div>
  <div class="wview" data-title="the ceiling"><h3>5d. Ceiling</h3>
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
  </script>
  <h2>6. What it adds up to</h2>
  ${loadTable(plan)}
  <h2>7. Order of work</h2>
  <div class="note"><ul>
  <li>Before the walls and ceiling are covered: run the risers, the cables across the ceiling and every branch, with grommets in all steel and the 12 V and 120 V in separate looms (at least 2 in apart, crossing at right angles). This is the rough-in step of the build order.</li>
  <li>With the furring rails: fix the electrical boxes to blocking between the furring rails, and add the blocking behind the hub board, the switch plates and the outlets before the planks go on.</li>
  <li>Last: the hub board and fuses, the inverter and the two chargers, the transfer switch, the lights and the plates, after the covering is up.</li>
  <li>Test every circuit with a meter before you connect the battery, and test the GFCI outlets with the button.</li></ul></div>
  <p class="lead" style="margin-top:14px"><a href="interactive.html">Back to the interactive plan</a> &middot; <a href="wall-map.html">Wall marking map</a></p>
  </div>`;
  // ---- wires.html: one diagram for each wire (power chain and the whole run), sharing one copy of the wall and ceiling base through <use>
  { const EC = require('./elcards.js');
    const LD = EW.wallLayers('D', Dlist, baseA, furn.D, symbol, esc, INK), LP = EW.wallLayers('P', Plist, baseD, furn.P, symbol, esc, INK);
    const noDefs = t => t.replace(/<defs>[\s\S]*?<\/defs>/g, ''), defs = (baseA.inner.match(/<defs>[\s\S]*?<\/defs>/g) || []).join('') + (baseD.inner.match(/<defs>[\s\S]*?<\/defs>/g) || []).join('');
    const hidden = `<svg width="0" height="0" style="position:absolute;width:0;height:0;overflow:hidden" aria-hidden="true">${defs}<g id="bD">${noDefs(LD.inner)}</g><g id="fD">${LD.fu}${LD.bigs.join('')}${LD.pump}${LD.stub}${LD.smalls.join('')}${LD.call}</g><g id="bP">${noDefs(LP.inner)}</g><g id="fP">${LP.fu}${LP.bigs.join('')}${LP.pump}${LP.stub}${LP.smalls.join('')}${LP.call}</g><g id="bC">${ceilingSVG(plan, null, true)}</g></svg>`;
    const ctx = { D: { X: LD.X, Y: LD.Y, H: 636, name: 'driver wall', use: '<use href="#bD" opacity=".33"/><use href="#fD"/>' }, P: { X: LP.X, Y: LP.Y, H: 636, name: 'passenger wall', use: '<use href="#bP" opacity=".33"/><use href="#fP"/>' }, C: { X: x => 50 + 6 * x, Y: y => 56 + 6 * y, H: 500, name: 'ceiling', use: '<use href="#bC"/>' } };
    const { index, cards } = EC.cardsPage(WR, ctx);
    const wstyle = style + `
  .wcard { border-top: 3px solid #1b1a17; margin-top: 30px; padding-top: 6px; }
  .wcard h3 { font-size: 18px; margin: 6px 0 6px; } .wcard h4 { font-size: 14px; margin: 12px 0 2px; color: #3d3b34; } .wcard h4 .kd { font-weight: 400; }
  .wc-h { font-size: 15px; } .wc-l { margin: 3px 0; font-size: 14.5px; }
  .wt-s, .wt-e { display: inline-block; font-size: 11px; font-weight: 700; color: #fff; border-radius: 9px; padding: 1px 8px; margin-right: 8px; letter-spacing: .4px; } .wt-s { background: #1B7F3B; } .wt-e { background: #111; }
  b.wid { color: #1b1a17; white-space: nowrap; background: #fff; border: 1.5px solid #8a8a84; border-radius: 9px; padding: 0 6px; }`;
    const wbody = `<div class="wrap">
  <h1>Wire by wire</h1>
  <p class="lead">One diagram for each of the ${WR.length} wires on the <a href="electric.html">electrical layout page</a>. Each starts with the chain from the power (the battery, the shore power inlet or the starter battery) through the fuses to the end of the wire, with the wire numbers on the arrows and this wire highlighted; then its whole run on the wall and the ceiling drawings, zoomed in, from the green START mark to the black END mark, with arrows showing the direction. Colour and thickness are the gauge, as on the electrical page (a solid line is 12 V or battery cable, a dashed line is 120 V). The routes are my proposal, drawn straight along the free bands between the furring rails and up the two risers, not measured paths.</p>
  ${index}
  ${cards}
  <p class="lead" style="margin-top:14px"><a href="electric.html">Back to the electrical layout</a> &middot; <a href="interactive.html">The interactive plan</a></p>
  </div>`;
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
