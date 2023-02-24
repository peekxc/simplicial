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

