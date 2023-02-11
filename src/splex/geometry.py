import numpy as np
from scipy.spatial.distance import pdist, squareform

from .meta import * 
from .simplextree import * 
from .combinatorial import rank_combs, unrank_combs
from .predicates import *

def enclosing_radius(x: ArrayLike) -> float:
  ''' Returns the smallest 'r' such that the Rips complex on the union of balls of radius 'r' is contractible to a point. '''
  if is_point_cloud(x):
    d = squareform(pdist(x))
    return 0.5*np.min(np.amax(d, axis = 0))
  elif is_dist_like(x):
    assert is_distance_matrix(x) or is_pairwise_distances(x), "Must be valid distances"
    d = x if is_distance_matrix(x) else squareform(x)
    return 0.5*np.min(np.amax(d, axis = 0))
  else:
    raise ValueError("Unknown input type")

def rips_complex(X: ArrayLike, radius: float = None) -> FiltrationLike:
  pd = pdist(X)
  radius = enclosing_radius(squareform(pd)) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  st = SimplexTree(unrank_combs(ind, n=X.shape[0], k=2, order="lex"))
  st.expand(2)
  ## TODO: replace 
  S = SimplicialComplex(list(map(Simplex, st.simplices())))
  return S

def flag_weight(x: ArrayLike, vertex_weights: Optional[ArrayLike] = None):
  if is_point_cloud(x):
    pd = pdist(x)
    n = x.shape[0]
  elif is_dist_like(distances):
    pd = np.tril(x) if is_distance_matrix(x) else x
    n = inverse_choose(len(pd), 2)
  else: 
    raise ValueError("Invalid input {type(x)}; not recongized")
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

def rips_filtration(X: ArrayLike, radius: float = None) -> FiltrationLike:
  pd = pdist(X)
  radius = enclosing_radius(squareform(pd)) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  st = SimplexTree(unrank_combs(ind, n=X.shape[0], k=2, order="lex"))
  st.expand(2)
  n = X.shape[0]
  def _clique_weight(s: SimplexLike) -> float:
    if len(s) == 1:
      return 0
    elif len(s) == 2:
      return pd[int(rank_combs([s], n=n, order='lex')[0])]
    else: 
      return max(pd[np.array(rank_combs(s.faces(1), n=X.shape[0], order='lex'), dtype=int)])
  simplices = list(map(Simplex, st.simplices()))
  filter_weights = np.array([_clique_weight(s) for s in simplices])
  K = MutableFiltration(zip(filter_weights, simplices))
  return K


def delaunay_complex(X: ArrayLike):
  from scipy.spatial import Delaunay
  dt = Delaunay(X)
  T = dt.simplices
  V = np.fromiter(range(X.shape[0]), dtype=np.int32)
  S = SimplicialComplex(chain(V, T))
  return(S)


