# Day 5 Build Brief: Group + Aggregate

**Fri Sep 4, 2026.** Self-contained: everything needed to draft Day 5 without a network
connection and without reading back through a prior session.

This is the largest new build in the rebuild. Two of the five files have no usable 2025
ancestor. Budget accordingly.

## Read first

1. `tasks/2026-planning/2026-day-skeleton.md`, the Day 5 section, its scope table, and
   **decision 10** (the rehearsal rule, which replaced the half-day rule on 2026-08-11)
2. `course-materials/interactive-sessions/3c_sorting_and_ranking.qmd` and
   `eod-practice/eod-day3-2026.qmd`, for voice and callout conventions
3. `course-materials/live-coding/2d_lists_and_dicts_notes.qmd`, for the live-coding notes
   format 5d must match
4. This file

## What Day 5 owns

One named sentence pattern, taught in two forms that students must recognize as the same
sentence:

```python
grouped = df.groupby('key')          # two-step
grouped['col'].mean()

df.groupby('key')['col'].mean()      # one-line
```

The 2025 materials only ever show the one-line form, and the ledger flags that gap explicitly.
Teaching both, side by side, and saying "these are the same sentence" is the point of 5a.

Fundamentals woven in: dicts deepened via `.agg({...})`, loops over `groupby`, and
comprehensions at reading level only.

## Scope table (from the skeleton; do not exceed it)

| Construct | Scope taught | Session | EOD depth |
|---|---|---|---|
| split-apply-combine, both forms | single key, single column, single agg | 5a, morning | WRITE |
| `.agg(['mean','max'])` / `.agg({col: fn})` | list and dict args | 5b, morning | WRITE |
| grouped result → top-N | Day 3 pattern reuse on grouped output | 5b, morning | WRITE |
| multi-key groupby + `.reset_index()` | recognize and unstick; not compose | 5b | ADAPT |
| loop over groupby | `for name, group in ...` shown | 5d, afternoon | ADAPT |
| comprehensions | READ/gloss + cheatsheet link | 5d, afternoon | READ |

Three WRITE constructs. There is real headroom under the budget of eight, and this is the day
most likely to need it. Spend it deliberately and add a row to the skeleton if you do.

## Files to produce

| New file | Adapt from | Notes |
|---|---|---|
| `interactive-sessions/5a_grouping_data.qmd` | `6a_grouping_joining_sorting.qmd` lines 118–144 only | 27 usable lines. Mostly new writing. |
| `interactive-sessions/5b_aggregating_data.qmd` | `cheatsheets/data_grouping.qmd` lines 30–65 | `.agg` list and dict forms live in the cheatsheet, not in any session. |
| `coding-colabs/5c_grouped_comparisons.qmd` | **nothing usable** | New build. See the question bank below. |
| `live-coding/5d_loops_over_groups.qmd` + `_notes.qmd` | `live-coding/2d_list_comprehensions{,_notes}.qmd` | Student-facing page carries no code; notes carry all of it plus timing checkpoints. |
| `eod-practice/eod-day5-2026.qmd` | **nothing** | New build on OpenAQ. Task design below. |

Then wire `course-materials/day5.qmd` and the `_quarto.yml` navbar as Days 2 and 3 were.

## What is actually in the 2025 sources

`6a_grouping_joining_sorting.qmd` (409 lines) is mostly not yours:

| Topic | Lines | Fate |
|---|---|---|
| sorting | 94–115 | **cut**, taught Day 3 |
| grouping and aggregation | 118–144 | → 5a / 5b, the only salvage |
| joining | 146–174 | → Day 6 |
| dates as index, `inplace=`, resample | 175–239 | → Day 6 |
| `df.apply()` | 240–277 | → Day 4 |
| pivot tables | 278–398 | → Day 6, and it is broken; see the Day 6 brief |

Inside those 27 salvageable lines: only the **one-line** groupby form is shown
(`df.groupby('site')['count'].sum()`, line 127); **no** two-step form; **no** multi-key
groupby; `.agg()` appears **only with a dict** (lines 137–141); `.reset_index()` appears in the
file but never after a groupby.

`cheatsheets/data_grouping.qmd` has what 6a lacks: the two-step form at lines 33 and 45–46, and
the `.agg(['mean','sum','count'])` list form at line 53. Start 5a/5b from the cheatsheet, not
from 6a.

`6b_advanced_data_manipulation.qmd`, the 2025 colab, is **not usable for 5c**. Every one of its
four tasks needs dates, and task 2 needs a merge. It belongs to Day 6.

`2d_list_comprehensions_notes.qmd` (256 lines, timed to 45 min) is the ancestor for 5d's
comprehension gloss: for-loop building at lines 70–119, list comprehensions at 120–149, dict
comprehensions at 150–200, conditionals in comprehensions at 201–240. **Demote all of it to
reading level.** Students read and predict; they never write one.

## The OpenAQ EOD

**The "~4,900 uncommitted appended rows" warning in the skeleton is stale. Ignore it.**
`tasks/2026-planning/openaq-reconciliation-report.md` (2026-07-20) established that the three
files were committed as Git LFS pointers with no active `.gitattributes` rule, so git compared
a 3-line pointer against the full CSV and reported the whole file as changed. Working-tree
content is byte-for-byte identical to the original LFS objects. The ~4,900 figure is simply the
total row count: 714 + 1,962 + 2,266 = 4,942 rows, 4,939 of them data. Commit `130a509`
resolved the storage question. Nothing to reconcile.

### The data

Three files, one station each, identical 15-column schema:

