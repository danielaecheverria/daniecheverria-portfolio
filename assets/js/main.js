(function(){
  var reduceMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  if (reduceMotion) return;

  var revealTargets = document.querySelectorAll('.reveal, .case');
  if (revealTargets.length && 'IntersectionObserver' in window) {
    var observer = new IntersectionObserver(function(entries){
      entries.forEach(function(entry){
        if (entry.isIntersecting) {
          entry.target.classList.add('in-view');
          observer.unobserve(entry.target);
        }
      });
    }, { threshold: 0.2 });
    revealTargets.forEach(function(el){ observer.observe(el); });
  }

  var strip = document.getElementById('strip');
  if (strip) {
    var ticking = false;
    window.addEventListener('scroll', function(){
      if (!ticking) {
        window.requestAnimationFrame(function(){
          strip.style.transform = 'translateX(' + (-window.scrollY * 0.15) + 'px)';
          ticking = false;
        });
        ticking = true;
      }
    }, { passive: true });
  }
})();
