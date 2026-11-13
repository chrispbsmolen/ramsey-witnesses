## Phase 2 (12 November 2026)

On 4 November 105 cells of the table above had no public witness (32 RECIPE, 73 NO_FILE_FOUND). Phase 2 built the published constructions for these cells, looked again for public files, and checked what was found or built. For three cells, R(4,10), R(5,8) and R(4,17), the published colouring is not public, and the witness here was found by a short search. Those rows, and R(6,15) and R(7,18), which are built from two of them, say so. Everything is in `phase2/`, with one row per cell in `phase2/coverage.csv` and `phase2/COVERAGE.md`.

| status on 12 November | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED | 10 | 27 | 37 |
| VERIFIED (symmetry-reduced) | 14 | 6 | 20 |
| VERIFIED (by proof: citation) | 18 | 3 | 21 |
| PARTIAL | 1 | 0 | 1 |
| RECIPE ONLY | 5 | 6 | 11 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 4 | 6 | 10 |
| all | 55 | 50 | 105 |

- VERIFIED: every half (every colour) of the witness was checked here by two independent exact checkers, `clique.c` and networkx or the separate C program `gen0.c` (or `linear0.c` for colourings given by a length vector).
- VERIFIED (symmetry-reduced): the same, but on a smaller problem that uses automorphisms of the object. The automorphisms and their orbits were checked on the object itself before the reduction was used.
- VERIFIED (by proof: citation): one half, one colour or the whole row follows from a published theorem, cited with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by both checkers. Where a whole row rests on a theorem, the object was rebuilt from its inputs and matched byte for byte. The certificates are in `phase2/certificates/`.
- PARTIAL: one check is missing, as stated in the row. RECIPE ONLY: the construction is written down or built, and not checked. NOT REPRODUCED: the construction as described could not be reproduced from the paper here (`phase2/NOTES.md`). STILL NO FILE: no public witness was found.
- Credit for every construction goes to the authors named in the row. The survey reference is kept for each cell, and where the witness comes from a different paper the row names it (`phase2/NOTES.md`, section 4).

79 witness files (2,457,784 bytes in all, compressed) are in `phase2/witnesses/`, each with its SHA-256, source and licence or credit in `phase2/witnesses/manifest.csv`. The checks behind each label are summarised in `phase2/CHECKS.md`, with the logs in `phase2/checks/logs/`. `python3 phase2/check_phase2.py` reruns the repository checker on every witness file.

Observations made on the way (a misprint in Shearer 1986, three constructions that could not be reproduced from the text, and third-party claims above the survey, which are noted and not counted) are in `phase2/NOTES.md`.

Six large multicolour cells (R(7,7,7,7), R(8,8,8,8), R(9,9,9,9), R(6,6,6,6,6), R(5,5,5,5,5,5), R(6,6,6,6,6,6)) are being checked in a run that has not finished. Their rows stay RECIPE ONLY until it does.
