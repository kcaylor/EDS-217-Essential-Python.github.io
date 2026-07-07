# EOD Concept Ledger — 2025 Baseline (Form-Level Audit)

**Created:** July 2026, for 2026 course redesign
**Method:** Every construct in each 2025 EOD activity (including hidden answer-key solutions) was inventoried at *form level* (the exact idiom used, not the topic), assigned a required depth, mapped to the 9-step workflow, and cross-referenced against where the 2025 schedule first taught it.

**Why this exists:** The 2025 audit (`tasks/course-audit/`) achieved 100% alignment at *topic* level, but student complaints persisted. This ledger shows why: several EODs used constructs in forms, combinations, or depths that differed from the form taught. A binary taught/not-taught matrix cannot catch these. This ledger is the design spec for 2026: every construct an EOD requires must appear below with a session assignment and an explicit scope.

## Depth legend

- **WRITE** — student must produce the construct to complete a task (verified against answer keys)
- **ADAPT** — scaffold or callout provides the idiom; student modifies or applies it
- **READ** — provided code the student only runs
- **KEY-ONLY** — appears in the answer key but is not required by any student-facing task (a scope bug, not a teaching requirement)

## Verdict legend

- ✅ aligned — taught earlier, in the same form
- ⚠️ form gap — topic taught, but the EOD form is materially harder (new combination, chaining, parameters, or context)
- ⏱️ same-day — taught only hours before the EOD (fresh, fragile)
- ❌ never taught — no session teaches it in any form
- 📖 in-EOD — the EOD itself teaches it via callout (this is the "backfill inside the EOD" pattern; make deliberate in 2026, not accidental)

---

## Day 1 — Toolik Lake climate workflow ("Coming Attractions" preview)

Entirely READ by design; students copy/paste/run a complete 9-step-ish workflow. No alignment risk. Constructs previewed: `pd.read_csv(url)`, `.head()`, `.isnull().sum()`, `.describe()`, `.info()`, two-step `groupby` → column select → `.mean()`, `plt.plot`, `plt.bar`, `.to_csv()`.

**2026 note:** This is the strongest existing asset for the "whole game first" approach. The preview framing (resolved in 2025) works. Candidate for becoming the template every day follows in miniature.

## Day 2 — Classmate data (lists & dictionaries)

| Construct (form) | Depth | Step | First taught | Verdict |
|---|---|---|---|---|
| List literal, `.append()`, `.pop(i)`, `.sort()`, `.index()` | WRITE | Transform/Sort | 2a | ✅ |
| Nested dict-of-dicts literal construction | WRITE | fundamentals | 2b (nested mentioned) | ⚠️ central structure; nesting depth beyond 2b examples |
| Loop over dict adding nested key | WRITE | Transform | 2b | ✅ |
| List comprehension over `.values()` | WRITE | Transform | 2d | ⏱️ same-day |
| Comprehension with `.items()` unpacking + `if` filter | WRITE | Filter | 2d (partially) | ⚠️⏱️ tuple unpacking in comprehension not taught |
| `sum(gen-expr)/len(...)` manual mean | KEY-ONLY | Aggregate | never | ❌ generator expressions |
| `max(d, key=lambda x: d[x].get(k, 0))` | KEY-ONLY | Aggregate | never | ❌ lambda; ❌ `.get()` default |
| `def` + list-destructuring `[a, b] = random.sample(...)` | ADAPT | other | 1d (functions, barely) | ⚠️ destructuring never taught |
| `random.choice/sample` | READ→ADAPT | other | 2d | ⏱️ |

**Bug found:** the analysis/filtering tasks requiring the lambda and comprehensions exist only in the answer key, not in the student-facing handout. Fix regardless of redesign.

## Day 3 — Test scores (Series + control flow)

Clean alignment (this was redesigned in 2025 and it shows). All WRITE. `pd.Series(data, index=months)` with custom string index, `.mean()/.max()/.min()/.median()`, `.idxmax()/.idxmin()`, 4-branch `if/elif/else`, f-strings.

