# Publishing updates during the course

Two remotes, and the live site is the second one:

| remote | repo | what it is |
| --- | --- | --- |
| `origin` | `kcaylor/EDS-217-Essential-Python.github.io` | your fork |
| `live` | `EDS-217-Essential-Python/EDS-217-Essential-Python.github.io` | what students see, and what every 2026 data URL points at |

Pushing to `origin` alone changes nothing for students. `make publish` pushes to both.

Everything below runs from the repo root on your own machine. The targets
activate `eds217_2026` themselves, so no `conda activate` first.

---

## 1. One file, small edits

For a typo, a wrong number, a sentence that did not read well in the room.

```bash
make preview PAGE=day3          # optional, watches and reloads on save
# edit course-materials/day3.qmd
make render                     # incremental, rebuilds only what changed
git add course-materials/day3.qmd docs/
git commit -m "day3: fix the read_csv path in Part 2"
make publish
```

`make publish` asks before it pushes, then waits up to three minutes for the
Pages build and checks the live site.

**Before you commit**, if the file is a page students read:

```bash
python3 tools/prose_guard.py verify course-materials/day3.qmd
```

That proves you stayed inside prose and left code cells, YAML, link targets and
shortcodes byte-identical. If you edited an end-of-day practice or its key, also
run `python3 tools/prose_guard.py desync --all`, because the handout and the key
repeat each other's question text and rewording one side leaves students checking
against a different question.

---

## 2. A suite of files, voice or other revisions

You do not need a full rebuild for this. `make render` is incremental per page,
not per session: for every source in the render set it compares the source
mtime against its `docs/*.html` mtime and builds only the stale ones. Ten
edited files means ten pages rebuilt.

```bash
# after the edits are done
python3 tools/prose_guard.py verify --all
python3 tools/prose_guard.py desync --all
make render                     # only the pages you changed
python3 tools/run_cells.py course-materials/day4.qmd course-materials/day5.qmd
make gates
git add course-materials/ docs/
git status                      # read it before committing
git commit -m "voice(2026): pass over days 4-7"
make publish
```

`make verify` is the same render plus every cell, every data URL and the gates,
across the whole site. Use it when you have time and want certainty. Use the
sequence above when you want to be back in the room in five minutes. Neither
one commits or pushes, and `make publish` re-runs the render checks itself.

Two cases where incremental is not enough:

- **A site-wide file changed.** `build_docs.py` watches `_quarto.yml`,
  `meds-website-styles.scss` and `course-materials/assets/css/exercises.css`,
  and queues every page when one of them moves. `make render` still does the
  right thing here, it just will not be quick.
- **You previewed.** `make preview` writes into `docs/`, so a previewed page can
  be newer than its source while its content came from a mid-edit state. The
  timestamps look fine and `make render` will skip it. `touch` the sources you
  previewed, or run `make render-full`.

No page in `course-materials/` uses `{{< include >}}`, so there is no hidden
dependency that incremental rendering would miss.

### If the batch is a voice pass

Voice-pass pages go through the state machine, not free-hand. The ledger at
`tasks/2026-planning/prelaunch/voice-pass.json` is the only memory across
sessions, so a page edited outside it is lost work.

```bash
python3 tools/voicepass.py resume     # says where you are
python3 tools/voicepass.py status
```

One page at a time, committed on its own, and no page signed off with an open
finding.

---

## 3. Showing a lecture

The lecture notebooks in `course-materials/lectures/` are instructor material.
`_quarto.yml` excludes `course-materials/lectures/**` from the render set, so
they are not part of the site and nothing in this section publishes anything.

Each notebook sets its reveal.js options in the raw cell at the top:

```yaml
---
format:
  revealjs:
    slide-level: 3
jupyter: eds217_2026
---
```

To show one:

```bash
bash tools/run.sh quarto preview \
  course-materials/lectures/01_the_zen_of_python.ipynb --port 4218 --no-browser
```