| File | Rows | Parameters | Date range (local) |
|---|---|---|---|
| `openaq_goleta_measurments.csv` | 1,962 | pm25 734, o3 711, pm10 517 | 2024-07-11 18:00 → 2024-08-11 17:00 |
| `openaq_santa_barbara_measurments.csv` | 2,266 | pm10 766, pm25 766, o3 734 | 2024-07-10 18:00 → 2024-08-11 17:00 |
| `openaq_CNSI_measurments.csv` | 714 | pm25 only | 2024-07-10 18:00 → 2024-08-11 17:00 |

Units: µg/m³ for pm25 and pm10, ppm for o3. `country_iso`, `isMobile` and `isMonitor` are 100%
null in all three; no other nulls. CNSI carrying only pm25 is a teaching feature, not a defect.

### The constraint that shapes the whole design

The skeleton wants grouping "by station, by parameter, by hour/day". But:

- **by station requires `pd.concat`**, which is a Day 6 construct
- **by hour requires `datetimeLocal.str[11:13]`**, string slicing, which is not one of Day 4's
  three `.str` methods

So both cross-cutting axes cost a Field Note, and the budget is exactly 2. That is legal but it
spends the whole allowance. Two ways to go:

**Option A, spend both.** Field Note 1 supplies the three-file stack:

```python
goleta['site'] = 'Goleta'
santa_barbara['site'] = 'Santa Barbara'
cnsi['site'] = 'CNSI'
aq = pd.concat([goleta, santa_barbara, cnsi], ignore_index=True)
```

Field Note 2 supplies the hour column: `aq['hour'] = aq['datetimeLocal'].str[11:13]`.
Everything after that is `groupby` on one key, which is the day's own material. This gives the
richest EOD and is the recommended option.

**Option B, spend neither.** Work one station at a time, grouping only by `parameter`. Cheaper,
and much thinner: a single station with three parameters supports maybe four real questions.

Decide before drafting. If you take Option A, note that the two Field Notes are both setup, so
the whole body of the EOD is Day 5 vocabulary, which is a clean shape.

### Verified question bank

All answers computed against the real files. Use these directly or as models.

| Question | Expression | Answer |
|---|---|---|
| Which site has the highest mean PM2.5? | `aq[aq['parameter']=='pm25'].groupby('site')['value'].mean().sort_values(ascending=False)` | Goleta 6.481, Santa Barbara 6.172, CNSI 6.083 |
| How many O3 readings per site? | `aq[aq['parameter']=='o3'].groupby('site')['value'].count()` | Goleta 711, Santa Barbara 734, CNSI absent |
| Which site has the highest mean PM10? | same shape, `parameter=='pm10'` | Santa Barbara 17.564, Goleta 14.973 |
| Highest PM2.5 ever recorded per site? | `...groupby('site')['value'].max()` | Goleta 22.0, Santa Barbara 17.0, CNSI 12.0 |
| Total readings per site? | `aq.groupby('site')['value'].count()` | SB 2,266, Goleta 1,962, CNSI 714 |
| Readings of each parameter at Goleta? | `goleta.groupby('parameter')['value'].count()` | pm25 734, o3 711, pm10 517 |
| Hours above 12 µg/m³ per site? | `aq[(aq['parameter']=='pm25') & (aq['value']>12)].groupby('site')['value'].count()` | Goleta 51, SB 25, CNSI 0 |
| Count, mean and max of PM2.5 per site in one call | `...groupby('site')['value'].agg(['count','mean','max'])` | CNSI 714/6.083/12.0; Goleta 734/6.481/22.0; SB 766/6.172/17.0 |
| Minimum PM2.5 per site (data-quality check) | `...groupby('site')['value'].min()` | CNSI 3.0, Goleta **−4.0**, SB **−1.0** |
| Mean O3 by hour of day | `aq[aq['parameter']=='o3'].groupby('hour')['value'].mean().sort_values(ascending=False)` | peak at hour `'14'`, 0.03087 ppm |

The last one is the best question in the set. Afternoon ozone peaks are real photochemistry,
the answer is unambiguous, and it needs the whole day's grammar to get at. Build the EOD's
closing section around it.

The negative-minimum question is the second best: it re-raises Day 2's "the data has problems"
theme, and CNSI having none while the other two do is a genuine puzzle worth a markdown answer.

## Rules that apply

- **Rehearsal rule** (skeleton decision 10). Every WRITE construct needs a named session and
  task where students wrote it unaided. All three of Day 5's WRITE constructs are morning-taught
  in 5a/5b, so **no exemption is needed**, but 5c must still supply the practice. Aim for at
  least three sole-author uses of the split-apply-combine sentence in 5c.
- **No `lambda`, anywhere, including answer keys.** There is none in any 2025 Day 5 source.
- **Comprehensions are READ only.** 5d is where the course discharges this obligation. Students
  read comprehensions and predict their output. They never write one, and no EOD requires one.
- **No h1 headers.** Largest heading is `##`. Notebook title cells inside fenced blocks are
  exempt.
- Every session opens with the Getting Started notebook ritual and closes with Key points and
  Resources. The live-coding pair follows `2d_lists_and_dicts{,_notes}.qmd`: no code at all on
  the student page, all code plus timing checkpoints in the notes.

## Verify before committing

```bash
python tools/run_cells.py course-materials/interactive-sessions/5*.qmd \
                         course-materials/coding-colabs/5c_*.qmd \
                         course-materials/live-coding/5d_*.qmd \
                         course-materials/eod-practice/eod-day5-2026.qmd
grep -rn "lambda" course-materials/*/5*.qmd course-materials/eod-practice/eod-day5-2026.qmd
grep -c "🧭 Field Note" course-materials/eod-practice/eod-day5-2026.qmd   # must be <= 2
grep -rn "merge\|pivot_table\|to_datetime" course-materials/eod-practice/eod-day5-2026.qmd
```

The last check must come back empty. The EOD is join-free and date-free by construction; if
any of those three appear, the day has drifted into Day 6.

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
