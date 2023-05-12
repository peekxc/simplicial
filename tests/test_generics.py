import numpy as np 
from splex.complexes import SimplexTree
from splex import * 
from more_itertools import unique_everseen


def test_faces():
  assert list(faces([0,1,2])) == [Simplex([0]), Simplex([1]), Simplex([2]), Simplex((0, 1)), Simplex((0, 2)), Simplex((1, 2)), Simplex((0, 1, 2))]

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