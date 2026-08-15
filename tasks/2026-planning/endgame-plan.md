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

**Gate A. Fri Aug 14, before departure.**
Site live on the org repo and verified. All mechanical updates done. Day 1 and Day 2 final in
the 2026 design. Days 3–9 running 2025 materials with 2026 dates. Offline toolchain confirmed
working on the laptop.

**Gate B. Wed Aug 26, from Nairobi.**
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

## Answer keys for the 2026 activities (COMPLETE 2026-08-11, 12 of 12 built)

Kelly raised this after the cheatsheet pass: the 2025 course had answer keys, students used them
to check their work, and the 2026 activities had none.

**The enabling fact:** all seven 2026 EODs and all five 2026 colabs already carried a complete,
verified answer-code solution, hidden by `execute: echo: false, include: false`. The code half of
a key already existed and only had to be surfaced. What did not exist was the prose, and that is
the half a student cannot check alone.

### Kelly's three decisions, 2026-08-11

1. **Content: code plus written answers.** Not code alone.
2. **Coverage: all 12 files.** Seven EODs plus the five colabs.
3. **Release: published from the start**, linked from the site, as in 2025.

### What was built

All twelve keys live in `answer-keys/`, named `<source-stem>-key.qmd`. **228 of 228 python cells
run clean** under `tools/run_cells.py` on Kelly's machine (pandas 2.3.3, seaborn 0.13.2), and the
em-dash count is zero in every one.

| Key | Cells |
|-----|-------|
| `eod-day1-2026-key.qmd` | 15 |
| `eod-day2-2026-key.qmd` | 17 |
| `eod-day3-2026-key.qmd` | 20 (the reference implementation, commit 714c233) |
| `eod-day4-2026-key.qmd` | 26 |
| `eod-day5-2026-key.qmd` | 20 |
| `eod-day6-2026-key.qmd` | 16 |
| `eod-day7-2026-key.qmd` | 23 |
| `3d_ranking_questions-key.qmd` | 19 |
| `4d_cleaning_messy_data-key.qmd` | 24 |
| `5c_grouped_comparisons-key.qmd` | 16 |
| `6d_two_table_exercise-key.qmd` | 15 |
| `7c_penguins-key.qmd` | 17 |

Every key follows the Day 3 shape: front matter flipping the two execute directives and adding
`search: false`, an opening `.callout-important` on how to use the key with a back-link, questions
reproduced verbatim in bold, a `:::{.callout-note title="✅ Answer"}` on every interpretive
question, a closing "Where the marks are" list, and a second back-link. Narrative, images, Field
Notes, R-versus-Python tips and wrap-ups are dropped.

**Method used throughout:** every number was computed before any answer was written, by running
the exercise's whole hidden solution through the offline cache and printing every figure the
questions ask about. No answer was written from memory or by paraphrasing the exercise's own prose.

### Wiring, done in the same pass

- **`answer_keys.qmd` rewritten** around the twelve 2026 keys, as two tables (colabs, end-of-day
  practice) with the exercise and its key side by side. Every 2025 link is gone, which discharges
  the "revising answer_keys.qmd" half of the orphan-retirement item below. It explains why the
  Day 2 colab has no key, and it states the "say what the number means" standard once, centrally.
- **Each key linked from its day page.** `day1.qmd` through `day7.qmd` gained an `## Answer keys`
  section between End-of-day practice and Additional Resources.
- **`_quarto.yml` navbar gained a `🔑 answer keys` entry** pointing at `answer_keys.qmd`, which
  was previously unreachable from anywhere on the site. Every key keeps `search: false`, so the
  navbar is the deliberate route in and a student cannot stumble onto an answer while searching.

### Decided 2026-08-11: no forward links, and no key URLs on the site

**The exercises do not link forward to their keys, and they should not.** Every key links back to
its exercise; nothing links the other way. Kelly's reasoning: he will give out key URLs in class
as he judges each one is due, so that students do not treat a key as a crutch available the moment
they get stuck. A forward link on the exercise page would put the answer one click away while the
exercise is still being worked, which is precisely the behaviour the timing is meant to prevent.

