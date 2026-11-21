/**
 * Project Detail View Controller
 * Hydrates project.html using ?p=<slug> parameter.
 */

(function () {
  'use strict';

  const params = new URLSearchParams(window.location.search);
  const slug = params.get('p');
  const statusEl = document.getElementById('detail-status');
  const articleEl = document.getElementById('project-detail');

  if (!slug) {
    statusEl.innerHTML = '<strong>No project specified.</strong> <a href="/">Return to Catalog</a>';
    return;
  }

  Promise.all([
    fetch('./projects.json').then(function (r) { return r.json(); }),
    fetch('./taxonomy.json').then(function (r) { return r.json(); })
  ])
  .then(function (results) {
    const projects = results[0];
    const taxonomy = results[1];

    const project = projects.find(function (p) { return p.slug === slug; });
    if (!project) {
      statusEl.innerHTML = '<strong>Project not found.</strong> <a href="/">Return to Catalog</a>';
      return;
    }

    // Hydrate Header
    document.getElementById('proj-name').textContent = project.name;
    document.getElementById('proj-desc').textContent = project.description;
    document.title = project.name + ' — Details';

    const canonicalUrl = project.canonicalOverride || (project.cfProjectName ? 'https://' + project.cfProjectName + '.pages.dev' : '#');
    const canonicalBtn = document.getElementById('proj-canonical');
    canonicalBtn.href = canonicalUrl;
    if (canonicalUrl === '#') canonicalBtn.style.display = 'none';

    // Hydrate Domain Banner
    const domain = (taxonomy.domains || []).find(function (d) { return d.id === project.primary_domain; });
    if (domain) {
      document.getElementById('domain-icon').textContent = domain.icon || '📁';
      document.getElementById('domain-label').textContent = domain.label;
      document.getElementById('domain-desc').textContent = domain.description || '';
    }

    // Helper: Render Chip Lists
    function renderChips(containerId, items, prefix) {
      const container = document.getElementById(containerId);
      container.innerHTML = '';
      if (!items || items.length === 0) {
        container.innerHTML = '<small style="color:var(--pico-muted-color);">None</small>';
        return;
      }
      const arr = Array.isArray(items) ? items : [items];
      arr.forEach(function (val) {
        const span = document.createElement('span');
        span.className = 'taxonomy-tag';
        span.textContent = (prefix || '') + val;
        container.appendChild(span);
      });
    }

    renderChips('sub-cat-list', project.sub_categories);
    renderChips('tag-list', project.tags, '#');
    renderChips('facet-platform', project.platform);
    renderChips('facet-delivery', project.delivery_model);
    renderChips('facet-monetization', project.monetization);
    renderChips('facet-ai', project.ai_integration);

    // Hydrate Version History
    const versionList = document.getElementById('version-list');
    versionList.innerHTML = '';

    if (project.cfProjectName && project.versions && project.versions.length > 0) {
      project.versions.forEach(function (v) {
        const li = document.createElement('li');
        li.className = 'version-item';

        const left = document.createElement('div');
        const link = document.createElement('a');
        link.href = 'https://' + v.hash + '.' + project.cfProjectName + '.pages.dev';
        link.target = '_blank';
        link.rel = 'noopener noreferrer';
        link.textContent = v.hash + '.' + project.cfProjectName + '.pages.dev';
        left.appendChild(link);

        if (v.label) {
          const badge = document.createElement('span');
          badge.className = 'badge';
          badge.style.marginLeft = '0.5rem';
          badge.textContent = v.label;
          left.appendChild(badge);
        }

        const date = document.createElement('small');
        date.style.color = 'var(--pico-muted-color)';
        date.textContent = v.date || '';

        li.appendChild(left);
        li.appendChild(date);
        versionList.appendChild(li);
      });
    } else if (project.cfProjectName) {
      versionList.innerHTML = '<li><small style="color:var(--pico-muted-color);">No version history available for this Cloudflare Pages project.</small></li>';
    } else {
      versionList.innerHTML = '<li><small style="color:var(--pico-muted-color);">No deployment version history available for external / non-Pages projects.</small></li>';
    }

    // Reveal UI
    statusEl.style.display = 'none';
    articleEl.style.display = 'block';
  })
  .catch(function (err) {
    statusEl.innerHTML = '<strong>Error loading project:</strong> ' + err.message;
  });
})();