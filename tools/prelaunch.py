#!/usr/bin/env python3
"""
EDS 217 pre-launch punch list.

Definitions live in tasks/2026-planning/prelaunch/punchlist.yml, which is
hand-editable and keeps its comments. Mutable state lives beside it in
state.json, which this tool maintains. Keeping them apart means the CLI never
rewrites the file you read.

    python tools/prelaunch.py status              what is left, grouped
    python tools/prelaunch.py next                the next item you can start
    python tools/prelaunch.py show D6             one item in full
    python tools/prelaunch.py check D6            run its verification
    python tools/prelaunch.py check --all         run every verification
    python tools/prelaunch.py certify D6 -n "..." record the sign-off
    python tools/prelaunch.py note D6 "..."       append a working note
    python tools/prelaunch.py set D6 in_progress  move an item by hand
    python tools/prelaunch.py dashboard           rebuild the HTML dashboard

An item becomes "verified" when its verification command passes. It becomes
"certified" only when a verified item is signed off. Certification of an item
whose verification is failing requires --force and a written reason, which is
recorded alongside the sign-off so it stays visible.
"""

import argparse
import datetime as dt
import json
import os
import shutil
import subprocess
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PRELAUNCH = ROOT / "tasks/2026-planning/prelaunch"
REGISTRY = PRELAUNCH / "punchlist.yml"
STATE = PRELAUNCH / "state.json"
DASHBOARD = PRELAUNCH / "dashboard.html"
DASHBOARD_BODY = PRELAUNCH / "dashboard.body.html"

DEFAULT_SIGNER = "Kelly Caylor"

SEVERITY_ORDER = {"blocker": 0, "high": 1, "medium": 2, "low": 3}
STATE_ORDER = ["blocked", "open", "in_progress", "verified", "certified", "deferred"]

COLOR = sys.stdout.isatty()


def paint(s, code):
    return f"\033[{code}m{s}\033[0m" if COLOR else s


BOLD = lambda s: paint(s, "1")
DIM = lambda s: paint(s, "2")
RED = lambda s: paint(s, "31")
GREEN = lambda s: paint(s, "32")
YELLOW = lambda s: paint(s, "33")
BLUE = lambda s: paint(s, "36")


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def git_sha():
    r = subprocess.run(["git", "rev-parse", "--short", "HEAD"],
                       cwd=str(ROOT), capture_output=True, text=True)
    return r.stdout.strip() or "unknown"


# ------------------------------------------------------------------ model

def load_registry():
    try:
        import yaml
    except ImportError:
        sys.exit("PyYAML is needed. Install it with: pip install pyyaml")
    data = yaml.safe_load(REGISTRY.read_text())
    items = {i["id"]: i for i in data["items"]}
    return data.get("meta", {}), items


def load_state():
    if STATE.exists():
        return json.loads(STATE.read_text())
    return {"schema": 1, "updated": None, "items": {}}


def save_state(state):
    state["updated"] = now()
    PRELAUNCH.mkdir(parents=True, exist_ok=True)
    STATE.write_text(json.dumps(state, indent=2, sort_keys=True) + "\n")


def item_state(item, state):
    """The state to act on, which is not always the state written down."""
    rec = state["items"].get(item["id"], {})
    declared = rec.get("state") or item.get("state", "open")
    if declared == "deferred":
        return "deferred"
    if rec.get("signoff"):
        return "certified"
    last = (rec.get("checks") or [None])[-1]
    if last and last.get("ok"):
        return "verified"
    if declared == "in_progress":
        return "in_progress"
    return declared


def blockers_open(item, items, state):
    return [b for b in item.get("blocked_by", [])
            if b in items and item_state(items[b], state) != "certified"]


def effective(item, items, state):
    s = item_state(item, state)
    if s in ("open", "in_progress") and blockers_open(item, items, state):
        return "blocked"
    return s


def sort_key(item, items, state):
    return (SEVERITY_ORDER.get(item.get("severity", "low"), 9),
            STATE_ORDER.index(effective(item, items, state))
            if effective(item, items, state) in STATE_ORDER else 9,
            item["id"])


