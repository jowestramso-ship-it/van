# C5: the removable couch: a frame (back rail on three wall blocks, front rail, end rail, cross rail, two posts) and a separate deck, over the gear cabinet.
# Uses the helpers of shelf.py (_t, _r, _l, colors, _MK) and the numbers of shelfdata.py. Three drawings: from the aisle, a section through a wall block, and from above.
BLKC='#5A2E0A'; RAILC='#C9A263'; GRN='#2F5E3F'
def _tag5(x,y,k): return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="8" fill="#fff" stroke="{INK}" stroke-width="1.2"/>'+_t(x,y+3.5,k,10,INK,'middle',700).replace('stroke-width:3px','stroke-width:0px')
def _aisle5():
    S=11.5; OX=40; FLY=300
    X=lambda x: OX+S*x; Z=lambda z: FLY-S*z
    o=[]; a=o.append
    a(_t(OX,24,'1  Seen from the aisle: the frame (grey), the wall blocks (dark) and the cabinet panels, deck shown over it',13,INK,'start',700))
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
    a(_t(X(SH_DIV/2),Z(BR_Z0+BR_H/2)+3,'front rail 3/4 x 3 1/2 on edge',10,INK,'middle',700))
    a(_t(X(55.5),Z(BR_Z0+BR_H/2)+3,'back rail behind (dashed), 74 long',10,INK,'middle',700))
    # the deck on top
    a(_r(X(0),Z(DECK_T),S*C0,S*.75,BRN,'#3E230B',1,'',.95)); a(_t(X(1),Z(DECK_T)-4,f'deck {fr8(DECK_U)} to {fr8(DECK_T)} up (the leaf folds onto it)',9.5,INK,'start'))
    # dowels in the panel tops
    for px in (CB_X0+CB_T/2,CB_X1+CB_T/2): a(_r(X(px)-S*.19,Z(DECK_U+.5),S*.38,S*1,'#C9A263',INK,1,'',1))
    # wall blocks
    for bx in BLK_X:
        a(_r(X(bx-BLK_W/2),Z(BLK_Z1),S*BLK_W,S*BLK_H,BLKC,'#fff',1,'',.95))
        a(_t(X(bx),Z(0)+22,f'{bx:g} in'+(' (if needed)' if bx==20 else ''),9.5,BLKC,'middle',700))
    a(_r(X(CB_X0+CB_T),Z(DECK_U),S*(C0-CB_X0-CB_T),S*BR_H,'none',INK,1.6,''))   # the back rail, doubled over the cabinet, on a ledger at each panel
    for lx in (CB_X0+CB_T,C0-.75): a(_r(X(lx),Z(BR_Z0),S*.75,S*LEDGE_H,'#C9A263',INK,1.1,'',1))
    a(_tag5(X(3),Z(BR_Z0+BR_H/2),'1')); a(_tag5(X(CB_X0-1.5),Z(8.5),'2'))
    a(_t(X(CB_X0+1),Z(DECK_T)-22,'tops of the panels carry the deck; 2 dowels in each',9.5,INK,'start'))
    a(_l(X(CB_X0+5),Z(DECK_T)-18.5,X(CB_X0+CB_T/2),Z(DECK_U+1.4),INK,1,'3 2'))
    # the front rail across the cabinet, glued under the deck edge (hardwood, 3/4 x 1)
    a(_r(X(RL_X0),Z(RL_Z1),S*(RL_X1-RL_X0),S*RL_H,RAILC,INK,1.5,'',1))
    a(_t(X(58),Z(DECK_T)-40,'front rail across the cabinet: 3/4 x 1, glued under the deck edge',9.5,INK,'middle',700))
    a(_l(X(58),Z(DECK_T)-36,X(58),Z(RL_Z0+.5),INK,1,'3 2'))
    return '\n'.join(o)
