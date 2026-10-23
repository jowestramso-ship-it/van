#!/usr/bin/env python3
"""Builds ../install.html: an illustrated step-by-step for the roof fan and the air conditioner.
Every number comes from the plan (interactive.html): openings, rib positions, frame cut lists, the fan's depth range.
Run from this folder (build.sh does):  python3 install.py
"""
import os, html

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- numbers from the plan (inches)
RIBS = [21.75, 37.875, 58.375, 97.375, 126.375]     # the edge of each rib nearest the rear doors, from the rear-door edge
RIBW = 2.75
RIBD = 2.0
FAN = dict(x=13.25, y=34.0, w=14.0, unit=17.75)
AC = dict(x=49.5, y=34.0, w=14.25, unit=28.25)
VAN_L, VAN_W = 160.0, 68.0
COV = 3 / 16 + 3 / 4                       # the ceiling covering: 3/16 in plywood against the roof, then 3/4 in slats
FRAME = RIBD + COV                         # frame depth = rib hang + covering = roof steel to the finished ceiling
STEEL = 1 / 16                             # the roof skin itself, about
STACK = FRAME + STEEL                      # steel to the trim
FAN_MIN, FAN_MAX = 2.75, 4.5               # roof to trim range the owner measured on the fan


def fr(v):
    """inches as a mixed number: 13.25 -> 13 1/4"""
    w = int(v + 1e-9)
    r = round((v - w) * 16)
    if r == 16:
        w, r = w + 1, 0
    num, den = r, 16
    while num and num % 2 == 0:
        num //= 2
        den //= 2
    if not num:
        return str(w)
    return (f'{w} ' if w else '') + f'{num}/{den}'


# ---------------------------------------------------------------- small svg helpers
def svg(w, h, body, title):
    return f'<svg class="fig" viewBox="0 0 {w} {h}" role="img" aria-label="{html.escape(title)}"><title>{html.escape(title)}</title>{body}</svg>'


def R(x, y, w, h, cls='', rx=0, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" rx="{rx}" class="{cls}" {extra}/>'


def L(x1, y1, x2, y2, cls='ln', extra=''):
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" class="{cls}" {extra}/>'


def C(x, y, r, cls=''):
    return f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r}" class="{cls}"/>'


def T(x, y, s, cls='t', anchor='middle'):
    return f'<text x="{x:.1f}" y="{y:.1f}" class="{cls}" text-anchor="{anchor}">{html.escape(s)}</text>'


def P(pts, cls=''):
    return '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" class="{cls}"/>'


def PL(pts, cls='ln'):
    return '<polyline points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" class="{cls}" fill="none"/>'


def dimh(x1, x2, y, label, up=True, cls='dim'):
    """horizontal dimension line with end ticks and a label above (or below)"""
    ty = y - 4 if up else y + 12
    return (L(x1, y, x2, y, cls) + L(x1, y - 4, x1, y + 4, cls) + L(x2, y - 4, x2, y + 4, cls) +
            T((x1 + x2) / 2, ty, label, 'tdim'))


def dimv(x, y1, y2, label, left=True, cls='dim'):
    tx = x - 5 if left else x + 5
    return (L(x, y1, x, y2, cls) + L(x - 4, y1, x + 4, y1, cls) + L(x - 4, y2, x + 4, y2, cls) +
            f'<text x="{tx:.1f}" y="{(y1 + y2) / 2 + 4:.1f}" class="tdim" text-anchor="{"end" if left else "start"}">{html.escape(label)}</text>')


def arrow(x1, y1, x2, y2, cls='arr'):
    import math
    a = math.atan2(y2 - y1, x2 - x1)
    h = 7
    p1 = (x2 - h * math.cos(a - .4), y2 - h * math.sin(a - .4))
    p2 = (x2 - h * math.cos(a + .4), y2 - h * math.sin(a + .4))
    return L(x1, y1, x2, y2, cls) + P([(x2, y2), p1, p2], 'arrhead')


# ---------------------------------------------------------------- the drawings
def fig_overview():
    S, X0, Y0 = 3.2, 26, 40
    X = lambda x: X0 + S * x
    Y = lambda y: Y0 + S * y
    W, H = int(X(VAN_L) + 24), int(Y(VAN_W) + 50)
    o = [R(X(0), Y(0), S * VAN_L, S * VAN_W, 'roofbox')]
    for r in RIBS:
        o.append(R(X(r), Y(0), S * RIBW, S * VAN_W, 'rib'))
        o.append(T(X(r) + S * RIBW / 2, Y(0) - 5, fr(r), 'tsm'))
    for nm, d in (('FAN', FAN), ('A/C', AC)):
        u = d['unit']
        o.append(R(X(d['x'] - u / 2), Y(d['y'] - u / 2), S * u, S * u, 'unit'))
        o.append(R(X(d['x'] - d['w'] / 2), Y(d['y'] - d['w'] / 2), S * d['w'], S * d['w'], 'hole'))
        o.append(T(X(d['x']), Y(d['y']) + 4, nm, 'tb'))
    for x in range(0, 161, 20):
        o.append(L(X(x), Y(VAN_W), X(x), Y(VAN_W) + 5, 'dim'))
        o.append(T(X(x), Y(VAN_W) + 17, str(x), 'tsm'))
    o.append(T(X(80), Y(VAN_W) + 34, 'inches from the rear-door edge', 'tsm'))
    o.append(T(X(0) + 4, Y(0) - 20, 'rib edge nearest the back (in)', 'tsm', 'start'))
    o.append(T(X(0) - 4, Y(VAN_W / 2), 'rear', 'tsm', 'end'))
    o.append(T(X(VAN_L) + 4, Y(VAN_W / 2), 'cab', 'tsm', 'start'))
    o.append(T(X(78), Y(8), 'driver wall', 'tsm'))
    o.append(T(X(78), Y(VAN_W - 5), 'passenger wall', 'tsm'))
    return svg(W, H, ''.join(o), 'The roof seen from above: five ribs, the fan opening near the back and the air conditioner opening 2 ribs further forward')


