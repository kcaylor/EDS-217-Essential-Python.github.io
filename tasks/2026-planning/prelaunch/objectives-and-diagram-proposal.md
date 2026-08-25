# Two proposals for the front page and the workflow diagram

Written 2026-08-25, from the 2026 schedule rather than from the 2025 text.

## What the 2026 course actually covers

Counted across the live pages, excluding answer keys.

| Taught, and on the schedule | Where |
|---|---|
| Jupyter notebooks in Positron | Day 1, session 1a |
| Variables, strings, f-strings | Day 1, session 1b |
| The ten-step workflow, end to end | Day 1, "The Whole Game", then every day after |
| Reading data into pandas, exploring a DataFrame | Day 2, sessions 2a and 2b |
| Lists and dictionaries | Day 2, live coding 2d |
| Booleans and conditionals | Day 3, live coding 3a |
| Filtering, sorting, top-N | Day 3, sessions 3b and 3c |
| Cleaning, writing functions, derived columns | Day 4, sessions 4a, 4b, 4c |
| Grouping, aggregating, loops over groups | Day 5, sessions 5a, 5b, live coding 5d |
| Joining, reshaping, dates | Day 6, sessions 6a, 6b, 6c |
| matplotlib and seaborn | Day 7, sessions 7a and 7b |
| Writing a data biography, evidence under every claim | Day 2 end-of-day practice |
| Paired work | Nine coding colabs, then the Day 8 and 9 project |
| Presenting a result to the room | Day 9 afternoon |
| GitHub | Day 8, self-paced |

Not on the 2026 schedule, despite appearing in the objectives or in the repository:

- **Algorithms.** The word appears in no course-materials page.
- **Error and exception interpretation.** `2c_exceptions_and_errors.qmd` exists but
  `_quarto.yml` line 14 excludes it from the render and no day page links it.
- **Getting help with `help()`.** Same: excluded at `_quarto.yml` line 13.
- **NumPy as a topic.** Five files mention it against forty-eight for pandas. One
  cheatsheet, no session of its own.
- **Comprehensions as a session.** A cheatsheet and some live-coding notes, but no
  scheduled slot.
- **Scripts.** The course is notebooks throughout. No `.py` file is ever written.

## Proposal 1: the learning objectives

Current text on index.qmd, with what is wrong beside it.

| Current | Problem |
|---|---|
| Manipulate and analyze data using libraries like pandas and NumPy | NumPy is given equal billing with pandas and has no session |
| Visualize data using Matplotlib and Seaborn | Accurate |
| Write, interpret, and debug Python scripts | No script is written in the course, and error interpretation is not scheduled |
| Implement basic algorithms for data processing | Matches nothing on the site |
| Use logical operations, control flow, and functions in your own code | Accurate |
| Collaborate with peers to solve group programming tasks, and communicate the process and results to the rest of the class | Accurate, and long |

### Proposed replacement

By the end of the nine days you should be able to:

- Read environmental data into a pandas DataFrame and say what it contains before
  analysing it
- Filter, sort, clean and transform a table to answer a question you have chosen
- Group rows and aggregate them into the comparison a question needs
- Combine two tables, reshape between long and wide, and handle dates as dates
- Build a figure in matplotlib or seaborn that carries the finding on its own
- Write your own Python: variables, collections, conditionals, loops and functions
- Keep a Jupyter notebook in which every claim sits below the cell that produced it
- Work with a partner on an analysis, and present the result to the class

Eight bullets against six. The three that are new are the ones the course spends the
most time on and the old list never mentioned: the workflow itself, the shape of a
defensible notebook, and the figure as the deliverable.

**One thing to check before applying.** If these bullets are also in the official
course catalog entry, changing them here makes the two disagree. The site can lead
and the catalog follow, but that should be a decision rather than a side effect.

## Proposal 2: the mermaid diagram

The reported problem is that step 5 and step 10 share the same emoji:

```
E["5. Sort 📊"]  ...  J["10. Visualize 📊"]
```

A reader scanning the chain meets the same icon twice and reads it as ending
twice. Step 8's 📈 is a third chart icon in the same diagram, so three of the ten
steps carry a graph and none of the three is the one about graphs.

The fix worth making is larger than swapping one character. Every step maps to a
session that already has an emoji on its day page, so the diagram can use the icon
the student will meet again on the day the step is taught.

| # | Step | Now | Proposed | Why |
|---|---|---|---|---|
| 1 | Import | 📂 | 📂 | unchanged |
| 2 | Explore | 🔍 | 🔎 | matches Day 2's "🔎 Exploring a DataFrame" |
| 3 | Clean | 🧹 | 🧼 | matches Day 4's "🧼 Missing, Duplicated, Miscast" |
| 4 | Filter | 🎯 | 🎯 | unchanged, and deliberately not a magnifier, so it cannot be confused with step 2 |
| 5 | Sort | 📊 | 🥇 | **the reported collision**, and it matches Day 3's "🥇 The Top-N Sentence" |
| 6 | Transform | 🔧 | ➕ | matches Day 4's "➕ The Derived-Column Sentence" |
| 7 | Group | 👥 | 🗂️ | matches Day 5's "🗂️ The Split-Apply-Combine Sentence" |
| 8 | Aggregate | 📈 | 📊 | matches Day 5's "📊 Several Answers at Once" |
| 9 | Join / Reshape | 🔗 | 🔗 | unchanged, already matches Day 6 |
| 10 | Visualize | 📊 | 🖼️ | matches Day 7's "🖼️ The Anatomy of a Figure" |

All ten are then distinct, and the only two that look alike, 🔎 and 🔍, are no
longer both in the diagram.

Proposed block:

```
flowchart LR
    A["1. Import 📂"] --> B["2. Explore 🔎"] --> C["3. Clean 🧼"]
    C --> D["4. Filter 🎯"] --> E["5. Sort 🥇"] --> F["6. Transform ➕"]
    F --> G["7. Group 🗂️"] --> H["8. Aggregate 📊"] --> I["9. Join / Reshape 🔗"]
    I --> J["10. Visualize 🖼️"]
```

🗂️ and 🖼️ carry a variation selector. Both already appear on the day pages and
render, so the diagram is not taking on a new risk.

The minimal version, if the full remapping is more churn than it is worth, is to
change step 5 to 🥇 and leave the other nine alone. That fixes the collision the
cold read reported and nothing else.
