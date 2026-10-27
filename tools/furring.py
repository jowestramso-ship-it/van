# The furring strips of the driver wall: their dots (attachment points), their pieces, and the side window opening they stop at.
# Exec'd by gen2.py (after shelfdata.py, which has the window's numbers) and by furrlist.py, so the maps, the tables and the cut list use one set of numbers.
# the main strips S1 to S8 are 1x4 laid flat: 3/4 thick and 3 1/2 wide (they were 1x2, 3/4 x 1 1/2); the window frame J1 to J4 and the nook frames V1 to V4 and cross pieces stay 1x2 (3/4 x 1 1/2)
STRIP_W, STRIP_T, FRAME_W = 3.5, .75, 1.5
# a spacer block: a 3 1/2 in cut off a 2x4 stood on its 3 1/2 in side: 1 1/2 along the wall x 3 1/2 up (as tall as the strip is wide) on the steel and 3 1/2 out (3 5/8 with the glue); the grain runs up the face, so the strip's screw goes into side grain
SPC_W, SPC_H, SPC_D = 1.5, 3.5, 3.5
HT = {'S1': 3, 'S2': 12, 'S3': 21.4, 'S4': 30.25, 'S5': 43.5, 'S6': 57.25, 'S7': 66, 'S8': 76.75}   # center heights up from the floor (the strip is 3 1/2 in wide, so it runs 1 3/4 in either side of its center)
AP = {'S1': [6, 17.75, 31.25, 82.94, 98.9, 119.35, 139.95], 'S2': [15, 30.75, 40, 54, 62, 72, 80, 96, 104, 119.35, 139.95], 'S3': [22, 34, 46, 58, 70, 78, 99, 110, 122, 134, 146], 'S4': [10, 17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75, 147], 'S5': [17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75], 'S6': [10, 17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75, 147], 'S7': [17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9, 114.94, 127.25, 139.75], 'S8': [10, 24, 36, 58.6, 76, 93, 98.9, 114, 127, 140]}
JAMB = 1.5                                  # the window opening is framed with a sill, a head and two jambs of the same 3/4 x 1 1/2 in strip
WL, WR = WIN_CX0 - JAMB, WIN_CX1 + JAMB     # the strips stop at the jambs
FR_Z0, FR_Z1 = WIN_CZ0 - JAMB, WIN_CZ1 + JAMB
WIN_STRIPS = [n for n, h in HT.items() if h + STRIP_W / 2 > FR_Z0 and h - STRIP_W / 2 < FR_Z1]   # the strips that cross the opening (S5 and S6)
for _n in WIN_STRIPS:
    AP[_n] = [x for x in AP[_n] if x < WL or x > WR]          # the dots inside the opening go
    if not any(x > WR for x in AP[_n]): AP[_n].append(147)    # the short piece past the window keeps one dot
SEG_D = {n: [(0, 154)] for n in HT}; SEG_D['S1'] = [(0, 42), (76, 154)]
for _n in WIN_STRIPS: SEG_D[_n] = [(0, WL), (WR, 154)]
# the opening's frame, from the back mark and up from the floor: (name, x0, x1, z0, z1)
WIN_FRAME = [('J1 left jamb', WL, WIN_CX0, FR_Z0, FR_Z1), ('J2 right jamb', WIN_CX1, WR, FR_Z0, FR_Z1), ('J3 sill', WIN_CX0, WIN_CX1, FR_Z0, WIN_CZ0), ('J4 head', WIN_CX0, WIN_CX1, WIN_CZ1, FR_Z1)]
# three blocks under each piece of the frame: the jambs at the top, middle and bottom, the sill and the head at a third of the way along
FRAME_BLK = []
for _nm, _x0, _x1, _z0, _z1 in WIN_FRAME:
    if _z1 - _z0 > _x1 - _x0:   # a jamb
        FRAME_BLK += [(_nm[:2], (_x0 + _x1) / 2, _z) for _z in (_z0 + 3, (_z0 + _z1) / 2, _z1 - 3)]
    else:                      # the sill and the head
        FRAME_BLK += [(_nm[:2], _x0 + (_x1 - _x0) * _f, (_z0 + _z1) / 2) for _f in (1 / 6, .5, 5 / 6)]
