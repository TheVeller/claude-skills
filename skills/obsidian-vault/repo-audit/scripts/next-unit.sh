#!/usr/bin/env bash
# Print next pending unit from Repo-Audit MANIFEST.md
# Usage: next-unit.sh [unit-id]
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../../.." && pwd)"
MANIFEST="$ROOT/06_Metadata/Reference/Repo-Audit/MANIFEST.md"

if [[ ! -f "$MANIFEST" ]]; then
  echo "MANIFEST missing: $MANIFEST" >&2
  exit 1
fi

if [[ -n "${1:-}" ]]; then
  awk -F'|' -v id="$1" '
    /^\|/ && $2 ~ id { gsub(/^[ \t]+|[ \t]+$/, "", $2); gsub(/^[ \t]+|[ \t]+$/, "", $3); gsub(/^[ \t]+|[ \t]+$/, "", $4); gsub(/^[ \t]+|[ \t]+$/, "", $5); print $2"|"$3"|"$4"|"$5; exit }
  ' "$MANIFEST"
  exit 0
fi

awk -F'|' '
  /^\|/ && $5 ~ /pending/ {
    gsub(/^[ \t]+|[ \t]+$/, "", $2)
    gsub(/^[ \t]+|[ \t]+$/, "", $3)
    gsub(/^[ \t]+|[ \t]+$/, "", $4)
    gsub(/^[ \t]+|[ \t]+$/, "", $5)
    if ($2 != "ID" && $2 != "---") { print $2"|"$3"|"$4"|"$5; exit }
  }
' "$MANIFEST"
