#!/usr/bin/env python3
"""Builds ../window-template.html: the TL201-SE measured from the owner's tape photos (IMG_0045 to 0050, 0056),
drawn to scale from inside, with the cutout (frame outline) numbers for a cardboard template.
Every number is marked: read from a tape in a photo, estimated from the full photo, or still needed.
Run from this folder (build.sh does):  python3 wtemplate.py
"""
import os, html
import install as I
import window as W
from install import svg, R, L, C, T, P, PL, fr

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

# ---------------------------------------------------------------- the numbers, inches, origin at the glass bottom-left corner as seen from inside
GW, GH = 54.35, 29.12            # glass, from the retailer listing: not taped yet
TOP = 3.5                        # frame outer edge up to the glass top edge        IMG_0045  (tape)
BOT = 3.25                       # frame outer edge down to the glass bottom edge   IMG_0047  (tape, along a block)
RIGHT = 3.5                      # frame outer edge to the glass right edge         IMG_0050  (tape)
LEFT = 8.5                       # frame outer edge to the glass left edge          full photo (estimate, +-1)
FRIT = 7.5                       # black band ends at the dotted edge, from left    IMG_0046  (tape)
BLK_END = 8.75                   # right edge of the right block to the glass right edge   IMG_0048 (tape, +-1/2)
BLK_W, BLK_L = 1.75, BOT         # block width (estimate), length = frame edge to glass edge
BLK_C = [17.0, 30.5, 44.5]       # block centers from the left glass edge: full photo (estimate)
DIV = 28.0                       # slider divider from the left glass edge: full photo (estimate)
RG, RGL = 2.75, 0.4              # glass corner radius right side, left side: full photo (estimate)
RF, RFL = 2.0, 0.5               # frame corner radius right side, left side: full photo (estimate)

