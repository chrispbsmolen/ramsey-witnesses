#!/bin/sh
# Job queue for one core: each line of QUEUE is "MAXLEGS<TAB>command"; a line is run through legs.sh
# (restartable legs under 10 min each) and recorded in QUEUE.done with its exit code. Re-running the queue skips done lines.
S=$1; Q=$2; touch $Q.done
while true; do
  line=$(grep -vxF -f $Q.done $Q | grep -v '^#' | grep -v '^$' | head -1)
  [ -z "$line" ] && break
  [ -f $S/state/STOP_queue ] && break
  max=$(printf '%s' "$line" | cut -f1); cmd=$(printf '%s' "$line" | cut -f2-)
  cd $S; sh $S/src/legs.sh $max $S/state/STOP_queue sh -c "$cmd"; rc=$?
  echo "$line" >> $Q.done; echo "$(date +%H:%M:%S) rc=$rc $cmd" >> $Q.log
done
