# Guia da land da Núcleo

Atualizado em 28/10/2026 (v3: 13 correções). Este arquivo é a versão em texto do "Guia da land da Núcleo" (PDF de 29/09/2026),
já com as mudanças de 27/10/2026 e de 28/10/2026.

## Como usar num chat novo

Mande o zip da land junto com este guia e cole o texto abaixo:

> Você vai atualizar a landing page da Núcleo (nucleobot.com.br). Mando o zip do projeto e o guia.
> Leia o GUIA-DA-LAND.md e o README.md antes de mexer. Sou o dono, não sou programador: explique em palavras simples.
> Regras: toda a página está num arquivo só (public/index.html). Não invente números, depoimentos nem clientes.
> Não coloque nome de pessoa real em imagem. Depois de mexer, abra a página no computador (1440 px) e no celular
> (390 px) com o Playwright, nos temas escuro e claro, confira que nada fica cortado nem sobra para os lados,
> e me mande as imagens do antes e depois. No fim, me entregue o zip novo e atualize a parte "Histórico" do guia.
> O que eu quero mudar: <escreva aqui>

Se o pedido mexer em preço, taxa, limites, gateways ou no que a plataforma faz, mande também o zip do sistema,
para o outro chat conferir no código.

## O que é a land

Página de apresentação fixa: sem banco de dados, login, formulário ou variável de ambiente. Tudo o que o visitante
vê está em `public/index.html` (texto, estilo e scripts juntos).

- Onde roda: container Docker com Nginx, publicado pelo Coolify a partir de um repositório Git, porta 80.
- Endereço: https://nucleobot.com.br/ (a prévia do link foi feita para esse endereço).
- Ligação com o painel: só links para `app.nucleobot.com.br` (`/cadastro`, `/entrar`, `/termos`).
- Independência: a land não conversa com a API. As demonstrações da página (PIX, baixar mídias, suporte) rodam
  só no navegador de quem visita e não enviam nada para lugar nenhum.
- Visual: fundo preto, roxo `#8f00ff`, fonte Inter local. Desde 27/10/2026 há também um **tema claro**
  (botão de sol/lua no topo; a escolha fica guardada só no aparelho de quem visita).

## Arquivos

| Arquivo | Para que serve |
|---|---|
| `public/index.html` | A página inteira: textos, estilo (`<style>` no topo) e scripts (`<script>` no fim) |
| `public/assets/dashboard-real.webp`, `conversas-real.webp`, `remarketing-real.webp`, `fluxo-pagamentos-real.webp` | Capturas do painel (topo, vitrine, fluxos). A do editor de fluxos aparece recortada e com o nome do fluxo coberto por "Fluxo de exemplo" |
| `public/assets/checkout-editor-real.webp` | Aba 04 "Checkout" da vitrine (editor do Checkout, conta de demonstração) |
| `public/assets/paginas-editor-real.webp`, `pagina-celular-real.webp` | Seção Páginas: editor e a página no celular (conta de demonstração "Estúdio Órbita") |
| `public/assets/ferramentas-midias-real.webp` | Seção Baixar mídias: a janela real do painel |
| `public/assets/espaco-*.webp`, `espaco-estrelas.png` | Arte espacial renderizada para a land (céu, planeta com anéis, rochas, pedras, borda de planeta, ícones redondos, estrelas). Feita pelo script `arte.py` (vai na pasta `ferramentas/` do zip). Para trocar por outra arte, use o mesmo nome de arquivo só se mudar também o nome no HTML (cache) |
| `public/assets/marca-produto-antes/logo/texto-1200/720.webp` | Antes/depois da marca d'água (desde 28/10). A **mesma** foto de produto nos três (frasco de sérum e pote de creme da loja fictícia "órbita"), renderizada por `ferramentas/produto.py`; a logo e o "@sualoja" foram aplicados por `ferramentas/marca_produto.py`, que imita as opções da ferramenta (não é a função da plataforma) |
| `public/assets/premio-10k/50k/100k/500k/1m-560.webp` e `-1000.webp` | Fotos dos prêmios (celular e computador) |
| `public/assets/rede-instagram/facebook/x/tiktok.png` | Ícones das redes aceitas no Baixar mídias (os mesmos do painel) |
| `public/assets/logo-nucleo.webp`, `logo-nucleo-claro.webp` | Logo do tema escuro e do tema claro |
| `public/assets/simbolo-nucleo.webp` / `.png` | Símbolo (aba, iPhone, fim da página, assistente) |
| `public/assets/logo-dotfy.png`, `logo-syncpay.png`, `logo-meta.png`, `logo-tiktok.png` | Integrações |
| `public/assets/compartilhar.png` | Prévia do link (1200 × 630) |
| `public/assets/fonts/inter.woff2` + `LICENSE-Inter.txt` | Fonte local (OFL) |
| `public/assets/nucleo-core.webp`, `nucleo-mascot.webp` | Não usadas hoje (da versão anterior) |
| `nginx.conf`, `Dockerfile`, `docker-compose.yml` | Servidor e container. Não mudaram |

