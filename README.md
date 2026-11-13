# ramsey-witnesses

An exact checker for lower-bound witnesses of small Ramsey numbers, the results of running it on the public
witness files found, and a table of every lower bound in Radziszowski's dynamic survey *Small Ramsey Numbers*
(Electron. J. Combin. DS1, revision 18, 24 April 2026) with whether a public witness for it was verified here.

A witness for R(k_1, ..., k_r) >= n + 1 is a colouring of the edges of K_n with r colours and no K_(k_i) in
colour i; for two colours, a graph on n vertices with no K_k and no independent set of size l. `verify_ramsey.py`
decides this exactly: for each colour class the C program `clique.c` (bitset branch and bound with greedy-colouring
bounds) searches for a clique of the forbidden size. `selftest.py` checks the solver against networkx on random
graphs and on planted cliques and corrupted witnesses; `crosscheck.py` rechecks some witnesses with networkx, which
shares no solver code with `clique.c`.

The results below are those of 4 November 2026. Phase 2 (13 November 2026) adds witnesses, checks and notes for the
105 cells that had no public witness then. It is summarised in the section Phase 2 below and kept in `phase2/`.

## Results

213 witnesses are listed in `sources/manifest.csv` (32 of them are in this repository; the others are
downloaded from their original URLs by `fetch_data.py`, and all 181 downloads matched the recorded SHA-256, `results/fetch_log.txt`).
Verdicts (`results/ledger.csv`, one row per witness file or per entry of a file holding several):

| verdict | witnesses |
|---|---|
| PASS: every colour class checked, no forbidden clique | 184 |
| PARTIAL: only some colour classes checked, those passed | 3 |
| NOT_COMPLETED: check started, stopped at the time limit | 1 |
| NOT_CHECKED: located, no check run here | 25 |
| FAIL | 0 |

McKay's files hold many graphs each; counting every graph checked, 12,492 graphs passed.

Every lower bound in the survey's tables Ia, IIa, IIb, IIc, XIa, XIb and the bounds listed in its section 6.1
(`results/coverage.csv`, 204 cells with a lower bound L; a witness needs L - 1 vertices):

| cells | VERIFIED | PARTIAL | RECIPE | NO_FILE_FOUND | total |
|---|---|---|---|---|---|
| two-colour, k <= l <= 15 | 46 | 2 | 13 | 6 | 67 |
| two-colour, l > 15 | 19 | 18 | 11 | 25 | 73 |
| multicolour | 14 | 0 | 8 | 42 | 64 |

- VERIFIED: a witness of at least the survey's strength passed here.
- PARTIAL: a public witness of that strength was found, but its check here is incomplete or was not run.
- RECIPE: no witness file of that strength was found; the survey or the cited paper describes a construction.
- NO_FILE_FOUND: the survey gives this bound with its reference; no public witness file was found here. This says
  nothing about the bound itself. (Sources searched: `sources/sources.csv`.)

Only witnesses for exactly the cell's parameters are counted. The survey is the reference point only; these are
statements about public files, checked on the dates in `results/VERIFICATION.md`.

### Public witnesses above the survey's table

These witness files passed here and give a larger lower bound than the survey's table entry:

