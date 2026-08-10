#!/usr/bin/env python3
"""
Execute every ```{python} cell in the given .qmd files and report failures.

A fast pre-render check: catches broken code without waiting on a full Quarto
build, and runs offline because the cache shim resolves course-site data URLs
to the repo's data/ directory.

    python tools/run_cells.py course-materials/**/2*.qmd
"""
import re, sys, io, traceback, contextlib, pathlib

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
import eds217_offline_cache as cache
cache.install()

total = failed_total = 0
for f in sys.argv[1:]:
    src = pathlib.Path(f).read_text()
    blocks = re.findall(r"```\{python\}\n(.*?)```", src, re.S)
    ns, fails = {}, 0
    for i, b in enumerate(blocks, 1):
        try:
            with contextlib.redirect_stdout(io.StringIO()):
                exec(compile(b, f"<cell {i}>", "exec"), ns)
        except Exception:
            fails += 1
            print(f"  {f} CELL {i} FAILED")
            print(f"    {b.strip().splitlines()[0][:100]}")
            print(f"    {traceback.format_exc().strip().splitlines()[-1]}")
    total += len(blocks); failed_total += fails
    print(f"{len(blocks)-fails:>3}/{len(blocks):<3} cells clean   {f}")
print(f"\n{total-failed_total}/{total} cells ran clean across {len(sys.argv)-1} files")
sys.exit(1 if failed_total else 0)
