import numpy as np 
from splex import * 
from splex.geometry import * 

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

## TODO: improve this massively
def test_rips():
  X = np.random.uniform(size=(15,2))
  assert is_complex_like(rips_complex(X))
  assert is_filtration_like(rips_filtration(X))
  from scipy.spatial.distance import pdist, squareform
  assert is_complex_like(rips_complex(pdist(X)))
  assert is_complex_like(rips_complex(squareform(pdist(X))))  
  assert is_filtration_like(rips_filtration(pdist(X)))
  assert is_filtration_like(rips_filtration(squareform(pdist(X))))

