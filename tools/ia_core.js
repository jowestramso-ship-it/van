'use strict';
/* ================= sizes ================= */
// k = key, g = group, l = label, d = default, s = step, a/b = min/max, t = type (n number, c checkbox, s select)
const PD = [
  { k: 'cab', g: 'Van', l: 'Cab wall, from the back', d: 154, s: .5, a: 100, b: 200 },
  { k: 'vanW', g: 'Van', l: 'Inside width', d: 68, s: .5, a: 50, b: 90 },
  { k: 'ceil', g: 'Van', l: 'Ceiling height at the wall (bare, to the rib)', d: 75.5, s: .5, a: 60, b: 90 },
  { k: 'numLbl', g: 'Take items out', l: 'Number the items in the side views and list their names and sizes under the drawing (untick to write them on the drawing)', d: true, t: 'c' },
  { k: 'showerOn', g: 'Take items out', l: 'Shower head and valve in the wet bath', d: true, t: 'c' },
  { k: 'microOn', g: 'Take items out', l: 'Microwave and its shelf (untick to take it out of the diagram and the checks)', d: true, t: 'c' },
  { k: 'tvOn', g: 'Take items out', l: 'TV over the nook', d: true, t: 'c' },
  { k: 'towelOn', g: 'Take items out', l: 'Paper towel roll in its recess in the angled front', d: true, t: 'c' },
  { k: 'fridgeOn', g: 'Take items out', l: 'Fridge and its platform (the space it leaves stays empty; the cabinet still starts where the fridge ends)', d: true, t: 'c' },
  { k: 'nookOn', g: 'Take items out', l: 'Jar shelf and the quart jars in the nook (the nook recess itself stays)', d: true, t: 'c' },
  { k: 'drawersOn', g: 'Take items out', l: 'Drawers and shelves under the counter (all of them, with the rail)', d: true, t: 'c' },
  { k: 'battOn', g: 'Take items out', l: 'Battery under the couch', d: true, t: 'c' },
  { k: 'closetOn', g: 'Take items out', l: 'Closet and its doors (the space it leaves stays empty; the dinette still starts where the closet ends)', d: true, t: 'c' },
  { k: 'toiletOn', g: 'Take items out', l: 'Toilet in the wet bath: the Reliance Fold-To-Go, left set up in the stall (at the cab end, sideways, its back against the wall to the fridge)', d: true, t: 'c' },
  { k: 'snItemsOn', g: 'Take items out', l: 'Towel bar, toilet paper and bottles in the shower nook', d: true, t: 'c' },
  { k: 'winOn', g: 'Take items out', l: 'Side window over the dinette (Van Windows Direct TL201-SE, driver side forward slider)', d: true, t: 'c' },
  { k: 'gearOn', g: 'Take items out', l: 'Charging gear on a pull-out shelf over the battery under the couch: the BELTTT inverter, the LiTime DC-DC charger and the VEVOR shore charger', d: true, t: 'c' },
  { k: 'gcabOn', g: 'Take items out', l: 'Gear cabinet under the east end of the couch (floor-mounted, two side panels, the shelf is its sliding top) and the removable couch frame with its wall blocks', d: true, t: 'c' },
  { k: 'blkBOn', g: 'Take items out', l: 'The middle wall block for the couch frame (20 in; you said "maybe, if needed")', d: true, t: 'c' },
  { k: 'wallsOn', g: 'Take items out', l: 'Floor-to-ceiling walls: behind the dinette backs (at the closet end and behind the driver seat) and one on each side of the fridge', d: true, t: 'c' },
  { k: 'bedLen', g: 'Bed / couch', l: 'Length', d: 74, s: .5, a: 40, b: 120 },
  { k: 'bedD', g: 'Bed / couch', l: 'Depth, closed (the couch on its base)', d: 26, s: .5, a: 15, b: 40 },
  { k: 'bedBack', g: 'Bed / couch', l: 'Leaf width (flips out in front; = back cushion length)', d: 20, s: .5, a: 0, b: 40 },
  { k: 'platform', g: 'Bed / couch', l: 'Seat base (deck 3/4 in lower; the leaf folds onto it). Raised from 14 to 17 1/2 for the gear shelf, then to 18 1/2 so a 3/4 x 1 rail can run along the deck front over the cabinet', d: 18.5, s: .5, a: 6, b: 30 },
  { k: 'mattress', g: 'Bed / couch', l: 'Seat and back cushion thickness (5 since the couch was raised 3 1/2 in, to keep a seated head under the wall cabinets)', d: 5, s: .5, a: 2, b: 12 },
  { k: 'legIn', g: 'Bed / couch', l: 'Legs set in from the leaf free edge', d: 3, s: .5, a: 0, b: 10 },
  { k: 'closetW', g: 'Closet', l: 'Width', d: 15, s: .25, a: 8, b: 40 },
  { k: 'closetD', g: 'Closet', l: 'Depth', d: 25, s: .5, a: 10, b: 40 },
  { k: 'rodHi', g: 'Closet', l: 'Rod for the hanging clothes, up from floor', d: 71, s: .5, a: 40, b: 85 },
  { k: 'cloLen', g: 'Closet', l: 'Hanging clothes: length of the longest garment (the drawers are under them)', d: 36, s: .5, a: 20, b: 60 },
  { k: 'hangDrop', g: 'Closet', l: 'Hanger: from the rod down to the shoulder of the garment', d: 3.5, s: .25, a: 1, b: 6 },
  { k: 'cloClear', g: 'Closet', l: 'Clear space between the bottom of the longest garment and the top of the drawers', d: 1, s: .25, a: 0, b: 6 },
  { k: 'cloDrawN', g: 'Closet', l: 'Drawers under the hanging clothes: how many', d: 4, s: 1, a: 1, b: 8 },
  { k: 'cloDrawD', g: 'Closet', l: 'Drawers: depth (the slide length; they pull out about 1 in less than this)', d: 22, s: 2, a: 10, b: 24 },
  { k: 'hinge', g: 'Closet', l: 'Door hinges on the', d: 'rear', t: 's', o: [['rear', 'bed side'], ['cab', 'dinette side']] },
  { k: 'openAng', g: 'Closet', l: 'Doors open to (degrees)', d: 90, s: 5, a: 30, b: 180 },
  { k: 'invL', g: 'Charging gear', l: 'Inverter (BELTTT 2000 W): length, along the wall (14.8 x 7.7 x 3.9 from its listing; measure yours)', d: 14.8, s: .1, a: 6, b: 24 },
  { k: 'invW', g: 'Charging gear', l: 'Inverter: width, out from the wall', d: 7.7, s: .1, a: 4, b: 16 },
  { k: 'invH', g: 'Charging gear', l: 'Inverter: height off the floor', d: 3.9, s: .1, a: 2, b: 10 },
  { k: 'dcL', g: 'Charging gear', l: 'DC-DC charger (LiTime 60 A): length, along the wall (you measured 16 x 9 x 4.5)', d: 16, s: .1, a: 6, b: 20 },
  { k: 'dcW', g: 'Charging gear', l: 'DC-DC charger: width, out from the wall', d: 9, s: .1, a: 4, b: 14 },
  { k: 'dcH', g: 'Charging gear', l: 'DC-DC charger: height off the floor', d: 4.5, s: .1, a: 2, b: 10 },
  { k: 'chL', g: 'Charging gear', l: 'Shore charger (VEVOR 80 A): length, along the wall (you measured 9.5 x 4 x 7: 9.5 long, 7 wide, 4 thick)', d: 9.5, s: .1, a: 4, b: 20 },
  { k: 'chW', g: 'Charging gear', l: 'Shore charger: width, out from the wall', d: 7, s: .1, a: 3, b: 14 },
  { k: 'chH', g: 'Charging gear', l: 'Shore charger: height off the floor (its thickness)', d: 4, s: .1, a: 2, b: 10 },
  { k: 'shG', g: 'Charging gear', l: 'Gear shelf: gap from the battery top (9 1/2 up) to the underside of the shelf, for the terminals, lugs and cable bends', d: 1, s: .25, a: .5, b: 4 },
  { k: 'shT', g: 'Charging gear', l: 'Gear shelf: thickness of the plywood tray', d: .5, s: .125, a: .25, b: 1 },
  { k: 'winX', g: 'Side window', l: 'Window cutout (the slider frame): left edge, from the back (centered over the table at 101 3/4)', d: 101.75, s: .25, a: 60, b: 150 },
  { k: 'winZ', g: 'Side window', l: 'Window cutout: bottom edge (the sill), up from the floor', d: 39, s: .25, a: 25, b: 70 },
  { k: 'winCW', g: 'Side window', l: 'Window cutout: width (from your tape readings: 39 11/16)', d: 39.6875, s: .0625, a: 30, b: 50 },
  { k: 'winCH', g: 'Side window', l: 'Window cutout: height (22 5/8)', d: 22.625, s: .0625, a: 15, b: 30 },
  { k: 'winGW', g: 'Side window', l: 'Window glass, overall: width (54.35 on the listing; it is glued on the outside, over the stamping)', d: 54.35, s: .05, a: 40, b: 70 },
  { k: 'winGH', g: 'Side window', l: 'Window glass, overall: height (29.12)', d: 29.12, s: .05, a: 20, b: 40 },
  { k: 'winOL', g: 'Side window', l: 'Glass edge to cutout: the glass starts this far left of the cutout (9 11/16)', d: 9.6875, s: .0625, a: 0, b: 20 },
  { k: 'winOB', g: 'Side window', l: 'Glass edge to cutout: the glass starts this far below the cutout (2 3/4)', d: 2.75, s: .125, a: 0, b: 8 },
  { k: 'blkA', g: 'Couch frame blocks', l: 'Wall block at the back end: its center, along the wall from the back mark (you said 3)', d: 3, s: .25, a: 1.5, b: 70 },
  { k: 'blkB', g: 'Couch frame blocks', l: 'Wall block in the middle (you said 20, if needed)', d: 20, s: .25, a: 1.5, b: 70 },
  { k: 'blkC', g: 'Couch frame blocks', l: 'Wall block at the cabinet end (you said 41)', d: 41, s: .25, a: 1.5, b: 70 },
  { k: 'shPull', g: 'Charging gear', l: 'Gear shelf: how far it pulls out (18 in full-extension slides; the shelf is 17 1/2 deep)', d: 18, s: 1, a: 10, b: 40 },
  { k: 'fwT', g: 'Floor-to-ceiling walls', l: 'Wall thickness (the walls are inside the closet, the shower and the counter cabinet, so nothing else moves)', d: .75, s: .125, a: .25, b: 3 },
  { k: 'benchLen', g: 'Dinette', l: 'Bench length', d: 19.5, s: .5, a: 10, b: 40 },
  { k: 'benchD', g: 'Dinette', l: 'Bench depth', d: 28, s: .5, a: 15, b: 45 },
  { k: 'seatH', g: 'Dinette', l: 'Seat height', d: 17.5, s: .5, a: 10, b: 26 },
  { k: 'backH', g: 'Dinette', l: 'Backrest top', d: 38, s: .5, a: 20, b: 50 },
  { k: 'pillowT', g: 'Dinette', l: 'Backrest cushion thickness (lies on the lowered table)', d: 2.9, s: .1, a: 1, b: 8 },
  { k: 'tableAuto', g: 'Dinette', l: 'Table fills the space between the benches', d: true, t: 'c', f: 'tableLen' },
  { k: 'tableLen', g: 'Dinette', l: 'Table length', d: 26, s: .5, a: 10, b: 70 },
  { k: 'tableD', g: 'Dinette', l: 'Table depth', d: 28, s: .5, a: 10, b: 45 },
  { k: 'tableH', g: 'Dinette', l: 'Table height', d: 29, s: .5, a: 20, b: 40 },
  { k: 'cabBot', g: 'Wall cabinets', l: 'Bottom, up from floor (63 since they were raised 2 in; the top stays at the finished ceiling, so they are 2 in shorter)', d: 63, s: .5, a: 40, b: 80 },
  { k: 'cabBackIn', g: 'Wall cabinets', l: 'Set a solid back of the cabinets in from the wall (0 = open backs: the sides are cut to follow the leaning wall)', d: 0, s: .5, a: 0, b: 8 },
  { k: 'cabDepth', g: 'Wall cabinets', l: 'Depth', d: 14, s: .5, a: 6, b: 24 },
  { k: 'doorH', g: 'Wall cabinets', l: 'Door height (3 doors a side, widths follow the cabinet; 10 now the cabinets are 2 in shorter)', d: 10, s: .5, a: 6, b: 24 },
  { k: 'panW', g: 'Passenger side', l: 'Shower pan length', d: 36, s: .5, a: 20, b: 50 },
  { k: 'panD', g: 'Passenger side', l: 'Shower pan depth', d: 24, s: .5, a: 16, b: 36 },
  { k: 'snookLen', g: 'Passenger side', l: 'Shower nook length along the wall (it ends at 29 3/4 on the cab side; a shorter nook comes off the rear end)', d: 17.25, s: .25, a: 6, b: 23.75 },
  { k: 'snookH', g: 'Passenger side', l: 'Shower nook height (the recess in the shower wall)', d: 16, s: .5, a: 6, b: 40 },
  { k: 'snookTop', g: 'Passenger side', l: 'Shower nook top, up from the floor (54 is level with the top of the jar nook and the bottom of the TV)', d: 54, s: .5, a: 20, b: 70 },
  { k: 'nookLen', g: 'Passenger side', l: 'Jar nook length along the wall (the nook ends at 93 1/4 on the cab side; a shorter nook comes off the rear end)', d: 17.25, s: .25, a: 6, b: 35.25 },
  { k: 'jarW', g: 'Passenger side', l: 'Jar width, center to center along the shelf (quart jars 3 3/4)', d: 3.75, s: .25, a: 2, b: 6 },
  { k: 'nookH', g: 'Passenger side', l: 'Jar nook height above the countertop (16 puts its top level with the bottom of the TV)', d: 16, s: .5, a: 8, b: 24 },
  { k: 'headX', g: 'Passenger side', l: 'Shower head: along the wall, from the back (the stall is 0 to the shower pan length; it is toward the rear, and the valve is at the cab end where the hot and cold lines arrive)', d: 9, s: .5, a: 1, b: 35 },
  { k: 'headZ', g: 'Passenger side', l: 'Shower head: height up from the floor (the finished ceiling at the wall is about 74 1/2)', d: 70, s: .5, a: 50, b: 74 },
  { k: 'headOut', g: 'Passenger side', l: 'Shower head: how far it sticks out from the wall on its arm', d: 6, s: .5, a: 2, b: 14 },
  { k: 'valveX', g: 'Passenger side', l: 'Shower valve (mixer handle): along the wall, from the back', d: 33, s: .5, a: 1, b: 35 },
  { k: 'valveZ', g: 'Passenger side', l: 'Shower valve: height up from the floor (the pan is fixed, with a 3 in curb)', d: 44, s: .5, a: 26, b: 60 },
  { k: 'toiletW', g: 'Toilet', l: 'Toilet: width, side to side (Reliance Fold-To-Go 14 1/2)', d: 14.5, s: .5, a: 10, b: 24 },
  { k: 'toiletD', g: 'Toilet', l: 'Toilet: depth, front to back (it sits sideways, so this runs along the wall; Fold-To-Go 14 1/2)', d: 14.5, s: .5, a: 10, b: 26 },
  { k: 'toiletH', g: 'Toilet', l: 'Toilet: height of the top of the seat (Fold-To-Go about 14 1/2, low)', d: 14.5, s: .25, a: 10, b: 24 },
  { k: 'tbarBay', g: 'Shower nook contents', l: 'Towel bar bay: width from the rear end of the nook (the rest of the nook holds the toilet paper and the bottles)', d: 6, s: .25, a: 3, b: 12 },
  { k: 'tbarDrop', g: 'Shower nook contents', l: 'Towel bar: how far below the top of the nook', d: 3.5, s: .25, a: 1, b: 8 },
  { k: 'snCord', g: 'Shower nook contents', l: 'Bungee cord across the nook front: height above the shelf board (0 for none; it keeps the bottles from falling out)', d: 5.5, s: .25, a: 0, b: 9 },
  { k: 'snShelf', g: 'Shower nook contents', l: 'Shelf board: its top, up from the floor (toilet paper under it, bottles on it)', d: 43.75, s: .25, a: 38, b: 54 },
  { k: 'snookLip', g: 'Passenger side', l: 'Shower nook front lip (0 for none: a bungee cord across the front keeps things in instead)', d: 0, s: .25, a: 0, b: 4 },
  { k: 'fridgeW', g: 'Passenger side', l: 'Fridge width', d: 22, s: .5, a: 14, b: 30 },
  { k: 'fridgeD', g: 'Passenger side', l: 'Fridge depth', d: 19, s: .5, a: 12, b: 26 },
  { k: 'fridgeH', g: 'Passenger side', l: 'Fridge height', d: 48, s: .5, a: 20, b: 66 },
  { k: 'counterH', g: 'Passenger side', l: 'Counter height', d: 38, s: .5, a: 30, b: 44 },
  { k: 'cabD', g: 'Passenger side', l: 'Cabinet depth', d: 21, s: .5, a: 12, b: 30 },
  { k: 'flatLen', g: 'Passenger side', l: 'Straight part of the cabinet', d: 30, s: .5, a: 10, b: 70 },
  { k: 'sinkD', g: 'Passenger side', l: 'Depth at the sink end (includes the 3/4 in door)', d: 17, s: .5, a: 10, b: 24 },
  { k: 'angLen', g: 'Passenger side', l: 'Length of the angled part of the counter front', d: 15, s: .5, a: 3, b: 40 },
  { k: 'sinkW', g: 'Passenger side', l: 'Sink cabinet width', d: 20, s: .5, a: 12, b: 40 },
  { k: 'sinkBowlD', g: 'Passenger side', l: 'Sink depth: from the countertop down to the underside of the sink, drain included (a guess until the sink is chosen)', d: 7.5, s: .25, a: 2, b: 14 },
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
  { k: 'tankLen', g: 'Water tanks', l: 'Fresh water tank length (35 leaves the cab-side column under the counter, 73 3/4 to 86 3/4 in, free for the trash can; 41 reaches back to 81 1/4)', d: 35, s: .5, a: 10, b: 70 },
  { k: 'tankD', g: 'Water tanks', l: 'Fresh water tank depth (out from the wall)', d: 16, s: .5, a: 4, b: 20 },
  { k: 'tankH', g: 'Water tanks', l: 'Fresh water tank height', d: 10, s: .5, a: 6, b: 24 },
  { k: 'hotGap', g: 'Water tanks', l: 'Clear space each side of the hot water tank', d: 6, s: .5, a: 0, b: 20 },
  { k: 'hotGal', g: 'Water tanks', l: 'Hot water tank: how much water it holds (gallons; 3.96 gal is 15 liters; its 14 x 14 x 13 in size is the outside of the heater)', d: 3.96, s: .1, a: 1, b: 20 },
  { k: 'hotEmptyLb', g: 'Water tanks', l: 'Heater weight: the hot water tank empty (lb)', d: 2, s: .5, a: 0, b: 60 },
  { k: 'hotX0', g: 'Water tanks', l: 'Hot water tank: where it starts along the wall when it sits on the fresh tank or is placed by hand (from the back; you can drag it)', d: 87.25, s: .5, a: 0, b: 140 },
  { k: 'hotFree', g: 'Water tanks', l: 'Hot water tank: place it by hand at any height and spot (dragging it turns this on; turn it off to go back to the floor or shelf spots)', d: false, t: 'c' },
  { k: 'hotShelf', g: 'Water tanks', l: 'Hot water tank bottom, up from the floor (0 = on the floor; 7.5 = on a shelf over the wheel well; 16.75 = on a shelf over the fresh tank, 10.75 rests it right on the 10 in tank, since the shelf is 3/4 in thick)', d: 16.75, s: .5, a: 0, b: 30 },
  { k: 'hotW', g: 'Water tanks', l: 'Hot water tank length along the wall', d: 14, s: .5, a: 6, b: 18 },
  { k: 'hotBack', g: 'Water tanks', l: 'Hot water tank: space behind it for the hot and cold fittings and the relief valve (they are at the back)', d: 1.625, s: .125, a: 0, b: 24 },
  { k: 'tankShift', g: 'Water tanks', l: 'Fresh water tank: moved toward the rear from the sink end (negative = toward the cab; you can drag it)', d: 0, s: .5, a: -40, b: 50 },
  { k: 'tankLift', g: 'Water tanks', l: 'Fresh water tank: lifted off the floor (you can drag it)', d: 0, s: .25, a: 0, b: 40 },
  { k: 'tankBack', g: 'Water tanks', l: 'Fresh water tank: space between it and the wall (you can drag it)', d: 0, s: .25, a: 0, b: 24 },
  { k: 'jugOn', g: 'Take items out', l: 'Draw the drain jug (the sink drains into it; it stands on the fresh water tank under the sink)', d: true, t: 'c' },
  { k: 'jugH', g: 'Water tanks', l: 'Drain jug height (a 5 gallon water bottle is about 19 1/2 tall, with its neck)', d: 19.5, s: .25, a: 6, b: 30 },
  { k: 'jugD', g: 'Water tanks', l: 'Drain jug diameter (a 5 gallon water bottle is about 10 3/4 across)', d: 10.75, s: .25, a: 4, b: 18 },
  { k: 'jugGal', g: 'Water tanks', l: 'Drain jug: how much it holds (gallons; a 5 gallon water bottle holds 5)', d: 5, s: .5, a: 1, b: 15 },
  { k: 'hookOn', g: 'Take items out', l: 'Dish towel hook on the wall to the cab side of the nook, under the TV (the strip between the end of the nook and the sliding door opening)', d: true, t: 'c' },
  { k: 'hookTowel', g: 'Dish towel hook', l: 'Dish towel hook: how far the towel hangs below the hook (a dish towel folded over a hook hangs about 11 in)', d: 11, s: .5, a: 4, b: 30 },
  { k: 'hookOut', g: 'Dish towel hook', l: 'Dish towel hook: how far it sticks out from the wall', d: 2, s: .25, a: .5, b: 6 },
  { k: 'chairOn', g: 'Take items out', l: 'Lawn chairs folded and stored flat on the floor under the couch (they slide in from the rear doors)', d: true, t: 'c' },
  { k: 'chairN', g: 'Lawn chairs', l: 'Lawn chairs: how many (stacked flat)', d: 2, s: 1, a: 1, b: 6 },
  { k: 'chairLen', g: 'Lawn chairs', l: 'Lawn chair folded: length (a standard aluminum webbed chair folds to about 34.5 x 21.7 x 2.8; a camp quad chair in its bag is about 39 x 8 x 7)', d: 34.5, s: .25, a: 12, b: 60 },
  { k: 'chairWid', g: 'Lawn chairs', l: 'Lawn chair folded: width', d: 21.7, s: .25, a: 4, b: 40 },
  { k: 'chairThk', g: 'Lawn chairs', l: 'Lawn chair folded: thickness of each one', d: 2.8, s: .1, a: 1, b: 12 },
  { k: 'chairTurn', g: 'Lawn chairs', l: 'Lawn chairs: turn them so the long side runs across the van instead of along it', d: false, t: 'c' },
  { k: 'canOn', g: 'Take items out', l: 'Trash can on a pull-out in the cab-side column under the counter (replaces the two lower cab-side drawers and their shelves; turn it off to bring them back)', d: true, t: 'c' },
  { k: 'canGal', g: 'Trash can', l: 'Trash can: size in gallons (a tall kitchen can is 13)', d: 13, s: 1, a: 4, b: 30 },
  { k: 'canW', g: 'Trash can', l: 'Trash can: width along the wall (the column is 13 wide between the drawer slides and the pull-out tray is 1 in wider than the can, so 12 leaves 1/2 in each side)', d: 12, s: .25, a: 6, b: 20 },
  { k: 'canD', g: 'Trash can', l: 'Trash can: depth, out from the wall', d: 16, s: .25, a: 6, b: 24 },
  { k: 'canH', g: 'Trash can', l: 'Trash can: height with the lid shut', d: 24, s: .25, a: 8, b: 36 },
  { k: 'canBase', g: 'Trash can', l: 'Trash can: how high the bottom of the can is off the floor (the 3/4 in tray and 1/2 in slides are under it; 4 3/4 puts them about 1/8 in over the wheel well edge, 3 1/3 in tall at the back of the column)', d: 4.75, s: .25, a: 0, b: 16 },
  { k: 'canTravel', g: 'Trash can', l: 'Trash can pull-out: how far the slides carry it out (a 20 in slide goes about 19)', d: 19, s: .5, a: 4, b: 30 },
  { k: 'drainOn', g: 'Water tanks', l: 'Draw the relief valve drain line (over the top of the tank, down in front of the fresh tank, out through the floor)', d: true, t: 'c' },
  { k: 'drainX', g: 'Water tanks', l: 'Relief valve drain line: where it comes down (from the back)', d: 89, s: .5, a: 60, b: 125 },
  { k: 'drainDz', g: 'Water tanks', l: 'Relief valve drain line: the run over the tank moved up (+) or down (-) (you can drag it)', d: 0, s: .25, a: -12, b: 6 },
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
  { k: 'wallOn', g: 'Walls', l: 'Cover the walls (3/8 in birch plywood on the furring)', d: true, t: 'c' },
  { k: 'wallSub', g: 'Walls', l: 'Take the covering thickness off the inside width (leave off if the width was measured to the covered wall)', d: false, t: 'c' },
  { k: 'wallT', g: 'Walls', l: 'Covering thickness (3/8 in plywood, you said; it was 1/8)', d: .375, s: .125, a: .125, b: .75 },
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
  { k: 'plyT', g: 'Ceiling', l: 'Plywood thickness', d: .1875, s: .0625, a: .125, b: 1 },
  { k: 'slatW', g: 'Ceiling', l: 'Slat width', d: 3, s: .25, a: 1, b: 8 },
  { k: 'slatT', g: 'Ceiling', l: 'Slat thickness', d: .75, s: .125, a: .25, b: 3 },
  { k: 'slatDens', g: 'Ceiling', l: 'Slat wood density (lb per cu ft; western red cedar about 23, pine about 28)', d: 23, s: 1, a: 15, b: 60 },
  { k: 'slatGap', g: 'Ceiling', l: 'Gap between slats', d: 1, s: .25, a: 0, b: 6 },
  { k: 'slatAuto', g: 'Ceiling', l: 'Slats as long as the whole ceiling (no joints)', d: true, t: 'c', f: 'slatLen' },
  { k: 'slatLen', g: 'Ceiling', l: 'Slat length', d: 160, s: 1, a: 12, b: 220 },
  { k: 'lightSpots', g: 'Ceiling', l: 'Ceiling lights only over the shower and over the countertop and sink together (untick for evenly spaced rows instead)', d: true, t: 'c' },
  { k: 'lightN', g: 'Ceiling', l: 'Round lights in the ceiling (count; with the box above ticked at most 2: the shower, then the countertop and sink)', d: 2, s: 1, a: 0, b: 24 },
  { k: 'lightRows', g: 'Ceiling', l: 'Rows of lights along the ceiling', d: 2, s: 1, a: 1, b: 4 },
  { k: 'lightD', g: 'Ceiling', l: 'Light diameter (mounted on a slat)', d: 2, s: .25, a: 1, b: 8 },
  { k: 'fanX', g: 'Ceiling', l: 'Roof fan cutout: along the van (from the back)', d: 13.25, s: .5, a: 0, b: 220 },
  { k: 'fanY', g: 'Ceiling', l: 'Fan cutout: across (from the driver wall; 34 is the middle of the van, over the aisle)', d: 34, s: .5, a: 0, b: 90 },
  { k: 'fanUnit', g: 'Ceiling', l: 'Roof fan unit on the roof: square footprint (2012 F36AR exhaust fan: 17.7 x 17.7 x 6.4 tall)', d: 17.75, s: .25, a: 6, b: 40 },
  { k: 'fanW', g: 'Ceiling', l: 'Roof fan cutout: square size', d: 14, s: .25, a: 4, b: 30 },
  { k: 'acX', g: 'Ceiling', l: 'Air conditioning cutout: along the van (from the back)', d: 49.5, s: .5, a: 0, b: 220 },
  { k: 'acY', g: 'Ceiling', l: 'Air conditioning cutout: across (from the driver wall)', d: 34, s: .5, a: 0, b: 90 },
  { k: 'acUnit', g: 'Ceiling', l: 'Air conditioner unit on the roof: square footprint (OutEquip 12 V cooling-only: 28.3 x 28.3 x 6.3 tall, 45 lb on the listing)', d: 28.25, s: .25, a: 10, b: 50 },
  { k: 'acW', g: 'Ceiling', l: 'Air conditioning cutout: square size', d: 14.25, s: .25, a: 4, b: 30 },
  { k: 'battAh', g: 'Power', l: 'Battery capacity (Ah at 12 V)', d: 280, s: 10, a: 50, b: 800 },
  { k: 'acTurboA', g: 'Power', l: 'Air conditioner current in turbo (A at 12 V; the listing says up to 58)', d: 58, s: 1, a: 5, b: 120 },
  { k: 'acEcoA', g: 'Power', l: 'Air conditioner current in eco or sleep (A at 12 V; the listing says 21 and up, reviews 16 to 29)', d: 21, s: 1, a: 2, b: 80 },
  { k: 'acEcoH', g: 'Power', l: 'Hours a day the air conditioner runs in eco', d: 8, s: .5, a: 0, b: 24 },
  { k: 'fanLowW', g: 'Power', l: 'Roof fan power on low (W, 12 V DC)', d: 3, s: 1, a: 0, b: 100 },
  { k: 'fanHighW', g: 'Power', l: 'Roof fan power on high (W, 12 V DC)', d: 32, s: 1, a: 0, b: 200 },
  { k: 'fanHighH', g: 'Power', l: 'Hours a day the fan runs on high (the rest of the day is low)', d: 1, s: .5, a: 0, b: 24 },
  { k: 'heaterW', g: 'Power', l: 'Hot water heater power (W, 120 V)', d: 1440, s: 40, a: 200, b: 3000 }
];
// the drawers and shelves under the counter, the jar shelf and the microwave shelf: how far each is moved from its planned spot (you can drag them; double-click one to put it back)
[['TB', 'Top drawer, back side', 1], ['TC', 'Top drawer, cab side', 1], ['C1', 'Cab-side column: upper (or only) drawer', 1], ['C2', 'Cab-side column: lower drawer', 1], ['B1', 'Back-side column: upper (or only) drawer', 1], ['B2', 'Back-side column: middle drawer', 1], ['B3', 'Back-side column: bottom drawer', 1],
  ['SC', 'Shelf under the cab-side drawers', 0], ['SB', 'Shelf under the back-side drawers', 0], ['SC2', 'Board between the two cab-side lower drawers', 0], ['SB1', 'Board between the upper and middle back-side drawers', 0], ['SB2', 'Board between the middle and bottom back-side drawers', 0],
  ['Nook', 'Jar shelf in the nook (with its upper row of jars)', 0], ['Micro', 'Microwave and its shelf', 0], ['Jug', 'Drain jug (the 5 gallon bottle under the sink)', 0], ['Can', 'Trash can on its pull-out', 0], ['Hook', 'Dish towel hook', 0], ['Chairs', 'Lawn chairs under the couch', 0]].forEach(([k, nm, along]) => {
  PD.push({ k: 'dx' + k, g: 'Drawers and shelves', l: nm + ': moved along the wall (+ toward the cab, - toward the rear)', d: 0, s: .25, a: -60, b: 60 });
  PD.push({ k: 'dz' + k, g: 'Drawers and shelves', l: nm + ': moved up (+) or down (-)', d: 0, s: .25, a: -40, b: 40 });
});
PD.push({ k: 'dyChairs', g: 'Drawers and shelves', l: 'Lawn chairs under the couch: moved out from the driver wall (+) or toward it (-); 1 1/2 clears the wall posts of the couch frame', d: 1.5, s: .25, a: -30, b: 30 });
PD.push({ k: 'dyCan', g: 'Drawers and shelves', l: 'Trash can on its pull-out: moved out from the wall (+) or toward it (-)', d: 0, s: .25, a: -12, b: 12 });
PD.push({ k: 'dyJug', g: 'Drawers and shelves', l: 'Drain jug (the 5 gallon bottle under the sink): moved out from the wall (+) or toward it (-)', d: 0, s: .25, a: -12, b: 12 });
const DEF = {}; PD.forEach(p => DEF[p.k] = p.d);
let P = Object.assign({}, DEF);

