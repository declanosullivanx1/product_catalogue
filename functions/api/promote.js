/**
 * UUIDv7: 01a2133a-ca07-72f3-9a79-390eac080a13
 * Timestamp: 2026-11-25T15:02:29Z
 * Promotion & Taxonomy Edge Controller
 */

const DOMAIN_KEYWORDS = {
  visual_imaging: ["image", "photo", "video", "render", "3d", "canvas", "graphic", "webp", "avif"],
  audio_sound: ["audio", "sound", "music", "speech", "voice", "transcribe", "tts", "stt", "podcast"],
  developer_technical_tools: ["api", "cli", "devops", "cloud", "database", "worker", "runtime", "rust", "git"],
  productivity_organization: ["task", "todo", "note", "calendar", "schedule", "track", "workflow"],
  security_privacy: ["auth", "jwt", "crypto", "security", "token", "mtls", "privacy", "scanner"],
  data_analytics: ["analytics", "metrics", "dashboard", "bi", "telemetry", "visualize", "query"],
  finance_economics: ["billing", "payment", "invoice", "crypto", "tax", "accounting", "ledger"]
};

function matchTaxonomy(text) {
  const lower = (text || "").toLowerCase();
  let bestDomain = "developer_technical_tools";
  let maxMatches = 0;
  for (const [domain, keywords] of Object.entries(DOMAIN_KEYWORDS)) {
    const matches = keywords.filter(kw => lower.includes(kw)).length;
    if (matches > maxMatches) {
      maxMatches = matches;
      bestDomain = domain;
    }
  }
  return bestDomain;
}

export async function onRequestPost(context) {
  const { request, env, data } = context;
  if (!data.authenticated) {
    return new Response(JSON.stringify({ error: "Unauthorized: Zero Trust Identity Required" }), { status: 401 });
  }

  try {
    const { uuid } = await request.json();
    if (!uuid) return new Response(JSON.stringify({ error: "Missing required 'uuid'" }), { status: 400 });

    const item = await env.DB.prepare("SELECT * FROM backlog_items WHERE uuid = ?").bind(uuid).first();
    if (!item) return new Response(JSON.stringify({ error: "Item not found in D1" }), { status: 404 });

    if (item.severity === "BLOCKER" || (item.issues && item.issues.toUpperCase().includes("[BLOCKER]"))) {
      return new Response(JSON.stringify({ error: "Promotion Gate Locked: Unresolved [BLOCKER] items exist." }), { status: 422 });
    }

    const slug = item.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
    const matchedDomain = matchTaxonomy(`${item.title} ${item.description} ${item.notes}`);

    const catalogEntry = {
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
    };

    const ghOwner = env.GITHUB_OWNER;
    const ghRepo = env.GITHUB_REPO;
    const ghBranch = env.GITHUB_BRANCH || "main";
    const ghToken = env.GITHUB_TOKEN;
    const filePath = "projects.json";

    const getFileUrl = `https://api.github.com/repos/${ghOwner}/${ghRepo}/contents/${filePath}?ref=${ghBranch}`;
    const fileRes = await fetch(getFileUrl, {
      headers: {
        "Authorization": `Bearer ${ghToken}`,
        "User-Agent": "Catalog-Promotion-Engine",
        "Accept": "application/vnd.github.v3+json"
      }
    });
    if (!fileRes.ok) throw new Error(`GitHub Read Error: ${fileRes.status}`);

    const fileMeta = await fileRes.json();
    const rawJson = new TextDecoder().decode(
      Uint8Array.from(atob(fileMeta.content.replace(/\s/g, "")), c => c.charCodeAt(0))
    );
    const catalogArray = JSON.parse(rawJson);

    if (catalogArray.some(p => p.slug === slug)) {
      return new Response(JSON.stringify({ error: `Conflict: Slug '${slug}' already exists` }), { status: 409 });
    }

    catalogArray.push(catalogEntry);
    const updatedRaw = JSON.stringify(catalogArray, null, 2);
    const updatedBase64 = btoa(unescape(encodeURIComponent(updatedRaw)));

    const putRes = await fetch(`https://api.github.com/repos/${ghOwner}/${ghRepo}/contents/${filePath}`, {
      method: "PUT",
      headers: {
        "Authorization": `Bearer ${ghToken}`,
        "Content-Type": "application/json",
        "User-Agent": "Catalog-Promotion-Engine",
        "Accept": "application/vnd.github.v3+json"
      },
      body: JSON.stringify({
        message: `feat(catalog): promote '${slug}' [${item.uuid}]`,
        content: updatedBase64,
        sha: fileMeta.sha,
        branch: ghBranch
      })
    });

    if (!putRes.ok) throw new Error(`GitHub Commit Error: ${await putRes.text()}`);
    const commitMeta = await putRes.json();

    await env.DB.prepare("UPDATE backlog_items SET severity = 'CLEAN', updated_at = CURRENT_TIMESTAMP WHERE uuid = ?")
      .bind(uuid)
      .run();

    return new Response(JSON.stringify({
      success: true,
      slug: slug,
      canonicalUrl: `https://${slug}.pages.dev`,
      commitSha: commitMeta.commit.sha,
      matchedDomain: matchedDomain
    }), { status: 200, headers: { "Content-Type": "application/json" } });
  } catch (err) {
    return new Response(JSON.stringify({ error: err.message }), { status: 500 });
  }
}
