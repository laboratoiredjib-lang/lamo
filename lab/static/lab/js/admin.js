/* Espace de gestion LAMO — petites interactions calquées sur le site public */
(function () {
  "use strict";

  /* Le script est chargé sans "defer" par Unfold (boucle SCRIPTS), donc
     exécuté avant que <body> n'existe : on attend le DOM avant d'agir. */
  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }

  function init() {
    var reduceMotion =
      window.matchMedia && window.matchMedia("(prefers-reduced-motion: reduce)").matches;

    /* Lueur qui suit le curseur sur les cartes du tableau de bord */
    document.querySelectorAll(".lamo-kpi-card").forEach(function (card) {
      card.addEventListener("mousemove", function (e) {
        var r = card.getBoundingClientRect();
        card.style.setProperty("--mx", ((e.clientX - r.left) / r.width) * 100 + "%");
        card.style.setProperty("--my", ((e.clientY - r.top) / r.height) * 100 + "%");
      });
    });

    /* Compteurs animés sur les cartes de statistiques */
    var counters = document.querySelectorAll(".lamo-kpi-value[data-count]");
    if (counters.length) {
      if (reduceMotion || !("IntersectionObserver" in window)) {
        counters.forEach(function (el) {
          el.textContent = el.getAttribute("data-count");
        });
      } else {
        var observer = new IntersectionObserver(function (entries) {
          entries.forEach(function (entry) {
            if (!entry.isIntersecting) return;
            observer.unobserve(entry.target);
            var el = entry.target;
            var target = parseInt(el.getAttribute("data-count"), 10) || 0;
            var start = null;
            var step = function (ts) {
              if (start === null) start = ts;
              var p = Math.min(1, (ts - start) / 1100);
              el.textContent = Math.round((1 - Math.pow(1 - p, 3)) * target);
              if (p < 1) requestAnimationFrame(step);
            };
            requestAnimationFrame(step);
          });
        }, { threshold: 0.4 });
        counters.forEach(function (el) { observer.observe(el); });
      }
    }

    /* Surface maillée animée derrière la page de connexion (même rendu que
       le canvas #hero-network du site public) */
    var cvs = document.getElementById("admin-login-network");
    if (cvs && cvs.getContext && !reduceMotion) {
      var ctx = cvs.getContext("2d");
      var W = 0, H = 0, raf = null;
      var dpr = Math.min(window.devicePixelRatio || 1, 2);

      var resize = function () {
        W = cvs.width = cvs.offsetWidth * dpr;
        H = cvs.height = cvs.offsetHeight * dpr;
      };
      resize();
      var rTimer;
      window.addEventListener("resize", function () {
        clearTimeout(rTimer);
        rTimer = setTimeout(resize, 150);
      }, { passive: true });

      var N = 26, M = 15;
      var z = function (u, v, t) {
        var cx = 0.5 + 0.22 * Math.sin(t * 0.00035);
        var cy = 0.45 + 0.12 * Math.cos(t * 0.00027);
        var g = Math.exp(-(Math.pow(u - cx, 2) / 0.09 + Math.pow(v - cy, 2) / 0.1));
        return 0.55 * g + 0.12 * Math.sin(6.28 * u * 2 + t * 0.0012) * Math.cos(6.28 * v + t * 0.0009);
      };
      var px = function (u, v) { return u * W * 1.15 - W * 0.07 + v * W * 0.06; };
      var py = function (v, h) { return H * 0.28 + v * H * 0.62 - h * H * 0.34; };

      var draw = function (now) {
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
      };
      raf = requestAnimationFrame(draw);
    }
  }
})();
