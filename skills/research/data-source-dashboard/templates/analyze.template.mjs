#!/usr/bin/env node
// __TITLE__ — raw source -> metrics.json (aggregates only; the raw file is read in place)
// Usage: node analyze.mjs "<path-to-raw-export>"
//
// MAP THE SOURCE FIRST: set FIELDS below, then delete the blocks that do not apply.
// Everything here is a primitive you keep or drop — no section is mandatory.
import { readFileSync, writeFileSync } from 'node:fs';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const HERE = dirname(fileURLToPath(import.meta.url));
const srcPath = process.argv[2];
if (!srcPath) { console.error('usage: node analyze.mjs "<path-to-raw-export>"'); process.exit(2); }

/* ── field map: the only part that is source-specific ────────────────── */
const FIELDS = {
  timestamp: 'created_at',   // ISO date or datetime — drives every time series
  id: 'id',                  // stable record id
  email: 'email',            // optional; used for domain buckets, never published
  tags: 'tags',              // optional; comma/semicolon separated
  actions: null,             // optional column: how many times this record acted
  completed: null,           // optional column: how many times it followed through
};
const PERSONAL_DOMAINS = new Set(['gmail.com', 'hotmail.com', 'outlook.com', 'yahoo.com', 'icloud.com', 'proton.me', 'live.com']);

/* ── CSV parser (quoted fields, embedded commas and newlines) ─────────── */
function parseCSV(text) {
  const rows = []; let row = [], field = '', q = false;
  for (let i = 0; i < text.length; i++) {
    const c = text[i];
    if (q) {
      if (c === '"') { if (text[i + 1] === '"') { field += '"'; i++; } else q = false; } else field += c;
    } else if (c === '"') q = true;
    else if (c === ',') { row.push(field); field = ''; }
    else if (c === '\n' || c === '\r') {
      if (c === '\r' && text[i + 1] === '\n') i++;
      row.push(field); field = '';
      if (row.length > 1 || row[0] !== '') rows.push(row);
      row = [];
    } else field += c;
  }
  if (field !== '' || row.length) { row.push(field); rows.push(row); }
  return rows;
}

const raw = readFileSync(srcPath, 'utf8').replace(/^﻿/, '');
const table = parseCSV(raw);
const header = table.shift().map((h) => h.trim());
const col = Object.fromEntries(header.map((h, i) => [h, i]));
const get = (r, key) => (FIELDS[key] && col[FIELDS[key]] !== undefined ? (r[col[FIELDS[key]]] ?? '').trim() : '');

const records = table.map((r) => ({
  ts: get(r, 'timestamp'),
  email: get(r, 'email').toLowerCase(),
  tags: get(r, 'tags'),
  actions: parseInt(get(r, 'actions') || '0', 10) || 0,
  completed: parseInt(get(r, 'completed') || '0', 10) || 0,
}));
const total = records.length;
if (!total) { console.error('no rows parsed — check FIELDS against the header'); process.exit(4); }

/* ── 01 growth: dense daily series, weekly, monthly, rates ───────────── */
const DAY = 86400000;
const byDay = new Map();
for (const r of records) {
  const d = r.ts.slice(0, 10);
  if (/^\d{4}-\d{2}-\d{2}$/.test(d)) byDay.set(d, (byDay.get(d) ?? 0) + 1);
}
const days = [...byDay.keys()].sort();
const firstDay = days[0], lastDay = days[days.length - 1];
const daily = [];
for (let t = Date.parse(firstDay), end = Date.parse(lastDay), cum = 0; t <= end; t += DAY) {
  const d = new Date(t).toISOString().slice(0, 10);
  cum += byDay.get(d) ?? 0;
  daily.push({ d, n: byDay.get(d) ?? 0, cum });
}
const isoWeek = (d) => {
  const dt = new Date(d + 'T00:00:00Z');
  dt.setUTCDate(dt.getUTCDate() - ((dt.getUTCDay() + 6) % 7) + 3);
  const jan4 = new Date(Date.UTC(dt.getUTCFullYear(), 0, 4));
  const w = 1 + Math.round(((dt - jan4) / DAY - 3 + ((jan4.getUTCDay() + 6) % 7)) / 7);
  return `${dt.getUTCFullYear()}-W${String(w).padStart(2, '0')}`;
};
const group = (keyFn) => {
  const m = new Map();
  for (const { d, n } of daily) m.set(keyFn(d), (m.get(keyFn(d)) ?? 0) + n);
  return [...m.entries()];
};
const weekly = group(isoWeek).map(([w, n]) => ({ w, n }));
const monthly = group((d) => d.slice(0, 7)).map(([mo, n]) => ({ mo, n }));
const win = (back, len) => daily.slice(Math.max(0, daily.length - back - len), daily.length - back).reduce((s, x) => s + x.n, 0);
const last7 = win(0, 7), prev7 = win(7, 7), last30 = win(0, 30), prev30 = win(30, 30), last90 = win(0, 90);
const base30 = daily[Math.max(0, daily.length - 31)].cum;
const rate30 = base30 > 0 ? last30 / base30 : 0;
const peak = daily.reduce((a, b) => (b.n > a.n ? b : a), daily[0]);
const sortedWeekly = weekly.map((w) => w.n).sort((a, b) => a - b);
const medianWeekly = sortedWeekly.length % 2
  ? sortedWeekly[(sortedWeekly.length - 1) / 2]
  : Math.round((sortedWeekly[sortedWeekly.length / 2 - 1] + sortedWeekly[sortedWeekly.length / 2]) / 2);