def days_left(meta):
    try:
        first = dt.date.fromisoformat(str(meta.get("first_class_day")))
    except Exception:
        return None
    return (first - dt.date.today()).days


# ------------------------------------------------------------------ actions

def run_check(item, state, timeout=900):
    verify = item.get("verify", {})
    if verify.get("kind") != "command":
        return None
    cmd = verify["cmd"]
    started = now()
    try:
        r = subprocess.run(cmd, shell=True, cwd=str(ROOT), capture_output=True,
                           text=True, timeout=timeout,
                           env={**os.environ, "MPLBACKEND": "Agg"})
        code, out, err = r.returncode, r.stdout, r.stderr
    except subprocess.TimeoutExpired:
        code, out, err = 124, "", f"timed out after {timeout}s"
    evidence = (out + ("\n" + err if err.strip() else "")).strip()
    rec = {
        "at": started,
        "cmd": cmd,
        "exit": code,
        "ok": code == 0,
        "could_not_run": code == 2,
        "git_sha": git_sha(),
        "evidence": evidence[-4000:],
    }
    entry = state["items"].setdefault(item["id"], {})
    entry.setdefault("checks", []).append(rec)
    entry["checks"] = entry["checks"][-10:]
    if rec["ok"] and entry.get("signoff"):
        pass
    return rec


def cmd_check(args, meta, items, state):
    targets = list(items.values()) if args.all else [items[i] for i in args.ids]
    ran = 0
    for item in targets:
        if item.get("verify", {}).get("kind") != "command":
            if not args.all:
                print(f"{item['id']}  manual item, no command to run.")
                print(f"       {item['verify'].get('cmd', '')}")
                print(f"       certify it with: python tools/prelaunch.py "
                      f"certify {item['id']} -n \"what you confirmed\"")
            continue
        rec = run_check(item, state)
        ran += 1
        mark = GREEN("PASS") if rec["ok"] else (
            YELLOW("SKIP") if rec["could_not_run"] else RED("FAIL"))
        print(f"{mark}  {item['id']}  {item['title']}")
        if args.verbose or (not rec["ok"] and not args.all):
            for line in rec["evidence"].splitlines()[:25]:
                print("      " + line)
    save_state(state)
    if ran:
        print(DIM(f"\n{ran} verification(s) run, recorded in {STATE.relative_to(ROOT)}"))
    return 0


def cmd_certify(args, meta, items, state):
    """Sign off one item, or several that one sentence covers."""
    ids = args.ids
    if len(ids) > 1:
        rc = 0
        for one in ids:
            sub = argparse.Namespace(**vars(args))
            sub.ids = [one]
            rc |= _certify_one(sub, meta, items, state)
        return rc
    return _certify_one(args, meta, items, state)


def _certify_one(args, meta, items, state):
    item = items[args.ids[0]]
    entry = state["items"].setdefault(item["id"], {})
    kind = item.get("verify", {}).get("kind")
    last = (entry.get("checks") or [None])[-1]

    if kind == "command":
        if not last:
            print(RED(f"{item['id']} has never been verified."))
            print(f"Run: python tools/prelaunch.py check {item['id']}")
            return 1
        if not last["ok"] and not args.force:
            print(RED(f"{item['id']} last verified as failing at {last['at']}."))
            print("Fix it and re-check, or certify with --force and a written reason.")
            return 1
    if not args.note:
        print(RED("A sign-off needs a note saying what you confirmed. Use -n."))
        return 1

    entry["signoff"] = {
        "at": now(),
        "by": args.by,
        "note": args.note,
        "git_sha": git_sha(),
        "forced": bool(args.force),
        "verification": {"kind": kind,
                         "ok": bool(last and last["ok"]),
                         "at": last["at"] if last else None},
    }
    entry["state"] = "certified"
    save_state(state)
    print(GREEN(f"CERTIFIED  {item['id']}  {item['title']}"))
    print(f"  by {args.by} at {entry['signoff']['at']} on {entry['signoff']['git_sha']}")
    print(f"  {args.note}")
    if args.force:
        print(YELLOW("  Recorded as forced. The failing verification stays visible."))
    remaining = [i for i in items.values()
                 if effective(i, items, state) not in ("certified", "deferred")
                 and i.get("severity") == "blocker"]
    print(DIM(f"\n{len(remaining)} blocker(s) left."))
    return 0