def fig_clearance():
    S, X0 = 7.6, 18
    X = lambda x: X0 + S * x
    W, H = int(X(66) + 12), 232
    yb = 50
    o = [R(X(0), yb, S * 66, 62, 'roofbox')]
    for r in RIBS[:3]:
        o.append(R(X(r), yb, S * RIBW, 62, 'rib'))
        o.append(T(X(r) + S * RIBW / 2, yb - 6, 'rib', 'tsm'))
    fx0, fx1 = FAN['x'] - FAN['w'] / 2, FAN['x'] + FAN['w'] / 2
    ax0, ax1 = AC['x'] - AC['w'] / 2, AC['x'] + AC['w'] / 2
    o.append(R(X(fx0 - .75), yb + 12, S * (FAN['w'] + 1.5), 38, 'frame'))
    o.append(R(X(ax0 - 1.5), yb + 12, S * (AC['w'] + 3), 38, 'frame'))
    o.append(R(X(fx0), yb + 12, S * FAN['w'], 38, 'hole'))
    o.append(R(X(ax0), yb + 12, S * AC['w'], 38, 'hole'))
    o.append(T(X(FAN['x']), yb + 36, 'FAN', 'tb'))
    o.append(T(X(AC['x']), yb + 36, 'A/C', 'tb'))
    # row 1: opening edge to the rib; row 2: frame edge to the rib
    y1, y2 = yb + 92, yb + 150
    o.append(T(X(0) + 4, y1 - 14, 'opening to rib:', 'tsm', 'start'))
    o.append(dimh(X(fx1), X(RIBS[0]), y1, fr(RIBS[0] - fx1)))
    o.append(dimh(X(RIBS[1] + RIBW), X(ax0), y1, fr(ax0 - (RIBS[1] + RIBW))))
    o.append(dimh(X(ax1), X(RIBS[2]), y1, fr(RIBS[2] - ax1)))
    o.append(T(X(0) + 4, y2 - 14, 'frame to rib:', 'tsm', 'start'))
    o.append(dimh(X(fx1 + .75), X(RIBS[0]), y2, fr(RIBS[0] - fx1 - .75)))
    o.append(dimh(X(RIBS[1] + RIBW), X(ax0 - 1.5), y2, fr(ax0 - 1.5 - (RIBS[1] + RIBW))))
    o.append(dimh(X(ax1 + 1.5), X(RIBS[2]), y2, fr(RIBS[2] - ax1 - 1.5)))
    o.append(T(X(0), 18, 'rear-door edge', 'tsm', 'start'))
    o.append(T(X(66), 18, 'toward the cab', 'tsm', 'end'))
    return svg(W, H, ''.join(o), 'Top view along the van: the clearance from each opening and each frame to the nearest ribs')

def fig_template():
    S = 11.2
    o = []
    for cx, nm, d in ((150, 'FAN', FAN), (410, 'A/C', AC)):
        w = d['w'] * S
        x0, y0 = cx - w / 2, 66
        o.append(R(x0, y0, w, w, 'tmpl'))
        o.append(L(x0, y0, x0 + w, y0 + w, 'diag'))
        o.append(L(x0 + w, y0, x0, y0 + w, 'diag'))
        o.append(L(cx, y0 - 8, cx, y0 + w + 8, 'ctr'))
        o.append(L(x0 - 8, y0 + w / 2, x0 + w + 8, y0 + w / 2, 'ctr'))
        for px, py in ((x0, y0), (x0 + w, y0), (x0, y0 + w), (x0 + w, y0 + w)):
            o.append(C(px, py, 5, 'drill'))
        o.append(T(cx, 20, f'{nm}  {fr(d["w"])} x {fr(d["w"])}', 'tb'))
        o.append(T(cx, 37, f'center {fr(d["x"])} from the rear-door edge,', 'tsm'))
        o.append(T(cx, 50, f'{fr(d["y"])} from the driver wall', 'tsm'))
        o.append(dimh(x0, x0 + w, y0 + w + 26, fr(d['w'])))
        o.append(T(cx, y0 + w + 52, 'both diagonals equal = square', 'tsm'))
    o.append(T(280, 296, 'dots: a hole at each corner, big enough for the jigsaw blade (about 3/8 in)', 'tsm'))
    return svg(560, 306, ''.join(o), 'Paper templates for the two openings with corner holes, diagonals and center lines')

def fig_cut():
    o = []
    o.append(R(40, 100, 480, 7, 'steel'))
    o.append(R(190, 100, 180, 7, 'sky'))
    o.append(R(150, 94, 38, 4, 'tape'))
    o.append(R(372, 94, 38, 4, 'tape'))
    o.append(T(168, 86, 'masking tape', 'tsm'))
    o.append(T(392, 86, 'masking tape', 'tsm'))
    o.append(R(262, 28, 36, 22, 'tool', 3))
    o.append(T(280, 43, 'jigsaw', 'twhite'))
    o.append(R(250, 50, 60, 8, 'tool'))
    o.append(R(278, 58, 4, 52, 'blade'))
    o.append(T(316, 34, 'fresh metal blade', 'tsm', 'start'))
    o.append(L(280, 112, 280, 128, 'spark'))
    o.append(PL([(120, 140), (170, 156), (400, 156), (450, 140)], 'plastic'))
    for i, x in enumerate(range(200, 360, 17)):
        o.append(C(x, 152 - (i % 2) * 2, 1.8, 'swarf'))
    o.append(T(285, 180, 'plastic sheet under the cut catches the steel shavings (they rust)', 'tsm'))
    o.append(T(285, 198, 'tape both sides of the line, cut slowly, keep the shoe flat', 'tsm'))
    o.append(T(100, 124, 'roof steel', 'tsm'))
    return svg(560, 210, ''.join(o), 'Cutting the opening with a jigsaw: tape on the paint, plastic sheet below')

def fig_edge():
    o = []
    for i, (cx, ttl, kind) in enumerate(((100, '1  file off the burr', 'burr'), (280, '2  rust-proof primer', 'prime'), (460, '3  paint over it', 'paint'))):
        o.append(T(cx, 22, ttl, 'tb'))
        o.append(R(cx - 70, 60, 70, 12, 'steel'))
        o.append(L(cx, 60, cx, 72, 'edge'))
        if kind == 'burr':
            o.append(P([(cx, 60), (cx + 5, 52), (cx + 2, 60)], 'steel'))
            o.append(P([(cx, 72), (cx + 7, 82), (cx + 2, 72)], 'steel'))
        if kind in ('prime', 'paint'):
            o.append(R(cx - 70, 56, 74, 4, 'primer'))
            o.append(R(cx - 70, 72, 74, 4, 'primer'))
            o.append(R(cx, 56, 4, 20, 'primer'))
        if kind == 'paint':
            o.append(R(cx - 70, 52, 78, 4, 'paint'))
            o.append(R(cx - 70, 76, 78, 4, 'paint'))
            o.append(R(cx + 4, 52, 4, 28, 'paint'))
        o.append(T(cx - 35, 100, 'cut edge on the right', 'tsm'))
    o.append(T(280, 128, 'bare cut steel rusts through the roof, so every edge gets primer and paint before the frame goes on', 'tsm'))
    return svg(560, 140, ''.join(o), 'The cut edge: file the burr, prime, paint')


def fig_frames():
    o = []
    # fan frame, plan view
    S = 11.2
    cx, y0 = 140, 40
    w = 15.5 * S
    x0 = cx - w / 2
    o.append(T(cx, 20, f'FAN frame, {fr(FRAME)} tall', 'tb'))
    o.append(R(x0, y0, w, .75 * S, 'wood'))
    o.append(R(x0, y0 + w - .75 * S, w, .75 * S, 'wood'))
    o.append(R(x0, y0 + .75 * S, .75 * S, 14 * S, 'wood2'))
    o.append(R(x0 + w - .75 * S, y0 + .75 * S, .75 * S, 14 * S, 'wood2'))
    o.append(T(cx, y0 + w / 2 + 4, 'opening 14 x 14', 'tsm'))
    o.append(dimh(x0, x0 + w, y0 + w + 20, 'outside 15 1/2'))
    # A/C frame, plan view (long way along the van = left-right)
    S2 = 10.4
    ax = 270
    ww, hh = 17.25 * S2, 15.75 * S2
    ay = 40 + (15.5 * S - hh) / 2
    o.append(T(ax + ww / 2, 20, 'A/C frame, 2 tall (step 6)', 'tb'))
    o.append(R(ax, ay, 1.5 * S2, hh, 'wood'))
    o.append(R(ax + ww - 1.5 * S2, ay, 1.5 * S2, hh, 'wood'))
    o.append(R(ax + 1.5 * S2, ay, 14.25 * S2, .75 * S2, 'wood2'))
    o.append(R(ax + 1.5 * S2, ay + hh - .75 * S2, 14.25 * S2, .75 * S2, 'wood2'))
    o.append(T(ax + ww / 2, ay + hh / 2 + 4, 'opening 14 1/4 square', 'tsm'))
    o.append(dimh(ax, ax + ww, ay + hh + 20, 'outside 17 1/4 along the van'))
    o.append(dimv(ax + ww + 12, ay, ay + hh, '15 3/4', False))
    o.append(T(ax + 1.5 * S2 / 2, ay - 6, 'rib side', 'tsm'))
    o.append(T(ax + ww - 1.5 * S2 / 2, ay - 6, 'rib side', 'tsm'))
    o.append(T(20, 250, 'Fan: 2 pieces 15 1/2 long (top and bottom), 2 pieces 14 long (sides, between them).', 'tsm', 'start'))
    o.append(T(20, 266, 'A/C: 2 pieces 15 3/4 x 1 1/2 thick (the rib sides, two 3/4 in layers glued),', 'tsm', 'start'))
    o.append(T(20, 282, '2 pieces 14 1/4 x 3/4 thick (the sides, between them).', 'tsm', 'start'))
    return svg(560, 292, ''.join(o), 'Plan view of the two frames with every piece labelled')


