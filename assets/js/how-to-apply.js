/* Native dialog provides focus containment, Escape, and focus restoration. */
(function () {
  'use strict';
  var dialog = document.querySelector('.faq-dialog');
  var trigger = document.querySelector('[data-open-faq]');
  if (!dialog || !trigger) return;
  trigger.addEventListener('click', function () { dialog.showModal(); });
  dialog.querySelector('.faq-close').addEventListener('click', function () { dialog.close(); });
  dialog.addEventListener('click', function (event) {
    var bounds = dialog.getBoundingClientRect();
    if (event.target === dialog && (event.clientX < bounds.left || event.clientX > bounds.right || event.clientY < bounds.top || event.clientY > bounds.bottom)) dialog.close();
  });
})();
