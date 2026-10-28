#!/usr/bin/env python3
"""Builds ../window.html: an illustrated step-by-step for the side window (Van Windows Direct TL201-SE, Ford Transit driver side forward slider).
Uses the helpers, styles and page shell of install.py. What is known comes from the window's retailer listings and the Sikaflex P2G data;
what is not known (Van Windows Direct's own instruction sheet was not found) is marked in the page.
Run from this folder (build.sh does):  python3 window.py
"""
import os
import install as I
from install import svg, R, L, C, T, P, PL, dimh, dimv, arrow, fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
exec(open(HERE + '/shelfdata.py').read())      # the window's place in the plan (WIN_*), CAB_BOT and the fraction helpers

WIN_W, WIN_H = 54.35, 29.12          # overall, inches (1380.6 x 739.7 mm on the listing)

EXTRA_CSS = """
.blk { fill: #8b9097; stroke: #3a4048; stroke-width: 1.4; }
.bead { fill: none; stroke: #e0842a; stroke-width: 7; stroke-linejoin: round; stroke-linecap: round; }
.beadfill { fill: #e0842a; stroke: #8a4a10; stroke-width: 1.4; }
.flange { fill: color-mix(in srgb, var(--steel) 35%, var(--card)); stroke: var(--steel); stroke-width: 1.6; }
.dark { fill: #222; stroke: #000; stroke-width: 1.4; }
.glass { fill: #2f4a40; opacity: .85; }
.cutline { fill: none; stroke: #c0392b; stroke-width: 2.4; stroke-dasharray: 8 5; }
.tape2 { fill: #5aa7e0; opacity: .85; stroke: #2d6ea3; stroke-width: .8; }
.cup { fill: #e8e6dd; stroke: #444; stroke-width: 1.4; }
.tdark { font-size: 12px; fill: #fff; font-weight: 700; }
.torange { font-size: 13px; fill: #b4601a; font-weight: 700; }
.tgrey { font-size: 13px; fill: var(--ink); font-weight: 700; }
.trimline { fill: none; stroke: #c0392b; stroke-width: 3; stroke-linejoin: round; }
.warnbox2 { fill: color-mix(in srgb, var(--warn) 12%, var(--card)); stroke: var(--warn); stroke-width: 1.4; }
"""


# ---------------------------------------------------------------- drawings
def window_face(x, y, w, h, rx=18, cls_frame='dark'):
    """the window seen from inside: black frame, glass, divider"""
    o = [R(x, y, w, h, cls_frame, rx)]
    o.append(R(x + 10, y + 10, w - 20, h - 20, 'glass', max(rx - 8, 4)))
    return ''.join(o)


def blocks_row(x, y, w, n=3, bw=26, bh=12):
    return ''.join(R(x + w * (i + 1) / (n + 1) - bw / 2, y, bw, bh, 'blk', 2) for i in range(n))


def fig_w1():
    S = 8.0
    x0, y0 = 60, 54
    w, h = WIN_W * S, WIN_H * S
    o = [window_face(x0, y0, w, h, 20)]
    o.append(L(x0 + w * .52, y0 + 10, x0 + w * .52, y0 + h - 10, 'diag'))
    o.append(T(x0 + w * .26, y0 + h / 2 + 4, 'glass or screen', 'tdark'))
    o.append(T(x0 + w * .76, y0 + h / 2 + 4, 'glass or screen', 'tdark'))
    o.append(blocks_row(x0, y0 + h + 4, w))
    o.append(T(x0 + w / 2, y0 + h + 38, '3 rubber setting blocks along the bottom edge', 'tgrey'))
    o.append(dimh(x0, x0 + w, y0 - 14, '54 3/8 overall'))
    o.append(dimv(x0 - 14, y0, y0 + h, '29 1/8', True))
    o.append(T(280, 18, 'Van Windows Direct TL201-SE, seen from inside', 'tb'))
    return svg(560, 350, ''.join(o), 'The window seen from inside with its size and the three rubber setting blocks on the bottom edge')


