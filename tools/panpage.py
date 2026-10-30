"""The shower pan page of the build guide: how to set the bought 36 x 24 pan, drain it and line the back wall of the stall with PVC paneling over the 3/8 in plywood. The other three sides of the stall are curtains (no end wall W3).
Nine drawings made from the plan's numbers (the pan, the planks, the nook, the head and the valve, the drain hole), a parts table and the steps in order.
Used by buildguide.py (the Shower pan page); run on its own it writes ../pan.html for a quick look.
The shared numbers (the nook, the head and the valve, the plank thickness and width, the curtain rail) come from shelfdata.py, the same as ia_core.js; the drain hole is at the middle of the rear-door end, 5 in from the rear end (the user's measurement; the 12 in out from the wall is the middle of the depth, assumed),
the pan's lip height against the wall is a guess, and PVC paneling is the user's choice ('The back wall will be lined with pvc paneling, including the nook'): change them here, in shelfdata.py, in ia_core.js (pdrX, pdrY, linerT, pvcW, linerTop, linerGap, curIn) and in plan.py together."""
import os
if 'SN_X0' not in globals():       # exec'd by buildguide.py after shelfdata.py, in the same namespace; on its own, read the shared numbers here
    exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'shelfdata.py')).read())

INK = '#2C2C2A'; PLY = '#E8CF9C'; PLYD = '#B8975A'; HARD = '#C9A263'; STEEL = '#9AA0A8'; FURR = '#7A4A1E'; SEAL = '#4F8C74'; TEAL = '#2A9D8F'; TEALD = '#1F7A70'
RED = '#A32D2D'; BLU = '#185FA5'; PAN = '#CFE3F3'; AMB = '#D4A017'; GRY = '#D8D8D4'; WOOD = '#C8A878'; PUR = '#7B3FA0'

# the numbers, the same as the plan
PW, PD = PAN_W, PAN_D           # the pan: length along the wall, depth out from it
PANTOP = 3.8                    # top of the pan's curb and lip: 3 in over the 0.8 in floor
GAP = .25                       # the paneling stops this far above the pan edge, the gap filled with flexible sealant
ZB, ZT = PANTOP + GAP, 74       # the paneling's bottom and top, up from the floor
H = ZT - ZB                     # 69 15/16
LT = LINER_T                    # the planks' thickness (5/16 in: a placeholder, measure yours)
NOOK = (SN_X0, SN_X1, SN_Z0, SN_Z1)    # the shower nook: x0, x1, z0, z1 (4 1/2 in deep, in the wall), centered on the pan
HEAD = (HEAD_X, HEAD_Z); VALVE = (VALVE_X, VALVE_Z)
HEADHOLE, VALVEHOLE = 1.125, 2.25    # the holes in the planks: the part that goes through + 1/4 in (a 1/2 in shower arm is 7/8 across; a single-handle valve cartridge is about 2 in: PLACEHOLDERS, measure the real parts)
DRAIN = (5, 12)                 # 5 in from the rear end (the user), 12 out = the middle of the depth (assumed)
TOILET = (TOILET_X[0], TOILET_X[1], 4.75, 19.25)
EDGES = [0] + list(PVC_JOINTS) + [PW]          # the plank edges along the wall from the back mark: 0, 9 3/8, 19 1/8, 28 7/8, 36
CUTS = list(zip(EDGES, EDGES[1:]))             # the four planks, the first and the last narrower
RE = .125                                      # a free edge stops 1/8 in short of its trim

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
    a(_t(20, 24, 'A  From above: the pan, the paneling on the wall and the curtains (passenger wall at the top)', 14, 'start', INK, 700))
    a(_r(X(SN_X0), Y(-4.5), S * SN_LEN, S * 4.5, '#F6EBD4', FURR, 1.2, 'stroke-dasharray="5 3"')); a(_t(X((SN_X0 + SN_X1) / 2), Y(-1.6), 'shower nook, 4 1/2 deep (in the wall)', 10.5, 'middle', FURR))
    a(_r(X(-2), Y(-.375), S * (PW + 2.5), S * .375 + 1, PLY, INK, 1)); a(_t(X(-2), Y(-.375) - 6, 'passenger wall: 3/8 in plywood', 10.5, 'start', '#5F5E5A'))
    a(_r(X(0), Y(0), S * PW, S * PD, PAN, BLU, 2.2))
    a(_l(X(0), Y(0) + 2, X(PW), Y(0) + 2, TEAL, 4)); a(_t(X(PW) - 4, Y(0) + 17, 'PVC paneling on the wall (4 planks)', 10.5, 'end', TEALD, 600))
    yF = PD - CUR_IN
    a(f'<polyline points="{X(CUR_IN):.1f},{Y(0):.1f} {X(CUR_IN):.1f},{Y(yF):.1f} {X(PW - CUR_IN):.1f},{Y(yF):.1f} {X(PW - CUR_IN):.1f},{Y(0):.1f}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-dasharray="8 4"/>')
    a(_l(X(CUR_IN), Y(.8), X(CUR_IN), Y(yF + .3), PUR, 4)); a(_l(X(CUR_IN), Y(yF + .3), X(PW / 2 + 3), Y(yF + .3), PUR, 4))
    a(_l(X(PW - CUR_IN), Y(.8), X(PW - CUR_IN), Y(yF - .9), '#B07ACB', 4)); a(_l(X(PW - CUR_IN), Y(yF - .9), X(PW / 2 - 3), Y(yF - .9), '#B07ACB', 4))
    tx0, tx1, ty0, ty1 = TOILET
    a(_r(X(tx0), Y(ty0), S * (tx1 - tx0), S * (ty1 - ty0), 'none', '#993556', 1.6, 'stroke-dasharray="6 3"')); a(_t(X((tx0 + tx1) / 2), Y((ty0 + ty1) / 2) + 4, 'toilet (stays set up)', 10.5, 'middle', '#993556'))
    a(f'<circle cx="{X(HEAD[0]):.1f}" cy="{Y(6):.1f}" r="7" fill="#fff" stroke="{BLU}" stroke-width="1.6"/>' + _t(X(HEAD[0]) + 11, Y(6) + 4, 'shower head', 10.5, 'start', BLU))
    dx, dy = DRAIN
    a(f'<circle cx="{X(dx):.1f}" cy="{Y(dy):.1f}" r="{S * 1.1:.1f}" fill="{INK}"/>')
    a(_t(X(dx) + 22, Y(dy) - 32, 'drain hole', 12, 'start', INK, 700)); a(_t(X(dx) + 22, Y(dy) - 18, f'{fr(dx)} in along, {fr(dy)} out', 11, 'start', INK)); a(_t(X(dx) + 22, Y(dy) - 4, '(12 out: check it)', 11, 'start', RED, 600))
    a(_arrow(X(14), Y(17), X(6.6), Y(13.3), BLU, 1.6)); a(_arrow(X(14), Y(13.8), X(6.5), Y(12.7), BLU, 1.6)); a(_arrow(X(2.2), Y(21), X(3.4), Y(14.4), BLU, 1.6))
    a(_t(X(9), Y(21) + 2, 'floor falls to the drain', 10.5, 'start', BLU))
    a(_t(X(0) - 8, Y(18), 'rear-door end', 11, 'end', '#5F5E5A', 600)); a(_t(X(0) - 8, Y(18) + 13, '(a curtain)', 10.5, 'end', '#5F5E5A'))
    a(_t(X(PW) + 8, Y(18), 'cab end', 11, 'start', '#5F5E5A', 600)); a(_t(X(PW) + 8, Y(18) + 13, '(a curtain,', 10.5, 'start', '#5F5E5A')); a(_t(X(PW) + 8, Y(18) + 26, 'no wall W3)', 10.5, 'start', '#5F5E5A'))
    yb = Y(PD) + 30
    a(_dim(X(0), yb, X(PW), yb, f'{PW} in')); a(_dim(X(0), yb + 22, X(dx), yb + 22, f'{fr(dx)}'))
    a(_dim(X(PW) + 100, Y(0), X(PW) + 100, Y(PD), f'{PD} in')); a(_dim(X(0) - 24, Y(0), X(0) - 24, Y(dy), f'{fr(dy)}'))
    a(_t(X(PW / 2), Y(PD) + 12, 'front (aisle side): two curtains on a ceiling rail, overlapping 6 in', 10.5, 'middle', PUR, 600))
    return _svg(760, 500, ''.join(o), 'The shower pan from above')

