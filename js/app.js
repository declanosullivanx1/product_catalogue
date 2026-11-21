/**
 * Personal Product Catalog — Controller
 * Loads projects.json + taxonomy.json concurrently with zero build steps.
 */

(function () {
  'use strict';

  function sanitizeUrl(rawUrl) {
    if (!rawUrl || typeof rawUrl !== 'string') return '#';
    const trimmed = rawUrl.trim();
    if (/^(javascript|data|vbscript):/i.test(trimmed)) return '#';
    if (!/^https?:\/\//i.test(trimmed) && !trimmed.startsWith('#')) {
      return 'https://' + trimmed;
    }
    try {
      const parsed = new URL(trimmed);
      if (parsed.protocol === 'http:' || parsed.protocol === 'https:') {
        return parsed.href;
      }
    } catch (err) {}
    return '#';
  }

  function resolveCanonicalUrl(entry) {
    if (entry.canonicalOverride) return sanitizeUrl(entry.canonicalOverride);
    if (entry.cfProjectName) return 'https://' + encodeURIComponent(entry.cfProjectName.trim()) + '.pages.dev';
    return '#';
  }

  function createSafeLink(text, url, className) {
    const a = document.createElement('a');
    a.href = sanitizeUrl(url);
    a.className = className || 'canonical-link';
    a.textContent = text || url;
    if (!url.startsWith('#') && !url.startsWith('/')) {
      a.target = '_blank';
      a.rel = 'noopener noreferrer';
    }
    return a;
  }

  function initTable(projects, taxonomy) {
    const statusEl = document.getElementById('table-status');

    // Build Domain Lookup Map
    const domainMap = new Map();
    (taxonomy.domains || []).forEach(function (d) {
      domainMap.set(d.id, { label: d.label, icon: d.icon || '📁' });
    });

    // Populate data with resolved domain text
    const processedData = projects.map(function (item) {
      const dom = domainMap.get(item.primary_domain) || { label: 'General', icon: '📦' };
      return {
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
      };
    });

    try {
      const table = new Tabulator('#projects-table', {
        data: processedData,
        layout: 'fitColumns',
        responsiveLayout: 'collapse',
        responsiveLayoutCollapseStartOpen: false,
        placeholder: 'No matching projects found.',

        // Responsive Collapse: Shows full taxonomy metadata
        responsiveLayoutCollapseFormatter: function (data) {
          const dl = document.createElement('dl');
          const rowData = data[0] ? data[0].getRow().getData() : null;

          data.forEach(function (col) {
            if (col.value !== undefined && col.title && col.field !== 'domainDisplay') {
              const dt = document.createElement('dt');
              dt.textContent = col.title;
              const dd = document.createElement('dd');

              if (col.field === 'canonicalUrl') {
                dd.appendChild(createSafeLink(col.value, col.value));
              } else {
                dd.textContent = col.value;
              }
              dl.appendChild(dt);
              dl.appendChild(dd);
            }
          });

          // Render Tags & Subcategories inside accordion
          if (rowData && rowData.tags && rowData.tags.length > 0) {
            const dtTags = document.createElement('dt');
            dtTags.textContent = 'Tags';
            const ddTags = document.createElement('dd');
            const ul = document.createElement('ul');
            ul.className = 'tag-list';
            rowData.tags.forEach(function (t) {
              const li = document.createElement('li');
              li.className = 'taxonomy-tag';
              li.textContent = '#' + t;
              ul.appendChild(li);
            });
            ddTags.appendChild(ul);
            dl.appendChild(dtTags);
            dl.appendChild(ddTags);
          }

          return dl;
        },

        // Keyboard Operability Polyfill
        rowFormatter: function (row) {
          const toggle = row.getElement().querySelector('.tabulator-responsive-collapse-toggle');
          if (toggle && !toggle.dataset.a11yInit) {
            toggle.dataset.a11yInit = 'true';
            toggle.setAttribute('tabindex', '0');
            toggle.setAttribute('role', 'button');
            toggle.setAttribute('aria-expanded', 'false');
            toggle.setAttribute('aria-label', 'Toggle details');

            toggle.addEventListener('keydown', function (e) {
              if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                toggle.click();
              }
            });

            toggle.addEventListener('click', function () {
              const isOpen = toggle.classList.contains('open');
              toggle.setAttribute('aria-expanded', isOpen ? 'true' : 'false');
            });
          }
        },

        columns: [
          {
            formatter: 'responsiveCollapse',
            width: 36,
            minWidth: 36,
            hozAlign: 'center',
            resizable: false,
            headerSort: false
          },
          // Project Column: Links to project.html detail page
          {
            title: 'Project',
            field: 'name',
            minWidth: 140,
            responsive: 0,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Search...',
            // Universal Search across Name, Description, Domain, and Tags
            headerFilterFunc: function (headerValue, rowValue, rowData) {
              if (!headerValue) return true;
              const q = headerValue.toLowerCase().trim();
              const nameMatch = (rowData.name || '').toLowerCase().includes(q);
              const descMatch = (rowData.description || '').toLowerCase().includes(q);
              const domainMatch = (rowData.domainLabel || '').toLowerCase().includes(q);
              const tagMatch = (rowData.tags || []).some(function (t) { return t.toLowerCase().includes(q); });
              return nameMatch || descMatch || domainMatch || tagMatch;
            },
            formatter: function (cell) {
              const row = cell.getRow().getData();
              const container = document.createElement('div');
              const link = document.createElement('a');
              link.href = 'project.html?p=' + encodeURIComponent(row.slug);
              link.className = 'project-title-link';
              link.textContent = cell.getValue();
              container.appendChild(link);
              return container;
            }
          },
          // Domain Column: Displays icon + label with built-in dropdown filter
          {
            title: 'Primary Domain',
            field: 'domainDisplay',
            minWidth: 160,
            responsive: 1,
            headerFilter: 'list',
            headerFilterParams: { valuesLookup: true, clearable: true },
            headerFilterPlaceholder: 'All Domains',
            formatter: function (cell) {
              const span = document.createElement('span');
              span.className = 'badge badge-domain';
              span.textContent = cell.getValue();
              return span;
            }
          },
          // Canonical URL
          {
            title: 'Canonical URL',
            field: 'canonicalUrl',
            minWidth: 160,
            responsive: 2,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Filter URL...',
            formatter: function (cell) {
              return createSafeLink(cell.getValue(), cell.getValue());
            }
          },
          // Type Column
          {
            title: 'Type',
            field: 'type',
            width: 90,
            responsive: 3,
            hozAlign: 'center',
            headerFilter: 'list',
            headerFilterParams: { valuesLookup: true, clearable: true },
            headerFilterPlaceholder: 'All',
            formatter: function (cell) {
              const span = document.createElement('span');
              span.className = 'badge';
              span.textContent = cell.getValue();
              return span;
            }
          },
          // Description
          {
            title: 'Description',
            field: 'description',
            minWidth: 180,
            responsive: 4,
            headerFilter: 'input',
            headerFilterPlaceholder: 'Filter text...'
          },
          // Status
          {
            title: 'Status',
            field: 'status',
            width: 95,
            responsive: 5,
            hozAlign: 'center',
            formatter: function (cell) {
              const span = document.createElement('span');
              span.className = 'badge';
              span.textContent = cell.getValue();
              return span;
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

  function initApp() {
    const statusEl = document.getElementById('table-status');

    Promise.all([
      fetch('./projects.json', { cache: 'no-cache' }).then(function (r) { return r.json(); }),
      fetch('./taxonomy.json', { cache: 'no-cache' }).then(function (r) { return r.json(); })
    ])
    .then(function (results) {
      const projects = results[0];
      const taxonomy = results[1];
      initTable(projects, taxonomy);
    })
    .catch(function (err) {
      if (statusEl) {
        statusEl.innerHTML = '<strong>Error loading catalog data:</strong> ' + err.message;
      }
    });
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initApp);
  } else {
    initApp();
  }
})();