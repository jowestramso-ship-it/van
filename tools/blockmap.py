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
            for x in FD['AP'][n]: out.append((n, x, HT[n], n in FD['LYING']))
        for nm, cx, cz in FD['FRAME_BLK']: out.append((nm, cx, cz, nm in ('J3', 'J4')))
        for nm, cx, cz in FD['NOOK_BLK_D']: out.append((nm, cx, cz, False))
    else:
        for n in ('S4', 'S5', 'S6'):
            for x in FD['PAP'][n]:
                if n == 'S5' and not (31.25 <= x <= 74.5): continue
                out.append((n, x, HT[n], n in FD['LYING']))
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
            left = g == 'V3'                                      # V3's label goes on the counter nook side; V5's goes inside the couch nook, clear of the height numbers
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
            '<p>A block is a 3 1/2 in cut of 2x4, <b>3 5/8 in out</b> with the glue. On <b>S5 and under the frames it stands up: 1 1/2 along the wall x 3 1/2 up</b>. On <b>S4 and S6 it lies on its side: 3 1/2 along the wall x 1 1/2 up</b>, because it sits on the 1 1/2 in strip of steel and the steel next to the strip stands out (1 1/2 in off the body below S4\'s strip, 3 in above S6\'s), so a block standing up would run into it; the window sill and head blocks lie on their side too. Its center sits on the dot, and its vertical center is the furring rail\'s height. Each dark block below shows its distance from the back mark; the tables list the same numbers. S1, S2 and S3 take adhesive pads and S7 and S8 thin shims at their dots, not blocks (the maps and the glossary below the diagrams show all three).</p>' + FD['marks_html']() +
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
    S = 52; X0 = 80; ZB = 392                       # S px per inch; X0 the body side of the drawing; ZB the bottom (27 1/2 in up)
    f = lambda y: X0 + S * (y + 1.4)                  # y: inches out from the steel face of the strip (the 1/8 in strip of steel at 29 1/2 to 31 up)
    Z = lambda z: ZB - S * (z - 27.5)
    BR = '#B45309'; GL = '#8A6A00'; WD = '#5A3A00'
    o = []; a = o.append
    a(_t(20, 24, 'Attaching a block to the steel: a section through one block of S4 (S6 is the same, upside down)', 13.5, 'start', INK, 700))
    a(_t(20, 41, 'the steel of the van on the left, the room on the right; a cut across the wall at a rib, 17 3/4 in from the back mark', 11, 'start', '#5F5E5A'))
    a('<defs><pattern id="hst" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9AA0A8" stroke-width="2"/></pattern></defs>')
    # the steel: the strip (29 1/2 to 31 up) and the rib above it are 1/8 off the body; below the strip the steel stands 1 1/2 off the body (1 3/8 further out)
    pts = [(-1.4, 33), (0, 33), (0, 29.5), (1.375, 29.5), (1.375, 27.5), (-1.4, 27.5)]
    a('<polygon points="' + ' '.join(f'{f(y):.1f},{Z(z):.1f}' for y, z in pts) + '" fill="url(#hst)" stroke="#9AA0A8" stroke-width="1"/>')
    a(_l(f(0), Z(33), f(0), Z(29.5), BR, 3)); a(_l(f(0), Z(29.5), f(1.375), Z(29.5), BR, 3)); a(_l(f(1.375), Z(29.5), f(1.375), Z(27.5), BR, 3))
    a(_t(f(-.7), Z(27.5) + 16, 'outside', 10, 'middle', '#5F5E5A', 600))
    # a block standing up would be 3 1/2 tall: it would run into the steel below the strip (dashed red)
    a(_r(f(.125), Z(32), S * 3.5, S * 3.5, 'none', RED, 1.6, 'stroke-dasharray="6 4"'))
    a(_t(f(1.55), Z(28.0) + 2, 'a block standing up would', 10.5, 'start', RED, 700)); a(_t(f(1.55), Z(28.0) + 14, 'run into the steel here', 10.5, 'start', RED, 700))
    # the real block, lying on its side on the 1 1/2 in strip: 3 1/2 along the wall, 1 1/2 up, 3 1/2 out
    a(_r(f(0), Z(31), S * .125, S * 1.5, '#D4A017', GL, 1))                                       # the bond line
    a(_r(f(.125), Z(31), S * 3.5, S * 1.5, '#C8A878', INK, 1.5))                                  # the block
    for k in range(1, 3): a(_l(f(.125) + 4, Z(31) + S * 1.5 * k / 3, f(3.625) - 4, Z(31) + S * 1.5 * k / 3, '#A8885A', .8))   # the grain, along the wall
    a(_r(f(3.625), Z(32), S * .75, S * 3.5, '#E9D3AA', '#B8975A', 1.3)); a(_r(f(3.625), Z(31), 4, S * 1.5, '#D4A017', GL, .6))   # the furring rail S4 (28 1/2 to 32 up), the wood glue
    a(_r(f(4.375), Z(33), S * .375, S * 5.5, '#F3E7C8', '#B8975A', 1, 'stroke-dasharray="4 3"'))     # the plywood, later
    xh = f(4.375); a(_l(xh, Z(30.25), f(2.9), Z(30.25), RED, 2.4)); a(_r(xh - 3, Z(30.25) - 5, 4, 10, RED, RED, .5))   # the rail's screw
    my = 78
    for xm, top, ch, col in ((f(-.7), Z(33), 'a', BR), (f(.06), Z(31), 'b', GL), (f(1.9), Z(31), 'c', WD), (f(3.625) + 2, Z(31), 'd', GL), (f(4.0), Z(32), 'e', WD), (f(4.56), Z(33), 'g', '#5F5E5A')):
        a(_l(xm, my + 9, xm, top, col, 1.2)); a(_mk(xm, my, ch, col))
    a(_mk(f(2.1), Z(30.25), 'f', RED))
    for k, (xe, lab, yo) in enumerate(((3.625, '3 5/8 in: the block and its glue', 20), (4.375, '4 3/8 in to the face of the furring rail', 48))):
        yd = ZB + 20 + yo - 10; a(_l(f(0), ZB - 20, f(0), yd + 5, '#B4B2A9', .8, '3 3')); a(_l(f(xe), Z(28.5) + 4, f(xe), yd + 5, '#B4B2A9', .8, '3 3'))
        a(_arr(f(0), yd, f(xe), yd)); a(_t(f(xe) + 8 if k else f(0) + 8, yd - 5, lab, 11, 'start', INK, 700 if k == 0 else 600))
    KX = 420; ky = 96
    key = [('a', BR, ['the steel at the dot, the 1/8 in strip: scuffed dull, wiped with', '70/30 alcohol and water, dry. Nothing is screwed into it']),
           ('b', GL, ['bond line, 1/8 in: polyurethane adhesive (Sikaflex-252)', 'or VHB tape (about 110 mil), put on the block']),
           ('c', WD, ['block: a 3 1/2 in cut of 2x4, lying on its side on S4 and S6:', '3 1/2 along the wall, 1 1/2 up (as tall as the strip), 3 1/2 out']),
           ('d', GL, ['wood glue between the block and the furring rail']),
           ('e', WD, ['furring rail S4: 1x4 laid flat, 3/4 x 3 1/2 in (28 1/2 to 32 up)']),
           ('f', RED, ['one #8 x 1 1/2 in screw per block, in a pilot hole']),
           ('g', '#5F5E5A', ['plywood wall, 3/8 in; it goes on later, over the screw heads'])]
    for ch, col, ls in key:
        a(_mk(KX, ky, ch, col))
        for n, ln in enumerate(ls): a(_t(KX + 18, ky + 4 + 15 * n, ln, 11.5, 'start', INK))
        ky += 15 * len(ls) + 17
    for k, ln in enumerate(['On S5 and under the frames the same block stands up (1 1/2 along', 'the wall, 3 1/2 up) on a rib: the steel is flat above and below it.', 'The furring rail\'s back ends up 3 3/4 in off the body either way.']):
        a(_t(KX - 9, ky + 12 + 15 * k, ln, 11, 'start', '#5F5E5A'))
    return _svg(780, 470, ''.join(o), 'Attaching a spacer block to the steel')

