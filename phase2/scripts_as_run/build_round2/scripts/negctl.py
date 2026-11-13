"""Negative controls: a checker must report FOUND when asked for a clique one smaller than the bound (lowered k),
or after one length of a Schur colouring is recoloured to create a monochromatic sum.  Logs to logs/negative_controls.jsonl."""
import sys, os, subprocess, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib2 as L
HERE = os.path.dirname(os.path.abspath(__file__))
def run(args):
    p = subprocess.run([sys.executable, os.path.join(HERE, 'verify_linear.py')] + args, capture_output=True, text=True, timeout=590)
    return json.loads(p.stdout.strip().split('\n')[-1])
mode = sys.argv[1]
if mode == 'lowered':
    f, k, ch, col = sys.argv[2], int(sys.argv[3]), sys.argv[4], sys.argv[5]
    r = run([f, str(k - 1), ch, col, '560'])
    txt = json.dumps(r['result'])
    ok = ('FOUND' in txt) or ('"verdict": "FAIL"' in txt) or ('"has_Kk": true' in txt)
    L.log('negative_controls.jsonl', dict(control='lowered k', file=f, k_used=k - 1, checker=ch, colour=col, fails_as_expected=ok, result=txt[:300]))
elif mode == 'schur':
    f = sys.argv[2]
    N, c = L.read_lengths(os.path.join(L.OUT, f))
    c2 = list(c); a = next(d for d in range(1, N) if c[d] == c[1] and d > 1)   # 1 and a same colour; recolour 1+a
    c2[1 + a] = c[1]
    tmp = os.path.join(L.OUT, 'logs', 'negctl_tmp.lengths'); L.write_lengths(N, c2, tmp)
    for ch in ('sumfree', 'repo_stream_full'):
        r = run(['logs/negctl_tmp.lengths', '3', ch, str(c[1]), '560'])
        txt = json.dumps(r['result'])
        L.log('negative_controls.jsonl', dict(control='Schur length %d recoloured to colour %d (1 + %d = %d)' % (1 + a, c[1], a, 1 + a), file=f, checker=ch,
                                               fails_as_expected=('FOUND' in txt) or ('FAIL' in txt), result=txt[:300]))
