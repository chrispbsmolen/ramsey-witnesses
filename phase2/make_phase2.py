"""Write phase2/COVERAGE.md, phase2/summary.json and phase2/README_section.md from phase2/coverage.csv,
phase2/witnesses/manifest.csv and phase2/recipes.csv, after checking every witness file against its SHA-256.
Run from the repository root:  python3 phase2/make_phase2.py"""
import os, csv, json, hashlib, collections
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__))); os.chdir(ROOT)
cov = list(csv.DictReader(open('phase2/coverage.csv')))
man = list(csv.DictReader(open('phase2/witnesses/manifest.csv')))
rec = list(csv.DictReader(open('phase2/recipes.csv')))
assert len(cov) == 105, len(cov)
for m in man:
    h = hashlib.sha256(open(m['file'], 'rb').read()).hexdigest()
    if h != m['sha256']: raise SystemExit('SHA-256 mismatch: %s' % m['file'])
mand = {m['cell']: m for m in man}
for c in cov:
    if c['witness']: assert c['witness'] == mand[c['cell']]['file'] and c['sha256_file'] == mand[c['cell']]['sha256'], c['cell']

R = lambda p: 'R(%s)' % p
fmt = lambda x: '{:,}'.format(int(x))
GROUPS = [('computer', 'VERIFIED, every half or color checked by two independent checkers on the object'),
          ('symmetry', 'VERIFIED (symmetry-reduced), both checkers on a reduction by automorphisms verified on the object'),
          ('proof', 'VERIFIED (by proof: citation), a half or the whole row follows by a published, cited theorem from inputs checked by both checkers'),
          ('search', 'VERIFIED (witness found here by search), the witness or its input found here by search (Amendments 2 and 6), every color checked by both checkers'),
          ('partial', 'PARTIAL'),
          ('recipe', 'RECIPE ONLY'),
          ('not_reproduced', 'NOT REPRODUCED'),
          ('no_file', 'STILL NO FILE')]
two = lambda c: int(c['colors']) == 2
cnt = {g: collections.Counter() for g, _ in GROUPS}
for c in cov: cnt[c['group']]['two' if two(c) else 'multi'] += 1
ver = sum(sum(cnt[g].values()) for g in ('computer', 'symmetry', 'proof', 'search'))
partial = [c['cell'] for c in cov if c['group'] == 'partial']
summary = dict(date='2026-11-14', cells=len(cov), verified=ver,
               by_group={g: dict(two_colour=cnt[g]['two'], multicolour=cnt[g]['multi'], total=sum(cnt[g].values())) for g, _ in GROUPS},
               witness_files=len(man), witness_bytes=sum(int(m['bytes']) for m in man), partial=partial)
json.dump(summary, open('phase2/summary.json', 'w'), indent=1)

def short(t, k=170):
    t = ' '.join(t.split())
    return t if len(t) <= k else t[:k].rsplit(' ', 1)[0] + ' ...'

lines = ['# Phase 2 coverage: the 105 cells without a public witness on 4 November 2026', '',
         'Written by `phase2/make_phase2.py` from `phase2/coverage.csv`, which has the full text of every field (source, how the file was read or built, license or credit, checks, proof, notes). Status as of 16 November 2026.', '',
         '| group | two-color | multicolor | total |', '|---|---|---|---|']
for g, name in GROUPS:
    lines.append('| %s | %d | %d | %d |' % (name, cnt[g]['two'], cnt[g]['multi'], sum(cnt[g].values())))
lines += ['| all | %d | %d | %d |' % (sum(cnt[g]['two'] for g in cnt), sum(cnt[g]['multi'] for g in cnt), len(cov)), '',
          'VERIFIED in one of its four forms: %d of 105.' % ver, '']
