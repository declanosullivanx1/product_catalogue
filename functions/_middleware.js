/**
 * UUIDv7: 01a2133a-ca02-7ae1-9a63-5fc34bb7af66
 * Timestamp: 2026-11-25T15:02:29Z
 * Cloudflare Pages Edge Zero Trust Middleware
 */

let CACHED_JWKS = null;
let JWKS_EXPIRY = 0;

async function getAccessJwks(teamDomain) {
  const now = Date.now();
  if (CACHED_JWKS && now < JWKS_EXPIRY) return CACHED_JWKS;
  const res = await fetch(`https://${teamDomain}/cdn-cgi/access/certs`, {
    cf: { cacheTtl: 3600, cacheEverything: true }
  });
  if (!res.ok) throw new Error(`Failed to fetch JWKS: ${res.status}`);
  const data = await res.json();
  CACHED_JWKS = data.keys;
  JWKS_EXPIRY = now + 3600 * 1000;
  return CACHED_JWKS;
}

export async function onRequest(context) {
  const { request, env, next } = context;
  const url = new URL(request.url);

  context.data.authenticated = false;
  context.data.authType = "anonymous";
  context.data.userEmail = null;
  context.data.groups = [];

  if (url.pathname.startsWith("/css/") || url.pathname.startsWith("/js/") || url.pathname === "/favicon.ico") {
    return next();
  }

  // 1. Service Token Authentication
  const clientId = request.headers.get("CF-Access-Client-Id");
  const clientSecret = request.headers.get("CF-Access-Client-Secret");
  if (clientId && clientSecret) {
    if (clientId === env.CF_SERVICE_TOKEN_CLIENT_ID && clientSecret === env.CF_SERVICE_TOKEN_CLIENT_SECRET) {
      context.data.authenticated = true;
      context.data.authType = "service_token";
      context.data.userEmail = "service-token@system.local";
      context.data.groups = ["system", "automation"];
      return next();
    } else {
      return new Response(JSON.stringify({ error: "Invalid Service Token Credentials" }), {
        status: 403,
        headers: { "Content-Type": "application/json" }
      });
    }
  }

  // 2. User JWT Verification
  const jwt = request.headers.get("Cf-Access-Jwt-Assertion");
  if (jwt && env.CF_ACCESS_TEAM_DOMAIN && env.CF_ACCESS_AUD) {
    try {
      const parts = jwt.split(".");
      if (parts.length === 3) {
        const header = JSON.parse(atob(parts[0].replace(/-/g, "+").replace(/_/g, "/")));
        const payload = JSON.parse(atob(parts[1].replace(/-/g, "+").replace(/_/g, "/")));
        const nowSec = Math.floor(Date.now() / 1000);
        if (payload.exp > nowSec && payload.aud.includes(env.CF_ACCESS_AUD)) {
          const keys = await getAccessJwks(env.CF_ACCESS_TEAM_DOMAIN);
          const jwk = keys.find(k => k.kid === header.kid);
          if (jwk) {
            const key = await crypto.subtle.importKey(
              "jwk", jwk, { name: "RSASSA-PKCS1-v1_5", hash: "SHA-256" }, false, ["verify"]
            );
            const enc = new TextEncoder();
            const signedData = enc.encode(`${parts[0]}.${parts[1]}`);
            const signature = Uint8Array.from(atob(parts[2].replace(/-/g, "+").replace(/_/g, "/")), c => c.charCodeAt(0));
            const valid = await crypto.subtle.verify("RSASSA-PKCS1-v1_5", key, signature, signedData);
            if (valid) {
              context.data.authenticated = true;
              context.data.authType = "user_jwt";
              context.data.userEmail = payload.email || "unknown@user";
              context.data.groups = payload.custom_groups || [];
            }
          }
        }
      }
    } catch (err) {}
  }

  if (url.pathname.startsWith("/api/sync")) {
    if (!context.data.authenticated) {
      return new Response(JSON.stringify({ error: "Unauthorized Zero Trust Perimeter" }), {
        status: 401,
        headers: { "Content-Type": "application/json" }
      });
    }
  }

  const response = await next();
  response.headers.set("X-Content-Type-Options", "nosniff");
  response.headers.set("X-Frame-Options", "DENY");
  response.headers.set("Referrer-Policy", "strict-origin-when-cross-origin");
  return response;
}
