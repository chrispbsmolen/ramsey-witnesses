"""Run one of the round scripts unchanged, but with verify_ramsey.py pointed at a Mac-built solver.

  python3 with_clique_mac.py [--default-timeout S] CHECKER_DIR SCRIPT [ARGS...]

CHECKER_DIR holds the unchanged copy of verify_ramsey.py and clique.c (build_G3/tools, build_G1_G2/checker).
The folder also holds `clique`, a Linux binary that cannot run on macOS.  verify_ramsey.py would only rebuild it
if it were older than clique.c, so instead of deleting or overwriting it this launcher sets
verify_ramsey.CLIQUE = CHECKER_DIR/clique_mac (built by wave0.sh: cc -O2 -o clique_mac clique.c).  Everything
else in verify_ramsey.py is untouched; the module object is the one SCRIPT then imports (same sys.modules entry).

--default-timeout S: changes only the DEFAULT of has_clique(timeout=3600), for callers that do not pass a timeout
(build_G1_G2/scripts/orbit_check.py, used by reduced_G2.py; its subproblems may need more than 1 h).
Explicit timeouts (verify_built.py passes its TIMEOUT_S) are not affected.
"""
import os, sys, runpy

a = sys.argv[1:]
deft = None
if a and a[0] == '--default-timeout':
    deft = float(a[1]); a = a[2:]
checker = os.path.abspath(a[0]); script = os.path.abspath(a[1])
sys.path.insert(0, checker)
import verify_ramsey as V
assert os.path.dirname(os.path.abspath(V.__file__)) == checker, V.__file__
V.CLIQUE = os.path.join(checker, 'clique_mac')
if not os.path.exists(V.CLIQUE):
    sys.exit('missing %s (wave0.sh builds it)' % V.CLIQUE)
if deft is not None:
    d = V.has_clique.__defaults__            # (sym=False, timeout=3600)
    assert len(d) == 2 and d[1] == 3600, d
    V.has_clique.__defaults__ = (d[0], deft)
print('with_clique_mac: solver %s, has_clique default timeout %s s' % (V.CLIQUE, V.has_clique.__defaults__[1]),
      file=sys.stderr, flush=True)
sys.argv = [script] + a[2:]
sys.path.insert(0, os.path.dirname(script))
runpy.run_path(script, run_name='__main__')
