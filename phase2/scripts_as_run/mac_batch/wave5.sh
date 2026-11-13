#!/bin/sh
# Wave 5 (up to about 15 h, 4 processes): R(16,16) >= 5605 symmetry-reduced check, colours 0 and 1 (J4, p = 2801);
# R(7,7,7) >= 3214 full verify_ramsey, colours 0 and 1 (J3).
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave5.sh
WAVE=wave5
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
say "begin"
( g12_reduced 2801 0 ) &
( g12_reduced 2801 1 ) &
( g12_one J3_c0 colormat built/R7_7_7_n3213.txt.gz '' 0 7 86400 ) &
( g12_one J3_c1 colormat built/R7_7_7_n3213.txt.gz '' 1 7 86400 ) &
wait
say "end; J4 PASS = \"verdict\": \"PASS\"; J3 PASS = \"K7\": [false, \"NONE 6\"]:"
for f in "$P2"/build_G1_G2/logs/mac_wave5_J4_*.txt; do echo "$(basename "$f"): $(grep '"verdict"' "$f" | tail -1)"; done | tee -a "$WAVELOG"
grep -h '"K7"' "$P2"/build_G1_G2/logs/mac_wave5_J3_*.txt | tee -a "$WAVELOG"
