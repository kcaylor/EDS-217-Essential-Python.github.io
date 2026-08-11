# Day 6 Build Brief: Join + Reshape + Dates

**Tue Sep 8, 2026.** Self-contained: everything needed to draft Day 6 without a network
connection and without reading back through a prior session.

Day 6 carries the only wholly new session in the rebuild (6b, reshape) and fixes the two
never-taught findings from the 2025 audit: `pivot_table` and `pd.concat`. No new fundamentals.
Python grammar consolidates.

## Read first

1. `tasks/2026-planning/2026-day-skeleton.md`, the Day 6 section, its scope table, and
   **decision 10** (the rehearsal rule, which replaced the half-day rule on 2026-08-11)
2. `course-materials/interactive-sessions/3b_filtering_data.qmd` and
   `eod-practice/eod-day3-2026.qmd`, for voice and callout conventions
3. `course-materials/cheatsheets/data_merging.qmd` (403 ln). This is the single richest source
   for the whole day, and it is better than any 2025 session file.
4. This file

## What Day 6 owns

Three named patterns:

- **join sentence**: `pd.merge(a, b, on='key')`, then `left_on=`/`right_on=` for mismatched
  key names, with `how='inner'` and `how='left'`
- **reshape**: `pd.concat([a, b])` for stacking, and
  `pivot_table(index=, columns=, values=)`
- **datetime parsing**: `pd.to_datetime(col, format=)` plus `.dt.year` / `.dt.month`

## Scope table (from the skeleton; do not exceed it)

| Construct | Scope taught | Session | EOD depth |
|---|---|---|---|
| `pd.merge` incl. `left_on`/`right_on`, `how='left'` | two-table, single-key | 6a, morning | WRITE |
| `pd.concat([a, b])` | row-wise, same columns | 6b, morning | WRITE |
| `pivot_table(index=, columns=, values=)` | single agg (default mean); reference resulting columns | 6b, morning | WRITE |
| `pd.to_datetime` + `.dt.` accessors | `%Y`/`%m`/`%d` formats only; year and month accessors | 6c, afternoon | WRITE (needs rehearsal audit) |
| `value_counts().reset_index()` + rename | the "Series to table" move (fixes the 2025 D6 gap) | 6b, morning | WRITE |
| MultiIndex `.idxmax()` on groups | redesigned away, see below | — | cut |

Five WRITE constructs, under the budget of eight.

## Files to produce

| New file | Adapt from | Notes |
|---|---|---|
| `interactive-sessions/6a_joining_data.qmd` | `6a_grouping_joining_sorting.qmd` lines 146–174, plus `cheatsheets/data_merging.qmd` lines 30–158 | The 2025 session shows almost nothing. See below. |
| `interactive-sessions/6b_reshaping_data.qmd` | `cheatsheets/data_merging.qmd` lines 159–200 for concat; **write pivot_table from scratch** | The only wholly new session in the rebuild. |
| `interactive-sessions/6c_dates.qmd` | `interactive-sessions/6c_dates.qmd` (399 ln), heavily trimmed | Keep the name, replace most of the content. |
| `coding-colabs/6d_two_table_exercise.qmd` | `coding-colabs/6b_advanced_data_manipulation.qmd` (156 ln) + its key | Pairs, answers hidden. Task 2 is the merge; tasks 3–4 need trimming. |
| `eod-practice/eod-day6-2026.qmd` | `eod-practice/eod-day6.qmd` (342 ln) + `answer-keys/eod-day6-key.qmd` (343 ln) | Eurovision. Trims below. |

Then wire `course-materials/day6.qmd` and the `_quarto.yml` navbar as Days 2 and 3 were.

## The 2025 sources are thinner than they look

**Joining.** `6a_grouping_joining_sorting.qmd` lines 146–174 is the entire join content, and
its only executed code is one call: `pd.merge(df, site_data, on='site', how='inner')` at line
160. The prose describes inner, left, right and outer, but **nothing else is ever run**, and
`left_on=`/`right_on=` appear nowhere in the file. The 2025 ledger flagged this with "verify
mismatched key names shown in 6a"; they are not. Build 6a from
`cheatsheets/data_merging.qmd` instead: the four `how=` variants each have their own worked
section, mismatched column names are at lines 103–126, and index joins at 127–158.

