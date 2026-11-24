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
/* === All-page cumulative PV with a compact Home-only display ===
 * Append ONCE to the END of static/js/site.js.
 * REMOVE the previous CountAPI block and the previous Cloudflare 30-day
 * .cf-traffic-card / fetch('/api/traffic') block before adding this.
 */
(() => {
  const path = location.pathname.replace(/\/index\.html$/i, '/');
  const visitorStorageKey = 'yw_visitor_id_v1';
  const uuid = () => crypto.randomUUID();
  const isUUID = str => /^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i.test(str || '');
  let visitorId;
  try {
    visitorId = localStorage.getItem(visitorStorageKey);
    if (!isUUID(visitorId)) {
      visitorId = uuid();
      localStorage.setItem(visitorStorageKey, visitorId);
    }
  } catch (_) {
    // Browsers disabling persistent storage get a session-only ID.
    try {
      visitorId = sessionStorage.getItem(visitorStorageKey);
      if (!isUUID(visitorId)) {
        visitorId = uuid();
        sessionStorage.setItem(visitorStorageKey, visitorId);
      }
    } catch (_) { visitorId = uuid(); }
  }

  // Record ONE PV per document load; a refresh is a new PV.
  // The eventId prevents accidental double inserts on retries.
  const eventId = uuid();
  const tracking = fetch('/api/track', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ path, visitorId, eventId }),
    cache: 'no-store',
    credentials: 'same-origin'
  }).then(response => {
    if (!response.ok) throw new Error('Tracking unavailable');
  }).catch(() => {});

  if (path !== '/') return;
  const contact = [...document.querySelectorAll('main h2, main h3, .article-body h2')]
    .find(el => el.textContent.trim().toLowerCase() === 'contact');
  if (!contact || document.querySelector('.yw-total-pv')) return;

  const css = document.createElement('style');
  css.textContent = `
    .yw-total-pv { float:right; width:94px; padding:7px 5px;
      box-sizing:border-box; margin:2px 0 8px 12px;
      background:#f1edf7; border:1px solid #e7e0ee;
      border-radius:7px; text-align:center; font-family:inherit; }
    .yw-total-pv-label { display:block; color:#625072; font-size:10px;
      line-height:1.3; font-weight:600; text-align:center; }
    .yw-total-pv-number { display:block; margin-top:2px; color:#76628d;
      font-size:17px; font-weight:600; line-height:1.3;
      font-variant-numeric:tabular-nums; text-align:center; }
    @media (max-width:620px) {
      .yw-total-pv { float:none; margin:6px 0 14px; }
    }
  `;
  document.head.appendChild(css);
  const box = document.createElement('aside');
  box.className = 'yw-total-pv';
  box.setAttribute('aria-label', 'Total page views since counting began');
  box.innerHTML = '<span class="yw-total-pv-label">Total PV</span>' +
    '<strong class="yw-total-pv-number" aria-live="polite">—</strong>';
  contact.insertAdjacentElement('afterend', box);

  tracking.finally(() => fetch('/api/traffic', { cache: 'no-store' })
    .then(response => { if (!response.ok) throw new Error('Unavailable'); return response.json(); })
    .then(data => {
      if (!Number.isSafeInteger(data.totalPageviews) || data.totalPageviews < 0) throw new Error('Invalid count');
      box.querySelector('.yw-total-pv-number').textContent =
        data.totalPageviews.toLocaleString('en-US');
    }).catch(() => {
      box.querySelector('.yw-total-pv-number').textContent = '—';
    }));
})();
