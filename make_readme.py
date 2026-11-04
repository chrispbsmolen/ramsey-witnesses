"""Write README.md and results/VERIFICATION.md.  Every number is read from results/summary.json,
results/ledger.csv, results/coverage.csv (all written by make_ledger.py), results/selftest_output.txt,
results/crosscheck_output.txt, results/fetch_log.txt and sources/sources.csv."""
import os, csv, json, collections
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
S = json.load(open('results/summary.json'))
led = {r['id']: r for r in csv.DictReader(open('results/ledger.csv'))}
cov = list(csv.DictReader(open('results/coverage.csv')))
src = list(csv.DictReader(open('sources/sources.csv')))
rd = lambda f: open(f).read().strip() if os.path.exists(f) else '(not run)'
fmt = lambda x: '{:,}'.format(int(x))
R = lambda p: 'R(%s)' % p
V = S['ledger_verdicts']; G = ['two-colour, k <= l <= 15', 'two-colour, l > 15', 'multicolour']
STAT = ['VERIFIED', 'PARTIAL', 'RECIPE', 'NO_FILE_FOUND']
cov_rows = '\n'.join('| %s | %s | %s |' % (g, ' | '.join(str(S['coverage'][g].get(s, 0)) for s in STAT), sum(S['coverage'][g].get(s, 0) for s in STAT)) for g in G)
srcname = {s['source']: s['name'] for s in src}
claims = {(r['parameters'], r['source']): r['where_claimed'] for r in csv.DictReader(open('sources/claims.csv'))}
exc = '\n'.join('| %s | %s | %s (%s%s) | %s | %s | `%s` |' % (R(x['parameters']), fmt(x['verified']), fmt(x['survey_lower']), x['survey_tables'], '; ' + x['other_table_values'] if x['other_table_values'] else '',
                 x['source'], claims.get((x['parameters'], x['source']), 'not recorded'), x['witness']) for x in S['exceeds'])
unclaimed = ' '.join('An unlisted file %s (%s vertices) is also in Tatarevic\'s graphs/ folder; its author claims nothing for it, and it was %s here.' % (u['id'].split('/')[-1], u['n'], 'not checked' if u['verdict'] == 'NOT_CHECKED' else 'checked (%s)' % u['verdict']) for u in S['unclaimed_files'])
data_mb = round(int(rd('results/fetch_log.txt').split('\n')[0].split('bytes ')[1]) / 1e6)
cl_now = __import__('hashlib').sha256(open('clique.c', 'rb').read()).hexdigest()[:16]
blank = '\n'.join('| %s | %s | `%s` | %s |' % (R(x['parameters']), fmt(x['verified']), x['witness'], led[x['witness']]['checked']) for x in S['no_survey_bound_verified'])
unv = '\n'.join('| %s | %s | %s | `%s` | %s |' % (R(x['parameters']), fmt(x['claimed']), fmt(x['survey_lower']) if x['survey_lower'] else 'blank', x['witness'], x['check']) for x in S['unverified_above_survey'])
def miss(g):
    xs = [x for x in S['no_public_witness'] if (lambda r: (len(r) > 2 and g == 'multicolour') or (len(r) == 2 and ((max(r) <= 15) == (g == G[0])) and g != 'multicolour'))(sorted(map(int, x['parameters'].split(','))))]
    return ', '.join('%s >= %s [%s]%s' % (R(x['parameters']), fmt(x['survey_lower']), x['lower_ref'], ' (recipe)' if x['status'] == 'RECIPE' else '') for x in xs), len(xs)
