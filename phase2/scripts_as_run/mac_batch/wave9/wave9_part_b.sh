#!/bin/sh
# Wave 9 (13 Nov 2026, REGISTRATION_phase2.md Amendment 9): three long Mac runs, each its own command.
#   a   R(19,19): clique number of the Paley graph on p = 8941 vertices (needed: 17), both checkers, 4 lanes
#   b   R(20,20): the same for p = 10861 (needed: 18), 4 lanes
#   c   R(6,13):  Kuznetsov's public search for a cyclic (6,13;346) colouring, 4 threads (success uncertain)
# Paste ONE line into Terminal (README_wave9.txt has times, memory and what the output means):
#   caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave9/wave9.sh a
#   caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave9/wave9.sh b
#   caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave9/wave9.sh c
# Also: "setup" (checks, builds, self-tests and a timing test; a few minutes; every part runs it first) and
# "status" (how far a and b are; starts nothing).
# Ctrl-C stops everything of the part.  Pasting the same line again continues where it stopped.
# Run one part at a time: each uses 4 busy processes.  All work runs at nice -n 10.  Nothing is deleted
# anywhere (there is no rm in this wave); records and logs are only appended to.
# Everything is written inside mac_batch/wave9/ (bin/, runs/, logs/) and mac_batch/logs/wave9*.log.
PART=${1:-}
case "$PART" in a|b|c|setup|status) ;; *)
    echo "usage: caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave9/wave9.sh a|b|c|setup|status" >&2; exit 2;; esac
WAVE=wave9$PART
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
W=$MB/wave9
L9=$W/logs
BIN=$W/bin
RUNS=$W/runs
mkdir -p "$L9" "$BIN" "$RUNS" || exit 1
export PYTHONDONTWRITEBYTECODE=1
# MACHINE.md: TMPDIR sometimes points at a volume that is not mounted, and then cc cannot write its temporary file
if [ -n "${TMPDIR:-}" ] && [ ! -d "$TMPDIR" ]; then TMPDIR=/tmp; export TMPDIR; fi
ulimit -s 65520 2>/dev/null || ulimit -s "$(ulimit -H -s)" 2>/dev/null || :
LANES=${W9_LANES:-4}   # W9_LANES=n sets the number of parallel lanes (default 4, as in part a)
W9_MODE=${W9_MODE:-ordered}
case "$W9_MODE" in ordered|plain) ;; *) echo "W9_MODE must be ordered or plain" >&2; exit 2;; esac
W9_CLIQUE=$BIN/clique_w9
W9_GEN0=$BIN/gen0_w9
export W9_MODE W9_CLIQUE W9_GEN0
KUZ=$BIN/kuz_w9
NICE="nice -n 10"

# ---------------------------------------------------------------------------------------------------- setup
setup9() {
echo "=== wave9 setup start $(date '+%Y-%m-%d %H:%M:%S') part=$PART $(uname -a)"
fail() { echo "WAVE9 SETUP FAIL: $*"; exit 1; }
cd "$W" || fail "cd $W"
if command -v shasum >/dev/null 2>&1; then shasum -a 256 -c SHA256SUMS || fail "checksum mismatch"
else sha256sum -c SHA256SUMS || fail "checksum mismatch"; fi
"$PY" -c 'import sys, numpy; print("python", sys.version.split()[0], "numpy", numpy.__version__)' || fail "python with numpy (run wave0.sh first)"
command -v cc >/dev/null 2>&1 || fail "no cc (run: xcode-select --install)"

# builds, each under a NEW name inside wave9/bin; an existing binary is kept, nothing is replaced
build() { out=$1; shift; if [ -e "$out" ]; then echo "keep existing $out"; else echo "cc $* -> $out"; cc "$@" -o "$out" || fail "cc $out"; fi; }
build "$W9_CLIQUE" -O2 "$W/paley/tools/clique.c"
build "$W9_GEN0" -O2 "$W/paley/tools/gen0.c"
T3='3
011
101
110'
case "$(printf '%s\n' "$T3" | "$W9_CLIQUE" 3 2>/dev/null)" in "FOUND 3 "*) ;; *) fail "clique_w9 triangle";; esac
case "$(printf '%s\n' "$T3" | "$W9_CLIQUE" 4 2>/dev/null)" in "NONE 3"*) ;; *) fail "clique_w9 triangle K4";; esac
case "$(printf '%s\n' "$T3" | "$W9_GEN0" 3)" in "FOUND n=3 K=3"*) ;; *) fail "gen0_w9 triangle";; esac
case "$(printf '%s\n' "$T3" | "$W9_GEN0" 4)" in "NONE n=3 K=4"*) ;; *) fail "gen0_w9 triangle K4";; esac
echo "OK solvers on a triangle"

