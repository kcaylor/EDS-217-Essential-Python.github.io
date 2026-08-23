#!/usr/bin/env bash
# Run a command inside the course environment.
#
#   bash tools/run.sh python tools/run_cells.py file.qmd
#
# The Makefile routes every python target through here. Without it, `make`
# inherits whatever environment the shell happens to be in, and a missing
# package then shows up as dozens of failing cells that look like defects in the
# course materials rather than a shell that never activated eds217_2026.

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"
eds217_activate
exec "$@"
