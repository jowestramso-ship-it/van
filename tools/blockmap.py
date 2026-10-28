"""The block placement chart of the Furring page of the build guide: where every spacer block goes on the driver wall and on the passenger wall (a block is 1 1/2 along the wall x 3 1/2 up, 3 5/8 out with the glue),
each marked with its distance from the back mark, and a table by strip. It only draws what the furring maps already hold (AP, PAP, FRAME_BLK, VFR, WIN_FRAME, HT in furring.py), so the chart and the maps cannot disagree.
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
    # the strips S1 to S8 (3 1/2 wide), pale, with the segments each really has
    SEG = FD['SEG_D'] if not flip else FD['SEG_P']
    for n, h in HT.items():
        for x0, x1 in SEG[n]:
            xa, xb = sorted((xx(x0), xx(x1)))
            a(_r(xa, yy(h + FD['STRIP_W'] / 2), xb - xa, S * FD['STRIP_W'], STRIP, '#B8975A', 1))
        a(_t(xx(2) if not flip else xx(W - 2) , yy(h) + 3.5, n, 10, 'middle', '#5A3A00', 700))
    # the wheel well, the window, the sliding door, the nooks
    a(_r(xx(42) if not flip else xx(76), yy(7.5), S * 34, S * 7.5, '#D8B79A', '#8A6B4D', 1, 'fill-opacity=".7" stroke-dasharray="4 3"')); a(_t(xx(59), yy(3.2), 'wheel well', 9.5, 'middle', '#5A3A00'))
    if not flip:
        wx0, wx1, wz0, wz1 = FD['WIN_CX0'], FD['WIN_CX1'], FD['WIN_CZ0'], FD['WIN_CZ1']
        a(_r(xx(wx0), yy(wz1), S * (wx1 - wx0), S * (wz1 - wz0), '#B5D4F4', BLU, 1.4, 'fill-opacity=".35"')); a(_t(xx((wx0 + wx1) / 2), yy((wz0 + wz1) / 2) + 3, 'side window cutout', 10, 'middle', BLU, 600))
        for nm, x0, x1, z0, z1 in FD['WIN_FRAME']:
            a(_r(xx(x0), yy(z1), S * (x1 - x0), S * (z1 - z0), '#E9D3AA', '#B8975A', 1, 'fill-opacity=".9"'))
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
            n = sum(1 for gg, *_ in bl[:k] if gg == g)                  # alternate the labels below and above the strip so close blocks do not touch
            ty = yy(z) + S * 1.75 + 10 if n % 2 == 0 else yy(z) - S * 1.75 - 4
            a(_t(xx(x), ty, fr16(x), 8.5, 'middle', '#3E230B', 700))
        elif g in ('J1', 'J2'):                                         # a window jamb: its height up, inside the cutout so the strips' labels stay clear
            left = (g == 'J1') != flip
            a(_t(xx(x) + (S * 2.4 if left else -S * 2.4), yy(z) + 3, g + ' ' + fr16(z) + ' up', 8.5, 'start' if left else 'end', '#3E230B', 700))
        elif fl:                                                        # the sill and the head: the distance along, below the sill and above the head
            a(_t(xx(x), yy(z) + (S * 1.8 + 9 if g == 'J3' else -S * 1.8 - 3), fr16(x), 8.5, 'middle', '#3E230B', 700))
        else:                                                           # a nook frame: its name and height up, beside it (V3's on the counter nook side)
            a(_t(xx(x) + (-S * 2.1 if g == 'V3' else S * 2.1), yy(z) + 3, g + ' ' + fr16(z) + ' up', 8.5, 'end' if g == 'V3' else 'start', '#3E230B', 700))
    return _svg(1100, 610, ''.join(o), f'Where every spacer block goes on the {"driver" if not flip else "passenger"} wall'), bl

def _svg(w, h, body, title):
    return f'<svg viewBox="0 0 {w} {h}" role="img" style="width:100%;height:auto;display:block;background:#fff;border-radius:6px"><title>{title}</title>{body}</svg>'

def _table(FD, side, bl):
    fr16, fr8, HT = FD['fr16'], FD['fr8'], FD['HT']
    rows = []
    for g in ('S4', 'S5', 'S6', 'J1', 'J2', 'J3', 'J4', 'V1', 'V2', 'V3'):
        it = [(i, x, z) for gg, i, x, z, fl in bl if gg == g]
        if not it: continue
        if g in HT: what = f'strip {g}, {fr8(HT[g])} up'
        elif g.startswith('J'): what = {'J1': 'window frame, left jamb', 'J2': 'window frame, right jamb', 'J3': 'window frame, sill', 'J4': 'window frame, head'}[g]
        else: what = {'V1': 'shower nook rear frame', 'V2': 'shower nook front frame', 'V3': 'counter nook rear frame'}[g]
        if g in HT or g in ('J3', 'J4'): pos = ', '.join(fr16(x) for _i, x, _z in it)
        else: pos = f'{fr16(it[0][1])} in from the back, at ' + ', '.join(fr16(z) for _i, _x, z in it) + ' in up'
        rows.append(f'<tr><td><b>{g}</b></td><td>{what}</td><td>{len(it)}</td><td>{pos}</td></tr>')
    return '<div class="wide"><table class="rt"><tr><th>Where</th><th>What it holds</th><th>Blocks</th><th>Positions, in from the back mark (strips and sill/head), or the heights up for a frame</th></tr>' + ''.join(rows) + '</table></div>'

CSS = '<style>.bmap{margin:10px 0 18px}.bmap figure{margin:0 0 10px;border:1px solid #d9d5ca;border-radius:8px;padding:8px;background:#fff;min-width:0}.bmap figcaption{font-size:14px;line-height:1.45;margin-top:6px}</style>'

def block_html(FD):
    d, bd = _map(FD, 'D'); p, bp = _map(FD, 'P')
    return (CSS + '<h3>Where every spacer block goes (' + str(len(bd) + len(bp)) + ' blocks)</h3>'
            '<p>A block is a 3 1/2 in cut of 2x4 stood on its 3 1/2 in side: <b>1 1/2 along the wall x 3 1/2 up</b> on the steel, <b>3 5/8 in out</b> with the glue. Its center sits on the dot, and its vertical center is the strip\'s height (the window sill and head blocks lie on their side). Each dark block below shows its distance from the back mark; the tables list the same numbers. S1, S2 and S3 take adhesive pads and S7 and S8 thin shims at their dots, not blocks.</p>'
            '<div class="bmap"><figure>' + d + f'<figcaption><b>Driver wall: {len(bd)} blocks</b> (S4, S5 and S6 at their dots, and three under each of the four window frame pieces).</figcaption></figure>' + _table(FD, 'D', bd) +
            '<figure style="margin-top:14px">' + p + f'<figcaption><b>Passenger wall: {len(bp)} blocks</b> (S4, S6, the middle piece of S5, and three under each nook frame V1 to V3; V4 sits straight on the steel).</figcaption></figure>' + _table(FD, 'P', bp) + '</div>')

if __name__ == '__main__':
    here = os.path.dirname(os.path.abspath(__file__)); FD = {}
    exec(open(os.path.join(here, 'shelfdata.py')).read(), FD); exec(open(os.path.join(here, 'furring.py')).read(), FD)
    out = os.path.join(os.path.dirname(here), 'blocks.html')
    open(out, 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Blocks</title><body style="font:16px/1.5 system-ui;max-width:1200px;margin:0 auto;padding:16px">' + block_html(FD) + '</body>')
    print('wrote', out)
