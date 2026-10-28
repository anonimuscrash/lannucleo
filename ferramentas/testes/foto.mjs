import { createRequire } from 'node:module';
const { chromium } = createRequire(import.meta.url)('playwright');
const [url, prefixo, larguras = '1440,390', tema = ''] = process.argv.slice(2);
const claro = tema === 'claro';
const b = await chromium.launch();
const out = [];
for (const w of larguras.split(',').map(Number)) {
  const ctx = await b.newContext({ viewport: { width: w, height: w < 800 ? 844 : 900 }, isMobile: w < 800, hasTouch: w < 800, reducedMotion: 'reduce', colorScheme: 'dark' });
  if (claro) await ctx.addInitScript(() => { try { localStorage.setItem('nucleo-land-tema', 'claro'); } catch {} });
  const p = await ctx.newPage();
  const erros = [];
  p.on('pageerror', (e) => erros.push(e.message));
  p.on('console', (m) => m.type() === 'error' && erros.push(m.text()));
  p.on('requestfailed', (r) => erros.push('falhou: ' + r.url()));
  await p.goto(url, { waitUntil: 'networkidle' });
  await p.evaluate(async () => { for (let y = 0; y < document.documentElement.scrollHeight; y += 600) { window.scrollTo(0, y); await new Promise((r) => setTimeout(r, 40)); } window.scrollTo(0, 0); });
  await p.waitForLoadState('networkidle');
  await p.waitForTimeout(500);
  const m = await p.evaluate(() => ({ sw: document.documentElement.scrollWidth, cw: document.documentElement.clientWidth, h: document.documentElement.scrollHeight }));
  await p.screenshot({ path: `${prefixo}-${w}.png`, fullPage: true });
  out.push({ w, ...m, erros });
  await ctx.close();
}
await b.close();
console.log(JSON.stringify(out));
