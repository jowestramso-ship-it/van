# The charging gear on ONE pull-out shelf over the battery, and the raised couch. The same numbers as layout() in ia_core.js (sizes: inverter 14.8 x 7.7 x 3.9, DC-DC 16 x 9 x 4.5, VEVOR 9.5 x 7 x 4).
# Shared by gen2.py (diagram B), plan.py (F), couch.py (C), leaf.py (C2, C3) and shelf.py (C4) through exec, so the static drawings cannot drift from each other.
PLAT = 18.5                      # seat base: deck 3/4 + the 3/4 leaf folded on it (was 14, then 17 1/2; raised 1 in so a 3/4 x 1 rail can run across the cabinet front)
DECK_T = PLAT - .75              # deck top 17 3/4
DECK_U = PLAT - 1.5              # deck underside 17
CUSH = 5                         # seat and back cushion thickness (was 6; 5 keeps a seated head under the wall cabinets after the raise)
SEAT_T = PLAT + CUSH             # seat cushion top 23 1/2
BACK_T = SEAT_T + 20             # back cushion top 43 1/2
BAT = (52, 73); C0 = 74
SH_G, SH_T = 1.0, .5             # gap over the battery (9 1/2) and the tray's plywood
SH_Z0 = 9.5 + SH_G; SH_Z1 = SH_Z0 + SH_T
HATCH_Y = 26 - .75               # the tray's face, flush with the couch front (the removable louvered panel was here)
SH_X1 = C0 - .65                 # outer face of the end rail, 1/2 in slide + 1/8 in clearance off the closet's end panel (74)
SH_X0 = SH_X1 - (16 + 14.8 + 2.5)   # two 3/4 in rails + 1/4 in each side + 1/2 between the DC-DC charger and the inverter
DD = max(9, 7.7)
SH_Y0 = HATCH_Y - (.75 + DD + .5 + 7 + .25)   # the rear lip, the first row, 1/2 in, the front row (7), 1/4 in to the face
SH_Y1 = HATCH_Y
DC = dict(x0=SH_X0 + 1, x1=SH_X0 + 1 + 16, y0=SH_Y0 + .75, y1=SH_Y0 + .75 + 9, h=4.5)
INV = dict(x0=DC['x1'] + .5, x1=DC['x1'] + .5 + 14.8, y0=SH_Y0 + .75, y1=SH_Y0 + .75 + 7.7, h=3.9)
CHG = dict(x0=DC['x0'], x1=DC['x0'] + 9.5, y0=SH_Y0 + .75 + DD + .5, y1=SH_Y0 + .75 + DD + .5 + 7, h=4)
SH_DIV = SH_X0 - .65 - .75       # the slide divider's west face
SH_PULL = 18                     # 18 in full-extension slides
# the shelf's plain face: 1/4 in under the deck's rails is no longer needed (the lift-out rail is dropped), but it stays 1 3/4 in under the deck so air reaches the units
FACE_Z0, FACE_Z1 = 10.25, 14.25
# the gear cabinet (user: 'I will need to build a cabinet for 7, 8, 10, 11. It will attach to the floor of the van. The top part will slide out'): two 3/4 in plywood side panels standing on the floor,
# as deep as the couch, floor to the deck's underside; the west one is the slide divider, the east one the couch's end panel next to the closet. No front, back or top of its own.
CB_X0, CB_X1, CB_T = SH_DIV, C0, .75
CB_Y1 = HATCH_Y + .75            # 26: the couch front
CB_H = DECK_U                    # 17
# the removable couch frame (user: 'the couch/bed item to fit on top and will be removable ... blocks along the back wall by 3in and 41in, maybe even 20in'):
# a full-length back rail hung on three wall blocks, a front rail, an end rail and a cross rail west of the cabinet on three posts, and a separate deck lid on top
BR_H = 3.5                       # the rails are 3/4 x 3 1/2 on edge
BR_Z0 = DECK_U - BR_H            # 13 1/2
BLK_X = (3, 20, 41)              # centers along the wall; the middle one 'if needed'
BLK_W, BLK_D = 1.5, 1.5          # a 2x2 (1 1/2 x 1 1/2 actual), standing on the floor against the wall (so they carry the back of the couch to the floor), tops at the rail's underside
BLK_Z0, BLK_Z1 = 0, BR_Z0; BLK_H = BLK_Z1 - BLK_Z0   # 0 to 13 1/2: screwed through the planks into the furring rails S1 (3 up) and S2 (12 up)
BEAM_T = 1.5                     # over the cabinet the back rail is doubled (two 3/4 x 3 1/2 on edge = 1 1/2 thick) and rests on a ledger on each panel
LEDGE_L, LEDGE_H = 3, 1.5        # 3/4 x 1 1/2 x 3 in, top at the rail's underside
POST = 1.5
# the front rail across the cabinet (user: 'Can't we have that extend over the cabinet? I can make the couch higher if needed'): 3/4 x 1 hardwood on edge, glued AND screwed to the deck's underside along the front edge between the cabinet panels,
# so rail and plywood work as one stiff T-beam; its bottom stays 1/2 in over the tallest unit (15 1/2). Without it the deck's free front edge (34 5/8 in) would sag 1/4 to 1 in under a person.
RL_T, RL_H = .75, 1.0
RL_Z0, RL_Z1 = DECK_U - RL_H, DECK_U          # 16 to 17
RL_X0, RL_X1 = CB_X0 + CB_T, CB_X1          # between the panels
RL_Y0, RL_Y1 = CB_Y1 - RL_T, CB_Y1
POST_X = (0, SH_DIV - POST)      # two posts, so the lawn chairs (34 1/2 long) can still slide in between them
# the wall cabinets: the bottom was 61, raised 2 in to 63 (user: 'make the wall cabinets be 2 in higher'); the top stays at the finished ceiling at the wall
CAB_BOT = 63; CAB_TOP = 74.5625; DOOR_H = 10; DOOR_Z0 = CAB_BOT + .5; DOOR_Z1 = DOOR_Z0 + DOOR_H
# the side window over the dinette: Van Windows Direct TL201-SE, driver side forward slider (the numbers of window.py and wtemplate.py)
WIN_CX0, WIN_CZ0 = 101.75, 39.0       # the cutout's left edge from the back, and its bottom edge up from the floor (centered on the table, sill 1 in over the backrests)
WIN_CW, WIN_CH = 39.6875, 22.625      # the cutout (the slider frame's outline)
WIN_GW, WIN_GH = 54.35, 29.12         # the glass, overall
WIN_OL, WIN_OB = 9.6875, 2.75         # the glass's left edge is this far left of the cutout, its bottom edge this far below it
WIN_GX0 = WIN_CX0 - WIN_OL; WIN_GX1 = WIN_GX0 + WIN_GW; WIN_GZ0 = WIN_CZ0 - WIN_OB; WIN_GZ1 = WIN_GZ0 + WIN_GH
WIN_CX1 = WIN_CX0 + WIN_CW; WIN_CZ1 = WIN_CZ0 + WIN_CH
AIR = DECK_U - (SH_Z1 + max(DC['h'], INV['h'], CHG['h']))   # air above the tallest unit
def fr8(v):
    """inches as a whole number and eighths: 41.6 -> '41 5/8'"""
    n = round(v * 8); w, e = divmod(n, 8)
    if e == 0: return str(w)
    from math import gcd
    g = gcd(e, 8); return (f'{w} ' if w else '') + f'{e // g}/{8 // g}'
def fr16(v):
    """inches as a whole number and sixteenths, the way the interactive page prints them: 41.05 -> '41 1/16'"""
    n = round(v * 16); w, e = divmod(n, 16)
    if e == 0: return str(w)
    from math import gcd
    g = gcd(e, 16); return (f'{w} ' if w else '') + f'{e // g}/{16 // g}'
