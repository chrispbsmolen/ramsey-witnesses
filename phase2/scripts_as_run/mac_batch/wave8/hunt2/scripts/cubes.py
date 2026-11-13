"""Print the cubic residues mod a prime p (p = 1 mod 6) as a circulant distance list n:D
(distances reduced to 1..p//2; -1 is a cube when p = 1 mod 6, so the set is symmetric).
Usage: python3 cubes.py P [COSET]   COSET 0 = cubes, 1/2 = the cosets g*H0, g^2*H0 (g = least primitive root)."""
import sys
p = int(sys.argv[1]); c = int(sys.argv[2]) if len(sys.argv) > 2 else 0
assert p % 6 == 1 and all(p % q for q in range(2, int(p**.5) + 1))
def order(a):
    x, k = a, 1
    while x != 1: x = x * a % p; k += 1
    return k
g = next(a for a in range(2, p) if order(a) == p - 1)
H = {pow(x, 3, p) for x in range(1, p)}
assert len(H) == (p - 1) // 3 and all((p - h) in H for h in H)
S = sorted({(pow(g, c, p) * h) % p for h in H})
D = sorted({min(s, p - s) for s in S})
print('%d:%s' % (p, ','.join(map(str, D))))
