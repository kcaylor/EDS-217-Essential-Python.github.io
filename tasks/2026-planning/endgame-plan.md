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
- a drift checklist to self-run before committing

Kelly drafts into the qmd files directly. Polish, answer keys, and rendering happen in a session
whenever there is bandwidth.

## Order of work on the road

Teaching order, not risk order. The vocabulary budget and the half-day rule are sequential, so
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
      Days 3-7 orphan as they are rebuilt. Decide per file: delete, or exclude via the
      `render:` block in `_quarto.yml`. Do this last, since each rebuilt day adds to the list.
- [ ] Run `python tools/run_cells.py` over every 2026 session and EOD.
- [ ] Run `python tools/warm_cache.py`; expect every course-site URL to resolve.
- [ ] Full `python build_docs.py --full` with no errors.
- [ ] Update the syllabus Google Doc link and TA information.
- [ ] Push to `origin`, then `live`, then verify the site serves `data/` correctly.

## Quality gates (unchanged, from work-plan.md)

1. Every construct traces to a day scope table in `2026-day-skeleton.md`
2. Half-day rule holds (afternoon-taught implies ADAPT at most in the same-day EOD)
3. At most 2 Field Notes per EOD
4. Handout and answer key agree: no key-only tasks, names match
5. `grep` for `lambda` returns nothing in course materials (currently fails: 3 files)
6. 2025 EOD alignment checklist run and archived
