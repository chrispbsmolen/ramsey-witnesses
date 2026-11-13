#!/bin/sh
# Restartable legs of Kuznetsov's cyclic ladder search for (6,13) (k0=4, k1=11), each under 10 minutes.
# Leg 1: Monte Carlo start + ladder (parameters patterned on his (6,12) line: dim 69, start 140, mc 5e4).
# Later legs: resume the ladder from every cyclic colouring of order >= 141 saved in sym613.txt.
# Stops when the file STOP exists or after NLEGS legs. Logs each leg to logs/t613_kuznetsov.jsonl.
S=$1; NLEGS=$2; D=$S/state/kuz613; cd $D || exit 1
i=0
while [ $i -lt $NLEGS ] && [ ! -f $D/STOP ]; do
  i=$((i+1)); leg=$(ls $D/leg_*.log 2>/dev/null | wc -l); leg=$((leg+1)); t0=$(date +%s)
  if [ $leg -eq 1 ]; then mode="ladder 4 11 69 140 50000 141"; else
    # resume the ladder from the longest saved cyclic colourings only (order = max), so that each
    # 10-minute leg works on the current frontier instead of re-processing the same low clusters
    mx=$(cut -f1 $D/sym613.txt | sort -n | tail -1); st=$mx; mode="resume 4 11 $st 141"; fi
  KUZ_THREADS=1 KUZ_SEED=$leg timeout 580 nice -n 19 stdbuf -oL $S/bin/kuz $mode > $D/leg_$leg.log 2>&1; rc=$?
  t1=$(date +%s)
  python3 $S/src/kuz_summ.py $D $leg "$mode" $rc $((t1-t0)) >> $S/logs/t613_kuznetsov.jsonl
done
