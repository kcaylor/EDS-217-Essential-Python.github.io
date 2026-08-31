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

The extra work here is that a batch is where a stale page hides. `make render`
is incremental and `make preview` leaves `docs/` holding pages rendered at
different times, so a full pass needs a full render.

```bash
# after the edits are done
python3 tools/prose_guard.py verify --all
python3 tools/prose_guard.py desync --all
make verify                     # full render, runs every cell, resolves every
                                # data URL, runs the six gates
```

`make verify` never commits and never pushes. When it is clean:

```bash
git add course-materials/ docs/
git status                      # read it before committing
git commit -m "voice(2026): pass over days 4-7"
make publish
```

If you changed a layout, `_quarto.yml`, or anything that touches every page,
`make verify` already did a full render. If you skipped `make verify`, run
`make render-full` instead of `make render`, or `make publish` will stop you.

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
