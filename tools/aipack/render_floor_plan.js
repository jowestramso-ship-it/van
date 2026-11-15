const { chromium } = require(process.env.NODE_PATH + '/playwright');
(async () => {
  const b = await chromium.launch({ executablePath: '/opt/pw-browsers/chromium' });
  const p = await b.newPage({ viewport: { width: 1500, height: 1000 }, deviceScaleFactor: 2 });
  await p.goto('file:///home/user/van/interactive.html'); await p.waitForTimeout(800);
  await p.click('text=From above'); await p.waitForTimeout(800);
  const box = await p.evaluate(() => { let best = null, area = 0; document.querySelectorAll('svg').forEach(s => { const r = s.getBoundingClientRect(); if (r.width * r.height > area) { area = r.width * r.height; best = { x: r.x, y: r.y, w: r.width, h: r.height }; } }); return best; });
  console.log(JSON.stringify(box));
  await p.screenshot({ fullPage: true, path: process.env.SC + '/lookpack/0-floor-plan-from-above.png', clip: { x: box.x, y: box.y, width: box.w, height: box.h } });
  await b.close();
})();
