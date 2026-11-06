/* The hub board space (section 1b of the electric page). Two views: (1) the divider panel (the tray's rear side wall), its outer face, where the TS-30, the AC panel and the fuse block go;
   (2) the closet's end panel (the east side of the gear cabinet, at 74 in along the wall) seen from the battery side, with what stands in front of it and the free zones.
   The plan's sizes (battery, gear, shelf, couch post blocks) come from the plan (pl); the TS-30 is from its listing (9.65 x 7.28 x 4.75 in); the other parts use typical sizes and are
   drawn dashed until the real ones are known. x = along the wall from the back mark, y = out from the driver wall, z = up. */
const INK = '#1b1a17';
function hubSVG(pl, esc) {
  const g = pl.gear, s = 21, W = 1070, H = 1140, o = [];
  const txt = (x, y, t, st = '') => `<text x="${x}" y="${y}" style="font-size:11.5px;fill:${INK};${st}">${esc(t)}</text>`;
  const defs = `<defs><pattern id="hubhat" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9a9a94" stroke-width="2"/></pattern></defs>`;
  o.push(defs);
  // ---------------------------------------------------------------- view 1: the divider panel (the tray's rear side wall), its outer face, seen from the rear doors
  { const X0 = 120, Z0 = 450, PX = y => X0 + s * y, PZ = z => Z0 - s * z;       // y = out from the driver wall (left to right), z = up
    const rect = (y0, y1, z0, z1, a) => `<rect x="${PX(y0)}" y="${PZ(z1)}" width="${s * (y1 - y0)}" height="${s * (z1 - z0)}" ${a}/>`;
    const ctr = (y0, y1, z0, z1, lines, st = '') => lines.map((t, i) => `<text x="${PX((y0 + y1) / 2)}" y="${PZ((z0 + z1) / 2) + 4 + (i - (lines.length - 1) / 2) * 13}" text-anchor="middle" style="font-size:11px;font-weight:${i ? 400 : 700};fill:${INK};${st}">${esc(t)}</text>`).join('');
    o.push(txt(24, 30, 'EF3 · The TS-30, the AC panel and the fuse block go on the divider panel, the tray’s rear side wall: its outer face, seen from the rear doors (driver wall on the left)', 'font-weight:700;font-size:13px'));
    o.push(txt(24, 48, 'The divider is 26 in wide and 17 in tall (floor to the couch deck), the board the tray’s rear slide bolts to. Its outer face looks into open space under the couch.', 'fill:#5F5E5A'));
    o.push(rect(0, 26, 0, 17, 'fill="#D9B47A" stroke="#8a6a3a" stroke-width="2.4"'));
    o.push(txt(PX(0.4), PZ(17) - 6, 'the divider (3/4 in plywood), outer face. The slide and the tray are on its other face, so screws here must not go through.', 'font-size:10.5px;fill:#5a3a10'));
    // the parts
    const part = (y0, y1, z0, z1, lines, real, col) => { o.push(rect(y0, y1, z0, z1, `fill="${col}" fill-opacity=".95" stroke="${INK}" stroke-width="${real ? 2.4 : 1.6}"${real ? '' : ' stroke-dasharray="5 3"'}`)); o.push(ctr(y0, y1, z0, z1, lines)); };
    part(1.5, 8.78, 2.5, 12.15, ['TS-30', 'transfer switch', '7 1/4 x 9 5/8', '4 3/4 deep', 'on end'], true, '#DCEBFA');
    part(10.5, 17.5, 6.4, 11.4, ['AC panel', '7 x 5 (typical)', '3 deep'], false, '#EDEDED');
    part(19, 25, 2.6, 6.1, ['10-way fuse block', '6 x 3 1/2 (typical)', '2 deep'], false, '#EDEDED');
    o.push(rect(10.5, 25, 12.6, 16.2, 'fill="none" stroke="#2E7D32" stroke-width="2" stroke-dasharray="7 4"')); o.push(ctr(10.5, 25, 12.6, 16.2, ['room for breakers, a wire', 'gutter or the shore cable'], 'fill:#2E7D32;font-size:10px'));
    // the holes to the tray
    o.push(`<circle cx="${PX(9.7)}" cy="${PZ(13.8)}" r="9" fill="#fff" stroke="${INK}" stroke-width="1.6" stroke-dasharray="3 2"/>`); o.push(txt(PX(9.7) - 62, PZ(13.8) + 24, 'grommet hole to the tray', 'font-size:9.5px'));
    for (let y = 0; y <= 25; y += 5) o.push(`<line x1="${PX(y)}" y1="${Z0}" x2="${PX(y)}" y2="${Z0 + 6}" stroke="${INK}"/>` + txt(PX(y) - 5, Z0 + 20, String(y)));
    o.push(txt(PX(5), Z0 + 38, 'inches out from the driver wall (left) toward the aisle (right)', 'fill:#5F5E5A'));
    for (let z = 0; z <= 15; z += 5) o.push(`<line x1="${X0 - 6}" y1="${PZ(z)}" x2="${X0}" y2="${PZ(z)}" stroke="${INK}"/>` + txt(X0 - 30, PZ(z) + 4, String(z)));
    ['Why here: the divider face is 26 x 17 in and clear, so the TS-30 (4 3/4 in deep), the AC panel and the fuse block fit with gaps for the wiring.', 'It is right beside the tray: the inverter\u2019s AC out and the shore charger\u2019s AC in are a few inches of cable through grommets in the divider,', 'and the shore inlet (9 in along, 15 3/4 up) is about 30 in away. The cables to the tray need the slack loop for the slide.', 'Open to the aisle under the couch front. The 12 V circuits leave from the fuse block and the 120 V ones from the AC panel, up the walls to the ceiling.'].forEach((t, i) => o.push(txt(24, Z0 + 62 + i * 15, t, 'font-size:11px')));
  }
  // ---------------------------------------------------------------- view 2: the closet's end panel (the east side of the gear cabinet) at 74 in
  { const X0 = 60, Z0 = 1040, PX = y => X0 + s * y, PZ = z => Z0 - s * z;
    const rect = (y0, y1, z0, z1, a) => `<rect x="${PX(y0)}" y="${PZ(z1)}" width="${s * (y1 - y0)}" height="${s * (z1 - z0)}" ${a}/>`;
    const ctr = (y0, y1, z0, z1, lines, st = '') => lines.map((t, i) => `<text x="${PX((y0 + y1) / 2)}" y="${PZ((z0 + z1) / 2) + 4 + (i - (lines.length - 1) / 2) * 13}" text-anchor="middle" style="font-size:11px;font-weight:${i ? 400 : 700};fill:${INK};${st}">${esc(t)}</text>`).join('');
    o.push(txt(24, 590, 'EF4 · The DC parts stay by the battery: the closet’s end panel (the east side of the gear cabinet, at 74 in), seen from the battery side looking toward the cab', 'font-weight:700;font-size:13px'));
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
    const side = ['Why not one big board on this panel:', 'the battery ends 1 in off the panel, the inverter 1 5/8 in,', 'and the shelf (z 10 1/2 to 11) and its end rail slide along the', 'face (the rail is within 5/8 in of it), so', 'most of the face has 0 to 1 5/8 in in front of it. The', 'free space is zone A (9 x 10 1/2, deep, beside the battery),', 'zone C (7 3/4 x 9 1/2, deep, above the wheel well) and a', '1 3/8 in slot across the top, above the gear, for flat parts.', '', 'So: the DC parts that must be near the battery post stay', 'here (the Class T holder within 7 in of it, the shunt, the', 'two bus bars if they are 1 3/8 in tall or less); the TS-30,', 'the AC panel and the fuse block go on the divider (EF3).'];
    side.forEach((t, i) => o.push(txt(640, 665 + i * 15, t, i === 0 ? 'font-weight:700' : 'font-size:11px')));
    o.push(txt(24, 1108, 'Dashed parts use typical sizes (the TS-30 is from its listing): send me the real ones.', 'font-size:10.5px;fill:#5F5E5A'));
  }
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Hub board space: a bigger board on the driver wall under the couch, and the closet end panel with its free zones"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}

const TRAY_PARTS = [
  { k: 'inv', n: 'BELTTT inverter 2000 W', short: ['BELTTT', 'inverter', '2000 W'], x0: 47.5, x1: 55.5, z0: 9.75, z1: 23.55, h: 3.9, c: 0xFFB45A, col: '#FFD9A8' },
  { k: 'dc', n: 'LiTime 60 A DC-DC charger', short: ['LiTime 60 A DC-DC', '(turned end for end:', 'input on the right)'], x0: 59.1, x1: 70.3, z0: 8.55, z1: 15.15, h: 4.5, c: 0x4F8FE0, col: '#CFE3FA' },
  { k: 'ch', n: 'VEVOR 80 A shore charger', short: ['VEVOR 80 A', 'shore charger'], x0: 61.4, x1: 71.7, z0: 17.45, z1: 25.05, h: 4, c: 0x4CAF6A, col: '#D5EFD9' },
  { k: 'rb', n: 'red (+) bus bar', short: ['red', 'bus'], x0: 56.2, x1: 58.4, z0: 9.85, z1: 14.65, h: 1.6, c: 0xD93025, col: '#F6C9C9' },
  { k: 'bb', n: 'black (\u2212) bus bar', short: ['black', 'bus'], x0: 56.3, x1: 58.1, z0: 20.65, z1: 24.95, h: 1.6, c: 0x2B2B2B, col: '#CFCFD9' },
  { k: 'br', n: '100 A breaker (the DC-DC\u2019s input)', short: ['100 A', 'brkr'], x0: 70.3, x1: 72.5, z0: 7.75, z1: 10.25, h: 3, c: 0x9C4FD0, col: '#E6D2F2' }];
// ---------------------------------------------------------------- section 1c: the user's real board (photo IMG_0143) on the pull-out tray, seen from above
function trayTopSVG(pl, esc) {
  const g = pl.gear, s = 19, X0 = 70, Y0 = 118, W = 1070, H = 900, o = [];
  const PX = x => X0 + s * (x - 31), PY = y => Y0 + s * y;
  const rect = (x0, x1, y0, y1, a) => `<rect x="${PX(x0)}" y="${PY(y0)}" width="${s * (x1 - x0)}" height="${s * (y1 - y0)}" ${a}/>`;
  const txt = (x, y, t, st = '') => `<text x="${x}" y="${y}" style="font-size:11.5px;fill:#1b1a17;${st}">${esc(t)}</text>`;
  const ctr = (x0, x1, y0, y1, lines, st = '') => lines.map((t, i) => `<text x="${PX((x0 + x1) / 2)}" y="${PY((y0 + y1) / 2) + 4 + (i - (lines.length - 1) / 2) * 13}" text-anchor="middle" style="font-size:11px;font-weight:${i ? 400 : 700};fill:#1b1a17;${st}">${esc(t)}</text>`).join('');
  o.push(`<defs><pattern id="trhat" width="7" height="7" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="7" stroke="#9a9a94" stroke-width="2"/></pattern><marker id="trar" markerWidth="9" markerHeight="9" refX="7" refY="4.5" orient="auto"><path d="M0 0 L9 4.5 L0 9 Z" fill="#1b1a17"/></marker></defs>`);
  o.push(txt(24, 28, 'EF5 · 1c. Your real board on the pull-out tray, seen from above (rear doors on the left, the driver wall at the top, the aisle at the bottom)', 'font-weight:700;font-size:13px'));
  o.push(txt(24, 46, 'Positions come from your photo, scaled with the inverter and the shore charger as rulers: good to about 2 in. The dashed grey box is the battery under the tray.', 'fill:#5F5E5A'));
  o.push(rect(31, 78, 0, 26.5, 'fill="#F3EFE4" stroke="none"'));
  o.push(`<line x1="${PX(31)}" y1="${PY(0)}" x2="${PX(78)}" y2="${PY(0)}" stroke="#1b1a17" stroke-width="3"/>`); o.push(txt(PX(31) + 4, PY(0) - 6, 'driver wall', 'font-weight:700'));
  o.push(rect(42, 76, 0, 7, 'fill="url(#trhat)" stroke="#6b6b66" stroke-width="1.5"'));
  o.push(rect(52, 73, 7, 17, 'fill="#E4E4E0" fill-opacity=".9" stroke="#6b6b66" stroke-width="1.6" stroke-dasharray="6 4"'));
  o.push(rect(38.65, 39.4, 0, 26, 'fill="#8a5a2b"')); o.push(txt(PX(38.65) - 4, PY(26) + 16, 'divider', 'font-size:10.5px;fill:#6b3a00'));
  o.push(rect(74, 74.8, 0, 26, 'fill="#8a5a2b"')); o.push(txt(PX(72), PY(26) + 16, 'closet end panel', 'font-size:10.5px;fill:#6b3a00'));
  o.push(rect(g.sh.x0, g.sh.x1, g.sh.y0, g.sh.y1, 'fill="#E7D3A8" fill-opacity=".6" stroke="#8a6a3a" stroke-width="2.2" stroke-dasharray="7 4"'));
  o.push(txt(PX(40.3), PY(g.sh.y1) + 14, 'the tray (a 1/2 in plywood tray on two 18 in slides): 33 x 17 1/2 in, 7 3/4 to 25 1/4 in out', 'font-size:10.5px;font-weight:700;fill:#6b3a00'));
  // the parts, mapped from the photo (van x = 48.6 + board x, van y = 9.05 + board y: moved back 0.8 in for the tray's end rail)
  TRAY_PARTS.forEach(q => { o.push(rect(q.x0, q.x1, q.z0, q.z1, `fill="${q.col}" fill-opacity=".93" stroke="#1b1a17" stroke-width="2"`)); o.push(ctr(q.x0, q.x1, q.z0, q.z1, q.short)); });
  o.push(rect(40.8, 47.2, 7.75, 25.25, 'fill="#2E7D32" fill-opacity=".08" stroke="#2E7D32" stroke-width="2" stroke-dasharray="8 4"')); o.push(ctr(40.8, 47.2, 7.75, 25.25, ['spare', '6 1/2 x', '17 1/2 in']));
  // the fixed parts on the end panel
  o.push(rect(72.2, 74, 1, 6.6, 'fill="#EDEDED" stroke="#1b1a17" stroke-width="1.6" stroke-dasharray="4 3"'));
  o.push(`<rect x="${PX(55.4)}" y="${PY(1.2)}" width="${s * 15.6}" height="${s * 4.4}" rx="5" fill="#fff" fill-opacity=".93" stroke="#1b1a17" stroke-width="1.2"/>`);
  o.push(txt(PX(55.8), PY(2.9), 'Class T holder and shunt: fixed on the end panel,', 'font-size:10.5px')); o.push(txt(PX(55.8), PY(4.6), 'above the wheel well (zone C in section 1b)', 'font-size:10.5px'));
  o.push(`<path d="M${PX(71.1)} ${PY(3.4)} L${PX(72.1)} ${PY(3.4)}" stroke="#1b1a17" stroke-width="1.5" marker-end="url(#trar)"/>`);
  // the TS-30, the AC panel and the fuse block on the divider's outer face (west of x = 38.65)
  o.push(rect(33.9, 38.65, 1.5, 8.78, 'fill="#DCEBFA" fill-opacity=".95" stroke="#1b1a17" stroke-width="2"')); o.push(rect(35.65, 38.65, 10.5, 17.5, 'fill="#EDEDED" fill-opacity=".95" stroke="#1b1a17" stroke-width="1.6" stroke-dasharray="5 3"')); o.push(rect(36.65, 38.65, 19, 25, 'fill="#EDEDED" fill-opacity=".95" stroke="#1b1a17" stroke-width="1.6" stroke-dasharray="5 3"'));
  o.push(ctr(33.9, 38.65, 1.5, 8.78, ['TS-30'])); o.push(ctr(35.65, 38.65, 10.5, 17.5, ['AC', 'panel'])); o.push(ctr(36.65, 38.65, 19, 25, ['fuse', 'block']));
  for (let x = 35; x <= 75; x += 5) o.push(`<line x1="${PX(x)}" y1="${PY(26.5)}" x2="${PX(x)}" y2="${PY(26.5) + 5}" stroke="#1b1a17"/>` + txt(PX(x) - 7, PY(26.5) + 36, String(x)));
  o.push(txt(PX(46), PY(26.5) + 54, 'inches along the wall from the back mark', 'fill:#5F5E5A'));
  const notes = [
    'What this shows',
    '1. Your arrangement fits the tray: about 24 x 17 1/2 in (the photo’s board with the parts hanging over its edges) against the tray’s 33 x 17 1/2,',
    '    with about 6 1/2 in spare at the rear end after the end rails. Mount the parts on the tray itself (cut your plywood down to it).',
    '2. The red bus bar lands over the battery, so the battery cables are a few inches long, as the plan wanted (the tray is 1 in over the battery top).',
    '3. Not on the tray: the Class T fuse and the shunt (fixed on the end panel by the battery, so the Class T stays within 7 in of the post);',
    '    the TS-30, the AC panel and the fuse block (on the divider, the tray\u2019s rear side wall, right beside the tray).',
    '4. Everything that runs to the tray needs a slack loop of about 24 in so it can slide 18 in: the two battery cables, the starter battery cable',
    '    (with its 100 A breaker), the shore AC to the shore charger, the inverter AC out, the 12 V feed (WR13) and the remote cable.',
    '    The bus bars now slide with the tray, so the two battery cables need the most slack.',
    '5. To check: the board size (measure it), the real size of the DC-DC (the plan had 16 x 9, the photo looks closer to 11 x 6 1/2),',
    '    the cable (the photo shows 1/0 where the plan has 2/0), and the weight on the slides.'];
  notes.forEach((t, i) => o.push(txt(24, 690 + i * 16, t, i === 0 ? 'font-weight:700;font-size:13px' : 'font-size:11.5px')));
  return `<svg viewBox="0 0 ${W} ${H}" role="img" aria-label="Your real board on the pull-out tray, seen from above"><style>text{font-family:-apple-system,"Segoe UI",sans-serif}</style>${o.join('')}</svg>`;
}
module.exports = { hubSVG, trayTopSVG, TRAY_PARTS };
