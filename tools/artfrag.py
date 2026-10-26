"""Makes the pages for the published artifacts 'Van Interior 3D', 'Electrical Layout' and 'Wall Marking Map' from interior.html, electric.html and wall-map.html:
fragments, because the artifact tool wraps the page in its own document (the title and the side-gutter meta go to the top, the html/head/body tags go, and the
links to the other pages point at the artifacts). Usage: python3 tools/artfrag.py KIND SRC OUTFILE   (KIND is 3d, electric or wallmap; then publish OUTFILE; see CLAUDE.md)."""
import re, sys
MAIN = 'https://claude.ai/artifact/PoTZ5J5BkcwXAr5J2RBTjs'     # Transit Van Plan
WMAP = 'https://claude.ai/artifact/1quE178yLUJmgmSuhm626H'     # Wall Marking Map
TITLE = {'3d': 'Van Interior 3D', 'electric': 'Electrical Layout', 'wallmap': 'Wall Marking Map'}
LINK = lambda u, t: f'<a href="{u}" target="_blank" rel="noopener">{t}</a>'

def convert(kind, s):
    s = re.sub(r'\A<!doctype html>.*?<title>[^<]*</title>', f'<meta name="claude:viewport-fit-sides" content="cover">\n<title>{TITLE[kind]}</title>\n', s, count=1, flags=re.S)
    s = re.sub(r'</style></head>\s*<body[^>]*>', '</style>\n', s, count=1)
    s = re.sub(r'\s*</body>\s*</html>\s*\Z', '\n', s)
    s = s.replace('<a href="interactive.html">Back to the interactive plan</a>', LINK(MAIN, 'Back to the interactive plan'))
    s = s.replace('<a href="wall-map.html">Wall marking map</a>', LINK(WMAP, 'Wall marking map'))
    return s

if __name__ == '__main__':
    kind, src, out = sys.argv[1:4]
    t = convert(kind, open(src, encoding='utf-8').read())
    open(out, 'w', encoding='utf-8').write(t)
    print('wrote', out, len(t))
