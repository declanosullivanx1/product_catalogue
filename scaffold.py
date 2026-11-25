#!/usr/bin/env python3
"""
========================================================================================
Product Catalog & Backlog Engine — Complete Project Bootstrapper & Scaffolder
Target: Cloudflare Pages + Google Sheets Ingestion Gateway
Timestamp: November 25, 2026 — Ireland (GMT)
========================================================================================
"""

import os
import sys
import time
from datetime import datetime, timezone

def generate_uuidv7() -> str:
    """Generates an RFC 9562-compliant UUID v7 using 48-bit UNIX ms timestamp."""
    ms = int(time.time() * 1000)
    time_hex = f"{ms:012x}"

    rand_a = int.from_bytes(os.urandom(2), "big") & 0x0FFF
    rand_a_hex = f"{rand_a:03x}"

    rand_b = int.from_bytes(os.urandom(8), "big")
    rand_b = (rand_b & 0x3FFFFFFFFFFFFFFF) | 0x8000000000000000  # Variant 10xx
    rand_b_hex = f"{rand_b:016x}"

    return f"{time_hex[:8]}-{time_hex[8:12]}-7{rand_a_hex}-{rand_b_hex[:4]}-{rand_b_hex[4:]}"

def get_iso_timestamp() -> str:
    """Returns the current UTC ISO 8601 timestamp."""
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

FILES = {}

# ======================================================================================
# 1. ROOT ASSETS: index.html, project.html, intake.html, projects.json, taxonomy.json, README.md
# ======================================================================================

FILES["index.html"] = lambda u, t: f"""<!--
  UUIDv7: {u}
  Timestamp: {t}
-->
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Product Catalog</title>
  <meta name="description" content="Production catalog of web apps, CLIs, libraries, and APIs.">
  <meta name="x-build-uuid" content="{u}">
  <meta name="x-build-timestamp" content="{t}">

  <!-- Immediate light-first theme script (FOUC Prevention) -->
  <script>
    (function () {{
      let theme = 'light';
      try {{
        const saved = localStorage.getItem('theme');
        if (saved === 'dark' || saved === 'light') theme = saved;
      }} catch (e) {{}}
      document.documentElement.setAttribute('data-theme', theme);
    }})();
  </script>

  <!-- Pico.css v2 -->
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" crossorigin="anonymous">
  <!-- Tabulator v6.2 -->
  <link rel="stylesheet" href="https://unpkg.com/tabulator-tables@6.2.5/dist/css/tabulator.min.css" crossorigin="anonymous">
  <!-- Custom Styling -->
  <link rel="stylesheet" href="/css/custom.css">
</head>
<body>
  <header class="container header-container">
    <nav aria-label="Main Navigation">
      <ul>
        <li><strong>Product Catalog</strong></li>
      </ul>
      <ul>
        <li><a href="/intake.html" class="contrast outline" style="font-size:0.8rem; padding:0.3rem 0.6rem;">+ Backlog Intake</a></li>
        <li>
          <button id="theme-toggle" class="outline secondary theme-toggle-btn" type="button" aria-label="Toggle theme">
            <span id="theme-icon">🌙</span>
            <span id="theme-label" class="toggle-text">Dark Mode</span>
          </button>
        </li>
      </ul>
    </nav>
  </header>

  <main class="container">
    <section>
      <div class="lead-header">
        <p class="description-text">Production deployment index and software registry.</p>
      </div>

      <div id="table-status" role="status" aria-live="polite" class="status-message">
        <span aria-busy="true">Loading catalog & taxonomy data...</span>
      </div>

      <div id="projects-table" class="table-wrapper" role="region" aria-label="Projects Table"></div>
    </section>
  </main>

  <footer class="container footer-container">
    <small>All production web apps resolve to their canonical <code>*.pages.dev</code> alias.</small>
  </footer>

  <script>
    (function () {{
      const btn = document.getElementById('theme-toggle');
      const icon = document.getElementById('theme-icon');
      const label = document.getElementById('theme-label');
      function sync(t) {{
        const isD = t === 'dark';
        if (icon) icon.textContent = isD ? '☀️' : '🌙';
        if (label) label.textContent = isD ? 'Light Mode' : 'Dark Mode';
        if (btn) btn.setAttribute('aria-pressed', isD ? 'true' : 'false');
      }}
      let cTheme = document.documentElement.getAttribute('data-theme') || 'light';
      sync(cTheme);
      if (btn) {{
        btn.addEventListener('click', function () {{
          cTheme = cTheme === 'light' ? 'dark' : 'light';
          document.documentElement.setAttribute('data-theme', cTheme);
          try {{ localStorage.setItem('theme', cTheme); }} catch(e) {{}}
          sync(cTheme);
        }});
      }}
    }})();
  </script>

  <script src="https://unpkg.com/tabulator-tables@6.2.5/dist/js/tabulator.min.js" crossorigin="anonymous"></script>
  <script src="/js/app.js"></script>
</body>
</html>
"""

FILES["project.html"] = lambda u, t: f"""<!--
  UUIDv7: {u}
  Timestamp: {t}
-->
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Project Details</title>
  <meta name="x-build-uuid" content="{u}">
  <meta name="x-build-timestamp" content="{t}">

  <script>
    (function () {{
      let theme = 'light';
      try {{
        const saved = localStorage.getItem('theme');
        if (saved === 'dark' || saved === 'light') theme = saved;
      }} catch (e) {{}}
      document.documentElement.setAttribute('data-theme', theme);
    }})();
  </script>

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css" crossorigin="anonymous">
  <link rel="stylesheet" href="/css/custom.css">
</head>
<body>
  <header class="container header-container">
    <nav aria-label="Breadcrumb Navigation">
      <ul>
        <li><a href="/" class="secondary">← Back to Catalog</a></li>
      </ul>
      <ul>
        <li>
          <button id="theme-toggle" class="outline secondary theme-toggle-btn" type="button" aria-label="Toggle theme">
            <span id="theme-icon">🌙</span>
            <span id="theme-label" class="toggle-text">Dark Mode</span>
          </button>
        </li>
      </ul>
    </nav>
  </header>

  <main class="container">
    <div id="detail-status" role="status" aria-live="polite">
      <span aria-busy="true">Loading project metadata...</span>
    </div>

    <article id="project-detail" style="display: none;">
      <header>
        <div style="display: flex; justify-content: space-between; align-items: flex-start; flex-wrap: wrap; gap: 0.5rem;">
          <div>
            <h1 id="proj-name" style="margin-bottom: 0.25rem;"></h1>
            <p id="proj-desc" class="description-text"></p>
          </div>
          <div>
            <a id="proj-canonical" class="contrast" target="_blank" rel="noopener noreferrer" role="button">Visit Live App ↗</a>
          </div>
        </div>
      </header>

      <section class="domain-banner">
        <span id="domain-icon" class="domain-icon">📁</span>
        <div>
          <strong id="domain-label">Domain</strong>
          <p id="domain-desc" style="margin: 0; font-size: 0.85rem; color: var(--pico-muted-color);"></p>
        </div>
      </section>

      <section class="detail-card">
        <h3>Taxonomy & Classification</h3>
        <div class="facet-grid">
          <div class="facet-item"><strong>Sub-Categories</strong><div id="sub-cat-list" class="tag-list"></div></div>
          <div class="facet-item"><strong>Tags</strong><div id="tag-list" class="tag-list"></div></div>
          <div class="facet-item"><strong>Platform</strong><div id="facet-platform" class="tag-list"></div></div>
          <div class="facet-item"><strong>Delivery Model</strong><div id="facet-delivery" class="tag-list"></div></div>
          <div class="facet-item"><strong>Monetization</strong><div id="facet-monetization" class="tag-list"></div></div>
          <div class="facet-item"><strong>AI Integration</strong><div id="facet-ai" class="tag-list"></div></div>
        </div>
      </section>

      <section class="detail-card">
        <h3>Deployment Versions</h3>
        <p style="font-size: 0.85rem; color: var(--pico-muted-color);">
          Production deployments hosted on Cloudflare Pages (<code>https://&lt;hash&gt;.&lt;project&gt;.pages.dev</code>).
        </p>
        <ul id="version-list" class="version-list"></ul>
      </section>
    </article>
  </main>

  <script>
    (function () {{
      const btn = document.getElementById('theme-toggle');
      const icon = document.getElementById('theme-icon');
      const label = document.getElementById('theme-label');
      function sync(t) {{
        const isD = t === 'dark';
        if (icon) icon.textContent = isD ? '☀️' : '🌙';
        if (label) label.textContent = isD ? 'Light' : 'Dark';
      }}
      let cTheme = document.documentElement.getAttribute('data-theme') || 'light';
      sync(cTheme);
      if (btn) {{
        btn.addEventListener('click', function () {{
          cTheme = cTheme === 'light' ? 'dark' : 'light';
          document.documentElement.setAttribute('data-theme', cTheme);
          try {{ localStorage.setItem('theme', cTheme); }} catch(e) {{}}
          sync(cTheme);
        }});
      }}
    }})();
  </script>

  <script src="/js/detail.js"></script>
</body>
</html>
"""

