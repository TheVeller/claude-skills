#!/usr/bin/env node
// Publication gate: no PII, no credentials, aggregates that reconcile.
// Usage: node audit.mjs <project-dir> [--allow-name "Org One" --allow-name "Org Two"]
// Exit: 1 a gate failed · 2 bad args · 4 missing input
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

const dir = process.argv[2];
if (!dir) { console.error('usage: audit.mjs <project-dir> [--allow-name "..."]'); process.exit(2); }
const allowed = process.argv.reduce((acc, a, i, arr) => (a === '--allow-name' ? [...acc, arr[i + 1]] : acc), []);

const metricsPath = join(dir, 'metrics.json');
if (!existsSync(metricsPath)) { console.error(`missing ${metricsPath}`); process.exit(4); }
const raw = readFileSync(metricsPath, 'utf8');
const M = JSON.parse(raw);
const built = existsSync(join(dir, 'dashboard.html')) ? readFileSync(join(dir, 'dashboard.html'), 'utf8') : null;

let fails = 0, warns = 0;
const fail = (m) => { console.log(`FAIL  ${m}`); fails++; };
const warn = (m) => { console.log(`warn  ${m}`); warns++; };
const pass = (m) => console.log(`pass  ${m}`);

/* --- 1. credentials --------------------------------------------------- */
const KEY_RE = /\b(sk-[A-Za-z0-9]{16,}|secret-[A-Za-z0-9]{16,}|luma_sk_[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|xox[baprs]-[A-Za-z0-9-]{10,}|AIza[A-Za-z0-9_-]{20,})/g;
for (const [label, text] of [['metrics.json', raw], ['dashboard.html', built]]) {
  if (!text) continue;
  const hits = text.match(KEY_RE);
  hits ? fail(`${label}: credential-shaped string — ${[...new Set(hits)].map((h) => h.slice(0, 10) + '…').join(', ')}`)
       : pass(`${label}: no credentials`);
}

/* --- 2. personal data ------------------------------------------------- */
// an address-shaped string with a real TLD; tags like "Hack@latam" are not
const ADDR_RE = /[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}/g;
for (const [label, text] of [['metrics.json', raw], ['dashboard.html', built]]) {
  if (!text) continue;
  const hits = [...new Set(text.match(ADDR_RE) || [])].filter((h) => !allowed.includes(h));
  hits.length ? fail(`${label}: ${hits.length} address-shaped string(s) — ${hits.slice(0, 5).join(', ')}`)
              : pass(`${label}: no personal addresses`);
}
const nameKeys = Object.keys(M).filter((k) => /(^|_)(members|people|users|contacts|rows)$/i.test(k) && Array.isArray(M[k]));
for (const k of nameKeys) {
  if (M[k].some((r) => r && typeof r === 'object' && ('email' in r || 'first_name' in r || 'phone' in r))) {
    fail(`metrics.json: "${k}" carries per-person records — aggregate before publishing`);
  }
}
if (!nameKeys.length) pass('metrics.json: no per-person record arrays');

/* --- 3. aggregates reconcile ------------------------------------------ */
const num = (v) => typeof v === 'number' && isFinite(v);
const total = M.totals && (M.totals.members ?? M.totals.records ?? M.totals.count);
if (num(total)) {
  const series = [
    ['daily', M.growth?.daily?.map((d) => d.n)],
    ['weekly', M.growth?.weekly?.map((w) => w.n)],
    ['monthly', M.growth?.monthly?.map((m) => m.n)],
  ].filter(([, s]) => Array.isArray(s) && s.length);
  for (const [name, s] of series) {
    const sum = s.reduce((a, b) => a + b, 0);
    sum === total ? pass(`${name} series sums to totals (${total})`)
                  : fail(`${name} series sums ${sum}, totals says ${total}`);
  }
  const lastCum = M.growth?.daily?.[M.growth.daily.length - 1]?.cum;
  if (num(lastCum)) {
    lastCum === total ? pass('final cumulative equals totals') : fail(`final cumulative ${lastCum} ≠ totals ${total}`);
  }
  if (!series.length) warn('no growth series to reconcile');
} else {
  warn('no totals.{members,records,count} — skipping reconciliation');
}

/* --- 4. shares stay inside 0–100 -------------------------------------- */
const badPct = [];
(function scan(o, path) {
  if (!o || typeof o !== 'object') return;
  for (const [k, v] of Object.entries(o)) {
    const p = path ? `${path}.${k}` : k;
    if (num(v) && /pct$/i.test(k) && (v < -100 || v > 100)) badPct.push(`${p}=${v}`);
    else if (typeof v === 'object') scan(v, p);
  }
})(M, '');
badPct.length ? fail(`percentage out of range — ${badPct.slice(0, 5).join(', ')}`) : pass('percentages in range');

/* --- 5. provenance present -------------------------------------------- */
if (built) {
  /observed|benchmark|assumed|observado|supuesto/i.test(built)
    ? pass('dashboard carries provenance vocabulary')
    : warn('no provenance tags found in the built page');
}

console.log(`\n${fails ? 'AUDIT FAILED' : 'AUDIT PASSED'} — ${fails} fail · ${warns} warn`);
process.exit(fails ? 1 : 0);
