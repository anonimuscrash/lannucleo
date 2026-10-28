"""Arte espacial da land da Núcleo, renderizada aqui (sem serviço de fora).

Gera camadas separadas para montar no HTML:
  ceu      - céu com nebulosa e estrelas (fundo do topo)
  planeta  - planeta facetado com anéis, fundo transparente
  rochas   - chão rochoso transparente (frente do topo)
  pedras   - asteroides soltos, transparentes
  palco    - palco rochoso para os prêmios
  borda    - borda de planeta (fundo do Checkout)
  orbes    - ícones redondos pequenos da faixa de destaques
Uso: python3 arte.py <pasta-de-saida> [partes...]
"""
import sys, os, math
import numpy as np
from PIL import Image
from scipy.ndimage import gaussian_filter

RNG = np.random.default_rng(27102026)
ROXO = np.array([0.56, 0.0, 1.0])
MAGENTA = np.array([1.0, 0.18, 0.72])
AZUL = np.array([0.22, 0.62, 1.0])
VIOLETA = np.array([0.62, 0.36, 1.0])


# ---------- ruído ----------
def _h3(ix, iy, iz):
    n = np.sin(ix * 127.1 + iy * 311.7 + iz * 74.7) * 43758.5453
    return n - np.floor(n)

def ruido3(x, y, z):
    ix, iy, iz = np.floor(x), np.floor(y), np.floor(z)
    fx, fy, fz = x - ix, y - iy, z - iz
    ux, uy, uz = fx * fx * (3 - 2 * fx), fy * fy * (3 - 2 * fy), fz * fz * (3 - 2 * fz)
    def h(a, b, c): return _h3(ix + a, iy + b, iz + c)
    x00 = h(0,0,0) * (1-ux) + h(1,0,0) * ux
    x10 = h(0,1,0) * (1-ux) + h(1,1,0) * ux
    x01 = h(0,0,1) * (1-ux) + h(1,0,1) * ux
    x11 = h(0,1,1) * (1-ux) + h(1,1,1) * ux
    y0 = x00 * (1-uy) + x10 * uy
    y1 = x01 * (1-uy) + x11 * uy
    return y0 * (1-uz) + y1 * uz

def fbm3(x, y, z, oit=5, lac=2.03, ganho=0.5):
    s, a, f = 0.0, 0.5, 1.0
    for i in range(oit):
        s = s + a * ruido3(x * f + i * 17.3, y * f - i * 9.1, z * f + i * 3.7)
        f *= lac; a *= ganho
    return s

def fbm2(w, h, escala, oit=6, sem=0.0):
    yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
    return fbm3(xx / escala, yy / escala, np.full_like(xx, sem), oit)


def salvar(arr, caminho, alfa=None):
    arr = np.clip(arr + (RNG.random(arr.shape) - RNG.random(arr.shape)) / 255.0, 0, 1)
    if alfa is not None:
        a = np.clip(alfa, 0, 1)
        img = np.dstack([arr, a])
        Image.fromarray((img * 255 + 0.5).astype(np.uint8), "RGBA").save(caminho)
    else:
        Image.fromarray((arr * 255 + 0.5).astype(np.uint8), "RGB").save(caminho)
    print("ok", caminho)


def tom(x):
    """Compressão suave das luzes (evita estourar)."""
    return 1 - np.exp(-np.maximum(x, 0) * 1.15)


