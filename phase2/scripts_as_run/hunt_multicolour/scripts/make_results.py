import csv, hashlib, os
os.chdir('<cloud>/ramsey-p2/hunt_multicolour')
def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
R5 = ('Rowley arXiv:2203.13476v3 ancillary spreadsheet, sheet Paper_Sep_2022 (https://arxiv.org/src/2203.13476, tarball sha256 '
      '5041096a33d6898c116a35a102e521fb14fe872fb18c20ff7d30822ed4c396b2, 197073 B; anc/content.xml sha256 '
      'd2280f45c90d0d55d6f3ba11270e0755d7649553c5d81e7089c852bf6bb6d8c4, 6148236 B; licence arXiv non-exclusive distrib.)')
JC = ('Courties, github.com/JuloJC/multicolour-ramsey-numbers commit d9ca62fe0307bebf00e519103cb711e588b69a5f (6 Nov 2026), data CC0 1.0; ')
def ev(name, ks):
    return 'verify_ramsey.py colormat PASS (logs/verify_%s.json) + crosscheck_mc.py PASS (logs/crosscheck_%s.json); lowered-k negative control in logs/negative_controls.txt' % (name, name)
rows = []
def add(cell, col, low, outcome, n='', f='', src='', evid='', notes=''):
    h = sha(f) if f and os.path.exists(f) else ''
    rows.append(dict(cell=cell, colours=col, survey_lower=low, outcome=outcome, vertices=n, file=f, sha256=h, source=src, evidence=evid, notes=notes))
RC = 'RECIPE_CANDIDATE: '
add('5,5,5', 3, 454, 'VERIFIED', 453, 'converted/julojc_atom_R5_5_5_n453.colormat',
    JC + 'ingredients/atom_5_5_5_n453_firstrow.txt, 674 B, sha256 c159b60e4063df6e5f88da6f1c137ce3418f5921872f3ecb57fd89f5a7479981 (labelled there as Exoo\'s published colouring); identical to the first 453 vertices of the (5,5,5,3;1429) colouring in ' + R5 + ' column 27',
    ev('julojc_atom_R5_5_5_n453', '5,5,5') + '; also logs/verify_rowley5_sub_R5_5_5_n453.json',
    'Cyclic. Rowley 2203.13476 p.4 (NDSATT4.tex l.245) says his 977 template extends "a (5,5,5;453)-graph derived by Exoo"; Rowley AJC 81(2) p.250 calls it unpublished. Lengths 1..452 of column 27 use only colours 1-3, so vertices 0..452 induce it. Two independent public copies agree byte for byte after relabelling.')