## Seções, de cima para baixo

| # | Seção (classe · id) | O que mostra |
|---|---|---|
| 1 | `site-header` | Logo, menu na ordem da página (Plataforma, Premiação, No Telegram, Checkout, Páginas, Ferramentas, Preço, Dúvidas), botão de tema, Entrar, Criar conta |
| 2 | `hero cosmos` · `#inicio` | Título (sem microfrase em cima), céu, planeta com anéis, 6 cartões com as funções (`cz-chips`), painel real inclinado e a faixa de fatos (`cz-fatos`: 20 bots, Só PIX "direto no seu gateway", R$ 0,75, Entrega, Aviso). No celular a faixa é uma lista num quadro só. Sempre escuro |
| 3 | `universo` · `#universo` | "Seis frentes, um só painel": órbitas clicáveis (Bots, Checkout PIX, Páginas, Remarketing, Análises, Ferramentas). No celular viram abas |
| 4 | `premiacao` · `#premiacao` | Prêmios em "escadinha" sobre o chão rochoso (10K pulseira + carta; 50K, 100K, 500K, 1M placas). No celular vira carrossel. Regras "em breve". Sempre escura. 3ª seção desde 28/10 |
| 5 | `chat-section` · `#no-telegram` | Celular com a conversa do Telegram (8 mensagens animadas) e o aviso "PIX pago" |
| 6 | `product` · `#produto` | Vitrine: 4 abas em linha (Visão geral, Conversas, Remarketing, Checkout) e a tela larga embaixo |
| 7 | `builder` | Título, três itens e o botão em cima; a captura do editor de fluxos larga, numa janela escura |
| 8 | `checkout-pix` · `#checkout-pix` | O que o Checkout faz + **simulação** de compra num celular, no formato da página de compra real (Seus dados → PIX → Aprovado). Sempre escura |
| 9 | `paginas` · `#paginas` | Páginas Inteligentes: editor real + página num celular com moldura de aparelho + quatro itens |
| 10 | `marca` · `#ferramentas` | Marca d'água: antes/depois arrastável numa foto de produto (logo ou texto) e as opções reais em blocos curtos |
| 11 | `midias` · `#baixar-midias` | Baixar mídias: redes aceitas, limites, **demonstração** das etapas e a tela real |
| 12 | `modules` · `#recursos` | "Muito mais que um bot": 6 cartões ilustrados (`solucoes`) |
| 13 | `integrations` · `#integracoes` | Telegram, Dotfy, SyncPay, Meta, TikTok, UTMify |
| 14 | `pricing` · `#preco` | R$ 0,75 por venda + nota (SyncPay e Ferramentas) |
| 15 | `novidades` · `#novidades` | O que mudou (com datas) e "No forno" (Área de membros em desenvolvimento, Suporte inteligente em breve) |
| 16 | `faq` · `#faq` | Perguntas com abas por assunto (Como funciona, Pagamentos, Ferramentas, Segurança) |
| 17 | `suporte-ia` · `#suporte` | "Você não precisa configurar tudo sozinho": assistente **em breve**, com conversa de exemplo |
| 18 | `final-cta` · `#acesso` | Quadro final |
| 19 | `site-footer` | Logo, links, ano |

Saíram em 28/10/2026: a seção de etapas ("Menos ferramentas. Mais operação.", `#como-funciona`), a faixa "10 / 10 / 24/7 / 0" (`.numbers`) e a grade de 12 recursos ("Tudo o que vem junto", `#recursos-lista`), com o estilo de cada uma.

## Promessas que precisam bater com a plataforma

Conferido no código do sistema em 27/10/2026.