# ---------- estrelas e nebulosa ----------
def estrelas(w, h, n, brilho=1.0, grandes=0):
    buf = np.zeros((h, w, 3))
    xs = RNG.uniform(0, w, n); ys = RNG.uniform(0, h, n)
    b = RNG.power(0.35, n) * brilho
    cores = np.where(RNG.random((n, 1)) < 0.25, np.array([0.8, 0.75, 1.0]), np.array([1.0, 1.0, 1.0]))
    cores = np.where(RNG.random((n, 1)) < 0.08, np.array([1.0, 0.8, 0.95]), cores)
    for x, y, bb, c in zip(xs, ys, b, cores):
        ix, iy = int(x), int(y)
        fx, fy = x - ix, y - iy
        for dx, dy, wgt in ((0, 0, (1-fx)*(1-fy)), (1, 0, fx*(1-fy)), (0, 1, (1-fx)*fy), (1, 1, fx*fy)):
            if 0 <= ix+dx < w and 0 <= iy+dy < h:
                buf[iy+dy, ix+dx] += c * bb * wgt
    if grandes:
        g = np.zeros((h, w, 3))
        for _ in range(grandes):
            x, y = int(RNG.uniform(0, w)), int(RNG.uniform(0, h))
            c = [np.array([0.85, 0.8, 1.0]), np.array([1.0, 0.85, 1.0]), np.array([0.8, 0.9, 1.0])][RNG.integers(0, 3)]
            g[y, x] += c * RNG.uniform(6, 16)
        glow = gaussian_filter(g, (1.2, 1.2, 0)) + gaussian_filter(g, (5, 5, 0)) * 0.6
        buf += glow
    return buf


def nebulosa(w, h, cor_a, cor_b, centro=(0.75, 0.25), raio=0.75, forca=1.0, sem=1.0):
    n1 = fbm2(w, h, w / 3.2, 6, sem)
    n2 = fbm2(w, h, w / 7.0, 5, sem + 5)
    yy, xx = np.mgrid[0:h, 0:w]
    d = np.sqrt(((xx / w - centro[0]) * 1.0) ** 2 + ((yy / h - centro[1]) * h / w * 1.6) ** 2)
    masc = np.clip(1 - d / raio, 0, 1) ** 1.6
    dens = np.clip((n1 - 0.38) * 2.2, 0, 1) ** 1.5 * masc
    fil = np.clip((n2 - 0.5) * 3, 0, 1) ** 2 * masc
    mix = np.clip(n2, 0, 1)[..., None]
    cor = cor_a * (1 - mix) + cor_b * mix
    return (dens[..., None] * 0.55 + fil[..., None] * 0.35) * cor * forca


# ---------- planeta ----------
def pontos_esfera(n):
    i = np.arange(n) + 0.5
    phi = np.arccos(1 - 2 * i / n)
    th = math.pi * (1 + 5 ** 0.5) * i
    p = np.stack([np.cos(th) * np.sin(phi), np.sin(th) * np.sin(phi), np.cos(phi)], -1)
    p += RNG.normal(0, 0.035, p.shape)
    return p / np.linalg.norm(p, axis=1, keepdims=True)


