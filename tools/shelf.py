# C4: the gear shelf over the battery, how to make it and how it pulls out.
# Three drawings in one: from the aisle with the face off (parts and the height stack), from above (stowed and pulled out 18 in),
# and a side section stowed and pulled out. All numbers come from shelfdata.py (the same formulas as layout() in ia_core.js).
INK='#2C2C2A'; AMB='#B45309'; BRN='#8A6B4D'; PLY='#E3C48F'; RED='#A32D2D'; BLU='#185FA5'; GRY='#9A9DA3'; PUR='#534AB7'
def _t(x,y,s,sz=10,col=INK,anchor='middle',w=400,extra=''):
    return f'<text class="ts" x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="font-size:{sz}px;font-weight:{w};fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px" {extra}>{s}</text>'
def _r(x,y,w,h,fill='none',stroke=INK,sw=1.2,dash='',fo=1):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{max(w,0):.1f}" height="{max(h,0):.1f}" fill="{fill}" fill-opacity="{fo}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
def _l(x1,y1,x2,y2,col=INK,sw=1.2,dash='',mk=''):
    d=f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d} {mk}/>'
_MK='marker-start="url(#c4a)" marker-end="url(#c4a)"'
_UNITS=[(DC,'DC-DC charger','16 x 9 x 4 1/2'),(INV,'Inverter','14 13/16 x 7 11/16 x 3 7/8'),(CHG,'Shore charger','9 1/2 x 7 x 4')]

