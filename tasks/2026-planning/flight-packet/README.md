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
| `day6-build-brief.md` | Tue Sep 8, Join + Reshape + Dates | **built 2026-08-11** |
| `day7-build-brief.md` | Wed Sep 9, Visualize | **built 2026-08-11** |

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

Three corrections to the Day 6 brief, found while building it and recorded in the skeleton's
Day 6 section. **The Eurovision merge does not need a trimmed population file**: restricting the
entry counts to 1990 onwards drops Morocco, which has competed exactly once, in 1980, so the
inner-versus-right contrast is 51 rows against 52 on unmodified data. **`//` integer division is
taught nowhere in the 2026 Days 1-5**, so the brief's decade line would have cost a Field Note;
`(col.dt.year / 10).astype(int) * 10` uses only taught vocabulary, because `4a_cleaning_data.qmd`
already states that `.astype(int)` truncates toward zero. And the brief's suggestion to keep the
2025 EOD's bare `.hist()` in task 2 is superseded by the Day 4 correction above; all plotting is
cut from the Day 6 EOD, which is correct for a data-shape day.

The Day 6 EOD spends **zero Field Notes**. The colab callback moved into the morning sessions
rather than the colab: 6a and 6b both re-open the Day 5 EOD's OpenAQ work, and 6b opens by
discharging the promise that EOD's Field Note made.

Image contention is now real enough to plan around. `day5.qmd` uses
`interactive-sessions/images/grouping_filtering.jpeg`, **which `day6.qmd` also currently uses**,
so the Day 6 rebuild must pick a different day-page image. `dates.jpeg` went to `6c_dates.qmd`, which is where it belongs;
`day6.qmd` now uses `images/structured-data.png`, `6a` uses `../images/panda.jpeg`, `6b` uses
`../images/dataframes.jpeg` and the 6d colab uses `../images/towersensors.jpeg`. **All four of
those are placeholders**, and prompts for bespoke Day 6 panels belong in the pre-launch checklist
alongside the Day 4 and Day 5 EOD prompts. `matplotlib_panda.jpeg` and `panda_seaborn.jpeg`
remain unclaimed and reserved for Day 7.

Six corrections to the Day 7 brief, recorded in the skeleton's Day 7 section. The largest:
**7a is a rebuild, not a trim.** Everything that survives the brief's 320-line cut of
`7a_visualizations_1.qmd` is synthetic `np.linspace`/`np.sin` waveforms, and numpy appears in no
2026 session, so 7a was rebuilt on Toolik instead, re-opening the Day 1 Whole Game figure and 6c's
monthly comparison. **`plt.xticks(rotation=)` is READ in the EOD**, not WRITE: no EOD figure needs
it, because the only bar chart is horizontal. **The `longitude < -60` filter is one corrupted
record**, not a territory filter — these files are the contiguous 48 states plus DC, and the single
row above −60 is Alexandria VA mislocated to the sea off Brittany, so the EOD makes students find
it rather than handing them the filter. The index-aligned subtraction was redesigned away as the
brief preferred, so the **second Field Note is unspent**; penguins is cached to
`data/penguins.csv`; and `final_project.qmd` was corrected from nine steps to ten.

Day 7's colab callback lived in the morning sessions again, exactly as on Day 6: 7a re-opens Day 1
and 6c, 7b re-opens the Thursday colab's field survey, so 7c is free for genuinely new data.

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
