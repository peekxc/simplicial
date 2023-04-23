import numpy as np 
from splex import Simplex


def test_simplex_bench(benchmark):
  benchmark([Simplex(np.random.choice(range(10), size=8)) for i in range(1000)])
  assert True
    
def test_boundary1_bench(benchmark):
  from scipy.sparse import spmatrix
  from itertools import combinations, chain
  triangles = list(combinations(range(20),2))
  S = simplicial_complex(triangles)
  D1 = benchmark(boundary_matrix, S, p=1)
  assert isinstance(D1, spmatrix),  "Is not sparse matrix"

def test_boundary2_bench(benchmark): 
  from scipy.sparse import spmatrix
  from itertools import combinations, chain
  triangles = list(combinations(range(16),3))
  S = simplicial_complex(triangles)
  D2 = benchmark(boundary_matrix, S, p=2)
  assert isinstance(D2, spmatrix),  "Is not sparse matrix"