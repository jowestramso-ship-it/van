# G: the ceiling covering seen from above through the roof: plywood pieces, slats, round lights on the slats, the roof ribs, the roof fan and air conditioning cutouts
# physical positions from the rear doors (the datum used on the other diagrams is 6 in in from the rear edge)
SC=5; X0=70; Y0=46
CL=160; CW=68
xx=lambda x: X0+SC*x
yy=lambda y: Y0+SC*y
def _g():
    o=[]; a=o.append
    W=xx(CL)+90; H=yy(CW)+86
    a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img"><title>The ceiling covering from above: plywood, slats, lights, roof ribs, fan and air conditioning cutouts</title>')
    a('<defs><marker id="arg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    a(f'<text x="{X0}" y="26" style="font-size:12px;fill:#5F5E5A">Seen from above through the roof: rear doors on the left, cab wall on the right, driver side at the top. Measured from the rear doors.</text>')
    # plywood: 4 x 8 ft sheets, long way along the van, in four pieces
    cx=[0,96,160]; cy=[3,51,65]
    for i in range(2):
        for j in range(2):
            a(f'<rect x="{xx(cx[i]):.1f}" y="{yy(cy[j]):.1f}" width="{SC*(cx[i+1]-cx[i]):.1f}" height="{SC*(cy[j+1]-cy[j]):.1f}" fill="#D9C7A5" fill-opacity="0.8" stroke="#8A6B4D" stroke-width="1.2"/>')
    # slats: 15 rows of 3 in with 1 in gaps (1 1/2 in left each side of the 62 in flat part), cut where the openings cross them
    fan=(13.25,34,14); ac=(49.5,34,14.25)
    cut=[(c[0]-c[2]/2,c[0]+c[2]/2,c[1]-c[2]/2,c[1]+c[2]/2) for c in (fan,ac)]
    ys=[4.5+4*k for k in range(15)]
    cutn=[0,0]
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
        for p0,p1 in parts:
            a(f'<rect x="{xx(p0):.1f}" y="{yy(y0):.1f}" width="{SC*(p1-p0):.1f}" height="{SC*3:.1f}" fill="#9A6B3A" fill-opacity="0.9" stroke="#5A3A00" stroke-width="0.8"/>')
    # the five roof ribs (their edge nearest the rear doors), dashed, over the covering
    for _i,_rx in enumerate((21.75,37.875,58.375,97.375,126.375)):
        a(f'<rect x="{xx(_rx):.1f}" y="{yy(0):.1f}" width="{SC*2.75:.1f}" height="{SC*CW:.1f}" fill="#A32D2D" fill-opacity="0.14" stroke="#A32D2D" stroke-width="1.2" stroke-dasharray="6 3"/>')
        a(f'<text x="{xx(_rx+1.375):.1f}" y="{yy(0)-6:.1f}" text-anchor="middle" style="font-size:10px;font-weight:600;fill:#A32D2D">rib {_i+1}</text>')
        a(f'<text x="{xx(_rx+1.375):.1f}" y="{yy(CW)+11:.1f}" text-anchor="middle" style="font-size:9px;fill:#A32D2D">{_rx:g}</text>')
    # round lights, only over the shower, the countertop and the sink, on the slat at 58 across (2 in clear of the ribs)
    for lx in (26.5,86.5,119):
        a(f'<circle cx="{xx(lx):.1f}" cy="{yy(58):.1f}" r="{SC*1:.1f}" fill="#FFE9A0" stroke="#B8860B" stroke-width="1.4"/>')
    a(f'<text x="{xx(86.5):.1f}" y="{yy(58)-9:.1f}" text-anchor="middle" style="font-size:11px;font-weight:600;fill:#fff;paint-order:stroke;stroke:#5A3A00;stroke-width:3px">round lights, 2 in: shower, countertop, sink</text>')
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
_rows=[('Plywood','3/16 in','3 sheets of 4 x 8 ft at least (69 sq ft of ceiling: 160 x 62), cut into pieces 96 x 48, 64 x 48, 96 x 14 and 64 x 14','against the roof bows; about 37 lb'),
 ('Slats','3 wide x 3/4 thick x 160 long','15, with 1 in gaps (1 1/2 in left at each side of the 62 in flat part); each one is cut where the fan or the A/C opening crosses it: the fan cuts %d, the A/C cuts %d'%(_cutn[0],_cutn[1]),'14 ft stock (8 in waste each); about 72 lb in western red cedar (about 23 lb per cubic foot, pine would be about 90); a board sold as 1 x 4 is 3/4 x 3 1/2, so rip it to 3 in wide'),
 ('Round lights','2 in across, 3','over the shower (26 1/2 in from the rear doors), the countertop (86 1/2) and the sink (119), all on the slat at 58 in across from the driver wall; no other ceiling lights','centered on a 3 in slat (1/2 in of wood each side) and 2 in clear of the ribs; a small hole through the plywood behind each for the wire; the shower one is wet rated'),
 ('Roof fan cutout','14 x 14','centered 13 1/4 in from the rear doors (7 1/4 on the datum of the other diagrams: it spans 6 1/4 to 20 1/4 from the rear doors, 1 1/2 in clear of the roof rib that starts at 21 3/4) and 34 in across from the driver wall, the middle of the van (not over the wet bath, as you decided); the fan unit is 17 3/4 square, so it sits on the roof from 4 3/8 to 22 1/8 from the rear doors','the F36AR fan cutout, 356 x 356 mm (14.02 in, drawn 14 x 14); framed between the roof bows'),
 ('Air conditioning cutout','14 1/4 x 14 1/4','centered 49 1/2 in from the rear doors (43 1/2 on the datum of the other diagrams: it spans 42 3/8 to 56 5/8 from the rear doors, inside the 40 to 70 asked for, between the roof ribs at 37 7/8 and 58 3/8) and 34 in across','the usual air conditioner opening; model not chosen; framed between the roof bows; its weight is not modeled')]
_tbl='<table><tr><th>Part</th><th>Size</th><th>How many and where</th><th>Notes</th></tr>'+''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%r for r in _rows)+'</table>'
_h=open((ROOT+'/sides.html')).read()
_blk='''<h2>4. The ceiling covering, seen from above (diagram G)</h2>
<div class="wide">'''+_svg+'''</div>
<p>The ceiling is covered with 3/16 in plywood against the roof and 3/4 in thick, 3 in wide cedar slats on it, so the finished ceiling is 15/16 in lower, at 75 1/16 in (the bare ceiling is 76 in). Everything that reached the ceiling stops at the new one: the wall cabinets are 14 1/16 in tall (61 to 75 1/16) and the closet and the wet bath are 75 1/16 in. The covering is the 62 in flat part of the roof, centered in the van (3 in each side of the 68 in inside width), so there are 15 slats. They run the whole length of the ceiling (160 in) for now, except where the fan and air conditioning openings cut them. The covering weighs about 109 lb (37 lb of plywood and 72 lb of cedar), all overhead. The five dashed red bands are the roof ribs, 2 3/4 in wide, drawn at the positions you measured (their edge nearest the rear doors: 21 3/4, 37 7/8, 58 3/8, 97 3/8 and 126 3/8 in); both openings sit between ribs, and the dashed blue squares are the fan unit (17 3/4 square) and the air conditioner unit (28 1/4 square) on the roof. Fan and air conditioner are both in the middle of the van, 34 in across. The wall diagrams B and E show the covering, the lights and the cutouts (their positions are 6 in less than the numbers here, because they are measured from the datum 6 in in from the rear edge), and the interactive page has a Ceiling view with the sizes.</p>
'''+_tbl+'\n'
assert '<h2>Driver side photos</h2>' in _h
_h=_h.replace('<h2>Driver side photos</h2>',_blk+'<h2>Driver side photos</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
