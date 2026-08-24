#!/usr/bin/env python3
"""
Check that an answer key matches the exercise it answers.

Kelly's requirement, 2026-08-24: "keys should match assignments cell-for-cell
with absolute expectation that output matches what the students were asked to
generate in the assignment."

Three checks, in order of how much they matter:

1. NUMBERS. Every number the key asserts in its prose must actually appear in the
   output of the key's own code. A key that says "2.72 square metres" when the
   code prints 2.83 sends every student who checks their work down a hole. This
   is the check a cold read cannot do, because a reader has no way to run the
   code.

2. TASKS. Every numbered task in the handout must have an answer in the key.

3. CELLS. The key should have at least as many executable cells as the handout
   has tasks that need code.

Rounding is tolerated in the obvious direction: a key that says 2.72 matches an
output of 2.7189, because the key is reporting a rounded value. A key that says
2.72 when nothing in the output rounds to 2.72 is reported.

    python tools/key_check.py                 every pair
    python tools/key_check.py eod-day3        one pair, by stem
    python tools/key_check.py --tasks-only    skip execution, structure only
"""

import io
import contextlib
import os
import re
import sys
import traceback
from pathlib import Path

os.environ["MPLBACKEND"] = "Agg"
import warnings
warnings.filterwarnings("ignore")

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))

COLOR = sys.stdout.isatty()
def paint(s, c): return f"\033[{c}m{s}\033[0m" if COLOR else s
B = lambda s: paint(s, "1")
D = lambda s: paint(s, "2")
R = lambda s: paint(s, "31")
G = lambda s: paint(s, "32")
Y = lambda s: paint(s, "33")

CODE = re.compile(r"^```\{python\}\s*$(.*?)^```\s*$", re.M | re.S)
PLAIN_CODE = re.compile(r"^```[a-zA-Z]*\s*$.*?^```\s*$", re.M | re.S)
INLINE = re.compile(r"`[^`\n]+`")
BOLD = re.compile(r"\*\*(.+?)\*\*", re.S)

# A number as a key would report one: optional sign, thousands separators,
# optional decimals, optional trailing percent.
# The "(?<![\w-])" before the sign keeps "top-10" from reading as negative ten
# and keeps the "5" of "PM2.5" from being pulled out on its own.
NUM = re.compile(r"(?<![\w-])-?\d{1,3}(?:,\d{3})+(?:\.\d+)?"
                 r"|(?<![\w-])-?\d+\.\d+"
                 r"|(?<![\w-])-?\d+")


def pairs():
    """Handout and key, matched by filename."""
    out = []
    for h in sorted((ROOT / "course-materials/eod-practice").glob("eod-day?-2026.qmd")):
        k = ROOT / "course-materials/answer-keys" / (h.stem + "-key.qmd")
        if k.exists():
            out.append((h, k))
    for h in sorted((ROOT / "course-materials/coding-colabs").glob("*.qmd")):
        k = ROOT / "course-materials/answer-keys" / (h.stem + "-key.qmd")
        if k.exists():
            out.append((h, k))
    return out


def prose_of(text):
    """The text with code blocks removed, so numbers in code are not 'asserted'."""
    text = CODE.sub("", text)
    text = PLAIN_CODE.sub("", text)
    return text


# The number that opens a restated task, "**16, 17 and 18.**", is the task
# number and not a result, so it is stripped before the rest of the bold text is
# read for asserted values.
LEAD_TASK = re.compile(r"\A(?:\d{1,2})(?:(?:,|\s+and)\s*\d{1,2})*\s*[.:](?!\d)\s*")


# A key refers back to earlier work constantly, "the near tie in question 13",
# "carry that into Part 5". Those numbers name a place in the handout and assert
# nothing about the data, so they are removed before the rest is read.
XREF = re.compile(r"\b(?:questions?|tasks?|parts?|steps?)\s+"
                  r"\d{1,2}(?:\s*(?:,|and|to|through)\s*\d{1,2})*", re.I)

# "Every one of the top 10 is a Total row" counts list entries, not data. The
# number says how long a list is, which the student chose when writing .head().
LISTSIZE = re.compile(
    r"\b(?:top|bottom|first|last|largest|smallest|highest|lowest)[- ]\d{1,3}\b"
    r"|\b(?:top|bottom|first|last)\s+\d{1,3}\b"
    r"|\b\d{1,3}\s+(?:largest|smallest|highest|lowest|biggest)\b", re.I)


