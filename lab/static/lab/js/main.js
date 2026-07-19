(function () {
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("main-nav");

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      var isOpen = nav.classList.toggle("is-open");
      toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    });
  }

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

  /* Illustration mathématique : effet de "dessin" au scroll (progressive enhancement) */
  var banner = document.querySelector(".math-banner");
  if (banner && "IntersectionObserver" in window) {
    var drawEls = banner.querySelectorAll(".draw");
    drawEls.forEach(function (el) {
      var len = 0;
      try { len = el.getTotalLength(); } catch (e) { return; }
      el.style.strokeDasharray = len;
      el.style.strokeDashoffset = len;
    });
    var bannerObserver = new IntersectionObserver(
      function (entries) {
        entries.forEach(function (entry) {
          if (entry.isIntersecting) {
            drawEls.forEach(function (el) { el.style.strokeDashoffset = 0; });
            bannerObserver.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.25 }
    );
    bannerObserver.observe(banner);
  }
})();