Minor: f-string `:.2f` precision spec (⚠️ small form gap vs 1c); `numpy` imported but never used (vestigial; learning objectives mention numpy functions no task uses). **2026 note: the only numpy the EODs genuinely require anywhere is `np.log10` on Day 4.**

## Day 4 — NOAA marine microplastics

| Construct (form) | Depth | Step | First taught | Verdict |
|---|---|---|---|---|
| `pd.read_csv(url, parse_dates=['Date'], date_format='%m/%d/%Y %I:%M:%S %p')` | ADAPT (tip) | Import | 4d | ⏱️ same-day; 12-hour format string is a stretch |
| `.head()/.describe()/.info()/.isnull().sum()` | WRITE | Explore | 4a | ✅ |
| `df[~df['Oceans'].isnull()]` | ADAPT (callout) | Clean/Filter | — | 📖 `~` taught in the EOD callout itself |
| Two-step groupby → `['col'].count()/.mean()` | WRITE | Group/Agg | 4b | ✅ |
| One-line `df2.groupby(['Oceans'])['Measurement'].max()` chain | WRITE | Group/Agg | — | ⚠️ chained form never explicitly taught (4a/4b teach two-step) |
| `df[df['Unit'] == 'pieces/m3']` | WRITE | Filter | 4a | ✅ |
| `df3 = df2[df2['Measurement'] > 0].copy()` | ADAPT (callout) | Filter | — | 📖 `.copy()` taught in EOD callout |
| `df3['log10'] = np.log10(df3['Measurement'])` | WRITE | Transform | 3c (numpy fns) | ⚠️ numpy-into-new-column form is new |
| `.hist()` on a Series | WRITE | Visualize | 4c (plt import only) | ⚠️ `.hist()` itself not demonstrated |

## Day 5 — Banana Index

Step emphasis: Filter ~15%, Sort ~20%, Transform ~18%. No groupby, no plotting.

| Construct (form) | Depth | Step | First taught | Verdict |
|---|---|---|---|---|
| `pd.read_csv(url, index_col='entity')` | WRITE | Import/Clean | 4d | ✅ |
| `df.drop([...5 labels...], axis='columns')` | WRITE | Clean | 5b (partially) | ⚠️ multi-label list drop |
| `df['col'].sort_values(ascending=False).head(10)` top-N idiom | WRITE | Sort/Agg | 4a sort + 4a head | ⚠️ the combined idiom is the day's backbone but never taught as a pattern |
| `def return_top_10(df, column): return ...` | ADAPT (stub) | fundamentals | 1d ("basic function concepts") | ⚠️ **major**: writing functions with `return` effectively learned here |
| `def return_top_n(df, column, n=10)` default arg | WRITE | fundamentals | never | ❌ default parameters |
| `set(...).intersection(...)`, incl. `*`-unpacking variant in tip | WRITE | Aggregate | 2c (sets) | ⚠️ sets-from-`.index` + unpacking far beyond 2c |
| `df.loc['Bananas', 'col']` scalar label lookup | WRITE | Transform | 5a | ✅ |
| New column via scalar division | WRITE | Transform | 4c-ish | ✅ |
| `df.filter(like='heese', axis='rows')` | WRITE | Filter | 5a (`.filter()` columns) | ⚠️ row-axis on index labels is a form extension |
| Stub named `return_top_ten` vs key's `return_top_10` | — | — | — | bug: name mismatch |

**Note:** answer-key sections 6–8 (`.corr()`, `sns.heatmap`, `.style.highlight_between()`) are properly fenced off as advanced. Good pattern to keep.

## Day 6 — Eurovision

Step emphasis: Group ~20%, Aggregate ~13%, Join (not a named step) ~significant, Visualize ~15%.