**Pivot tables.** `6a` lines 278–398 look like a starting point and are not. The sample frame
built at lines 304–310 has only `date`, `city`, `temperature`. The student exercise at line 379
asks for a `humidity` column that does not exist, and the hidden answer at lines 390–397
references both `humidity` and a `location` column that is also not there. The block is
`eval: false`, so it has never run. **Do not salvage it.** The only correct pivot content in
the repo is the two examples in `cheatsheets/data_grouping.qmd` lines 103–140.

**Concat.** `pd.concat` appears in exactly one file in the whole repo:
`cheatsheets/data_merging.qmd`, at line 180 (vertical, `axis=0`) and line 195 (horizontal,
`axis=1`). It is genuinely never session-taught. Teach the vertical form; the horizontal form
is a merge in disguise and will confuse.

**Dates.** `6c_dates.qmd` **never uses a `.dt` accessor.** Every date-component operation in it
goes through a `DatetimeIndex` attribute: `df.index.month` (306, 330), `df.index.year` (323),
`df.index.weekday` (339). The `.dt.month` / `.dt.dayofyear` idiom the skeleton wants lives in
`6a` at lines 229–230. So the new 6c needs the `.dt` pattern written fresh, or ported from 6a.

Also trim these from 6c, all beyond the `%Y %m %d` scope:

- line 124: `pd.to_datetime(..., format='mixed')`
- line 139: `format='%d-%b-%Y'` (`%b` is a locale month abbreviation)
- line 365: `.strftime('%B %d, %Y')` (`%B` is a full month name)
- lines 175–299: the resample and datetime-index machinery. `resample` is not in the scope
  table and is not needed by any 2026 EOD.

The format-string reference callout at lines 143–173 can stay as a callout, since it is
reference material students read rather than vocabulary they are asked to produce.

## Eurovision EOD: required trims

The 2025 file is `eod-practice/eod-day6.qmd`, seven tasks: Exploration and Cleaning, Filtering
and Transformation, Sorting and Aggregation, Grouping and Analysis, Joining Data, Time Series
Analysis, and an open-ended Task 7.

**Redesign the decade-winner task.** The 2025 key, lines 168–184, does this:

```python
eurovision_df['decade'] = (eurovision_df['year'].dt.year // 10) * 10
decade_country_avg = eurovision_df.groupby(['decade', 'to_country'])['points_final'].mean()
decade_winners = decade_country_avg.groupby('decade').idxmax()
```

Three untaught things stack up in three lines: a two-key groupby, a MultiIndex result, and
`.idxmax()` applied to index levels returning `(decade, country)` tuples that then need
unpacking. The skeleton cuts this from WRITE expectations. Replace it with the following, which
uses only Day 3's filter and top-N sentences, a single-key groupby, `reset_index()` and
`concat`. It has been run against the real file and reproduces the original winners exactly for
all eight decades:

```python
eurovision_df['decade'] = (eurovision_df['year'].dt.year // 10) * 10

decade_winners_list = []
for decade in sorted(eurovision_df['decade'].unique()):
    decade_data = eurovision_df[eurovision_df['decade'] == decade].copy()
    country_avg = decade_data.groupby('to_country')['points_final'].mean().reset_index()
    top_country = country_avg.sort_values('points_final', ascending=False).head(1)
    top_country['decade'] = decade
    decade_winners_list.append(top_country)

decade_winners = pd.concat(decade_winners_list, ignore_index=True)
decade_winners[['decade', 'to_country', 'points_final']]
```

This is also a better teaching artifact than the original, because the `concat` at the end is
the day's own vocabulary being used for something real.

**Fix the 2020 artifact.** Task 1 does `fillna(0)` across the whole frame. The 2020 contest was
cancelled, so every `points_final` for 2020 is null, and `fillna(0)` turns that into a real
zero. The 2020s decade winner is therefore an artifact of the fill, not a result. Either
restrict the fill to the columns that need it, or filter 2020 out and say why in a callout. The
second is better; it is a genuine data-provenance lesson and it costs one sentence.

