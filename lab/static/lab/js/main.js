/* ============================================================================
   LAMO — interactions du site
   1. En-tête, barre de progression, retour en haut
   2. Menu (desktop : survol / mobile : panneau + accordéons)
   3. Accordéons de contenu
   4. Apparitions au défilement (.reveal / .stagger)
   5. Tracé progressif des illustrations SVG
   6. Lueur au curseur sur les cartes
   7. Compteurs animés
   8. Carrousel photo des activités
   9. Visionneuse plein écran (lightbox)
  10. Surface maillée animée du héros (canvas)
  11. Inclinaison 3D de l'affiche
   ========================================================================= */
(function () {
  "use strict";

  var reduceMotion =
    window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;
  var finePointer = !window.matchMedia || window.matchMedia("(hover: hover)").matches;

  /* ---------------------------------------- 1. En-tête & progression */
  var header = document.querySelector(".site-header");
  var progress = document.getElementById("scroll-progress");
  var toTop = document.getElementById("to-top");

  function onScroll() {
    var y = window.scrollY;
    if (header) header.classList.toggle("is-scrolled", y > 24);
    if (progress) {
      var max = document.documentElement.scrollHeight - window.innerHeight;
      progress.style.width = (max > 0 ? Math.min(100, (y / max) * 100) : 0) + "%";
    }
    if (toTop) toTop.classList.toggle("is-visible", y > 600);
  }
  onScroll();
  window.addEventListener("scroll", onScroll, { passive: true });
  window.addEventListener("resize", onScroll, { passive: true });

  if (toTop) {
    toTop.addEventListener("click", function () {
      window.scrollTo({ top: 0, behavior: reduceMotion ? "auto" : "smooth" });
    });
  }

  /* ------------------------------------------------------ 2. Menu */
  var toggle = document.getElementById("nav-toggle");
  var nav = document.getElementById("main-nav");
  var backdrop = document.getElementById("nav-backdrop");

  function closeAllDropdowns() {
    document.querySelectorAll(".main-nav li.is-open").forEach(function (li) {
      li.classList.remove("is-open");
      var btn = li.querySelector("button");
      if (btn) btn.setAttribute("aria-expanded", "false");
    });
  }

  function setNavOpen(isOpen) {
    if (!nav || !toggle) return;
    nav.classList.toggle("is-open", isOpen);
    toggle.classList.toggle("is-open", isOpen);
    toggle.setAttribute("aria-expanded", isOpen ? "true" : "false");
    toggle.setAttribute("aria-label", isOpen ? "Fermer le menu" : "Ouvrir le menu");
    if (backdrop) backdrop.classList.toggle("is-open", isOpen);
    document.body.classList.toggle("nav-locked", isOpen);
    if (!isOpen) closeAllDropdowns();
  }

  if (toggle && nav) {
    toggle.addEventListener("click", function () {
      setNavOpen(!nav.classList.contains("is-open"));
    });
  }
  if (backdrop) backdrop.addEventListener("click", function () { setNavOpen(false); });
  document.addEventListener("keydown", function (e) {
    if (e.key === "Escape") { setNavOpen(false); closeAllDropdowns(); }
  });
  /* fermeture du panneau après un clic sur un lien (mobile) */
  if (nav) {
    nav.querySelectorAll("a").forEach(function (a) {
      a.addEventListener("click", function () { setNavOpen(false); });
    });
  }

  /* ouverture des sous-menus : accordéon (mobile) / bascule (desktop) */
  document.querySelectorAll(".has-dropdown > button").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var parent = btn.closest("li");
      var wasOpen = parent.classList.contains("is-open");
      closeAllDropdowns();
      if (!wasOpen) {
        parent.classList.add("is-open");
        btn.setAttribute("aria-expanded", "true");
      }
    });
  });
  document.addEventListener("click", function (e) {
    if (!e.target.closest(".has-dropdown") && !e.target.closest(".nav-toggle")) {
      if (!nav || !nav.classList.contains("is-open")) closeAllDropdowns();
    }
  });

  /* ------------------------------------------- 3. Accordéons de contenu */
  document.querySelectorAll(".accordion-toggle").forEach(function (btn) {
    btn.addEventListener("click", function () {
      var isOpen = btn.getAttribute("aria-expanded") === "true";
      var panel = btn.nextElementSibling;
      btn.setAttribute("aria-expanded", isOpen ? "false" : "true");
      if (panel) panel.hidden = isOpen;
    });
  });

  /* ------------------------------------ 4. Apparitions au défilement */
  document.querySelectorAll(".stagger").forEach(function (group) {
    Array.prototype.forEach.call(group.children, function (child, i) {
      child.style.setProperty("--i", i);
    });
  });
  document.querySelectorAll(".pipe-step").forEach(function (step, i) {
    step.style.setProperty("--i", i);
  });

  var revealTargets = document.querySelectorAll(".reveal, .stagger, .pipeline");
  if (revealTargets.length && "IntersectionObserver" in window && !reduceMotion) {
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
      if (rect.top < window.innerHeight * 0.95 && rect.bottom > 0) {
        el.classList.add("is-visible");
      } else {
        el.classList.add("reveal-js");
        observer.observe(el);
      }
    });
  } else {
    revealTargets.forEach(function (el) { el.classList.add("is-visible"); });
  }

  /* ------------------------------- 5. Tracé progressif des SVG */
  var drawContainers = document.querySelectorAll(".math-banner, .page-header-icon");
  if (drawContainers.length && "IntersectionObserver" in window && !reduceMotion) {
    drawContainers.forEach(function (container) {
      var drawEls = container.querySelectorAll(
        "svg path:not([fill]), svg line:not([fill]), svg polyline:not([fill]), " +
        "svg circle:not([fill]), svg ellipse:not([fill]), svg rect:not([fill]), svg .draw"
      );
      if (!drawEls.length) return;
      drawEls.forEach(function (el) {
        var len = 0;
        try { len = el.getTotalLength(); } catch (e) { return; }
        el.style.strokeDasharray = len;
        el.style.strokeDashoffset = len;
      });
      var reveal = function () {
        drawEls.forEach(function (el) { el.style.strokeDashoffset = 0; });
      };
      var rect = container.getBoundingClientRect();
      if (rect.top < window.innerHeight * 0.95 && rect.bottom > 0) {
        reveal();
      } else {
        var obs = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (entry.isIntersecting) { reveal(); obs.unobserve(entry.target); }
          });
        }, { threshold: 0.25 });
        obs.observe(container);
      }
    });
  }

  /* --------------------------------- 6. Lueur au curseur sur les cartes */
  if (finePointer && !reduceMotion) {
    document.querySelectorAll(
      ".team-card, .theme-card, .info-card, .pub-item, .thesis-card, .hdr-card, " +
      ".project-card, .axis-item, .news-card, .partner-tile, .course-card, .activity-feed-card"
    ).forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
      });
    });
  }

  /* ------------------------------------------------ 7. Compteurs animés */
  var counters = document.querySelectorAll(".num[data-count]");
  if (counters.length) {
    if (reduceMotion || !("IntersectionObserver" in window)) {
      counters.forEach(function (el) { el.textContent = el.getAttribute("data-count"); });
    } else {
      var cObs = new IntersectionObserver(function (entries) {
        entries.forEach(function (entry) {
          if (!entry.isIntersecting) return;
          cObs.unobserve(entry.target);
          var el = entry.target;
          var target = parseInt(el.getAttribute("data-count"), 10) || 0;
          var start = null;
          var step = function (ts) {
            if (start === null) start = ts;
            var p = Math.min(1, (ts - start) / 1500);
            el.textContent = Math.round((1 - Math.pow(1 - p, 3)) * target);
            if (p < 1) requestAnimationFrame(step);
          };
          requestAnimationFrame(step);
        });
      }, { threshold: 0.5 });
      counters.forEach(function (el) { cObs.observe(el); });
    }
  }

  /* -------------------------------------- 8. Carrousel des activités */
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
      requestAnimationFrame(function () { updateUI(); updating = false; });
    });
    var goTo = function (d) {
      carousel.scrollBy({ left: d * carousel.clientWidth, behavior: "smooth" });
    };
    if (prevBtn) prevBtn.addEventListener("click", function () { goTo(-1); });
    if (nextBtn) nextBtn.addEventListener("click", function () { goTo(1); });
    updateUI();
  });

  /* --------------------------------------------------- 9. Lightbox */
  var lightboxTriggers = document.querySelectorAll(
    ".activity-feed-media img, .news-media img, .member-hero-photo-compact img"
  );
  if (lightboxTriggers.length) {
    var lb = document.createElement("div");
    lb.className = "lightbox";
    lb.setAttribute("role", "dialog");
    lb.setAttribute("aria-modal", "true");
    lb.setAttribute("aria-label", "Aperçu de l'image");
    lb.innerHTML =
      '<button type="button" class="lightbox-close" aria-label="Fermer">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"><path d="M6 6l12 12M18 6L6 18"/></svg></button>' +
      '<button type="button" class="lightbox-nav lightbox-nav--prev" aria-label="Image précédente">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M15 18l-6-6 6-6"/></svg></button>' +
      '<button type="button" class="lightbox-nav lightbox-nav--next" aria-label="Image suivante">' +
      '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round"><path d="M9 18l6-6-6-6"/></svg></button>' +
      '<div class="lightbox-stage"><img class="lightbox-img" src="" alt=""></div>' +
      '<div class="lightbox-counter"></div>' +
      '<div class="lightbox-hint">Cliquer sur l\u2019image pour zoomer</div>';
    document.body.appendChild(lb);

    var lbStage = lb.querySelector(".lightbox-stage");
    var lbImg = lb.querySelector(".lightbox-img");
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
    var showImage = function (i) {
      lbIndex = (i + lbGroup.length) % lbGroup.length;
      resetZoom();
      lbImg.classList.remove("is-loaded");
      lbImg.src = lbGroup[lbIndex].src;
      lbImg.alt = lbGroup[lbIndex].alt || "";
      var multi = lbGroup.length > 1;
      lbPrev.hidden = !multi;
      lbNext.hidden = !multi;
      lbCounter.hidden = !multi;
      if (multi) lbCounter.textContent = lbIndex + 1 + " / " + lbGroup.length;
    };
    lbImg.addEventListener("load", function () { lbImg.classList.add("is-loaded"); });
    var closeLightbox = function () {
      lb.classList.remove("is-open");
      document.body.classList.remove("lightbox-locked");
      resetZoom();
    };
    lb.querySelector(".lightbox-close").addEventListener("click", closeLightbox);
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
        var scrollWrap = mediaWrap
          ? mediaWrap.querySelector(".activity-feed-media--carousel")
          : null;
        var groupEls = scrollWrap ? scrollWrap.querySelectorAll("img") : [image];
        lbGroup = Array.prototype.map.call(groupEls, function (el) {
          return { src: el.currentSrc || el.src, alt: el.alt };
        });
        var idx = Array.prototype.indexOf.call(groupEls, image);
        showImage(idx < 0 ? 0 : idx);
        lb.classList.add("is-open");
        document.body.classList.add("lightbox-locked");
      });
    });
  }

  /* -------------------------- 10. Surface maillée animée du héros */
  var cvs = document.getElementById("hero-network");
  if (cvs && cvs.getContext && !reduceMotion) {
    var ctx = cvs.getContext("2d");
    var W = 0, H = 0, raf = null;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);

    function resize() {
      W = cvs.width = cvs.offsetWidth * dpr;
      H = cvs.height = cvs.offsetHeight * dpr;
    }
    resize();
    var rTimer;
    window.addEventListener("resize", function () {
      clearTimeout(rTimer);
      rTimer = setTimeout(resize, 150);
    }, { passive: true });

    var N = 26, M = 15;
    function z(u, v, t) {
      var cx = 0.5 + 0.22 * Math.sin(t * 0.00035);
      var cy = 0.45 + 0.12 * Math.cos(t * 0.00027);
      var g = Math.exp(-(Math.pow(u - cx, 2) / 0.09 + Math.pow(v - cy, 2) / 0.1));
      return 0.55 * g + 0.12 * Math.sin(6.28 * u * 2 + t * 0.0012) * Math.cos(6.28 * v + t * 0.0009);
    }
    function px(u, v) { return u * W * 1.15 - W * 0.07 + v * W * 0.06; }
    function py(v, h) { return H * 0.28 + v * H * 0.62 - h * H * 0.34; }

    function draw(now) {
      ctx.clearRect(0, 0, W, H);
      ctx.lineWidth = Math.max(1, dpr * 0.8);
      var i, j, u, v, grad;
      for (j = 0; j <= M; j++) {
        v = j / M;
        grad = ctx.createLinearGradient(0, 0, W, 0);
        grad.addColorStop(0, "rgba(31,181,132," + (0.34 - v * 0.16) + ")");
        grad.addColorStop(0.55, "rgba(47,168,220," + (0.3 - v * 0.14) + ")");
        grad.addColorStop(1, "rgba(30,99,180," + (0.26 - v * 0.12) + ")");
        ctx.strokeStyle = grad;
        ctx.beginPath();
        for (i = 0; i <= N; i++) {
          u = i / N;
          var h = z(u, v, now);
          if (i) ctx.lineTo(px(u, v), py(v, h)); else ctx.moveTo(px(u, v), py(v, h));
        }
        ctx.stroke();
      }
      ctx.strokeStyle = "rgba(94,214,168,.10)";
      for (i = 0; i <= N; i += 2) {
        u = i / N;
        ctx.beginPath();
        for (j = 0; j <= M; j++) {
          v = j / M;
          var h2 = z(u, v, now);
          if (j) ctx.lineTo(px(u, v), py(v, h2)); else ctx.moveTo(px(u, v), py(v, h2));
        }
        ctx.stroke();
      }
      raf = requestAnimationFrame(draw);
    }

    if ("IntersectionObserver" in window) {
      new IntersectionObserver(function (entries) {
        entries.forEach(function (e) {
          if (e.isIntersecting) { if (!raf) raf = requestAnimationFrame(draw); }
          else { cancelAnimationFrame(raf); raf = null; }
        });
      }, { threshold: 0 }).observe(cvs);
    } else {
      raf = requestAnimationFrame(draw);
    }
  }

  /* ------------------------------- 11. Inclinaison 3D de l'affiche */
  var tiltWrap = document.querySelector(".hero-v3-media");
  var tiltFrame = document.querySelector(".hero-v3-media-frame");
  if (tiltWrap && tiltFrame && finePointer && !reduceMotion) {
    tiltWrap.addEventListener("mousemove", function (e) {
      var r = tiltWrap.getBoundingClientRect();
      var x = (e.clientX - r.left) / r.width - 0.5;
      var y = (e.clientY - r.top) / r.height - 0.5;
      tiltFrame.style.transform =
        "rotateY(" + (x * 9).toFixed(2) + "deg) rotateX(" + (-y * 9).toFixed(2) + "deg) translateZ(12px)";
    });
    tiltWrap.addEventListener("mouseleave", function () { tiltFrame.style.transform = ""; });
  }

  /* défilement infini du bandeau partenaires */
  var marquee = document.querySelector(".partner-marquee-track");
  if (marquee && !marquee.dataset.cloned) {
    marquee.innerHTML += marquee.innerHTML;
    marquee.dataset.cloned = "1";
  }
})();
