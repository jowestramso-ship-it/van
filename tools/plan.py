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
a(f'<text class="ts" x="{xx(22)}" y="{yy(10.5)}" text-anchor="middle" style="font-size:9px;fill:{P}">overhead cabinet 74 x 14 (bottom 63 up)</text>')
a(f'<text class="ts" x="{xx(120)}" y="{yy(10.5)}" text-anchor="middle" style="font-size:9px;fill:{P}">overhead cabinet 65 x 14 (bottom 63 up)</text>')
# driver side
item(0,74,0,26,P,'Bed / couch',f'74 x 26, deck {fr8(DECK_T)}, seat top {fr8(SEAT_T)}',0.12)
item(0,74,26,46,P,'',None,0.05,'stroke-dasharray="6 4"')
a(f'<text class="th" x="{xx(52)}" y="{yy(39)}" text-anchor="middle" style="font-size:10.5px;fill:{P}">bed made up with the leaf: 74 x 46</text>')
a(f'<line x1="{xx(76)}" y1="{yy(12.5)}" x2="{xx(87)}" y2="{yy(12.5)}" stroke="{G}" stroke-width="3.5" stroke-linecap="round"/>')
item(74,89,0,25,G,'Closet','15 x 25, 1 rod, drawers under',0.14)
item(89,108.5,0,28,K,'Bench','19.5 x 28, seat 17.5 up',0.14)
item(108.5,134.5,0,28,G,'Table','26 x 28, 29 up',0.14)
item(134.5,154,0,28,K,'Bench','19.5 x 28, seat 17.5 up',0.14)
# driver wheel well and battery
item(42,76,0,7,W2,'Wheel well','34 x 7, 7.5 tall',0.5,'',10)
item(52,73,7,17,B,'Battery','21 x 10 x 9.5',0.5,'',10)
item(SH_X0,SH_X1,SH_Y0,SH_Y1,W2,'',None,0.12,'stroke-dasharray="5 3"')
item(INV['x0'],INV['x1'],INV['y0'],INV['y1'],'#B45309','Inverter',f"{fr8(14.8)} x {fr8(7.7)}",0.22,'stroke-dasharray="3 2"',9)
item(DC['x0'],DC['x1'],DC['y0'],DC['y1'],'#B45309','DC-DC','16 x 9',0.22,'stroke-dasharray="3 2"',9)
item(CHG['x0'],CHG['x1'],CHG['y0'],CHG['y1'],'#B45309','Charger','9.5 x 7',0.22,'stroke-dasharray="3 2"',9)
item(SH_X0,SH_X1,SH_Y0+SH_PULL,SH_Y1+SH_PULL+.75,W2,'',None,0.06,'stroke-dasharray="2 3"')
a(f'<text class="th" x="{xx((SH_X0+SH_X1)/2)}" y="{yy((SH_Y0+SH_Y1)/2+SH_PULL)}" text-anchor="middle" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">gear shelf pulled out {SH_PULL} in</text>')
a(f'<line x1="{xx(50)}" y1="{yy(0)}" x2="{xx(50)}" y2="{yy(17)}" stroke="#A32D2D" stroke-width="1.5" marker-start="url(#arq)" marker-end="url(#arq)"/><text x="{xx(48.6)}" y="{yy(10)}" text-anchor="end" style="font-size:10px;font-weight:700;fill:#A32D2D">17</text>')
# passenger side (wall at y=68)
item(0,36,44,68,T,'',None,0.08,'stroke-dasharray="6 4"')
a(f'<text class="th" x="{xx(10.4)}" y="{yy(55)}" text-anchor="middle" style="font-size:11px;fill:{T};paint-order:stroke;stroke:#fff;stroke-width:3px">Shower</text><text class="ts" x="{xx(10.4)}" y="{yy(55)+13}" text-anchor="middle" style="font-size:9.5px;fill:{T};paint-order:stroke;stroke:#fff;stroke-width:3px">36 x 24, fixed pan</text>')
item(20.75,35.25,48.75,63.25,K,'Toilet','Fold-To-Go 14 1/2',0.2,'',9)
for _w0,_w1,_d0,_d1,_n in ((88.25,89,0,28,'W1'),(154,154.75,0,28,'W2'),(35.25,36,44,68,'W3'),(58,58.75,47,68,'W4')):
    item(_w0,_w1,_d0,_d1,W2,'',None,0.85)
    a(f'<text class="ts" x="{xx((_w0+_w1)/2)}" y="{yy(_d1)+11 if _d0==0 else yy(_d0)-4}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:#5A3A00">{_n}</text>')
