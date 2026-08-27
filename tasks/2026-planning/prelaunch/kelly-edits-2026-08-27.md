# Kelly's own edits, 2026-08-27

The teaching register, in his hand, taken from the working tree while he was
editing `day8.qmd`, `day9.qmd` and `final_project.qmd`. Three pages the voice
pass had already signed off.

`house-style.md` opens by noting that `~/dev/kkc_corpus` holds no teaching
samples: its folders are email, letters, reviews, grants, evaluative and
longform, and none of those is a person explaining pandas to somebody who
learned it last Tuesday. These pairs are the first teaching samples there are.
Read them before drafting course prose. Imitate them, not the summary below.

Typos in the "Kelly" column are his, typed at speed, and are not style: *ened*,
*progess*, *expectedt*, *bes*, *notenook*, *excercise*, *asychronously*, `!.`
They should be fixed, and they are not the point.

---

## 1. A prescription is "should", not "is"

The single most common change, present on every page. Draft prose asserts as
fact what is really an instruction or a goal, which leaves a student who has not
done it yet reading a description of a world they are not in.

| Draft | Kelly |
|---|---|
| It is **self-contained**: somebody who has your notebook and nothing else can restart the kernel, run every cell, and get your figures back. | Your notebook should be **self-contained**: somebody who has your notebook and nothing else should be able to restart the kernel, run every cell, and get your figures back. |
| It is **documented**: markdown cells explain what each step was for. | Your code should be **documented**: markdown cells should explain what each step was for. |
| Every one of the ten steps appears in the notebook under its own markdown heading, even where the honest content of a step is one sentence. | Every one of the ten steps should appear in your notebook under its own markdown heading, even if the content of a step is one sentence. |
| The dataset is the problem. Change it. | The dataset may be the problem. Change it! |
| The question is too big. | Your question is probably too big. |

The related move: **"the" becomes "your"** wherever the thing is the student's.
"Which rows the question is about" became "Which rows your question is about".

## 2. Cut the aphorism, give the mechanism

Draft prose closes sections on epigrams. Kelly deletes them, and where the
epigram was doing real work he replaces it with the reason.

| Draft | Kelly |
|---|---|
| Self-containment matters more than anything else on this page. | *(deleted)* |
| It is also the property most often lost, and it is lost in one particular way. You define a variable in a cell, you run the cell, and later you delete it. | Repeatable, shareable, and consistent code is sometimes difficult in notebooks because they can be run asychronously. You can define a variable in one cell, run the cell, and then later delete it. |
| If you have twenty minutes tonight, read your own notebook from the top as though somebody else wrote it... You will find more than you expect. I always do. | *(deleted)* |
| There is no end-of-day activity today. The project is the work. | There is no end-of-day activity today. The project is the only thing we are working on. |
| The whole morning is yours to finish in. | *(deleted)* |
| You will lose an hour and save a day. | You lose an hour, but you might save the day! |

An epigram is the shape a draft reaches for when it wants a section to feel
finished. It reads as a lecture rather than as help.

## 3. Hedge, and leave the student an out

The draft register is certain and slightly stern. His is warm and gives students
room to be behind, confused, or wrong.

| Draft | Kelly |
|---|---|
| Yesterday afternoon you left with a team, a dataset, three questions and one rough figure. | Yesterday afternoon you (hopefully!) ened up with a team, a dataset, three questions you're interested in asking, and one rough figure. |
| Being behind at a checkpoint is normal on a two-day project. | Being behind at a checkpoint is normal and expectedt. |
| Usually the data cannot answer them, and writing down why is worth the minute it takes. | Usually this is some combination of data or coding knowledge limitations. You don't need to use this project to teach yourself an entire new python course, so "we didn't know how to do that" is a legitimate answer. |
| By mid afternoon, steps 3 to 6 should be done and written up. | By mid afternoon, steps 3 to 6 should be done(ish) and written up. |
| ### Checkpoint 3, 4:30. The analysis is finished | ### Checkpoint 3, 4:30. The analysis is finished(ish) |
| ## Today's agenda | ## Today's agenda (Note: your actual progess will go however it goes!) |

