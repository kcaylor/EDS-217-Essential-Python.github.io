#!/usr/bin/env python3
"""
Fence a voice pass to prose, and prove afterwards that nothing else moved.

A style pass over 89 pages of teaching material is a judgement task, and the
person doing it should be free to rewrite a paragraph. What they must not do is
touch a code cell, a YAML header, a link target or a shortcode, because those
carry behaviour rather than voice, and a single silent change there breaks a
page for a student.

Rules cannot make prose good. They can keep an editing pass off the parts of the
file that are not prose, which is what this does.

    python tools/prose_guard.py regions <file>        what is protected, and what is editable
    python tools/prose_guard.py verify <file> [...]   compare the working tree against HEAD
    python tools/prose_guard.py verify --all          every live page

Exit status is 0 when every protected region is byte-identical to its committed
version, and 1 when any of them changed.
"""

import hashlib
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Everything here carries behaviour, not voice. A voice pass must not alter it.
PROTECTED = [
    ("yaml front matter", re.compile(r"\A---\n.*?\n---\n", re.S)),
    ("fenced code block", re.compile(r"^```.*?^```", re.M | re.S)),
    ("inline code span", re.compile(r"`[^`\n]+`")),
    ("quarto shortcode", re.compile(r"\{\{<.*?>\}\}", re.S)),
    ("link or image target", re.compile(r"\]\(([^)]*)\)")),
    ("div or callout fence", re.compile(r"^:::+.*$", re.M)),
    ("attribute block", re.compile(r"^\s*:\s*\{[^}]*\}\s*$", re.M)),
]


def regions(text):
    """Return protected spans as (label, start, end, text), longest first."""
    found = []
    for label, rx in PROTECTED:
        for m in rx.finditer(text):
            found.append((label, m.start(), m.end(), m.group(0)))
    # Drop spans that sit inside a larger one, so a backtick inside a code
    # block is not counted twice.
    found.sort(key=lambda r: (r[1], -(r[2] - r[1])))
    kept, last_end = [], -1
    for r in found:
        if r[1] >= last_end:
            kept.append(r)
            last_end = r[2]
    return kept


def fingerprint(text):
    """A stable hash of every protected region, in order."""
    parts = [f"{label}:{body}" for label, _, _, body in regions(text)]
    joined = "\n\x00\n".join(parts)
    return hashlib.sha256(joined.encode()).hexdigest(), parts


def prose_only(text):
    """The text with every protected region blanked, which is what may change."""
    out, last = [], 0
    for _, start, end, _ in regions(text):
        out.append(text[last:start])
        last = end
    out.append(text[last:])
    return "".join(out)


# Kelly's rule for the teaching register, given 2026-08-23:
#
#   "Do not use referent nouns (That) unless they are absolutely necessary, and
#    NEVER to start a sentence. You aren't conversing with the student... They are
#    reading for understanding and comprehension. There is a huge difference."
#
# A demonstrative opening a sentence makes the reader hold the previous sentence
# in mind while parsing the next one. In conversation that is free, because the
# listener has just heard it. A student reading to understand is doing other work
# with that capacity. So: sentence-initial That, This, These and Those are wrong
# in course prose, whatever precedes them.
SENTENCE_START = re.compile(
    r"(?:^|(?<=[.!?]\s)|(?<=[.!?]\s\s))(That|This|These|Those)\b")

# Everything the demonstrative might be pointing at, if it is pointing at the
# document rather than back into the text. Reported separately because "This
# session teaches..." is a different act from "That sentence is the point...".
DEICTIC_NOUNS = {
    "session", "page", "morning", "afternoon", "evening", "week", "course",
    "exercise", "activity", "colab", "notebook", "chapter", "cheatsheet",
}


