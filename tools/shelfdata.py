# The charging gear on ONE pull-out shelf over the battery, and the raised couch. The same numbers as layout() in ia_core.js (sizes: inverter 14.8 x 7.7 x 3.9, DC-DC 16 x 9 x 4.5, VEVOR 9.5 x 7 x 4).
# Shared by gen2.py (diagram B), plan.py (F), couch.py (C), leaf.py (C2, C3) and shelf.py (C4) through exec, so the static drawings cannot drift from each other.
PLAT = 17.5                      # seat base: deck 3/4 + the 3/4 leaf folded on it (was 14)
DECK_T = PLAT - .75              # deck top 16 3/4
DECK_U = PLAT - 1.5              # deck underside 16
CUSH = 5                         # seat and back cushion thickness (was 6; 5 keeps a seated head under the wall cabinets after the raise)
SEAT_T = PLAT + CUSH             # seat cushion top 22 1/2
BACK_T = SEAT_T + 20             # back cushion top 42 1/2
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
# the lift-out front rail across the opening: a 3/4 x 1 1/2 in steel tube under the deck's front edge, on two angle ledges
FACE_Z0, FACE_Z1 = 10.25, 14.25  # the shelf's louvered face (1/4 in under the rail's ledges)
RAIL_Z0, RAIL_Z1 = DECK_U - 1.5, DECK_U   # 14 1/2 to 16
RAIL_Y0, RAIL_Y1 = HATCH_Y, HATCH_Y + .75  # 25 1/4 to 26: directly over the face
GAP_W = SH_DIV + .75             # the divider's east face (39 3/8)
GAP_E = C0                       # the couch's end panel next to the closet (74)
RAIL_L = GAP_E - GAP_W - .125    # 1/16 in each end
LEDGE = 1.25                     # angle legs 1 1/4 x 1 1/4 x 1/8
# the wall cabinets: the bottom was 61, raised 2 in to 63 (user: 'make the wall cabinets be 2 in higher'); the top stays at the finished ceiling at the wall
CAB_BOT = 63; CAB_TOP = 74.5625; DOOR_H = 10; DOOR_Z0 = CAB_BOT + .5; DOOR_Z1 = DOOR_Z0 + DOOR_H
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
