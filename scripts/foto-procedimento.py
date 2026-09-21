#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Troca a ilustração de um procedimento por uma foto real.

Uso:
    python3 scripts/foto-procedimento.py botox-terco-superior ~/Downloads/foto.jpg

O script:
 1. gera assets/img/procedimentos/<slug>.jpg e .webp em 800x600 (recorte 4:3);
 2. troca, em todas as páginas do site, o <img> que aponta para <slug>.svg
    por um <picture> com webp e jpg;
 3. mantém o .svg no repositório, caso você queira voltar atrás.

Para listar os slugs disponíveis:
    python3 scripts/foto-procedimento.py --listar

Regras: sem paciente identificável no enquadramento, sem receituário legível,
sem foto de antes e depois.

Requisito: Pillow (pip3 install pillow)
"""

import argparse
import glob
import os
import re
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow não instalado. Rode: pip3 install pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PASTA = os.path.join(RAIZ, "assets", "img", "procedimentos")
LARGURA, ALTURA = 800, 600
PROPORCAO = LARGURA / ALTURA


def slugs():
    return sorted(os.path.basename(f)[:-4] for f in glob.glob(os.path.join(PASTA, "*.svg")))


def recorta(img, foco):
    l, a = img.size
    if l / a > PROPORCAO:
        nova_l = int(round(a * PROPORCAO))
        esq = (l - nova_l) // 2
        return img.crop((esq, 0, esq + nova_l, a))
    nova_a = int(round(l / PROPORCAO))
    topo = 0 if foco == "cima" else (a - nova_a if foco == "baixo" else (a - nova_a) // 2)
    return img.crop((0, topo, l, topo + nova_a))


def atualiza_paginas(slug):
    alvo = "/assets/img/procedimentos/%s.svg" % slug
    padrao = re.compile(r'<img class="proc-card__img" src="%s" alt="([^"]*)"[^>]*>' % re.escape(alvo))
    trocadas = 0
    for caminho in glob.glob(os.path.join(RAIZ, "**", "*.html"), recursive=True):
        html = open(caminho, encoding="utf-8").read()
        if alvo not in html:
            continue
        def substitui(m):
            alt = m.group(1).replace("Ilustração do procedimento: ", "")
            return (
                '<picture>\n'
                '              <source type="image/webp" srcset="/assets/img/procedimentos/%s.webp">\n'
                '              <source type="image/jpeg" srcset="/assets/img/procedimentos/%s.jpg">\n'
                '              <img class="proc-card__img" src="/assets/img/procedimentos/%s.jpg" alt="%s, realizado pela Dra. Roberta Sayuri, médica (CRM-SP 213495)" loading="lazy" width="800" height="600">\n'
                '            </picture>' % (slug, slug, slug, alt))
        novo, n = padrao.subn(substitui, html)
        if n:
            open(caminho, "w", encoding="utf-8").write(novo)
            trocadas += n
            print("atualizado: %s (%d)" % (os.path.relpath(caminho, RAIZ), n))
    return trocadas


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("slug", nargs="?", help="identificador do procedimento")
    ap.add_argument("foto", nargs="?", help="arquivo da foto")
    ap.add_argument("--foco", choices=["cima", "centro", "baixo"], default="centro")
    ap.add_argument("--listar", action="store_true", help="lista os slugs disponíveis")
    args = ap.parse_args()

    if args.listar or not args.slug:
        print("Procedimentos disponíveis:\n")
        for s in slugs():
            print("  " + s)
        return

    if args.slug not in slugs():
        sys.exit("Slug desconhecido. Rode com --listar para ver a lista.")
    if not args.foto or not os.path.isfile(args.foto):
        sys.exit("Informe o arquivo da foto.")

    img = ImageOps.exif_transpose(Image.open(args.foto)).convert("RGB")
    img = recorta(img, args.foco).resize((LARGURA, ALTURA), Image.LANCZOS)
    jpg = os.path.join(PASTA, args.slug + ".jpg")
    webp = os.path.join(PASTA, args.slug + ".webp")
    img.save(jpg, "JPEG", quality=86, optimize=True, progressive=True)
    img.save(webp, "WEBP", quality=82, method=6)
    print("gerado: %s (%d KB)" % (jpg, os.path.getsize(jpg) // 1024))
    print("gerado: %s (%d KB)" % (webp, os.path.getsize(webp) // 1024))

    n = atualiza_paginas(args.slug)
    if n:
        print("\nPronto: %d cartão(ões) agora usam a foto real." % n)
    else:
        print("\nA foto foi gerada, mas nenhum cartão apontava para a ilustração "
              "(talvez já tenha sido trocado antes).")


if __name__ == "__main__":
    main()