def _front():
    S=12.0; OX=60; FLY=330
    X=lambda x: OX+S*(x-36); Z=lambda z: FLY-S*z
    o=[]; a=o.append
    a(_t(OX,26,'Seen from the aisle, the face and the lower panel off (the shelf stowed)',13,INK,'start',700))
    a(_l(X(36),Z(0),X(77),Z(0),INK,2.5))
    # wheel well behind, battery
    pts=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
    a('<polygon points="'+' '.join(f'{X(x):.1f},{Z(z):.1f}' for x,z in pts)+f'" fill="#D8B79A" fill-opacity=".6" stroke="{BRN}" stroke-width="1.2"/>')
    a(_r(X(BAT[0]),Z(9.5),S*(BAT[1]-BAT[0]),S*9.5,'#F2B84B',AMB,1.4,'4 3',.35)); a(_t(X(62.5),Z(4.4),'battery 21 x 10 x 9 1/2 (on the floor)',10,'#5A3A00'))
    # closet end panel and the divider
    a(_r(X(74),Z(19.5),S*2.4,S*19.5,GRY,INK,1.2,'',.55)); a(_t(X(75.2),Z(14.5),'closet',9.5,INK,'middle',400,f'transform="rotate(-90 {X(75.2):.1f} {Z(14.5):.1f})"'))
    a(_r(X(SH_DIV),Z(DECK_U),S*.75,S*DECK_U,PLY,INK,1.2,'',.9)); a(_t(X(SH_DIV)-3,Z(6),'divider, 3/4 ply',9.5,INK,'end'))
    # deck, leaf folded back
    a(_r(X(36),Z(DECK_T),S*(74-36),S*.75,BRN,'#3E230B',1,'',.9)); a(_t(X(36.3),Z(PLAT+1.0),f'deck {fr8(DECK_U)} to {fr8(DECK_T)} up, folded leaf to {fr8(PLAT)}',9.5,INK,'start'))
    a(_r(X(36),Z(PLAT),S*(74-36),S*.75,'#B07A2A','#5A3A00',1,'',.85))
    # slides: 1/2 in thick, 1 3/4 in tall, centered on the rails
    zc=SH_Z0+1.25
    a(_r(X(SH_DIV+.75),Z(zc+.875),S*.5,S*1.75,BLU,INK,1,'',.75))
    a(_r(X(SH_X1+.15),Z(zc+.875),S*.5,S*1.75,BLU,INK,1,'',.75))
    # tray: rails, plywood, gear
    a(_r(X(SH_X0),Z(SH_Z0+2.5),S*.75,S*2.5,PLY,INK,1.3,'',1)); a(_r(X(SH_X1-.75),Z(SH_Z0+2.5),S*.75,S*2.5,PLY,INK,1.3,'',1))
    a(_r(X(SH_X0+.75),Z(SH_Z1),S*(SH_X1-SH_X0-1.5),S*SH_T,PLY,INK,1.3,'',1))
    for u,nm,dm in (( INV,'Inverter','3 7/8 tall'),(DC,'DC-DC','4 1/2 tall')):
        a(_r(X(u['x0']),Z(SH_Z1+u['h']),S*(u['x1']-u['x0']),S*u['h'],'#F6C28B',AMB,1.6,'',.7)); a(_t(X((u['x0']+u['x1'])/2+(5 if u is DC else 0)),Z(SH_Z1+u['h']/2)+3,f'{nm}, {dm}',9.5,'#5A2A00','middle',700))
    a(_r(X(CHG['x0']),Z(SH_Z1+CHG['h']),S*(CHG['x1']-CHG['x0']),S*CHG['h'],'#F6C28B',AMB,1.8,'',.9)); a(_t(X((CHG['x0']+CHG['x1'])/2),Z(SH_Z1+CHG['h']/2)+3,'Shore 4 tall',9,'#5A2A00','middle',700))
    # lift-out rail
    a(_r(X(SH_X0-.5),Z(DECK_U),S*(SH_X1-SH_X0+1),S*1.5,'none',RED,1.4,'5 3',1)); a(_t(X(SH_X0+3),Z(PLAT+3.4),'front rail across the opening (lifts out)',9.5,RED,'start',700)); a(_l(X(SH_X0+3.5),Z(PLAT+3.0),X(SH_X0+3.5),Z(DECK_U-.2),RED,1,'3 2'))
    # slide and rail callouts
    a(_t(X(SH_DIV)-3,Z(zc)+3,'slide',9.5,BLU,'end',700)); a(_t(X(76.8),Z(zc)+3,'slide',9.5,BLU,'start',700))
    a(_t(X(SH_X0-.3),Z(SH_Z0)+14,'rail 3/4 x 2 1/2',9.5,INK,'start'))
    a(_t(X(55),Z(SH_Z1)+S*SH_T+13,'tray: 1/2 in ply',9.5,INK,'middle'))
    # the height stack, right of the closet
    sx=X(79); st=[(0,9.5,'battery 9 1/2'),(9.5,SH_Z0,f'gap {fr8(SH_G)}'),(SH_Z0,SH_Z1,'ply 1/2'),(SH_Z1,SH_Z1+4.5,'tallest unit 4 1/2'),(SH_Z1+4.5,DECK_U,f'air {fr8(AIR)}')]
    for (z0,z1,lab),dy in zip(st,(0,7,-3,0,0)):
        a(_l(sx,Z(z0),sx,Z(z1),RED,1.6)); a(_l(sx-4,Z(z1),sx+4,Z(z1),RED,1.2)); a(_t(sx+7,Z((z0+z1)/2)+3+dy,lab,9.5,RED,'start',700))
    a(_l(sx-4,Z(0),sx+4,Z(0),RED,1.2))
    a(_l(sx-14,Z(0),sx-14,Z(DECK_U),INK,1.6,'',_MK)); a(_t(sx-18,Z(DECK_U/2)+3,f'{fr8(DECK_U)} under the deck',10,INK,'end',700,f'transform="rotate(-90 {sx-18:.1f} {Z(DECK_U/2)+3:.1f})"'))
    return '\n'.join(o)

