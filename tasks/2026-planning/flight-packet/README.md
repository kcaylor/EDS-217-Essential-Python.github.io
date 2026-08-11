# Flight packet

One brief per remaining day, written so drafting needs no network connection and no prior
session context. Each brief names the 2025 files to adapt, the scope table to respect, the
required trims, and the verification commands.

Order of work is teaching order, since the vocabulary budget and the rehearsal rule are
sequential: Day 4 cannot be scoped correctly until Day 3 is fixed.

The half-day rule was replaced by the **rehearsal rule** on 2026-08-11 (skeleton decision 10).
A construct is WRITE in an EOD only if students have already written it unaided at least three
times, across at least two sessions, in at least one of which they were the sole author. Any
brief written before that date states the old rule; read decision 10 first.

| Brief | Day | Status |
|---|---|---|
| `day3-build-brief.md` | Wed Sep 2, Filter + Sort | **built 2026-08-11** |
| `day4-build-brief.md` | Thu Sep 3, Clean + Transform | **built 2026-08-11** |
| `day5-build-brief.md` | Fri Sep 4, Group + Aggregate | **built 2026-08-11** |
| `day6-build-brief.md` | Tue Sep 8, Join + Reshape + Dates | ready |
| `day7-build-brief.md` | Wed Sep 9, Visualize | ready |

Two corrections to the Day 4 brief, found while building it and recorded in the skeleton's
Day 4 section. Bare `.hist()` is **not** in Day 2's explore toolkit (it appears nowhere in the
2026 Days 1-3); the EOD uses `plt.hist()` behind a Field Note instead, which spends the second
Field Note. And `data/messy.csv` was replaced rather than extended: the 4d colab now uses
`data/messy_field_survey.csv`, authored for the course by `tools/make_messy_field_survey.py`.

Two notes from building Day 5. Kelly chose a **single combined setup Field Note** over the
brief's Option A pair: the `pd.concat` stack and the `.str[11:13]` hour column are both setup,
so they share one note and the EOD keeps a Field Note in reserve. The WRITE budget stayed at
three; the headroom the brief flagged was deliberately left for Days 6 and 7. The brief's claim
that 5c had no usable ancestor was true of the 2025 files but understated the opportunity: the
Day 4 EOD is the ancestor, because 5c re-does its Atlantic-versus-Pacific comparison properly.
**Check Days 6 and 7 for the same kind of callback before treating either colab as a pure new
build.**

Image contention is now real enough to plan around. `day5.qmd` uses
`interactive-sessions/images/grouping_filtering.jpeg`, **which `day6.qmd` also currently uses**,
so the Day 6 rebuild must pick a different day-page image. `dates.jpeg`,
`matplotlib_panda.jpeg` and `panda_seaborn.jpeg` are unclaimed and are the obvious reservations
for Days 6 and 7.

Effort is not even across the four. Day 5 has two files with no usable 2025 ancestor, and Day 7
needs 7b rewritten rather than trimmed, because two of the three seaborn functions its exercise
requires are taught nowhere in the 2025 sessions. Days 4 and 6 are closer to relocation and
trimming. Each brief says so at the top.

## Starting a fresh session

Say: "Build Day N for EDS 217. Read
`tasks/2026-planning/flight-packet/dayN-build-brief.md` first."

The brief points at the skeleton and at the Day 1-2 files that set the house style. Project
memory carries the same status, but the brief is the authority, and it works even in a
session with no memory access.
