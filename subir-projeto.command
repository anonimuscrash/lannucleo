#!/bin/bash
# ============================================================
# Enviar projeto para o GitHub
#
# Genérico: funciona com qualquer projeto, não só com o Operza.
#
# O script anterior verificava a existência de `src/` e de arquivos
# específicos do CRM antes de enviar. Isso fazia sentido lá — evitava
# subir um zip descompactado pela metade. Num projeto de outra
# estrutura, vira uma trava sem propósito.
#
# Aqui a verificação é outra: em vez de exigir arquivos que eu não
# posso prever, ele confere o que realmente causa estrago —
# credenciais e dependências indo junto.
# ============================================================

cd "$(dirname "$0")" || exit 1

echo "============================================================"
echo "  Enviar projeto para o GitHub"
echo "============================================================"
echo ""
echo "Pasta: $(pwd)"
echo ""

# ---------- 1. A pasta tem algo? ----------
ARQUIVOS=$(find . -type f -not -path "./.git/*" -not -path "./node_modules/*" | wc -l | tr -d ' ')

if [ "$ARQUIVOS" -lt 1 ]; then
  echo "✗ A pasta está vazia."
  echo "  Descompacte o projeto aqui antes de rodar."
  echo ""
  echo "Aperte Enter para fechar."
  read -r
  exit 1
fi

echo "[1/7] $ARQUIVOS arquivos encontrados"

# ---------- 2. git instalado ----------
if ! command -v git >/dev/null 2>&1; then
  echo "✗ Git não está instalado."
  echo "  Rode: xcode-select --install"
  echo ""
  read -r
  exit 1
fi
echo "[2/7] git ok ($(git --version))"

# ---------- 3. .gitignore ----------
#
# A verificação que importa. Sem isto você sobe node_modules (milhares
# de arquivos) e, pior, arquivos .env com credenciais — que num
# repositório público ficam expostas para sempre, mesmo depois de
# apagadas, porque o histórico do git guarda tudo.
echo "[3/7] Verificando .gitignore..."

PRECISA_GITIGNORE=0
[ ! -f .gitignore ] && PRECISA_GITIGNORE=1
[ -f .gitignore ] && ! grep -q "node_modules" .gitignore && PRECISA_GITIGNORE=1
[ -f .gitignore ] && ! grep -qE "^\.env|\*\.env|\.env\*" .gitignore && PRECISA_GITIGNORE=1

if [ "$PRECISA_GITIGNORE" -eq 1 ]; then
  echo "  Criando/completando .gitignore..."
  cat >> .gitignore <<'IGNOREEOF'

# --- adicionado pelo script de envio ---
node_modules/
.next/
dist/
build/
out/
.env
.env.*
!.env.example
*.log
.DS_Store
.vercel
coverage/
IGNOREEOF
  echo "  ✓ .gitignore atualizado"
else
  echo "  ✓ .gitignore já cobre node_modules e .env"
fi

# ---------- 4. Credenciais prestes a subir ----------
#
# Última checagem antes do commit. Um .env que já está rastreado pelo
# git não é ignorado pelo .gitignore — ignorar só vale para arquivo
# novo.
echo "[4/7] Procurando credenciais..."

SUSPEITOS=$(find . -maxdepth 2 -type f \( -name ".env" -o -name ".env.local" -o -name "*.pem" -o -name "*.key" \) -not -path "./node_modules/*" 2>/dev/null)

if [ -n "$SUSPEITOS" ]; then
  echo ""
  echo "  ⚠ ATENÇÃO — estes arquivos podem conter credenciais:"
  echo "$SUSPEITOS" | sed 's/^/     /'
  echo ""
  echo "  O .gitignore acima os exclui SE ainda não estiverem no git."
  echo "  Se este repositório for público, confira antes de seguir."
  echo ""
  printf "  Continuar mesmo assim? (s/n): "
  read -r RESP
  if [ "$RESP" != "s" ] && [ "$RESP" != "S" ]; then
    echo "  Cancelado. Nada foi enviado."
    echo ""
    read -r
    exit 0
  fi
