# Two ways to place the charging gear (BELTTT 2000 W inverter, LiTime 60 A DC-DC, VEVOR 80 A): under the couch beside the battery and wheel well, or in a recess in the driver wall behind the couch.
# Writes an artifact fragment (index.html) and a standalone preview into the folder given as the first argument. Not part of build.sh: it is a comparison, not the plan.
import sys, os
OUT = sys.argv[1]
INK='#26241f'; MUTE='#6a665c'; AMB='#B45309'; BLU='#185FA5'; RED='#A32D2D'; BRN='#8A6B4D'; GRN='#0F6E56'
def T(x,y,s,sz=11,col=INK,anchor='middle',w=400,extra=''):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="font-size:{sz}px;font-weight:{w};fill:{col};paint-order:stroke;stroke:#fbfaf6;stroke-width:3px;stroke-linejoin:round" {extra}>{s}</text>'
def R(x,y,w,h,fill='none',stroke=INK,sw=1.4,dash='',fo=1,rx=2):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def L(x1,y1,x2,y2,col=INK,sw=1.4,dash=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d}/>'
def svg(w,h,body,label):
    return f'<svg viewBox="0 0 {w} {h}" role="img" aria-label="{label}" style="width:100%;height:auto;display:block"><rect width="{w}" height="{h}" fill="#fbfaf6"/><g font-family="Inter,Arial,sans-serif">{body}</g></svg>'

# ---------------- option A, top view (looking down under the couch) ----------------
def a_top():
    S=11.5; X0=34; Y0=40; xa=lambda x: X0+(x-28)*S; ya=lambda y: Y0+y*S
    W=int(xa(80)+30); H=int(ya(29)+20); o=[]
    o.append(T(X0,20,'Looking down under the couch (deck removed). Driver wall at the top, the couch front at the bottom.',12,INK,'start',700))
    o.append(L(xa(28),ya(0),xa(80),ya(0),INK,5))
    o.append(T(xa(28)+2,ya(0)-8,'driver wall',10,MUTE,'start'))
    o.append(R(xa(42),ya(0),(76-42)*S,7*S,'#D8B79A',BRN,1.4,'',.8))
    o.append(T(xa(59),ya(3.7),'wheel well: 7 out, 7.5 tall',10,'#5A3A00'))
    o.append(R(xa(28),ya(0),(34.5-28)*S,21.7*S,'#cfd2d6','#8a8d92',1.2,'4 3',.8)); o.append(T(xa(31.2),ya(11),'chairs',10,MUTE,'middle','400','transform="rotate(-90 %.1f %.1f)"'%(xa(31.2),ya(11))))
    o.append(R(xa(52),ya(7),21*S,10*S,'#F2B84B',AMB,1.8,'',.45)); o.append(T(xa(62.5),ya(10),'battery 21 x 10 x 9.5',10.5,'#5A3A00')); 
    o.append(L(xa(74),ya(0),xa(74),ya(26),INK,3)); o.append(T(xa(74)+4,ya(14),'closet',10,MUTE,'start'))
    o.append(R(xa(34.5),ya(25.25),(74-34.5)*S,.75*S,'#e3dccd',BRN,1,'',1,0))
    o.append(T(xa(54),ya(27.9),'removable louvered panel in the couch front (3/4 thick)',10,'#5A3A00'))
    # units
    def unit(x0,x1,y0,y1,name,dim,col):
        return R(xa(x0),ya(y0),(x1-x0)*S,(y1-y0)*S,col,AMB,2,'',.28)+T(xa((x0+x1)/2),ya((y0+y1)/2)-2,name,11,'#5A2A00','middle',700)+T(xa((x0+x1)/2),ya((y0+y1)/2)+11,dim,10,'#5A2A00')
    o.append(unit(35.5,51.5,8,17,'DC-DC LiTime 60 A','16 x 9 x 4.5','#F6C28B'))
    o.append(unit(36,45.5,17.5,24.5,'VEVOR 80 A','9.5 x 7 x 4','#F6C28B'))
    o.append(unit(52.5,67.3,17.3,25,'Inverter BELTTT 2000 W','14.8 x 7.7 x 3.9','#F6C28B'))
    # gaps
    o.append(T(xa(51.75),ya(7.2),'1/2',9,RED,'middle',700)); o.append(T(xa(67.9),ya(27.2)-1,'1/4 to the panel',9,RED,'start',700)); o.append(T(xa(35),ya(17.2)+3,'',9))
    o.append(L(xa(60),ya(17.3),xa(60),ya(17),RED,2))
    o.append(T(xa(70.2),ya(21.3),'battery cables',9.5,RED,'start',700)); o.append(T(xa(70.2),ya(22.9),'about 1 ft',9.5,RED,'start',700))
    o.append(T(xa(41),ya(5.8),'1 in to the chairs',9.5,RED,'middle',700))
    o.append(L(xa(34.5),ya(5),xa(35.5),ya(5),RED,2))
    return svg(W,H,''.join(o),'Option A top view')

