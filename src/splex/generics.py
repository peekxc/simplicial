## --- GENERICS --- 
import numpy as np 
# import networkx as nx
from .meta import *   # typing utilities for meta-programming
from sortedcontainers import SortedDict, SortedSet
from dataclasses import dataclass
from numbers import Integral

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
    if s.dimension() > 0:
      I.extend([F.index(f) for f in s.faces(s.dimension()-1)])
      J.extend(repeat(j, s.dimension()+1))
      X.extend(islice(cycle([1,-1]), s.dimension()+1))
    m += 1
  D = coo_array((X, (I,J)), shape=(len(F), m)).tolil(copy=False)
  return D 


def dim(sigma: Union[SimplexLike, ComplexLike]) -> int:
  """
  Returns the dimension of a simplicial object, suitably defined 
  """
  if isinstance(sigma, ComplexLike): # hasattr(s, "boundary")
    return sigma.dim()
  return len(s) - 1

def boundary(s: Union[SimplexLike, ComplexLike], p: int = None, oriented: bool = False, **kwargs) -> Iterable['SimplexLike']:
  """
  Returns the boundary of a simplicial object, optionally signed.

  If _s_ has an existing method _s.boundary(p, oriented)_, then that method is called with additional keyword args _kwargs_.
  
  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike with dimension _p_, then a generator enumerating _(p-1)_-faces of _s_ is created. 
  - if _s_ is ComplexLike, then a sparse boundary matrix whose columns represent boundary chains is returned. 
  - if _s_ is FiltrationLike, then a sparse boundary matrix whose columns represent boundary chains in filtration order is returned.

  """
  if hasattr(s, "boundary"):
    return s.boundary(**kwargs)
  return combinations(s, len(s)-1)
  
def faces(s: Union[SimplexLike, ComplexLike], p: int = None) -> Iterable['SimplexLike']:
  """
  Returns the faces of a simplicial object, optionally restricted by dimension.

  If _s_ has an existing method _s.faces(p)_, then that method is called with additional keyword args _kwargs_.
  
  Otherwise, the behavior of this function depends on the type-class of _s_. Namely, 
  - if _s_ is SimplexLike, then a generator enumerating _p_-combinations of _s_ is created. 
  - if _s_ is ComplexLike, then a generator enumerating _p_-faces of _s_ is created. 
  - if _s_ is FiltrationLike, then a generator enumerating _p_-faces of _s_ in filtration order is created.
  """
  if hasattr(s, "faces"):
    return s.faces(p)
  assert isinstance(s, SimplexLike)
  k = len(s)
  if p is None:
    return (combinations(s, k-i) for i in reversed(range(1, k)))
  else:
    assert isinstance(p, Integral), f"Invalid type {type(p)}; dimension 'p' must be integral type"
    return (combinations(s, p+1))
  ## TODO: handle ComplexLike



# def boundary_matrix(K: Union[SimplicialComplex, MutableFiltration, Iterable[tuple]], p: Optional[Union[int, tuple]] = None):
#   """
#   Returns the ordered p-th boundary matrix of a simplicial complex 'K'

#   Return: 
#     D := sparse matrix representing either the full or p-th boundary matrix (as List-of-Lists format)
#   """
#   from collections.abc import Sized
#   if isinstance(p, tuple):
#     return (boundary_matrix(K, pi) for pi in p)
#   else: 
#     assert p is None or isinstance(p, Integral), "p must be integer, or None"
#     if isinstance(K, SimplicialComplex) or isinstance(K, MutableFiltration):
#       if p is None:
#         simplices = list(K.values())
#         D = _boundary(simplices, simplices)
#       else:
#         p_simplices = K.faces(p=p)
#         p_faces = list(K.faces(p=p-1))
#         D = _boundary(p_simplices, p_faces)
#     else: 
#       raise ValueError("Invalid input")
#     return D
