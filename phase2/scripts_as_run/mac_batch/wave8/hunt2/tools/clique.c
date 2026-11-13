/* clique: decide whether a graph has a clique of size >= s (exact, bitset branch and bound
   with greedy-coloring upper bounds, after Tomita's MCQ/MCS).  Reads a graph as
       n
       <n lines of n characters, '0'/'1', symmetric, zero diagonal>
   from stdin.  Usage: clique s [--sym] [--complement]
     --complement : search the complement (independent sets of size >= s)
     --sym        : the graph is vertex transitive, so only cliques containing vertex 0 are
                    searched (valid because every clique can be mapped onto one through 0)
   Output: one line "FOUND <size> <vertices...>" (a clique of at least s vertices) or
   "NONE <s-1>" (no clique of s vertices exists; the search is exact).  The number of search
   nodes goes to stderr. */
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <stdint.h>
#include <alloca.h>

typedef uint64_t u64;
static int n, W;            /* vertices, words per bitset */
static u64 *adj;            /* n * W */
static int target;
static int best = 0;
static int *bestset, *cur;
static long long nodes = 0;

static inline int popc(u64 x) { return __builtin_popcountll(x); }
static inline int bs_count(const u64 *b) { int c = 0; for (int i = 0; i < W; i++) c += popc(b[i]); return c; }
static inline int bs_test(const u64 *b, int v) { return (b[v >> 6] >> (v & 63)) & 1; }
static inline void bs_clear(u64 *b, int v) { b[v >> 6] &= ~(1ULL << (v & 63)); }

/* greedy colouring of the candidate set P; returns vertices in order with colour numbers */
static void color_sort(const u64 *P, int *order, int *colors, int *cnt) {
    u64 *Q = alloca(W * sizeof(u64)), *Qc = alloca(W * sizeof(u64));
    memcpy(Q, P, W * sizeof(u64));
    int k = 0, col = 0;
    while (bs_count(Q)) {
        col++;
        memcpy(Qc, Q, W * sizeof(u64));
        while (1) {
            int v = -1;
            for (int i = 0; i < W; i++) if (Qc[i]) { v = i * 64 + __builtin_ctzll(Qc[i]); break; }
            if (v < 0) break;
            bs_clear(Qc, v); bs_clear(Q, v);
            for (int i = 0; i < W; i++) Qc[i] &= ~adj[(size_t)v * W + i];
            order[k] = v; colors[k] = col; k++;
        }
    }
    *cnt = k;
}

static int expand(u64 *P, int depth) {
    nodes++;
    int *order = malloc(n * sizeof(int)), *colors = malloc(n * sizeof(int)), cnt;
    color_sort(P, order, colors, &cnt);
    for (int i = cnt - 1; i >= 0; i--) {
        if (depth + colors[i] <= best) { free(order); free(colors); return 0; }   /* bound; best >= target-1 after init */
        int v = order[i];
        cur[depth] = v;
        u64 *NP = alloca(W * sizeof(u64));
        for (int j = 0; j < W; j++) NP[j] = P[j] & adj[(size_t)v * W + j];
        if (bs_count(NP) == 0) {
            if (depth + 1 > best) { best = depth + 1; memcpy(bestset, cur, (depth + 1) * sizeof(int)); if (best >= target) { free(order); free(colors); return 1; } }
        } else {
            if (expand(NP, depth + 1)) { free(order); free(colors); return 1; }
        }
        bs_clear(P, v);
    }
    free(order); free(colors);
    return 0;
}

int main(int argc, char **argv) {
    if (argc < 2) { fprintf(stderr, "usage: clique s [--sym] [--complement]\n"); return 2; }
    target = atoi(argv[1]);
    int sym = 0, comp = 0;
    for (int i = 2; i < argc; i++) { if (!strcmp(argv[i], "--sym")) sym = 1; if (!strcmp(argv[i], "--complement")) comp = 1; }
    if (scanf("%d", &n) != 1) return 2;
    W = (n + 63) / 64;
    adj = calloc((size_t)n * W, sizeof(u64));
    char *line = malloc(n + 2);
    for (int i = 0; i < n; i++) {
        if (scanf("%s", line) != 1) return 2;
        for (int j = 0; j < n; j++) {
            int e = line[j] == '1';
            if (comp) e = !e;
            if (i != j && e) adj[(size_t)i * W + (j >> 6)] |= 1ULL << (j & 63);
        }
    }
    /* symmetry check: adjacency must be symmetric */
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) if (bs_test(adj + (size_t)i * W, j) != bs_test(adj + (size_t)j * W, i)) { printf("ERROR asymmetric %d %d\n", i, j); return 3; }
    bestset = malloc(n * sizeof(int)); cur = malloc(n * sizeof(int));
    u64 *P = calloc(W, sizeof(u64));
    int depth0 = 0;
    if (sym) { cur[0] = 0; depth0 = 1; memcpy(P, adj, W * sizeof(u64)); }
    else for (int v = 0; v < n; v++) P[v >> 6] |= 1ULL << (v & 63);
    best = target - 1;               /* we only care whether a clique of size >= target exists */
    int found = (bs_count(P) == 0) ? (depth0 >= target) : expand(P, depth0);
    if (found || best >= target) {
        printf("FOUND %d", best);
        for (int i = 0; i < best; i++) printf(" %d", bestset[i]);
        printf("\n");
    } else {
        printf("NONE %d\n", target - 1);
    }
    fprintf(stderr, "nodes %lld\n", nodes);
    return 0;
}
