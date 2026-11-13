# Certificates for the rows labelled VERIFIED (by proof: citation)

In these 21 rows one half, one colour or the whole row follows from a published theorem. The rule (Amendments 3 and 4
of the phase-2 registration) is that the theorem is cited with page, that every input it is applied to was checked
here by both checkers, and that every computed part was checked by both checkers. Where a whole row rests on the
theorem, the object was also rebuilt from its hashed inputs, the hypotheses of the theorem were checked, and the
rebuild was matched to the committed file by SHA-256.

Files in this folder (copies of records also kept in `../checks/logs/`):

| file | what it records |
|---|---|
| `rebuild_certificates.jsonl` | rebuild certificates: R(13,13) to R(18,18) (Shearer), R(7,16) (XXER Thm 9), R(10,10,10) (Rowley Thm 3.2), and the control p = 101 |
| `paley_omega_inputs.jsonl` | the inputs c(Q_p) for the Shearer rows: verified automorphisms, both checkers on every orbit representative, K_k witnesses, negative controls |
| `rowley_r10_window.jsonl` | the 253-vertex window that Rowley Thm 3.2 leaves for colour 1 of R(10,10,10), checked by clique.c, gen0 and linear0, with a K9 control |
| `inputs_both_checkers.jsonl` | the inputs of the XXER Thm 9 rows, each rerun with both checkers on the whole graph and matched to its pinned SHA-256 |
| `xsr2_reduction_G3.jsonl`, `xsr2_reduction_6_21.jsonl` | the exact reduction alpha(F) <= alpha(G) + 1 of XSR2 Thm 3, checked on the object |
| `two_implementations_G3.json`, `two_implementations_round4.jsonl` | every built graph was produced by two separate implementations and the two agree edge for edge |

The scripts that wrote these records are in `../scripts_as_run/build_round5/scripts/` (`cert_shearer.py`,
`cert_xxer_t9.py`, `cert_rowley_r10.py`, `paley_check.py`, `r10_window.py`, `confirm_inputs.py`),
`../scripts_as_run/build_round4/src/` and `../scripts_as_run/build_G3/`. They are kept as they were run. Paths inside
them point to the working folders of 7 to 12 November.

## Rows that rest entirely on a theorem (Amendment 4)

| cell | theorem | hypotheses and inputs checked | rebuild |
|---|---|---|---|
| R(13,13) | Shearer, J. Combin. Theory Ser. A 42 (1986), Lemma 1 pp.302-303, Thm 1 p.303 | p = 1277 prime, p = 1 mod 4, c(Q_1277) = 11 (no K12 with clique.c and gen0 on all 159 orbit representatives, a K11 checked edge by edge) | graph6 rebuilt from the definition on p.302, byte-identical (sha256 fd8c9020... uncompressed), complement mapped onto H_p edge by edge |
| R(14,14) | same | p = 1493, c = 12, 186 representatives | identical (5e982735...) |
| R(15,15) | same | p = 2741, c = 13, 342 representatives | identical (85376258...) |
| R(16,16) | same | p = 2801, c = 14, 350 representatives | identical (eebd70ad...) |
| R(17,17) | same, with c(Q_4457) = 15 from Luo, Su, Li, Australas. J. Combin. 25 (2002) Thm 2 | both checkers on all 557 representatives (cloud, 7 Nov), automorphisms rechecked 12 Nov | identical (7c3b5e70...) |
| R(18,18) | same, with c(Q_5501) = 16 from Luo, Su, Li | gen0 and clique.c on all 687 representatives (Mac, wave 8a, 2566 s and 2571 s) | identical (20de6f9e...) |

Control: the repository file `constructions/witnesses/mathon101_R7_7.g6` (p = 101) is certified the same way, and
both checkers find a K6 and no K7 in it and in its complement. Theorem 1 is used with c(G_p) = k (see `../NOTES.md`,
section 1).

## Rows where one half or one colour rests on a theorem (Amendment 3)

| cell | theorem | computed parts (both checkers) | inputs (both checkers) | build evidence |
|---|---|---|---|---|
| R(7,12) | XSR2 Thm 3, preprint pp.4-5, Cor. 3 p.6 | no K7 | (7,11;404) graph, both halves | two implementations agree. Reduction alpha <= alpha(G) + 1 checked on the object (14 subproblems) |
| R(8,13) | XXER Thm 9, pp.15-16 | no K8 | Mathon (7,7;204) | two implementations agree |
| R(8,15) | XXER Thm 9 | no K8 | Tatarevic g78.218 | two implementations agree |
| R(10,15) | XXER Thm 9 | no K10 (networkx through vertex 0 with verified automorphisms) | Kuznetsov (8,9;328) | two implementations agree |
| R(5,21) | XXER Thm 9, (14) p.16 | no K5 | Exoo r3.20.110 | two implementations agree |
| R(5,23) | XXER Thm 9 | no K5 (through vertex 0, 4 automorphisms verified) | WSLX2 (3,22;130) | built with the same code |
| R(6,21) | XSR2 Thm 3 and Cor. 3, preprint pp.4-6 | no K6, whole graph, no symmetry | SLLL (6,20;877), row R(6,20) | two implementations agree. Reduction checked on the object |
| R(7,16) | XXER Thm 9 | no K7 | Tatarevic g415.157 | rebuilt from the text, byte-identical to the row file (rebuild_certificates.jsonl) |
| R(7,17) | XXER Thm 9 | no K7 | Kuznetsov (6,9;182) | two implementations agree |
| R(8,17) | XXER Thm 9 | no K8 | Kuznetsov (7,9;251) | two implementations agree |
| R(8,19) | XSR2 Thm 3, pp.4-6 | no K8 | (8,13;816) of row R(8,13), (7,8;216) both halves | two implementations agree |
| R(8,21) | XXER Thm 9 | no K8 | (7,11;404) graph | two implementations agree |
| R(9,9,9) | XXER Cor. 5 p.15 | colours 1 and 2 (Mac, wave 8a) | Rowley (3,8,8;940) | 7 automorphisms verified |
| R(8,8,9) | XXER Cor. 5 p.15 | colours 1 and 2 (cloud) | Rowley (3,7,7;673) | 7 automorphisms verified |
| R(10,10,10) | Rowley, Australas. J. Combin. 81(2) Thm 3.2, pp.248-250 | colours 2 and 3 (Mac, waves 8a and 8b), colour 1 window (cloud) | template (10,3;30) (sheet sha256 53f2bf9d...), Q_797 | length file rebuilt from the proof text, byte-identical (7c26d120...) |

For R(7,12) and R(7,16) one checker also ran the independence half directly on the object (clique.c, Mac, wave 3),
and found no forbidden set. networkx did not finish those runs in 12 hours, so they are recorded as extra evidence
only.
