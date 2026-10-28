/* Light by day, dark by night (local time 6:00 to 18:00 is light). Once a visitor uses the toggle, their choice is saved and always wins. */
(function () {
  var KEY = 'disclosure-theme', root = document.documentElement, saved = null;
  try { saved = localStorage.getItem(KEY); } catch (e) {}
  function auto() { var h = new Date().getHours(); return (h >= 6 && h < 18) ? 'light' : 'dark'; }
  function apply(t) {
    root.setAttribute('data-theme', t);
    root.style.colorScheme = t;
    var m = document.querySelector('meta[name="theme-color"]');
    if (m) m.setAttribute('content', t === 'dark' ? '#0a0a0a' : '#f1ede4');
  }
  apply(saved === 'light' || saved === 'dark' ? saved : auto());
  function mount() {
    if (document.getElementById('themeBtn')) return;
    var b = document.createElement('button');
    b.id = 'themeBtn'; b.type = 'button';
    function paint() {
      var dark = root.getAttribute('data-theme') === 'dark';
      b.setAttribute('aria-label', dark ? 'Switch to light mode' : 'Switch to dark mode');
      b.title = dark ? 'Switch to light mode. Your choice is remembered.' : 'Switch to dark mode. Your choice is remembered.';
      b.innerHTML = dark
        ? '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="4"/><path d="M12 2v3M12 19v3M2 12h3M19 12h3M4.9 4.9l2.1 2.1M17 17l2.1 2.1M4.9 19.1L7 17M17 7l2.1-2.1"/></svg>'
        : '<svg viewBox="0 0 24 24" width="18" height="18" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M21 12.8A9 9 0 1 1 11.2 3a7 7 0 0 0 9.8 9.8z"/></svg>';
    }
    b.addEventListener('click', function () {
      var next = root.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
      apply(next); paint();
      try { localStorage.setItem(KEY, next); } catch (e) {}
    });
    paint();
    document.body.appendChild(b);
  }
  if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', mount); else mount();
})();
