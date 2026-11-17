(() => {
  const btn = document.querySelector('[data-mobile-menu]');
  const menu = document.querySelector('[data-main-nav]');
  if (btn && menu) {
    btn.addEventListener('click', () => {
      const open = menu.classList.toggle('is-open');
      btn.setAttribute('aria-expanded', String(open));
    });
  }
  const filters = document.querySelectorAll('[data-pub-filter]');
  const pubs = document.querySelectorAll('[data-publication]');
  const count = document.querySelector('[data-publication-count]');
  if (count && pubs.length) count.textContent = `${pubs.length} items`;
  filters.forEach(button => button.addEventListener('click', () => {
    const value = button.dataset.pubFilter;
    filters.forEach(f => {f.classList.toggle('active', f === button); f.setAttribute('aria-pressed', String(f === button));});
    pubs.forEach(p => {p.hidden = value !== 'All' && p.dataset.type !== value;});
  }));
  const date = document.querySelector('[data-current-year]');
  if (date) date.textContent = String(new Date().getFullYear());
})();
