#!/usr/bin/env python3
"""summarise.py - one table row per (log file, label, ansatz): legs, total seconds, final result, clause counts / best
score.  Reads logs/*.jsonl; prints markdown.  usage: summarise.py LOGDIR"""
import sys, os, json, glob, collections
D = sys.argv[1]
rows = collections.OrderedDict(); starts = collections.Counter()
for f in sorted(glob.glob(os.path.join(D, '*.jsonl'))):
    if 'verify' in os.path.basename(f): continue
    for line in open(f):
        d = json.loads(line)
        if d.get('event') == 'leg_start':
            starts[(os.path.basename(f), d.get('label', ''))] += 1; continue
        key = (os.path.basename(f), d.get('label', ''), d.get('group') or d.get('mode', '') if 'group' in d else d.get('base', d.get('mode', '')),
               d.get('T'), d.get('add'))
        r = rows.setdefault(key, {'legs': 0, 'seconds': 0.0, 'last': None, 'method': d.get('method', ''), 'best': None})
        r['legs'] += 1; r['seconds'] += float(d.get('seconds') or d.get('wall_seconds') or 0); r['last'] = d
        b = d.get('best_score', d.get('best_score_order_reached'))
        if b is not None: r['best'] = b if r['best'] is None else (min(r['best'], b) if 'orbsa' in r['method'] else max(r['best'], b))
print('| log | label | ansatz / input | method | legs | CPU s (sum) | result | detail |')
print('|---|---|---|---|---|---|---|---|')
for (f, label, g, T, add), r in rows.items():
    d = r['last']; m = r['method'].split(' (')[0]
    if m.startswith('Kuznetsov'): detail = 'largest cyclic order reached %s; %s colourings saved' % (d.get('best_score_order_reached'), d.get('sym_file_colourings'))
    elif m.startswith('edgesa'): detail = 'best cost %s monochromatic forbidden cliques (start %s, T %s, %s moves last leg)' % (r['best'], d.get('start_cost'), T, d.get('moves'))
    elif m.startswith('orbsa'): detail = 'best cost %s (T %s)' % (r['best'], T)
    else: detail = 'lazy clauses %s, solve calls (last leg) %s' % (d.get('lazy_clauses_total'), d.get('solve_iterations'))
    res = d.get('result', 'TIME' if d.get('exit_code') == 124 else '')
    print('| %s | %s | %s | %s | %d | %.0f | %s | %s |' % (f, label, g if not add else '%s +%s' % (os.path.basename(str(g)), add), m, r['legs'], r['seconds'], res, detail))

ended = {(f, lab) for (f, lab, g, T, add) in rows}
for (f, lab), k in starts.items():
    if (f, lab) not in ended:
        print('| %s | %s | (see label) | symsat/extsat | %d started | about %d | TIME (every leg stopped by the 590 s process limit inside one solve call) | no end record |' % (f, lab, k, 580 * k))
print()
print('Legs started (leg_start records) per label, including legs stopped by the process limit:')
for (f, lab), k in starts.items(): print('- %s: %s: %d' % (f, lab, k))