| number | bound from the witness | survey (table) | source | where claimed | witness |
|---|---|---|---|---|---|
| R(4,15) | 163 | 159 (Ia; IIa lists 158) | alphaevolve | repository file only (paper claims 159) | `alphaevolve/R(4, 15) >= 163.txt` |
| R(6,8) | 135 | 134 (Ia) | fritzcremer | arXiv:2610.12122 (October 2026), repository README | `fritzcremer/R6_8/n134-gpt-6.1-sol.g6` |
| R(3,17) | 93 | 92 (IIa) | alphaevolve | repository file only (the paper's table lists 92) | `alphaevolve/R(3, 17) >= 93.txt` |
| R(4,16) | 174 | 170 (IIa) | alphaevolve | NaRT v5 abstract (arXiv:2603.09172v5) | `alphaevolve/R(4, 16) >= 174.txt` |
| R(4,18) | 209 | 205 (IIa) | alphaevolve | NaRT v5 abstract (arXiv:2603.09172v5) | `alphaevolve/R(4, 18) >= 209.txt` |
| R(4,19) | 219 | 213 (IIa) | alphaevolve | NaRT v5 abstract (arXiv:2603.09172v5) | `alphaevolve/R(4, 19) >= 219.txt` |
| R(4,20) | 237 | 234 (IIa) | alphaevolve | NaRT v5 abstract (arXiv:2603.09172v5) | `alphaevolve/R(4, 20) >= 237.txt` |
| R(4,21) | 244 | 242 (IIa) | alphaevolve | repository file only (not in the paper) | `alphaevolve/R(4,21)>=244.txt` |
| R(3,24) | 151 | 143 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_24_graphSize_150.clq` |
| R(3,25) | 160 | 154 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_25_graphSize_159.clq` |
| R(3,26) | 163 | 161 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_26_graphSize_162.clq` |
| R(3,28) | 181 | 179 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_28_graphSize_180.clq` |
| R(3,29) | 194 | 190 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_29_graphSize_193.clq` |
| R(3,30) | 199 | 197 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_30_graphSize_198.clq` |
| R(3,31) | 210 | 208 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_31_graphSize_209.clq` |
| R(3,32) | 219 | 217 (IIb) | furini_certificates | arXiv:2608.18769v1 (19 August 2026), Table 7 | `furini/R_3_32_graphSize_218.clq` |
| R(3,3,9) | 133 | 129 (XIb) | lachy_dauth | preprint and README in the repository (commit of 26 October 2026) | `lachy_dauth/circulants.json#0` |
| R(3,3,11) | 183 | 174 (XIb) | lachy_dauth | preprint and README in the repository (commit of 26 October 2026) | `lachy_dauth/circulants.json#1` |
| R(3,3,12) | 203 | 194 (XIb) | lachy_dauth | preprint and README in the repository (commit of 26 October 2026) | `lachy_dauth/circulants.json#2` |
| R(3,3,13) | 232 | 217 (XIb) | lachy_dauth | preprint and README in the repository (commit of 26 October 2026) | `lachy_dauth/circulants.json#3` |
| R(3,3,14) | 267 | 242 (XIb) | lachy_dauth | preprint and README in the repository (commit of 26 October 2026) | `lachy_dauth/circulants.json#4` |

Survey revision 18 is dated 24 April 2026. The files of Coniglio, Furini et al. (arXiv:2608.18769, August 2026),
of fritzcremer/ramsey-lower-bounds (arXiv:2610.12122, October 2026) and of Lachy-Dauth/ramsey-neighbourhood-counting
(repository commit of 26 October 2026) appeared after it, and the AlphaEvolve values above are those of the
repository files and of version 5 of arXiv:2603.09172, not the values the survey cites. So this list is of files
newer than the survey or not cited in it, not of omissions from the survey.

### Witnesses for cells the survey leaves blank

| number | bound from the witness | witness | checked |
|---|---|---|---|
| R(8,12) | 511 | `alphaevolve/R(8, 12) >= 511.txt` | no K_8 and no independent 12-set (two separate processes) |
| R(9,11) | 617 | `alphaevolve/R(9, 11) >= 617.txt` | no K_9 and no independent 11-set (two separate processes) |

### Public files above the survey that were not fully checked here

| number | bound the file would give | survey | witness | check here |
|---|---|---|---|---|
| R(7,13) | 513 | 511 | `alphaevolve/R(7, 13) >= 513.txt` | PARTIAL: no K_7 only |
| R(8,10) | 345 | 343 | `fritzcremer/R8_10/n344-gpt-6.1-sol-1.g6` | NOT_CHECKED: none |
| R(10,12) | 856 | blank | `alphaevolve/R(10, 12) >= 856.txt` | PARTIAL: no K_10 only |
| R(8,18) | 1,052 | 1,049 | `alphaevolve/R(8, 18) >= 1052.txt` | PARTIAL: no K_8 only |
| R(3,33) | 230 | 227 | `furini/R_3_33_graphSize_229.clq` | NOT_CHECKED: none |
| R(3,34) | 239 | 234 | `furini/R_3_34_graphSize_238.clq` | NOT_CHECKED: none |
| R(3,35) | 253 | 248 | `furini/R_3_35_graphSize_252.clq` | NOT_CHECKED: none |
| R(3,36) | 261 | 255 | `furini/R_3_36_graphSize_260.clq` | NOT_CHECKED: none |
| R(3,37) | 272 | 267 | `furini/R_3_37_graphSize_271.clq` | NOT_CHECKED: none |
| R(3,38) | 281 | 278 | `furini/R_3_38_graphSize_280.clq` | NOT_CHECKED: none |
| R(3,39) | 294 | 290 | `furini/R_3_39_graphSize_293.clq` | NOT_CHECKED: none |
| R(3,40) | 305 | 298 | `furini/R_3_40_graphSize_304.clq` | NOT_CHECKED: none |
| R(3,41) | 317 | 311 | `furini/R_3_41_graphSize_316.clq` | NOT_CHECKED: none |
| R(3,42) | 327 | 320 | `furini/R_3_42_graphSize_326.clq` | NOT_CHECKED: none |
| R(3,43) | 340 | 333 | `furini/R_3_43_graphSize_339.clq` | NOT_CHECKED: none |
| R(3,44) | 348 | 339 | `furini/R_3_44_graphSize_347.clq` | NOT_CHECKED: none |
| R(3,45) | 364 | 354 | `furini/R_3_45_graphSize_363.clq` | NOT_CHECKED: none |
| R(3,46) | 371 | 362 | `furini/R_3_46_graphSize_370.clq` | NOT_CHECKED: none |
| R(3,47) | 385 | 380 | `furini/R_3_47_graphSize_384.clq` | NOT_CHECKED: none |
| R(3,48) | 391 | 384 | `furini/R_3_48_graphSize_390.clq` | NOT_CHECKED: none |
| R(3,49) | 411 | 402 | `furini/R_3_49_graphSize_410.clq` | NOT_CHECKED: none |
| R(3,3,15) | 278 | 269 | `lachy_dauth/R_3_3_15_n277_compact.json` | NOT_CHECKED: none |

An unlisted file g1212.1640 (1640 vertices) is also in Tatarevic's graphs/ folder; its author claims nothing for it, and it was not checked here.

### Survey lower bounds with no public witness found on 4 November 2026

The section Phase 2 below gives the status of each of these cells on 13 November 2026.

No witness file of the survey's strength was found for these (in brackets the survey's reference; "recipe" marks
a construction described in the survey or the cited paper). Two-colour with k <= l <= 15 (19): R(3,14) >= 67 [Kol2], R(4,10) >= 92 [HaKr1], R(5,7) >= 80 [CaET], R(5,8) >= 101 [HaKr1], R(5,15) >= 275 [2.3.h] (recipe), R(6,13) >= 347 [Kuz], R(6,15) >= 401 [2.3.i] (recipe), R(7,11) >= 405 [XXER] (recipe), R(7,12) >= 417 [XSR2] (recipe), R(8,9) >= 329 [Kuz], R(8,11) >= 457 [2.3.i] (recipe), R(8,13) >= 817 [XXER] (recipe), R(8,15) >= 873 [2.3.i] (recipe), R(9,10) >= 581 [XSR2] (recipe), R(10,15) >= 1,313 [2.3.i] (recipe), R(11,11) >= 1,597 [2.2.c] (recipe), R(13,13) >= 2,557 [2.2.c] (recipe), R(14,14) >= 2,989 [2.2.c] (recipe), R(15,15) >= 5,485 [2.2.c] (recipe).