item(6,29.75,63.5,68,'#7A4A1E','',None,0.3,'stroke-dasharray="3 2"')
a(f'<text class="ts" x="{xx(18)}" y="{yy(66.7)}" text-anchor="middle" style="font-size:8.5px;fill:#5A3510;paint-order:stroke;stroke:#fff;stroke-width:2.5px">shower nook 4.5 deep</text>')
a(f'<text class="th" x="{xx(66)}" y="{yy(50.5)}" text-anchor="middle" style="font-size:10px;fill:{C};paint-order:stroke;stroke:#fff;stroke-width:3px">Cabinet 21 deep</text>')
a(f'<polygon points="{xx(58):.1f},{yy(47):.1f} {xx(88):.1f},{yy(47):.1f} {xx(103):.1f},{yy(51):.1f} {xx(123):.1f},{yy(51):.1f} {xx(123):.1f},{yy(68):.1f} {xx(58):.1f},{yy(68):.1f}" fill="{C}" fill-opacity="0.12" stroke="{C}" stroke-width="1.6"/>')
# tall fridge over the passenger wheel well, next to the shower (22 wide along the wall, 19 out)
item(36,58,47,66,'#0A6A8A','',None,0.3)
a(f'<text class="th" x="{xx(47)}" y="{yy(50.5)}" text-anchor="middle" style="font-size:10px;fill:#0A6A8A;paint-order:stroke;stroke:#fff;stroke-width:3px">Fridge 22 x 19 x 48</text>')
item(103,123,51,68,C,'Sink','20 x 17 counter',0.12,'',10)
item(123,152,53,68,'#8A5A00','Fold-out table','29 x 15, 29 up (open)',0.2,'stroke-dasharray="5 3"',10)
item(123,133,51,68,'#5A3A00','',None,0.12,'stroke-dasharray="2 2"')
a(f'<text class="ts" x="{xx(128)}" y="{yy(66.7)}" text-anchor="middle" style="font-size:8px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:2.5px">foot ledge 13 x 17</text>')
item(36,58,47,68,'#8A6B4D','',None,0.08,'stroke-dasharray="6 3"')
item(37.75,56.25,56,68,G,'',None,0.2,'stroke-dasharray="4 3"')
a(f'<text class="th" x="{xx(47)}" y="{yy(62.5)}" text-anchor="middle" style="font-size:9px;fill:{G};paint-order:stroke;stroke:#fff;stroke-width:3px">Microwave 18.5 x 12</text>')
item(42,76,61,68,W2,'',None,0.3)
item(87.25,122.25,52,68,BL,'',None,0.1,'stroke-dasharray="5 3"')
_n=(0.2577,-0.9662)
def _P(x,off):
    return (x+off*_n[0], 47+0.2667*(x-88)+off*_n[1])
_roll=[_P(91.5,-0.5),_P(102.5,-0.5),_P(102.5,-6),_P(91.5,-6)]
a('<polygon points="'+' '.join(f'{xx(x):.1f},{yy(y):.1f}' for x,y in _roll)+'" fill="#B07A2A" fill-opacity="0.35" stroke="#8A5A00" stroke-width="1.2"/>')
a(f'<text class="ts" x="{xx(106)}" y="{yy(47.2)}" text-anchor="middle" style="font-size:8.5px;fill:#8A5A00;paint-order:stroke;stroke:#fff;stroke-width:2.5px">paper towels (recessed, high)</text>')

item(87.25,101.25,52,66,'#C0392B','',None,0.2,'stroke-dasharray="4 3"')
item(59.25,72.25,48,68,'#8A5A00','',None,0.15,'stroke-dasharray="3 2"')
item(73.75,86.75,48,68,'#8A5A00','',None,0.15,'stroke-dasharray="3 2"')
a(f'<text class="ts" x="{xx(66)}" y="{yy(58)}" text-anchor="middle" style="font-size:8.5px;fill:#8A5A00;paint-order:stroke;stroke:#fff;stroke-width:2.5px">5 drawers, 20 deep</text>')
# the trash can on its pull-out in the cab-side column (12 x 16, 74 1/4 to 86 1/4 in from the back, 1 1/2 to 17 1/2 in out from the wall), shut
item(74.25,86.25,50.5,66.5,'#5F5E5A','',None,0.28)
a(f'<text class="ts" x="{xx(80.25)}" y="{yy(58.7)}" text-anchor="middle" style="font-size:8.5px;fill:#5F5E5A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">13 gal can</text>')
a(f'<text class="ts" x="{xx(94.25)}" y="{yy(65.2)}" text-anchor="middle" style="font-size:8.5px;fill:#C0392B;paint-order:stroke;stroke:#fff;stroke-width:2.5px">hot water tank</text>')
item(58,93.25,63.5,68,'#7A4A1E','',None,0.3,'stroke-dasharray="3 2"')
a(f'<text class="ts" x="{xx(66)}" y="{yy(66.7)}" text-anchor="middle" style="font-size:8.5px;fill:#5A3510;paint-order:stroke;stroke:#fff;stroke-width:2.5px">nook 4.5 deep</text>')
a(f'<text class="th" x="{xx(104.75)}" y="{yy(62)}" text-anchor="middle" style="font-size:9.5px;fill:{BL};paint-order:stroke;stroke:#fff;stroke-width:3px">Fresh water tank 35 x 16</text>')
a(f'<text class="ts" x="{xx(104.75)}" y="{yy(65)}" text-anchor="middle" style="font-size:9px;fill:{BL};paint-order:stroke;stroke:#fff;stroke-width:3px">on the floor, sink end</text>')
# the drain jug (5 gallon bottle) seen from above, on the sink end of the fresh tank
a(f'<circle cx="{xx(112.625):.1f}" cy="{yy(60):.1f}" r="{S*5.375:.1f}" fill="#A9D4F5" fill-opacity="0.3" stroke="{BL}" stroke-width="1.6"/>')
a(f'<circle cx="{xx(112.625):.1f}" cy="{yy(60):.1f}" r="{S*1.06:.1f}" fill="none" stroke="{BL}" stroke-width="1"/>')
a(f'<text class="ts" x="{xx(112.625):.1f}" y="{yy(67.3):.1f}" text-anchor="middle" style="font-size:8.5px;fill:{BL};paint-order:stroke;stroke:#fff;stroke-width:3px">drain jug 10 3/4 across</text>')
a(f'<text class="ts" x="{xx(53)}" y="{yy(66.2)}" text-anchor="middle" style="font-size:9px;fill:#3E230B;paint-order:stroke;stroke:#fff;stroke-width:3px">wheel well 7 out</text>')