| Construct (form) | Depth | Step | First taught | Verdict |
|---|---|---|---|---|
| `.isnull().sum()`, `fillna(0)` whole-frame | WRITE | Clean | 4a, 5b | ✅ |
| `pd.to_datetime(col, format='%Y')`, `.dt.year` | WRITE | Clean/Transform | 6c | ✅ (⏱️ same-day) |
| Mask with `.dt.year >= 1990` + `.copy()` | WRITE | Filter | 6c + D4 callout | ✅/⚠️ |
| Column-minus-column new column; `.hist()` | WRITE | Transform/Viz | D4 EOD | ⚠️ taught-by-prior-EOD, not by a session |
| `value_counts().head(10)` | WRITE | Group/Agg | "basic operation" per 2025 matrix | ⚠️ verify a session actually shows it |
| `groupby('to_country')['points_final'].mean()` + `.sort_values(ascending=False)` | WRITE | Group/Agg/Sort | 6a | ✅ |
| `(df['year'].dt.year // 10) * 10` decade bucket | WRITE | Transform | 6c patterns + 1d `//` | ✅ (clever but components taught) |
| `groupby(['decade','to_country'])[...].mean()` → MultiIndex → `.groupby('decade').idxmax()` | WRITE | Group/Agg | 6a (single-key + agg) | ⚠️ **major**: multi-key groupby, MultiIndex result, and idxmax-on-groups; the 2025 "break into steps" revision scaffolded but did not remove the construct |
| `pd.merge(a, b, left_on=, right_on=)`, incl. `how='left'` | WRITE | Join | 6a "various join types" | ⚠️ verify mismatched key names shown in 6a |
| `value_counts().reset_index()` + manual `.columns = [...]` | WRITE | Transform | — | ⚠️ reshaping idiom untaught |
| Per-capita derived column; `1_000_000` literal | WRITE | Transform | components taught | ✅ |
| `Series.plot(kind='line')`; full `plt.bar` block with `xticks(rotation=45, ha='right')`, `tight_layout()` | WRITE | Visualize | 4c import; D4 EOD `.hist()` | ⚠️ matplotlib formal instruction is Day 7, *after* this EOD needs it |

## Day 7 — USDA plant hardiness zones

Step emphasis: Clean ~18%, Visualize ~22%, reshape (not a named step) ~13%.

| Construct (form) | Depth | Step | First taught | Verdict |
|---|---|---|---|---|
| `.astype(str).str.zfill(5)` | ADAPT (setup) | Clean | 5b (`.str` basics) | ⚠️ zfill + cast chain |
| `pd.concat([df_2023, df_2012], axis=0)` | ADAPT (setup) | Clean | never in a session | ❌ (2025 matrix hand-waved as "advanced pandas operations") |
| `.str.split().str.get(0).astype(int)` chain | ADAPT (setup) | Transform | 5b partially | ⚠️ two chained `.str` accessors + cast |
| `pd.merge(left_on='zipcode', right_on='zip')` | WRITE | Join | 6a/6b + D6 EOD | ✅ |
| Boolean filters (`longitude < -60`, `year == 2023`) | WRITE | Filter | 4a/5a | ✅ |
| `groupby('state')['trange_min'].mean()` ×2 + index-aligned Series subtraction | WRITE | Group/Agg | 6a; subtraction ⚠️ (alignment semantics untaught) |
| `pivot_table(index=[3 cols], columns='year', values=...).reset_index()` then `df[2023] - df[2012]` | WRITE | Transform/reshape | **never** | ❌ **the largest never-taught construct in the course** (2025 matrix marked it "appropriate for Day 7" without a teaching session) |
| `sns.scatterplot(data=, x=, y=, hue=, palette=, s=)` ×3 | WRITE | Visualize | 7b/7c | ✅ (⏱️ same-day, intended) |
| `sns.barplot(x=top10.values, y=top10.index, palette=)` | WRITE | Visualize | 7b/7c | ⚠️ Series `.values`/`.index` feeding idiom is non-obvious |
| `plt.figure(figsize=)`, labels, `legend(title=)` | WRITE | Visualize | 7a | ✅ |

---

## Findings summary (likely sources of the residual 2025 complaints)

