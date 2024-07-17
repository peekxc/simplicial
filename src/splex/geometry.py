import numpy as np
import itertools as it
from scipy.spatial.distance import pdist, squareform

from .generics import *
from .filters import *
from .predicates import *
from .complexes import * 
from .filtrations import *
from combin import rank_to_comb, comb_to_rank, inverse_choose

def enclosing_radius(x: ArrayLike) -> float:
  """Returns the smallest 'r' such that the Rips complex on the union of balls of radius 'r' is contractible to a point. """
  if is_dist_like(x):
    assert is_distance_matrix(x) or is_pairwise_distances(x), "Must be valid distances"
    d = x if is_distance_matrix(x) else squareform(x)
    return 0.5*np.min(np.max(d, axis = 0))
  elif is_point_cloud(x):
    d = squareform(pdist(x))
    return 0.5*np.min(np.max(d, axis = 0))
  else:
    raise ValueError("Unknown input type")

def rips_complex(x: ArrayLike, radius: float = None, p: int = 1) -> FiltrationLike:
  """Constructs the Vietoris-Rips complex from _x_ by unioning balls of diameter at most 2 * _radius_ 
  
  Parameters: 
    x: point cloud, pairwise distance vector, or distance matrix
    radius: scale parameter for the Rips complex. 
    p: highest dimension of simplices to consider in the expansion. 
  
  Returns: 
    rips complex, returned as a simplex tree
  """ 
  from simplextree import SimplexTree
  pd = as_pairwise_dist(x)
  n = inverse_choose(len(pd), 2)
  radius = enclosing_radius(squareform(pd)) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  edges = rank_to_comb(ind, n=n, k=2, order="lex")
  st = SimplexTree([[i] for i in range(n)])
  st.insert(edges)
  st.expand(p)
  return st
  
def rips_filtration(x: ArrayLike, radius: float = None, p: int = 1, **kwargs) -> FiltrationLike:
  """Constructs a _p_-dimensional rips filtration from _x_ by unioning balls of diameter at most 2 * _radius_.
  """
  from simplextree import SimplexTree
  pd = as_pairwise_dist(x)
  radius = enclosing_radius(pd) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  n = inverse_choose(len(pd), 2)
  st = SimplexTree([[i] for i in range(n)])
  st.insert(rank_to_comb(ind, n=n, k=2, order="lex"))
  st.expand(p)
  f = flag_filter(pd)
  G = ((f([s]), s) for s in st)
  K = filtration(G, **kwargs)
  return K

def delaunay_complex(x: ArrayLike):
  from scipy.spatial import Delaunay
  dt = Delaunay(x)
  T = dt.simplices
  V = np.fromiter(range(x.shape[0]), dtype=np.int32)
  S = simplicial_complex(it.chain(V, T))
  return(S)


