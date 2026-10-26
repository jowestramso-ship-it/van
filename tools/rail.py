# C5: the lift-out front rail across the gear shelf opening: a 3/4 x 1 1/2 in steel tube on two angle ledges, held by two screw-head pins.
# Uses the helpers of shelf.py (_t, _r, _l) and the numbers of shelfdata.py. The rail carries the deck's front edge over the 34 in opening;
# it lifts out because the units on the shelf (to 15 1/2 in up) are taller than the 1 1/2 in under the deck.
STL='#7C8088'; PIN_Y=(RAIL_Y0+RAIL_Y1)/2
def _front5():
    S=15.0
    X=lambda x: 50+S*(x-36); Z=lambda z: 118+S*(18-z)
    o=[]; a=o.append
    a(_t(50,26,'Seen from the aisle: the rail in place, the shelf stowed behind and under it',13,INK,'start',700))
    # couch end panel next to the closet, divider
    a(_r(X(GAP_E),Z(18),S*2,S*9,GRY,INK,1.2,'',.55)); a(_t(X(GAP_E+1),Z(13.5),'couch end panel',9.5,INK,'middle',400,f'transform="rotate(-90 {X(GAP_E+1):.1f} {Z(13.5):.1f})"'))
    a(_r(X(SH_DIV),Z(DECK_U),S*.75,S*(DECK_U-9),PLY,INK,1.2,'',.9)); a(_t(X(SH_DIV)-3,Z(12.5),'divider',9.5,INK,'end'))
    # deck, leaf folded back
    a(_r(X(36),Z(DECK_T),S*(GAP_E-36),S*.75,BRN,'#3E230B',1,'',.9)); a(_r(X(36),Z(PLAT),S*(GAP_E-36),S*.75,'#B07A2A','#5A3A00',1,'',.85))
    a(_t(X(36.3),Z(PLAT+.6)-1,f'deck {fr8(DECK_U)} to {fr8(DECK_T)} up, folded leaf above it',9.5,INK,'start'))
    # the shelf face
    a(_r(X(SH_X0),Z(FACE_Z1),S*(SH_X1-SH_X0),S*(FACE_Z1-FACE_Z0),PLY,INK,1.3,'',1))
    a(_r(X(55),Z(FACE_Z1-.6),S*6,S*.35,'#5A3A00',INK,1,'',.8))
    a(_t(X(57),Z(12.2)+4,'shelf face, 10 1/4 to 14 1/4 up',9.5,INK))
    # the units behind (dashed): they are taller than the rail's underside
    for u,nm in ((INV,'inverter'),(DC,'DC-DC'),(CHG,'charger')):
        a(_r(X(u['x0']),Z(SH_Z1+u['h']),S*(u['x1']-u['x0']),S*u['h'],'none',RED,1.2,'3 3',1))
    a(_t(X(56.7),Z(FACE_Z0)+22,'dashed red: the units behind the face, 14 7/8 to 15 1/2 in up: taller than the 14 1/2 in under the rail',9.5,RED,'middle',700))
    # ledges: an L whose horizontal leg is under the rail (top at 14 1/2) and whose vertical leg is screwed to the panel
    zb=RAIL_Z0-.125
    for x0,x1,vx in ((GAP_W,GAP_W+LEDGE,GAP_W),(GAP_E-LEDGE,GAP_E,GAP_E-.125)):
        a(_r(X(x0),Z(RAIL_Z0),S*(x1-x0),S*.125,STL,INK,1.2,'',1)); a(_r(X(vx),Z(zb+1.25),S*.125,S*1.25,STL,INK,1.2,'',1))
    # pins (screw heads) and the rail
    a(_r(X(GAP_W+.0625),Z(RAIL_Z1),S*RAIL_L,S*1.5,'#B9BCC2',INK,1.6,'',1))
    for px in (GAP_W+.8,GAP_E-.8):
        a(_r(X(px)-S*.165,Z(RAIL_Z0+.115),S*.33,S*.115,'#3E3E3A',INK,1,'',1))
    for x0 in (GAP_W+.0625,GAP_E-.0625-1):
        a(_r(X(x0),Z(RAIL_Z1-.075),S*1,S*1.35,'none','#8A5A00',1.2,'4 2',1))
    a(_t(X(60),Z(15.25)+4,f'steel tube 3/4 x 1 1/2, {fr8(RAIL_L)} long',10,INK,'middle',700))
    # marks A to F
    def tag(x,y,k): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'+_t(x,y+3.5,k,10,INK,'middle',700).replace('stroke-width:3px','stroke-width:0px')
    a(tag(X(46),Z(15.25),'A')); a(tag(X(GAP_W+.55),Z(15.25),'B')); a(tag(X(GAP_W+.8),Z(RAIL_Z0)+30,'C')); a(tag(X(GAP_W+LEDGE+1.0),Z(RAIL_Z0)+22,'D')); a(tag(X(GAP_E-.55),Z(15.25),'B'))
    # the gap dimensions
    a(_l(X(GAP_W),64,X(GAP_E),64,INK,1.4,'',_MK)); a(_t(X(56.7),58,f'{fr16(GAP_E-GAP_W)} between the divider and the end panel; the rail is {fr8(RAIL_L)}, 1/16 in short each end',10,INK,'middle',700))
    return '\n'.join(o)

