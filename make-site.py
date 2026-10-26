#!/usr/bin/env python3
"""Rebuild the site/ folder that gets uploaded to the website.

site/index.html        the home page: a card for every page below
site/interactive.html  the adjustable plan
site/diagrams.html     copy of sides.html (the static diagrams, photos and measurement tables)
site/install.html      the illustrated fan and A/C steps
site/window.html       the illustrated side window steps
site/window-template.html  the measured window and its cardboard template
site/wall-map.html     the wall marking map
site/electric.html     the electrical and lighting layout
site/interior.html     the 3D view of the inside of the van
Every page gets the same navigation bar across the top and a noindex tag (search engines are asked to leave the site alone).
site/photos/driver/    the driver side photos with all metadata (GPS location, camera, date) removed;
                       only the orientation tag is kept, so the pictures still turn the right way up
Run from this folder:  python3 make-site.py
"""
import glob, os, shutil, struct

HERE = os.path.dirname(os.path.abspath(__file__))
SITE = os.path.join(HERE, 'site')


def orientation(b):
    i = b.find(b'Exif\x00\x00')
    if i < 0:
        return None
    t = b[i + 6:]
    e = '<' if t[:2] == b'II' else '>'
    off = struct.unpack(e + 'I', t[4:8])[0]
    n = struct.unpack(e + 'H', t[off:off + 2])[0]
    for k in range(n):
        tag = struct.unpack(e + 'H', t[off + 2 + 12 * k:off + 4 + 12 * k])[0]
        if tag == 0x0112:
            return struct.unpack(e + 'H', t[off + 10 + 12 * k:off + 12 + 12 * k])[0]
    return None


def strip(b):
    o = orientation(b)
    out = [b[:2]]
    i = 2
    while b[i] == 0xFF and b[i + 1] != 0xDA:
        n = struct.unpack('>H', b[i + 2:i + 4])[0]
        if b[i + 1] != 0xE1:          # drop every APP1 segment (EXIF and XMP)
            out.append(b[i:i + 2 + n])
        i += 2 + n
    out.append(b[i:])
    if o and o != 1:                  # keep just the orientation
        tiff = b'MM\x00\x2A' + struct.pack('>I', 8) + struct.pack('>H', 1) + struct.pack('>HHIHH', 0x0112, 3, 1, o, 0) + struct.pack('>I', 0)
        seg = b'Exif\x00\x00' + tiff
        out.insert(1, b'\xFF\xE1' + struct.pack('>H', len(seg) + 2) + seg)
    return b''.join(out)


shutil.rmtree(SITE, ignore_errors=True)
os.makedirs(os.path.join(SITE, 'photos', 'driver'))
for f in sorted(glob.glob(os.path.join(HERE, 'photos', 'driver', '*.jpg'))):
    data = strip(open(f, 'rb').read())
    assert b'GPS' not in data, f
    open(os.path.join(SITE, 'photos', 'driver', os.path.basename(f)), 'wb').write(data)
import re, sys
sys.path.insert(0, os.path.join(HERE, 'tools'))
import buildguide
PAGES = [('index.html', 'Home', 'Start here: every page in one place.'),
         ('build/index.html', 'Build guide', 'Every part of the build on its own page, from the first thing to do to the last, with the drawings, the numbers and the steps.'),
         ('interactive.html', 'Plan', 'The adjustable plan: drag things around, open the doors, and see right away what does not fit.'),
         ('diagrams.html', 'Diagrams', 'The static diagrams of both walls, the bed, the ceiling and the roof, the photos and every measurement.'),
         ('interior.html', '3D view', 'Walk around the inside of the van in 3D: light wood stain walls and cabinets, a medium grey countertop, and a light grey plywood ceiling under light wood planks.'),
         ('wall-map.html', 'Wall map', 'The steel and the furring strips on each wall with every item almost transparent on top, to mark the walls from.'),
         ('electric.html', 'Electrical', 'The electrical and lighting layout: one-line diagram, outlets, switches and lights on each wall, the ceiling plan and the load table.'),
         ('install.html', 'Fan and A/C', 'Step by step with drawings: cutting, framing and mounting the roof fan and the air conditioner.'),
         ('window.html', 'Side window', 'Step by step with drawings: installing the side window.'),
         ('window-template.html', 'Window template', 'The side window measured from the photos, with the cutout numbers for a cardboard template.')]
