"""
Foto de produto da demonstração da marca d'água (28/10/2026).

Renderiza, por código e sem serviço de fora, uma cena de estúdio com um frasco
de sérum e um pote de creme de uma marca inventada ("órbita", o mesmo nome da
conta de demonstração usada nas capturas do painel). A imagem é nossa: não vem
de banco de imagens nem de IA.

Precisa de: pip install mitsuba numpy pillow fonttools brotli
Uso:        python3 ferramentas/produto.py SAIDA.png [largura altura amostras]
            (padrão 1800 x 1200, 384 amostras; demora alguns minutos)
"""
import os
import sys
import math
import tempfile

import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter

import mitsuba as mi

mi.set_variant("llvm_ad_rgb")

AQUI = os.path.dirname(os.path.abspath(__file__))
FONTE_WOFF2 = os.path.join(AQUI, "..", "public", "assets", "fonts", "inter.woff2")
TMP = tempfile.mkdtemp(prefix="produto-")


def fonte(tamanho, peso=400):
    ttf = os.path.join(TMP, "inter.ttf")
    if not os.path.exists(ttf):
        from fontTools.ttLib import TTFont

        f = TTFont(FONTE_WOFF2)
        f.flavor = None
        f.save(ttf)
    ft = ImageFont.truetype(ttf, tamanho)
    try:
        ft.set_variation_by_axes([peso])
    except Exception:
        pass
    return ft


# ---------- malhas por revolução (torno) ----------
def torno(nome, perfil, segmentos=160, t0=0.0, t1=2 * math.pi, fechar=True):
    """perfil: lista de (raio, altura) de baixo para cima. Grava um PLY com UV."""
    perfil = np.asarray(perfil, dtype=float)
    n = len(perfil)
    comp = np.concatenate([[0], np.cumsum(np.hypot(np.diff(perfil[:, 0]), np.diff(perfil[:, 1])))])
    v_coord = comp / comp[-1] if comp[-1] > 0 else np.linspace(0, 1, n)
    volta = abs((t1 - t0) - 2 * math.pi) < 1e-9
    cols = segmentos if volta else segmentos + 1
    verts, uvs = [], []
    for j in range(cols):
        u = j / segmentos
        t = t0 + (t1 - t0) * u
        c, s = math.cos(t), math.sin(t)
        for i, (r, y) in enumerate(perfil):
            verts.append((r * c, y, r * s))
            uvs.append((u, v_coord[i]))
    faces = []
    for j in range(segmentos):
        j2 = (j + 1) % cols
        for i in range(n - 1):
            a, b = j * n + i, j * n + i + 1
            c_, d = j2 * n + i, j2 * n + i + 1
            faces += [(a, b, c_), (b, d, c_)]
    caminho = os.path.join(TMP, nome + ".ply")
    with open(caminho, "w") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(verts)}\nproperty float x\nproperty float y\nproperty float z\n")
        f.write("property float u\nproperty float v\n")
        f.write(f"element face {len(faces)}\nproperty list uchar int vertex_indices\nend_header\n")
        for (x, y, z), (u, v) in zip(verts, uvs):
            f.write(f"{x:.6f} {y:.6f} {z:.6f} {u:.6f} {v:.6f}\n")
        for a, b, c_ in faces:
            f.write(f"3 {a} {b} {c_}\n")
    return caminho


def fundo_infinito(nome, y0=-2.6, raio=34.0, recuo=-58.0, largura=260.0):
    """Fundo de estúdio sem emenda: chão que sobe em curva até a parede."""
    perfil = [(160.0, y0), (recuo + raio, y0)]
    for k in range(1, 25):
        a = -math.pi / 2 - (math.pi / 2) * k / 24
        perfil.append((recuo + raio + raio * math.cos(a), y0 + raio + raio * math.sin(a)))
    perfil.append((recuo, y0 + 220.0))
    verts, faces = [], []
    for x in (-largura / 2, largura / 2):
        for z, y in perfil:
            verts.append((x, y, z))
    n = len(perfil)
    for i in range(n - 1):
        a, b, c_, d = i, i + 1, n + i, n + i + 1
        faces += [(a, c_, b), (b, c_, d)]
    caminho = os.path.join(TMP, nome + ".ply")
    with open(caminho, "w") as f:
        f.write("ply\nformat ascii 1.0\n")
        f.write(f"element vertex {len(verts)}\nproperty float x\nproperty float y\nproperty float z\n")
        f.write(f"element face {len(faces)}\nproperty list uchar int vertex_indices\nend_header\n")
        for x, y, z in verts:
            f.write(f"{x:.4f} {y:.4f} {z:.4f}\n")
        for a, b, c_ in faces:
            f.write(f"3 {a} {b} {c_}\n")
    return caminho


