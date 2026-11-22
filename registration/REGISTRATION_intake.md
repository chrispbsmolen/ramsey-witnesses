# Registration: intake of witnesses

Written 21 and 22 November 2026, after phase 2 closed at commit 1d7aabe (phase-2 Amendment 11). The intake holds the items in flight at phase 2's close and everything received or found since, each in its own row. The third-party files and claims that phase 2 recorded only in its notes, search records or check logs stay
there, and each is entered when its file has been fetched at a fixed address and checked here. Three GitHub issues (#1
received 18 November, #2 and #3 received 20 November) had already been received when this was written, and they are
decided under it like any later item.

## Scope

In:
- a witness file for a lower bound on a Ramsey number, for a cell of the survey's tables or a cell the survey leaves
  blank, that is public at a fixed address (a repository commit, a DOI version, or an archived copy), or that its
  author sent with written permission to publish it here
- a claim of a lower bound with no file checked here, recorded as a claim and never as a witness

Out: any claim that a survey entry is wrong, and upper bounds.

## How a witness is checked

- Two independent exact checkers, `clique.c` of this repository and `phase2/scripts_as_run/build_round2/checker/gen0.c`,
  each reading the file with its own reader, on every color of the whole object. A reduction may be used only as
  phase-2 Amendments 1, 5 and 10 allow, and the row says which.
- Controls: each checker must find a clique one smaller than the forbidden size in every color where one exists, and
  must find the forbidden clique in a copy where one was planted.
- `verify_ramsey.py` is also run.
- The logs and the scripts as run are stored with SHA-256 under `intake/checks/<id>/`.
- A TIMEOUT is never a check.

## Decisions

Each received or found item gets one row in `table/intake.csv` with one of these decisions:

| decision | meaning |
|---|---|
| pending | recorded, and not yet checked under this registration (a row says what, if anything, phase 2 checked) |
| accepted | checked here as above, and every check passed |
| failed | a check here did not pass. The logs are kept and the file is never listed as a witness |
| noted | a claim with no file checked here, entered only when its source has been read again, and listed only in
`table/claims.csv` |
| withdrawn | removed from the current tree at the request of its author or holder (CORRECTIONS.md). Git history keeps it |

Every decision that makes a file count or stop counting (accepted, failed, withdrawn) is its own commit, so every
change in the list of witnesses belongs to one decision. Rows recorded as pending or noted may share a commit. A row is
never deleted. If a later recheck fails, the decision becomes failed with its date and logs.

## What each row records

- the file credit (who made and published the file) and, where it is known, its public date, the earliest dated public
  posting
- the bound credit (the survey's reference for the value, if the survey has one), kept separate from the file credit
- the construction credit, when the file was built from other graphs
- the survey basis, compared with the survey's table only: in the survey table, implied by the survey's own items, or
  above the survey table
- for each accepted witness, a canonical-form hash of the graph or coloring, so that two files of the same object are
  recognized. When two files give the same bound, both are listed, earliest public date first
- the date of the check here, and exactly what was checked

## Files and licenses

A file is stored here when its license allows redistribution, with the notices the license requires. For CC BY 4.0
(section 3(a)) these are the creator, the copyright notice, a notice that refers to the license, a notice that refers
to its disclaimer of warranties, the source link, and a note if the file was modified. For MIT they are the copyright
and permission notice. Otherwise the row links the file at its fixed address with its SHA-256. A file sent by its author is stored only with the author's written permission.

## Survey revisions

The survey reference is revision 18 (24 April 2026). When a new revision appears, its values are read into a new
dated snapshot beside the old one, which is kept. The current view says which revision it compares against.

## Maintenance

This replaces the line "No maintenance obligation" of the phase-1 registration. The repository is maintained by
Christopher Smolen. Each change to the current view is released under a git tag. If maintenance stops, the last
tagged release stays as the dated snapshot.

Approval: Christopher, with his OK of the push that first publishes this file.