m0, n0 = miss(G[0]); m1, n1 = miss(G[1]); m2, n2 = miss(G[2])
cons = [r for r in led.values() if r['source'] == 'constructed_here']
cons_rows = '\n'.join('| `%s` | %s | %s | %s | %s |' % (r['file'], R(r['parameters']), r['claimed_bound'], r['n'], r['verdict']) for r in cons)
pc = ', '.join(R(r['parameters']) for r in cov if 'computed here' in r['search_note'] and r['status'] == 'RECIPE')
po = '; '.join('Q_%d has clique number %d' % (o['p'], o['omega']) for o in S['paley_omega'])
src_rows = '\n'.join('| %s | %s | %s | %s |' % (s['name'], s['where'], s['licence found'], s['here']) for s in src)
by_src = '\n'.join('| %s | %s |' % (k, ', '.join('%s %s' % (kk, vv) for kk, vv in sorted(v.items()))) for k, v in S['ledger_by_source'].items())
part_rows = '\n'.join('| %s | %s | %s | %s |' % (R(x['parameters']), fmt(x['survey_lower']), fmt(x['claimed']), x['check']) for x in S['partial'])
fl = rd('results/fetch_log.txt').split('\n'); fetch_ok = sum(1 for l in fl if l.startswith('OK ')); fetch_n = len(fl) - 1

readme = f'''# ramsey-witnesses

An exact checker for lower-bound witnesses of small Ramsey numbers, the results of running it on the public
witness files found, and a table of every lower bound in Radziszowski's dynamic survey *Small Ramsey Numbers*
(Electron. J. Combin. DS1, revision 18, 24 April 2026) with whether a public witness for it was verified here.

A witness for R(k_1, ..., k_r) >= n + 1 is a colouring of the edges of K_n with r colours and no K_(k_i) in
colour i; for two colours, a graph on n vertices with no K_k and no independent set of size l. `verify_ramsey.py`
decides this exactly: for each colour class the C program `clique.c` (bitset branch and bound with greedy-colouring
bounds) searches for a clique of the forbidden size. `selftest.py` checks the solver against networkx on random
graphs and on planted cliques and corrupted witnesses; `crosscheck.py` rechecks some witnesses with networkx, which
shares no solver code with `clique.c`.

## Results

{fmt(S['manifest_witnesses'])} witnesses are listed in `sources/manifest.csv` ({S['committed']} of them are in this repository; the others are
downloaded from their original URLs by `fetch_data.py`, and all {fetch_n} downloads matched the recorded SHA-256, `results/fetch_log.txt`).
Verdicts (`results/ledger.csv`, one row per witness file or per entry of a file holding several):

| verdict | witnesses |
|---|---|
| PASS: every colour class checked, no forbidden clique | {V.get('PASS', 0)} |
| PARTIAL: only some colour classes checked, those passed | {V.get('PARTIAL', 0)} |
| NOT_COMPLETED: check started, stopped at the time limit | {V.get('NOT_COMPLETED', 0)} |
| NOT_CHECKED: located, no check run here | {V.get('NOT_CHECKED', 0)} |
| FAIL | {V.get('FAIL', 0)} |

McKay's files hold many graphs each; counting every graph checked, {fmt(S['graphs_pass'])} graphs passed.

Every lower bound in the survey's tables Ia, IIa, IIb, IIc, XIa, XIb and the bounds listed in its section 6.1
(`results/coverage.csv`, {S['survey_cells_with_lower_bound']} cells with a lower bound L; a witness needs L - 1 vertices):

| cells | VERIFIED | PARTIAL | RECIPE | NO_FILE_FOUND | total |
|---|---|---|---|---|---|
{cov_rows}

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
{exc}

Survey revision 18 is dated 24 April 2026. The files of Coniglio, Furini et al. (arXiv:2608.18769, August 2026),
of fritzcremer/ramsey-lower-bounds (arXiv:2610.12122, October 2026) and of Lachy-Dauth/ramsey-neighbourhood-counting
(repository commit of 26 October 2026) appeared after it, and the AlphaEvolve values above are those of the
repository files and of version 5 of arXiv:2603.09172, not the values the survey cites. So this list is of files
newer than the survey or not cited in it, not of omissions from the survey.

### Witnesses for cells the survey leaves blank

| number | bound from the witness | witness | checked |
|---|---|---|---|
{blank}

### Public files above the survey that were not fully checked here

| number | bound the file would give | survey | witness | check here |
|---|---|---|---|---|
{unv}

{unclaimed}

### Survey lower bounds with no public witness found

No witness file of the survey's strength was found for these (in brackets the survey's reference; "recipe" marks
a construction described in the survey or the cited paper). Two-colour with k <= l <= 15 ({n0}): {m0}.

Two-colour with l > 15 ({n1}): {m1}.

Multicolour ({n2}): {m2}.

### Witnesses constructed here

`constructions/build.py` builds these deterministically (Paley graphs Q_p and the doubling of Q_p on 2p + 2 vertices
described in the survey, the 5-cycle, the GF(16) cube-coset colouring of K_16, the cubic-residue graph on Z_127 and the cube-coset colouring
of K_127):

| file | number | bound | vertices | verdict |
|---|---|---|---|---|
{cons_rows}

`constructions/paley_omega.py` computes the clique numbers of larger Paley graphs exactly ({po}); with the doubling
construction these give the survey's bounds for {pc}, whose graphs were not built or checked here (status RECIPE).

## Usage

Python 3 with numpy and networkx (`requirements.txt`), a C compiler (`clique.c` is compiled on first use) and,
for Kuznetsov's circulants, `pdftotext` from poppler. Run every script from the repository root.

```
python3 selftest.py                    # results/selftest_output.txt
python3 verify_ramsey.py FORMAT FILE K1,K2[,...] [INDEX]
python3 fetch_data.py [SOURCE ...]     # data/ (about {data_mb} MB), results/fetch_log.txt
python3 run_ramsey.py RUN [--quick] [--max-n N] [--source S ...] [--id ID ...]   # results/runs/RUN.jsonl
python3 crosscheck.py                  # results/crosscheck_output.txt
python3 constructions/build.py         # rebuilds constructions/witnesses/
python3 make_ledger.py                 # results/ledger.csv, coverage.csv, summary.json
python3 make_readme.py                 # this file and results/VERIFICATION.md
```

A full `run_ramsey.py` without `--quick` takes hours: the cloud run took about {fmt(round(S['runs']['cloud']['seconds'], -2))} s in all, with a
time limit of 1800 s per file, and the independence halves of the large AlphaEvolve witnesses took up to about
{round(S['mac_max_half_seconds'] / 60)} minutes each on a separate machine (`tools/run_hard.py`).

`survey/` holds the survey's lower bounds as extracted from the tables (with their reference tags) and
`survey/search_notes.csv` the notes from the search for each witness. `tools/run_hard.py` is the script used for
the large AlphaEvolve witnesses on a separate machine.

## Sources and licences

| source | where | licence found | here |
|---|---|---|---|
{src_rows}

Files of the other sources are identified by URL and SHA-256 in `sources/manifest.csv` and are not
redistributed. The survey and the papers are not included.

## Credit, corrections and removal

Every result here names its source; please cite the original authors for their results. Corrections, missing or
wrong credit, and requests to change or remove anything (including a request to stop linking a file) are welcome as
a GitHub issue or by email to the maintainer, Christopher Smolen (independent researcher, ORCID 0009-0002-9537-7961),
chrispbsmolen@gmail.com. A file whose author objects to its inclusion is removed. Every such change is recorded,
with its date and reason, in `CORRECTIONS.md`.

## Licence

MIT (`LICENSE`), except the files in `third_party/`, which keep their own licences (see the NOTICE file in each folder).

Christopher Smolen, November 2026.
'''
open('README.md', 'w').write(readme)

