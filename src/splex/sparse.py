import numpy as np 
from numpy.typing import ArrayLike
from scipy.sparse import coo_array, spmatrix
from collections.abc import Sized
from array import array
from .generics import *
from .predicates import *


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

def _fast_boundary(simplices: Iterable[SimplexConvertible], dtype) -> spmatrix:
  assert len(dtype) == 2
  from hirola import HashTable
  if dtype[1] == 1:
    return coo_array((0, len(simplices)), dtype=dtype[0])
  elif dtype[1] == 2:
    S_arr = np.fromiter(simplices, dtype=dtype)
    m = S_arr.shape[0]
    h = HashTable((3*m)*1.25, dtype=S_arr.dtype)
    ind = np.arange(S_arr.shape[1]).astype(int)
    I,J,X = array('I'), array('I'), array('i')
    for i, idx in enumerate(combinations(ind, len(ind)-1)):
      I.extend(h.add(S_arr[:,int(idx[0])]))
      J.extend(range(m))
      X.extend(repeat((-1)**i, m))
    return coo_array((X, (I,J)), shape=(len(h.keys), m))
  else:
    S_arr = np.fromiter(simplices, dtype=dtype)
    m = S_arr.shape[0]
    h = HashTable((3*m)*1.25, dtype=(S_arr.dtype, S_arr.shape[1]-1))
    ind = np.arange(S_arr.shape[1]).astype(int)
    #I, J, X = [],[],[]
    I,J,X = array('I'), array('I'), array('i')
    for i, idx in enumerate(combinations(ind, len(ind)-1)):
      I.extend(h.add(S_arr[:,idx]))
      J.extend(range(m))
      X.extend(repeat((-1)**i, m))
    return coo_array((X, (I,J)), shape=(len(h.keys), m))


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
  for (j,s) in enumerate(S):
    if dim(s) > 0:
      I.extend([F.index(f) for f in faces(s, dim(s)-1)])
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
    assert p is None or isinstance(p, Integral), "p must be integer, or None"
    assert isinstance(K, ComplexLike) or isinstance(K, FiltrationLike), f"Unknown input type '{type(K)}'"
    if p is None:
      simplices = list(faces(K)) # to ensure repeatable
      D = _boundary(simplices)
    else:
      # p_simplices = faces(K, p=p)
      # p_faces = list(faces(K, p=p-1))
      # D = _boundary(p_simplices, p_faces)
      D = _fast_boundary(faces(K, p=p), dtype=(np.uint16, p+1))
    return D

