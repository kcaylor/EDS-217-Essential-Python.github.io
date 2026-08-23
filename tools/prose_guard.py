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
    bad, checked, missing = [], 0, []
    for p in paths:
        after = Path(p).read_text()
        before = head_version(p)
        if before is None:
            missing.append(str(p))
            continue
        checked += 1
        h_before, parts_before = fingerprint(before)
        h_after, parts_after = fingerprint(after)
        if h_before == h_after:
            continue
        rel = Path(p).resolve().relative_to(ROOT)
        diffs = []
        for i, (b, a) in enumerate(zip(parts_before, parts_after)):
            if b != a:
                diffs.append((b, a))
        if len(parts_before) != len(parts_after):
            diffs.append((f"({len(parts_before)} protected regions)",
                          f"({len(parts_after)} protected regions)"))
        bad.append((str(rel), diffs))

    for rel, diffs in bad:
        print(f"CHANGED  {rel}")
        for b, a in diffs[:5]:
            print(f"    was: {b.strip()[:100]}")
            print(f"    now: {a.strip()[:100]}")
        if len(diffs) > 5:
            print(f"    ... and {len(diffs) - 5} more")
    for m in missing:
        print(f"SKIPPED  {m}  (not in HEAD)")

    if bad:
        print(f"\n{len(bad)} file(s) changed something a voice pass must not touch.")
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
    if cmd == "verify" and args[:1] == ["--all"]:
        paths = live_pages()
    else:
        paths = [Path(a) for a in args]
    if not paths:
        print("no files given")
        return 2
    if cmd == "regions":
        return cmd_regions(paths)
    if cmd == "verify":
        return cmd_verify(paths)
    print(f"unknown command: {cmd}")
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
