#pragma once
#include <vector>
#include <mutex>
namespace Concurrency {
template<class T> class concurrent_vector {
  std::vector<T> v; std::mutex m;
public:
  typedef typename std::vector<T>::iterator iterator;
  void push_back(const T& x){ std::lock_guard<std::mutex> g(m); v.push_back(x); }
  size_t size() const { return v.size(); }
  T& operator[](size_t i){ return v[i]; }
  iterator begin(){ return v.begin(); } iterator end(){ return v.end(); }
  void clear(){ v.clear(); }
};
}