/* ================= helpers ================= */
const $ = s => document.querySelector(s);
const clamp = (v, a, b) => Math.min(b, Math.max(a, v));
const f1 = n => String(Math.round(n * 10) / 10);
function fmt(n) {
  const neg = n < 0; n = Math.abs(n);
  let w = Math.floor(n + 1e-9), fr = Math.round((n - w) * 16);
  if (fr === 16) { w++; fr = 0; }
  if (!w && !fr) return '0';
  const F = ['', '1/16', '1/8', '3/16', '1/4', '5/16', '3/8', '7/16', '1/2', '9/16', '5/8', '11/16', '3/4', '13/16', '7/8', '15/16'][fr];
  const s = fr ? (w ? w + ' ' + F : F) : String(w);
  return (neg ? '-' : '') + s;
}
const slatWood = P => P.slatDens <= 25 ? 'cedar' : P.slatDens <= 32 ? 'pine' : 'hardwood';
const COL = { P: '#534AB7', G: '#444441', K: '#993556', T: '#0F6E56', C: '#993C1D', B: '#8A5A00', W2: '#8A6B4D', BL: '#185FA5' };
const HALO = 'paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-opacity:.85';
function T(x, y, s, o) {
  o = o || {};
  const size = o.size || 12, fill = o.fill || '#2C2C2A', anchor = o.anchor || 'middle', w = o.w || 400, halo = o.halo !== false;
  return `<text x="${f1(x)}" y="${f1(y)}" text-anchor="${anchor}"${o.op != null && o.op < 1 ? ` opacity="${f1(o.op)}"` : ''} style="font-size:${size}px;font-weight:${w};fill:${fill};${halo ? HALO : ''}">${s}</text>`;
}
// The jar nook: it ends at 93 1/4 on the cab side and its length comes off the rear end; how many jars fit in a row
const NK = P => [93.25 - P.nookLen, 93.25];
const JN = P => Math.max(0, Math.floor((P.nookLen - 1) / P.jarW + 1e-9));
// An item label: the name and its size written on the drawing, or (the Number the items box) a small numbered badge with the name and size listed under the drawing.
// The badge carries a token that render() replaces with the final number, once it knows which labels are really in the picture and where they sit.
const KEYS = [];
function LBL(x, y, name, dims, o) {
  o = o || {};
  if (o.op != null && o.op <= .02) return '';
  const fill = o.fill || '#2C2C2A';
  if (!P.numLbl) {
    const to = Object.assign({}, o); delete to.dy;
    if (o.dimsOnly) return T(x, y, dims, to);
    let g = T(x, y, name, to);
    if (dims) g += T(x, y + (o.dy == null ? 14 : o.dy), dims, Object.assign({}, to, { size: o.size2 || Math.max(9, (o.size || 12) - 1.5) }));
    return g;
  }
  const i = KEYS.length; KEYS.push({ x, y, name, dims: [dims, o.keyMore].filter(Boolean).join(', '), fill });
  const op = o.op != null && o.op < 1 ? ` opacity="${f1(o.op)}"` : '';
  return `<g class="nb"${op}><circle cx="${f1(x)}" cy="${f1(y)}" r="9.5" fill="#fff" fill-opacity=".94" stroke="${fill}" stroke-width="1.7"/><text x="${f1(x)}" y="${f1(y + 3.8)}" text-anchor="middle" style="font-size:10.5px;font-weight:700;fill:${fill}">\u0001${i}\u0001</text></g>`;
}
// small notes that only belong on a drawing with the names written on it
const NOTE = (x, y, s, o) => P.numLbl ? '' : T(x, y, s, o);
// the numbers, in the order the items sit across the drawing; returns the body with the tokens replaced and the key rows
function numberLabels(body) {
  const seen = [...new Set([...body.matchAll(/\u0001(\d+)\u0001/g)].map(m => +m[1]))];
  const ord = seen.sort((a, b) => KEYS[a].x - KEYS[b].x || KEYS[a].y - KEYS[b].y);
  const num = {}; ord.forEach((k, n) => { num[k] = n + 1; });
  return { body: body.replace(/\u0001(\d+)\u0001/g, (m, k) => num[k]), rows: ord.map(k => Object.assign({ n: num[k] }, KEYS[k])) };
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
// named groups in a drawing, so the page can hide an item: everything drawn between GB and GE carries data-grp (and so does the item's drag handle)
const GB = (id, label) => `<g class="hg" data-grp="${id}" data-label="${label}">`;
const GE = () => '</g>';
// items that were taken out (their tick box in Sizes is off): cut their groups and drag handles out of a finished drawing
const REMOVED = () => [['showerOn', 'shower'], ['microOn', 'Micro'], ['tvOn', 'tv'], ['towelOn', 'towels'], ['fridgeOn', 'fridge'], ['drawersOn', 'drawers'], ['battOn', 'batt'], ['closetOn', 'closet'], ['wallsOn', 'fwalls'], ['toiletOn', 'toilet'], ['snItemsOn', 'snitems'], ['gearOn', 'gear'], ['gcabOn', 'gcab'], ['winOn', 'win']].filter(r => !P[r[0]]).map(r => r[1]);
function stripGroups(html, ids) {
  ids.forEach(id => {
    const open = `<g class="hg" data-grp="${id}"`;
    let i;
    while ((i = html.indexOf(open)) >= 0) {
      const re = /<g[\s>]|<\/g>/g; re.lastIndex = i; let depth = 0, m, end = -1;
      while ((m = re.exec(html))) { depth += m[0] === '</g>' ? -1 : 1; if (depth === 0) { end = re.lastIndex; break; } }
      if (end < 0) break;
      html = html.slice(0, i) + html.slice(end);
    }
    html = html.replace(new RegExp(`<rect class="drg"[^>]*data-grp="${id}"[^>]*>[^<]*<title>[^<]*</title></rect>`, 'g'), '');
  });
  return html;
}
// a see-through rectangle over an item that can be dragged.
// ax = [size changed by sideways drags, inches per drawing unit, size changed by up and down drags, inches per drawing unit]; a size name may be '' for none, and the inches
// are negative where the drawing runs the other way. on = a tick box size that the first drag switches on.
function HIT(id, x, y, w, h, ax, bad, label, on, grp) {
  const k = v => +(+v || 0).toFixed(5);
  return `<rect class="drg" data-drag="${id}" data-grp="${grp || id}" data-px="${ax[0]}" data-kx="${k(ax[1])}" data-py="${ax[2]}" data-ky="${k(ax[3])}" data-on="${on || ''}" x="${f1(x)}" y="${f1(y)}" width="${f1(Math.max(2, w))}" height="${f1(Math.max(2, h))}" rx="3" fill="#534AB7" fill-opacity="${bad ? .12 : .02}" stroke="${bad ? '#C0392B' : '#534AB7'}" stroke-width="${bad ? 2.6 : 1}" stroke-dasharray="${bad ? '5 2' : '2 3'}" stroke-opacity="${bad ? 1 : .6}"><title>${label}${bad ? ' (overlaps something: see the red message above the drawing)' : ' (drag to move it, double-click to put it back)'}</title></rect>`;
}
// every drawer and shelf board under the counter as a box: kind, id (the sizes that move it are dx<id> along the wall and dz<id> up), n = its name,
// x0/x1 along the wall and z0/z1 up (the planned spot plus how far it was dragged, both ways), y0/y1 out from the wall. The planned spots fill the space between the shelves, the
// top drawers and the tanks, as before; dragging only adds to them.
function cabinetParts(L) {
  const P = L.P, ch = P.counterH, d0 = L.cabS + 1.25, dm = L.cabS + 14.75, sx0 = L.cabS + (P.wallsOn ? P.fwT : 0), z0 = ch - 6.75, z1 = ch - 2.75, tl = z0 - .25, can = !!P.canOn, bs = (can ? L.backShelf : L.cabShelf) + 1, tot = tl - bs, parts = [];
  const add = (kind, id, n, x0, x1, b0, b1) => {
    const dx = P['dx' + id] || 0, dz = P['dz' + id] || 0;
    parts.push({ kind, id, n, x0: x0 + dx, x1: x1 + dx, z0: b0 + dz, z1: b1 + dz, y0: 0, y1: 20, dxk: 'dx' + id, dzk: 'dz' + id });
  };
  L.cabTot = tot; L.wellShelf = tot >= 11 || can ? L.backShelf : L.cabShelf;
  if (!P.drawersOn) return parts;   // taken out: no drawers, boards or rail (the divider the trash can needs stays in the solids)
  add('drawer', 'TB', 'the top drawer on the back side', d0, dm - .5, z0, z1);
  add('drawer', 'TC', 'the top drawer on the cab side', dm + 1, dm + 14, z0, z1);
  if (tot >= 3) {
    const ws = L.wellShelf;
    if (!can) add('shelf', 'SC', 'the shelf under the cab-side drawers', dm, L.angS - .75, L.cabShelf, L.cabShelf + .75);   // with the trash can the cab-side column has no lower drawers or shelves
    add('shelf', 'SB', 'the shelf under the back-side drawers', sx0, dm, ws, ws + .75);
    if (tot >= 11) {
      const bt = tl - 6, bb = ws + 1, many = bt - bb >= 14.5, rh2 = (bt - bb - 1) / 2;
      if (!can) {
        add('shelf', 'SC2', 'the board between the two cab-side lower drawers', dm, L.angS - .75, tl - 6, tl - 5.25);
        add('drawer', 'C1', 'the upper cab-side drawer', dm + 1, dm + 14, tl - 5, tl);
        add('drawer', 'C2', 'the lower cab-side drawer', dm + 1, dm + 14, tl - 11, tl - 6);
      }
      if (many) {
        add('shelf', 'SB1', 'the board between the upper and middle back-side drawers', sx0, dm, bt, bt + .75);
        add('shelf', 'SB2', 'the board between the middle and bottom back-side drawers', sx0, dm, bb + rh2, bb + rh2 + .75);
        add('drawer', 'B1', 'the upper back-side drawer', d0, dm - .5, tl - 5, tl);
        add('drawer', 'B2', 'the middle back-side drawer', d0, dm - .5, bb + rh2 + 1, bt);
        add('drawer', 'B3', 'the bottom back-side drawer', d0, dm - .5, bb, bb + rh2);
      } else add('drawer', 'B1', 'the back-side drawer', d0, dm - .5, bb, tl);
    } else {
      add('drawer', 'B1', 'the back-side drawer', d0, dm - .5, bs, tl);
      if (!can) add('drawer', 'C1', 'the cab-side drawer', dm + 1, dm + 14, bs, tl);
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
  const fresh = bx('fresh', 'the fresh water tank', L.tankX[0], L.tankX[1], P.tankBack, P.tankBack + P.tankD, P.tankLift, P.tankLift + P.tankH, { kind: 'tank' });
  const mov = [hot, fresh];
  L.parts.forEach(p => mov.push(bx(p.id, p.n, p.x0, p.x1, p.y0, p.y1, p.z0, p.z1, { kind: p.kind })));
  const [nx0, nx1] = NK(P);
  if (P.nookOn) mov.push(bx('Nook', 'the jar shelf in the nook with its upper row of jars', L.nookX[0], L.nookX[1], 0, 4.5, L.nookZ, L.nookZ + .75 + 7, { kind: 'jars' }));
  if (P.microOn) mov.push(bx('Micro', 'the microwave and its shelf', L.microX[0], L.microX[1], 0, P.microIn + 12, L.microZ[0] - .75, L.microZ[1], { kind: 'micro' }));
  // the drain jug (a bottle) is checked by its square outline; it stands on the fresh water tank
  // the trash can with its tray and slides (a 3/4 in tray and 1/2 in slide under the can), closed in its place under the counter
  if (L.hook) mov.push(bx('Hook', 'the dish towel hook with its towel', L.hook.x0, L.hook.x1, L.hook.y0, L.hook.y1, L.hook.z0, L.hook.z1, { kind: 'hook' }));
  if (L.chairs) mov.push(bx('Chairs', 'the stack of lawn chairs', L.chairs.x0, L.chairs.x1, L.chairs.y0, L.chairs.y1, L.chairs.z0, L.chairs.z1, { kind: 'chair' }));
  if (L.can) {
    const c = L.can;
    mov.push(bx('Can', 'the trash can', c.x0, c.x1, c.y0, c.y1, c.z0, c.z1, { kind: 'can' }));
    mov.push(bx('Can', 'the pull-out tray under the trash can', c.tx0, c.tx1, c.ty0, c.ty1, c.z0 - 1.25, c.z0, { kind: 'can' }));
  }
  if (L.jug) mov.push(bx('Jug', 'the drain jug', L.jug.x0, L.jug.x1, L.jug.y0, L.jug.y1, L.jug.z0, L.jug.z1, { kind: 'jug' }));
  // the wheel well is a trapezoid: 2 in high at 42, 7.5 from 51.25 to 66.75, 2 in high at 76
  const wellH = x => x < 42 || x > 76 ? 0 : x < 51.25 ? 2 + (x - 42) * 5.5 / 9.25 : x <= 66.75 ? 7.5 : 7.5 - (x - 66.75) * 5.5 / 9.25;
  if (P.hotShelf > .5) mov.push(bx('hot', 'the hot water tank shelf', L.hotX[0] - 1, L.hotX[1] + 1, P.hotBack, P.hotBack + P.hotD, P.hotShelf - .75, P.hotShelf, { kind: 'hotboard', vs: ['drawer', 'tank', 'can', 'jug'] }));
  const fix = [
    bx('', 'the wheel well', 42, 76, 0, 7, 0, 7.5, { prof: wellH }), P.fridgeOn && bx('', 'the fridge', L.fr[0], L.fr[1], 2, 2 + P.fridgeD, 8.25, ft), bx('', 'the cab wall', P.cab, P.cab + 60, 0, 40, 0, 120),
    ...L.walls.filter(w => w.side === 'p').map(w => bx('', w.n, w.x0, w.x1, 0, w.d, 0, L.ceilF)),
    bx('', 'the floor', -10, P.cab + 10, -5, 45, -40, 0), bx('', 'the ceiling', -10, P.cab + 10, -5, 45, L.ceilF, L.ceilF + 40),
    bx('', 'the counter and its rail', L.cabS, L.angS - .75, 0, P.cabD, ch - 2.25, ch), bx('', 'the countertop', L.angS - .75, L.sinkE, 0, P.cabD, ch - 1.2, ch),
    bx('', 'the sink under the counter', L.sinkS, L.sinkE, 0, P.sinkD, ch - P.sinkBowlD, ch - 1.2),
    P.nookOn && JN(P) > 0 && bx('', 'the lower row of jars', nx0 + .75, nx0 + .75 + JN(P) * P.jarW, 0, 4.5, ch, ch + 7), bx('', 'the top of the nook', nx0, nx1, 0, 4.5, ch + P.nookH, ch + 40),
    P.tvOn && bx('', 'the TV', 76.5, 103.5, 0, 4.5, ch + 16, ch + 31.4),
    // the paper towel roll sits in a recess in the angled front, 6 in deep from the door face (a tank may touch its bottom, not reach into it)
    P.towelOn && bx('', 'the paper towel recess', L.sinkS - 11.5, L.sinkS - .5, Math.max(0, Math.min(L.angS < L.sinkS ? Math.max(P.sinkD, P.cabD - L.slope * (L.sinkS - L.angS)) : P.sinkD, P.cabD) - 6.75), P.cabD, 29.75, 35.25, { vs: ['tank'] }),
    // the sink cabinet door (3/4 in, at the sink end depth) and the wall: the drain jug has to stay between them
    bx('', 'the sink cabinet door', L.sinkS, L.sinkE, P.sinkD - .75, P.sinkD, 0, ch, { vs: ['jug'] }), bx('', 'the van wall', -30, P.cab + 10, -5, 0, 0, ch, { vs: ['jug', 'can'] }),
    // the divider between the two drawer columns (only drawers count: the shelves meet it by design)
    bx('', 'the divider between the two columns', dm, dm + .5, 0, 20, L.cabTot >= 3 ? L.wellShelf + .75 : ch - 7.25, ch - 2.5, { vs: ['drawer'] }),
    // under the couch: the driver wheel well, the battery, the underside of the deck, the closet and the rear doors; the lawn chairs have to stay between them (y is out from the passenger wall: the driver side is at y = vanW)
    bx('', 'the driver side wheel well', 42, 76, P.vanW - 7, P.vanW, 0, 7.5, { prof: wellH, vs: ['chair'] }), P.battOn && bx('', 'the battery', L.batt[0], L.batt[1], P.vanW - 17, P.vanW - 7, 0, 9.5, { vs: ['chair'] }),
    bx('', 'the underside of the couch deck', 0, P.bedLen, P.vanW - P.bedD, P.vanW + 5, P.platform - 1.5, P.platform + 40, { vs: ['chair'] }), P.closetOn && bx('', 'the closet', L.c0, L.c1, P.vanW - P.closetD, P.vanW + 5, 0, 80, { vs: ['chair'] }),
    bx('', 'the rear doors', -30, -6, -5, P.vanW + 5, 0, 90, { vs: ['chair'] }), bx('', 'the driver side wall', -30, P.cab, P.vanW, P.vanW + 5, 0, 90, { vs: ['chair'] }), bx('', 'the floor', -30, P.cab + 10, -5, P.vanW + 5, -40, 0, { vs: ['chair'] }),
    // the trash can has the divider (down to the floor for it) beside it and the cabinet door in front of it
    P.canOn && bx('', 'the divider between the two columns', dm, dm + .5, 0, 20, 0, ch - 2.5, { vs: ['can', 'tank', 'hotboard'] }), bx('', 'the cabinet door', L.cabS, L.angS - .75, P.cabD - .75, P.cabD, 0, ch - 2.5, { vs: ['can'] })
  ].filter(Boolean);
  const ov = (a0, a1, b0, b1) => Math.min(a1, b1) - Math.max(a0, b0), seen = new Set(), cp = n => n[0].toUpperCase() + n.slice(1);
  const test = (a, b) => {
    if ((b.vs && !b.vs.includes(a.kind)) || (a.vs && !a.vs.includes(b.kind)) || (a.id && a.id === b.id)) return;
    let bz1 = b.z1;
    if (b.prof) { const lo = Math.max(a.x0, b.x0), hi = Math.min(a.x1, b.x1); bz1 = Math.max(b.prof(lo), b.prof(hi), lo <= 51.25 && hi >= 51.25 ? 7.5 : 0, lo <= 66.75 && hi >= 66.75 ? 7.5 : 0); }
    const ox = ov(a.x0, a.x1, b.x0, b.x1), oy = ov(a.y0, a.y1, b.y0, b.y1), oz = ov(a.z0, a.z1, b.z0, bz1);
    if (ox > .06 && oy > .06 && oz > .06) {
      const key = a.id + '|' + b.n + '|' + b.id; if (seen.has(key)) return; seen.add(key); ids.add(a.id); if (b.id) ids.add(b.id);
      list.push({ ids: [a.id, b.id], msg: `${cp(a.n)} overlaps ${b.n} (${fmt(ox)} in along the wall, ${fmt(oy)} in out from it, ${fmt(oz)} in up).` });
    }
  };
  mov.forEach((a, i) => { for (let j = i + 1; j < mov.length; j++) test(a, mov[j]); fix.forEach(b => test(a, b)); });
  // drawers and boards must stay inside the flat part of the cabinet, the jar shelf inside the nook, the microwave shelf over the fridge
  const outOf = (id, n, x0, x1, lo, hi, what) => { const out = Math.max(lo - x0, x1 - hi); if (out > .06) { ids.add(id); list.push({ ids: [id], msg: `${cp(n)} sticks out ${fmt(out)} in past ${what} (${fmt(lo)} to ${fmt(hi)} in).` }); } };
  L.parts.forEach(p => outOf(p.id, p.n, p.x0, p.x1, p.kind === 'drawer' ? L.cabS + .75 : L.cabS, L.angS - .75, 'the flat part of the cabinet'));
  if (P.nookOn) outOf('Nook', 'the jar shelf in the nook', L.nookX[0], L.nookX[1], nx0, nx1, 'the nook');
  if (P.microOn && P.fridgeOn) outOf('Micro', 'the microwave and its shelf', L.microX[0], L.microX[1], L.fr[0], L.fr[1], 'the top of the fridge');
  if (L.hook) outOf('Hook', 'the dish towel hook with its towel', L.hook.x0, L.hook.x1, 0, P.doorX, 'the wall before the sliding door opening');
  if (L.chairs) {
    const c = L.chairs, over = c.d1 - P.bedD;
    if (over > .06 && c.x1 > 0 && c.x0 < P.bedLen) { ids.add('Chairs'); list.push({ ids: ['Chairs'], msg: `The stack of lawn chairs sticks out ${fmt(over)} in past the front of the couch deck (${fmt(P.bedD)} in out from the driver wall) into the aisle.` }); }
  }
  if (L.can) outOf('Can', 'the pull-out tray under the trash can', L.can.tx0, L.can.tx1, L.cabS, L.angS - .75, 'the flat part of the cabinet');
  if (L.jug) {
    // under the sink, and standing on the top of the fresh water tank (its footprint is the tank's: along the wall and out from it)
    outOf('Jug', 'the drain jug', L.jug.x0, L.jug.x1, L.sinkS, L.sinkE - .75, 'the sink cabinet, under the sink');
    outOf('Jug', 'the drain jug', L.jug.x0, L.jug.x1, L.tankX[0], L.tankX[1], 'the top of the fresh water tank');
    const outY = Math.max(P.tankBack - L.jug.y0, L.jug.y1 - (P.tankBack + P.tankD));
    if (outY > .06) { ids.add('Jug'); list.push({ ids: ['Jug'], msg: `The drain jug sticks out ${fmt(outY)} in past the ${P.tankBack - L.jug.y0 > L.jug.y1 - (P.tankBack + P.tankD) ? 'back' : 'front'} of the top of the fresh water tank (${fmt(P.tankBack)} to ${fmt(P.tankBack + P.tankD)} in out from the wall).` }); }
  }
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
  // the closet: the clothes hang from the rod (the garment's shoulder is hangDrop below it), the longest one ends cloClear above the drawers, and the drawers fill the space under it
  L.hangBot = P.rodHi - P.hangDrop - P.cloLen; L.drawTop = Math.max(3, L.hangBot - P.cloClear); L.split = L.drawTop + .15;
  { const n = Math.max(1, Math.round(P.cloDrawN)), gap = .125, h = (L.drawTop - 1 - (n - 1) * gap) / n; L.cloDr = []; for (let i = 0; i < n; i++) L.cloDr.push({ z0: 1 + i * (h + gap), z1: 1 + i * (h + gap) + h }); L.cloDrH = h; L.cloDrW = P.closetW - 1.5 - 1; L.cloPull = Math.max(0, P.cloDrawD - 1); }
  // the toilet: sideways at the cab end of the wet bath, back against the wall to the fridge, centered across the stall (y = out from the passenger wall)
  { const x1 = P.panW - (P.wallsOn ? P.fwT : 0), y0 = (P.panD - P.toiletW) / 2; L.toilet = P.toiletOn ? { x0: x1 - P.toiletD, x1, y0, y1: y0 + P.toiletW, z1: P.toiletH } : null; }
  // the shower nook contents: a towel bar bay at the rear end, then a shelf board with the bottles on it and the toilet paper rolls under it
  {
    const nkx = Math.min(29.75, P.panW - 6.25), nk0 = nkx - P.snookLen, bot = P.snookTop - P.snookH, top = P.snookTop, lip = P.snookLip;
    const sn = { x0: nk0, x1: nkx, z0: bot, z1: top, bay: nk0 + P.tbarBay, shelfTop: Math.min(top - 1, P.snShelf) };
    sn.bar = { x0: nk0 + .5, x1: sn.bay - .5, z: top - P.tbarDrop };
    sn.cord = P.snCord > 0 ? { x0: nk0 + .6, x1: nkx - .6, z: Math.min(top - .75, sn.shelfTop + P.snCord) } : null;   // a bungee cord stretched across the front of the nook between two screw eyes
    sn.rolls = [[nkx - 4.75, nkx - .25], [nkx - 9.5, nkx - 5]].map(r => ({ x0: r[0], x1: r[1], z0: bot, z1: bot + 4.5 }));
    let bx0 = sn.bay + .5; sn.bottles = [[2.6, 8.5], [3, 9], [2.6, 7.5]].map(b => { const o = { x0: bx0, x1: bx0 + b[0], z0: sn.shelfTop, z1: sn.shelfTop + b[1] }; bx0 += b[0] + .5; return o; });
    sn.bottlesEnd = bx0 - .5; sn.rollClear = sn.shelfTop - .75 - bot - 4.5; sn.bottleClear = top - sn.shelfTop;
    L.sn = P.snItemsOn ? sn : null;
  }
  // floor-to-ceiling walls. Driver side (y = out from the driver wall): the closet's cab-side panel carried out to the bench depth, which the back of the rear bench leans on,
  // and the wall behind the driver seat (face at the cab wall mark, body behind it), which the back of the cab-end bench leans on. Passenger side (y = out from the passenger wall):
  // one each side of the fridge, taken out of the shower and out of the counter cabinet so that no other position moves; the shower one is as deep as the pan, the counter one as deep as the cabinet
  L.walls = !P.wallsOn ? [] : [
    { id: 'W1', side: 'd', x0: L.c1 - P.fwT, x1: L.c1, d: P.benchD, n: 'wall behind the rear dinette seat (closet end)' },
    { id: 'W2', side: 'd', x0: P.cab, x1: P.cab + P.fwT, d: P.benchD, n: 'wall behind the driver seat' },
    { id: 'W3', side: 'p', x0: P.panW - P.fwT, x1: P.panW, d: Math.max(P.panD, 2 + P.fridgeD), n: 'wall between the shower and the fridge' },
    { id: 'W4', side: 'p', x0: P.panW + P.fridgeW, x1: P.panW + P.fridgeW + P.fwT, d: Math.max(P.cabD, 2 + P.fridgeD), n: 'wall between the fridge and the counter cabinet' },
  ];
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
  // the charging gear on ONE pull-out shelf over the battery (y = out from the driver wall; the couch front over the gear is the shelf's own face, 3/4 in thick, at bedD - 3/4):
  // a 1/2 in plywood tray between two 3/4 in end rails on two 18 in full-extension slides, one on the closet's end panel and one on a plywood divider west of the wheel well, 1 in over the battery top for the terminals and lugs;
  // the tray runs from the front of the couch back over the battery (7 3/4 to 25 1/4 out) so an 18 in pull puts all of it in the aisle.
  // Row 1 (rear): the DC-DC charger, then the inverter; row 2 (front): the shore charger. The battery stays on the floor under it.
  { const hy = P.bedD - .75, sz0 = 9.5 + P.shG, sz1 = sz0 + P.shT, sx1 = L.c0 - .65, sx0 = sx1 - (P.dcL + P.invL + 2.5), dd = Math.max(P.dcW, P.invW), ty0 = hy - (.75 + dd + .5 + P.chW + .25);
    const dc = { x0: sx0 + 1, x1: sx0 + 1 + P.dcL, y0: ty0 + .75, y1: ty0 + .75 + P.dcW, z0: sz1, z1: sz1 + P.dcH, n: 'the DC-DC charger', id: 'G2' };
    const inv = { x0: dc.x1 + .5, x1: dc.x1 + .5 + P.invL, y0: ty0 + .75, y1: ty0 + .75 + P.invW, z0: sz1, z1: sz1 + P.invH, n: 'the inverter', id: 'G1' };
    const ch = { x0: dc.x0, x1: dc.x0 + P.chL, y0: ty0 + .75 + dd + .5, y1: ty0 + .75 + dd + .5 + P.chW, z0: sz1, z1: sz1 + P.chH, n: 'the shore charger', id: 'G3' };
    const sh = { x0: sx0, x1: sx1, y0: ty0, y1: hy, z0: sz0, z1: sz1, div: sx0 - .65 - .75 };
    L.gear = P.gearOn ? { inv, dc, ch, sh, hatchY: hy } : null;
    // the gear cabinet: two 3/4 in plywood side panels standing on the floor, as deep as the couch (the west one is the shelf's slide divider, the east one the closet's end panel), from the floor to the underside of the deck.
    // The couch is a separate removable frame: a 3/4 x 3 1/2 in back rail hung on wooden blocks screwed to the wall (blkA, blkB, blkC along the wall: each a 2x2 post 1 1/2 x 1 1/2 standing on the floor, tops at the rail's underside), a front rail and posts west of the cabinet, and the deck resting on the cabinet's panels.
    const du = P.platform - 1.5, bz1 = du - 3.5, bz0 = bz1 - 3.5;
    L.gcab = P.gcabOn ? { x0: sx0 - .65 - .75, x1: L.c0, y1: P.bedD, z1: du } : null;
    L.cblk = P.gcabOn ? [[P.blkA, 1], [P.blkB, P.blkBOn ? 1 : 0], [P.blkC, 1]].filter(b => b[1]).map(b => ({ x: b[0], x0: b[0] - .75, x1: b[0] + .75, y0: 0, y1: 1.5, z0: 0, z1: bz1 })) : [];
    // the front rail across the cabinet: 3/4 x 1 on edge, glued and screwed to the deck's underside along the front edge between the panels (fh = its height; its bottom stays fz0 up, over the tallest unit)
    const fh = 1, tall = L.gear ? Math.max(P.dcH, P.invH, P.chH) + sz1 : 0;
    L.cmod = P.gcabOn ? { du, rz0: bz1, beamX0: sx0 - .65 - .75 + .75, beamX1: L.c0, west: sx0 - .65 - .75, posts: [0, sx0 - .65 - .75 - 1.5], fr: { x0: sx0 - .65 - .75 + .75, x1: L.c0, y0: P.bedD - .75, y1: P.bedD, z0: du - fh, z1: du, h: fh, tall } } : null; }
  // the side window over the dinette: the cutout (the slider frame's outline, what goes through the steel) and the glass (outside, glued over the stamping)
  { const cx0 = P.winX, cx1 = cx0 + P.winCW, cz0 = P.winZ, cz1 = cz0 + P.winCH, gx0 = cx0 - P.winOL, gz0 = cz0 - P.winOB;
    L.win = P.winOn ? { cx0, cx1, cz0, cz1, gx0, gx1: gx0 + P.winGW, gz0, gz1: gz0 + P.winGH, div: gx0 + 28.625 } : null; }
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
    const overCab = ov(L.hotX[0], L.hotX[1], dm, L.angS - .75), overBack = ov(L.hotX[0], L.hotX[1], L.cabS, dm);
    const freshCab = ov(L.tankX[0], L.tankX[1], dm, L.angS - .75), freshBack = ov(L.tankX[0], L.tankX[1], L.cabS, dm);
    const pick = (h, f) => { const c = [[7.5, 'the wheel well'], [h ? hotTopZ : 0, 'the hot water tank'], [f ? P.tankLift + P.tankH : 0, 'the fresh water tank']]; return c.reduce((a, b) => b[0] > a[0] ? b : a); };
    const cb = pick(overCab, freshCab), bb = pick(overBack, freshBack);
    L.cabShelf = cb[0] + .5; L.cabBy = cb[1]; L.backShelf = bb[0] + .5; L.backBy = bb[1];
  }
  L.hotY = [P.hotBack, P.hotBack + P.hotD];
  {
    // the relief valve drain run goes forward over the tank and back along its front to the down leg; it has to stay inside the cabinet door, which is shallower toward the sink
    const rx = L.hotX[0] + .8 * P.hotW, x0 = Math.min(P.drainX, rx), x1 = Math.max(P.drainX, rx), dA = x => x <= L.angS ? P.cabD : Math.max(P.sinkD, P.cabD - L.slope * (x - L.angS));
    L.drainInside = Math.min(dA(x0), dA(x1)) - .75;
    L.drainY = Math.min(P.tankBack + P.tankD + 2.5, L.drainInside - P.drainDia / 2 - .1);
  }
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
    if (P.lightSpots) {
      // lights only over the shower stall and one over the countertop and sink together: x is from the rear-door edge (the wall numbers + 6), y across from the driver wall;
      // each sits on the slat nearest the middle of what it lights (ties go toward the passenger wall) and 2 in clear of a rib (on the nearer side), so the wire hole misses it
      const cs = L.cabS + 6, se = L.sinkE + 6;
      const want = [[6 + P.panW / 2, P.vanW - P.panD / 2], [(cs + se) / 2, P.vanW - P.cabD / 2]].slice(0, N);
      want.forEach(w => {
        let x = w[0], y = w[1];
        L.ribBands.forEach(b => { if (x > b[0] - 2 && x < b[1] + 2) x = (x - (b[0] - 2)) < ((b[1] + 2) - x) ? b[0] - 2 : b[1] + 2; });
        if (P.liningOn && n > 0) { let best = 0, bd = 1e9; L.slatY.forEach((sy, k) => { const d = Math.abs(sy + P.slatW / 2 - y); if (d < bd - 1e-9 || (Math.abs(d - bd) < 1e-9 && sy > L.slatY[best])) { bd = d; best = k; } }); y = L.slatY[best] + P.slatW / 2; if (L.chanY.indexOf(y) < 0) L.chanY.push(y); }
        L.lights.push({ x, y });
      });
    } else
    for (let r = 0; r < rows; r++) {
      const cnt = Math.floor(N / rows) + (r < N % rows ? 1 : 0); if (cnt < 1) continue;
      const target = L.ceilOff + P.ceilW * (r + 1) / (rows + 1); let y = target;
      if (P.liningOn && n > 0) { let best = 0, bd = 1e9; L.slatY.forEach((sy, k) => { const d = Math.abs(sy + P.slatW / 2 - target); if (d < bd) { bd = d; best = k; } }); y = L.slatY[best] + P.slatW / 2; L.chanY.push(y); }
      for (let c = 0; c < cnt; c++) L.lights.push({ x: P.ceilLen * (c + .5) / cnt, y });
    }
    L.fan = { x: P.fanX, y: P.fanY, w: P.fanW, nm: 'roof fan', u: P.fanUnit }; L.ac = { x: P.acX, y: P.acY, w: P.acW, nm: 'A/C', u: P.acUnit };
    L.slatsCut = c => L.slatY.filter((sy, k) => !L.slatOut.has(k) && sy < c.y + c.w / 2 && sy + P.slatW > c.y - c.w / 2).length;
  }
  // the drawers and shelves under the counter (as planned plus dragged), the jar shelf in the nook and the microwave shelf above the fridge
  L.parts = cabinetParts(L); L.partById = {}; L.parts.forEach(p => { L.partById[p.id] = p; });
  L.nookZ = P.counterH + 7.5 + P.dzNook; L.nookX = [NK(P)[0] + P.dxNook, NK(P)[1] + P.dxNook];
  L.microX = [L.fr[0] + P.dxMicro, L.fr[1] + P.dxMicro];
  L.microZ = [8.25 + P.fridgeH + 2.75 + P.dzMicro, 8.25 + P.fridgeH + 12.75 + P.dzMicro];   // the microwave bottom and top; its shelf is the 3/4 in under it, 2 in over the fridge top
  // the dish towel hook on the wall strip between the end of the nook (93 1/4) and the sliding door opening, under the TV; the folded towel (8 in wide) hangs from it
  L.hook = null;
  if (P.hookOn) {
    const hx = 98.5 + P.dxHook, hz = 50 + P.dzHook;
    L.hook = { x: hx, z: hz, x0: hx - 4, x1: hx + 4, y0: 0, y1: P.hookOut, z0: hz - P.hookTowel, z1: hz + 1 };
  }
  // the lawn chairs: folded and stacked flat on the floor under the couch, against the driver wall at the rear end of the deck, plus how far they were dragged (d = out from the driver wall, y = out from the passenger wall)
  L.chairs = null;
  if (P.chairOn) {
    const n = Math.max(1, Math.round(P.chairN)), lx = P.chairTurn ? P.chairWid : P.chairLen, ld = P.chairTurn ? P.chairLen : P.chairWid, cx0 = P.dxChairs, cd0 = P.dyChairs, cz0 = P.dzChairs;
    L.chairs = { n, x0: cx0, x1: cx0 + lx, d0: cd0, d1: cd0 + ld, y0: P.vanW - cd0 - ld, y1: P.vanW - cd0, z0: cz0, z1: cz0 + n * P.chairThk };
  }
  // the trash can on its pull-out in the cab-side column (centered between the drawer slides, 1 1/2 in off the wall), plus how far it was dragged; z0 is the bottom of the can (the tray and slides are under it)
  L.can = null;
  if (P.canOn) {
    const ccx = L.cabS + 14.75 + 1 + 6.5 + P.dxCan, cy0 = 1.5 + P.dyCan, cz0 = P.canBase + P.dzCan;
    L.can = { x0: ccx - P.canW / 2, x1: ccx + P.canW / 2, y0: cy0, y1: cy0 + P.canD, z0: cz0, z1: cz0 + P.canH, cx: ccx };
    // the tray under it: 1/4 in wider each side than the can, 19 1/2 deep (3/4 in behind the can's back, 1 3/4 in past its front), 3/4 in thick on 1/2 in slides
    Object.assign(L.can, { tx0: L.can.x0 - .5, tx1: L.can.x1 + .5, ty0: cy0 - .75, ty1: cy0 + 18.75 });
  }
  // the drain jug stands on the top of the fresh water tank under the sink: centered on the part of the tank that is under the sink, in the middle of the tank's depth, plus how far it was dragged
  L.jug = null;
  if (P.jugOn) {
    const jo0 = Math.max(L.sinkS, L.tankX[0]), jo1 = Math.min(L.sinkE - .75, L.tankX[1]), jcx = (jo1 > jo0 ? (jo0 + jo1) / 2 : (L.sinkS + L.sinkE) / 2) + P.dxJug, jcy = P.tankBack + P.tankD / 2 + P.dyJug, jz0 = P.tankLift + P.tankH + P.dzJug;
    L.jug = { x0: jcx - P.jugD / 2, x1: jcx + P.jugD / 2, y0: jcy - P.jugD / 2, y1: jcy + P.jugD / 2, z0: jz0, z1: jz0 + P.jugH, cx: jcx, cy: jcy };
  }
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
const MOVER_IDS = ['dc0', 'dc1', 'dc2', 'dc3', 'dc4', 'dc5', 'clo_dr', 'clo_hi', 'gear_sh', 'bed', 'dinette', 'flap', 'ledge', 'fridge'];
MOVER_IDS.forEach(ensure);
