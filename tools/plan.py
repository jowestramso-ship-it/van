import re
S=6.0; X0=60; Y0=64
xx=lambda i:X0+S*i; yy=lambda d:Y0+S*d
W=xx(154)+100; H=yy(68)+60
o=[]; a=o.append
a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img"><title>Looking down into the van, both sides</title>')
a('<defs><marker id="arq" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker><pattern id="hq" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#888780" stroke-width="1"/></pattern></defs>')
a(f'<text class="ts" x="{X0}" y="18" style="font-size:13px">Looking down into the van. Rear doors on the left, cab on the right. Driver side wall at the top, passenger side wall at the bottom. Inches.</text>')
a(f'<text class="th" x="{xx(80)}" y="{yy(0)-30}" text-anchor="middle" style="font-size:13px;fill:#444441">DRIVER SIDE WALL</text>')
a(f'<text class="th" x="{xx(80)}" y="{yy(68)+34}" text-anchor="middle" style="font-size:13px;fill:#444441">PASSENGER SIDE WALL</text>')
# grid
for t in range(0,151,10):
    a(f'<line x1="{xx(t)}" y1="{yy(0)}" x2="{xx(t)}" y2="{yy(68)}" stroke="#3F3E3A" stroke-opacity="0.22" stroke-dasharray="3 3"/>')
    a(f'<text x="{xx(t)}" y="{yy(0)-8}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#185FA5">{t}→</text>')
for d in range(0,69,10):
    a(f'<line x1="{xx(0)}" y1="{yy(d)}" x2="{xx(154)}" y2="{yy(d)}" stroke="#3F3E3A" stroke-opacity="0.22" stroke-dasharray="3 3"/>')
    a(f'<text x="{xx(0)-6}" y="{yy(d)+4}" text-anchor="end" style="font-size:10px;font-weight:700;fill:#8A4B0F">{d}↓</text>')
# floor
a(f'<rect x="{xx(0)}" y="{yy(0)}" width="{S*154}" height="{S*68}" fill="#F1EFE8" fill-opacity="0.7" stroke="#5F5E5A" stroke-width="2"/>')
a(f'<text class="ts" x="{xx(0)+3}" y="{yy(68)+14}" style="font-size:10px">rear doors</text>')
# cab wall and allowance
a(f'<rect x="{xx(150)}" y="{yy(0)}" width="{S*4}" height="{S*68}" fill="url(#hq)" fill-opacity="0.35"/>')
a(f'<line x1="{xx(154)}" y1="{yy(0)}" x2="{xx(154)}" y2="{yy(68)}" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="6 3"/>')
a(f'<text class="ts" x="{xx(154)-3}" y="{yy(68)+14}" text-anchor="end" style="font-size:10px">cab wall at 154 (could be off by 2 to 4 in)</text>')
def item(x0,x1,y0,y1,col,label,sub=None,fo=0.14,dash='',fs=11):
    a(f'<rect x="{xx(x0):.1f}" y="{yy(y0):.1f}" width="{S*(x1-x0):.1f}" height="{S*(y1-y0):.1f}" rx="2" fill="{col}" fill-opacity="{fo}" stroke="{col}" stroke-width="1.6" {dash}/>')
    cx=xx((x0+x1)/2); cy=yy((y0+y1)/2)
    a(f'<text class="th" x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" style="font-size:{fs}px;fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px">{label}</text>')
    if sub: a(f'<text class="ts" x="{cx:.1f}" y="{cy+13:.1f}" text-anchor="middle" style="font-size:9.5px;fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px">{sub}</text>')