1. **Form gaps, not topic gaps.** Every day except 3 uses at least one construct in a form materially harder than taught: one-line groupby chains (D4), functions with return/defaults (D5), multi-key groupby → idxmax (D6), pivot_table (D7).
2. **Never-taught constructs that survived the 2025 audit:** lambda + generator expressions (D2 key), default function parameters (D5), `pd.concat` (D7), `pivot_table` (D7), possibly `value_counts` depending on session content.
3. **Same-day fragility.** Comprehensions (D2), date parsing (D4), datetime accessors (D6), and all of seaborn (D7) are taught hours before the EOD requires them at WRITE depth.
4. **Matplotlib sequencing error.** D6 EOD requires substantial matplotlib (line plots, styled bar charts) but formal matplotlib instruction is Session 7a, the next day. D4/D6 EODs carry plotting on an import statement and one `.hist()`.
5. **In-EOD callout teaching already exists** (`~`, `.copy()` on D4; set-intersection tip on D5) and works. In 2026 this becomes a deliberate, named mechanism rather than an ad-hoc patch.
6. **Handout/key drift:** D2 tasks only in key; D5 function-name mismatch. Add a mechanical check to the pre-course checklist.
7. **The 9-step framework has two unnamed steps.** Join/merge (D6, D7) and reshape/pivot (D7) are load-bearing in the EODs but absent from the Import→…→Visualize list. Either extend the framework or fold them explicitly into Transform.
8. **numpy is nearly absent from EOD requirements:** one `np.log10` call (D4) and a vestigial import (D3). Confirms the 2026 de-emphasis is structurally cheap.

## Recurring grammar patterns (candidate explicit "sentence patterns" for 2026)

These idioms recur across EODs and should each be taught *as a named pattern*, once, with spaced reuse:

1. `df[df['col'] <op> value]` (+ `.copy()`) — the filter sentence (D4, D6, D7)
2. `df.groupby(key)['col'].agg()` — the split-apply-combine sentence (D1, D4, D6, D7)
3. `.sort_values(ascending=False).head(n)` — the top-N sentence (D5, D6, D7)
4. `df['new'] = <vectorized expr of columns>` — the derived-column sentence (D4, D5, D6, D7)
5. `pd.merge(a, b, left_on=, right_on=)` — the join sentence (D6, D7)
6. `.isnull().sum()` → decide → `.dropna()/.fillna()` — the missing-data sentence (D1, D4, D6)
7. `.str.<method>` chains — the string-cleaning sentence (D7)
8. `def f(df, col, n=10): return ...` — the reusable-analysis sentence (D5)

## EOD step-distribution matrix (approximate % of activity)

| Step | D1* | D2 | D3 | D4 | D5 | D6 | D7 |
|---|---|---|---|---|---|---|---|
| Import | 10 | – | 5 | 10 | 3 | 5 | 5 |
| Explore | 35 | 5 | 10 | 20 | 7 | 8 | 7 |
| Clean | – | – | – | 10 | 12 | 12 | 18 |
| Filter | – | 10 | – | 15 | 15 | 8 | 12 |
| Sort | – | 5 | – | – | 20 | 7 | 5 |
| Transform | 30 | 30 | 20 | 10 | 18 | 12 | 13 |
| Group | 15 | – | – | 10 | – | 20 | 10 |
| Aggregate | 15 | 15 | 40 | 15 | 10 | 13 | 8 |
| Visualize | 20 | – | – | 10 | – | 15 | 22 |
| Join (unnamed) | – | – | – | – | – | ✓ | ✓ |
| Reshape (unnamed) | – | – | – | – | – | – | ✓ |

*D1 is READ-only preview. Columns are rough proportions of student effort, not equal-precision measurements.

Observations for the workflow-to-days design question: Sort never exceeds 20% of any single EOD and is usually an appendage of Aggregate (top-N). Explore is front-loaded and shrinks to boilerplate by D5. Group/Aggregate and Import/Explore behave as natural pairs. Visualize is absent from D2/D3/D5 entirely, then dominates D7. The EODs already spiral through the workflow with shifting emphasis rather than marching through it one step at a time.