def _plan():
    S=8.0; OX=730; OY=60
    X=lambda x: OX+S*(x-36); Y=lambda y: OY+S*y
    o=[]; a=o.append
    a(_t(OX-4,26,'From above, driver wall at the top',13,INK,'start',700))
    a(_l(X(36),Y(0),X(77),Y(0),INK,4)); a(_t(X(37),Y(0)-6,'driver wall',9.5,INK,'start'))
    a(_r(X(42),Y(0),S*34,S*7,'#D8B79A',BRN,1.2,'',.7)); a(_t(X(59),Y(3.7),'wheel well',9.5,'#5A3A00'))
    a(_r(X(BAT[0]),Y(7),S*21,S*10,'#F2B84B',AMB,1.4,'4 3',.45)); a(_t(X(62.5),Y(15.6),'battery',9.5,'#5A3A00'))
    a(_r(X(74),Y(0),S*3,S*25,GRY,INK,1.2,'',.55)); a(_t(X(75.5),Y(12),'closet',9.5,INK,'middle',400,f'transform="rotate(-90 {X(75.5):.1f} {Y(12):.1f})"'))
    a(_r(X(SH_DIV),Y(0),S*.75,S*HATCH_Y,PLY,INK,1.2,'',.9)); a(_t(X(SH_DIV)-2,Y(4),'divider',9.5,INK,'end'))
    a(_l(X(36),Y(HATCH_Y+.75),X(74),Y(HATCH_Y+.75),PUR,1.4,'6 3')); a(_t(X(36.5),Y(HATCH_Y+.75)+11,'couch front',9.5,PUR,'start'))
    a(_r(X(36),Y(47),S*22,S*5,'#9FC5C0',INK,1.2,'',.6)); a(_t(X(47),Y(50),'fridge, 21 deep (47 out)',9.5,INK))
    def tray(off,solid):
        d='' if solid else '4 3'; fo=.9 if solid else .35
        a(_r(X(SH_X0),Y(SH_Y0+off),S*(SH_X1-SH_X0),S*(SH_Y1-SH_Y0),PLY,INK,1.4,d,fo))
        a(_r(X(SH_X0),Y(SH_Y0+off),S*.75,S*(SH_Y1-SH_Y0),'#C9A263',INK,1,d,.9)); a(_r(X(SH_X1-.75),Y(SH_Y0+off),S*.75,S*(SH_Y1-SH_Y0),'#C9A263',INK,1,d,.9))
        a(_r(X(SH_X0),Y(SH_Y1+off),S*(SH_X1-SH_X0),S*.75,'#7A5A2E',INK,1.2,d,.9))
        for u,nm in ((DC,'DC-DC'),(INV,'Inverter'),(CHG,'Charger')):
            a(_r(X(u['x0']),Y(u['y0']+off),S*(u['x1']-u['x0']),S*(u['y1']-u['y0']),'#F6C28B',AMB,1.5,d,.75 if solid else .4)); a(_t(X((u['x0']+u['x1'])/2),Y((u['y0']+u['y1'])/2+off)+3,nm,9.5,'#5A2A00','middle',700))
    tray(SH_PULL,False); tray(0,True)
    a(_t(X(55),Y(SH_Y1+SH_PULL+.75)+13,f'pulled out {SH_PULL} in: all of it in the aisle',10,RED,'middle',700))
    a(_l(X(79),Y(SH_Y1+.75),X(79),Y(SH_Y1+.75+SH_PULL),RED,1.6,'',_MK)); a(_t(X(79)+5,Y(SH_Y1+.75+SH_PULL/2)+3,f'{SH_PULL} in',10,RED,'start',700))
    a(_l(X(SH_X0-3),Y(SH_Y1+SH_PULL+.75),X(SH_X0-3),Y(47),BLU,1.4,'',_MK)); a(_t(X(SH_X0-4),Y((SH_Y1+SH_PULL+.75+47)/2)+3,'3 in',9.5,BLU,'end',700))
    return '\n'.join(o)

