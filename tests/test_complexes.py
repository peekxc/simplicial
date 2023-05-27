import numpy as np 
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


def test_incr_modify():
  np.random.seed(1234)
  S1, S2, S3 = SetComplex(), RankComplex(), SimplexTree()
  for i in range(100): # 1000
    k = np.random.choice(range(1,5))
    # s = Simplex(np.random.choice(range(150), size=k, replace=False)) # ordered 
    s = np.random.choice(range(150), size=k, replace=False)
    S1.add(s)
    S2.add(s)
    S3.insert([s])
    assert card(S1) == card(S2) and card(S2) == card(S3) 

  for i in range(50): 
    print(i)
    # assert i != 25
    k = np.random.choice(range(1,4))
    s = np.random.choice(range(150), size=k, replace=False)
    S1.add(s)
    S2.add(s)
    S3.insert([s])
    assert card(S1) == card(S2) and card(S2) == card(S3) 
    s = np.random.choice(range(150), size=k, replace=False) # 98 76
    S1.discard(s)
    S2.discard(s)
    S3.remove([s])
    # S3.remove([[98,76]])
    assert card(S1) == card(S2) and card(S2) == card(S3)

def benchmark_incr_modify():
  import line_profiler
  profile = line_profiler.LineProfiler()
  profile.add_function(test_incr_modify)
  profile.enable_by_count()
  test_incr_modify()
  profile.print_stats(output_unit=1e-3, stripzeros=True)

def test_bulk_insertion():
  np.random.seed(1234)
  S1, S2, S3 = SetComplex(), RankComplex(), SimplexTree()
  triangles = np.random.choice(range(250), replace=True, size=3*150).reshape((150,3))
  S1 = SetComplex(triangles)
  S2 = RankComplex(triangles)
  S3 = SimplexTree(map(Simplex, triangles))
  assert card(S1) == card(S2) and card(S2) == card(S3)

