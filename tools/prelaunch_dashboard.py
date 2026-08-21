#!/usr/bin/env python3
"""
Render the EDS 217 pre-launch dashboard.

Two outputs, from one body of markup:

  render_body(payload)              page content, for publishing as an Artifact
  render_standalone(body, payload)  a full HTML document, for opening from disk

Everything is rendered here in Python. The browser only filters, expands and
copies, so a template bug shows up when the file is written rather than when
someone opens it.
"""

import html
import json

CATEGORIES = [
    ("deploy", "Deploy", "Getting the 2026 site published with working data."),
    ("content", "Content", "What a student reads, clicks and is graded against."),
    ("tooling", "Tooling", "Whether the checks can be believed."),
    ("assets", "Assets", "Images students see. None of these breaks anything."),
    ("housekeeping", "Housekeeping", "Safe to carry past the first day of class."),
]

STATE_LABEL = {
    "certified": "certified",
    "verified": "verified, awaiting sign-off",
    "in_progress": "in progress",
    "blocked": "blocked",
    "open": "open",
    "deferred": "deferred",
}

CHAIN = [
    ("Prepare the tree", ["D1", "D2", "D3", "D4", "C2", "C4"]),
    ("Render and commit", ["D5", "D6"]),
    ("Publish and verify", ["D7", "D8"]),
]

E = html.escape


def paras(text):
    if not text:
        return ""
    blocks = [" ".join(b.split()) for b in text.strip().split("\n\n") if b.strip()]
    return "".join(f"<p>{E(b)}</p>" for b in blocks)


def pill(state):
    return (f'<span class="pill pill--{state}">'
            f'<span class="dot"></span>{E(STATE_LABEL.get(state, state))}</span>')


def render_item(it):
    sev = it["severity"]
    state = it["state"]
    last = it.get("last_check")
    sign = it.get("signoff")

    verdict = ""
    if last:
        if last["ok"]:
            vclass, vtext = "good", "verification passed"
        elif last.get("could_not_run"):
            vclass, vtext = "warn", "verification could not run here"
        else:
            vclass, vtext = "bad", "verification failing"
        verdict = (f'<div class="verdict verdict--{vclass}">'
                   f'<strong>{E(vtext)}</strong>'
                   f'<span>{E(last["at"])} on {E(last["git_sha"])}</span></div>'
                   f'<pre class="evidence">{E(last["evidence"] or "(no output)")}</pre>')
    else:
        verdict = ('<div class="verdict verdict--none">'
                   '<strong>not yet verified</strong>'
                   '<span>run the command below</span></div>')

    signblock = ""
    if sign:
        forced = ' <em>recorded as forced</em>' if sign.get("forced") else ""
        signblock = (f'<div class="signoff"><h4>Signed off</h4>'
                     f'<p class="meta">{E(sign["by"])} · {E(sign["at"])} · '
                     f'{E(sign["git_sha"])}{forced}</p>'
                     f'<p>{E(sign["note"])}</p></div>')

    notes = ""
    if it.get("notes"):
        rows = "".join(f'<li><span class="mono">{E(n["at"])}</span> {E(n["text"])}</li>'
                       for n in it["notes"])
        notes = f'<div class="notes"><h4>Working notes</h4><ul>{rows}</ul></div>'

    deps = ""
    if it.get("waiting_on"):
        deps = (f'<span class="dep dep--wait">waiting on '
                f'{E(", ".join(it["waiting_on"]))}</span>')
    elif it.get("blocked_by"):
        deps = (f'<span class="dep">after {E(", ".join(it["blocked_by"]))}</span>')
    if it.get("blocks"):
        deps += f'<span class="dep">unblocks {E(", ".join(it["blocks"]))}</span>'

    v = it.get("verify", {})
    cmd = v.get("cmd", "")
    kindnote = ("This one is checked by hand." if v.get("kind") == "manual"
                else "This one is checked by command.")

    certify_cmd = f'python tools/prelaunch.py certify {it["id"]} -n "..."'

    haystack = " ".join([it["id"], it["title"], it.get("why", ""),
                         it.get("action", ""), it.get("category", ""),
                         it.get("owner", "")]).lower()

    return f'''
<article class="item item--{sev} is-{state}" id="item-{E(it["id"])}"
         data-sev="{E(sev)}" data-cat="{E(it["category"])}" data-state="{E(state)}"
         data-owner="{E(it["owner"])}" data-q="{E(haystack)}">
  <button class="item__head" aria-expanded="false" aria-controls="body-{E(it["id"])}">
    <span class="item__id mono">{E(it["id"])}</span>
    <span class="item__title">{E(it["title"])}</span>
    <span class="item__tags">
      <span class="sev sev--{E(sev)}">{E(sev)}</span>
      <span class="owner">{E(it["owner"])}</span>
      {pill(state)}
    </span>
    <span class="chev" aria-hidden="true"></span>
  </button>
  <div class="item__body" id="body-{E(it["id"])}" hidden>
    <div class="deps">{deps}</div>
    <div class="prose">
      <h4>Why it matters</h4>{paras(it.get("why"))}
      {"<h4>How we know</h4>" + paras(it.get("evidence")) if it.get("evidence") else ""}
      <h4>What to do</h4>{paras(it.get("action"))}
    </div>
    <div class="verify">
      <h4>Verification <span class="kindnote">{E(kindnote)}</span></h4>
      <div class="cmdrow">
        <code class="mono">{E(cmd)}</code>
        <button class="copy" data-copy="{E(cmd)}">copy</button>
      </div>
      <p class="expect"><span class="lbl">expect</span> {E(v.get("expect", ""))}</p>
      {verdict}
      <div class="cmdrow cmdrow--quiet">
        <code class="mono">{E(certify_cmd)}</code>
        <button class="copy" data-copy="{E(certify_cmd)}">copy</button>
      </div>
    </div>
    {signblock}
    {notes}
  </div>
</article>'''


