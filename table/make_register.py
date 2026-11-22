"""Write table/register.csv, table/cells.csv, table/claims.csv and table/CURRENT.md.

Inputs: the closed phase records (pinned in table/closed_inputs.csv) and the open intake (table/intake.csv).
Run from anywhere: python3 table/make_register.py
"""
import os, sys, csv, gzip, hashlib, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)
sys.path.insert(0, ROOT)
import verify_ramsey as V


def key(s):
    return ','.join(map(str, sorted(int(x) for x in s.split(','))))


def rd(f):
    with open(f, newline='') as h:
        return list(csv.DictReader(h))


def sha(p):
    return hashlib.sha256(open(p, 'rb').read()).hexdigest()


def write_csv(path, cols, rows):
    with open(path, 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=cols, lineterminator='\r\n')
        w.writeheader()
        w.writerows(rows)


for p in rd('table/closed_inputs.csv'):
    if sha(p['path']) != p['sha256']:
        raise SystemExit('closed input changed: %s. A closed record changes only with an entry in CORRECTIONS.md '
                         'and a new pin in table/closed_inputs.csv in the same commit.' % p['path'])

ORIGINS = {'third party: public file', 'third party: sent by the author', 'third party: printed, transcribed here',
           'built here from a published construction', 'found here by search'}
CHECKS = {'two checkers, every color', 'two checkers, symmetry-reduced', 'two checkers and a cited theorem',
          'one checker, every color', 'one checker, some colors', 'not completed', 'not checked', 'failed'}
DECISIONS = {'pending', 'accepted', 'failed', 'noted', 'withdrawn'}
BASES = {'in the survey table', "implied by the survey's own items", 'above the survey table'}
WITNESS_CHECKS = {'two checkers, every color', 'two checkers, symmetry-reduced', 'two checkers and a cited theorem',
                  'one checker, every color'}

COLS = ['witness_id', 'cell', 'colors', 'n', 'n_measured_here', 'bound_from_witness', 'claimed_bound', 'origin', 'file_credit',
        'public_date', 'construction_credit', 'bound_credit', 'survey_basis', 'license', 'held', 'file', 'url',
        'sha256', 'canonical_hash', 'checks', 'check_scope', 'check_date', 'check_record', 'label_in_phase',
        'registration', 'entered_on', 'decision', 'record_of', 'notes']


def n_of(fmt, path):
    if fmt == 'lengths':
        with gzip.open(path, 'rt') as f:
            return int(f.readline().split()[0])
    if fmt == 'g6':
        line = V.g6_lines(path)[0]
        b = line[0] - 63
        return b if b < 63 else (line[1] - 63) * 4096 + (line[2] - 63) * 64 + (line[3] - 63)
    with gzip.open(path, 'rt') if path.endswith('.gz') else open(path) as f:
        return sum(1 for l in f if l.strip())


cov1 = {key(c['parameters']): c for c in rd('results/coverage.csv')}
cov2 = {key(c['cell']): c for c in rd('phase2/coverage.csv')}
src = {s['source']: s for s in rd('sources/sources.csv')}
claims1 = {(key(c['parameters']), c['source']): c['where_claimed'] for c in rd('sources/claims.csv')}
cross = {l.split(':')[0] for l in open('results/crosscheck_output.txt') if ': n = ' in l}
RUN_DATE = {'cloud': '2026-11-03', 'cloud_constructions': '2026-11-03', 'repo': '2026-11-04'}

reg = []


def survey_lower(cell):
    c = cov1.get(cell)
    return int(c['survey_lower']) if c and c['survey_lower'] else None


def add(r):
    out = {c: '' for c in COLS}
    out.update(r)
    out['cell'] = key(out['cell'])
    out['colors'] = str(len(out['cell'].split(',')))
    if out['n']:
        out['bound_from_witness'] = str(int(out['n']) + 1)
    c = cov1.get(out['cell'])
    out['bound_credit'] = c['lower_ref'] if c else ''
    lo = survey_lower(out['cell'])
    if not out['survey_basis'] and out['bound_from_witness'] and lo is not None and out['checks'] in WITNESS_CHECKS:
        out['survey_basis'] = 'in the survey table' if int(out['bound_from_witness']) <= lo else 'above the survey table'
    reg.append(out)