FILES["intake.html"] = lambda u, t: f"""<!--
  UUIDv7: {u}
  Timestamp: {t}
-->
<!DOCTYPE html>
<html lang="en" data-theme="light">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Catalog Backlog — Intake Terminal</title>
  <meta name="x-build-uuid" content="{u}">
  <meta name="x-build-timestamp" content="{t}">

  <script>
    (function () {{
      let theme = 'light';
      try {{
        const saved = localStorage.getItem('theme');
        if (saved === 'dark' || saved === 'light') theme = saved;
      }} catch (e) {{}}
      document.documentElement.setAttribute('data-theme', theme);
    }})();
  </script>

  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@2/css/pico.min.css">
  <style>
    :root {{ --pico-font-size: 88%; }}
    .status-badge {{ font-size: 0.75rem; padding: 0.2rem 0.5rem; border-radius: 4px; font-weight: 600; }}
    .badge-saved {{ background-color: var(--pico-ins-color); color: white; }}
    .badge-dirty {{ background-color: var(--pico-del-color); color: white; }}
    .badge-avail {{ background-color: #137333; color: white; }}
    .badge-taken {{ background-color: #c5221f; color: white; }}
    .preflight-card {{
      border: 1px solid var(--pico-muted-border-color);
      padding: 1rem;
      border-radius: var(--pico-border-radius);
      margin-bottom: 1.5rem;
      background-color: var(--pico-card-background-color);
    }}
  </style>
</head>
<body>
  <header class="container">
    <nav>
      <ul><li><strong>Backlog Intake Cockpit</strong></li></ul>
      <ul>
        <li><span id="draft-status" class="status-badge badge-saved">Draft Clean</span></li>
        <li><a href="/" class="secondary">Back to Catalog</a></li>
      </ul>
    </nav>
  </header>

  <main class="container">
    <form id="intake-form">
      <div class="grid">
        <div>
          <label for="uuid-field">UUID v7 (Auto-Generated)
            <input type="text" id="uuid-field" readonly>
          </label>
        </div>
        <div>
          <label for="account-select">Google Account ID
            <select id="account-select" required>
              <option value="declanjosephosullivan@gmail.com">declanjosephosullivan@gmail.com (Default)</option>
              <option value="declanosullivanx1@gmail.com">declanosullivanx1@gmail.com</option>
              <option value="cathal.and.declan@gmail.com">cathal.and.declan@gmail.com</option>
              <option value="declanjosullivan86@gmail.com">declanjosullivan86@gmail.com</option>
              <option value="declanseer@gmail.com">declanseer@gmail.com</option>
              <option value="declanjoseph2025@gmail.com">declanjoseph2025@gmail.com</option>
              <option value="davewilson1x1@gmail.com">davewilson1x1@gmail.com</option>
              <option value="charlie.and.declan.osullivan@gmail.com">charlie.and.declan.osullivan@gmail.com</option>
              <option value="declan@transparency-x.com">declan@transparency-x.com</option>
              <option value="Other">Other</option>
            </select>
          </label>
        </div>
      </div>

      <div class="grid">
        <div>
          <label for="chat-link">Active Chat Session URL
            <input type="url" id="chat-link" placeholder="https://claude.ai/chat/..." required>
          </label>
        </div>
        <div>
          <label for="llm-select">LLM Account / Platform
            <select id="llm-select" required>
              <option value="">Select Platform...</option>
              <option value="Google AI Studio Web App">Google AI Studio Web App</option>
              <option value="Gemini Chat Web App">Gemini Chat Web App</option>
              <option value="Qwen AI Studio">Qwen AI Studio</option>
              <option value="Kimi AI">Kimi AI</option>
              <option value="ChatGPT Web App">ChatGPT Web App</option>
              <option value="Claude AI Web App">Claude AI Web App</option>
              <option value="Other">Other</option>
            </select>
          </label>
        </div>
      </div>

      <div class="grid">
        <div>
          <label for="project-title">Project Title
            <input type="text" id="project-title" placeholder="e.g. Edge Image Transformer" required>
          </label>
        </div>
        <div>
          <label>Target Pages Subdomain
            <div style="display:flex; align-items:center; gap:0.5rem;">
              <input type="text" id="slug-preview" placeholder="edge-image-transformer" readonly>
              <span id="domain-badge" class="status-badge" style="display:none;">Probing...</span>
            </div>
          </label>
        </div>
      </div>

      <label for="project-desc">Description / Target Function
        <textarea id="project-desc" placeholder="One-line summary of what was built in this chat..."></textarea>
      </label>

      <details>
        <summary><strong>Raw Chat / Artifact Import Zone (Extract Code)</strong></summary>
        <textarea id="raw-chat-dump" placeholder="Paste full chat text or Claude <antArtifact> code here..."></textarea>
        <button type="button" id="extract-code-btn" class="secondary outline" style="margin-bottom:1rem;">
          Extract Clean Code into Notes
        </button>
      </details>

      <div class="grid">
        <div>
          <label for="project-notes">Architecture Notes & Implementation Details
            <textarea id="project-notes" style="min-height:120px;" placeholder="Architecture details, dependencies, extracted code..."></textarea>
          </label>
        </div>
        <div>
          <label for="project-issues">Bugs & Issues Checklist (Use [BLOCKER] for fatal bugs)
            <textarea id="project-issues" style="min-height:120px;" placeholder="- [ ] [BLOCKER] Token refresh fails on mobile&#10;- [ ] [POLISH] Update footer font size"></textarea>
          </label>
        </div>
      </div>

      <div class="preflight-card">
        <strong>Pre-Flight Telemetry:</strong>
        <div class="grid" style="margin-top:0.5rem;">
          <div>Context Window Load: <span id="telemetry-context">0 tokens (Healthy)</span></div>
          <div>Checklist Status: <span id="telemetry-checklist">No tasks</span></div>
          <div>Promotion Gate: <span id="telemetry-gate" style="color:var(--pico-ins-color);">READY</span></div>
        </div>
      </div>

      <div class="grid">
        <button type="button" id="copy-tsv-btn" class="contrast">Copy Row for Google Sheets</button>
        <button type="button" id="catchup-prompt-btn" class="secondary">Copy Catch-Up Prompt for AI</button>
        <button type="button" id="clear-draft-btn" class="secondary outline">Reset Draft</button>
      </div>
    </form>
  </main>

  <script src="/js/intake.js"></script>
  <script src="/js/triage.js"></script>
  <script>
    const titleInput = document.getElementById('project-title');
    const slugInput = document.getElementById('slug-preview');
    const domainBadge = document.getElementById('domain-badge');
    const issuesInput = document.getElementById('project-issues');
    const notesInput = document.getElementById('project-notes');
    const rawDump = document.getElementById('raw-chat-dump');
    const gateStatus = document.getElementById('telemetry-gate');
    const checklistStatus = document.getElementById('telemetry-checklist');
    const contextStatus = document.getElementById('telemetry-context');

    titleInput.addEventListener('input', () => {{
      const slug = titleInput.value.toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/(^-|-$)/g, '');
      slugInput.value = slug ? `${{slug}}.pages.dev` : '';
      if (slug) {{
        domainBadge.style.display = 'inline-block';
        domainBadge.textContent = 'Probing DNS...';
        domainBadge.className = 'status-badge';
        window.probePagesSubdomain(slug, (status) => {{
          if (status === 'AVAILABLE') {{
            domainBadge.textContent = 'Domain Available';
            domainBadge.className = 'status-badge badge-avail';
          }} else if (status === 'TAKEN') {{
            domainBadge.textContent = 'Subdomain Taken';
            domainBadge.className = 'status-badge badge-taken';
          }} else {{
            domainBadge.style.display = 'none';
          }}
        }});
      }} else {{
        domainBadge.style.display = 'none';
      }}
    }});

    document.getElementById('extract-code-btn').addEventListener('click', () => {{
      const extracted = window.extractArtifacts(rawDump.value);
      if (extracted) {{
        notesInput.value = (notesInput.value ? notesInput.value + "\\n\\n" : "") + extracted;
        rawDump.value = "";
        alert("Extracted clean code artifacts into Notes field!");
      }} else {{
        alert("No code blocks or <antArtifact> tags detected in paste.");
      }}
    }});

    document.getElementById('catchup-prompt-btn').addEventListener('click', () => {{
      const prompt = window.generateCatchUpPrompt(
        titleInput.value,
        document.getElementById('project-desc').value,
        notesInput.value,
        issuesInput.value,
        document.getElementById('llm-select').value
      );
      navigator.clipboard.writeText(prompt).then(() => {{
        alert("Catch-Up Prompt copied to clipboard! Paste directly into your LLM chat.");
      }});
    }});

    function updateTelemetry() {{
      const hasBlocker = issuesInput.value.toUpperCase().includes('[BLOCKER]');
      if (hasBlocker) {{
        gateStatus.textContent = 'LOCKED ([BLOCKER] Present)';
        gateStatus.style.color = '#c5221f';
      }} else {{
        gateStatus.textContent = 'READY FOR PROMOTION';
        gateStatus.style.color = 'var(--pico-ins-color)';
      }}
      const matches = issuesInput.value.match(/- \[[ xX]\]/g);
      if (matches) {{
        const done = (issuesInput.value.match(/- \[[xX]\]/g) || []).length;
        checklistStatus.textContent = `${{done}}/${{matches.length}} Tasks Closed (${{Math.round((done/matches.length)*100)}}%)`;
      }} else {{
        checklistStatus.textContent = 'No markdown checklist';
      }}
      const tokens = Math.ceil(((notesInput.value || "").length + (issuesInput.value || "").length) / 4);
      contextStatus.textContent = `~${{tokens.toLocaleString()}} tokens`;
    }}

    issuesInput.addEventListener('input', updateTelemetry);
    notesInput.addEventListener('input', updateTelemetry);
  </script>
</body>
</html>
"""

FILES["projects.json"] = lambda u, t: f"""[
  {{
    "_meta": {{
      "uuid_v7": "{u}",
      "timestamp": "{t}"
    }},
    "slug": "aura-scaler",
    "name": "Aura Scaler",
    "description": "Dynamic WebP/AVIF image transformation pipeline running on Cloudflare Workers.",
    "type": "SPA",
    "cfProjectName": "aura-scaler-python",
    "canonicalOverride": null,
    "status": "Production",
    "primary_domain": "visual_imaging",
    "sub_categories": ["image_generation", "data_visualization"],
    "tags": ["image-optimization", "webp", "avif", "edge-compute"],
    "platform": ["web", "api_only"],
    "delivery_model": ["saas"],
    "monetization": ["freemium"],
    "ai_integration": "ai_assisted",
    "versions": [
      {{ "hash": "a0a5e86", "date": "2026-11-21", "label": "v1.2.0" }},
      {{ "hash": "8f3b129", "date": "2026-10-15", "label": "v1.1.0" }}
    ]
  }},
  {{
    "slug": "hexgrid-engine",
    "name": "HexGrid Engine",
    "description": "Discrete procedural terrain generator with interactive SVG rendering.",
    "type": "SPA",
    "cfProjectName": "hex-grid-engine",
    "canonicalOverride": null,
    "status": "Production",
    "primary_domain": "entertainment_media",
    "sub_categories": ["gaming", "interactive_storytelling"],
    "tags": ["procedural-generation", "svg", "hexgrid", "game-dev"],
    "platform": ["web"],
    "delivery_model": ["pwa"],
    "monetization": ["open_source"],
    "ai_integration": "none",
    "versions": [
      {{ "hash": "c4d1e2f", "date": "2026-11-10", "label": "v0.9.4" }}
    ]
  }},
  {{
    "slug": "k8s-pod-reaper",
    "name": "k8s-pod-reaper",
    "description": "Lightweight Rust CLI daemon that sweeps and terminates orphaned development pods.",
    "type": "CLI",
    "cfProjectName": null,
    "canonicalOverride": "https://github.com/example/k8s-pod-reaper",
    "status": "Active",
    "primary_domain": "developer_technical_tools",
    "sub_categories": ["devops_cicd", "infrastructure_cloud"],
    "tags": ["kubernetes", "rust", "cli", "devops", "cleanup"],
    "platform": ["cli", "desktop_linux"],
    "delivery_model": ["native_app"],
    "monetization": ["open_source"],
    "ai_integration": "none",
    "versions": []
  }},
  {{
    "slug": "py-geo-locator",
    "name": "py-geo-locator",
    "description": "Fast memory-mapped MaxMind DB query wrapper with zero runtime dependencies.",
    "type": "Library",
    "cfProjectName": null,
    "canonicalOverride": "https://pypi.org/project/py-geo-locator/",
    "status": "Active",
    "primary_domain": "navigation_location",
    "sub_categories": ["maps_directions", "fleet_logistics"],
    "tags": ["python", "maxmind", "geoip", "zero-dependency"],
    "platform": ["api_only"],
    "delivery_model": ["sdk_library"],
    "monetization": ["open_source"],
    "ai_integration": "none",
    "versions": []
  }},
  {{
    "slug": "statusping-edge-api",
    "name": "StatusPing Edge API",
    "description": "Multi-region synthetic ping monitor running across distributed edge nodes.",
    "type": "API",
    "cfProjectName": null,
    "canonicalOverride": "https://api.statusping.dev",
    "status": "Beta",
    "primary_domain": "developer_technical_tools",
    "sub_categories": ["devops_cicd", "infrastructure_cloud"],
    "tags": ["synthetic-monitoring", "uptime", "edge-network"],
    "platform": ["api_only"],
    "delivery_model": ["saas"],
    "monetization": ["subscription"],
    "ai_integration": "none",
    "versions": []
  }}
]
"""

