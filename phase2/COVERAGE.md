# Phase 2 coverage: the 105 cells without a public witness on 4 November 2026

Written by `phase2/make_phase2.py` from `phase2/coverage.csv`, which has the full text of every field (source, how the file was read or built, licence or credit, checks, proof, notes). Status as of 14 November 2026.

| group | two-colour | multicolour | total |
|---|---|---|---|
| VERIFIED, every half or colour checked by two independent checkers on the object | 8 | 27 | 35 |
| VERIFIED (symmetry-reduced), both checkers on a reduction by automorphisms verified on the object | 15 | 6 | 21 |
| VERIFIED (by proof: citation), a half or the whole row follows by a published, cited theorem from inputs checked by both checkers | 20 | 9 | 29 |
| VERIFIED (witness found here by search), the witness or its input found here by search (Amendments 2 and 6), every colour checked by both checkers | 3 | 1 | 4 |
| PARTIAL | 0 | 0 | 0 |
| RECIPE ONLY | 3 | 0 | 3 |
| NOT REPRODUCED | 3 | 2 | 5 |
| STILL NO FILE | 3 | 5 | 8 |
| all | 55 | 50 | 105 |

VERIFIED in one of its four forms: 89 of 105.

## VERIFIED, every half or colour checked by two independent checkers on the object (35)

