import numpy as np 
from splex import *


def test_st_construct_bench(benchmark):
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

# def test_simplex_bench(benchmark):
#   benchmark(lambda: [Simplex(np.random.choice(range(10), size=8)) for i in range(1000)])
#   assert True
    
# def test_boundary1_bench(benchmark):
#   from scipy.sparse import spmatrix
#   from itertools import combinations, chain
#   triangles = list(combinations(range(20),2))
#   S = simplicial_complex(triangles)
#   D1 = benchmark(boundary_matrix, S, p=1)
#   assert isinstance(D1, spmatrix),  "Is not sparse matrix"

# def test_boundary2_bench(benchmark): 
#   from scipy.sparse import spmatrix
#   from itertools import combinations, chain
#   triangles = list(combinations(range(16),3))
#   S = simplicial_complex(triangles)
#   D2 = benchmark(boundary_matrix, S, p=2)
#   assert isinstance(D2, spmatrix),  "Is not sparse matrix"