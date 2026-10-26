#!/bin/sh
# Rebuild everything from the sources in this folder.
#   interactive.html  = ia_head.html, zoom.js and the four other ia_* files joined
#   sides.html        = first-draft.html (the first draft) patched step by step by gen2.py, which runs
#                       cur, plan, couch, leaf, ceiling, letters, toggle and zoom .py in that order
#   install.html      = the illustrated fan and A/C install steps (install.py)
#   window.html       = the illustrated side window install steps (window.py, uses install.py's helpers)
#   window-template.html = the side window measured from the owner's photos, with the cutout numbers (wtemplate.py)
#   wall-map.html     = the see-through wall marking map, read off interactive.html in a headless browser (wallmap.js; needs node + playwright, skipped if they are missing)
#   electric.html     = the electrical and lighting layout (electric.js, same method as wall-map.html)
#   interior.html     = the 3D view of the inside of the van, drawn from the plan's sizes (interior.js + interior_scene.js; needs node + playwright, skipped if missing)
#   site/             = the copy for posting (make-site.py), with the build guide in site/build/ (tools/buildguide.py: one page per part of the build, in order, from sides.html, install.html, window.html, the plan table (tools/plan_rows.json), tools/build_steps.json and furring-cut-list.md)
set -e
cd "$(dirname "$0")"
cat ia_head.html zoom.js ia_core.js ia_elev.js ia_plan.js ia_ui.js > ../interactive.html
node buildsteps.js 2>/dev/null || echo 'build_steps.json not rebuilt (node + playwright needed)'
python3 gen2.py
python3 furrlist.py
python3 install.py
python3 window.py
python3 wtemplate.py
node wallmap.js 2>/dev/null || echo 'wall-map.html not rebuilt (node + playwright needed)'
node electric.js 2>/dev/null || echo 'electric.html not rebuilt (node + playwright needed)'
node interior.js 2>/dev/null || echo 'interior.html not rebuilt (node + playwright needed)'
cd ..
python3 make-site.py