| cell | survey bound [ref] | label | witness | n | checks |
|---|---|---|---|---|---|
| R(3,14) | 67 [Kol2] | VERIFIED | `R3_14_n66.colormat.gz` | 66 | clique.c and gen0 on the whole graph, no reduction: no triangle (NONE 2) and no independent set of 14 vertices (NONE 13 on the complement). verify_ramsey PASS on the ... |
| R(5,7) | 80 [CaET] | VERIFIED | `R5_7_n79.g6.gz` | 79 | verify_ramsey PASS both halves. networkx PASS both halves. Cloud, 7 Nov. |
| R(5,15) | 275 [2.3.h] | VERIFIED | `R5_15_n274.g6.gz` | 274 | No K5: clique.c NONE and networkx NONE (cloud). No independent 15-set: clique.c NONE, 52.7 s (cloud), networkx NONE, best 14, 5877 s (Mac, wave 3, 8 Nov). |
| R(8,9) | 329 [Kuz] | VERIFIED | `R8_9_n328.g6.gz` | 328 | verify_ramsey PASS and networkx PASS, both halves, for both 328-vertex entries. Cloud, 7 Nov. Decoded and checked a second time, independently, by build_G3. |
| R(8,11) | 457 [2.3.i] | VERIFIED | `R8_11_n456.g6.gz` | 456 | No K8: clique.c NONE (0.4 s) and networkx NONE (49.8 s), cloud. No independent 11-set: clique.c NONE 10, 301 s (Mac, wave 2) and networkx NONE, 16212 s (Mac, wave 4). |
| R(9,10) | 581 [XSR2] | VERIFIED | `R9_10_n580.g6.gz` | 580 | No K9: clique.c NONE (22 s, cloud) and networkx NONE (1447 s, Mac, wave 3). No independent 10-set: clique.c NONE (175 s, cloud) and networkx NONE (10537 s, Mac, wave 3). |
| R(3,21) | 122 [W1+] | VERIFIED | `R3_21_n121.g6.gz` | 121 | verify_ramsey PASS and networkx PASS, both halves. Cloud, 7 Nov. |
| R(3,22) | 131 [W2+] | VERIFIED | `R3_22_n130.g6.gz` | 130 | verify_ramsey PASS and networkx PASS, both halves. Cloud, 7 Nov. |
| R(5,5,5) | 454 [Ex23] | VERIFIED | `R5_5_5_n453.colormat.gz` | 453 | verify_ramsey PASS and crosscheck_mc (networkx) PASS. Cloud, 7 Nov. |
| R(6,6,6) | 1,106 [Row3] | VERIFIED | `R6_6_6_n1105.lengths.gz` | 1,105 | No K6 in any colour: clique.c and gen0, full search, no symmetry. Also verify_ramsey and crosscheck_mc with the cyclic reduction. Cloud, 7 Nov. |
| R(3,3,3,3) | 51 [Chu1] | VERIFIED | `R3x4_n50.colormat.gz` | 50 | verify_ramsey PASS (all 4 colours K3-free). networkx: clique number 2 in each colour. Negative control FAIL as required. Cloud, 7 Nov. |
| R(4,4,4,4) | 634 [XXER] | VERIFIED | `R4x4_n633.lengths.gz` | 633 | No K4 in any colour: clique.c and gen0, full search. Also verify_ramsey and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,3,3,3) | 162 [Ex10] | VERIFIED | `R3x5_n161.colormat.gz` | 161 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(4,4,4,4,4) | 4,176 [Row1] | VERIFIED | `R4x5_n4175.lengths.gz` | 4,175 | No K4 in any colour: clique.c (11.6 s) and gen0 (10.6 s), full search. Cloud, 7 Nov. |
| R(3,3,3,3,3,3) | 538 [FreSw] | VERIFIED | `R3x6_n537.colormat.gz` | 537 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,3,3,3,3,3) | 1,698 [Row4] | VERIFIED | `R3x7_n1697.colormat.gz` | 1,697 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,3,3,3,3,3,3) | 5,288 [Row3] | VERIFIED | `R3x8_n5287.lengths.gz` | 5,287 | No K3 in any of 8 colours: clique.c, all vertices. Exact sum-free check of the partition. linear0 and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,3,3,3,3,3,3,3) | 17,805 [AgCP+] | VERIFIED | `R3x9_n17804.lengths.gz` | 17,804 | No K3 in any of 9 colours: clique.c, all vertices (46 s). Exact sum-free check. linear0 PASS. Cloud, 7 Nov. |
| R(3,3,4) | 30 [Ka2] | VERIFIED | `R3_3_4_n29.colormat.gz` | 29 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,3,5) | 45 [Ex2] | VERIFIED | `R3_3_5_n44.colormat.gz` | 44 | verify_ramsey PASS and crosscheck_mc PASS. All 13 graphs of Table III pass both. Negative controls FAIL as required. Cloud, 7 Nov. |
| R(3,4,4) | 55 [KrLR] | VERIFIED | `R3_4_4_n54.colormat.gz` | 54 | verify_ramsey PASS and crosscheck_mc PASS. 16 of the 18 Table IV rows pass both. Cloud, 7 Nov. |
| R(3,4,8) | 193 [6.2.g] | VERIFIED | `R3_4_8_n192.colormat.gz` | 192 | verify_ramsey PASS. networkx clique numbers 3, 7, 2. Cloud, 7 Nov. |
| R(3,5,5) | 139 [Ex17] | VERIFIED | `R3_5_5_n139.colormat.gz` | 139 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,5,6) | 181 [Ex17] | VERIFIED | `R3_5_6_n191.colormat.gz` | 191 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,5,7) | 241 [6.2.g] | VERIFIED | `R3_5_7_n240.colormat.gz` | 240 | verify_ramsey PASS. networkx clique numbers 2, 6, 4. Cloud, 7 Nov. |
| R(3,3,4,4) | 174 [Row2] | VERIFIED | `R3_3_4_4_n173.colormat.gz` | 173 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,4,4,4) | 381 [6.2.j] | VERIFIED | `R3_4_4_4_n380.colormat.gz` | 380 | verify_ramsey PASS (circulant). networkx clique numbers 3, 3, 3, 2. Cloud, 7 Nov. |
| R(3,3,3,10) | 513 [6.2.g] | VERIFIED | `R3_3_3_10_n512.colormat.gz` | 512 | verify_ramsey PASS (12 s). networkx clique numbers 2, 2, 9, 2 (colour 2 in 3 parts, 1100 s). Cloud, 7 Nov. |
| R(3,3,3,11) | 597 [6.2.g] | VERIFIED | `R3_3_3_11_n596.colormat.gz` | 596 | verify_ramsey PASS (22.8 s, cloud). networkx colours 0, 1, 3 (cloud) and colour 2 in 4 residue classes, all done, omega 10 (Mac, wave 1). |
| R(3,4,5,5) | 729 [Row2] | VERIFIED | `R3_4_5_5_n728.colormat.gz` | 728 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,5,5,5) | 1,430 [Row5] | VERIFIED | `R3_5_5_5_n1429.colormat.gz` | 1,429 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,6,6) | 338 [Row5] | VERIFIED | `R3_6_6_n337.colormat.gz` | 337 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,7,7) | 674 [Row5] | VERIFIED | `R3_7_7_n673.colormat.gz` | 673 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,8,8) | 941 [Row5] | VERIFIED | `R3_8_8_n940.colormat.gz` | 940 | verify_ramsey PASS and crosscheck_mc PASS. Cloud, 7 Nov. |
| R(3,9,9) | 1,844 [Row5] | VERIFIED | `R3_9_9_n1843.colormat.gz` | 1,843 | verify_ramsey PASS (14 s) and crosscheck_mc PASS (110 s). Cloud, 7 Nov. |