for g, name in GROUPS:
    rows = [c for c in cov if c['group'] == g]
    if not rows: continue
    lines += ['## %s (%d)' % (name, len(rows)), '']
    if g in ('computer', 'symmetry', 'proof', 'search', 'partial'):
        lines += ['| cell | survey bound [ref] | label | witness | n | checks |', '|---|---|---|---|---|---|']
        for c in rows:
            lines.append('| %s | %s [%s] | %s | `%s` | %s | %s |' % (R(c['cell']), fmt(c['survey_lower']), c['survey_ref'], c['label'], os.path.basename(c['witness']), fmt(c['n']), short(c['checks'])))
    else:
        lines += ['| cell | survey bound [ref] | label | what there is | notes |', '|---|---|---|---|---|']
        for c in rows:
            lines.append('| %s | %s [%s] | %s | %s | %s |' % (R(c['cell']), fmt(c['survey_lower']), c['survey_ref'], c['label'], short(c['how'], 120), short(c['notes'], 160)))
    lines.append('')
open('phase2/COVERAGE.md', 'w').write('\n'.join(lines))

# CHECKS.md: what was run for each row
ck = ['# Checks behind the phase-2 labels', '',
      'Written by `phase2/make_phase2.py` from `phase2/coverage.csv`. One line per cell with a witness file. The full records are in `phase2/checks/logs/` (index with SHA-256 in `phase2/checks/logs/INDEX.csv`).', '',
      '## Checkers', '',
      '| name here | program | what it decides |', '|---|---|---|',
      '| clique.c, verify_ramsey | `clique.c` of this repository (sha256 137a1002...), called by `verify_ramsey.py` (657db0ad...) or directly | is there a clique of a given size in a color class, bitset branch and bound |',
      '| networkx | `networkx.find_cliques` (version 3.x), as in `crosscheck.py`, `xcheck.py`, `crosscheck_mc.py` | maximal-clique enumeration, shares no solver code with clique.c |',
      '| gen0 | `phase2/scripts_as_run/build_round2/checker/gen0.c` (sha256 d82e1855...) | a separate exact clique search in C, written independently of clique.c |',
      '| linear0 | `phase2/scripts_as_run/build_round2/checker/linear0.c` (sha256 db46ca7e...) | exact clique search for colorings given by a length vector, cliques through vertex 0 |', '',
      'Every record names the SHA-256 of the object it checked. The witness files in `phase2/witnesses/` are those objects, gzip-compressed where they were not already. `phase2/witnesses/manifest.csv` gives both hashes: `sha256` of the committed file and `sha256_as_checked` of the object as named in the logs.', '',
      '## Machines', '',
      '- cloud: a Linux x86_64 machine, one to two cores per process, 7 to 16 November 2026.',
      '- Mac: an Apple Silicon laptop (macOS, arm64), at most four processes, runs pasted by hand in waves 0 to 8b, 7 to 12 November 2026. Each wave log starts with the command and ends with `exit=0`. Wave 9 (13 November, the inputs of R(19,19) and R(20,20)) ran with 4 and with 12 processes.', '',
      '## How to rerun one check', '',
      '```',
      'python3 verify_ramsey.py g6 phase2/witnesses/R7_11_n404.g6.gz 7,11      # both halves with clique.c',
      'python3 verify_ramsey.py colormat phase2/witnesses/R3_3_5_n44.colormat.gz 3,3,5',
      'python3 phase2/check_phase2.py --only 6,16 --limit 600                   # one row, repository checker',
      'python3 phase2/check_phase2.py                                            # every witness file, 60 s per search',
      '```', '',
      'The symmetry-reduced and proof-based checks need the scripts in `phase2/scripts_as_run/` (for example `build_round5/scripts/cyclo_reduce.py` for the cubic-residue rows, `build_round5/scripts/paley_check.py` and `mac_batch/wave9/paley/paley9.py` for c(Q_p)). They are kept as run, and their paths point to the working folders, so a rerun needs the paths adjusted.', '',
      '## Per cell', '',
      '| cell | label | witness (sha256 of committed file) | checks |', '|---|---|---|---|']
