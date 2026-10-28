"""
Gera o antes/depois da seção Marca d'água (28/10/2026) a partir da MESMA foto
(saída de ferramentas/produto.py). Só muda a marca aplicada:
  - logo PNG de uma loja fictícia no canto inferior direito (opacidade 80%);
  - texto "@sualoja" no canto inferior esquerdo, com contorno.
Reproduz as opções da ferramenta (posição, tamanho em % da largura, opacidade,
margem, cor e contorno). Não é a função da plataforma: é uma ilustração.
Uso: python3 ferramentas/marca_produto.py FOTO.png PASTA_ASSETS
"""
import os, sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
from fontTools.ttLib import TTFont

AQUI = os.path.dirname(os.path.abspath(__file__))
foto, pasta = sys.argv[1], sys.argv[2]
ttf = "/tmp/inter-marca.ttf"
f = TTFont(os.path.join(AQUI, "..", "public", "assets", "fonts", "inter.woff2")); f.flavor = None; f.save(ttf)

def fonte(t, peso):
    ft = ImageFont.truetype(ttf, t)
    try: ft.set_variation_by_axes([peso])
    except Exception: pass
    return ft

base = Image.open(foto).convert("RGB").resize((1200, 800), Image.LANCZOS)
W, H = base.size

def logo_loja(largura):
    """Logo fictícia: anel inclinado + 'órbita' + 'ESTÚDIO', branca, fundo transparente."""
    esc = 4
    L, A = largura * esc, int(largura * 0.36) * esc
    im = Image.new("RGBA", (L, A), (0, 0, 0, 0))
    d = ImageDraw.Draw(im)
    r = A * 0.30; cx, cy = A * 0.42, A * 0.5
    d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=(255, 255, 255, 255), width=int(A * 0.055))
    d.ellipse((cx - r * 1.75, cy - r * 0.42, cx + r * 1.75, cy + r * 0.42), outline=(255, 255, 255, 255), width=int(A * 0.045))
    ft = fonte(int(A * 0.5), 700)
    d.text((A * 1.02, A * 0.06), "órbita", font=ft, fill=(255, 255, 255, 255))
    ft2 = fonte(int(A * 0.17), 600)
    d.text((A * 1.06, A * 0.68), "E S T Ú D I O", font=ft2, fill=(255, 255, 255, 255))
    return im.resize((largura, A // esc), Image.LANCZOS)

def aplicar(img, marca, x, y, opacidade, contorno=0):
    img = img.convert("RGBA")
    if contorno:
        alfa = marca.split()[3].filter(ImageFilter.MaxFilter(contorno * 2 + 1)).filter(ImageFilter.GaussianBlur(1))
        sombra = Image.new("RGBA", marca.size, (20, 12, 30, 0)); sombra.putalpha(alfa.point(lambda v: int(v * 0.55)))
        camada = Image.new("RGBA", img.size, (0, 0, 0, 0)); camada.paste(sombra, (x, y), sombra)
        camada.putalpha(camada.split()[3].point(lambda v: int(v * opacidade)))
        img = Image.alpha_composite(img, camada)
    m = marca.copy(); m.putalpha(m.split()[3].point(lambda v: int(v * opacidade)))
    camada = Image.new("RGBA", img.size, (0, 0, 0, 0)); camada.paste(m, (x, y), m)
    return Image.alpha_composite(img, camada).convert("RGB")

margem = int(W * 0.035)
# logo: 22% da largura, canto inferior direito, opacidade 80%
lg = logo_loja(int(W * 0.22))
com_logo = aplicar(base, lg, W - lg.width - margem, H - lg.height - margem, 0.8, contorno=2)
# texto: 4% de altura, canto inferior esquerdo, opacidade 85%, branco com contorno
ft = fonte(int(W * 0.036), 700)
caixa = ImageDraw.Draw(Image.new("RGBA", (1, 1))).textbbox((0, 0), "@sualoja", font=ft)
tx = Image.new("RGBA", (caixa[2] + 8, caixa[3] + 8), (0, 0, 0, 0))
ImageDraw.Draw(tx).text((4, 4), "@sualoja", font=ft, fill=(255, 255, 255, 255))
com_texto = aplicar(base, tx, margem, H - tx.height - margem, 0.85, contorno=3)

for nome, im in [("antes", base), ("logo", com_logo), ("texto", com_texto)]:
    for w in (1200, 720):
        out = im if w == 1200 else im.resize((720, 480), Image.LANCZOS)
        out.save(os.path.join(pasta, f"marca-produto-{nome}-{w}.webp"), quality=80, method=6)
print("ok")
