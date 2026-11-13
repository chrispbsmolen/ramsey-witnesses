#!/bin/sh
# Wave 8 (7 Nov 2026): the Mac jobs written after waves 0-7 were assembled.
#   R(3,27) > 171 (Li-Li circulant, Table 2 of LiLi 2015): checker 1 (verify_ramsey + clique.c) on the Mac, and the
#     missing networkx independence half (xcheck.py --sym, the same method as wave 7);
#   hunt2_two_colour/MAC_JOBS.txt J1 (n = 709, 907, 877) and J2 (p = 1069, 1213);
#   build_round2/macjobs/MAC_JOBS.md M1, M2, M3, M4.
# Everything runs on the copies inside mac_batch/wave8/ (inputs listed in wave8/SHA256SUMS); no other folder is
# written to except mac_batch/logs/ (the wave summary, as in waves 0-7).  Needs wave 0's venv (mac_batch/venv).
#
# Three parts, one at a time (README_wave8.txt has the time and memory table):
#   caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave8/wave8.sh a          (up to about 18 h, 4 lanes)
#   caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave8/wave8.sh b          (up to about 22 h, 4 lanes)
#   caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave8/wave8.sh r327split  (optional, 4 processes)
# Every part first runs the setup (checksums, Mac builds under new names, smoke tests and negative controls, about
# 3-5 min, 1 process) and stops if anything in it fails.  DRYRUN=1 logs the job commands without running them.
PART=${1:-}
case "$PART" in a|b|r327split|setup) ;; *)
    echo "usage: caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave8/wave8.sh a|b|r327split|setup" >&2; exit 2;; esac
case "$PART" in a) WAVE=wave8a;; b) WAVE=wave8b;; r327split) WAVE=wave8s;; setup) WAVE=wave8setup;; esac
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
W=$MB/wave8
L8=$W/logs
mkdir -p "$L8" "$W/round2/logs" || exit 1
export PYTHONDONTWRITEBYTECODE=1
# build_round2 scripts take their solvers from these variables (verify_linear.py, verify_nbhd.py)
export CLIQUE_BIN="$W/round2/checker/clique_bigstack_mac" LINEAR0_BIN="$W/round2/checker/linear0_mac" GEN0_BIN="$W/round2/checker/gen0_mac"
# the build_round2 spec asks for the largest stack macOS allows; clique.c itself runs on clique_bigstack's 1 GiB thread
ulimit -s 65520 2>/dev/null || ulimit -s "$(ulimit -H -s)" 2>/dev/null || :

