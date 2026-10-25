# Van project rules

This repo is a custom Ford Transit 350 high-roof van plan. The pages are built from the sources in `tools/`; edit the sources, not the generated HTML.

- **Always show changes in all the html files when changes are made** (user rule). A change to the design goes into every page it touches: `interactive.html` (the adjustable plan, from `tools/ia_*.js`), `sides.html` (the static diagrams and tables, from `tools/gen2.py`, `plan.py`, `cur.py`, `ceiling.py`, `couch.py`, `leaf.py`, `letters.py`), `wall-map.html` (`tools/wallmap.js`), `electric.html` (`tools/electric.js`), `interior.html` (the 3D view, `tools/interior.js` and `interior_scene.js`), `install.html` when its numbers change (`tools/install.py`), and `site/` (`make-site.py`). Then update every published artifact link, and commit and push.
- **Exception, the 3D view is on hold (user: 'Leave 3d view until I say to make it'):** do NOT change `interior.html`, `tools/interior.js` or `tools/interior_scene.js`, and do not republish the 3D artifact, until the user says to make the 3D view. It stays as it was after the closet-drawers change; it does not show anything made after that. Every other page still follows the rule above.
- Rebuild with `sh tools/build.sh` (do not pipe it through head).
- Add an entry to `van-notes.md` for every change.
- Never make the repo public: the top-level `photos/` has GPS data. Only `site/` (photos with the metadata stripped) is meant to be published.
- Commit on the working branch and push there; do not open pull requests unless asked.