P1 = {'PASS': 'one checker, every color', 'PARTIAL': 'one checker, some colors', 'NOT_COMPLETED': 'not completed',
      'NOT_CHECKED': 'not checked', 'FAIL': 'failed'}
for l in rd('results/ledger.csv'):
    chk = P1[l['verdict']]
    if l['verdict'] == 'PASS' and l['id'] in cross:
        chk = 'two checkers, every color'
    dates = sorted({RUN_DATE[r] for r in l['runs'].split(';') if r in RUN_DATE})
    stored = l['committed'] == 'yes'
    add(dict(witness_id='p1:' + l['id'], cell=l['parameters'], n=l['n'], n_measured_here='',
             origin='built here from a published construction' if l['source'] == 'constructed_here'
             else 'third party: public file',
             file_credit=src[l['source']]['name'], public_date='not recorded in phase 1',
             license=src[l['source']]['license found'], held='stored' if stored else 'linked',
             file=l['file'] if stored else '', url=l['url'], sha256=l['sha256'],
             checks=chk, check_scope=l['checked'], check_date=' and '.join(dates),
             check_record='results/ledger.csv, results/VERIFICATION.md',
             label_in_phase='phase 1: ' + l['verdict'], registration='registration/REGISTRATION_phase1.md',
             entered_on='2026-11-04', decision='accepted' if chk in WITNESS_CHECKS else '',
             record_of='results/ledger.csv', notes=claims1.get((key(l['parameters']), l['source']), '')))

ent = {e['file']: e['entered_on'] for e in rd('table/phase2_entered.csv')}
man = {m['file']: m for m in rd('phase2/witnesses/manifest.csv')}
P2 = {'computer': 'two checkers, every color', 'symmetry': 'two checkers, symmetry-reduced',
      'proof': 'two checkers and a cited theorem', 'search': 'two checkers, every color'}


def origin2(c):
    if c.get('group') == 'search':
        return 'found here by search'
    lic = c['license']
    if lic.startswith('sent by the author'):
        return 'third party: sent by the author'
    if lic.startswith('built here'):
        return 'built here from a published construction'
    if 'transcribed' in lic:
        return 'third party: printed, transcribed here'
    return 'third party: public file'


def reg2(c):
    if c.get('group') == 'search':
        return 'registration/REGISTRATION_phase2.md, Amendment %s' % ('6' if key(c['cell']) == '3,3,3,7' else '2')
    return 'registration/REGISTRATION_phase2.md'


for c in rd('phase2/coverage.csv'):
    if not c['witness']:
        continue
    m = man[c['witness']]
    add(dict(witness_id='p2:' + os.path.basename(c['witness']), cell=c['cell'], n=c['n'],
             n_measured_here=str(n_of(m['format'], c['witness'])), origin=origin2(c), file_credit=m['credit'],
             public_date='not recorded in phase 2', license=c['license'], held='stored', file=c['witness'],
             url=c['url'], sha256=c['sha256_file'], checks=P2[c['group']], check_scope=c['checks'],
             check_record='phase2/CHECKS.md', label_in_phase='phase 2: ' + c['label'], registration=reg2(c),
             entered_on=ent[c['witness']], decision='accepted', record_of='phase2/coverage.csv', notes=c['notes']))
for c in rd('phase2/above_survey.csv'):
    m = man[c['witness']]
    add(dict(witness_id='p2:' + os.path.basename(c['witness']), cell=c['cell'], n=c['n'],
             n_measured_here=str(n_of(m['format'], c['witness'])), origin=origin2(c), file_credit=m['credit'],
             public_date='not recorded in phase 2', survey_basis="implied by the survey's own items",
             license=c['license'], held='stored', file=c['witness'], url=c['url'], sha256=c['sha256_file'],
             checks='two checkers, every color', check_scope=c['checks'], check_record='phase2/CHECKS.md',
             label_in_phase='phase 2: ' + c['label'], registration='registration/REGISTRATION_phase2.md, Amendment 8',
             entered_on=ent[c['witness']], decision='accepted', record_of='phase2/above_survey.csv',
             notes=c['notes']))

