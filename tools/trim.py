"""Seven drawings of how the corners and edges of the 3/8 in plywood walls are finished: sheet joints, inside corners, outside corners, visible plywood edges,
the side window reveal, the top edge at the ceiling and the floor edge. Each is a section drawn to scale from the numbers in the build guide's trim table.
Used by buildguide.py (the Walls page); run on its own it writes ../trim.html for a quick look."""
import os

INK = '#2C2C2A'; PLY = '#E8CF9C'; PLYD = '#B8975A'; HARD = '#C9A263'; STEEL = '#9AA0A8'; FURR = '#7A4A1E'; SEAL = '#4F8C74'; LED = '#F2B84B'
RED = '#A32D2D'; BLU = '#185FA5'; BLK = '#2A2A2A'; GRY = '#D8D8D4'

def _r(x, y, w, h, fill, stroke=INK, sw=1.1, extra=''):
    return f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def _p(pts, fill, stroke=INK, sw=1.1, extra=''):
    return '<polygon points="' + ' '.join(f'{x:.1f},{y:.1f}' for x, y in pts) + f'" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" {extra}/>'
def _l(x1, y1, x2, y2, col=INK, sw=1, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{col}" stroke-width="{sw}"{d}/>'
def _t(x, y, s, sz=12, anchor='start', col=INK, w=400):
    return f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" style="font-size:{sz}px;font-weight:{w};fill:{col};paint-order:stroke;stroke:#fff;stroke-width:3px;stroke-linejoin:round">{s}</text>'
def _call(x, y, tx, ty, s, anchor='start', col=INK):
    """a label with a leader line from the label to the point (x, y)"""
    return _l(tx + (3 if anchor == 'start' else -3), ty, x, y, col, 1) + f'<circle cx="{x:.1f}" cy="{y:.1f}" r="2.2" fill="{col}"/>' + _t(tx + (8 if anchor == 'start' else -8), ty + 4, s, 12, anchor, col)
def _plies(x, y, w, h, n=5, vertical=False):
    """the layers of a plywood section: thin lines parallel to the faces"""
    o = []
    for i in range(1, n):
        if vertical: o.append(_l(x + w * i / n, y, x + w * i / n, y + h, PLYD, .8))
        else: o.append(_l(x, y + h * i / n, x + w, y + h * i / n, PLYD, .8))
    return ''.join(o)
def _svg(w, h, body, title):
    return f'<svg viewBox="0 0 {w} {h}" role="img" style="width:100%;height:auto;display:block;background:#fff;border-radius:6px"><title>{title}</title>{body}</svg>'

# ---- 1  sheet joints: a section along the wall at a joint, the aisle at the top -------------------------------------------------
def fig_joint():
    S = 64; o = []; a = o.append
    def half(x0, chamfer, batten):
        yT, yB = 120, 144
        a(_r(x0, yB, 288, .75 * S, FURR, INK, 1.1)); a(_l(x0, yB, x0 + 288, yB, '#000', 1.6))                     # the strip, and the glue line
        L = [(x0, yT), (x0 + 142 - (4 if chamfer else 0), yT)] + ([(x0 + 142, yT + 4)] if chamfer else []) + [(x0 + 142, yB), (x0, yB)]
        R = ([(x0 + 146, yT + 4), (x0 + 150, yT)] if chamfer else [(x0 + 146, yT)]) + [(x0 + 288, yT), (x0 + 288, yB), (x0 + 146, yB)]
        a(_p(L, PLY)); a(_p(R, PLY)); a(_plies(x0, yT, 142, 24)); a(_plies(x0 + 146, yT, 142, 24))
        if batten: a(_r(x0 + 144 - 48, yT - 16, 96, 16, HARD))
        return yT, yB
    half(20, True, False); half(330, False, True)
    a(_t(20, 28, 'A  V joint: 1/16 in gap, 1/16 in chamfer', 14, 'start', INK, 700)); a(_t(330, 28, 'B  batten over the joint', 14, 'start', INK, 700))
    a(_call(166, 122, 130, 80, '1/16 chamfer on both edges', 'start')); a(_call(164, 144, 108, 218, '1/16 gap', 'start'))
    a(_call(60, 132, 30, 58, '3/8 plywood sheets', 'start')); a(_call(100, 168, 60, 250, 'furring strip 3/4 x 1 1/2, glue and screw', 'start'))
    a(_call(474, 106, 520, 70, 'batten 1/4 x 1 1/2', 'start')); a(_call(474, 144, 520, 218, '1/16 gap under it', 'start'))
    a(_t(20, 276, 'aisle side at the top, the van wall at the bottom; the strips run sideways behind the joint', 11.5, 'start', '#5F5E5A'))
    return _svg(760, 290, ''.join(o), 'Sheet joint: V joint and batten')

# ---- 2  inside corner: a plan section where a sheet meets a floor-to-ceiling wall ----------------------------------------------
def fig_inside():
    S = 64; o = []; a = o.append
    def side(x0, sealant):
        yT = 130; xp = x0 + 200
        a(_r(x0, yT + 24, 200, 48, FURR)); a(_l(x0, yT + 24, xp, yT + 24, '#000', 1.6))                              # the strip behind the sheet
        a(_r(x0, yT, 196, 24, PLY)); a(_plies(x0, yT, 196, 24))                                                       # the sheet stops 1/16 short
        a(_r(xp, 30, 48, 66 + 24, PLY)); a(_plies(xp, 30, 48, 90, 5, True))                                          # the 3/4 wall, standing out from the wall
        if sealant: a(_p([(xp - 26, yT), (xp, yT), (xp, yT - 26)], SEAL, '#2F5E3F', 1)); a(_r(xp - 4, yT, 4, 24, SEAL, SEAL, .5))
        else: a(_r(xp - 48, yT - 48, 48, 48, HARD))
        return xp, yT
    xp, yT = side(20, False); xq, _ = side(330, True)
    a(_t(20, 24, 'A  3/4 x 3/4 in hardwood strip', 14, 'start', INK, 700)); a(_t(330, 24, 'B  flexible sealant line', 14, 'start', INK, 700))
    a(_call(xp - 24, yT - 24, 60, 70, 'corner strip, glued and pinned', 'start')); a(_call(xp + 24, 60, xp + 40, 52, '3/4 in wall (W1 to W4)', 'start'))
    a(_call(xp - 2, yT + 12, 150, 232, '1/16 gap, covered by the strip', 'start')); a(_call(60, yT + 12, 40, 214, '3/8 sheet', 'start'))
    a(_call(xq - 13, yT - 8, 370, 70, 'flexible sealant, color matched', 'start', '#2F5E3F'))
    a(_t(20, 276, 'a plan view from above: the van wall at the bottom, the 3/4 wall standing out of it toward the top', 11.5, 'start', '#5F5E5A'))
    return _svg(760, 290, ''.join(o), 'Inside corner: hardwood strip or sealant')

# ---- 3  outside corner: the wheel well box, the end of a closet wall --------------------------------------------------------------
def fig_outside():
    o = []; a = o.append
    cx0, cy1 = 150, 206                       # the box's outer corner
    a(_r(cx0, 40, 250, cy1 - 40, GRY, INK, 1.1)); a(_t(cx0 + 125, 120, 'box (wheel well, closet, shower wall)', 12, 'middle', '#5F5E5A'))
    a(_r(cx0 - 24, 40, 24, cy1 - 40 - 72, PLY)); a(_plies(cx0 - 24, 40, 24, cy1 - 40 - 72, 5, True))               # the sheet on the left face stops at the post
    a(_r(cx0 + 72, cy1, 328 - 72, 24, PLY)); a(_plies(cx0 + 72, cy1, 328 - 72, 24))                                 # the sheet on the bottom face starts after the post
    post = 'M %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f L %.1f %.1f Q %.1f %.1f %.1f %.1f Z' % (cx0 - 24, cy1 - 72, cx0 + 72, cy1 - 72, cx0 + 72, cy1 + 24, cx0 - 24 + 8, cy1 + 24, cx0 - 24, cy1 + 24 - 8, cx0 - 24, cy1 + 24, cx0 - 24 + 8, cy1 + 24)
    a(f'<path d="M {cx0-24} {cy1-72} L {cx0+72} {cy1-72} L {cx0+72} {cy1+24} L {cx0} {cy1+24} Q {cx0-24} {cy1+24} {cx0-24} {cy1} Z" fill="{HARD}" stroke="{INK}" stroke-width="1.1"/>')
    a(_call(cx0 + 24, cy1 - 24, 420, 84, 'corner post 1 1/2 x 1 1/2, glued, pinned', 'start')); a(_call(cx0 - 18, cy1 + 14, 40, 262, 'outer edge rounded 1/8 in', 'start'))
    a(_call(cx0 - 12, 100, 30, 70, '3/8 sheet, its end edge hidden', 'start')); a(_call(cx0 + 220, cy1 + 12, 330, 262, '3/8 sheet, its end edge hidden', 'start'))
    a(_t(20, 24, 'Outside corner, seen from above', 14, 'start', INK, 700)); a(_t(420, 130, 'sheets stop at the post', 12, 'start', '#5F5E5A'))
    return _svg(760, 290, ''.join(o), 'Outside corner with a hardwood post')

# ---- 4  visible plywood edge: iron-on veneer tape -----------------------------------------------------------------------------------
def fig_edge():
    o = []; a = o.append
    def sheet(y, tape, trimmed):
        a(_r(40, y, 300, 120, PLY)); a(_plies(40, y, 300, 120, 5))                                                    # a 3/8 sheet seen from the side, 320 px per inch
        if tape:
            ov = 0 if trimmed else 20
            a(_r(340, y - ov, 12, 120 + 2 * ov, '#E9D8B4', '#8A6B4D', 1))
    sheet(40, False, False); sheet(40, True, False)
    a(_t(40, 24, 'A  iron on the 1/2 in tape (it overhangs 1/16 in each side)', 13, 'start', INK, 700))
    sheet(206, True, True)
    a(_t(40, 196, 'B  trim it flush, sand with 220 grit, finish', 13, 'start', INK, 700))
    a(_call(346, 100, 420, 90, 'birch veneer tape, 0.5 mm, pre-glued', 'start')); a(_call(346, 40, 420, 40, '1/16 overhang', 'start'))
    a(_call(200, 100, 420, 130, '3/8 plywood, five layers', 'start')); a(_call(346, 266, 420, 266, 'edge now smooth and sealed', 'start'))
    a(_t(40, 350, 'enlarged: the sheet is 3/8 in thick, the tape 1/2 in wide; trim with an edge trimmer or a sharp chisel held flat', 11.5, 'start', '#5F5E5A'))
    return _svg(760, 362, ''.join(o), 'Iron-on edge tape')

# ---- 5  the side window reveal: a section across a jamb --------------------------------------------------------------------------------
def fig_window():
    S = 36; o = []; a = o.append
    xc = 330; ySt = 300                                                                                                    # the opening's edge, and the steel's inner face
    a(_r(20, ySt, xc - 20, 9, STEEL)); a(_t(24, ySt + 26, 'van body steel (the cutout is to the right)', 12, 'start', '#5F5E5A'))
    blk = 3.625 * S; fy = ySt - blk                                                                                         # spacer block 3 5/8
    a(_r(xc - 54, fy, 54, blk, '#5A2E0A', '#fff', 1)); a(_r(xc - 54, fy - .75 * S, 54, .75 * S, FURR))                    # block and the jamb J1 (3/4 x 1 1/2)
    sh = fy - .75 * S - .375 * S
    a(_r(20, sh, xc - 20, .375 * S, PLY)); a(_plies(20, sh, xc - 20, .375 * S))                                            # the 3/8 sheet ends at the opening
    a(_r(xc, sh, .25 * S, ySt - sh, '#D9B777'))                                                                           # the 1/4 liner on the reveal
    tr = sh - .75 * S; a(_r(xc - 45, tr, 54, .75 * S, HARD))                                                              # picture-frame trim 3/4 x 1 1/2
    a(_r(xc + 9, ySt - 30, 40, 38, BLK)); a(_t(xc + 56, ySt - 6, 'window frame', 12, 'start', INK))
    a(_call(xc + 22, ySt + 4, xc + 70, ySt + 40, '1/8 gap, sealed', 'start', SEAL))
    a(_call(xc - 20, tr + 14, xc + 70, tr - 20, 'picture-frame trim 3/4 x 1 1/2', 'start'))
    a(_call(xc + 4, (sh + ySt) / 2 - 40, xc + 70, 150, 'liner 1/4 in, lines the reveal', 'start'))
    a(_call(120, sh + 7, 40, 90, '3/8 sheet, edge covered', 'start')); a(_call(xc - 28, fy - 12, 60, 150, 'jamb J1, 3/4 x 1 1/2', 'start'))
    a(_call(xc - 28, fy + blk / 2, 60, 200, 'spacer block 3 5/8 in', 'start', '#5A2E0A'))
    a(_t(20, 24, 'Side window: a section across the jamb (aisle at the top)', 14, 'start', INK, 700))
    return _svg(760, 362, ''.join(o), 'Side window reveal and trim')

# ---- 6  the top edge at the ceiling: a section looking along the wall, the wall at the left ------------------------------------------
def fig_top():
    import math
    o = []; a = o.append
    lean = math.tan(math.radians(5)); yCe = 70; xt = 170; h = 150                                                          # the ceiling plywood's underside, the wall face at the ceiling, the part of the wall drawn
    a(_r(xt - 40, yCe - 7.5, 560, 7.5, '#D9C7A5', '#8A6B4D', 1)); a(_t(xt + 330, yCe - 14, '3/16 ceiling plywood', 12, 'start', '#5F5E5A'))
    a(_r(xt + 60, yCe, 300, 30, '#DDC397', '#8A6B4D', 1)); a(_t(xt + 370, yCe + 20, 'cedar slat 3/4', 12, 'start', '#5F5E5A'))
    a(_p([(xt - 15, yCe), (xt, yCe), (xt - h * lean, yCe + h), (xt - 15 - h * lean, yCe + h)], PLY))                       # the wall sheet leans in toward the right as it rises
    tw, th = 30, 60
    a(_p([(xt, yCe), (xt + tw, yCe), (xt + tw, yCe + th), (xt - th * lean, yCe + th)], HARD, INK, 1.2))                   # the trim: 3/4 along the ceiling, 1 1/2 down the wall, back edge ripped to the lean
    cx = xt + tw - 22; cy = yCe + th + 2
    a(_r(cx, cy, 22, 11, '#B9BCC2', INK, 1)); a(_r(cx + 4, cy + 7, 14, 3, LED, '#8A5A00', .6))
    a(_p([(cx + 4, cy + 10), (cx + 18, cy + 10), (cx + 40, cy + 52), (cx - 18, cy + 52)], '#FFE9A8', 'none', 0, 'fill-opacity=".6"'))
    a(_call(xt + tw / 2, yCe + 30, 330, 170, 'trim 3/4 x 1 1/2, back edge ripped to the 5 degree lean', 'start'))
    a(_call(cx + 11, cy + 6, 330, 214, 'LED strip in an aluminum channel', 'start', '#8A5A00'))
    a(_call(xt - 40, yCe + 60, 40, 150, '3/8 wall sheet, leaning in 5 degrees', 'start')); a(_call(xt + 12, yCe - 3, 20, 44, 'screwed to the ceiling blocking, not to the sheet', 'start'))
    a(_t(20, 24, 'Top edge at the ceiling: a section along the wall (the wall on the left)', 14, 'start', INK, 700))
    return _svg(760, 300, ''.join(o), 'Top edge trim with the LED strip')

# ---- 7  the floor edge: a section looking along the wall --------------------------------------------------------------------------------
def fig_floor():
    o = []; a = o.append
    xw = 190; yF = 210
    a(_r(xw - 90, yF, 560, 30, '#B9A58A', INK, 1.1)); a(_t(xw + 120, yF + 52, 'floor: subfloor and flooring (free to move)', 12, 'start', '#5F5E5A'))
    a(_r(xw - 22, 40, 22, yF - 10 - 40, PLY, INK, 1.1)); a(_plies(xw - 22, 40, 22, yF - 10 - 40, 5, True))               # the sheet stops 1/4 in above the floor
    a(_r(xw - 52, 40, 30, yF - 40, FURR, INK, 1))                                                                         # the strip behind
    a(f'<path d="M {xw} {yF-2-30} Q {xw+30} {yF-2-30} {xw+30} {yF-2} L {xw} {yF-2} Z" fill="{HARD}" stroke="{INK}" stroke-width="1.2"/>')   # the quarter round, 1/16 above the floor
    a(_call(xw - 11, yF - 5, 330, 80, 'sheet 1/4 in off the floor: no wicking', 'start')); a(_call(xw + 10, yF - 12, 330, 126, 'quarter round 3/4 in, fixed to the wall with brads', 'start'))
    a(_call(xw + 20, yF - 1, 330, 172, '1/16 in clear of the floor, so it can move', 'start', RED))
    a(_t(20, 24, 'Floor edge: a section along the wall (the wall on the left)', 14, 'start', INK, 700))
    return _svg(760, 290, ''.join(o), 'Floor edge with a quarter round')

FIGS = [
    ('1', 'Sheet joints', fig_joint, 'Leave the 1/16 in gap and ease both edges with a 1/16 in chamfer so each joint reads as a clean V line, or hide the joint under a 1/4 x 1 1/2 in hardwood batten.'),
    ('2', 'Inside corners', fig_inside, 'Where a sheet meets a floor-to-ceiling wall (W1 to W4), the rear door frame or the cab end: stop the sheet 1/16 in short and glue a 3/4 x 3/4 in hardwood strip into the corner, or run a flexible sealant line.'),
    ('3', 'Outside corners', fig_outside, 'The wheel well box and the ends of the closet, shower and counter walls: a solid hardwood corner post that the sheets stop against, with the outer edges rounded 1/8 in.'),
    ('4', 'Visible plywood edges', fig_edge, 'The sliding door opening, shelf and nook edges: iron on 1/2 in birch veneer tape, trim it flush and sand it, then finish it with the sheets.'),
    ('5', 'The side window', fig_window, 'The cutout is framed with J1 to J4 behind the sheet; line the reveal with 1/4 in strips and mitre a 3/4 x 1 1/2 in picture-frame trim over the sheet\'s cut edge.'),
    ('6', 'The top edge at the ceiling', fig_top, 'A 3/4 x 1 1/2 in hardwood strip covers the sheet\'s top edge and the 1 1/2 in gap beside the slats; its back edge is ripped to the lean and the LED strip sits in a channel behind its lower edge.'),
    ('7', 'The bottom edge at the floor', fig_floor, 'Keep the sheet 1/4 in off the floor and fix a 3/4 in quarter round to the wall, with 1/16 in under it, so the floor can move.')]

CSS = '''<style>.trimgrid{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(100%,420px),1fr));gap:16px;margin:12px 0}
.trimgrid figure{margin:0;border:1px solid #d9d5ca;border-radius:8px;padding:10px;background:#fff;min-width:0}
.trimgrid figcaption{font-size:14px;line-height:1.45;margin-top:8px;color:#26241f}.trimgrid figcaption b{font-size:15px}</style>'''

def trim_html():
    return CSS + '<div class="trimgrid">' + ''.join(f'<figure>{fn()}<figcaption><b>{n}. {name}.</b> {cap}</figcaption></figure>' for n, name, fn, cap in FIGS) + '</div>'

if __name__ == '__main__':
    out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'trim.html')
    open(out, 'w', encoding='utf-8').write('<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Corners and edges</title><body style="font:16px/1.5 system-ui;max-width:1100px;margin:0 auto;padding:16px;background:#fbfaf7">' + trim_html())
    print('wrote', out)