# self-tests of the Paley driver on small primes whose clique numbers are already VERIFIED rows (Q_101: 5,
# Q_1277: 11), in both modes, with the negative control (asking for one less must FAIL).
# Each self-test has its own run folder; a repeated setup finds the pieces recorded and only re-applies the rule.
selftest() { mode=$1; p=$2; k=$3; want=$4; d=$RUNS/selftest_${p}_k${k}_$mode
    W9_MODE=$mode "$PY" "$W/paley/paley9.py" verify "$p" "$k" "$d" >/dev/null || fail "paley9 verify p=$p"
    for l in 0 1 2 3; do W9_MODE=$mode "$PY" "$W/paley/paley9.py" lane "$p" "$k" "$d" $l 4 >/dev/null || fail "paley9 lane p=$p"; done
    W9_MODE=$mode "$PY" "$W/paley/paley9.py" witness "$p" "$k" "$d" 0 1 >/dev/null || fail "paley9 witness p=$p"
    out=$(W9_MODE=$mode "$PY" "$W/paley/paley9.py" collect "$p" "$k" "$d" | tail -1); echo "selftest $mode: $out"
    case "$out" in "VERDICT p=$p: $want"*) ;; *) fail "paley9 self-test p=$p k=$k mode=$mode: expected $want";; esac; }
selftest ordered 101 5 PASS
selftest plain 101 5 PASS
selftest ordered 101 4 FAIL
selftest plain 101 4 FAIL
selftest ordered 1277 11 PASS
selftest ordered 1277 10 FAIL
for wf in "$W"/paley/witnesses/Q*_K*.txt; do [ -f "$wf" ] || continue
    b=$(basename "$wf" .txt); p=${b#Q}; p=${p%%_*}; k=${b##*_K}
    "$PY" -c 'import sys; sys.path.insert(0, sys.argv[1]); import paley9 as P
G = P.Paley(int(sys.argv[2])); vs = [int(x) for x in open(sys.argv[4]).read().replace(",", " ").split()]
ok = P.check_witness(G, int(sys.argv[3]), vs); print("witness file", sys.argv[4].split("/")[-1], "K_%s in Q_%s, every edge checked:" % (sys.argv[3], sys.argv[2]), ok); sys.exit(0 if ok else 1)' "$W/paley" "$p" "$k" "$wf" || fail "witness file $wf"
done
echo "OK paley9 self-tests (PASS on Q_101 and Q_1277, FAIL on both negative controls)"

# timing test on this machine: 3 pieces of the p = 8941 run (rep indices 447, 335, 223; ordered mode; nothing is
# recorded).  Cloud reference, one core, 13 Nov 2026: gen0 + clique.c took 100.7 seconds for the three.
out=$(W9_MODE=ordered $NICE "$PY" "$W/paley/paley9.py" time 8941 17 447,335,223) || fail "timing test"
echo "$out"
echo "$out" | "$PY" -c 'import sys, json
ref = float(sys.argv[1]); a_ch = float(sys.argv[2]); b_ch = float(sys.argv[3])
rs = [json.loads(l) for l in sys.stdin if l.startswith("{")]
assert len(rs) == 3 and all(r["gen0"] == "NONE" and r["clique"] == "NONE" for r in rs), "timing pieces must be NONE"
t = sum(r["gen0_seconds"] + r["clique_seconds"] for r in rs); f = t / ref
print("TIMING: the three test pieces took %.1f s here; the cloud reference is %.1f s; this machine is %.2f x the cloud time" % (t, ref, f))
print("TIMING: estimate for this machine at 4 lanes (divide by lanes/4 for more), ordered mode: part a about %.1f h, part b about %.1f h (plain mode: about 9 times longer)" % (a_ch * f / 4, b_ch * f / 4))' 100.7 17.4 80 || fail "timing test output"

if [ "$PART" = c ] || [ "$PART" = setup ]; then setup9c; fi
echo "=== wave9 setup OK $(date '+%Y-%m-%d %H:%M:%S')"
}

