#!/usr/bin/env python3
"""
Verification checks for the EDS 217 pre-launch punch list.

Every item in tasks/2026-planning/prelaunch/punchlist.yml whose verify.kind is
"command" names one function in here. Each function returns (ok, evidence) where
evidence is a list of lines. Run one by name:

    python tools/prelaunch_checks.py d6_docs_data_tracked

Exit status is 0 when the check passes and 1 when it does not. The CLI in
tools/prelaunch.py calls this module rather than duplicating the logic.

Two rules these checks are written to obey:

1. A check that cannot run reports "could not run" and exits 2. It never reports
   a pass. Several checks need Quarto, conda or the network, none of which exist
   in the Cowork VM, and a green result from a check that did not actually run is
   worse than a red one.
2. A check states what it measured, not just whether it liked the answer.
"""

import ast
import json
import os
import re
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_PARTS = {
    "docs", "nbs", "extra_files", "_to_delete", ".git", ".quarto",
    ".ipynb_checkpoints", "__pycache__", "tasks",
}

DAY_DATES = {
    1: "08/31/2026", 2: "09/01/2026", 3: "09/02/2026", 4: "09/03/2026",
    5: "09/04/2026", 6: "09/08/2026", 7: "09/09/2026", 8: "09/10/2026",
    9: "09/11/2026",
}


class CannotRun(Exception):
    """Raised when a check has no way to reach a verdict."""


# ---------------------------------------------------------------- helpers

def sh(cmd, cwd=None):
    r = subprocess.run(cmd, shell=True, cwd=str(cwd or ROOT),
                       capture_output=True, text=True)
    return r.returncode, r.stdout, r.stderr


def skipped(path):
    return any(p in SKIP_PARTS for p in Path(path).parts)


def source_files(exts=(".qmd", ".ipynb")):
    out = []
    for ext in exts:
        for f in ROOT.rglob("*" + ext):
            rel = f.relative_to(ROOT)
            if not skipped(rel):
                out.append(rel)
    return sorted(out)


def live_qmd():
    """The qmd files a student can reach, plus the two site root pages."""
    files = [f for f in source_files((".qmd",))]
    excl = render_exclusions()
    return [f for f in files if not any(match_glob(str(f), p) for p in excl)]


def match_glob(path, pattern):
    rx = re.escape(pattern)
    rx = rx.replace(r"\*\*/", "(?:.*/)?").replace(r"\*\*", ".*")
    rx = rx.replace(r"\*", "[^/]*").replace(r"\?", ".")
    return re.fullmatch(rx, path) is not None


def quarto_render_block():
    text = (ROOT / "_quarto.yml").read_text()
    lines = text.splitlines()
    out, inside, indent = [], False, None
    for ln in lines:
        stripped = ln.strip()
        if re.match(r"^render:\s*$", stripped):
            inside = True
            indent = len(ln) - len(ln.lstrip())
            continue
        if inside:
            cur = len(ln) - len(ln.lstrip())
            if stripped and not stripped.startswith("#") and cur <= indent:
                break
            m = re.match(r'^-\s*"?([^"#]+?)"?\s*$', stripped)
            if m:
                out.append(m.group(1))
    return out


def render_exclusions():
    return [p[1:] for p in quarto_render_block() if p.startswith("!")]


def correct_render_set():
    """The files quarto actually builds, per _quarto.yml."""
    excl = render_exclusions()
    out = []
    for f in source_files():
        s = str(f)
        if any(match_glob(s, p) for p in excl):
            continue
        out.append(s)
    return sorted(out)


CODE_BLOCK = re.compile(r"^```\{python\}\s*$(.*?)^```\s*$", re.M | re.S)


def executing_python_blocks(path):
    """Yield the body of every ```{python} block that quarto will execute."""
    text = Path(path).read_text(errors="replace")
    for m in CODE_BLOCK.finditer(text):
        body = m.group(1)
        if re.search(r"^#\|\s*eval:\s*false\s*$", body, re.M):
            continue
        yield body


# Placeholders that appear in teaching prose to contrast a URL with a local path.
# warm_cache.py classifies these as illustrative and so do we.
ILLUSTRATIVE = {"some_file.csv", "measurements.csv", "filename.csv",
                "filename.xlsx", "data.csv", "my_data.csv"}


