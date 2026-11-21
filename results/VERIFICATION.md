# Verification record

## Runs

| run | where and how | records | graphs passed (all color classes) | seconds | verifier (SHA-256 prefixes) |
|---|---|---|---|---|---|
| cloud | cloud machine, 3 November 2026, working layout (paths rewritten for this repository, per-graph records of McKay files merged per file) | 171 | 12,115 | 4483.7 | verify_ramsey.py 786a69c43a9b4b95 (working version), clique.c 34b72631979d0ebf |
| cloud_constructions | cloud machine, 3 November 2026, constructions built then | 5 | 5 | 84.8 | verify_ramsey.py 786a69c43a9b4b95 (working version), clique.c 34b72631979d0ebf |
| mac | separate machine (Mac), tools/run_hard.py, one process per half | 9 | 2 | 9869.7 | tools/run_hard.py, clique.c 34b72631979d0ebf (the copy kept on the Mac, hashed afterward) |
| repo | this repository, 4 November 2026, after fetch_data.py: run_ramsey.py repo --quick --max-n 300 (a first pass under a looser quick rule was stopped by hand during the first check of furini/R_3_33_graphSize_229.clq, which wrote no record; the run then resumed under the current rule; constructions/cubic3_127_R4_4_4.txt was added afterward with --id) | 150 | 9,455 | 45.5 | verify_ramsey.py 657db0ada9f88716, clique.c 34b72631979d0ebf |

The cloud runs used an earlier layout of the same code (`verify_ramsey.py` before it was tidied for this
repository). Every run used `clique.c` with SHA-256 34b72631979d0ebfdb871d8e04fc62a3547477aef96b945d71b91ec30a147c6c
(for the Mac run, the copy kept on that machine was hashed afterward and is identical). After all runs the header
comment of `clique.c` was corrected (it described a MAX output line the program never prints); the code is unchanged,
and the file's SHA-256 prefix is now 137a100275a4a061. The repository run rechecked 143 witnesses that the
earlier runs had also checked: 0 differences in verdict or vertex count. It also checked
7 witnesses for the first time: `constructions/c5_R3_3.g6`, `constructions/clebsch16_R3_3_3.txt`, `constructions/cubic127_R4_12.g6`, `constructions/cubic3_127_R4_4_4.txt`, `fritzcremer/R6_8/n134-gpt-6.1-sol.g6`, `mckay/r46_35some.g6`, `mckay/r55_42some.g6`.
Every record carries the SHA-256 of the file it checked, and `make_ledger.py` stops if one differs from the manifest.

## Large witnesses checked in halves

On the separate machine each half (no K_k; no independent l-set, by searching the complement) ran as its own
process with no time limit. `tools/run_hard.py` reads files named `Rk_l_geB.txt`, so the AlphaEvolve files
`R(k, l) >= B.txt` were copied under those names with their contents unchanged; its records carry the SHA-256 of
each file, and they are matched to `sources/manifest.csv` by that hash. 9 half runs are recorded, 2 of them repeats of a half with the same output.
Only what is listed was checked; the other halves were not run to completion.

| witness | verdict | checked | solver detail |
|---|---|---|---|
| `alphaevolve/R(10, 12) >= 856.txt` | PARTIAL | no K_10 only | no_clique: solver nodes 533,108,333, 119.5 s |
| `alphaevolve/R(7, 13) >= 513.txt` | PARTIAL | no K_7 only | no_clique: solver nodes 3,067,340, 0.4 s |
| `alphaevolve/R(8, 12) >= 511.txt` | PASS | no K_8 and no independent 12-set (two separate processes) | no_clique: solver nodes 2,766,956, 0.5 s; no_independent_set: solver nodes 23,627,171,346, 2955.4 s; no_independent_set: solver nodes 23,627,171,346, 2959.9 s |
| `alphaevolve/R(8, 18) >= 1052.txt` | PARTIAL | no K_8 only | no_clique: solver nodes 46,637,531, 8.9 s |
| `alphaevolve/R(9, 11) >= 617.txt` | PASS | no K_9 and no independent 11-set (two separate processes) | no_clique: solver nodes 83,254,302, 14.0 s; no_independent_set: solver nodes 11,422,587,890, 1898.4 s; no_independent_set: solver nodes 11,422,587,890, 1912.7 s |

## Not completed or not checked