def fig_bond():
    SX, SY, X0, Y0 = 13.0, 24.0, 70, 70      # px per inch along the van, per inch down, left edge, the steel line
    X = lambda x: X0 + SX * x
    Y = lambda z: Y0 + SY * z                 # z in down from the steel
    o = []
    o.append(L(X(0), Y0 - 40, X(0), Y(5.2), 'ctr'))
    o.append(T(4, Y0 - 44, 'rear-door edge', 'tsm', 'start'))
    o.append(R(X(0), Y0 - 4, X(6.25) - X(0), 4, 'steel'))
    o.append(R(X(20.25), Y0 - 4, X(30) - X(20.25), 4, 'steel'))
    o.append(T(X(14.5), Y0 - 14, 'opening 14 in', 'tsm'))
    # frame walls, 3/4 in thick, as deep as the covering stack: outer faces at 5 1/2 and 21
    o.append(R(X(5.5), Y0, X(6.25) - X(5.5), SY * FRAME, 'wood'))
    o.append(R(X(20.25), Y0, X(21.0) - X(20.25), SY * FRAME, 'wood'))
    o.append(R(X(5.5), Y0 - 6, X(6.25) - X(5.5), 6, 'glue'))
    o.append(R(X(20.25), Y0 - 6, X(21.0) - X(20.25), 6, 'glue'))
    o.append(T(X(13.25), Y0 + 26, 'frame', 'tb'))
    # the rib
    o.append(R(X(21.75), Y0, X(24.5) - X(21.75), SY * 2.0, 'rib'))
    o.append(T(X(23.1), Y0 + SY + 4, 'rib', 'twh'))
    # dimensions
    o.append(dimv(X(3.9), Y0, Y(FRAME), fr(FRAME), True))
    o.append(dimv(X(26.2), Y0, Y(2.0), '2 in', False))
    o.append(L(X(21.0), Y(2.0) + 8, X(21.75), Y(2.0) + 8, 'dim'))
    o.append(L(X(21.0), Y(2.0) + 4, X(21.0), Y(2.0) + 12, 'dim'))
    o.append(L(X(21.75), Y(2.0) + 4, X(21.75), Y(2.0) + 12, 'dim'))
    o.append(T(X(21.5), Y(2.0) + 26, '3/4 in to the rib', 'tdim', 'start'))
    # bead label
    o.append(T(X(8), Y0 - 40, 'adhesive bead on the frame top (orange)', 'tsm', 'start'))
    o.append(arrow(X(8), Y0 - 36, X(6.0), Y0 - 8))
    # props
    for px in (X(5.88), X(20.62)):
        o.append(R(px - 3, Y(3.15), 6, 46, 'prop'))
    o.append(T(X(13.25), Y(3.15) + 64, 'props from the floor (sticks or a board) hold the frame up', 'tsm'))
    o.append(T(X(13.25), Y(3.15) + 82, 'work time 35 min, skin 40 min, leave the props in overnight', 'tb'))
    return svg(560, 252, ''.join(o), 'Section along the van: the fan frame hangs from the roof steel on a bead of adhesive with props under it')

def fig_flange():
    S = 13.0
    cx, cy = 200, 188
    u = 17.7 * S
    o = []
    o.append(R(cx - u / 2, cy - u / 2, u, u, 'unit'))
    rl, rr = cx - 8.75 * S, cx + 8.4 * S           # the ring is clipped short of the rib on the front side
    o.append(R(rl, cy - 8.75 * S, rr - rl, 17.5 * S, 'ring'))
    o.append(R(cx - 7.75 * S, cy - 7.75 * S, 15.5 * S, 15.5 * S, 'frame'))
    o.append(R(cx - 7 * S, cy - 7 * S, 14 * S, 14 * S, 'hole'))
    rx = cx + 8.5 * S
    o.append(R(rx, cy - 11 * S, 2.75 * S, 22 * S, 'rib'))
    o.append(T(rx + 1.4 * S, cy - 11 * S - 6, 'rib 21 3/4', 'tsm'))
    for dx, dy in ((-8.2, -8.2), (0, -8.3), (8.2, -8.2), (-8.2, 0), (8.2, 0), (-8.2, 8.2), (0, 8.3), (8.2, 8.2)):
        o.append(C(cx + dx * S, cy + dy * S, 3, 'drill'))
    o.append(T(cx, cy + 4, 'opening 14 x 14', 'tsm'))
    ly = cy - 11 * S - 10
    o.append(T(20, ly + 14, 'Seen from above, rear on the left.', 'tsm', 'start'))
    o.append(T(20, ly + 30, 'blue dashes: the fan flange (17.7 square)', 'tsm', 'start'))
    o.append(T(20, cy + 11.4 * S + 12, 'dark tan: the frame wall (3/4 in).  light tan: backing ring, 1 in wide, 1/2 in on the rib side.', 'tsm', 'start'))
    o.append(T(20, cy + 11.4 * S + 28, 'dots: flange screw holes (yours may differ). A dot on neither tan is bare thin steel.', 'tsm', 'start'))
    return svg(560, 372, ''.join(o), 'Top view of the fan flange over the opening, the frame, a backing ring and the nearest rib')


