# Writes furring-cut-list.md from the same numbers as the furring maps (shelfdata.py and furring.py), so the list and the drawings cannot drift apart.
import os, math
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
exec(open(HERE + '/shelfdata.py').read())
exec(open(HERE + '/furring.py').read())

def dots(d): return ', '.join(f'{v:g}' for v in d)
def row(tag, i, p):
    n, k, x0, x1, joined, d = p
    return f'| {tag}{i:02d} | {n}{k} | {fr8(HT[n])} | {fr16(x0)} | {fr16(x1)} | **{fr16(x1 - x0)}** | {"joins its other half" if joined else ""} | {dots(d)} |'
HEAD = '| Cut | Strip | Height up | From (in) | To (in) | Length | Joint | Dots (attachment points) within the piece |\n|---|---|---|---|---|---|---|---|'
drv = [row('D', i + 1, p) for i, p in enumerate(DRV_PIECES)]
pas = [row('P', i + 1, p) for i, p in enumerate(PASS_PIECES)]
# the window frame: the jambs stand between the strips, the sill and the head fit between the jambs
frame_len = {nm: max(z1 - z0, x1 - x0) for nm, x0, x1, z0, z1 in WIN_FRAME}
frame_rows = [f'| W{i + 1:02d} | {nm} | {"vertical jamb" if z1 - z0 > x1 - x0 else "horizontal, between the jambs"} | **{fr16(frame_len[nm])}** | {fr16(x0)} to {fr16(x1)} in from the back, {fr16(z0)} to {fr16(z1)} in up |' for i, (nm, x0, x1, z0, z1) in enumerate(WIN_FRAME)]
# nook frames (passenger)
efr = [f'| E{i + 1:02d} | {nm} | vertical, {["shower nook rear end", "shower nook front end", "counter nook rear end", "counter nook right end"][i]} | **{fr16(t - b)}** | {fr16(x0)} to {fr16(x1)} in from the back, {fr16(b)} to {fr16(t)} in up |' for i, (nm, x0, x1, b, t, sp) in enumerate(VFR)]
efr += ['| E05 | X1 | cross piece, shower nook floor | **17 1/4** | between V1 and V2, top edge at 38 in up |',
        '| E06 | X2 | cross piece, shower nook top | **17 1/4** | between V1 and V2, bottom edge at 54 in up |',
        '| E07 | X3 | cross piece, counter nook top | **17 1/4** | between V3 and V4, bottom edge at 54 in up |']