def _section(OX,off,label,ymax):
    S=11.0; FLY=745
    Y=lambda y: OX+S*y; Z=lambda z: FLY-S*z
    o=[]; a=o.append
    a(_t(OX,510,label,13,INK,'start',700))
    a(_l(Y(0),Z(0),Y(ymax),Z(0),INK,2.5)); a(_l(Y(0),Z(0),Y(0),Z(20),INK,4)); a(_t(Y(0)+4,Z(19.4),'wall',9.5,INK,'start'))
    a(_r(Y(0),Z(7.5),S*7,S*7.5,'#D8B79A',BRN,1.2,'',.7)); a(_t(Y(3.5),Z(3.2),'well',9.5,'#5A3A00'))
    a(_r(Y(7),Z(9.5),S*10,S*9.5,'#F2B84B',AMB,1.4,'4 3',.45)); a(_t(Y(12),Z(4.4),'battery',10,'#5A3A00'))
    # divider behind (dashed), couch parts
    a(_r(Y(0),Z(DECK_U),S*HATCH_Y,S*DECK_U,'none',BRN,1,'3 3',1))
    a(_r(Y(0),Z(DECK_T),S*26,S*.75,BRN,'#3E230B',1,'',.9)); a(_r(Y(6),Z(PLAT),S*20,S*.75,'#B07A2A','#5A3A00',1,'',.85)); a(_r(Y(0),Z(PLAT+2.4),S*26,S*2.4,PUR,PUR,1,'',.18)); a(_t(Y(13),Z(PLAT+1.5),'seat cushion',9.5,PUR))
    # lower panel (fixed), front rail (in or lifted out)
    a(_r(Y(HATCH_Y),Z(SH_Z0-.25),S*.75,S*(SH_Z0-.25),'#C9A263',INK,1.2,'',.9)); a(_t(Y(HATCH_Y+1.2),Z(3),'lower panel',9.5,INK,'start'))
    if off==0: a(_r(Y(HATCH_Y),Z(DECK_U),S*.75,S*1.5,'#C9A263',INK,1.2,'',.9)); a(_t(Y(HATCH_Y+1.2),Z(15.0)+3,'front rail',9.5,INK,'start'))
    else: a(_r(Y(HATCH_Y),Z(DECK_U),S*.75,S*1.5,'none',RED,1.2,'4 3',1)); a(_t(Y(HATCH_Y+1.2),Z(15.0)+3,'front rail lifted out',9.5,RED,'start',700))
    # slide: fixed member and moving member (edge-on)
    zc=SH_Z0+1.25
    a(_l(Y(7.5),Z(zc),Y(25.5),Z(zc),BLU,3)); a(_l(Y(SH_Y0+off-.25),Z(zc)-5,Y(SH_Y1+off+.1),Z(zc)-5,AMB,3))
    # tray
    a(_r(Y(SH_Y0+off),Z(SH_Z1),S*(SH_Y1-SH_Y0),S*SH_T,PLY,INK,1.3,'',1)); a(_r(Y(SH_Y0+off),Z(SH_Z1+.75),S*.75,S*.75,PLY,INK,1.1,'',1))
    a(_r(Y(SH_Y0+off),Z(SH_Z0+2.5),S*(SH_Y1-SH_Y0),S*2.5,'none',BRN,1,'3 3',1))
    a(_r(Y(SH_Y1+off),Z(14.5),S*.75,S*(14.5-SH_Z0+.25),'#7A5A2E',INK,1.2,'',.9))
    for u,nm in ((DC,'DC-DC + inverter'),(CHG,'charger')):
        a(_r(Y(u['y0']+off),Z(SH_Z1+u['h']),S*(u['y1']-u['y0']),S*u['h'],'#F6C28B',AMB,1.5,'',.75))
        a(_t(Y((u['y0']+u['y1'])/2+off),Z(SH_Z1+u['h']/2)+3,nm,9 if u is DC else 8.5,'#5A2A00','middle',700))
    a(_t(Y(SH_Y1+off+1.2),Z(11.9)+3,'face',9.5,INK,'start'))
    return '\n'.join(o)

def _c4_svg():
    W=1160; H=775
    o=[f'<svg viewBox="0 0 {W} {H}" role="img"><title>The gear shelf over the battery: parts, height stack and how it pulls out</title>']
    o.append('<defs><marker id="c4a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>')
    o.append(_front()); o.append(_plan())
    o.append(_section(50,0,'Side section, stowed',31))
    o.append(_section(450,SH_PULL,f'Side section, pulled out {SH_PULL} in (wall on the left, aisle on the right)',53))
    o.append('</svg>')
    return '\n'.join(o)

