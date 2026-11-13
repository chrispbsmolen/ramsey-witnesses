#!/bin/sh
# Wave 2 (about 1 h, 4 lanes = 4 processes): R(5^5) linear0 colours 1 and 2; G3 (8,11) independence half with
# clique.c; five short networkx clique halves of G3.
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave2.sh
WAVE=wave2
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
HM=$P2/hunt_multicolour; G3=$P2/build_G3
say "begin"
( job "$HM/logs/mac_wave2_linear0_c1.txt" "$HM" ./mac_jobs/linear0_mac converted/julojc_R5x5_n44337.lengths 1 5 ) &
( job "$HM/logs/mac_wave2_linear0_c2.txt" "$HM" ./mac_jobs/linear0_mac converted/julojc_R5x5_n44337.lengths 2 5
  g3 10,15 clique nx
  g3 8,19 clique nx ) &
( g3 8,11 indep repo
  g3 8,13 clique nx
  g3 8,15 clique nx ) &
( g3 7,16 clique nx ) &
wait
say "end; linear0 PASS = lines starting NONE; G3 PASS = \"result\": \"NONE\":"
grep -h '^NONE\|^FOUND\|^PARTIAL' "$HM"/logs/mac_wave2_linear0_c?.txt | tee -a "$WAVELOG"
grep -h '"result"' "$G3"/logs/mac_wave2_*.txt | tee -a "$WAVELOG"