def _section5():
    S=14.0; OX=60; FLY=712
    Y=lambda y: OX+S*y; Z=lambda z: FLY-S*z
    o=[]; a=o.append
    a(_t(OX-10,376,'2  Section at a wall block (wall on the left, aisle on the right)',13,INK,'start',700))
    a(_l(Y(-1),Z(0),Y(28),Z(0),INK,2.5)); a(_l(Y(0),Z(0),Y(0),Z(24),INK,4)); a(_t(Y(0.4),Z(21.4),'wall (finished face)',9.5,INK,'start'))
    # furring strip S2 behind the planks
    a(_r(Y(-1.5),Z(12.75),S*1.5,S*1.5,'#7A4A1E','#3E230B',1.1,'',.9)); a(_t(Y(-1.7),Z(12.0)+3,'S2',9,'#3E230B','end'))
    a(_r(Y(-1.5),Z(3.75),S*1.5,S*1.5,'#7A4A1E','#3E230B',1.1,'',.9)); a(_t(Y(-1.7),Z(3.0)+3,'S1',9,'#3E230B','end'))
    # block, rail, deck, cushion
    a(_r(Y(0),Z(BLK_Z1),S*BLK_D,S*BLK_H,BLKC,'#fff',1,'',.95)); a(_t(Y(BLK_D+.3),Z(7.0)+3,'wall block: a 2x2 post standing on the floor',9.5,BLKC,'start',700))
    a(_r(Y(0),Z(DECK_U),S*.75,S*BR_H,RAILC,INK,1.3,'',1)); a(_t(Y(1.2),Z(BR_Z0+BR_H*.75)+3,'back rail',9.5,INK,'start',700))
    a(_r(Y(0),Z(DECK_T),S*26,S*.75,BRN,'#3E230B',1,'',.95)); a(_r(Y(6),Z(PLAT),S*20,S*.75,'#B07A2A','#5A3A00',1,'',.85)); a(_r(Y(0),Z(SEAT_T),S*26,S*CUSH,PUR,PUR,1,'',.16))
    a(_t(Y(13),Z(PLAT+2.5)+3,'seat cushion',9.5,PUR,'middle'))
    # the screws: the wall screws (horizontal, through the block and the planks into S2) and the rail screws (down through the top edge into the block)
    for zz in (12.0,3.0): a(_l(Y(BLK_D+.6),Z(zz),Y(-1.2),Z(zz),RED,2.2))
    a(_t(Y(BLK_D+.8),Z(11.0)-5,'2 screws #8 x 3 into S2',9.5,RED,'start',700)); a(_t(Y(BLK_D+.8),Z(3.0)-5,'2 screws #8 x 3 into S1',9.5,RED,'start',700))
    a(_l(Y(.375),Z(DECK_U),Y(.375),Z(BLK_Z1-1.0),RED,2.2)); a(_t(Y(1.2),Z(BR_Z0+.9)+3,'dowel in the post top: nothing is screwed',9.5,RED,'start',700))
    # front rail west of the cabinet
    a(_r(Y(CB_Y1-.75),Z(DECK_U),S*.75,S*BR_H,RAILC,INK,1.1,'',.6)); a(_t(Y(CB_Y1-.75),Z(DECK_U-BR_H)+13,'front rail',9.5,INK,'end'))
    a(_l(Y(0),Z(0)+12,Y(BLK_D),Z(0)+12,INK,1.2,'',_MK)); a(_t(Y(0.8),Z(0)+24,'1 1/2',9.5,INK,'middle',700))
    a(_r(Y(CB_Y1-.75),Z(RL_Z1),S*RL_T,S*RL_H,RAILC,'#5A3A00',1.6,'',1))
    a(_t(Y(CB_Y1)+4,Z(10.2),'3 1/2 tall west of the cabinet;',9.5,INK,'end')); a(_t(Y(CB_Y1)+4,Z(10.2)+11,'over the cabinet only the 1 in (solid)',9.5,INK,'end'))
    return '\n'.join(o)
