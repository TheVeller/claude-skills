import assert from 'node:assert/strict';
import { createHash } from 'node:crypto';
import { afterEach, test } from 'node:test';
import { mkdtemp, mkdir, readFile, rm, symlink, unlink, writeFile } from 'node:fs/promises';
import { join, relative } from 'node:path';
import { tmpdir } from 'node:os';

import { formatSessionStart, parseArgs, runCheck } from './check.mjs';

const roots = [];

async function fixture({ config, mirror } = {}) {
  const root = await mkdtemp(join(tmpdir(), 'govern-agentic-os-'));
  roots.push(root);
  const skillFiles = [
    'SKILL.md',
    'agents/openai.yaml',
    'references/governance-contract.md',
    'references/audit-protocol.md',
    'scripts/check.mjs',
    'scripts/check.test.mjs',
  ];
  for (const path of skillFiles) {
    const absolute = join(root, '.claude/skills/govern-agentic-os', path);
    await mkdir(join(absolute, '..'), { recursive: true });
    await writeFile(absolute, `fixture ${path}\n`);
  }
  const canonicalSkill = join(root, '.claude/skills/govern-agentic-os');
  for (const runtime of ['.cursor', '.codex']) {
    const mirror = join(root, runtime, 'skills/govern-agentic-os');
    await mkdir(join(mirror, '..'), { recursive: true });
    await symlink(canonicalSkill, mirror, 'dir');
  }
  if (config) {
    await mkdir(join(root, '.config'), { recursive: true });
    await writeFile(join(root, '.config/agentic-os-governance.json'), JSON.stringify(config));
    await writeFile(join(root, 'package.json'), JSON.stringify({ scripts: config.checks.requiredPackageScripts }));
    const intention = join(root, config.checks.intentionScript);
    await mkdir(join(intention, '..'), { recursive: true });
    await writeFile(intention, 'process.exit(0);\n');
    const tracker = join(root, config.checks.trackerScript);
    await mkdir(join(tracker, '..'), { recursive: true });
    await writeFile(tracker, 'console.log(JSON.stringify({mode:"report",linearWrites:false}));\n');
    const index = join(root, config.checks.skillIndex);
    await mkdir(join(index, '..'), { recursive: true });
    await writeFile(index, '# Skills\n- govern-agentic-os\n');
    const phase0 = join(root, config.phases.phase0.metadataFile);
    await mkdir(join(phase0, '..'), { recursive: true });
    await writeFile(phase0, [...config.phases.phase0.core, ...config.phases.phase0.amendments].join('\n'));
    const phase2 = join(root, config.phases.phase2.metadataFile);
    await mkdir(join(phase2, '..'), { recursive: true });
    await writeFile(
      phase2,
      `${Array.from({ length: config.phases.phase2.count }, (_, index) => `2.${index + 1}`).join('\n')}\n${config.phases.phase2.gateIssue}\n`,
    );
  }
  if (mirror) {
    const absolute = join(root, mirror.path);
    await mkdir(join(absolute, '..'), { recursive: true });
    await writeFile(absolute, mirror.content);
  }
  return root;
}

function validConfig(local) {
  const document = (key) => ({
    id: `doc-${key}`,
    url: `https://linear.example/document/${key}`,
    anchorIssue: `MAK-${key}`,
    ...(local && key === 'architecture' ? { mirror: local.path } : {}),
  });
  return {
    schemaVersion: 1,
    canonicalLanguage: 'es',
    ossTargetLanguage: 'en',
    linear: {
      documents: {
        architecture: document('architecture'),
        governance: document('governance'),
        tooling: document('tooling'),
        data: document('data'),
      },
    },
    phases: {
      phase0: {
        core: ['0.1', '0.2', '0.3', '0.4', '0.5', '0.6', '0.7', '0.8', '0.9', '0.10'],
        amendments: ['0.1a', '0.4b'],
        metadataFile: '02_Programs/0-Projects/Agentic OS Setup/FASE-0.md',
      },
      phase2: {
        count: 25,
        first: '2.1',
        last: '2.25',
        gateIssue: 'ABC-123',
        metadataFile: '02_Programs/0-Projects/Agentic OS Setup/PHASE-ORDER.md',
      },
    },
    checks: {
      packageFile: 'package.json',
      requiredPackageScripts: {
        'agentic-os:check': 'node .claude/skills/govern-agentic-os/scripts/check.mjs',
        'test:agentic-os': 'node --test .claude/skills/govern-agentic-os/scripts/check.test.mjs',
      },
      forbiddenPackageScripts: ['linear:enrich-agentic-os'],
      intentionScript: '06_Metadata/scripts/check-intentions-map.mjs',
      trackerScript: '.scripts/sync-agentic-os-trackers.js',
      skillIndex: '06_Metadata/Skills/_INDEX.md',
    },
    audit: { excludedRoots: ['01_Journal', '03_Areas', '04_Resources'] },
  };
}