def loaded_datasets():
    """Every data filename the live corpus loads, including concatenated URLs."""
    names = set()
    lit = re.compile(r"https?://[^\s\"')]+/data/([A-Za-z0-9_.\-]+\.(?:csv|tsv|txt|json|xlsx|xls))")
    cat = re.compile(r"""\+\s*['"]([A-Za-z0-9_.\-]+\.(?:csv|tsv|txt|json|xlsx|xls))['"]""")
    for f in source_files():
        text = (ROOT / f).read_text(errors="replace")
        names.update(lit.findall(text))
        if "eds-217-essential-python.github.io/data/" in text:
            names.update(cat.findall(text))
    return names - ILLUSTRATIVE


def result(ok, lines):
    return ok, lines


# ---------------------------------------------------------------- D checks

def d1_clean_docs_guard():
    """clean_docs() must not run on an incremental build."""
    src = (ROOT / "build_docs.py").read_text()
    tree = ast.parse(src)
    parents = {}
    for node in ast.walk(tree):
        for child in ast.iter_child_nodes(node):
            parents[child] = node

    calls = [n for n in ast.walk(tree)
             if isinstance(n, ast.Call) and getattr(n.func, "id", None) == "clean_docs"]
    if not calls:
        return result(False, ["No call to clean_docs() found in build_docs.py."])

    lines = []
    unguarded = []
    for c in calls:
        guarded = False
        node = c
        while node in parents:
            node = parents[node]
            if isinstance(node, ast.If):
                test = ast.unparse(node.test)
                if "full" in test:
                    guarded = True
                    lines.append(f"  line {c.lineno}: guarded by  if {test}")
                    break
            if isinstance(node, ast.FunctionDef) and node.name != "main":
                guarded = True
                lines.append(f"  line {c.lineno}: inside {node.name}(), not the build path")
                break
        if not guarded:
            unguarded.append(c.lineno)
            lines.append(f"  line {c.lineno}: UNGUARDED, runs on every build path")

    ok = not unguarded
    head = ("clean_docs() is called only on the full-build path."
            if ok else
            f"clean_docs() runs unguarded at line(s) {unguarded}. "
            "An incremental build would delete the rendered site.")
    return result(ok, [head] + lines)


def d2_render_set():
    """build_docs.py --full must build exactly the set _quarto.yml declares."""
    correct = correct_render_set()
    lines = [f"_quarto.yml render exclusions: {render_exclusions() or 'none'}",
             f"correct render set: {len(correct)} files"]

    sys.path.insert(0, str(ROOT))
    try:
        import importlib
        bd = importlib.import_module("build_docs")
        importlib.reload(bd)
    except Exception as e:
        raise CannotRun(f"could not import build_docs.py: {e}")
    finally:
        sys.path.pop(0)

    cwd = os.getcwd()
    os.chdir(ROOT)
    try:
        actual = sorted(bd.get_all_buildable_files())
    finally:
        os.chdir(cwd)

    lines.append(f"build_docs.get_all_buildable_files(): {len(actual)} files")
    extra = sorted(set(actual) - set(correct))
    missing = sorted(set(correct) - set(actual))
    if extra:
        lines.append(f"would render {len(extra)} files it must not, first ten:")
        lines += ["    " + e for e in extra[:10]]
    if missing:
        lines.append(f"would skip {len(missing)} files it must render:")
        lines += ["    " + m for m in missing[:10]]
    ok = not extra and not missing
    return result(ok, lines)


def d3_lecture_kernels():
    """No notebook inside the render set may name the 2025 kernel."""
    inset = set(correct_render_set())
    hits = []
    for f in source_files((".ipynb",)):
        if str(f) not in inset:
            continue
        text = (ROOT / f).read_text(errors="replace")
        n = text.count("eds217_2025")
        if n:
            hits.append((str(f), n))
    lines = [f"notebooks in the render set: "
             f"{sum(1 for f in source_files(('.ipynb',)) if str(f) in inset)}"]
    for f, n in hits:
        lines.append(f"  {f}: {n} reference(s) to eds217_2025")
    if not hits:
        lines.append("No rendered notebook names the 2025 kernel.")
    return result(not hits, lines)


def d4_lectures_excluded():
    """course-materials/lectures must not be reachable on the site."""
    excl = render_exclusions()
    covered = [p for p in excl if "lectures" in p]
    inset = [f for f in correct_render_set() if "course-materials/lectures/" in f]
    lines = [f"render exclusions naming lectures: {covered or 'none'}",
             f"lecture files still in the render set: {len(inset)}"]
    lines += ["    " + f for f in inset[:8]]
    return result(not inset, lines)