# ---------------- option A, front view (panel off) ----------------
def a_front():
    S=11.5; X0=34; Z0=190; xa=lambda x: X0+(x-28)*S; za=lambda z: Z0-z*S
    W=int(xa(80)+80); H=Z0+46; o=[]
    o.append(T(X0,20,'The same, seen from the aisle with the front panel off',12,INK,'start',700))
    o.append(L(xa(28),za(0),xa(80),za(0),INK,3))
    o.append(R(xa(28),za(14),(74-28)*S,(14-12.5)*S,'#D9C7A5',BRN,1,'',.7,0)); o.append(T(xa(74),za(14)-5,'couch deck',10,MUTE,'end'))
    o.append(R(xa(28),za(12.5),(74-28)*S,1.5*S,'#c9b79a',BRN,1,'',.6,0)); o.append(T(xa(76),za(11.6),'front rail',10,MUTE,'start'))
    o.append(L(xa(28),za(12.5),xa(74),za(12.5),BRN,1.2,'5 3'))
    # wheel well (behind)
    pts=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
    o.append('<polygon points="'+' '.join(f'{xa(x):.1f},{za(z):.1f}' for x,z in pts)+f'" fill="#D8B79A" fill-opacity=".6" stroke="{BRN}" stroke-width="1.2"/>')
    o.append(R(xa(52),za(9.5),21*S,9.5*S,'#F2B84B',AMB,1.4,'4 3',.3)); o.append(T(xa(70),za(8),'battery (behind)',9.5,'#5A3A00','middle',400))
    o.append(R(xa(35.5),za(4.5),16*S,4.5*S,'#F6C28B',AMB,1.8,'',.5)); o.append(R(xa(36),za(4),9.5*S,4*S,'#F6C28B',AMB,1.8,'',.7))
    o.append(T(xa(40.7),za(2),'VEVOR (in front)',9.5,'#5A2A00','middle',700)); o.append(T(xa(48.3),za(5.8),'DC-DC 4.5',9.5,'#5A2A00','middle',700))
    o.append(R(xa(52.5),za(3.9),14.8*S,3.9*S,'#F6C28B',AMB,1.8,'',.7)); o.append(T(xa(59.9),za(1.9),'Inverter 3.9 tall',9.5,'#5A2A00','middle',700))
    o.append(L(xa(80),za(12.5),xa(80),za(4.5),RED,1.6)); o.append(T(xa(80)+6,za(8.5),'about 8 in of',9.5,RED,'start',700)); o.append(T(xa(80)+6,za(8.5)+11,'air above',9.5,RED,'start',700))
    o.append(T(xa(54),Z0+30,'inches along the wall from the back: 28 to 80',10,MUTE))
    return svg(W,H,''.join(o),'Option A front view')