function generatedMirror(config, body, sourceBody = body) {
  return `---
linear-document: ${config.linear.documents.architecture.id}
source: ${config.linear.documents.architecture.url}
source-content-sha256: ${createHash('sha256').update(sourceBody).digest('hex')}
rendered-content-sha256: ${createHash('sha256').update(body).digest('hex')}
generated: true
---

${body}`;
}

afterEach(async () => {
  while (roots.length) {
    const root = roots.pop();
    assert.equal(relative(tmpdir(), root).startsWith('govern-agentic-os-'), true);
    await rm(root, { recursive: true, force: true });
  }
});

test('parseArgs defaults to local and supports JSON/root', () => {
  const options = parseArgs(['--json', '--root', '/tmp/example']);
  assert.equal(options.mode, 'local');
  assert.equal(options.json, true);
  assert.equal(options.root, '/tmp/example');
  assert.throws(() => parseArgs(['--unknown']), /unknown option/);
  assert.equal(parseArgs(['--session-start']).sessionStart, true);
});

test('local mode treats pending governance config as a warning', async () => {
  const root = await fixture();
  const result = await runCheck({ mode: 'local', root });
  assert.equal(result.exitCode, 0);
  assert.equal(result.findings.some((item) => item.code === 'config-pending' && item.level === 'warning'), true);
});

test('local mode accepts a generated mirror that cites its source', async () => {
  const path = '02_Programs/0-Projects/Agentic OS Setup/ARCHITECTURE.md';
  const config = validConfig({ mode: 'generated-mirror', path });
  const body = '# Architecture\n\nFixture body.\n';
  const root = await fixture({
    config,
    mirror: {
      path,
      content: generatedMirror(config, body),
    },
  });
  const result = await runCheck({ mode: 'local', root });
  assert.equal(result.exitCode, 0, JSON.stringify(result.findings));
});

test('local mode detects mirror and canonical-copy drift', async () => {
  const path = '02_Programs/0-Projects/Agentic OS Setup/ARCHITECTURE.md';
  const config = validConfig({ mode: 'generated-mirror', path });
  config.linear.documents.architecture.body = 'copied canon';
  const root = await fixture({ config, mirror: { path, content: 'manual mirror\n' } });
  const result = await runCheck({ mode: 'local', root });
  assert.equal(result.exitCode, 1);
  assert.equal(result.findings.some((item) => item.code === 'canonical-copy'), true);
  assert.equal(result.findings.some((item) => item.code === 'projection-source-drift'), true);
});

test('local mode detects edits to a generated mirror payload', async () => {
  const path = '02_Programs/0-Projects/Agentic OS Setup/ARCHITECTURE.md';
  const config = validConfig({ mode: 'generated-mirror', path });
  const body = '# Architecture\n\nFixture body.\n';
  const root = await fixture({
    config,
    mirror: {
      path,
      content: `${generatedMirror(config, body)}manual edit\n`,
    },
  });
  const result = await runCheck({ mode: 'local', root });
  assert.equal(result.exitCode, 1);
  assert.equal(result.findings.some((item) => item.code === 'projection-content-drift'), true);
});

