#!/usr/bin/env python3
"""
Pre-flight check on every data URL the course materials use.

Course-site URLs (https://eds-217-essential-python.github.io/data/...) are
served from the repo's data/ directory by the offline shim, so they are
*verified*, not downloaded. Anything pointing somewhere else is downloaded
into the fallback cache so it still works offline.

    python tools/warm_cache.py           # verify + cache anything external
    python tools/warm_cache.py --list    # show what was found, touch nothing
    python tools/warm_cache.py --refresh # re-download the external ones

A non-zero exit means a URL in the materials has no data behind it.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eds217_offline_cache as cache  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
# tools/ is skipped: fetch_data.py lists upstream sources on purpose, and they
# are already mirrored into data/. Scanning it would re-download ~28MB.
SKIP_DIRS = {"docs", "nbs", "extra_files", ".git", "tasks", "tools", "_to_delete"}

DIRECT = re.compile(r"""pd\.read_\w+\(\s*['"](https?://[^'"]+)['"]""")
ASSIGN = re.compile(r"""^\s*\w*url\w*\s*=\s*['"](https?://[^'"]+)['"]""",
                    re.IGNORECASE | re.MULTILINE)
BARE = re.compile(r"""['"](https?://[^'"]+\.(?:csv|tsv|txt|json|xlsx|xls))['"]""",
                  re.IGNORECASE)

# Seven datasets are loaded only as `base + 'name.csv'`, where `base` is assigned
# once at the top of the block. The three patterns above match literal strings and
# never see them, so the tool used to report "all data URLs resolve" while covering
# ten of the seventeen datasets the course loads. A checker that reports green on a
# set it cannot see is worse than no checker, so concatenation is resolved here.
BASEVAR = re.compile(r"""^\s*(\w+)\s*=\s*['"](https?://[^'"]+/)['"]""", re.MULTILINE)
CONCAT = re.compile(
    r"""(\w+)\s*\+\s*['"]([A-Za-z0-9_.\-]+\.(?:csv|tsv|txt|json|xlsx|xls))['"]""",
    re.IGNORECASE)

# Illustrative URLs, not course data. The final-project page shows students how
# to load their OWN Google Drive CSV; the link there is an example, and each
# student substitutes their own. Nothing to mirror.
# URLs that appear only as teaching placeholders and are never fetched. Google Drive
# and Docs links are student-supplied. example.org is the RFC 2606 reserved example
# domain, used in 2a_reading_data.qmd to contrast a web address with a local path.
# some_file.csv is the generic stand-in in the parse_dates example: it appears only
# on a commented-out line in timeseries.qmd and inside a plain ```python block (not
# ```{python}) in 2a_reading_data.qmd, so neither reference ever executes.
ILLUSTRATIVE = re.compile(
    r"drive\.google\.com|docs\.google\.com|example\.(org|com|net)|some_file\.csv",
    re.IGNORECASE)


def collect():
    found = {}
    files = [p for p in ROOT.rglob("*.qmd") if not any(s in p.parts for s in SKIP_DIRS)]
    files += [p for p in ROOT.rglob("*.py") if not any(s in p.parts for s in SKIP_DIRS)]
    for p in files:
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for rx in (DIRECT, ASSIGN, BARE):
            for m in rx.finditer(text):
                found.setdefault(m.group(1), set()).add(str(p.relative_to(ROOT)))
        bases = dict(BASEVAR.findall(text))
        for var, name in CONCAT.findall(text):
            if var in bases:
                found.setdefault(bases[var] + name, set()).add(str(p.relative_to(ROOT)))
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    found = collect()
    # Illustrative first: a placeholder wins regardless of which host it imitates,
    # otherwise a course-site-shaped placeholder is reported as missing data.
    example = {u: f for u, f in found.items() if ILLUSTRATIVE.search(u)}
    course = {u: f for u, f in found.items()
              if u not in example and u.startswith(cache.COURSE_DATA_BASE)}
    other = {u: f for u, f in found.items() if u not in course and u not in example}

    datasets = {u.rsplit("/", 1)[-1] for u in found if u not in example}
    print(f"{len(found)} data URLs in the course materials, "
          f"{len(datasets)} distinct datasets")
    print(f"  {len(course)} served from the repo's data/ directory")
    print(f"  {len(other)} external")
    print(f"  {len(example)} illustrative (student-supplied, nothing to mirror)\n")

    if args.list:
        for label, group in (("course site", course), ("external", other)):
            if group:
                print(f"-- {label} --")
                for u, f in sorted(group.items()):
                    print(f"  {u}\n      {', '.join(sorted(f))}")
        return 0

    problems = []

    print("-- course-site URLs (verified against data/, not downloaded) --")
    for url in sorted(course):
        name = url[len(cache.COURSE_DATA_BASE):]
        path = cache.repo_data_dir() / name
        if path.is_file():
            print(f"  ok    {path.stat().st_size:>11,}  {name}")
        else:
            print(f"  MISSING            {name}")
            problems.append((url, sorted(course[url]), "no file in data/"))

    if other:
        print("\n-- external URLs (downloaded to the fallback cache) --")
        for url in sorted(other):
            try:
                p = cache.fetch(url, force=args.refresh)
                print(f"  ok    {p.stat().st_size:>11,}  {url}")
            except Exception as exc:
                print(f"  FAIL               {url}  ({exc.__class__.__name__})")
                problems.append((url, sorted(other[url]), str(exc)))

    if example:
        print("\n-- illustrative, skipped --")
        for u, f in sorted(example.items()):
            print(f"  {u}\n      {', '.join(sorted(f))}")

    print()
    if problems:
        print(f"{len(problems)} URL(s) with no data behind them:")
        for url, files, why in problems:
            print(f"  {url}\n      {why}\n      used in: {', '.join(files)}")
        print("\nIf a course-site file is missing, run: python tools/fetch_data.py")
        return 1

    print("All data URLs resolve. Materials will render with no network.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