def d5_render_complete():
    """docs/ must hold a complete, current render."""
    docs = ROOT / "docs"
    if not docs.exists():
        return result(False, ["docs/ does not exist. Run: make render"])
    html = [p for p in docs.rglob("*.html")]
    data_files = sorted(p.name for p in (ROOT / "data").iterdir() if p.is_file())
    docs_data = docs / "data"
    docs_data_files = sorted(p.name for p in docs_data.iterdir() if p.is_file()) if docs_data.exists() else []
    expected = len(correct_render_set())
    index = docs / "index.html"
    index_txt = index.read_text(errors="replace") if index.exists() else ""
    search = docs / "search.json"
    try:
        entries = len(json.loads(search.read_text())) if search.exists() else 0
    except Exception:
        entries = 0

    lines = [
        f"rendered HTML files: {len(html)}  (render set is {expected})",
        f"docs/data files: {len(docs_data_files)}  (data/ holds {len(data_files)})",
        f"search.json entries: {entries}",
        f"index.html says Summer 2026: {'Summer 2026' in index_txt}",
    ]
    missing_data = sorted(set(data_files) - set(docs_data_files))
    if missing_data:
        lines.append(f"missing from docs/data: {missing_data[:8]}")
    ok = (len(html) >= expected - 5
          and not missing_data and docs_data_files
          and "Summer 2026" in index_txt
          and entries >= expected - 5)
    return result(ok, lines)


def d10_render_current():
    """Every rendered page must be newer than the source it came from.

    The voice pass edits pages over several days, and previewing one page
    re-renders only that page. So docs/ can hold a coherent-looking site whose
    pages were built from different versions of the source. Counting files does
    not catch it; comparing timestamps does.
    """
    docs = ROOT / "docs"
    if not docs.exists():
        return result(False, ["docs/ does not exist. Run: make render"])
    stale, missing = [], []
    for src in correct_render_set():
        if not src.endswith(".qmd"):
            continue
        out = docs / (src[:-4] + ".html")
        if not out.exists():
            missing.append(src)
            continue
        if (ROOT / src).stat().st_mtime > out.stat().st_mtime + 1:
            stale.append(src)
    lines = [f"pages in the render set: "
             f"{sum(1 for f in correct_render_set() if f.endswith('.qmd'))}",
             f"never rendered: {len(missing)}",
             f"rendered before their source last changed: {len(stale)}"]
    lines += ["    " + s_ for s_ in (missing + stale)[:12]]
    if not missing and not stale:
        lines.append("Every page in docs/ was rendered after its source last changed.")
    return result(not missing and not stale, lines)


def d6_docs_data_tracked():
    """Every dataset must be committed under docs/data or the live site 404s."""
    code, out, err = sh("git ls-tree -r --name-only HEAD docs/data")
    tracked = [l for l in out.splitlines() if l.strip()]
    data_files = sorted(p.name for p in (ROOT / "data").iterdir() if p.is_file())
    tracked_names = sorted(Path(t).name for t in tracked)
    missing = sorted(set(data_files) - set(tracked_names))
    lines = [
        f"files tracked at HEAD under docs/data: {len(tracked)}",
        f"files in data/: {len(data_files)}",
    ]
    if missing:
        lines.append(f"not tracked, so they will 404 on the live site: {len(missing)}")
        lines += ["    " + m for m in missing[:10]]
    else:
        lines.append("Every dataset is committed under docs/data.")
    return result(not missing and bool(tracked), lines)


def d9_push_hooks():
    """No local git hook may refuse to run for want of a binary that is absent."""
    code, out, _ = sh("git config --get core.hookspath")
    hookdir = ROOT / (out.strip() or ".git/hooks")
    if not hookdir.exists():
        return result(True, [f"no hook directory at {hookdir}"])
    active = [h for h in sorted(hookdir.iterdir())
              if h.is_file() and not h.name.endswith(".sample")]
    lines = [f"active hooks in {hookdir.relative_to(ROOT) if ROOT in hookdir.parents or hookdir.parent == ROOT else hookdir}: "
             f"{len(active)}"]
    bad = []
    for h in active:
        try:
            text = h.read_text(errors="replace")
        except OSError:
            continue
        for binary in ("git-lfs",):
            if binary in text:
                present = subprocess.run(["bash", "-lc", f"command -v {binary}"],
                                         capture_output=True, text=True).returncode == 0
                lines.append(f"  {h.name}: needs {binary}, on PATH: {present}")
                if not present:
                    bad.append(h.name)
    if not active:
        lines.append("No hook can interfere with a commit or a push.")
    elif not bad:
        lines.append("Every active hook can run.")
    else:
        lines.append(f"These exit non-zero and would block the operation: {bad}")
    return result(not bad, lines)


