import re
_path=(ROOT+'/sides.html')
_h=open(_path).read()
# letter badges inside each diagram, in page order
_starts=[m.start() for m in re.finditer(r'<svg viewBox="[^"]*" role="img"',_h)]
_letters=['A','B','C','C2','C3','D','E','E3','F','G']
if len(_starts)!=10: print('WARN: expected 10 diagrams, found',len(_starts))
for _k in range(len(_starts)-1,-1,-1):
    _e=_h.index('</svg>',_starts[_k])
    _w=13 if len(_letters[_k])==1 else 19
    _b=f'<g><rect x="{16-_w}" y="3" width="{2*_w}" height="26" rx="13" fill="#2C2C2A"/><text x="16" y="22" text-anchor="middle" style="font-size:{17 if len(_letters[_k])==1 else 15}px;font-weight:700;fill:#fff">{_letters[_k]}</text></g>'
    _h=_h[:_e]+_b+_h[_e:]
# letters in the headings
for _a,_b in [('<h3>Driver side wall: depth color map and furring layout</h3>','<h3>A. Driver side wall: depth color map and furring layout</h3>'),
 ('<h3>Driver side: built items</h3>','<h3>B. Driver side: built items</h3>'),
 ('<h3>Driver side: bed and couch, side section</h3>','<h3>C. Driver side: bed and couch, side section</h3>'),
 ('<h3>Driver side: the bed with a hinged leaf, day and night</h3>','<h3>C2. Driver side: the bed with a hinged leaf, day and night</h3>'),
 ('<h3>Driver side: building the leaf, slots and legs</h3>','<h3>C3. Driver side: building the leaf, slots and legs</h3>'),
 ('<h3>Passenger side wall: depth color map','<h3>D. Passenger side wall: depth color map'),
 ('<h3>Passenger side: built items</h3>','<h3>E. Passenger side: built items</h3>'),
 ('<h2>3. Looking down into the van, both sides</h2>','<h2>3. Looking down into the van, both sides (diagram F)</h2>')]:
    if _a not in _h: print('WARN heading missing',_a)
    _h=_h.replace(_a,_b,1)
# index of the diagrams, before section 1
_idx='<p><b>Diagrams:</b> A driver side depth map and furring layout, B driver side built items, C driver side bed and couch (side section), C2 driver side bed with a hinged leaf (day and night), C3 building the leaf, slots and legs, D passenger side depth map, E passenger side built items, E3 shower curtain on three sides (the old tipping-pan version; the pan is fixed now), F looking down at both sides, G the ceiling covering (plywood, slats, lights, fan and air conditioning cutouts).</p>\n'
_h=_h.replace('<h2>1. Driver side</h2>',_idx+'<h2>1. Driver side</h2>',1)
# legend: the red dashed line
_sw='<span><i class="sw" style="background:none;border:0;border-top:2px dashed #993C1D;height:0;vertical-align:4px"></i>red dashed line: the seam / pillar at about 98 in</span>'
_h=_h.replace('depth not measured</span>','depth not measured</span>'+_sw)
open(_path,'w').write(_h)
