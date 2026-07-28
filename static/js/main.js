(function () {
  'use strict';

  var burger = document.getElementById('navBurger');
  var menu = document.getElementById('navMenu');

  /* Mobil menyu ochish/yopish */
  if (burger && menu) {
    burger.addEventListener('click', function () {
      var open = menu.classList.toggle('is-open');
      burger.setAttribute('aria-expanded', open ? 'true' : 'false');
    });
    menu.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') {
        menu.classList.remove('is-open');
        burger.setAttribute('aria-expanded', 'false');
      }
    });
  }

  /* Scroll'da faol bo'limni belgilash */
  var sections = [], navLinks = [];
  document.querySelectorAll('.nav-menu a').forEach(function (a) {
    var href = a.getAttribute('href') || '';
    if (href.charAt(0) !== '#' || href.length < 2) return;
    var sec = document.querySelector(href);
    if (sec) { sections.push(sec); navLinks.push(a); }
  });

  function highlight() {
    var pos = window.scrollY + 120, current = -1;
    for (var i = 0; i < sections.length; i++) {
      if (sections[i].offsetTop <= pos) current = i;
    }
    for (var j = 0; j < navLinks.length; j++) {
      if (!navLinks[j].classList.contains('contact-link')) {
        navLinks[j].classList.toggle('is-active', j === current);
      }
    }
  }

  window.addEventListener('scroll', highlight, { passive: true });
  window.addEventListener('load', highlight);
  highlight();

  /* Flash xabarlarni avtomatik yashirish */
  setTimeout(function () {
    document.querySelectorAll('.flash-item').forEach(function (el) {
      el.style.transition = 'opacity .5s';
      el.style.opacity = '0';
      setTimeout(function () { el.remove(); }, 500);
    });
  }, 6000);
})();
