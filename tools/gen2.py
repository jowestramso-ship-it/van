import os
HERE=os.path.dirname(os.path.abspath(__file__))
ROOT=os.path.dirname(HERE)
src=open((ROOT+'/index.html')).read()
head=src[:src.index('<body>')].replace('Ford Transit Van Conversion Layout','Ford Transit Wall Diagrams')
S=6.0; X0=50; FL=540
X=lambda i:X0+S*i
K=25.5/27
PK=1
OFF=0.8
KK=25.5/27
U=lambda a:(a-OFF)/KK
Y=lambda h:FL-S*(h*PK+(OFF if PK!=1 else 0))
CP=[(1,6),(14.5,16),(18.5,19.5),(31.5,29.75),(35.5,32.75),(48,43),(52.5,46),(63.5,56.25),(68.5,61),(77.5,69.625),(80.5,73),(90,81.25),(93,84.625),(101,93.25),(105,98.3),(112,104.5),(158.5,155)]
def f(x):
    if x<=CP[0][0]: return x+(CP[0][1]-CP[0][0])
    if x>=CP[-1][0]: return x+(CP[-1][1]-CP[-1][0])
    for (a,b),(c,d) in zip(CP,CP[1:]):
        if a<=x<=c: return b+(x-a)*(d-b)/(c-a)
def box(a,b,h0,h1,extra=''):
    return f'<rect x="{X(a):.1f}" y="{Y(h1):.1f}" width="{S*(b-a):.1f}" height="{S*(h1-h0)*PK:.1f}" {extra}/>'
