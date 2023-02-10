import numpy as np 
from splex import * 
from splex import SimplicialComplex, MutableFiltration

def test_simplex():
  s = Simplex([0,1,2])
  assert isinstance(s, Simplex)
  assert isinstance(s, SimplexLike)

def test_combinatorial_complex():
  S = SimplicialComplex([[0,1,2,3,4]])
  C = CombinatorialComplex(S)

def test_combinatorial_filtration():
  S = SimplicialComplex([[0,1,2,3,4]])
  C = CombinatorialComplex(S)
  K = CombinatorialFiltration(S)

def test_rips():
  pass 

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

def test_rips():
  # radius = 0.35
  # X = np.random.uniform(size=(15,2))
  # from scipy.spatial.distance import pdist
  # pd = pdist(X)
  # D = squareform(pd)
  # radius = enclosing_radius(squareform(pd)) if radius is None else float(radius)
  # ind = np.flatnonzero(pd <= 2*radius)
  # st = SimplexTree(unrank_combs(ind, n=X.shape[0], k=2, order="lex"))
  # st.expand(2)
  # n = X.shape[0]
  # def _clique_weight(s: SimplexLike) -> float:
  #   if len(s) == 1:
  #     return 0
  #   elif len(s) == 2:
  #     return pd[int(rank_combs([s], n=n, order='lex')[0])]
  #   else: 
  #     return max(pd[np.array(rank_combs(s.faces(1), n=X.shape[0], order='lex'), dtype=int)])
  # simplices = list(map(Simplex, st.simplices()))
  # filter_weights = np.array([_clique_weight(s) for s in simplices])
  # K = MutableFiltration(zip(filter_weights, simplices))
  return K


def test_face_poset():
  from itertools import product
  S = SimplicialComplex([[0,1,2,3,4]])

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