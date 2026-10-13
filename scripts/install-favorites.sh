#!/usr/bin/env bash
# Install TheVeller's curated third-party favorites from their upstream repos.
#   scripts/install-favorites.sh            install into the current project
#   scripts/install-favorites.sh -g         install globally
#   scripts/install-favorites.sh --dry-run  print the commands only
set -euo pipefail
cd "$(dirname "$0")/.."
extra=()
dry=0
for arg in "$@"; do
  case "$arg" in
    --dry-run) dry=1 ;;
    *) extra+=("$arg") ;;
  esac
done
node -e '
const { sources } = require("./favorites.json");
for (const s of sources) console.log([s.repo, ...s.skills].join(" "));
' | while read -r repo skills; do
  # shellcheck disable=SC2086
  cmd=(npx -y skills add "$repo" -s $skills -y ${extra[@]+"${extra[@]}"})
  if [ "$dry" = 1 ]; then echo "${cmd[*]}"; else "${cmd[@]}"; fi
done
