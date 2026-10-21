# G: the ceiling covering seen from above through the roof: plywood pieces, slats, round lights on the slats, the shower fan and air conditioning cutouts
# physical positions from the rear doors (the datum used on the other diagrams is 6 in in from the rear edge)
SC=5; X0=70; Y0=46
CL=160; CW=68
xx=lambda x: X0+SC*x
yy=lambda y: Y0+SC*y
def _g():
    o=[]; a=o.append
    W=xx(CL)+90; H=yy(CW)+86
    a(f'<svg viewBox="0 0 {W:.0f} {H:.0f}" role="img"><title>The ceiling covering from above: plywood, slats, lights, fan and air conditioning cutouts</title>')
    a('<defs><marker id="arg" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    a(f'<text x="{X0}" y="26" style="font-size:12px;fill:#5F5E5A">Seen from above through the roof: rear doors on the left, cab wall on the right, driver side at the top. Measured from the rear doors.</text>')
    # plywood: 4 x 8 ft sheets, long way along the van, in four pieces
    cx=[0,96,160]; cy=[0,48,68]
    for i in range(2):
        for j in range(2):
            a(f'<rect x="{xx(cx[i]):.1f}" y="{yy(cy[j]):.1f}" width="{SC*(cx[i+1]-cx[i]):.1f}" height="{SC*(cy[j+1]-cy[j]):.1f}" fill="#D9C7A5" fill-opacity="0.8" stroke="#8A6B4D" stroke-width="1.2"/>')
    # slats: 17 rows of 3 in with 1 in gaps (1/2 in left each side), cut where the openings cross them
    fan=(13.25,46,14); ac=(49.5,34,14.25)
    cut=[(c[0]-c[2]/2,c[0]+c[2]/2,c[1]-c[2]/2,c[1]+c[2]/2) for c in (fan,ac)]
    ys=[0.5+4*k for k in range(17)]
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
    # round lights, mounted on the slats nearest the rows at 22 and 46 across
    for ly in (22,46):
        for lx in (26.67,80,133.33):
            a(f'<circle cx="{xx(lx):.1f}" cy="{yy(ly):.1f}" r="{SC*1:.1f}" fill="#FFE9A0" stroke="#B8860B" stroke-width="1.4"/>')
    a(f'<text x="{xx(80):.1f}" y="{yy(22)-9:.1f}" text-anchor="middle" style="font-size:11px;font-weight:600;fill:#fff;paint-order:stroke;stroke:#5A3A00;stroke-width:3px">round lights, 2 in, on the slats</text>')
    # cutouts
    for (x0,x1,ya,yb),nm,sz in zip(cut,('shower fan','air conditioning'),('14 x 14','14 1/4 x 14 1/4')):
        a(f'<rect x="{xx(x0):.1f}" y="{yy(ya):.1f}" width="{SC*(x1-x0):.1f}" height="{SC*(yb-ya):.1f}" fill="#2C2C2A" fill-opacity="0.9" stroke="#000" stroke-width="1.4"/>')
        a(f'<text x="{xx((x0+x1)/2):.1f}" y="{yy((ya+yb)/2)-2:.1f}" text-anchor="middle" style="font-size:11px;font-weight:600;fill:#fff">{nm}</text><text x="{xx((x0+x1)/2):.1f}" y="{yy((ya+yb)/2)+12:.1f}" text-anchor="middle" style="font-size:10px;fill:#fff">{sz} cutout</text>')
    # outline, labels, dimensions
    a(f'<rect x="{xx(0):.1f}" y="{yy(0):.1f}" width="{SC*CL:.1f}" height="{SC*CW:.1f}" fill="none" stroke="#2C2C2A" stroke-width="1.8"/>')
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
_rows=[('Plywood','1/4 in','3 sheets of 4 x 8 ft at least (76 sq ft of ceiling), cut into pieces 96 x 48, 64 x 48, 96 x 20 and 64 x 20','against the roof bows; about 54 lb'),
 ('Slats','3 wide x 1 thick x 160 long','17, with 1 in gaps (1/2 in left at each side); each one is cut where the fan or the A/C opening crosses it: the fan cuts %d, the A/C cuts %d'%(_cutn[0],_cutn[1]),'14 ft stock (8 in waste each); about 109 lb in western red cedar (about 23 lb per cubic foot, pine would be about 132); a board sold as 1 x 3 is only 3/4 x 2 1/2, so this is milled or 5/4 stock'),
 ('Round lights','2 in across, 6','two rows of three, at 26 2/3, 80 and 133 1/3 in from the rear doors, on the slats nearest 22 and 46 in across from the driver wall','centered on a 3 in slat (1/2 in of wood each side); a small hole through the plywood behind each for the wire'),
 ('Shower fan cutout','14 x 14','centered 13 1/4 in from the rear doors (7 1/4 on the datum of the other diagrams: it spans 6 1/4 to 20 1/4 from the rear doors, 1 1/2 in clear of the roof rib that starts at 21 3/4) and 46 in across from the driver wall (its center is over the wet bath; the opening runs 39 to 53 across, 5 in of it past the pan front edge at 44)','the F36AR fan cutout, 356 x 356 mm (14.02 in, drawn 14 x 14); framed between the roof bows'),
 ('Air conditioning cutout','14 1/4 x 14 1/4','centered 49 1/2 in from the rear doors (43 1/2 on the datum of the other diagrams: it spans 42 3/8 to 56 5/8 from the rear doors, inside the 40 to 70 asked for, between the roof ribs at 37 7/8 and 58 3/8) and 34 in across','the usual air conditioner opening; model not chosen; framed between the roof bows; its weight is not modeled')]
_tbl='<table><tr><th>Part</th><th>Size</th><th>How many and where</th><th>Notes</th></tr>'+''.join('<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>'%r for r in _rows)+'</table>'
_h=open((ROOT+'/sides.html')).read()
_blk='''<h2>4. The ceiling covering, seen from above (diagram G)</h2>
<div class="wide">'''+_svg+'''</div>
<p>The ceiling is covered with 1/8 in plywood against the roof and 1 in thick, 3 in wide cedar slats on it, so the finished ceiling is 1 1/8 in lower, at 74 7/8 in (the bare ceiling is 76 in). Everything that reached the ceiling stops at the new one: the wall cabinets are 13 7/8 in tall (61 to 74 7/8) and the closet and the wet bath are 74 7/8 in. The slats run the whole length of the ceiling (160 in) for now, except where the fan and air conditioning openings cut them. The covering weighs about 190 lb, all overhead. The 68 in width is the widest interior width: the roof curves in at the sides, so the real flat width has to be measured. The wall diagrams B and E show the covering, the lights and the cutouts (their positions are 6 in less than the numbers here, because they are measured from the datum 6 in in from the rear edge), and the interactive page has a Ceiling view with the sizes.</p>
'''+_tbl+'\n'
assert '<h2>Driver side photos</h2>' in _h
_h=_h.replace('<h2>Driver side photos</h2>',_blk+'<h2>Driver side photos</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
