import numpy as np
from scipy.spatial.distance import pdist, squareform

from .generics import *
from .complexes import * 
from .filtrations import *
from .predicates import *
from combin import rank_to_comb, comb_to_rank, inverse_choose
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

def flag_weight(x: ArrayLike, vertex_weights: Optional[ArrayLike] = None) -> Callable:
  """Filter function factory method for constructing flag/clique filter functions. 

  Parameters: 
    x: point cloud, vector of pairwise weights, or square matrix. 
    vertex_weights: optional weights to use for vertices. Defaults to None, which sets vertex weights to 0.

  Returns: 
    callable which takes as input a simplex or set of simplices and returns their clique weights. 
  """
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
        if s.ndim == 1 or (1 in s.shape):
          # print("hello")
          return np.ravel(self.vertex_weights[s])
        else: 
          if s.shape[1] == 2: 
            ind = comb_to_rank(s, n=self.n, order='lex')
            return self.edge_weights[ind]
          else:
            fw = np.zeros(s.shape[0])
            for i,j in combinations(range(s.shape[1]), 2):
              np.maximum(fw, self.edge_weights[comb_to_rank(s[:,[i,j]], n=self.n, order='lex')], out=fw)
            return fw
      elif is_simplex_like(s):
        if len(s) == 1: 
          return self.vertex_weights[s] 
        else: 
          ind = np.array(comb_to_rank(combinations(s, 2), n=self.n, order='lex'), dtype=np.uint64)
          # ind = np.fromiter((rank_lex(e, n=self.n) for e in combinations(s, 2)), dtype=np.uint32)
          return np.max(self.edge_weights[ind])
      else:
        # assert is_complex_like(s), "Input simplices must be complex like" # this is unneeded since not not be sized or repeatable
        rank_boundary = lambda f: np.array(comb_to_rank(combinations(f, 2), n=self.n, order='lex'), dtype=np.uint64)
        return np.array([np.max(self.edge_weights[rank_boundary(f)]) if dim(f) >= 1 else np.take(self.vertex_weights[f],0) for f in s], dtype=float)
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
    
    def __call__(self, S: Union[SimplexConvertible, ArrayLike]) -> Union[float, np.ndarray]:
      if is_simplex_like(S):
        return np.max(self.vertex_weights[Simplex(S)]) # Simplices can be used for indexing!
      elif hasattr(S, "__array__") and is_complex_like(S):
        S = np.asarray(S)
        return np.max(self.vertex_weights[S], axis=-1) ## vectorized form
      else:
        assert isinstance(S, Iterable), "simplex iterable must be supplied"
        return np.array([np.max(self.vertex_weights[s]) for s in map(Simplex, S)])
  return LS(x)

def rips_filtration(x: ArrayLike, radius: float = None, p: int = 1, **kwargs) -> FiltrationLike:
  """Constructs a _p_-dimensional rips filtration from _x_ by unioning balls of diameter at most 2 * _radius_
  """
  from simplextree import SimplexTree
  pd = as_pairwise_dist(x)
  radius = enclosing_radius(pd) if radius is None else float(radius)
  ind = np.flatnonzero(pd <= 2*radius)
  n = inverse_choose(len(pd), 2)
  st = SimplexTree([[i] for i in range(n)])
  st.insert(rank_to_comb(ind, n=n, k=2, order="lex"))
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