def cmd_note(args, meta, items, state):
    entry = state["items"].setdefault(args.id, {})
    entry.setdefault("notes", []).append({"at": now(), "text": args.text})
    save_state(state)
    print(f"noted on {args.id}")
    return 0


def cmd_set(args, meta, items, state):
    if args.new_state not in STATE_ORDER:
        print(f"state must be one of: {', '.join(STATE_ORDER)}")
        return 1
    entry = state["items"].setdefault(args.id, {})
    if args.new_state != "certified":
        entry.pop("signoff", None)
    entry["state"] = args.new_state
    save_state(state)
    print(f"{args.id} -> {args.new_state}")
    return 0


def cmd_show(args, meta, items, state):
    item = items[args.id]
    entry = state["items"].get(args.id, {})
    eff = effective(item, items, state)
    w = shutil.get_terminal_size((100, 24)).columns - 4

    print(BOLD(f"\n{item['id']}  {item['title']}"))
    print(DIM(f"{item['category']} · {item['severity']} · owner {item['owner']} · {eff}"))
    blocked = blockers_open(item, items, state)
    if blocked:
        print(YELLOW(f"blocked by: {', '.join(blocked)}"))
    if item.get("blocks"):
        print(DIM(f"blocks: {', '.join(item['blocks'])}"))

    for label in ("why", "evidence", "action"):
        if item.get(label):
            print(BOLD(f"\n{label.upper()}"))
            for para in str(item[label]).strip().split("\n\n"):
                print(textwrap.fill(" ".join(para.split()), width=w,
                                    initial_indent="  ", subsequent_indent="  "))
    v = item.get("verify", {})
    print(BOLD("\nVERIFY"))
    print(f"  kind:   {v.get('kind')}")
    print(f"  cmd:    {v.get('cmd')}")
    print(f"  expect: {v.get('expect')}")

    checks = entry.get("checks") or []
    if checks:
        last = checks[-1]
        mark = GREEN("PASS") if last["ok"] else (
            YELLOW("COULD NOT RUN") if last["could_not_run"] else RED("FAIL"))
        print(BOLD("\nLAST VERIFICATION") + f"  {mark}  {last['at']}  on {last['git_sha']}")
        for line in last["evidence"].splitlines()[:30]:
            print("  " + line)
    if entry.get("signoff"):
        s = entry["signoff"]
        print(BOLD("\nSIGN-OFF"))
        print(f"  {s['by']} at {s['at']} on {s['git_sha']}"
              + ("  (forced)" if s.get("forced") else ""))
        print(textwrap.fill(s["note"], width=w, initial_indent="  ",
                            subsequent_indent="  "))
    for n in entry.get("notes", []):
        print(DIM(f"\nnote {n['at']}: {n['text']}"))
    print()
    return 0


