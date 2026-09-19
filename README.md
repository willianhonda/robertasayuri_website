# Site Dra. Roberta Sayuri — Manual de Deploy

> **Atualização 19/09/2026:** endereço de São José dos Campos corrigido para **Espaço Vitalle, Av. Saga, 108, Jardim Oriente, CEP 12241-200** (o antigo New Worker Tower / Jardim Aquarius saiu do site inteiro). O Linktree saiu de todos os CTAs: agora o botão "Agendar" leva à seção `#agendar`, que tem um botão por unidade apontando direto para o WhatsApp correspondente. Seis páginas novas entraram: `/sjc/`, `/consulta-particular/`, `/queda-de-cabelo-sjc/`, `/acne-sjc/`, `/melasma-manchas-sjc/`, `/estetica-sjc/`.

Site institucional para **robertasayuri.com.br**, em HTML/CSS/JS puro, pronto para GitHub Pages.

---

## 📁 Estrutura do projeto

```
robertasayuri-site/
├── index.html                              ← Home
├── 404.html                                ← Página de erro
├── CNAME                                   ← Domínio customizado (www.robertasayuri.com.br)
├── robots.txt
├── sitemap.xml
├── assets/
│   ├── css/style.css                       ← Design system completo
│   ├── js/main.js                          ← Interações
│   └── img/                                ← Logos, favicon, OG image, placeholder
├── sobre/                                  ← /sobre/
├── atendimentos/
│   ├── index.html                          ← Hub de atendimentos
│   ├── cuidados-com-a-pele/
│   ├── cuidados-com-os-cabelos/
│   ├── cuidados-com-as-unhas/
│   └── procedimentos-esteticos/
├── blog/
│   ├── index.html                          ← Hub de blog
│   ├── protetor-solar-no-dia-a-dia/
│   ├── queda-de-cabelo-quando-procurar-ajuda/
│   └── acne-adulta-mitos-verdades/
├── contato/
├── politica-de-privacidade/
└── termos-de-uso/
```

---

## 🚀 Passo 1 — Subir para o GitHub

```bash
# 1. Descompacte o ZIP em uma pasta local
# 2. Dentro da pasta:
git init
git add .
git commit -m "Site institucional v1"

# 3. Crie um repositório novo no GitHub (sugestão: robertasayuri-site)
# 4. Conecte e suba:
git remote add origin https://github.com/SEU_USUARIO/robertasayuri-site.git
git branch -M main
git push -u origin main
```

---

## 🌐 Passo 2 — Ativar GitHub Pages

1. No GitHub, vá em **Settings → Pages**.
2. Em **Source**, escolha:
   - Branch: `main`
   - Folder: `/ (root)`
3. Clique em **Save**.
4. O GitHub vai te dar uma URL temporária do tipo `seu-usuario.github.io/robertasayuri-site`.

Aguarde alguns minutos para o primeiro deploy.

---

## 🔗 Passo 3 — Apontar o domínio robertasayuri.com.br

### 3.1 No GitHub Pages

O arquivo `CNAME` já vem com `www.robertasayuri.com.br`. Verifique em **Settings → Pages → Custom domain** se aparece. Salve. O GitHub vai verificar o domínio.

Marque **Enforce HTTPS** assim que o certificado for emitido (pode levar até 24h).

### 3.2 No painel do seu provedor de domínio (Registro.br, GoDaddy, etc.)

Configure os DNS:

**Para o domínio raiz (robertasayuri.com.br) — registros A:**

```
Tipo  Nome  Valor                    TTL
A     @     185.199.108.153          3600
A     @     185.199.109.153          3600
A     @     185.199.110.153          3600
A     @     185.199.111.153          3600
```

**Para o subdomínio www — registro CNAME:**

```
Tipo   Nome  Valor                       TTL
CNAME  www   seu-usuario.github.io.      3600
```

> Substitua `seu-usuario` pelo seu username real do GitHub.
> O domínio raiz redirecionará para `www.robertasayuri.com.br`.

**Propagação:** geralmente leva 1 a 24 horas.

---

## ✏️ O que personalizar depois

### 1. Coordenadas exatas do Google Maps (página /contato/)

No arquivo `contato/index.html`, há um `<iframe>` do Google Maps. As coordenadas atuais são aproximadas. Para o endereço exato:

