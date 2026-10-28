import { createRequire } from 'node:module'; const { chromium } = createRequire(import.meta.url)('playwright');
const [url, sel, saida, larguras='1440', tema=''] = process.argv.slice(2);
const b=await chromium.launch(); const out=[];
for (const w of larguras.split(',').map(Number)){
  const ctx=await b.newContext({viewport:{width:w,height:w<700?844:900}});
  if(tema) await ctx.addInitScript(()=>localStorage.setItem('nucleo-land-tema','claro'));
  const p=await ctx.newPage(); const erros=[]; p.on('pageerror',e=>erros.push(e.message)); p.on('console',m=>{if(m.type()==='error')erros.push(m.text())});
  await p.goto(url); await p.evaluate(async()=>{for(let y=0;y<document.body.scrollHeight;y+=500){scrollTo(0,y);await new Promise(r=>setTimeout(r,40))}});
  const el=p.locator(sel); await el.scrollIntoViewIfNeeded(); await p.waitForTimeout(900); await p.evaluate(()=>document.querySelector('.site-header').style.visibility='hidden');
  await el.screenshot({path:`${saida}-${w}.png`});
  out.push({w,sw:await p.evaluate(()=>document.documentElement.scrollWidth),erros}); await ctx.close();
}
console.log(JSON.stringify(out)); await b.close();
