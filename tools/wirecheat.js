/* The printable wire cheat sheet (cheatsheet.html): every wire number with its from and to in short words, one page.
   A new wire in elwires.js needs a line in SHORT, or the build stops: that keeps the sheet in step with the wire list. */
const SHORT = {
  WR1: ['Battery +', 'Class T, bus +'], WR2: ['Battery −', 'Shunt, bus −'], WR3: ['Bus bars', 'Inverter'], WR4: ['Starter battery', 'DC-DC charger'],
  WR5: ['DC-DC charger', 'Bus bars'], WR6: ['Shore charger', 'Bus bars'], WR7: ['Shore inlet (ED6)', 'TS-30'], WR8: ['Inverter', 'TS-30'],
  WR9: ['TS-30', 'AC panel'], WR10: ['AC panel', 'Shore charger'], WR11: ['Bus (100 A fuse)', 'A/C unit'], WR12: ['AC panel', 'Riser B (B/D and C)'],
  WR13: ['Bus bars', 'Fuse block'], WR14: ['Fuse block', 'JB2'], WR15: ['Fuse block', 'Roof fan'], WR16: ['Fuse block', 'JB'],
  WR18: ['AC panel', 'Couch outlet (ED10)'], WR19: ['Couch outlet', 'Dinette outlet (ED15)'], WR20: ['JB', 'Couch light, right (ED18)'], WR21: ['JB', 'Rear plate (ED11)'],
  WR22: ['Rear plate ED11', 'Rear couch light (ED7)'], WR23: ['Rear plate ED11', 'Shower light (EP1)'], WR24: ['JB', 'Dinette switch (ED12)'], WR25: ['Dinette switch ED12', 'Dinette lights (ED8, ED9)'],
  WR26: ['Riser B', 'Fridge outlet (EP3)'], WR27: ['Riser B', 'Selector (EP9)'], WR28: ['Selector', 'Microwave outlet (EP4)'], WR29: ['Selector', 'Heater outlet (EP7)'],
  WR30: ['Couch outlet', 'Counter outlet (EP15)'], WR31: ['Fuse block', 'Water pump (PL3)'], WR32: ['Fuse block', 'Control panel (EP5)'], WR33: ['Switch EP11', 'Counter light (EP2)'],
  WR34: ['Switch EP14', 'Ceiling lights (EP12, EP13)'], WR35: ['JB', 'Switches EP11, EP14'], WR37: ['Counter outlet', 'TV outlet (EP6)'],
  WR38: ['JB2', 'Slide dimmer (ED22)'], WR39: ['Slide dimmer ED22', 'JB2'], WR40: ['JB2', '3 strips (F1, F2, F3)'],
};
const esc = s => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
function cheatHTML(WRall) {
  const live = WRall.filter(w => !w.retired), gone = WRall.filter(w => w.retired);
  live.forEach(w => { if (!SHORT[w.id]) throw new Error('wire cheat sheet: no short words for ' + w.id + ' (add it to SHORT in tools/wirecheat.js)'); });
  const kind = w => w.t === 'ac' ? ['120 V', 'k-ac'] : ((['2/0', '2', '6'].includes(w.g) || w.id === 'WR13') ? ['Batt', 'k-bt'] : ['12 V', 'k-dc']);
  const rows = live.map(w => { const [k, c] = kind(w), [a, b] = SHORT[w.id];
    return `<tr><td class="n">${w.id}</td><td class="g">${w.g}</td><td class="${c}">${k}</td><td>${esc(a)}</td><td class="ar">→</td><td>${esc(b)}</td><td class="ck">☐</td></tr>`; }).join('');
  return `<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>Wire cheat sheet</title><style>
  @page { size: letter; margin: .4in; }
  body { font: 12px/1.25 -apple-system, "Segoe UI", system-ui, sans-serif; color: #1b1a17; background: #fff; margin: 0; padding: 14px max(16px, env(safe-area-inset-left, 0px)); color-scheme: light; }
  .sheet { max-width: 760px; margin: 0 auto; }
  h1 { font-size: 19px; margin: 0 0 2px; } .sub { font-size: 11.5px; color: #4a483f; margin: 0 0 8px; }
  table { border-collapse: collapse; width: 100%; } th { text-align: left; font-size: 10.5px; letter-spacing: .04em; text-transform: uppercase; color: #4a483f; border-bottom: 1.5px solid #1b1a17; padding: 2px 6px; }
  td { padding: 2.2px 6px; border-bottom: .5px solid #cfcbbd; } tr:nth-child(even) td { background: #f6f4ee; }
  td.n { font-weight: 700; white-space: nowrap; } td.g { white-space: nowrap; text-align: right; } td.ar { color: #8a867a; text-align: center; padding: 2.2px 0; } td.ck { font-size: 15px; text-align: center; padding: 0 8px; }
  .k-ac { color: #B3261E; font-weight: 600; white-space: nowrap; } .k-dc { color: #185FA5; font-weight: 600; white-space: nowrap; } .k-bt { color: #6A1B9A; font-weight: 600; white-space: nowrap; }
  .foot { font-size: 11px; color: #4a483f; margin-top: 8px; } .foot p { margin: 2px 0; }
  @media print { body { padding: 0; } .vannav { display: none !important; } tr { break-inside: avoid; } }
  </style></head><body><div class="sheet">
  <h1>Wire cheat sheet</h1>
  <p class="sub">Tag both ends of every wire with its number and + or −. AWG is the wire size. <b class="k-bt">Batt</b> = battery cables, <b class="k-dc">12 V</b> = lights, fan, pump, strip, <b class="k-ac">120 V</b> = household power. Tick the box when the wire is in.</p>
  <table><thead><tr><th>Wire</th><th style="text-align:right">AWG</th><th>Kind</th><th>From</th><th></th><th>To</th><th>Done</th></tr></thead><tbody>${rows}</tbody></table>
  <div class="foot"><p>Retired numbers (never reused): ${gone.map(w => w.id).join(', ')}. The old WR36 cable stays in place as the pull line.</p>
  <p>WR40 is three pairs: F1 driver strip, F2 passenger strip, F3 back strip, each tagged "WR40 F1 +" and "WR40 F1 −" and so on. JB = lights junction box, JB2 = strip junction box, both in the couch cabinet.</p></div>
  </div></body></html>`;
}
module.exports = { cheatHTML, SHORT };
