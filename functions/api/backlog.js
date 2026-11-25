/**
 * UUIDv7: 01a2133a-ca06-7809-9acd-402d643a133f
 * Timestamp: 2026-11-25T15:02:29Z
 * RBAC Sensitivity Slicing Endpoint
 */

export async function onRequestGet(context) {
  const { env, data } = context;
  try {
    const isEngineer = data.authenticated && (
      data.authType === "service_token" ||
      (data.groups && data.groups.includes("engineering")) ||
      (data.userEmail && data.userEmail.endsWith("@transparency-x.com"))
    );

    let query = isEngineer
      ? "SELECT * FROM backlog_items ORDER BY updated_at DESC"
      : "SELECT uuid, title, description, llm_account, link, severity FROM backlog_items WHERE data_sensitivity = 'public' AND severity != 'BLOCKER' ORDER BY updated_at DESC";

    const { results } = await env.DB.prepare(query).all();

    return new Response(JSON.stringify({
      viewerRole: isEngineer ? "authenticated_engineer" : "public_visitor",
      count: results.length,
      data: results
    }), {
      status: 200,
      headers: {
        "Content-Type": "application/json",
        "Cache-Control": isEngineer ? "private, no-cache" : "public, max-age=60"
      }
    });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
