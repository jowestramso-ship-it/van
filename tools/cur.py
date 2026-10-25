_path=(ROOT+'/sides.html')
_h=open(_path).read()
W=1040; H=620
o=[]; a=o.append
a(f'<svg viewBox="0 0 {W} {H}" role="img"><title>Shower curtains on three sides, pan down and pan tipped up</title>')
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
a(f'<text class="ts" x="{px(18):.1f}" y="{py(0)+20:.1f}" text-anchor="middle" style="font-size:12px">passenger wall, with the hinge along it</text>')
a(f'<text class="ts" x="{px(0)-8:.1f}" y="{py(12):.1f}" text-anchor="end" style="font-size:11px">rear</text>')
a(f'<circle cx="{px(18):.1f}" cy="{py(4):.1f}" r="7" fill="{DK}"/><text class="ts" x="{px(18)-12:.1f}" y="{py(4)+4:.1f}" text-anchor="end" style="font-size:11px">drain, next to the hinge</text>')
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
a(f'<text class="th" x="{px(18):.1f}" y="{py(13):.1f}" text-anchor="middle" style="font-size:15px;fill:{BLU}">pan 36 x 24</text><text class="ts" x="{px(18):.1f}" y="{py(13)+16:.1f}" text-anchor="middle" style="font-size:11px">33 x 22 1/2 inside the curtains</text>')
a(f'<text class="ts" x="{px(18):.1f}" y="{py(24)-30:.1f}" text-anchor="middle" style="font-size:10.5px">ceiling rod (dashed), 1 1/2 in inside the pan edge</text>')
a(f'<line x1="{px(28):.1f}" y1="{py(10):.1f}" x2="{px(28):.1f}" y2="{py(2.5):.1f}" stroke="#A32D2D" stroke-width="2" marker-end="url(#ar3)"/><text class="ts" x="{px(28)-6:.1f}" y="{py(8):.1f}" text-anchor="end" style="font-size:10.5px;fill:#A32D2D">pan tips up toward the wall</text>')
# ---------- right: from the rear, along the wall ----------
S2=7.0; FL=570
pz=lambda z:FL-S2*z
def view(Wx,title):
    a(f'<text class="th" x="{Wx-176}" y="24" style="font-size:14px">{title}</text>')
    a(f'<line x1="{Wx-190}" y1="{FL}" x2="{Wx+10}" y2="{FL}" stroke="{DK}" stroke-width="3"/>')
    a(f'<line x1="{Wx-190}" y1="{pz(76):.1f}" x2="{Wx+10}" y2="{pz(76):.1f}" stroke="#5F5E5A" stroke-width="1.5" stroke-dasharray="7 4"/>')
    a(f'<line x1="{Wx}" y1="{pz(76):.1f}" x2="{Wx}" y2="{FL}" stroke="{DK}" stroke-width="4"/>')
    a(f'<text class="ts" x="{Wx-186}" y="{pz(76)-4:.1f}" style="font-size:10.5px">ceiling 76</text>')
    a(f'<text class="ts" x="{Wx-4}" y="{pz(76)+14:.1f}" text-anchor="end" style="font-size:10.5px">wall</text>')
