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
/* Home page visitor counter */
(() => {
  if (!document.body.classList.contains('page-home')) return;

  const contact = [...document.querySelectorAll('.article-body h2')]
    .find(el => el.textContent.trim().toLowerCase() === 'contact');

  if (!contact) return;

  const style = document.createElement('style');
  style.textContent = `
  .home-visitor-counter {
    float: right;
    width: 88px;
    margin: 2px 0 8px 12px;
    padding: 7px 5px;
    border: 1px solid #e7e0ee;
    border-radius: 7px;
    background: #f1edf7;
    text-align: center;
    box-sizing: border-box;
}

.home-visitor-counter .visitor-label {
    display: block;
    font-size: 11px;
    font-weight: 500;
    color: #625072;
}

.home-visitor-counter .visitor-number {
    display: block;
    margin-top: 2px;
    font-size: 17px;
    font-weight: 600;
    line-height: 1.15;
    color: #76628d;
    font-variant-numeric: tabular-nums;
}
    @media (max-width: 620px) {
      .home-visitor-counter {
        float: none;
        margin: 4px 0 20px;
      }
    }
  `;
  document.head.appendChild(style);

  const card = document.createElement('aside');
  card.className = 'home-visitor-counter';
  card.innerHTML =
    '<span class="visitor-label">Visitors</span>' +
    '<strong class="visitor-number" aria-live="polite">…</strong>';

  contact.insertAdjacentElement('afterend', card);

  const number = card.querySelector('.visitor-number');
  const api = 'https://countapi.mileshilliard.com/api/v1';
  const key = 'yubaowei_pages_dev_home_visitors_2026';
  const storageKey = 'yubaowei_home_last_visit_v1';

  let recentlyVisited = false;

  try {
    const last = Number(localStorage.getItem(storageKey));
    recentlyVisited =
      last > 0 &&
      Date.now() >= last &&
      Date.now() - last < 86400000;
  } catch (_) {}

  const action = recentlyVisited ? 'get' : 'hit';

  fetch(`${api}/${action}/${key}`, {
    cache: 'no-store',
    referrerPolicy: 'no-referrer'
  })
    .then(response => {
      if (!response.ok) throw new Error('Counter unavailable');
      return response.json();
    })
    .then(data => {
      const value = Number(data.value);
      if (!Number.isFinite(value) || value < 1) {
        throw new Error('Invalid count');
      }

      // First visit: API returns 1; displayed count is 11.
      number.textContent = (value + 9).toLocaleString('en-US');

      if (!recentlyVisited) {
        try {
          localStorage.setItem(storageKey, String(Date.now()));
        } catch (_) {}
      }
    })
    .catch(() => {
      number.textContent = '—';
      number.title = 'Visitor count temporarily unavailable';
    });
})();
