## Phase 2 (updated 21 November 2026)

On 4 November 105 cells of the table above had no public witness (32 RECIPE, 73 NO_FILE_FOUND). Phase 2 built the published constructions for these cells, looked again for public files, and checked what was found or built. For three cells, R(4,10), R(5,8) and R(4,17), the published coloring is not public, and the witness here was found by a short search. Those rows, and R(6,15) and R(7,18), which are built from two of them, say so. For R(3,3,3,7) the input coloring needed by the published construction is not public, and a registered search found one (see below). For R(3,14) the witness is the graph of the author the survey cites, Kolodyazhny, read from archived copies of his page. For R(6,13), R(3,3,7), R(3,3,8), R(3,4,6) and R(3,3,3,4) the witness is the coloring of the author the survey cites, sent by him on request in November 2026 (Eugene Kuznetsov and Geoffrey Exoo) and credited to him as personal communication. Everything is in `phase2/`, with one row per cell in `phase2/coverage.csv` and `phase2/COVERAGE.md`.

| status on 16 November | two-color | multicolor | total |
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

- VERIFIED: every half (every color) of the witness was checked here by two independent exact checkers, `clique.c` and networkx or the separate C program `gen0.c` (or `linear0.c` for colorings given by a length vector).
- VERIFIED (symmetry-reduced): the same, but on a smaller problem that uses automorphisms of the object. The automorphisms and their orbits were checked on the object itself before the reduction was used.
- VERIFIED (by proof: citation): one half, one color or the whole row follows from a published theorem, cited with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by both checkers. Where a whole row rests on a theorem, the object was rebuilt from its inputs and matched byte for byte. The certificates are in `phase2/certificates/`.
- VERIFIED (witness found here by search): the witness, or the input it is built from, was found here by a search (Amendment 2 or 6, see below), and every color of the witness was checked by both checkers, on the whole object or with a reduction verified on the object, as the row says.
- PARTIAL: one check is missing, as stated in the row. RECIPE ONLY: the construction is written down or built, and not checked. NOT REPRODUCED: the construction as described could not be reproduced from the paper here (`phase2/NOTES.md`). STILL NO FILE: no public witness was found.
- Credit for every construction goes to the authors named in the row. The survey reference is kept for each cell, and where the witness comes from a different paper the row names it (`phase2/NOTES.md`, section 4).

95 witness files (3,234,073 bytes in all, compressed) are in `phase2/witnesses/`, each with its SHA-256, source and license or credit in `phase2/witnesses/manifest.csv`. The checks behind each label are summarized in `phase2/CHECKS.md`, with the logs in `phase2/checks/logs/`. `python3 phase2/check_phase2.py` reruns the repository checker on every witness file.

**Searches.** Searching for new witnesses was outside the original registration. It was allowed later by two amendments, and every row whose witness was found by search says so. Amendment 2 (7 November) kept three witnesses found by short searches, R(4,10), R(5,8) and R(4,17), with this label. Amendment 6 (12 November) allowed a search for the lost cells, with these rules: runs in the cloud only, each restartable and under 10 minutes, at most 2 cores at low priority. About one day of computing per target, and a target is dropped once three independent methods have stopped improving. Methods are cyclic, block-cyclic and Cayley ansatzes, annealing, and SAT with clique clauses added lazily. Third-party code only from its public source, with its commit recorded. Every find is checked with both checkers like any other witness and labeled "witness found here by search". Nothing is published or sent as part of the search. Under Amendment 6 a cyclic (3,3,7;80) coloring was found by SAT on Z_80. With Robertson's construction it gives the 246-vertex witness for R(3,3,3,7) >= 247 (`phase2/NOTES.md`, section 5, and `phase2/search_s1/SEARCH_RECORD.md`). The search ended on 13 November with no witness for another cell. For each target `phase2/search_s1/SEARCH_RECORD.md` lists the symmetric forms that were excluded exactly (for example, there is no (3,14;66) Cayley graph on any group of order 66) and the runs that ended undecided.

Observations made on the way (a misprint in Shearer 1986, three constructions that could not be reproduced from the text, third-party claims above the survey, which are noted and not counted, and what the search for unpublished colorings covered) are in `phase2/NOTES.md`.

No row is PARTIAL.

**A witness above the survey's table.** One witness above the survey's table was added on 21 November. It is not one of the 105 cells. Table XIb of the survey lists R(3,3,16) >= 291 [ExT], and that value has a public witness, checked in phase 1. The survey's item 6.2.g (p.58), R(3,k,l) >= 4R(k,l-1) - 3 [XuX2, XXER], with its own entry R(3,15) >= 74 [Kol2] (Tables Ia and IIa), gives 4 * 74 - 3 = 293. `phase2/witnesses/R3_3_16_n292.colormat.gz` is a 3-coloring of K_292 with no triangle in colors 1 and 2 and no K_16 in color 3, so R(3,3,16) >= 293. It was built here by the construction in the proof of Theorem 7 of Xu, Xie, Exoo and Radziszowski (Electron. J. Combin. 11 (2004) #R35, pp.11-12) from Kolodyazhny's (3,15;73) graph, read from the same archived page as the R(3,14) graph. Every color was checked on the whole graph by `clique.c` and `gen0.c`, with controls. This is not a new bound. It is a checked, explicit coloring for the value the survey's own items give. The row is in `phase2/above_survey.csv` and `phase2/COVERAGE.md`, and the logs are in `phase2/checks/logs/build_r3316_292/`.