`(ish)`, `(hopefully!)`, `probably`, `may be`, `or a new contender!` are his, and
they are doing pedagogical work rather than softening for its own sake. A
checkpoint labelled "finished" tells a student who is not finished that they have
failed. `finished(ish)` does not.

## 4. Punctuation he puts back

`STYLE.md` records these as fingerprints, and draft prose strips every one of
them out. He puts them back by hand.

- **Exclamation marks.** "Change it!", "you might save the day!", "until you have
  written it down!", "Choose you question!"
- **Trailing `etc...`** "why the other two (or three, etc...) questions were set
  aside"
- **Parenthetical asides** that qualify in real time: "(or a new contender!)",
  "(Remember: Absence of evidence is not evidence of absence!)"

## 5. Name the actual people

| Draft | Kelly |
|---|---|
| Come and find me at any of the three checkpoints. | Come and find Cella or Kelly at any time, but especially if you are nearing a checkpoint and find yourself behind. |
| You can also track down Cella or Kelly to get some help. | *(his addition)* |

The teaching staff are Cella and Kelly. Draft prose writes "me", "the
instructor", or nothing.

## 6. First person plural, and the present progressive

Already the rule in `house-style.md`, and his edits go further than the rule did.

| Draft | Kelly |
|---|---|
| Yesterday you finished the analysis. Today you finish the notebook, and then you tell eleven other teams what you found. | Today we are finishing our notebooks and sharing our final results. |
| Today you find out which of your three questions the data can actually answer. There is no new Python in the next two days... | Today you will keep working to determine which of your three questions the data can actually answer. We will cover no new python in the next two days... |
| Presentations are in the afternoon for that reason. | We will have presentations in the afternoon. |

Note also the tense: "we are finishing", "you will keep working". Draft prose
uses a clipped present ("Today you finish the notebook") that reads as a command
disguised as a description.

## 7. Sentences get longer, not shorter

The correction to genAI prose is not terseness. Kelly's replacements are
routinely two or three times the length of the draft sentence, because they
carry the qualification, the reason and the way out that the short version left
implicit. A page of short declaratives is its own tell.

> the answer is almost always to stop.

became

> you probably want to put a pause on that and go back to finishing up the stuff
> you have already started.

"the stuff" is his. Reaching for a more precise noun there would be a mistake.

## 8. Two he fixed that the rules already covered

- "[Day 8](day8.qmd) and [Day 9](day9.qmd) **carry** the hour-by-hour plan" became
  "**contain** the hour-by-hour plan". He caught the metaphorical carry by hand
  before the check existed.
- "## The shape of the day" became "## Today's agenda" on both day8 and day9.

Both are now HARD rules in `tools/prelaunch_checks.py`. He should not have had
to find either one.


---

# Second batch: day3 through day7, same day

Five more day pages, edited by hand a few hours after the first three. They
repeat every pattern above and add one that is larger than all of them.

## 9. The drafts are portentous. His prose is not.

This is the biggest single difference, and it appears on every one of the five
pages. The draft builds suspense, promises revelation, and makes grand claims
about what a lesson will do to you. He deletes all of it.

| Draft | Kelly |
|---|---|
| find the one pattern in them that no amount of filtering would have shown you | explore patterns across the dataset and reveal a new result that depends on the split-apply-combine workflow we have learned today |
| find three separate reasons to distrust an answer you have just computed | find a number of reasons to be wary of easy answers |
| Six figures, and only one of them is the one the evening was about. | *(deleted)* |
| one argument in it, `hue=`, that will change how you look at data for the rest of your career | *(deleted)* |
| taking my word for it that the ordering meant something | *(deleted)* |
| Today is the tenth step, and it is the one all the others were for. | Today we take our last step, and it is the one all the others have been prepping us for. |
| Tonight you take two versions of the USDA map... and find out what you can honestly say about the difference. | Today you take two versions of the USDA plant hardiness map, eleven years apart, and explore (without maps!) what you can say about the differences between them. |

