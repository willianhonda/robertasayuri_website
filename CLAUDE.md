# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Static institutional site for Dra. Roberta Sayuri (www.robertasayuri.com.br), in plain HTML/CSS/JS with no build step, framework, package manager, linter or tests. It is hosted on GitHub Pages from `main` at `/` (root), with the domain in `CNAME`. Pushing to `main` deploys. All content and copy is in Brazilian Portuguese. README.md (also in Portuguese) is the operator manual and changelog. Keep its changelog and pending items up to date when content changes.

## Local preview

Pages use root-absolute paths (`/assets/...`, `/contato/#agendar`), so open them through a server at the repo root, not with `file://`:

```bash
python3 -m http.server 8000   # http://localhost:8000/
```

## Architecture

- **One `index.html` per directory** gives clean URLs (`/sjc/`, `/blog/<slug>/`). A new page needs a new folder with an `index.html` and an entry in `sitemap.xml`.
- **No templating:** the `<head>` (meta, OG, favicons, Google Fonts), header/nav, footer, floating WhatsApp button, cookie banner and inline WhatsApp tracking script are **copied into every page**. A change to any of these must be made in all 22 HTML files, including `404.html`. Use grep to find every copy.
- `assets/css/style.css` is the whole design system. Brand colors (cream, sage, rosé, bordeaux) and fonts are CSS variables in `:root`. Cormorant Garamond and Inter stand in for the brand fonts Blackline and Nexa.
- `assets/js/main.js` adds behavior through data attributes: `[data-nav-toggle]`/`[data-nav-menu]`, `[data-faq-item]`/`[data-faq-question]`, `[data-cookie-banner]` (consent stored in localStorage key `rs-cookie-consent`), `.reveal` (scroll reveal) and active-link marking on `.nav__link`.
- **Booking flow:** there is no Linktree and no form. The header, floating button and CTAs point to `#agendar` (or `/contato/#agendar` on pages without that block). That block has one WhatsApp button per clinic location:
  - Guaianases (`/guaianases/`): `wa.me/5511982819473`, CEMID, Rua Saturnino Pereira, 317, Vila Santa Cruz, CEP 08411-000 (Saturdays 8h–17h)
  - São José dos Campos (`/sjc/`): `wa.me/5512992371046`, **Espaço Vitale** (one L, confirmed by the client), Av. Saga, 108, Jardim Oriente, **CEP 12236-170** (verified on ViaCEP; the old 12241-200 was wrong), Fridays 13h–17h
- Official profiles: Instagram `https://www.instagram.com/dra.roberta.sayuri/`; Google Business Profiles Guaianases `kgmid=/g/11z7gr5n07` (share.google/07G1CWmfQdCao6MiV) and SJC `kgmid=/g/11z8s_2zd5` (share.google/fFXfOB14PxpM1fB2H). They are used in `sameAs` and on the location pages.
- **WhatsApp tracking:** every WhatsApp link needs `class="wa-cta"`, `data-unidade="guaianases|sjc"` and a `data-source`. Every `<body>` has `data-pagina="..."`. The inline script before `</body>` appends `[utm_source / utm_campaign-or-data-pagina]` to the prefilled text. It also fires the GA4 event `clique_whatsapp` if `gtag` exists. `main.js` separately fires `whatsapp_click`. GA4 is not installed yet.
- **SEO / structured data:** each page has its own canonical, OG and Twitter tags (OG image: `assets/img/og-dra-roberta-sayuri.jpg`). JSON-LD is one entity graph with stable `@id`s, repeated where relevant:
  - `/sobre/#medica`: the doctor as a `Person` (CRM, education, `worksFor` both locations). Do not use `Physician` for her as a person.
  - `/guaianases/#consultorio` and `/sjc/#consultorio`: one `Physician` (local-business type) per location, with address, geo, phone and services.
  - `/#website`: `WebSite`.
  - The full nodes live on home, `/guaianases/`, `/sjc/`, `/contato/` and `/sobre/`. When NAP, hours or services change, update every copy, plus the visible copy, footer, maps and `llms.txt`.
- `llms.txt` at the root is a plain-text summary of the official facts for AI crawlers. Keep it in sync.
- City strategy: no doorway pages per city. Nearby cities (Jacareí, Caçapava, Taubaté; Zona Leste neighborhoods and CPTM Linha 11 cities) are covered with real access info inside `/sjc/` and `/guaianases/`.
- **Images:** photos live in `assets/img/photos/` as `-md`/`-lg` pairs in both JPG and WebP, used through `<picture>`. Procedure cards use SVG placeholders in `assets/img/procedimentos/<slug>.svg`. These appear on `/atendimentos/procedimentos-esteticos/` and `/estetica-sjc/`.

## Image scripts (need Pillow: `pip3 install pillow`)

```bash
python3 scripts/atualizar-foto-dra.py ~/Downloads/foto.jpg [--foco cima|baixo]
# regenerates dra-roberta-sayuri-medica-retrato-{md,lg}.{jpg,webp} (4:5, home hero); no HTML change needed

python3 scripts/foto-procedimento.py --listar
python3 scripts/foto-procedimento.py <slug> ~/Downloads/foto.jpg
# writes <slug>.jpg/.webp 800x600 and rewrites the <img src=...svg> into a <picture> in every page; keeps the SVG
```

## Content rules (CFM Resolution 2.336/2023), mandatory for any copy change

- Never call her "dermatologista" or "especialista" (she has no RQE). Use "médica" and "cuidados com a pele, cabelos e unhas". Her pós-graduação (Dermatologia Clínica e Cosmética, Inspirali) may only appear with "NÃO ESPECIALISTA" in caps (CFM 2.336/2023, art. 13).
- No before/after photos, patient testimonials, clinical cases, prices, promotions or promises of results. Procedures say "após avaliação médica".
- Show CRM-SP 213495 on every page. Keep the ethical disclaimers on service and blog pages.
- Write informative copy, not advertising copy. Don't use the em dash (—) in site copy. Say "recibo", not "nota fiscal".
- Photos must not show identifiable patients or readable prescriptions.
- These old strings must not come back to public pages: "New Worker", "Aquarius", "linktr.ee", "15 minutos", "Vitalle", "12241-200". "Dermatologista" appears only in the explicit negation "não é dermatologista / sem RQE" (FAQ and /sobre/), which is intentional.

## Pending items marked in code

- The new SJC pages include a commented-out "version B" price paragraph. Publish it only if the doctor approves.
