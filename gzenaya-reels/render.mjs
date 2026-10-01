// Render client.html / interne.html to A4 PDFs with headless Chromium.
import { createRequire } from 'node:module';
import { execSync } from 'node:child_process';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const here = path.dirname(fileURLToPath(import.meta.url));
// Use a local playwright if present, else the global install.
const req = createRequire(import.meta.url);
let pw;
try { pw = req('playwright'); } catch { pw = req(path.join(execSync('npm root -g').toString().trim(), 'playwright')); }
const { chromium } = pw;
const jobs = [
  ['client.html', 'Gzenaya-Guide-Reels-CLIENT.pdf'],
  ['interne.html', 'Gzenaya-Reel-Playbook-INTERNE-Saad.pdf'],
];

const browser = await chromium.launch();
const page = await browser.newPage();
for (const [src, out] of jobs) {
  await page.goto('file://' + path.join(here, src), { waitUntil: 'networkidle' });
  await page.evaluate(() => document.fonts.ready);
  await page.pdf({ path: path.join(here, out), format: 'A4', printBackground: true, preferCSSPageSize: true, scale: 0.95 });
  console.log('wrote', out);
}
await browser.close();
