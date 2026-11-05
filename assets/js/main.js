/* UWA India — homepage behaviour (no dependencies) */
(function () {
  "use strict";

  /* ---------- Header: menu + search toggles ---------- */
  function toggle(btn, panel, onOpen) {
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
    var updateBar = function () {
      var max = track.scrollWidth - track.clientWidth;
      var visible = track.clientWidth / track.scrollWidth;
      bar.style.width = Math.max(visible, 0.15) * 100 + "%";
      var ratio = max > 0 ? track.scrollLeft / max : 0;
      var free = 1 / Math.max(visible, 0.15) - 1;
      bar.style.transform = "translateX(" + ratio * free * 100 + "%)";
      bar.parentElement.style.visibility = max > 0 ? "visible" : "hidden";
    };
    track.addEventListener("scroll", updateBar, { passive: true });
    window.addEventListener("resize", updateBar);
    updateBar();
  }

  /* ---------- Footer country switcher ---------- */
  var countryBtn = document.querySelector(".country__btn");
  var countryMenu = document.getElementById("country-menu");
  countryBtn.addEventListener("click", function (e) {
    e.stopPropagation();
    var open = countryMenu.hidden;
    countryMenu.hidden = !open;
    countryBtn.setAttribute("aria-expanded", String(open));
  });
  document.addEventListener("click", function () {
    countryMenu.hidden = true;
    countryBtn.setAttribute("aria-expanded", "false");
  });

  /* ---------- Enquiry form ---------- */
  var data = window.UWA_FORM_DATA;
  var form = document.getElementById("enquiry-form");
  if (!form || !data) return;

  var $ = function (id) { return document.getElementById(id); };
  var state = $("f-state"), city = $("f-city"), campus = $("f-campus"),
      program = $("f-program"), course = $("f-course"), intake = $("f-intake");

  function fill(select, placeholder, values) {
    select.innerHTML = "";
    var first = document.createElement("option");
    first.value = ""; first.textContent = placeholder;
    select.appendChild(first);
    (values || []).forEach(function (v) {
      var o = document.createElement("option");
      o.value = v; o.textContent = v;
      select.appendChild(o);
    });
  }
  function enable(select, placeholder, values) {
    fill(select, placeholder, values);
    select.disabled = !values || !values.length;
  }

  fill(state, "Select State", Object.keys(data.states));
  fill(campus, "Select Campus", Object.keys(data.campuses));
  fill(intake, "Select Intake Period", data.intakes);

  state.addEventListener("change", function () {
    if (state.value) enable(city, "Select City", data.states[state.value]);
    else enable(city, "Select State first", null);
  });
  campus.addEventListener("change", function () {
    if (campus.value) enable(program, "Select Program", Object.keys(data.campuses[campus.value]));
    else enable(program, "Select Campus first", null);
    enable(course, "Select Programme first", null);
  });
  program.addEventListener("change", function () {
    if (program.value) enable(course, "Select Course", data.campuses[campus.value][program.value]);
    else enable(course, "Select Programme first", null);
  });

  /* "Enquiring as" changes the name label */
  var nameLabel = $("f-name-label"), nameInput = $("f-name");
  var labels = {
    "Student": ["Student Name", "Enter student name"],
    "Parent/Guardian": ["Parent/Guardian Name", "Enter parent/guardian name"],
    "Others": ["Your Name", "Enter your name"]
  };
  form.querySelectorAll('input[name="enquiringAs"]').forEach(function (r) {
    r.addEventListener("change", function () {
      var l = labels[r.value];
      nameLabel.textContent = l[0];
      nameInput.placeholder = l[1];
    });
  });

  /* Audience tiles */
  var tiles = document.querySelectorAll(".audience__tile");
  tiles.forEach(function (t) {
    t.addEventListener("click", function () {
      tiles.forEach(function (x) { x.setAttribute("aria-pressed", String(x === t)); });
    });
  });

  /* Captcha (client-side demo only — replace with Sitecore Forms / reCAPTCHA) */
  var canvas = $("captcha-canvas"), ctx = canvas.getContext("2d"), captchaText = "";
  function drawCaptcha() {
    var chars = "ABCDEFGHJKLMNPQRSTUVWXYZabcdefghjkmnpqrstuvwxyz23456789";
    captchaText = "";
    for (var i = 0; i < 6; i++) captchaText += chars[Math.floor(Math.random() * chars.length)];
    ctx.clearRect(0, 0, canvas.width, canvas.height);
    ctx.font = "italic 700 30px Outfit, Arial, sans-serif";
    ctx.fillStyle = "#0032ff";
    ctx.textBaseline = "middle";
    var x = 4;
    for (var j = 0; j < captchaText.length; j++) {
      ctx.save();
      ctx.translate(x, 24);
      ctx.rotate((Math.random() - 0.5) * 0.25);
      ctx.fillText(captchaText[j], 0, 0);
      x += ctx.measureText(captchaText[j]).width + 6;
      ctx.restore();
    }
    ctx.strokeStyle = "#0032ff"; ctx.lineWidth = 1.5;
    ctx.beginPath(); ctx.moveTo(0, 24 + (Math.random() * 6 - 3)); ctx.lineTo(x, 24 + (Math.random() * 6 - 3)); ctx.stroke();
    canvas.setAttribute("aria-label", "Captcha: " + captchaText.split("").join(" "));
  }
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(drawCaptcha); else drawCaptcha();
  $("captcha-refresh").addEventListener("click", function () { drawCaptcha(); $("f-captcha").value = ""; });

  /* Validation */
  var rules = {
    "f-name": function (v) { return v.trim().length >= 2; },
    "f-email": function (v) { return /^[^\s@]+@[^\s@]+\.[^\s@]{2,}$/.test(v.trim()); },
    "f-mobile": function (v) {
      var digits = v.replace(/\D/g, "");
      return $("f-code").value === "+91" ? /^[6-9]\d{9}$/.test(digits) : digits.length >= 6 && digits.length <= 14;
    },
    "f-state": Boolean, "f-city": Boolean, "f-campus": Boolean,
    "f-program": Boolean, "f-course": Boolean, "f-intake": Boolean,
    "f-captcha": function (v) { return v.trim() === captchaText; }
  };
  function check(id) {
    var el = $(id);
    var ok = rules[id](el.value);
    el.closest(".field").classList.toggle("has-error", !ok);
    el.setAttribute("aria-invalid", String(!ok));
    return ok;
  }
  Object.keys(rules).forEach(function (id) {
    var el = $(id);
    el.addEventListener(el.tagName === "SELECT" ? "change" : "blur", function () {
      if (el.closest(".field").classList.contains("has-error") || el.value) check(id);
    });
  });

  form.addEventListener("submit", function (e) {
    e.preventDefault();
    var firstBad = null;
    Object.keys(rules).forEach(function (id) { if (!check(id) && !firstBad) firstBad = $(id); });
    var consent = $("f-consent");
    $("consent-box").classList.toggle("has-error", !consent.checked);
    if (!consent.checked && !firstBad) firstBad = consent;
    if (firstBad) {
      if (firstBad.disabled) firstBad = state.value ? campus : state;
      firstBad.focus();
      if (firstBad.id === "f-captcha") drawCaptcha();
      return;
    }
    /* TODO(sitecore): POST to Sitecore Forms / CRM endpoint here */
    form.hidden = true;
    var done = $("enquiry-success");
    done.hidden = false;
    done.focus();
  });
})();
