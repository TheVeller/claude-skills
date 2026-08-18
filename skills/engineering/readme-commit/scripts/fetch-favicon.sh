#!/usr/bin/env bash
# fetch-favicon.sh — download a site's favicon/apple-touch-icon into repo assets.
# Usage: fetch-favicon.sh <url> [outdir]
# Default outdir: docs/assets/brand (created if missing). Prints saved path.
set -euo pipefail

URL="${1:-}"
OUTDIR="${2:-docs/assets/brand}"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [[ -z "$URL" ]]; then
  echo "Usage: $0 <url> [outdir]" >&2
  exit 2
fi

# Normalize base
BASE="${URL%/}"
case "$BASE" in
  http://*|https://*) ;;
  *) BASE="https://$BASE" ;;
esac

mkdir -p "$OUTDIR"

TMP="$(mktemp)"
trap 'rm -f "$TMP"' EXIT

if ! curl -fsSL -L --max-time 25 -A "readme-commit-favicon/1.0" "$BASE" -o "$TMP" 2>/dev/null; then
  echo "WARN: could not fetch HTML from $BASE" >&2
  ICON_URL="${BASE}/favicon.ico"
else
  ICON_URL="$(python3 "$SCRIPT_DIR/resolve-icon-url.py" "$BASE" "$TMP")"
fi

EXT="${ICON_URL##*.}"
EXT="$(echo "$EXT" | cut -d'?' -f1 | tr '[:upper:]' '[:lower:]')"
case "$EXT" in
  png|ico|svg|jpg|jpeg|webp|gif) ;;
  *) EXT="ico" ;;
esac

HOST="$(python3 -c "import urllib.parse,sys; print(urllib.parse.urlparse(sys.argv[1]).hostname or 'site')" "$BASE")"
OUTFILE="${OUTDIR%/}/${HOST}.${EXT}"

if ! curl -fsSL -L --max-time 25 -A "readme-commit-favicon/1.0" "$ICON_URL" -o "$OUTFILE"; then
  echo "ERROR: failed to download icon from $ICON_URL" >&2
  exit 1
fi

SIZE="$(wc -c < "$OUTFILE" | tr -d ' ')"
if [[ "$SIZE" -lt 50 ]]; then
  echo "ERROR: downloaded file too small ($SIZE bytes) — not a usable icon" >&2
  rm -f "$OUTFILE"
  exit 1
fi

echo "$OUTFILE"
