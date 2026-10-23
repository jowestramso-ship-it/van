#!/bin/sh
# Rebuild everything from the sources in this folder.
#   interactive.html  = ia_head.html, zoom.js and the four other ia_* files joined
#   sides.html        = first-draft.html (the first draft) patched step by step by gen2.py, which runs
#                       cur, plan, couch, leaf, ceiling, letters, toggle and zoom .py in that order
#   install.html      = the illustrated fan and A/C install steps (install.py)
#   window.html       = the illustrated side window install steps (window.py, uses install.py's helpers)
#   window-template.html = the side window measured from the owner's photos, with the cutout numbers (wtemplate.py)
#   site/             = the copy for posting (make-site.py)
set -e
cd "$(dirname "$0")"
cat ia_head.html zoom.js ia_core.js ia_elev.js ia_plan.js ia_ui.js > ../interactive.html
python3 gen2.py
python3 install.py
python3 window.py
python3 wtemplate.py
cd ..
python3 make-site.py
