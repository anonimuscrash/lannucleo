import { createRequire } from 'node:module'; const { chromium } = createRequire(import.meta.url)('playwright');
import { pathToFileURL } from 'node:url'; import path from 'node:path';
const [entrada, saida] = process.argv.slice(2);
const b = await chromium.launch(); const p = await b.newPage();
await p.goto(pathToFileURL(path.resolve(entrada)).href, { waitUntil: 'networkidle' });
await p.evaluate(() => document.fonts.ready);
await p.pdf({ path: saida, format: 'A4', printBackground: true, displayHeaderFooter: true,
  headerTemplate: '<span></span>',
  footerTemplate: '<div style="width:100%;font-size:7.5pt;color:#8a8199;padding:0 17mm;display:flex;justify-content:space-between;font-family:sans-serif"><span>Land da Núcleo · manual de continuidade · 28/10/2026</span><span class="pageNumber"></span></div>',
  margin: { top: '18mm', bottom: '20mm', left: '17mm', right: '17mm' } });
await b.close(); console.log('ok');
