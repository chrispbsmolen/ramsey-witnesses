/* edgesa.c - search S1: simulated annealing on a whole (unsymmetric) edge colouring of K_n.
 * Cost = sum over colours c of the number of monochromatic K_{k_c} in colour c (exact).  Move: recolour one edge;
 * the cost change is exact: cliques lost = K_{k-2} inside the common c1-neighbourhood of the edge's ends, cliques
 * gained = K_{k-2} inside the common c2-neighbourhood.  Edge choice: with probability pf an edge of a violating
 * clique (found by a search from a random vertex), otherwise a random edge.  Metropolis at fixed T, reload best
 * after R seconds without improvement.
 * Start: colormat file (rows of colour digits; rows shorter than n are padded with random colours, so an m-vertex
 * colouring plus n-m new vertices is a valid start) or random.
 * usage: edgesa n K1,K2,.. seed secs T outprefix [-i start.colormat] [-f pf] [-r reload]
 * Writes outprefix.colormat (best colouring) and prints a JSON line.  Exit 0 at cost 0, else 3. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#define MAXN 256
#define MW 4
typedef uint64_t W;
static int n, r, ks[8], nw;
static W adj[8][MAXN][MW];
static unsigned char col[MAXN][MAXN];
static uint64_t rs = 88172645463325252ULL;
static inline uint64_t xr(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline long rndl(long m){ return (long)(((xr()>>32) * (uint64_t)m) >> 32); }
static inline double rndu(void){ return (xr()>>11) * (1.0/9007199254740992.0); }
static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+1e-9*ts.tv_nsec; }
static inline int popc(const W *a){ int s=0; for(int i=0;i<nw;i++) s+=__builtin_popcountll(a[i]); return s; }
static long cnt(int c, const W *P, int need){
  if(need==0) return 1;
  int pc=popc(P); if(pc<need) return 0;
  if(need==1) return pc;
  long tot=0; W Q[MW];
  for(int wi=0;wi<nw;wi++){ W x=P[wi]; while(x){ int b=__builtin_ctzll(x); x&=x-1; int u=wi*64+b;
      for(int j=0;j<nw;j++) Q[j]=0;
      for(int j=wi;j<nw;j++){ W m=P[j]&adj[c][u][j]; if(j==wi) m&=(b==63)?0:(~0ULL<<(b+1)); Q[j]=m; }
      tot+=cnt(c,Q,need-1); } }
  return tot;
}
static long edge_cliques(int c, int u, int v){ W P[MW]; for(int j=0;j<nw;j++) P[j]=adj[c][u][j]&adj[c][v][j]; return cnt(c,P,ks[c]-2); }
static void setc(int u, int v, int c){ int o=col[u][v];
  adj[o][u][v>>6]&=~(1ULL<<(v&63)); adj[o][v][u>>6]&=~(1ULL<<(u&63));
  adj[c][u][v>>6]|=1ULL<<(v&63); adj[c][v][u>>6]|=1ULL<<(u&63); col[u][v]=col[v][u]=c; }
static int stk[64];
static int findq(int c, const W *P, int need, int depth){
  if(need==0) return 1; if(popc(P)<need) return 0; W Q[MW];
  for(int wi=0;wi<nw;wi++){ W x=P[wi]; while(x){ int b=__builtin_ctzll(x); x&=x-1; int u=wi*64+b;
      for(int j=0;j<nw;j++) Q[j]=0;
      for(int j=wi;j<nw;j++){ W m=P[j]&adj[c][u][j]; if(j==wi) m&=(b==63)?0:(~0ULL<<(b+1)); Q[j]=m; }
      stk[depth]=u; if(findq(c,Q,need-1,depth+1)) return 1; } }
  return 0;
}
static int focus(int *eu, int *ev){
  int c0=rndl(r);
  for(int t=0;t<r;t++){ int c=(c0+t)%r; int v0=rndl(n);
    for(int s=0;s<n;s++){ int v=(v0+s)%n; W P[MW]; for(int j=0;j<nw;j++) P[j]=adj[c][v][j];
      /* cliques containing v: search all of N(v) (not only higher vertices) */
      stk[0]=v; if(findq(c,P,ks[c]-1,1)){ int k=ks[c]; int i=rndl(k), j=rndl(k-1); if(j>=i) j++; *eu=stk[i]; *ev=stk[j]; return 1; } } }
  return 0;
}
int main(int argc, char **argv){
  if(argc<7){ fprintf(stderr,"usage: edgesa n K1,K2,.. seed secs T outprefix [-i start] [-f pf] [-r reload]\n"); return 2; }
  n=atoi(argv[1]); r=0; for(char *p=strtok(argv[2],","); p; p=strtok(NULL,",")) ks[r++]=atoi(p);
  long seed=atol(argv[3]); double secs=atof(argv[4]), T=atof(argv[5]); char *out=argv[6];
  char *init=NULL; double pf=0.5, reload=60;
  for(int i=7;i<argc;i++){ if(!strcmp(argv[i],"-i")) init=argv[++i]; else if(!strcmp(argv[i],"-f")) pf=atof(argv[++i]); else if(!strcmp(argv[i],"-r")) reload=atof(argv[++i]); }
  nw=(n+63)/64; rs^=(uint64_t)seed*0x9E3779B97F4A7C15ULL; for(int i=0;i<20;i++) xr();
  memset(adj,0,sizeof adj);
  static unsigned char st[MAXN][MAXN]; int m=0;
  if(init){ FILE *f=fopen(init,"r"); if(!f){ perror("start"); return 2; } char line[1024];
    while(m<n && fgets(line,sizeof line,f)){ int L=strlen(line); while(L&&(line[L-1]=='\n'||line[L-1]=='\r')) line[--L]=0; if(!L) continue;
      for(int j=0;j<L && j<n;j++) st[m][j]=line[j]-'0'; m++; } fclose(f); }
  for(int u=0;u<n;u++) for(int v=u+1;v<n;v++){ int c = (u<m && v<m) ? st[u][v] : rndl(r); if(c<0||c>=r) c=rndl(r);
      col[u][v]=col[v][u]=c; adj[c][u][v>>6]|=1ULL<<(v&63); adj[c][v][u>>6]|=1ULL<<(u&63); }
  long cost=0; for(int c=0;c<r;c++){ for(int v=0;v<n;v++){ W P[MW]; for(int j=0;j<nw;j++) P[j]=adj[c][v][j]; for(int j=0;j<=v/64 && j<nw;j++){ if(j<v/64) P[j]=0; else P[j]&=(v%64==63)?0:(~0ULL<<(v%64+1)); } cost+=cnt(c,P,ks[c]-1); } }
  static unsigned char best[MAXN][MAXN]; memcpy(best,col,sizeof col); long bestc=cost, start=cost;
  double t0=now(), timp=t0; long moves=0, acc=0;
  while(bestc>0){
    if((moves&1023)==0){ double t=now(); if(t-t0>secs) break;
      if(reload>0 && t-timp>reload && cost>bestc){ for(int u=0;u<n;u++) for(int v=u+1;v<n;v++) if(col[u][v]!=best[u][v]) setc(u,v,best[u][v]); cost=bestc; timp=t; } }
    moves++;
    int u,v; if(!(rndu()<pf && focus(&u,&v))){ u=rndl(n); v=rndl(n-1); if(v>=u) v++; }
    int c1=col[u][v], c2=rndl(r-1); if(c2>=c1) c2++;
    long lost=edge_cliques(c1,u,v), gain=edge_cliques(c2,u,v); long d=gain-lost;
    if(d<=0 || rndu()<exp(-d/T)){ setc(u,v,c2); cost+=d; acc++; if(cost<bestc){ bestc=cost; memcpy(best,col,sizeof col); timp=now(); } }
  }
  char fn[1024]; snprintf(fn,sizeof fn,"%s.colormat",out); FILE *g=fopen(fn,"w");
  for(int u=0;u<n;u++){ for(int v=0;v<n;v++) fputc(u==v?'0':'0'+best[u][v],g); fputc('\n',g); } fclose(g);
  printf("{\"best_score\": %ld, \"start_cost\": %ld, \"final_cost\": %ld, \"moves\": %ld, \"accepted\": %ld, \"seconds\": %.1f}\n", bestc, start, cost, moves, acc, now()-t0);
  return bestc==0?0:3;
}
