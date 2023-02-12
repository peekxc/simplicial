import numpy as np 
from numpy.typing import ArrayLike
from scipy.sparse import coo_array
from collections.abc import Sized
from .meta import * 

# See: https://stackoverflow.com/questions/70381559/ensure-that-an-argument-can-be-iterated-twice
def _boundary(S: Iterable[SimplexLike], F: Optional[Sequence[SimplexLike]] = None):

  ## Load faces. If not given, by definition, the given p-simplices contain their boundary faces.
  if F is None: 
    assert not(S is iter(S)), "Simplex iterable must be repeatable (a generator is not sufficient!)"
    F = list(map(Simplex, set(chain.from_iterable([combinations(s, len(s)-1) for s in S]))))
  
  ## Ensure faces 'F' is indexable
  assert isinstance(F, Sequence), "Faces must be a valid Sequence (supporting .index(*) with SimplexLike objects!)"

  ## Build the boundary matrix from the sequence
  m = 0
  I,J,X = [],[],[] # row, col, data 
  for (j,s) in enumerate(map(Simplex, S)):
    if dim(s) > 0:
      I.extend([F.index(f) for f in s.faces(dim(s)-1)])
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

  Returns: 
    D := sparse matrix representing either the full or p-th boundary matrix (as List-of-Lists format)
  """
  if isinstance(p, tuple):
    return (boundary_matrix(K, pi) for pi in p)
  else: 
    assert p is None or isinstance(p, Integral), "p must be integer, or None"
    assert isinstance(K, ComplexLike) or isinstance(K, FiltrationLike), f"Unknown input type '{type(K)}'"
    if p is None:
      simplices = faces(K), faces(K)
      D = _boundary(simplices, simplices)
    else:
      p_simplices = K.faces(p=p)
      p_faces = list(K.faces(p=p-1))
      D = _boundary(p_simplices, p_faces)
    return D

