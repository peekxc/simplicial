from splex import *

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

def test_rank_complex():
  S = RankComplex([[0,1,2]])
  S.add([[0,1,2,3]])
  assert check_poset(S)
  assert card(S) == (4,6,4,1)
  # assert list(S.cofaces([0,1,2])) == [(0,1,2), (0,1,2,3)]
  S.remove([[0,1,2,3]])
  assert [0,1,2,3] not in S
  # assert S.remove([[0,1,2,3]]) == KeyError
  assert dim(S) == 2
  assert S.discard([[0,1,2,3]]) is None 
  assert S.discard([[0,1]]) is None 
  assert [0,1] not in S
  assert np.all(np.array(S) == S.simplices), "Array conversion doesn't work"
  assert card(S) == (4,4,5)