**Cut the styled plotting.** Task 5 ends with a `plt.bar` block using
`xticks(rotation=45, ha='right')` and `tight_layout()`. Visualization is Day 7, and the
skeleton's Day 7 note explicitly depends on no earlier EOD demanding styled matplotlib. Task 6
uses `Series.plot(kind='line')`, also untaught. Keep the bare `.hist()` in task 2, which is
part of Day 2's explore toolkit, and cut the rest. If the day feels visually flat without them,
that is correct: Day 6 is a data-shape day.

**Field Note budget is 2.** With the decade task redesigned and the plotting cut, Day 6 may not
need either one. Spending zero is a good outcome, not a suspicious one.

Confirm no `lambda` survives. There is none in any 2025 Day 6 source.

## Data, and one problem to solve before drafting

`eurovision_contestants.csv`: 1,603 rows × 21 columns, years **1956–2020**. Null counts are
uneven by design, since televote/jury splits and semifinals are modern-era features:
`points_tele_final` and `points_jury_final` are null on 1,499 of 1,603 rows;
`sf_num`/`place_sf`/`points_sf` null on roughly 1,046–1,081.

`eurovision_country_populations.csv`: 52 rows × 2 columns, `country_name` and `population`.

**The merge keys are `to_country` and `country_name`.** The names differ, which is exactly the
teaching goal. But the two files contain the **identical set of 52 countries**, so an inner
merge and a left merge both return 1,603 rows with no nulls introduced. The contrast between
`how='inner'` and `how='left'`, which is half of what 6a is supposed to teach, is invisible in
this data.

Fix it one of two ways before you draft 6a:

- **Trim the population file.** Drop three or four countries and commit it as
  `eurovision_country_populations.csv`. Then inner drops those countries' rows and left keeps
  them with a null population, and the difference is visible in one `.shape` call. This is the
  cleaner option and it takes two minutes.
- **Teach the contrast on a smaller pair.** Build a five-row toy example inside 6a for the
  inner-versus-left picture, and use Eurovision only for the mismatched-key-name form.

Either works. What does not work is presenting inner and left as different and then showing two
identical row counts.

Also note, contrary to appearances: `monthly_temperature_data.csv` and
`monthly_co2_concentration.csv`, which the 2025 6b colab loads, **are both present in `data/`**
and resolve offline. That colab is usable as a starting point for 6d.

## Rules that apply

- **Rehearsal rule** (skeleton decision 10). `pd.to_datetime` and the `.dt` accessors are
  taught in 6c, an afternoon session, and the scope table wants them at WRITE in the EOD. They
  are part of the datetime-parsing named pattern, so the exemption is available, but only if 6d
  gives students at least three sole-author uses. **Design 6d to include date parsing, and
  record the audit table in the skeleton's Day 6 section**, in the format Day 3 uses. If 6d
  ends up merge-only, demote the EOD's date tasks to ADAPT instead.
- **No `lambda`, anywhere, including answer keys.**
- **Comprehensions are not taught.** Day 5 glosses them at reading level; nothing here needs one.
- **No h1 headers.** Largest heading is `##`. Notebook title cells inside fenced blocks are
  exempt.
- Every session opens with the Getting Started notebook ritual and closes with Key points and
  Resources. Copy the shape from `2a_reading_data.qmd`.

## Verify before committing

```bash
python tools/run_cells.py course-materials/interactive-sessions/6*.qmd \
                         course-materials/coding-colabs/6d_*.qmd \
                         course-materials/eod-practice/eod-day6-2026.qmd
grep -rn "lambda" course-materials/*/6*.qmd course-materials/eod-practice/eod-day6-2026.qmd
grep -c "🧭 Field Note" course-materials/eod-practice/eod-day6-2026.qmd    # must be <= 2
grep -rn "idxmax\|groupby(\[" course-materials/eod-practice/eod-day6-2026.qmd  # must be empty
grep -rn "plt\.\|sns\." course-materials/eod-practice/eod-day6-2026.qmd    # only bare .hist() allowed
```

The last two must come back clean. The first catches the MultiIndex construct creeping back in;
the second catches the Day 7 sequencing bug the whole redesign exists to fix.

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
