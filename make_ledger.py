"""Write results/ledger.csv (one row per witness in sources/manifest.csv), results/coverage.csv (one row
per lower bound in the survey tables in survey/) and results/summary.json, from results/runs/*.jsonl.

Ledger verdicts
  PASS           every colour class was checked and none contains its forbidden clique
  PARTIAL        only some colour classes were checked (the column checked says which), all of those passed
  FAIL           a forbidden clique was found
  NOT_COMPLETED  a check was started and did not finish (time limit)
  NOT_CHECKED    no check was run here

Coverage status of a survey cell (lower bound L, so a witness needs L - 1 vertices)
  VERIFIED   a witness on at least L - 1 vertices has verdict PASS here
  PARTIAL    no such PASS, but a public witness file on at least L - 1 vertices was found; its check here is
             PARTIAL, NOT_COMPLETED or NOT_CHECKED
  RECIPE     no witness file at that strength was found; the survey or the cited paper gives a construction
             (survey/search_notes.csv class recipe_only, or for cells without a note, a reference that is a
             survey item such as 2.3.i)
  NO_FILE_FOUND  the survey gives this bound with its reference; no public witness file was found here. This
             says nothing about the bound itself
  NO_SURVEY_BOUND  the survey cell has no lower bound (listed only when a witness was checked here)
Only witnesses for exactly the cell's parameters count (in any order); bounds implied by monotonicity are not
used.
"""
import os, re, csv, json, glob, collections
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)
man = list(csv.DictReader(open('sources/manifest.csv')))
runs = collections.defaultdict(list)
for f in sorted(glob.glob('results/runs/*.jsonl')):
    for l in open(f):
        r = json.loads(l)
        if 'id' in r: runs[r['id']].append(r)
key = lambda s: tuple(sorted(int(x) for x in s.split(',')))
P = lambda t: ','.join(map(str, t))

# ---------- ledger
ledger = []
for m in man:
    rs = runs.get(m['id'], []); full = [r for r in rs if 'half' not in r]; halves = [r for r in rs if 'half' in r]
    ks = [int(x) for x in m['parameters'].split(',')]
    row = dict(parameters=m['parameters'], colours=len(ks), claimed_bound=m['claimed_bound'], n=m['n'], source=m['source'], id=m['id'],
               file=m['path'], committed=m['committed'], url=m['url'], sha256=m['sha256'], verdict='NOT_CHECKED', checked='none',
               graphs_in_file=m['graphs_in_file'], graphs_checked='', runs=';'.join(sorted({r['run'] for r in rs})),
               seconds=round(sum(r.get('seconds', 0) for r in rs), 1), detail='')
    for r in rs:
        if r.get('sha256') and r['sha256'] != m['sha256']: raise SystemExit('hash differs for %s in run %s' % (m['id'], r['run']))
        if r.get('n') is not None and int(r['n']) != int(m['n']): raise SystemExit('order differs for %s in run %s' % (m['id'], r['run']))
    if any(r['verdict'] == 'FAIL' for r in full) or any(r['result'] == 'FOUND' for r in halves):
        row.update(verdict='FAIL', checked='see runs', detail='; '.join(str(r.get('detail')) for r in full if r['verdict'] == 'FAIL'))
    elif any(r['verdict'] == 'PASS' for r in full):
        p = [r for r in full if r['verdict'] == 'PASS']; g = max(p, key=lambda r: r.get('graphs_checked', 1))
        row.update(verdict='PASS', checked='all colour classes')
        if m['format'] == 'g6': row.update(graphs_checked=g.get('graphs_checked', 1), detail='' if g.get('graphs_selection', 'all') == 'all' else 'graphs checked: ' + g['graphs_selection'])
    elif halves:
        ok = sorted({r['half'] for r in halves if r['result'] == 'OK'})
        name = {'no_clique': 'no K_%d' % ks[0], 'no_independent_set': 'no independent %d-set' % ks[1]}
        row.update(verdict='PASS' if len(ok) == 2 else 'PARTIAL', checked=' and '.join(name[h] for h in ok) + (' (two separate processes)' if len(ok) == 2 else ' only'),
                   detail='; '.join('%s: solver nodes %s, %s s' % (r['half'], format(r['solver_nodes'], ','), r['seconds']) for r in halves))
    elif any(r['verdict'] == 'NOT_COMPLETED' for r in full):
        row.update(verdict='NOT_COMPLETED', detail='; '.join(r.get('detail') or '' for r in full))
    if not rs: row['detail'] = 'no check run here (%s)' % m['note']
    ledger.append(row)
cols = list(ledger[0])
with open('results/ledger.csv', 'w', newline='') as fo:
    w = csv.DictWriter(fo, fieldnames=cols); w.writeheader(); w.writerows(ledger)
