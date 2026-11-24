/** Record a single page view on the server into Cloudflare D1.
 * Production Pages D1 binding: DB
 * Secret (production): CF_VISITOR_SALT -- random 32+ character secret
 */
const VALID_ID = /^[a-f0-9]{8}-[a-f0-9]{4}-[1-8][a-f0-9]{3}-[89ab][a-f0-9]{3}-[a-f0-9]{12}$/i;
const json = (body, status = 200) => new Response(JSON.stringify(body), {
  status, headers: {
    'Content-Type': 'application/json; charset=utf-8',
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
  }
});
export async function onRequestPost({ request, env }) {
  if (!env.DB || !env.CF_VISITOR_SALT) return json({ error: 'Storage is not configured' }, 503);
  const url = new URL(request.url);
  // Only same-origin browser calls are accepted. No public cross-origin API.
  if (request.headers.get('Origin') !== url.origin) return json({ error: 'Forbidden' }, 403);
  if (!/^application\/json(?:\s*;|$)/i.test(request.headers.get('Content-Type') || '')) {
    return json({ error: 'JSON required' }, 415);
  }
  const raw = await request.text();
  if (raw.length > 1024) return json({ error: 'Request too large' }, 413);
  let data;
  try { data = JSON.parse(raw); } catch { return json({ error: 'Invalid JSON' }, 400); }
  if (!VALID_ID.test(data?.visitorId || '') || !VALID_ID.test(data?.eventId || '')) {
    return json({ error: 'Invalid identifiers' }, 400);
  }
  let path;
  try {
    const target = new URL(data.path, url.origin);
    if (target.origin !== url.origin) throw new Error('cross-origin');
    path = target.pathname.replace(/\/index\.html$/i, '/');
  } catch { return json({ error: 'Invalid path' }, 400); }
  if (!/^\/[a-z0-9/_-]*$/i.test(path) || path.length > 120 || path.includes('//') || path.startsWith('/api/')) {
    return json({ error: 'Invalid path' }, 400);
  }
  if (!path.endsWith('/')) path += '/';
  const material = new TextEncoder().encode(`${env.CF_VISITOR_SALT}:${data.visitorId}`);
  const digest = await crypto.subtle.digest('SHA-256', material);
  const hash = [...new Uint8Array(digest)].map(b => b.toString(16).padStart(2, '0')).join('');
  try {
    const result = await env.DB.prepare(
      'INSERT OR IGNORE INTO page_views (event_id, path, visitor_hash) VALUES (?, ?, ?)'
    ).bind(data.eventId, path, hash).run();
    return json({ ok: true, counted: (result.meta?.changes || 0) > 0 });
  } catch (error) {
    console.error('D1 page view insert failed:', error);
    return json({ error: 'Counter temporarily unavailable' }, 503);
  }
}