# ---------------------------------------------------------------------------------------------------- setup
setup8() {
echo "=== wave8 setup start $(date '+%Y-%m-%d %H:%M:%S') part=$PART $(uname -a)"
fail() { echo "WAVE8 SETUP FAIL: $*"; exit 1; }
cd "$W" || fail "cd $W"
if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c SHA256SUMS || fail "checksum mismatch"
else sha256sum -c SHA256SUMS || fail "checksum mismatch"; fi
"$PY" -c 'import sys, numpy, networkx; print("python", sys.version.split()[0], "numpy", numpy.__version__, "networkx", networkx.__version__)' || fail "python imports (run wave0.sh first)"
command -v cc >/dev/null 2>&1 || fail "no cc (run: xcode-select --install)"
command -v bash >/dev/null 2>&1 || fail "no bash (the build_round2 scripts call bash -c)"

# Mac builds, each under a NEW name; nothing that exists is rebuilt or replaced
build() { out=$1; shift; if [ -e "$out" ]; then echo "keep existing $out"; else echo "cc $* -> $out"; cc "$@" -o "$out" || fail "cc $out"; fi; }
build "$W/r3_27/tools/clique_mac" -O2 "$W/r3_27/tools/clique.c"
build "$W/hunt2/tools/clique_mac" -O2 "$W/hunt2/tools/clique.c"
build "$W/round2/checker/clique_bigstack_mac" -O2 -I "$W/round2/checker" "$W/macsrc/clique_bigstack.c" -lpthread
build "$W/round2/checker/linear0_mac" -O2 "$W/round2/checker/linear0.c"
build "$W/round2/checker/gen0_mac" -O2 "$W/round2/checker/gen0.c"
# Two scripts hard-code a solver name: cube_alpha.py runs ../tools/clique, paley_omega_check.py runs
# checker/clique_r2 and checker/gen0_r2 (it ignores CLIQUE_BIN/GEN0_BIN).  In these copies no file of those
# names exists (the Linux binaries were not copied), so a symlink to the Mac build is made.  An existing
# file of that name is never touched: the setup stops instead.
alias_to() { a=$1; t=$2
    if [ -L "$a" ]; then [ "$(readlink "$a")" = "$t" ] || fail "$a is a symlink to $(readlink "$a"), expected $t"; echo "keep link $a -> $t"
    elif [ -e "$a" ]; then fail "$a exists and is not the expected link (a Linux binary?); left as it is"
    else ln -s "$t" "$a" || fail "ln -s $t $a"; echo "link $a -> $t"; fi; }
alias_to "$W/hunt2/tools/clique" clique_mac
alias_to "$W/round2/checker/clique_r2" clique_bigstack_mac
alias_to "$W/round2/checker/gen0_r2" gen0_mac

# smoke tests and negative controls (each must print the expected line, or the setup stops)
T3='3
011
101
110'
case "$(printf '%s\n' "$T3" | "$W/r3_27/tools/clique_mac" 3)" in "FOUND 3 "*) ;; *) fail "clique_mac (r3_27) triangle";; esac
case "$(printf '%s\n' "$T3" | "$W/hunt2/tools/clique" 4)" in "NONE 3"*) ;; *) fail "clique link (hunt2) triangle";; esac
case "$(printf '%s\n' "$T3" | "$W/round2/checker/clique_r2" 4)" in "NONE 3"*) ;; *) fail "clique_bigstack_mac triangle";; esac
case "$(printf '%s\n' "$T3" | "$W/round2/checker/gen0_r2" 3)" in "FOUND n=3 K=3"*) ;; *) fail "gen0_mac triangle";; esac
case "$(printf '%s\n' "$T3" | "$W/round2/checker/gen0_mac" 4)" in "NONE n=3 K=4"*) ;; *) fail "gen0_mac triangle K4";; esac
echo "OK solvers on a triangle"

cd "$W/r3_27" || fail cd
ONE='import sys, os, json; sys.path.insert(0, "tools"); import verify_ramsey as V; V.CLIQUE = os.path.abspath("tools/clique_mac"); print(json.dumps(V.verify(V.load(sys.argv[1], sys.argv[2], ""), [int(x) for x in sys.argv[3].split(",")], timeout=float(sys.argv[4]))))'
out=$("$PY" -c "$ONE" circulant 13:1,5 3,5 60); echo "$out"
case "$out" in *'"verdict": "PASS"'*) ;; *) fail "checker 1 on the (3,5;13) circulant";; esac
out=$("$PY" -c "$ONE" circulant 13:1,5 3,4 60); echo "negative control: $out"
case "$out" in *'"verdict": "FAIL"'*) ;; *) fail "checker 1 negative control (3,4) on 13:1,5 did not fail";; esac
out=$(cd scripts && "$PY" xcheck.py circulant 13:1,5 3,5 60 --sym); echo "$out"
case "$out" in *"clique number 2 (< 3, ok), independence number 4 (< 5, ok)"*) ;; *) fail "xcheck on 13:1,5";; esac
out=$(cd scripts && "$PY" xcheck.py circulant 13:1,5 3,4 60 --sym); echo "negative control: $out"
case "$out" in *"independence number 4 (NOT < 4)"*) ;; *) fail "xcheck negative control on 13:1,5";; esac
"$PY" make_sub.py R3_27_n171_LiLi.circ --check R3_27_n171_H0.colormat | tail -1 | grep -q "^CHECK OK identical" || fail "make_sub.py --check"
out=$("$PY" scripts/crosscheck_split.py colormat R3_27_n171_H0.colormat 1 100 144); echo "$out"
case "$out" in *'"omega_max": 15, "status": "done"'*) ;; *) fail "crosscheck_split tail of H0";; esac
echo "OK r3_27 tools (checker 1, xcheck, derived H0 file, split checker)"