P='#534AB7'; G='#444441'; K='#993556'; T='#0F6E56'; C='#993C1D'; B='#8A5A00'; W2='#8A6B4D'; BL='#185FA5'
# driver wall cabinets (overhead, dashed)
item(0,74,0,14,P,'',None,0.04,'stroke-dasharray="5 3"')
item(89,154,0,14,P,'',None,0.04,'stroke-dasharray="5 3"')
a(f'<text class="ts" x="{xx(22)}" y="{yy(10.5)}" text-anchor="middle" style="font-size:9px;fill:{P}">overhead cabinet 74 x 14 (bottom 61 up)</text>')
a(f'<text class="ts" x="{xx(120)}" y="{yy(10.5)}" text-anchor="middle" style="font-size:9px;fill:{P}">overhead cabinet 65 x 14 (bottom 61 up)</text>')
# driver side
item(0,74,0,26,P,'Bed / couch','74 x 26, deck 13 1/4, seat top 20',0.12)
item(0,74,26,46,P,'',None,0.05,'stroke-dasharray="6 4"')
a(f'<text class="th" x="{xx(52)}" y="{yy(39)}" text-anchor="middle" style="font-size:10.5px;fill:{P}">bed made up with the leaf: 74 x 46</text>')
a(f'<line x1="{xx(76)}" y1="{yy(12.5)}" x2="{xx(87)}" y2="{yy(12.5)}" stroke="{G}" stroke-width="3.5" stroke-linecap="round"/>')
item(74,89,0,25,G,'Closet','15 x 25, 2 rods',0.14)
item(89,108.5,0,30,K,'Bench','19.5 x 30, seat 17.5 up',0.14)
item(108.5,134.5,0,30,G,'Table','26 x 30, 29 up',0.14)
item(134.5,154,0,30,K,'Bench','19.5 x 30, seat 17.5 up',0.14)
# driver wheel well and battery
item(42,76,0,7,W2,'Wheel well','34 x 7, 7.5 tall',0.5,'',10)
item(52,73,7,17,B,'Battery','21 x 10 x 9.5',0.5,'',10)
a(f'<line x1="{xx(50)}" y1="{yy(0)}" x2="{xx(50)}" y2="{yy(17)}" stroke="#A32D2D" stroke-width="1.5" marker-start="url(#arq)" marker-end="url(#arq)"/><text x="{xx(48.6)}" y="{yy(10)}" text-anchor="end" style="font-size:10px;font-weight:700;fill:#A32D2D">17</text>')
# passenger side (wall at y=68)
item(0,36,44,68,T,'Fold-up shower','36 x 24 open, folds into the side wall',0.08,'stroke-dasharray="6 4"')
item(6,29.75,63.5,68,'#7A4A1E','',None,0.3,'stroke-dasharray="3 2"')
a(f'<text class="ts" x="{xx(18)}" y="{yy(66.7)}" text-anchor="middle" style="font-size:8.5px;fill:#5A3510;paint-order:stroke;stroke:#fff;stroke-width:2.5px">shower nook 4.5 deep</text>')
a(f'<text class="th" x="{xx(66)}" y="{yy(50.5)}" text-anchor="middle" style="font-size:10px;fill:{C};paint-order:stroke;stroke:#fff;stroke-width:3px">Cabinet 21 deep</text>')
a(f'<polygon points="{xx(58):.1f},{yy(47):.1f} {xx(88):.1f},{yy(47):.1f} {xx(103):.1f},{yy(52.25):.1f} {xx(123):.1f},{yy(52.25):.1f} {xx(123):.1f},{yy(68):.1f} {xx(58):.1f},{yy(68):.1f}" fill="{C}" fill-opacity="0.12" stroke="{C}" stroke-width="1.6"/>')
# tall fridge over the passenger wheel well, next to the shower (22 wide along the wall, 19 out)
item(36,58,47,66,'#0A6A8A','',None,0.3)
a(f'<text class="th" x="{xx(47)}" y="{yy(50.5)}" text-anchor="middle" style="font-size:10px;fill:#0A6A8A;paint-order:stroke;stroke:#fff;stroke-width:3px">Fridge 22 x 19 x 48</text>')
item(103,123,52.25,68,C,'Sink','20 x 15 3/4 counter',0.12,'',10)
item(123,152,53,68,'#8A5A00','Fold-out table','29 x 15, 29 up (open)',0.2,'stroke-dasharray="5 3"',10)
item(123,133,52.25,68,'#5A3A00','',None,0.12,'stroke-dasharray="2 2"')
a(f'<text class="ts" x="{xx(128)}" y="{yy(66.7)}" text-anchor="middle" style="font-size:8px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:2.5px">foot ledge 13 x 15</text>')
item(36,58,47,68,'#8A6B4D','',None,0.08,'stroke-dasharray="6 3"')
item(37.75,56.25,56,68,G,'',None,0.2,'stroke-dasharray="4 3"')
a(f'<text class="th" x="{xx(47)}" y="{yy(62.5)}" text-anchor="middle" style="font-size:9px;fill:{G};paint-order:stroke;stroke:#fff;stroke-width:3px">Microwave 18.5 x 12</text>')
item(42,76,61,68,W2,'',None,0.3)
item(81.25,122.25,51.5,68,BL,'',None,0.1,'stroke-dasharray="5 3"')

