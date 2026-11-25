/**
 * UUIDv7: 01a2133a-ca1a-7c53-8e0d-262e176902a9
 * Timestamp: 2026-11-25T15:02:29Z
 * Service Token Authenticated Webhook
 */

function SYNC_ROW_TO_EDGE(rowNumber) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const row = sheet.getRange(rowNumber, 1, 1, 8).getValues()[0];
  const [uuid, accountId, llmAccount, link, title, description, notes, issues] = row;
  if (!uuid || !title || !link) return;

  const props = PropertiesService.getScriptProperties();
  const url = props.getProperty("CF_PAGES_ENDPOINT");
  const id = props.getProperty("CF_ACCESS_CLIENT_ID");
  const secret = props.getProperty("CF_ACCESS_CLIENT_SECRET");

  if (!url || !id || !secret) return;

  UrlFetchApp.fetch(url, {
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({ uuid, accountId, llmAccount, link, title, description, notes, issues }),
    headers: { "CF-Access-Client-Id": id, "CF-Access-Client-Secret": secret },
    muteHttpExceptions: true
  });
}