1. Acesse [maps.google.com](https://maps.google.com).
2. Procure: **Rua Saturnino Pereira, 317, Guaianases, SP**.
3. Clique em **Compartilhar → Incorporar um mapa → Copiar HTML**.
4. Substitua o `<iframe>` existente em `contato/index.html`.

### 2. Imagem de capa para redes sociais (OG image)

O arquivo `assets/img/og-cover.png` (1200x630) é o que aparece ao compartilhar o link no WhatsApp, Facebook, LinkedIn etc. Já criamos uma versão placeholder estilizada. Quando quiser substituir por uma com foto real da médica/consultório:

- Mantenha exatamente **1200x630 px**.
- Salve como `og-cover.png` no mesmo caminho.

### 3. Fotos reais da médica e do consultório

Quando as fotos profissionais estiverem prontas:

- Substitua o `placeholder-portrait.svg` por imagens reais nos blocos `hero__visual-placeholder` e `about-split__visual-placeholder`.
- Locais para editar (basta trocar o `<img>` por um `<img src="/assets/img/foto-roberta.jpg" alt="Dra. Roberta Sayuri">`):
  - `index.html` (hero principal + sobre)
  - `sobre/index.html` (sobre completa)
  - Posts do blog (covers — opcional)
- Otimize as imagens antes (use [squoosh.app](https://squoosh.app) — JPG/WebP, ~150-300KB cada).

### 4. Fontes da marca (Blackline e Nexa)

Atualmente o site usa Google Fonts como fallback:
- **Títulos:** Cormorant Garamond (no lugar de Blackline)
- **Nome manuscrito:** Dancing Script
- **Corpo:** Inter (no lugar de Nexa)

Quando tiver as licenças/arquivos `.woff2` da Blackline e Nexa:

1. Coloque os arquivos em `assets/fonts/`.
2. Em `assets/css/style.css`, **antes do `:root`**, adicione:

```css
@font-face {
  font-family: "Blackline";
  src: url("/assets/fonts/Blackline.woff2") format("woff2");
  font-weight: 400;
  font-display: swap;
}
@font-face {
  font-family: "Nexa";
  src: url("/assets/fonts/Nexa-Regular.woff2") format("woff2");
  font-weight: 400;
  font-display: swap;
}
@font-face {
  font-family: "Nexa";
  src: url("/assets/fonts/Nexa-Bold.woff2") format("woff2");
  font-weight: 600;
  font-display: swap;
}
```

3. No mesmo `style.css`, atualize as variáveis:

```css
--font-display: "Blackline", "Cormorant Garamond", Georgia, serif;
--font-body:    "Nexa", "Inter", -apple-system, sans-serif;
```

4. Remova o `<link>` do Google Fonts em cada HTML (opcional, para performance).

### 5. Google Analytics (opcional)

O `main.js` já está pronto para `gtag` — basta colar o snippet do GA4 no `<head>` de cada página HTML (logo antes de `</head>`):

```html
<!-- Google Analytics 4 -->
<script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXX"></script>
<script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){dataLayer.push(arguments);}
  gtag('js', new Date());
  gtag('config', 'G-XXXXXXX', { anonymize_ip: true });
</script>
```

Os cliques no WhatsApp serão automaticamente rastreados como evento `whatsapp_click`.

---

## ✅ Checklist pós-deploy

- [ ] Site abre em `https://www.robertasayuri.com.br` (com cadeado verde)
- [ ] Domínio raiz `robertasayuri.com.br` redireciona para `www`
- [ ] Botão WhatsApp flutuante abre conversa com `(11) 98281-9473`
- [ ] Menu mobile abre e fecha
- [ ] FAQs expandem e colapsam
- [ ] Banner de cookies aparece na primeira visita e some após escolha
- [ ] Submeter `sitemap.xml` no [Google Search Console](https://search.google.com/search-console)
- [ ] Validar Schema.org em [validator.schema.org](https://validator.schema.org/) (testar Home e /sobre/)
- [ ] Validar performance no [PageSpeed Insights](https://pagespeed.web.dev/)
- [ ] Validar conformidade no [Mobile-Friendly Test](https://search.google.com/test/mobile-friendly)
- [ ] Conectar o site ao Google Business Profile existente (link em "Site" do GBP)
- [ ] Compartilhar a URL no WhatsApp para testar a OG image
- [ ] Revisar conteúdo com a Dra. Roberta — especialmente bio, horários, redes

---

## 📐 Conformidade ética (Resolução CFM 2.336/2023)

Este site foi construído respeitando rigorosamente:

✅ **Não usa** "Dermatologista" ou "Dermatologia" como autointitulação (médica não tem RQE)
✅ **Não exibe** antes/depois, depoimentos de pacientes ou casos clínicos
✅ **Não exibe** preços, promoções, descontos ou ofertas
✅ **Não promete** resultados de tratamentos
✅ **Exibe** CRM-SP nº 213495 em todas as páginas
✅ **Inclui** disclaimers éticos em páginas de atendimento e blog
✅ **Linguagem informativa**, não publicitária

Mantenha esses cuidados em qualquer atualização futura de conteúdo.

---

## 🆘 Suporte

- **Hospedagem:** GitHub Pages (gratuita, ilimitada para sites estáticos)
- **Domínio:** verifique a renovação anual no seu provedor
- **Certificado HTTPS:** renovado automaticamente pelo GitHub

Em caso de dúvidas sobre atualização de conteúdo, basta editar os arquivos `.html` correspondentes, commitar e dar push — o deploy é automático.

---

**Versão:** 1.0 · Maio de 2026


---

## 🔄 Changelog 19/09/2026

### Endereço e dados
- SJC: Espaço Vitalle, Av. Saga, 108, Jardim Oriente, São José dos Campos/SP, CEP 12241-200 (home, /contato/, /sobre/, rodapé de todas as páginas, FAQ, JSON-LD, mapa incorporado, política de privacidade).
- Zero ocorrências de "New Worker", "Armando", "Cobra", "Aquarius", "linktr.ee", "nota fiscal", "15 minutos", "dermatolog", "especialista" nas páginas públicas.
- "Nota fiscal" virou "recibo" (atendimento como pessoa física).
- O caractere travessão foi removido de toda a copy.

### Agendamento
- Cabeçalho, botão flutuante e CTAs apontam para `#agendar` (ou `/contato/#agendar` nas páginas sem bloco próprio).
- Cada bloco de agendamento tem dois botões, um por unidade, com texto pré-preenchido no WhatsApp.
- Todo link de WhatsApp tem `class="wa-cta"` e `data-unidade="guaianases|sjc"`.

### Rastreamento
- Script antes de `</body>` em todas as páginas: acrescenta `[origem / campanha]` ao texto do WhatsApp e dispara o evento `clique_whatsapp` no GA4.
- `<body data-pagina="...">` em todas as páginas.
- **Pendente:** instalar o GA4 (o script só dispara se `gtag` existir) e marcar `clique_whatsapp` como conversão.

### Conteúdo
- /atendimentos/procedimentos-esteticos/: lista completa dos procedimentos, sem preço, com "após avaliação médica".
- Páginas de pele, cabelos e unhas: bloco "O que está incluso na consulta" (dermatoscopia e tricoscopia sem cobrança à parte) e links internos para as páginas de SJC.
- Home: FAQ com "O que está incluso na consulta" e "Qual é o valor da consulta", além de schema FAQPage.
- JSON-LD da home reescrito com as duas unidades, sem `medicalSpecialty`.

### Pendências marcadas no código
- **Horário de SJC:** as páginas dizem "durante a semana, com hora marcada". Assim que o horário real estiver confirmado (o perfil no Google mostra quinta-feira, 13h às 18h), trocar o texto e preencher `openingHoursSpecification` da unidade de SJC no JSON-LD da home. Buscar por `CONFIRMAR`.
- **Preço da consulta (versão B):** o bloco "Valor" das páginas novas traz um comentário HTML com o texto "R$ 289 no Pix ou R$ 299 no cartão". Publicar só com aprovação da Dra., trocando o parágrafo da versão A.
- **Fotos do Espaço Vitalle:** 8 a 12 fotos (fachada com o número 108, entrada, recepção, sala de consulta, equipamentos), sem pacientes, para /sjc/ e /contato/.
- **Estacionamento e como chegar em SJC:** ainda não descrito no site.

---

## 📸 Trocar a foto principal da Dra.

A foto aparece em três lugares (hero da home, bloco "Sobre a médica" e página /sobre/) e sempre pelos mesmos quatro arquivos. Para trocar:

```bash
pip3 install pillow
python3 scripts/atualizar-foto-dra.py ~/Downloads/nova-foto.jpg
```

Isso regenera, com recorte central 4:5:

```
assets/img/photos/dra-roberta-retrato-md.jpg    480 x 600
assets/img/photos/dra-roberta-retrato-md.webp   480 x 600
assets/img/photos/dra-roberta-retrato-lg.jpg    800 x 1000
assets/img/photos/dra-roberta-retrato-lg.webp   800 x 1000
```

Se o enquadramento sair ruim, use `--foco cima` ou `--foco baixo`. Nenhum HTML precisa ser alterado.
