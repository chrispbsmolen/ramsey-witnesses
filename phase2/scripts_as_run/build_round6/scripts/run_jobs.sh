#!/bin/bash
# Runs the jobs in a list, P at a time, each as its own process under nice -n 10 and a 600 s cap.
# Usage: run_jobs.sh JOBLIST P BUILT_DIR      (each job line: CELL COLOUR CHECKER MODE TIMEOUT)
HERE=$(cd "$(dirname "$0")" && pwd)
cat "$1" | xargs -P "$2" -L 1 sh -c 'nice -n 10 timeout 600 python3 -I "'"$HERE"'/window_check.py" "'"$3"'" "$0" "$1" "$2" "$3" "$4" > /dev/null 2>&1 || echo "job exit $? : $0 $1 $2 $3"'
