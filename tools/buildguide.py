"""The build guide: one page per part of the build, in the order to do them, from the first thing to the last.
Called by make-site.py. Reads the finished pages (sides.html, electric.html), the plan table (tools/plan_rows.json, written by plan.py),
tools/build_steps.json (the Build order card with the plan's own numbers, written by tools/buildsteps.js) and furring-cut-list.md.
pages(root) returns (GUIDE, PAGES): GUIDE is the ordered list of parts, PAGES maps a file name in site/build/ to its HTML (without the navigation bars, which make-site.py adds).
The steps on a page are a suggested order made from the plan's own sizes; where the plan has no drawn instructions yet, the page says so."""
import html as H, json, os, re


def _read(p):
    return open(p, encoding='utf-8').read()


def _md(text):
    """the tiny markdown of furring-cut-list.md: headings, bullets, tables, bold"""
    out, tab, ul = [], [], False
    inl = lambda s: re.sub(r'\*\*(.+?)\*\*', r'<b>\1</b>', H.escape(s, quote=False))
    def flush_tab():
        nonlocal tab
        if tab:
            rows = [[c.strip() for c in r.strip().strip('|').split('|')] for r in tab if not re.match(r'^\|[-| ]+\|$', r.strip())]
            out.append('<div class="wide"><table><tr>' + ''.join(f'<th>{inl(c)}</th>' for c in rows[0]) + '</tr>' + ''.join('<tr>' + ''.join(f'<td>{inl(c)}</td>' for c in r) + '</tr>' for r in rows[1:]) + '</table></div>')
            tab = []
    for ln in text.split('\n'):
        if ln.startswith('|'):
            tab.append(ln); continue
        flush_tab()
        if ln.startswith('- '):
            if not ul: out.append('<ul>'); ul = True
            out.append(f'<li>{inl(ln[2:])}</li>'); continue
        if ul: out.append('</ul>'); ul = False
        if ln.startswith('### '): out.append(f'<h4>{inl(ln[4:])}</h4>')
        elif ln.startswith('## '): out.append(f'<h3>{inl(ln[3:])}</h3>')
        elif ln.startswith('# '): continue
        elif ln.strip(): out.append(f'<p>{inl(ln)}</p>')
    flush_tab()
    if ul: out.append('</ul>')
    return '\n'.join(out)


