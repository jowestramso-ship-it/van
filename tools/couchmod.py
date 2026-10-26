# C5: the removable couch: a frame (back rail on three wall blocks, front rail, end rail, cross rail, two posts) and a separate deck lid, over the gear cabinet.
# Uses the helpers of shelf.py (_t, _r, _l, colors, _MK) and the numbers of shelfdata.py. Three drawings: from the aisle, a section through a wall block, and from above.
BLKC='#5A2E0A'; RAILC='#C9A263'; GRN='#2F5E3F'
def _tag5(x,y,k): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'+_t(x,y+3.5,k,10,INK,'middle',700).replace('stroke-width:3px','stroke-width:0px')
def _aisle5():
    S=11.5; OX=40; FLY=300
    X=lambda x: OX+S*x; Z=lambda z: FLY-S*z
    o=[]; a=o.append
    a(_t(OX,24,'1  Seen from the aisle: the frame (grey), the wall blocks (dark) and the cabinet panels, deck lid shown over them',13,INK,'start',700))
    a(_l(X(-1),Z(0),X(80),Z(0),INK,2.5))
    # wheel well, battery, chairs (dashed)
    pts=[(42,0),(76,0),(76,2),(66.75,7.5),(51.25,7.5),(42,2)]
    a('<polygon points="'+' '.join(f'{X(x):.1f},{Z(z):.1f}' for x,z in pts)+f'" fill="#D8B79A" fill-opacity=".45" stroke="{BRN}" stroke-width="1" stroke-dasharray="4 3"/>')
    a(_r(X(BAT[0]),Z(9.5),S*(BAT[1]-BAT[0]),S*9.5,'#F2B84B',AMB,1.2,'4 3',.3))
    a(_r(X(0),Z(5.625),S*34.5,S*5.625,'#7FB08F',GRN,1.2,'4 3',.35)); a(_t(X(17),Z(2.8)+3,'lawn chairs (slide in between the posts)',9.5,GRN))
    # cabinet panels and the shelf behind the lid
    for px in (CB_X0,CB_X1): a(_r(X(px),Z(CB_H),S*CB_T,S*CB_H,PLY,INK,1.2,'',.9))
    a(_r(X(SH_X0),Z(SH_Z1),S*(SH_X1-SH_X0),S*SH_T,PLY,INK,1.1,'',.9))
    for u in (DC,INV): a(_r(X(u['x0']),Z(SH_Z1+u['h']),S*(u['x1']-u['x0']),S*u['h'],'#F6C28B',AMB,1.2,'3 2',.55))
    a(_t(X((CB_X0+CB_X1)/2),Z(5.5),'gear cabinet: the shelf slides out of the front',10,'#5A3A00','middle',700))
    # the frame: back rail (dashed, behind), front rail, posts
    a(_r(X(0),Z(DECK_U),S*C0,S*BR_H,'none',INK,1.1,'5 3',1))
    a(_r(X(0),Z(DECK_U),S*SH_DIV,S*BR_H,'#B9BCC2',INK,1.4,'',.9))
    for px in POST_X: a(_r(X(px),Z(BR_Z0),S*POST,S*BR_Z0,'#B9BCC2',INK,1.4,'',.9))
    a(_t(X(SH_DIV/2),Z(14.25)+3,'front rail 3/4 x 3 1/2 on edge',10,INK,'middle',700))
    a(_t(X(55.5),Z(14.25)+3,'back rail behind (dashed), 74 long',10,INK,'middle',700))
    # the deck lid on top
    a(_r(X(0),Z(DECK_T),S*C0,S*.75,BRN,'#3E230B',1,'',.95)); a(_t(X(1),Z(DECK_T)-4,f'deck lid {fr8(DECK_U)} to {fr8(DECK_T)} up (the leaf folds onto it)',9.5,INK,'start'))
    # dowels in the panel tops
    for px in (CB_X0+CB_T/2,CB_X1+CB_T/2): a(_r(X(px)-S*.19,Z(DECK_U+.5),S*.38,S*1,'#C9A263',INK,1,'',1))
    # wall blocks
    for bx in BLK_X:
        a(_r(X(bx-BLK_W/2),Z(BLK_Z1),S*BLK_W,S*BLK_H,BLKC,'#fff',1,'',.95))
        a(_t(X(bx),Z(0)+22,f'{bx:g} in'+(' (if needed)' if bx==20 else ''),9.5,BLKC,'middle',700))
    a(_r(X(CB_X0+CB_T),Z(DECK_U),S*(C0-CB_X0-CB_T),S*BR_H,'none',INK,1.6,''))   # the back rail, doubled over the cabinet, on a ledger at each panel
    for lx in (CB_X0+CB_T,C0-.75): a(_r(X(lx),Z(BR_Z0),S*.75,S*LEDGE_H,'#C9A263',INK,1.1,'',1))
    a(_tag5(X(3),Z(14.25),'1')); a(_tag5(X(CB_X0-1.5),Z(8.5),'2'))
    a(_t(X(CB_X0+1),Z(20.5),'tops of the panels carry the lid; 2 dowels in each',9.5,INK,'start'))
    a(_l(X(CB_X0+5),Z(20.1),X(CB_X0+CB_T/2),Z(DECK_U+1.4),INK,1,'3 2'))
    return '\n'.join(o)
