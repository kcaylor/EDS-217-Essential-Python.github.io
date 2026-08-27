# House style for EDS 217 course prose

Rules Kelly has stated directly, for the teaching register. This file exists
because the style corpus at `~/dev/kkc_corpus` has no teaching samples: its
folders are email, letters, reviews, grants, evaluative and longform, and none of
those is a person explaining pandas to somebody who learned it last Tuesday.

Everything here came from Kelly in conversation, not from extrapolation. Add to
it only when he says something, and record the date.

**Read `kelly-edits-2026-08-27.md` first.** It holds the teaching register in his
own hand, taken from three pages he re-edited after this pass had signed them
off. Rules are a summary of samples and these are the samples, so where the two
disagree the samples win. The largest pattern in them is not on any list below:
a prescription is "should", not "is", and his replacement sentences are longer
than the draft sentences, not shorter.

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

### Ground the reader in the course, not in the document

**Refined 2026-08-24.**

> I would still prefer a more direct adjective "Today's lesson", "This morning's
> lesson", etc... to ground the reader in the course experience. I realize this
> could break if we move things around... (Today is always Today, but This Morning
> could become This Afternoon). However, we can catch that as we go, and I think
> the payoff is worth the price.

A demonstrative pointing at the document the student is holding needs no
antecedent, so "This session teaches lists and dictionaries" is not wrong. It is
just ungrounded: it tells the reader where they are in a file rather than where
they are in the week.

| Instead of | Write |
|---|---|
| This session teaches lists and dictionaries. | Today's lesson is lists and dictionaries. |
| This exercise takes about 45 minutes. | Today's practice takes about 45 minutes. |
| In this session we cover grouping. | This morning we cover grouping. |

**"Tonight" is always wrong. Corrected 2026-08-27.**

> Stop using tonight for the EOD activity text and references to it. The course
> runs until 4:00-4:30 each day and there is no homework. So tonight has no
> meaning the context of this class or any of its activities.

An end-of-day practice is the last block of the class day, done in the room, with
Cella and Kelly present. It is not homework. Every "tonight", "this evening",
"at night" and "last night's" in the course prose came from an assumption that
was never checked, and it is worse than a style error: a page that says "there is
nobody to ask" tells a student to struggle alone while the instructor is standing
in the room. Use "the end-of-day practice", "this afternoon", "before you leave
today", or "yesterday's practice" for a backward reference.

Genuine night-time references in the data are untouched: an overnight ozone
decline, a reading taken at three in the morning.

**Durability, and the price Kelly has accepted.** "Today" is true whatever else
moves, because a day page is a day. "This morning" and "this
afternoon" are true only while the session stays in that half of the day. Prefer
the most durable phrasing that still grounds, and accept the rest.

The price is paid by a checker rather than by caution:

```
python tools/prose_guard.py deictics --all    bare deictics still to ground
python tools/prose_guard.py timeclaims        every grounded claim, and whether it moved
```

`timeclaims` records which half of which day each session is linked from, and
reports any page whose placement has changed since the last snapshot while still
making a temporal claim. It does not judge whether a claim is correct, because
that needs to know where the referenced content is taught. A first version tried
to, and reported twelve failures of which nearly all were correct backward
references from an afternoon colab to the morning.

Check with:

```
python tools/prose_guard.py referents --all
```

It separates the two cases and exits non-zero when any sentence-initial
demonstrative points back into the text.

---

## Teach in the first person plural

**Stated 2026-08-24.**

> It is generally better to write in the 1st person plural (We are skipping this
> today), so the student feels like they are part of a group of learners and that
> the authorial voice is participating equally with the learner. This puts the
> student in a more collaborative mood, versus "You" or what you did, which was
> to (bizarrely!) omit the subject entirely.

Counted on 2026-08-24 across the day pages and end-of-day activities: **11 uses of
we, our or us against 508 of you or your.** The site talks at students almost
exclusively.

The rule is not to replace every "you". Three cases, and they are different:

