#!/usr/bin/env node
/**
 * Resolve Notion Publisher targets from a content package.
 * Usage:
 *   node resolve-channels.mjs --package=<path> [--sources=A,B] [--channels=C]
 *                             [--producer-skill=<SKILL.md>] [--self-check]
 */
import fs from 'fs';
import path from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

function arg(name) {
  const hit = process.argv.find((a) => a.startsWith(`--${name}=`));
  return hit ? hit.slice(name.length + 3) : undefined;
}
function hasFlag(name) {
  return process.argv.includes(`--${name}`);
}

function parseFrontmatter(raw) {
  if (!raw.startsWith('---')) return { meta: {}, body: raw };
  const end = raw.indexOf('\n---', 3);
  if (end === -1) return { meta: {}, body: raw };
  const yaml = raw.slice(3, end).trim();
  const body = raw.slice(end + 4).replace(/^\n/, '');
  return { meta: looseYaml(yaml), body };
}

/** ponytail: enough YAML for cms:/title — not a full parser. Ceiling: nested lists of scalars. */
function looseYaml(text) {
  const out = {};
  let key = null;
  for (const line of text.split('\n')) {
    const m = line.match(/^([A-Za-z0-9_]+):\s*(.*)$/);
    if (m) {
      key = m[1];
      const v = m[2].trim();
      if (v === '' || v === '|' || v === '>') {
        out[key] = out[key] ?? {};
        continue;
      }
      out[key] = parseScalar(v);
      continue;
    }
    const list = line.match(/^\s+-\s+(.+)$/);
    if (list && key) {
      if (!Array.isArray(out[key])) out[key] = [];
      out[key].push(parseScalar(list[1]));
      continue;
    }
    const nested = line.match(/^\s+([A-Za-z0-9_]+):\s*(.*)$/);
    if (nested && key && typeof out[key] === 'object' && !Array.isArray(out[key])) {
      const nv = nested[2].trim();
      out[key][nested[1]] = nv === '' ? [] : parseScalar(nv);
      if (nv === '') {
        // keep collecting list under nested key via key pointer hack
        key = `${key}.${nested[1]}`;
      }
    }
  }
  // flatten cms.layer style from accidental "cms.layer" keys
  if (out.cms && typeof out.cms === 'object') {
    for (const [k, v] of Object.entries(out)) {
      if (k.startsWith('cms.') && k !== 'cms') {
        out.cms[k.slice(4)] = v;
        delete out[k];
      }
    }
  }
  return out;
}