def pages(root):
    sides = _read(os.path.join(root, 'sides.html'))
    rows = json.load(open(os.path.join(root, 'tools', 'plan_rows.json'), encoding='utf-8'))
    try:
        bs = {s['id']: s for s in json.load(open(os.path.join(root, 'tools', 'build_steps.json'), encoding='utf-8'))}
    except Exception:
        bs = {}
    cut = _read(os.path.join(root, 'furring-cut-list.md')) if os.path.exists(os.path.join(root, 'furring-cut-list.md')) else ''

    def body(k):
        return bs[k]['body'] if k in bs else ''

    def sec(start, *ends):
        i = sides.index(start)
        js = [sides.index(e, i + len(start)) for e in ends if e in sides[i + len(start):]]
        return sides[i:min(js)] if js else sides[i:]

    def table(pats):
        sel = [r for r in rows if any(re.search(p, r[1], re.I) for p in pats)]
        if not sel: return ''
        return ('<div class="wide"><table class="rt"><tr><th>Item</th><th>In from the back</th><th>Size</th><th>Up from the floor</th><th>Notes</th></tr>' +
                ''.join(f'<tr><td><b>{H.escape(r[1])}</b></td><td>{H.escape(r[2])}</td><td>{H.escape(r[3])}</td><td>{H.escape(r[4])}</td><td>{H.escape(r[5])}</td></tr>' for r in sel) + '</table></div>')

    ol = lambda steps: '<ol class="steps">' + ''.join(f'<li>{s}</li>' for s in steps) + '</ol>'
    fp = '<p class="sug">The steps below are a suggested order made from the plan\'s own sizes. The plan has no drawn, step-by-step instructions for this part yet, so check each one against the real parts before you cut.</p>'

    A = sec('<h3>A. Driver side wall: depth color map and furring layout</h3>', '<h3>Reading the wall</h3>')
    D = sec('<h3>D. Passenger side wall: depth color map', '<h3>Passenger side adjustments</h3>')
    Bd = sec('<h3>B. Driver side: built items</h3>', '<h3>C. Driver side: bed and couch')
    C = sec('<h3>C. Driver side: bed and couch, side section</h3>', '<h3>C4. Driver side')
    C4 = sec('<h3>C4. Driver side', '<h3>C5. Driver side')
    C5 = sec('<h3>C5. Driver side', '<h2>2. Passenger side</h2>')
    E = sec('<h3>E. Passenger side: built items</h3>', '<h3>E3. ')
    E3 = sec('<h3>E3. ', '<h2>3. Looking down')
    G = sec('<h2>4. The ceiling covering, seen from above (diagram G)</h2>', '<h2>Driver side photos</h2>')

    P = []   # (slug, nav, title, kicker, intro, steps, blocks)  or ext pages
    P.append(dict(slug='before', nav='Before you cut', title='Before you cut: manuals, measurements and decisions',
        kick='Do this first. Nothing here needs a tool, but every later step depends on it.',
        intro=f'<p>{H.escape(body("manuals"))}</p>',
        steps=['<b>Get the two manuals</b> (the roof fan, a 2012 F36AR with a 356 mm opening, and the OutEquip air conditioner) and read the opening size and the roof thickness each kit clamps across, before anything is cut.',
               '<b>Re-measure what the plan still marks as an estimate:</b> the cab-end numbers (the wheel well\'s front, the end of pan P11 and the cab wall itself can each be 2 to 4 in off), the depth of the driver wall at 41 to 56 in up (not measured), the width of the flat part of the roof (assumed 68 in), and the real sizes of the units you own: the battery, the LiTime and VEVOR chargers, the BELTTT inverter and its lugs, and the slides you buy.',
               '<b>Settle the electrics the other steps depend on:</b> the battery (280 Ah lithium is assumed), the inverter and its transfer switch (the BELTTT has none, so a 30 A transfer switch is needed), where the starter-battery cable leaves the cab, and where the grey water tank goes (not set yet).',
               '<b>Open the interactive plan and read "Does it fit?".</b> Anything red or amber is a decision to make before building; for example, seated headroom under the wall cabinets is 1 1/2 in with the 5 in cushions.',
               '<b>Buy the long-lead parts first:</b> the fan and the air conditioner, the side window, the 18 in full-extension slides (75 lb or more), the steel tube for the lift-out rail, and the 2/0 and 2 AWG cable (the electrical page lists how much).'],
        blocks=[]))
    P.append(dict(slug='fan-ac', nav='Fan and A/C', title='Roof fan and air conditioner', ext='install.html',
        kick='Cut the roof first: it is dirty, and everything under it is still open.', desc='Step by step with drawings: cutting, framing and mounting the roof fan and the air conditioner.', intro='', steps=[], blocks=[]))
    P.append(dict(slug='window', nav='Side window', title='Side window', ext='window.html', also=('window-template.html', 'the window template'),
        kick='Another steel cut, so it also comes before the insulation and the wiring.', desc='Step by step with drawings: installing the side window, with a cardboard template.', intro='', steps=[], blocks=[]))
    P.append(dict(slug='wiring', nav='Wiring rough-in', title='Wiring rough-in',
        kick='Everything that will be hidden gets wired before it is covered.',
        intro=f'<p>{H.escape(body("wiring"))}</p><p>The drawings, the wire sizes and the cable table are on the <a href="../electric.html">electrical layout page</a>.</p>',
        steps=['<b>Before the walls and ceiling are covered:</b> run the risers, the ceiling trunk and every branch, with grommets in all steel and the 12 V and 120 V in separate looms (at least 2 in apart, crossing at right angles).',
               '<b>Ceiling first (it is hidden first):</b> the two ceiling lights (16 AWG, each on one slat), the soft LED strip (14 AWG, its own 10 A circuit), the roof fan (14 AWG, 5 A) and the A/C feed (a 6 AWG pair, a 100 A fuse at the battery, about 12 ft).',
               '<b>The 12 V trunk</b> to the fuse block (12 AWG), the water pump circuit (14 AWG, 10 A, under the sink) and the control panel (18 AWG, 3 A).',
               '<b>The 120 V circuits</b> in flexible conduit (12 AWG): the outlets (A), the microwave through the selector (B), the fridge (C) and the water heater through the selector (D). One shore inlet (30 A), at 80 in from the back and 21 in up, through the solid steel band at 19 1/2 to 23 in up.',
               '<b>With the furring strips:</b> fix the electrical boxes to blocking between the strips, and add blocking behind the hub board, the switch plates and the outlets before the planks go on.',
               '<b>Last, after the covering is up:</b> the hub board (on the closet\'s rear panel, 72 to 74 in from the back, 1 to 11 in up) with its fuses, the inverter and the two chargers on the gear shelf, the transfer switch, the lights and the plates. Every cable to the gear shelf needs a loop about 24 in longer than a fixed run.',
               '<b>Test</b> every circuit with a meter before you connect the battery, test the GFCI outlets with their button, and have the 120 V side inspected before you use it.'],
        blocks=[]))
    P.append(dict(slug='insulate', nav='Insulation and floor', title='Insulation and subfloor',
        kick='After the roof and the window are cut and the wiring is in, before anything covers the walls.',
        intro=f'<p>{H.escape(body("insulate"))}</p><p>{H.escape(body("floor"))}</p><p class="sug">The plan does not choose the insulation material or the subfloor thickness yet, so there are no numbers for them here; the plan only fixes the depths and the order.</p>',
        steps=['<b>Insulate between the ribs and in the walls,</b> keeping the insulation clear of the opening frames and the wiring, and not past the ceiling plane.',
               '<b>Lay the subfloor.</b> Everything else stands on it: the couch base, the counter, the tanks and the battery. Check it is flat before the heavy things go on.'],
        blocks=[]))
    P.append(dict(slug='furring', nav='Furring strips', title='Furring strips, spacer blocks and shims',
        kick='Eight strips on each wall, so every plank is held at least every 14 in.',
        intro=f'<p>{H.escape(body("furring"))}</p>',
        steps=['<b>Cut the 1x2 strips</b> to the cut list below: 40 pieces, about 26 eight-foot sticks. Any strip over 8 ft is two pieces butted at an attachment dot.',
               '<b>Cut the spacer blocks and shims:</b> 63 blocks (1 1/2 in cuts off a 2x4, stood on the 3 1/2 in side) and 37 thin plywood shims (1/4 in for S7, 5/8 in for S8).',
               '<b>Mark the dots on the steel</b> from the maps below (white dots; dark squares are blocks, light dashed squares are shims). Keep every dot on solid steel, clear of the holes.',
               '<b>Glue the blocks to the steel</b> (adhesive, never screws into the van\'s body) at the dots of S4, S5 and S6 and the nook frames V1 to V3, with adhesive pads for S1, S2 and S3, and hold them until cured.',
               '<b>Fix the strips to the blocks:</b> glue and a #8 x 1 1/2 in screw through the strip into each block. S7 and S8 sit on their shims.',
               '<b>Check the line:</b> every strip\'s back should sit on one line, 3 3/4 in off the body, so the planks lie flat 4 1/2 in off it.',
               '<b>Passenger side:</b> the strips stop at the sliding door opening (104 in) except S8; S5 is cut away at the two nooks; then add the nook frames V1 to V4 and the three cross pieces.',
               '<b>Blocking for the ceiling slats</b> goes in before the walls are covered.'],
        blocks=[_md(cut), A, D]))
    P.append(dict(slug='ceiling', nav='Ceiling', title='Ceiling covering',
        kick='Ceiling before walls, so the wall sheets finish against it.',
        intro=f'<p>{H.escape(body("cover").split("Walls:")[0].strip())}</p>' + table(['^Covering$', 'Round lights', 'Roof fan cutout', 'Air conditioning cutout']),
        steps=['<b>Plywood first:</b> 3 sheets of 3/16 in plywood against the roof, cut around the fan and the A/C openings (their frames are already in from the roof step).',
               '<b>Lights:</b> the two round lights sit on slats (each centered on a 3 in slat, 2 in clear of the ribs), with a small hole through the plywood behind each for the wire. The shower light is wet rated.',
               '<b>Slats:</b> 15 cedar slats, 3 x 3/4 in with 1 in gaps (1 1/2 in at each side), on the blocking; each needs 14 ft stock, or shorter slats in the plan\'s "for now" option.',
               '<b>Cut the slats at the fan and A/C openings;</b> each ends at a framed curb.',
               '<b>The soft LED strip</b> goes around the ceiling edge on its own circuit.'],
        blocks=[G]))
    P.append(dict(slug='walls', nav='Walls', title='Wall planks and floor-to-ceiling walls',
        kick='After the ceiling, so the sheets finish against it.',
        intro=f'<p>{H.escape("Walls: " + body("cover").split("Walls:")[1].strip()) if "Walls:" in body("cover") else ""}</p>' + table(['Floor-to-ceiling wall']),
        steps=['<b>Seal and finish both faces of every sheet first</b> (a clear water-based finish or hardwax oil), before you hang it.',
               '<b>Hang the sheets floor to ceiling,</b> glued to every strip, with a screw and a finish washer about every 8 in and 1/16 in between sheets; the joints fall at 42, 90 and 138 in.',
               '<b>Stand the four 3/4 in floor-to-ceiling walls</b> (W1 closet end, W2 behind the driver seat, W3 shower and fridge, W4 fridge and counter) on the finished floor and fix them to the framing; the dinette backs lean on W1 and W2.'],
        blocks=[]))
    P.append(dict(slug='heavy', nav='Battery and tanks', title='The heavy low things: battery, tanks, couch base',
        kick='Heavy things go in before the cabinets that would block the way.',
        intro=f'<p>{H.escape(body("heavy"))}</p>' + table(['^Battery$', 'Wheel well', 'Fresh water tank', 'Hot water tank', 'Grey water tank']),
        steps=['<b>Battery</b> on the floor next to the driver-side wheel well, on its aisle side, 1 in from the closet (52 to 73 in from the back), with room over it for the gear shelf (the battery top at 9 1/2 in).',
               '<b>The hot water tank and the fresh water tank</b> on the floor at their places on the passenger side (see the table), before the counter and the sink cabinet go up.',
               '<b>Then the couch base</b> (next page), then the gear shelf and the lift-out rail, then the counter and the drawers.'],
        blocks=[]))
    P.append(dict(slug='couch', nav='Couch and bed', title='Couch, deck and the bed leaf',
        kick='After the battery is in; the shelf goes into this frame.',
        intro='<p>The couch is 74 x 26 in and sits on a base 3 1/2 in higher than the old plan, so the gear shelf fits over the battery. The front under the deck is open (nothing covers it). The bed makes up with a hinged leaf and four fold-down legs.</p>' + table(['Bed / couch', 'Wheel well']),
        steps=['<b>Build the base:</b> two end panels (the one next to the closet is 26 in deep), a ledger on the wall and a front rail, so the deck is 16 to 16 3/4 in up. Add the slide divider at 38 5/8 in (next page) while the frame is open.',
               '<b>Leave the front under the deck open:</b> only the front rail carries the deck edge (a steel tube lifts out across the gear shelf opening).',
               '<b>Deck:</b> 3/4 in plywood, 74 x 26 in. <b>Leaf:</b> 3/4 in birch plywood, 20 x 73 3/4 in, a plain slab; hinge it with a 74 in continuous hinge on the top faces (#8 x 5/8 in screws every 3 to 4 in, a 1/8 to 3/16 in gap).',
               '<b>Legs:</b> cut four through-slots (1 1/2 x 13 in) in the leaf, 3 in from the free edge, about 24 in apart; each leg is a 3/8 x 1 1/4 in bar, 12 5/8 in long, on a 1/4 in pin, with a threaded foot that screws out about 3 1/2 in.',
               '<b>Latches:</b> two turn buttons or magnetic catches hold the leaf folded back while driving.',
               '<b>Cushions:</b> the seat cushion 5 in thick, and the back cushion 5 in thick and 20 in tall in one piece, leaning back 12 degrees; check the seated headroom (1 1/2 in).'],
        blocks=[C, Bd]))
    P.append(dict(slug='gear-shelf', nav='Gear shelf', title='The pull-out gear shelf over the battery',
        kick='The couch frame and the divider have to be in first.',
        intro='', steps=[], blocks=[C4]))
    P.append(dict(slug='lift-out-rail', nav='Lift-out rail', title='The lift-out front rail',
        kick='After the shelf slides are on the divider and the couch end panel.',
        intro='', steps=[], blocks=[C5]))
    P.append(dict(slug='bath', nav='Wet bath', title='Wet bath: stall, toilet and nook',
        kick='Passenger side, at the rear end; it needs the passenger-side strips and the walls first.',
        intro=table(['Shower', 'Toilet', 'Floor-to-ceiling wall W3']),
        steps=[fp.replace('<p class="sug">', '').replace('</p>', ''),
               '<b>Stand W3</b> (35 1/4 to 36 in from the back, 24 in deep) as the end wall of the stall, and frame the shower nook between the nook frames V1 and V2 (the furring page).',
               '<b>Fix the pan:</b> 36 x 24 in with a 3 in curb; it does not tip.',
               '<b>Plumb it:</b> the shower head at 9 in from the back and the valve at 33 in; the drain runs to a tank under the van (the grey tank\'s place is not set).',
               '<b>Curtain on three sides</b> on a rod above (diagram E3), pulled to the rear end.',
               '<b>Toilet:</b> the Reliance Fold-To-Go stays set up on the pan at the cab end (20 3/4 to 35 1/4 in), sideways.',
               '<b>Nook contents:</b> towel bar, a shelf, toilet paper and bottles (keep the paper out of the splash).'],
        blocks=[E3]))
    P.append(dict(slug='kitchen', nav='Kitchen side', title='Counter, sink, fridge and the rest of the passenger side',
        kick='After the heavy tanks, before the wall cabinets.',
        intro=table(['Cabinet / counter', 'Nook \\(P6', 'Fridge', 'Shelf over the fridge', 'Microwave', 'TV', 'Sink', 'Drawers', 'Lower drawers', 'Trash can', 'Drain jug', 'Paper towel', 'Dish towel', 'Floor-to-ceiling wall W4']),
        steps=[fp.replace('<p class="sug">', '').replace('</p>', ''),
               '<b>Stand W4</b> (58 to 58 3/4 in) and the fridge platform, then the tall fridge (36 to 58 in) and the shelf over it for the microwave.',
               '<b>Build the counter cabinet</b> from 58 in to the sink (the angled front) with the drawers and the trash can pull-out, and the sink cabinet over the fresh water tank.',
               '<b>Counter top, sink and faucet,</b> then the nook for the jars (76 to 93 1/4 in), the TV, the paper towel holder and the dish towel hook.',
               '<b>Fit the pump</b> under the sink, then connect the supply lines (two 1/2 in PEX lines to the shower valve).'],
        blocks=[E]))
    P.append(dict(slug='closet-dinette', nav='Closet and dinette', title='Closet and dinette',
        kick='Driver side, cab end of the couch.',
        intro=table(['^Closet$', 'Closet door', 'Dinette', 'Floor-to-ceiling wall W1', 'Floor-to-ceiling wall W2']),
        steps=[fp.replace('<p class="sug">', '').replace('</p>', ''),
               '<b>Closet:</b> 15 x 25 in, starting at 74 in from the back (right at the end of the couch); the side panel next to the couch is the couch\'s end panel (26 deep).',
               '<b>One rod</b> along the wall at 71 in up, then the four drawers under the clothes (each 7 5/16 in tall), and the one door above them on the bed-side hinge.',
               '<b>Dinette:</b> two benches (19 1/2 x 28 in, seat 17 1/2 in up) and a table (26 x 28 in, 29 in up); the backrests stand at the ends, against W1 and W2.'],
        blocks=[]))
    P.append(dict(slug='cabinets', nav='Wall cabinets', title='Wall cabinets, doors and the fold-out table',
        kick='Last of the big pieces: they are the ones most likely to need small adjustments.',
        intro=f'<p>{H.escape(body("cabinets"))}</p>' + table(['Overhead cabinets', 'Cabinet doors', 'Fold-out table', 'Foot ledge', 'Entry']),
        steps=['<b>Scribe the cabinet backs to the leaning wall</b> (or fill the wedge) and cut their tops to the finished ceiling at the wall.',
               '<b>Doors:</b> three per cabinet, 10 in tall (63 1/2 to 73 1/2 in up), flip-up, with 1/8 in gaps; the pulls are black.',
               '<b>Fold-out table</b> at the cab-side end of the sink cabinet, with its foot ledge hinged under it.'],
        blocks=[]))
    P.append(dict(slug='finish', nav='Finish and test', title='Finishing and checking',
        kick='The last things, and the checks that tell you it works.',
        intro='<p>This is a checklist more than a build step: the work is done when each line is true.</p>',
        steps=['Cushions on, the leaf folded back, legs in their slots and the turn buttons shut.',
               'The gear shelf slides out smoothly with the lift-out rail off, the cable loops follow it without catching, and it goes back home.',
               'Every circuit tested with a meter, the GFCI outlets tested, the 120 V side inspected.',
               'The roof fan and the air conditioner run, the seals around them hold water, the window is sealed.',
               'Open every door and drawer in turn: the closet door and drawers, the trash can, the fridge door, the fold-out table; check the walkway they leave.',
               'Re-read "Does it fit?" on the interactive plan: nothing red, and you are happy with what is amber.'],
        blocks=[]))
    # ---- compose ----
    GUIDE = []
    for n, p in enumerate(P, 1):
        GUIDE.append(dict(n=n, slug=p['slug'], nav=p['nav'], title=p['title'], kick=p['kick'], ext=p.get('ext'), also=p.get('also'), desc=p.get('desc', ''),
                          file=p.get('ext') or f"{n:02d}-{p['slug']}.html"))
    head = sides[:sides.index('<body>')]
    head = re.sub(r'<title>.*?</title>', '<title>__TITLE__</title>', head, count=1)
    scripts = ''.join(re.findall(r'<script[^>]*>.*?</script>', sides[sides.index('<body>'):], re.S))
    extra_css = ('<style>.gk{color:#5F5E5A;margin:-4px 0 14px}.steps{padding-left:22px}.steps li{margin:0 0 9px}.sug{color:#5F5E5A;font-size:14px;border-left:3px solid #D3D1C7;padding:2px 12px;margin:10px 0}'
                 '.rt td,.rt th{vertical-align:top;padding:5px 12px 5px 0;font-size:13px}.rt td:last-child{min-width:260px}.gp{display:flex;flex-wrap:wrap;justify-content:space-between;gap:10px;margin:28px 0 8px}'
                 '.gp a{padding:8px 14px;border:1px solid #B4B2A9;border-radius:18px;text-decoration:none;color:#185FA5}.gp a:hover{border-color:#2C2C2A}h1 .gn{color:#5F5E5A;font-weight:400}</style>')
    def href(g, from_build=True):
        return (('../' if from_build else '') + g['file']) if g['ext'] else (g['file'] if from_build else 'build/' + g['file'])
    PAGES = {}
    for i, (p, g) in enumerate(zip(P, GUIDE)):
        if g['ext']: continue
        prev = GUIDE[i - 1] if i else None
        nxt = GUIDE[i + 1] if i + 1 < len(GUIDE) else None
        foot = '<div class="gp">' + (f'<a href="{href(prev)}">&larr; {prev["n"]}. {H.escape(prev["nav"])}</a>' if prev else '<span></span>') + (f'<a href="{href(nxt)}">{nxt["n"]}. {H.escape(nxt["nav"])} &rarr;</a>' if nxt else f'<a href="index.html">Back to the build guide</a>') + '</div>'
        parts = [f'<h1><span class="gn">Step {g["n"]} of {len(GUIDE)}</span><br>{H.escape(g["title"])}</h1><p class="gk">{H.escape(g["kick"])}</p>']
        if p['intro']: parts.append(p['intro'])
        if p['steps']:
            parts.append('<h2>Steps, in order</h2>' + ol(p['steps']))
        if p['blocks']:
            parts.append('<h2>Drawings and numbers</h2>' if p['steps'] else '')
            parts.extend(p['blocks'])
        parts.append(foot)
        doc = head.replace('__TITLE__', H.escape(g['title']) + ' - Van build guide').replace('</head>', extra_css + '</head>', 1) + '<body><!--NAVS-->' + '\n'.join(parts) + scripts + '</body></html>'
        PAGES[g['file']] = doc
    # the index: every part in order, first to last
    items = ''.join(f'<li><a href="{href(g)}"><b>{H.escape(g["title"])}</b></a><br><span class="gk">{H.escape(g["kick"])}</span></li>' for g in GUIDE)
    idx = (head.replace('__TITLE__', 'Van build guide').replace('</head>', extra_css + '</head>', 1) + '<body><!--NAVS--><h1>Van build guide</h1>'
           '<p>Every part of the build on its own page, from the first thing to do to the last. Use the numbered bar under the main bar to jump to a part, or the links at the bottom of each page to go to the next. '
           'The order is a suggestion made from the plan (the same nine steps as the Build order on the interactive plan, with the parts that came later put in their place); the numbers on each page come from the plan\'s own sizes.</p>'
           f'<ol class="steps">{items}</ol>'
           '<p class="sug">To put this online: upload everything in this folder (the files and the folders next to this one) to any web host, keeping the folder structure. There is nothing to install; open <b>index.html</b>. Every page asks search engines not to list it.</p></body></html>')
    PAGES['index.html'] = idx
    return GUIDE, PAGES


