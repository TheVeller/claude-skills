#!/usr/bin/env bash
# check-readme-contract.sh — fail-closed gate for readme-commit.
# Usage:
#   check-readme-contract.sh <path/to/README.md> [--repo owner/repo] [--require-homepage]
# Ship MUST pass with --repo.
set -euo pipefail

README=""
REPO=""
REQUIRE_HOMEPAGE=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --repo)
      REPO="${2:-}"
      shift 2
      ;;
    --require-homepage)
      REQUIRE_HOMEPAGE=1
      shift
      ;;
    -*)
      echo "Unknown arg: $1" >&2
      exit 2
      ;;
    *)
      if [[ -z "$README" ]]; then
        README="$1"
        shift
      else
        echo "Unexpected arg: $1" >&2
        exit 2
      fi
      ;;
  esac
done

if [[ -z "$README" || ! -f "$README" ]]; then
  echo "Usage: $0 <path/to/README.md> [--repo owner/repo] [--require-homepage]" >&2
  exit 2
fi

FAIL=0
ok() { echo "OK  $1"; }
bad() { echo "MISSING  $1" >&2; FAIL=1; }

# Exact locked H2s
if grep -qF '## ✨ Why this exists + Features' "$README"; then ok "H2 Why + Features"; else bad "H2 Why + Features"; fi
if grep -qF '## 🚀 Quick start' "$README"; then ok "H2 Quick start"; else bad "H2 Quick start"; fi

# Footer
if grep -qE 'with 🖤 by .+TheVeller.+ · .+Núcleo Lab.+ · .+Crafter Station' "$README" \
  || grep -qF 'with 🖤 by TheVeller · Núcleo Lab · Crafter Station' "$README"; then
  ok "footer TheVeller · Núcleo Lab · Crafter Station"
else
  bad "footer TheVeller · Núcleo Lab · Crafter Station"
fi

# Double-box hero OR distilledbrew-style centered H1 block
if grep -qF '╔' "$README"; then
  ok "hero box-drawing ╔"
elif grep -qE '<h1 align="center">' "$README" && grep -qE '<p align="center">' "$README"; then
  ok "hero centered logo/H1 pattern"
else
  bad "hero double-box ╔ (or centered distilledbrew H1)"
fi

# Cover or honest skip
if grep -qE 'width="900"' "$README"; then
  ok "cover width=900"
elif grep -qF '<!-- cover: pending -->' "$README" \
  || grep -qiE 'UI screenshots not in-repo yet' "$README"; then
  ok "cover honest skip"
else
  bad "cover width=900 OR honest skip marker/prose"
fi

# Compatible-with: channels only — deny stack names in src/alt
STACK_DENY='react|vite|bun\.sh|clerk|supabase|tanstack|tailwind|typescript'
if grep -qF '<!-- logos: pending -->' "$README"; then
  ok "logos pending marker"
elif grep -qF '### Compatible with' "$README"; then
  COMPAT_BLOB="$(awk '
    BEGIN { on=0 }
    /^### Compatible with/ { on=1; next }
    on && /^## / { exit }
    on && /^### / && $0 !~ /^### Compatible with/ { exit }
    on { print }
  ' "$README")"
  IMG_COUNT="$(printf '%s\n' "$COMPAT_BLOB" | grep -c '<img ' || true)"
  if [[ "$IMG_COUNT" -lt 2 ]]; then
    bad "Compatible-with needs ≥2 <img> (found $IMG_COUNT) or <!-- logos: pending -->"
  else
    if printf '%s\n' "$COMPAT_BLOB" | grep -qiE "$STACK_DENY"; then
      bad "Compatible-with contains stack marks (deny: react/vite/bun/clerk/supabase/tanstack/tailwind/typescript) — use badges + Tech Stack / Surfaces"
    else
      ok "Compatible-with strip ($IMG_COUNT imgs, no stack deny-list hits)"
    fi
  fi
else
  bad "### Compatible with strip OR <!-- logos: pending -->"
fi

# Surfaces / App tools matrix
if grep -qF '<!-- surfaces: pending -->' "$README"; then
  ok "surfaces pending marker"
