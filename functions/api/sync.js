/**
 * UUIDv7: 01a2133a-ca04-7388-8de0-b429c2c3fd58
 * Timestamp: 2026-11-25T15:02:29Z
 * Edge Ingestion & Webhook Controller
 */

export async function onRequestPost(context) {
  const { request, env, data } = context;
  if (!data.authenticated) {
    return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });
  }

  try {
    const payload = await request.json();
    const { uuid, accountId, llmAccount, link, title, description, notes, issues, dataSensitivity } = payload;

    if (!uuid || !accountId || !title || !link) {
      return new Response(JSON.stringify({ error: "Missing required fields" }), { status: 400 });
    }

    const isCorporate = accountId.toLowerCase().includes("@transparency-x.com");
    const isConfidential = (dataSensitivity || "").toLowerCase() === "confidential";
    if (isConfidential && !isCorporate) {
      return new Response(JSON.stringify({
        error: "GOVERNANCE VIOLATION: Confidential project cannot be assigned to personal Gmail account.",
        accountId: accountId
      }), { status: 422 });
    }

    let severity = "CLEAN";
    const issuesUpper = (issues || "").toUpperCase();
    if (issuesUpper.includes("[BLOCKER]")) severity = "BLOCKER";
    else if (issuesUpper.includes("[MAJOR]")) severity = "MAJOR";
    else if (issuesUpper.includes("[MINOR]")) severity = "MINOR";
    else if (issuesUpper.includes("[POLISH]")) severity = "POLISH";

    const query = `
      INSERT INTO backlog_items (
        uuid, account_id, llm_account, link, title, description, notes, issues, severity, data_sensitivity, updated_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
      ON CONFLICT(uuid) DO UPDATE SET
        account_id = excluded.account_id,
        llm_account = excluded.llm_account,
        link = excluded.link,
        title = excluded.title,
        description = excluded.description,
        notes = excluded.notes,
        issues = excluded.issues,
        severity = excluded.severity,
        data_sensitivity = excluded.data_sensitivity,
        updated_at = CURRENT_TIMESTAMP
    `;

    await env.DB.prepare(query)
      .bind(
        uuid,
        accountId,
        llmAccount || "Other",
        link,
        title,
        description || "",
        notes || "",
        issues || "",
        severity,
        dataSensitivity || "public"
      )
      .run();

    return new Response(JSON.stringify({
      success: true,
      uuid: uuid,
      syncedAt: new Date().toISOString()
    }), { status: 200, headers: { "Content-Type": "application/json" } });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
