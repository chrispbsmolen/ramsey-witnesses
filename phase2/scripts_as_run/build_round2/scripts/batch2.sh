#!/bin/bash
# sequential follow-up runs (one process at a time, each <= 10 min, ulimit 1.6 GB)
cd <cloud>/ramsey-p2/build_round2/scripts
ulimit -v 1600000
for a in "R4^4_n633 4" "R6^3_n1105 6" "R4^5_n4175 4" "R5^4_n4072 5"; do set -- $a
  for ch in repo_stream_full gen0_full; do timeout 600 python3 verify_linear.py "built/$1.lengths" $2 $ch all 580 | cut -c1-200; done; done
for a in "R4^4_n633 4 repo all" "R4^4_n633 4 mc all" "R6^3_n1105 6 repo all" "R6^3_n1105 6 mc all" "R5^4_n4072 5 repo all" "R4^5_n4175 4 repo all" "R4^5_n4175 4 mc all" \
         "R4^6_n32005 4 linear0 1" "R4^6_n32005 4 repo_stream 1" "R4^7_n160023 4 linear0 1" "R4^7_n160023 4 repo_nbhd 1" "R6^4_n23501 6 linear0 3" "R6^4_n23501 6 repo_stream 3" \
         "R4^4_n633 4 gen0_full 1" "R4^4_n633 4 repo_stream_full 1"; do set -- $a
  timeout 600 python3 negctl.py lowered "built/$1.lengths" $2 $3 $4; done
timeout 600 python3 negctl.py schur "built/R3^8_n5287.lengths"
timeout 600 python3 negctl.py schur "built/R3^9_n17804.lengths"
for ch in gen0 repo; do timeout 600 python3 verify_nbhd.py built/R8_8_9_n10768.colormat.gz 673 2 1 7 $ch - 560 | cut -c1-200; done
echo BATCH2_DONE
