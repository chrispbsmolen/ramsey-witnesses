# Check the cliques printed in SLLL (Discrete Math 250 (2002)), proof of Theorem 1, pp.206-208,
# against the cubic-residue graphs built in hunt2_two_colour/witnesses.
# SLLL: S1 = A0 (cubic residues mod p), S2 = A1 u A2. Theorem 3: [S_i] = [B_i] + 2, clique {0,e} u chain,
# e = g^k (k=0 for S1; k in {1,2} for S2). Theorem 2: R([S1]+1,[S2]+1) >= p+1.
import networkx as nx, sys
data = {  # p: (g, S1 chain, S2 chain, (k,l) claimed), transcribed from pp.206-208
 433:(5,[2,75,159],[50,72,112,61,143,118,55,11,14,36,121,-186,-176],(6,16)),
 547:(2,[31,-236,-237],[106,124,-74,-15,36,147,113,145,128,-213,-117,-63,-56,-13],(6,17)),
 613:(2,[9,-22,68],[18,-136,153,-16,286,132,13,117,128,241,291,-249,-119,-86,-32],(6,18)),
 709:(2,[45,-109,149],[5,-141,-116,-296,36,79,164,200,261,272,332,-298,-259,-227,-178,-130],(6,19)),
 877:(2,[90,149,29],[78,360,-335,112,-260,7,81,103,190,222,244,257,330,399,402,-294,-257],(6,20)),
 907:(2,[112,-293,146,-285],[162,-444,103,-265,108,-73,36,45,284,386,-412,-406,-335,-220,-188,-79],(7,19)),
 1069:(6,[78,-472,418],[175,-387,-284,-423,295,36,72,243,341,387,439,507,-459,-393,-376,-367,-103,-20,-11],(6,22)),
 1213:(2,[115,-176,87,336],[230,327,-259,278,-245,426,-248,283,361,432,435,578,-576,-315,-250,-243,-97,-7],(7,21)),
}
ok=True
for p,(g,c1,c2,(k,l)) in data.items():
    cubes={pow(x,3,p) for x in range(1,p)}
    assert pow(g,(p-1)//2,p)!=1 and all(pow(g,(p-1)//q,p)!=1 for q in {2,3}|{q for q in range(2,p) if (p-1)%q==0 and all(q%r for r in range(2,int(q**.5)+1))}), (p,'g not primitive')
    def cliq(S,set_):
        s=[x%p for x in S]; return len(set(s))==len(s) and all(((a-b)%p in set_) for i,a in enumerate(s) for b in s[i+1:])
    non={x for x in range(1,p)}-cubes
    r1=cliq([0,1]+c1,cubes)
    r2=[e for e in (g%p,pow(g,2,p)) if cliq([0,e]+c2,non)]
    # built witness: same graph? compare edge set of g6 with cubes circulant
    G=nx.read_graph6(f'hunt2_two_colour/witnesses/R{k}_{l}_n{p}_SLLLcubic.g6')
    same = G.number_of_nodes()==p and all(G.has_edge(0,x)==(x in cubes) for x in range(1,p))
    comp = (not same) and all(G.has_edge(0,x)==(x in non) for x in range(1,p))
    print(p,'g',g,'S1 clique',len(c1)+2,'=k-1' if len(c1)+2==k-1 else 'MISMATCH',r1,'| S2 clique',len(c2)+2,'=l-1' if len(c2)+2==l-1 else 'MISMATCH',bool(r2),'e=',r2,'| witness = cube graph' if same else ('| witness = complement (noncubes)' if comp else '| WITNESS DIFFERS'))
    ok &= r1 and bool(r2) and len(c1)+2==k-1 and len(c2)+2==l-1 and (same or comp)
print('ALL OK' if ok else 'PROBLEM')