for c in cov:
    if not c['witness']: continue
    ck.append('| %s | %s | `%s` (%s...) | %s |' % (R(c['cell']), c['label'], os.path.basename(c['witness']), c['sha256_file'][:12], ' '.join(c['checks'].split())))
if os.path.exists('phase2/results/repo_check.txt'):
    ck += ['', '## Repository checker on every witness file', '',
           'Output of `python3 phase2/check_phase2.py --limit 120` run from a fresh clone of this branch (see `phase2/results/RUN_NOTE.txt`) (`phase2/results/repo_check.txt`, records in `phase2/results/repo_check.jsonl`). This is a uniform light re-check with a time limit. NOT_COMPLETED means the limit was reached. NOT_RUN_SIZE means the file has more vertices than the in-memory checker loads. Neither is a failure, and the labels rest on the checks listed above.', '',
           '```'] + open('phase2/results/repo_check.txt').read().rstrip().split('\n') + ['```']
if os.path.exists('phase2/results/repo_check_v2.txt'):
    ck += ['', 'The seven witness files added later (the six Rowley rows and R(3,3,3,7)), checked the same way from a fresh clone (`phase2/results/repo_check_v2.txt`):', '',
           '```'] + open('phase2/results/repo_check_v2.txt').read().rstrip().split('\n') + ['```']
if os.path.exists('phase2/results/repo_check_v3.txt'):
    ck += ['', 'The two rows that changed on 13 November, R(3,14) and R(9,9,9,9), checked the same way from a fresh clone (`phase2/results/repo_check_v3.txt`):', '',
           '```'] + open('phase2/results/repo_check_v3.txt').read().rstrip().split('\n') + ['```']
if os.path.exists('phase2/results/repo_check_v4.txt'):
    ck += ['', 'The three rows that changed on 14 November, R(7,21), R(19,19) and R(20,20), checked the same way from a fresh clone (`phase2/results/repo_check_v4.txt`):', '',
           '```'] + open('phase2/results/repo_check_v4.txt').read().rstrip().split('\n') + ['```']
if os.path.exists('phase2/results/repo_check_v5.txt'):
    ck += ['', 'The five rows that changed on 16 November, R(6,13), R(3,3,7), R(3,3,8), R(3,4,6) and R(3,3,3,4), checked the same way from a fresh clone (`phase2/results/repo_check_v5.txt`):', '',
           '```'] + open('phase2/results/repo_check_v5.txt').read().rstrip().split('\n') + ['```']
open('phase2/CHECKS.md', 'w').write('\n'.join(ck) + '\n')

# section for the top-level README (make_readme.py includes it)
P = lambda g: sum(cnt[g].values())
sec = ['## Phase 2 (updated 16 November 2026)', '',
       'On 4 November 105 cells of the table above had no public witness (32 RECIPE, 73 NO_FILE_FOUND). Phase 2 built the published constructions for these cells, looked again for public files, and checked what was found or built. For three cells, R(4,10), R(5,8) and R(4,17), the published coloring is not public, and the witness here was found by a short search. Those rows, and R(6,15) and R(7,18), which are built from two of them, say so. For R(3,3,3,7) the input coloring needed by the published construction is not public, and a registered search found one (see below). For R(3,14) the witness is the graph of the author the survey cites, Kolodyazhny, read from archived copies of his page. For R(6,13), R(3,3,7), R(3,3,8), R(3,4,6) and R(3,3,3,4) the witness is the coloring of the author the survey cites, sent by him on request in November 2026 (Eugene Kuznetsov and Geoffrey Exoo) and credited to him as personal communication. Everything is in `phase2/`, with one row per cell in `phase2/coverage.csv` and `phase2/COVERAGE.md`.', '',
       '| status on 16 November | two-color | multicolor | total |', '|---|---|---|---|']
for g, name in GROUPS:
    sec.append('| %s | %d | %d | %d |' % (name.split(',')[0], cnt[g]['two'], cnt[g]['multi'], P(g)))