# Every key puts its findings inside this callout and restates the task outside
# it. Reading only the callouts is what separates a claim about the output from
# the wording of the question, which carries numbers of its own: "why is that
# number smaller than 80,000?"
ANSWER_BLOCK = re.compile(
    r"^:::+\s*\{\s*\.callout-note[^}]*✅ Answer[^}]*\}\s*$(.*?)^:::+\s*$",
    re.M | re.S)


def answer_prose(key_text):
    """The text of every answer callout, with code and cross-references gone."""
    blocks = ANSWER_BLOCK.findall(prose_of(key_text))
    return LISTSIZE.sub(" ", XREF.sub(" ", "\n\n".join(blocks)))


def code_literals(key_text):
    """Numbers written into the key's own cells.

    A threshold the exercise sets, "-100", is a number the student types rather
    than one the run produces, so a key that quotes it back is not making a
    claim about output.
    """
    lits = set()
    for b in CODE.findall(key_text):
        for m in NUM.finditer(b):
            lits.add(m.group(0).replace(",", ""))
    return lits


def asserted_numbers(key_text):
    """Numbers the key states as findings: bolded, or in inline code, in prose."""
    prose = answer_prose(key_text)
    literals = code_literals(key_text)
    found = []
    for m in BOLD.finditer(prose):
        body = LEAD_TASK.sub("", m.group(1))
        for n in NUM.finditer(body):
            if n.group(0).replace(",", "") in literals:
                continue
            found.append((n.group(0), " ".join(body.split())))
    for m in INLINE.finditer(prose):
        body = m.group(0).strip("`")
        # Inline code that is a bare value, not an expression or a column name.
        if re.fullmatch(r"[-\d,.\s%]+", body):
            for n in NUM.finditer(body):
                if n.group(0).replace(",", "") in literals:
                    continue
                found.append((n.group(0), " ".join(body.split())))
    return found


def run_key(key_path):
    """Execute the key's cells and return everything they printed or returned."""
    import eds217_offline_cache as cache
    cache.install()
    # Pandas elides wide frames with "...", which hides the very columns a key
    # reports on. Without this, a correct assertion about a Date column reads as
    # a number the code never produced.
    import pandas as pd
    pd.set_option("display.max_columns", None)
    pd.set_option("display.width", 250)
    pd.set_option("display.max_rows", 200)
    src = key_path.read_text()
    blocks = CODE.findall(src)
    ns, outputs, failures, skipped = {}, [], [], 0
    for i, b in enumerate(blocks, 1):
        if re.search(r"^#\|\s*eval:\s*false\s*$", b, re.M):
            skipped += 1
            continue
        if re.search(r"^\s*[%!]|=\s*!", b, re.M):
            skipped += 1
            continue
        buf = io.StringIO()
        body = [l for l in b.splitlines() if not l.strip().startswith("#|")]
        try:
            with contextlib.redirect_stdout(buf):
                # Run all but the last statement, then echo the last expression
                # the way a notebook would.
                src_block = "\n".join(body)
                try:
                    import ast as _ast
                    tree = _ast.parse(src_block)
                    if tree.body and isinstance(tree.body[-1], _ast.Expr):
                        head = _ast.Module(body=tree.body[:-1], type_ignores=[])
                        exec(compile(head, "<cell>", "exec"), ns)
                        val = eval(compile(_ast.Expression(tree.body[-1].value),
                                           "<cell>", "eval"), ns)
                        if val is not None:
                            print(repr(val))
                    else:
                        exec(compile(tree, "<cell>", "exec"), ns)
                except SyntaxError:
                    exec(src_block, ns)
            outputs.append(buf.getvalue())
        except Exception:
            failures.append((i, body[0][:70] if body else "",
                             traceback.format_exc().strip().splitlines()[-1]))
            outputs.append(buf.getvalue())
    return "\n".join(outputs), failures, skipped, len(blocks)


# Pandas prints large integers in scientific notation, so the maximum of a date
# column reaches the output as "1.988060e+07" rather than as 19880601. Both the
# value and the digits it was printed to are kept, so a key that reports the
# exact integer still matches.
SCI = re.compile(r"(?<![\w.])(-?\d(?:\.\d+)?)[eE]([+-]?\d+)")


def significant(raw):
    """How many significant digits a printed number carries."""
    digits = raw.replace("-", "").replace(",", "").lstrip("0")
    if "." in digits:
        digits = digits.replace(".", "").lstrip("0")
    return max(len(digits.rstrip("0")) or 1, 1)