const top10 = [...daily].sort((a, b) => b.n - a.n).slice(0, 10);

/* ── 02 acquisition: origin buckets + long tail ──────────────────────── */
const domCount = new Map();
for (const r of records) {
  const at = r.email.lastIndexOf('@');
  if (at > 0) { const d = r.email.slice(at + 1); domCount.set(d, (domCount.get(d) ?? 0) + 1); }
}
const isEdu = (d) => /\.edu(\.[a-z]{2})?$|\.ac\.[a-z]{2}$/.test(d);
let personal = 0, edu = 0, other = 0;
for (const [d, n] of domCount) (PERSONAL_DOMAINS.has(d) ? (personal += n) : isEdu(d) ? (edu += n) : (other += n));
const topBy = (pred, k = 10) => [...domCount.entries()].filter(([d]) => pred(d)).sort((a, b) => b[1] - a[1]).slice(0, k).map(([dom, n]) => ({ dom, n }));

/* ── 03 engagement funnel ────────────────────────────────────────────── */
const acted1 = records.filter((r) => r.actions >= 1).length;
const acted2 = records.filter((r) => r.actions >= 2).length;
const completed1 = records.filter((r) => r.completed >= 1).length;
const dist = new Map();
for (const r of records) { const b = r.actions >= 5 ? '5+' : String(r.actions); dist.set(b, (dist.get(b) ?? 0) + 1); }

/* ── 04 cohorts + 05 engine (spikes, velocity) ───────────────────────── */
const splitTags = (s) => (s ? s.split(/[;,]/).map((x) => x.trim()).filter(Boolean) : []);
const tagCount = new Map();
for (const r of records) for (const t of splitTags(r.tags)) tagCount.set(t, (tagCount.get(t) ?? 0) + 1);
const tags = [...tagCount.entries()].sort((a, b) => b[1] - a[1]);
const topTags = tags.slice(0, 12).map(([t]) => t);
const cohortWeekly = {};
for (const r of records) {
  const d = r.ts.slice(0, 10);
  if (!/^\d{4}-\d{2}-\d{2}$/.test(d)) continue;
  const w = isoWeek(d), ts = splitTags(r.tags);
  const bump = (name) => { (cohortWeekly[name] ??= {})[w] = (cohortWeekly[name][w] ?? 0) + 1; };
  if (!ts.length) bump('untagged');
  for (const t of ts) if (topTags.includes(t)) bump(t);
}
const cutoff = daily[Math.max(0, daily.length - 30)].d;
const recentTag = new Map(); let recentTotal = 0;
for (const r of records) {
  const d = r.ts.slice(0, 10);
  if (d < cutoff) continue;
  recentTotal++;
  for (const t of splitTags(r.tags)) recentTag.set(t, (recentTag.get(t) ?? 0) + 1);
}
const velocity = topTags.map((t) => {
  const hist = (tagCount.get(t) ?? 0) / total;
  const recentShare = recentTotal ? (recentTag.get(t) ?? 0) / recentTotal : 0;
  return { t, recent: recentTag.get(t) ?? 0, recentSharePct: +(recentShare * 100).toFixed(1), histSharePct: +(hist * 100).toFixed(1), idx: hist ? +(recentShare / hist).toFixed(2) : null };
}).sort((a, b) => b.recent - a.recent);
const spikes = top10.slice(0, 6).map(({ d, n }) => {
  const m = new Map();
  for (const r of records) if (r.ts.slice(0, 10) === d) for (const t of splitTags(r.tags)) m.set(t, (m.get(t) ?? 0) + 1);
  return { d, n, topTags: [...m.entries()].sort((a, b) => b[1] - a[1]).slice(0, 4).map(([t, c]) => ({ t, c, pct: +((c / n) * 100).toFixed(0) })) };
});