def fig_fan_stack():
    SX, SY, Y0 = 11.0, 26.0, 124            # px per inch across, per inch down, the roof steel line
    X0 = 24
    X = lambda x: X0 + SX * x               # x in: 0 is the left edge of the flange (rear side)
    Y = lambda z: Y0 + SY * z
    o = []
    o.append(R(X(0), Y0 - 4, X(1.85) - X(0), 4, 'steel'))
    o.append(R(X(15.85), Y0 - 4, X(30) - X(15.85), 4, 'steel'))
    o.append(R(X(0), Y0 - 18, X(17.7) - X(0), 12, 'unit'))
    o.append(R(X(0), Y0 - 6, X(17.7) - X(0), 3, 'butyl'))
    o.append(R(X(2.5), Y0 - 66, X(15.2) - X(2.5), 48, 'unit', 4))
    o.append(T(X(8.85), Y0 - 44, 'FAN 6.4 in tall', 'tb'))
    o.append(T(X(8.85), Y0 - 30, '(not to scale)', 'tsm'))
    for sx in (X(.65), X(17.05)):
        o.append(L(sx, Y0 - 22, sx, Y0 + 3 + SY * .75, 'screw'))
    o.append(P([(X(-0.4), Y0 - 3), (X(.3), Y0 - 16), (X(.3), Y0 - 3)], 'seal'))
    o.append(P([(X(18.1), Y0 - 3), (X(17.4), Y0 - 16), (X(17.4), Y0 - 3)], 'seal'))
    o.append(T(X(0), 16, 'butyl tape under the flange (dark), sealant over the screws (green)', 'tsm', 'start'))
    # frame walls (3/4 in, as deep as the covering stack), backing ring under the screws, trim ring at the finished ceiling
    o.append(R(X(1.1), Y0, X(1.85) - X(1.1), SY * FRAME, 'wood'))
    o.append(R(X(15.85), Y0, X(16.6) - X(15.85), SY * FRAME, 'wood'))
    o.append(R(X(0.1), Y0, X(1.1) - X(0.1), SY * .75, 'ring'))
    o.append(R(X(16.6), Y0, X(17.1) - X(16.6), SY * .75, 'ring'))
    o.append(R(X(2.0), Y0, 8, SY * (FRAME - .125), 'sleeve'))
    o.append(R(X(15.7) - 8, Y0, 8, SY * (FRAME - .125), 'sleeve'))
    o.append(R(X(0.6), Y(FRAME), X(17.1) - X(0.6), 6, 'trim'))
    o.append(T(X(8.85), Y(FRAME) + 22, 'trim ring on the finished ceiling (last)', 'tsm'))
    # the rib 3/4 in from the frame, and the covering under it
    o.append(R(X(17.35), Y0, X(20.1) - X(17.35), SY * 2, 'rib'))
    o.append(R(X(16.6), Y(RIBD), X(27) - X(16.6), SY * COV, 'ply'))
    o.append(T(X(18.7), Y(1) + 4, 'rib', 'twh'))
    o.append(T(X(22), Y(RIBD + COV / 2) + 4, f'covering {fr(COV)}', 'twh'))
    o.append(T(X(0.6), Y(.75) + 12, 'ring', 'tsm', 'end'))
    # where the frame depth comes from: the frame is as deep as the rib plus the covering
    fx = X(3.6)
    o.append(L(fx, Y0 + 2, fx, Y(FRAME) - 2, 'dim'))
    o.append(L(fx - 5, Y0 + 2, fx + 5, Y0 + 2, 'dim'))
    o.append(L(fx - 5, Y(FRAME) - 2, fx + 5, Y(FRAME) - 2, 'dim'))
    o.append(f'<text x="{fx + 9:.1f}" y="{Y(1.5) + 2:.1f}" class="tb" text-anchor="start">frame {fr(FRAME)}</text>')
    o.append(f'<text x="{fx + 9:.1f}" y="{Y(1.5) + 18:.1f}" class="tsm" text-anchor="start">= rib 2</text>')
    o.append(f'<text x="{fx + 9:.1f}" y="{Y(1.5) + 33:.1f}" class="tsm" text-anchor="start">+ covering {fr(COV)}</text>')
    rx = X(28.2)
    for z0, z1, lab in ((0, RIBD, 'rib 2'), (RIBD, FRAME, fr(COV))):
        o.append(L(rx, Y(z0) + 2, rx, Y(z1) - 2, 'dim'))
        o.append(L(rx - 4, Y(z0) + 2, rx + 4, Y(z0) + 2, 'dim'))
        o.append(L(rx - 4, Y(z1) - 2, rx + 4, Y(z1) - 2, 'dim'))
        o.append(f'<text x="{rx + 8:.1f}" y="{(Y(z0) + Y(z1)) / 2 + 4:.1f}" class="tdim" text-anchor="start">{lab}</text>')
    bx = 400
    o.append(L(bx, Y0, bx, Y(4.5), 'dim'))
    o.append(R(bx - 4, Y(2.75), 8, SY * (4.5 - 2.75), 'range'))
    for z, lab, c, dy in ((0, 'roof', 'tdim', 4), (FAN_MIN, 'fan minimum ' + fr(FAN_MIN), 'tdim', -3), (STACK, 'your stack ' + fr(STACK), 'tb', 8), (FAN_MAX, 'fan maximum ' + fr(FAN_MAX), 'tdim', 4)):
        o.append(L(bx - 6, Y(z), bx + 6, Y(z), 'dim'))
        o.append(f'<text x="{bx + 12}" y="{Y(z) + dy:.1f}" class="{c}" text-anchor="start">{lab}</text>')
    o.append(T(280, Y(4.5) + 38, f'your stack = steel + 2 in of rib + {fr(COV)} in of covering, measured to the trim', 'tsm'))
    return svg(580, 296, ''.join(o), 'Section through the fan: sealing at the roof, the frame, the backing rings and the trim depth against the fan depth range')


def fig_ac():
    import math
    o = []
    cx, base = 280, 100
    pts = []
    for i in range(-24, 25):
        x = cx + i * 10
        d = i * 10 / 10.0
        pts.append((x, base + (d * d) / (2 * 108.9) * 3.0 * 10))
    o.append(PL(pts, 'steelline'))
    o.append(R(cx - 71, base - 8, 142, 30, 'sky'))
    # frame walls: 3/4 in thick, 2 in tall, outside 15 3/4 (10 px per inch)
    o.append(R(cx - 78.75, base + 1, 7.5, 20, 'wood'))
    o.append(R(cx + 71.25, base + 1, 7.5, 20, 'wood'))
    o.append(R(cx - 141, base - 10, 282, 8, 'butyl'))
    o.append(R(cx - 141, base - 72, 282, 62, 'unit', 4))
    o.append(T(cx, base - 46, 'A/C  28 1/4 x 28 1/4, 6.3 in tall', 'tb'))
    o.append(T(cx, base - 30, '33 to 45 lb: two people, pad the roof', 'tsm'))
    # indoor panel at the bottom of the frame (up to 14.5 wide)
    o.append(R(cx - 72.5, base + 21, 145, 9, 'trim'))
    o.append(T(cx, base + 46, 'indoor panel (up to 14 1/2 x 10) on the frame bottom', 'tsm'))
    o.append(dimh(cx - 71.25, cx + 71.25, base + 70, 'opening 14 1/4'))
    o.append(dimh(cx - 78.75, cx + 78.75, base + 96, 'frame outside 15 3/4 across, 2 in deep'))
    o.append(T(cx - 152, base - 14, 'roof falls away', 'tsm', 'end'))
    o.append(T(cx - 152, base - 1, 'about 0.9 in here', 'tsm', 'end'))
    o.append(T(cx + 152, base - 14, 'roof falls away', 'tsm', 'start'))
    o.append(T(cx + 152, base - 1, 'about 0.9 in here', 'tsm', 'start'))
    o.append(T(cx, 20, 'section across the van (the roof curve is drawn 3 times too strong)', 'tsm'))
    return svg(560, 218, ''.join(o), 'Cross-section across the van at the air conditioner: the roof crown, the gasket and the frame')

