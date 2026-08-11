# EDS 217 2026: Endgame Plan

**Written 2026-08-10.** Supersedes the pacing in `work-plan.md`. Milestones M1–M3 there are
overdue and the week-by-week schedule no longer applies. The design in `2026-day-skeleton.md`
is unchanged and remains the specification.

## What changed

Kelly is working through the Kenya trip rather than freezing content on Aug 14. That converts
Aug 15–30 from a blackout into roughly two weeks of usable drafting time, most of it without
reliable connectivity. The plan is rebuilt around that.

## The one rule

**The site is teachable at every moment from Aug 14 onward.** Any day not yet rebuilt points at
its working 2025 materials with correct 2026 dates. Every push after Aug 14 replaces a working
day with a better day. Nothing is ever left half-wired. If connectivity, time, or health fails
at any point in the trip, the course still runs.

## Two gates

**Gate A — Fri Aug 14, before departure.**
Site live on the org repo and verified. All mechanical updates done. Day 1 and Day 2 final in
the 2026 design. Days 3–9 running 2025 materials with 2026 dates. Offline toolchain confirmed
working on the laptop.

**Gate B — Wed Aug 26, from Nairobi.**
Days 3–7 rebuilt to the skeleton, all six quality gates passed, full render clean, pushed and
verified. Days 6–7 hold a real reserve window over Sep 5–7 because they are not taught until
Sep 8–9.

## This week

Kelly's time is reserved for decisions. Drafting happens between blocks.

| When | Kelly | Claude |
|---|---|---|
| Mon Aug 10 | nothing required | mechanics: kernel rename, 2026 dates, navbar, index; wire Day 1 into the site; commit the Day 1 EOD |
| Tue Aug 11 | nothing required (3 meetings) | draft Day 2 in full; cache every dataset into `data/` and repoint materials |
| Wed Aug 12, 8:30–11:30 | **Day 2 review and sign-off.** The crux decision of the redesign | revisions from the block |
| Thu Aug 13 | ~30 min: read the flight packet | flight packet; full render; run the six quality gates; fix the `your-course-website.com` placeholders |
| Fri Aug 14, 13:00–16:00 | **Gate A.** Final read, push fork, sync org repo, verify live site | deploy support |

The Wed Aug 12 block is the only irreplaceable item on Kelly's calendar this week. If Day 2 is
not signed off before departure, the fallback in the skeleton applies: re-insert 2025's 2a/2b
sessions and slide the spine half a day.

## Offline prerequisites (all must be true before wheels up)

1. `eds217_2026` conda env installed on the laptop and verified by rendering one session
2. Every remote dataset cached into `data/`, with course materials reading the local copy
3. Full repo cloned with `docs/` intact, so incremental builds work
4. Quarto CLI present and working offline
5. Flight packet on disk, readable without a Claude session

Item 2 is the load-bearing one. 26 files currently fetch from 10 external hosts, including
`prism.oregonstate.edu` and `uszipcodelist.com`. Caching them fixes offline work and removes a
standing mid-course failure risk.

## The flight packet

One self-contained markdown brief per remaining day, written so drafting needs no network and no
Claude session. Each brief carries:

- the day's scope table from the skeleton, verbatim
- the exact 2025 source files to adapt, with what to cut and what to keep
- the sentence patterns the day owns
- the EOD task list with its Field Note budget
- for any afternoon-taught construct the EOD wants at WRITE depth, the rehearsal audit required
  by skeleton decision 10
- a drift checklist to self-run before committing

Kelly drafts into the qmd files directly. Polish, answer keys, and rendering happen in a session
whenever there is bandwidth.

## Order of work on the road

Teaching order, not risk order. The vocabulary budget and the rehearsal rule are sequential, so
Day 5 cannot be scoped correctly until Day 4 is fixed.

| Window | Location | Work |
|---|---|---|
| Sat Aug 15 | in transit (~24h) | Day 3: rebuild 3a from data questions; 3b/3c from 2025 5a; Banana EOD relocation and trims |
| Aug 16–19 | Nairobi | polish and push Day 3; draft Day 4 (relocations plus the new 4c functions session) |
| Aug 19–22 | Mpala, assume offline | Day 5: sessions 5a/5b/5c/5d and the new OpenAQ EOD, the largest new build |
| Aug 22–26 | Nairobi | push Days 4–5; build Day 6 including the 6b reshape session; redesign the Eurovision decade task |
| Aug 26–30 | Nairobi | Day 7 (mostly retained from 2025) plus the 7d project kickoff; run all gates; full render; **Gate B** |
| Sep 5–7 | home, Labor Day weekend | reserve window for Days 6–7 only |

