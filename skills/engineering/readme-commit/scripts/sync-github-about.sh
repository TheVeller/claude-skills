#!/usr/bin/env bash
# sync-github-about.sh — set GitHub About (description, optional homepage, topics).
# Usage:
#   sync-github-about.sh <owner/repo> --description "…" [--homepage URL] [--topic t]… [--dry-run]
set -euo pipefail

REPO="${1:-}"
shift || true

if [[ -z "$REPO" || "$REPO" != */* ]]; then
  echo "Usage: $0 <owner/repo> --description \"…\" [--homepage URL] [--topic t]… [--dry-run]" >&2
  exit 2
fi

DESC=""
HOMEPAGE=""
DRY=0
TOPICS=()

while [[ $# -gt 0 ]]; do
  case "$1" in
    --description|-d)
      DESC="${2:-}"
      shift 2
      ;;
    --homepage|-h)
      HOMEPAGE="${2:-}"
      shift 2
      ;;
    --topic|-t)
      TOPICS+=("${2:-}")
      shift 2
      ;;
    --dry-run)
      DRY=1
      shift
      ;;
    *)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
  esac
done

if [[ -z "$DESC" ]]; then
  echo "ERROR: --description is required" >&2
  exit 2
fi

CMD=(gh repo edit "$REPO" --description "$DESC")

# Homepage only when provided (non-empty)
if [[ -n "$HOMEPAGE" ]]; then
  CMD+=(--homepage "$HOMEPAGE")
fi

for t in "${TOPICS[@]+"${TOPICS[@]}"}"; do
  [[ -n "$t" ]] && CMD+=(--add-topic "$t")
done

if [[ "$DRY" -eq 1 ]]; then
  printf 'DRY-RUN:'
  printf ' %q' "${CMD[@]}"
  printf '\n'
  exit 0
fi

"${CMD[@]}"
echo "Updated About for $REPO"
