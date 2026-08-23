# EDS 217 pre-launch. One place for everything you run between now and Day 1.
#
#   make            this list
#   make status     what is left on the punch list
#   make next       the next item you can start
#   make board      rebuild the dashboard and open it
#   make preview    live preview of the whole site
#   make preview PAGE=day3     live preview of one page
#   make render     full render into docs/
#   make verify     render, run every cell, resolve every URL, run the gates
#   make publish    guarded push to both remotes
#
# Every target runs in the eds217_2026 conda environment. Nothing here commits
# or pushes except `publish`, which asks first.

SHELL := /bin/bash

# Every python target runs inside eds217_2026. See tools/run.sh for why.
RUN := bash tools/run.sh
PAGE ?=
DAY ?=

.DEFAULT_GOAL := help
.PHONY: help status next show board dashboard preview render verify verify-live \
        gates cells cache check certify publish env clean-preview

help:
	@echo ""
	@echo "  EDS 217 pre-launch"
	@echo ""
	@echo "  Where things stand"
	@echo "    make status              the punch list, open items only"
	@echo "    make status-all          the punch list, everything"
	@echo "    make next                the next item you can start, in full"
	@echo "    make show ID=D6          one item in full"
	@echo "    make board               rebuild the dashboard and open it"
	@echo ""
	@echo "  Reading and editing"
	@echo "    make preview             live preview of the whole site"
	@echo "    make preview PAGE=day3   live preview of one page"
	@echo ""
	@echo "  Verifying"
	@echo "    make check               run every punch-list verification"
	@echo "    make gates               the six quality gates"
	@echo "    make cells               execute every code cell in the 2026 corpus"
	@echo "    make cache               confirm every data URL resolves"
	@echo "    make render              full render into docs/"
	@echo "    make verify              render plus all of the above"
	@echo "    make verify-live         check the published site"
	@echo ""
	@echo "  Signing off and publishing"
	@echo "    make certify ID=D6 NOTE=\"what you confirmed\""
	@echo "    make publish             guarded push to origin and live"
	@echo ""
	@echo "  When git says another process is running"
	@echo "    make unlock              clear the lock files a session left behind"
	@echo ""

status:
	@$(RUN) python tools/prelaunch.py status

status-all:
	@$(RUN) python tools/prelaunch.py status --all

next:
	@$(RUN) python tools/prelaunch.py next

show:
	@test -n "$(ID)" || { echo "usage: make show ID=D6"; exit 1; }
	@$(RUN) python tools/prelaunch.py show $(ID)

dashboard:
	@$(RUN) python tools/prelaunch.py dashboard

board:
	@$(RUN) python tools/prelaunch.py dashboard --open

preview:
	@bash tools/preview.sh $(PAGE)

render:
	@$(RUN) python build_docs.py --full

check:
	@$(RUN) python tools/prelaunch.py check --all
	@$(RUN) python tools/prelaunch.py dashboard

gates:
	@bash tools/gates.sh

cells:
	@$(RUN) python tools/run_cells.py $$($(RUN) python tools/prelaunch_checks.py --render-set | grep '\.qmd$$')

cache:
	@$(RUN) python tools/warm_cache.py

verify:
	@bash tools/render-check.sh

verify-live:
	@$(RUN) python tools/prelaunch_checks.py d8_live_site

certify:
	@test -n "$(ID)" || { echo "usage: make certify ID=D6 NOTE=\"...\""; exit 1; }
	@test -n "$(NOTE)" || { echo "a sign-off needs a NOTE saying what you confirmed"; exit 1; }
	@$(RUN) python tools/prelaunch.py certify $(ID) -n "$(NOTE)"
	@$(RUN) python tools/prelaunch.py dashboard

unlock:
	@bash tools/unlock.sh

publish:
	@bash tools/publish.sh

env:
	@echo "conda env: $${CONDA_DEFAULT_ENV:-none}"
	@$(RUN) python -c "import sys, pandas, numpy, matplotlib, seaborn; \
	print('python', sys.version.split()[0]); \
	print('pandas', pandas.__version__); print('numpy', numpy.__version__); \
	print('matplotlib', matplotlib.__version__); print('seaborn', seaborn.__version__)"
	@quarto --version | sed 's/^/quarto /'
