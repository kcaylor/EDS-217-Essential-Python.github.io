"""Generate data/messy_field_survey.csv for the EDS 217 Day 4 colab (4d).

Deterministic. Every defect below is fixable with Day 4 scope only:
  duplicates          -> .drop_duplicates()
  sentinel -999.0     -> the Day 3 filter sentence
  missing values      -> .dropna(subset=[...]) and .fillna(value)
  float-typed count   -> .fillna(1) then .astype(int)
  comma decimals      -> .str.replace(',', '.') then .astype(float)
  label chaos         -> .str.strip(), .str.lower(), .str.replace('-', '_')
  spaced column name  -> .rename(columns={...})   (taught Day 2)
"""
import pathlib
import random
from datetime import date, timedelta

random.seed(217)

DEST = pathlib.Path(__file__).resolve().parent.parent / "data" / "messy_field_survey.csv"

SITES = ["site_a", "site_b", "site_c", "site_d", "site_e", "site_f"]

# Per-site "true" character, so the cleaned data has something to say.
PROFILE = {
    "site_a": dict(temp=16.5, ph=7.4, do=9.4, cond=310),
    "site_b": dict(temp=18.2, ph=7.1, do=8.6, cond=455),
    "site_c": dict(temp=21.8, ph=6.6, do=6.9, cond=790),
    "site_d": dict(temp=15.1, ph=7.7, do=10.1, cond=265),
    "site_e": dict(temp=19.6, ph=6.9, do=7.5, cond=620),
    "site_f": dict(temp=22.9, ph=6.4, do=6.1, cond=880),
}

# How each site's label was written down in the field. Same site, six spellings.
SPELLINGS = {
    "site_a": ["SITE_A", "site_a", "Site_A", " site_a", "site_a ", "site-a"],
    "site_b": ["site_b", "SITE_B", "Site_B", "site-b", " Site_B", "site_b "],
    "site_c": ["Site_C", "site-c", "SITE_C", "site_c", "site_c ", " site-c"],
    "site_d": ["site_d", "Site_D", "SITE_D", " site_d", "site-d", "site_d "],
    "site_e": ["SITE_E", "site-e", "Site_E", "site_e ", "site_e", " SITE_E"],
    "site_f": ["site_f", "SITE_F", " site-f", "Site_F", "site_f ", "site-f"],
}

start = date(2025, 6, 2)
rows = []
for i in range(300):
    site = SITES[i % 6]
    p = PROFILE[site]
    day = start + timedelta(days=i // 6 * 2)

    temp = round(random.gauss(p["temp"], 1.4), 1)
    ph = round(random.gauss(p["ph"], 0.22), 2)
    do = round(random.gauss(p["do"], 0.7), 2)
    cond = round(random.gauss(p["cond"], 42), 1)

    rows.append({
        "site": random.choice(SPELLINGS[site]),
        "collection date": day.isoformat(),
        "temperature_c": f"{temp}",
        "pH": f"{ph}",
        "dissolved_oxygen_mg_L": f"{do}",
        "conductivity_uS_cm": f"{cond}",
        "n_replicates": str(random.choice([2, 3, 3, 3, 4])),
    })

idx = list(range(300))
random.shuffle(idx)


def take(n):
    """Pop n distinct row indices off the shuffled pool."""
    out, idx[:] = idx[:n], idx[n:]
    return out


# 1. Datalogger sentinel: the thermistor writes -999 when it fails.
for i in take(9):
    rows[i]["temperature_c"] = "-999.0"

# 2. Blanks, one block per instrument.
for i in take(18):
    rows[i]["temperature_c"] = ""
for i in take(11):
    rows[i]["dissolved_oxygen_mg_L"] = ""
for i in take(7):
    rows[i]["conductivity_uS_cm"] = ""

# 3. Replicate count left blank on a handful of sheets -> column reads as float.
for i in take(5):
    rows[i]["n_replicates"] = ""

# 4. A field notebook written with European decimal commas.
for i in take(24):
    rows[i]["pH"] = rows[i]["pH"].replace(".", ",")

# 5. Twenty sheets entered twice.
dupes = [dict(rows[i]) for i in take(20)]
rows.extend(dupes)
random.shuffle(rows)

cols = ["site", "collection date", "temperature_c", "pH",
        "dissolved_oxygen_mg_L", "conductivity_uS_cm", "n_replicates"]

import csv

with open(str(DEST), "w", newline="") as fh:
    writer = csv.DictWriter(fh, fieldnames=cols)
    writer.writeheader()
    writer.writerows(rows)

print(f"wrote {len(rows)} data rows to {DEST}")