def d8_live_site():
    """The published site must be the 2026 build and must serve data/."""
    import urllib.request
    import urllib.error
    base = "https://eds-217-essential-python.github.io"
    targets = [
        (f"{base}/", "Summer 2026"),
        (f"{base}/data/toolik_weather.csv", None),
        (f"{base}/course-materials/interactive-sessions/1a_positron_notebooks.html", None),
    ]
    lines, ok = [], True
    for url, needle in targets:
        try:
            with urllib.request.urlopen(url, timeout=25) as r:
                body = r.read(200000).decode("utf-8", "replace")
                status = r.status
        except urllib.error.HTTPError as e:
            status, body = e.code, ""
        except Exception as e:
            raise CannotRun(f"no network access from here: {e}")
        good = status == 200 and (needle is None or needle in body)
        ok = ok and good
        detail = f"  {status}  {url}"
        if needle:
            detail += f"   contains '{needle}': {needle in body}"
        lines.append(detail)
    return result(ok, lines)


# ---------------------------------------------------------------- C checks

def c1_day89_specified():
    """Days 8 and 9 must say enough to be taught and handed in."""
    d8 = (ROOT / "course-materials/day8.qmd").read_text()
    d9 = (ROOT / "course-materials/day9.qmd").read_text()
    fp = (ROOT / "course-materials/final_project.qmd").read_text()
    joined = d8 + d9 + fp

    want = {
        "a timed schedule on Day 8": bool(re.search(r"10:00 to 11:30", d8)),
        "a timed schedule on Day 9": bool(re.search(r"10:00 to 11:45", d9)),
        "checkpoints on Day 8": d8.count("Checkpoint") >= 3,
        "a submission mechanism": "own repository" in joined,
        "a deadline": bool(re.search(r"due .{0,60}(before lunch|[0-9]{1,2}:[0-9]{2})", joined)),
        "presentation length": bool(re.search(r"[Tt]welve minutes", joined)),
        "what to present": "walkthrough" in joined or "0 to 2" in d9,
        "a definition of finished": "What \"done\" looks like" in fp,
        "the ten steps enumerated": fp.count("Visualize Data") >= 1,
        "no empty trailing heading": not any(
            [l for l in x.splitlines() if l.strip()][-1].lstrip().startswith("#")
            for x in (d8, d9, fp)),
    }
    lines = [f"  {'yes' if ok else 'NO '}  {name}" for name, ok in want.items()]
    missing = [n for n, ok in want.items() if not ok]
    lines.insert(0, f"Days 8 and 9 carry {len(want) - len(missing)} of {len(want)} "
                    f"things a student or an instructor needs.")
    if missing:
        lines.append(f"still missing: {', '.join(missing)}")
    return result(not missing, lines)


# House style has a mechanical half and a judgement half, and mixing them
# produces a checker nobody reads. Only rules that cannot reasonably fire on
# correct prose belong in HARD. "land" is here as a verb only: "land use" and
# "land-hungry" are the noun and are fine, while "makes the argument land" is not.
HARD_RULES = [
    ("em-dash", re.compile("\u2014")),
    ("metaphorical 'land'", re.compile(
        r"\b(?:to|will|would|should|does|do|did|can|could|may|might|must|really|"
        r"never|always|truly)\s+land\b|\bland(?:ed|ing)\s+(?:well|badly|flat|hard)\b",
        re.I)),
    ("metaphorical 'hinge'", re.compile(r"\bhinges?\b|\bhinging\b", re.I)),
    ("'X with a hint of Y'", re.compile(r"with a (?:hint|touch|dash) of", re.I)),
    # A clause that announces an explanation instead of giving one.
    ("promise instead of tell", re.compile(
        r"and here (?:is|are|'s) why"
        r"|for (?:a|the) reason (?:you|we)(?:'ll| will) see"
        r"|as (?:you|we)(?:'ll| will) see\b"
        r"|(?:you|we)(?:'ll| will) see why"
        r"|more on (?:this|that) (?:below|later|shortly)"
        r"|(?:we|you)(?:'ll| will) come back to (?:this|that)"
        r"|for reasons? (?:that )?(?:will become|becomes) clear", re.I)),
]