def sentence_initial_demonstratives(text):
    """Every sentence that opens with That, This, These or Those, outside code."""
    sys.path.insert(0, str(ROOT / "tools"))
    protected = regions(text)
    blocked = [(s_, e_) for _, s_, e_, _ in protected]

    def inside_protected(pos):
        return any(s_ <= pos < e_ for s_, e_ in blocked)

    out = []
    line_starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            line_starts.append(i + 1)

    def line_of(pos):
        lo, hi = 0, len(line_starts) - 1
        while lo < hi:
            mid = (lo + hi + 1) // 2
            if line_starts[mid] <= pos:
                lo = mid
            else:
                hi = mid - 1
        return lo + 1

    for m in SENTENCE_START.finditer(text):
        pos = m.start(1)
        if inside_protected(pos):
            continue
        line_no = line_of(pos)
        raw = text[line_starts[line_no - 1]:].split("\n", 1)[0]
        # Skip markdown structure: headings, table rows, list markers are not prose.
        stripped = raw.lstrip()
        if stripped.startswith(("#", "|", ">", ":::", "!", "-", "*", "+")):
            continue
        rest = text[m.end(1):m.end(1) + 40].strip().split()
        noun = rest[0].rstrip(".,;:").lower() if rest else ""
        deictic = m.group(1) in {"This", "These"} and noun in DEICTIC_NOUNS
        snippet = text[pos:pos + 90].split("\n")[0]
        out.append((line_no, m.group(1), noun, deictic, snippet))
    return out


# The same failure in a different costume. "any of the three", "all five", "the
# two you set aside" all ask the reader to supply a noun the writer left out.
# Flagged when the numeral is followed by punctuation or a function word, which
# means no noun follows it.
ELLIPTIC = re.compile(
    r"\b(?:the|all|any of the|one of the|both of the|first|last|other)\s+"
    r"(two|three|four|five|six|seven|eight|nine|ten)\b"
    r"(?=\s*[.,;:)]|\s+(?:you|they|we|i|it|and|or|but|that|which|who|whose|"
    r"is|are|was|were|will|would|can|properly|cleanly|already|here|there)\b)",
    re.I)


def elliptical_numerals(text):
    """Numerals used as nouns, with the noun left for the reader to supply."""
    protected = regions(text)
    blocked = [(a, b) for _, a, b, _ in protected]
    out = []
    line_no = 1
    for m in ELLIPTIC.finditer(text):
        if any(a <= m.start() < b for a, b in blocked):
            continue
        line_no = text.count("\n", 0, m.start()) + 1
        snippet = text[max(0, m.start() - 40):m.end() + 40].replace("\n", " ").strip()
        out.append((line_no, m.group(0), snippet))
    return out


# Kelly prefers a grounded temporal adjective to a bare deictic: "Today's lesson"
# rather than "This session". The price is that a temporal claim breaks if the
# thing it points at moves between halves of a day, and he has accepted that
# price. So the job here is not to judge whether a claim is right, which needs to
# know where the referenced *content* is taught, but to notice when the ground
# moves underneath one.
#
# A first version of this reported twelve mismatches, and nearly all were correct:
# an afternoon colab saying "this morning you learned X" is a backward reference.
# Asserting a verdict the data cannot support is how a checker stops being read.
TIME_PHRASE = re.compile(
    r"\b(this morning|this afternoon|this evening|yesterday morning|"
    r"yesterday afternoon|tomorrow morning|tomorrow afternoon|tonight)\b", re.I)

BARE_DEICTIC = re.compile(
    r"\bThis (session|page|exercise|colab|notebook|activity|practice|cheatsheet)\b")

PLACEMENTS = ROOT / "tasks/2026-planning/prelaunch/time-claims.json"


def day_placements():
    """Which half of which day each session is linked from."""
    out = {}
    for d in range(1, 10):
        page = ROOT / f"course-materials/day{d}.qmd"
        if not page.exists():
            continue
        for line in page.read_text().splitlines():
            m = re.match(r"\|\s*day \d+ / (morning|afternoon)\b(.*)", line)
            if not m:
                continue
            for link in re.findall(r"\]\(([^)]+\.qmd)\)", m.group(2)):
                target = (page.parent / link).resolve()
                try:
                    rel = str(target.relative_to(ROOT))
                except ValueError:
                    continue
                out.setdefault(rel, set()).add(f"day{d}/{m.group(1)}")
    return {k: sorted(v) for k, v in out.items()}