# the passenger side, which has no window: the strips stop at the sliding door (104 in) and are cut away at the two nooks
SEG_P = {'S1': [(0, 42), (76, 104)], 'S2': [(0, 104)], 'S3': [(0, 104)], 'S4': [(0, 104)], 'S5': [(0, 11), (31.25, 74.5), (94.75, 104)], 'S6': [(0, 104)], 'S7': [(0, 104)], 'S8': [(0, 154)]}
PAP = {'S1': [6, 17.75, 31.25, 82.94, 98.9], 'S2': [15, 30.75, 40, 54, 62, 72, 80, 96, 104], 'S3': [22, 34, 46, 58, 70, 78, 99], 'S4': [10, 17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9], 'S5': [2, 9, 32, 44.5, 58.6, 71.31, 98.9], 'S6': [10, 17.75, 31.25, 44.5, 58.6, 71.31, 82.94, 98.9], 'S7': [x for x in AP['S7'] if x <= 104], 'S8': AP['S8']}
# the nook frames: (name, x0, x1, bottom, top, spacer?)
S4_TOP, S6_BOT = HT['S4'] + STRIP_W / 2, HT['S6'] - STRIP_W / 2      # the counter nook frames run from the top of S4 to the bottom of S6 (32 to 55 1/2)
VFR = (('V1', 11, 12.5, 38, 54, True), ('V2', 29.75, 31.25, 38, 54, True), ('V3', 74.5, 76, S4_TOP, S6_BOT, True), ('V4', 93.25, 94.75, S4_TOP, S6_BOT, False))
# where the long strips are joined (a strip over 96 in does not come in one stick); the joint sits on a dot
JOINT_D = {'S2': 80, 'S3': 78, 'S4': 71.25, 'S5': 71.25, 'S6': 71.25, 'S7': 71.25, 'S8': 76}
JOINT_P = {'S2': 54, 'S3': 46, 'S4': 58.625, 'S6': 58.625, 'S7': 58.625, 'S8': 76}
def cut_pieces(seg, joint, dots):
    """every strip piece: (strip, letter, x0, x1, joined?, dots in the piece), in order from the back"""
    out = []
    for n in HT:
        pcs = []
        for x0, x1 in seg[n]:
            j = joint.get(n)
            if j and x0 < j < x1: pcs += [(x0, j, False), (j, x1, True)]
            else: pcs.append((x0, x1, False))
        for k, (x0, x1, after) in enumerate(pcs):
            joined = after or (k + 1 < len(pcs) and pcs[k + 1][2])
            d = [x for x in dots[n] if (x > x0 + .1 if after else x >= x0 - .1) and x <= x1 + .1]
            out.append((n, 'abc'[k] if len(pcs) > 1 else '', x0, x1, joined, d))
    return out
DRV_PIECES = cut_pieces(SEG_D, JOINT_D, AP)
PASS_PIECES = cut_pieces(SEG_P, JOINT_P, PAP)
DRV_BLOCKS = sum(len(AP[n]) for n in ('S4', 'S5', 'S6')) + len(FRAME_BLK)
PASS_BLOCKS = len(PAP['S4']) + sum(1 for x in PAP['S5'] if 31.25 <= x <= 74.5) + len(PAP['S6']) + 3 * 3      # S4, S5 (middle piece only), S6, and three under each of V1 to V3
DRV_SHIMS = len(AP['S7']) + len(AP['S8'])
PASS_SHIMS = len(PAP['S7']) + len(PAP['S8'])
# the totals for the cut list and the build guide
import math as _m
FRAME_LEN = {nm: max(z1 - z0, x1 - x0) for nm, x0, x1, z0, z1 in WIN_FRAME}
NOOK_LEN = [t - b for nm, x0, x1, b, t, sp in VFR] + [17.25] * 3
ALL_LENGTHS = [p[3] - p[2] for p in DRV_PIECES + PASS_PIECES] + list(FRAME_LEN.values()) + NOOK_LEN
N_PIECES = len(ALL_LENGTHS)
def pack_sticks(lengths, stick=96, kerf=.125):
    """first fit, longest first, onto 8 ft sticks with a saw kerf"""
    sticks = []
    for L in sorted(lengths, reverse=True):
        for i, s in enumerate(sticks):
            if s + L + kerf <= stick: sticks[i] = s + L + kerf; break
        else: sticks.append(L + kerf)
    return len(sticks)
MAIN_LENGTHS = [p[3] - p[2] for p in DRV_PIECES + PASS_PIECES]      # the 1x4 strips S1 to S8
SMALL_LENGTHS = list(FRAME_LEN.values()) + NOOK_LEN                   # the 1x2 window frame, nook frames and cross pieces
N_PIECES4, N_PIECES2 = len(MAIN_LENGTHS), len(SMALL_LENGTHS)
N_STICKS4, N_STICKS2 = pack_sticks(MAIN_LENGTHS), pack_sticks(SMALL_LENGTHS)
N_BUY4, N_BUY2 = _m.ceil(N_STICKS4 * 1.15), _m.ceil(N_STICKS2 * 1.15)
N_STICKS = N_STICKS4 + N_STICKS2
N_BUY = N_BUY4 + N_BUY2
TOT_BLOCKS = DRV_BLOCKS + PASS_BLOCKS
BLK_PER_STICK = int(96 // (SPC_D + .125))                                # blocks cut off one 8 ft 2x4 with a 1/8 in kerf
N_2X4 = _m.ceil(TOT_BLOCKS / BLK_PER_STICK * 1.1)
TOT_SHIMS = DRV_SHIMS + PASS_SHIMS
