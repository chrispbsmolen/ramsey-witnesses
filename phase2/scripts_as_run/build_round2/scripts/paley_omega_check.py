"""Exact check of the published clique number alpha of the Paley graph Q_p (input of the doublings).

Reduction (automorphisms of Q_p, checked here on the vertex sets used): x -> a x + b with a a nonzero square is an
automorphism and acts transitively on ordered edges, so a K_s (s >= 3) exists iff one contains 0 and 1; the
map sigma: x -> 1 - x fixes {0,1} (a = -1 is a square as p = 1 mod 4).  With B = N(0) & N(1), a K_s through
0, 1 exists iff for some a in B (one per sigma-orbit {a, 1-a}) the set B & N(a) holds a K_{s-3}.
Claims checked: (i) a K_alpha exists (one witness, verified edge by edge); (ii) no K_{alpha+1}: every orbit
representative a gives no K_{alpha-2} in B & N(a), decided by CHECKER:
   repo : checker/clique_r2 (repo clique.c)      gen0 : checker/gen0_r2 (independent of clique.c)
Usage: python3 paley_omega_check.py P ALPHA CHECKER [START END]   (orbit representatives START..END-1, for splitting)
Appends to logs/paley_omega.jsonl."""
import sys, os, json, time, subprocess
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import lib2 as L


def run(exe, k, A):
    buf = b'%d\n' % len(A) + b'\n'.join((r.astype(np.uint8) + 48).tobytes() for r in A) + b'\n'
    p = subprocess.run(['bash', '-c', 'ulimit -s unlimited; exec "$@"', 'x', exe, str(k)], input=buf, capture_output=True)
    return p.stdout.decode().strip()


def main():
    p, alpha, checker = int(sys.argv[1]), int(sys.argv[2]), sys.argv[3]
    exe = os.path.join(L.CHECKER, {'repo': 'clique_r2', 'gen0': 'gen0_r2'}[checker])
    QR = np.zeros(p, dtype=bool); QR[[x * x % p for x in range(1, p)]] = True
    B = [x for x in range(2, p) if QR[x] and QR[(x - 1) % p]]
    Bset = set(B)
    assert all(((1 - a) % p) in Bset for a in B), 'sigma does not preserve B'
    reps = sorted({min(a, (1 - a) % p) for a in B})
    start = int(sys.argv[4]) if len(sys.argv) > 4 else 0
    end = int(sys.argv[5]) if len(sys.argv) > 5 else len(reps)
    t0 = time.time(); found = []; outs = {}
    for a in reps[start:end]:
        T = [x for x in B if QR[(x - a) % p]]
        idx = np.array(T); A = QR[(idx[:, None] - idx[None, :]) % p]; np.fill_diagonal(A, False)
        o = run(exe, alpha - 2, A)
        if not o.startswith('NONE'): found.append((a, o[:80]))
        outs[a] = len(T)
    rec = dict(p=p, alpha=alpha, checker=checker, B=len(B), orbit_reps=len(reps), range=[start, end],
               claim='no K_%d in Q_%d' % (alpha + 1, p), found=found, verdict='PASS' if not found else 'FAIL',
               max_subproblem=max(outs.values()) if outs else 0, seconds=round(time.time() - t0, 1))
    # (i) existence of a K_alpha: search K_{alpha-2} in B & N(a) for the first reps until found (clique.c output lists it)
    if start == 0 and checker == 'repo':
        for a in reps:
            T = [x for x in B if QR[(x - a) % p]]
            idx = np.array(T); A = QR[(idx[:, None] - idx[None, :]) % p]; np.fill_diagonal(A, False)
            o = run(exe, alpha - 3, A)
            if o.startswith('FOUND'):
                vs = [0, 1, a] + [T[int(v)] for v in o.split()[2:]]
                ok = all(QR[(u - v) % p] for u in vs for v in vs if u != v)
                rec['K_alpha_witness'] = dict(vertices=vs[:alpha], size=len(vs[:alpha]), all_edges_checked=ok and len(vs) >= alpha); break
    L.log('paley_omega.jsonl', rec)


if __name__ == '__main__':
    main()