else
  echo "  ✓ nenhum arquivo de credencial solto"
fi

# ---------- 5. Repositório ----------
echo ""
REMOTE_ATUAL=$(git remote get-url origin 2>/dev/null | sed -E 's#.*github.com[:/]##; s#\.git$##')

if [ -n "$REMOTE_ATUAL" ]; then
  echo "[5/7] Repositório detectado: $REMOTE_ATUAL"
  printf "      Enter para usar, ou digite outro (usuario/repo): "
  read -r REPO
  [ -z "$REPO" ] && REPO="$REMOTE_ATUAL"
else
  echo "[5/7] Qual repositório do GitHub?"
  echo "      Formato: usuario/repositorio"
  printf "      > "
  read -r REPO
fi

if ! echo "$REPO" | grep -qE '^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$'; then
  echo "✗ Formato inválido. Use: usuario/repositorio"
  echo ""
  read -r
  exit 1
fi

USUARIO=$(echo "$REPO" | cut -d'/' -f1)

# ---------- 6. Commit ----------
echo "[6/7] Preparando o envio..."

if [ ! -d .git ]; then
  git init -q
  echo "  repositório git criado"
fi

git config user.name >/dev/null 2>&1 || git config user.name "$USUARIO"
if ! git config user.email >/dev/null 2>&1; then
  printf "      Seu e-mail do GitHub: "
  read -r EMAIL
  git config user.email "$EMAIL"
fi

git add -A

if git diff --cached --quiet 2>/dev/null; then
  echo "  nada novo para enviar"
else
  printf "      Mensagem do commit (Enter para 'atualização'): "
  read -r MSG
  [ -z "$MSG" ] && MSG="atualização"
  git commit -q -m "$MSG"
  echo "  ✓ commit criado"
fi

git branch -M main 2>/dev/null

# ---------- 7. Token e push ----------
echo ""
echo "[7/7] Autenticação"
echo ""
echo "Cole abaixo seu Personal Access Token do GitHub."
echo "(começa com ghp_ — se não tiver, gere em:"
echo " https://github.com/settings/tokens → Generate new token (classic)"
echo " → marque a caixa 'repo' → Generate token)"
echo ""
echo "Nada vai aparecer na tela enquanto você cola. É normal."
echo ""
printf "Token: "
read -rs TOKEN
echo ""

if [ -z "$TOKEN" ]; then
  echo "✗ Token vazio."
  echo ""
  read -r
  exit 1
fi

echo ""
echo "Verificando o token..."
CODIGO=$(curl -s -o /dev/null -w "%{http_code}" \
  -H "Authorization: token $TOKEN" \
  "https://api.github.com/repos/$REPO")

case "$CODIGO" in
  200)
    echo "✓ Acesso ao repositório confirmado"
    ;;
  404)
    echo "✗ Repositório '$REPO' não encontrado."
    echo "  Crie em https://github.com/new (vazio, sem README)"
    echo "  ou confira se o nome está certo."
    echo ""
    read -r
    exit 1
    ;;
  401)
    echo "✗ Token inválido ou expirado."
    echo ""
    read -r
    exit 1
    ;;
  *)
    echo "✗ GitHub respondeu $CODIGO. Confira token e repositório."
    echo ""
    read -r
    exit 1
    ;;
esac

git remote remove origin 2>/dev/null
git remote add origin "https://${USUARIO}:${TOKEN}@github.com/${REPO}.git"

echo ""
echo "Enviando..."
if git push -f origin main 2>&1 | grep -v "^remote:" ; then
  echo ""
  echo "============================================================"
  echo "  PRONTO"
  echo "============================================================"
  echo ""
  echo "Confira em: https://github.com/$REPO"
else
  echo ""
  echo "✗ O envio falhou. Manda print desta janela."
fi

# O token fica embutido na URL do remote. Removê-lo evita que ele
# fique legível em .git/config na sua máquina.
git remote set-url origin "https://github.com/${REPO}.git" 2>/dev/null

echo ""
echo "Aperte Enter para fechar."
read -r
