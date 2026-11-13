import sys, json, time, os, re
D, leg, mode, rc, secs = sys.argv[1], int(sys.argv[2]), sys.argv[3], int(sys.argv[4]), int(sys.argv[5])
lens = []
p = os.path.join(D, 'sym613.txt')
if os.path.exists(p):
    for line in open(p):
        line = line.strip()
        if not line: continue
        tok = line.split('\t')
        try: lens.append(int(tok[0]))
        except ValueError: pass
log = open(os.path.join(D, f'leg_{leg}.log')).read()
best_pass = [int(m) for m in re.findall(r'best overall (\d+)', log)]
print(json.dumps({'logged_at': time.strftime('%Y-%m-%dT%H:%M:%S%z'), 'method': 'Kuznetsov ramsey_df cyclic ladder search (github ekuznetsov139/ramsey, commit f5c81c7b9ca4b1f570c1226665de9e67118bd8de; Linux port, GRAPH_MAX_LEN 6)',
                  'label': 'R(6,13) n=346 cyclic', 'leg': leg, 'mode': mode, 'seed': leg, 'threads': 1, 'exit_code': rc, 'seconds': secs,
                  'sym_file_colourings': len(lens), 'best_score_order_reached': max(lens) if lens else None,
                  'best_overall_in_leg_log': max(best_pass) if best_pass else None}, sort_keys=True))
