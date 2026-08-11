# Day 7 Build Brief: Visualize

**Wed Sep 9, 2026.** Self-contained: everything needed to draft Day 7 without a network
connection and without reading back through a prior session.

The skeleton describes Day 7 as "mostly retained from 2025." That is wrong, and the audit below
is the reason. Two of the three seaborn functions the EOD requires are taught nowhere in the
2025 sessions, and the two techniques the plan assigns to 7a are currently taught only in 7b.
Budget more time than the endgame plan allows for this day.

## Read first

1. `tasks/2026-planning/2026-day-skeleton.md`, the Day 7 section, its scope table, and
   **decision 10** (the rehearsal rule, which replaced the half-day rule on 2026-08-11)
2. `course-materials/interactive-sessions/3c_sorting_and_ranking.qmd` and
   `eod-practice/eod-day3-2026.qmd`, for voice and callout conventions
3. This file, especially "What is actually taught today"

## What Day 7 owns

The plotting sentences:

- **matplotlib anatomy**: figure and axes, `plt.figure(figsize=)`, labels, titles,
  `xticks(rotation=)`, `tight_layout()`
- **seaborn**: `sns.scatterplot` / `sns.barplot` / `sns.histplot` with `data=`, `x=`, `y=`,
  `hue=`
- **the Series `.values`/`.index` barplot idiom**, taught explicitly

No new fundamentals.

## Scope table

The skeleton's Day 7 section has no formal scope table. Build one from this and add it to the
skeleton before you start drafting; quality gate 1 needs it to exist.

| Construct | Scope taught | Session | EOD depth |
|---|---|---|---|
| `plt.figure(figsize=)` | figure sizing only | 7a, morning | WRITE |
| `plt.xlabel/ylabel/title/legend` | labels and a titled legend | 7a, morning | WRITE |
| `plt.xticks(rotation=, ha=)` | rotation of tick labels | 7a, morning | WRITE |
| `plt.tight_layout()` | as a closing line | 7a, morning | WRITE |
| `sns.scatterplot(data=, x=, y=, hue=)` | those four arguments | 7b, morning | WRITE (needs rehearsal audit) |
| `sns.barplot`, incl. `x=series.values, y=series.index` | the Series feeding idiom, explicitly | 7b, morning | WRITE (needs rehearsal audit) |
| `sns.histplot(data=, x=)` | single variable | 7b, morning | WRITE (needs rehearsal audit) |
| `.str.split().str.get(n).astype(int)` | 🧭 Field Note in EOD setup | — | ADAPT |
| index-aligned Series subtraction | 🧭 Field Note, or redesigned away | — | ADAPT |

## Files to produce

| New file | Adapt from | Notes |
|---|---|---|
| `interactive-sessions/7a_matplotlib.qmd` | `7a_visualizations_1.qmd` (740 ln), cut hard | Roughly 60% of the source is out of scope. |
| `interactive-sessions/7b_seaborn.qmd` | `7b_visualizations_2.qmd` (426 ln) | Must teach three functions it currently does not. |
| `coding-colabs/7c_visualizations.qmd` | `coding-colabs/7c_visualizations.qmd` (196 ln) | Survives largely intact. One data dependency to fix. |
| `interactive-sessions/7d_project_kickoff.qmd` | **nothing** | New. Teams, dataset browsing, question drafting. |
| `eod-practice/eod-day7-2026.qmd` | `eod-practice/eod-day7.qmd` (247 ln) + `answer-keys/eod-day7-key.qmd` (240 ln) | Hardiness zones. Trims below. |

Then wire `course-materials/day7.qmd` and the `_quarto.yml` navbar as Days 2 and 3 were.

## What is actually taught today, versus what the plan assumes

Read this before you plan the split. Three findings, each verified by direct inspection.

