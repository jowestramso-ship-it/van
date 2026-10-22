#!/usr/bin/env python3
"""Builds ../window-template.html: the TL201-SE measured from the owner's tape photos (IMG_0045 to 0050, 0056) and tape readings,
drawn to scale from inside, with the cutout (frame outline) numbers for a cardboard template.
Every measurement has a number in the drawing and in the table. Each one is marked: read from a tape,
worked out from the tapes, or an estimate from the full photo that still needs a tape.
Run from this folder (build.sh does):  python3 wtemplate.py
"""
import os, html, math
import install as I
import window as W
from install import svg, R, L, C, T, P, PL, fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- the numbers, inches
# Coordinates: x across from the glass's left edge, y up from the FRAME's bottom edge, seen from inside, frame level.
# The glass is not a rectangle (owner): 54 1/8 across the bottom, 52 1/2 across the top, 28 5/8 high on the left, 29 on the right,
# and the top margin above the frame is 3 1/2 at the frame's left end and 3 1/8 at its right end.
GWB, GWT = 54.125, 52.5          # glass width at the bottom / at the top                owner's tape
GHL, GHR = 28.625, 29.0          # glass height on the left / on the right (right along its edge)   owner's tape
TOP_L, TOP_R = 3.5, 3.125        # frame top edge to glass top edge, at the frame's left / right end   IMG_0045 / owner's tape
BOT_C = 3.125                    # frame bottom edge to glass bottom edge, along block C   IMG_0047 read 3 1/4; the owner corrected it to 3 1/8
RIGHT = 3.5                      # frame right edge to glass right edge, about 3 1/2 in below the frame top   IMG_0050  (tape)
LEFT_T, LEFT_B = 9.75, 9.625     # frame left edge to glass left edge, at the top rail / the bottom rail   owner's tapes
LEFT = (LEFT_T + LEFT_B) / 2     # the frame's left edge is drawn upright at the average: the 1/8 difference over its height is within the tape
FRIT = 7.5                       # black band ends at the dotted edge, from left    IMG_0046  (tape)
BLK_END = 8.75                   # right edge of the right block to the glass right edge   IMG_0048 (tape, +-1/2)
BLK_W = 1.625                    # block width, all three: owner's tape
BLK_LE = [15.75, 29.0, 43.625]   # left edge of blocks A, B, C from the left glass edge: owner's tape
BLK_C = [x + BLK_W / 2 for x in BLK_LE]   # block centers: the taped left edge plus half the estimated width
DIV = 28.625                     # slider divider from the left glass edge: owner's tape
RG, RGL = 2.75, 0.4              # glass corner radius right side, left side: full photo (estimate)
RF, RFL = 2.0, 0.5               # frame corner radius right side, left side: full photo (estimate)

# Worked out, assuming: the frame is a level rectangle, the glass's left edge is square to it, and the glass's top and bottom edges are straight.
XR = (GWB + GWT) / 2             # where along x the right-hand height was taken
FX0 = LEFT
FX1 = 49.4
for _ in range(8):               # the frame's right edge and the slopes depend on each other: settle them
    S_T = -(TOP_L - TOP_R) / (FX1 - FX0)                 # slope of the glass top edge against the level frame
    S_B = S_T - (GHR - GHL) / XR                         # slope of the glass bottom edge
    YB0 = -BOT_C - S_B * BLK_C[2]                        # glass bottom edge at the left glass edge, relative to the frame bottom
    HF = GHL + YB0 - TOP_L + S_T * FX0                   # frame height
    ytop = lambda x: HF + TOP_L + S_T * (x - FX0)
    ybot = lambda x: -BOT_C + S_B * (x - BLK_C[2])
    xg = lambda y: GWB + (GWT - GWB) * (y - ybot(GWB)) / (ytop(GWT) - ybot(GWB))
    FX1 = xg(HF - 3.5) - RIGHT
FY0, FY1 = 0.0, HF
BLK_LEN = [FY0 - ybot(c) for c in BLK_C]
BOT_L = FY0 - ybot(0)            # bottom margin at the left end
FW = FX1 - FX0
RIGHT_B = xg(1.0) - FX1          # right margin about 1 in above the frame bottom
YMAX = ytop(0)