FILES["taxonomy.json"] = lambda u, t: f"""{{
  "_meta": {{
    "uuid_v7": "{u}",
    "timestamp": "{t}"
  }},
  "version": "1.0.0",
  "lastUpdated": "{t[:10]}",
  "schema": {{
    "primary_domain": {{ "type": "single-select", "required": true, "label": "Primary Domain" }},
    "secondary_domains": {{ "type": "multi-select", "required": false, "label": "Secondary Domains" }},
    "sub_categories": {{ "type": "multi-select", "required": false, "label": "Sub-Categories" }},
    "tags": {{ "type": "freeform-tags", "required": false, "label": "Tags" }}
  }},
  "domains": [
    {{ "id": "audio_sound", "label": "Audio & Sound", "icon": "🎵", "description": "Music, podcasts, sound design, voice" }},
    {{ "id": "visual_imaging", "label": "Visual & Imaging", "icon": "👁️", "description": "Photography, video, graphics, animation" }},
    {{ "id": "text_language", "label": "Text & Language", "icon": "✍️", "description": "Writing, translation, NLP, documentation" }},
    {{ "id": "research_knowledge", "label": "Research & Knowledge", "icon": "🔬", "description": "Academic, scientific, data gathering, reference" }},
    {{ "id": "business_enterprise", "label": "Business & Enterprise", "icon": "💼", "description": "Operations, strategy, management, B2B tools" }},
    {{ "id": "finance_economics", "label": "Finance & Economics", "icon": "💰", "description": "Banking, investing, accounting, fintech" }},
    {{ "id": "education_learning", "label": "Education & Learning", "icon": "📚", "description": "EdTech, courses, tutoring, skill-building" }},
    {{ "id": "health_wellness", "label": "Health & Wellness", "icon": "🏥", "description": "Fitness, mental health, medical, nutrition" }},
    {{ "id": "social_communication", "label": "Social & Communication", "icon": "💬", "description": "Messaging, networking, community, collaboration" }},
    {{ "id": "entertainment_media", "label": "Entertainment & Media", "icon": "🎮", "description": "Streaming, gaming, content consumption" }},
    {{ "id": "commerce_retail", "label": "Commerce & Retail", "icon": "🛒", "description": "E-commerce, marketplaces, shopping" }},
    {{ "id": "productivity_organization", "label": "Productivity & Organization", "icon": "⚡", "description": "Task management, notes, scheduling, workflow" }},
    {{ "id": "developer_technical_tools", "label": "Developer & Technical Tools", "icon": "🛠️", "description": "IDEs, APIs, DevOps, testing, infrastructure" }},
    {{ "id": "data_analytics", "label": "Data & Analytics", "icon": "📊", "description": "BI, visualization, data pipelines, ML/AI" }},
    {{ "id": "design_creative", "label": "Design & Creative", "icon": "🎨", "description": "UI/UX, branding, prototyping, industrial design" }},
    {{ "id": "marketing_growth", "label": "Marketing & Growth", "icon": "📣", "description": "SEO, advertising, CRM, email campaigns" }},
    {{ "id": "security_privacy", "label": "Security & Privacy", "icon": "🔒", "description": "Cybersecurity, encryption, identity, compliance" }},
    {{ "id": "navigation_location", "label": "Navigation & Location", "icon": "🗺️", "description": "Maps, GPS, travel, logistics, geospatial" }},
    {{ "id": "home_lifestyle", "label": "Home & Lifestyle", "icon": "🏠", "description": "Smart home, cooking, fashion, hobbies" }},
    {{ "id": "legal_governance", "label": "Legal & Governance", "icon": "⚖️", "description": "Contracts, compliance, policy, civic tech" }},
    {{ "id": "science_engineering", "label": "Science & Engineering", "icon": "🔭", "description": "Simulation, lab tools, CAD, R&D" }},
    {{ "id": "environment_sustainability", "label": "Environment & Sustainability", "icon": "🌍", "description": "Climate, energy, agriculture, conservation" }},
    {{ "id": "real_estate_property", "label": "Real Estate & Property", "icon": "🏗️", "description": "Listings, property management, construction" }},
    {{ "id": "transportation_mobility", "label": "Transportation & Mobility", "icon": "🚗", "description": "Ride-sharing, fleet, autonomous, delivery" }},
    {{ "id": "government_public_sector", "label": "Government & Public Sector", "icon": "🏛️", "description": "Civic services, public records, e-governance" }},
    {{ "id": "human_resources_talent", "label": "Human Resources & Talent", "icon": "👥", "description": "Recruiting, payroll, performance, culture" }},
    {{ "id": "events_experiences", "label": "Events & Experiences", "icon": "🎪", "description": "Ticketing, planning, virtual events, hospitality" }},
    {{ "id": "agriculture_food_systems", "label": "Agriculture & Food Systems", "icon": "🌾", "description": "Farming, supply chain, food tech, restaurant" }},
    {{ "id": "sports_recreation", "label": "Sports & Recreation", "icon": "⚽", "description": "Athletics, coaching, outdoor, fantasy sports" }},
    {{ "id": "accessibility_inclusion", "label": "Accessibility & Inclusion", "icon": "♿", "description": "Assistive tech, universal design, equity tools" }}
  ],
  "facets": {{
    "platform": {{
      "label": "Platform",
      "options": [
        {{ "id": "web", "label": "Web" }},
        {{ "id": "cli", "label": "CLI" }},
        {{ "id": "api_only", "label": "API-only" }},
        {{ "id": "desktop_linux", "label": "Desktop (Linux)" }},
        {{ "id": "desktop_macos", "label": "Desktop (macOS)" }},
        {{ "id": "desktop_windows", "label": "Desktop (Windows)" }},
        {{ "id": "ios", "label": "iOS" }},
        {{ "id": "android", "label": "Android" }}
      ]
    }},
    "delivery_model": {{
      "label": "Delivery Model",
      "options": [
        {{ "id": "saas", "label": "SaaS" }},
        {{ "id": "pwa", "label": "PWA" }},
        {{ "id": "native_app", "label": "Native App" }},
        {{ "id": "sdk_library", "label": "SDK / Library" }}
      ]
    }},
    "monetization": {{
      "label": "Monetization",
      "options": [
        {{ "id": "open_source", "label": "Open Source" }},
        {{ "id": "free", "label": "Free" }},
        {{ "id": "freemium", "label": "Freemium" }},
        {{ "id": "subscription", "label": "Subscription" }}
      ]
    }},
    "ai_integration": {{
      "label": "AI/ML Integration",
      "options": [
        {{ "id": "none", "label": "None" }},
        {{ "id": "ai_assisted", "label": "AI-Assisted" }},
        {{ "id": "ai_powered", "label": "AI-Powered" }},
        {{ "id": "generative_ai", "label": "Generative AI" }}
      ]
    }}
  }}
}}
"""

FILES["README.md"] = lambda u, t: f"""<!--
  UUIDv7: {u}
  Timestamp: {t}
-->
# Product Catalog & Backlog Engine

A static-first personal product catalog and edge-synchronized generative backlog engine deployed on Cloudflare Pages.

- **Build UUIDv7:** `{u}`
- **Generated:** `{t}`
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
"""

# ======================================================================================
# 2. STYLES & CLIENT JS: css/custom.css, js/app.js, js/detail.js, js/intake.js, js/triage.js
# ======================================================================================