NAV_CSS = ('<style>.vannav{display:flex;flex-wrap:wrap;gap:4px 6px;align-items:center;margin:0;padding:8px max(12px,env(safe-area-inset-left,0px));'
           'font:14px/1.3 -apple-system,"Segoe UI",system-ui,sans-serif;background:#f3f1ea;border-bottom:1px solid #cfcbbd;color:#26241f}'
           '.vannav a{color:#185FA5;text-decoration:none;padding:4px 9px;border-radius:14px;white-space:nowrap}'
           '.vannav a:hover{background:#e3e0d4}.vannav a[aria-current=page]{background:#26241f;color:#fff;font-weight:600}'
           '@media (prefers-color-scheme:dark){.vannav{background:#26241f;border-bottom-color:#4a473e;color:#ece9e0}.vannav a{color:#8fc2f0}.vannav a:hover{background:#3a372f}'
           '.vannav a[aria-current=page]{background:#ece9e0;color:#1b1a17}}</style>')


def navbar(cur, up=''):
    return '<nav class="vannav" aria-label="All pages">' + ''.join(
        f'<a href="{up}{f}"' + (' aria-current="page"' if f == cur else '') + f'>{t}</a>' for f, t, d in PAGES) + '</nav>'


def put(name, html, cur=None, guide=None):
    """write a page into site/: links to sides.html go to diagrams.html, noindex, the nav bar under <body>; guide = the slug of its part of the build guide (adds the numbered bar), or 'index'"""
    up = '../' if '/' in name else ''
    html = html.replace('href="sides.html"', f'href="{up}diagrams.html"')
    if 'name="robots"' not in html:
        html = html.replace('</head>', '<meta name="robots" content="noindex, nofollow"></head>', 1)
    html = html.replace('</head>', NAV_CSS + (buildguide.GUIDE_CSS if guide else '') + '</head>', 1)
    bars = navbar(cur or name, up) + (buildguide.guide_nav(GUIDE, guide, bool(up)) if guide else '')
    html = html.replace('<!--NAVS-->', '')
    html, n = re.subn(r'(<body[^>]*>)', lambda m: m.group(1) + bars, html, count=1)
    assert n == 1, name
    os.makedirs(os.path.dirname(os.path.join(SITE, name)) or SITE, exist_ok=True)
    open(os.path.join(SITE, name), 'w').write(html)


GUIDE, BUILD_PAGES = buildguide.pages(HERE)
GUIDE_OF = {g['file']: g['slug'] for g in GUIDE if g['ext']}
for name, src in (('diagrams.html', 'sides.html'), ('interactive.html', 'interactive.html'), ('install.html', 'install.html'), ('window.html', 'window.html'),
                  ('window-template.html', 'window-template.html'), ('wall-map.html', 'wall-map.html'), ('electric.html', 'electric.html'), ('interior.html', 'interior.html')):
    if os.path.exists(os.path.join(HERE, src)):
        put(name, open(os.path.join(HERE, src)).read(), guide=GUIDE_OF.get(name) or ('window' if name == 'window-template.html' else None))
for name, doc in BUILD_PAGES.items():
    slug = 'index' if name == 'index.html' else next(g['slug'] for g in GUIDE if g['file'] == name)
    put('build/' + name, doc, 'build/index.html', guide=slug)

cards = ''.join(f'<a class="card" href="{f}"><b>{t}</b><span>{d}</span></a>' for f, t, d in PAGES[1:])
home = ('<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Ford Transit van build</title>'
        '<style>:root{color-scheme:light dark;--bg:#fbfaf7;--card:#fff;--ink:#26241f;--mute:#6a665c;--line:#d9d5ca;--acc:#185FA5}'
        '@media (prefers-color-scheme:dark){:root{--bg:#1b1a17;--card:#242320;--ink:#ece9e0;--mute:#aaa598;--line:#3d3b34;--acc:#6fb1ee}}'
        '*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.5 -apple-system,"Segoe UI",system-ui,sans-serif}'
        '.wrap{max-width:900px;margin:0 auto;padding-block:20px;padding-left:max(16px,env(safe-area-inset-left,0px));padding-right:max(16px,env(safe-area-inset-right,0px))}'
        'h1{font-size:28px;margin:8px 0 4px}.lead{color:var(--mute);margin:0 0 18px}'
        '.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(250px,1fr));gap:12px}'
        '.card{display:flex;flex-direction:column;gap:4px;padding:14px 16px;background:var(--card);border:1px solid var(--line);border-radius:12px;text-decoration:none;color:var(--ink)}'
        '.card:hover{border-color:var(--acc)}.card b{font-size:18px;color:var(--acc)}.card span{color:var(--mute);font-size:14px}</style></head><body>'
        '<div class="wrap"><h1>Ford Transit 350 van build</h1><p class="lead">The plan, the diagrams, the install steps and the layouts, all in one place. Use the bar across the top of any page to move between them.</p>'
        f'<div class="grid">{cards}</div></div></body></html>')
put('index.html', home, 'index.html')
print('site/ rebuilt:', sorted(os.listdir(SITE)))
