/* Forced-include shim: Linux stand-ins for the few Win32 calls in ramsey_df.cpp (cpu_init, Sleep,
   InterlockedIncrement). Thread count comes from env KUZ_THREADS (default 1). */
#pragma once
#include <x86intrin.h>
#define __rdtsc kz_rdtsc
#include <unistd.h>
#include <stdint.h>
#include <stdlib.h>
#include <string.h>
#include <mutex>
#include <vector>
typedef unsigned int DWORD; typedef int BOOL;
enum { RelationProcessorCore=0, RelationAll=0xffff };
#define ALL_PROCESSOR_GROUPS 0xffff
#define BELOW_NORMAL_PRIORITY_CLASS 0
struct KZ_GROUP_AFFINITY { uint64_t Mask; };
struct KZ_PROC { KZ_GROUP_AFFINITY GroupMask[1]; };
typedef struct { int Relationship; DWORD Size; KZ_PROC Processor; } SYSTEM_LOGICAL_PROCESSOR_INFORMATION_EX;
static inline int kz_threads(){ const char* e=getenv("KUZ_THREADS"); int t=e?atoi(e):1; return t<1?1:t; }
static inline int GetActiveProcessorCount(int){ return kz_threads(); }
static inline BOOL GetLogicalProcessorInformationEx(int, SYSTEM_LOGICAL_PROCESSOR_INFORMATION_EX* p, DWORD* len){
  int t=kz_threads(); for(int i=0;i<t;i++){ p[i].Relationship=RelationProcessorCore; p[i].Size=sizeof(*p); p[i].Processor.GroupMask[0].Mask=1ull<<i; }
  *len=t*sizeof(*p); return 1; }
static inline int GetCurrentProcess(){ return 0; }
static inline void SetProcessAffinityMask(int, uint64_t){}
static inline void SetPriorityClass(int, int){}
static inline long InterlockedIncrement(volatile long* p){ return __sync_add_and_fetch(p,1); }
static inline int InterlockedIncrement(volatile int* p){ return __sync_add_and_fetch(p,1); }
static inline unsigned long long InterlockedIncrement(volatile unsigned long long* p){ return __sync_add_and_fetch(p,1); }
static inline void Sleep(unsigned ms){ usleep(ms*1000u); }
#include <stdio.h>
#include <algorithm>
#define _fseeki64 fseeko64
static inline size_t min(int a, size_t b){ return (size_t)a < b ? (size_t)a : b; }
static inline size_t min(size_t a, int b){ return a < (size_t)b ? a : (size_t)b; }
static std::vector<bool> kz_empty_vb;
