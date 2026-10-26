"""Makes the page for the published artifact 'Transit Van Plan' from site/interactive.html (the plan with the numbered nav bar): a fragment, because the artifact
tool wraps the page in its own document. Usage: python3 tools/artmain.py OUTFILE   (then publish OUTFILE with the whole of site/ as its files; see CLAUDE.md)."""
import os, re, sys
HERE = os.path.dirname(os.path.abspath(__file__))
s = open(os.path.join(HERE, '..', 'site', 'interactive.html'), encoding='utf-8').read()
s = re.sub(r'\A<!doctype html>.*?</title>\s*', '<meta name="claude:viewport-fit-sides" content="cover">\n<title>Transit Van Plan</title>\n', s, count=1, flags=re.S)
s = s.replace('.wrap { max-width: 1380px; margin: 0 auto; padding: 16px; }', '.wrap { max-width: 1380px; margin: 0 auto; padding-block: 16px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); }')
s = re.sub(r'</head>\s*<body[^>]*>', '', s, count=1)
s = re.sub(r'\s*</body>\s*</html>\s*\Z', '\n', s)
open(sys.argv[1], 'w', encoding='utf-8').write(s)
print('wrote', sys.argv[1], len(s))
