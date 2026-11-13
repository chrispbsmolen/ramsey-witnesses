/* Tabu search for a circulant (k,l)-graph on Z_n (n <= 128): symmetric distance set S.
   G = Cay(Z_n, S) must have no K_k; complement must have no K_l.
   cost = #K_k(G) through 0 + #K_l(complement) through 0, each capped.
   usage: circ_tabu n k l seed max_seconds  -> prints "FOUND n: d1,d2,..." (distances <= n/2) */
#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <string.h>
#include <time.h>
typedef unsigned __int128 bs;
static int n,K,L; static bs adjG[128], adjC[128];
static long cap=200000, cnt;
static int pc(bs x){return __builtin_popcountll((uint64_t)x)+__builtin_popcountll((uint64_t)(x>>64));}
static int lowbit(bs x){uint64_t lo=(uint64_t)x; if(lo) return __builtin_ctzll(lo); return 64+__builtin_ctzll((uint64_t)(x>>64));}
static void rec(bs *adj, bs cand, int need){
  if(cnt>=cap) return;
  if(need==0){cnt++;return;}
  if(pc(cand)<need) return;
  while(cand){ int v=lowbit(cand); cand&=~((bs)1<<v);
    if(need==1){cnt++; if(cnt>=cap) return; continue;}
    bs c2=cand&adj[v]; if(pc(c2)>=need-1) rec(adj,c2,need-1); if(cnt>=cap) return; }
}
static int S[128];
static void build(){ for(int i=0;i<n;i++){adjG[i]=0;adjC[i]=0;}
  for(int i=0;i<n;i++) for(int j=0;j<n;j++) if(i!=j){int d=(j-i+n)%n; if(d>n-d) d=n-d;
    if(S[d]) adjG[i]|=(bs)1<<j; else adjC[i]|=(bs)1<<j;} }
static long cost(){ build(); long c=0; cnt=0; rec(adjG,adjG[0],K-1); c+=cnt; cnt=0; rec(adjC,adjC[0],L-1); c+=cnt; return c; }
int main(int argc,char**argv){
  n=atoi(argv[1]);K=atoi(argv[2]);L=atoi(argv[3]); unsigned seed=atoi(argv[4]); double maxs=atof(argv[5]);
  srand(seed); int h=n/2; double dens=argc>6?atof(argv[6]):0.3;
  for(int d=1;d<=h;d++) S[d]=(rand()/(double)RAND_MAX)<dens;
  int tabu[128]={0}; long cur=cost(), best=cur; time_t t0=time(NULL); long it=0;
  while(difftime(time(NULL),t0)<maxs){
    it++; long bc=-1; int bd=-1, ties=0;
    for(int d=1;d<=h;d++){ S[d]^=1; long c=cost(); S[d]^=1;
      if(tabu[d]>it && !(c<best)) continue;
      if(bc<0||c<bc){bc=c;bd=d;ties=1;} else if(c==bc){ties++; if(rand()%ties==0) bd=d;} }
    if(bd<0){continue;}
    S[bd]^=1; cur=bc; tabu[bd]=it+3+rand()%(h/4+1);
    if(cur<best){best=cur; fprintf(stderr,"it %ld cost %ld t=%.0f\n",it,cur,difftime(time(NULL),t0));}
    if(cur==0){ printf("FOUND %d:",n); int first=1; for(int d=1;d<=h;d++) if(S[d]){printf(first?"%d":",%d",d);first=0;} printf("\n"); return 0;}
    if(it%2000==0){ for(int d=1;d<=h;d++) if(rand()%10==0) S[d]^=1; cur=cost(); }
  }
  printf("NOTFOUND best %ld\n",best); return 1;
}