Two-colour with l > 15 (36): R(16,16) >= 5,605 [2.2.c] (recipe), R(17,17) >= 8,917 [LuSL], R(18,18) >= 11,005 [LuSL], R(19,19) >= 17,885 [LuSL], R(20,20) >= 21,725 [Ex23], R(21,21) >= 30,925 [Ex23], R(22,22) >= 39,109 [Ex23], R(23,23) >= 49,421 [Ex23], R(3,21) >= 122 [W1+], R(3,22) >= 131 [W2+], R(3,23) >= 139 [XWCS], R(4,17) >= 200 [Lia+], R(4,22) >= 314 [LinCa], R(5,17) >= 388 [XSR2], R(5,18) >= 396 [2.3.h] (recipe), R(5,19) >= 411 [XSR2], R(5,20) >= 424 [XSR2], R(5,21) >= 441 [2.3.i] (recipe), R(5,22) >= 492 [Ihr], R(5,23) >= 521 [2.3.i] (recipe), R(6,16) >= 434 [SLLL], R(6,17) >= 548 [SLLL], R(6,18) >= 614 [SLLL], R(6,19) >= 710 [SLLL], R(6,20) >= 878 [SLLL], R(6,21) >= 888 [2.3.h] (recipe), R(6,22) >= 1,070 [SLLL], R(7,16) >= 629 [2.3.i] (recipe), R(7,17) >= 729 [2.3.i] (recipe), R(7,18) >= 797 [2.3.i] (recipe), R(7,19) >= 908 [SLLL], R(7,21) >= 1,214 [SLLL], R(8,17) >= 1,005 [2.3.i] (recipe), R(8,19) >= 1,237 [2.2.h] (recipe), R(8,21) >= 1,617 [2.3.i] (recipe), R(3,27) >= 172 [LiLi].

