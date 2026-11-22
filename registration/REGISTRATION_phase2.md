# Registration: Ramsey phase 2, build the RECIPE cells and hunt files for the rest (approved 7 Nov 2026)

Public edition. The text is the original, word for word and in its original spelling, except where a line is marked
[edited]. Each edit is listed in `registration/EDITS.md` with its reason, and the SHA-256 of the full original is
recorded there.

Written 7 Nov 2026 before any computation. [edited: a reference to a private working file and a working note are removed.]

Why: [edited: a commitment made in private correspondence is summarized, not quoted] the plan was to start with the
cells that have a published construction and then track down files [edited: a reference to a private working file is
removed].

Scope IN: the 32 cells marked RECIPE in results/coverage.csv of ramsey-witnesses (bundle 2026-11-04). Three groups:
- G1, multicolour constructions (8 cells): R(3,3,3,3) >= 51 (Chung recursion), R(3,4,8) >= 193, R(3,5,7) >= 241, R(3,3,3,10) >= 513, R(3,3,3,11) >= 597, R(3,3,3,7) >= 247 (survey 6.2.g/6.2.h), R(3,4,4,4) >= 381 (6.2.j), R(7,7,7) >= 3214 (Mathon cyclotomic, XuR1).
- G2, Paley doubling (Mathon, survey 2.2.c) (5 cells): R(11,11) >= 1597, R(13,13) >= 2557, R(14,14) >= 2989, R(15,15) >= 5485, R(16,16) >= 5605.
- G3, constructions glued from other witnesses (survey 2.3.h, 2.3.i, 2.2.h; papers XXER, XSR2) (19 cells): (5,15), (6,15), (7,11), (7,12), (8,11), (8,13), (8,15), (9,10), (10,15), (5,18), (5,21), (5,23), (6,21), (7,16), (7,17), (7,18), (8,17), (8,19), (8,21).
Scope OUT: any claim that a survey bound is wrong; new search for better bounds.
Also IN (added at approval): a file hunt for the 73 NO_FILE_FOUND cells, run in parallel [edited: working-process detail removed] (papers, authors' pages, repositories, data supplements, theses). A found file is fetched and verified, never just linked on faith.

Step 0, prior-art gate (before building): recheck House of Graphs Ramsey collection, google-research ramsey_number_bounds, Lachy-Dauth, Exoo's site, McKay's page and the 2026 literature for public files of these 32 cells. Any cell found there moves to the file-hunt list instead of being built.

Method: build each graph or colouring exactly as the cited construction says, from the paper's text (each step cited to page). Verify with the existing verify_ramsey.py and the independent crosscheck.py.
Tiers (unchanged): VERIFIED both halves checked here; PARTIAL one half checked (expected for the largest graphs, where the clique search is too heavy); RECIPE stays RECIPE if the construction cannot be reproduced from the paper.
Compute: build and small checks in the cloud. Any heavy clique search goes to the Mac as Terminal commands Christopher runs himself, with tested time, core (4 max) and memory estimates. No runners, no background jobs.
Order: G1 first (smallest, quickest wins), then G2, then G3.

Kill criteria:
- a built graph fails the property the paper claims for it: stop that cell, recheck the construction against the paper twice, and if it still fails record it as "not reproduced from the text" (not as an error in the survey) and consider asking the author, at most one or two cells [edited: a limit stated in private correspondence is not attributed].
- verify_ramsey.py and crosscheck.py disagree on any graph: nothing from that run goes in the VERIFIED tier.
- a cell whose verification would take more than about a day of Mac time at 4 cores: PARTIAL, not attempted further.

Output: new rows in the ramsey-witnesses repository (Christopher approves each push), updated coverage table and the count of cells still without a public witness. [edited: a planned private message is removed.]

Approval: Christopher, 7 Nov 2026 15:21 Chicago [edited: the wording of a private message is removed], read as approval of this registration with the file hunt run in parallel.

## Amendment 1 (7 Nov 2026 17:42 Chicago): what counts as VERIFIED
Decided under Christopher's delegation [edited: the wording of a private message and how the decision was carried out are removed]. Decision:
- VERIFIED: every half checked by both independent checkers on the actual object. A check may be reduced by symmetry only if the automorphisms used were themselves verified on the object's matrix (each generator checked to preserve every colour, and transitivity checked), and both checkers ran on the reduced problem. Such rows are labelled "VERIFIED (symmetry-reduced)" with the automorphism generators recorded. Reason: the reduction is itself machine-checked on the object, and it is the same reduction the repo already uses for circulants.
- PARTIAL: at least one half checked by both checkers (or one checker, stated). If the other half follows from a written proof (for example "the independence number is at most that of the input plus one", or a published theorem's lemma) the row says "other half by proof, see <file/paper>", but it stays PARTIAL. Reason: a human-written argument is not a machine check of the object, and the tier must mean the same thing for every row.
- No row is upgraded later without a new check entry in the ledger.

## Amendment 2 (7 Nov 2026 20:26 Chicago): witnesses found by light search
Approved by Christopher, provided no public version of the original authors' coloring exists [edited: the wording of a private message is replaced by this summary of its condition].
- R(4,10) >= 92, R(5,8) >= 101 (short tabu search over circulants) and R(4,17) >= 200 (cyclotomic-class scan mod 199), found [edited: working-process detail removed] outside the original scope, are kept.
- Label on every file and row: "independent witness found here by search (circulant / cyclotomic); not the colouring of HaKr1 / LiaWXS, which is unpublished". The row cites the paper that holds the bound and the search script (with its SHA-256) that found the witness.
- If a public version of the original authors' colouring turns up (HaKr1, HaKr2, LiaWXS or LiaWXCS, the Xu-Liang-Luo book), it is verified and becomes the row's primary witness; the search-found one stays as a second witness.
- Any further searching still needs its own registration with kill criteria (unchanged).

## Amendment 3 (12 Nov 2026 18:02 Chicago): halves that follow by proof
Approved by Christopher, for proofs that are standard [edited: the wording of a private message is replaced by this summary of its condition]. A half (or colour) that follows exactly by a written, cited proof from inputs that are themselves VERIFIED counts as VERIFIED, provided every computed part of the object has both checkers. Such rows are labelled "VERIFIED (by proof: <citation>)" and the proof is cited in the table, so a reader can tell them apart from rows checked fully by computer. Replaces the line "A half that follows from a written proof keeps the row PARTIAL".

## Amendment 4 (12 Nov 2026 18:29 Chicago): whole rows by proof
Approved by Christopher [edited: the wording of a private message is removed]. A row whose every half or colour follows by a published, cited theorem (paper, theorem, page) from inputs that are themselves VERIFIED with both checkers counts as "VERIFIED (by proof: <citation>)", even when the final object is never searched by computer. The input checks and a rebuild certificate (rebuild the object from hashed inputs, check the theorem's hypotheses, match SHA-256) are recorded. Proofs written up by us do not count; only the published paper.

## Amendment 5 (12 Nov 2026 18:46 Chicago): vertex-stabiliser reductions
Approved by Christopher [edited: the wording of a private message is removed]. A symmetry reduction may also use automorphisms fixing a vertex (the stabiliser), not only transitivity, provided those automorphisms and the resulting orbits are verified on the object itself and both checkers run on the reduced problem. Rows labelled "VERIFIED (symmetry-reduced)". Applies to the R(6,20) input check of build_round4 (x -> x+1 and x -> 8x on Q-type 877), so R(6,20) is VERIFIED (symmetry-reduced) and R(6,21) VERIFIED (by proof: XSR2 Thm 3 / Cor. 3).

## Amendment 6 (12 Nov 2026 20:03 Chicago): search S1 for lost cells
Approved by Christopher [edited: the wording of a private message, and a note on how the proposal was shown, are removed]. Targets, in order: R(6,13) (6,13;346) via Kuznetsov's public code; R(3,3,7) (3,3,7;84), which unlocks R(3,3,3,7); R(3,4,6) (3,4,6;116); R(3,3,8) (3,3,8;102); R(3,3,3,4) (3,3,3,4;96); R(3,3,3,5) (3,3,3,5;161); R(3,14) (3,14;66) on non-cyclic groups of order 66.
Methods: cyclic, block-cyclic and Cayley ansatzes; annealing; SAT (CaDiCaL via python-sat) with lazy clique clauses; methods and lessons from [edited: the name of another private project is removed].
Rules: cloud only, restartable runs each under 10 minutes, at most 2 cores with nice. Budget about one day of compute per target; stop a target when three independent methods have plateaued. Any find is checked with both checkers like every other witness and labelled "witness found here by search". Third-party code used only from its public source, with commit hash recorded. Nothing published or sent.

## Amendment 7 (13 Nov 2026 03:46 Chicago): check the 249-vertex R(3,3,3,7) candidate
Approved by Christopher [edited: the wording of a private message is removed]. Build Robertson's construction from the S1 cyclic (3,3,7;81) colouring (249 vertices), check it with both checkers unreduced, read exactly what Robertson's theorem requires of its input and how the survey's bound 247 for R(3,3,3,7) was obtained, and search the literature for any later bound. Nothing is claimed, published or sent; the result goes to Christopher first.

## Amendment 8 (13 Nov 2026 12:29 Chicago): implied-bound findings
Approved by Christopher [edited: the wording of a private message is removed]. (a) Build the explicit (3,3,16;292) colouring by XXER Theorem 7 (survey item 6.2.g) from the verified (3,15;73) graph, check it with both checkers unreduced or as Amendments 1 and 5 allow, with controls. (b) Have the three implied-bound findings of [edited: the name of a working folder not in this repository is removed] (R(3,3,3,7) 259, R(3,3,16) 293, R(7,16) 633) and the text/table notes re-checked independently against the survey and the cited papers. Nothing is claimed, published or sent before Christopher has seen the results.

## Amendment 9 (13 Nov 2026 13:38 Chicago): R(7,21) cap exception and long Mac runs
Approved by Christopher [edited: the wording of a private message is removed]. (a) The one remaining R(7,21) check (gen0 on independence subproblem w=4, p=1213) may run past the 10-minute cloud cap as a single process. (b) Prepare Mac runs, which Christopher starts himself: R(19,19) (omega of Paley 8941, both checkers), R(20,20) (same route, may exceed one day), R(6,13) (Kuznetsov's public search, multi-day). Each with a measured time estimate, cores and peak memory, how to stop, at most 4 processes, caffeinate and nice, no rm, logs [edited: a private path is removed]. [edited: a planned private message and its target are removed.]

## Amendment 10 (13 Nov 2026 17:50 Chicago): ordered subproblems for Paley rows. Recorded after the run.
This entry was written after wave 9 part a had finished (run 14:52 to 17:15 on the Mac, started by Christopher), not before it. The method was fixed in [edited: a working path is replaced by the file's path in this repository] phase2/scripts_as_run/mac_batch/wave9/paley/paley9.py (written 14:43, SHA-256 in [edited: the working file is replaced by this repository's index] phase2/scripts_as_run/INDEX.csv) before the run and was not changed afterwards. What it adds to Amendments 1 and 5: with sigma: x -> 1 - x, which fixes the edge {0,1} and is verified on the graph, the subproblem for the i-th orbit representative a keeps only the vertices of N(0) & N(1) & N(a) whose sigma-orbit index is at least i. Argument: in a clique through 0 and 1 take a further vertex of least orbit index; after applying sigma if needed it is the representative, and all other vertices have index at least i. Every representative must still answer NONE in both checkers. Rows that use it say "ordered" in their status note. Plain mode (W9_MODE=plain) remains available to anyone who wants the run without this step.
Result under this amendment: Paley graph on 8941 vertices has clique number 17 (2234 pieces, 1117 representatives, both checkers, all NONE, largest subproblem 1122 vertices), so R(19,19) > 17884 by Shearer 1986 Lemma 1 and Theorem 1.
Result under Amendment 10, 13 Nov 2026 21:37: Paley graph on 10861 vertices has clique number 18 (2714 pieces, 1357 representatives, both checkers, all NONE), so R(20,20) > 21724 by Shearer 1986. Run at 12 lanes (W9_LANES=12; lane count does not change the pieces).

## Amendment 11 (21 Nov 2026 22:28 Chicago): phase 2 closed. Recorded after the results.
This entry was written after the phase-2 count was known, not before. Phase 2 closes at repository commit 1d7aabe (pushed 21 Nov 2026), with 94 of the 105 cells VERIFIED in the sense of Amendments 1 to 5 and 10. Items in flight at the close, which do not change that count: GitHub issue #1 (R(3,23), received 18 Nov) and issues #2 and #3 (R(3,18) and R(4,18), received 20 Nov). Committed phase-2 rows stay as they are, R(3,3,16) above the survey included. Anything received or found after the close goes through the intake registration (REGISTRATION_intake.md), never into the phase-2 count.
Proposed 21 Nov 2026 22:28 Chicago, under Christopher's 22:18 instruction that these decisions are made by this work [edited: the wording of a private message is removed]. Approval: Christopher, with his OK of the push that first publishes this amendment. Corrected 22:49: the first version of this line called the 22:18 message an approval, which it is not [edited: working-process detail removed]. [edited: a note on a second change made before publication is removed.]
