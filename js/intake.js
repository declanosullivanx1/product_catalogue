/**
 * UUIDv7: 01a2133a-c9ff-75eb-9d21-914ed00ac813
 * Timestamp: 2026-11-25T15:02:29Z
 * Client Intake Logic & LocalStorage Stash
 */

(function () {
  'use strict';

  const STORAGE_KEY = 'catalog_intake_draft_v2';
  const statusBadge = document.getElementById('draft-status');

  function generateUUIDv7() {
    const now = Date.now();
    const timeHex = now.toString(16).padStart(12, '0');
    const randA = Math.floor(Math.random() * 0x0FFF).toString(16).padStart(3, '0');
    const randB1 = (Math.floor(Math.random() * 0x3FFF) | 0x8000).toString(16).padStart(4, '0');
    const randB2 = Math.floor(Math.random() * 0xFFFFFFFFFFFF).toString(16).padStart(12, '0');
    return `${timeHex.slice(0, 8)}-${timeHex.slice(8, 12)}-7${randA}-${randB1}-${randB2}`;
  }

  function setDirty(isDirty) {
    if (!statusBadge) return;
    if (isDirty) {
      statusBadge.textContent = 'Unsaved Changes';
      statusBadge.className = 'status-badge badge-dirty';
    } else {
      statusBadge.textContent = 'Draft Stashed';
      statusBadge.className = 'status-badge badge-saved';
    }
  }

  function detectPlatform(url) {
    if (/aistudio\.google\.com/i.test(url)) return "Google AI Studio Web App";
    if (/gemini\.google\.com/i.test(url)) return "Gemini Chat Web App";
    if (/qwen|tongyi\.aliyun/i.test(url)) return "Qwen AI Studio";
    if (/kimi\.moonshot\.cn/i.test(url)) return "Kimi AI";
    if (/chatgpt\.com|chat\.openai\.com/i.test(url)) return "ChatGPT Web App";
    if (/claude\.ai/i.test(url)) return "Claude AI Web App";
    return "";
  }

  function saveToStorage() {
    const payload = {
      uuid: document.getElementById('uuid-field').value,
      account: document.getElementById('account-select').value,
      link: document.getElementById('chat-link').value,
      llm: document.getElementById('llm-select').value,
      title: document.getElementById('project-title').value,
      desc: document.getElementById('project-desc').value,
      notes: document.getElementById('project-notes').value,
      issues: document.getElementById('project-issues').value
    };
    try {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(payload));
      setDirty(false);
    } catch (e) {}
  }

  function loadFromStorage() {
    let saved = null;
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) saved = JSON.parse(raw);
    } catch (e) {}

    if (saved) {
      document.getElementById('uuid-field').value = saved.uuid || generateUUIDv7();
      document.getElementById('account-select').value = saved.account || "declanjosephosullivan@gmail.com";
      document.getElementById('chat-link').value = saved.link || "";
      document.getElementById('llm-select').value = saved.llm || "";
      document.getElementById('project-title').value = saved.title || "";
      document.getElementById('project-desc').value = saved.desc || "";
      document.getElementById('project-notes').value = saved.notes || "";
      document.getElementById('project-issues').value = saved.issues || "";
      setDirty(false);
    } else {
      document.getElementById('uuid-field').value = generateUUIDv7();
      setDirty(false);
    }
  }

  document.getElementById('account-select').addEventListener('change', saveToStorage);
  document.getElementById('chat-link').addEventListener('input', (e) => {
    const detected = detectPlatform(e.target.value);
    if (detected) document.getElementById('llm-select').value = detected;
    setDirty(true);
    saveToStorage();
  });

  ['llm-select', 'project-title', 'project-desc', 'project-notes', 'project-issues'].forEach(id => {
    document.getElementById(id).addEventListener('input', () => {
      setDirty(true);
      saveToStorage();
    });
  });

  document.getElementById('clear-draft-btn').addEventListener('click', () => {
    if (confirm("Reset current draft?")) {
      localStorage.removeItem(STORAGE_KEY);
      document.getElementById('intake-form').reset();
      document.getElementById('uuid-field').value = generateUUIDv7();
      setDirty(false);
    }
  });

  document.getElementById('copy-tsv-btn').addEventListener('click', () => {
    const row = [
      document.getElementById('uuid-field').value,
      document.getElementById('account-select').value,
      document.getElementById('llm-select').value,
      document.getElementById('chat-link').value,
      document.getElementById('project-title').value,
      document.getElementById('project-desc').value.replace(/\n/g, ' '),
      document.getElementById('project-notes').value.replace(/\n/g, ' '),
      document.getElementById('project-issues').value.replace(/\n/g, ' ')
    ];
    navigator.clipboard.writeText(row.join('\t')).then(() => {
      alert("TSV Row copied to clipboard! Paste directly into Google Sheets (Column A).");
    });
  });

  loadFromStorage();
})();