def render_chain(items_by_id):
    cols = []
    for label, ids in CHAIN:
        chips = []
        for i in ids:
            it = items_by_id.get(i)
            if not it:
                continue
            chips.append(
                f'<a class="chip is-{it["state"]}" href="#item-{i}" '
                f'title="{E(it["title"])}"><span class="mono">{i}</span>'
                f'<span class="chip__t">{E(it["title"])}</span></a>')
        cols.append(f'<div class="chaincol"><h3>{E(label)}</h3>'
                    f'<div class="chips">{"".join(chips)}</div></div>')
    return '<div class="chain">' + '<div class="arrow" aria-hidden="true"></div>'.join(cols) + '</div>'


def render_body(payload):
    meta = payload["meta"]
    items = payload["items"]
    by_id = {i["id"]: i for i in items}

    total = len(items)
    certified = sum(1 for i in items if i["state"] == "certified")
    deferred = sum(1 for i in items if i["state"] == "deferred")
    blockers = [i for i in items if i["severity"] == "blocker"
                and i["state"] not in ("certified", "deferred")]
    verified = sum(1 for i in items if i["state"] == "verified")
    days = meta.get("days_left")

    segs = "".join(f'<span class="seg seg--{i["state"]} seg--sev-{i["severity"]}" '
                   f'title="{E(i["id"])} {E(i["title"])}"></span>' for i in items)

    counts = {}
    for i in items:
        counts[i["state"]] = counts.get(i["state"], 0) + 1
    legend = "".join(
        f'<li><span class="key key--{s}"></span>{E(STATE_LABEL.get(s, s))}'
        f'<b class="mono">{n}</b></li>'
        for s, n in sorted(counts.items(), key=lambda kv: -kv[1]))

    sections = []
    for key, label, blurb in CATEGORIES:
        group = [i for i in items if i["category"] == key]
        if not group:
            continue
        gdone = sum(1 for i in group if i["state"] in ("certified", "deferred"))
        sections.append(f'''
<section class="cat" data-cat="{E(key)}">
  <header class="cat__head">
    <h2>{E(label)}</h2>
    <p>{E(blurb)}</p>
    <span class="cat__count mono">{gdone}/{len(group)}</span>
  </header>
  {"".join(render_item(i) for i in group)}
</section>''')

    owners = sorted({i["owner"] for i in items})
    owner_chips = "".join(
        f'<button class="f" data-f="owner" data-v="{E(o)}">{E(o)}</button>'
        for o in owners)

    countdown = (f'<span class="big mono">{days}</span><span class="unit">'
                 f'day{"s" if days != 1 else ""} to first class</span>'
                 if days is not None else "")

    blockline = (f'<strong class="alarm">{len(blockers)} blocker'
                 f'{"s" if len(blockers) != 1 else ""} open</strong>'
                 if blockers else '<strong class="clear">no blockers open</strong>')

    return f'''<title>EDS 217 Launch Board</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Archivo:wght@500;600;700&family=Source+Serif+4:opsz,wght@8..60,400;8..60,600&family=JetBrains+Mono:wght@400;600&display=swap">
<style>{CSS}</style>

<div class="wrap">
  <aside class="rail">
    <div class="brand">
      <span class="eyebrow">EDS 217 · {E(str(meta.get("term", "")))}</span>
      <h1>Launch Board</h1>
      <p class="sub">Everything between today and a course site that works on the
      first morning.</p>
    </div>

    <div class="countdown">{countdown}</div>

    <div class="meter">
      <div class="segs">{segs}</div>
      <p class="meterline"><b class="mono">{certified}</b> of
      <b class="mono">{total}</b> certified{f", {deferred} deferred" if deferred else ""}.
      {blockline}.</p>
      <ul class="legend">{legend}</ul>
    </div>

    <div class="filters">
      <label class="search">
        <span class="lbl">search</span>
        <input type="search" id="q" placeholder="id, title, anything" autocomplete="off">
      </label>
      <div class="fgroup">
        <span class="lbl">severity</span>
        <div class="frow">
          <button class="f" data-f="sev" data-v="blocker">blocker</button>
          <button class="f" data-f="sev" data-v="high">high</button>
          <button class="f" data-f="sev" data-v="medium">medium</button>
          <button class="f" data-f="sev" data-v="low">low</button>
        </div>
      </div>
      <div class="fgroup">
        <span class="lbl">state</span>
        <div class="frow">
          <button class="f" data-f="state" data-v="open">open</button>
          <button class="f" data-f="state" data-v="blocked">blocked</button>
          <button class="f" data-f="state" data-v="verified">verified</button>
          <button class="f" data-f="state" data-v="certified">certified</button>
        </div>
      </div>
      <div class="fgroup">
        <span class="lbl">owner</span>
        <div class="frow">{owner_chips}</div>
      </div>
      <div class="frow frow--wide">
        <button class="f f--solo" id="onlyopen">hide what is done</button>
        <button class="f f--solo" id="clearf">clear filters</button>
      </div>
      <p class="count mono" id="count"></p>
    </div>

    <footer class="railfoot">
      <p>Generated {E(str(meta.get("generated", "")))} from
      <code>tasks/2026-planning/prelaunch/punchlist.yml</code> at
      <code>{E(str(meta.get("git_sha", "")))}</code>.</p>
      <p>Rebuild with <code>python tools/prelaunch.py dashboard</code>.</p>
    </footer>
  </aside>

  <main class="main">
    <section class="path">
      <header class="path__head">
        <h2>The critical path</h2>
        <p>Nothing on the live site changes until this chain finishes, left to
        right. Everything else can be done in any order.</p>
      </header>
      {render_chain(by_id)}
      <p class="pathnote">The site currently serves the 2025 course, and every
      2026 dataset URL returns 404. Both conditions clear at the end of this chain
      and not before.</p>
    </section>

    <div class="stats">
      <div class="stat"><span class="mono">{len(blockers)}</span><span>blockers open</span></div>
      <div class="stat"><span class="mono">{verified}</span><span>verified, awaiting sign-off</span></div>
      <div class="stat"><span class="mono">{certified}</span><span>certified</span></div>
      <div class="stat"><span class="mono">{total - certified - deferred}</span><span>still to do</span></div>
    </div>

    {"".join(sections)}

    <p class="empty" id="empty" hidden>Nothing matches those filters.</p>
  </main>
</div>

<script>{JS}</script>
'''


