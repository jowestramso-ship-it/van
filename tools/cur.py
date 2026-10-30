_path=(ROOT+'/sides.html')
_h=open(_path).read()
W=760; H=620
o=[]; a=o.append
a(f'<svg viewBox="0 0 {W} {H}" role="img"><title>Shower curtains on three sides, PVC paneling on the back wall, fixed pan, toilet at the cab end</title>')
a('<defs><marker id="ar3" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0 0 L10 5 L0 10 z" fill="#A32D2D"/></marker></defs>')
P='#7B3FA0'; P2='#C28AD8'; BLU='#185FA5'; DK='#2C2C2A'; BR='#7A4A1E'
# ---------- left: looking down ----------
S=9.0; OX=50
px=lambda x:OX+S*x
py=lambda d:336-S*d
a(f'<text class="th" x="50" y="24" style="font-size:14px">Looking down at the shower, pan down</text>')
a(f'<rect x="{px(0):.1f}" y="{py(24):.1f}" width="{S*36:.1f}" height="{S*24:.1f}" fill="#D9ECF7" stroke="{BLU}" stroke-width="2.5"/>')
a(f'<rect x="{px(1.5):.1f}" y="{py(22.5):.1f}" width="{S*33:.1f}" height="{S*22.5:.1f}" fill="#F4FAFD" stroke="{BLU}" stroke-width="1" stroke-dasharray="4 3"/>')
a(f'<rect x="{px(36):.1f}" y="{py(21):.1f}" width="{S*10:.1f}" height="{S*19:.1f}" fill="#0A6A8A" fill-opacity="0.15" stroke="#0A6A8A" stroke-width="1.5"/><text class="ts" x="{px(41):.1f}" y="{py(11.5):.1f}" text-anchor="middle" style="font-size:11px;fill:#0A6A8A">fridge</text>')
a(f'<line x1="{px(0):.1f}" y1="{py(0):.1f}" x2="{px(36):.1f}" y2="{py(0):.1f}" stroke="{DK}" stroke-width="6"/>')
a(f'<text class="ts" x="{px(18):.1f}" y="{py(0)+20:.1f}" text-anchor="middle" style="font-size:12px">passenger wall: PVC paneling, no end wall</text>')
a(f'<text class="ts" x="{px(0)-8:.1f}" y="{py(12):.1f}" text-anchor="end" style="font-size:11px">rear</text>')
a(f'<circle cx="{px(5):.1f}" cy="{py(12):.1f}" r="7" fill="{DK}"/><text class="ts" x="{px(5)+11:.1f}" y="{py(12)+4:.1f}" style="font-size:11px">drain</text>')
a(f'<rect x="{px(TOILET_X[0]):.1f}" y="{py(19.25):.1f}" width="{S*14.5:.1f}" height="{S*14.5:.1f}" rx="6" fill="#993556" fill-opacity="0.16" stroke="#993556" stroke-width="2"/><text class="th" x="{px(TOILET_X[0]+7.25):.1f}" y="{py(12):.1f}" text-anchor="middle" style="font-size:12px;fill:#993556">toilet</text><text class="ts" x="{px(TOILET_X[0]+7.25):.1f}" y="{py(12)+14:.1f}" text-anchor="middle" style="font-size:10px;fill:#993556">Fold-To-Go</text>')
a(f'<text class="ts" x="{px(10):.1f}" y="{py(20.5):.1f}" text-anchor="middle" style="font-size:10.5px;fill:#185FA5">19 1/2 in to stand</text>')
a(f'<rect x="{px(SN_X0):.1f}" y="{py(4.5):.1f}" width="{S*SN_LEN:.1f}" height="{S*4.5:.1f}" fill="#7A4A1E" fill-opacity="0.18" stroke="#7A4A1E" stroke-width="1.3" stroke-dasharray="5 3"/><text class="ts" x="{px((SN_X0+SN_X1)/2):.1f}" y="{py(2.2)+3:.1f}" text-anchor="middle" style="font-size:10px;fill:#5A3510">shower nook (centered)</text>')
a(f'<rect x="{px(HEAD_X)-4:.1f}" y="{py(6)-4:.1f}" width="8" height="8" fill="#9EC9E8" stroke="#185FA5" stroke-width="1.3"/><text class="ts" x="{px(HEAD_X):.1f}" y="{py(6)-8:.1f}" text-anchor="middle" style="font-size:10px;fill:#185FA5">head</text>')
# ceiling track (dashed) and the two curtains
pts=[(1.5,0.8),(1.5,22.5),(34.5,22.5),(34.5,0.8)]
path='M'+' L'.join(f'{px(x):.1f} {py(d):.1f}' for x,d in pts)
a(f'<path d="{path}" fill="none" stroke="{DK}" stroke-width="3" stroke-dasharray="9 4"/>')
# left curtain: left end + front to x=21
pl=[(1.5,0.8),(1.5,22.8),(21,22.8)]
a('<path d="M'+' L'.join(f'{px(x):.1f} {py(d):.1f}' for x,d in pl)+f'" fill="none" stroke="{P}" stroke-width="5" stroke-opacity="0.85" stroke-linejoin="round" stroke-linecap="round"/>')
# right curtain: right end + front from x=15
pr=[(34.5,0.8),(34.5,21.6),(15,21.6)]
a('<path d="M'+' L'.join(f'{px(x):.1f} {py(d):.1f}' for x,d in pr)+f'" fill="none" stroke="{P2}" stroke-width="5" stroke-opacity="0.9" stroke-linejoin="round" stroke-linecap="round"/>')
for x,d in ((1.5,0.8),(34.5,0.8)):
    a(f'<rect x="{px(x)-9:.1f}" y="{py(d)-3:.1f}" width="18" height="6" fill="{DK}"/>')
