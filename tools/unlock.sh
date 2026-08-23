#!/usr/bin/env bash
# Clear the git lock files a Cowork session leaves behind.
#
# The mount that sessions write through cannot delete files, so every git
# command run from one leaves .git/index.lock or .git/HEAD.lock in place. Git
# then reports "Another git process seems to be running", which is not what has
# happened. This checks for a real git process before removing anything.

source "$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)/_env.sh"
eds217_clear_stale_locks || exit 1
if [ -z "$(ls .git/*.lock 2>/dev/null)" ]; then
  echo "${C_GRN}No lock file remains. git is free to write.${C_0}"
fi