This does not need revisiting. If a future pass adds a key, it gets a back-link only.

The `🔑 answer keys` navbar entry and `answer_keys.qmd` remain, since Kelly wants the keys
published and reachable once he has named them. `search: false` on every key means a student
cannot arrive at one by searching the site.

### Errors found in the source exercises, corrected 2026-08-11

Building a key runs the exercise honestly for the first time since it was written, so five factual
slips surfaced, plus one design problem and one house-style nit. **All seven were corrected on
2026-08-11**, in a single deliberate pass with the "do not edit Days 1 to 7" rule suspended for
these items only. Every number was recomputed through the offline cache before any edit was made,
and every claim below reproduced exactly. The four affected keys were reconciled in the same pass,
since each had been written around the error and said so.

1. **Day 4 EOD, task 3** said "Four columns have gaps." There are **five**: `SubRegions` 15,657,
   `Regions` 8,249, `Measurement` 5,792, `Oceans` 271, and `Keywords` 18. Now reads "Five".
   The key's task 3 answer no longer opens "There are five, not four" and no longer teaches the
   discrepancy as a lesson in reading output against expectations, since there is no longer a
   discrepancy. It names the five and keeps the point that `Keywords` is easy to skim past.
2. **Day 4 EOD, task 7** said to "confirm with `.isnull().sum()` that nothing is missing anywhere."
   After filling `Regions` and `SubRegions`, `Keywords` still has 18 nulls. Now reads "confirm
   that only `Keywords` is still missing anything." The key's task 7 answer leads with `Keywords`
   as the expected result rather than as a gap the student had to catch.
3. **Day 6 EOD, question 9** said two decade winners rest on fewer than four entries. There are
   **three**: France in the 1950s (3 entries, 19.7), Serbia in the 2000s (2 finals, 214.0) and
   Bulgaria in the 2010s (3, 362.7). Now reads "Three", with "either one" changed to "any of them"
   for grammar. The key names all three in its opening sentence and drops "not two, so count the
   rows yourself rather than taking the question's word for it."
4. **Day 7 EOD, "the figure minute"** said question 18 showed "six distinct values". The correct
   count is **eleven**, all multiples of five, from -30 to +25. Now reads "eleven". The Day 7 key
   already said eleven throughout and needed no change here.
5. **Day 7 EOD, question 26** said one of the bottom-five states "has more zip codes in it than any
   other state in the file." California has 2,552 in `change`, second to **Texas at 2,566**. Now
   reads "than all but one other state in the file", which keeps the teaching point that a small
   mean resting on a very large count is more trustworthy and less interesting. The key's answer
   drops the "the largest count in this table but one" workaround and states it directly.

**The design problem. Day 2 EOD, question 10** asked "do all years have the same number of
observations?" but prescribed `.value_counts().head()`, which sorts by count descending and
therefore returns five leap years at 366 and never surfaces 1988's 214 rows. A student following
it exactly would conclude that all years are the same length.

**Decision: run both ends, `.head()` and then `.tail()`.** The question now reads "Use
`.value_counts()` on the `Year` column and look at both ends of the result, with `.head()` and
then with `.tail()`", and a second one-line cell was added after the existing one. Switching to
`.tail()` alone was the smaller edit and was tried first, but it makes only half the question
answerable: the tail shows 1988 at 214 against four years of 365 and hides the five leap years at
366, so a student reading only the tail would answer "yes, 365 each except 1988", which is also
wrong. Running both ends is the smallest change that lets both halves of the question be answered
from true output. It also puts the sorting behaviour of `.value_counts()` in front of the student,
which is the conceptual gap that produced the error. `.groupby('Year').size()` was rejected: it
preserves year order but introduces a construct that Day 2 does not have, since Day 2 holds only
the collections vocabulary plus the explore toolkit. The key's question 10 answer was rewritten to
explain what each end shows rather than to catch the student out, and its "Where the marks are"
item 2 no longer treats the call as a trap. It now asks for the explanation of 1988 rather than
the discovery of it.

