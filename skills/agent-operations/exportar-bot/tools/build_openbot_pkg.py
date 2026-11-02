#!/usr/bin/env python3
"""Arma un paquete de tenant de OpenBot (CopilotKit/openbot) desde bots Grok, en modo dry-run.

Uso:
  python3 build_openbot_pkg.py --scope bot     --target <agent-id>
  python3 build_openbot_pkg.py --scope dept    --target Forja [--include-ambiguous]
  python3 build_openbot_pkg.py --scope account
Opciones: --out DIR (default /workspace/exports/openbot-<target>), --dumps DIR (memorias volcadas),
          --no-memory-in-prompt, --include-workspace-files, --zip/--no-zip.

Solo lee: profile.json, group.json, automations/*/automation.json, memory/*.md (filtrando
[episode]/[note]), /home/box/agent-data/workflows/*/SKILL.md y volcados memory.md.
NUNCA lee box-secrets.json, host-secrets.json, connector-secrets/, cookies, store.db ni Bitwarden.
No envía mensajes, no cambia nada fuera de --out.
Formato verificado contra github.com/CopilotKit/openbot (docs/configuration.md "Tenant package",
server/src/tenant-package.ts). Routines y memorias NO se pueden sembrar por paquete: van como
ROUTINES.md / routines.json y archivos de memoria para cargar a mano.
"""
import argparse, json, re, sys, unicodedata, zipfile, glob, os
from pathlib import Path

try:
    import yaml
except ImportError:
    sys.exit("Falta PyYAML: pip install --user pyyaml")

AGENTS = Path("/home/box/agent-data/agents")
WORKFLOWS = Path("/home/box/agent-data/workflows")
EXPORTS = Path("/workspace/exports")
DENY = re.compile(r"(box-secrets|host-secrets|connector-secrets|cookie|bitwarden|\.db$|\.db-|secret)", re.I)
RESERVED_IDS = {"policy", "fleet", "policy-dry-run"}          # server/src/computer/deployment-routes.ts
SLUG_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,38}[a-z0-9]$")      # tenant-package.ts (skills)
ROLE_MAX = 1000                                                # server/src/agents/routes.ts
ORQ_ID = "144e56d8-343c-4be2-9dd5-a764b44a2c88"
GMS = {"forja": "Forja", "brandy": "Brandy", "levy": "Levy", "inti": "Inti", "oppy": "Oppy"}
SECRET_RE = re.compile(r"(sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|xox[bpa]-[A-Za-z0-9-]{10,}|AKIA[0-9A-Z]{16}|"
                       r"ntn_[A-Za-z0-9]{20,}|secret_[A-Za-z0-9]{20,}|eyJ[A-Za-z0-9_-]{30,}\.[A-Za-z0-9_-]+|"
                       r"(?i:password|contraseña|api[_-]?key|token)\s*[:=]\s*\S{6,}|\+\d{9,13}\b)")

PERSONAL_MAIL = re.compile(r"[A-Za-z0-9._%+-]+@(?:gmail|googlemail|hotmail|outlook|live|yahoo|icloud|proton(?:mail)?)\.[a-z.]{2,}", re.I)
REDACTED = {}
class Lit(str): pass
yaml.add_representer(Lit, lambda d, v: d.represent_scalar("tag:yaml.org,2002:str", v, style="|"))

def safe_read(p: Path) -> str:
    if DENY.search(str(p)):
        raise RuntimeError(f"ruta prohibida: {p}")
    return p.read_text(encoding="utf-8", errors="replace")

def slugify(s, maxlen=40):
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:maxlen].strip("-")
    return s or "x"

def clean(text):  # quita espacios finales para que YAML use bloque literal
    return "\n".join(l.rstrip() for l in text.strip().splitlines()) + "\n"

def load_all():
    bots, rooms = {}, {}
    for d in sorted(AGENTS.iterdir()):
        pj = d / "profile.json"
        if not pj.exists():
            continue
        prof = json.loads(safe_read(pj))
        if (d / "group.json").exists():
            rooms[d.name] = {"name": prof.get("name", d.name),
                             "members": json.loads(safe_read(d / "group.json")).get("memberIds", [])}
        else:
            bots[d.name] = prof
    return bots, rooms