def rot(ax, ay, az):
    cx, sx, cy, sy, cz, sz = math.cos(ax), math.sin(ax), math.cos(ay), math.sin(ay), math.cos(az), math.sin(az)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def planeta(S=1600, R=None, aneis=True, facetas=760, brilho_borda=1.0, giro=(0.4, -0.5, 0.2),
            luz_cor=VIOLETA, borda_cor=None, halo=1.0, aneis_cfg=None):
    R = R or S * 0.235
    c = S / 2
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float64)
    X = (xx + 0.5 - c) / R; Y = (yy + 0.5 - c) / R
    r2 = X * X + Y * Y
    dentro = r2 < 1.0
    Z = np.sqrt(np.clip(1 - r2, 0, 1))
    # borda antisserrilhada
    dist_borda = (1 - np.sqrt(r2)) * R
    cobre = np.clip(dist_borda + 0.5, 0, 1)

    idx = np.nonzero(r2 < 1.02)
    nx, ny, nz = X[idx], -Y[idx], Z[idx]
    N = np.stack([nx, ny, nz], -1)
    M = rot(*giro)
    P = N @ M.T  # coordenadas na superfície (giradas)

    # facetas (Voronoi na esfera): cada célula vira um plano
    pts = pontos_esfera(facetas)
    melhor = np.full(len(P), -2.0); seg = np.full(len(P), -2.0); qual = np.zeros(len(P), int)
    for k in range(0, len(pts), 64):
        d = P @ pts[k:k+64].T
        for j in range(d.shape[1]):
            v = d[:, j]
            m1 = v > melhor
            seg = np.where(m1, melhor, np.maximum(seg, v))
            qual = np.where(m1, k + j, qual)
            melhor = np.where(m1, v, melhor)
    aresta = np.clip((melhor - seg) * 160, 0, 1)  # 0 na aresta
    cel = pts[qual] @ M  # direção da faceta no espaço da câmera
    tilt = 0.38
    Nf = N * (1 - tilt) + cel * tilt
    Nf /= np.linalg.norm(Nf, axis=1, keepdims=True)

    rugo = fbm3(P[:, 0] * 3, P[:, 1] * 3, P[:, 2] * 3, 5)
    rugo2 = fbm3(P[:, 0] * 11, P[:, 1] * 11, P[:, 2] * 11, 3)
    var_cel = _h3(qual * 1.0, qual * 0.37, 3.0)

    base = np.array([0.016, 0.010, 0.028]) + np.array([0.022, 0.012, 0.045]) * np.clip(rugo[:, None] - 0.35, 0, 1) + 0.014 * var_cel[:, None] * np.array([0.6, 0.4, 1.0])
    # luz de preenchimento (frente-esquerda, fraca) e luz principal (atrás-direita, roxa)
    L1 = np.array([-0.6, 0.55, 0.45]); L1 /= np.linalg.norm(L1)
    L2 = np.array([0.75, 0.35, -0.55]); L2 /= np.linalg.norm(L2)
    d1 = np.clip(Nf @ L1, 0, 1)
    d2 = np.clip(Nf @ L2, 0, 1)
    V = np.array([0, 0, 1.0])
    H1 = (L1 + V); H1 /= np.linalg.norm(H1)
    spec = np.clip(Nf @ H1, 0, 1) ** 60 * (0.3 + 0.7 * var_cel)
    fres = (1 - np.clip(nz, 0, 1)) ** 2.6
    cor = base * (0.4 + 0.8 * d1[:, None]) + luz_cor * 0.13 * d1[:, None] ** 3 * (0.4 + var_cel[:, None])
    cor += np.array([0.75, 0.55, 1.0]) * spec[:, None] * 0.35
    cor += MAGENTA * 0.7 * d2[:, None] ** 2 * fres[:, None] ** 0.6 + ROXO * 0.5 * d2[:, None] ** 3
    bc = borda_cor if borda_cor is not None else ROXO * 0.7 + AZUL * 0.3
    cor += bc * fres[:, None] ** 1.4 * 1.2 * brilho_borda
    # veias nas arestas das facetas, mais vivas perto da borda iluminada
    veia = (1 - aresta) ** 2 * (0.08 + 0.92 * np.clip(d2 * 1.6 + fres ** 1.5, 0, 1)) * (0.4 + rugo2)
    cor += np.array([0.55, 0.3, 1.0]) * veia[:, None] * 0.28

    img = np.zeros((S, S, 3))
    img[idx] = cor
    alfa = np.zeros((S, S)); alfa[idx] = 1.0
    alfa *= cobre; img *= cobre[..., None]

    # halo (atmosfera) fora do disco
    rr = np.sqrt(r2)
    fora = np.clip(rr - 1, 0, None)
    ang = np.arctan2(-Y, X)
    lado = 0.3 + 0.7 * (np.cos(ang - 0.5) * 0.5 + 0.5) ** 1.5  # mais forte à direita/cima
    halo_v = (np.exp(-fora * 9) * 0.9 + np.exp(-fora * 2.4) * 0.35) * lado * halo
    halo_v *= (rr >= 0.985)
    glow = halo_v[..., None] * (ROXO * 0.7 + MAGENTA * 0.25 + AZUL * 0.15)

    frente = np.zeros((S, S, 3)); tras = np.zeros((S, S, 3))
    if aneis:
        cfg = aneis_cfg or [
            dict(r=1.62, incl=-1.32, rotz=0.6, cor=(MAGENTA, ROXO), larg=3.0, forca=1.45),
            dict(r=1.78, incl=-1.35, rotz=0.57, cor=(ROXO, AZUL), larg=2.0, forca=1.1),
            dict(r=1.48, incl=-1.29, rotz=0.63, cor=(AZUL, VIOLETA), larg=1.5, forca=0.8),
        ]
        for a in cfg:
            f, t = anel(S, R, **a)
            frente += f; tras += t
    # tudo junto: atrás do planeta (halo + anéis de trás), planeta, anéis da frente
    emis_tras = glow + tras
    rgb = img + emis_tras * (1 - alfa[..., None]) + frente
    lum_emis = np.max(emis_tras * (1 - alfa[..., None]) + frente, axis=2)
    a_tot = np.clip(alfa + np.clip(lum_emis, 0, 1) * (1 - alfa), 0, 1)
    q = np.clip((0.5 - np.hypot(xx / S - 0.5, yy / S - 0.5)) / 0.06, 0, 1) ** 1.5
    a_tot = a_tot * np.maximum(q, alfa)
    rgb = tom(rgb * 1.25)
    cor_final = np.where(a_tot[..., None] > 1e-4, rgb / np.maximum(a_tot[..., None], 1e-4), 0)
    return np.clip(cor_final, 0, 1), a_tot


