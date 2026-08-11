# EDS 217: 2026 Day Skeleton (Draft 1)

**Created:** July 2026. Companion to `eod-concept-ledger-2025.md` (the construct source of truth).
**Status:** Design decisions resolved with Kelly on 2026-07-07 (see Decisions section). This is now the working spec for the 2026 build.

## Design principles

1. **Workflow as spine, segment as focus.** Every day (2–7) runs the complete Import→Visualize workflow in miniature; the day's teaching goes deep on one segment. The EOD is the day's "conversation": full workflow, with the focus segment done at WRITE depth and all prior segments done using already-mastered patterns.
2. **Alignment by construction.** An EOD may only require WRITE depth for (a) the day's focus constructs and (b) patterns from previous days. Anything else appears at ADAPT (scaffolded) or READ (given) depth, or via a Field Note (see 5).
3. **The rehearsal rule** (was the half-day rule; amended 2026-08-11, see decision 10). A construct may be required at WRITE depth in an EOD only if every student has already produced it unaided, from the pattern rather than by editing supplied code, in an earlier session that same course. Clock time is not the test. Rehearsal is. This addresses the 2025 same-day fragility (comprehensions D2, date parsing D4, seaborn D7), all three of which were taught once and then demanded without any student ever having typed them.

   The rule cuts both ways, and the second half is the one that protects students. **A construct students have only read, or only watched the instructor type, is never WRITE, no matter which half of the day it was taught in.** A morning demonstration with no student-authored practice is exactly as weak as an afternoon one.