**1. `sns.scatterplot` and `sns.barplot` are taught nowhere.** Not in 7a, not in 7b, not in 7c.
They appear for the first time in the EOD itself. `sns.histplot` is taught, but only in 7c, the
colab. The 2025 ledger claims all three were "first taught 7b/7c"; the ledger is wrong. This is
the single largest gap in the day and the reason 7b needs rewriting rather than trimming.

**2. `figsize` and `xticks(rotation=)` are taught in 7b, not 7a.** The plan assigns both to 7a.
`7a_visualizations_1.qmd` calls `plt.figure()` fifteen times and never once passes `figsize`,
and uses `plt.xticks()` without `rotation=`. Both techniques appear for the first time in 7b at
lines 266–341 and 290–412. Move them to 7a.

**3. 7a spends most of its length outside the scope table.** Lines 190–401 are the color,
linestyle, marker and format-string systems, four vocabularies where the day needs none. Lines
620–729 are `plt.subplot()`, `fig.add_subplot()`, and a Figure-versus-Axes method translation
table. Cutting both blocks removes about 320 of 740 lines and loses nothing the EOD or the
project needs. What survives: `plt.plot`/`plt.scatter` (129–186), limits (409–428), labels
(464–510), title (512–540), legend (542–618), `tight_layout` (728–732).

Also out of scope in 7b, and safe to cut: `sns.relplot` (85–113),
`plt.gca().xaxis.set_major_locator(plt.MaxNLocator(5))` (305–320), and `.resample()` (323–341).
`sns.lineplot` is taught repeatedly (145–342) and is not in the plan; keep one small example if
the BSRN time-series framing is worth it, or cut it.

## Hardiness zones EOD: required trims

The 2025 file is `eod-practice/eod-day7.qmd`. Its shape: load three CSVs, zero-pad zipcodes,
concat two years, split the temperature range, merge against the zipcode database, then three
figures.

**The good news.** Two of the six constructs the 2025 EOD needed without teaching are now
taught: `pd.concat` and `pivot_table` both arrive on Day 6. That alone converts this EOD from
unworkable to workable.

**Field Note 1: the `.str` chain.** From `eod-day7.qmd` lines 130–131:

```python
df['trange_min'] = df['trange'].str.split().str.get(0).astype(int)
df['trange_max'] = df['trange'].str.split().str.get(-1).astype(int)
```

Two chained `.str` accessors plus a cast, against Day 4's "single method, no chaining" scope.
Supply both lines whole. Verified still correct against the current files: `trange` is always
exactly three whitespace-separated tokens of the form `-10 to -5`, zero rows deviate in either
year, and the chain produces zero nulls.

**Field Note 2: index-aligned Series subtraction.** The top-10-states figure computes two
grouped means and subtracts them:

```python
mean_2023 - mean_2012
```

Alignment semantics are never taught anywhere in the course. Either supply this as the second
Field Note, or redesign the task to use the `pivot_table` difference the EOD already computes
elsewhere, which is Day 6 vocabulary and needs no note. **Prefer the redesign**, and keep the
second Field Note unspent.

**Also fix:**

- `.astype(str).str.zfill(5)` in setup, used on three columns. `zfill` is not taught. Supply it
  inside Field Note 1 alongside the split chain, since both are setup and both are about the
  same skill of reshaping text into something joinable.
- The seaborn calls carry `palette=`, `s=`, `edgecolor=` and `legend='full'`. None are in the
  scope table. Either strip them or make sure 7b teaches them; stripping is cleaner.
- **Field Note budget is 2**, and setup alone wants three things (`zfill`, the split chain,
  alignment). Folding `zfill` and the split chain into one note is what makes the budget work.

Confirm no `lambda` and no comprehensions survive. There are none in any 2025 Day 7 source.

## Data

`hardiness_zones_2012.csv`: 40,534 × 4. `hardiness_zones_2023.csv`: 39,921 × 4. Columns in
both: `zipcode` (int64), `zone`, `trange`, `zonetitle`. No nulls in either file. Shared merge
key `zipcode`, same name and dtype in both, so the concat-then-merge shape works.

