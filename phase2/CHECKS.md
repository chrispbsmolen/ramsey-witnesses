# Checks behind the phase-2 labels

Written by `phase2/make_phase2.py` from `phase2/coverage.csv`. One line per cell with a witness file. The full records are in `phase2/checks/logs/` (index with SHA-256 in `phase2/checks/logs/INDEX.csv`).

## Checkers

| name here | program | what it decides |
|---|---|---|
| clique.c, verify_ramsey | `clique.c` of this repository (sha256 137a1002...), called by `verify_ramsey.py` (657db0ad...) or directly | is there a clique of a given size in a color class, bitset branch and bound |
| networkx | `networkx.find_cliques` (version 3.x), as in `crosscheck.py`, `xcheck.py`, `crosscheck_mc.py` | maximal-clique enumeration, shares no solver code with clique.c |
| gen0 | `phase2/scripts_as_run/build_round2/checker/gen0.c` (sha256 d82e1855...) | a separate exact clique search in C, written independently of clique.c |
| linear0 | `phase2/scripts_as_run/build_round2/checker/linear0.c` (sha256 db46ca7e...) | exact clique search for colorings given by a length vector, cliques through vertex 0 |

Every record names the SHA-256 of the object it checked. The witness files in `phase2/witnesses/` are those objects, gzip-compressed where they were not already. `phase2/witnesses/manifest.csv` gives both hashes: `sha256` of the committed file and `sha256_as_checked` of the object as named in the logs.

## Machines

- cloud: a Linux x86_64 machine, one to two cores per process, 7 to 16 November 2026.
- Mac: an Apple Silicon laptop (macOS, arm64), at most four processes, runs pasted by hand in waves 0 to 8b, 7 to 12 November 2026. Each wave log starts with the command and ends with `exit=0`. Wave 9 (13 November, the inputs of R(19,19) and R(20,20)) ran with 4 and with 12 processes.

## How to rerun one check

```
python3 verify_ramsey.py g6 phase2/witnesses/R7_11_n404.g6.gz 7,11      # both halves with clique.c
python3 verify_ramsey.py colormat phase2/witnesses/R3_3_5_n44.colormat.gz 3,3,5
python3 phase2/check_phase2.py --only 6,16 --limit 600                   # one row, repository checker
python3 phase2/check_phase2.py                                            # every witness file, 60 s per search
```

The symmetry-reduced and proof-based checks need the scripts in `phase2/scripts_as_run/` (for example `build_round5/scripts/cyclo_reduce.py` for the cubic-residue rows, `build_round5/scripts/paley_check.py` and `mac_batch/wave9/paley/paley9.py` for c(Q_p)). They are kept as run, and their paths point to the working folders, so a rerun needs the paths adjusted.

## Per cell

