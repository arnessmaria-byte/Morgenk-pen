// Lager PDF-utgaven av spillbladet fra HTML-fila med Chromium (Playwright).
// Bruk: node lag-pdf.js ravnebladet.html ravnebladet.pdf
const { chromium } = require('playwright');
const path = require('path');

(async () => {
  const [, , inn, ut] = process.argv;
  if (!inn || !ut) { console.error('Bruk: node lag-pdf.js inn.html ut.pdf'); process.exit(1); }
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1100, height: 1400 } });
  await page.emulateMedia({ media: 'print', colorScheme: 'light' });
  await page.goto('file://' + path.resolve(inn), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.waitForTimeout(800);
  await page.pdf({
    path: ut,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '0', right: '0', bottom: '0', left: '0' },
  });
  await browser.close();
  console.log('Skrev ' + ut);
})();