FX0, FX1 = LEFT, GW - RIGHT
FY0, FY1 = BOT, GH - TOP

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
.badge { fill: #fff; stroke: #222; stroke-width: 1.2; }
.tbadge { font-size: 10.5px; font-weight: 800; fill: #111; }
.chip { display: inline-block; border-radius: 10px; padding: 0 8px; font-size: 13px; font-weight: 700; color: #fff; }
.c-m { background: #1f6fb2; } .c-e { background: #b8651a; } .c-n { background: #8a2f2f; }
td.num { white-space: nowrap; font-weight: 700; }
"""


def rr(l, t, r, b, tl, tr, br, bl, cls):
    """rounded rect in pixels with a different radius on each corner"""
    d = (f'M {l + tl:.1f} {t:.1f} L {r - tr:.1f} {t:.1f} A {tr:.1f} {tr:.1f} 0 0 1 {r:.1f} {t + tr:.1f} '
         f'L {r:.1f} {b - br:.1f} A {br:.1f} {br:.1f} 0 0 1 {r - br:.1f} {b:.1f} '
         f'L {l + bl:.1f} {b:.1f} A {bl:.1f} {bl:.1f} 0 0 1 {l:.1f} {b - bl:.1f} '
         f'L {l:.1f} {t + tl:.1f} A {tl:.1f} {tl:.1f} 0 0 1 {l + tl:.1f} {t:.1f} Z')
    return f'<path d="{d}" class="{cls}"/>'


def fig_window():
    S = 11.5
    ox, oy = 76, 70
    X = lambda x: ox + x * S
    Y = lambda y: oy + (GH - y) * S
    o = []
    o.append(T(ox + GW * S / 2, 20, 'TL201-SE seen from inside (the side you photographed), to scale', 'tb'))
    # glass
    o.append(rr(X(0), Y(GH), X(GW), Y(0), RGL * S, RG * S, RG * S, RGL * S, 'panel'))
    # frame
    o.append(rr(X(FX0), Y(FY1), X(FX1), Y(FY0), RFL * S, RF * S, RF * S, RFL * S, 'frame2'))
    pad = 1.0
    o.append(rr(X(FX0 + pad), Y(FY1 - pad), X(DIV), Y(FY0 + pad), 0.6 * S, 0, 0, 0.6 * S, 'glassp'))
    o.append(rr(X(DIV), Y(FY1 - pad), X(FX1 - pad), Y(FY0 + pad), 0, 1.4 * S, 1.4 * S, 0, 'screen'))
    o.append(T(X((FX0 + DIV) / 2), Y((FY0 + FY1) / 2) + 4, 'glass', 'tdark'))
    o.append(T(X((DIV + FX1) / 2), Y((FY0 + FY1) / 2) + 4, 'screen', 'tdark'))
    # frit dots edge (tape reading from the left)
    o.append(L(X(FRIT), Y(FY1 + 1.2), X(FRIT), Y(FY0 - 1.2), 'fritl'))
    o.append(T(X(FRIT) - 3, Y(FY1 + 1.2) - 5, 'dots end', 'tm', 'end'))
    # blocks
    for i, c in enumerate(BLK_C):
        o.append(R(X(c - BLK_W / 2), Y(FY0), BLK_W * S, BLK_L * S - 2, 'blk', 2))
        o.append(T(X(c), Y(FY0) + 30, 'ABC'[i], 'tdark'))
    # measured margins (blue, solid)
    mx = 38.0
    o.append(L(X(mx), Y(GH) + 3, X(mx), Y(FY1) - 3, 'dimm'))
    o.append(T(X(mx) + 6, (Y(GH) + Y(FY1)) / 2 + 4, fr(TOP), 'tm', 'start'))
    my = 14.0
    o.append(L(X(FX1) + 3, Y(my), X(GW) - 3, Y(my), 'dimm'))
    o.append(T((X(FX1) + X(GW)) / 2, Y(my) - 6, fr(RIGHT), 'tm'))
    bx = 24.0
    o.append(L(X(bx), Y(FY0) + 3, X(bx), Y(0) - 3, 'dimm'))
    o.append(T(X(bx) + 6, (Y(FY0) + Y(0)) / 2 + 4, fr(BOT), 'tm', 'start'))
    # right block to the right edge (tape)
    c3r = BLK_C[2] + BLK_W / 2
    o.append(L(X(c3r) + 2, Y(1.5), X(GW) - 3, Y(1.5), 'dimm'))
    o.append(T((X(c3r) + X(GW)) / 2, Y(1.5) - 5, fr(BLK_END), 'tm'))
    # estimated (orange, dashed)
    ey = 20.0
    o.append(L(X(0) + 3, Y(ey), X(FX0) - 3, Y(ey), 'dime'))
    o.append(T(X(FX0 / 2), Y(ey) - 6, '~' + fr(LEFT), 'te'))
    for c in BLK_C:
        o.append(T(X(c), Y(0) + 17, '~' + fr(c), 'te'))
        o.append(L(X(c), Y(0), X(c), Y(0) + 5, 'dime'))
    o.append(T(X(DIV), Y(FY1) - 6, 'divider ~' + fr(DIV), 'te'))
    # photo badges: where each tape was
    for n, bx_, by_ in ((45, mx - 3, GH - 1.2), (46, 2.5, 12), (47, bx - 3, 1.6), (50, GW - 1.75, 19.0)):
        o.append(C(X(bx_), Y(by_), 11, 'badge'))
        o.append(T(X(bx_), Y(by_) + 3.5, str(n % 100).zfill(2), 'tbadge'))
    o.append(L(X(50.5), Y(1.5), X(50.5), Y(0) + 12, 'dimm'))
    o.append(C(X(50.5), Y(0) + 22, 11, 'badge'))
    o.append(T(X(50.5), Y(0) + 25.5, '48', 'tbadge'))
    # overall dimensions (from the listing)
    o.append(L(X(0), oy - 18, X(GW), oy - 18, 'dim'))
    o.append(L(X(0), oy - 22, X(0), oy - 14, 'dim'))
    o.append(L(X(GW), oy - 22, X(GW), oy - 14, 'dim'))
    o.append(T(X(GW / 2), oy - 23, fr(GW) + ' (listing, not taped yet)', 'tdim'))
    o.append(L(ox - 16, Y(GH), ox - 16, Y(0), 'dim'))
    o.append(L(ox - 20, Y(GH), ox - 12, Y(GH), 'dim'))
    o.append(L(ox - 20, Y(0), ox - 12, Y(0), 'dim'))
    o.append(f'<text x="{ox - 22}" y="{(Y(GH) + Y(0)) / 2}" class="tdim" text-anchor="middle" transform="rotate(-90 {ox - 22} {(Y(GH) + Y(0)) / 2})">{fr(GH)} (listing)</text>')
    # origin
    o.append(C(X(0), Y(0), 4, 'drill'))
    o.append(T(X(0), Y(0) + 34, '0,0', 'tsm', 'middle'))
    # legend
    ly = Y(0) + 56
    o.append(L(ox, ly, ox + 40, ly, 'dimm'))
    o.append(T(ox + 48, ly + 4, 'read from a tape in your photo', 'tsm', 'start'))
    o.append(L(ox + 240, ly, ox + 280, ly, 'dime'))
    o.append(T(ox + 288, ly + 4, 'estimated from the full photo (+-1 in)', 'tsm', 'start'))
    o.append(C(ox + 3, ly + 22, 9, 'badge'))
    o.append(T(ox + 3, ly + 25.5, '45', 'tbadge'))
    o.append(T(ox + 18, ly + 26, 'IMG number of the photo each tape reading came from', 'tsm', 'start'))
    return svg(760, int(ly + 40), ''.join(o), 'The TL201-SE from inside, to scale: glass, frame, three blocks and the measured margins')


def fig_cut():
    """just the cutout and the glass outline as the cardboard template: the frame outline relative to the glass"""
    S = 11.0
    ox, oy = 50, 40
    X = lambda x: ox + x * S
    Y = lambda y: oy + (GH - y) * S
    o = []
    o.append(rr(X(0), Y(GH), X(GW), Y(0), RGL * S, RG * S, RG * S, RGL * S, 'flange'))
    o.append(rr(X(FX0), Y(FY1), X(FX1), Y(FY0), RFL * S, RF * S, RF * S, RFL * S, 'cutline'))
    o.append(T(X((FX0 + FX1) / 2), Y((FY0 + FY1) / 2) - 2, 'cut this out of the cardboard', 'tb'))
    o.append(T(X((FX0 + FX1) / 2), Y((FY0 + FY1) / 2) + 16, fr(FX1 - FX0) + ' wide x ' + fr(FY1 - FY0) + ' tall (draft)', 'tgrey'))
    o.append(T(X(GW / 2), Y(GH) - 8, 'glass outline = the cardboard&#39;s outer edge'.replace('&#39;', "'"), 'tsm'))
    for c in BLK_C:
        o.append(R(X(c - BLK_W / 2), Y(FY0), BLK_W * S, BLK_L * S - 2, 'blk', 2))
    o.append(T(X(GW / 2), Y(0) + 20, 'Dashed red: the opening to cut. Grey: the three blocks,', 'tsm'))
    o.append(T(X(GW / 2), Y(0) + 36, 'marked so you can check that the stamping clears them.', 'tsm'))
    return svg(700, int(Y(0) + 50), ''.join(o), 'The cardboard template: glass outline with the frame opening cut out and the three blocks marked')


def row(item, val, tag, src):
    chip = {'m': '<span class="chip c-m">tape</span>', 'e': '<span class="chip c-e">estimate</span>', 'n': '<span class="chip c-n">needed</span>'}[tag]
    return f'<tr><td>{item}</td><td class="num">{val}</td><td>{chip}</td><td>{src}</td></tr>'


def build():
    rows = [
        row('Glass overall, across x up', f'{fr(GW)} x {fr(GH)}', 'n', 'retailer listing: tape it, edge to outer edge'),
        row('Frame top edge to glass top edge', fr(TOP), 'm', 'IMG_0045'),
        row('Frame bottom edge to glass bottom edge, along a block', fr(BOT), 'm', 'IMG_0047 (to the face edge; 3 7/16 to the outer edge of the glass)'),
        row('Frame right edge to glass right edge', fr(RIGHT), 'm', 'IMG_0050 (T-square held to the frame, tape to the glass)'),
        row('Right block, its far edge to the glass right edge', fr(BLK_END), 'm', 'IMG_0048 (reading 8 3/4, hook on the block&rsquo;s edge, about 1/2 in either way)'),
        row('Black band, glass edge to where the dots end', fr(FRIT), 'm', 'IMG_0046 (assumed the left edge: please confirm which edge)'),
        row('Frame left edge to glass left edge', '~' + fr(LEFT) + ' (7 1/2 to 9 1/2)', 'n', 'full photo only; tape it'),
        row('Frame outer width x height', f'~{fr(FX1 - FX0)} x {fr(FY1 - FY0)}', 'n', 'worked out from the margins above; tape it across the frame&rsquo;s outer lips'),
        row('Block centers from the left edge', '~' + ', '.join(fr(c) for c in BLK_C), 'n', 'full photo only'),
        row('Block size', f'~{fr(BLK_W)} wide x {fr(BLK_L)} long', 'n', 'width from the full photo; length is the frame-to-edge gap'),
        row('Slider divider from the left edge', '~' + fr(DIV), 'n', 'full photo only'),
        row('Corner radii: glass right / left, frame right / left', f'~{fr(RG)} / {fr(RGL)}, ~{fr(RF)} / {fr(RFL)}', 'n', 'full photo only; a radius gauge or a compass will settle it'),
    ]
    todo = [
        '<b>The glass, edge to edge:</b> across the bottom and up one side. I used the listing&rsquo;s 54 3/8 x 29 1/8.',
        '<b>The frame, outer lip to outer lip:</b> across and up. Also tape its left edge to the glass left edge: that is the one margin I could only estimate.',
        '<b>Which edge each photo was:</b> I took 0045 as the top, 0047 and 0048 as the bottom with the blocks, 0050 as the right (top right corner), and 0046 as the left. Tell me where I am wrong.',
        '<b>The blocks:</b> tape from the glass left edge to the middle of each, then each one&rsquo;s width and length.',
        '<b>How far the frame sits proud of the glass</b> (its depth toward the inside): that decides how much room the cutout has behind it.',
        '<b>The van:</b> the same opening, measured on the stamping: width, height and corner radius. The template is only useful once you can compare the two.',
    ]
    steps = [
        'Cardboard (or thin ply) a little over <b>54 3/8 x 29 1/8</b>. Mark the glass outline from one bottom corner, round the two right corners at about <b>2 3/4 in</b> and the left ones at about <b>3/8 in</b>.',
        f'Mark the opening: its left edge <b>{fr(FX0)}</b> in from the left, right edge <b>{fr(FX1)}</b> (that is {fr(RIGHT)} in from the right), bottom edge <b>{fr(FY0)}</b> up from the bottom, top edge <b>{fr(FY1)}</b> (that is {fr(TOP)} in down from the top). Round its right corners at about <b>2 in</b>.',
        f'Mark the three blocks on the bottom band, {fr(BLK_W)} wide and {fr(BLK_L)} long, centered about <b>{", ".join(fr(c) for c in BLK_C)}</b> in from the left.',
        'Cut out the opening. Test it against the window (the frame should drop in with the cardboard sitting on the glass face) and fix any number that does not match.',
        '<b>Seen from outside the van the drawing is a mirror image:</b> flip the cardboard over, or turn the numbers around, before you trace.',
        'Hold it on the van: the glass outline must sit inside the stamping&rsquo;s recess with margin all round, and the opening must clear the stamping&rsquo;s inner edge. Then trace and use it as the cut line, once the numbers are confirmed.',
    ]
    head = ('<h1>Side window: template</h1>'
            '<p class="lead">Drawn from your tape photos (IMG_0045 to 0050) and the full picture (0056). Blue numbers were read off a tape in a photo, orange ones are my estimate from the full picture, and the rest still need a tape. '
            'The window is a big black glass panel with the slider frame bonded in it, and three blocks along the bottom edge. The frame is what goes through the van&rsquo;s opening, so its outline is the cut.</p>'
            '<div class="card warnbox"><h3 style="margin-top:0">This is a draft</h3>'
            '<p style="margin:0">The margins at the top, bottom and right are tape readings, good to about 1/8 in. The left margin, the frame&rsquo;s overall size, the block spots and the corner radii are estimates. '
            '<b>Do not cut the van from this yet.</b> Confirm the orange numbers first, and check the template against the stamping.</p>'
            '<p class="swipe">On a phone, swipe a drawing sideways to see all of it.</p></div>'
            '<div class="card"><div class="figwrap">' + fig_window() + '</div></div>'
            '<div class="card"><h2>The numbers</h2><div class="figwrap"><table style="min-width:560px"><tr><th>What</th><th>Inches</th><th></th><th>From</th></tr>' + ''.join(rows) + '</table></div></div>'
            '<div class="card"><h2>The cardboard template</h2><div class="figwrap">' + fig_cut() + '</div><ol>' + I.li(steps) + '</ol></div>'
            '<div class="card"><h2>What to confirm, and what to measure</h2><ul>' + I.li(todo) + '</ul></div>')
    key = 'van-window-template'
    page = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">'
            '<title>Side window template</title><style>' + I.CSS + EXTRA + '</style></head><body><div class="wrap">' + head +
            '<p class="lead">Back to <a href="window.html">the side window steps</a>, <a href="interactive.html">the interactive plan</a> or <a href="sides.html">the static diagrams</a>.</p>'
            '</div></body></html>')
    return page


if __name__ == '__main__':
    out = os.path.join(ROOT, 'window-template.html')
    open(out, 'w').write(build())
    print('window-template.html written,', os.path.getsize(out), 'bytes')
