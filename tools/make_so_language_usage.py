#!/usr/bin/env python3
"""Rebuild data/so_2025_language_usage.csv from the Stack Overflow survey archive.

The Day 1 lecture (course-materials/lectures/00_intro_to_python_2026.ipynb) plots which
languages people use. It used to plot Anaconda's State of Data Science survey, but Anaconda's
last public data file is from 2023 and the survey no longer asks the language question, so the
lecture now uses Stack Overflow's survey instead.

Stack Overflow publishes the full anonymised responses as a 134 MB results.csv, which is far too
large to read live in class. It also publishes the aggregated chart data as JSON, which is what
this script reads. The output keeps three of the six respondent groups, because those three are
the ones the lecture compares.

Upstream:  https://github.com/StackExchange/Survey/tree/main/packages/archive/2025
Licence:   Open Database License (ODbL) 1.0

Usage:
    python3 tools/make_so_language_usage.py            # rebuild from upstream
    python3 tools/make_so_language_usage.py --check    # verify the in-repo file matches
"""
from __future__ import annotations

import argparse
import json
import sys
import urllib.request
from decimal import Decimal, ROUND_HALF_UP
from pathlib import Path

SOURCE = (
    "https://raw.githubusercontent.com/StackExchange/Survey/main/"
    "packages/archive/2025/json/technology.json"
)

OUT = Path(__file__).resolve().parent.parent / "data" / "so_2025_language_usage.csv"

# Stack Overflow's key for each group, in the order the lecture uses them.
GROUPS = ["Language", "Language_prof", "Language_learn"]

UA = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0 Safari/537.36"}


def one_decimal(fraction: float) -> str:
    """Round a proportion to a percentage with one decimal, matching the published chart.

    Stack Overflow stores each percentage to four decimals and formats it in the browser with
    JavaScript's toFixed, which rounds an exact half away from zero. Python's own formatting
    rounds an exact half to the even digit instead, so 0.0525 prints as 5.2 where the published
    chart reads 5.3. Taking the Decimal of the float rather than of its string keeps the binary
    value, and ROUND_HALF_UP then settles the exact ties the same way the browser does.
    """
    return str(Decimal(fraction * 100).quantize(Decimal("0.1"), rounding=ROUND_HALF_UP))


def build() -> str:
    request = urllib.request.Request(SOURCE, headers=UA)
    with urllib.request.urlopen(request, timeout=60) as response:
        payload = json.load(response)

    datasets = payload["Language"]["datasets"]
    lines = ["group,total_respondents,language,count,percent"]
    for key in GROUPS:
        group = datasets[key]
        for row in group["data"]:
            lines.append(
                f'"{group["name"]}",{group["total_respondents"]},'
                f'"{row["response"]}",{row["frequency"]},{one_decimal(row["percent"])}'
            )
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="compare against the in-repo file instead of rewriting it")
    args = parser.parse_args()

    csv = build()

    if args.check:
        if not OUT.exists():
            print(f"MISSING {OUT}")
            return 1
        if OUT.read_text() == csv:
            print(f"OK {OUT.name} matches upstream")
            return 0
        print(f"CHANGED {OUT.name} differs from upstream; rerun without --check to update")
        return 1

    OUT.write_text(csv)
    print(f"wrote {OUT} ({len(csv.splitlines()) - 1} rows)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
