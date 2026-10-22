#!/usr/bin/env python3
"""Rebuild the site/ folder that gets uploaded to the website.

site/index.html        copy of sides.html
site/interactive.html  copy of interactive.html (its link back goes to the folder's index)
site/install.html      copy of install.html (the illustrated fan and A/C steps)
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
shutil.copy(os.path.join(HERE, 'sides.html'), os.path.join(SITE, 'index.html'))
ipage = open(os.path.join(HERE, 'install.html')).read()
assert 'href="sides.html"' in ipage
open(os.path.join(SITE, 'install.html'), 'w').write(ipage.replace('href="sides.html"', 'href="./"'))   # the install steps; the link to the static diagrams goes to the folder's index
page = open(os.path.join(HERE, 'interactive.html')).read()
assert 'href="sides.html"' in page
open(os.path.join(SITE, 'interactive.html'), 'w').write(page.replace('href="sides.html"', 'href="./"'))
print('site/ rebuilt:', sorted(os.listdir(SITE)))
