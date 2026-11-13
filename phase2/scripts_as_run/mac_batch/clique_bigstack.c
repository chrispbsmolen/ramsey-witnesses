/* clique_bigstack.c: runs the UNCHANGED repo clique.c on a thread with a 1 GiB stack.

   Why: clique.c's expand() calls alloca() inside its candidate loop, so one stack frame holds one bitset per
   candidate tried.  For the 44,337-vertex R(5,5,5,5,5) colouring (693 words = 5,544 B per bitset) the top frame
   alone is 33.5 MB for colour 1 and 38.3 MB for colour 2 (6,336 / 7,241 loop iterations, replayed exactly; the
   spec's 80 / 70 MB assumed all 14,484 / 12,676 candidates), and deeper frames add more.  macOS caps the main
   thread's stack (ulimit -s) at 64 MB, too close to call, and the frame grows during the run, so a failure
   could come hours in.  A secondary thread can have a much larger stack (pthread_attr_setstacksize), mapped
   lazily, so only the pages actually used cost memory.

   clique.c is not edited: it is #included verbatim with its main() renamed by the preprocessor.  wave0.sh
   checks its SHA-256 (137a1002...9101) before building.  Input, arguments and output are exactly clique.c's.

   Extra, outside clique.c: if CLIQUE_TIME_LIMIT=<seconds> is set, the program prints
   "TIMEOUT time limit reached" and exits with code 4 when that much wall time has passed.

   Build:  cc -O2 -I <folder holding clique.c> -o clique_bigstack_mac clique_bigstack.c -lpthread        */
#define main clique_c_main
#include "clique.c"
#undef main
#include <pthread.h>
#include <signal.h>
#include <unistd.h>

#ifndef BIG_STACK_BYTES
#define BIG_STACK_BYTES ((size_t)1 << 30)
#endif

static int g_argc, g_rc;
static char **g_argv;

static void *runner(void *unused) { (void)unused; g_rc = clique_c_main(g_argc, g_argv); return NULL; }

static void on_alarm(int sig) {
    static const char msg[] = "TIMEOUT time limit reached\n";
    (void)sig;
    if (write(1, msg, sizeof msg - 1) < 0) { /* nothing else to do */ }
    _exit(4);
}

int main(int argc, char **argv) {
    pthread_attr_t attr;
    pthread_t th;
    int e;
    const char *lim = getenv("CLIQUE_TIME_LIMIT");
    g_argc = argc; g_argv = argv;
    if (lim && atoi(lim) > 0) { signal(SIGALRM, on_alarm); alarm((unsigned)atoi(lim)); }
    pthread_attr_init(&attr);
    e = pthread_attr_setstacksize(&attr, BIG_STACK_BYTES);
    if (e) { fprintf(stderr, "pthread_attr_setstacksize(%zu): %s\n", (size_t)BIG_STACK_BYTES, strerror(e)); return 5; }
    e = pthread_create(&th, &attr, runner, NULL);
    if (e) { fprintf(stderr, "pthread_create: %s\n", strerror(e)); return 5; }
    pthread_join(th, NULL);
    fflush(stdout);
    return g_rc;
}
