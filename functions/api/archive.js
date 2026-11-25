/**
 * UUIDv7: 01a2133a-ca0e-7a4a-90d0-f816adf76801
 * Timestamp: 2026-11-25T15:02:29Z
 * Archived Prototype Search API
 */

export async function onRequestGet(context) {
  const { request, env, data } = context;
  const url = new URL(request.url);
  const q = url.searchParams.get("q") || "";
  const filter = q ? "%" + q.toLowerCase() + "%" : "%";

  try {
    const isEngineer = data.authenticated;
    let sql = isEngineer
      ? "SELECT uuid, account_id, llm_account, title, description, severity, updated_at FROM backlog_items WHERE (LOWER(title) LIKE ? OR LOWER(description) LIKE ?) ORDER BY updated_at DESC LIMIT 100"
      : "SELECT uuid, title, description, llm_account, link, severity FROM backlog_items WHERE data_sensitivity = 'public' AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?) ORDER BY updated_at DESC LIMIT 50";

    const { results } = await env.DB.prepare(sql).bind(filter, filter).all();
    return new Response(JSON.stringify({ query: q, totalMatches: results.length, data: results }), {
      status: 200,
      headers: { "Content-Type": "application/json" }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