GUIDE_CSS = ('<style>.guidenav{display:flex;flex-wrap:wrap;gap:3px 5px;align-items:center;margin:0;padding:6px max(12px,env(safe-area-inset-left,0px));font:13px/1.3 -apple-system,"Segoe UI",system-ui,sans-serif;background:#fff;border-bottom:1px solid #cfcbbd;color:#26241f}'
             '.guidenav b{margin-right:4px;color:#5F5E5A;font-weight:600}.guidenav a{color:#185FA5;text-decoration:none;padding:3px 8px;border-radius:12px;white-space:nowrap}.guidenav a:hover{background:#e3e0d4}'
             '.guidenav a[aria-current=page]{background:#185FA5;color:#fff;font-weight:600}@media (prefers-color-scheme:dark){.guidenav{background:#1b1a17;border-bottom-color:#4a473e;color:#ece9e0}.guidenav a{color:#8fc2f0}.guidenav a[aria-current=page]{background:#8fc2f0;color:#1b1a17}}</style>')


def guide_nav(GUIDE, cur, from_build):
    """the numbered bar of the parts; cur is a slug, or None"""
    def hr(g): return (('../' if from_build else '') + g['file']) if g['ext'] else (g['file'] if from_build else 'build/' + g['file'])
    return ('<nav class="guidenav" aria-label="Build guide, in order"><b>Build order:</b>' +
            f'<a href="{"index.html" if from_build else "build/index.html"}"' + (' aria-current="page"' if cur == 'index' else '') + '>All</a>' +
            ''.join(f'<a href="{hr(g)}"' + (' aria-current="page"' if g['slug'] == cur else '') + f'>{g["n"]} {H.escape(g["nav"])}</a>' for g in GUIDE) + '</nav>')