def _section5():
    S=14.0; OX=60; FLY=700
    Y=lambda y: OX+S*y; Z=lambda z: FLY-S*z
    o=[]; a=o.append
    a(_t(OX-10,376,'2  Section at a wall block (wall on the left, aisle on the right)',13,INK,'start',700))
    a(_l(Y(-1),Z(0),Y(28),Z(0),INK,2.5)); a(_l(Y(0),Z(0),Y(0),Z(22),INK,4)); a(_t(Y(0.4),Z(21.4),'wall (finished face)',9.5,INK,'start'))
    # furring strip S2 behind the planks
    a(_r(Y(-1.5),Z(12.75),S*1.5,S*1.5,'#7A4A1E','#3E230B',1.1,'',.9)); a(_t(Y(-1.7),Z(12.0)+3,'S2',9,'#3E230B','end'))
    a(_r(Y(-1.5),Z(3.75),S*1.5,S*1.5,'#7A4A1E','#3E230B',1.1,'',.9)); a(_t(Y(-1.7),Z(3.0)+3,'S1',9,'#3E230B','end'))
    # block, rail, deck, cushion
    a(_r(Y(0),Z(BLK_Z1),S*BLK_D,S*BLK_H,BLKC,'#fff',1,'',.95)); a(_t(Y(BLK_D+.3),Z(7.0)+3,'wall block: a 2x2 post standing on the floor',9.5,BLKC,'start',700))
    a(_r(Y(0),Z(DECK_U),S*.75,S*BR_H,RAILC,INK,1.3,'',1)); a(_t(Y(1.2),Z(14.9)+3,'back rail',9.5,INK,'start',700))
    a(_r(Y(0),Z(DECK_T),S*26,S*.75,BRN,'#3E230B',1,'',.95)); a(_r(Y(6),Z(PLAT),S*20,S*.75,'#B07A2A','#5A3A00',1,'',.85)); a(_r(Y(0),Z(SEAT_T),S*26,S*CUSH,PUR,PUR,1,'',.16))
    a(_t(Y(13),Z(PLAT+2.5)+3,'seat cushion',9.5,PUR,'middle'))
    # the screws: the wall screws (horizontal, through the block and the planks into S2) and the rail screws (down through the top edge into the block)
    for zz in (12.0,3.0): a(_l(Y(BLK_D+.6),Z(zz),Y(-1.2),Z(zz),RED,2.2))
    a(_t(Y(BLK_D+.8),Z(11.0)-5,'2 screws #8 x 3 into S2',9.5,RED,'start',700)); a(_t(Y(BLK_D+.8),Z(3.0)-5,'2 screws #8 x 3 into S1',9.5,RED,'start',700))
    a(_l(Y(.375),Z(DECK_U),Y(.375),Z(BLK_Z1-1.0),RED,2.2)); a(_t(Y(1.2),Z(13.4)+3,'4 1/2 in screws, down from the top (lid off)',9.5,RED,'start',700))
    # front rail west of the cabinet
    a(_r(Y(CB_Y1-.75),Z(DECK_U),S*.75,S*BR_H,RAILC,INK,1.1,'',.6)); a(_t(Y(CB_Y1-.75),Z(DECK_U-BR_H)+13,'front rail',9.5,INK,'end'))
    a(_l(Y(0),Z(0)+12,Y(BLK_D),Z(0)+12,INK,1.2,'',_MK)); a(_t(Y(0.8),Z(0)+24,'1 1/2',9.5,INK,'middle',700))
    a(_t(Y(CB_Y1)+4,Z(10.2),'west of the cabinet only,',9.5,INK,'end')); a(_t(Y(CB_Y1)+4,Z(10.2)+11,'none across the cabinet',9.5,INK,'end'))
    return '\n'.join(o)
