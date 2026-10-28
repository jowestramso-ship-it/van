"""The block placement chart of the Furring page of the build guide: where every spacer block goes on the driver wall and on the passenger wall (a block is 1 1/2 along the wall x 3 1/2 up, 3 5/8 out with the glue),
each marked with its distance from the back mark, and a table by furring rail. It only draws what the furring maps already hold (AP, PAP, FRAME_BLK, VFR, WIN_FRAME, HT in furring.py), so the chart and the maps cannot disagree.
Used by buildguide.py (the Furring page): block_html(FD), where FD is the namespace made by running shelfdata.py and furring.py. Run on its own it writes ../blocks.html for a quick look."""
import os

INK = '#2C2C2A'; BLK = '#5A2E0A'; STRIP = '#E9D3AA'; BLU = '#185FA5'; RED = '#A32D2D'; GRY = '#9A9DA3'

def _t(x, y, s, sz=10, anchor='middle', col=INK, w=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="font-size:{sz}px;font-weight:{w};fill:{col};paint-order:stroke;stroke:#fff;stroke-width:2.6px;stroke-linejoin:round">{s}</text>'
def _r(x, y, w, h, fill, stroke=INK, sw=1, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def _l(x1, y1, x2, y2, col=INK, sw=1, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d}/>'

def _blocks(FD, side):
    """every block of one wall: (label group, number, x along the wall from the back mark, z height of its center, flat?)"""
    HT, out = FD['HT'], []
    if side == 'D':
        for n in ('S4', 'S5', 'S6'):
            for x in FD['AP'][n]: out.append((n, x, HT[n], False))
        for nm, cx, cz in FD['FRAME_BLK']: out.append((nm, cx, cz, nm in ('J3', 'J4')))
        for nm, cx, cz in FD['NOOK_BLK_D']: out.append((nm, cx, cz, False))
    else:
        for n in ('S4', 'S5', 'S6'):
            for x in FD['PAP'][n]:
                if n == 'S5' and not (31.25 <= x <= 74.5): continue
                out.append((n, x, HT[n], False))
        for nm, x0, x1, b, t, sp in FD['VFR']:
            if sp:
                for hh in (b + 5, (b + t) / 2, t - 5): out.append((nm, (x0 + x1) / 2, hh, False))
    return [(g, i + 1, x, z, fl) for i, (g, x, z, fl) in enumerate(out)]

def _map(FD, side):
    fr16, HT = FD['fr16'], FD['HT']
    S = 6.4; X0 = 56; FL = 560
    flip = side == 'P'
    xx = (lambda x: X0 + S * (154 - x)) if flip else (lambda x: X0 + S * x)
    yy = lambda z: FL - S * z
    o = []; a = o.append
    W = 154
    a(_t(X0, 22, ('Driver' if not flip else 'Passenger') + ' wall: every spacer block, seen from inside the van (' + ('rear doors on the left, cab on the right' if not flip else 'cab on the left, rear doors on the right') + ')', 14, 'start', INK, 700))
    a(_r(xx(0) if not flip else xx(W), yy(75.5), S * W, S * 75.5, '#F7F5EE', '#5F5E5A', 1.6))
    a(_l(xx(0), yy(74.5625), xx(W), yy(74.5625), GRY, 1, '6 3')); a(_t(xx(W / 2), yy(74.5625) - 4, 'finished ceiling at the wall 74 9/16', 9.5, 'middle', '#5F5E5A'))
    # the grid: ticks every 10 in along the wall and every 10 up
    for t in range(0, W + 1, 10):
        a(_l(xx(t), yy(0), xx(t), yy(75.5), '#D3D1C7', .7, '2 3')); a(_t(xx(t), FL + 14, str(t), 9.5, 'middle', BLU, 600))
    for z in range(0, 80, 10):
        a(_l(xx(0), yy(z), xx(W), yy(z), '#D3D1C7', .7, '2 3')); a(_t(X0 - 8 if not flip else X0 - 8, yy(z) + 3, str(z), 9.5, 'end', '#8A4B0F', 600))
    a(_t(xx(W / 2), FL + 30, 'inches along the wall from the back mark (6 in in from the rear-door edge)', 10.5, 'middle', '#5F5E5A'))
    # the furring rails S1 to S8 (3 1/2 wide), pale, with the segments each really has
    SEG = FD['SEG_D'] if not flip else FD['SEG_P']
    for n, h in HT.items():
        for x0, x1 in SEG[n]:
            xa, xb = sorted((xx(x0), xx(x1)))
            a(_r(xa, yy(h + FD['STRIP_W'] / 2), xb - xa, S * FD['STRIP_W'], STRIP, '#B8975A', 1))
        x2 = SEG[n][0][0] + 2 if SEG[n][0][0] > 2 else 2                # the name sits on the first piece (S5 starts after the nook behind the couch)
        a(_t(xx(x2) if not flip else xx(W - 2), yy(h) + 3.5, n, 10, 'middle', '#5A3A00', 700))
    # the wheel well, the window, the sliding door, the nooks
    a(_r(xx(42) if not flip else xx(76), yy(7.5), S * 34, S * 7.5, '#D8B79A', '#8A6B4D', 1, 'fill-opacity=".7" stroke-dasharray="4 3"')); a(_t(xx(59), yy(3.2), 'wheel well', 9.5, 'middle', '#5A3A00'))
    if not flip:
        wx0, wx1, wz0, wz1 = FD['WIN_CX0'], FD['WIN_CX1'], FD['WIN_CZ0'], FD['WIN_CZ1']
        a(_r(xx(wx0), yy(wz1), S * (wx1 - wx0), S * (wz1 - wz0), '#B5D4F4', BLU, 1.4, 'fill-opacity=".35"')); a(_t(xx((wx0 + wx1) / 2), yy((wz0 + wz1) / 2) + 3, 'side window cutout', 10, 'middle', BLU, 600))
        for nm, x0, x1, z0, z1 in FD['WIN_FRAME']:
            a(_r(xx(x0), yy(z1), S * (x1 - x0), S * (z1 - z0), '#E9D3AA', '#B8975A', 1, 'fill-opacity=".9"'))
        a(_r(xx(FD['CN_X0']), yy(FD['CN_OZ1']), S * (FD['CN_X1'] - FD['CN_X0']), S * (FD['CN_OZ1'] - FD['CN_OZ0']), '#F6EBD4', '#534AB7', 1.4, 'stroke-dasharray="6 3"')); a(_t(xx((FD['CN_X0'] + FD['CN_X1']) / 2), yy(48.4), 'nook behind the couch (S5 cut away)', 10.5, 'middle', '#3C3489', 600))
        for nm, x0, x1, b, t, sp in FD['VFR_D']:
            a(_r(xx(x0), yy(t), S * (x1 - x0), S * (t - b), '#E9D3AA', '#B8975A', 1))
    else:
        a(_r(xx(155), yy(67), S * (155 - 104), S * 67, '#fff', '#8A5A00', 1.4, 'stroke-dasharray="6 4"')); a(_t(xx(129.5), yy(33), 'sliding door opening', 11, 'middle', '#8A5A00', 600)); a(_t(xx(129.5), yy(33) + 14, '(no wall behind it)', 10, 'middle', '#8A5A00'))
        for nx0, nx1 in ((12.5, 29.75), (76, 93.25)):
            a(_r(xx(nx1), yy(54), S * (nx1 - nx0), S * 16, '#F6EBD4', '#7A4A1E', 1.2, 'stroke-dasharray="5 3"')); a(_t(xx((nx0 + nx1) / 2), yy(46), 'nook', 10, 'middle', '#7A4A1E'))
        for nm, x0, x1, b, t, sp in FD['VFR']:
            xa, xb = sorted((xx(x0), xx(x1)))
            a(_r(xa, yy(t), xb - xa, S * (t - b), '#E9D3AA', '#B8975A', 1))
    # the blocks, each with its distance from the back mark under or over it
    bl = _blocks(FD, side)
    for g, i, x, z, fl in bl:
        w, h = (3.5, 1.5) if fl else (1.5, 3.5)
        a(_r(xx(x) - S * w / 2, yy(z) - S * h / 2, S * w, S * h, BLK, '#fff', 1, 'rx="1"'))
    for k, (g, i, x, z, fl) in enumerate(bl):
        if g in ('S4', 'S5', 'S6'):
            n = sum(1 for gg, *_ in bl[:k] if gg == g)                  # alternate the labels below and above the furring rail so close blocks do not touch
            ty = yy(z) + S * 1.75 + 10 if n % 2 == 0 else yy(z) - S * 1.75 - 4
            a(_t(xx(x), ty, fr16(x), 8.5, 'middle', '#3E230B', 700))
        elif g in ('J1', 'J2'):                                         # a window jamb: its height up, inside the cutout so the furring rails' labels stay clear
            left = (g == 'J1') != flip
            a(_t(xx(x) + (S * 2.4 if left else -S * 2.4), yy(z) + 3, g + ' ' + fr16(z) + ' up', 8.5, 'start' if left else 'end', '#3E230B', 700))
        elif fl:                                                        # the sill and the head: the distance along, below the sill and above the head
            a(_t(xx(x), yy(z) + (S * 1.8 + 9 if g == 'J3' else -S * 1.8 - 3), fr16(x), 8.5, 'middle', '#3E230B', 700))
        else:                                                           # a nook frame: its name and height up, beside it (V3's on the counter nook side)
            left = g in ('V3', 'V5')                                      # V3 on the counter nook side, V5 on the rear side of the couch nook
            a(_t(xx(x) + (-S * 2.1 if left else S * 2.1), yy(z) + 3, g + ' ' + fr16(z) + ' up', 8.5, 'end' if left else 'start', '#3E230B', 700))
    return _svg(1100, 610, ''.join(o), f'Where every spacer block goes on the {"driver" if not flip else "passenger"} wall'), bl

def _svg(w, h, body, title):
    return f'<svg viewBox="0 0 {w} {h}" role="img" style="width:100%;height:auto;display:block;background:#fff;border-radius:6px"><title>{title}</title>{body}</svg>'

def _table(FD, side, bl):
    fr16, fr8, HT = FD['fr16'], FD['fr8'], FD['HT']
    rows = []
    for g in ('S4', 'S5', 'S6', 'J1', 'J2', 'J3', 'J4', 'V5', 'V6', 'V1', 'V2', 'V3'):
        it = [(i, x, z) for gg, i, x, z, fl in bl if gg == g]
        if not it: continue
        if g in HT: what = f'furring rail {g}, {fr8(HT[g])} up'
        elif g.startswith('J'): what = {'J1': 'window frame, left jamb', 'J2': 'window frame, right jamb', 'J3': 'window frame, sill', 'J4': 'window frame, head'}[g]
        else: what = {'V1': 'shower nook rear frame', 'V2': 'shower nook front frame', 'V3': 'counter nook rear frame', 'V5': 'couch nook rear frame', 'V6': 'couch nook front frame'}[g]
        if g in HT or g in ('J3', 'J4'): pos = ', '.join(fr16(x) for _i, x, _z in it)
        else: pos = f'{fr16(it[0][1])} in from the back, at ' + ', '.join(fr16(z) for _i, _x, z in it) + ' in up'
        rows.append(f'<tr><td><b>{g}</b></td><td>{what}</td><td>{len(it)}</td><td>{pos}</td></tr>')
    return '<div class="wide"><table class="rt"><tr><th>Where</th><th>What it holds</th><th>Blocks</th><th>Positions, in from the back mark (furring rails and sill/head), or the heights up for a frame</th></tr>' + ''.join(rows) + '</table></div>'

CSS = '<style>.bmap{margin:10px 0 18px}.bmap figure{margin:0 0 10px;border:1px solid #d9d5ca;border-radius:8px;padding:8px;background:#fff;min-width:0}.bmap figcaption{font-size:14px;line-height:1.45;margin-top:6px}</style>'

def block_html(FD):
    d, bd = _map(FD, 'D'); p, bp = _map(FD, 'P')
    return (CSS + '<h3>Where every spacer block goes (' + str(len(bd) + len(bp)) + ' blocks)</h3>'
            '<p>A block is a 3 1/2 in cut of 2x4 stood on its 3 1/2 in side: <b>1 1/2 along the wall x 3 1/2 up</b> on the steel, <b>3 5/8 in out</b> with the glue. Its center sits on the dot, and its vertical center is the furring rail\'s height (the window sill and head blocks lie on their side). Each dark block below shows its distance from the back mark; the tables list the same numbers. S1, S2 and S3 take adhesive pads and S7 and S8 thin shims at their dots, not blocks (the maps and the glossary below the diagrams show all three).</p>' + FD['marks_html']() +
            '<div class="bmap"><figure>' + d + f'<figcaption><b>Driver wall: {len(bd)} blocks</b> (S4, S5 and S6 at their dots, three under each of the four window frame pieces, and three under each of the two couch nook frames V5 and V6).</figcaption></figure>' + _table(FD, 'D', bd) +
            '<figure style="margin-top:14px">' + p + f'<figcaption><b>Passenger wall: {len(bp)} blocks</b> (S4, S6, the middle piece of S5, and three under each nook frame V1 to V3; V4 sits straight on the steel).</figcaption></figure>' + _table(FD, 'P', bp) + '</div>')


def _arr(x1, y1, x2, y2, col=INK, sw=1):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 6
    hd = lambda x, y, ang: f'<polygon points="{x:.1f},{y:.1f} {x - L * math.cos(ang - .45):.1f},{y - L * math.sin(ang - .45):.1f} {x - L * math.cos(ang + .45):.1f},{y - L * math.sin(ang + .45):.1f}" fill="{col}"/>'
    return _l(x1, y1, x2, y2, col, sw) + hd(x2, y2, a) + hd(x1, y1, a + math.pi)

def _call(x, y, tx, ty, s, anchor='start', col=INK, sz=11.5):
    return _l(tx + (3 if anchor == 'start' else -3), ty, x, y, col, 1) + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{col}"/>' + _t(tx + (8 if anchor == 'start' else -8), ty + 4, s, sz, anchor, col)

def _mk(x, y, ch, col=INK):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="9" fill="#fff" stroke="{col}" stroke-width="1.6"/>' + _t(x, y + 4, ch, 11.5, 'middle', col, 700).replace('stroke-width:2.6px', 'stroke-width:0px')

def _att_svg():
    S = 52; X0 = 96; ZB = 372                       # S px per inch; X0 the steel face at the dot; ZB the bottom of the block
    X = lambda x: X0 + S * x; Z = lambda z: ZB - S * z
    BR = '#B45309'; GL = '#8A6A00'; WD = '#5A3A00'
    xs = {'bond': 0, 'blk': .125, 'glue': 3.625, 'strip': 3.625, 'ply': 4.375}       # inches out from the steel face
    o = []; a = o.append
    a(_t(20, 24, 'Attaching a block to the steel: a section through one block', 13.5, 'start', INK, 700))
    a(_t(20, 41, 'the steel of the van on the left, the room on the right; this is a cut across the wall at the middle of a block', 11, 'start', '#5F5E5A'))
    a('<defs><pattern id="hst" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9AA0A8" stroke-width="2"/></pattern></defs>')
    a(_r(X(-1.05), Z(5.3), S * 1.05, S * 5.8, 'url(#hst)', '#9AA0A8', 1))                                                       # the steel
    a(_r(X0 - 1.5, Z(5.3), 3, S * 5.8, BR, BR, .5))                                                                             # its cleaned, scuffed face
    a(_t(52, ZB + 44, 'outside of the van', 10, 'middle', '#5F5E5A', 600))
    a(_r(X(xs['bond']), Z(3.5), S * .125, S * 3.5, '#D4A017', GL, 1))                                                          # the bond line
    a(_r(X(xs['blk']), Z(3.5), S * 3.5, S * 3.5, '#C8A878', INK, 1.4))                                                         # the block
    for k in range(1, 7): a(_l(X(xs['blk']) + 4, Z(3.5) + S * 3.5 * k / 7, X(3.625) - 4, Z(3.5) + S * 3.5 * k / 7, '#A8885A', .8))   # the grain, running up
    a(_r(X(xs['strip']), Z(3.5), S * .75, S * 3.5, '#E9D3AA', '#B8975A', 1.3))                                                 # the 1x4 furring rail
    a(_r(X(xs['glue']), Z(3.5), 4, S * 3.5, '#D4A017', GL, .6))                                                                # wood glue
    a(_r(X(xs['ply']), Z(5.3), S * .375, S * 5.8, '#F3E7C8', '#B8975A', 1))                                                    # the plywood, later
    xh = X(xs['ply']); a(_l(xh, Z(1.75), X(2.7), Z(1.75), RED, 2.4)); a(_r(xh - 3, Z(1.75) - 5, 4, 10, RED, RED, .5))       # the furring rail's screw
    # the markers, with short straight leaders
    my = 78
    for xm, top, ch, col in ((X(-.55), Z(5.3), 'a', BR), (X(.06) + 3, Z(3.5), 'b', GL), (X(1.9), Z(3.5), 'c', WD), (X(3.625) + 2, Z(3.5), 'd', GL), (X(4.0), Z(3.5), 'e', WD), (X(4.56), Z(5.3), 'g', '#5F5E5A')):
        a(_l(xm, my + 9, xm, top, col, 1.2)); a(_mk(xm, my, ch, col))
    a(_l(xh + S * .375 + 2, Z(1.75), xh + S * .375 + 26, Z(1.75), RED, 1.2)); a(_mk(xh + S * .375 + 35, Z(1.75), 'f', RED))
    # the two standoffs, measured from the steel
    for k, (xe, lab, yo) in enumerate(((3.625, '3 5/8 in: the block and its glue', 26), (4.375, '4 3/8 in to the face of the furring rail', 56))):
        yd = ZB + yo; a(_l(X0, ZB + 2, X0, yd + 5, '#B4B2A9', .8, '3 3')); a(_l(X(xe), ZB + 2, X(xe), yd + 5, '#B4B2A9', .8, '3 3'))
        a(_arr(X0, yd, X(xe), yd)); a(_t(X(xe) + 8 if k else X0 + 8, yd - 5, lab, 11, 'start', INK, 700 if k == 0 else 600))
    # the key
    KX = 420; ky = 96
    key = [('a', BR, ['the van\'s steel at the dot: scuffed dull, wiped with', '70/30 alcohol and water, dry. Nothing is screwed into it']),
           ('b', GL, ['bond line, 1/8 in: polyurethane adhesive (Sikaflex-252)', 'or VHB tape (about 110 mil), put on the block']),
           ('c', WD, ['block: a 3 1/2 in cut of 2x4. 1 1/2 along the wall,', '3 1/2 up, 3 1/2 out; the grain runs up the face']),
           ('d', GL, ['wood glue between the block and the furring rail']),
           ('e', WD, ['furring rail: 1x4 laid flat, 3/4 x 3 1/2 in']),
           ('f', RED, ['one #8 x 1 1/2 in screw per block, in a pilot hole']),
           ('g', '#5F5E5A', ['plywood wall, 3/8 in; it goes on later, over the screw heads'])]
    for ch, col, ls in key:
        a(_mk(KX, ky, ch, col))
        for n, ln in enumerate(ls): a(_t(KX + 18, ky + 4 + 15 * n, ln, 11.5, 'start', INK))
        ky += 15 * len(ls) + 17
    a(_t(KX - 9, ky + 12, 'The furring rail\'s back ends up about 3 3/4 in off the body of the van', 11, 'start', '#5F5E5A'))
    a(_t(KX - 9, ky + 27, '(the steel at the dots is 1/8 in off the body), the same line as', 11, 'start', '#5F5E5A'))
    a(_t(KX - 9, ky + 42, 'the pads and shims on the other furring rails.', 11, 'start', '#5F5E5A'))
    return _svg(780, 460, ''.join(o), 'Attaching a spacer block to the steel')

ATT_STEPS = [
    '<b>Mark the dots.</b> From the chart above, mark each block\'s place on the steel with a pencil or a bit of tape (its distance from the back mark and its height up). Each one goes on solid steel at the dot, clear of the holes and of the edges of the pans.',
    '<b>Prepare the steel</b> at each mark, a little bigger than the block: remove loose paint and rust; wipe off any oil or wax; scuff lightly with a gray Scotch-Brite pad or 400 grit paper until the paint is evenly dull (if you go through to bare steel, touch it with a rust-inhibiting primer first); vacuum the dust; wipe with a 70/30 mix of isopropyl alcohol and water on a lint-free cloth and dry it with another; do not touch it again.',
    '<b>Prepare the block.</b> Sand the face smooth and wipe off the dust. For VHB tape, also seal the face with a coat of polyurethane and let it dry, because raw wood is porous.',
    '<b>Put the adhesive on the block, not on the steel.</b> Polyurethane adhesive (Sikaflex-252 or similar): a bead round the edge of the 1 1/2 x 3 1/2 in face and one down the middle, enough to leave a 1/8 in bond line when pressed. It works from 50 to 95 F and stays workable for only about 35 minutes at 73 F, so press each block on within that time. VHB tape (about 110 mil, so the 3 1/2 in block plus the tape is the 3 5/8 in standoff): put the tape on the block face first, press it firmly, then peel the liner. Apply it only when the steel, the block and the tape are between 70 and 100 F, never below about 50 F, and with no condensation on the steel.',
    '<b>Set the block on its mark</b>, square to the wall with its 3 1/2 in side up, and press it on at once (no sliding it around). Use a furring rail as the gauge: lay one of the furring rail\'s own pieces across the faces of the blocks of that furring rail, with wax paper or plastic wrap between so it does not stick, and press each block against it, so they all end on one line. With VHB press hard, about 15 psi, which on this face is about 79 lb, for a minute, and brace it. With adhesive hold it with masking tape or a prop until it sets. Nothing is screwed into the van body: there are no holes through to the outside.',
    '<b>Leave it a day or more</b> before it takes any load. Then lay a straightedge across the blocks of one furring rail: their outer faces should be within about 1/16 in of each other (sand a high block, or shim a low one with thin veneer), so the furring rail\'s back sits 3 3/4 in off the body along its whole length.',
    '<b>Then the furring rail:</b> wood glue on the block, the furring rail on top, and one #8 x 1 1/2 in screw through the furring rail into the block, in a pilot hole. S1, S2 and S3 (adhesive pads) and S7 and S8 (shims) get their pad or shim glued to the steel the same way (steps 2 to 6), and the furring rail goes on top of it.',
    '<b>Test one block first.</b> Glue one block to a spot that will be hidden and try to pry it off with a flat bar after a day: it should tear the wood or the paint off the steel, not let go clean. If it lets go clean, the steel was not clean enough or the wrong adhesive for it.',
]

def attach_html(FD):
    return ('<h3>How to attach a block to the steel</h3>'
            '<p>All ' + str(FD['TOT_BLOCKS']) + ' blocks go on the same way, with adhesive or tape and never with screws. The drawing shows one block in section; the steps follow.</p>'
            '<figure style="margin:0 0 12px;border:1px solid #d9d5ca;border-radius:8px;padding:8px;background:#fff;min-width:0">' + _att_svg() + '</figure>'
            '<ol class="steps">' + ''.join(f'<li>{x}</li>' for x in ATT_STEPS) + '</ol>')


def _flat_svg():
    RAIL = '#E9D3AA'; RS = '#B8975A'; GR = '#5F5E5A'
    o = []; a = o.append
    a(_t(10, 22, 'What "laid flat" means: the same 1x4 board four ways', 13.5, 'start', INK, 700))
    a('<defs><pattern id="hst2" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9AA0A8" stroke-width="2"/></pattern></defs>')
    for x, y in ((10, 44), (395, 44), (10, 360), (395, 360)): a(_r(x, y, 375, 300, '#fff', '#D9D5CA', 1, 'rx="8"'))
    # 1. the board, cut across (50 px per inch)
    a(_t(24, 66, 'The board, cut across (the end of it)', 12.5, 'start', INK, 700))
    a(_r(100, 96, 37.5, 175, RAIL, INK, 1.6))
    a(_arr(82, 96, 82, 271)); a(_t(76, 188, '3 1/2 in', 11, 'end', INK, 700))
    a(_arr(100, 86, 137.5, 86)); a(_t(119, 80, '3/4 in', 11, 'middle', INK, 700))
    a(_l(137.5, 190, 188, 190, INK, 1)); a(f'<circle cx="137.5" cy="190" r="2.4" fill="{INK}"/>')
    a(_t(194, 186, 'wide face', 12, 'start', INK, 700)); a(_t(194, 201, 'the 3 1/2 in side', 11, 'start', GR))
    a(_l(131, 96, 188, 118, INK, 1)); a(f'<circle cx="131" cy="96" r="2.4" fill="{INK}"/>')
    a(_t(194, 126, 'edge', 12, 'start', INK, 700)); a(_t(194, 141, 'the 3/4 in side', 11, 'start', GR))
    for k, ln in enumerate(['A board sold as 1x4 really measures', '3/4 x 3 1/2 in. This is the end of it,', 'as if it were cut across.']): a(_t(24, 304 + 16 * k, ln, 11.5, 'start', INK))
    # 2. laid flat (32 px per inch): the section across the wall
    a(_t(409, 66, 'Laid flat (how the furring rails are used)', 12.5, 'start', '#2E6B2E', 700))
    a(_r(420, 80, 32, 170, 'url(#hst2)', '#9AA0A8', 1)); a(_r(451, 80, 2, 170, '#B45309', '#B45309', .5))
    a(_r(453, 100, 4, 112, '#D4A017', '#8A6A00', .8)); a(_r(457, 100, 112, 112, '#C8A878', INK, 1.3))
    a(_r(569, 100, 24, 112, RAIL, INK, 1.6)); a(_l(596, 80, 596, 230, GR, 1.2, '4 3'))
    a(_t(606, 92, 'plywood goes here, later', 10.5, 'start', GR))
    a(_t(436, 266, 'steel', 11, 'middle', GR, 600)); a(_t(513, 230, 'spacer', 11, 'middle', GR, 600))
    a(_t(606, 128, 'wide face,', 12, 'start', INK, 700)); a(_t(606, 143, 'toward the room', 12, 'start', INK, 700))
    a(_arr(668, 156, 598, 156, INK, 1.4)); a(_t(606, 172, 'furring rail:', 11.5, 'start', INK, 600)); a(_t(606, 186, '3/4 in out,', 11.5, 'start', INK)); a(_t(606, 200, '3 1/2 in up', 11.5, 'start', INK))
    a(_arr(569, 226, 593, 226)); a(_t(606, 230, '3/4 in thick', 10.5, 'start', GR))
    for k, ln in enumerate(['Laid flat: the wide face looks into the room and', 'the other wide face sits on the spacers, so the board', 'sticks out only 3/4 in from them.']): a(_t(409, 294 + 16 * k, ln, 11.5, 'start', INK))
    # 3. on edge (not used)
    a(_t(24, 382, 'On edge (NOT used)', 12.5, 'start', RED, 700))
    a(_r(36, 396, 32, 170, 'url(#hst2)', '#9AA0A8', 1)); a(_r(67, 396, 2, 170, '#B45309', '#B45309', .5))
    a(_r(69, 416, 4, 112, '#D4A017', '#8A6A00', .8)); a(_r(73, 416, 112, 112, '#C8A878', INK, 1.3))
    a(_r(185, 460, 112, 24, RAIL, INK, 1.6)); a(_l(300, 396, 300, 566, GR, 1.2, '4 3'))
    a(_t(183, 412, 'spacer', 11, 'middle', GR, 600)); a(_t(52, 579, 'steel', 11, 'middle', GR, 600))
    a(_l(290, 460, 290, 446, INK, 1)); a(f'<circle cx="290" cy="460" r="2.4" fill="{INK}"/>')
    a(_t(192, 427, 'only a 3/4 in edge', 10.5, 'start', INK, 600)); a(_t(192, 440, 'to screw to', 10.5, 'start', INK, 600))
    a(_arr(69, 546, 297, 546)); a(_t(183, 540, '7 1/8 in from the steel, not 4 3/8 in', 11, 'middle', INK, 700))
    for k, ln in enumerate(['On edge, the board sticks out 3 1/2 in, puts the wall', '2 3/4 in further into the room and gives the plywood', 'only a 3/4 in edge to screw to. It is not used this way.']): a(_t(24, 598 + 16 * k, ln, 11.5, 'start', INK))
    # 4. from the room
    a(_t(409, 382, 'Seen from inside the room (plywood off)', 12.5, 'start', INK, 700))
    a(_r(462, 412, 290, 112, RAIL, INK, 1.6)); a(_t(607, 404, 'furring rail, the wide face toward you', 11, 'middle', GR, 600))
    a(_arr(450, 412, 450, 524)); a(_t(444, 472, '3 1/2 in', 11, 'end', INK, 700))
    for x in (478, 734): a(f'<circle cx="{x}" cy="468" r="4.5" fill="#fff" stroke="{INK}" stroke-width="1.4"/>')
    a(_arr(478, 546, 734, 546)); a(_t(606, 540, 'screws about 8 in apart hold the plywood', 11, 'middle', INK, 700))
    for k, ln in enumerate(['From the room, with the plywood off, you see the', 'wide face, 3 1/2 in tall. The plywood is screwed to', 'it, so each sheet lands on a wide board and not on', 'a thin edge.']): a(_t(409, 598 + 16 * k, ln, 11.5, 'start', INK))
    return _svg(780, 676, ''.join(o), 'What laid flat means for a 1x4 furring rail')

def flat_html(FD):
    return ('<h3>What "laid flat" means</h3>'
            '<p>The eight main furring rails are 1x4 boards. A 1x4 measures 3/4 in thick and 3 1/2 in wide. <b>Laid flat</b> means the 3 1/2 in wide face looks into the room, so the board sticks out only 3/4 in from the spacers behind it. The drawing shows the board cut across, the same board laid flat (how it is used), on edge (not used), and as you see it from inside the room.</p>'
            '<figure style="margin:0 0 14px;border:1px solid #d9d5ca;border-radius:8px;padding:8px;background:#fff;min-width:0">' + _flat_svg() + '</figure>')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__)); FD = {}
    exec(open(os.path.join(here, 'shelfdata.py')).read(), FD); exec(open(os.path.join(here, 'furring.py')).read(), FD)
    out = os.path.join(os.path.dirname(here), 'blocks.html')
    open(out, 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Blocks</title><body style="font:16px/1.5 system-ui;max-width:1200px;margin:0 auto;padding:16px">' + flat_html(FD) + block_html(FD) + attach_html(FD) + '</body>')
    print('wrote', out)