EXTRA = W.EXTRA_CSS + """
.dimm { stroke: #8cc8ff; stroke-width: 1.6; }
.dime { stroke: #ffb35c; stroke-width: 1.6; stroke-dasharray: 5 3; }
.tm { font-size: 12.5px; font-weight: 700; fill: #9fd0ff; }
.te { font-size: 12.5px; font-weight: 700; fill: #ffbf7a; }
.frame2 { fill: #131416; stroke: #d9d9d9; stroke-width: 1.4; }
.screen { fill: #3e4339; }
.glassp { fill: #2c4a43; }
.panel { fill: #3b3d44; stroke: #9aa0a8; stroke-width: 1.6; }
.fritl { stroke: #c9c9c9; stroke-width: 1.2; stroke-dasharray: 3 3; }
.mkm { fill: #fff; stroke: #1f6fb2; stroke-width: 2.2; }
.mke { fill: #fff; stroke: #d9801f; stroke-width: 2.2; }
.tmk { font-size: 11px; font-weight: 800; fill: #111; }
.chip { display: inline-block; border-radius: 10px; padding: 0 8px; font-size: 13px; font-weight: 700; color: #fff; }
.c-m { background: #1f6fb2; } .c-e { background: #b8651a; } .c-n { background: #8a2f2f; }
.mid { display: inline-flex; align-items: center; justify-content: center; width: 24px; height: 24px; border-radius: 50%; border: 2px solid #1f6fb2; background: #fff; color: #111; font-weight: 800; font-size: 12px; }
.mid.e { border-color: #d9801f; }
td.num { white-space: nowrap; font-weight: 700; }
"""


def rr(l, t, r, b, tl, tr, br, bl, cls):
    """rounded rect in pixels with a different radius on each corner"""
    d = (f'M {l + tl:.1f} {t:.1f} L {r - tr:.1f} {t:.1f} A {tr:.1f} {tr:.1f} 0 0 1 {r:.1f} {t + tr:.1f} '
         f'L {r:.1f} {b - br:.1f} A {br:.1f} {br:.1f} 0 0 1 {r - br:.1f} {b:.1f} '
         f'L {l + bl:.1f} {b:.1f} A {bl:.1f} {bl:.1f} 0 0 1 {l:.1f} {b - bl:.1f} '
         f'L {l:.1f} {t + tl:.1f} A {tl:.1f} {tl:.1f} 0 0 1 {l + tl:.1f} {t:.1f} Z')
    return f'<path d="{d}" class="{cls}"/>'


def rpoly(pts, radii, cls):
    """polygon (pixel points) with a rounded corner at each vertex"""
    n = len(pts)
    segs = []
    for i in range(n):
        p0, p1, p2 = pts[i - 1], pts[i], pts[(i + 1) % n]
        r = radii[i]

        def toward(a, b, d):
            dx, dy = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(dx, dy)
            return (a[0] + dx / ln * d, a[1] + dy / ln * d)
        segs.append((toward(p1, p0, r), p1, toward(p1, p2, r)))
    d = f'M {segs[0][2][0]:.1f} {segs[0][2][1]:.1f}'
    for i in range(1, n + 1):
        a_, v, b_ = segs[i % n]
        d += f' L {a_[0]:.1f} {a_[1]:.1f} Q {v[0]:.1f} {v[1]:.1f} {b_[0]:.1f} {b_[1]:.1f}'
    return f'<path d="{d} Z" class="{cls}"/>'


def glass_path(X, Y, S, cls):
    pts = [(X(0), Y(ytop(0))), (X(GWT), Y(ytop(GWT))), (X(GWB), Y(ybot(GWB))), (X(0), Y(ybot(0)))]      # top-left, top-right, bottom-right, bottom-left
    return rpoly(pts, [RGL * S, RG * S, RG * S, RGL * S], cls)


def marker(px, py, n, kind):
    return C(px, py, 10, 'mkm' if kind == 'm' else 'mke') + f'<text x="{px:.1f}" y="{py + 3.8:.1f}" class="tmk" text-anchor="middle">{n}</text>'


