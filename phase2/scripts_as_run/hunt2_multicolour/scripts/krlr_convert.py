"""Kreher, Li, Radziszowski, 'Lower Bounds for Multi-Colored Ramsey Numbers from Group Orbits',
JCMCC 4 (1988) 87-96; scan at https://www.cs.rit.edu/~spr/PUBL/paper16.pdf.
Distance sets transcribed by eye from the 300 dpi rasterised scan (checked against tesseract OCR):
  Table III (p.93): 13 non-isomorphic cyclic (3,3,5)-Ramsey graphs on K44 (distances 1..22)
  Table IV  (p.94): 18 cyclic (3,4,4)-Ramsey graphs on K54 (distances 1..27)
  Table V   (p.94): the 2 non-isomorphic ones (= Table IV Nos. 1 and 10)
  Table I   (p.91): the graphs giving the bounds (= Table III No.1 and Table V No.1)
Colour 1 = Red, 2 = Green, 3 = Blue.  Circulant: edge {i,j} gets the colour of min(|i-j|, n-|i-j|).
Writes OUT/<name>.colormat (n rows of n digits, diagonal 0) and OUT/<name>.lengths (n; colour of d=1..n-1)."""
import sys, os
T3 = """1 4 9 12 15 22 | 2 3 10 14 18 19 | 5 6 7 8 11 13 16 17 20 21
1 4 12 15 22 | 2 3 10 14 18 19 | 5 6 7 8 9 11 13 16 17 20 21
1 4 10 16 21 | 2 5 6 15 18 22 | 3 7 8 9 11 12 13 14 17 19 20
1 3 11 16 18 20 | 2 6 9 14 17 22 | 4 5 7 8 10 12 13 15 19 21
1 3 11 16 18 20 | 2 6 9 14 17 | 4 5 7 8 10 12 13 15 19 21 22
1 3 10 14 18 | 2 5 8 11 12 15 | 4 6 7 9 13 16 17 19 20 21 22
1 3 7 11 15 20 | 2 8 9 12 13 | 4 5 6 10 14 16 17 18 19 21 22
1 3 10 14 18 22 | 2 8 9 12 13 | 4 5 6 7 11 15 16 17 19 20 21
1 3 10 14 22 | 2 8 9 12 13 | 4 5 6 7 11 15 16 17 18 19 20 21
1 3 8 12 17 22 | 2 9 10 13 14 | 4 5 6 7 11 15 16 18 19 20 21
1 3 8 13 15 19 | 4 7 12 21 22 | 2 5 6 9 10 11 14 16 17 18 20
1 3 8 15 19 | 4 7 12 13 21 22 | 2 5 6 9 10 11 14 16 17 18 20
1 3 8 15 19 | 4 7 12 21 22 | 2 5 6 9 10 11 13 14 16 17 18 20"""
T4 = """1 4 9 15 20 22 27 | 7 8 13 14 16 17 18 19 23 26 | 2 3 5 6 10 11 12 21 24 25
2 5 8 9 20 21 27 | 7 11 13 14 16 18 19 22 23 26 | 1 3 4 6 10 12 15 17 24 25
2 9 10 13 16 21 27 | 4 5 7 8 14 17 18 20 23 25 | 1 3 6 11 12 15 19 22 24 26
2 9 14 15 19 22 27 | 1 4 5 8 10 17 18 20 23 25 | 3 6 7 11 12 13 16 21 24 26
3 4 9 10 11 26 27 | 7 8 14 16 17 18 19 20 23 25 | 1 2 5 6 12 13 15 21 22 24
3 7 8 9 22 26 27 | 1 2 4 5 10 11 17 18 20 25 | 6 12 13 14 15 16 19 21 23 24
3 8 9 10 14 25 27 | 1 2 7 11 13 16 18 19 22 26 | 4 5 6 12 15 17 20 21 23 24
4 9 14 15 16 17 27 | 1 2 5 10 11 13 18 19 22 26 | 3 6 7 8 12 20 21 23 24 25
9 16 20 21 23 26 27 | 1 2 4 5 10 11 13 18 22 25 | 3 6 7 8 12 14 15 17 19 24
1 4 9 15 20 22 27 | 2 3 5 6 10 11 12 21 24 25 | 7 8 13 14 16 17 18 19 23 26
2 5 8 9 20 21 27 | 1 3 4 6 10 12 15 17 24 25 | 7 11 13 14 16 18 19 22 23 26
2 9 10 13 16 21 27 | 1 3 6 11 12 15 19 22 24 26 | 4 5 7 8 14 17 18 20 23 25
2 9 14 15 19 22 27 | 3 6 7 11 12 13 16 21 24 26 | 1 3 4 8 10 17 18 20 23 25
3 4 9 10 11 26 27 | 1 2 5 6 12 13 15 21 22 24 | 7 8 14 16 17 18 19 20 23 25
3 7 8 9 22 26 27 | 6 12 13 14 15 16 19 21 23 24 | 1 2 4 5 10 11 17 18 20 25
3 8 9 10 14 25 27 | 4 5 6 12 15 17 20 21 23 24 | 1 2 7 11 13 16 18 19 22 26
4 9 14 15 16 17 27 | 3 6 7 8 12 20 21 23 24 25 | 1 2 5 10 11 13 18 19 22 26
9 16 20 21 23 26 27 | 3 6 7 8 12 14 15 17 19 24 | 1 2 4 5 10 11 13 18 24 25"""


def parse(block, n, tag):
    """Rows are kept exactly as printed; a row that is not a partition of 1..n/2 is reported and skipped."""
    out = []
    for no, line in enumerate(block.strip().splitlines(), 1):
        sets = [[int(x) for x in p.split()] for p in line.split('|')]
        c = {}; dup = []
        for col, ds in enumerate(sets, 1):
            for d in ds:
                if d in c: dup.append(d)
                c[d] = col
        missing = sorted(set(range(1, n // 2 + 1)) - set(c))
        if dup or missing:
            print(tag, 'row', no, 'AS PRINTED is not a partition: repeated', dup, 'missing', missing, '-> skipped')
            continue
        out.append((no, [c[min(d, n - d)] for d in range(1, n)]))
    return out


def write(out, name, n, L):
    open(os.path.join(out, name + '.lengths'), 'w').write('%d\n%s\n' % (n, ' '.join(map(str, L))))
    with open(os.path.join(out, name + '.colormat'), 'w') as f:
        for i in range(n): f.write(''.join('0' if i == k else str(L[abs(i - k) - 1]) for k in range(n)) + '\n')


if __name__ == '__main__':
    out = sys.argv[1]; os.makedirs(out, exist_ok=True)
    for tag, block, n in (('T3', T3, 44), ('T4', T4, 54)):
        rows = parse(block, n, tag)
        for no, L in rows:
            write(out, 'krlr_%s_no%02d_n%d' % (tag, no, n), n, L)
            print(tag, no, 'ok', n)