def render_standalone(body, payload):
    return ('<!doctype html>\n<html lang="en">\n<head>\n'
            '<meta charset="utf-8">\n'
            '<meta name="viewport" content="width=device-width, initial-scale=1">\n'
            '</head>\n<body>\n' + body + '\n</body>\n</html>\n')


CSS = r"""
*, *::before, *::after { box-sizing: border-box; }

:root {
  --ground:      #f4f6f3;
  --surface:     #ffffff;
  --surface-2:   #eef1ed;
  --line:        #d8ded8;
  --line-soft:   #e6eae5;
  --ink:         #17201c;
  --ink-2:       #3c4b44;
  --muted:       #64736b;
  --accent:      #0e6e63;
  --accent-soft: #d7e9e5;
  --crit:        #a83527;
  --crit-soft:   #f6e2df;
  --warn:        #9a6612;
  --warn-soft:   #f7ecd8;
  --good:        #2b6f4a;
  --good-soft:   #dcece1;
  --shadow:      0 1px 2px rgba(23,32,28,.06), 0 8px 24px -18px rgba(23,32,28,.35);
  --radius:      4px;
  --font-ui:     "Archivo", "Helvetica Neue", Arial, sans-serif;
  --font-read:   "Source Serif 4", Georgia, "Times New Roman", serif;
  --font-mono:   "JetBrains Mono", ui-monospace, "SF Mono", Menlo, monospace;
}

@media (prefers-color-scheme: dark) {
  :root:not([data-theme="light"]) {
    --ground:      #0f1512;
    --surface:     #161d19;
    --surface-2:   #1d2622;
    --line:        #2b3630;
    --line-soft:   #232d28;
    --ink:         #e7ede9;
    --ink-2:       #b9c5bf;
    --muted:       #8c9a93;
    --accent:      #57bfae;
    --accent-soft: #16302c;
    --crit:        #e08476;
    --crit-soft:   #331d1a;
    --warn:        #d5a45f;
    --warn-soft:   #322616;
    --good:        #6cbb8c;
    --good-soft:   #16291d;
    --shadow:      0 1px 2px rgba(0,0,0,.4), 0 10px 30px -20px rgba(0,0,0,.9);
  }
}

:root[data-theme="dark"] {
  --ground:      #0f1512;
  --surface:     #161d19;
  --surface-2:   #1d2622;
  --line:        #2b3630;
  --line-soft:   #232d28;
  --ink:         #e7ede9;
  --ink-2:       #b9c5bf;
  --muted:       #8c9a93;
  --accent:      #57bfae;
  --accent-soft: #16302c;
  --crit:        #e08476;
  --crit-soft:   #331d1a;
  --warn:        #d5a45f;
  --warn-soft:   #322616;
  --good:        #6cbb8c;
  --good-soft:   #16291d;
  --shadow:      0 1px 2px rgba(0,0,0,.4), 0 10px 30px -20px rgba(0,0,0,.9);
}

body {
  margin: 0;
  background: var(--ground);
  color: var(--ink);
  font-family: var(--font-ui);
  font-size: 15px;
  line-height: 1.5;
  -webkit-font-smoothing: antialiased;
}

.mono { font-family: var(--font-mono); font-variant-numeric: tabular-nums; }

.wrap {
  display: grid;
  grid-template-columns: 22rem minmax(0, 1fr);
  gap: 0;
  align-items: start;
  max-width: 96rem;
  margin: 0 auto;
}

/* ------------------------------------------------------------------ rail */

.rail {
  position: sticky;
  top: 0;
  max-height: 100vh;
  overflow-y: auto;
  padding: 2.25rem 1.75rem 2rem;
  border-right: 1px solid var(--line);
  background: var(--surface);
  display: flex;
  flex-direction: column;
  gap: 1.75rem;
}

.eyebrow {
  font-size: .688rem;
  letter-spacing: .13em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 600;
}

.brand h1 {
  font-size: 1.75rem;
  line-height: 1.1;
  margin: .35rem 0 .5rem;
  font-weight: 700;
  letter-spacing: -.02em;
  text-wrap: balance;
}

.brand .sub {
  margin: 0;
  font-family: var(--font-read);
  color: var(--ink-2);
  font-size: .938rem;
  line-height: 1.45;
}

.countdown {
  display: flex;
  align-items: baseline;
  gap: .6rem;
  padding: .9rem 1rem;
  background: var(--accent-soft);
  border-radius: var(--radius);
  border: 1px solid color-mix(in srgb, var(--accent) 25%, transparent);
}
.countdown .big { font-size: 2.5rem; font-weight: 600; line-height: 1; color: var(--accent); }
.countdown .unit { font-size: .813rem; color: var(--ink-2); letter-spacing: .01em; }

.meter .segs {
  display: flex;
  gap: 2px;
  height: 26px;
  margin-bottom: .7rem;
}
.seg {
  flex: 1 1 0;
  border-radius: 1px;
  background: var(--line);
  border-bottom: 3px solid transparent;
}
.seg--sev-blocker { border-bottom-color: var(--crit); }
.seg--sev-high    { border-bottom-color: var(--warn); }
.seg--certified { background: var(--good); }
.seg--verified  { background: var(--accent); }
.seg--in_progress { background: var(--warn); }
.seg--deferred  { background: var(--line-soft); }

.meterline {
  margin: 0 0 .6rem;
  font-size: .875rem;
  color: var(--ink-2);
  font-family: var(--font-read);
}
.meterline b { color: var(--ink); }
.alarm { color: var(--crit); }
.clear { color: var(--good); }

.legend { list-style: none; margin: 0; padding: 0; display: flex; flex-wrap: wrap; gap: .35rem .9rem; }
.legend li { display: flex; align-items: center; gap: .35rem; font-size: .75rem; color: var(--muted); }
.legend b { color: var(--ink-2); }
.key { width: 10px; height: 10px; border-radius: 2px; background: var(--line); display: inline-block; }
.key--certified { background: var(--good); }
.key--verified  { background: var(--accent); }
.key--in_progress { background: var(--warn); }
.key--deferred  { background: var(--line-soft); border: 1px solid var(--line); }

.filters { display: flex; flex-direction: column; gap: 1rem; }
.lbl {
  display: block;
  font-size: .688rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  font-weight: 600;
  margin-bottom: .4rem;
}
.search input {
  width: 100%;
  padding: .5rem .65rem;
  border: 1px solid var(--line);
  border-radius: var(--radius);
  background: var(--ground);
  color: var(--ink);
  font: inherit;
  font-size: .875rem;
}
.search input:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }

.frow { display: flex; flex-wrap: wrap; gap: .35rem; }
.f {
  font: inherit;
  font-size: .75rem;
  font-weight: 500;
  padding: .28rem .6rem;
  border: 1px solid var(--line);
  border-radius: 100px;
  background: transparent;
  color: var(--ink-2);
  cursor: pointer;
}
.f:hover { border-color: var(--accent); color: var(--accent); }
.f:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }
.f.on { background: var(--accent); border-color: var(--accent); color: var(--surface); }
:root[data-theme="dark"] .f.on { color: #0f1512; }
.f--solo { border-style: dashed; }
.count { font-size: .75rem; color: var(--muted); margin: 0; }

.railfoot { margin-top: auto; font-size: .75rem; color: var(--muted); }
.railfoot p { margin: 0 0 .3rem; }
.railfoot code { font-family: var(--font-mono); font-size: .7rem; color: var(--ink-2); }

/* ------------------------------------------------------------------ main */

.main { padding: 2.25rem 2.5rem 5rem; min-width: 0; }

.path { margin-bottom: 2.25rem; }
.path__head h2, .cat__head h2 {
  font-size: 1.125rem;
  margin: 0;
  letter-spacing: -.01em;
  font-weight: 700;
}
.path__head p {
  margin: .3rem 0 1.1rem;
  color: var(--ink-2);
  font-family: var(--font-read);
  max-width: 62ch;
}

.chain {
  display: flex;
  align-items: stretch;
  gap: 0;
  overflow-x: auto;
  padding-bottom: .3rem;
}
.chaincol {
  flex: 1 1 0;
  min-width: 13rem;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: .85rem .9rem 1rem;
}
.chaincol h3 {
  font-size: .688rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 0 0 .6rem;
  font-weight: 600;
}
.arrow {
  flex: 0 0 2.25rem;
  align-self: center;
  height: 1px;
  background: var(--line);
  position: relative;
}
.arrow::after {
  content: "";
  position: absolute;
  right: 0; top: -3px;
  border-left: 6px solid var(--line);
  border-top: 3.5px solid transparent;
  border-bottom: 3.5px solid transparent;
}
.chips { display: flex; flex-direction: column; gap: .3rem; }
.chip {
  display: flex;
  align-items: baseline;
  gap: .5rem;
  padding: .3rem .5rem;
  border-radius: 3px;
  border: 1px solid var(--line-soft);
  background: var(--ground);
  text-decoration: none;
  color: var(--ink-2);
  border-left: 3px solid var(--muted);
}
.chip:hover { border-color: var(--accent); color: var(--ink); }
.chip .mono { font-size: .75rem; font-weight: 600; color: var(--ink); }
.chip__t {
  font-size: .75rem;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}
.chip.is-certified { border-left-color: var(--good); background: var(--good-soft); }
.chip.is-verified  { border-left-color: var(--accent); background: var(--accent-soft); }
.chip.is-blocked   { border-left-color: var(--line); opacity: .68; }
.chip.is-in_progress { border-left-color: var(--warn); background: var(--warn-soft); }
.chip.is-open      { border-left-color: var(--crit); }

.pathnote {
  margin: .9rem 0 0;
  font-family: var(--font-read);
  color: var(--ink-2);
  font-size: .938rem;
  border-left: 2px solid var(--crit);
  padding-left: .8rem;
  max-width: 68ch;
}

.stats {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(9rem, 1fr));
  gap: .75rem;
  margin-bottom: 2.5rem;
}
.stat {
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: var(--radius);
  padding: .8rem .9rem;
  display: flex;
  flex-direction: column;
  gap: .15rem;
}
.stat span:first-child { font-size: 1.75rem; font-weight: 600; line-height: 1; }
.stat span:last-child { font-size: .75rem; color: var(--muted); }

.cat { margin-bottom: 2.5rem; }
.cat__head {
  display: grid;
  grid-template-columns: 1fr auto;
  align-items: baseline;
  gap: .5rem 1rem;
  padding-bottom: .55rem;
  border-bottom: 1px solid var(--line);
  margin-bottom: .9rem;
}
.cat__head p {
  grid-column: 1 / -1;
  margin: 0;
  color: var(--muted);
  font-size: .875rem;
  font-family: var(--font-read);
}
.cat__count { font-size: .813rem; color: var(--muted); }

/* ------------------------------------------------------------------ item */

.item {
  background: var(--surface);
  border: 1px solid var(--line);
  border-left: 3px solid var(--muted);
  border-radius: var(--radius);
  margin-bottom: .5rem;
  box-shadow: var(--shadow);
}
.item--blocker { border-left-color: var(--crit); }
.item--high    { border-left-color: var(--warn); }
.item--medium  { border-left-color: var(--accent); }
.item--low     { border-left-color: var(--line); }
.item.is-certified { opacity: .72; }
.item.is-certified .item__title { text-decoration: line-through; text-decoration-color: var(--line); }

.item__head {
  width: 100%;
  display: grid;
  grid-template-columns: 2.6rem minmax(0, 1fr) auto 1rem;
  align-items: center;
  gap: .75rem;
  padding: .7rem .9rem;
  background: transparent;
  border: 0;
  text-align: left;
  cursor: pointer;
  font: inherit;
  color: inherit;
}
.item__head:hover { background: var(--surface-2); }
.item__head:focus-visible { outline: 2px solid var(--accent); outline-offset: -2px; }
.item__id { font-size: .813rem; font-weight: 600; color: var(--muted); }
.item__title { font-weight: 500; font-size: .938rem; min-width: 0; }
.item__tags { display: flex; align-items: center; gap: .4rem; flex-wrap: wrap; justify-content: flex-end; }

.sev {
  font-size: .625rem;
  letter-spacing: .1em;
  text-transform: uppercase;
  font-weight: 700;
  padding: .15rem .4rem;
  border-radius: 2px;
}
.sev--blocker { background: var(--crit-soft); color: var(--crit); }
.sev--high    { background: var(--warn-soft); color: var(--warn); }
.sev--medium  { background: var(--accent-soft); color: var(--accent); }
.sev--low     { background: var(--surface-2); color: var(--muted); }

.owner {
  font-size: .688rem;
  color: var(--muted);
  border: 1px solid var(--line);
  border-radius: 100px;
  padding: .1rem .45rem;
}

.pill {
  display: inline-flex;
  align-items: center;
  gap: .3rem;
  font-size: .688rem;
  color: var(--ink-2);
  white-space: nowrap;
}
.dot { width: 7px; height: 7px; border-radius: 50%; background: var(--muted); }
.pill--certified .dot { background: var(--good); }
.pill--certified { color: var(--good); }
.pill--verified .dot { background: var(--accent); }
.pill--verified { color: var(--accent); }
.pill--in_progress .dot { background: var(--warn); }
.pill--blocked { color: var(--muted); }
.pill--blocked .dot { background: transparent; border: 1px solid var(--muted); }

.chev {
  width: .5rem; height: .5rem;
  border-right: 1.5px solid var(--muted);
  border-bottom: 1.5px solid var(--muted);
  transform: rotate(45deg);
  transition: transform .15s ease;
  justify-self: end;
}
.item__head[aria-expanded="true"] .chev { transform: rotate(-135deg); }

.item__body {
  border-top: 1px solid var(--line-soft);
  padding: 1rem 1.1rem 1.2rem;
  display: grid;
  gap: 1.1rem;
}

.deps { display: flex; flex-wrap: wrap; gap: .4rem; }
.dep {
  font-size: .688rem;
  color: var(--muted);
  border: 1px dashed var(--line);
  border-radius: 100px;
  padding: .12rem .55rem;
}
.dep--wait { color: var(--crit); border-color: color-mix(in srgb, var(--crit) 45%, transparent); }

.prose { font-family: var(--font-read); color: var(--ink-2); max-width: 68ch; }
.prose p { margin: 0 0 .55rem; }
h4 {
  font-family: var(--font-ui);
  font-size: .688rem;
  letter-spacing: .12em;
  text-transform: uppercase;
  color: var(--muted);
  margin: 1rem 0 .35rem;
  font-weight: 600;
}
.prose h4:first-child { margin-top: 0; }

.verify { background: var(--surface-2); border-radius: var(--radius); padding: .8rem .9rem 1rem; }
.verify h4 { margin-top: 0; display: flex; gap: .6rem; align-items: baseline; }
.kindnote { text-transform: none; letter-spacing: 0; font-weight: 400; font-size: .75rem; }

.cmdrow { display: flex; gap: .5rem; align-items: stretch; margin-bottom: .5rem; }
.cmdrow code {
  flex: 1 1 auto;
  min-width: 0;
  overflow-x: auto;
  white-space: pre;
  background: var(--surface);
  border: 1px solid var(--line);
  border-radius: 3px;
  padding: .4rem .55rem;
  font-size: .781rem;
  color: var(--ink);
}
.cmdrow--quiet code { color: var(--muted); }
.copy {
  font: inherit;
  font-size: .688rem;
  padding: .2rem .55rem;
  border: 1px solid var(--line);
  border-radius: 3px;
  background: var(--surface);
  color: var(--ink-2);
  cursor: pointer;
  white-space: nowrap;
}
.copy:hover { border-color: var(--accent); color: var(--accent); }
.copy:focus-visible { outline: 2px solid var(--accent); outline-offset: 1px; }

.expect { margin: 0 0 .7rem; font-size: .813rem; color: var(--ink-2); }
.expect .lbl { display: inline; margin: 0 .4rem 0 0; }

.verdict {
  display: flex;
  flex-wrap: wrap;
  align-items: baseline;
  gap: .2rem .7rem;
  padding: .4rem .6rem;
  border-radius: 3px 3px 0 0;
  font-size: .813rem;
}
.verdict span { color: var(--muted); font-size: .75rem; font-family: var(--font-mono); }
.verdict--good { background: var(--good-soft); color: var(--good); }
.verdict--bad  { background: var(--crit-soft); color: var(--crit); }
.verdict--warn { background: var(--warn-soft); color: var(--warn); }
.verdict--none { background: var(--surface); color: var(--muted); border: 1px dashed var(--line); border-radius: 3px; }

.evidence {
  margin: 0;
  padding: .6rem .7rem;
  background: var(--surface);
  border: 1px solid var(--line);
  border-top: 0;
  border-radius: 0 0 3px 3px;
  font-family: var(--font-mono);
  font-size: .75rem;
  line-height: 1.45;
  color: var(--ink-2);
  overflow-x: auto;
  max-height: 22rem;
  white-space: pre;
}

.signoff, .notes {
  border-left: 2px solid var(--good);
  padding-left: .8rem;
  font-family: var(--font-read);
  color: var(--ink-2);
}
.notes { border-left-color: var(--line); }
.signoff h4, .notes h4 { margin-top: 0; }
.signoff .meta { font-family: var(--font-mono); font-size: .75rem; color: var(--muted); margin: 0 0 .3rem; }
.signoff p:last-child, .notes ul { margin: 0; }
.notes ul { padding-left: 1rem; font-size: .875rem; }
.notes .mono { font-size: .7rem; color: var(--muted); }

.empty { text-align: center; color: var(--muted); font-family: var(--font-read); padding: 3rem 0; }

@media (max-width: 62rem) {
  .wrap { grid-template-columns: 1fr; }
  .rail { position: static; max-height: none; border-right: 0; border-bottom: 1px solid var(--line); }
  .main { padding: 1.5rem 1.25rem 4rem; }
  .item__head { grid-template-columns: 2.4rem 1fr 1rem; }
  .item__tags { grid-column: 1 / -1; justify-content: flex-start; }
}

@media (prefers-reduced-motion: reduce) {
  * { transition: none !important; animation: none !important; }
}
"""