sec += ['| all | %d | %d | %d |' % (sum(cnt[g]['two'] for g in cnt), sum(cnt[g]['multi'] for g in cnt), len(cov)), '',
        '- VERIFIED: every half (every color) of the witness was checked here by two independent exact checkers, `clique.c` and networkx or the separate C program `gen0.c` (or `linear0.c` for colorings given by a length vector).',
        '- VERIFIED (symmetry-reduced): the same, but on a smaller problem that uses automorphisms of the object. The automorphisms and their orbits were checked on the object itself before the reduction was used.',
        '- VERIFIED (by proof: citation): one half, one color or the whole row follows from a published theorem, cited with page, applied to inputs that were themselves checked by both checkers. Every computed part was checked by both checkers. Where a whole row rests on a theorem, the object was rebuilt from its inputs and matched byte for byte. The certificates are in `phase2/certificates/`.',
        '- VERIFIED (witness found here by search): the witness, or the input it is built from, was found here by a search (Amendment 2 or 6, see below), and every color of the witness was checked by both checkers, on the whole object or with a reduction verified on the object, as the row says.',
        '- PARTIAL: one check is missing, as stated in the row. RECIPE ONLY: the construction is written down or built, and not checked. NOT REPRODUCED: the construction as described could not be reproduced from the paper here (`phase2/NOTES.md`). STILL NO FILE: no public witness was found.',
        '- Credit for every construction goes to the authors named in the row. The survey reference is kept for each cell, and where the witness comes from a different paper the row names it (`phase2/NOTES.md`, section 4).', '', '%d witness files (%s bytes in all, compressed) are in `phase2/witnesses/`, each with its SHA-256, source and license or credit in `phase2/witnesses/manifest.csv`. The checks behind each label are summarized in `phase2/CHECKS.md`, with the logs in `phase2/checks/logs/`. `python3 phase2/check_phase2.py` reruns the repository checker on every witness file.' % (len(man), fmt(summary['witness_bytes'])),
        '', '**Searches.** Searching for new witnesses was outside the original registration. It was allowed later by two amendments, and every row whose witness was found by search says so. Amendment 2 (7 November) kept three witnesses found by short searches, R(4,10), R(5,8) and R(4,17), with this label. Amendment 6 (12 November) allowed a search for the lost cells, with these rules: runs in the cloud only, each restartable and under 10 minutes, at most 2 cores at low priority. About one day of computing per target, and a target is dropped once three independent methods have stopped improving. Methods are cyclic, block-cyclic and Cayley ansatzes, annealing, and SAT with clique clauses added lazily. Third-party code only from its public source, with its commit recorded. Every find is checked with both checkers like any other witness and labeled \"witness found here by search\". Nothing is published or sent as part of the search. Under Amendment 6 a cyclic (3,3,7;80) coloring was found by SAT on Z_80. With Robertson\'s construction it gives the 246-vertex witness for R(3,3,3,7) >= 247 (`phase2/NOTES.md`, section 5, and `phase2/search_s1/SEARCH_RECORD.md`). The search ended on 13 November with no witness for another cell. For each target `phase2/search_s1/SEARCH_RECORD.md` lists the symmetric forms that were excluded exactly (for example, there is no (3,14;66) Cayley graph on any group of order 66) and the runs that ended undecided.', '', 'Observations made on the way (a misprint in Shearer 1986, three constructions that could not be reproduced from the text, third-party claims above the survey, which are noted and not counted, and what the search for unpublished colorings covered) are in `phase2/NOTES.md`.', '', ('One row is PARTIAL (%s): the row says which check is missing.' if len(partial) == 1 else 'These rows are PARTIAL (%s): each row says which check is missing.') % ', '.join(R(x) for x in partial), '']
open('phase2/README_section.md', 'w').write('\n'.join(sec))
print(json.dumps(summary['by_group']), ver)