# ---- B  section at the wall: the pan edge, the sealed gap and the planks ---------------------------------------------------------
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
    a(_t(X(2.6), Z(5.5), 'water runs down the planks,', 11.5, 'start', BLU, 600)); a(_t(X(2.6), Z(5.5) + 14, 'over the sealant, into the pan', 11.5, 'start', BLU, 600))
    a(_call(X(.1), Z(6.55), X(5.2), Z(6.65), f'PVC plank, {fr(LT)} in (measure yours)', 'start', TEALD))
    a(_call(X(.03), Z(4.6), X(5.2), Z(4.35), 'adhesive under the plank', 'start', '#8A6A00'))
    a(_call(X(.2), Z(ZB - .12), X(5.2), Z(3.3), f'{fr(GAP)} in gap filled with flexible sealant', 'start', '#2E5B49'))
    a(_call(X(.14), Z(2.5), X(5.2), Z(2.6), 'pan lip, sealed to the plywood', 'start', BLU))
    a(_call(X(8.6), Z(1.42), X(8.0), Z(2.2), 'pan floor', 'start', BLU))
    a(_call(X(9.2), Z(1.17), X(10.4), Z(1.75), 'adhesive bed', 'start', '#8A6A00'))
    a(_call(X(-.2), Z(1.2), X(-1.7), Z(2.4), 'edge sealed', 'end', INK))
    return _svg(760, 400, ''.join(o), 'Section at the wall: pan lip, sealed gap and PVC plank')


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