Multicolour (50): R(5,5,5) >= 454 [Ex23], R(6,6,6) >= 1,106 [Row3], R(7,7,7) >= 3,214 [XuR1] (recipe), R(8,8,8) >= 7,174 [Row5], R(9,9,9) >= 15,041 [Row5], R(10,10,10) >= 23,094 [Row5], R(3,3,3,3) >= 51 [Chu1] (recipe), R(4,4,4,4) >= 634 [XXER], R(5,5,5,5) >= 4,073 [Row3], R(6,6,6,6) >= 23,502 [Row5], R(7,7,7,7) >= 94,874 [Row5], R(8,8,8,8) >= 182,002 [Row5], R(9,9,9,9) >= 719,204 [Row5], R(3,3,3,3,3) >= 162 [Ex10], R(4,4,4,4,4) >= 4,176 [Row1], R(5,5,5,5,5) >= 41,626 [Row5], R(6,6,6,6,6) >= 258,506 [Row5], R(3,3,3,3,3,3) >= 538 [FreSw], R(4,4,4,4,4,4) >= 32,006 [Row1], R(5,5,5,5,5,5) >= 441,606 [Row5], R(3,3,3,3,3,3,3) >= 1,698 [Row4], R(4,4,4,4,4,4,4) >= 160,024 [Row1], R(3,3,3,3,3,3,3,3) >= 5,288 [Row3], R(3,3,3,3,3,3,3,3,3) >= 17,805 [AgCP+], R(3,3,4) >= 30 [Ka2], R(3,3,5) >= 45 [Ex2], R(3,3,7) >= 85 [Ex18], R(3,3,8) >= 103 [Ex18], R(3,4,4) >= 55 [KrLR], R(3,4,6) >= 117 [Ex17], R(3,4,8) >= 193 [6.2.g] (recipe), R(3,5,5) >= 139 [Ex17], R(3,5,6) >= 181 [Ex17], R(3,5,7) >= 241 [6.2.g] (recipe), R(3,3,3,4) >= 97 [Ex17], R(3,3,4,4) >= 174 [Row2], R(3,4,4,4) >= 381 [6.2.j] (recipe), R(3,3,3,5) >= 162 [XXER], R(3,3,3,10) >= 513 [6.2.g] (recipe), R(3,3,3,11) >= 597 [6.2.g] (recipe), R(3,4,5,5) >= 729 [Row2], R(3,5,5,5) >= 1,430 [Row5], R(3,6,6) >= 338 [Row5], R(3,7,7) >= 674 [Row5], R(3,8,8) >= 941 [Row5], R(3,9,9) >= 1,844 [Row5], R(3,10,10) >= 2,841 [Row5], R(8,8,9) >= 10,769 [Row5], R(6,6,6,6,6,6) >= 4,515,702 [Row2/Row3 (linear Ramsey graphs)], R(3,3,3,7) >= 247 [6.2.h (derived, unpublished explicit)] (recipe).

### Witnesses constructed here

`constructions/build.py` builds these deterministically (Paley graphs Q_p and the doubling of Q_p on 2p + 2 vertices
described in the survey, the 5-cycle, the GF(16) cube-coset colouring of K_16, the cubic-residue graph on Z_127 and the cube-coset colouring
of K_127):

