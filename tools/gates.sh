#!/usr/bin/env bash
# The six EDS 217 quality gates, from tasks/2026-planning/endgame-plan.md.
#
# Four are mechanical and this script runs them. Two depend on reading the
# material and are reported as human gates with a pointer to where the reading
# was recorded. The script never reports a human gate as passing, because it did
# not check one.
#
# Exit status: 0 when every mechanical gate passes, 1 otherwise.

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"

FAILED=0
pass() { echo "${C_GRN}PASS${C_0}   $1"; }
fail() { echo "${C_RED}FAIL${C_0}   $1"; FAILED=1; }
human() { echo "${C_YEL}HUMAN${C_0}  $1"; }
detail() { echo "       ${C_DIM}$1${C_0}"; }

echo "${C_B}EDS 217 quality gates${C_0}"
echo

# --- Gate 1 ---------------------------------------------------------------
human "Gate 1  every construct traces to a day scope table"
detail "Deciding what counts as a construct and matching it to a prose scope"
detail "table is a reading task. Recorded per day in"
detail "tasks/2026-planning/2026-day-skeleton.md."

# --- Gate 2 ---------------------------------------------------------------
human "Gate 2  the rehearsal rule holds for every WRITE-depth construct"
detail "Depth labels and rehearsal claims are prose. Afternoon-taught constructs"
detail "additionally need the decision 10 exemption and its audit table, also in"
detail "2026-day-skeleton.md."

# --- Gate 3 ---------------------------------------------------------------
G3=0
G3LINES=""
for d in 1 2 3 4 5 6 7; do
  f="course-materials/eod-practice/eod-day${d}-2026.qmd"
  [ -f "$f" ] || { G3=1; G3LINES="${G3LINES}\n       day ${d}: ${f} is missing"; continue; }
  n=$(grep -c 'callout-tip title="🧭 Field Note' "$f" || true)
  G3LINES="${G3LINES}\n       day ${d}: ${n}"
  [ "$n" -gt 2 ] && G3=1
done
if [ "$G3" -eq 0 ]; then
  pass "Gate 3  at most two Field Notes per end-of-day activity"
else
  fail "Gate 3  at most two Field Notes per end-of-day activity"
fi
printf "%b\n" "${C_DIM}${G3LINES}${C_0}"

# --- Gate 4 ---------------------------------------------------------------
G4=0
G4LINES=""
for d in 2 3 4 5 6 7; do
  h="course-materials/eod-practice/eod-day${d}-2026.qmd"
  k="course-materials/answer-keys/eod-day${d}-2026-key.qmd"
  if [ ! -f "$h" ] || [ ! -f "$k" ]; then
    G4=1; G4LINES="${G4LINES}\n       day ${d}: a file is missing"; continue
  fi
  if diff -q <(grep -E '^## Part' "$h") <(grep -E '^## Part' "$k") >/dev/null; then
    n=$(grep -cE '^## Part' "$h" || true)
    G4LINES="${G4LINES}\n       day ${d}: ${n} parts, handout and key agree"
  else
    G4=1
    G4LINES="${G4LINES}\n       day ${d}: handout and key disagree on part headings"
  fi
done
G4LINES="${G4LINES}\n       day 1: structured without Part headings, read it by hand"
if [ "$G4" -eq 0 ]; then
  pass "Gate 4  handout and answer key agree, structurally"
else
  fail "Gate 4  handout and answer key agree, structurally"
fi
printf "%b\n" "${C_DIM}${G4LINES}${C_0}"
detail "The structural half is mechanical. Task-by-task agreement is not, because"
detail "handouts number tasks and keys group them under parts."

# --- Gate 5 ---------------------------------------------------------------
HITS=$(grep -rnE 'lambda[[:alnum:]_, *]*:' course-materials \
  --include='*.qmd' --include='*.ipynb' --exclude-dir='.ipynb_checkpoints' || true)
if [ -z "$HITS" ]; then
  pass "Gate 5  no lambda anywhere in the course materials"
  detail "Pattern requires a parameter list and a colon, so backticked prose about"
  detail "lambda does not match."
else
  fail "Gate 5  no lambda anywhere in the course materials"
  printf '       %s\n' "$HITS"
fi

# --- Gate 6 ---------------------------------------------------------------
G6=0
for f in tasks/course-audit/eod-alignment-checklist.md \
         tasks/course-audit/day{1,2,3,4,5,6,7}-eod-alignment-audit.md; do
  [ -f "$f" ] || { G6=1; detail "missing: $f"; }
done
if [ "$G6" -eq 0 ]; then
  pass "Gate 6  the 2025 alignment checklist and all seven per-day audits are archived"
else
  fail "Gate 6  the 2025 alignment checklist and all seven per-day audits are archived"
fi
detail "File existence only. Whether the checklist was applied is a reading task."

echo
if [ "$FAILED" -eq 0 ]; then
  echo "${C_GRN}${C_B}Four mechanical gates pass. Two human gates are noted above.${C_0}"
else
  echo "${C_RED}${C_B}At least one mechanical gate is failing.${C_0}"
fi
exit "$FAILED"
