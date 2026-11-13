# Phase 2: the 105 cells without a public witness on 4 November 2026

On 4 November 2026, 105 lower bounds in the tables of Radziszowski's survey *Small Ramsey Numbers* (DS1, revision
18) had no public witness file that was checked here (32 marked RECIPE and 73 marked NO_FILE_FOUND in
`results/coverage.csv`). Phase 2, from 7 to 12 November 2026, built the constructions that the survey and the cited
papers describe, looked again for public files, and checked what was found or built. This folder holds the result.

The work followed a registration written before it started, with six amendments on what each label means and on
searching. The labels are:

- **VERIFIED**: every half (two colours) or every colour of the witness was checked by two independent exact
  checkers on the object itself.
- **VERIFIED (symmetry-reduced)**: as above, on a smaller problem that uses automorphisms of the object. Each
  automorphism, the transitivity or the orbits used were checked on the object first, and both checkers ran on the
  reduced problem.
- **VERIFIED (by proof: citation)**: one half, one colour or the whole row follows from a published theorem, cited
  with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by
  both checkers. Proofs written here do not count.
- **VERIFIED (witness found here by search)**: the witness, or the input it is built from, was found here by a search
  (Amendment 2 or 6, see Searches below), and every colour of the witness was checked by both checkers, on the whole
  object or with a reduction verified on the object, as the row says.
- **PARTIAL**: one check is missing, as the row says.
- **RECIPE ONLY**: the construction is written down or built, and not checked.
- **NOT REPRODUCED**: the construction as described could not be reproduced from the paper here.
- **STILL NO FILE**: no public witness was found.

A TIMEOUT is never counted as a check.

## Status on 12 November 2026

| status | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED | 7 | 27 | 34 |
| VERIFIED (symmetry-reduced) | 14 | 6 | 20 |
| VERIFIED (by proof: citation) | 18 | 8 | 26 |
| VERIFIED (witness found here by search) | 3 | 1 | 4 |
| PARTIAL | 1 | 1 | 2 |
| RECIPE ONLY | 5 | 0 | 5 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 4 | 5 | 9 |
| all | 55 | 50 | 105 |

84 of the 105 cells are VERIFIED in one of the four forms. The table is written by `make_phase2.py` into
`summary.json` and `COVERAGE.md`. Two rows are PARTIAL while a check is still running:

- R(9,9,9,9): the object is built and certified and its inputs have both checkers, but the window search for
  colours 1 and 2 (K9 on vertices 0..10240) is not finished.
- R(7,21): one reduced independence subproblem has been decided by clique.c only.

When such a check finishes, the row is updated the same way as the others: logs under `checks/logs/`, the new
`label`, `group`, `checks` and `proof` in `coverage.csv`, then `python3 phase2/make_phase2.py`,
`python3 make_readme.py` and `python3 phase2/check_phase2.py --only CELL`. A row moves up only with a new check entry.

## Searches

Searching for new witnesses was outside the registration at first. Two amendments allowed it, and every row whose
witness was found by search says so in its label or its notes.

- Amendment 2 (7 November) kept three witnesses found by short searches outside the original scope: R(4,10) and
  R(5,8) (circulant tabu search) and R(4,17) (unions of cyclotomic classes mod 199). Their rows are labelled
  "VERIFIED (witness found here by search)", and the rows R(6,15) and R(7,18), built from two of them, say so in their notes.
- Amendment 6 (12 November) allowed a search for the lost cells under these rules: runs in the cloud only, each
  restartable and under 10 minutes, at most 2 cores at low priority. About one day of computing per target, and a
  target is dropped once three independent methods have stopped improving. Methods are cyclic, block-cyclic and
  Cayley ansatzes, annealing, and SAT with clique clauses added lazily. Third-party code is used only from its public
  source, with its commit recorded. Every find is checked with both checkers like any other witness and labelled
  "witness found here by search". Nothing is published or sent as part of the search.

Find so far under Amendment 6 (full record of the run, with scripts, solver versions and logs, in `search_s1/SEARCH_RECORD.md`):

| find | how | check |
|---|---|---|
| cyclic (3,3,7;80) colouring, `witnesses/inputs/R3_3_7_n80_cyclic.colormat.gz` (sha256 636ac4bc... uncompressed) | SAT on Z_80 | verify_ramsey PASS (circulant). clique.c and gen0 on every colour, whole graph: NONE 2, NONE 2, NONE 6. Controls: lowered k FOUND, one edge recoloured caught, by both checkers |
| (3,3,3,7;246) colouring, `witnesses/R3_3_3_7_n246.colormat.gz` (sha256 e1e5cda0... uncompressed), so R(3,3,3,7) >= 247 | Robertson's construction (Electron. J. Combin. 6 (1999) #R3, Part Two) applied to the find above | verify_ramsey PASS. clique.c and gen0 on every colour, whole graph, no reduction: NONE 2, 2, 2, 6. Controls as above |

The (3,3,7;80) colouring is below the survey's value R(3,3,7) >= 85, so that cell stays STILL NO FILE. The other
targets (R(6,13), R(3,3,7), R(3,4,6), R(3,3,8), R(3,3,3,4), R(3,3,3,5), R(3,14)): search in progress, no results
recorded.

## Contents

| path | what |
|---|---|
| `coverage.csv` | one row per cell: survey bound and reference, label, witness file and SHA-256, source with page, table or row, URL or DOI, how the file was read or built, licence or credit, checks, proof, notes |
| `COVERAGE.md` | the same, as tables grouped by label |
| `witnesses/` | 86 witness files, gzip-compressed (2.5 MB in all, the largest 1.2 MB), the search input in `witnesses/inputs/`, and `manifest.csv` with format, vertex count, SHA-256 of the committed file and of the object as named in the check logs, credit and licence |
| `CHECKS.md` | the checks behind each label, the checkers and machines, and how to rerun a check |
| `checks/logs/` | the check logs and build records, with `INDEX.csv` |
| `certificates/` | rebuild certificates and the records for the rows that rest on a theorem, with `CERTIFICATES.md` |
| `NOTES.md` | a misprint, three constructions not reproduced from the text, readings of printed tables, third-party claims noted and not counted |
| `search_s1/` | the record of the Amendment 6 search run behind R(3,3,3,7): scripts, solver versions, log entries, `SEARCH_RECORD.md` |
| `search_records/` | where each search round looked, with what it found, including searches that found nothing (`sources.csv` and `searched_before.csv` of the rounds), with `INDEX.csv` |
| `recipes.csv` | the large built objects (the five RECIPE ONLY rows and the six Rowley rows): the object, the expected SHA-256 of the built file, the build script and the row's status |
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
