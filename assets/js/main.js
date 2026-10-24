/* =========================================================
   Roberta Sayuri — Interações
   ========================================================= */

(function () {
  'use strict';

  /* ---------- 1. Menu mobile ---------- */
  const navToggle = document.querySelector('[data-nav-toggle]');
  const navMenu   = document.querySelector('[data-nav-menu]');

  if (navToggle && navMenu) {
    navToggle.addEventListener('click', function () {
      const isOpen = navMenu.classList.toggle('is-open');
      navToggle.setAttribute('aria-expanded', isOpen);
    });

    // Fecha ao clicar em um link
    navMenu.querySelectorAll('a').forEach(function (link) {
      link.addEventListener('click', function () {
        navMenu.classList.remove('is-open');
        navToggle.setAttribute('aria-expanded', 'false');
      });
    });
  }

  /* ---------- 2. Header com sombra ao rolar ---------- */
  const header = document.querySelector('.site-header');
  if (header) {
    const onScroll = function () {
      header.classList.toggle('is-scrolled', window.scrollY > 8);
    };
    window.addEventListener('scroll', onScroll, { passive: true });
    onScroll();
  }

  /* ---------- 3. FAQ accordion ---------- */
  document.querySelectorAll('[data-faq-item]').forEach(function (item) {
    const button = item.querySelector('[data-faq-question]');
    if (!button) return;

    button.addEventListener('click', function () {
      const isOpen = item.classList.toggle('is-open');
      button.setAttribute('aria-expanded', isOpen);
    });
  });

  /* ---------- 4. Cookie banner (LGPD) e Google Analytics 4 ---------- */
  // ID da propriedade GA4 (G-XXXXXXXXXX). Vazio = analytics desligado.
  // O gtag.js só é carregado depois que o visitante aceita os cookies analíticos.
  const GA_ID = 'G-QX7GF6W65P';
  const COOKIE_KEY = 'rs-cookie-consent';
  const banner   = document.querySelector('[data-cookie-banner]');
  const accept   = document.querySelector('[data-cookie-accept]');
  const decline  = document.querySelector('[data-cookie-decline]');

  const lerConsentimento = function () {
    try { return localStorage.getItem(COOKIE_KEY); } catch (e) { return null; }
  };
  const gravarConsentimento = function (valor) {
    try { localStorage.setItem(COOKIE_KEY, valor); } catch (e) {}
  };

  var carregaAnalytics = function () {
    if (!GA_ID || window.gtag) return;
    window.dataLayer = window.dataLayer || [];
    window.gtag = function () { window.dataLayer.push(arguments); };
    window.gtag('js', new Date());
    window.gtag('config', GA_ID);
    var s = document.createElement('script');
    s.async = true;
    s.src = 'https://www.googletagmanager.com/gtag/js?id=' + GA_ID;
    document.head.appendChild(s);
  };

  if (lerConsentimento() === 'accepted') carregaAnalytics();

  if (banner) {
    var abreBanner = function () {
      banner.classList.add('is-visible');
      document.body.classList.add('cookie-aberto');
    };

    if (!lerConsentimento()) setTimeout(abreBanner, 1200);

    var fechaBanner = function () {
      banner.classList.remove('is-visible');
      document.body.classList.remove('cookie-aberto');
    };

    if (accept) accept.addEventListener('click', function () {
      gravarConsentimento('accepted');
      fechaBanner();
      carregaAnalytics();
    });

    if (decline) decline.addEventListener('click', function () {
      gravarConsentimento('declined');
      fechaBanner();
      // Se o analytics já estava carregado, a recusa vale a partir da próxima página
      if (window.gtag) window.gtag('consent', 'update', { analytics_storage: 'denied' });
    });

    // Link "Alterar preferências de cookies" (Política de Privacidade)
    document.querySelectorAll('[data-cookie-reset]').forEach(function (el) {
      el.addEventListener('click', function (e) {
        e.preventDefault();
        abreBanner();
      });
    });
  }

  /* ---------- 5. Reveal on scroll ---------- */
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(function (entries) {
      entries.forEach(function (entry) {
        if (entry.isIntersecting) {
          entry.target.classList.add('is-visible');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0, rootMargin: '0px 0px -40px 0px' });

    document.querySelectorAll('.reveal').forEach(function (el) {
      observer.observe(el);
    });
  } else {
    document.querySelectorAll('.reveal').forEach(function (el) {
      el.classList.add('is-visible');
    });
  }

  /* ---------- 6. Active nav link ---------- */
  const currentPath = window.location.pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
  document.querySelectorAll('.nav__link').forEach(function (link) {
    const linkPath = new URL(link.href, window.location.origin).pathname.replace(/\/index\.html$/, '/').replace(/\/$/, '') || '/';
    if (linkPath === currentPath) {
      link.classList.add('is-active');
      link.setAttribute('aria-current', 'page');
    }
  });

  /* ---------- 7. Eventos de clique para o GA4 ---------- */
  // O clique no WhatsApp (clique_whatsapp) é medido pelo script inline de cada página.
  const unidadeDaPagina = function () {
    const p = window.location.pathname;
    if (/guaianases/.test(p)) return 'guaianases';
    if (/sjc|sao-jose/.test(p)) return 'sjc';
    return '';
  };

  const EVENTOS = [
    { evento: 'clique_telefone',  teste: /^tel:/ },
    { evento: 'clique_rota',      teste: /google\.[^/]+\/maps|maps\.app\.goo\.gl|goo\.gl\/maps/ },
    { evento: 'clique_perfil_google', teste: /share\.google|g\.page|kgmid=/ },
    { evento: 'clique_instagram', teste: /instagram\.com/ }
  ];

  document.addEventListener('click', function (e) {
    const link = e.target.closest && e.target.closest('a[href]');
    if (!link || !window.gtag) return;
    const href = link.getAttribute('href');
    for (var i = 0; i < EVENTOS.length; i++) {
      if (EVENTOS[i].teste.test(href)) {
        window.gtag('event', EVENTOS[i].evento, {
          unidade: link.dataset.unidade || unidadeDaPagina(),
          pagina: window.location.pathname,
          link_url: href
        });
        return;
      }
    }
  });
})();