L = {r['id']: r for r in ledger}

# ---------- coverage
cells = collections.OrderedDict()
def addcell(params, lower, ref, table):
    k = key(params)
    if k not in cells: cells[k] = dict(lower='', ref='', tables=[])
    c = cells[k]; c['tables'].append(table); c.setdefault('by_table', []).append((table, lower))
    if lower and (not c['lower'] or int(lower) > int(c['lower'])): c['lower'], c['ref'] = lower, ref
for r in csv.DictReader(open('survey/two_color.csv')): addcell('%s,%s' % (r['k'], r['l']), r['lower'], r['lower_ref'], 'Ia')
for r in csv.DictReader(open('survey/two_color_higher.csv')): addcell('%s,%s' % (r['k'], r['l']), r['lower'], r['lower_ref'], r['table'])
for r in csv.DictReader(open('survey/multicolor.csv')):
    try: addcell(r['parameters'], r['lower'], r['lower_ref'], r['table'])
    except ValueError: pass
notes = {key(r['parameters']): r for r in csv.DictReader(open('survey/search_notes.csv'))}
omega = [json.loads(l) for l in open('results/runs/paley_omega.jsonl')]
recipe_here = {}
for o in omega:
    for b in (o['paley_bound'], o['mathon_bound']):
        mm = re.match(r'R\((\d+),(\d+)\) >= (\d+)', b); recipe_here.setdefault((int(mm.group(1)), int(mm.group(2))), []).append((int(mm.group(3)), o['p'], o['omega'], b))
cov = []
for k, c in cells.items():
    ws = [r for r in ledger if key(r['parameters']) == k and r['claimed_bound']]   # a file whose author claims nothing is not counted
    ver = [r for r in ws if r['verdict'] == 'PASS']; par = [r for r in ws if r['verdict'] in ('PARTIAL', 'NOT_COMPLETED', 'NOT_CHECKED')]
    bv = max(ver, key=lambda r: (int(r['claimed_bound']), r['committed'] == 'yes'), default=None)
    bp = max(par, key=lambda r: int(r['claimed_bound']), default=None)
    note = notes.get(k, {}); lower = int(c['lower']) if c['lower'] else None
    rh = [x for x in recipe_here.get(k, []) if lower and x[0] >= lower]
    if lower is None: st = 'NO_SURVEY_BOUND'
    elif bv and int(bv['claimed_bound']) >= lower: st = 'VERIFIED'
    elif bp and int(bp['claimed_bound']) >= lower: st = 'PARTIAL'
    elif note.get('class') == 'recipe_only' or (not note and re.match(r'\d\.\d\.[a-z]', c['ref'] or '')) or rh: st = 'RECIPE'
    else: st = 'NO_FILE_FOUND'
    if st == 'NO_SURVEY_BOUND' and not ws: continue
    sn = note.get('witness_search_note', '')
    if rh: sn = (sn + '; ' if sn else '') + 'computed here: clique number of Q_%d is %d, so the construction gives %s; that graph was not built or checked here' % (rh[0][1], rh[0][2], rh[0][3])
    other = '; '.join('%s lists %s' % (t, v) for t, v in c['by_table'] if v and v != c['lower'])
    cov.append(dict(parameters=P(k), colours=len(k), survey_tables='/'.join(sorted(set(c['tables']))), survey_lower=c['lower'], lower_ref=c['ref'],
                    survey_table_of_lower='/'.join(sorted({t for t, v in c['by_table'] if v == c['lower']})), other_table_values=other, status=st,
                    best_verified=bv['claimed_bound'] if bv else '', verified_witness=bv['id'] if bv else '', verified_source=bv['source'] if bv else '',
                    exceeds_survey='yes' if (bv and lower and int(bv['claimed_bound']) > lower) else '',
                    best_unverified=bp['claimed_bound'] if bp and (not bv or int(bp['claimed_bound']) > int(bv['claimed_bound'])) else '',
                    unverified_witness=bp['id'] if bp and (not bv or int(bp['claimed_bound']) > int(bv['claimed_bound'])) else '',
                    unverified_check=(bp['verdict'] + ': ' + bp['checked']) if bp and (not bv or int(bp['claimed_bound']) > int(bv['claimed_bound'])) else '',
                    search_note=sn))
with open('results/coverage.csv', 'w', newline='') as fo:
    w = csv.DictWriter(fo, fieldnames=list(cov[0])); w.writeheader(); w.writerows(cov)

# ---------- summary
def group(r):
    k = key(r['parameters'])
    if len(k) > 2: return 'multicolour'
    return 'two-colour, k <= l <= 15' if k[1] <= 15 else 'two-colour, l > 15'
