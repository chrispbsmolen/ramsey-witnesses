"""Parse an ODS content.xml into one CSV per sheet (handles repeated rows/cols)."""
import sys, csv, os
import xml.etree.ElementTree as ET
NS={'table':'urn:oasis:names:tc:opendocument:xmlns:table:1.0','text':'urn:oasis:names:tc:opendocument:xmlns:text:1.0','office':'urn:oasis:names:tc:opendocument:xmlns:office:1.0'}
T='{%s}'%NS['table']; X='{%s}'%NS['text']; O='{%s}'%NS['office']
src,out=sys.argv[1],sys.argv[2]; os.makedirs(out,exist_ok=True)
root=ET.parse(src).getroot()
for tab in root.iter(T+'table'):
    name=tab.get(T+'name'); rows=[]
    for r in tab.iter(T+'table-row'):
        rr=int(r.get(T+'number-rows-repeated','1'))
        cells=[]
        for c in r:
            if c.tag not in (T+'table-cell',T+'covered-table-cell'): continue
            cr=int(c.get(T+'number-columns-repeated','1'))
            v=c.get(O+'value')
            if v is None: v=' '.join(''.join(p.itertext()) for p in c.findall(X+'p'))
            cells += [v]*min(cr,5000)
        while cells and cells[-1]=='': cells.pop()
        for _ in range(min(rr,1 if not cells else rr)): rows.append(cells)
    while rows and not rows[-1]: rows.pop()
    with open(os.path.join(out,name+'.csv'),'w',newline='') as f: csv.writer(f).writerows(rows)
    print(name,len(rows),max((len(r) for r in rows),default=0))
