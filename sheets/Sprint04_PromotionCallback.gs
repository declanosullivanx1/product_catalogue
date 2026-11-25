/**
 * UUIDv7: 01a2133a-ca1f-7458-87e0-8d76ac6688be
 * Timestamp: 2026-11-25T15:02:29Z
 * Post-Promotion Row Lock
 */

function LOCK_AND_FINALIZE_ROW(uuid, canonicalUrl) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {
    if (data[i][0] === uuid) {
      const r = i + 1;
      const range = sheet.getRange(r, 1, 1, 9);
      range.setBackground("#e6f4ea");
      sheet.getRange(r, 9).setValue(canonicalUrl);
      const prot = range.protect().setDescription(`Locked (${uuid})`);
      prot.removeEditors(prot.getEditors());
      break;
    }
  }
}