runs = S['runs']
run_desc = {'cloud': 'cloud machine, 3 November 2026, working layout (paths rewritten for this repository, per-graph records of McKay files merged per file)',
            'cloud_constructions': 'cloud machine, 3 November 2026, constructions built then',
            'mac': 'separate machine (Mac), tools/run_hard.py, one process per half',
            'repo': 'this repository, 4 November 2026, after fetch_data.py: run_ramsey.py repo --quick --max-n 300 (a first pass under a looser quick rule was stopped by hand during the first check of furini/R_3_33_graphSize_229.clq, which wrote no record; the run then resumed under the current rule; constructions/cubic3_127_R4_4_4.txt was added afterwards with --id)'}
run_rows = '\n'.join('| %s | %s | %s | %s | %s | %s |' % (k, run_desc.get(k, ''), v['records'], fmt(v['graphs_pass']), v['seconds'], '; '.join(S['run_verifiers'].get(k, []))) for k, v in runs.items())
hard = [r for r in led.values() if r['runs'] and 'mac' in r['runs'].split(';')]
hard_rows = '\n'.join('| `%s` | %s | %s | %s |' % (r['id'], r['verdict'], r['checked'], r['detail']) for r in hard)
nc = [r for r in led.values() if r['verdict'] in ('NOT_COMPLETED', 'NOT_CHECKED')]
nc_rows = '\n'.join('| `%s` | %s | %s | %s |' % (r['id'], R(r['parameters']), r['verdict'], r['detail']) for r in nc)
samp = [r for r in led.values() if r['detail'].startswith('graphs checked')]
samp_rows = '\n'.join('| `%s` | %s | %s | %s |' % (r['id'], fmt(r['graphs_in_file']), r['graphs_checked'], 'line numbers divisible by %s, from 0' % r['detail'].split()[3].split('-')[0]) for r in samp)
ver = f'''# Verification record

## Runs

| run | where and how | records | graphs passed (all colour classes) | seconds | verifier (SHA-256 prefixes) |
|---|---|---|---|---|---|
{run_rows}

The cloud runs used an earlier layout of the same code (`verify_ramsey.py` before it was tidied for this
repository). Every run used `clique.c` with SHA-256 34b72631979d0ebfdb871d8e04fc62a3547477aef96b945d71b91ec30a147c6c
(for the Mac run, the copy kept on that machine was hashed afterwards and is identical). After all runs the header
comment of `clique.c` was corrected (it described a MAX output line the program never prints); the code is unchanged,
and the file's SHA-256 prefix is now {cl_now}. The repository run rechecked {S['rerun_overlap']} witnesses that the
earlier runs had also checked: {len(S['rerun_disagreements'])} differences in verdict or vertex count. It also checked
{len(S['repo_run_new_ids'])} witnesses for the first time: {', '.join('`%s`' % i for i in S['repo_run_new_ids'])}.
Every record carries the SHA-256 of the file it checked, and `make_ledger.py` stops if one differs from the manifest.

## Large witnesses checked in halves

On the separate machine each half (no K_k; no independent l-set, by searching the complement) ran as its own
process with no time limit. `tools/run_hard.py` reads files named `Rk_l_geB.txt`, so the AlphaEvolve files
`R(k, l) >= B.txt` were copied under those names with their contents unchanged; its records carry the SHA-256 of
each file, and they are matched to `sources/manifest.csv` by that hash. {S['mac_half_runs']} half runs are recorded, {S['mac_duplicate_half_runs']} of them repeats of a half with the same output.
Only what is listed was checked; the other halves were not run to completion.

| witness | verdict | checked | solver detail |
|---|---|---|---|
{hard_rows}

## Not completed or not checked

| witness | number | verdict | note |
|---|---|---|---|
{nc_rows}

## Sampled graph6 files

Files with more than 3,000 graphs were sampled (all other graph6 files were checked line by line in full):

| file | graphs in file | graphs checked | selection |
|---|---|---|---|
{samp_rows}

## Checks on the checker

`selftest.py`:

```
{rd('results/selftest_output.txt')}
```

`crosscheck.py` (networkx only, no shared solver code):

```
{rd('results/crosscheck_output.txt')}
```

Downloads (`fetch_data.py`, `results/fetch_log.txt`): {fetch_ok} of {fetch_n} witnesses matched the recorded SHA-256.

## What this does not show

- Nothing about upper bounds, or about whether a bound is the best known; the survey is the reference point only.
- A NOT_CHECKED or PARTIAL row says nothing either way about that file.
- NO_FILE_FOUND and "no public witness found" mean none was found in the sources listed in `sources/sources.csv`; witnesses may
  exist in papers, theses or private files that were not searched or could not be retrieved.
- For sampled McKay files only the sampled graphs were checked; for complete sets the completeness claimed by the
  source was not checked.
'''
open('results/VERIFICATION.md', 'w').write(ver)
print(readme[:400])