# sliding door gap in passenger wall
a(f'<line x1="{xx(104)}" y1="{yy(68)}" x2="{xx(154)}" y2="{yy(68)}" stroke="#BA7517" stroke-width="5" stroke-dasharray="10 5"/>')
a(f'<text class="th" x="{xx(138)}" y="{yy(49.5)}" text-anchor="middle" style="font-size:11px;fill:#854F0B;paint-order:stroke;stroke:#fff;stroke-width:3px">Sliding door opening</text>')
a(f'<text class="ts" x="{xx(138)}" y="{yy(46.5)}" text-anchor="middle" style="font-size:10px;fill:#854F0B;paint-order:stroke;stroke:#fff;stroke-width:3px">51 wide, 104 to 155</text>')
a(f'<text class="ts" x="{xx(138)}" y="{yy(43.5)}" text-anchor="middle" style="font-size:10px;fill:#444441;paint-order:stroke;stroke:#fff;stroke-width:3px">entry 31 clear (blocked by the table)</text>')
# ceiling: the two lights (shower, and countertop and sink together) on the slats and the two cutouts (above the floor, dashed like the other overhead things)
for _lx,_ly in ((20.5,58),(89.375,58)):
    a(f'<circle cx="{xx(_lx):.1f}" cy="{yy(_ly):.1f}" r="{S*1:.1f}" fill="#FFE9A0" fill-opacity="0.9" stroke="#B8860B" stroke-width="1"/>')
item(0.25,14.25,27,41,'#2C2C2A','',None,0.12,'stroke-dasharray="4 3"')
a(f'<text class="ts" x="{xx(7.25):.1f}" y="{yy(27)+10:.1f}" text-anchor="middle" style="font-size:8.5px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">roof fan</text><text class="ts" x="{xx(7.25):.1f}" y="{yy(41)-4:.1f}" text-anchor="middle" style="font-size:8px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">14 x 14</text>')
item(36.375,50.625,26.875,41.125,'#2C2C2A','',None,0.12,'stroke-dasharray="4 3"')
a(f'<text class="ts" x="{xx(43.5):.1f}" y="{yy(34)-2:.1f}" text-anchor="middle" style="font-size:8.5px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">A/C cutout</text><text class="ts" x="{xx(43.5):.1f}" y="{yy(34)+9:.1f}" text-anchor="middle" style="font-size:8px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.5px">14 1/4 x 14 1/4</text>')
# aisle dimensions
def dim(x,y0,y1,txt,col='#A32D2D'):
    a(f'<line x1="{xx(x)}" y1="{yy(y0)}" x2="{xx(x)}" y2="{yy(y1)}" stroke="{col}" stroke-width="1.6" marker-start="url(#arq)" marker-end="url(#arq)"/><text x="{xx(x)+5}" y="{yy((y0+y1)/2)+4}" style="font-size:11px;font-weight:700;fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px">{txt}</text>')
dim(14,26,44,'18 gap in front of the shower')
dim(81.5,25,47,'22 aisle')
dim(60,26,47,'21 aisle')
dim(112,28,51,'23 aisle')
dim(90,28,47.4,'19 1/4 aisle (tightest)')
# overall width
a(f'<line x1="{xx(154)+18}" y1="{yy(0)}" x2="{xx(154)+18}" y2="{yy(68)}" stroke="#444441" stroke-width="1.5" marker-start="url(#arq)" marker-end="url(#arq)"/><text x="{xx(154)+24}" y="{yy(34)}" style="font-size:11px;font-weight:700;fill:#444441">68 wide</text>')
a('</svg>')
svg='\n'.join(o)

