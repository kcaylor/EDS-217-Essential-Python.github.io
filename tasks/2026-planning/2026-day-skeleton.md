# EDS 217: 2026 Day Skeleton (Draft 1)

**Created:** July 2026. Companion to `eod-concept-ledger-2025.md` (the construct source of truth).
**Status:** Design decisions resolved with Kelly on 2026-07-07 (see Decisions section). This is now the working spec for the 2026 build.

## Design principles

1. **Workflow as spine, segment as focus.** Every day (2–7) runs the complete Import→Visualize workflow in miniature; the day's teaching goes deep on one segment. The EOD is the day's "conversation": full workflow, with the focus segment done at WRITE depth and all prior segments done using already-mastered patterns.
2. **Alignment by construction.** An EOD may only require WRITE depth for (a) the day's focus constructs and (b) patterns from previous days. Anything else appears at ADAPT (scaffolded) or READ (given) depth, or via a Field Note (see 5).
3. **The half-day rule.** Constructs taught in the afternoon sessions appear in that day's EOD at ADAPT depth maximum. WRITE depth requires at least a half-day gap (morning teaching → afternoon EOD is acceptable; same-afternoon is not). This directly addresses the 2025 same-day fragility (comprehensions D2, date parsing D4, seaborn D7).
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
| `for x in list` | taught in 2d, which is afternoon; half-day rule applies | ADAPT |
| dict literal + `d[key]`, as `rename` mapping | NOT methods, NOT iteration, NOT nesting | WRITE |
| `.rename(columns=dict)` | columns direction only | WRITE |

WRITE constructs: 8. At the vocabulary budget cap, not over it.

Note (2026-08-10): `for x in list` was previously bundled into the list row at WRITE. That
conflicted with the half-day rule, since loops are taught in the afternoon 2d session. Split
out and demoted to ADAPT. The Day 2 EOD supplies the complete loop in a Field Note and asks
students only to change the list.

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
| `.sort_values(col, ascending=False)` | single key | WRITE |
| top-N sentence | as a named pattern | WRITE |
| `.loc[row_label, col_label]` | scalar lookup only (Banana task 4 needs it) | ADAPT |
| `.filter(like=)` | 🧭 Field Note (cheese task); sets task cut per decision 5 | ADAPT |
| `.drop(list, axis='columns')` | 🧭 Field Note in EOD setup | ADAPT |

### Day 4: Clean + Transform

Sessions (sketch):
- 4a: missing-data sentence completed (diagnose Day 2 → treat today: `.dropna()`, `.fillna()`, the `~ .isnull()` mask re-using Day 3 grammar); `.astype()`; `.drop_duplicates()`.
- 4b: derived-column sentence (`df['new'] = expr`), column arithmetic, scalar broadcast; basic `.str` methods (`.strip/.lower/.replace`, scoped; chains deferred to Day 7 Field Note).
- 4c: functions, properly: `def`/`return`/default args, motivated by "you've now written the same filter-sort-head three times" (fixes the 2025 Day 5 gap where functions were effectively learned inside the EOD); `.apply(func)` on a column as the payoff.
- 4d (colab): clean a deliberately messy dataset in pairs.
- EOD: marine microplastics (relocated from 2025 Day 4; now everything it needs is taught: masks Day 3, `~` and `.copy()` Day 3, derived column and `np.log10` today). Its groupby tasks become ADAPT preview cells for Day 5, or get trimmed.

Scope table:
| Construct | Scope taught | EOD depth |
|---|---|---|
| `.dropna()/.fillna(value)` | whole-frame and single-column | WRITE |
| `.astype(str/int/float)` | single cast, no chains | WRITE |
| derived-column sentence | arithmetic of columns and scalars; one numpy function (`np.log10`) as "vectorized math comes from numpy", total intended numpy exposure for the course | WRITE |
| `.str.strip/.lower/.replace` | single method, no chaining | WRITE |
| `def f(x): return ...`; default args | 1–2 param functions returning a value | WRITE |
| `.apply(func)` | named function only, NO lambda | WRITE |
| `read_csv(parse_dates=['col'])` | 🧭 Field Note (full datetime treatment Day 6) | ADAPT |

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
| `pd.to_datetime` + `.dt.` accessors | `%Y/%m/%d` formats; year/month accessors | WRITE |
| `value_counts().reset_index()` + rename | as the "Series to table" move (fixes 2025 D6 gap) | WRITE |
| MultiIndex `.idxmax()` on groups | 🧭 Field Note or redesigned away | ADAPT |

### Day 7: Visualize

Sessions (sketch):
- 7a: matplotlib anatomy (figure/axes, `plt.figure(figsize=)`, labels, titles, `xticks(rotation=)`, `tight_layout`). 2025's 7a largely survives, now with the D6-2025 sequencing bug fixed because no earlier EOD demands styled matplotlib anymore (D4 EOD keeps only bare `.hist()`, taught as part of Explore's toolkit).
- 7b: seaborn: `sns.scatterplot/barplot/histplot` with `data=/x=/y=/hue=`; the Series `.values/.index` barplot idiom taught explicitly (2025 flag).
- 7c (colab): Palmer penguins exploration (2025's 7c survives).
- 7d (**decided**): project kickoff. Form teams, browse dataset sources (final_project.qmd list), draft the analysis question. Decompresses Day 8; students start the project with the full 10-step grammar fresh. Fallback if Day 7 runs hot: convert to buffer/review and push kickoff to Day 8 morning.
- EOD: USDA hardiness zones (everything it needs is now taught: merge D6, pivot_table D6, concat D6; the `.str.split().str.get().astype()` chain in setup becomes a 🧭 Field Note; seaborn same-day, so per the half-day rule the EOD's seaborn tasks provide the call skeleton and students fill mappings: ADAPT-leaning WRITE).

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
   is the half-day rule working as designed, since loops are taught in the afternoon 2d session.

## Risks

- **Day 2 is the experiment's crux.** Students touch DataFrames on day 2 with one day of Python. If the "data biography" EOD works, the design works. Mitigation: keep 2d (pure-Python grammar session) robust, and hold 2025's 2a/2b sessions ready as fallback inserts.
- **Fundamentals debt surfacing late.** A student who never solidifies loops may not notice until Day 5. Mitigation: grammar minutes + the D2/D5 live-coding grammar sessions are the designated debt-collection points; colab pairing surfaces struggling students early.
- **Instructor context-switching in sessions** (the original worry): bounded by the vocabulary budget: each session teaches its scope-table rows and nothing else; anything a dataset tempts us toward that isn't in the table becomes a Field Note or a cheatsheet link.
- **Schedule check:** all of this assumes the 2025 4-sessions+EOD daily rhythm and a 7+2 day calendar. Verify against actual September 2026 dates before allocating sessions to clock times.
