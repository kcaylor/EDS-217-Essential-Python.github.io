# Day 4 Build Brief: Clean + Transform

**Thu Sep 3, 2026.** Self-contained: everything needed to draft Day 4 without a network
connection and without reading back through a prior session.

## Read first

1. `tasks/2026-planning/2026-day-skeleton.md`, the Day 4 section, its scope table, and
   **decision 10** (the rehearsal rule, which replaced the half-day rule on 2026-08-11)
2. `course-materials/interactive-sessions/3b_filtering_data.qmd` and
   `eod-practice/eod-day3-2026.qmd`, for voice, structure, and callout conventions
3. This file

## Session order changed on 2026-08-11

Kelly's decision: **swap 4b and 4c.** The day now runs:

| Slot | Session | When |
|---|---|---|
| 4a | missing-data treatment, `.astype()`, `.drop_duplicates()` | morning |
| 4b | functions (`def`/`return`/default args) and `.apply(named_func)` | morning |
| 4c | derived-column sentence, column arithmetic, `np.log10`, basic `.str` methods | afternoon |
| 4d | colab, clean a messy dataset in pairs | afternoon |

Why: `def`/`return` and `.apply` are **fundamentals**, and decision 10's rehearsal exemption
reaches named sentence patterns only. Leaving them in the afternoon caps them at ADAPT in the
same evening's EOD, which re-creates the exact 2025 failure the skeleton says 4c exists to fix
("functions were effectively learned inside the EOD"). The derived-column and string-cleaning
sentences **are** named patterns, so they sit comfortably in the afternoon and can take the
exemption provided 4d rehearses them.

Bonus: 4c's motivation in the skeleton is "you have now written the same filter-sort-head
three times." After the Day 3 Banana EOD that is a callback to last night, and it works better
first thing in the morning.

## What Day 4 owns

Three named sentence patterns:

- **derived-column sentence**: `df['new'] = expr`
- **missing-data sentence, treat half**: `.dropna()` / `.fillna(value)` (Day 2 taught diagnose)
- **string-cleaning sentence, basic**: `.str.strip()` / `.str.lower()` / `.str.replace()`

Fundamentals woven in: `def`/`return`/default args, and `.apply(named_func)` as the payoff.

## Scope table (from the skeleton; do not exceed it)

| Construct | Scope taught | Session | EOD depth |
|---|---|---|---|
| `.dropna()/.fillna(value)` | whole-frame and single-column | 4a, morning | WRITE |
| `.astype(str/int/float)` | single cast, no chains | 4a, morning | WRITE |
| `.drop_duplicates()` | bare and `subset=[...]` | 4a, morning | WRITE |
| `def f(x): return ...`; default args | 1–2 param functions returning a value | 4b, morning | WRITE |
| `.apply(func)` | named function only, NO lambda | 4b, morning | WRITE |
| derived-column sentence | arithmetic of columns and scalars; `np.log10` as the course's total numpy exposure | 4c, afternoon | WRITE (needs rehearsal audit) |
| `.str.strip/.lower/.replace` | single method, no chaining | 4c, afternoon | WRITE (needs rehearsal audit) |
| `read_csv(parse_dates=['col'], date_format=)` | 🧭 Field Note (full datetime treatment Day 6) | EOD setup | ADAPT |

Seven WRITE constructs, under the budget of eight. Add a row to the skeleton if you spend the
eighth.

## Files to produce

