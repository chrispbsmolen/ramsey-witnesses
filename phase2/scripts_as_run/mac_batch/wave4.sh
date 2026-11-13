#!/bin/sh
# Wave 4 (up to 12 h, 4 processes): the two long G3 networkx independence halves (12 h cap each) and
# R(15,15) >= 5485 symmetry-reduced clique.c check, colours 0 and 1 (build_G1_G2 J4, p = 2741).
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave4.sh
WAVE=wave4
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
say "begin"
( g3 8,11 indep nx ) &
( g3 7,12 indep nx ) &
( g12_reduced 2741 0 ) &
( g12_reduced 2741 1 ) &
wait
say "end; G3 PASS = \"result\": \"NONE\"; J4 PASS = last line \"verdict\": \"PASS\":"
grep -h '"result"' "$P2"/build_G3/logs/mac_wave4_*.txt | tee -a "$WAVELOG"
for f in "$P2"/build_G1_G2/logs/mac_wave4_J4_*.txt; do echo "$(basename "$f"): $(grep '"verdict"' "$f" | tail -1)"; done | tee -a "$WAVELOG"