S = dict(manifest_witnesses=len(man), committed=sum(m['committed'] == 'yes' for m in man),
         ledger_verdicts=dict(collections.Counter(r['verdict'] for r in ledger)),
         ledger_by_source={s: dict(collections.Counter(r['verdict'] for r in ledger if r['source'] == s)) for s in sorted({r['source'] for r in ledger})},
         graphs_pass=sum(int(r['graphs_checked'] or 1) for r in ledger if r['verdict'] == 'PASS'),
         coverage={g: dict(collections.Counter(r['status'] for r in cov if group(r) == g)) for g in ('two-colour, k <= l <= 15', 'two-colour, l > 15', 'multicolour')},
         survey_cells_with_lower_bound=sum(1 for r in cov if r['survey_lower']))
S['exceeds'] = [dict(parameters=r['parameters'], survey_lower=int(r['survey_lower']), survey_tables=r['survey_table_of_lower'], other_table_values=r['other_table_values'], verified=int(r['best_verified']),
                     witness=r['verified_witness'], source=r['verified_source']) for r in cov if r['exceeds_survey']]
S['unverified_above_survey'] = [dict(parameters=r['parameters'], survey_lower=int(r['survey_lower']) if r['survey_lower'] else None, claimed=int(r['best_unverified']),
                                     witness=r['unverified_witness'], check=r['unverified_check']) for r in cov if r['best_unverified'] and (not r['survey_lower'] or int(r['best_unverified']) > int(r['survey_lower']))]
S['no_survey_bound_verified'] = [dict(parameters=r['parameters'], verified=int(r['best_verified']), witness=r['verified_witness']) for r in cov if r['status'] == 'NO_SURVEY_BOUND' and r['best_verified']]
S['no_public_witness'] = [dict(parameters=r['parameters'], survey_lower=int(r['survey_lower']), lower_ref=r['lower_ref'], status=r['status'], best_verified=r['best_verified'])
                          for r in cov if r['status'] in ('NO_FILE_FOUND', 'RECIPE')]
S['partial'] = [dict(parameters=r['parameters'], survey_lower=int(r['survey_lower']), witness=r['unverified_witness'], claimed=int(r['best_unverified']), check=r['unverified_check'])
                for r in cov if r['status'] == 'PARTIAL']
# runs
rc = collections.defaultdict(lambda: dict(records=0, graphs=0, seconds=0.0))
for i, rs in runs.items():
    for r in rs:
        x = rc[r['run']]; x['records'] += 1; x['graphs'] += r.get('graphs_checked', 1) if r.get('verdict') == 'PASS' else 0; x['seconds'] += r.get('seconds', 0)
macpass = {i for i, rs in runs.items() if {r['half'] for r in rs if r['run'] == 'mac' and r.get('result') == 'OK'} == {'no_clique', 'no_independent_set'}}
rc['mac']['graphs'] = len(macpass)
S['runs'] = {k: dict(records=v['records'], graphs_pass=v['graphs'], seconds=round(v['seconds'], 1)) for k, v in sorted(rc.items())}
S['run_verifiers'] = {k: sorted({r['verifier'] for rs in runs.values() for r in rs if r['run'] == k}) for k in rc}
rep = {i: [r for r in rs if r['run'] == 'repo'] for i, rs in runs.items()}
ov = [i for i, rr in rep.items() if rr and any(r['run'] != 'repo' and 'half' not in r for r in runs[i])]
S['rerun_overlap'] = len(ov)
S['rerun_disagreements'] = [i for i in ov if {r['verdict'] for r in runs[i] if 'half' not in r} != {'PASS'} or len({r.get('n') for r in runs[i] if 'half' not in r}) != 1]
S['repo_run_new_ids'] = sorted(i for i, rr in rep.items() if rr and i not in ov)
S['mac_half_runs'] = len([r for rs in runs.values() for r in rs if 'half' in r])
S['mac_duplicate_half_runs'] = S['mac_half_runs'] - len({(r['id'], r['half']) for rs in runs.values() for r in rs if 'half' in r})
S['paley_omega'] = omega
S['mac_max_half_seconds'] = max((r['seconds'] for rs in runs.values() for r in rs if 'half' in r), default=0)
S['unclaimed_files'] = [dict(id=r['id'], n=int(r['n']), verdict=r['verdict']) for r in ledger if not r['claimed_bound']]
st = open('results/selftest_output.txt').read() if os.path.exists('results/selftest_output.txt') else ''
S['selftest'] = 'ALL TESTS PASS' if 'ALL TESTS PASS' in st else 'not run or failed'
json.dump(S, open('results/summary.json', 'w'), indent=1)
print(json.dumps({k: S[k] for k in ('ledger_verdicts', 'graphs_pass', 'coverage', 'rerun_overlap', 'rerun_disagreements', 'runs')}, indent=1))