| cell | label | witness (sha256 of committed file) | checks |
|---|---|---|---|
| R(3,14) | VERIFIED | `R3_14_n66.colormat.gz` (739df72b3909...) | clique.c and gen0 on the whole graph, no reduction: no triangle (NONE 2) and no independent set of 14 vertices (NONE 13 on the complement). verify_ramsey PASS on the matrix and on a graph6 copy. networkx: clique number 2, independence number 13. Controls: asked for (3,13), verify_ramsey answers FAIL and networkx reports independence number 13. For each color the clique one vertex smaller is FOUND by both checkers, and a copy with a few edges recolored is caught by both. Cloud, 13 Nov (hunt4). |
| R(4,10) | VERIFIED (witness found here by search) | `R4_10_n91.g6.gz` (4d6491b990d7...) | verify_ramsey PASS (circulant). networkx, whole graph, no symmetry: clique number 3, independence number 9. Cloud, 7 Nov. |
| R(5,7) | VERIFIED | `R5_7_n79.g6.gz` (e1f088fe7efe...) | verify_ramsey PASS both halves. networkx PASS both halves. Cloud, 7 Nov. |
| R(5,8) | VERIFIED (witness found here by search) | `R5_8_n100.g6.gz` (2981ac092220...) | verify_ramsey PASS (circulant). networkx, whole graph, no symmetry: clique number 4, independence number 7. Cloud, 7 Nov. |
| R(5,15) | VERIFIED | `R5_15_n274.g6.gz` (bee135f0e847...) | No K5: clique.c NONE and networkx NONE (cloud). No independent 15-set: clique.c NONE, 52.7 s (cloud), networkx NONE, best 14, 5877 s (Mac, wave 3, 8 Nov). |
| R(6,13) | VERIFIED (symmetry-reduced) | `R6_13_n346.g6.gz` (f21d45d432d4...) | Circulant: the mask is symmetric and x -> x+1 is an automorphism, checked entry by entry on the matrix, so only cliques through vertex 0 are searched (Amendment 1). clique.c and gen0 on the neighborhood of vertex 0 in each color: no K6 in the 122-regular color (NONE, K5 asked on N(0)) and no K13 in the 223-regular color (NONE 11, K12 asked on N(0), 1.7 s and 1.6 s). Controls: the clique one size smaller is FOUND by both, and a corrupted copy with a planted clique is caught by both. verify_ramsey PASS (circulant) on the distances and on the committed graph6 file. Records in phase2/scripts_as_run/kuznetsov_2026-11-14/out/kuz_check.jsonl. Cloud, 14 Nov. |
| R(6,15) | VERIFIED (symmetry-reduced) | `R6_15_n400.g6.gz` (1e57095fc237...) | No K6: clique.c and networkx on the whole graph. No independent 15-set: clique.c --sym NONE 14 (54 s) and gen0 on N(0) (38.6 s), 4 automorphism generators and transitivity checked on the matrix. Cloud, 12 Nov. |
| R(7,11) | VERIFIED (symmetry-reduced) | `R7_11_n404.g6.gz` (7ae34e4d30ae...) | Vertex transitivity checked on the graph (4 automorphism generators, orbit of vertex 0 is everything). Both checkers on cliques through vertex 0: no K7, clique.c NONE and networkx NONE. No independent 11-set, clique.c NONE (6 s) and networkx NONE (431 s). Cloud, 7 Nov. |
| R(7,12) | VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6) | `R7_12_n416.g6.gz` (9e441de30ee5...) | No K7: clique.c NONE and networkx NONE (cloud). No independent 12-set: clique.c NONE 11, 1278 s (Mac, wave 3). networkx reached its 12 h limit (wave 4), not a check. Exact reduction alpha(F) <= alpha(G) + 1 checked on the object (decomp.py), input alpha(G) <= 10 with both checkers. |
| R(8,9) | VERIFIED | `R8_9_n328.g6.gz` (91de200ad653...) | verify_ramsey PASS and networkx PASS, both halves, for both 328-vertex entries. Cloud, 7 Nov. Decoded and checked a second time, independently, by build_G3. |
| R(8,11) | VERIFIED | `R8_11_n456.g6.gz` (da82f4a20a4c...) | No K8: clique.c NONE (0.4 s) and networkx NONE (49.8 s), cloud. No independent 11-set: clique.c NONE 10, 301 s (Mac, wave 2) and networkx NONE, 16212 s (Mac, wave 4). |
| R(8,13) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_13_n816.g6.gz` (93d6912b362b...) | No K8: clique.c NONE (7.7 s, cloud) and networkx NONE (446 s, Mac, wave 2). Input (7,7;204): both checkers, whole graph (build_round5). |
| R(8,15) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_15_n872.g6.gz` (cff93148c479...) | No K8: clique.c NONE (8.8 s, cloud) and networkx NONE (495 s, Mac, wave 2). Input g78.218: both checkers, whole graph (build_round5). |
| R(9,10) | VERIFIED | `R9_10_n580.g6.gz` (6f849d9d21e4...) | No K9: clique.c NONE (22 s, cloud) and networkx NONE (1447 s, Mac, wave 3). No independent 10-set: clique.c NONE (175 s, cloud) and networkx NONE (10537 s, Mac, wave 3). |
| R(10,15) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R10_15_n1312.g6.gz` (af65811b537d...) | No K10: clique.c NONE (2.4 s, cloud) and networkx with verified automorphisms through vertex 0, NONE (250 s, Mac, wave 2). Input (8,9;328): both checkers. |
| R(11,11) | VERIFIED (symmetry-reduced) | `R11_11_n1596.g6.gz` (57ea197e3cf3...) | Reduced check with verified automorphisms, clique.c and networkx, both colors (10 searches, 908 s, cloud). Full verify_ramsey on both colors, NONE 10 (23039 s and 22668 s, Mac, wave 6). |
| R(13,13) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R13_13_n2556.g6.gz` (bbbaf5df236e...) | Input: omega(Q_1277) = 11, no K_12 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_11 checked edge by edge (cloud 12 Nov). Also: reduced clique.c check of the doubled graph, both colors (cloud, 7 Nov). |
| R(14,14) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R14_14_n2988.g6.gz` (98e7263d2406...) | Input: omega(Q_1493) = 12, no K_13 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_12 checked edge by edge (cloud 12 Nov). Also: reduced clique.c check of the doubled graph, both colors (cloud, 7 Nov). |
| R(15,15) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R15_15_n5484.g6.gz` (7f03f23df617...) | Input: omega(Q_2741) = 13, no K_14 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_13 checked edge by edge (cloud 12 Nov). Also: reduced clique.c check of the doubled graph, both colors PASS (Mac, wave 4). |
| R(16,16) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R16_16_n5604.g6.gz` (5f6e3f8d58a3...) | Input: omega(Q_2801) = 14, no K_15 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_14 checked edge by edge (cloud 12 Nov). Also: reduced clique.c check of the doubled graph, both colors PASS (Mac, wave 5). |
| R(17,17) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R17_17_n8916.g6.gz` (cf548408ad39...) | Input: omega(Q_4457) = 15, no K_16 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_15 checked edge by edge (cloud 7 Nov). |
| R(18,18) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R18_18_n11004.g6.gz` (4e4e1a46c4f7...) | Input: omega(Q_5501) = 16, no K_17 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_16 checked edge by edge (Mac wave 8a, 12 Nov). |
| R(19,19) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R19_19_n17884.g6.gz` (a80de56e2094...) | Input: omega(Q_8941) = 17, no K_18 with clique.c and gen0 on every one of the 1117 orbit representatives after verified automorphisms (ordered subproblems, NOTES.md section 10: 2234 pieces, the largest on 1122 vertices, all NONE), and a K_17 checked edge by edge (Mac, wave 9, 13 Nov, 4 processes, 2.4 h). |
| R(20,20) | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R20_20_n21724.g6.gz` (6b8fa8b6bc6a...) | Input: omega(Q_10861) = 18, no K_19 with clique.c and gen0 on every one of the 1357 orbit representatives after verified automorphisms (ordered subproblems, NOTES.md section 10: 2714 pieces, the largest on 1375 vertices, all NONE), and a K_18 checked edge by edge (Mac, wave 9, 13 Nov, 12 processes, 3.7 h). |
| R(3,21) | VERIFIED | `R3_21_n121.g6.gz` (ad8557d4ac2a...) | verify_ramsey PASS and networkx PASS, both halves. Cloud, 7 Nov. |
| R(3,22) | VERIFIED | `R3_22_n130.g6.gz` (f581a1592676...) | verify_ramsey PASS and networkx PASS, both halves. Cloud, 7 Nov. |
| R(4,17) | VERIFIED (witness found here by search) | `R4_17_n199.g6.gz` (ce66ef50b537...) | verify_ramsey PASS (circulant). networkx: clique number 3 on the whole graph, independence number 16 through vertex 0 (circulant). Cloud, 7 Nov. |
| R(4,22) | VERIFIED (symmetry-reduced) | `R4_22_n313.g6.gz` (a45f36747cd6...) | verify_ramsey PASS both halves (46 s, cloud). networkx with translation symmetry: clique number 3, independence number 21 (23075 s, Mac, wave 7). |
| R(5,21) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R5_21_n440.g6.gz` (315aaf8a6948...) | No K5: clique.c NONE (0.1 s) and networkx NONE (2.4 s), cloud. Input r3.20.110: both checkers, whole graph (build_round5). |
| R(5,22) | VERIFIED (symmetry-reduced) | `R5_22_n491.g6.gz` (b1597d918c89...) | verify_ramsey PASS both halves (104.5 s, cloud). Reduced check after verifying x -> x+1 and x -> 2^7 x on the matrix: clique.c and gen0 NONE on all 7 subproblems (cloud, 12 Nov). networkx without reduction reached its 24 h limit (Mac, wave 7), not a check. |
| R(5,23) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R5_23_n520.g6.gz` (1034483d9459...) | No K5: clique.c --sym NONE 4 and networkx on N(0), after 4 automorphisms checked (cloud). Input (3,22;130): both checkers (build_round5). |
| R(6,16) | VERIFIED (symmetry-reduced) | `R6_16_n433.g6.gz` (f6c31087744d...) | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1 (47 vertices), independence side w=3, 7 (195, 187 vertices)). clique.c and gen0 NONE on every subproblem (cloud, 12 Nov). Full verify_ramsey PASS (cloud). |
| R(6,17) | VERIFIED (symmetry-reduced) | `R6_17_n547.g6.gz` (9e42dcc11901...) | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on every subproblem (cloud, 12 Nov). Full verify_ramsey PASS (cloud). |
| R(6,18) | VERIFIED (symmetry-reduced) | `R6_18_n613.g6.gz` (e8fcc6ee407d...) | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on every subproblem (cloud, 12 Nov). Full verify_ramsey PASS (cloud). |
| R(6,19) | VERIFIED (symmetry-reduced) | `R6_19_n709.g6.gz` (229124d5e3d6...) | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on every subproblem (cloud, 12 Nov). Full verify_ramsey PASS (460 s, Mac, wave 8a). |
| R(6,20) | VERIFIED (symmetry-reduced) | `R6_20_n877.g6.gz` (d5eba99b1c47...) | No K6: clique.c and networkx (cloud). No independent 20-set: x -> x+1 and x -> 8x verified on the matrix, 2 orbits of non-neighbors of 0 (reps 2, 3), clique.c NONE 17 and gen0 NONE on both subproblems (cloud, 12 Nov, build_round4). Full verify_ramsey PASS (3286 s, Mac, wave 8a). |
| R(6,21) | VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6) | `R6_21_n887.g6.gz` (ac5b5bc0f1c5...) | No K6: clique.c and networkx on the whole graph, no symmetry (cloud, 12 Nov). Exact reduction alpha(F) <= alpha(G) + 1 checked on the object. Input alpha(G) <= 19: both checkers (row R(6,20)). |
| R(6,22) | VERIFIED (symmetry-reduced) | `R6_22_n1069.g6.gz` (ea19f09782b3...) | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=3, 7 (475, 479 vertices)). clique.c and gen0 NONE on every subproblem (cloud, 12 Nov). Independence subproblems also clique.c NONE 19 (Mac, wave 8a). |
| R(7,16) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R7_16_n628.g6.gz` (d3d908f0abe9...) | No K7: clique.c NONE (12.6 s, cloud) and networkx NONE (580 s, Mac, wave 2). Independent 16-set: clique.c NONE 15 (1076 s, Mac, wave 3), networkx reached its 12 h limit (not a check). Input g415.157: both checkers (build_round5). |
| R(7,17) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R7_17_n728.g6.gz` (0026a3def1fe...) | Vertex transitivity checked. No K7: clique.c NONE and networkx NONE (cloud). Input (6,9;182): both checkers, whole graph (build_round5). |
| R(7,18) | VERIFIED (symmetry-reduced) | `R7_18_n796.g6.gz` (08392b78e557...) | No K7: clique.c on the whole graph NONE 6 (32 s), networkx on N(0) NONE. No independent 18-set: clique.c --sym NONE 17 (13.6 s) and gen0 on N(0) (10.1 s). 4 automorphism generators and transitivity checked. Cloud, 12 Nov. |
| R(7,19) | VERIFIED (symmetry-reduced) | `R7_19_n907.g6.gz` (669a8848694b...) | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on every subproblem (cloud, 12 Nov). Full verify_ramsey PASS (1366 s, Mac, wave 8a). |
| R(7,21) | VERIFIED (symmetry-reduced) | `R7_21_n1213.g6.gz` (7a8be2327408...) | No K7: clique.c and gen0 NONE (cloud). No independent 21-set: x -> x+1 and x -> 8x verified on the matrix, 2 orbits of non-neighbors of 0 (reps 2, 4). Subproblem w = 2 (532 vertices): clique.c NONE 18 (424.5 s, Mac, wave 8b) and gen0 NONE (546 s, cloud). Subproblem w = 4 (545 vertices): clique.c NONE 18 (465.6 s, Mac, wave 8b) and gen0 NONE (613.1 s, cloud, 13 Nov, build_round7; asked for an 18-set on the same input it answers FOUND). The Mac inputs are byte-identical to the cloud subproblems. |
| R(8,17) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_17_n1004.g6.gz` (ccb32910e841...) | Vertex transitivity checked. No K8: clique.c NONE (0.2 s) and networkx NONE (5.0 s), cloud. Input (7,9;251): both checkers (build_round5). |
| R(8,19) | VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5) | `R8_19_n1236.g6.gz` (8598388ef20f...) | No K8: clique.c NONE (34 s, cloud) and networkx NONE (1848 s, Mac, wave 2). Inputs: (8,13;816) row R(8,13), (7,8;216) both checkers on both halves. |
| R(8,21) | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_21_n1616.g6.gz` (6a1a5f726200...) | Vertex transitivity checked (7 generators). No K8: clique.c NONE (0.3 s) and networkx NONE (5.6 s), cloud. Input (7,11;404): both checkers on both halves. |
| R(3,27) | VERIFIED (symmetry-reduced) | `R3_27_n171.g6.gz` (5765f45e3cc0...) | verify_ramsey PASS (circulant, 30.6 s cloud). Negative control (3,26) FAIL as required. networkx with translation symmetry: clique number 2, independence number 26 (8712 s, Mac, wave 8a). |
| R(5,5,5) | VERIFIED | `R5_5_5_n453.colormat.gz` (af30b1401df3...) | verify_ramsey PASS and crosscheck_mc (networkx) PASS. Cloud, 7 Nov. |
| R(6,6,6) | VERIFIED | `R6_6_6_n1105.lengths.gz` (7c1dc57c4aba...) | No K6 in any color: clique.c and gen0, full search, no symmetry. Also verify_ramsey and crosscheck_mc with the cyclic reduction. Cloud, 7 Nov. |
| R(7,7,7) | VERIFIED (symmetry-reduced) | `R7_7_7_n3213.colormat.gz` (857a106a5727...) | Reduced check with verified automorphisms, clique.c and networkx (99 searches, cloud). Full verify_ramsey on all three colors, NONE 6 (about 1200 s each, Mac, waves 5 and 6). |
| R(9,9,9) | VERIFIED (by proof: XXER Cor. 5, p.15) | `R9_9_9_n15040.colormat.gz` (8411c743ec09...) | Colors 1 and 2: 7 automorphism generators and transitivity checked, clique.c NONE 7 and gen0 NONE on N(0) (Mac, wave 8a). Input (3,8,8;940): verify_ramsey and crosscheck_mc PASS. |
| R(10,10,10) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R10_10_10_n23093.lengths.gz` (68804706cea4...) | Colors 2 and 3: linear0 NONE (Mac, wave 8a) and clique.c NONE 9 (Mac, wave 8b). Color 1 on the 253-vertex window the theorem leaves: clique.c, gen0 and linear0 NONE (cloud, 12 Nov). Q_797 with both checkers. |
| R(3,3,3,3) | VERIFIED | `R3x4_n50.colormat.gz` (04cdf0605ce9...) | verify_ramsey PASS (all 4 colors K3-free). networkx: clique number 2 in each color. Negative control FAIL as required. Cloud, 7 Nov. |
| R(4,4,4,4) | VERIFIED | `R4x4_n633.lengths.gz` (8c207318fe5b...) | No K4 in any color: clique.c and gen0, full search. Also verify_ramsey and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(5,5,5,5) | VERIFIED (symmetry-reduced) | `R5x4_n4072.lengths.gz` (9ead73a445c0...) | Cyclic (rotation tested). verify_ramsey PASS (11.1 s) and crosscheck_mc PASS (41 s), cliques through vertex 0. Cloud, 7 Nov. |
| R(6,6,6,6) | VERIFIED (symmetry-reduced) | `R6x4_n23501.lengths.gz` (122090f8b15e...) | Cyclic. Colors 3 and 4: clique.c --sym NONE 5 and linear0 NONE (cloud). Colors 1 and 2: linear0 NONE (545 s, 527 s, Mac, wave 8a) and clique.c NONE 5 (2674 s, 2814 s, Mac, wave 8b). |
| R(7,7,7,7) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R7x4_n94873.lengths.gz` (10bfdf16d496...) | Inputs U and V: clique.c and gen0 on every color, whole graph, with lowered-k controls. Template color checked triangle-free and containing length m-1, phi and N checked. Then colors 3, 4 by the theorem from V (both checkers, whole graph). Colors 1, 2: window 0..2820 (K7 through vertex 0, 784 and 849 lengths): clique.c NONE 5, gen0 NONE, linear0 NONE, and the K6 control FOUND by both (cloud, 12 Nov, build_round6). |
| R(8,8,8,8) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R8x4_n182001.lengths.gz` (448d25692c6a...) | Inputs U and V: clique.c and gen0 on every color, whole graph, with lowered-k controls. Template color checked triangle-free and containing length m-1, phi and N checked. Then colors 3, 4 by the theorem from V = Q_281 (both checkers). Colors 1, 2: window 0..4536: clique.c NONE 6 (30.9 s, 20.2 s), gen0 NONE, linear0 NONE, K7 control FOUND by both (cloud, 12 Nov, build_round6). |
| R(9,9,9,9) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R9x4_n719203.lengths.gz` (b4fdde975a81...) | Inputs. U (9,9,3;1282): colors 1, 2 clique.c and gen0 through vertex 0 with lowered-k controls (the whole-graph run did not finish in 140 s), color 3 both checkers on the whole graph. V (9,9;562): clique.c and gen0 on both colors, whole graph, with lowered-k controls. Template color checked triangle-free and containing length m-1, phi and N checked. Then colors 3, 4 by the theorem from V. Colors 1, 2: window 0..10240 (K9 through vertex 0, 2981 and 2908 lengths). The search for a K8 among these lengths was split exactly by the smallest vertex of the K8, into 2981 and 2908 pieces. Every piece was decided by clique.c and, separately, by gen0, all NONE. The recorded ranges cover the pieces exactly once for each color and checker (summarise.py: 16, 15, 16 and 16 calls, 8611 s, 8326 s, 8460 s and 8549 s). K8 control in the window FOUND by both checkers in each color. The undivided searches (clique.c and linear0 on color 1) reached the 570 s limit and are not counted. Cloud, 12 and 13 Nov (build_round6). |
| R(3,3,3,3,3) | VERIFIED | `R3x5_n161.colormat.gz` (69e2748a5381...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(4,4,4,4,4) | VERIFIED | `R4x5_n4175.lengths.gz` (13c9a8613708...) | No K4 in any color: clique.c (11.6 s) and gen0 (10.6 s), full search. Cloud, 7 Nov. |
| R(5,5,5,5,5) | VERIFIED (symmetry-reduced) | `R5x5_n44337.lengths.gz` (a25327a0bdba...) | Cyclic, cliques through vertex 0. Colors 3, 4, 5: linear0 and clique.c NONE (cloud). Color 1: linear0 NONE (290 s, Mac, wave 2) and clique.c NONE 4 (Mac, wave 6). Color 2: linear0 NONE (128 s, wave 2) and clique.c NONE 4 (wave 3). |
| R(6,6,6,6,6) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R6x5_n258505.lengths.gz` (29ae816508ae...) | Inputs U and V: clique.c and gen0 on every color, whole graph, with lowered-k controls. Template color checked triangle-free and containing length m-1, phi and N checked. Then colors 2 to 5 by the theorem from V (the R(6,6,6,6) row, every color both checkers). Color 1: window 0..50: clique.c, gen0 and linear0 NONE, K5 control FOUND by both (cloud, 12 Nov, build_round6). |
| R(3,3,3,3,3,3) | VERIFIED | `R3x6_n537.colormat.gz` (687b8fcee6c6...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(4,4,4,4,4,4) | VERIFIED (symmetry-reduced) | `R4x6_n32005.lengths.gz` (1b3f7421f8c5...) | Cyclic, cliques through vertex 0. clique.c --sym NONE 3 in all 6 colors (58 s) and linear0 NONE in all 6 colors. Cloud, 7 Nov. |
| R(5,5,5,5,5,5) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R5x6_n441605.lengths.gz` (9f21737f29b5...) | Inputs U and V: clique.c and gen0 on every color, whole graph, with lowered-k controls. Template color checked triangle-free and containing length m-1, phi and N checked. Then colors 4, 5, 6 by the theorem from V (both checkers). Colors 1, 2, 3: window 0..3900: clique.c NONE 3, gen0 NONE, linear0 NONE, K4 control FOUND by both (cloud, 12 Nov, build_round6). |
| R(3,3,3,3,3,3,3) | VERIFIED | `R3x7_n1697.colormat.gz` (49612ddcf022...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(4,4,4,4,4,4,4) | VERIFIED (symmetry-reduced) | `R4x7_n160023.lengths.gz` (55f0f485d6c4...) | Cyclic, cliques through vertex 0: clique.c on N(0) in each of 7 colors (82 s) and linear0 NONE in all 7 colors (50 s). Cloud, 7 Nov. |
| R(3,3,3,3,3,3,3,3) | VERIFIED | `R3x8_n5287.lengths.gz` (991923139443...) | No K3 in any of 8 colors: clique.c, all vertices. Exact sum-free check of the partition. linear0 and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,3,3,3,3,3,3,3) | VERIFIED | `R3x9_n17804.lengths.gz` (b3f71af9806e...) | No K3 in any of 9 colors: clique.c, all vertices (46 s). Exact sum-free check. linear0 PASS. Cloud, 7 Nov. |
| R(3,3,4) | VERIFIED | `R3_3_4_n29.colormat.gz` (f4314cc19168...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,5) | VERIFIED | `R3_3_5_n44.colormat.gz` (901f2e9e858b...) | verify_ramsey PASS and crosscheck_mc PASS. All 13 graphs of Table III pass both. Negative controls FAIL as required. Cloud, 7 Nov. |
| R(3,3,7) | VERIFIED | `R3_3_7_n84.colormat.gz` (c3bbf2ba472f...) | clique.c and gen0 on every color, whole graph, no reduction: color 0: NONE 2 with both (no K3); color 1: NONE 2 with both (no K3); color 2: NONE 6 with both (no K7). verify_ramsey PASS. networkx gives the same clique numbers. Controls for every color: the clique one vertex smaller is FOUND by both checkers, and a copy with one K_k planted is caught by both. Script phase2/scripts_as_run/exoo_2026-11-16/exoo_check.py, records in phase2/checks/logs/exoo_2026-11-16/exoo_check.jsonl. Cloud, 16 Nov. |
| R(3,3,8) | VERIFIED | `R3_3_8_n102.colormat.gz` (ff32eb94cf0a...) | clique.c and gen0 on every color, whole graph, no reduction: color 0: NONE 2 with both (no K3); color 1: NONE 2 with both (no K3); color 2: NONE 7 with both (no K8). verify_ramsey PASS. networkx gives the same clique numbers. Controls for every color: the clique one vertex smaller is FOUND by both checkers, and a copy with one K_k planted is caught by both. Script phase2/scripts_as_run/exoo_2026-11-16/exoo_check.py, records in phase2/checks/logs/exoo_2026-11-16/exoo_check.jsonl. Cloud, 16 Nov. |
| R(3,4,4) | VERIFIED | `R3_4_4_n54.colormat.gz` (60778bcc0dd6...) | verify_ramsey PASS and crosscheck_mc PASS. 16 of the 18 Table IV rows pass both. Cloud, 7 Nov. |
| R(3,4,6) | VERIFIED | `R3_4_6_n116.colormat.gz` (eca1092e85bb...) | clique.c and gen0 on every color, whole graph, no reduction: color 0: NONE 2 with both (no K3); color 1: NONE 3 with both (no K4); color 2: NONE 5 with both (no K6). verify_ramsey PASS. networkx gives the same clique numbers. Controls for every color: the clique one vertex smaller is FOUND by both checkers, and a copy with one K_k planted is caught by both. Script phase2/scripts_as_run/exoo_2026-11-16/exoo_check.py, records in phase2/checks/logs/exoo_2026-11-16/exoo_check.jsonl. Cloud, 16 Nov. |
| R(3,4,8) | VERIFIED | `R3_4_8_n192.colormat.gz` (4231ac0ff9fc...) | verify_ramsey PASS. networkx clique numbers 3, 7, 2. Cloud, 7 Nov. |
| R(3,5,5) | VERIFIED | `R3_5_5_n139.colormat.gz` (8971d5cb7bd6...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,5,6) | VERIFIED | `R3_5_6_n191.colormat.gz` (fb3e344dbe32...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,5,7) | VERIFIED | `R3_5_7_n240.colormat.gz` (efe97958e7a1...) | verify_ramsey PASS. networkx clique numbers 2, 6, 4. Cloud, 7 Nov. |
| R(3,3,3,4) | VERIFIED | `R3_3_3_4_n96.colormat.gz` (4d9ce2d3b796...) | clique.c and gen0 on every color, whole graph, no reduction: color 0: NONE 2 with both (no K3); color 1: NONE 2 with both (no K3); color 2: NONE 2 with both (no K3); color 3: NONE 3 with both (no K4). verify_ramsey PASS. networkx gives the same clique numbers. Controls for every color: the clique one vertex smaller is FOUND by both checkers, and a copy with one K_k planted is caught by both. Script phase2/scripts_as_run/exoo_2026-11-16/exoo_check.py, records in phase2/checks/logs/exoo_2026-11-16/exoo_check.jsonl. Cloud, 16 Nov. |
| R(3,3,4,4) | VERIFIED | `R3_3_4_4_n173.colormat.gz` (aeaf8519f211...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,4,4,4) | VERIFIED | `R3_4_4_4_n380.colormat.gz` (bfc5aa86152b...) | verify_ramsey PASS (circulant). networkx clique numbers 3, 3, 3, 2. Cloud, 7 Nov. |
| R(3,3,3,10) | VERIFIED | `R3_3_3_10_n512.colormat.gz` (8dda62cc78be...) | verify_ramsey PASS (12 s). networkx clique numbers 2, 2, 9, 2 (color 2 in 3 parts, 1100 s). Cloud, 7 Nov. |
| R(3,3,3,11) | VERIFIED | `R3_3_3_11_n596.colormat.gz` (bbdb1cac1c8c...) | verify_ramsey PASS (22.8 s, cloud). networkx colors 0, 1, 3 (cloud) and color 2 in 4 residue classes, all done, omega 10 (Mac, wave 1). |
| R(3,4,5,5) | VERIFIED | `R3_4_5_5_n728.colormat.gz` (059321afcc2f...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,5,5,5) | VERIFIED | `R3_5_5_5_n1429.colormat.gz` (d8c2cb831f8a...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,6,6) | VERIFIED | `R3_6_6_n337.colormat.gz` (a62f6ee116da...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,7,7) | VERIFIED | `R3_7_7_n673.colormat.gz` (b60261c269b2...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,8,8) | VERIFIED | `R3_8_8_n940.colormat.gz` (6a27c0367149...) | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,9,9) | VERIFIED | `R3_9_9_n1843.colormat.gz` (177449e9b110...) | verify_ramsey PASS (14 s) and crosscheck_mc PASS (110 s). Cloud, 7 Nov. |
| R(8,8,9) | VERIFIED (by proof: XXER Cor. 5, p.15) | `R8_8_9_n10768.colormat.gz` (268519f30308...) | Vertex-transitive (7 automorphisms checked). Colors 1 and 2: no K7 in N(0), clique.c (37 s, 32 s) and gen0 (39 s, 35 s), cloud. Input (3,7,7;673): verify_ramsey and crosscheck_mc PASS. |
| R(6,6,6,6,6,6) | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R6x6_n5499101.lengths.gz` (c5645d4c19da...) | Inputs U and V: clique.c and gen0 on every color, whole graph, with lowered-k controls. Template color checked triangle-free and containing length m-1, phi and N checked. Then colors 3 to 6 by the theorem from V. Colors 1, 2: window 0..1165: clique.c, gen0 and linear0 NONE, K5 control FOUND by both (cloud, 12 Nov, build_round6). |
| R(3,3,3,7) | VERIFIED (witness found here by search) | `R3_3_3_7_n246.colormat.gz` (797d057b62d7...) | Input (3,3,7;80): verify_ramsey PASS (circulant), and clique.c and gen0 on every color, whole graph: NONE 2, NONE 2, NONE 6. Witness (3,3,3,7;246): verify_ramsey PASS (0.3 s), and clique.c and gen0 on every color, whole graph, no reduction: NONE 2, 2, 2, 6. Negative controls for every color: the color asked for one vertex less is FOUND by both checkers, and a copy with one or two edges recolored is caught by both. Cloud, 12 Nov. |

## Repository checker on every witness file

Output of `python3 phase2/check_phase2.py --limit 120` run from a fresh clone of this branch (see `phase2/results/RUN_NOTE.txt`) (`phase2/results/repo_check.txt`, records in `phase2/results/repo_check.jsonl`). This is a uniform light re-check with a time limit. NOT_COMPLETED means the limit was reached. NOT_RUN_SIZE means the file has more vertices than the in-memory checker loads. Neither is a failure, and the labels rest on the checks listed above.

```
Repository checker on the phase-2 witness files (Linux x86_64, CPython 3.13.18, 2 cores, limit 120 s per clique search, max n 6000)
verify_ramsey.py 657db0ada9f88716, clique.c 137a100275a4a061

cell                   file                                     n verdict         seconds  label
4,10                   R4_10_n91.g6.gz                         91 PASS                0.0  VERIFIED
5,7                    R5_7_n79.g6.gz                          79 PASS                0.0  VERIFIED
5,8                    R5_8_n100.g6.gz                        100 PASS                0.0  VERIFIED
5,15                   R5_15_n274.g6.gz                       274 PASS               46.7  VERIFIED
6,15                   R6_15_n400.g6.gz                       400 NOT_COMPLETED     120.2  VERIFIED (symmetry-reduced)
7,11                   R7_11_n404.g6.gz                       404 NOT_COMPLETED     120.2  VERIFIED
7,12                   R7_12_n416.g6.gz                       416 NOT_COMPLETED     120.2  VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6)
8,9                    R8_9_n328.g6.gz                        328 PASS                0.1  VERIFIED
8,11                   R8_11_n456.g6.gz                       456 NOT_COMPLETED     120.2  VERIFIED
8,13                   R8_13_n816.g6.gz                       816 NOT_COMPLETED     120.5  VERIFIED (by proof: XXER Thm 9, pp.15-16)
8,15                   R8_15_n872.g6.gz                       872 NOT_COMPLETED     120.5  VERIFIED (by proof: XXER Thm 9, pp.15-16)
9,10                   R9_10_n580.g6.gz                       580 NOT_COMPLETED     120.3  VERIFIED
10,15                  R10_15_n1312.g6.gz                    1312 NOT_COMPLETED     120.9  VERIFIED (by proof: XXER Thm 9, pp.15-16)
11,11                  R11_11_n1596.g6.gz                    1596 NOT_COMPLETED     121.9  VERIFIED (symmetry-reduced)
13,13                  R13_13_n2556.g6.gz                    2556 NOT_COMPLETED     124.3  VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
14,14                  R14_14_n2988.g6.gz                    2988 NOT_COMPLETED     127.4  VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
15,15                  R15_15_n5484.g6.gz                    5484 NOT_COMPLETED     147.5  VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
16,16                  R16_16_n5604.g6.gz                    5604 NOT_COMPLETED     153.4  VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
17,17                  R17_17_n8916.g6.gz                    8916 NOT_RUN_SIZE             VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
18,18                  R18_18_n11004.g6.gz                  11004 NOT_RUN_SIZE             VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
3,21                   R3_21_n121.g6.gz                       121 PASS                1.0  VERIFIED
3,22                   R3_22_n130.g6.gz                       130 PASS                6.3  VERIFIED
4,17                   R4_17_n199.g6.gz                       199 PASS                0.3  VERIFIED (symmetry-reduced)
4,22                   R4_22_n313.g6.gz                       313 PASS               64.3  VERIFIED (symmetry-reduced)
5,21                   R5_21_n440.g6.gz                       440 NOT_COMPLETED     120.3  VERIFIED (by proof: XXER Thm 9, pp.15-16)
5,22                   R5_22_n491.g6.gz                       491 NOT_COMPLETED     120.3  VERIFIED (symmetry-reduced)
5,23                   R5_23_n520.g6.gz                       520 NOT_COMPLETED     120.5  VERIFIED (by proof: XXER Thm 9, pp.15-16)
6,16                   R6_16_n433.g6.gz                       433 PASS               10.7  VERIFIED (symmetry-reduced)
6,17                   R6_17_n547.g6.gz                       547 PASS               84.3  VERIFIED (symmetry-reduced)
6,18                   R6_18_n613.g6.gz                       613 NOT_COMPLETED     120.5  VERIFIED (symmetry-reduced)
6,19                   R6_19_n709.g6.gz                       709 NOT_COMPLETED     120.6  VERIFIED (symmetry-reduced)
6,20                   R6_20_n877.g6.gz                       877 NOT_COMPLETED     120.9  VERIFIED (symmetry-reduced)
6,21                   R6_21_n887.g6.gz                       887 NOT_COMPLETED     121.0  VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6)
6,22                   R6_22_n1069.g6.gz                     1069 NOT_COMPLETED     121.4  VERIFIED (symmetry-reduced)
7,16                   R7_16_n628.g6.gz                       628 NOT_COMPLETED     120.6  VERIFIED (by proof: XXER Thm 9, pp.15-16)
7,17                   R7_17_n728.g6.gz                       728 NOT_COMPLETED     120.7  VERIFIED (by proof: XXER Thm 9, pp.15-16)
7,18                   R7_18_n796.g6.gz                       796 NOT_COMPLETED     120.7  VERIFIED (symmetry-reduced)
7,19                   R7_19_n907.g6.gz                       907 NOT_COMPLETED     121.0  VERIFIED (symmetry-reduced)
7,21                   R7_21_n1213.g6.gz                     1213 NOT_COMPLETED     121.8  PARTIAL: one independence subproblem (w = 4) has clique.c only, gen0 not finished
8,17                   R8_17_n1004.g6.gz                     1004 NOT_COMPLETED     121.2  VERIFIED (by proof: XXER Thm 9, pp.15-16)
8,19                   R8_19_n1236.g6.gz                     1236 NOT_COMPLETED     121.8  VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5)
8,21                   R8_21_n1616.g6.gz                     1616 NOT_COMPLETED     122.6  VERIFIED (by proof: XXER Thm 9, pp.15-16)
3,27                   R3_27_n171.g6.gz                       171 PASS               74.1  VERIFIED (symmetry-reduced)
5,5,5                  R5_5_5_n453.colormat.gz                453 PASS                0.2  VERIFIED
6,6,6                  R6_6_6_n1105.lengths.gz               1105 PASS                1.2  VERIFIED
7,7,7                  R7_7_7_n3213.colormat.gz              3213 NOT_COMPLETED     126.3  VERIFIED (symmetry-reduced)
9,9,9                  R9_9_9_n15040.colormat.gz            15040 NOT_RUN_SIZE             VERIFIED (by proof: XXER Cor. 5, p.15)
10,10,10               R10_10_10_n23093.lengths.gz          23093 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)
3,3,3,3                R3x4_n50.colormat.gz                    50 PASS                0.0  VERIFIED
4,4,4,4                R4x4_n633.lengths.gz                   633 PASS                0.5  VERIFIED
5,5,5,5                R5x4_n4072.lengths.gz                 4072 PASS               25.6  VERIFIED (symmetry-reduced)
6,6,6,6                R6x4_n23501.lengths.gz               23501 NOT_RUN_SIZE             VERIFIED (symmetry-reduced)
3,3,3,3,3              R3x5_n161.colormat.gz                  161 PASS                0.1  VERIFIED
4,4,4,4,4              R4x5_n4175.lengths.gz                 4175 PASS               25.2  VERIFIED
5,5,5,5,5              R5x5_n44337.lengths.gz               44337 NOT_RUN_SIZE             VERIFIED (symmetry-reduced)
3,3,3,3,3,3            R3x6_n537.colormat.gz                  537 PASS                0.5  VERIFIED
4,4,4,4,4,4            R4x6_n32005.lengths.gz               32005 NOT_RUN_SIZE             VERIFIED (symmetry-reduced)
3,3,3,3,3,3,3          R3x7_n1697.colormat.gz                1697 PASS                5.6  VERIFIED
4,4,4,4,4,4,4          R4x7_n160023.lengths.gz             160023 NOT_RUN_SIZE             VERIFIED (symmetry-reduced)
3,3,3,3,3,3,3,3        R3x8_n5287.lengths.gz                 5287 PASS               65.3  VERIFIED
3,3,3,3,3,3,3,3,3      R3x9_n17804.lengths.gz               17804 NOT_RUN_SIZE             VERIFIED
3,3,4                  R3_3_4_n29.colormat.gz                  29 PASS                0.0  VERIFIED
3,3,5                  R3_3_5_n44.colormat.gz                  44 PASS                0.0  VERIFIED
3,4,4                  R3_4_4_n54.colormat.gz                  54 PASS                0.0  VERIFIED
3,4,8                  R3_4_8_n192.colormat.gz                192 PASS                0.1  VERIFIED
3,5,5                  R3_5_5_n139.colormat.gz                139 PASS                0.0  VERIFIED
3,5,6                  R3_5_6_n191.colormat.gz                191 PASS                0.0  VERIFIED
3,5,7                  R3_5_7_n240.colormat.gz                240 PASS                0.1  VERIFIED
3,3,4,4                R3_3_4_4_n173.colormat.gz              173 PASS                0.0  VERIFIED
3,4,4,4                R3_4_4_4_n380.colormat.gz              380 PASS                0.3  VERIFIED
3,3,3,10               R3_3_3_10_n512.colormat.gz             512 PASS               18.4  VERIFIED
3,3,3,11               R3_3_3_11_n596.colormat.gz             596 PASS               51.2  VERIFIED
3,4,5,5                R3_4_5_5_n728.colormat.gz              728 PASS                0.6  VERIFIED
3,5,5,5                R3_5_5_5_n1429.colormat.gz            1429 PASS                4.2  VERIFIED
3,6,6                  R3_6_6_n337.colormat.gz                337 PASS                0.2  VERIFIED
3,7,7                  R3_7_7_n673.colormat.gz                673 PASS                0.7  VERIFIED
3,8,8                  R3_8_8_n940.colormat.gz                940 PASS                1.7  VERIFIED
3,9,9                  R3_9_9_n1843.colormat.gz              1843 PASS               33.0  VERIFIED
8,8,9                  R8_8_9_n10768.colormat.gz            10768 NOT_RUN_SIZE             VERIFIED (by proof: XXER Cor. 5, p.15)

totals: NOT_COMPLETED 30, NOT_RUN_SIZE 10, PASS 39
sha256 all match: True
```

The seven witness files added later (the six Rowley rows and R(3,3,3,7)), checked the same way from a fresh clone (`phase2/results/repo_check_v2.txt`):

```
Repository checker on the phase-2 witness files (Linux x86_64, CPython 3.13.18, 2 cores, limit 120 s per clique search, max n 6000)
verify_ramsey.py 657db0ada9f88716, clique.c 137a100275a4a061

cell                   file                                     n verdict         seconds  label
7,7,7,7                R7x4_n94873.lengths.gz               94873 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)
8,8,8,8                R8x4_n182001.lengths.gz             182001 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)
9,9,9,9                R9x4_n719203.lengths.gz             719203 NOT_RUN_SIZE             PARTIAL: the window for colours 1 and 2 (K9 on vertices 0..10240) is not finished
6,6,6,6,6              R6x5_n258505.lengths.gz             258505 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)
5,5,5,5,5,5            R5x6_n441605.lengths.gz             441605 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)
6,6,6,6,6,6            R6x6_n5499101.lengths.gz           5499101 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)
3,3,3,7                R3_3_3_7_n246.colormat.gz              246 PASS                0.2  VERIFIED (witness found here by search)

totals: NOT_RUN_SIZE 6, PASS 1
sha256 all match: True
```

The two rows that changed on 13 November, R(3,14) and R(9,9,9,9), checked the same way from a fresh clone (`phase2/results/repo_check_v3.txt`):

```
Repository checker on the phase-2 witness files (Linux x86_64, CPython 3.13.18, 2 cores, limit 120 s per clique search, max n 6000)
verify_ramsey.py 657db0ada9f88716, clique.c 137a100275a4a061

cell                   file                                     n verdict         seconds  label
3,14                   R3_14_n66.colormat.gz                   66 PASS                0.0  VERIFIED
9,9,9,9                R9x4_n719203.lengths.gz             719203 NOT_RUN_SIZE             VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250)

totals: NOT_RUN_SIZE 1, PASS 1
sha256 all match: True
```

The three rows that changed on 14 November, R(7,21), R(19,19) and R(20,20), checked the same way from a fresh clone (`phase2/results/repo_check_v4.txt`):

```
Repository checker on the phase-2 witness files (Linux x86_64, CPython 3.13.18, 2 cores, limit 120 s per clique search, max n 6000)
verify_ramsey.py 657db0ada9f88716, clique.c 137a100275a4a061

cell                   file                                     n verdict         seconds  label
19,19                  R19_19_n17884.g6.gz                  17884 NOT_RUN_SIZE             VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
20,20                  R20_20_n21724.g6.gz                  21724 NOT_RUN_SIZE             VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303)
7,21                   R7_21_n1213.g6.gz                     1213 NOT_COMPLETED     122.5  VERIFIED (symmetry-reduced)

totals: NOT_COMPLETED 1, NOT_RUN_SIZE 2
sha256 all match: True
```

The five rows that changed on 16 November, R(6,13), R(3,3,7), R(3,3,8), R(3,4,6) and R(3,3,3,4), checked the same way from a fresh clone (`phase2/results/repo_check_v5.txt`):

```
Repository checker on the phase-2 witness files (Linux x86_64, CPython 3.13.18, 2 cores, limit 120 s per clique search, max n 6000)
verify_ramsey.py 657db0ada9f88716, clique.c 137a100275a4a061

cell                   file                                     n verdict         seconds  label
6,13                   R6_13_n346.g6.gz                       346 PASS                2.1  VERIFIED (symmetry-reduced)
3,3,7                  R3_3_7_n84.colormat.gz                  84 PASS                0.0  VERIFIED
3,3,8                  R3_3_8_n102.colormat.gz                102 PASS                0.0  VERIFIED
3,4,6                  R3_4_6_n116.colormat.gz                116 PASS                0.0  VERIFIED
3,3,3,4                R3_3_3_4_n96.colormat.gz                96 PASS                0.0  VERIFIED

totals: PASS 5
sha256 all match: True
```
