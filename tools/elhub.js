/* The hub board space (section 1b of the electric page). Two views: (1) the driver wall under the couch, rear of the gear cabinet, where a bigger board can go;
   (2) the closet's end panel (the east side of the gear cabinet, at 74 in along the wall) seen from the battery side, with what stands in front of it and the free zones.
   The plan's sizes (battery, gear, shelf, couch post blocks) come from the plan (pl); the TS-30 is from its listing (9.65 x 7.28 x 4.75 in); the other parts use typical sizes and are
   drawn dashed until the real ones are known. x = along the wall from the back mark, y = out from the driver wall, z = up. */
const INK = '#1b1a17';
function hubSVG(pl, esc) {
  const g = pl.gear, s = 21, W = 1070, H = 1140, o = [];
  const txt = (x, y, t, st = '') => `<text x="${x}" y="${y}" style="font-size:11.5px;fill:${INK};${st}">${esc(t)}</text>`;
  const defs = `<defs><pattern id="hubhat" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9a9a94" stroke-width="2"/></pattern></defs>`;
  o.push(defs);
  // ---------------------------------------------------------------- view 1: the driver wall under the couch (x 0 to 46)
  { const X0 = 60, Z0 = 450, PX = x => X0 + s * x, PZ = z => Z0 - s * z;
    const rect = (x0, x1, z0, z1, a) => `<rect x="${PX(x0)}" y="${PZ(z1)}" width="${s * (x1 - x0)}" height="${s * (z1 - z0)}" ${a}/>`;
    const ctr = (x0, x1, z0, z1, lines, st = '') => lines.map((t, i) => `<text x="${PX((x0 + x1) / 2)}" y="${PZ((z0 + z1) / 2) + 4 + (i - (lines.length - 1) / 2) * 13}" text-anchor="middle" style="font-size:11px;font-weight:${i ? 400 : 700};fill:${INK};${st}">${esc(t)}</text>`).join('');
    o.push(txt(24, 30, '1. A bigger board: the driver wall under the couch, just rear of the gear cabinet (seen from the aisle, rear doors on the left)', 'font-weight:700;font-size:13px'));
    o.push(txt(24, 48, 'The wall here is clear below the couch frame’s back rail (13 1/2 to 17 up), between the couch’s wall post blocks at 20 and the cabinet’s rear panel at 38 5/8: 17 3/4 in wide, about 12 in tall.', 'fill:#5F5E5A'));
    o.push(rect(0, 46, 0, 17, 'fill="#F3EFE4" stroke="#8a8a84" stroke-width="1.6"'));
    o.push(rect(0, 46, 13.5, 17, 'fill="#D9C9A6" fill-opacity=".8" stroke="#8a6a3a" stroke-width="1.2"')); o.push(txt(PX(0.5), PZ(15.2) + 4, 'couch frame back rail (13 1/2 to 17 up)', 'font-size:10.5px;fill:#6b3a00'));
    [8, 20, 41].forEach(x => o.push(rect(x - .75, x + .75, 0, 13.5, 'fill="#B89B6A" stroke="#6b3a00" stroke-width="1.2"')));
    o.push(txt(PX(8) - 22, PZ(0) - 6 - 0, 'post', 'font-size:10px;fill:#6b3a00')); o.push(txt(PX(20) - 10, PZ(0) - 6, 'post', 'font-size:10px;fill:#6b3a00'));
    o.push(rect(42, 46, 0, 7.5, 'fill="url(#hubhat)" stroke="#6b6b66" stroke-width="1.4"')); o.push(txt(PX(42.2), PZ(8.3), 'wheel well', 'font-size:10.5px'));
    o.push(rect(38.65, 39.4, 0, 17, 'fill="#8a5a2b"')); o.push(txt(PX(31.2), PZ(17) - 24 + 18, '', ''));
    o.push(txt(PX(39.6), PZ(3), 'gear cabinet', 'font-size:10.5px;fill:#6b3a00'));
    o.push(rect(4.75, 13.25, 10.75, 16.75, 'fill="none" stroke="#B45309" stroke-width="1.4" stroke-dasharray="4 3"')); o.push(txt(PX(4.9), PZ(10.75) + 12, 'shore inlet plate (outside)', 'font-size:9.5px;fill:#B45309'));
    // the board
    o.push(rect(21.3, 38.1, 1.3, 13.2, 'fill="#E7D3A8" fill-opacity=".55" stroke="#8a6a3a" stroke-width="2.4"')); o.push(txt(PX(21.6), PZ(13.2) - 6, 'AC and 12 V board: 16 3/4 x 11 3/4 in, plywood, fixed to blocking behind the furring rails', 'font-weight:700;font-size:11px'));
    const part = (x0, x1, z0, z1, lines, real, col) => { o.push(rect(x0, x1, z0, z1, `fill="${col}" fill-opacity=".92" stroke="${INK}" stroke-width="${real ? 2.4 : 1.6}"${real ? '' : ' stroke-dasharray="5 3"'}`)); o.push(ctr(x0, x1, z0, z1, lines)); };
    part(21.6, 28.88, 2.3, 11.95, ['TS-30', 'transfer', 'switch', '7 1/4 x 9 5/8', '4 3/4 deep', 'on end'], true, '#DCEBFA');
    part(29.4, 36.4, 7.6, 12.6, ['AC panel', '7 x 5 (typical)'], false, '#EDEDED');
    part(29.4, 35.4, 2.6, 6.1, ['10-way fuse', 'block', '6 x 3 1/2 (typical)'], false, '#EDEDED');
    // scale
    for (let x = 0; x <= 45; x += 5) o.push(`<line x1="${PX(x)}" y1="${Z0}" x2="${PX(x)}" y2="${Z0 + 6}" stroke="${INK}"/>` + txt(PX(x) - 6, Z0 + 20, String(x)));
    o.push(txt(PX(14), Z0 + 38, 'inches along the wall from the back mark', 'fill:#5F5E5A'));
    for (let z = 0; z <= 15; z += 5) o.push(`<line x1="${60 - 6}" y1="${PZ(z)}" x2="60" y2="${PZ(z)}" stroke="${INK}"/>` + txt(24, PZ(z) + 4, String(z)));
    o.push(txt(PX(0.5), PZ(1.5) + 2, '', ''));
    ['Why here: room for the TS-30 (4 3/4 in deep, so about 5 1/2 in off the wall with the board), the AC panel and the fuse block, with gaps for the wiring;', 'open to the aisle through the couch front; the shore inlet (9 in along) is 12 to 30 in away (it is 64 in away at the cabinet end). It needs blocking behind the', 'furring rails, and the lawn chairs must still clear it (the plan\u2019s check does not know about this board yet).'].forEach((t, i) => o.push(txt(24, Z0 + 62 + i * 15, t, 'font-size:11px')));
  }
  // ---------------------------------------------------------------- view 2: the closet's end panel (the east side of the gear cabinet) at 74 in
  { const X0 = 60, Z0 = 1040, PX = y => X0 + s * y, PZ = z => Z0 - s * z;
    const rect = (y0, y1, z0, z1, a) => `<rect x="${PX(y0)}" y="${PZ(z1)}" width="${s * (y1 - y0)}" height="${s * (z1 - z0)}" ${a}/>`;
    const ctr = (y0, y1, z0, z1, lines, st = '') => lines.map((t, i) => `<text x="${PX((y0 + y1) / 2)}" y="${PZ((z0 + z1) / 2) + 4 + (i - (lines.length - 1) / 2) * 13}" text-anchor="middle" style="font-size:11px;font-weight:${i ? 400 : 700};fill:${INK};${st}">${esc(t)}</text>`).join('');
    o.push(txt(24, 590, '2. The DC parts stay by the battery: the closet’s end panel (the east side of the gear cabinet, at 74 in), seen from the battery side looking toward the cab', 'font-weight:700;font-size:13px'));
    o.push(txt(24, 608, 'Driver wall on the left, aisle on the right. 26 in wide, 17 in tall. This panel cannot be made bigger: what stands in front of it leaves only the green zones.', 'fill:#5F5E5A'));
    o.push(rect(0, 26, 0, 17, 'fill="#F3E6CC" stroke="#8a6a3a" stroke-width="2.2"'));
    o.push(rect(0, 7, 0, 7.5, 'fill="url(#hubhat)" stroke="#6b6b66" stroke-width="1.6"')); o.push(ctr(0, 7, 0, 7.5, ['wheel well']));
    o.push(rect(7, 17, 0, 9.5, 'fill="#E4E4E0" fill-opacity=".92" stroke="#6b6b66" stroke-width="1.6" stroke-dasharray="6 4"')); o.push(ctr(7, 17, 0, 9.5, ['battery', '1 in off the panel']));
    o.push(rect(g.sh.y0, g.sh.y1, g.sh.z0, g.sh.z1, 'fill="#8a5a2b"')); o.push(txt(PX(g.sh.y0) + 3, PZ(g.sh.z1) + 11, 'gear shelf', 'font-size:10px;fill:#fff;font-weight:700'));
    ['inv', 'dc', 'ch'].forEach(k => { const b = g[k]; o.push(rect(b.y0, b.y1, b.z0, b.z1, 'fill="#FFF1D6" fill-opacity=".9" stroke="#B45309" stroke-width="1.6" stroke-dasharray="5 3"')); });
    o.push(ctr(g.inv.y0, g.inv.y1, g.inv.z0, g.inv.z1, ['inverter', '1 5/8 in off'])); o.push(ctr(g.ch.y0, g.ch.y1, g.ch.z0, g.ch.z1, ['charger', '23 in off']));
    const zone = (y0, y1, z0, z1) => o.push(rect(y0, y1, z0, z1, 'fill="#2E7D32" fill-opacity=".10" stroke="#2E7D32" stroke-width="2" stroke-dasharray="8 4"'));
    zone(17, 26, 0, 10.4); zone(0, 7.75, 7.5, 17); zone(7.75, 26, 15.6, 17);
    o.push(txt(PX(17.3), PZ(10.4) + 14, 'zone A (deep): spare', 'font-weight:700;fill:#2E7D32')); o.push(txt(PX(0.3), PZ(17) + 14, 'zone C (deep)', 'font-weight:700;fill:#2E7D32')); o.push(txt(PX(23), PZ(16.2), 'top slot', 'font-weight:700;fill:#2E7D32;font-size:10.5px'));
    const part = (y0, y1, z0, z1, lines, col) => { o.push(rect(y0, y1, z0, z1, `fill="${col}" fill-opacity=".9" stroke="${INK}" stroke-width="1.6" stroke-dasharray="5 3"`)); o.push(ctr(y0, y1, z0, z1, lines)); };
    part(1, 6.5, 9.6, 12.3, ['Class T holder', '5 1/2 x 2 1/2 (typical)'], '#EDEDED');
    part(1, 6.3, 12.8, 15.9, ['500 A shunt', '5 x 3 (typical)'], '#EDEDED');
    part(8.6, 14.6, 15.7, 16.9, ['+ bus bar (typical)'], '#F6D9D9');
    part(16.4, 22.4, 15.7, 16.9, ['− bus bar (typical)'], '#D9D9F6');
    for (let y = 0; y <= 25; y += 5) o.push(`<line x1="${PX(y)}" y1="${Z0}" x2="${PX(y)}" y2="${Z0 + 6}" stroke="${INK}"/>` + txt(PX(y) - 5, Z0 + 20, String(y)));
    o.push(txt(PX(8), Z0 + 38, 'inches out from the driver wall', 'fill:#5F5E5A'));
    for (let z = 0; z <= 15; z += 5) o.push(`<line x1="54" y1="${PZ(z)}" x2="60" y2="${PZ(z)}" stroke="${INK}"/>` + txt(24, PZ(z) + 4, String(z)));
    const side = ['Why not one big board on this panel:', 'the battery ends 1 in off the panel, the inverter 1 5/8 in,', 'and the shelf (z 10 1/2 to 11) and its end rail slide along the', 'face (the rail is within 5/8 in of it), so', 'most of the face has 0 to 1 5/8 in in front of it. The', 'free space is zone A (9 x 10 1/2, deep, beside the battery),', 'zone C (7 3/4 x 9 1/2, deep, above the wheel well) and a', '1 3/8 in slot across the top, above the gear, for flat parts.', '', 'So: the DC parts that must be near the battery post stay', 'here (the Class T holder within 7 in of it, the shunt, the', 'two bus bars if they are 1 3/8 in tall or less); the AC panel,', 'the TS-30 and the fuse block go to the board on the wall.'];
    side.forEach((t, i) => o.push(txt(640, 665 + i * 15, t, i === 0 ? 'font-weight:700' : 'font-size:11px')));
    ['Dashed parts use typical sizes (the TS-30 is from its listing): send me the real ones. One big board on the wall instead would put the bus bars and the', 'Class T 20 to 30 in from the battery: about 2 1/2 ft more 2/0 cable on each of the three runs.'].forEach((t, i) => o.push(txt(24, 1108 + i * 14, t, 'font-size:10.5px;fill:#5F5E5A')));
  }
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Hub board space: a bigger board on the driver wall under the couch, and the closet end panel with its free zones"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

// ---------------------------------------------------------------- section 1c: the user's real board (photo IMG_0143) on the pull-out tray, seen from above
function trayTopSVG(pl, esc) {
  const g = pl.gear, s = 19, X0 = 70, Y0 = 118, W = 1070, H = 900, o = [];
  const PX = x => X0 + s * (x - 36), PY = y => Y0 + s * y;
  const rect = (x0, x1, y0, y1, a) => `<rect x="${PX(x0)}" y="${PY(y0)}" width="${s * (x1 - x0)}" height="${s * (y1 - y0)}" ${a}/>`;
  const txt = (x, y, t, st = '') => `<text x="${x}" y="${y}" style="font-size:11.5px;fill:#1b1a17;${st}">${esc(t)}</text>`;
  const ctr = (x0, x1, y0, y1, lines, st = '') => lines.map((t, i) => `<text x="${PX((x0 + x1) / 2)}" y="${PY((y0 + y1) / 2) + 4 + (i - (lines.length - 1) / 2) * 13}" text-anchor="middle" style="font-size:11px;font-weight:${i ? 400 : 700};fill:#1b1a17;${st}">${esc(t)}</text>`).join('');
  o.push(`<defs><pattern id="trhat" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9a9a94" stroke-width="2"/></pattern><marker id="trar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#1b1a17"/></marker></defs>`);
  o.push(txt(24, 28, '1c. Your real board on the pull-out tray, seen from above (rear doors on the left, the driver wall at the top, the aisle at the bottom)', 'font-weight:700;font-size:13px'));
  o.push(txt(24, 46, 'Positions come from your photo, scaled with the inverter and the shore charger as rulers: good to about 2 in. The dashed grey box is the battery under the tray.', 'fill:#5F5E5A'));
  o.push(rect(36, 78, 0, 26.5, 'fill="#F3EFE4" stroke="none"'));
  o.push(`<line x1="${PX(36)}" y1="${PY(0)}" x2="${PX(78)}" y2="${PY(0)}" stroke="#1b1a17" stroke-width="3"/>`); o.push(txt(PX(36) + 4, PY(0) - 6, 'driver wall', 'font-weight:700'));
  o.push(rect(42, 76, 0, 7, 'fill="url(#trhat)" stroke="#6b6b66" stroke-width="1.5"'));
  o.push(rect(52, 73, 7, 17, 'fill="#E4E4E0" fill-opacity=".9" stroke="#6b6b66" stroke-width="1.6" stroke-dasharray="6 4"'));
  o.push(rect(38.65, 39.4, 0, 26, 'fill="#8a5a2b"')); o.push(txt(PX(38.65) - 4, PY(26) + 16, 'divider', 'font-size:10.5px;fill:#6b3a00'));
  o.push(rect(74, 74.8, 0, 26, 'fill="#8a5a2b"')); o.push(txt(PX(72), PY(26) + 16, 'closet end panel', 'font-size:10.5px;fill:#6b3a00'));
  o.push(rect(g.sh.x0, g.sh.x1, g.sh.y0, g.sh.y1, 'fill="#E7D3A8" fill-opacity=".6" stroke="#8a6a3a" stroke-width="2.2" stroke-dasharray="7 4"'));
  o.push(txt(PX(40.3), PY(g.sh.y1) + 14, 'the tray (a 1/2 in plywood tray on two 18 in slides): 33 x 17 1/2 in, 7 3/4 to 25 1/4 in out', 'font-size:10.5px;font-weight:700;fill:#6b3a00'));
  // the parts, mapped from the photo: van x = 49.4 + board x, van y = 9.05 + board y
  const part = (x0, x1, y0, y1, lines, col) => { o.push(rect(x0, x1, y0, y1, `fill="${col}" fill-opacity=".93" stroke="#1b1a17" stroke-width="2"`)); o.push(ctr(x0, x1, y0, y1, lines)); };
  part(48.3, 56.3, 9.75, 23.55, ['BELTTT', 'inverter', '2000 W'], '#FFD9A8');
  part(59.9, 71.1, 8.55, 15.15, ['LiTime 60 A DC-DC', '(turned end for end:', 'input on the right)'], '#CFE3FA');
  part(62.2, 72.5, 17.45, 25.05, ['VEVOR 80 A', 'shore charger'], '#D5EFD9');
  part(57.0, 59.2, 9.85, 14.65, ['red', 'bus'], '#F6C9C9');
  part(57.1, 58.9, 20.65, 24.95, ['black', 'bus'], '#CFCFD9');
  part(71.1, 73.3, 7.75, 10.25, ['100 A', 'brkr'], '#E6D2F2');
  o.push(rect(40.05, 48.0, 7.75, 25.25, 'fill="#2E7D32" fill-opacity=".08" stroke="#2E7D32" stroke-width="2" stroke-dasharray="8 4"')); o.push(ctr(40.05, 48.0, 7.75, 25.25, ['spare tray', '8 x 17 1/2 in', '', 'room for', 'loops or', 'later parts']));
  // the fixed parts on the end panel, and the wall board
  o.push(rect(72.2, 74, 1, 6.6, 'fill="#EDEDED" stroke="#1b1a17" stroke-width="1.6" stroke-dasharray="4 3"'));
  o.push(`<rect x="${PX(55.4)}" y="${PY(1.2)}" width="${s * 15.6}" height="${s * 4.4}" rx="5" fill="#fff" fill-opacity=".93" stroke="#1b1a17" stroke-width="1.2"/>`);
  o.push(txt(PX(55.8), PY(2.9), 'Class T holder and shunt: fixed on the end panel,', 'font-size:10.5px')); o.push(txt(PX(55.8), PY(4.6), 'above the wheel well (zone C in section 1b)', 'font-size:10.5px'));
  o.push(`<path d="M${PX(71.1)} ${PY(3.4)} L${PX(72.1)} ${PY(3.4)}" stroke="#1b1a17" stroke-width="1.5" marker-end="url(#trar)"/>`);
  o.push(`<rect x="${PX(40)}" y="${PY(0.7)}" width="${s * 15.2}" height="${s * 2.8}" rx="5" fill="#fff" fill-opacity=".93" stroke="#B45309" stroke-width="1.2"/>`);
  o.push(txt(PX(40.4), PY(2.0), '← the AC and 12 V board is on the wall at 21 to 38 in:', 'font-size:10.5px;font-weight:700;fill:#B45309')); o.push(txt(PX(40.4), PY(3.1), 'TS-30, AC panel and fuse block (section 1b)', 'font-size:10.5px;font-weight:700;fill:#B45309'));
  for (let x = 40; x <= 75; x += 5) o.push(`<line x1="${PX(x)}" y1="${PY(26.5)}" x2="${PX(x)}" y2="${PY(26.5) + 5}" stroke="#1b1a17"/>` + txt(PX(x) - 7, PY(26.5) + 36, String(x)));
  o.push(txt(PX(48), PY(26.5) + 54, 'inches along the wall from the back mark', 'fill:#5F5E5A'));
  const notes = [
    'What this shows',
    '1. Your arrangement fits the tray: about 24 x 17 1/2 in (the photo’s board with the parts hanging over its edges) against the tray’s 33 x 17 1/2,',
    '    with 8 in spare at the rear end. Mount the parts on the tray itself (cut your plywood down to it).',
    '2. The red bus bar lands over the battery, so the battery cables are a few inches long, as the plan wanted (the tray is 1 in over the battery top).',
    '3. Not on the tray: the Class T fuse and the shunt (fixed on the end panel by the battery, so the Class T stays within 7 in of the post),',
    '    and the TS-30, the AC panel and the fuse block (the wall board).',
    '4. Everything that runs to the tray needs a slack loop of about 24 in so it can slide 18 in: the two battery cables, the starter battery cable',
    '    (with its 100 A breaker), the shore AC to the shore charger, the inverter AC out, the 12 V feed (WR13) and the remote cable.',
    '    The bus bars now slide with the tray, so the two battery cables need the most slack.',
    '5. To check: the board size (measure it), the real size of the DC-DC (the plan had 16 x 9, the photo looks closer to 11 x 6 1/2),',
    '    the cable (the photo shows 1/0 where the plan has 2/0), and the weight on the slides.'];
  notes.forEach((t, i) => o.push(txt(24, 690 + i * 16, t, i === 0 ? 'font-weight:700;font-size:13px' : 'font-size:11.5px')));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Your real board on the pull-out tray, seen from above"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
module.exports = { hubSVG, trayTopSVG };
