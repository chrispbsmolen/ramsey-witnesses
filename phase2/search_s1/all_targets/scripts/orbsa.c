/* orbsa.c - search S1: simulated annealing over colourings of K_n that are constant on the edge orbits of a group.
 * Cost = sum over colours c and vertex-orbit representatives v of the number of monochromatic K_{k_c} in colour c
 * that contain v (exact count; 0 means no forbidden clique anywhere, because every clique is moved by the group
 * onto one through a representative).  Move: recolour one orbit (random orbit, or an orbit of an edge of a
 * violating clique with probability pf).  Metropolis at fixed temperature T; reload best after R seconds without
 * improvement.  Cost of a move = recount of the two colours touched (exact, no approximation).
 *
 * Input (from mkorb.py): line 1 "n r norb nreps", line 2 "k_0 .. k_{r-1}", line 3 reps, then n*(n-1)/2 orbit ids
 * for pairs (a<b) in row order.
 * usage: orbsa INPUT seed secs T outprefix [-i statefile] [-f pf] [-r reload]
 * Writes outprefix.state (best colouring: one colour per orbit) at the end and when improving, and
 * outprefix.found at cost 0. Prints a JSON line with the best cost.
 */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <math.h>
#include <time.h>
#define MAXN 384
#define MW 6
typedef uint64_t W;
static int n, r, norb, nreps, ks[8], reps[MAXN];
static int *orbof;           /* n*n */
static int *oe_a, *oe_b, *ostart;  /* edges of each orbit */
static int *col, *bestcol;
static W adj[8][MAXN][MW];
static int nw;
static uint64_t rs = 88172645463325252ULL;
static inline uint64_t xr(void){ rs ^= rs<<13; rs ^= rs>>7; rs ^= rs<<17; return rs; }
static inline long rndl(long m){ return (long)(((xr()>>32) * (uint64_t)m) >> 32); }
static inline double rndu(void){ return (xr()>>11) * (1.0/9007199254740992.0); }
static double now(void){ struct timespec ts; clock_gettime(CLOCK_MONOTONIC,&ts); return ts.tv_sec+1e-9*ts.tv_nsec; }
static inline int popc(const W *a){ int s=0; for(int i=0;i<nw;i++) s+=__builtin_popcountll(a[i]); return s; }

