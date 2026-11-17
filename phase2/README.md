# Phase 2: the 105 cells without a public witness on 4 November 2026

On 4 November 2026, 105 lower bounds in the tables of Radziszowski's survey *Small Ramsey Numbers* (DS1, revision
18) had no public witness file that was checked here (32 marked RECIPE and 73 marked NO_FILE_FOUND in
`results/coverage.csv`). Phase 2, from 7 to 14 November 2026, built the constructions that the survey and the cited
papers describe, looked again for public files, and checked what was found or built. This folder holds the result.

The work followed a registration written before it started, with amendments on what each label means, on
searching and on the symmetry reductions that may be used. The labels are:

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

## Status on 16 November 2026

| status | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED | 8 | 31 | 39 |
| VERIFIED (symmetry-reduced) | 16 | 6 | 22 |
| VERIFIED (by proof: citation) | 20 | 9 | 29 |
| VERIFIED (witness found here by search) | 3 | 1 | 4 |
| PARTIAL | 0 | 0 | 0 |
| RECIPE ONLY | 3 | 0 | 3 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 2 | 1 | 3 |
| all | 55 | 50 | 105 |

94 of the 105 cells are VERIFIED in one of the four forms. The table is written by `make_phase2.py` into
`summary.json` and `COVERAGE.md`. Two rows changed on 13 November:

- R(9,9,9,9) is VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250). The window search for colours 1 and 2
  (K9 on vertices 0..10240) was split exactly into 2981 and 2908 pieces, and every piece was decided by clique.c and
  by gen0. The record is `certificates/rowley_round6_windows_full.jsonl`.
- R(3,14) is VERIFIED with Kolodyazhny's own (3,14;66) graph, read from three Wayback Machine captures of his page
  (21 January 2022, 31 December 2024, 20 February 2025). The page states no licence. The matrix is included as a
  transcribed fact with credit, exact source and SHA-256, and is removed on request (`CORRECTIONS.md`).

Three rows changed on 14 November:

- R(7,21) is VERIFIED (symmetry-reduced). The one reduced independence subproblem that had been decided by clique.c
  only was decided by gen0 as well (NONE, 613 s). The record is `checks/logs/build_round7/`.
- R(19,19) and R(20,20) are VERIFIED (by proof: Shearer 1986). Their inputs, c(G_8941) = 17 and c(G_10861) = 18, were
  checked by clique.c and by gen0 on every orbit representative (2234 and 2714 pieces, all NONE), with a K_17 and a
  K_18 checked edge by edge. These two runs use one more step of symmetry than the rows R(13,13) to R(18,18). It is
  described in `NOTES.md`, section 10, and was written into the registration after the first of the two runs. The
  records are `certificates/paley_omega_ordered_wave9.jsonl` and `checks/logs/mac_batch/wave9/`.

Five rows changed on 16 November. In each the witness is the colouring of the author the survey cites, sent by him
on request and credited to him as personal communication (`CORRECTIONS.md` applies):

- R(6,13) is VERIFIED (symmetry-reduced) with the first of the five cyclic (6,13;346) colourings that Eugene Kuznetsov
  sent on 14 November (he agreed to its addition on 15 November). It was checked on 14 November by clique.c and gen0
  through vertex 0 after the circulant automorphism was checked on the matrix. The record is
  `scripts_as_run/kuznetsov_2026-11-14/`.
- R(3,3,7), R(3,3,8), R(3,4,6) and R(3,3,3,4) are VERIFIED with the (3,3,7;84), (3,3,8;102), (3,4,6;116) and
  (3,3,3,4;96) colourings that Geoffrey Exoo sent on 16 November. Every colour of each was checked on the whole graph
  by clique.c and gen0, with controls. The record is `checks/logs/exoo_2026-11-16/` and the script is
  `scripts_as_run/exoo_2026-11-16/exoo_check.py`.

No row is PARTIAL. When a later check finishes, the row is updated the same way as the others: logs under `checks/logs/`, the new
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

Finds under Amendment 6 (the record of the search, with scripts, solver versions and logs, is `search_s1/SEARCH_RECORD.md`):

