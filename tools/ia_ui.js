/* ================= checks ================= */
function computeChecks(L, V) {
  const P = L.P, out = [], push = (lv, t) => out.push({ lv, t });
  const O = obstacles(L, V), O0 = obstacles(L, {});
  const lvA = v => v < 0 ? 'bad' : v < 12 ? 'bad' : v < 16 ? 'warn' : 'ok';
  // dinette
  const dspace = L.bB[1] - L.bA[0];
  if (L.spare < -0.01) push('bad', `The two benches and the table are ${fmt(-L.spare)} in too long for the dinette space (${fmt(dspace)} in from the closet to the cab wall).`);
  else push('ok', `Dinette fits: ${fmt(dspace)} in of space, ${L.spare < .01 ? 'none left over' : fmt(L.spare) + ' in left over'}.`);
  // walkway, everything closed
  const a0 = aisleMin(L, O0);
  if (a0.v < 1e8) push(a0.v < 0 ? 'bad' : lvA(a0.v), a0.v < 0 ? `${cap(a0.dn)} and ${a0.qn} overlap by ${fmt(-a0.v)} in at ${fmt(a0.x)} in from the back.` : `Narrowest walkway, everything closed: ${fmt(a0.v)} in at ${fmt(a0.x)} in from the back (${a0.dn} against ${a0.qn}).`);
  // walkway right now
  const anyOpen = Object.keys(V).some(k => V[k] > .02);
  if (anyOpen) {
    const a1 = aisleMin(L, O);
    if (a1.v < 1e8) push(a1.v < 0 ? 'bad' : lvA(a1.v), a1.v < 0 ? `Right now ${a1.dn} and ${a1.qn} overlap by ${fmt(-a1.v)} in at ${fmt(a1.x)} in from the back.` : `Narrowest walkway right now: ${fmt(a1.v)} in at ${fmt(a1.x)} in from the back (${a1.dn} against ${a1.qn}).`);
  }
  // bed leaf
  const LEG = P.platform - .75 - .375 - .25, slotEnd = P.legIn + LEG + .25;
  push('ok', `Bed: a ${fmt(P.bedBack)} x ${fmt(P.bedLen)} in leaf of 3/4 in plywood on a hinge along the front edge of the deck, flipped out level with the deck (${fmt(P.platform - .75)} in) on 4 legs ${fmt(LEG)} in long, about ${fmt((P.bedLen - 3.25) / 3)} in apart, that lie in slots in the leaf (no rails) and land ${fmt(P.bedD + P.bedBack - P.legIn)} in out from the wall (${fmt(P.legIn)} in in from its free edge), with the back cushion on it (${fmt(P.bedD)} + ${fmt(P.bedBack)} = ${fmt(P.bedD + P.bedBack)} in wide). The seat is ${fmt(P.platform + P.mattress)} in by day and ${fmt(P.bedD - P.mattress)} in deep, and the bed ${fmt(P.platform - .75 + P.mattress)} in at night. The seat cushion comes off to flip it. Put the legs down before anyone sits on the free edge: with the legs up it levers on the hinge screws.`);
  if (slotEnd > P.bedBack - 1.5) push('warn', `The leg slots (${fmt(slotEnd)} in from the free edge) reach to within ${fmt(Math.max(0, P.bedBack - slotEnd))} in of the hinge; the leaf needs to be at least ${fmt(slotEnd + 1.5)} in wide, or the legs set in less.`);
  // wall lean
  if (P.leanOn) {
    const z0 = P.cabBot, z1 = L.ceilF, l0 = L.leanAt(z0), l1 = L.leanAt(z1), wc = P.vanW - 2 * L.leanAt(P.ceil), d = Math.abs(wc - P.ceilW);
    push(L.leanK <= 0 ? 'warn' : 'ok', `Wall lean: from your two widths (${fmt(P.leanW1)} in at ${fmt(P.leanZ1)} up, ${fmt(P.leanW2)} in at ${fmt(P.leanZ2)} up) each wall is straight up to about ${fmt(L.leanStart)} in (${fmt(P.vanW)} wide), then leans in ${(L.leanK * 12).toFixed(2)} in per foot, ${(Math.atan(L.leanK) * 180 / Math.PI).toFixed(1)} degrees: ${fmt(L.leanAt(P.ceil))} in each side by the bare roof, so ${fmt(wc)} in wide at ${fmt(P.ceil)} up. ${d <= .75 ? `That matches the ${fmt(P.ceilW)} in flat roof.` : `The flat roof is set to ${fmt(P.ceilW)} in; the lean says ${fmt(wc)}.`}`);
    const bk = P.cabBackIn, mk = P.microIn, m0 = L.leanAt(59), m1 = L.leanAt(69), yf = bk + P.cabDepth, d0 = yf - Math.max(bk, l0), d1 = yf - Math.max(bk, l1), ang = Math.atan((Math.max(bk, l1) - Math.max(bk, l0)) / (z1 - z0)) * 180 / Math.PI;
    if (bk <= .01) push('ok', `The driver side wall cabinets (${fmt(z0)} to ${fmt(z1)} in up) have open backs and sit against the leaning wall, so only their sides follow it: the wall is ${fmt(l0)} in in at the bottom of the cabinets and ${fmt(l1)} in at the top, so each side panel is ${fmt(d0)} in deep at the bottom and ${fmt(d1)} in at the top, the rear edge cut at about ${ang.toFixed(0)} degrees (${fmt(l1 - l0)} in over ${fmt(z1 - z0)} in); the front stays ${fmt(P.cabDepth)} in out from the widest wall line. The shelves and the top are ${fmt(d1)} in deep at the top. Scribe the sides to the real wall when you fit them.`);
    else push(bk < l1 - .01 ? 'bad' : 'ok', `The driver side wall cabinets (${fmt(z0)} to ${fmt(z1)} in up) have a solid back set in ${fmt(bk)} in from the wall: ${fmt(bk - l0)} in off the wall at the bottom and ${fmt(bk - l1)} in at the top${bk < l1 - .01 ? `: it would run into the wall by ${fmt(l1 - bk)} in` : ''}.`);
    {
      const cz = L.ceilF, cl = L.leanAt(cz), st = Math.min(Math.max(L.leanStart, 0), cz), cAng = Math.atan(L.leanK) * 180 / Math.PI;
      push('ok', `The closet (${fmt(P.closetD)} deep, ${fmt(cz)} in tall) has an open back, so its sides follow the wall too: ${fmt(P.closetD)} deep up to ${fmt(st)} in, then the rear edge leans in at about ${cAng.toFixed(0)} degrees to ${fmt(P.closetD - cl)} deep at the top (${fmt(cl)} in less over the last ${fmt(cz - st)} in).`);
    }
    push(mk < m1 - .01 ? 'bad' : 'ok', `The microwave (59 to 69 in up) is on a wall that leans in ${fmt(m0)} in at its bottom and ${fmt(m1)} in at its top; its back is set in ${fmt(mk)} in, so it is ${fmt(mk - m0)} in off the wall at the bottom and ${fmt(mk - m1)} in at the top${mk < m1 - .01 ? `: it would run into the wall by ${fmt(m1 - mk)} in` : ''}. A microwave has to sit level (its turntable and door seal are made for that), so it cannot lean with the wall: its back touches the wall at the top corner and leaves a ${fmt(m1 - m0)} in wedge behind its bottom (good for its vent and the cord). What follows the wall is everything built around it: the shelf, its side panels and any trim are cut to the same ${(Math.atan(L.leanK) * 180 / Math.PI).toFixed(0)} degree lean. The same wedge is behind the wall covering and the vertical planks.`);
  }
  // rib marks on the bare roof: each rib is a band ribW wide; an opening has to sit in the clear space between two bands
  if (L.ribs.length) {
    const bands = L.ribBands, over = (a0, a1) => bands.map((b, i) => [b, i]).filter(([b]) => a0 < b[1] && a1 > b[0]).map(([b, i]) => L.ribs[i]);
    const gaps = []; let prev = 0; bands.forEach((b, i) => { gaps.push([prev, b[0], i === 0 ? 'behind the first rib' : `between ribs ${fmt(L.ribs[i - 1])} and ${fmt(L.ribs[i])}`]); prev = b[1]; }); gaps.push([prev, P.ceilLen, 'in front of the last rib']);
    const gdesc = gaps.map(g => `${fmt(g[1] - g[0])} ${g[2]}`).join('; ');
    const fits = (w, from, to) => gaps.filter(g => g[1] - g[0] >= w - .01 && (g[0] + g[1]) / 2 >= from && (g[0] + g[1]) / 2 <= to).map(g => `${fmt((g[0] + g[1]) / 2)} (${g[2]}, ${fmt(g[1] - g[0] - w)} to spare)`);
    const units = [[L.fan, 'fan', 0, P.panW], [L.ac, 'air conditioner', 40 - 6 + 0, 70 - 6]];
    const bad = units.filter(([c]) => over(c.x - c.w / 2, c.x + c.w / 2).length);
    const msgs = units.map(([c, nm, f0, f1]) => { const o = over(c.x - c.w / 2, c.x + c.w / 2); const ok = fits(c.w, f0, f1); return o.length ? `The ${nm} opening (${fmt(c.w)} wide at ${fmt(c.x)}, ${fmt(c.x - c.w / 2)} to ${fmt(c.x + c.w / 2)}) overlaps the rib at ${o.map(fmt).join(', ')}; a ${fmt(c.w)} in opening fits the clear space centered at ${ok.length ? ok.join(' or ') : 'nowhere in the places you want it (use a smaller opening, or frame the rib out)'}.` : `The ${nm} opening clears the ribs.`; });
    push(bad.length ? 'warn' : 'ok', `Roof ribs: ${L.ribs.length} marked, each ${fmt(P.ribW)} wide (${P.ribRef === 'center' ? 'positions are the middles' : P.ribRef === 'front' ? 'positions are the edge nearest the cab' : 'positions are the edge nearest the back'}); clear space: ${gdesc}. ${msgs.join(' ')}`);
  }
  // roof arc (ribs 75 1/2 at the wall, 80 in the middle)
  {
    const fW = P.roofWallH - L.lining, fM = L.roofZ(P.vanW / 2) - L.lining, sag = L.roofSag;
    push(L.ceilF > fW + .01 ? 'warn' : 'ok', `Roof: the ribs are ${fmt(P.roofWallH)} in up at the wall and ${fmt(P.roofMidH)} in in the middle, so the roof rises ${fmt(sag)} in across ${fmt(L.roofW)} in (an arc of about ${L.roofR > 1e8 ? 'infinite' : fmt(L.roofR)} in radius). ${L.lining > 0 ? `With the ${fmt(L.lining)} in covering the finished ceiling is ${fmt(fW)} in at the wall and ${fmt(fM)} in in the middle. ` : ''}${L.ceilF > fW + .01 ? `The wall cabinets and the closet are cut for a flat ${fmt(L.ceilF)} in ceiling, ${fmt(L.ceilF - fW)} in above the finished ceiling at the wall, so they are too tall by that much there (or the covering is thinner at the wall). ` : ''}The ceiling is drawn flat at ${fmt(P.ceil)} in in the side views; the cross-section shows the arc. 1/4 in plywood bends across this arc easily (the slats run along the van, so each one stays at one height).`);
    push('ok', `Roof stack at the openings: the ribs hang ${fmt(P.ribDepth)} in below the steel, so the outside of the roof is ${fmt(P.roofWallH + P.ribDepth)} in up at the wall and ${fmt(P.roofMidH + P.ribDepth)} in in the middle; from the outside of the steel to the finished ceiling is the ${fmt(P.ribDepth)} in rib depth${L.lining > 0 ? ` plus the ${fmt(L.lining)} in covering` : ''} = ${fmt(P.ribDepth + L.lining)} in, plus the steel skin itself (a few hundredths of an inch). That is the thickness the fan and the air conditioner mounting kits clamp across and have to be framed for; compare it with each manual's range (not found yet).`);
    const under = (c, nm) => { const h = c.u / 2, dz = Math.abs(L.roofZ(c.y + h) - L.roofZ(c.y - h)); return `${nm} (${fmt(c.y)} across): the roof tilts about ${L.roofTilt(c.y).toFixed(1)} degrees there and drops ${fmt(dz)} in across its ${fmt(c.u)} in base`; };
    const worst = Math.max(Math.abs(L.roofZ(L.fan.y + L.fan.u / 2) - L.roofZ(L.fan.y - L.fan.u / 2)), Math.abs(L.roofZ(L.ac.y + L.ac.u / 2) - L.roofZ(L.ac.y - L.ac.u / 2)));
    push(worst > 2 ? 'warn' : 'ok', `Units on the curved roof: ${under(L.ac, 'air conditioner')}; ${under(L.fan, 'fan')}. A flat base on a tilted roof needs a curb or a shaped gasket to sit level and seal; check the manuals for the most curve each allows.`);
  }
  // wall covering: plywood sheets standing floor to ceiling on the furring strips, both side walls
  if (P.wallOn) {
    const P0sub = P.wallSub, len = P.cab + 6, h = L.ceilF, door = P.doorX + P.slideW > len ? 0 : P.slideW * P.slideH, area = (2 * len * h - door) / 144, wt = area * P.wallT / 12 * P.wallDens;
    const tall = P.sheetH >= h, sheetsD = Math.ceil(len / P.sheetW), sheetsP = Math.ceil((P.doorX + 6) / P.sheetW), sheets = sheetsD + sheetsP;
    const gaps = FURR.slice(1).map((z, i) => z - FURR[i]), maxGap = Math.max(...gaps);
    push(tall ? 'ok' : 'warn', `Wall covering: ${fmt(P.wallT)} in plywood on both side walls (${area.toFixed(0)} sq ft after the sliding door opening) takes about ${sheets} sheets of ${fmt(P.sheetW)} x ${fmt(P.sheetH)} in standing floor to ceiling (${sheetsD} on the driver side, ${sheetsP} on the passenger side; the pieces over the door and past it come out of the offcuts)${tall ? '' : `; the sheets are shorter than the ${fmt(h)} in wall, so there would be a horizontal joint`}. It weighs about ${Math.round(wt)} lb (more with adhesive and screws).`);
    push(maxGap <= P.wallSpan ? 'ok' : 'warn', `The furring strips are at most ${fmt(maxGap)} in apart (3, 12, 21 1/2, 30 1/4, 43 1/2, 57 1/4, 66, 76 3/4 in up), ${maxGap <= P.wallSpan ? 'within' : 'more than'} the ${fmt(P.wallSpan)} in the covering may span. Glue to every strip and put a screw with a finish washer (so the head does not pull through) about every 8 in along the strips, near the edges first; leave 1/16 in between sheets. ${P0sub ? `It takes ${fmt(P.wallT)} in off each side, so the inside width is ${fmt(P.vanW)} in (bare ${fmt(P.vanW + 2 * P.wallT)}) and every aisle is ${fmt(2 * P.wallT)} in narrower.` : `The ${fmt(P.vanW)} in inside width is taken as already measured to the covered wall, so nothing is subtracted.`}`);
  }
  // ceiling covering
  if (P.liningOn) {
    const area = P.ceilLen * P.ceilW, n = L.nSlats, out = L.slatOut.size, nEff = n - out, used = n * P.slatW + Math.max(0, n - 1) * P.slatGap, margin = (P.ceilW - used) / 2;
    const sheets = Math.ceil(area / 4608), stockIn = [96, 120, 144, 168, 192].find(v => v >= L.slatLen), pieces = Math.ceil(P.ceilLen / L.slatLen) * nEff;
    const wPly = area * P.plyT * .02, wSlat = nEff * P.ceilLen * P.slatW * P.slatT * .0162, wTot = wPly + wSlat;
    push('ok', `Ceiling covering: the ${fmt(P.plyT)} in plywood and ${fmt(P.slatT)} in slats take ${fmt(L.lining)} in, so the finished ceiling is ${fmt(L.ceilF)} in (bare ${fmt(P.ceil)}); the wall cabinets are ${fmt(L.ceilF - P.cabBot)} tall and the closet ${fmt(L.ceilF)} (they stop at the new ceiling).`);
    push(stockIn ? 'ok' : 'warn', `${fmt(P.ceilLen)} x ${fmt(P.ceilW)} in of ceiling (${(area / 144).toFixed(0)} sq ft) takes at least ${sheets} sheets of ${fmt(P.plyT)} in plywood (4 x 8 ft, laid long way) and ${nEff} slats ${fmt(P.slatW)} x ${fmt(P.slatT)} x ${fmt(L.slatLen)} in with ${fmt(P.slatGap)} in gaps (${fmt(margin)} in left at each side)${L.slatLen >= P.ceilLen ? ` and no joints; a ${fmt(L.slatLen)} in slat needs ${stockIn ? (stockIn / 12) + ' ft stock, ' + fmt(stockIn - L.slatLen) + ' in of waste each' : 'stock longer than 16 ft, which is not sold, so it must be joined'}` : `; ${pieces} pieces in all`}.`);
    push(wTot > 150 ? 'warn' : 'ok', `The covering weighs about ${Math.round(wTot)} lb (plywood about ${Math.round(wPly)}, pine slats about ${Math.round(wSlat)}; a hardwood would be about a third more), plus glue and screws, all above head height.`);
  }
  {
    const fit = P.lightD <= P.slatW + .01 || !P.liningOn;
    if (P.lightN > 0) push(fit ? 'ok' : 'warn', `Ceiling lights: ${L.lights.length} round lights ${fmt(P.lightD)} in across in ${Math.max(1, Math.round(P.lightRows))} row${P.lightRows > 1 ? 's' : ''} (${L.lights.map(l => fmt(l.x)).filter((v, i, a) => a.indexOf(v) === i).join(', ')} in from the back; rows ${L.chanY.length ? L.chanY.map(fmt).join(' and ') : '--'} in from the driver wall), each mounted on a slat${P.liningOn ? `, centered on a ${fmt(P.slatW)} in slat (${fmt((P.slatW - P.lightD) / 2)} in of wood left each side), so every slat stays whole${fit ? '' : `; the lights are wider than the slat (${fmt(P.slatW)} in): use a smaller light or wider slats`}` : ''}. A small hole through the ${fmt(P.plyT)} in plywood behind each one takes the wire to a switch; surface mounted they hang about 1/2 in below the slat faces, or recessed into the 1 in slat they add nothing.`);
    const outside = c => c.x - c.w / 2 < 0 || c.x + c.w / 2 > P.ceilLen || c.y - c.w / 2 < L.ceilOff || c.y + c.w / 2 > L.ceilOff + P.ceilW;
    const over = (a, b) => Math.abs(a.x - b.x) < (a.w + b.w) / 2 && Math.abs(a.y - b.y) < (a.w + b.w) / 2;
    const near = c => L.lights.filter(l => { const dx = Math.max(Math.abs(l.x - c.x) - c.w / 2, 0), dy = Math.max(Math.abs(l.y - c.y) - c.w / 2, 0); return Math.hypot(dx, dy) < P.lightD / 2 + 2; }).length;
    const panY = P.vanW - P.panD, onBath = L.fan.x >= 0 && L.fan.x <= P.panW && L.fan.y >= panY - .01, overhang = Math.max(0, panY - (L.fan.y - L.fan.w / 2), L.fan.x + L.fan.w / 2 - P.panW, -(L.fan.x - L.fan.w / 2));
    const prob = [];
    if (outside(L.fan) || outside(L.ac)) prob.push('a cutout reaches past the ceiling being covered');
    if (over(L.fan, L.ac)) prob.push('the fan and A/C cutouts overlap');
    if (near(L.fan) + near(L.ac) > 0) prob.push(`${near(L.fan) + near(L.ac)} light${near(L.fan) + near(L.ac) === 1 ? ' is' : 's are'} within 2 in of a cutout`);
    if (!onBath) prob.push('the center of the fan is not over the wet bath (36 x 24 against the passenger wall)');
    [[L.ac, 'air conditioner'], [L.fan, 'fan']].forEach(([c, nm]) => { const h = c.u / 2; if (c.x - h < 0 || c.x + h > P.ceilLen || c.y - h < L.ceilOff || c.y + h > L.ceilOff + P.ceilW) prob.push(`the ${fmt(c.u)} in ${nm} unit does not fit on the flat part of the roof (${fmt(P.ceilW)} wide)`); });
    if (Math.abs(L.ac.x - L.fan.x) < (L.ac.u + L.fan.u) / 2 && Math.abs(L.ac.y - L.fan.y) < (L.ac.u + L.fan.u) / 2) prob.push('the fan unit and the air conditioner unit overlap on the roof');
    push(prob.length ? 'warn' : 'ok', `Cutouts: shower fan ${fmt(L.fan.w)} x ${fmt(L.fan.w)} in at ${fmt(L.fan.x)} in from the back and ${fmt(L.fan.y)} across from the driver wall (${onBath ? `its center is over the wet bath${overhang > .1 ? `, with ${fmt(overhang)} in of the opening past the pan edge` : ''}` : 'NOT over the wet bath'}), and air conditioning ${fmt(L.ac.w)} x ${fmt(L.ac.w)} in at ${fmt(L.ac.x)} and ${fmt(L.ac.y)}. They go through the plywood and the slats${P.liningOn ? `, so the fan cuts ${L.slatsCut(L.fan)} slats and the A/C cuts ${L.slatsCut(L.ac)} (each cut slat becomes two pieces, ending at a framed curb)` : ''}.${prob.length ? ' Problem: ' + prob.join('; ') + '.' : ''} The air conditioner is the OutEquip 12 V cooling-only rooftop unit (white, non-ducted): 28.3 x 28.3 in on the roof, 6.3 in tall, 45 lb on the listing (the maker's sheet says 33 lb), a roof opening of at least 14.1 x 13.7 in (drawn at 14 1/4) and an indoor panel up to 14.5 x 10 in; the fan is the 2012 F36AR exhaust fan (white, 12 V DC): 17.7 x 17.7 in on the roof, 6.4 in tall, cutout 356 x 356 mm, which is 14.02 in (drawn 14 x 14). Both openings need a frame between the roof bows.`);
  }
  // dinette bed
  const dbw = Math.min(P.benchD, P.tableD), dbl = L.bB[1] - L.bA[0], cover = Math.min(100, 2 * P.benchLen * (P.backH - P.seatH) / Math.max(1, L.tableLen * P.tableD) * 100);
  push(dbl < 72 ? 'warn' : 'ok', `Dinette bed: ${fmt(dbl)} x ${fmt(dbw)} in with its top at ${fmt(P.seatH)} in: the table lowers to ${fmt(L.tableLow)} in and the two backrest cushions (${fmt(P.pillowT)} thick) lie on it so all three sections are level.${dbl < 72 ? ` It is ${fmt(72 - dbl)} in short of a 72 in adult bed, so it suits a child or a guest who curls up.` : ''}`);
  if (L.tableLen > 0) push(cover < 98 ? 'warn' : 'ok', `The two backrest cushions (${fmt(P.benchLen)} x ${fmt(P.backH - P.seatH)} in each) cover ${Math.round(cover)}% of the lowered table (${fmt(L.tableLen)} x ${fmt(P.tableD)} in)${cover < 98 ? '; add a filler cushion or a thicker table pad' : ''}.`);
  if (P.tableD < P.benchD - .01) push('warn', `The table (${fmt(P.tableD)} deep) is shallower than the benches (${fmt(P.benchD)}), so the dinette bed has a ${fmt(P.benchD - P.tableD)} in notch along its edge.`);
  push(P.cabBot - P.seatH < 24 ? 'warn' : 'ok', `${fmt(P.cabBot - P.seatH)} in between the dinette bed and the wall cabinets.`);
  // closet doors fully open
  const hx = P.hinge === 'rear' ? L.c0 + 0.125 : L.c1 - 0.125, wC = P.closetW - 0.25;
  const O1 = obstacles(L, { clo_lo: 1, clo_hi: 1 }), hits = doorHits(L, O1), r1 = aisleAt(L, O1, hx);
  const sw = wC * Math.sin(P.openAng * Math.PI / 180);
  if (hits.length) push('bad', `Closet doors opened to ${P.openAng} degrees run into ${[...new Set(hits)].join(' and ')}. Open them less, or use a bi-fold or flip-up door.`);
  else push(r1.v < 10 ? 'warn' : 'ok', `Closet doors open to ${P.openAng} degrees stick out ${fmt(sw)} in${r1.dm > 0 && r1.qm > 0 ? `, leaving ${fmt(r1.v)} in of walkway beside them` : ''}.`);
  // bed out and the shower
  const Ob = obstacles(L, { bed: 1 }), Obp = obstacles(L, { bed: 1, pan: 1 });
  const xs = Math.min(14, P.panW - 2), rb = aisleAt(L, Ob, xs), rbp = aisleAt(L, Obp, xs);
  if (rb.v < 0) push('warn', `With the bed made up (${fmt(P.bedD + P.bedBack)} in) the shower pan has to be tipped up: down it overlaps by ${fmt(-rb.v)} in; tipped up it leaves ${fmt(rbp.v)} in.`);
  else push('ok', `Bed made up (${fmt(P.bedD + P.bedBack)} in) leaves ${fmt(rb.v)} in in front of the shower pan.`);
  { const legY = P.bedD + P.bedBack - P.legIn, panEdge = P.vanW - P.panD, legX = 1; // the end leg at 1 in from the rear is across from the pan (the pan is panW long)
    push(panEdge - legY >= 0 ? 'ok' : 'warn', panEdge - legY >= 0 ? `The leg at the rear end of the leaf lands ${fmt(legY)} in out from the wall, ${fmt(panEdge - legY)} in short of the shower pan's front edge (${fmt(panEdge)} in) when the pan is down; the leaf edge hangs ${fmt(Math.max(0, P.bedD + P.bedBack - panEdge))} in over the pan.` : `The leg at the rear end of the leaf lands ${fmt(legY)} in out from the wall, ${fmt(-(panEdge - legY))} in over the shower pan (its front edge is at ${fmt(panEdge)} in), so with the pan down the leg stands on it; tip the pan up first.`); }
  // fold-out table
  const reach = L.sinkE + L.flapLen, left = P.cab - reach;
  if (left < -0.01) push('bad', `The fold-out table (${fmt(L.flapLen)} long) runs ${fmt(-left)} in past the cab wall.`);
  else push(left < .5 ? 'warn' : 'ok', `Fold-out table: ${fmt(L.flapLen)} long, reaching ${fmt(reach)} in from the back, ${fmt(left)} in short of the cab wall. Open, it closes off the sliding door entry (${fmt(L.entry)} in).`);
  const fold = P.flapH - (L.flapLen - .75);
  if (fold < 0) push('warn', `Folded down, the fold-out table (${fmt(L.flapLen)} long) is longer than its hinge height (${fmt(P.flapH)}) and would touch the floor by ${fmt(-fold)} in.`);
  const rF = aisleAt(L, obstacles(L, { flap: 1 }), L.sinkE + 1);
  if (rF.dm > 0 && rF.qm > 0 && rF.v < 14) push(rF.v < 8 ? 'bad' : 'warn', `With the fold-out table open only ${fmt(rF.v)} in is left between it and the ${rF.dn}.`);
  // foot ledge
  const lclr = P.flapH - .75 - P.ledgeH;
  if (P.ledgeH - .75 + L.ledgeTot > P.flapH + .01 && P.ledgeH - .75 + L.ledgeTot <= P.counterH - 1) push('warn', `Folded up, the ${fmt(L.ledgeTot)} in foot ledge reaches ${fmt(P.ledgeH - .75 + L.ledgeTot)} in up, ${fmt(P.ledgeH - .75 + L.ledgeTot - P.flapH)} in above the fold-out table's hinge (${fmt(P.flapH)} in), so that much of it shows above the folded-down table; shorten the ledge, set the foot platform nearer, or lower the ledge.`);
  if (L.ledgeTot > L.flapLen + .01) push('warn', `The foot ledge (${fmt(L.ledgeTot)} long) is longer than the fold-out table (${fmt(L.flapLen)}).`);
  else if (P.ledgeH - .75 + L.ledgeTot > P.counterH - 1) push('warn', `Folded up, the foot ledge (${fmt(P.ledgeH - .75 + L.ledgeTot)} in up) is taller than the cabinet end (${fmt(P.counterH)}).`);
  else push(lclr < 16 ? 'warn' : 'ok', `Foot ledge: a ${fmt(L.ledgeTot)} x ${fmt(P.sinkD)} in plate hinged on the cabinet end${P.ledgeOff > 0 ? `, with the ${fmt(P.ledgeLen)} in foot platform starting ${fmt(P.ledgeOff)} in from the end` : ''}, its outer edge ${fmt(L.ledgeTot)} in from the end (${fmt(L.sinkE)} to ${fmt(L.sinkE + L.ledgeTot)} in from the back). Its top is ${fmt(P.ledgeH)} in up and ${fmt(lclr)} in under the table${lclr < 16 ? ' (tight for knees)' : ''}; folded up it stands ${fmt(L.ledgeTot)} in tall in the end panel recess. The cab passenger seat is ${fmt(P.cabSeatH)} in up (see the next line). The cabinet base is full, so it folds up into the end panel.`);
  {
    const gap = P.flapH - P.cabSeatH, below = P.cabSeatH - P.ledgeH, swR = Math.hypot(P.cabSeatW / 2, P.cabSeatD / 2), swIn = swR - (P.cabSeatD / 2 - P.cabSeatOut), swFwd = swR - (P.cabSeatD / 2 + P.cabSeatFwd);
    push(gap < 9 || gap > 13 || P.cab - P.cabSeatOut - L.sinkE - L.flapLen < .5 ? 'warn' : 'ok', `Cab passenger seat: ${fmt(P.cabSeatH)} in up, so the fold-out table is ${fmt(gap)} in above the seat cushion (a dining table is usually about 11 to 12 in above its seat) and the foot ledge (${fmt(P.ledgeH)} in up) is ${fmt(below)} in below the seat. The seat sticks out ${fmt(P.cabSeatOut)} in past the cab wall, so at seat height the living area ends at ${fmt(P.cab - P.cabSeatOut)} in: the open table (to ${fmt(L.sinkE + L.flapLen)} in) leaves ${fmt(P.cab - P.cabSeatOut - L.sinkE - L.flapLen)} in to the seat and the entry is ${fmt(P.cab - P.cabSeatOut - L.sinkE)} in clear there. The seat back does not stick out; the seat is on a swivel. Swivel: the ${fmt(P.cabSeatW)} x ${fmt(P.cabSeatD)} in cushion turns about its pivot (at the middle of the cushion), so its corners sweep a circle ${fmt(swR)} in in radius; in the rearmost position they reach ${fmt(Math.max(0, swIn))} in past the cab wall into the living area (to ${fmt(P.cab - Math.max(0, swIn))} in) as it turns. At 17 in up the cushion passes under the table (${fmt(P.flapH - .75)} in up underneath) and over the foot ledge (${fmt(P.ledgeH)} in up), so the turn is clear of both. Turned in its rearmost position the corners reach into the entry, leaving ${fmt(P.cab - Math.max(0, swIn) - L.sinkE)} in to the sink cabinet end. Pulled all the way forward (the cushion rear edge ${fmt(P.cabSeatFwd)} in in front of the cab wall) the corners reach ${fmt(Math.abs(swFwd))} in ${swFwd > 0 ? 'past the cab wall into the living area' : 'short of the cab wall, so the turn does not enter the living area at all'}: slide the seat forward before turning it.`);
  }
  // tanks: the sink cabinet is open to the area beside it, so the fresh tank runs out of it; the hot tank is on a shelf over the wheel well with clear space each side
  {
    const wellEnd = P.hotShelf > .5 ? L.fr[1] : 76, gapL = L.hotX[0] - wellEnd, gapR = L.tankX[0] - L.hotX[1], hotTop = P.hotShelf + P.hotH, gal = (L.tankLen * P.tankD * P.tankH / 231).toFixed(1);
    const dAt = x => x <= L.angS ? P.cabD : Math.max(P.sinkD, P.cabD - L.slope * (x - L.angS)), room = Math.min(dAt(L.hotX[0]), dAt(L.hotX[1])) - .75 - P.hotBack - P.hotD;
    if (L.tankX[0] < 76.5) push('bad', `The fresh water tank starts at ${fmt(L.tankX[0])} in, over the wheel well (it runs to 76 in at the wall).`);
    else push('ok', `Fresh water tank: ${fmt(L.tankLen)} x ${fmt(P.tankD)} x ${fmt(P.tankH)} in on the floor (${fmt(L.tankX[0])} to ${fmt(L.tankX[1])} in), about ${gal} gal; it sits at the sink end against the cab-side end panel (partly in the open area beside the sink cabinet), and ${fmt(P.sinkD - .75 - P.tankD)} in of cabinet depth is left in front of it for the sink pipes (111 in from the back) and for reaching it. Full, it holds about ${Math.round(L.tankLen * P.tankD * P.tankH / 231 * 8.34)} lb of water; with the ${L.hotGal.toFixed(1)} gal hot tank the water on the passenger side weighs about ${Math.round(L.tankLen * P.tankD * P.tankH / 231 * 8.34 + L.hotGal * 8.34)} lb (${Math.round(L.tankLen * P.tankD * P.tankH / 231 * 8.34 + L.hotGal * 8.34 + P.hotEmptyLb)} lb with the ${fmt(P.hotEmptyLb)} lb heater), plus the fresh tank itself.`);
    if (hotTop > P.counterH - 2) push('bad', `The hot water tank top (${fmt(hotTop)} in) is up against the counter (${fmt(P.counterH)} in).`);
    else if (P.hotShelf < 7.5 && gapL < -.01) push('bad', `The hot water tank starts at ${fmt(L.hotX[0])} in, over the wheel well (7 1/2 in tall, to 76 in at the wall); raise it onto a shelf or move it toward the sink.`);
    else if (P.hotShelf <= 10 && gapR < -.01) push('bad', `The hot water tank (${fmt(L.hotX[0])} to ${fmt(L.hotX[1])} in) runs into the fresh water tank (from ${fmt(L.tankX[0])} in).`);
    else if (room < -.0625) push('bad', `The hot water tank (${fmt(P.hotD)} deep, with ${fmt(P.hotBack)} in behind it for the fittings and the relief valve, which are at its back, so its front is ${fmt(P.hotBack + P.hotD)} in from the wall) sticks out past where the cabinet door goes by ${fmt(-room)} in at its sink end (the angled front makes the cabinet shallower there, ${fmt(room + P.hotBack + P.hotD)} in clear inside the door). To fit: slide the tank back toward the drawers, use less space behind it, notch the door at that corner, or make the angled front start later.`);
    else if (P.hotShelf > 10) {
      const onT = L.hotX[0] >= L.tankX[0] - .01 && L.hotX[1] <= L.tankX[1] + .01, dr = L.hotX[0] < L.angS - .75 && L.hotX[1] > L.cabS + 1.25, sinkHit = L.hotX[1] > L.sinkS + .01;
      push(onT && !dr && !sinkHit && P.counterH - 1.5 - hotTop >= 3 ? 'ok' : 'warn', `Hot water tank: ${fmt(P.hotW)} x ${fmt(P.hotD)} x ${fmt(P.hotH)} tall on a 3/4 in shelf on top of the fresh water tank (the shelf at ${fmt(P.hotShelf - .75)} to ${fmt(P.hotShelf)} in, carried by the cabinet sides, not by the tank), ${fmt(L.hotX[0])} to ${fmt(L.hotX[1])} in from the back, top at ${fmt(hotTop)} in, ${fmt(P.counterH - 1.5 - hotTop)} in under the counter for its fittings and relief valve; it holds ${L.hotGal.toFixed(1)} gal (${Math.round(L.hotGal * 8.34)} lb of water; the heater itself weighs ${fmt(P.hotEmptyLb)} lb, so ${Math.round(L.hotGal * 8.34 + P.hotEmptyLb)} lb full). ${room < .0625 ? 'no spare cabinet depth is left' : fmt(room) + ' in of cabinet depth is left'} in front of it at its tightest end (the front is angled from ${fmt(L.angS)} in); the hot and cold fittings and the relief valve are at its back, in the ${fmt(P.hotBack)} in between the tank and the wall (about ${fmt(P.hotBack + P.hotD)} in from the wall to its front). ${onT ? '' : 'It is not all over the fresh tank. '}${dr ? 'It is over the drawers. ' : ''}${sinkHit ? `It reaches ${fmt(L.hotX[1] - L.sinkS)} in into the sink cabinet, under the sink bowl (its bottom is at about 30 1/2 in); keep it to ${fmt(L.sinkS)} in. ` : ''}The paper towel recess (91 1/2 to 102 1/2 in, 29 3/4 to 35 1/4 in up) is just above it: they touch.`);
    }
    else push(gapL < P.hotGap - .01 || gapR < P.hotGap - .01 ? 'warn' : 'ok', `Hot water tank: ${fmt(P.hotW)} x ${fmt(P.hotD)} x ${fmt(P.hotH)} tall ${P.hotShelf > .5 ? `on a shelf at ${fmt(P.hotShelf)} in` : 'on the floor'} ${P.hotShelf > .5 ? 'over the wheel well' : 'next to the wheel well'} (${fmt(L.hotX[0])} to ${fmt(L.hotX[1])} in from the back), top at ${fmt(hotTop)} in, ${fmt(P.counterH - hotTop)} in under the counter, holds ${L.hotGal.toFixed(1)} gal (${Math.round(L.hotGal * 8.34)} lb of water; the ${fmt(P.hotW)} x ${fmt(P.hotD)} x ${fmt(P.hotH)} in is the outside of the heater, the heater itself weighs ${fmt(P.hotEmptyLb)} lb, so ${Math.round(L.hotGal * 8.34 + P.hotEmptyLb)} lb full), ${fmt(gapL)} in from the ${P.hotShelf > .5 ? 'fridge platform end (58 in)' : 'wheel well end'} and ${fmt(gapR)} in from the fresh tank${gapL < P.hotGap - .01 || gapR < P.hotGap - .01 ? ` (you wanted ${fmt(P.hotGap)} in each side; the ${fmt(L.tankX[0] - wellEnd)} in between the well and the fresh tank holds the tank plus ${fmt(L.tankX[0] - wellEnd - P.hotW)} in of space)` : ''}; ${fmt(room)} in of cabinet depth is left in front of it at its tightest end.`);
    {
      const shelfZ = L.cabShelf, tot = P.counterH - 6.75 - .25 - (shelfZ + 1), tlz = P.counterH - 7, bbz = L.backShelf + 1, manyB = tlz - 6 - bbz >= 14.5;
      const fitL = L.angS - .75 - L.cabS, fitD = P.cabD - .75;
      if (fitL < 29.2 || fitD < 19.95) push('bad', `The drawers under the counter need a flat part 29 1/4 in long between end panels (58 to 87 1/4 in) and a cabinet 20 3/4 in deep (20 in boxes plus a 3/4 in front); here the flat part is ${fmt(fitL)} in and the cabinet is ${fmt(P.cabD)} in deep.`);
      else if (tot < 3) push('bad', `The lower drawers under the top pair do not fit: only ${fmt(Math.max(0, tot))} in is left between the shelf over the hot water tank (${fmt(shelfZ)} in up) and the top drawers.`);
      else push(tot < 10 ? 'warn' : 'ok', `Lower drawers: ${tot >= 10 ? `two 13 x 20 x 5 in drawers one above the other on the cab side (shelf at ${fmt(shelfZ)} in up, 1/2 in over what is under it) and, toward the back, ${manyB ? `a 13 x 20 x 5 in drawer over two 13 x 20 x ${fmt((tlz - 6 - bbz - 1) / 2)} in ones` : `one 13 x 20 x ${fmt(tlz - bbz)} in drawer`} on a shelf at ${fmt(L.backShelf)} in up (1/2 in over ${L.backShelf > 8 ? 'the hot water tank' : 'the wheel well'}), all under the top pair` : `one row of two, 13 x 20 x ${fmt(tot)} in`}. All are 20 deep so they reach the wall. Nothing may come out of the top of the hot water tank (fittings, relief valve).`);
    }
    const ac = P.heaterW / 120, dc = P.heaterW / (12 * .9), kwhGal = 8.34 * 80 / 3412, ahGal = kwhGal / .9 * 1000 / 12;
    {
      const eco = P.acEcoA, turbo = P.acTurboA, ahDay = eco * P.acEcoH, hrsEco = P.battAh / eco, hrsTurbo = P.battAh / turbo, heaterA = P.heaterW / (12 * .9), fanA = P.fanHighW / 12;
      push(ahDay > P.battAh * .6 ? 'warn' : 'ok', `Air conditioner power (12 V DC, 10,000 BTU, cooling only; from the listing and reviews, confirm with the manual): about ${fmt(eco)} A in eco and up to ${fmt(turbo)} A in turbo (about ${Math.round(turbo * 12)} W). ${fmt(P.acEcoH)} hours a day in eco is ${Math.round(ahDay)} Ah, ${(ahDay / P.battAh * 100).toFixed(0)} percent of the ${fmt(P.battAh)} Ah battery; on its own the battery runs it about ${hrsEco.toFixed(0)} hours in eco or ${hrsTurbo.toFixed(1)} hours in turbo (nothing else running, a full battery, no reserve). Wire and fuse the feed for ${fmt(turbo)} A with margin (the cable size depends on the run length). With the water heater on too (about ${Math.round(heaterA)} A through the inverter) and the fan on high the worst case is about ${Math.round(turbo + heaterA + fanA)} A, which the battery's BMS has to allow (its limit is not known yet).`);
    }
    {
      const aLo = P.fanLowW / 12, aHi = P.fanHighW / 12, ah = aLo * (24 - P.fanHighH) + aHi * P.fanHighH, pct = ah / P.battAh * 100;
      push('ok', `Shower fan power (12 V DC, no inverter): ${fmt(P.fanLowW)} W on low is ${aLo.toFixed(2)} A and ${fmt(P.fanHighW)} W on high is ${aHi.toFixed(1)} A. Run ${fmt(P.fanHighH)} hour${P.fanHighH === 1 ? '' : 's'} on high and the rest of the day on low it uses about ${ah.toFixed(1)} Ah a day, ${pct.toFixed(1)} percent of the ${fmt(P.battAh)} Ah battery. Small next to the water heater; wire and fuse it for ${aHi.toFixed(1)} A.`);
    }
    push('ok', `Hot water power: ${fmt(P.heaterW)} W at 120 V is ${ac.toFixed(0)} A AC, about ${Math.round(dc)} A from a 12 V battery through an inverter. The ${fmt(P.battAh)} Ah battery is said to handle it; what is left to size for about ${Math.round(dc)} A is an inverter of ${Math.ceil(P.heaterW * 1.25 / 500) * 500} W or more, the battery cable and its fuse. Heating a gallon by 80 F takes about ${kwhGal.toFixed(2)} kWh, ${Math.round(ahGal)} Ah of the ${fmt(P.battAh)} Ah battery, so a full battery is about ${Math.round(P.battAh / ahGal)} gal of hot water from cold if nothing else runs; each gallon takes about ${Math.round(kwhGal / (P.heaterW / 1000) * 60)} min to heat. The ${L.hotGal.toFixed(1)} gal tank heated from cold by 80 F takes about ${(kwhGal * L.hotGal).toFixed(2)} kWh, ${Math.round(ahGal * L.hotGal)} Ah (${Math.round(ahGal * L.hotGal / P.battAh * 100)} percent of the battery) and about ${Math.round(kwhGal * L.hotGal / (P.heaterW / 1000) * 60)} minutes at ${fmt(P.heaterW)} W, so a full tank is about one short shower of hot water (mixed with cold it goes further), not a day's; the ${L.hotGal.toFixed(1)} gal is refilled from the fresh tank as you use it.`);
  }
  const ov = Math.min(L.sinkE, P.doorX + P.slideW) - Math.max(L.sinkS, P.doorX);
  if (ov > .5) push('warn', `The sink cabinet (${fmt(L.sinkS)} to ${fmt(L.sinkE)}) sits ${fmt(ov)} in inside the sliding door opening (${fmt(P.doorX)} to ${fmt(P.doorX + P.slideW)} in, ${fmt(P.slideH)} tall); you said that overlap is intended.`);
  // headroom, battery, doors
  const head = Math.max(P.platform + P.mattress, P.seatH) + 37, hg = P.cabBot - head;
  push(hg < 1 ? 'bad' : hg < 3 ? 'warn' : 'ok', `Seated headroom under the wall cabinets: ${fmt(hg)} in for a 6 ft person (head at ${fmt(head)} up).`);
  const bc = P.platform - 1.5 - 9.5;
  push(bc < 0 ? 'bad' : 'ok', bc < 0 ? `The battery (9 1/2 in) is taller than the space under the deck (${fmt(P.platform - 1.5)} in).` : `The battery clears the underside of the deck (${fmt(P.platform - 1.5)} in up) by ${fmt(bc)} in.`);
  if (P.doorH > L.ceilF - P.cabBot - .5) push('bad', 'The wall cabinet doors are taller than the cabinet.');
  else push('ok', `Wall cabinet doors: ${fmt(L.doors[0].w)} x ${fmt(P.doorH)} on the bed side and ${fmt(L.doors[3].w)} x ${fmt(P.doorH)} on the dinette side (3 each, widths follow the cabinet).`);
  if (P.fridgeD > P.cabD + .01) push('warn', `The fridge (${fmt(P.fridgeD)} deep) sticks out ${fmt(P.fridgeD - P.cabD)} in past the cabinet front (${fmt(P.cabD)}).`);
  const rank = { bad: 0, warn: 1, ok: 2 };
  return out.map((c, i) => [c, i]).sort((a, b) => rank[a[0].lv] - rank[b[0].lv] || a[1] - b[1]).map(x => x[0]);
}
const cap = s => s.charAt(0).toUpperCase() + s.slice(1);