# state 1: in use
W1=640
view(W1,'In use: pan down')
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
# state 2: curtains pulled to the sides, pan tipped up
W2=1000
view(W2,'Curtains to the sides, pan up')
dx2=lambda d:W2-S2*d
a(f'<rect x="{W2-S2*4.5:.1f}" y="{pz(56.5):.1f}" width="{S2*4.5:.1f}" height="{S2*25.5:.1f}" fill="{BR}" fill-opacity="0.2" stroke="{BR}" stroke-width="1.5" stroke-dasharray="5 3"/>')
a(f'<text class="ts" x="{W2-40}" y="{pz(44):.1f}" text-anchor="end" style="font-size:10.5px;fill:#5A3510;paint-order:stroke;stroke:#fff;stroke-width:3px">shower nook, 31 to 56 1/2 in</text>')
a(f'<rect x="{dx2(3.5):.1f}" y="{pz(24.5):.1f}" width="{S2*3.5:.1f}" height="{S2*24:.1f}" fill="#D9ECF7" stroke="{BLU}" stroke-width="1.5"/>')
a(f'<circle cx="{W2-1}" cy="{pz(0.8):.1f}" r="5" fill="{DK}"/><text class="ts" x="{W2-12}" y="{pz(0.8)+3:.1f}" text-anchor="end" style="font-size:10.5px">hinge</text>')
a(f'<rect x="{dx2(3.5)-5:.1f}" y="{pz(22):.1f}" width="6" height="12" fill="{DK}"/><text class="ts" x="{dx2(3.5)-4:.1f}" y="{pz(28):.1f}" text-anchor="end" style="font-size:10.5px">latch (catch on S3)</text>')
a(f'<line x1="{dx2(0.8):.1f}" y1="{pz(75):.1f}" x2="{dx2(22.5):.1f}" y2="{pz(75):.1f}" stroke="{DK}" stroke-width="4"/>')
# gathered curtain: hangs from the track near the wall, over the top of the pan, into the pan against the wall
cpath=f'M{dx2(8):.1f} {pz(75):.1f} L{dx2(8):.1f} {pz(34):.1f} Q{dx2(8):.1f} {pz(26):.1f} {dx2(4.5):.1f} {pz(25.5):.1f} L{dx2(3.5)+1:.1f} {pz(24.5)-2:.1f} L{dx2(1.6):.1f} {pz(10):.1f}'
a(f'<path d="{cpath}" fill="none" stroke="{P}" stroke-width="9" stroke-opacity="0.55" stroke-linecap="round" stroke-linejoin="round"/>')
a(f'<path d="{cpath}" fill="none" stroke="{P}" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>')
a(f'<text class="th" x="{dx2(8)-12:.1f}" y="{pz(58):.1f}" text-anchor="end" style="font-size:11px;fill:{P};paint-order:stroke;stroke:#fff;stroke-width:3px">curtains gathered at the</text><text class="th" x="{dx2(8)-12:.1f}" y="{pz(58)+13:.1f}" text-anchor="end" style="font-size:11px;fill:{P};paint-order:stroke;stroke:#fff;stroke-width:3px">sides, hanging free</text>')
a(f'<text class="ts" x="{dx2(14):.1f}" y="{pz(11):.1f}" text-anchor="middle" style="font-size:10px;fill:#A32D2D;paint-order:stroke;stroke:#fff;stroke-width:3px">the pan carries the hems into the</text><text class="ts" x="{dx2(14):.1f}" y="{pz(11)+12:.1f}" text-anchor="middle" style="font-size:10px;fill:#A32D2D;paint-order:stroke;stroke:#fff;stroke-width:3px">gap between pan and wall</text>')
a(f'<path d="M{dx2(24):.1f} {FL-6} A{S2*24:.1f} {S2*24:.1f} 0 0 1 {W2-8} {pz(24.5):.1f}" fill="none" stroke="#A32D2D" stroke-width="2" stroke-dasharray="6 4"/>')
a(f'<text class="ts" x="{dx2(12):.1f}" y="{FL+18}" text-anchor="middle" style="font-size:11px">pan up: 24 tall, 3 1/2 thick (sketch of the curtain)</text>')
a('</svg>')
_svg='\n'.join(o)
_blk='<h3>E3. Shower curtains on three sides (the pan no longer tips up: it is fixed, so the second state, curtains pulled aside and the pan tipped, is not used)</h3>\n<div class="wide">'+_svg+'</div>\n'
_blk+='<p>Two flexible plastic curtains, like a home shower curtain, hang free from a rod at the ceiling on three sides, and slide around on it (left: looking down at the 36 x 24 in pan). The rod runs 1 1/2 in inside the pan\'s edge, 33 in across the front and 22 1/2 in down each end, and the two curtains overlap 6 in in the middle of the front. The only rod is the one at the ceiling; there is no rod in the hem: the bottom is free, with small weights (a light stainless chain or sewn-in weights) that keep it inside the 3 in curb in use. Right: from the rear, along the wall.</p>\n'
_blk+='<p><b>Folding the pan:</b> pull both curtains to the sides, so they lie in the pan. Then tip the pan up toward the wall. Because the curtains are loose plastic, nothing blocks the pan: it carries the hems with it and they fold into the gap between the pan and the wall, and the rest hangs from the ceiling rod against the folded pan. The pan stands 24 in tall and about 3 1/2 in thick, and its top (24 1/2 in) stays 6 1/2 in below the shower nook (31 in). The drawing of the folded curtain is a sketch; plastic drapes however it falls.</p>\n'
_blk+='<p><b>Things to watch:</b> (1) no stiff rod in the hem, as it would jam between the pan and the wall; (2) the rod runs to the wall so the curtain seals the ends in use, which means the parked curtain is pinched against the wall when the pan is up; if you stop the rod about 5 in short of the wall instead, the curtain is not pinched, but each back corner then has a 5 in gap where spray can escape; (3) wipe the pan and curtains dry before folding, or the pinched plastic mildews; (4) keep the lowest few inches of the curtain away from the hinge and the drain hose; (5) hold the gathered curtains with a loop or magnet at the ceiling while driving. Total fabric: about 80 to 100 in wide by 74 in long, as two curtains (each about 40 to 50 in wide), cut from standard 72 in curtains.</p>\n'
_h=_h.replace('<h2>Driver side photos</h2>',_blk+'<h2>Driver side photos</h2>',1)
open(_path,'w').write(_h)
