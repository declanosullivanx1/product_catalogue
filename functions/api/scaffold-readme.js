/**
 * UUIDv7: 01a2133a-ca0b-757b-a263-9964254c677c
 * Timestamp: 2026-11-25T15:02:29Z
 * Automated Starter README.md Generator
 */

export async function onRequestPost(context) {
  const { request, env, data } = context;
  if (!data.authenticated) return new Response(JSON.stringify({ error: "Unauthorized" }), { status: 401 });

  const { uuid } = await request.json();
  const item = await env.DB.prepare("SELECT * FROM backlog_items WHERE uuid = ?").bind(uuid).first();
  if (!item) return new Response(JSON.stringify({ error: "Item not found" }), { status: 404 });

  const slug = item.title.toLowerCase().replace(/[^a-z0-9]+/g, "-").replace(/(^-|-$)/g, "");
  const md = `# ${item.title}

> ${item.description || 'Production web application deployed on Cloudflare Pages.'}

[![Cloudflare Pages](https://img.shields.io/badge/Deployed%20on-Cloudflare%20Pages-F38020?logo=cloudflare)](https://${slug}.pages.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)

## Overview
* **Live Canonical URL:** [https://${slug}.pages.dev](https://${slug}.pages.dev)
* **LLM Prototyping Platform:** ${item.llm_account}
* **Governing Account:** \`${item.account_id}\`
* **Promoted Tracking UUID:** \`${item.uuid}\`

## Architectural Notes
${item.notes || '_No architectural notes documented._'}
`;

  return new Response(JSON.stringify({ slug: slug, markdown: md }), { status: 200, headers: { "Content-Type": "application/json" } });
}
