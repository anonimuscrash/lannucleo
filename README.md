# Núcleo — Landing pronta para Coolify

Este pacote contém a landing estática completa da Núcleo, servida por Nginx em um container Docker.

## Configuração recomendada no Coolify

1. Descompacte este pacote e envie os arquivos para um repositório Git.
2. No Coolify, crie um novo recurso usando esse repositório.
3. Selecione **Dockerfile** como método de build.
4. Use `/Dockerfile` como caminho do Dockerfile.
5. Configure a porta exposta como **80**.
6. Adicione o domínio desejado e faça o deploy.

O endpoint de verificação de saúde é `/health`. Não é necessário configurar banco de dados, variáveis de ambiente ou volume persistente.

## Domínios já conectados na página

- Login: `https://app.nucleobot.com.br/entrar`
- Termos: `https://app.nucleobot.com.br/termos`

## Teste local opcional

```bash
docker build -t nucleo-landing .
docker run --rm -p 8080:80 nucleo-landing
```

Depois, abra `http://localhost:8080`.


## Atualização de 29/09/2026

- Botões de entrada ("Criar conta", "Criar minha conta") agora levam ao **cadastro** (`/cadastro`); "Entrar" continua no login.
- Corrigido o estilo da faixa logo abaixo do topo: os números "20 / Pix / Auto" voltaram a aparecer grandes e roxos.
- Nova seção **"O que seu cliente vê"** (`#no-telegram`): um celular com a conversa do bot se montando sozinha
  (boas-vindas com foto e áudio, planos, order bump, "Aguarde...", PIX, acesso liberado) e o aviso "PIX pago" no celular.
  Quem pede menos movimento no aparelho vê a conversa parada, inteira.
- Recursos novos na página: recuperação de vendas, aviso no celular (com modo discreto) e assinaturas no automático.
- Integrações: **SyncPay** ao lado da Dotfy, Meta e TikTok com nome e função.
- Mais três perguntas no "Direto ao ponto".
- Fonte **Inter** hospedada na própria land (`assets/fonts/inter.woff2`, licença OFL junto) — antes a página pedia Inter mas não carregava, e aparecia em Arial.
- Prévia do link no WhatsApp/Telegram: `assets/compartilhar.png` (1200×630) e as tags `og:`.
  **Se a land não estiver em `https://nucleobot.com.br/`, troque esse endereço nas linhas `og:url` e `og:image` do `index.html`.**
- Ícone para a tela inicial do iPhone (`assets/simbolo-nucleo.png`).

Nada mudou no Nginx, no Dockerfile nem no Coolify: é só publicar de novo.
- Tirada a tela "Mapa de acessos" da vitrine de telas (ficaram Visão geral, Conversas e Remarketing).
- Seção **Preço** (`#preco`): R$ 0,75 por venda aprovada, sem mensalidade, com exemplo de uma venda de R$ 29,90 e a
  observação do SyncPay (lá a taxa vira a porcentagem inteira mais próxima, mínimo de 1%) e da taxa do gateway, que é à parte.
  Também entrou a pergunta "Quanto custa?" no topo das dúvidas e "Preço" no menu.
  **Se a taxa mudar, troque os valores nessa seção, na pergunta "Quanto custa?", na linha de destaques do topo e na
  descrição da prévia do link (`og:description`).**

## Atualização de 27/10/2026

Leia também o **GUIA-DA-LAND.md** (seções, regras e o que precisa bater com a plataforma).

- **Seções novas:** Universo Núcleo (`#universo`), Checkout PIX com demonstração de compra (`#checkout-pix`),
  Páginas Inteligentes (`#paginas`), Marca d'água com antes/depois (`#ferramentas`), Baixar mídias (`#baixar-midias`),
  Premiação (`#premiacao`), Novidades (`#novidades`) e Suporte inteligente, marcado "em breve" (`#suporte`).
- **Mudanças nas seções antigas:** aba 04 "Checkout" na vitrine; recursos Bot de suporte, Limpeza programada e UTMify;
  UTMify nas integrações; perguntas com abas por assunto e seis perguntas novas; planeta com anéis no topo; menu novo.