| Case | Person | Example |
|---|---|---|
| What happens in the room | **we** | We skip Clean today. We use pandas because it is what the field uses. |
| An instruction to carry out | **imperative, no subject** | Create a new notebook. Copy this cell and run it. |
| What the individual student produces or is responsible for | **you** | Your notebook should hold four things. Name the file after your team. |

Never omit the subject in a declarative sentence. "Skipped today, and here is why"
has no actor at all, which is worse than either person.

The boundary case is a shared experience described from outside, as in Day 7's
"You have not made a picture since Monday". By this rule it becomes "We have not
made a picture since Monday", and the sentence is better for it, because the
instructor made that choice and is standing behind it.

## No promise-instead-of-tell constructions

**Stated 2026-08-24.**

> Basically, all your "X is Y, and here's Z" crap has got to go.

A clause that announces an explanation instead of giving one. The reader stops,
expects the answer, and gets a signpost.

| Instead of | Write |
|---|---|
| Step 3: Clean (skipped today, and here is why) | Step 3: Clean, which we skip today |
| We skip Clean along the way, for a reason you will see. | We skip Clean, because this file has nothing wrong with it. |
| That is why the exercise asks for it. | The exercise asks for it because a third of the rows are affected. |

The same shape includes "as you will see", "more on this below", "we will come
back to this", and "for reasons that will become clear". If the explanation is
short, give it. If it is long, give the one-line version and link the long one.

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

**Stated 2026-08-23. Extended 2026-08-27.**

Never "land", never "hinge". Write "depend" or "rely". The noun forms are fine:
Day 3 is full of "land use" and "land-hungry" and always will be.

### "Carry" is the worst of them

> Carrying is a physical act and never really relevant to concepts or ideas.
> Ideas support, reveal, depend on, explain, justify, etc... They cannot carry
> anything.

A file does not carry columns. A label does not carry units. A sentence does not
carry a claim. In every case the writer already knew the real relation, which is
"has" or "shows" or "means" or "states", and reached for one soft verb that fits
all of them. Name the relation.

| Instead of | Write |
|---|---|
| The file carries five bookkeeping columns. | The file has five bookkeeping columns. |
| the rows that carry a `Measurement` | the rows with a `Measurement` |
| Axis labels should carry units. | Axis labels should give units. |
| a column that carries no information | a column that tells you nothing |
| a sentence that carries all four things | a sentence that states all four things |
| a lot of ink for the information it carries | a lot of ink for what it shows |
| the ranking carries no weight | the ranking means nothing |
| A Series carries its numbers in `.values`. | A Series holds its numbers in `.values`. |
| That imbalance is worth carrying into question 17. | Remember the imbalance in question 17. |
| Make yesterday's figure carry the claim. | Make yesterday's figure show the claim. |

Two survive. **"Carry out"** where it means perform, though "do" is usually
shorter. **"Last observation carried forward"** in `05_Drop_or_Impute.qmd`,
because it is the name of the method.

The same test applies to every other verb of physical transport standing in for
a relation between ideas: hold, bring, deliver, bear. Ask what the sentence
actually asserts, and assert it.

### "Own" as a verb, banned outright

**Stated 2026-08-27.**

> I think you can put a blanket prohibition on "owns" as a verb that you use in
> any teaching material. It's almost never the correct word (same problem as
> "carries") and it has baggage as a verb that I do not want to inject into my
> writing.

Same failure as "carry": one soft verb standing where a real relation was
available. A library does not own an attribute, it uses one. A day does not own a
pattern, it introduces one. A field does not own a word, it uses one.

| Instead of | Write |
|---|---|
| Day 3 owns two patterns. | Day 3 brings in two new patterns. |
| matplotlib owns the frame around them. | matplotlib provides the frame around them. |
| `voicepass.py` owns the ledger. | `voicepass.py` maintains the ledger. |
| what the student owns | what the student produces |
| a word this field already owns | a word this field already uses |

The possessive and the adjective are untouched and stay everywhere: "your own
notebook", "on your own", "our own eyes", "in your own words".

## A noun beats an idiom

**Stated 2026-08-27.**

> "Shape of the day" is so lame; an Agenda or Plan are what you are talking
> about. In general, if you are about to use an idiom when an actual noun would
> do... DON'T USE THE IDIOM.

