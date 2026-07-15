#!/usr/bin/env bash
# clone-to-software.sh — clone a GitHub repo into 02_Programs/3-Software/ with
# Drive-safe defaults (SSH rewrite + core.fileMode false + health check).
#
# Usage:
#   clone-to-software.sh <url|owner/repo> [target-name] [--dry-run]
#
# Accepts:
#   https://github.com/OWNER/REPO            git@github.com:OWNER/REPO.git
#   https://github.com/OWNER/REPO.git        OWNER/REPO
#   https://github.com/OWNER/REPO/tree/BRANCH   (branch is honored)
#
# Exit codes: 0 ok · 2 bad args · 3 target exists · 4 clone failed · 5 corrupt after clone

set -uo pipefail

DRY=0; ARGS=()
for a in "$@"; do
  case "$a" in
    --dry-run) DRY=1 ;;
    *) ARGS+=("$a") ;;
  esac
done
RAW="${ARGS[0]:-}"
TARGET_NAME="${ARGS[1]:-}"
[ -z "$RAW" ] && { echo "usage: clone-to-software.sh <url|owner/repo> [target-name] [--dry-run]"; exit 2; }

# Vault root = 4 levels up from this script (.claude/skills/clone-software-repo/scripts/)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
VAULT_ROOT="$(cd "$SCRIPT_DIR/../../../.." && pwd)"
SOFT="$VAULT_ROOT/02_Programs/3-Software"
[ -d "$SOFT" ] || { echo "ERROR: 3-Software not found at $SOFT"; exit 2; }

# --- parse owner/repo (+ optional branch) ---
BRANCH=""
if [[ "$RAW" =~ /tree/([^/]+) ]]; then BRANCH="${BASH_REMATCH[1]}"; fi
if [[ "$RAW" =~ github\.com[:/]+([^/]+)/([^/]+) ]]; then
  OWNER="${BASH_REMATCH[1]}"; REPO="${BASH_REMATCH[2]}"
elif [[ "$RAW" =~ ^([A-Za-z0-9._-]+)/([A-Za-z0-9._-]+)$ ]]; then
  OWNER="${BASH_REMATCH[1]}"; REPO="${BASH_REMATCH[2]}"
else
  echo "ERROR: can't parse a GitHub owner/repo from: $RAW"; exit 2
fi
REPO="${REPO%.git}"; REPO="${REPO%/}"
SSH="git@github.com:$OWNER/$REPO.git"   # HTTPS auth is broken in this env — always SSH
NAME="${TARGET_NAME:-$REPO}"
TARGET="$SOFT/$NAME"

echo "owner/repo : $OWNER/$REPO"
echo "ssh url    : $SSH"
[ -n "$BRANCH" ] && echo "branch     : $BRANCH"
echo "target     : 02_Programs/3-Software/$NAME"

if [ -e "$TARGET" ]; then
  echo "EXISTS: $TARGET already present — refusing to overwrite. Pick a [target-name] or remove it first."
  exit 3
fi

if [ "$DRY" = "1" ]; then echo "[dry-run] would clone now."; exit 0; fi

# --- clone (SSH) ---
if [ -n "$BRANCH" ]; then
  git clone --branch "$BRANCH" "$SSH" "$TARGET" || { echo "CLONE_FAILED"; exit 4; }
else
  git clone "$SSH" "$TARGET" || { echo "CLONE_FAILED"; exit 4; }
fi

cd "$TARGET" || exit 4
git config core.fileMode false          # Drive flips perm bits → silence mode-noise

# --- health check (Drive can corrupt the object store) ---
if git fsck --connectivity-only 2>&1 | grep -qiE 'bad object|did not send|badRefName'; then
  echo "WARN: fsck reports corruption right after clone (Drive?). Inspect before trusting."
  exit 5
fi

# --- stack detection → install hint ---
INSTALL="(none detected)"
if   [ -f bun.lockb ] || [ -f bun.lock ];        then INSTALL="bun install"
elif [ -f pnpm-lock.yaml ];                       then INSTALL="pnpm install"
elif [ -f yarn.lock ];                            then INSTALL="yarn"
elif [ -f package-lock.json ] || [ -f package.json ]; then INSTALL="npm install"
elif [ -f deno.json ] || [ -f deno.jsonc ] || [ -f deno.lock ]; then INSTALL="deno cache / deno task"
elif [ -f pyproject.toml ];                       then INSTALL="uv sync  (or pip install -e .)"
elif [ -f requirements.txt ];                     then INSTALL="pip install -r requirements.txt"
elif [ -f Cargo.toml ];                           then INSTALL="cargo build"
elif [ -f go.mod ];                               then INSTALL="go mod download"
fi

CUR_BRANCH="$(git rev-parse --abbrev-ref HEAD)"
LAST="$(git log -1 --format='%h %s')"
HAS_ENV=no; [ -f .env ] && HAS_ENV=yes
HAS_AGENTS=no; { [ -f AGENTS.md ] || [ -f CLAUDE.md ]; } && HAS_AGENTS=yes

echo "----- CLONED -----"
echo "path        : 02_Programs/3-Software/$NAME"
echo "branch      : $CUR_BRANCH"
echo "latest      : $LAST"
echo "stack/install: $INSTALL"
echo ".env present : $HAS_ENV"
echo "agent docs   : $HAS_AGENTS (AGENTS.md/CLAUDE.md)"
