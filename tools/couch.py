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
a(f'<line x1="{xx(0)}" y1="{yy(76)}" x2="{xx(38)}" y2="{yy(76)}" stroke="#5F5E5A" stroke-width="1.5" stroke-dasharray="6 3"/><text class="ts" x="{xx(38)}" y="{yy(76)-4}" text-anchor="end" style="font-size:10px">ceiling 76 (bare), 74 3/4 with the covering</text>')
a(f'<rect x="{xx(0):.1f}" y="{yy(76):.1f}" width="{SC*38:.1f}" height="{SC*0.25:.1f}" fill="#D9C7A5" stroke="#8A6B4D" stroke-width="0.6"/><rect x="{xx(0):.1f}" y="{yy(75.75):.1f}" width="{SC*38:.1f}" height="{SC*1:.1f}" fill="#9A6B3A" fill-opacity="0.85" stroke="#5A3A00" stroke-width="0.6"/>')
# body
a(f'<line x1="{xx(0)}" y1="{yy(0)}" x2="{xx(0)}" y2="{yy(76)}" stroke="#2C2C2A" stroke-width="3"/><text class="th" x="{xx(0)+3}" y="{yy(76)-8}" style="font-size:11px">body (0)</text>')
# steel profile
prof=[(3.75,0),(3.75,23.25),(1.5,23.25),(1.5,29.5),(0.125,29.5),(0.125,31),(0,31),(0,56.5),(0.125,56.5),(0.125,58),(3.4,58),(3.4,76)]
a('<polyline points="'+' '.join(f'{xx(d):.1f},{yy(h):.1f}' for d,h in prof)+'" fill="none" stroke="#B5502F" stroke-width="3" stroke-linejoin="round"/>')
# finished wall face
a(f'<line x1="{xx(4.5)}" y1="{yy(0)}" x2="{xx(4.5)}" y2="{yy(76)}" stroke="#7A4A1E" stroke-width="1.6" stroke-dasharray="6 3"/><text class="ts" x="{xx(4.5)+3}" y="{yy(70)}" style="font-size:10px;fill:#7A4A1E">planks, 4 1/2 off the body</text>')
# bed: couch by day. Deck 12 1/2 to 13 1/4 on a base, the 3/4 in leaf folded back on it face down (top 14), seat cushion 14 to 20
fx=4.5; front=fx+26; ST=20
a(f'<rect x="{xx(fx):.1f}" y="{yy(13.25):.1f}" width="{SC*26:.1f}" height="{SC*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B"/>')
a(f'<rect x="{xx(front-0.75):.1f}" y="{yy(12.5):.1f}" width="{SC*0.75:.1f}" height="{SC*1.5:.1f}" fill="#8A6B4D" stroke="#3E230B"/>')
a(f'<rect x="{xx(front-20):.1f}" y="{yy(14):.1f}" width="{SC*20:.1f}" height="{SC*0.75:.1f}" fill="#B07A2A" fill-opacity="0.85" stroke="#5A3A00"/>')
a(f'<rect x="{xx(front-20+3):.1f}" y="{yy(13.8125):.1f}" width="{SC*12.625:.1f}" height="{SC*0.375:.1f}" fill="#2C2C2A" fill-opacity="0.8"/>')
a(f'<circle cx="{xx(front):.1f}" cy="{yy(13.25):.1f}" r="3.2" fill="#2C2C2A"/>')
a(f'<text class="ts" x="{xx(front)+8:.1f}" y="{yy(14)+2:.1f}" style="font-size:10px;fill:#5A3A00">leaf, folded back</text><text class="ts" x="{xx(front)+8:.1f}" y="{yy(14)+14:.1f}" style="font-size:10px;fill:#5A3A00">(leg in its slot)</text>')
a(f'<text class="ts" x="{xx(front)+8:.1f}" y="{yy(11.6)+3:.1f}" style="font-size:10px;fill:#444441">base front rail</text>')
a(f'<rect x="{xx(fx):.1f}" y="{yy(ST):.1f}" width="{SC*26:.1f}" height="{SC*6:.1f}" fill="#534AB7" fill-opacity="0.18" stroke="#534AB7" stroke-width="1.6"/>')
a(f'<text class="th" x="{xx(fx+13):.1f}" y="{yy(17)+4}" text-anchor="middle" style="font-size:11px;fill:#534AB7">Seat cushion 6 in, top at 20</text>')
a(f'<text class="ts" x="{xx(fx+24):.1f}" y="{yy(5)}" text-anchor="middle" style="font-size:10px">storage under the bed,</text><text class="ts" x="{xx(fx+24):.1f}" y="{yy(5)+12}" text-anchor="middle" style="font-size:10px">12 1/2 in tall</text>')
# back cushion, 12 degrees
th=math.radians(12); t=6/math.cos(th)
rb=(fx,ST); fb=(fx+t,ST)
top=ST+20
rt=(fx-(top-ST)*math.tan(th),top); ft=(fb[0]-(top-ST)*math.tan(th),top)
a('<polygon points="'+' '.join(f'{xx(d):.1f},{yy(h):.1f}' for d,h in (rb,fb,ft,rt))+'" fill="#F2B84B" fill-opacity="0.65" stroke="#8A5A00" stroke-width="2"/>')
a(f'<text class="th" x="{xx(fx+t+0.6):.1f}" y="{yy(33)}" style="font-size:11px;fill:#5A3A00">Back cushion</text><text class="ts" x="{xx(fx+t+0.6):.1f}" y="{yy(33)+13}" style="font-size:10px;fill:#5A3A00">6 thick, 20 tall,</text><text class="ts" x="{xx(fx+t+0.6):.1f}" y="{yy(33)+25}" style="font-size:10px;fill:#5A3A00">leaning back 12 degrees</text>')
# seat depth dimension
a(f'<line x1="{xx(fb[0]):.1f}" y1="{yy(22.3)}" x2="{xx(front):.1f}" y2="{yy(22.3)}" stroke="#A32D2D" stroke-width="1.6" marker-start="url(#arc)" marker-end="url(#arc)"/><text class="th" x="{xx((fb[0]+front)/2):.1f}" y="{yy(22.3)-5}" text-anchor="middle" style="font-size:11px;fill:#A32D2D">seat about 20 in deep</text>')
# bed depth dimension
a(f'<line x1="{xx(fx):.1f}" y1="{yy(11)}" x2="{xx(front):.1f}" y2="{yy(11)}" stroke="#534AB7" stroke-width="1.4" marker-start="url(#arc)" marker-end="url(#arc)"/>')
a(f'<text class="ts" x="{xx(fx+12.5):.1f}" y="{yy(11)-4}" text-anchor="middle" style="font-size:10px;fill:#534AB7">bed 26 deep from the planks</text>')
# wheel well + battery (if the 7 in is measured from the wall steel), dashed, at this section
a(f'<rect x="{xx(3.75):.1f}" y="{yy(7.5):.1f}" width="{SC*7:.1f}" height="{SC*7.5:.1f}" fill="#D8B79A" fill-opacity="0.8" stroke="#8A6B4D" stroke-dasharray="4 3"/>')
a(f'<rect x="{xx(10.75):.1f}" y="{yy(9.5):.1f}" width="{SC*10:.1f}" height="{SC*9.5:.1f}" fill="#F2B84B" fill-opacity="0.5" stroke="#8A5A00" stroke-dasharray="4 3"/>')
a(f'<text class="ts" x="{xx(10.75)+SC*5:.1f}" y="{yy(4)}" text-anchor="middle" style="font-size:9px;fill:#5A3A00">well + battery</text>')
# overhead cabinet
a(f'<rect x="{xx(4.5):.1f}" y="{yy(74.75):.1f}" width="{SC*14:.1f}" height="{SC*13.75:.1f}" fill="#534AB7" fill-opacity="0.06" stroke="#534AB7" stroke-dasharray="5 3"/><text class="ts" x="{xx(11.5):.1f}" y="{yy(70)}" text-anchor="middle" style="font-size:9px;fill:#534AB7">overhead cabinet, bottom 61</text>')
a('</svg>')
svg='\n'.join(o)
html=open((ROOT+'/sides.html')).read()
if '<h3>Driver side: bed and couch, side section</h3>' in html:
    i=html.index('<h3>Driver side: bed and couch, side section</h3>'); j=html.index('<h2>2. Passenger side</h2>')
    html=html[:i]+html[j:]