def fig_w2():
    x0, y0, w, h = 70, 40, 420, 230
    o = []
    o.append(R(x0, y0, w, h, 'flange', 36))                                # the stamped recess in the van's side
    o.append(T(x0 + 14, y0 + 20, 'factory stamping (the recess for the window)', 'tsm', 'start'))
    ix, iy, iw, ih = x0 + 34, y0 + 34, w - 68, h - 68
    o.append(R(ix, iy, iw, ih, 'cutline', 22))
    o.append(R(ix + 1, iy + 1, iw - 2, ih - 2, 'hole', 22))
    # two uprights across the opening
    for fx in (.33, .68):
        ux = ix + iw * fx
        o.append(R(ux - 9, iy, 18, ih, 'rib'))
    o.append(T(ix + iw * .33, iy + ih / 2 + 4, 'upright', 'twh'))
    o.append(T(ix + iw * .68, iy + ih / 2 + 4, 'upright', 'twh'))
    o.append(T(x0 + w / 2, y0 + h + 22, 'red dashes: usual cut line, round the inner metal edge; trim uprights flush', 'tsm'))
    o.append(T(x0 + w / 2, y0 + h + 40, 'Schematic. The real line comes from Van Windows Direct, and from what you find behind the panel.', 'tsm'))
    return svg(560, 330, ''.join(o), 'The factory stamping with the cut line along the inner metal edge and two uprights to trim flush')


def fig_w3():
    S = 8.0
    ox, oy = 40, 50
    ow, oh = 470, 250
    o = [R(ox, oy, ow, oh, 'flange', 24)]
    gx, gy = ox + 30, oy + 22
    gw, gh = ow - 60, oh - 52
    o.append(window_face(gx, gy, gw, gh, 16))
    o.append(blocks_row(ox, oy + oh - 28, ow))
    o.append(T(ox + ow / 2, oy + oh + 22, 'window set in, unglued, resting on all three blocks', 'tgrey'))
    for fx in (.25, .75):
        o.append(C(gx + gw * fx, gy + gh * .42, 15, 'cup'))
    o.append(T(gx + gw * .25, gy + gh * .42 + 32, 'suction cup', 'tdark'))
    o.append(T(gx + gw * .75, gy + gh * .42 + 32, 'suction cup', 'tdark'))
    for tx, ty in ((ox + 16, oy + 50), (ox + ow - 16, oy + 50), (ox + ow / 2, oy + 6), (ox + ow / 2, oy + oh - 8)):
        o.append(R(tx - 12, ty - 4, 24, 8, 'tape2'))
    o.append(T(ox + ow / 2, oy - 8, 'painter&#39;s tape marks across the joint (4 places) show where it sits'.replace('&#39;', "'"), 'tsm'))
    o.append(T(ox + ow / 2, oy + oh + 42, 'Check the gap is even all round,', 'tsm'))
    o.append(T(ox + ow / 2, oy + oh + 58, 'then work the slider and the latch before you take it out.', 'tsm'))
    return svg(560, 380, ''.join(o), 'Dry-fitting the window: it rests on three blocks with an even gap and tape marks on the joint')


def fig_w4():
    """the bead runs unbroken and steps around each block: face view above, a cut through the bottom edge below"""
    o = []
    ax, ay, aw, ah = 20, 36, 520, 232
    o.append(T(280, 18, 'A. Looking at the window from inside', 'tb'))
    o.append(R(ax, ay, aw, ah, 'flange', 28))
    fx, fy, fw, fh = ax + 56, ay + 34, aw - 112, ah - 80
    o.append(R(fx, fy, fw, fh, 'dark', 14))
    o.append(R(fx + 9, fy + 9, fw - 18, fh - 18, 'glass', 8))
    o.append(T(fx + fw / 2, fy + fh / 2 + 4, 'window', 'tdark'))
    bx0, by0, bx1, by1 = ax + 26, ay + 18, ax + aw - 26, ay + ah - 20
    r = 16
    cx = [fx + fw * f for f in (.2, .5, .8)]
    d = [f'M {bx0 + r} {by0} L {bx1 - r} {by0} Q {bx1} {by0} {bx1} {by0 + r} L {bx1} {by1 - r} Q {bx1} {by1} {bx1 - r} {by1}']
    for c in sorted(cx, reverse=True):
        d.append(f'L {c + 28} {by1} L {c + 28} {by1 - 18} L {c - 28} {by1 - 18} L {c - 28} {by1}')
    d.append(f'L {bx0 + r} {by1} Q {bx0} {by1} {bx0} {by1 - r} L {bx0} {by0 + r} Q {bx0} {by0} {bx0 + r} {by0} Z')
    o.append(f'<path d="{" ".join(d)}" class="bead"/>')
    for c in cx:
        o.append(R(c - 17, by1 - 12, 34, 16, 'blk', 2))
    o.append(T(280, ay + ah + 20, 'Orange: one unbroken bead. At each grey block it steps around the block', 'torange'))
    o.append(T(280, ay + ah + 38, 'and carries on. Nothing is cut out of the bead and no block is taken out.', 'torange'))
    # panel B, a cut through the bottom edge
    by = 362
    o.append(T(280, by - 14, 'B. A cut through the bottom edge', 'tb'))
    bx = 100
    base = by + 112
    o.append(R(bx - 30, base, 420, 22, 'flange'))
    o.append(T(bx + 180, base + 16, "van's steel flange", 'tsm'))
    o.append(R(bx + 20, base - 28, 70, 28, 'blk', 3))
    o.append(T(bx + 55, base - 9, 'block', 'tdark'))
    o.append(P([(bx + 190, base), (bx + 225, base - 28), (bx + 260, base)], 'beadfill'))
    o.append(T(bx + 225, base - 36, 'bead', 'torange'))
    o.append(R(bx - 20, base - 28 - 62, 400, 62, 'dark', 6))
    o.append(T(bx + 180, base - 28 - 26, 'window frame', 'tdark'))
    o.append(T(280, base + 46, 'The frame sits on the blocks and squashes the bead down', 'tgrey'))
    o.append(T(280, base + 64, "to the blocks' height, so the blocks set the thickness.", 'tgrey'))
    o.append(T(280, base + 90, 'Schematic. Confirm the bead position and size with Van Windows Direct.', 'tsm'))
    return svg(560, base + 106, ''.join(o), 'The bead of urethane runs unbroken around the three rubber setting blocks; a cut through the bottom edge shows the frame resting on a block beside the squashed bead')


