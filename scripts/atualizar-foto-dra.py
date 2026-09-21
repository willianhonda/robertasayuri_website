#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Atualiza a foto principal da Dra. Roberta no site.

Uso:
    python3 scripts/atualizar-foto-dra.py caminho/para/nova-foto.jpg

Gera, em assets/img/photos/, os quatro arquivos que o site usa no hero da
home, no bloco "Sobre a médica" e na página /sobre/:

    dra-roberta-retrato-md.jpg    480 x 600
    dra-roberta-retrato-md.webp   480 x 600
    dra-roberta-retrato-lg.jpg    800 x 1000
    dra-roberta-retrato-lg.webp   800 x 1000

O recorte é central, na proporção 4:5. Se o enquadramento ficar ruim, use
--foco cima  ou  --foco baixo  para deslocar o corte na vertical.

Requisito: Pillow (pip install pillow)
"""

import argparse
import os
import sys

try:
    from PIL import Image, ImageOps
except ImportError:
    sys.exit("Pillow não instalado. Rode: pip3 install pillow")

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DESTINO = os.path.join(RAIZ, "assets", "img", "photos")
TAMANHOS = {"md": (480, 600), "lg": (800, 1000)}
PROPORCAO = 4 / 5


def recorta(img, foco):
    largura, altura = img.size
    alvo_altura = largura / PROPORCAO
    if alvo_altura <= altura:
        nova_altura = int(round(alvo_altura))
        if foco == "cima":
            topo = 0
        elif foco == "baixo":
            topo = altura - nova_altura
        else:
            topo = (altura - nova_altura) // 2
        return img.crop((0, topo, largura, topo + nova_altura))
    nova_largura = int(round(altura * PROPORCAO))
    esquerda = (largura - nova_largura) // 2
    return img.crop((esquerda, 0, esquerda + nova_largura, altura))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("origem", help="arquivo da nova foto (jpg, png, heic convertido)")
    ap.add_argument("--foco", choices=["cima", "centro", "baixo"], default="centro",
                    help="de onde manter o enquadramento no corte vertical")
    args = ap.parse_args()

    if not os.path.isfile(args.origem):
        sys.exit("Arquivo não encontrado: %s" % args.origem)

    img = Image.open(args.origem)
    img = ImageOps.exif_transpose(img).convert("RGB")
    img = recorta(img, args.foco)

    os.makedirs(DESTINO, exist_ok=True)
    for sufixo, (w, h) in TAMANHOS.items():
        versao = img.resize((w, h), Image.LANCZOS)
        jpg = os.path.join(DESTINO, "dra-roberta-retrato-%s.jpg" % sufixo)
        webp = os.path.join(DESTINO, "dra-roberta-retrato-%s.webp" % sufixo)
        versao.save(jpg, "JPEG", quality=86, optimize=True, progressive=True)
        versao.save(webp, "WEBP", quality=82, method=6)
        print("gerado: %s (%d KB)" % (jpg, os.path.getsize(jpg) // 1024))
        print("gerado: %s (%d KB)" % (webp, os.path.getsize(webp) // 1024))

    print("\nPronto. Confira a home e a página /sobre/ antes de publicar.")


if __name__ == "__main__":
    main()