Two costs, and the second is the larger one. An idiom is vaguer than the noun it
displaced, so the reader gets less. And many students in this room read English
as a second language, so an idiom is the sentence they stop on.

| Instead of | Write |
|---|---|
| ## The shape of the day | ## Today's agenda |
| You now know the shape of the whole course. | You now know the plan for the whole course. |
| so you can see the shape of the thing | so you can see the method on a real file |
| "does not come into it" | "does not matter" |

Literal geometry is not this rule. "The shape of the curve" on Day 5 and
"the size and shape of a figure" on Day 7 are about actual shapes and stay.

### Figures are wanted. The test is whether the figure maps onto anything

**Stated 2026-08-27, twice.**

> Idioms and puns in headings are a good time as long as they are tuned to the
> context of the material and not pablum idioms that are just repetitive turns of
> phrase that the genAI agent uses as a sort of "humanity crutch".

> I am figurative, but in a clever and highly-contextual way. "Exploring the
> TableLands" when talking about how to work with datatables is... just really
> clever. "The shape of tables" is... decidedly less clever (all tables are
> rectangles in data science!). Saying "Shape of the day" is just completely
> rotten. Days don't have a shape in any figurative sense. It's like saying the
> "Shape of water"!

Three grades, one diagnostic: **what is the source domain, and does mapping it
onto the subject tell the reader something?**

**Clever.** *"Exploring the TableLands."* A tableland is a real landform and a
word this field already uses, and it maps onto data tables as somewhere you can
go into and move around in. The pun is grounded twice, on the geography and on
the subject, and it earns the verb "exploring" that comes with it. Also his:
"big 'ol bag-o-data (tm)", "your new best frenemy: `datetime`", "the highs and
lows (pitches, natch)" of Eurovision.

**Weak.** *"The shape of tables."* There is a source domain, but the mapping
collides with a literal fact. Every data table is a rectangle, and pandas already
calls the attribute `.shape`. The figure has no room to mean anything the literal
reading has not already taken.

**Rotten.** *"The shape of the day."* There is no source domain at all. A day has
no shape literally or figuratively, so the phrase is an empty frame, in the
manner of "the shape of water". It sounds like it means something, which is
precisely the problem: it is the noise a generator makes when it wants a heading
to feel written.

So the question is never "is this an idiom". It is "what is the source, and does
it map". A figure that survives is wanted anywhere, heading or body. A figure
that does not is worse than the plain noun it displaced, because it costs the
reader a parse and gives nothing back.

**A heading is not exempt.** The phrase that prompted this rule was itself a
heading, `## The shape of the day`, on two separate day pages. The checker holds
a short list of figures with nothing to map from and fails on those wherever they
appear. Everything else it can only report, because no regex recognises a clever
one.

## Every sentence resolves forward

**Stated 2026-08-27.**

> If a reader has to read backwards from the end of a paragraph to even
> understand the basic subject matter that you are trying to communicate, then
> you have failed as a communication tool.

The sentence that prompted the rule, ending the opening paragraph of day8.qmd:

> What is new is that nobody is going to tell you which method to reach for.

Three failures in one sentence. It opens on "What is", which is a placeholder
rather than a subject, so the reader holds an empty slot until the verb has gone
by. It is built on a negation, so the reader has to work out what the positive
claim was. And "new" is a comparison whose other half sits three sentences
earlier, which is the backwards read: the student has to return to the top of
the paragraph to find out what today is being compared with.

Two rules, and they are about the reader's working memory rather than taste.

1. **Name the subject before the verb.** Cleft openers, "What is new is that",
   "What matters here is", "The thing about X is", always have a subject-first
   version, and it is always shorter.
2. **A paragraph's last sentence has to make sense read alone.** It is the one
   sentence a student is most likely to meet cold, because it is where they stop.
   If it only works with the paragraph above it, either move it up or end on
   something that stands.

| Instead of | Write |
|---|---|
| What is new is that nobody is going to tell you which method to reach for. | Until now we told you which method to use. Choosing it is your job from today. |
| What matters here is the number of rows you dropped. | The number of rows you dropped is what to report. |
| The thing about `.dropna()` is that it works on rows by default. | `.dropna()` works on rows by default. |