# Advisory only. The "not X, it is Y" shape is glib when it is a rhetorical
# flourish and perfectly clear when it is a plain correction, and no regex can
# tell those apart. Counted and listed for the voice pass, never failed on.
ADVISORY_RULES = [
    # "since" is first a temporal word, so a causal use costs the reader a
    # restart. Advisory because the temporal use is correct and common.
    ("causal 'since', where 'because' is meant", re.compile(
        r"\bsince\s+(?!then\b|yesterday\b|last\b|\d{4}\b|Day \d|Monday|Tuesday|"
        r"Wednesday|Thursday|Friday|Saturday|Sunday|January|February|March|April|"
        r"May|June|July|August|September|October|November|December)", re.I)),
    ("'not X, it is Y' shape", re.compile(
        r"(is|are|was|were)\s+not\s+[^.;:]{3,60}[.,]\s*(it|they|that)\s+(is|are|was|were)\b",
        re.I)),
]


def _style_scan(rules):
    hits = []
    for f in live_qmd():
        text = (ROOT / f).read_text(errors="replace")
        for i, line in enumerate(text.splitlines(), 1):
            for name, rx in rules:
                if rx.search(line):
                    hits.append((str(f), i, name, line.strip()[:88]))
    return hits


def c10_house_style():
    """The mechanical half of house style, across every page a student can reach."""
    hard = _style_scan(HARD_RULES)
    advisory = _style_scan(ADVISORY_RULES)
    pages = live_qmd()

    lines = [f"pages scanned: {len(pages)}"]
    if hard:
        lines.append(f"HARD violations: {len(hard)} across "
                     f"{len({h[0] for h in hard})} page(s)")
        for f, i, name, text in hard[:20]:
            lines.append(f"    {f}:{i}  [{name}]  {text}")
        if len(hard) > 20:
            lines.append(f"    ... and {len(hard) - 20} more")
    else:
        lines.append("HARD violations: none. No em-dash, no metaphorical land or "
                     "hinge, no 'with a hint of' on any live page.")

    lines.append(f"advisory, for the voice pass to judge: {len(advisory)} line(s) "
                 f"across {len({h[0] for h in advisory})} page(s) use the "
                 f"'not X, it is Y' shape. Some of those are plain corrections and "
                 f"are fine. No regex can tell which, so this never fails the check.")

    # The mechanical rules are the smaller half. Without the ledger below, this
    # check reported PASS while two pages out of eighty-nine had been read, which
    # is worse than no check at all: it says the work is done.
    ledger = ROOT / "tasks/2026-planning/prelaunch/voice-pass.json"
    signed = 0
    total = len(pages)
    if ledger.exists():
        import json
        data = json.loads(ledger.read_text())
        entries = data.get("pages", data)
        signed = sum(1 for e in entries.values()
                     if isinstance(e, dict) and e.get("status") in ("signed_off", "skipped"))
        total = len(entries)
    lines.append(f"pages signed off: {signed} of {total}")
    if signed < total:
        lines.append(f"    {total - signed} page(s) have not been read. The mechanical "
                     f"rules above are clean, which is not the same as the pass being done.")

    return result(bool(not hard and signed >= total), lines)


def c2_mailto():
    """Both contact links on the front page must work."""
    text = (ROOT / "index.qmd").read_text()
    lines, ok = [], True
    doubled = [(i + 1, l.strip()) for i, l in enumerate(text.splitlines()) if "mailto::" in l]
    for ln, s in doubled:
        ok = False
        lines.append(f"  line {ln}: doubled colon, link does not work: {s}")
    for m in re.finditer(r"\[([^\]]*@[^\]]*)\]\(mailto:+([^)]+)\)", text):
        shown, target = m.group(1).strip(), m.group(2).strip()
        if shown != target:
            ok = False
            lines.append(f"  displayed '{shown}' does not match link target '{target}'")
    if ok:
        lines.append("Every mailto link on index.qmd is well formed and matches its label.")
    return result(ok, lines)


IMG_REF = re.compile(r"!\[[^\]]*\]\((images/[^)\s]+)\)")


def c3_images_present():
    """Every image the front page names has to exist on disk.

    A missing headshot renders as a broken image on the landing page, which is
    the first thing a student sees. The teaching team block is the case that
    prompted this: a photo referenced before the file was saved.
    """
    text = (ROOT / "index.qmd").read_text()
    lines, ok = [], True
    for m in IMG_REF.finditer(text):
        rel = m.group(1)
        if not (ROOT / rel).exists():
            ok = False
            lines.append(f"  {rel} is referenced by index.qmd but not on disk")
    if ok:
        lines.append("Every image index.qmd references exists.")
    return result(ok, lines)