def anel(S, R, r=1.5, incl=1.2, rotz=-0.6, cor=(MAGENTA, ROXO), larg=2.0, forca=1.0, n=26000):
    th = np.linspace(0, 2 * math.pi, n, endpoint=False)
    p = np.stack([np.cos(th) * r, np.sin(th) * r, np.zeros_like(th)], -1)
    M = rot(incl, 0, 0)
    M = rot(0, 0, rotz) @ M
    q = p @ M.T
    x = S / 2 + q[:, 0] * R; y = S / 2 - q[:, 1] * R; z = q[:, 2]
    dentro_disco = (q[:, 0] ** 2 + q[:, 1] ** 2) < 1.0
    atras = (z < 0) & dentro_disco
    esc = np.where(z >= 0, 1.0, 0.55)
    mistura = (np.sin(th + 0.9) * 0.5 + 0.5)[:, None]
    cores = cor[0] * (1 - mistura) + cor[1] * mistura
    brilho = (0.45 + 0.55 * (np.cos(th - 2.2) * 0.5 + 0.5) ** 1.5) * esc * forca
    frente = np.zeros((S, S, 3)); tras = np.zeros((S, S, 3))
    for alvo, m in ((frente, z >= 0), (tras, (z < 0) & ~atras)):
        xs, ys, cs, bs = x[m], y[m], cores[m], brilho[m]
        ix = xs.astype(int); iy = ys.astype(int)
        ok = (ix >= 0) & (ix < S - 1) & (iy >= 0) & (iy < S - 1)
        ix, iy, cs, bs, fx, fy = ix[ok], iy[ok], cs[ok], bs[ok], (xs - ix)[ok], (ys - iy)[ok]
        for dx, dy, wgt in ((0, 0, (1-fx)*(1-fy)), (1, 0, fx*(1-fy)), (0, 1, (1-fx)*fy), (1, 1, fx*fy)):
            np.add.at(alvo, (iy + dy, ix + dx), cs * (bs * wgt)[:, None])
    passo = 2 * math.pi * r * R / n  # px por amostra
    out = []
    for alvo in (frente, tras):
        alvo *= passo
        nuc = gaussian_filter(alvo, (larg * 0.45, larg * 0.45, 0)) * 2.2
        g1 = gaussian_filter(alvo, (larg * 2.5, larg * 2.5, 0)) * 2.4
        g2 = gaussian_filter(alvo, (larg * 9, larg * 9, 0)) * 2.0
        out.append(nuc + g1 + g2)
    return out[0], out[1]


