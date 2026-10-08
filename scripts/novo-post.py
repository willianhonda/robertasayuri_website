#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Gera um artigo do blog a partir de um rascunho em Markdown.

Uso:
    python3 scripts/novo-post.py blog/_rascunhos/molusco-contagioso.md
    python3 scripts/novo-post.py --todos

O rascunho tem um cabeçalho entre linhas "---" e o texto em Markdown simples
(## títulos, ### subtítulos, parágrafos, listas com "- " ou "1. ",
**negrito**, *itálico* e [links](/url)). A pasta blog/_rascunhos/ não é
publicada pelo GitHub Pages (pastas com "_" são ignoradas).

Campos do cabeçalho:
    titulo        título do artigo (H1)
    descricao     meta description (até 160 caracteres)
    resumo        frase abaixo do título
    categoria     ex.: Cuidados com a pele
    data          AAAA-MM-DD (publicação)
    revisado      AAAA-MM-DD (opcional; padrão = data)
    instagram     link do post original (opcional)
    sobre         nome da condição ou do procedimento, para o schema
    sobre_tipo    MedicalCondition ou MedicalProcedure
    servicos      "Nome|/url; Nome|/url" (links para atendimentos)

A seção "## Perguntas frequentes" (### pergunta + resposta) vira também
FAQPage no JSON-LD. O script gera blog/<slug>/index.html, inclui o card no
topo de /blog/, a URL no sitemap.xml e a linha no llms.txt.

Sem dependências externas.
"""

import glob
import html
import json
import math
import os
import re
import sys

RAIZ = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = "https://www.robertasayuri.com.br"
MODELO = os.path.join(RAIZ, "blog", "acne-adulta-mitos-verdades", "index.html")
MESES = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho",
         "agosto", "setembro", "outubro", "novembro", "dezembro"]
OG = BASE + "/assets/img/og-dra-roberta-sayuri.jpg"
AUTORA = ("Médica, CRM-SP 213495, pós-graduada em Dermatologia Clínica e Cosmética "
          "pela Inspirali (NÃO ESPECIALISTA). Atende em Guaianases (SP) e em São José dos Campos.")


def ler_rascunho(caminho):
    texto = open(caminho, encoding="utf-8").read()
    m = re.match(r"---\n(.*?)\n---\n(.*)", texto, re.S)
    if not m:
        sys.exit("Rascunho sem cabeçalho entre linhas '---': %s" % caminho)
    meta = {}
    for linha in m.group(1).splitlines():
        if ":" in linha:
            k, v = linha.split(":", 1)
            meta[k.strip()] = v.strip()
    for campo in ("titulo", "descricao", "resumo", "categoria", "data"):
        if not meta.get(campo):
            sys.exit("Campo '%s' ausente em %s" % (campo, caminho))
    if len(meta["descricao"]) > 160:
        sys.exit("descricao com %d caracteres (máx. 160) em %s" % (len(meta["descricao"]), caminho))
    meta.setdefault("revisado", meta["data"])
    return meta, m.group(2).strip()


def inline(t):
    t = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", t)
    t = re.sub(r"(?<![\w*])\*(?!\s)(.+?)(?<!\s)\*(?![\w*])", r"<em>\1</em>", t)

    def link(m):
        txt, url = m.group(1), m.group(2)
        ext = url.startswith("http")
        attrs = ' target="_blank" rel="noopener"' if ext else ""
        return '<a href="%s"%s>%s</a>' % (url, attrs, txt)
    return re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link, t)


def markdown(md):
    """Converte o Markdown do rascunho. Devolve (html, faq)."""
    out, faq, lista, par = [], [], None, []
    secao = ""
    pergunta = None

    def fecha_par():
        nonlocal par, pergunta
        if par:
            texto = " ".join(par)
            out.append("        <p>%s</p>" % inline(texto))
            if pergunta is not None:
                faq.append((pergunta, re.sub(r"<[^>]+>", "", inline(texto))))
                pergunta = None
            par = []

    def fecha_lista():
        nonlocal lista
        if lista:
            tag, itens = lista
            out.append("        <%s>\n%s\n        </%s>" % (
                tag, "\n".join("          <li>%s</li>" % inline(i) for i in itens), tag))
            lista = None

    for linha in md.splitlines() + [""]:
        s = linha.strip()
        if not s:
            fecha_par(); fecha_lista(); continue
        if s.startswith("### "):
            fecha_par(); fecha_lista()
            out.append("        <h3>%s</h3>" % inline(s[4:]))
            if secao.lower().startswith("perguntas frequentes"):
                pergunta = s[4:]
            continue
        if s.startswith("## "):
            fecha_par(); fecha_lista()
            secao = s[3:]
            out.append("        <h2>%s</h2>" % inline(s[3:]))
            continue
        m = re.match(r"(- |\d+\. )(.*)", s)
        if m:
            fecha_par()
            tag = "ul" if m.group(1) == "- " else "ol"
            if not lista or lista[0] != tag:
                fecha_lista(); lista = (tag, [])
            lista[1].append(m.group(2)); continue
        fecha_lista(); par.append(s)
    return "\n\n".join(out), faq


def data_extenso(d):
    a, m, dia = d.split("-")
    return "%d de %s de %s" % (int(dia), MESES[int(m) - 1], a)


def gerar(caminho):
    meta, md = ler_rascunho(caminho)
    slug = os.path.splitext(os.path.basename(caminho))[0]
    url = "%s/blog/%s/" % (BASE, slug)
    corpo, faq = markdown(md)
    palavras = len(re.sub(r"<[^>]+>", " ", corpo).split())
    leitura = max(3, math.ceil(palavras / 200))
    titulo_seo = meta.get("titulo_seo") or meta["titulo"]
    e = html.escape

    # capa (gerada por scripts/capa-post.py); sem ela, card com a mandala e og:image padrão
    capa_rel = "/assets/img/blog/%s-capa" % slug
    tem_capa = os.path.exists(os.path.join(RAIZ, capa_rel.lstrip("/") + ".jpg"))
    og_img, og_w, og_h = (BASE + capa_rel + ".jpg", 1200, 675) if tem_capa else (OG, 1200, 630)
    og_alt = ("Capa do artigo: " + meta["titulo"]) if tem_capa else \
        "Dra. Roberta Sayuri, médica (CRM-SP 213495), com consultas em Guaianases (São Paulo) e São José dos Campos"

    def picture(alt, sizes, lazy=True):
        return ('<picture><source type="image/webp" srcset="{c}.webp"><img src="{c}.jpg" alt="{a}" width="1200" height="675"'
                ' sizes="{s}"{l}></picture>').format(c=capa_rel, a=e(alt), s=sizes, l=' loading="lazy"' if lazy else "")

    modelo = open(MODELO, encoding="utf-8").read()
    head_comum = modelo[modelo.index('  <link rel="icon"'):modelo.index('<script type="application/ld+json">')]
    cabecalho = modelo[modelo.index('  <a class="skip-link"'):modelo.index("  <main id=\"main\">")]
    cta = modelo[modelo.index('    <section class="section" id="agendar">'):modelo.index("  </main>")]
    rodape = modelo[modelo.index('  <footer class="site-footer">'):]

    post = {
        "@type": "BlogPosting", "@id": url + "#artigo", "headline": meta["titulo"],
        "description": meta["descricao"], "datePublished": meta["data"], "dateModified": meta["revisado"],
        "inLanguage": "pt-BR", "image": og_img, "wordCount": palavras,
        "mainEntityOfPage": {"@type": "WebPage", "@id": url},
        "isPartOf": {"@id": BASE + "/#website"},
        "author": {"@type": "Person", "@id": BASE + "/sobre/#medica", "name": "Dra. Roberta Sayuri",
                   "url": BASE + "/sobre/", "jobTitle": "Médica",
                   "identifier": {"@type": "PropertyValue", "propertyID": "CRM-SP", "value": "213495"}},
        "publisher": {"@id": BASE + "/sobre/#medica"},
    }
    if meta.get("sobre"):
        post["about"] = {"@type": meta.get("sobre_tipo", "MedicalCondition"), "name": meta["sobre"]}
    if meta.get("instagram"):
        post["sameAs"] = meta["instagram"]
    grafo = [post, {"@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": 1, "name": "Início", "item": BASE + "/"},
        {"@type": "ListItem", "position": 2, "name": "Blog", "item": BASE + "/blog/"},
        {"@type": "ListItem", "position": 3, "name": meta["titulo"], "item": url}]}]
    if faq:
        grafo.append({"@type": "FAQPage", "mainEntity": [
            {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": a}} for q, a in faq]})
    ld = '<script type="application/ld+json">\n%s\n</script>' % json.dumps(
        {"@context": "https://schema.org", "@graph": grafo}, ensure_ascii=False, indent=2)

    servicos = [s.split("|") for s in meta.get("servicos", "").split(";") if "|" in s]
    links_serv = " e ".join('<a href="%s">%s</a>' % (u.strip(), n.strip()) for n, u in servicos)
    onde = ('        <p><strong>Onde ter uma avaliação:</strong> a Dra. Roberta Sayuri atende em consulta nas unidades de '
            '<a href="/guaianases/">Guaianases (São Paulo)</a>, aos sábados, e de <a href="/sjc/">São José dos Campos</a>, '
            'às sextas-feiras.%s</p>') % ((" Saiba mais em " + links_serv + ".") if servicos else "")
    insta = ""
    if meta.get("instagram"):
        insta = ('\n\n        <p>Este artigo amplia um conteúdo publicado no '
                 '<a href="%s" target="_blank" rel="noopener">Instagram da Dra. Roberta Sayuri</a>.</p>') % meta["instagram"]

    figura = ""
    if tem_capa:
        figura = '        <figure class="post-capa">%s</figure>\n\n' % picture(meta["titulo"], "(max-width: 768px) 100vw, 720px", lazy=False)
    pagina = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <meta name="theme-color" content="#FFFDFA">

  <title>{tseo} | Dra. Roberta Sayuri</title>
  <meta name="description" content="{desc}">
  <link rel="canonical" href="{url}">

  <meta property="og:type" content="article">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="Dra. Roberta Sayuri">
  <meta property="og:title" content="{tseo} | Dra. Roberta Sayuri">
  <meta property="og:description" content="{desc}">
  <meta property="og:url" content="{url}">
  <meta property="og:image" content="{og}">
  <meta property="og:image:width" content="{ogw}">
  <meta property="og:image:height" content="{ogh}">
  <meta property="og:image:alt" content="{ogalt}">
  <meta property="article:published_time" content="{data}">
  <meta property="article:modified_time" content="{rev}">

  <meta name="twitter:card" content="summary_large_image">
  <meta name="twitter:title" content="{tseo} | Dra. Roberta Sayuri">
  <meta name="twitter:description" content="{desc}">
  <meta name="twitter:image" content="{og}">

{head}{ld}
</head>

<body data-pagina="blog/{slug}">
{cab}  <main id="main">
    <section class="page-hero">
      <div class="container">
        <div class="page-hero__inner reveal">
          <ol class="breadcrumb"><li><a href="/">Início</a></li><li><a href="/blog/">Blog</a></li><li>{tit}</li></ol>
          <span class="eyebrow">{cat}</span>
          <h1>{tit}</h1>
          <p style="margin-top: var(--space-sm); font-size: 1.1rem; color: var(--color-text-soft);">{resumo}</p>
          <p class="post-meta">Por <a href="/sobre/">Dra. Roberta Sayuri</a>, médica, CRM-SP 213495 · Publicado em <time datetime="{data}">{data_ext}</time> · {leitura} min de leitura</p>
        </div>
      </div>
    </section>
    <section class="section">
      <div class="container">
        <article class="prose reveal" style="margin: 0 auto;">

{figura}{corpo}

{onde}{insta}

          <div class="disclaimer">
            <strong>Aviso:</strong> este artigo tem caráter educativo e não substitui consulta médica. Diagnóstico e tratamento dependem de avaliação individual.
          </div>

          <div class="author-card">
            <img src="/assets/img/photos/dra-roberta-avatar-md.jpg" alt="Dra. Roberta Sayuri, médica, sorrindo, de jaleco branco" width="72" height="72" loading="lazy">
            <div class="author-card__text">
              <strong>Dra. Roberta Sayuri</strong>
              <span>{autora} <a href="/sobre/">Conheça a trajetória</a>.</span>
            </div>
          </div>
        </article>
      </div>
    </section>
{cta}  </main>

{rod}""".format(tseo=e(titulo_seo), desc=e(meta["descricao"]), url=url, og=og_img, ogw=og_w, ogh=og_h, ogalt=e(og_alt), figura=figura, data=meta["data"],
                rev=meta["revisado"], head=head_comum, ld=ld, slug=slug, cab=cabecalho, tit=e(meta["titulo"]),
                cat=e(meta["categoria"]), resumo=e(meta["resumo"]), data_ext=data_extenso(meta["data"]),
                leitura=leitura, corpo=corpo, onde=onde, insta=insta, autora=AUTORA, cta=cta, rod=rodape)

    destino = os.path.join(RAIZ, "blog", slug)
    os.makedirs(destino, exist_ok=True)
    open(os.path.join(destino, "index.html"), "w", encoding="utf-8").write(pagina)

    # card no topo de /blog/
    idx_path = os.path.join(RAIZ, "blog", "index.html")
    idx = open(idx_path, encoding="utf-8").read()
    href = '/blog/%s/' % slug
    card = """          <a class="blog-card reveal" href="{href}">
            <div class="blog-card__cover" aria-hidden="true">
              {capa}
            </div>
            <div class="blog-card__body">
              <span class="blog-card__category">{cat}</span>
              <h3>{tit}</h3>
              <p class="blog-card__excerpt">{resumo}</p>
              <span class="blog-card__meta">{leitura} min de leitura</span>
            </div>
          </a>

""".format(href=href, capa=picture("", "(max-width: 768px) 100vw, 380px") if tem_capa else '<img src="/assets/img/decor-mandala.svg" alt="">', cat=e(meta["categoria"]), tit=e(meta["titulo"]), resumo=e(meta["resumo"]), leitura=leitura)
    bloco = re.search(r'          <a class="blog-card reveal" href="%s">.*?</a>\n\n' % re.escape(href), idx, re.S)
    if bloco:
        idx = idx[:bloco.start()] + card + idx[bloco.end():]
    else:
        marca = '<div class="blog-grid">\n'
        idx = idx.replace(marca, marca + card, 1)
    open(idx_path, "w", encoding="utf-8").write(idx)

    # sitemap
    sm_path = os.path.join(RAIZ, "sitemap.xml")
    sm = open(sm_path, encoding="utf-8").read()
    if url not in sm:
        sm = sm.replace("</urlset>", "  <url>\n    <loc>%s</loc>\n    <lastmod>%s</lastmod>\n  </url>\n</urlset>" % (url, meta["revisado"]))
        open(sm_path, "w", encoding="utf-8").write(sm)

    # llms.txt
    llms_path = os.path.join(RAIZ, "llms.txt")
    llms = open(llms_path, encoding="utf-8").read()
    if url not in llms:
        llms = llms.rstrip("\n") + "\n- [%s](%s): %s\n" % (meta["titulo"], url, meta["descricao"])
        open(llms_path, "w", encoding="utf-8").write(llms)

    print("ok  %s  (%d palavras, %d min, %d perguntas)" % (href, palavras, leitura, len(faq)))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    arquivos = sorted(glob.glob(os.path.join(RAIZ, "blog", "_rascunhos", "*.md"))) if sys.argv[1] == "--todos" else sys.argv[1:]
    for a in arquivos:
        gerar(a)