def fig_w5():
    ox, oy, ow, oh = 70, 56, 420, 230
    o = [R(ox, oy, ow, oh, 'flange', 24)]
    o.append(window_face(ox + 26, oy + 24, ow - 52, oh - 50, 14))
    o.append(T(ox + ow / 2, oy + oh / 2 + 4, 'window', 'tdark'))
    for tx, ty, hor in ((ox + 60, oy + 6, True), (ox + ow / 2, oy + 6, True), (ox + ow - 60, oy + 6, True), (ox + 60, oy + oh - 8, True), (ox + ow / 2, oy + oh - 8, True), (ox + ow - 60, oy + oh - 8, True)):
        o.append(R(tx - 14, ty - 4, 28, 8, 'tape2'))
    o.append(T(ox + ow / 2, oy - 10, 'painter&#39;s tape every 8 to 12 in, from the frame to the body'.replace('&#39;', "'"), 'tgrey'))
    o.append(T(ox + ow / 2, oy + oh + 24, 'Leave it taped. Keep the van still. Do not slam doors.', 'tgrey'))
    o.append(T(ox + ow / 2, oy + oh + 44, 'Drive-away: 3 hours for P2G Premium at 73 F; allow longer when cooler.', 'tsm'))
    return svg(560, 360, ''.join(o), 'The window taped to the body while the adhesive cures')


def fig_w6():
    o = []
    # a cut through the cut edge: two metal walls with a U channel of edge trim over them
    x0 = 150
    o.append(R(x0, 70, 14, 130, 'steel'))
    o.append(R(x0 + 40, 70, 14, 130, 'steel'))
    o.append(R(x0 + 14, 70, 26, 130, 'ply'))
    o.append(T(x0 + 27, 214, 'foam', 'tsm'))
    o.append(T(x0 - 8, 214, 'outer', 'tsm', 'end'))
    o.append(T(x0 + 62, 214, 'inner', 'tsm', 'start'))
    o.append(PL([(x0 - 8, 160), (x0 - 8, 60), (x0 + 62, 60), (x0 + 62, 160)], 'trimline'))
    o.append(T(x0 + 27, 46, 'Trim-Lok clips over both metal edges', 'tgrey'))
    o.append(R(x0 + 95, 100, 215, 64, 'warnbox2', 6))
    o.append(T(x0 + 202, 124, 'If it will not seat,', 'tgrey'))
    o.append(T(x0 + 202, 142, 'dig out the foam between', 'tgrey'))
    o.append(T(x0 + 202, 158, 'the metal walls first.', 'tgrey'))
    o.append(T(280, 244, 'Schematic of the raw cut edge. Buy the trim for the full circumference', 'tsm'))
    o.append(T(280, 260, '(about 14 ft) and tap it on with a rubber mallet.', 'tsm'))
    return svg(560, 280, ''.join(o), 'Edge trim clipped over the cut edge, with the foam between the metal walls removed if needed')


