/* Shared, dependency-free navigation, search, course filters and enquiry drafts. */
(function () {
  'use strict';
  document.querySelectorAll('[data-course-catalogue]').forEach(function (catalogue) {
    var form = catalogue.querySelector('[data-course-filter]');
    var cards = Array.from(catalogue.querySelectorAll('[data-catalogue-card]'));
    var params = new URLSearchParams(window.location.search);
    ['q', 'level', 'campus'].forEach(function (name) {
      var input = form.elements.namedItem(name);
      if (input && params.has(name)) input.value = params.get(name);
    });
    function filter() {
      var q = form.elements.q.value.trim().toLowerCase();
      var campus = form.elements.campus.value;
      var level = form.elements.level ? form.elements.level.value : '';
      var count = 0;
      cards.forEach(function (card) {
        var words = q.split(/\s+/).filter(Boolean);
        var title = card.dataset.title.toLowerCase();
        var visible = words.every(function (word) { return title.indexOf(word) !== -1; }) && (!campus || card.dataset.campus.split(',').includes(campus)) && (!level || card.dataset.level === level);
        card.hidden = !visible;
        if (visible) count++;
      });
      catalogue.querySelector('.course-count').textContent = count + (count === 1 ? ' course' : ' courses');
      catalogue.querySelector('.course-empty').hidden = count !== 0;
    }
    form.addEventListener('input', filter);
    form.addEventListener('change', filter);
    form.addEventListener('submit', function (event) { event.preventDefault(); filter(); });
    form.addEventListener('reset', function () { setTimeout(filter, 0); });
    filter();
  });

  document.querySelectorAll('[data-enquiry-form]').forEach(function (form) {
    form.addEventListener('submit', function (event) {
      event.preventDefault();
      if (!form.reportValidity()) return;
      var data = new FormData(form);
      var body = ['Name: ' + data.get('name'), 'Email: ' + data.get('email'), 'Phone: ' + (data.get('phone') || 'Not provided'), 'Campus: ' + (data.get('campus') || 'Not selected'), 'Topic: ' + data.get('topic'), '', data.get('message')].join('\n');
      var email = 'mailto:info.uwaindia@uwa.edu.au?subject=' + encodeURIComponent('UWA India enquiry: ' + data.get('topic')) + '&body=' + encodeURIComponent(body);
      var panel = form.querySelector('[data-draft-panel]');
      if (!panel) {
        panel = document.createElement('div');
        panel.dataset.draftPanel = '';
        panel.className = 'info-panel';
        var open = document.createElement('a');
        open.className = 'btn btn--primary';
        open.dataset.openDraft = '';
        open.textContent = 'Open email draft';
        panel.appendChild(open);
        var label = document.createElement('label');
        var draft = document.createElement('textarea');
        draft.readOnly = true;
        draft.rows = 8;
        draft.dataset.draftText = '';
        draft.setAttribute('aria-label', 'Your enquiry email draft');
        label.textContent = 'Or copy this draft into your email app';
        label.appendChild(draft);
        panel.appendChild(label);
        form.appendChild(panel);
      }
      panel.querySelector('[data-open-draft]').href = email;
      panel.querySelector('[data-draft-text]').value = 'To: info.uwaindia@uwa.edu.au\nSubject: UWA India enquiry: ' + data.get('topic') + '\n\n' + body;
      form.querySelector('.form-status').textContent = 'Your enquiry draft is ready. Open your email app and send it to complete your enquiry. Nothing has been submitted from this form.';
      panel.querySelector('[data-open-draft]').focus();
    });
  });

  var siteSearch = document.querySelector('[data-site-search]');
  if (siteSearch && window.UWA_SEARCH_INDEX) {
    var field = siteSearch.elements.q;
    var params = new URLSearchParams(window.location.search);
    field.value = params.get('q') || '';
    function search() {
      var query = field.value.trim().toLowerCase();
      var output = document.getElementById('search-results');
      output.replaceChildren();
      if (!query) { document.getElementById('search-status').textContent = 'Enter a word or phrase to find a page.'; return; }
      var terms = query.split(/\s+/).filter(Boolean);
      var matches = window.UWA_SEARCH_INDEX.map(function (item) {
        var text = (item.title + ' ' + item.description + ' ' + item.content).toLowerCase();
        var score = terms.every(function (term) { return text.includes(term); }) ? 1 : 0;
        if (score && item.title.toLowerCase().includes(query)) score += 3;
        return {item:item, score:score};
      }).filter(function (result) { return result.score; }).sort(function (a,b) { return b.score-a.score; });
      document.getElementById('search-status').textContent = matches.length ? matches.length + (matches.length === 1 ? ' page found' : ' pages found') : 'No pages match your search. Try a different word, or contact our team.';
      matches.forEach(function (result) {
        var item = result.item;
        var a = document.createElement('a');a.href = item.url;
        var title = document.createElement('strong');title.textContent = item.title;
        var description = document.createElement('p');description.textContent = item.description;
        a.append(title,description);output.appendChild(a);
      });
    }
    siteSearch.addEventListener('submit', function (event) { event.preventDefault(); search(); });
    field.addEventListener('input', search);
    search();
  }
  var eventCampus = document.getElementById('event-campus');
  if (eventCampus) eventCampus.addEventListener('change', function () {
    var count = 0;
    document.querySelectorAll('[data-event-campus]').forEach(function (card) {
      card.hidden = eventCampus.value !== 'all' && card.dataset.eventCampus !== eventCampus.value;
      if (!card.hidden) count++;
    });
    document.getElementById('event-status').textContent = count + (count === 1 ? ' campus event directory' : ' campus event directories');
  });
})();