| file | number | bound | vertices | verdict |
|---|---|---|---|---|
| `constructions/witnesses/c5_R3_3.g6` | R(3,3) | 6 | 5 | PASS |
| `constructions/witnesses/clebsch16_R3_3_3.txt` | R(3,3,3) | 17 | 16 | PASS |
| `constructions/witnesses/cubic127_R4_12.g6` | R(4,12) | 128 | 127 | PASS |
| `constructions/witnesses/cubic3_127_R4_4_4.txt` | R(4,4,4) | 128 | 127 | PASS |
| `constructions/witnesses/paley101_R6_6.g6` | R(6,6) | 102 | 101 | PASS |
| `constructions/witnesses/mathon101_R7_7.g6` | R(7,7) | 205 | 204 | PASS |
| `constructions/witnesses/paley281_R8_8.g6` | R(8,8) | 282 | 281 | PASS |
| `constructions/witnesses/mathon281_R9_9.g6` | R(9,9) | 565 | 564 | PASS |
| `constructions/witnesses/paley797_R10_10.g6` | R(10,10) | 798 | 797 | PASS |

`constructions/paley_omega.py` computes the clique numbers of larger Paley graphs exactly (Q_101 has clique number 5; Q_281 has clique number 7; Q_797 has clique number 9; Q_1277 has clique number 11; Q_1493 has clique number 12; Q_2741 has clique number 13); with the doubling
construction these give the survey's bounds for R(11,11), R(13,13), R(14,14), R(15,15), whose graphs were not built or checked here by 4 November (status RECIPE). Phase 2 built them, and their status on 13 November is in the section Phase 2.

## Phase 2 (13 November 2026)

On 4 November 105 cells of the table above had no public witness (32 RECIPE, 73 NO_FILE_FOUND). Phase 2 built the published constructions for these cells, looked again for public files, and checked what was found or built. For three cells, R(4,10), R(5,8) and R(4,17), the published colouring is not public, and the witness here was found by a short search. Those rows, and R(6,15) and R(7,18), which are built from two of them, say so. For R(3,3,3,7) the input colouring needed by the published construction is not public, and a registered search found one (see below). For R(3,14) the witness is the graph of the author the survey cites, Kolodyazhny, read from archived copies of his page. Everything is in `phase2/`, with one row per cell in `phase2/coverage.csv` and `phase2/COVERAGE.md`.

| status on 13 November | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED | 8 | 27 | 35 |
| VERIFIED (symmetry-reduced) | 14 | 6 | 20 |
| VERIFIED (by proof: citation) | 18 | 9 | 27 |
| VERIFIED (witness found here by search) | 3 | 1 | 4 |
| PARTIAL | 1 | 0 | 1 |
| RECIPE ONLY | 5 | 0 | 5 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 3 | 5 | 8 |
| all | 55 | 50 | 105 |

- VERIFIED: every half (every colour) of the witness was checked here by two independent exact checkers, `clique.c` and networkx or the separate C program `gen0.c` (or `linear0.c` for colourings given by a length vector).
- VERIFIED (symmetry-reduced): the same, but on a smaller problem that uses automorphisms of the object. The automorphisms and their orbits were checked on the object itself before the reduction was used.
- VERIFIED (by proof: citation): one half, one colour or the whole row follows from a published theorem, cited with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by both checkers. Where a whole row rests on a theorem, the object was rebuilt from its inputs and matched byte for byte. The certificates are in `phase2/certificates/`.
- VERIFIED (witness found here by search): the witness, or the input it is built from, was found here by a search (Amendment 2 or 6, see below), and every colour of the witness was checked by both checkers, on the whole object or with a reduction verified on the object, as the row says.
- PARTIAL: one check is missing, as stated in the row. RECIPE ONLY: the construction is written down or built, and not checked. NOT REPRODUCED: the construction as described could not be reproduced from the paper here (`phase2/NOTES.md`). STILL NO FILE: no public witness was found.
- Credit for every construction goes to the authors named in the row. The survey reference is kept for each cell, and where the witness comes from a different paper the row names it (`phase2/NOTES.md`, section 4).

