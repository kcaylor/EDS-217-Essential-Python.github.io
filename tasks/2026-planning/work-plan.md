# EDS 217: 2026 Revision Work Plan

**Created:** 2026-07-07 (rev. same day after calendar check). Working document; permanent record lives in the Obsidian vault and `2026-day-skeleton.md`.
**Course dates:** Mon Aug 31 – Fri Sep 4 (Days 1–5), Tue Sep 8 – Fri Sep 11 (Days 6–9). Labor Day Sep 7 off.
**Hard constraints from Kelly's calendar:**
- Out of office Jul 29 – Aug 4
- **Kenya Aug 16–31, returning the day class starts**
- Therefore: **launch = Fri Aug 14** (site live before departure). Aug 16–30 is a content freeze; only emergency fixes.

**Team:** Kelly (~5–6 hrs/week in scheduled blocks; ~11 blocks total through Aug 14), Claude (drafting, mechanics, QA; works between blocks), Cella Schnabel (TA: cold-tests materials week of Aug 10, must be scheduled with her NOW).

## Milestones (compressed for Aug 14 launch)

| # | Date | Gate |
|---|---|---|
| M1 | Fri Jul 17 | Housekeeping done: OpenAQ reconciled + committed; `eds217_2026` env + kernel refs; org-repo remote; navbar/dates; fork PR resolved; D5 OpenAQ EOD design reviewed |
| M2 | Fri Jul 24 | New builds drafted + reviewed: D2 data-biography EOD, Day 1 Whole Game sessions, 6b reshape session |
| M3 | Fri Aug 7 | All session rebuilds/relocations/trims complete (D2–D7); cheatsheets updated; materials to Cella |
| M4 | Wed Aug 12 | Content-complete: full build clean; all six quality gates pass on all 7 EODs; Cella feedback triaged |
| M5 | **Fri Aug 14** | Launch: fixes in, index/syllabus/TA updated, pushed to fork + org synced, live site verified |

Days 6–9 materials (used Sep 8–11) get one final look Sun Aug 30 / Mon Aug 31 evening if needed, but plan as if Aug 14 is final.

## Quality gates (every EOD, before M4)

1. Every construct traces to a day scope table in `2026-day-skeleton.md`
2. Half-day rule holds (afternoon-taught → ADAPT max same day)
3. ≤2 Field Notes per EOD
4. Handout/answer-key drift check passes (no key-only tasks; names match)
5. `grep` for lambda returns nothing in course materials
6. 2025 EOD alignment checklist run and archived

## Week-by-week (Kelly's blocks are on the calendar; Claude works between them)

### W1 · Jul 13–17 → **M1**
- Claude: reconcile OpenAQ CSVs; `eds217_2026` env + kernel rename script; drift/lambda check scripts; navbar/dates; org remote; resolve fork PR; draft D5 OpenAQ EOD
- Kelly blocks: Wed 7/15 13:00–14:45 (housekeeping decisions, OpenAQ keep/revert); Fri 7/17 15:15–17:15 (D5 EOD design review: sets the template for all new EODs)

### W2 · Jul 20–24 → **M2**
- Claude: rebuild Day 1 (1a merge, 1b compress, Whole Game 1c/1d, EOD READ→ADAPT); draft D2 data-biography EOD; build 6b reshape session
- Kelly blocks: Mon 7/20 8:30–11:30 (Day 1 + D2 EOD pedagogy pass: the crux); Wed 7/22 8:30–11:30 (reshape session + carry-over)

### W3 · Jul 27–28 (short week; OOO from 7/29) 
- Claude: D2 sessions (2a/2b/2c/2d) and D3 sessions (3a–3d) + Banana relocation trims; continues drafting D4/D5 sessions through Kelly's OOO
- Kelly blocks: Mon 7/27 8:30–11:30 (D2 sessions review); Tue 7/28 8:30–11:30 (D3 review + pre-OOO triage)

### W4 · Aug 5–7 (OOO ends 8/4) → **M3**
- Claude: finish D4 (incl. functions session 4c) + microplastics trims; D5 sessions + OpenAQ EOD final; D6 (Eurovision redesign) and D7 (project-kickoff slot, hardiness Field Notes); cheatsheet updates
- Kelly blocks: Wed 8/5 8:30–11:30 (D4/D5 review); Thu 8/6 8:30–11:30 (D6/D7 review); send materials + instructions to Cella by Fri 8/7

### W5 · Aug 10–14 → **M4, M5 (LAUNCH)**
- Claude: `_quarto.yml` nav overhaul; full build; run all quality gates; link check; simulated-student pass on D2 + D5; fix list from Cella
- Cella: cold-tests D2 + D5 EODs Mon–Tue
- Kelly blocks: Mon 8/10 8:30–11:30 (QA + gate review); Wed 8/12 8:30–11:30 (Cella feedback triage, M4 signoff); Fri 8/14 13:00–16:00 (final review, deploy: push fork → sync org → verify live site)

### Aug 16–30: Kenya. Content freeze.
- Optional: Kelly skims Days 6–9 materials Sun 8/30 evening; Claude available in a session for emergency fixes only.

## Standing rhythm

- Work happens in Cowork sessions during Kelly's calendar blocks; Claude preps drafts before each block so block time is review/decision time
- Things project "EDS 217 — 2026 Course Revision" carries the five milestones; this file carries the detail
- Every block's calendar event links the Things project and current milestone

## Risks

- **Zero slack after Aug 14.** Any slip eats the Cella test or the launch, not the calendar. If a week slips, cut scope in this order: 7d project-kickoff session → D2 colab polish → cheatsheet updates (ship 2025 versions).
- **Day 2 crux:** if the data-biography EOD tests poorly with Cella (Aug 10–11), fallback: re-insert 2025's 2a/2b sessions, slide the spine half a day. Decision: Aug 12 block.
- **Cella availability week of Aug 10:** confirm with her THIS WEEK; if she can't, Claude's simulated-student pass substitutes (weaker signal), and Kelly spot-tests D2 during the Aug 10 block.
- **Course opens the day Kelly returns from Kenya:** Days 1–5 materials must be genuinely final on Aug 14; prioritize their QA over Days 6–9.
- **Org-repo sync is manual:** deploy checklist on Aug 14 includes same-day live-site verification.