# Part c build: Kuznetsov's ramsey_df with the port in r6_13/port (no Windows, no SSE, no TBB needed).
# Preferred compiler: Homebrew g++ (has OpenMP).  Fallback: the system c++ (Apple clang) with the omp.h stand-in;
# then the "#pragma omp" loops run on one thread and only the parallel_for loops use 4 threads.
setup9c() {
    R=$W/r6_13
    if [ -e "$KUZ" ]; then echo "keep existing $KUZ"
    else
        GXX=""
        for c in /opt/homebrew/bin/g++-[0-9]* /usr/local/bin/g++-[0-9]*; do [ -x "$c" ] && GXX=$c; done
        built=""
        if [ -n "$GXX" ]; then
            echo "building kuz_w9 with $GXX -fopenmp"
            if "$GXX" -O2 -std=c++17 -w -fopenmp -DKZ_PORTABLE -include "$R/port/kz_port.h" -I"$R/port/sseshim" -I"$R/port" -I"$R" \
                "$R/port/kuz_ramsey.cpp" "$R/src/graph.cpp" "$R/port/driver.cpp" -o "$KUZ" -lpthread; then built="$GXX -fopenmp"; else echo "that build failed; trying the system c++"; fi
        fi
        if [ -z "$built" ]; then
            echo "building kuz_w9 with c++ and the omp.h stand-in"
            c++ -O2 -std=c++17 -w -DKZ_PORTABLE -include "$R/port/kz_port.h" -I"$R/port/sseshim" -I"$R/port/ompstub" -I"$R/port" -I"$R" \
                "$R/port/kuz_ramsey.cpp" "$R/src/graph.cpp" "$R/port/driver.cpp" -o "$KUZ" -lpthread || fail "could not build kuz_w9 with g++ or c++"
            built="c++ (no OpenMP)"
        fi
        echo "kuz_w9 built with: $built"
    fi
    # self-test: the same program on a small case, cyclic (5,7) colourings; it must stop by itself within a
    # few minutes and its largest colouring (order >= 63; the cloud runs reached 74 to 79) must pass both checkers.
    d=$RUNS/kuz_selftest_$(date '+%Y%m%d_%H%M%S'); mkdir -p "$d" || fail "mkdir $d"
    # (output capped at 20 MB and run time at 10 minutes, in case the program misbehaves on this machine)
    ( cd "$d" && KUZ_THREADS=4 KUZ_SEED=1 $NICE "$KUZ" ladder 3 5 30 62 20000 63 2>&1 | head -c 20000000 >selftest_stdout.txt ) &
    stpid=$!; stn=0
    while kill -0 "$stpid" 2>/dev/null; do
        sleep 5; stn=$(( stn + 1 ))
        if [ "$stn" -ge 120 ]; then pkill -TERM -f "kuz_w9 ladder 3 5 30 62" 2>/dev/null; fail "kuz_w9 self-test still running after 10 minutes (see $d/selftest_stdout.txt)"; fi
    done
    echo "kuz_w9 self-test run ended after about $(( stn * 5 )) s"
    out=$("$PY" "$R/kuz_check.py" "$d/sym57.txt" 5 7 63 "$d/check" --max 2 --full | grep -e "FIND CHECKED" -e "NO FIND"); echo "$out"
    case "$out" in *"FIND CHECKED: PASS"*) ;; *) fail "kuz_w9 self-test: no valid cyclic (5,7) colouring of order >= 63 (see $d)";; esac
    case "$out" in *"FIND CHECKED: FAIL"*) fail "kuz_w9 self-test wrote an invalid colouring (see $d)";; esac
    echo "OK kuz_w9 self-test (cyclic (5,7) colouring found and checked with both checkers)"
}

