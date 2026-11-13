"""Extract Rowley arXiv:2203.13476 ancillary columns: colour of edge-length d for each graph column."""
import csv, sys, json
R=list(csv.reader(open(sys.argv[1])))
g=lambda i,j: R[i][j] if j<len(R[i]) else ''
hdr={}
for i in range(20):
    if g(i,2).strip(): hdr[g(i,2).strip()]=i
r1=[i for i in range(len(R)) if g(i,1)=='1'][0]
out={}
for j in range(3,28,2):
    vals=[]; d=1
    while r1+d-1<len(R) and g(r1+d-1,j).strip()!='':
        vals.append(int(float(g(r1+d-1,j)))); d+=1
    info={k:g(i,j) for k,i in hdr.items()}
    out[j]=dict(info=info,col=vals)
json.dump(out,open(sys.argv[2],'w'))
for j,o in out.items(): print(j,o['info'],len(o['col']),sorted(set(o['col'])))
