#!/usr/bin/env python3
"""
Harvest Kelly's own edits into before/after pairs, so the editor stage learns
from samples rather than from rules.

The style corpus at ~/dev/kkc_corpus has no teaching samples: its folders are
email, letters, reviews, grants, evaluative and longform, and none of those is a
person explaining pandas to somebody who learned it last Tuesday. Every time
Kelly re-edits a page by hand he produces exactly the sample that is missing, and
those samples are worth more than any rule written about them.

This reads a git range, or the working tree, and prints the paragraphs of prose
that changed, paired. Code cells, YAML headers, link targets and shortcodes are
excluded, because a voice pass never touches them.

    python3 tools/kelly_edits.py                       working tree vs HEAD
    python3 tools/kelly_edits.py --since HEAD~5        a range
    python3 tools/kelly_edits.py --paths course-materials/day7.qmd
    python3 tools/kelly_edits.py --out samples.md      append to a samples file

Read the result, find the pattern, and write it into
tasks/2026-planning/prelaunch/kelly-edits-2026-08-27.md with a name. A pair on
its own is data; the named pattern is what the next editor pass can act on.
"""

import argparse
import difflib
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
import prose_guard  # noqa: E402


def paragraphs(text):
    """Prose paragraphs only, whitespace-normalised, code and headers removed."""
    out = []
    for block in prose_guard.prose_only(text).split("\n\n"):
        s = " ".join(block.split())
        # Skip headings, list scaffolding and table rows: they change for
        # reasons that are not voice, and they drown the interesting pairs.
        if len(s) < 40 or s.startswith("#") or s.startswith("|"):
            continue
        out.append(s)
    return out


def at_rev(path, rev):
    rel = Path(path).resolve().relative_to(ROOT)
    r = subprocess.run(["git", "show", f"{rev}:{rel}"], cwd=str(ROOT),
                       capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def changed_files(since):
    r = subprocess.run(["git", "diff", "--name-only", since, "--", "*.qmd"],
                       cwd=str(ROOT), capture_output=True, text=True)
    return [ROOT / f for f in r.stdout.split() if f.endswith(".qmd")]


def pairs_for(path, since):
    before = at_rev(path, since)
    if before is None:
        return []
    after = Path(path).read_text(errors="replace")
    a, b = paragraphs(before), paragraphs(after)
    found = []
    for tag, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b).get_opcodes():
        if tag == "equal":
            continue
        old = a[i1:i2]
        new = b[j1:j2]
        # Pair them up positionally. An unmatched old paragraph was deleted,
        # which is itself a strong signal: Kelly cuts epigrams.
        for k in range(max(len(old), len(new))):
            found.append((old[k] if k < len(old) else None,
                          new[k] if k < len(new) else None))
    return found


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--since", default="HEAD", help="git ref to compare against")
    ap.add_argument("--paths", nargs="*", help="limit to these .qmd files")
    ap.add_argument("--out", help="append the report to this file")
    a = ap.parse_args(argv)

    files = [Path(p) for p in a.paths] if a.paths else changed_files(a.since)
    lines, n = [], 0
    for f in sorted(files):
        got = pairs_for(f, a.since)
        if not got:
            continue
        rel = Path(f).resolve()
        try:
            rel = rel.relative_to(ROOT)
        except ValueError:
            pass
        lines.append(f"\n## {rel}\n")
        for old, new in got:
            n += 1
            if old and new:
                lines.append(f"**Draft:** {old}\n")
                lines.append(f"**Kelly:** {new}\n")
            elif old:
                lines.append(f"**Draft:** {old}\n")
                lines.append("**Kelly:** *(deleted)*\n")
            else:
                lines.append(f"**Kelly added:** {new}\n")
    if not n:
        print(f"No prose paragraphs changed since {a.since}.")
        return 0
    body = "\n".join(lines)
    header = (f"# Kelly's edits since {a.since}\n\n"
              f"{n} changed prose paragraph(s) across {len([l for l in lines if l.startswith(chr(10)+'## ')])} file(s).\n"
              "Read for the pattern, name it, and add the named pattern to\n"
              "tasks/2026-planning/prelaunch/kelly-edits-2026-08-27.md.\n")
    if a.out:
        with open(a.out, "a") as fh:
            fh.write(header + body + "\n")
        print(f"{n} pair(s) appended to {a.out}")
    else:
        print(header + body)
    return 0


if __name__ == "__main__":
    sys.exit(main())