`zone` is the USDA code, e.g. `6a`. `zonetitle` is a redundant concatenation, e.g.
`6a: -10 to -5`. `trange` is what the `.str` chain parses.

`zip_code_database.csv` (42,523 rows) is present in `data/` and resolves offline. Verify its
`zip` column name before writing the merge task; the EOD merges
`left_on='zipcode', right_on='zip'`.

**One offline risk.** `7c_visualizations.qmd` uses `sns.load_dataset("penguins")`, which fetches
from the seaborn-data GitHub repo at runtime. It is the only Day 7 asset not reading from the
course site, and it will fail on a plane or a bad hotel connection. Cache it to
`data/penguins.csv` and repoint the colab before you rely on 7c working offline.

## 7d, the project kickoff

New session, no ancestor. Its job is to form teams, browse dataset sources, and draft an
analysis question. `final_project.qmd` already carries the source list 7d sends students to:

Kaggle CSV search, Data is Plural, data.gov, Zenodo, TidyTuesday, the Central Park Squirrel
Census, and three named Kaggle sets (Harry Potter characters, Spotify tracks, Lego). It also
carries a Google Drive CSV-loading recipe with a hardcoded example file ID, which is fine as
syntax illustration.

The fallback, if Day 7 runs hot, is already designed: convert 7d to buffer and review, and move
the kickoff to Day 8 morning. Say so explicitly in the instructor notes so the decision is
available in the room rather than needing to be invented.

## Rules that apply

- **Rehearsal rule** (skeleton decision 10). The three seaborn functions are the day's named
  plotting sentences and the EOD wants them at WRITE. 7b is a morning session, so on timing
  alone they are fine; what they need is the rehearsal itself. **7c is the audit**: it must give
  at least three sole-author uses of `sns.scatterplot` and of `sns.barplot`, and 7c currently
  teaches neither. Rework 7c's tasks around the three functions the EOD actually uses, then
  record the audit table in the skeleton's Day 7 section in the format Day 3 uses.
- **No `lambda`, anywhere, including answer keys.**
- **Comprehensions are not taught.**
- **No h1 headers.** Largest heading is `##`. Notebook title cells inside fenced blocks are
  exempt.
- Every session opens with the Getting Started notebook ritual and closes with Key points and
  Resources. Copy the shape from `2a_reading_data.qmd`.

## Verify before committing

```bash
python tools/run_cells.py course-materials/interactive-sessions/7*.qmd \
                         course-materials/coding-colabs/7c_*.qmd \
                         course-materials/eod-practice/eod-day7-2026.qmd
grep -rn "lambda" course-materials/*/7*.qmd course-materials/eod-practice/eod-day7-2026.qmd
grep -c "🧭 Field Note" course-materials/eod-practice/eod-day7-2026.qmd   # must be <= 2
grep -rn "load_dataset" course-materials/coding-colabs/7c_*.qmd           # must be empty once cached
grep -rn "relplot\|MaxNLocator\|add_subplot" course-materials/interactive-sessions/7*.qmd
```

The last check must come back empty. Those three are the out-of-scope constructs most likely to
survive a trim by accident.

Then confirm that every seaborn function the EOD calls is taught in 7a or 7b, and rehearsed in
7c. That check is the whole reason this brief is longer than the others.

## Committing through the Cowork device bridge

The mount cannot unlink, so git leaves stale lock files behind. Before every commit:

```bash
mkdir -p .git/_stale; N=$(date +%s)
for L in .git/index.lock .git/HEAD.lock .git/refs/heads/main.lock; do
  [ -e "$L" ] && mv "$L" ".git/_stale/$(basename $L).$N"
done
git -c user.name="Kelly Caylor" -c user.email="caylor@ucsb.edu" commit -m "..."
```

The bridge also drops intermittently, and `device_commit_files` times out on large batches.
Commit files in groups of two or three and retry rather than pushing one big batch.