| New file | Adapt from | Notes |
|---|---|---|
| `interactive-sessions/4a_cleaning_data.qmd` | `interactive-sessions/5b_cleaning_data.qmd` lines 110–396 | Missing data, duplicates, `.astype`. Split table below. |
| `interactive-sessions/4b_functions.qmd` | `cheatsheets/functions.qmd` — **not** `1d_operators_functions.qmd`, see the trap below | Functions and `.apply`. Mostly new writing. |
| `interactive-sessions/4c_transforming_data.qmd` | `5b_cleaning_data.qmd` lines 398–437, plus new material | Derived columns do not exist in any 2025 source. Write them. |
| `coding-colabs/4d_cleaning_messy_data.qmd` | `coding-colabs/5c_cleaning_data.qmd` (94 ln) + its key | Pairs, answers hidden via `execute: echo/include: false`. Dataset problem below. |
| `eod-practice/eod-day4-2026.qmd` | `eod-practice/eod-day4.qmd` (229 ln) + `answer-keys/eod-day4-key.qmd` (231 ln) | Marine microplastics. Trims below. |

Then wire `course-materials/day4.qmd` and the `_quarto.yml` navbar, exactly as Days 2 and 3
were. Retire from the navbar: `4a_dataframes`, `4c_dataframe_workflows`,
`4d_data_import_export`, `4b_pandas_dataframes` colab, `5b_cleaning_data`, `5c_cleaning_data`.

## The 1d trap

`1d_operators_functions.qmd` is titled "Variables, Operators, and Functions" and contains
**no `def`, no `return`, and zero function-definition content**. Verified by grep: zero
matches. "Functions" in that file means calling built-ins such as `type()`, `round()`, `abs()`.

So 4b has no session-level ancestor. Build it from `cheatsheets/functions.qmd`:

- `def`/`return` syntax and a worked Celsius-to-Fahrenheit example: lines 16–43
- more `def`/`return` examples: lines 45–73
- default parameters: lines 96–117
- keyword arguments: lines 119–127

**Skip its "Higher-Order Functions" section, lines 128–144.** It passes a function as an
argument, which is out of scope, and line 137 is a list comprehension.

## Splitting `5b_cleaning_data.qmd` (458 lines)

| Topic | Lines | Goes to |
|---|---|---|
| sample DataFrame the whole file uses | 92–108 | both, or replace with microplastics |
| `.isnull()`, the axis explainer, `.dropna()`, `.fillna()` | 110–256 | 4a |
| `.duplicated()`, `.drop_duplicates()`, `subset=`, `inplace=` | 258–343 | 4a |
| `.dtypes`, `.astype(float)` | 345–382 | 4a |
| `pd.to_datetime()` | 384–396 | **cut**; dates are Day 6, and the EOD Field Note covers the one place Day 4 needs a date |
| `.str.capitalize()`, `.str.strip()` | 398–437 | 4c |

Two gaps to fill by writing new material: nothing in 5b covers derived-column arithmetic,
column-to-column math, or `np.log10`, and its `.str` coverage is only `.capitalize()` and
`.strip()`. `.lower()` and `.replace()` appear nowhere in a session.

## Banana-style EOD trims: marine microplastics

The 2025 file is `eod-practice/eod-day4.qmd`. Its five sections are Loading, Exploring,
Grouping, Filtering and Aggregating, and Simple Plots.

- **Cut section 3 whole** (tasks 3.1–3.3, lines 112–142) and **task 4.2** (lines 156–165).
  All four are groupby, which is Day 5. Where the EOD wanted a count per ocean, use
  `.value_counts()`, which has been WRITE since Day 2.
- **`parse_dates` becomes a Field Note.** The 2025 load line is
  `pd.read_csv(url, parse_dates=['Date'], date_format='%m/%d/%Y %I:%M:%S %p')`. That 12-hour
  format string with AM/PM is the "monster" the skeleton flags. Supply the whole line and ask
  students to run it as written.
- **Add a function task.** The 2025 EOD contains no `def` anywhere, so as it stands 4b gets no
  payoff in the evening. Add one task that defines a small named function and applies it with
  `.apply()`. A density classifier over `Measurement` is the natural candidate, since it also
  re-uses Day 3's `if`/`elif`/`else`.
- Keep the bare `.hist()` calls (tasks 5.1 and 5.4). Bare `.hist()` is part of Day 2's explore
  toolkit. No seaborn anywhere; that is Day 7.
