#!/usr/bin/env node

import { spawnSync } from 'node:child_process';
import { createHash } from 'node:crypto';
import { existsSync, lstatSync, readFileSync, readdirSync, realpathSync } from 'node:fs';
import { dirname, extname, isAbsolute, join, relative, resolve, sep } from 'node:path';
import { fileURLToPath } from 'node:url';

const REQUIRED_DOCUMENT_KEYS = [
  'architecture',
  'governance',
  'tooling',
  'data',
];

const REQUIRED_EXCLUSIONS = ['01_Journal', '03_Areas', '04_Resources'];
const SENSITIVE_PART = /(^|[._-])(\.env|secret|secrets|credential|credentials|token|tokens|api[-_]?key|private[-_]?key)([._/-]|$)/i;
const CONFIG_PATH = '.config/agentic-os-governance.json';
const SKILL_FILES = [
  '.claude/skills/govern-agentic-os/SKILL.md',
  '.claude/skills/govern-agentic-os/agents/openai.yaml',
  '.claude/skills/govern-agentic-os/references/governance-contract.md',
  '.claude/skills/govern-agentic-os/references/audit-protocol.md',
  '.claude/skills/govern-agentic-os/scripts/check.mjs',
  '.claude/skills/govern-agentic-os/scripts/check.test.mjs',
];

function defaultRoot() {
  return resolve(dirname(fileURLToPath(import.meta.url)), '../../../..');
}

export function parseArgs(argv) {
  const options = { mode: 'local', json: false, root: defaultRoot(), sessionStart: false };
  for (let i = 0; i < argv.length; i += 1) {
    const value = argv[i];
    if (value === '--local') options.mode = 'local';
    else if (value === '--live') options.mode = 'live';
    else if (value === '--json') options.json = true;
    else if (value === '--session-start') options.sessionStart = true;
    else if (value === '--root') {
      const next = argv[i + 1];
      if (!next || next.startsWith('--')) throw new Error('--root requires a path');
      options.root = resolve(next);
      i += 1;
    } else if (value === '--help' || value === '-h') options.help = true;
    else throw new Error(`unknown option: ${value}`);
  }
  return options;
}

function finding(level, code, message, path) {
  return { level, code, message, ...(path ? { path } : {}) };
}