**The house-style nit. Day 4 EOD, question 23** used "land" as a metaphorical verb ("samples they
called `Very Low` land in your `high` bin"). Changed to "fall in", in the exercise and in
`eod-day4-2026-key.qmd`, which reproduces the question verbatim.

**Verification.** `python tools/run_cells.py` over the four edited exercises and all twelve keys
stayed at 228/228 clean on the keys. Zero em-dash characters in every touched file. No question
was renumbered, no section restructured, and nothing outside these seven items was changed. No
forward links from any exercise to its key were added, per the decision above.

**Still true: do not edit the source exercises casually.** This pass was the deliberate correction
the rule was reserving. The rule is back in force.

## Pre-launch checklist

Run once the restructuring is done and the revisions are settled, before the deploy. These
are cleanup items that would be premature while days are still moving.

- [x] **Retire the superseded 2025 files from the render. DONE 2026-08-15.**

      The candidate list was rebuilt mechanically rather than taken from the enumeration that
      used to sit here. A breadth-first walk from the 42 roots in `_quarto.yml` plus `index.qmd`,
      following link chains so that a file reachable only through another orphan still counts as
      an orphan, found 98 of 163 renderable files reachable and 65 unreachable. The result was
      cross-checked in the opposite direction by grepping all 98 reachable files for every
      orphan's filename stem; the only hits were word-boundary false positives (`eod-day1` inside
      `eod-day1-2026`, the words "dictionaries" and "lectures" in prose). No live page linked any
      orphan, so nothing broke.

      **Kept live, deliberately unlinked (3).** The instructor-notes siblings of the three live
      2026 live-coding sessions: `live-coding/2d_lists_and_dicts_notes.qmd`,
      `3a_booleans_and_conditionals_notes.qmd` and `5d_loops_over_groups_notes.qmd`. Each opens
      "Instructor run-through for Session 2D / 3A / 5D" and links its live student-facing parent.
      A content scan confirmed this independently: these are the only three orphans carrying any
      2026 marker (a Field Note, or the `lambda` prohibition).

      **Deleted (59),** since git history preserves every one and 59 exclusion lines would have
      made the four-line render block unusable. By day: Day 1 (8), Day 2 (9), Day 3 (9),
      Day 4 (11), Day 5 (7), Day 6 (8), Day 7 (6), plus `lectures/lectures.ipynb`. This covers all
      seven 2025 EOD and key pairs including `eod-day1-draft.qmd`, both `_old` 6a/6b siblings,
      `coding-colabs/6b_preprocess.ipynb`, and the five 2025 colab keys. Moved through
      `_to_delete/2025-orphan-sweep/` because `rm` fails on the Cowork mount.

      **Excluded via the `render:` block in `_quarto.yml` (3).** Three pages that are unlinked but
      are general references rather than day sessions, and are superseded by nothing in 2026:
      `interactive-sessions/2c_exceptions_and_errors.qmd` (325 lines on reading Python errors),
      `2a_getting_help.qmd` (100 lines on `help()`), and `interactive-session-git.qmd` (a sidebar
      on Git for notebooks). They stay in the working tree as instructor reference and stop being
      reachable on the site.

      **Two claims in the old text had gone stale and are recorded here for the history.**
      `answer-keys/answer_keys.qmd` links none of the fifteen 2025 keys, having been rewritten on
      2026-08-11 around the twelve 2026 keys, so it needed no revision in this pass. And the
      `jupyter:` field is not a 2025-versus-2026 discriminator, since an earlier pass renamed the
      kernel across the whole tree; classification used the link graph plus subtitle and content
      instead. The single exception found: `lectures/lectures.ipynb` still read
      `jupyter: eds217_2025`, because its YAML sits in a raw notebook cell that the rename missed.
      It was deleted as a superseded two-cell stub of `lectures.qmd`.

      **Also found and worth knowing.** `interactive-sessions/4c_dataframe_workflows.qmd`, now
      deleted, taught the **nine**-step workflow that the 2026 build corrected to ten, so it
      contradicted `final_project.qmd` rather than merely being superseded.

