#!/bin/sh
# Wave 1 (about 20-25 min, 4 processes): R(3,3,3,11) >= 597, networkx crosscheck of colour 2 (no K_11),
# split by smallest vertex mod 4 (build_G1_G2 J1).
# Paste:  caffeinate -i /bin/sh ~/Ramsey/phase2/mac_batch/wave1.sh
WAVE=wave1
. "${P2:-$HOME/Ramsey/phase2}/mac_batch/common.sh"
G12=$P2/build_G1_G2
say "begin"
for R in 0 1 2 3; do
    job "$G12/logs/mac_wave1_J1_R$R.txt" "$G12" "$PY" scripts/crosscheck_split.py colormat built/R3_3_3_11_n596.txt.gz 2 0 596 --mod 4 $R &
done
wait
say "end; PASS needs 4 lines with \"status\": \"done\" and omega_max <= 10:"
grep -h '"status"' "$G12"/logs/mac_wave1_J1_R?.txt | tee -a "$WAVELOG"