_PARTS=[
 ('1','Tray','1/2 in birch plywood',f'{fr16(SH_X1-SH_X0-1.5)} x {fr16(SH_Y1-SH_Y0)}','1','the floor of the shelf; the long way runs along the wall; saw it square (check the diagonals)'),
 ('2','End rails','3/4 x 2 1/2 in hardwood (a 1x3 on edge)',f'{fr16(SH_Y1-SH_Y0)} long','2','glue and screw to the tray ends (#8 x 1 1/4 every 3 in), bottoms flush with the tray; the slides screw to their outer faces'),
 ('3','Rear lip','3/4 x 3/4 in hardwood',f'{fr16(SH_X1-SH_X0-1.5)}','1','glued on top of the tray\'s rear edge between the rails; stops the units sliding back and stiffens the edge'),
 ('4','Face','3/4 in plywood, louvered (or a vented panel)',f'{fr16(SH_X1-SH_X0)} x 4 1/4','1','screwed through into the front ends of the rails and the tray edge; flush with the couch front; a 1 1/2 in pull handle or two finger holes; louvers for the fans'),
 ('5','Slides','full-extension, side mount, ball bearing, 18 in, 75 lb or more a pair','','1 pair (one slide each end)','the fixed member goes on the divider and on the closet end panel; the moving member on the rail face'),
 ('6','Divider','3/4 in plywood',f'{fr8(DECK_U)} x {fr8(HATCH_Y)}','1',f'stands on the floor from the wall to the couch front at {fr16(SH_DIV)} to {fr16(SH_DIV+.75)} in; screwed to a 3/4 x 3/4 cleat on the floor and one under the deck; west of the wheel well (42 in) and 4 in past the lawn chairs'),
 ('7','Lift-out front rail','3/4 x 1 1/2 in hardwood',f'{fr16(SH_X1-SH_X0+1)}','1','replaces the couch front rail across the opening (14 1/2 to 16 in up); rests in notches in the divider and the closet end panel and carries the front edge of the deck; lift it out before you pull the shelf'),
 ('8','Lower panel','3/4 in plywood, louvered',f'{fr8(SH_Z0-.25)} x {fr16(SH_X1-SH_X0+1)}','1','fills the couch front under the shelf; on turn buttons, so the battery is reachable'),
 ('9','Hardware','','','','screws #8 x 5/8 for the slides (about 24), #8 x 1 1/4 for the rails and the face, wood glue, #10 pan head screws and washers to hold each unit down through its mounting ears, cable clamps, adhesive-lined heat shrink, 4 turn buttons'),
]
_STEPS=[
 f'<b>Raise the couch first.</b> The base (two end panels, the wall ledger and the front rail) goes up 3 1/2 in: deck {fr8(DECK_U)} to {fr8(DECK_T)} up, the folded leaf on it to {fr8(PLAT)}, seat top {fr8(SEAT_T)}. The leg feet screw out another 3 1/2 in (diagram C3).',
 f'<b>Stand the divider.</b> Cut it 3/4 x {fr8(DECK_U)} x {fr8(HATCH_Y)}, clamp it plumb at {fr16(SH_DIV)} in from the back, and screw it to the floor cleat and the cleat under the deck; also check it is parallel to the closet end panel (74 in) within 1/16 in over its length, because the slides must run parallel.',
 f'<b>Mark the slide height with a story stick.</b> The tray bottom sits {fr8(SH_Z0)} in up (1 in over the battery top). Each slide is 1 3/4 in tall and centered on the rail, so its center is {fr8(SH_Z0+1.25)} in up and its top {fr8(SH_Z0+2.125)}. Screw the fixed members to the divider face and the closet end panel (with 5/8 in screws, so they do not come out through the 3/4 in plywood), their front ends flush with the couch front, both at the same height.',
 f'<b>Build the tray.</b> Cut the plywood and the two rails, glue and screw the rails to the ends of the tray with the bottoms flush, glue on the rear lip, and check the diagonals match to 1/16 in. The tray with its rails is {fr16(SH_X1-SH_X0)} wide, so it leaves {fr16(74-SH_X1)} in each side for a 1/2 in slide and about 1/8 in of clearance.',
 'Screw the moving members to the outer faces of the rails, with the tray upside down on a flat bench, then set the tray on the fixed members and push it home. If the slides bind, shim the divider end by 1/16 in or loosen the screws and re-seat the members; do not force them.',
 f'<b>Fit the face</b> to the front of the tray and the rails, flush with the couch front ({fr8(HATCH_Y)} to {fr8(HATCH_Y+.75)} in out from the wall), from 10 1/4 to 14 1/2 in up; the lift-out rail goes above it (14 1/2 to 16 in up) and the lower panel below it (floor to 10 1/4).',
 f'<b>Set the gear on the tray.</b> Rear row: the DC-DC charger at {fr16(DC["x0"])} to {fr16(DC["x1"])} in along the wall and the inverter at {fr16(INV["x0"])} to {fr16(INV["x1"])}; front row: the shore charger at {fr16(CHG["x0"])} to {fr16(CHG["x1"])}; 1/2 in between the units, 1/4 in from the rails and the face. Hold each down through its mounting ears (the 4 1/2 in DC-DC leaves {fr8(AIR)} in under the deck). Keep the inverter\'s fan sides and the louvers on the same side.',
 f'<b>Wire it with loops.</b> Every cable from the battery and the starter battery, the chargers\' AC inputs and the inverter\'s AC output runs over the rear lip to a U-shaped loop {SH_PULL+6} in longer than a fixed run (2/0 and 2 AWG cable bends about 4 in tight, so make the loop 8 in deep or more), tied down along the closet end panel and the tray rail with clamps so it cannot catch the slide. Fuses stay fixed on the battery side: the Class T within 7 in of the post.',
 'Test it: lift out the front rail, pull the face, watch the loops, check the shelf clears the fridge by 3 in, then push it home. Label the lift-out rail "LIFT OUT BEFORE PULLING THE SHELF". About 28 lb loaded: check the sag at full extension (it should be well under 1/8 in with the units on).']
