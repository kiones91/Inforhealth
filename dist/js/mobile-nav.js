(function () {
  function initMobileNav() {
    var toggle = document.querySelector('.site-nav-toggle');
    var drawer = document.getElementById('site-mobile-nav');
    var desktop = document.querySelector('.site-nav-desktop');
    var panel = drawer && drawer.querySelector('.site-mobile-nav-panel');
    var linksContainer = drawer && drawer.querySelector('.site-mobile-nav-links');
    var closeBtn = drawer && drawer.querySelector('.site-mobile-nav-close');

    if (!toggle || !drawer || !linksContainer || !panel) return;

    if (!linksContainer.children.length && desktop) {
      desktop.querySelectorAll('a').forEach(function (link) {
        var clone = link.cloneNode(true);
        clone.className = 'site-mobile-nav-link';
        if (link.getAttribute('aria-current')) {
          clone.setAttribute('aria-current', 'page');
        }
        linksContainer.appendChild(clone);
      });
    }

    var lastFocus = null;

    function setInert(state) {
      if ('inert' in HTMLElement.prototype) {
        drawer.inert = state;
      }
    }

    function openNav() {
      lastFocus = document.activeElement;
      drawer.classList.add('is-open');
      drawer.setAttribute('aria-hidden', 'false');
      toggle.setAttribute('aria-expanded', 'true');
      document.body.classList.add('site-nav-open');
      setInert(false);
      if (closeBtn) closeBtn.focus();
    }

    function closeNav() {
      drawer.classList.remove('is-open');
      drawer.setAttribute('aria-hidden', 'true');
      toggle.setAttribute('aria-expanded', 'false');
      document.body.classList.remove('site-nav-open');
      setInert(true);
      if (lastFocus && typeof lastFocus.focus === 'function') {
        lastFocus.focus();
      } else {
        toggle.focus();
      }
    }

    toggle.addEventListener('click', function () {
      if (drawer.classList.contains('is-open')) closeNav();
      else openNav();
    });

    drawer.querySelectorAll('[data-mobile-nav-close]').forEach(function (el) {
      el.addEventListener('click', closeNav);
    });

    linksContainer.addEventListener('click', function (e) {
      if (e.target.closest('a')) closeNav();
    });

    document.addEventListener('keydown', function (e) {
      if (e.key === 'Escape' && drawer.classList.contains('is-open')) {
        e.preventDefault();
        closeNav();
      }
    });

    window.addEventListener('resize', function () {
      if (window.matchMedia('(min-width: 1024px)').matches && drawer.classList.contains('is-open')) {
        closeNav();
      }
    });

    setInert(true);
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initMobileNav);
  } else {
    initMobileNav();
  }
})();