| Informação | Valor hoje | De onde vem no sistema |
|---|---|---|
| Taxa da Núcleo | R$ 0,75 por venda aprovada (bot, Checkout e Páginas). Aparece também na faixa de fatos do topo | `tenants.platform_fee_fixed_cents` |
| Taxa no SyncPay | % inteira mais perto de R$ 0,75, mínimo 1% | `integrations/syncpay.ts` |
| Bots por conta / por fluxo / planos por fluxo | 20 / 10 / 10 | `tenants.max_bots`, `MAX_BOTS_PER_FLOW`, `MAX_PLANS_PER_FLOW` |
| Formas de pagamento | **Só PIX** (sem cartão, boleto ou moeda estrangeira) | gateways Dotfy e SyncPay |
| Baixar mídias: redes | Instagram, Facebook, X e TikTok. **Telegram não** | `services/midias` |
| Baixar mídias: limites | 20 links por lote; vídeo até 20 min e 200 MB; ZIP com 2+ arquivos | `services/midias` |
| Marca d'água | Logo (PNG) ou texto; 9 posições ou mosaico; opacidade 5–100%; tamanho; margem; cor. Imagem até 20 MB, 50 por lote, ZIP até 50 MB | `services/midias/app/marca.py` |
| Valor das Ferramentas | Configurável no Admin (cota diária e preço do lote). **Não escrever valores na land** | `ferramentas/servico.ts` |
| Páginas | Blocos, arrastar, estilos, prévia celular/computador, métricas, Mini App | módulo páginas |
| Checkout | Editor próprio, entrega automática, pixel Meta/TikTok com aviso de cookies, UTMify | módulo checkout |
| Planos | Por mês, ano ou em dias | migração 0050 |
| Segurança | Tokens e chaves guardados cifrados e mostrados só mascarados; 2FA; permissões de equipe | API |
| Suporte inteligente | **Não existe ainda** → "em breve" | — |
| Área de membros | **Em desenvolvimento** | — |
| Regras dos prêmios | **O dono ainda não passou** → "em breve" | — |

## Partes que se mexem (scripts no fim do `index.html`)

Tudo que já existia continua igual (`.reveal`, menu, vitrine, conversa do Telegram, perguntas, ano). Novos em 27/10/2026:

- **Tema claro/escuro**: um script curto no `<head>` aplica o tema salvo antes de a página aparecer (sem piscar).
  O botão `#tema-botao` troca `data-tema="claro"` no `<html>` e salva em `localStorage` (`nucleo-land-tema`).
  As cores do tema claro ficam no bloco `html[data-tema="claro"]` do estilo.
- **Universo**: os textos de cada órbita ficam no objeto `universo` do script. Botões com `data-u`. O planeta do centro é `espaco-planeta-640.webp`.
- **Topo espacial**: camadas separadas (céu, planeta, rochas, pedras) posicionadas por CSS (`cz-*`). No celular o céu é outra imagem, em pé (`espaco-ceu-celular-900.webp`). O planeta flutua devagar; com menos movimento, fica parado.
- **Seções sempre escuras**: a classe `escuro-sempre` mantém o topo, os prêmios e o Checkout escuros mesmo no tema claro.
- **Demonstração do Checkout**: a escolha do produto de exemplo fica acima do celular e muda nome e preço em todas as etapas. 3 etapas (`data-etapa`): Seus dados, Pague com PIX, Pagamento aprovado. Faixa laranja "Simulação: o PIX desta página não é real e nada é cobrado" no topo do celular. O QR é um desenho apagado (não é código PIX) com DEMONSTRAÇÃO, e não há código copia e cola.
- **Conversa do Telegram**: 8 mensagens em `#tg-chat`, cada uma com sua pausa em `pausas` (uma por mensagem). Mensagem e botões do mesmo envio ficam juntos (`.tm-grupo`).
- **Vitrine**: só as abas ficam dentro da lista de abas; o painel `#showcase-painel` aponta para a aba ativa.
- **Marca d'água**: o corte do antes/depois é um `<input type="range">` invisível por cima (funciona com o dedo, o mouse e as setas do teclado).
- **Baixar mídias**: etapas de exemplo; o botão "Baixar ZIP" não baixa nada.
- **Premiação**: no celular a galeria rola de lado; as setas ajudam.
- **Perguntas**: abas por assunto (`data-faq` em cada pergunta).
- **Suporte inteligente**: respostas de exemplo no objeto `respostas`, escritas a partir das telas reais do painel.
- **Menu**: abaixo de 860 px vira o botão de três riscos (com o botão de tema ao lado). Entre 861 e 1320 px os links
  com `hide-md` (Plataforma, Páginas, Premiação) somem para caber numa linha.
- **Menos movimento**: quem pede menos movimento no aparelho vê tudo parado e as demonstrações sem espera.

## Regras para não quebrar

