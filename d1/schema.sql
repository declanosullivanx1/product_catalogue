-- UUIDv7: 01a2133a-ca14-78fe-afb7-bdb8686235f8
-- Timestamp: 2026-11-25T15:02:29Z
-- Cloudflare D1 Backlog Mirror Schema

CREATE TABLE IF NOT EXISTS backlog_items (
  uuid TEXT PRIMARY KEY,
  account_id TEXT NOT NULL,
  llm_account TEXT NOT NULL,
  link TEXT NOT NULL,
  title TEXT NOT NULL,
  description TEXT,
  notes TEXT,
  issues TEXT,
  severity TEXT DEFAULT 'CLEAN',
  checklist_progress TEXT,
  subdomain_status TEXT,
  data_sensitivity TEXT DEFAULT 'public',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_backlog_account ON backlog_items(account_id);
CREATE INDEX IF NOT EXISTS idx_backlog_severity ON backlog_items(severity);
