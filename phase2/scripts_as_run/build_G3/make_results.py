"""Write results.csv from built/manifest.json and the decisions recorded below (python3 make_results.py)."""
import csv, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(open(os.path.join(HERE, 'built', 'manifest.json')))
XXER = 'XXER: Xu, Xie, Exoo, Radziszowski, EJC 11 (2004) #R35, Thm 9 pp.15-16 (construction of Thm 7 p.11); downloads/xxer/XXER_v11i1r35.pdf sha256 a267b818...'
XSR2 = 'XSR2: Xu, Shao, Radziszowski, SIAM J. DM 25 (2011) 394-400; preprint https://www.cs.rit.edu/~spr/PUBL/paper68.pdf (sha256 98726fd2...), Thm 3 pp.4-6, Cor 3 p.6, Thm 4 pp.6-7'
SURV = 'survey DS1 rev18 '
rows = [
 ('7,11', 405, 'VERIFIED', SURV + 'Table Ia [XXER]; ' + XXER + ' (lists R(7,11)>=405 p.16)',
  'input Paley Q101 (repo constructions/paley101_R6_6.g6, VERIFIED); built graph = complement of Thm 9 graph; vertex transitivity proved (4 explicit automorphisms, orbit of 0 = all); no K7: repo NONE 0.0 s, nx NONE 0.4 s; no I11: repo NONE 6.0 s, nx NONE 431 s (both through vertex 0); 2nd implementation identical',
  'first G3 cell fully checked'),
 ('5,15', 275, 'PENDING_MAC', SURV + 'Table Ia/IIa [2.3.h], item 2.3.h p.12 (k-2 term [XSR2]); ' + XSR2 + ' Cor 3: R(5,15) >= R(5,14)+8',
  'input Kuznetsov (5,14;266) circulant (VERIFIED); no K5: repo NONE, nx NONE; no I15: repo NONE 52.7 s (direct, full graph); nx direct not finished in 570 s; exact reduction alpha(F) <= alpha(G)+1 (decomp.py: all independent T in X have |T|<=2, every pair implied) with nx PASS on the input (111.8 s)',
  'Mac job: nx indep direct. Becomes VERIFIED when it passes (or if the reduction is accepted)'),
 ('7,12', 417, 'PENDING_MAC', SURV + 'Table Ia [XSR2]; ' + XSR2 + ': R(7,12) >= R(7,11)+12',
  'input = built (7,11;404) graph above (VERIFIED here); no K7: repo NONE 0.1 s, nx NONE 12.6 s; no I12: direct not finished in 60 s (estimate ~2e4 s); exact reduction alpha(F) <= alpha(G)+1 = 11 (decomp.py), alpha(G) <= 10 checked by both checkers',
  'Mac jobs: repo and nx indep direct'),
 ('9,10', 581, 'PENDING_MAC', SURV + 'Table Ia [XSR2]; ' + XSR2 + ': R(9,10) >= R(9,9)+16',
  'input Mathon doubling of Q281 (repo constructions/mathon281_R9_9.g6, VERIFIED by verify_ramsey only, ledger run cloud_constructions); no K9: repo NONE 22.1 s; no I10: repo NONE 175.3 s (direct); nx both halves not run here; exact reduction alpha(F) <= alpha(G)+1 also holds',
  'Mac jobs: nx clique and indep'),
 ('8,11', 457, 'PENDING_MAC', SURV + 'Table Ia [2.3.i], item 2.3.i p.12; ' + XXER + ': R(11,8) >= 4R(6,7)-3',
  'input Exoo-Tatarevic g67.114 (VERIFIED); no K8: repo NONE 0.4 s, nx NONE 49.8 s; no I11: not finished in 60 s (estimate ~1.3e3 s)',
  'Mac jobs: repo and nx indep'),
 ('7,16', 629, 'PENDING_MAC', SURV + 'Table IIa [2.3.i]; ' + XXER + ': R(7,16) >= 4R(4,15)-3 with R(4,15)>=158 (IIa value, Tat)',
  'input Tatarevic g415.157 (ledger PASS); no K7: repo NONE 12.6 s; nx not finished in 280 s; no I16: estimate ~7e3 s; structural: alpha(T9(G)) <= alpha(G)+1',
  'Mac jobs: nx clique, repo and nx indep'),
 ('5,21', 441, 'PARTIAL', SURV + 'Table IIa [2.3.i]; item 2.3.i: R(5,l) >= 4R(3,l-1)-3; ' + XXER + ' (14) p.16',
  'input Exoo r3.20.110 (VERIFIED); no K5: repo NONE 0.1 s, nx NONE 2.4 s; no I21: estimate > 1e8 s (beyond kill criterion); structural: alpha(T9(G)) <= alpha(G)+1 = 20',
  'independence half not checkable by search; rests on Thm 9 proof + verified input'),
 ('7,17', 729, 'PARTIAL', SURV + 'Table IIa [2.3.i]; ' + XXER + ': R(17,7) >= 4R(9,6)-3',
  'input Kuznetsov (6,9;182) circulant (VERIFIED); vertex transitive (proved); no K7: repo NONE 0.1 s, nx NONE 0.4 s; no I17 (= no K17 in Thm 9 graph): repo not finished in 560 s, estimate > 1e9 s',
  'independence half rests on Thm 9 proof (omega <= 2(k-1)) + verified input'),
 ('8,17', 1005, 'PARTIAL', SURV + 'Table IIa [2.3.i]; ' + XXER + ': R(17,8) >= 4R(9,7)-3',
  'input Kuznetsov (7,9;251) circulant (VERIFIED); vertex transitive (proved); no K8: repo NONE 0.2 s, nx NONE 5.0 s; no I17: estimate > 1e11 s',
  'as 7,17'),
 ('8,21', 1617, 'PARTIAL', SURV + 'Table IIa [2.3.i]; ' + XXER + ' applied twice: R(21,8) >= 4R(11,7)-3, R(11,7) >= 405',
  'input = built (7,11;404) graph (VERIFIED here); vertex transitive (proved, 7 generators); no K8: repo NONE 0.3 s, nx NONE 5.6 s; no I21: not finished in 60 s, far beyond limits',
  'as 7,17'),
 ('8,13', 817, 'PARTIAL', SURV + 'Table Ia [XXER]; ' + XXER + ' (lists R(8,13)>=817 p.16): R(13,8) >= 4R(7,7)-3',
  'input Mathon doubling of Q101 (repo constructions/mathon101_R7_7.g6, VERIFIED; nx recheck here PASS both halves); no K8: repo NONE 7.7 s; nx not finished in 280 s; no I13: estimate > 1e10 s',
  'Mac job: nx clique. Independence half rests on Thm 9 proof'),
 ('8,15', 873, 'PARTIAL', SURV + 'Table IIa [2.3.i]; ' + XXER + ': R(15,8) >= 4R(8,7)-3',
  'input Tatarevic g78.218 (VERIFIED); no K8: repo NONE 8.8 s; no I15: estimate > 1e12 s',
  'Mac job: nx clique. Independence half rests on Thm 9 proof'),
 ('8,19', 1237, 'PARTIAL', SURV + 'Table IIa [2.2.h], item 2.2.h pp.11-12; 2.3.h p.12; ' + XSR2 + ' Thm 3 (and Thm 4 for R(7,8) >= 217)',
  'G = built (8,13;816), H = complement of built XSR2 (7,8;216) graph (VERIFIED here, both checkers both halves), M = complement of Mathon(204) induced on vertices 0..203 of both (checked); no K8: repo NONE 34.2 s; no I19: far beyond limits',
  'Mac job: nx clique. H on 216 vertices is our reading of "properly chosen H" in 2.2.h (the survey does not name it)'),
 ('10,15', 1313, 'PARTIAL', SURV + 'Table Ia [2.3.i]; ' + XXER + ': R(15,10) >= 4R(8,9)-3',
  'input NOT in repo verified tier: (8,9;328) circulant decoded here from Kuznetsov arXiv:1505.07186 source review.py lines 771-772 (local copy sha256 8b39c23a...), PASS both halves with both checkers (repo 0.1 s, nx 3.8 s, circulant); vertex transitive (proved); no K10: repo NONE 2.4 s; nx not finished in 280 s; no I15: estimate > 1e8 s',
  'unblocked by the R(8,9) decoding; that input to be accepted (it also closes the (8,9) NO_FILE_FOUND cell)'),
 ('6,15', 401, 'STILL_NO_FILE', SURV + 'Table Ia/IIa [2.3.i]; ' + XXER + ': R(15,6) >= 4R(8,5)-3, needs R(5,8) >= 101',
  'BLOCKED: no (5,8;100)-graph (coverage NO_FILE_FOUND, survey ref HaKr1)', 'buildable in seconds once a (5,8;100) witness is found'),
 ('7,18', 797, 'STILL_NO_FILE', SURV + 'Table IIa [2.3.i]; ' + XXER + ': R(7,18) >= 4R(4,17)-3, needs R(4,17) >= 200',
  'BLOCKED: no (4,17;199)-graph (coverage NO_FILE_FOUND, survey ref LiaWXS, unpublished)', 'buildable once a (4,17;199) witness is found'),
 ('5,23', 521, 'STILL_NO_FILE', SURV + 'Table IIa [2.3.i]; ' + XXER + ' (14): R(5,23) >= 4R(3,22)-3, needs R(3,22) >= 131',
  'BLOCKED: no (3,22;130)-graph (coverage NO_FILE_FOUND, survey ref WSLX2)', 'buildable once a (3,22;130) witness is found'),
 ('5,18', 396, 'STILL_NO_FILE', SURV + 'Table IIa [2.3.h]; ' + XSR2 + ' Cor 3: R(5,18) >= R(5,17)+8, needs R(5,17) >= 388 (XSR2 Thm 5: G387 = one colour of the tripling construction, p = 127, of XuR1 = Xu-Radziszowski EJC 16 (2009) N1)',
  'BLOCKED: no (5,17;387)-graph on file (coverage NO_FILE_FOUND); G387 is itself a recipe (XuR1, not fetched here)', 'G1 builds XuR1 for R(7,7,7); if it also yields G387 this cell follows from Cor 3'),
 ('6,21', 888, 'STILL_NO_FILE', SURV + 'Table IIa [2.3.h]; ' + XSR2 + ' Cor 3: R(6,21) >= R(6,20)+10, needs R(6,20) >= 878 (SLLL, cubic residues, Discrete Math 250 (2002) 197-209)',
  'BLOCKED: no (6,20;877)-graph (coverage NO_FILE_FOUND); SLLL paper not fetched', 'buildable once a (6,20;877) witness is found or SLLL is reproduced'),
]
with open(os.path.join(HERE, 'results.csv'), 'w', newline='') as f:
    w = csv.writer(f)
    w.writerow(['cell', 'colours', 'survey_lower', 'outcome', 'vertices', 'file', 'sha256', 'source', 'evidence', 'notes'])
    for cell, L, out, src, ev, notes in rows:
        m = M.get(cell)
        w.writerow([cell, 2, L, out, m['n'] if m else '', ('build_G3/' + m['file']) if m else '', m['sha256_file'] if m else '', src, ev, notes])
        if m: assert m['n'] == L - 1, cell
print('rows', len(rows))
