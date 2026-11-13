#!/bin/sh
# Run restartable legs (each its own process, under 10 minutes, nice 19) of one search command until it
# exits 0 (found) or 1 (UNSAT / exhausted), MAXLEGS legs are used, or the file $STOPFILE exists.
# usage: legs.sh MAXLEGS STOPFILE command args...
MAX=$1; STOP=$2; shift 2
i=0
while [ $i -lt $MAX ] && [ ! -f "$STOP" ]; do
  i=$((i+1))
  timeout 590 nice -n 19 "$@"; rc=$?
  echo "leg $i rc $rc $(date +%H:%M:%S)"
  [ $rc -eq 0 ] && exit 0
  [ $rc -eq 1 ] && exit 1
done
exit 3
