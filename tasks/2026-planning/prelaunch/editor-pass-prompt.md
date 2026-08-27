# The editor pass

The second of three stages. It sits between drafting and the cold read, and
before 2026-08-27 it did not exist.

## Why it was added

Kelly, 2026-08-27, after reading pages the pipeline had already signed off:

> I am staring down 10-15 hours of hand editing EVERY page you've touched
> because you've done such a bad job of matching either my style or my
> expectations.

The pipeline at that point was draft, then cold read, then Kelly. Nothing in it
edited prose. The cold-read prompt is explicit about this:

> DO NOT report: tone, word choice you merely dislike

which is correct for a comprehension reader and meant that no stage ever caught
"carries", "the shape of the day", or a paragraph ending on a cleft. day8.qmd
was signed off on 2026-08-23 carrying all three. Kelly found them by hand four
days later.

He also named the fix:

> My guess is you need to write everything once, then completely hand it off to
> a new agent who only edits in my voice and with my perspective and THEN show
> it to me.

## The stage

`.claude/agents/kelly-editor.md`. Invoke it on every page after drafting and
before the cold read.

Two properties matter and both are easy to lose:

**It has not seen the draft's reasoning.** Give it the file and nothing else. A
writer re-reading their own edit supplies the meaning they intended, so they
read past the sentence a student will stop on. Explaining the draft to the
editor recreates that problem inside the stage built to solve it.

**It edits rather than reports.** A finding it describes instead of fixing is a
finding that reaches Kelly, which is the cost this stage exists to remove. Its
report is for facts only Kelly knows and for things that are wrong rather than
badly written.

## How the three stages divide the work

| Stage | Catches | Cannot catch |
|---|---|---|
| `c10_house_style` and `prose_guard` | The named shapes: em-dash, carry, cleft, "shape of the day", sentence-initial demonstratives | Anything that needs a reader |
| `kelly-editor` | Voice, rhythm, sentences that read backwards, flourishes | Whether a claim is true |
| `cold-read-prompt.md` | Comprehension failures, arithmetic, contradictions, cross-references | Voice, by design |

Skipping the middle stage is what produced the 10 to 15 hours.
