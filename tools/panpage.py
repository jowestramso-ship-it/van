"""The shower pan page of the build guide: how to set the bought 36 x 24 pan, drain it and line the stall with a thin waterproof (FRP) liner over the 3/8 in plywood.
Six drawings made from the plan's numbers (the pan, W3, the nook, the head and the valve, the drain hole), a parts table and the steps in order.
Used by buildguide.py (the Shower pan page); run on its own it writes ../pan.html for a quick look.
The drain hole is at the middle of the rear-door end, 5 in from the rear end (the user's measurement; the 12 in out from the wall is the middle of the depth, assumed), the pan's lip height against the wall is a guess,
and FRP is the user's choice ('I'll use FRP paneling'): change them here, in ia_core.js (pdrX, pdrY, linerT, linerTop, linerGap) and in plan.py together."""
import os

INK = '#2C2C2A'; PLY = '#E8CF9C'; PLYD = '#B8975A'; HARD = '#C9A263'; STEEL = '#9AA0A8'; FURR = '#7A4A1E'; SEAL = '#4F8C74'; TEAL = '#2A9D8F'; TEALD = '#1F7A70'
RED = '#A32D2D'; BLU = '#185FA5'; PAN = '#CFE3F3'; AMB = '#D4A017'; GRY = '#D8D8D4'; WOOD = '#C8A878'

# the numbers, the same as the plan
PW, PD = 36, 24                 # the pan: length along the wall, depth out from it
W3X = 35.25                     # W3 (3/4 in plywood) stands at 35 1/4 to 36
PANTOP = 3.8                    # top of the pan's curb and lip: 3 in over the 0.8 in floor
GAP = .25                       # the liner stops this far above the pan edge, the gap filled with flexible sealant
ZB, ZT = PANTOP + GAP, 74       # the liner's bottom and top, up from the floor
H = ZT - ZB                     # 69 15/16
LT = .09                        # the liner's thickness
NOOK = (12.5, 29.75, 38, 54)    # the shower nook: x0, x1, z0, z1 (4 1/2 in deep, in the wall)
HEAD = (9, 70); VALVE = (33, 44)
DRAIN = (5, 12)                 # 5 in from the rear end (the user), 12 out = the middle of the depth (assumed)
TOILET = (20.75, 35.25, 4.75, 19.25)

def fr(v):
    n = round(v * 16); w, e = divmod(n, 16)
    if e == 0: return str(w)
    from math import gcd
    g = gcd(e, 16); return (f'{w} ' if w else '') + f'{e // g}/{16 // g}'