# ---------------- option B, the wall from the aisle ----------------
def b_front():
    S=7.2; X0=40; Z0=560; xb=lambda x: X0+x*S; zb=lambda z: Z0-z*S
    W=int(xb(80)+40); H=Z0+36; o=[]
    o.append(T(X0,20,'The driver wall seen from the aisle: the gear in a recess above the back cushion',12,INK,'start',700))
    o.append(L(xb(0),zb(0),xb(80),zb(0),INK,3))
    o.append(R(xb(0),zb(74.5),74*S,13.5*S,'#c9c4e6','#534AB7',1.2,'',.35,2)); o.append(T(xb(37),zb(66),'wall cabinet, bottom at 61',10.5,'#534AB7'))
    o.append(R(xb(0),zb(20),74*S,20*S,'#d9d6ee','#534AB7',1.2,'',.6,3)); o.append(T(xb(2),zb(24),'couch back cushion (top 40)',10.5,'#534AB7','start'))
    o.append(R(xb(0),zb(14),74*S,6*S,'#d9d6ee','#534AB7',1.2,'',.5,3)); o.append(R(xb(0),zb(14),74*S,0.01,'none','#534AB7',0))
    o.append(R(xb(52),zb(9.5),21*S,9.5*S,'#F2B84B',AMB,1.4,'',.45)); o.append(T(xb(62.5),zb(4.5),'battery',10,'#5A3A00'))
    # the recess and the gear
    o.append(R(xb(20),zb(56),52*S,15*S,'#7A4A1E',BRN,1.8,'5 3',.1,3)); o.append(T(xb(46),zb(57.4),'recess in the wall, 4.5 deep, 41 to 56 up (the pans start at 31)',10,'#5A3A00'))
    def unit(x0,w,h,name,dim):
        return R(xb(x0),zb(43+h),w*S,h*S,'#F6C28B',AMB,2,'',.55)+T(xb(x0+w/2),zb(43+h/2)-2,name,10.5,'#5A2A00','middle',700)+T(xb(x0+w/2),zb(43+h/2)+10,dim,9.5,'#5A2A00')
    o.append(unit(22,14.8,7.7,'Inverter','14.8 x 7.7'))
    o.append(unit(38,16,9,'DC-DC','16 x 9'))
    o.append(unit(55.5,9.5,7,'VEVOR','9.5 x 7'))
    o.append(R(xb(20.5),zb(55.5),51*S,14*S,'none','#5A3A00',1.4,'2 3',1,2)); o.append(T(xb(66),zb(41.3)+1,'hinged louvered panel',9.5,'#5A3A00'))
    # cable route
    o.append(f'<polyline points="{xb(56)},{zb(9.5)} {xb(56)},{zb(30)} {xb(30)},{zb(30)} {xb(30)},{zb(43)}" fill="none" stroke="{RED}" stroke-width="2.4" stroke-dasharray="6 4"/>')
    o.append(T(xb(43),zb(31.8),'2/0 cables up the wall: about 4 to 5 ft each way',10,RED,'middle',700))
    o.append(T(xb(37),Z0+26,'inches along the wall from the back: 0 to 74',10,MUTE))
    return svg(W,H,''.join(o),'Option B wall view')