/* number of cliques of size `need` inside P using vertices in increasing order */
static long cnt(int c, W *P, int need, long cap){
  if(need==0) return 1;
  int pc = popc(P); if(pc<need) return 0;
  if(need==1) return pc;
  long tot=0; W Q[MW];
  for(int wi=0; wi<nw; wi++){ W x=P[wi]; while(x){ int b=__builtin_ctzll(x); x&=x-1; int u=wi*64+b;
      /* candidates after u */
      for(int j=0;j<nw;j++) Q[j]=0;
      for(int j=wi;j<nw;j++){ W m=P[j]&adj[c][u][j]; if(j==wi) m &= (b==63)?0:(~0ULL<<(b+1)); Q[j]=m; }
      tot += cnt(c,Q,need-1,cap-tot); if(tot>=cap) return tot; } }
  return tot;
}
static long colour_cost(int c){
  long t=0;
  for(int i=0;i<nreps;i++){ int v=reps[i]; W P[MW]; for(int j=0;j<nw;j++) P[j]=adj[c][v][j]; t+=cnt(c,P,ks[c]-1,1L<<40); }
  return t;
}
static void setorb(int o, int c){
  int old=col[o];
  for(int e=ostart[o]; e<ostart[o+1]; e++){ int a=oe_a[e], b=oe_b[e];
    adj[old][a][b>>6]&=~(1ULL<<(b&63)); adj[old][b][a>>6]&=~(1ULL<<(a&63));
    adj[c][a][b>>6]|=1ULL<<(b&63); adj[c][b][a>>6]|=1ULL<<(a&63); }
  col[o]=c;
}
/* find one violating clique through a rep (random rep order) and return one of its orbits, or -1 */
static int stk[64];
static int findq(int c, W *P, int need, int depth){
  if(need==0) return 1;
  if(popc(P)<need) return 0;
  W Q[MW];
  for(int wi=0; wi<nw; wi++){ W x=P[wi]; while(x){ int b=__builtin_ctzll(x); x&=x-1; int u=wi*64+b;
      for(int j=0;j<nw;j++) Q[j]=0;
      for(int j=wi;j<nw;j++){ W m=P[j]&adj[c][u][j]; if(j==wi) m &= (b==63)?0:(~0ULL<<(b+1)); Q[j]=m; }
      stk[depth]=u; if(findq(c,Q,need-1,depth+1)) return 1; } }
  return 0;
}
static int focus_orbit(void){
  int c0=rndl(r);
  for(int t=0;t<r;t++){ int c=(c0+t)%r; int i0=rndl(nreps);
    for(int s=0;s<nreps;s++){ int v=reps[(i0+s)%nreps]; W P[MW]; for(int j=0;j<nw;j++) P[j]=adj[c][v][j];
      stk[0]=v; if(findq(c,P,ks[c]-1,1)){ int k=ks[c]; int i=rndl(k), j=rndl(k-1); if(j>=i) j++;
          int a=stk[i], b=stk[j]; return orbof[a*n+b]; } } }
  return -1;
}
int main(int argc, char **argv){
  if(argc<6){ fprintf(stderr,"usage: orbsa INPUT seed secs T outprefix [-i state] [-f pf] [-r reload]\n"); return 2; }
  FILE *f=fopen(argv[1],"r"); if(!f){ perror("input"); return 2; }
  long seed=atol(argv[2]); double secs=atof(argv[3]), T=atof(argv[4]); char *out=argv[5];
  char *init=NULL; double pf=0.3, reload=60;
  for(int i=6;i<argc;i++){ if(!strcmp(argv[i],"-i")) init=argv[++i]; else if(!strcmp(argv[i],"-f")) pf=atof(argv[++i]); else if(!strcmp(argv[i],"-r")) reload=atof(argv[++i]); }
  if(fscanf(f,"%d %d %d %d",&n,&r,&norb,&nreps)!=4) return 2;
  for(int c=0;c<r;c++) if(fscanf(f,"%d",&ks[c])!=1) return 2;
  for(int i=0;i<nreps;i++) if(fscanf(f,"%d",&reps[i])!=1) return 2;
  nw=(n+63)/64; orbof=malloc(sizeof(int)*n*n);
  int *ocount=calloc(norb+1,sizeof(int));
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){ int o; if(fscanf(f,"%d",&o)!=1) return 2; orbof[a*n+b]=orbof[b*n+a]=o; ocount[o]++; }
  fclose(f);
  ostart=malloc(sizeof(int)*(norb+1)); ostart[0]=0; for(int o=0;o<norb;o++) ostart[o+1]=ostart[o]+ocount[o];
  int ne=ostart[norb]; oe_a=malloc(sizeof(int)*ne); oe_b=malloc(sizeof(int)*ne); int *fill=calloc(norb,sizeof(int));
  for(int a=0;a<n;a++) for(int b=a+1;b<n;b++){ int o=orbof[a*n+b]; int e=ostart[o]+fill[o]++; oe_a[e]=a; oe_b[e]=b; }
  rs ^= (uint64_t)seed*0x9E3779B97F4A7C15ULL; for(int i=0;i<20;i++) xr();
  col=malloc(sizeof(int)*norb); bestcol=malloc(sizeof(int)*norb);
  int *init_col=malloc(sizeof(int)*norb);
  if(init){ FILE *g=fopen(init,"r"); if(!g){ perror("state"); return 2; } for(int o=0;o<norb;o++) if(fscanf(g,"%d",&init_col[o])!=1) return 2; fclose(g); }
  else for(int o=0;o<norb;o++) init_col[o]=rndl(r);
  memset(adj,0,sizeof(adj));
  for(int o=0;o<norb;o++){ col[o]=init_col[o]; for(int e=ostart[o];e<ostart[o+1];e++){ int a=oe_a[e],b=oe_b[e]; int c=col[o];
      adj[c][a][b>>6]|=1ULL<<(b&63); adj[c][b][a>>6]|=1ULL<<(a&63);} }
  long cc[8]; long cost=0; for(int c=0;c<r;c++){ cc[c]=colour_cost(c); cost+=cc[c]; }
  long best=cost; memcpy(bestcol,col,sizeof(int)*norb);
  double t0=now(), tlast=t0, timp=t0; long moves=0, acc=0;
  char fn[1024];
  while(best>0){
    if((moves&255)==0){ double t=now(); if(t-t0>secs) break;
      if(reload>0 && t-timp>reload && cost>best){ for(int o=0;o<norb;o++) if(col[o]!=bestcol[o]) setorb(o,bestcol[o]);
        cost=0; for(int c=0;c<r;c++){ cc[c]=colour_cost(c); cost+=cc[c]; } timp=t; } }
    moves++;
    int o = (rndu()<pf) ? focus_orbit() : -1; if(o<0) o=rndl(norb);
    int c1=col[o], c2=rndl(r-1); if(c2>=c1) c2++;
    setorb(o,c2); long n1=colour_cost(c1), n2=colour_cost(c2);
    long nc=cost-cc[c1]-cc[c2]+n1+n2; long d=nc-cost;
    if(d<=0 || rndu()<exp(-d/T)){ cost=nc; cc[c1]=n1; cc[c2]=n2; acc++;
      if(cost<best){ best=cost; memcpy(bestcol,col,sizeof(int)*norb); timp=now(); } }
    else setorb(o,c1);
  }
  snprintf(fn,sizeof fn,"%s.state",out); FILE *g=fopen(fn,"w"); for(int o=0;o<norb;o++) fprintf(g,"%d\n",bestcol[o]); fclose(g);
  if(best==0){ snprintf(fn,sizeof fn,"%s.found",out); g=fopen(fn,"w"); for(int o=0;o<norb;o++) fprintf(g,"%d\n",bestcol[o]); fclose(g); }
  printf("{\"best_score\": %ld, \"final_cost\": %ld, \"moves\": %ld, \"accepted\": %ld, \"seconds\": %.1f}\n", best, cost, moves, acc, now()-t0);
  return best==0?0:3;
}
