#!/usr/bin/env python3
"""
Download every dataset the course materials read, into the local cache.

Run this while online. Afterwards the same notebooks render with no network.

    python tools/warm_cache.py             # fetch anything not cached
    python tools/warm_cache.py --refresh   # re-download everything
    python tools/warm_cache.py --list      # just show what was found

Reports any URL that fails, which doubles as a dead-link check on the
course materials.
"""

import argparse
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import eds217_offline_cache as cache  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SKIP_DIRS = {"docs", "nbs", "extra_files", ".git", "tasks"}

# a URL passed straight into a pandas reader
DIRECT = re.compile(r"""pd\.read_\w+\(\s*['"](https?://[^'"]+)['"]""")
# a URL bound to a variable that a reader later uses
ASSIGN = re.compile(r"""^\s*\w*url\w*\s*=\s*['"](https?://[^'"]+)['"]""",
                    re.IGNORECASE | re.MULTILINE)
# urls collected in a list or dict literal, e.g. data_urls.py
BARE = re.compile(r"""['"](https?://[^'"]+\.(?:csv|tsv|txt|json|xlsx|xls))['"]""",
                  re.IGNORECASE)

PLACEHOLDER = re.compile(r"your-course-website\.com|example\.(com|org)", re.I)


def sources():
    files = [p for p in ROOT.rglob("*.qmd") if not any(s in p.parts for s in SKIP_DIRS)]
    files += [p for p in ROOT.rglob("*.py") if not any(s in p.parts for s in SKIP_DIRS)]
    return files


def collect():
    found = {}
    for p in sources():
        try:
            text = p.read_text(errors="ignore")
        except OSError:
            continue
        for rx in (DIRECT, ASSIGN, BARE):
            for m in rx.finditer(text):
                found.setdefault(m.group(1), set()).add(str(p.relative_to(ROOT)))
    return found


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--refresh", action="store_true")
    ap.add_argument("--list", action="store_true")
    args = ap.parse_args()

    found = collect()
    live = {u: f for u, f in found.items() if not PLACEHOLDER.search(u)}
    stub = {u: f for u, f in found.items() if PLACEHOLDER.search(u)}

    print(f"Found {len(found)} URLs across the course materials "
          f"({len(live)} real, {len(stub)} placeholder).")
    print(f"Cache directory: {cache.cache_dir()}\n")

    if args.list:
        for u, f in sorted(live.items()):
            print(f"  {u}\n      used in: {', '.join(sorted(f))}")
        if stub:
            print("\nPlaceholders (never resolvable, materials need fixing):")
            for u, f in sorted(stub.items()):
                print(f"  {u}\n      used in: {', '.join(sorted(f))}")
        return 0

    ok = 0
    failures = []
    for url in sorted(live):
        try:
            path = cache.fetch(url, force=args.refresh)
            size = path.stat().st_size
            if size == 0:
                raise OSError("downloaded 0 bytes")
            print(f"  ok    {size:>10,}  {url}")
            ok += 1
        except Exception as exc:
            print(f"  FAIL              {url}\n            {exc.__class__.__name__}: {exc}")
            failures.append((url, sorted(live[url])))

    print(f"\ncached {ok} datasets, {len(failures)} failed")

    if stub:
        print("\nPlaceholder URLs still in the materials (these fail for students too):")
        for u, f in sorted(stub.items()):
            print(f"  {u}  <-  {', '.join(sorted(f))}")

    if failures:
        print("\nFailed downloads, by file:")
        for u, f in failures:
            print(f"  {u}\n      {', '.join(f)}")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
