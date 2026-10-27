# C2: the bed with a hinged leaf, seen from the aisle (looking at the driver side wall), day and night
# C3: build detail of the leaf, the hinge and a leg in its slot (section from the rear)
# couch 26 deep on a base, leaf 20 deep (3/4 plywood, no rails), deck 16 to 16 3/4 (raised 3 1/2 in for the gear shelf), legs 12 5/8 in of bar plus a 3 1/2 in screw-out foot (16 1/8 standing) on pins at mid-thickness, 3 in in from the free edge (they land 43 in out)
S=5; W=1050; FLY=420
DECK=DECK_T; DU=DECK_U
def _panel(ox, night):
    X=lambda x: ox+S*x
    Y=lambda z: FLY-S*z
    r=lambda x0,x1,z0,z1: f'x="{X(x0):g}" y="{Y(z1):g}" width="{S*(x1-x0):g}" height="{S*(z1-z0):g}"'
    o=[]
    o.append(f'<rect class="box" {r(0,92,0,76)} stroke-width="0.5"/>')
    o.append(f'<g class="c-amber"><rect {r(0,92,75.8125,76)} stroke-width="0.5"/><rect {r(0,92,75.0625,75.8125)} stroke-width="0.5"/></g>')
    o.append(f'<g class="c-purple"><rect {r(0,74,CAB_BOT,CAB_TOP)} stroke-width="0.5" stroke-dasharray="5 3"/><text class="ts" x="{X(37):g}" y="{Y((CAB_BOT+CAB_TOP)/2):g}" text-anchor="middle" dominant-baseline="central">Wall cabinets</text></g>')
    o.append(f'<g class="c-gray"><rect {r(74,89,0,75.0625)} stroke-width="0.5"/><text class="ts" x="{X(81.5):g}" y="{Y(40):g}" text-anchor="middle" dominant-baseline="central">Closet</text></g>')
    o.append(f'<g class="c-gray"><rect {r(0,74,0,DU)} stroke-width="0.5" stroke-dasharray="5 3"/>' + ('' if night else f'<text class="ts" x="{X(37):g}" y="{Y(6):g}" text-anchor="middle" dominant-baseline="central">Under the deck, 16 in tall</text>') + f'<rect {r(0,74,DU,DECK)} stroke-width="0.5"/></g>')
    if not night:
        o.append(f'<g class="c-amber"><rect {r(0,74,DECK,PLAT)} stroke-width="0.5"/></g>')
        o.append(f'<g class="c-purple"><rect {r(0,74,PLAT,SEAT_T)} stroke-width="0.5"/><text class="th" x="{X(37):g}" y="{Y((PLAT+SEAT_T)/2):g}" text-anchor="middle" dominant-baseline="central">Seat cushion, top at {fr8(SEAT_T)}</text></g>')
        o.append(f'<g class="c-purple"><rect {r(0,74,SEAT_T,BACK_T)} stroke-width="0.5"/><text class="th" x="{X(37):g}" y="{Y((SEAT_T+BACK_T)/2):g}" text-anchor="middle" dominant-baseline="central">Back cushion, upright (20 tall)</text></g>')
    else:
        o.append('<g class="c-gray">' + ''.join(f'<rect {r(lx,lx+1.25,0.25,DU)} stroke-width="0.5"/>' for lx in (1,24.6,48.2,71.75)) + '</g>')
        o.append(f'<text class="ts" x="{X(19):g}" y="{Y(6):g}" text-anchor="middle" dominant-baseline="central">4 fold-down legs</text>')
        o.append(f'<g class="c-amber"><rect {r(0,74,DU,DECK)} stroke-width="0.5"/></g>')
        o.append(f'<g class="c-purple"><rect {r(0,74,DECK,DECK+CUSH)} stroke-width="1"/><text class="th" x="{X(37):g}" y="{Y(DECK+CUSH/2):g}" text-anchor="middle" dominant-baseline="central">Back cushion on the leaf, top at 21 3/4</text></g>')
    return '\n'.join(o)