- **Tema claro:** botão de sol/lua no topo. A escolha fica guardada só no aparelho de quem visita.
- **Demonstrações** (PIX, baixar mídias, assistente) rodam só no navegador e não cobram nem enviam nada.
- **Imagens novas** em `public/assets/` (todas com nome novo, por causa do cache de 30 dias).
- **Ordem de publicação:** primeiro a atualização da plataforma (Checkout, UTMify, bot de suporte etc.), depois a land.

Nada mudou no Nginx, no Dockerfile nem no Coolify.

### Visual espacial (27/10/2026, segunda entrega)

- A página segue agora a referência visual do PDF de refinamento: topo com planeta e anéis, cartões das funções em volta,
  prêmios em escadinha sobre chão rochoso, cartões ilustrados "Muito mais que um bot" e Checkout num celular.
- A arte (`public/assets/espaco-*`) foi renderizada para a land pelo script `ferramentas/arte.py`, sem serviço de fora.
- Topo, prêmios e Checkout ficam escuros também no tema claro.

### Manual de continuidade (27/10/2026)

- `docs/manual-continuidade-land.pdf`: manual completo da land para quem pega o projeto sem histórico, com o prompt para o chat novo no Anexo A (o prompt também está em `docs/prompt-continuidade-land.md`).
- `ferramentas/testes/`: os testes usados nas entregas (tamanhos, cliques e capturas). Como rodar: `ferramentas/testes/LEIA-ME.md`.
- Removido do `index.html` o CSS do planeta de linhas da primeira versão, que não era mais usado.

## Atualização de 28/10/2026 (v3): 13 correções

Base: o PDF "Núcleo Landing · 13 correções" de 28/10/2026. Nada mudou no Nginx, no Dockerfile nem no Coolify.

- **Topo:** saiu a microfrase acima do título; o parágrafo foi reescrito sem travessão; na faixa de fatos, "Só PIX" agora diz "direto no seu gateway". No celular, os 5 fatos ficam numa lista dentro de um quadro só.
- **Saíram:** a seção "Menos ferramentas. Mais operação." (`#como-funciona`), a faixa "10 / 10 / 24/7 / 0", a grade de 12 recursos ("Tudo o que vem junto") e o "N." grande da vitrine, com o estilo e os links de cada um. Os microtítulos do Universo, Telegram, vitrine, editor de fluxos e Checkout também saíram.
- **Premiação** virou a 3ª seção (depois do topo e do Universo). O menu e o rodapé seguem a ordem da página.
- **Telegram:** celular refeito (barra de status, cabeçalho do Telegram, balões, botões e campo de mensagem); texto novo pedido pelo dono.
- **Vitrine:** abas em linha em cima e a tela bem maior embaixo; o aviso de acessibilidade herdado sumiu.
- **Editor de fluxos:** texto em cima, captura larga numa janela escura; o nome do fluxo da captura ("Vanessa") está coberto por "Fluxo de exemplo". Não existe captura escura dessa tela.
- **Checkout:** o celular mostra uma página de compra como a real (loja, resumo, Seus dados, PIX, aprovado), com a faixa "Simulação: o PIX desta página não é real e nada é cobrado". O primeiro benefício virou "Receba diretamente no seu gateway".
- **Páginas:** o celular de exemplo ganhou moldura e proporção de aparelho.
- **Marca d'água:** foto de produto (frasco de sérum e pote de creme da loja fictícia "órbita") no lugar do planeta, a mesma foto antes e depois. Renderizada por código (`ferramentas/produto.py`, `ferramentas/marca_produto.py`). As opções ficaram em blocos curtos.
- **Imagens novas:** `marca-produto-*.webp` (6). Saíram `marca-antes*`, `marca-depois-logo*` e `marca-depois-texto*` (não eram mais usadas).
- **Testes:** 17 testes novos no `interacao.mjs` (53 no total).