add('6,6,6', 3, 1106, 'STILL_NO_FILE', notes=RC + 'Rowley AJC 81(2) (2021) p.250-251 Thm 3.2 + Fig.1: template (6,3;12) = lengths 1..11 colours 1 1 1 1 2 1 2 2 2 1 2 (template colour 2) composed with Kalbfleisch (6,6;101) = Paley(101) (repo constructions/witnesses/paley101_R6_6.g6) gives a cyclic (6,6,6;1105). Fully explicit; inputs public. Searched: AJC PDFs, Row5 spreadsheet, JuloJC atlas (no file).')
add('8,8,8', 3, 7174, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Sec.6 (NDSATT4.tex l.300): (3,7,7;673) [verified here, converted/rowley5_R3_7_7_n673] -> XXER Cor.5 quadrupling twice -> (9,8,8;10768) -> neighbourhood of a vertex in colour 1 (degree 9*d1+7*673+5 = 7173 needs d1 = 273) is an (8,8,8;7173). The spreadsheet (3,7,7;673) verified here has triangle-free degree 198 (gives 6498), so the recipe needs the 273-degree graph, which is not in the spreadsheet: not reproduced from the text with the public data. Needs XXER Cor.5 rule (EJC 11 #R35); 10768-vertex intermediate -> heavy check.')
add('9,9,9', 3, 15041, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Sec.6 (l.298): (3,8,8;940) [verified here] -> XXER Cor.5 quadrupling twice -> (9,9,9;15040). Heavy verification (Mac).')
add('10,10,10', 3, 23094, 'STILL_NO_FILE', notes='Rowley 2203.13476 Table 2 (NDSATT4_Table2_Orders.pdf, r=3,k=10: 23093) lists the order but neither the text nor the spreadsheet gives its construction or data. Searched: Row5 tex/tables/spreadsheet, Row3, JuloJC, web search.')
add('4,4,4,4', 4, 634, 'STILL_NO_FILE', notes=RC + 'XXER EJC 11 (2004) #R35 p.5 Thm 1 (Giraud) + Cor.1: cyclic (4,4,4;127) Hill-Irving cubic-residue colouring (repo constructions/witnesses/cubic3_127_R4_4_4.txt) -> cyclic (4,4,4,4;633) with D_i = {j+l(2n-1)} as printed. Also Rowley AJC 68(3) Cor.3.3. Exoo site still has only n=577.')
add('5,5,5,5', 4, 4073, 'STILL_NO_FILE', notes=RC + 'Rowley AJC 81(2) p.250-251 Thm 3.2: template (5,3;10) = 1 1 1 2 1 2 2 1 2 (Fig.1) composed with the (5,5,5;453) colouring verified here (cell 5,5,5) -> (5,5,5,5;4072). Fully explicit; inputs public.')
add('6,6,6,6', 4, 23502, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Table 1: (6,6,3;235) template (spreadsheet column 15, phi=100) composed (AJC 81(2) Thm 3.2) with Paley(101) -> crg(6,6,6,6;23501) = 234*100+1+100. Inputs public.')
add('7,7,7,7', 4, 94874, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Table 1: (7,7,3;472) template (column 19, phi=201) composed with a linear (7,7;202) Mathon-Shearer doubled Paley(101) -> 471*201+1+201 = 94873. Needs a linear ordering of the 202-vertex graph (Row2 Sec.6). Heavy check.')
add('8,8,8,8', 4, 182002, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Table 1: (8,8,3;650) template (column 21, phi=280) composed with Paley(281) -> 649*280+1+280 = 182001. Heavy check.')
add('9,9,9,9', 4, 719204, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Table 1: (9,9,3;1282) template (column 25, phi=561) composed with a linear (9,9;562) doubled Paley(281) -> 1281*561+1+561 = 719203. Heavy check.')
add('3,3,3,3,3', 5, 162, 'VERIFIED', 161, 'converted/exoo94_R3x5_n161.colormat',
    'Exoo, EJC 1 (1994) #R8 p.2, symmetric sum-free partition of [1,160] (printed sets 1..80); PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/v1i1r8/pdf, 92776 B, sha256 d56540f55003a94585f0f79ee338792ee6e850ea03de4ec77ebf854d91f35fb4; licence not stated in PDF',
    ev('exoo94_R3x5_n161', '3^5'), 'Converted by scripts/ex10_convert.py (mirror i -> 161-i as the paper states); partition covers [1,160], 0 sum-free violations; circulant colouring of K_161.')
add('4,4,4,4,4', 5, 4176, 'STILL_NO_FILE', notes=RC + 'Rowley AJC 68(3) (2017) p.388 Thm 3.1/Cor.3.2 (eqs 3.1-3.2): U=(4,4,4;127) cubic residues, V=(4,4;17) Paley(17): 2*127*17-127-17+1 = 4175. Inputs public (repo cubic3_127, Paley(17)).')
add('5,5,5,5,5', 5, 41626, 'PENDING_MAC', 44337, 'converted/julojc_R5x5_n44337.lengths',
    JC + 'records/R_5_5_5_5_5_n44337_firstrow.txt, 44337 B, sha256 993cff57a419667c6410cf2843e04dee58034c8b0dbfed8b99fa6cc518eb9a70',
    'Cyclic linear colouring. Colours 3,4,5: no K5 by mac_jobs/linear0.c and by repo/clique.c (--sym, streamed input) (logs/partial_julojc_R5x5_n44337.txt). Colours 1,2 not finished here (est. <=55 min and <=20 min on one core).',
    'Exceeds the survey value (44337 >= 41625). verify_ramsey.py cannot load n=44337 (n x n int64). Job spec: mac_jobs/MAC_JOB_R5x5_n44337.md. Also ' + RC + 'Rowley Table 1: (5,5,3;93) template (column 13) + (5,5,5;453).')
add('6,6,6,6,6', 5, 258506, 'STILL_NO_FILE', notes='Rowley 2203.13476 Table 1 lists crg(6,6,6,6,6;258505) "etc" from the (6,6,3;235) template, but the composition chain is not spelled out; the single composition with (6,6,6;1105) gives 234*1104+1+100 = 258437, so the stated order is not reproduced from the text by that reading. Searched: Row5 tex/tables/spreadsheet, JuloJC atlas.')
add('3,3,3,3,3,3', 6, 538, 'VERIFIED', 537, 'converted/fresw_R3x6_n537.colormat',
    'Fredricksen and Sweet, EJC 7 (2000) #R32 p.6, "Partition of 536 into 6 symmetric sumfree sets"; PDF https://www.combinatorics.org/ojs/index.php/eljc/article/download/v7i1r32/pdf, 132421 B, sha256 ae8541c564efd65785a0e1d2c778108d58fec4c060707d7c277dd7f3eecad259; licence not stated in PDF',
    ev('fresw_R3x6_n537', '3^6'), 'Converted by scripts/fresw_convert.py: printed smaller halves mirrored x -> 537-x, except the pair 179 (set 4) / 358 (set 1) which the paper prints in different sets (their special provision, cf. Rowley 2107.03560 l.116); covers [1,536], 0 sum-free violations. Linear, not circulant.')
add('4,4,4,4,4,4', 6, 32006, 'STILL_NO_FILE', notes=RC + 'Rowley AJC 68(3) Thm 3.1: U=V=(4,4,4;127): 2*127*127-254+1 = 32005. Inputs public.')
add('5,5,5,5,5,5', 6, 441606, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Table 1: (5,5,5,3;977) template (column 27, phi=452) composed with (5,5,5;453): 976*452+1+452 = 441605. Inputs public (both verified here). Heavy check.')
add('3,3,3,3,3,3,3', 7, 1698, 'VERIFIED', 1697, 'converted/rowley4_R3x7_n1697.colormat',
    'Rowley arXiv:2107.03560 ancillary Specimens_S_7____TFTs-4,5,6.xls, sheet "S(7) >= 1696" (https://arxiv.org/src/2107.03560, tarball sha256 5d6bf8e28360e4a3bea6c0dbc9c64b5113128c62745667124befab478b957525; xls 308224 B sha256 c50cf981c1c437557b261cb8a66e193ee2cf77a8a50b0ae70c986b1c1cbb6fbb; licence arXiv non-exclusive)',
    ev('rowley4_R3x7_n1697', '3^7'), 'Partition of [1,1696] into 7 sum-free sets, 0 violations, fully symmetric x <-> 1697-x; circulant colouring of K_1697 (scripts/rowley4_convert.py).')
add('4,4,4,4,4,4,4', 7, 160024, 'STILL_NO_FILE', notes=RC + 'Rowley AJC 68(3) Thm 3.1: U=(4,4,4,4;633) (Giraud from cubic 127) and V=(4,4,4;127): 2*633*127-633-127+1 = 160023. Heavy check.')
add('3,3,3,3,3,3,3,3', 8, 5288, 'STILL_NO_FILE', notes=RC + 'S(8) >= 33*S(5)+6 = 5286 (Rowley AJC 81(2) p.254; AgCP+ arXiv:2112.03175 Table 3) from the width-33 S-template printed in AgCP+ Table 5 (p.~20) and Exoo\'s S(5)=160 partition (verified here). Note: Helbert, arXiv:2607.15034 (Jul 2026) claims S(8) >= 5362 (i.e. R_8(3) >= 5364) via shifted S-templates; no data file; not checked.')
add('3,3,3,3,3,3,3,3,3', 9, 17805, 'STILL_NO_FILE', notes=RC + 'S(9) >= 111*S(5)+43 = 17803 (AgCP+ arXiv:2112.03175v2 Table 3, Thm 2.3) from the width-111 S-template printed in AgCP+ Table 6 and Exoo\'s S(5)=160 partition. AgCP+ v2 PDF sha256 0bef5716f171992d6b125cfea15551b4e065eecfb243cd7b3e73884cbe5ca703; no ancillary files, no data link in the PDF.')
add('3,3,4', 3, 30, 'VERIFIED', 29, 'converted/codish_fig3_R3_3_4_n29.colormat',
    'Codish, Frank, Itzhakov, Miller, arXiv:1510.08266 (Constraints 2016) p.7 Fig.3, a (4,3,3;29) colouring printed as a 29x29 matrix; PDF https://arxiv.org/pdf/1510.08266, sha256 98fed0c495bf5354ee3d1aa21f194be68afaea6a215246eb65276552db8504d4; licence arXiv non-exclusive',
    ev('codish_fig3_R3_3_4_n29', '3,3,4'), 'Matrix rebuilt from word coordinates (pdftotext -bbox) because the figure shares lines with body text; result is square, symmetric, zero diagonal. Not the cited source (Ka2, Kalbfleisch 1966) but a witness for the same bound.')
add('3,3,5', 3, 45, 'STILL_NO_FILE', notes='Cited Ex2 (Congr. Numer. 59, 1987) not online. Searched: Exoo site (RAMSEY, SmallRamsey: unchanged, no 3,3,5), XXER, Robertson math/9811117, JuloJC atlas, Lachy-Dauth repo, web search.')
add('3,3,7', 3, 85, 'STILL_NO_FILE', notes='Ex18 says "constructions available at cs.indstate.edu/ge/RAMSEY" but the page (unchanged since Apr 2024, sha256 9ee57eb4...) has only g337.78; guessed file names 404; Wayback could not be reached. Weaker: JuloJC atom (3,3,7) N=81.')
add('3,3,8', 3, 103, 'STILL_NO_FILE', notes='Ex18; not on Exoo site. Weaker: JuloJC bricks atom (3,3,8) N=100 (needs 102).')
add('3,4,4', 3, 55, 'STILL_NO_FILE', notes='KrLR (JCMCC 4, 1988) group-orbit colouring not online. Lachy-Dauth data/circ_344.json holds only K30/K40 control circulants.')
add('3,4,6', 3, 117, 'STILL_NO_FILE', notes='Ex17; not on Exoo site; not in JuloJC records or Row5 spreadsheet.')
add('3,5,5', 3, 139, 'VERIFIED', 139, 'converted/julojc_R3_5_5_n139.colormat',
    JC + 'records/R_3_5_5_n139_firstrow.txt, 139 B, sha256 223d2f4cef4a7be73b609e47cb738dd4ce83fdc6975bce31e4e784bd1c69b899',
    ev('julojc_R3_5_5_n139', '3,5,5'), 'Cyclic, 139 vertices: exceeds the survey value by one (any 138 of the vertices cover the cell). Not the cited source (Ex17). Unrefereed (Nov 2026).')
add('3,5,6', 3, 181, 'VERIFIED', 191, 'converted/julojc_R3_5_6_n191.colormat',
    JC + 'records/R_3_5_6_n191_firstrow.txt, 191 B, sha256 208878e0a2caa43c1de3e61ce0e1c6febf4f671e0a324bc860338ab7d70fda6b',
    ev('julojc_R3_5_6_n191', '3,5,6'), 'Cyclic, 191 vertices, exceeds the survey value (180 needed). Not the cited source (Ex17). Unrefereed.')
add('3,3,3,4', 4, 97, 'STILL_NO_FILE', notes='Ex17; Exoo site still has only g3334.92/ch3334.92 (n=92).')
add('3,3,4,4', 4, 174, 'VERIFIED', 173, 'converted/rowley2_R3_3_4_4_n173.colormat',
    'Rowley, AJC 78(1) (2020) p.6 Table 1, distance sets of a cyclic (3,3,4,4;173)-graph; PDF https://ajc.maths.uq.edu.au/pdf/78/ajc_v78_p001.pdf, 329982 B, sha256 f66933cdf7a11180c20d7f11dd17dc3e872f7f66c13fa2e2346d85699aa0e3bf; CC BY-ND 4.0',
    ev('rowley2_R3_3_4_4_n173', '3,3,4,4'), 'Distances 1..86 as printed, the rest by d -> 173-d (scripts/row2_convert.py). CC BY-ND: a converted file may count as a derivative; redistribution to be decided.')
add('3,3,3,5', 4, 162, 'NOT_REPRODUCED', notes='XXER EJC 11 #R35 p.2-3 states that merging colours 2 and 3 of Exoo\'s (3,3,3,3,3;161) colouring gives a (3,5,3,3;161) colouring. Not reproduced from the text: with the partition printed in Ex10 (verified here), merging any of the 10 colour pairs leaves a K5 in the merged colour (both checkers). XXER may have used another of Exoo\'s ~10,000 partitions (Ex10 p.2); no file of it found.')
add('3,4,5,5', 4, 729, 'VERIFIED', 728, 'converted/rowley5_R3_4_5_5_n728.colormat', R5 + ', column 5 ("for testing crg(3,4,5,5;728)")',
    ev('rowley5_R3_4_5_5_n728', '3,4,5,5'), 'Cyclic. Also JuloJC records/R_3_4_5_5_n769 (sha256 9a43e071...346c, CC0), 769 vertices, both checkers PASS (logs/*julojc_R3_4_5_5_n769*). Survey cites Row2, whose text gives only 693; the 728 colouring is in the Row5 spreadsheet (Table 1).')
add('3,5,5,5', 4, 1430, 'VERIFIED', 1429, 'converted/rowley5_R3_5_5_5_n1429.colormat', R5 + ', column 27 (5,5,5,3 template, first 1428 lengths)',
    ev('rowley5_R3_5_5_5_n1429', '3,5,5,5'), 'The column is a repetition test file; its first 1428 entries equal the template extended by phi=452 (lengths 978..1428 mirror 1..451), i.e. exactly the cyclic (5,5,5,3;1429) of Row5 l.247. Taking the prefix is a conversion, no construction step.')
add('3,6,6', 3, 338, 'VERIFIED', 337, 'converted/rowley5_R3_6_6_n337.colormat', R5 + ', column 17 (CYC 3,6,6, order 337)', ev('rowley5_R3_6_6_n337', '3,6,6'), 'Cyclic, given in full in the spreadsheet.')
add('3,7,7', 3, 674, 'VERIFIED', 673, 'converted/rowley5_R3_7_7_n673.colormat', R5 + ', column 19 (7,7,3 template, first 672 lengths)', ev('rowley5_R3_7_7_n673', '3,7,7'), 'Prefix of the test column = template + phi=201 extension, cyclic (Row5 l.247: cyclic (7,7,3;673)). Colour degrees here: 232 / 242 (K7-free colours) and 198 (triangle-free colour); Row5 Sec.6 (l.302) says its (3,7,7;673) has degree 273 in the triangle-free colour, so the graph used there is probably a different one (relevant for the R(8,8,8) recipe).')
add('3,8,8', 3, 941, 'VERIFIED', 940, 'converted/rowley5_R3_8_8_n940.colormat', R5 + ', column 23 (CYC 8,8,3, order 940)', ev('rowley5_R3_8_8_n940', '3,8,8'), 'Cyclic, given in full in the spreadsheet.')
add('3,9,9', 3, 1844, 'VERIFIED', 1843, 'converted/rowley5_R3_9_9_n1843.colormat', R5 + ', column 25 (9,9,3 template, first 1842 lengths)', ev('rowley5_R3_9_9_n1843', '3,9,9'), 'Prefix = template (1282) + phi=561 extension, cyclic. verify 14 s, crosscheck 110 s.')
add('3,10,10', 3, 2841, 'STILL_NO_FILE', notes='Listed in survey 6.1.f from Row5, but neither Row5 text, tables nor spreadsheet contain a (3,10,10) or (10,10,3) graph. Searched also JuloJC, web.')
add('8,8,9', 3, 10769, 'STILL_NO_FILE', notes=RC + 'Rowley 2203.13476 Sec.6 (l.300): (3,7,7;673) [verified here] -> XXER Cor.5 quadrupling twice -> (9,8,8;10768). Heavy check.')
add('6,6,6,6,6,6', 6, 4515702, 'STILL_NO_FILE', notes=RC + 'Rowley AJC 81(2) Table 1 row H&J (order 4515701) by repeated composition; chain only in table form. 4.5M vertices: exhaustive check out of reach here.')
# Step 0 (report only)
S0 = 'STEP0 (RECIPE cell, report only): '
add('7,7,7 [Step0]', 3, 3214, 'STILL_NO_FILE', notes=S0 + 'no public file found (Exoo site, McKay, google-research, Lachy-Dauth, JuloJC, Row5 spreadsheet: Row5 Table 2 has only a linear 3021). Stays RECIPE (XuR1).')
add('3,3,3,3 [Step0]', 4, 51, 'STILL_NO_FILE', notes=S0 + 'no file; Radziszowski CGTC 2025 slides (cs.rit.edu/~spr/COURSES/CCOMP/r3333.pdf) give history only. Stays RECIPE (Chung matrix, with the known typo).')
add('3,4,8 [Step0]', 3, 193, 'STILL_NO_FILE', notes=S0 + 'no file. JuloJC bricks list a (3,8,3) template m=73 and an Atlas row, not a witness file. Stays RECIPE (6.2.g).')
add('3,5,7 [Step0]', 3, 241, 'FOUND_ELSEWHERE_ALREADY', 266, 'converted/julojc_R3_5_7_n266.colormat',
    JC + 'records/R_3_5_7_n266_firstrow.txt, 266 B, sha256 4b710dff1c18a0c07308aa92150060ee2f08e2b2c03647c6dfbe7a948b613cbf',
    ev('julojc_R3_5_7_n266', '3,5,7'), S0 + 'public file appeared 6 Nov 2026 (cyclic, 266 vertices, exceeds the survey value). Per registration Step 0 this cell moves from build to file-hunt; light checks here both PASS (so it could be VERIFIED). Unrefereed.')
add('3,4,4,4 [Step0]', 4, 381, 'STILL_NO_FILE', notes=S0 + 'no file. Stays RECIPE (6.2.j).')
add('3,3,3,10 [Step0]', 4, 513, 'STILL_NO_FILE', notes=S0 + 'no file. Stays RECIPE (6.2.g).')
add('3,3,3,11 [Step0]', 4, 597, 'STILL_NO_FILE', notes=S0 + 'no file. Stays RECIPE (6.2.g).')
add('3,3,3,7 [Step0]', 4, 247, 'STILL_NO_FILE', notes=S0 + 'no file. Stays RECIPE (6.2.h).')
with open('results.csv', 'w', newline='') as f:
    w = csv.DictWriter(f, fieldnames=list(rows[0])); w.writeheader(); w.writerows(rows)
import collections
print(len(rows), collections.Counter(r['outcome'] for r in rows[:42]), collections.Counter(r['outcome'] for r in rows[42:]))