def _r(x, y, w, h, fill, stroke=INK, sw=1.1, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def _p(pts, fill, stroke=INK, sw=1.1, extra=''):
    return '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def _l(x1, y1, x2, y2, col=INK, sw=1, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d}/>'
def _t(x, y, s, sz=12, anchor='start', col=INK, w=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="font-size:{sz}px;font-weight:{w};fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round">{s}</text>'
def _call(x, y, tx, ty, s, anchor='start', col=INK, sz=12):
    """a label with a leader line from the label to the point (x, y)"""
    return _l(tx + (3 if anchor == 'start' else -3), ty, x, y, col, 1) + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{col}"/>' + _t(tx + (8 if anchor == 'start' else -8), ty + 4, s, sz, anchor, col)
def _arrow(x1, y1, x2, y2, col=BLU, sw=2):
    import math
    a = math.atan2(y2 - y1, x2 - x1); L = 8
    h = [(x2, y2), (x2 - L * math.cos(a - .45), y2 - L * math.sin(a - .45)), (x2 - L * math.cos(a + .45), y2 - L * math.sin(a + .45))]
    return _l(x1, y1, x2 - 4 * math.cos(a), y2 - 4 * math.sin(a), col, sw) + _p(h, col, col, .5)
def _dim(x1, y1, x2, y2, s, off=0, col=INK, sz=11):
    """a dimension line with arrow heads and its label in the middle (horizontal or vertical)"""
    mx, my = (x1 + x2) / 2, (y1 + y2) / 2
    o = _arrow(mx, my, x1, y1, col, 1) + _arrow(mx, my, x2, y2, col, 1)
    if y1 == y2: o += _t(mx, my - 5, s, sz, 'middle', col, 600)
    else: o += _t(mx + 6, my + 4, s, sz, 'start', col, 600)
    return o
def _hatch(id_, col=STEEL):
    return f'<defs><pattern id="{id_}" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="{col}" stroke-width="2"/></pattern></defs>'
def _svg(w, h, body, title):
    return f'<svg viewBox="0 0 {w} {h}" role="img" style="width:100%;height:auto;display:block;background:#fff;border-radius:6px"><title>{title}</title>{body}</svg>'

# ---- A  from above ---------------------------------------------------------------------------------------------------------
def fig_top():
    S = 13.0; OX = 110; OY = 100
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    o = []; a = o.append
    a(_t(20, 24, 'A  From above: the pan, its drain, the liner on the wall and on W3 (passenger wall at the top)', 14, 'start', INK, 700))
    a(_r(X(12.5), Y(-4.5), S * 17.25, S * 4.5, '#F6EBD4', FURR, 1.2, 'stroke-dasharray="5 3"')); a(_t(X(21.1), Y(-1.6), 'shower nook, 4 1/2 deep (in the wall)', 10.5, 'middle', FURR))
    a(_r(X(-2), Y(-.375), S * 38.5, S * .375 + 1, PLY, INK, 1)); a(_t(X(-2), Y(-.375) - 6, 'passenger wall: 3/8 in plywood', 10.5, 'start', '#5F5E5A'))
    a(_r(X(W3X), Y(0), S * .75, S * PD, PLY, INK, 1)); a(_t(X(36.3), Y(PD / 2), 'W3', 12, 'start', INK, 700))
    a(_r(X(0), Y(0), S * PW, S * PD, PAN, BLU, 2.2)); a(_r(X(1.5), Y(1.5), S * (PW - 3), S * (PD - 3), 'none', BLU, 1, 'stroke-dasharray="4 3"'))
    a(_l(X(0), Y(0) + 2, X(W3X), Y(0) + 2, TEAL, 4)); a(_l(X(W3X) - 2, Y(0), X(W3X) - 2, Y(PD), TEAL, 4))
    a(_t(X(2), Y(0) + 17, 'liner on the wall', 10.5, 'start', TEALD, 600)); a(_t(X(W3X) - 7, Y(PD) - 6, 'liner on W3', 10.5, 'end', TEALD, 600))
    tx0, tx1, ty0, ty1 = TOILET
    a(_r(X(tx0), Y(ty0), S * (tx1 - tx0), S * (ty1 - ty0), 'none', '#993556', 1.6, 'stroke-dasharray="6 3"')); a(_t(X((tx0 + tx1) / 2), Y((ty0 + ty1) / 2) + 4, 'toilet (folded away or in use)', 10.5, 'middle', '#993556'))
    a(f'<circle cx="{X(HEAD[0]):.1f}" cy="{Y(6):.1f}" r="7" fill="#fff" stroke="{BLU}" stroke-width="1.6"/>' + _t(X(HEAD[0]) + 11, Y(6) + 4, 'shower head', 10.5, 'start', BLU))
    dx, dy = DRAIN
    a(f'<circle cx="{X(dx):.1f}" cy="{Y(dy):.1f}" r="{S * 1.1:.1f}" fill="{INK}"/>')
    a(_t(X(dx) + 22, Y(dy) - 32, 'drain hole', 12, 'start', INK, 700)); a(_t(X(dx) + 22, Y(dy) - 18, f'{fr(dx)} in along, {fr(dy)} out', 11, 'start', INK)); a(_t(X(dx) + 22, Y(dy) - 4, '(12 out: check it)', 11, 'start', RED, 600))
    a(_arrow(X(14), Y(17), X(6.6), Y(13.3), BLU, 1.6)); a(_arrow(X(14), Y(13.8), X(6.5), Y(12.7), BLU, 1.6)); a(_arrow(X(2.2), Y(21), X(3.4), Y(14.4), BLU, 1.6))
    a(_t(X(9), Y(21) + 2, 'floor falls to the drain', 10.5, 'start', BLU))
    a(_t(X(0) - 8, Y(18), 'rear-door end', 11, 'end', '#5F5E5A', 600)); a(_t(X(0) - 8, Y(18) + 13, '(the curtain)', 10.5, 'end', '#5F5E5A'))
    yb = Y(PD) + 30
    a(_dim(X(0), yb, X(PW), yb, f'{PW} in')); a(_dim(X(0), yb + 22, X(dx), yb + 22, f'{fr(dx)}'))
    a(_dim(X(PW) + 52, Y(0), X(PW) + 52, Y(PD), f'{PD} in')); a(_dim(X(0) - 24, Y(0), X(0) - 24, Y(dy), f'{fr(dy)}'))
    a(_t(X(PW / 2), Y(PD) + 12, 'open side: curtain', 10.5, 'middle', '#5F5E5A'))
    return _svg(760, 500, ''.join(o), 'The shower pan from above')

# ---- B  section at the wall: the pan edge, the sealed gap and the liner ---------------------------------------------------------
def fig_edge():
    S = 40.0; OX = 190; FL = 360
    X = lambda x: OX + S * x; Z = lambda z: FL - S * z
    o = []; a = o.append
    a(_hatch('hB'))
    a(_t(20, 24, 'B  The pan edge against the wall: a section across the stall (the wall on the left)', 14, 'start', INK, 700))
    a(_r(X(-1.7), Z(6.9), S * 1.3, S * 6.9, 'url(#hB)', STEEL, 1)); a(_t(X(-1.7) + 2, Z(6.9) - 5, 'steel wall', 10.5, 'start', '#5F5E5A'))
    a(_r(X(-.375), Z(6.9), S * .375, S * (6.9 - 1.05), PLY, INK, 1.1)); a(_r(X(-1.7), Z(0), S * 12.4, S * .12, STEEL, INK, 1))     # plywood wall, steel floor
    a(_r(X(-.375), Z(.8), S * 10.7, S * .8, WOOD, INK, 1)); a(_t(X(1.2), Z(.4) + 4, 'subfloor 3/4 in', 10.5, 'start', '#3E2A10'))
    a(_r(X(0), Z(1.05), S * 10, S * .25, AMB, '#8A6A00', 1, 'opacity=".9"'))                                                              # the bed of flexible adhesive
    a(_r(X(0), Z(1.3), S * 10, S * .25, PAN, BLU, 1.2))                                                                                   # the pan floor
    a(_r(X(0), Z(PANTOP), S * .28, S * (PANTOP - 1.3), PAN, BLU, 1.2))                                                                    # its lip against the wall
    a(_r(X(.06), Z(7), S * LT, S * (7 - ZB), TEAL, TEALD, .8))                                                                             # the liner
    a(_r(X(0), Z(7), S * .06, S * (7 - ZB), AMB, AMB, .5))                                                                                # its adhesive
    a(_p([(X(0), Z(PANTOP)), (X(.3), Z(PANTOP)), (X(.34), Z(ZB + .02)), (X(.15), Z(ZB + .02)), (X(0), Z(ZB))], SEAL, '#2E5B49', 1))     # the sealant in the gap
    a(_l(X(.3), Z(PANTOP), X(10.3), Z(PANTOP), '#5F5E5A', 1, '3 2')); a(_t(X(10.4), Z(PANTOP) + 4, f'pan top {PANTOP} up', 10.5, 'start', '#5F5E5A'))
    a(_arrow(X(.7), Z(6.2), X(.7), Z(PANTOP + .7), BLU, 2)); a(_arrow(X(.7), Z(PANTOP + .7), X(2.2), Z(1.9), BLU, 2))
    a(_t(X(2.6), Z(5.5), 'water runs down the liner,', 11.5, 'start', BLU, 600)); a(_t(X(2.6), Z(5.5) + 14, 'over the sealant, into the pan', 11.5, 'start', BLU, 600))
    a(_call(X(.1), Z(6.55), X(5.2), Z(6.65), f'liner: FRP panel, {LT:.2f} in', 'start', TEALD))
    a(_call(X(.03), Z(4.6), X(5.2), Z(4.35), 'adhesive under the liner', 'start', '#8A6A00'))
    a(_call(X(.2), Z(ZB - .12), X(5.2), Z(3.3), f'{fr(GAP)} in gap filled with flexible sealant', 'start', '#2E5B49'))
    a(_call(X(.14), Z(2.5), X(5.2), Z(2.6), 'pan lip, sealed to the plywood', 'start', BLU))
    a(_call(X(8.6), Z(1.42), X(8.0), Z(2.2), 'pan floor', 'start', BLU))
    a(_call(X(9.2), Z(1.17), X(10.4), Z(1.75), 'adhesive bed', 'start', '#8A6A00'))
    a(_call(X(-.2), Z(1.2), X(-1.7), Z(2.4), 'edge sealed', 'end', INK))
    return _svg(760, 400, ''.join(o), 'Section at the wall: pan lip, sealed gap and liner')

# ---- C  the drain through the floor ----------------------------------------------------------------------------------------------
def fig_drain():
    S = 60.0; OX = 270; Z0 = 120
    X = lambda x: OX + S * x; Z = lambda z: Z0 - S * z
    o = []; a = o.append
    a(_t(20, 24, 'C  The drain: a section through the hole in the floor', 14, 'start', INK, 700))
    a(_r(X(-4.2), Z(-.33), S * 8.4, S * .33, PAN, BLU, 1.2)); a(_r(X(-1.0), Z(-.33), S * 2.0, S * .33, '#fff', '#fff', .1))                  # pan floor with the hole
    a(_r(X(-4.2), Z(-.6), S * 3.1, S * .27, AMB, '#8A6A00', 1)); a(_r(X(1.1), Z(-.6), S * 3.1, S * .27, AMB, '#8A6A00', 1))                  # the bed, cut back from the hole
    a(_r(X(-4.2), Z(-1.4), S * 2.95, S * .8, WOOD, INK, 1)); a(_r(X(1.25), Z(-1.4), S * 2.95, S * .8, WOOD, INK, 1))                        # subfloor with the hole
    a(_r(X(-4.2), Z(-1.55), S * 2.95, S * .15, '#6C7077', INK, 1)); a(_r(X(1.25), Z(-1.55), S * 2.95, S * .15, '#6C7077', INK, 1))           # the steel floor, hole 1/4 in bigger than the drain body
    a(_l(X(-1.25), Z(-1.55), X(-1.25), Z(-1.4), RED, 3)); a(_l(X(1.25), Z(-1.55), X(1.25), Z(-1.4), RED, 3))
    a(_r(X(-1.7), Z(.16), S * 3.4, S * .16, '#B9BCC2', INK, 1.1)); a(_r(X(-1.7), Z(.0), S * 3.4, S * .08, SEAL, '#2E5B49', 1))                  # the flange on its sealant bed
    a(_r(X(-1.05), Z(.3), S * 2.1, S * .14, 'none', INK, 1, 'stroke-dasharray="3 2"'))                                                         # the strainer
    a(_r(X(-1.0), Z(.16), S * .14, S * 2.05, '#B9BCC2', INK, 1)); a(_r(X(.86), Z(.16), S * .14, S * 2.05, '#B9BCC2', INK, 1))               # the body
    a(_r(X(-1.7), Z(-1.55), S * 3.4, S * .16, '#8E9299', INK, 1.1)); a(_r(X(-1.7), Z(-1.71), S * 3.4, S * .2, '#8E9299', INK, 1.1))          # gasket and lock nut
    a(_r(X(-.75), Z(-1.9), S * 1.5, S * .55, 'none', INK, 1.2)); a(_t(X(0), Z(-2.3), 'to the P-trap', 12, 'middle', INK, 600))
    a(_arrow(X(0), Z(-2.45), X(0), Z(-2.9), BLU, 2))
    RX = 560
    a(_call(X(1.7), Z(.1), RX, Z(.1) - 18, 'flange in neutral silicone', 'start', '#2E5B49', 11.5))
    a(_call(X(1.0), Z(.37), RX, Z(.1) + 6, 'strainer', 'start', INK, 11.5))
    a(_call(X(4.0), Z(-.17), RX, Z(-.17) + 14, 'pan floor', 'start', BLU, 11.5))
    a(_call(X(4.0), Z(-.47), RX, Z(-.47) + 26, 'adhesive bed', 'start', '#8A6A00', 11.5))
    a(_call(X(4.0), Z(-1.0), RX, Z(-1.0) + 30, 'subfloor 3/4 in', 'start', INK, 11.5))
    a(_call(X(4.0), Z(-1.48), RX, Z(-1.48) + 36, 'steel floor', 'start', INK, 11.5))
    a(_t(20, Z(-3.0) + 6, 'Red: the bare steel edge of the hole (rust converter, then epoxy primer). The hole is cut 1/4 in bigger than the drain body.', 11.5, 'start', RED, 600))
    a(_t(20, Z(-3.0) + 22, 'The gasket and the lock nut go on from below, then the tailpiece, the trap and a hose that falls all the way to the grey tank (vented).', 11.5, 'start', INK))
    return _svg(760, 345, ''.join(o), 'Section through the drain')

# ---- D  the liner on the wall ------------------------------------------------------------------------------------------------------
def fig_wall():
    S = 7.0; OX = 220; FL = 640
    X = lambda x: OX + S * (36 - x); Z = lambda z: FL - S * z       # the rear end on the right, the cab on the left, as in the plan's passenger view
    o = []; a = o.append
    a(_t(20, 24, 'D  The liner on the stall wall, seen from inside (the cab to the left, the rear to the right)', 14, 'start', INK, 700))
    a(_r(X(36), Z(74.5), S * .75, S * 74.5, PLY, INK, 1)); a(_t(X(36), Z(74.5) - 5, 'W3', 11, 'end', INK, 700))
    a(_r(X(W3X), Z(ZT), S * W3X, S * H, TEAL, TEALD, 1.4, 'fill-opacity=".16"'))
    a(_r(X(PW), Z(PANTOP), S * PW, S * PANTOP, PAN, BLU, 1.4)); a(_t(X(18), Z(1.5) + 4, 'pan, 3 in curb', 10.5, 'middle', BLU))
    a(_r(X(W3X), Z(PANTOP + GAP), S * W3X, S * GAP + 1, SEAL, SEAL, 1))
    nx0, nx1, nz0, nz1 = NOOK
    a(_r(X(nx1), Z(nz1), S * (nx1 - nx0), S * (nz1 - nz0), '#fff', FURR, 1.5, 'stroke-dasharray="5 3"'))
    hx, hz = HEAD; a(f'<circle cx="{X(hx):.1f}" cy="{Z(hz):.1f}" r="9" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    vx, vz = VALVE; a(f'<circle cx="{X(vx):.1f}" cy="{Z(vz):.1f}" r="10" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    a(_l(X(W3X), Z(ZT), X(W3X), Z(ZB), FURR, 4)); a(_l(X(0), Z(ZT), X(0), Z(ZB), INK, 3))
    a(_dim(X(W3X), Z(ZT) - 22, X(0), Z(ZT) - 22, f'{fr(W3X)} in wide (cut 1/8 in short at a free edge)', 0, INK, 11))
    a(_dim(X(0) + 26, Z(ZT), X(0) + 26, Z(ZB), f'{fr(H)} in', 0, INK, 11))
    RX = X(0) + 66
    a(_call(X(18), Z(ZT) + 1, RX, Z(ZT) + 8, 'top: under the trim strip at the ceiling', 'start', INK, 11.5))
    a(_call(X(hx) + 9, Z(hz), RX, Z(hz) + 4, f'head: {fr(hx)} in along, {hz} up', 'start', BLU, 11.5)); a(_t(RX + 8, Z(hz) + 18, 'hole saw; sealant behind its flange', 10.5, 'start', '#5F5E5A'))
    a(_call(X(nx0), Z(46), RX, Z(46), 'nook: cut out of the wall panel', 'start', FURR, 11.5)); a(_t(RX + 8, Z(46) + 14, 'and lined (its sides from the offcut)', 10.5, 'start', '#5F5E5A'))
    a(_call(X(0), Z(30), RX, Z(30), 'free rear edge: edge trim', 'start', INK, 11.5))
    a(_call(X(0) , Z(PANTOP + GAP / 2), RX, Z(PANTOP + GAP / 2) - 20, f'{fr(GAP)} in sealant gap above the pan', 'start', '#2E5B49', 11.5))
    LX = X(36) - 14
    a(_call(X(vx) - 10, Z(vz), LX, Z(vz) - 30, f'valve: {fr(vx)} in along, {vz} up', 'end', BLU, 11.5)); a(_t(LX - 8, Z(vz) - 16, 'hole saw; sealant behind its flange', 10.5, 'end', '#5F5E5A'))
    a(_call(X(W3X), Z(20), LX, Z(20), 'inside corner moulding', 'end', FURR, 11.5)); a(_t(LX - 8, Z(20) + 14, 'between the wall liner and W3\'s', 10.5, 'end', '#5F5E5A')); a(_t(LX - 8, Z(20) + 27, 'liner (drawing F)', 10.5, 'end', '#5F5E5A'))
    return _svg(760, 680, ''.join(o), 'The liner on the shower wall')

# ---- E  the cutting plan ------------------------------------------------------------------------------------------------------------
def fig_cut():
    S = 3.0; OY = 70
    o = []; a = o.append
    a(_t(20, 24, 'E  Cutting two 4 x 8 ft sheets (48 x 96 in): the pieces, to scale', 14, 'start', INK, 700))
    def sheet(ox, nm):
        a(_r(ox, OY, S * 48, S * 96, '#F4F4F0', INK, 1.4)); a(_t(ox + S * 24, OY - 8, nm, 12, 'middle', INK, 700))
    ox1, ox2 = 40, 250
    sheet(ox1, 'Sheet 1'); sheet(ox2, 'Sheet 2')
    # sheet 1: the wall panel with the nook cut out, the nook sides in the offcut, the spare strip
    a(_r(ox1, OY, S * W3X, S * H, '#BFE5DF', TEALD, 1.4))
    nx0, nx1, nz0, nz1 = NOOK
    a(_r(ox1 + S * nx0, OY + S * (ZT - nz1), S * (nx1 - nx0), S * (nz1 - nz0), '#9AD3CB', TEALD, 1.2, 'stroke-dasharray="4 3"'))
    a(_t(ox1 + S * W3X / 2, OY + S * 10, 'wall panel', 11.5, 'middle', TEALD, 700)); a(_t(ox1 + S * W3X / 2, OY + S * 10 + 13, f'{fr(W3X)} x {fr(H)}', 11, 'middle', TEALD, 700))
    a(_t(ox1 + S * (nx0 + nx1) / 2, OY + S * (ZT - (nz0 + nz1) / 2) - 3, 'cut-out =', 10, 'middle', TEALD)); a(_t(ox1 + S * (nx0 + nx1) / 2, OY + S * (ZT - (nz0 + nz1) / 2) + 9, 'nook back', 10, 'middle', TEALD))
    ys = OY + S * H + 4
    a(_r(ox1 + 2, ys, S * 17.25, S * 4.5, '#D5EEE9', TEALD, 1)); a(_r(ox1 + 2, ys + S * 4.5 + 3, S * 17.25, S * 4.5, '#D5EEE9', TEALD, 1))
    a(_r(ox1 + S * 17.25 + 6, ys, S * 4.5, S * 16, '#D5EEE9', TEALD, 1)); a(_r(ox1 + S * 17.25 + S * 4.5 + 10, ys, S * 4.5, S * 16, '#D5EEE9', TEALD, 1))
    a(_t(ox1, OY + S * 96 + 16, 'nook sides from the offcut: 2 of 17 1/4 x 4 1/2 and 2 of 4 1/2 x 16', 10.5, 'start', TEALD))
    a(_t(ox1 + S * (W3X + 48) / 2 + 2, OY + S * 48, 'spare', 10.5, 'middle', '#5F5E5A')); a(_t(ox1 + S * (W3X + 48) / 2 + 2, OY + S * 48 + 12, f'{fr(48 - W3X)} x 96', 10.5, 'middle', '#5F5E5A'))
    # sheet 2: W3's face and a spare
    a(_r(ox2, OY, S * PD, S * H, '#BFE5DF', TEALD, 1.4)); a(_t(ox2 + S * PD / 2, OY + S * 12, 'W3 face', 11.5, 'middle', TEALD, 700)); a(_t(ox2 + S * PD / 2, OY + S * 12 + 13, f'{PD} x {fr(H)}', 11.5, 'middle', TEALD, 700))
    a(_t(ox2 + S * (PD + 48) / 2, OY + S * 48, 'spare', 10.5, 'middle', '#5F5E5A')); a(_t(ox2 + S * (PD + 48) / 2, OY + S * 48 + 12, f'{PD} x 96', 10.5, 'middle', '#5F5E5A'))
    a(_t(470, 100, 'Cut each piece 1/8 in short at a', 12, 'start', INK)); a(_t(470, 116, 'free edge, and 1/4 in above the pan,', 12, 'start', INK)); a(_t(470, 132, 'so it can move and the sealant has room.', 12, 'start', INK))
    a(_t(470, 164, 'Score the face with a utility knife and', 12, 'start', INK)); a(_t(470, 180, 'snap it, or use a fine-tooth saw, with the', 12, 'start', INK)); a(_t(470, 196, 'face up (a 40-tooth blade, slowly).', 12, 'start', INK))
    a(_t(470, 228, 'The nook cut-out is saved: it is the', 12, 'start', INK)); a(_t(470, 244, 'back of the nook, so the wall panel and', 12, 'start', INK)); a(_t(470, 260, 'the nook back match.', 12, 'start', INK))
    a(_t(470, 292, 'Every hole (head, valve) is drilled', 12, 'start', INK)); a(_t(470, 308, 'with a hole saw, never a twist drill.', 12, 'start', INK))
    return _svg(760, 400, ''.join(o), 'Cutting plan for the two FRP sheets')

# ---- F  the inside corner ------------------------------------------------------------------------------------------------------------
def fig_corner():
    S = 78.0; OX = 60; OY = 80
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    o = []; a = o.append
    a(_t(20, 24, 'F  The inside corner at W3, from above (the liner drawn 3 times too thick)', 14, 'start', INK, 700))
    a(_r(X(0), Y(-.375), S * 6.9, S * .375, PLY, INK, 1.1)); a(_r(X(6.0), Y(-.375), S * .75, S * 4.4, PLY, INK, 1.1))             # the wall plywood and W3
    LW = .25                                                                                                                       # the liners, 3 times too thick
    a(_r(X(0), Y(0), S * 5.6, S * LW, TEAL, TEALD, 1)); a(_r(X(6.0 - LW), Y(LW + .35), S * LW, S * 3.8, TEAL, TEALD, 1))           # the wall liner, and W3's liner starting 1/8 in lower
    a(_p([(X(5.6), Y(0)), (X(6.0), Y(0)), (X(6.0), Y(LW + .35)), (X(6.0 - LW), Y(LW + .35)), (X(6.0 - LW), Y(LW)), (X(5.6), Y(LW))], '#9FD0A9', '#2E5B49', 1))   # the sealant that fills the corner
    mo = [(X(4.7), Y(LW)), (X(6.0 - LW) + 1, Y(LW)), (X(6.0 - LW) + 1, Y(1.6)), (X(6.0 - LW) - 8, Y(1.6)), (X(6.0 - LW) - 8, Y(LW) + 9), (X(4.7), Y(LW) + 9)]
    a(_p(mo, '#8FD3C8', TEALD, 1.5))                                                                                              # the corner moulding, clipped over both liners
    a(_t(X(0), Y(-.375) - 8, 'wall plywood 3/8', 11, 'start', '#5F5E5A')); a(_t(X(6.9), Y(2.2), 'W3 plywood 3/4', 11, 'start', '#5F5E5A'))
    RX = X(7.3)
    a(_call(X(2.0), Y(LW / 2), X(0.2), Y(1.5), 'liner on the wall', 'start', TEALD, 12))
    a(_call(X(6.0 - LW / 2), Y(3.0), RX, Y(3.05), 'liner on W3', 'start', TEALD, 12))
    a(_call(X(5.3), Y(LW) + 5, X(0.2), Y(2.4), 'corner moulding clipped over both liners', 'start', TEALD, 12))
    a(_call(X(5.8), Y(.2), X(0.2), Y(3.3), 'flexible sealant fills the corner behind it', 'start', '#2E5B49', 12))
    a(_call(X(5.9), Y(LW + .28), X(0.2), Y(3.95), '1/8 in gap between the liners, filled with sealant', 'start', INK, 12))
    return _svg(760, 410, ''.join(o), 'The inside corner at W3')

FIGS = [
    ('A', 'The pan from above', fig_top, 'The bought pan sits against the plywood wall with W3 at its cab end. The drain hole is at the middle of the rear-door end, 5 in from the rear end (you said) and 12 out (the middle of the depth: check it on the pan). The floor falls to it. The liner runs along the wall and across the face of W3.'),
    ('B', 'The pan edge and the sealed gap', fig_edge, 'A stiff panel cannot lap over the pan lip, so it stops 1/4 in above the pan edge and the gap is filled with flexible sealant: the water runs down the liner, over the sealant and into the pan. The plywood edge below it is sealed and hidden behind the lip.'),
    ('C', 'The drain through the floor', fig_drain, 'The flange is bedded in neutral silicone on the pan, the body goes through the subfloor and the steel, a gasket and a lock nut hold it from below, and the bare steel edge of the hole is primed against rust. A P-trap and a hose take it to the grey tank, which must be vented (its place is not set).'),
    ('D', 'The liner on the wall', fig_wall, 'One panel for the wall (35 1/4 wide, 69 15/16 tall) with the nook cut out; the panel on W3 is separate, with an inside corner moulding between them. The head and the valve are hole-sawed through it and sealed behind their flanges.'),
    ('E', 'Cutting the sheets', fig_cut, 'Two 4 x 8 ft sheets are enough: the wall panel and the nook sides from the first, W3 from the second, with spares.'),
    ('F', 'The inside corner', fig_corner, 'At W3 the two liners meet in a corner moulding clipped over both, with a bead of flexible sealant behind each flange; a stiff panel never takes a tight corner by itself.')]

PARTS = [
    ('Shower pan', '36 x 24 in, 3 in curb (bought)', '1', 'measure the drain hole (its distance from the rear end and the wall, its size) and the height of the lip against the wall, and change the plan\'s sizes to match'),
    ('FRP panel', '4 x 8 ft, 0.09 in, white, smooth or pebbled', '2', 'the wall panel and the nook sides from one, W3 from the other; about 16 lb of liner in all (a rough weight)'),
    ('FRP adhesive', 'the panel maker\'s FRP adhesive (for example Crane\'s Glasbond or Marlite\'s, or a similar water-based or urethane panel adhesive), 1 gal', '1', 'spread on the plywood with the trowel or roller the can names, never on the panel; follow the can for open time and temperature'),
    ('Liner tools and safety', 'notched trowel or roller (as the can says), 3 in hand roller, masking tape, 1/8 in and 1/4 in spacers, fine-tooth saw or utility knife, hole saws, dust mask, gloves and glasses', '1 set', 'FRP dust and cut edges irritate skin and eyes; wear the mask and glasses when you cut'),
    ('FRP inside corner moulding', '8 ft piece in the panel\'s color', '1', 'at W3 (69 15/16 in) and to join the nook pieces if you want; the nook corners can be sealant only'),
    ('FRP edge (end) trim', '8 ft piece', '1', 'the free rear edge of the liner, and the top edge if it is not under the trim strip'),
    ('Flexible sealant', 'neutral-cure silicone or MS polymer, mold-resistant, white or clear', '4 tubes', 'drain flange, the pan joint, the pan lip, corners, valve and head flanges, the nook; never a hard caulk'),
    ('Pan bedding', 'flexible polyurethane or MS-polymer construction adhesive, 28 oz tubes or 10 oz cartridges', 'about 3 cartridges', 'zig-zag beads every 3 in under the pan; not a rigid mortar (the van flexes and the mortar cracks)'),
    ('Shower drain', 'fits the pan\'s drain hole, with a gasket and a lock nut from below; 1 1/2 in tailpiece', '1', 'check whether the pan comes with one'),
    ('P-trap and hose', '1 1/2 in trap (or a waterless trap valve) and 1 1/2 in flexible hose', '1', 'to the grey tank, which needs a vent (the tank\'s place is not set)'),
    ('Hole saws', 'drain body + 1/4 in; head; valve', '3', 'a hole saw for each, never a twist drill through the liner'),
    ('Epoxy and rust primer', 'thin epoxy for the plywood edges and cut-outs; rust converter and epoxy primer for the steel edge of the drain hole', '1 each', 'two coats of epoxy on every cut edge of the plywood in the stall'),
]
STEPS = [
    '<b>Measure the pan before anything is cut.</b> Write down its length and depth (36 x 24), the height of its curb and of its lip against the wall, the size of the drain hole and how far it is from the rear end and from the wall (you said the middle of the rear-door end, 5 in from the rear end; the plan has it at 5 in along and 12 out, the middle of the depth, which is my guess). Put the real numbers into the plan\'s sizes (Shower drain hole, Liner), so the drawings and checks follow.',
    '<b>Look under the floor where the hole goes.</b> Cross-members, wires, brake or fuel lines and the grey tank\'s place all matter before you drill. The hole at the middle of the rear-door end is near the rear bumper area: check it clears the frame.',
    '<b>Check and prepare the floor.</b> The subfloor under the pan must be flat to 1/8 in over the 36 x 24 in (a 4 ft level or a straightedge). Fill any dip with a flexible leveling filler or shim it; the pan\'s floor is thin and a fiberglass or acrylic pan must be supported all over, or it cracks where you stand.',
    '<b>Drill the drain hole.</b> Dry-fit the pan, mark the center of its drain hole on the floor, take the pan out, drill a pilot hole through the subfloor and the steel, then cut with a hole saw 1/4 in bigger than the drain body. Deburr the steel edge, treat it with rust converter and epoxy primer, and seal the cut edge of the subfloor with epoxy. Vacuum all the chips out of the van.',
    '<b>Bed the pan.</b> Run zig-zag beads of the flexible adhesive over the subfloor about every 3 in (keep it 2 in back from the hole), bed the drain flange in neutral silicone on the pan, set the pan down against the plywood wall and a hair short of W3, and press it. Check it is level side to side and falls to the drain. Weigh it down (jugs of water, 100 lb) for the adhesive\'s open time and wipe the squeeze-out.',
    '<b>Connect the drain from below:</b> gasket and lock nut on the body, then the tailpiece, the P-trap and the hose to the grey tank, with a vent on the tank. Keep the hose falling all the way to the tank.',
    '<b>Seal the pan to the wall.</b> A bead of flexible sealant where the pan lip meets the plywood, and the plywood edge below the liner sealed with epoxy (drawing B).',
    '<b>Fill test.</b> Plug the drain, fill the pan to just under the curb, mark the water line and leave it for a day. Check the line has not dropped and look under the floor for any drip. Then open the drain, check it flows freely and leaks nowhere at the nut or the trap.',
    '<b>Prepare the plywood before the liner goes on.</b> (1) Two coats of thin epoxy on every cut edge and on the bare plywood of the nook and of the valve and head cut-outs: water gets in from the edges. (2) Make the face flat. The screws that hold the plywood have finish washers, and a washer would show through a 0.09 in panel as a bump and stop it sticking: in the stall, countersink each screw (or refit it with a flat head) and fill the dimple with epoxy filler, then sand it flush; sand off raised grain, fill any gouge, and check with a straightedge that nothing stands more than about 1/32 in proud, because FRP shows every bump. (3) Vacuum the dust and wipe the face with a damp cloth: it must be clean, dry and free of oil where the adhesive goes (scuff-sand any epoxy that reached the face).',
    '<b>Cut the liner</b> (drawing E): the wall panel (35 1/4 x 69 15/16, with the nook cut out), W3\'s face (24 x 69 15/16) and the four nook sides, each 1/8 in short at a free edge and 1/4 in above the pan. Hole-saw the head and the valve holes.',
    '<b>Glue the wall panel</b> with the panel maker\'s adhesive (read its can for the trowel, the open time and the temperature). (1) Let the panels sit in the van for at least 24 hours first, so they match its temperature and humidity, and glue at room temperature (about 60 F or more, or what the can says). (2) Dry-fit it: rest the bottom edge on 1/4 in spacers at the pan and keep 1/8 in off W3, the rear edge and the ceiling. (3) Spread the adhesive on the plywood, never on the panel, with the notched trowel or roller the can names, only as far as you can cover within the open time, and keep it about 1 in back from the edges so none squeezes out at the gaps. (4) Set the panel on its spacers, tip the top in, press it flat from the middle outward and roll the whole face with a hand roller, edges last. (5) Hold the top with a few strips of masking tape for the first hour, and leave it alone for the cure time on the can. No screws go through the face: they leak and stop the panel from moving, and the mouldings and the sealant hold the edges. (6) Then the nook (back, then sides), then W3\'s face, then the inside corner moulding with sealant behind each flange (drawing F).',
    '<b>Seal and trim.</b> Fill the 1/4 in gap at the pan with flexible sealant and tool it; seal the rear edge under its edge trim, the top under the trim strip, every nook corner, and behind the head and valve flanges; wipe the excess off straight away. Let it cure a day.',
    '<b>Finish and test.</b> Fit the head and valve, hang the curtain and the nook cord, then run the shower for ten minutes with the curtain closed and check under the floor and along the bottom of W3 for any wet.',
]

CSS = '''<style>.pangrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,520px),1fr));gap:16px;margin:12px 0}
.pangrid figure{margin:0;border:1px solid #d9d5ca;border-radius:8px;padding:10px;background:#fff;min-width:0}
.pangrid figcaption{font-size:14px;line-height:1.45;margin-top:8px;color:#26241f}.pangrid figcaption b{font-size:15px}</style>'''

def pan_html():
    figs = CSS + '<div class="pangrid">' + ''.join(f'<figure>{fn()}<figcaption><b>{n}. {name}.</b> {cap}</figcaption></figure>' for n, name, fn, cap in FIGS) + '</div>'
    tbl = '<h3>Parts and materials</h3><div class="wide"><table class="rt"><tr><th>Part</th><th>What</th><th>Qty</th><th>Notes</th></tr>' + ''.join(f'<tr><td><b>{a}</b></td><td>{b}</td><td>{c}</td><td>{d}</td></tr>' for a, b, c, d in PARTS) + '</table></div>'
    return figs + tbl

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'pan.html')
    open(out, 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Shower pan</title><body style="font:16px/1.5 system-ui;max-width:1100px;margin:0 auto;padding:16px">' + pan_html() + '<ol>' + ''.join(f'<li>{s}</li>' for s in STEPS) + '</ol></body>')
    print('wrote', out)