/* ================= views, movers, drawing loop ================= */
const ALLDC = ['dc0', 'dc1', 'dc2', 'dc3', 'dc4', 'dc5'];
const VIEWS = [
  { id: 'driver', label: 'Driver side', draw: drawDriver, movers: [['Couch to bed', ['bed']], ['Dinette to bed', ['dinette']], ['Wall cabinet doors, bed side', ['dc0', 'dc1', 'dc2']], ['Wall cabinet doors, dinette side', ['dc3', 'dc4', 'dc5']], ['Closet doors', ['clo_hi', 'clo_lo']]] },
  { id: 'pass', label: 'Passenger side', draw: drawPass, movers: [['Shower pan', ['pan']], ['Fridge door', ['fridge']], ['Fold-out table with the foot ledge', ['flap', 'ledge']], ['Foot ledge only', ['ledge']]] },
  { id: 'end', label: 'Bed, from the end', draw: drawBedEnd, movers: [['Couch to bed', ['bed']]] },
  { id: 'cross', label: 'Cross-section', draw: drawCross, movers: [] },
  { id: 'bare', label: 'Bare roof (mark the ribs)', draw: drawBare, movers: [] },
  { id: 'ceil', label: 'Ceiling', draw: drawCeiling, movers: [] },
  { id: 'plan', label: 'From above', draw: drawPlan, movers: [['Couch to bed', ['bed']], ['Dinette to bed', ['dinette']], ['Shower pan', ['pan']], ['Closet doors', ['clo_hi', 'clo_lo']], ['Fridge door', ['fridge']], ['Fold-out table with the foot ledge', ['flap', 'ledge']], ['Foot ledge only', ['ledge']], ['Wall cabinet doors', ALLDC]] }
];
let view = 'driver', L = layout(P), lastSig = '';
const DEFS = '<defs><marker id="arq" viewBox="0 0 10 10" refX="8" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse"><path d="M2 1L8 5L2 9" fill="none" stroke="context-stroke" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"/></marker><pattern id="hatch" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#888780" stroke-width="1"/></pattern><pattern id="hq" width="6" height="6" patternUnits="userSpaceOnUse" patternTransform="rotate(45)"><line x1="0" y1="0" x2="0" y2="6" stroke="#888780" stroke-width="1"/></pattern></defs>';
let raf = 0;
function kick() { if (!raf) raf = requestAnimationFrame(frame); }
function frame() { raf = 0; render(); if (animating(performance.now())) kick(); }
// the build order: what to do first, with the numbers from the current sizes; ticks are kept in this browser
let buildSig = '', buildDone = {};
try { buildDone = JSON.parse(localStorage.getItem('van-build-done') || '{}') || {}; } catch (e) { buildDone = {}; }
function buildSteps(L) {
  const P = L.P, rib = L.ribs.map(fmt).join(', '), strips = FURR.map(fmt).join(', ');
  return [
    ['manuals', 'Get the two manuals before you cut anything', `The fan (2012 F36AR, 356 mm opening) and the OutEquip air conditioner: the exact roof opening and how thick a roof each kit clamps across. Your stack from the outside of the steel to the finished ceiling is ${fmt(P.ribDepth + L.lining)} in (${fmt(P.ribDepth)} in of rib plus ${fmt(L.lining)} in of covering) plus the steel skin.`],
    ['roof', 'Cut and frame the roof openings', `Air conditioner ${fmt(L.ac.w)} in square at ${fmt(L.ac.x)} in from the rear doors and ${fmt(L.ac.y)} across; fan ${fmt(L.fan.w)} in square at ${fmt(L.fan.x)} and ${fmt(L.fan.y)} across. Ribs start at ${rib} in (${fmt(P.ribW)} wide), so the openings sit between them: frame each opening, then seal, rust-proof the cut edges and fit the units.`],
    ['wiring', 'Rough in the wiring before anything is covered', `12 V DC runs for the fan (up to ${(P.fanHighW / 12).toFixed(1)} A), the air conditioner (up to ${fmt(P.acTurboA)} A), the ${L.lights.length} ceiling lights and the battery cable; the hot water heater needs about ${Math.round(P.heaterW / (12 * .9))} A through the inverter. Decide the battery (${fmt(P.battAh)} Ah), inverter and fuses first, since the electrics are still undecided.`],
    ['insulate', 'Insulate between the ribs and in the walls', `The ribs hang ${fmt(P.ribDepth)} in, so the insulation fits between them without going past the ceiling plane. Keep it clear of the openings' frames and the wiring.`],
    ['floor', 'Lay the subfloor', 'Everything else stands on it: the bed and couch base, the counter, the tanks and the battery.'],
    ['furring', 'Fit the furring strips and the blocking', `The eight horizontal strips on each wall (at ${strips} in up, at most 13 3/4 in apart; S7 stops at the sliding door opening and only S8 carries over it), then the blocking for the ceiling slats. Do the ceiling blocking before the walls.`],
    ['cover', 'Cover the ceiling, then the walls', `Ceiling: ${P.ceilLen > 0 ? Math.ceil(P.ceilLen * P.ceilW / 4608) : 0} sheets of ${fmt(P.plyT)} in plywood and ${L.nSlats - L.slatOut.size} slats ${fmt(P.slatW)} x ${fmt(P.slatT)} in, the lights on the slats. Walls: ${fmt(P.wallT)} in birch plywood standing floor to ceiling, joints at 42, 90 and 138 in. Seal both faces and finish before hanging (clear water-based finish or hardwax oil), glue to every strip, a screw with a finish washer about every 8 in, 1/16 in between sheets.`],
    ['heavy', 'Build the heavy low things first', `The battery (${fmt(P.battW || 21)} x ${fmt(P.battD || 10)} in, 52 to 73 in from the back), the hot water tank (${fmt(L.hotX[0])} to ${fmt(L.hotX[1])} in) and the fresh water tank (${fmt(L.tankX[0])} to ${fmt(L.tankX[1])} in), then the couch base, the counter and the drawers under it.`],
    ['cabinets', 'Last: wall cabinets, closet and the fold-out table', `The walls lean in about ${(Math.atan(L.leanK) * 180 / Math.PI).toFixed(0)} degrees above ${fmt(L.leanStart)} in, so the wall cabinets (${fmt(P.cabBot)} to ${fmt(L.ceilF)} in up) stand ${fmt(L.leanAt(P.cabBot))} in off the wall at the bottom and ${fmt(L.leanAt(L.ceilF))} in at the top: scribe the backs or fill the wedge, and cut their tops to the finished ceiling at the wall (${fmt(P.roofWallH - L.lining)} in, because the roof arcs up toward the middle). These are the pieces most likely to need small adjustments, so fit them last.`]
  ];
}
function renderBuild(L) {
  const steps = buildSteps(L), sig = JSON.stringify(steps) + JSON.stringify(buildDone);
  if (sig === buildSig) return; buildSig = sig;
  $('#build').innerHTML = steps.map(s => `<li class="${buildDone[s[0]] ? 'done' : ''}"><label><input type="checkbox" data-s="${s[0]}"${buildDone[s[0]] ? ' checked' : ''}><span><span class="bt">${s[1]}</span><span class="bb">${s[2]}</span></span></label></li>`).join('');
}
document.addEventListener('change', e => {
  const t = e.target; if (!t || !t.dataset || !t.dataset.s || t.type !== 'checkbox') return;
  buildDone[t.dataset.s] = t.checked; if (!t.checked) delete buildDone[t.dataset.s];
  try { localStorage.setItem('van-build-done', JSON.stringify(buildDone)); } catch (err) { }
  renderBuild(L);
});
function render() {
  const now = performance.now(), V = curVals(now), vw = VIEWS.find(v => v.id === view);
  L = layout(P);
  const r = vw.draw(L, V), svg = $('#svg');
  svg.setAttribute('viewBox', `0 0 ${Math.round(r.w)} ${Math.round(r.h)}`);
  svg.innerHTML = DEFS + r.body;
  // checks (only touch the page when the text changed)
  const ch = computeChecks(L, V), sig = JSON.stringify(ch);
  if (sig !== lastSig) { lastSig = sig; $('#checks').innerHTML = ch.map(c => `<li class="${c.lv}">${c.t}</li>`).join(''); }
  renderBuild(L);
  // movers: pressed state
  document.querySelectorAll('#movers .chip[data-ids]').forEach(b => b.setAttribute('aria-pressed', isOpenIds(b.dataset.ids.split(',')) ? 'true' : 'false'));
  // auto-sized fields show the value they work out
  PD.filter(p => p.t === 'c' && P[p.k]).forEach(p => { const el = $('#in_' + p.f); if (el && document.activeElement !== el) el.value = Math.round(L[p.f] * 100) / 100; });
}
function buildTabs() {
  const t = $('#tabs');
  t.innerHTML = VIEWS.map(v => `<button class="tab" role="tab" data-v="${v.id}" aria-selected="${v.id === view}">${v.label}</button>`).join('');
  t.querySelectorAll('.tab').forEach(b => b.onclick = () => { view = b.dataset.v; $('#svg').__zoomReset && $('#svg').__zoomReset(); buildTabs(); buildMovers(); saveHash(); render(); });
}
function buildMovers() {
  const vw = VIEWS.find(v => v.id === view), m = $('#movers');
  m.innerHTML = '<span class="lab">Open or close:</span>' + vw.movers.map(x => `<button type="button" class="chip" data-ids="${x[1].join(',')}" aria-pressed="false">${x[0]}</button>`).join('') + '<button type="button" class="chip all" id="openall">Open everything</button><button type="button" class="chip all" id="closeall">Close everything</button>';
  m.querySelectorAll('.chip[data-ids]').forEach(b => b.onclick = () => toggleIds(b.dataset.ids.split(',')));
  const all = [].concat(...vw.movers.map(x => x[1]));
  $('#openall').onclick = () => { all.forEach((id, i) => setTarget(id, 1, i * 240)); kick(); };
  $('#closeall').onclick = () => { all.forEach((id, i) => setTarget(id, 0, i * 160)); kick(); };
  render();
}
// click anything marked data-act in the drawing (looked up by position, so it still works while the drawing is redrawing)
$('#svg').addEventListener('click', e => {
  for (const el of document.elementsFromPoint(e.clientX, e.clientY)) {
    const g = el.closest && el.closest('[data-act]');
    if (g) { toggleIds(g.dataset.act.split(',')); return; }
  }
});