## VERIFIED (symmetry-reduced), both checkers on a reduction by automorphisms verified on the object (21)

| cell | survey bound [ref] | label | witness | n | checks |
|---|---|---|---|---|---|
| R(6,15) | 401 [2.3.i] | VERIFIED (symmetry-reduced) | `R6_15_n400.g6.gz` | 400 | No K6: clique.c and networkx on the whole graph. No independent 15-set: clique.c --sym NONE 14 (54 s) and gen0 on N(0) (38.6 s), 4 automorphism generators and ... |
| R(7,11) | 405 [XXER] | VERIFIED (symmetry-reduced) | `R7_11_n404.g6.gz` | 404 | Vertex transitivity checked on the graph (4 automorphism generators, orbit of vertex 0 is everything). Both checkers on cliques through vertex 0: no K7, clique.c NONE ... |
| R(11,11) | 1,597 [2.2.c] | VERIFIED (symmetry-reduced) | `R11_11_n1596.g6.gz` | 1,596 | Reduced check with verified automorphisms, clique.c and networkx, both colours (10 searches, 908 s, cloud). Full verify_ramsey on both colours, NONE 10 (23039 s and ... |
| R(4,22) | 314 [LinCa] | VERIFIED (symmetry-reduced) | `R4_22_n313.g6.gz` | 313 | verify_ramsey PASS both halves (46 s, cloud). networkx with translation symmetry: clique number 3, independence number 21 (23075 s, Mac, wave 7). |
| R(5,22) | 492 [Ihr] | VERIFIED (symmetry-reduced) | `R5_22_n491.g6.gz` | 491 | verify_ramsey PASS both halves (104.5 s, cloud). Reduced check after verifying x -> x+1 and x -> 2^7 x on the matrix: clique.c and gen0 NONE on all 7 subproblems (cloud, ... |
| R(6,16) | 434 [SLLL] | VERIFIED (symmetry-reduced) | `R6_16_n433.g6.gz` | 433 | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1 (47 vertices), independence side w=3, 7 (195, 187 ... |
| R(6,17) | 548 [SLLL] | VERIFIED (symmetry-reduced) | `R6_17_n547.g6.gz` | 547 | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on ... |
| R(6,18) | 614 [SLLL] | VERIFIED (symmetry-reduced) | `R6_18_n613.g6.gz` | 613 | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on ... |
| R(6,19) | 710 [SLLL] | VERIFIED (symmetry-reduced) | `R6_19_n709.g6.gz` | 709 | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on ... |
| R(6,20) | 878 [SLLL] | VERIFIED (symmetry-reduced) | `R6_20_n877.g6.gz` | 877 | No K6: clique.c and networkx (cloud). No independent 20-set: x -> x+1 and x -> 8x verified on the matrix, 2 orbits of non-neighbours of 0 (reps 2, 3), clique.c NONE 17 ... |
| R(6,22) | 1,070 [SLLL] | VERIFIED (symmetry-reduced) | `R6_22_n1069.g6.gz` | 1,069 | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=3, 7 (475, 479 vertices)). clique.c ... |
| R(7,18) | 797 [2.3.i] | VERIFIED (symmetry-reduced) | `R7_18_n796.g6.gz` | 796 | No K7: clique.c on the whole graph NONE 6 (32 s), networkx on N(0) NONE. No independent 18-set: clique.c --sym NONE 17 (13.6 s) and gen0 on N(0) (10.1 s). 4 automorphism ... |
| R(7,19) | 908 [SLLL] | VERIFIED (symmetry-reduced) | `R7_19_n907.g6.gz` | 907 | Translations and x -> g^3 x verified on the matrix, edge and non-edge orbits through 0 computed (clique side w=1, independence side w=2, 4). clique.c and gen0 NONE on ... |
| R(7,21) | 1,214 [SLLL] | VERIFIED (symmetry-reduced) | `R7_21_n1213.g6.gz` | 1,213 | No K7: clique.c and gen0 NONE (cloud). No independent 21-set: x -> x+1 and x -> 8x verified on the matrix, 2 orbits of non-neighbours of 0 (reps 2, 4). Subproblem w = 2 ... |
| R(3,27) | 172 [LiLi] | VERIFIED (symmetry-reduced) | `R3_27_n171.g6.gz` | 171 | verify_ramsey PASS (circulant, 30.6 s cloud). Negative control (3,26) FAIL as required. networkx with translation symmetry: clique number 2, independence number 26 (8712 ... |
| R(7,7,7) | 3,214 [XuR1] | VERIFIED (symmetry-reduced) | `R7_7_7_n3213.colormat.gz` | 3,213 | Reduced check with verified automorphisms, clique.c and networkx (99 searches, cloud). Full verify_ramsey on all three colours, NONE 6 (about 1200 s each, Mac, waves 5 ... |
| R(5,5,5,5) | 4,073 [Row3] | VERIFIED (symmetry-reduced) | `R5x4_n4072.lengths.gz` | 4,072 | Cyclic (rotation tested). verify_ramsey PASS (11.1 s) and crosscheck_mc PASS (41 s), cliques through vertex 0. Cloud, 7 Nov. |
| R(6,6,6,6) | 23,502 [Row5] | VERIFIED (symmetry-reduced) | `R6x4_n23501.lengths.gz` | 23,501 | Cyclic. Colours 3 and 4: clique.c --sym NONE 5 and linear0 NONE (cloud). Colours 1 and 2: linear0 NONE (545 s, 527 s, Mac, wave 8a) and clique.c NONE 5 (2674 s, 2814 s, ... |
| R(5,5,5,5,5) | 41,626 [Row5] | VERIFIED (symmetry-reduced) | `R5x5_n44337.lengths.gz` | 44,337 | Cyclic, cliques through vertex 0. Colours 3, 4, 5: linear0 and clique.c NONE (cloud). Colour 1: linear0 NONE (290 s, Mac, wave 2) and clique.c NONE 4 (Mac, wave 6). ... |
| R(4,4,4,4,4,4) | 32,006 [Row1] | VERIFIED (symmetry-reduced) | `R4x6_n32005.lengths.gz` | 32,005 | Cyclic, cliques through vertex 0. clique.c --sym NONE 3 in all 6 colours (58 s) and linear0 NONE in all 6 colours. Cloud, 7 Nov. |
| R(4,4,4,4,4,4,4) | 160,024 [Row1] | VERIFIED (symmetry-reduced) | `R4x7_n160023.lengths.gz` | 160,023 | Cyclic, cliques through vertex 0: clique.c on N(0) in each of 7 colours (82 s) and linear0 NONE in all 7 colours (50 s). Cloud, 7 Nov. |

## VERIFIED (by proof: citation), a half or the whole row follows by a published, cited theorem from inputs checked by both checkers (29)

| cell | survey bound [ref] | label | witness | n | checks |
|---|---|---|---|---|---|
| R(7,12) | 417 [XSR2] | VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6) | `R7_12_n416.g6.gz` | 416 | No K7: clique.c NONE and networkx NONE (cloud). No independent 12-set: clique.c NONE 11, 1278 s (Mac, wave 3). networkx reached its 12 h limit (wave 4), not a check. ... |
| R(8,13) | 817 [XXER] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_13_n816.g6.gz` | 816 | No K8: clique.c NONE (7.7 s, cloud) and networkx NONE (446 s, Mac, wave 2). Input (7,7;204): both checkers, whole graph (build_round5). |
| R(8,15) | 873 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_15_n872.g6.gz` | 872 | No K8: clique.c NONE (8.8 s, cloud) and networkx NONE (495 s, Mac, wave 2). Input g78.218: both checkers, whole graph (build_round5). |
| R(10,15) | 1,313 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R10_15_n1312.g6.gz` | 1,312 | No K10: clique.c NONE (2.4 s, cloud) and networkx with verified automorphisms through vertex 0, NONE (250 s, Mac, wave 2). Input (8,9;328): both checkers. |
| R(13,13) | 2,557 [2.2.c] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R13_13_n2556.g6.gz` | 2,556 | Input: omega(Q_1277) = 11, no K_12 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_11 checked edge by edge (cloud 12 Nov). ... |
| R(14,14) | 2,989 [2.2.c] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R14_14_n2988.g6.gz` | 2,988 | Input: omega(Q_1493) = 12, no K_13 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_12 checked edge by edge (cloud 12 Nov). ... |
| R(15,15) | 5,485 [2.2.c] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R15_15_n5484.g6.gz` | 5,484 | Input: omega(Q_2741) = 13, no K_14 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_13 checked edge by edge (cloud 12 Nov). ... |
| R(16,16) | 5,605 [2.2.c] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R16_16_n5604.g6.gz` | 5,604 | Input: omega(Q_2801) = 14, no K_15 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_14 checked edge by edge (cloud 12 Nov). ... |
| R(17,17) | 8,917 [LuSL] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R17_17_n8916.g6.gz` | 8,916 | Input: omega(Q_4457) = 15, no K_16 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_15 checked edge by edge (cloud 7 Nov). |
| R(18,18) | 11,005 [LuSL] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R18_18_n11004.g6.gz` | 11,004 | Input: omega(Q_5501) = 16, no K_17 with clique.c and gen0 on every orbit representative after verified automorphisms, and a K_16 checked edge by edge (Mac wave 8a, 12 ... |
| R(19,19) | 17,885 [LuSL] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R19_19_n17884.g6.gz` | 17,884 | Input: omega(Q_8941) = 17, no K_18 with clique.c and gen0 on every one of the 1117 orbit representatives after verified automorphisms (ordered subproblems, NOTES.md ... |
| R(20,20) | 21,725 [Ex23] | VERIFIED (by proof: Shearer 1986, Lemma 1 pp.302-303 and Thm 1 p.303) | `R20_20_n21724.g6.gz` | 21,724 | Input: omega(Q_10861) = 18, no K_19 with clique.c and gen0 on every one of the 1357 orbit representatives after verified automorphisms (ordered subproblems, NOTES.md ... |
| R(5,21) | 441 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R5_21_n440.g6.gz` | 440 | No K5: clique.c NONE (0.1 s) and networkx NONE (2.4 s), cloud. Input r3.20.110: both checkers, whole graph (build_round5). |
| R(5,23) | 521 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R5_23_n520.g6.gz` | 520 | No K5: clique.c --sym NONE 4 and networkx on N(0), after 4 automorphisms checked (cloud). Input (3,22;130): both checkers (build_round5). |
| R(6,21) | 888 [2.3.h] | VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6) | `R6_21_n887.g6.gz` | 887 | No K6: clique.c and networkx on the whole graph, no symmetry (cloud, 12 Nov). Exact reduction alpha(F) <= alpha(G) + 1 checked on the object. Input alpha(G) <= 19: both ... |
| R(7,16) | 629 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R7_16_n628.g6.gz` | 628 | No K7: clique.c NONE (12.6 s, cloud) and networkx NONE (580 s, Mac, wave 2). Independent 16-set: clique.c NONE 15 (1076 s, Mac, wave 3), networkx reached its 12 h limit ... |
| R(7,17) | 729 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R7_17_n728.g6.gz` | 728 | Vertex transitivity checked. No K7: clique.c NONE and networkx NONE (cloud). Input (6,9;182): both checkers, whole graph (build_round5). |
| R(8,17) | 1,005 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_17_n1004.g6.gz` | 1,004 | Vertex transitivity checked. No K8: clique.c NONE (0.2 s) and networkx NONE (5.0 s), cloud. Input (7,9;251): both checkers (build_round5). |
| R(8,19) | 1,237 [2.2.h] | VERIFIED (by proof: XSR2 Thm 3, preprint pp.4-5) | `R8_19_n1236.g6.gz` | 1,236 | No K8: clique.c NONE (34 s, cloud) and networkx NONE (1848 s, Mac, wave 2). Inputs: (8,13;816) row R(8,13), (7,8;216) both checkers on both halves. |
| R(8,21) | 1,617 [2.3.i] | VERIFIED (by proof: XXER Thm 9, pp.15-16) | `R8_21_n1616.g6.gz` | 1,616 | Vertex transitivity checked (7 generators). No K8: clique.c NONE (0.3 s) and networkx NONE (5.6 s), cloud. Input (7,11;404): both checkers on both halves. |
| R(9,9,9) | 15,041 [Row5] | VERIFIED (by proof: XXER Cor. 5, p.15) | `R9_9_9_n15040.colormat.gz` | 15,040 | Colours 1 and 2: 7 automorphism generators and transitivity checked, clique.c NONE 7 and gen0 NONE on N(0) (Mac, wave 8a). Input (3,8,8;940): verify_ramsey and ... |
| R(10,10,10) | 23,094 [Row5] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R10_10_10_n23093.lengths.gz` | 23,093 | Colours 2 and 3: linear0 NONE (Mac, wave 8a) and clique.c NONE 9 (Mac, wave 8b). Colour 1 on the 253-vertex window the theorem leaves: clique.c, gen0 and linear0 NONE ... |
| R(7,7,7,7) | 94,874 [Row5] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R7x4_n94873.lengths.gz` | 94,873 | Inputs U and V: clique.c and gen0 on every colour, whole graph, with lowered-k controls. Template colour checked triangle-free and containing length m-1, phi and N ... |
| R(8,8,8,8) | 182,002 [Row5] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R8x4_n182001.lengths.gz` | 182,001 | Inputs U and V: clique.c and gen0 on every colour, whole graph, with lowered-k controls. Template colour checked triangle-free and containing length m-1, phi and N ... |
| R(9,9,9,9) | 719,204 [Row5] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R9x4_n719203.lengths.gz` | 719,203 | Inputs. U (9,9,3;1282): colours 1, 2 clique.c and gen0 through vertex 0 with lowered-k controls (the whole-graph run did not finish in 140 s), colour 3 both checkers on ... |
| R(6,6,6,6,6) | 258,506 [Row5] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R6x5_n258505.lengths.gz` | 258,505 | Inputs U and V: clique.c and gen0 on every colour, whole graph, with lowered-k controls. Template colour checked triangle-free and containing length m-1, phi and N ... |
| R(5,5,5,5,5,5) | 441,606 [Row5] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R5x6_n441605.lengths.gz` | 441,605 | Inputs U and V: clique.c and gen0 on every colour, whole graph, with lowered-k controls. Template colour checked triangle-free and containing length m-1, phi and N ... |
| R(8,8,9) | 10,769 [Row5] | VERIFIED (by proof: XXER Cor. 5, p.15) | `R8_8_9_n10768.colormat.gz` | 10,768 | Vertex-transitive (7 automorphisms checked). Colours 1 and 2: no K7 in N(0), clique.c (37 s, 32 s) and gen0 (39 s, 35 s), cloud. Input (3,7,7;673): verify_ramsey and ... |
| R(6,6,6,6,6,6) | 4,515,702 [Row2/Row3 (linear Ramsey graphs)] | VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2, pp.248-250) | `R6x6_n5499101.lengths.gz` | 5,499,101 | Inputs U and V: clique.c and gen0 on every colour, whole graph, with lowered-k controls. Template colour checked triangle-free and containing length m-1, phi and N ... |

## VERIFIED (witness found here by search), the witness or its input found here by search (Amendments 2 and 6), every colour checked by both checkers (4)

| cell | survey bound [ref] | label | witness | n | checks |
|---|---|---|---|---|---|
| R(4,10) | 92 [HaKr1] | VERIFIED (witness found here by search) | `R4_10_n91.g6.gz` | 91 | verify_ramsey PASS (circulant). networkx, whole graph, no symmetry: clique number 3, independence number 9. Cloud, 7 Nov. |
| R(5,8) | 101 [HaKr1] | VERIFIED (witness found here by search) | `R5_8_n100.g6.gz` | 100 | verify_ramsey PASS (circulant). networkx, whole graph, no symmetry: clique number 4, independence number 7. Cloud, 7 Nov. |
| R(4,17) | 200 [Lia+] | VERIFIED (witness found here by search) | `R4_17_n199.g6.gz` | 199 | verify_ramsey PASS (circulant). networkx: clique number 3 on the whole graph, independence number 16 through vertex 0 (circulant). Cloud, 7 Nov. |
| R(3,3,3,7) | 247 [6.2.h (derived, unpublished explicit)] | VERIFIED (witness found here by search) | `R3_3_3_7_n246.colormat.gz` | 246 | Input (3,3,7;80): verify_ramsey PASS (circulant), and clique.c and gen0 on every colour, whole graph: NONE 2, NONE 2, NONE 6. Witness (3,3,3,7;246): verify_ramsey PASS ... |

## RECIPE ONLY (3)

| cell | survey bound [ref] | label | what there is | notes |
|---|---|---|---|---|
| R(21,21) | 30,925 [Ex23] | RECIPE ONLY | built in the cloud as graph6 (2p+2 = 30924 vertices), not checked, not committed | The file can be rebuilt with the doubling rule of the R(13,13) to R(18,18) rows. Expected SHA-256 of the built file is in phase2/recipes.csv. |
| R(22,22) | 39,109 [Ex23] | RECIPE ONLY | built in the cloud as graph6 (2p+2 = 39108 vertices), not checked, not committed | The file can be rebuilt with the doubling rule of the R(13,13) to R(18,18) rows. Expected SHA-256 of the built file is in phase2/recipes.csv. |
| R(23,23) | 49,421 [Ex23] | RECIPE ONLY | formula only, no file written (49,420 vertices) | The file can be rebuilt with the doubling rule of the R(13,13) to R(18,18) rows. Expected SHA-256 of the built file is in phase2/recipes.csv. |

## NOT REPRODUCED (5)

| cell | survey bound [ref] | label | what there is | notes |
|---|---|---|---|---|
| R(5,17) | 388 [XSR2] | NOT REPRODUCED | G387 built from the text with the code that reproduced R(7,7,7) | See NOTES.md. Restricted to the 384-vertex core, one colour class is K5-free with independence number 16, which gives 385. |
| R(5,19) | 411 [XSR2] | NOT REPRODUCED | needs G387, see row R(5,17) | See NOTES.md. |
| R(5,20) | 424 [XSR2] | NOT REPRODUCED | needs G387, see row R(5,17) | See NOTES.md. |
| R(8,8,8) | 7,174 [Row5] | NOT REPRODUCED | the (8,9,8;10768) colouring of row R(8,8,9) built from the public (3,7,7;673) | See NOTES.md. |
| R(3,3,3,5) | 162 [XXER] | NOT REPRODUCED | merges tested on every public and every symmetric S(5) partition | See NOTES.md, sections 2 and 9. No partition file was captured on Exoo's pages. Search S1 did not find one (phase2/search_s1/SEARCH_RECORD.md). |

## STILL NO FILE (8)

| cell | survey bound [ref] | label | what there is | notes |
|---|---|---|---|---|
| R(6,13) | 347 [Kuz] | STILL NO FILE | searched in four rounds (phase2/search_records/) | The paper states a cyclic (6,13;346) colouring. Its data were not printed and were not found. Search S1 did not find one (phase2/search_s1/SEARCH_RECORD.md). |
| R(3,23) | 139 [XWCS] | STILL NO FILE | searched in four rounds (phase2/search_records/) | No public version found. |
| R(5,18) | 396 [2.3.h] | STILL NO FILE | not built: the input G387 was not reproduced (row R(5,17)) |  |
| R(3,3,7) | 85 [Ex18] | STILL NO FILE | searched in four rounds. In the fourth every Wayback Machine capture of Exoo's Ramsey pages on cs.indstate.edu, ... | No 84-vertex file was captured. The largest (3,3,7) files in the fullest captured listing have 80 vertices (g337.80a to g337.80e), and the older g337.78 is ... |
| R(3,3,8) | 103 [Ex18] | STILL NO FILE | searched in four rounds. In the fourth every Wayback Machine capture of Exoo's Ramsey pages on cs.indstate.edu, ... | No 102-vertex file was captured. The largest in the fullest captured listing is g338.100. Search S1 did not find one (phase2/search_s1/SEARCH_RECORD.md). |
| R(3,4,6) | 117 [Ex17] | STILL NO FILE | searched in four rounds. In the fourth every Wayback Machine capture of Exoo's Ramsey pages on cs.indstate.edu, ... | No 116-vertex file was captured. The largest in the fullest captured listing is g346.108. Search S1 did not find one (phase2/search_s1/SEARCH_RECORD.md). |
| R(3,3,3,4) | 97 [Ex17] | STILL NO FILE | searched in four rounds. In the fourth every Wayback Machine capture of Exoo's Ramsey pages on cs.indstate.edu, ... | No 96-vertex file was captured. Only g3334.92 and an older cyclic colouring on 86 vertices are public. Search S1 did not find one ... |
| R(3,10,10) | 2,841 [Row5] | STILL NO FILE | searched in four rounds (phase2/search_records/) | Neither the text, the tables nor the spreadsheet of Row5 contain a (3,10,10) or (10,10,3) colouring. |
