(function () {
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("main-nav");
  var backdrop = document.getElementById("nav-backdrop");

  function setNavOpen(isOpen) {
    nav.classList.toggle("is-open", isOpen);
    toggle.classList.toggle("is-open", isOpen);
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    toggle.setAttribute("aria-label", isOpen ? "Fermer le menu" : "Ouvrir le menu");
    if (backdrop) backdrop.classList.toggle("is-open", isOpen);
    document.body.classList.toggle("nav-locked", isOpen);
    if (!isOpen) {
      document.querySelectorAll(".main-nav li.is-open").forEach(function (li) {
        li.classList.remove("is-open");
      });
    }
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("is-open"));
    });
  }
  if (backdrop) {
    backdrop.addEventListener("click", function () { setNavOpen(false); });
  }
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") setNavOpen(false);
  });

  document.querySelectorAll(".has-dropdown > button").forEach(function (btn) {
    btn.addEventListener("click", function (e) {
      var parent = btn.closest("li");
      var wasOpen = parent.classList.contains("is-open");
      document.querySelectorAll(".main-nav li.is-open").forEach(function (li) {
        li.classList.remove("is-open");
      });
      if (!wasOpen) parent.classList.add("is-open");
    });
  });

  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-dropdown")) {
      document.querySelectorAll(".main-nav li.is-open").forEach(function (li) {
        li.classList.remove("is-open");
      });
    }
  });

  /* Scroll reveal: fade-up for .reveal, cascading fade-up for children of .stagger */
  document.querySelectorAll(".stagger").forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty("--i", i);
    });
  });

  var revealTargets = document.querySelectorAll(".reveal, .stagger");
  if (revealTargets.length && "IntersectionObserver" in window) {
    var observer = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            entry.target.classList.add("is-visible");
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0, rootMargin: "0px 0px -8% 0px" }
    );
    revealTargets.forEach(function (el) {
      var rect = el.getBoundingClientRect();
      var alreadyInView = rect.top < window.innerHeight * 0.95 && rect.bottom > 0;
      if (alreadyInView) {
        el.classList.add("is-visible");
      } else {
        el.classList.add("reveal-js");
        observer.observe(el);
      }
    });
  } else {
    revealTargets.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* Illustrations SVG : effet de "dessin" au scroll/chargement (progressive enhancement).
     S'applique au bandeau mathématique et à chaque icône de bannière de page :
     tout élément à contour (sans attribut fill propre, donc hérité de fill="none")
     est traité comme un trait à dessiner ; les points pleins (accent) restent statiques. */
  var drawContainers = document.querySelectorAll(".math-banner, .page-header-icon");
  if (drawContainers.length && "IntersectionObserver" in window) {
    drawContainers.forEach(function (container) {
      var drawEls = container.querySelectorAll(
        "svg path:not([fill]), svg line:not([fill]), svg polyline:not([fill]), svg circle:not([fill]), svg ellipse:not([fill]), svg .draw"
      );
      if (!drawEls.length) return;
      drawEls.forEach(function (el) {
        var len = 0;
        try { len = el.getTotalLength(); } catch (e) { return; }
        el.style.strokeDasharray = len;
        el.style.strokeDashoffset = len;
      });
      var rect = container.getBoundingClientRect();
      var alreadyInView = rect.top < window.innerHeight * 0.95 && rect.bottom > 0;
      var reveal = function () {
        drawEls.forEach(function (el) { el.style.strokeDashoffset = 0; });
      };
      if (alreadyInView) {
        reveal();
      } else {
        var obs = new IntersectionObserver(
          function (entries) {
            entries.forEach(function (entry) {
              if (entry.isIntersecting) { reveal(); obs.unobserve(entry.target); }
            });
          },
          { threshold: 0.25 }
        );
        obs.observe(container);
      }
    });
  }
})();
