"""Write results.csv and sources.csv of build_round2 from the logs (file hashes are read from the logs and
re-hashed from disk; a mismatch stops the script)."""
import os, sys, csv, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import lib2 as L

OUT = L.OUT


def jl(name):
    p = os.path.join(L.LOGS, name)
    return [json.loads(l) for l in open(p)] if os.path.exists(p) else []


builds = {}
for r in jl('builds_linear.jsonl') + jl('builds_quad.jsonl') + jl('builds_two.jsonl') + jl('builds_paley.jsonl'):
    if 'cell' in r: builds[r['cell']] = r
for c, r in builds.items():
    if r.get('file'):
        got = L.sha256_file(os.path.join(OUT, r['file']))
        assert got == r['sha256'], (c, got, r['sha256'])

S = dict(
    survey='Radziszowski, Small Ramsey Numbers, EJC Dynamic Survey DS1 rev. 18 (24 Apr 2026), local <cloud>/ramsey-work/downloads/survey/DS1_rev18.pdf sha256 9519a676ee381f02f03269c22e3f101162b2fdcc9d432e4103cb1192fdff91bc',
    XXER='Xu, Xie, Exoo, Radziszowski, Constructive lower bounds on classical multicolor Ramsey numbers, EJC 11 (2004) #R35 (local build_G1_G2/downloads/v11i1r35.pdf sha256 a267b8188b336a771f34698a71949e6a7aaf6fa882fddbd1a400d87758a6930c)',
    Row1='Rowley, Constructive lower bounds for Ramsey numbers from linear graphs, Australas. J. Combin. 68(3) (2017) 385-395 (local hunt_multicolour/downloads/ajc_rowley/ajc_v68_p385.pdf sha256 0e970300aa694a781c66d76454f6f013342a788fec890ac6d5b280850c35fdba)',
    Row2='Rowley, Australas. J. Combin. 78(1) (2020) 1-10, CC BY-ND 4.0 (local hunt_multicolour/downloads/ajc_rowley/ajc_v78_p001.pdf sha256 f66933cdf7a11180c20d7f11dd17dc3e872f7f66c13fa2e2346d85699aa0e3bf)',
    Row3='Rowley, A generalised linear Ramsey graph construction, Australas. J. Combin. 81(2) (2021) 245-256, CC BY 4.0 (local hunt_multicolour/downloads/ajc_rowley/ajc_v81_p245.pdf sha256 703de8bf591ffcfcab8d4d5445ab0d820278dedc3e6e359f68ac4e3dc8af5615)',
    Row5='Rowley, arXiv:2203.13476v3 (source tarball https://arxiv.org/src/2203.13476, local hunt_multicolour/downloads/arxiv_2203.13476/src.tar sha256 5041096a33d6898c116a35a102e521fb14fe872fb18c20ff7d30822ed4c396b2; ancillary spreadsheet anc/content.xml sha256 d2280f45c90d0d55d6f3ba11270e0755d7649553c5d81e7089c852bf6bb6d8c4; arXiv non-exclusive licence)',
    AgCP='Ageron, Casteras, Pellerin, Portella, Rimmel, Tomasik, arXiv:2112.03175v2 (local hunt_multicolour/downloads/arxiv_2112.03175/2112.03175v2.pdf sha256 0bef5716f171992d6b125cfea15551b4e065eecfb243cd7b3e73884cbe5ca703)',
    Ex10='Exoo, A lower bound for Schur numbers and multicolor Ramsey numbers of K3, EJC 1 (1994) #R8 p.2 (local hunt_multicolour/downloads/ejc_Ex10/v1i1r8.pdf sha256 d56540f55003a94585f0f79ee338792ee6e850ea03de4ec77ebf854d91f35fb4)',
    XuR1='Xu, Radziszowski, An improvement to Mathon\'s cyclotomic Ramsey colorings, EJC 16 (2009) #N1 (local build_G1_G2/downloads/v16i1n1.pdf sha256 c309cc580402f9db9544559c6859497753336e525b0794913f2bf388b48de23b)',
    XSR2='Xu, Shao, Radziszowski, More constructive lower bounds on classical Ramsey numbers, SIAM J. Discrete Math. 25 (2011) 394-400; preprint https://www.cs.rit.edu/~spr/PUBL/paper68.pdf (local build_G3/downloads/xsr2/paper68.pdf sha256 98726fd291b07cf46e6e39b38932b20405bb59441b7d6ad4a5348e6f2a302dcd)',
    WSLX2='Wu, Su, Luo, Xu, EJC 17 (2010) #N25 (local hunt_two_colour/downloads/wslx2/WSLX2_v17i1n25.pdf sha256 8fad308ee534abe756ab70c5e36ac0d1686d40daf8d0f7e1afe85344cb7d1b68)',
    LuSL='Luo, Su, Li, Australas. J. Combin. 25 (2002) 103-116 (local hunt_two_colour/downloads/papers/LuSL_ajc_v25_p103.pdf sha256 54d4d1ac0f251c54d63038628e12da23af0b2b83a477c2e548e27cd0510ee2f6)',
    ExP='Exoo, Largest Paley Graphs with Small Clique Numbers, https://cs.indstate.edu/ge/Paley/ramsey.html (local <cloud>/ramsey-work/downloads/papers/exoo_site/Paley/ramsey.html sha256 3bbd44c52bc97443f6b1dcde07a515bcdeaa41fe075dcfb351b27a3f7bdd8fa7, unchanged since 3 Nov per hunt_two_colour)',
)


def inp(cell):
    b = builds.get(cell, {})
    return '; '.join('%s %s sha256 %s' % (i.get('name'), i.get('file', ''), i.get('sha256', i.get('source', ''))) for i in b.get('inputs', []))


ROWS = []


def row(cell, colours, sl, outcome, source, evidence, notes, key=None, file=None, sha=None, n=None):
    b = builds.get(key or cell, {})
    ROWS.append(dict(cell=cell, colours=colours, survey_lower=sl, outcome=outcome,
                     vertices=n if n is not None else b.get('N', ''),
                     file=file if file is not None else ('build_round2/' + b['file'] if b.get('file') else ''),
                     sha256=sha if sha is not None else b.get('sha256', '') or '',
                     source=source, evidence=evidence, notes=notes))


exec(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'rows.py')).read())

with open(os.path.join(OUT, 'results.csv'), 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=['cell', 'colours', 'survey_lower', 'outcome', 'vertices', 'file', 'sha256', 'source', 'evidence', 'notes'])
    w.writeheader(); [w.writerow(r) for r in ROWS]
with open(os.path.join(OUT, 'sources.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['cell', 'role', 'citation', 'doi_or_url', 'accessed', 'local_copy', 'sha256', 'size_bytes', 'licence', 'contains', 'route'])
    for r in SOURCES: w.writerow(r)
print(len(ROWS), 'rows;', len(SOURCES), 'sources')
from collections import Counter
print(Counter(r['outcome'] for r in ROWS))
