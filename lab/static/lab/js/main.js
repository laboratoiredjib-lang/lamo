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

  document.querySelectorAll(".accordion-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var isOpen = btn.getAttribute("aria-expanded") === "true";
      var panel = btn.nextElementSibling;
      btn.setAttribute("aria-expanded", isOpen ? "false" : "true");
      if (panel) panel.hidden = isOpen;
    });
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

  /* Lueur qui suit le curseur sur les cartes de contenu (accueil, activités, production, formations...). */
  document.querySelectorAll(
    ".team-card, .theme-card, .activity-card, .info-card, .pub-item, .thesis-card, " +
    ".hdr-card, .project-card, .axis-item, .news-card, .partner-tile, .activity-feed-card"
  ).forEach(function (card) {
    card.addEventListener("mousemove", function (e) {
      var rect = card.getBoundingClientRect();
      card.style.setProperty("--mx", ((e.clientX - rect.left) / rect.width * 100) + "%");
      card.style.setProperty("--my", ((e.clientY - rect.top) / rect.height * 100) + "%");
    });
  });

  /* Compteurs animés du hero (0 -> valeur cible), joués une fois au chargement. */
  var counters = document.querySelectorAll(".hero-v2-stat .num[data-count]");
  if (counters.length) {
    var animateCounter = function (el) {
      var target = parseInt(el.getAttribute("data-count"), 10) || 0;
      var start = null;
      var duration = 1200;
      var step = function (ts) {
        if (start === null) start = ts;
        var progress = Math.min(1, (ts - start) / duration);
        var eased = 1 - Math.pow(1 - progress, 3);
        el.textContent = Math.round(eased * target);
        if (progress < 1) requestAnimationFrame(step);
      };
      requestAnimationFrame(step);
    };
    if (window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches) {
      counters.forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
    } else {
      window.setTimeout(function () {
        counters.forEach(animateCounter);
      }, 550);
    }
  }

  /* Carrousel photo des activités : compteur "n / total", boutons précédent/suivant et défilement à la molette. */
  document.querySelectorAll(".activity-feed-media--carousel").forEach(function (carousel) {
    var wrap = carousel.parentElement;
    var counter = wrap.querySelector(".activity-feed-count");
    var prevBtn = wrap.querySelector(".activity-feed-nav--prev");
    var nextBtn = wrap.querySelector(".activity-feed-nav--next");
    var total = carousel.querySelectorAll("img").length;
    if (!total) return;

    var updateUI = function () {
      var index = Math.round(carousel.scrollLeft / carousel.clientWidth) + 1;
      index = Math.max(1, Math.min(total, index));
      if (counter) counter.textContent = index + " / " + total;
      if (prevBtn) prevBtn.disabled = index <= 1;
      if (nextBtn) nextBtn.disabled = index >= total;
    };

    var updating = false;
    carousel.addEventListener("scroll", function () {
      if (updating) return;
      updating = true;
      requestAnimationFrame(function () {
        updateUI();
        updating = false;
      });
    });

    var goTo = function (delta) {
      carousel.scrollBy({ left: delta * carousel.clientWidth, behavior: "smooth" });
    };
    if (prevBtn) prevBtn.addEventListener("click", function () { goTo(-1); });
    if (nextBtn) nextBtn.addEventListener("click", function () { goTo(1); });

    updateUI();
  });

  /* Lightbox : agrandissement et zoom des images (activités, formations, partenaires, actualités...). */
  var lightboxTriggers = document.querySelectorAll(".activity-feed-media img, .news-media img");
  if (lightboxTriggers.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Aperçu de l'image");
    lb.innerHTML =
      '<button type="button" class="lightbox-close" aria-label="Fermer">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg>' +
      '</button>' +
      '<button type="button" class="lightbox-nav lightbox-nav--prev" aria-label="Image précédente">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg>' +
      '</button>' +
      '<button type="button" class="lightbox-nav lightbox-nav--next" aria-label="Image suivante">' +
        '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg>' +
      '</button>' +
      '<div class="lightbox-stage"><img class="lightbox-img" src="" alt=""></div>' +
      '<div class="lightbox-counter"></div>' +
      '<div class="lightbox-hint">Cliquer sur l’image pour zoomer</div>';
    document.body.appendChild(lb);

    var lbStage = lb.querySelector(".lightbox-stage");
    var lbImg = lb.querySelector(".lightbox-img");
    var lbClose = lb.querySelector(".lightbox-close");
    var lbPrev = lb.querySelector(".lightbox-nav--prev");
    var lbNext = lb.querySelector(".lightbox-nav--next");
    var lbCounter = lb.querySelector(".lightbox-counter");
    var lbGroup = [];
    var lbIndex = 0;

    var resetZoom = function () {
      lbImg.classList.remove("is-zoomed");
      lbImg.style.width = "";
      lbImg.style.maxWidth = "";
    };

    var showImage = function (index) {
      lbIndex = (index + lbGroup.length) % lbGroup.length;
      resetZoom();
      lbImg.classList.remove("is-loaded");
      lbImg.src = lbGroup[lbIndex].src;
      lbImg.alt = lbGroup[lbIndex].alt || "";
      var multi = lbGroup.length > 1;
      lbPrev.hidden = !multi;
      lbNext.hidden = !multi;
      lbCounter.hidden = !multi;
      if (multi) lbCounter.textContent = (lbIndex + 1) + " / " + lbGroup.length;
    };
    lbImg.addEventListener("load", function () { lbImg.classList.add("is-loaded"); });

    var openLightbox = function (group, index) {
      lbGroup = group;
      showImage(index);
      lb.classList.add("is-open");
      document.body.classList.add("lightbox-locked");
    };
    var closeLightbox = function () {
      lb.classList.remove("is-open");
      document.body.classList.remove("lightbox-locked");
      resetZoom();
    };

    lbClose.addEventListener("click", closeLightbox);
    lb.addEventListener("click", function (e) {
      if (e.target === lb || e.target === lbStage) closeLightbox();
    });
    lbPrev.addEventListener("click", function () { showImage(lbIndex - 1); });
    lbNext.addEventListener("click", function () { showImage(lbIndex + 1); });
    lbImg.addEventListener("click", function (e) {
      e.stopPropagation();
      if (lbImg.classList.contains("is-zoomed")) {
        resetZoom();
      } else {
        lbImg.classList.add("is-zoomed");
        lbImg.style.maxWidth = "none";
        lbImg.style.width = Math.round((lbImg.naturalWidth || 1200) * 1.7) + "px";
      }
    });
    document.addEventListener("keydown", function (e) {
      if (!lb.classList.contains("is-open")) return;
      if (e.key === "Escape") closeLightbox();
      if (e.key === "ArrowLeft") showImage(lbIndex - 1);
      if (e.key === "ArrowRight") showImage(lbIndex + 1);
    });

    lightboxTriggers.forEach(function (image) {
      image.addEventListener("click", function () {
        var mediaWrap = image.closest(".activity-feed-media, .news-media");
        var scrollWrap = mediaWrap ? mediaWrap.querySelector(".activity-feed-media--carousel") : null;
        var groupEls = scrollWrap ? scrollWrap.querySelectorAll("img") : [image];
        var group = Array.prototype.map.call(groupEls, function (el) {
          return { src: el.currentSrc || el.src, alt: el.alt };
        });
        var idx = Array.prototype.indexOf.call(groupEls, image);
        openLightbox(group, idx < 0 ? 0 : idx);
      });
    });
  }
})();
