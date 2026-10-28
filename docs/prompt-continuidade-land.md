Você vai continuar a landing page da Núcleo (nucleobot.com.br), que já existe. Estou
enviando o zip da land (o mais recente: lannucleo-28-10-v3.zip) e o "Manual de
continuidade da land, edição de 28/10/2026" em PDF. Leia o GUIA-DA-LAND.md, o
README.md e o manual ANTES de propor ou mudar qualquer coisa. Se o pedido mexer em
preço, taxa, limites, gateways ou no que a plataforma faz, eu mando também o zip da
plataforma (nucleo-27-10-plano-com-manual.zip) para você conferir no código.

O QUE É
A land é o site de apresentação da Núcleo Bot, uma plataforma (SaaS) onde donos de
conteúdo conectam bots do Telegram e vendem por PIX, com entrega automática do
acesso. A land é OUTRO projeto, separado do painel e da API: um site estático, sem
banco, sem login, sem formulário e sem variável de ambiente. Ela não conversa com a
API; só tem links para app.nucleobot.com.br (/cadastro, /entrar, /termos).
Eu sou o dono. NÃO sou programador: me explique em palavras simples.

COMO É FEITA
- Tudo o que o visitante vê está num arquivo só: public/index.html (~200 KB), com
  o estilo num <style> no topo e os scripts num <script> no fim. Sem framework, sem
  build, sem biblioteca de fora. Fonte Inter local (public/assets/fonts).
- O estilo tem quatro blocos, nesta ordem: o original; "27/10/2026 — Seções novas e
  tema claro"; "27/10/2026 (v2): visual espacial da referência" (classes cz-*,
  pr-*, cp-*, so-*, escuro-sempre); e "28/10/2026 (v3): 13 correções" (tgx-*, tm-*,
  vx, bx-*, ck-*, pgx-*, mx-*). O script tem o original e, depois,
  "27/10/2026: partes novas" (tema, Universo, demonstrações, prêmios, perguntas,
  assistente).
- Imagens em public/assets (WebP; PNG só quando precisa de transparência simples).
  A arte espacial (espaco-*.webp) foi renderizada por ferramentas/arte.py e a foto
  de produto da marca d'água (marca-produto-*.webp) por ferramentas/produto.py e
  marca_produto.py, sem serviço de fora.
- Servida por Nginx num container Docker (Dockerfile + nginx.conf), publicada pelo
  Coolify a partir de um repositório Git, porta 80, /health responde "ok". O Nginx
  guarda /assets/ em cache por 30 dias.
- Testes prontos em ferramentas/testes (Playwright + Chromium): matriz.mjs (12
  tamanhos x 2 temas), interacao.mjs (53 testes de clique), foto.mjs e secao.mjs
  (capturas). Como rodar: ferramentas/testes/LEIA-ME.md.