def _states5():
    S=44.0
    o=[]; a=o.append
    def panel(ox,title,subs,lift,fwd):
        Y=lambda y: ox+S*(y-24); Z=lambda z: 380+S*(16.9-z)
        d=.125 if lift else 0                   # the rail and the deck's edge ride up 1/8 in
        yo=2.0 if fwd else 0
        a(_t(ox,296,title,12,INK,'start',700))
        for k,ln in enumerate(subs): a(_t(ox,312+k*12,ln,10,'#5A5851','start'))
        # deck (lifted with the rail only while it is on it) and the leaf
        dz=d if not fwd else 0
        a(_r(Y(24),Z(DECK_T+dz),S*2,S*.75,BRN,'#3E230B',1,'',.9)); a(_r(Y(24),Z(PLAT+dz),S*2,S*.75,'#B07A2A','#5A3A00',1,'',.85))
        # the shelf face
        a(_r(Y(RAIL_Y0),Z(FACE_Z1),S*.75,S*(FACE_Z1-13.4),PLY,INK,1.2,'',1))
        # the ledge: the cut passes through the pin, so we see its horizontal leg, the screw and the nut
        a(_r(Y(24.5),Z(RAIL_Z0),S*1.5,S*.125,STL,INK,1.2,'',1))
        a(_r(Y(PIN_Y)-S*.082,Z(RAIL_Z0),S*.164,S*.5,'#3E3E3A',INK,1,'',1)); a(_r(Y(PIN_Y)-S*.17,Z(RAIL_Z0-.125),S*.34,S*.17,'#3E3E3A',INK,1,'',1))
        a(_r(Y(PIN_Y)-S*.165,Z(RAIL_Z0+.115),S*.33,S*.115,'#3E3E3A',INK,1,'',1))
        # the rail: tube, plug, the hole
        ry0=RAIL_Y0+yo; rz=d if (lift or fwd) else 0
        a(_r(Y(ry0),Z(RAIL_Z1+rz),S*.75,S*1.5,'#B9BCC2',INK,1.6,'',1))
        a(_r(Y(ry0+.075),Z(RAIL_Z1-.075+rz),S*.6,S*1.35,'#E3C48F','#8A5A00',1,'',1))
        a(_r(Y(ry0+.375-.1875),Z(RAIL_Z0+.18+rz),S*.375,S*.18,'#fff','#8A5A00',1,'3 2',1))
        return Y,Z
    Y1,Z1=panel(40,'1  In place',('Sits on its two screw-head pins;','the deck rests on it.'),False,False)
    for zz,tx in ((15.55,'steel tube, 14 gauge'),(15.0,'hardwood plug (epoxied)'),(14.45,'3/8 hole, 3/16 deep in the plug'),(14.0,'ledge: steel angle'),(13.6,'screw head = pin, nut under it'),(13.2,'shelf face, top at 14 1/4')): a(_t(Y1(26.3),Z1(zz)+3,tx,9.5,INK,'start'))
    Y2,Z2=panel(300,'2  Lift 1/8 in',('The screw head clears the 3/16 in hole.','The deck only rests on it, so its','edge rises 1/8 in too.'),True,False)
    a(_r(Y2(RAIL_Y0),Z2(RAIL_Z1),S*.75,S*1.5,'none',RED,1.2,'3 3',1))
    a(_l(Y2(24.7),Z2(14.6),Y2(24.7),Z2(15.4),RED,2.2,'',_MK)); a(_t(Y2(24.7)-5,Z2(15.0)+3,'up 1/8 in',10,RED,'end',700))
    Y3,Z3=panel(560,'3  Pull it toward you',('Set it on the seat, then pull the','shelf by its face.'),False,True)
    a(_l(Y3(26.2),Z3(15.25),Y3(27.2),Z3(15.25),RED,2.2,'',_MK)); a(_t(Y3(26.7),Z3(15.25)-8,'toward the aisle',10,RED,'middle',700))
    return '\n'.join(o)

