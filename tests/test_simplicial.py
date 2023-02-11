import numpy as np 
from splex import * 
from splex import SimplicialComplex, MutableFiltration

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

  return True 

def test_simplex():
  s = Simplex([0,1,2])
  assert isinstance(s, Simplex)
  assert isinstance(s, SimplexLike)

def test_combinatorial_complex():
  S = SimplicialComplex([[0,1,2,3,4]])
  C = CombinatorialComplex(S)
  check_poset(C)

def test_combinatorial_filtration():
  S = SimplicialComplex([[0,1,2,3,4]])
  C = CombinatorialComplex(S)
  K = CombinatorialFiltration(S)

## Testing reindexing capability 
def test_filtration():
  S = SimplicialComplex([[0,1,2,3,4]])
  assert isinstance(S, SimplicialComplex)
  K = MutableFiltration(S)
  assert isinstance(K, MutableFiltration)
  # L = K.copy()
  # K.reindex(lambda s: 10 + sum(s))
  # L_simplices = [tuple(s) for s in L.values()]
  # K_simplices = [tuple(s) for s in K.values()]
  # assert len(L_simplices) == len(K_simplices)
  # assert L_simplices != K_simplices
  # assert list(sorted(K_simplices)) == list(sorted(L_simplices))

def test_boundary_matrix():
  S = SimplicialComplex([[0,1,2,3,4]])
  D = boundary_matrix(S)
  from scipy.sparse import spmatrix
  assert isinstance(D, spmatrix), "Is not sparse matrix"
  x = np.random.uniform(size=5, low = 0, high=5)
  F = MutableFiltration(S, lambda s: max(x[s]))
  assert isinstance(F, MutableFiltration)
  assert len(list(F.faces())) == len(F)

def test_face_poset():
  from itertools import product
  S = SimplicialComplex([[0,1,2,3,4]])
  check_poset(S)
  
# def test_rips():
#   from splex.constructions import flag_weight, delaunay_complex, rips_filtration
#   X = np.random.uniform(size=(10,2))
#   f = flag_weight(X)
#   S = delaunay_complex(X)
#   assert isinstance([f(s) for s in S], list)
#   assert isinstance(MutableFiltration(S, f=f), MutableFiltration)

# def test_rips():
#   radius = 0.35
#   X = np.random.uniform(size=(15,2))
#   K = rips_filtration(X, radius)
#   assert isinstance(K, MutableFiltration)