def _plan5():
    S=6.5; OX=470; OY=410
    X=lambda x: OX+S*x; Y=lambda y: OY+S*y
    o=[]; a=o.append
    a(_t(OX,376,'3  From above, driver wall at the top (deck off)',13,INK,'start',700))
    a(_l(X(-1),Y(0),X(80),Y(0),INK,4))
    a(_r(X(42),Y(0),S*34,S*7,'#D8B79A',BRN,1.1,'',.6)); a(_r(X(BAT[0]),Y(7),S*21,S*10,'#F2B84B',AMB,1.2,'4 3',.35))
    a(_r(X(0),Y(2),S*34.5,S*21,'#7FB08F',GRN,1.2,'4 3',.2)); a(_t(X(17),Y(13),'lawn chairs',9.5,GRN))
    # panels, shelf
    for px in (CB_X0,CB_X1): a(_r(X(px),Y(0),S*CB_T,S*CB_Y1,PLY,INK,1.2,'',.95))
    a(_r(X(SH_X0),Y(SH_Y0),S*(SH_X1-SH_X0),S*(SH_Y1-SH_Y0),PLY,INK,1.1,'',.5))
    # frame: back rail (full length), end rail, cross rail, front rail, posts
    a(_r(X(0),Y(0),S*C0,S*.75,RAILC,INK,1.2,'',.95)); a(_r(X(0),Y(0),S*.75,S*CB_Y1,RAILC,INK,1.2,'',.95)); a(_r(X(SH_DIV/2),Y(0),S*.75,S*CB_Y1,RAILC,INK,1.2,'',.95)); a(_r(X(0),Y(CB_Y1-.75),S*SH_DIV,S*.75,RAILC,INK,1.2,'',.95)); a(_r(X(RL_X0),Y(RL_Y0),S*(RL_X1-RL_X0),S*RL_T,RAILC,'#5A3A00',1.6,'',.95))
    for px in POST_X: a(_r(X(px),Y(CB_Y1-POST),S*POST,S*POST,'#B9BCC2',INK,1.4,'',1))
    for bx in BLK_X: a(_r(X(bx-BLK_W/2),Y(0),S*BLK_W,S*BLK_D,BLKC,'#fff',1,'',.95))
    a(_t(X(SH_DIV/2+4),Y(CB_Y1)+14,'frame: back, end, cross and front rails; 2 posts',9.5,INK,'middle',700))
    a(_t(X(42),Y(CB_Y1)+14,'cabinet panels and the 3/4 x 1 front rail between them',9.5,'#5A3A00','start',700))
    a(_l(X(0),Y(CB_Y1)+30,X(3),Y(CB_Y1)+30,BLKC,1,'',_MK)); a(_t(X(3)+4,Y(CB_Y1)+34,'blocks at 3, 20 (if needed) and 41 in from the back mark',9.5,BLKC,'start',700))
    return '\n'.join(o)
