import numpy as np 
from typing import *
from splex import * 
from splex.filtrations import * 


def validate_filtration(index_values: Iterable, simplices: Iterable, light: bool = True) -> bool:
  index_values = list(index_values)
  simplices = list(simplices)
  for i, s in enumerate(simplices): 
    p = dim(s) - 1 if light and len(s) >= 2 else None
    assert all([simplices.index(face) <= i for face in s.faces(p)])
  return all([k1 <= k2 for k1, k2 in zip(index_values[:-1], index_values[1:])])

def test_filtration_api():
  S = simplicial_complex([[0,1,2,3]])
  assert isinstance(filtration(S, form="set"), SetFiltration)
  assert isinstance(filtration(S, form="rank"), RankFiltration)
  K = SetFiltration(S, f=lambda s: max(s))
  assert isinstance(K, SetFiltration)
  m_vals = [max(s) for s in K.values()]
  assert sorted(m_vals) == m_vals
  assert validate_filtration(K.keys(), faces(K))

def test_set_filtration():
  S = simplicial_complex([[0,1,2,3]])
  K = SetFiltration(S, f=lambda s: max(s))
  assert sorted(list(K.values())) == list(map(Simplex, [(0), (1), (0,1), (2), (0,2), (1,2), (0,1,2), (3), (0,3), (1,3), (2,3), (0,1,3), (0,2,3), (1,2,3), (0,1,2,3)]))
  assert list(K.keys()) == [0, 1, 1, 2, 2, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3]
  assert (K == K.copy()) and id(K) != id(K.copy())
  assert dim(K) == 3
  assert list(faces(K)) == list(K.values())
  assert isinstance(K.get(3), SortedSet)
  assert list(K.get(3)) == list(filter(lambda s: 3 in s, K.values()))
  assert list(zip(K.keys(), K.values())) == list(K.items())
  assert format(K) == "3-d filtered complex with (4, 6, 4, 1)-simplices of dimension (0, 1, 2, 3)\nI: 0   ≤ 1   ≤ 1     ≤ 2   ≤ 2     ≤  ...  ≤ 3       ≤ 3        \nS: (0) ⊆ (1) ⊆ (0,1) ⊆ (2) ⊆ (0,2) ⊆  ...  ⊆ (1,2,3) ⊆ (0,1,2,3)\n"
  K += [(2, Simplex([0,1,2]))]
  assert len(K) == 15
  K += [(5, Simplex([5]))]
  assert len(K) == 16
  # K.clear()
  