#!/bin/sh
# Wave 7 (up to 24 h, 2 processes): hunt_two_colour networkx crosschecks, independence side, 24 h cap each.
# R(4,22) > 313 may finish; R(5,22) > 491 will probably hit the cap (estimate in MAC_BATCH.md).
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave7.sh
WAVE=wave7
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
say "begin"
( xcheck_job R4_22_n313 R4_22_n313_LinCa.circ 4,22 86400 ) &
( xcheck_job R5_22_n491 R5_22_n491_Ihr.circ 5,22 86400 ) &
wait
say "end; PASS = clique number below k and independence number 21 (< 22, ok):"
grep -h 'clique number' "$P2"/hunt_two_colour/logs/mac_wave7_*.txt | tee -a "$WAVELOG"
