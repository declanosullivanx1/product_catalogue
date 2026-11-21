# Product Catalog

A static-first, zero-build software and project registry designed for Cloudflare Pages. Built with vanilla JavaScript, Pico.css v2, and Tabulator.js v6.2.

---

## Architecture & Design Principles

* **Zero Build Pipeline**: Plain static HTML, CSS, and JS. Deploys instantly to Cloudflare Pages without bundlers, compilers, or CI install steps.
* **Single Source of Truth**: All project metadata lives in a single human-readable file (`projects.json`).
* **Sub-2-Minute Upkeep**: Adding or updating a project requires editing only `projects.json` and pushing to `main`.
* **Light-First Theming**: Forces a high-contrast light theme on initial visit regardless of OS `prefers-color-scheme`, with dark mode toggled and persisted via `localStorage`.
* **Mobile-First Layout**: Fully functional at 360px viewport widths with responsive column collapsing and keyboard-navigable controls.
* **Canonical URL Prioritization**: Links resolve directly to production aliases (`https://<project>.pages.dev`), with protocol-sanitized overrides for external entries.

---

## Tech Stack

| Component | Technology | Source | Delivery |
| :--- | :--- | :--- | :--- |
| **Hosting** | Cloudflare Pages | Edge Network | Static file serving |
| **CSS Framework** | Pico.css v2 | jsDelivr CDN | Semantic classless foundation |
| **Data Grid** | Tabulator.js v6.2.5 | Unpkg CDN | Built-in sort, filter, and responsive collapse |
| **Runtime** | Vanilla ECMAScript (ES6+) | Native | Browser-native execution |
| **Data Layer** | JSON | Local File | `fetch('./projects.json')` |

---

## Directory Structure

```text
.
├── index.html          # Pre-MVP single-page catalog interface
├── projects.json       # Canonical data store for all projects
├── css/
│   └── custom.css      # Pico/Tabulator variable mapping & mobile rules
├── js/
│   └── app.js          # Controller: sanitization, theming, and table init
└── functions/          # (MVP) Cloudflare Pages Functions
    └── api/
        └── versions.js # (MVP) Cloudflare Deployments API proxy
```

---

## Data Schema & Specifications

All catalog items must adhere to the schema in `projects.json`.

### Schema Example

```json
[
  {
    "name": "Aura Scaler",
    "description": "Dynamic image transformation pipeline running on Cloudflare Workers.",
    "type": "SPA",
    "cfProjectName": "aura-scaler-python",
    "canonicalOverride": null,
    "status": "Production"
  },
  {
    "name": "k8s-pod-reaper",
    "description": "Lightweight Rust CLI daemon that terminates orphaned development pods.",
    "type": "CLI",
    "cfProjectName": null,
    "canonicalOverride": "https://github.com/example/k8s-pod-reaper",
    "status": "Active"
  }
]
```

### Field Definitions

* **`name`** *(string, required)*: Display title of the project or product.
* **`description`** *(string, required)*: One-line functional summary.
* **`type`** *(string, required)*: Classification category. Recommended values: `"SPA"`, `"CLI"`, `"Library"`, `"API"`, `"Other"`.
* **`cfProjectName`** *(string | null)*: Cloudflare Pages project slug. Automatically resolves to `https://<cfProjectName>.pages.dev`.
* **`canonicalOverride`** *(string | null)*: Explicit external URL. Overrides `cfProjectName` if provided. Protocols (`http://`, `https://`) are normalized automatically.
* **`status`** *(string, optional)*: Lifecycle flag (`"Production"`, `"Beta"`, `"Active"`, `"Archived"`). Defaults to `"Active"`.

### Canonical Resolution Hierarchy

1. If `canonicalOverride` is present: Validates protocol and returns sanitized absolute URL.
2. If `cfProjectName` is present: Returns `https://<cfProjectName>.pages.dev`.
3. If neither is present: Falls back safely to `'#'`.

---

## Security & Accessibility Audit Hardening

* **DOM XSS Immunity**: Formatters inject native DOM nodes via `document.createElement()` and `.textContent`. Unescaped HTML string interpolation is strictly prohibited.
* **Protocol Whitelisting**: The URL sanitizer strips `javascript:`, `data:`, and `vbscript:` schemes to eliminate script execution vectors.
* **WCAG 2.1.1 Keyboard Compliance**: Tabulator's `.tabulator-responsive-collapse-toggle` element is programmatically polyfilled with `tabindex="0"`, `role="button"`, `aria-label`, and `Enter`/`Space` activation listeners.
* **Storage Isolation**: Storage calls are wrapped in `try/catch` blocks to prevent uncaught `SecurityError` exceptions in Safari Private Browsing mode.
* **iOS Safari Zoom Prevention**: Header filter inputs enforce a minimum `16px` font size to bypass iOS auto-zoom behavior on input focus.
* **Mobile Multi-Field Search**: The Project Name filter uses an overarching matcher (`headerFilterFunc`) that searches Name, Description, and Type simultaneously, preserving mobile searchability when columns collapse.

---

## Local Development & Verification

Because there is no build step, you can serve the directory with any standard static file server:

```bash
# Option 1: Python 3
python3 -m http.server 8080

# Option 2: Node.js (npx)
npx serve .

# Option 3: Cloudflare Wrangler (Pages emulation)
npx wrangler pages dev .
```

### Verification Checklist Before Pushing

* [ ] **JSON Syntax**: Validate `projects.json` has no trailing commas or missing quotes (`jq . projects.json`).
* [ ] **First-Visit Theme**: Verify in an incognito/private window that the site boots into `light` mode regardless of OS theme.
* [ ] **Mobile Viewport (360px)**: In DevTools, set width to `360px`. Confirm no horizontal page scroll exists and that row expanders operate smoothly.
* [ ] **Keyboard Navigation**: Press `Tab` through the table to verify focus indicators and test expanding collapsed rows via `Space` or `Enter`.

---

## Cloudflare Pages Deployment

### Initial Setup

1. Push this repository to GitHub or GitLab.
2. Navigate to **Cloudflare Dashboard > Workers & Pages > Create Application > Pages > Connect to Git**.
3. Configure build settings:
   * **Framework preset**: None
   * **Build command**: *(leave blank)*
   * **Build output directory**: `.` (root)
4. Click **Save and Deploy**.

### Standard Update Workflow

```bash
# 1. Edit projects.json
$EDITOR projects.json

# 2. Commit and push changes
git commit -am "chore: add new project"
git push origin main
```

*Changes deploy automatically to the Cloudflare edge in under 60 seconds.*

---

## Roadmap

* [x] **Pre-MVP**: Single-page responsive project table with built-in search, sorting, light/dark theming, and canonical URL resolution.
* [ ] **MVP**: Dynamic detail page (`project.html?p=:slug`) consuming Cloudflare Deployments API via Pages Functions to list immutable production deployment hashes (`https://<hash>.<project>.pages.dev`).
