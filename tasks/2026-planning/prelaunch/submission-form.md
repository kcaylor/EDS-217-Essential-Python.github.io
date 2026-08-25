# The final project submission form

Decided 2026-08-24. One Google Form, one submission per team, and its timestamp
is the deadline.

**Built and published 2026-08-25.** Responders are restricted to University of
California, Santa Barbara, so a personal Google account is turned away. The link
is live in `final_project.qmd` (under Handing it in) and `day9.qmd` (step 5).

- Responder link: <https://docs.google.com/forms/d/e/1FAIpQLSdfFOUGbZHfXONdrP1adl6D-8H90DSHgnMic4I2-YwQyLre8A/viewform>
- Edit link: <https://docs.google.com/forms/d/11V-4tFtEVcPeC0XSsXhycm5g7AFDr4_BUe0TioBrlLQ/edit>

Built as specified below, with two deliberate changes. The total upload ceiling
is 10 GB rather than the 1 GB default, because twelve teams at up to 100 MB each
could approach 1 GB and Forms stops accepting responses at the limit rather than
warning. And the UCSB restriction is set as the publish audience, which is where
that control now lives, rather than as a separate setting.

## Questions

| # | Question | Type | Required |
|---|---|---|---|
| 1 | Team name | Short answer | yes |
| 2 | Team members, full names | Short answer | yes |
| 3 | Repository URL | Short answer, response validation set to URL | yes |
| 4 | Your notebook. Upload the `.ipynb`, or an HTML export if you prefer. | File upload, 1 file, 100 MB | yes |
| 5 | Your slides, if your team made any. Most teams present from the notebook and upload nothing here. | File upload, 1 file, 100 MB | no |

## Settings

- **Restrict to UCSB.** File upload requires it, because Google needs a signed-in
  account to attribute the file.
- **Collect email addresses.** Gives a second identifier if a team name is
  ambiguous.
- **Limit to one response**, with editing allowed after submission, so a team can
  correct a wrong URL without a second row appearing.
- Title it so it is findable a year later: *EDS 217 Summer 2026 final project*.

## Why a form rather than email

Twelve teams submit inside a ten-minute window before lunch. Email gives no single
view of who has submitted and no timestamp anybody trusts. The form's response
sheet is one row per team, timestamped, and it doubles as the roster for Friday
afternoon.

## What still needs doing

The form URL is not yet in the pages. Both `final_project.qmd` and `day9.qmd` say
"the course form" and describe what it asks for, so they are correct but not yet
clickable. Recorded as a needs-kelly finding on both pages in the voice-pass
ledger.