# ---------------- option B, cross-section ----------------
def b_section():
    S=14; Y0=120; yb=lambda y: Y0+y*S; zb=lambda z: 66+(60-z)*S
    W=int(yb(16)+30); H=int(zb(36)+34); o=[]
    o.append(T(20,20,'Cut across the recess, looking along the wall',12,INK,'start',700))
    o.append(T(20,36,'(wall on the left, aisle on the right)',10,MUTE,'start'))
    o.append(R(yb(-4.5)-12,zb(56),12,20*S,'#8a8d92','#5F5E5A',1,'',.6,0)); o.append(T(yb(-4.5)-14,zb(57)-2,'body',10,MUTE,'end'))
    o.append(L(yb(0),zb(60),yb(0),zb(56),INK,3)); o.append(L(yb(0),zb(41),yb(0),zb(36),INK,3))
    o.append(L(yb(-4.5),zb(56),yb(0),zb(56),INK,3)); o.append(L(yb(-4.5),zb(41),yb(0),zb(41),INK,3)); o.append(L(yb(-4.5),zb(41),yb(-4.5),zb(56),INK,3))
    o.append(T(yb(-2.2),zb(58.2),'recess 4 1/2 deep',10.5,'#5A3A00')); 
    # units (they sit at different places along the wall; shown overlapped)
    o.append(R(yb(-4.5),zb(43+9),4.5*S,9*S,'#F6C28B',AMB,2,'',.5,0)); o.append(R(yb(-4.5),zb(43+7.7),3.9*S,7.7*S,'#F6C28B',AMB,1.6,'4 3',.5,0)); o.append(R(yb(-4.5),zb(43+7),4*S,7*S,'#F6C28B','#7A3B07',1.4,'2 3',.4,0))
    o.append(T(yb(1.4),zb(48.6),'gear: 3.9, 4 and 4.5 thick',10.5,'#5A2A00','start',700)); o.append(T(yb(1.4),zb(47.2),'(the DC-DC fills the whole depth)',10.5,'#5A2A00','start',700))
    o.append(R(yb(0.15),zb(55.5),0.75*S,14*S,'#e3dccd',BRN,1.2,'',.9,0)); o.append(T(yb(1.4),zb(55.2),'louvered panel: it has to stand',10.5,'#5A3A00','start')); o.append(T(yb(1.4),zb(55.2)+12,'3/4 in proud of the wall',10.5,'#5A3A00','start'))
    o.append(R(yb(0.3),zb(40),6*S,4*S,'#d9d6ee','#534AB7',1.2,'',.7,3)); o.append(T(yb(6.6),zb(38.4),'back cushion, top at 40',10,'#534AB7','start'))
    o.append(f'<circle cx="{yb(10.5):.1f}" cy="{zb(51):.1f}" r="{4.2*S/2+8:.1f}" fill="#f1d8c0" stroke="#7a5a3a" stroke-width="1.4"/>'); o.append(T(yb(10.5),zb(51)+3,'head',10.5,'#5a3a1a')); o.append(T(yb(10.5),zb(45.2),'seated: 1 to 2 ft',10.5,RED,'middle',700)); o.append(T(yb(10.5),zb(45.2)+12,'from the fans',10.5,RED,'middle',700))
    return svg(W,H,''.join(o),'Option B cross-section')

