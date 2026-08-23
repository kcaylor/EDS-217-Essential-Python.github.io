#!/usr/bin/env bash
# Guarded publish of the course site.
#
# The site is served from docs/ on main, from two repos: origin (Kelly's fork)
# and live (the EDS-217-Essential-Python org repo, which is the host every 2026
# data URL points at). Pushing to origin alone does not update what students see.
#
# This script refuses to push a render that is not complete, because the failure
# mode it exists to prevent is publishing an empty docs/ over a working site.

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"

say()  { echo "${C_B}$1${C_0}"; }
bad()  { echo "${C_RED}$1${C_0}" >&2; }
ok()   { echo "${C_GRN}$1${C_0}"; }

say "1. Clearing any lock a session left behind"
eds217_clear_stale_locks || exit 1

say ""
say "2. Checking the render"
if ! python tools/prelaunch_checks.py d5_render_complete; then
  bad "docs/ does not hold a complete render. Run 'make render' first."
  exit 1
fi
if ! python tools/prelaunch_checks.py d6_docs_data_tracked; then
  bad "Datasets under docs/data are not committed."
  bad "Without them every read_csv in the course returns 404. Stage them:"
  bad "  git add -A docs && git commit -m 'render(2026): rebuild the site and publish data/'"
  exit 1
fi
ok "The render is complete and the datasets are committed."

say ""
say "3. Local git hooks"
if ! python tools/prelaunch_checks.py d9_push_hooks; then
  bad "A local hook would refuse to run and stop the push."
  exit 1
fi
ok "No hook will interfere."

say ""
say "4. Working tree"
if [ -n "$(git status --porcelain)" ]; then
  git status --short | head -20
  bad "Commit or stash the above before publishing."
  exit 1
fi
ok "Clean."

say ""
say "5. Remote state"
git fetch --all --prune
for remote in origin live; do
  behind=$(git rev-list --count "HEAD..${remote}/main" 2>/dev/null || echo "?")
  ahead=$(git rev-list --count "${remote}/main..HEAD" 2>/dev/null || echo "?")
  echo "   ${remote}: ${ahead} ahead, ${behind} behind"
  if [ "$behind" != "0" ]; then
    bad "${remote} has commits you do not have. Reconcile before pushing."
    exit 1
  fi
done

say ""
say "6. Dry run"
git push --dry-run origin main
git push --dry-run live main
ok "Both remotes accept a fast-forward."

say ""
read -r -p "Push to origin and live now? [y/N] " reply
case "$reply" in
  [yY]*) ;;
  *) echo "Nothing pushed."; exit 0 ;;
esac

git push origin main
git push live main
ok "Pushed."

say ""
say "7. Waiting for the Pages build, then checking the live site"
for i in 1 2 3 4 5 6; do
  sleep 30
  echo "   attempt ${i}"
  if python tools/prelaunch_checks.py d8_live_site; then
    ok "The published site is the 2026 build and serves data/."
    echo "Certify it with:"
    echo "  python tools/prelaunch.py certify D8 -n \"pushed and verified live\""
    exit 0
  fi
done
bad "The site has not caught up after three minutes."
bad "Check Settings then Pages on the org repo: the source should be main, folder /docs."
exit 1
