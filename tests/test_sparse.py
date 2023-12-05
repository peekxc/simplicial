import numpy as np
from splex import *

def test_boundary():
  K = filtration(zip([0,1,2,3,4,5], [0,1,2,[0,1],[0,2],[1,2]]))
  
  ## Test full boundary matrix 
  D_test = boundary_matrix(K).todense()
  D_true = np.array([
    [ 0,  0,  0,  1,  1,  0],
    [ 0,  0,  0, -1,  0,  1],
    [ 0,  0,  0,  0, -1, -1],
    [ 0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0],
    [ 0,  0,  0,  0,  0,  0]
  ])
  assert np.allclose(D_test - D_true, 0.0)

  ## Test vertex-edge 
  D1_test = boundary_matrix(K, p=1).todense()
  D1_true = np.array([
    [  1,  1,  0],
    [ -1,  0,  1],
    [  0, -1, -1],
  ])
  assert np.allclose(D1_test - D1_true, 0.0)

  S = simplicial_complex([[0,1,2], [2,3,4], [3,4,5]])
  K = filtration(enumerate(S))
  
  assert all(np.ravel(boundary_matrix(K, p=2).todense() == np.array([
    [ 1,  0,  0],
    [-1,  0,  0],
    [ 1,  0,  0],
    [ 0,  1,  0],
    [ 0, -1,  0],
    [ 0,  1,  1],
    [ 0,  0, -1],
    [ 0,  0,  1]
  ])))
  

def test_boundary_large():
  X = np.random.uniform(size=(30,2))
  K = rips_filtration(X, p=2)
  for p in range(0, 5):
    D = boundary_matrix(K, p=p)
    assert D.shape[0] == card(K,p-1) and D.shape[1] == card(K,p)

def test_boundary2_large():
  X = np.random.uniform(size=(150,2))
  K = rips_complex(X, radius=0.25, p=2)
  X = np.random.uniform(size=(150,2))
  K = rips_complex(X, radius=0.25, p=2)
  D = boundary_matrix(K, p=2)
  assert D.nnz == int(sx.card(K, 2) * 3)
  from collections import Counter
  col_counts = np.fromiter(Counter(D.col).values(), dtype=int)
  assert np.all(col_counts == 3)
