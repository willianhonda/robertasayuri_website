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

  /* ---------- 4. Cookie banner (LGPD) ---------- */
  const COOKIE_KEY = 'rs-cookie-consent';
  const banner   = document.querySelector('[data-cookie-banner]');
  const accept   = document.querySelector('[data-cookie-accept]');
  const decline  = document.querySelector('[data-cookie-decline]');

  if (banner) {
    const consent = localStorage.getItem(COOKIE_KEY);
    if (!consent) {
      setTimeout(function () { banner.classList.add('is-visible'); }, 1200);
    }

    if (accept) accept.addEventListener('click', function () {
      localStorage.setItem(COOKIE_KEY, 'accepted');
      banner.classList.remove('is-visible');
    });

    if (decline) decline.addEventListener('click', function () {
      localStorage.setItem(COOKIE_KEY, 'declined');
      banner.classList.remove('is-visible');
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
    }, { threshold: 0.12, rootMargin: '0px 0px -80px 0px' });

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

  /* ---------- 7. WhatsApp click tracking (placeholder para analytics) ---------- */
  document.querySelectorAll('a[href*="wa.me"]').forEach(function (link) {
    link.addEventListener('click', function () {
      if (window.gtag) {
        window.gtag('event', 'whatsapp_click', {
          event_category: 'engagement',
          event_label: link.dataset.source || 'unknown'
        });
      }
    });
  });
})();