# ---------------------------------------------------------------- the measurements: number, what, value, kind, where it came from
# kind: m = read off a tape, e = worked out from tapes, n = estimate from the full photo, still needs a tape
MEAS = [
    (1, 'Glass width, bottom edge', fr(GWB), 'm', 'your tape (the listing says 54 3/8)'),
    (2, 'Glass width, top edge', fr(GWT), 'm', 'your tape: the right edge leans in toward the top'),
    (3, 'Glass height, left edge', fr(GHL), 'm', 'your tape (the listing says 29 1/8)'),
    (4, 'Glass height, right edge', fr(GHR), 'm', 'your tape'),
    (5, 'Top margin at the frame&rsquo;s left end', fr(TOP_L), 'm', 'IMG_0045, and your message'),
    (6, 'Top margin at the frame&rsquo;s right end', fr(TOP_R), 'm', 'your message'),
    (7, 'Bottom margin, along block C', fr(BOT_C), 'm', 'IMG_0047 (I read 3 1/4 from the photo; you corrected it to 3 1/8)'),
    (8, 'Bottom margin at the left end', '~' + fr(BOT_L), 'e', 'worked out from 3, 4, 5, 6 and 7'),
    (9, 'Right margin, about 3 1/2 in below the frame top', fr(RIGHT), 'm', 'IMG_0050 (T-square held to the frame, tape to the glass)'),
    (10, 'The same margin, 1 in above the frame bottom', '~' + fr(RIGHT_B), 'e', 'worked out from the lean: it grows going down'),
    (11, 'Right block, its far edge to the glass right edge', fr(BLK_END), 'm', 'IMG_0048 (hook on the block&rsquo;s edge, about 1/2 in either way)'),
    (12, 'Black band on the glass: left edge to where it ends (the row of dots where the black fades into clear glass)', fr(FRIT), 'm', 'IMG_0046, and you confirmed 7 1/2 (measured from the left edge)'),
    (13, 'Frame left edge, top rail, from the glass left edge', fr(LEFT_T), 'm', 'your message'),
    (14, 'Block A, its left edge from the glass left edge', fr(BLK_LE[0]), 'm', 'your message (so its center is about ' + fr(BLK_C[0]) + ')'),
    (15, 'Block B, its left edge from the glass left edge', fr(BLK_LE[1]), 'm', 'your message (center about ' + fr(BLK_C[1]) + ')'),
    (16, 'Block C, its left edge from the glass left edge', fr(BLK_LE[2]), 'm', 'your message (center about ' + fr(BLK_C[2]) + ')'),
    (17, 'Slider divider, from the glass left edge', fr(DIV), 'm', 'your message'),
    (18, 'Block width, A, B and C', fr(BLK_W), 'm', 'your message'),
    (19, 'Block lengths, A / B / C', '~' + ' / '.join(fr(b) for b in BLK_LEN), 'e', 'frame bottom to glass edge, from the sloping bottom edge: tape them to check'),
    (20, 'Frame outer width', '~' + fr(FW), 'e', f'from 13 and 9 and the lean (right edge at ~{fr(FX1)}): tape it across the outer lips'),
    (21, 'Frame outer height', '~' + fr(HF), 'e', 'from 3, 5, 7 and the slopes: tape it across the outer lips'),
    (22, 'Glass corner radii, right / left', f'~{fr(RG)} / {fr(RGL)}', 'n', 'full photo only; a radius gauge or a compass will settle it'),
    (23, 'Frame corner radii, right / left', f'~{fr(RF)} / {fr(RFL)}', 'n', 'full photo only'),
    (24, 'Frame left edge, bottom rail, from the glass left edge', fr(LEFT_B), 'm', 'your message: 1/8 less than the top rail, so the glass left edge is square to the frame within about 1/8'),
]
KIND = {m[0]: m[3] for m in MEAS}