blk='''<h3>Driver side: bed and couch, side section</h3>
<div class="wide">'''+svg+'''</div>
<p>By day the seat is at 20 in: a 13 1/4 in deck with the 3/4 in leaf lying on it, face down (top at 14 in), and a 6 in seat cushion. At night the leaf is flipped out level with the deck, so the bed is at 19 1/4 in (diagram C2). The back cushion is 6 in thick, 20 in tall (to 40 in up), and leans back 12 degrees into the wall. The seat in front of it is about 20 in deep (26 in couch minus the cushion's base). The couch sits on a base (two end panels, a ledger on the wall and a rail under the front edge of the deck, the small square under the front of the deck) that supports its ends and front. The bed makes up with a hinged leaf: a 20 in leaf (3/4 in plywood, 74 in long, no rails) is hinged on the front edge of the deck and lies back flat on it, face down, under the seat cushion, by day; the dark strip in it is one of the four legs, folded into its slot, so nothing sticks out. For the bed you lift the seat cushion, flip the leaf out until it is level with the deck, fold down its four 12 5/8 in legs, put the seat cushion back and lay the back cushion, as one 20 in piece, on the leaf: 26 + 20 = 46 in wide (diagram C2, with the build in C3). There are no rails or slides, so the space under the base stays free (12 1/2 in tall). The bed is drawn 26 in deep measured from the planks; the wheel well and battery are only under the part of the bed where the well is, and the well's 7 in is measured from the wall steel (confirmed), which is 3 3/4 in off the body, so it sticks out 10 3/4 in from the body.</p>
<table><tr><th>Height up</th><th>Steel off the body</th><th>Room behind the planks (4 1/2 off)</th><th>The back's rear edge</th></tr>
<tr><td>20 to 23 1/4</td><td>3 3/4 in</td><td>3/4 in</td><td>0 to 0.7 in behind the planks</td></tr>
<tr><td>23 1/4 to 29 1/2 (blue band)</td><td>1 1/2 in</td><td>3 in</td><td>0.7 to 2 in</td></tr>
<tr><td>29 1/2 to 31 (yellow strip)</td><td>1/8 in</td><td>4 3/8 in</td><td>2 to 2.3 in</td></tr>
<tr><td>31 to 40 (pans)</td><td>0</td><td>4 1/2 in</td><td>2.3 to 4.25 in (1/4 in short of the body at the top)</td></tr></table>
'''
html=html.replace('<h2>2. Passenger side</h2>',blk+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)
