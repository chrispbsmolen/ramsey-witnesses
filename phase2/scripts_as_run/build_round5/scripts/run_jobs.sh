#!/bin/sh
# Runs the R2 job list two at a time: one reduced subproblem and one checker per process, nice -n 10, 600 s cap per
# process (solver cap 570 s).  Usage: sh run_jobs.sh JOBS_FILE
cd "$(dirname "$0")" || exit 1
xargs -P 2 -L 1 sh -c 'timeout 600 nice -n 10 python3 cyclo_reduce.py solve "$1" "$2" "$3" "$4" "$5" "$6" "$7" "$8" 570 >/dev/null 2>&1 || echo "process failed: $*" >&2' x < "$1"
