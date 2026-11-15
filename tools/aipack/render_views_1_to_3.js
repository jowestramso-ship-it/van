const { chromium } = require(process.env.NODE_PATH + '/playwright');
(async () => {
  const SC = process.env.SC;
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 800 }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push('c:' + m.text()); });
  await p.goto('file://' + SC + '/three3d/interior_local.html'); await p.waitForTimeout(3000);
  const shots = [['1-from-the-rear-doors', 'rear'], ['2-from-the-cab-end', 'cab'], ['3-kitchen', 'kitchen'], ['4-couch', 'couch'], ['5-dinette', 'dinette']];
  for (const [n, v] of shots) {
    await p.evaluate(v => { window.__look('natural'); window.__setView(v); window.__bed(0); }, v); await p.waitForTimeout(900);
    const c = await p.$('canvas'); await c.screenshot({ path: SC + '/lookpack/' + n + '.png' });
  }
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