def cmd_timeclaims(paths):
    """List grounded temporal claims, and report where the ground has moved."""
    import json as _json
    place = day_placements()
    current = {}
    for rel, slots in sorted(place.items()):
        f = ROOT / rel
        if not f.exists():
            continue
        prose = prose_only(f.read_text(errors="replace"))
        phrases = sorted({m.group(0).lower() for m in TIME_PHRASE.finditer(prose)})
        if phrases:
            current[rel] = {"slots": slots, "phrases": phrases}

    old = {}
    if PLACEMENTS.exists():
        old = _json.loads(PLACEMENTS.read_text()).get("pages", {})

    moved = []
    for rel, info in current.items():
        was = old.get(rel, {}).get("slots")
        if was and was != info["slots"]:
            moved.append((rel, was, info["slots"], info["phrases"]))

    print(f"{len(current)} page(s) make a grounded temporal claim.")
    for rel, info in current.items():
        print(f"  {rel}")
        print(f"      placed {', '.join(info['slots'])}; says {', '.join(info['phrases'])}")

    if moved:
        print(f"\n{len(moved)} page(s) MOVED since the last snapshot, and their")
        print("temporal claims may now be wrong:")
        for rel, was, now, phrases in moved:
            print(f"  {rel}: {', '.join(was)} -> {', '.join(now)}")
            print(f"      check: {', '.join(phrases)}")
    elif old:
        print("\nNo page has moved since the last snapshot.")
    else:
        print("\nNo previous snapshot. Writing one now, so the next run can compare.")

    PLACEMENTS.parent.mkdir(parents=True, exist_ok=True)
    PLACEMENTS.write_text(_json.dumps({"pages": current}, indent=1, sort_keys=True) + "\n")
    return 1 if moved else 0


def cmd_deictics(paths):
    """Bare deictics that could be grounded in the course calendar instead."""
    total = 0
    for p in paths:
        text = Path(p).read_text(errors="replace")
        prose = prose_only(text)
        hits = []
        for m in BARE_DEICTIC.finditer(prose):
            ctx = prose[max(0, m.start() - 40):m.end() + 45].replace("\n", " ").strip()
            hits.append((m.group(0), ctx))
        if not hits:
            continue
        total += len(hits)
        rel = Path(p).resolve()
        try:
            rel = rel.relative_to(ROOT)
        except ValueError:
            pass
        print(f"\n{rel}  ({len(hits)})")
        for phrase, ctx in hits:
            print(f"  {phrase}: ...{ctx}...")
    print(f"\n{total} bare deictic(s). Prefer a grounded adjective: "
          f"\"Today's lesson\", \"This morning's session\".")
    print("\"Today\" is durable. \"This morning\" is not, and prose_guard.py timeclaims")
    print("watches for the day it stops being true.")
    return 1 if total else 0


def cmd_referents(paths):
    total = deictic_n = 0
    for p in paths:
        hits = sentence_initial_demonstratives(Path(p).read_text(errors="replace"))
        if not hits:
            continue
        total += len(hits)
        deictic_n += sum(1 for h in hits if h[3])
        real = [h for h in hits if not h[3]]
        if not real:
            continue
        rel = Path(p).resolve()
        try:
            rel = rel.relative_to(ROOT)
        except ValueError:
            pass
        print(f"\n{rel}  ({len(real)})")
        for line_no, word, noun, _, snippet in real:
            print(f"  line {line_no}: {snippet}")
    ell_total = 0
    for p in paths:
        hits = elliptical_numerals(Path(p).read_text(errors="replace"))
        if not hits:
            continue
        ell_total += len(hits)
        rel = Path(p).resolve()
        try:
            rel = rel.relative_to(ROOT)
        except ValueError:
            pass
        print(f"\n{rel}  ({len(hits)} elliptical numeral(s))")
        for line_no, phrase, snippet in hits:
            print(f"  line {line_no}: \"{phrase}\"  ...{snippet}...")

    print(f"\n{total} sentence(s) open with a demonstrative.")
    print(f"{deictic_n} of those point at the document itself (\"This session\", \"This")
    print(f"morning\"). The other {total - deictic_n} point back into the text and are the ones")
    print("Kelly's rule is about: a student reading for comprehension should not have to")
    print("hold the previous sentence in mind to parse the next one.")
    print(f"\n{ell_total} numeral(s) used as a noun with the noun left out.")
    return 1 if (total - deictic_n or ell_total) else 0


