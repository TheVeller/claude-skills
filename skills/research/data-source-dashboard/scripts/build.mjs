#!/usr/bin/env node
// dashboard.template.html + metrics.json (+ visuals/*.png) -> dashboard.html
// Usage: node build.mjs <project-dir>
// Exit: 2 bad args · 4 missing input
import { readFileSync, writeFileSync, existsSync, readdirSync } from 'node:fs';
import { join, basename, extname } from 'node:path';

const dir = process.argv[2];
if (!dir) { console.error('usage: build.mjs <project-dir>'); process.exit(2); }

const tplPath = join(dir, 'dashboard.template.html');
const metricsPath = join(dir, 'metrics.json');
for (const p of [tplPath, metricsPath]) {
  if (!existsSync(p)) { console.error(`missing ${p} — run analyze.mjs first`); process.exit(4); }
}

let html = readFileSync(tplPath, 'utf8');

// metrics ride inside a <script type="application/json"> block, so "<" must not
// close it early
const metrics = readFileSync(metricsPath, 'utf8').replace(/</g, '\\u003c');
html = html.replace('__METRICS_JSON__', metrics);

// diagrams: __DIAGRAM_<NAME>__ -> data: URI of visuals/<name>.png
const visuals = join(dir, 'visuals');
const embedded = [];
if (existsSync(visuals)) {
  for (const f of readdirSync(visuals).filter((f) => extname(f) === '.png')) {
    const key = `__DIAGRAM_${basename(f, '.png').toUpperCase().replace(/[^A-Z0-9]+/g, '_')}__`;
    if (!html.includes(key)) continue;
    const b64 = readFileSync(join(visuals, f)).toString('base64');
    html = html.split(key).join(`data:image/png;base64,${b64}`);
    embedded.push(`${f} (${Math.round(b64.length / 1365)}KB)`);
  }
}

const leftover = html.match(/__(METRICS_JSON|DIAGRAM_[A-Z0-9_]+)__/g);
writeFileSync(join(dir, 'dashboard.html'), html);

const kb = Math.round(Buffer.byteLength(html) / 1024);
console.log(`ok: dashboard.html ${kb}KB${embedded.length ? ' · embedded ' + embedded.join(', ') : ''}`);
if (leftover) console.warn(`warn: unresolved placeholders — ${[...new Set(leftover)].join(', ')}`);
if (kb > 16000) console.warn('warn: over the 16MB artifact ceiling — shrink the diagrams');