cd "$W/hunt2" || fail cd
out=$("$PY" -c "$ONE" g6 witnesses/R6_16_n433_SLLLcubic.g6 6,16 600); echo "$out"
case "$out" in *'"verdict": "PASS"'*'"claim": "R(6,16) > 433"'*) ;; *) fail "J1-style verify on n=433";; esac
out=$("$PY" -c "$ONE" g6 witnesses/R6_16_n433_SLLLcubic.g6 6,15 600); echo "negative control: $out"
case "$out" in *'"verdict": "FAIL"'*) ;; *) fail "J1 negative control (6,15) on n=433 did not fail";; esac
out=$(cd scripts && "$PY" cube_alpha.py 433 16 60); echo "$out"
[ "$(echo "$out" | grep -c ': NONE 13 ')" = 2 ] || fail "cube_alpha p=433 L=16"
out=$(cd scripts && "$PY" cube_alpha.py 433 15 60); echo "negative control: $out"
[ "$(echo "$out" | grep -c ': FOUND 13')" -ge 1 ] || fail "cube_alpha negative control p=433 L=15 found nothing"
echo "OK hunt2 tools (J1 one-liner, cube_alpha.py)"

cd "$W/round2" || fail cd
out=$("$PY" scripts/verify_linear.py "built/R6^4_n23501.lengths" 6 linear0 3 600); echo "$out" | cut -c1-400
case "$out" in *'NONE N=23501 colour=3 k=6'*) ;; *) fail "verify_linear linear0 colour 3";; esac
out=$("$PY" scripts/verify_linear.py "built/R6^4_n23501.lengths" 6 repo_stream 3 600); echo "$out" | cut -c1-400
case "$out" in *'"out": "NONE 5"'*) ;; *) fail "verify_linear repo_stream colour 3 (clique_bigstack_mac)";; esac
out=$("$PY" scripts/verify_linear.py "built/R6^4_n23501.lengths" 5 repo_stream 3 600); echo "negative control: $out" | cut -c1-400
case "$out" in *'"out": "FOUND 5'*) ;; *) fail "verify_linear negative control k=5";; esac
out=$("$PY" scripts/verify_nbhd.py "built/R9^3_n15040.colormat.gz" 940 2 2 9 gen0 3 600); echo "$out" | cut -c1-400
case "$out" in *'"all_automorphisms": true, "transitive": true'*'PARTIAL_NONE n=2953 K=8 start_vertices_done=3/2953'*) ;; *) fail "verify_nbhd gen0 (3 start vertices)";; esac
out=$("$PY" scripts/paley_omega_check.py 101 5 repo); echo "$out"
case "$out" in *'"verdict": "PASS"'*'"all_edges_checked": true'*) ;; *) fail "paley_omega_check Q_101 repo";; esac
out=$("$PY" scripts/paley_omega_check.py 101 5 gen0); echo "$out"
case "$out" in *'"verdict": "PASS"'*) ;; *) fail "paley_omega_check Q_101 gen0";; esac
out=$("$PY" scripts/paley_omega_check.py 101 4 gen0); echo "negative control: $out"
case "$out" in *'"verdict": "FAIL"'*) ;; *) fail "paley_omega_check negative control alpha=4";; esac
echo "OK round2 tools (verify_linear, verify_nbhd, paley_omega_check)"
echo "=== wave8 setup OK $(date '+%Y-%m-%d %H:%M:%S')"
}

SL=$L8/wave8_setup.txt
say "setup (log $SL)"
setup8 2>&1 | tee -a "$SL"
tail -1 "$SL" | grep -q "^=== wave8 setup OK" || { say "SETUP FAILED, no job started (log $SL)"; exit 1; }
say "setup OK"
[ "$PART" = setup ] && exit 0