def _plan5():
    S=6.5; OX=470; OY=410
    X=lambda x: OX+S*x; Y=lambda y: OY+S*y
    o=[]; a=o.append
    a(_t(OX,376,'3  From above, driver wall at the top (deck lid off)',13,INK,'start',700))
    a(_l(X(-1),Y(0),X(80),Y(0),INK,4))
    a(_r(X(42),Y(0),S*34,S*7,'#D8B79A',BRN,1.1,'',.6)); a(_r(X(BAT[0]),Y(7),S*21,S*10,'#F2B84B',AMB,1.2,'4 3',.35))
    a(_r(X(0),Y(2),S*34.5,S*21,'#7FB08F',GRN,1.2,'4 3',.2)); a(_t(X(17),Y(13),'lawn chairs',9.5,GRN))
    # panels, shelf
    for px in (CB_X0,CB_X1): a(_r(X(px),Y(0),S*CB_T,S*CB_Y1,PLY,INK,1.2,'',.95))
    a(_r(X(SH_X0),Y(SH_Y0),S*(SH_X1-SH_X0),S*(SH_Y1-SH_Y0),PLY,INK,1.1,'',.5))
    # frame: back rail (full length), end rail, cross rail, front rail, posts
    a(_r(X(0),Y(0),S*C0,S*.75,RAILC,INK,1.2,'',.95)); a(_r(X(0),Y(0),S*.75,S*CB_Y1,RAILC,INK,1.2,'',.95)); a(_r(X(SH_DIV/2),Y(0),S*.75,S*CB_Y1,RAILC,INK,1.2,'',.95)); a(_r(X(0),Y(CB_Y1-.75),S*SH_DIV,S*.75,RAILC,INK,1.2,'',.95))
    for px in POST_X: a(_r(X(px),Y(CB_Y1-POST),S*POST,S*POST,'#B9BCC2',INK,1.4,'',1))
    for bx in BLK_X: a(_r(X(bx-BLK_W/2),Y(0),S*BLK_W,S*BLK_D,BLKC,'#fff',1,'',.95))
    a(_t(X(SH_DIV/2+4),Y(CB_Y1)+14,'frame: back, end, cross and front rails; 2 posts',9.5,INK,'middle',700))
    a(_t(X(42),Y(CB_Y1)+14,'cabinet panels',9.5,'#5A3A00','start',700))
    a(_l(X(0),Y(CB_Y1)+30,X(3),Y(CB_Y1)+30,BLKC,1,'',_MK)); a(_t(X(3)+4,Y(CB_Y1)+34,'blocks at 3, 20 (if needed) and 41 in from the back mark',9.5,BLKC,'start',700))
    return '\n'.join(o)