/* ================= sizes panel ================= */
function buildSizes() {
  const groups = []; PD.forEach(p => { if (!groups.includes(p.g)) groups.push(p.g); });
  $('#sizes').innerHTML = groups.map((g, gi) => `<details${gi < 2 ? ' open' : ''}><summary>${g}</summary>${PD.filter(p => p.g === g).map(p => {
    if (p.t === 'c') return `<label class="fld chk"><input type="checkbox" id="in_${p.k}"${P[p.k] ? ' checked' : ''}><span>${p.l}</span></label>`;
    if (p.t === 'x') return `<label class="fld" style="grid-template-columns:1fr"><span>${p.l}</span><input type="text" id="in_${p.k}" value="${P[p.k]}" placeholder="for example 12, 26.5, 41" style="width:100%;padding:4px 6px;border:1px solid #B4B2A9;border-radius:6px;font:inherit"></label>`;
    if (p.t === 's') return `<label class="fld"><span>${p.l}</span><select id="in_${p.k}">${p.o.map(o => `<option value="${o[0]}"${P[p.k] === o[0] ? ' selected' : ''}>${o[1]}</option>`).join('')}</select></label>`;
    return `<label class="fld"><span>${p.l}</span><input type="number" id="in_${p.k}" value="${P[p.k]}" step="${p.s}" min="${p.a}" max="${p.b}" inputmode="decimal"></label>`;
  }).join('')}</details>`).join('');
  PD.forEach(p => {
    const el = $('#in_' + p.k);
    if (p.t === 'c') el.onchange = () => { P[p.k] = el.checked; syncAuto(); saveHash(); render(); };
    else if (p.t === 'x') el.oninput = () => { P[p.k] = el.value; saveHash(); render(); };
    else if (p.t === 's') el.onchange = () => { P[p.k] = el.value; saveHash(); render(); };
    else {
      el.oninput = () => { const v = parseFloat(el.value); if (!isNaN(v)) { P[p.k] = clamp(v, p.a, p.b); saveHash(); render(); } };
      el.onchange = () => { const v = parseFloat(el.value); P[p.k] = isNaN(v) ? p.d : clamp(v, p.a, p.b); el.value = P[p.k]; syncAuto(); saveHash(); render(); };
    }
  });
  syncAuto();
}
function syncAuto() {
  PD.filter(p => p.t === 'c').forEach(p => { const el = $('#in_' + p.f); if (el) { el.disabled = !!P[p.k]; if (!P[p.k]) el.value = P[p.f]; } });
}
function setAll(vals) {
  P = Object.assign({}, DEF, vals);
  PD.forEach(p => { const el = $('#in_' + p.k); if (!el) return; if (p.t === 'c') el.checked = !!P[p.k]; else el.value = P[p.k]; });
  syncAuto(); saveHash(); render();
}
$('#reset').onclick = () => setAll({});

