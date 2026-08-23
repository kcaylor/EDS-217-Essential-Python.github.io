# House style for EDS 217 course prose

Rules Kelly has stated directly, for the teaching register. This file exists
because the style corpus at `~/dev/kkc_corpus` has no teaching samples: its
folders are email, letters, reviews, grants, evaluative and longform, and none of
those is a person explaining pandas to somebody who learned it last Tuesday.

Everything here came from Kelly in conversation, not from extrapolation. Add to
it only when he says something, and record the date.

---

## The reader is not a conversational partner

**Stated 2026-08-23.**

> Do not use referent nouns (That) unless they are absolutely necessary, and
> NEVER to start a sentence. You aren't conversing with the student... They are
> reading for understanding and comprehension. There is a huge difference.

A demonstrative opening a sentence asks the reader to hold the previous sentence
in working memory while parsing the next one. In conversation that costs nothing,
because the listener heard it a second ago and is doing nothing else. A student
reading to understand is already spending that capacity on the material.

So: no sentence begins with **That**, **This**, **These** or **Those**, and
mid-sentence use needs a reason. Name the thing instead.

| Instead of | Write |
|---|---|
| That is the step done properly. | Saying so is the step done properly. |
| That single property matters more than anything else. | Self-containment matters more than anything else. |
| That sentence is the point of the whole exercise. | The one-sentence finding is the point of the whole exercise. |
| That is right for coursework and wrong here. | Stripping output is right for coursework and wrong here. |

The exception is deictic use, where the demonstrative points at the document the
student is holding rather than back into the text: "This session teaches lists
and dictionaries", "This morning you learned a sentence that answers most grouped
questions". Those need no antecedent and are fine.

Check with:

```
python tools/prose_guard.py referents --all
```

It separates the two cases and exits non-zero when any sentence-initial
demonstrative points back into the text.

---

## "because", not "since", for an explanatory clause

**Stated 2026-08-23.**

> I also really prefer to use "because" to join an explanatory clause and not
> "since". They mean different things. Kelly Clarkson's hit single "Since you've
> been gone" would be a very different song if the title had been "Because you've
> been gone". Words have meaning. Choose wisely.

"Since" is first a temporal word. A reader meets it and starts a clock, then has
to go back and restart when the clause turns out to be causal. In course prose
that costs a re-read on every occurrence.

Reserve "since" for time: *since Monday*, *since Day 2*, *since 2019*. Use
"because" for cause.

| Instead of | Write |
|---|---|
| There is no new Python, since every method is one you have written. | There is no new Python, because every method is one you have written. |
| Step 9 is short, since your project uses a single table. | Step 9 is short, because your project uses a single table. |

The count across the live pages stood at 31 causal uses on 2026-08-23.

---

## No em-dashes

Long-standing, and it now matches `~/dev/kkc_corpus/STYLE.md`, which records it
as overriding an older note that treated dashes as a fingerprint. Restructure
with commas, periods, parentheses or `...`.

`grep -c '—'` must return 0 on every file.

## No metaphorical verbs standing in for literal ones

Never "land", never "hinge". Write "depend" or "rely". The noun forms are fine:
Day 3 is full of "land use" and "land-hungry" and always will be.

## No juxtapositional flourishes

"That is not X, it is Y" and "X with a hint of Y" are cadence rather than
content. A load-bearing contrast, where the two poles genuinely differ and both
carry information, is fine. Reaching for the shape by default is not.

## Reduce idiomatic constructions

Many students in this room read English as a second language. "does not come
into it" becomes "does not matter". Prefer the literal verb.

---

## Checking

```
python tools/prelaunch_checks.py c10_house_style   the mechanical rules
python tools/prose_guard.py referents --all        sentence-initial demonstratives
python tools/prose_guard.py verify --all           nothing outside prose moved
```

None of these makes prose good. They keep an editing pass off the parts of a file
that are not prose, and they find the two or three shapes Kelly has said he does
not want. The rest is reading.