- [x] **Switch the course from JupyterLab to Positron. DONE 2026-08-15.**

      MEDS runs Positron in 2026, and students arrive having used it in their R course, so
      Session 1a was rewritten to teach what changes when the interpreter is Python rather than
      to introduce an IDE from nothing. `1a_jupyterlab_notebooks.qmd` became
      `1a_positron_notebooks.qmd`, and `cheatsheets/JupyterLab.qmd` became
      `cheatsheets/positron.qmd`. Both old files were retired through
      `_to_delete/positron-switch/`. Navbar, `cheatsheets.qmd` and `day1.qmd` follow the renames,
      and the navbar reference link now points at the Positron documentation.

      **The wider change was the setup ritual, not the two Day 1 pages.** Fifteen sessions across
      Days 1 through 7 told students to open a JupyterLab Launcher and click a kernel tile, then
      rename the untitled tab. Nine used the compact one-line form and six the expanded form, and
      neither is reachable by grepping for "JupyterLab", which is why the first scan missed them.
      All fifteen now read: create from the Command Palette, confirm the Kernel Selector reads
      `eds217_2026`, save with a name straight away. Prose only; no code cell changed, and
      `run_cells.py` reports 21/21 clean over the three files with executable blocks.

      **Content that changed rather than moved.** The cheatsheet dropped the
      `lckr-jupyterlab-variableinspector` install, which Positron's Variables pane makes
      unnecessary, and gained the Data Explorer, the interpreter-against-kernel distinction, and a
      corrected shortcut table. Session 1a gained a section on choosing the interpreter, and a
      caution that switching it clears the session. `setting_up_python.qmd` now installs the
      kernel machinery and Positron rather than JupyterLab, with a note that the guide is optional
      because class runs on Workbench. `day1-welcome-outline.md` says Positron Pro in the
      logistics and environment-check bullets.

      **Left alone deliberately.** `environment-2026.yml` still pins `jupyterlab>=4.4,<5.0`. It is
      harmless, it keeps a fallback available on Workbench, and removing it would mean rebuilding
      the environment two weeks before class.

- [ ] **Capture two Positron screenshots for Session 1a.** The page carries two commented-out
      image references at the exact insertion points: `images/positron_launch.png` after the
      launch steps, and `images/interface-positron.png` after the interface tour. Both need
      screenshots from a live Positron Pro session on `workbench-1.bren.ucsb.edu`, since the old
      `JupyterLab_launch.png` and `interface-jupyterlab.png` no longer show what students will
      see. Those two files, plus `JupyterLab_launcher.png`, are now unreferenced by any page and
      can be retired once the replacements are in. `images/Jupyter.png` is still the Session 1a
      header and is still correct, since the session is about Jupyter notebooks.

- [ ] **Verify the Session 1a instructions against a live Positron Pro session.** Four claims were
      written from the Posit documentation rather than from the running environment, and each is a
      first-hour step: that the Workbench session type is labelled **Positron Pro**; that
      **Create: New Jupyter Notebook** is the Command Palette entry; that saving a new untitled
      notebook with `Ctrl + S` prompts for a file name; and that the `eds217_2026` kernel appears
      in the notebook Kernel Selector without further configuration. Posit does not publish
      cell-level notebook shortcuts for the Positron Notebook Editor, so the cheatsheet lists only
      `Shift + Enter`, `Ctrl + Enter`, save, and the Command Palette, and tells students to search
      the palette for anything else.

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

