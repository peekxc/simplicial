import numpy as np 
from splex import * 
from more_itertools import unique_everseen

def check_poset(S: ComplexLike):
  ## Reflexivity 
  for s in S: assert s <= s, "Simplex order not reflexive"

  ## Antisymmetry 
  for x, y in product(S, S):
    if x <= y and y <= x:
      assert x == y, "Simplex order not symmetric"

  ## Transitivity
  for x, y, z in product(S, S, S):
    if x <= y and y <= z:
      assert x <= z, "Simplex order not transitive"

  ## Test containment of faces 
  for s in S: 
    for face in faces(Simplex(s)):
      assert face in S

  return True 

def test_simplex():
  s = Simplex([0,1,2])
  assert isinstance(s, Simplex)
  assert isinstance(s, SimplexLike)
  assert isinstance(s, SimplexConvertible)

def test_simplicial_complex_api():
  for form in ["set", "tree", "rank"]:
    # S = simplicial_complex(form=form)
    # assert isinstance(S, ComplexLike)
    S = simplicial_complex([[0,1,2,3,4]], form=form)
    assert isinstance(S, ComplexLike)
    check_poset(S)

# def test_filtration_api():
#   for form in ["set", "tree", "rank"]:
#     # S = simplicial_complex(form=form)
#     # assert isinstance(S, ComplexLike)
#     K = filtration(enumerate(faces([[0,1,2,3,4]])), form=form)
#     assert isinstance(K, ComplexLike)
#     check_poset(K)

def test_set_complex():
  S = simplicial_complex([[0,1,2,3]], form="set")
  assert list(S.cofaces([0,1,2])) == [(0,1,2), (0,1,2,3)]
  S.remove([0,1,2,3])
  assert [0,1,2,3] not in S
  assert dim(S) == 2
  assert S.discard([0,1,2,3]) is None 
  assert S.discard([0,1]) is None 
  assert [0,1] not in S


## Testing reindexing capability 
def test_filtration():
  S = simplicial_complex([[0,1,2,3,4]], "set")
  assert isinstance(S, SetComplex)
  # K = filtration(S, "set_filtration")
  # assert isinstance(K, MutableFiltration)
  # L = K.copy()
  # K.reindex(lambda s: 10 + sum(s))
  # L_simplices = [tuple(s) for s in L.values()]
  # K_simplices = [tuple(s) for s in K.values()]
  # assert len(L_simplices) == len(K_simplices)
  # assert L_simplices != K_simplices
  # assert list(sorted(K_simplices)) == list(sorted(L_simplices))

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

def test_face_poset():
  from itertools import product
  S = simplicial_complex([[0,1,2,3,4]])
  check_poset(S)
  
def test_rips():
  from splex.geometry import flag_weight, delaunay_complex, rips_filtration
  X = np.random.uniform(size=(10,2))
  f = flag_weight(X)
  S = delaunay_complex(X)
  assert isinstance([f(s) for s in S], list)
  assert isinstance(filtration(S, f=f), FiltrationLike)

def test_rips():
  radius = 0.35
  X = np.random.uniform(size=(15,2))
  K = rips_filtration(X, radius)
  assert isinstance(K, FiltrationLike)

def test_boundary():
  K = filtration(enumerate([0,1,2,[0,1],[0,2],[1,2]]))
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

  D1_test = boundary_matrix(K, p=1).todense()
  D1_true = np.array([
    [  1,  1,  0],
    [ -1,  0,  1],
    [  0, -1, -1],
  ])
  assert np.allclose(D1_test - D1_true, 0.0)

  K = filtration([[0,1,2]], form="set")


def test_generics():
  assert list(unique_everseen([[0], [0], [1], [0,1]])) == [[0], [1], [0,1]]
  S = simplicial_complex([[0,1,2]])
  assert card(S) == (3,3,1)
  assert card(S,0) == 3
  assert dim(S) == 2
  assert list(faces(S)) == list(map(Simplex, [(0),(1),(2),(0,1),(0,2),(1,2),(0,1,2)]))
  assert list(faces(S,0)) ==  list(map(Simplex, [(0),(1),(2)]))
  K = filtration(S)
  assert card(K) == (3,3,1)
  assert card(K,0) == 3
  assert dim(K) == 2
  assert list(faces(K)) == list(map(Simplex, [(0),(1),(2),(0,1),(0,2),(1,2),(0,1,2)]))
  assert list(faces(K,0)) ==  list(map(Simplex, [(0),(1),(2)]))