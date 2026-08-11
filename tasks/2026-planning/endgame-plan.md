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
3. Cheatsheet updates (ship 2025 versions)
4. Day 4 colab polish

Days 2, 3, and 5 are not cuttable. They carry the redesign.

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
      `answer-keys/eod-day7-key.qmd`. Three of the Day 5
      four, two of the Day 6 six and at least one of the Day 7 five are still linked from
      `answer-keys/answer_keys.qmd`, **so that page needs revising in the same pass**, not just the
      render config. `7a_visualizations_1.qmd` also links its own retired sibling. Note that
      `cheatsheets/data_merging.qmd` also names `6b_advanced_data_manipulation` in a section
      heading; that is prose, not a link, but it should be reworded. Decide per file: delete, or exclude via the
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