# ---------- rochas ----------
def silhueta(w, escala, oit=6, sem=0.0):
    x = np.arange(w) / escala
    return fbm3(x, np.full_like(x, sem), np.full_like(x, sem * 0.3), oit)


def _relevo(w, h, escala, sem, oit=6):
    n = fbm2(w, h, escala, oit, sem)
    return 1 - np.abs(2 * n - 1)  # cristas


def chao(w, h, alto=0.55, sem=2.0, plano=False):
    """Chão rochoso em camadas (longe → perto), com relevo iluminado; transparente acima."""
    rgb = np.zeros((h, w, 3)); alfa = np.zeros((h, w))
    yy = np.arange(h)[:, None].astype(np.float64)
    xs = np.linspace(-1, 1, w)
    camadas = [(0.48, 0.42, 0.4, 2.2), (0.80, 0.46, 1.0, 1.0)]
    L = np.array([0.55, 0.65, 0.5]); L /= np.linalg.norm(L)
    for i, (base_y, amp, perto, esc) in enumerate(camadas):
        x = np.arange(w) / (w / (3.2 * esc))
        grande = fbm3(x, np.full_like(x, sem + i), np.full_like(x, i * 1.7), 3)
        fino = fbm3(x * 9, np.full_like(x, sem + i + 50), np.full_like(x, i), 5)
        crista = 1 - np.abs(2 * fino - 1)
        perfil = np.clip((grande - 0.3) * 1.6, 0, 1.2) * 0.8 + crista * 0.22
        if plano:
            lados = np.clip((np.abs(xs) - 0.55) / 0.45, 0, 1) ** 1.6
            perfil = perfil * (0.12 + 0.88 * lados) + lados * 0.9
        linha = (1 - alto) * h + base_y * alto * h - perfil * amp * alto * h
        dy = yy - linha[None, :]
        m = np.clip(dy + 0.5, 0, 1)
        H = _relevo(w, h, 30 * esc, sem + 7 + i, 6) * 0.7 + fbm2(w, h, 9 * esc, 4, sem + 30 + i) * 0.3
        if plano:
            H = _relevo(w, h, 30 * esc, sem + 7 + i, 6)
            H = H * 0.5 + fbm2(w, int(h), 60 * esc, 5, sem + 40) * 0.5
        gy, gx = np.gradient(H)
        N = np.dstack([-gx * 14, gy * 14 * (2.2 if plano else 1.0), np.ones_like(H)])
        N /= np.linalg.norm(N, axis=2, keepdims=True)
        d = np.clip(N @ L, 0, 1)
        prof = np.clip(dy / (0.22 * h), 0, 1)
        topo = np.exp(-np.maximum(dy, 0) / (2.5 + 3 * perto))
        inclin = np.gradient(linha)[None, :]
        luz_lado = np.clip(-gaussian_filter(inclin[0], 3)[None, :] * 0.9 + 0.15, 0, 1) ** 1.5
        cor = np.array([0.022, 0.014, 0.036]) * (0.55 + 0.9 * H[..., None])
        cor = cor + ROXO * 0.45 * d[..., None] ** 3 * np.exp(-prof[..., None] * 1.6)
        cor = cor + (ROXO * 0.8 + MAGENTA * 0.2) * topo[..., None] * (0.08 + 0.92 * luz_lado[..., None]) * (0.45 + 0.55 * perto) * (0.5 + H[..., None] * 0.8)
        if plano:
            centro = np.exp(-xs[None, :] ** 2 / 0.25) * np.exp(-prof * 2.5)
            cor = cor + np.array([0.55, 0.22, 0.62]) * 0.10 * centro[..., None] * (0.6 + H[..., None])
        cor = cor * (1 - prof[..., None] * 0.55)
        neblina = (1 - perto) * 0.55
        cor = cor * (1 - neblina) + np.array([0.045, 0.02, 0.09]) * neblina * np.exp(-prof[..., None])
        rgb = rgb * (1 - m[..., None]) + cor * m[..., None]
        alfa = np.maximum(alfa, m)
    return rgb, alfa