_svg=f'<svg viewBox="0 0 {W} 480" role="img"><title>The bed with a hinged leaf, seen from the aisle, day and night</title>\n'
_svg+=f'<text class="th" x="50" y="24" style="font-size:14px">Day: couch</text>\n'+_panel(50,False)+'\n'
_svg+=f'<text class="ts" x="50" y="{FLY+22}" style="font-size:12px">Leaf folded back flat on the deck under the seat cushion, legs in their slots,</text><text class="ts" x="50" y="{FLY+37}" style="font-size:12px">back cushion against the wall, seat top at 22 1/2 in</text>\n'
_svg+=f'<text class="th" x="540" y="24" style="font-size:14px">Night: bed</text>\n'+_panel(540,True)+'\n'
_svg+=f'<text class="ts" x="540" y="{FLY+22}" style="font-size:12px">Leaf flipped out level with the deck on four legs, back cushion on it,</text><text class="ts" x="540" y="{FLY+37}" style="font-size:12px">seat cushion back on the deck: bed 74 x 46, top at 21 3/4 in</text>\n</svg>'

# ---- C3 build detail (scale 10 px per inch, section from the rear, wall on the left; y = inches out from the planks)
def _detail(FL, night):
    S=10; OX=60
    X=lambda y: OX+S*y
    Z=lambda z: FL-S*z
    r=lambda y0,y1,z0,z1: f'x="{X(y0):g}" y="{Z(z1):g}" width="{S*(y1-y0):g}" height="{S*(z1-z0):g}"'
    ink='#2C2C2A'
    ld=lambda x1,y1,x2,y2: f'<line x1="{x1:g}" y1="{y1:g}" x2="{x2:g}" y2="{y2:g}" stroke="#888780" stroke-width="0.6" stroke-dasharray="3 3"/>'
    o=[]
    o.append(f'<line x1="{X(0):g}" y1="{Z(25):g}" x2="{X(0):g}" y2="{FL:g}" stroke="{ink}" stroke-width="2"/>')
    o.append(f'<line x1="{X(0):g}" y1="{FL:g}" x2="{X(56):g}" y2="{FL:g}" stroke="{ink}" stroke-width="1"/>')
    # wheel well and battery (dashed: only at 42 to 76 and 52 to 73 in from the back)
    o.append(f'<rect {r(0,6.25,0,7.5)} fill="#E24B4A" fill-opacity="0.15" stroke="#A32D2D" stroke-width="1" stroke-dasharray="5 3"/>')
    o.append(f'<rect {r(6.25,16.25,0,9.5)} fill="#F2B84B" fill-opacity="0.3" stroke="#8A5A00" stroke-width="1" stroke-dasharray="5 3"/>')
    o.append(f'<text class="ts" x="{X(3.1):g}" y="{Z(3.2):g}" text-anchor="middle" style="font-size:9px">well</text><text class="ts" x="{X(11.25):g}" y="{Z(4.5):g}" text-anchor="middle" style="font-size:9px">battery</text>')
    # the frame: deck on a front rail (west of the gear cabinet; over the cabinet the lid rests on the two panels)
    o.append(f'<g class="c-gray"><rect {r(0,26,DU,DECK)} stroke-width="0.5"/><rect {r(25.25,26,DU-1.5,DU)} stroke-width="0.5"/></g>')
    if not night:
        # leaf folded back on the deck, face down: free edge at 6, hinge at 26; the leg lies in its slot (pin 3 in from the free edge)
        o.append(f'<g class="c-amber"><rect {r(6,26,DECK,PLAT)} stroke-width="0.5"/></g>')
        o.append(f'<rect {r(9,21.625,DECK+0.1875,DECK+0.5625)} fill="{ink}" opacity="0.85"/>')
        o.append(f'<circle cx="{X(26):g}" cy="{Z(DECK):g}" r="3.5" fill="{ink}"/>')
        o.append(f'<g class="c-purple"><rect {r(0,26,PLAT,SEAT_T)} stroke-width="0.5"/><text class="th" x="{X(13):g}" y="{Z((PLAT+SEAT_T)/2):g}" text-anchor="middle" dominant-baseline="central">Seat cushion</text></g>')
        o.append(f'<text class="ts" x="{X(27.5):g}" y="{Z(PLAT+3.6):g}">Hinge on the top faces,</text><text class="ts" x="{X(27.5):g}" y="{Z(PLAT+3.6)+15:g}">closes flat</text>')
        o.append(ld(X(27.4),Z(PLAT+3.6)+19,X(26.3),Z(DECK-.1)))
        o.append(f'<text class="ts" x="{X(27.5):g}" y="{Z(DU-2.1):g}">Front rail under the deck edge (west of the cabinet)</text>')
        o.append(ld(X(27.4),Z(DU-2.1)-4,X(26.1),Z(DU-.8)))
        o.append(f'<text class="ts" x="{X(17.5):g}" y="{Z(5.6):g}">Leaf folded back, face down: the leg lies in its slot,</text><text class="ts" x="{X(17.5):g}" y="{Z(5.6)+15:g}">nothing sticks out under the cushion</text>')
        o.append(ld(X(21),Z(5.6)-4,X(20),Z(DECK-.1)))
    else:
        # leaf out, level with the deck; the slot (dashed) and the leg standing 3 in from the free edge (43 in out)
        o.append(f'<g class="c-amber"><rect {r(26,46,DU,DECK)} stroke-width="0.5"/></g>')
        o.append(f'<rect {r(30.125,43.75,DU+0.1,DECK-0.1)} fill="none" stroke="#5A3A00" stroke-width="0.8" stroke-dasharray="3 2"/>')
        o.append(f'<rect {r(42.81,43.19,3.9,DECK-0.375)} fill="{ink}" opacity="0.8"/><rect {r(42.9,43.1,0.4,3.9)} fill="{ink}" opacity="0.8"/><rect {r(42.3,43.7,0,0.4)} fill="{ink}"/>')
        o.append(f'<circle cx="{X(43):g}" cy="{Z(DECK-0.375):g}" r="3" fill="{ink}"/>')
        o.append(f'<circle cx="{X(26):g}" cy="{Z(DECK):g}" r="3.5" fill="{ink}"/>')
        o.append(f'<g class="c-purple"><rect {r(0,26,DECK,DECK+CUSH)} stroke-width="0.5"/><text class="th" x="{X(13):g}" y="{Z(DECK+CUSH/2):g}" text-anchor="middle" dominant-baseline="central">Seat cushion</text><rect {r(26,46,DECK,DECK+CUSH)} stroke-width="0.5"/><text class="th" x="{X(36):g}" y="{Z(DECK+CUSH/2):g}" text-anchor="middle" dominant-baseline="central">Back cushion, {CUSH} thick</text></g>')
        # shower pan (down): front edge at 44, 1 in from the leg
        o.append(f'<rect {r(44,52,0,3)} fill="#185FA5" fill-opacity="0.15" stroke="#185FA5" stroke-width="1" stroke-dasharray="4 3"/><text class="ts" x="{X(48):g}" y="{Z(1.3):g}" text-anchor="middle" style="font-size:9px;fill:#185FA5">shower pan, down</text>')
        o.append(f'<line x1="{X(43.19):g}" y1="{Z(4.6):g}" x2="{X(44):g}" y2="{Z(4.6):g}" stroke="#A32D2D" stroke-width="1.6"/><text class="ts" x="{X(46.5):g}" y="{Z(5.6):g}" text-anchor="middle" style="font-size:9px;fill:#A32D2D">1 in to the pan</text>')
        o.append(f'<text class="ts" x="{X(17):g}" y="{Z(8.2):g}">Leg: 3/8 x 1 1/4 bar, 12 5/8 long + a 3 1/2 in screw-out foot, on a pin through</text><text class="ts" x="{X(17):g}" y="{Z(8.2)+15:g}">the leaf; it lands 43 in out (3 in in)</text>')
        o.append(ld(X(42.2),Z(8.2)-4,X(42.9),Z(8.8)))
        o.append(f'<text class="ts" x="{X(17):g}" y="{Z(3.2):g}">Slot (dashed): the leg lies in it when folded</text>')
        o.append(ld(X(31),Z(3.2)-4,X(33),Z(DU+.3)))
        o.append(f'<text class="ts" x="{X(26.5):g}" y="{Z(DECK+8):g}">Both halves are {CUSH} in of padding on a level top at 21 3/4 in</text>')
    return '\n'.join(o)
