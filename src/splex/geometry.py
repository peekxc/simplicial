import numpy as np
from scipy.spatial.distance import pdist, squareform

from .generics import *
from .complexes import * 
from .filtrations import *
from .combinatorial import rank_combs, unrank_combs
from .predicates import *
from dataclassy import dataclass

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

## TODO: revamp to include index tracking with hirola 
def lower_star_weight(x: ArrayLike) -> Callable[SimplexConvertible, float]:
  def _weight(s: SimplexConvertible) -> float:
    return max(x[np.asarray(s)])
  return _weight

def flag_weight(x: ArrayLike, vertex_weights: Optional[ArrayLike] = None) -> Callable:
  pd = as_pairwise_dist(x)
  n = inverse_choose(len(pd), 2)
  vertex_weights = np.zeros(n) if vertex_weights is None else vertex_weights
  assert len(vertex_weights) == n, "Invalid vertex weights"
  @dataclass(frozen=True, slots=True, init=False, repr=False, eq=False)
  class _clique_weight:
    n: int = 0
    vertex_weights: np.ndarray = np.empty(0, dtype=np.float32)
    edge_weights: np.ndarray = np.empty(0, dtype=np.float32)
    def __init__(self, v: np.ndarray, pd: np.ndarray, n: int) -> None:
      object.__setattr__(self, 'n', n)
      object.__setattr__(self, 'vertex_weights', v)
      object.__setattr__(self, 'edge_weights', pd)
    def __call__(self, s: Union[SimplexConvertible, ArrayLike]) -> Union[float, np.ndarray]:
      if hasattr(s, "__array__") and is_complex_like(s):
        ## Handles numpy matrices of simplices OR array_convertible containers, so long as they are complex-like
        s = np.asarray(s)
        if s.ndim == 1:
          # print("hello")
          return np.ravel(self.vertex_weights[s])
        else: 
          if s.shape[1] == 2: 
            return self.edge_weights[rank_combs(s, n=n, order='lex')]
          elif s.shape[1] == 3:
            fw = np.zeros(s.shape[0])
            for i,j in combinations(range(s.shape[1]), 2):
              np.maximum(fw, self.edge_weights[rank_combs(s[:,[i,j]], n=self.n, order='lex')], out=fw)
            return fw
      elif is_simplex_like(s):
        if len(s) == 1: 
          return self.vertex_weights[int(s)] 
        else: 
          ind = np.fromiter((rank_lex(e, n=self.n) for e in combinations(s, 2)), dtype=np.uint32)
          return np.max(self.edge_weights[ind])
      else:
        # assert is_complex_like(s), "Input simplices must be complex like" # this is unneeded since not not be sized or repeatable
        rank_boundary = lambda f: np.array([rank_lex(sf, n=self.n) for sf in combinations(f, 2)], dtype=np.uint32)
        return np.array([np.max(self.edge_weights[rank_boundary(f)]) if dim(f) >= 1 else float(self.vertex_weights[f]) for f in s], dtype=float)
  C = _clique_weight(vertex_weights, pd, n)
  return C

## TODO: revamp to include support for arbitrary simplicial complexes via index tracking with hirola 
def lower_star_weight(x: ArrayLike) -> Callable:
  """Constructs a simplex-parameterized _Callable_ that evaluates its lower star value based on _x_. 

  Vertex labels are assumed to be 0-indexed for now. 
  
  If simplex-like, use 0-indexed vertex labels to index vertex values directly. 
  
  Otherwise assumes a 2d array of simplex labels is given and vectorizes the computation.
  """
  @dataclass(frozen=True, slots=True, init=False, repr=False, eq=False)
  class LS:
    vertex_weights: np.ndarray = np.empty(0, dtype=np.float32)

    def __init__(self, v: np.ndarray) -> None:
      object.__setattr__(self, 'vertex_weights', v)
    
    def __call__(self, s: Union[SimplexConvertible, ArrayLike]) -> Union[float, np.ndarray]:
      # assert hasattr(faces(S, 1), "__array__")
      s = np.asarray(s)
      return np.max(self.vertex_weights[s], axis=-1) ## vectorized form
      # if s.ndim == 2:
      #   return self.vertex_weights[s].max(axis=1) 
      # return np.max(self.vertex_weights[s])
    # def __array_function__(self, func, types, args, kwargs):
  return LS(x)

def rips_filtration(x: ArrayLike, radius: float = None, p: int = 1, **kwargs) -> FiltrationLike:
  pd = as_pairwise_dist(x)
  radius = enclosing_radius(pd) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  n = inverse_choose(len(pd), 2)
  st = SimplexTree([[i] for i in range(n)])
  st.insert(unrank_combs(ind, n=n, k=2, order="lex"))
  st.expand(p)
  f = flag_weight(pd)
  G = ((f([s]), s) for s in st)
  K = filtration(G, **kwargs)
  return K

def delaunay_complex(x: ArrayLike):
  from scipy.spatial import Delaunay
  dt = Delaunay(x)
  T = dt.simplices
  V = np.fromiter(range(x.shape[0]), dtype=np.int32)
  S = simplicial_complex(chain(V, T))
  return(S)


