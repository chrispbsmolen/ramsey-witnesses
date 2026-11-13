/* linear0.c: exact check that a LINEAR colouring (colour of {i,j} = c[|i-j|]) of K_N has no
   monochromatic K_k in colour col.  By translation, any monochromatic clique can be shifted to
   contain vertex 0, so it suffices to look for a (k-1)-clique inside S = {d : c[d] == col},
   where d < e in S are adjacent iff c[e-d] == col.  Bitset branch and bound with a greedy
   colouring bound (Tomita-style).  Independent of repo/clique.c.
   Input: a '.lengths' file (line 1: N; then N-1 integers c[1..N-1]).
   Usage: linear0 FILE COL K [MAXV]   (MAXV: stop after MAXV start vertices, for timing tests)
   Output: FOUND / NONE plus timing.  Build: cc -O2 -o linear0 linear0.c */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <time.h>
typedef uint64_t W;
static int N, *c, *S, m, nw; static W *adj;
#define ROW(i) (adj + (size_t)(i) * nw)
static int popc(const W *a){int s=0;for(int i=0;i<nw;i++)s+=__builtin_popcountll(a[i]);return s;}
static int search(W *P, int need, int depth){
    if(need==0) return 1;
    int cnt=popc(P); if(cnt<need) return 0;
    if(need==1) return cnt>0;
    /* greedy colouring: order vertices with colour classes */
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
        if(search(NP,need-1,depth+1)) found=1;
        P[v/64]&=~((W)1<<(v%64));
    }
    free(ord);free(col);free(U);free(Q);free(NP); return found;
}
int main(int argc,char**argv){
    if(argc<4){fprintf(stderr,"usage: linear0 FILE COL K [MAXV]\n");return 2;}
    FILE*f=fopen(argv[1],"r"); int col=atoi(argv[2]), K=atoi(argv[3]); long maxv=argc>4?atol(argv[4]):-1;
    if(fscanf(f,"%d",&N)!=1)return 2; c=malloc(sizeof(int)*N);
    for(int d=1;d<N;d++) if(fscanf(f,"%d",&c[d])!=1){fprintf(stderr,"short file\n");return 2;}
    S=malloc(sizeof(int)*N); m=0; for(int d=1;d<N;d++) if(c[d]==col) S[m++]=d;
    nw=(m+63)/64; adj=calloc((size_t)m*nw,sizeof(W));
    for(int a=0;a<m;a++) for(int b=a+1;b<m;b++) if(c[S[b]-S[a]]==col){ ROW(a)[b/64]|=(W)1<<(b%64); ROW(b)[a/64]|=(W)1<<(a%64); }
    clock_t t0=clock(); int found=0; long done=0;
    /* (K-1)-clique in G[S]: iterate start vertex v, search (K-2)-clique among later neighbours */
    W *P=malloc(sizeof(W)*nw);
    for(int v=0; v<m && !found; v++){
        if(maxv>=0 && done>=maxv) break;
        W *r=ROW(v); for(int j=0;j<nw;j++)P[j]=r[j];
        for(int j=0;j<=v/64 && j<nw;j++){ if(j<v/64)P[j]=0; else P[j]&=~(((W)2<<(v%64))-1); }
        if(search(P,K-2,1)) found=1; done++;
    }
    double t=(double)(clock()-t0)/CLOCKS_PER_SEC;
    printf("%s N=%d colour=%d k=%d degree(0)=%d start_vertices_done=%ld/%d seconds=%.1f\n", found?"FOUND":(done==m?"NONE":"PARTIAL_NONE"), N,col,K,m,done,m,t);
    return 0;
}