# ---------------------------------------------------------------------------------------------------- job helpers
ONE='import sys, os, json; sys.path.insert(0, "tools"); import verify_ramsey as V; V.CLIQUE = os.path.abspath("tools/clique_mac"); print(json.dumps(V.verify(V.load(sys.argv[1], sys.argv[2], ""), [int(x) for x in sys.argv[3].split(",")], timeout=float(sys.argv[4]))))'
# R(3,27) checker 1: verify_ramsey (translation reduction, tested by verify itself), clique.c, 24 h cap per half
r327_c1() { job "$L8/mac_${WAVE}_R3_27_c1_verify.txt" "$W/r3_27" "$PY" -c "$ONE" circulant "$(cat "$W/r3_27/R3_27_n171_LiLi.circ")" 3,27 86400; }
# its negative control on the object itself: with 3,26 the check must FAIL (alpha = 26); under 1 s in the cloud
r327_neg() { job "$L8/mac_${WAVE}_R3_27_c1_negative_3_26.txt" "$W/r3_27" "$PY" -c "$ONE" circulant "$(cat "$W/r3_27/R3_27_n171_LiLi.circ")" 3,26 600; }
# R(3,27) checker 2: xcheck.py (networkx), --sym, 24 h cap, as wave 7
r327_nx() { job "$L8/mac_${WAVE}_R3_27_xcheck.txt" "$W/r3_27/scripts" "$PY" xcheck.py circulant "$(cat "$W/r3_27/R3_27_n171_LiLi.circ")" 3,27 86400 --sym; }
# R(3,27) checker 2, split over 4 processes: crosscheck_split.py on H0 (make_sub.py), lane R = vertices v % 4 == R
r327_split() { job "$L8/mac_${WAVE}_R3_27_split_R$1.txt" "$W/r3_27" "$PY" scripts/crosscheck_split.py colormat R3_27_n171_H0.colormat 1 0 144 --mod 4 "$1"; }
# hunt2 J1: the spec's one-liner (verify(..., timeout=86400)), solver tools/clique_mac.  j1 TAG G6 K,L
j1() { job "$L8/mac_${WAVE}_J1_$1.txt" "$W/hunt2" "$PY" -c "$ONE" g6 "witnesses/$2" "$3" 86400; }
# hunt2 J2: cube_alpha.py P L 86400 (two clique.c subproblems, one after the other)
j2() { job "$L8/mac_${WAVE}_J2_alpha_$1.txt" "$W/hunt2/scripts" "$PY" cube_alpha.py "$1" "$2" 86400; }
# build_round2 M1/M2: verify_linear.py FILE K CHECKER COLOUR 86400.  r2lin TAG FILE K CHECKER COLOUR
r2lin() { job "$L8/mac_${WAVE}_$1.txt" "$W/round2" "$PY" scripts/verify_linear.py "built/$2" "$3" "$4" "$5" 86400; }
# build_round2 M3: verify_nbhd.py (automorphisms checked on the matrix first).  r2nbhd TAG COLOUR CHECKER
r2nbhd() { job "$L8/mac_${WAVE}_$1.txt" "$W/round2" "$PY" scripts/verify_nbhd.py "built/R9^3_n15040.colormat.gz" 940 2 "$2" 9 "$3" - 86400; }
# build_round2 M4: omega(Q_5501) = 16.  r2paley CHECKER
r2paley() { job "$L8/mac_${WAVE}_M4_5501_$1.txt" "$W/round2" "$PY" scripts/paley_omega_check.py 5501 16 "$1"; }
# Part b: the four repo_stream jobs each start a stream_adj.py feeder (552 MB of text; measured here: under
# 1 s on its own, a few seconds while clique.c reads it).  A lane waits until the previous lane's job has
# started and no feeder is running, so the feeders never overlap and the wave stays at 4 busy processes.
# wait_turn PREVIOUS_LOG
wait_turn() {
    while ! grep -q "^=== start" "$1" 2>/dev/null; do sleep 5; done
    while :; do
        sleep 20
        pgrep -f "[-]I $W/round2/checker/stream_adj[.]py" >/dev/null 2>&1 || return 0
    done
}

