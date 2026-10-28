/* Motion and polish for the whole site: reveal on scroll, reading progress, card tilt, count-up numbers, checklist on cheat sheets, map tooltips. Respects prefers-reduced-motion. */
(function () {
  var root = document.documentElement, idx = root.classList.contains('idx');
  var rm = matchMedia('(prefers-reduced-motion: reduce)').matches, coarse = matchMedia('(pointer: coarse)').matches;
  root.classList.add('fx'); if (rm) root.classList.add('fx-rm');
  function ready(f) { if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', f); else f(); }
  ready(function () {
    var io = 'IntersectionObserver' in window ? new IntersectionObserver(function (es) {
      es.forEach(function (e) { if (e.isIntersecting) { e.target.classList.add('fx-in'); io.unobserve(e.target); } });
    }, { threshold: 0.12, rootMargin: '0px 0px -6% 0px' }) : null;

    var SEL = '.cscard,.sgc,.evc,.evcrit>div,.evprom>div,.evsteps li,.csstep,.csweek,.cgb,.cgp a,.cevl a,.pwl a,.pwbox,.fgq,.shr a,.shim figure,.msg,.shq,.evstats>div,.cgpdf a,.fgnote,.evmapw,.qidx,main h2';
    function scan(scope) {
      if (idx || !io) return;
      var groups = new Map();
      (scope || document).querySelectorAll(SEL).forEach(function (el) {
        if (el.__fx) return; el.__fx = 1;
        var p = el.parentElement, n = groups.get(p) || 0; groups.set(p, n + 1);
        el.classList.add('fx-r'); el.style.setProperty('--d', Math.min(n, 7) * 70 + 'ms');
        io.observe(el);
      });
      (scope || document).querySelectorAll('.evd').forEach(function (d, i) { d.style.setProperty('--i', i); });
    }
    scan();
    var fb = document.getElementById('faq-body');
    if (fb) new MutationObserver(function () { scan(fb); }).observe(fb, { childList: true });

    /* images fade in once loaded */
    if (!idx) {
      var imgs = [].slice.call(document.querySelectorAll('picture img'));
      imgs.forEach(function (im) { if (im.complete && im.naturalWidth) im.classList.add('fx-l'); else im.addEventListener('load', function () { im.classList.add('fx-l'); }); });
      setTimeout(function () { imgs.forEach(function (im) { im.classList.add('fx-l'); }); }, 4500);
    }

    if (rm) return;

    /* reading progress and back to top (not on the front page, which has its own) */
    if (!idx) {
      var bar = document.createElement('div'); bar.id = 'fxbar'; document.body.appendChild(bar);
      var top = document.createElement('button'); top.id = 'fxtop'; top.type = 'button'; top.setAttribute('aria-label', 'Back to the top');
      top.innerHTML = '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 19V5M5 12l7-7 7 7"/></svg>';
      top.addEventListener('click', function () { scrollTo({ top: 0, behavior: 'smooth' }); });
      document.body.appendChild(top);
      var tick = false;
      function onScroll() {
        if (tick) return; tick = true;
        requestAnimationFrame(function () {
          var h = document.documentElement.scrollHeight - innerHeight, y = scrollY;
          bar.style.transform = 'scaleX(' + (h > 0 ? Math.min(1, y / h) : 0) + ')';
          top.classList.toggle('on', y > 900); tick = false;
        });
      }
      addEventListener('scroll', onScroll, { passive: true }); onScroll();
    }

    /* card tilt toward the pointer (mouse only) */
    if (!coarse) {
      var TILT = '.cscard,.sgc,.evc .evi,.cgp a';
      document.addEventListener('pointermove', function (e) {
        if (e.pointerType !== 'mouse') return;
        var t = e.target.closest && e.target.closest(TILT); if (!t) return;
        var r = t.getBoundingClientRect(), x = (e.clientX - r.left) / r.width - .5, y = (e.clientY - r.top) / r.height - .5;
        t.classList.add('fx-tilt'); t.style.setProperty('--ry', (x * 5).toFixed(2) + 'deg'); t.style.setProperty('--rx', (-y * 4).toFixed(2) + 'deg'); t.style.setProperty('--ty', '-3px');
      }, { passive: true });
      document.addEventListener('pointerout', function (e) {
        var t = e.target.closest && e.target.closest(TILT); if (!t || (e.relatedTarget && t.contains(e.relatedTarget))) return;
        t.style.setProperty('--ry', '0deg'); t.style.setProperty('--rx', '0deg'); t.style.setProperty('--ty', '0px');
      }, { passive: true });
    }

    /* numbers count up when they arrive */
    document.querySelectorAll('.evstats b').forEach(function (b) {
      var end = parseInt(b.textContent, 10); if (!end) return; b.textContent = '0';
      var go = new IntersectionObserver(function (es) {
        if (!es[0].isIntersecting) return; go.disconnect(); var t0 = performance.now();
        (function step(t) { var k = Math.min(1, (t - t0) / 1100), e = 1 - Math.pow(1 - k, 3); b.textContent = Math.round(end * e); if (k < 1) requestAnimationFrame(step); })(t0);
      }, { threshold: 0.5 }); go.observe(b);
    });

    /* checklist on the cheat sheets: tick things off, saved on this device only */
    var steps = [].slice.call(document.querySelectorAll('.cssteps .csstep'));
    if (steps.length) {
      var key = 'disclosure-check-' + location.pathname.replace(/\W+/g, '-'), saved = [];
      try { saved = JSON.parse(localStorage.getItem(key) || '[]'); } catch (e) {}
      var prog = document.createElement('div'); prog.className = 'fxprog noprint'; prog.innerHTML = '<span></span><i><b></b></i>';
      steps[0].parentNode.parentNode.insertBefore(prog, steps[0].parentNode);
      function paintProg() {
        var n = steps.filter(function (s) { return s.classList.contains('done'); }).length;
        prog.firstChild.textContent = n === steps.length ? 'All done. That is the practice.' : n + ' of ' + steps.length + ' done';
        prog.querySelector('b').style.width = (100 * n / steps.length) + '%';
        try { localStorage.setItem(key, JSON.stringify(steps.map(function (s, i) { return s.classList.contains('done') ? i : -1; }).filter(function (i) { return i >= 0; }))); } catch (e) {}
      }
      steps.forEach(function (s, i) {
        s.setAttribute('role', 'checkbox'); s.setAttribute('tabindex', '0'); s.setAttribute('aria-checked', saved.indexOf(i) > -1 ? 'true' : 'false');
        if (saved.indexOf(i) > -1) s.classList.add('done');
        function tog() { s.classList.toggle('done'); s.setAttribute('aria-checked', s.classList.contains('done') ? 'true' : 'false'); paintProg(); }
        s.addEventListener('click', function (e) { if (e.target.closest('a')) return; tog(); });
        s.addEventListener('keydown', function (e) { if (e.key === ' ' || e.key === 'Enter') { e.preventDefault(); tog(); } });
      });
      paintProg();
    }

    /* map: name appears beside the pointer */
    var map = document.querySelector('.evmapw');
    if (map) {
      var tip = document.createElement('div'); tip.className = 'evtip'; tip.setAttribute('aria-hidden', 'true'); document.body.appendChild(tip);
      map.querySelectorAll('.evd').forEach(function (d) { var t = d.querySelector('title'); if (t) { d.setAttribute('aria-label', t.textContent); d.dataset.tip = t.textContent; t.remove(); } });
      map.addEventListener('pointermove', function (e) {
        var d = e.target.closest && e.target.closest('.evd');
        if (!d) { tip.classList.remove('on'); return; }
        tip.textContent = d.dataset.tip; tip.classList.add('on');
        tip.style.left = Math.min(innerWidth - tip.offsetWidth - 10, e.clientX + 14) + 'px'; tip.style.top = (e.clientY + 16) + 'px';
      }, { passive: true });
      map.addEventListener('pointerleave', function () { tip.classList.remove('on'); });
    }
  });

  /* front page: the woodcuts drift a little against the scroll */
  if (idx && !rm) {
    var pend = false;
    function par() {
      pend = false; var h = innerHeight;
      document.querySelectorAll('section.in figure img, section figure img').forEach(function (im) {
        var r = im.getBoundingClientRect(); if (r.bottom < -40 || r.top > h + 40) return;
        im.style.setProperty('--py', (((r.top + r.height / 2) - h / 2) / h * -14).toFixed(1) + 'px');
      });
    }
    addEventListener('scroll', function () { if (!pend) { pend = true; requestAnimationFrame(par); } }, { passive: true });
  }
})();