| witness | number | verdict | note |
|---|---|---|---|
| `tatarevic/g1212.1639` | R(12,12) | NOT_COMPLETED | solver stopped at the 1800 s time limit |
| `tatarevic/g1212.1640` | R(12,12) | NOT_CHECKED | no check run here (in graphs/ but not listed in the README table; its author claims nothing for it) |
| `furini/R_3_33_graphSize_229.clq` | R(3,33) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_34_graphSize_238.clq` | R(3,34) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_35_graphSize_252.clq` | R(3,35) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_36_graphSize_260.clq` | R(3,36) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_37_graphSize_271.clq` | R(3,37) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_38_graphSize_280.clq` | R(3,38) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_39_graphSize_293.clq` | R(3,39) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_40_graphSize_304.clq` | R(3,40) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_41_graphSize_316.clq` | R(3,41) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_42_graphSize_326.clq` | R(3,42) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_43_graphSize_339.clq` | R(3,43) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_44_graphSize_347.clq` | R(3,44) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_45_graphSize_363.clq` | R(3,45) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_46_graphSize_370.clq` | R(3,46) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_47_graphSize_384.clq` | R(3,47) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_48_graphSize_390.clq` | R(3,48) | NOT_CHECKED | no check run here (file name gives the order) |
| `furini/R_3_49_graphSize_410.clq` | R(3,49) | NOT_CHECKED | no check run here (file name gives the order) |
| `lachy_dauth/R_3_3_15_n277_compact.json` | R(3,3,15) | NOT_CHECKED | no check run here (compact description (host circulant plus 11 vertices); this repository has no loader for it and did not check it) |
| `fritzcremer/R8_10/n343-gpt-6-pro-1.g6` | R(8,10) | NOT_CHECKED | no check run here (file name gives the order) |
| `fritzcremer/R8_10/n343-gpt-6-pro-2.g6` | R(8,10) | NOT_CHECKED | no check run here (file name gives the order) |
| `fritzcremer/R8_10/n343-gpt-6-pro-3.g6` | R(8,10) | NOT_CHECKED | no check run here (file name gives the order) |
| `fritzcremer/R8_10/n343-gpt-6.1-sol.g6` | R(8,10) | NOT_CHECKED | no check run here (file name gives the order) |
| `fritzcremer/R8_10/n344-gpt-6.1-sol-1.g6` | R(8,10) | NOT_CHECKED | no check run here (file name gives the order) |
| `fritzcremer/R8_10/n344-gpt-6.1-sol-2.g6` | R(8,10) | NOT_CHECKED | no check run here (file name gives the order) |

## Sampled graph6 files

Files with more than 3,000 graphs were sampled (all other graph6 files were checked line by line in full):

| file | graphs in file | graphs checked | selection |
|---|---|---|---|
| `mckay/r36_10.g6` | 6,657 | 202 | line numbers divisible by 33, from 0 |
| `mckay/r36_11.g6.gz` | 30,395 | 202 | line numbers divisible by 151, from 0 |
| `mckay/r36_12.g6.gz` | 116,792 | 201 | line numbers divisible by 583, from 0 |
| `mckay/r36_13.g6.gz` | 275,086 | 201 | line numbers divisible by 1375, from 0 |
| `mckay/r36_14.g6.gz` | 263,520 | 201 | line numbers divisible by 1317, from 0 |
| `mckay/r36_15.g6.gz` | 64,732 | 201 | line numbers divisible by 323, from 0 |
| `mckay/r37_21.g6.gz` | 1,118,436 | 201 | line numbers divisible by 5592, from 0 |
| `mckay/r38_27.g6.gz` | 477,142 | 201 | line numbers divisible by 2385, from 0 |
| `mckay/r44_10.g6.gz` | 103,706 | 201 | line numbers divisible by 518, from 0 |
| `mckay/r44_11.g6.gz` | 546,356 | 201 | line numbers divisible by 2731, from 0 |
| `mckay/r44_12.g6.gz` | 1,449,166 | 201 | line numbers divisible by 7245, from 0 |
| `mckay/r44_13.g6.gz` | 1,184,231 | 201 | line numbers divisible by 5921, from 0 |
| `mckay/r44_14.g6.gz` | 130,816 | 201 | line numbers divisible by 654, from 0 |
| `mckay/r44_9.g6` | 14,701 | 202 | line numbers divisible by 73, from 0 |
| `mckay/r45_24.g6` | 352,366 | 201 | line numbers divisible by 1761, from 0 |

## Checks on the checker

`selftest.py`:

```
A. oracle: 40 random graphs, disagreements 0               ok
B. planted K6 in G(80, 0.15) found                         ok
B. planted independent 12-set in G(80, 0.85) found         ok
B. Paley(101) passes R(6,6)                                ok
B. Paley(101) fails R(5,6) (its clique number is 5)        ok
B. Paley(101) with a planted K6 fails R(6,6)               ok
B. Clebsch colouring passes R(3,3,3)                       ok
B. Clebsch colouring with one edge recoloured fails        ok
B. Lachy-Dauth R(3,3,9) circulant fails as R(3,3,8)        ok
C. circulant shortcut agrees with full search, k = 4..8    ok
C. is_circulant: Paley(101) yes, Clebsch colouring no      ok
D. g6, matrix01, npmatrix, dimacs, circulant load identically ok
D. colormat loads the same partition                       ok
D. distrow: colour of ij is c[|i-j|]                       ok
E. networkx: c5_R3_3.g6 has clique number < 3 and independence number < 3 ok
E. networkx: paley101_R6_6.g6 has clique number < 6 and independence number < 6 ok
E. networkx: each colour class of clebsch16 is triangle-free ok

ALL TESTS PASS
```

`crosscheck.py` (networkx only, no shared solver code):

```
constructions/cubic127_R4_12.g6: n = 127, clique number 3 (< 4, ok), independence number 11 (< 12, ok)
fritzcremer/R6_8/n134-gpt-6.1-sol.g6: n = 134, clique number 5 (< 6, ok), independence number 7 (< 8, ok)
alphaevolve/R(3, 13) >= 61.txt: n = 60, clique number 2 (< 3, ok), independence number 12 (< 13, ok)
alphaevolve/R(4, 15) >= 163.txt: n = 162, clique number 3 (< 4, ok), independence number 14 (< 15, ok)
```

Downloads (`fetch_data.py`, `results/fetch_log.txt`): 181 of 181 witnesses matched the recorded SHA-256.

## What this does not show

- Nothing about upper bounds, or about whether a bound is the best known; the survey is the reference point only.
- A NOT_CHECKED or PARTIAL row says nothing either way about that file.
- NO_FILE_FOUND and "no public witness found" mean none was found in the sources listed in `sources/sources.csv`; witnesses may
  exist in papers, theses or private files that were not searched or could not be retrieved.
- For sampled McKay files only the sampled graphs were checked; for complete sets the completeness claimed by the
  source was not checked.
