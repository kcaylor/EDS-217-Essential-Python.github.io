#!/usr/bin/env python3
"""
Execute every ```{python} cell in the given .qmd files and report failures.

A fast pre-render check: catches broken code without waiting on a full Quarto
build, and runs offline because the cache shim resolves course-site data URLs
to the repo's data/ directory.

    python tools/run_cells.py course-materials/**/2*.qmd
"""
import os

# Force a headless plotting backend before anything imports matplotlib.
# On macOS matplotlib defaults to the "macosx" backend, and a plt.show() in an
# answer key then tries to start a GUI event loop inside this process, which
# aborts the interpreter outright. Quarto does not hit this, because it renders
# through a Jupyter kernel using the inline backend. The crash is therefore a
# defect in this checker rather than in the page, so the backend is pinned here
# instead of being left to whoever happens to invoke the script.
os.environ["MPLBACKEND"] = "Agg"

import re, sys, io, traceback, contextlib, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import eds217_offline_cache as cache
cache.install()

files = sys.argv[1:]
if not files:
    # Exiting 0 here would let a wrapper whose glob matched nothing report a
    # passing gate. Say what is wrong instead.
    print("run_cells.py was given no files, so it checked nothing.")
    print("Usage: python tools/run_cells.py <file.qmd> [<file.qmd> ...]")
    print("For the whole 2026 corpus, use: make cells")
    sys.exit(2)

total = failed_total = 0
for f in files:
    src = pathlib.Path(f).read_text()
    blocks = re.findall(r"```\{python\}\n(.*?)```", src, re.S)
    ns, fails, skipped = {}, 0, []
    for i, b in enumerate(blocks, 1):
        # Quarto never executes a block marked `eval: false`, so neither do we.
        # These are usually shell commands or deliberately broken examples.
        if re.search(r"^#\|\s*eval:\s*false\s*$", b, re.M):
            skipped.append("eval: false")
            continue
        # IPython magics (%whos) and shell escapes (!ls, files = !ls) are valid in
        # the Jupyter kernel Quarto renders through, but not in plain exec(). We
        # cannot check these blocks, so skip them rather than report a false failure.
        if re.search(r"^\s*[%!]|=\s*!", b, re.M):
            skipped.append("IPython magic")
            continue
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(b, f"<cell {i}>", "exec"), ns)
        except Exception:
            fails += 1
            print(f"  {f} CELL {i} FAILED")
            print(f"    {b.strip().splitlines()[0][:100]}")
            print(f"    {traceback.format_exc().strip().splitlines()[-1]}")
    try:
        import matplotlib.pyplot as _plt
        _plt.close("all")
    except Exception:
        pass
    ran = len(blocks) - len(skipped)
    total += ran; failed_total += fails
    reasons = ", ".join(sorted(set(skipped)))
    note = f"   ({len(skipped)} skipped: {reasons})" if skipped else ""
    print(f"{ran-fails:>3}/{ran:<3} cells clean   {f}{note}")
print(f"\n{total-failed_total}/{total} cells ran clean across {len(files)} files")
sys.exit(1 if failed_total else 0)
