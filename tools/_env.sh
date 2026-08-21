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

eds217_activate() {
  if [ "${CONDA_DEFAULT_ENV:-}" = "$ENV_NAME" ]; then
    return 0
  fi
  if ! command -v conda >/dev/null 2>&1; then
    echo "conda is not on PATH. Open a shell where conda is initialised, or set" >&2
    echo "EDS217_SKIP_ENV=1 to run without it." >&2
    [ "${EDS217_SKIP_ENV:-0}" = "1" ] && return 0
    exit 1
  fi
  # shellcheck disable=SC1090
  eval "$(conda shell.bash hook)"
  if ! conda env list | grep -qE "^${ENV_NAME}[[:space:]]"; then
    echo "conda environment '${ENV_NAME}' does not exist." >&2
    echo "Create it with: conda env create -f environment-2026.yml" >&2
    exit 1
  fi
  conda activate "$ENV_NAME"
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
