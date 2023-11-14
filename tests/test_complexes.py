import numpy as np 
from splex import *

def check_poset(S: ComplexLike):
  ## Reflexivity 
  for s in S: assert Simplex(s) <= Simplex(s), "Simplex order not reflexive"

  ## Antisymmetry 
  for x, y in product(S, S):
    x, y = Simplex(x), Simplex(y)
    if x <= y and y <= x:
      assert x == y, "Simplex order not symmetric"

  ## Transitivity
  for x, y, z in product(S, S, S):
    x, y, z = Simplex(x), Simplex(y), Simplex(z)
    if x <= y and y <= z:
      assert x <= z, "Simplex order not transitive"

  ## Test containment of faces 
  for s in S: 
    for face in faces(Simplex(s)):
      assert face in S

  return True 

def test_set_complex():
  S = SetComplex()
  S.add([[0,1,2,3]])
  assert list(S.cofaces([0,1,2])) == [(0,1,2), (0,1,2,3)]
  S.remove([0,1,2,3])
  assert [0,1,2,3] not in S
  assert dim(S) == 2
  assert S.discard([0,1,2,3]) is None 
  assert S.discard([0,1]) is None 
  assert [0,1] not in S
  assert len(list(S.cofaces([0,1]))) == 0
  assert card(S) == (4,5,2)

# def test_abc_complex():
#   from splex.complexes.Complex_ABCs import Complex
  # class MyComplex(Complex): pass 
  # K = MyComplex()
  # K.__format__()

def test_rank_complex():
  S = RankComplex([[0,1,2]])
  S.add([0,1,2,3])
  assert check_poset(S)
  assert card(S) == (4,6,4,1)
  # assert list(S.cofaces([0,1,2])) == [(0,1,2), (0,1,2,3)]
  S.remove([0,1,2,3])
  assert [0,1,2,3] not in S
  # assert S.remove([[0,1,2,3]]) == KeyError
  assert dim(S) == 2
  assert S.discard([0,1,2,3]) is None 
  assert S.discard([0,1]) is None 
  assert [0,1] not in S
  assert len(list(S.cofaces([0,1]))) == 0
  #assert np.all(np.array(S) == S.simplices), "Array conversion doesn't work"
  assert card(S) == (4,5,2)
  assert format(S) == '0 1 0 2 1 0 3 0 1 1 2\n    2   2 2   3 2 3 3\n          3     3    '
  assert np.all(faces(S, 1) == np.array([[0,2],[1,2],[0,3],[1,3],[2,3]], np.uint16))

def test_bulk_insertion():
  np.random.seed(1234)
  from simplextree import SimplexTree
  S1, S2, S3 = SetComplex(), RankComplex(), SimplexTree()
  triangles = np.random.choice(range(150), replace=True, size=3*150).reshape((150,3))
  S1 = SetComplex(triangles)
  S2 = RankComplex(triangles)
  S3 = SimplexTree(map(Simplex, triangles))
  assert card(S1) == card(S2) and card(S2) == card(S3)