- [x] **Four broken image paths. DONE 2026-08-15.** All four targets existed; each reference was
      missing a `../` or carried a typo. `live-coding/2d_lists_and_dicts.qmd` and
      `coding-colabs/2c_exploring_unfamiliar_data.qmd` now use `../images/`, matching the pattern
      all six live 2026 colabs already use. `eod-practice/eod-day2-2026.qmd` likewise, and
      `lectures/pandas_workflow.qmd` now points at `assets/workflow_pandas.jpeg` rather than the
      misspelled `assets/workflows_panads.png`.

      The `.jpg` versus `.jpeg` difference was a red herring: `images/collections.jpg` (189 KB,
      2023) and `images/collections.jpeg` (231 KB, 2024) are two genuinely different files, so
      nothing needed copying or renaming.

- [ ] **Generate four Day 6 images.** The collision with `day5.qmd` is resolved, but every Day 6
      panel is now a placeholder pulled from the 2025 stock. `dates.jpeg` went to `6c_dates.qmd`,
      which is the one assignment worth keeping. The other four want bespoke panels in house style
      (a single anthropomorphic panda, painterly, square, no lettering):

      - `course-materials/day6.qmd`, currently `images/structured-data.png`. A panda standing
        between two piles of paper, one tall and narrow, one short and wide, holding one sheet up
        to compare them
      - `6a_joining_data.qmd`, currently `../images/panda.jpeg`. A panda fitting two halves of a
        torn map together on a table so the roads line up across the seam
      - `6b_reshaping_data.qmd`, currently `../images/dataframes.jpeg`. A panda turning a long
        paper scroll sideways on a light table so its rows become columns
      - `6d_two_table_exercise.qmd`, currently `../images/towersensors.jpeg`. A panda at a desk
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
- [x] **Last `lambda` in the course materials. DONE 2026-08-15, gate 5 passes.**
      The orphan sweep removed `answer-keys/eod-day2-key.qmd` line 164 and
      `interactive-sessions/6b_grouping_joining_sorting_2_old.qmd` line 428 as planned.

      **The old accounting here was incomplete: it counted only `.qmd` files.**
      `lectures/00_intro_to_python.ipynb` carried two real `lambda` calls at lines 894 and 932,
      and that notebook is tracked, rendered, and reachable from the navbar through
      `lectures.qmd`. Both were rewritten as dict comprehensions, which are in course scope:
      the `rename(columns=...)` call now builds a `language_names` dict first, and the
      `apply(...)` call now builds a `response_percentages` dict and passes it to
      `pd.DataFrame(...)`. Behaviour is identical. The inner `.fillna(0)` in the original was a
      no-op, since `value_counts` never yields NaN, and the cross-column NaNs that alignment
      produces were not filled before and are not filled now. Quarto does not re-execute `.ipynb`
      files, so the stored outputs stay consistent. The diff is 6 insertions and 2 deletions,
      confined to the two cells.

      The seventh naive-grep hit was `lectures/.ipynb_checkpoints/00_intro_to_python-checkpoint.ipynb`,
      which is untracked and gitignored. The tightened gate-5 grep skips that directory.

- [x] **Four orphan CSVs in `course-materials/cheatsheets/`. DONE 2026-08-15.** The live cause
      was `pandas_dataframes.qmd` calling `df.to_csv('output.csv')` on every render. That block is
      now `#| eval: false`, so the syntax still displays but nothing is written. A full cheatsheet
      run afterwards confirmed no `output.csv` is recreated anywhere. All four files were then
      removed. `ocean_temperatures.csv` was byte-identical to `data/ocean_temperatures.csv` (same
      md5), so it was a 316 KB duplicate of the cached copy rather than a unique asset.