NET_CALL = re.compile(r"(import\s+requests|requests\.(get|post)|urlopen|urlretrieve|urllib\.request)")


def c4_no_network_at_render():
    """No executing block may reach the network during a render."""
    hits = []
    for f in live_qmd():
        for body in executing_python_blocks(ROOT / f):
            m = NET_CALL.search(body)
            if m:
                hits.append((str(f), m.group(0)))
    lines = [f"executing python blocks scanned across {len(live_qmd())} live pages"]
    for f, what in hits:
        lines.append(f"  {f}: executes {what} at render time")
    if not hits:
        lines.append("No executing block reaches the network.")
    return result(not hits, lines)


def c9_no_external_images():
    """No page a student opens should fetch an image from another host."""
    rx = re.compile(r'!\[[^\]]*\]\((https?://[^)]+)\)|<img[^>]+src="(https?://[^"]+)"')
    hits = []
    for f in live_qmd():
        for m in rx.finditer((ROOT / f).read_text(errors="replace")):
            hits.append((str(f), m.group(1) or m.group(2)))
    lines = [f"live pages scanned: {len(live_qmd())}"]
    for f, url in hits:
        lines.append(f"  {f}: {url}")
    if not hits:
        lines.append("Every image on a live page is served from the course site.")
    return result(not hits, lines)


def c6_positron_screenshots():
    """Session 1a must show the two Positron screenshots."""
    page = ROOT / "course-materials/interactive-sessions/1a_positron_notebooks.qmd"
    text = page.read_text()
    imgs = ["positron_launch.png", "interface-positron.png"]
    lines, ok = [], True
    for name in imgs:
        f = page.parent / "images" / name
        exists = f.exists()
        commented = bool(re.search(r"<!--[^>]*" + re.escape(name), text))
        referenced = bool(re.search(r"!\[[^\]]*\]\(images/" + re.escape(name), text))
        lines.append(f"  {name}: file exists {exists}, referenced {referenced}, "
                     f"still commented out {commented}")
        if not (exists and referenced and not commented):
            ok = False
    return result(ok, lines)


def c7_eod_dates():
    """Every end-of-day page must carry its own date."""
    lines, ok = [], True
    for d in range(1, 8):
        f = ROOT / f"course-materials/eod-practice/eod-day{d}-2026.qmd"
        if not f.exists():
            lines.append(f"  day {d}: {f.name} is missing")
            ok = False
            continue
        text = f.read_text()
        want = DAY_DATES[d]
        m = re.search(r"Date:\s*([0-9/]{8,10})", text)
        if not m:
            lines.append(f"  day {d}: no Date line")
            ok = False
        elif m.group(1) != want:
            lines.append(f"  day {d}: Date reads {m.group(1)}, expected {want}")
            ok = False
        else:
            lines.append(f"  day {d}: Date {m.group(1)}")
    return result(ok, lines)


def c8_empty_headings():
    """No day page may end on a heading with nothing under it."""
    lines, ok = [], True
    for d in range(1, 10):
        f = ROOT / f"course-materials/day{d}.qmd"
        if not f.exists():
            continue
        body = [l for l in f.read_text().splitlines() if l.strip()]
        if body and body[-1].lstrip().startswith("#"):
            lines.append(f"  day{d}.qmd ends on an empty heading: {body[-1].strip()}")
            ok = False
    if ok:
        lines.append("No day page ends on an empty heading.")
    return result(ok, lines)


# ---------------------------------------------------------------- T checks

def t1_warm_cache_coverage():
    """warm_cache.py must cover every dataset the course actually loads."""
    wanted = loaded_datasets()
    code, out, err = sh(f"{sys.executable} tools/warm_cache.py")
    seen = {n for n in wanted if n in out}
    uncovered = sorted(wanted - seen)
    lines = [
        f"datasets the live corpus loads: {len(wanted)}",
        f"datasets warm_cache.py reports on: {len(seen)}",
        f"warm_cache.py exit status: {code}",
    ]
    if uncovered:
        lines.append("outside the gate, so their loss would not be detected:")
        lines += ["    " + u for u in uncovered]
    ok = code == 0 and not uncovered
    return result(ok, lines)