FILES["css/custom.css"] = lambda u, t: f"""/*
  UUIDv7: {u}
  Timestamp: {t}
*/

:root {{
  --table-border-radius: 8px;
  --table-font-size: 0.9rem;
}}

body {{
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}}

main.container {{
  flex: 1 0 auto;
  padding-top: 0.75rem;
  padding-bottom: 2rem;
}}

.header-container {{
  padding-top: 0.75rem;
  padding-bottom: 0.5rem;
}}

.footer-container {{
  padding-top: 1.5rem;
  padding-bottom: 1.5rem;
  border-top: 1px solid var(--pico-muted-border-color);
  text-align: center;
}}

.lead-header {{
  margin-bottom: 0.75rem;
}}

.description-text {{
  margin-bottom: 0;
  color: var(--pico-muted-color);
  font-size: 0.95rem;
}}

.theme-toggle-btn {{
  padding: 0.35rem 0.75rem;
  font-size: 0.85rem;
  margin-bottom: 0;
  display: inline-flex;
  align-items: center;
  gap: 0.35rem;
  cursor: pointer;
}}

.status-message {{
  margin: 1rem 0;
  font-size: 0.95rem;
}}

.table-wrapper {{
  border-radius: var(--table-border-radius);
  overflow-x: auto;
  box-shadow: var(--pico-box-shadow);
  border: 1px solid var(--pico-muted-border-color);
  outline: none;
}}

.table-wrapper:focus-within {{
  border-color: var(--pico-primary);
}}

.tabulator {{
  background-color: var(--pico-background-color) !important;
  color: var(--pico-color) !important;
  font-family: inherit !important;
  font-size: var(--table-font-size) !important;
  border: none !important;
}}

.tabulator .tabulator-header {{
  background-color: var(--pico-card-background-color) !important;
  border-bottom: 2px solid var(--pico-muted-border-color) !important;
  color: var(--pico-color) !important;
  font-weight: 600;
}}

.tabulator .tabulator-header .tabulator-col {{
  background-color: var(--pico-card-background-color) !important;
  border-right: 1px solid var(--pico-muted-border-color) !important;
}}

.tabulator .tabulator-header .tabulator-col .tabulator-col-content {{
  padding: 0.5rem 0.4rem !important;
}}

/* --- FIX FOR OVERLAPPING MAGNIFYING GLASS & FILTER BOXES --- */
.tabulator .tabulator-header .tabulator-col input,
.tabulator .tabulator-header .tabulator-col select {{
  background-image: none !important;
  -webkit-appearance: none !important;
  -moz-appearance: none !important;
  appearance: none !important;
  padding: 0.35rem 0.5rem !important;
  padding-inline-start: 0.5rem !important;
  padding-inline-end: 0.5rem !important;
  font-size: 14px !important;
  border: 1px solid var(--pico-muted-border-color) !important;
  border-radius: var(--pico-border-radius) !important;
  background-color: var(--pico-background-color) !important;
  color: var(--pico-color) !important;
  height: 32px !important;
  min-height: 32px !important;
  line-height: normal !important;
  width: 100% !important;
  box-sizing: border-box !important;
  box-shadow: none !important;
}}

.tabulator .tabulator-header .tabulator-col input::-webkit-search-decoration,
.tabulator .tabulator-header .tabulator-col input::-webkit-search-cancel-button,
.tabulator .tabulator-header .tabulator-col input::-webkit-search-results-button,
.tabulator .tabulator-header .tabulator-col input::-webkit-search-results-decoration {{
  display: none !important;
  -webkit-appearance: none !important;
}}

.tabulator .tabulator-header .tabulator-col .tabulator-col-sorter .tabulator-arrow {{
  border-bottom-color: var(--pico-muted-color) !important;
}}

[data-theme="dark"] .tabulator .tabulator-header .tabulator-col .tabulator-col-sorter .tabulator-arrow {{
  border-bottom-color: var(--pico-color) !important;
}}

.tabulator .tabulator-header .tabulator-col.tabulator-sortable[aria-sort="ascending"] .tabulator-arrow {{
  border-bottom-color: var(--pico-primary) !important;
}}

.tabulator .tabulator-header .tabulator-col.tabulator-sortable[aria-sort="descending"] .tabulator-arrow {{
  border-top-color: var(--pico-primary) !important;
}}

.tabulator .tabulator-row {{
  background-color: var(--pico-background-color) !important;
  color: var(--pico-color) !important;
  border-bottom: 1px solid var(--pico-muted-border-color) !important;
  min-height: 44px;
}}

.tabulator .tabulator-row:nth-child(even) {{
  background-color: var(--pico-card-background-color) !important;
}}

.tabulator .tabulator-row:hover {{
  background-color: var(--pico-primary-background) !important;
}}

.tabulator .tabulator-cell {{
  padding: 0.5rem 0.5rem !important;
  border-right: 1px solid var(--pico-muted-border-color) !important;
  display: inline-flex;
  align-items: center;
}}

.tabulator-cell a.canonical-link,
.tabulator-responsive-collapse a.canonical-link,
a.project-title-link {{
  color: var(--pico-primary) !important;
  text-decoration: underline;
  word-break: break-all;
  outline: none;
}}

a.project-title-link {{
  font-weight: 700;
  text-decoration: none;
}}

a.project-title-link:hover {{
  text-decoration: underline;
}}

.badge {{
  display: inline-flex;
  align-items: center;
  gap: 0.25rem;
  padding: 0.15rem 0.45rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  border: 1px solid var(--pico-muted-border-color);
  background-color: var(--pico-card-background-color);
  color: var(--pico-color);
  white-space: nowrap;
}}

.badge-domain {{
  border-color: var(--pico-primary);
  background-color: transparent;
  color: var(--pico-color);
}}

.tag-list {{
  display: flex;
  flex-wrap: wrap;
  gap: 0.3rem;
  margin: 0;
  padding: 0;
  list-style: none;
}}

.taxonomy-tag {{
  display: inline-block;
  padding: 0.1rem 0.4rem;
  border-radius: 12px;
  font-size: 0.72rem;
  background-color: var(--pico-muted-border-color);
  color: var(--pico-color);
}}

.tabulator-responsive-collapse {{
  padding: 0.75rem !important;
  background-color: var(--pico-card-background-color) !important;
  border-bottom: 1px solid var(--pico-muted-border-color) !important;
}}

.tabulator-responsive-collapse dl {{
  margin: 0;
  display: grid;
  grid-template-columns: 110px 1fr;
  gap: 0.4rem 0.75rem;
  font-size: 0.85rem;
}}

.tabulator-responsive-collapse dt {{
  font-weight: 600;
  color: var(--pico-muted-color);
}}

.tabulator-responsive-collapse dd {{
  margin: 0;
  word-break: break-word;
}}

.tabulator-row .tabulator-responsive-collapse-toggle {{
  display: inline-flex !important;
  align-items: center;
  justify-content: center;
  min-width: 32px;
  min-height: 32px;
  cursor: pointer;
  border-radius: 4px;
  outline: none;
  user-select: none;
}}

.tabulator-row .tabulator-responsive-collapse-toggle:focus-visible {{
  outline: 2px solid var(--pico-primary) !important;
}}

.detail-card {{
  padding: 1.5rem;
  border-radius: var(--table-border-radius);
  border: 1px solid var(--pico-muted-border-color);
  background-color: var(--pico-card-background-color);
  margin-bottom: 1.5rem;
}}

.domain-banner {{
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border-radius: var(--pico-border-radius);
  background-color: var(--pico-background-color);
  border: 1px solid var(--pico-muted-border-color);
  margin-bottom: 1.25rem;
}}

.domain-banner .domain-icon {{
  font-size: 1.8rem;
}}

.facet-grid {{
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 1rem;
  margin-top: 1rem;
}}

.facet-item strong {{
  display: block;
  font-size: 0.75rem;
  text-transform: uppercase;
  color: var(--pico-muted-color);
  margin-bottom: 0.25rem;
}}

.version-list {{
  list-style: none;
  padding: 0;
  margin: 0;
}}

.version-item {{
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.6rem 0;
  border-bottom: 1px solid var(--pico-muted-border-color);
}}

.version-item:last-child {{
  border-bottom: none;
}}

@media (max-width: 480px) {{
  :root {{
    --table-font-size: 0.85rem;
  }}
  main.container {{
    padding-left: 0.5rem;
    padding-right: 0.5rem;
  }}
  .toggle-text {{
    display: none;
  }}
  .theme-toggle-btn {{
    padding: 0.4rem 0.6rem;
  }}
}}
"""