def head_version(path):
    rel = Path(path).resolve().relative_to(ROOT)
    r = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=str(ROOT),
                       capture_output=True, text=True)
    if r.returncode != 0:
        return None
    return r.stdout


def live_pages():
    sys.path.insert(0, str(ROOT / "tools"))
    import prelaunch_checks as pc
    return [ROOT / f for f in pc.correct_render_set() if f.endswith(".qmd")]


def cmd_regions(paths):
    for p in paths:
        text = Path(p).read_text()
        rs = regions(text)
        protected_chars = sum(e - s for _, s, e, _ in rs)
        prose = prose_only(text)
        prose_words = len(prose.split())
        print(f"\n{p}")
        print(f"  {len(rs)} protected region(s), {protected_chars:,} characters")
        counts = {}
        for label, _, _, _ in rs:
            counts[label] = counts.get(label, 0) + 1
        for label, n in sorted(counts.items(), key=lambda kv: -kv[1]):
            print(f"    {n:>4}  {label}")
        print(f"  editable prose: about {prose_words:,} words")
    return 0


def cmd_verify(paths):
    """Compare protected regions against HEAD as multisets, not by position.

    A positional comparison reports a cascade the moment a region is added, so
    inserting one legitimate link makes every later region look changed. What
    matters is which regions appeared, which disappeared, and which were altered.
    """
    from collections import Counter
    bad, checked, missing = [], 0, []
    for p in paths:
        after = Path(p).read_text()
        before = head_version(p)
        if before is None:
            missing.append(str(p))
            continue
        checked += 1
        b = Counter(f"{lab}\x00{body}" for lab, _, _, body in regions(before))
        a = Counter(f"{lab}\x00{body}" for lab, _, _, body in regions(after))
        removed = sorted((b - a).elements())
        added = sorted((a - b).elements())
        if not removed and not added:
            continue
        rel = Path(p).resolve()
        try:
            rel = rel.relative_to(ROOT)
        except ValueError:
            pass
        bad.append((str(rel), removed, added))

    for rel, removed, added in bad:
        print(f"\n{rel}")
        for r in removed:
            lab, body = r.split("\x00", 1)
            print(f"  GONE     [{lab}] {body.strip()[:88]}")
        for a_ in added:
            lab, body = a_.split("\x00", 1)
            print(f"  NEW      [{lab}] {body.strip()[:88]}")
    for m in missing:
        print(f"SKIPPED  {m}  (not in HEAD)")

    if bad:
        print(f"\n{len(bad)} file(s) changed something outside prose.")
        print("A NEW link or code span is usually a deliberate content edit and is fine.")
        print("A GONE region, or a pair that reads as one thing rewritten, needs a reason.")
        return 1
    print(f"{checked} file(s) checked. Every code block, header, link target and "
          f"shortcode is unchanged from HEAD.")
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__)
        return 0
    cmd = argv[1]
    args = argv[2:]
    if cmd in ("verify", "referents", "deictics") and args[:1] == ["--all"]:
        paths = live_pages()
    else:
        paths = [Path(a) for a in args]
    if cmd == "timeclaims":
        return cmd_timeclaims(paths)
    if not paths:
        print("no files given")
        return 2
    if cmd == "regions":
        return cmd_regions(paths)
    if cmd == "verify":
        return cmd_verify(paths)
    if cmd == "referents":
        return cmd_referents(paths)
    if cmd == "timeclaims":
        return cmd_timeclaims(paths)
    if cmd == "deictics":
        return cmd_deictics(paths)
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
