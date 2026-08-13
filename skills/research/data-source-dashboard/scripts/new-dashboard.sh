#!/usr/bin/env bash
# Scaffold a dashboard project from the data-source-dashboard templates.
# Usage: new-dashboard.sh <dest-dir> "<Dashboard Title>"
# Exit: 2 bad args · 3 destination exists
set -euo pipefail

DEST="${1:-}"
TITLE="${2:-}"
if [[ -z "$DEST" || -z "$TITLE" ]]; then
  echo "usage: new-dashboard.sh <dest-dir> \"<Dashboard Title>\"" >&2
  exit 2
fi
if [[ -e "$DEST" ]]; then
  echo "destination exists: $DEST (never clobbered — pick another path)" >&2
  exit 3
fi

SKILL_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
mkdir -p "$DEST/visuals"

sed "s|__TITLE__|${TITLE}|g" "$SKILL_DIR/templates/analyze.template.mjs"   > "$DEST/analyze.mjs"
sed "s|__TITLE__|${TITLE}|g" "$SKILL_DIR/templates/dashboard.template.html" > "$DEST/dashboard.template.html"

cat > "$DEST/README.md" <<EOF
# ${TITLE}

Aggregated dashboard built with the \`data-source-dashboard\` skill. The raw
export stays where it is — only \`metrics.json\` (aggregates, no personal data)
lives here.

## Refresh with a new export

\`\`\`bash
node analyze.mjs "<path-to-raw-export>"                                  # -> metrics.json
node "${SKILL_DIR}/scripts/audit.mjs" .                                  # publication gate
node "${SKILL_DIR}/scripts/build.mjs" .                                  # -> dashboard.html
\`\`\`

Then republish \`dashboard.html\` with the Artifact tool — same file path keeps
the same URL.

## Files

| File | Role |
|---|---|
| \`analyze.mjs\` | raw source → \`metrics.json\` (edit \`FIELDS\` to match the source) |
| \`dashboard.template.html\` | the page; \`__METRICS_JSON__\` and \`__DIAGRAM_*__\` are filled at build |
| \`metrics.json\` | aggregates — safe to commit |
| \`visuals/\` | \`.excalidraw\` sources + rendered \`.png\`, inlined as data: URIs |
| \`dashboard.html\` | build output — this is what gets published |
EOF

cat > "$DEST/.gitignore" <<'EOF'
# raw exports never belong in the repo
*.csv
*.tsv
raw/
EOF

echo "ok: scaffolded $DEST"
echo "next: 1) map FIELDS in analyze.mjs  2) node analyze.mjs <raw>  3) build the sections"
