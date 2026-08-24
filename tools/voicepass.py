#!/usr/bin/env python3
"""
The EDS 217 voice pass, one page at a time, resumable.

The pass runs over 89 pages across several days, from Nairobi and Wajir, on
connections that drop. So no state lives in a session. Everything is in
tasks/2026-planning/prelaunch/voice-pass.json, committed after every page, and
any new session can pick up mid-batch by running:

    python tools/voicepass.py resume

The workflow per page, which `resume` will tell you where you are in:

    1. start      records the page, the git SHA and the measurable counts
    2. edit       the write-as-kelly pass, fenced by tools/prose_guard.py
    3. coldread   a subagent reads the result having never seen the original
    4. findings   the cold reader's report is recorded, one entry per finding
    5. resolve    each finding becomes fixed, needs-kelly or wontfix
    6. signoff    Kelly's sentence, recorded with the SHA it was signed on

A page is never signed off with an open finding, and a batch is never closed
with an unsigned page.

    python tools/voicepass.py status
    python tools/voicepass.py resume
    python tools/voicepass.py start course-materials/day1.qmd
    python tools/voicepass.py record course-materials/day1.qmd findings.json
    python tools/voicepass.py resolve course-materials/day1.qmd 3 fixed -n "..."
    python tools/voicepass.py signoff course-materials/day1.qmd -n "..."
    python tools/voicepass.py pending
"""

import argparse
import datetime as dt
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LEDGER = ROOT / "tasks/2026-planning/prelaunch/voice-pass.json"

STATUSES = ["pending", "started", "edited", "cold_read", "resolved", "signed_off", "skipped"]
FINDING_STATES = ["open", "fixed", "needs-kelly", "wontfix"]

BATCHES = [
    (1, "Front page and day pages",
     "Every student sees these, and they set the register."),
    (2, "End-of-day activities",
     "The longest time-on-page of anything on the site."),
    (3, "Sessions, colabs and live coding",
     "Read alongside the instructor, so ambiguity surfaces in the room."),
    (4, "Cheatsheets",
     "Reference prose. Terse beats characterful here."),
    (5, "Answer keys",
     "Read after the fact. The written answers matter more than the voice."),
]

COLOR = sys.stdout.isatty()
def paint(s, c): return f"\033[{c}m{s}\033[0m" if COLOR else s
B = lambda s: paint(s, "1")
D = lambda s: paint(s, "2")
R = lambda s: paint(s, "31")
G = lambda s: paint(s, "32")
Y = lambda s: paint(s, "33")
C = lambda s: paint(s, "36")


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def sha():
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"], cwd=str(ROOT),
                       capture_output=True, text=True)
    return r.stdout.strip() or "unknown"


def dirty(path=None):
    cmd = ["git", "status", "--porcelain"] + ([str(path)] if path else [])
    r = subprocess.run(cmd, cwd=str(ROOT), capture_output=True, text=True)
    return [l for l in r.stdout.splitlines() if l.strip()]


def render_set():
    sys.path.insert(0, str(ROOT / "tools"))
    import prelaunch_checks as pc
    return [f for f in pc.correct_render_set() if f.endswith(".qmd")]


# Batch 1 is everything a student lands on rather than works through: the front
# page, the nine day pages, the workflow the course is built around, and the
# specification of the only deliverable.
BATCH_ONE = {
    "index.qmd",
    "course-materials/the-data-science-workflow.qmd",
    "course-materials/final_project.qmd",
}


def batch_of(path):
    p = str(path)
    if p in BATCH_ONE or p.startswith("course-materials/day"):
        return 1
    if "/eod-practice/" in p:
        return 2
    if "/answer-keys/" in p:
        return 5
    if "/cheatsheets/" in p or p == "cheatsheets.qmd":
        return 4
    return 3


def measure(path):
    """The counts a pass should move, recorded before and after."""
    sys.path.insert(0, str(ROOT / "tools"))
    import prose_guard as pg
    import re
    text = (ROOT / path).read_text(errors="replace")
    dem = pg.sentence_initial_demonstratives(text)
    return {
        "words": len(pg.prose_only(text).split()),
        "sentence_initial_demonstratives": sum(1 for d in dem if not d[3]),
        "elliptical_numerals": len(pg.elliptical_numerals(text)),
        "causal_since": len(re.findall(
            r"\bsince\s+(?!then\b|yesterday\b|last\b|\d{4}\b|Day \d|Monday|Tuesday|"
            r"Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|"
            r"April|May|June|July|August|September|October|November|December)",
            text, re.I)),
        "em_dashes": text.count("—"),
    }