def fig_wiring():
    o = []
    o.append(R(16, 92, 104, 58, 'box', 6))
    o.append(T(68, 116, 'BATTERY', 'tb'))
    o.append(T(68, 132, '12 V, 280 Ah', 'tsm'))
    o.append(L(120, 104, 176, 104, 'pos'))
    o.append(T(148, 98, '+', 'tb'))
    # fan branch (top)
    o.append(L(176, 104, 176, 52, 'pos'))
    o.append(L(176, 52, 214, 52, 'pos'))
    o.append(R(214, 38, 80, 28, 'box', 4))
    o.append(T(254, 56, 'fuse about 5 A', 'tsm'))
    o.append(L(294, 52, 322, 52, 'pos'))
    o.append(R(322, 38, 60, 28, 'box', 4))
    o.append(T(352, 56, 'switch', 'tsm'))
    o.append(L(382, 52, 410, 52, 'pos'))
    o.append(R(410, 36, 130, 32, 'box', 6))
    o.append(T(475, 56, 'FAN, 14 AWG pair', 'tb'))
    # A/C branch (bottom)
    o.append(L(176, 104, 176, 150, 'pos'))
    o.append(L(176, 150, 214, 150, 'pos'))
    o.append(R(214, 134, 146, 32, 'box', 4))
    o.append(T(287, 154, 'big fuse near the battery', 'tsm'))
    o.append(T(287, 182, 'size per the A/C manual', 'tsm'))
    o.append(L(360, 150, 410, 150, 'pos'))
    o.append(R(410, 134, 130, 32, 'box', 6))
    o.append(T(475, 154, 'A/C, up to 58 A', 'tb'))
    # negative return: one rail below, joined up the right side
    o.append(L(120, 138, 150, 138, 'neg'))
    o.append(L(150, 138, 150, 216, 'neg'))
    o.append(L(150, 216, 566, 216, 'neg'))
    o.append(L(566, 216, 566, 52, 'neg'))
    o.append(L(540, 52, 566, 52, 'neg'))
    o.append(L(540, 150, 566, 150, 'neg'))
    o.append(T(358, 210, 'negative: back to the battery', 'tsm'))
    o.append(T(300, 238, 'red = positive, black = negative.', 'tsm'))
    o.append(T(300, 254, 'Check polarity with a meter before you connect the fan (it has no directions).', 'tsm'))
    return svg(580, 268, ''.join(o), 'Wiring sketch: battery, fuses, a switch for the fan and heavy cable for the air conditioner')

def fig_leak():
    o = []
    o.append(R(60, 120, 440, 6, 'steel'))
    o.append(R(240, 80, 90, 40, 'unit', 4))
    o.append(T(285, 104, 'fan', 'tb'))
    # water
    for x in range(140, 440, 26):
        o.append(arrow(x, 24, x - 10, 70, 'water'))
    o.append(T(120, 20, 'garden hose, from low to high', 'tsm', 'start'))
    o.append(R(240, 126, 90, 26, 'wood'))
    o.append(T(285, 168, 'a helper inside with a light', 'tsm'))
    o.append(T(285, 184, 'watches the frame and the ceiling edge', 'tsm'))
    o.append(T(285, 206, 'any drip: dry it, find where it came from, add sealant, test again', 'tsm'))
    return svg(560, 218, ''.join(o), 'The leak test: water from outside, a person inside with a light')


# ---------------------------------------------------------------- page
CSS = """
:root { color-scheme: light dark; --bg:#fbfaf7; --card:#fff; --ink:#26241f; --mute:#6a665c; --line:#d9d5ca; --acc:#185FA5; --ok:#0F6E56; --warn:#8A5A00; --steel:#9aa3ad; --wood:#d9b382; --wood2:#e8cba4; }
@media (prefers-color-scheme: dark) { :root { --bg:#1b1a17; --card:#242320; --ink:#ece9e0; --mute:#aaa598; --line:#3d3b34; --acc:#6fb1ee; --ok:#5cc9a7; --warn:#e0b25d; --steel:#7c8691; --wood:#a98258; --wood2:#bf9a6e; } }
* { box-sizing: border-box; }
body { margin: 0; background: var(--bg); color: var(--ink); font: 16px/1.5 system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; }
.wrap { max-width: 900px; margin: 0 auto; padding: 16px; }
h1 { font-size: 26px; margin: 8px 0 4px; }
h2 { font-size: 20px; margin: 0 0 8px; display: flex; align-items: center; gap: 10px; }
h3 { font-size: 16px; margin: 14px 0 6px; }
.lead { color: var(--mute); margin: 0 0 14px; }
.n { display: inline-flex; align-items: center; justify-content: center; width: 30px; height: 30px; border-radius: 50%; background: var(--acc); color: var(--bg); font-weight: 700; flex: 0 0 auto; }
.card { background: var(--card); border: 1px solid var(--line); border-radius: 12px; padding: 14px 16px; margin: 0 0 16px; }
.card.done { opacity: .6; }
.cols { display: grid; grid-template-columns: 1fr 1fr; gap: 16px; }
@media (max-width: 640px) { .cols { grid-template-columns: 1fr; } }
table { border-collapse: collapse; width: 100%; font-size: 15px; }
th, td { border-bottom: 1px solid var(--line); padding: 5px 8px; text-align: left; vertical-align: top; }
th { color: var(--mute); font-weight: 600; }
ul, ol { margin: 6px 0 6px 20px; padding: 0; }
li { margin: 3px 0; }
.chk { list-style: none; margin-left: 0; }
.chk li { display: flex; gap: 8px; align-items: flex-start; }
.chk input { margin-top: 5px; }
.figwrap { overflow-x: auto; margin: 8px 0 10px; }
.fig { width: 100%; height: auto; display: block; background: var(--card); }
@media (max-width: 640px) { .fig { min-width: 560px; } .swipe { display: block !important; } }
.swipe { display: none; color: var(--mute); font-size: 13px; margin: 0 0 6px; }
@media print { .card { break-inside: avoid; } h2 { break-after: avoid; } .fig { min-width: 0; } .tick { display: none; } }
.note { border-left: 4px solid var(--warn); background: color-mix(in srgb, var(--warn) 10%, transparent); padding: 6px 10px; margin: 8px 0; border-radius: 0 8px 8px 0; font-size: 15px; }
.ok { border-left-color: var(--ok); background: color-mix(in srgb, var(--ok) 10%, transparent); }
.tick { margin-left: auto; font-size: 14px; color: var(--mute); font-weight: 400; display: flex; gap: 6px; align-items: center; }
.time { display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; }
@media (max-width: 640px) { .time { grid-template-columns: 1fr; } }
.time div { border: 1px solid var(--line); border-radius: 10px; padding: 8px 10px; }
.time b { display: block; margin-bottom: 4px; color: var(--acc); }
/* drawings */
svg text { font-family: system-ui, -apple-system, 'Segoe UI', Roboto, sans-serif; fill: var(--ink); }
.t { font-size: 12px; } .tb { font-size: 13px; font-weight: 700; } .tsm { font-size: 11.5px; fill: var(--mute); } .tdim { font-size: 12px; fill: var(--acc); font-weight: 600; } .twh { font-size: 11px; fill: var(--ink); font-weight: 600; } .twhite { font-size: 11px; fill: #fff; font-weight: 600; }
.roofbox { fill: none; stroke: var(--ink); stroke-width: 1.5; }
.rib { fill: var(--steel); stroke: var(--ink); stroke-width: .8; opacity: .85; }
.unit { fill: color-mix(in srgb, var(--acc) 12%, transparent); stroke: var(--acc); stroke-width: 1.4; stroke-dasharray: 5 3; }
.hole { fill: var(--card); stroke: var(--ink); stroke-width: 1.6; }
.frame { fill: var(--wood); stroke: #5a3a00; stroke-width: 1; }
.frameline { fill: none; stroke: #8a5a00; stroke-width: 1.4; stroke-dasharray: 4 3; }
.ring { fill: var(--wood2); stroke: #8a5a00; stroke-width: 1; opacity: .8; }
.tmpl { fill: color-mix(in srgb, var(--warn) 10%, transparent); stroke: var(--ink); stroke-width: 1.4; }
.diag { stroke: var(--mute); stroke-width: 1; stroke-dasharray: 3 3; }
.ctr { stroke: var(--acc); stroke-width: 1; stroke-dasharray: 8 3 2 3; }
.drill { fill: var(--ink); }
.ln, .dim { stroke: var(--acc); stroke-width: 1.1; }
.steel { fill: var(--steel); stroke: var(--ink); stroke-width: .8; }
.steelline { fill: none; stroke: var(--steel); stroke-width: 5; stroke-linecap: round; }
.sky { fill: var(--card); }
.tape { fill: #e9d78a; stroke: #8a7a2a; stroke-width: .8; }
.tool { fill: #555a60; stroke: var(--ink); stroke-width: .8; }
.blade { fill: #c9ced4; stroke: var(--ink); stroke-width: .6; }
.spark { stroke: #e0842a; stroke-width: 2; stroke-dasharray: 2 2; }
.plastic { stroke: #4a90c8; stroke-width: 2.5; fill: none; }
.swarf { fill: #8a4a2a; }
.edge { stroke: #c0392b; stroke-width: 1.4; }
.primer { fill: #b8423a; }
.paint { fill: #f2efe6; stroke: var(--line); stroke-width: .6; }
.wood { fill: var(--wood); stroke: #5a3a00; stroke-width: 1; }
.wood2 { fill: var(--wood2); stroke: #5a3a00; stroke-width: 1; }
.glue { fill: #e0842a; stroke: #8a4a10; stroke-width: .6; }
.prop { fill: var(--wood2); stroke: #5a3a00; stroke-width: .8; }
.arr, .water { stroke: var(--acc); stroke-width: 1.6; fill: none; }
.water { stroke: #4a90c8; stroke-dasharray: 5 4; }
.arrhead { fill: var(--acc); }
.butyl { fill: var(--ink); opacity: .75; }
.screw { stroke: var(--ink); stroke-width: 2; }
.seal { fill: #2a9d6a; }
.ply { fill: #e8d8b0; stroke: #8a6a2a; stroke-width: .8; }
.sleeve { fill: #cfd4da; stroke: var(--ink); stroke-width: .6; }
.trim { fill: #f4f1e8; stroke: var(--ink); stroke-width: 1; }
.range { fill: var(--ok); opacity: .55; }
.box { fill: var(--card); stroke: var(--ink); stroke-width: 1.2; }
.pos { stroke: #c0392b; stroke-width: 2.5; fill: none; }
.neg { stroke: var(--ink); stroke-width: 2.5; fill: none; }
.propline { stroke: #5a3a00; stroke-width: 5; opacity: .8; }
.warnbox { border: 2px solid var(--warn); }
"""