o=[]; A=o.append
W=X(160)+60; H=FL+80
A(f'<svg viewBox="0 0 {W:.0f} {H}" role="img"><title>Driver side wall: steel map with layout</title>')
A('<defs><marker id="ar" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
A(f'<text class="ts" x="{X0}" y="22" style="font-size:14px">Driver side wall seen from the aisle. Rear doors on the left, cab on the right.</text>')
# faint grid
for i in range(0,161,10):
    A(f'<line x1="{X(i)}" y1="{Y(83)}" x2="{X(i)}" y2="{FL}" stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"/>')
for h in range(0,84,10):
    A(f'<line x1="{X(0)}" y1="{Y(h)}" x2="{X(160)}" y2="{Y(h)}" stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"/>')
    A(f'<text class="ts" x="{X(0)-6}" y="{Y(h)+4}" text-anchor="end" style="font-size:11px">{h}</text>')
GRID_END=len(o)
# wall body
PK=K
A(box(0,160,0,66,'fill="#F1EFE8" stroke="#5F5E5A" stroke-width="1.2"'))
# flat bands
A(box(0,160,59,66,'fill="#E8E6DC"'))
A(box(0,160,22,32,'fill="#E8E6DC"'))
A(f'<text class="ts" x="{X(2)}" y="{Y(U(58.7))+4}" style="font-size:11px">flat band: ? in off the body</text>')
# pans
pans=[(6,16),(19.5,29.75),(32.75,43),(46,56.25),(61,69.625),(73,81.25),(84.625,93.25),(104.5,113.625),(116.25,125.5),(129,138.25),(141.25,150.375)]
for a,b in pans:
    est=' stroke-dasharray="5 3"' if pans.index((a,b)) in () else ''
    idx=pans.index((a,b)); ST='fill="#2C2C2A" fill-opacity="0.55" stroke="#444441" stroke-width="1.2" stroke-linejoin="round"'
    if idx in (0,10):
        c=1.5; v=1.5
        if idx==0: pts=[(a,32),(b,32),(b,59),(a+c,59),(a,59-v)]
        else: pts=[(a,32),(b,32),(b,59-v),(b-c,59),(a,59)]
        A('<polygon points="'+' '.join(f'{X(x):.1f},{Y(h):.1f}' for x,h in pts)+f'" {ST}/>')
    else:
        A(box(a,b,32,59,'rx="10" '+ST+est))
# P1 chamfer note
A(f'<polygon points="{X(6)},{Y(38)} {X(6)},{Y(32)} {X(11)},{Y(32)}" fill="#F1EFE8" stroke="#5F5E5A" stroke-width="1"/>')
# ribs between pans: 1/8 in from the body
for i,j in ((0,1),(1,2),(2,3),(4,5),(5,6),(7,8),(8,9),(9,10)):
    A(box(pans[i][1],pans[j][0],32,59,'fill="#D3D1C7" fill-opacity="0.9" stroke="#888780" stroke-width="1"'))
# group frames (raised)
for a,b in ((4.2,58.5),(58.5,95.8),(102.2,153)):
    A(box(a,b,31,60,'rx="12" fill="none" stroke="#5F5E5A" stroke-width="1.5" stroke-dasharray="1 0"'))
for i,(a,b) in enumerate(pans):
    A(f'<text class="th" x="{X((a+b)/2)}" y="{Y(33.8)}" text-anchor="middle" style="fill:#fff;font-size:12px">P{i+1}</text>')
# slots
LK=25.5/27; LO=0.8
H=lambda h: round(h*LK+LO,1)
LOWROWS=[]
def lab(n,cx,cy,sz=11):
    A(f'<text class="th" x="{cx:.1f}" y="{cy+4:.1f}" text-anchor="middle" style="fill:#2C2C2A;font-size:{sz}px;paint-order:stroke;stroke:#fff;stroke-width:3px">{n}</text>')
SC=[44.625,56.875,67.125,77.625,87.875]
for k,c in enumerate(SC,1):
    cy=Y(U(25.3))
    A(f'<ellipse cx="{X(c):.1f}" cy="{cy:.1f}" rx="{S*0.875:.1f}" ry="{S*0.55:.1f}" fill="#2C2C2A" fill-opacity="0.8"/>')
    lab(f'S{k}',X(c),cy-12,10)
    LOWROWS.append((f'S{k}','oval slot, 1 3/4 wide',f'{c-0.875:.2f} to {c+0.875:.2f}','24.75 to 25.85'))
# lower holes
HOLE='fill="#2C2C2A" fill-opacity="0.55" stroke="#BA7517" stroke-width="1.8"'
LD=[('L1',21.5,31.6,(10.5-0.8)/(25.5/27),(19.5-0.8)/(25.5/27),'rectangle'),('L2',34.6,42.1,(10.5-0.8)/(25.5/27),(19.5-0.8)/(25.5/27),'rectangle'),('L3',46,55.8,(10.5-0.8)/(25.5/27),(19.5-0.8)/(25.5/27),'rectangle, sits over the wheel well'),('L4',62.7,68.2,(13.75-0.8)/(25.5/27),(19.5-0.8)/(25.5/27),'small rectangle'),('L5',72.8,86.2,(13.75-0.8)/(25.5/27),(19.5-0.8)/(25.5/27),'large rectangle with a brace inside'),('L6',105.85,117.1,(2.75-0.8)/(25.5/27),(19.75-0.8)/(25.5/27),'tall rectangle with a brace inside'),('L7',121.6,137.7,(2.75-0.8)/(25.5/27),(19.75-0.8)/(25.5/27),'large rectangle with braces inside'),('L8',142.2,157,(2.75-0.8)/(25.5/27),(19.75-0.8)/(25.5/27),'tall rectangle at the cab end')]
LABS={'L1':(20,29.25),'L2':(32.25,38.0),'L3':(42.0,50.75),'L4':(57,62),'L5':(66,79)}
for n,a,b,h0,h1,d in LD:
    l=a if a>100 else f(a); r=min(b,153.5) if a>100 else min(f(b),160)
    if n in LABS: l,r=LABS[n]
    A(box(l,r,h0,h1,f'rx="5" {HOLE}'))
    lab(n,X((l+r)/2),Y((h0+h1)/2*1.0)+0 if False else Y((h0+h1)/2),12)
    LOWROWS.append((n,d,f'{l:.1f} to {r:.1f}',f'{H(h0)} to {H(h1)}'))
R1C=82.5+5.25; R2C=f(97)+(R1C-f(92.8))
A(f'<circle cx="{X(R1C):.1f}" cy="{Y(U(17.25)):.1f}" r="{S*5.25:.1f}" {HOLE}/>')
lab('R1',X(R1C),Y(U(17.25)),12)
LOWROWS.append(('R1','round hole, about 10 1/2 across',f'{R1C-5.25:.2f} to {R1C+5.25:.2f}','12 to 22.5'))
A(f'<circle cx="{X(R2C):.1f}" cy="{Y(U(11.5)):.1f}" r="{S*1.0:.1f}" {HOLE}/>')
lab('R2',X(R2C)+14,Y(U(11.5))+10,10)
LOWROWS.append(('R2','small round hole, 2 across',f'{R2C-1:.1f} to {R2C+1:.1f}','10.5 to 12.5'))
A(box(98.9,103.7,0,18,'fill="#F1EFE8" stroke="#5F5E5A" stroke-width="1.2"'))
LOWROWS.append(('PL','seam pillar post','98.9 to 103.7',f'0 to {H(18)}'))
A(box(99.5,102.1,(6.5-LO)/LK,(13.5-LO)/LK,f'{HOLE}'))
lab('PO',X(100.8),Y((10-LO)/LK)-2,9)
LOWROWS.append(('PO','opening in the pillar post','99.5 to 102.1','6.5 to 13.5'))
A(box(1.5,48,(4-LO)/LK,(9-LO)/LK,'rx="3" fill="#2C2C2A" fill-opacity="0.5" stroke="#BA7517" stroke-width="1.6"'))
lab('LO',X(24.75),Y((6.5-LO)/LK),11)
LOWROWS.append(('LO','long low opening behind the wheel well','1.5 to 48','4 to 9'))
# cover plate + low pocket
PK_=dict(fill='#378ADD')
A(box(U(10.75),0,0,0,'') if False else box(4.75,13.25,(10.75-LO)/LK,(16.75-LO)/LK,'rx="3" fill="#2C2C2A" fill-opacity="0.55" stroke="#444441" stroke-width="1"'))
lab('CP',X(9),Y(14.5),11)
LOWROWS.append(('CP','cover plate (not a hole)','4.75 to 13.25','10.75 to 16.75'))
A(box(71,97,(4-LO)/LK,(9-LO)/LK,f'rx="4" {HOLE}'))
A(f'<text class="th" x="{X(84)}" y="{Y(6.5)+4}" text-anchor="middle" style="fill:#2C2C2A;font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:3px">LP</text>')
LOWROWS.append(('LP','low hole in front of the wheel well','71 to 97','4 to 9'))
# seam
A(f'<line x1="{X(98.3)}" y1="{Y(72)}" x2="{X(98.3)}" y2="{FL}" stroke="#993C1D" stroke-width="1.6" stroke-dasharray="7 4"/>')
A(f'<text class="th" x="{X(98.3)}" y="{FL+70}" text-anchor="middle" style="fill:#993C1D;font-size:12px">seam / pillar, about 98</text>')
# rail + harness
A(f'<path d="M{X(f(98))} {Y(U(63.5))} Q {X(115)} {Y(U(63))} {X(125)} {Y(U(65))} T {X(152)} {Y(U(66.5))}" fill="none" stroke="#2C2C2A" stroke-width="3" stroke-dasharray="6 2"/>')
A(f'<text class="ts" x="{X(125)}" y="{Y(72.6)}" text-anchor="middle" style="font-size:11px">wiring harness</text>')
# roof structure openings (approximate)
A(box(0,160,U(68),U(79),'fill="#E8E6DC" fill-opacity="0.7" stroke="#888780" stroke-width="0.8" stroke-dasharray="5 4"'))
TOP=[('T1',4,6.75,67.875,74.5,'narrow, near the rear edge','full'),
('T2',9,19.5,67,74.5,'large','full'),
('T3',27.25,40,67,74.5,'large, notched','full'),
('T4',42.5,56.25,67.25,76.25,'large','full'),
('T5',62.75,73.75,67.25,76.25,'large','full'),
('T6',76.75,89.75,67.25,76.25,'large','full'),
('T7',93.5,96.25,69.75,73.25,'small square','full'),
('T8',106,110.75,67.5,69.5,'small slot','full'),
('T8a',103.75,109.75,74.5,76.5,'above T8, parallelogram','full'),
('T9',113.75,124.375,67.5,74,'large, diagonal corner','full'),
('T10',130.125,139.125,67.5,73.75,'large','full')]
for n,a,b,h0,h1,_,m in TOP:
    dash='' if m=='full' else ' stroke-dasharray="4 3"'
    if n=='T8a':
        pts=[(a,h0),(b,h0),(b,h1),(a+1.5,h1)]
        A('<polygon points="'+' '.join(f'{X(x):.1f},{Y(U(h)):.1f}' for x,h in pts)+'" fill="#2C2C2A" fill-opacity="0.55" stroke="#BA7517" stroke-width="1.2" stroke-dasharray="4 3" stroke-linejoin="round"/>')
    else:
        A(box(a,b,U(h0),U(h1),'rx="4" fill="#2C2C2A" fill-opacity="0.55" stroke="#BA7517" stroke-width="1.2"'+dash))
    A(f'<text class="th" x="{X((a+b)/2):.1f}" y="{Y(U((h0+h1)/2))+4:.1f}" text-anchor="middle" style="fill:#2C2C2A;font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:3px">{n}</text>')
BAND=[('B1',90.25,92.25,60.25,63,'dark square, just left of the seam'),('B2',101.25,105,60.25,63,'dark slot, just right of the seam')]
for n,a,b,h0,h1,_ in BAND:
    A(box(a,b,U(h0),U(h1),'rx="2" fill="#2C2C2A" fill-opacity="0.7" stroke="#BA7517" stroke-width="1.4" stroke-dasharray="3 2"'))
    A(f'<text class="th" x="{X((a+b)/2):.1f}" y="{Y(U(h1))-4:.1f}" text-anchor="middle" style="fill:#2C2C2A;font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:3px">{n}</text>')
A(f'<text class="ts" x="{X(160)}" y="{Y(82)-5}" text-anchor="end" style="font-size:11px">roof structure above the wall: top holes T1-T10 and T8a</text>')
# wheel well
PK=1
WW0=len(o)
WW=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
A('<polygon points="'+' '.join(f'{X(x):.1f},{Y(h):.1f}' for x,h in WW)+'" fill="#E24B4A" fill-opacity="0.35" stroke="#A32D2D" stroke-width="1.6" stroke-dasharray="5 3" stroke-linejoin="round"/>')
A(f'<text class="th" x="{X(59)}" y="{Y(3.2)}" text-anchor="middle" style="fill:#791F1F;font-size:12px">wheel well</text>')
WW1=len(o)
# built items (drawn on their own diagram)
BI=[]
BA=BI.append
_og=[False]
def BG(name=None,label=''):
    if _og[0]: BI.append('</g>'); _og[0]=False
    if name: BI.append(f'<g class="tg" data-g="{name}" data-label="{label}">'); _og[0]=True
def item(a,b,h0,h1,col,label,sub=None,ly=None):
    BA(box(a,b,h0,h1,f'rx="3" fill="{col}" fill-opacity="0.12" stroke="{col}" stroke-opacity="0.9" stroke-width="1.4"'))
    yy=Y((h0+h1)/2) if ly is None else ly
    BA(f'<text class="th" x="{X((a+b)/2)}" y="{yy}" text-anchor="middle" style="fill:{col};font-size:12.5px;paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-opacity:.8">{label}</text>')
    if sub: BA(f'<text class="ts" x="{X((a+b)/2)}" y="{yy+15}" text-anchor="middle" style="fill:{col};font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-opacity:.8">{sub}</text>')
P='#534AB7'; G='#444441'; K='#993556'
BG('wallcab','Wall cabinets')
item(0,74,61,74.75,P,'',None,Y(67.5))
item(89,154,61,74.75,P,'',None,Y(67.5))
BA(f'<text class="th" x="{X(37)}" y="{Y(58.6)}" text-anchor="middle" style="fill:{P};font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:3px">Wall cabinet, 74 long x 14 deep x 15 tall (61 to 76 in up)</text>')
BA(f'<text class="th" x="{X(121.5)}" y="{Y(58.6)}" text-anchor="middle" style="fill:{P};font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:3px">Wall cabinet, 65 long x 14 deep x 15 tall (61 to 76 in up)</text>')
BG('pockets','Closet door pockets')
# pockets on the inside of the two closet doors (dashed: they face into the closet): 2 columns x 4 rows on the lower door, 2 x 3 on the upper door
for _z0,_z1 in ((5,12),(12.5,19.5),(20,27),(27.5,34.5),(42,49),(49.5,56.5),(57,64)):
    for _x0,_x1 in ((74.625,81.2),(81.7,88.3)):
        BA(box(_x0,_x1,_z0,_z1,f'rx="2" fill="#B07A2A" fill-opacity="0.10" stroke="#8A5A00" stroke-width="1" stroke-dasharray="3 2"'))
BA(f'<text class="ts" x="{X(81.5)}" y="{Y(66.5)}" text-anchor="middle" style="fill:#8A5A00;font-size:9.5px;paint-order:stroke;stroke:#fff;stroke-width:3px">dashed: door pockets inside</text>')
BG('doors','Cabinet doors')
# doors, 12 tall (landscape, flip-up), three per cabinet, trimmed in width: 24 1/2 on the bed side, 21 1/2 on the dinette side, 1/8 in gaps
for _d0,_w,_t in ((0.125,24.5,'door 24 1/2 x 12'),(24.75,24.5,'door 24 1/2 x 12'),(49.375,24.5,'door 24 1/2 x 12'),(89.125,21.5,'door 21 1/2 x 12'),(110.75,21.5,'door 21 1/2 x 12'),(132.375,21.5,'door 21 1/2 x 12')):
    BA(box(_d0,_d0+_w,61.5,73.5,f'rx="3" fill="{P}" fill-opacity="0.18" stroke="{P}" stroke-width="1.6"'))
    BA(f'<text class="th" x="{X(_d0+_w/2)}" y="{Y(67.8)}" text-anchor="middle" style="fill:{P};font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:3px">{_t}</text>')
BG('bed','Bed / couch')
item(0,74,14,20,P,'Seat cushion, top at 20 in (deck at 13 1/4, leaf folded on it)',None,Y(16.2))
item(0,74,20,40,P,'Back cushion, upright (20 tall)',None,Y(30))
BA(f'<line x1="{X(0)}" y1="{Y(14)}" x2="{X(74)}" y2="{Y(14)}" stroke="{P}" stroke-opacity="0.9" stroke-width="1.6"/>')
BG('closet','Closet')
item(74,89,0,74.75,G,'Closet','15 in',Y(47))
BG('ceil','Ceiling covering')
BA(box(0,154,75.75,76,'fill="#D9C7A5" stroke="#8A6B4D" stroke-width="0.8"'))
BA(box(0,154,74.75,75.75,'fill="#9A6B3A" fill-opacity="0.85" stroke="#5A3A00" stroke-width="0.8"'))
for _x0,_x1,_nm in ((0.25,14.25,'shower fan'),(36.375,50.625,'A/C')):
    BA(box(_x0,_x1,74.75,76,'fill="#2C2C2A" fill-opacity="0.85"'))
    BA(f'<text class="ts" x="{X((_x0+_x1)/2)}" y="{Y(77.4)}" text-anchor="middle" style="font-size:10px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:3px">{_nm}</text>')
for _lx in (20.67,74,127.33): BA(f'<circle cx="{X(_lx)}" cy="{Y(74.4)}" r="3" fill="#FFD84A" stroke="#B8860B" stroke-width="0.8"/>')
BA(f'<text class="ts" x="{X(152)}" y="{Y(77.4)}" text-anchor="end" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">ceiling covering: 1/4 plywood + 1 in slats, finished ceiling at 74 3/4</text>')
BG('cdoors','Closet doors')
# two doors on the closet, stacked, split at 38 so each opens one rod
for _z0,_z1,_n in ((0.25,37.9,'lower door'),(38.1,75.75,'upper door')):
    BA(box(74.125,88.875,_z0,_z1,f'rx="3" fill="{G}" fill-opacity="0.12" stroke="{G}" stroke-width="1.6"'))
    BA(f'<text class="th" x="{X(81.5)}" y="{Y((_z0+_z1)/2+(9 if _n=="upper door" else -9))}" text-anchor="middle" style="fill:{G};font-size:11.5px;paint-order:stroke;stroke:#fff;stroke-width:3px">{_n}</text><text class="ts" x="{X(81.5)}" y="{Y((_z0+_z1)/2+(9 if _n=="upper door" else -9))+13}" text-anchor="middle" style="fill:{G};font-size:10px;paint-order:stroke;stroke:#fff;stroke-width:3px">14 3/4 x 37 5/8</text>')
BG('rods','Closet rods')
for _rh in (71,36):
    BA(f'<line x1="{X(76)}" y1="{Y(_rh)}" x2="{X(87)}" y2="{Y(_rh)}" stroke="{G}" stroke-width="3.5" stroke-linecap="round"/>')
    BA(f'<text class="ts" x="{X(81.5)}" y="{Y(_rh)-5}" text-anchor="middle" style="fill:{G};font-size:10px;font-weight:700;paint-order:stroke;stroke:#fff;stroke-width:3px">rod, {_rh} in up</text>')
BG('benches','Dinette benches')
item(89,108.5,0,17.5,K,'Bench',None,Y(2.5))
item(89,91.9,17.5,38,K,'',None)
item(134.5,154,0,17.5,K,'Bench',None,Y(2.5))
item(151.1,154,17.5,38,K,'',None)
BG('table','Table')
BA(box(108.5,134.5,28,29,f'fill="{G}" fill-opacity="0.35" stroke="{G}" stroke-width="1.4"'))
BA(f'<text class="th" x="{X(121.5)}" y="{Y(25.3)}" text-anchor="middle" style="fill:{G};font-size:12.5px;paint-order:stroke;stroke:#fff;stroke-width:3px">Table, 29 in high</text>')
BG()
TAIL0=len(o)
# cab wall and rear lip
A(f'<defs><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#888780" stroke-width="1"/></pattern></defs>')
A(f'<rect x="{X(150)}" y="{Y(79)}" width="{S*8}" height="{S*79}" fill="url(#hatch)" fill-opacity="0.4"/>')
A(f'<rect x="{X(152)}" y="{Y(79)}" width="{S*4}" height="{S*79}" fill="url(#hatch)" fill-opacity="0.4"/>')
A(f'<line x1="{X(154)}" y1="{Y(79)}" x2="{X(154)}" y2="{FL}" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="6 3"/>')
A(f'<text class="ts" x="{X(154)-4}" y="{Y(79)-22}" text-anchor="end" style="font-size:11px">cab wall about 154; could be 150 to 158 (cab-end numbers may be off by 2 to 4 in)</text>')
# ruler
yb=FL+16
A(f'<line x1="{X(0)}" y1="{yb}" x2="{X(160)}" y2="{yb}" stroke="#888780" stroke-width="0.6"/>')
for t in range(0,161,10):
    A(f'<line x1="{X(t)}" y1="{yb-4}" x2="{X(t)}" y2="{yb+4}" stroke="#888780" stroke-width="0.6"/>')
    A(f'<text class="ts" x="{X(t)}" y="{yb+18}" text-anchor="middle" style="font-size:11px">{t}</text>')
A(f'<text class="ts" x="{X(80)}" y="{yb+36}" text-anchor="middle" style="font-size:12px">inches from where you start measuring at the back (about 6 in in from the rear edge; the rear lip is not counted)</text>')
A(f'<text class="ts" x="{X(0)}" y="{yb+36}" style="font-size:12px">Back (your zero)</text><text class="ts" x="{X(160)}" y="{yb+36}" text-anchor="end" style="font-size:12px">Cab</text>')
A(f'<text class="ts" x="{X(0)-30}" y="{Y(83)-8}" style="font-size:11px">in up from floor</text>')
A('</svg>')
svg='\n'.join(o)
PK=1
hdr=list(o[:GRID_END])
hdr[0]=hdr[0].replace('Driver side wall: steel map with layout','Driver side: built items')
hdr[2]=hdr[2].replace('Driver side wall seen from the aisle. Rear doors on the left, cab on the right.','Driver side built items (bed, closet, dinette, wall cabinets), seen from the aisle. Wheel well shown for reference.')
outline=f'<rect x="{X(0)}" y="{Y(79)}" width="{S*160}" height="{S*79}" fill="#F1EFE8" fill-opacity="0.6" stroke="#5F5E5A" stroke-width="1.2"/>'
svg2='\n'.join(hdr+[outline]+['<g class="tg" data-g="ww" data-label="Wheel well">']+o[WW0:WW1]+['</g>']+BI+o[TAIL0:])
import re as _re
# arrows on the axis numbers, and 20 in marks inside, like the depth map
def _fix(txt):
    txt=_re.sub(r'(<text class="ts" x="[\d.]+" y="[\d.]+" text-anchor="end" style="font-size:11px")>(\d+)</text>',lambda m:m.group(1)[:-1]+'; font-weight:700;fill:#8A4B0F">'+m.group(2)+'\u2191</text>' if False else '<text class="ts" x="'+m.group(1).split('x="')[1].split('"')[0]+'" y="'+m.group(1).split('y="')[1].split('"')[0]+'" text-anchor="end" style="font-size:11px;font-weight:700;fill:#8A4B0F">'+m.group(2)+'\u2191</text>',txt)
    txt=_re.sub(r'<text class="ts" x="([\d.]+)" y="([\d.]+)" text-anchor="middle" style="font-size:11px">(\d+)</text>',lambda m:'<text class="ts" x="'+m.group(1)+'" y="'+m.group(2)+'" text-anchor="middle" style="font-size:11px;font-weight:700;fill:#185FA5">'+m.group(3)+'\u2192</text>',txt)
    return txt
svg2=_fix(svg2)
_marks=''
for _t in range(20,150,20):
    for _h in (10,30,50,70):
        _marks+=f'<text x="{X(_t)+2:.1f}" y="{FL-6*_h+3:.1f}" style="font-size:10px;font-weight:700;fill:#185FA5;paint-order:stroke;stroke:#fff;stroke-width:2.5px;stroke-opacity:.8">{_t}\u2192</text>'
for _h in (20,40,60):
    for _t in (10,50,90,130):
        _marks+=f'<text x="{X(_t)+2:.1f}" y="{FL-6*_h-3:.1f}" style="font-size:10px;font-weight:700;fill:#8A4B0F;paint-order:stroke;stroke:#fff;stroke-width:2.5px;stroke-opacity:.8">{_h}\u2191</text>'
_marks+=f'<text class="ts" x="{X(0)}" y="{FL+88}" style="font-size:11px"><tspan style="fill:#185FA5;font-weight:600">blue numbers with an arrow \u2192</tspan> = inches from the back; <tspan style="fill:#8A4B0F;font-weight:700">brown numbers with \u2191</tspan> = inches up from the floor (marked every 20 in)</text>'
svg2=svg2.replace('</svg>','<g pointer-events="none">'+_marks+'</g></svg>')
_bat=''
_Y=lambda h:FL-6*h
# battery on the floor next to the wheel well, on its aisle side (well sticks out 7, battery 10 more = 17 in)
_bat+=f'<rect x="{X(52):.1f}" y="{_Y(9.5):.1f}" width="{6*21:.1f}" height="{6*9.5:.1f}" rx="3" fill="#F2B84B" fill-opacity="0.65" stroke="#8A5A00" stroke-width="2"/>'
_bat+=f'<text class="th" x="{X(62.5):.1f}" y="{_Y(5.8):.1f}" text-anchor="middle" style="font-size:11px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">Battery</text>'
_bat+=f'<text class="ts" x="{X(62.5):.1f}" y="{_Y(5.8)+13:.1f}" text-anchor="middle" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">21 x 9.5 in, 52 to 73 in</text>'
_bat+=f'<text class="ts" x="{X(62.5):.1f}" y="{_Y(5.8)+25:.1f}" text-anchor="middle" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">in front of the well</text>'
svg2=svg2.replace('</svg>','<g class="tg" data-g="battery" data-label="Battery">'+_bat+'</g></svg>')

svg2=svg2.replace('stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"','stroke="#3F3E3A" stroke-opacity="0.4" stroke-width="0.9" stroke-dasharray="3 3"')
svg2=svg2.replace('viewBox="0 0 %d %d"'%(round(X(160)+60),FL+80),'viewBox="0 0 %d %d"'%(round(X(160)+60),FL+96))

def rng(lst): return ', '.join(f'{a:g}-{b:g}' for a,b in lst)
def fr(v):
    return f'{v:g}'
def trow(n,a,b,h0,h1,d,m):
    if m=='full': note='measured'
    elif m=='part': note='left edge and heights measured; width still to measure'
    elif m=='t10': note='left edge (5 3/4 in after T9), top and bottom measured (6 1/4 tall); width to measure'
    elif m=='tt': note='top measured (5 1/4 in down from the top); left edge, width and bottom to measure'
    elif m=='tw': note='left edge, top (5 in down) and height (6 1/2) measured; width to measure'
    elif m=='tb': note='top (9 1/2 in down from the top) and bottom (67 1/2 in up) measured; left edge and width to measure'
    elif m=='ta': note='left edge (7 1/2 in after T7), top (2 1/2 in down) and bottom (74 1/2 in up) measured; width to measure'
    elif m=='tl': note='left edge, width (2 3/4) and height (3 1/2) measured; how far up it sits to measure'
    elif m=='t6': note='top and height measured (9 in tall); left edge and width to measure'
    elif m=='t4': note='left edge, width and top measured; bottom to measure'
    elif m=='top': note='top measured (2 3/4 in down from the top); the rest to measure'
    elif m=='part3': note='left edge, top and height measured; width still to measure'
    else: note=''
    return f'<tr><td>{n}</td><td>{d}</td><td>{a:g} to {b:g}{" (right edge est.)" if m in ("part3","part") else (" (est.)" if m in ("no","top","t6","ta","tb","tw","tt","t10") else ("" if m=="tl" else ""))}</td><td>{h0:g} to {h1:g}{" (bottom est.)" if m=="part3" else (" (est.)" if m=="no" else "")}</td><td>{note}</td><td>3 in at the top edge, 3 3/4 in at the bottom edge</td></tr>'
toprows=''.join(trow(*t) for t in TOP)+''.join(f'<tr><td>{n}</td><td>{d}</td><td>{a:g} to {b:g}</td><td>{h0:g} to {h1:g}{'' if n=='B1' else ' (top est.)'}</td><td>{"measured" if n=="B1" else "left edge, width (3 3/4) and bottom (60 1/4 in up) measured; top to measure"}</td><td>not measured</td></tr>' for n,a,b,h0,h1,d in BAND)
lowrows=''.join((f'<tr><td>{n}</td><td>{d}</td><td>{a}</td><td>24.75 to 25.85 (top est.)</td><td>left edge, width (1 3/4) and bottom measured; height to measure</td><td>not measured</td></tr>' if n=='S1' else f'<tr><td>{n}</td><td>{d}</td><td>{a}</td><td>{h}</td><td>measured (bottom 10 3/4 in up, top 62 1/4 in down from the top)</td><td>1 1/2 in (around it)</td></tr>' if n=='CP' else f'<tr><td>{n}</td><td>{d}</td><td>82.5 to 93</td><td>12 to 22.5</td><td>measured: 10 1/2 across, bottom 12 in up</td><td>3 3/4 in</td></tr>' if n=='R1' else f'<tr><td>{n}</td><td>{d}</td><td>71 (left edge measured) to 97 (est.)</td><td>4 to 9</td><td>left edge and bottom measured; top assumed the same as LO (9 in); right edge to measure</td><td>3 3/4 in (around it)</td></tr>' if n=='LP' else f'<tr><td>{n}</td><td>{d}</td><td>99.5 (left edge measured) to 102.1 (est.)</td><td>{h}</td><td>left edge and heights measured; width and depth to measure</td><td>not measured</td></tr>' if n=='PO' else f'<tr><td>{n}</td><td>{d}</td><td>{a}{" (left edge from PO + 3 3/4 in, 11 1/4 wide)" if n=="L6" else " (left edge from L6 + 4 1/2 in; right edge est.)" if n=="L7" else " (left edge from L7 + 4 1/2 in; runs to the cab wall, est.)"}</td><td>{h}</td><td>heights measured (2.75 in up, 17 tall); across {"left edge from the 3 3/4 in gap to PO (PO right edge is an estimate)" if n=="L6" else "to measure"}</td><td>3 3/4 in</td></tr>' if n in ('L6','L7','L8') else f'<tr><td>{n}</td><td>{d}</td><td>{a}</td><td>{h}</td><td>measured (46 1/2 long, runs 6 in past the rear edge of the wheel well)</td><td>2 1/2 in</td></tr>' if n=='LO' else f'<tr><td>{n}</td><td>{d}</td><td>{a} (est.)</td><td>{h}</td><td>heights measured (2 in round); position across to measure</td><td>3 3/4 in</td></tr>' if n=='R2' else f'<tr><td>{n}</td><td>{d}</td><td>{a}</td><td>{h if ('(' in h or n in ('L1','L2','L3','L4','L5')) else h+' (est.)'}</td><td>left and right edges measured; gap to the next hole: {"3 in" if n=="L1" else "6 1/2 in" if n=="L3" else "4 1/4 in" if n=="L4" else "not given"}</td><td>3 3/4 in</td></tr>' if n in ('L1','L3','L4','L5') else f'<tr><td>{n}</td><td>{d}</td><td>{a}</td><td>24.75 to 25.85 (top est.)</td><td>left edge measured; same width and height as S1, so the same bottom is assumed</td><td>not measured</td></tr>' if n in ('S2','S3','S4','S5') else f'<tr><td>{n}</td><td>{d}</td><td>{a} (est.)</td><td>{h if ('(' in h or n in ('L1','L2','L3','L4','L5')) else h+' (est.)'}</td><td>{"gap to the next hole: 3 in" if n=="L1" else "gap to the next hole: 4 in" if n=="L2" else "gap to the next hole: 6 1/2 in" if n=="L3" else "gap to the next hole: 4 1/4 in" if n=="L4" else ""}</td><td>{"3 3/4 in" if n in ("L1","L2","L3","L4","L5","L6","L7","L8","R1","R2") else "not measured"}</td></tr>') for n,d,a,h in LOWROWS)
panrows=''.join(f'<tr><td>P{i+1}</td><td>{a:g} to {b:g}</td><td>{b-a:.2f}</td></tr>' for i,(a,b) in enumerate(pans))
photos=[('IMG_0752','Rear, lower: cutouts, wheel well starting'),('IMG_0753','Rear, upper: roof rail, ribbed panels'),('IMG_0754','Seam and pillar, lower'),('IMG_0755','Seam, upper: wiring harness'),('IMG_0756','Wide view toward the cab')]
figs=''.join(f'<figure><a href="photos/driver/{p}.jpg"><img src="photos/driver/{p}.jpg" alt="{c}"></a><figcaption>{c}</figcaption></figure>' for p,c in photos)
css='''<style>
  body { max-width: 1100px; }
  figure { margin: 0; } figure img { width: 100%; height: auto; border-radius: 4px; display: block; }
  figcaption { font-size: 12px; color: #5F5E5A; margin-top: 4px; }
  .photos { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 12px; }
  .legend span { display: inline-block; margin-right: 16px; font-size: 13px; }
  .sw { display: inline-block; width: 14px; height: 12px; vertical-align: -1px; margin-right: 5px; border: 1px solid #5F5E5A; }
  table { border-collapse: collapse; font-size: 14px; } td, th { border-bottom: 1px solid #D3D1C7; padding: 3px 14px 3px 0; text-align: left; }
  .wide { overflow-x: auto; }
</style>
'''
head=head.replace('</style>','</style>'+css,1)
body=f'''<body>
<h1>Ford Transit wall diagrams</h1>
<p>One diagram per side, to scale (6 px per inch), with a faint grid every 10 inches. The van's steel and its depths are on one map (the depth color map); the built items (bed, closet, dinette, cabinets) are on their own diagram below it. Anything measured from the cab end (the wheel well front, P11's end, the cab wall itself) may be off by 2 to 4 in, shown by the hatched band at the right. Nearly everything on the map is a measurement you gave me. Anything marked (est.) in the tables below is still a guess from the photos, and those are the only things left to measure.</p>

<h2>1. Driver side</h2>
<h3>Reading the wall</h3>
<ul>
<li><b>Pans (light gray):</b> eleven pans, each 25.5 in tall (your measurement), from 31 to 56.5 in up (P1's top is 10.5 in below the bottom of T2). The pan is the body of the van; the other side of the metal is the outside, so a hole through a pan goes through to the outside.</li>
<li><b>Ribs (light gray):</b> the 3 in strips between the pans, standing 1/8 in off the body. That is the only standoff measured so far, and it is the shallow space you have behind anything you mount on a rib.</li>
<li><b>Flat steel:</b> a band above the pans (about 56 to 63 in), the belt line below them (about 22 to 31 in, with five oval slots at about 27 in), and the seam pillar at about 98 in. How far these stand off the body is not measured yet; that is the next thing to find.</li>
<li><b>Holes (light gray inside):</b> eight rectangular cutouts and a round hole low on the wall, the pillar opening, and the openings in the roof structure above the wall. These are where the inner steel is missing. The light gray you see in every hole is the outside wall of the van (the body), at the depth listed, the same as the pans. The depth numbers are for the steel around each hole, not inside it: around the top holes (T1-T10 and T8a) it is 3 in from the body at the top edge and 3 3/4 in at the bottom edge; around the L and R holes in the lower wall it is 3 3/4 in; inside every hole you see the body itself. The slots (S), the pillar opening and the low pocket are not measured yet.</li>
</ul>

<h3>Top holes: measured and still open</h3>
<p>These are the measurements you gave me for the top holes. (est.) marks the few numbers I still have as a guess from the photos; the notes column says what is measured.</p>
<table><tr><th>Hole</th><th>What I see</th><th>Left to right (in)</th><th>Bottom to top (in)</th><th>Measured</th><th>Steel around the hole is this far from the body</th></tr>{toprows}</table>

<h3>Bottom area: measured and still open</h3>
<p>Same as the top holes: these are your measurements, and (est.) marks the numbers still guessed from the photos. The wheel well (base 42 to 76 in, 7 1/2 in tall, sticks out 7 in) is measured too.</p>
<table><tr><th>Item</th><th>What I see</th><th>Left to right (in)</th><th>Up from the floor (in)</th><th>Measured</th><th>Steel around the hole is this far from the body</th></tr>{lowrows}</table>

<h3>Recessed pans, inches from the rear doors</h3>
<table><tr><th>Pan</th><th>From - to (in)</th><th>Width (in)</th></tr>{panrows}</table>
<p>Every pan is 25.5 in tall (measured). Their height off the floor, 31 to 56 1/2 in, comes from your T2 measurement (P1's top is 10 1/2 in below the bottom of T2). Rear group P1-P4, middle group P5-P7, seam at about 98 in, front group P8-P11. Your measurements: left edges of P1 (6), P2 (19.5), P4 (46), P5 (61), P8 (104.5), P9 (116.25), P10 (129), P11 (141.25); right edge of P7 (93.25). Widths: P5 8 5/8, P6 8 1/4, P7 8 5/8, so the ribs between P5, P6 and P7 work out to about 3 3/8 in. Ribs between neighboring pans are 3 in. P1 is 10 wide and P2-P4 are 10 1/4 wide, so P3 sits at 32 3/4 to 43. All eleven pans are measured or worked out from your measurements. P11 ends at about 150 in. P1 and P11 are drawn with their outer top corners angled slightly; the holes, slots and roof openings are placed from the photos.</p>

<h2>2. Passenger side</h2>
<p>Waiting for the passenger side photos.</p>

<h2>Driver side photos</h2>
<div class="photos">{figs}</div>
</body>
</html>
'''
open((ROOT+'/sides.html'),'w').write(head+body)

# ---- depth sections ----
def section_a():
    S2=6; D=30; FL2=560; x0=130
    yy=lambda h:FL2-S2*h
    xx=lambda d:x0+D*d
    o=[]; a=o.append
    a(f'<svg viewBox="0 0 560 620" role="img" style="max-width:620px"><title>Side section through T3 and P3</title>')
    a('<defs><marker id="ar2" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    a(f'<rect x="20" y="{yy(79)}" width="{x0-20}" height="{S2*79}" fill="#D3E4F2" fill-opacity="0.55"/>')
    a(f'<text class="ts" x="75" y="{yy(40)}" text-anchor="middle" style="font-size:13px">outside</text><text class="ts" x="75" y="{yy(40)+16}" text-anchor="middle" style="font-size:13px">of the van</text>')
    a(f'<text class="ts" x="{x0+300}" y="{yy(3)}" text-anchor="middle" style="font-size:13px">inside the van</text>')
    a(f'<line x1="{x0}" y1="{yy(79)}" x2="{x0}" y2="{FL2}" stroke="#2C2C2A" stroke-width="3"/>')
    a(f'<text class="th" x="{x0}" y="{yy(79)-8}" text-anchor="middle" style="font-size:12px">body (outer skin)</text>')
    a(f'<line x1="20" y1="{FL2}" x2="{x0+400}" y2="{FL2}" stroke="#5F5E5A" stroke-width="1.5"/><text class="ts" x="{x0+400}" y="{FL2+16}" text-anchor="end" style="font-size:12px">floor</text>')
    for h in range(0,80,10):
        a(f'<line x1="{x0-6}" y1="{yy(h)}" x2="{x0+400}" y2="{yy(h)}" stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"/><text class="ts" x="14" y="{yy(h)+4}" style="font-size:11px">{h}</text>')
    # depth ruler
    for d in range(0,13):
        a(f'<line x1="{xx(d)}" y1="{FL2+6}" x2="{xx(d)}" y2="{FL2+12}" stroke="#888780" stroke-width="0.6"/><text class="ts" x="{xx(d)}" y="{FL2+26}" text-anchor="middle" style="font-size:11px">{d}</text>')
    a(f'<text class="ts" x="{xx(6)}" y="{FL2+44}" text-anchor="middle" style="font-size:12px">inches in from the body</text>')
    # pan zone
    a(f'<line x1="{x0+3}" y1="{yy(31)}" x2="{x0+3}" y2="{yy(56.5)}" stroke="#5F5E5A" stroke-width="5"/>')
    a(f'<line x1="{xx(0.125)}" y1="{yy(56.5)}" x2="{xx(0.125)}" y2="{yy(58)}" stroke="#B4B2A9" stroke-width="5"/>')
    a(f'<text class="th" x="{x0+20}" y="{yy(44)}" style="fill:#444441;font-size:12px">Pan (P3): the inner side is the body, 0 in</text>')
    a(f'<text class="ts" x="{x0+20}" y="{yy(44)+15}" style="font-size:11px">31 to 56 1/2 in up. Ribs between pans stand 1/8 in off it.</text>')
    # unknown zones
    for h0,h1,label in ((58,67.5,'flat band and frame: standoff not measured'),(76.25,79,'')):
        a(f'<rect x="{x0+2}" y="{yy(h1)}" width="{D*3.75}" height="{S2*(h1-h0)}" fill="none" stroke="#888780" stroke-width="1" stroke-dasharray="4 4"/>')
        if label: a(f'<text class="ts" x="{x0+10}" y="{yy((h0+h1)/2)+4}" style="font-size:11px">{label}</text>')
    # lower wall below the pans
    a(f'<line x1="{xx(0.125)}" y1="{yy(31)}" x2="{xx(0.125)}" y2="{yy(29.5)}" stroke="#B4B2A9" stroke-width="5"/>')
    a(f'<line x1="{xx(0.125)}" y1="{yy(29.5)}" x2="{xx(1.5)}" y2="{yy(29.5)}" stroke="#5F5E5A" stroke-width="2"/>')
    a(f'<line x1="{xx(1.5)}" y1="{yy(29.5)}" x2="{xx(1.5)}" y2="{yy(23.25)}" stroke="#5F5E5A" stroke-width="5"/>')
    a(f'<line x1="{xx(1.5)}" y1="{yy(23.25)}" x2="{xx(3.75)}" y2="{yy(23.25)}" stroke="#5F5E5A" stroke-width="2"/>')
    a(f'<line x1="{xx(3.75)}" y1="{yy(23.25)}" x2="{xx(3.75)}" y2="{FL2}" stroke="#8F4508" stroke-width="5"/>')
    a(f'<text class="th" x="{xx(3.75)+12}" y="{yy(12)}" style="font-size:12px;fill:#8F4508">3 3/4 in off, 23 1/4 in up to the floor</text>')
    a(f'<text class="ts" x="{xx(3.75)+12}" y="{yy(12)+15}" style="font-size:11px">(from 15 in from the back to the cab; the bottom 5 in at the back too)</text>')
    a(f'<text class="th" x="{xx(1.5)+12}" y="{yy(29.9)+4}" style="font-size:12px;fill:#5F5E5A">1 1/2 in below (and above) the pan, 1/8 in off</text>')
    a(f'<text class="th" x="{xx(1.5)+12}" y="{yy(26.5)}" style="font-size:12px">1 1/2 in off the body</text>')
    a(f'<text class="ts" x="{xx(1.5)+12}" y="{yy(26.5)+15}" style="font-size:11px">from 29 1/2 down to 23 1/4 in up (ovals)</text>')
    a(f'<line x1="{x0+2}" y1="{yy(25)}" x2="{xx(1.5)}" y2="{yy(25)}" class="arr" marker-start="url(#ar2)" marker-end="url(#ar2)"/>')
    # hole T3 lips
    a(f'<line x1="{xx(3)-10}" y1="{yy(74.5)}" x2="{xx(3)+10}" y2="{yy(74.5)}" stroke="#BA7517" stroke-width="3"/>')
    a(f'<line x1="{xx(3.75)-10}" y1="{yy(67)}" x2="{xx(3.75)+10}" y2="{yy(67)}" stroke="#BA7517" stroke-width="3"/>')
    a(f'<line x1="{xx(3)}" y1="{yy(74.5)}" x2="{xx(3.75)}" y2="{yy(67)}" stroke="#BA7517" stroke-width="1.2" stroke-dasharray="4 3"/>')
    a(f'<line x1="{x0+2}" y1="{yy(74.5)-8}" x2="{xx(3)}" y2="{yy(74.5)-8}" class="arr" marker-start="url(#ar2)" marker-end="url(#ar2)"/><text class="th" x="{xx(3)+14}" y="{yy(74.5)-4}" style="font-size:12px;fill:#854F0B">3 in at the top edge</text>')
    a(f'<line x1="{x0+2}" y1="{yy(67)+10}" x2="{xx(3.75)}" y2="{yy(67)+10}" class="arr" marker-start="url(#ar2)" marker-end="url(#ar2)"/><text class="th" x="{xx(3.75)+14}" y="{yy(67)+14}" style="font-size:12px;fill:#854F0B">3 3/4 in at the bottom edge</text>')
    a(f'<text class="th" x="{xx(3.25)+16}" y="{yy(70.7)}" style="font-size:12px;fill:#854F0B">hole T3, 7 1/2 tall</text>')
    a(f'<text class="ts" x="{xx(3.25)+16}" y="{yy(70.7)+14}" style="font-size:11px">67 to 74 1/2 in up</text>')
    # cabinet
    a(f'<rect x="{x0}" y="{yy(74)}" width="{D*12}" height="{S2*18}" rx="3" fill="#534AB7" fill-opacity="0.02" stroke="#534AB7" stroke-opacity="0.3" stroke-width="1"/>')
    a(f'<text class="th" x="{xx(6)}" y="{yy(58)}" text-anchor="middle" style="fill:#534AB7;font-size:12px">Wall cabinet, 12 in deep, 56 to 74 in up</text>')
    a('</svg>')
    return '\n'.join(o)

def section_b():
    S3=6; D=40; x0=50; y0=40
    xx=lambda i:x0+S3*i
    o=[]; a=o.append
    W=xx(160)+30
    a(f'<svg viewBox="0 0 {W:.0f} 190" role="img"><title>Plan section through the pans</title>')
    a(f'<rect x="{x0}" y="14" width="{S3*160}" height="{y0-14}" fill="#D3E4F2" fill-opacity="0.55"/>')
    a(f'<text class="ts" x="{x0+4}" y="28" style="font-size:12px">outside of the van</text>')
    a(f'<line x1="{x0}" y1="{y0}" x2="{xx(160)}" y2="{y0}" stroke="#2C2C2A" stroke-width="3"/>')
    pr=[(6,16),(19.5,29.75),(32.75,43),(46,56.25),(61,69.625),(73,81.25),(84.625,93.25),(104.5,113.625),(116.25,125.5),(129,138.25),(141.25,150.375)]
    for i,j in ((0,1),(1,2),(2,3),(4,5),(5,6),(7,8),(8,9),(9,10)):
        a(f'<rect x="{xx(pr[i][1])}" y="{y0}" width="{S3*(pr[j][0]-pr[i][1])}" height="{D/8}" fill="#D3D1C7" stroke="#888780" stroke-width="0.8"/>')
    for i,(l,r) in enumerate(pr):
        a(f'<text class="ts" x="{xx((l+r)/2)}" y="{y0+34}" text-anchor="middle" style="font-size:11px;fill:#444441">P{i+1}</text>')
    a(f'<text class="ts" x="{x0}" y="{y0+62}" style="font-size:12px">Cut at pan height, looking down. The pans are the body (0 in). Each light gray rib stands 1/8 in off it (drawn 40 px per inch, so it looks tiny). The frames around the pan groups are not measured.</text>')
    a(f'<text class="ts" x="{x0}" y="{y0+80}" style="font-size:12px">The 3 in ribs: P1-P2, P2-P3, P3-P4, P5-P6, P6-P7, P8-P9, P9-P10, P10-P11.</text>')
    for t in range(0,161,10):
        a(f'<line x1="{xx(t)}" y1="{y0+92}" x2="{xx(t)}" y2="{y0+98}" stroke="#888780" stroke-width="0.6"/><text class="ts" x="{xx(t)}" y="{y0+112}" text-anchor="middle" style="font-size:11px">{t}</text>')
    a(f'<line x1="{xx(0)}" y1="{y0+92}" x2="{xx(160)}" y2="{y0+92}" stroke="#888780" stroke-width="0.6"/>')
    a('</svg>')
    return '\n'.join(o)

html=open((ROOT+'/sides.html')).read()
block=f'''<h2>Depth sections</h2>
<p>Side-on cuts through the wall, so you can see how far things stand off the body. Only the numbers you measured are drawn solid. Dashed boxes are parts I don't have a depth for yet. The lower-wall steps below the pans come from your description, so check where the heights fall.</p>
<h3>A. Through T3 and pan P3, looking from the rear toward the cab</h3>
<div class="wide">{section_a()}</div>
<p>The pan is the body itself (0 in), so the other side of it is the outside of the van. The top holes are cut in steel that stands 3 to 3 3/4 in off the body, so you can see the body through them. The part between the top of the pan and the bottom of the hole (the flat band and frame, 56 1/2 to 67 in up) has an unknown standoff. Above and below the pans, the first 1 1/2 in (31 to 29 1/2 in up, and 56 1/2 to 58 in up) is 1/8 in off the body, then the wall is 1 1/2 in off the body down to 23 1/4 in up, and under that, all the way to the floor, it is 3 3/4 in off the body (from 15 in from the back to the cab; the bottom 5 in at the back too). A 12 in deep wall cabinet at 56 to 74 in up would cover nearly all of the hole (7 of its 7 1/2 in).</p>
<h3>B. Through the pans, looking down</h3>
<div class="wide">{section_b()}</div>
'''
html=html.replace('<h2>2. Passenger side</h2>',block+'\n<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)

def section_c():
    S3=6; D=40; x0=50; y0=40
    xx=lambda i:x0+S3*i
    o=[]; a=o.append
    W=xx(160)+30
    a(f'<svg viewBox="0 0 {W:.0f} 190" role="img"><title>Plan section through the lower wall</title>')
    a(f'<rect x="{x0}" y="14" width="{S3*160}" height="{y0-14}" fill="#D3E4F2" fill-opacity="0.55"/>')
    a(f'<text class="ts" x="{x0+4}" y="28" style="font-size:12px">outside of the van</text>')
    a(f'<line x1="{x0}" y1="{y0}" x2="{xx(160)}" y2="{y0}" stroke="#2C2C2A" stroke-width="3"/>')
    # standoff profile: 1 in at ends, 2 in in the middle, dashed ramps (length not measured)
    p=lambda i,d:f'{xx(i):.1f},{y0+D*d:.1f}'
    a(f'<polyline points="{p(30,1.5)} {p(130,1.5)}" fill="none" stroke="#5F5E5A" stroke-width="4"/>')
    a(f'<polyline points="{p(0,1)} {p(30,1.5)}" fill="none" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="5 4"/>')
    a(f'<polyline points="{p(130,1.5)} {p(160,1)}" fill="none" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="5 4"/>')
    a(f'<circle cx="{xx(0)}" cy="{y0+D}" r="4" fill="#5F5E5A"/><circle cx="{xx(160)}" cy="{y0+D}" r="4" fill="#5F5E5A"/>')
    a(f'<text class="th" x="{xx(80)}" y="{y0+D*1.5+18}" text-anchor="middle" style="font-size:12px">1 1/2 in off the body</text>')
    a(f'<text class="th" x="{xx(0)+8}" y="{y0+D-12}" style="font-size:12px">1 in at the rear</text>')
    a(f'<text class="th" x="{xx(160)-8}" y="{y0+D-12}" text-anchor="end" style="font-size:12px">1 in at the cab end</text>')
    for t in range(0,161,10):
        a(f'<line x1="{xx(t)}" y1="{y0+D*1.5+30}" x2="{xx(t)}" y2="{y0+D*1.5+36}" stroke="#888780" stroke-width="0.6"/><text class="ts" x="{xx(t)}" y="{y0+D*1.5+50}" text-anchor="middle" style="font-size:11px">{t}</text>')
    a(f'<line x1="{xx(0)}" y1="{y0+D*1.5+30}" x2="{xx(160)}" y2="{y0+D*1.5+30}" stroke="#888780" stroke-width="0.6"/>')
    a('</svg>')
    return '\n'.join(o)

html=open((ROOT+'/sides.html')).read()
blk='<h3>C. Through the lower wall, looking down</h3>\n<div class="wide">'+section_c()+'</div>\n<p>Cut at about 26 in up (the 1 1/2 in belt-line wall, 23 1/4 to 29 1/2 in up), looking down. The 1 1/2 in depth drops to 1 in at the back and the front of the van. The dashed slopes show that, but I do not know where the slopes start, so 30 in and 130 in are placeholders.</p>\n'
html=html.replace('<h2>2. Passenger side</h2>',blk+'\n<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)

def section_d():
    S2=14; D=40
    yy=lambda h:410-S2*(h-4)
    o=[]; a=o.append
    a('<svg viewBox="0 0 900 450" role="img" style="max-width:900px"><title>Lower wall steps</title>')
    a('<defs><marker id="ar4" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    def panel(bx,title,htop,hbot,step,stepnote,holename):
        xx=lambda d:bx+D*d
        a(f'<rect x="{bx-50}" y="{yy(33)}" width="50" height="{S2*29}" fill="#D3E4F2" fill-opacity="0.55"/>')
        a(f'<text class="ts" x="{bx-25}" y="{yy(18)}" text-anchor="middle" style="font-size:11px">outside</text>')
        a(f'<text class="th" x="{bx}" y="{yy(33)-10}" style="font-size:13px">{title}</text>')
        a(f'<line x1="{bx}" y1="{yy(33)}" x2="{bx}" y2="{yy(4)}" stroke="#2C2C2A" stroke-width="3"/>')
        for h in (10,15,20,25,30):
            a(f'<line x1="{bx-6}" y1="{yy(h)}" x2="{bx+250}" y2="{yy(h)}" stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"/><text class="ts" x="{bx-10}" y="{yy(h)+4}" text-anchor="end" style="font-size:10px">{h}</text>')
        # pan
        a(f'<line x1="{bx+3}" y1="{yy(33)}" x2="{bx+3}" y2="{yy(31)}" stroke="#5F5E5A" stroke-width="5"/>')
        a(f'<text class="ts" x="{xx(0.4)+4}" y="{yy(32)+4}" style="font-size:11px;fill:#444441">pan (the body)</text>')
        # strip
        a(f'<line x1="{xx(0.125)}" y1="{yy(31)}" x2="{xx(0.125)}" y2="{yy(29.5)}" stroke="#B4B2A9" stroke-width="5"/>')
        a(f'<line x1="{xx(0.125)}" y1="{yy(29.5)}" x2="{xx(1.5)}" y2="{yy(29.5)}" stroke="#5F5E5A" stroke-width="2"/>')
        # 2 in zone
        a(f'<line x1="{xx(1.5)}" y1="{yy(29.5)}" x2="{xx(1.5)}" y2="{yy(step)}" stroke="#5F5E5A" stroke-width="5"/>')
        a(f'<text class="th" x="{xx(1.5)+10}" y="{yy((29.5+step)/2)+4}" style="font-size:12px">1 1/2 in off the body</text>')
        # step out
        a(f'<line x1="{xx(1.5)}" y1="{yy(step)}" x2="{xx(3.75)}" y2="{yy(step)}" stroke="#5F5E5A" stroke-width="2"/>')
        # 3.75 band above the hole
        a(f'<line x1="{xx(3.75)}" y1="{yy(step)}" x2="{xx(3.75)}" y2="{yy(htop)}" stroke="#BA7517" stroke-width="5"/>')
        a(f'<text class="th" x="{xx(3.75)-8}" y="{yy((step+htop)/2)-2}" text-anchor="end" style="font-size:12px;fill:#854F0B">3 3/4 in</text><text class="th" x="{xx(3.75)-8}" y="{yy((step+htop)/2)+12}" text-anchor="end" style="font-size:12px;fill:#854F0B">deep</text>')
        # hole
        a(f'<line x1="{xx(3.75)-12}" y1="{yy(htop)}" x2="{xx(3.75)+12}" y2="{yy(htop)}" stroke="#2C2C2A" stroke-width="3"/>')
        a(f'<line x1="{xx(3.75)-12}" y1="{yy(hbot)}" x2="{xx(3.75)+12}" y2="{yy(hbot)}" stroke="#2C2C2A" stroke-width="3"/>')
        a(f'<rect x="{xx(3.75)-12}" y="{yy(htop)}" width="24" height="{S2*(htop-hbot)}" fill="#2C2C2A" fill-opacity="0.12"/>')
        a(f'<text class="th" x="{xx(3.75)+22}" y="{yy((htop+hbot)/2)+4}" style="font-size:12px">hole {holename}</text>')
        # below hole unknown
        if hbot>8:
            a(f'<line x1="{xx(3.75)}" y1="{yy(hbot)}" x2="{xx(3.75)}" y2="{yy(8)}" stroke="#888780" stroke-width="2" stroke-dasharray="4 4"/>')
            a(f'<text class="ts" x="{xx(3.75)+10}" y="{yy(10)+4}" style="font-size:11px">below: not known</text>')
        # dimension 3.5 / 3.25
        a(f'<line x1="{xx(5.2)}" y1="{yy(step)}" x2="{xx(5.2)}" y2="{yy(htop)}" class="arr" marker-start="url(#ar4)" marker-end="url(#ar4)"/>')
        a(f'<text class="th" x="{xx(5.2)+8}" y="{yy((step+htop)/2)+4}" style="font-size:12px;fill:#5F5E5A">{stepnote}</text>')
        a(f'<text class="ts" x="{xx(0)}" y="{yy(4)+22}" style="font-size:11px">inches up from the floor on the left; depth in from the body across</text>') if False else None
    panel(60,'Through L2 (same top for L1 to L5; L4 and L5 start higher)',19.5,10.5,23.0,'3.5 in','L2')
    panel(350,'Through L7 (same for L6, L8)',19.75,2.75,23.25,'3.5 in','L7')
    a('</svg>')
    return '\n'.join(o)

html=open((ROOT+'/sides.html')).read()
blk='''<h3>D. How the lower wall steps in (shape confirmed by you)</h3>
<div class="wide">'''+section_d()+'''</div>
<p>Side view, outside of the van on the left. Below the pan: a 1 1/2 in strip (and the same above the pan) 1/8 in off the body, then the wall is 1 1/2 in off the body, then it steps out to 3 3/4 in deep at a height 3 1/2 in above the top of each L hole, and the hole is cut in that deeper surface. The shape, depths and the 3 1/2 in distance are confirmed by you, and the same 3 1/2 in step applies above L6, L7 and L8. For those three, the holes are measured (2.75 to 19.75 in up), so the step is at 23.25 in up. L1 to L5 are measured (bottoms 10.5 in for L1 to L3 and 13.75 in for L4 and L5, tops 19.5 in), so their step is at 23 in up. L6 to L8 (2.75 to 19.75 in up) step in at 23.25 in. The 3 3/4 in band I had drawn above R1 was wrong, so it is removed; R1 only has its own ring of steel around it.</p>
'''
html=html.replace('<h2>2. Passenger side</h2>',blk+'\n<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)

html=open((ROOT+'/sides.html')).read()
blk='''<h3>Driver side: built items</h3>
<div class="wide">'''+svg2+'''</div>
<p><b>Battery.</b> The 21 x 10 x 9.5 in battery (280 Ah, taken as 12 V) sits on the floor next to the wheel well, on its aisle side, 1 in from the closet (52 to 73 in from the back). The well sticks out 7 in and the battery adds 10 in, so the two together reach 17 in into the van, which leaves 10 in of the bed's 27 in depth for storage. The battery is 9.5 in tall, so it clears the underside of the bed deck (12 1/2 in up) by 3 in. The looking-down view below shows the depths.</p>
<p><b>Closet rods.</b> Two rods run along the wall inside the closet (74 to 89 in from the back, 15 wide by 25 deep), one above the other: the upper one at 71 in up and the lower one at 36 in up, each about 11 in long (76 to 87). The hangers sit across the 25 in depth, 1 1/2 in apart, so each rod holds about 7 or 8 garments, 14 to 16 in all. The gap between the rods is 35 in, so only short garments fit: about 32 in or less on top and about 30 in or less below. Long coats and dresses do not fit.</p>
<p>The bed, closet, dinette and wall cabinets, drawn on their own so they do not cover the wall details above. They were measured from the rear doors earlier; check whether they use the same zero as the wall numbers (about 6 in in from the rear edge).</p>
'''
html=html.replace('<h2>Depth sections</h2>',blk+'\n<h2>Depth sections</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)

def section_e():
    S=6.0; X0=50; FL=540
    xx=lambda i:X0+S*i
    yy=lambda h:FL-S*h
    o=[]; a=o.append
    W=xx(160)+60
    a(f'<svg viewBox="0 0 {W:.0f} {FL+80}" role="img"><title>Driver side: outlines with depths</title>')
    a(f'<text class="ts" x="{X0}" y="22" style="font-size:14px">Driver side wall, outlines only. Each label is how far that part is from the body (the outer skin) toward the inside of the van.</text>')
    for i in range(0,161,10):
        a(f'<line x1="{xx(i)}" y1="{yy(83)}" x2="{xx(i)}" y2="{FL}" stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"/>')
    for h in range(0,84,10):
        a(f'<line x1="{xx(0)}" y1="{yy(h)}" x2="{xx(160)}" y2="{yy(h)}" stroke="#B4B2A9" stroke-width="0.4" stroke-dasharray="2 4"/><text class="ts" x="{xx(0)-6}" y="{yy(h)+4}" text-anchor="end" style="font-size:11px">{h}</text>')
    a(f'<rect x="{xx(0)}" y="{yy(79)}" width="{S*154}" height="{S*79}" fill="none" stroke="#5F5E5A" stroke-width="1.2"/>')
    def shape(x0,x1,h0,h1,txt,kind='hole',fs=11,sub=None):
        st={'hole':'fill="none" stroke="#BA7517" stroke-width="1.6"','region':'fill="none" stroke="#5F5E5A" stroke-width="1" stroke-dasharray="5 3"','pan':'fill="none" stroke="#444441" stroke-width="1.2"','rib':'fill="none" stroke="#888780" stroke-width="1"','unk':'fill="none" stroke="#B4B2A9" stroke-width="1" stroke-dasharray="2 3"'}[kind]
        a(f'<rect x="{xx(x0):.1f}" y="{yy(h1):.1f}" width="{S*(x1-x0):.1f}" height="{S*(h1-h0):.1f}" rx="3" {st}/>')
        cx=xx((x0+x1)/2); cy=yy((h0+h1)/2)+4
        a(f'<text class="th" x="{cx:.1f}" y="{cy:.1f}" text-anchor="middle" style="font-size:{fs}px;paint-order:stroke;stroke:#fff;stroke-width:3px">{txt}</text>')
    pans=[(6,16),(19.5,29.75),(32.75,43),(46,56.25),(61,69.625),(73,81.25),(84.625,93.25),(104.5,113.625),(116.25,125.5),(129,138.25),(141.25,150.375)]
    for i,(l,r) in enumerate(pans):
        shape(l,r,31,56.5,f'P{i+1}<tspan x="{xx((l+r)/2):.1f}" dy="14">0 in</tspan>','pan',11)
    for i,j in ((0,1),(1,2),(2,3),(4,5),(5,6),(7,8),(8,9),(9,10)):
        l,r=pans[i][1],pans[j][0]
        a(f'<rect x="{xx(l):.1f}" y="{yy(56.5):.1f}" width="{S*(r-l):.1f}" height="{S*25.5:.1f}" fill="none" stroke="#888780" stroke-width="1"/>')
        a(f'<text class="ts" x="{xx((l+r)/2):.1f}" y="{yy(52):.1f}" text-anchor="middle" style="font-size:10px">1/8</text>')
    # strip under pans
    shape(6,150.375,29.5,31,'1/8 in','rib',10)
    shape(6,150.375,56.5,58,'1/8 in','rib',10)
    # 2 in zone
    shape(6,150.375,23.25,29.5,'','region',12)
    a(f'<text class="th" x="{xx(141):.1f}" y="{yy(26.4)+4:.1f}" text-anchor="middle" style="font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:3px">2 in</text>')
    # 3 3/4 bands above holes
    shape(20,79,19.5,23.0,'3 3/4 in','region',11)
    shape(105.85,153.5,19.75,23.25,'3 3/4 in','region',11)
    # holes
    L=[('L1',20,29.25,10.5,19.5),('L2',32.25,38,10.5,19.5),('L3',42,50.75,10.5,19.5),('L4',57,62,13.75,19.5),('L5',66,79,13.75,19.5),('L6',105.85,117.1,2.75,19.75),('L7',121.6,137.7,2.75,19.75),('L8',142.2,153.5,2.75,19.75)]
    for n,l,r,h0,h1 in L:
        shape(l,r,h0,h1,f'{n}<tspan x="{xx((l+r)/2):.1f}" dy="13">3 3/4 around</tspan>','hole',10)
    a(f'<circle cx="{xx(87.75):.1f}" cy="{yy(17.25):.1f}" r="{S*5.25:.1f}" fill="none" stroke="#BA7517" stroke-width="1.6"/>')
    a(f'<text class="th" x="{xx(87.75):.1f}" y="{yy(17.25)-2:.1f}" text-anchor="middle" style="font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:3px">R1<tspan x="{xx(87.75):.1f}" dy="13">3 3/4 around</tspan></text>')
    a(f'<circle cx="{xx(92.3):.1f}" cy="{yy(11.5):.1f}" r="{S:.1f}" fill="none" stroke="#BA7517" stroke-width="1.4"/><text class="ts" x="{xx(96):.1f}" y="{yy(15.3):.1f}" style="font-size:10px">R2 3 3/4</text>')
    shape(1.5,48,4,9,'LO  2 1/2 in around','hole',11)
    shape(4.75,13.25,10.75,16.75,'CP<tspan x="'+f'{xx(9):.1f}'+'" dy="13">1 3/4 in</tspan>','hole',10)
    shape(99.5,102.1,6.5,13.5,'PO','hole',9)
    shape(71,97,4,9,'LP  3 3/4 around','hole',11)
    # ovals
    for k,l in enumerate((43.75,56,66.25,76.75,87),1):
        a(f'<ellipse cx="{xx(l+0.875):.1f}" cy="{yy(25.3):.1f}" rx="{S*0.875:.1f}" ry="{S*0.55:.1f}" fill="none" stroke="#BA7517" stroke-width="1.4"/>')
        a(f'<text class="ts" x="{xx(l+0.875):.1f}" y="{yy(25.3)-8:.1f}" text-anchor="middle" style="font-size:9px">S{k}  ?</text>')
    # top holes
    T=[('T1',4,6.75,67.875,74.5),('T2',9,19.5,67,74.5),('T3',27.25,40,67,74.5),('T4',42.5,56.25,67.25,76.25),('T5',62.75,73.75,67.25,76.25),('T6',76.75,89.75,67.25,76.25),('T7',93.5,96.25,69.75,73.25),('T8',106,110.75,67.5,69.5),('T8a',103.75,109.75,74.5,76.5),('T9',113.75,124.375,67.5,74),('T10',130.125,139.125,67.5,73.75)]
    for n,l,r,h0,h1 in T:
        small=(r-l)<8
        if small:
            a(f'<rect x="{xx(l):.1f}" y="{yy(h1):.1f}" width="{S*(r-l):.1f}" height="{S*(h1-h0):.1f}" fill="none" stroke="#BA7517" stroke-width="1.4"/>')
            a(f'<text class="ts" x="{xx((l+r)/2):.1f}" y="{yy(h1)-4:.1f}" text-anchor="middle" style="font-size:9px">{n}</text>')
        else:
            shape(l,r,h0,h1,f'{n}<tspan x="{xx((l+r)/2):.1f}" dy="13">3 - 3 3/4 around</tspan>','hole',9)
    a(f'<rect x="{xx(90.25):.1f}" y="{yy(63):.1f}" width="{S*2:.1f}" height="{S*2.75:.1f}" fill="none" stroke="#BA7517" stroke-width="1.4"/><text class="ts" x="{xx(91.25):.1f}" y="{yy(63)-4:.1f}" text-anchor="middle" style="font-size:9px">B1 ?</text>')
    a(f'<rect x="{xx(101.25):.1f}" y="{yy(63):.1f}" width="{S*3.75:.1f}" height="{S*2.75:.1f}" fill="none" stroke="#BA7517" stroke-width="1.4"/><text class="ts" x="{xx(103.1):.1f}" y="{yy(63)-4:.1f}" text-anchor="middle" style="font-size:9px">B2 ?</text>')
    shape(0,154,0,5,'','region',11)
    a(f'<text class="th" x="{xx(115):.1f}" y="{yy(1.6):.1f}" text-anchor="middle" style="font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:3px">1 in, from 5 in up down to the floor</text>')
    # wheel well
    WW=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
    a('<polygon points="'+' '.join(f'{xx(x):.1f},{yy(h):.1f}' for x,h in WW)+'" fill="none" stroke="#A32D2D" stroke-width="1.6" stroke-dasharray="5 3"/>')
    a(f'<text class="th" x="{xx(59):.1f}" y="{yy(3.4):.1f}" text-anchor="middle" style="font-size:11px;fill:#791F1F">wheel well, sticks out 7 in</text>')
    # unknown low zone
    a(f'<text class="ts" x="{xx(125)}" y="{yy(0.6)}" text-anchor="middle" style="font-size:10px"></text>')
    a(f'<text class="th" x="{xx(6)}" y="{yy(28.3)+4:.1f}" style="font-size:10px">1 in at the back and at the cab end</text>')
    # cab wall
    a(f'<line x1="{xx(154)}" y1="{yy(79)}" x2="{xx(154)}" y2="{FL}" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="6 3"/>')
    yb=FL+16
    a(f'<line x1="{xx(0)}" y1="{yb}" x2="{xx(154)}" y2="{yb}" stroke="#888780" stroke-width="0.6"/>')
    for t in range(0,161,10):
        a(f'<line x1="{xx(t)}" y1="{yb-4}" x2="{xx(t)}" y2="{yb+4}" stroke="#888780" stroke-width="0.6"/><text class="ts" x="{xx(t)}" y="{yb+18}" text-anchor="middle" style="font-size:11px">{t}</text>')
    a(f'<text class="ts" x="{xx(77)}" y="{yb+36}" text-anchor="middle" style="font-size:12px">inches from where you start measuring at the back</text>')
    a('</svg>')
    return '\n'.join(o)

html=open((ROOT+'/sides.html')).read()
blk='''<h2>1c. Driver side, outlines with depths</h2>
<div class="wide">'''+section_e()+'''</div>
<p>Depth means how far the surface is from the body (the outer skin) toward the inside of the van. Pans are the body (0 in); the 3 in ribs, and the 1 1/2 in strips above and below the pans, are 1/8 in off it; the belt-line wall is 1 1/2 in off. For the holes, the depth is the steel around the hole, not inside it (inside you see the body): around L and R, and the band above them, it is 3 3/4 in; around LO 2 1/2 in; around CP 1 3/4 in; around the top holes it is 3 in at the top edge and 3 3/4 in at the bottom edge. The ovals (S), B1 and B2 have no depth yet (marked ?). The 1 1/2 in band steps in to 1 in at the back and at the cab end.</p>
'''
html=html.replace('<h2>Depth sections</h2>',blk+'\n<h2>Depth sections</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)

# ---- redo 1c: holes read 0 in, surrounding steel color coded by depth ----
C={'0':'#CFCDC6','1/8':'#FFF1A8','1':'#BDE8A8','1.5':'#A9D4F5','2.5':'#FBDCDC','3':'#F5B9B9','3.75':'#E88A8A','4':'#D96868','7':'#D8B79A'}
ADJ={}
def _adjL(L):
    bots=ADJ.get('lbot',{})
    if bots:
        L=[(r[0],r[1],r[2],bots.get(r[0],r[3]),r[4]) for r in L]
    if not ADJ.get('l1split'): return L
    out=[]
    for row in L:
        if row[0]=='L1':
            n,l,r,h0,h1=row
            mid=(l+r)/2
            out+= [('L1a',12.5,21.5,9.75,18.5),('L1b',23,29.5,9.75,18.5)] if ADJ.get('l1a') else [('L1a',l,mid-0.4,h0,h1),('L1b',mid+0.4,r,h0,h1)]
        else: out.append(row)
    return out
def section_e2():
    cp=ADJ.get('cp',(4.75,13.25)); cpd=ADJ.get('cpdepth','1.5'); cph=ADJ.get('cph',(10.75,16.75))
    S=6.0; X0=50; FL=540
    xx=lambda i:X0+S*i
    yy=lambda h:FL-S*h
    o=[]; a=o.append
    W=xx(160)+60
    a(f'<svg viewBox="0 0 {W:.0f} {FL+96}" role="img"><title>Driver side: depths color coded</title>')
    a('<defs><pattern id="unk" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#B4B2A9" stroke-width="1"/></pattern><linearGradient id="gr25" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="'+C['2.5']+'"/><stop offset="1" stop-color="'+C['3.75']+'"/></linearGradient><pattern id="hatch2" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#888780" stroke-width="1"/></pattern><linearGradient id="gr34" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+C['3']+'"/><stop offset="0.9286" stop-color="'+C['3.75']+'"/><stop offset="1" stop-color="'+C['1/8']+'"/></linearGradient><linearGradient id="gr34b" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+C['3']+'"/><stop offset="1" stop-color="'+C['3.75']+'"/></linearGradient><linearGradient id="grv" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="'+C['3.75']+'"/><stop offset="1" stop-color="'+C['2.5']+'"/></linearGradient><linearGradient id="gr25r" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="'+C['3.75']+'"/><stop offset="1" stop-color="'+C['2.5']+'"/></linearGradient></defs>')
    a(f'<text class="ts" x="{X0}" y="22" style="font-size:14px">Driver side wall. Inside every hole you see the body. The steel around it is colored by how far it is from the body.</text>')
    for i in range(0,161,10):
        a(f'<line x1="{xx(i)}" y1="{yy(83)}" x2="{xx(i)}" y2="{FL}" stroke="#D3D1C7" stroke-width="0.4" stroke-dasharray="2 4"/>')
    for h in range(0,84,10):
        a(f'<line x1="{xx(0)}" y1="{yy(h)}" x2="{xx(160)}" y2="{yy(h)}" stroke="#D3D1C7" stroke-width="0.4" stroke-dasharray="2 4"/>')
        a(f'<text x="{xx(0)-6}" y="{yy(h)+4}" text-anchor="end" style="font-size:11px;font-weight:700;fill:#8A4B0F">{h}\u2191</text>')
    a(f'<rect x="{xx(0)}" y="{yy(79)}" width="{S*154}" height="{S*79}" fill="url(#unk)" fill-opacity="0.5" stroke="#5F5E5A" stroke-width="1.2"/>')
    def rect(x0,x1,h0,h1,col,extra='',rx=3):
        a(f'<rect x="{xx(x0):.1f}" y="{yy(h1):.1f}" width="{S*(x1-x0):.1f}" height="{S*(h1-h0):.1f}" rx="{rx}" fill="{col}" {extra}/>')
    def txt(x,h,t,fs=11,col='#2C2C2A',anchor='middle'):
        a(f'<text class="th" x="{xx(x):.1f}" y="{yy(h):.1f}" text-anchor="{anchor}" style="font-size:{fs}px;fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-opacity:.8">{t}</text>')
    def hole(x0,x1,h0,h1,name,fs=11,tcol='#2C2C2A'):
        rect(x0,x1,h0,h1,C['0'],'stroke="#6F6E69" stroke-width="1"',3)
        cx=xx((x0+x1)/2); cy=yy((h0+h1)/2)
        a(f'<text class="th" x="{cx:.1f}" y="{cy-1:.1f}" text-anchor="middle" style="font-size:{fs}px;fill:{tcol}">{name}</text>')
    # steel by depth
    rect(6,15,5,23.25,C[cpd],'',1)                              # CP area filled up to the 1 1/2 band
    rect(15,56,0,23.25,'url(#gr25)','',1)                          # light 2 1/2 around L1, L2, getting darker
    rect(56,154,0,23.25,C['3.75'],'',1)                            # then 3 3/4 in to the cab
    rect(150.375,154,23.25,58,C['1/8'],'',1)                      # right of P11 up to the cab wall, 1/8 in
    rect(56.25,61,31,56.5,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)   # gap between P4 and P5, 1/8 in
    rect(0,15,0,5,C['2.5'],'',1)                                 # bottom 5 in toward the back, 3 3/4 in
    rect(6,150.375,23.25,29.5,C['1.5'],'',1)                       # belt line wall, 2 in
    rect(6,150.375,29.5,31,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)
    rect(6,11,29.5,31,C['1.5'],'',1)                              # blue only under the angle (6 to 11), yellow again from 11 to 16
    rect(6,150.375,56.5,58,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)
    pans=[(6,16),(19.5,29.75),(32.75,43),(46,56.25),(61,69.625),(73,81.25),(84.625,93.25),(104.5,113.625),(116.25,125.5),(129,138.25),(141.25,150.375)]
    for i,j in ((0,1),(1,2),(2,3),(4,5),(5,6),(7,8),(8,9),(9,10)):
        rect(pans[i][1],pans[j][0],31,56.5,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)
    # bands and rings around holes
    rect(105.85,153.5,19.75,23.25,C['3.75'],'',2)
    PAD=1.25
    def ring(l,r,h0,h1,key):
        rect(l-PAD,r+PAD,h0-PAD,h1+PAD,C[key],'',4)
    L=[('L1',20,29.25,10.5,19.5),('L2',32.25,38,10.5,19.5),('L3',42,50.75,10.5,19.5),('L4',57,62,13.75,19.5),('L5',66,79,13.75,19.5),('L6',105.85,117.1,2.75,19.75),('L7',121.6,137.7,2.75,19.75),('L8',142.2,153.5,2.75,19.75)]
    L=_adjL(L)
    for n,l,r,h0,h1 in L:
        if n not in ('L1','L2','L3','L4'): ring(l,r,h0,h1,'3.75')
    a(f'<circle cx="{xx(87.75):.1f}" cy="{yy(17.25):.1f}" r="{S*(5.25+PAD):.1f}" fill="{C["3.75"]}"/>')
    ring(71,97,4,9,'3.75')
    TOP=[('T1',4,6.75,67.875,74.5),('T2',9,19.5,67,74.5),('T3',27.25,40,67,74.5),('T4',42.5,56.25,67.25,76.25),('T5',62.75,73.75,67.25,76.25),('T6',76.75,89.75,67.25,76.25),('T7',93.5,96.25,69.75,73.25),('T8',106,110.75,67.5,69.5),('T8a',103.75,109.75,74.5,76.5),('T9',113.75,124.375,67.5,74),('T10',130.125,139.125,67.5,73.75)]
    rect(93.25,104.5,0,59.5,C['3.75'],'',1)                       # space between P7 and P8, 3 3/4 in, all the way down to the floor
    rect(93.25,96.25,31,56.5,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)      # 3 in right of P7, 1/8 in like the other sides
    rect(101.5,104.5,31,56.5,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)      # 3 in left of P8, 1/8 in like the other sides
    rect(0,154,58,79,'url(#gr34)','',1)
    rect(93.25,104.5,58,79,'url(#gr34b)','',1)                      # the P7-P8 strip goes all the way up, 3 3/4 in shading to 3 in at the top                            # top part, 19.5 in from the top down, shades 3 in (top) to 4 in
    # plate CP (a plate, 1 3/4 in)
    ring(cp[0],cp[1],cph[0],cph[1],cpd)
    rect(0,3,0,23.25,C['3.75'],'',1)                            # bottom left: 3 3/4 under the red, shading to 2 1/2 at the floor
    rect(0,3,23.25,58,C['3.75'],'',1)                              # 3 3/4 in starts 3 in left of P1 and goes to the back
    rect(3,6,0,58,C['1/8'],'stroke="#C4B79A" stroke-width="0.6"',1)   # the 3 in left of P1 is 1/8 in
    rect(3,6,0,9,C['2.5'],'',1)                                    # bottom left part around x=4, up to the top of LO, 2 1/2 in
    rect(3,6,9,36.7,C['1.5'],'',1)
    rect(0,3,23.25,36.7,C['1.5'],'',1)                             # to the left of the angle's bottom corner, 1 1/2 in                                 # P1 bottom-left corner area, 1 1/2 in, down to the top of LO, not above where the angle ends
    hole(1.5,48,4,9,'LO',11)          # LO and LP are behind the wheel well
    hole(71,97,4,9,'LP',11)
    # wheel well (7 in)
    WW=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
    a('<polygon points="'+' '.join(f'{xx(x):.1f},{yy(h):.1f}' for x,h in WW)+f'" fill="{C["7"]}" stroke="#8A6B4D" stroke-width="1.2" stroke-linejoin="round"/>')
    a(f'<text class="th" x="{xx(59):.1f}" y="{yy(3.2):.1f}" text-anchor="middle" style="font-size:11px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:3px">wheel well 7 in</text>')
    a(f'<polygon points="{xx(6):.1f},{yy(36.7):.1f} {xx(11):.1f},{yy(31):.1f} {xx(6):.1f},{yy(31):.1f}" fill="{C["1.5"]}"/>')
    # pans (0 in)
    for i,(l,r) in enumerate(pans):
        if i==0:
            a(f'<polygon points="{xx(6):.1f},{yy(36.7):.1f} {xx(11):.1f},{yy(31):.1f} {xx(16):.1f},{yy(31):.1f} {xx(16):.1f},{yy(56.5):.1f} {xx(6):.1f},{yy(56.5):.1f}" fill="{C["0"]}" stroke="#6F6E69" stroke-width="1" stroke-linejoin="round"/>')
            a(f'<text class="th" x="{xx(11):.1f}" y="{yy(43.75)-1:.1f}" text-anchor="middle" style="font-size:12px;fill:#2C2C2A">P1</text>')
        else:
            hole(l,r,31,56.5,f'P{i+1}',12)
    # holes, all 0 in
    for n,l,r,h0,h1 in L: hole(l,r,h0,h1,n,10)
    a(f'<circle cx="{xx(87.75):.1f}" cy="{yy(17.25):.1f}" r="{S*5.25:.1f}" fill="{C["0"]}" stroke="#2C2C2A" stroke-width="1"/>')
    a(f'<text class="th" x="{xx(87.75):.1f}" y="{yy(17.25)-1:.1f}" text-anchor="middle" style="font-size:11px;fill:#2C2C2A">R1</text>')
    a(f'<circle cx="{xx(92.3):.1f}" cy="{yy(11.5):.1f}" r="{S:.1f}" fill="{C["0"]}" stroke="#6F6E69"/><text class="ts" x="{xx(96):.1f}" y="{yy(15.3):.1f}" style="font-size:10px">R2</text>')
    hole(cp[0],cp[1],cph[0],cph[1],'CP',10)
    hole(99.5,102.1,6.5,13.5,'PO',8)
    for n,l,r,h0,h1 in TOP:
        if (r-l)>=8: hole(l,r,h0,h1,n,10)
        else:
            rect(l,r,h0,h1,C['0'],'stroke="#6F6E69"',2); txt((l+r)/2,h1+1.4,n,9)
    hole(103.75,109.75,74.5,76.5,'',8); txt(106.75,78,'T8a',9)
    # ovals, unknown ring
    for k,l in enumerate((43.75,56,66.25,76.75,87),1):
        hw=0.875; cxv=l+0.875
        if k==1 and ADJ.get('s1'):
            hw=(ADJ['s1'][1]-ADJ['s1'][0])/2; cxv=(ADJ['s1'][0]+ADJ['s1'][1])/2
        cyv=25.3; ryv=0.55; lab_h=27.5
        if k==1 and ADJ.get('s1h'):
            cyv=(ADJ['s1h'][0]+ADJ['s1h'][1])/2; ryv=(ADJ['s1h'][1]-ADJ['s1h'][0])/2; lab_h=ADJ['s1h'][1]+1.4
        if k==1 and ADJ.get('s1h'):
            a(f'<rect x="{xx(cxv-hw):.1f}" y="{yy(cyv+ryv):.1f}" width="{S*2*hw:.1f}" height="{S*2*ryv:.1f}" rx="3" fill="{C["0"]}" stroke="#6F6E69" stroke-width="1"/>')
        else:
            a(f'<ellipse cx="{xx(cxv):.1f}" cy="{yy(cyv):.1f}" rx="{S*hw:.1f}" ry="{S*ryv:.1f}" fill="{C["0"]}" stroke="#6F6E69" stroke-width="1"/>')
        txt(cxv,lab_h,f'S{k}',9)
    # B1, B2, LP: depth unknown around, 0 inside
    rect(90.25,92.25,60.25,63,C['0'],'stroke="#6F6E69" stroke-width="1"',2); txt(91.25,64.3,'B1',9)
    rect(101.25,105,60.25,63,C['0'],'stroke="#6F6E69" stroke-width="1"',2); txt(103.1,64.3,'B2',9)
    # labels on areas
    txt(141,26.4,'1 1/2 in',12)
    txt(30,30,'1/8 in strip',9)
    # grid lines every 10 in across the whole diagram, on top of the colors but light
    for t in range(0,155,10):
        a(f'<line x1="{xx(t)}" y1="{yy(79)}" x2="{xx(t)}" y2="{FL}" stroke="#2C2C2A" stroke-opacity="0.22" stroke-width="0.9"/>')
    for h in range(0,80,10):
        a(f'<line x1="{xx(0)}" y1="{yy(h)}" x2="{xx(154)}" y2="{yy(h)}" stroke="#2C2C2A" stroke-opacity="0.22" stroke-width="0.9"/>')
    # inch marks every 20 in throughout the diagram: blue arrows = inches from the back, boxed brown up-arrows = inches up from the floor
    for t in range(20,150,20):
        for h in (10,30,50,70):
            a(f'<text x="{xx(t)+2:.1f}" y="{yy(h)+3:.1f}" style="font-size:10px;font-weight:600;fill:#185FA5;paint-order:stroke;stroke:#fff;stroke-width:2.5px;stroke-opacity:.8">{t}\u2192</text>')
    for h in (20,40,60):
        for t in (10,50,90,130):
            a(f'<text x="{xx(t)+2:.1f}" y="{yy(h)-3:.1f}" style="font-size:10px;font-weight:700;fill:#8A4B0F;paint-order:stroke;stroke:#fff;stroke-width:2.5px;stroke-opacity:.8">{h}\u2191</text>')
    a(f'<text class="ts" x="{xx(0)}" y="{FL+88}" style="font-size:11px"><tspan style="fill:#185FA5;font-weight:600">blue numbers with an arrow \u2192</tspan> = inches from the back; <tspan style="fill:#8A4B0F;font-weight:700">brown numbers with \u2191</tspan> = inches up from the floor (marked every 20 in)</text>')
    # seam / pillar, wiring harness, cab-end allowance
    a(f'<rect x="{xx(98.9):.1f}" y="{yy(17.8):.1f}" width="{S*4.8:.1f}" height="{S*17.8:.1f}" fill="none" stroke="#5F5E5A" stroke-width="1.2"/>')
    a(f'<line x1="{xx(98.3)}" y1="{yy(72)}" x2="{xx(98.3)}" y2="{FL}" stroke="#993C1D" stroke-width="1.6" stroke-dasharray="7 4"/>')
    a(f'<text class="th" x="{xx(98.3)}" y="{FL+70}" text-anchor="middle" style="fill:#993C1D;font-size:12px">seam / pillar, about 98</text>')
    if not ADJ.get('noharness'):
        a(f'<path d="M{xx(93.25)} {yy(63.5)} Q {xx(115)} {yy(63)} {xx(125)} {yy(65)} T {xx(152)} {yy(66.5)}" fill="none" stroke="#2C2C2A" stroke-width="3" stroke-dasharray="6 2"/>')
        a(f'<text class="ts" x="{xx(125)}" y="{yy(67.8)}" text-anchor="middle" style="font-size:11px">wiring harness</text>')
    a(f'<rect x="{xx(150)}" y="{yy(79)}" width="{S*8}" height="{S*79}" fill="url(#hatch2)" fill-opacity="0.4"/>')
    a(f'<rect x="{xx(152)}" y="{yy(79)}" width="{S*4}" height="{S*79}" fill="url(#hatch2)" fill-opacity="0.4"/>')
    a(f'<text class="ts" x="{xx(154)-4}" y="{yy(79)-12}" text-anchor="end" style="font-size:11px">cab wall about 154; could be 150 to 158 (cab-end numbers may be off by 2 to 4 in)</text>')
    a(f'<text class="ts" x="{xx(160)}" y="{yy(82)-5}" text-anchor="end" style="font-size:11px">top part: roof structure above the wall</text>')
    # cab wall
    a(f'<line x1="{xx(154)}" y1="{yy(79)}" x2="{xx(154)}" y2="{FL}" stroke="#5F5E5A" stroke-width="2" stroke-dasharray="6 3"/>')
    yb=FL+16
    a(f'<line x1="{xx(0)}" y1="{yb}" x2="{xx(154)}" y2="{yb}" stroke="#888780" stroke-width="0.6"/>')
    for t in range(0,161,10):
        a(f'<line x1="{xx(t)}" y1="{yb-4}" x2="{xx(t)}" y2="{yb+4}" stroke="#888780" stroke-width="0.6"/><text x="{xx(t)}" y="{yb+18}" text-anchor="middle" style="font-size:11px;font-weight:700;fill:#185FA5">{t}\u2192</text>')
    a(f'<text class="ts" x="{xx(77)}" y="{yb+36}" text-anchor="middle" style="font-size:12px">inches from where you start measuring at the back</text>')
    a('</svg>')
    return '\n'.join(o)

html=open((ROOT+'/sides.html')).read()
i=html.index('<h2>1c.'); j=html.index('<h2>Depth sections')
labels=[('0','0 in: the body (pans, and inside every hole)'),('1/8','1/8 in'),('1.5','1 1/2 in'),('2.5','2 1/2 in'),('3.75','3 3/4 in'),('7','7 in (wheel well)')]
legend=''.join(f'<span><i class="sw" style="background:{C[k]}"></i>{t}</span>' for k,t in labels)+'<span><i class="sw" style="background:linear-gradient(180deg,'+C['3']+','+C['3.75']+')"></i>3 in at the top getting darker to 3 3/4 in (the top 19 1/2 in)</span><span><i class="sw" style="background:linear-gradient(90deg,'+C['2.5']+','+C['3.75']+')"></i>2 1/2 in lightest, getting darker to 3 3/4 in</span>'+'<span><i class="sw" style="background:repeating-linear-gradient(45deg,#fff,#fff 3px,#B4B2A9 3px,#B4B2A9 4px)"></i>depth not measured</span>'
blk='<h3>Driver side wall: depth color map</h3>\n<div class="wide">'+section_e2()+'</div>\n<p class="legend">'+legend+'</p>\n<p>Every hole (and every pan) reads 0 in, because inside it you see the body. The color around a hole is how far that steel is from the body: 3 3/4 in around the L and R holes and the band above the L holes, the top 19 1/2 in of the wall (around the T holes) shades from 3 in at the top to 3 3/4 in at the bottom, 1 1/2 in for the belt-line wall and around the cover plate CP (inside it, 0 in), the strip along the back (0 to 3 in from the back) is 3 3/4 in from the floor up, the 3 in left of P1 is 1/8 in and then it goes to 3 3/4 in toward the back (above 23 1/4 in up), and 3 3/4 in from 56 in to the cab, for everything under the 1 1/2 in band, and for the space between P7 and P8 (except the 3 in right of P7 and the 3 in left of P8 on the pan rows, which are 1/8 in like the other sides), which is 3 3/4 in from the floor all the way up and shades to 3 in at the top; from 15 in to 56 in (around L1 to L4) it shades from 2 1/2 in at the lightest, getting darker toward 3 3/4 in, 1/8 in for the ribs and the 1 1/2 in strips above and below the pans. The area right of P11, up to the cab wall, is 1/8 in. The gap between P4 and P5 is 1/8 in too. Hatched areas have no depth yet (around the ovals, B1 and B2). The steel behind the wheel well (around LO) starts at 2 1/2 in and shades darker with the rest toward 3 3/4 in; the area in front of it (around LP) is 3 3/4 in. The 1 1/2 in band steps in to 1 in at the back and at the cab end.</p>\n\n'
html=html[:i]+html[j:]
html=html.replace('<h2>1. Driver side</h2>\n','<h2>1. Driver side</h2>\n'+blk,1)
open((ROOT+'/sides.html'),'w').write(html)

# ---- passenger side: start as a copy of the driver side dimensions ----
def passenger(svgtxt):
    t=svgtxt
    t=t.replace('Driver side wall: steel map with layout','Passenger side wall: steel map (copied from the driver side)').replace('Driver side: depths color coded','Passenger side: depths color coded (copied from the driver side)')
    t=t.replace('Driver side wall seen from the aisle. Rear doors on the left, cab on the right.','Passenger side wall, copied from the driver side as a starting point (not measured yet). Rear on the left, cab on the right.')
    t=t.replace('Driver side wall. Inside every hole you see the body. The steel around it is colored by how far it is from the body.','Passenger side, seen from inside the van: cab on the left, rear on the right.')
    PS=6.0; PX0=50; PFL=540
    px=lambda i:PX0+PS*i; py=lambda h:PFL-PS*h
    door=(f'<rect x="{px(104):.1f}" y="{py(67):.1f}" width="{PS*51:.1f}" height="{PS*67:.1f}" fill="#fff" fill-opacity="1" stroke="#BA7517" stroke-width="2" stroke-dasharray="8 4"/>'
          f'<text class="th" x="{px(129.5):.1f}" y="{py(30):.1f}" text-anchor="middle" style="font-size:14px;fill:#854F0B">Sliding door opening</text>'
          f'<text class="ts" x="{px(129.5):.1f}" y="{py(30)+17:.1f}" text-anchor="middle" style="font-size:12px">51 in wide, 104 to 155 in</text>'
          f'<text class="ts" x="{px(129.5):.1f}" y="{py(30)+33:.1f}" text-anchor="middle" style="font-size:11px">(rear edge 104 in, measured); empty behind it</text>')
    return t.replace('</svg>',door+'</svg>')
pass1=passenger(svg)
def flip_view(txt):
    import re as _r
    m=_r.search(r'viewBox="0 0 (\d+) (\d+)"',txt); W=int(m.group(1))
    def fix(mm):
        tag=mm.group(0)
        xm=_r.search(r' x="([\d.]+)"',tag)
        if not xm: return tag
        X=xm.group(1)
        if 'text-anchor="end"' in tag: tag=tag.replace('text-anchor="end"','text-anchor="start"')
        elif 'text-anchor="start"' in tag: tag=tag.replace('text-anchor="start"','text-anchor="end"')
        elif 'text-anchor="middle"' in tag: pass
        else: tag=tag[:-1]+' text-anchor="end">'
        return tag[:-1]+f' transform="translate({X},0) scale(-1,1) translate(-{X},0)">'
    t=_r.sub(r'<text [^>]*>',fix,txt)
    t=t.replace('\u2192','\u2190')
    t=_r.sub(r'(<svg [^>]*>)',lambda m_:m_.group(1)+f'<g transform="translate({W},0) scale(-1,1)">',t,count=1)
    t=t.replace('</svg>','</g></svg>')
    return t
ADJ.update({'noharness':True,'cp':(2.5,12),'cpdepth':'2.5','cph':(12,20.25),'l1split':True,'l1a':True,'lbot':{'L2':9.5,'L3':10},'s1':(38.25,47.75),'s1h':(25,27.75)})
pass2=flip_view(passenger(section_e2()))
ADJ.clear()

PASS_NOTES=['<b>Wiring harness:</b> removed on this side (the driver side map still shows it).','<b>CP:</b> 2.5 to 12 in from the back (driver side: 4.75 to 13.25 in), and the steel around it is 2.5 in deep (driver side: 1.5 in). It runs 12 to 20.25 in up from the floor (driver side: 10.75 to 16.75 in), so it is 8 1/4 in tall. The area around it up to the 1 1/2 in band is colored 2.5 in too.','<b>S1</b> is a larger hole on the passenger side: 38.25 to 47.75 in from the back (9 1/2 in wide; the driver side one is 43.75 to 45.5 in). It runs 25 to 27.75 in up from the floor (2 3/4 in tall; the driver side one is 24.75 to about 25.85 in), and it is more rectangular than the driver side ovals, so I drew it as a rectangle with slightly rounded corners. The depth around it is still to come.','<b>L2 and L3:</b> their bottoms are 9.5 in (L2) and 10 in (L3) up from the floor, about 1 in and 1/2 in lower than the driver side (10.5 in). Their tops are assumed to stay at 19.5 in, and their positions across are the same as the driver side.','<b>L1 is two areas on the passenger side,</b> labeled <b>L1a</b> and <b>L1b</b> (L1a is the one nearer the back). <b>L1a</b> is 12.5 to 21.5 in from the back (9 in wide) and 9.75 to 18.5 in up from the floor, the same height as L1b (8 3/4 in tall); its depth is assumed the same as the driver side. <b>L1b</b> is 23 to 29.5 in from the back (6 1/2 in wide) and 9.75 to 18.5 in up from the floor (8 3/4 in tall), both measured. The gap between L1a and L1b is 1 1/2 in. Depth around both is assumed the same as the driver side.']
html=open((ROOT+'/sides.html')).read()
old='<h2>2. Passenger side</h2>\n<p>Waiting for the passenger side photos.</p>'
assert old in html
new='<h2>2. Passenger side</h2>\n<p>This wall is the same as the driver side, with a few adjustments you will tell me about. Until then every dimension is the driver-side one: pans, ribs, holes, ovals, the lower wall, the wheel well and all the depths. The adjustments are listed below as they come in. The sliding door is the one thing that cannot match, so the area behind it is left empty (51 in wide, 104 to 155 in, up to 58 in; its rear edge at 104 in is measured, the width and height are not).</p>\n<h3>Passenger side wall: depth color map (same as the driver side, adjustments to come)</h3>\n<div class="wide">'+pass2+'</div>\n<p class="legend">'+legend+'</p>\n<h3>Passenger side adjustments</h3>\n<ul>'+''.join('<li>'+x+'</li>' for x in PASS_NOTES)+'</ul>\n'
html=html.replace(old,new,1)
open((ROOT+'/sides.html'),'w').write(html)

# ---- move all the measurement tables to the bottom of the page ----
html=open((ROOT+'/sides.html')).read()
i=html.index('<h3>Top holes: measured and still open</h3>')
j=html.index('<h3>Driver side: built items</h3>')
block=html[i:j]
html=html[:i]+html[j:]
html=html.replace('</body>','<h2>All measurements</h2>\n'+block+'\n</body>',1)
open((ROOT+'/sides.html'),'w').write(html)

# ---- furring layout for vertical planks ----
AP={'S1': [6, 17.75, 31.25, 82.94, 98.9, 119.35, 139.95], 'S2': [15, 30.75, 40, 54, 62, 72, 80, 96, 104, 119.35, 139.95], 'S3': [22, 34, 46, 58, 70, 78, 99, 110, 122, 134, 146], 'S4': [10, 17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75, 147], 'S5': [17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75], 'S6': [10, 17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75, 147], 'S7': [17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75], 'S8': [10, 24, 36, 58.6, 76, 93, 98.9, 114, 127, 140]}
def furring_svg():
    S=6.0; X0=50; FL=540
    xx=lambda i:X0+S*i
    yy=lambda h:FL-S*h
    base=section_e2()
    strips=[('S1',3),('S2',12),('S3',21.4),('S4',30.25),('S5',43.5),('S6',57.25),('S7',66),('S8',76.75)]
    o=[]; a=o.append
    for n,h in strips:
        segs=[(0,154)] if n!='S1' else [(0,42),(76,154)]
        for x0,x1 in segs:
            fill='#7A4A1E' if n in ('S1','S2','S3') else ('url(#spc)' if n in ('S4','S5','S6') else '#D9A05B')
            a(f'<rect x="{xx(x0):.1f}" y="{yy(h+0.75):.1f}" width="{S*(x1-x0):.1f}" height="{S*1.5:.1f}" fill="{fill}" fill-opacity="0.95" stroke="#3E230B" stroke-width="1"/>')
        for px in AP[n]:
            a(f'<circle cx="{xx(px):.1f}" cy="{yy(h):.1f}" r="4.2" fill="#fff" stroke="#3E230B" stroke-width="1.5"/>')
        if n in ('S4','S5','S6'):
            a(f'<text x="{xx(152):.1f}" y="{yy(h)-6:.1f}" text-anchor="end" style="font-size:9px;font-weight:700;fill:#3E230B;paint-order:stroke;stroke:#fff;stroke-width:2.5px">spacer 3 5/8 at each dot</text>')
        a(f'<circle cx="{xx(3):.1f}" cy="{yy(h)-0:.1f}" r="9" fill="#fff" stroke="#3E230B" stroke-width="1.2"/><text x="{xx(3):.1f}" y="{yy(h)+3.5:.1f}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:#3E230B">{n}</text>')
    a(f'<text class="th" x="{xx(59):.1f}" y="{yy(5.6):.1f}" text-anchor="middle" style="font-size:10px;fill:#791F1F;paint-order:stroke;stroke:#fff;stroke-width:3px">box out the wheel well (sticks out 7 in)</text>')
    t=base.replace('Driver side wall. Inside every hole you see the body. The steel around it is colored by how far it is from the body.','Driver side wall: depth colors with the furring strips on top (S1 to S8, white dots are attachment points). Untick the box above to hide the strips.')
    t=t.replace('<defs>','<defs><pattern id="spc" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#C7792A"/><line x1="0" y1="0" x2="0" y2="7" stroke="#FFF1D6" stroke-width="2.5"/></pattern>',1)
    t=t.replace('</svg>','<g id="furr">'+''.join(o)+'</g></svg>')
    return t
rows=[('S1','3 in up','the flat lower wall (3 3/4 in deep); stops at the wheel well, which sticks out 7 in and has to be boxed out','0 (strip sits straight on the steel)'),
('S2','12 in up','the lower wall; it bridges the L, R and PO holes, so anchor it on the steel between them','0; 1 1/4 in at the back, before 15 in'),
('S3','21 1/2 in up','the 3 3/4 in band above the L holes (19 1/2 to 23 in up), a solid line of steel the whole way','0; 2 1/4 in left of 15 in (the 1 1/2 in blue area)'),
('S4','30 1/4 in up','the 1/8 in strip under the pans (29 1/2 to 31 in up)','3 5/8 in'),
('S5','43 1/2 in up','the 3 in ribs between the pans (1/8 in); it bridges the pans between them','3 5/8 in'),
('S6','57 1/4 in up','the 1/8 in strip above the pans (56 1/2 to 58 in up)','3 5/8 in'),
('S7','66 in up','the top part, below the T holes (about 3 1/2 in deep there)','about 1/4 in'),
('S8','76 3/4 in up','the top part, above the T holes (about 3 in deep there)','about 5/8 in')]
tbl='<table><tr><th>Strip</th><th>Height (center)</th><th>What it sits on</th><th>Spacer needed</th><th>Attachment points</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{len(AP[a])} dots, at '+', '.join(f'{v:g}' for v in AP[a])+' in from the back</td></tr>' for a,b,c,d in rows)+'</table>'
blk='''<h3>Driver side: furring layout for vertical planks</h3>
<div class="wide">'''+furring_svg()+'''</div>
<p class="legend"><span><i class="sw" style="background:#7A4A1E"></i>Dark brown strip: sits straight on the steel, no spacer (S1, S2, S3)</span><span><i class="sw" style="background:repeating-linear-gradient(45deg,#C7792A,#C7792A 3px,#FFF1D6 3px,#FFF1D6 5px)"></i>Orange striped strip: needs a 3 5/8 in spacer at every dot (S4, S5, S6)</span><span><i class="sw" style="background:#D9A05B"></i>Light tan strip: needs a small spacer, 1/4 to 5/8 in (S7, S8)</span></p>
<p>Vertical planks need strips that run sideways, so they cross every plank. Eight strips, 3/4 in thick and 1 1/2 in wide, with the planks fixed to them. The strips are spaced 9 to 14 in apart from the floor to the top, so every plank is held at least every 14 in. The "spacer needed" column is how much each strip has to be built up so its back sits on a common line 3 3/4 in off the body, the deepest steel on the wall (the lower wall and the top part). The planks then lie flat against the strips' fronts, 4 1/2 in off the body, with nothing sticking out through them. The wheel well sticks out 7 in, so it needs its own box built around it.</p>
'''+tbl+'''
<p><b>Attachment points.</b> Each white dot on the drawing is a place where the strip is fixed to the van. On S1, S2, S3, S7, and S8 a dot is an adhesive pad (structural adhesive or VHB tape) straight onto the steel, placed on solid steel and kept clear of the holes. On S4 and S6 a dot is a 3 5/8 in spacer block bonded to the 1 1/2 in strip of steel, with the strip screwed to the block. On S5 a dot is a spacer block bonded onto a rib, so S5 touches the van only at the ten ribs, 13 to 16 in apart, and spans the pans between them. This is general van-build practice, so test the adhesive bond on your own steel before you rely on it.</p>
<p>Rough materials, counting 154 in per strip with S1 stopping at the wheel well: about 100 ft of 3/4 x 1 1/2 in strip. Spacers are needed under S4, S5, and S6 at every rib, about 10 per strip. This is a starting layout from your measurements, so check the strip positions against where you want shelves, cabinets, and outlets before you glue anything.</p>
'''
html=open((ROOT+'/sides.html')).read()
# merge: the depth map now carries the furring strips; drop the separate furring diagram
a0=html.index('<h3>Driver side wall: depth color map</h3>')
d0=html.index('<div class="wide">',a0); d1=html.index('</div>',d0)
toggle='<p><label><input type="checkbox" id="furrbox" checked onchange="document.getElementById(\'furr\').style.display=this.checked?\'\':\'none\'"> Show the furring strips (S1 to S8)</label></p>\n'
html=html[:d0]+toggle+'<div class="wide">'+furring_svg()+html[d1:]
html=html.replace('<h3>Driver side wall: depth color map</h3>','<h3>Driver side wall: depth color map and furring layout</h3>',1)
# furring text goes right after the depth map explanation
rest=blk[blk.index('<p class="legend"><span><i class="sw" style="background:#7A4A1E">'):]
p1=html.index('<h3>Reading the wall</h3>')
html=html[:p1]+'<h4>Furring layout for vertical planks</h4>\n'+rest+html[p1:]
open((ROOT+'/sides.html'),'w').write(html)

# ---- passenger side furring with the nooks ----
def furring_pass_group():
    S=6.0; X0=50; FL=540
    xx=lambda i:X0+S*i
    yy=lambda h:FL-S*h
    o=[]; a=o.append
    strips=[('S1',3),('S2',12),('S3',21.4),('S4',30.25),('S5',43.5),('S6',57.25),('S7',66),('S8',76.75)]
    SEG={'S1':[(0,42),(76,104)],'S2':[(0,104)],'S3':[(0,104)],'S4':[(0,104)],'S5':[(0,4.5),(31.25,56.5),(94.75,104)],'S6':[(0,104)],'S7':[(0,104)],'S8':[(0,154)]}
    PAP={'S1':[6,17.75,31.25,82.94,98.9],'S2':[15,30.75,40,54,62,72,80,96,104],'S3':[22,34,46,58,70,78,99],'S4':[10,17.75,31.25,44.5,58.6,71.31,82.94,98.9],'S5':[2,32,44.5,98.9],'S6':[10,17.75,31.25,44.5,58.6,71.31,82.94,98.9],'S7':[x for x in AP['S7'] if x<=104],'S8':AP['S8']}
    for n,h in strips:
        for x0,x1 in SEG[n]:
            fill='#7A4A1E' if n in ('S1','S2','S3') else ('url(#spcP)' if n in ('S4','S5','S6') else '#D9A05B')
            if n=='S5' and x1-x0<=10 and x0 in (0,94.75): fill='#7A4A1E'
            a(f'<rect x="{xx(x0):.1f}" y="{yy(h+0.75):.1f}" width="{S*(x1-x0):.1f}" height="{S*1.5:.1f}" fill="{fill}" fill-opacity="0.95" stroke="#3E230B" stroke-width="1"/>')
        for px in PAP[n]:
            a(f'<circle cx="{xx(px):.1f}" cy="{yy(h):.1f}" r="4.2" fill="#fff" stroke="#3E230B" stroke-width="1.5"/>')
        a(f'<circle cx="{xx(3):.1f}" cy="{yy(h)-0:.1f}" r="9" fill="#fff" stroke="#3E230B" stroke-width="1.2"/><text x="{xx(3):.1f}" y="{yy(h)+3.5:.1f}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:#3E230B">{n}</text>')
    # vertical frames at the nook ends: (name, x0, x1, bottom, top, spacer?)
    for n,x0,x1,b,t,sp in (('V1',4.5,6,31,56.5,True),('V2',29.75,31.25,31,56.5,True),('V3',56.5,58,31,56.5,True),('V4',93.25,94.75,31,56.5,False)):
        fill='url(#spcP)' if sp else '#5B3A1A'
        a(f'<rect x="{xx(x0):.1f}" y="{yy(t):.1f}" width="{S*(x1-x0):.1f}" height="{S*(t-b):.1f}" fill="{fill}" fill-opacity="0.95" stroke="#3E230B" stroke-width="1"/>')
        cx=(x0+x1)/2
        for hh in (b+5,(b+t)/2,t-5):
            a(f'<circle cx="{xx(cx):.1f}" cy="{yy(hh):.1f}" r="4.2" fill="#fff" stroke="#3E230B" stroke-width="1.5"/>')
        a(f'<circle cx="{xx(cx):.1f}" cy="{yy(61.5):.1f}" r="9" fill="#fff" stroke="#3E230B" stroke-width="1.2"/><text x="{xx(cx):.1f}" y="{yy(61.5)+3.5:.1f}" text-anchor="middle" style="font-size:9px;font-weight:700;fill:#3E230B">{n}</text>')
    a(f'<text class="th" x="{xx(59):.1f}" y="{yy(5.6):.1f}" text-anchor="middle" style="font-size:10px;fill:#791F1F;paint-order:stroke;stroke:#fff;stroke-width:3px">box out the wheel well (sticks out 7 in)</text>')
    return ''.join(o)
ADJ.update({'noharness':True,'cp':(2.5,12),'cpdepth':'2.5','cph':(12,20.25),'l1split':True,'l1a':True,'lbot':{'L2':9.5,'L3':10},'s1':(38.25,47.75),'s1h':(25,27.75)})
_pt=passenger(section_e2())
ADJ.clear()
_pt=_pt.replace('<defs>','<defs><pattern id="spcP" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><rect width="7" height="7" fill="#C7792A"/><line x1="0" y1="0" x2="0" y2="7" stroke="#FFF1D6" stroke-width="2.5"/></pattern>',1)
_pt=_pt.replace('</svg>','<g id="furrP">'+furring_pass_group()+'</g></svg>',1)
_pass2f=flip_view(_pt)
html=open((ROOT+'/sides.html')).read()
assert pass2 in html
html=html.replace(pass2,_pass2f,1)
_h3='<h3>Passenger side wall: depth color map (same as the driver side, adjustments to come)</h3>\n'
assert _h3 in html
html=html.replace(_h3,_h3+'<p><label><input type="checkbox" id="furrboxP" checked onchange="document.getElementById(\'furrP\').style.display=this.checked?\'\':\'none\'"> Show the furring strips (S1 to S8) and the nook frames (V1 to V4)</label></p>\n',1)
_rows=[('S1 to S4, S6, S7','stop at the door opening (104 in)','There is no wall behind the sliding door (51 wide, 67 tall, measured), so these strips end at 104 in and the dots past 104 are dropped. S7 (65 1/4 to 66 3/4 in up) is inside the 67 in opening, so it stops too. Only S8 (76 in up) carries on above the door.'),
('S4','under the shower nook','Its top edge (31 in) is the bottom of the shower nook, so S4 is the nook floor frame. No change to the strip.'),
('S5','cut at both nooks','S5 (43 1/2 in up) crosses both nooks, so it is removed there. It now runs 0 to 4 1/2 in (a stub, one dot at 2 in, sitting straight on the 3 3/4 in steel, no spacer), 31 1/4 to 56 1/2 in (dots at 32 and 44 1/2), and 94 3/4 to 104 in (dot at 98.9, on the 3 3/4 in steel between P7 and P8, no spacer). The dots at 17.75 (shower nook) and 58.6, 71.31 and 82.94 (counter nook) are dropped.'),
('S6','top of both nooks','Its bottom edge (56 1/2 in) is the top of both nooks, so S6 is the top frame. No change to the strip.'),
('V1','shower nook, rear end','Vertical frame 4 1/2 to 6 in from the back, 31 to 56 1/2 in up; bonded on spacers to the 1/8 in strip left of P1 (3 5/8 in spacer at each of 3 dots).'),
('V2','shower nook, front end','Vertical frame 29 3/4 to 31 1/4 in from the back, 31 to 56 1/2 in up; on spacers on the rib between P2 and P3 (3 dots).'),
('V3','counter nook, left end','Vertical frame 56 1/2 to 58 in from the back, 31 to 56 1/2 in up (down to S4, behind the countertop, where it gives the back edge of the counter something to fasten to); on spacers on the rib between P4 and P5 (3 dots).'),
('V4','counter nook, right end','Vertical frame 93 1/4 to 94 3/4 in from the back, 31 to 56 1/2 in up (down to S4, behind the countertop); sits straight on the 3 3/4 in steel between P7 and P8, no spacer (3 dots).')]
_fp='<h4>Furring on the passenger side, with the nooks</h4>\n<p>The passenger wall uses the same eight strips and the same dots as the driver side (S1 to S8), changed only for the sliding door and the two nooks. The nook frames V1 to V4 are 3/4 x 1 1/2 in vertical strips that finish the planks beside each nook, hold the nook lining, and carry the shelf in the counter nook. All four run from S4 (31 in) up to S6 (56 1/2 in); below 38 in the counter nook frames sit behind the countertop. The low passenger-side holes (CP, S1, L2, L3) were checked against the dots: no dot lands inside any of them.</p>\n<p class="legend"><span><i class="sw" style="background:#5B3A1A"></i>Dark brown: sits on the 3 3/4 in steel, no spacer (V4 and the two S5 ends)</span><span><i class="sw" style="background:repeating-linear-gradient(45deg,#C7792A,#C7792A 3px,#FFF1D6 3px,#FFF1D6 5px)"></i>Orange striped: 3 5/8 in spacer at every dot (S4, S5 middle, S6, V1 to V3)</span></p>\n<table><tr><th>Strip</th><th>Where</th><th>Change from the driver side</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td></tr>' for a,b,c in _rows)+'</table>\n'
_h3b='<h3>Passenger side adjustments</h3>'
assert _h3b in html
html=html.replace(_h3b,_fp+_h3b,1)
open((ROOT+'/sides.html'),'w').write(html)

# ---- passenger side: built items (seen from inside, cab on the left) ----
def passenger_items(tank=False):
    S=6.0; X0=50; FL=540
    xx=lambda i:X0+S*i; yy=lambda h:FL-S*h
    W=xx(160)+60
    o=[]; a=o.append
    _ttl='Passenger side option: shower on the grey water tank' if tank else 'Passenger side: built items'
    a(f'<svg viewBox="0 0 {W:.0f} {FL+96}" role="img"><title>{_ttl}</title>')
    _cap='Option 2, shower on the grey water tank, seen from inside the van: cab on the left, rear on the right.' if tank else 'Passenger side built items, seen from inside the van: cab on the left, rear on the right. The wheel well matches the driver side; the door is not measured yet.'
    a(f'<text class="ts" x="{X0}" y="22" style="font-size:14px">{_cap}</text>')
    for i in range(0,161,10):
        a(f'<line x1="{xx(i)}" y1="{yy(80)}" x2="{xx(i)}" y2="{FL}" stroke="#3F3E3A" stroke-opacity="0.4" stroke-width="0.9" stroke-dasharray="3 3"/>')
    for h in range(0,81,10):
        a(f'<line x1="{xx(0)}" y1="{yy(h)}" x2="{xx(160)}" y2="{yy(h)}" stroke="#3F3E3A" stroke-opacity="0.4" stroke-width="0.9" stroke-dasharray="3 3"/>')
        a(f'<text x="{xx(0)-6}" y="{yy(h)+4}" text-anchor="end" style="font-size:11px;font-weight:700;fill:#8A4B0F">{h}↑</text>')
    a(f'<rect x="{xx(0)}" y="{yy(76)}" width="{S*154}" height="{S*76}" fill="#F1EFE8" fill-opacity="0.6" stroke="#5F5E5A" stroke-width="1.2"/>')
    def box(x0,x1,h0,h1,col,label,sub=None,ly=None,fo=0.12,dash=''):
        a(f'<rect x="{xx(x0):.1f}" y="{yy(h1):.1f}" width="{S*(x1-x0):.1f}" height="{S*(h1-h0):.1f}" rx="3" fill="{col}" fill-opacity="{fo}" stroke="{col}" stroke-width="1.5" {dash}/>')
        cy=yy((h0+h1)/2) if ly is None else ly
        a(f'<text class="th" x="{xx((x0+x1)/2):.1f}" y="{cy:.1f}" text-anchor="middle" style="fill:{col};font-size:12px;paint-order:stroke;stroke:#fff;stroke-width:3px">{label}</text>')
        if sub: a(f'<text class="ts" x="{xx((x0+x1)/2):.1f}" y="{cy+14:.1f}" text-anchor="middle" style="fill:{col};font-size:10.5px;paint-order:stroke;stroke:#fff;stroke-width:3px">{sub}</text>')
    _og=[False]
    def grp(name=None,label=''):
        if _og[0]: a('</g>'); _og[0]=False
        if name: a(f'<g class="tg" data-g="{name}" data-label="{label}">'); _og[0]=True
    T='#0F6E56'; G='#444441'; P='#534AB7'; K='#993556'; C='#993C1D'
    # wheel well (copy of driver side) and water tank on top
    grp('ww','Wheel well')
    WW=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
    a('<polygon points="'+' '.join(f'{xx(x):.1f},{yy(h):.1f}' for x,h in WW)+'" fill="#D8B79A" fill-opacity="0.8" stroke="#8A6B4D" stroke-width="1.2"/>')
    a(f'<text class="ts" x="{xx(59):.1f}" y="{yy(3.2):.1f}" text-anchor="middle" style="font-size:10px">wheel well (same as the driver side)</text>')
    grp('ceil','Ceiling covering')
    a(f'<rect x="{xx(0):.1f}" y="{yy(76):.1f}" width="{S*154:.1f}" height="{S*0.25:.1f}" fill="#D9C7A5" stroke="#8A6B4D" stroke-width="0.8"/>')
    a(f'<rect x="{xx(0):.1f}" y="{yy(75.75):.1f}" width="{S*154:.1f}" height="{S*1:.1f}" fill="#9A6B3A" fill-opacity="0.85" stroke="#5A3A00" stroke-width="0.8"/>')
    for _x0,_x1,_nm in ((0.25,14.25,'shower fan'),(36.375,50.625,'A/C')):
        a(f'<rect x="{xx(_x0):.1f}" y="{yy(76):.1f}" width="{S*(_x1-_x0):.1f}" height="{S*1.25:.1f}" fill="#2C2C2A" fill-opacity="0.85"/>')
        a(f'<text class="ts" x="{xx((_x0+_x1)/2):.1f}" y="{yy(77.4):.1f}" text-anchor="middle" style="font-size:10px;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:3px">{_nm}</text>')
    for _lx in (20.67,74,127.33): a(f'<circle cx="{xx(_lx):.1f}" cy="{yy(74.4):.1f}" r="3" fill="#FFD84A" stroke="#B8860B" stroke-width="0.8"/>')
    grp('bath','Wet bath (shower pan)')
    if tank:
        TK='#6D6A62'
        box(0,36,9.5,74.75,T,'Wet bath','shower floor at 9.5 up, 65 1/4 in headroom',yy(68),0.08)
        box(0,30,0,9.5,TK,'Grey water tank','30 x 15 x 9.5 in, about 15 gal',yy(6.2),0.3)
        a(f'<line x1="{xx(0):.1f}" y1="{yy(9.5):.1f}" x2="{xx(36):.1f}" y2="{yy(9.5):.1f}" stroke="{T}" stroke-width="4"/>')
        a(f'<line x1="{xx(29):.1f}" y1="{yy(9.5):.1f}" x2="{xx(29):.1f}" y2="{yy(6.5):.1f}" stroke="#A32D2D" stroke-width="2" marker-end="url(#arq)"/><text class="ts" x="{xx(29):.1f}" y="{yy(11.6):.1f}" text-anchor="middle" style="font-size:10px;fill:#A32D2D;paint-order:stroke;stroke:#fff;stroke-width:3px">drain</text>')
    else:
        box(0,36,0,74.75,T,'Wet bath','36 x 24 in, shower curtain',yy(68),0.08)
    grp('snook','Shower nook')
    box(6,29.75,31,56.5,'#7A4A1E','Shower nook','23.75 x 25.5, 4.5 deep',yy(44),0.2,'stroke-dasharray="5 3"')
    grp('cabs','Cabinets and countertop')
    box(58,103,0,38,C,'',None,yy(31),0.08)
    box(103,123,0,38,C,'Sink cabinet','20 wide, counter 15 3/4 deep',yy(26),0.08)
    a(f'<rect x="{xx(58):.1f}" y="{yy(38):.1f}" width="{S*65:.1f}" height="{S*1.2:.1f}" fill="#5F5E5A" fill-opacity="0.75"/>')
    a(f'<text class="ts" x="{xx(100):.1f}" y="{yy(38)-4:.1f}" text-anchor="middle" style="font-size:10.5px">countertop at 38 in</text>')
    # tall fridge on a platform over the wheel well, next to the shower
    grp('fridge','Fridge')
    a(f'<rect x="{xx(36):.1f}" y="{yy(8.25):.1f}" width="{S*22:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="1"/>')
    a(f'<rect x="{xx(36):.1f}" y="{yy(7.5):.1f}" width="{S*1.5:.1f}" height="{S*7.5:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="1"/>')
    box(36,58,8.25,56.25,'#0A6A8A','Fridge','22 x 19 x 48, front opening',yy(34),0.22)
    a(f'<text class="ts" x="{xx(47):.1f}" y="{yy(34)+28:.1f}" text-anchor="middle" style="font-size:9.5px;fill:#0A6A8A;paint-order:stroke;stroke:#fff;stroke-width:3px">on a platform over the well</text>')
    grp('cnook','Counter nook')
    box(58,93.25,38,56.5,'#7A4A1E','',None,yy(48),0.2,'stroke-dasharray="5 3"')
    grp('jars','Nook shelf and jars')
    # shelf at 45.5 up (3/4 thick) and two tiers of quart canning jars (3 3/4 wide, 7 tall with the lid), 9 per tier
    a(f'<rect x="{xx(58):.1f}" y="{yy(46.25):.1f}" width="{S*35.25:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="1"/>')
    for _base in (38,46.25):
        for _i in range(9):
            _jx=58.75+3.75*_i
            a(f'<rect x="{xx(_jx+0.1):.1f}" y="{yy(_base+6.25):.1f}" width="{S*3.55:.1f}" height="{S*6.25:.1f}" rx="2.5" fill="#A9D4F5" fill-opacity="0.6" stroke="#185FA5" stroke-width="0.9"/>')
            a(f'<rect x="{xx(_jx+0.45):.1f}" y="{yy(_base+7):.1f}" width="{S*2.85:.1f}" height="{S*0.75:.1f}" fill="#8A8A8A" stroke="#444441" stroke-width="0.6"/>')
        _cy=_base+3.5
        a(f'<line x1="{xx(58.4):.1f}" y1="{yy(_cy):.1f}" x2="{xx(92.85):.1f}" y2="{yy(_cy):.1f}" stroke="#7A4A1E" stroke-width="1.6" stroke-dasharray="3 2"/>')
    a(f'<text class="th" x="{xx(67):.1f}" y="{yy(54.7):.1f}" text-anchor="middle" style="fill:#7A4A1E;font-size:11px;paint-order:stroke;stroke:#fff;stroke-width:3px">Nook: quart jars</text>')
    a(f'<text class="ts" x="{xx(98.8):.1f}" y="{yy(46):.1f}" text-anchor="middle" style="fill:#5A3510;font-size:10px;paint-order:stroke;stroke:#fff;stroke-width:3px">shelf 45.5 up</text>')
    a(f'<text class="ts" x="{xx(98.8):.1f}" y="{yy(46)+12:.1f}" text-anchor="middle" style="fill:#5A3510;font-size:10px;paint-order:stroke;stroke:#fff;stroke-width:3px">9 jars a tier</text>')
    grp('tv','TV')
    box(76.5,103.5,54,69.4,G,'TV 30 in','27 x 15.4, over the cabinet',yy(63),0.25)
    grp('fresh','Fresh water tank')
    box(97.25,122.25,0,15,'#185FA5','Fresh water tank','25 x 9 x 15, on the floor',yy(8),0.14,'stroke-dasharray="5 3"')
    grp('angle','Counter angle marker')
    a(f'<line x1="{xx(88):.1f}" y1="{yy(23):.1f}" x2="{xx(88):.1f}" y2="{yy(38):.1f}" stroke="#A32D2D" stroke-width="2" stroke-dasharray="5 3"/>')
    # paper towel roll in a recess in the angled front (91 to 103), and two towel bars under it
    grp('towels','Paper towels and bars')
    box(91.5,102.5,29.75,35.25,'#B07A2A','Paper towels','11 in roll, recessed',yy(32.9),0.35)
    for _zb in (25.5,19.5):
        a(f'<line x1="{xx(91.5):.1f}" y1="{yy(_zb):.1f}" x2="{xx(102.5):.1f}" y2="{yy(_zb):.1f}" stroke="#444441" stroke-width="3.5" stroke-linecap="round"/><circle cx="{xx(91.5):.1f}" cy="{yy(_zb):.1f}" r="3" fill="#444441"/><circle cx="{xx(102.5):.1f}" cy="{yy(_zb):.1f}" r="3" fill="#444441"/>')
    a(f'<text class="ts" x="{xx(97):.1f}" y="{yy(22.2):.1f}" text-anchor="middle" style="font-size:9.5px;fill:#444441;paint-order:stroke;stroke:#fff;stroke-width:3px">2 towel bars, 11 in</text>')
    grp('hot','Hot water tank')
    box(79.625,93.625,0,15,'#C0392B','Hot water tank','14 x 15, 15 tall, 120 V 1,440 W',yy(8),0.18,'stroke-dasharray="5 3"')
    grp('draw','Drawers under the counter')
    a(f'<rect x="{xx(58):.1f}" y="{yy(36.5):.1f}" width="{S*29.25:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    a(f'<rect x="{xx(72.75):.1f}" y="{yy(35.75):.1f}" width="{S*0.5:.1f}" height="{S*4.5:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    box(59.25,72.25,31.25,35.25,'#8A5A00','Drawer + tray','13 x 20 x 4',yy(33.9),0.2)
    box(73.75,86.75,31.25,35.25,'#8A5A00','Drawer','13 x 20 x 4',yy(33.9),0.2)
    # lower drawers, 20 deep to the wall: a 3/4 in shelf 1/2 in over the hot water tank top (15) carries two 5 in drawers (cab side); the back-side column is over the wheel well only, so its 10 in and 11 in drawers sit on a lower shelf 1/2 in over the well
    a(f'<rect x="{xx(72.75):.1f}" y="{yy(16.25):.1f}" width="{S*14.5:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    a(f'<rect x="{xx(58):.1f}" y="{yy(8.75):.1f}" width="{S*14.75:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    a(f'<rect x="{xx(58):.1f}" y="{yy(20.75):.1f}" width="{S*14.75:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    a(f'<rect x="{xx(72.75):.1f}" y="{yy(31.25):.1f}" width="{S*0.5:.1f}" height="{S*22.5:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    a(f'<rect x="{xx(72.75):.1f}" y="{yy(25.75):.1f}" width="{S*14.5:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="0.8"/>')
    box(73.75,86.75,26.0,31.0,'#8A5A00','Drawer','13 x 20 x 5',yy(29.4),0.2)
    box(73.75,86.75,20.0,25.0,'#8A5A00','Drawer','13 x 20 x 5',yy(23.4),0.2)
    box(59.25,72.25,21.0,31.0,'#8A5A00','Drawer','13 x 20 x 10',yy(26.4),0.2)
    box(59.25,72.25,9.0,20.0,'#8A5A00','Drawer','13 x 20 x 11',yy(14.9),0.2)
    grp('plumb','Sink plumbing')
    a(f'<line x1="{xx(111):.1f}" y1="{yy(0):.1f}" x2="{xx(111):.1f}" y2="{yy(31):.1f}" stroke="#185FA5" stroke-width="3" stroke-dasharray="2 2"/>')
    a(f'<text class="ts" x="{xx(113):.1f}" y="{yy(34):.1f}" text-anchor="middle" style="font-size:9.5px;fill:#185FA5;paint-order:stroke;stroke:#fff;stroke-width:3px">sink plumbing, 12 in from the cab-side edge</text>')
    grp('micro','Microwave and shelf')
    a(f'<rect x="{xx(36):.1f}" y="{yy(59):.1f}" width="{S*22:.1f}" height="{S*0.75:.1f}" fill="#8A6B4D" stroke="#3E230B" stroke-width="1"/>')
    box(37.75,56.25,59,69,G,'Microwave','18.5 x 10 x 12 in',yy(66),0.25)
    # foot ledge on the cabinet end: 10 long x 15 wide, top at 8 up, hinged on the end, folds up into a recess in the end panel
    grp('ledge','Foot ledge')
    _lh=8.5; _ll=13
    a(f'<line x1="{xx(123):.1f}" y1="{yy(_lh-0.75-6):.1f}" x2="{xx(123+_ll-1.5):.1f}" y2="{yy(_lh-0.75):.1f}" stroke="#5A3A00" stroke-width="2.2"/>')
    a(f'<rect x="{xx(123):.1f}" y="{yy(_lh):.1f}" width="{S*_ll:.1f}" height="{S*0.75:.1f}" fill="#B07A2A" fill-opacity="0.9" stroke="#5A3A00" stroke-width="1.2"/>')
    a(f'<rect x="{xx(123+_ll-0.75):.1f}" y="{yy(_lh+1):.1f}" width="{S*0.75:.1f}" height="{S*1:.1f}" fill="#B07A2A" fill-opacity="0.9" stroke="#5A3A00" stroke-width="1"/>')
    a(f'<rect x="{xx(122.25):.1f}" y="{yy(_lh-0.75+_ll):.1f}" width="{S*0.75:.1f}" height="{S*_ll:.1f}" fill="none" stroke="#5A3A00" stroke-width="1.2" stroke-dasharray="4 3"/>')
    a(f'<circle cx="{xx(123):.1f}" cy="{yy(_lh-0.4):.1f}" r="3" fill="#5A3A00"/>')
    a(f'<text class="th" x="{xx(135):.1f}" y="{yy(3.2):.1f}" text-anchor="middle" style="font-size:10.5px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">Foot ledge, 13 x 15 3/4, top 8 1/2 up</text>')
    # fold-out table at the cab-side end of the sink cabinet: 29 long x 15 deep, 29 up, hinged on the cabinet end, folds down against it, carried by a folding brace
    grp('flap','Fold-out table')
    _fh=29; _fl=29
    a(f'<line x1="{xx(123):.1f}" y1="{yy(_fh-0.75-13):.1f}" x2="{xx(123+15.75):.1f}" y2="{yy(_fh-0.75):.1f}" stroke="#5A3A00" stroke-width="3"/>')
    a(f'<circle cx="{xx(123):.1f}" cy="{yy(_fh-0.75-13):.1f}" r="3" fill="#5A3A00"/><circle cx="{xx(123+15.75):.1f}" cy="{yy(_fh-0.75):.1f}" r="2.5" fill="#5A3A00"/>')
    a(f'<rect x="{xx(123):.1f}" y="{yy(_fh):.1f}" width="{S*_fl:.1f}" height="{S*0.75:.1f}" fill="#B07A2A" fill-opacity="0.85" stroke="#5A3A00" stroke-width="1.2"/>')
    a(f'<rect x="{xx(123):.1f}" y="{yy(_fh):.1f}" width="{S*0.75:.1f}" height="{S*_fh:.1f}" fill="none" stroke="#5A3A00" stroke-width="1.2" stroke-dasharray="4 3"/>')
    a(f'<circle cx="{xx(123):.1f}" cy="{yy(_fh-0.4):.1f}" r="3.2" fill="#5A3A00"/>')
    a(f'<text class="th" x="{xx(139):.1f}" y="{yy(46):.1f}" text-anchor="middle" style="font-size:11.5px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">Fold-out table</text>')
    a(f'<text class="ts" x="{xx(139):.1f}" y="{yy(42.5):.1f}" text-anchor="middle" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">29 long x 15 deep, 29 up</text>')
    a(f'<text class="ts" x="{xx(139):.1f}" y="{yy(39.5):.1f}" text-anchor="middle" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">dashed: folded against the cabinet end</text>')
    a(f'<text class="ts" x="{xx(145.5):.1f}" y="{yy(22.5):.1f}" text-anchor="middle" style="font-size:10px;fill:#5A3A00;paint-order:stroke;stroke:#fff;stroke-width:3px">folding brace under the table</text>')
    # sliding door (copy) and conflicts
    grp('door','Sliding door opening')
    a(f'<rect x="{xx(104):.1f}" y="{yy(67):.1f}" width="{S*51:.1f}" height="{S*67:.1f}" fill="none" stroke="#BA7517" stroke-width="2" stroke-dasharray="8 4"/>')
    a(f'<text class="th" x="{xx(129.5):.1f}" y="{yy(52):.1f}" text-anchor="middle" style="font-size:12px;fill:#854F0B;paint-order:stroke;stroke:#fff;stroke-width:3px">Sliding door opening (104 to 155)</text>')
    a(f'<text class="th" x="{xx(146):.1f}" y="{yy(14):.1f}" text-anchor="middle" style="font-size:11px;fill:#444441;paint-order:stroke;stroke:#fff;stroke-width:3px">Entry, 31 in clear</text>')
    grp()
    yb=FL+16
    a(f'<line x1="{xx(0)}" y1="{yb}" x2="{xx(160)}" y2="{yb}" stroke="#888780" stroke-width="0.6"/>')
    for t in range(0,161,10):
        a(f'<line x1="{xx(t)}" y1="{yb-4}" x2="{xx(t)}" y2="{yb+4}" stroke="#888780" stroke-width="0.6"/><text x="{xx(t)}" y="{yb+18}" text-anchor="middle" style="font-size:11px;font-weight:700;fill:#185FA5">{t}→</text>')
    a(f'<text class="ts" x="{xx(80)}" y="{yb+36}" text-anchor="middle" style="font-size:12px">inches from where you start measuring at the back</text>')
    a('</svg>')
    return '\n'.join(o)
_pi=flip_view(passenger_items().replace('→','→'))
html=open((ROOT+'/sides.html')).read()
blk='''<h3>Passenger side: built items</h3>
<div class="wide">'''+_pi+'''</div>
<p>Drawn from the sizes in your notes, as seen from inside the van (cab on the left). Two 4 in tall drawers side by side (boxes 13 in wide and 20 in deep, 59 1/4 to 72 1/4 and 73 3/4 to 86 3/4, 31 1/4 to 35 1/4 in up, a 1/2 in divider between, the silverware tray in the left one) hang under the counter in the flat part, and under them four more 13 in wide, 20 in deep drawers: two 5 in tall boxes one above the other on the cab side (20 to 25 and 26 to 31 in up) on a 3/4 in shelf at 15 1/2 to 16 1/4 in up, 1/2 in over the top of the hot water tank (15), with 3 3/4 in open below them; and toward the back a 10 in box (21 to 31) over an 11 in box (9 to 20) on their own lower shelf at 8 to 8 3/4 in up, 1/2 in over the wheel well (7 1/2 tall), since that column is over the well and not over the tank. They run the full 20 in back to the wall, over the tank and the well (a 3/4 in front brings each to 20 3/4 of the 21 in cabinet). The grey water tank is not here because it goes under the van; the fresh water tank (dashed blue, 25 x 9 x 15 in, about 14 1/2 gal) is on the floor at the sink end against the cab-side end panel, partly in the sink cabinet and partly in the open area beside it, from 97 1/4 to 122 1/4 in, and the space above the fresh water tank under the counter is open (the drawers that were there were removed and will be redone), a paper towel roll recessed into the angled front at 91 to 103 in (29 3/4 to 35 1/4 in up) with two 11 in towel bars under it (25 1/2 and 19 1/2 in up), and the hot water tank (dashed red, 14 in along the wall, 15 in deep and 15 in tall, 120 V and 1,440 W) sits on the floor next to the wheel well at 79 5/8 to 93 5/8 in, with 3 5/8 in clear on each side (the wheel well ends at 76 in and the fresh water tank starts at 97 1/4 in; the 6 in asked for on each side would need 26 in and there are 21 1/4); the sink plumbing (dotted blue) 12 in from the cab-side edge of the counter comes down in the 6 in in front of the fresh water tank. The wheel well matches the driver side, and the sliding door is not measured. One problem is still open: the sink cabinet (103 to 123 in) falls almost entirely inside the sliding door opening (104 to 155 in; the rear edge at 104 in is measured), and the fresh water tank (97 1/4 to 122 1/4 in) stands in front of it too. The door's width and height still need measuring. The passenger wall cabinet was removed. Everything is measured from the same zero, 6 in in from the back.</p>
<p><b>Nook.</b> The nook (brown dashed) is the recess of pans P4 to P7 behind the countertop, open above the counter: 58 to 93 1/4 in from the back (35 1/4 in long), 38 to 56 1/2 in up (18 1/2 in tall) and about 4 1/2 in deep, from the body to the planks (4 3/8 in over the ribs). The part of P4 behind the fridge (46 to 58 in) is not usable. The TV (bottom at 54 in) covers the top 2 1/2 in of the nook from 76 1/2 to 93 1/4 in; raising the TV to a 56 1/2 in bottom would clear it. For storage, the drawing shows a 3/4 in shelf at 45 1/2 in up and two tiers of quart canning jars (3 3/4 in wide, 7 in tall with the lid), 9 jars a tier, 18 in all, about 54 lb. The bottom tier sits on the countertop. The dashed lines across the fronts are elastic cords that stop the jars sliding out; under the TV (76 1/2 to 93 1/4 in) the top tier has only about 1/2 in of clearance.</p>
<p><b>Shower nook.</b> The shower has its own nook (brown dashed, in the wet bath): the recess of pans P1 and P2, 6 to 29 3/4 in from the back (23 3/4 in long), 31 to 56 1/2 in up (25 1/2 in tall) and about 4 1/2 in deep. It needs a waterproof lining (tile or a sheet panel) and a slight slope to the front so water drains out.</p>
<p><b>Fold-out table.</b> At the cab-side end of the sink cabinet (123 in), a board 29 in long (123 to 152), 15 in deep like the counter and 3/4 in thick is hinged on the end of the cabinet at 29 in up. Open, it reaches toward the passenger seat, so the seat turned to face the back sits behind a table; closed, it hangs down against the cabinet end (dashed) and takes about 3/4 in of the 31 in entry. A folding brace carries it, because a 29 in cantilever on a 15 3/4 in cabinet end is a long lever: a diagonal arm hinged on the cabinet end (13 in below the board) that swings up and locks under the board 15 3/4 in out; a floor leg at the free end would be where the rotated seat's knees and shins are. Open, it closes off the entry from the sliding door (the rear doors still work). 29 in matches the dinette table; a seated table is about 10 in above the seat cushion, so set the height from the cushion once the swivel seat is chosen (38 in would be counter height but is too high for a seated person unless the cushion is about 27 in up).</p>
<p><b>Foot ledge.</b> Under the table, a shelf 13 in long (123 to 136, so its outer edge is 13 in from the cabinet end), 15 3/4 in wide (the cabinet depth) and 3/4 in thick with a 1 in lip is hinged on the cabinet end with its top at 8 1/2 in up; folded up it sits flat in a 3/4 in recess in the end panel (dashed), behind the folded table, so the table goes up first and the ledge down after it. It is held by a small folding brace and only carries the weight of your legs. The base of the cabinet is full (the fresh water tank, floor to 15 in), so a ledge that slides out of the base does not fit. About 20 in is left between the ledge and the underside of the table. The cab passenger seat cushion is 17 in up, so the ledge top is 8 1/2 in below it.</p>
'''
html=html.replace('<h2>Driver side photos</h2>',blk+'<h2>Driver side photos</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)
exec(open((HERE+'/cur.py')).read())


# ---- plan view: wall, wheel well, battery, bed, closet ----
def battery_plan():
    S=6.0; X0=50; Y0=40
    xx=lambda i:X0+S*i; yy=lambda d:Y0+S*d
    W=xx(100)+40
    o=[]; a=o.append
    a(f'<svg viewBox="0 0 {W:.0f} {yy(30)+34:.0f}" role="img" style="max-width:760px"><title>Battery next to the wheel well, looking down</title>')
    a('<defs><marker id="arp" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    a(f'<text class="ts" x="{X0}" y="20" style="font-size:13px">Driver side, looking down. The wall is the top edge.</text>')
    a(f'<rect x="{xx(0)}" y="{yy(0)-6}" width="{S*100}" height="6" fill="#5F5E5A"/>')
    a(f'<text class="ts" x="{xx(1)}" y="{yy(0)-9}" style="font-size:10px">wall (steel face)</text>')
    for d in range(0,31,10):
        a(f'<line x1="{xx(0)}" y1="{yy(d)}" x2="{xx(100)}" y2="{yy(d)}" stroke="#3F3E3A" stroke-opacity="0.3" stroke-dasharray="3 3"/><text x="{xx(0)-6}" y="{yy(d)+4}" text-anchor="end" style="font-size:10px;font-weight:700;fill:#8A4B0F">{d} in</text>')
    for t in range(0,101,10):
        a(f'<line x1="{xx(t)}" y1="{yy(0)}" x2="{xx(t)}" y2="{yy(30)}" stroke="#3F3E3A" stroke-opacity="0.3" stroke-dasharray="3 3"/><text x="{xx(t)}" y="{yy(30)+16}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#185FA5">{t}→</text>')
    # bed and closet footprints
    a(f'<rect x="{xx(0)}" y="{yy(0)}" width="{S*74}" height="{S*27}" fill="#534AB7" fill-opacity="0.08" stroke="#534AB7" stroke-width="1.4"/>')
    a(f'<text class="th" x="{xx(18)}" y="{yy(22)}" text-anchor="middle" style="font-size:11px;fill:#534AB7">Bed 74 x 27 in</text>')
    a(f'<rect x="{xx(74)}" y="{yy(0)}" width="{S*18.5}" height="{S*27}" fill="#444441" fill-opacity="0.08" stroke="#444441" stroke-width="1.4"/>')
    a(f'<text class="th" x="{xx(83.25)}" y="{yy(22)}" text-anchor="middle" style="font-size:11px;fill:#444441">Closet</text>')
    # wheel well
    a(f'<rect x="{xx(42)}" y="{yy(0)}" width="{S*34}" height="{S*7}" fill="#D8B79A" fill-opacity="0.9" stroke="#8A6B4D" stroke-width="1.5"/>')
    a(f'<rect x="{xx(51.25)}" y="{yy(0)}" width="{S*15.5}" height="{S*7}" fill="none" stroke="#8A6B4D" stroke-width="1" stroke-dasharray="4 3"/>')
    a(f'<text class="th" x="{xx(59)}" y="{yy(3.8)}" text-anchor="middle" style="font-size:11px;fill:#5A3A1A">Wheel well, 7 in out</text>')
    # battery
    a(f'<rect x="{xx(48.5)}" y="{yy(7)}" width="{S*21}" height="{S*10}" rx="3" fill="#F2B84B" fill-opacity="0.65" stroke="#8A5A00" stroke-width="2"/>')
    a(f'<text class="th" x="{xx(59)}" y="{yy(11.8)}" text-anchor="middle" style="font-size:11px;fill:#5A3A00">Battery 21 x 10 in</text>')
    # depth arrows
    ax=xx(73)
    a(f'<line x1="{xx(72)}" y1="{yy(0)}" x2="{xx(72)}" y2="{yy(7)}" stroke="#8A6B4D" stroke-width="1.4" marker-start="url(#arp)" marker-end="url(#arp)"/><text x="{xx(72.6)}" y="{yy(3.8)}" style="font-size:10.5px;font-weight:700;fill:#5A3A1A">7</text>')
    a(f'<line x1="{xx(72)}" y1="{yy(7)}" x2="{xx(72)}" y2="{yy(17)}" stroke="#8A5A00" stroke-width="1.4" marker-start="url(#arp)" marker-end="url(#arp)"/><text x="{xx(72.6)}" y="{yy(12.4)}" style="font-size:10.5px;font-weight:700;fill:#8A5A00">10</text>')
    a(f'<line x1="{xx(79)}" y1="{yy(0)}" x2="{xx(79)}" y2="{yy(17)}" stroke="#A32D2D" stroke-width="1.6" marker-start="url(#arp)" marker-end="url(#arp)"/><text x="{xx(80)}" y="{yy(9)}" style="font-size:11px;font-weight:700;fill:#A32D2D">17 in total</text>')
    a(f'<line x1="{xx(26)}" y1="{yy(17)}" x2="{xx(26)}" y2="{yy(27)}" stroke="#534AB7" stroke-width="1.4" marker-start="url(#arp)" marker-end="url(#arp)"/><text x="{xx(26.8)}" y="{yy(22.5)}" style="font-size:10.5px;font-weight:700;fill:#534AB7">10 in left under the bed</text>')
    a('</svg>')
    return '\n'.join(o)
html=open((ROOT+'/sides.html')).read()
blk='<h4>Battery next to the wheel well, looking down</h4>\n<div class="wide">'+battery_plan()+'</div>\n<p>The wheel well sticks out 7 in from the wall and the battery sits against its aisle face, so the two together reach 17 in into the van. The bed is 27 in deep, which leaves 10 in under it past the battery, and the battery top (9.5 in) is below the underside of the bed deck (12 1/2 in). Where the 7 in is measured from still matters: it was not said whether it is from the wall steel or from the body, and the lower wall steel is 3 3/4 in off the body here, so the real total from the body could be larger. This is the same view for the passenger side once its wheel well is measured.</p>\n'
html=html.replace('<h2>Depth sections</h2>',blk+'<h2>Depth sections</h2>',1)
open((ROOT+'/sides.html'),'w').write(html)
exec(open((HERE+'/plan.py')).read())
exec(open((HERE+'/couch.py')).read())
exec(open((HERE+'/leaf.py')).read())
exec(open((HERE+'/ceiling.py')).read())
exec(open((HERE+'/letters.py')).read())
exec(open((HERE+'/toggle.py')).read())
exec(open((HERE+'/zoom.py')).read())