- Keep `np.log10` (task 5.3). It is in the scope table and is the course's entire numpy budget.
- **Fix the handout/key drift**, which quality gate 4 will catch: task 2.2 differs materially
  between the two files; the tip text says "the `Dates` column" where the actual column is
  `Date`; the tip calls the parameter `parse_date` where the code uses `parse_dates`.
- **Field Note budget is 2.** `parse_dates` is one. Try to leave the second unspent.
- Confirm no `lambda` survives. (There is none in any 2025 Day 4 source; this is a check, not
  a fix.)

## Data

`https://eds-217-essential-python.github.io/data/marine_microplastics.csv`, 16,245 rows ×
22 columns. Already in `data/`, resolves offline through the shim.

**Build the missing-data teaching on this.** `Measurement` is null on exactly 5,792 rows,
which is exactly the number of rows where `Unit == 'pieces/10 mins'`. A naive
`.dropna(subset=['Measurement'])` silently deletes an entire unit category. That is the best
missing-data lesson available anywhere in the course, and it pays off Day 2's units warning.

Other counts, verified:

- `Oceans` null on 271 rows. Values: Atlantic 14,483 / Pacific 1,402 / Arctic 69 / Southern 20.
- `Unit`: pieces/m3 10,178 / pieces/10 mins 5,792 / pieces kg-1 d.w. 275.
- `Regions` null on 8,249; `SubRegions` null on 15,657. Both are legitimately mostly empty.
- `Date` is an object column of strings like `2/3/2017 12:00:00 AM`.

## The 4d colab has a dataset problem

`data/messy.csv` exists but is **five data rows**. That is a demo, not a 45-minute colab.
Either extend it to a few hundred rows with the same defects, or point 4d at a deliberately
degraded slice of the microplastics file. Decide before drafting, since the task list depends
on it.

Also fix, in `5c_cleaning_data.qmd` line 67 and its key line 68:
`messy_df['site'].str.lower().replace('sitec','site_c')` calls `Series.replace`, which does
whole-value replacement, not `.str.replace`. It silently does nothing. It also chains, which
4c's scope forbids. Neither file has YAML front matter; add it.

## Rules that apply

- **Rehearsal rule** (skeleton decision 10). A construct is WRITE in the EOD only if students
  have already written it unaided at least three times, across at least two sessions, in at
  least one of which they were sole author. The swap puts both fundamentals in the morning, so
  only the two afternoon sentence patterns need the exemption. **Record the audit table in the
  skeleton's Day 4 section**, in the format Day 3 uses.
- **No `lambda`, anywhere, including answer keys.**
- **Comprehensions are not taught.** They appear on Day 5 at reading level only.
- **No h1 headers.** Largest heading is `##`. Notebook title cells inside fenced blocks are
  exempt, since they are not rendered as headings.
- Every session opens with the Getting Started notebook ritual and closes with Key points and
  Resources. Copy the shape from `2a_reading_data.qmd`.
- The EOD opens with a short "today's sentences" box and closes with a grammar minute. Copy
  the shape from `eod-day3-2026.qmd`.

## Verify before committing

```bash
python tools/run_cells.py course-materials/interactive-sessions/4*.qmd \
                         course-materials/coding-colabs/4d_*.qmd \
                         course-materials/eod-practice/eod-day4-2026.qmd
grep -rn "lambda" course-materials/*/4*.qmd course-materials/eod-practice/eod-day4-2026.qmd
grep -c "🧭 Field Note" course-materials/eod-practice/eod-day4-2026.qmd   # must be <= 2
grep -rn "groupby" course-materials/eod-practice/eod-day4-2026.qmd        # must be empty
```

Then check that every construct in the EOD traces to a row in the scope table above, and that
every WRITE construct can be traced to the session and task where students first wrote it
unaided. That is quality gates 1 and 2, and they are the ones that catch real problems.

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