def fig_window():
    S = 11.5
    ox, oy = 76, 70
    X = lambda x: ox + x * S
    Y = lambda y: oy + (YMAX - y) * S
    mk = lambda n, x, y: marker(X(x), Y(y), n, 'm' if KIND[n] == 'm' else 'e')
    o = []
    o.append(T(ox + GWB * S / 2, 20, 'TL201-SE seen from inside, frame level, to scale. Numbers match the table', 'tb'))
    o.append(glass_path(X, Y, S, 'panel'))
    o.append(L(X(GWB), Y(ybot(GWB)), X(GWB), Y(ytop(GWT)), 'fritl'))
    # frame
    o.append(rr(X(FX0), Y(FY1), X(FX1), Y(FY0), RFL * S, RF * S, RF * S, RFL * S, 'frame2'))
    pad = 1.0
    o.append(rr(X(FX0 + pad), Y(FY1 - pad), X(DIV), Y(FY0 + pad), 0.6 * S, 0, 0, 0.6 * S, 'glassp'))
    o.append(rr(X(DIV), Y(FY1 - pad), X(FX1 - pad), Y(FY0 + pad), 0, 1.4 * S, 1.4 * S, 0, 'screen'))
    o.append(T(X((FX0 + DIV) / 2), Y(FY1 / 2) - 8, 'glass', 'tdark'))
    o.append(T(X((DIV + FX1) / 2), Y(FY1 / 2) - 8, 'screen', 'tdark'))
    # 12: where the black band (the dots) ends, from the left glass edge
    o.append(L(X(FRIT), Y(FY1 + 1.2), X(FRIT), Y(FY0 - 1.2), 'fritl'))
    y12 = 11.0
    o.append(L(X(0) + 3, Y(y12), X(FRIT) - 3, Y(y12), 'dimm'))
    o.append(T(X(FRIT / 2), Y(y12) - 6, fr(FRIT), 'tm'))
    o.append(T(X(FRIT / 2), Y(y12) + 17, 'black band', 'tm'))
    o.append(T(X(FRIT / 2), Y(y12) + 32, '(dots) ends', 'tm'))
    o.append(mk(12, FRIT, y12))
    # blocks, 14 to 19
    for i, c in enumerate(BLK_C):
        o.append(R(X(c - BLK_W / 2), Y(FY0), BLK_W * S, BLK_LEN[i] * S - 2, 'blk', 2))
        o.append(T(X(c), Y(FY0) + 17, 'ABC'[i], 'tdark'))
        o.append(T(X(c), Y(ybot(c)) + 17, fr(BLK_LE[i]) + ' to its left edge', 'tm'))
        o.append(L(X(c), Y(ybot(c)), X(c), Y(ybot(c)) + 5, 'dimm'))
        o.append(mk(14 + i, c, ybot(c) - 3.4))
    o.append(mk(18, BLK_C[0] - BLK_W / 2 - 1.2, FY0 - 1.3))
    o.append(mk(19, BLK_C[1] + BLK_W / 2 + 1.2, FY0 - 1.6))
    # 5 and 6: top margins
    mx5 = FX0 + 6.0
    o.append(L(X(mx5), Y(ytop(mx5)) + 3, X(mx5), Y(FY1) - 3, 'dimm'))
    o.append(T(X(mx5) + 6, (Y(ytop(mx5)) + Y(FY1)) / 2 + 4, fr(TOP_L), 'tm', 'start'))
    o.append(mk(5, mx5 - 1.4, (ytop(mx5) + FY1) / 2))
    mx6 = FX1 - 5.0
    o.append(L(X(mx6), Y(ytop(mx6)) + 3, X(mx6), Y(FY1) - 3, 'dimm'))
    o.append(T(X(mx6) + 6, (Y(ytop(mx6)) + Y(FY1)) / 2 + 4, fr(TOP_R), 'tm', 'start'))
    o.append(mk(6, mx6 - 1.4, (ytop(mx6) + FY1) / 2))
    # 9 and 10: right margins
    YR = FY1 - 3.5
    o.append(L(X(FX1) + 3, Y(YR), X(xg(YR)) - 3, Y(YR), 'dimm'))
    o.append(T((X(FX1) + X(xg(YR))) / 2, Y(YR) - 6, fr(RIGHT), 'tm'))
    o.append(mk(9, (FX1 + xg(YR)) / 2, YR - 2.4))
    yb = FY0 + 1.0
    o.append(L(X(FX1) + 3, Y(yb), X(xg(yb)) - 3, Y(yb), 'dime'))
    o.append(T((X(FX1) + X(xg(yb))) / 2, Y(yb) - 6, '~' + fr(xg(yb) - FX1), 'te'))
    o.append(mk(10, (FX1 + xg(yb)) / 2, yb + 2.3))
    # 7 and 8: bottom margins
    bx = BLK_C[2] - 3.5
    o.append(L(X(bx), Y(FY0) + 3, X(bx), Y(ybot(bx)) - 3, 'dimm'))
    o.append(T(X(bx) - 6, (Y(FY0) + Y(ybot(bx))) / 2 + 4, fr(BOT_C), 'tm', 'end'))
    o.append(mk(7, bx + 1.4, (FY0 + ybot(bx)) / 2))
    o.append(L(X(1.5), Y(FY0) + 3, X(1.5), Y(ybot(1.5)) - 3, 'dime'))
    o.append(T(X(1.5) + 6, (Y(FY0) + Y(ybot(1.5))) / 2 + 4, '~' + fr(BOT_L), 'te', 'start'))
    o.append(mk(8, 6.9, (FY0 + ybot(1.5)) / 2))
    # 11: right block to the right edge
    c3r = BLK_C[2] + BLK_W / 2
    y11 = -1.6
    o.append(L(X(c3r) + 2, Y(y11), X(xg(y11)) - 3, Y(y11), 'dimm'))
    o.append(T((X(c3r) + X(xg(y11))) / 2, Y(y11) - 5, fr(BLK_END), 'tm'))
    o.append(mk(11, (c3r + xg(y11)) / 2, y11 - 1.5))
    # 13 and 24: frame left edge at the top and bottom rails (tapes)
    ey = FY1 - 0.7
    o.append(L(X(0) + 3, Y(ey), X(LEFT_T) - 3, Y(ey), 'dimm'))
    o.append(T(X(LEFT_T / 2), Y(ey) - 6, fr(LEFT_T), 'tm'))
    o.append(mk(13, LEFT_T / 2, ey - 2.2))
    ey2 = FY0 + 0.7
    o.append(L(X(0) + 3, Y(ey2), X(LEFT_B) - 3, Y(ey2), 'dimm'))
    o.append(T(X(LEFT_B / 2), Y(ey2) - 6, fr(LEFT_B), 'tm'))
    o.append(mk(24, LEFT_B / 2, ey2 + 2.2))
    # 17: divider
    o.append(T(X(DIV) + 14, Y(FY1) - 6, fr(DIV) + ' from the left', 'tm', 'start'))
    o.append(mk(17, DIV, FY1 + 0.8))
    # 20 and 21: frame size, worked out
    y20 = 2.2
    o.append(L(X(FX0) + 3, Y(y20), X(FX1) - 3, Y(y20), 'dime'))
    o.append(T(X((FX0 + FX1) / 2), Y(y20) - 6, '~' + fr(FW) + ' wide', 'te'))
    o.append(mk(20, FX0 + 6.0, y20 + 1.0))
    x21 = FX1 - 2.6
    o.append(L(X(x21), Y(FY1) + 14, X(x21), Y(FY0) - 14, 'dime'))
    o.append(f'<text x="{X(x21) - 6:.1f}" y="{Y(FY1 * 0.5) + 2:.1f}" class="te" text-anchor="end">~{fr(HF)} tall</text>')
    o.append(mk(21, x21 + 1.6, FY1 * 0.5 + 1.2))
    # 22 and 23: corner radii
    o.append(mk(22, GWT - 1.35, ytop(GWT) - 1.2))
    o.append(mk(23, FX1 - 0.9, FY1 - 0.95))
    # 1, 2, 3, 4: glass overall
    ty = oy - 18
    o.append(L(X(0), ty, X(GWT), ty, 'dim'))
    o.append(L(X(0), ty - 4, X(0), ty + 4, 'dim'))
    o.append(L(X(GWT), ty - 4, X(GWT), ty + 4, 'dim'))
    o.append(T(X(GWT / 2), ty - 5, fr(GWT) + ' across the top (your tape)', 'tdim'))
    o.append(marker(X(GWT / 2) - 150, ty - 9, 2, 'm'))
    by2 = Y(ybot(GWB)) + 66
    o.append(L(X(0), by2, X(GWB), by2, 'dim'))
    o.append(L(X(0), by2 - 4, X(0), by2 + 4, 'dim'))
    o.append(L(X(GWB), by2 - 4, X(GWB), by2 + 4, 'dim'))
    o.append(T(X(GWB / 2), by2 + 16, fr(GWB) + ' across the bottom (your tape)', 'tdim'))
    o.append(marker(X(GWB / 2) - 150, by2 + 12, 1, 'm'))
    lx = ox - 16
    o.append(L(lx, Y(ytop(0)), lx, Y(ybot(0)), 'dim'))
    o.append(L(lx - 4, Y(ytop(0)), lx + 4, Y(ytop(0)), 'dim'))
    o.append(L(lx - 4, Y(ybot(0)), lx + 4, Y(ybot(0)), 'dim'))
    cy = (Y(ytop(0)) + Y(ybot(0))) / 2
    o.append(f'<text x="{lx - 6:.1f}" y="{cy:.1f}" class="tdim" text-anchor="middle" transform="rotate(-90 {lx - 6:.1f} {cy:.1f})">{fr(GHL)} (your tape)</text>')
    o.append(marker(lx, cy - 80, 3, 'm'))
    rx = X(GWB) + 20
    o.append(L(rx, Y(ytop(GWT)), rx, Y(ybot(GWB)), 'dim'))
    o.append(L(rx - 4, Y(ytop(GWT)), rx + 4, Y(ytop(GWT)), 'dim'))
    o.append(L(rx - 4, Y(ybot(GWB)), rx + 4, Y(ybot(GWB)), 'dim'))
    cy2 = (Y(ytop(GWT)) + Y(ybot(GWB))) / 2
    o.append(f'<text x="{rx + 14:.1f}" y="{cy2:.1f}" class="tdim" text-anchor="middle" transform="rotate(90 {rx + 14:.1f} {cy2:.1f})">{fr(GHR)} (your tape)</text>')
    o.append(marker(rx, cy2 - 80, 4, 'm'))
    # origin and legend
    o.append(C(X(0), Y(ybot(0)), 4, 'drill'))
    ly = by2 + 56
    o.append(L(ox, ly, ox + 40, ly, 'dimm'))
    o.append(C(ox + 20, ly, 10, 'mkm'))
    o.append(T(ox + 20, ly + 3.8, 'n', 'tmk'))
    o.append(T(ox + 52, ly + 4, 'read off a tape (yours or in your photo)', 'tsm', 'start'))
    o.append(L(ox + 320, ly, ox + 360, ly, 'dime'))
    o.append(C(ox + 340, ly, 10, 'mke'))
    o.append(T(ox + 340, ly + 3.8, 'n', 'tmk'))
    o.append(T(ox + 372, ly + 4, 'worked out, or estimated from the photo', 'tsm', 'start'))
    o.append(T(ox, ly + 30, 'Assumed: the frame is level, the glass&#39;s left edge is square to it, and its top and bottom edges are straight.'.replace('&#39;', "'"), 'tsm', 'start'))
    o.append(T(ox, ly + 46, 'The dotted line is straight up from the bottom-right corner, to show the right edge leaning in.', 'tsm', 'start'))
    return svg(760, int(ly + 60), ''.join(o), 'The TL201-SE from inside, to scale, with every measurement numbered: glass, frame, three blocks')