function parseScalar(v) {
  if ((v.startsWith('[') && v.endsWith(']')) || (v.startsWith('"') && v.endsWith('"'))) {
    if (v.startsWith('[')) {
      return v
        .slice(1, -1)
        .split(',')
        .map((s) => s.trim().replace(/^["']|["']$/g, ''))
        .filter(Boolean);
    }
    return v.slice(1, -1);
  }
  return v.replace(/^["']|["']$/g, '');
}

function asList(v) {
  if (v == null || v === '') return [];
  if (Array.isArray(v)) return v.map(String);
  return [String(v)];
}

function uniq(arr) {
  return [...new Set(arr.filter(Boolean))];
}

function headings(body) {
  return [...body.matchAll(/^#+\s+(.+)$/gm)].map((m) => m[1].trim());
}

function extractCms(meta) {
  const cms = meta.cms && typeof meta.cms === 'object' ? meta.cms : {};
  // also accept top-level mistyped keys already nested by looseYaml
  return {
    layer: asList(cms.layer),
    sources: asList(cms.sources),
    channels: asList(cms.channels),
    expand: cms.expand || 'multi',
  };
}

function heuristics(body, filePath) {
  const h = headings(body).join('\n').toLowerCase();
  const base = path.basename(filePath).toLowerCase();
  const layer = [];
  const sources = [];
  const channels = [];

  const hit = (...needles) => needles.some((n) => h.includes(n) || base.includes(n));

  if (hit('landing page copy', 'gumroad title', 'gumroad')) {
    layer.push('Products');
    sources.push('Gumroad');
  }
  if (hit('github repo', 'release tag', 'release notes')) {
    layer.push('Products');
    sources.push('GitHub');
  }
  if (hit('caption', 'pov', 'instagram caption', 'postly')) {
    layer.push('Social');
    sources.push('Postly');
  }
  if (hit('reddit title', 'reddit body', 'reddit subreddit', 'reddit')) {
    layer.push('Social');
    sources.push('Composio');
    channels.push('Reddit');
  }
  if (hit('luma title', 'luma start', 'luma description', 'luma')) {
    layer.push('Events');
    sources.push('Luma');
  }
  return { layer, sources, channels };
}

function sectionMap(body) {
  const map = {};
  const parts = body.split(/^#+\s+/m).filter(Boolean);
  for (const part of parts) {
    const nl = part.indexOf('\n');
    const title = (nl === -1 ? part : part.slice(0, nl)).trim();
    const content = (nl === -1 ? '' : part.slice(nl + 1)).trim();
    if (title) map[title] = content;
  }
  return map;
}

function pickTitle(meta, sections) {
  return (
    meta.title ||
    sections['Gumroad Title'] ||
    sections['Luma Title'] ||
    sections['Name'] ||
    sections['Reddit Title'] ||
    'Untitled package'
  );
}

const BUTTONS = {
  Gumroad: 'Publish in Gumroad',
  Postly: 'Publish in Social',
  Composio: 'Publish in Composio',
  Luma: 'Publish in Luma',
  GitHub: 'Publish in GitHub',
  Skool: 'Publish in Skool (when live)',
};

const STATUS_PROP = {
  Gumroad: 'Gumroad Publish Status',
  Postly: 'Postly Publish Status',
  Composio: 'Composio Publish Status',
  Luma: 'Luma Publish Status',
  GitHub: 'GitHub Publish Status',
  Skool: 'Skool Publish Status',
};

const SOURCE_LAYER = {
  Gumroad: 'Products',
  GitHub: 'Products',
  Skool: 'Products',
  Postly: 'Social',
  Composio: 'Social',
  Luma: 'Events',
  ONCE: 'Music',
};

function resolve(opts) {
  const raw = fs.readFileSync(opts.packagePath, 'utf8');
  const { meta, body } = parseFrontmatter(raw);
  const sections = sectionMap(body);
  const pkg = extractCms(meta);
  let producer = { layer: [], sources: [], channels: [] };
  if (opts.producerSkill) {
    const pRaw = fs.readFileSync(opts.producerSkill, 'utf8');
    producer = extractCms(parseFrontmatter(pRaw).meta);
  }
  const heur = heuristics(body, opts.packagePath);

  const overrideSources = opts.sources;
  const overrideChannels = opts.channels;

  const sources = uniq(
    overrideSources.length
      ? overrideSources
      : [...pkg.sources, ...producer.sources, ...heur.sources]
  );
  const channels = uniq(
    overrideChannels.length
      ? overrideChannels
      : [...pkg.channels, ...producer.channels, ...heur.channels]
  );
  let layers = uniq([...pkg.layer, ...producer.layer, ...heur.layer]);
  if (!layers.length) {
    layers = uniq(sources.map((s) => SOURCE_LAYER[s]).filter(Boolean));
  }

  const title = String(pickTitle(meta, sections)).trim();
  const missing = [];
  if (!title || title === 'Untitled package') missing.push('title');
  if (!layers.length) missing.push('layer (cms.layer or heuristics)');
  if (!sources.length) missing.push('sources (cms.sources or heuristics)');

  // recommended field checklist (non-blocking)
  const recommended = [];
  if (sources.includes('Gumroad') && !sections['Landing Page Copy']) recommended.push('Landing Page Copy');
  if (sources.includes('Postly') && !(sections['Caption'] || sections['POV'])) recommended.push('Caption');
  if (sources.includes('Composio') && !sections['Reddit Body']) recommended.push('Reddit Body');
  if (sources.includes('Luma') && !sections['Luma Start']) recommended.push('Luma Start');

  const byLayer = {};
  for (const src of sources) {
    const layer = SOURCE_LAYER[src] || layers[0] || 'Social';
    if (!byLayer[layer]) byLayer[layer] = { layer, sources: [], channels: [], statusProps: [] };
    byLayer[layer].sources.push(src);
    if (STATUS_PROP[src]) byLayer[layer].statusProps.push(STATUS_PROP[src]);
  }
  for (const ch of channels) {
    // Reddit → Social page
    const layer = ch === 'Eventbrite' ? 'Events' : 'Social';
    if (!byLayer[layer]) byLayer[layer] = { layer, sources: [], channels: [], statusProps: [] };
    byLayer[layer].channels.push(ch);
  }

  const pages = Object.values(byLayer).map((p) => ({
    layer: p.layer,
    sources: uniq(p.sources),
    channels: uniq(p.channels),
    statusProps: uniq(p.statusProps),
    title,
    fields: sections,
  }));

  const buttons = uniq(sources.map((s) => BUTTONS[s]).filter(Boolean));

  return {
    title,
    layers,
    sources,
    channels,
    pages,
    missing,
    recommended,
    buttons,
    ok: missing.length === 0,
  };
}

function selfCheck() {
  const fixture = path.join(__dirname, '..', 'fixtures', 'sample-package.md');
  const result = resolve({
    packagePath: fixture,
    sources: [],
    channels: [],
    producerSkill: undefined,
  });
  const wantLayers = ['Products', 'Social'];
  const wantSources = ['Gumroad', 'Postly'];
  const layersOk = wantLayers.every((l) => result.layers.includes(l));
  const sourcesOk = wantSources.every((s) => result.sources.includes(s));
  const pagesOk = result.pages.length === 2;
  if (!layersOk || !sourcesOk || !pagesOk || !result.ok) {
    console.error('SELF-CHECK FAIL', JSON.stringify(result, null, 2));
    process.exit(1);
  }
  console.log(
    JSON.stringify(
      { selfCheck: 'ok', layers: result.layers, sources: result.sources, pages: result.pages.length },
      null,
      2
    )
  );
}

function main() {
  if (hasFlag('self-check')) {
    selfCheck();
    return;
  }
  const pkg = arg('package');
  if (!pkg) {
    console.error('Usage: resolve-channels.mjs --package=<path> [--self-check]');
    process.exit(2);
  }
  const packagePath = path.resolve(pkg);
  if (!fs.existsSync(packagePath)) {
    console.error(`Package not found: ${packagePath}`);
    process.exit(2);
  }
  const result = resolve({
    packagePath,
    sources: asList(arg('sources') ? arg('sources').split(',') : []),
    channels: asList(arg('channels') ? arg('channels').split(',') : []),
    producerSkill: arg('producer-skill'),
  });
  console.log(JSON.stringify(result, null, 2));
  process.exit(result.ok ? 0 : 1);
}

main();
