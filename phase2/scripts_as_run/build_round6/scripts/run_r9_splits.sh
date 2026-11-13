#!/bin/bash
# R(9,9,9,9) window, colour COLOUR, checker CHK: repeated budgeted calls of window_check.py split mode, each a separate
# process under nice -n 10 and a 600 s cap (560 s budget), each starting where the last completed range ended
# (read back from logs/windows.jsonl).  Usage: run_r9_splits.sh BUILT_DIR COLOUR CHK SIZE_OF_S
HERE=$(cd "$(dirname "$0")" && pwd); LOGS=${R5_LOGS:-$HERE/../logs}
while :; do
  END=$(python3 -I -c "
import json,sys
e=0
for l in open('$LOGS/windows.jsonl'):
    r=json.loads(l)
    if r['cell']=='R(9,9,9,9)' and r['colour']==$2 and r['checker']=='$3' and r['mode'].startswith('split:') and r['found'] is False and r['range'][0]==e: e=r['range'][1]
print(e)")
  [ "$END" -ge "$4" ] && break
  nice -n 10 timeout 600 python3 -I "$HERE/window_check.py" "$1" 'R(9,9,9,9)' "$2" "$3" "split:$END:$4" 560 > /dev/null 2>&1 || { echo "call failed at $END"; break; }
  NEW=$(grep -c . "$LOGS/windows.jsonl")
  grep '"cell": "R(9,9,9,9)"' "$LOGS/windows.jsonl" | tail -1 | grep -q '"found": true' && { echo "FOUND"; break; }
done
echo "done colour $2 $3 end=$END"