4. **Vocabulary budget.** Each day introduces a bounded set of named constructs (target: ≤8 new WRITE-depth items/day). The per-day allocation tables below are the budget. If a session wants to teach something not in the table, it either displaces an item or waits.
5. **Field Notes (in-EOD backfill).** The 2025 `~`/`.copy()` callouts become a named, styled mechanism: a "🧭 Field Note" callout that teaches a small construct exactly where it's needed, always paired with a cheatsheet link. Budget: ≤2 per EOD. Field Notes are recorded in the ledger like any taught construct.
6. **Grammar minute.** Each day ends (last 5–10 min before EOD, or as the EOD's closing cell) with explicit consolidation: "here is the general form of the pattern you used three times today." Prevents idiom-only learning that can't generalize.
7. **Sentence patterns are the curriculum.** The eight recurring patterns from the ledger get named, introduced once each, and deliberately re-used on later days (spaced repetition). Fundamentals are taught as the grammar those sentences require, at the moment a sentence requires them.

## The 9-day map

| Day | Focus segment(s) | New sentence patterns | Fundamentals woven in (scope) | EOD "conversation" | Dataset |
|---|---|---|---|---|---|
| 1 | The Whole Game | (all previewed, none owned) | variables, strings, f-strings, `print`, types, notebooks | Run + lightly modify a complete workflow | Toolik climate |
| 2 | Import + Explore | missing-data sentence (diagnose half) | lists (literals, indexing, `len`, loop over); dicts (literal + lookup, as `rename` mapping) | Import an unfamiliar dataset, produce a written "data biography" | world cities or openaq |
| 3 | Filter + Sort | filter sentence; top-N sentence | booleans & comparison ops; `if/elif/else`; logical `&`/`|`/`~` | Rank and subset to answer "which/top" questions | Banana Index |
| 4 | Clean + Transform | derived-column sentence; missing-data sentence (treat half); string-cleaning sentence (basic) | functions (`def`/`return`/default args); `for` loops over columns/lists | Clean a messy dataset, build derived columns, write one reusable function | marine microplastics |
| 5 | Group + Aggregate | split-apply-combine sentence | dicts deepened (`.agg({...})`); loops over groupby; comprehensions (READ/gloss only) | Grouped comparison answering "which category differs?" | OpenAQ air quality (in repo: Goleta / Santa Barbara / CNSI stations) |
| 6 | Join + Reshape + Dates | join sentence; reshape (pivot_table, `concat`); datetime parsing + `.dt` | none new (consolidation day for fundamentals) | Multi-table analysis with a time dimension | Eurovision (+ population) |
| 7 | Visualize | the plotting sentences (matplotlib anatomy; seaborn `data=/x=/y=/hue=`) | none new | Full workflow ending in 2–3 polished figures | USDA hardiness zones |
| 8 | Project | — | — | Build 9-step workflow notebook (pairs) | student-chosen |
| 9 | Project + presentations | — | — | Present | student-chosen |

Framework change (**decided**): the 9-step workflow becomes **10 steps** by adding **Join/Reshape** between Group/Aggregate and Visualize. The ledger showed join and reshape are load-bearing in Days 6–7 EODs but unnamed in the framework, which is how pivot_table went untaught in 2025. Naming the step forces a teaching slot (Day 6) and adds a clean project-rubric line item.

---

## Per-day detail

### Day 1: The Whole Game

Goal: by 4:30pm every student has executed a complete data science workflow and knows the shape of the next eight days. Fundamentals are taught only to the depth the walkthrough needs.

Sessions (sketch):
- 1a: JupyterLab + notebooks (merge 2025's 1a+1b; compress)
- 1b: Variables, strings, f-strings, `print`, `type()`, scoped to "enough to read the walkthrough"
- 1c: The Whole Game, part 1 (Import→Aggregate on Toolik, instructor-led ADAPT: students run given code, then change one thing per step: a column name, a threshold)
- 1d: The Whole Game, part 2 (Visualize + export) + the 10-step framework named explicitly
- EOD: re-run the workflow with two or three prescribed modifications (different month, different variable). READ→ADAPT depth only.

Scope table:
| Construct | Scope taught | EOD depth |
|---|---|---|
| `import x as y` | recognize the three aliases | READ |
| `pd.read_csv(url)` | single positional arg only | ADAPT |
| `.head()/.info()/.describe()` | no-arg forms | ADAPT |
| `.isnull().sum()` | as a fixed phrase ("the health check"), not as chaining theory | READ |
| two-step groupby → select → `.mean()` | recognize and modify the key/column | ADAPT |
| `plt.plot`/`plt.bar` | modify labels only | ADAPT |
| f-strings | `f"text {var}"` only, no format specs | WRITE |

2025 carry-over: keep the "Coming Attractions" framing that resolved Day 1 in 2025, but upgrade student role from pure READ to ADAPT.

### Day 2: Import + Explore

Sessions (sketch):
- 2a: `read_csv` properly (url vs path; `index_col=`; what a DataFrame is; Series as a column). Lists arise: `df.columns.tolist()`, a list of column names to select.
- 2b: Exploration toolkit (`.head/.tail/.shape/.columns/.dtypes/.describe/.info`, `.value_counts()`, taught here explicitly since the ledger flagged it as never clearly taught). Dicts arise: `df.rename(columns={...})` as the motivating case for dict literal + lookup.
- 2c (colab): explore an unfamiliar dataset in pairs, produce 5 factual claims with evidence.
- 2d (live coding): lists and dicts as objects in their own right: 20 minutes of pure-Python grammar consolidating what the morning used in context (indexing, `.append`, loop over a list; dict get/set). This is the "grammar minute" scaled up for the two most important collections.
- EOD: "data biography" (import, explore, and characterize a new dataset; markdown answers with code evidence). Focus-segment WRITE; no filtering/grouping demanded.

Scope table:
| Construct | Scope taught | EOD depth |
|---|---|---|
| `pd.read_csv(url, index_col=)` | those two params only (no parse_dates yet) | WRITE |
| exploration methods | all no-arg forms | WRITE |
| `.value_counts()` | bare + `.head(n)` | WRITE |
| `df['col']` / `df[['a','b']]` | select one / list-of-columns | WRITE |
| `.isnull().sum()` | as a fixed phrase, the missing-data count (added 2026-08-10) | WRITE |
| list literal, indexing, `.append`, `len` | in service of column lists | WRITE |
| `for x in list` | taught in 2d, which is afternoon; a fundamental, so no decision 10 exemption | ADAPT |
| dict literal + `d[key]`, as `rename` mapping | NOT methods, NOT iteration, NOT nesting | WRITE |
| `.rename(columns=dict)` | columns direction only | WRITE |

WRITE constructs: 8. At the vocabulary budget cap, not over it.

Note (2026-08-10): `for x in list` was previously bundled into the list row at WRITE. That
conflicted with the half-day rule, since loops are taught in the afternoon 2d session. Split
out and demoted to ADAPT. The Day 2 EOD supplies the complete loop in a Field Note and asks
students only to change the list. Still correct under the amended rule (2026-08-11): loops are
a fundamental, and decision 10's exemption reaches named sentence patterns only.

### Day 3: Filter + Sort

Sessions (sketch):
- 3a (live coding): booleans, comparisons, `if/elif/else`, taught through data questions ("is this row's value above threshold?"), landing in the boolean-mask idea. Replaces 2025's abstract control-flow session.
- 3b: the filter sentence: `df[df['col'] <op> value]`, `&`/`|`/`~` with parentheses, `.isin(list)` (list vocabulary re-used), `.copy()` taught properly here (promoted from 2025's Day 4 callout).
- 3c: the top-N sentence: `.sort_values()` (one key; `ascending=`) + `.head(n)`; `.idxmax()/.idxmin()` as label-lookup companions.
- 3d (colab): ranking questions in pairs.
- EOD: Banana Index (relocated from 2025 Day 5: its Filter 15% / Sort 20% / Transform 18% profile matches this day nearly perfectly). Trim the function-writing tasks (functions move to Day 4). **Decided:** the set-intersection task is cut; sets drop to a cheatsheet gloss, and the "which foods appear in all three top-10s?" question is answered by visual comparison of the three lists.

Scope table:
| Construct | Scope taught | EOD depth |
|---|---|---|
| comparison + boolean ops | in mask context; bare `if/elif/else` for categorization | WRITE |
| filter sentence + `.copy()` | single and two-condition masks | WRITE |
| `.isin(list)` | list literal arg | WRITE |
| `.sort_values(col, ascending=False)` | single key | WRITE (rehearsal exemption, decision 10) |
| top-N sentence | as a named pattern | WRITE (rehearsal exemption, decision 10) |
| `.loc[row_label, col_label]` | scalar lookup only (Banana task 4 needs it) | ADAPT |
| `.idxmax()/.idxmin()` | on a single column, returning a label; paired with `.loc` (added 2026-08-11) | ADAPT |
| `.filter(like=)` | 🧭 Field Note (cheese task); sets task cut per decision 5 | ADAPT |
| `.drop(list, axis='columns')` | 🧭 Field Note in EOD setup | ADAPT |

Note (2026-08-11): `.idxmax()/.idxmin()` were named in the 3c session sketch above but had no
row in this table. Session 3C teaches them and the Banana EOD uses `.idxmax()` in a scaffolded
task, so they are recorded here at ADAPT. WRITE-depth constructs remain at five, under the
budget of eight.

Rehearsal exemption, recorded 2026-08-11 (decision 10). The top-N sentence is taught in 3C, an
afternoon session, and is required at WRITE depth in the same evening's EOD. The rehearsal
audit for that exemption:

| Requirement | Day 3 evidence |
|---|---|
| named sentence pattern | top-N sentence, from the ledger's eight |
| written unaided ≥3 times | 3 prompts in 3C, 6 questions in the 3D colab |
| across ≥2 sessions, student sole author | 3C "Test your knowledge" boxes; 3D colab |
| EOD restates the pattern verbatim | "Today's two sentences" box, above Part 1 |

The filter sentence is morning-taught and needs no exemption, but it meets the same bar: 5
prompts in 3B and 4 questions in the 3D colab.

### Day 4: Clean + Transform

**Built 2026-08-11.** Files: `4a_cleaning_data`, `4b_functions`, `4c_transforming_data`,
`4d_cleaning_messy_data` (colab), `eod-day4-2026`.

Sessions (**4b and 4c swapped 2026-08-11**; see the note below):
- 4a (morning): missing-data sentence completed (diagnose Day 2 → treat today: `.dropna()`, `.fillna()`); `.astype()`; `.duplicated()`/`.drop_duplicates()` with `subset=`.
- 4b (morning): functions, properly: `def`/`return`/default args/keyword args, motivated by "you've now written the same filter-sort-head three times" (fixes the 2025 Day 5 gap where functions were effectively learned inside the EOD); `.apply(named_func)` on a column as the payoff.
- 4c (afternoon): derived-column sentence (`df['new'] = expr`), column arithmetic, scalar broadcast, `np.log10`; basic `.str` methods (`.strip/.lower/.replace`, scoped; chains deferred to Day 7 Field Note).
- 4d (colab, afternoon): clean a deliberately messy dataset in pairs.
- EOD: marine microplastics (relocated from 2025 Day 4; now everything it needs is taught: masks Day 3, `~` and `.copy()` Day 3, derived column and `np.log10` today). Its groupby tasks are **cut**, not previewed: the ocean comparison is done with two filters instead.

Note (2026-08-11), why 4b and 4c swapped: `def`/`return` and `.apply` are **fundamentals**, and
decision 10's rehearsal exemption reaches named sentence patterns only. Left in the afternoon
they would cap at ADAPT in the same evening's EOD, re-creating the exact 2025 failure 4b exists
to fix. The derived-column and string-cleaning sentences **are** named patterns, so they sit in
the afternoon and take the exemption, rehearsed by 4d.

Dataset allocation: marine microplastics is the spine (4a cleans it, 4b applies functions to
it, 4c transforms it, the EOD carries it the whole way); banana_index returns for one section
of 4c so that column-to-column arithmetic has two related numeric columns to work with; the 4d
colab uses `messy_field_survey.csv`, authored for this course (see below).

Scope table:
| Construct | Scope taught | Session | EOD depth |
|---|---|---|---|
| `.dropna()/.fillna(value)` | whole-frame and single-column; `subset=[...]` | 4a, morning | WRITE |
| `.astype(str/int/float)` | single cast, no chains | 4a, morning | WRITE |
| `.duplicated()/.drop_duplicates()` | bare and `subset=[...]`; `keep=False` shown | 4a, morning | WRITE |
| `def f(x): return ...`; default args; keyword args | 1–3 param functions returning a value | 4b, morning | WRITE |
| `.apply(func)` | named function only, NO lambda | 4b, morning | WRITE |
| derived-column sentence | arithmetic of columns and scalars; one numpy function (`np.log10`) as "vectorized math comes from numpy", total intended numpy exposure for the course | 4c, afternoon | WRITE (rehearsal exemption, decision 10) |
| `.str.strip/.lower/.replace` | single method, no chaining | 4c, afternoon | WRITE (rehearsal exemption, decision 10) |
| `read_csv(parse_dates=, date_format=)` + `.dt.year` | 🧭 Field Note, both lines supplied (full datetime treatment Day 6) | EOD setup | ADAPT |
| `plt.hist(series)` | 🧭 Field Note, line supplied; extends Day 1's `plt.plot()`/`plt.bar()` | EOD task 15 | ADAPT |

Seven WRITE constructs, under the budget of eight. Field Notes in the EOD: 2, the budget.

Rehearsal exemption, recorded 2026-08-11 (decision 10). Both afternoon-taught sentence patterns
are required at WRITE depth in the same evening's EOD. The audit:

| Requirement | derived-column sentence | string-cleaning sentence |
|---|---|---|
| named sentence pattern | yes, from the ledger's eight | yes, from the ledger's eight |
| written unaided ≥3 times | 4C "Test your knowledge" ×3 (latitude→radians, emissions ratio, log10 per litre); 4D tasks 14, 15, 16 | 4C "Test your knowledge" ×1 (sampling method), 4D tasks 7 and 8 (four separate `.str` statements) |
| across ≥2 sessions, student sole author | 4C TYK boxes (sole author); 4D colab | 4C TYK box (sole author); 4D colab |
| EOD restates the pattern verbatim | "Today's three sentences" box, above Setup | same box |

The morning constructs need no exemption, but quality gate 2 asks where each was written
unaided anyway: `.dropna`/`.fillna` in 4A TYK ×2 and 4D tasks 9–10; `.astype` in 4A TYK and 4D
tasks 8 and 10; `.drop_duplicates` in 4A TYK and 4D task 6; `def`/`return` in 4B TYK ×4 and 4D
tasks 15–16; `.apply` in 4B TYK ×1 and 4D tasks 15–16.

Deviation from the build brief, recorded 2026-08-11: the brief said bare `.hist()` was already
in Day 2's explore toolkit and could be kept without a Field Note. It is not — `.hist()` appears
nowhere in the 2026 Days 1–3, and the only plotting students have is `plt.plot()`/`plt.bar()`
from the Day 1 Whole Game. The EOD therefore uses `plt.hist()`, which matches that prefix and
Day 7's matplotlib base, and spends the second Field Note on it. The `.hist()` → `plt.hist()`
substitution is the reason the Field Note budget is fully spent.

New dataset: `data/messy_field_survey.csv`, 320 rows × 7 columns, authored for this course
(generator: `tools/make_messy_field_survey.py`, seed 217). `data/messy.csv` is five data rows,
too small for a 45-minute colab; Kelly chose to author a larger one rather than degrade a real
file. Planted defects, each fixable with Day 4 scope only: 20 exact duplicate rows; 36 spellings
of 6 site labels (case, leading/trailing space, hyphen-for-underscore); `pH` typed as text
because 24 values use a decimal comma; blanks in three measurement columns; blanks in
`n_replicates` forcing it to float; 9 `-999.0` datalogger sentinels in `temperature_c`; a column
name with a space. Cleaned it runs 320 → 300 → 264 → 255 rows and shows a real gradient (sites
c and f warm, acidic, oxygen-poor; sites a and d cool, alkaline, oxygen-rich).

### Day 5: Group + Aggregate

Sessions (sketch):
- 5a: split-apply-combine sentence: `groupby(key)['col'].mean()`, taught in BOTH the two-step and one-line forms, explicitly ("these are the same sentence"; fixes the 2025 D4 form gap).
- 5b: `.agg()` with a list and with a dict (dict vocabulary deepened on schedule); `.count/.sum/.max/.min`; grouped result → `.sort_values()` → `.head()` (re-using Day 3's top-N sentence on grouped output).
- 5c (colab): grouped-comparison questions.
- 5d (live coding): loops over `groupby` ("when a sentence isn't enough"); comprehensions shown as READ-level "you will see this in the wild" with cheatsheet link.
- EOD (**decided**): OpenAQ air-quality data (already in `data/`: Goleta, Santa Barbara, CNSI station files). Natural grouping questions: by station, by parameter, by hour/day. It is join-free by construction. Task design is new work; note the repo's openaq CSVs have ~4,900 uncommitted appended rows from the 2025 class to reconcile first.
- Multi-key groupby: taught here at ADAPT scope only (show the two-key form and what a MultiIndex looks like; `.reset_index()` as the escape hatch). The 2025 D6 `groupby(...).idxmax()` MultiIndex construct is CUT from EOD WRITE expectations.

Scope table:
| Construct | Scope taught | EOD depth |
|---|---|---|
| split-apply-combine, both forms | single key, single column, single agg | WRITE |
| `.agg(['mean','max'])` / `.agg({col: fn})` | list and dict args | WRITE |
| grouped → top-N | pattern reuse | WRITE |
| multi-key groupby + `.reset_index()` | recognize and unstick; not compose | ADAPT |
| loop over groupby | `for name, group in ...` shown | ADAPT |
| comprehensions | READ/gloss + cheatsheet | READ |

**BUILT 2026-08-11 (commit 83055c6).** Files: `5a_grouping_data.qmd`,
`5b_aggregating_data.qmd`, `5c_grouped_comparisons.qmd` colab,
`5d_loops_over_groups{,_notes}.qmd`, `eod-day5-2026.qmd`. Scope table above was met exactly; no
row was added or promoted. 86/86 python cells verified offline against pandas 2.3.3.

Two build decisions, both Kelly's:

1. **The EOD spends one Field Note, not two.** The brief offered Option A (separate notes for
   `pd.concat` and for `.str[11:13]`) or Option B (neither, one station at a time). Neither was
   taken. Both lines are *setup*, so they share a single combined Field Note before Task 1. The
   EOD gets Option A's full richness and still holds one Field Note in reserve.
2. **WRITE stays at three.** The brief flagged real headroom under the budget of eight and
   invited spending it. It was left unspent, deliberately, for Days 6 and 7. Group-and-aggregate
   is one sentence in two forms; the day buys fluency by repetition rather than coverage.

Rehearsal-rule audit (quality gate 2). **No exemption needed** — all three WRITE constructs are
morning-taught in 5a/5b:

| WRITE construct | Taught | Written unaided |
|---|---|---|
| split-apply-combine, both forms | 5a, morning | 5a "Test your knowledge" x4; 5c tasks 1, 2, 3, 6, 9, 12, 14; EOD tasks 1, 4, 6 |
| `.agg()` list and dict forms | 5b, morning | 5b "Test your knowledge" x2; 5c tasks 5, 7, 9, 14; EOD tasks 2, 7, 9, 16 |
| grouped result -> top-N | 5b, morning | 5b "Test your knowledge" x2; 5c tasks 1, 9; EOD tasks 6, 18 |

Dataset allocation, chosen so each session inherits a table students already trust:
`messy_field_survey` (5a and 5d, rebuilt clean from the 4d colab), `national_parks` (5b, from the
3d colab), `marine_microplastics` (5c, from the Day 4 EOD), OpenAQ (EOD, all three stations).

The 5a payoff is real and was not arranged: across the six survey sites, mean dissolved oxygen
and mean temperature rank the sites in exactly mirrored order, no exceptions. The 5b argument for
`.agg(['count', ...])` is the NE region, which has the highest mean visitor count of any region
and contains exactly two parks. The EOD closes on mean ozone by hour, which climbs monotonically
from 0.0111 ppm at hour `'06'` to 0.0309 at `'14'` and falls back, a ratio of 2.77.

### Day 6: Join + Reshape + Dates

The new-content day that fixes the two ❌ never-taught findings (pivot_table, concat). No new fundamentals; Python grammar consolidates.

Sessions (sketch):
- 6a: join sentence: `pd.merge(a, b, on=)` then `left_on=/right_on=` (mismatched keys taught explicitly: the recurring D6/D7 form), `how='inner'/'left'` with a picture.
- 6b: reshape: `pd.concat([...])` for stacking; `pivot_table(index=, columns=, values=)` taught with a small worked example (single-level index first, then the multi-column index form Day 7's EOD uses); `.reset_index()` re-used.
- 6c: dates: `pd.to_datetime(col, format=)`, `.dt.year/.month`, format strings scoped to `%Y %m %d` (the D4-2025 `%I:%M:%S %p` monster becomes a Field Note wherever its dataset is used).
- 6d (colab): two-table exercise.
- EOD: Eurovision (its Group 20% is now review; Join + dates are the day's focus at WRITE depth). The decade-winner task keeps the two-step scaffold, and the MultiIndex `.idxmax()` step becomes ADAPT with a Field Note, or is redesigned to `reset_index()` + top-N per decade.

Scope table:
| Construct | Scope taught | EOD depth |
|---|---|---|
| `pd.merge` incl. `left_on/right_on`, `how='left'` | two-table, single-key | WRITE |
| `pd.concat([a, b])` | row-wise, same columns | WRITE |
| `pivot_table(index=, columns=, values=)` | single agg (default mean); reference resulting columns | WRITE |
| `pd.to_datetime` + `.dt.` accessors | `%Y/%m/%d` formats; year/month accessors | WRITE (afternoon; exemption taken, audit below) |
| `value_counts().reset_index()` + rename | as the "Series to table" move (fixes 2025 D6 gap) | WRITE |
| MultiIndex `.idxmax()` on groups | **CUT** — redesigned away, see below | — |

**BUILT 2026-08-11 (commit 0aabec7).** Files: `6a_joining_data.qmd`,
`6b_reshaping_data.qmd`, `6c_dates.qmd` (name kept, content replaced),
`6d_two_table_exercise.qmd` colab, `eod-day6-2026.qmd`. 74/74 python cells verified offline
against pandas 2.3.3 with `FutureWarning` and `DeprecationWarning` escalated to errors. Scope
table met exactly; no row added or promoted. **Zero Field Notes spent in the EOD** — the full
budget of two is unspent, which the brief called a good outcome rather than a suspicious one.

Four build decisions:

1. **The MultiIndex `.idxmax()` row is CUT, not demoted.** The EOD's decade-winner task is
   rebuilt on 5d's `for name, group in df.groupby(key):` loop plus `.agg(['count','mean'])`,
   `.reset_index()`, the top-N sentence and `pd.concat()`. Every construct in it was taught. It
   reproduces the original seven decade winners exactly, and the `count` column it now carries is
   what makes two of those winners visibly untrustworthy (France 1950s on 3 entries, Serbia 2000s
   on 2).
2. **The Eurovision merge asymmetry was solved without editing a data file.** The brief proposed
   trimming three or four countries from `eurovision_country_populations.csv` because all 52
   countries appear in both files. Unnecessary: restrict the entry counts to **1990 onwards** and
   **Morocco** drops out, because Morocco has competed exactly once, in 1980. Inner returns 51
   rows, `how='right'` returns 52 with one null, and the missing row is a real fact about the
   contest rather than a manufactured one. `eurovision_country_populations.csv` is unchanged.
3. **`//` integer division is avoided, not Field-Noted.** It is taught nowhere in the 2026
   Days 1–5 (`1d_operators_functions.qmd`, which has the operator table, is a 2025 orphan). The
   decade column is `(col.dt.year / 10).astype(int) * 10`, and `4a_cleaning_data.qmd` already
   states that `.astype(int)` truncates toward zero. That is the whole reason no Field Note was
   needed.
4. **`.corr()` was drafted into 6a and then removed** for scope discipline; it is not in the
   scope table. 6a's joined-table payoff is the top-N sentence instead, which is a better artifact
   anyway: four of Goleta's ten smokiest hours are at 01:00, when ozone is near its daily minimum,
   so the two pollutants are not two symptoms of one process.

Rehearsal-rule audit (quality gate 2). Four of the five WRITE constructs are **morning-taught**
and need only the base rule. The fifth is afternoon-taught and **takes the exemption**:

| WRITE construct | Taught | Written unaided |
|---|---|---|
| `pd.merge`, incl. `left_on`/`right_on` and `how=` | 6a, morning | 6a "Test your knowledge" x3; 6d tasks 2, 3, 15; EOD tasks 15, 16 |
| `pd.concat([a, b])` | 6b, morning | 6b "Test your knowledge" x2 (reordered stack, two-file stack); EOD task 10 |
| `pivot_table(index=, columns=, values=)` | 6b, morning | 6b "Test your knowledge" x1 (transpose); 6d tasks 11, 15; EOD tasks 19, 20 |
| `value_counts().reset_index()` + rename | 6b, morning | 6b "Test your knowledge" x1 (per-parameter count table); EOD task 14 |
| `pd.to_datetime` + `.dt.` accessors | **6c, afternoon** | **exemption taken**: (a) named "the parsing sentence"; (b) written unaided 4x; (c) across 6c ("Test your knowledge" x2, sole author) and the 6d colab (tasks 6, 7); (d) the EOD restates `pd.to_datetime(column, format='%Y')` and `column.dt.year` verbatim in "Today's sentences"; (e) this table |

Dataset allocation, continuing Day 5's rule that each session inherits a table students already
trust: **OpenAQ Goleta** (6a, one file split into two tables and joined back), **OpenAQ all three
stations** (6b, which discharges the Day 5 EOD's supplied `pd.concat` block by making students
write it), **Toolik** (6c, from Day 1 and Day 2), **GISTEMP + Mauna Loa** (6d colab), **Eurovision**
(EOD).

The colab-callback pattern held, but it moved into the morning sessions rather than the colab.
6a and 6b both re-open Friday evening's OpenAQ work with Tuesday's tools, and 6b opens by naming
the promise the Day 5 EOD Field Note made ("It is Tuesday"). 6c discharges the same Field Note's
second half. The 6d colab is a genuine new build on GISTEMP and Mauna Loa, because both morning
sessions had already spent the callback.

Findings worth keeping, all verified:

- Goleta records **no ozone at all at hour 03**, on any of the 31 days. An inner join of the
  station's o3 and pm25 tables silently drops those 30 rows, and every one of them is the same
  hour of the day. This is 6a's central lesson and it is real, not arranged: inner 704, left 711
  (7 nulls), right 734 (30 nulls), outer 741.
- `national_parks.csv` has an **eighth region code, `NT`**, on 76 rows, all of them the Blue Ridge
  Parkway. A seven-row hand-written lookup table therefore loses a real American landmark to an
  inner join without warning. This is 6a's `left_on`/`right_on` example.
- Toolik's `Date` column is the **integer** `19880601`, so `format='%Y%m%d'` is exactly in scope,
  and the file's own `Year` and `Month` columns let students verify the parse for free (both
  match on all 11,171 rows). The payoff: comparing 1988–1998 with 2009–2018 month by month,
  January is **+3.5 °C** and October **+4.3 °C**, while July is **−0.8 °C**. Toolik's warming is a
  cold-season phenomenon, and it is invisible in an annual mean.
- GISTEMP (1880–2024, 1,736 months) and Mauna Loa (1958–2024, 796 months) merge to **796 rows
  inner and 1,736 left, with 940 nulls**. The best real inner-vs-left contrast in the whole data
  directory, and the decision is a scientific one rather than a technical one.
- Eurovision **2020 has 41 entries and zero non-null `points_final`**, because the contest was
  cancelled. The 2025 EOD's `fillna(0)` turned that into a real decade winner. The 2026 EOD
  filters 2020 out and spends a callout on why.
- Eurovision entries per million (1990 onwards): San Marino 431, Andorra 110, Iceland 109,
  Monaco 100, Malta 82; bottom, Yugoslavia 0.13, Russia 0.15. The population column is undated and
  clearly historical (Iceland 255,866), which the EOD asks students to name as a limitation rather
  than work around.

### Day 7: Visualize

Sessions (sketch):
- 7a: matplotlib anatomy (figure/axes, `plt.figure(figsize=)`, labels, titles, `xticks(rotation=)`, `tight_layout`). 2025's 7a largely survives, now with the D6-2025 sequencing bug fixed because no earlier EOD demands styled matplotlib anymore (D4 EOD keeps only bare `.hist()`, taught as part of Explore's toolkit).
- 7b: seaborn: `sns.scatterplot/barplot/histplot` with `data=/x=/y=/hue=`; the Series `.values/.index` barplot idiom taught explicitly (2025 flag).
- 7c (colab): Palmer penguins exploration (rebuilt around the three seaborn functions; 2025's 7c did not survive, see below).
- 7d (**decided**): project kickoff. Form teams, browse dataset sources (final_project.qmd list), draft the analysis question. Decompresses Day 8; students start the project with the full 10-step grammar fresh. Fallback if Day 7 runs hot: convert to buffer/review and push kickoff to Day 8 morning.
- EOD: USDA hardiness zones (everything it needs is now taught: merge D6, pivot_table D6, concat D6; the `.str.split().str.get().astype()` chain in setup becomes a 🧭 Field Note; seaborn is taught the same day). **Revisit under decision 10 when Day 7 is built.** The plotting sentences are named patterns, so the rehearsal exemption is available if 7c gives students enough sole-author practice with `data=/x=/y=/hue=`. If it does, the EOD's seaborn tasks can be WRITE. If it does not, they provide the call skeleton and students fill mappings, as originally planned. Decide by auditing 7c, not by the clock.

Scope table (drafted in the flight-packet brief, finalised at build time):

| Construct | Scope taught | Session | EOD depth |
|---|---|---|---|
| `plt.figure(figsize=)` | figure sizing only, inches | 7a, morning | WRITE |
| `plt.xlabel/ylabel/title` | labels and a title, units required in axis labels | 7a, morning | WRITE |
| `plt.tight_layout()` | as a closing line | 7a, morning | WRITE |
| `plt.legend()` with `label=` | one `label=` per series, one `legend()` per figure | 7a, morning | READ (the EOD never puts two series on one axes) |
| `plt.xticks(rotation=, ha=)` | rotation of tick labels | 7a, morning | READ (see correction 2) |
| `plt.plot` / `plt.scatter` | two sequences, ordered vs unordered x | 7a, morning | READ |
| `sns.scatterplot(data=, x=, y=, hue=)` | those four arguments | 7b, morning | WRITE |
| `sns.histplot(data=, x=, hue=)` | single variable; heights are counts | 7b, morning | WRITE |
| `sns.barplot`, incl. `x=series.values, y=series.index` | both forms; the Series idiom taught explicitly, and the `data=` form's silent mean flagged | 7b, morning | WRITE |
| `.str.zfill(5)` + `.str.split().str.get(n).astype(int)` | one combined 🧭 Field Note in EOD setup | — | ADAPT |
| index-aligned Series subtraction | **CUT** — redesigned away, see correction 3 | — | — |

Six WRITE constructs, against a budget of eight.

**BUILT 2026-08-11.** Files: `7a_matplotlib.qmd`, `7b_seaborn.qmd`, `7c_penguins.qmd` (colab),
`7d_project_kickoff.qmd` (new, no ancestor), `eod-day7-2026.qmd`. `day7.qmd` and the navbar
rewired; `final_project.qmd` updated from nine steps to ten. 60/60 python cells verified offline
against pandas 2.3.3 / seaborn 0.13.2 with `FutureWarning` and `DeprecationWarning` escalated to
errors. **One Field Note spent in the EOD**, of a budget of two.

Six corrections to the build brief:

1. **7a is a rebuild, not a trim.** The brief said to cut about 320 of `7a_visualizations_1.qmd`'s
   740 lines. What survives that cut is entirely `np.linspace`/`np.sin` synthetic waveforms, and
   numpy appears in no 2026 session at all. 7a is therefore built on **Toolik**, opening on the
   figure students drew on Day 1 (`plt.plot(monthly_means)`, under a box promising "you will learn
   how visualization really works on Day 7") and closing on 6c's early-versus-late monthly
   comparison. Nothing from the 2025 file is retained verbatim; only its section order survives.
   `plt.xlim`/`plt.ylim` were dropped too, since they are not in the scope table and nothing needs them.
2. **`plt.xticks(rotation=, ha=)` is READ in the EOD, not WRITE.** None of the EOD's six figures
   needs it: the only bar chart is horizontal, and 7b argues for horizontal bars precisely because
   they make rotation unnecessary. It is still taught in 7a, with its own unaided "Test your
   knowledge", because the Day 8–9 project will want it.
3. **The index-aligned subtraction is redesigned away**, as the brief preferred, so the second
   Field Note is unspent. The top-ten-states task groups the `pivot_table` difference by `state`,
   which is Day 5 and Day 6 vocabulary end to end.
4. **The `longitude < -60` filter is one corrupted record, not a territory filter.** These files
   cover the contiguous 48 states plus DC, with no Alaska, Hawaii or Puerto Rico, so nothing is
   being excluded on geographic grounds. Exactly one zip code exceeds −60: **22350, Alexandria VA,
   recorded at 48.31 N, 2.12 W**, which is in the sea off Brittany. Two rows out of 80,455, and
   they flatten the map into the left third of the figure. The EOD therefore makes students draw
   the broken figure, notice it, and find the row, rather than handing them the filter as the 2025
   version did. It is the clearest demonstration in the course of what a plot does that
   `.describe()` does not.
5. **`sns.load_dataset("penguins")` is cached** to `data/penguins.csv` (344 × 7) and 7c reads it
   from the course site like every other file. The colab is otherwise a rebuild: `relplot`,
   `pairplot`, `regplot`, `lmplot`, `jointplot` and `heatmap` are all out of scope and gone, and
   `.corr()` stays uncalled per the Day 6 decision. `pd.crosstab` was drafted and replaced with
   `pivot_table(aggfunc='count')`, which is taught.
6. **`final_project.qmd` said nine steps.** It now says ten, names Join/Reshape as step 9, and
   points at `the-data-science-workflow.qmd`. 7d sends students there, so the mismatch would have
   been visible in the room.

Rehearsal-rule audit (quality gate 2). **All six WRITE constructs are morning-taught**, so the
base rule applies and no exemption is needed. Day 7 is the second clean case after Day 5:

| WRITE construct | Taught | Written unaided |
|---|---|---|
| `plt.figure(figsize=)` | 7a, morning | 7a "Test your knowledge" ×3; 7b ×3; 7c questions 5–16 |
| `plt.xlabel/ylabel/title` | 7a, morning | 7a ×3; 7b ×3; every figure in 7c |
| `plt.tight_layout()` | 7a, morning | 7a "Test your knowledge" (precipitation counts by year); 7b "Test your knowledge" (conductivity bars) |
| `sns.scatterplot(data=, x=, y=, hue=)` | 7b, morning | 7b "Test your knowledge" ×1; 7c questions 8, 9, 10, 11, four sole-author uses |
| `sns.histplot(data=, x=, hue=)` | 7b, morning | 7b "Test your knowledge" ×1; 7c questions 5, 6, 7 |
| `sns.barplot` + the Series idiom | 7b, morning | 7b "Test your knowledge" ×1; 7c questions 13, 15, 16 |

Dataset allocation: **Toolik** (7a, where Day 1's figure and 6c's table are both re-opened),
**messy_field_survey** (7b, where Friday's grouped means become one visible relationship),
**Palmer penguins** (7c colab, genuinely new), **hardiness zones + zip code database** (EOD).
The colab callback again lived in the **morning** sessions, as on Day 6, which freed 7c for new
data.

Verified numbers, so a later session need not recompute:

- Toolik early-versus-late monthly change, plotted as bars, is the day's best "the table said it,
  the picture shows it" moment: January **+3.46 °C**, October **+4.27 °C**, February +2.48,
  November +2.37, December +1.20, against March −2.02, April −1.45, May −0.91, July −0.77. The
  two-line version of the same figure is honest and nearly useless, because a 3.5 °C signal sits
  on an axis that must span 35 °C. 7a spends a section on exactly that.
- Toolik air temperature has **31 complete years except 1988** (214 days). Precipitation is
  another story: 1995 has **182** readings, 1994 has 273, 1990 has 277, 2004 has 314. That is the
  rotation "Test your knowledge" and it earns the caveat in the one after it.
- `messy_field_survey` cleaned: temperature against dissolved oxygen is a clean negative
  relationship, and with `hue='site'` the six sites lie **along** it in exactly the order 5A's two
  grouped means gave (d, a, b, e, c, f). One argument turns two printed lists into one claim.
- Penguins (333 rows after `dropna()`): bill length against bill depth is **negative across the
  pooled data and positive within every species**, which is Simpson's paradox, revealed by
  `hue='species'` and by nothing else. Adélie and Chinstrap mean body mass are 3706 g and 3733 g, nearly identical
  despite obviously different bills, which is what makes question 14 work. Chinstrap appear only on
  Dream and Gentoo only on Biscoe, so island and species are confounded.
- Hardiness zones: 2012 is 40,534 × 4 and 2023 is 39,921 × 4, no nulls, `trange` is **always**
  exactly three whitespace-separated tokens in both years, so the `.str` chain yields zero nulls.
  Stacked: 80,455. Mean `trange_min` **−1.900 °F in 2012 and +1.017 °F in 2023, a difference of
  2.917**. The merge against the zip code database loses **103 rows covering 63 zip codes**.
- The pivoted difference table has 40,492 rows, of which **634 have a null `temp_diff`** (a zip
  code present in one map and not the other). `temp_diff` takes only **eleven distinct values, all
  multiples of five**: 0 on 16,574 zip codes and +5 on 22,374, with a thin tail out to −30 and
  +25. It is a zone-boundary crossing, not a measured temperature change, and the EOD's histogram
  is what makes that unmissable. Classified: **warmer 22,888, unchanged 16,574, colder 396**.
- The extremes are all mountains: the five largest increases are 95604 CA (+25), 59761 MT (+20),
  37729 TN (+15), 80442 CO (+15), 83246 ID (+15); the largest decreases are 95321 CA (−30), 95644
  CA (−20) and 95223 CA (−20), all in the Sierra Nevada. Six zones of movement in eleven years is
  a methodology change in terrain with huge within-zip-code elevation range, not a climate signal.
- Top ten states by mean increase, with the counts that matter: **DC 7.18 on 275 zip codes** (one
  city), TN 4.37 (774), **DE 4.35 on 93**, MO 4.12 (1,142), AL 4.02 (803), WV 4.00 (842), KY 3.99
  (929), MD 3.82 (599), GA 3.72 (937), AR 3.68 (690). Bottom five: **CA 0.82 on 2,552 zip codes**,
  the largest count in the file, then AZ 0.99 (520), ND 1.00 (404), IA 1.20 (1,042), UT 1.31 (336).

Images claimed: `matplotlib_panda.jpeg` → 7a, `panda_seaborn.jpeg` → 7b, `horst-samples.jpg` →
7c, `ds_friends.jpg` → 7d, and a new `eod-practice/images/hardiness_panda.jpeg` (the 2025 EOD's
gardening panda, pulled off the MidJourney CDN and committed so the page renders offline).
`visualization_1.jpeg` stays on `day7.qmd`.

### Days 8–9: Project

Unchanged from 2025 in structure (pairs, 9→10-step workflow notebook, day 9 afternoon presentations). The 10-step framework gives project rubrics one new line item (join or reshape used where appropriate; keep "even if minimal" allowance).

---

## Session reuse map (2025 → 2026)

| 2025 asset | 2026 fate |
|---|---|
| 1a JupyterLab, 1b Notebooks | merge → 1a |
| 1c variables/strings, 1d operators/functions | compress → 1b (operators fold into D3; functions move to D4) |
| EOD day 1 (Toolik) | keep; upgrade READ→ADAPT; becomes the Whole Game anchor (1c/1d + EOD) |
| 2a lists, 2b dicts | compress → 2d live-coding grammar session; content resurfaces inside 2a/2b in pandas context |
| 2c colab (lists/dicts/sets) | retire as-is; sets drop to cheatsheet gloss |
| 2d comprehensions | retire from core; content → D5 gloss + cheatsheet |
| EOD day 2 (classmates) | retire (pure-Python EOD conflicts with workflow-spine design); salvage tasks into 2d grammar session |
| 3a/3b control flows | rebuild → 3a (data-motivated booleans/conditionals) |
| 3c arrays & Series | **retire** (numpy de-emphasis; Series concepts fold into 2a) |
| 3d colab Series | retire; salvage into D5 colab |
| EOD day 3 (test scores) | salvage as D5 warm-up or retire |
| 4a DataFrames | split across 2a/2b |
| 4b colab | adapt → D4 or D5 colab |
| 4c workflows (9-step) | promote → Day 1 Whole Game framing (10-step) |
| 4d import/export live-coding | split: import basics → 2a; parse_dates → 6c; export → Whole Game + cheatsheet |
| EOD day 4 (microplastics) | keep → D4 EOD (trim groupby tasks) |
| 5a selecting/filtering | rebuild → 3b/3c |
| 5b cleaning | keep → 4a/4b |
| 5c cleaning colab | keep → 4d colab |
| EOD day 5 (Banana Index) | keep → **D3 EOD** (trim functions + set tasks) |
| 6a grouping/joining/sorting | split: grouping → 5a/5b; joining → 6a; sorting → 3c |
| 6b data-manipulation colab | adapt → 6d colab |
| 6c dates | keep → 6c |
| EOD day 6 (Eurovision) | keep → D6 EOD (redesign decade-winner step) |
| 7a/7b/7c visualization | keep → 7a/7b/7c |
| EOD day 7 (hardiness zones) | keep → D7 EOD (Field-Note the str chains) |
| NEW build required | 6b reshape session (pivot_table/concat), the only wholly new session; D5 EOD (new or adapted); D2 EOD (data biography) |

Net new construction: one session (6b reshape), two EODs (D2, D5), heavy rework of Day 1–3 sessions. Days 4–7 are mostly relocation and trimming.

## Decisions (resolved with Kelly, 2026-07-07)

1. **Framework: 10 steps.** Join/Reshape added between Group/Aggregate and Visualize. Taught in Day 6; new line item in the project rubric (keep the "even if minimal" allowance).
2. **D5 EOD dataset: OpenAQ** air-quality data already in `data/` (Goleta, Santa Barbara, CNSI). New task design required; reconcile the uncommitted 2025 appended rows in those CSVs first.
3. **Lambda: cut entirely.** No session, no EOD, no answer key may use lambda. `.apply(named_func)` and named functions with `key=` cover every need. Enforce via the pre-course drift check.
4. **Comprehensions: READ-only gloss.** Reading fluency taught in the D5 grammar session + cheatsheet; never required at WRITE depth in any EOD.
5. **Sets: cut from D3.** Set-intersection task removed from the Banana Index EOD; sets become a cheatsheet gloss only.
6. **Day 7 slot 4: project kickoff** (teams, dataset browsing, question drafting). Fallback if the day runs hot: buffer/review, kickoff moves to Day 8 morning.
7. **Backfill mechanism: "Field Note," hard cap 2 per EOD.** The cap is a design constraint, not a guideline: a third needed Field Note means the day's teaching or the EOD is misdesigned and must change.
8. **`.isnull().sum()` is WRITE on Day 2** (2026-08-10). Taught as a fixed phrase, not as
   chaining theory. Takes the eighth and last WRITE slot in the Day 2 vocabulary budget.
9. **Day 2 EOD keeps one Field Note** (2026-08-10): the optional loop over a column list. The
   complete pattern is supplied, students change only the list, and the task is optional. This
   is the rehearsal rule working as designed. Loops are taught in the afternoon 2d session and
   no session asks a student to write one, so ADAPT is the ceiling. The exemption in decision
   10 does not apply, because `for x in list` is a fundamental and not a named sentence
   pattern.

10. **The half-day rule becomes the rehearsal rule** (2026-08-11, Kelly). A construct taught in
    an afternoon session may be required at WRITE depth in that same evening's EOD, but only
    under all five of the following conditions. Any construct that fails even one of them is
    ADAPT at most.

    a. It is a **named sentence pattern**, one of the eight in the ledger. Fundamentals
       (loops, comprehensions, `def`), library idioms, and format strings never qualify. Those
       keep the original half-day separation.
    b. Students have **written it themselves, unaided**, at least three times, producing it
       from the named pattern rather than by editing supplied working code.
    c. That practice is spread across **at least two sessions**, in at least one of which the
       student is the sole author: a colab, a practice block, or a "Test your knowledge"
       prompt. Coding along while the instructor types the same line does not count.
    d. The EOD **restates the pattern verbatim once**, near the top, with no worked values in
       it. The Day 3 "Today's two sentences" box is the reference implementation.
    e. The day's scope table **marks the row** as a rehearsal exemption and the day's section
       carries the audit table showing where (b) and (c) were satisfied.

    Rationale, in Kelly's terms: a strict half-day separation makes it nearly impossible to
    teach anything new after lunch, and the workaround is worse than the problem. Material
    pushed out of the same-day EOD to protect students arrives instead on the following
    morning, unpracticed, competing with that day's new material. The 2025 failures were not
    caused by afternoon timing. They were caused by students being asked to produce something
    they had never once produced.

    **The backslide this must never permit:** an EOD demanding grammar the students have only
    read. If you cannot name the session and the specific task where students wrote a construct
    from scratch, it is not WRITE, and no amount of same-day proximity changes that.

## Risks

- **Day 2 is the experiment's crux.** Students touch DataFrames on day 2 with one day of Python. If the "data biography" EOD works, the design works. Mitigation: keep 2d (pure-Python grammar session) robust, and hold 2025's 2a/2b sessions ready as fallback inserts.
- **Fundamentals debt surfacing late.** A student who never solidifies loops may not notice until Day 5. Mitigation: grammar minutes + the D2/D5 live-coding grammar sessions are the designated debt-collection points; colab pairing surfaces struggling students early.
- **Instructor context-switching in sessions** (the original worry): bounded by the vocabulary budget: each session teaches its scope-table rows and nothing else; anything a dataset tempts us toward that isn't in the table becomes a Field Note or a cheatsheet link.
- **Schedule check:** all of this assumes the 2025 4-sessions+EOD daily rhythm and a 7+2 day calendar. Verify against actual September 2026 dates before allocating sessions to clock times.