a(f'<text class="th" x="{px(18):.1f}" y="{py(22.5)-16:.1f}" text-anchor="middle" style="font-size:11px;fill:{P};paint-order:stroke;stroke:#fff;stroke-width:3px">two curtains overlap 6 in in the middle of the front</text>')
a(f'<text class="th" x="{px(1.5)+10:.1f}" y="{py(14):.1f}" style="font-size:11px;fill:{P};paint-order:stroke;stroke:#fff;stroke-width:3px">left</text><text class="th" x="{px(34.5)-10:.1f}" y="{py(14):.1f}" text-anchor="end" style="font-size:11px;fill:#9A55B8;paint-order:stroke;stroke:#fff;stroke-width:3px">right</text>')
a(f'<text class="th" x="{px(10.4):.1f}" y="{py(18):.1f}" text-anchor="middle" style="font-size:15px;fill:{BLU}">pan 36 x 24</text><text class="ts" x="{px(10.4):.1f}" y="{py(18)+16:.1f}" text-anchor="middle" style="font-size:11px">33 x 22 1/2 inside the curtains</text>')
a(f'<text class="ts" x="{px(18):.1f}" y="{py(24)-30:.1f}" text-anchor="middle" style="font-size:10.5px">ceiling rod (dashed), 1 1/2 in inside the pan edge</text>')
# ---------- right: from the rear, along the wall ----------
S2=7.0; FL=570
pz=lambda z:FL-S2*z
def view(Wx,title):
    a(f'<text class="th" x="{Wx-176}" y="24" style="font-size:14px">{title}</text>')
    a(f'<line x1="{Wx-190}" y1="{FL}" x2="{Wx+10}" y2="{FL}" stroke="{DK}" stroke-width="3"/>')
    a(f'<line x1="{Wx-190}" y1="{pz(75.5):.1f}" x2="{Wx+10}" y2="{pz(75.5):.1f}" stroke="#5F5E5A" stroke-width="1.5" stroke-dasharray="7 4"/>')
    a(f'<line x1="{Wx}" y1="{pz(75.5):.1f}" x2="{Wx}" y2="{FL}" stroke="{DK}" stroke-width="4"/>')
    a(f'<text class="ts" x="{Wx-186}" y="{pz(75.5)-4:.1f}" style="font-size:10.5px">ceiling 75 1/2</text>')
    a(f'<text class="ts" x="{Wx-4}" y="{pz(75.5)+14:.1f}" text-anchor="end" style="font-size:10.5px">wall</text>')
# state 1: in use
W1=640
view(W1,'From the rear, along the wall')
dx1=lambda d:W1-S2*d
a(f'<rect x="{dx1(24):.1f}" y="{pz(1):.1f}" width="{S2*24:.1f}" height="{S2*1:.1f}" fill="#D9ECF7" stroke="{BLU}" stroke-width="1.5"/>')
a(f'<rect x="{dx1(24):.1f}" y="{pz(3):.1f}" width="{S2*1.5:.1f}" height="{S2*3:.1f}" fill="#B9D9EE" stroke="{BLU}" stroke-width="1.5"/>')
a(f'<rect x="{dx1(1.5):.1f}" y="{pz(3):.1f}" width="{S2*1.5:.1f}" height="{S2*3:.1f}" fill="#B9D9EE" stroke="{BLU}" stroke-width="1.5"/>')
a(f'<line x1="{dx1(0.8):.1f}" y1="{pz(75):.1f}" x2="{dx1(22.5):.1f}" y2="{pz(75):.1f}" stroke="{DK}" stroke-width="4"/>')
a(f'<line x1="{dx1(22.5):.1f}" y1="{pz(75):.1f}" x2="{dx1(22.5):.1f}" y2="{pz(1.3):.1f}" stroke="{P}" stroke-width="3" stroke-opacity="0.85"/>')
for dz in (3.0,6.0,9.0):
    a(f'<circle cx="{dx1(22.5)+0.0:.1f}" cy="{pz(1.9):.1f}" r="3.2" fill="{DK}"/>')
    break