| find | how | check |
|---|---|---|
| cyclic (3,3,7;80) colouring, `witnesses/inputs/R3_3_7_n80_cyclic.colormat.gz` (sha256 636ac4bc... uncompressed) | SAT on Z_80 | verify_ramsey PASS (circulant). clique.c and gen0 on every colour, whole graph: NONE 2, NONE 2, NONE 6. Controls: lowered k FOUND, one edge recoloured caught, by both checkers |
| (3,3,3,7;246) colouring, `witnesses/R3_3_3_7_n246.colormat.gz` (sha256 e1e5cda0... uncompressed), so R(3,3,3,7) >= 247 | Robertson's construction (Electron. J. Combin. 6 (1999) #R3, Part Two) applied to the find above | verify_ramsey PASS. clique.c and gen0 on every colour, whole graph, no reduction: NONE 2, 2, 2, 6. Controls as above |

The (3,3,7;80) colouring is below the survey's value R(3,3,7) >= 85, so that cell stays STILL NO FILE. The search also
found a cyclic (3,3,7;81) colouring, which is not used in any row.

The search ended on 13 November. Outcome for the other targets:

| target | outcome |
|---|---|
| R(6,13), a (6,13;346) colouring | not found. Three cyclic forms with a multiplier excluded exactly, two forms undecided. Kuznetsov's public code reached cyclic order 172 within the run limits |
| R(3,3,7), a (3,3,7;84) colouring | not found. The cyclic (3,3,7;81) colouring has no extension by one or by three new vertices (exact). Cyclic and block-cyclic forms on 82 to 84 vertices undecided |
| R(3,4,6), a (3,4,6;116) colouring | not found. Four symmetric forms excluded exactly, three undecided |
| R(3,3,8), a (3,3,8;102) colouring | not found. Two symmetric forms excluded exactly, two undecided |
| R(3,3,3,4), a (3,3,3,4;96) colouring | not found. Two symmetric forms excluded exactly, the cyclic form undecided |
| R(3,3,3,5), a (3,3,3,5;161) colouring | not found. Three symmetric forms excluded exactly, two undecided |
| R(3,14), a (3,14;66) graph | not found by the search. There is no Cayley graph of this kind on any of the four groups of order 66 (exact). The cell is VERIFIED by Kolodyazhny's graph, which is not a Cayley graph |

An exact negative holds only for the symmetric form stated in `search_s1/SEARCH_RECORD.md`. A run that reached its
time limit decides nothing. The annealing runs stopped improving for every target, which is a plateau of the method
and not evidence that no colouring exists.

## Contents

| path | what |
|---|---|
| `coverage.csv` | one row per cell: survey bound and reference, label, witness file and SHA-256, source with page, table or row, URL or DOI, how the file was read or built, licence or credit, checks, proof, notes |
| `COVERAGE.md` | the same, as tables grouped by label |
| `witnesses/` | 89 witness files, gzip-compressed (3.2 MB in all, the largest 1.2 MB), the search input in `witnesses/inputs/`, and `manifest.csv` with format, vertex count, SHA-256 of the committed file and of the object as named in the check logs, credit and licence |
| `CHECKS.md` | the checks behind each label, the checkers and machines, and how to rerun a check |
| `checks/logs/` | the check logs and build records, with `INDEX.csv` |
| `certificates/` | rebuild certificates and the records for the rows that rest on a theorem, with `CERTIFICATES.md` |
| `NOTES.md` | a misprint, three constructions not reproduced from the text, readings of printed tables, third-party claims noted and not counted, and what the search for Exoo's unpublished colourings covered |
| `search_s1/` | the record of the Amendment 6 search: the run behind R(3,3,3,7), and in `all_targets/` the scripts and logs of every target, with the outcome for each in `SEARCH_RECORD.md` |
| `search_records/` | where each search round looked, with what it found, including searches that found nothing (`sources.csv` and `searched_before.csv` of the rounds), with `INDEX.csv` |
| `recipes.csv` | the large built objects (the diagonal rows R(19,19) to R(23,23), of which three are RECIPE ONLY, and the six Rowley rows): the object, the expected SHA-256 of the built file, the build script and the row's status |
| `scripts_as_run/` | the build and check scripts as they were run, with `INDEX.csv` |
| `check_phase2.py` | runs the repository checker on every witness file |
| `make_phase2.py` | writes `COVERAGE.md`, `CHECKS.md`, `summary.json` and the README section from the CSV files |
| `results/` | output of `check_phase2.py` from a fresh clone |

## File formats

- `.g6.gz`: graph6, one graph (two-colour witnesses). The graph has no K_k and no independent l-set for R(k,l).
- `.colormat.gz`: n lines of n digits, the colour of edge ij (the `colormat` format of `verify_ramsey.py`). The
  R(3,14) file is the 0/1 adjacency matrix as its author printed it: digit 1 is an edge, digit 0 a non-edge.
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