rows=[('Driver','Bed / couch','0 to 74','74 x 26 (couch), 74 x 46 opened','deck top 16 3/4, seat base 17 1/2 (deck + the 3/4 in leaf), seat top 22 1/2 by day, bed top 21 3/4 at night (raised 3 1/2 in from 13 1/4 / 14 / 20 / 19 1/4 so the gear shelf fits over the battery, with the cushions cut from 6 in to 5 in to keep the headroom)','makes up with a hinged leaf: the 20 in leaf (3/4 in plywood, a plain slab with no rails) lies back on the deck, face down, under the seat cushion by day and flips out level with the deck on 4 legs, about 24 in apart (12 5/8 in of 3/8 x 1 1/4 in flat bar folded into through-slots in the leaf so they are flush, plus a 3 1/2 in screw-out foot, 16 1/8 in standing) at night, 3 in in from the free edge so they land 43 in out from the wall (1 in short of the front edge of the shower pan, 44 in, when the pan is down); the back cushion (5 in thick, one 20 in piece, 20 in tall) lies on it, 26 + 20 = 46 in wide; the couch sits on a base (end panels, a wall ledger and a rail under the front edge of the deck); no rails or slides under the deck; the space under it is 16 in, with the gear shelf over the battery (see the gear shelf row)'),
('Driver','Closet','74 to 89','15 x 25','floor to the finished ceiling (74 9/16; the bare ceiling is 75 1/2)','starts right at the end of the bed (no gap); ONE rod along the wall at 71 in up, about 11 in long (76 to 87); clothes up to 36 in long hang to 31 1/2 in up; four drawers under them (1 to 30 1/2 up, each 7 5/16 tall x 12 1/2 wide x 22 deep inside); the last 2 in of the wheel well (74 to 76) sits inside the bottom of the closet'),
('Driver','Dinette bench','89 to 108.5','19.5 x 28 (was 30)','seat 17.5',''),
('Driver','Dinette table','108.5 to 134.5','26 x 28 (was 30)','29',''),
('Driver','Dinette bench','134.5 to 154','19.5 x 28 (was 30)','seat 17.5',''),
('Driver','Overhead cabinets','0 to 74 and 89 to 154','74 x 14 and 65 x 14 (was 18 deep, 12 before that)','11 9/16 tall: bottom 63, top 74 9/16 (flush with the closet and the finished ceiling; raised 2 in from 61, so 2 in shorter: they were 13 9/16 tall, 14 1/16 and 15 before the ceiling covering, and 56 to 69, and 56 to 74 before that)','split by the closet; the 10 in doors sit at 63.5 to 73.5, with a 1 1/16 in rail above them that backs the flip-up hinges; the bottom is at 63 so a seated 6 ft head has to clear it: 3 1/2 in over the couch (head at 59 1/2 with the 5 in cushion and the couch raised; it was 4 in at 57), 8 1/2 in over the dinette (54 1/2); only the furring strip S7 (66 in up) is behind the back (S6 at 57 1/4 is below it, S8 at 76 3/4 is just above it), so add a strip at about 64 or 72; the 76 in ceiling is the bare measurement, so the tops follow the finished ceiling (lower after insulation and a ceiling panel); 14 deep loads the furring about 22% less than 18 deep, but still use fasteners into steel'),
('Ceiling','Covering','0 to 154 (160 from the rear doors)','160 x 62 (the flat part of the roof, centered in the van: 3 in each side)','15/16 thick: 3/16 in plywood against the roof and 3/4 in cedar slats below it, finished ceiling at 75 1/16 (bare 76)','at least 3 sheets of 3/16 in plywood (pieces 96 x 48, 64 x 48, 96 x 14 and 64 x 14, laid long way) and 15 slats 3 x 3/4 x 160 with 1 in gaps (1 1/2 in at each side); each slat needs 14 ft stock (8 in waste); about 109 lb with cedar slats, all overhead; the roof bows, wiring and insulation behind the plywood are not counted'),
('Ceiling','Round lights (2)','20 1/2 (shower) and 89 3/8 (over the countertop and sink together)','2 in across, mounted on the slats','on the slat at 58 in across from the driver wall; surface mounted they hang about 1/2 in below the slats','the only ceiling lights; each centered on a 3 in slat (1/2 in of wood each side) and 2 in clear of the ribs, so no slat is cut; a small hole through the plywood behind each for the wire; the shower one is wet rated (IP65)'),
('Ceiling','Roof fan cutout','1/4 to 14 1/4 (centered at 7 1/4)','14 x 14','through the plywood and the slats, at 27 to 41 in across from the driver wall (the middle of the van)','in the middle of the van, not over the wet bath, as you decided; 1 1/2 in clear of the roof rib at 21 3/4 from the rear doors; cuts 5 slats, each ending at a framed curb; the F36AR fan cutout is 356 x 356 mm (14.02 in); framed between the roof bows'),
('Ceiling','Air conditioning cutout','36 3/8 to 50 5/8 (centered at 43 1/2; asked for between 40 and 70 from the rear doors, between the roof ribs at 37 7/8 and 58 3/8 from the rear doors)','14 1/4 x 14 1/4','through the plywood and the slats, at 26 7/8 to 41 1/8 in across (centered)','over the bed and the aisle, clear of the wall cabinets (14 deep, along the driver wall), the microwave shelf on the passenger side and the lights; cuts 5 slats; the model is not chosen (14 1/4 in is the usual opening); its weight and the roof bows are not modeled'),
('Driver','Closet door pockets','74.6 to 88.3 (on the inside of the upper closet door)','pockets about 6 1/2 wide x 7 tall, no more than 3 in deep when full','upper door 34.65 to 56.65 up (2 columns x 3 rows, 6 pockets)','14 pockets for socks and underwear; the door is 24 1/4 in from the wall inside and the hangers (17 in wide) fill about 3 1/2 to 20 1/2 from the wall, so a full pocket has only about 3 in before it touches the clothes; keep the upper rows low (reach to about 64); use elastic tops or flaps so the items do not fall out when the upper door flips up and when the van moves'),
('Driver','Closet door (1) and drawers (4)','74.125 to 88.875','14 3/4 wide: the door 43 11/16 tall, each drawer front 7 5/16 tall','door 30.65 to 74.25 up; drawers 1 to 30 1/2 up','changed (user: hung clothes 36 in long on top, drawers under): the rod at 71 up, the 36 in garments hang to 31 1/2, the drawers fill the space under them; there is no lower rod or lower door any more. Opened 90 degrees the 14 3/4 in door sticks 14 3/4 in into the 22 in aisle; a drawer pulled all the way out is 21 in and leaves about 1 in'),
('Driver','Cabinet doors (3 per cabinet)','0.125 to 73.875 (bed side); 89.125 to 153.875 (dinette side)','bed side 24 1/2 x 10 (three, 1/2 in trimmed off each 25 in door); dinette side 21 1/2 x 10 (three, 3 1/2 in trimmed off each)','63.5 to 73.5 up (they were 12 tall at 61.5 to 73.5)','landscape, like flip-up doors; 1/8 in gaps between doors and at the ends; positions: bed side 0.125, 24.75, 49.375; dinette side 89.125, 110.75, 132.375; the doors on the two sides are different widths because the cabinets are 74 and 65 long'),
('Driver','Wheel well','42 to 76','34 x 7','7.5 tall','measured; flat top 15.5 long'),
('Driver','Battery','52 to 73','21 x 10','9.5 tall','next to the well, 17 in total depth; 1 in from the closet'),
('Passenger','Shower head and valve','head 9, valve 33 (the stall is 0 to 36)','head on a 6 in arm, pointing into the stall','head 70 up, valve 44 up (the pan is fixed, with a 3 in curb)','added later; the head is toward the rear and the valve at the cab end, where the hot and cold lines arrive from the hot water tank; positions are adjustable in the interactive plan. The static drawings E and F do not show them yet'),
('Passenger','Shower nook (P1, P2)','12.5 to 29.75','17.25 long x 4.5 deep','38 to 54 up (16 tall), with a 1 1/2 in lip along the front of the floor to keep things in','recess in the shower wall: the pans are the body (0 deep) and the planks sit 4.5 in off the body; needs a waterproof lining and a slight slope to the front (leave a gap or notch in the lip so water drains)'),
('Passenger','Shower (fixed pan)','0 to 36','36 x 24','fixed pan with a 3 in curb, curtain on the aisle side','the pan does not tip; the drain is in the middle of the standing part (8 5/8 in along, 12 out) and runs straight down through the floor to the grey water tank under the van'),
('Passenger','Toilet (Reliance Fold-To-Go)','20.75 to 35.25','14 1/2 deep x 14 1/2 wide','seat about 14 1/2 up (it stands on the pan, 3.8 up)','left set up in the stall, sideways, its back against W3; 20 3/4 in of floor in front, 4 3/4 in each side; a folding seat on four legs holding a bag, so no tank, vent or drain'),
('Passenger','Shower nook contents','12.5 to 29.75','towel bar 5 in long; a shelf board; two toilet paper rolls and three bottles','bar 50 1/2 up; shelf top 43 3/4; rolls 38 to 42 1/2; bottles 43 3/4 up to about 53','towel bar in the rear 6 in of the nook, the shelf and bottles in the rest, the paper (one in use, one spare) under the shelf; the paper is about 18 in along the wall from the shower head, so it needs a small hinged door or a lidded holder'),
('Passenger','Floor-to-ceiling wall W3 (shower and fridge)','35.25 to 36','3/4 thick x 24 out from the wall','floor to the finished ceiling','the end wall of the shower, between it and the fridge; inside the 36 in pan length'),
('Passenger','Floor-to-ceiling wall W4 (fridge and counter)','58 to 58.75','3/4 thick x 21 out from the wall','floor to the finished ceiling','the end panel of the counter cabinet; the shelves under the back-side drawers start 3/4 in later to meet it'),
('Driver','Floor-to-ceiling wall W1 (closet end)','88.25 to 89','3/4 thick x 28 out from the wall','floor to the finished ceiling','the closet\'s cab-side end panel, carried out to the bench depth (3 in past the closet front); the back of the rear dinette bench leans on it'),
('Driver','Floor-to-ceiling wall W2 (behind the driver seat)','154 to 154.75','3/4 thick x 28 out from the wall','floor to the finished ceiling','its face is at the cab wall mark (which could be off by 2 to 4 in); the back of the cab-end bench leans on it; the dinette light switch goes on it'),
('Passenger','Cabinet / counter','58 to 88, then angled to 103','21 deep to 88, angling in 15 long to 17 deep at 103 (slope 4 in over 15 in)','counter 38','the angle starts at the sink and runs back toward the shower'),
('Passenger','Nook (P6, P7)','76 to 93.25','17.25 long x 4.5 deep','38 to 54 up (16 tall, its top level with the bottom of the TV)','recess in the wall behind the countertop, open above the counter; the pans are the body (0 deep) and the planks sit 4.5 in off the body, so it is 4.5 deep (4 3/8 over the ribs); the part behind the fridge (46 to 58) is not usable; storage: shelf at 45.5 up (3/4 thick) and 2 tiers of 4 quart canning jars (3 3/4 wide, 7 tall), 8 in all; the TV (bottom 54, 76.5 to 103.5) sits right on top of its end, so the top row of jars has about 3/4 in under the nook top'),
('Passenger','Fridge (tall)','36 to 58','22 x 19','48 tall, on a platform over the wheel well (8.25 to 56.25)','front opening; sits 2 in off the wall so its front is flush with the 21 deep cabinet and shelf; next to the shower'),
('Passenger','Sink','103 to 123','20 wide','counter 38','sits on a flat 17 deep counter (16 1/4 in clear inside behind a 3/4 in door; the 16 in deep fresh water tank fits it with 1/4 in to spare)'),
('Passenger','Shelf over the fridge','36 to 58','22 x 21','top at 59, 2 in above the fridge','21 deep, flush with the cabinet front; the fridge is 19 deep'),
('Passenger','Microwave','37.75 to 56.25','18.5 x 12','10 tall, on the shelf over the fridge (59 to 69)','shelf 2 in above the fridge top (56.25); needs about 2,000 W inverter'),
('Passenger','TV','76.5 to 103.5','27 wide (15.4 is its height; depth not set)','bottom 54, top 69.4','30 in, over the cabinet, clear of the door opening that starts at 104; its bottom (54) is level with the top of the P4-P7 nook (to 93.25), so it does not overlap it'),
('Passenger','Fresh water tank','87.25 to 122.25','35 x 16','10 tall, lying flat on the floor (0 to 10), about 24 gal (about 202 lb full)','at the sink end against the cab-side end panel (122.25), partly in the sink cabinet (103 to 123) and partly in the open area beside it; the new tank (10 tall, 16 deep; it was 41 long, but the cab-side column under the counter needs the floor for the trash can, so it starts at 87 1/4, where the hot water tank on its shelf starts); it fits the sink end, which is 17 deep (16 1/4 in clear inside the 3/4 in door), with 1/4 in to spare in front of it (there is no sink pipe: the sink drains into the 5 gallon bottle standing on the tank under the sink, see the next row); clear of the wheel well (ends at 76); the part from 104 to 122 stands in front of the sliding door opening (104 to 155), as the sink cabinet does'),
('Passenger','Drain jug (5 gallon water bottle)','107 1/4 to 118','10 3/4 across (round), 19 1/2 tall','10 to 29 1/2 up, standing on the fresh water tank: 1 in under the sink (underside at 30 1/2, a guess for the 7 1/2 in deep sink)','the sink drains into it (no sink pipe), centered on the sink end of the tank, 2 5/8 to 13 3/8 in out from the wall and 2 7/8 in behind the cabinet door; 5 gal, about 42 lb of water when full, resting on the tank top (put a flat board under it); the neck is about 2 1/8 in across (55 mm), so the drain hose goes into a small opening and the bottle needs a vent; only 1 in over its top, so it does not lift straight up off the hose: pull the hose out of the neck, then slide the bottle forward out of the door'),
('Passenger','Dish towel hook','98 1/2 (the towel hangs from 94 1/2 to 102 1/2)','sticks out 2 in; the folded towel is about 8 wide and hangs 11','hook 50 up, 4 in under the TV (which starts at 54); the towel hangs down to 39, 1 in over the countertop (38)','on the strip of wall between the end of the nook (93 1/4) and the sliding door opening (104), 10 3/4 in wide, so the hook is 1 1/4 in from the nook end on that side and the towel 1 1/2 in from the door opening; fasten it with a screw into a furring strip or backing behind the wall covering'),
('Passenger','Paper towel holder','91.5 to 102.5','11 in roll, recessed into the angled front','29.75 to 35.25 up (5 1/2 in roll)','a recess (open cubby) in the angled front above the tank, so the roll sits inside the cabinet and sticks out nothing; a face-mounted holder would stick out about 6 in and squeeze the aisle across from the bench to about 12 in at 91; the cubby is 12 in wide between the faces, depth 15 to 19 in behind it'),
('Passenger','Drawers (2, side by side)','59.25 to 72.25 and 73.75 to 86.75','13 x 20 each','4 tall, 31.25 to 35.25 up','under the counter in the flat part (58 to 88), over the wheel well and the trash can; the left drawer holds the 12 x 14 x 3 silverware tray; none at the angle'),
('Passenger','Lower drawers (3, on the back side: a 5 in over two 7 1/2 in)','59.25 to 72.25 (toward the back, to the right in diagram E)','13 x 20 each','5 tall at 26 to 31, 7 1/2 tall at 17 1/2 to 25 and 7 1/2 tall at 9 to 16 1/2 (rails at 25 to 25.75 and 16 1/2 to 17.25), on their own shelf at 8 to 8.75 (1/2 in over the wheel well, 7.5 tall)','under the top drawer; 20 deep so they reach back to the wall over the wheel well; the cab-side column next to them holds the trash can (next row), not drawers'),
('Passenger','Trash can on a pull-out (13 gal kitchen can)','74 1/4 to 86 1/4 (the cab-side column, under the top drawer)','12 wide x 16 deep x 24 tall, 1 1/2 to 17 1/2 in out from the wall (about the size of a tall 13 gallon kitchen can; measure the real one)','4 3/4 to 28 3/4 up, on a 3/4 in tray and 1/2 in full-extension slides (they ride about 1/8 in over the wheel well edge, 3 3/8 in tall at the edge of the tray); 2 1/2 in under the top drawer above it','replaces the two lower cab-side drawers and their shelves; the divider beside it runs down to the floor; the fresh water tank was shortened from 41 to 35 in so it starts at 87 1/4, past the can; the slides carry it 19 in out so a bag lifts out clear of the top drawers (at least 18 1/2 in is needed), which leaves 3 3/4 in of aisle across from the closet at the tray (6 1/2 in at the can) while it is out: nobody can walk past then and the closet door must stay shut; a latch keeps it shut while driving and a strap or bracket keeps the can from tipping'),
('Passenger','Hot water tank','87.25 to 101.25','14 x 14','13 tall, on a 3/4 in shelf over the fresh water tank (16.75 to 29.75, 6 in over the tank top at 10)','at the end of the drawers (87.25) and short of the sink cabinet (103), so it clears the sink bowl; the hot and cold fittings and the relief valve are at its back, so it needs a 1 5/8 in gap to the wall and its front is 15 5/8 in from the wall, which fits the 16 3/4 in the angled front leaves clear inside the door at its sink end, with about 1 in to spare; 6 3/4 in under the counter for its fittings and relief valve; the shelf is carried by the cabinet sides, not by the tank; the paper towel recess is just above it; holds about 4 gal (33 lb of water); the heater itself weighs 2 lb, so about 35 lb full; 14 x 14 x 13 is its outside size; electric, so no vent or combustion air; 120 V AC, 1,440 W (12 A: a 20 A circuit on 12 AWG, or a 15 A circuit on 14 AWG right at its limit, and about 133 A at 12 V through an inverter of 2,000 W or more from the 280 Ah battery, which is close: the battery is at 52 to 73); fittings, access, the relief valve and the drain are not set yet'),
('Passenger','Wheel well','42 to 76','34 x 7','7.5 tall','same as the driver side (flat top 15.5 long)'),
('Passenger','Sliding door','104 to 155','51 opening, 59 panel','up to 58','only the rear edge is measured'),
('Passenger','Fold-out table','123 to 152','29 long x 15 deep (3/4 thick)','29 up (hinged on the sink cabinet end, folds down against it)','reaches the passenger seat when it is turned to face the back; carried by a folding brace (a diagonal arm hinged on the cabinet end, 13 in below the board, locking 15 3/4 in out), not a floor leg, because the knees and shins of the rotated seat are at the free end; closes off the entry while open; length may need to be shorter, it should stop in front of the belly'),
('Passenger','Foot ledge','123 to 136','13 long x 17 wide (3/4 thick, flat, no lip); its outer edge is 13 in from the cabinet end','top at 8 1/2 up, flat, 8 1/2 in below the 17 in cab seat cushion','hinged on the cabinet end under the table, folds up into a 3/4 in recess in the end panel behind the folded table; small folding brace; the base of the sink cabinet is full (fresh water tank), so it cannot slide out of the base'),
('Passenger','Entry','123 to 154','31 clear (about 30 with the table folded down)','','behind the passenger seat; closed off while the table is open'),
('Under the van','Grey water tank','not set','30 x 17 x 8 space (was 24 x 17 x 8)','','shower and sink (grey water only); both drains run down through the floor; no off-the-shelf tank found that fits; size to be chosen; toilet waste (black water) is not covered'),
('Aisles','Bed to counter','','21 across (couch, 26 deep), 22 with the bed opened to 46 in','',''),
('Aisles','Dinette to counter','','19 1/4 at 89 (tightest: the counter is 21 deep up to 88, then angles in), 23 from 103 (was 17 1/4 and 21 with the dinette 30 deep)','','across from the closet it is 22'),
('Driver','Gear shelf (over the battery)',f'{fr8(SH_X0)} to {fr8(SH_X1)}',f'{fr16(SH_X1-SH_X0-1.5)} x {fr16(SH_Y1-SH_Y0)} in of 1/2 in plywood between two 3/4 x 2 1/2 in end rails ({fr16(SH_X1-SH_X0)} wide with them)',f'underside {fr8(SH_Z0)} up (1 in over the battery top at 9 1/2, for the terminals and lugs), top {fr8(SH_Z1)}; {fr8(SH_Y0)} to {fr8(SH_Y1)} in out from the wall; the tallest unit leaves {fr8(AIR)} in under the deck ({fr8(DECK_U)})',f'one tray on two {SH_PULL} in full-extension slides (one on the closet end panel at 74, one on a 3/4 in plywood divider at {fr16(SH_DIV)} to {fr16(SH_DIV+.75)}, west of the wheel well); its front is a plain face (a board with a finger slot) flush with the couch front, so pulling the face pulls the shelf, and the rest of the couch front under the deck is left open (not covered) {SH_PULL} in into the aisle, and all of it is open from above (the couch front rail across the opening is a steel tube on two angle ledges that lifts out: diagram C5); about 28 lb loaded; every cable to it needs a loop about {SH_PULL+6} in longer than a fixed run; how to build it: diagram C4'),
('Driver','Inverter (BELTTT 2000 W)',f'{fr16(INV["x0"])} to {fr16(INV["x1"])}','14.8 x 7.7 x 3.9 (from its listing)',f'on the gear shelf, rear row, {fr16(INV["y0"])} to {fr16(INV["y1"])} in out from the wall','inverter only: no charger and no transfer switch (so a 30 A transfer switch on the hub board); 2/0 AWG to the battery bus with a loop for the shelf; its remote has a 23 ft cable'),
('Driver','DC-DC charger (LiTime 60 A)',f'{fr16(DC["x0"])} to {fr16(DC["x1"])}','16 x 9 x 4.5 (measured by you)',f'on the gear shelf, rear row, {fr16(DC["y0"])} to {fr16(DC["y1"])} in out from the wall, over the battery','2 AWG from the starter battery (about 15 ft), 80 A fuses at both ends; the starter cable needs a loop for the shelf'),
('Driver','Shore charger (VEVOR 80 A)',f'{fr16(CHG["x0"])} to {fr16(CHG["x1"])}','9.5 x 7 x 4 (measured by you: 9.5 x 4 x 7)',f'on the gear shelf, front row, {fr16(CHG["y0"])} to {fr16(CHG["y1"])} in out from the wall','14.6 V lithium charger; AC from the shore side only, on its own 15 A breaker; 2 AWG and a 100 A fuse to the battery bus'),
('Aisles','Closet to cabinet','','22 across','',''),
('Aisles','Shower to bed','','19 across','','in front of the shower')]
import json as _json; _json.dump(rows,open(HERE+'/plan_rows.json','w'),indent=0)   # for the build guide pages (tools/buildguide.py)
tbl='<table><tr><th>Side</th><th>Item</th><th>Along the wall (in from the back)</th><th>Size, along x out (in)</th><th>Height (in)</th><th>Notes</th></tr>'+''.join('<tr>'+''.join(f'<td>{c}</td>' for c in r)+'</tr>' for r in rows)+'</table>'
blk='<h2>3. Looking down into the van, both sides</h2>\n<div class="wide">'+svg+'</div>\n<p>Every item is drawn from the sizes in your notes. The across numbers add up: shower 24 + 18 gap + bed 26 = 68, bed 26 + 21 aisle + counter 21 = 68, and dinette 28 + 23 aisle + sink counter 17 = 68. Dashed outlines are above the floor (overhead cabinets, microwave, the ceiling fan and air conditioning cutouts; the round yellow dots are the ceiling lights). The grey water tank goes under the van and is not drawn. The fresh water tank (dashed blue, 35 x 16) is on the floor at the sink end, partly in the sink cabinet (which is open to the area beside it), and the hot water tank (dashed red, 14 x 14, 13 tall) is on a shelf over the fresh water tank, 87 1/4 to 101 1/4 in, just before the sink cabinet, with a 1 5/8 in gap behind it to the wall for its fittings and relief valve. The bed (74 long) rolls out to 46 in wide (dashed, 26 in bed depth + the 20 in back): the tall fridge (19 deep, sitting 2 in off the wall so its front is flush with the cabinet) and the cabinet (21 deep) each leave 1 in, and the shower folds into the side wall so it does not count while the bed is out. The fold-out table (dashed, 29 x 15, at the cab-side end of the sink cabinet) is drawn open with the foot ledge (13 x 17) under it; folded, the table hangs against the cabinet end and the ledge folds into a recess in it. The passenger wheel well matches the driver side, and the sliding door is only measured at its rear edge. Everything is measured from the same zero, 6 in in from the back (the rear lip is not counted), and the cab wall is at 154 in, which can be off by 2 to 4 in. The sliding door opening (104 to 155) runs 1 in past the cab wall.</p>\n'+tbl+'\n'
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
