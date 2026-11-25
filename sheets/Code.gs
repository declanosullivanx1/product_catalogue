/**
 * UUIDv7: 01a2133a-ca17-7f99-8ee2-84d97ebcea8a
 * Timestamp: 2026-11-25T15:02:29Z
 * Google Apps Script Core Intake Engine
 */

const ACCOUNTS = [
  "declanosullivanx1@gmail.com",
  "declanjosephosullivan@gmail.com",
  "cathal.and.declan@gmail.com",
  "declanjosullivan86@gmail.com",
  "declanseer@gmail.com",
  "declanjoseph2025@gmail.com",
  "davewilson1x1@gmail.com",
  "charlie.and.declan.osullivan@gmail.com",
  "declan@transparency-x.com",
  "Other"
];

const LLM_PLATFORMS = [
  "Google AI Studio Web App",
  "Gemini Chat Web App",
  "Qwen AI Studio",
  "Kimi AI",
  "ChatGPT Web App",
  "Claude AI Web App",
  "Other"
];

function GENERATE_UUIDV7() {
  const now = Date.now();
  const timeHex = now.toString(16).padStart(12, '0');
  const randA = Math.floor(Math.random() * 0x0FFF).toString(16).padStart(3, '0');
  const randB1 = (Math.floor(Math.random() * 0x3FFF) | 0x8000).toString(16).padStart(4, '0');
  const randB2 = Math.floor(Math.random() * 0xFFFFFFFFFFFF).toString(16).padStart(12, '0');
  return `${timeHex.slice(0, 8)}-${timeHex.slice(8, 12)}-7${randA}-${randB1}-${randB2}`;
}

function onEdit(e) {
  if (!e || !e.range) return;
  const sheet = e.source.getActiveSheet();
  const row = e.range.getRow();
  const col = e.range.getColumn();
  if (row < 2) return;

  if (col === 5) {
    const title = e.range.getValue().toString().trim();
    const uuidCell = sheet.getRange(row, 1);
    if (title !== "" && uuidCell.getValue().toString().trim() === "") {
      uuidCell.setValue(GENERATE_UUIDV7());
    }
  }
}