def find_gm(bots, dept):
    want = GMS.get(dept.lower(), dept)
    for i, p in bots.items():
        if p.get("name", "").strip().lower() == want.lower():
            return i
    sys.exit(f"No encuentro al GM '{dept}'")

def dept_members(bots, rooms, gm_id):
    gm = bots[gm_id]["name"]
    pat = re.compile(rf"(bajo\s+{gm}\b|→\s*{gm}\b|->\s*{gm}\b|reporta\s+a\s+{gm}\b)", re.I)
    by_desc = {i for i, p in bots.items() if i != gm_id and pat.search(p.get("description") or "")}
    room_ids = [r for r, v in rooms.items() if gm_id in v["members"] and not
                any(g in v["members"] for g in (set(find_all_gms(bots)) - {gm_id}))]
    in_room = {m for r in room_ids for m in rooms[r]["members"]} - {gm_id, ORQ_ID}
    ambiguous = {}
    for m in in_room - by_desc:
        d = bots.get(m, {}).get("description", "")
        ambiguous[m] = "en la sala del GM, pero la descripción no lo pone bajo el GM" + \
                       (" (dice Orquestador)" if re.search(r"orquestador", d, re.I) else "")
    return by_desc, ambiguous, room_ids

def find_all_gms(bots):
    names = {v.lower() for v in GMS.values()}
    return [i for i, p in bots.items() if p.get("name", "").lower() in names]

def skills_index():
    idx = {}
    for d in sorted(WORKFLOWS.iterdir()):
        f = d / "SKILL.md"
        if not f.exists():
            continue
        txt = safe_read(f)
        m = re.search(r"^name:\s*(.+)$", txt, re.M)
        name = m.group(1).strip().strip("'\"") if m else d.name
        dm = re.search(r"^description:\s*>?-?\s*\n?((?:\s{2,}.+\n?)+|.+)$", txt, re.M)
        summary = " ".join((dm.group(1) if dm else name).split())[:300]
        idx[d.name] = {"name": name, "summary": summary, "text": txt}
    return idx

def referenced_skills(text, idx):
    found = set()
    low = text.lower()
    for slug, s in idx.items():
        if (len(slug) >= 5 or "-" in slug) and re.search(rf"(?<![a-z0-9-]){re.escape(slug)}(?![a-z0-9-])", low) or \
           (len(s["name"]) > 4 and s["name"].lower() in low):
            found.add(slug)
    return found

def portable_memory(agent_id, dumps_dirs):
    parts, sources = [], []
    for dd in dumps_dirs:
        for cand in (dd / agent_id / "memory.md", dd / f"{agent_id}.md"):
            if cand.exists():
                parts.append(safe_read(cand)); sources.append(str(cand))
    mdir = AGENTS / agent_id / "memory"
    for f in [mdir / "profile.md", *sorted((mdir / "log").glob("*.md"))] if mdir.exists() else []:
        if f.exists():
            parts.append(safe_read(f)); sources.append(str(f))
    lines = [l for p in parts for l in p.splitlines()
             if not re.search(r"\[(episode|note)\]", l, re.I) and not l.strip().startswith("<!--")]
    text = "\n".join(lines).strip()
    text, n = PERSONAL_MAIL.subn("[email personal redactado]", text)
    REDACTED[agent_id] = n
    return text, sources

def routines_of(agent_id):
    out = []
    for f in sorted((AGENTS / agent_id / "automations").glob("*/automation.json")):
        a = json.loads(safe_read(f))
        trig = (a.get("triggerPresentation") or {}).get("trigger") or {}
        out.append({"slug": f.parent.name, "name": a.get("name"), "cron": a.get("schedule") or trig.get("schedule"),
                    "trigger": trig.get("type", "cron"), "enabled": bool(a.get("enabled")),
                    "timezone": "America/Lima", "prompt": a.get("prompt", "")})
    return out

