/**
 * Personal Product Catalog — Hardened Pre-MVP Controller
 * Fully static, zero-build, vanilla JS runtime.
 */

(function () {
  'use strict';

  // --- 1. Safe Theme Management ---
  const themeToggleBtn = document.getElementById('theme-toggle');
  const themeIcon = document.getElementById('theme-icon');
  const themeLabel = document.getElementById('theme-label');

  function getStoredTheme() {
    try {
      return localStorage.getItem('theme') || 'light';
    } catch (e) {
      return 'light'; // Graceful fallback if storage restricted
    }
  }

  function setStoredTheme(theme) {
    try {
      localStorage.setItem('theme', theme);
    } catch (e) {
      // Storage access disabled; fail silently
    }
  }

  function updateThemeUI(theme) {
    const isDark = theme === 'dark';
    if (themeIcon) themeIcon.textContent = isDark ? '☀️' : '🌙';
    if (themeLabel) themeLabel.textContent = isDark ? 'Light Mode' : 'Dark Mode';
    if (themeToggleBtn) {
      themeToggleBtn.setAttribute('aria-pressed', isDark ? 'true' : 'false');
    }
  }

  function initTheme() {
    const activeTheme = getStoredTheme();
    document.documentElement.setAttribute('data-theme', activeTheme);
    updateThemeUI(activeTheme);

    if (themeToggleBtn) {
      themeToggleBtn.addEventListener('click', function () {
        const currentTheme = document.documentElement.getAttribute('data-theme') || 'light';
        const nextTheme = currentTheme === 'light' ? 'dark' : 'light';
        document.documentElement.setAttribute('data-theme', nextTheme);
        setStoredTheme(nextTheme);
        updateThemeUI(nextTheme);
      });
    }
  }

  // --- 2. Security: URL Sanitization & Protocol Whitelisting ---
  function sanitizeUrl(rawUrl) {
    if (!rawUrl || typeof rawUrl !== 'string') return '#';
    const trimmed = rawUrl.trim();

    // Defend against javascript: and data: URI DOM injection
    if (/^(javascript|data|vbscript):/i.test(trimmed)) {
      console.warn('[Security] Blocked unsafe URI scheme:', trimmed);
      return '#';
    }

    // Auto-normalize protocolless URLs to https://
    if (!/^https?:\/\//i.test(trimmed) && !trimmed.startsWith('#')) {
      return 'https://' + trimmed;
    }

    try {
      const parsed = new URL(trimmed);
      if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
        return parsed.href;
      }
    } catch (err) {
      // Not a valid absolute URL
      return '#';
    }

    return '#';
  }

  function resolveCanonicalUrl(entry) {
    if (entry.canonicalOverride && typeof entry.canonicalOverride === 'string') {
      return sanitizeUrl(entry.canonicalOverride);
    }
    if (entry.cfProjectName && typeof entry.cfProjectName === 'string') {
      const cleanName = encodeURIComponent(entry.cfProjectName.trim());
      return 'https://' + cleanName + '.pages.dev';
    }
    return '#';
  }

  // --- 3. DOM Node Generators (Strict Immunity to DOM XSS) ---
  function createSafeLink(text, url) {
    const safeUrl = sanitizeUrl(url);
    const a = document.createElement('a');
    a.href = safeUrl;
    a.target = '_blank';
    a.rel = 'noopener noreferrer';
    a.className = 'canonical-link';
    a.textContent = text || safeUrl;
    return a;
  }

  function createBadge(text, isSpa) {
    const span = document.createElement('span');
    span.className = 'badge' + (isSpa ? ' badge-spa' : '');
    span.textContent = text;
    return span;
  }

  // --- 4. Tabulator Initialization & A11y Polyfill ---
  function initTable(data) {
    const statusEl = document.getElementById('table-status');

    if (typeof Tabulator === 'undefined') {
      if (statusEl) {
        statusEl.innerHTML = '<span style="color: var(--pico-form-element-error-border-color);">' +
          '<strong>Error:</strong> Tabulator library failed to load from CDN. Please check network connectivity.</span>';
      }
      return;
    }

    const processedData = data.map(function (item) {
      return {
        name: typeof item.name === 'string' ? item.name : 'Untitled',
        description: typeof item.description === 'string' ? item.description : '',
        type: typeof item.type === 'string' ? item.type : 'Other',
        canonicalUrl: resolveCanonicalUrl(item),
        status: typeof item.status === 'string' ? item.status : 'Active'
      };
    });

    try {
      const table = new Tabulator('#projects-table', {
        data: processedData,
        layout: 'fitColumns',
        responsiveLayout: 'collapse',
        responsiveLayoutCollapseStartOpen: false,
        headerVisible: true,
        placeholder: 'No matching projects found.',

        // Accessible key/value DL for collapsed rows (DOM-safe)
        responsiveLayoutCollapseFormatter: function (data) {
          const list = document.createElement('dl');
          data.forEach(function (col) {
            if (col.value !== undefined && col.title) {
              const dt = document.createElement('dt');
              dt.textContent = col.title;

              const dd = document.createElement('dd');
              if (col.field === 'canonicalUrl') {
                dd.appendChild(createSafeLink(col.value, col.value));
              } else {
                dd.textContent = col.value;
              }

              list.appendChild(dt);
              list.appendChild(dd);
            }
          });
          return list;
        },

        // WCAG 2.1.1 Accessibility Polyfill: Runs per row rendering
        rowFormatter: function (row) {
          const toggle = row.getElement().querySelector('.tabulator-responsive-collapse-toggle');
          if (toggle && !toggle.dataset.a11yInit) {
            toggle.dataset.a11yInit = 'true';
            toggle.setAttribute('tabindex', '0');
            toggle.setAttribute('role', 'button');
            toggle.setAttribute('aria-expanded', 'false');

            const projectName = row.getData().name || 'project';
            toggle.setAttribute('aria-label', 'Toggle details for ' + projectName);

            // Enable Enter & Spacebar activation on the toggle
            toggle.addEventListener('keydown', function (e) {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggle.click();
              }
            });

            // Synchronize aria-expanded attribute
            toggle.addEventListener('click', function () {
              const isExpanded = toggle.classList.contains('open');
              toggle.setAttribute('aria-expanded', isExpanded ? 'true' : 'false');
            });
          }
        },

        columns: [
          // Responsive collapse handle
          {
            formatter: 'responsiveCollapse',
            width: 36,
            minWidth: 36,
            hozAlign: 'center',
            resizable: false,
            headerSort: false
          },
          // Project Name (Always visible; search searches name, type, and description)
          {
            title: 'Project',
            field: 'name',
            minWidth: 120,
            responsive: 0,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Search...',
            // Universal filter function: Allows filtering collapsed metadata on mobile
            headerFilterFunc: function (headerValue, rowValue, rowData) {
              if (!headerValue) return true;
              const term = headerValue.toLowerCase().trim();
              const nameMatch = (rowData.name || '').toLowerCase().includes(term);
              const descMatch = (rowData.description || '').toLowerCase().includes(term);
              const typeMatch = (rowData.type || '').toLowerCase().includes(term);
              return nameMatch || descMatch || typeMatch;
            },
            formatter: function (cell) {
              const row = cell.getRow().getData();
              const strong = document.createElement('strong');
              strong.appendChild(createSafeLink(cell.getValue(), row.canonicalUrl));
              return strong; // DOM Node prevents XSS
            }
          },
          // Canonical URL (Desktop priority)
          {
            title: 'Canonical URL',
            field: 'canonicalUrl',
            minWidth: 160,
            responsive: 1,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Filter URL...',
            formatter: function (cell) {
              return createSafeLink(cell.getValue(), cell.getValue());
            }
          },
          // Type (Collapses on small screens)
          {
            title: 'Type',
            field: 'type',
            width: 95,
            minWidth: 85,
            responsive: 2,
            hozAlign: 'center',
            headerFilter: 'list',
            headerFilterParams: { valuesLookup: true, clearable: true },
            headerFilterPlaceholder: 'All',
            formatter: function (cell) {
              const val = cell.getValue();
              return createBadge(val, val.toLowerCase() === 'spa');
            }
          },
          // Description (Collapses on mobile)
          {
            title: 'Description',
            field: 'description',
            minWidth: 160,
            responsive: 3,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Filter...'
          },
          // Status (Collapses on mobile)
          {
            title: 'Status',
            field: 'status',
            width: 95,
            minWidth: 85,
            responsive: 4,
            hozAlign: 'center',
            formatter: function (cell) {
              return createBadge(cell.getValue(), false);
            }
          }
        ]
      });

      table.on('tableBuilt', function () {
        if (statusEl) statusEl.remove();
      });

    } catch (err) {
      if (statusEl) {
        statusEl.innerHTML = '<span style="color: var(--pico-form-element-error-border-color);">' +
          'Failed to render catalog table: ' + err.message + '</span>';
      }
    }
  }

  // --- 5. Bootstrapper with Detailed Parsing Diagnostics ---
  function initApp() {
    initTheme();

    const statusEl = document.getElementById('table-status');

    fetch('./projects.json', { cache: 'no-cache' })
      .then(function (res) {
        if (!res.ok) {
          throw new Error('HTTP ' + res.status + ' (' + res.statusText + ')');
        }
        return res.text();
      })
      .then(function (rawText) {
        let projects;
        try {
          projects = JSON.parse(rawText);
        } catch (jsonErr) {
          throw new Error('Invalid JSON in projects.json: ' + jsonErr.message);
        }

        if (!Array.isArray(projects)) {
          throw new Error('Malformed data structure: projects.json root must be an array.');
        }

        initTable(projects);
      })
      .catch(function (error) {
        if (statusEl) {
          statusEl.innerHTML = '<strong>Failed to load catalog:</strong> ' + error.message + 
            '<br><small>If you just edited <code>projects.json</code>, verify syntax (e.g. check for trailing commas).</small>';
        }
      });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();