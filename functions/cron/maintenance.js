/**
 * UUIDv7: 01a2133a-ca13-7f66-85c9-0395f9a6f1b9
 * Timestamp: 2026-11-25T15:02:29Z
 * Scheduled Edge Maintenance: R2 Backup & Link Sweeper
 */

export async function onRequestGet(context) {
  const { env, request } = context;
  const authHeader = request.headers.get("Authorization");
  if (authHeader !== `Bearer ${env.CRON_SECRET}` && env.ENVIRONMENT === "production") {
    return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
  }

  try {
    const allRows = await env.DB.prepare("SELECT * FROM backlog_items ORDER BY created_at ASC").all();
    const backupJson = JSON.stringify({
      timestamp: new Date().toISOString(),
      count: allRows.results.length,
      records: allRows.results
    }, null, 2);

    const dateStr = new Date().toISOString().split("T")[0];
    const key = `backups/${dateStr}/backlog-${Date.now()}.json`;
    await env.BACKUP_BUCKET.put(key, backupJson, {
      httpMetadata: { contentType: "application/json" }
    });

    return new Response(JSON.stringify({ success: true, backupKey: key }), { status: 200 });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
