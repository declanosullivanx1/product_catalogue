/**
 * UUIDv7: 01a2133a-ca09-7442-836d-609ac220548e
 * Timestamp: 2026-11-25T15:02:29Z
 * Health Verification & Rollback Controller
 */

export async function onRequestPost(context) {
  const { request, env, data } = context;
  if (!data.authenticated) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });

  const { action, slug } = await request.json();

  if (action === "verify") {
    if (!slug) return new Response(JSON.stringify({ error: "Missing slug" }), { status: 400 });
    try {
      const probeRes = await fetch(`https://${slug}.pages.dev/`, {
        headers: { "User-Agent": "Catalog-Health-Probe" },
        cf: { cacheTtl: 0 }
      });
      const isHealthy = probeRes.status === 200;
      return new Response(JSON.stringify({
        targetUrl: `https://${slug}.pages.dev/`,
        status: probeRes.status,
        isHealthy: isHealthy,
        verifiedAt: new Date().toISOString()
      }), { status: isHealthy ? 200 : 502 });
    } catch (err) {
      return new Response(JSON.stringify({ isHealthy: false, error: err.message }), { status: 502 });
    }
  }

  if (action === "rollback") {
    if (!slug) return new Response(JSON.stringify({ error: "Missing slug" }), { status: 400 });
    try {
      const ghOwner = env.GITHUB_OWNER;
      const ghRepo = env.GITHUB_REPO;
      const ghBranch = env.GITHUB_BRANCH || "main";
      const ghToken = env.GITHUB_TOKEN;
      const filePath = "projects.json";

      const fileRes = await fetch(`https://api.github.com/repos/${ghOwner}/${ghRepo}/contents/${filePath}?ref=${ghBranch}`, {
        headers: { "Authorization": `Bearer ${ghToken}`, "User-Agent": "Catalog-Rollback" }
      });
      const fileMeta = await fileRes.json();
      const rawJson = new TextDecoder().decode(
        Uint8Array.from(atob(fileMeta.content.replace(/\s/g, "")), c => c.charCodeAt(0))
      );
      let catalog = JSON.parse(rawJson);
      catalog = catalog.filter(p => p.slug !== slug);

      const putRes = await fetch(`https://api.github.com/repos/${ghOwner}/${ghRepo}/contents/${filePath}`, {
        method: "PUT",
        headers: {
          "Authorization": `Bearer ${ghToken}`,
          "Content-Type": "application/json",
          "User-Agent": "Catalog-Rollback"
        },
        body: JSON.stringify({
          message: `revert: rollback '${slug}'`,
          content: btoa(unescape(encodeURIComponent(JSON.stringify(catalog, null, 2)))),
          sha: fileMeta.sha,
          branch: ghBranch
        })
      });
      const commitRes = await putRes.json();
      return new Response(JSON.stringify({ success: true, newCommitSha: commitRes.commit.sha }), { status: 200 });
    } catch (err) {
      return new Response(JSON.stringify({ error: err.message }), { status: 500 });
    }
  }

  return new Response(JSON.stringify({ error: "Invalid action" }), { status: 400 });
}
