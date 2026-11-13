# common.sh: sourced by every waveN.sh (POSIX sh; macOS /bin/sh).  Not run on its own.
#   P2       the phase-2 folder (default ~/Ramsey/phase2)
#   PY       the batch's own Python (a venv made by wave0.sh, so Homebrew's "externally managed" rule does not bite)
#   job LOG DIR CMD...   runs CMD in DIR, appends a header, all output (stdout+stderr), the /usr/bin/time
#                        report (wall time, max RSS) and the exit code to LOG.  Never overwrites a log.
#   Ctrl-C (or closing the Terminal window) stops every job of the wave: the trap kills the wave's whole
#   process group, so nothing is left running unattended.
P2=${P2:-$HOME/Ramsey/phase2}
PY=${PY:-$P2/mac_batch/venv/bin/python3}
MB=$P2/mac_batch
mkdir -p "$MB/logs" || exit 1
WAVELOG=$MB/logs/${WAVE:-wave}.log
if [ "$(uname)" = Darwin ] && [ -x /usr/bin/time ]; then TIMECMD="/usr/bin/time -l"
elif [ -x /usr/bin/time ]; then TIMECMD="/usr/bin/time -v"
else TIMECMD=""; fi

trap 'trap "" INT TERM HUP; echo "$(date "+%Y-%m-%d %H:%M:%S") ${WAVE:-wave}: interrupted, stopping all its jobs" | tee -a "$WAVELOG" >&2; kill -TERM 0; exit 130' INT TERM HUP

say() { echo "$(date '+%Y-%m-%d %H:%M:%S') ${WAVE:-wave}: $*" | tee -a "$WAVELOG"; }

job() {
    _log=$1; _dir=$2; shift 2
    mkdir -p "$(dirname "$_log")"
    { echo "=== start $(date '+%Y-%m-%d %H:%M:%S') wave=${WAVE:-?} dir=$_dir"; echo "=== cmd: $*"; } >>"$_log"
    say "start $(basename "$_log")"
    if [ -n "${DRYRUN:-}" ]; then echo "DRYRUN (cd $_dir && $TIMECMD $*)" >>"$_log"; _rc=0
    else ( cd "$_dir" && $TIMECMD "$@" ) >>"$_log" 2>&1; _rc=$?; fi
    echo "=== end $(date '+%Y-%m-%d %H:%M:%S') exit=$_rc" >>"$_log"
    say "done  $(basename "$_log") (exit $_rc)"
}

# R(5^5) check 2: stream_adj.py pipes the 2 GB adjacency matrix of one colour into clique.c (unchanged, run on a
# 1 GiB thread stack by clique_bigstack_mac), cliques through vertex 0 (--sym; the colouring is cyclic).
# The feeder exits after about a minute, once clique has read the matrix.  Usage: r55_clique COLOUR LIMIT_S
r55_clique() {
    job "$P2/hunt_multicolour/logs/mac_${WAVE}_clique_c$1.txt" "$P2/hunt_multicolour" \
        /bin/sh -c '"$0" -I "$2" converted/julojc_R5x5_n44337.lengths "$1" | CLIQUE_TIME_LIMIT="$3" ./mac_jobs/clique_bigstack_mac 5 --sym' \
        "$PY" "$1" mac_jobs/stream_adj.py "$2"
}

# Lanes that must not start while a stream_adj.py feeder is still piping its matrix into clique (keeps the
# wave at 4 busy processes): wait until no feeder is running.  The pattern matches only the python process.
wait_feeders() {
    sleep 5
    while pgrep -f "[-]I mac_jobs/stream_adj[.]py" >/dev/null 2>&1; do sleep 15; done
}

# G3 half: CELL HALF CHECKER, through verify_built.py with its 12 h cap (43200 s), solver clique_mac.
g3() {
    job "$P2/build_G3/logs/mac_${WAVE}_$(echo "$1" | tr , _)_$2_$3.txt" "$P2/build_G3" \
        "$PY" "$MB/with_clique_mac.py" "$P2/build_G3/tools" verify_built.py "$1" "$2" "$3" 43200
}

# build_G1_G2 J2/J3: one colour of one file, clique.c via onecolour.py, cap LIMIT_S.
#   g12_one TAG FORMAT PATH ENTRY COLOUR K LIMIT_S
g12_one() {
    job "$P2/build_G1_G2/logs/mac_${WAVE}_$1.txt" "$P2/build_G1_G2" \
        "$PY" "$MB/onecolour.py" checker "$2" "$3" "$4" "$5" "$6" "$7"
}

# build_G1_G2 J4: reduced_G2.py P 0 0 COLOUR (clique.c only; NX_MAX = 0 as in the spec).  Each subproblem gets
# a 6 h cap (orbit_check.py would otherwise use has_clique's default of 3600 s and stop with a traceback).
g12_reduced() {
    job "$P2/build_G1_G2/logs/mac_${WAVE}_J4_$1_c$2.txt" "$P2/build_G1_G2" \
        "$PY" "$MB/with_clique_mac.py" --default-timeout 21600 "$P2/build_G1_G2/checker" scripts/reduced_G2.py "$1" 0 0 "$2"
}

# hunt_two_colour: xcheck.py (networkx), independence side, cap LIMIT_S.  xcheck_job TAG WITNESS K,L LIMIT_S
xcheck_job() {
    job "$P2/hunt_two_colour/logs/mac_${WAVE}_$1.txt" "$P2/hunt_two_colour/scripts" \
        "$PY" xcheck.py circulant "$(cat "$P2/hunt_two_colour/witnesses/$2")" "$3" "$4" --sym
}

[ -n "${SKIP_PY_CHECK:-}" ] || [ -x "$PY" ] || { echo "missing $PY: run wave0.sh first" >&2; exit 1; }