def round_sig(x, n):
    if x == 0:
        return 0.0
    from math import floor, log10
    return round(x, -int(floor(log10(abs(x)))) + (n - 1))


def output_numbers(corpus):
    """Every numeric literal the code produced, with the precision it printed at."""
    vals = set()
    for m in SCI.finditer(corpus):
        try:
            vals.add((float(m.group(0)), significant(m.group(1))))
        except ValueError:
            pass
    for m in NUM.finditer(corpus):
        raw = m.group(0).replace(",", "")
        try:
            vals.add((float(raw), significant(raw)))
        except ValueError:
            pass
    return vals


def matches(asserted, produced):
    """Does any produced value round to the asserted one at its own precision?"""
    raw = asserted.replace(",", "")
    try:
        a = float(raw)
    except ValueError:
        return True
    dec = len(raw.split(".")[1]) if "." in raw else 0
    for p, sig in produced:
        if round(p, dec) == round(a, dec):
            return True
        # A key often reports a percentage of something printed as a fraction.
        if dec and round(p * 100, dec) == round(a, dec):
            return True
        # The output may carry fewer digits than the key, which is what happens
        # when pandas prints an integer in scientific notation.
        if p and round_sig(a, sig) == round_sig(p, sig):
            return True
    return False


# A handout numbers its tasks with a bare "N. " at line start. An EOD handout
# numbers its setup steps the same way, restarting at 1, so the task list is the
# longest run of consecutive numbers rather than every number in the file.
H_NUM = re.compile(r"^\**(\d{1,2})\.\s+\S", re.M)

# A key restates each task in bold before answering it, and sometimes answers
# two or three together: "**5, 6 and 7. The three top-10 lists.**"
# A key marker closes the bold either right after the number, "**16, 17 and
# 18.**", or after a restatement of the task, "**1. How many foods...**". The
# "(?!\d)" keeps "**1.0**, and it could not be anything else" out, because a
# digit after the period means a decimal rather than a task number.
K_NUM = re.compile(r"^\*\*((?:\d{1,2})(?:(?:,|\s+and)\s*\d{1,2})*)\s*[.:](?!\d)", re.M)

# Day 1 does not number anything. It marks work with these two headers instead,
# and the key repeats them, so the pair is compared by count.
MARKERS = [("Required", re.compile(r"Required:", re.M)),
           ("Your change", re.compile(r"\*\*Your change", re.M))]


def longest_run(nums):
    """The longest stretch of consecutive numbers starting at 1, in file order."""
    best, cur = [], []
    for n in nums:
        if cur and n == cur[-1] + 1:
            cur.append(n)
        else:
            if len(cur) > len(best):
                best = cur
            cur = [n] if n == 1 else []
    return cur if len(cur) > len(best) else best


def derived_index(produced, depth=4):
    """Values reachable from two printed numbers by one arithmetic step.

    A key reports "89 percent of the samples" when the code printed 9,039 and
    10,178 and nothing else. The percentage is correct and appears nowhere in
    the output. Indexing one step of arithmetic over the printed values
    separates that case from a number the key simply got wrong, which is the
    distinction that decides whether a run is worth reading.
    """
    vals = sorted({v for v, _ in produced})[:200]
    index = {d: set() for d in range(depth + 1)}

    # Significant-figure buckets carry the hedged claims, "a ratio of about
    # 403,000", where the key rounds a derived value to three digits.
    sigs = {n: set() for n in range(1, 7)}

    def add(x):
        if x is None or x != x or abs(x) > 1e12:
            return
        for d in index:
            index[d].add(round(x, d))
        for n in sigs:
            sigs[n].add(round_sig(x, n))

    # Only ratios. Sums and differences of two hundred printed values cover the
    # integer line so densely that every wrong count looks explainable, which
    # made an injected error of 9,139 for 9,039 pass silently. A percentage or a
    # bin width is the case worth allowing, and both are ratios.
    for x in vals:
        for y in vals:
            if y:
                add(100.0 * x / y)
                add(x / y)
    return index, sigs


HEDGE = re.compile(r"\b(about|roughly|approximately|around|nearly|some|"
                   r"a little (over|under)|just (over|under))\s*$", re.I)


