/**
 * UUIDv7: 01a2133a-ca11-75be-82c9-7def1f565eab
 * Timestamp: 2026-11-25T15:02:29Z
 * Secret Key & PII Redactor
 */

const SECRET_PATTERNS = [
  { name: "OPENAI_API_KEY", regex: /sk-[a-zA-Z0-9_-]{32,}/g },
  { name: "OPENAI_PROJECT_KEY", regex: /sk-proj-[a-zA-Z0-9_-]{40,}/g },
  { name: "ANTHROPIC_API_KEY", regex: /sk-ant-[a-zA-Z0-9_-]{40,}/g },
  { name: "GITHUB_PAT", regex: /(ghp_[a-zA-Z0-9]{36}|github_pat_[a-zA-Z0-9_]{60,})/g },
  { name: "CLOUDFLARE_API_KEY", regex: /[0-9a-f]{40}/g },
  { name: "GOOGLE_AI_STUDIO_KEY", regex: /AIzaSy[a-zA-Z0-9_-]{33}/g },
  { name: "AWS_ACCESS_KEY_ID", regex: /(A3T[A-Z0-9]|AKIA|AGPA|AIDA|AROA|AIPA|ANPA|ANVA|ASIA)[A-Z0-9]{16}/g },
  { name: "JWT_ASSERTION", regex: /eyJ[a-zA-Z0-9_-]{10,}\.eyJ[a-zA-Z0-9_-]{10,}\.[a-zA-Z0-9_-]{10,}/g }
];

const APPROVED_EMAILS = [
  "declanosullivanx1@gmail.com",
  "declanjosephosullivan@gmail.com",
  "cathal.and.declan@gmail.com",
  "declanjosullivan86@gmail.com",
  "declanseer@gmail.com",
  "declanjoseph2025@gmail.com",
  "davewilson1x1@gmail.com",
  "charlie.and.declan.osullivan@gmail.com",
  "declan@transparency-x.com"
];

export function scanAndSanitize(input) {
  if (!input || typeof input !== "string") return { sanitizedText: input || "", violations: [], containsHardBlocker: false };

  let text = input;
  const violations = [];
  let containsHardBlocker = false;

  for (const pattern of SECRET_PATTERNS) {
    if (pattern.regex.test(text)) {
      containsHardBlocker = true;
      violations.push({ type: "SECRET", pattern: pattern.name });
      text = text.replace(pattern.regex, `[REDACTED_SECRET_${pattern.name}]`);
    }
    pattern.regex.lastIndex = 0;
  }

  const emailRegex = /\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b/g;
  text = text.replace(emailRegex, (m) => {
    if (APPROVED_EMAILS.includes(m.toLowerCase())) return m;
    violations.push({ type: "PII", pattern: "EXTERNAL_EMAIL" });
    return "[REDACTED_PII_EMAIL]";
  });

  return { sanitizedText: text, violations: violations, containsHardBlocker: containsHardBlocker };
}
