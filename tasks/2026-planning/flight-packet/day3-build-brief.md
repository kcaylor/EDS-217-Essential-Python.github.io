# Day 3 Build Brief: Filter + Sort

**Wed Sep 2, 2026.** Self-contained: everything needed to draft Day 3 without a network
connection and without reading back through a prior session.

## Read first

1. `tasks/2026-planning/2026-day-skeleton.md`, the Day 3 section and its scope table
2. `course-materials/interactive-sessions/2a_reading_data.qmd` and `2b_exploring_data.qmd`,
   for voice, structure, and callout conventions
3. This file

## What Day 3 owns

Two named sentence patterns, which is the whole point of the day:

- **the filter sentence**: `df[df['col'] > value]`
- **the top-N sentence**: `df.sort_values('col', ascending=False).head(n)`

Fundamentals woven in: booleans, comparison operators, `if/elif/else`. They arrive because a
filter needs them, not as a separate grammar lesson.

## Scope table (from the skeleton; do not exceed it)

| Construct | Scope taught | EOD depth |
|---|---|---|
| comparison + boolean ops | in mask context; bare `if/elif/else` for categorization | WRITE |
| filter sentence + `.copy()` | single and two-condition masks | WRITE |
| `.isin(list)` | list literal arg | WRITE |
| `.sort_values(col, ascending=False)` | single key | WRITE |
| top-N sentence | as a named pattern | WRITE |
| `.loc[row_label, col_label]` | scalar lookup only | ADAPT |
| `.filter(like=)` | Field Note (cheese task) | ADAPT |
| `.drop(list, axis='columns')` | Field Note in EOD setup | ADAPT |

Five WRITE constructs, so there is headroom under the budget of eight. Spend it only if a
session genuinely needs it, and add a row to the skeleton table if you do.

## Files to produce

| New file | Adapt from | Notes |
|---|---|---|
| `live-coding/3a_booleans_and_conditionals.qmd` | `live-coding/3a_control_flows.qmd` (141 ln) | Student-facing. Rebuild, don't edit: 2025 taught control flow abstractly. Teach through data questions. |
| `live-coding/3a_booleans_and_conditionals_notes.qmd` | `3a_control_flows_notes.qmd` (129 ln) | Instructor notes with timing checkpoints, matching the 2d notes format. |
| `interactive-sessions/3b_filtering_data.qmd` | `live-coding/5a_selecting_and_filtering_notes.qmd` (284 ln) | The filter sentence. Promote `.copy()` here from its 2025 Day 4 callout. |
| `interactive-sessions/3c_sorting_and_ranking.qmd` | `5a_selecting_and_filtering_notes.qmd` | The top-N sentence, plus `.idxmax()`/`.idxmin()` as label lookups. |
| `coding-colabs/3d_ranking_questions.qmd` | `coding-colabs/3b_control_flows.qmd` (295 ln) | Pairs, answers hidden via `execute: echo/include: false`. |
| `eod-practice/eod-day3-2026.qmd` | `eod-practice/eod-day5.qmd` (257 ln) + `answer-keys/eod-day5-key.qmd` (349 ln) | Banana Index, relocated. See trims below. |

Then wire `course-materials/day3.qmd` and the `_quarto.yml` navbar, exactly as Day 2 was.

## Banana Index EOD: required trims

The 2025 file is `eod-practice/eod-day5.qmd`. Its five task sections are Data Preparation,
Exploring Banana Scores, Common High-Scoring Foods, Land Use Analysis, and Cheese Analysis.

- **Cut the function-writing tasks.** Lines ~115 and ~128 define `return_top_ten` and
  `return_top_10`. Functions move to Day 4, so these cannot stand at WRITE depth. Replace with
  the top-N sentence written out each time. Repetition is the motivation for Day 4's functions
  session, so leave it visible rather than hiding it.
- **Cut the set-intersection task** (decision 5). Section 3 currently builds three sets and
  calls `set.intersection`. Sets are a cheatsheet gloss only in 2026. Rewrite "which foods
  appear in all three top-10s?" as a visual comparison of three printed lists.
- **`df.filter(like='Bana')`** appears at line ~107 and in the cheese task. Keep it, as a
  Field Note at ADAPT depth.
- **`.drop(list, axis='columns')`** in setup: Field Note.
- **Field Note budget is 2.** `.filter(like=)` and `.drop()` are exactly two. Anything else
  that needs backfilling means the day is misdesigned; change the day, not the cap.
- Confirm no `lambda` survives from the 2025 key.

## Data

`https://eds-217-essential-python.github.io/data/banana_index.csv` (24 KB). Already in
`data/`, resolves offline through the shim. Verify its columns before writing tasks; the 2025
key refers to `Bananas index (kg)`, `Bananas index (1000 kcalories)`, and
`Bananas index (100g protein)`.

## Rules that apply

- **Half-day rule.** 3d is the last afternoon session, so anything it introduces can be ADAPT
  at most in the same evening's EOD. 3a is morning, so booleans and conditionals are fair game
  at WRITE depth.
- **No `lambda`, anywhere, including answer keys.**
- **Comprehensions are not taught.** They appear on Day 5 at reading level only.
- **No h1 headers.** Largest heading is `##`. Notebook title cells inside fenced blocks are
  exempt, since they are not rendered as headings.
- Every session opens with the Getting Started notebook ritual and closes with Key points and
  Resources. Copy the shape from `2a_reading_data.qmd`.

## Verify before committing

```bash
python tools/run_cells.py course-materials/interactive-sessions/3*.qmd \
                         course-materials/coding-colabs/3d_*.qmd \
                         course-materials/live-coding/3a_*.qmd \
                         course-materials/eod-practice/eod-day3-2026.qmd
grep -rn "lambda" course-materials/*/3*.qmd course-materials/eod-practice/eod-day3-2026.qmd
grep -c "🧭 Field Note" course-materials/eod-practice/eod-day3-2026.qmd   # must be <= 2
```

Then check that every construct in the EOD traces to a row in the scope table above. That is
quality gate 1, and it is the one that catches real problems.

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
