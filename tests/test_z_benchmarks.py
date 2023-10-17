import numpy as np 
from splex import *

## Benchmark inserting 500 triangles, not necessarily unique
def test_st_construct_bench(benchmark):
  from simplextree import SimplexTree
  F = np.random.choice(range(150), size=(500, 3), replace=True)
  S = simplicial_complex(F, form="tree")
  assert isinstance(S, SimplexTree)
  benchmark(lambda: simplicial_complex(F, form="tree"))

def test_rc_construct_bench(benchmark):
  F = np.random.choice(range(150), size=(500, 3), replace=True)
  S = simplicial_complex(F, form="rank")
  assert isinstance(S, RankComplex)
  benchmark(lambda: simplicial_complex(F, form="rank"))

def test_sc_construct_bench(benchmark):
  F = np.random.choice(range(150), size=(500, 3), replace=True)
  S = simplicial_complex(F, form="set")
  assert isinstance(S, SetComplex)
  benchmark(lambda: simplicial_complex(F, form="set"))

def test_simplex_bench(benchmark):
  simplices = benchmark(lambda: [Simplex(np.random.choice(range(10), size=8)) for i in range(1000)])
  assert all([isinstance(s, Simplex) for s in simplices])
    
def test_boundary1_bench(benchmark):
  from scipy.sparse import sparray
  from itertools import combinations, chain
  triangles = list(combinations(range(20),2))
  S = simplicial_complex(triangles)
  # assert isinstance(boundary_matrix(S, p=1), sparray)
  D1 = benchmark(boundary_matrix, S, p=1)
  assert isinstance(D1, sparray),  "Is not sparse matrix"

def test_boundary2_bench(benchmark): 
  from scipy.sparse import sparray
  from itertools import combinations, chain
  triangles = list(combinations(range(16),3))
  S = simplicial_complex(triangles)
  # assert isinstance(boundary_matrix(S, p=2), sparray)
  D2 = benchmark(boundary_matrix, S, p=2)
  assert isinstance(D2, sparray),  "Is not sparse matrix"

def test_boundary_full_bench(benchmark):
  from scipy.sparse import sparray
  from itertools import combinations, chain
  triangles = list(combinations(range(20),2))
  S = simplicial_complex(triangles)
  D = benchmark(boundary_matrix, S)
  assert isinstance(D, sparray),  "Is not sparse matrix"


#   def test_incr_modify():
#   np.random.seed(1234)
#   from simplextree import SimplexTree
#   S1, S2, S3 = SetComplex(), RankComplex(), SimplexTree()
#   for i in range(100): # 1000
#     k = np.random.choice(range(1,5))
#     # s = Simplex(np.random.choice(range(150), size=k, replace=False)) # ordered 
#     s = np.random.choice(range(150), size=k, replace=False)
#     S1.add(s)
#     S2.add(s)
#     S3.insert([s])
#     assert card(S1) == card(S2) and card(S2) == card(S3) 

#   for i in range(50): 
#     print(i)
#     # assert i != 25
#     k = np.random.choice(range(1,4))
#     s = np.random.choice(range(150), size=k, replace=False)
#     S1.add(s)
#     S2.add(s)
#     S3.insert([s])
#     assert card(S1) == card(S2) and card(S2) == card(S3) 
#     s = np.random.choice(range(150), size=k, replace=False) # 98 76
#     S1.discard(s)
#     S2.discard(s)
#     S3.remove([s])
#     # S3.remove([[98,76]])
#     assert card(S1) == card(S2) and card(S2) == card(S3)

# def benchmark_incr_modify():
#   import line_profiler
#   profile = line_profiler.LineProfiler()
#   profile.add_function(test_incr_modify)
#   profile.enable_by_count()
#   test_incr_modify()
#   profile.print_stats(output_unit=1e-3, stripzeros=True)
