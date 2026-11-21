# Search S1 (Amendment 6): record of the search

Search S1 looked for witnesses for cells with no public witness, under Amendment 6 of the phase-2 registration
(12 November 2026, rules in `../README.md`, section Searches). It ran on 12 and 13 November 2026 and has ended.
The first part of this record is the run that produced the find used in the table, R(3,3,3,7) >= 247. The section
Outcome for every target gives the result for each target, and `all_targets/` holds the scripts and logs of the
whole search.

## Environment

| item | version |
|---|---|
| machine | Linux x86_64 cloud machine, 2 cores, each search process under `nice -n 19` and `timeout 590` |
| Python | CPython 3.13.18 |
| python-sat | 1.9.dev22, installed with pip from PyPI (wheel cp313 manylinux). The package metadata records no VCS commit |
| SAT solver | CaDiCaL 1.5.3, the copy bundled with python-sat (solver name `cadical153`) |
| check | `clique.c` of this repository (sha256 137a1002...) and `gen0.c` (d82e1855...), through `verify_find.py` and `verify_ramsey.py` |

## Method (`scripts/symsat.py`, `scripts/symlib.py`)

An exact SAT search for a 3-coloring of K_n with no monochromatic triangle in colors 0 and 1 and no K7 in color 2,
inside a cyclic ansatz: the group Z_n acts on the vertices, and every edge orbit (difference class) gets one color.
Triangle clauses are added up front. K7 clauses are added lazily: the solver's model is searched for a K7 through
vertex 0 in color 2, a clause excluding each one found is added, and the solver runs again. Every added clause is
implied by the problem, so a model with no K7 found is a witness. A degree bound of 22 in colors 0 and 1 (the
standard bound R(3,7) - 1) was added as a cardinality constraint (`--maxdeg 0:22,1:22`). The run is restartable: the
lazy clauses are kept in a state file and reloaded.

## The runs

Commands, from the job queue (`logs/queue_lines_n80_n81.txt`, run through `scripts/queue.sh` and `scripts/legs.sh`):

```
python3 src/symsat.py cyc:80 3,3,7 560 state/t337/cyc80.jsonl finds/t337/cyc80 logs/t337_R337.jsonl --label "R(3,3,7) frontier n=80 cyclic (n>=80 gives R(3,3,3,7) via Robertson)" --maxdeg 0:22,1:22
python3 src/symsat.py cyc:81 3,3,7 560 state/t337/cyc81.jsonl finds/t337/cyc81 logs/t337_R337.jsonl --label "R(3,3,7) frontier n=81 cyclic (n>=80 gives R(3,3,3,7) via Robertson)" --maxdeg 0:22,1:22
```

| n | group | edge orbits | lazy clauses | seconds | result | file sha256 |
|---|---|---|---|---|---|---|
| 80 | Z_80 | 40 | 17,574 | 14.7 | FOUND | 636ac4bcf760273490857de41592c48e81a88147dc2906c06c81212a6b9bf1b0 |
| 81 | Z_81 | 40 | 19,557 | 15.3 | FOUND | c62f5d26a7d57ef93853b02c61d0f25510ccf06a701dac92014d319395ab7a8e |

The log entries are in `logs/t337_runs_n80_n81.jsonl`, the color of each edge orbit in `finds/`, and the lazy
clauses of each run in `state/` (gzip). Seed 1 in both runs.

## Use and checks

- The n = 80 coloring is the input of row R(3,3,3,7): Robertson's construction (Electron. J. Combin. 6 (1999) #R3,
  Part Two), built by `scripts/build_3337.py`, gives the 246-vertex witness `../witnesses/R3_3_3_7_n246.colormat.gz`.
- Both files were checked by `scripts/verify_find.py` (`logs/verify_finds.jsonl`): verify_ramsey PASS, and clique.c and
  gen0 on every color on the whole graph, with no reduction. Controls: the color asked for one vertex less is FOUND
  by both checkers, and a copy with one or two edges recolored is caught by both.
- The n = 81 coloring gives R(3,3,7) >= 82, below the survey's value 85. It is not used in any row and is recorded
  by its hash only.

## Outcome for every target (final, 13 November 2026)

Three words are used. Found: a coloring was written and then checked with both checkers. Exact negative: the SAT
solver returned UNSAT, so no coloring of the stated symmetric form exists. This says nothing about colorings
without that symmetry. Undecided: the run reached its time limit, which decides nothing. The edge annealing runs
all stopped improving at a positive number of forbidden cliques. That is a plateau of the method and not evidence
that no coloring exists.

Every SAT run used only clauses that hold for every coloring of the stated form: the triangle clauses, the clique
clauses added lazily, and degree bounds that follow from known upper bounds (for example at most 13 neighbors in the
triangle-free color of a (3,14) coloring). The bounds used are in each log record (`maxdeg`).

