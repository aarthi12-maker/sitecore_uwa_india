(function () {
  'use strict';
  var track = document.querySelector('.reasons-rankings__track');
  var progress = document.querySelector('.reasons-rankings__progress span');
  if (!track || !progress) return;
  function update() {
    var max = track.scrollWidth - track.clientWidth;
    var fraction = max > 0 ? track.scrollLeft / max : 0;
    progress.style.transform = 'translateX(' + fraction * 100 + '%)';
  }
  track.addEventListener('scroll', update, { passive: true });
  track.addEventListener('keydown', function (event) {
    if (event.key !== 'ArrowRight' && event.key !== 'ArrowLeft') return;
    event.preventDefault();
    var direction = event.key === 'ArrowRight' ? 1 : -1;
    track.scrollBy({ left: direction * track.querySelector('.reasons-ranking').offsetWidth, behavior: matchMedia('(prefers-reduced-motion: reduce)').matches ? 'instant' : 'smooth' });
  });
  window.addEventListener('resize', update);
  update();
})();