function normalizedRelative(path) {
  return path.replaceAll('\\', '/').replace(/^\.\//, '');
}

function isWithin(root, candidate) {
  const rel = relative(root, candidate);
  return rel === '' || (!rel.startsWith(`..${sep}`) && rel !== '..' && !isAbsolute(rel));
}

function isExcludedPath(path, exclusions = REQUIRED_EXCLUSIONS) {
  const rel = normalizedRelative(path);
  return exclusions.some((prefix) => {
    const normalized = normalizedRelative(prefix).replace(/\/$/, '');
    return rel === normalized || rel.startsWith(`${normalized}/`);
  });
}

function isSensitivePath(path) {
  return normalizedRelative(path).split('/').some((part) => SENSITIVE_PART.test(part));
}

function safeRead(root, relPath, exclusions = REQUIRED_EXCLUSIONS, encoding = 'utf8') {
  const rel = normalizedRelative(relPath);
  if (!rel || isAbsolute(rel) || rel.split('/').includes('..')) {
    return { error: finding('error', 'unsafe-path', 'Path must be repository-relative without traversal.', relPath) };
  }
  if (isExcludedPath(rel, exclusions)) {
    return { error: finding('error', 'excluded-path', 'Refusing to read an absolutely excluded path.', rel) };
  }
  if (isSensitivePath(rel)) {
    return { error: finding('error', 'sensitive-path', 'Refusing to read a secret-like path.', rel) };
  }
  const absolute = resolve(root, rel);
  if (!isWithin(root, absolute)) {
    return { error: finding('error', 'unsafe-path', 'Resolved path escapes repository root.', rel) };
  }
  if (!existsSync(absolute)) {
    return { error: finding('error', 'missing-path', 'Declared path does not exist.', rel) };
  }
  return { value: readFileSync(absolute, encoding), absolute, relative: rel };
}

function safeLstat(path) {
  try {
    return lstatSync(path);
  } catch {
    return null;
  }
}

function safeRealpath(path) {
  try {
    return realpathSync(path);
  } catch {
    return null;
  }
}

function directoryEntries(root, relPath) {
  const path = resolve(root, relPath);
  if (!isWithin(root, path) || !existsSync(path)) return [];
  try {
    return readdirSync(path, { withFileTypes: true });
  } catch {
    return [];
  }
}

function defaultRunCommand(command, args, cwd) {
  const result = spawnSync(command, args, {
    cwd,
    encoding: 'utf8',
    env: {
      LANG: process.env.LANG ?? 'C',
      PATH: process.env.PATH ?? '',
    },
    timeout: 12000,
  });
  return {
    status: result.status ?? (result.error ? 2 : 0),
    stdout: result.stdout ?? '',
    stderr: result.stderr ?? '',
    error: result.error,
  };
}

function compactOutput(value) {
  return value.trim().split('\n').filter(Boolean).slice(0, 8).join(' | ').slice(0, 1200);
}

function validateConfig(config, findings) {
  if (!config || typeof config !== 'object' || Array.isArray(config)) {
    findings.push(finding('error', 'config-shape', 'Governance config must be a JSON object.', CONFIG_PATH));
    return;
  }
  if (config.schemaVersion !== 1) {
    findings.push(finding('error', 'config-version', 'Governance config schemaVersion must be 1.', CONFIG_PATH));
  }
  const documents = config.linear?.documents;
  if (!documents || typeof documents !== 'object') {
    findings.push(finding('error', 'documents-missing', 'Governance config must declare documents.', CONFIG_PATH));
  } else {
    for (const key of REQUIRED_DOCUMENT_KEYS) {
      if (!documents[key]) {
        findings.push(finding('error', 'document-key-missing', `Missing canonical document key: ${key}.`, CONFIG_PATH));
      }
    }
    for (const [key, document] of Object.entries(documents)) {
      if (!document || typeof document !== 'object' || Array.isArray(document)) {
        findings.push(finding('error', 'document-shape', `Document ${key} must be an object.`, CONFIG_PATH));
        continue;
      }
      for (const forbidden of ['body', 'content', 'markdown', 'text']) {
        if (Object.hasOwn(document, forbidden)) {
          findings.push(finding('error', 'canonical-copy', `Document ${key} must not copy canonical field ${forbidden}.`, CONFIG_PATH));
        }
      }
      if (!document.id || typeof document.id !== 'string') {
        findings.push(finding('error', 'document-id-missing', `Document ${key} needs id.`, CONFIG_PATH));
      }
      if (!document.url || typeof document.url !== 'string') {
        findings.push(finding('error', 'document-url-missing', `Document ${key} needs url.`, CONFIG_PATH));
      }
    }
  }
  const exclusions = config.audit?.excludedRoots;
  if (!Array.isArray(exclusions)) {
    findings.push(finding('error', 'exclusions-missing', 'Governance config must declare excludedPaths.', CONFIG_PATH));
  } else {
    for (const required of REQUIRED_EXCLUSIONS) {
      if (!exclusions.map((value) => value.replace(/\/$/, '')).includes(required)) {
        findings.push(finding('error', 'required-exclusion-missing', `Missing absolute exclusion: ${required}.`, CONFIG_PATH));
      }
    }
  }
  if (config.canonicalLanguage !== 'es' || config.ossTargetLanguage !== 'en') {
    findings.push(finding('error', 'language-policy', 'Language policy must declare canonical=es and ossTarget=en.', CONFIG_PATH));
  }
  const phase0 = config.phases?.phase0;
  const expectedCore = Array.from({ length: 10 }, (_, index) => `0.${index + 1}`);
  if (JSON.stringify(phase0?.core) !== JSON.stringify(expectedCore)) {
    findings.push(finding('error', 'phase0-core', 'Phase 0 core must be contiguous from 0.1 through 0.10.', CONFIG_PATH));
  }
  if (JSON.stringify(phase0?.amendments) !== JSON.stringify(['0.1a', '0.4b'])) {
    findings.push(finding('error', 'phase0-amendments', 'Phase 0 amendments must be 0.1a and 0.4b.', CONFIG_PATH));
  }
  const phase2 = config.phases?.phase2;
  if (phase2?.count !== 25 || phase2?.first !== '2.1' || phase2?.last !== '2.25' || !phase2?.gateIssue) {
    findings.push(finding('error', 'phase2-sequence', 'Phase 2 must declare 25 canonical positions from 2.1 through 2.25 and one gate issue.', CONFIG_PATH));
  }
  const checks = config.checks;
  if (!checks || typeof checks !== 'object' || Array.isArray(checks)) {
    findings.push(finding('error', 'checks-missing', 'Governance config must declare deterministic local checks.', CONFIG_PATH));
  } else {
    for (const key of ['packageFile', 'intentionScript', 'trackerScript', 'skillIndex']) {
      if (!checks[key] || typeof checks[key] !== 'string') {
        findings.push(finding('error', 'check-path-missing', `Governance checks need ${key}.`, CONFIG_PATH));
      }
    }
    if (!checks.requiredPackageScripts || typeof checks.requiredPackageScripts !== 'object') {
      findings.push(finding('error', 'required-scripts-missing', 'Governance checks need requiredPackageScripts.', CONFIG_PATH));
    }
    if (!Array.isArray(checks.forbiddenPackageScripts)) {
      findings.push(finding('error', 'forbidden-scripts-missing', 'Governance checks need forbiddenPackageScripts.', CONFIG_PATH));
    }
  }
}

function maskInlineCode(markdown) {
  let output = '';
  let plainStart = 0;

  for (let i = 0; i < markdown.length;) {
    if (markdown[i] !== '`') {
      i += 1;
      continue;
    }
    let delimiterLength = 1;
    while (markdown[i + delimiterLength] === '`') delimiterLength += 1;
    let closing = i + delimiterLength;
    while (closing < markdown.length) {
      if (markdown[closing] !== '`') {
        closing += 1;
        continue;
      }
      let closingLength = 1;
      while (markdown[closing + closingLength] === '`') closingLength += 1;
      if (closingLength === delimiterLength) break;
      closing += closingLength;
    }
    if (closing >= markdown.length) {
      i += delimiterLength;
      continue;
    }
    output += markdown.slice(plainStart, i);
    output += markdown.slice(i, closing + delimiterLength).replace(/[^\n]/g, ' ');
    i = closing + delimiterLength;
    plainStart = i;
  }
  return output + markdown.slice(plainStart);
}

function markdownOutsideCode(markdown) {
  const lines = markdown.match(/[^\n]*(?:\n|$)/g) ?? [];
  let output = '';
  let plain = '';
  let fence = null;

  for (const line of lines) {
    if (!line) continue;
    const lineBody = line.endsWith('\n') ? line.slice(0, -1) : line;
    if (fence) {
      output += line.replace(/[^\n]/g, ' ');
      const closing = lineBody.match(/^ {0,3}(`{3,}|~{3,})[ \t]*$/);
      if (closing && closing[1][0] === fence.character && closing[1].length >= fence.length) fence = null;
      continue;
    }
    const opening = lineBody.match(/^ {0,3}(`{3,}|~{3,})/);
    if (!opening) {
      plain += line;
      continue;
    }
    output += maskInlineCode(plain);
    plain = '';
    output += line.replace(/[^\n]/g, ' ');
    fence = { character: opening[1][0], length: opening[1].length };
  }
  return output + maskInlineCode(plain);
}

function residualMarkup(markdown) {
  return markdownOutsideCode(markdown).match(/<!--|<![A-Za-z]|<\/?[A-Za-z][\w.-]*(?:\s[^<>\n]*?)?\/?>|<>|<\/>/);
}

function projectionParts(markdown) {
  const frontmatter = markdown.match(/^---\n[\s\S]*?\n---\n\n?/);
  if (!frontmatter) return null;
  return { body: markdown.slice(frontmatter[0].length) };
}

function checksum(value) {
  return createHash('sha256').update(value).digest('hex');
}

function validateLocalProjection(root, key, document, exclusions, findings) {
  if (!document?.mirror) return;
  const read = safeRead(root, document.mirror, exclusions);
  if (read.error) {
    findings.push(read.error);
    return;
  }
  if (!read.value.includes(document.url)) {
    findings.push(finding('error', 'projection-source-drift', `Local projection for ${key} does not cite its configured Linear Document URL.`, read.relative));
  }
  if (!read.value.includes(`linear-document: ${document.id}`) || !read.value.includes('generated: true')) {
    findings.push(finding('error', 'projection-metadata-drift', `Local projection for ${key} is missing its generated/document metadata.`, read.relative));
  }
  const sourceChecksum = read.value.match(/^source-content-sha256: ([a-f0-9]{64})$/m)?.[1];
  const renderedChecksum = read.value.match(/^rendered-content-sha256: ([a-f0-9]{64})$/m)?.[1];
  const projection = projectionParts(read.value);
  if (!sourceChecksum || !renderedChecksum || !projection) {
    findings.push(finding('error', 'projection-checksum-missing', `Local projection for ${key} needs raw-source and rendered-content checksums.`, read.relative));
    return;
  }
  if (checksum(projection.body) !== renderedChecksum) {
    findings.push(finding('error', 'projection-content-drift', `Local projection for ${key} was edited after generation. Run its explicit pull command.`, read.relative));
  }
  const markup = residualMarkup(projection.body);
  if (markup) {
    findings.push(finding('error', 'projection-preview-unsafe', `Local projection for ${key} contains residual HTML/JSX outside code: ${markup[0]}.`, read.relative));
  }
}

function validateLinearProjectionSource(root, key, document, linearDocument, exclusions, findings) {
  if (!document?.mirror || typeof linearDocument?.title !== 'string' || typeof linearDocument?.content !== 'string') return;
  const read = safeRead(root, document.mirror, exclusions);
  if (read.error) return;
  const expected = read.value.match(/^source-content-sha256: ([a-f0-9]{64})$/m)?.[1];
  if (!expected) return;
  const sourceBody = `# ${linearDocument.title}\n\n${linearDocument.content.trim()}\n`;
  if (checksum(sourceBody) !== expected) {
    findings.push(finding('error', 'projection-source-content-drift', `Local projection for ${key} was not generated from current raw Linear content. Run its explicit pull command.`, read.relative));
  }
}

function validateVisuals(root, config, exclusions, findings) {
  if (!Object.hasOwn(config, 'visuals')) return;
  if (!Array.isArray(config.visuals)) {
    findings.push(finding('error', 'visuals-shape', 'Governance visuals must be an array.', CONFIG_PATH));
    return;
  }
  for (const [index, visual] of config.visuals.entries()) {
    const label = visual?.id || `visual[${index}]`;
    if (!visual || typeof visual !== 'object' || Array.isArray(visual)) {
      findings.push(finding('error', 'visual-shape', `${label} must be an object.`, CONFIG_PATH));
      continue;
    }
    for (const field of ['id', 'source', 'render', 'sourceSha256', 'renderSha256', 'verifiedAt']) {
      if (typeof visual[field] !== 'string' || !visual[field].trim()) {
        findings.push(finding('error', `visual-${field}-missing`, `${label} needs non-empty ${field}.`, CONFIG_PATH));
      }
    }
    for (const [kind, pathField, hashField] of [
      ['source', 'source', 'sourceSha256'],
      ['render', 'render', 'renderSha256'],
    ]) {
      if (typeof visual[pathField] !== 'string' || !visual[pathField] || typeof visual[hashField] !== 'string') continue;
      const read = safeRead(root, visual[pathField], exclusions, null);
      if (read.error) {
        findings.push(read.error);
        continue;
      }
      if (!/^[a-f0-9]{64}$/i.test(visual[hashField]) || checksum(read.value) !== visual[hashField].toLowerCase()) {
        findings.push(finding('error', `visual-${kind}-drift`, `${label} ${kind} hash differs from its manifest.`, read.relative));
      }
    }
  }
}

function containsOrdinal(text, ordinal) {
  const escaped = ordinal.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');
  return new RegExp(`(^|[^0-9A-Za-z.])${escaped}(?![0-9A-Za-z])`, 'm').test(text);
}

function validatePhaseMetadata(root, config, exclusions, findings) {
  const phase0 = config.phases?.phase0;
  if (phase0?.metadataFile) {
    const read = safeRead(root, phase0.metadataFile, exclusions);
    if (read.error) findings.push(read.error);
    else {
      const missing = [...(phase0.core ?? []), ...(phase0.amendments ?? [])]
        .filter((ordinal) => !containsOrdinal(read.value, ordinal));
      if (missing.length) {
        findings.push(finding('error', 'phase0-metadata-drift', `Phase 0 metadata is missing: ${missing.join(', ')}.`, read.relative));
      }
    }
  }

  const phase2 = config.phases?.phase2;
  if (phase2?.metadataFile) {
    const read = safeRead(root, phase2.metadataFile, exclusions);
    if (read.error) findings.push(read.error);
    else {
      const expected = Array.from({ length: phase2.count ?? 0 }, (_, index) => `2.${index + 1}`);
      const missing = expected.filter((ordinal) => !containsOrdinal(read.value, ordinal));
      if (missing.length || !read.value.includes(phase2.gateIssue)) {
        findings.push(finding(
          'error',
          'phase2-metadata-drift',
          `${missing.length ? `Missing ordinals: ${missing.join(', ')}. ` : ''}Final gate ${phase2.gateIssue} must be referenced.`,
          read.relative,
        ));
      }
    }
  }
}

function validatePackageAndScripts(root, config, exclusions, findings, runCommand) {
  const checks = config.checks;
  if (!checks || typeof checks !== 'object') return;
  const packageRead = safeRead(root, checks.packageFile, exclusions);
  if (packageRead.error) findings.push(packageRead.error);
  else {
    try {
      const packageJson = JSON.parse(packageRead.value);
      for (const [name, expected] of Object.entries(checks.requiredPackageScripts ?? {})) {
        if (packageJson.scripts?.[name] !== expected) {
          findings.push(finding('error', 'package-script-drift', `Package script ${name} must equal: ${expected}.`, packageRead.relative));
        }
      }
      for (const name of checks.forbiddenPackageScripts ?? []) {
        if (Object.hasOwn(packageJson.scripts ?? {}, name)) {
          findings.push(finding('error', 'forbidden-package-script', `Obsolete package script remains: ${name}.`, packageRead.relative));
        }
      }
    } catch (error) {
      findings.push(finding('error', 'package-json', `Invalid package JSON: ${error.message}.`, packageRead.relative));
    }
  }

  const intentionRead = safeRead(root, checks.intentionScript, exclusions);
  if (intentionRead.error) findings.push(intentionRead.error);
  else {
    const result = runCommand(process.execPath, [intentionRead.absolute], root);
    if (result.status !== 0) {
      findings.push(finding(
        'error',
        'intention-drift',
        compactOutput(result.stderr || result.stdout || result.error?.message || 'Intention checker failed.'),
        intentionRead.relative,
      ));
    }
  }

  const trackerRead = safeRead(root, checks.trackerScript, exclusions);
  if (trackerRead.error) findings.push(trackerRead.error);
  else {
    const result = runCommand(process.execPath, [trackerRead.absolute, '--json'], root);
    try {
      const report = JSON.parse(result.stdout);
      if (result.status !== 0 || report.mode !== 'report' || report.linearWrites !== false) {
        findings.push(finding('error', 'tracker-default-unsafe', 'Tracker default must be a read-only report with Linear writes disabled.', trackerRead.relative));
      }
    } catch {
      findings.push(finding('error', 'tracker-report-invalid', 'Tracker default did not return its JSON safety report.', trackerRead.relative));
    }
  }
}

function canonicalSkillPath(root, name) {
  const claude = join(root, '.claude', 'skills', name);
  const agents = join(root, '.agents', 'skills', name);
  const claudeStat = safeLstat(claude);
  const agentsStat = safeLstat(agents);
  if (claudeStat && !claudeStat.isSymbolicLink()) return safeRealpath(claude);
  if (agentsStat && !agentsStat.isSymbolicLink()) return safeRealpath(agents);
  return safeRealpath(claude) ?? safeRealpath(agents);
}

function validateSymlink(link, expected) {
  const stat = safeLstat(link);
  return Boolean(stat?.isSymbolicLink() && safeRealpath(link) === expected);
}

function validateAdk(root, config, exclusions, findings) {
  const skillNames = new Set();
  for (const base of ['.claude/skills', '.agents/skills']) {
    for (const entry of directoryEntries(root, base)) {
      if (!entry.name.startsWith('.') && (entry.isDirectory() || entry.isSymbolicLink())) skillNames.add(entry.name);
    }
  }
  const drift = [];
  for (const name of [...skillNames].sort()) {
    const canonical = canonicalSkillPath(root, name);
    if (!canonical) {
      drift.push(`broken canonical skill ${name}`);
      continue;
    }
    for (const runtime of ['.cursor', '.codex']) {
      const mirror = join(root, runtime, 'skills', name);
      if (!validateSymlink(mirror, canonical)) drift.push(`${runtime}/skills/${name}`);
    }
  }

  for (const entry of directoryEntries(root, '.claude/commands')) {
    if (!entry.isFile() || extname(entry.name) !== '.md') continue;
    const canonical = safeRealpath(join(root, '.claude', 'commands', entry.name));
    for (const runtime of ['.cursor', '.codex']) {
      const mirror = join(root, runtime, 'commands', entry.name);
      if (!validateSymlink(mirror, canonical)) drift.push(`${runtime}/commands/${entry.name}`);
    }
  }

  if (drift.length) {
    findings.push(finding(
      'error',
      'adk-drift',
      `${drift.length} ADK mirror(s) drift. ${drift.slice(0, 12).join(', ')}${drift.length > 12 ? ', …' : ''}`,
      '.claude/skills',
    ));
  }

  if (!config.checks?.skillIndex) return;
  const indexRead = safeRead(root, config.checks.skillIndex, exclusions);
  if (indexRead.error) findings.push(indexRead.error);
  else if (!indexRead.value.includes('govern-agentic-os')) {
    findings.push(finding('error', 'skill-index-drift', 'Skill index does not include govern-agentic-os.', indexRead.relative));
  }
}

export async function runCheck(options, dependencies = {}) {
  const root = resolve(options.root ?? defaultRoot());
  const findings = [];
  const mode = options.mode ?? 'local';
  const runCommand = dependencies.runCommand ?? defaultRunCommand;

  for (const path of SKILL_FILES) {
    const read = safeRead(root, path);
    if (read.error) findings.push(read.error);
  }

  let config;
  const configRead = safeRead(root, CONFIG_PATH);
  if (configRead.error?.code === 'missing-path') {
    findings.push(finding(mode === 'live' ? 'precondition' : 'warning', 'config-pending', 'Governance config is not installed yet.', CONFIG_PATH));
  } else if (configRead.error) {
    findings.push(configRead.error);
  } else {
    try {
      config = JSON.parse(configRead.value);
      validateConfig(config, findings);
      const exclusions = Array.isArray(config.audit?.excludedRoots) ? config.audit.excludedRoots : REQUIRED_EXCLUSIONS;
      for (const [key, document] of Object.entries(config.linear?.documents ?? {})) {
        validateLocalProjection(root, key, document, exclusions, findings);
      }
      validateVisuals(root, config, exclusions, findings);
      validatePhaseMetadata(root, config, exclusions, findings);
      validatePackageAndScripts(root, config, exclusions, findings, runCommand);
      validateAdk(root, config, exclusions, findings);
    } catch (error) {
      findings.push(finding('error', 'config-json', `Invalid JSON: ${error.message}`, CONFIG_PATH));
    }
  }

  if (mode === 'live' && config) {
    const apiKey = dependencies.apiKey ?? process.env.LINEAR_API_KEY;
    const fetchImpl = dependencies.fetchImpl ?? globalThis.fetch;
    if (!apiKey) {
      findings.push(finding('precondition', 'linear-auth', 'LINEAR_API_KEY is required for --live; no secret file is read automatically.'));
    } else if (typeof fetchImpl !== 'function') {
      findings.push(finding('precondition', 'fetch-unavailable', 'A fetch implementation is required for --live.'));
    } else {
      for (const [key, document] of Object.entries(config.linear?.documents ?? {})) {
        if (!document.id) continue;
        try {
          const response = await fetchImpl('https://api.linear.app/graphql', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json', Authorization: apiKey },
            body: JSON.stringify({
              query: 'query($id:String!){document(id:$id){id title content url updatedAt}}',
              variables: { id: document.id },
            }),
          });
          if (!response.ok) {
            findings.push(finding('precondition', 'linear-http', `Linear returned HTTP ${response.status} for ${key}.`));
            continue;
          }
          const payload = await response.json();
          if (payload.errors?.length) {
            findings.push(finding('precondition', 'linear-graphql', `Linear query failed for ${key}: ${payload.errors[0].message ?? 'unknown error'}.`));
          } else if (!payload.data?.document) {
            findings.push(finding('error', 'linear-document-missing', `Canonical Linear Document is missing or inaccessible: ${key}.`));
          } else {
            if (payload.data.document.url !== document.url) {
              findings.push(finding('error', 'linear-document-url-drift', `Configured URL differs from Linear for ${key}.`, CONFIG_PATH));
            }
            const exclusions = Array.isArray(config.audit?.excludedRoots) ? config.audit.excludedRoots : REQUIRED_EXCLUSIONS;
            validateLinearProjectionSource(root, key, document, payload.data.document, exclusions, findings);
          }
        } catch (error) {
          findings.push(finding('precondition', 'linear-network', `Linear request failed for ${key}: ${error.message}.`));
        }
      }
    }
    findings.push(finding(
      'warning',
      'runtime-tooling-check-manual',
      'Runtime tooling drift remains an explicit `npm run tooling:check`; it reads user-home runtime configs and is outside this checker\'s privacy boundary.',
    ));
  }

  const hasPrecondition = findings.some((item) => item.level === 'precondition');
  const hasError = findings.some((item) => item.level === 'error');
  const exitCode = hasPrecondition ? 2 : hasError ? 1 : 0;
  return { ok: exitCode === 0, mode, root, exitCode, findings };
}

export function formatHuman(result) {
  const lines = [`Agentic OS check (${result.mode})`];
  for (const item of result.findings) {
    const mark = item.level === 'error' ? 'ERROR' : item.level === 'precondition' ? 'BLOCKED' : item.level.toUpperCase();
    lines.push(`[${mark}] ${item.code}${item.path ? ` (${item.path})` : ''}: ${item.message}`);
  }
  if (result.findings.length === 0) lines.push('[OK] No drift detected.');
  lines.push(`Exit ${result.exitCode}`);
  return lines.join('\n');
}

export function formatSessionStart(result) {
  if (!result.findings.length) return '';
  const details = result.findings
    .slice(0, 10)
    .map((item) => `- ${item.code}${item.path ? ` (${item.path})` : ''}: ${item.message}`)
    .join('\n');
  const suffix = result.findings.length > 10 ? `\n- … ${result.findings.length - 10} additional finding(s)` : '';
  return JSON.stringify({
    hookSpecificOutput: {
      hookEventName: 'SessionStart',
      additionalContext: `\n\n# Agentic OS coherence warning\n\nRead-only check exit: ${result.exitCode}. No fixes or pulls were applied.\n${details}${suffix}\n`,
    },
  });
}

function printHelp() {
  return [
    'Usage: check.mjs [--local|--live] [--json] [--session-start] [--root PATH]',
    '',
    '--local  Check declared local artifacts only (default).',
    '--live   Add read-only Linear Document reachability checks.',
    '--json   Emit one JSON object.',
    '--session-start  Emit Claude hook context and always exit zero.',
    '--root   Override repository root (intended for tests/fixtures).',
  ].join('\n');
}

async function main() {
  let options;
  try {
    options = parseArgs(process.argv.slice(2));
  } catch (error) {
    console.error(error.message);
    console.error(printHelp());
    process.exitCode = 2;
    return;
  }
  if (options.help) {
    console.log(printHelp());
    return;
  }
  try {
    const result = await runCheck(options);
    if (options.sessionStart) {
      const output = formatSessionStart(result);
      if (output) console.log(output);
      process.exitCode = 0;
      return;
    }
    console.log(options.json ? JSON.stringify(result, null, 2) : formatHuman(result));
    process.exitCode = result.exitCode;
  } catch (error) {
    if (options.sessionStart) {
      console.log(JSON.stringify({
        hookSpecificOutput: {
          hookEventName: 'SessionStart',
          additionalContext: `\n\n# Agentic OS coherence warning\n\nRead-only check could not run: ${error.message}. No fixes or pulls were applied.\n`,
        },
      }));
      process.exitCode = 0;
      return;
    }
    console.error(`Agentic OS check failed: ${error.message}`);
    process.exitCode = 2;
  }
}

if (resolve(process.argv[1] ?? '') === resolve(fileURLToPath(import.meta.url))) await main();
