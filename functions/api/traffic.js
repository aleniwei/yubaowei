/** Public read-only API. Returns only the all-time PV count, not visitor IDs. */
export async function onRequestGet({ env }) {
  if (!env.DB) return reply({ error: 'Database binding DB is missing' }, 503);
  try {
    const row = await env.DB.prepare('SELECT COUNT(*) AS total FROM page_views').first();
    return reply({ totalPageviews: Number(row?.total || 0), period: 'since_counter_enabled' });
  } catch (error) {
    console.error('D1 traffic query failed:', error);
    return reply({ error: 'Counter temporarily unavailable' }, 503);
  }
}
function reply(data, status = 200) {
  return new Response(JSON.stringify(data), {
    status, headers: {
      'Content-Type': 'application/json; charset=utf-8',
      'Cache-Control': 'no-store',
      'X-Content-Type-Options': 'nosniff'
    }
  });
}