CHECK_KEY = 'van-install-ticks'


def li(items):
    return ''.join(f'<li>{i}</li>' for i in items)


def step(n, title, body, fig=None):
    return (f'<section class="card" id="s{n}" data-step="{n}"><h2><span class="n">{n}</span>{title}'
            f'<label class="tick"><input type="checkbox" data-s="{n}"> done</label></h2>{("<div class=figwrap>" + fig + "</div>") if fig else ""}{body}</section>')


def build():
    S = []
    S.append(step(1, 'Find the ribs first',
                  '<ul>' + li([
                      'Measure from the <b>rear-door edge</b> (not the 6 in zero on the wall drawings). The ribs run across the van; their edge nearest the back is at 21 3/4, 37 7/8, 58 3/8, 97 3/8 and 126 3/8 in, each 2 3/4 wide.',
                      'Find the real ones from inside with a magnet, or by knocking. Measure the rib edges to <b>1/8 in</b>: the drawing above shows how little room there is, <b>1 1/2 in</b> from the fan opening to its rib and <b>1 3/4 in</b> each side of the A/C opening, and the A/C frame leaves only <b>1/4 in</b> to each rib.',
                      'If a rib edge next to the A/C is more than 1/8 in closer than 40 5/8 or 58 3/8 in, trim the 1 1/2 in rib-side pieces in step 6 before you glue. If any rib is more than about 1/2 in away from the numbers, stop and tell me: the openings or frames move.',
                  ]) + '</ul>', fig_clearance()))
    S.append(step(2, 'Make the templates',
                  '<ul>' + li([
                      'Cut paper templates: fan <b>14 x 14</b>, A/C <b>14 1/4 x 14 1/4</b> (the A/C manual may say otherwise: the maker lists a minimum of 14.1 x 13.7).',
                      'Draw both diagonals and the center lines. Both diagonals must measure the same, or the template is not square.',
                      'Put the <b>center</b> of the fan template <b>13 1/4 in from the rear-door edge and 34 in from the driver wall (the middle of the van)</b>; the A/C center <b>49 1/2 in and 34 in</b>. Measure across horizontally (use a level or a plumb line): the roof curves.',
                      'Tape the template to the inside of the roof, drill a hole at each corner right through, and mark the same square on the outside from those holes. Seal any hole you do not cut out with primer and sealant.',
                  ]) + '</ul>', fig_template()))
    S.append(step(3, 'Cut the fan opening first, then the A/C',
                  '<ul>' + li([
                      '<b>A/C only if you have its manual&rsquo;s opening size.</b> Without it, cut the fan today and leave the A/C hole for later.',
                      'Tape the paint on both sides of each cut line with masking tape, and hang a plastic sheet under the cut to catch the steel shavings.',
                      'Jigsaw with a fresh fine-tooth metal blade, from corner hole to corner hole. Go slowly and keep the shoe flat; the fan is the smaller one, so it is good practice.',
                      'Wear glasses, gloves and hearing protection. Vacuum up every shaving: they rust and stain the roof.',
                      '<b>Cover each hole</b> with plastic or a board taped to clean, dry paint whenever you stop, until its unit is on.',
                  ]) + '</ul>', fig_cut()))
    S.append(step(4, 'Deburr and rust-proof every cut edge',
                  '<ul>' + li([
                      'File or sand off the burr, inside and out. Wipe off the dust.',
                      'Brush rust-inhibiting primer on the cut edge and a little onto the top and bottom faces, then paint over it. Keep the paint to the edge and a thin band: the frame bonds to the underside of the roof next to the cut, and that band is scuffed and cleaned bare in step 7.',
                      'Let the primer and paint dry as the cans say before the frame goes on. Do the cutting early in the day.',
                  ]) + '</ul>', fig_edge()))
    S.append(step(5, 'Lay the fan on the roof and mark its screw holes',
                  '<ul>' + li([
                      'Set the fan on the roof unfastened, centered on the opening, and mark where each flange screw hole lands. Do this <b>before</b> you build the frame, so the frame and backing rings come out right.',
                      'The flange reaches about 1 3/4 in past the opening, but the frame wall reaches only 3/4 in. A hole that falls outside the frame bites into thin steel.',
                      'If so, add a <b>backing ring</b>: 3/4 in plywood strips, <b>1 in wide</b>, butted to the outside of the frame wall under the roof (outer edge 8 3/4 in from the fan&rsquo;s center), and only 1/2 in wide on the rib side so it stays off the rib. It is bonded with the frame in step 7, so it is cured before the fan screws go in. One Transit build on the Sportsmobile forum bonded wood strips for the same reason.',
                      'The fan sits in the middle of the van, at the crown of the roof arc, so the flange falls away about 3/8 in below its highest point across its 17.7 in base. See step 8.',
                  ]) + '</ul>', fig_flange()))
    S.append(step(6, 'Build the two frames',
                  '<ul>' + li([
                      '3/4 in plywood (Baltic birch is best) ripped into strips. No pressure-treated wood: it eats steel. <b>Cut, glue and screw the frame first</b>, laminate the thick A/C pieces, then seal or paint the finished frame, leaving the top face bare or sanded for the adhesive.',
                      f'<b>Fan:</b> strips <b>{fr(FRAME)} in wide</b> (the depth to the finished ceiling: the rib&rsquo;s 2 in plus the {fr(COV)} in covering). 2 pieces 15 1/2 long, 2 pieces 14 long fitted between them. Outside 15 1/2 square, opening 14 x 14. Cut the backing ring pieces from step 5 too.',
                      '<b>A/C:</b> strips <b>2 in wide</b> for now (flush with the rib bottoms). 4 pieces 15 3/4 long, glued in pairs into two <b>1 1/2 in thick</b> pieces; 2 pieces 14 1/4 long, 3/4 thick, fitted between them. Outside 17 1/4 along the van by 15 3/4 across.',
                      f'Make the A/C frame {fr(FRAME)} deep too if its manual allows about {fr(STACK)} in from the roof to the trim. <b>I have not seen that manual.</b> Check it before you decide.',
                      'Measure both diagonals of each frame: they must match. Hold each frame up under the roof around its opening and check that its inside faces line up with the cut and that it clears the ribs.',
                  ]) + '</ul>', fig_frames()))
    S.append(step(7, 'Bond the frames to the roof',
                  '<ul>' + li([
                      'Adhesive: one-part polyurethane made for vehicles: Sikaflex-252, or 3M 5200 (permanent). 3M 5200 <b>Fast Cure</b> works too: 3M lists tack-free in about 1 to 2 hours and full cure in about 48 hours, so your working time is shorter than the plain kind (check the tube). Epoxy, silicone and ordinary construction adhesive are the wrong tools.',
                      'Wipe the steel band next to the cut with isopropyl alcohol, scuff it, and wipe again. Sand the wood face and wipe off the dust.',
                      'The frame&rsquo;s inside faces line up with the cut edge. Lay a continuous bead, about 3/8 in wide, along the whole top edge of the frame (and the backing rings). No breaks in the bead: water finds them.',
                      'Both openings sit in the middle of the van, at the crown of the roof, so the frames go on <b>level</b>: no tilt. The arc still leaves up to about 1/4 in of gap under a frame (the top face is straight, the roof is curved). Check with a straightedge that the top face touches the steel along its length, and let the bead fill what is left.',
                      '<b>You have 35 minutes</b> (Sikaflex-252) to press the frame up and prop it. Do one frame at a time, or have a helper. Wipe off the squeeze-out right away.',
                      'Prop each frame from the floor and leave it overnight. Do not screw through the roof. <b>Cover each hole</b> with plastic taped over it.',
                  ]) + '</ul><p class="note">Upper 60s with no rain is good: the adhesive works from 50 to 95 &deg;F. Keep the doors open a little (humidity cures it) and the roof out of strong sun.</p>', fig_bond()))
    S.append(step(8, 'Mount the fan (the next morning)',
                  '<ul>' + li([
                      'Butyl tape in a loop around the opening under the flange, set the fan, screw it down evenly into the frame and the backing rings.',
                      'Use a <b>non-sag</b> lap sealant (or Eternabond tape) over the screw heads and the flange edge: it stays put on the curve. The butyl tape is the real seal.',
                      'The roof falls away about 3/8 in below its highest point across the 17.7 in flange. Check how much curve the fan allows; if it will not seat, use a shaped or thick foam gasket or a curb.',
                      f'The fan needs <b>2 3/4 to 4 1/2 in</b> from the roof to the trim. Your stack (steel + 2 in of rib + {fr(COV)} in of covering: 3/16 in plywood, then 3/4 in slats) is about <b>{fr(STACK)} in</b>, so it fits with {fr(STACK - FAN_MIN)} in to spare above the minimum. This only works if the finished ceiling covering is at least about {fr(FAN_MIN - RIBD - STEEL)} in thick.',
                      'Leave the trim ring until the ceiling is covered. The frame bottom is the finished-ceiling plane.',
                  ]) + '</ul>', fig_fan_stack()))
    S.append(step(9, 'Mount the A/C (48 hours after bonding)',
                  '<ul>' + li([
                      '<b>Read its manual first</b> for the opening size, the roof thickness range and the most roof curve it allows. At the A/C the roof is <b>not tilted</b>, but it is at its crown and falls away about 0.9 in at each side of the unit. A flat gasket cannot close that: use a shaped gasket or curb, whatever the manual allows.',
                      'Two people lift it: 33 lb on the maker&rsquo;s sheet, 45 lb on the listing. Pad the roof and lay a board across the ribs for your feet.',
                      'Gasket, set it straight down on the opening, fasten as the manual says, then non-sag sealant over the fasteners.',
                      'The indoor panel goes on from inside after the ceiling is covered.',
                  ]) + '</ul>', fig_ac()))
    S.append(step(10, 'Wire them',
                  '<ul>' + li([
                      '<b>Fan</b> (12 V DC): a 14 AWG pair, a fuse of about 5 A, and a switch. These are my suggestions: the fan has no amp rating beyond the listing&rsquo;s 3 to 32 W (0.25 to 2.7 A).',
                      '<b>A/C</b> (12 V DC, up to about 58 A in turbo): heavy cable and a big fuse close to the battery, <b>as its manual says</b>. A related OutEquipPro unit lists 6 AWG for a 12 ft lead with a 100 A fuse, and 4 AWG or heavier for longer runs. That is for a different model: confirm for yours.',
                      'Run the wires before the walls and ceiling are covered. Use grommets or sleeves where wire goes through metal.',
                      'Check polarity with a meter before connecting the fan.',
                  ]) + '</ul>', fig_wiring()))
    S.append(step(11, 'Leak test, then finish',
                  '<ul>' + li([
                      'After the adhesive and the sealant have cured, run a garden hose over the roof from the low side up, with a helper inside with a light.',
                      'Any drip: dry it, find where it came from, add sealant and test again.',
                      'Only then insulate around the frames and cover the ceiling. The trim rings go on last.',
                  ]) + '</ul>', fig_leak()))

    nums = ('<table><tr><th></th><th>Fan (F36AR)</th><th>A/C (OutEquip 12 V)</th></tr>'
            '<tr><td>Unit on the roof</td><td>17.7 x 17.7 x 6.4 in</td><td>28.3 x 28.3 x 6.3 in</td></tr>'
            '<tr><td>Roof opening</td><td>14 x 14 in</td><td>14 1/4 square (min 14.1 x 13.7)</td></tr>'
            '<tr><td>Center, from the rear-door edge</td><td>13 1/4 in</td><td>49 1/2 in</td></tr>'
            '<tr><td>Center, from the driver wall</td><td>34 in (middle)</td><td>34 in (middle)</td></tr>'
            '<tr><td>Frame outside</td><td>15 1/2 square</td><td>17 1/4 x 15 3/4</td></tr>'
            f'<tr><td>Frame depth</td><td>{fr(FRAME)} in</td><td>2 in ({fr(FRAME)} if the manual allows)</td></tr>'
            '<tr><td>Roof to trim</td><td>2 3/4 to 4 1/2 in</td><td>not found: check the manual</td></tr>'
            '<tr><td>Weight</td><td>light</td><td>33 lb (maker) to 45 lb (listing)</td></tr></table>')
    mats = ['Primer for the cut edges, rust-inhibiting, plus matching paint',
            'Butyl tape; non-sag lap sealant (or Eternabond tape) for the sloped fan flange; self-leveling Dicor only on the flat',
            'Vehicle polyurethane adhesive: Sikaflex-252 (or 3M 5200)',
            '3/4 in plywood, Baltic birch, about a 2 x 4 ft piece, wood glue, plus primer or paint for it',
            'Isopropyl alcohol, rags, masking tape, paper for templates, plastic sheeting and painter&rsquo;s tape to cover the holes',
            'Fan: 14 AWG pair, about a 5 A fuse holder, a switch, grommets',
            'A/C: heavy cable, big fuse, lugs and heat shrink, as its manual says',
            'Screws for the frames; the units&rsquo; own screws and gaskets']
    tools = ['Drill with bits and a step bit; jigsaw with fresh fine-tooth metal blades',
             'File or deburring tool, sandpaper, wire brush; a saw to rip the strips; a caulk gun',
             'Tape measure, square, level, straightedge, pencil, magnet (to find the ribs)',
             'Props or a board to hold each frame up overnight; spring clamps',
             'Plastic sheet, vacuum, a blanket to protect the paint',
             'Ladder, a board to kneel on across the ribs, a helper',
             'Gloves, safety glasses, hearing protection, a dust mask',
             'Multimeter; garden hose for the leak test']
    nook = ['OSI Quad Max (paintable hybrid sealant) for a thin bead where the plywood meets the wall covering; leave the top or bottom edge unsealed so the wool can breathe',
            'Havelock wool for the nook: a pad cut from a batt, about 7/8 in thick when fitted (split the batt into layers if it is thicker), cut about 1/4 in oversize so it stays put',
            '3/8 in plywood for the back of the jar nook (cut it about 35 1/8 x 15 7/8: the nook is 35 1/4 x 16, 38 to 54 in up). With 1 1/4 in spare behind the jars, 3/8 in plywood leaves 7/8 in for the wool',
            'Water-based polyurethane for the back and every edge of that plywood, two coats, cured for a few days before it goes in',
            'Isopropyl alcohol and rags to wipe the steel, touch-up white paint and rust-inhibiting primer for any chips in the factory paint']
    head = ('<h1>Roof fan and air conditioner: install steps</h1>'
            '<p class="lead">Drawn from the sizes in the plan. I have not seen the A/C manual, and the fan has no directions: where a manual would decide something, the step says so.</p>'
            '<div class="card warnbox"><h3 style="margin-top:0">Before you cut</h3><ul>'
            '<li><b>A/C:</b> I have not seen its manual. Its opening size, the roof thickness it clamps across and the most roof curve it allows decide the cut and the frame. The only figure I have is a minimum opening of 14.1 x 13.7 in. <b>If you do not have the manual in hand, cut and frame only the fan today</b> and leave the A/C for when you do.</li>'
            '<li><b>Fan:</b> it has no directions. This page uses what you measured: a 14 x 14 opening and 2 3/4 to 4 1/2 in from the roof to the trim.</li>'
            '<li><b>Weather:</b> cover every open hole (plastic or a board taped to clean, dry paint) whenever you stop, until its unit is on.</li></ul>'
            '<p class="swipe">On a phone, swipe a drawing sideways to see all of it.</p></div>'
            '<div class="card"><h3 style="margin-top:0">The numbers</h3>' + nums + '</div>'
            '<div class="card"><div class="cols"><div><h3 style="margin-top:0">Materials</h3><ul class="chk">'
            + ''.join(f'<li><input type="checkbox" data-s="m{i}"><span>{m}</span></li>' for i, m in enumerate(mats)) +
            '</ul></div><div><h3 style="margin-top:0">Tools</h3><ul class="chk">'
            + ''.join(f'<li><input type="checkbox" data-s="t{i}"><span>{t}</span></li>' for i, t in enumerate(tools)) +
            '</ul></div></div></div>'
            '<div class="card"><h3 style="margin-top:0">Also on your list: the storage nook back (a separate job from the roof)</h3><ul class="chk">'
            + ''.join(f'<li><input type="checkbox" data-s="n{i}"><span>{m}</span></li>' for i, m in enumerate(nook)) +
            '</ul></div>'
            '<div class="card"><h3 style="margin-top:0">Where the openings and ribs are</h3><div class="figwrap">' + fig_overview() + '</div>' +
            '<p style="margin:0;color:var(--mute);font-size:14px">Seen from above: rear doors on the left, cab on the right, driver side wall at the top. Dashed outlines are the units on the roof.</p></div>'
            '<div class="card"><h3 style="margin-top:0">Plan for the days</h3><div class="time">'
            '<div><b>Today</b>Steps 1 to 7: find the ribs, template, cut (the A/C only with its manual), deburr and prime, mark the fan&rsquo;s screw holes, build and bond the frames, prop overnight, cover the holes. Prep the wiring.</div>'
            '<div><b>Tomorrow morning</b>Step 8: mount the fan, then wire it.</div>'
            '<div><b>About 48 hours after bonding</b>Steps 9 to 11: A/C on, wire it, leak test.</div></div></div>')
    js = ("<script>(function(){var K='" + CHECK_KEY + "',s={};try{s=JSON.parse(localStorage.getItem(K)||'{}')||{};}catch(e){}"
          "document.querySelectorAll('input[data-s]').forEach(function(b){var k=b.dataset.s;b.checked=!!s[k];"
          "var c=b.closest('.card');if(c&&c.dataset.step&&b.checked)c.classList.add('done');"
          "b.addEventListener('change',function(){s[k]=b.checked;try{localStorage.setItem(K,JSON.stringify(s));}catch(e){}"
          "var c=b.closest('.card');if(c&&c.dataset.step)c.classList.toggle('done',b.checked);});});})();</script>")
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Fan and A/C install steps</title><style>' + CSS + '</style></head><body><div class="wrap">' + head + ''.join(S) +
            '<p class="lead">Back to <a href="interactive.html">the interactive plan</a>, <a href="window.html">the side window steps</a> or <a href="sides.html">the static diagrams</a>.</p>'
            '</div>' + js + '</body></html>')
    return page


if __name__ == '__main__':
    out = os.path.join(ROOT, 'install.html')
    open(out, 'w').write(build())
    print('install.html written,', os.path.getsize(out), 'bytes')