- [x] **Checked `JupyterLab.qmd` and `setting_up_python.qmd`. DONE 2026-08-15.**

      `workbench-1.bren.ucsb.edu` is still correct and needs no change. Bren's own compute
      documentation lists `workbench-1` as the coursework server and `workbench-2` as the capstone
      server, with neither marked retired or renamed, and the MEDS installation guide names the
      same pair.

      `setting_up_python.qmd` agrees with `environment-2026.yml` on everything the course uses.
      The environment name (`eds217_2026`) and Python version (3.11) match exactly. An import
      audit across all 51 live 2026 files plus the 24 cheatsheets found exactly four third-party
      packages in use: **pandas, numpy, matplotlib, seaborn**, all of which both install paths
      cover. The divergence runs the other way: the yml carries nine packages no 2026 material
      imports (scipy, scikit-learn, plotly, statsmodels, requests, beautifulsoup4, openpyxl, xlrd,
      lxml). That is not a problem to fix before the course, but a leaner environment would
      install faster for students, and it is worth revisiting for 2027.

      One real gap was fixed: line 82 ran `python -m ipykernel install` without ever installing
      `ipykernel`. It arrives as a dependency of `jupyter`, so it worked, but it is now explicit.

- [x] **`search: false` added to `live-coding/2d_lists_and_dicts_notes.qmd`. DONE 2026-08-15.**
      Six of the seven `_notes.qmd` files carried it; this one did not, so the Day 2 instructor
      run-through was indexed by site search and a student could find it.
- [x] **`tools/run_cells.py` now honours `#| eval: false`. DONE 2026-08-15.** The checker used to
      report eight failures in `interactive-sessions/8a_github.qmd`, whose `{python}` blocks hold
      shell commands and are all marked `eval: false`, so Quarto never runs them. Those eight were
      false failures in the tool, not defects in the page. Skipped blocks are now counted and
      reported separately.
- [x] **`run_cells.py` over every 2026 session, EOD, key and cheatsheet. DONE 2026-08-15:
      933/933 cells clean across 76 files, zero failures.** The twelve keys hold at 228/228.
      Two checker defects were fixed along the way, both of which produced false failures:
      `#| eval: false` blocks were being executed (8 in `8a_github.qmd`), and IPython magics and
      shell escapes were being executed (2 in `JupyterLab.qmd`). Skipped blocks are now counted
      and reported with their reason.
- [x] **`warm_cache.py`. DONE 2026-08-15: all 10 real course-site URLs resolve, 0 external,
      exit 0, and it now runs with no network at all.** The offline caching work is complete:
      the "26 files fetching from 10 external hosts" problem is fully closed.

      Two phantom failures were fixed first, and both would have cost time during Gate A. The
      tool classified course-site URLs before illustrative ones, so
      `data/some_file.csv`, a placeholder that appears only on a commented-out line in
      `timeseries.qmd` and inside a plain ```` ```python ```` block in `2a_reading_data.qmd`, was
      reported as missing data. Illustrative now wins regardless of which host a placeholder
      imitates, and the pattern covers `example.org` (RFC 2606) alongside the Google Drive links.
- [ ] Full `python build_docs.py --full` with no errors. **Not runnable in the Cowork VM: Quarto
      is not installed there.** Run this on the laptop. A whole-tree internal link and asset scan
      over all 101 rendered files returned zero broken references on 2026-08-15, which covers what
      the render would catch for the changes made this week.
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
5. `grep` for `lambda` returns nothing in course materials. **Passes as of 2026-08-15.** The
   naive `grep -r lambda` produced false positives on prose (the live 2026 instructor notes
   each carry the line "Do not use `lambda` anywhere. It is not in this course.") and on the
   untracked `.ipynb_checkpoints/` copies. The gate is now:

   ```
   grep -rnE 'lambda[[:alnum:]_, *]*:' course-materials \
     --include='*.qmd' --include='*.ipynb' --exclude-dir='.ipynb_checkpoints'
   ```

   Requiring the parameter list and colon matches real lambdas in all three forms
   (`key=lambda r:`, bare `lambda:`, multi-arg `lambda a, b:`) and never matches backticked
   prose. Verified against a probe file carrying all three forms.
6. 2025 EOD alignment checklist run and archived
