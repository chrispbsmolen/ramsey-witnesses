# Search S1 (Amendment 6): record of the run behind R(3,3,3,7) >= 247

Search S1 looks for witnesses for cells with no public witness, under Amendment 6 of the phase-2 registration
(12 November 2026, rules in `../README.md`, section Searches). It was still running when this record was written.
Only the run that produced a find used in the table is recorded here.

## Environment

| item | version |
|---|---|
| machine | Linux x86_64 cloud machine, 2 cores, each search process under `nice -n 19` and `timeout 590` |
| Python | CPython 3.13.18 |
| python-sat | 1.9.dev22, installed with pip from PyPI (wheel cp313 manylinux). The package metadata records no VCS commit |
| SAT solver | CaDiCaL 1.5.3, the copy bundled with python-sat (solver name `cadical153`) |
| check | `clique.c` of this repository (sha256 137a1002...) and `gen0.c` (d82e1855...), through `verify_find.py` and `verify_ramsey.py` |

## Method (`scripts/symsat.py`, `scripts/symlib.py`)

An exact SAT search for a 3-colouring of K_n with no monochromatic triangle in colours 0 and 1 and no K7 in colour 2,
inside a cyclic ansatz: the group Z_n acts on the vertices, and every edge orbit (difference class) gets one colour.
Triangle clauses are added up front. K7 clauses are added lazily: the solver's model is searched for a K7 through
vertex 0 in colour 2, a clause excluding each one found is added, and the solver runs again. Every added clause is
implied by the problem, so a model with no K7 found is a witness. A degree bound of 22 in colours 0 and 1 (the
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

The log entries are in `logs/t337_runs_n80_n81.jsonl`, the colour of each edge orbit in `finds/`, and the lazy
clauses of each run in `state/` (gzip). Seed 1 in both runs.

## Use and checks

- The n = 80 colouring is the input of row R(3,3,3,7): Robertson's construction (Electron. J. Combin. 6 (1999) #R3,
  Part Two), built by `scripts/build_3337.py`, gives the 246-vertex witness `../witnesses/R3_3_3_7_n246.colormat.gz`.
- Both files were checked by `scripts/verify_find.py` (`logs/verify_finds.jsonl`): verify_ramsey PASS, and clique.c and
  gen0 on every colour on the whole graph, with no reduction. Controls: the colour asked for one vertex less is FOUND
  by both checkers, and a copy with one or two edges recoloured is caught by both.
- The n = 81 colouring gives R(3,3,7) >= 82, below the survey's value 85. It is not used in any row and was not
  checked here, so it is recorded by its hash only.

## Other S1 targets

Search in progress on 12 November 2026, no results recorded here:

- R(6,13), a (6,13;346) colouring, with Kuznetsov's public code
- R(3,3,7), a (3,3,7;84) colouring, cyclic n = 82 to 84
- R(3,4,6), (3,4,6;116)
- R(3,3,8), (3,3,8;102)
- R(3,3,3,4), (3,3,3,4;96)
- R(3,3,3,5), (3,3,3,5;161)
- R(3,14), (3,14;66) on the non-cyclic groups of order 66

## Files

`INDEX.csv` gives each file's source in the working folder and the SHA-256 of the original and of the copy here.
Local paths were replaced by placeholders as in `../checks/logs/` (one line of `build_3337.py`). The two log files
are extracts: the lines for n = 80 and 81, copied unchanged.