if [ "$PART" != status ]; then
    SL=$L9/wave9_setup.txt
    say "setup (log $SL)"
    setup9 2>&1 | tee -a "$SL"
    tail -1 "$SL" | grep -q "^=== wave9 setup OK" || { say "SETUP FAILED, nothing started (log $SL)"; exit 1; }
    say "setup OK"
    grep "^TIMING: estimate" "$SL" | tail -1
fi
[ "$PART" = setup ] && exit 0

# ---------------------------------------------------------------------------------------------------- parts a, b
# One lane: python (idle while it waits) plus one solver process.  Output goes to the terminal and to the lane log.
lane() { # lane MODE P K RUN LANE   (MODE = lane or witness)
    _log=$L9/mac_${WAVE}_paley$2_$1$5.txt
    { echo "=== start $(date '+%Y-%m-%d %H:%M:%S') wave=$WAVE mode=$W9_MODE"; echo "=== cmd: paley9.py $1 $2 $3 $4 $5 $LANES"; } >>"$_log"
    ( cd "$W/paley" && $TIMECMD $NICE "$PY" -u paley9.py "$1" "$2" "$3" "$4" "$5" "$LANES"; echo "=== end $(date '+%Y-%m-%d %H:%M:%S') exit=$?" ) 2>&1 | tee -a "$_log"
}
paley_status() { # P K
    RUN=$RUNS/paley_$1_$W9_MODE
    [ -d "$RUN" ] || { say "p=$1: not started (no folder $RUN)"; return 0; }
    ( cd "$W/paley" && "$PY" paley9.py collect "$1" "$2" "$RUN" "$W/paley/witnesses/Q$1_K$2.txt" ) 2>&1 | tee -a "$L9/mac_${WAVE}_paley$1_collect.txt" | tail -1 | tee -a "$WAVELOG"
}
paley_part() { # P K CELL
    P=$1; K=$2; RUN=$RUNS/paley_${P}_$W9_MODE
    if pgrep -f "paley9[.]py (lane|witness) $P " >/dev/null 2>&1; then say "a run for p=$P is already going (another window?); nothing started"; exit 1; fi
    mkdir -p "$RUN" || exit 1
    say "part $PART: $3, c(G_$P) = $K wanted, mode $W9_MODE, $LANES lanes, records in $RUN"
    ( cd "$W/paley" && "$PY" paley9.py verify "$P" "$K" "$RUN" ) 2>&1 | tee -a "$L9/mac_${WAVE}_paley${P}_verify.txt" | cut -c1-400
    tail -1 "$RUN/header.jsonl" | grep -q '"ok": true' || { say "automorphism checks FAILED for p=$P; nothing started"; exit 1; }
    l=0; while [ $l -lt $LANES ]; do lane lane "$P" "$K" "$RUN" $l & l=$((l+1)); done
    wait
    if [ ! -f "$W/paley/witnesses/Q${P}_K$K.txt" ]; then
        say "no K_$K witness file shipped for p=$P: searching for one (clique.c, $LANES lanes)"
        l=0; while [ $l -lt $LANES ]; do lane witness "$P" "$K" "$RUN" $l & l=$((l+1)); done
        wait
    fi
    say "end part $PART.  Coverage rule and verdict:"
    paley_status "$P" "$K"
}

