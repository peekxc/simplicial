import numpy as np 
from splex import *
from splex.geometry import lower_star_weight, flag_weight, rips_complex

def test_delaunay():
  X = np.random.uniform(size=(15,2))
  assert isinstance(delaunay_complex(X), ComplexLike)

def test_lower_star_array():
  S = simplicial_complex([[0,1,2,3,4,5]], form="rank")
  assert card(S, 0) == 6
  vertex_weights = np.arange(card(S,0))*0.10
  f = lower_star_weight(vertex_weights)
  f1 = np.array([f(s) for s in faces(S,1)])
  f2 = f(faces(S, 1))
  assert all(f1 == f2)

def test_flag_weight():
  from scipy.spatial.distance import pdist
  S = simplicial_complex([[0,1,2,3,4,5]], form="rank")
  X = np.random.uniform(size=(card(S,0),2))
  f = flag_weight(pdist(X))
  assert all([np.isclose(f([(i,j)]), np.linalg.norm(X[i] - X[j])) for i,j in faces(S,1)])
  assert len(f(faces(S))) == len(S)
  assert len(f(S)) == len(S)
  assert isinstance(f(faces(S,1)), np.ndarray) and len(f(faces(S,1))) == card(S,1)
  assert isinstance(f(faces(S,2)), np.ndarray) and len(f(faces(S,2))) == card(S,2)
  ## TODO: to pass the tests, bring rmap / itertools back into splex

## TODO: improve this massively
def test_rips():
  X = np.random.uniform(size=(25,2))
  assert is_complex_like(rips_complex(X))
  assert is_filtration_like(rips_filtration(X))
  from scipy.spatial.distance import pdist, squareform
  assert is_complex_like(rips_complex(pdist(X)))
  assert is_complex_like(rips_complex(squareform(pdist(X))))  
  assert is_filtration_like(rips_filtration(pdist(X)))
  assert is_filtration_like(rips_filtration(squareform(pdist(X))))
  assert card(rips_complex(pdist(X), radius = 0.0), 0) == len(X)

