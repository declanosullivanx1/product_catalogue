/**
 * UUIDv7: 01a2133a-ca00-7329-bab0-c45d95de6e76
 * Timestamp: 2026-11-25T15:02:29Z
 * Triage & Pre-flight Client Module
 */

(function () {
  'use strict';

  window.extractArtifacts = function (rawText) {
    if (!rawText || typeof rawText !== 'string') return "";
    let extracted = [];

    const claudeRegex = /<antArtifact\s+[^>]*?language="([^"]*)"[^>]*?>([\s\S]*?)<\/antArtifact>/gi;
    let match;
    while ((match = claudeRegex.exec(rawText)) !== null) {
      const lang = match[1] || 'plaintext';
      const code = match[2].trim();
      extracted.push(`### [Extracted Artifact: ${lang}]\n\\`\\`\\`${lang}\n${code}\n\\`\\`\\``);
    }

    if (extracted.length === 0) {
      const fenceRegex = /\\`\\`\\`([a-zA-Z0-9_-]*)\n([\s\S]*?)\\`\\`\\`/g;
      while ((match = fenceRegex.exec(rawText)) !== null) {
        const lang = match[1] || 'code';
        const code = match[2].trim();
        extracted.push(`\\`\\`\\`${lang}\n${code}\n\\`\\`\\``);
      }
    }
    return extracted.join("\n\n");
  };

  let debounceTimer = null;
  window.probePagesSubdomain = function (slug, callback) {
    clearTimeout(debounceTimer);
    if (!slug) {
      callback('EMPTY');
      return;
    }
    const clean = slug.toLowerCase().replace(/[^a-z0-9-]/g, '').trim();
    if (!clean) {
      callback('INVALID');
      return;
    }
    debounceTimer = setTimeout(() => {
      fetch(`https://cloudflare-dns.com/dns-query?name=${clean}.pages.dev&type=CNAME`, {
        headers: { "Accept": "application/dns-json" }
      })
      .then(res => res.json())
      .then(data => {
        if (data.Status === 3) {
          callback('AVAILABLE', clean);
        } else if (data.Status === 0 && data.Answer) {
          callback('TAKEN', clean);
        } else {
          callback('UNKNOWN', clean);
        }
      })
      .catch(() => callback('ERROR', clean));
    }, 400);
  };

  window.generateCatchUpPrompt = function (title, desc, notes, issues, llm) {
    return [
      `# RESUME CODING SESSION: ${title || 'Untitled Project'}`,
      `**Platform:** ${llm || 'Universal LLM'} | **Date:** ${new Date().toISOString().split('T')[0]}`,
      `\n## Target Objective\n${desc || 'No summary documented.'}`,
      notes ? `\n## Verified Architecture & Implementation\n${notes}` : null,
      issues ? `\n## Blockers & Defects to Solve Now\n${issues}` : null,
      "\n---",
      "Please review the state above. Address all [BLOCKER] items first. Provide the complete code fix."
    ].filter(Boolean).join("\n");
  };
})();