`tools/run.sh` activates `eds217_2026`, which the `jupyter:` key needs in order
to execute the code cells. Port 4218 keeps a lecture off 4217, so a site preview
can stay open in another terminal. In Positron you can open the notebook and use
the Quarto extension's Preview button instead, as long as that window is already
running in the course environment.

`make preview` will not find these. `tools/preview.sh` searches for `.qmd` only.

In the deck, `s` opens presenter view with the next slide and a clock, `o` shows
the slide overview, `f` goes fullscreen and `Esc` returns to the slide.

`slide-level` sets which heading level starts a new slide. It differs by notebook
because the headings do:

| notebook | slide-level | what makes a slide |
| --- | --- | --- |
| `00_intro_to_python` | 3 | `##` sections, `###` slides |
| `01_the_zen_of_python` | 3 | one `##`, then `###` per aphorism |
| `02_helpGPT` | 3 | `###` per topic |
| `03-debugging` | 2 | only `#` and `##` are present |
| `04-next_steps` | 2 | the ten tips are `##` |
| `99_dry_vs_wet` | 3 | `##` sections, `###` slides |

Check the level against this table before adding headings to a lecture, or the
deck will split somewhere you did not intend.

Preview renders into `docs/`, the same as every other preview. Run `git status`
afterwards. Lecture output does not belong in the published site, so do not
commit it, and `make publish` refuses on a dirty working tree.

### The nbconvert path

Each notebook also still has the older per-cell `slideshow` metadata, which RISE
and nbconvert read and Quarto ignores.

```bash
bash tools/run.sh jupyter nbconvert --to slides --post serve \
  course-materials/lectures/01_the_zen_of_python.ipynb
```

That honors the slide, subslide and fragment tag on each cell, and it leaves
`docs/` alone. It does not use the site theme, and it writes
`01_the_zen_of_python.slides.html` beside the notebook, which you should delete
rather than commit. The YAML cell at the top of each notebook is tagged
`slide_type: skip`, so neither exporter prints it as text on the title slide.

RISE itself will not run in Positron, which has no classic Jupyter notebook
interface.

---

## What `make publish` refuses to do

It exits before pushing, with the reason, when:

- **`docs/` is not a complete render.** Run `make render`.
- **A page in `docs/` is older than its source.** This is the incremental-build
  gap, and it caught a stale page twice on 27 and 28 August. Run `make render`,
  or `make render-full` after a layout change.
- **Datasets under `docs/data` are not committed.** Without them every
  `read_csv` in the course returns 404. `git add -A docs`.
- **The working tree is dirty.** Commit or stash first. The one exception is
  `tasks/2026-planning/prelaunch/state.json`, which the checks rewrite and which
  does not affect the site.
- **A remote has commits you do not.** Reconcile before pushing.

---

## When git says another process is running

Nothing is running. A Cowork session left a lock file behind, because that mount
cannot delete files.

```bash
make unlock
```

`make publish` clears them itself as its first step.

---

## Quick reference

```
make preview PAGE=day3     live preview of one page
make render                render the pages whose source changed
make render-full           rebuild every page
make verify                render, cells, URLs, gates. Never pushes.
make gates                 the six quality gates on their own
make keys PAIR=eod-day3    one handout and key pair
make publish               guarded push to origin and live
make unlock                clear stale git locks
make verify-live           check what the published site is serving

bash tools/run.sh quarto preview course-materials/lectures/<nb>.ipynb --port 4218 --no-browser
                           show a lecture as reveal.js slides

python3 tools/prose_guard.py verify --all    nothing outside prose moved
python3 tools/prose_guard.py desync --all    exercise reworded, key not
python3 tools/prose_guard.py regions <file>  what is protected in one file
python3 tools/voicepass.py resume            the next page in the voice pass
```

---

## Right now

`course-materials/the-data-science-workflow.qmd` has three uncommitted lines.
`make publish` will stop on the dirty working tree until they are committed or
stashed.
