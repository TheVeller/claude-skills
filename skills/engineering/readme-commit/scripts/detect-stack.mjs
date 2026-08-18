#!/usr/bin/env node
/**
 * detect-stack.mjs — read package.json (and light hints) → print stack for README Tech Stack.
 * Usage: node detect-stack.mjs [path/to/package.json|project-dir]
 * No network. Exit 0 always when package.json found; exit 2 on usage/missing.
 */
import { readFileSync, existsSync, readdirSync } from "node:fs";
import { dirname, join, resolve } from "node:path";

const arg = process.argv[2] || ".";
let pkgPath = resolve(arg);
if (existsSync(pkgPath) && !pkgPath.endsWith("package.json")) {
  pkgPath = join(pkgPath, "package.json");
}
if (!existsSync(pkgPath)) {
  console.error(`No package.json at ${pkgPath}`);
  process.exit(2);
}

const pkg = JSON.parse(readFileSync(pkgPath, "utf8"));
const deps = { ...pkg.dependencies, ...pkg.devDependencies };
const names = Object.keys(deps);

const rules = [
  { id: "React", test: (n) => n === "react", layer: "Frontend", badge: "React" },
  { id: "Next.js", test: (n) => n === "next", layer: "Frontend", badge: "Next.js" },
  { id: "Vue", test: (n) => n === "vue", layer: "Frontend", badge: "Vue" },
  { id: "Svelte", test: (n) => n === "svelte" || n.startsWith("@sveltejs/"), layer: "Frontend", badge: "Svelte" },
  { id: "TypeScript", test: (n) => n === "typescript", layer: "Frontend", badge: "TypeScript" },
  { id: "Vite", test: (n) => n === "vite", layer: "Frontend", badge: "Vite" },
  { id: "Tailwind CSS", test: (n) => n === "tailwindcss", layer: "Frontend", badge: "Tailwind_CSS" },
  { id: "shadcn/ui", test: (n) => n.includes("shadcn"), layer: "Frontend", badge: "shadcn/ui" },
  { id: "TanStack Start", test: (n) => n.startsWith("@tanstack/react-start") || n === "@tanstack/start", layer: "Frontend", badge: "TanStack" },
  { id: "TanStack Query", test: (n) => n.includes("react-query") || n === "@tanstack/react-query", layer: "State", badge: "TanStack_Query" },
  { id: "Clerk", test: (n) => n.startsWith("@clerk/"), layer: "Auth", badge: "Clerk" },
  { id: "Supabase", test: (n) => n.startsWith("@supabase/"), layer: "Backend", badge: "Supabase" },
  { id: "Prisma", test: (n) => n === "prisma" || n === "@prisma/client", layer: "Backend", badge: "Prisma" },
  { id: "Drizzle", test: (n) => n.startsWith("drizzle-"), layer: "Backend", badge: "Drizzle" },
  { id: "Express", test: (n) => n === "express", layer: "Backend", badge: "Express" },
  { id: "Hono", test: (n) => n === "hono", layer: "Backend", badge: "Hono" },
  { id: "Bun", test: (n) => n === "bun" || n === "bun:test", layer: "Runtime", badge: "Bun" },
];

const found = [];
const seen = new Set();
for (const rule of rules) {
  if (names.some(rule.test) && !seen.has(rule.id)) {
    seen.add(rule.id);
    found.push(rule);
  }
}

const root = dirname(pkgPath);
const engines = pkg.engines || {};
const requirements = [];
if (engines.node) requirements.push(`Node ${engines.node}`);
if (engines.bun) requirements.push(`Bun ${engines.bun}`);
if (existsSync(join(root, "bun.lockb")) || existsSync(join(root, "bun.lock"))) {
  if (!requirements.some((r) => r.startsWith("Bun"))) requirements.push("Bun");
}
if (existsSync(join(root, "supabase"))) requirements.push("Supabase project / CLI");

const byLayer = {};
for (const f of found) {
  (byLayer[f.layer] ||= []).push(f.id);
}

const out = {
  name: pkg.name || null,
  packageManager: existsSync(join(root, "bun.lockb")) || existsSync(join(root, "bun.lock"))
    ? "bun"
    : existsSync(join(root, "pnpm-lock.yaml"))
      ? "pnpm"
      : existsSync(join(root, "yarn.lock"))
        ? "yarn"
        : "npm",
  badges: found.map((f) => f.badge),
  layers: byLayer,
  requirements,
  scripts: Object.keys(pkg.scripts || {}),
};

// Human-readable for agents
console.log(JSON.stringify(out, null, 2));
console.log("\n--- badges (for-the-badge labels) ---");
for (const b of out.badges) console.log(b);
console.log("\n--- Layer | Technology ---");
for (const [layer, techs] of Object.entries(byLayer)) {
  console.log(`${layer}\t${techs.join(", ")}`);
}
if (requirements.length) {
  console.log("\n--- Requirements ---");
  for (const r of requirements) console.log(r);
}
