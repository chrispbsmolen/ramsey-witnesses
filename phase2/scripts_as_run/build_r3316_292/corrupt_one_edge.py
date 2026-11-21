#!/usr/bin/env python3
"""corrupt_one_edge.py - copy of a colormat file with the colour of one edge {x,y} changed to digit D (both entries).
usage: corrupt_one_edge.py IN OUT X Y D"""
import sys, hashlib
src, out, x, y, d = sys.argv[1], sys.argv[2], int(sys.argv[3]), int(sys.argv[4]), sys.argv[5]
rows = [list(l.strip()) for l in open(src) if l.strip()]
old = rows[x][y]; assert x != y and old == rows[y][x] and old != d
rows[x][y] = rows[y][x] = d
open(out, 'w').write('\n'.join(''.join(r) for r in rows) + '\n')
print('edge {%d,%d}: digit %s -> %s; in sha256 %s; out sha256 %s' % (x, y, old, d, hashlib.sha256(open(src, 'rb').read()).hexdigest(),
                                                              hashlib.sha256(open(out, 'rb').read()).hexdigest()))
