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

// One week per landscape page. The page shrinks its own type until each week
// fits (see FIT_JS in calendar.py); fail loudly if one still overflows.
async function renderPrint() {
  const browser = await launch();
  const page = await browser.newPage();
  await page.goto(pathToFileURL(path.join(ROOT, 'calendar', 'launch-calendar-print.html')).href, { waitUntil: 'load' });
  await page.waitForSelector('body[data-fit="done"]');
  const report = await page.$$eval('.page', (pages) => pages.map((p) => ({
    scale: p.style.getPropertyValue('--s') || '1',
    overflow: p.classList.contains('overflow'),
  })));
  report.forEach((r, i) => console.log(`page ${i + 1}: type scale ${r.scale}${r.overflow ? '  ** OVERFLOW **' : ''}`));
  if (report.some((r) => r.overflow)) throw new Error('a week does not fit on its page');
  // Below ~85% the smallest text drops under 6 pt, too small to read on paper.
  if (report.some((r) => parseFloat(r.scale) < 0.85)) throw new Error('a week only fits below 85% type size');
  await page.pdf({
    path: path.join(ROOT, 'calendar', 'launch-calendar-print.pdf'),
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: 0, bottom: 0, left: 0, right: 0 },
  });
  console.log('wrote calendar/launch-calendar-print.pdf');
  await browser.close();
}

const what = process.argv[2];
const jobs = { calendar: renderCalendar, pdf: renderPdf, print: renderPrint };
(jobs[what] ? jobs[what]() : Promise.reject(new Error('usage: render.js calendar|pdf|print')))
  .catch((e) => { console.error(e); process.exit(1); });