CSS = """
:root{--bg:#fbfaf6;--card:#fff;--ink:#26241f;--mute:#6a665c;--line:#d9d5ca;--acc:#B45309;--ok:#0F6E56;--warn:#8A5A00;--bad:#A32D2D}
@media (prefers-color-scheme: dark){:root:not([data-theme="light"]){--bg:#17160f;--card:#201f17;--ink:#ece8dc;--mute:#a8a396;--line:#3a3829;--acc:#E39A4A;--ok:#4EC3A0;--warn:#E3B24A;--bad:#F08A80;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#17160f;--card:#201f17;--ink:#ece8dc;--mute:#a8a396;--line:#3a3829;--acc:#E39A4A;--ok:#4EC3A0;--warn:#E3B24A;--bad:#F08A80;color-scheme:dark}
body{background:var(--bg);color:var(--ink);font-family:Inter,system-ui,sans-serif;line-height:1.5;padding-block:20px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}
.wrap{max-width:980px;margin:0 auto}
h1{font-size:26px;margin:0 0 6px;text-wrap:balance}h2{font-size:19px;margin:30px 0 8px;text-wrap:balance}
.lead{color:var(--mute);margin:0 0 14px;max-width:70ch}
.fig{background:#fbfaf6;border:1px solid var(--line);border-radius:10px;overflow:hidden;margin:10px 0}
.cols{display:grid;grid-template-columns:1fr;gap:12px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:12px 16px;min-width:0}
ul{margin:6px 0 0;padding-left:20px}li{margin:3px 0}
.tag{display:inline-block;font-size:12px;font-weight:700;letter-spacing:.04em;text-transform:uppercase;padding:2px 8px;border-radius:99px;border:1px solid currentColor}
.ok{color:var(--ok)}.warn{color:var(--warn)}.bad{color:var(--bad)}
table{border-collapse:collapse;width:100%;font-size:14px}th,td{border-bottom:1px solid var(--line);padding:7px 8px;text-align:left;vertical-align:top}th{color:var(--mute);font-weight:600}
.scroll{overflow-x:auto}
"""
BODY = f"""
<div class="wrap">
<h1>Charging gear: two ways to place it</h1>
<p class="lead">The BELTTT 2000 W inverter (14.8 x 7.7 x 3.9 in, from its listing), the LiTime 60 A DC-DC charger (16 x 9 x 4.5, as you measured) and the VEVOR 80 A shore charger (9.5 x 7 x 4, as you measured). Both layouts are drawn to the same scale from the plan's own numbers. A is what the plan has now; B is the recess in the driver wall behind the couch, as an alternative.</p>

<h2>A. Under the couch, around the battery and the wheel well <span class="tag ok">in the plan</span></h2>
<div class="cols"><div class="fig">{a_top()}</div><div class="fig">{a_front()}</div></div>
<div class="card"><ul>
<li><b>Fits, but tight:</b> the smallest gap is 1/4 in (the inverter to the couch front panel), then 5/16 in to the battery, 1/2 in for the DC-DC to the battery. Fans need about an inch beside them, so real units have to be measured in place; the panel can be thin or notched.</li>
<li><b>Cables:</b> the inverter is in front of the battery, so its battery cables are about 1 ft; the DC-DC sits behind the battery.</li>
<li><b>Noise and heat:</b> at floor level, under the bed deck; about 8 in of air above the tallest unit; louvers in the removable panel.</li>
<li><b>Access:</b> take the couch front panel off; nothing to move on the couch.</li>
</ul></div>

<h2>B. In the wall recess behind the couch <span class="tag warn">alternative</span></h2>
<div class="cols"><div class="fig">{b_front()}</div><div class="fig">{b_section()}</div></div>
<div class="card"><ul>
<li><b>Depth is the problem:</b> the units are 3.9, 4 and 4.5 in thick and the recess is 4.5 deep, so the DC-DC fills it exactly. A louvered panel then has to stand about 3/4 in proud of the wall, and the 4.5 deep recess only exists from 31 in up (lower, the steel is closer). I have not measured the driver wall there.</li>
<li><b>Cables:</b> the battery is on the floor, so each 2/0 cable climbs about 3 ft plus the run along the wall: 4 to 5 ft, and a Class T fuse at the battery.</li>
<li><b>Noise and heat:</b> at 41 to 56 in up the fans are 1 to 2 ft from a seated head, and the recess backs onto the outside wall.</li>
<li><b>Access:</b> easy: a hinged panel above the back cushion, so no cushion has to move.</li>
<li><b>It leaves the floor under the couch free</b> (the lawn chairs could use it).</li>
</ul></div>

<h2>Side by side</h2>
<div class="scroll"><table>
<thead><tr><th></th><th>A. Under the couch</th><th>B. Wall recess</th></tr></thead>
<tbody>
<tr><td>Battery cables</td><td class="ok">about 1 ft</td><td class="warn">4 to 5 ft each way</td></tr>
<tr><td>Fits the sizes</td><td class="warn">yes, 1/4 to 1/2 in gaps</td><td class="bad">only if the panel stands proud (DC-DC fills the recess)</td></tr>
<tr><td>Fan noise near your head</td><td class="ok">low, under the deck</td><td class="bad">1 to 2 ft from a seated head</td></tr>
<tr><td>Heat</td><td class="ok">8 in of air, louvers</td><td class="warn">closed recess, needs louvers</td></tr>
<tr><td>Measured?</td><td class="ok">floor space measured</td><td class="bad">wall depth at 41 to 56 up not measured</td></tr>
<tr><td>Access</td><td class="ok">remove the front panel</td><td class="ok">hinged panel</td></tr>
</tbody></table></div>
<p class="lead" style="margin-top:12px">My pick is A. If the gaps prove too tight once you hold the real units against the floor, the way out is to move the VEVOR charger (the smallest) into a wall recess and keep the other two under the couch.</p>
</div>
"""
frag = '<meta name="claude:viewport-fit-sides" content="cover">\n<title>Charging Gear Options</title>\n<style>'+CSS+'</style>\n'+BODY
open(os.path.join(OUT,'index.html'),'w',encoding='utf-8').write(frag)
open(os.path.join(OUT,'preview.html'),'w',encoding='utf-8').write('<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"></head><body style="margin:0">'+frag+'</body></html>')
print('written', len(frag))
