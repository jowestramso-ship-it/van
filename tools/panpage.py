"""The shower pan page of the build guide: how to set the bought 36 x 24 pan, drain it and line the back wall of the stall with ONE solid 4 x 8 ft PVC paneling sheet over the 3/8 in plywood, with a small hinged door in it that carries the shower valve. The cab end of the stall is the wall W5 (user, 2026-11-14) and the other two sides, the rear end and the front, are curtains.
Nine drawings made from the plan's numbers (the pan, the sheet, the nook, the head, the valve door, the drain hole), a parts table and the steps in order.
Used by buildguide.py (the Shower pan page); run on its own it writes ../pan.html for a quick look.
The shared numbers (the nook, the head and the valve, the sheet thickness, the valve door VD_*, the curtain rail) come from shelfdata.py, the same as ia_core.js; the drain hole is at the middle of the rear-door end, 5 in from the rear end (the user's measurement; the 12 in out from the wall is the middle of the depth, assumed),
the pan's lip height against the wall is a guess, and PVC paneling is the user's choice ('The back wall will be lined with pvc paneling, including the nook'): change them here, in shelfdata.py, in ia_core.js (pdrX, pdrY, linerT, pvcSheet, vdoorOn, vdoorW, linerTop, linerGap, curIn) and in plan.py together."""
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
LT = LINER_T                    # the sheet's thickness (5/16 in: a placeholder, measure yours: a 4 x 8 sheet is often thinner)
NOOK = (SN_X0, SN_X1, SN_Z0, SN_Z1)    # the shower nook: x0, x1, z0, z1 (4 1/2 in deep, in the wall), centered on the pan
HEAD = (HEAD_X, HEAD_Z); VALVE = (VALVE_X, VALVE_Z)
HEADHOLE, VALVEHOLE = 1.125, 2.25    # the head hole is in the sheet and the valve hole in the door: the part that goes through + 1/4 in (a 1/2 in shower arm is 7/8 across; a single-handle valve cartridge is about 2 in: PLACEHOLDERS, measure the real parts)
DRAIN = (5, 12)                 # 5 in from the rear end (the user), 12 out = the middle of the depth (assumed)
TOILET = (TOILET_X[0], TOILET_X[1], 4.75, 19.25)
RAILW = 3.5                                    # the furring rails S4 and S5 (3 1/2 wide, centers 30 1/4 and 43 1/2 up): the valve opening runs from the top of S4 to the bottom of S5
assert (30.25 + RAILW / 2, 43.5 - RAILW / 2) == (VD_Z0, VD_Z1) and PVC_SHEET
OPEN = (VD_X0, VD_X1, VD_Z0, VD_Z1)                             # the opening in the sheet and the plywood: 25 1/2 to 33 1/2 along, 32 to 41 3/4 up
DOOR = (VD_X0 - VD_OV, VD_X1 + VD_OV, VD_Z0 - VD_OV, VD_Z1 + VD_OV)   # the door: 25 to 34 along, 31 1/2 to 42 1/4 up (9 x 10 3/4)
DW, DH = DOOR[1] - DOOR[0], DOOR[3] - DOOR[2]
GASKET, DOORT = .1875, .5                      # closed-cell foam gasket 3/16 in (1/8 squeezed), door board 1/2 in
RJ = (SN_X1, SN_X1 + 1.5, VD_Z0, SN_Z0)        # the rear jamb: a short piece of 1x2 under the nook frame V2 (24 to 25 1/2 along, 32 to 38 up), so the door has wood behind its rear edge
CJ = (VD_X1, VD_X1 + 1.5, VD_Z0, VD_Z1)        # the cab-side jamb: 1x2 between S4 and S5 (33 1/2 to 35 along): the hinge and the cab-side screws go into it
HINGE_LEN = 6                                  # a 6 in piece of mini piano hinge, centered on the door's cab edge, so that the corner screws clear it
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
    a(_l(X(0), Y(0) + 2, X(PW), Y(0) + 2, TEAL, 4)); a(_t(X(PW) - 4, Y(0) + 17, 'PVC paneling on the wall (one sheet)', 10.5, 'end', TEALD, 600))
    a(_l(X(DOOR[0]), Y(0) + 5, X(DOOR[1]), Y(0) + 5, BLU, 5)); a(_t(X(PW) + 8, Y(0) + 6, 'valve door', 10.5, 'start', BLU, 600))
    yF = PD - CUR_IN
    a(f'<polyline points="{X(CUR_IN):.1f},{Y(0):.1f} {X(CUR_IN):.1f},{Y(yF):.1f} {X(PW - .5):.1f},{Y(yF):.1f}" fill="none" stroke="{INK}" stroke-width="2.4" stroke-dasharray="8 4"/>')
    a(_r(X(PW), Y(0), S * .75, S * PD, '#8A6B4D', '#3E230B', 1.2, '') + _t(X(PW) + 14, Y(PD) - 6, 'W5', 12, 'middle', '#5A3A00', 700))
    a(_l(X(CUR_IN), Y(.8), X(CUR_IN), Y(yF + .3), PUR, 4)); a(_l(X(CUR_IN), Y(yF + .3), X(PW / 2 + 3), Y(yF + .3), PUR, 4))
    a(_l(X(PW - .5), Y(yF - .9), X(PW / 2 - 3), Y(yF - .9), '#B07ACB', 4))
    tx0, tx1, ty0, ty1 = TOILET
    a(_r(X(tx0), Y(ty0), S * (tx1 - tx0), S * (ty1 - ty0), 'none', '#993556', 1.6, 'stroke-dasharray="6 3"')); a(_t(X((tx0 + tx1) / 2), Y((ty0 + ty1) / 2) + 4, 'toilet (stays set up)', 10.5, 'middle', '#993556'))
    a(f'<circle cx="{X(HEAD[0]):.1f}" cy="{Y(6):.1f}" r="7" fill="#fff" stroke="{BLU}" stroke-width="1.6"/>' + _t(X(HEAD[0]) + 11, Y(6) + 4, 'shower head', 10.5, 'start', BLU))
    dx, dy = DRAIN
    a(f'<circle cx="{X(dx):.1f}" cy="{Y(dy):.1f}" r="{S * 1.1:.1f}" fill="{INK}"/>')
    a(_t(X(dx) + 22, Y(dy) - 32, 'drain hole', 12, 'start', INK, 700)); a(_t(X(dx) + 22, Y(dy) - 18, f'{fr(dx)} in along, {fr(dy)} out', 11, 'start', INK)); a(_t(X(dx) + 22, Y(dy) - 4, '(12 out: check it)', 11, 'start', RED, 600))
    a(_arrow(X(14), Y(17), X(6.6), Y(13.3), BLU, 1.6)); a(_arrow(X(14), Y(13.8), X(6.5), Y(12.7), BLU, 1.6)); a(_arrow(X(2.2), Y(21), X(3.4), Y(14.4), BLU, 1.6))
    a(_t(X(9), Y(21) + 2, 'floor falls to the drain', 10.5, 'start', BLU))
    a(_t(X(0) - 8, Y(18), 'rear-door end', 11, 'end', '#5F5E5A', 600)); a(_t(X(0) - 8, Y(18) + 13, '(a curtain)', 10.5, 'end', '#5F5E5A'))
    a(_t(X(PW) + 24, Y(18), 'cab end', 11, 'start', '#5F5E5A', 600)); a(_t(X(PW) + 24, Y(18) + 13, '(the wall W5,', 10.5, 'start', '#5F5E5A')); a(_t(X(PW) + 24, Y(18) + 26, 'then the fridge)', 10.5, 'start', '#5F5E5A'))
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
    a(_t(X(2.6), Z(5.5), 'water runs down the sheet,', 11.5, 'start', BLU, 600)); a(_t(X(2.6), Z(5.5) + 14, 'over the sealant, into the pan', 11.5, 'start', BLU, 600))
    a(_call(X(.1), Z(6.55), X(5.2), Z(6.65), f'PVC sheet, {fr(LT)} in (measure yours)', 'start', TEALD))
    a(_call(X(.03), Z(4.6), X(5.2), Z(4.35), 'adhesive under the sheet', 'start', '#8A6A00'))
    a(_call(X(.2), Z(ZB - .12), X(5.2), Z(3.3), f'{fr(GAP)} in gap filled with flexible sealant', 'start', '#2E5B49'))
    a(_call(X(.14), Z(2.5), X(5.2), Z(2.6), 'pan lip, sealed to the plywood', 'start', BLU))
    a(_call(X(8.6), Z(1.42), X(8.0), Z(2.2), 'pan floor', 'start', BLU))
    a(_call(X(9.2), Z(1.17), X(10.4), Z(1.75), 'adhesive bed', 'start', '#8A6A00'))
    a(_call(X(-.2), Z(1.2), X(-1.7), Z(2.4), 'edge sealed', 'end', INK))
    return _svg(760, 400, ''.join(o), 'Section at the wall: pan lip, sealed gap and PVC sheet')


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

