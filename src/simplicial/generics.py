## --- GENERICS --- 
import numpy as np 
# import networkx as nx
from .meta import *   # typing utilities for meta-programming
from .simplicial import *
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
  if isinstance(sigma, ComplexLike):
    return sigma.dim()
  return len(s) - 1

def boundary(s: Union[SimplexLike, ComplexLike]) -> Iterable['SimplexLike']:
  return combinations(s, len(s)-1)


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
