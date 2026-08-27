# EDS 217, Python for Environmental Data Science

Course site for Summer 2026. First class day: **2026-08-31**. Rendered to
`docs/` by Quarto and served from GitHub Pages.

## Writing prose for this repo

Everything a student reads is Kelly's writing under his name. Kelly has spent
hours re-editing generated prose that ignored rules he had already stated, so
this section is the most load-bearing part of this file.

**Before writing or editing any prose that a student will read, read
`tasks/2026-planning/prelaunch/house-style.md`.** It records the rules Kelly has
stated, each dated, in his own words. Read it every time. Do not work from
memory of it, and do not add to it unless Kelly says something new, in which
case record the date and quote him.

`~/dev/kkc_corpus/` is the voice corpus: `STYLE.md` plus real pre-genAI samples
in `samples/`. It has no teaching samples, which is why `house-style.md` exists
separately.

For teaching prose the samples are
`tasks/2026-planning/prelaunch/kelly-edits-2026-08-27.md`: Kelly's own edits to
three pages this pipeline had already signed off. Imitate those, not the
summary. The pattern they show that no rule list had caught is that a
prescription is "should", not "is", and that his sentences are longer than the
draft's, not shorter. Terseness is its own tell.

### The three-stage pipeline, which is not optional

A draft that goes straight from writing to Kelly is the failure mode this repo
is organised around. Every page goes through all three:

1. **Draft or revise.** Stay inside the prose. `python3 tools/prose_guard.py
   regions <file>` shows what is protected.
2. **Edit, by a different agent.** Invoke the `kelly-editor` subagent, which has
   not seen the draft's reasoning and rewrites rather than reports. A writer
   re-reading their own edit supplies the meaning they intended and cannot see
   the sentence a student will meet.
3. **Cold read, by a third agent.** `tasks/2026-planning/prelaunch/cold-read-prompt.md`,
   used verbatim. It checks comprehension and arithmetic, not voice. On three
   pages already called finished it found eighteen problems.

Only then does the page go to Kelly. Show him prose you have already put through
2 and 3, and say which stages ran.

4. **When he edits a page by hand, harvest it.** `python3 tools/kelly_edits.py`
   prints the changed prose paragraphs paired, draft against his. Read for the
   pattern, name it, and write the named pattern into
   `tasks/2026-planning/prelaunch/kelly-edits-2026-08-27.md`. That file is the
   only teaching-register sample set that exists, and it is what the editor
   stage reads first. Every hand edit he makes is a sample the corpus lacks;
   a pair on its own is data, the named pattern is what the next pass can act on.

Run `python3 tools/prose_guard.py desync --all` after any pass over an
end-of-day practice. The exercise and its answer key repeat each other's question
text verbatim, and rewording one side leaves a student checking themselves
against a different question.

### Facts the pages keep getting wrong

The class runs to 4:00 or 4:30 and **there is no homework**. An end-of-day
practice is the last block of the class day, in the room, with Cella and Kelly
present. "Tonight", "this evening" and "nobody to ask" are all false about it.
The teaching staff are Cella and Kelly.

### The four tics that keep coming back

Full rules and replacement tables are in `house-style.md`. These four are here
because they recur:

- **No metaphorical "carry", and no "own" as a verb.** A file has columns, a
  label gives units, a library uses an attribute rather than owning one. Both are
  one soft verb standing where a real relation was available. "Carry out" and the
  LOCF method name survive; the possessive "your own notebook" is untouched.
- **A noun, not an idiom.** "Today's agenda", never "the shape of the day". Many
  students in this room read English as a second language.
- **Every sentence resolves forward.** Subject before verb, no cleft openers,
  and a paragraph's last sentence has to make sense read on its own.
- **No em-dashes.** `grep -c '—'` returns 0 on every file.

## Running the tools

The repo has its own environment. A bare `python tools/...` in base Python makes
real checks report false failures.

```
source tools/_env.sh                                the environment
python3 tools/prelaunch.py status                   the pre-launch punch list
python3 tools/prelaunch_checks.py c10_house_style   the mechanical style rules
python3 tools/prose_guard.py verify --all           nothing outside prose moved
python3 tools/voicepass.py resume                   the next page in the voice pass
python3 tools/prose_guard.py desync --all           an exercise reworded, its key not
python3 tools/kelly_edits.py                        harvest Kelly's own edits as samples
bash tools/gates.sh                                 the six quality gates
```

`tools/voicepass.py` maintains the ledger at
`tasks/2026-planning/prelaunch/voice-pass.json`. Never edit a page in the voice
pass outside the state machine, because the ledger is the only memory across
sessions. One page at a time, committed on its own.

## Where things live

- `course-materials/` — the pages students read. `day*.qmd`, `interactive-sessions/`,
  `coding-colabs/`, `eod-practice/`, `answer-keys/`, `cheatsheets/`, `lectures/`
- `docs/` — Quarto output. Never hand-edit. Rebuild with `tools/publish.sh`.
- `tasks/2026-planning/` — planning and the pre-launch punch list
- `tools/` — checks, the voice-pass state machine, cache warming