def pedra(S=360, sem=1.0, luz=(0.7, 0.4, -0.3)):
    yy, xx = np.mgrid[0:S, 0:S].astype(np.float64)
    X = (xx - S / 2) / (S * 0.42); Y = (yy - S / 2) / (S * 0.42)
    ang = np.arctan2(Y, X); rr = np.sqrt(X * X + Y * Y)
    def forma(a):
        return 0.78 + 0.22 * fbm3(np.cos(a) * 1.4 + sem, np.sin(a) * 1.4, np.full_like(a, sem), 4) * 1.6 - 0.18
    lim = forma(ang)
    m = np.clip((lim - rr) * S * 0.42 + 0.5, 0, 1)
    h = np.sqrt(np.clip(1 - (rr / lim) ** 2, 0, 1)) + 0.25 * fbm2(S, S, S / 6, 5, sem)
    gy, gx = np.gradient(h)
    N = np.dstack([-gx * S * 0.12, gy * S * 0.12, np.ones_like(h)])
    N /= np.linalg.norm(N, axis=2, keepdims=True)
    L = np.array(luz); L /= np.linalg.norm(L)
    L2 = np.array([-0.5, 0.6, 0.6]); L2 /= np.linalg.norm(L2)
    d = np.clip(N @ L, 0, 1); d2 = np.clip(N @ L2, 0, 1)
    borda = np.clip(1 - (lim - rr) * 6, 0, 1) ** 3
    tex = fbm2(S, S, S / 14, 4, sem + 3)
    cor = np.array([0.05, 0.035, 0.07])[None, None] * (0.5 + tex[..., None]) * (0.4 + 0.6 * d2[..., None])
    cor += ROXO * 1.1 * d[..., None] ** 2.5 + MAGENTA * 0.5 * borda[..., None] * d[..., None] + VIOLETA * 0.08 * d2[..., None]
    return tom(cor * 1.2), m


# ---------- montagem ----------
def ceu(w, h, limbo=True):
    y = np.linspace(0, 1, h)[:, None, None]
    fundo = np.array([0.018, 0.01, 0.035]) * (1 - y) + np.array([0.008, 0.004, 0.016]) * y
    img = np.broadcast_to(fundo, (h, w, 3)).copy()
    img += nebulosa(w, h, ROXO * 0.55, MAGENTA * 0.45, centro=(0.66, 0.42), raio=0.62, forca=0.9, sem=3)
    img += nebulosa(w, h, AZUL * 0.25, ROXO * 0.35, centro=(0.2, 0.15), raio=0.4, forca=0.45, sem=8)
    img += estrelas(w, h, int(w * h / 900), 0.9, grandes=int(w * h / 90000))
    if limbo:
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
        cx, cy, Rr = w * 1.02, -h * 0.55, h * 0.92
        d = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2) - Rr
        disco = np.clip(-d + 0.5, 0, 1)
        dentro_cor = np.array([0.012, 0.008, 0.022]) + ROXO * 0.10 * np.exp(np.minimum(d, 0) / 60)[..., None]
        img = img * (1 - disco[..., None]) + dentro_cor * disco[..., None]
        brilho = np.exp(-np.abs(d) / 2.2) * 0.9 + np.exp(-np.maximum(d, 0) / 45) * 0.28 * (d > 0)
        img += (AZUL * 0.5 + ROXO * 0.6)[None, None] * brilho[..., None] * 0.8
    return tom(img * 1.6)


