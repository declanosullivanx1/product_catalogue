<!--
  UUIDv7: 01a2133a-c9f5-70b0-ae85-f8a08254bed4
  Timestamp: 2026-11-25T15:02:29Z
-->
# Product Catalog & Backlog Engine

A static-first personal product catalog and edge-synchronized generative backlog engine deployed on Cloudflare Pages.

- **Build UUIDv7:** `01a2133a-c9f5-70b0-ae85-f8a08254bed4`
- **Generated:** `2026-11-25T15:02:29Z`
- **Stack:** Pico.css v2, Tabulator.js v6.2, Cloudflare D1, Cloudflare Pages Functions, Google Apps Script.

---

## Directory Architecture

```text
.
├── index.html                  # Main production catalog table view
├── project.html                # Project detail & version explorer template
├── intake.html                 # Backlog intake cockpit & pre-flight prober
├── projects.json               # Canonical source of truth for public catalog
├── taxonomy.json               # 30-domain multi-layered classification schema
├── css/
│   └── custom.css              # Pico variable overrides & filter de-collision rules
├── js/
│   ├── app.js                  # Main catalog data controller
│   ├── detail.js               # Detail page dynamic hydration script
│   ├── intake.js               # Client intake logic & local draft persistence
│   └── triage.js               # Claude artifact extractor & DNS prober
├── functions/
│   ├── _middleware.js          # Zero Trust Access JWT & Service Token verifier
│   ├── api/
│   │   ├── sync.js             # D1 edge upsert & corporate boundary guard
│   │   ├── backlog.js          # RBAC sensitivity-sliced catalog endpoint
│   │   ├── promote.js          # Blocker gate check & GitHub REST API committer
│   │   ├── verify-and-rollback.js # Edge health prober & instant git rollback
│   │   ├── scaffold-readme.js  # Starter README.md generator
│   │   ├── archive.js          # Archived prototypes full-text search API
│   │   └── audit-and-metrics.js # NDJSON audit logger & velocity analytics
│   ├── utils/
│   │   └── sanitizer.js        # Secret token & PII redaction engine
│   └── cron/
│       └── maintenance.js      # Nightly R2 database backup & link-rot sweeper
├── d1/
│   └── schema.sql              # Cloudflare D1 SQL table schema
└── sheets/
    ├── Code.gs                 # Google Apps Script core intake engine
    ├── Sprint02_ContextOps.gs  # Context ops & triage severity calculator
    ├── Sprint03_Webhook.gs     # Service Token edge webhook emitter
    └── Sprint04_PromotionCallback.gs # Post-promotion row lock script
```

---

## Local Development

```bash
# 1. Start local edge emulation via Wrangler
npx wrangler pages dev .

# 2. Execute D1 database migrations locally
npx wrangler d1 execute DB --local --file=./d1/schema.sql
```