item(87.25,101.25,52,66,'#C0392B','',None,0.2,'stroke-dasharray="4 3"')
item(59.25,72.25,48,68,'#8A5A00','',None,0.15,'stroke-dasharray="3 2"')
item(73.75,86.75,48,68,'#8A5A00','',None,0.15,'stroke-dasharray="3 2"')
a(f'<text class="ts" x="{xx(73)}" y="{yy(58)}" text-anchor="middle" style="font-size:8.5px;fill:#8A5A00;paint-order:stroke;stroke:#fff;stroke-width:2.5px">7 drawers, 20 deep</text>')
a(f'<text class="ts" x="{xx(94.25)}" y="{yy(65.2)}" text-anchor="middle" style="font-size:8.5px;fill:#C0392B;paint-order:stroke;stroke:#fff;stroke-width:2.5px">hot water tank</text>')
a(f'<circle cx="{xx(111):.1f}" cy="{yy(67.1):.1f}" r="3.5" fill="#185FA5"/>')
item(58,93.25,63.5,68,'#7A4A1E','',None,0.3,'stroke-dasharray="3 2"')
a(f'<text class="ts" x="{xx(66)}" y="{yy(66.7)}" text-anchor="middle" style="font-size:8.5px;fill:#5A3510;paint-order:stroke;stroke:#fff;stroke-width:2.5px">nook 4.5 deep</text>')
a(f'<text class="th" x="{xx(101.75)}" y="{yy(62)}" text-anchor="middle" style="font-size:9.5px;fill:{BL};paint-order:stroke;stroke:#fff;stroke-width:3px">Fresh water tank 41 x 16 1/2</text>')
a(f'<text class="ts" x="{xx(101.75)}" y="{yy(65)}" text-anchor="middle" style="font-size:9px;fill:{BL};paint-order:stroke;stroke:#fff;stroke-width:3px">on the floor, sink end</text>')
a(f'<text class="ts" x="{xx(53)}" y="{yy(66.2)}" text-anchor="middle" style="font-size:9px;fill:#3E230B;paint-order:stroke;stroke:#fff;stroke-width:3px">wheel well 7 out</text>')

# sliding door gap in passenger wall
a(f'<line x1="{xx(104)}" y1="{yy(68)}" x2="{xx(154)}" y2="{yy(68)}" stroke="#BA7517" stroke-width="5" stroke-dasharray="10 5"/>')
a(f'<text class="th" x="{xx(138)}" y="{yy(49.5)}" text-anchor="middle" style="font-size:11px;fill:#854F0B;paint-order:stroke;stroke:#fff;stroke-width:3px">Sliding door opening</text>')
a(f'<text class="ts" x="{xx(138)}" y="{yy(46.5)}" text-anchor="middle" style="font-size:10px;fill:#854F0B;paint-order:stroke;stroke:#fff;stroke-width:3px">51 wide, 104 to 155</text>')
a(f'<text class="ts" x="{xx(138)}" y="{yy(43.5)}" text-anchor="middle" style="font-size:10px;fill:#444441;paint-order:stroke;stroke:#fff;stroke-width:3px">entry 31 clear (blocked by the table)</text>')
# ceiling: lights on the slats and the two cutouts (above the floor, dashed like the other overhead things)
for _lx,_ly in ((20.67,22),(74,22),(127.33,22),(20.67,46),(74,46),(127.33,46)):
    a(f'<circle cx="{xx(_lx):.1f}" cy="{yy(_ly):.1f}" r="{S*1:.1f}" fill="#FFE9A0" fill-opacity="0.9" stroke="#B8860B" stroke-width="1"/>')
