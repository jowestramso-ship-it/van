/* Writes tools/build_steps.json: the nine steps of the Build order card of interactive.html (with the plan's own numbers), for the build guide pages.
   Run:  node tools/buildsteps.js   (needs playwright + the bundled Chromium; build.sh runs it and skips it if they are missing) */
const {chromium} = require(process.env.NODE_PATH + '/playwright');
const fs = require('fs');
(async () => {
  const b = await chromium.launch({executablePath: '/opt/pw-browsers/chromium'});
  const page = await b.newPage({viewport: {width: 1400, height: 1000}});
  await page.goto('file://' + __dirname + '/../interactive.html'); await page.waitForTimeout(700);
  const steps = await page.evaluate(() => buildSteps(L).map(s => ({id: s[0], title: s[1], body: s[2].replace(/<[^>]+>/g, '')})));
  await b.close();
  fs.writeFileSync(__dirname + '/build_steps.json', JSON.stringify(steps, null, 1));
  console.log('build_steps.json written,', steps.length, 'steps');
})();