# ---------------------------------------------------------------- page
def build():
    S = []
    st = I.step
    li = I.li
    S.append(st(1, 'Look at the opening',
                '<ul>' + li([
                    'The TL201-SE is Van Windows Direct&rsquo;s driver-side <b>forward</b> slider for a 2015+ Transit: <b>54.35 x 29.12 in</b> overall (1380.6 x 739.7 mm), glued in, using the van&rsquo;s <b>factory metal stamping</b> as the opening (the Nomadic Supply listing says so). It has a screen and a spring latch.',
                    'Look inside before you touch the panel: what is behind it (wiring, trim clips, insulation foam)? Cover the floor and the bed deck.',
                    'Wall cabinets and the dinette conflict with this opening in the plan. You said you will adjust those after the window is in.',
                ]) + '</ul>', fig_w1()))
    S.append(st(2, 'Mask and mark the cut line',
                '<ul>' + li([
                    'Tape the paint all round the stamping on the outside, wide enough for the jigsaw shoe to ride on.',
                    '<b>Where exactly to cut is on Van Windows Direct&rsquo;s sheet, which I have not seen.</b> The listings only say the window uses the factory stamping. The usual way, and what the drawing shows, is to cut along the stamping&rsquo;s inner metal edge and trim any uprights flush with it. Confirm that first.',
                    'Drill a hole at each corner big enough for the blade. Hold the window up to the line before cutting: you cannot put metal back.',
                    'Make a cardboard template first: see <a href="window-template.html">the window measured from your photos</a> (a draft until the orange numbers are taped).',
                ]) + '</ul>', fig_w2()))
    S.append(st(3, 'Cut the opening',
                '<ul>' + li([
                    'Jigsaw, nibbler or air saw with fresh metal blades, going slowly and keeping the shoe flat. Plastic sheet inside to catch the shavings; glasses, gloves and hearing protection.',
                    'Cut to the line you confirmed, then trim any uprights flush with it.',
                    '<b>Cover the opening</b> with plastic taped to clean, dry paint whenever you stop.',
                ]) + '</ul>'))
    S.append(st(4, 'Deburr and treat the edge',
                '<ul>' + li([
                    'File off the burrs, inside and out. Wipe off the dust.',
                    'If the edge trim will not seat over both metal edges, dig out the factory foam between the sheet-metal walls (see the last drawing).',
                    'Rust-inhibiting primer on the raw cut edge, then paint, and let it dry as the cans say. The bonding surface must be left clean for step 6: keep paint off the band the adhesive goes on.',
                    'Test-fit the edge trim all the way round now.',
                ]) + '</ul>'))
    S.append(st(5, 'Dry-fit the window',
                '<ul>' + li([
                    'Two people with suction cups set the window in <b>without glue</b>. The bottom edge rests on the <b>three rubber setting blocks</b> (do not remove them).',
                    'The gap should be even all round. Stick painter&rsquo;s tape across the joint at four places and mark both sides so you can put it back exactly.',
                    'Work the slider, the latch and the screen. Then lift it out and stage it on a clean bench.',
                ]) + '</ul>', fig_w3()))
    S.append(st(6, 'Clean and prime',
                '<ul>' + li([
                    'Van Windows Direct&rsquo;s fixed-window listings say to bond with the <b>Sikaflex P2G</b> urethane and primer kit. I found that on the sister listings, not the TL201-SE&rsquo;s, so confirm it applies. With P2G Premium, Sika&rsquo;s sheet says no primer is needed on the glass or its black band; for the van&rsquo;s painted body follow the kit&rsquo;s sheet (you have already primed).',
                    'Wipe both bonding surfaces (the window&rsquo;s black frame band and the van&rsquo;s flange) with the kit&rsquo;s wipe or isopropyl alcohol. Prime as the kit says and let it flash off for the time on the can. Do not touch it afterwards.',
                    'Sika lists <b>50 to 95 &deg;F</b> for application. Upper 60s is fine.',
                ]) + '</ul>'))
    S.append(st(7, 'Lay the bead, quickly',
                '<ul>' + li([
                    '<b>Be ready first:</b> you have <b>P2G Premium</b>. Sika&rsquo;s sheet gives <b>15 minutes of open time</b> and a <b>35 minute skin time</b> at 73 &deg;F and 50% humidity, and says the open time is shorter when it is hot and humid. The window must be set within the open time: never set glass on a bead that has skinned (wipe it off and start again). Cut the nozzle, load the gun, have the helper and the suction cups ready, and the tape marks visible. Start the clock when the first bead leaves the nozzle and aim to have the window set within 10 minutes.',
                    'Lay one <b>unbroken bead</b> all the way round on the surface the instructions give. Make it a triangle, tall enough that the window squashes it down to the height of the rubber blocks.',
                    '<b>Where it meets a block, step the bead around it and carry on.</b> No gaps: water finds them. See the drawing.',
                    'Where the bead goes exactly (on the frame band or on the flange) and how thick it must be are for Van Windows Direct to say. <b>I have not seen their sheet.</b>',
                ]) + '</ul>', fig_w4()))
    S.append(st(8, 'Set the window',
                '<ul>' + li([
                    'Two people, suction cups. Set the bottom edge on the blocks first, then tilt the top in, lining up the tape marks.',
                    'Press gently round the whole edge until the bead is squashed to the blocks&rsquo; height. Do not slide the window sideways: it smears the bead.',
                    'Check the gap again, then wipe off the squeeze-out right away.',
                ]) + '</ul>'))
    S.append(st(9, 'Tape it and let it cure',
                '<ul>' + li([
                    'Painter&rsquo;s tape from the frame to the body every 8 to 12 in. Leave it taped.',
                    'Keep the van still, do not slam the doors, and leave the doors cracked: humidity speeds the cure.',
                    'Drive-away for P2G Premium is <b>3 hours</b> on Sika&rsquo;s sheet, measured at 73 &deg;F and 50% humidity; it takes longer when it is cooler, so in the 60s give it longer (I would wait 6 hours or more) and keep the van still. Full cure takes longer: give it a day before the leak test.',
                ]) + '</ul>', fig_w5()))
    S.append(st(10, 'Fit the edge trim',
                '<ul>' + li([
                    'Trim-Lok (or similar edge molding) clips over the raw cut edge all the way round, as the sister listings recommend. Size it to the full circumference: measure your cut (about 14 ft for a window this size).',
                    'Tap it on with a rubber mallet, cut the ends square and tuck them out of sight. If it will not seat, remove the foam between the walls (step 4).',
                ]) + '</ul>', fig_w6()))
    S.append(st(11, 'Test, then finish',
                '<ul>' + li([
                    'After the full cure, remove the tape and the protective film. Run a garden hose over the window from low to high, with a helper inside with a light. Any drip: dry it, find it, add sealant, test again.',
                    'Check the slider, the latch and the screen.',
                    'Then adjust the wall cabinets and the dinette around it, as you said.',
                ]) + '</ul>'))

    mats = ['The window, and Sikaflex P2G (2 tubes, primer, wipes and swabs: check the kit and its version)',
            'Edge trim (Trim-Lok or similar), about 14 ft',
            'Rust-inhibiting primer and matching paint for the cut edge',
            'Painter&rsquo;s tape, plastic sheeting, isopropyl alcohol and rags, nitrile gloves',
            'Cutting: jigsaw, nibbler or air saw with fresh metal blades; drill and bits; files']
    tools = ['Two suction cups for glass (and a helper)',
             'Caulk gun, utility knife (to cut the nozzle)',
             'Rubber mallet for the edge trim; a small pick to dig out foam',
             'Glasses, gloves, hearing protection, vacuum',
             'Garden hose for the leak test']
    head = ('<h1>Side window: install steps</h1>'
            '<p class="lead">Van Windows Direct TL201-SE, a glue-in slider for the driver side forward position of a 2015+ Transit. <b>I could not find Van Windows Direct&rsquo;s own instruction sheet.</b> What I could confirm: the window&rsquo;s size and that it uses the factory stamping (retailer listings), the Sikaflex P2G kit and Trim-Lok (sister listings), and Sika&rsquo;s cure figures. The cutting, dry-fit and bead steps are general bonded-window practice, marked where a sheet would decide. Where their sheet would decide something, the step says so.</p>'
            '<div class="card warnbox"><h3 style="margin-top:0">Before you cut</h3><ul>'
            '<li><b>Get the instruction sheet</b> for the TL201-SE (check the box, or ask Van Windows Direct): the exact cut line, where the bead goes and how thick it is.</li>'
            '<li><b>The kit:</b> yours is P2G Premium (open time 15 minutes, drive-away 3 hours at 73 &deg;F). Sika says Premium needs no primer on the glass or its black band; the primer is for the painted body side.</li>'
            '<li><b>The open time is short:</b> 15 minutes. Cut and dry-fit first (done); do the bonding in one planned session with a helper.</li>'
            '<li><b>Weather:</b> cover the opening whenever you stop.</li></ul>'
            '<p class="swipe">On a phone, swipe a drawing sideways to see all of it.</p></div>'
            '<div class="card"><h3 style="margin-top:0">Where it goes in this van</h3><ul>'
            f'<li><b>Over the dinette, centered on the table.</b> The cutout (the slider frame&rsquo;s outline, {fr16(WIN_CW)} x {fr16(WIN_CH)} in) runs {fr16(WIN_CX0)} to {fr16(WIN_CX1)} in from the back mark and {fr16(WIN_CZ0)} to {fr16(WIN_CZ1)} in up. The glass ({fr16(WIN_GW)} x {fr16(WIN_GH)}) is bigger than the cutout: it ends {fr16(WIN_OL)} in left of it and {fr16(WIN_OB)} in below it, so on the outside it covers {fr16(WIN_GX0)} to {fr16(WIN_GX1)} in from the back and {fr16(WIN_GZ0)} to {fr16(WIN_GZ1)} in up.</li>'
            f'<li><b>Clearances inside:</b> the sill is {fr8(WIN_CZ0 - 29)} in over the table (29 up) and {fr8(WIN_CZ0 - 38)} in over the backrest tops (38 up); the top of the cutout is {fr16(CAB_BOT - WIN_CZ1)} in under the wall cabinet (its bottom is at {fr8(CAB_BOT)}).</li>'
            f'<li><b>This place is an assumption.</b> Your opening is already cut, but where it sits on the wall is not in the plan. Measure its edges from the back mark and the floor, and put the numbers in the Side window group on the interactive page, so the furring frame, the outlet and the drawings follow the real hole.</li>'
            f'<li><b>The seam:</b> the steel map shows a seam or pillar at about 98 in from the back, {fr16(WIN_CX0 - 98)} in left of the cutout. It runs under the left end of the glass, so the bead crosses it there: find it on the outside and seal it before the bead goes on.</li>'
            f'<li><b>Inside:</b> furring rails S5 and S6 stop at a frame of four pieces (J1 to J4) around the cutout, and the dinette outlet drops from 36 to 34 in up. See the build guide and the furring cut list.</li></ul></div>'
            '<div class="card"><div class="cols"><div><h3 style="margin-top:0">Materials</h3><ul class="chk">'
            + ''.join(f'<li><input type="checkbox" data-s="m{i}"><span>{m}</span></li>' for i, m in enumerate(mats)) +
            '</ul></div><div><h3 style="margin-top:0">Tools</h3><ul class="chk">'
            + ''.join(f'<li><input type="checkbox" data-s="t{i}"><span>{t}</span></li>' for i, t in enumerate(tools)) +
            '</ul></div></div></div>')
    key = 'van-window-ticks'
    js = ("<script>(function(){var K='" + key + "',s={};try{s=JSON.parse(localStorage.getItem(K)||'{}')||{};}catch(e){}"
          "document.querySelectorAll('input[data-s]').forEach(function(b){var k=b.dataset.s;b.checked=!!s[k];"
          "var c=b.closest('.card');if(c&&c.dataset.step&&b.checked)c.classList.add('done');"
          "b.addEventListener('change',function(){s[k]=b.checked;try{localStorage.setItem(K,JSON.stringify(s));}catch(e){}"
          "var c=b.closest('.card');if(c&&c.dataset.step)c.classList.toggle('done',b.checked);});});})();</script>")
    return ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Side window install steps</title><style>' + I.CSS + EXTRA_CSS + '</style></head><body><div class="wrap">' + head + ''.join(S) +
            '<p class="lead">Back to <a href="interactive.html">the interactive plan</a>, <a href="window-template.html">the window template</a>, <a href="install.html">the fan and A/C steps</a> or <a href="sides.html">the static diagrams</a>.</p>'
            '</div>' + js + '</body></html>')


if __name__ == '__main__':
    out = os.path.join(ROOT, 'window.html')
    open(out, 'w').write(build())
    print('window.html written,', os.path.getsize(out), 'bytes')