item(0.25,14.25,39,53,'#2C2C2A','',None,0.12,'stroke-dasharray="4 3"')
a(f'<text class="ts" x="{xx(7.25):.1f}" y="{yy(39)+10:.1f}" text-anchor="middle" style="font-size:8.5px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">shower fan</text><text class="ts" x="{xx(7.25):.1f}" y="{yy(53)-4:.1f}" text-anchor="middle" style="font-size:8px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">14 x 14</text>')
item(36.375,50.625,26.875,41.125,'#2C2C2A','',None,0.12,'stroke-dasharray="4 3"')
a(f'<text class="ts" x="{xx(43.5):.1f}" y="{yy(34)-2:.1f}" text-anchor="middle" style="font-size:8.5px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">A/C cutout</text><text class="ts" x="{xx(43.5):.1f}" y="{yy(34)+9:.1f}" text-anchor="middle" style="font-size:8px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">14 1/4 x 14 1/4</text>')
# aisle dimensions
def dim(x,y0,y1,txt,col='#A32D2D'):
    a(f'<line x1="{xx(x)}" y1="{yy(y0)}" x2="{xx(x)}" y2="{yy(y1)}" stroke="{col}" stroke-width="1.6" marker-start="url(#arq)" marker-end="url(#arq)"/><text x="{xx(x)+5}" y="{yy((y0+y1)/2)+4}" style="font-size:11px;font-weight:700;fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px">{txt}</text>')
dim(14,26,44,'18 gap in front of the shower')
dim(81.5,25,47,'22 aisle')
dim(60,26,47,'21 aisle')
dim(112,30,52.25,'22 1/4 aisle')
dim(90,30,47.4,'17 aisle (tightest)')
# overall width
a(f'<line x1="{xx(154)+18}" y1="{yy(0)}" x2="{xx(154)+18}" y2="{yy(68)}" stroke="#444441" stroke-width="1.5" marker-start="url(#arq)" marker-end="url(#arq)"/><text x="{xx(154)+24}" y="{yy(34)}" style="font-size:11px;font-weight:700;fill:#444441">68 wide</text>')
a('</svg>')
svg='\n'.join(o)