def arredondado(r, y0, y1, raio_canto, passos=10, topo=True, base=True):
    """Perfil de um cilindro com cantos arredondados (fechado em cima e embaixo)."""
    p = [(0.0, y0)]
    if base:
        for k in range(passos + 1):
            a = -math.pi / 2 + (math.pi / 2) * k / passos
            p.append((r - raio_canto + raio_canto * math.cos(a), y0 + raio_canto + raio_canto * math.sin(a)))
    else:
        p.append((r, y0))
    if topo:
        for k in range(passos + 1):
            a = (math.pi / 2) * k / passos
            p.append((r - raio_canto + raio_canto * math.cos(a), y1 - raio_canto + raio_canto * math.sin(a)))
    else:
        p.append((r, y1))
    p.append((0.0, y1))
    return p


# ---------- texturas ----------
def rotulo_frasco(caminho):
    W, H = 2048, 820
    im = Image.new("RGB", (W, H), (236, 229, 216))
    d = ImageDraw.Draw(im)
    # papel com leve textura
    ruido = (np.random.default_rng(3).normal(0, 3.2, (H, W, 1)) * np.ones(3)).astype(np.int16)
    arr = np.clip(np.asarray(im).astype(np.int16) + ruido, 0, 255).astype(np.uint8)
    im = Image.fromarray(arr)
    d = ImageDraw.Draw(im)
    cx = W // 2
    tinta = (44, 30, 58)
    # marca: anel inclinado + nome
    d.ellipse((cx - 70, 120, cx + 70, 260), outline=tinta, width=9)
    d.ellipse((cx - 150, 170, cx + 150, 214), outline=(125, 60, 190), width=7)
    f1 = fonte(150, 650)
    t = "órbita"
    w = d.textlength(t, font=f1)
    d.text((cx - w / 2, 300), t, font=f1, fill=tinta)
    f2 = fonte(54, 500)
    for i, (txt, y) in enumerate([("SÉRUM FACIAL", 510), ("vitamina C 10%", 590)]):
        ff = f2 if i == 0 else fonte(50, 400)
        w = d.textlength(txt, font=ff)
        d.text((cx - w / 2, y), txt, font=ff, fill=tinta if i == 0 else (90, 78, 104))
    f3 = fonte(44, 500)
    w = d.textlength("30 ml", font=f3)
    d.text((cx - w / 2, 700), "30 ml", font=f3, fill=(90, 78, 104))
    d.line((cx - 260, 480, cx + 260, 480), fill=(180, 168, 150), width=3)
    im.rotate(180).save(caminho)


def rotulo_pote(caminho):
    W, H = 2048, 300
    im = Image.new("RGB", (W, H), (233, 226, 214))
    d = ImageDraw.Draw(im)
    tinta = (44, 30, 58)
    f1 = fonte(120, 650)
    w = d.textlength("órbita", font=f1)
    d.text((W / 2 - w / 2, 40), "órbita", font=f1, fill=tinta)
    f2 = fonte(44, 500)
    w = d.textlength("CREME HIDRATANTE · 50 g", font=f2)
    d.text((W / 2 - w / 2, 205), "CREME HIDRATANTE · 50 g", font=f2, fill=(90, 78, 104))
    im.rotate(180).save(caminho)


