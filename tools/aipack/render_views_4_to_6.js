const { chromium } = require(process.env.NODE_PATH + '/playwright');
(async () => {
  const SC = process.env.SC;
  const b = await chromium.launch({ args: ['--use-gl=angle', '--use-angle=swiftshader', '--enable-webgl', '--ignore-gpu-blocklist', '--enable-unsafe-swiftshader'] });
  const p = await b.newPage({ viewport: { width: 1300, height: 800 }, deviceScaleFactor: 2 });
  const errs = []; p.on('pageerror', e => errs.push(String(e))); p.on('console', m => { if (m.type() === 'error') errs.push('c:' + m.text()); });
  await p.goto('file://' + SC + '/three3d/interior_pack.html'); await p.waitForTimeout(3000);
  const shots = [['4-couch-and-aisle', [12, 36, 39], [58, 30, 24], 70], ['5-dinette', [121, 47, 43], [121, 37, 0], 72], ['6-couch-from-the-rear', [-3, 52, 40], [50, 34, 8], 62]];
  for (const [n, pp, t, f] of shots) {
    await p.evaluate(([pp, t, f]) => { window.__look('natural'); window.__bed(0); window.__cam(pp, t, f); }, [pp, t, f]); await p.waitForTimeout(900);
    const c = await p.$('canvas'); await c.screenshot({ path: SC + '/lookpack/' + n + '.png' });
  }
  console.log('errors', JSON.stringify(errs)); await b.close();
})();