_PARTS5=[
 ('A','Rail','3/4 x 1 1/2 in steel rectangular tube, 14 gauge (0.075 in wall)',f'{fr8(RAIL_L)} long','1','about 3 lb; hacksaw or chop saw, deburr, prime and paint to match the couch front'),
 ('B','End plugs','hardwood, 5/8 x 1 5/16 in',f'1 in long','2','epoxied 1 in into each end of the tube, flush with the ends; the pin holes go in them'),
 ('C','Pins','#8-32 x 1/2 in pan head machine screws, with a nut and lock washer','','2','one in each ledge, head up (head 0.115 in tall, 0.33 in across), nut under the ledge'),
 ('D','Ledges','steel angle 1 1/4 x 1 1/4 x 1/8 in','2 in long','2','vertical leg screwed to the divider and to the couch end panel (#10 x 5/8 in screws, 3 each, plus construction adhesive); horizontal leg under the rail, its top at 14 1/2 in up'),
 ('E','Felt','1/16 in adhesive felt, 3/4 in wide',f'{fr8(RAIL_L)}','1','along the top of the tube if the deck does not touch it'),
]
_STEPS5=[
 f'<b>Measure first.</b> The divider and the couch end panel must both be 26 in deep and plumb, and the distance between the divider\'s east face and the end panel at the rail height should be {fr16(GAP_E-GAP_W)} in. If it is not, cut the tube 1/8 in shorter than what you measure (1/16 in each end).',
 f'<b>Cut and finish the tube</b> to {fr8(RAIL_L)} in, deburr both ends and prime it. A wood rail would sag about 1/4 in over this span with two adults on the front edge (rough hand calculation, 175 lb on the front); this tube sags about 0.04 in and weighs about 3 lb.',
 f'<b>Plug the ends.</b> Cut two hardwood plugs 5/8 x 1 5/16 x 1 in (a snug fit in the 0.6 x 1.35 in opening), epoxy them in 1 in, flush with the ends, and let the epoxy cure.',
 f'<b>Drill the pin holes.</b> From the bottom, 0.8 in in from each end and centered front to back, drill a 3/8 in hole up through the tube wall and 3/16 in into the plug (a drill-press stop or tape on the bit).',
 f'<b>Fit the ledges.</b> Drill a 3/16 in hole through the middle of each angle\'s horizontal leg, 0.8 in out from the vertical leg, and bolt the pin screw through it, head up, nut underneath. Clamp each ledge so the top of its horizontal leg is {fr8(RAIL_Z0)} in up, with the vertical leg flat on the panel and its front edge flush with the couch front ({fr8(RAIL_Y1)} in out); screw it on with three #10 x 5/8 in screws (5/8 in so they stop short of the other face of the 3/4 in plywood) and a bead of adhesive. The units on the shelf start 0.4 in past the end of the west ledge, so check that the ledge does not touch the shore charger.',
 f'<b>Drop the rail on.</b> Set it over the two screw heads. It should sit level with 1/16 in at each end and the deck resting on its top; if there is a gap under the deck, stick the felt on the top of the tube, and if it is tight, file the underside of the deck edge or the top of the tube (not the pin holes).',
 '<b>To use it:</b> push the rail up 1/8 in (the deck edge rises with it), pull it toward you off the pins, set it on the seat, and pull the shelf by its face. To put it back, push the shelf home first, then set the rail on the pins and let it down. Sit on the front edge of the couch only with the rail in; with it out, the deck edge is held up only by the plywood.',
 'Add a latch or a turn button on the shelf face (not on the rail) before driving, so the shelf cannot slide out on a hard stop; the rail itself stays put because the deck rests on it and the pins hold it forward and back.']
def _c5_html():
    pt='<table><tr><th>Mark</th><th>Part</th><th>Material</th><th>Size</th><th>Qty</th><th>Notes</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a,b,c,d,e,f in _PARTS5)+'</table>'
    st='<ol>'+''.join(f'<li>{x}</li>' for x in _STEPS5)+'</ol>'
    svg=['<svg viewBox="0 0 1000 560" role="img"><title>The lift-out front rail: parts, the ledges and how it comes out</title>','<defs><marker id="c4a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',_front5(),_states5(),'</svg>']
    return ('<h3>Driver side: the lift-out front rail, how to make it</h3>\n<div class="wide">'+'\n'.join(svg)+'</div>\n'
     f'<p>The units on the gear shelf are 14 7/8 to 15 1/2 in tall once they stand on the tray, and the couch\'s front rail has only 14 1/2 in under it, so across the {fr16(GAP_E-GAP_W)} in opening between the divider and the couch end panel the rail has to come out whenever the shelf is pulled. It still has to carry the deck\'s front edge when it is in (two adults sitting on that edge), so it is a 3/4 x 1 1/2 in steel tube, not a wood rail: 1 1/2 in is all the height there is, and wood that size would sag about 1/4 in. It rests on two small angle ledges, held forward and back by two screw heads that fit holes in its end plugs, and the deck rests on top of it. It lifts out 1/8 in and comes toward you.</p>\n'
     '<p><b>Parts</b> (marks A to D are on the drawing, E is the felt):</p>\n'+pt+'\n<p><b>How to build it, in order:</b></p>\n'+st+
     '\n<p><b>Not settled:</b> the couch end panel next to the closet is 26 in deep only if you make it so (the closet itself is 25 in deep, so its side panel needs a 1 in strip on the front edge, or the couch needs its own end panel there); the tube\'s real wall thickness (14 gauge is 0.075 in; 11 gauge is 0.12 in, which is heavier and stiffer); whether the deck edge needs a stiffener on the leaf side; and a latch for the shelf face.</p>\n')
_h=open((ROOT+'/sides.html')).read()
assert '<h2>2. Passenger side</h2>' in _h
_h=_h.replace('<h2>2. Passenger side</h2>',_c5_html()+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