def t6_cells_clean():
    """Every code cell on a page students can reach must run."""
    files = [f for f in correct_render_set() if f.endswith(".qmd")]
    code, out, err = sh(f"{sys.executable} tools/run_cells.py " +
                        " ".join(f"'{f}'" for f in files))
    tail = [l for l in out.splitlines() if "ran clean across" in l]
    fails = [l for l in out.splitlines() if "FAILED" in l]
    lines = [f"pages in the render set: {len(files)}"]
    lines += tail
    if fails:
        lines.append(f"{len(fails)} failing cell(s):")
        lines += ["    " + f.strip() for f in fails[:15]]
    return result(code == 0 and not fails, lines)


def t7_make_targets_use_the_env():
    """Every make target that runs python must run it inside eds217_2026."""
    mk = (ROOT / "Makefile").read_text()
    bare, invoking, continued = [], 0, False
    for line in mk.splitlines():
        is_recipe = line.startswith("\t")
        # A recipe line ending in a backslash continues into the next one, and
        # the continuation is not a separate invocation.
        if is_recipe and not continued and "python" in line:
            invoking += 1
            if "$(RUN)" not in line and not line.strip().startswith("#"):
                bare.append(line.strip())
        continued = is_recipe and line.rstrip().endswith("\\")
    wrapper = (ROOT / "tools/run.sh")
    lines = [f"tools/run.sh present: {wrapper.exists()}",
             f"recipe lines invoking python: {invoking}",
             f"of those, not routed through the wrapper: {len(bare)}"]
    lines += ["    " + b for b in bare[:8]]
    if wrapper.exists() and not bare:
        lines.append("Every python target activates the course environment first.")
    return result(wrapper.exists() and not bare, lines)


def t3_fetch_check_exit():
    """fetch_data.py --check must fail when a dataset is absent."""
    src = (ROOT / "tools/fetch_data.py").read_text()
    tree = ast.parse(src)
    returns = [n for n in ast.walk(tree)
               if isinstance(n, ast.Return) and n.value is not None]
    exprs = [ast.unparse(n.value) for n in returns]
    exit_exprs = [e for e in exprs if "failed" in e or "absent" in e or "missing" in e]
    ok = any("missing" in e for e in exit_exprs)
    lines = [f"exit-status expressions in fetch_data.py: {exit_exprs or 'none found'}"]
    lines.append("The missing-dataset list is consulted." if ok else
                 "The missing-dataset list is never consulted, so --check cannot fail.")
    return result(ok, lines)


def t4_run_cells_empty():
    """run_cells.py must not report success when it checked nothing."""
    code, out, err = sh(f"{sys.executable} tools/run_cells.py")
    lines = [f"exit status with no file arguments: {code}",
             f"stdout: {out.strip()[:200] or '(empty)'}"]
    ok = code != 0
    lines.append("Reports a problem rather than a green result." if ok else
                 "Exits 0 having checked nothing, so an empty glob reports a passing gate.")
    return result(ok, lines)


def t5_dataset_catalog():
    """Every dataset a live page loads must have a provenance record."""
    urls_src = (ROOT / "data/data_urls.py").read_text()
    fetch_src = (ROOT / "tools/fetch_data.py").read_text()
    wanted = loaded_datasets()
    missing_urls = sorted(n for n in wanted if n not in urls_src)
    missing_fetch = sorted(n for n in wanted if n not in fetch_src)
    lines = [f"datasets loaded by live pages: {len(wanted)}"]
    if missing_urls:
        lines.append(f"absent from data/data_urls.py: {missing_urls}")
    if missing_fetch:
        lines.append(f"absent from tools/fetch_data.py: {missing_fetch}")
    if not missing_urls and not missing_fetch:
        lines.append("Every loaded dataset is catalogued in both places.")
    return result(not missing_urls and not missing_fetch, lines)


# ---------------------------------------------------------------- A checks

def a1_day45_headers():
    """Day 4 and Day 5 need their own header images."""
    want = {
        4: "microplastics_panda.jpeg",
        5: "airquality_panda.jpeg",
    }
    lines, ok = [], True
    for d, name in want.items():
        page = ROOT / f"course-materials/eod-practice/eod-day{d}-2026.qmd"
        img = ROOT / "course-materials/eod-practice/images" / name
        text = page.read_text() if page.exists() else ""
        referenced = name in text
        lines.append(f"  day {d}: {name} exists {img.exists()}, referenced {referenced}")
        if not (img.exists() and referenced):
            ok = False
    if ok:
        lines.append("Both end-of-day headers are bespoke.")
    return result(ok, lines)


# ---------------------------------------------------------------- H checks

