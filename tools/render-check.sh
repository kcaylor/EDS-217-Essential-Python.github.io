#!/usr/bin/env bash
# Full render, then the verification battery, then the punch-list checks.
#
# Run this before any push. It is the one command that answers "is the site in a
# state I can publish". It never pushes and never commits.

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"
eds217_activate
eds217_need quarto

STEP=0
step() { STEP=$((STEP+1)); echo; echo "${C_B}[$STEP] $1${C_0}"; }
FAILED=0
note_fail() { echo "${C_RED}   that step failed${C_0}"; FAILED=1; }

step "Full render"
python build_docs.py --full || note_fail

step "Every executable cell on a page the site renders"
FILES=$(python tools/prelaunch_checks.py --render-set | grep '\.qmd$')
python tools/run_cells.py $FILES || note_fail

step "Every data URL resolves"
python tools/warm_cache.py || note_fail

step "The six quality gates"
bash tools/gates.sh || note_fail

step "The pre-launch punch list"
python tools/prelaunch.py check --all || true
python tools/prelaunch.py status

echo
if [ "$FAILED" -eq 0 ]; then
  echo "${C_GRN}${C_B}Render and verification battery are clean.${C_0}"
  echo "Next: review docs/, then  make publish"
else
  echo "${C_RED}${C_B}Something above failed. Do not push.${C_0}"
fi
exit "$FAILED"