# ---- D  the planks on the wall ------------------------------------------------------------------------------------------------------
def fig_wall():
    S = 7.0; OX = 270; FL = 640
    X = lambda x: OX + S * (PW - x); Z = lambda z: FL - S * z       # the rear end on the right, the cab on the left, as in the plan's passenger view
    o = []; a = o.append
    a(_t(20, 24, 'D  The PVC planks on the back wall, seen from inside (the cab to the left, the rear to the right)', 14, 'start', INK, 700))
    nx0, nx1, nz0, nz1 = NOOK
    for i, (e0, e1) in enumerate(CUTS):
        x0 = e0 + (RE if i == 0 else 0); x1 = e1 - (RE if i == len(CUTS) - 1 else 0)
        a(_r(X(x1), Z(ZT), S * (x1 - x0), S * H, TEAL, TEALD, 1.2, 'fill-opacity=".16"'))
        a(_t(X((x0 + x1) / 2), Z(ZT) + 18, str(i + 1), 12, 'middle', TEALD, 700))
    a(_r(X(PW), Z(PANTOP), S * PW, S * PANTOP, PAN, BLU, 1.4)); a(_t(X(18), Z(1.5) + 4, 'pan, 3 in curb', 10.5, 'middle', BLU))
    a(_r(X(PW), Z(PANTOP + GAP), S * PW, S * GAP + 1, SEAL, SEAL, 1))
    a(_r(X(nx1), Z(nz1), S * (nx1 - nx0), S * (nz1 - nz0), '#fff', FURR, 1.5, 'stroke-dasharray="5 3"'))
    hx, hz = HEAD; a(f'<circle cx="{X(hx):.1f}" cy="{Z(hz):.1f}" r="9" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    vx, vz = VALVE; a(f'<circle cx="{X(vx):.1f}" cy="{Z(vz):.1f}" r="10" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    a(_l(X(PW), Z(ZT), X(PW), Z(ZB), FURR, 4)); a(_l(X(0), Z(ZT), X(0), Z(ZB), FURR, 4))
    a(_dim(X(PW), Z(ZT) - 22, X(0), Z(ZT) - 22, f'{PW} in along the wall (4 planks, each cut 1/8 in short at a free edge)', 0, INK, 11))
    a(_dim(X(0) + 26, Z(ZT), X(0) + 26, Z(ZB), f'{fr(H)} in', 0, INK, 11))
    RX = X(0) + 66
    a(_call(X(18), Z(ZT) + 1, RX, Z(ZT) + 8, 'top: under the ceiling trim strip', 'start', INK, 11.5))
    a(_call(X(hx) + 9, Z(hz), RX, Z(hz) + 4, f'head: {fr(hx)} in along, {hz} up', 'start', BLU, 11.5)); a(_t(RX + 8, Z(hz) + 18, 'hole saw, plank 1, sealed behind', 10.5, 'start', '#5F5E5A'))
    a(_call(X(nx0), Z(46), RX, Z(46), 'nook: cut out of planks 2 and 3', 'start', FURR, 11.5)); a(_t(RX + 8, Z(46) + 14, 'and lined (floor, ceiling and sides', 10.5, 'start', '#5F5E5A')); a(_t(RX + 8, Z(46) + 27, 'from the offcuts)', 10.5, 'start', '#5F5E5A'))
    a(_call(X(0), Z(30), RX, Z(30), 'rear end: end trim', 'start', INK, 11.5))
    a(_call(X(0), Z(PANTOP + GAP / 2), RX, Z(PANTOP + GAP / 2) - 20, f'{fr(GAP)} in sealant gap above the pan', 'start', '#2E5B49', 11.5))
    LX = X(PW) - 14
    a(_call(X(vx) - 10, Z(vz), LX, Z(vz) - 30, f'valve: {fr(vx)} in along, {vz} up', 'end', BLU, 11.5)); a(_t(LX - 8, Z(vz) - 16, 'hole saw, plank 2, sealed behind', 10.5, 'end', '#5F5E5A'))
    a(_call(X(PW), Z(20), LX, Z(20), 'cab end: end trim, then the curtain', 'end', INK, 11.5)); a(_t(LX - 8, Z(20) + 14, '(no wall W3, no corner)', 10.5, 'end', '#5F5E5A'))
    for j, jx in enumerate(PVC_JOINTS):
        a(_call(X(jx), Z(ZT - 8 - 3 * j), LX, Z(ZT - 8 - 3 * j), f'joint at {fr(jx)}' + (' (the nook\'s rear edge)' if j == 0 else ''), 'end', TEALD, 11))
    return _svg(820, 680, ''.join(o), 'The PVC planks on the shower wall')

# ---- E  the cutting plan ------------------------------------------------------------------------------------------------------------
def fig_cut():
    S = 3.0; OY = 78
    o = []; a = o.append
    a(_t(20, 24, 'E  Cutting the planks: four 10 in x 8 ft planks and a spare, to scale', 14, 'start', INK, 700))
    nx0, nx1, nz0, nz1 = NOOK
    n3 = nx1 - PVC_JOINTS[1]                    # how much of plank 3 the nook takes (7 1/2)
    for i in range(5):
        ox = 36 + i * 76
        a(_r(ox, OY, S * 10, S * 96, '#F4F4F0', INK, 1.2)); a(_t(ox + S * 5, OY - 8, 'spare' if i == 4 else f'plank {i + 1}', 11.5, 'middle', INK, 700))
        if i == 4: continue
        e0, e1 = CUTS[i]; w = min(10, e1 - e0 - (RE if i in (0, 3) else 0))
        a(_r(ox, OY, S * w, S * H, '#BFE5DF', TEALD, 1.3)); a(_t(ox + S * w / 2, OY + S * H + 11, f'{fr(w)} wide', 9.5, 'middle', TEALD, 600)); a(_t(ox + S * w / 2, OY + S * H + 22, f'{fr(H)} long', 9.5, 'middle', TEALD, 600))
        if i in (1, 2):                          # the nook crosses planks 2 and 3: the part inside it is the nook's back
            ww = 10 if i == 1 else n3
            a(_r(ox, OY + S * (ZT - nz1), S * ww, S * (nz1 - nz0), '#9AD3CB', TEALD, 1.1, 'stroke-dasharray="4 3"'))
            a(_t(ox + S * ww / 2, OY + S * (ZT - (nz0 + nz1) / 2) - 2, 'nook', 9.5, 'middle', TEALD)); a(_t(ox + S * ww / 2, OY + S * (ZT - (nz0 + nz1) / 2) + 9, 'back', 9.5, 'middle', TEALD))
        ys = OY + S * H + 30                      # the offcut under it (26 in)
        if i == 1:
            for k in range(2): a(_r(ox + 2 + k * S * 4.7, ys, S * 4.5, S * 17.25, '#D5EEE9', TEALD, 1))
            a(_t(ox + 1, ys + S * 17.25 + 12, 'floor, ceiling', 9.5, 'start', TEALD))
        if i == 2:
            for k in range(2): a(_r(ox + 2 + k * S * 4.7, ys, S * 4.5, S * 16, '#D5EEE9', TEALD, 1))
            a(_t(ox + 1, ys + S * 16 + 12, 'two sides', 9.5, 'start', TEALD))
    a(_t(36, OY + S * 96 + 30, 'the offcuts of planks 2 and 3 (26 in long) make the nook\'s floor and ceiling (2 of 17 1/4 x 4 1/2) and its two sides (2 of 16 x 4 1/2)', 10.5, 'start', TEALD))
    X0 = 430
    a(_t(X0, 100, 'Cut each plank to 69 15/16 in (it stops 1/4 in', 12, 'start', INK)); a(_t(X0, 116, 'above the pan and 1/8 in under the trim', 12, 'start', INK)); a(_t(X0, 132, 'strip at the ceiling). Plank 1 and plank 4', 12, 'start', INK)); a(_t(X0, 148, 'are ripped narrower (9 1/4 and 7 in) on the', 12, 'start', INK)); a(_t(X0, 164, 'edge that is not the tongue.', 12, 'start', INK))
    a(_t(X0, 196, 'Cut with a fine-tooth saw (a 24-teeth-per-inch', 12, 'start', INK)); a(_t(X0, 212, 'back saw, or a jigsaw with a fine blade, a', 12, 'start', INK)); a(_t(X0, 228, 'plank at a time, supported all along, face', 12, 'start', INK)); a(_t(X0, 244, 'up for a hand saw), or score a thin plank', 12, 'start', INK)); a(_t(X0, 260, 'with a utility knife and snap it.', 12, 'start', INK))
    a(_t(X0, 292, 'The cut-outs of the nook are saved: they are', 12, 'start', INK)); a(_t(X0, 308, 'the back of the nook, so the wall and the', 12, 'start', INK)); a(_t(X0, 324, 'nook back match. Every hole (head, valve)', 12, 'start', INK)); a(_t(X0, 340, 'is made with a hole saw, never a twist drill.', 12, 'start', INK))
    return _svg(840, 460, ''.join(o), 'Cutting plan for the PVC planks')

# ---- F  the joint and the end trim ---------------------------------------------------------------------------------------------------
def fig_corner():
    S = 80.0; OX = 40; OY = 116
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    o = []; a = o.append
    a(_t(20, 24, 'F  The joint between two planks, and the end trim (from above, to scale: a plank is 5/16 in thick)', 14, 'start', INK, 700))
    LW = LT                                                                                                                  # the plank
    # --- left: the tongue and groove joint, plank 2 (left) into plank 3 (right), seen from above, the plywood wall at the top
    a(_t(X(0), Y(-.375) - 22, 'Tongue and groove joint', 12.5, 'start', INK, 700))
    a(_r(X(0), Y(-.375), S * 6.2, S * .375, PLY, INK, 1.1)); a(_t(X(0), Y(-.375) - 6, 'wall plywood 3/8', 11, 'start', '#5F5E5A'))
    a(_r(X(0), Y(0), S * 6.2, S * .06, AMB, '#8A6A00', .6))                                                                    # the dab of adhesive behind the planks
    a(_p([(X(0), Y(.06)), (X(2.6), Y(.06)), (X(2.6), Y(.06 + LW * .3)), (X(3.05), Y(.06 + LW * .3)), (X(3.05), Y(.06 + LW * .62)), (X(2.6), Y(.06 + LW * .62)), (X(2.6), Y(.06 + LW)), (X(0), Y(.06 + LW))], '#BFE5DF', TEALD, 1.3))   # plank 2, with its tongue
    a(_p([(X(3.0), Y(.06)), (X(6.2), Y(.06)), (X(6.2), Y(.06 + LW)), (X(3.0), Y(.06 + LW)), (X(3.0), Y(.06 + LW * .62) + 0), (X(2.55), Y(.06 + LW * .62)), (X(2.55), Y(.06 + LW * .3)), (X(3.0), Y(.06 + LW * .3))], '#9AD3CB', TEALD, 1.3))   # plank 3, with its groove
    a(_call(X(2.9), Y(.06 + LW * .45), X(0.1), Y(1.55), 'tongue (plank 2) in the groove (plank 3)', 'start', TEALD, 11.5))
    a(_call(X(1.2), Y(.03), X(0.1), Y(2.2), 'dabs of adhesive behind the plank,', 'start', '#8A6A00', 11.5)); a(_t(X(0.1) + 8, Y(2.2) + 14, 'none in the joint', 11, 'start', '#8A6A00'))
    a(_call(X(5.2), Y(.06 + LW), X(3.9), Y(1.4), 'the face: smooth, with a', 'start', INK, 11.5)); a(_t(X(3.9) + 8, Y(1.4) + 14, 'V-groove at the joint', 11, 'start', INK))
    # --- right: a free edge (the rear end or the cab end) with its end trim
    a(_t(X(0), Y(3.55), 'A free edge: the end trim (rear end and cab end)', 12.5, 'start', INK, 700))
    y0 = 4.6
    a(_r(X(0), Y(y0 - .375), S * 6.2, S * .375, PLY, INK, 1.1)); a(_r(X(0), Y(y0), S * 4.6, S * .06, AMB, '#8A6A00', .6))
    a(_r(X(0), Y(y0 + .06), S * 4.45, S * LW, '#BFE5DF', TEALD, 1.3)); a(_t(X(2.2), Y(y0 + .06 + LW) + 14, 'plank', 11, 'middle', TEALD))
    a(_p([(X(4.2), Y(y0 + .06 + LW + .25)), (X(4.75), Y(y0 + .06 + LW + .25)), (X(4.75), Y(y0 - .08)), (X(4.2), Y(y0 - .08)), (X(4.2), Y(y0 + .06 - .03)), (X(4.6), Y(y0 + .06 - .03)), (X(4.6), Y(y0 + .06 + LW + .15)), (X(4.2), Y(y0 + .06 + LW + .15))], '#E7D9B8', INK, 1.3))   # the J-shaped trim
    a(_p([(X(4.45), Y(y0 + .06)), (X(4.6), Y(y0 + .06)), (X(4.6), Y(y0 + .06 + LW)), (X(4.45), Y(y0 + .06 + LW))], SEAL, '#2E5B49', .8))            # the sealant in the 1/8 in gap
    a(_call(X(4.45), Y(y0 + .06 + LW / 2), X(5.0), Y(y0 + 1.5), '1/8 in gap, filled with', 'start', '#2E5B49', 11.5)); a(_t(X(5.0) + 8, Y(y0 + 1.5) + 14, 'flexible sealant', 11, 'start', '#2E5B49'))
    a(_call(X(4.7), Y(y0 - .02), X(5.0), Y(y0 + 2.4), 'J-shaped end trim, glued to the', 'start', INK, 11.5)); a(_t(X(5.0) + 8, Y(y0 + 2.4) + 14, 'plywood, over the plank\'s edge', 'start' and 11, 'start', INK))
    return _svg(760, 735, ''.join(o), 'The plank joint and the end trim')

# ---- G  cutting the nook out of the planks -------------------------------------------------------------------------------------------
def fig_nook():
    S = 6.2; OX = 70; OY = 96
    j2, j3 = PVC_JOINTS[0], PVC_JOINTS[1]                    # the joints either side of plank 2
    pw2, pw3 = j3 - j2, PVC_JOINTS[2] - j3                   # planks 2 and 3 as they cover (9 3/4 each)
    nw3 = NOOK[1] - j3                                       # how far the nook goes into plank 3 (7 1/2)
    PH = H; ny0 = ZT - NOOK[3]; nh = NOOK[3] - NOOK[2]       # the nook from the planks' top edge, and its height
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    o = []; a = o.append
    a(_t(20, 24, 'G  Cutting the nook out of planks 2 and 3 (flat on the bench, face up, laid side by side, rear on the left)', 14, 'start', INK, 700))
    a(_r(X(0), Y(0), S * pw2, S * PH, '#BFE5DF', TEALD, 1.6)); a(_r(X(pw2), Y(0), S * pw3, S * PH, '#9AD3CB', TEALD, 1.6))
    a(_t(X(pw2 / 2), Y(PH) + 18, 'plank 2', 11.5, 'middle', TEALD, 700)); a(_t(X(pw2 + pw3 / 2), Y(PH) + 18, 'plank 3', 11.5, 'middle', TEALD, 700))
    a(_t(X(0), Y(PH) + 36, f'each {fr(PH)} long, 1/4 in off the pan end', 10.5, 'start', '#5F5E5A')); a(_t(X(0) - 8, Y(0) + 4, 'top end', 11, 'end', '#5F5E5A', 600))
    a(_r(X(0), Y(ny0), S * (pw2 + nw3), S * nh, '#fff', INK, 1.6, 'stroke-dasharray="5 3"'))
    a(_t(X((pw2 + nw3) / 2), Y(ny0 + nh / 2) - 6, 'cut-out:', 11.5, 'middle', INK, 700)); a(_t(X((pw2 + nw3) / 2), Y(ny0 + nh / 2) + 9, 'save it (the', 11, 'middle', INK)); a(_t(X((pw2 + nw3) / 2), Y(ny0 + nh / 2) + 22, 'nook back)', 11, 'middle', INK))
    # the cuts, in order: 1 and 2 across both planks, 3 along plank 3
    a(_l(X(0) - 8, Y(ny0), X(pw2 + pw3) + 8, Y(ny0), RED, 2)); a(_l(X(0) - 8, Y(ny0 + nh), X(pw2 + pw3) + 8, Y(ny0 + nh), RED, 2)); a(_l(X(j3 + nw3), Y(ny0) - 8, X(j3 + nw3), Y(ny0 + nh) + 8, RED, 2))
    for (cx, cy, k) in ((X(pw2 + pw3) + 20, Y(ny0), '1'), (X(pw2 + pw3) + 20, Y(ny0 + nh), '2'), (X(j3 + nw3), Y(ny0 + nh) + 22, '3')):
        a(f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="8" fill="#fff" stroke="{RED}" stroke-width="1.2"/>' + _t(cx, cy + 4, k, 10.5, 'middle', RED, 700).replace('stroke-width:3px', 'stroke-width:0px'))
    # dimensions
    xl = X(0) - 20
    a(_arrow(xl, Y(ny0 / 2), xl, Y(0), INK, 1)); a(_arrow(xl, Y(ny0 / 2), xl, Y(ny0), INK, 1)); a(_t(xl - 6, Y(ny0 / 2) + 4, f'{fr(ny0)}', 10.5, 'end', INK, 600))
    xl2 = X(0) - 52
    a(_arrow(xl2, Y(ny0 + nh / 2), xl2, Y(ny0), INK, 1)); a(_arrow(xl2, Y(ny0 + nh / 2), xl2, Y(ny0 + nh), INK, 1)); a(_t(xl2 - 6, Y(ny0 + nh / 2) + 4, f'{fr(nh)}', 10.5, 'end', INK, 600))
    yt = Y(0) - 12
    a(_dim(X(j3), yt, X(j3 + nw3), yt, f'{fr(nw3)}', 0, INK, 10.5))
    a(_t(X(j3 + nw3) + 14, Y(ny0 + nh / 2) + 4, 'cut 3: along plank 3,', 11, 'start', RED, 600)); a(_t(X(j3 + nw3) + 14, Y(ny0 + nh / 2) + 18, f'{fr(nw3)} in from its rear edge', 11, 'start', RED, 600))
    # the notes, on the right
    X0 = 400
    notes = ['1  Tape over the line (less chipping) and on the', '   saw\'s base plate (no scratches); mark the three lines', '   from the planks\' own top edge and the joint, not', '   from the wall, and check the cut-out is the same', '   size as the nook (17 1/4 x 16).', '',
             'Cut 1 and 2 across both planks with a fine-tooth', 'saw and a square, planks butted together and held', 'flat on a sheet of foam board so the cut is supported', 'all round.', '',
             'Cut 3 along plank 3 only, from cut 1 to cut 2, with the', 'jigsaw and a fine blade (start it in the cut 1 kerf). The', 'planks are hollow, so no corner holes are needed;', 'round the inside corner a little with a file.', '',
             'The strip of plank 3 that is left beyond cut 3', f'({fr(PVC_JOINTS[2] - NOOK[1])} in wide, between the nook and the next joint)', 'stays on the wall. Fill the open flutes of every', 'cut end that faces the nook with sealant.']
    for k, t in enumerate(notes): a(_t(X0, 110 + 16 * k, t, 12, 'start', INK))
    return _svg(820, 590, ''.join(o), 'Cutting the nook out of the planks')

# ---- H  cutting the head and valve holes -----------------------------------------------------------------------------------------------
def fig_holes():
    S = 5.2; OX = 80; OY = 100
    PWd = PW - .25; PH = H
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    hx, hy = HEAD[0] - .125, ZT - HEAD[1]; vx, vy = VALVE[0] - .125, ZT - VALVE[1]          # from the panel's rear edge and its top edge
    nx0, nw, ny0, nh = NOOK[0] - .125, NOOK[1] - NOOK[0], ZT - NOOK[3], NOOK[3] - NOOK[2]
    o = []; a = o.append
    a(_t(20, 24, 'H  The head and valve holes: where to mark them, and how the hole is covered', 14, 'start', INK, 700))
    a(_r(X(0), Y(0), S * PWd, S * PH, '#BFE5DF', TEALD, 1.6)); a(_t(X(PWd / 2), Y(PH) + 18, 'the four planks side by side, face up (rear edge on the left)', 11.5, 'middle', TEALD, 700))
    for jx in PVC_JOINTS: a(_l(X(jx - .125), Y(0), X(jx - .125), Y(PH), TEALD, 1, '2 4'))
    a(_r(X(nx0), Y(ny0), S * nw, S * nh, 'none', '#9AA0A8', 1.2, 'stroke-dasharray="4 3"')); a(_t(X(nx0 + nw / 2), Y(ny0 + nh / 2) + 4, 'nook (cut-out)', 10.5, 'middle', '#7A7F86'))
    for (cx, cy, r, nm, dsz, col) in ((hx, hy, 8, 'head', HEADHOLE, BLU), (vx, vy, 11, 'valve', VALVEHOLE, BLU)):
        a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="{r}" fill="#fff" stroke="{col}" stroke-width="2"/>' + _l(X(cx) - r - 4, Y(cy), X(cx) + r + 4, Y(cy), col, 1) + _l(X(cx), Y(cy) - r - 4, X(cx), Y(cy) + r + 4, col, 1))
    a(_t(X(hx) + 14, Y(hy) + 4, f'head hole {fr(HEADHOLE)}', 11, 'start', BLU, 700)); a(_t(X(vx), Y(vy) + 28, f'valve hole {fr(VALVEHOLE)}', 11, 'middle', BLU, 700))
    a(_t(X(vx), Y(vy) + 41, '(circles drawn bigger than scale)', 10, 'middle', '#5F5E5A'))
    # dimensions from the rear edge (along the top) and from the top edge (down the left)
    yt = Y(0) - 10
    a(_dim(X(0), yt, X(hx), yt, f'{fr(hx)}', 0, INK, 10.5)); a(_dim(X(0), yt - 18, X(vx), yt - 18, f'{fr(vx)}', 0, INK, 10.5))
    xl = X(0) - 16
    a(_arrow(xl, Y(hy / 2), xl, Y(0), INK, 1)); a(_arrow(xl, Y(hy / 2), xl, Y(hy), INK, 1)); a(_t(xl - 6, Y(hy / 2) + 4, f'{fr(hy)}', 10.5, 'end', INK, 600))
    xl2 = X(0) - 48
    a(_arrow(xl2, Y(vy / 2), xl2, Y(0), INK, 1)); a(_arrow(xl2, Y(vy / 2), xl2, Y(vy), INK, 1)); a(_t(xl2 - 6, Y(vy / 2) + 4, f'{fr(vy)}', 10.5, 'end', INK, 600))
    a(_l(xl2, Y(vy), X(vx), Y(vy), '#B4B2A9', .8, '3 3')); a(_l(xl, Y(hy), X(hx), Y(hy), '#B4B2A9', .8, '3 3'))
    # the section through one hole (the head's): the wall on the left, the stall on the right
    T0 = 520; CY = 250; Sc = 60
    a(_t(T0 - 90, 64, 'A hole in section (the wall on the left)', 12.5, 'start', INK, 700))
    ply = Sc * .375; frp = Sc * LT; ph = Sc * .875; hh = Sc * 1.125; fh = Sc * 2.5; ft = Sc * .35
    a(_r(T0 - ply, CY - 130, ply, 260, PLY, INK, 1.1)); a(_r(T0 - ply - 1, CY - Sc * .65, ply + 2, Sc * 1.3, '#fff', '#fff', .1))           # the plywood, with its hole
    a(_r(T0, CY - 130, frp, 260, TEAL, TEALD, .8)); a(_r(T0 - 1, CY - hh / 2, frp + 2, hh, '#fff', '#fff', .1))                           # the FRP, with its hole
    a(_r(T0 - 100, CY - ph / 2, 330, ph, '#B9BCC2', INK, 1.2))                                                                              # the shower arm
    a(_r(T0 + frp, CY - fh / 2, ft, fh, '#D8D8D4', INK, 1.4)); a(_r(T0 + frp, CY - ph / 2, ft, ph, '#B9BCC2', INK, 1.2))                      # the flange
    for yy in (CY - fh / 2 + 4, CY + fh / 2 - 12): a(_r(T0 + frp - 3, yy, 5, 9, SEAL, '#2E5B49', 1))                                       # the sealant ring on its back
    RX = T0 + 90
    a(_call(T0 + frp / 2, CY - 100, RX, CY - 150, f'PVC plank ({fr(LT)} in)', 'start', TEALD, 11.5))
    a(_call(T0 + frp + ft / 2, CY - fh / 2 + 4, RX, CY - 128, 'flange hides the hole', 'start', INK, 11.5))
    a(_call(T0 + frp - 1, CY - fh / 2 + 8, RX, CY - 106, 'sealant ring behind it', 'start', '#2E5B49', 11.5))
    a(_arrow(T0 + 70, CY, T0 + 70, CY - fh / 2, INK, 1)); a(_arrow(T0 + 70, CY, T0 + 70, CY + fh / 2, INK, 1)); a(_t(T0 + 80, CY + 50, '2 1/2 in flange', 10.5, 'start', INK, 600)); a(_t(RX, CY + 66, 'the flange overlaps the hole', 10.5, 'start', '#5F5E5A')); a(_t(RX, CY + 79, 'by at least 1/2 in all round', 10.5, 'start', '#5F5E5A'))
    a(_t(T0 + 150, CY - ph / 2 - 8, 'shower arm', 11, 'start', INK, 600))
    LX = T0 - 60
    a(_call(T0 - ply / 2, CY - 110, LX, CY - 140, 'plywood 3/8', 'end', '#5F5E5A', 11.5))
    a(_call(T0 + frp / 2, CY + hh / 2 - 4, LX, CY + 95, 'hole 1/4 in bigger than the pipe:', 'end', RED, 11.5)); a(_t(LX - 8, CY + 109, '1/8 in clear all round', 11, 'end', RED))
    a(_t(T0 + 30, 96, 'the stall side', 10.5, 'start', '#5F5E5A', 600)); a(_t(T0 - 40, 96, 'behind', 10.5, 'end', '#5F5E5A', 600))
    a(_t(20, 520, 'Check the real pipe and valve before you cut: the stubs can sit a little off the plan\'s numbers.', 11.5, 'start', RED, 600))
    return _svg(760, 545, ''.join(o), 'Cutting the head and valve holes')

# ---- I  sealing around the valve ------------------------------------------------------------------------------------------------------
def fig_valve():
    S = 34; CX, CY = 190, 215
    o = []; a = o.append
    a(_t(20, 24, 'I  Sealing around the valve (the head\'s flange is done the same way)', 14, 'start', INK, 700))
    a(_t(20, 54, 'From the front', 12.5, 'start', INK, 700))
    a(_r(40, 70, 300, 290, '#BFE5DF', TEALD, 1.4))
    a(f'<circle cx="{CX}" cy="{CY}" r="{S * 2.4:.1f}" fill="none" stroke="#6CA6D9" stroke-width="{S * .3:.1f}" opacity=".55"/>')                      # painter's tape ring
    a(f'<circle cx="{CX}" cy="{CY}" r="{S * 2.125:.1f}" fill="none" stroke="{SEAL}" stroke-width="{S * .25:.1f}"/>')                                     # the outer bead, tooled
    a(f'<circle cx="{CX}" cy="{CY}" r="{S * 2:.1f}" fill="#D8D8D4" stroke="{INK}" stroke-width="1.6"/>')                                                   # the trim plate
    a(f'<circle cx="{CX}" cy="{CY}" r="{S * 1.75:.1f}" fill="none" stroke="{SEAL}" stroke-width="3" stroke-dasharray="7 4"/>')                            # the ring behind the plate
    a(f'<circle cx="{CX}" cy="{CY}" r="{S * 1.125:.1f}" fill="none" stroke="#7A7F86" stroke-width="1.2" stroke-dasharray="2 3"/>')                        # the hole under the plate
    a(f'<circle cx="{CX}" cy="{CY}" r="{S * .55:.1f}" fill="#B9BCC2" stroke="{INK}" stroke-width="1.2"/>')                                                # the handle's stem
    for sx in (-1, 1): a(f'<circle cx="{CX + sx * S * 1.45:.1f}" cy="{CY}" r="4.5" fill="#fff" stroke="{INK}" stroke-width="1.2"/>')
    LX = 372
    a(_call(CX + S * 2.12 * .71, CY - S * 2.12 * .71, LX, 100, '3  bead, tooled flat, between the tape and the plate', 'start', '#2E5B49', 11.5))
    a(_call(CX + S * 2.4 * .71, CY + S * 2.4 * .71, LX, 150, 'painter\'s tape, 1/4 in outside the plate', 'start', '#3E7FBF', 11.5))
    a(_call(CX - S * 1.75 * .71, CY - S * 1.75 * .71, LX, 200, '1  ring of sealant on the back of the plate', 'start', '#2E5B49', 11.5)); a(_t(LX + 8, 218, '(hidden: a closed ring, no gaps)', 11, 'start', '#2E5B49'))
    a(_call(CX + S * 1.45, CY, LX, 270, '2  the plate\'s own screws go into the valve,', 'start', INK, 11.5)); a(_t(LX + 8, 288, 'never into the panel alone', 11, 'start', INK))
    a(_call(CX, CY, LX, 340, 'the handle and cartridge: the valve\'s own seals', 'start', '#5F5E5A', 11.5))
    # the section: wall on the left, the stall on the right
    T0 = 250; Sc = 40; CYs = 590
    a(_t(20, 410, 'In section (the wall on the left)', 12.5, 'start', INK, 700))
    ply = Sc * .375; frp = Sc * LT; ph = Sc * .3; plate = Sc * 4; hole = Sc * 2.25; cart = Sc * 2
    a(_r(T0 - ply, CYs - 130, ply, 260, PLY, INK, 1.1)); a(_r(T0 - ply - 1, CYs - hole / 2 - 4, ply + 2, hole + 8, '#fff', '#fff', .1))
    a(_r(T0, CYs - 130, frp, 260, TEAL, TEALD, .8)); a(_r(T0 - 1, CYs - hole / 2, frp + 2, hole, '#fff', '#fff', .1))
    a(_r(T0 - 130, CYs - cart / 2, 190, cart, '#B9BCC2', INK, 1.2))                                                                                    # the valve's cartridge through the hole
    a(_r(T0 + frp, CYs - plate / 2, ph, plate, '#D8D8D4', INK, 1.4))                                                                                     # the plate
    for yy in (CYs - plate / 2 + 12, CYs + plate / 2 - 21): a(_r(T0 + frp - 3, yy, 5, 9, SEAL, '#2E5B49', 1))                                              # the ring behind it
    for sy in (-1, 1): a(_p([(T0 + frp + ph, CYs + sy * plate / 2), (T0 + frp + ph + 13, CYs + sy * plate / 2), (T0 + frp + ph, CYs + sy * (plate / 2 + 13))], SEAL, '#2E5B49', 1))   # the tooled outer bead
    for sy in (-1, 1): a(_r(T0 + frp, CYs + sy * (plate / 2 + 18) - 3, 3, 6, '#6CA6D9', '#3E7FBF', .8))                                                   # the tape
    RX = 420
    a(_call(T0 + frp + ph + 8, CYs - plate / 2 + 1, RX, CYs - 130, '3  tooled bead', 'start', '#2E5B49', 11.5))
    a(_call(T0 + frp + ph / 2, CYs - plate / 2 + 6, RX, CYs - 102, '2  plate pressed on the ring', 'start', INK, 11.5))
    a(_call(T0 + frp - 1, CYs - plate / 2 + 16, RX, CYs - 74, '1  ring of sealant behind the plate', 'start', '#2E5B49', 11.5))
    a(_call(T0 + frp, CYs - plate / 2 - 18, RX, CYs - 164, 'painter\'s tape, pulled off before it skins', 'start', '#3E7FBF', 11.5))
    a(_t(RX, CYs + 90, 'The plate overlaps the hole', 11, 'start', '#5F5E5A')); a(_t(RX, CYs + 104, 'by at least 1/2 in all round.', 11, 'start', '#5F5E5A'))
    a(_t(T0 - 130, CYs + 150, 'valve cartridge through the hole', 11, 'start', INK))
    a(_t(20, 770, 'Do the head\'s flange the same way. Wait a day before any water.', 11.5, 'start', RED, 600))
    return _svg(760, 790, ''.join(o), 'Sealing around the valve')

FIGS = [
    ('A', 'The pan from above', fig_top, 'The bought pan sits against the plywood wall. The back wall is lined with PVC paneling; the other three sides have no wall, only two curtains on a rail on the ceiling that runs round them 1 1/2 in inside the pan\'s edge. The nook is centered on the pan. The drain hole is at the middle of the rear-door end, 5 in from the rear end (you said) and 12 out (the middle of the depth: check it on the pan). The floor falls to it.'),
    ('B', 'The pan edge and the sealed gap', fig_edge, 'A stiff plank cannot lap over the pan lip, so it stops 1/4 in above the pan edge and the gap is filled with flexible sealant, pressed into the open flutes of the plank: the water runs down the plank, over the sealant and into the pan. The plywood edge below it is sealed and hidden behind the lip.'),
    ('C', 'The drain through the floor', fig_drain, 'The flange is bedded in neutral silicone on the pan, the body goes through the subfloor and the steel, a gasket and a lock nut hold it from below, and the bare steel edge of the hole is primed against rust. A P-trap and a hose take it to the grey tank, which must be vented (its place is not set).'),
    ('D', 'The planks on the wall', fig_wall, 'Four planks stood on end (joints at 9 3/8, 19 1/8 and 28 7/8 in, the first at the nook\'s rear edge) with the nook cut out of planks 2 and 3. The head (in plank 1) and the valve (in plank 2, under the nook\'s rear end) are hole-sawed through and sealed behind their flanges. The two ends have end trim; there is no end wall and no corner.'),
    ('E', 'Cutting the planks', fig_cut, 'Four 10 in x 8 ft planks and a spare are enough: the wall pieces are 69 15/16 in, the cut-outs of planks 2 and 3 are the nook\'s back, and their 26 in offcuts are the nook\'s floor, ceiling and sides.'),
    ('F', 'The joint and the end trim', fig_corner, 'The tongue and groove joint closes to a hairline, with the adhesive in dabs behind the plank and none in the joint; each free edge (the rear end and the cab end) stops 1/8 in short of its J-shaped trim, and the gap is filled with flexible sealant.'),
    ('G', 'Cutting the nook out of the planks', fig_nook, 'Cut it flat on the bench before the planks go on the wall: lay planks 2 and 3 butted together, mark the lines from the planks\' own top end and joint, cut across both (cuts 1 and 2) with a fine-tooth saw, then along plank 3 (cut 3) with a jigsaw. The cut-out is the nook back.'),
    ('H', 'The head and valve holes', fig_holes, 'Mark each hole from its own plank (head: 6 7/8 in along and 4 down on plank 1; valve: 1 5/8 along and 38 down on plank 2), check it against the real pipe and valve, cut it with a hole saw 1/4 in bigger than the part that goes through, and hide it under the flange or trim plate with a ring of flexible sealant behind it.'),
    ('I', 'Sealing around the valve', fig_valve, 'Three layers: a closed ring of sealant on the back of the plate (1), the plate pressed on it, and a thin tooled bead around the plate\'s edge, laid between painter\'s tape and the plate (3). The valve\'s own seals look after the cartridge.')]

PARTS = [
    ('Shower pan', '36 x 24 in, 3 in curb (bought)', '1', 'measure the drain hole (its distance from the rear end and the wall, its size) and the height of the lip against the wall, and change the plan\'s sizes to match'),
    ('PVC wall paneling', 'tongue and groove planks, 10 in wide (about 9 3/4 covering) x 8 ft x 5/16 in (8 mm), hollow core, white or light, smooth', '5', 'four stood on end for the back wall (joints at 9 3/8, 19 1/8 and 28 7/8 in from the back) and a spare; the cut-outs and the offcuts of planks 2 and 3 line the nook; about 9 lb in all (a rough weight); measure the real width and thickness before you cut'),
    ('PVC panel adhesive', 'a flexible construction adhesive the panel maker approves for PVC (polyurethane or MS polymer: solvent-based adhesives can craze PVC), 10 oz cartridges', 'about 4', 'dabs about 8 in apart behind each plank, never in a joint or near an edge; follow the cartridge for the open time and the temperature'),
    ('Paneling tools and safety', 'fine-tooth saw (24 teeth per inch) and a jigsaw with a fine blade, utility knife, square, level or plumb line, 3 in hand roller, masking and painter\'s tape, 1/8 in and 1/4 in spacers, caulk gun, hole saws, dust mask and glasses', '1 set', 'cut a plank at a time, supported all along; PVC chips and dust irritate eyes and lungs'),
    ('J-shaped end trim and top trim', 'PVC J-trim in the plank color, 8 ft, and the trim strip under the ceiling', '2 and 1', 'the rear end and the cab end of the paneling (69 15/16 in each); the top edge goes under the ceiling trim strip'),
    ('Flexible sealant', 'neutral-cure silicone or MS polymer, mold-resistant, white or clear', '4 tubes', 'drain flange, the pan joint, the pan lip, the flutes at cut ends, the trims, the nook corners, valve and head flanges; never a hard caulk'),
    ('Pan bedding', 'flexible polyurethane or MS-polymer construction adhesive, 28 oz tubes or 10 oz cartridges', 'about 3 cartridges', 'zig-zag beads every 3 in under the pan; not a rigid mortar (the van flexes and the mortar cracks)'),
    ('Shower drain', 'fits the pan\'s drain hole, with a gasket and a lock nut from below; 1 1/2 in tailpiece', '1', 'check whether the pan comes with one'),
    ('P-trap and hose', '1 1/2 in trap (or a waterless trap valve) and 1 1/2 in flexible hose', '1', 'to the grey tank, which needs a vent (the tank\'s place is not set)'),
    ('Hole saws', 'bi-metal or carbide: the drain (body + 1/4 in), the head arm (1 1/8 in) and the valve (2 1/4 in), or 1/4 in bigger than your own parts', '3', 'a hole saw for each, never a twist drill through the planks'),
    ('Epoxy and rust primer', 'thin epoxy for the plywood edges and cut-outs; rust converter and epoxy primer for the steel edge of the drain hole', '1 each', 'two coats of epoxy on every cut edge of the plywood in the stall'),
]
STEPS = [
    "<b>Measure the pan before anything is cut.</b> Write down its length and depth (36 x 24), the height of its curb and of its lip against the wall, the size of the drain hole and how far it is from the rear end and from the wall (you said the middle of the rear-door end, 5 in from the rear end; the plan has it at 5 in along and 12 out, the middle of the depth, which is my guess), and the thickness and the covering width of the PVC planks (5/16 in and 9 3/4 in are placeholders). Put the real numbers into the plan's sizes (Shower drain hole, Liner), so the drawings and checks follow.",
    "<b>Look under the floor where the hole goes.</b> Cross-members, wires, brake or fuel lines and the grey tank's place all matter before you drill. The hole at the middle of the rear-door end is near the rear bumper area: check it clears the frame.",
    "<b>Check and prepare the floor.</b> The subfloor under the pan must be flat to 1/8 in over the 36 x 24 in (a 4 ft level or a straightedge). Fill any dip with a flexible leveling filler or shim it; the pan's floor is thin and a fiberglass or acrylic pan must be supported all over, or it cracks where you stand.",
    '<b>Drill the drain hole.</b> Dry-fit the pan, mark the center of its drain hole on the floor, take the pan out, drill a pilot hole through the subfloor and the steel, then cut with a hole saw 1/4 in bigger than the drain body. Deburr the steel edge, treat it with rust converter and epoxy primer, and seal the cut edge of the subfloor with epoxy. Vacuum all the chips out of the van.',
    "<b>Bed the pan.</b> Run zig-zag beads of the flexible adhesive over the subfloor about every 3 in (keep it 2 in back from the hole), bed the drain flange in neutral silicone on the pan, set the pan down against the plywood wall with its rear end at the back mark (the cab end is just a curtain, so nothing stops it there: measure 36 in from the back mark), and press it. Check it is level side to side and falls to the drain. Weigh it down (jugs of water, 100 lb) for the adhesive's open time and wipe the squeeze-out.",
    '<b>Connect the drain from below:</b> gasket and lock nut on the body, then the tailpiece, the P-trap and the hose to the grey tank, with a vent on the tank. Keep the hose falling all the way to the tank.',
    '<b>Seal the pan to the wall.</b> A bead of flexible sealant where the pan lip meets the plywood, and the plywood edge below the planks sealed with epoxy (drawing B).',
    '<b>Fill test.</b> Plug the drain, fill the pan to just under the curb, mark the water line and leave it for a day. Check the line has not dropped and look under the floor for any drip. Then open the drain, check it flows freely and leaks nowhere at the nut or the trap.',
    '<b>Prepare the plywood before the planks go on.</b> (1) Two coats of thin epoxy on every cut edge and on the bare plywood of the nook and of the valve and head cut-outs: water gets in from the edges. (2) Make the face flat. The screws that hold the plywood have finish washers, and a washer would show through a 5/16 in plank as a bump and stop it sticking: in the stall, countersink each screw (or refit it with a flat head) and fill the dimple with epoxy filler, then sand it flush; sand off raised grain, fill any gouge, and check with a straightedge that nothing stands more than about 1/16 in proud (the hollow planks bridge a small dip, never a bump). (3) Vacuum the dust and wipe the face with a damp cloth: it must be clean, dry and free of oil where the adhesive goes (scuff-sand any epoxy that reached the face). (4) Mark the joints with a level or a plumb line from the back mark: at 9 3/8, 19 1/8 and 28 7/8 in, the first at the nook\'s rear edge so that the nook\'s edges fall on joints; if your planks cover a different width, redo the sum from the nook\'s rear edge (the plan\'s size "PVC plank width" does it).',
    '<b>Cut the planks</b> (drawing E). (1) Let the planks sit in the van for at least 24 hours first, so they match its temperature (PVC moves with heat, about 1/16 in over 8 ft for each 15 F). (2) Cut each to 69 15/16 in: it stops 1/4 in above the pan edge and 1/8 in under the trim strip at the ceiling. (3) Rip plank 1 down to 9 1/4 in and plank 4 to 7 in (so each stops 1/8 in short of its end trim), on the edge that is not the tongue. (4) Use a fine-tooth saw (24 teeth per inch) or a jigsaw with a fine blade, a plank at a time, supported all along; a thin plank can be scored with a utility knife and snapped. (5) Dry-fit all four on the wall, tongues toward the cab, and number them 1 to 4 on the back.',
    "<b>Cut the nook out of planks 2 and 3</b> (drawing G), flat on the bench before gluing. (1) Lay the two planks butted together, face up, on foam board or a sacrificial sheet, so the cut is supported all round. (2) Measure from the planks' own top ends, not from the wall: the nook starts 20 in down from the top (the nook top is at 54, the planks' top at 74) and is 16 in tall; plank 2 is cut through at both lines (it is all inside the nook), and plank 3 is cut through at both lines and then along its length 7 1/2 in from its rear edge (the nook ends at 26 5/8 in, and plank 3 starts at 19 1/8). (3) Put painter's tape over the lines and on the saw's base plate. (4) Make cuts 1 and 2 across both planks with a fine-tooth saw and a square, then cut 3 with a jigsaw and a fine blade, starting it in the kerf of cut 1. (5) Save the two cut-outs: they are the back of the nook, and their tongue and groove still fit each other. (6) File the cut edges smooth, round the inside corners a little, and seal the open flutes of every cut end that faces the nook with a dab of sealant.",
    "<b>Cut the head and valve holes</b> (drawing H), flat on the bench before gluing. (1) Mark each from its own plank: the head hole's center is 6 7/8 in from plank 1's rear edge (the head is 7 in along) and 4 in down from its top end (the head is 70 up); the valve hole's center is 1 5/8 in from plank 2's rear edge (the valve is 11 in along, the joint is at 9 3/8) and 38 in down from its top end (the valve is 36 up). The valve hole then clears the joint by 1/2 in. (2) Check them against the real plumbing before you cut: the stubs move a little when they are roughed in, so the pipe's true position beats the plan. Dry-fit the plank on its spacers and compare, or tape a cardboard template to the wall, mark the centers through it and carry them to the plank. (3) Size each hole from your own parts, not from mine: 1/4 in bigger than the part that goes through (a 1/2 in shower arm is 7/8 in across, so 1 1/8 in; a single-handle valve cartridge is about 2 in, so 2 1/4 in), and small enough that the flange or plate overlaps it by at least 1/2 in all round. (4) Cut with a hole saw, slowly and with the plank face up on the foam board, so the PVC does not melt or crack; never a twist drill. (5) Seal the flutes that the hole opens with a dab of sealant.",
    "<b>Glue the planks on, starting at the nook.</b> (1) Dab the flexible adhesive on the plywood in beads about 8 in apart down each plank's width, never near a joint or an edge, and only as many planks as you can fit in the open time on the cartridge (cool or warm, as it says). (2) Set plank 2 first, its rear edge exactly on the line at 9 3/8, resting on 1/4 in spacers on the pan, plumb with a level; press it flat from the middle outward and roll the face. (3) Slide plank 3 in (tongue into groove, closing the joint to a hairline, not forcing it), then plank 4 the same way. (4) Put plank 1 in last, its tongue into plank 2's groove, 1/8 in off the rear end. (5) Hold the planks with strips of masking tape for the first hour, keep the van within the temperatures the cartridge allows while it cures, and wipe any squeeze-out at once. (6) Leave the spacers in until the adhesive has set.",
    '<b>Line the nook.</b> Glue the two cut-outs to the plywood back of the nook as its back (tongue into groove), then its floor, its ceiling and its two sides from the offcuts (the floor and the ceiling are 17 1/4 x 4 1/2 in, the sides 16 x 4 1/2 in), each in dabs of adhesive and each butted to the back, with a bead of sealant in every inside corner. The front edges are left open, with no lip: a bungee cord across the front keeps things in. Use a 4 in roll: the nook is about 4 1/4 in clear inside the lining.',
    '<b>Seal and trim.</b> Fit the J-shaped end trim over the plank edges at the rear end and at the cab end, glued to the plywood, with a bead of sealant in the 1/8 in gap behind each (drawing F); fit the top trim strip under the ceiling; fill the 1/4 in gap at the pan with flexible sealant and tool it, pressing it into the open flutes; seal every nook corner and behind the head and valve flanges; wipe the excess off straight away. Let it cure a day.',
    "<b>Seal around the valve and the head</b> (drawing I), after the planks are glued and the valve and the shower arm are in, with the trim plates off. (1) Wipe the plank around each hole and the back of each plate with isopropyl alcohol and let it dry. (2) Dry-fit the plate: it must cover its hole by at least 1/2 in all round. (3) Run a continuous 1/8 in bead of neutral-cure silicone or MS polymer on the back of the plate, in a closed ring about 1/4 in in from its edge, with no gaps (overlap the ends). (4) Press the plate on and tighten its own screws, which go into the valve fitting and never into the plank alone, until the bead squeezes out evenly all round; do not over-tighten, which cracks the plank or the plate. (5) Stick painter's tape on the panel 1/4 in outside the plate's edge, run a thin bead in the gap between the tape and the plate, smooth it in one pass with a wet finger or a tool, and pull the tape off before it skins. (6) Leave the cartridge and the handle alone: the valve's own seals look after them. (7) Wait a day, then run the shower for ten minutes and look for wet behind (from under the floor or through the valve access); touch up any pinhole. Check these beads once a year and redo any that crack or go black.",
    '<b>Finish and test.</b> Fit the head and valve, hang the curtains from the ceiling rail and the nook cord (the Wet bath page), then run the shower for ten minutes with the curtains closed and check under the floor and along the bottom of the back wall, and where the cab-end curtain hangs by the fridge, for any wet.',
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
