import { createRequire } from 'node:module'; const { chromium } = createRequire(import.meta.url)('playwright');
const BASE = (process.argv[2] || process.env.LAND_URL || 'http://localhost:8090/').replace(/\/?$/, '/');
const b = await chromium.launch();
const out = [];
for (const tema of ['escuro','claro']) for (const [w,h] of [[320,640],[360,740],[375,812],[390,844],[430,932],[768,1024],[870,900],[1024,768],[1151,800],[1440,900],[844,390],[932,430]]) {
  const ctx = await b.newContext({ viewport:{width:w,height:h} });
  if (tema==='claro') await ctx.addInitScript(()=>localStorage.setItem('nucleo-land-tema','claro'));
  const p = await ctx.newPage(); const erros=[];
  p.on('pageerror',e=>erros.push(e.message)); p.on('console',m=>{if(m.type()==='error')erros.push(m.text())});
  p.on('requestfailed',r=>erros.push('falhou '+r.url()));
  await p.goto(BASE,{waitUntil:'load'});
  await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=600){scrollTo(0,y);await new Promise(r=>setTimeout(r,30))}scrollTo(0,0)});
  const r = await p.evaluate(()=>{const de=document.documentElement;
    const largos=[...document.querySelectorAll('body *')].filter(el=>{const q=el.getBoundingClientRect();return q.width&&q.right>de.clientWidth+1&&getComputedStyle(el).position!=='fixed'&&!el.closest('.pr-galeria,.u-abas,.faq-abas,.showcase-tabs,.orbita-hero,.hero-visual,[aria-hidden="true"]')}).slice(0,3).map(el=>el.className||el.tagName);
    const imgs=[...document.images].filter(i=>i.complete&&i.naturalWidth===0).map(i=>i.src);
    return {sw:de.scrollWidth,cw:de.clientWidth,largos,imgs,tema:de.dataset.tema||'escuro'}});
  out.push({tema,w,h,...r,erros}); await ctx.close();
}
console.log(out.map(o=>`${o.tema} ${o.w}x${o.h} sw=${o.sw} cw=${o.cw} ${o.sw===o.cw?'OK':'ESTOURO'} largos=${JSON.stringify(o.largos)} imgsQuebradas=${o.imgs.length} erros=${o.erros.length} ${o.erros.join('|')} temaAplicado=${o.tema}`).join('\n'));
await b.close();