## Open on the subject, never on a tease

**Stated 2026-08-27**, about the opening of eod-day2:

> Yesterday you ran a complete data science workflow on `toolik_weather.csv`. You
> imported it, summarized it, plotted it, and exported a result. Nobody asked you
> what was actually in the file, and pandas was never going to volunteer it.
>
> Tonight you will find out.
>
> "This just fails in so many ways"

It is a film trailer in three beats: you did X, nobody told you Y, now you will
find out. It withholds the subject for suspense, and a student opening the page
wants to know what the practice is. "You will find out" names nothing. It is the
promise-instead-of-tell rule in a form the checker's regex does not reach.

The other four pages in the same series already do it right, and they all do the
same thing: **open on the dataset, concretely, with real numbers.** Day 4 opens
on 16,245 water samples from thirty-seven studies. Day 5 on three monitors within
fifteen kilometres and 4,942 hourly measurements. Day 6 on 1,603 rows of
Eurovision. Day 7 on the USDA hardiness map and the one number it is built from.
Day 2 was the only one that opened on a tease, and it now opens on 11,171 days of
Arctic weather in 21 columns.

## No portent

**Observed 2026-08-27**, across all five of the day pages Kelly re-edited in one
sitting. It is the largest single difference between the drafts and his hand.

The draft register builds suspense and promises revelation. His does not. It says
what the lesson covers, then makes a joke.

| Draft | Kelly |
|---|---|
| find the one pattern in them that no amount of filtering would have shown you | explore patterns across the dataset and reveal a new result that depends on the split-apply-combine workflow |
| find three separate reasons to distrust an answer you have just computed | find a number of reasons to be wary of easy answers |
| one argument, `hue=`, that will change how you look at data for the rest of your career | *(deleted)* |
| Six figures, and only one of them is the one the evening was about. | *(deleted)* |
| Today is the tenth step, and it is the one all the others were for. | Today we take our last step, and it is the one all the others have been prepping us for. |

The tells travel together: **"honestly"**, **"no amount of"**, **"for the rest of
your career"**, and a suspiciously exact count used for drama. He replaced "three
separate reasons" with "a number of reasons", which reverses the usual advice
about specifics and is right here, because the draft's precision was invented.

His jokes are the alternative, and they are always self-deprecating or about the
course, never about the significance of the material: "which is a bad look for a
data science class!", "somebody (your kind and generous instructional team)",
"your new best frenemy: `datetime`", "explore (without maps!)".

## Tools are not people

**Same passage, 2026-08-27.** "pandas was never going to volunteer it" was added
by the editor stage, not by the draft. A library does not volunteer, refuse,
decide, want, know or try to help. The joke is the "humanity crutch": a
personification that reads as warmth and delivers nothing. Say what is true:
pandas shows you what you ask it for.

Kelly's own warmth is in the aside and the exclamation mark, "(which is fine, and
expected!)", not in pretending the software has a personality.

## "Shape" is a filler noun

**Observed 2026-08-27.** Kelly, after the fourth use in one conversation: "You
have a serious shape fetish."

Three legitimate uses, and they are all literal:

- `df.shape`, and prose about it: "check its shape", "compare the shapes".
- **Long and wide.** Day 6 and `6b_reshaping_data` teach reshaping, where the
  shape of a table is the actual subject and the correct word.
- Real geometry and distributions: the shape of a curve, of a histogram, of a
  marker, of the country in a scatter of zip codes.

Everything else is the tic, standing in for form, pattern, structure or order
because the writer did not stop to name which one was meant. "A good project
question has a shape" means it follows a pattern. "The two-step shape" is a
two-step pattern. Name it.

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

`c10_house_style` masks code cells, YAML headers and shortcodes before scanning,
so a rule can name a common English word without firing on every code comment.

None of these makes prose good. They keep an editing pass off the parts of a file
that are not prose, and they find the shapes Kelly has said he does not want. The
rest is reading, and the reading is done by a second agent that did not write the
draft. See `editor-pass-prompt.md`.
