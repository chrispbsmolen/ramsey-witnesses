"""Per-cell verdicts from logs/certificates.jsonl, logs/inputs.jsonl and logs/windows.jsonl (no new computation).
A cell is VERIFIED (by proof: Rowley Thm 3.2) when: its certificate is CERTIFIED; every U and V input PASSes with both
checkers; and for every remaining U colour the window has NONE from clique.c and gen0 (mode whole, or every split range
covering S exactly once), with the lowered-k control FOUND by both.  Usage: python3 summarise.py LOGDIR > table"""
import sys, os, json
D = sys.argv[1]
rd = lambda f: [json.loads(l) for l in open(os.path.join(D, f))] if os.path.exists(os.path.join(D, f)) else []
cert = {r['certificate'].split(' via')[0]: r for r in rd('certificates.jsonl')}
inp = {}
for r in rd('inputs.jsonl'):
    if isinstance(r.get('colours'), dict):
        for s, v in r['colours'].items(): inp[(r['input'], s)] = v['verdict']
    if r['input'] == 'V64': inp[('V64', 'all')] = r['verdict']
win = rd('windows.jsonl')
NEED = {'R(7,7,7,7)': (['U7', 'V7'], [1, 2]), 'R(8,8,8,8)': (['U8', 'V8'], [1, 2]), 'R(9,9,9,9)': (['U9', 'V9'], [1, 2]),
        'R(5,5,5,5,5,5)': (['U5', 'V5'], [1, 2, 3]), 'R(6,6,6,6,6)': (['U6b', 'V64'], [1]), 'R(6,6,6,6,6,6)': (['U6', 'V64'], [1, 2])}
for cell, (ins, cols) in NEED.items():
    out = dict(cell=cell, certificate=cert.get(cell, {}).get('verdict', 'missing'))
    out['inputs'] = {i: sorted({v for (a, s), v in inp.items() if a == i}) for i in ins}
    wv = {}
    for s in cols:
        rs = [r for r in win if r['cell'] == cell and r['colour'] == s and r['sha_match']]
        d = {}
        for chk in ('clique', 'gen0'):
            whole = [r for r in rs if r['checker'] == chk and r['mode'] == 'whole']
            if any(r['found'] is False for r in whole): d[chk] = 'NONE (whole)'
            else:
                sp = [r for r in rs if r['checker'] == chk and r['mode'].startswith('split:')]
                S = rs[0]['S_size'] if rs else 0
                cov = sorted(tuple(r['range']) for r in sp if r['found'] is False)
                ok = bool(cov) and cov[0][0] == 0 and cov[-1][1] == S and all(cov[i][1] == cov[i + 1][0] for i in range(len(cov) - 1))
                d[chk] = 'NONE (split, ranges cover S exactly)' if ok else ('FOUND' if any(r['found'] for r in whole + sp) else 'NOT DONE')
            ctl = [r for r in rs if r['checker'] == chk and r['mode'] == 'control']
            d[chk + '_control'] = 'FOUND' if any(r['found'] is True for r in ctl) else 'missing'
            fu = [r for r in rs if r['checker'] == chk and r['mode'] == 'full']
            d[chk + '_full_no_reduction'] = ('NONE' if any(r['found'] is False for r in fu) else ('TIMEOUT %s s' % fu[0]['seconds'] if fu and fu[0]['found'] is None else ('FOUND' if any(r['found'] for r in fu) else 'not run')))
        l0 = [r for r in rs if r['mode'] == 'linear0']
        d['linear0'] = 'NONE' if any(r['found'] is False for r in l0) else ('not done' if l0 else 'not run')
        wv[s] = d
    out['windows'] = wv
    okw = all(v['clique'].startswith('NONE') and v['gen0'].startswith('NONE') and v['clique_control'] == 'FOUND' and v['gen0_control'] == 'FOUND' for v in wv.values())
    oki = all(x and all(y.startswith('PASS') for y in x) for x in out['inputs'].values())
    out['status'] = 'VERIFIED (by proof: Rowley AJC 81(2) Thm 3.2 pp.248-250)' if (okw and oki and out['certificate'].startswith('CERTIFIED')) else 'PARTIAL / not done'
    print(json.dumps(out))