def _referenced_names():
    refs = set()
    for f in source_files((".qmd", ".ipynb")) + [Path("_quarto.yml"), Path("index.qmd")]:
        p = ROOT / f
        if not p.exists():
            continue
        text = p.read_text(errors="replace")
        refs.update(re.findall(r"[A-Za-z0-9_.\- ]+\.(?:png|jpe?g|webp|svg|gif|tiff)", text))
    for f in ROOT.rglob("*.scss"):
        refs.update(re.findall(r"[A-Za-z0-9_.\- ]+\.(?:png|jpe?g|webp|svg|gif|tiff)",
                               f.read_text(errors="replace")))
    return {r.strip() for r in refs}


def a4_day89_headers():
    """The last two day pages should not open with the same picture."""
    import re as _re
    imgs = {}
    for d in (8, 9):
        text = (ROOT / f"course-materials/day{d}.qmd").read_text()
        m = _re.search(r"!\[[^\]]*\]\(([^)]+)\)", text)
        imgs[d] = m.group(1) if m else None
    lines = [f"  day {d}: {v}" for d, v in imgs.items()]
    same = imgs[8] == imgs[9]
    lines.append("Day 8 and Day 9 share a header image." if same
                 else "The two day pages use different images.")
    return result(not same, lines)


def h1_orphan_assets():
    """No large image or render leftover should be tracked but unused."""
    refs = _referenced_names()
    big = []
    for p in ROOT.rglob("*"):
        if not p.is_file() or skipped(p.relative_to(ROOT)):
            continue
        if p.suffix.lower() not in {".png", ".jpg", ".jpeg", ".webp", ".svg", ".gif", ".tiff"}:
            continue
        if p.name in refs:
            continue
        size = p.stat().st_size
        if size > 500_000:
            big.append((size, str(p.relative_to(ROOT))))
    leftovers = []
    for pat in ("sample_plot.*", "monthly_means.*", "*.qmd.copy"):
        for p in (ROOT / "course-materials").rglob(pat):
            leftovers.append(str(p.relative_to(ROOT)))
    big.sort(reverse=True)
    lines = [f"unreferenced images over 500 KB: {len(big)}",
             f"render leftovers under course-materials: {len(leftovers)}"]
    lines += [f"    {s/1e6:.1f} MB  {n}" for s, n in big[:10]]
    lines += ["    " + n for n in sorted(leftovers)[:10]]
    ok = not big and not leftovers
    return result(ok, lines)


def h4_stale_checklist_item():
    """The plan must not carry an open item for work already done."""
    plan = ROOT / "tasks/2026-planning/endgame-plan.md"
    text = plan.read_text()
    open_items = re.findall(r"^- \[ \] \*\*(.+?)\*\*", text, re.M)
    stale = [t for t in open_items if "2c colab" in t]
    lines = [f"open items in the endgame plan: {len(open_items)}"]
    for s in stale:
        lines.append(f"  still open but already done: {s}")
    if not stale:
        lines.append("No open item duplicates completed work.")
    return result(not stale, lines)


def h5_locks_clear():
    """Stale git locks stop the next commit."""
    gitdir = ROOT / ".git"
    locks = [str(p.relative_to(ROOT)) for p in gitdir.rglob("*.lock")]
    lines = [f"lock files under .git: {len(locks)}"] + ["    " + l for l in locks[:10]]
    if not locks:
        lines.append("No stale lock file.")
    return result(not locks, lines)


# ---------------------------------------------------------------- dispatch

CHECKS = {name: fn for name, fn in sorted(globals().items())
          if callable(fn) and re.match(r"^[a-z]\d+_", name)}


def main(argv):
    if len(argv) == 2 and argv[1] == "--render-set":
        for f in correct_render_set():
            print(f)
        return 0
    if len(argv) != 2 or argv[1] in ("-h", "--help"):
        print("usage: python tools/prelaunch_checks.py <check-name>")
        print("\navailable checks:")
        for name, fn in CHECKS.items():
            doc = (fn.__doc__ or "").strip().splitlines()[0] if fn.__doc__ else ""
            print(f"  {name:32s} {doc}")
        return 0
    name = argv[1]
    if name not in CHECKS:
        print(f"no such check: {name}")
        return 2
    try:
        ok, lines = CHECKS[name]()
    except CannotRun as e:
        print(f"COULD NOT RUN  {name}")
        print(f"  {e}")
        return 2
    except Exception as e:
        print(f"COULD NOT RUN  {name}")
        print(f"  {type(e).__name__}: {e}")
        return 2
    print(("PASS  " if ok else "FAIL  ") + name)
    for l in lines:
        print(l if l.startswith(" ") else "  " + l)
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
