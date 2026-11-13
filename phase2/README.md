# Phase 2: the 105 cells without a public witness on 4 November 2026

On 4 November 2026, 105 lower bounds in the tables of Radziszowski's survey *Small Ramsey Numbers* (DS1, revision
18) had no public witness file that was checked here (32 marked RECIPE and 73 marked NO_FILE_FOUND in
`results/coverage.csv`). Phase 2, from 7 to 12 November 2026, built the constructions that the survey and the cited
papers describe, looked again for public files, and checked what was found or built. This folder holds the result.

The work followed a registration written before it started, with five amendments on what each label means. The
labels are:

- **VERIFIED**: every half (two colours) or every colour of the witness was checked by two independent exact
  checkers on the object itself.
- **VERIFIED (symmetry-reduced)**: as above, on a smaller problem that uses automorphisms of the object. Each
  automorphism, the transitivity or the orbits used were checked on the object first, and both checkers ran on the
  reduced problem.
- **VERIFIED (by proof: citation)**: one half, one colour or the whole row follows from a published theorem, cited
  with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by
  both checkers. Proofs written here do not count.
- **PARTIAL**: one check is missing, as the row says.
- **RECIPE ONLY**: the construction is written down or built, and not checked.
- **NOT REPRODUCED**: the construction as described could not be reproduced from the paper here.
- **STILL NO FILE**: no public witness was found.

A TIMEOUT is never counted as a check.

## Status on 12 November 2026

| status | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED | 10 | 27 | 37 |
| VERIFIED (symmetry-reduced) | 14 | 6 | 20 |
| VERIFIED (by proof: citation) | 18 | 3 | 21 |
| PARTIAL | 1 | 0 | 1 |
| RECIPE ONLY | 5 | 6 | 11 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 4 | 6 | 10 |
| all | 55 | 50 | 105 |

The table is written by `make_phase2.py` into `summary.json` and `COVERAGE.md`. Six of the RECIPE ONLY rows,
R(7,7,7,7), R(8,8,8,8), R(9,9,9,9), R(6,6,6,6,6), R(5,5,5,5,5,5) and R(6,6,6,6,6,6), are being checked in a run
that had not finished on 12 November. Their rows say so, and they stay RECIPE ONLY until a new check entry exists.
R(7,21) is PARTIAL because one of its reduced subproblems has been decided by clique.c only.

### Slot for the six rows still running

When that run finishes, each of the six rows is filled in the same way as the others:

1. add the witness file to `witnesses/` (gzip) and a row to `witnesses/manifest.csv`,
2. in `coverage.csv`, set `label`, `group`, `witness`, `n`, the two SHA-256 fields, `checks` and `proof`, and replace
   the note "SLOT build_round6",
3. add the logs under `checks/logs/build_round6/` (and to its `INDEX.csv`) and any rebuild certificate to
   `certificates/`,
4. set the row's status in `recipes.csv`, then run `python3 phase2/make_phase2.py`, `python3 make_readme.py` and
   `python3 phase2/check_phase2.py --only CELL`.

A row whose checks do not meet the rules above stays RECIPE ONLY or becomes PARTIAL, with what is missing.

## Contents

| path | what |
|---|---|
| `coverage.csv` | one row per cell: survey bound and reference, label, witness file and SHA-256, source with page, table or row, URL or DOI, how the file was read or built, licence or credit, checks, proof, notes |
| `COVERAGE.md` | the same, as tables grouped by label |
| `witnesses/` | 79 witness files, gzip-compressed (2.5 MB in all, the largest 1.2 MB), and `manifest.csv` with format, vertex count, SHA-256 of the committed file and of the object as named in the check logs, credit and licence |
| `CHECKS.md` | the checks behind each label, the checkers and machines, and how to rerun a check |
| `checks/logs/` | the check logs and build records, with `INDEX.csv` |
| `certificates/` | rebuild certificates and the records for the rows that rest on a theorem, with `CERTIFICATES.md` |
| `NOTES.md` | a misprint, three constructions not reproduced from the text, readings of printed tables, third-party claims noted and not counted |
| `search_records/` | where each search round looked, with what it found, including searches that found nothing (`sources.csv` and `searched_before.csv` of the rounds), with `INDEX.csv` |
| `recipes.csv` | the RECIPE ONLY rows: the object, the expected SHA-256 of the built file and the build script |
| `scripts_as_run/` | the build and check scripts as they were run, with `INDEX.csv` |
| `check_phase2.py` | runs the repository checker on every witness file |
| `make_phase2.py` | writes `COVERAGE.md`, `CHECKS.md`, `summary.json` and the README section from the CSV files |
| `results/` | output of `check_phase2.py` from a fresh clone |

## File formats

- `.g6.gz`: graph6, one graph (two-colour witnesses). The graph has no K_k and no independent l-set for R(k,l).
- `.colormat.gz`: n lines of n digits, the colour of edge ij (the `colormat` format of `verify_ramsey.py`).
- `.lengths.gz`: a linear colouring. Line 1 is n, line 2 the colours of the edge lengths 1..n-1, and edge {i, j}
  has the colour of length |i - j|. All of these are cyclic (the colour of length d equals that of n - d).

`verify_ramsey.py` reads the first two formats directly, compressed or not. `check_phase2.py` reads all three.

## Logs and scripts

The logs and scripts were copied from the working folders without change, except that local folder names and the
host name were replaced by `<ramsey>`, `<cloud>`, `<scratch>`, `<mac>` and `<user>`. `INDEX.csv` in each folder gives
the SHA-256 of the original file and of the copy here, and marks which files had such a replacement. In the search
records and in a few scripts some working remarks were reworded, and those files are marked in the same way.

## Sources and licences

Each witness file is credited in `witnesses/manifest.csv` and `coverage.csv` to the authors whose construction or
data it is. Files built here from published constructions are MIT like the rest of this repository, with the
construction credited to its authors. Colourings transcribed from papers (distance sets, partitions, printed
matrices) are recorded as facts with credit to the paper, page and table. Files converted from public data keep
the licence of that data (CC0 1.0 for the Courties repository, the arXiv licence for arXiv source files), and
the row says which. A request to change the credit or remove a file is handled as described in `CORRECTIONS.md`.
