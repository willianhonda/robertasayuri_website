#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera a imagem de capa de um artigo do blog (1200 x 675, JPG + WebP).

Uso:
    python3 scripts/capa-post.py molusco-contagioso
        capa com a identidade visual do site, usando o campo "capa_texto"
        (ou "sobre") do rascunho blog/_rascunhos/<slug>.md

    python3 scripts/capa-post.py protetor-solar-no-dia-a-dia --texto "Protetor solar" --categoria "Cuidados com a pele"
        capa com a identidade visual para um artigo sem rascunho em Markdown

    python3 scripts/capa-post.py molusco-contagioso ~/Downloads/foto.jpg [--foco cima|baixo]
        capa a partir de uma foto (recorte 16:9)

Grava assets/img/blog/<slug>-capa.jpg e .webp. Depois rode
scripts/novo-post.py no mesmo rascunho para a capa entrar no card, no topo do
artigo e no compartilhamento (og:image).

Fotos: sem paciente identificável, sem receituário legível, sem antes e depois,
e só imagens próprias ou com autorização de uso.

Requisito: Pillow (pip3 install pillow)
"""

import os
import re
import sys

try:
    from PIL import Image, ImageDraw, ImageFont, ImageOps
except ImportError:
    sys.exit("Pillow não instalado. Rode: pip3 install pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "img", "blog")
W, H = 1200, 675
CREME, SALVIA, ROSE, BORDO, SALVIA_ESC, TEXTO = (255, 253, 250), (198, 209, 165), (245, 208, 202), (142, 69, 83), (89, 98, 84), (44, 50, 44)
FONTES = {
    "titulo": ["/System/Library/Fonts/Supplemental/Georgia.ttf", "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"],
    "texto": ["/System/Library/Fonts/Avenir Next.ttc", "/System/Library/Fonts/Supplemental/Arial.ttf",
              "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"],
}


def fonte(tipo, tamanho, indice=0):
    for f in FONTES[tipo]:
        if os.path.exists(f):
            try:
                return ImageFont.truetype(f, tamanho, index=indice if f.endswith(".ttc") else 0)
            except OSError:
                continue
    return ImageFont.load_default()


def meta_rascunho(slug):
    caminho = os.path.join(RAIZ, "blog", "_rascunhos", slug + ".md")
    if not os.path.exists(caminho):
        sys.exit("Rascunho não encontrado: %s" % caminho)
    cab = re.match(r"---\n(.*?)\n---", open(caminho, encoding="utf-8").read(), re.S).group(1)
    return dict((k.strip(), v.strip()) for k, v in (l.split(":", 1) for l in cab.splitlines() if ":" in l))


def quebra(draw, texto, f, largura):
    linhas, atual = [], ""
    for palavra in texto.split():
        teste = (atual + " " + palavra).strip()
        if draw.textlength(teste, font=f) <= largura:
            atual = teste
        else:
            linhas.append(atual); atual = palavra
    linhas.append(atual)
    return linhas


def capa_marca(slug, texto=None, categoria=None):
    meta = {"titulo": texto, "categoria": categoria} if texto else meta_rascunho(slug)
    texto = meta.get("capa_texto") or meta.get("sobre") or meta["titulo"]
    categoria = meta.get("categoria", "Blog").upper()
    im = Image.new("RGB", (W, H), CREME)
    d = ImageDraw.Draw(im)
    d.ellipse((760, -260, 1380, 360), fill=(252, 236, 232))
    d.ellipse((-220, 420, 360, 1000), fill=(239, 242, 228))
    d.ellipse((900, 470, 1080, 650), outline=SALVIA, width=3)
    d.ellipse((960, 530, 1020, 590), fill=ROSE)
    logo = os.path.join(RAIZ, "assets", "img", "logotype.png")
    if os.path.exists(logo):
        mark = Image.open(logo).convert("RGBA").resize((84, 84))
        im.paste(mark, (90, 80), mark)
    d.text((90, 205), categoria, font=fonte("texto", 24, 2), fill=BORDO)
    d.line((90, 245, 160, 245), fill=BORDO, width=2)
    tam = 84
    while True:
        f = fonte("titulo", tam)
        linhas = quebra(d, texto, f, 820)
        if len(linhas) <= 3 or tam <= 52:
            break
        tam -= 6
    y = 285
    for l in linhas:
        d.text((86, y), l, font=f, fill=SALVIA_ESC)
        y += int(tam * 1.18)
    d.text((90, H - 80), "Dra. Roberta Sayuri · Médica · CRM-SP 213495", font=fonte("texto", 24, 0), fill=SALVIA_ESC)
    return im


def capa_foto(caminho, foco):
    im = ImageOps.exif_transpose(Image.open(os.path.expanduser(caminho))).convert("RGB")
    centro = {"cima": (0.5, 0.2), "baixo": (0.5, 0.8)}.get(foco, (0.5, 0.5))
    return ImageOps.fit(im, (W, H), Image.LANCZOS, centering=centro)


def main():
    def opcao(nome):
        return sys.argv[sys.argv.index(nome) + 1] if nome in sys.argv else None
    foco, texto, categoria = opcao("--foco") or "centro", opcao("--texto"), opcao("--categoria")
    args = [a for a in sys.argv[1:] if not a.startswith("--") and a not in (foco, texto, categoria)]
    if not args:
        sys.exit(__doc__)
    slug = args[0]
    im = capa_foto(args[1], foco) if len(args) > 1 else capa_marca(slug, texto, categoria)
    os.makedirs(DESTINO, exist_ok=True)
    base = os.path.join(DESTINO, slug + "-capa")
    im.save(base + ".jpg", "JPEG", quality=84, optimize=True, progressive=True)
    im.save(base + ".webp", "WEBP", quality=82, method=6)
    print("ok  %s.jpg / .webp" % os.path.relpath(base, RAIZ))


if __name__ == "__main__":
    main()
