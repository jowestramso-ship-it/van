# G: the ceiling covering seen from above through the roof: plywood pieces, slats, round lights on the slats, the roof ribs, the roof fan and air conditioning cutouts
# physical positions from the rear doors (the datum used on the other diagrams is 6 in in from the rear edge)
SC=5; X0=70; Y0=46
CL=160; CW=68
xx=lambda x: X0+SC*x
yy=lambda y: Y0+SC*y
import math
def fr(v):
    # inches as a mixed number in sixteenths
    w=int(v); n=round((v-w)*16)
    if n==16: w+=1; n=0
    if n==0: return str(w)
    from math import gcd
    g=gcd(n,16); f='%d/%d'%(n//g,16//g)
    return f if w==0 else '%d %s'%(w,f)
# the roof ribs (edge nearest the rear doors, 2 3/4 wide) and the six furring strips under them
RIBS=[(21.75,24.5),(37.875,40.625),(58.375,61.125),(97.375,100.125),(126.375,129.125)]
PLYX=[59.75,127.75]            # the plywood seams across the van: the middle of rib 3 and rib 5 (pieces 59 3/4, 68 and 32 1/4 long)
BW=2.5; BT=0.5                 # the furring strips: 1/2 x 2 1/2 in (user, 2026-11-11: 'going length wise ... held on via steel ribs ... 1/2 in ... 6 across the whole ceiling'); width assumed
JOINTS=(23.125,98.75)          # the strip joints, on the middle of rib 1 and rib 4 (never at the plywood seams, which are on rib 3 and rib 5)
PIECES=[(0,JOINTS[0]),(JOINTS[0],JOINTS[1]),(JOINTS[1],CL)]
LIGHTS=((26.5,58),(95.375,58),(35.875,34),(102.125,34)); LD=2.75; LH=2.25   # the four lights (from the rear doors, across from the driver wall), the puck and its hole: the same as in the plan's lights
STRIPS=(('CB1','driver side wall top, under the trim',4.25),('CB4','between CB1 and the openings',14),('CB5','beside the openings, driver side',24.25),('CB6','beside the openings, aisle side',43.6),('CB3','under the long plywood seam',51),('CB2','passenger side wall top, under the trim',63.75))
RAILS=tuple((i_,n_,y_-BW/2,y_+BW/2) for i_,n_,y_ in STRIPS)   # (id, name, y0, y1) across from the driver wall
def _g():
    o=[]; a=o.append
    W=xx(CL)+90; H=yy(CW)+86
    a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img"><title>The ceiling covering from above: plywood, slats, lights, roof ribs, fan and air conditioning cutouts</title>')
    a('<defs><marker id="arg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    a(f'<text x="{X0}" y="26" style="font-size:12px;fill:#5F5E5A">Seen from above through the roof: rear doors on the left, cab wall on the right, driver side at the top. Measured from the rear doors.</text>')
    # plywood: 4 x 8 ft sheets, long way along the van, in six pieces; the seams across the van are on the middle of rib 3 and rib 5 (59 3/4 and 127 3/4 from the rear doors: they fell at 96 with sheets from the rear doors, across the countertop light's hole), and the long seam is 51 in across
    cx=[0]+PLYX+[160]; cy=[3,51,65]
    for i in range(len(cx)-1):
        for j in range(2):
            a(f'<rect x="{xx(cx[i]):.1f}" y="{yy(cy[j]):.1f}" width="{SC*(cx[i+1]-cx[i]):.1f}" height="{SC*(cy[j+1]-cy[j]):.1f}" fill="#D9C7A5" fill-opacity="0.8" stroke="#8A6B4D" stroke-width="1.2"/>')
    # slats: 15 rows of 3 in with 1 in gaps (1 1/2 in left each side of the 62 in flat part), cut where the openings cross them
    fan=(13.25,34,14); ac=(49.5,34,14.25)
    cut=[(c[0]-c[2]/2,c[0]+c[2]/2,c[1]-c[2]/2,c[1]+c[2]/2) for c in (fan,ac)]
    ys=[4.5+4*k for k in range(15)]
    cutn=[0,0]
    LIGHTS=((26.5,58),(95.375,58),(35.875,34),(102.125,34))   # the lights, from the rear doors and across from the driver wall (the same as in the plan's ceiling lights); each slat is cut away LGAP in at its light
    LGAP=3; LD=2.75; LH=2.25
    for y0 in ys:
        parts=[(0,CL)]
        for ci,(x0,x1,ya,yb) in enumerate(cut):
            if y0<yb and y0+3>ya:
                cutn[ci]+=1
                nx=[]
                for p0,p1 in parts:
                    if x1<=p0 or x0>=p1: nx.append((p0,p1))
                    else:
                        if x0>p0: nx.append((p0,x0))
                        if x1<p1: nx.append((x1,p1))
                parts=nx
        for lx,ly in LIGHTS:
            if abs(y0+1.5-ly)<.01:
                nx=[]
                for p0,p1 in parts:
                    g0,g1=lx-LGAP/2,lx+LGAP/2
                    if g1<=p0 or g0>=p1: nx.append((p0,p1))
                    else:
                        if g0>p0: nx.append((p0,g0))
                        if g1<p1: nx.append((g1,p1))
                parts=nx
        for p0,p1 in parts:
            a(f'<rect x="{xx(p0):.1f}" y="{yy(y0):.1f}" width="{SC*(p1-p0):.1f}" height="{SC*3:.1f}" fill="#9A6B3A" fill-opacity="0.9" stroke="#5A3A00" stroke-width="0.8"/>')
    # the five roof ribs (their edge nearest the rear doors), dashed, over the covering
    for _i,_rx in enumerate((21.75,37.875,58.375,97.375,126.375)):
        a(f'<rect x="{xx(_rx):.1f}" y="{yy(0):.1f}" width="{SC*2.75:.1f}" height="{SC*CW:.1f}" fill="#A32D2D" fill-opacity="0.14" stroke="#A32D2D" stroke-width="1.2" stroke-dasharray="6 3"/>')
        a(f'<text x="{xx(_rx+1.375):.1f}" y="{yy(0)-6:.1f}" text-anchor="middle" style="font-size:10px;font-weight:600;fill:#A32D2D">rib {_i+1}</text>')
        a(f'<text x="{xx(_rx+1.375):.1f}" y="{yy(CW)+11:.1f}" text-anchor="middle" style="font-size:9px;fill:#A32D2D">{_rx:g}</text>')
    # round lights (Acegoo 12 V slim pucks, 2 3/4 in across, 1/2 in thick, 2 1/4 in hole, two spring clips: they clip into the plywood alone, so the slat is cut away 3 in at each): over the shower, the countertop and the sink on the slat at 58 across, and two in the center row at 34 across (2 in clear of the ribs)
    for lx,ly in LIGHTS:
        a(f'<circle cx="{xx(lx):.1f}" cy="{yy(ly):.1f}" r="{SC*LD/2:.1f}" fill="#FFE9A0" stroke="#B8860B" stroke-width="1.4"/>')
        a(f'<circle cx="{xx(lx):.1f}" cy="{yy(ly):.1f}" r="{SC*LH/2:.1f}" fill="none" stroke="#8A5A00" stroke-width="1" stroke-dasharray="3 2"/>')
    a(f'<text x="{xx(70):.1f}" y="{yy(58)-9:.1f}" text-anchor="middle" style="font-size:11px;font-weight:600;fill:#fff;paint-order:stroke;stroke:#5A3A00;stroke-width:3px">round lights, 2 3/4 in pucks in 2 1/4 in holes, each in a 3 in gap in its slat: shower, countertop and sink, and two in the center row</text>')
    # the six furring strips: under the ribs and above the plywood (so seen from above they are dashed over the slats); each is three pieces joined on the middle of rib 1 and rib 4
    for _i,(_id,_nm,_y0,_y1) in enumerate(RAILS):
        for p0,p1 in PIECES:
            a(f'<rect x="{xx(p0):.1f}" y="{yy(_y0):.1f}" width="{SC*(p1-p0):.1f}" height="{SC*(_y1-_y0):.1f}" fill="#3A1E05" fill-opacity="0.5" stroke="#3A1E05" stroke-width="1.1" stroke-dasharray="5 2"/>')
        a(f'<text x="{xx(142):.1f}" y="{(yy(_y0)-3 if _i else yy(_y1)+12):.1f}" text-anchor="middle" style="font-size:10px;font-weight:700;fill:#3A1E05;paint-order:stroke;stroke:#fff;stroke-width:2.6px">{_id}  1/2 x 2 1/2</text>')
    # cutouts
    # the units on the roof: fan 17 3/4 square, A/C 28 1/4 square, dashed around their cutouts
    for _c,_u in ((fan,17.75),(ac,28.25)):
        a(f'<rect x="{xx(_c[0]-_u/2):.1f}" y="{yy(_c[1]-_u/2):.1f}" width="{SC*_u:.1f}" height="{SC*_u:.1f}" fill="none" stroke="#185FA5" stroke-width="1.6" stroke-dasharray="7 4"/>')
    for (x0,x1,ya,yb),nm,sz in zip(cut,('roof fan','air conditioning'),('14 x 14','14 1/4 x 14 1/4')):
        a(f'<rect x="{xx(x0):.1f}" y="{yy(ya):.1f}" width="{SC*(x1-x0):.1f}" height="{SC*(yb-ya):.1f}" fill="#2C2C2A" fill-opacity="0.9" stroke="#000" stroke-width="1.4"/>')
        a(f'<text x="{xx((x0+x1)/2):.1f}" y="{yy((ya+yb)/2)-2:.1f}" text-anchor="middle" style="font-size:11px;font-weight:600;fill:#fff;paint-order:stroke;stroke:#2C2C2A;stroke-width:3px">{nm}</text><text x="{xx((x0+x1)/2):.1f}" y="{yy((ya+yb)/2)+12:.1f}" text-anchor="middle" style="font-size:10px;fill:#fff;paint-order:stroke;stroke:#2C2C2A;stroke-width:3px">{sz} cutout</text>')
    # outline, labels, dimensions
    a(f'<rect x="{xx(0):.1f}" y="{yy(0):.1f}" width="{SC*CL:.1f}" height="{SC*CW:.1f}" fill="none" stroke="#2C2C2A" stroke-width="1.8"/>')
    a(f'<text x="{xx(CL-2):.1f}" y="{yy(1.9):.1f}" text-anchor="end" style="font-size:9.5px;fill:#5F5E5A">62 in flat part, 3 in each side</text>')
    a(f'<line x1="{xx(0):.1f}" y1="{yy(CW)+18:.1f}" x2="{xx(CL):.1f}" y2="{yy(CW)+18:.1f}" stroke="#A32D2D" stroke-width="1.4" marker-start="url(#arg)" marker-end="url(#arg)"/>')
    a(f'<text x="{xx(CL/2):.1f}" y="{yy(CW)+34:.1f}" text-anchor="middle" style="font-size:12px;font-weight:500;fill:#A32D2D">160 in long, rear doors to cab wall</text>')
    a(f'<line x1="{xx(CL)+18:.1f}" y1="{yy(0):.1f}" x2="{xx(CL)+18:.1f}" y2="{yy(CW):.1f}" stroke="#A32D2D" stroke-width="1.4" marker-start="url(#arg)" marker-end="url(#arg)"/>')
    a(f'<text x="{xx(CL)+28:.1f}" y="{yy(CW/2)+4:.1f}" style="font-size:12px;font-weight:500;fill:#A32D2D">68</text>')
    for xt in range(0,161,20):
        a(f'<text x="{xx(xt):.1f}" y="{yy(CW)+54:.1f}" text-anchor="middle" style="font-size:11px;font-weight:700;fill:#185FA5">{xt}</text>')
    a(f'<text x="{xx(0)-6:.1f}" y="{yy(CW/2)+4:.1f}" text-anchor="end" style="font-size:11px;fill:#5F5E5A">rear</text><text x="{xx(CL/2):.1f}" y="{yy(0)-6:.1f}" text-anchor="middle" style="font-size:11px;fill:#5F5E5A">driver side wall</text><text x="{xx(CL/2):.1f}" y="{yy(CW)+72:.1f}" text-anchor="middle" style="font-size:11px;fill:#5F5E5A">passenger side wall (inches from the rear doors along the bottom)</text>')
    a('</svg>')
    return '\n'.join(o), cutn
_svg,_cutn=_g()
_rows=[('Plywood','3/16 in','3 sheets of 4 x 8 ft at least (69 sq ft of ceiling: 160 x 62), cut into six pieces: 59 3/4, 68 and 32 1/4 long, each 48 wide, and the same three 14 wide (the two seams across the van are on the middle of rib 3 and rib 5, 59 3/4 and 127 3/4 in from the rear doors, so the steel is under them; the long seam is 51 in across from the driver wall, over CB3; no seam crosses a light hole or an opening)','on the six furring strips under the ribs, screwed up into them about every 8 in (1/2 in pieces of plywood: 5/8 in screws with washers); about 37 lb'),
 ('Slats','3 wide x 3/4 thick x 160 long','15, with 1 in gaps (1 1/2 in left at each side of the 62 in flat part); each one is cut where the fan or the A/C opening crosses it: the fan cuts %d, the A/C cuts %d; and each light cuts a 3 in gap in its slat (4 gaps: two in the slat at 58 across, two in the slat at 34 across)'%(_cutn[0],_cutn[1]),'14 ft stock (8 in waste each); about 72 lb in western red cedar (about 23 lb per cubic foot, pine would be about 90); a board sold as 1 x 4 is 3/4 x 3 1/2, so rip it to 3 in wide'),
 ('Round lights','Acegoo 12 V slim pucks, 2 3/4 in across, 1/2 in thick, in 2 1/4 in holes; 4','over the shower (26 1/2 in from the rear doors) and one over the countertop and sink together (95 3/8), both on the slat at 58 in across from the driver wall, and two in the center row on the slat at 34 in across, at 35 7/8 (36 asked for) and 102 1/8 (around 100 asked for) from the rear doors; no other ceiling lights','centered on a 3 in slat and 2 in clear of the ribs (7/8 in from the hole to the rib edge); the slat is cut away 3 in at each light (the flange 2 3/4 plus 1/8 each side), so the puck clips into the 3/16 plywood alone: its two spring clips cannot reach behind the slat and plywood together (15/16 in); the hole is 2 1/4 in; the face sits about 5/8 in behind the slat faces; the shower one is wet rated; the two in the center row share one switch on the passenger wall just rear of the sink'),
 ('Ceiling furring strips','1/2 thick x 2 1/2 wide, six strips CB1 to CB6, 160 long, each in 3 pieces: 23 1/8, 75 5/8 and 61 1/4 (about 24 lb of 1/2 in plywood, 12 sticks of 8 ft, one 4 x 8 sheet ripped)','they run the whole length of the ceiling, lengthwise, centered across from the driver wall at 4 1/4 (CB1, the driver side trim, its edge on the plywood edge, 3 in from the wall), 14 (CB4), 24 1/4 (CB5, beside the openings), 43 5/8 (CB6, beside the openings), 51 (CB3, under the long plywood seam) and 63 3/4 (CB2, the passenger side trim, its edge on the plywood edge); they clear the fan and A/C frames and the light holes; the joints are on the middle of rib 1 (23 1/8) and rib 4 (98 3/4), so they never meet the plywood seams (the middle of rib 3 and rib 5)','under the bottoms of the steel ribs (so the finished ceiling is 1/2 in lower), each screwed to every rib it crosses with two self-drilling screws about 1 in apart (a piece joined on a rib: each piece takes its own half); the plywood is screwed to them about every 8 in, and the trim (CB1, CB2) is screwed up through the plywood into them; the cables run in the 2 in bays above them, so no gaps are needed'),
 ('Roof fan cutout','14 x 14','centered 13 1/4 in from the rear doors (7 1/4 on the datum of the other diagrams: it spans 6 1/4 to 20 1/4 from the rear doors, 1 1/2 in clear of the roof rib that starts at 21 3/4) and 34 in across from the driver wall, the middle of the van (not over the wet bath, as you decided); the fan unit is 17 3/4 square, so it sits on the roof from 4 3/8 to 22 1/8 from the rear doors','the F36AR fan cutout, 356 x 356 mm (14.02 in, drawn 14 x 14); framed between the roof bows'),
 ('Air conditioning cutout','14 1/4 x 14 1/4','centered 49 1/2 in from the rear doors (43 1/2 on the datum of the other diagrams: it spans 42 3/8 to 56 5/8 from the rear doors, inside the 40 to 70 asked for, between the roof ribs at 37 7/8 and 58 3/8) and 34 in across','the usual air conditioner opening; model not chosen; framed between the roof bows; its weight is not modeled')]
_pt=''.join('<tr><td>%d</td><td>%s to %s</td><td>%s</td></tr>'%(i+1,fr(p0),fr(p1),fr(p1-p0)) for i,(p0,p1) in enumerate(PIECES))
_cut='<h3>The ceiling furring strips: the pieces</h3><p>Each of the six strips, CB1 to CB6, is the same three pieces (18 in all) of 1/2 in material, 2 1/2 in wide, laid lengthwise under the ribs and joined on the middle of rib 1 and rib 4. The piece names are the strip and the number: CB1.1 to CB1.3, CB2.1 to CB2.3, and so on. Cut them 1/16 in short at each joint.</p><table><tr><th>Piece</th><th>From the rear doors</th><th>Length, in</th></tr>'+_pt+'</table><p>Twelve 8 ft sticks make the six strips: one stick for the 23 1/8 and the 61 1/4 pieces (84 3/8 in with the saw cut) and one for the 75 5/8 piece, for each strip. If you use 1/2 in plywood, one 4 x 8 ft sheet ripped to 2 1/2 in gives 19 sticks, so one sheet covers the 12 you need. Screw each piece to every rib it crosses with two self-drilling screws about 1 in apart, through the strip into the steel (about 1 in long). At a joint each piece takes its own half of the rib, its screws 3/4 in from the rib\'s middle. Each strip lies flat on the rib bottoms and tilts with the roof: near the walls the roof is an arc, up to 16 degrees across the strip, so do not try to keep it level: lay it against the rib bottoms, screw it there, and check it with a string line along its length before the plywood goes up.</p>'
_tbl='<table><tr><th>Part</th><th>Size</th><th>How many and where</th><th>Notes</th></tr>'+''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%r for r in _rows)+'</table>'+_cut
# H: the six plywood pieces, the order they go up, and where they are screwed (seen from above, like G)
def _hdiag():
    o=[]; a=o.append
    W=xx(CL)+90; H=yy(CW)+56
    a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img"><title>The six ceiling plywood pieces PW1 to PW6, the order they go up and where they are screwed</title>')
    a(f'<text x="{X0}" y="22" style="font-size:12px;fill:#5F5E5A">Seen from above, like G. The numbered circles are the order the pieces go up, rear doors to cab wall.</text>')
    PX=[0]+PLYX+[160]; PY=[3,51,65]
    tints=['#EAD9B0','#E0CB9B','#F0E1BD','#DFC995','#EBDAB5','#E2CE9F']
    pcs=[]
    for i in range(len(PX)-1):
        for j in range(2):
            n=i*2+j+1; pcs.append((n,PX[i],PX[i+1],PY[j],PY[j+1]))
    for n,x0,x1,y0,y1 in pcs:
        a(f'<rect x="{xx(x0):.1f}" y="{yy(y0):.1f}" width="{SC*(x1-x0):.1f}" height="{SC*(y1-y0):.1f}" fill="{tints[n-1]}" stroke="#8A6B4D" stroke-width="1.6"/>')
    # the roof ribs (steel) under the pieces, and the six furring strips
    for k,(r0,r1) in enumerate(RIBS):
        a(f'<rect x="{xx(r0):.1f}" y="{yy(0):.1f}" width="{SC*(r1-r0):.1f}" height="{SC*CW:.1f}" fill="#A32D2D" fill-opacity="0.13" stroke="#A32D2D" stroke-width="1.1" stroke-dasharray="6 3"/>')
        a(f'<text x="{xx((r0+r1)/2):.1f}" y="{yy(0)-6:.1f}" text-anchor="middle" style="font-size:10px;font-weight:600;fill:#A32D2D">rib {k+1}</text>')
    for _id,_nm,_y0,_y1 in RAILS:
        for p0,p1 in PIECES:
            a(f'<rect x="{xx(p0):.1f}" y="{yy(_y0):.1f}" width="{SC*(p1-p0):.1f}" height="{SC*(_y1-_y0):.1f}" fill="#3A1E05" fill-opacity="0.4" stroke="#3A1E05" stroke-width="1" stroke-dasharray="5 2"/>')
        a(f'<text x="{xx(113):.1f}" y="{(yy(_y0)-3 if _id!="CB1" else yy(_y1)+11):.1f}" text-anchor="middle" style="font-size:9.5px;font-weight:700;fill:#3A1E05;paint-order:stroke;stroke:#fff;stroke-width:2.4px">{_id}</text>')
    # the openings and light holes cut in the pieces on the floor
    for (cx_,cy_,w_,nm) in ((13.25,34,14,'fan 14 x 14'),(49.5,34,14.25,'A/C 14 1/4 sq')):
        a(f'<rect x="{xx(cx_-w_/2):.1f}" y="{yy(cy_-w_/2):.1f}" width="{SC*w_:.1f}" height="{SC*w_:.1f}" fill="#2C2C2A" fill-opacity="0.88" stroke="#000" stroke-width="1.2"/>')
        a(f'<text x="{xx(cx_):.1f}" y="{yy(cy_)+3:.1f}" text-anchor="middle" style="font-size:9.5px;font-weight:600;fill:#fff">{nm}</text>')
    for lx,ly in LIGHTS:
        a(f'<circle cx="{xx(lx):.1f}" cy="{yy(ly):.1f}" r="{SC*LH/2:.1f}" fill="#FFE9A0" stroke="#B8860B" stroke-width="1.4"/>')
    # the screws: the plywood is screwed up into the six strips every 8 in (not into the ribs: the strips are between); at CB3 each piece takes its own half of the strip
    dots=[]
    for _id,_nm,_y0,_y1 in RAILS:
        yc=(_y0+_y1)/2
        for p0,p1 in PIECES:
            xv=p0+3
            while xv<p1-1:
                if _id=='CB3': dots+= [(xv,yc-0.6),(xv,yc+0.6)]
                else: dots.append((xv,yc))
                xv+=8
    for xv,yv in dots:
        a(f'<circle cx="{xx(xv):.1f}" cy="{yy(yv):.1f}" r="1.5" fill="#1B1B1B"/>')
    # the numbered circles and piece labels
    for n,x0,x1,y0,y1 in pcs:
        bx_=x0+10; by_=(y0+7) if y1-y0>20 else (y0+4.4)
        a(f'<circle cx="{xx(bx_):.1f}" cy="{yy(by_):.1f}" r="10" fill="#185FA5" stroke="#fff" stroke-width="1.5"/>')
        a(f'<text x="{xx(bx_):.1f}" y="{yy(by_)+4.5:.1f}" text-anchor="middle" style="font-size:13px;font-weight:700;fill:#fff">{n}</text>')
        a(f'<text x="{xx(bx_)+16:.1f}" y="{yy(by_)+4:.1f}" style="font-size:11px;font-weight:700;fill:#2C2C2A;paint-order:stroke;stroke:#fff;stroke-width:2.6px">PW{n}  {fr(x1-x0)} x {fr(y1-y0)}</text>')
    a(f'<rect x="{xx(0):.1f}" y="{yy(0):.1f}" width="{SC*CL:.1f}" height="{SC*CW:.1f}" fill="none" stroke="#2C2C2A" stroke-width="1.8"/>')
    # seams
    a(f'<text x="{xx(PLYX[0]):.1f}" y="{yy(CW)+14:.1f}" text-anchor="middle" style="font-size:10px;font-weight:600;fill:#185FA5">seam on the middle of rib 3 ({fr(PLYX[0])})</text>')
    a(f'<text x="{xx(PLYX[1]):.1f}" y="{yy(CW)+14:.1f}" text-anchor="middle" style="font-size:10px;font-weight:600;fill:#185FA5">seam on the middle of rib 5 ({fr(PLYX[1])})</text>')
    a(f'<text x="{xx(CL)+6:.1f}" y="{yy(51)-1:.1f}" style="font-size:10px;font-weight:600;fill:#185FA5">long seam</text><text x="{xx(CL)+6:.1f}" y="{yy(51)+11:.1f}" style="font-size:10px;font-weight:600;fill:#185FA5">over CB3</text>')
    for xs in PLYX:
        a(f'<line x1="{xx(xs):.1f}" y1="{yy(0):.1f}" x2="{xx(xs):.1f}" y2="{yy(CW)+4:.1f}" stroke="#185FA5" stroke-width="1" stroke-dasharray="2 2"/>')
    # legend
    ly=yy(CW)+34
    a(f'<rect x="{X0}" y="{ly-9:.1f}" width="16" height="10" fill="#A32D2D" fill-opacity="0.13" stroke="#A32D2D" stroke-dasharray="4 2"/><text x="{X0+22}" y="{ly:.1f}" style="font-size:10.5px;fill:#2C2C2A">steel roof rib</text>')
    a(f'<rect x="{X0+120}" y="{ly-9:.1f}" width="16" height="10" fill="#3A1E05" fill-opacity="0.4" stroke="#3A1E05" stroke-dasharray="4 2"/><text x="{X0+142}" y="{ly:.1f}" style="font-size:10.5px;fill:#2C2C2A">furring strips CB1 to CB6</text>')
    a(f'<circle cx="{X0+330}" cy="{ly-4:.1f}" r="1.8" fill="#1B1B1B"/><text x="{X0+340}" y="{ly:.1f}" style="font-size:10.5px;fill:#2C2C2A">a screw, every 8 in</text>')
    a(f'<rect x="{X0+470}" y="{ly-9:.1f}" width="12" height="10" fill="#2C2C2A"/><text x="{X0+488}" y="{ly:.1f}" style="font-size:10.5px;fill:#2C2C2A">opening, cut in the piece first</text>')
    a(f'<circle cx="{X0+680}" cy="{ly-4:.1f}" r="5" fill="#FFE9A0" stroke="#B8860B"/><text x="{X0+690}" y="{ly:.1f}" style="font-size:10.5px;fill:#2C2C2A">light hole 2 1/4, cut first</text>')
    a('</svg>')
    return '\n'.join(o)
_hsvg=_hdiag()
def _rel(x,y,x0,y0): return fr(x-x0)+' along, '+fr(y-y0)+' across'
_hrows=[
 ('PW1','1','59 3/4 x 48','0 to 59 3/4 along, 3 to 51 across','fan 14 x 14 at '+_rel(13.25,34,0,3)+'; A/C 14 1/4 square at '+_rel(49.5,34,0,3)+'; light hole 2 1/4 at '+_rel(35.875,34,0,3)),
 ('PW2','2','59 3/4 x 14','0 to 59 3/4 along, 51 to 65 across','light hole 2 1/4 at '+_rel(26.5,58,0,51)),
 ('PW3','3','68 x 48','59 3/4 to 127 3/4 along, 3 to 51 across','light hole 2 1/4 at '+_rel(102.125,34,59.75,3)),
 ('PW4','4','68 x 14','59 3/4 to 127 3/4 along, 51 to 65 across','light hole 2 1/4 at '+_rel(95.375,58,59.75,51)),
 ('PW5','5','32 1/4 x 48','127 3/4 to 160 along, 3 to 51 across','none'),
 ('PW6','6','32 1/4 x 14','127 3/4 to 160 along, 51 to 65 across','none')]
_htab='<table><tr><th>Piece</th><th>Order</th><th>Size, in</th><th>Covers (from the rear doors, and across from the driver wall)</th><th>Cut in it first (measured from the piece\'s rear edge and its driver-side edge)</th></tr>'+''.join('<tr><td><b>%s</b></td><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%r for r in _hrows)+'</table>'
_hsteps="""<h3>How the pieces go up</h3>
<ol>
<li><b>Cut the six pieces from three 4 x 8 ft sheets.</b> Sheet 1: PW1 (59 3/4 x 48) and PW5 (32 1/4 x 48), 92 in with the saw cut. Sheet 2: PW3 (68 x 48). Sheet 3: ripped into 14 in strips, one strip for PW2 and PW6 (59 3/4 and 32 1/4) and one for PW4 (68). Number each piece on its back.</li>
<li><b>Cut the openings and the light holes on the floor</b>, from the table: PW1 has the fan and A/C openings, PW1 to PW4 each have one light hole. Check the two openings against the curbs you built (14 x 14 and 14 1/4 square inside).</li>
<li><b>Draw the screw lines on the room face of each piece</b>, because the strips will be hidden once it is up. The six strips, 2 1/2 in wide, run lengthwise at 4 1/4, 14, 24 1/4, 43 5/8, 51 and 63 3/4 in across from the driver wall (their centers). At CB3, under the long seam, each piece takes its own half of the strip: its screw line is 3/8 in from the seam.</li>
<li><b>Wool first, one bay at a time:</b> fill the bays under a piece with the wool just before that piece goes up (the wool goes in after the strips are on, and before the plywood; the space between the roof and the plywood is now 2 1/2 in: the 2 in of the ribs and the 1/2 in strips).</li>
<li><b>Lift PW1 first</b> (rear, driver side: the biggest, with the openings), with a helper and two props (2x4s cut to the ceiling height) in the middle. Push it flat against the strips, then start screwing at the middle and work outward, every 8 in along each strip: 5/8 in screws with washers (they go through the 3/16 in plywood and 7/16 in into the 1/2 in strip).</li>
<li><b>PW2 next</b> (the 14 in strip beside it): it butts PW1 over CB3 with a 1/16 in gap; each piece takes half of CB3. Then <b>PW3 and PW4</b> the same way, butting PW1 and PW2 at 59 3/4 in; then <b>PW5 and PW6</b> at 127 3/4 in. The strips run under every seam, so the plywood screws into a strip all along each edge.</li>
<li>Leave the 1/16 in gaps at every seam. Do not fill them: the slats, glued across, hold the seams flat.</li>
</ol>"""
_hblk='<h2>5. The ceiling plywood: the six pieces and how they go up (diagram H)</h2>\n<div class="wide">'+_hsvg+'</div>\n<p>PW1 to PW6 are the six pieces of 3/16 in plywood. The numbers are the order they go up, from the rear doors to the cab wall. The seams across the van are at 59 3/4 and 127 3/4 in (the middle of rib 3 and rib 5, kept from the earlier layout: the strips run lengthwise under both, so they could also go elsewhere); the long seam is over CB3.</p>\n'+_htab+'\n'+_hsteps+'\n'
_h=open((ROOT+'/sides.html')).read()
_blk='''<h2>4. The ceiling covering, seen from above (diagram G)</h2>
<div class="wide">'''+_svg+'''</div>
<p>The ceiling is built from six lengthwise furring strips, 1/2 in thick, screwed to the bottoms of the steel ribs, then 3/16 in plywood screwed to the strips, then 3/4 in thick, 3 in wide cedar slats glued on the plywood: so the finished ceiling is 1 7/16 in below the bottoms of the ribs, at 74 1/16 in (the ribs are 75 1/2 in up at the wall). Everything that reaches the ceiling stops at the new one: the closet and the wet bath are 74 1/16 in tall and the overhead cabinets top out there. The covering is the 62 in flat part of the roof, centered in the van (3 in each side of the 68 in inside width), so there are 15 slats. They run the whole length of the ceiling (160 in) for now, except where the fan and air conditioning openings cut them and at the four lights (each slat is cut away 3 in there, so the 2 3/4 in puck clips into the plywood alone). The six furring strips (the dashed brown lines, CB1 to CB6) run lengthwise under the ribs, above the plywood: CB1 and CB2 under the trim along the wall tops, CB3 under the long plywood seam, CB5 and CB6 on each side of the fan and air conditioning openings and CB4 between CB1 and CB5; each is three pieces joined on the middle of rib 1 and rib 4. The covering weighs about 133 lb (37 lb of plywood, 72 lb of cedar and about 24 lb of strips), all overhead. The five dashed red bands are the roof ribs, 2 3/4 in wide, drawn at the positions you measured (their edge nearest the rear doors: 21 3/4, 37 7/8, 58 3/8, 97 3/8 and 126 3/8 in); both openings sit between ribs, and the dashed blue squares are the fan unit (17 3/4 square) and the air conditioner unit (28 1/4 square) on the roof. Fan and air conditioner are both in the middle of the van, 34 in across. The wall diagrams B and E show the covering, the lights and the cutouts (their positions are 6 in less than the numbers here, because they are measured from the datum 6 in in from the rear edge), and the interactive page has a Ceiling view with the sizes.</p>
'''+_tbl+'\n'+_hblk
assert '<h2>Driver side photos</h2>' in _h
_h=_h.replace('<h2>Driver side photos</h2>',_blk+'<h2>Driver side photos</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
