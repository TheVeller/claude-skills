#!/usr/bin/env bash
# repo-sync.sh — check / sync a local git repo against its GitHub remote.
#
# Design goal: make the local working copy match the GitHub remote's latest,
# the way it's needed when a repo is also edited in the cloud (e.g. Lovable
# commits to GitHub and the local clone falls behind).
#
# Safe by default:
#   - `check` is READ-ONLY: fetch + report state, never mutates.
#   - `sync` fast-forwards when that's lossless; for anything that would
#     discard local commits or uncommitted work it REFUSES unless --force,
#     and even with --force it first creates a recoverable backup
#     (a backup/pre-sync-<ts> branch for committed state + a git stash for
#     uncommitted/untracked files) BEFORE touching anything.
#
# Usage:
#   repo-sync.sh check            # read-only status + recommendation
#   repo-sync.sh sync             # apply the safe action (ff-only / no-op)
#   repo-sync.sh sync --force     # also allow overwriting local (with backup)
set -euo pipefail

CMD="${1:-check}"; shift || true
FORCE=0
for arg in "$@"; do
  case "$arg" in
    --force) FORCE=1 ;;
    *) echo "unknown arg: $arg" >&2; exit 64 ;;
  esac
done

if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  echo "ERROR: not inside a git repository" >&2; exit 2
fi

BRANCH="$(git branch --show-current)"
if [ -z "$BRANCH" ]; then
  echo "ERROR: detached HEAD — checkout a branch first" >&2; exit 2
fi

# Upstream, falling back to origin/<branch> when none is configured.
if ! UPSTREAM="$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null)"; then
  UPSTREAM="origin/${BRANCH}"
fi
REMOTE_NAME="${UPSTREAM%%/*}"

echo "repo:     $(git rev-parse --show-toplevel)"
echo "branch:   $BRANCH"
echo "upstream: $UPSTREAM"

echo "fetching $REMOTE_NAME ..."
if ! git fetch --quiet "$REMOTE_NAME"; then
  echo "ERROR: git fetch failed (no network / no remote?)" >&2; exit 3
fi
if ! git rev-parse --verify --quiet "$UPSTREAM" >/dev/null; then
  echo "ERROR: upstream ref '$UPSTREAM' not found on remote" >&2; exit 3
fi

LOCAL="$(git rev-parse @)"
REMOTE="$(git rev-parse "$UPSTREAM")"
BASE="$(git merge-base @ "$UPSTREAM")"
AHEAD="$(git rev-list --count "$UPSTREAM"..@)"
BEHIND="$(git rev-list --count @.."$UPSTREAM")"
DIRTY=0; [ -n "$(git status --porcelain)" ] && DIRTY=1

if   [ "$LOCAL" = "$REMOTE" ]; then STATE="up-to-date"
elif [ "$LOCAL" = "$BASE"   ]; then STATE="behind"
elif [ "$REMOTE" = "$BASE"  ]; then STATE="ahead"
else                                STATE="diverged"
fi

echo "state:    $STATE (ahead $AHEAD, behind $BEHIND, dirty=$DIRTY)"

backup() {
  local ts bb; ts="$(date +%Y%m%d-%H%M%S)"; bb="backup/pre-sync-$ts"
  git branch "$bb" "$LOCAL" >/dev/null 2>&1 || true
  echo "backup:   branch $bb -> ${LOCAL:0:9} (committed state recoverable here)"
  if [ "$DIRTY" = "1" ]; then
    git stash push -u -m "pre-sync $ts" >/dev/null
    echo "backup:   uncommitted + untracked saved to git stash ('pre-sync $ts')"
  fi
}

case "$CMD" in
  check)
    case "$STATE" in
      up-to-date) echo "action:   none — local already matches $UPSTREAM" ;;
      behind)     echo "action:   run 'sync' to fast-forward $BEHIND commit(s) (lossless)" ;;
      ahead)      echo "action:   local has $AHEAD unpushed commit(s); 'sync --force' DISCARDS them (backed up first)" ;;
      diverged)   echo "action:   diverged; 'sync --force' OVERWRITES local with remote (backed up first)" ;;
    esac
    [ "$DIRTY" = "1" ] && echo "note:     working tree has uncommitted/untracked changes"
    ;;
  sync)
    case "$STATE" in
      up-to-date)
        echo "action:   nothing to pull."
        [ "$DIRTY" = "1" ] && echo "note:     uncommitted changes left untouched."
        ;;
      behind)
        if [ "$DIRTY" = "1" ] && [ "$FORCE" != "1" ]; then
          echo "BLOCKED:  behind but working tree is dirty. Re-run 'sync --force' to stash local changes and fast-forward." >&2
          exit 10
        fi
        [ "$DIRTY" = "1" ] && backup
        git merge --ff-only "$UPSTREAM"
        echo "action:   fast-forwarded to $UPSTREAM"
        ;;
      ahead|diverged)
        if [ "$FORCE" != "1" ]; then
          echo "BLOCKED:  $STATE — overwriting local would discard commits. Confirm with the user, then re-run 'sync --force' (backup branch + stash are made automatically)." >&2
          exit 10
        fi
        backup
        git reset --hard "$UPSTREAM"
        echo "action:   hard-reset local to $UPSTREAM (recover prior state from the backup above)"
        ;;
    esac
    ;;
  *)
    echo "usage: repo-sync.sh [check|sync] [--force]" >&2; exit 64 ;;
esac
