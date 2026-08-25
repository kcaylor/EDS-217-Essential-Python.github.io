#!/usr/bin/env bash
# Shared setup for the EDS 217 helper scripts. Source it, do not run it.
#
# Activates the course conda environment and moves to the repo root, so every
# relative path in the scripts means the same thing wherever they are called
# from.

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$REPO_ROOT"

ENV_NAME="${EDS217_ENV:-eds217_2026}"

# Headless plotting for every script here. Without this, a plt.show() in a page
# opens a window, or on macOS aborts the process outright.
export MPLBACKEND="${MPLBACKEND:-Agg}"

eds217_activate() {
  if [ "${EDS217_SKIP_ENV:-0}" = "1" ]; then
    return 0
  fi
  if [ "${CONDA_DEFAULT_ENV:-}" = "$ENV_NAME" ]; then
    return 0
  fi
  if ! command -v conda >/dev/null 2>&1; then
    echo "conda is not on PATH. Open a shell where conda is initialised, or set" >&2
    echo "EDS217_SKIP_ENV=1 to run without it." >&2
    exit 1
  fi

  # Conda's activate and deactivate hooks are not written to survive `set -u`.
  # The geotiff hook shipped with mambaforge reads _CONDA_SET_GEOTIFF_CSV with
  # no default, so under `set -euo pipefail` the whole script dies on an unbound
  # variable before a single page renders, and the only thing printed is a line
  # number inside somebody else's deactivate script.
  #
  # Relax both options across the activation, then put back whatever was in
  # force. The hooks are third-party code and we do not get to fix them.
  local restore=""
  case "$-" in *u*) restore="${restore}u";; esac
  case "$-" in *e*) restore="${restore}e";; esac
  set +u +e

  # shellcheck disable=SC1090
  eval "$(conda shell.bash hook)"
  if ! conda env list | grep -qE "^${ENV_NAME}[[:space:]]"; then
    case "$restore" in *u*) set -u;; esac
    case "$restore" in *e*) set -e;; esac
    echo "conda environment '${ENV_NAME}' does not exist." >&2
    echo "Create it with: conda env create -f environment-2026.yml" >&2
    exit 1
  fi
  conda activate "$ENV_NAME"
  local rc=$?

  case "$restore" in *u*) set -u;; esac
  case "$restore" in *e*) set -e;; esac

  if [ "$rc" -ne 0 ]; then
    echo "conda activate ${ENV_NAME} failed with status ${rc}." >&2
    exit 1
  fi
  if [ "${CONDA_DEFAULT_ENV:-}" != "$ENV_NAME" ]; then
    echo "conda activate reported success but the active environment is" >&2
    echo "'${CONDA_DEFAULT_ENV:-none}' rather than '${ENV_NAME}'." >&2
    exit 1
  fi
  return 0
}

eds217_clear_stale_locks() {
  # Every git command run from a Cowork session leaves a lock file behind,
  # because that mount cannot delete files. The next git command then reports
  # "Another git process seems to be running", which is misleading: nothing is
  # running. Clear them here, but only after confirming that is true.
  if pgrep -x git >/dev/null 2>&1; then
    echo "A git process is running. Not touching the lock files." >&2
    pgrep -l git >&2
    return 1
  fi
  local cleared=0 stuck=0 f
  for f in .git/*.lock .git/refs/heads/*.lock; do
    [ -e "$f" ] || continue
    if rm -f "$f" 2>/dev/null; then
      cleared=$((cleared + 1))
    else
      stuck=$((stuck + 1))
      echo "Could not remove $f" >&2
    fi
  done
  [ "$cleared" -gt 0 ] && echo "Cleared $cleared stale git lock file(s)."
  if [ "$stuck" -gt 0 ]; then
    echo "$stuck lock file(s) could not be removed. If you are in a Cowork" >&2
    echo "session, delete them from a terminal on the machine itself." >&2
    return 1
  fi
  return 0
}

eds217_need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "$1 is not installed or not on PATH." >&2
    exit 1
  }
}

# Colours, only when a terminal is attached.
if [ -t 1 ]; then
  C_RED=$'\033[31m'; C_GRN=$'\033[32m'; C_YEL=$'\033[33m'
  C_DIM=$'\033[2m';  C_B=$'\033[1m';   C_0=$'\033[0m'
else
  C_RED=""; C_GRN=""; C_YEL=""; C_DIM=""; C_B=""; C_0=""
fi
