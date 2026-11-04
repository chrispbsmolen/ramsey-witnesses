"""Verify the witnesses listed in sources/manifest.csv and append one record per witness to
results/runs/<RUN>.jsonl (resumable: ids already in that file are skipped).

  python3 run_ramsey.py RUN [--max-n N] [--quick] [--source S ...] [--id ID ...] [--timeout SECONDS]

--max-n N   only witnesses with at most N vertices
--quick     only witnesses with at most 60 vertices, or whose earlier recorded check
            (results/runs/*.jsonl) took at most 5 seconds; graph6 files with more than 3000
            graphs are skipped
graph6 files with up to 3000 graphs are checked line by line in full; larger files are sampled
(every (count // 200)-th line from line 0), and the record says so.
Witnesses with format 'none' (no loader here) and files missing from data/ are skipped and
reported; run fetch_data.py first.
"""
import os, sys, json, csv, time, glob, argparse, hashlib
import verify_ramsey as V
ROOT = os.path.dirname(os.path.abspath(__file__)); os.chdir(ROOT)


def stamp():
    h = lambda p: hashlib.sha256(open(p, 'rb').read()).hexdigest()[:16]
    return 'verify_ramsey.py %s, clique.c %s' % (h('verify_ramsey.py'), h('clique.c'))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument('run'); ap.add_argument('--max-n', type=int); ap.add_argument('--quick', action='store_true')
    ap.add_argument('--source', nargs='*'); ap.add_argument('--id', nargs='*'); ap.add_argument('--timeout', type=int, default=1800)
    a = ap.parse_args()
    out = 'results/runs/%s.jsonl' % a.run
    done = {json.loads(l)['id'] for l in open(out)} if os.path.exists(out) else set()
    earlier = {}
    for f in glob.glob('results/runs/*.jsonl'):
        if f == out: continue
        for l in open(f):
            r = json.loads(l)
            if 'seconds' in r and 'id' in r: earlier[r['id']] = max(earlier.get(r['id'], 0), r['seconds'])
    rows = list(csv.DictReader(open('sources/manifest.csv')))
    if a.source: rows = [r for r in rows if r['source'] in a.source]
    if a.id: rows = [r for r in rows if r['id'] in a.id]
    if a.max_n: rows = [r for r in rows if int(r['n']) <= a.max_n]
    if a.quick: rows = [r for r in rows if (not r['graphs_in_file'] or int(r['graphs_in_file']) <= 3000) and (int(r['n']) <= 60 or (r['id'] in earlier and earlier[r['id']] <= 5))]
    rows.sort(key=lambda r: int(r['n']))
    st = stamp(); t_all = time.time()
    with open(out, 'a') as fo:
        for r in rows:
            if r['id'] in done: continue
            if r['format'] == 'none': print('skip (no loader)', r['id']); continue
            if not os.path.exists(r['path']): print('skip (missing, run fetch_data.py)', r['id']); continue
            ks = [int(x) for x in r['parameters'].split(',')]
            rec = dict(run=a.run, id=r['id'], ks=ks, verifier=st); t0 = time.time()
            try:
                if r['format'] == 'circcsv':
                    n, D = V.circcsv_entry(r['path'], r['entry']); rec['sha256'] = V.sha256_text(V.circulant_key(n, D))
                else:
                    rec['sha256'] = V.sha256_file(r['path'])
                if rec['sha256'] != r['sha256']: raise ValueError('sha256 differs from the manifest')
                if r['format'] == 'g6':
                    lines = V.g6_lines(r['path']); cnt = len(lines)
                    idx = list(range(cnt)) if cnt <= 3000 else list(range(0, cnt, max(1, cnt // 200)))
                    res = [V.verify(V.from_g6(lines[i]), ks, timeout=a.timeout) for i in idx]
                    bad = [i for i, x in zip(idx, res) if x['verdict'] != 'PASS']
                    rec.update(n=res[0]['n'], graphs_in_file=cnt, graphs_checked=len(idx),
                               graphs_selection='all' if len(idx) == cnt else 'every %d-th line from line 0' % max(1, cnt // 200),
                               verdict='FAIL' if bad else 'PASS', checked='all colour classes')
                    if bad: rec['detail'] = 'lines failing: %s' % bad[:20]
                else:
                    x = V.verify(V.load(r['format'], r['path'], r['entry']), ks, timeout=a.timeout)
                    rec.update(n=x['n'], verdict=x['verdict'], checked='all colour classes', detail=x.get('note'))
                    if x.get('assignment'): rec['assignment'] = x['assignment']
            except Exception as e:
                rec.update(verdict='NOT_COMPLETED', checked='none', detail=repr(e)[:200])
            rec['seconds'] = round(time.time() - t0, 1)
            fo.write(json.dumps(rec) + '\n'); fo.flush()
            print(rec['verdict'], r['id'], rec['seconds'], flush=True)
    print('finished in %.0f s' % (time.time() - t_all))


if __name__ == '__main__':
    main()
