import numpy as np
import splex as sx

def test_boundary():
  K = sx.filtration(enumerate([[0],[1],[2],[0,1],[0,2],[1,2],[0,1,2]]))
  
  ## Test full boundary matrix 
  D_test = sx.boundary_matrix(K).todense()
  D_true = np.array([
    [ 0,  0,  0,  1,  1,  0,  0],
    [ 0,  0,  0, -1,  0,  1,  0],
    [ 0,  0,  0,  0, -1, -1,  0],
    [ 0,  0,  0,  0,  0,  0,  1],
    [ 0,  0,  0,  0,  0,  0, -1],
    [ 0,  0,  0,  0,  0,  0,  1],
    [ 0,  0,  0,  0,  0,  0,  0]
  ])
  assert np.allclose(D_test - D_true, 0.0)

  ## Test vertex-edge 
  D1_test = sx.boundary_matrix(K, p=1).todense()
  D1_true = np.array([
    [  1,  1,  0],
    [ -1,  0,  1],
    [  0, -1, -1],
  ])
  assert np.allclose(D1_test - D1_true, 0.0)

  S = sx.simplicial_complex([[0,1,2], [2,3,4], [3,4,5]])
  K = sx.filtration(enumerate(S))
  
  assert all(np.ravel(sx.boundary_matrix(K, p=2).todense() == np.array([
    [ 1,  0,  0],
    [-1,  0,  0],
    [ 1,  0,  0],
    [ 0,  1,  0],
    [ 0, -1,  0],
    [ 0,  1,  1],
    [ 0,  0, -1],
    [ 0,  0,  1]
  ])))
  
def test_boundary_colex():
  f_vals = np.array([0,0,0,0,3,3,4,4,5,5,5,5,5,5,5])
  s_vals = [[3],[2],[1],[0],[3,2],[1,0],[3,1],[2,0],[3,0],[2,1],[3,2,1],[3,2,0],[3,1,0],[2,1,0],[3,2,1,0]]
  K = sx.RankFiltration(zip(f_vals, s_vals))
  K.order = 'reverse colex'
  assert np.all([sx.Simplex(s1) == sx.Simplex(s2) for s1,s2 in zip(s_vals, sx.faces(K))])
  assert len(sx.faces(K,-1)) == 0
  for p in range(-2, 6):
    Dp = sx.boundary_matrix(K, p)
    assert Dp.shape == (sx.card(K,p-1), sx.card(K,p))
  # D1 = sx.boundary_matrix(K,1).todense() # both seem correct using the vertex ordering
  # D2 = sx.boundary_matrix(K,2).todense()


def test_boundary_large():
  X = np.random.uniform(size=(30,2))
  K = sx.rips_filtration(X, p=2)
  for p in range(0, 5):
    D = sx.boundary_matrix(K, p=p)
    assert D.shape[0] == sx.card(K,p-1) and D.shape[1] == sx.card(K,p)

def test_boundary2_large():
  X = np.random.uniform(size=(150,2))
  K = sx.rips_complex(X, radius=0.25, p=2)
  D = sx.boundary_matrix(K, p=2)
  assert D.nnz == int(sx.card(K, 2) * 3)
  from collections import Counter
  col_counts = np.array(list(Counter(D.col).values()))
  assert np.all(col_counts == 3)

  S = sx.RankComplex(K)
  D = sx.boundary_matrix(S, p=2)
  assert D.nnz == int(sx.card(K, 2) * 3)
  col_counts = np.array(list(Counter(D.col).values()))
  assert np.all(col_counts == 3)