def load():
    if LEDGER.exists():
        return json.loads(LEDGER.read_text())
    pages = {}
    for f in render_set():
        pages[f] = {"batch": batch_of(f), "status": "pending", "history": [],
                    "findings": [], "metrics": {}}
    return {"schema": 1, "updated": None, "started": now(), "pages": pages}


def save(led):
    led["updated"] = now()
    LEDGER.parent.mkdir(parents=True, exist_ok=True)
    LEDGER.write_text(json.dumps(led, indent=1, sort_keys=True) + "\n")


def get(led, path):
    p = str(path)
    if p not in led["pages"]:
        sys.exit(f"{p} is not in the render set. Known pages: run `status`.")
    return led["pages"][p]


def log(entry, event, **kw):
    entry["history"].append({"at": now(), "event": event, "sha": sha(), **kw})


# ------------------------------------------------------------------ commands

def cmd_status(a, led):
    print(B("\nEDS 217 voice pass"))
    tot = len(led["pages"])
    done = sum(1 for v in led["pages"].values() if v["status"] in ("signed_off", "skipped"))
    width = 40
    fill = int(width * done / max(tot, 1))
    print(f"  {'█' * fill}{'·' * (width - fill)}  {done}/{tot} pages signed off\n")
    for n, name, why in BATCHES:
        pages = {k: v for k, v in led["pages"].items() if v["batch"] == n}
        if not pages:
            continue
        d = sum(1 for v in pages.values() if v["status"] in ("signed_off", "skipped"))
        head = f"BATCH {n}  {name}"
        print(B(head) + D(f"  {d}/{len(pages)}"))
        print(D(f"  {why}"))
        if a.all or d < len(pages):
            for k, v in sorted(pages.items()):
                if not a.all and v["status"] in ("signed_off", "skipped"):
                    continue
                mark = {"pending": "[ ]", "started": Y("[>]"), "edited": Y("[e]"),
                        "cold_read": C("[r]"), "resolved": C("[~]"),
                        "signed_off": G("[x]"), "skipped": D("[-]")}[v["status"]]
                openf = sum(1 for f in v["findings"] if f["status"] == "open")
                needs = sum(1 for f in v["findings"] if f["status"] == "needs-kelly")
                extra = ""
                if openf:
                    extra += R(f"  {openf} open finding(s)")
                if needs:
                    extra += Y(f"  {needs} waiting on Kelly")
                print(f"    {mark} {k}{extra}")
        print()
    nk = [(k, f) for k, v in led["pages"].items() for f in v["findings"]
          if f["status"] == "needs-kelly"]
    if nk:
        print(Y(f"{len(nk)} finding(s) waiting on Kelly. See `voicepass.py pending`.\n"))
    return 0


def cmd_resume(a, led):
    """Say exactly what to do next, assuming the reader remembers nothing."""
    print(B("\nWhere the voice pass is\n"))
    d = dirty()
    if d:
        print(Y("The working tree is dirty:"))
        for l in d[:10]:
            print(f"    {l}")
        print()

    in_flight = [(k, v) for k, v in led["pages"].items()
                 if v["status"] in ("started", "edited", "cold_read", "resolved")]
    if in_flight:
        k, v = sorted(in_flight)[0]
        print(f"{B(k)} is mid-pass, at {B(v['status'])}.")
        last = v["history"][-1] if v["history"] else None
        if last:
            print(D(f"  last event: {last['event']} at {last['at']} on {last['sha']}"))
        openf = [f for f in v["findings"] if f["status"] == "open"]
        nxt = {
            "started": "Run the write-as-kelly pass on it, then:\n"
                       f"    python tools/prose_guard.py verify {k}\n"
                       f"    python tools/voicepass.py edited {k}",
            "edited": "Cold-read it. Use the prompt in\n"
                      "    tasks/2026-planning/prelaunch/cold-read-prompt.md\n"
                      f"  then record the report:\n"
                      f"    python tools/voicepass.py record {k} findings.json",
            "cold_read": (f"Resolve the {len(openf)} open finding(s):\n"
                          f"    python tools/voicepass.py resolve {k} <n> fixed -n \"...\""),
            "resolved": (f"Ask Kelly to sign off:\n"
                         f"    python tools/voicepass.py signoff {k} -n \"...\""),
        }[v["status"]]
        print("\n" + nxt + "\n")
        return 0

    pending = sorted(k for k, v in led["pages"].items() if v["status"] == "pending")
    if not pending:
        print(G("Every page is signed off or skipped."))
        return 0
    pending.sort(key=lambda k: (led["pages"][k]["batch"], k))
    k = pending[0]
    n = led["pages"][k]["batch"]
    name = next(b[1] for b in BATCHES if b[0] == n)
    left = sum(1 for p in pending if led["pages"][p]["batch"] == n)
    print(f"Nothing is mid-pass. Next is batch {n}, {name}, "
          f"with {left} page(s) left.\n")
    print(f"  python tools/voicepass.py start {k}\n")
    return 0


