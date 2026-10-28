# Testes da land

Precisam do Node 18+ e do Playwright com o Chromium (`npm i playwright` e `npx playwright install chromium`,
se a máquina ainda não tiver). Sirva a pasta `public` antes:

```bash
cd public && python3 -m http.server 8090      # ou o container: docker run --rm -p 8090:80 nucleo-landing
```

| Script | O que faz | Como rodar |
|---|---|---|
| `matriz.mjs` | Abre a página em 12 tamanhos (320 a 1440 px e celular deitado), nos temas escuro e claro. Diz se algo sobra para os lados (`scrollWidth` maior que a tela), se há imagem quebrada e se há erro no console. Tem de dar **24 de 24 OK**. | `node ferramentas/testes/matriz.mjs http://localhost:8090/` |
| `interacao.mjs` | 53 testes de clique e funcionamento: âncoras, tema, menu do celular, Universo, vitrine, demonstração do PIX, antes/depois, baixar mídias, prêmios, perguntas, assistente, movimento reduzido, foco do teclado, links externos; e, desde 28/10, os 17 que começam com "v3" (as 13 correções). Tem de dar **53 passaram, 0 falharam**. Rode duas vezes. | `node ferramentas/testes/interacao.mjs http://localhost:8090/` |
| `foto.mjs` | Captura da página inteira (rola antes, para carregar as imagens). Use para o antes e depois. | `node ferramentas/testes/foto.mjs http://localhost:8090/ depois 1440,390` (acrescente `claro` para o tema claro) |
| `secao.mjs` | Captura de uma seção só. | `node ferramentas/testes/secao.mjs http://localhost:8090/ '#premiacao' premiacao 1440,390` |

Rode os scripts a partir da raiz do projeto, com o Playwright instalado ali ou globalmente.
Se um teste falhar, investigue se o defeito é da página ou do teste antes de mexer no teste
(em 27/10 um teste falhou por olhar o cartão antes do fim da animação de 0,3 s — o defeito era do teste).

Em 28/10 os testes "v3" foram rodados também contra a versão anterior (v2): os 12 que conferem as correções
reprovam lá, e os 36 antigos passam. É a prova de que eles pegam o que foi corrigido.