_PARTS5=[
 ('1','Back rail','3/4 x 3 1/2 in hardwood or 3/4 in plywood ripped to 3 1/2',f'{fr8(C0)} long','1','full length, 12 1/2 to 16 in up, against the wall on the wall blocks; over the cabinet it lies behind the shelf (the shelf starts 7 3/4 in out from the wall)'),
 ('1b','Back beam (doubler) and ledgers','a second 3/4 x 3 1/2 in rail glued to the front of the back rail; two 3/4 x 1 1/2 x 3 in hardwood ledgers',f'{fr16(CB_X1-CB_X0-CB_T)} long (the beam)','1 and 2','over the cabinet only (between the panels, 39 3/8 to 74 in) the rail is 1 1/2 in thick, with each end resting on a ledger screwed to the inner face of its panel (top at 12 1/2 in up); this holds the back of the lid there, 34 5/8 in between the panels'),
 ('2','Front rail','3/4 x 3 1/2 in, on edge',f'{fr16(SH_DIV)} long','1','under the deck\'s front edge from the west end to the west panel; no rail crosses the cabinet (the units are taller than the 1 1/2 in under the deck would leave)'),
 ('3','End rail and cross rail','3/4 x 3 1/2 in, on edge',f'{fr16(CB_Y1-1.5)} long','2',f'at the west end (x = 0) and in the middle (about {fr8(SH_DIV/2)} in from the back), between the back and front rails; glue and two #8 x 2 1/2 in screws at each end (or pocket screws)'),
 ('4','Posts','1 1/2 x 1 1/2 in hardwood',f'{fr8(BR_Z0-1)} long','2',f'at the front corners (0 and {fr16(POST_X[1])} in from the back), glued and screwed to the inside of the front rail; each with a T-nut and a 1/4-20 leveling foot that adds about 1 in (so the post and foot reach the floor from the rail underside at 12 1/2 in up) and screws out a little more to level; only two, so the 34 1/2 in lawn chairs still slide in between them'),
 ('5','Wall blocks (posts)','2x2 (1 1/2 x 1 1/2 in actual), 12 1/2 in long','1 1/2 x 1 1/2 x 12 1/2','3 (the middle one if needed)','stand on the floor against the wall at 3, 20 and 41 in from the back mark (centers), tops at the rail\'s underside (12 1/2 in up): they carry the back of the couch to the floor; two #8 x 3 in screws through each and the planks into S1 (3 up) and two into S2 (12 up) hold them upright; the one at 41 is 40 1/4 to 41 3/4 in, clear of the west panel (39 3/8) and the wheel well (42); the lawn chairs sit 1 1/2 in off the wall to clear them'),
 ('6','Rail screws','1/4 x 4 1/2 in structural screws (or #10 x 4 in)','','6','two per block, down through the top edge of the back rail into the block, with 3/16 in pilot holes and the deck lid off (the top of a 2x2 is end grain, so a T-nut and a 1/4-20 bolt is better if you can reach it); these hold the frame to the posts and stop it lifting'),
 ('7','Deck lid','3/4 in plywood, 74 x 26 (with its leaf and hinge, diagrams C2 and C3)','74 x 26','1','rests on the rails and on the tops of the two panels (a 3/8 in dowel in each panel top fits a hole in the lid\'s underside); screwed down to the back, front and end rails from above (#8 x 1 1/4 in every 8 in), so the lid and the frame come apart in two lifts'),
 ('8','Dowels','3/8 x 1 in','','4','two in the top of each cabinet panel, glued in, 1/2 in standing proud'),
]
_STEPS5=[
 '<b>Make the three blocks.</b> Cut a 2x2 into three 12 1/2 in posts (a stop block on the saw keeps them identical; the floor is level but check each post is square), and seal them. The one at 20 in is the one you said "maybe, if needed": cut it, but fit it only if the frame feels springy.',
 f'<b>Mark them on the wall.</b> Centers at {BLK_X[0]}, {BLK_X[1]} and {BLK_X[2]} in from the back mark; each stands on the finished floor and its top must be {fr8(BLK_Z1)} in up, so shim under any that comes up short and plane or trim any that is long: the back rail rests on all three tops. The strips S1 (3 up) and S2 (12 up) sit behind the planks, so each post has two screws into each.',
 '<b>Screw each block on:</b> a bead of construction adhesive on its back, then two #8 x 3 in screws into S1 and two into S2 through the 3/8 in planks (pilot holes). The posts stand on the floor, so the strips only keep them upright and stop the couch sliding sideways; the strips are glued to the steel only at their dots (S2: 15, 30 3/4, 40), but that is enough for that job.',
 f'<b>Build the frame on the bench:</b> the back rail ({fr8(C0)} long), the front rail ({fr16(SH_DIV)}), the end rail and the cross rail ({fr16(CB_Y1-1.5)}), all 3/4 x 3 1/2 on edge, glued and screwed into a ladder, with the tops flush; glue the doubler ({fr16(CB_X1-CB_X0-CB_T)} long) to the front of the back rail over the cabinet. Check the diagonal of the west rectangle. Glue and screw the two posts to the front rail\'s inside face, fit the T-nuts and feet, and screw the feet in so each post and foot is about 12 1/2 in to start.',
 '<b>Screw the two ledgers</b> (3/4 x 1 1/2 x 3 in, tops at 12 1/2 in up) to the inner faces of the cabinet panels at the wall end, one on each. <b>Lift the frame in:</b> the back rail goes onto the three blocks, the front posts on the floor, and the ends of the doubled part rest on the two ledgers. Adjust the two feet until the tops of the rails are level (use a level on the front rail and a straightedge from the front rail over the west panel top to the east panel top); the panel tops are at 16 in, and so are the rails.',
 '<b>Screw the rail down</b> to each block, two 1/4 x 4 1/2 in structural screws through its top edge (3/16 in pilot holes, 1 in into the block). Do not fix the frame to the cabinet or the floor: the back stands on the three wall posts, the front on its two posts, and the ends of the doubled part on the two ledgers.',
 '<b>Set the deck lid</b> on the frame and on the panel dowels and screw it to the rails from above. Pull the gear shelf out and push it home: it must clear the lid by 1 3/4 in at the face. Then put a person on the front edge of the lid over the cabinet (34 5/8 in unsupported between the panels) before the cushions go on; if it sags, a stiff front beam that lifts out is the fix (the rail that was dropped), because anything fixed under the deck there is in the way of the units.',
 '<b>To take the couch out:</b> cushions and leaf off, the lid\'s screws out and the lid lifted off (about 45 lb, two people), then the six rail screws, and the frame lifts off the blocks (about 40 lb). Everything else, the cabinet, the shelf and the battery, stays.',
]
def _c5_html():
    pt='<table><tr><th>#</th><th>Part</th><th>Material</th><th>Size (in)</th><th>Qty</th><th>Notes</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a,b,c,d,e,f in _PARTS5)+'</table>'
    st='<ol>'+''.join(f'<li>{x}</li>' for x in _STEPS5)+'</ol>'
    svg=['<svg viewBox="0 0 1000 740" role="img"><title>The removable couch: the frame, the wall blocks, the deck lid and the gear cabinet</title>','<defs><marker id="c4a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',_aisle5(),_section5(),_plan5(),'</svg>']
    return ('<h3>Driver side: the removable couch (frame, wall blocks and deck lid), how to make it</h3>\n<div class="wide">'+'\n'.join(svg)+'</div>\n'
     f'<p>The couch is a separate piece that sits over the gear cabinet (diagram C4) and lifts out in two lifts. <b>The frame</b> has a full-length back rail ({fr8(C0)} in, 3/4 x 3 1/2 on edge) that rests on three wall blocks, which are 2x2 posts standing on the floor against the wall at {BLK_X[0]}, {BLK_X[1]} (if needed) and {BLK_X[2]} in from the back mark, and is screwed down into them from above; west of the cabinet (0 to {fr16(SH_DIV)} in) a front rail, an end rail and a cross rail make a ladder carried at the front by two posts with screw-out feet, with the lawn chairs between them. <b>What holds it up:</b> at the back the three wall posts, at the front the two front posts west of the cabinet, and over the cabinet the two panels, with the back rail doubled and resting on a ledger on each panel; the wall itself carries none of the weight. Over the cabinet there is no front rail: the front edge of the deck is free, because the units on the shelf are taller than the room under a rail. <b>The deck lid</b> (3/4 in plywood, 74 x 26, with the leaf and cushions of diagrams C, C2 and C3) sits on the frame and on two dowels in each panel top and is screwed to the rails from above. Nothing is fixed to the floor except the cabinet, and nothing is fixed to the cabinet except by its dowels.</p>\n'
     '<p><b>Parts</b> (the numbers 1 and 2 on the drawing are the wall blocks and the cabinet panels):</p>\n'+pt+'\n<p><b>How to build it, in order:</b></p>\n'+st+
     '\n<p><b>Not settled:</b> the deck\'s front edge over the cabinet (34 5/8 in with nothing under it: test it, and keep the old lift-out rail in mind as the fix), whether the block at 3 in has an S2 attachment dot behind it, the weight of the whole couch (about 85 lb with the cushions is an estimate), and how the rail screws find solid wood in the blocks (use a drill stop and pilot holes).</p>\n')
_h=open((ROOT+'/sides.html')).read()
assert '<h2>2. Passenger side</h2>' in _h
_h=_h.replace('<h2>2. Passenger side</h2>',_c5_html()+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