def cmd_start(a, led):
    e = get(led, a.page)
    if e["status"] not in ("pending", "skipped"):
        print(Y(f"{a.page} is already at {e['status']}. Use `resume`."))
        return 1
    e["metrics"]["before"] = measure(a.page)
    e["status"] = "started"
    log(e, "started")
    save(led)
    m = e["metrics"]["before"]
    print(B(f"\nstarted {a.page}") + D(f"  batch {e['batch']}  on {sha()}"))
    print(f"  {m['words']} words of prose")
    print(f"  {m['sentence_initial_demonstratives']} sentence-initial demonstratives")
    print(f"  {m['elliptical_numerals']} elliptical numerals")
    print(f"  {m['causal_since']} causal 'since'")
    print(D("\n  Read tasks/2026-planning/prelaunch/house-style.md before editing."))
    print(D(f"  python tools/prose_guard.py regions {a.page}\n"))
    return 0


def cmd_edited(a, led):
    e = get(led, a.page)
    if e["status"] != "started":
        print(Y(f"{a.page} is at {e['status']}, not started."))
        return 1
    r = subprocess.run([sys.executable, "tools/prose_guard.py", "verify", a.page],
                       cwd=str(ROOT), capture_output=True, text=True)
    print(r.stdout.strip())
    if r.returncode != 0 and not a.force:
        print(R("\nThe guard reports a change outside prose. Explain it with --force "
                "and a note, or undo it."))
        return 1
    e["metrics"]["after"] = measure(a.page)
    e["status"] = "edited"
    log(e, "edited", note=a.note, guard_forced=bool(a.force))
    save(led)
    b, af = e["metrics"]["before"], e["metrics"]["after"]
    print(B(f"\nedited {a.page}"))
    for key in ("sentence_initial_demonstratives", "elliptical_numerals",
                "causal_since", "em_dashes"):
        print(f"  {key}: {b[key]} -> {af[key]}")
    print(D("\n  Next: cold-read it, using"))
    print(D("  tasks/2026-planning/prelaunch/cold-read-prompt.md\n"))
    return 0


def cmd_record(a, led):
    e = get(led, a.page)
    data = json.loads(Path(a.report).read_text())
    items = data if isinstance(data, list) else data.get("findings", [])
    e["findings"] = [
        {"id": i + 1,
         "severity": f.get("severity", "unrated"),
         "text": f.get("text") or f.get("summary") or str(f),
         "status": "open", "note": None}
        for i, f in enumerate(items)
    ]
    e["status"] = "cold_read"
    log(e, "cold_read", findings=len(e["findings"]))
    save(led)
    print(B(f"\n{len(e['findings'])} finding(s) recorded on {a.page}\n"))
    for f in e["findings"]:
        print(f"  {f['id']:>2}. [{f['severity']}] {f['text'][:96]}")
    print(D(f"\n  python tools/voicepass.py resolve {a.page} 1 fixed -n \"...\"\n"))
    return 0


def cmd_resolve(a, led):
    e = get(led, a.page)
    if a.state not in FINDING_STATES:
        sys.exit(f"state must be one of: {', '.join(FINDING_STATES)}")
    hit = next((f for f in e["findings"] if f["id"] == a.number), None)
    if hit is None:
        sys.exit(f"no finding {a.number} on {a.page}")
    if a.state in ("wontfix", "needs-kelly") and not a.note:
        sys.exit(f"a finding marked {a.state} needs a note saying why")
    hit["status"] = a.state
    hit["note"] = a.note
    hit["resolved_at"] = now()
    hit["sha"] = sha()
    openf = [f for f in e["findings"] if f["status"] == "open"]
    if not openf and e["status"] == "cold_read":
        e["status"] = "resolved"
        log(e, "resolved")
    save(led)
    print(f"{a.page} finding {a.number} -> {a.state}")
    if openf:
        print(D(f"  {len(openf)} still open: {', '.join(str(f['id']) for f in openf)}"))
    else:
        print(G("  Every finding resolved. Ready for sign-off."))
    return 0


