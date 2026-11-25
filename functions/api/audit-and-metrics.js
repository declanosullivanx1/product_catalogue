/**
 * UUIDv7: 01a2133a-ca10-7901-ae60-45e76c4d8f7a
 * Timestamp: 2026-11-25T15:02:29Z
 * Audit Logger & Velocity Analytics Controller
 */

export async function onRequest(context) {
  const { request, env, data } = context;

  if (request.method === "POST") {
    if (!data.authenticated) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
    try {
      const { action, targetUuid, metadata } = await request.json();
      const event = {
        eventId: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        actor: data.userEmail || "service-token@system.local",
        action: action,
        targetUuid: targetUuid,
        clientIp: request.headers.get("CF-Connecting-IP"),
        metadata: metadata || {}
      };
      const dateStr = new Date().toISOString().split("T")[0];
      const logKey = `audit-logs/${dateStr}.ndjson`;
      let current = "";
      const obj = await env.AUDIT_BUCKET.get(logKey);
      if (obj) current = await obj.text();
      await env.AUDIT_BUCKET.put(logKey, current + JSON.stringify(event) + "\n", {
        httpMetadata: { contentType: "application/x-ndjson" }
      });
      return new Response(JSON.stringify({ success: true, eventId: event.eventId }), { status: 201 });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  }

  if (request.method === "GET") {
    try {
      const items = await env.DB.prepare("SELECT uuid, account_id, llm_account, created_at, updated_at FROM backlog_items WHERE severity = 'CLEAN'").all();
      let totalDays = 0, count = 0;
      for (const item of items.results) {
        let cMs = null;
        try {
          cMs = parseInt(item.uuid.split("-")[0] + item.uuid.split("-")[1], 16);
        } catch(e) {
          cMs = new Date(item.created_at).getTime();
        }
        const uMs = new Date(item.updated_at).getTime();
        totalDays += Math.max(0, (uMs - cMs) / (1000 * 60 * 60 * 24));
        count++;
      }
      return new Response(JSON.stringify({
        averageCycleTimeDays: count > 0 ? (totalDays / count).toFixed(2) : 0,
        totalAnalyzed: count
      }), { status: 200, headers: { "Content-Type": "application/json" } });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  }

  return new Response("Method Not Allowed", { status: 405 });
}