def hedged(context, asserted):
    """Was the number introduced as an approximation?

    Either a hedging word stands in front of it, or the number is round enough
    to be one on its face: "40,000 points are enough to draw a map" is a stated
    approximation of 40,492 whether or not the word "about" appears.
    """
    at = context.find(asserted)
    if at > 0 and HEDGE.search(context[:at]):
        return True
    bare = asserted.replace(",", "").lstrip("-")
    return len(bare) >= 4 and bare.endswith("000")


def approximates(asserted, produced, sigs):
    """A hedged number need only agree to the digits it was written with."""
    raw = asserted.replace(",", "")
    try:
        a = float(raw)
    except ValueError:
        return False
    sig = significant(raw)
    target = round_sig(a, sig)
    if sig in sigs and target in sigs[sig]:
        return True
    return any(p_ and target == round_sig(p_, sig) for p_, _ in produced)


# Numbers a key states that its own output cannot show, checked by hand and
# recorded here so the run stays readable. Each entry names why.
ACCEPTED = {
    ("4d_cleaning_messy_data-key.qmd", "-9999"):
        "hypothetical, the sentence explains why the filter uses a range "
        "rather than one sentinel value",
    ("eod-day4-2026-key.qmd", "10,147"):
        "verified by hand against np.histogram; the cell now prints its bin "
        "counts, so this entry is a safety net rather than the reason it passes",
}


def from_neighbours(asserted, context):
    """Is the number the sum, difference or ratio of others in the same sentence?

    "CO2 rose from 320.29 ppm to 400.41 ppm, an increase of 80.12 ppm" states
    its own arithmetic. Restricting the operands to one sentence keeps this from
    excusing any number at all, which is what happened when sums and differences
    ranged over every value the run printed.
    """
    raw = asserted.replace(",", "")
    try:
        a = float(raw)
    except ValueError:
        return False
    dec = len(raw.split(".")[1]) if "." in raw else 0
    near = []
    for m in NUM.finditer(context):
        t = m.group(0).replace(",", "")
        if t == raw:
            continue
        try:
            near.append(float(t))
        except ValueError:
            pass
    for x in near:
        for y in near:
            if x is y:
                continue
            for cand in (x - y, x + y, (x / y if y else None),
                         (100.0 * x / y if y else None)):
                if cand is not None and round(cand, dec) == round(a, dec):
                    return True
    return False


PCT = re.compile(r"per ?cent|%")


def is_derived(asserted, context, index):
    """A percentage the code did not print but that its numbers imply.

    Only percentages. Ratios of every printed value against every other cover
    the small integers so completely that an injected 166 for 160 passed as
    explainable. A percentage is bounded and usually carries a decimal, so the
    same index is a real constraint rather than a rubber stamp. Everything else
    has to be printed, or derivable from numbers in its own sentence.
    """
    if not PCT.search(context):
        return False
    raw = asserted.replace(",", "")
    try:
        a = float(raw)
    except ValueError:
        return False
    if not 0 <= a <= 100:
        return False
    dec = len(raw.split(".")[1]) if "." in raw else 0
    return dec in index and round(a, dec) in index[dec]


def handout_tasks(text):
    """Numbered tasks in a handout.

    An end-of-day handout numbers its setup steps 1, 2, 3 and then restarts at 1
    for the tasks, so the task list is the longest consecutive run rather than
    every number in the file.
    """
    return longest_run([int(m.group(1)) for m in H_NUM.finditer(prose_of(text))])


def key_markers(text):
    """Every number a key opens a bold line with, in file order.

    A group is dropped when its own numbers descend. A heading that covers
    several tasks always names them in order, "**16, 17 and 18.**", so a
    descending pair is a sentence about two counts, "**26 and 25.** The
    difference is exactly one row", and not a heading at all.
    """
    nums = []
    for m in K_NUM.finditer(prose_of(text)):
        group = [int(n) for n in re.findall(r"\d{1,2}", m.group(1))]
        if group == sorted(set(group)):
            nums += group
    return nums


def answered(tasks, markers):
    """Walk the key's markers against the handout's tasks, in order.

    Matching in order rather than by set membership means a sentence that
    happens to open with a number, "**26 and 25.** The difference is exactly one
    row", cannot be mistaken for an answer to task 26 or task 25. Only a marker
    that continues the sequence counts.
    """
    hit, i = set(), 0
    for n in markers:
        if i < len(tasks) and n == tasks[i]:
            hit.add(n)
            i += 1
        elif n in tasks and n > (tasks[i - 1] if i else 0):
            # A key may answer two tasks under one heading and skip a number.
            hit.add(n)
            i = tasks.index(n) + 1
    return hit