def cmd_signoff(a, led):
    e = get(led, a.page)
    openf = [f for f in e["findings"] if f["status"] == "open"]
    if openf:
        print(R(f"{len(openf)} finding(s) still open on {a.page}: "
                f"{', '.join(str(f['id']) for f in openf)}"))
        return 1
    if e["status"] not in ("resolved", "cold_read"):
        print(R(f"{a.page} is at {e['status']}. It has not been cold-read."))
        return 1
    if not a.note:
        print(R("A sign-off needs a note saying what you read and agreed to."))
        return 1
    e["status"] = "signed_off"
    e["signoff"] = {"at": now(), "by": a.by, "note": a.note, "sha": sha()}
    log(e, "signed_off")
    save(led)
    print(G(f"\nSIGNED OFF  {a.page}"))
    print(f"  {a.by} at {e['signoff']['at']} on {e['signoff']['sha']}")
    left = sum(1 for v in led["pages"].values()
               if v["batch"] == e["batch"] and v["status"] not in ("signed_off", "skipped"))
    print(D(f"\n  {left} page(s) left in batch {e['batch']}\n"))
    return 0


def cmd_skip(a, led):
    e = get(led, a.page)
    if not a.note:
        sys.exit("a skipped page needs a note saying why")
    e["status"] = "skipped"
    log(e, "skipped", note=a.note)
    save(led)
    print(f"{a.page} skipped: {a.note}")
    return 0


def cmd_reopen(a, led):
    """Send a page back to the start of the pass.

    Kelly states a new rule roughly once a sitting, and a rule stated on Tuesday
    applies to the page signed off on Monday. Reopening is normal, not a failure,
    so it is a first-class move rather than something done by hand in the JSON.
    """
    e = get(led, a.page)
    if not a.note:
        sys.exit("a reopened page needs a note saying what changed")
    was = e["status"]
    e["status"] = "started"
    e.setdefault("metrics", {})["before"] = measure(a.page)
    log(e, "reopened", was=was, note=a.note)
    save(led)
    print(f"{a.page} reopened from {was}: {a.note}")
    print(D("  Earlier findings and their resolutions are kept in the history."))
    return 0


def cmd_pending(a, led):
    rows = [(k, f) for k, v in sorted(led["pages"].items()) for f in v["findings"]
            if f["status"] == "needs-kelly"]
    if not rows:
        print(G("\nNothing is waiting on Kelly.\n"))
        return 0
    print(B(f"\n{len(rows)} finding(s) waiting on Kelly\n"))
    for k, f in rows:
        print(f"  {B(k)}  finding {f['id']}")
        print(f"    {f['text']}")
        if f.get("note"):
            print(D(f"    {f['note']}"))
        print()
    return 0


def main(argv=None):
    p = argparse.ArgumentParser(prog="voicepass", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status"); s.add_argument("--all", action="store_true"); s.set_defaults(fn=cmd_status)
    s = sub.add_parser("resume"); s.set_defaults(fn=cmd_resume)
    s = sub.add_parser("start"); s.add_argument("page"); s.set_defaults(fn=cmd_start)
    s = sub.add_parser("edited"); s.add_argument("page")
    s.add_argument("-n", "--note"); s.add_argument("--force", action="store_true")
    s.set_defaults(fn=cmd_edited)
    s = sub.add_parser("record"); s.add_argument("page"); s.add_argument("report")
    s.set_defaults(fn=cmd_record)
    s = sub.add_parser("resolve"); s.add_argument("page"); s.add_argument("number", type=int)
    s.add_argument("state"); s.add_argument("-n", "--note"); s.set_defaults(fn=cmd_resolve)
    s = sub.add_parser("signoff"); s.add_argument("page"); s.add_argument("-n", "--note")
    s.add_argument("--by", default="Kelly Caylor"); s.set_defaults(fn=cmd_signoff)
    s = sub.add_parser("skip"); s.add_argument("page"); s.add_argument("-n", "--note")
    s.set_defaults(fn=cmd_skip)
    s = sub.add_parser("reopen"); s.add_argument("page"); s.add_argument("-n", "--note")
    s.set_defaults(fn=cmd_reopen)
    s = sub.add_parser("pending"); s.set_defaults(fn=cmd_pending)

    a = p.parse_args(argv)
    return a.fn(a, load())


if __name__ == "__main__":
    sys.exit(main())
