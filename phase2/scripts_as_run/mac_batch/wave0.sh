#!/bin/sh
# Wave 0 (setup, about 2-5 minutes, 1 process at a time): checksums, Python venv, Mac builds under NEW names,
# smoke tests on tiny inputs.  Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave0.sh
WAVE=wave0; SKIP_PY_CHECK=1
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
L=$MB/logs/wave0_setup.txt
setup() {
echo "=== wave0 start $(date '+%Y-%m-%d %H:%M:%S') $(uname -a)"
fail() { echo "WAVE0 FAIL: $*"; exit 1; }

# 1. folders and checksums (inputs, scripts, the unchanged checker copies, this batch's own files)
for d in hunt_multicolour hunt_two_colour build_G3 build_G1_G2 mac_batch; do [ -d "$P2/$d" ] || fail "missing folder $P2/$d"; done
cd "$P2" || fail "cd $P2"
if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c mac_batch/SHA256SUMS || fail "checksum mismatch"
else sha256sum -c mac_batch/SHA256SUMS || fail "checksum mismatch"; fi

# 2. Python: a venv for this batch (Homebrew python3 refuses a global pip install; Xcode python3 works too)
command -v python3 >/dev/null 2>&1 || fail "no python3 (install Xcode command line tools or Homebrew python)"
python3 -c 'import sys; assert sys.version_info >= (3, 8), sys.version' || fail "python3 older than 3.8"
[ -x "$PY" ] || python3 -m venv "$MB/venv" || fail "python3 -m venv"
"$PY" -c 'import numpy, networkx' 2>/dev/null || "$PY" -m pip install numpy networkx || fail "pip install numpy networkx"
"$PY" -c 'import sys, numpy, networkx; print("python", sys.version.split()[0], "numpy", numpy.__version__, "networkx", networkx.__version__)' || fail "imports"

# 3. C builds, each to a NEW file name (the Linux binaries shipped in the folders are left as they are)
command -v cc >/dev/null 2>&1 || fail "no cc (run: xcode-select --install)"
build() { out=$1; shift; if [ -e "$out" ]; then echo "keep existing $out"; else echo "cc $* -> $out"; cc "$@" -o "$out" || fail "cc $out"; fi; }
build "$P2/hunt_multicolour/mac_jobs/linear0_mac" -O2 "$P2/hunt_multicolour/mac_jobs/linear0.c"
build "$P2/hunt_multicolour/mac_jobs/clique_bigstack_mac" -O2 -I "$P2/build_G3/tools" "$MB/clique_bigstack.c" -lpthread
build "$P2/build_G3/tools/clique_mac" -O2 "$P2/build_G3/tools/clique.c"
build "$P2/build_G1_G2/checker/clique_mac" -O2 "$P2/build_G1_G2/checker/clique.c"

# 4. smoke tests (seconds).  Each prints OK or stops the wave.
T3='3
011
101
110'
case "$(printf '%s\n' "$T3" | "$P2/build_G3/tools/clique_mac" 3)" in "FOUND 3 "*) ;; *) fail "clique_mac G3 triangle";; esac
[ "$(printf '%s\n' "$T3" | "$P2/build_G1_G2/checker/clique_mac" 4)" = "NONE 3" ] || fail "clique_mac G1_G2 triangle"
[ "$(printf '%s\n' "$T3" | "$P2/hunt_multicolour/mac_jobs/clique_bigstack_mac" 4 --sym)" = "NONE 3" ] || fail "clique_bigstack_mac triangle"
echo "OK solvers on a triangle"
cd "$P2/hunt_multicolour" || fail cd
"$PY" -c 'import numpy as np
t = open("converted/julojc_R5x5_n44337.lengths").read().split(); N = int(t[0]); c = np.array([0] + [int(x) for x in t[1:]])
assert len(c) == N and (c[1:] == c[1:][::-1]).all() and set(c[1:].tolist()) == {1, 2, 3, 4, 5}
print("OK lengths file: N =", N, "colours 1..5, cyclic (c[d] == c[N-d]), degree of 0 per colour", [int((c == k).sum()) for k in range(1, 6)])' || fail "lengths file"
out=$(./mac_jobs/linear0_mac converted/julojc_R5x5_n44337.lengths 5 5); echo "$out"
case "$out" in NONE*) echo "OK linear0_mac colour 5 (cloud: NONE, 0.4 s)";; *) fail "linear0_mac colour 5";; esac
cd "$P2/build_G1_G2" || fail cd
out=$("$PY" "$MB/onecolour.py" checker colormat built/R3_3_3_3_n50.txt '' 0 3 60); echo "$out"
case "$out" in *'"K3": [false, "NONE 2"]'*) echo "OK onecolour.py on R(3,3,3,3) n=50, colour 0";; *) fail "onecolour.py smoke test";; esac
"$PY" -c 'import sys; sys.path.insert(0, "scripts"); import lib, constructions, orbit_check; print("OK reduced_G2 imports")' || fail "reduced_G2 imports"
cd "$P2/build_G3" || fail cd
"$PY" -c 'import sys; sys.path.insert(0, "tools"); sys.path.insert(0, "."); import verify_built; print("OK verify_built imports")' || fail "verify_built imports"
cd "$P2/hunt_two_colour/scripts" || fail cd
out=$("$PY" xcheck.py circulant "$(cat ../witnesses/R5_7_n79_CaET.circ)" 5,7 120 --sym); echo "$out"
case "$out" in *"clique number 6 (< 7, ok), independence number 4 (< 5, ok)"*) echo "OK xcheck.py on R(5,7) n=79";; *) fail "xcheck smoke test";; esac
echo "=== wave0 OK $(date '+%Y-%m-%d %H:%M:%S')"
}
setup 2>&1 | tee -a "$L"
grep -q "^=== wave0 OK" "$L" && tail -1 "$L" | grep -q "^=== wave0 OK" && say "OK, setup complete (log $L)" || { say "FAILED (log $L)"; exit 1; }
