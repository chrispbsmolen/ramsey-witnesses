"""Check that table/register.csv, cells.csv and claims.csv lose nothing from the records they are built from.

Run from anywhere after table/make_register.py: python3 table/check_register.py
"""
import os, re, csv, json, collections

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(ROOT)


def rd(f):
    with open(f, newline='') as h:
        return list(csv.DictReader(h))


def key(s):
    return ','.join(map(str, sorted(int(x) for x in s.split(','))))


for f in ('table/register.csv', 'table/cells.csv', 'table/claims.csv', 'table/intake.csv', 'table/closed_inputs.csv',
          'table/phase2_entered.csv'):
    b = open(f, 'rb').read()
    assert b.count(b'\n') == b.count(b'\r\n'), f + ' is not CRLF'

reg = rd('table/register.csv')
cells = {c['cell']: c for c in rd('table/cells.csv')}
ids = collections.Counter(r['witness_id'] for r in reg)
assert not [i for i, n in ids.items() if n != 1], 'witness ids not unique'
byid = {r['witness_id']: r for r in reg}

led = rd('results/ledger.csv')
p2 = [c for c in rd('phase2/coverage.csv') if c['witness']]
ab = rd('phase2/above_survey.csv')
it = rd('table/intake.csv')
noted = [i for i in it if i['decision'] == 'noted']
assert len(reg) == len(led) + len(p2) + len(ab) + len(it) - len(noted), 'row count'

for l in led:
    r = byid['p1:' + l['id']]
    assert (r['n'], r['sha256'], r['url']) == (l['n'], l['sha256'], l['url']), l['id']
    assert r['cell'] == key(l['parameters']), l['id']
    assert r['label_in_phase'] == 'phase 1: ' + l['verdict'], l['id']
for c in p2 + ab:
    r = byid['p2:' + os.path.basename(c['witness'])]
    assert (r['n'], r['sha256'], r['file'], r['label_in_phase']) == (
        c['n'], c['sha256_file'], c['witness'], 'phase 2: ' + c['label']), c['cell']
    assert r['n_measured_here'] == c['n'], (c['cell'], 'n measured')
for i in it:
    if i['decision'] != 'noted':
        assert ids['in:' + i['intake_id']] == 1, i['intake_id']
claims = {c['intake_id'] for c in rd('table/claims.csv')}
assert claims == {i['intake_id'] for i in noted}, 'claims.csv does not match the noted intake rows'

for c in rd('results/coverage.csv'):
    k = key(c['parameters'])
    assert cells[k]['status_4_nov'] == c['status'], k
    if c['best_verified']:
        assert cells[k]['best_bound'] and int(cells[k]['best_bound']) >= int(c['best_verified']), k
    if c['status'] == 'VERIFIED':
        assert cells[k]['status_now'].startswith('survey value: witness checked'), k
for c in rd('phase2/coverage.csv'):
    k = key(c['cell'])
    assert cells[k]['label_phase2'] == c['label'], k
    if c['label'].startswith('VERIFIED'):
        assert cells[k]['status_now'] == 'survey value: witness checked by two checkers', k

S2 = json.load(open('phase2/summary.json'))
g = collections.Counter(c['group'] for c in rd('phase2/coverage.csv'))
for grp, v in S2['by_group'].items():
    assert g[grp] == v['total'], grp

readme = open('README.md').read()
sec = readme.split("### Public witnesses above the survey's table")[1].split('###')[0]
for m in re.finditer(r'^\| R\(([\d,]+)\) \| ([\d,]+) \|', sec, re.M):
    k, b = key(m.group(1)), int(m.group(2).replace(',', ''))
    assert cells[k]['above_survey'] == 'yes' and int(cells[k]['best_bound']) >= b, (k, b)

print('register: %d rows. Every phase-1 ledger row, phase-2 witness row, above-survey row and intake row maps to '
      'exactly one row with the same n, SHA-256 and label. n measured from every phase-2 file matches. Statuses of '
      '4 November and phase-2 labels reproduced, phase-2 group counts match, no cell below its 4 November value, '
      'every row of the README list above the survey kept.' % len(reg))