# ---- D  the sheet on the wall ------------------------------------------------------------------------------------------------------
def fig_wall():
    S = 7.0; OX = 270; FL = 640
    X = lambda x: OX + S * (PW - x); Z = lambda z: FL - S * z       # the rear end on the right, the cab on the left, as in the plan's passenger view
    o = []; a = o.append
    a(_t(20, 24, 'D  The PVC sheet on the back wall, seen from inside (the cab to the left, the rear to the right)', 14, 'start', INK, 700))
    nx0, nx1, nz0, nz1 = NOOK
    a(_r(X(PW - RE), Z(ZT), S * (PW - 2 * RE), S * H, TEAL, TEALD, 1.2, 'fill-opacity=".16"'))
    a(_t(X(PW / 2), Z(ZT) + 18, 'one sheet, no joints', 12, 'middle', TEALD, 700))
    # behind the sheet (dotted): the furring rails S4 and S5 and the frame of the valve door
    a(_r(X(PW), Z(30.25 + RAILW / 2), S * PW, S * RAILW, 'none', FURR, 1, 'stroke-dasharray="2 3"')); a(_t(X(0) + 6, Z(30.25) + 4, 'S4', 10.5, 'start', FURR, 600))
    for (rx0, rx1) in ((0, SN_X0 - 1.5), (SN_X1 + 1.5, PW)):
        a(_r(X(rx1), Z(43.5 + RAILW / 2), S * (rx1 - rx0), S * RAILW, 'none', FURR, 1, 'stroke-dasharray="2 3"'))
    a(_t(X(0) + 6, Z(43.5) + 4, 'S5', 10.5, 'start', FURR, 600))
    for (fx0, fx1, fz0, fz1) in (RJ, (SN_X1, SN_X1 + 1.5, SN_Z0, SN_Z1), CJ):
        a(_r(X(fx1), Z(fz1), S * (fx1 - fx0), S * (fz1 - fz0), '#F6EBD4', FURR, 1, 'stroke-dasharray="2 3"'))
    a(_r(X(PW), Z(PANTOP), S * PW, S * PANTOP, PAN, BLU, 1.4)); a(_t(X(18), Z(1.5) + 4, 'pan, 3 in curb', 10.5, 'middle', BLU))
    a(_r(X(PW), Z(PANTOP + GAP), S * PW, S * GAP + 1, SEAL, SEAL, 1))
    a(_r(X(nx1), Z(nz1), S * (nx1 - nx0), S * (nz1 - nz0), '#fff', FURR, 1.5, 'stroke-dasharray="5 3"'))
    hx, hz = HEAD; a(f'<circle cx="{X(hx):.1f}" cy="{Z(hz):.1f}" r="9" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    # the valve door: the opening (dashed) under the door, its hinge on the cab side (the left here), four screws, and the valve on it
    a(_r(X(DOOR[1]), Z(DOOR[3]), S * DW, S * DH, '#DCEAF6', BLU, 1.8))
    a(_r(X(OPEN[1]), Z(OPEN[3]), S * (OPEN[1] - OPEN[0]), S * (OPEN[3] - OPEN[2]), 'none', BLU, 1, 'stroke-dasharray="3 3"'))
    dzc = (DOOR[2] + DOOR[3]) / 2
    a(_l(X(DOOR[1]), Z(dzc + HINGE_LEN / 2), X(DOOR[1]), Z(dzc - HINGE_LEN / 2), INK, 4))
    for sx in (DOOR[0] + .25, DOOR[1] - .25):
        for sz in (DOOR[2] + .25, DOOR[3] - .25): a(f'<circle cx="{X(sx):.1f}" cy="{Z(sz):.1f}" r="2.8" fill="#E0E3E6" stroke="{INK}" stroke-width="1"/>')
    vx, vz = VALVE; a(f'<circle cx="{X(vx):.1f}" cy="{Z(vz):.1f}" r="10" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    a(_l(X(PW), Z(ZT), X(PW), Z(ZB), FURR, 4)); a(_l(X(0), Z(ZT), X(0), Z(ZB), FURR, 4))
    a(_dim(X(PW), Z(ZT) - 22, X(0), Z(ZT) - 22, f'{PW} in along the wall (one sheet, cut 1/8 in short at each free edge)', 0, INK, 11))
    a(_dim(X(0) + 26, Z(ZT), X(0) + 26, Z(ZB), f'{fr(H)} in', 0, INK, 11))
    RX = X(0) + 66
    a(_call(X(18), Z(ZT) + 1, RX, Z(ZT) + 8, 'top: under the ceiling trim strip', 'start', INK, 11.5))
    a(_call(X(hx) + 9, Z(hz), RX, Z(hz) + 4, f'head: {fr(hx)} in along, {hz} up', 'start', BLU, 11.5)); a(_t(RX + 8, Z(hz) + 18, 'hole saw in the sheet, sealed behind', 10.5, 'start', '#5F5E5A'))
    a(_call(X(nx0), Z(48), RX, Z(48), 'nook: cut out of the sheet', 'start', FURR, 11.5)); a(_t(RX + 8, Z(48) + 14, 'and lined (its cut-out is the back;', 10.5, 'start', '#5F5E5A')); a(_t(RX + 8, Z(48) + 27, 'floor, ceiling and sides from the offcuts)', 10.5, 'start', '#5F5E5A'))
    a(_call(X(0), Z(30), RX, Z(30), 'rear end: end trim', 'start', INK, 11.5))
    a(_call(X(0), Z(PANTOP + GAP / 2), RX, Z(PANTOP + GAP / 2) - 20, f'{fr(GAP)} in sealant gap above the pan', 'start', '#2E5B49', 11.5))
    LX = X(PW) - 14
    a(_call(X(DOOR[1]), Z(DOOR[3]) + 2, LX, Z(DOOR[3]) - 34, f'valve door {fr(DW)} x {fr(DH)} in', 'end', BLU, 11.5)); a(_t(LX - 8, Z(DOOR[3]) - 20, f'over an opening {fr(OPEN[1] - OPEN[0])} x {fr(OPEN[3] - OPEN[2])}', 10.5, 'end', '#5F5E5A')); a(_t(LX - 8, Z(DOOR[3]) - 7, f'({fr(OPEN[0])} to {fr(OPEN[1])} along, {fr(OPEN[2])} to {fr(OPEN[3])} up)', 10.5, 'end', '#5F5E5A'))
    a(_call(X(DOOR[1]), Z(dzc), LX, Z(dzc) + 6, 'hinge (thick line) on the cab side,', 'end', INK, 11.5)); a(_t(LX - 8, Z(dzc) + 20, '4 stainless screws at the corners', 10.5, 'end', '#5F5E5A'))
    a(_call(X(vx) - 10, Z(vz), LX, Z(vz) + 40, f'valve: {fr(vx)} in along, {vz} up, on the door', 'end', BLU, 11.5))
    a(_call(X(CJ[0]), Z(46), LX, Z(52), 'dotted: S4, S5, V2 and the two door jambs', 'end', FURR, 11)); a(_t(LX - 8, Z(52) + 13, 'behind the sheet', 10.5, 'end', '#5F5E5A'))
    a(_call(X(PW), Z(20), LX, Z(20), 'cab end: end trim, then the wall W5', 'end', INK, 11.5)); a(_t(LX - 8, Z(20) + 14, '(the sheet stops 1/16 in short of it)', 10.5, 'end', '#5F5E5A'))
    return _svg(820, 680, ''.join(o), 'The PVC sheet and the valve door on the shower wall')

# ---- E  the cutting plan ------------------------------------------------------------------------------------------------------------
def fig_cut():
    S = 3.4; OX = 30; OY = 70
    o = []; a = o.append
    a(_t(20, 24, 'E  Cutting the sheet: one 4 x 8 ft sheet, to scale', 14, 'start', INK, 700))
    nx0, nx1, nz0, nz1 = NOOK
    ww = PW - 2 * RE                                                  # the wall piece's width, 1/8 in short at each free edge
    a(_r(OX, OY, S * 48, S * 96, '#F4F4F0', INK, 1.2)); a(_t(OX + S * 24, OY - 8, 'the sheet, 48 x 96 in', 11.5, 'middle', INK, 700))
    a(_r(OX, OY, S * ww, S * H, '#BFE5DF', TEALD, 1.3))
    a(_t(OX + S * ww / 2, OY + S * 8, 'wall piece', 11, 'middle', TEALD, 700)); a(_t(OX + S * ww / 2, OY + S * 8 + 12, f'{fr(ww)} x {fr(H)}', 10, 'middle', TEALD, 600))
    a(_r(OX + S * (nx0 - RE), OY + S * (ZT - nz1), S * (nx1 - nx0), S * (nz1 - nz0), '#9AD3CB', TEALD, 1.1, 'stroke-dasharray="4 3"'))
    a(_t(OX + S * (nx0 - RE + (nx1 - nx0) / 2), OY + S * (ZT - (nz0 + nz1) / 2) - 2, 'nook', 9.5, 'middle', TEALD)); a(_t(OX + S * (nx0 - RE + (nx1 - nx0) / 2), OY + S * (ZT - (nz0 + nz1) / 2) + 9, 'back', 9.5, 'middle', TEALD))
    a(_r(OX + S * (OPEN[0] - RE), OY + S * (ZT - OPEN[3]), S * (OPEN[1] - OPEN[0]), S * (OPEN[3] - OPEN[2]), '#fff', BLU, 1.1, 'stroke-dasharray="4 3"'))
    a(_t(OX + S * (OPEN[0] - RE + (OPEN[1] - OPEN[0]) / 2), OY + S * (ZT - (OPEN[2] + OPEN[3]) / 2) + 3, 'waste', 9, 'middle', BLU))
    a(_r(OX + S * ww, OY + S * H, S * (48 - ww), S * (96 - H), '#F4F4F0', INK, 0))
    a(_t(OX + S * ww / 2, OY + S * (H + (96 - H) / 2) - 3, 'spare offcut', 10, 'middle', '#5F5E5A')); a(_t(OX + S * ww / 2, OY + S * (H + (96 - H) / 2) + 9, f'{fr(ww)} x {fr(96 - H)}', 10, 'middle', '#5F5E5A'))
    sx = OX + S * (ww + 1)                                            # the strip beside the wall piece (12 1/4 wide): the small pieces
    y2 = 1
    for k in range(2): a(_r(sx + k * S * 4.75, OY + S * y2, S * 4.5, S * (nz1 - nz0), '#D5EEE9', TEALD, 1)); a(_t(sx + k * S * 4.75 + S * 2.25, OY + S * (y2 + (nz1 - nz0) / 2) + 3, '1', 11, 'middle', TEALD, 700))
    y3 = y2 + (nz1 - nz0) + 1.5
    for k in range(2): a(_r(sx + k * S * 4.75, OY + S * y3, S * 4.5, S * SN_LEN, '#D5EEE9', TEALD, 1)); a(_t(sx + k * S * 4.75 + S * 2.25, OY + S * (y3 + SN_LEN / 2) + 3, '2', 11, 'middle', TEALD, 700))
    a(_t(30, OY + S * 96 + 22, f'1  the nook\'s two sides (2 of {fr(nz1 - nz0)} x 4 1/2);  2  its floor and ceiling (2 of {fr(SN_LEN)} x 4 1/2)', 10.5, 'start', TEALD))
    X0 = 430
    for k, t in enumerate([f'Cut the wall piece {fr(ww)} x {fr(H)} in: it stops 1/4 in', 'above the pan, 1/8 in under the trim strip at the', 'ceiling and 1/8 in short of the end trim at each side.', 'Cut it square: the sheet face up on a sheet of foam', 'board, a straightedge and a fine-blade jigsaw (or a', 'utility knife, scored several times and snapped, if', 'the sheet is thin).']):
        a(_t(X0, 100 + 16 * k, t, 12, 'start', INK))
    for k, t in enumerate(['The nook and the valve opening are cut out of the', 'wall piece (drawing G). The nook cut-out is the back', 'of the nook; the opening\'s cut-out is waste.', 'The nook\'s floor, ceiling and two sides come out of', f'the {fr(48 - ww)} in strip beside the wall piece (no joints,', 'no planks to match).']):
        a(_t(X0, 236 + 16 * k, t, 12, 'start', INK))
    a(_t(X0, 372, 'Let the sheet sit in the van for 24 hours first (PVC', 12, 'start', INK)); a(_t(X0, 388, 'moves with heat), and never use a twist drill: a hole', 12, 'start', INK)); a(_t(X0, 404, 'saw for round holes, a jigsaw for the corners.', 12, 'start', INK))
    return _svg(840, 470, ''.join(o), 'Cutting plan for the PVC sheet')

# ---- F  the valve door in section, and the end trim ---------------------------------------------------------------------------------
def fig_corner():
    S = 80.0; OX = 40; OY = 100
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    o = []; a = o.append
    a(_t(20, 24, 'F  The valve door in section (from above, nearly to scale), and the end trim', 14, 'start', INK, 700))
    # --- upper: a section through the door at the valve's height; the wall at the top, the stall below it; the cab side (and the hinge) on the right
    s = 34.0; ox = 24; oy = 185
    DX = lambda x: ox + s * (x - 23.5); DY = lambda y: oy + s * y          # y = 0 is the plywood's front face, where the sheet starts; behind the wall is up
    GP = .1875                                                              # the gasket, drawn at its full 3/16 in (it squeezes to 1/8)
    fy0, fy1 = -.375 - .75, -.375                                           # the frame behind the plywood: 3/4 in thick
    d0 = LT + GP; d1 = d0 + DOORT                                           # the door board's back and front faces
    a(_t(ox, 52, 'Section through the door (the wall at the top, the stall below, the cab side to the right)', 12.5, 'start', INK, 700))
    for (fx0, fx1, nm) in ((SN_X1 - 0.0, SN_X1 + 1.5, 'rear jamb'), (VD_X1, VD_X1 + 1.5, 'cab-side jamb')):
        a(_r(DX(fx0), DY(fy0), s * (fx1 - fx0), s * (fy1 - fy0), '#E0C99A', FURR, 1.2))
    for (px0, px1) in ((23.5, VD_X0), (VD_X1, 36.5)):
        a(_r(DX(px0), DY(-.375), s * (px1 - px0), s * .375, PLY, INK, 1.1))                                    # the plywood, cut at the opening
        a(_r(DX(px0), DY(0), s * (px1 - px0), s * LT, TEAL, TEALD, 1))                                          # the sheet
    for (gx0, gx1) in ((DOOR[0], VD_X0), (VD_X1, DOOR[1])): a(_r(DX(gx0), DY(LT), s * (gx1 - gx0), s * GP, '#9A9A96', INK, .8))   # the gasket
    a(_r(DX(DOOR[0]), DY(d0), s * DW, s * DOORT, '#E7D9B8', INK, 1.3))                                         # the door board
    a(_r(DX(VD_X1 + .02), DY(LT + .015), s * .54, s * .035, '#B9BCC2', INK, .6))                               # the wall leaf of the hinge, on the sheet
    a(_r(DX(DOOR[1] - .55), DY(d0 - .045), s * .55, s * .035, '#B9BCC2', INK, .6))                             # the door leaf, on the door's back
    a(f'<circle cx="{DX(DOOR[1] + .07):.1f}" cy="{DY(LT + GP / 2):.1f}" r="{s * .075:.1f}" fill="#8E9299" stroke="{INK}" stroke-width="1"/>')           # the hinge barrel
    # the valve through the door
    vx = VALVE_X
    a(_r(DX(vx - 1), DY(-2.4), s * 2, s * (d1 + 2.4), '#B9BCC2', INK, 1.1))                                      # the cartridge and body, through the hole
    a(_r(DX(vx - 1.125), DY(d0), s * .125, s * DOORT, '#fff', '#fff', .1)); a(_r(DX(vx + 1.0), DY(d0), s * .125, s * DOORT, '#fff', '#fff', .1))
    a(_r(DX(vx - 2.25), DY(d1), s * 4.5, s * .3, '#D8D8D4', INK, 1.3))                                           # the valve's plate on the door's front
    a(_l(DX(vx - 1.6), DY(-2.4), DX(vx + 1.6), DY(-2.4), INK, 1, '3 2'))
    # four screws: the rear pair into the rear jamb, the cab pair into the cab-side jamb (seen from the side; in the corner of the door)
    for sxp in (DOOR[0] + .25, DOOR[1] - .25):
        a(_r(DX(sxp - .08), DY(d1), s * .16, s * .09, '#E0E3E6', INK, 1)); a(_l(DX(sxp), DY(d1 + .09), DX(sxp), DY(d1 - 2.0), INK, 1.6))
    # callouts
    RX = ox + s * (36.5 - 23.5) + 16
    a(_call(DX(34.2), DY(-.75), RX, DY(-2.1), 'cab-side jamb, 3/4 x 1 1/2 in', 'start', FURR, 11.5)); a(_t(RX + 8, DY(-2.1) + 15, '(S4 and S5 are above and below)', 10.5, 'start', '#5F5E5A'))
    a(_call(DX(24.75), DY(-.75), ox + 4, DY(-2.3), 'rear jamb, 3/4 x 1 1/2 in', 'start', FURR, 11.5))
    a(_call(DX(36.2), DY(-.19), RX, DY(-1.0), 'plywood 3/8 in', 'start', '#5F5E5A', 11.5))
    a(_call(DX(36.2), DY(LT / 2), RX, DY(-.35), f'PVC sheet {fr(LT)} in', 'start', TEALD, 11.5))
    a(_call(DX(34.1), DY(LT + GP * .5), RX, DY(.45), 'mini piano hinge (6 in), between', 'start', INK, 11.5)); a(_t(RX + 8, DY(.45) + 15, 'the door and the sheet, cab side', 10.5, 'start', '#5F5E5A'))
    a(_call(DX(33.75), DY(d1 - 1.0), RX, DY(1.45), 'stainless screw #8 x 2 in,', 'start', INK, 11.5)); a(_t(RX + 8, DY(1.45) + 15, 'into the jamb (4 in all)', 10.5, 'start', '#5F5E5A'))
    a(_call(DX(34.0), DY(d1 - DOORT / 2), RX, DY(2.45), 'door, 1/2 in rigid board', 'start', '#6B5A2E', 11.5))
    a(_call(DX(25.25), DY(LT + GP / 2), ox + 4, DY(2.2), '3/16 in foam gasket (1/8 squeezed)', 'start', '#5F5E5A', 11.5))
    a(_call(DX(VALVE_X + 1.0), DY(-1.8), DX(VALVE_X) + 30, DY(-2.55), 'valve body behind the door', 'start', BLU, 11.5))
    a(_t(ox, DY(3.4), 'The gasket and the hinge are drawn a little larger than scale. Epoxy and seal the cut edges of the plywood and of the sheet at the opening.', 10.5, 'start', RED, 600))
    # --- lower: a free edge (the rear end or the cab end) with its end trim
    a(_t(X(0), Y(3.55), 'A free edge: the end trim (rear end and cab end)', 12.5, 'start', INK, 700))
    y0 = 4.6
    a(_r(X(0), Y(y0 - .375), S * 6.2, S * .375, PLY, INK, 1.1)); a(_r(X(0), Y(y0), S * 4.6, S * .06, AMB, '#8A6A00', .6))
    a(_r(X(0), Y(y0 + .06), S * 4.45, S * LT, '#BFE5DF', TEALD, 1.3)); a(_t(X(2.2), Y(y0 + .06 + LT) + 14, 'sheet', 11, 'middle', TEALD))
    a(_p([(X(4.2), Y(y0 + .06 + LT + .25)), (X(4.75), Y(y0 + .06 + LT + .25)), (X(4.75), Y(y0 - .08)), (X(4.2), Y(y0 - .08)), (X(4.2), Y(y0 + .06 - .03)), (X(4.6), Y(y0 + .06 - .03)), (X(4.6), Y(y0 + .06 + LT + .15)), (X(4.2), Y(y0 + .06 + LT + .15))], '#E7D9B8', INK, 1.3))   # the J-shaped trim
    a(_p([(X(4.45), Y(y0 + .06)), (X(4.6), Y(y0 + .06)), (X(4.6), Y(y0 + .06 + LT)), (X(4.45), Y(y0 + .06 + LT))], SEAL, '#2E5B49', .8))            # the sealant in the 1/8 in gap
    a(_call(X(4.45), Y(y0 + .06 + LT / 2), X(5.0), Y(y0 + 1.5), '1/8 in gap, filled with', 'start', '#2E5B49', 11.5)); a(_t(X(5.0) + 8, Y(y0 + 1.5) + 14, 'flexible sealant', 11, 'start', '#2E5B49'))
    a(_call(X(4.7), Y(y0 - .02), X(5.0), Y(y0 + 2.4), 'J-shaped end trim, glued to the', 'start', INK, 11.5)); a(_t(X(5.0) + 8, Y(y0 + 2.4) + 14, 'plywood, over the sheet\'s edge', 11, 'start', INK))
    return _svg(760, 700, ''.join(o), 'The valve door in section and the end trim')

# ---- G  cutting the nook and the valve opening out of the wall piece ------------------------------------------------------------------
def fig_nook():
    S = 5.0; OX = 70; OY = 112
    nx0, nx1, nz0, nz1 = NOOK
    ww = PW - 2 * RE                                         # the wall piece, as cut in drawing E
    ny0 = ZT - nz1; nh = nz1 - nz0                           # the nook from the wall piece's top end, and its height
    ox0, ox1, oy0, oy1 = OPEN[0] - RE, OPEN[1] - RE, ZT - OPEN[3], ZT - OPEN[2]      # the valve opening, from the piece's rear edge and top end
    mx0, mx1 = nx0 - RE, nx1 - RE
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    o = []; a = o.append
    a(_t(20, 24, 'G  Cutting the nook and the valve opening out of the wall piece (flat on the bench, face up, rear edge on the left)', 14, 'start', INK, 700))
    a(_r(X(0), Y(0), S * ww, S * H, '#BFE5DF', TEALD, 1.6)); a(_t(X(ww / 2), Y(H) + 18, f'the wall piece, {fr(ww)} x {fr(H)} in', 11.5, 'middle', TEALD, 700))
    a(_t(X(ww / 2), Y(0) + 15, 'top end', 11, 'middle', '#5F5E5A', 600))
    a(_r(X(mx0), Y(ny0), S * (mx1 - mx0), S * nh, '#fff', RED, 2)); a(_r(X(ox0), Y(oy0), S * (ox1 - ox0), S * (oy1 - oy0), '#fff', RED, 2))
    a(_t(X((mx0 + mx1) / 2), Y(ny0 + nh / 2) - 6, 'cut-out:', 11.5, 'middle', INK, 700)); a(_t(X((mx0 + mx1) / 2), Y(ny0 + nh / 2) + 9, 'save it (the', 11, 'middle', INK)); a(_t(X((mx0 + mx1) / 2), Y(ny0 + nh / 2) + 22, 'nook back)', 11, 'middle', INK))
    a(_t(X((ox0 + ox1) / 2), Y((oy0 + oy1) / 2) + 4, 'waste', 11, 'middle', INK))
    for (cx, cy) in ((mx0, ny0), (mx1, ny0 + nh), (ox0, oy0), (ox1, oy1)): a(f'<circle cx="{X(cx):.1f}" cy="{Y(cy):.1f}" r="4" fill="{RED}"/>')
    # dimensions: along the top from the rear edge, down the sides from the top end
    yt = Y(0) - 12
    a(_dim(X(0), yt, X(mx0), yt, f'{fr(mx0)}', 0, INK, 10.5)); a(_dim(X(mx0), yt, X(mx1), yt, f'{fr(mx1 - mx0)}', 0, INK, 10.5)); a(_dim(X(ox0), yt, X(ox1), yt, f'{fr(ox1 - ox0)}', 0, INK, 10.5))
    a(_dim(X(0), yt - 20, X(ox0), yt - 20, f'{fr(ox0)}', 0, INK, 10.5))
    xl = X(0) - 20; xl2 = X(0) - 52
    a(_arrow(xl, Y(ny0 / 2), xl, Y(0), INK, 1)); a(_arrow(xl, Y(ny0 / 2), xl, Y(ny0), INK, 1)); a(_t(xl - 6, Y(ny0 / 2) + 4, f'{fr(ny0)}', 10.5, 'end', INK, 600))
    a(_arrow(xl2, Y(ny0 + nh / 2), xl2, Y(ny0), INK, 1)); a(_arrow(xl2, Y(ny0 + nh / 2), xl2, Y(ny0 + nh), INK, 1)); a(_t(xl2 - 6, Y(ny0 + nh / 2) + 4, f'{fr(nh)}', 10.5, 'end', INK, 600))
    xr = X(ww) + 16; xr2 = X(ww) + 50
    a(_arrow(xr, Y(oy0 / 2), xr, Y(0), INK, 1)); a(_arrow(xr, Y(oy0 / 2), xr, Y(oy0), INK, 1)); a(_t(xr + 6, Y(oy0 / 2) + 4, f'{fr(oy0)}', 10.5, 'start', INK, 600))
    a(_arrow(xr2, Y((oy0 + oy1) / 2), xr2, Y(oy0), INK, 1)); a(_arrow(xr2, Y((oy0 + oy1) / 2), xr2, Y(oy1), INK, 1)); a(_t(xr2 + 6, Y((oy0 + oy1) / 2) + 4, f'{fr(oy1 - oy0)}', 10.5, 'start', INK, 600))
    X0 = 400
    notes = ['1  Tape over the lines (less chipping) and on the saw\'s', '   base plate (no scratches). Mark both rectangles from the', '   wall piece\'s own rear edge and top end, not from the wall,', f'   and check the sizes: the nook {fr(nx1 - nx0)} x {fr(nh)}, the opening {fr(OPEN[1] - OPEN[0])} x {fr(OPEN[3] - OPEN[2])}.', '',
             '2  The sheet is solid, so a jigsaw needs a way in: drill a 3/8 in', '   hole inside the waste at two opposite corners of each', '   rectangle (the red dots), put the blade in and cut from', '   hole to hole along the lines, slowly, on foam board.', '',
             '3  Take the corners with a small file, rounded about 1/8 in', '   radius, not sharp (a sharp inside corner starts a crack).', '',
             f'4  Keep the nook\'s cut-out: it is the back of the nook. The', f'   opening\'s cut-out is waste. The opening is cut in the plywood', f'   on the wall too (same size, {fr(OPEN[0])} to {fr(OPEN[1])} along and {fr(OPEN[2])} to {fr(OPEN[3])} up),', '   before the sheet goes on, with the edges sealed in epoxy.']
    for k, t in enumerate(notes): a(_t(X0, 130 + 16 * k, t, 12, 'start', INK))
    return _svg(840, 640, ''.join(o), 'Cutting the nook and the valve opening out of the wall piece')

# ---- H  cutting the head hole and the valve hole ----------------------------------------------------------------------------------------
def fig_holes():
    S = 5.0; OX = 80; OY = 112
    ww = PW - 2 * RE; PH = H
    X = lambda x: OX + S * x; Y = lambda y: OY + S * y
    hx, hy = HEAD[0] - RE, ZT - HEAD[1]                                                       # from the piece's rear edge and top end
    nx0, nw, ny0, nh = NOOK[0] - RE, NOOK[1] - NOOK[0], ZT - NOOK[3], NOOK[3] - NOOK[2]
    o = []; a = o.append
    a(_t(20, 24, 'H  The head hole (in the sheet) and the valve hole (in the door): where to mark them', 14, 'start', INK, 700))
    a(_r(X(0), Y(0), S * ww, S * PH, '#BFE5DF', TEALD, 1.6)); a(_t(X(ww / 2), Y(PH) + 18, 'the wall piece, face up (rear edge on the left)', 11.5, 'middle', TEALD, 700))
    a(_r(X(nx0), Y(ny0), S * nw, S * nh, 'none', '#9AA0A8', 1.2, 'stroke-dasharray="4 3"')); a(_t(X(nx0 + nw / 2), Y(ny0 + nh / 2) + 4, 'nook (cut-out)', 10.5, 'middle', '#7A7F86'))
    a(_r(X(OPEN[0] - RE), Y(ZT - OPEN[3]), S * (OPEN[1] - OPEN[0]), S * (OPEN[3] - OPEN[2]), 'none', '#9AA0A8', 1.2, 'stroke-dasharray="4 3"')); a(_t(X(OPEN[0] - RE + (OPEN[1] - OPEN[0]) / 2), Y(ZT - (OPEN[2] + OPEN[3]) / 2) + 4, 'opening', 10.5, 'middle', '#7A7F86'))
    a(f'<circle cx="{X(hx):.1f}" cy="{Y(hy):.1f}" r="8" fill="#fff" stroke="{BLU}" stroke-width="2"/>' + _l(X(hx) - 12, Y(hy), X(hx) + 12, Y(hy), BLU, 1) + _l(X(hx), Y(hy) - 12, X(hx), Y(hy) + 12, BLU, 1))
    a(_t(X(hx) - 14, Y(hy) + 4, f'head hole {fr(HEADHOLE)}', 11, 'end', BLU, 700)); a(_t(X(hx) - 14, Y(hy) + 18, '(circle drawn bigger than scale)', 10, 'end', '#5F5E5A'))
    yt = Y(0) - 10
    a(_dim(X(0), yt, X(hx), yt, f'{fr(hx)}', 0, INK, 10.5))
    xl = X(0) - 16
    a(_arrow(xl, Y(hy / 2), xl, Y(0), INK, 1)); a(_arrow(xl, Y(hy / 2), xl, Y(hy), INK, 1)); a(_t(xl - 6, Y(hy / 2) + 4, f'{fr(hy)}', 10.5, 'end', INK, 600))
    a(_l(xl, Y(hy), X(hx), Y(hy), '#B4B2A9', .8, '3 3'))
    # the door board, with the valve hole (rear edge on the left, the hinge on the right)
    d0 = (440, 410); Sd = 12
    DX = lambda x: d0[0] + Sd * x; DY = lambda y: d0[1] + Sd * y
    vx_, vy_ = VALVE_X - DOOR[0], DOOR[3] - VALVE_Z                                           # from the door's rear edge and top edge
    a(_t(d0[0] - 30, d0[1] - 38, f'The door board, {fr(DW)} x {fr(DH)} in', 12.5, 'start', INK, 700)); a(_t(d0[0] - 30, d0[1] - 24, '(rear edge on the left)', 10.5, 'start', '#5F5E5A'))
    a(_r(DX(0), DY(0), Sd * DW, Sd * DH, '#E7D9B8', INK, 1.4))
    a(_r(DX(vx_ - 2.25), DY(vy_ - 2.25), Sd * 4.5, Sd * 4.5, 'none', '#7A7F86', 1, 'stroke-dasharray="3 2"'))
    a(f'<circle cx="{DX(vx_):.1f}" cy="{DY(vy_):.1f}" r="{Sd * VALVEHOLE / 2:.1f}" fill="#fff" stroke="{BLU}" stroke-width="2"/>')
    a(_l(DX(DW), DY(DH / 2 - HINGE_LEN / 2), DX(DW), DY(DH / 2 + HINGE_LEN / 2), INK, 4)); a(_t(DX(DW) + 8, DY(DH / 2) + 4, 'hinge', 11, 'start', INK, 600))
    for sx in (.25, DW - .25):
        for sy in (.25, DH - .25): a(f'<circle cx="{DX(sx):.1f}" cy="{DY(sy):.1f}" r="3" fill="#E0E3E6" stroke="{INK}" stroke-width="1"/>')
    a(_dim(DX(0), DY(0) - 8, DX(vx_), DY(0) - 8, f'{fr(vx_)}', 0, INK, 10.5)); xd = DX(0) - 14
    a(_arrow(xd, DY(vy_ / 2), xd, DY(0), INK, 1)); a(_arrow(xd, DY(vy_ / 2), xd, DY(vy_), INK, 1)); a(_t(xd - 5, DY(vy_ / 2) + 4, f'{fr(vy_)}', 10.5, 'end', INK, 600))
    a(_t(DX(vx_), DY(vy_ + 2.25) + 17, f'valve hole {fr(VALVEHOLE)}, plate 4 1/2', 11, 'middle', BLU, 700))
    a(_t(DX(DW / 2), DY(DH) + 34, 'the four screw holes are drilled with the door in place', 10.5, 'middle', '#5F5E5A'))
    # the section through the head hole: the wall on the left, the stall on the right
    T0 = 520; CY = 230; Sc = 60
    a(_t(T0 - 90, 64, 'The head hole in section (the wall on the left)', 12.5, 'start', INK, 700))
    ply = Sc * .375; frp = Sc * LT; ph = Sc * .875; hh = Sc * 1.125; fh = Sc * 2.5; ft = Sc * .35
    a(_r(T0 - ply, CY - 100, ply, 200, PLY, INK, 1.1)); a(_r(T0 - ply - 1, CY - Sc * .65, ply + 2, Sc * 1.3, '#fff', '#fff', .1))           # the plywood, with its hole
    a(_r(T0, CY - 100, frp, 200, TEAL, TEALD, .8)); a(_r(T0 - 1, CY - hh / 2, frp + 2, hh, '#fff', '#fff', .1))                           # the sheet, with its hole
    a(_r(T0 - 100, CY - ph / 2, 330, ph, '#B9BCC2', INK, 1.2))                                                                              # the shower arm
    a(_r(T0 + frp, CY - fh / 2, ft, fh, '#D8D8D4', INK, 1.4)); a(_r(T0 + frp, CY - ph / 2, ft, ph, '#B9BCC2', INK, 1.2))                      # the flange
    for yy in (CY - fh / 2 + 4, CY + fh / 2 - 12): a(_r(T0 + frp - 3, yy, 5, 9, SEAL, '#2E5B49', 1))                                       # the sealant ring on its back
    RX = T0 + 90
    a(_call(T0 + frp / 2, CY - 80, RX, CY - 130, f'PVC sheet ({fr(LT)} in)', 'start', TEALD, 11.5))
    a(_call(T0 + frp + ft / 2, CY - fh / 2 + 4, RX, CY - 108, 'flange hides the hole', 'start', INK, 11.5))
    a(_call(T0 + frp - 1, CY - fh / 2 + 8, RX, CY - 86, 'sealant ring behind it', 'start', '#2E5B49', 11.5))
    a(_arrow(T0 + 70, CY, T0 + 70, CY - fh / 2, INK, 1)); a(_arrow(T0 + 70, CY, T0 + 70, CY + fh / 2, INK, 1)); a(_t(T0 + 80, CY + 50, '2 1/2 in flange', 10.5, 'start', INK, 600)); a(_t(RX, CY + 66, 'the flange overlaps the hole', 10.5, 'start', '#5F5E5A')); a(_t(RX, CY + 79, 'by at least 1/2 in all round', 10.5, 'start', '#5F5E5A'))
    a(_t(T0 + 150, CY - ph / 2 - 8, 'shower arm', 11, 'start', INK, 600))
    LX = T0 - 60
    a(_call(T0 - ply / 2, CY - 80, LX, CY - 110, 'plywood 3/8', 'end', '#5F5E5A', 11.5))
    a(_call(T0 + frp / 2, CY + hh / 2 - 4, LX, CY + 95, 'hole 1/4 in bigger than the pipe:', 'end', RED, 11.5)); a(_t(LX - 8, CY + 109, '1/8 in clear all round', 11, 'end', RED))
    a(_t(T0 + 30, 96, 'the stall side', 10.5, 'start', '#5F5E5A', 600)); a(_t(T0 - 40, 96, 'behind', 10.5, 'end', '#5F5E5A', 600))
    a(_t(20, 625, 'Check the real pipe and valve before you cut: the stubs can sit a little off the plan\'s numbers.', 11.5, 'start', RED, 600))
    return _svg(760, 645, ''.join(o), 'Cutting the head hole and the valve hole')

# ---- I  sealing around the valve ------------------------------------------------------------------------------------------------------
def fig_valve():
    S = 34; CX, CY = 190, 215
    o = []; a = o.append
    a(_t(20, 24, 'I  Sealing around the valve (on the door; the head\'s flange in the sheet is done the same way)', 14, 'start', INK, 700))
    a(_t(20, 54, 'From the front', 12.5, 'start', INK, 700))
    a(_r(40, 70, 300, 290, '#E7D9B8', INK, 1.4)); a(_t(190, 358, 'the door board', 11, 'middle', '#6B5A2E', 600))
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
    a(_call(CX + S * 1.45, CY, LX, 270, '2  the plate\'s own screws go into the valve,', 'start', INK, 11.5)); a(_t(LX + 8, 288, 'never into the door board alone', 11, 'start', INK))
    a(_call(CX, CY, LX, 340, 'the handle and cartridge: the valve\'s own seals', 'start', '#5F5E5A', 11.5))
    # the section: the door on the left, the stall on the right
    T0 = 250; Sc = 40; CYs = 590
    a(_t(20, 410, 'In section (the wall on the left)', 12.5, 'start', INK, 700))
    ply = Sc * DOORT; ph = Sc * .3; plate = Sc * 4; hole = Sc * 2.25; cart = Sc * 2
    a(_r(T0 - ply, CYs - 130, ply, 260, '#E7D9B8', INK, 1.1)); a(_r(T0 - ply - 1, CYs - hole / 2, ply + 2, hole, '#fff', '#fff', .1))
    a(_r(T0 - 130, CYs - cart / 2, 190, cart, '#B9BCC2', INK, 1.2))                                                                                    # the valve's cartridge through the hole
    a(_r(T0, CYs - plate / 2, ph, plate, '#D8D8D4', INK, 1.4))                                                                                           # the plate
    for yy in (CYs - plate / 2 + 12, CYs + plate / 2 - 21): a(_r(T0 - 3, yy, 5, 9, SEAL, '#2E5B49', 1))                                                    # the ring behind it
    for sy in (-1, 1): a(_p([(T0 + ph, CYs + sy * plate / 2), (T0 + ph + 13, CYs + sy * plate / 2), (T0 + ph, CYs + sy * (plate / 2 + 13))], SEAL, '#2E5B49', 1))   # the tooled outer bead
    for sy in (-1, 1): a(_r(T0, CYs + sy * (plate / 2 + 18) - 3, 3, 6, '#6CA6D9', '#3E7FBF', .8))                                                       # the tape
    RX = 420
    a(_call(T0 + ph + 8, CYs - plate / 2 + 1, RX, CYs - 130, '3  tooled bead', 'start', '#2E5B49', 11.5))
    a(_call(T0 + ph / 2, CYs - plate / 2 + 6, RX, CYs - 102, '2  plate pressed on the ring', 'start', INK, 11.5))
    a(_call(T0 - 1, CYs - plate / 2 + 16, RX, CYs - 74, '1  ring of sealant behind the plate', 'start', '#2E5B49', 11.5))
    a(_call(T0, CYs - plate / 2 - 18, RX, CYs - 164, 'painter\'s tape, pulled off before it skins', 'start', '#3E7FBF', 11.5))
    a(_t(RX, CYs + 90, 'The plate overlaps the hole', 11, 'start', '#5F5E5A')); a(_t(RX, CYs + 104, 'by at least 1/2 in all round.', 11, 'start', '#5F5E5A'))
    a(_t(T0 - 130, CYs + 150, 'valve cartridge through the hole', 11, 'start', INK))
    a(_t(20, 770, 'Do the head\'s flange the same way. Wait a day before any water.', 11.5, 'start', RED, 600))
    return _svg(760, 790, ''.join(o), 'Sealing around the valve')

FIGS = [
    ('A', 'The pan from above', fig_top, 'The bought pan sits against the plywood wall. The back wall is lined with one PVC paneling sheet; the cab end is the 3/4 in wall W5 and the other two sides have no wall, only two curtains on a rail on the ceiling that runs round the rear end and along the front, 1 1/2 in inside the pan\'s edge. The nook is centered on the pan. The drain hole is at the middle of the rear-door end, 5 in from the rear end (you said) and 12 out (the middle of the depth: check it on the pan). The floor falls to it.'),
    ('B', 'The pan edge and the sealed gap', fig_edge, 'A stiff sheet cannot lap over the pan lip, so it stops 1/4 in above the pan edge and the gap is filled with flexible sealant: the water runs down the sheet, over the sealant and into the pan. The plywood edge below it is sealed and hidden behind the lip.'),
    ('C', 'The drain through the floor', fig_drain, 'The flange is bedded in neutral silicone on the pan, the body goes through the subfloor and the steel, a gasket and a lock nut hold it from below, and the bare steel edge of the hole is primed against rust. A P-trap and a hose take it to the grey tank, which must be vented (its place is not set).'),
    ('D', 'The sheet and the valve door on the wall', fig_wall, 'One 4 x 8 ft sheet stood on end, with no joints, covers the 36 in back wall; the nook is cut out of it and lined. The shower valve, on the cab side of the nook (the left of it in the passenger-wall view, around 30 in along the wall), is mounted on a small hinged door: the opening is 8 x 9 3/4 in, between furring rails S4 and S5, starting 1 1/2 in past the nook so that the nook frame V2 (with a short piece under it) is its rear jamb; the door is 9 x 10 3/4 in, overlaps the opening 1/2 in all round, is held shut by four stainless screws and hangs on a hinge on the cab side. The head is a hole in the sheet. The two ends have end trim; the cab end meets the wall W5 and the rear end the rear doors, so there is no corner to line.'),
    ('E', 'Cutting the sheet', fig_cut, 'The wall piece (35 3/4 x 69 15/16 in) comes out of one corner of the sheet; the nook\'s cut-out is its back, and the strip beside it (12 1/4 in wide) gives the nook\'s floor, ceiling and two sides.'),
    ('F', 'The valve door in section, and the end trim', fig_corner, 'The door is a 1/2 in rigid board that lies on a 3/16 in foam gasket round the opening (it squeezes to 1/8 in). A 6 in piece of mini piano hinge sits between the door and the sheet on the cab side, its wall leaf screwed through the sheet and the plywood into the cab-side jamb. Four #8 x 2 in stainless screws at the corners go through the door, the gasket, the sheet and the plywood into the wood behind (the rear jamb, the cab-side jamb, S4 and S5). Each free edge of the sheet (the rear end and the cab end) stops 1/8 in short of its J-shaped trim, and the gap is filled with flexible sealant.'),
    ('G', 'Cutting the nook and the opening out of the wall piece', fig_nook, 'Cut them flat on the bench before the sheet goes on the wall: mark both rectangles from the piece\'s own rear edge and top end, drill a 3/8 in hole at two opposite corners inside the waste of each, and cut from hole to hole with a jigsaw and a fine blade. The nook\'s cut-out is its back; the opening\'s is waste.'),
    ('H', 'The head hole and the valve hole', fig_holes, 'The head hole is marked on the sheet (28 7/8 in along from its rear edge and 4 down from its top end); the valve hole is marked on the door board (4 in from its rear edge and 6 1/4 down from its top edge, with the 4 1/2 in plate around it). Check each against the real pipe and valve, cut it with a hole saw 1/4 in bigger than the part that goes through, and hide it under the flange or trim plate with a ring of flexible sealant behind it.'),
    ('I', 'Sealing around the valve', fig_valve, 'Three layers: a closed ring of sealant on the back of the plate (1), the plate pressed on it, and a thin tooled bead around the plate\'s edge, laid between painter\'s tape and the plate (3). The valve\'s own seals look after the cartridge.')]

PARTS = [
    ('Shower pan', '36 x 24 in, 3 in curb (bought)', '1', 'measure the drain hole (its distance from the rear end and the wall, its size) and the height of the lip against the wall, and change the plan\'s sizes to match'),
    ('PVC wall paneling sheet', 'one solid sheet, 4 x 8 ft (48 x 96 in), smooth, white or light; the plan assumes 5/16 in (8 mm): measure yours, a 4 x 8 sheet is often thinner', '1', 'stood on end: the wall piece is 35 3/4 x 69 15/16 in; its nook cut-out is the nook\'s back and the 12 1/4 in strip beside it makes the nook\'s floor, ceiling and sides; check the sheet is rigid PVC made for wet walls (not a thin plastic film), and note its weight: 5/16 in solid is heavy (about 2 lb a sq ft), so look at the maker\'s weight before you lift it'),
    ('PVC panel adhesive', 'a construction adhesive the sheet maker approves for PVC (polyurethane or MS polymer: solvent-based adhesives can craze PVC), 10 oz cartridges', 'about 6', 'a solid sheet needs full coverage: ribbons about 4 in apart over the whole back, never within 1 in of an edge or of the opening; follow the cartridge for the open time and the temperature'),
    ('Valve door board', '1/2 in rigid board, 9 x 10 3/4 in: cellular PVC trim board (best), or marine plywood sealed with epoxy on every face and edge and painted', '1', 'the valve, its plate and the hinge go on it; do not use anything that swells when wet'),
    ('Door frame lumber', '1x2 furring (3/4 x 1 1/2 in), the same sticks as the nook frames', '2 pieces', 'VD1 the cab-side jamb, 9 3/4 in, between S4 and S5 at 33 1/2 to 35 in; and VD2 a 6 in piece under the nook frame V2 (24 to 25 1/2 in, 32 to 38 up) as the rear jamb (both are in the furring cut list); fitted with the furring, before the plywood'),
    ('Door gasket', 'closed-cell foam strip, 3/16 in thick x 1/2 in wide, self-adhesive', 'about 4 ft', 'one strip all round the opening on the front of the sheet, under the door\'s 1/2 in overlap'),
    ('Door hinge', 'stainless mini piano hinge, about 1 in wide open, with a barrel of 1/8 in or so, cut to 6 in', '1', 'between the door\'s back edge and the sheet on the cab side; its screws are short (the door leaf: #4 x 3/8 in into the 1/2 in board) and long (the wall leaf: #6 x 1 1/4 in into the cab-side jamb); stainless only'),
    ('Door screws', '#8 x 2 in stainless pan-head screws with finishing washers (the heads show)', '4 and 2 spare', 'one in each corner of the door, 1/4 in from the edges, into S4, S5, the rear jamb and the cab-side jamb; drilled with a pilot and a countersunk washer seat so they pull the door down onto the gasket without cracking the board'),
    ('Shutoff valves', '1/2 in push-to-connect PEX ball valves', '2', 'one on the hot line and one on the cold line in the sink cabinet, so the door can be opened with the water off; and 8 to 12 in of spare PEX behind the door on each line, so the valve can be pulled forward'),
    ('Paneling tools and safety', 'jigsaw with a fine blade, straightedge, utility knife, square, level or plumb line, 3 in hand roller, masking and painter\'s tape, 1/8 in and 1/4 in spacers, caulk gun, hole saws, 3/8 in drill bit, a small file, dust mask and glasses', '1 set', 'cut slowly on foam board, supported all along; PVC chips and dust irritate eyes and lungs'),
    ('J-shaped end trim and top trim', 'PVC J-trim in the sheet color, 8 ft, and the trim strip under the ceiling', '2 and 1', 'the rear end and the cab end of the paneling (69 15/16 in each); the top edge goes under the ceiling trim strip'),
    ('Flexible sealant', 'neutral-cure silicone or MS polymer, mold-resistant, white or clear', '4 tubes', 'drain flange, the pan joint, the pan lip, the cut edges of the opening, the trims, the nook corners, valve and head flanges; never a hard caulk'),
    ('Pan bedding', 'flexible polyurethane or MS-polymer construction adhesive, 28 oz tubes or 10 oz cartridges', 'about 3 cartridges', 'zig-zag beads every 3 in under the pan; not a rigid mortar (the van flexes and the mortar cracks)'),
    ('Shower drain', 'fits the pan\'s drain hole, with a gasket and a lock nut from below; 1 1/2 in tailpiece', '1', 'check whether the pan comes with one'),
    ('P-trap and hose', '1 1/2 in trap (or a waterless trap valve) and 1 1/2 in flexible hose', '1', 'to the grey tank, which needs a vent (the tank\'s place is not set)'),
    ('Hole saws', 'bi-metal or carbide: the drain (body + 1/4 in), the head arm (1 1/8 in) and the valve (2 1/4 in), or 1/4 in bigger than your own parts', '3', 'a hole saw for each, never a twist drill through the sheet'),
    ('Epoxy and rust primer', 'thin epoxy for the plywood edges and cut-outs; rust converter and epoxy primer for the steel edge of the drain hole', '1 each', 'two coats of epoxy on every cut edge of the plywood in the stall, and on the edge of the valve opening'),
]
STEPS = [
    "<b>Measure the pan before anything is cut.</b> Write down its length and depth (36 x 24), the height of its curb and of its lip against the wall, the size of the drain hole and how far it is from the rear end and from the wall (you said the middle of the rear-door end, 5 in from the rear end; the plan has it at 5 in along and 12 out, the middle of the depth, which is my guess), and the thickness of the PVC sheet (5/16 in is a placeholder: a 4 x 8 sheet is often 1/8 in or less). Put the real numbers into the plan's sizes (Shower drain hole, Liner), so the drawings and checks follow.",
    "<b>Look under the floor where the hole goes.</b> Cross-members, wires, brake or fuel lines and the grey tank's place all matter before you drill. The hole at the middle of the rear-door end is near the rear bumper area: check it clears the frame.",
    "<b>Check and prepare the floor.</b> The subfloor under the pan must be flat to 1/8 in over the 36 x 24 in (a 4 ft level or a straightedge). Fill any dip with a flexible leveling filler or shim it; the pan's floor is thin and a fiberglass or acrylic pan must be supported all over, or it cracks where you stand.",
    '<b>Drill the drain hole.</b> Dry-fit the pan, mark the center of its drain hole on the floor, take the pan out, drill a pilot hole through the subfloor and the steel, then cut with a hole saw 1/4 in bigger than the drain body. Deburr the steel edge, treat it with rust converter and epoxy primer, and seal the cut edge of the subfloor with epoxy. Vacuum all the chips out of the van.',
    "<b>Bed the pan.</b> Run zig-zag beads of the flexible adhesive over the subfloor about every 3 in (keep it 2 in back from the hole), bed the drain flange in neutral silicone on the pan, set the pan down against the plywood wall with its rear end at the back mark (the cab end is the wall W5, which stands just past the pan at 36 to 36 3/4 in: put the pan against its face, measuring 36 in from the back mark), and press it. Check it is level side to side and falls to the drain. Weigh it down (jugs of water, 100 lb) for the adhesive's open time and wipe the squeeze-out.",
    '<b>Connect the drain from below:</b> gasket and lock nut on the body, then the tailpiece, the P-trap and the hose to the grey tank, with a vent on the tank. Keep the hose falling all the way to the tank.',
    '<b>Seal the pan to the wall.</b> A bead of flexible sealant where the pan lip meets the plywood, and the plywood edge below the sheet sealed with epoxy (drawing B).',
    '<b>Fill test.</b> Plug the drain, fill the pan to just under the curb, mark the water line and leave it for a day. Check the line has not dropped and look under the floor for any drip. Then open the drain, check it flows freely and leaks nowhere at the nut or the trap.',
    "<b>Fit the frame behind the valve door, and cut the opening in the plywood.</b> (1) Two small pieces of 1x2 furring (VD1 and VD2 in the cut list) go behind the plywood, in the same layer as the furring rails: the cab-side jamb, 9 3/4 in long, upright between S4 and S5 at 33 1/2 to 35 in along (S4's top edge is at 32 up and S5's bottom edge at 41 3/4), and a 6 in piece in line under the nook frame V2, at 24 to 25 1/2 in along and 32 to 38 up, as the rear jamb. Fit them with the furring, before the plywood goes on, each with two 2 in screws driven at an angle into the rail (if the plywood is already on this part of the wall, take its piece off, fit the jambs and put it back). The opening then has wood all round it: S4 below, S5 above, V2 and its extension at the rear, the jamb at the cab side. (2) Mark the opening on the plywood, 8 x 9 3/4 in at 25 1/2 to 33 1/2 in along and 32 to 41 3/4 in up, and cut it out with a jigsaw (drawing G). (3) Two coats of thin epoxy on its four cut edges. The valve door is shown in drawings D and F.",
    "<b>Prepare the plywood before the sheet goes on.</b> (1) Two coats of thin epoxy on every cut edge and on the bare plywood of the nook and of the head's hole: water gets in from the edges. (2) Make the face flat. The screws that hold the plywood have finish washers, and a washer would show through a thin sheet as a bump and stop it sticking: in the stall, countersink each screw (or refit it with a flat head) and fill the dimple with epoxy filler, then sand it flush; sand off raised grain, fill any gouge, and check with a straightedge that nothing stands more than about 1/32 in proud (a solid sheet follows a bump and shows it). (3) Vacuum the dust and wipe the face with a damp cloth: it must be clean, dry and free of oil where the adhesive goes (scuff-sand any epoxy that reached the face). (4) Mark the wall piece's outline on the plywood with a level or a plumb line from the back mark: 1/8 in in from the rear end and from the cab end, 4 1/16 in up (1/4 in over the pan edge) and 74 in up.",
    "<b>Cut the wall piece out of the sheet</b> (drawing E). (1) Let the sheet sit in the van for at least 24 hours first, so it matches its temperature (PVC moves with heat, about 1/16 in over 8 ft for each 15 F). (2) Lay it face up on foam board and cut the wall piece, 35 3/4 x 69 15/16 in, square, from one corner: it stops 1/4 in above the pan edge and 1/8 in under the trim strip at the ceiling, and 1/8 in short of the end trim at each side. (3) Use a straightedge and a jigsaw with a fine blade, or score a thin sheet with a utility knife several times and snap it. (4) Dry-fit it on the wall, and mark which end is the top.",
    "<b>Cut the nook and the valve opening out of the wall piece</b> (drawing G), flat on the bench before gluing. (1) Measure from the piece's own rear edge and top end, not from the wall: the nook starts 11 7/8 in from the rear edge and 20 in down from the top end, and is 12 in wide and 16 in tall; the valve opening starts 25 3/8 in from the rear edge and 32 1/4 in down, and is 8 in wide and 9 3/4 in tall. (2) Put painter's tape over the lines and on the saw's base plate. (3) The sheet is solid: drill a 3/8 in hole at two opposite corners of each rectangle, inside the waste, and cut from hole to hole with a jigsaw and a fine blade, slowly. (4) Save the nook's cut-out: it is the back of the nook. The opening's cut-out is waste. (5) File the cut edges smooth, round the inside corners a little (about 1/8 in), and seal the cut edges that face the nook with a dab of sealant.",
    "<b>Make the valve door</b> (drawing H). (1) Cut the door board to 9 x 10 3/4 in; if it is plywood, seal every face and edge in epoxy and paint it. (2) Mark the valve hole on it, 4 in from the rear edge and 6 1/4 in down from the top edge (the valve is 29 in along and 36 up), and check it against the real valve before you cut: the stubs move a little when they are roughed in, so the part's true position beats the plan. (3) Size the hole from your own part, not from mine: 1/4 in bigger than the part that goes through (a single-handle valve cartridge is about 2 in, so 2 1/4 in), and small enough that the valve's plate overlaps it by at least 1/2 in all round. Check also that the valve's threaded body is long enough to pass through the 1/2 in board and take its nut or plate. (4) Cut it with a hole saw, slowly and face up on foam board, so the board does not melt or crack; never a twist drill. (5) Fix the valve on the door with its own plate and screws, and connect the two swivel elbows to its inlets on the bench. The head's hole in the sheet is made the same way, 28 7/8 in from the wall piece's rear edge and 4 in down from its top end.",
    "<b>Glue the sheet on.</b> (1) Run the flexible adhesive on the plywood in ribbons about 4 in apart over the whole face of the wall piece, never within 1 in of an edge or of the nook and the opening, and only as much as you can cover in the open time on the cartridge (cool or warm, as it says). (2) Set the sheet on 1/4 in spacers on the pan, its rear edge 1/8 in from the end trim line, plumb with a level, and press it flat from the middle outward, then roll the face firmly; the nook and the opening must line up with their holes in the plywood (and with the nook frames V1 and V2). (3) Hold the edges with strips of masking tape for the first hour, keep the van within the temperatures the cartridge allows while it cures, and wipe any squeeze-out at once. (4) Leave the spacers in until the adhesive has set.",
    '<b>Line the nook.</b> Glue the cut-out to the plywood back of the nook as its back, then its floor, its ceiling and its two sides from the offcuts (the floor and the ceiling are 12 x 4 1/2 in, the sides 16 x 4 1/2 in), each in full ribbons of adhesive and each butted to the back, with a bead of sealant in every inside corner. The front edges are left open, with no lip: a bungee cord across the front keeps things in. Use a 4 in roll: the nook is about 4 1/4 in clear inside the lining.',
    '<b>Hang the door.</b> (1) Stick the foam gasket all round the opening on the front of the sheet, 1/4 in outside the cut edge, so that the door\'s 1/2 in overlap lies on it. (2) Screw the 6 in hinge to the door\'s back edge on the cab side (short screws, drilled first) and, with the door held in place on the gasket, screw its wall leaf through the sheet and the plywood into the cab-side jamb (long screws, drilled first). (3) Drill the four corner pilot holes through the door, the gasket, the sheet and the plywood, 1/4 in in from each corner of the door, and screw the four #8 x 2 in stainless screws in until the door is snug on the gasket, not crushed. (4) Check the door opens a full 90 degrees without catching the toilet, the curtain or the head arm, and shuts flat with all four screws in.',
    '<b>Seal and trim.</b> Fit the J-shaped end trim over the sheet edges at the rear end and at the cab end, glued to the plywood, with a bead of sealant in the 1/8 in gap behind each (drawing F); fit the top trim strip under the ceiling; fill the 1/4 in gap at the pan with flexible sealant and tool it; seal every nook corner and behind the head flange; seal the plywood and sheet edges at the opening where the gasket does not cover them; wipe the excess off straight away. Let it cure a day.',
    "<b>Seal around the valve and the head</b> (drawing I), after the sheet is glued and the valve and the shower arm are in, with the trim plates off. (1) Wipe the sheet around the head hole, the door around the valve hole and the back of each plate with isopropyl alcohol and let it dry. (2) Dry-fit the plate: it must cover its hole by at least 1/2 in all round. (3) Run a continuous 1/8 in bead of neutral-cure silicone or MS polymer on the back of the plate, in a closed ring about 1/4 in in from its edge, with no gaps (overlap the ends). (4) Press the plate on and tighten its own screws, which go into the valve fitting and never into the sheet or the door alone, until the bead squeezes out evenly all round; do not over-tighten, which cracks the plate. (5) Stick painter's tape on the surface 1/4 in outside the plate's edge, run a thin bead in the gap between the tape and the plate, smooth it in one pass with a wet finger or a tool, and pull the tape off before it skins. (6) Leave the cartridge and the handle alone: the valve's own seals look after them. (7) Wait a day, then run the shower for ten minutes and look for wet behind: back out the four screws, swing the door open and look at the back of the valve and the two elbows. Check these beads once a year and redo any that crack or go black.",
    '<b>Connect the water and test it with the door open.</b> Push the two PEX lines onto the elbows with the 8 to 12 in of spare line behind the door, close the two shutoffs in the sink cabinet and open them slowly, run the shower with the door OPEN and look at every joint with a dry paper towel; then close the door onto its gasket and screw it down. If a joint ever weeps, the shutoffs and the door are all you need.',
    '<b>Finish and test.</b> Hang the curtains from the ceiling rail and the nook cord (the Wet bath page), then run the shower for ten minutes with the curtains closed and check under the floor and along the bottom of the back wall, and along the foot of the wall W5 by the fridge, for any wet.',
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