/* ================= link with the sizes in it ================= */
function saveHash() {
  const q = new URLSearchParams(); q.set('view', view);
  PD.forEach(p => { if (P[p.k] !== p.d) q.set(p.k, p.t === 'c' ? (P[p.k] ? '1' : '0') : P[p.k]); });
  try { history.replaceState(null, '', '#' + q.toString()); } catch (e) { }
}
function loadHash() {
  const q = new URLSearchParams(location.hash.replace(/^#/, '')), vals = {};
  if (VIEWS.some(v => v.id === q.get('view'))) view = q.get('view');
  PD.forEach(p => {
    if (!q.has(p.k)) return;
    const raw = q.get(p.k);
    if (p.t === 'c') vals[p.k] = raw === '1';
    else if (p.t === 'x') vals[p.k] = raw.slice(0, 400);
    else if (p.t === 's') { if (p.o.some(o => o[0] === raw)) vals[p.k] = raw; }
    else { const v = parseFloat(raw); if (!isNaN(v)) vals[p.k] = clamp(v, p.a, p.b); }
  });
  P = Object.assign({}, DEF, vals);
}
$('#share').onclick = () => {
  saveHash();
  const url = location.href, msg = $('#sharemsg');
  const done = ok => { msg.textContent = ok ? 'Link copied. It opens this view with these sizes.' : 'Copy this link: ' + url; };
  try { navigator.clipboard.writeText(url).then(() => done(true), () => done(false)); } catch (e) { done(false); }
};

loadHash();
buildTabs(); buildSizes(); buildMovers();
makeZoomable($('#svg'));
</script>
</body>
</html>