def _rail5():
    """the front rail across the cabinet: from the aisle, from the side (the sag of the bare edge and of the railed edge, drawn about 3 times too big) and the joint in detail"""
    o = []; a = o.append
    EX = 3.0; SAG0 = 0.5; SAG1 = 1 / 16      # sag of the bare edge (a middle guess between 1/4 and 1 in) and of the railed edge, in inches
    GLU = '#D4A017'
    a(_t(40, 800, '4  The front rail across the cabinet makes the deck edge a stiff T-beam (sags drawn about 3 times too big)', 13, INK, 'start', 700))
    # --- (a) from the aisle ---
    S = 9.0; OX = 50; FLY = 1075
    X = lambda x: OX + S * (x - CB_X0); Z = lambda z: FLY - S * z
    xa, xb = X(CB_X0 + CB_T), X(CB_X1); mx = (xa + xb) / 2
    a(_l(X(CB_X0) - 20, Z(0), X(CB_X1 + CB_T) + 20, Z(0), INK, 2.5))
    a(_r(X(CB_X0) - 20, Z(DECK_T), X(CB_X1 + CB_T) + 40 - X(CB_X0), S * .75, BRN, '#3E230B', 1, '', .95))
    for px in (CB_X0, CB_X1): a(_r(X(px), Z(CB_H), S * CB_T, S * CB_H, PLY, INK, 1.2, '', .95))
    a(_r(X(BAT[0]), Z(9.5), S * (BAT[1] - BAT[0]), S * 9.5, '#F2B84B', AMB, 1.2, '4 3', .3))
    for u in (DC, INV): a(_r(X(u['x0']), Z(SH_Z1 + u['h']), S * (u['x1'] - u['x0']), S * u['h'], '#F6C28B', AMB, 1.1, '3 2', .55))
    a(_r(X(SH_X0), Z(FACE_Z1), S * (SH_X1 - SH_X0), S * (FACE_Z1 - FACE_Z0), PLY, INK, 1.1, '', 1)); a(_t(X(57), Z(12.2) + 4, 'shelf face', 10, INK, 'middle'))
    a(_r(xa, Z(RL_Z1), xb - xa, S * RL_H, RAILC, INK, 1.5, '', 1))
    a(_t(mx, Z(DECK_T) - 30, f'rail 3/4 x {fr8(RL_H)} hardwood, glued and screwed under the deck edge', 11.5, INK, 'middle', 700)); a(_l(mx, Z(DECK_T) - 24, mx, Z(RL_Z0 + .5), INK, 1, '3 2'))
    a(_l(xa, FLY + 22, xb, FLY + 22, INK, 1.6, '', _MK)); a(_t(mx, FLY + 40, f'{fr16(RL_X1 - RL_X0)} in between the panels', 11.5, INK, 'middle', 700))
    a(_t(X(CB_X0) - 20, Z(CB_H) - 78, 'from the aisle', 12, '#5F5E5A', 'start'))
    # --- (b) from the side ---
    S2 = 8.0; OY = 450
    Y = lambda y: OY + S2 * y; Z2 = lambda z: FLY - S2 * z
    a(_l(Y(-1), Z2(0), Y(29), Z2(0), INK, 2.5)); a(_l(Y(0), Z2(0), Y(0), Z2(26), INK, 4)); a(_t(Y(.5), Z2(25.2), 'wall', 11, INK, 'start'))
    a(_r(Y(0), Z2(DECK_U), S2 * BEAM_T, S2 * BR_H, RAILC, INK, 1.3, '', 1)); a(_t(Y(.3), Z2(BR_Z0 - .6) + 2, 'back beam', 10, INK, 'start', 700))
    for u in (DC, INV, CHG): a(_r(Y(u['y0']), Z2(SH_Z1 + u['h']), S2 * (u['y1'] - u['y0']), S2 * u['h'], '#F6C28B', AMB, 1.1, '3 2', .5))
    a(_r(Y(SH_Y0), Z2(SH_Z1), S2 * (SH_Y1 - SH_Y0), S2 * SH_T, PLY, INK, 1.1, '', 1)); a(_r(Y(CB_Y1 - .75), Z2(FACE_Z1), S2 * .75, S2 * (FACE_Z1 - FACE_Z0), PLY, INK, 1.1, '', 1))
    pts_t = []; pts_b = []; bare = []
    for k in range(0, 27):
        f = (max(0, k - BEAM_T) / (CB_Y1 - BEAM_T)) ** 2
        d1 = SAG1 * EX * S2 * f; d0 = SAG0 * EX * S2 * f
        pts_t.append((Y(k), Z2(DECK_T) + d1)); pts_b.append((Y(k), Z2(DECK_U) + d1)); bare.append((Y(k), Z2(DECK_T) + d0))
    a('<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts_t + pts_b[::-1]) + f'" fill="{BRN}" fill-opacity=".9" stroke="{GRN}" stroke-width="1.6"/>')
    a('<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in bare) + f'" fill="none" stroke="{RED}" stroke-width="1.8" stroke-dasharray="5 3"/>')
    a(_r(Y(CB_Y1 - RL_T), Z2(RL_Z1) + SAG1 * EX * S2, S2 * RL_T, S2 * RL_H, RAILC, '#5A3A00', 1.5, '', 1))
    a(_r(Y(0), Z2(SEAT_T), S2 * CB_Y1, S2 * CUSH, PUR, PUR, 1, '', .12)); a(_t(Y(10), Z2(PLAT + 2.2) + 3, 'seat cushion', 10.5, PUR, 'middle'))
    a(f'<path d="M {Y(23):.1f} {Z2(SEAT_T)-52:.1f} L {Y(23):.1f} {Z2(SEAT_T)-2:.1f}" stroke="{INK}" stroke-width="3" fill="none" marker-end="url(#c4a)"/>'); a(_t(Y(23) + 8, Z2(SEAT_T) - 40, 'weight', 11, INK, 'start', 700))
    a(_t(Y(0), Z2(26) - 14, 'from the side (wall on the left)', 12, '#5F5E5A', 'start'))
    a(_l(Y(1), FLY + 26, Y(5), FLY + 26, RED, 2, '5 3')); a(_t(Y(5.6), FLY + 30, 'bare edge: 1/4 to 1 in of sag', 11, RED, 'start', 700))
    a(_l(Y(1), FLY + 44, Y(5), FLY + 44, GRN, 2.4)); a(_t(Y(5.6), FLY + 48, 'with the glued rail: about 1/16 in', 11, GRN, 'start', 700))
    # --- (c) the joint, seen from the side, large ---
    S4 = 26.0; OX4 = 750
    Y4 = lambda y: OX4 + S4 * (y - 18); Z4 = lambda z: FLY - S4 * (z - 10)
    a(_t(OX4 - 6, Z4(18.4), 'the joint at the front edge', 12, '#5F5E5A', 'start'))
    a(_r(Y4(18), Z4(DECK_T), S4 * 8, S4 * .75, BRN, '#3E230B', 1.2, '', .95)); a(_t(Y4(18.2), Z4(DECK_T) + 14, 'deck 3/4', 9.5, INK, 'start', 700))
    a(_r(Y4(RL_Y0), Z4(RL_Z1), S4 * RL_T, S4 * RL_H, RAILC, '#5A3A00', 1.6, '', 1)); a(_l(Y4(RL_Y0), Z4(DECK_U), Y4(RL_Y1), Z4(DECK_U), GLU, 3.2))
    a(_t(Y4(RL_Y0) - 4, Z4(RL_Z1 - RL_H / 2) + 4, 'rail 3/4 x 1', 10, INK, 'end', 700))
    a(_l(Y4((RL_Y0 + RL_Y1) / 2), Z4(RL_Z0) + 2, Y4((RL_Y0 + RL_Y1) / 2), Z4(DECK_U + .5), RED, 2.4)); a(f'<circle cx="{Y4((RL_Y0+RL_Y1)/2):.1f}" cy="{Z4(RL_Z0)+2:.1f}" r="3.5" fill="{RED}"/>')
    a(_r(Y4(RL_Y0), Z4(FACE_Z1), S4 * .75, S4 * (FACE_Z1 - FACE_Z0), PLY, INK, 1.1, '', 1)); a(_t(Y4(CB_Y1) + 4, Z4(12.2), 'face', 9.5, INK, 'start'))
    a(_r(Y4(18.5), Z4(SH_Z1 + DC['h']), S4 * 6, S4 * DC['h'], '#F6C28B', AMB, 1.2, '3 2', .55)); a(_t(Y4(21.5), Z4(SH_Z1 + DC['h'] / 2) + 4, f'DC-DC {fr8(SH_Z1 + DC["h"])} up', 9.5, '#5A3A00', 'middle'))
    a(_l(Y4(23.2), Z4(RL_Z0), Y4(23.2), Z4(SH_Z1 + DC['h']), RED, 1.6, '', _MK)); a(_t(Y4(23.5), Z4(15.75) + 4, f'{fr8(RL_Z0 - SH_Z1 - DC["h"])} in', 9.5, RED, 'start', 700))
    for i, tx in enumerate(['glue (thick line) + #8 x 1 1/2 in screws every 6 in,', 'up through the rail into the deck;', f'rail bottom {fr8(RL_Z0)} up, over the DC-DC ({fr8(SH_Z1 + DC["h"])}) so', 'the shelf slides out under it']):
        a(_t(OX4 - 6, FLY + 26 + 13 * i, tx, 10.5, INK, 'start', 400))
    return '\n'.join(o)
_PARTS5=[
 ('1','Back rail','3/4 x 3 1/2 in hardwood or 3/4 in plywood ripped to 3 1/2',f'{fr8(C0)} long','1',f'full length, {fr8(BR_Z0)} to {fr8(DECK_U)} in up, against the wall on the wall blocks; over the cabinet it lies behind the shelf (the shelf starts 7 3/4 in out from the wall)'),
 ('1b','Back beam (doubler) and ledgers','a second 3/4 x 3 1/2 in rail glued to the front of the back rail; two 3/4 x 1 1/2 x 3 in hardwood ledgers',f'{fr16(CB_X1-CB_X0-CB_T)} long (the beam)','1 and 2','over the cabinet only (between the panels, 39 3/8 to 74 in) the rail is 1 1/2 in thick, with each end resting on a ledger screwed to the inner face of its panel (top at 13 1/2 in up); this holds the back of the lid there, 34 5/8 in between the panels'),
 ('2','Front rail','3/4 x 3 1/2 in, on edge',f'{fr16(SH_DIV)} long','1','under the deck\'s front edge from the west end to the west panel'),
 ('2b','Front rail across the cabinet',f'3/4 x {fr8(RL_H)} in hardwood (maple or oak), a straight board, on edge',f'{fr16(RL_X1-RL_X0)} long','1',f'between the two panels ({fr16(RL_X0)} to {fr8(RL_X1)} in), flush with the front of the deck, glued (waterproof wood glue) and screwed to the deck\'s underside: #8 x 1 1/2 in screws every 6 in from below, in pilot holes. Its bottom is {fr8(RL_Z0)} in up, 1/2 in over the tallest unit (the DC-DC charger, {fr8(SH_Z1+DC["h"])}), so the shelf slides out under it. Rail and plywood act as one T-shaped beam: about 1/16 in of sag at 100 lb, where the bare edge gave 1/4 to 1 in. It lifts out with the frame'),
 ('3','End rail and cross rail','3/4 x 3 1/2 in, on edge',f'{fr16(CB_Y1-1.5)} long','2',f'at the west end (x = 0) and in the middle (about {fr8(SH_DIV/2)} in from the back), between the back and front rails; glue and two #8 x 2 1/2 in screws at each end (or pocket screws)'),
 ('4','Posts','1 1/2 x 1 1/2 in hardwood',f'{fr8(BR_Z0-1)} long','2',f'at the front corners (0 and {fr16(POST_X[1])} in from the back), glued and screwed to the inside of the front rail; each with a T-nut and a 1/4-20 leveling foot that adds about 1 in (so the post and foot reach the floor from the rail underside at 13 1/2 in up) and screws out a little more to level; only two, so the 34 1/2 in lawn chairs still slide in between them'),
 ('5','Wall blocks (posts)','2x2 (1 1/2 x 1 1/2 in actual), 13 1/2 in long','1 1/2 x 1 1/2 x 13 1/2','3 (the middle one if needed)','stand on the floor against the wall at 3, 20 and 41 in from the back mark (centers), tops at the rail\'s underside (13 1/2 in up): they carry the back of the couch to the floor; two #8 x 3 in screws through each and the planks into S1 (3 up) and two into S2 (12 up) hold them upright; the one at 41 is 40 1/4 to 41 3/4 in, clear of the west panel (39 3/8) and the wheel well (42); the lawn chairs sit 1 1/2 in off the wall to clear them'),
 ('6','Dowels','3/8 x 1 in','','7','one glued into the top of each wall post (3) and two into the top of each cabinet panel (4), standing 1/2 in proud; each fits a 3/8 in hole, 3/4 in deep, in the underside of the frame (the back rail over a post, the deck over a panel) so the frame cannot slide sideways; nothing is screwed'),
 ('7','Deck','3/4 in plywood, 74 x 26 (with its leaf and hinge, diagrams C2 and C3)','74 x 26','1','glued and screwed down to the back, front, end and cross rails (#8 x 1 1/4 in every 8 in): the deck and the frame are ONE piece, so the whole frame lifts out together (about 80 lb without cushions: two people); over the cabinet it also rests on the tops of the two panels'),
 ('8','Hold-down for driving','two turn-buttons, or a strap and two floor eye bolts','','2','the frame only sits, so it could slide or lift when the van brakes or hits a bump: two turn-buttons on the cabinet panels that swing over the deck, or a strap to two floor anchors, hold it down while you drive and take a minute to undo'),
]
_STEPS5=[
 '<b>Make the three blocks.</b> Cut a 2x2 into three 13 1/2 in posts (a stop block on the saw keeps them identical; the floor is level but check each post is square), and seal them. The one at 20 in is the one you said "maybe, if needed": cut it, but fit it only if the frame feels springy.',
 f'<b>Mark them on the wall.</b> Centers at {BLK_X[0]}, {BLK_X[1]} and {BLK_X[2]} in from the back mark; each stands on the finished floor and its top must be {fr8(BLK_Z1)} in up, so shim under any that comes up short and plane or trim any that is long: the back rail rests on all three tops. The strips S1 (3 up) and S2 (12 up) sit behind the planks, so each post has two screws into each.',
 '<b>Screw each block on:</b> a bead of construction adhesive on its back, then two #8 x 3 in screws into S1 and two into S2 through the 3/8 in planks (pilot holes). The posts stand on the floor, so the strips only keep them upright and stop the couch sliding sideways; the strips are glued to the steel only at their dots (S2: 15, 30 3/4, 40), but that is enough for that job.',
 f'<b>Build the frame on the bench:</b> the back rail ({fr8(C0)} long), the front rail ({fr16(SH_DIV)}), the end rail and the cross rail ({fr16(CB_Y1-1.5)}), all 3/4 x 3 1/2 on edge, glued and screwed into a ladder, with the tops flush; glue the doubler ({fr16(CB_X1-CB_X0-CB_T)} long) to the front of the back rail over the cabinet. Check the diagonal of the west rectangle. Glue and screw the two posts to the front rail\'s inside face, fit the T-nuts and feet, and screw the feet in so each post and foot is about 13 1/2 in to start.',
 f'<b>Put the deck on and glue the rail under it.</b> Lay the deck (74 x 26, 3/4 plywood) on the ladder, glue and screw it down (#8 x 1 1/4 in every 8 in), then clamp the 3/4 x {fr8(RL_H)} hardwood rail to the underside of its front edge between {fr16(RL_X0)} and {fr8(RL_X1)} in, flush with the front, with glue along its whole length. Pilot-drill and drive #8 x 1 1/2 in screws up through the rail every 6 in (they stop 1/4 in short of the top face). Check the rail with a straightedge: its bottom must be {fr8(RL_Z0)} in up and straight, because the gear shelf slides under it with 1/2 in to spare. Let the glue set a day.',
 '<b>Screw the two ledgers</b> (3/4 x 1 1/2 x 3 in, tops at 13 1/2 in up) to the inner faces of the cabinet panels at the wall end, one on each. <b>Lift the frame in:</b> the back rail goes onto the three blocks, the front posts on the floor, and the ends of the doubled part rest on the two ledgers. Adjust the two feet until the tops of the rails are level (use a level on the front rail and a straightedge from the front rail over the west panel top to the east panel top); the panel tops are at 17 in, and so are the rail tops.',
 '<b>Fit the dowels:</b> glue a 3/8 x 1 in dowel into the top of each wall post and two into the top of each cabinet panel, and drill matching 3/8 in holes, 3/4 in deep, in the underside of the back rail over each post and in the deck over each panel. Nothing is screwed: the back stands on the three wall posts, the front on its two posts, and the ends of the doubled part on the two ledgers.',
 '<b>Try it in place:</b> pull the gear shelf out and push it home: the tallest unit must slide under the front rail with 1/2 in to spare, and the face must clear it by 1 3/4 in. Then put a person on the front edge of the deck over the cabinet (34 5/8 in between the panels) before the cushions go on: it should feel solid, with no more than about 1/16 in of give. If it springs more, add a second row of screws, or glue a second 3/4 x 1 strip under the first at the middle (the units have 1/2 in to spare, so check the shelf again).',
 '<b>To take the couch out:</b> take the hold-downs off, the cushions off and the leaf folded back, then two people lift the whole frame straight up off its dowels (about 80 lb) and carry it out end first through the rear doors (its cross-section is only about 26 x 18 in). Everything else, the cabinet, the shelf and the battery, stays. To put it back, lower it over the cabinet and the dowels find their holes.',
]
def _c5_html():
    pt='<table><tr><th>#</th><th>Part</th><th>Material</th><th>Size (in)</th><th>Qty</th><th>Notes</th></tr>'+''.join(f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a,b,c,d,e,f in _PARTS5)+'</table>'
    st='<ol>'+''.join(f'<li>{x}</li>' for x in _STEPS5)+'</ol>'
    svg=['<svg viewBox="0 0 1000 1130" role="img"><title>The removable couch: the frame, the wall blocks, the deck and the gear cabinet</title>','<defs><marker id="c4a" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker></defs>',_aisle5(),_section5(),_plan5(),_rail5(),'</svg>']
    return ('<h3>Driver side: the removable couch (frame, wall blocks and deck), how to make it</h3>\n<div class="wide">'+'\n'.join(svg)+'</div>\n'
     f'<p>The couch is a separate piece, built apart from the gear cabinet (diagram C4). The cabinet, with the battery under it and the shelf on top, is permanent. The couch frame, with its deck on top, lifts up and out of the van in one piece, and when it is set down it just sits over the cabinet: nothing is screwed to the van or the cabinet, and dowels in the post tops and the panel tops fit holes in its underside so it cannot slide. <b>The frame</b> has a full-length back rail ({fr8(C0)} in, 3/4 x 3 1/2 on edge) that just rests on three wall blocks, which are 2x2 posts standing on the floor against the wall at {BLK_X[0]}, {BLK_X[1]} (if needed) and {BLK_X[2]} in from the back mark; west of the cabinet (0 to {fr16(SH_DIV)} in) a front rail, an end rail and a cross rail make a ladder carried at the front by two posts with screw-out feet, with the lawn chairs between them. <b>What holds it up:</b> at the back the three wall posts, at the front the two front posts west of the cabinet, and over the cabinet the two panels, with the back rail doubled and resting on a ledger on each panel; the wall itself carries none of the weight. Over the cabinet the front rail is only 3/4 x 1 and is glued under the deck edge, because the units on the shelf are almost as tall as the room under the deck (the 3 1/2 in rails would hit them). <b>The deck</b> (3/4 in plywood, 74 x 26, with the leaf and cushions of diagrams C, C2 and C3) is glued and screwed to the rails, so deck and frame are one piece of about 80 lb that two people can lift. Because it only sits, add two turn-buttons or a strap to hold it down when you drive. Nothing is fixed to the floor except the cabinet.</p>\n'
     f'<p><b>The deck\'s front edge over the cabinet (drawing 4).</b> The deck is held along the back (the doubled back rail on its two ledgers) and at both ends (the panel tops), and its front edge runs {fr16(CB_X1-CB_X0-CB_T)} in between the panels. A rough hand calculation (3/4 in plywood, about 100 lb reaching a 12 in wide strip in the middle of the front edge, plywood stiffness 1.2 million psi) gave about 1/4 in of sag for a bare edge acting like a beam between the two panels, and about 1 in if it acted like a cantilever off the back beam, so a rail was needed. A deep rail would hit the units, so the couch was raised 1 in: the deck underside is now {fr8(DECK_U)} up and a hardwood rail 3/4 x {fr8(RL_H)} hangs from its front edge, bottom at {fr8(RL_Z0)}, 1/2 in over the tallest unit ({fr8(SH_Z1+DC["h"])}). Glued and screwed along its whole length, it makes the plywood and the rail one T-shaped beam (about 12 in of deck acting as the top flange; hardwood stiffness 1.4 million psi), which this calculation puts at about 1/16 in of sag at 100 lb, a quarter or less of the bare edge\'s. The cost is that the seat is 1 in higher ({fr8(SEAT_T)} in) and the headroom under the wall cabinets is 2 1/2 in for a 6 ft person. The estimate is rough: load the front edge with a person before the cushions go on.</p>\n'
     '<p><b>Parts</b> (the numbers 1 and 2 on the drawing are the wall blocks and the cabinet panels):</p>\n'+pt+'\n<p><b>How to build it, in order:</b></p>\n'+st+
     '\n<p><b>Not settled:</b> how stiff the glued front rail really is (an estimate of about 1/16 in at 100 lb: test it before the cushions go on), the weight of the whole frame (about 80 lb without cushions is an estimate), and whether you want the hold-downs (a frame that only sits can slide or lift in a hard stop).</p>\n')
_h=open((ROOT+'/sides.html')).read()
assert '<h2>2. Passenger side</h2>' in _h
_h=_h.replace('<h2>2. Passenger side</h2>',_c5_html()+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
