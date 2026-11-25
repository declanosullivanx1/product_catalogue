/**
 * UUIDv7: 01a2133a-ca18-714d-b288-dcb65d1fd695
 * Timestamp: 2026-11-25T15:02:29Z
 * Context Ops & Triage Engine
 */

function BUILD_CATCHUP_PROMPT(title, description, notes, issues, targetLLM) {
  if (!title) return "ERROR: Title required.";
  return [
    `# RESUME CODING: ${title}`,
    `**Target LLM:** ${targetLLM || 'Universal'}`,
    `## Objective\n${description || 'None'}`,
    notes ? `## Architecture\n${notes}` : "",
    issues ? `## Open Bugs to Fix\n${issues}` : "",
    "---",
    "Resolve [BLOCKER] items first. Provide clean diffs."
  ].filter(Boolean).join("\n");
}

function PARSE_ISSUE_SEVERITY(issuesText) {
  if (!issuesText) return "CLEAN";
  const u = issuesText.toUpperCase();
  if (u.includes("[BLOCKER]")) return "BLOCKER";
  if (u.includes("[MAJOR]")) return "MAJOR";
  if (u.includes("[MINOR]")) return "MINOR";
  return "CLEAN";
}