FILES["js/app.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Main Catalog Table Controller
 */

(function () {{
  'use strict';

  function sanitizeUrl(rawUrl) {{
    if (!rawUrl || typeof rawUrl !== 'string') return '#';
    const trimmed = rawUrl.trim();
    if (/^(javascript|data|vbscript):/i.test(trimmed)) return '#';
    if (!/^https?:\\/\\//i.test(trimmed) && !trimmed.startsWith('#')) {{
      return 'https://' + trimmed;
    }}
    try {{
      const parsed = new URL(trimmed);
      if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {{
        return parsed.href;
      }}
    }} catch (err) {{}}
    return '#';
  }}

  function resolveCanonicalUrl(entry) {{
    if (entry.canonicalOverride) return sanitizeUrl(entry.canonicalOverride);
    if (entry.cfProjectName) return 'https://' + encodeURIComponent(entry.cfProjectName.trim()) + '.pages.dev';
    return '#';
  }}

  function createSafeLink(text, url, className) {{
    const a = document.createElement('a');
    a.href = sanitizeUrl(url);
    a.className = className || 'canonical-link';
    a.textContent = text || url;
    if (!url.startsWith('#') && !url.startsWith('/')) {{
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    }}
    return a;
  }}

  function initTable(projects, taxonomy) {{
    const statusEl = document.getElementById('table-status');

    const domainMap = new Map();
    (taxonomy.domains || []).forEach(function (d) {{
      domainMap.set(d.id, {{ label: d.label, icon: d.icon || '📁' }});
    }});

    const processedData = projects.map(function (item) {{
      const dom = domainMap.get(item.primary_domain) || {{ label: 'General', icon: '📦' }};
      return {{
        slug: item.slug || '',
        name: item.name || 'Untitled',
        description: item.description || '',
        type: item.type || 'Other',
        domainId: item.primary_domain || '',
        domainLabel: dom.label,
        domainDisplay: dom.icon + ' ' + dom.label,
        subCategories: item.sub_categories || [],
        tags: item.tags || [],
        canonicalUrl: resolveCanonicalUrl(item),
        status: item.status || 'Active',
        platform: item.platform || [],
        cfProjectName: item.cfProjectName || null
      }};
    }});

    try {{
      const table = new Tabulator('#projects-table', {{
        data: processedData,
        layout: 'fitColumns',
        responsiveLayout: 'collapse',
        responsiveLayoutCollapseStartOpen: false,
        placeholder: 'No matching projects found.',

        responsiveLayoutCollapseFormatter: function (data) {{
          const dl = document.createElement('dl');
          const rowData = data[0] ? data[0].getRow().getData() : null;

          data.forEach(function (col) {{
            if (col.value !== undefined && col.title && col.field !== 'domainDisplay') {{
              const dt = document.createElement('dt');
              dt.textContent = col.title;
              const dd = document.createElement('dd');

              if (col.field === 'canonicalUrl') {{
                dd.appendChild(createSafeLink(col.value, col.value));
              }} else {{
                dd.textContent = col.value;
              }}
              dl.appendChild(dt);
              dl.appendChild(dd);
            }}
          }});

          if (rowData && rowData.tags && rowData.tags.length > 0) {{
            const dtTags = document.createElement('dt');
            dtTags.textContent = 'Tags';
            const ddTags = document.createElement('dd');
            const ul = document.createElement('ul');
            ul.className = 'tag-list';
            rowData.tags.forEach(function (t) {{
              const li = document.createElement('li');
              li.className = 'taxonomy-tag';
              li.textContent = '#' + t;
              ul.appendChild(li);
            }});
            ddTags.appendChild(ul);
            dl.appendChild(dtTags);
            dl.appendChild(ddTags);
          }}

          return dl;
        }},

        rowFormatter: function (row) {{
          const toggle = row.getElement().querySelector('.tabulator-responsive-collapse-toggle');
          if (toggle && !toggle.dataset.a11yInit) {{
            toggle.dataset.a11yInit = 'true';
            toggle.setAttribute('tabindex', '0');
            toggle.setAttribute('role', 'button');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.setAttribute('aria-label', 'Toggle details');

            toggle.addEventListener('keydown', function (e) {{
              if (e.key === 'Enter' || e.key === ' ') {{
                e.preventDefault();
                toggle.click();
              }}
            }});

            toggle.addEventListener('click', function () {{
              const isOpen = toggle.classList.contains('open');
              toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            }});
          }}
        }},

        columns: [
          {{
            formatter: 'responsiveCollapse',
            width: 36,
            minWidth: 36,
            hozAlign: 'center',
            resizable: false,
            headerSort: false
          }},
          {{
            title: 'Project',
            field: 'name',
            minWidth: 140,
            responsive: 0,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Search...',
            headerFilterFunc: function (headerValue, rowValue, rowData) {{
              if (!headerValue) return true;
              const q = headerValue.toLowerCase().trim();
              const nameMatch = (rowData.name || '').toLowerCase().includes(q);
              const descMatch = (rowData.description || '').toLowerCase().includes(q);
              const domainMatch = (rowData.domainLabel || '').toLowerCase().includes(q);
              const tagMatch = (rowData.tags || []).some(function (t) {{ return t.toLowerCase().includes(q); }});
              return nameMatch || descMatch || domainMatch || tagMatch;
            }},
            formatter: function (cell) {{
              const row = cell.getRow().getData();
              const container = document.createElement('div');
              const link = document.createElement('a');
              link.href = 'project.html?p=' + encodeURIComponent(row.slug);
              link.className = 'project-title-link';
              link.textContent = cell.getValue();
              container.appendChild(link);
              return container;
            }}
          }},
          {{
            title: 'Primary Domain',
            field: 'domainDisplay',
            minWidth: 160,
            responsive: 1,
            headerFilter: 'list',
            headerFilterParams: {{ valuesLookup: true, clearable: true }},
            headerFilterPlaceholder: 'All Domains',
            formatter: function (cell) {{
              const span = document.createElement('span');
              span.className = 'badge badge-domain';
              span.textContent = cell.getValue();
              return span;
            }}
          }},
          {{
            title: 'Canonical URL',
            field: 'canonicalUrl',
            minWidth: 160,
            responsive: 2,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Filter URL...',
            formatter: function (cell) {{
              return createSafeLink(cell.getValue(), cell.getValue());
            }}
          }},
          {{
            title: 'Type',
            field: 'type',
            width: 90,
            responsive: 3,
            hozAlign: 'center',
            headerFilter: 'list',
            headerFilterParams: {{ valuesLookup: true, clearable: true }},
            headerFilterPlaceholder: 'All',
            formatter: function (cell) {{
              const span = document.createElement('span');
              span.className = 'badge';
              span.textContent = cell.getValue();
              return span;
            }}
          }},
          {{
            title: 'Description',
            field: 'description',
            minWidth: 180,
            responsive: 4,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Filter text...'
          }},
          {{
            title: 'Status',
            field: 'status',
            width: 95,
            responsive: 5,
            hozAlign: 'center',
            formatter: function (cell) {{
              const span = document.createElement('span');
              span.className = 'badge';
              span.textContent = cell.getValue();
              return span;
            }}
          }}
        ]
      }});

      table.on('tableBuilt', function () {{
        if (statusEl) statusEl.remove();
      }});

    }} catch (err) {{
      if (statusEl) {{
        statusEl.innerHTML = '<span style="color: var(--pico-form-element-error-border-color);">' +
          'Failed to render catalog table: ' + err.message + '</span>';
      }}
    }}
  }}

  function initApp() {{
    const statusEl = document.getElementById('table-status');

    Promise.all([
      fetch('/projects.json', {{ cache: 'no-cache' }}).then(r => r.json()),
      fetch('/taxonomy.json', {{ cache: 'no-cache' }}).then(r => r.json())
    ])
    .then(results => {{
      initTable(results[0], results[1]);
    }})
    .catch(err => {{
      if (statusEl) {{
        statusEl.innerHTML = '<strong>Error loading catalog data:</strong> ' + err.message;
      }}
    }});
  }}

  if (document.readyState === 'loading') {{
    document.addEventListener('DOMContentLoaded', initApp);
  }} else {{
    initApp();
  }}
}})();
"""

FILES["js/detail.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Project Detail View Controller
 */

(function () {{
  'use strict';

  const params = new URLSearchParams(window.location.search);
  const slug = params.get('p');
  const statusEl = document.getElementById('detail-status');
  const articleEl = document.getElementById('project-detail');

  if (!slug) {{
    statusEl.innerHTML = '<strong>No project specified.</strong> <a href="/">Return to Catalog</a>';
    return;
  }}

  Promise.all([
    fetch('/projects.json').then(r => r.json()),
    fetch('/taxonomy.json').then(r => r.json())
  ])
  .then(results => {{
    const projects = results[0];
    const taxonomy = results[1];

    const project = projects.find(p => p.slug === slug);
    if (!project) {{
      statusEl.innerHTML = '<strong>Project not found.</strong> <a href="/">Return to Catalog</a>';
      return;
    }}

    document.getElementById('proj-name').textContent = project.name;
    document.getElementById('proj-desc').textContent = project.description;
    document.title = project.name + ' — Details';

    const canonicalUrl = project.canonicalOverride || (project.cfProjectName ? 'https://' + project.cfProjectName + '.pages.dev' : '#');
    const canonicalBtn = document.getElementById('proj-canonical');
    canonicalBtn.href = canonicalUrl;
    if (canonicalUrl === '#') canonicalBtn.style.display = 'none';

    const domain = (taxonomy.domains || []).find(d => d.id === project.primary_domain);
    if (domain) {{
      document.getElementById('domain-icon').textContent = domain.icon || '📁';
      document.getElementById('domain-label').textContent = domain.label;
      document.getElementById('domain-desc').textContent = domain.description || '';
    }}

    function renderChips(containerId, items, prefix) {{
      const container = document.getElementById(containerId);
      container.innerHTML = '';
      if (!items || items.length === 0) {{
        container.innerHTML = '<small style="color:var(--pico-muted-color);">None</small>';
        return;
      }}
      const arr = Array.isArray(items) ? items : [items];
      arr.forEach(val => {{
        const span = document.createElement('span');
        span.className = 'taxonomy-tag';
        span.textContent = (prefix || '') + val;
        container.appendChild(span);
      }});
    }}

    renderChips('sub-cat-list', project.sub_categories);
    renderChips('tag-list', project.tags, '#');
    renderChips('facet-platform', project.platform);
    renderChips('facet-delivery', project.delivery_model);
    renderChips('facet-monetization', project.monetization);
    renderChips('facet-ai', project.ai_integration);

    const versionList = document.getElementById('version-list');
    versionList.innerHTML = '';

    if (project.cfProjectName && project.versions && project.versions.length > 0) {{
      project.versions.forEach(v => {{
        const li = document.createElement('li');
        li.className = 'version-item';

        const left = document.createElement('div');
        const link = document.createElement('a');
        link.href = 'https://' + v.hash + '.' + project.cfProjectName + '.pages.dev';
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = v.hash + '.' + project.cfProjectName + '.pages.dev';
        left.appendChild(link);

        if (v.label) {{
          const badge = document.createElement('span');
          badge.className = 'badge';
          badge.style.marginLeft = '0.5rem';
          badge.textContent = v.label;
          left.appendChild(badge);
        }}

        const date = document.createElement('small');
        date.style.color = 'var(--pico-muted-color)';
        date.textContent = v.date || '';

        li.appendChild(left);
        li.appendChild(date);
        versionList.appendChild(li);
      }});
    }} else if (project.cfProjectName) {{
      versionList.innerHTML = '<li><small style="color:var(--pico-muted-color);">No version history available for this Cloudflare Pages project.</small></li>';
    }} else {{
      versionList.innerHTML = '<li><small style="color:var(--pico-muted-color);">No deployment version history available for external / non-Pages projects.</small></li>';
    }}

    statusEl.style.display = 'none';
    articleEl.style.display = 'block';
  }})
  .catch(err => {{
    statusEl.innerHTML = '<strong>Error loading project:</strong> ' + err.message;
  }});
}})();
"""

FILES["js/intake.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Client Intake Logic & LocalStorage Stash
 */

(function () {{
  'use strict';

  const STORAGE_KEY = 'catalog_intake_draft_v2';
  const statusBadge = document.getElementById('draft-status');

  function generateUUIDv7() {{
    const now = Date.now();
    const timeHex = now.toString(16).padStart(12, '0');
    const randA = Math.floor(Math.random() * 0x0FFF).toString(16).padStart(3, '0');
    const randB1 = (Math.floor(Math.random() * 0x3FFF) | 0x8000).toString(16).padStart(4, '0');
    const randB2 = Math.floor(Math.random() * 0xFFFFFFFFFFFF).toString(16).padStart(12, '0');
    return `${{timeHex.slice(0, 8)}}-${{timeHex.slice(8, 12)}}-7${{randA}}-${{randB1}}-${{randB2}}`;
  }}

  function setDirty(isDirty) {{
    if (!statusBadge) return;
    if (isDirty) {{
      statusBadge.textContent = 'Unsaved Changes';
      statusBadge.className = 'status-badge badge-dirty';
    }} else {{
      statusBadge.textContent = 'Draft Stashed';
      statusBadge.className = 'status-badge badge-saved';
    }}
  }}

  function detectPlatform(url) {{
    if (/aistudio\\.google\\.com/i.test(url)) return "Google AI Studio Web App";
    if (/gemini\\.google\\.com/i.test(url)) return "Gemini Chat Web App";
    if (/qwen|tongyi\\.aliyun/i.test(url)) return "Qwen AI Studio";
    if (/kimi\\.moonshot\\.cn/i.test(url)) return "Kimi AI";
    if (/chatgpt\\.com|chat\\.openai\\.com/i.test(url)) return "ChatGPT Web App";
    if (/claude\\.ai/i.test(url)) return "Claude AI Web App";
    return "";
  }}

  function saveToStorage() {{
    const payload = {{
      uuid: document.getElementById('uuid-field').value,
      account: document.getElementById('account-select').value,
      link: document.getElementById('chat-link').value,
      llm: document.getElementById('llm-select').value,
      title: document.getElementById('project-title').value,
      desc: document.getElementById('project-desc').value,
      notes: document.getElementById('project-notes').value,
      issues: document.getElementById('project-issues').value
    }};
    try {{
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
      setDirty(false);
    }} catch (e) {{}}
  }}

  function loadFromStorage() {{
    let saved = null;
    try {{
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) saved = JSON.parse(raw);
    }} catch (e) {{}}

    if (saved) {{
      document.getElementById('uuid-field').value = saved.uuid || generateUUIDv7();
      document.getElementById('account-select').value = saved.account || "declanjosephosullivan@gmail.com";
      document.getElementById('chat-link').value = saved.link || "";
      document.getElementById('llm-select').value = saved.llm || "";
      document.getElementById('project-title').value = saved.title || "";
      document.getElementById('project-desc').value = saved.desc || "";
      document.getElementById('project-notes').value = saved.notes || "";
      document.getElementById('project-issues').value = saved.issues || "";
      setDirty(false);
    }} else {{
      document.getElementById('uuid-field').value = generateUUIDv7();
      setDirty(false);
    }}
  }}

  document.getElementById('account-select').addEventListener('change', saveToStorage);
  document.getElementById('chat-link').addEventListener('input', (e) => {{
    const detected = detectPlatform(e.target.value);
    if (detected) document.getElementById('llm-select').value = detected;
    setDirty(true);
    saveToStorage();
  }});

  ['llm-select', 'project-title', 'project-desc', 'project-notes', 'project-issues'].forEach(id => {{
    document.getElementById(id).addEventListener('input', () => {{
      setDirty(true);
      saveToStorage();
    }});
  }});

  document.getElementById('clear-draft-btn').addEventListener('click', () => {{
    if (confirm("Reset current draft?")) {{
      localStorage.removeItem(STORAGE_KEY);
      document.getElementById('intake-form').reset();
      document.getElementById('uuid-field').value = generateUUIDv7();
      setDirty(false);
    }}
  }});

  document.getElementById('copy-tsv-btn').addEventListener('click', () => {{
    const row = [
      document.getElementById('uuid-field').value,
      document.getElementById('account-select').value,
      document.getElementById('llm-select').value,
      document.getElementById('chat-link').value,
      document.getElementById('project-title').value,
      document.getElementById('project-desc').value.replace(/\\n/g, ' '),
      document.getElementById('project-notes').value.replace(/\\n/g, ' '),
      document.getElementById('project-issues').value.replace(/\\n/g, ' ')
    ];
    navigator.clipboard.writeText(row.join('\\t')).then(() => {{
      alert("TSV Row copied to clipboard! Paste directly into Google Sheets (Column A).");
    }});
  }});

  loadFromStorage();
}})();
"""

FILES["js/triage.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Triage & Pre-flight Client Module
 */

(function () {{
  'use strict';

  window.extractArtifacts = function (rawText) {{
    if (!rawText || typeof rawText !== 'string') return "";
    let extracted = [];

    const claudeRegex = /<antArtifact\\s+[^>]*?language="([^"]*)"[^>]*?>([\\s\\S]*?)<\\/antArtifact>/gi;
    let match;
    while ((match = claudeRegex.exec(rawText)) !== null) {{
      const lang = match[1] || 'plaintext';
      const code = match[2].trim();
      extracted.push(`### [Extracted Artifact: ${{lang}}]\\n\\\`\\\`\\\`${{lang}}\\n${{code}}\\n\\\`\\\`\\\``);
    }}

    if (extracted.length === 0) {{
      const fenceRegex = /\\\`\\\`\\\`([a-zA-Z0-9_-]*)\\n([\\s\\S]*?)\\\`\\\`\\\`/g;
      while ((match = fenceRegex.exec(rawText)) !== null) {{
        const lang = match[1] || 'code';
        const code = match[2].trim();
        extracted.push(`\\\`\\\`\\\`${{lang}}\\n${{code}}\\n\\\`\\\`\\\``);
      }}
    }}
    return extracted.join("\\n\\n");
  }};

  let debounceTimer = null;
  window.probePagesSubdomain = function (slug, callback) {{
    clearTimeout(debounceTimer);
    if (!slug) {{
      callback('EMPTY');
      return;
    }}
    const clean = slug.toLowerCase().replace(/[^a-z0-9-]/g, '').trim();
    if (!clean) {{
      callback('INVALID');
      return;
    }}
    debounceTimer = setTimeout(() => {{
      fetch(`https://cloudflare-dns.com/dns-query?name=${{clean}}.pages.dev&type=CNAME`, {{
        headers: {{ "Accept": "application/dns-json" }}
      }})
      .then(res => res.json())
      .then(data => {{
        if (data.Status === 3) {{
          callback('AVAILABLE', clean);
        }} else if (data.Status === 0 && data.Answer) {{
          callback('TAKEN', clean);
        }} else {{
          callback('UNKNOWN', clean);
        }}
      }})
      .catch(() => callback('ERROR', clean));
    }}, 400);
  }};

  window.generateCatchUpPrompt = function (title, desc, notes, issues, llm) {{
    return [
      `# RESUME CODING SESSION: ${{title || 'Untitled Project'}}`,
      `**Platform:** ${{llm || 'Universal LLM'}} | **Date:** ${{new Date().toISOString().split('T')[0]}}`,
      `\\n## Target Objective\\n${{desc || 'No summary documented.'}}`,
      notes ? `\\n## Verified Architecture & Implementation\\n${{notes}}` : null,
      issues ? `\\n## Blockers & Defects to Solve Now\\n${{issues}}` : null,
      "\\n---",
      "Please review the state above. Address all [BLOCKER] items first. Provide the complete code fix."
    ].filter(Boolean).join("\\n");
  }};
}})();
"""