test('local mode rejects residual HTML/JSX but ignores code examples', async () => {
  const path = '02_Programs/0-Projects/Agentic OS Setup/ARCHITECTURE.md';
  const unsafeConfig = validConfig({ mode: 'generated-mirror', path });
  const unsafeBody = '# Architecture\n\n<div>Unsafe</div>\n<Component value={1} />\n';
  const unsafeRoot = await fixture({
    config: unsafeConfig,
    mirror: { path, content: generatedMirror(unsafeConfig, unsafeBody) },
  });
  const unsafe = await runCheck({ mode: 'local', root: unsafeRoot });
  assert.equal(unsafe.exitCode, 1);
  assert.equal(unsafe.findings.some((item) => item.code === 'projection-preview-unsafe'), true);

  const safeConfig = validConfig({ mode: 'generated-mirror', path });
  const safeBody = '# Architecture\n\n`<Component />`\n\n```html\n<div>Example</div>\n```\n';
  const safeRoot = await fixture({
    config: safeConfig,
    mirror: { path, content: generatedMirror(safeConfig, safeBody) },
  });
  const safe = await runCheck({ mode: 'local', root: safeRoot });
  assert.equal(safe.exitCode, 0, JSON.stringify(safe.findings));
});

test('local mode refuses excluded and secret-like declared paths', async () => {
  const config = validConfig({ mode: 'operational-projection', path: '01_Journal/private.md' });
  config.linear.documents.tooling.mirror = '.env.local';
  const root = await fixture({ config });
  const result = await runCheck({ mode: 'local', root });
  assert.equal(result.exitCode, 1);
  assert.equal(result.findings.some((item) => item.code === 'excluded-path'), true);
  assert.equal(result.findings.some((item) => item.code === 'sensitive-path'), true);
});

test('live mode returns precondition 2 without config or auth', async () => {
  const root = await fixture();
  const result = await runCheck({ mode: 'live', root }, { apiKey: '' });
  assert.equal(result.exitCode, 2);
  assert.equal(result.findings.some((item) => item.code === 'config-pending'), true);
});

test('live mode checks documents through an injected read-only transport', async () => {
  const config = validConfig();
  const root = await fixture({ config });
  const requested = [];
  const fetchImpl = async (_url, request) => {
    const body = JSON.parse(request.body);
    requested.push(body.variables.id);
    const key = body.variables.id.replace(/^doc-/, '');
    return {
      ok: true,
      status: 200,
      json: async () => ({
        data: {
          document: {
            id: body.variables.id,
            title: key,
            content: 'Canonical content.',
            url: `https://linear.example/document/${key}`,
            updatedAt: '2026-08-03T00:00:00.000Z',
          },
        },
      }),
    };
  };
  const result = await runCheck({ mode: 'live', root }, { apiKey: 'test-only', fetchImpl });
  assert.equal(result.exitCode, 0, JSON.stringify(result.findings));
  assert.equal(requested.length, 4);
});

test('live mode verifies raw Linear source independently from rendered mirror bytes', async () => {
  const path = '02_Programs/0-Projects/Agentic OS Setup/ARCHITECTURE.md';
  const config = validConfig({ mode: 'generated-mirror', path });
  const sourceBody = '# Architecture\n\n[Canon](<https://linear.example/document/canon>)\n';
  const renderedBody = '# Architecture\n\n[Canon](https://linear.example/document/canon)\n';
  const root = await fixture({
    config,
    mirror: { path, content: generatedMirror(config, renderedBody, sourceBody) },
  });
  let changed = false;
  const fetchImpl = async (_url, request) => {
    const { variables } = JSON.parse(request.body);
    const key = variables.id.replace(/^doc-/, '');
    return {
      ok: true,
      status: 200,
      json: async () => ({
        data: {
          document: {
            id: variables.id,
            title: key === 'architecture' ? 'Architecture' : key,
            content: key === 'architecture'
              ? changed ? 'Changed canonical content.' : '[Canon](<https://linear.example/document/canon>)'
              : 'Canonical content.',
            url: `https://linear.example/document/${key}`,
            updatedAt: '2026-08-04T00:00:00.000Z',
          },
        },
      }),
    };
  };

  const current = await runCheck({ mode: 'live', root }, { apiKey: 'test-only', fetchImpl });
  assert.equal(current.exitCode, 0, JSON.stringify(current.findings));
  changed = true;
  const drift = await runCheck({ mode: 'live', root }, { apiKey: 'test-only', fetchImpl });
  assert.equal(drift.exitCode, 1);
  assert.equal(drift.findings.some((item) => item.code === 'projection-source-content-drift'), true);
});