def fig_cut():
    """the cardboard template: the glass outline with the frame opening and the blocks"""
    S = 11.0
    ox, oy = 50, 40
    X = lambda x: ox + x * S
    Y = lambda y: oy + (YMAX - y) * S
    o = []
    o.append(glass_path(X, Y, S, 'flange'))
    o.append(rr(X(FX0), Y(FY1), X(FX1), Y(FY0), RFL * S, RF * S, RF * S, RFL * S, 'cutline'))
    o.append(T(X((FX0 + FX1) / 2), Y(FY1 / 2) - 2, 'cut this out of the cardboard', 'tb'))
    o.append(T(X((FX0 + FX1) / 2), Y(FY1 / 2) + 16, '~' + fr(FW) + ' wide x ~' + fr(HF) + ' tall (draft)', 'tgrey'))
    o.append(T(X(GWT / 2), Y(ytop(GWT / 2)) - 8, 'glass outline = the cardboard&#39;s outer edge'.replace('&#39;', "'"), 'tsm'))
    for i, c in enumerate(BLK_C):
        o.append(R(X(c - BLK_W / 2), Y(FY0), BLK_W * S, BLK_LEN[i] * S - 2, 'blk', 2))
    yb = Y(ybot(GWB))
    o.append(T(X(GWB / 2), yb + 22, 'Dashed red: the opening to cut. Grey: the three blocks,', 'tsm'))
    o.append(T(X(GWB / 2), yb + 38, 'marked so you can check that the stamping clears them.', 'tsm'))
    return svg(700, int(yb + 52), ''.join(o), 'The cardboard template: glass outline with the frame opening cut out and the three blocks marked')


