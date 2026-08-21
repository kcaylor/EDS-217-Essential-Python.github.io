#!/usr/bin/env bash
# Live preview of the course site.
#
#   tools/preview.sh              the whole site
#   tools/preview.sh day3         one day page and nothing else
#   tools/preview.sh 5a_grouping  any page whose filename contains this
#
# Quarto watches the source and reloads the browser on save, so this is the
# loop for reading a page, editing the qmd, and seeing the result. It renders
# into a scratch directory rather than docs/, so a preview can never leave the
# published output in a half-built state.

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"
eds217_activate
eds217_need quarto

PORT="${EDS217_PORT:-4217}"

if [ $# -eq 0 ]; then
  echo "${C_B}Previewing the whole site${C_0} on http://localhost:${PORT}"
  echo "${C_DIM}First build takes a few minutes. Later saves reload in seconds.${C_0}"
  exec quarto preview --port "$PORT" --no-browser
fi

PATTERN="$1"
MATCHES=$(find . -name "*${PATTERN}*.qmd" \
  -not -path "./_to_delete/*" -not -path "./docs/*" \
  -not -path "./nbs/*" -not -path "./extra_files/*" | sort)
COUNT=$(printf '%s\n' "$MATCHES" | grep -c . || true)

if [ "$COUNT" -eq 0 ]; then
  echo "${C_RED}No page matches '${PATTERN}'.${C_0}" >&2
  exit 1
fi
if [ "$COUNT" -gt 1 ]; then
  echo "${C_YEL}'${PATTERN}' matches ${COUNT} pages:${C_0}"
  printf '  %s\n' $MATCHES
  echo "Narrow the pattern."
  exit 1
fi

echo "${C_B}Previewing${C_0} ${MATCHES} on http://localhost:${PORT}"
exec quarto preview "$MATCHES" --port "$PORT" --no-browser
