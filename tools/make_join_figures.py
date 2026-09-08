import pathlib
OUT = pathlib.Path(__file__).resolve().parent.parent / "course-materials" / "images" / "join_types_keyaxis.svg"

# ---------------------------------------------------------------- config
W, H   = 1112, 792
N      = 20            # slots on the shared key axis
RH     = 15            # height of one row
BW, VW = 26, 34        # blue (key) column width, value column width
CW     = BW + VW + VW  # 76

TITLE_FONT = "'Bradley Hand', 'Comic Sans MS', 'Segoe Print', ui-sans-serif, system-ui, sans-serif"
SANS       = "ui-sans-serif, system-ui, -apple-system, 'Helvetica Neue', Arial, sans-serif"

BLUE, GREEN, ORANGE = "#3F9BF2", "#67CC3F", "#F3A72C"
L = dict(ink="#111111", frame="#111111", nanf="#e9ecf0", nans="#9aa3ae", muted="#555555")
D = dict(ink="#e8eaed", frame="#8b93a1", nanf="#232a35", nans="#7b8494", muted="#a5adba")

# df1 / df2 coverage on the key axis, as inclusive runs of slots
DF1 = [(0,3),(5,6),(8,11),(14,16),(18,19)]
DF2 = [(0,2),(4,5),(8,10),(12,15),(18,19)]

def keys(runs):
    s = set()
    for a,b in runs: s |= set(range(a,b+1))
    return s

d1, d2 = keys(DF1), keys(DF2)
PANELS = [
    ("Inner", ["(where", "both", "occur)"],  d1 & d2),
    ("Outer", ["(where", "either", "occur)"], d1 | d2),
    ("Left",  ["(where", "left", "occurs)"],  set(d1)),
    ("Right", ["(where", "right", "occurs)"], set(d2)),
]

out = []
def add(s): out.append(s)

def segments(K, state):
    """Maximal runs of consecutive slots in K sharing the same state."""
    segs, cur = [], None
    for i in range(N):
        if i not in K:
            if cur: segs.append(cur); cur = None
            continue
        st = state(i)
        if cur and cur[1] == i-1 and cur[2] == st:
            cur = (cur[0], i, st)
        else:
            if cur: segs.append(cur)
            cur = (i, i, st)
    if cur: segs.append(cur)
    return segs

def column(x, y0, K, state, color):
    """state(i) -> True (value present) or False (NaN)."""
    for a, b, st in segments(K, state):
        y = y0 + a*RH
        h = (b-a+1)*RH
        w = BW if color is None else VW
        if st:
            add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{color or BLUE}"/>')
        else:
            add(f'<rect x="{x+1.25}" y="{y+1.25}" width="{w-2.5}" height="{h-2.5}" rx="2" '
                f'fill="{L["nanf"]}" stroke="{L["nans"]}" stroke-width="1.6" '
                f'class="c-nanf s-nans"/>')

def result_block(x, y0, K):
    column(x,          y0, K, lambda i: True,    None)
    column(x+BW,       y0, K, lambda i: i in d1, GREEN)
    column(x+BW+VW,    y0, K, lambda i: i in d2, ORANGE)

def source_block(x, y0, own, color):
    column(x,    y0, own, lambda i: True, None)
    column(x+BW, y0, own, lambda i: True, color)

# ---------------------------------------------------------------- canvas
AXIS_H = N*RH
add(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {W} {H}" width="{W}" height="{H}" role="img" '
    f'aria-label="Four pandas join types drawn on a shared key axis. Blue marks the rows a table has, '
    f'green a value from df1, orange a value from df2. Grey outlined boxes mark NaN, where a row exists '
    f'but the other table had no matching key.">')
add(f'''<style>
@media (prefers-color-scheme: dark) {{
  .c-ink{{fill:{D["ink"]}}} .c-muted{{fill:{D["muted"]}}} .c-nanf{{fill:{D["nanf"]}}}
  .s-nans{{stroke:{D["nans"]}}} .s-frame{{stroke:{D["frame"]}}}
}}
</style>''')

# ---------------------------------------------------------------- panels
PW, PH, PGAP = 380, AXIS_H + 40, 22
PX0, PY0 = 300, 30
for idx, (title, desc, K) in enumerate(PANELS):
    px = PX0 + (idx % 2) * (PW + PGAP)
    py = PY0 + (idx // 2) * (PH + PGAP)
    add(f'<rect x="{px}" y="{py}" width="{PW}" height="{PH}" fill="none" '
        f'stroke="{L["frame"]}" stroke-width="3.5" class="s-frame"/>')
    add(f'<text x="{px+22}" y="{py+52}" font-family="{TITLE_FONT}" font-size="30" '
        f'font-weight="700" fill="{L["ink"]}" class="c-ink">{title}</text>')
    for j, line in enumerate(desc):
        add(f'<text x="{px+30}" y="{py+112+j*26}" font-family="{SANS}" font-size="20" '
            f'fill="{L["ink"]}" class="c-ink">{line}</text>')
    result_block(px + PW - 34 - CW, py + 20, K)

# ---------------------------------------------------------------- sources
SY = PY0 + (2*PH + PGAP - AXIS_H)/2
for x, runs, color, lab in ((60, DF1, GREEN, "df1"), (178, DF2, ORANGE, "df2")):
    source_block(x, SY, keys(runs), color)
    add(f'<text x="{x}" y="{SY+AXIS_H+34}" font-family="{SANS}" font-size="26" '
        f'fill="{L["ink"]}" class="c-ink">{lab}</text>')

# ---------------------------------------------------------------- legend
ly = H - 26
items = [(BLUE, "row exists at this key"), (GREEN, "value from df1"),
         (ORANGE, "value from df2"), (None, "NaN (no matching key)")]
lx = 60
for color, label in items:
    if color:
        add(f'<rect x="{lx}" y="{ly-11}" width="16" height="14" fill="{color}"/>')
    else:
        add(f'<rect x="{lx+0.8}" y="{ly-10.2}" width="14.4" height="12.4" rx="2" fill="{L["nanf"]}" '
            f'stroke="{L["nans"]}" stroke-width="1.6" class="c-nanf s-nans"/>')
    add(f'<text x="{lx+24}" y="{ly}" font-family="{SANS}" font-size="15" fill="{L["muted"]}" '
        f'class="c-muted">{label}</text>')
    lx += 34 + len(label)*8.1

add('</svg>')
open(OUT, "w").write("\n".join(out))

# sanity report
def runs_str(K):
    r, cur = [], None
    for i in range(N):
        if i in K:
            cur = (cur[0], i) if cur and cur[1] == i-1 else (i, i)
            if cur[0] == i: r.append(cur)
            else: r[-1] = cur
        else: cur = None
    return r
print("df1 rows:", len(d1), runs_str(d1))
print("df2 rows:", len(d2), runs_str(d2))
for t,_,K in PANELS:
    print(f"{t:6s} rows={len(K):2d}  green NaN at {sorted(K-d1)}  orange NaN at {sorted(K-d2)}  runs={runs_str(K)}")
