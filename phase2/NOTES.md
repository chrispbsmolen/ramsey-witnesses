# Notes on phase 2

Observations made while building and checking the phase-2 witnesses, with the evidence for each. They are
statements about what could be reproduced here from the public text, on the dates given. None of them is a claim
that a published bound is wrong. Corrections are welcome (see `CORRECTIONS.md` at the top of the repository).

## 1. A misprint in Shearer 1986, Theorem 1

J. B. Shearer, Lower bounds for small diagonal Ramsey numbers, J. Combin. Theory Ser. A 42 (1986) 302-304,
https://doi.org/10.1016/0097-3165(86)90102-0 (Elsevier open archive).

Theorem 1 (p.303) is printed as "If c(G_p) = p then R_2(k+2) > 2p+2". The condition should read c(G_p) = k:

- the abstract (p.302) states R_2(k+2) > 2p+2 with k = c(G_p),
- the proof uses only Lemma 1 (pp.302-303, c(H_p) = c(G_p) + 1 = k + 1) and the isomorphism between the
  complement of H_p and H_p with the edges (x, x') deleted, and neither needs c(G_p) = p.

The rows R(13,13) to R(18,18) use the theorem with c(G_p) = k. For each of them the clique number of the Paley
graph Q_p was checked here with two checkers, the doubled graph was rebuilt byte for byte from the definition on
p.302, and the isomorphism from the proof was checked on the object edge by edge (`certificates/CERTIFICATES.md`).

## 2. Constructions not reproduced from the text

### R(3,3,3,5) >= 162

Source: Xu, Xie, Exoo, Radziszowski, Electron. J. Combin. 11 (2004) #R35, pp.2-3. The paper merges two colors of an
Exoo (3,3,3,3,3;161) coloring to get a (3,3,3,5;161) coloring, and says no other combination of colors gives an
improvement.

What was tried here, and found:

- Exoo's partition printed in Electron. J. Combin. 1 (1994) #R8 p.2: each of the 10 merges of two colors leaves a K5
  in the merged color (both checkers).
- Heule's palindromic S(5) = 160 certificate (arXiv:1711.08076, Fig. 1): each of the 10 merges contains a K5.
- All 5,840 symmetric sum-free 5-partitions of [1,160] (the count agrees with Fredricksen and Sweet, Electron. J.
  Combin. 7 (2000) #R32 p.5): none of the 58,400 merges is K5-free in the merged color.
- 38,424 non-symmetric partitions one move away from the two public ones, and every 5-color partition of [1,160]
  obtained from larger public sum-free partitions (Rowley arXiv:2107.03560, Fredricksen and Sweet, Chen, Zhu and Long
  arXiv:2610.31362): none works.

Exoo 1994 p.2 mentions about 10,000 partitions, most of them unpublished, so the coloring used in XXER may be one of
those. Evidence: `checks/logs/hunt_multicolour/logs/*xxer_merge*`, `checks/logs/hunt2_multicolour/logs/`,
`checks/logs/hunt3_multicolour/logs/`.

### The graph G387 behind R(5,17), R(5,18), R(5,19), R(5,20)

Source: Xu, Shao, Radziszowski, SIAM J. Discrete Math. 25 (2011) 394-400 (preprint
https://www.cs.rit.edu/~spr/PUBL/paper68.pdf), Thm 5 proof p.7 and Table 1 p.7. G387 is described as one color of
the tripling construction with p = 127 of Xu and Radziszowski, Electron. J. Combin. 16 (2009) #N1, pp.2-4.

What was found here:

- The 387-vertex coloring M'_127 was built from the text with the same code that reproduced R(7,7,7) >= 3214 from
  that paper.
- Every color class is K5-free, but in every color, and for every way of recoloring the special edges, the union
  of the other two colors contains a K17 (clique.c FOUND, the set rechecked edge by edge). So no color class is a
  (5,17;387) graph as built.
- A counting reason: in each color two of the six added vertices are complete to the same block of 127 vertices,
  and the edge between them then lies in either a K5 or an independent 17-set.
- Restricted to the 384-vertex core, one color class is K5-free with independence number exactly 16, which gives
  R(5,17) >= 385.

R(5,19) and R(5,20) use G387 directly (XSR2 Table 1). R(5,18) is built from G387 (survey item 2.3.h) and was not
attempted. Evidence: `checks/logs/hunt2_two_colour/logs/g387_structure*.txt`, `checks/logs/build_round2/logs/r5_17.jsonl`.

### R(8,8,8) >= 7174

Source: Rowley, arXiv:2203.13476v3, Section 6, with the quadrupling of XXER Cor. 5 p.15. The route needs a
(3,7,7;673) coloring whose triangle-free color has degree 273.

What was found here:

- The public cyclic (3,7,7;673) coloring (Rowley's spreadsheet, column 19, row R(3,7,7) here) has triangle-free
  degree 198. Quadrupling it twice gives the (8,9,8;10768) coloring of row R(8,8,9), whose K9-free color is
  6497-regular, so its neighborhoods give (8,8,8;6497) only.
- Counting degrees through the two steps gives 9 d1 + 7 x 673 + 4 for the neighborhood size, where the text has
  + 5. With d1 = 273 this is 7172, one less than the 7173 vertices needed. This is arithmetic only and may reflect a
  different graph or a step not written out.

Evidence: `checks/logs/build_round2/` and the R(3,7,7) and R(8,8,9) rows.

## 3. Reading of printed tables

- Kreher, Li, Radziszowski, J. Combin. Math. Combin. Comput. 4 (1988), Table IV rows 13 and 18 are not partitions of
  1..27 as printed (row 13 repeats 3 and lacks 5, row 18 repeats 24 and lacks 22). They are color-swapped copies of
  rows 4 and 9 and were not used. Row 1 of Tables III and V gives the witnesses here.
- Ageron et al., arXiv:2112.03175v2, Table 6 as printed omits the element 49. Exactly two colors keep the S-template
  conditions with it added, one of them was used, and the finished coloring of R(3^9) is checked directly.
- Rowley's spreadsheet (arXiv:2203.13476v3), column 25, has the header ORDER = 8001, while Table 1 gives order 1282.
  The parameter block of the column also gives 1282, and the header value is the order of a test compound further
  down the sheet. The first 1281 lengths were used for R(9,9,9,9) and checked as a (9,9,3;1282) coloring.

## 4. Witnesses taken from a different paper than the one the survey cites

These rows count the cell because a public witness of the survey's strength was checked. The survey reference is
kept in the table, and the source column names the paper actually used.

| cell | survey reference | witness from |
|---|---|---|
| R(3,21), R(3,22) | W1+, W2+ (manuscripts) | Wu, Su, Luo, Xu, Electron. J. Combin. 17 (2010) #N25 |
| R(3,3,4) | Ka2 | Codish, Frank, Itzhakov, Miller, arXiv:1510.08266, Fig. 3 |
| R(3,3,5) | Ex2 | Kreher, Li, Radziszowski 1988, Table III |
| R(3,5,5), R(3,5,6) | Ex17 | Courties, github.com/JuloJC/multicolour-ramsey-numbers (CC0) |
| R(3,4,5,5) | Row2 | Rowley, arXiv:2203.13476v3 spreadsheet |
| R(3^8) | Row3 | Ageron et al., arXiv:2112.03175v2, Table 5 |

## 5. Witnesses found here by search (Amendments 2 and 6 of the registration)

For R(4,10) >= 92, R(5,8) >= 101 and R(4,17) >= 200 the cited colorings (Harborth and Krause, HaKr1, and LiaWXS)
are not public. The witnesses here were found by a short circulant tabu search (R(4,10), R(5,8)) and by a scan of
unions of cyclotomic classes mod 199 (R(4,17)). Their rows are labeled "VERIFIED (witness found here by search)" and the files say so, and the search
scripts are in `scripts_as_run/hunt3_two_colour/` with their SHA-256 in `scripts_as_run/INDEX.csv`. R(6,15) and
R(7,18) are built from two of these witnesses by the survey's construction and carry the same label on their input.

Under Amendment 6 (12 November, a registered search for the lost cells, rules in `README.md`), a SAT search on
Z_80 found a cyclic (3,3,7;80) coloring. Robertson's construction (Electron. J. Combin. 6 (1999) #R3, Part Two)
turns it into a (3,3,3,7;246) coloring, so R(3,3,3,7) >= 247, the survey's value (item 6.2.h). The row is labeled
"VERIFIED (witness found here by search)". The (3,3,7;80) coloring is not Exoo's (3,3,7;84) coloring, which is not
public, and it does not reach the survey's value for R(3,3,7) itself. The search run (scripts, python-sat and CaDiCaL
versions, log entries) is recorded in `search_s1/SEARCH_RECORD.md`.

The search ended on 13 November. It also found a cyclic (3,3,7;81) coloring, which is below the survey's value for
R(3,3,7) as well and is not used in any row. For the other targets (R(6,13), R(3,3,7), R(3,4,6),
R(3,3,8), R(3,3,3,4), R(3,3,3,5), R(3,14)) the search found no witness. `search_s1/SEARCH_RECORD.md` lists for each of
them the symmetric forms that were excluded exactly and the runs that ended undecided. An exact negative holds only
for the form stated. For example, there is no (3,14;66) Cayley graph on any of the four groups of order 66, while
Kolodyazhny's (3,14;66) graph, which is not a Cayley graph, is the witness of row R(3,14).

## 6. Choices made in builds

- R(8,19): XSR2 Thm 3 needs a "properly chosen H" (survey 2.2.h). H here is the complement of the (7,8;216) graph
  built from XSR2 Thm 4. This is a reading of the text.
- R(3,3,3,10): the input is the first 128 vertices of the Lachy-Dauth R(3,3,9) circulant (repository
  `third_party/lachy-dauth/`). The full 132-vertex input would give 528 vertices.
- R(6,6,6,6,6,6): the object follows the 5,499,101-vertex route of Rowley, arXiv:2203.13476v3 Table 2, not the
  survey's recipe (Row2/Row3 with a (6,6,3;213) template that is not printed). Its first 4,515,701 vertices give the
  survey's value.
- R(5,5,5): the file is Exoo's coloring as published by Courties (CC0). Rowley's spreadsheet has the same coloring
  (first 453 vertices of column 27), and the two agree byte for byte after relabeling.

## 7. Third-party claims noted, not counted

These files or papers give more than the survey's value. They are recorded here only. The table counts each cell at
the survey's value.

The intake registration (`registration/REGISTRATION_intake.md`) applies to this section from the commit that adds it.
The third-party files and claims that phase 2 recorded only in its notes, search records or check logs stay there, and
each is entered when its file has been fetched at a fixed address and checked here.
The table below is kept as it was written.

| cell | claim | where | check here |
|---|---|---|---|
| R(5,15) | >= 283 (and >= 279) | arhancanli/quantavane-ramsey-records (CC BY 4.0), Zenodo 10.5281/zenodo.23920916 | the 282-vertex file passed both checkers |
| R(3,5,5) | >= 140 | Courties repository, 139-vertex cyclic file (unrefereed, November 2026) | passed both checkers |
| R(3,5,6) | >= 192 | Courties repository, 191 vertices | passed both checkers |
| R(3,5,7) | >= 267 | Courties repository, 266 vertices | passed both checkers |
| R(3,4,5,5) | >= 770 | Courties repository, 769 vertices | passed both checkers |
| R(5,5,5,5,5) | >= 44,338 | Courties repository, 44,337 vertices | this file is the witness of the row, checked as stated there |
| R(4,20), R(4,21) | >= 252 | arXiv:2608.18169 | not checked |
| R(3^8) | S(8) >= 5362 | Helbert, arXiv:2607.15034 (no data file) | not checked |

## 8. Count

The working tally of 12 November 20:30 Chicago gave 77 VERIFIED. Counting the table row by row gave 78 at that
point, and 84 after the six Rowley rows (five VERIFIED, R(9,9,9,9) PARTIAL) and the search find for R(3,3,3,7). The
difference of one is R(6,20): it became VERIFIED (symmetry-reduced) under Amendment 5 at 18:46, and it is one of the 105
cells, but it was not added to the running count at that step. The table counts it.

On 13 November two rows moved, and the count is 86: R(9,9,9,9) (the window search finished, VERIFIED by proof) and
R(3,14) (Kolodyazhny's graph found in the Wayback Machine, VERIFIED).

On 14 November three rows moved, and the count is 89: R(7,21) (the last reduced subproblem decided by the second
checker, VERIFIED symmetry-reduced), and R(19,19) and R(20,20) (the clique numbers of the Paley graphs on 8941 and
10861 vertices checked, VERIFIED by proof, see section 10).

## 9. The cells that rest on colorings by Exoo that are not public (fourth search round, 13 November)

The survey cites personal communications of Exoo for R(3,3,7) >= 85 and R(3,3,8) >= 103 (Ex18) and for
R(3,4,6) >= 117 and R(3,3,3,4) >= 97 (Ex17). R(3,3,3,5) >= 162 (XXER) uses a (3,3,3,3,3;161) coloring by Exoo that
is not printed (section 2). The fourth search round looked for these files in the Wayback Machine:

- every capture of every address under /ge/RAMSEY on cs.indstate.edu (210 captures), isu.indstate.edu (576) and
  ginger.indstate.edu (1736), and under isu.indstate.edu/~gexoo (25), was listed,
- all 23 distinct versions of the index pages (2001 to 2026) and all 6 versions of the ExTa/ directory listing were
  read,
- the three hosts were searched for other addresses containing 337, 338, 346, 3334, 3335 or "schur".

No file with 84, 102, 116, 96 or 161 vertices appears in any capture. The fullest directory listing (ginger, 16 May
2015, 63 files) has g337.80a to g337.80e, g338.100 and g346.108, and the index pages link g337.78 and g3334.92. So
these five colorings could not be checked here. Four rows stay STILL NO FILE and R(3,3,3,5) stays NOT REPRODUCED.
This is a statement about which files are public, and nothing else. The record is `search_records/hunt4__sources.csv`,
and the SHA-256 of every listing and page that was read is in `checks/logs/hunt4/downloads_SHA256SUMS.txt`.

The same round found Kolodyazhny's page in the Wayback Machine (row R(3,14)). For R(6,13), R(3,23), R(5,17) to R(5,20), R(8,8,8) and R(3,10,10) it found nothing new.

## 10. The ordered subproblems behind R(19,19) and R(20,20)

For R(13,13) to R(18,18) the clique number of the Paley graph G_p was checked as follows (`build_round5`). The maps
x -> x + 1 and x -> g^2 x are automorphisms and together move every edge to {0, 1}. With B the common neighbors of
0 and 1, the map sigma: x -> 1 - x fixes the edge {0, 1} and maps B to itself. So G_p has a K_(k+1) exactly when, for
some representative a of an orbit {a, 1 - a} of sigma on B, the common neighbors of 0, 1 and a hold a K_(k-2). Both
checkers ran on that set for every representative.

For p = 8941 and p = 10861 one more step was used. Number the orbits of sigma on B in increasing order of their least
element, and write idx(x) for the number of the orbit of x. Take a K_(k+1) through 0 and 1, and among its other
vertices one, x, of least idx. If x is not the representative of its orbit, apply sigma to the clique. It is again
a clique through 0 and 1, with the same idx values, and it now holds the representative. So a K_(k+1) exists exactly
when, for some i, the vertices y of B that are adjacent to the i-th representative and have idx(y) >= i hold a
K_(k-2). This uses sigma only. The subproblems become smaller as i grows, and the total work is about a ninth.

Before any search the script checks on the graph that x -> x + 1 and x -> g^2 x are automorphisms, that the second
is transitive on the squares, that sigma maps B to itself, that the representatives cover B, and that idx is constant
on the orbits of sigma. Every representative needs the answer NONE from clique.c and from gen0, on byte-identical
input, and the final step checks that every piece is recorded exactly once with the input hash it recomputes from p
alone. On p = 101 the ordered and the plain form both pass, and on p = 1277 the ordered form gives the value of the R(13,13)
row. With the wanted size lowered by one the script reports the clique that exists. The script is `scripts_as_run/mac_batch/wave9/paley/paley9.py`.

This step was not in the registration when the run for p = 8941 started on 13 November. The script was fixed before
the run and was not changed after it, and the amendment that describes the step was written the same evening, after
that run and before the result was counted. The run for p = 10861 followed. The plain form can be run with the same
script (`W9_MODE=plain`) and takes about nine times as long.

Results: c(G_8941) = 17 (1117 representatives, 2234 pieces, the largest on 1122 vertices, 9.4 hours of solver time)
and c(G_10861) = 18 (1357 representatives, 2714 pieces, the largest on 1375 vertices, 42.4 hours of solver time).
These are the values published by Luo, Su and Li (2002) and by Exoo.