87 witness files (2,545,003 bytes in all, compressed) are in `phase2/witnesses/`, each with its SHA-256, source and licence or credit in `phase2/witnesses/manifest.csv`. The checks behind each label are summarised in `phase2/CHECKS.md`, with the logs in `phase2/checks/logs/`. `python3 phase2/check_phase2.py` reruns the repository checker on every witness file.

**Searches.** Searching for new witnesses was outside the original registration. It was allowed later by two amendments, and every row whose witness was found by search says so. Amendment 2 (7 November) kept three witnesses found by short searches, R(4,10), R(5,8) and R(4,17), with this label. Amendment 6 (12 November) allowed a search for the lost cells, with these rules: runs in the cloud only, each restartable and under 10 minutes, at most 2 cores at low priority. About one day of computing per target, and a target is dropped once three independent methods have stopped improving. Methods are cyclic, block-cyclic and Cayley ansatzes, annealing, and SAT with clique clauses added lazily. Third-party code only from its public source, with its commit recorded. Every find is checked with both checkers like any other witness and labelled "witness found here by search". Nothing is published or sent as part of the search. Under Amendment 6 a cyclic (3,3,7;80) colouring was found by SAT on Z_80. With Robertson's construction it gives the 246-vertex witness for R(3,3,3,7) >= 247 (`phase2/NOTES.md`, section 5, and `phase2/search_s1/SEARCH_RECORD.md`). The search ended on 13 November with no witness for another cell. For each target `phase2/search_s1/SEARCH_RECORD.md` lists the symmetric forms that were excluded exactly (for example, there is no (3,14;66) Cayley graph on any group of order 66) and the runs that ended undecided.

Observations made on the way (a misprint in Shearer 1986, three constructions that could not be reproduced from the text, third-party claims above the survey, which are noted and not counted, and what the search for unpublished colourings covered) are in `phase2/NOTES.md`.

One row is PARTIAL (R(7,21)): the row says which check is missing.

## Usage

Python 3 with numpy and networkx (`requirements.txt`), a C compiler (`clique.c` is compiled on first use) and,
for Kuznetsov's circulants, `pdftotext` from poppler. Run every script from the repository root.

```
python3 selftest.py                    # results/selftest_output.txt
python3 verify_ramsey.py FORMAT FILE K1,K2[,...] [INDEX]
python3 fetch_data.py [SOURCE ...]     # data/ (about 63 MB), results/fetch_log.txt
python3 run_ramsey.py RUN [--quick] [--max-n N] [--source S ...] [--id ID ...]   # results/runs/RUN.jsonl
python3 crosscheck.py                  # results/crosscheck_output.txt
python3 constructions/build.py         # rebuilds constructions/witnesses/
python3 make_ledger.py                 # results/ledger.csv, coverage.csv, summary.json
python3 make_readme.py                 # this file and results/VERIFICATION.md
python3 phase2/make_phase2.py          # phase2/COVERAGE.md, phase2/CHECKS.md, phase2/summary.json (run before make_readme.py)
python3 phase2/check_phase2.py         # phase2/results/: the repository checker on every phase-2 witness file
```

A full `run_ramsey.py` without `--quick` takes hours: the cloud run took about 4,500 s in all, with a
time limit of 1800 s per file, and the independence halves of the large AlphaEvolve witnesses took up to about
49 minutes each on a separate machine (`tools/run_hard.py`).

`survey/` holds the survey's lower bounds as extracted from the tables (with their reference tags) and
`survey/search_notes.csv` the notes from the search for each witness. `tools/run_hard.py` is the script used for
the large AlphaEvolve witnesses on a separate machine.

## Sources and licences

