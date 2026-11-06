(function () {
  'use strict';
  var dialog = document.querySelector('.course-dialog');
  if (!dialog || typeof dialog.showModal !== 'function') return;
  document.querySelectorAll('[data-course]').forEach(function (card) {
    card.addEventListener('click', function (event) {
      // Preserve normal link behaviour for opening a new tab or window.
      if (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey) return;
      event.preventDefault();
      var title = card.getAttribute('data-course');
      document.getElementById('course-dialog-title').textContent = title;
      document.getElementById('course-enquiry-link').href = 'mailto:info.uwaindia@uwa.edu.au?subject=' + encodeURIComponent('Course enquiry: ' + title);
      dialog.showModal();
    });
  });
  dialog.querySelector('.course-dialog__close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) {
    var bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
})();