/* ── 07 forecast: linear scenarios to a horizon ──────────────────────── */
const ageDays = daily.length;
const HORIZON = process.env.HORIZON || `${new Date(lastDay).getUTCFullYear()}-12-31`;
const daysToHorizon = Math.max(1, Math.round((Date.parse(HORIZON) - Date.parse(lastDay)) / DAY));
const top3 = [...monthly].sort((a, b) => b.n - a.n).slice(0, 3);
const scenarios = [
  { key: 'current', label: 'current 30d pace', perDay: last30 / 30 },
  { key: 'lifetime', label: 'lifetime average', perDay: total / ageDays },
  { key: 'best', label: 'best-months pace', perDay: top3.reduce((s, m) => s + m.n, 0) / 3 / 30.44 },
].map((s) => {
  const proj = (d) => Math.round(total + s.perDay * d);
  const eta = (target) => (s.perDay <= 0 || total >= target ? null
    : new Date(Date.parse(lastDay) + Math.ceil((target - total) / s.perDay) * DAY).toISOString().slice(0, 10));
  const round5 = Math.ceil((total * 1.1) / 5000) * 5000;
  return { ...s, perDay: +s.perDay.toFixed(1), at30: proj(30), at90: proj(90), at180: proj(180), atHorizon: proj(daysToHorizon), milestone: round5, etaMilestone: eta(round5) };
});

/* ── write aggregates ────────────────────────────────────────────────── */
const metrics = {
  title: '__TITLE__',
  generatedAt: new Date().toISOString(),
  exportDate: lastDay,
  totals: { records: total, withTags: records.filter((r) => r.tags).length },
  growth: {
    firstDay, lastDay, daily, weekly, monthly,
    last7, prev7, last30, prev30, last90,
    peakDay: peak.d, peakCount: peak.n,
  },
  growthRate: {
    wowNowPct: prev7 ? +(((last7 - prev7) / prev7) * 100).toFixed(1) : null,
    momNowPct: prev30 ? +(((last30 - prev30) / prev30) * 100).toFixed(1) : null,
    listRate30Pct: +(rate30 * 100).toFixed(1),
    doublingMonths: rate30 > 0 ? +(Math.log(2) / Math.log(1 + rate30)).toFixed(1) : null,
  },
  kpis: {
    medianWeekly,
    top10DaysTotal: top10.reduce((s, d) => s + d.n, 0),
    spikeDependencePct: +((top10.reduce((s, d) => s + d.n, 0) / total) * 100).toFixed(1),
    returning: acted2,
    returningPct: +((acted2 / total) * 100).toFixed(1),
  },
  age: { days: ageDays, months: +(ageDays / 30.44).toFixed(1), perDay: +(total / ageDays).toFixed(1) },
  domains: { unique: domCount.size, personal, edu, other, top: topBy(() => true, 15), topEdu: topBy(isEdu), topCorporate: topBy((d) => !PERSONAL_DOMAINS.has(d) && !isEdu(d)) },
  funnel: {
    records: total, acted1, acted2, completed1,
    actedRatePct: +((acted1 / total) * 100).toFixed(1),
    dist: [...dist.entries()].sort((a, b) => (a[0] === '5+' ? 1 : b[0] === '5+' ? -1 : +a[0] - +b[0])),
    never: total - acted1,
    neverPct: +(((total - acted1) / total) * 100).toFixed(1),
  },
  tags, cohortWeekly, weekLabels: weekly.map((w) => w.w), velocity, spikes,
  forecast: { from: lastDay, horizon: HORIZON, daysToHorizon, scenarios },
};

writeFileSync(join(HERE, 'metrics.json'), JSON.stringify(metrics, null, 2));
console.log(`ok: ${total} records -> metrics.json`);
console.log(`range ${firstDay}..${lastDay} · last7=${last7} last30=${last30} peak=${peak.d}(${peak.n})`);
console.log(`acted≥1 ${acted1} · returning ${acted2} · never ${total - acted1}`);
