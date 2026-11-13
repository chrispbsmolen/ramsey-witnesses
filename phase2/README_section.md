## Phase 2 (12 November 2026)

On 4 November 105 cells of the table above had no public witness (32 RECIPE, 73 NO_FILE_FOUND). Phase 2 built the published constructions for these cells, looked again for public files, and checked what was found or built. For three cells, R(4,10), R(5,8) and R(4,17), the published colouring is not public, and the witness here was found by a short search. Those rows, and R(6,15) and R(7,18), which are built from two of them, say so. For R(3,3,3,7) the input colouring needed by the published construction is not public, and a registered search found one (see below). Everything is in `phase2/`, with one row per cell in `phase2/coverage.csv` and `phase2/COVERAGE.md`.

| status on 12 November | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED | 9 | 27 | 36 |
| VERIFIED (symmetry-reduced) | 15 | 6 | 21 |
| VERIFIED (by proof: citation) | 18 | 8 | 26 |
| VERIFIED (witness found here by search) | 0 | 1 | 1 |
| PARTIAL | 1 | 1 | 2 |
| RECIPE ONLY | 5 | 0 | 5 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 4 | 5 | 9 |
| all | 55 | 50 | 105 |

- VERIFIED: every half (every colour) of the witness was checked here by two independent exact checkers, `clique.c` and networkx or the separate C program `gen0.c` (or `linear0.c` for colourings given by a length vector).
- VERIFIED (symmetry-reduced): the same, but on a smaller problem that uses automorphisms of the object. The automorphisms and their orbits were checked on the object itself before the reduction was used.
- VERIFIED (by proof: citation): one half, one colour or the whole row follows from a published theorem, cited with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by both checkers. Where a whole row rests on a theorem, the object was rebuilt from its inputs and matched byte for byte. The certificates are in `phase2/certificates/`.
- VERIFIED (witness found here by search): the witness, or the input it is built from, was found here by a search run under the rules below, and every colour of the witness was checked by both checkers on the whole object, with negative controls.
- PARTIAL: one check is missing, as stated in the row. RECIPE ONLY: the construction is written down or built, and not checked. NOT REPRODUCED: the construction as described could not be reproduced from the paper here (`phase2/NOTES.md`). STILL NO FILE: no public witness was found.
- Credit for every construction goes to the authors named in the row. The survey reference is kept for each cell, and where the witness comes from a different paper the row names it (`phase2/NOTES.md`, section 4).

86 witness files (2,544,330 bytes in all, compressed) are in `phase2/witnesses/`, each with its SHA-256, source and licence or credit in `phase2/witnesses/manifest.csv`. The checks behind each label are summarised in `phase2/CHECKS.md`, with the logs in `phase2/checks/logs/`. `python3 phase2/check_phase2.py` reruns the repository checker on every witness file.

**Searches.** Searching for new witnesses was outside the original registration. It was allowed later by two amendments, and every row whose witness was found by search says so. Amendment 2 (7 November) kept three witnesses found by short searches, R(4,10), R(5,8) and R(4,17), labelled as such. Amendment 6 (12 November) allowed a search for the lost cells, with these rules: runs in the cloud only, each restartable and under 10 minutes, at most 2 cores at low priority. About one day of computing per target, and a target is dropped once three independent methods have stopped improving. Methods are cyclic, block-cyclic and Cayley ansatzes, annealing, and SAT with clique clauses added lazily. Third-party code only from its public source, with its commit recorded. Every find is checked with both checkers like any other witness and labelled "witness found here by search". Nothing is published or sent as part of the search. Under Amendment 6 a cyclic (3,3,7;80) colouring was found by SAT on Z_80. With Robertson's construction it gives the 246-vertex witness for R(3,3,3,7) >= 247 (`phase2/NOTES.md`, section 5).

Observations made on the way (a misprint in Shearer 1986, three constructions that could not be reproduced from the text, and third-party claims above the survey, which are noted and not counted) are in `phase2/NOTES.md`.

Two rows are PARTIAL (R(7,21), R(9,9,9,9)): each row says which check is missing.