## Scope cuts, in order, if a window is lost

1. 7d project kickoff session (fallback already designed: buffer, kickoff moves to Day 8 morning)
2. Day 6 rebuild (ship 2025's Day 6; costs the pivot_table and concat fix)
3. ~~Cheatsheet updates (ship 2025 versions)~~ **DONE 2026-08-11, not cut.** See
   "Cheatsheet revision" below.
4. Day 4 colab polish

Days 2, 3, and 5 are not cuttable. They carry the redesign.

## Cheatsheet revision (done 2026-08-11)

The 28 cheatsheets were audited against the per-day scope tables in `2026-day-skeleton.md` and
revised. **24 remain.** Kelly's decisions, and what was done under each:

1. **`data_aggregation.qmd` deleted.** It was a 14-line stub reading "To be added", linked from
   `1c_whole_game_1.qmd`, the first session of the first day. The link is removed from 1c, which
   already links `data_grouping.qmd` on the line above it.
2. **Three unreferenced pages retired**, and three kept behind a scope banner.
   Retired: `random_numbers.qmd`, `datetimeindex_vs_columns.qmd`, `emoji_visualizations.qmd`.
   The last of those fetched PNGs from `raw.githubusercontent.com` at render time and would have
   failed offline. Kept with a "Not used in EDS 217" callout: `sets.qmd`, `comprehensions.qmd`
   and `numpy.qmd`, now grouped under a new **Beyond EDS 217** heading in `cheatsheets.qmd`.
3. **`seaborn.qmd` and `chart_customization.qmd` restructured**, in-scope material first and the
   rest under a "Beyond EDS 217" heading shown as syntax only. All five `sns.load_dataset` calls
   replaced with `data/penguins.csv` read from the course site.
4. **Surgical scope trim** rather than a full pass over all sixteen over-scope files.
   `matplotlib.qmd` was rewritten from the `fig, ax` API to the `plt.*` API Day 7 actually
   teaches, which was the worst mismatch in the set. `dictionaries.qmd` was cut back to literals
   and lookup, per the Day 2 scope row that says "NOT methods, NOT iteration, NOT nesting", and
   gained a closing section on the two places the course uses a dict (`rename` and `.agg`).
   `control_flows.qmd` was cut to `if/elif/else` plus loops, and gained the `for name, group in`
   form from 5d. numpy was stripped from every file that only used it to build demo data.
   `workflow_methods.qmd` lost its `plot()`, `corr()` and `cov()` rows, and gained a note saying
   the Visualizing column is empty on purpose.

Also fixed in the same pass: the `lambda` section in `pandas_series.qmd` (quality gate 5), the
`6b_advanced_data_manipulation` heading in `data_merging.qmd`, an `astype(`string`)` typo and a
numpy-free z-score in `data_cleaning.qmd`, two invalid `::: {type="note"}` divs in `print.qmd`,
a `DataFrameGroupBy.apply` FutureWarning in `data_grouping.qmd`, and the missing comprehensions
cheatsheet link in `5d_loops_over_groups.qmd` that the Day 5 scope table had promised.

**Verification:** 150 python cells across the 15 executable cheatsheets, 148 clean. The two
failures are the IPython magics in `JupyterLab.qmd` (`%whos`, `!ls`), which are valid under the
Jupyter kernel Quarto renders with and cannot run under `run_cells.py`'s plain `exec`. Zero
em-dashes, zero `lambda`, zero `load_dataset`, zero pandas `.plot` accessor references, zero
references to retired files.

**Three corrections to the audit that preceded this pass**, worth keeping: the pandas `.plot`
accessor appeared in one file rather than four (the other three were `plt.plot`/`ax.plot`, which
is in scope); `sets.qmd` and `comprehensions.qmd` had no inbound link from any 2026 file, only
from 2025 orphans; and no cheatsheet ever read the four sibling CSVs, so nothing needed to move
into `data/`.

## Pre-launch checklist

Run once the restructuring is done and the revisions are settled, before the deploy. These
are cleanup items that would be premature while days are still moving.

- [ ] **Retire the superseded 2025 files from the render.** They are unlinked from the navbar
      and the day pages, but Quarto still builds them, so a student can reach a page teaching
      material we cut. Known orphans: `2d_list_comprehensions.qmd` and its notes, `2a_lists`,
      `2b_dictionaries`, `2c_lists_dictionaries_sets`, the 2025 `1a`-`1d`, plus whatever
      Days 3-7 orphan as they are rebuilt. Day 5 added four: `live-coding/5a_selecting_and_filtering.qmd`
      and its notes, `interactive-sessions/5b_cleaning_data.qmd`, and
      `coding-colabs/5c_cleaning_data.qmd`. Day 6 added six:
      `interactive-sessions/6a_grouping_joining_sorting.qmd` and both its `_old` siblings,
      `coding-colabs/6b_advanced_data_manipulation.qmd` and `coding-colabs/6b_preprocess.ipynb`,
      and `eod-practice/eod-day6.qmd` with its `answer-keys/eod-day6-key.qmd`. Day 7 added five:
      `interactive-sessions/7a_visualizations_1.qmd`, `interactive-sessions/7b_visualizations_2.qmd`,
      `coding-colabs/7c_visualizations.qmd`, and `eod-practice/eod-day7.qmd` with its
      `answer-keys/eod-day7-key.qmd`.

      **All seven 2025 EODs and all seven 2025 EOD keys are orphans, and Days 1 to 5 were not
      named above.** Verified 2026-08-11: no day page and no navbar entry links any of
      `eod-practice/eod-day1.qmd`, `eod-day1-draft.qmd`, `eod-day2.qmd`, `eod-day3.qmd`,
      `eod-day4.qmd`, `eod-day5.qmd`, `eod-day6.qmd` or `eod-day7.qmd`. Their keys,
      `answer-keys/eod-day1-key.qmd` through `eod-day7-key.qmd`, are linked only from
      `answer_keys.qmd`. **`eod-day2-key.qmd` is where the last `lambda` in the course lives**,
      so this pair in particular must not be skipped. The 2026 EODs have no answer keys at all,
      which is why `answer_keys.qmd` needs rewriting rather than repointing.

      Three of the Day 5
      four, two of the Day 6 six and at least one of the Day 7 five are still linked from
      `answer-keys/answer_keys.qmd`, **so that page needs revising in the same pass**, not just the
      render config. `7a_visualizations_1.qmd` also links its own retired sibling. Decide per file: delete, or exclude via the
      `render:` block in `_quarto.yml`. Do this last, since each rebuilt day adds to the list.
- [ ] **Replace the four Day 7 placeholder images with bespoke panels.** Day 7 claimed four
      existing files and downloaded one. `7a_matplotlib.qmd` uses `images/matplotlib_panda.jpeg`
      and `7b_seaborn.qmd` uses `images/panda_seaborn.jpeg`; both were generated for this purpose
      and are fine as they stand, though `panda_seaborn.jpeg` (a panda at a press-conference
      podium) fits "presenting a result" better than it fits seaborn. Two are genuine
      placeholders: the 7c colab uses `../images/horst-samples.jpg` (Allison Horst's two
      distributions, on point but not house style) and 7d uses `images/ds_friends.jpg` (the
      dancing-tools cartoon). `eod-practice/images/hardiness_panda.jpeg` is the 2025 EOD's
      gardening panda, pulled off the MidJourney CDN and committed so the page renders offline;
      it is correct and needs nothing.

      Prompts, if bespoke panels are wanted:

      - 7c: *A cartoon panda in an Antarctic field station, three penguins of visibly different
        sizes lined up beside a set of calipers, painterly, square, no lettering.*
      - 7d: *A cartoon panda standing in front of a whiteboard covered in question marks and one
        circled question, a laptop open beside it, painterly, square, no lettering.*

- [ ] **Generate the Day 4 EOD header image.** `eod-day4-2026.qmd` currently points at
      `../images/panda.jpeg`, a stock photo used as a placeholder. Every other EOD carries a
      themed MidJourney panda in `eod-practice/images/`. Generate one, save it as
      `course-materials/eod-practice/images/microplastics_panda.jpeg`, then replace lines 15-21
      of the qmd with:

      ```
      ::: {style="width: 80%; margin: auto;"}
      ![](images/microplastics_panda.jpeg)
      :::

      :::{.gray-text .center-text}
      *A cartoon panda in waders picks flecks of plastic out of a plankton net and sorts them
      into labelled sample jars.* [MidJourney 5](https://www.midjourney.com)

      :::
      ```

      Note the path changes from `../images/` to `images/`, since the new file lives in
      `eod-practice/images/` alongside `banana_panda.jpeg`.

      Prompt:

      > a cartoon panda in yellow waders and an orange life vest stands on the deck of a small
      > research vessel, hauling a fine-mesh plankton net up over the rail; he is picking tiny
      > bright fragments of plastic out of the net with tweezers and dropping them into labelled
      > glass sample jars lined up on a crate beside him; grey open ocean and overcast sky
      > behind him; painterly illustration, muted palette with a few saturated plastic colours,
      > warm and gently comic, no text --ar 1:1 --style raw

      The house style across the other EOD images is one anthropomorphic panda doing the thing
      the exercise is about, painterly rather than photographic, square, no lettering.
- [ ] **Generate the Day 5 EOD header image.** Same situation as Day 4: `eod-day5-2026.qmd`
      points at `../images/panda.jpeg` as a placeholder. Save the result as
      `course-materials/eod-practice/images/airquality_panda.jpeg` and replace lines 15-21 of the
      qmd with:

      ```
      ::: {style="width: 80%; margin: auto;"}
      ![](images/airquality_panda.jpeg)
      :::

      :::{.gray-text .center-text}
      *A cartoon panda on a rooftop checks an air quality monitor while the afternoon haze
      builds behind him.* [MidJourney 5](https://www.midjourney.com)

      :::
      ```

      Prompt:

      > a cartoon panda in a field technician's vest stands on a flat building rooftop beside a
      > white cylindrical air quality monitor on a tripod, reading a clipboard and adjusting a
      > dial on the instrument; behind him a low coastal city and ocean under a hazy yellow
      > early-afternoon sky; painterly illustration, warm muted palette, gently comic, no text
      > --ar 1:1 --style raw

- [ ] **Fix the broken image in the 2d live-coding page.**
      `live-coding/2d_lists_and_dicts.qmd` line 13 references `images/collections.jpg`, but
      `live-coding/` has no `images/` directory, only `assets/`. This is a **Day 2 page, which is
      otherwise signed off**, so it is worth checking before the deploy rather than after. Either
      point it at `../images/collections.jpg` or copy the file into `live-coding/assets/`.

- [ ] **Generate four Day 6 images.** The collision with `day5.qmd` is resolved, but every Day 6
      panel is now a placeholder pulled from the 2025 stock. `dates.jpeg` went to `6c_dates.qmd`,
      which is the one assignment worth keeping. The other four want bespoke panels in house style
      (a single anthropomorphic panda, painterly, square, no lettering):

      - `course-materials/day6.qmd`, currently `images/structured-data.png` — a panda standing
        between two piles of paper, one tall and narrow, one short and wide, holding one sheet up
        to compare them
      - `6a_joining_data.qmd`, currently `../images/panda.jpeg` — a panda fitting two halves of a
        torn map together on a table so the roads line up across the seam
      - `6b_reshaping_data.qmd`, currently `../images/dataframes.jpeg` — a panda turning a long
        paper scroll sideways on a light table so its rows become columns
      - `6d_two_table_exercise.qmd`, currently `../images/towersensors.jpeg` — a panda at a desk
        with two long paper strip-charts of different lengths, sliding them until the dates align

      `panda_seaborn.jpeg` and `matplotlib_panda.jpeg` remain reserved for Day 7.

- [ ] **Fix the broken image in the 2c colab.** `coding-colabs/2c_exploring_unfamiliar_data.qmd`
      references `images/collections.jpeg`, but there is no `coding-colabs/images/` directory.
      One-line fix: `../images/collections.jpeg`. The Day 3 and Day 4 colabs already use
      `../images/`.
- [x] **DONE 2026-08-11. Removed all 89 tracked `.fuse_hidden*` files and added
      `.fuse_hidden*` to `.gitignore`.** Every one was a stale duplicate of a live file: 54
      course pages still carrying `jupyter: eds217_2025`, plus shadow copies of
      `environment.yml`, `environment-2026.yml`, `build_docs.py`, `README.md`, `BUILD_DOCS.md`,
      `FAST_SETUP.md` and `KERNEL_FIX.md`. All are recoverable from git history. Original note
      follows, for the reasoning.

      ~~Remove the 61 remaining tracked `.fuse_hidden*` files.~~ These are stale byte-copies of
      course files left by the Cowork mount, committed at some point and still carrying
      `jupyter: eds217_2025`. They are invisible to Quarto but they match every grep-based
      quality gate, which is how they were found: the gate-5 `lambda` search and the
      `load_dataset` search both reported failures that were entirely these shadow files. The 28
      in `course-materials/cheatsheets/` were removed on 2026-08-11. The rest are spread across
      `answer-keys` (10), `interactive-sessions` (21), `eod-practice` (8), `lectures` (6),
      `live-coding` (4), `coding-colabs` (3), `course-materials` (1) and the repo root (8).
      Add `.fuse_hidden*` to `.gitignore` in the same pass. Note that `rm` fails through the
      Cowork mount, so move them into the gitignored `_to_delete/` and let `git add -A` record
      the deletion.
- [ ] **Last `lambda` in the course materials: no separate work needed, but do not lose it.**
      `answer-keys/eod-day2-key.qmd` line 164 uses `max(..., key=lambda x: ...)`. Checked
      2026-08-11: **that file is a 2025 orphan, not a 2026 file.** Its subtitle is "Python Data
      Structures Practice" and it is the key to `eod-practice/eod-day2.qmd`, the 2025 Day 2 EOD.
      The 2026 Day 2 EOD is `eod-day2-2026.qmd`, the Toolik data biography, and it has no answer
      key. So the last `lambda` disappears the moment the orphan sweep above runs, provided that
      sweep covers the 2025 EOD and key pairs, which it must now do explicitly (see the expanded
      list). `interactive-sessions/6b_grouping_joining_sorting_2_old.qmd` line 428 has the other
      one and is already on the list. **After the sweep, re-run gate 5 to confirm it passes.**
- [ ] **Four orphan CSVs in `course-materials/cheatsheets/`.** `ocean_temperatures.csv` (316 KB),
      `sample_time_data.csv`, `temp_data.csv` and `output.csv` are tracked, sit outside `data/`,
      and are read by nothing. The last two were render artifacts: `timeseries.qmd` used to write
      and re-read `temp_data.csv`, which was fixed on 2026-08-11 by round-tripping through
      `StringIO` instead. **`pandas_dataframes.qmd` still calls `df.to_csv('output.csv')`**, so it
      writes a file into whatever the working directory happens to be every time it renders.
      Either point it at a throwaway path or make it a non-executing block.
- [ ] **Check `JupyterLab.qmd` and `setting_up_python.qmd` against the 2026 setup.** The first
      references `https://workbench-1.bren.ucsb.edu`; confirm that is still the Bren workbench
      address. The second installs a package list by hand; confirm it agrees with
      `environment-2026.yml`. Neither is a scope problem, both are the kind of thing a student
      hits in the first hour of Day 1.
- [ ] Run `python tools/run_cells.py` over every 2026 session and EOD.
- [ ] Run `python tools/warm_cache.py`; expect every course-site URL to resolve.
- [ ] Full `python build_docs.py --full` with no errors.
- [ ] Update the syllabus Google Doc link and TA information.
- [ ] Push to `origin`, then `live`, then verify the site serves `data/` correctly.

## Quality gates (unchanged, from work-plan.md)

1. Every construct traces to a day scope table in `2026-day-skeleton.md`
2. Rehearsal rule holds. For **every** construct at WRITE depth in an EOD, name the session and
   the specific task where students wrote it unaided. If you cannot name one, it is not WRITE.
   Afternoon-taught constructs additionally need the decision 10 exemption, with its audit table
   recorded in the day's section of the skeleton. (Amended 2026-08-11; was "afternoon-taught
   implies ADAPT at most in the same-day EOD".)
3. At most 2 Field Notes per EOD
4. Handout and answer key agree: no key-only tasks, names match
5. `grep` for `lambda` returns nothing in course materials (currently fails: 3 files)
6. 2025 EOD alignment checklist run and archived
