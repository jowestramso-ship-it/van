# Pictures for ChatGPT and Gemini (not part of the website)

A side tool: 3D stills of the van (the plan's current layout, the plan's own colors) with a description for each, and prompts for six looks, to paste into ChatGPT or Gemini so they draw the inside of the van as photographs. Published as the artifact 'Pictures for ChatGPT and Gemini' (https://claude.ai/artifact/N5AkCj3r8kw5uXbZSy965d), made of one page and the pictures.

Rebuild after the design changes (with `SC` set to a scratchpad where `sh tools/build.sh` wrote `$SC/three3d/interior_local.html`):
1. Copy `$SC/three3d/interior_local.html` to `$SC/three3d/interior_pack.html` with `window.__cam = (p, t, f) => { VIEWS.__tmp = { n: 'tmp', p, t, fov: f }; setView('__tmp'); };` added after `window.__setView = setView;` (the stills 4 to 6 use it for their cameras).
2. `render_views_1_to_3.js` (also writes 4 and 5, which the next script overwrites), `render_views_4_to_6.js`, `render_floor_plan.js` write the PNGs to `$SC/lookpack/`; delete `4-couch.png`. Make JPEGs (2000 px wide) in `pictures/` and the contact sheet `ALL-VIEWS-contact-sheet.jpg` (2 x 3 of the six views).
3. `python3 build_ai_index.py prompt-for-chatgpt.txt index.html`, then publish `index.html` with `pictures/*.jpg`, the contact sheet and the prompt text as its files, `capabilities: {downloads: true}`.
The descriptions of each view are in `build_ai_index.py` (`VIEWS`); the van description and the looks are in `prompt-for-chatgpt.txt`.