def cmd_next(args, meta, items, state):
    # Sign-offs come first. A verified item holds up everything that waits on it,
    # and clearing one costs a sentence, so it is always the cheapest next move.
    awaiting = [i for i in items.values() if effective(i, items, state) == "verified"]
    if awaiting:
        awaiting.sort(key=lambda i: sort_key(i, items, state))
        print(BOLD(f"{len(awaiting)} item(s) verified and waiting on your sign-off.\n"))
        for i in awaiting:
            entry = state["items"].get(i["id"], {})
            last = (entry.get("checks") or [None])[-1]
            unblocks = [b for b in i.get("blocks", []) if b in items]
            print(f"  {BOLD(i['id']):<6} {i['title']}")
            if last:
                first = (last["evidence"] or "").splitlines()
                if len(first) > 1:
                    print(DIM(f"         {first[1].strip()[:88]}"))
            if unblocks:
                print(DIM(f"         signing this off unblocks {', '.join(unblocks)}"))
            print(DIM(f"         python tools/prelaunch.py certify {i['id']} -n \"...\""))
        print()

    ready = [i for i in items.values()
             if effective(i, items, state) in ("open", "in_progress")]
    if not ready:
        blocked = [i for i in items.values() if effective(i, items, state) == "blocked"]
        if blocked:
            print("Everything startable is done. Still blocked:")
            for i in sorted(blocked, key=lambda x: sort_key(x, items, state)):
                print(f"  {i['id']}  {i['title']}  (waiting on "
                      f"{', '.join(blockers_open(i, items, state))})")
        else:
            print(GREEN("Nothing open. Every item is certified or deferred."))
        return 0
    ready.sort(key=lambda i: sort_key(i, items, state))
    item = ready[0]
    print(DIM(f"{len(ready)} item(s) startable. Next by severity:\n"))
    args.id = item["id"]
    return cmd_show(args, meta, items, state)


def cmd_status(args, meta, items, state):
    d = days_left(meta)
    total = len(items)
    counts = {}
    for i in items.values():
        counts[effective(i, items, state)] = counts.get(effective(i, items, state), 0) + 1
    certified = counts.get("certified", 0)
    deferred = counts.get("deferred", 0)

    print(BOLD(f"\nEDS 217 {meta.get('term', '')} pre-launch"))
    line = f"first class {meta.get('first_class_day')}"
    if d is not None:
        line += f", {d} day{'s' if d != 1 else ''} from today"
    print(DIM(line))

    width = 40
    done = int(width * certified / max(total, 1))
    bar = "█" * done + "·" * (width - done)
    print(f"\n  {bar}  {certified}/{total} certified"
          + (f", {deferred} deferred" if deferred else ""))

    blockers = [i for i in items.values()
                if i.get("severity") == "blocker"
                and effective(i, items, state) not in ("certified", "deferred")]
    if blockers:
        print(RED(f"\n  {len(blockers)} blocker(s) between here and a working course site."))
    else:
        print(GREEN("\n  No blockers left."))

    order = ["deploy", "content", "tooling", "assets", "housekeeping"]
    shown = 0
    for cat in order:
        group = [i for i in items.values() if i.get("category") == cat]
        if not group:
            continue
        group.sort(key=lambda i: sort_key(i, items, state))
        cdone = sum(1 for i in group
                    if effective(i, items, state) in ("certified", "deferred"))
        print(BOLD(f"\n{cat.upper()}") + DIM(f"  {cdone}/{len(group)}"))
        for i in group:
            eff = effective(i, items, state)
            if not args.all and eff in ("certified", "deferred"):
                continue
            shown += 1
            mark = {"certified": GREEN("[x]"), "verified": BLUE("[~]"),
                    "blocked": DIM("[.]"), "in_progress": YELLOW("[>]"),
                    "deferred": DIM("[-]")}.get(eff, "[ ]")
            sev = {"blocker": RED("blocker"), "high": YELLOW("high   "),
                   "medium": "medium ", "low": DIM("low    ")}[i["severity"]]
            extra = ""
            if eff == "blocked":
                extra = DIM(f"  waiting on {', '.join(blockers_open(i, items, state))}")
            print(f"  {mark} {BOLD(i['id']):<6} {sev}  {i['title']}{extra}")
    if not shown and not args.all:
        print(GREEN("\nNothing outstanding. Use --all to see certified items."))
    print(DIM(f"\n  python tools/prelaunch.py next     to start the next item"))
    print(DIM(f"  python tools/prelaunch.py dashboard  to rebuild the HTML view\n"))
    return 0


def cmd_export(args, meta, items, state):
    print(json.dumps(build_payload(meta, items, state), indent=2))
    return 0


