"""Builds the page 'Pictures for ChatGPT and Gemini' (an index of the 3D pictures of the van, each with its description and Copy/Save buttons).
Usage: python3 build_ai_index.py START_HERE.txt OUT.html   (START_HERE.txt is the prompt text file of the pack; the pictures are published beside the page under pictures/)"""
import re, json, sys
t = open(sys.argv[1], encoding='utf-8').read()
iA = t.index('PART A  (paste this first'); iB = t.index('PART B  (paste ONE look'); iC = t.index('PART C  (if the result')
body = lambda b: '\n'.join(b.strip('\n').split('\n')[2:]).strip()
A, Bsec, C = body(t[iA:iB]), body(t[iB:iC]), body(t[iC:])
looks, cur = [], None
for line in Bsec.split('\n'):
    m = re.match(r'^([A-F])\. ([A-Z0-9 ()\-]+)$', line)
    if m: cur = {'k': m.group(1), 'name': m.group(2).title(), 'text': ''}; looks.append(cur)
    elif cur is not None: cur['text'] += line + '\n'
for l in looks: l['text'] = l['text'].strip()
VIEWS = [
 ('1-from-the-rear-doors', 'From the rear doors', 'Camera at the rear doors at standing eye height, looking toward the cab. Left: the couch (seat about 26 in high, a tall back cushion, one pillow in view) with its wall cabinet above, then the floor-to-ceiling closet. Right: the shower curtain at the near end; beyond the stall, the plain solid wall that closes its cab end (the fridge and microwave are behind it, mostly hidden); then the kitchen counter. The cab is at the far end.'),
 ('2-from-the-cab-end', 'From the cab end', 'Camera at the cab end looking back toward the rear doors. Left: the kitchen counter with the sink, the flat TV above it and the open sliding door (the bright opening). Right: the dinette with its wall cabinet and sliding window. Far end: the rear doors.'),
 ('3-kitchen', 'The kitchen', 'The kitchen counter seen from the aisle: the sink and single-lever tap in the foreground, the TV above the counter with a small open shelf beside it, the open sliding door on the left, a dinette bench on the right and the rear doors at the far end.'),
 ('4-couch-and-aisle', 'Along the couch', 'A low camera in the aisle, looking toward the cab along the front of the couch. Left: the couch with its plain flat front panel down to the floor, the seat cushion and one pillow, the corner of the wall cabinet above; beyond it the closet with its drawers. Right: the shower curtain, then the kitchen counter in the distance.'),
 ('5-dinette', 'The dinette', 'The dinette seen from the aisle, looking at the driver side wall: the sliding window in the middle, a small table with one pedestal leg in front of it, and a bench seat on each side.'),
 ('6-couch-from-the-rear', 'The couch from its rear end', 'The couch seen from its rear end, looking along it: the long back cushion against the wall, two pillows, the wall cabinet above with a small warm light under it, and the closet at the far end.'),
]
D = json.dumps({'A': A, 'looks': looks, 'C': C, 'views': [{'f': f, 'name': n, 'note': d} for f, n, d in VIEWS]})
cards = ''.join(f'''<article class="view" data-i="{i}"><img src="pictures/{f}.jpg" alt="{n}" loading="lazy"><div class="vb"><h3>{n}</h3><p class="desc">{d}</p><div class="row"><button type="button" class="btn small" data-act="prompt" data-i="{i}">Copy prompt</button><button type="button" class="btn small ghost" data-act="desc" data-i="{i}">Copy description</button><button type="button" class="btn small ghost" data-act="img" data-i="{i}">Copy image</button><button type="button" class="btn small ghost" data-act="save" data-i="{i}">Save image</button></div></div></article>''' for i, (f, n, d) in enumerate(VIEWS))
looksel = ''.join(f'<label class="chip"><input type="radio" name="look" value="{l["k"]}"><span>{l["name"]}</span></label>' for l in looks)
html = f'''<meta name="claude:viewport-fit-sides" content="cover">
<title>Pictures for ChatGPT and Gemini</title>
<style>
/* layout: a look picker, then one card per picture (image, description, buttons) */
:root {{
  --bg: #f6f7f5; --surface: #ffffff; --ink: #1f2a2e; --mute: #5c6a6f; --line: #d9dfdd;
  --accent: #1d6f7a; --accent-ink: #ffffff; --soft: #e4f0f1;
  --font: "Inter", system-ui, -apple-system, "Segoe UI", sans-serif; --mono: ui-monospace, "SF Mono", Menlo, Consolas, monospace;
}}
@media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{
  --bg: #14191b; --surface: #1c2326; --ink: #e8eeee; --mute: #9aa8ac; --line: #2f3a3e; --accent: #5fb8c4; --accent-ink: #0b1a1d; --soft: #20363a; color-scheme: dark; }} }}
:root[data-theme="dark"] {{ --bg: #14191b; --surface: #1c2326; --ink: #e8eeee; --mute: #9aa8ac; --line: #2f3a3e; --accent: #5fb8c4; --accent-ink: #0b1a1d; --soft: #20363a; color-scheme: dark; }}
* {{ box-sizing: border-box; }}
body {{ background: var(--bg); color: var(--ink); font: 16px/1.55 var(--font); margin: 0; }}
main {{ max-width: 980px; margin: 0 auto; padding-block: 22px 60px; padding-left: max(16px, env(safe-area-inset-left, 0px)); padding-right: max(16px, env(safe-area-inset-right, 0px)); display: grid; gap: 26px; }}
h1 {{ font-size: 27px; line-height: 1.15; margin: 0 0 6px; text-wrap: balance; }}
h2 {{ font-size: 19px; margin: 0 0 6px; text-wrap: balance; }}
h3 {{ font-size: 17px; margin: 0; }}
p {{ margin: 0; }}
.lead {{ color: var(--mute); max-width: 64ch; }}
.row {{ display: flex; flex-wrap: wrap; gap: 8px; }}
.btn {{ font: inherit; font-weight: 600; font-size: 15px; padding: 9px 16px; border-radius: 8px; border: 1px solid var(--accent); background: var(--accent); color: var(--accent-ink); cursor: pointer; }}
.btn.ghost {{ background: transparent; color: var(--accent); }}
.btn.small {{ font-size: 13.5px; padding: 6px 12px; }}
.btn:focus-visible, .chip input:focus-visible + span {{ outline: 3px solid var(--ink); outline-offset: 2px; }}
.btn:disabled {{ opacity: .6; cursor: default; }}
.steps {{ margin: 8px 0 0; padding-left: 1.2em; max-width: 70ch; display: grid; gap: 3px; }}
.looks {{ display: flex; flex-wrap: wrap; gap: 8px; margin: 10px 0; }}
.chip input {{ position: absolute; opacity: 0; pointer-events: none; }}
.chip span {{ display: inline-block; padding: 8px 14px; border: 1px solid var(--line); border-radius: 999px; background: var(--surface); cursor: pointer; font-size: 15px; }}
.chip input:checked + span {{ background: var(--accent); border-color: var(--accent); color: var(--accent-ink); font-weight: 600; }}
.lookbox {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; font: 13.5px/1.55 var(--mono); white-space: pre-wrap; overflow-wrap: anywhere; max-height: 190px; overflow: auto; }}
.status {{ min-height: 1.4em; color: var(--mute); font-size: 14px; }}
.views {{ display: grid; gap: 16px; }}
.view {{ background: var(--surface); border: 1px solid var(--line); border-radius: 10px; overflow: hidden; display: grid; grid-template-columns: minmax(0, 1.1fr) minmax(0, 1fr); min-width: 0; }}
.view img {{ display: block; width: 100%; height: 100%; object-fit: cover; background: var(--line); min-height: 200px; }}
.vb {{ padding: 14px; display: grid; gap: 10px; align-content: start; min-width: 0; }}
.desc {{ color: var(--mute); font-size: 15px; }}
.view.plan {{ grid-template-columns: 1fr; }}
.view.plan img {{ height: auto; object-fit: contain; min-height: 0; }}
@media (max-width: 720px) {{ .view {{ grid-template-columns: 1fr; }} .view img {{ height: auto; aspect-ratio: 16 / 9; }} }}
details {{ background: var(--surface); border: 1px solid var(--line); border-radius: 8px; padding: 10px 12px; }}
summary {{ cursor: pointer; font-weight: 600; }}
details pre {{ margin: 10px 0 0; white-space: pre-wrap; overflow-wrap: anywhere; font: 13.5px/1.55 var(--mono); max-height: 260px; overflow: auto; }}
</style>
<main>
<header>
  <h1>Pictures for ChatGPT and Gemini</h1>
  <p class="lead">Six 3D pictures of the van, each with a description. Pick a look, then copy the prompt and the picture into ChatGPT or Gemini and ask it to draw the picture as a photograph.</p>
  <ol class="steps">
    <li>Pick a look below.</li>
    <li>On a picture, press <b>Copy prompt</b> and paste it in ChatGPT or Gemini.</li>
    <li>Attach the picture: press <b>Copy image</b> and paste it, or <b>Save image</b> and attach the file.</li>
  </ol>
  <p class="lead" style="margin-top:8px">ChatGPT and Gemini cannot open links to this page, so the pictures have to be pasted or attached.</p>
</header>

<section>
  <h2>1. Pick a look</h2>
  <div class="looks" role="radiogroup" aria-label="Look">{looksel}<label class="chip"><input type="radio" name="look" value="none" checked><span>No look: keep these colors</span></label></div>
  <div class="lookbox" id="lookbox" aria-live="polite"></div>
</section>

<section>
  <h2>2. The pictures</h2>
  <p class="lead">Each prompt holds the description of the whole van, the description of that picture and the look you picked.</p>
  <p class="status" id="st" role="status" aria-live="polite"></p>
  <div class="views">{cards}
    <article class="view plan"><img src="ALL-VIEWS-contact-sheet.jpg" alt="All six views on one sheet" loading="lazy"><div class="vb"><h3>Contact sheet: all six views</h3><p class="desc">Attach this first if the tool lets you attach more than one picture, so it sees the whole van. Then attach the picture to redraw.</p><div class="row"><button type="button" class="btn small ghost" data-act="img-sheet">Copy image</button><button type="button" class="btn small ghost" data-act="save-sheet">Save image</button></div></div></article>
    <article class="view plan"><img src="pictures/0-floor-plan-from-above.jpg" alt="The floor plan from above" loading="lazy"><div class="vb"><h3>Floor plan, looking down</h3><p class="desc">Rear doors on the left, cab on the right, driver side at the top. Labels overlap a little. For layout help only: do not ask it to redraw this one.</p><div class="row"><button type="button" class="btn small ghost" data-act="img-plan">Copy image</button><button type="button" class="btn small ghost" data-act="save-plan">Save image</button></div></div></article>
  </div>
</section>

<section>
  <h2>3. More</h2>
  <div class="row" style="margin-bottom:10px"><button type="button" class="btn" id="zipbtn">Save all pictures in a zip</button><button type="button" class="btn ghost" id="firstbtn">Copy the first prompt only</button><button type="button" class="btn ghost" id="fixbtn">Copy the fixes list</button></div>
  <details><summary>What the first prompt says</summary><pre id="firstpre"></pre></details>
  <details style="margin-top:10px"><summary>If the result is wrong, reply with one of these</summary><pre id="fixpre"></pre></details>
</section>
</main>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"></script>
<script>
const DATA = {D};
const st = document.getElementById('st'); let dl = null;
const say = m => {{ st.textContent = m; }};
(async () => {{ try {{ dl = await claude.use('downloads'); }} catch (e) {{ dl = null; }} }})();
const lookbox = document.getElementById('lookbox');
const curLook = () => {{ const v = document.querySelector('input[name=look]:checked').value; return DATA.looks.find(l => l.k === v) || null; }};
function showLook() {{ const l = curLook(); lookbox.textContent = l ? l.name.toUpperCase() + '\\n' + l.text : 'No look: ChatGPT or Gemini keeps the colors and materials of the render and only makes them look like a photograph.'; }}
document.querySelectorAll('input[name=look]').forEach(r => r.addEventListener('change', showLook)); showLook();
document.getElementById('firstpre').textContent = DATA.A; document.getElementById('fixpre').textContent = DATA.C;
function buildPrompt(i) {{
  const v = DATA.views[i], l = curLook();
  return DATA.A + '\\n\\nTHIS PICTURE (' + v.name + ')\\n' + v.note + '\\n\\n' + (l ? 'LOOK: ' + l.name.toUpperCase() + '\\n' + l.text : 'LOOK: keep the colors and materials of the render, only make them photorealistic.');
}}
async function copyText(text, label) {{
  try {{ await navigator.clipboard.writeText(text); say('Copied ' + label + '. Paste it in ChatGPT or Gemini.'); }}
  catch (e) {{ say('The browser would not copy. Select the text in the box and copy it by hand.'); }}
}}
function pngBlob(path) {{
  return fetch(path).then(r => r.blob()).then(b => createImageBitmap(b)).then(bm => new Promise(res => {{ const c = document.createElement('canvas'); c.width = bm.width; c.height = bm.height; c.getContext('2d').drawImage(bm, 0, 0); c.toBlob(res, 'image/png'); }}));
}}
async function copyImage(path, label) {{
  try {{ await navigator.clipboard.write([new ClipboardItem({{ 'image/png': pngBlob(path) }})]); say('Copied the picture (' + label + '). Paste it in ChatGPT or Gemini.'); }}
  catch (e) {{ say('The browser would not copy the picture. Use Save image and attach the file instead.'); }}
}}
async function saveFile(path, name) {{
  if (!dl) {{ say('Saving is not available in this view. Press and hold the picture to save it.'); return; }}
  try {{ const b = await (await fetch(path)).blob(); await dl.save({{ filename: name, data: b }}); say('Saved ' + name + '.'); }}
  catch (e) {{ say(e && e.code === 'declined' ? 'Not saved.' : 'Could not save ' + name + '. Press and hold the picture instead.'); }}
}}
const P = i => 'pictures/' + DATA.views[i].f + '.jpg';
document.addEventListener('click', ev => {{
  const b = ev.target.closest('[data-act]'); if (!b) return; const a = b.dataset.act, i = +b.dataset.i;
  if (a === 'prompt') copyText(buildPrompt(i), 'the prompt for "' + DATA.views[i].name + '"');
  else if (a === 'desc') copyText(DATA.views[i].note, 'the description');
  else if (a === 'img') copyImage(P(i), DATA.views[i].name);
  else if (a === 'save') saveFile(P(i), DATA.views[i].f + '.jpg');
  else if (a === 'img-sheet') copyImage('ALL-VIEWS-contact-sheet.jpg', 'contact sheet');
  else if (a === 'save-sheet') saveFile('ALL-VIEWS-contact-sheet.jpg', 'ALL-VIEWS-contact-sheet.jpg');
  else if (a === 'img-plan') copyImage('pictures/0-floor-plan-from-above.jpg', 'floor plan');
  else if (a === 'save-plan') saveFile('pictures/0-floor-plan-from-above.jpg', '0-floor-plan-from-above.jpg');
}});
document.getElementById('firstbtn').addEventListener('click', () => copyText(DATA.A, 'the first prompt'));
document.getElementById('fixbtn').addEventListener('click', () => copyText(DATA.C, 'the fixes list'));
const ZIPFILES = ['ALL-VIEWS-contact-sheet.jpg', 'pictures/1-from-the-rear-doors.jpg', 'pictures/2-from-the-cab-end.jpg', 'pictures/3-kitchen.jpg', 'pictures/4-couch-and-aisle.jpg', 'pictures/5-dinette.jpg', 'pictures/6-couch-from-the-rear.jpg', 'pictures/0-floor-plan-from-above.jpg', 'START-HERE-prompt-for-ChatGPT.txt'];
document.getElementById('zipbtn').addEventListener('click', async ev => {{
  const btn = ev.currentTarget, old = btn.textContent;
  if (!dl) {{ say('Saving is not available in this view. Save the pictures one by one instead.'); return; }}
  if (!window.JSZip) {{ say('The zip tool did not load. Save the pictures one by one instead.'); return; }}
  btn.disabled = true; btn.textContent = 'Building the zip';
  try {{
    const z = new JSZip();
    for (const p of ZIPFILES) {{ const r = await fetch(p); if (!r.ok) throw new Error('missing ' + p); z.file(p, await r.blob()); }}
    await dl.save({{ filename: 'van-for-chatgpt.zip', data: await z.generateAsync({{ type: 'blob', compression: 'STORE' }}) }}); say('Saved van-for-chatgpt.zip.');
  }} catch (e) {{ say(e && e.code === 'declined' ? 'Not saved.' : 'Could not build the zip. Save the pictures one by one instead.'); }}
  finally {{ btn.disabled = false; btn.textContent = old; }}
}});
</script>
'''
open(sys.argv[2], 'w', encoding='utf-8').write(html)
print('wrote', sys.argv[2], len(html))