a(f'<text class="th" x="{dx1(22.5)+8:.1f}" y="{pz(40):.1f}" style="font-size:11px;fill:{P};paint-order:stroke;stroke:#fff;stroke-width:3px">plastic curtain, 74 in long</text>')
a(f'<text class="ts" x="{dx1(22.5)+8:.1f}" y="{pz(40)+13:.1f}" style="font-size:10px;fill:{P}">hangs free from the ceiling rod</text>')
a(f'<text class="th" x="{dx1(22.5)+10:.1f}" y="{pz(9):.1f}" style="font-size:10.5px;paint-order:stroke;stroke:#fff;stroke-width:3px">no rod: free hem with</text><text class="th" x="{dx1(22.5)+10:.1f}" y="{pz(9)+12:.1f}" style="font-size:10.5px;paint-order:stroke;stroke:#fff;stroke-width:3px">small weights, inside the curb</text>')
a(f'<text class="ts" x="{dx1(24)-6:.1f}" y="{pz(1.5):.1f}" text-anchor="end" style="font-size:10px">3 in curb,</text><text class="ts" x="{dx1(24)-6:.1f}" y="{pz(1.5)+12:.1f}" text-anchor="end" style="font-size:10px">1 1/2 in inset</text>')
a(f'<text class="ts" x="{dx1(12):.1f}" y="{FL+18}" text-anchor="middle" style="font-size:11px">pan 24 deep</text>')
a('</svg>')
_svg='\n'.join(o)
_blk='<h3>E3. Shower curtains on three sides, with a fixed pan and the toilet at the cab end</h3>\n<div class="wide">'+_svg+'</div>\n'
_blk+='<p>Two flexible plastic curtains, like a home shower curtain, hang free from one rail at the ceiling on the three open sides of the stall (the back wall, along the passenger wall, is lined with PVC paneling, glued over the plywood), and slide round on it (left: looking down at the 36 x 24 in pan). The rod runs 1 1/2 in inside the pan\'s edge, 33 in across the front and 22 1/2 in down each end, and the two curtains overlap 6 in in the middle of the front. The only rail is the one at the ceiling (a bendable ceiling track bent to a U, fixed up into the ceiling slats; it replaces the wall W3 the plan had at the cab end); there is no rod in the hem: the bottom is free, with small weights (a light stainless chain or sewn-in weights) that keep it inside the 3 in curb in use. Right: from the rear, along the wall.</p>\n'
_blk+='<p><b>The toilet.</b> The Reliance Fold-To-Go (14 1/2 in square and 14 1/2 in high, a folding seat on four legs that holds a bag) stays set up on the pan at the cab end, sideways, with its back half an inch short of the cab-end curtain, next to the fridge (19 1/2 to 34 in from the back; there is no wall between the shower and the fridge now, so the fridge\'s side stands just outside the curtain). That leaves 19 1/2 in of the pan in front of it to stand and shower, and 4 3/4 in each side of it. It gets wet when you shower: wipe the seat. The drain is at the middle of the rear-door end of the pan (5 in from the rear end, as you said, and 12 out from the wall, the middle of the depth: assumed, check it on the pan), the pan sloping to it, and runs straight down through the floor to the grey water tank under the van. The pan is bought (36 x 24), fixed and does not tip; the Shower pan page of the build guide shows how to set it.</p>\n'
_blk+='<p><b>Things to watch:</b> (1) no stiff rod in the hem, so the hem stays free and the weights hold it inside the 3 in curb; (2) the rod runs to the wall so the curtain seals the ends; (3) wipe the pan and the curtains dry, or the plastic mildews; (4) the toilet paper in the shower nook is about 12 in along the wall from the shower head and faces the stall, so give it a small hinged door or a lidded holder; (5) hold the curtains aside with a loop or a magnet at the ceiling while driving. Total fabric: about 80 to 100 in wide by 74 in long, as two curtains (each about 40 to 50 in wide), cut from standard 72 in curtains.</p>\n'
_h=_h.replace('<h2>Driver side photos</h2>',_blk+'<h2>Driver side photos</h2>',1)
open(_path,'w').write(_h)
