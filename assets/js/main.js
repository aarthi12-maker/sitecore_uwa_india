/* UWA India — shared navigation and carousel behaviour (no dependencies) */
(function () {
  "use strict";

  /* ---------- Header: menu + search toggles ---------- */
  function toggle(btn, panel, onOpen) {
    if (!btn || !panel) return;
    btn.addEventListener("click", function () {
      var open = btn.getAttribute("aria-expanded") !== "true";
      btn.setAttribute("aria-expanded", String(open));
      panel.classList.toggle("is-open", open);
      if (open && onOpen) onOpen();
    });
  }
  var menuBtn = document.querySelector(".icon-btn--menu");
  var searchBtn = document.querySelector(".icon-btn--search");
  toggle(menuBtn, document.getElementById("site-nav"));
  toggle(searchBtn, document.getElementById("site-search"), function () {
    document.getElementById("site-search-input").focus();
  });

  /* ---------- Why Choose carousel progress ---------- */
  var track = document.querySelector(".why__track");
  var bar = document.querySelector(".why__progress-bar");
  if (track && bar) {
    var cards = track.children.length;
    var updateBar = function () {
      /* one segment per card, like the design (1 of 4 = 25%) */
      var max = track.scrollWidth - track.clientWidth;
      var ratio = max > 0 ? track.scrollLeft / max : 0;
      bar.style.width = 100 / cards + "%";
      bar.style.transform = "translateX(" + ratio * (cards - 1) * 100 + "%)";
      bar.parentElement.style.visibility = max > 1 ? "visible" : "hidden";
    };
    track.addEventListener("scroll", updateBar, { passive: true });
    window.addEventListener("resize", updateBar);
    updateBar();
  }

  /* ---------- Footer country switcher ---------- */
  var countryBtn = document.querySelector(".country__btn");
  var countryMenu = document.getElementById("country-menu");
  if (countryBtn && countryMenu) countryBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = countryMenu.hidden;
    countryMenu.hidden = !open;
    countryBtn.setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("click", function () {
    if (!countryBtn || !countryMenu) return;
    countryMenu.hidden = true;
    countryBtn.setAttribute("aria-expanded", "false");
  });

  /* Escape closes navigation and search and restores focus. */
  document.addEventListener("keydown", function (event) {
    if (event.key !== "Escape") return;
    var active = document.activeElement;
    var nav = document.getElementById("site-nav");
    var search = document.getElementById("site-search");
    var inNav = nav && nav.contains(active);
    var inSearch = search && search.contains(active);
    [menuBtn, searchBtn].forEach(function (btn) {
      if (!btn) return;
      btn.setAttribute("aria-expanded", "false");
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      if (panel) panel.classList.remove("is-open");
    });
    if (inNav) menuBtn.focus();
    if (inSearch) searchBtn.focus();
  });
})();
