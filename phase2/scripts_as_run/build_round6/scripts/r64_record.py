"""V of R(6^5) and R(6^6) is the R(6,6,6,6) object (build_round2/built/R6^4_n23501.lengths), VERIFIED (symmetry-reduced)
on 12 Nov.  Nothing is re-run here (its clique.c runs took 2673-2814 s, over the cap).  This script (a) re-hashes the
file, (b) re-checks on the file that it is a linear colouring of K_23501 in 4 colours and that it is cyclic
(c(d) = c(N-d)), which is what makes x -> x+1 mod N an automorphism for the --sym / linear0 runs, and (c) collects the
existing check records with their SHA-256 field: build_round2/logs/verify_linear.jsonl (colours 3, 4: linear0 and
clique.c) and mac_batch/wave8/logs (colours 1, 2: wave 8a linear0, wave 8b clique.c).
Usage: python3 r64_record.py R64_FILE VERIFY_LINEAR_JSONL WAVE8_LOG ...   Appends to logs/inputs.jsonl."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import r5lib as L
import r6common as C

path, vl, logs = sys.argv[1], sys.argv[2], sys.argv[3:]
N, c = C.read_lengths(path)
rec = dict(input='V64', name='R(6,6,6,6) object R6^4_n23501.lengths', sha256=L.sha256_file(path))
rec['sha_match'] = rec['sha256'] == C.R64[1]
rec.update(n=int(N), colours=sorted(set(int(x) for x in c[1:])), cyclic=bool((c[1:] == c[1:][::-1]).all()))
found = []
for line in open(vl):
    r = json.loads(line)
    if r.get('sha256') == C.R64[1]: found.append(dict(source='build_round2/logs/verify_linear.jsonl', record=r))
for lg in logs:
    for line in open(lg):
        if line.startswith('{'):
            r = json.loads(line)
            if r.get('sha256') == C.R64[1]: found.append(dict(source='mac_batch/wave8/logs/' + os.path.basename(lg), record=r))
summ = {}
for f in found:
    r = f['record']
    for col, res in r['result'].items():
        if r['k'] == 6: summ.setdefault(col, []).append('%s: %s' % (r['checker'], res['out'][:40]))
rec['existing_k6_records_by_colour'] = summ
rec['existing_records'] = found
ok = rec['sha_match'] and rec['cyclic'] and all(any(x.startswith('linear0: NONE') for x in summ.get(str(s), [])) and
                                                any(x.startswith('repo_stream: NONE') for x in summ.get(str(s), [])) for s in (1, 2, 3, 4))
rec['verdict'] = 'PASS (existing records, both checkers on every colour; cyclicity re-checked here)' if ok else 'NOT PASS'
L.log('inputs.jsonl', rec)
