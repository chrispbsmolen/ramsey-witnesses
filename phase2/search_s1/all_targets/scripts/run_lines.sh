#!/bin/sh
# run lines A..B of a job list file as single legs in parallel (at most 2 lines), each under timeout 590, nice 19
S=$1; F=$2; A=$3; B=$4; cd $S; mkdir -p state/q/jobs
for i in $(seq $A $B); do sed -n "${i}p" $F > state/q/jobs/j$i.sh; ( timeout 580 nice -n 19 sh state/q/jobs/j$i.sh > /dev/null 2>&1; echo "rc=$? line $i: $(cut -c1-90 state/q/jobs/j$i.sh)" ) & done; wait