ATT_STEPS = [
    '<b>Mark the dots.</b> From the chart above, mark each block\'s place on the steel with a pencil or a bit of tape (its distance from the back mark and its height up). Each one goes on solid steel at the dot, clear of the holes and of the edges of the pans. On S4 and S6 the block lies on the 1 1/2 in strip of steel (29 1/2 to 31 up, and 56 1/2 to 58 up), so mark the strip\'s two edges, not the block\'s height.',
    '<b>Prepare the steel</b> at each mark, a little bigger than the block: remove loose paint and rust; wipe off any oil or wax; scuff lightly with a gray Scotch-Brite pad or 400 grit paper until the paint is evenly dull (if you go through to bare steel, touch it with a rust-inhibiting primer first); vacuum the dust; wipe with a 70/30 mix of isopropyl alcohol and water on a lint-free cloth and dry it with another; do not touch it again.',
    '<b>Prepare the block.</b> Sand the face smooth and wipe off the dust. For VHB tape, also seal the face with a coat of polyurethane and let it dry, because raw wood is porous.',
    '<b>Put the adhesive on the block, not on the steel.</b> Polyurethane adhesive (Sikaflex-252 or similar): a bead round the edge of the 1 1/2 x 3 1/2 in face and one down the middle, enough to leave a 1/8 in bond line when pressed. It works from 50 to 95 F and stays workable for only about 35 minutes at 73 F, so press each block on within that time. VHB tape (about 110 mil, so the 3 1/2 in block plus the tape is the 3 5/8 in standoff): put the tape on the block face first, press it firmly, then peel the liner. Apply it only when the steel, the block and the tape are between 70 and 100 F, never below about 50 F, and with no condensation on the steel.',
    '<b>Set the block on its mark</b>, square to the wall: lying on its side (3 1/2 along the wall, 1 1/2 up) on S4 and S6, standing up (1 1/2 along, 3 1/2 up) on S5 and under the frames, and press it on at once (no sliding it around). Use a furring rail as the gauge: lay one of the furring rail\'s own pieces across the faces of the blocks of that furring rail, with wax paper or plastic wrap between so it does not stick, and press each block against it, so they all end on one line. With VHB press hard, about 15 psi, which on this face is about 79 lb, for a minute, and brace it. With adhesive hold it with masking tape or a prop until it sets. Nothing is screwed into the van body: there are no holes through to the outside.',
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
    a(_r(453, 132, 4, 48, '#D4A017', '#8A6A00', .8)); a(_r(457, 132, 112, 48, '#C8A878', INK, 1.3))
    a(_r(569, 100, 24, 112, RAIL, INK, 1.6)); a(_l(596, 80, 596, 230, GR, 1.2, '4 3'))
    a(_t(606, 92, 'plywood goes here, later', 10.5, 'start', GR))
    a(_t(436, 266, 'steel', 11, 'middle', GR, 600)); a(_t(513, 198, 'spacer (on S4 and S6 it lies on its side)', 10, 'middle', GR, 600))
    a(_t(606, 128, 'wide face,', 12, 'start', INK, 700)); a(_t(606, 143, 'toward the room', 12, 'start', INK, 700))
    a(_arr(668, 156, 598, 156, INK, 1.4)); a(_t(606, 172, 'furring rail:', 11.5, 'start', INK, 600)); a(_t(606, 186, '3/4 in out,', 11.5, 'start', INK)); a(_t(606, 200, '3 1/2 in up', 11.5, 'start', INK))
    a(_arr(569, 226, 593, 226)); a(_t(606, 230, '3/4 in thick', 10.5, 'start', GR))
    for k, ln in enumerate(['Laid flat: the wide face looks into the room and', 'the other wide face sits on the spacers, so the board', 'sticks out only 3/4 in from them.']): a(_t(409, 294 + 16 * k, ln, 11.5, 'start', INK))
    # 3. on edge (not used)
    a(_t(24, 382, 'On edge (NOT used)', 12.5, 'start', RED, 700))
    a(_r(36, 396, 32, 170, 'url(#hst2)', '#9AA0A8', 1)); a(_r(67, 396, 2, 170, '#B45309', '#B45309', .5))
    a(_r(69, 448, 4, 48, '#D4A017', '#8A6A00', .8)); a(_r(73, 448, 112, 48, '#C8A878', INK, 1.3))
    a(_r(185, 460, 112, 24, RAIL, INK, 1.6)); a(_l(300, 396, 300, 566, GR, 1.2, '4 3'))
    a(_t(129, 440, 'spacer', 11, 'middle', GR, 600)); a(_t(52, 579, 'steel', 11, 'middle', GR, 600))
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


# ---------------------------------------------------------------- the couch nook: lining the back, and the sides
PLY = '#E3C48A'; PLYD = '#C9A263'; COV = '#F3E7C8'; RAILC = '#E9D3AA'; GOLD = '#D4A017'
def _hatch(a):
    a('<defs><pattern id="hst3" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9AA0A8" stroke-width="2"/></pattern></defs>')

def _nook_sec(FD):
    import math
    S = 17; X0 = 30; ZB = 760
    Y = lambda y: X0 + S * (y + 1.5); Z = lambda z: ZB - S * (z - 23)
    FACE, D, LN = FD['CN_FACE'], FD['CN_D'], FD['CN_LINE']; OZ0, OZ1 = FD['CN_OZ0'], FD['CN_OZ1']
    SE, SEAT, TOP, TILT = FD['CN_SETOUT'], FD['SEAT_T'], FD['BACK_T'], FD['CN_TILT']
    o = []; a = o.append; _hatch(a)
    a(_t(20, 24, 'The nook seen in section: a cut across the wall at a rib (17 3/4 in from the back mark)', 13.5, 'start', INK, 700))
    a(_t(20, 41, 'steel on the left, the room on the right, the wall coverings and the couch cushion on the right of that', 11, 'start', '#5F5E5A'))
    # the steel at a rib: 1/8 in off the body from 29 1/2 up to 58 (the two strips and the rib), 1 1/2 in off below the strip and 3 in off above S6's strip
    pts = [(-1.5, 60), (3, 60), (3, 58), (.125, 58), (.125, 29.5), (1.5, 29.5), (1.5, 23), (-1.5, 23)]
    a('<polygon points="' + ' '.join(f'{Y(y):.1f},{Z(z):.1f}' for y, z in pts) + '" fill="url(#hst3)" stroke="#9AA0A8" stroke-width="1"/>')
    a('<polyline points="' + ' '.join(f'{Y(y):.1f},{Z(z):.1f}' for y, z in pts[1:7]) + '" fill="none" stroke="#B45309" stroke-width="3" stroke-linejoin="round"/>')
    # the wall coverings (3/8 in plywood) below 32 and above 55 1/2, the rails on their blocks
    a(_r(Y(4.5), Z(32), S * .375, S * 9, COV, '#B8975A', 1)); a(_r(Y(4.5), Z(60), S * .375, S * 4.5, COV, '#B8975A', 1))
    for z0, z1, bz0, bz1 in ((28.5, 32, 29.5, 31), (55.5, 59, 56.5, 58)):
        a(_r(Y(.125), Z(bz1), S * .125, S * 1.5, GOLD, '#8A6A00', .8)); a(_r(Y(.25), Z(bz1), S * 3.5, S * 1.5, '#C8A878', INK, 1.2))
        a(_r(Y(3.75), Z(z1), S * .75, S * (z1 - z0), RAILC, '#B8975A', 1.3))
    # the lining on the rib, the floor on S4, the ceiling under S6
    a(_r(Y(.1), Z(OZ1 - .0625), S * .03, S * (OZ1 - OZ0 - .125), GOLD, GOLD, 1))
    a(_r(Y(.125), Z(OZ1 - .0625), S * LN, S * (OZ1 - OZ0 - .125), PLY, INK, 1.2))
    a(_r(Y(.125 + LN), Z(OZ0 + LN), S * D, S * LN, PLY, INK, 1.2)); a(_r(Y(.125 + LN), Z(OZ1), S * D, S * LN, PLY, INK, 1.2))
    # the back cushion, tilted: its base stands SE out from the wall face so that its rear edge is at the face at the bottom of the opening
    t = 5 / math.cos(math.radians(TILT)); tn = math.tan(math.radians(TILT)); rb = FACE + SE
    poly = [(rb, SEAT), (rb + t, SEAT), (rb + t - 20 * tn, SEAT + 20), (rb - 20 * tn, SEAT + 20)]
    a('<polygon points="' + ' '.join(f'{Y(y):.1f},{Z(z):.1f}' for y, z in poly) + '" fill="#F2B84B" fill-opacity=".5" stroke="#8A5A00" stroke-width="1.8" stroke-dasharray="6 3"/>')
    a(_t(Y(rb + 2.2), Z(SEAT + 8), 'back cushion', 11, 'middle', WD := '#5A3A00', 700)); a(_t(Y(rb + 2.2), Z(SEAT + 8) + 14, f'tilted {TILT:g} degrees', 10.5, 'middle', '#5A3A00'))
    a(_l(Y(-1.5), Z(SEAT), Y(13), Z(SEAT), '#9A9DA3', 1, '3 3')); a(_t(Y(12.9), Z(SEAT) - 4, 'seat 23 1/2', 10, 'end', '#5F5E5A'))
    # the depth, and the opening
    a(_arr(Y(.125 + LN), Z(46), Y(FACE), Z(46))); a(_t(Y((.125 + LN + FACE) / 2), Z(46) - 6, '4 1/2 in deep' if abs(D - 4.5) < .01 else f'{D:g} in deep', 11, 'middle', INK, 700))
    a(_l(Y(FACE), Z(OZ0) + 3, Y(FACE) + 22, Z(OZ0) + 3, '#534AB7', 1, '3 3')); a(_l(Y(FACE), Z(OZ1) - 3, Y(FACE) + 22, Z(OZ1) - 3, '#534AB7', 1, '3 3'))
    # the labels, each at its own height to the right of the cushion, with a leader to the part
    LX = Y(13.2)
    lab = [(59.6, 'covering', ['the 3/8 in plywood walls, cut at 32 and 55 1/2'], (4.7, 59.3), '#5F5E5A'),
           (57.4, 'S6', ['furring rail S6 (55 1/2 to 59 up) on its block, which lies on the 1 1/2 in strip (56 1/2 to 58)'], (4.1, 57.6), WD),
           (55.5, 'ceiling', ['1/4 in plywood under S6: glued to the back, screwed up into S6'], (3.0, 55.4), WD),
           (53.2, 'steel', ['the rib, 1/8 in off the body (above S6\'s strip the steel is 3 in off)'], (-.5, 53.2), '#B45309'),
           (50.7, 'lining', ['1/4 in plywood back, 23 3/8 tall, on the ribs'], (.25, 50.7), WD),
           (48.2, 'glue', ['polyurethane adhesive on the rib, never screws into the steel'], (.11, 48.2), '#8A6A00'),
           (32.9, 'floor', ['1/4 in plywood on top of S4 and the covering\'s edge: glued to the back, screwed down into S4'], (3.0, 32.12), WD),
           (30.3, 'S4', ['furring rail S4 (28 1/2 to 32 up) on its block, lying on the strip (29 1/2 to 31)'], (4.1, 30.0), WD),
           (26.6, 'step', ['below the strip the steel stands 1 1/2 in off the body'], (1.2, 26.6), '#B45309')]
    for z, ttl, ls, (py, pz), col in lab:
        a(_l(LX - 6, Z(z), Y(py), Z(pz), col, .9)); a(f'<circle cx="{Y(py):.1f}" cy="{Z(pz):.1f}" r="2.2" fill="{col}"/>')
        a(_t(LX, Z(z) - 2, ttl, 11.5, 'start', col, 700))
        for k, ln in enumerate(ls): a(_t(LX, Z(z) + 12 + 12 * k, ln, 10.5, 'start', INK))
    a(_t(Y(-.7), Z(23) + 16, 'outside', 10, 'middle', '#5F5E5A', 600))
    return _svg(900, 800, ''.join(o), 'The couch nook in section')

def _nook_room(FD):
    S = 11.4; X0 = 52; ZB = 448
    X = lambda x: X0 + S * x; Z = lambda z: ZB - S * (z - 28)
    OX0, OX1, OZ0, OZ1 = FD['CN_X0'], FD['CN_X1'], FD['CN_OZ0'], FD['CN_OZ1']; LN = FD['CN_LINE']
    o = []; a = o.append; _hatch(a)
    a(_t(20, 24, 'The nook seen from the room with the wall covering off: the five plywood pieces', 13.5, 'start', INK, 700))
    a(_t(20, 41, 'the lining is behind the floor, the ceiling and the sides; the rails and frames are drawn as they are fixed to the steel', 11, 'start', '#5F5E5A'))
    # the steel angle at the lower rear corner (it stands 1 1/2 in off the body)
    a('<polygon points="' + ' '.join(f'{X(x):.1f},{Z(z):.1f}' for x, z in ((3, 36.7), (6, 36.7), (10.1, 32), (3, 32))) + '" fill="url(#hst3)" stroke="#9A9DA3" stroke-width="1"/>')
    # the lining with its notch
    pts = [(OX0 + 6, 32.0625), (OX1, 32.0625), (OX1, 55.4375), (OX0, 55.4375), (OX0, 32.0625 + 4.75), (OX0 + 6, 32.0625 + 4.75)]
    a('<polygon points="' + ' '.join(f'{X(x):.1f},{Z(z):.1f}' for x, z in pts) + f'" fill="{PLY}" fill-opacity=".9" stroke="{INK}" stroke-width="1.4"/>')
    # the ribs the lining is glued to (dashed), from the depth map of the steel
    for r0, r1 in ((5, 6), (16, 19.5), (29.75, 32.75), (43, 46), (56.25, 61), (69.625, 73)):
        a(_r(X(r0), Z(55.4), S * (r1 - r0), S * 23.3, GOLD, '#8A6A00', 1, 'fill-opacity=".22" stroke-dasharray="4 3"'))
    a(_t(X(24.5), Z(53.3), 'the ribs (shaded): two beads of adhesive on each', 11, 'middle', '#8A6A00', 700))
    # the rails and frames (tan) around the opening
    for z0, z1, nm in ((28.5, 32, 'S4'), (55.5, 59, 'S6')):
        a(_r(X(0), Z(z1), S * 80, S * (z1 - z0), RAILC, '#B8975A', 1.2, 'fill-opacity=".8"')); a(_t(X(1.2), Z((z0 + z1) / 2) + 4, nm, 11, 'start', WD := '#5A3A00', 700))
    for x0, x1, nm in ((OX0 - 1.5, OX0, 'V5'), (OX1, OX1 + 1.5, 'V6')):
        a(_r(X(x0), Z(OZ1), S * (x1 - x0), S * (OZ1 - OZ0), RAILC, '#B8975A', 1.2)); a(_t(X((x0 + x1) / 2), Z(OZ1) - 5, nm, 10.5, 'middle', '#5A3A00', 700))
    # the floor, the ceiling and the two sides (1/4 in, drawn a little thick)
    th = .36
    a(_r(X(OX0), Z(OZ0 + th), S * (OX1 - OX0), S * th, PLYD, INK, 1.2)); a(_r(X(OX0), Z(OZ1), S * (OX1 - OX0), S * th, PLYD, INK, 1.2))
    a(_r(X(OX0), Z(OZ1 - th), S * th, S * (OZ1 - OZ0 - 2 * th), PLYD, INK, 1.2)); a(_r(X(OX1 - th), Z(OZ1 - th), S * th, S * (OZ1 - OZ0 - 2 * th), PLYD, INK, 1.2))
    a(_r(X(OX0), Z(OZ1), S * (OX1 - OX0), S * (OZ1 - OZ0), 'none', '#534AB7', 1.6, 'stroke-dasharray="7 4"'))
    # the pieces, lettered
    for x, z, ch, col in ((OX0 + 38, 44, 'A', INK), (OX0 + 38, OZ0 + .13, 'B', INK), (OX0 + 38, OZ1 - .18, 'C', INK), (OX0 + .12, 46, 'D', INK)):
        a(_mk(X(x), Z(z), ch, col))
    # dimensions
    a(_arr(X(OX0), Z(61), X(OX1), Z(61))); a(_t(X((OX0 + OX1) / 2), Z(61) - 6, f'{OX1 - OX0:g} in: the opening, and the back (A) is the same width', 11, 'middle', INK, 700))
    a(_l(X(OX0), Z(61) + 4, X(OX0), Z(OZ1) - 14, '#B4B2A9', .8, '3 3')); a(_l(X(OX1), Z(61) + 4, X(OX1), Z(OZ1) - 14, '#B4B2A9', .8, '3 3'))
    a(_arr(X(-2.6), Z(OZ0), X(-2.6), Z(OZ1))); a(f'<text transform="translate({X(-2.6) - 6:.1f},{Z(44):.1f}) rotate(-90)" text-anchor="middle" style="font-size:10.5px;font-weight:700;fill:{INK}">23 1/2 in</text>')
    a(_l(X(-3), Z(OZ0), X(OX0 - 1.8), Z(OZ0), '#B4B2A9', .8, '3 3')); a(_l(X(-3), Z(OZ1), X(OX0 - 1.8), Z(OZ1), '#B4B2A9', .8, '3 3'))
    a(_arr(X(OX0), Z(36.8125) + 0, X(OX0 + 6), Z(36.8125))); a(_t(X(OX0 + 3), Z(36.8125) - 5, '6 in', 10, 'middle', INK, 700))
    a(_t(X(OX0 + 6.4), Z(35), 'notch 6 x 4 3/4 where the steel', 10.5, 'start', '#5F5E5A', 600)); a(_t(X(OX0 + 6.4), Z(35) + 12, 'angle is 1 1/2 in off the body', 10.5, 'start', '#5F5E5A', 600))
    for k, ln in enumerate(['A  the back: 1/4 in plywood, 69 x 23 3/8, with the notch', 'B  the floor: 69 x 4 1/2, on top of S4 and the covering\'s edge', 'C  the ceiling: 69 x 4 1/2, under S6', 'D  the two sides: 23 x 4 1/2 each, one at each end against V5 and V6']): a(_t(X(24), Z(26.2) + 15 * k, ln, 11.5, 'start', INK, 600))
    return _svg(1000, 540, ''.join(o), 'The couch nook from the room, with the pieces')

def _nook_ends(FD):
    S = 30; ZH = 44
    FACE, LN = FD['CN_FACE'], FD['CN_LINE']; OX0, OX1 = FD['CN_X0'], FD['CN_X1']
    o = []; a = o.append; _hatch(a)
    a(_t(20, 24, 'The two sides of the nook, seen from above: a cut across the wall at 44 in up', 13.5, 'start', INK, 700))
    a(_t(20, 41, 'steel at the top, the room below; the rear end on the left, the front end on the right (they are 69 in apart)', 11, 'start', '#5F5E5A'))
    def end(ox, x0, prof, nm, vx0, vx1, bz, sx, lx0, lx1, ribs, covx, note, pan):
        X = lambda x: ox + S * (x - x0); Yq = lambda y: 95 + S * y
        # the steel above, with its profile: ribs 1/8 off the body, pans at 0
        pts = [(prof[0][0], -.8)] + [(x, yy) for x, yy in prof] + [(prof[-1][0], -.8)]
        a('<polygon points="' + ' '.join(f'{X(x):.1f},{Yq(y):.1f}' for x, y in pts) + '" fill="url(#hst3)" stroke="#9A9DA3" stroke-width="1"/>')
        a('<polyline points="' + ' '.join(f'{X(x):.1f},{Yq(y):.1f}' for x, y in prof) + '" fill="none" stroke="#B45309" stroke-width="2.6"/>')
        # the lining on the ribs (it bridges the pans), the glue
        a(_r(X(lx0), Yq(.125), S * (lx1 - lx0), S * LN, PLY, INK, 1.2))
        for r in ribs: a(_r(X(r) - 3, Yq(.125) - 3, 6, 4, GOLD, '#8A6A00', .6))
        # the frame V with its block, the side, the covering
        a(_r(X(bz[0]), Yq(.25), S * (bz[1] - bz[0]), S * 3.5, '#C8A878', INK, 1.2)); a(_r(X(vx0), Yq(3.75), S * (vx1 - vx0), S * .75, RAILC, '#B8975A', 1.3))
        a(_r(X(sx), Yq(.125 + LN), S * LN, S * (FACE - .125 - LN), PLYD, INK, 1.3))
        a(_r(X(covx[0]), Yq(4.5), S * (covx[1] - covx[0]), S * .375, COV, '#B8975A', 1.2))
        a(_t(X(x0) + 4, 78, nm, 12.5, 'start', INK, 700))
        return X, Yq
    # the rear end: V5 at 3 1/2 to 5, its block, the side at 5 to 5 1/4, the covering to the left of 5, the rib at 3 to 6 and the pan P1 from 6
    X, Yq = end(40, 2, [(2, .125), (6, .125), (6, 0), (11.5, 0)], 'rear end, at 5 in', OX0 - 1.5, OX0, (OX0 - 1.5, OX0), OX0, OX0, 11.5, (5.5,), (2, OX0), '', False)
    a(_t(X(2) + 4, Yq(5.65), 'covering', 10.5, 'start', '#5F5E5A', 600))
    # the front end: V6 at 74 to 75 1/2 over the pan P6, the lining to 74, the side at 73 3/4 to 74, the covering to the right of 74, the rib at 69 5/8 to 73
    X2, Y2 = end(520, 68, [(68, 0), (69.625, 0), (69.625, .125), (73, .125), (73, 0), (79.5, 0)], 'front end, at 74 in', OX1, OX1 + 1.5, (OX1, OX1 + 1.5), OX1 - LN, 68, OX1, (70.3, 72.4), (OX1, 79.5), '', True)
    a(_t(X2(79.5) - 4, Y2(5.65), 'covering', 10.5, 'end', '#5F5E5A', 600))
    # markers on the parts, and a key under each end
    a(_mk(X(5.62 + 1.2), Yq(.25), 'A', INK)); a(_mk(X(OX0 + LN / 2), Yq(2.4), 'D', INK))
    a(_t(X(OX0 - .75), Yq(2.1), 'block', 10, 'middle', '#5A3A00', 600)); a(_t(X(OX0 - .75), Yq(4.12), 'V5', 10, 'middle', '#5A3A00', 700))
    a(_mk(X2(70.0), Y2(.25), 'A', INK)); a(_mk(X2(OX1 - LN / 2), Y2(2.4), 'D', INK))
    a(_t(X2(OX1 + .75), Y2(2.1), 'block', 10, 'middle', '#5A3A00', 600)); a(_t(X2(OX1 + .75), Y2(4.12), 'V6', 10, 'middle', '#5A3A00', 700))
    a(_t(X2(70.3), Y2(.125) - 8, 'glue', 10, 'middle', '#8A6A00', 700))
    a(_arr(X(11.0), Yq(.375), X(11.0), Yq(FACE))); a(_t(X(11.0) + 6, Yq(2.6), '4 1/2', 10.5, 'start', INK, 700)); a(_t(X(11.0) + 6, Yq(2.6) + 12, 'in', 10.5, 'start', INK, 700))
    key1 = ['A  the lining, glued to the rib; over the pan it spans 1/8 in off the steel', 'D  the side: glued to the edge of A, to the floor, the ceiling and the frame,', '    and 1 in brads through it into V5 (the frame is 3/4 thick)', 'the covering stops at 5 in; the side\'s 1/4 in front edge shows beside it']
    key2 = ['A  the lining, to 74 in; the glue is on the rib at 69 5/8 to 73', 'D  the side at 73 3/4 to 74, against V6 (which stands over the pan P6:', '    the block\'s glue line is 1/8 in thicker there, check it sits flat)', 'the covering starts at 74 in: edge band or a nosing on the 1/4 in edge']
    for k, ln in enumerate(key1): a(_t(40, 282 + 14 * k, ln, 10.5, 'start', INK, 600 if k in (0, 1) else 400))
    for k, ln in enumerate(key2): a(_t(520, 282 + 14 * k, ln, 10.5, 'start', INK, 600 if k in (0, 1) else 400))
    return _svg(1000, 350, ''.join(o), 'The two sides of the couch nook from above')

NOOK_PARTS = [
 ('A', 'Back (lining)', '1/4 in plywood, birch, one good face', '69 x 23 3/8, with a 6 x 4 3/4 notch at the lower rear corner', '1', 'glued to the ribs; 1/8 in shorter than the 23 1/2 in gap between S4 and S6 so it goes in without forcing'),
 ('B', 'Floor', '1/4 in plywood, same sheet', '69 x 4 1/2', '1', 'on top of S4 (its top edge is at 32 up) and of the covering\'s top edge; back edge against the face of A; ends at x = 5 and 74'),
 ('C', 'Ceiling', '1/4 in plywood, same sheet', '69 x 4 1/2', '1', 'under S6 (its bottom edge is at 55 1/2 up); back edge against the face of A'),
 ('D', 'Sides', '1/4 in plywood, same sheet', '23 x 4 1/2', '2', 'one at each end, between B and C, against the inside face of V5 (at 5 in) and V6 (at 74 in); 23 = 23 1/2 less the floor and the ceiling'),
 ('', 'Adhesive', 'polyurethane construction adhesive (or the same Sikaflex-252 as the blocks)', '', '2 tubes', 'two beads down each rib for A, and a bead on each joint for B, C and D; wipe the squeeze-out before it skins'),
 ('', 'Screws and brads', '#6 x 1 1/4 in screws; 1 in brads', 'about 20 screws and 24 brads', '', 'screws every 8 in through B down into S4 and through C up into S6, pilot holes, countersunk; brads every 4 in through each side into its frame'),
 ('', 'Finish', 'sealer and clear finish or paint; iron-on veneer edge tape', 'about 16 ft of tape', '', 'finish every piece on both faces before it goes in; the tape covers the 1/4 in front edges of B, C and D (69 + 69 + 23 + 23 in)'),
]
NOOK_STEPS = [
 '<b>Cut the five pieces</b> from one 4 x 8 sheet of 1/4 in plywood (the sizes are in the table): the back A 69 x 23 3/8 in, the floor B and the ceiling C 69 x 4 1/2 in each, and the two sides D 23 x 4 1/2 in each. Cut the 6 x 4 3/4 in notch in A\'s lower rear corner: mark it from the real steel, because the angle there stands 1 1/2 in off the body (up to 36 3/4 in at 3 to 6 in along, sloping down to 31 up at 11 in), and a flat sheet cannot lie on it.',
 '<b>Finish every piece before it goes in:</b> sand, and seal and finish (or paint) both faces and all edges. The nook is hard to reach once it is built, and the plywood walls are not on yet.',
 '<b>Mark the ribs on the steel.</b> The lining sits on the ribs, the 3 in strips between the pans that stand 1/8 in off the body: from the back mark they are at 5 to 6, 16 to 19 1/2, 29 3/4 to 32 3/4, 43 to 46, 56 1/4 to 61 and 69 5/8 to 73. The pans between them are 1/8 in lower and the lining bridges them. Scuff and clean the ribs as for the blocks. Do this when S4, S6, V5 and V6 are on and S5 is out of the way, before the plywood walls.',
 '<b>Fit the back dry.</b> Slide A in from the front between S4 and S6 and press it on the ribs: it should lie flat on all of them, with the notch clear of the angle. Trim the notch to the steel.',
 '<b>Glue the back to the ribs.</b> Put two beads of adhesive down each rib (not on the pans), press A on, and hold it with painter\'s tape to S4 and S6 and a few light props for a day. Nothing is screwed into the van\'s body.',
 '<b>The floor.</b> Lay B on top of S4 with its back edge against the face of A, glue it to A and to S4, and screw it down into S4 every 8 in, 3/4 in from the front edge (pilot holes, countersunk). Its front edge ends flush with the face of the walls.',
 '<b>The ceiling.</b> The same under S6: glue C to A and to S6\'s underside and screw it up into S6 every 8 in.',
 '<b>The sides.</b> Fit each D between the floor and the ceiling at the end of the nook, against the inside face of V5 (at 5 in) or V6 (at 74 in). Glue its edges to A, B and C and its back face to the frame, and nail it with 1 in brads every 4 in, through D and into the frame, which is 3/4 in thick. Wipe the glue off at once.',
 '<b>The covering.</b> Cut the opening in the 3/8 in plywood sheets at 5 to 74 in along and 32 to 55 1/2 in up, so the edges of the walls meet the outside faces of D, B and C, and finish the 1/4 in front edges of B, C and D with iron-on veneer tape or a thin nosing (the Walls page has the edge details).',
 '<b>Try the cushion:</b> with the back cushion tilted 12 degrees, its base stands 1 13/16 in out from the wall and its top edge goes about 2 1/2 in into the nook, leaving about 2 in behind it.',
]
def nook_html(FD):
    pt = '<table class="rt"><tr><th>#</th><th>Part</th><th>Material</th><th>Size (in)</th><th>Qty</th><th>Notes</th></tr>' + ''.join(f'<tr><td>{a1}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td><td>{f}</td></tr>' for a1, b, c, d, e, f in NOOK_PARTS) + '</table>'
    st = '<ol class="steps">' + ''.join(f'<li>{x}</li>' for x in NOOK_STEPS) + '</ol>'
    fig = lambda svg: '<figure style="margin:0 0 14px;border:1px solid #d9d5ca;border-radius:8px;padding:8px;background:#fff;min-width:0">' + svg + '</figure>'
    return ('<h3>The couch nook: the plywood lining and the sides</h3>'
            '<p>The nook behind the couch is lined with 1/4 in plywood, all cut from one sheet: a <b>back</b> glued to the ribs of the steel, a <b>floor</b> on top of S4, a <b>ceiling</b> under S6, and a <b>side</b> at each end against the frames V5 and V6. The lining keeps the cushion off the bare steel and closes the gap behind the rails (S4 and S6 stand 3 3/4 in off the body, so without a floor and a ceiling the nook would open into the wall cavity). It leaves the nook ' + f"{FD['CN_D']:g}" + ' in deep from the face of the walls to the back, which is the number the cushion\'s tilt was worked out for.</p>'
            + fig(_nook_sec(FD)) + fig(_nook_room(FD)) + fig(_nook_ends(FD))
            + '<p><b>Parts</b> (the letters are on the second drawing):</p><div class="wide">' + pt + '</div><p><b>How to build it, in order:</b></p>' + st)

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__)); FD = {}
    exec(open(os.path.join(here, 'shelfdata.py')).read(), FD); exec(open(os.path.join(here, 'furring.py')).read(), FD)
    out = os.path.join(os.path.dirname(here), 'blocks.html')
    open(out, 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Blocks</title><body style="font:16px/1.5 system-ui;max-width:1200px;margin:0 auto;padding:16px">' + flat_html(FD) + block_html(FD) + attach_html(FD) + nook_html(FD) + '</body>')
    print('wrote', out)
