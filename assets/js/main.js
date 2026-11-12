/* UWA India — shared navigation and carousel behaviour (no dependencies) */
(function () {
  "use strict";

  /* ---------- Header: menu + search toggles ---------- */
  var menuBtn = document.querySelector(".icon-btn--menu");
  var searchBtn = document.querySelector(".icon-btn--search");
  var nav = document.getElementById("site-nav");
  var search = document.getElementById("site-search");
  var desktopNav = window.matchMedia("(min-width: 1100px)");
  function setPanel(btn, panel, open) {
    if (!btn || !panel) return;
    btn.setAttribute("aria-expanded", String(open));
    btn.setAttribute("aria-label", (open ? "Close " : "Open ") + (btn === menuBtn ? "menu" : "search"));
    panel.classList.toggle("is-open", open);
  }
  if (menuBtn && nav) menuBtn.addEventListener("click", function () {
    var open = menuBtn.getAttribute("aria-expanded") !== "true";
    setPanel(searchBtn, search, false);
    setPanel(menuBtn, nav, open);
  });
  if (searchBtn && search) searchBtn.addEventListener("click", function () {
    var open = searchBtn.getAttribute("aria-expanded") !== "true";
    setPanel(menuBtn, nav, false);
    closeGroups();
    setPanel(searchBtn, search, open);
    if (open) document.getElementById("site-search-input").focus();
  });
  var groups = nav ? Array.from(nav.querySelectorAll(".nav-group")) : [];
  function closeGroups() { groups.forEach(function (group) { group.open = false; }); }
  if (desktopNav.matches) closeGroups();
  groups.forEach(function (group) {
    var summary = group.querySelector("summary");
    var list = group.querySelector("ul");
    var firstLink = list.querySelector("a");
    var title = document.createElement("li");
    title.className = "nav-panel-title";
    var overview = document.createElement("a");
    overview.href = firstLink.getAttribute("href");
    overview.textContent = summary.textContent;
    title.appendChild(overview);
    list.prepend(title);
    var closeItem = document.createElement("li");
    closeItem.className = "nav-panel-close";
    var closeButton = document.createElement("button");
    closeButton.type = "button";
    closeButton.textContent = "×";
    closeButton.setAttribute("aria-label", "Close " + summary.textContent + " submenu");
    closeButton.addEventListener("click", function () {
      group.open = false;
      summary.focus();
    });
    closeItem.appendChild(closeButton);
    list.appendChild(closeItem);
    var hoverClose;
    group.addEventListener("pointerenter", function (event) {
      window.clearTimeout(hoverClose);
      if (!desktopNav.matches || event.pointerType === "touch") return;
      closeGroups();
      group.open = true;
    });
    group.addEventListener("pointerleave", function (event) {
      if (!desktopNav.matches || event.pointerType === "touch") return;
      hoverClose = window.setTimeout(function () {
        if (!group.contains(document.activeElement)) group.open = false;
      }, 180);
    });
    group.addEventListener("focusout", function (event) {
      if (desktopNav.matches && !group.contains(event.relatedTarget)) group.open = false;
    });
    group.querySelector("summary").addEventListener("click", function () {
      if (desktopNav.matches) groups.forEach(function (other) { if (other !== group) other.open = false; });
    });
  });
  document.addEventListener("click", function (event) {
    if (!event.target.closest(".site-header")) {
      setPanel(menuBtn, nav, false);
      setPanel(searchBtn, search, false);
      closeGroups();
    }
  });
  desktopNav.addEventListener("change", function () {
    setPanel(menuBtn, nav, false);
    closeGroups();
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
      btn.setAttribute("aria-label", btn === menuBtn ? "Open menu" : "Open search");
      var panel = document.getElementById(btn.getAttribute("aria-controls"));
      if (panel) panel.classList.remove("is-open");
    });
    var activeGroup = active.closest && active.closest(".nav-group");
    closeGroups();
    if (inNav && desktopNav.matches && activeGroup) activeGroup.querySelector("summary").focus();
    else if (inNav) menuBtn.focus();
    if (inSearch) searchBtn.focus();
  });
})();