def pedra(caminho):
    """Textura de travertino claro para o pedestal."""
    rng = np.random.default_rng(11)
    W, H = 1024, 512
    base = np.zeros((H, W))
    for esc, peso in [(4, 0.5), (16, 0.3), (64, 0.2)]:
        g = rng.random((H // esc + 2, W // esc + 2))
        g = np.asarray(Image.fromarray((g * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC)) / 255.0
        base += g * peso
    veios = np.sin(np.linspace(0, 40, H)[:, None] + base * 6) * 0.5 + 0.5
    v = 0.86 + (base - 0.5) * 0.08 - (veios ** 12) * 0.08
    cor = np.stack([v * 229, v * 216, v * 199], -1)
    poros = rng.random((H, W)) > 0.996
    cor[poros] *= 0.82
    Image.fromarray(np.clip(cor, 0, 255).astype(np.uint8)).filter(ImageFilter.GaussianBlur(0.6)).save(caminho)


def cena(largura, altura, amostras):
    tex_rot = os.path.join(TMP, "rotulo.png")
    tex_pote = os.path.join(TMP, "pote.png")
    tex_pedra = os.path.join(TMP, "pedra.png")
    rotulo_frasco(tex_rot)
    rotulo_pote(tex_pote)
    pedra(tex_pedra)

    # unidades em cm. Pedestal em y=0..3, produtos em cima.
    pedestal = torno("pedestal", arredondado(9.5, 0.0, 3.0, 0.35, 8), 200)
    pedestal2 = torno("pedestal2", arredondado(13.5, -2.6, 0.02, 0.3, 8), 200)

    # frasco conta-gotas (vidro âmbar), x = -2.2
    Y = 3.0
    corpo = [(0.0, Y)]
    for k in range(9):
        a = -math.pi / 2 + (math.pi / 2) * k / 8
        corpo.append((2.25 - 0.45 + 0.45 * math.cos(a), Y + 0.45 + 0.45 * math.sin(a)))
    corpo += [(2.25, Y + 6.4)]
    for k in range(1, 13):
        a = (math.pi / 2) * k / 12
        corpo.append((0.75 + 1.5 * math.cos(a), Y + 6.4 + 1.25 * math.sin(a)))
    corpo += [(0.72, Y + 7.65), (0.72, Y + 8.1), (0.0, Y + 8.1)]
    frasco = torno("frasco", corpo, 200)
    rotulo = torno("rotulo", [(2.272, Y + 1.35), (2.272, Y + 5.55)], 160, t0=math.pi / 2 - 1.25, t1=math.pi / 2 + 1.25)
    colar = torno("colar", arredondado(0.98, Y + 7.9, Y + 9.5, 0.12, 6), 160)
    bulbo_p = [(0.0, Y + 9.45), (0.7, Y + 9.45), (0.72, Y + 10.2)]
    for k in range(1, 17):
        a = (math.pi / 2) * k / 16
        bulbo_p.append((0.72 * math.cos(a), Y + 10.2 + 1.55 * math.sin(a)))
    bulbo = torno("bulbo", bulbo_p, 160)

    # pote de creme (vidro branco leitoso, tampa dourada), atrás à direita
    pote = torno("pote", arredondado(3.0, Y, Y + 3.0, 0.5, 8), 200)
    pote_rot = torno("pote_rot", [(3.01, Y + 0.7), (3.01, Y + 2.3)], 160, t0=math.pi / 2 - 1.1, t1=math.pi / 2 + 1.1)
    tampa = torno("tampa", arredondado(3.05, Y + 3.0, Y + 4.25, 0.3, 8), 200)

    def malha(arq, bsdf, x=0.0, z=0.0, ry=0.0):
        return {
            "type": "ply",
            "filename": arq,
            "to_world": mi.ScalarTransform4f().translate([x, 0, z]).rotate([0, 1, 0], ry),
            "bsdf": bsdf,
        }

    vidro_ambar = {"type": "dielectric", "int_ior": 1.5, "specular_transmittance": {"type": "rgb", "value": [0.78, 0.38, 0.12]}}
    preto = {"type": "roughplastic", "distribution": "ggx", "alpha": 0.32, "diffuse_reflectance": {"type": "rgb", "value": [0.025, 0.022, 0.03]}}
    borracha = {"type": "roughplastic", "distribution": "ggx", "alpha": 0.55, "diffuse_reflectance": {"type": "rgb", "value": [0.03, 0.028, 0.034]}}
    papel = lambda tex: {"type": "twosided", "bsdf": {"type": "roughplastic", "alpha": 0.6, "diffuse_reflectance": {"type": "bitmap", "filename": tex}}}
    leitoso = {"type": "roughplastic", "distribution": "ggx", "alpha": 0.12, "int_ior": 1.5, "diffuse_reflectance": {"type": "rgb", "value": [0.86, 0.84, 0.86]}}
    ouro = {"type": "roughconductor", "material": "Au", "alpha": 0.18}
    travertino = {"type": "roughplastic", "alpha": 0.5, "diffuse_reflectance": {"type": "bitmap", "filename": tex_pedra}}
    fundo = {"type": "diffuse", "reflectance": {"type": "rgb", "value": [0.66, 0.58, 0.64]}}

    xf, zf = -2.6, 1.6
    xp, zp = 4.4, -2.2
    cena = {
        "type": "scene",
        "integrator": {"type": "path", "max_depth": 14},
        "sensor": {
            "type": "perspective",
            "fov": 26,
            "to_world": mi.ScalarTransform4f().look_at(origin=[2.0, 16.0, 62], target=[0.8, 6.2, 0], up=[0, 1, 0]),
            "film": {"type": "hdrfilm", "width": largura, "height": altura, "rfilter": {"type": "gaussian"}},
            "sampler": {"type": "independent", "sample_count": amostras},
        },
        # luz de estúdio: caixa grande à esquerda, recorte atrás à direita, preenchimento frontal
        "luz_caixa": {
            "type": "rectangle",
            "to_world": mi.ScalarTransform4f().look_at(origin=[-30, 22, 18], target=[0, 6, 0], up=[0, 1, 0]).scale([9, 12, 1]),
            "emitter": {"type": "area", "radiance": {"type": "rgb", "value": [7.2, 6.8, 6.4]}},
        },
        "luz_recorte": {
            "type": "rectangle",
            "to_world": mi.ScalarTransform4f().look_at(origin=[30, 14, -14], target=[0, 7, 0], up=[0, 1, 0]).scale([4, 9, 1]),
            "emitter": {"type": "area", "radiance": {"type": "rgb", "value": [9.0, 7.6, 10.5]}},
        },
        "luz_frente": {
            "type": "rectangle",
            "to_world": mi.ScalarTransform4f().look_at(origin=[8, 30, 60], target=[0, 5, 0], up=[0, 1, 0]).scale([14, 6, 1]),
            "emitter": {"type": "area", "radiance": {"type": "rgb", "value": [1.1, 1.05, 1.1]}},
        },
        "ambiente": {"type": "constant", "radiance": {"type": "rgb", "value": [0.05, 0.045, 0.06]}},
        # fundo infinito (chão + parede curva)
        "fundo": {"type": "ply", "filename": fundo_infinito("fundo"), "bsdf": {"type": "twosided", "bsdf": fundo}},
        "pedestal": malha(pedestal, travertino),
        "pedestal2": malha(pedestal2, travertino, ry=40),
        "frasco": malha(frasco, vidro_ambar, xf, zf),
        "rotulo": malha(rotulo, papel(tex_rot), xf, zf, ry=-8),
        "colar": malha(colar, preto, xf, zf),
        "bulbo": malha(bulbo, borracha, xf, zf),
        "pote": malha(pote, leitoso, xp, zp),
        "pote_rot": malha(pote_rot, papel(tex_pote), xp, zp, ry=-14),
        "tampa": malha(tampa, ouro, xp, zp),
    }
    return mi.load_dict(cena)


def revelar(hdr, saida):
    """Converte o HDR em sRGB com curva suave e leve vinheta."""
    a = np.asarray(hdr, dtype=np.float32)[..., :3]
    a = a * 1.05
    a = a / (1.0 + a * 0.18)  # ombro suave
    a = np.where(a <= 0.0031308, 12.92 * a, 1.055 * np.power(np.clip(a, 0, None), 1 / 2.4) - 0.055)
    h, w = a.shape[:2]
    yy, xx = np.mgrid[0:h, 0:w]
    vin = 1 - 0.18 * (((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2) / 2
    a = a * vin[..., None]
    Image.fromarray((np.clip(a, 0, 1) * 255 + 0.5).astype(np.uint8)).save(saida)


if __name__ == "__main__":
    saida = sys.argv[1]
    largura = int(sys.argv[2]) if len(sys.argv) > 2 else 1800
    altura = int(sys.argv[3]) if len(sys.argv) > 3 else 1200
    amostras = int(sys.argv[4]) if len(sys.argv) > 4 else 384
    sc = cena(largura, altura, amostras)
    img = mi.render(sc)
    revelar(img, saida)
    print("ok", saida)