Note what goes with the portent: "honestly", "no amount of", "three separate",
"for the rest of your career". Precision used for drama rather than for fact. He
replaces a suspiciously exact "three separate reasons" with "a number of
reasons", which is the opposite of the usual advice, and correct here because the
draft's precision was invented.

## 10. Announce the lesson plainly

Where the draft withholds, he states the plan and says who is doing what.

| Draft | Kelly |
|---|---|
| Today you learn the three sentences that do it. | Today we will learn the three steps that take a **big 'ol bag-o-data (tm)** and turn it into a **dataframe you can actually use**. |
| Day 3 owns two sentences, and between them they answer most of the questions | Day 3 brings in two new patterns that address most of the questions |
| Booleans... arrive this morning because a filter needs them. | In addition, booleans... arrive this morning because they are the underlying grammar that a filter depends on. |
| This afternoon you pick your project. | Finally, this afternoon, you will pick your project. |

"Day 3 **owns** two sentences" also personifies the day, which is the same crutch
as "pandas was never going to volunteer it". A day does not own anything.

## 11. His jokes are self-deprecating or about the course. Never portentous.

Collected from these five pages, all his:

- "somebody (your kind and generous instructional team) had already put everything you needed in one place"
- "We've not made a figure since Monday, which is a bad look for a data science class!"
- "a **big 'ol bag-o-data (tm)**"
- "your new best frenemy: `datetime`"
- "we've been exploring the TableLands"
- "the highs and lows (pitches, natch) of sixty-four years of the Eurovision Song Contest"
- "explore (without maps!) what you can say"
- "Suffice to say, that is not how data usually arrives. Instead it shows up on your doorstep as a grab bag of files"

He also made two headings **more** figurative, not less:

| Draft | Kelly |
|---|---|
| One Cloud of Points, Three Species | A Cloud of Points, Three flocks of 🐧 |
| Three Stations, One Air Shed | Three Stations, One Atmosphere |

The second is the pair worth studying: he kept the figure and dropped the jargon.
"Air shed" is a technical term; "atmosphere" is the plainer word and the better
one, and the heading is no less clever for it.

## 12. He adds content, not just voice

Editing is not only subtraction. On day5 he added a whole paragraph mapping
split-apply-combine onto `map-reduce`, added the Wickham plyr paper as a
resource, and on day6 added the "everything-is-an-object paradigm". The draft had
been keeping the course narrow. He widened it where a student might be curious.

## 13. Confirmations of rules already written

- **First person plural**, everywhere: "Yesterday **we** interrogated a table",
  "The past four days **we** have been asking", "For five days every question
  **we've** asked".
- **Day 7's boundary case**, which `house-style.md` predicted: "You have not made
  a picture since Monday" became "**We've** not made a figure since Monday". The
  rule said the sentence would be better for it, and he agreed, then added the
  joke.
- **`sentence` was never the right word.** "Day 3 owns two **sentences**",
  "Day 4 owns three **sentences**", "the three **sentences** that do it" all
  became **patterns** in his hand, which is the word the course already used for
  "the filter pattern" and "the top-N pattern".

---

## Boundaries, found by over-applying these rules

First run of the `kelly-editor` stage, on `eod-day3-2026.qmd`, 2026-08-27. It
got 30 of 34 sentences right and overshot on three of the patterns above. The
overshoots are recorded here because a rule without a boundary produces a new
defect rather than fixing the old one.

| Rule | Overshoot | The boundary |
|---|---|---|
| "should", not "is" | "Your answer **must** cite at least three numbers" became "should cite" | A description of something not yet built becomes "should". A stated requirement of an assignment stays "must". Demoting a requirement tells the student it is optional. |
| Cut the epigram | "exactly the itch that **functions** exist to scratch... worth having felt the itch before you get the cure" became "exactly the problem that functions solve... it helps to have felt the problem before you meet the solution" | The target is a closing maxim that adds no information. Figurative language is not the target. Kelly writes "big 'ol bag-o-data (tm)", "your new best frenemy: `datetime`", "the TableLands" in a single week. He is more figurative than the drafts, not less. |
| Sentences get longer | "answer this:" became "answer the following question:" | Length has to buy something: a qualification, a reason, a way out. Never filler. |