elif grep -qE '^## .+Surfaces|^## .+App tools' "$README"; then
  SURF_BLOB="$(awk '
    BEGIN { on=0 }
    /^## / && /Surfaces|App tools/ { on=1; next }
    on && /^## / { exit }
    on { print }
  ' "$README")"
  SURF_IMGS="$(printf '%s\n' "$SURF_BLOB" | grep -c '<img ' || true)"
  # Count table data rows (lines starting with | that are not header/separator)
  SURF_ROWS="$(printf '%s\n' "$SURF_BLOB" | grep -E '^\|' | grep -vE '^\|\s*-+' | grep -vE '^\|\s*\|?\s*Name\s*\|' | grep -ciE '<img ' || true)"
  if [[ "$SURF_IMGS" -ge 2 ]]; then
    ok "Surfaces matrix ($SURF_IMGS logos in section)"
  else
    bad "Surfaces / App tools needs ≥2 <img> in table rows (found $SURF_IMGS) or <!-- surfaces: pending -->"
  fi
else
  bad "H2 Surfaces / App tools OR <!-- surfaces: pending -->"
fi

# Topics H2 + ≥3 topic-like tokens
if ! grep -qE '^## 🏷️ Topics' "$README"; then
  bad "H2 Topics (## 🏷️ Topics …)"
else
  ok "H2 Topics"
  TOPIC_BLOB="$(awk '
    BEGIN { on=0 }
    /^## 🏷️ Topics/ { on=1; next }
    on && /^## / { exit }
    on { print }
  ' "$README")"
  TOPIC_N="$(printf '%s\n' "$TOPIC_BLOB" | grep -oE '`[a-z0-9][a-z0-9._-]*`|[a-z0-9][a-z0-9._-]{2,}' | grep -viE '^(topics|search|keywords|and|the|for|with)$' | sort -u | wc -l | tr -d ' ')"
  if [[ "$TOPIC_N" -ge 3 ]]; then
    ok "Topics tokens (≥3, found $TOPIC_N)"
  else
    bad "Topics section needs ≥3 topic tokens (found $TOPIC_N)"
  fi
fi

# Every ## H2 must start with a leading emoji
EMOJI_FAIL=0
while IFS= read -r line; do
  case "$line" in
    '## '*)
      case "$line" in
        '###'*) continue ;;
      esac
      rest="${line#\#\# }"
      first="$(printf '%s' "$rest" | cut -c1)"
      case "$first" in
        [A-Za-z0-9#*_\[\`])
          bad "H2 missing leading emoji: $line"
          EMOJI_FAIL=1
          ;;
      esac
      ;;
  esac
done < "$README"

if [[ "$EMOJI_FAIL" -eq 0 ]] && grep -qE '^## ' "$README"; then
  ok "all H2s emoji-prefixed"
fi

HAS_LIVE_URL=0
if grep -qiE 'https?://[a-z0-9.-]+\.(lovable\.app|vercel\.app|netlify\.app)' "$README" \
  || grep -qiE '\*\*\[Live|\*\*\[Website|\*\*\[App' "$README"; then
  HAS_LIVE_URL=1
fi

if [[ -n "$REPO" ]]; then
  if [[ "$REPO" != */* ]]; then
    bad "--repo must be owner/repo (got: $REPO)"
  else
    ABOUT_JSON="$(gh api "repos/$REPO" --jq '{description,homepage,topics}' 2>/dev/null || true)"
    if [[ -z "$ABOUT_JSON" ]]; then
      bad "gh api repos/$REPO (About fetch failed)"
    else
      DESC="$(printf '%s' "$ABOUT_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("description") or "")')"
      HOME="$(printf '%s' "$ABOUT_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(d.get("homepage") or "")')"
      TOPIC_LEN="$(printf '%s' "$ABOUT_JSON" | python3 -c 'import json,sys; d=json.load(sys.stdin); print(len(d.get("topics") or []))')"
      if [[ -n "$DESC" ]]; then
        ok "About description set"
      else
        bad "About description empty — run sync-github-about.sh"
      fi
      if [[ "$TOPIC_LEN" -ge 3 ]]; then
        ok "About topics (≥3, found $TOPIC_LEN)"
      else
        bad "About topics need ≥3 (found $TOPIC_LEN)"
      fi
      if [[ "$REQUIRE_HOMEPAGE" -eq 1 || "$HAS_LIVE_URL" -eq 1 ]]; then
        if [[ -n "$HOME" ]]; then
          ok "About homepage set ($HOME)"
        else
          bad "About homepage empty but live URL in README (or --require-homepage)"
        fi
      else
        ok "About homepage optional (no live URL detected)"
      fi
    fi
  fi
else
  echo "NOTE  --repo omitted: skipping native About checks (dev only; ship MUST pass --repo)"
fi

if [[ "$FAIL" -ne 0 ]]; then
  echo "check-readme-contract: FAIL $README" >&2
  exit 1
fi
echo "check-readme-contract: PASS $README${REPO:+ ($REPO)}"
exit 0