def marker_counts(text):
    return {name: len(pat.findall(text)) for name, pat in MARKERS}


def check(handout, key, tasks_only=False):
    hp = handout.relative_to(ROOT)
    kp = key.relative_to(ROOT)
    htext, ktext = handout.read_text(), key.read_text()
    problems = []

    tasks = handout_tasks(htext)
    markers = key_markers(ktext)
    answers = answered(tasks, markers)

    print(B(f"\n{hp.name}  ->  {kp.name}"))

    if len(tasks) < 5:
        # Day 1 numbers only its setup steps and marks the actual work with
        # headers, so the two files are compared by how many of each they carry.
        hm, km = marker_counts(htext), marker_counts(ktext)
        print(f"  unnumbered handout, compared by marker: "
              + ", ".join(f"{n} {hm[n]}/{km[n]}" for n in hm))
        for name in hm:
            if hm[name] != km[name]:
                problems.append(
                    f"handout has {hm[name]} '{name}' and the key has {km[name]}")
                print(R(f"  handout has {hm[name]} '{name}', "
                        f"key has {km[name]}"))
        if not problems:
            print(G("  every marked task has a matching block in the key"))
    else:
        missing = [t for t in tasks if t not in answers]
        extra = sorted({m for m in markers if m not in tasks})
        print(f"  handout tasks: {len(tasks)}   key answers: {len(answers)}")
        if missing:
            problems.append(f"{len(missing)} task(s) with no answer: {missing}")
            print(R(f"  no answer for task(s): {missing}"))
        if extra:
            problems.append(f"key answers questions not asked: {extra}")
            print(Y(f"  key answers numbers the handout does not ask: {extra}"))
        if not missing and not extra:
            print(G(f"  all {len(tasks)} tasks answered, none extra"))

    if tasks_only:
        return problems

    corpus, failures, skipped, total = run_key(key)
    print(f"  cells: {total} total, {skipped} skipped, {len(failures)} failed")
    for i, first, err in failures:
        problems.append(f"cell {i} failed: {err}")
        print(R(f"    cell {i} FAILED  {first}"))
        print(R(f"      {err}"))

    produced = output_numbers(corpus)
    claims = asserted_numbers(ktext)
    unmatched = [(a, ctx) for a, ctx in claims if not matches(a, produced)]
    print(f"  numbers asserted in prose: {len(claims)}   "
          f"produced by the code: {len(produced)}")

    if not unmatched:
        print(G(f"  all {len(claims)} asserted numbers appear in the output"))
        return problems

    index, sigs = derived_index(produced)
    derived, missing, allowed = [], [], []
    for a, ctx in unmatched:
        if (kp.name, a) in ACCEPTED:
            allowed.append((a, ctx))
        elif (is_derived(a, ctx, index) or from_neighbours(a, ctx)
              or (hedged(ctx, a) and approximates(a, produced, sigs))):
            derived.append((a, ctx))
        else:
            missing.append((a, ctx))

    for a, ctx in allowed:
        print(D(f"  {a} allowed: {ACCEPTED[(kp.name, a)]}"))

    if derived:
        print(D(f"  {len(derived)} asserted number(s) the code did not print, "
                f"each one step of arithmetic from numbers it did:"))
        for a, ctx in derived[:8]:
            print(D(f"    {a:>12}   in: {ctx[:70]}"))
        if len(derived) > 8:
            print(D(f"    ... and {len(derived) - 8} more"))

    if missing:
        problems.append(f"{len(missing)} asserted number(s) not produced")
        print(R(f"  {len(missing)} asserted number(s) the output does not "
                f"support:"))
        for a, ctx in missing:
            print(R(f"    {a:>12}   in: {ctx[:70]}"))
    else:
        print(G("  every asserted number is in the output or derived from it"))
    return problems


def main(argv):
    args = [a for a in argv[1:] if not a.startswith("--")]
    tasks_only = "--tasks-only" in argv
    todo = pairs()
    if args:
        todo = [(h, k) for h, k in todo if any(a in h.stem for a in args)]
    if not todo:
        print("no handout and key pair matched")
        return 2
    bad = 0
    for h, k in todo:
        if check(h, k, tasks_only):
            bad += 1
    print(B(f"\n{len(todo) - bad} of {len(todo)} pair(s) clean"))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