| source | where | licence found | here |
|---|---|---|---|
| Brendan McKay's Ramsey graph data | https://users.cecs.anu.edu.au/~bdm/data/ramsey.html | none stated | not redistributed; fetch_data.py downloads the graph6 files |
| Geoffrey Exoo's Ramsey constructions page | https://cs.indstate.edu/ge/RAMSEY/ | none stated | not redistributed; fetched |
| Exoo and Tatarevic, New Lower Bounds for 28 Classical Ramsey Numbers, Electron. J. Combin. 22(3) (2015) #P3.11, data file | https://www.combinatorics.org/ojs/index.php/eljc/article/view/v22i3p11 | none stated for the data file | not redistributed; fetched (one zip) |
| Milos Tatarevic's graphs | https://github.com/milostatarevic/ramsey-numbers (commit f3e9b7009f78ce24ddbc140df5141725bb85a7fa) | no licence file | not redistributed; fetched |
| Kuznetsov, Computational lower limits on small Ramsey numbers, arXiv:1505.07186v5, Table 2 | https://arxiv.org/abs/1505.07186v5 | arXiv licence of the paper; treated as not redistributable | not redistributed; fetch_data.py extracts the circulants from the PDF |
| Coniglio, Furini, Ljubic, San Segundo, Thuerauf, Traversi, certificates (arXiv:2608.18769) | https://github.com/fabiofurini/ramsey-number-lower-bounds (commit 0b53ca478bec9f9aa6c64e33c8b9b0088bafd9e8) | GPL-3.0 licence file in the repository | not redistributed; fetched |
| Nagda, Raghavan and Thakurta (AlphaEvolve), arXiv:2603.09172, witness matrices | https://github.com/google-research/google-research/tree/master/ramsey_number_bounds (commit 83f1e7b59e762648c953de751d31f75720683622) | repository README: datasets CC BY 4.0, source files Apache 2.0 | committed unchanged in third_party/google-research/ with attribution |
| Lachlan Dauth, Neighbourhood counting and new bounds for small three-colour Ramsey numbers (preprint), ancillary data | https://github.com/Lachy-Dauth/ramsey-neighbourhood-counting (commit 5770baac746878a3a63b9720fdda97726fe02851) | MIT (code and data) | circulants.json committed unchanged in third_party/lachy-dauth/ with its LICENSE; the 277-vertex R(3,3,15) file is fetched |
| witness graphs in the GitHub repository fritzcremer/ramsey-lower-bounds (arXiv:2610.12122) | https://github.com/fritzcremer/ramsey-lower-bounds (commit 9382a5eb8e6ec634873cea0850b133764e0eecbf) | CC BY 4.0 | not redistributed; fetched |
| Paley graphs, the doubling of Paley graphs on 2p+2 vertices, the 5-cycle, the GF(16) colouring, the cubic-residue graph on Z_127 and the cube-coset colouring of Z_127, built by constructions/build.py | constructions/ | MIT (this repository) | committed as graph6 (colour matrices for the two cube-coset colourings) |

Files of the other sources are identified by URL and SHA-256 in `sources/manifest.csv` and are not
redistributed. The survey and the papers are not included.

The phase-2 witness files are listed with their source, page or table, licence or credit in
`phase2/witnesses/manifest.csv` and `phase2/coverage.csv`. They use the constructions and data of:

- Calkin, Erdos and Tovey
- Kolodyazhny
- Kuznetsov
- Wu, Su, Luo and Xu
- Lindsay and Cain
- Ihringer
- Su, Li, Luo and Li
- Li Mingbo and Li Yusheng
- Xu, Xie, Exoo and Radziszowski
- Xu, Shao and Radziszowski
- Xu and Radziszowski
- Shearer, and Mathon
- Luo, Su and Li
- Paley, Kalbfleisch, Hill and Irving, Giraud, Chung, and Robertson
- Exoo, Exoo and Tatarevic, and Tatarevic
- Rowley
- Courties
- Fredricksen and Sweet
- Ageron, Casteras, Pellerin, Portella, Rimmel and Tomasik
- Codish, Frank, Itzhakov and Miller
- Kreher, Li and Radziszowski
- Dauth

Please cite them for their results.

## Credit, corrections and removal

Every result here names its source; please cite the original authors for their results. Corrections, missing or
wrong credit, and requests to change or remove anything (including a request to stop linking a file) are welcome as
a GitHub issue or by email to the maintainer, Christopher Smolen (independent researcher, ORCID 0009-0002-9537-7961),
chrispbsmolen@gmail.com. A file whose author objects to its inclusion is removed. Every such change is recorded,
with its date and reason, in `CORRECTIONS.md`.

## Licence

MIT (`LICENSE`), except the files in `third_party/`, which keep their own licences (see the NOTICE file in each folder).

Christopher Smolen, November 2026.