1. Nada de nome real nas imagens. Captura nova só de conta de demonstração.
2. Nada inventado: sem depoimentos, clientes, faturamento, ganhadores ou número de usuários.
3. Toda promessa confere com o sistema (tabela acima). Função que não existe = "em breve" ou "em desenvolvimento".
4. Preço é decisão do dono. Não escreva "grátis", desconto ou prazo sem ele pedir. Valores das Ferramentas não vão na land.
5. Demonstração é sempre marcada como demonstração e nunca cobra nada.
6. Teste em 320, 360, 375, 390, 430, 768, 870, 1024, 1151 e 1440 px, nos dois temas: `scrollWidth` igual à largura da tela e console sem erros.
10. Sem travessão no meio das frases (pedido do dono em 28/10). Use ponto, vírgula ou dois-pontos.
7. Estilo novo com classe própria. Cor fixa (ex.: `#111`) quebra o tema claro: use as variáveis (`var(--surface)`, `var(--white)`…) ou acrescente a regra no bloco do tema claro.
8. Imagem nova com nome novo (cache de 30 dias em `/assets/`).
9. Sem serviço de fora sem o dono pedir.

## Testar e publicar

```bash
cd public && python3 -m http.server 8090
# em outro terminal, na raiz do projeto:
node ferramentas/testes/matriz.mjs http://localhost:8090/      # 24 de 24 OK
node ferramentas/testes/interacao.mjs http://localhost:8090/   # 53 passaram (rode duas vezes)
node ferramentas/testes/foto.mjs http://localhost:8090/ depois 1440,390   # imagens do antes e depois
```

Detalhes em `ferramentas/testes/LEIA-ME.md`. O manual completo da land está em `docs/manual-continuidade-land.pdf`.

Container igual ao do ar: `docker build -t nucleo-landing .` e `docker run --rm -p 8080:80 nucleo-landing`
(`/health` responde `ok`). Publicar: enviar ao Git e fazer o deploy no Coolify (Dockerfile, porta 80).
Para voltar atrás, faça o deploy da versão anterior: a land não guarda dado nenhum.

**Atenção na ordem:** a land de 27/10/2026 (e a v3 de 28/10, que só corrigiu visual e texto) fala de Checkout PIX, UTMify, bot de suporte, limpeza programada e planos
em dias. Publique primeiro a atualização da plataforma e só depois a land.

## Histórico (a mais nova em cima)

| Data | O que mudou |
|---|---|
| 28/10/2026 (v3) | 13 correções do PDF de 28/10: topo sem microfrase, parágrafo sem travessão e "Só PIX · direto no seu gateway"; sem microtítulo no Universo, Telegram, vitrine, editor e Checkout; saíram as etapas, a faixa de números, a grade de 12 recursos e o "N."; celular do Telegram refeito; vitrine com abas em linha e tela maior; editor de fluxos com captura larga numa janela escura e nome do fluxo coberto; Checkout no formato da página de compra real ("Receba diretamente no seu gateway"); celular das Páginas com moldura de aparelho; marca d'água com foto de produto (mesma foto antes e depois); faixa de fatos do celular em lista; Premiação como 3ª seção e menu na ordem da página; travessões tirados das frases. 17 testes novos (53 no total) |
| 27/10/2026 (2) | Visual da referência do PDF de refinamento: topo com planeta, anéis e cartões das funções, faixa de fatos com ícones de planeta, prêmios em escadinha sobre chão rochoso, cartões ilustrados "Muito mais que um bot", Checkout num celular sobre a borda de um planeta, planeta no centro do Universo e estrelas no fundo das seções escuras. Arte renderizada para a land (o Higgsfield exigia plano pago) |
| 27/10/2026 | Seções novas: Universo Núcleo (órbitas/abas), Checkout PIX com demonstração, Páginas Inteligentes, Marca d'água (antes/depois), Baixar mídias, Premiação, Novidades e Suporte inteligente (em breve). Aba 04 "Checkout" na vitrine, 3 recursos novos, UTMify nas integrações, perguntas por assunto (+6), planeta com anéis no topo, tema claro, menu novo (Plataforma, No Telegram, Checkout, Páginas, Ferramentas, Premiação, Preço, Dúvidas) |
| 29/09/2026 | Tirada a tela "Mapa de acessos" da vitrine |
| 29/09/2026 | Seção Preço, pergunta "Quanto custa?", "Preço" no menu |
| 29/09/2026 | Botões para o cadastro, faixa de números corrigida, conversa do Telegram, SyncPay, recursos e perguntas novos, Inter local, prévia do link, ícone do iPhone |
| 21/09/2026 | Primeira versão da land |