rows=[('Driver','Bed / couch','0 to 74','74 x 26 (couch), 74 x 46 opened','deck top 13 1/4, seat base 14 (deck + the 3/4 in leaf), seat top 20 by day, bed top 19 1/4 at night','makes up with a hinged leaf: the 20 in leaf (3/4 in plywood, a plain slab with no rails) lies back on the deck, face down, under the seat cushion by day and flips out level with the deck on 4 legs, about 24 in apart (12 5/8 in, 3/8 x 1 1/4 in flat bar, folded into through-slots in the leaf so they are flush) at night, 3 in in from the free edge so they land 43 in out from the wall (1 in short of the front edge of the shower pan, 44 in, when the pan is down); the back cushion (6 in thick, one 20 in piece, 20 in tall) lies on it, 26 + 20 = 46 in wide; the couch sits on a base (end panels, a wall ledger and a rail under the front edge of the deck); no rails or slides, so the space under the deck stays free (12 1/2 in)'),
('Driver','Closet','74 to 89','15 x 25','floor to the finished ceiling (74 3/4; the bare ceiling is 76)','starts right at the end of the bed (no gap); two rods along the wall, one above the other: upper at 71 in up, lower at 36 in up, each about 11 in long (76 to 87); hangers sit across the 25 in depth; about 7 or 8 garments per rod, 14 to 16 in all; short garments only (about 32 in hang on top, 30 below); the last 2 in of the wheel well (74 to 76) sits inside the bottom of the closet'),
('Driver','Dinette bench','89 to 108.5','19.5 x 30','seat 17.5',''),
('Driver','Dinette table','108.5 to 134.5','26 x 30','29',''),
('Driver','Dinette bench','134.5 to 154','19.5 x 30','seat 17.5',''),
('Driver','Overhead cabinets','0 to 74 and 89 to 154','74 x 14 and 65 x 14 (was 18 deep, 12 before that)','13 3/4 tall: bottom 61, top 74 3/4 (flush with the closet and the finished ceiling; 15 tall to the bare 76 before the ceiling covering, and 56 to 69, and 56 to 74 before that)','split by the closet; the 12 in doors sit at 61.5 to 73.5, with a 1 1/4 in rail above them that backs the flip-up hinges (it was 2 1/2 in before the ceiling covering); the bottom is at 61 so a seated 6 ft head clears it: 4 in over the couch (head at 57) and 6 1/2 in over the dinette (54 1/2); only the furring strip S7 (66 in up) is behind the back (S6 at 57 1/4 is below it, S8 at 76 3/4 is just above it), so add a strip at about 62 or 72; the 76 in ceiling is the bare measurement, so the tops follow the finished ceiling (lower after insulation and a ceiling panel); 14 deep loads the furring about 22% less than 18 deep, but still use fasteners into steel'),
('Ceiling','Covering','0 to 154 (160 from the rear doors)','160 x 68 (the width is assumed: measure the flat part of the roof)','1 1/4 thick: 1/4 in plywood against the roof and 1 in slats below it, finished ceiling at 74 3/4 (bare 76)','at least 3 sheets of 1/4 in plywood (pieces 96 x 48, 64 x 48, 96 x 20 and 64 x 20, laid long way) and 17 slats 3 x 1 x 160 with 1 in gaps (1/2 in at each side); each slat needs 14 ft stock (8 in waste); about 190 lb with pine slats, all overhead; the roof bows, wiring and insulation behind the plywood are not counted'),
('Ceiling','Round lights (6)','20 2/3, 74 and 127 1/3 (two rows of three)','2 in across, mounted on the slats','on the slats nearest 22 and 46 in across from the driver wall; surface mounted they hang about 1/2 in below the slats','each centered on a 3 in slat (1/2 in of wood each side), so no slat is cut; a small hole through the plywood behind each for the wire to a switch (wiring not drawn)'),
('Ceiling','Shower fan cutout','1/4 to 14 1/4 (centered at 7 1/4)','14 x 14','through the plywood and the slats, at 39 to 53 in across from the driver wall','its center is over the wet bath (0 to 36, against the passenger wall; 5 in of the opening is past the pan front edge at 44); cuts 4 slats, each ending at a framed curb; the F36AR fan cutout is 356 x 356 mm (14.02 in); framed between the roof bows'),
('Ceiling','Air conditioning cutout','36 3/8 to 50 5/8 (centered at 43 1/2; asked for between 40 and 70 from the rear doors, between the roof ribs at 37 7/8 and 58 3/8 from the rear doors)','14 1/4 x 14 1/4','through the plywood and the slats, at 26 7/8 to 41 1/8 in across (centered)','over the bed and the aisle, clear of the wall cabinets (14 deep, along the driver wall), the microwave shelf on the passenger side and the lights; cuts 5 slats; the model is not chosen (14 1/4 in is the usual opening); its weight and the roof bows are not modeled'),
('Driver','Closet door pockets','74.6 to 88.3 (on the inside of the two closet doors)','pockets about 6 1/2 wide x 7 tall, no more than 3 in deep when full','lower door 5 to 34.5 up (2 columns x 4 rows, 8 pockets); upper door 42 to 64 up (2 x 3, 6 pockets)','14 pockets for socks and underwear; the door is 24 1/4 in from the wall inside and the hangers (17 in wide) fill about 3 1/2 to 20 1/2 from the wall, so a full pocket has only about 3 in before it touches the clothes; keep the upper rows low (reach to about 64); use elastic tops or flaps so the items do not fall out when the upper door flips up and when the van moves'),
('Driver','Closet doors (2, stacked)','74.125 to 88.875','14 3/4 wide x 37 5/8 tall each','0.25 to 37.9 (lower) and 38.1 to 75.75 (upper)','split at 38 so each opens one rod (rods at 36 and 71 up); opened 90 degrees a 14 3/4 in door sticks 14 3/4 in into the 22 in aisle (7 in left), and it cannot open flat against the bed (to 22 up) or the bench (to 17.5 up, backrest to 38 at 89 to 91.9); a flip-up upper door and a bi-fold lower door would project only about 7 1/2 in'),
('Driver','Cabinet doors (3 per cabinet)','0.125 to 73.875 (bed side); 89.125 to 153.875 (dinette side)','bed side 24 1/2 x 12 (three, 1/2 in trimmed off each 25 in door); dinette side 21 1/2 x 12 (three, 3 1/2 in trimmed off each)','61.5 to 73.5 up','landscape, like flip-up doors; 1/8 in gaps between doors and at the ends; positions: bed side 0.125, 24.75, 49.375; dinette side 89.125, 110.75, 132.375; the doors on the two sides are different widths because the cabinets are 74 and 65 long'),
('Driver','Wheel well','42 to 76','34 x 7','7.5 tall','measured; flat top 15.5 long'),
('Driver','Battery','52 to 73','21 x 10','9.5 tall','next to the well, 17 in total depth; 1 in from the closet'),
('Passenger','Shower nook (P1, P2)','6 to 29.75','23.75 long x 4.5 deep','31 to 56.5 up (25.5 tall)','recess in the shower wall: the pans are the body (0 deep) and the planks sit 4.5 in off the body; needs a waterproof lining and a slight slope to the front'),
('Passenger','Fold-up shower','0 to 36','36 x 24 open','folds into the side wall','open only when the bed is folded to 27; folded thickness not given'),
('Passenger','Cabinet / counter','58 to 88, then angled to 103','21 deep to 88, angling in 15 long to 15 3/4 deep at 103 (slope 5 1/4 in over 15 in)','counter 38','the angle starts at the sink and runs back toward the shower'),
('Passenger','Nook (P4 to P7)','58 to 93.25','35.25 long x 4.5 deep','38 to 56.5 up (18.5 tall)','recess in the wall behind the countertop, open above the counter; the pans are the body (0 deep) and the planks sit 4.5 in off the body, so it is 4.5 deep (4 3/8 over the ribs); the part behind the fridge (46 to 58) is not usable; storage: shelf at 45.5 up (3/4 thick) and 2 tiers of 9 quart canning jars (3 3/4 wide, 7 tall), 18 in all; the TV (bottom 54, 76.5 to 103.5) covers its top 2.5 in from 76.5 to 93.25'),
('Passenger','Fridge (tall)','36 to 58','22 x 19','48 tall, on a platform over the wheel well (8.25 to 56.25)','front opening; sits 2 in off the wall so its front is flush with the 21 deep cabinet and shelf; next to the shower'),
('Passenger','Sink','103 to 123','20 wide','counter 38','sits on a flat 15 3/4 deep counter (15 in clear inside behind a 3/4 in door)'),
('Passenger','Shelf over the fridge','36 to 58','22 x 21','top at 59, 2 in above the fridge','21 deep, flush with the cabinet front; the fridge is 19 deep'),
('Passenger','Microwave','37.75 to 56.25','18.5 x 12','10 tall, on the shelf over the fridge (59 to 69)','shelf 2 in above the fridge top (56.25); needs about 2,000 W inverter'),
('Passenger','TV','76.5 to 103.5','27 wide (15.4 is its height; depth not set)','bottom 54, top 69.4','30 in, over the cabinet, clear of the door opening that starts at 104; overlaps the right end of the P4-P7 nook (to 93.25) by about 2 1/2 in at 54 to 56.5 up'),
('Passenger','Fresh water tank','81.25 to 122.25','41 x 16 1/2','10 tall, lying flat on the floor (0 to 10), about 29 1/4 gal (about 244 lb full)','at the sink end against the cab-side end panel (122.25), partly in the sink cabinet (103 to 123) and partly in the open area beside it; the new tank (10 tall, 16 1/2 deep; the earlier one was 41 x 10 x 15 1/2 standing on its side); it is 1 1/2 in too deep for the sink end: the cabinet is 15 in clear inside the 3/4 in door there, so it sticks out 1 1/2 in past the door line from about 98 3/4 in to its end (it clears the door from 88 to 98 3/4); the sink plumbing (111 in from the back) has no room in front of it; clear of the wheel well (ends at 76); the part from 104 to 122 stands in front of the sliding door opening (104 to 155), as the sink cabinet does'),
('Passenger','Drawers (2, side by side)','59.25 to 72.25 and 73.75 to 86.75','13 x 20 each','4 tall, 31.25 to 35.25 up','under the counter in the flat part (58 to 88), over the wheel well and the hot water tank; the left drawer holds the 12 x 14 x 3 silverware tray; none at the angle'),
('Passenger','Lower drawers (5: two 5 in on the cab side; a 5 in over two 7 1/2 in toward the back)','73.75 to 86.75 (cab side); 59.25 to 72.25 (toward the back, to the right in diagram E)','13 x 20 each','cab side: two 5 tall, 20 to 25 and 26 to 31 (rail 25 to 25.75), 8 3/4 in open below them down to the shelf at 10 1/2 to 11 1/4 (1/2 in over the fresh tank top at 10); back side: 5 tall at 26 to 31, 7 1/2 tall at 17 1/2 to 25 and 7 1/2 tall at 9 to 16 1/2 (rails at 25 to 25.75 and 16 1/2 to 17.25), on its own shelf at 8 to 8.75 (1/2 in over the wheel well, 7.5 tall)','under the top pair; 20 deep so they reach back to the wall over the tank and the wheel well'),
('Passenger','Hot water tank','87.25 to 101.25','14 x 14','13 tall, on a 3/4 in shelf over the fresh water tank (16.75 to 29.75, 6 in over the tank top at 10)','at the end of the drawers (87.25) and short of the sink cabinet (103), so it clears the sink bowl; the hot and cold fittings and the relief valve are at its back, so it needs a 1 5/8 in gap to the wall and its front is 15 5/8 in from the wall, which just fits the 15 5/8 in the angled front leaves clear inside the door at its sink end (no spare); 6 3/4 in under the counter for its fittings and relief valve; the shelf is carried by the cabinet sides, not by the tank; holds about 4 gal (33 lb of water); the heater itself weighs 2 lb, so about 35 lb full; 14 x 14 x 13 is its outside size; electric, so no vent or combustion air; 120 V AC, 1,440 W (12 A: a 20 A circuit on 12 AWG, or a 15 A circuit on 14 AWG right at its limit, and about 133 A at 12 V through an inverter of 2,000 W or more from the 280 Ah battery, which is close: the battery is at 52 to 73); fittings, access, the relief valve and the drain are not set yet'),
('Passenger','Wheel well','42 to 76','34 x 7','7.5 tall','same as the driver side (flat top 15.5 long)'),
('Passenger','Sliding door','104 to 155','51 opening, 59 panel','up to 58','only the rear edge is measured'),
('Passenger','Fold-out table','123 to 152','29 long x 15 deep (3/4 thick)','29 up (hinged on the sink cabinet end, folds down against it)','reaches the passenger seat when it is turned to face the back; carried by a folding brace (a diagonal arm hinged on the cabinet end, 13 in below the board, locking 15 3/4 in out), not a floor leg, because the knees and shins of the rotated seat are at the free end; closes off the entry while open; length may need to be shorter, it should stop in front of the belly'),
('Passenger','Foot ledge','123 to 136','13 long x 15 3/4 wide (3/4 thick, flat, no lip); its outer edge is 13 in from the cabinet end','top at 8 1/2 up, flat, 8 1/2 in below the 17 in cab seat cushion','hinged on the cabinet end under the table, folds up into a 3/4 in recess in the end panel behind the folded table; small folding brace; the base of the sink cabinet is full (fresh water tank), so it cannot slide out of the base'),
('Passenger','Entry','123 to 154','31 clear (about 30 with the table folded down)','','behind the passenger seat; closed off while the table is open'),
('Under the van','Grey water tank','not set','30 x 17 x 8 space (was 24 x 17 x 8)','','shower and sink (grey water only); both drains run down through the floor; no off-the-shelf tank found that fits; size to be chosen; toilet waste (black water) is not covered'),
('Aisles','Bed to counter','','21 across (couch, 26 deep), 22 with the bed opened to 46 in','',''),
('Aisles','Dinette to counter','','17 at 89 to 90 (tightest, where the counter is 21 deep), 23 from 103','','across from the closet it is 22'),
('Aisles','Closet to cabinet','','22 across','',''),
('Aisles','Shower to bed','','19 across','','where the fold-up shower opens')]
tbl='<table><tr><th>Side</th><th>Item</th><th>Along the wall (in from the back)</th><th>Size, along x out (in)</th><th>Height (in)</th><th>Notes</th></tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table>'
blk='<h2>3. Looking down into the van, both sides</h2>\n<div class="wide">'+svg+'</div>\n<p>Every item is drawn from the sizes in your notes. The across numbers add up: shower 24 + 18 gap + bed 26 = 68, bed 26 + 21 aisle + counter 21 = 68, and dinette 30 + 22 1/4 aisle + sink counter 15 3/4 = 68. Dashed outlines are above the floor (overhead cabinets, microwave, the ceiling fan and air conditioning cutouts; the round yellow dots are the ceiling lights). The grey water tank goes under the van and is not drawn. The fresh water tank (dashed blue, 41 x 16 1/2) is on the floor at the sink end, partly in the sink cabinet (which is open to the area beside it), and the hot water tank (dashed red, 14 x 14, 13 tall) is on a shelf over the fresh water tank, 87 1/4 to 101 1/4 in, just before the sink cabinet, with a 1 5/8 in gap behind it to the wall for its fittings and relief valve. The bed (74 long) rolls out to 46 in wide (dashed, 26 in bed depth + the 20 in back): the tall fridge (19 deep, sitting 2 in off the wall so its front is flush with the cabinet) and the cabinet (21 deep) each leave 1 in, and the shower folds into the side wall so it does not count while the bed is out. The fold-out table (dashed, 29 x 15, at the cab-side end of the sink cabinet) is drawn open with the foot ledge (10 x 15 3/4) under it; folded, the table hangs against the cabinet end and the ledge folds into a recess in it. The passenger wheel well matches the driver side, and the sliding door is only measured at its rear edge. Everything is measured from the same zero, 6 in in from the back (the rear lip is not counted), and the cab wall is at 154 in, which can be off by 2 to 4 in. The sliding door opening (104 to 155) runs 1 in past the cab wall.</p>\n'+tbl+'\n'
html=open((ROOT+'/sides.html')).read()
if '<h2>3. Looking down into the van' in html:
    i=html.index('<h2>3. Looking down into the van'); j=html.index('<h2>Driver side photos</h2>')
    html=html[:i]+html[j:]
html=html.replace('<h2>Driver side photos</h2>',blk+'<h2>Driver side photos</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)

# ---- drop the battery looking-down picture and depth sections A, B, C ----
html=open((ROOT+'/sides.html')).read()
if '<h4>Battery next to the wheel well, looking down</h4>' in html:
    i=html.index('<h4>Battery next to the wheel well, looking down</h4>'); j=html.index('<h2>Depth sections</h2>')
    html=html[:i]+html[j:]
if '<h3>A. Through T3' in html:
    i=html.index('<h3>A. Through T3'); j=html.index('<h3>D. How the lower wall steps in')
    html=html[:i]+html[j:]
html=html.replace(" The looking-down view below shows the depths.","")
html=html.replace("<h2>Depth sections</h2>","<h2>Depth section</h2>")
open((ROOT+'/sides.html'),'w').write(html)

# ---- also drop depth section D (and the now-empty Depth section heading) ----
html=open((ROOT+'/sides.html')).read()
if '<h3>D. How the lower wall steps in' in html:
    i=html.index('<h2>Depth section</h2>'); j=html.index('<h2>2. Passenger side</h2>')
    html=html[:i]+html[j:]
open((ROOT+'/sides.html'),'w').write(html)