| target | outcome | exact negatives | undecided at the time limit | annealing, best number of forbidden cliques |
|---|---|---|---|---|
| R(6,13), a (6,13;346) coloring | not found | cyclic on Z_346 and invariant under the multiplier 175 (subgroup of order 172), 177 (order 86) or 189 (order 43) | cyclic on Z_346, cyclic with multiplier 253 (order 4). Kuznetsov's public search code reached cyclic order 172 and did not get further within the run limits | not run |
| R(3,3,7), a (3,3,7;84) coloring | not found. Cyclic colorings on 80 and 81 vertices found | the cyclic (3,3,7;81) coloring kept fixed plus 1 new vertex, plus 3 new vertices, and plus 3 new vertices with 6 spread vertices freed | cyclic on Z_82, Z_83 and Z_84, block-cyclic Z_42 x 2, Z_28 x 3 and Z_21 x 4, the (3,3,7;81) coloring with 12 vertices freed plus 3 new | 97 |
| R(3,3,3,7) | found: the 246-vertex coloring of the row, from the cyclic (3,3,7;80) coloring | | | |
| R(3,4,6), a (3,4,6;116) coloring | not found | cyclic on Z_116 with multiplier 17 (order 4) or 25 (order 7), four blocks of Z_29 with multiplier 7 (order 7) or 4 (order 14) | cyclic on Z_116, four blocks of Z_29 with multiplier -1 or 12 | 874 |
| R(3,3,8), a (3,3,8;102) coloring | not found | cyclic on Z_102 with multiplier 13 (order 4) or 19 (order 8) | cyclic on Z_102, six blocks of Z_17 with multiplier 4 | 894 |
| R(3,3,3,4), a (3,3,3,4;96) coloring | not found | cyclic on Z_96 with multiplier 7 (order 4) or 5 (order 8) | cyclic on Z_96 | 63 |
| R(3,3,3,5), a (3,3,3,5;161) coloring | not found | cyclic on Z_161 with multiplier 24 (order 6), 8 (order 11) or 93 (order 3) | cyclic on Z_161, cyclic with multiplier 22 (order 3) | 1687 |
| R(3,14), a (3,14;66) graph | not found by this search | Cayley graphs on each of the four groups of order 66 (Z_66, D_33, S_3 x Z_11, Z_3 x D_11), and a cyclic (3,14;63) graph kept fixed plus 3 new vertices | the cyclic (3,14;63) graph with 9 vertices freed plus 3 new | 52 |

Notes on the table:

- R(3,14) was closed on 13 November by another route: Kolodyazhny's (3,14;66) graph was found in the Wayback Machine
  (row R(3,14) of `../coverage.csv`). Its degrees are 11 to 13, so it is not a Cayley graph, in agreement with the
  exact negative above.
- R(6,13): Kuznetsov's code is github.com/ekuznetsov139/ramsey at commit f5c81c7b9ca4b1f570c1226665de9e67118bd8de.
  It was built on Linux with three small portability changes (GRAPH_MAX_LEN raised from 4 to 6, a base-class
  qualification in `bigint.h`, one constructor argument in `ramsey_df.cpp`). The patch has sha256 d0be44d9... and is
  not included, because it contains lines of his source. The driver and the two header files written here are in
  `all_targets/kuznetsov_port/`. Run with one thread, a pass of the search takes longer than the 10 minutes allowed
  per process, and the code saves its state only between passes.
- Calibration (`all_targets/logs/calibration*.jsonl`): the SAT search found cyclic colorings again at the sizes of
  the public (3,3,7;78), (3,3,3,4;92) and (3,14;63) colorings. An orbit annealer did not pass calibration and was
  not used on the targets. The edge annealer is weak at these sizes.
- The budget of about one day of computing per target was not used up. The longest runs were 30 to 60 core-minutes
  per symmetric form. The search was stopped on 13 November.
- `all_targets/logs/run_table.txt` lists every run with its form, method, number of restartable legs, time and
  result. A leg with a start record and no end record was stopped by the 590 s process limit.

## Files

`INDEX.csv` gives each file's source in the working folder and the SHA-256 of the original and of the copy here.
Local paths were replaced by placeholders as in `../checks/logs/` (one line of `build_3337.py`). The two log files
in `logs/` are extracts: the lines for n = 80 and 81, copied unchanged. `scripts/`, `logs/`, `state/` and `finds/`
are the record of 12 November for the run behind R(3,3,3,7).

`all_targets/` is the working folder of the whole search as it stood at the end: `scripts/` (the final versions,
which differ from the 12 November copies in `symsat.py`, by an added start record, and in one path line of
`build_3337.py`), `logs/` (one log per target, the job queues, the calibration runs and `run_table.txt`),
`kuznetsov_port/` and `SHA256SUMS`. The solver state files of the runs that found nothing are not included.