def _c4_html():
    pt='<table><tr><th>#</th><th>Part</th><th>Material</th><th>Cut size (in)</th><th>Qty</th><th>Notes</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a,b,c,d,e,f in _PARTS)+'</table>'
    st='<ol>'+''.join(f'<li>{x}</li>' for x in _STEPS)+'</ol>'
    return ('<h3>Driver side: the gear shelf over the battery, how to make it</h3>\n<div class="wide">'+_c4_svg()+'</div>\n'
     f'<p>The inverter, the DC-DC charger and the shore charger all sit on one tray over the battery. The tray is 1/2 in plywood between two 3/4 x 2 1/2 in end rails, on two {SH_PULL} in full-extension slides: one on the closet\'s end panel (74 in from the back) and one on a plywood divider just west of the wheel well. Its louvered face is flush with the couch front, so you pull the face and the whole shelf comes out {SH_PULL} in into the aisle, with every unit and terminal open from above. The battery stays on the floor under it, with a 1 in gap for its terminals and lugs. The stack, from the floor: battery 9 1/2, gap 1, tray 1/2, the tallest unit (the DC-DC) 4 1/2, air {fr8(AIR)}, which is the {fr8(DECK_U)} in under the deck; that is why the couch was raised 3 1/2 in. The front rail of the couch lifts out across the opening, because the units are taller than the 1 1/2 in under it.</p>\n'
     '<p><b>Parts and cut list</b> (all sizes in inches; the same numbers as the interactive page, with the interactive page\'s 1/16 in rounding):</p>\n'+pt+
     '\n<p><b>How to build it, in order:</b></p>\n'+st+
     '\n<p><b>Not settled:</b> the exact slide model (check its thickness and height against the 1/2 in and 1 3/4 in drawn here), the battery\'s real terminal height (1 in of gap assumes right-angle lugs), the real weights of the two chargers (28 lb is a guess apart from the inverter\'s 7.7 lb), where the cables enter the closet end panel, and the front rail\'s support at its notches. The couch is now 3 1/2 in higher and the cushions are 5 in (they were 6): a seated 6 ft head is 1 1/2 in under the wall cabinets, tight but not touching.</p>\n')
_h=open((ROOT+'/sides.html')).read()
assert '<h2>2. Passenger side</h2>' in _h
_h=_h.replace('<h2>2. Passenger side</h2>',_c4_html()+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