# ======================================================================================
# 3. EDGE FUNCTIONS: _middleware.js, sync.js, backlog.js, promote.js, verify-and-rollback.js,
#                   scaffold-readme.js, archive.js, audit-and-metrics.js, sanitizer.js, maintenance.js
# ======================================================================================

FILES["functions/_middleware.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Cloudflare Pages Edge Zero Trust Middleware
 */

let CACHED_JWKS = null;
let JWKS_EXPIRY = 0;

async function getAccessJwks(teamDomain) {{
  const now = Date.now();
  if (CACHED_JWKS && now < JWKS_EXPIRY) return CACHED_JWKS;
  const res = await fetch(`https://${{teamDomain}}/cdn-cgi/access/certs`, {{
    cf: {{ cacheTtl: 3600, cacheEverything: true }}
  }});
  if (!res.ok) throw new Error(`Failed to fetch JWKS: ${{res.status}}`);
  const data = await res.json();
  CACHED_JWKS = data.keys;
  JWKS_EXPIRY = now + 3600 * 1000;
  return CACHED_JWKS;
}}

export async function onRequest(context) {{
  const {{ request, env, next }} = context;
  const url = new URL(request.url);

  context.data.authenticated = false;
  context.data.authType = "anonymous";
  context.data.userEmail = null;
  context.data.groups = [];

  if (url.pathname.startsWith("/css/") || url.pathname.startsWith("/js/") || url.pathname === "/favicon.ico") {{
    return next();
  }}

  // 1. Service Token Authentication
  const clientId = request.headers.get("CF-Access-Client-Id");
  const clientSecret = request.headers.get("CF-Access-Client-Secret");
  if (clientId && clientSecret) {{
    if (clientId === env.CF_SERVICE_TOKEN_CLIENT_ID && clientSecret === env.CF_SERVICE_TOKEN_CLIENT_SECRET) {{
      context.data.authenticated = true;
      context.data.authType = "service_token";
      context.data.userEmail = "service-token@system.local";
      context.data.groups = ["system", "automation"];
      return next();
    }} else {{
      return new Response(JSON.stringify({{ error: "Invalid Service Token Credentials" }}), {{
        status: 403,
        headers: {{ "Content-Type": "application/json" }}
      }});
    }}
  }}

  // 2. User JWT Verification
  const jwt = request.headers.get("Cf-Access-Jwt-Assertion");
  if (jwt && env.CF_ACCESS_TEAM_DOMAIN && env.CF_ACCESS_AUD) {{
    try {{
      const parts = jwt.split(".");
      if (parts.length === 3) {{
        const header = JSON.parse(atob(parts[0].replace(/-/g, "+").replace(/_/g, "/")));
        const payload = JSON.parse(atob(parts[1].replace(/-/g, "+").replace(/_/g, "/")));
        const nowSec = Math.floor(Date.now() / 1000);
        if (payload.exp > nowSec && payload.aud.includes(env.CF_ACCESS_AUD)) {{
          const keys = await getAccessJwks(env.CF_ACCESS_TEAM_DOMAIN);
          const jwk = keys.find(k => k.kid === header.kid);
          if (jwk) {{
            const key = await crypto.subtle.importKey(
              "jwk", jwk, {{ name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }}, false, ["verify"]
            );
            const enc = new TextEncoder();
            const signedData = enc.encode(`${{parts[0]}}.${{parts[1]}}`);
            const signature = Uint8Array.from(atob(parts[2].replace(/-/g, "+").replace(/_/g, "/")), c => c.charCodeAt(0));
            const valid = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, signature, signedData);
            if (valid) {{
              context.data.authenticated = true;
              context.data.authType = "user_jwt";
              context.data.userEmail = payload.email || "unknown@user";
              context.data.groups = payload.custom_groups || [];
            }}
          }}
        }}
      }}
    }} catch (err) {{}}
  }}

  if (url.pathname.startsWith("/api/sync")) {{
    if (!context.data.authenticated) {{
      return new Response(JSON.stringify({{ error: "Unauthorized Zero Trust Perimeter" }}), {{
        status: 401,
        headers: {{ "Content-Type": "application/json" }}
      }});
    }}
  }}

  const response = await next();
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  return response;
}}
"""

FILES["functions/api/sync.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Edge Ingestion & Webhook Controller
 */

export async function onRequestPost(context) {{
  const {{ request, env, data }} = context;
  if (!data.authenticated) {{
    return new Response(JSON.stringify({{ error: "Unauthorized" }}), {{ status: 401 }});
  }}

  try {{
    const payload = await request.json();
    const {{ uuid, accountId, llmAccount, link, title, description, notes, issues, dataSensitivity }} = payload;

    if (!uuid || !accountId || !title || !link) {{
      return new Response(JSON.stringify({{ error: "Missing required fields" }}), {{ status: 400 }});
    }}

    const isCorporate = accountId.toLowerCase().includes("@transparency-x.com");
    const isConfidential = (dataSensitivity || "").toLowerCase() === "confidential";
    if (isConfidential && !isCorporate) {{
      return new Response(JSON.stringify({{
        error: "GOVERNANCE VIOLATION: Confidential project cannot be assigned to personal Gmail account.",
        accountId: accountId
      }}), {{ status: 422 }});
    }}

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

    return new Response(JSON.stringify({{
      success: true,
      uuid: uuid,
      syncedAt: new Date().toISOString()
    }}), {{ status: 200, headers: {{ "Content-Type": "application/json" }} }});
  }} catch (err) {{
    return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
  }}
}}
"""

