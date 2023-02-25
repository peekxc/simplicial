import numpy as np 
from splex import * 

def test_delaunay():
  X = np.random.uniform(size=(15,2))
  assert isinstance(delaunay_complex(X), ComplexLike)

## TODO: improve this massively
def test_rips():
  X = np.random.uniform(size=(15,2))
  assert isinstance(rips_complex(X), ComplexLike)
  assert isinstance(rips_filtration(X), FiltrationLike)
  from scipy.spatial.distance import pdist, squareform
  assert isinstance(rips_complex(pdist(X)), ComplexLike)
  assert isinstance(rips_complex(squareform(pdist(X))), ComplexLike)