O VISUAL (APROVADO PELO DONO)
- Espacial, escuro e roxo (#8f00ff), com planeta, anéis inclinados como o logo,
  estrelas e chão rochoso, seguindo a referência do PDF "Refinamento anti-IA".
- Tema claro e escuro (botão de sol/lua; escolha guardada só no aparelho). O topo,
  a Premiação e o Checkout ficam escuros nos dois temas (classe escuro-sempre).
- Não troque o conceito: mude, melhore e corrija dentro dele.

COMO EU QUERO QUE VOCÊ TRABALHE
- Sempre em português, simples e direto, sem jargão.
- Nunca diga que algo funciona sem ter testado. Depois de mexer, sirva a pasta
  public e rode, da raiz do projeto:
    node ferramentas/testes/matriz.mjs http://localhost:8090/     -> 24 de 24 OK
    node ferramentas/testes/interacao.mjs http://localhost:8090/  -> 53 passaram
  (rode os testes de clique duas vezes). Olhe as capturas: computador (1440) e
  celular (390), temas escuro e claro. Conte o que testou.
- Se um teste falhar, investigue e diga se o defeito é da página ou do teste. NÃO
  ajuste o teste só para passar. Correção de defeito: prove que o teste reprova sem
  a correção. Funcionalidade nova entra com teste novo no interacao.mjs.
- Me mande as imagens do ANTES e do DEPOIS (computador e celular).
- No fim: zip novo da land (sem .git), README e GUIA-DA-LAND.md atualizados (com
  uma linha nova no "Histórico") e este prompt/manual atualizados se algo mudou.
- Não publique nada, não troque domínio e não chame serviço de fora sem eu pedir.

REGRAS QUE NÃO PODEM SER QUEBRADAS
- Só PIX, em reais: nada de cartão, boleto, moeda estrangeira, países ou "pagamentos
  globais" em lugar nenhum (nem em imagem).
- Nada inventado: sem números de clientes, faturamento, estabilidade, depoimentos,
  ganhadores de prêmio, selos ou logos de parceiros sem prova. Os valores que
  aparecem nas capturas do painel são dados de exemplo e não podem virar
  "resultado" no texto.
- Toda promessa confere com o código da plataforma (tabela "Promessas" do manual).
  Função que não existe = "em breve" (ou "em desenvolvimento").
- Demonstração é sempre marcada como demonstração, roda só no navegador e nunca
  cobra nem envia nada.
- Preço é decisão do dono: não escreva "grátis", desconto ou prazo sem eu pedir.
  Valores das Ferramentas não vão na land (são configuráveis no Admin).
- Nada de nome real de pessoa em imagem. Captura nova do painel só de conta de
  demonstração.
- Imagem nova sempre com NOME NOVO (cache de 30 dias). Nunca sobrescreva um arquivo
  de assets/ com conteúdo diferente.
- Estilo novo com classe própria. Cor fixa quebra o tema claro: use as variáveis
  (var(--surface), var(--white)...) ou acrescente a regra do tema claro.
- Grade com uma coluna: use minmax(0, 1fr), nunca 1fr sozinho (o conteúdo largo
  empurra a página para o lado).
- Não ponha backdrop-filter no cabeçalho (.site-header): ele faz o menu do celular
  ficar preso no cabeçalho.
- Acessibilidade e leveza: foco visível, textos alternativos, contraste, "menos
  movimento" respeitado (prefers-reduced-motion), imagens abaixo da dobra com
  loading="lazy", e o celular usando imagens menores.

ESTADO ATUAL (28/10/2026)
- A land v3 (lannucleo-28-10-v3.zip) está pronta e testada, mas AINDA NÃO
  PUBLICADA. Ela é a v2 com as 13 correções de 28/10 (menos seções repetidas,
  Premiação como 3ª seção, celulares do Telegram, Checkout e Páginas refeitos,
  vitrine e editor de fluxos maiores, marca d'água com foto de produto, sem
  travessões no meio das frases). Ela fala de funções que entram com a atualização da plataforma
  (migrações 0050/0051: Checkout PIX, UTMify, bot de suporte, limpeza, planos em
  dias). Publique a land só DEPOIS da plataforma.
- Testes da última entrega: 53 de 53 nos cliques (duas rodadas), 24 de 24 tamanhos
  sem nada sobrando para os lados e sem erro no console. Lighthouse (servidor
  simples, sem compressão): celular velocidade 90, acessibilidade 100; computador
  velocidade 99, acessibilidade 100.

PENDÊNCIAS (decisões minhas)
1. Regras de elegibilidade e envio dos prêmios (hoje "em breve").
2. Prêmio de 50K: a land tem, a Corrida da plataforma não (10K, 100K, 500K, 1M).
3. Canal de atendimento humano (o suporte inteligente ainda não existe).
4. Se quero "grátis" na explicação das Ferramentas (hoje: "cota diária").
5. Se a arte espacial deve ser trocada por arte gerada no Higgsfield (precisa de
   plano pago); se trocar, só as imagens mudam.
6. Se os microtítulos roxos que sobraram (Páginas inteligentes, Ferramentas,
   Soluções, Premiação etc.) e a linha "Tudo em um só lugar" do topo também saem.
Pequenos ajustes técnicos conhecidos: não há robots.txt; assets/nucleo-core.webp e
nucleo-mascot.webp não são usados; não existe captura escura do editor de fluxos.

COMECE ASSIM: leia o GUIA-DA-LAND.md, o README e o manual; sirva a pasta public;
rode os dois testes e me diga o que entendeu, o estado atual e se deram 24 de 24 e
53 de 53. Só então eu digo o que quero mudar.

Observação de uso: se for abrir o chat para uma mudança específica, troque o
"COMECE ASSIM" pela mudança — o resto do texto é o que evita erro.
