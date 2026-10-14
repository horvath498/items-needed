// Render calendar PNGs and the playbook PDF with Playwright's Chromium.
// Usage (from launch-playbook-2026-10/): node build/render.js calendar|pdf
const path = require('path');
const { pathToFileURL } = require('url');

function loadPlaywright() {
  try { return require('playwright'); } catch (_) {}
  return require('/opt/node22/lib/node_modules/playwright');
}
const { chromium } = loadPlaywright();

const ROOT = path.resolve(__dirname, '..');

async function launch() {
  const opts = process.env.CHROMIUM_PATH ? { executablePath: process.env.CHROMIUM_PATH } : {};
  return chromium.launch(opts);
}

async function renderCalendar() {
  const browser = await launch();
  const page = await browser.newPage({ viewport: { width: 1700, height: 1000 }, deviceScaleFactor: 1.5 });
  await page.goto(pathToFileURL(path.join(ROOT, 'calendar', 'launch-calendar.html')).href);
  await page.evaluate(() => document.fonts.ready);
  for (const [id, file] of [['#sprint', 'sprint-calendar.png'], ['#quarter', 'q4-calendar.png']]) {
    await page.locator(id).screenshot({ path: path.join(ROOT, 'calendar', file) });
    console.log('wrote calendar/' + file);
  }
  await browser.close();
}

async function renderPdf() {
  const browser = await launch();
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.join(ROOT, '.playbook-print.html')).href, { waitUntil: 'load' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({
    path: path.join(ROOT, 'LAUNCH_PLAYBOOK.pdf'),
    format: 'Letter',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '0.6in', bottom: '0.7in', left: '0.6in', right: '0.6in' },
    displayHeaderFooter: true,
    headerTemplate: '<div></div>',
    footerTemplate:
      '<div style="font-family:Inter,sans-serif;font-size:8px;color:#64748b;width:100%;padding:0 0.6in;display:flex;justify-content:space-between">' +
      '<span>Launch &amp; Marketing Playbook · DBR · W2SA · Lucent Veritas · 2026-10-14</span>' +
      '<span><span class="pageNumber"></span> / <span class="totalPages"></span></span></div>',
  });
  console.log('wrote LAUNCH_PLAYBOOK.pdf');
  await browser.close();
}

const what = process.argv[2];
(what === 'calendar' ? renderCalendar() : what === 'pdf' ? renderPdf() : Promise.reject(new Error('usage: render.js calendar|pdf')))
  .catch((e) => { console.error(e); process.exit(1); });