JS = r"""
(function () {
  var KEY = "eds217-launch-board";
  var filters = { sev: [], state: [], owner: [] };
  var onlyOpen = false;
  var q = "";

  try {
    var saved = JSON.parse(localStorage.getItem(KEY) || "{}");
    if (saved.filters) filters = saved.filters;
    if (saved.onlyOpen) onlyOpen = saved.onlyOpen;
  } catch (e) { /* private window, or storage blocked */ }

  function persist() {
    try {
      localStorage.setItem(KEY, JSON.stringify({ filters: filters, onlyOpen: onlyOpen }));
    } catch (e) { /* nothing to do */ }
  }

  var items = Array.prototype.slice.call(document.querySelectorAll(".item"));
  var countEl = document.getElementById("count");
  var emptyEl = document.getElementById("empty");

  function passes(el) {
    var d = el.dataset;
    if (filters.sev.length && filters.sev.indexOf(d.sev) < 0) return false;
    if (filters.state.length && filters.state.indexOf(d.state) < 0) return false;
    if (filters.owner.length && filters.owner.indexOf(d.owner) < 0) return false;
    if (onlyOpen && (d.state === "certified" || d.state === "deferred")) return false;
    if (q && d.q.indexOf(q) < 0) return false;
    return true;
  }

  function apply() {
    var shown = 0;
    items.forEach(function (el) {
      var ok = passes(el);
      el.hidden = !ok;
      if (ok) shown++;
    });
    document.querySelectorAll(".cat").forEach(function (sec) {
      var any = sec.querySelector(".item:not([hidden])");
      sec.hidden = !any;
    });
    countEl.textContent = shown + " of " + items.length + " shown";
    emptyEl.hidden = shown !== 0;
  }

  function syncButtons() {
    document.querySelectorAll(".f[data-f]").forEach(function (b) {
      var on = filters[b.dataset.f].indexOf(b.dataset.v) >= 0;
      b.classList.toggle("on", on);
      b.setAttribute("aria-pressed", on ? "true" : "false");
    });
    var oo = document.getElementById("onlyopen");
    oo.classList.toggle("on", onlyOpen);
    oo.setAttribute("aria-pressed", onlyOpen ? "true" : "false");
  }

  document.querySelectorAll(".f[data-f]").forEach(function (b) {
    b.addEventListener("click", function () {
      var list = filters[b.dataset.f];
      var i = list.indexOf(b.dataset.v);
      if (i < 0) { list.push(b.dataset.v); } else { list.splice(i, 1); }
      persist(); syncButtons(); apply();
    });
  });

  document.getElementById("onlyopen").addEventListener("click", function () {
    onlyOpen = !onlyOpen; persist(); syncButtons(); apply();
  });

  document.getElementById("clearf").addEventListener("click", function () {
    filters = { sev: [], state: [], owner: [] };
    onlyOpen = false;
    document.getElementById("q").value = "";
    q = "";
    persist(); syncButtons(); apply();
  });

  document.getElementById("q").addEventListener("input", function (e) {
    q = e.target.value.trim().toLowerCase();
    apply();
  });

  document.querySelectorAll(".item__head").forEach(function (h) {
    h.addEventListener("click", function () {
      var open = h.getAttribute("aria-expanded") === "true";
      h.setAttribute("aria-expanded", open ? "false" : "true");
      document.getElementById(h.getAttribute("aria-controls")).hidden = open;
    });
  });

  document.querySelectorAll(".copy").forEach(function (b) {
    b.addEventListener("click", function (e) {
      e.stopPropagation();
      var text = b.dataset.copy;
      var done = function () {
        var was = b.textContent;
        b.textContent = "copied";
        setTimeout(function () { b.textContent = was; }, 1200);
      };
      if (navigator.clipboard && navigator.clipboard.writeText) {
        navigator.clipboard.writeText(text).then(done, function () {});
      } else {
        var ta = document.createElement("textarea");
        ta.value = text;
        document.body.appendChild(ta);
        ta.select();
        try { document.execCommand("copy"); done(); } catch (err) {}
        document.body.removeChild(ta);
      }
    });
  });

  document.querySelectorAll(".chip").forEach(function (a) {
    a.addEventListener("click", function () {
      var id = a.getAttribute("href").slice(1);
      var el = document.getElementById(id);
      if (!el) return;
      var h = el.querySelector(".item__head");
      if (h && h.getAttribute("aria-expanded") !== "true") { h.click(); }
    });
  });

  syncButtons();
  apply();
})();
"""