def row(n, item, val, tag, src):
    chip = {'m': '<span class="chip c-m">tape</span>', 'e': '<span class="chip c-e">worked out</span>', 'n': '<span class="chip c-n">estimate</span>'}[tag]
    kind = '' if tag == 'm' else ' e'
    return f'<tr><td><span class="mid{kind}">{n}</span></td><td>{item}</td><td class="num">{val}</td><td>{chip}</td><td>{src}</td></tr>'


def build():
    rows = [row(*m) for m in MEAS]
    # corner points for the cardboard: from the glass's bottom-left corner, x across, y up, frame level
    ox0, oy0 = 0.0, ybot(0)
    P_ = lambda x, y: f'({fr(x - ox0)}, {fr(y - oy0)})'
    corner_rows = (
        f'<tr><td>Bottom-left</td><td class="num">{P_(0, ybot(0))}</td></tr>'
        f'<tr><td>Top-left</td><td class="num">{P_(0, ytop(0))}</td></tr>'
        f'<tr><td>Top-right (before rounding)</td><td class="num">{P_(GWT, ytop(GWT))}</td></tr>'
        f'<tr><td>Bottom-right (before rounding)</td><td class="num">{P_(GWB, ybot(GWB))}</td></tr>'
        f'<tr><td>Opening, bottom-left</td><td class="num">{P_(FX0, FY0)}</td></tr>'
        f'<tr><td>Opening, top-right</td><td class="num">{P_(FX1, FY1)}</td></tr>')
    todo = [
        '<b>The shape of the glass:</b> your 54 1/8 across the bottom, 52 1/2 across the top, 28 5/8 high on the left, 29 on the right, and 3 1/2 and 3 1/8 for the top margin are in (numbers 1 to 6). Both diagonals (corner to corner) would settle the shape. You said the area around 50 gets wider the further down: I drew one straight lean on the right edge. If it is a step or a bend, tell me where it starts.',
        '<b>What I assumed:</b> the frame is level, the glass&rsquo;s left edge is square to it, and the top and bottom edges are straight. Check the left edge with a square against the frame&rsquo;s bottom edge.',
        f'<b>The frame, outer lip to outer lip (20 and 21):</b> across and up. Its left edge is in (13 and 24). And the bottom margin at the frame&rsquo;s left end (8): I make it about {fr(BOT_L)}.',
        '<b>The blocks (19):</b> I have the left edge and the width of all three blocks (14 to 18). Tape each one&rsquo;s length, from the frame&rsquo;s bottom edge to the glass edge. I worked them out from the sloping bottom edge, so if they come out the same, the bottom edge is not as sloped as I drew it.',
        '<b>Which edge each photo was:</b> I took 0045 as the top, at the frame&rsquo;s left end; 0047 and 0048 as the bottom, along the right-hand block; 0050 as the right (top right corner); and 0046 as the left (you confirmed its 7 1/2). Tell me where I am wrong.',
        '<b>How far the frame sits proud of the glass</b> (its depth toward the inside): that decides how much room the cutout has behind it.',
        '<b>The van:</b> the same opening, measured on the stamping: width, height and corner radius. The template is only useful once you can compare the two.',
    ]
    steps = [
        f'Cardboard (or thin ply) a little over <b>{fr(GWB)} x {fr(GHR)}</b>. Mark the corner points in the table below, measuring from the bottom-left corner: across, then up. Use a level or a square for &ldquo;up&rdquo;, so the frame lines come out level. Join the four corners with straight lines and round the right corners at about <b>2 3/4 in</b> and the left ones at about <b>3/8 in</b>.',
        f'Mark the opening: the bottom edge <b>{fr(FY0 - oy0)}</b> up from the bottom-left corner, the top edge <b>{fr(FY1 - oy0)}</b> up, the left edge <b>{fr(FX0)}</b> in and the right edge <b>{fr(FX1)}</b> in, all level and upright. Round its right corners at about <b>2 in</b>. The glass edge should be about {fr(TOP_L)} above the opening at its left end and {fr(TOP_R)} at its right end.',
        f'Mark the three blocks, {fr(BLK_W)} wide, centered about <b>{", ".join(fr(c) for c in BLK_C)}</b> in from the left, each running from the opening&rsquo;s bottom edge to the glass edge.',
        'Cut out the opening. Test it against the window (the frame should drop in with the cardboard sitting on the glass face) and fix any number that does not match.',
        '<b>Seen from outside the van the drawing is a mirror image:</b> flip the cardboard over, or turn the numbers around, before you trace.',
        'Hold it on the van: the glass outline must sit inside the stamping&rsquo;s recess with margin all round, and the opening must clear the stamping&rsquo;s inner edge. Then trace and use it as the cut line, once the numbers are confirmed.',
    ]
    head = ('<h1>Side window: template</h1>'
            '<p class="lead">Drawn from your tape readings, your photos (IMG_0045 to 0050) and the full picture (0056). Every measurement has a number in the drawing and in the table. Blue ones were read off a tape, orange ones I worked out or estimated. '
            'The window is a big black glass panel, narrower at the top than the bottom, with the slider frame bonded in it, and three blocks along the bottom edge. The frame is what goes through the van&rsquo;s opening, so its outline is the cut.</p>'
            '<div class="card warnbox"><h3 style="margin-top:0">This is a draft</h3>'
            '<p style="margin:0">The blue numbers are good to about 1/8 in. The orange ones (the frame&rsquo;s size, the corner radii and everything worked out from the slopes) are not. '
            '<b>Do not cut the van from this yet.</b> Confirm the orange numbers first, and check the template against the stamping.</p>'
            '<p class="swipe">On a phone, swipe a drawing sideways to see all of it.</p></div>'
            '<div class="card"><div class="figwrap">' + fig_window() + '</div></div>'
            '<div class="card"><h2>The numbers</h2><div class="figwrap"><table style="min-width:600px"><tr><th>#</th><th>What</th><th>Inches</th><th></th><th>From</th></tr>' + ''.join(rows) + '</table></div></div>'
            '<div class="card"><h2>The cardboard template</h2><div class="figwrap">' + fig_cut() + '</div><ol>' + I.li(steps) + '</ol>'
            '<h3>Corner points, inches from the bottom-left corner (across, up)</h3><div class="figwrap"><table style="min-width:420px">' + corner_rows + '</table></div></div>'
            '<div class="card"><h2>What to confirm, and what to measure</h2><ul>' + I.li(todo) + '</ul></div>')
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Side window template</title><style>' + I.CSS + EXTRA + '</style></head><body><div class="wrap">' + head +
            '<p class="lead">Back to <a href="window.html">the side window steps</a>, <a href="interactive.html">the interactive plan</a> or <a href="sides.html">the static diagrams</a>.</p>'
            '</div></body></html>')
    return page


if __name__ == '__main__':
    out = os.path.join(ROOT, 'window-template.html')
    open(out, 'w').write(build())
    print('window-template.html written,', os.path.getsize(out), 'bytes')
    print('frame x', fr(FX0), fr(FX1), 'w', fr(FW), 'h', fr(HF), 'bottom margin left', fr(BOT_L), 'right margin at bottom', fr(RIGHT_B),
          'block lengths', [fr(b) for b in BLK_LEN], 'slopes', round(S_T, 4), round(S_B, 4), 'glass corners y', fr(ytop(0) - ybot(0)), fr(ytop(GWT) - ybot(GWB)))