intake = rd('table/intake.csv')
for i in intake:
    if i['decision'] not in DECISIONS:
        raise SystemExit('intake %s: decision %r is not one of %s' % (i['intake_id'], i['decision'], sorted(DECISIONS)))
    if i['decision'] == 'noted':
        continue
    if i['decision'] == 'accepted':
        if not i['sha256'] or not (i['file'] or i['url']) or i['checks'] not in WITNESS_CHECKS or not i['check_record']:
            raise SystemExit('intake %s: accepted needs a SHA-256, a file or URL, a check record and a passing check'
                             % i['intake_id'])
        if i['file'] and sha(i['file']) != i['sha256']:
            raise SystemExit('intake %s: file does not match its SHA-256' % i['intake_id'])
    n_here = str(n_of(i['format'], i['file'])) if i['file'] else ''
    if n_here and n_here != i['n']:
        raise SystemExit('intake %s: n is %s in the row and %s in the file' % (i['intake_id'], i['n'], n_here))
    add(dict(witness_id='in:' + i['intake_id'], cell=i['cell'], n=i['n'], n_measured_here=n_here,
             claimed_bound=i['claimed_bound'], origin=i['origin'], file_credit=i['file_credit'], public_date=i['public_date'],
             construction_credit=i['construction_credit'], survey_basis=i['survey_basis'], license=i['license'],
             held=i['held'], file=i['file'], url=i['url'], sha256=i['sha256'], canonical_hash=i['canonical_hash'],
             checks=i['checks'], check_scope=i['check_scope'], check_date=i['checked_on'],
             check_record=i['check_record'], registration='registration/REGISTRATION_intake.md',
             entered_on=i['decision_on'] or i['received_on'], decision=i['decision'],
             record_of='table/intake.csv', notes=i['notes']))

for r in reg:
    for col, allowed in (('origin', ORIGINS), ('checks', CHECKS), ('survey_basis', BASES)):
        if r[col] and r[col] not in allowed:
            raise SystemExit('%s: %s %r is not one of %s' % (r['witness_id'], col, r[col], sorted(allowed)))
    if r['n_measured_here'] and r['n_measured_here'] != r['n']:
        raise SystemExit('%s: n is %s in the record and %s in the file' % (r['witness_id'], r['n'], r['n_measured_here']))
write_csv('table/register.csv', COLS, reg)


def is_witness(r):
    return r['decision'] == 'accepted' and r['checks'] in WITNESS_CHECKS and r['n'] and r['sha256']


CLAIM_COLS = ['intake_id', 'cell', 'claimed_bound', 'claimed_by', 'where_claimed', 'public_date', 'received_on',
              'why_not_checked', 'source_line', 'notes']
claims = [{c: i.get(c, '') for c in CLAIM_COLS} for i in intake if i['decision'] == 'noted']
for c, i in zip(claims, [i for i in intake if i['decision'] == 'noted']):
    c['cell'] = key(i['cell'])
    c['claimed_by'] = i['file_credit']
write_csv('table/claims.csv', CLAIM_COLS, claims)

by = collections.defaultdict(list)
for r in reg:
    by[r['cell']].append(r)