def cron_words(c):
    if not c: return "(sin cron: disparo por evento)"
    p = c.split()
    if len(p) != 5: return c
    m, h, dom, mon, dow = p
    days = {"*": "todos los días", "1-5": "de lunes a viernes", "1": "los lunes", "2": "los martes",
            "3": "los miércoles", "4": "los jueves", "5": "los viernes", "6": "los sábados", "0": "los domingos"}
    if m.isdigit() and h.isdigit() and dom == "*" and mon == "*":
        return f"{days.get(dow, 'días ' + dow)} a las {int(h)}:{int(m):02d}"
    return f"cron `{c}`"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scope", choices=["bot", "dept", "account"], required=True)
    ap.add_argument("--target", default="")
    ap.add_argument("--out")
    ap.add_argument("--dumps", action="append", default=[])
    ap.add_argument("--include-ambiguous", action="store_true")
    ap.add_argument("--no-memory-in-prompt", action="store_true")
    ap.add_argument("--include-workspace-files", action="store_true")
    ap.add_argument("--no-zip", action="store_true")
    a = ap.parse_args()

    bots, rooms = load_all()
    ambiguous, room_ids = {}, []
    if a.scope == "bot":
        if a.target not in bots: sys.exit("--target debe ser un id de bot (no una sala)")
        ids = [a.target]; label = slugify(bots[a.target]["name"])
    elif a.scope == "dept":
        gm = find_gm(bots, a.target)
        members, ambiguous, room_ids = dept_members(bots, rooms, gm)
        ids = [gm] + sorted(members) + (sorted(ambiguous) if a.include_ambiguous else [])
        label = slugify(a.target)
    else:
        ids = sorted(bots); label = "account"
        room_ids = list(rooms)

    out = Path(a.out or EXPORTS / f"openbot-{label}")
    pkg = out / "tenant"
    for sub in ("agents", "memory", "workspace"):
        (pkg / sub).mkdir(parents=True, exist_ok=True)
    dumps = [Path(d) for d in a.dumps] + [EXPORTS / label, EXPORTS / "memory-dumps"]
    idx = skills_index()

    agent_ids, used, needed_skills, report = {}, set(), set(), []
    all_routines = {}
    for i in ids:
        p = bots[i]
        aid = slugify(p["name"])
        if aid in RESERVED_IDS: aid += "-bot"
        while aid in used: aid = (aid[:36] + "-" + i[:3])
        used.add(aid); agent_ids[i] = aid
        desc = (p.get("description") or "").strip() or f"{p['name']} (sin descripción en Grok)"
        mem, msrc = portable_memory(i, dumps)
        rts = routines_of(i); all_routines[aid] = rts
        corpus = "\n".join([desc, mem] + [r["prompt"] for r in rts])
        sk = sorted(referenced_skills(corpus, idx)); needed_skills.update(sk)
        role = re.sub(r"[#*`>]", "", " ".join(desc.split()))
        role = role if len(role) <= ROLE_MAX else role[:ROLE_MAX - 1].rsplit(" ", 1)[0] + "…"
        prompt = desc
        if mem:
            (pkg / "memory" / f"{aid}.md").write_text(clean(f"# Memoria portable — {p['name']}\n\n{mem}"))
            if not a.no_memory_in_prompt:
                prompt += "\n\n## Memoria portable (exportada de Grok)\n" + mem
        prompt += "\n\n## Zona horaria\nTrabaja en America/Lima. Al pedir routines di siempre la zona IANA America/Lima (OpenBot usa UTC por defecto)."
        entry = {"id": aid, "name": p["name"][:80], "title": (p.get("title") or p["name"])[:120],
                 "role_description": role, "avatar_seed": aid, "type": "built-in",
                 "system_prompt": Lit(clean(prompt)), "skills": sk}
        (pkg / "agents" / f"{aid}.yaml").write_text(
            f"# Grok id: {i}\n" + yaml.dump(entry, allow_unicode=True, sort_keys=False, width=1000))
        wfiles = []
        mdir = AGENTS / i / "memory"
        if mdir.exists():
            for f in sorted(mdir.iterdir()):
                if f.is_file() and f.name != "profile.md" and not DENY.search(str(f)):
                    wfiles.append(f.name)
                    if a.include_workspace_files:
                        (pkg / "workspace" / aid).mkdir(parents=True, exist_ok=True)
                        (pkg / "workspace" / aid / f.name).write_text(safe_read(f))
        report.append({"grok_id": i, "id": aid, "name": p["name"], "skills": sk, "routines": len(rts),
                       "memory_sources": msrc, "memory_lines": len(mem.splitlines()) if mem else 0, "personal_emails_redacted": REDACTED.get(i, 0),
                       "workspace_files_seen": wfiles, "role_truncated": len(" ".join(desc.split())) > ROLE_MAX})

    # agents.yaml requerido; vacío: todos van en agents/ (verificado: ambos se leen)
    (pkg / "agents.yaml").write_text("# Requerido por OpenBot. Los coworkers van uno por archivo en agents/.\nagents: []\n")
    skills = []
    for s in sorted(needed_skills):
        slug = s if SLUG_RE.match(s) else slugify(s)
        skills.append({"slug": slug, "title": idx[s]["name"], "summary": idx[s]["summary"] or idx[s]["name"],
                       "instructions": Lit(clean(idx[s]["text"]))})
    (pkg / "skills.yaml").write_text("# Deduplicadas por slug (una entrada por skill aunque la usen varios bots).\n"
                                     "# Sin `tools`: no verificados para estas skills; el admin otorga herramientas por bot.\n" +
                                     yaml.dump({"skills": skills}, allow_unicode=True, sort_keys=False, width=1000))
    channels = []
    for r in room_ids:
        perm = [agent_ids[m] for m in rooms[r]["members"] if m in agent_ids]
        if len(perm) >= 1:
            channels.append({"id": slugify(rooms[r]["name"]), "name": rooms[r]["name"],
                             "description": f"Sala Grok '{rooms[r]['name']}' ({r}).",
                             "permitted_agents": perm, "allowed_groups": ["all"]})
    (pkg / "channels.yaml").write_text("# Salas Grok → channels. OJO: OpenBot no crea membresías para canales del paquete\n"
                                       "# (docs/configuration.md): hay que agregar personas a mano.\n" +
                                       yaml.dump({"channels": channels}, allow_unicode=True, sort_keys=False, width=1000))
    (pkg / "brand.yaml").write_text(yaml.dump({"tenant": {"id": f"ignacio-{label}", "product_name": f"Bots de Ignacio · {label}"}}, allow_unicode=True))
    (pkg / "model.yaml").write_text("# credential_secret_ref es una REFERENCIA a /admin/credentials, no una llave.\n" +
                                    yaml.dump({"model": {"provider": "openai", "credential_secret_ref": "openai-api-key",
                                                         "default_model": "CAMBIAR-por-el-modelo-del-endpoint"}}))
    (pkg / "knowledge.yaml").write_text("# Solo google-drive / microsoft-onedrive. Vacío por defecto.\nsources: []\n")

    rlist = []
    md = ["# ⏰ Routines — crear a mano (OpenBot no las siembra por paquete; docs/routines.md)\n",
          "> Requisitos: admin otorga `create_routine` en `/admin/plugins/routines`; piso 15 min; máx. 20 activas por persona; **zona por defecto UTC → di siempre America/Lima**.\n"]
    for aid, rts in all_routines.items():
        for r in rts:
            rlist.append({"agent": aid, **r})
            estado = "ACTIVA" if r["enabled"] else "⏸️ PAUSADA (no crear todavía)"
            md.append(f"\n## {aid} · {r['name']} · {estado}\n- Cron: `{r['cron']}` (America/Lima) · {cron_words(r['cron'])}\n"
                      f"- Pedido (pégalo en el chat de **{aid}**):\n```\nCrea una routine en este canal: {cron_words(r['cron'])}, "
                      f"hora de Lima (zona America/Lima). Nombre: \"{r['name']}\". Instrucción:\n{r['prompt'].strip()}\n```\n")
    (out / "ROUTINES.md").write_text("".join(md))
    (out / "routines.json").write_text(json.dumps(rlist, ensure_ascii=False, indent=2))

    amb_md = "".join(f"- ⚠️ {bots[m]['name']} · `{m}`: {why}{' (incluido)' if a.include_ambiguous else ' (NO incluido)'}\n"
                     for m, why in ambiguous.items()) or "- Ninguno\n"
    (out / "README.md").write_text(clean(f"""# 📦 Paquete OpenBot — {label} ({a.scope})

- **Qué es:** carpeta de tenant de OpenBot en `tenant/` + `{label}.zip`. OpenBot NO importa zips: se descomprime y se apunta `TENANT_PACKAGE_DIR` a `tenant/`, luego se reinicia el server.
- **Bots:** {len(ids)} · **Skills (dedupe):** {len(skills)} · **Canales:** {len(channels)} · **Routines:** {len(rlist)} (crear a mano, ver ROUTINES.md)
- **Memorias:** `tenant/memory/<id>.md` y, salvo `--no-memory-in-prompt`, al final del `system_prompt`.
- **Archivos de workspace:** `tenant/workspace/` solo con `--include-workspace-files` (OpenBot no los lee; subirlos al /workspace de cada bot).

## ⚠️ Ambiguos
{amb_md}
## 📋 Bots
""" + "".join(f"- {r['name']} → `{r['id']}` · skills {len(r['skills'])} · routines {r['routines']} · memoria {r['memory_lines']} líneas\n" for r in report)))
    (out / "MIGRATION.md").write_text(clean("""# 🚚 Checklist — OpenBot
- [ ] Ignacio aprobó el alcance y la lista de bots; aviso a Orquestador
- [ ] Volcados de memoria pedidos a cada bot (ver skill exportar-bot v2) y re-correr el builder
- [ ] Desplegar OpenBot; `TENANT_PACKAGE_DIR` → `tenant/`; editar model.yaml; reiniciar (valida al arrancar)
- [ ] Admin: conectores (Notion, Drive, Composio) y grants por bot; `message_bot` entre GM y staff
- [ ] Agregar personas a cada canal (el paquete no crea membresías)
- [ ] Crear routines de ROUTINES.md en America/Lima (las pausadas, no)
- [ ] Smoke test por bot: recall, routine de prueba, paridad
- [ ] Solo tras verificación y OK de Ignacio: pausar (no borrar) los bots Grok
"""))
    (out / "build-report.json").write_text(json.dumps({"scope": a.scope, "target": a.target, "bots": report,
                                                       "ambiguous": ambiguous, "skills": [s["slug"] for s in skills],
                                                       "channels": [c["id"] for c in channels]}, ensure_ascii=False, indent=2))

    # Validación estilo loader (tenant-package.ts)
    errs = []
    sl = {s["slug"] for s in skills}
    if len(sl) != len(skills): errs.append("slug duplicado")
    for s in sl:
        if not SLUG_RE.match(s): errs.append(f"slug inválido {s}")
    for f in (pkg / "agents").glob("*.yaml"):
        e = yaml.safe_load(f.read_text())
        for k in ("id", "name", "title", "role_description", "type", "system_prompt"):
            if not e.get(k): errs.append(f"{f.name}: falta {k}")
        for s in e.get("skills", []):
            if s not in sl: errs.append(f"{f.name}: skill {s} no está en skills.yaml")
        if len(e["role_description"]) > ROLE_MAX: errs.append(f"{f.name}: role_description > 1000")
    for c in channels:
        if len(set(c["permitted_agents"])) != len(c["permitted_agents"]): errs.append(f"canal {c['id']} repite agente")
    hits = []
    for f in out.rglob("*"):
        if f.is_file() and f.suffix in (".md", ".yaml", ".json"):
            for n, line in enumerate(f.read_text(errors="replace").splitlines(), 1):
                if SECRET_RE.search(line): hits.append(f"{f.relative_to(out)}:{n}")
    zpath = None
    if not a.no_zip and not hits:
        zpath = out / f"{label}.zip"
        with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
            for f in sorted(out.rglob("*")):
                if f.is_file() and f != zpath:
                    z.write(f, f.relative_to(out))
    print(json.dumps({"out": str(out), "zip": str(zpath) if zpath else None, "bots": len(ids),
                      "skills": len(skills), "channels": len(channels), "routines": len(rlist),
                      "ambiguous": {bots[m]["name"]: w for m, w in ambiguous.items()},
                      "validation_errors": errs, "secret_hits": hits}, ensure_ascii=False, indent=2))
    sys.exit(1 if errs or hits else 0)

if __name__ == "__main__":
    main()
