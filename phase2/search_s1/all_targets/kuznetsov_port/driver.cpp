// Driver for Kuznetsov's ramsey_df (commit f5c81c7): calls his public entry points with command-line parameters.
// usage: kuz ladder k0 k1 dim start mc minlog | kuz resume k0 k1 start minlog | kuz network k0 k1 ml minlog passes [fwd]
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <vector>
#include <string>
#include <omp.h>
#define TBB_PREVIEW_GLOBAL_CONTROL 1
#include <tbb/global_control.h>
#include "src/bigint.h"
typedef ext_bigint<GRAPH_MAX_LEN> bigint_t;
extern omp_lock_t op_count_lock;
extern int g_kmax[2];
void init_phi(); int cpu_init();
void cyclic_ladder_search(int dim, int k0, int k1, int start_size, int mc_test_count, int min_log_len);
void cyclic_ladder_search(int k0, int k1, int start_length, std::vector<bigint_t>& init_sym, int min_log_len);
void cyclic_network_search(int k0, int k1, int d, bool fwd_only, int min_log, int max_passes);
void readsym(std::string s, std::vector<bigint_t>& v, int target);
std::string format_sym_name(std::string prefix);
int main(int argc, char** argv){
  int th = getenv("KUZ_THREADS") ? atoi(getenv("KUZ_THREADS")) : 1;
  tbb::global_control gc(tbb::global_control::max_allowed_parallelism, th);
  omp_set_num_threads(th);
  if(getenv("KUZ_SEED")) srand(atoi(getenv("KUZ_SEED")));
  omp_init_lock(&op_count_lock); init_phi(); cpu_init();
  if(argc<2) return 2;
  if(!strcmp(argv[1],"ladder")) cyclic_ladder_search(atoi(argv[4]),atoi(argv[2]),atoi(argv[3]),atoi(argv[5]),atoi(argv[6]),atoi(argv[7]));
  else if(!strcmp(argv[1],"resume")){ g_kmax[0]=atoi(argv[2]); g_kmax[1]=atoi(argv[3]); std::vector<bigint_t> v; readsym(format_sym_name(""), v, atoi(argv[4]));
     printf("resume: %zu sym graphs\n", v.size()); cyclic_ladder_search(atoi(argv[2]),atoi(argv[3]),atoi(argv[4]),v,atoi(argv[5])); }
  else if(!strcmp(argv[1],"network")) cyclic_network_search(atoi(argv[2]),atoi(argv[3]),atoi(argv[4]), argc>7, atoi(argv[5]), atoi(argv[6]));
  else return 2;
  return 0;
}