def build_payload(meta, items, state):
    out = []
    for i in sorted(items.values(), key=lambda x: sort_key(x, items, state)):
        entry = state["items"].get(i["id"], {})
        checks = entry.get("checks") or []
        last = checks[-1] if checks else None
        out.append({
            "id": i["id"],
            "title": i["title"],
            "category": i.get("category"),
            "severity": i.get("severity"),
            "owner": i.get("owner"),
            "state": effective(i, items, state),
            "why": str(i.get("why", "")).strip(),
            "evidence": str(i.get("evidence", "")).strip(),
            "action": str(i.get("action", "")).strip(),
            "verify": i.get("verify", {}),
            "blocked_by": i.get("blocked_by", []),
            "blocks": i.get("blocks", []),
            "waiting_on": blockers_open(i, items, state),
            "last_check": last,
            "signoff": entry.get("signoff"),
            "notes": entry.get("notes", []),
        })
    return {
        "meta": {**meta, "generated": now(), "git_sha": git_sha(),
                 "days_left": days_left(meta)},
        "items": out,
    }


def cmd_dashboard(args, meta, items, state):
    sys.path.insert(0, str(ROOT / "tools"))
    import prelaunch_dashboard as pd
    payload = build_payload(meta, items, state)
    body = pd.render_body(payload)
    DASHBOARD_BODY.write_text(body)
    DASHBOARD.write_text(pd.render_standalone(body, payload))
    print(f"wrote {DASHBOARD.relative_to(ROOT)}")
    print(f"wrote {DASHBOARD_BODY.relative_to(ROOT)}  (body only, for publishing)")
    if args.open:
        subprocess.run(["open", str(DASHBOARD)], check=False)
    return 0


# ------------------------------------------------------------------ cli

def main(argv=None):
    p = argparse.ArgumentParser(
        prog="prelaunch",
        description="EDS 217 pre-launch punch list",
        formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    s = sub.add_parser("status", help="what is left")
    s.add_argument("--all", action="store_true", help="include certified items")
    s.set_defaults(fn=cmd_status)

    s = sub.add_parser("next", help="the next item you can start")
    s.set_defaults(fn=cmd_next)

    s = sub.add_parser("show", help="one item in full")
    s.add_argument("id")
    s.set_defaults(fn=cmd_show)

    s = sub.add_parser("check", help="run verifications")
    s.add_argument("ids", nargs="*")
    s.add_argument("--all", action="store_true")
    s.add_argument("-v", "--verbose", action="store_true")
    s.set_defaults(fn=cmd_check)

    s = sub.add_parser("certify", help="record a sign-off, on one item or several")
    s.add_argument("ids", nargs="+", metavar="ID")
    s.add_argument("-n", "--note", help="what you confirmed")
    s.add_argument("--by", default=DEFAULT_SIGNER)
    s.add_argument("--force", action="store_true",
                   help="sign off despite a failing or absent verification")
    s.set_defaults(fn=cmd_certify)

    s = sub.add_parser("note", help="append a working note")
    s.add_argument("id")
    s.add_argument("text")
    s.set_defaults(fn=cmd_note)

    s = sub.add_parser("set", help="move an item by hand")
    s.add_argument("id")
    s.add_argument("new_state")
    s.set_defaults(fn=cmd_set)

    s = sub.add_parser("dashboard", help="rebuild the HTML dashboard")
    s.add_argument("--open", action="store_true")
    s.set_defaults(fn=cmd_dashboard)

    s = sub.add_parser("export", help="print the dashboard payload as JSON")
    s.set_defaults(fn=cmd_export)

    args = p.parse_args(argv)
    meta, items = load_registry()
    state = load_state()
    for attr in ("id", "ids"):
        val = getattr(args, attr, None)
        for one in ([val] if isinstance(val, str) else (val or [])):
            if one not in items:
                sys.exit(f"no such item: {one}. Known ids: {' '.join(items)}")
    return args.fn(args, meta, items, state)


if __name__ == "__main__":
    sys.exit(main())
