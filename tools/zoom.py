_path=(ROOT+'/sides.html')
_h=open(_path).read()
_js='<script>\n'+open(HERE+'/zoom.js').read()+'zoomAll();\n</script>\n'
assert '</body>' in _h
_h=_h.replace('</body>',_js+'</body>',1)
_h=_h.replace('<h2>1. Driver side</h2>','<p><b>Zoom:</b> every diagram has + and − buttons in its top right corner; you can also hold Ctrl (Cmd on a Mac) and scroll, or pinch on a touch screen. Drag a zoomed diagram to move it, and press Reset to go back.</p>\n<h2>1. Driver side</h2>',1)
open(_path,'w').write(_h)
