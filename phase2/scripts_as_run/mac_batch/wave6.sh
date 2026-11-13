#!/bin/sh
# Wave 6 (up to 24 h, 4 lanes): R(11,11) >= 1597 full verify_ramsey, both colours (J2); R(5^5) colour 1 with
# clique.c (big-stack wrapper); R(7,7,7) colour 2 (J3).  Every job capped at 24 h.
# Lanes 2-4 start only after the stream_adj.py feeder has finished (about 1 min), so at most 4 processes run.
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave6.sh
WAVE=wave6
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
say "begin"
( r55_clique 1 86400 ) &
( wait_feeders; g12_one J2_c0 g6 built/mathon797_R11_11.g6.gz 0 0 11 86400 ) &
( wait_feeders; g12_one J2_c1 g6 built/mathon797_R11_11.g6.gz 0 1 11 86400 ) &
( wait_feeders; g12_one J3_c2 colormat built/R7_7_7_n3213.txt.gz '' 2 7 86400 ) &
wait
say "end; R(5^5) PASS = NONE 4; J2 PASS = \"K11\": [false, \"NONE 10\"]; J3 PASS = \"K7\": [false, \"NONE 6\"]:"
grep -h '^NONE\|^FOUND\|^TIMEOUT' "$P2"/hunt_multicolour/logs/mac_wave6_clique_c1.txt | tee -a "$WAVELOG"
grep -h '"K11"\|"K7"' "$P2"/build_G1_G2/logs/mac_wave6_J*.txt | tee -a "$WAVELOG"