_det=f'''<svg viewBox="0 0 680 640" role="img"><title>Leaf, hinge and leg detail</title>
<text class="th" x="60" y="26" style="font-size:14px">Day: leaf folded back</text>
{_detail(290,False)}
<text class="th" x="60" y="346" style="font-size:14px">Night: leaf flipped out</text>
{_detail(600,True)}
</svg>'''

_h=open((ROOT+'/sides.html')).read()
_blk='''<h3>Driver side: the bed with a hinged leaf, day and night</h3>
<div class="wide">'''+_svg+'''</div>
<p>Seen from the aisle, looking at the driver side wall. <b>Day (left):</b> the 20 in leaf lies back flat on the deck (deck top at 16 3/4 in), face down, under the seat cushion (leaf top at 17 1/2 in, seat cushion 17 1/2 to 22 1/2 in), and the back cushion (5 in thick, 20 in tall) stands against the wall (22 1/2 to 42 1/2 in up). The couch is 3 1/2 in higher than it was so the gear shelf fits over the battery (diagram C4). The seat is 22 1/2 in high and 21 in deep (the 26 in couch minus the 5 in cushion). <b>Night (right):</b> the seat cushion comes off, the leaf is flipped out on its hinge along the front edge of the deck until it is level with the deck, four legs (12 5/8 in of bar plus a 3 1/2 in screw-out foot) fold down out of slots in the leaf (one near each end and two between them, about 24 in apart, because the leaf is 74 in long), the seat cushion goes back and the back cushion lies on the leaf as one 20 in piece. The bed is 74 x 46 in (26 + 20) with its top at 21 3/4 in (the seat is 22 1/2 in by day, 3/4 in higher because the folded leaf sits under it); from the aisle only the low strip shows. There are no rails and no slides, so the space under the deck stays open at 16 in (the battery and wheel well stay where they are, with the gear shelf over the battery). The legs, the hinge and the slots are on C3, and the flip is animated on the interactive page (click the couch, or open the Bed, from the end view).</p>
<h3>Driver side: building the leaf, slots and legs</h3>
<div class="wide">'''+_det+'''</div>
<p>Section from the rear (wall on the left, 0 is the finished wall face). <b>Frame:</b> the deck is part of a removable frame (diagram C5): a back rail on three wall blocks and, west of the gear cabinet, a 3/4 x 3 1/2 in rail under the front edge of the deck on two posts; over the cabinet the frame rests on the cabinet's two panels. <b>Leaf:</b> 3/4 in birch plywood, 20 x 73 3/4 in, edges banded, about 24 lb, a plain flat slab with no rails, so folded back it leaves no ridges under the seat cushion. <b>Hinge:</b> a 74 in continuous hinge, 1 1/2 in leaves, on the top faces of the deck and the leaf, #8 x 5/8 in screws every 3 to 4 in, a 1/8 to 3/16 in gap so it folds flat both ways. <b>Legs:</b> four 3/8 x 1 1/4 in aluminum flat bars, 12 5/8 in long, each with a threaded rubber foot that screws out about 3 1/2 in (the couch is 3 1/2 in higher than it was, so the leg is 16 1/8 in from pin to floor; the foot is a 3/8 in stud that screws into the bar's end; folded, only the bar lies in the slot), each lying in a through-slot (1 1/2 x 13 in) cut in the leaf, on a 1/4 in stainless pin through the plywood either side of the slot, 3 in from the free edge; folded, the leg is inside the plywood, so the leaf is flat on both faces. The pin is 3 in in from the free edge, so the leg lands 43 in out from the wall (the bed is 46) and the front 3 in of the leaf overhangs it. The two end slots are 1 in in from the ends of the leaf (the sides) and the other two are evenly between them (the four are about 24 in apart, so the free edge never spans more than that; with three legs it spanned 35 in); each slot leaves about 4 in of solid plywood at the hinge end. A stop (the end of the slot) keeps the leg from passing vertical and a ball catch or magnet holds it up. <b>Latches:</b> two turn buttons or magnetic catches hold the leaf folded back while driving. <b>Shower:</b> the leg at the rear end of the leaf lands 43 in out, 1 in short of the front edge of the shower pan (44 in) with the pan down, and the leaf edge hangs 2 in over the pan; the pan is tipped up anyway when the bed is made up. <b>Loads (rough):</b> two adults (350 lb) put about 150 lb on the 20 in leaf; with the legs down about 75 lb of that goes through the hinge (about 3 1/2 lb a screw) and the legs take about 19 lb each. A 200 lb person sitting on the free edge between two legs puts about 100 lb on each nearest leg. With the legs up the same person is a lever of about 4,000 in-lb on the hinge, which is several hundred pounds a screw and more than a #8 screw holds in plywood, so the legs go down before anyone sits on the free edge. A 3/8 x 1 1/4 in flat bar buckles at about 3,500 lb, so the bar is not the weak point; the pin, the slot walls and the hinge screws are.</p>
'''
assert '<h2>2. Passenger side</h2>' in _h
_h=_h.replace('<h2>2. Passenger side</h2>',_blk+'<h2>2. Passenger side</h2>',1)
open((ROOT+'/sides.html'),'w').write(_h)