def principal(saida, partes):
    os.makedirs(saida, exist_ok=True)
    if "ceu" in partes:
        salvar(ceu(2560, 1300, limbo=False), f"{saida}/espaco-ceu.png")
    if "ceu-celular" in partes:
        salvar(ceu(1080, 2340, limbo=False), f"{saida}/espaco-ceu-celular.png")
    if "ceu2" in partes:
        salvar(ceu(2560, 1300, limbo=True), f"{saida}/espaco-ceu-limbo.png")
    if "planeta" in partes:
        rgb, a = planeta(1600)
        salvar(rgb, f"{saida}/espaco-planeta.png", a)
    if "rochas" in partes:
        rgb, a = chao(2560, 520, alto=0.9, sem=4.0)
        salvar(rgb, f"{saida}/espaco-rochas.png", a)
    if "pedras" in partes:
        for i in range(3):
            rgb, a = pedra(360, sem=1.0 + i * 2.7)
            salvar(rgb, f"{saida}/espaco-pedra-{i+1}.png", a)
    if "palco" in partes:
        bg = ceu(2560, 1100, limbo=True)
        rgb, a = chao(2560, 1100, alto=0.48, sem=9.0, plano=True)
        salvar(bg * (1 - a[..., None]) + rgb * a[..., None], f"{saida}/espaco-palco.png")
    if "borda" in partes:
        w, h = 1800, 1300
        y = np.linspace(0, 1, h)[:, None, None]
        img = np.broadcast_to(np.array([0.012, 0.007, 0.024]), (h, w, 3)).copy()
        img += nebulosa(w, h, ROXO * 0.4, MAGENTA * 0.3, centro=(0.7, 0.6), raio=0.6, forca=0.6, sem=12)
        img += estrelas(w, h, int(w * h / 1100), 0.8, grandes=14)
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float64)
        cx, cy, Rr = w * 1.55, h * 0.95, w * 0.78
        dd = np.sqrt((xx - cx) ** 2 + (yy - cy) ** 2)
        d = dd - Rr
        disco = np.clip(-d + 0.5, 0, 1)
        nz = np.sqrt(np.clip(1 - (dd / Rr) ** 2, 0, 1))
        luzes = (fbm2(w, h, 9, 3, 21) > 0.68) * (fbm2(w, h, 120, 4, 22) > 0.45) * 0.5
        sup = np.array([0.012, 0.008, 0.022]) + ROXO * 0.12 * (1 - nz[..., None]) ** 4 + np.array([0.7, 0.5, 1.0]) * luzes[..., None] * nz[..., None] * 0.35
        img = img * (1 - disco[..., None]) + sup * disco[..., None]
        brilho = np.exp(-np.abs(d) / 2.2) * 1.1 + np.exp(-np.maximum(d, 0) / 55) * 0.4 * (d > 0) + np.exp(np.minimum(d, 0) / 25) * 0.25 * (d <= 0)
        img += (AZUL * 0.55 + ROXO * 0.55)[None, None] * brilho[..., None]
        salvar(tom(img * 1.5), f"{saida}/espaco-borda.png")
    if "orbes" in partes:
        cores = [(ROXO, MAGENTA), (AZUL, ROXO), (MAGENTA, ROXO), (VIOLETA, AZUL), (ROXO, AZUL)]
        for i, (c1, c2) in enumerate(cores):
            rgb, a = planeta(240, R=240 * 0.25, facetas=60, giro=(0.3 * i, -0.4, 0.1 * i), luz_cor=c1, borda_cor=c2,
                             aneis_cfg=[dict(r=1.55, incl=1.2, rotz=-0.6, cor=(c2, c1), larg=1.2, forca=1.3, n=5000)])
            salvar(rgb, f"{saida}/espaco-orbe-{i+1}.png", a)


if __name__ == "__main__":
    principal(sys.argv[1], sys.argv[2:] or ["ceu", "planeta", "rochas", "pedras", "palco", "borda", "orbes"])