# ---------------------------------------------------------------------------------------------------- part c
# Legs of Kuznetsov's cyclic ladder search for (6,13): k0 = 4, k1 = 11 in his convention (k - 2).
# First leg (no saved colourings yet): his Monte Carlo start and ladder, parameters patterned on his own (6,12)
# line "cyclic_ladder_search(69,4,10,140,5e4,227)": dim 69, start 140, 5e4 tests, log from order 141.
# Later legs: resume the ladder from the saved colourings of order >= (largest saved order - 8).
# The program appends every new colouring to sym613.txt as it goes (after each cluster of each pass); that file
# is the saved state.  Stop: Ctrl-C.  Continue: paste the same line again.
# W9_C_HOURS (default 72): after that many hours in this run the current leg is stopped and the part ends.
kuz_max() { _k=""; [ -s "$1" ] && _k=$(cut -f1 "$1" | grep -E '^[0-9]+$' | sort -n | tail -1); echo "${_k:-0}"; }
kuz_report() { # appends a one-line status to the terminal and the wave log
    _m=$(kuz_max "$CRUN/sym613.txt"); _n=0; [ -f "$CRUN/sym613.txt" ] && _n=$(wc -l <"$CRUN/sym613.txt" | tr -d ' ')
    say "R(6,13) search: $_n colourings saved, largest order $_m (a find is order 346 or more)"
}
part_c() {
    CRUN=$RUNS/kuz613; mkdir -p "$CRUN/legs" || exit 1
    HOURS=${W9_C_HOURS:-72}
    if pgrep -f "kuz_w9 (ladder|resume) 4 11" >/dev/null 2>&1; then say "an R(6,13) search is already running (another window?); nothing started"; exit 1; fi
    T_END=$(( $(date +%s) + HOURS * 3600 ))
    say "part c: search for a cyclic (6,13;346) colouring, 4 threads, up to $HOURS h in this run; state in $CRUN/sym613.txt"
    validated=""
    [ -f "$CRUN/port_validated.txt" ] && validated=yes
    short=0
    while :; do
        now=$(date +%s); [ "$now" -ge "$T_END" ] && { say "time limit of $HOURS h reached"; break; }
        best=$(kuz_max "$CRUN/sym613.txt")
        if [ "$best" -ge 346 ]; then break; fi
        leg=$(( $(ls "$CRUN/legs" | grep -c '^leg_[0-9]*[.]txt$') + 1 ))
        if [ "$best" -lt 141 ]; then mode="ladder 4 11 69 140 50000 141"
        else
            # a line cut off by an earlier Ctrl-C must not run into the next one: end the file with a newline
            [ -n "$(tail -c 1 "$CRUN/sym613.txt")" ] && echo >>"$CRUN/sym613.txt"
            st=$(( best - 8 )); [ "$st" -lt 141 ] && st=141
            mode="resume 4 11 $st 141"
        fi
        log=$CRUN/legs/leg_$leg.txt
        { echo "=== start $(date '+%Y-%m-%d %H:%M:%S') leg=$leg mode=$mode threads=4 seed=$leg"; } >>"$log"
        say "leg $leg: kuz_w9 $mode (log $log)"
        t0=$(date +%s)
        ( cd "$CRUN" && KUZ_THREADS=4 KUZ_SEED=$leg $TIMECMD $NICE "$KUZ" $mode; echo "=== end $(date '+%Y-%m-%d %H:%M:%S') exit=$?" ) >>"$log" 2>&1 &
        legpid=$!
        # while the leg runs: a status line every 10 minutes, the port validation once, the time limit, a find
        ticks=0
        while kill -0 "$legpid" 2>/dev/null; do
            sleep 20; ticks=$(( ticks + 1 ))
            best=$(kuz_max "$CRUN/sym613.txt")
            if [ -z "$validated" ] && [ "$best" -ge 141 ] && [ "$ticks" -ge 3 ]; then
                # first colourings written on this machine: check the largest with both checkers (shows the port works here)
                out=$($NICE "$PY" "$W/r6_13/kuz_check.py" "$CRUN/sym613.txt" 6 13 141 "$CRUN/port_validation" --max 1 2>&1 | grep -e "FIND CHECKED" -e "NO FIND")
                say "port validation on the largest colouring so far: $out"
                case "$out" in *"FIND CHECKED: PASS"*) echo "$(date '+%Y-%m-%d %H:%M:%S') $out" >>"$CRUN/port_validated.txt"; validated=yes;;
                    *) say "PORT VALIDATION FAILED: the search wrote a colouring that the checkers reject; stopping part c"; kill -TERM "$legpid" 2>/dev/null; pkill -TERM -f "kuz_w9 (ladder|resume) 4 11" 2>/dev/null; wait "$legpid" 2>/dev/null; exit 1;; esac
            fi
            if [ "$best" -ge 346 ] || [ "$(date +%s)" -ge "$T_END" ]; then
                kill -TERM "$legpid" 2>/dev/null; pkill -TERM -f "kuz_w9 (ladder|resume) 4 11" 2>/dev/null; break
            fi
            if [ $(( ticks % 30 )) -eq 0 ]; then
                kuz_report; grep -a "Cluster" "$log" | tail -1
                # disk guard: stop if the leg log passes 200 MB or the saved colourings pass W9_C_MAXMB (default 4000 MB)
                lk=$(du -k "$log" | cut -f1); sk=$(du -k "$CRUN/sym613.txt" 2>/dev/null | cut -f1)
                if [ "${lk:-0}" -gt 200000 ] || [ "${sk:-0}" -gt $(( ${W9_C_MAXMB:-4000} * 1024 )) ]; then
                    say "disk guard: leg log ${lk:-0} KB, sym613.txt ${sk:-0} KB; stopping part c"
                    kill -TERM "$legpid" 2>/dev/null; pkill -TERM -f "kuz_w9 (ladder|resume) 4 11" 2>/dev/null; wait "$legpid" 2>/dev/null; exit 1
                fi
            fi
        done
        wait "$legpid" 2>/dev/null
        kuz_report
        dt=$(( $(date +%s) - t0 ))
        if [ "$dt" -lt 120 ]; then short=$(( short + 1 )); else short=0; fi
        if [ "$short" -ge 3 ]; then say "three legs in a row ended within 2 minutes: the search has nothing left to extend (plateau); stopping"; break; fi
    done
    best=$(kuz_max "$CRUN/sym613.txt")
    if [ "$best" -ge 346 ]; then
        say "A COLOURING OF ORDER $best IS IN sym613.txt.  Checking it with both checkers (can take a while):"
        $NICE "$PY" "$W/r6_13/kuz_check.py" "$CRUN/sym613.txt" 6 13 346 "$CRUN/find" --max 3 2>&1 | tee -a "$L9/mac_${WAVE}_find_check.txt" | grep -e "FIND CHECKED" -e "NO FIND" | tee -a "$WAVELOG"
    else
        say "end part c: NO FIND.  Largest cyclic (6,13) colouring so far has order $best; 346 is needed.  Paste the same line to continue."
    fi
}

case "$PART" in
a) paley_part 8941 17 "R(19,19)";;
b) paley_part 10861 18 "R(20,20)";;
c) part_c;;
status) say "status (nothing is started)"; paley_status 8941 17; paley_status 10861 18
    if [ -f "$RUNS/kuz613/sym613.txt" ]; then CRUN=$RUNS/kuz613; kuz_report; else say "R(6,13) search: not started"; fi;;
esac
