// Small visual reading indicator for long pages; no analytics and no cookies.
(() => {
  const bar = document.querySelector('.reading-progress');
  const fill = document.querySelector('.reading-progress-fill');
  if (!bar || !fill) return;
  let scheduled = false;
  function paint() {
    scheduled = false;
    const max = document.documentElement.scrollHeight - window.innerHeight;
    if (max <= 280) { bar.classList.remove('show'); fill.style.height = '0%'; return; }
    bar.classList.add('show');
    fill.style.height = Math.min(100, Math.max(0, (window.scrollY / max) * 100)) + '%';
  }
  function update() { if (!scheduled) { scheduled = true; requestAnimationFrame(paint); } }
  addEventListener('scroll', update, { passive: true });
  addEventListener('resize', update, { passive: true });
  addEventListener('load', update);
  update();
})();
