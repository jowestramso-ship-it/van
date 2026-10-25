import math
SC=8.0; X0=70; FLY=640
xx=lambda d:X0+SC*d; yy=lambda h:FLY-SC*h
W=xx(38)+40; H=FLY+50
o=[]; a=o.append
a(f'<svg viewBox="0 0 {W:.0f} {H}" role="img" style="max-width:820px"><title>Driver side bed and couch, side section</title>')
a('<defs><marker id="arc" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
a(f'<text class="ts" x="40" y="21" style="font-size:13px">Looking from the rear</text>')
# grid
for h in range(0,77,10):
    a(f'<line x1="{xx(0)-6}" y1="{yy(h)}" x2="{xx(38)}" y2="{yy(h)}" stroke="#3F3E3A" stroke-opacity="0.25" stroke-dasharray="3 3"/><text x="{xx(0)-10}" y="{yy(h)+4}" text-anchor="end" style="font-size:10px;font-weight:700;fill:#8A4B0F">{h}↑</text>')
for d in range(0,39,5):
    a(f'<line x1="{xx(d)}" y1="{yy(0)}" x2="{xx(d)}" y2="{yy(76)}" stroke="#3F3E3A" stroke-opacity="0.25" stroke-dasharray="3 3"/><text x="{xx(d)}" y="{yy(0)+16}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#185FA5">{d}→</text>')
a(f'<text class="ts" x="{xx(19)}" y="{yy(0)+32}" text-anchor="middle" style="font-size:11px">inches into the van from the body</text>')
# outside
a(f'<rect x="{xx(-6)}" y="{yy(76)}" width="{SC*6}" height="{SC*76}" fill="#D3E4F2" fill-opacity="0.6"/><text class="ts" x="{xx(-3)}" y="{yy(35)}" text-anchor="middle" style="font-size:11px">outside</text>')
# floor, ceiling
a(f'<line x1="{xx(-6)}" y1="{yy(0)}" x2="{xx(38)}" y2="{yy(0)}" stroke="#5F5E5A" stroke-width="2"/>')
a(f'<line x1="{xx(0)}" y1="{yy(76)}" x2="{xx(38)}" y2="{yy(76)}" stroke="#5F5E5A" stroke-width="1.5" stroke-dasharray="6 3"/><text class="ts" x="{xx(38)}" y="{yy(76)-4}" text-anchor="end" style="font-size:10px">ceiling 76 (bare), 75 1/16 with the covering</text>')
a(f'<rect x="{xx(0):.1f}" y="{yy(76):.1f}" width="{SC*38:.1f}" height="{SC*0.1875:.1f}" fill="#D9C7A5" stroke="#8A6B4D" stroke-width="0.6"/><rect x="{xx(0):.1f}" y="{yy(75.8125):.1f}" width="{SC*38:.1f}" height="{SC*0.75:.1f}" fill="#9A6B3A" fill-opacity="0.85" stroke="#5A3A00" stroke-width="0.6"/>')
# body
a(f'<line x1="{xx(0)}" y1="{yy(0)}" x2="{xx(0)}" y2="{yy(76)}" stroke="#2C2C2A" stroke-width="3"/><text class="th" x="{xx(0)+3}" y="{yy(76)-8}" style="font-size:11px">body (0)</text>')
# steel profile
prof=[(3.75,0),(3.75,23.25),(1.5,23.25),(1.5,29.5),(0.125,29.5),(0.125,31),(0,31),(0,56.5),(0.125,56.5),(0.125,58),(3.4,58),(3.4,76)]
a('<polyline points="'+' '.join(f'{xx(d):.1f},{yy(h):.1f}' for d,h in prof)+'" fill="none" stroke="#B5502F" stroke-width="3" stroke-linejoin="round"/>')
# finished wall face
a(f'<line x1="{xx(4.5)}" y1="{yy(0)}" x2="{xx(4.5)}" y2="{yy(76)}" stroke="#7A4A1E" stroke-width="1.6" stroke-dasharray="6 3"/><text class="ts" x="{xx(4.5)+3}" y="{yy(70)}" style="font-size:10px;fill:#7A4A1E">planks, 4 1/2 off the body</text>')
# bed: couch by day. Deck 16 to 16 3/4 on a base (raised 3 1/2 in for the gear shelf), the 3/4 in leaf folded back on it face down (top 17 1/2), seat cushion 17 1/2 to 23 1/2
fx=4.5; front=fx+26; ST=SEAT_T
a(f'<rect x="{xx(fx):.1f}" y="{yy(DECK_T):.1f}" width="{SC*26:.1f}" height="{SC*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B"/>')
a(f'<rect x="{xx(front-0.75):.1f}" y="{yy(DECK_U):.1f}" width="{SC*0.75:.1f}" height="{SC*1.5:.1f}" fill="#8A6B4D" stroke="#3E230B"/>')
a(f'<rect x="{xx(front-20):.1f}" y="{yy(PLAT):.1f}" width="{SC*20:.1f}" height="{SC*0.75:.1f}" fill="#B07A2A" fill-opacity="0.85" stroke="#5A3A00"/>')
a(f'<rect x="{xx(front-20+3):.1f}" y="{yy(PLAT-.1875):.1f}" width="{SC*12.625:.1f}" height="{SC*0.375:.1f}" fill="#2C2C2A" fill-opacity="0.8"/>')
a(f'<circle cx="{xx(front):.1f}" cy="{yy(DECK_T):.1f}" r="3.2" fill="#2C2C2A"/>')
a(f'<text class="ts" x="{xx(front)+8:.1f}" y="{yy(PLAT)+2:.1f}" style="font-size:10px;fill:#5A3A00">leaf, folded back</text><text class="ts" x="{xx(front)+8:.1f}" y="{yy(PLAT)+14:.1f}" style="font-size:10px;fill:#5A3A00">(leg in its slot)</text>')
a(f'<text class="ts" x="{xx(front)+8:.1f}" y="{yy(DECK_U-3.4)+3:.1f}" style="font-size:10px;fill:#444441">base front rail</text>')
a(f'<rect x="{xx(fx):.1f}" y="{yy(ST):.1f}" width="{SC*26:.1f}" height="{SC*CUSH:.1f}" fill="#534AB7" fill-opacity="0.18" stroke="#534AB7" stroke-width="1.6"/>')
a(f'<text class="th" x="{xx(fx+13):.1f}" y="{yy((PLAT+SEAT_T)/2)+4}" text-anchor="middle" style="font-size:11px;fill:#534AB7">Seat cushion {CUSH} in, top at {fr8(SEAT_T)}</text>')
a(f'<text class="ts" x="{xx(fx+24):.1f}" y="{yy(6)}" text-anchor="middle" style="font-size:10px">space under the bed,</text><text class="ts" x="{xx(fx+24):.1f}" y="{yy(6)+12}" text-anchor="middle" style="font-size:10px">16 in tall</text>')
# back cushion, 12 degrees
th=math.radians(12); t=CUSH/math.cos(th)
rb=(fx,ST); fb=(fx+t,ST)
top=ST+20
rt=(fx-(top-ST)*math.tan(th),top); ft=(fb[0]-(top-ST)*math.tan(th),top)
a('<polygon points="'+' '.join(f'{xx(d):.1f},{yy(h):.1f}' for d,h in (rb,fb,ft,rt))+'" fill="#F2B84B" fill-opacity="0.65" stroke="#8A5A00" stroke-width="2"/>')
a(f'<text class="th" x="{xx(fx+t+0.6):.1f}" y="{yy(ST+13)}" style="font-size:11px;fill:#5A3A00">Back cushion</text><text class="ts" x="{xx(fx+t+0.6):.1f}" y="{yy(ST+13)+13}" style="font-size:10px;fill:#5A3A00">{CUSH} thick, 20 tall,</text><text class="ts" x="{xx(fx+t+0.6):.1f}" y="{yy(ST+13)+25}" style="font-size:10px;fill:#5A3A00">leaning back 12 degrees</text>')
# seat depth dimension
a(f'<line x1="{xx(fb[0]):.1f}" y1="{yy(ST+2.3)}" x2="{xx(front):.1f}" y2="{yy(ST+2.3)}" stroke="#A32D2D" stroke-width="1.6" marker-start="url(#arc)" marker-end="url(#arc)"/><text class="th" x="{xx((fb[0]+front)/2):.1f}" y="{yy(ST+2.3)-5}" text-anchor="middle" style="font-size:11px;fill:#A32D2D">seat about 21 in deep</text>')
# bed depth dimension
a(f'<line x1="{xx(fx):.1f}" y1="{yy(ST+5.2)}" x2="{xx(front):.1f}" y2="{yy(ST+5.2)}" stroke="#534AB7" stroke-width="1.4" marker-start="url(#arc)" marker-end="url(#arc)"/>')
a(f'<text class="ts" x="{xx(fx+12.5):.1f}" y="{yy(ST+5.2)-4}" text-anchor="middle" style="font-size:10px;fill:#534AB7">bed 26 deep from the planks</text>')
# wheel well + battery (if the 7 in is measured from the wall steel), dashed, at this section
a(f'<rect x="{xx(3.75):.1f}" y="{yy(7.5):.1f}" width="{SC*7:.1f}" height="{SC*7.5:.1f}" fill="#D8B79A" fill-opacity="0.8" stroke="#8A6B4D" stroke-dasharray="4 3"/>')
a(f'<rect x="{xx(10.75):.1f}" y="{yy(9.5):.1f}" width="{SC*10:.1f}" height="{SC*9.5:.1f}" fill="#F2B84B" fill-opacity="0.5" stroke="#8A5A00" stroke-dasharray="4 3"/>')
a(f'<text class="ts" x="{xx(10.75)+SC*5:.1f}" y="{yy(5.2)}" text-anchor="middle" style="font-size:9px;fill:#5A3A00">well + battery</text>')
# the gear shelf over the battery (dashed): the tray 1 in over the battery top, the DC-DC charger (wall side, behind) and the shore charger (aisle side) on it; plan y out from the finished wall = x here minus 3.75
a(f'<rect x="{xx(4.5+SH_Y0):.1f}" y="{yy(SH_Z1):.1f}" width="{SC*(SH_Y1-SH_Y0):.1f}" height="{SC*(SH_Z1-SH_Z0):.1f}" fill="#8A6B4D" fill-opacity="0.6" stroke="#5A3A00"/>')
for _u in (DC,CHG):
    a(f'<rect x="{xx(4.5+_u["y0"]):.1f}" y="{yy(SH_Z1+_u["h"]):.1f}" width="{SC*(_u["y1"]-_u["y0"]):.1f}" height="{SC*_u["h"]:.1f}" fill="#B45309" fill-opacity="0.18" stroke="#B45309" stroke-width="1.4" stroke-dasharray="4 3"/>')
a(f'<text class="ts" x="{xx(4.5+13):.1f}" y="{yy(SH_Z1+2.2):.1f}" text-anchor="middle" style="font-size:9px;fill:#7A3B07">DC-DC (behind)</text><text class="ts" x="{xx(4.5+21.5):.1f}" y="{yy(SH_Z1+2.2):.1f}" text-anchor="middle" style="font-size:9px;fill:#7A3B07">charger</text><text class="ts" x="{xx(front)+8:.1f}" y="{yy(SH_Z0+.3)+3:.1f}" style="font-size:10px;fill:#5A3A00">gear shelf (C4)</text>')
# overhead cabinet
a(f'<rect x="{xx(4.5):.1f}" y="{yy(75.0625):.1f}" width="{SC*14:.1f}" height="{SC*14.0625:.1f}" fill="#534AB7" fill-opacity="0.06" stroke="#534AB7" stroke-dasharray="5 3"/><text class="ts" x="{xx(11.5):.1f}" y="{yy(70)}" text-anchor="middle" style="font-size:9px;fill:#534AB7">overhead cabinet, bottom 61</text>')
a('</svg>')
svg='\n'.join(o)
html=open((ROOT+'/sides.html')).read()
if '<h3>Driver side: bed and couch, side section</h3>' in html:
    i=html.index('<h3>Driver side: bed and couch, side section</h3>'); j=html.index('<h2>2. Passenger side</h2>')
    html=html[:i]+html[j:]
blk='''<h3>Driver side: bed and couch, side section</h3>
<div class="wide">'''+svg+'''</div>
<p>By day the seat is at 22 1/2 in: a 16 3/4 in deck with the 3/4 in leaf lying on it, face down (top at 17 1/2 in), and a 5 in seat cushion (it was 6: 5 in keeps a seated head 1 1/2 in under the wall cabinets after the raise). The couch was raised 3 1/2 in (the seat was 20, now 22 1/2) so the gear shelf, with the inverter and the two chargers on it, fits over the battery (diagram C4). At night the leaf is flipped out level with the deck, so the bed is at 21 3/4 in (diagram C2). The back cushion is 5 in thick, 20 in tall (to 42 1/2 in up), and leans back 12 degrees into the wall. The seat in front of it is about 21 in deep (26 in couch minus the cushion's base). The couch sits on a base (two end panels, a ledger on the wall and a rail under the front edge of the deck, the small square under the front of the deck) that supports its ends and front. The bed makes up with a hinged leaf: a 20 in leaf (3/4 in plywood, 74 in long, no rails) is hinged on the front edge of the deck and lies back flat on it, face down, under the seat cushion, by day; the dark strip in it is one of the four legs, folded into its slot, so nothing sticks out. For the bed you lift the seat cushion, flip the leaf out until it is level with the deck, fold down its four legs (12 5/8 in of flat bar plus a 3 1/2 in screw-out foot), put the seat cushion back and lay the back cushion, as one 20 in piece, on the leaf: 26 + 20 = 46 in wide (diagram C2, with the build in C3). There are no rails or slides, so the space under the base stays free (16 in tall, with the gear shelf over the battery). The bed is drawn 26 in deep measured from the planks; the wheel well and battery are only under the part of the bed where the well is, and the well's 7 in is measured from the wall steel (confirmed), which is 3 3/4 in off the body, so it sticks out 10 3/4 in from the body.</p>
<table><tr><th>Height up</th><th>Steel off the body</th><th>Room behind the planks (4 1/2 off)</th><th>The back's rear edge</th></tr>
<tr><td>22 1/2 to 23 1/4</td><td>3 3/4 in</td><td>3/4 in</td><td>0 to 0.2 in behind the planks</td></tr>
<tr><td>23 1/4 to 29 1/2 (blue band)</td><td>1 1/2 in</td><td>3 in</td><td>0.2 to 1.5 in</td></tr>
<tr><td>29 1/2 to 31 (yellow strip)</td><td>1/8 in</td><td>4 3/8 in</td><td>1.5 to 1.8 in</td></tr>
<tr><td>31 to 42 1/2 (pans)</td><td>0</td><td>4 1/2 in</td><td>1.8 to 4.25 in (1/4 in short of the body at the top)</td></tr></table>
'''
html=html.replace('<h2>2. Passenger side</h2>',blk+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)
