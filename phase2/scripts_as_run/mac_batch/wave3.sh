#!/bin/sh
# Wave 3 (about 8 h, 4 lanes): R(5^5) colour 2 with clique.c (big-stack wrapper); the medium G3 halves.
# Lanes 2-4 start only after the stream_adj.py feeder has finished (about 1 min), so at most 4 processes run.
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave3.sh
WAVE=wave3
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
say "begin"
( r55_clique 2 86400 ) &
( wait_feeders; g3 7,12 indep repo; g3 5,15 indep nx ) &
( wait_feeders; g3 7,16 indep nx ) &
( wait_feeders; g3 7,16 indep repo; g3 9,10 indep nx; g3 9,10 clique nx ) &
wait
say "end; R(5^5) PASS = NONE 4; G3 PASS = \"result\": \"NONE\":"
grep -h '^NONE\|^FOUND\|^TIMEOUT' "$P2"/hunt_multicolour/logs/mac_wave3_clique_c2.txt | tee -a "$WAVELOG"
grep -h '"result"' "$P2"/build_G3/logs/mac_wave3_*.txt | tee -a "$WAVELOG"