d_len = sum(p[3] - p[2] for p in DRV_PIECES); p_len = sum(p[3] - p[2] for p in PASS_PIECES)
f_len = sum(frame_len.values()); e_len = sum(t - b for nm, x0, x1, b, t, sp in VFR[:4]) + 3 * 17.25
allp = [p[3] - p[2] for p in DRV_PIECES + PASS_PIECES] + list(frame_len.values()) + [t - b for nm, x0, x1, b, t, sp in VFR] + [17.25] * 3
total_len = sum(allp); npieces = len(allp)
stk = N_STICKS
spare = N_BUY
tot_blocks = DRV_BLOCKS + PASS_BLOCKS; tot_shims = DRV_SHIMS + PASS_SHIMS
per_stick = int(96 // 1.625); blk_sticks = math.ceil(tot_blocks / per_stick)

md = f'''# Furring strips to cut

All strips are **1x2 furring: 3/4 x 1 1/2 in actual**. Positions are inches along the wall from the back mark (6 in in from the rear-door edge), the same numbers as the furring drawings on the wall diagrams. "Height" is the center of the strip above the floor, so the strip runs 3/4 in below to 3/4 in above that. Nothing here needs a width cut, only cuts to length.

A 154 in wall does not come in one stick, so a strip that is longer than 8 ft (96 in) is two pieces **butted at an attachment dot** (the joint then sits on a fixed point, with a pad or spacer under it). The pieces are listed as "a", "b" and "c", in order from the back.

## Driver side ({len(DRV_PIECES)} strip pieces)

{HEAD}
''' + '\n'.join(drv) + f'''

S1 is in two pieces on purpose: it stops at the wheel well (42 to 76), which needs its own box. S2 to S4, S7 and S8 run the whole 154 in. **S5 and S6 stop at the side window frame**: each is a piece from 0 to 100 1/4 in (cut in two at 71 1/4 so it fits on an 8 ft stick) and a short piece from {fr16(WR)} to 154 in.

### Side window frame, driver side ({len(WIN_FRAME)} pieces)

The window cutout is {fr16(WIN_CW)} x {fr16(WIN_CH)} in. Around it goes a frame of the same strip, 1 1/2 in wide, that stops S5 and S6 and gives the planks an edge: the two jambs stand against the strips' ends and the sill and the head fit between the jambs. Each piece sits on three 3 5/8 in spacer blocks.

| Cut | Piece | What it is | Length | Where |
|---|---|---|---|---|
''' + '\n'.join(frame_rows) + f'''

The frame sits {fr16(JAMB)} in outside the cutout on every side, so the opening that is left is exactly the cutout. Cut the four pieces after you have measured the real hole (the opening is already cut), not before.

## Passenger side ({len(PASS_PIECES)} strip pieces)

{HEAD}
''' + '\n'.join(pas) + f'''

The passenger strips stop at the sliding door opening (104 in); only S8 carries on above the door. S5 is cut away at the two nooks, so it is three short pieces with no joint.

### Nook frames and cross pieces, passenger side ({len(efr)} pieces)

| Cut | Piece | What it is | Length | Where |
|---|---|---|---|---|
''' + '\n'.join(efr) + f'''

## Totals

- Driver side strips: {fr8(d_len)} in ({d_len / 12:.1f} ft), {len(DRV_PIECES)} pieces; window frame {fr8(f_len)} in, {len(WIN_FRAME)} pieces.
- Passenger side strips: {fr8(p_len)} in ({p_len / 12:.1f} ft), {len(PASS_PIECES)} pieces; frames and cross pieces {fr8(e_len)} in, {len(efr)} pieces.
- Everything: **{fr8(total_len)} in ({total_len / 12:.0f} ft), {npieces} pieces**. Packed onto 8 ft sticks with a 1/8 in saw kerf that is **{stk} sticks**; buy about {spare} (some spare for bad boards and cutting mistakes).
- The wall diagrams say about {round((d_len + f_len) / 12)} ft for the driver side alone; this list agrees ({fr8(d_len + f_len)} in is {(d_len + f_len) / 12:.1f} ft).

## Also cut: spacer blocks (not strips), and what holds them

The wood blocks are the spacers that hold S4, S5, S6, the window frame (J1 to J4) and the nook frames V1 to V3 off the steel so every strip's back sits on the same line, 3 3/4 in off the body.

- **Size and stock: cut 1 1/2 in pieces off a 2x4** (a 2x4 is really 1 1/2 x 3 1/2 in) and stand each on its 3 1/2 in side, so the block is 1 1/2 x 1 1/2 in on the steel and 3 1/2 in out. The 1/8 in glue line under it makes the 3 5/8 in standoff, and the grain runs across the block, so the strip's screw goes into side grain (a block cut 3 5/8 long from 2x2 would take that screw in end grain, which holds about half as well).
- **Block to the steel: adhesive, not screws.** Nothing is drilled into the van's body. Use a polyurethane construction adhesive (the kind van builders use is Sikaflex 252 or a similar one; check the label for steel and for a bond line of about 1/8 in) or 3M VHB tape. Put it only on solid steel, away from the holes, and test one block on a scrap of your own steel (pull it off after a day) before you do the wall.
- **If you use polyurethane adhesive instead of tape (Sikaflex-252 is one):** Sika's data sheet gives an application range of 50 to 95 F (10 to 35 C), best at 59 to 77 F (15 to 25 C), a skin time of about 40 minutes and an open time of about 35 minutes at 73 F, so press each block on within half an hour and hold it (masking tape or a prop) until it has set; leave it a day or more before loading it. Painted steel may need Sika's primer or activator (see its pre-treatment chart, and test one block). The prep is the same as below: scuff, wipe off the dust, 70/30 isopropyl alcohol and water, dry. Do not use screws or rivnuts into the steel: at the dots it is the van's outer skin or a rib pressed from it, so a screw would go through the outside of the van.
- **If you use VHB tape, temperature:** apply it when the steel, the block and the tape are all between 70 and 100 F (21 to 38 C); do not apply it below about 50 F (10 C), where the adhesive is too stiff to wet the surface (some grades say 60 F). Warm the steel with the van heater or a heat lamp if you have to, keep it out of direct sun that heats the steel well past 100 F, and make sure there is no condensation on it. Once the tape is on, it holds in the cold.
- **If you use VHB tape, steel prep:** (1) remove loose paint, rust and dust, and make sure the factory paint under the tape is sound, because the tape is only as good as the paint it sticks to; (2) if the steel is oily or waxy, wipe it first with a degreaser or solvent; (3) scuff lightly to dull the gloss, with a gray (ultra fine) or maroon (very fine) Scotch-Brite pad or 400 to 420 grit sandpaper, only until the paint looks evenly dull and not through to bare steel (if you do hit bare steel, touch it up with a rust-inhibiting primer before taping), then wipe the dust off; (4) wipe with a 70/30 mix of isopropyl alcohol and water on a clean lint-free cloth, then wipe dry with another; (5) do not touch the cleaned spot. Seal the face of each wood block (a coat of polyurethane or similar, dry) or sand it smooth first, because raw wood is porous.
- **If you use VHB tape, applying it:** put the tape on the block first, press it firmly, peel the liner, set the block in place (no sliding it around), then press hard, about 15 psi, which on a 1 1/2 x 1 1/2 in block is about 35 lb, for a minute, and hold or brace it. The bond keeps building for a day or more, so leave the strips off it until the next day. Choose a foam thickness near 1/8 in (110 mil) so the 3 1/2 in block plus the tape is the 3 5/8 in standoff. Read the data sheet of the exact tape you buy: the numbers above are the ones 3M gives for its VHB tapes in general.
- **Strip to the block:** wood glue or construction adhesive plus one #8 x 1 1/2 in screw through the strip into the block.
- **How many:** {DRV_BLOCKS} on the driver side (S4 {len(AP['S4'])}, S5 {len(AP['S5'])}, S6 {len(AP['S6'])}, and {len(FRAME_BLK)} under the window frame, 3 under each of J1 to J4) and {PASS_BLOCKS} on the passenger side (S4 {len(PAP['S4'])}, S5 {sum(1 for x in PAP['S5'] if 31.25 <= x <= 74.5)} in the middle piece only, S6 {len(PAP['S6'])}, and 3 each under V1, V2 and V3), so **{tot_blocks}**. A 2x4x8 ft stick gives about {per_stick} blocks with a 1/8 in kerf, so **{blk_sticks} sticks** (some spare).
- **Where each one goes:** one at every dot of those strips, drawn as a dark square on the furring maps (diagram A for the driver side, diagram D for the passenger side) with the count printed on each strip.
- **S7 and S8** only need thin shims at their dots: 1/4 in thick for S7 and 5/8 in for S8 (1 1/2 x 1 1/2 in, cut from plywood), glued the same way: {tot_shims} in all (driver S7 {len(AP['S7'])} and S8 {len(AP['S8'])}, passenger S7 {len(PAP['S7'])} and S8 {len(PAP['S8'])}), drawn as light dashed squares.

## Things to check before you cut

- **S8 (76 3/4 in up) is above the finished ceiling.** The ceiling covering ends at 74 9/16 in at the wall, so S8 (76 to 77 1/2 in) would sit above it, hidden in the roof curve. I did not change it; decide whether you still want it before cutting the two S8 pieces on each side.
- **The side window position is an assumption, not a measurement.** The opening is already cut, but where it is on the wall is not in the plan: it is drawn {fr16(WIN_CX0)} to {fr16(WIN_CX1)} in from the back mark and {fr16(WIN_CZ0)} to {fr16(WIN_CZ1)} in up, centered over the dinette table. Measure the real hole's edges, put the numbers in the Side window sizes on the interactive page, rebuild, and cut S5, S6 and the four J pieces to what the real hole needs.
- The dot positions come from the steel map; if you move a shelf, cabinet, window or outlet, move the dots (and the joints) first.
- Cut the pieces a hair long and trim to the wall at the rear door and the cab wall; the datum at 154 could be off by 2 to 4 in (the diagrams say so).
'''
open(ROOT + '/furring-cut-list.md', 'w', encoding='utf-8').write(md)
print(f'furring-cut-list.md: {len(DRV_PIECES)} + {len(PASS_PIECES)} strip pieces, {len(WIN_FRAME)} window frame, {len(efr)} nook; {npieces} pieces, {stk} sticks, {tot_blocks} blocks, {tot_shims} shims')
