import numpy as np 
from typing import *
from splex import * 

def validate_filtration(index_values: Iterable, simplices: Iterable, light: bool = True) -> bool:
  index_values = list(index_values)
  simplices = [Simplex(s) for s in simplices]
  for i, s in enumerate(simplices): 
    p = dim(s) - 1 if light and len(s) >= 2 else None
    assert all([simplices.index(face) <= i for face in faces(s, p)])
  return all([k1 <= k2 for k1, k2 in zip(index_values[:-1], index_values[1:])])

def test_set_filtration_simple():
  S = SetComplex([[0,1,2,3]])
  K = SetFiltration(enumerate(S))
  assert K.n_simplices == (4,6,4,1), "simplex cardinality tracking not working properly"
  assert [0,1,2,3] in K, "contains not working properly"
  assert np.all([K.index(s[1]) == i for i,s in enumerate(K)]), "indexing working properly"
  assert K.reindex(index_set = np.arange(len(K))) is None, "reindexing failed"
  assert list(K.indices()) == list(range(len(K))), "invalid index set"
  f = fixed_filter(S, np.arange(len(K))+1)
  assert K.reindex(f) is None, "function indexing failed"
  assert list(K.indices()) == list(range(1, len(K)+1)), "function indexing failed"


  # K.discard([0,1,2,3])

def test_rank_filtration_order():
  F = RankFiltration(zip([0,0,0,0,1,1,1], [[3], [2], [1], [0], [0,1], [1,2], [3,1]]))
  assert F[0] == (0.0, (0,))
  assert F[3] == (0.0, (3,))
  F.order = 'reverse colex'
  assert F[3] == (0.0, (0,))
  assert F[0] == (0.0, (3,))
  assert np.all(F.simplices['rank'] == np.array([3,2,1,0,4,2,0]))
  F.order = 'colex'
  assert np.all(F.simplices['rank'] == np.array([0,1,2,3,0,2,4]))
  F.order = 'lex'
  assert np.all(F.simplices['rank'] == np.array([0,1,2,3,0,3,4]))
  F.order = 'reverse lex'
  assert np.all(F.simplices['rank'] == np.array([3,2,1,0,4,3,0]))

def test_rank_filtration_simple():
  S = RankComplex([[0,1,2,3]])
  K = RankFiltration(enumerate(S))
  assert card(K) == (4,6,4,1), "simplex cardinality tracking not working properly"
  assert [0,1,2,3] in K, "contains not working properly"
  assert np.all([K.index(s[1]) == i for i,s in enumerate(K)]), "indexing working properly"

def test_filtration_api():
  S = simplicial_complex([[0,1,2,3]])
  assert isinstance(filtration(S, form="set"), SetFiltration)
  assert isinstance(filtration(S, form="rank"), RankFiltration)
  for f_type in ["set", "rank"]:
    K = filtration(S, f=lambda s: max(s), form=f_type)
    assert isinstance(K, FiltrationLike)
    assert validate_filtration(K.indices(), faces(K))

def test_set_filtration():
  S = simplicial_complex([[0,1,2,3]])
  K = SetFiltration(S, f=lambda s: max(s))
  assert sorted(faces(K)) == list(map(Simplex, [(0), (1), (0,1), (2), (0,2), (1,2), (0,1,2), (3), (0,3), (1,3), (2,3), (0,1,3), (0,2,3), (1,2,3), (0,1,2,3)]))
  assert list(K.indices()) == [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]
  assert (K == K.copy()) and id(K) != id(K.copy())
  assert dim(K) == 3
  from operator import itemgetter
  assert list(faces(K)) == list(map(itemgetter(1), iter(K)))
  assert format(K) == "3-d filtered complex with (4, 6, 4, 1)-simplices of dimension (0, 1, 2, 3)\nI: 0   ≤ 1   ≤ 1     ≤ 2   ≤ 2     ≤  ...  ≤ 3       ≤ 3        \nS: (0) ⊆ (1) ⊆ (0,1) ⊆ (2) ⊆ (0,2) ⊆  ...  ⊆ (1,2,3) ⊆ (0,1,2,3)\n"
  # K += [(2, Simplex([0,1,2]))]
  # assert len(K) == 15
  # K += [(5, Simplex([5]))]
  # assert len(K) == 16
  # K.clear()
  