test('live mode reports a missing canonical document as drift', async () => {
  const root = await fixture({ config: validConfig() });
  const fetchImpl = async () => ({
    ok: true,
    status: 200,
    json: async () => ({ data: { document: null } }),
  });
  const result = await runCheck({ mode: 'live', root }, { apiKey: 'test-only', fetchImpl });
  assert.equal(result.exitCode, 1);
  assert.equal(result.findings.some((item) => item.code === 'linear-document-missing'), true);
});

test('local mode detects intention and ADK drift without network', async () => {
  const config = validConfig();
  const root = await fixture({ config });
  await writeFile(join(root, config.checks.intentionScript), 'process.exit(1);\n');
  await unlink(join(root, '.cursor/skills/govern-agentic-os'));
  let fetched = false;
  const result = await runCheck(
    { mode: 'local', root },
    { fetchImpl: async () => { fetched = true; throw new Error('must not fetch'); } },
  );
  assert.equal(result.exitCode, 1);
  assert.equal(fetched, false);
  assert.equal(result.findings.some((item) => item.code === 'intention-drift'), true);
  assert.equal(result.findings.some((item) => item.code === 'adk-drift'), true);
});

test('optional visual manifest verifies source, render, hashes and verifiedAt', async () => {
  const config = validConfig();
  const source = '06_Metadata/Visual/architecture.excalidraw';
  const render = '06_Metadata/Visual/architecture.png';
  const sourceBytes = Buffer.from('{"type":"excalidraw"}\n');
  const renderBytes = Buffer.from([0x89, 0x50, 0x4e, 0x47]);
  config.visuals = [{
    id: 'architecture',
    source,
    render,
    sourceSha256: createHash('sha256').update(sourceBytes).digest('hex'),
    renderSha256: createHash('sha256').update(renderBytes).digest('hex'),
    verifiedAt: '2026-08-04',
  }];
  const root = await fixture({ config });
  await mkdir(join(root, source, '..'), { recursive: true });
  await writeFile(join(root, source), sourceBytes);
  await writeFile(join(root, render), renderBytes);

  const current = await runCheck({ mode: 'local', root });
  assert.equal(current.exitCode, 0, JSON.stringify(current.findings));
  await writeFile(join(root, render), Buffer.from('stale render'));
  config.visuals[0].verifiedAt = '';
  await writeFile(join(root, '.config/agentic-os-governance.json'), JSON.stringify(config));
  const drift = await runCheck({ mode: 'local', root });
  assert.equal(drift.exitCode, 1);
  assert.equal(drift.findings.some((item) => item.code === 'visual-render-drift'), true);
  assert.equal(drift.findings.some((item) => item.code === 'visual-verifiedAt-missing'), true);
});

test('session-start output is warning-only hook context', () => {
  const output = formatSessionStart({
    exitCode: 1,
    findings: [{ level: 'error', code: 'example-drift', message: 'Example.', path: 'package.json' }],
  });
  const payload = JSON.parse(output);
  assert.equal(payload.hookSpecificOutput.hookEventName, 'SessionStart');
  assert.match(payload.hookSpecificOutput.additionalContext, /No fixes or pulls were applied/);
});

test('local mode detects phase metadata drift', async () => {
  const config = validConfig();
  const root = await fixture({ config });
  await writeFile(join(root, config.phases.phase2.metadataFile), '2.1\nABC-123\n');
  const result = await runCheck({ mode: 'local', root });
  assert.equal(result.exitCode, 1);
  assert.equal(result.findings.some((item) => item.code === 'phase2-metadata-drift'), true);
});

test('local mode does not mutate declared artifacts', async () => {
  const config = validConfig();
  const root = await fixture({ config });
  const packagePath = join(root, config.checks.packageFile);
  const before = await readFile(packagePath, 'utf8');
  const result = await runCheck({ mode: 'local', root });
  const after = await readFile(packagePath, 'utf8');
  assert.equal(result.exitCode, 0, JSON.stringify(result.findings));
  assert.equal(after, before);
});
