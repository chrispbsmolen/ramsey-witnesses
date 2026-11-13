# Li Mingbo, Li Yusheng, "Ramsey numbers and triangle-free Cayley graphs", J. Tongji Univ. (Nat. Sci.) 43(11) (2015) 1750-1752,
# DOI 10.11908/j.issn.0253-374x.2015.11.021. Table 2 (p.1752), column n = 171, alpha = 26.
# Read by eye from the PDF <user> supplied 7 Nov 2026 (papers/LiLi_JTongji_43-11_2015_1750-1752.pdf).
n = 171
A = [1,3,5,9,15,17,28,36,47,58,69,76,82,89,95,102,113,124,135,143,154,156,162,166,168,170]
assert len(set(A)) == len(A) == 26
assert all((n - a) in A for a in A), 'not inverse-closed'          # the paper requires inverse-closed A
S = set(A)
assert not any(((x + y) % n) in S for x in A for y in A), 'not sum-free'  # Theorem 1(2): sum-free <=> triangle-free
half = sorted(a for a in A if a <= n // 2)
print('inverse-closed, sum-free, |A| =', len(A), '; half distance set:', ','.join(map(str, half)))
open('lili/R3_27_n171_LiLi.circ', 'w').write(f'{n}:' + ','.join(map(str, half)) + '\n')
