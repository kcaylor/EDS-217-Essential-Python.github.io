# OpenAQ CSV Reconciliation Report

**Date:** 2026-07-20
**Prepared for:** Task 1 keep/revert decision (M1 housekeeping)
**Files:** `data/openaq_CNSI_measurments.csv`, `data/openaq_goleta_measurments.csv`, `data/openaq_santa_barbara_measurments.csv`

---

## Headline finding — the premise is wrong: there are **no appended 2025 rows**

The task described these files as having "~4,900 uncommitted appended rows from the 2025
class." That is not what git is actually flagging. Investigation shows:

- **HEAD stores each file as a 3-line Git LFS pointer**, not CSV content. They were committed
  as LFS objects in `e793e34` ("Added large files using Git LFS").
- **The working tree holds the full, materialized CSV content** (the smudged LFS object).
- **There is no active `.gitattributes` LFS rule** for these paths. So git compares the
  committed *pointer text* against the *full-content* working file and reports the whole file
  as changed (`3 deletions`, all-rows `insertions`). That is the entire source of the `M` flag.
- **The working-tree content is byte-for-byte identical to the original LFS object** for all
  three files (verified by smudging `HEAD:` through `git lfs smudge` and `diff`-ing —
  0 differences, identical byte counts):

  | File | HEAD (LFS pointer) | Working tree | LFS-object bytes | WT bytes | Content diff |
  |---|---|---|---|---|---|
  | CNSI | pointer, oid `97c66dc…`, size 119251 | full CSV | 119,251 | 119,251 | **identical** |
  | goleta | pointer, size 371976 | full CSV | 371,976 | 371,976 | **identical** |
  | santa_barbara | pointer, size 445766 | full CSV | 445,766 | 445,766 | **identical** |

**Conclusion:** No rows were added, removed, or edited by anyone. The ~4,900 rows are the
*entire* contents of the three files (714 + 1,962 + 2,266 = 4,942 rows incl. headers → 4,939
data rows), not a 2025-class delta. There is nothing to "reconcile" in the data sense. The
only real question is a **storage-format** one: do we keep these as regular in-repo CSVs, or
restore them to LFS pointers?

---

## Per-file inventory (working-tree = LFS-original content)

Row counts are data rows (excluding header). All three share the identical 15-column header:

```
location_id,location_name,parameter,value,unit,datetimeUtc,datetimeLocal,
timezone,latitude,longitude,country_iso,isMobile,isMonitor,owner_name,provider
```

### CNSI — `data/openaq_CNSI_measurments.csv`
- **Rows:** HEAD = LFS pointer (no rows); working tree = **714** data rows
- **Schema:** 15 columns, **0 nonconforming rows**; header matches the other two files
- **Location:** `CNSI Roof Top` (single station)
- **Parameters:** `pm25` only (714)
- **Date range (datetimeUtc):** 2024-07-11T01:00 → 2024-08-12T00:00
- **Duplicates:** 0 fully-duplicated rows; 0 duplicate `(parameter, datetimeUtc)` keys
- **Gaps:** pm25 — 714 obs over a 768-hour window → **54 missing hours (93.0% coverage)**

### goleta — `data/openaq_goleta_measurments.csv`
- **Rows:** HEAD = LFS pointer; working tree = **1,962** data rows
- **Schema:** 15 columns, **0 nonconforming rows**; header matches
- **Location:** `Goleta` (single station)
- **Parameters:** `pm25` (734), `o3` (711), `pm10` (517)
- **Date range (datetimeUtc):** 2024-07-12T01:00 → 2024-08-12T00:00
- **Duplicates:** 0 fully-duplicated rows; 0 duplicate `(parameter, datetimeUtc)` keys
- **Gaps:**
  - pm25 — 734 obs / 744h → 10 missing hours (98.7%)
  - o3 — 711 obs / 744h → 33 missing hours (95.6%)
  - pm10 — 517 obs / 620h → 103 missing hours (83.4%)

### santa_barbara — `data/openaq_santa_barbara_measurments.csv`
- **Rows:** HEAD = LFS pointer; working tree = **2,266** data rows
- **Schema:** 15 columns, **0 nonconforming rows**; header matches
- **Location:** `Santa Barbara` (single station)
- **Parameters:** `pm10` (766), `pm25` (766), `o3` (734)
- **Date range (datetimeUtc):** 2024-07-11T01:00 → 2024-08-12T00:00
- **Duplicates:** 0 fully-duplicated rows; 0 duplicate `(parameter, datetimeUtc)` keys
- **Gaps:**
  - pm25 — 766 obs / 768h → 2 missing hours (99.7%)
  - pm10 — 766 obs / 768h → 2 missing hours (99.7%)
  - o3 — 734 obs / 768h → 34 missing hours (95.6%)

### Schema / duplicates / gaps summary
- **Schema:** all three files are internally consistent and mutually consistent (same 15
  columns, same order, zero malformed rows). Good for a Day 5 groupby EOD.
- **Duplicates:** none, on either a full-row or `(parameter, datetimeUtc)` basis.
- **Gaps:** all series are nominally hourly with modest missingness (mostly 93–99.7%
  coverage; goleta pm10 is the weakest at 83.4%). This is *real* sensor downtime, not a
  data error — and it is pedagogically useful (`.isnull()`, coverage counts, per-group
  completeness are natural D5 questions). No gap-filling needed for the EOD.
- **Note on `datetimeUtc`:** all timestamps sit in a **July–August 2024** window, consistent
  with data pulled for the 2024/2025 course cycle. Nothing here is 2026 data.

---

## The actual decision: keep as in-repo CSV, or revert to LFS pointer

Because working-tree content == LFS object content, **no data is lost either way.**

- **KEEP** (`git add` the three files, commit): promotes them from LFS pointers to ordinary
  in-repo CSV blobs. Total ~0.9 MB across the three files — well within normal git limits, no
  LFS needed. Upside: anyone cloning gets the CSVs without `git lfs pull` / an LFS-enabled
  checkout; the D5 OpenAQ EOD can rely on them being present locally. This effectively
  de-LFS-es these three files. (There's no `.gitattributes` rule to remove — there isn't one.)
- **REVERT** (`git checkout -- data/openaq_*.csv`): restores the 3-line LFS pointers. Working
  tree goes back to matching HEAD; the full content remains available via LFS. Keeps the
  storage design as-is. Downside: contributors/students need LFS configured to get real data,
  and the D5 EOD build must account for that.

**Recommendation:** **KEEP.** These are small (~0.9 MB total), static teaching CSVs that the
2026 Day 5 EOD is being designed around (per the day skeleton, decision #2). Plain in-repo
CSVs remove an LFS dependency for a core dataset with no real cost, and content is provably
identical to what LFS holds. If you'd rather preserve the LFS design, revert is clean and
lossless too.

**No commit has been made.** Awaiting your keep/revert decision before proceeding.

---

### Appendix — how this was verified
- `git show HEAD:<file>` → confirms 3-line LFS pointer at HEAD.
- `git show HEAD:<file> | git lfs smudge` → materializes the original LFS object; byte count
  and `diff` against the working tree show **identical** content for all three files.
- `git diff --stat` → the reported "715 insertions, 3 deletions" is pointer-vs-content, not a
  row-level delta.
- Content stats (rows, parameters, date range, duplicates, hourly gaps) computed directly
  from the working-tree CSVs with Python `csv`.
