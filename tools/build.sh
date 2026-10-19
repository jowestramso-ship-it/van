#!/bin/sh
# Rebuild everything from the sources in this folder.
#   interactive.html  = ia_head.html, zoom.js and the four other ia_* files joined
#   sides.html        = index.html (the first draft) patched step by step by gen2.py, which runs
#                       cur, plan, couch, leaf, ceiling, letters and toggle .py in that order
#   site/             = the copy for posting (make-site.py)
set -e
cd "$(dirname "$0")"
cat ia_head.html zoom.js ia_core.js ia_elev.js ia_plan.js ia_ui.js > ../interactive.html
python3 gen2.py
cd ..
python3 make-site.py