say "begin part $PART"
case "$PART" in
a)
    ( r327_c1; r327_neg; r327_nx; j1 R6_19_n709 R6_19_n709_SLLLcubic.g6 6,19; j1 R7_19_n907 R7_19_n907_SLLLcubic.g6 7,19 ) &
    ( r2lin M1_c1_linear0 "R6^4_n23501.lengths" 6 linear0 1; r2lin M1_c2_linear0 "R6^4_n23501.lengths" 6 linear0 2
      r2lin M2_c2_linear0 "R10^3_n23093.lengths" 10 linear0 2; r2lin M2_c3_linear0 "R10^3_n23093.lengths" 10 linear0 3
      r2paley gen0; r2paley repo; r2nbhd M3_c1_gen0 1 gen0; r2nbhd M3_c2_gen0 2 gen0 ) &
    ( j1 R6_20_n877 R6_20_n877_SLLLcubic.g6 6,20 ) &
    ( r2nbhd M3_c1_clique 1 repo; r2nbhd M3_c2_clique 2 repo; j2 1069 22 ) &
    wait
    say "end part a.  PASS lines (see README_wave8.txt):"
    { grep -h '"verdict"' "$L8"/mac_wave8a_R3_27_c1_verify.txt "$L8"/mac_wave8a_J1_*.txt
      grep -h '"verdict"' "$L8"/mac_wave8a_R3_27_c1_negative_3_26.txt | sed 's/^/negative control, must be FAIL: /' | cut -c1-200
      grep -h 'clique number' "$L8"/mac_wave8a_R3_27_xcheck.txt
      grep -h '"result"' "$L8"/mac_wave8a_M1_*.txt "$L8"/mac_wave8a_M2_*.txt "$L8"/mac_wave8a_M3_*.txt | cut -c1-600
      grep -h '"verdict"' "$L8"/mac_wave8a_M4_*.txt
      grep -h '^p=' "$L8"/mac_wave8a_J2_*.txt; } 2>/dev/null | tee -a "$WAVELOG"
    ;;
b)
    ( r2lin M1_c1_clique "R6^4_n23501.lengths" 6 repo_stream 1; j2 1213 21 ) &
    ( wait_turn "$L8/mac_wave8b_M1_c1_clique.txt"; r2lin M1_c2_clique "R6^4_n23501.lengths" 6 repo_stream 2 ) &
    ( wait_turn "$L8/mac_wave8b_M1_c1_clique.txt"; wait_turn "$L8/mac_wave8b_M1_c2_clique.txt"
      r2lin M2_c2_clique "R10^3_n23093.lengths" 10 repo_stream 2 ) &
    ( wait_turn "$L8/mac_wave8b_M1_c1_clique.txt"; wait_turn "$L8/mac_wave8b_M1_c2_clique.txt"; wait_turn "$L8/mac_wave8b_M2_c2_clique.txt"
      r2lin M2_c3_clique "R10^3_n23093.lengths" 10 repo_stream 3 ) &
    wait
    say "end part b.  PASS lines (see README_wave8.txt):"
    { grep -h '"result"' "$L8"/mac_wave8b_M1_*.txt "$L8"/mac_wave8b_M2_*.txt | cut -c1-600
      grep -h '^p=' "$L8"/mac_wave8b_J2_*.txt; } 2>/dev/null | tee -a "$WAVELOG"
    ;;
r327split)
    for R in 0 1 2 3; do ( r327_split $R ) & done
    wait
    say "end part r327split.  PASS = 4 lines with \"status\": \"done\" and omega_max <= 25 (alpha = 1 + max <= 26):"
    grep -h '"status"' "$L8"/mac_wave8s_R3_27_split_R?.txt 2>/dev/null | tee -a "$WAVELOG"
    ;;
esac
