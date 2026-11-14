/* gen0.c: does a graph contain a clique of size K?  Second checker for build_round2, written as the
   search() of round 1's linear0.c (hunt_multicolour/mac_jobs/linear0.c, independent of repo/clique.c)
   with a plain graph reader instead of the linear-colouring reader.  No symmetry is used here: the caller
   passes the subgraph it wants searched (for a vertex-transitive colouring, the neighbourhood of vertex 0
   in one colour, with K = k-1).
   Input (stdin): n, then n lines of n characters '0'/'1' (symmetric, zero diagonal; checked).
   Usage: gen0 K [MAXV]   (MAXV: stop after MAXV start vertices, for timing tests)
   Output: FOUND / NONE / PARTIAL_NONE plus timing.  Build: cc -O2 -o gen0_r2 gen0.c */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
typedef uint64_t W;
static int m, nw; static W *adj;
#define ROW(i) (adj + (size_t)(i) * nw)
static int popc(const W *a){int s=0;for(int i=0;i<nw;i++)s+=__builtin_popcountll(a[i]);return s;}
static int search(W *P, int need){
    if(need==0) return 1;
    int cnt=popc(P); if(cnt<need) return 0;
    if(need==1) return cnt>0;
    int *ord=malloc(sizeof(int)*cnt), *col=malloc(sizeof(int)*cnt); int k=0, colour=0;
    W *U=malloc(sizeof(W)*nw), *Q=malloc(sizeof(W)*nw), *NP=malloc(sizeof(W)*nw);
    for(int i=0;i<nw;i++)U[i]=P[i];
    while(k<cnt){ colour++; for(int i=0;i<nw;i++)Q[i]=U[i];
        for(int wi=0;wi<nw;wi++) while(Q[wi]){ int b=__builtin_ctzll(Q[wi]); int v=wi*64+b;
            Q[wi]&=~((W)1<<b); U[wi]&=~((W)1<<b); W *r=ROW(v); for(int j=0;j<nw;j++)Q[j]&=~r[j];
            ord[k]=v; col[k]=colour; k++; } }
    int found=0;
    for(int idx=cnt-1; idx>=0 && !found; idx--){
        if(col[idx]<need) break;
        int v=ord[idx]; W *r=ROW(v); for(int j=0;j<nw;j++)NP[j]=P[j]&r[j];
        if(search(NP,need-1)) found=1;
        P[v/64]&=~((W)1<<(v%64));
    }
    free(ord);free(col);free(U);free(Q);free(NP); return found;
}
int main(int argc,char**argv){
    if(argc<2){fprintf(stderr,"usage: gen0 K [MAXV]\n");return 2;}
    int K=atoi(argv[1]); long maxv=argc>2?atol(argv[2]):-1;
    if(scanf("%d",&m)!=1)return 2;
    nw=(m+63)/64; adj=calloc((size_t)m*nw,sizeof(W));
    char *line=malloc(m+2);
    for(int a=0;a<m;a++){ if(scanf("%s",line)!=1){fprintf(stderr,"short input\n");return 2;}
        for(int b=0;b<m;b++) if(line[b]=='1'){ if(a==b){printf("ERROR loop %d\n",a);return 3;} ROW(a)[b/64]|=(W)1<<(b%64);} }
    for(int a=0;a<m;a++) for(int b=0;b<m;b++) if(((ROW(a)[b/64]>>(b%64))&1)!=((ROW(b)[a/64]>>(a%64))&1)){printf("ERROR asymmetric %d %d\n",a,b);return 3;}
    clock_t t0=clock(); int found=0; long done=0;
    W *P=malloc(sizeof(W)*nw);
    if(K<=1){ found = (K<=0) || m>0; done=m; }
    else for(int v=0; v<m && !found; v++){
        if(maxv>=0 && done>=maxv) break;
        W *r=ROW(v); for(int j=0;j<nw;j++)P[j]=r[j];
        for(int j=0;j<=v/64 && j<nw;j++){ if(j<v/64)P[j]=0; else P[j]&=~(((W)2<<(v%64))-1); }
        if(search(P,K-1)) found=1; done++;
    }
    double t=(double)(clock()-t0)/CLOCKS_PER_SEC;
    printf("%s n=%d K=%d start_vertices_done=%ld/%d seconds=%.1f\n", found?"FOUND":(done==m?"NONE":"PARTIAL_NONE"), m,K,done,m,t);
    return 0;
}