cells = []
allcells = list(cov1) + sorted({r['cell'] for r in reg} - set(cov1))
for k in allcells:
    c = cov1.get(k, {})
    lo = survey_lower(k)
    ws = [r for r in by[k] if is_witness(r)]
    best = max(ws, key=lambda r: (int(r['n']), r['checks'].startswith('two'), [-ord(x) for x in r['entered_on']]),
               default=None)
    at = [r for r in ws if lo is not None and int(r['bound_from_witness']) >= lo]
    if lo is None:
        now = 'no survey value'
    elif any(r['checks'].startswith('two') for r in at):
        now = 'survey value: witness checked by two checkers'
    elif at:
        now = 'survey value: witness checked by one checker'
    else:
        now = 'survey value: no checked witness'
    cells.append(dict(cell=k, survey_lower=c.get('survey_lower', ''), survey_ref=c.get('lower_ref', ''),
                      survey_tables=c.get('survey_table_of_lower', ''), status_4_nov=c.get('status', ''),
                      label_phase2=cov2[k]['label'] if k in cov2 else '', status_now=now,
                      best_bound=best['bound_from_witness'] if best else '',
                      best_witness=best['witness_id'] if best else '', best_origin=best['origin'] if best else '',
                      best_file_credit=best['file_credit'] if best else '', best_checks=best['checks'] if best else '',
                      above_survey='yes' if best and lo is not None and int(best['bound_from_witness']) > lo else '',
                      witnesses=str(len(ws)),
                      same_bound=';'.join(r['witness_id'] for r in ws if best and r is not best
                                          and r['bound_from_witness'] == best['bound_from_witness']),
                      received_not_counted=';'.join(r['witness_id'] for r in by[k]
                                                    if r['record_of'] == 'table/intake.csv' and not is_witness(r)),
                      claims=';'.join(x['intake_id'] for x in claims if x['cell'] == k)))
write_csv('table/cells.csv', list(cells[0]), cells)


def R(p):
    return 'R(%s)' % p


byid = {r['witness_id']: r for r in reg}
out = ['# Current table', '',
       'Written by `table/make_register.py` from `table/register.csv` and `table/cells.csv`. The columns are '
       'described in `table/COLUMNS.md`, and the rules for new witnesses in `registration/REGISTRATION_intake.md`. '
       'Survey: revision 18 (24 April 2026).', '',
       '## Checked witnesses above the survey\'s table', '',
       '| number | survey [ref] | bound from the witness | file credit | origin | checks | survey basis | entered |',
       '|---|---|---|---|---|---|---|---|']
for c in cells:
    if c['above_survey']:
        b = byid[c['best_witness']]
        out.append('| %s | %s [%s] | %s | %s | %s | %s | %s | %s |' % (
            R(c['cell']), c['survey_lower'], c['survey_ref'], c['best_bound'], b['file_credit'], b['origin'],
            b['checks'], b['survey_basis'], b['entered_on']))
out += ['', '## Survey values with no checked witness', '',
        '| number | survey [ref] | status on 4 November | phase-2 label |', '|---|---|---|---|']
for c in cells:
    if c['status_now'] == 'survey value: no checked witness':
        out.append('| %s | %s [%s] | %s | %s |' % (R(c['cell']), c['survey_lower'], c['survey_ref'],
                                                  c['status_4_nov'], c['label_phase2']))
out += ['', '## Received, not counted', '', '| number | witness | bound the file would give, or the bound claimed | decision | checks |', '|---|---|---|---|---|']
for r in reg:
    if r['record_of'] == 'table/intake.csv' and not is_witness(r):
        out.append('| %s | `%s` | %s | %s | %s |' % (R(r['cell']), r['witness_id'], r['bound_from_witness'] or r['claimed_bound'],
                                                     r['decision'], r['checks']))
if out[-1] == '|---|---|---|---|---|':
    out.append('| none | | | | |')
out += ['', '## Claims with no file checked here', '', '| number | claimed | by | where | why not checked |',
        '|---|---|---|---|---|']
for c in claims:
    out.append('| %s | %s | %s | %s | %s |' % (R(c['cell']), c['claimed_bound'], c['claimed_by'], c['where_claimed'],
                                              c['why_not_checked']))
if out[-1] == '|---|---|---|---|---|':
    out.append('| none | | | | |')
open('table/CURRENT.md', 'w').write('\n'.join(out) + '\n')
print(len(reg), 'register rows,', len(cells), 'cells,', len(claims), 'claims')
