import { createRequire } from 'node:module'; const { chromium } = createRequire(import.meta.url)('playwright');
const BASE = (process.argv[2] || process.env.LAND_URL || 'http://localhost:8090/').replace(/\/?$/, '/');
const b = await chromium.launch(); const res=[]; const ok=(n,c,x='')=>res.push(`${c?'PASSOU':'FALHOU'} ${n} ${x}`);
async function pagina(w,h,extra={}){const ctx=await b.newContext({viewport:{width:w,height:h},...extra});const p=await ctx.newPage();p.erros=[];p.on('pageerror',e=>p.erros.push(e.message));p.on('console',m=>{if(m.type()==='error')p.erros.push(m.text())});await p.goto(BASE);return p;}
// computador
let p=await pagina(1440,900);
const ids=await p.evaluate(()=>[...document.querySelectorAll('a[href^="#"]')].map(a=>a.getAttribute('href')).filter(h=>h.length>1&&!document.querySelector(h)));
ok('âncoras existem',ids.length===0,JSON.stringify(ids));
await p.click('#tema-botao'); ok('tema claro liga',await p.evaluate(()=>document.documentElement.dataset.tema==='claro'&&localStorage.getItem('nucleo-land-tema')==='claro'));
await p.reload(); ok('tema claro fica salvo após recarregar',await p.evaluate(()=>document.documentElement.dataset.tema==='claro'));
await p.click('#tema-botao'); ok('tema escuro volta',await p.evaluate(()=>!document.documentElement.dataset.tema));
await p.click('.u-no[data-u="paginas"]'); ok('Universo: clicar órbita Páginas',(await p.textContent('#u-titulo'))==='Páginas' && (await p.getAttribute('#u-link','href'))==='#paginas');
await p.click('.u-no[data-u="checkout"]'); ok('Universo: clicar órbita Checkout',(await p.textContent('#u-titulo'))==='Checkout PIX');
await p.locator('.showcase-tab').nth(3).click(); await p.waitForTimeout(400); ok('Vitrine: aba 04 Checkout',(await p.getAttribute('#showcase-image','src')).includes('checkout'));
// checkout demo
await p.click('.demo-produto >> nth=1'); await p.click('[data-acao="gerar"]'); ok('Demo PIX: etapa 2 visível',await p.isVisible('[data-etapa="2"]'));
ok('Demo PIX: aviso de demonstração na etapa 2',/demonstra/i.test(await p.textContent('[data-etapa="2"]')));
await p.click('[data-acao="pagar"]'); ok('Demo PIX: confirmação com produto escolhido',(await p.textContent('#demo-linha'))==='Pack de Presets' && (await p.textContent('#demo-valor')).includes('29,90'));
await p.waitForTimeout(450); ok('Checkout: cartão "Pagamento aprovado" aparece só depois da simulação, com o valor certo',await p.evaluate(()=>{const c=document.querySelector('.cp-flutua');return getComputedStyle(c).opacity!=='0'&&document.querySelector('#cp-flutua-valor').textContent.includes('29,90')&&/simula/i.test(c.textContent)}));
await p.click('[data-acao="recomecar"]'); await p.waitForTimeout(400);
ok('Checkout: cartão some ao recomeçar',await p.evaluate(()=>getComputedStyle(document.querySelector('.cp-flutua')).opacity==='0')); ok('Demo PIX: recomeçar',await p.isVisible('[data-etapa="1"]'));
// marca
await p.focus('#marca-range'); for(let i=0;i<5;i++) await p.keyboard.press('ArrowLeft');
ok('Antes/depois: teclado move o corte',(await p.evaluate(()=>document.querySelector('#marca-palco').style.getPropertyValue('--corte')))==='45%');
await p.click('[data-marca="texto"]'); await p.waitForTimeout(300); ok('Marca: troca para texto',(await p.getAttribute('#marca-depois','src')).includes('texto') && await p.evaluate(()=>{const i=document.querySelector('#marca-depois');return i.complete&&i.naturalWidth>0}));
// mídias
await p.click('#md-buscar'); await p.waitForFunction(()=>document.querySelector('#md-estado-2').textContent==='Pronto',null,{timeout:8000});
ok('Baixar mídias: chega em Pronto',(await p.textContent('#md-baixar')).includes('exemplo'));
// faq
await p.click('[data-faq="ferramentas"]:not(article)'); const vis=await p.evaluate(()=>[...document.querySelectorAll('article.faq-item')].filter(a=>!a.hidden).map(a=>a.dataset.faq));
ok('FAQ: filtro Ferramentas',vis.length>0&&vis.every(v=>v==='ferramentas'),JSON.stringify(vis));
await p.click('[data-faq="todas"]:not(article)');
const q=p.locator('article.faq-item:not([hidden]) .faq-question').nth(1); await q.click(); ok('FAQ: abrir pergunta',(await q.getAttribute('aria-expanded'))==='true');
// IA
const antes=await p.locator('#ia-mensagens .ia-msg').count(); await p.click('[data-ia="pessoa"]'); ok('IA: sugestão adiciona resposta',(await p.locator('#ia-mensagens .ia-msg').count())===antes+2);
ok('Sem erros no console (computador)',p.erros.length===0,p.erros.join('|'));
// links externos
const ext=await p.evaluate(()=>[...new Set([...document.querySelectorAll('a[href^="http"]')].map(a=>new URL(a.href).host))]); ok('Links externos só para app.nucleobot.com.br',ext.every(h=>h==='app.nucleobot.com.br'),JSON.stringify(ext));
// celular
p=await pagina(390,844,{isMobile:true,hasTouch:true});
await p.click('.menu-toggle'); ok('Menu celular abre',await p.isVisible('#mobile-menu a[href="#paginas"]'));
await p.click('#mobile-menu a[href="#paginas"]'); await p.waitForTimeout(3000); ok('Menu celular: link leva à seção e fecha',!(await p.evaluate(()=>document.body.classList.contains('menu-open')||document.documentElement.classList.contains('menu-open'))) && await p.evaluate(()=>Math.abs(document.querySelector('#paginas').getBoundingClientRect().top)<150));
const aba=p.locator('.u-abas [data-u="ferramentas"]'); ok('Universo: abas visíveis no celular',await aba.isVisible()); await aba.click(); ok('Universo: aba Ferramentas',(await p.textContent('#u-titulo'))==='Ferramentas');
ok('Universo: órbitas escondidas no celular',!(await p.isVisible('.u-no[data-u="bots"]')));
await p.locator('#pr-galeria').scrollIntoViewIfNeeded(); const x0=await p.evaluate(()=>document.querySelector('#pr-galeria').scrollLeft); await p.click('[data-pr="1"]'); await p.waitForTimeout(800);
ok('Premiação: seta avança',(await p.evaluate(()=>document.querySelector('#pr-galeria').scrollLeft))>x0);
ok('Sem erros no console (celular)',p.erros.length===0,p.erros.join('|'));
p=await pagina(390,844,{isMobile:true,hasTouch:true}); await p.tap('#tema-botao'); await p.tap('.menu-toggle'); await p.waitForTimeout(300);
ok('Celular: botão de tema visível e menu claro cobre a tela',await p.evaluate(()=>{const r=document.querySelector('#mobile-menu').getBoundingClientRect();return document.documentElement.dataset.tema==='claro'&&r.height>600&&getComputedStyle(document.querySelector('#mobile-menu')).backgroundColor!=='rgba(0, 0, 0, 0)'}));
p=await pagina(1440,900);
ok('Topo: 6 cartões de funções levam a seções que existem',await p.evaluate(()=>{const l=[...document.querySelectorAll('.cz-chips a')];return l.length===6&&l.every(a=>document.querySelector(a.getAttribute('href')))}));
ok('Topo: cartões visíveis no computador',await p.isVisible('.cz-chips .c1 a'));
ok('Soluções: 6 cartões com destino válido',await p.evaluate(()=>{const l=[...document.querySelectorAll('.solucoes a')];return l.length===6&&l.every(a=>document.querySelector(a.getAttribute('href')))}));
ok('Topo/prêmios/checkout continuam escuros no tema claro',await (async()=>{await p.click('#tema-botao');return p.evaluate(()=>['#inicio','#premiacao','#checkout-pix'].every(id=>{const c=getComputedStyle(document.querySelector(id)).backgroundColor.match(/\d+/g).map(Number);return c[0]+c[1]+c[2]<60}))})());
await p.click('#tema-botao');
// movimento reduzido
p=await pagina(1440,900,{reducedMotion:'reduce'});
ok('Movimento reduzido: planeta do topo parado',await p.evaluate(()=>{const e=document.querySelector('.cz-planeta');const a=getComputedStyle(e).animationName;const d=parseFloat(getComputedStyle(e).animationDuration);return !!e&&(a==='none'||d<=0.01)}));
await p.click('#md-buscar'); await p.waitForTimeout(200); ok('Movimento reduzido: demo de mídias sem espera',(await p.textContent('#md-estado-2'))==='Pronto');
// foco teclado
p=await pagina(1440,900); await p.keyboard.press('Tab'); const f=await p.evaluate(()=>{const e=document.activeElement;return e.tagName+' '+getComputedStyle(e).outlineStyle+' '+(e.textContent||'').trim().slice(0,20)}); ok('Teclado: primeiro Tab tem foco visível',!f.includes(' none '),f);
// ===== 28/10/2026 (v3): testes das 13 correções =====
// ok2: se a página não tiver a peça (versão antiga), o teste reprova em vez de parar tudo.
const ok2=async(n,f,x='')=>{try{ok(n,await f(),x)}catch(e){ok(n,false,'erro: '+String(e.message).split('\n')[0])}};
const clica=async(sel)=>{try{await p.click(sel,{timeout:3000})}catch(e){}};
p=await pagina(1440,900);
await ok2('v3 ordem: Premiação é a 3ª seção (depois do topo e do Universo)',async()=>await p.evaluate(()=>[...document.querySelectorAll('main > section')].slice(0,3).map(s=>s.id).join(',')==='inicio,universo,premiacao'));
await ok2('v3 removidos: etapas, faixa de números, grade de 12 recursos e o "N."',async()=>await p.evaluate(()=>!document.querySelector('#como-funciona,.process,.numbers,#recursos-lista,.module-grid,.product-mark')));
await ok2('v3 removidos: microtítulos do topo, Universo, Telegram, vitrine, editor e Checkout',async()=>await p.evaluate(()=>!document.querySelector('.cz-eyebrow')&&['#universo','#no-telegram','#produto','section.builder','#checkout-pix'].every(s=>!document.querySelector(s+' .eyebrow'))));
await ok2('v3 Recursos: os 6 cartões ilustrados continuam',async()=>await p.evaluate(()=>document.querySelectorAll('#recursos .solucoes > li').length===6));
// travessão no meio de uma frase (o "—" sozinho do status vazio em Baixar mídias não é frase)
await ok2('v3 texto: sem travessão nas frases da página',async()=>await p.evaluate(()=>!/[\wÀ-ú,.!?)][  ]+—[  ]*[\wÀ-ú(]|[\wÀ-ú]—[\wÀ-ú]/.test(document.querySelector('main').innerText)),'');
await ok2('v3 topo: "Só PIX" diz "direto no seu gateway"',async()=>await p.evaluate(()=>[...document.querySelectorAll('.cz-fatos li')].some(l=>/Só PIX/.test(l.textContent)&&/direto no seu gateway/i.test(l.textContent))));
await ok2('v3 Checkout: benefício "Receba diretamente no seu gateway"',async()=>/Receba diretamente no seu gateway/.test(await p.textContent('#checkout-pix')));
await clica('.demo-produto >> nth=1'); await ok2('v3 Checkout: o celular mostra o produto escolhido',async()=>await p.evaluate(()=>document.querySelector('[data-etapa="1"] .ck-titulo').textContent==='Pack de Presets'&&document.querySelector('.ck-pagar').textContent.includes('29,90')));
await clica('[data-acao="gerar"]'); await ok2('v3 Checkout: PIX gerado sem código falso, com aviso de simulação visível',async()=>await p.evaluate(()=>{const e=document.querySelector('[data-etapa="2"]');return !/PIX-DE-DEMONSTRACAO|000201/.test(e.textContent)&&getComputedStyle(document.querySelector('.ck-aviso')).display!=='none'&&/não é real/.test(document.querySelector('.ck-aviso').textContent)}));
await clica('[data-acao="voltar"]');
await p.locator('.showcase-tab').nth(1).click(); await p.waitForTimeout(300);
await ok2('v3 Vitrine: lista de abas só com abas e painel ligado à aba ativa',async()=>await p.evaluate(()=>{const l=document.querySelector('.showcase-tabs');return [...l.children].every(c=>c.getAttribute('role')==='tab')&&document.querySelector('#showcase-painel').getAttribute('aria-labelledby')==='aba-conversas'}));
await ok2('v3 Editor: nome do fluxo coberto por "Fluxo de exemplo"',async()=>await p.evaluate(()=>{const m=document.querySelector('.bx-nome-mask');return !!m&&m.textContent==='Fluxo de exemplo'&&m.getBoundingClientRect().width>40}));
await ok2('v3 Marca d\'água: antes e depois da mesma foto de produto',async()=>await p.evaluate(()=>{const [a,d]=[...document.querySelectorAll('#marca-palco img')].map(i=>i.getAttribute('src'));return /marca-produto-antes/.test(a)&&/marca-produto-(logo|texto)/.test(d)}));
await ok2('v3 Telegram: uma pausa para cada mensagem da conversa',async()=>await p.evaluate(()=>document.querySelectorAll('#tg-chat > *').length===8));
await ok2('Sem erros no console (v3, computador)',async()=>p.erros.length===0,p.erros.join('|'));
p=await pagina(1440,900,{reducedMotion:'reduce'});
await ok2('v3 Telegram: com menos movimento a conversa aparece inteira até "Entrar no grupo VIP"',async()=>await p.evaluate(()=>{const c=document.querySelector('#tg-chat');const u=c.lastElementChild.getBoundingClientRect(),r=c.getBoundingClientRect();return getComputedStyle(c.lastElementChild).display!=='none'&&u.bottom<=r.bottom+2}));
for (const w of [320,390]) {
  p=await pagina(w,800,{isMobile:true,hasTouch:true});
  await ok2(`v3 Faixa de fatos no celular ${w}px: 5 fatos inteiros, nada cortado`,async()=>await p.evaluate(()=>{const de=document.documentElement;const li=[...document.querySelectorAll('.cz-fatos li')];return li.length===5&&li.every(l=>{const r=l.getBoundingClientRect();return r.left>=0&&r.right<=de.clientWidth&&l.scrollWidth<=l.clientWidth+1})&&!document.querySelector('.cz-fatos button,.cz-fatos [data-pr]')}));
}
console.log(res.join('\n')); await b.close();
