import numpy as np 
from numpy.typing import ArrayLike
from scipy.sparse import coo_array, spmatrix
from collections.abc import Sized
from array import array
from .generics import *
from .predicates import *
from .Simplex import Simplex

from more_itertools import flatten, collapse, chunked, unique_everseen 

# def iterable2sequence(S: Iterable[Hashable], dtype): # dtype = (np.uint16, 3)
#   """Converts an arbitrary iterable of homogenous types to Sequence"""
#   assert dtype is not None
#   from hirola import HashTable
#   S_arr = np.fromiter(S, dtype=dtype)
#   h = HashTable(len(S_arr)*1.15, dtype=dtype)
#   h.add(S_arr)

#   I,J in combinations(S_arr.T, S_arr.shape[1]-1)
#   S_arr[]
# qr = np.array(rank_combs(S), dtype=np.uint64)

def _fast_boundary(S: Iterable[SimplexConvertible], F: Iterable[SimplexConvertible], dtype) -> spmatrix:
  assert len(dtype) == 2
  from hirola import HashTable
  # S_arr = np.fromiter(S, dtype=dtype) if dtype[1] > 1 else np.fromiter(collapse(S), dtype=dtype[0])
  S_arr = np.atleast_2d(S).astype(np.uint32) if len(S) > 0 else np.empty((0,0)).astype(np.uint32)
  F_arr = np.atleast_2d(F).astype(np.uint32) if len(F) > 0 else np.empty((0,0)).astype(np.uint32)
  if S_arr.ndim > 1:
    S_arr.sort(axis=1) ## Ensure lex order *on vertices*
    F_arr.sort(axis=1) ## Ensure lex order *on vertices*
  m, q = S_arr.shape
  n, p = F_arr.shape
  # F_arr = np.fromiter(F, dtype=(S_arr.dtype, d-1)) if d > 2 else np.fromiter(collapse(F), dtype=S_arr.dtype)
  if m == 0 or n == 0:
    return coo_array((n, m), dtype=dtype[0])
    # return coo_array((S_arr.shape[0], S_arr.shape[0]), dtype=dtype[0])
  else:
    ## Use euler characteristic bound
    d = q
    tbl_sz = max(max((3*m)*1.35, 16), F_arr.shape[0]*1.25) + 16
    h = HashTable(tbl_sz, dtype=(S_arr.dtype, d-1)) if d > 2 else HashTable(tbl_sz, dtype=S_arr.dtype)
    h.add(F_arr)
    ind = np.arange(d).astype(int)
    I = np.empty(m*d, dtype=S_arr.dtype)
    J = np.empty(m*d, dtype=S_arr.dtype)
    X = np.empty(m*d, dtype=int)
    CI = np.fromiter(range(m), dtype=int).astype(S_arr.dtype)

    ## Column-wise assignnment
    for i, idx in enumerate(combinations(ind, len(ind)-1)):
      f_ind = h[S_arr[:,idx]] if d > 2 else np.ravel(h[S_arr[:,idx]]) ## get rows in (0,1)
      I[i*m:(i+1)*m] = f_ind                                          ## row indices
      J[i*m:(i+1)*m] = CI                                             ## col indices
      X[i*m:(i+1)*m] = np.repeat((-1)**i, m)                          ## always choose lex order (?)
    # X = np.fromiter(flatten([(-1)**np.argsort(I[J == j]) for j in range(m)]), dtype=int)
    # X = np.empty(m*d, dtype=int)
    # for j in range(m):
    #   X[J==j] = (-1)**np.argsort(I[J == j]) ## this is wrong 
    D = coo_array((X, (I,J)), shape=(len(h.keys), m))
    return D


def _boundary(S: Iterable[SimplexConvertible], F: Optional[Sequence[SimplexConvertible]] = None):
  ## Load faces. If not given, by definition, the given p-simplices contain their boundary faces.
  if F is None: 
    assert is_repeatable(S), "Simplex iterable must be repeatable (a generator is not sufficient!)"
    F = list(faces(S))
  
  ## Ensure faces 'F' is indexable
  assert isinstance(F, Sequence), "Faces must be a valid Sequence (supporting .index(*) with SimplexLike objects!)"

  ## Build the boundary matrix from the sequence
  m = 0
  I,J,X = [],[],[] # row, col, data 
  face_dict = { s : i for i,s in enumerate(F) }
  for (j,s) in enumerate(S):
    if dim(s) > 0:
      # I.extend([F.index(f) for f in faces(s, dim(s)-1)]) ## TODO: this is painfully slow
      I.extend([face_dict[f] for f in faces(s, dim(s)-1)])
      J.extend(repeat(j, dim(s)+1))
      X.extend(islice(cycle([1,-1]), dim(s)+1))
    m += 1
  D = coo_array((X, (I,J)), shape=(len(F), m)).tolil(copy=False)
  return D 

## TODO: investigate whether to make a 'ChainLike' for extension with 'BoundaryChain'?
## Or maybe its fine to just rely on something with __index__
## class Chain(SupportsIndex[int], [Coefficient], Protocol):
##    def __init__(orientation = ...)
##    def __iter__() -> tuple[int, Coefficient]:
##    def __add__(Chain) -> Chain
##    def __iadd__(Chain) -> None
##    def pivot() -> (int, coefficient) [for homology]
##    def index(SimplexConvertible) -> int 
## something like chain(s: SimplexLike, c: ComplexLike, oriented: bool) -> ndarray, or generator (index, value)
## complexLike could be overloaded to handle .index(), checked if Sequence[SimplexLike] or if just Container[int] (+implying)
def boundary_matrix(K: Union[ComplexLike, FiltrationLike], p: Optional[Union[int, tuple]] = None):
  """
  Constructs a sparse boundary matrix of a given simplicial object _K_

  Parameters: 
    K: simplicial complex (optionally filtered) or ComplexLike. 
    p: dimension of the p-chains to form the columns. 
  
  Returns: 
    D: sparse matrix representing either the full or p-th boundary matrix (as List-of-Lists format)
  """
  if isinstance(p, tuple):
    return (boundary_matrix(K, pi) for pi in p)
  else: 
    assert p is None or isinstance(p, Integral), "p must be non-negative integer, or None"
    assert isinstance(K, ComplexLike) or isinstance(K, FiltrationLike), f"Unknown input type '{type(K)}'"
    if p is None:
      simplices = list(faces(K)) # to ensure repeatable
      D = _boundary(simplices)
    else:
      p_simplices = list(map(Simplex, faces(K, p=p)))
      p_faces = list(map(Simplex, faces(K, p=p-1)))
      D = _fast_boundary(p_simplices, p_faces, dtype=(np.uint32, p+1))
    return D

## It's enough to just manipulate the row, col, indices of a coo array from the boundary matrix
def coboundary_matrix():
  pass 
  # D1.shape[1]-np.flip(D1.col)-1, D1.shape[0]-np.flip(D1.row)-1