FILES["functions/api/backlog.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * RBAC Sensitivity Slicing Endpoint
 */

export async function onRequestGet(context) {{
  const {{ env, data }} = context;
  try {{
    const isEngineer = data.authenticated && (
      data.authType === "service_token" ||
      (data.groups && data.groups.includes("engineering")) ||
      (data.userEmail && data.userEmail.endsWith("@transparency-x.com"))
    );

    let query = isEngineer
      ? "SELECT * FROM backlog_items ORDER BY updated_at DESC"
      : "SELECT uuid, title, description, llm_account, link, severity FROM backlog_items WHERE data_sensitivity = 'public' AND severity != 'BLOCKER' ORDER BY updated_at DESC";

    const {{ results }} = await env.DB.prepare(query).all();

    return new Response(JSON.stringify({{
      viewerRole: isEngineer ? "authenticated_engineer" : "public_visitor",
      count: results.length,
      data: results
    }}), {{
      status: 200,
      headers: {{
        "Content-Type": "application/json",
        "Cache-Control": isEngineer ? "private, no-cache" : "public, max-age=60"
      }}
    }});
  }} catch (err) {{
    return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
  }}
}}
"""

FILES["functions/api/promote.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Promotion & Taxonomy Edge Controller
 */

const DOMAIN_KEYWORDS = {{
  visual_imaging: ["image", "photo", "video", "render", "3d", "canvas", "graphic", "webp", "avif"],
  audio_sound: ["audio", "sound", "music", "speech", "voice", "transcribe", "tts", "stt", "podcast"],
  developer_technical_tools: ["api", "cli", "devops", "cloud", "database", "worker", "runtime", "rust", "git"],
  productivity_organization: ["task", "todo", "note", "calendar", "schedule", "track", "workflow"],
  security_privacy: ["auth", "jwt", "crypto", "security", "token", "mtls", "privacy", "scanner"],
  data_analytics: ["analytics", "metrics", "dashboard", "bi", "telemetry", "visualize", "query"],
  finance_economics: ["billing", "payment", "invoice", "crypto", "tax", "accounting", "ledger"]
}};

function matchTaxonomy(text) {{
  const lower = (text || "").toLowerCase();
  let bestDomain = "developer_technical_tools";
  let maxMatches = 0;
  for (const [domain, keywords] of Object.entries(DOMAIN_KEYWORDS)) {{
    const matches = keywords.filter(kw => lower.includes(kw)).length;
    if (matches > maxMatches) {{
      maxMatches = matches;
      bestDomain = domain;
    }}
  }}
  return bestDomain;
}}

export async function onRequestPost(context) {{
  const {{ request, env, data }} = context;
  if (!data.authenticated) {{
    return new Response(JSON.stringify({{ error: "Unauthorized: Zero Trust Identity Required" }}), {{ status: 401 }});
  }}

  try {{
    const {{ uuid }} = await request.json();
    if (!uuid) return new Response(JSON.stringify({{ error: "Missing required 'uuid'" }}), {{ status: 400 }});

    const item = await env.DB.prepare("SELECT * FROM backlog_items WHERE uuid = ?").bind(uuid).first();
    if (!item) return new Response(JSON.stringify({{ error: "Item not found in D1" }}), {{ status: 404 }});

    if (item.severity === "BLOCKER" || (item.issues && item.issues.toUpperCase().includes("[BLOCKER]"))) {{
      return new Response(JSON.stringify({{ error: "Promotion Gate Locked: Unresolved [BLOCKER] items exist." }}), {{ status: 422 }});
    }}

    const slug = item.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
    const matchedDomain = matchTaxonomy(`${{item.title}} ${{item.description}} ${{item.notes}}`);

    const catalogEntry = {{
      slug: slug,
      name: item.title,
      description: item.description || "Production deployment catalog entry.",
      type: "SPA",
      cfProjectName: slug,
      canonicalOverride: item.link.startsWith("https://") && !item.link.includes(".pages.dev") && !item.link.includes("claude.ai") && !item.link.includes("chatgpt.com") ? item.link : null,
      status: "Production",
      primary_domain: matchedDomain,
      sub_categories: ["web_applications"],
      tags: ["edge", "promoted-prototype"],
      promoted_from_uuid: item.uuid,
      promoted_at: new Date().toISOString()
    }};

    const ghOwner = env.GITHUB_OWNER;
    const ghRepo = env.GITHUB_REPO;
    const ghBranch = env.GITHUB_BRANCH || "main";
    const ghToken = env.GITHUB_TOKEN;
    const filePath = "projects.json";

    const getFileUrl = `https://api.github.com/repos/${{ghOwner}}/${{ghRepo}}/contents/${{filePath}}?ref=${{ghBranch}}`;
    const fileRes = await fetch(getFileUrl, {{
      headers: {{
        "Authorization": `Bearer ${{ghToken}}`,
        "User-Agent": "Catalog-Promotion-Engine",
        "Accept": "application/vnd.github.v3+json"
      }}
    }});
    if (!fileRes.ok) throw new Error(`GitHub Read Error: ${{fileRes.status}}`);

    const fileMeta = await fileRes.json();
    const rawJson = new TextDecoder().decode(
      Uint8Array.from(atob(fileMeta.content.replace(/\\s/g, "")), c => c.charCodeAt(0))
    );
    const catalogArray = JSON.parse(rawJson);

    if (catalogArray.some(p => p.slug === slug)) {{
      return new Response(JSON.stringify({{ error: `Conflict: Slug '${{slug}}' already exists` }}), {{ status: 409 }});
    }}

    catalogArray.push(catalogEntry);
    const updatedRaw = JSON.stringify(catalogArray, null, 2);
    const updatedBase64 = btoa(unescape(encodeURIComponent(updatedRaw)));

    const putRes = await fetch(`https://api.github.com/repos/${{ghOwner}}/${{ghRepo}}/contents/${{filePath}}`, {{
      method: "PUT",
      headers: {{
        "Authorization": `Bearer ${{ghToken}}`,
        "Content-Type": "application/json",
        "User-Agent": "Catalog-Promotion-Engine",
        "Accept": "application/vnd.github.v3+json"
      }},
      body: JSON.stringify({{
        message: `feat(catalog): promote '${{slug}}' [${{item.uuid}}]`,
        content: updatedBase64,
        sha: fileMeta.sha,
        branch: ghBranch
      }})
    }});

    if (!putRes.ok) throw new Error(`GitHub Commit Error: ${{await putRes.text()}}`);
    const commitMeta = await putRes.json();

    await env.DB.prepare("UPDATE backlog_items SET severity = 'CLEAN', updated_at = CURRENT_TIMESTAMP WHERE uuid = ?")
      .bind(uuid)
      .run();

    return new Response(JSON.stringify({{
      success: true,
      slug: slug,
      canonicalUrl: `https://${{slug}}.pages.dev`,
      commitSha: commitMeta.commit.sha,
      matchedDomain: matchedDomain
    }}), {{ status: 200, headers: {{ "Content-Type": "application/json" }} }});
  }} catch (err) {{
    return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
  }}
}}
"""

FILES["functions/api/verify-and-rollback.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Health Verification & Rollback Controller
 */

export async function onRequestPost(context) {{
  const {{ request, env, data }} = context;
  if (!data.authenticated) return new Response(JSON.stringify({{ error: "Unauthorized" }}), {{ status: 401 }});

  const {{ action, slug }} = await request.json();

  if (action === "verify") {{
    if (!slug) return new Response(JSON.stringify({{ error: "Missing slug" }}), {{ status: 400 }});
    try {{
      const probeRes = await fetch(`https://${{slug}}.pages.dev/`, {{
        headers: {{ "User-Agent": "Catalog-Health-Probe" }},
        cf: {{ cacheTtl: 0 }}
      }});
      const isHealthy = probeRes.status === 200;
      return new Response(JSON.stringify({{
        targetUrl: `https://${{slug}}.pages.dev/`,
        status: probeRes.status,
        isHealthy: isHealthy,
        verifiedAt: new Date().toISOString()
      }}), {{ status: isHealthy ? 200 : 502 }});
    }} catch (err) {{
      return new Response(JSON.stringify({{ isHealthy: false, error: err.message }}), {{ status: 502 }});
    }}
  }}

  if (action === "rollback") {{
    if (!slug) return new Response(JSON.stringify({{ error: "Missing slug" }}), {{ status: 400 }});
    try {{
      const ghOwner = env.GITHUB_OWNER;
      const ghRepo = env.GITHUB_REPO;
      const ghBranch = env.GITHUB_BRANCH || "main";
      const ghToken = env.GITHUB_TOKEN;
      const filePath = "projects.json";

      const fileRes = await fetch(`https://api.github.com/repos/${{ghOwner}}/${{ghRepo}}/contents/${{filePath}}?ref=${{ghBranch}}`, {{
        headers: {{ "Authorization": `Bearer ${{ghToken}}`, "User-Agent": "Catalog-Rollback" }}
      }});
      const fileMeta = await fileRes.json();
      const rawJson = new TextDecoder().decode(
        Uint8Array.from(atob(fileMeta.content.replace(/\\s/g, "")), c => c.charCodeAt(0))
      );
      let catalog = JSON.parse(rawJson);
      catalog = catalog.filter(p => p.slug !== slug);

      const putRes = await fetch(`https://api.github.com/repos/${{ghOwner}}/${{ghRepo}}/contents/${{filePath}}`, {{
        method: "PUT",
        headers: {{
          "Authorization": `Bearer ${{ghToken}}`,
          "Content-Type": "application/json",
          "User-Agent": "Catalog-Rollback"
        }},
        body: JSON.stringify({{
          message: `revert: rollback '${{slug}}'`,
          content: btoa(unescape(encodeURIComponent(JSON.stringify(catalog, null, 2)))),
          sha: fileMeta.sha,
          branch: ghBranch
        }})
      }});
      const commitRes = await putRes.json();
      return new Response(JSON.stringify({{ success: true, newCommitSha: commitRes.commit.sha }}), {{ status: 200 }});
    }} catch (err) {{
      return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
    }}
  }}

  return new Response(JSON.stringify({{ error: "Invalid action" }}), {{ status: 400 }});
}}
"""

FILES["functions/api/scaffold-readme.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Automated Starter README.md Generator
 */

export async function onRequestPost(context) {{
  const {{ request, env, data }} = context;
  if (!data.authenticated) return new Response(JSON.stringify({{ error: "Unauthorized" }}), {{ status: 401 }});

  const {{ uuid }} = await request.json();
  const item = await env.DB.prepare("SELECT * FROM backlog_items WHERE uuid = ?").bind(uuid).first();
  if (!item) return new Response(JSON.stringify({{ error: "Item not found" }}), {{ status: 404 }});

  const slug = item.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  const md = `# ${{item.title}}

> ${{item.description || 'Production web application deployed on Cloudflare Pages.'}}

[![Cloudflare Pages](https://img.shields.io/badge/Deployed%20on-Cloudflare%20Pages-F38020?logo=cloudflare)](https://${{slug}}.pages.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview
* **Live Canonical URL:** [https://${{slug}}.pages.dev](https://${{slug}}.pages.dev)
* **LLM Prototyping Platform:** ${{item.llm_account}}
* **Governing Account:** \`${{item.account_id}}\`
* **Promoted Tracking UUID:** \`${{item.uuid}}\`

## Architectural Notes
${{item.notes || '_No architectural notes documented._'}}
`;

  return new Response(JSON.stringify({{ slug: slug, markdown: md }}), {{ status: 200, headers: {{ "Content-Type": "application/json" }} }});
}}
"""

FILES["functions/api/archive.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Archived Prototype Search API
 */

export async function onRequestGet(context) {{
  const {{ request, env, data }} = context;
  const url = new URL(request.url);
  const q = url.searchParams.get("q") || "";
  const filter = q ? "%" + q.toLowerCase() + "%" : "%";

  try {{
    const isEngineer = data.authenticated;
    let sql = isEngineer
      ? "SELECT uuid, account_id, llm_account, title, description, severity, updated_at FROM backlog_items WHERE (LOWER(title) LIKE ? OR LOWER(description) LIKE ?) ORDER BY updated_at DESC LIMIT 100"
      : "SELECT uuid, title, description, llm_account, link, severity FROM backlog_items WHERE data_sensitivity = 'public' AND (LOWER(title) LIKE ? OR LOWER(description) LIKE ?) ORDER BY updated_at DESC LIMIT 50";

    const {{ results }} = await env.DB.prepare(sql).bind(filter, filter).all();
    return new Response(JSON.stringify({{ query: q, totalMatches: results.length, data: results }}), {{
      status: 200,
      headers: {{ "Content-Type": "application/json" }}
    }});
  }} catch (err) {{
    return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
  }}
}}
"""

FILES["functions/api/audit-and-metrics.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Audit Logger & Velocity Analytics Controller
 */

export async function onRequest(context) {{
  const {{ request, env, data }} = context;

  if (request.method === "POST") {{
    if (!data.authenticated) return new Response(JSON.stringify({{ error: "Unauthorized" }}), {{ status: 401 }});
    try {{
      const {{ action, targetUuid, metadata }} = await request.json();
      const event = {{
        eventId: crypto.randomUUID(),
        timestamp: new Date().toISOString(),
        actor: data.userEmail || "service-token@system.local",
        action: action,
        targetUuid: targetUuid,
        clientIp: request.headers.get("CF-Connecting-IP"),
        metadata: metadata || {{}}
      }};
      const dateStr = new Date().toISOString().split("T")[0];
      const logKey = `audit-logs/${{dateStr}}.ndjson`;
      let current = "";
      const obj = await env.AUDIT_BUCKET.get(logKey);
      if (obj) current = await obj.text();
      await env.AUDIT_BUCKET.put(logKey, current + JSON.stringify(event) + "\\n", {{
        httpMetadata: {{ contentType: "application/x-ndjson" }}
      }});
      return new Response(JSON.stringify({{ success: true, eventId: event.eventId }}), {{ status: 201 }});
    }} catch (err) {{
      return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
    }}
  }}

  if (request.method === "GET") {{
    try {{
      const items = await env.DB.prepare("SELECT uuid, account_id, llm_account, created_at, updated_at FROM backlog_items WHERE severity = 'CLEAN'").all();
      let totalDays = 0, count = 0;
      for (const item of items.results) {{
        let cMs = null;
        try {{
          cMs = parseInt(item.uuid.split("-")[0] + item.uuid.split("-")[1], 16);
        }} catch(e) {{
          cMs = new Date(item.created_at).getTime();
        }}
        const uMs = new Date(item.updated_at).getTime();
        totalDays += Math.max(0, (uMs - cMs) / (1000 * 60 * 60 * 24));
        count++;
      }}
      return new Response(JSON.stringify({{
        averageCycleTimeDays: count > 0 ? (totalDays / count).toFixed(2) : 0,
        totalAnalyzed: count
      }}), {{ status: 200, headers: {{ "Content-Type": "application/json" }} }});
    }} catch (err) {{
      return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
    }}
  }}

  return new Response("Method Not Allowed", {{ status: 405 }});
}}
"""

FILES["functions/utils/sanitizer.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Secret Key & PII Redactor
 */

const SECRET_PATTERNS = [
  {{ name: "OPENAI_API_KEY", regex: /sk-[a-zA-Z0-9_-]{{32,}}/g }},
  {{ name: "OPENAI_PROJECT_KEY", regex: /sk-proj-[a-zA-Z0-9_-]{{40,}}/g }},
  {{ name: "ANTHROPIC_API_KEY", regex: /sk-ant-[a-zA-Z0-9_-]{{40,}}/g }},
  {{ name: "GITHUB_PAT", regex: /(ghp_[a-zA-Z0-9]{{36}}|github_pat_[a-zA-Z0-9_]{{60,}})/g }},
  {{ name: "CLOUDFLARE_API_KEY", regex: /[0-9a-f]{{40}}/g }},
  {{ name: "GOOGLE_AI_STUDIO_KEY", regex: /AIzaSy[a-zA-Z0-9_-]{{33}}/g }},
  {{ name: "AWS_ACCESS_KEY_ID", regex: /(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{{16}}/g }},
  {{ name: "JWT_ASSERTION", regex: /eyJ[a-zA-Z0-9_-]{{10,}}\\.eyJ[a-zA-Z0-9_-]{{10,}}\\.[a-zA-Z0-9_-]{{10,}}/g }}
];

const APPROVED_EMAILS = [
  "declanosullivanx1@gmail.com",
  "declanjosephosullivan@gmail.com",
  "cathal.and.declan@gmail.com",
  "declanjosullivan86@gmail.com",
  "declanseer@gmail.com",
  "declanjoseph2025@gmail.com",
  "davewilson1x1@gmail.com",
  "charlie.and.declan.osullivan@gmail.com",
  "declan@transparency-x.com"
];

export function scanAndSanitize(input) {{
  if (!input || typeof input !== "string") return {{ sanitizedText: input || "", violations: [], containsHardBlocker: false }};

  let text = input;
  const violations = [];
  let containsHardBlocker = false;

  for (const pattern of SECRET_PATTERNS) {{
    if (pattern.regex.test(text)) {{
      containsHardBlocker = true;
      violations.push({{ type: "SECRET", pattern: pattern.name }});
      text = text.replace(pattern.regex, `[REDACTED_SECRET_${{pattern.name}}]`);
    }}
    pattern.regex.lastIndex = 0;
  }}

  const emailRegex = /\\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Z|a-z]{{2,7}}\\b/g;
  text = text.replace(emailRegex, (m) => {{
    if (APPROVED_EMAILS.includes(m.toLowerCase())) return m;
    violations.push({{ type: "PII", pattern: "EXTERNAL_EMAIL" }});
    return "[REDACTED_PII_EMAIL]";
  }});

  return {{ sanitizedText: text, violations: violations, containsHardBlocker: containsHardBlocker }};
}}
"""

FILES["functions/cron/maintenance.js"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Scheduled Edge Maintenance: R2 Backup & Link Sweeper
 */

export async function onRequestGet(context) {{
  const {{ env, request }} = context;
  const authHeader = request.headers.get("Authorization");
  if (authHeader !== `Bearer ${{env.CRON_SECRET}}` && env.ENVIRONMENT === "production") {{
    return new Response(JSON.stringify({{ error: "Unauthorized" }}), {{ status: 401 }});
  }}

  try {{
    const allRows = await env.DB.prepare("SELECT * FROM backlog_items ORDER BY created_at ASC").all();
    const backupJson = JSON.stringify({{
      timestamp: new Date().toISOString(),
      count: allRows.results.length,
      records: allRows.results
    }}, null, 2);

    const dateStr = new Date().toISOString().split("T")[0];
    const key = `backups/${{dateStr}}/backlog-${{Date.now()}}.json`;
    await env.BACKUP_BUCKET.put(key, backupJson, {{
      httpMetadata: {{ contentType: "application/json" }}
    }});

    return new Response(JSON.stringify({{ success: true, backupKey: key }}), {{ status: 200 }});
  }} catch (err) {{
    return new Response(JSON.stringify({{ error: err.message }}), {{ status: 500 }});
  }}
}}
"""

# ======================================================================================
# 4. DATABASE & GOOGLE SHEETS ASSETS
# ======================================================================================

FILES["d1/schema.sql"] = lambda u, t: f"""-- UUIDv7: {u}
-- Timestamp: {t}
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
"""

FILES["sheets/Code.gs"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
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

function GENERATE_UUIDV7() {{
  const now = Date.now();
  const timeHex = now.toString(16).padStart(12, '0');
  const randA = Math.floor(Math.random() * 0x0FFF).toString(16).padStart(3, '0');
  const randB1 = (Math.floor(Math.random() * 0x3FFF) | 0x8000).toString(16).padStart(4, '0');
  const randB2 = Math.floor(Math.random() * 0xFFFFFFFFFFFF).toString(16).padStart(12, '0');
  return `${{timeHex.slice(0, 8)}}-${{timeHex.slice(8, 12)}}-7${{randA}}-${{randB1}}-${{randB2}}`;
}}

function onEdit(e) {{
  if (!e || !e.range) return;
  const sheet = e.source.getActiveSheet();
  const row = e.range.getRow();
  const col = e.range.getColumn();
  if (row < 2) return;

  if (col === 5) {{
    const title = e.range.getValue().toString().trim();
    const uuidCell = sheet.getRange(row, 1);
    if (title !== "" && uuidCell.getValue().toString().trim() === "") {{
      uuidCell.setValue(GENERATE_UUIDV7());
    }}
  }}
}}
"""

FILES["sheets/Sprint02_ContextOps.gs"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Context Ops & Triage Engine
 */

function BUILD_CATCHUP_PROMPT(title, description, notes, issues, targetLLM) {{
  if (!title) return "ERROR: Title required.";
  return [
    `# RESUME CODING: ${{title}}`,
    `**Target LLM:** ${{targetLLM || 'Universal'}}`,
    `## Objective\\n${{description || 'None'}}`,
    notes ? `## Architecture\\n${{notes}}` : "",
    issues ? `## Open Bugs to Fix\\n${{issues}}` : "",
    "---",
    "Resolve [BLOCKER] items first. Provide clean diffs."
  ].filter(Boolean).join("\\n");
}}

function PARSE_ISSUE_SEVERITY(issuesText) {{
  if (!issuesText) return "CLEAN";
  const u = issuesText.toUpperCase();
  if (u.includes("[BLOCKER]")) return "BLOCKER";
  if (u.includes("[MAJOR]")) return "MAJOR";
  if (u.includes("[MINOR]")) return "MINOR";
  return "CLEAN";
}}
"""

FILES["sheets/Sprint03_Webhook.gs"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Service Token Authenticated Webhook
 */

function SYNC_ROW_TO_EDGE(rowNumber) {{
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const row = sheet.getRange(rowNumber, 1, 1, 8).getValues()[0];
  const [uuid, accountId, llmAccount, link, title, description, notes, issues] = row;
  if (!uuid || !title || !link) return;

  const props = PropertiesService.getScriptProperties();
  const url = props.getProperty("CF_PAGES_ENDPOINT");
  const id = props.getProperty("CF_ACCESS_CLIENT_ID");
  const secret = props.getProperty("CF_ACCESS_CLIENT_SECRET");

  if (!url || !id || !secret) return;

  UrlFetchApp.fetch(url, {{
    method: "post",
    contentType: "application/json",
    payload: JSON.stringify({{ uuid, accountId, llmAccount, link, title, description, notes, issues }}),
    headers: {{ "CF-Access-Client-Id": id, "CF-Access-Client-Secret": secret }},
    muteHttpExceptions: true
  }});
}}
"""

FILES["sheets/Sprint04_PromotionCallback.gs"] = lambda u, t: f"""/**
 * UUIDv7: {u}
 * Timestamp: {t}
 * Post-Promotion Row Lock
 */

function LOCK_AND_FINALIZE_ROW(uuid, canonicalUrl) {{
  const sheet = SpreadsheetApp.getActiveSpreadsheet().getActiveSheet();
  const data = sheet.getDataRange().getValues();
  for (let i = 1; i < data.length; i++) {{
    if (data[i][0] === uuid) {{
      const r = i + 1;
      const range = sheet.getRange(r, 1, 1, 9);
      range.setBackground("#e6f4ea");
      sheet.getRange(r, 9).setValue(canonicalUrl);
      const prot = range.protect().setDescription(`Locked (${{uuid}})`);
      prot.removeEditors(prot.getEditors());
      break;
    }}
  }}
}}
"""

# ======================================================================================
# SCAFFOLDING EXECUTION ENGINE
# ======================================================================================

def scaffold_project(target_dir: str = "."):
    abs_target = os.path.abspath(target_dir)
    print("=" * 88)
    print(f"[*] Bootstrapping Product Catalog & Backlog Engine")
    print(f"[*] Root Directory: {abs_target}")
    print(f"[*] Timestamp: {get_iso_timestamp()}")
    print("=" * 88)

    os.makedirs(abs_target, exist_ok=True)
    generated_count = 0

    for rel_path, content_factory in FILES.items():
        file_path = os.path.join(abs_target, rel_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        file_uuid = generate_uuidv7()
        file_ts = get_iso_timestamp()

        file_content = content_factory(file_uuid, file_ts)

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(file_content)

        byte_size = len(file_content.encode("utf-8"))
        print(f"  + [{file_uuid}] {rel_path:<40} ({byte_size:,} bytes)")
        generated_count += 1

    print("=" * 88)
    print(f"[SUCCESS] Scaffolding complete. Created {generated_count} files.")
    print("Run `npx wrangler pages dev .` to launch locally.")
    print("=" * 88)

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    scaffold_project(target)
