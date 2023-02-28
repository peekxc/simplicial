import numpy as np
from scipy.spatial.distance import pdist, squareform

from .generics import *
from .complexes import * 
from .filtrations import *
from .combinatorial import rank_combs, unrank_combs
from .predicates import *

def as_pairwise_dist(x: ArrayLike) -> ArrayLike:
  if is_point_cloud(x):
    pd = pdist(x)
  elif is_dist_like(x):
    pd = np.tril(x) if is_distance_matrix(x) else x
  else: 
    raise ValueError("Unknown input shape 'x' ")
  return pd

def enclosing_radius(x: ArrayLike) -> float:
  """Returns the smallest 'r' such that the Rips complex on the union of balls of radius 'r' is contractible to a point. """
  if is_point_cloud(x):
    d = squareform(pdist(x))
    return 0.5*np.min(np.amax(d, axis = 0))
  elif is_dist_like(x):
    assert is_distance_matrix(x) or is_pairwise_distances(x), "Must be valid distances"
    d = x if is_distance_matrix(x) else squareform(x)
    return 0.5*np.min(np.amax(d, axis = 0))
  else:
    raise ValueError("Unknown input type")

def rips_complex(x: ArrayLike, radius: float = None, p: int = 1) -> FiltrationLike:
  pd = as_pairwise_dist(x)
  radius = enclosing_radius(squareform(pd)) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  st = SimplexTree(unrank_combs(ind, n=x.shape[0], k=2, order="lex"))
  st.expand(p)
  return st

def flag_weight(x: ArrayLike, vertex_weights: Optional[ArrayLike] = None) -> Callable:
  pd = as_pairwise_dist(x)
  n = inverse_choose(len(pd), 2)
  vertex_weights = np.zeros(n) if vertex_weights is None else vertex_weights
  assert len(vertex_weights) == n, "Invalid vertex weights"
  def _clique_weight(s: SimplexLike) -> float:
    if len(s) == 1:
      return float(vertex_weights[s])
    elif len(s) == 2:
      return float(pd[int(rank_combs([s], n=n, order='lex')[0])])
    else: 
      return float(max(pd[np.array(rank_combs(faces(s,1), n=n, order='lex'), dtype=int)]))
  return _clique_weight

def rips_filtration(x: ArrayLike, radius: float = None, p: int = 1, **kwargs) -> FiltrationLike:
  pd = as_pairwise_dist(x)
  radius = enclosing_radius(pd) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  n = inverse_choose(len(pd), 2)
  st = SimplexTree([[i] for i in range(n)])
  st.insert(unrank_combs(ind, n=n, k=2, order="lex"))
  st.expand(p)
  f = flag_weight(pd)
  G = ((f(s), s) for s in st)
  K = filtration(G, **kwargs)
  return K

def delaunay_complex(x: ArrayLike):
  from scipy.spatial import Delaunay
  dt = Delaunay(x)
  T = dt.simplices
  V = np.fromiter(range(x.shape[0]), dtype=np.int32)
  S = simplicial_complex(chain(V, T))
  return(S)


